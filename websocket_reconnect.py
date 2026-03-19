#!/usr/bin/env python3
"""
WebSocket 生产级重连算法 - 基于 EVO Map 热门 Capsule 实现

EVO Map Capsule ID: sha256:900d5178ad84e9f7a6393ab3979ec555bac87881cc2f06463a7a0023da6f0378
置信度: 99%，使用次数: 73,438，GDI: 72.0

核心算法：全抖动指数退避策略
问题：服务器重启时所有客户端同时重连，造成「重连风暴」
解决方案：随机抖动使客户端重连时间分散，服务器负载降低 90%
"""

import asyncio
import random
import time
from enum import Enum
from typing import Optional, Callable, Any
import logging

try:
    import websockets
    from websockets.client import WebSocketClientProtocol
    from websockets.exceptions import ConnectionClosed
except ImportError:
    print("警告：需要安装 websockets 库：pip install websockets")
    websockets = None

logger = logging.getLogger(__name__)


class ConnectionState(Enum):
    """连接状态机 - 基于 EVO Map 状态机设计"""
    DISCONNECTED = "disconnected"      # 未连接
    CONNECTING = "connecting"          # 连接中
    OPEN = "open"                      # 连接已打开
    CLOSING = "closing"                # 正在关闭
    CLOSED = "closed"                  # 已关闭
    RECONNECTING = "reconnecting"      # 重连中


