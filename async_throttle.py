#!/usr/bin/env python3
"""
异步 HTTP 客户端限流包装器 - 基于 EVO Map 热门 Capsule 实现

EVO Map Capsule ID: sha256:d6f0e5a397a95d1cc8c9fb1c63fc2093a32fb6548f52119f874d160684c36067
置信度: 99%，使用次数: 32,911，GDI: 71.6

核心问题：异步代码可能同时发起数千连接，耗尽文件描述符，压垮下游服务
解决方案：信号量 + 连接池双重限流
"""

import asyncio
import time
from typing import Optional, Dict, Any, List, Union
import logging
from dataclasses import dataclass
from contextlib import asynccontextmanager

try:
    import httpx
    from httpx import AsyncClient, Response, Timeout
except ImportError:
    print("警告：需要安装 httpx 库：pip install httpx")
    httpx = None

logger = logging.getLogger(__name__)


@dataclass
class ThrottleStats:
    """限流统计"""
    total_requests: int = 0
    successful_requests: int = 0
    failed_requests: int = 0
    total_wait_time: float = 0.0
    max_concurrent: int = 0
    current_concurrent: int = 0


class CircuitBreaker:
    """断路器模式 - 防止持续失败调用"""
    
    def __init__(
        self,
        failure_threshold: int = 5,      # 连续失败次数阈值
        reset_timeout: float = 30.0,     # 重置超时（秒）
        half_open_max_requests: int = 3,  # 半开状态最大请求数
    ):
        self.failure_threshold = failure_threshold
        self.reset_timeout = reset_timeout
        self.half_open_max_requests = half_open_max_requests
        
        self.failures = 0
        self.state = "closed"  # closed, open, half-open
        self.last_failure_time: Optional[float] = None
        self.half_open_attempts = 0
        
    def can_execute(self) -> bool:
        """检查是否允许执行"""
        now = time.time()
        
        if self.state == "closed":
            return True
            
        elif self.state == "open":
            if self.last_failure_time and (now - self.last_failure_time) >= self.reset_timeout:
                # 超时，进入半开状态
                self.state = "half-open"
                self.half_open_attempts = 0
                logger.info("断路器：超时，进入半开状态")
                return True
            return False
            
        elif self.state == "half-open":
            if self.half_open_attempts < self.half_open_max_requests:
                return True
            return False
            
        return False
    
    def on_success(self):
        """请求成功"""
        if self.state == "half-open":
            # 半开状态下成功，关闭断路器
            self.state = "closed"
            self.failures = 0
            self.half_open_attempts = 0
            logger.info("断路器：半开状态下成功，关闭断路器")
        elif self.state == "closed":
            # 正常状态下成功，重置失败计数
            self.failures = 0
            
    def on_failure(self):
        """请求失败"""
        self.failures += 1
        self.last_failure_time = time.time()
        
        if self.state == "half-open":
            # 半开状态下失败，重新打开断路器
            self.state = "open"
            self.half_open_attempts = 0
            logger.warning("断路器：半开状态下失败，重新打开断路器")
        elif self.state == "closed" and self.failures >= self.failure_threshold:
            # 达到失败阈值，打开断路器
            self.state = "open"
            logger.warning(f"断路器：达到失败阈值 {self.failure_threshold}，打开断路器")
            
    def get_state(self) -> str:
        """获取当前状态"""
        return self.state


