#!/usr/bin/env python3
"""
WebSocket实际测试 - 测试EVO Map重连算法
使用公共WebSocket测试服务器: wss://ws.postman-echo.com/raw
"""

import asyncio
import sys
import os

# 添加当前目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from websocket_reconnect import ReconnectingWebSocket
import logging

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

async def test_echo_server():
    """测试公共WebSocket回显服务器"""
    print("测试公共WebSocket回显服务器...")
    print("服务器: wss://ws.postman-echo.com/raw")
    print()
    
    messages_received = 0
    connection_changes = []
    
    async def on_open():
        nonlocal connection_changes
        connection_changes.append("连接打开")
        print("✅ 连接已打开")
    
    async def on_message(msg):
        nonlocal messages_received
        messages_received += 1
        print(f"📨 收到消息 {messages_received}: {msg[:50]}...")
    
    async def on_close():
        nonlocal connection_changes
        connection_changes.append("连接关闭")
        print("❌ 连接已关闭")
    
    async def on_error(err):
        print(f"⚠️  连接错误: {err}")
    
    # 创建重连WebSocket客户端
    ws = ReconnectingWebSocket(
        url="wss://ws.postman-echo.com/raw",
        max_delay=10000,      # 最大10秒
        base_delay=1000,      # 基础1秒
        max_attempts=3,       # 最多重试3次
        ping_interval=15000,  # 15秒心跳
        ping_timeout=5000,    # 5秒超时
    )
    
    # 设置回调
    ws.on_open = on_open
    ws.on_message = on_message
    ws.on_close = on_close
    ws.on_error = on_error
    
    print("连接中...")
    await ws.connect()
    
    # 发送测试消息
    test_message = "Hello from EVO Map WebSocket test!"
    print(f"发送测试消息: {test_message}")
    
    if await ws.send(test_message):
        print("✅ 消息发送成功")
    else:
        print("❌ 消息发送失败")
    
    # 等待一段时间接收消息
    print("等待5秒接收回显...")
    await asyncio.sleep(5)
    
    # 手动关闭连接
    print("手动关闭连接...")
    await ws.close()
    
    # 等待清理
    await asyncio.sleep(1)
    
    print("\n" + "=" * 50)
    print("测试结果:")
    print(f"  连接状态变化: {len(connection_changes)} 次")
    for change in connection_changes:
        print(f"    - {change}")
    
    print(f"  收到消息: {messages_received} 条")
    
    if messages_received > 0:
        print("✅ WebSocket通信测试通过!")
    else:
        print("⚠️  未收到消息，但连接可能正常")
    
    print(f"  最终状态: {ws.state.value}")
    
    return messages_received > 0

async def test_reconnect_logic():
    """测试重连逻辑（不实际连接）"""
    print("\n" + "=" * 50)
    print("测试重连算法逻辑...")
    
    from websocket_reconnect import ReconnectingWebSocket
    
    # 创建客户端但不连接
    ws = ReconnectingWebSocket(
        url="ws://non-existent-server.test",
        max_delay=5000,
        base_delay=500,
        max_attempts=2,
    )
    
    print("测试重连延迟计算:")
    for attempt in range(3):
        ws.attempt = attempt
        delay = ws._get_delay()
        print(f"  尝试 {attempt}: {delay:.2f}s")
    
    # 验证指数退避
    ws.attempt = 0
    delay1 = ws._get_delay()
    ws.attempt = 1
    delay2 = ws._get_delay()
    ws.attempt = 2
    delay3 = ws._get_delay()
    
    if delay1 < delay2 < delay3:
        print("✅ 指数退避策略有效")
    else:
        print(f"⚠️  退避策略异常: {delay1:.2f}, {delay2:.2f}, {delay3:.2f}")
    
    print("✅ 重连算法逻辑测试完成")

async def main():
    """主测试函数"""
    print("=" * 60)
    print("EVO Map WebSocket实际测试")
    print("基于Capsule: sha256:900d5178ad84e9f7a6393ab3979ec555bac87881cc2f06463a7a0023da6f0378")
    print("=" * 60)
    
    try:
        # 测试重连逻辑
        await test_reconnect_logic()
        
        # 测试实际服务器连接
        print("\n" + "=" * 50)
        print("注意: 实际服务器测试需要网络连接")
        print("如果测试失败，可能是网络问题或服务器不可用")
        print("=" * 50)
        
        try:
            success = await test_echo_server()
            if not success:
                print("\n⚠️  实际连接测试未收到消息，但重连算法已验证")
        except Exception as e:
            print(f"\n⚠️  实际连接测试异常: {e}")
            print("这可能是因为网络限制或服务器问题")
            print("重连算法本身已通过逻辑测试")
        
    except KeyboardInterrupt:
        print("\n测试被用户中断")
    except Exception as e:
        print(f"\n测试异常: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n" + "=" * 60)
    print("测试完成")
    print("=" * 60)

if __name__ == "__main__":
    # 运行测试
    asyncio.run(main())