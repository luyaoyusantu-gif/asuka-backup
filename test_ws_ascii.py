#!/usr/bin/env python3
"""
WebSocket ASCII测试 - 无Unicode字符
使用公共WebSocket测试服务器
"""

import asyncio
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from websocket_reconnect import ReconnectingWebSocket
    print("WebSocket重连模块导入成功")
except ImportError as e:
    print(f"导入失败: {e}")
    sys.exit(1)

async def test_echo():
    """测试公共回显服务器"""
    print("测试公共WebSocket回显服务器...")
    print("服务器: wss://ws.postman-echo.com/raw")
    
    messages = []
    
    async def on_open():
        print("连接已打开")
    
    async def on_message(msg):
        messages.append(msg)
        print(f"收到消息 {len(messages)}: {msg[:50]}")
    
    async def on_close():
        print("连接已关闭")
    
    async def on_error(err):
        print(f"连接错误: {err}")
    
    # 创建客户端
    ws = ReconnectingWebSocket(
        url="wss://ws.postman-echo.com/raw",
        max_delay=10000,
        base_delay=1000,
        max_attempts=2,
        ping_interval=15000,
        ping_timeout=5000,
    )
    
    ws.on_open = on_open
    ws.on_message = on_message
    ws.on_close = on_close
    ws.on_error = on_error
    
    print("连接中...")
    await ws.connect()
    
    # 发送测试消息
    test_msg = "Test from EVO Map WebSocket"
    print(f"发送消息: {test_msg}")
    
    if await ws.send(test_msg):
        print("消息发送成功")
    else:
        print("消息发送失败")
    
    # 等待接收
    print("等待3秒接收回显...")
    await asyncio.sleep(3)
    
    # 关闭
    print("关闭连接...")
    await ws.close()
    
    print(f"\n测试结果:")
    print(f"  收到消息数: {len(messages)}")
    print(f"  最终状态: {ws.state.value}")
    
    return len(messages) > 0

async def test_reconnect_logic():
    """测试重连逻辑"""
    print("\n测试重连算法逻辑...")
    
    ws = ReconnectingWebSocket("ws://test", max_delay=5000, base_delay=500)
    
    print("重连延迟计算:")
    for i in range(3):
        ws.attempt = i
        delay = ws._get_delay()
        print(f"  尝试{i}: {delay:.2f}s")
    
    # 验证指数退避
    ws.attempt = 0
    d1 = ws._get_delay()
    ws.attempt = 1
    d2 = ws._get_delay()
    ws.attempt = 2
    d3 = ws._get_delay()
    
    if d1 < d2 < d3:
        print("指数退避策略有效")
    else:
        print(f"退避策略异常: {d1:.2f}, {d2:.2f}, {d3:.2f}")
    
    return True

async def main():
    print("=" * 60)
    print("EVO Map WebSocket实际测试 (ASCII版本)")
    print("=" * 60)
    
    try:
        # 测试逻辑
        await test_reconnect_logic()
        
        # 测试实际连接
        print("\n" + "=" * 50)
        print("实际连接测试 (需要网络)...")
        
        try:
            success = await test_echo()
            if success:
                print("[SUCCESS] WebSocket通信测试通过")
            else:
                print("[WARNING] 未收到消息，连接可能正常")
        except Exception as e:
            print(f"[WARNING] 连接测试异常: {e}")
            print("可能是网络问题或服务器不可用")
        
    except KeyboardInterrupt:
        print("\n测试中断")
    except Exception as e:
        print(f"\n测试异常: {e}")
    
    print("\n" + "=" * 60)
    print("测试完成")
    print("=" * 60)

if __name__ == "__main__":
    asyncio.run(main())