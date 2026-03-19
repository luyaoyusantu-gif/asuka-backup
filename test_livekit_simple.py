#!/usr/bin/env python3
"""
LiveKit简单导入测试
"""

import sys

print("LiveKit导入测试")
print("=" * 50)

try:
    import livekit
    print(f"[OK] livekit {livekit.__version__}")
except ImportError as e:
    print(f"[FAIL] livekit: {e}")
    sys.exit(1)

try:
    import livekit.agents
    print("[OK] livekit.agents")
except ImportError as e:
    print(f"[FAIL] livekit.agents: {e}")

try:
    # 测试核心结构
    from livekit.agents import AgentSession, JobContext, WorkerOptions
    print("[OK] AgentSession, JobContext, WorkerOptions 导入正常")
except ImportError as e:
    print(f"[FAIL] 核心类导入: {e}")

print("\n" + "=" * 50)
print("LiveKit环境状态:")
print(f"  Python: {sys.version.split()[0]}")
print(f"  虚拟环境: .venv-livekit")

print("\n下一步:")
print("  1. 安装插件: pip install livekit-plugins-openai")
print("  2. 获取API Key: OpenAI, Deepgram等")
print("  3. 创建最小语音Agent")

print("\n最小示例代码已准备在 livekit_test_plan.md")