class ReconnectingWebSocket:
    """
    生产级 WebSocket 客户端，支持全抖动指数退避重连
    
    特性：
    1. 全抖动指数退避算法防止重连风暴
    2. 完整的状态机管理
    3. 心跳检测 (ping/pong)
    4. 异常安全的重连逻辑
    5. 事件回调支持
    """
    
    def __init__(
        self,
        url: str,
        max_delay: int = 30000,      # 最大退避时间 30秒
        base_delay: int = 1000,      # 基础退避时间 1秒
        max_attempts: Optional[int] = None,  # 最大重试次数，None表示无限重试
        ping_interval: int = 30000,  # 心跳间隔 30秒
        ping_timeout: int = 10000,   # 心跳超时 10秒
    ):
        """
        初始化重连 WebSocket 客户端
        
        Args:
            url: WebSocket 服务器地址 (ws:// 或 wss://)
            max_delay: 最大退避延迟（毫秒）
            base_delay: 基础退避延迟（毫秒）
            max_attempts: 最大重试次数，None 表示无限重试
            ping_interval: 心跳发送间隔（毫秒）
            ping_timeout: 心跳响应超时（毫秒）
        """
        if websockets is None:
            raise ImportError("需要安装 websockets 库：pip install websockets")
            
        self.url = url
        self.max_delay = max_delay
        self.base_delay = base_delay
        self.max_attempts = max_attempts
        self.ping_interval = ping_interval / 1000  # 转换为秒
        self.ping_timeout = ping_timeout / 1000    # 转换为秒
        
        # 状态管理
        self.state = ConnectionState.DISCONNECTED
        self.attempt = 0  # 当前重试次数
        self.ws: Optional[WebSocketClientProtocol] = None
        self._reconnect_task: Optional[asyncio.Task] = None
        self._ping_task: Optional[asyncio.Task] = None
        
        # 事件回调
        self.on_open: Optional[Callable] = None
        self.on_message: Optional[Callable[[Any], None]] = None
        self.on_close: Optional[Callable] = None
        self.on_error: Optional[Callable[[Exception], None]] = None
        
        # 控制标志
        self._should_reconnect = True
        self._manually_closed = False
        
    def _get_delay(self) -> float:
        """
        计算重连延迟 - 全抖动指数退避算法
        
        算法：delay = base_delay * 2^attempt (指数增长，上限 max_delay)
             实际延迟 = delay/2 + random() * delay/2 (全抖动策略)
        
        效果：使客户端重连时间分散，避免所有客户端同时重连
        参考：EVO Map Capsule 中 JavaScript 实现
        """
        # 指数增长：1s, 2s, 4s, 8s... 上限 max_delay
        exp_delay = min(self.base_delay * (2 ** self.attempt), self.max_delay)
        
        # 全抖动策略：随机分布在 [exp_delay/2, exp_delay] 区间
        # 相比固定延迟，有效防止同步重连
        delay = exp_delay / 2 + random.random() * exp_delay / 2
        
        logger.debug(f"重连延迟计算: attempt={self.attempt}, exp={exp_delay}ms, jittered={delay:.0f}ms")
        return delay / 1000  # 转换为秒
    
    async def connect(self) -> None:
        """建立 WebSocket 连接"""
        if self.state in [ConnectionState.CONNECTING, ConnectionState.OPEN]:
            logger.warning("连接已在进行中或已建立")
            return
            
        self._manually_closed = False
        self._should_reconnect = True
        self._change_state(ConnectionState.CONNECTING)
        
        try:
            # 建立 WebSocket 连接
            self.ws = await websockets.connect(
                self.url,
                ping_interval=self.ping_interval,
                ping_timeout=self.ping_timeout,
                close_timeout=1,
            )
            
            self._change_state(ConnectionState.OPEN)
            self.attempt = 0  # 连接成功，重置重试计数
            
            logger.info(f"WebSocket 连接成功: {self.url}")
            
            # 触发连接打开回调
            if self.on_open:
                try:
                    await self.on_open()
                except Exception as e:
                    logger.error(f"on_open 回调异常: {e}")
            
            # 启动消息监听和心跳任务
            self._reconnect_task = asyncio.create_task(self._listen())
            self._ping_task = asyncio.create_task(self._keepalive())
            
        except Exception as e:
            logger.error(f"连接失败: {e}")
            self._change_state(ConnectionState.DISCONNECTED)
            
            # 触发错误回调
            if self.on_error:
                try:
                    await self.on_error(e)
                except Exception as cb_err:
                    logger.error(f"on_error 回调异常: {cb_err}")
            
            # 启动重连（如果不是手动关闭）
            if self._should_reconnect and not self._manually_closed:
                await self._schedule_reconnect()
    
    async def _listen(self) -> None:
        """监听消息"""
        if not self.ws:
            return
            
        try:
            async for message in self.ws:
                if self.on_message:
                    try:
                        await self.on_message(message)
                    except Exception as e:
                        logger.error(f"on_message 回调异常: {e}")
                        
        except ConnectionClosed as e:
            logger.info(f"连接关闭: {e}")
            self._handle_disconnection(e)
        except Exception as e:
            logger.error(f"监听异常: {e}")
            self._handle_disconnection(e)
    
    async def _keepalive(self) -> None:
        """心跳保持 - 检测连接状态"""
        while self.state == ConnectionState.OPEN and self.ws:
            try:
                await asyncio.sleep(self.ping_interval)
                # websockets 库会自动处理 ping/pong
                # 这里主要是日志记录和状态检查
                if self.ws and self.ws.open:
                    logger.debug("心跳正常")
                else:
                    logger.warning("连接似乎已断开，触发重连")
                    self._handle_disconnection(ConnectionClosed(1006, "heartbeat failed"))
                    break
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"心跳异常: {e}")
                self._handle_disconnection(e)
                break
    
    def _handle_disconnection(self, error: Exception) -> None:
        """处理连接断开"""
        if self.state != ConnectionState.OPEN:
            return
            
        self._change_state(ConnectionState.CLOSED)
        
        # 清理资源
        if self._ping_task:
            self._ping_task.cancel()
            self._ping_task = None
            
        self.ws = None
        
        # 触发关闭回调
        if self.on_close:
            try:
                asyncio.create_task(self.on_close())
            except Exception as e:
                logger.error(f"on_close 回调异常: {e}")
        
        # 自动重连（如果不是手动关闭）
        if self._should_reconnect and not self._manually_closed:
            asyncio.create_task(self._schedule_reconnect())
    
    async def _schedule_reconnect(self) -> None:
        """安排重连"""
        if self._manually_closed or not self._should_reconnect:
            return
            
        # 检查重试次数限制
        if self.max_attempts and self.attempt >= self.max_attempts:
            logger.error(f"达到最大重试次数: {self.max_attempts}")
            self._change_state(ConnectionState.DISCONNECTED)
            return
            
        self._change_state(ConnectionState.RECONNECTING)
        self.attempt += 1
        
        delay = self._get_delay()
        logger.info(f"{self.attempt}秒后重连尝试 #{self.attempt}, 延迟: {delay:.1f}s")
        
        await asyncio.sleep(delay)
        
        if self._should_reconnect and not self._manually_closed:
            await self.connect()
    
    def _change_state(self, new_state: ConnectionState) -> None:
        """更新状态"""
        old_state = self.state
        self.state = new_state
        logger.debug(f"状态变更: {old_state.value} -> {new_state.value}")
    
    async def send(self, data: Any) -> bool:
        """发送消息"""
        if self.state != ConnectionState.OPEN or not self.ws:
            logger.warning("连接未就绪，无法发送消息")
            return False
            
        try:
            await self.ws.send(data)
            return True
        except Exception as e:
            logger.error(f"发送消息失败: {e}")
            self._handle_disconnection(e)
            return False
    
    async def close(self, code: int = 1000, reason: str = "") -> None:
        """关闭连接（手动关闭）"""
        self._manually_closed = True
        self._should_reconnect = False
        
        if self.state == ConnectionState.DISCONNECTED:
            return
            
        self._change_state(ConnectionState.CLOSING)
        
        # 取消任务
        if self._reconnect_task:
            self._reconnect_task.cancel()
            self._reconnect_task = None
            
        if self._ping_task:
            self._ping_task.cancel()
            self._ping_task = None
        
        # 关闭 WebSocket 连接
        if self.ws and self.ws.open:
            try:
                await self.ws.close(code=code, reason=reason)
            except Exception as e:
                logger.error(f"关闭连接异常: {e}")
        
        self._change_state(ConnectionState.CLOSED)
        self.ws = None
        logger.info("连接已手动关闭")
    
    def is_connected(self) -> bool:
        """检查是否已连接"""
        return self.state == ConnectionState.OPEN and self.ws is not None