class ThrottledClient:
    """
    生产级异步 HTTP 客户端，支持信号量限流和连接池控制
    
    特性：
    1. 信号量控制并发协程数
    2. TCP 连接池限制
    3. 断路器模式防止持续失败
    4. 重试逻辑
    5. 详细统计信息
    6. 异常安全
    
    参考 EVO Map Capsule 代码模式：
    ```
    async with self.sem:  # 信号量限流
        async with self.session.get(url) as resp:
            return await resp.json()
    ```
    """
    
    def __init__(
        self,
        max_concurrent: int = 50,           # 最大并发请求数
        max_connections: int = 100,         # 最大 TCP 连接数
        timeout: float = 30.0,              # 请求超时时间
        retries: int = 3,                   # 重试次数
        retry_delay: float = 1.0,           # 重试延迟（秒）
        rate_limit_per_sec: Optional[int] = None,  # 每秒速率限制
        circuit_breaker: bool = True,       # 启用断路器
    ):
        """
        初始化限流客户端
        
        Args:
            max_concurrent: 最大并发请求数（信号量控制）
            max_connections: 最大 TCP 连接数（连接池控制）
            timeout: 请求超时时间（秒）
            retries: 重试次数
            retry_delay: 重试延迟（秒）
            rate_limit_per_sec: 每秒请求数限制，None 表示无限制
            circuit_breaker: 是否启用断路器
        """
        if httpx is None:
            raise ImportError("需要安装 httpx 库：pip install httpx")
            
        self.max_concurrent = max_concurrent
        self.max_connections = max_connections
        self.timeout = timeout
        self.retries = retries
        self.retry_delay = retry_delay
        
        # 信号量控制并发协程数
        self.semaphore = asyncio.Semaphore(max_concurrent)
        
        # 速率限制（令牌桶）
        self.rate_limit_per_sec = rate_limit_per_sec
        self._rate_tokens = rate_limit_per_sec if rate_limit_per_sec else float('inf')
        self._rate_last_update = time.time()
        self._rate_lock = asyncio.Lock()
        
        # 断路器
        self.circuit_breaker_enabled = circuit_breaker
        if circuit_breaker:
            self.circuit_breaker = CircuitBreaker()
        
        # HTTP 客户端（带连接池限制）
        limits = httpx.Limits(
            max_connections=max_connections,
            max_keepalive_connections=max_connections // 2,
        )
        
        timeout_obj = Timeout(timeout=timeout, connect=10.0)
        self.client = AsyncClient(
            limits=limits,
            timeout=timeout_obj,
            follow_redirects=True,
        )
        
        # 统计信息
        self.stats = ThrottleStats(max_concurrent=max_concurrent)
        self._stats_lock = asyncio.Lock()
        
        logger.info(
            f"初始化限流客户端: "
            f"并发={max_concurrent}, "
            f"连接数={max_connections}, "
            f"超时={timeout}s, "
            f"重试={retries}"
        )
    
    async def _acquire_rate_limit(self):
        """获取速率限制令牌"""
        if self.rate_limit_per_sec is None:
            return
            
        async with self._rate_lock:
            now = time.time()
            elapsed = now - self._rate_last_update
            
            # 补充令牌
            self._rate_tokens += elapsed * self.rate_limit_per_sec
            self._rate_tokens = min(self._rate_tokens, self.rate_limit_per_sec)
            self._rate_last_update = now
            
            # 等待可用令牌
            if self._rate_tokens < 1:
                wait_time = (1 - self._rate_tokens) / self.rate_limit_per_sec
                await asyncio.sleep(wait_time)
                self._rate_tokens = 0  # 使用令牌
            else:
                self._rate_tokens -= 1  # 使用令牌
    
    async def _update_stats(self, success: bool, wait_time: float = 0.0):
        """更新统计信息"""
        async with self._stats_lock:
            self.stats.total_requests += 1
            self.stats.total_wait_time += wait_time
            
            if success:
                self.stats.successful_requests += 1
            else:
                self.stats.failed_requests += 1
            
            # 更新最大并发数
            current = self.max_concurrent - self.semaphore._value
            self.stats.current_concurrent = current
            if current > self.stats.max_concurrent:
                self.stats.max_concurrent = current
    
    @asynccontextmanager
    async def _throttled_request(self):
        """
        限流请求上下文管理器
        
        双重限流：
        1. 信号量控制并发协程数
        2. 速率限制控制 QPS
        """
        start_time = time.time()
        
        # 检查断路器
        if self.circuit_breaker_enabled and not self.circuit_breaker.can_execute():
            raise Exception(f"断路器打开，当前状态: {self.circuit_breaker.get_state()}")
        
        # 速率限制
        await self._acquire_rate_limit()
        
        # 信号量限流
        async with self.semaphore:
            wait_time = time.time() - start_time
            try:
                yield wait_time
                
                # 请求成功
                if self.circuit_breaker_enabled:
                    self.circuit_breaker.on_success()
                await self._update_stats(True, wait_time)
                
            except Exception as e:
                # 请求失败
                if self.circuit_breaker_enabled:
                    self.circuit_breaker.on_failure()
                await self._update_stats(False, wait_time)
                raise
    
    async def request(
        self,
        method: str,
        url: str,
        **kwargs
    ) -> Response:
        """
        发送 HTTP 请求（带限流和重试）
        
        Args:
            method: HTTP 方法 (GET, POST, PUT, DELETE, etc.)
            url: 请求 URL
            **kwargs: 传递给 httpx 的参数
            
        Returns:
            httpx.Response 对象
            
        Raises:
            Exception: 所有重试失败后抛出异常
        """
        last_exception = None
        
        for attempt in range(self.retries + 1):
            try:
                async with self._throttled_request() as wait_time:
                    if attempt > 0:
                        logger.debug(f"重试请求: {method} {url}, 尝试 #{attempt}, 等待 {wait_time:.2f}s")
                    
                    response = await self.client.request(method, url, **kwargs)
                    
                    # 检查 HTTP 状态码
                    if 400 <= response.status_code < 500:
                        logger.warning(f"客户端错误: {response.status_code} {method} {url}")
                        # 4xx 错误不重试（除了 429）
                        if response.status_code != 429:
                            return response
                        raise Exception(f"HTTP 429 Too Many Requests")
                    
                    elif response.status_code >= 500:
                        logger.warning(f"服务器错误: {response.status_code} {method} {url}")
                        raise Exception(f"HTTP {response.status_code}")
                    
                    return response
                    
            except Exception as e:
                last_exception = e
                logger.warning(f"请求失败: {method} {url}, 尝试 #{attempt}, 错误: {e}")
                
                # 如果不是最后一次尝试，等待后重试
                if attempt < self.retries:
                    delay = self.retry_delay * (2 ** attempt)  # 指数退避
                    logger.debug(f"{delay:.1f}秒后重试...")
                    await asyncio.sleep(delay)
                else:
                    logger.error(f"所有重试失败: {method} {url}")
        
        # 所有重试都失败
        raise last_exception or Exception("未知错误")
    
    async def get(self, url: str, **kwargs) -> Response:
        """发送 GET 请求"""
        return await self.request("GET", url, **kwargs)
    
    async def post(self, url: str, **kwargs) -> Response:
        """发送 POST 请求"""
        return await self.request("POST", url, **kwargs)
    
    async def put(self, url: str, **kwargs) -> Response:
        """发送 PUT 请求"""
        return await self.request("PUT", url, **kwargs)
    
    async def delete(self, url: str, **kwargs) -> Response:
        """发送 DELETE 请求"""
        return await self.request("DELETE", url, **kwargs)
    
    async def fetch_all(self, requests: List[Dict[str, Any]]) -> List[Any]:
        """
        并发获取多个请求
        
        Args:
            requests: 请求列表，每个元素是包含 method, url, kwargs 的字典
            
        Returns:
            响应列表，保持原始顺序
        """
        async def fetch_one(req: Dict[str, Any]) -> Any:
            return await self.request(req["method"], req["url"], **req.get("kwargs", {}))
        
        tasks = [fetch_one(req) for req in requests]
        return await asyncio.gather(*tasks, return_exceptions=True)
    
    def get_stats(self) -> ThrottleStats:
        """获取统计信息"""
        return self.stats
    
    def get_circuit_breaker_state(self) -> Optional[str]:
        """获取断路器状态"""
        if self.circuit_breaker_enabled:
            return self.circuit_breaker.get_state()
        return None
    
    async def close(self):
        """关闭客户端"""
        await self.client.aclose()
        logger.info("限流客户端已关闭")
    
    async def __aenter__(self):
        """异步上下文管理器入口"""
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """异步上下文管理器退出"""
        await self.close()


