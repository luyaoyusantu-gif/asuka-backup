#!/usr/bin/env python3
"""
ASCII编码测试 - 检查包导入，避免Unicode问题
"""

import sys

print("Python版本:", sys.version.split()[0])
print("Python路径:", sys.executable)
print()

# 测试关键包
packages_to_test = [
    ("websockets", "WebSocket重连需要"),
    ("httpx", "异步HTTP限流需要"),
    ("aiohttp", "备选HTTP客户端"),
    ("livekit", "LiveKit核心"),
]

print("包导入测试:")
print("-" * 40)

missing_packages = []

for package, description in packages_to_test:
    try:
        __import__(package)
        print(f"  OK  {package:12} - {description}")
    except ImportError:
        print(f"  MISS {package:12} - {description}")
        missing_packages.append(package)

print()
print("测试内置模块:")
builtin_ok = True
for module in ["asyncio", "logging", "random", "time"]:
    try:
        __import__(module)
        print(f"  OK  {module}")
    except ImportError:
        print(f"  MISS {module}")
        builtin_ok = False

print()
print("=" * 40)
print("环境总结:")

if missing_packages:
    print(f"需要安装的包: {', '.join(missing_packages)}")
    print()
    print("安装命令:")
    print(f"  python3.12 -m pip install {' '.join(missing_packages)}")
else:
    print("所有必要包已安装")

if builtin_ok:
    print("内置模块正常")
else:
    print("警告: 部分内置模块缺失")

print()
print("下一步建议:")
if "websockets" in sys.modules and "httpx" in sys.modules:
    print("1. 可以测试EVO Map技术实现")
    print("2. 运行 websocket_reconnect.py 测试")
    print("3. 运行 async_throttle.py 测试")
else:
    print("1. 先安装websockets和httpx包")
    print("2. 然后测试技术实现")

if "livekit" in sys.modules:
    print("4. LiveKit环境已就绪，可以开始语音开发")
else:
    print("4. LiveKit需要单独安装: pip install livekit-agents")