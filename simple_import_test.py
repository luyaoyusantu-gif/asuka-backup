#!/usr/bin/env python3
"""
简单导入测试 - 检查EVO Map技术实现所需包
"""

import sys

print("Python版本:", sys.version)
print("Python路径:", sys.executable)
print()

# 测试内置模块
print("测试内置模块:")
builtin_modules = ["asyncio", "logging", "random", "time", "json", "os", "sys"]
for module in builtin_modules:
    try:
        __import__(module)
        print(f"  ✓ {module}")
    except ImportError:
        print(f"  ✗ {module}")

print("\n测试第三方包:")

# 测试websockets (WebSocket重连需要)
try:
    import websockets
    print("  ✓ websockets (版本:", websockets.__version__ + ")")
except ImportError:
    print("  ✗ websockets - 需要安装: pip install websockets")

# 测试httpx (异步HTTP限流需要)
try:
    import httpx
    print("  ✓ httpx (版本:", httpx.__version__ + ")")
except ImportError:
    print("  ✗ httpx - 需要安装: pip install httpx")

# 测试aiohttp (备选)
try:
    import aiohttp
    print("  ✓ aiohttp (版本:", aiohttp.__version__ + ")")
except ImportError:
    print("  ✗ aiohttp - 备选HTTP客户端")

print("\n测试LiveKit相关包:")

# 测试LiveKit
try:
    import livekit
    print("  ✓ livekit")
except ImportError:
    print("  ✗ livekit - 需要安装: pip install livekit-agents")

try:
    import livekit.agents
    print("  ✓ livekit.agents")
except ImportError:
    print("  ✗ livekit.agents - LiveKit Agents模块")

try:
    import livekit.plugins
    print("  ✓ livekit.plugins")
except ImportError:
    print("  ✗ livekit.plugins - LiveKit插件")

print("\n环境建议:")
print("-" * 40)

# 检查是否需要创建虚拟环境
print("建议为LiveKit开发创建新的虚拟环境:")
print("  python -m venv .venv-livekit")
print("  .venv-livekit\\Scripts\\activate  # Windows")
print("  pip install websockets httpx livekit-agents")

print("\nEVO Map代码测试:")
print("  1. 先安装缺失包: pip install websockets httpx")
print("  2. 测试 websocket_reconnect.py")
print("  3. 测试 async_throttle.py")

print("\n当前状态:")
if "websockets" in sys.modules and "httpx" in sys.modules:
    print("  ✅ 可以测试EVO Map技术实现")
else:
    print("  ⚠️  需要先安装websockets和httpx")

if "livekit" in sys.modules:
    print("  ✅ LiveKit环境已就绪")
else:
    print("  ⚠️  LiveKit需要单独安装")