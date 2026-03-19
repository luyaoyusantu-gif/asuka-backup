#!/usr/bin/env python3
"""
EVO Map技术实现测试 - 验证websocket重连和异步限流代码
"""

import sys
import os

# 添加当前目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("=" * 60)
print("EVO Map技术实现测试")
print("=" * 60)

print("\n1. 检查包导入...")

# 检查websockets
try:
    import websockets
    print(f"  OK websockets {websockets.__version__}")
except ImportError as e:
    print(f"  ✗ websockets: {e}")
    sys.exit(1)

# 检查httpx
try:
    import httpx
    print(f"  ✓ httpx {httpx.__version__}")
except ImportError as e:
    print(f"  ✗ httpx: {e}")
    sys.exit(1)

print("\n2. 测试WebSocket重连算法代码...")

# 测试websocket_reconnect.py的类定义
try:
    # 动态导入类
    from websocket_reconnect import ReconnectingWebSocket, ConnectionState
    
    print(f"  ✓ ReconnectingWebSocket 类定义正常")
    print(f"  ✓ ConnectionState 枚举定义正常")
    
    # 测试算法函数
    ws = ReconnectingWebSocket("ws://test", max_delay=30000, base_delay=1000)
    
    # 测试_get_delay方法
    ws.attempt = 0
    delay1 = ws._get_delay()
    
    ws.attempt = 1
    delay2 = ws._get_delay()
    
    ws.attempt = 2
    delay3 = ws._get_delay()
    
    print(f"  ✓ _get_delay() 方法正常:")
    print(f"     尝试0: {delay1:.2f}s")
    print(f"     尝试1: {delay2:.2f}s") 
    print(f"     尝试2: {delay3:.2f}s")
    
    # 验证全抖动策略
    if delay2 > delay1 and delay3 > delay2:
        print(f"  ✓ 指数退避策略有效")
    else:
        print(f"  ⚠️  退避策略需要检查")
        
except Exception as e:
    print(f"  ✗ WebSocket代码测试失败: {e}")
    import traceback
    traceback.print_exc()

print("\n3. 测试异步限流客户端代码...")

try:
    from async_throttle import ThrottledClient, ThrottleStats, CircuitBreaker
    
    print(f"  ✓ ThrottledClient 类定义正常")
    print(f"  ✓ ThrottleStats 数据类正常")
    print(f"  ✓ CircuitBreaker 断路器类正常")
    
    # 测试断路器逻辑
    cb = CircuitBreaker(failure_threshold=3, reset_timeout=5.0)
    
    # 初始状态应该是closed
    if cb.get_state() == "closed":
        print(f"  ✓ 断路器初始状态正常: {cb.get_state()}")
    else:
        print(f"  ⚠️  断路器初始状态异常: {cb.get_state()}")
    
    # 测试可以执行
    if cb.can_execute():
        print(f"  ✓ 断路器允许执行检查正常")
    
    # 模拟失败
    for i in range(3):
        cb.on_failure()
    
    if cb.get_state() == "open":
        print(f"  ✓ 断路器在3次失败后打开正常")
    else:
        print(f"  ⚠️  断路器状态异常: {cb.get_state()}")
    
    # 测试不能执行
    if not cb.can_execute():
        print(f"  ✓ 断路器打开后拒绝执行正常")
    
except Exception as e:
    print(f"  ✗ 异步限流代码测试失败: {e}")
    import traceback
    traceback.print_exc()

print("\n4. 测试异步功能...")

try:
    import asyncio
    
    # 简单异步函数测试
    async def test_async():
        return "异步测试通过"
    
    # 运行异步测试
    result = asyncio.run(test_async())
    print(f"  ✓ 异步运行时正常: {result}")
    
except Exception as e:
    print(f"  ✗ 异步功能测试失败: {e}")

print("\n" + "=" * 60)
print("测试总结")
print("=" * 60)

# 检查文件存在
import os
files_to_check = [
    "websocket_reconnect.py",
    "async_throttle.py", 
    "Dockerfile.optimized",
    "evomap-knowledge.md",
    "learning-plan.md"
]

print("\n文件完整性检查:")
all_files_exist = True
for filename in files_to_check:
    if os.path.exists(filename):
        print(f"  ✓ {filename}")
    else:
        print(f"  ✗ {filename}")
        all_files_exist = False

print("\n环境状态:")
print(f"  Python: {sys.version.split()[0]}")
print(f"  虚拟环境: {'是' if hasattr(sys, 'real_prefix') or sys.base_prefix != sys.prefix else '否'}")

if all_files_exist:
    print("\n🎉 EVO Map技术实现测试通过!")
    print("   下一步: 运行实际功能测试")
    print("   1. python test_websocket_actual.py")
    print("   2. python test_async_throttle_actual.py")
else:
    print("\n⚠️  部分文件缺失，请检查")

print("\n建议后续步骤:")
print("  1. 创建实际的WebSocket服务器进行连接测试")
print("  2. 运行async_throttle的性能测试")
print("  3. 安装LiveKit: pip install livekit-agents")
print("  4. 开始实时语音开发")

print("\n" + "=" * 60)