# ====================== 使用示例 ======================

async def example_usage():
    """使用示例"""
    import json
    
    # 配置日志
    logging.basicConfig(level=logging.INFO)
    
    # 创建重连 WebSocket 客户端
    ws = ReconnectingWebSocket(
        url="wss://echo.websocket.org",  # 测试服务器
        max_delay=30000,    # 最大 30秒
        base_delay=1000,    # 基础 1秒
        max_attempts=10,    # 最多重试 10次
    )
    
    # 设置事件回调
    async def on_open():
        print("✅ 连接已打开")
        # 连接成功后发送测试消息
        await ws.send(json.dumps({"type": "hello", "data": "test"}))
    
    async def on_message(msg):
        print(f"📨 收到消息: {msg}")
    
    async def on_close():
        print("❌ 连接已关闭")
    
    async def on_error(err):
        print(f"⚠️  连接错误: {err}")
    
    ws.on_open = on_open
    ws.on_message = on_message
    ws.on_close = on_close
    ws.on_error = on_error
    
    # 连接
    print("🔄 连接中...")
    await ws.connect()
    
    # 保持运行一段时间
    try:
        await asyncio.sleep(60)  # 运行 60秒
    except KeyboardInterrupt:
        print("\n👋 用户中断")
    finally:
        # 关闭连接
        await ws.close()
        print("🔒 连接已清理")


if __name__ == "__main__":
    asyncio.run(example_usage())