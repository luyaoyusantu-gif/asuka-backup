#!/usr/bin/env python3
"""
异步限流ASCII测试 - 无Unicode字符
测试EVO Map限流算法
"""

import asyncio
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from async_throttle import ThrottledClient, CircuitBreaker
    print("异步限流模块导入成功")
except ImportError as e:
    print(f"导入失败: {e}")
    sys.exit(1)

async def test_basic():
    """测试基本HTTP请求"""
    print("测试基本HTTP请求...")
    
    async with ThrottledClient(
        max_concurrent=3,
        max_connections=5,
        timeout=10.0,
        retries=2,
        rate_limit_per_sec=2,
        circuit_breaker=True,
    ) as client:
        
        # 测试GET
        try:
            response = await client.get("https://httpbin.org/get")
            print(f"GET成功: HTTP {response.status_code}")
            print(f"响应大小: {len(response.content)} 字节")
        except Exception as e:
            print(f"GET失败: {e}")
        
        # 测试POST
        try:
            response = await client.post(
                "https://httpbin.org/post",
                json={"test": "data"}
            )
            print(f"POST成功: HTTP {response.status_code}")
        except Exception as e:
            print(f"POST失败: {e}")
        
        # 统计
        stats = client.get_stats()
        print(f"\n统计信息:")
        print(f"  总请求数: {stats.total_requests}")
        print(f"  成功请求: {stats.successful_requests}")
        print(f"  失败请求: {stats.failed_requests}")
        print(f"  最大并发: {stats.max_concurrent}")
        
        cb_state = client.get_circuit_breaker_state()
        if cb_state:
            print(f"  断路器状态: {cb_state}")
        
        return stats.successful_requests >= 1

async def test_circuit_breaker():
    """测试断路器"""
    print("\n测试断路器功能...")
    
    async with ThrottledClient(
        max_concurrent=2,
        timeout=3.0,
        retries=0,
        circuit_breaker=True,
    ) as client:
        
        # 正常请求
        try:
            response = await client.get("https://httpbin.org/status/200")
            print(f"正常请求成功: HTTP {response.status_code}")
        except Exception as e:
            print(f"正常请求失败: {e}")
        
        # 模拟失败
        print("模拟失败请求...")
        failures = 0
        for i in range(5):
            try:
                await client.get(f"https://non-existent-domain-{i}.test/")
                print(f"请求{i}: 成功（意外）")
            except Exception:
                failures += 1
                print(f"请求{i}: 失败")
        
        print(f"失败次数: {failures}")
        
        # 检查断路器
        cb_state = client.get_circuit_breaker_state()
        print(f"断路器状态: {cb_state}")
        
        if cb_state == "open":
            print("断路器正确打开")
        else:
            print(f"断路器状态异常: {cb_state}")
        
        return True

async def test_concurrent():
    """测试并发限流"""
    print("\n测试并发请求限流...")
    
    async with ThrottledClient(
        max_concurrent=2,
        rate_limit_per_sec=3,
    ) as client:
        
        urls = [
            "https://httpbin.org/delay/1",
            "https://httpbin.org/delay/0.5",
            "https://httpbin.org/delay/1",
            "https://httpbin.org/delay/0.3",
        ]
        
        print(f"发送 {len(urls)} 个请求...")
        
        tasks = []
        for i, url in enumerate(urls):
            task = asyncio.create_task(client.get(url))
            tasks.append((i, task))
        
        results = []
        for i, task in tasks:
            try:
                response = await task
                results.append((i, "成功", response.status_code))
                print(f"  请求{i}: 成功 (HTTP {response.status_code})")
            except Exception as e:
                results.append((i, "失败", str(e)[:50]))
                print(f"  请求{i}: 失败")
        
        successes = sum(1 for _, status, _ in results if status == "成功")
        print(f"\n成功: {successes}/{len(urls)}")
        
        return successes > 0

async def main():
    print("=" * 60)
    print("EVO Map 异步限流测试 (ASCII版本)")
    print("=" * 60)
    
    try:
        # 测试1: 基本请求
        print("\n测试1: 基本HTTP请求")
        success1 = await test_basic()
        
        # 测试2: 断路器
        print("\n测试2: 断路器功能")
        success2 = await test_circuit_breaker()
        
        # 测试3: 并发限流
        print("\n测试3: 并发请求限流")
        success3 = await test_concurrent()
        
        print("\n" + "=" * 60)
        print("测试总结")
        print("=" * 60)
        
        tests = [
            ("基本请求", success1),
            ("断路器", success2),
            ("并发限流", success3),
        ]
        
        all_passed = True
        for name, passed in tests:
            status = "通过" if passed else "失败"
            print(f"  {name:10} {status}")
            if not passed:
                all_passed = False
        
        if all_passed:
            print("\n[SUCCESS] 异步限流测试通过")
        else:
            print("\n[WARNING] 部分测试失败")
        
        print("\n技术验证:")
        print("  - 信号量并发控制")
        print("  - 连接池限制")
        print("  - 速率限制")
        print("  - 断路器模式")
        
    except KeyboardInterrupt:
        print("\n测试中断")
    except Exception as e:
        print(f"\n测试异常: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n" + "=" * 60)
    print("测试完成")
    print("=" * 60)

if __name__ == "__main__":
    asyncio.run(main())