# ====================== 使用示例 ======================

async def example_usage():
    """使用示例"""
    import json
    
    # 配置日志
    logging.basicConfig(level=logging.INFO)
    
    # 创建限流客户端
    async with ThrottledClient(
        max_concurrent=10,          # 最大并发 10 个请求
        max_connections=20,         # 最大 20 个 TCP 连接
        timeout=10.0,               # 10秒超时
        retries=3,                  # 重试 3 次
        retry_delay=1.0,            # 重试延迟 1秒
        rate_limit_per_sec=5,       # 限制每秒 5 个请求
        circuit_breaker=True,       # 启用断路器
    ) as client:
        
        print("🚀 开始并发测试...")
        
        # 准备测试 URL（使用公共测试 API）
        test_urls = [
            "https://httpbin.org/get",
            "https://httpbin.org/post",
            "https://httpbin.org/put",
            "https://httpbin.org/delete",
            "https://httpbin.org/status/200",
            "https://httpbin.org/status/404",
            "https://httpbin.org/status/500",
            "https://httpbin.org/delay/2",  # 2秒延迟
            "https://httpbin.org/delay/3",  # 3秒延迟
            "https://httpbin.org/delay/1",  # 1秒延迟
        ]
        
        # 创建请求列表
        requests = []
        for i, url in enumerate(test_urls):
            method = "GET"
            if "post" in url:
                method = "POST"
            elif "put" in url:
                method = "PUT"
            elif "delete" in url:
                method = "DELETE"
                
            requests.append({
                "method": method,
                "url": url,
                "kwargs": {"headers": {"X-Test-Id": str(i)}}
            })
        
        # 并发执行所有请求
        results = await client.fetch_all(requests)
        
        # 分析结果
        successes = 0
        failures = 0
        
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                print(f"❌ 请求 {i} 失败: {result}")
                failures += 1
            else:
                print(f"✅ 请求 {i} 成功: HTTP {result.status_code}")
                successes += 1
        
        # 显示统计信息
        stats = client.get_stats()
        print("\n📊 统计信息:")
        print(f"   总请求数: {stats.total_requests}")
        print(f"   成功请求: {stats.successful_requests}")
        print(f"   失败请求: {stats.failed_requests}")
        print(f"   最大并发: {stats.max_concurrent}")
        print(f"   当前并发: {stats.current_concurrent}")
        print(f"   总等待时间: {stats.total_wait_time:.2f}s")
        
        # 断路器状态
        cb_state = client.get_circuit_breaker_state()
        if cb_state:
            print(f"   断路器状态: {cb_state}")
        
        print(f"\n🎯 成功率: {successes}/{len(results)} ({successes/len(results)*100:.1f}%)")


async def performance_test():
    """性能测试 - 模拟高并发场景"""
    import random
    
    logging.basicConfig(level=logging.WARNING)  # 减少日志
    
    # 创建更严格的限流客户端
    async with ThrottledClient(
        max_concurrent=5,           # 仅允许 5 个并发
        max_connections=10,
        timeout=5.0,
        retries=2,
        rate_limit_per_sec=10,      # 10 QPS
    ) as client:
        
        # 模拟 50 个请求
        tasks = []
        for i in range(50):
            # 随机延迟 URL
            delay = random.choice([0, 1, 2])
            url = f"https://httpbin.org/delay/{delay}"
            
            task = asyncio.create_task(client.get(url))
            tasks.append(task)
        
        # 等待所有任务完成
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        stats = client.get_stats()
        print(f"性能测试完成:")
        print(f"  处理 {len(tasks)} 个请求")
        print(f"  最大并发: {stats.max_concurrent}")
        print(f"  平均等待时间: {stats.total_wait_time/stats.total_requests:.3f}s/请求")


if __name__ == "__main__":
    print("=== 限流客户端示例 ===")
    
    # 运行示例
    asyncio.run(example_usage())
    
    print("\n=== 性能测试 ===")
    asyncio.run(performance_test())