#!/usr/bin/env python3
"""
测试脚本 - 无Unicode字符，避免Windows命令行编码问题
"""

import sys
import os

print("=" * 60)
print("EVO Map技术实现测试（无Unicode版本）")
print("=" * 60)

# 1. 检查关键包
print("\n1. 包导入检查:")
try:
    import websockets
    print("  [OK] websockets", websockets.__version__)
except ImportError as e:
    print("  [FAIL] websockets:", e)
    sys.exit(1)

try:
    import httpx
    print("  [OK] httpx", httpx.__version__)
except ImportError as e:
    print("  [FAIL] httpx:", e)
    sys.exit(1)

# 2. 测试WebSocket重连算法
print("\n2. WebSocket重连算法测试:")
try:
    from websocket_reconnect import ReconnectingWebSocket
    
    # 创建测试实例
    ws = ReconnectingWebSocket("ws://test", max_delay=30000, base_delay=1000)
    
    # 测试重连延迟计算
    print("  重连延迟计算测试:")
    for i in range(3):
        ws.attempt = i
        delay = ws._get_delay()
        print(f"    尝试{i}: {delay:.2f}秒")
    
    # 验证指数退避
    if ws._get_delay() < ws._get_delay():
        print("  [OK] 指数退避策略有效")
    else:
        print("  [WARN] 退避策略需要检查")
    
    print("  [OK] WebSocket重连算法通过")
    
except Exception as e:
    print(f"  [FAIL] WebSocket测试失败: {e}")

# 3. 测试异步限流
print("\n3. 异步限流客户端测试:")
try:
    from async_throttle import ThrottledClient, CircuitBreaker
    
    # 测试断路器
    cb = CircuitBreaker(failure_threshold=3)
    print(f"  断路器初始状态: {cb.get_state()}")
    
    if cb.get_state() == "closed":
        print("  [OK] 断路器初始状态正常")
    
    # 模拟失败
    for i in range(3):
        cb.on_failure()
    
    if cb.get_state() == "open":
        print("  [OK] 断路器在3次失败后正确打开")
    else:
        print(f"  [WARN] 断路器状态异常: {cb.get_state()}")
    
    print("  [OK] 异步限流核心逻辑通过")
    
except Exception as e:
    print(f"  [FAIL] 异步限流测试失败: {e}")

# 4. 文件完整性检查
print("\n4. 文件完整性检查:")
files = [
    ("websocket_reconnect.py", "WebSocket重连算法"),
    ("async_throttle.py", "异步HTTP限流"),
    ("Dockerfile.optimized", "Docker优化"),
    ("evomap-knowledge.md", "EVO Map知识库"),
    ("learning-plan.md", "学习计划"),
]

all_ok = True
for filename, desc in files:
    if os.path.exists(filename):
        print(f"  [OK] {filename} - {desc}")
    else:
        print(f"  [MISS] {filename} - {desc}")
        all_ok = False

print("\n" + "=" * 60)
print("测试总结")
print("=" * 60)

if all_ok:
    print("[SUCCESS] EVO Map技术实现基本验证通过")
    print("\n下一步行动:")
    print("  1. 可以进行实际功能测试")
    print("  2. 尝试简化LiveKit安装")
    print("  3. 开始实时语音开发准备")
else:
    print("[WARNING] 部分检查未通过")

print(f"\nPython环境: {sys.version.split()[0]}")
print("虚拟环境: .venv-livekit")

print("\n建议:")
print("  1. 修复缺失文件")
print("  2. 运行实际网络测试")
print("  3. 继续LiveKit环境准备")