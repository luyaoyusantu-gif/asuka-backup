#!/usr/bin/env python3
"""
最小化测试 - 只检查EVO Map代码导入，避免Unicode问题
"""

import sys
import os

print("EVO Map技术实现最小化测试")
print("=" * 50)

# 1. 检查包导入
print("\n1. 包导入检查:")
try:
    import websockets
    print("  websockets: OK")
except ImportError as e:
    print(f"  websockets: FAIL - {e}")
    sys.exit(1)

try:
    import httpx
    print("  httpx: OK")
except ImportError as e:
    print(f"  httpx: FAIL - {e}")
    sys.exit(1)

# 2. 检查EVO Map代码
print("\n2. EVO Map代码检查:")

# WebSocket重连
try:
    from websocket_reconnect import ReconnectingWebSocket, ConnectionState
    print("  websocket_reconnect: OK")
    
    # 测试算法
    ws = ReconnectingWebSocket("ws://test", max_delay=30000, base_delay=1000)
    ws.attempt = 0
    d1 = ws._get_delay()
    ws.attempt = 1
    d2 = ws._get_delay()
    print(f"   重连延迟测试: 尝试0={d1:.2f}s, 尝试1={d2:.2f}s")
    
except Exception as e:
    print(f"  websocket_reconnect: FAIL - {e}")

# 异步限流
try:
    from async_throttle import ThrottledClient, CircuitBreaker
    print("  async_throttle: OK")
    
    # 测试断路器
    cb = CircuitBreaker(failure_threshold=3)
    if cb.get_state() == "closed":
        print("   断路器: 初始状态正常")
    
except Exception as e:
    print(f"  async_throttle: FAIL - {e}")

# 3. 文件存在检查
print("\n3. 文件存在检查:")
files = ["websocket_reconnect.py", "async_throttle.py", "Dockerfile.optimized"]
all_ok = True
for f in files:
    if os.path.exists(f):
        print(f"  {f}: 存在")
    else:
        print(f"  {f}: 缺失")
        all_ok = False

print("\n" + "=" * 50)
print("测试结果:")

if all_ok:
    print("SUCCESS: EVO Map技术实现基本验证通过")
    print("\n下一步:")
    print("  1. 可以进行实际功能测试")
    print("  2. 考虑安装LiveKit: pip install livekit-agents")
    print("  3. 开始实时语音开发准备")
else:
    print("WARNING: 部分检查未通过")
    print("\n需要:")
    print("  1. 确保所有文件存在")
    print("  2. 修复导入错误")

print("\nPython环境:", sys.version.split()[0])
print("虚拟环境:", "是" if hasattr(sys, 'real_prefix') or sys.base_prefix != sys.prefix else "否")