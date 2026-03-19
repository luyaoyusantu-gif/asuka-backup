#!/usr/bin/env python3
"""
LiveKit 最小测试 - 验证安装和基本结构
"""

import sys
import os

print("LiveKit 最小化测试")
print("=" * 50)

# 1. 检查LiveKit导入
print("\n1. LiveKit包导入检查:")

try:
    import livekit
    print(f"  livekit: OK (版本: {livekit.__version__})")
except ImportError as e:
    print(f"  livekit: FAIL - {e}")
    sys.exit(1)

try:
    import livekit.agents
    print(f"  livekit.agents: OK")
except ImportError as e:
    print(f"  livekit.agents: FAIL - {e}")
    sys.exit(1)

try:
    import livekit.plugins
    print(f"  livekit.plugins: OK")
except ImportError as e:
    print(f"  livekit.plugins: FAIL - {e}")
    sys.exit(1)

# 2. 检查插件
print("\n2. LiveKit插件检查:")

try:
    from livekit.plugins import deepgram
    print(f"  deepgram插件: OK")
except ImportError as e:
    print(f"  deepgram插件: FAIL - {e} (需要 livekit-plugins-deepgram)")

try:
    from livekit.plugins import openai
    print(f"  openai插件: OK")
except ImportError as e:
    print(f"  openai插件: FAIL - {e} (需要 livekit-plugins-openai)")

try:
    from livekit.plugins import cartesia
    print(f"  cartesia插件: OK")
except ImportError:
    print(f"  cartesia插件: 未安装 (可选)")

# 3. 测试AgentSession结构
print("\n3. AgentSession结构测试:")

try:
    from livekit.agents import AgentSession, JobContext, WorkerOptions
    
    print(f"  AgentSession: OK")
    print(f"  JobContext: OK") 
    print(f"  WorkerOptions: OK")
    
    # 测试创建最小Agent结构（不实际运行）
    async def dummy_entrypoint(ctx: JobContext):
        """虚拟入口点，用于测试结构"""
        print(f"   虚拟入口点结构正常")
        return
    
    # 创建WorkerOptions测试
    worker_opts = WorkerOptions(entrypoint_fnc=dummy_entrypoint)
    print(f"  WorkerOptions创建: OK")
    
except Exception as e:
    print(f"  Agent结构测试失败: {e}")
    import traceback
    traceback.print_exc()

# 4. 检查环境变量
print("\n4. 环境变量检查:")

required_env_vars = [
    "LIVEKIT_URL",
    "LIVEKIT_API_KEY", 
    "LIVEKIT_API_SECRET",
    "OPENAI_API_KEY",
    "DEEPGRAM_API_KEY",
]

for var in required_env_vars:
    value = os.getenv(var)
    if value:
        print(f"  {var}: 已设置 ({'*' * min(len(value), 10)}...)")
    else:
        print(f"  {var}: 未设置")

# 5. 提供最小示例代码
print("\n5. 最小语音Agent示例代码:")
print("-" * 40)

example_code = '''
#!/usr/bin/env python3
from livekit.agents import AgentSession, JobContext, WorkerOptions, cli
from livekit.plugins import deepgram, openai

async def entrypoint(ctx: JobContext):
    await ctx.connect()
    
    session = AgentSession(
        stt=deepgram.STT(),
        llm=openai.LLM(model="gpt-4.1-mini"),
        # tts=cartesia.TTS(),  # 需要 cartesia API key
    )
    
    session.start(ctx.room)
    await session.say("Hello! How can I help?")

if __name__ == "__main__":
    cli.run_app(WorkerOptions(entrypoint_fnc=entrypoint))
'''

print(example_code)

print("\n" + "=" * 50)
print("测试总结")
print("=" * 50)

print("\n下一步行动:")
print("  1. 设置必要的API Key环境变量")
print("  2. 运行最小语音Agent测试")
print("  3. 测试不同提供商 (Deepgram, OpenAI, Cartesia)")
print("  4. 集成到飞书消息流")

print("\n环境变量示例 (.env文件):")
print("""
LIVEKIT_URL=wss://your-app.livekit.cloud
LIVEKIT_API_KEY=your-api-key
LIVEKIT_API_SECRET=your-api-secret
OPENAI_API_KEY=your-openai-key
DEEPGRAM_API_KEY=your-deepgram-key
CARTESIA_API_KEY=your-cartesia-key  # 可选
""")

print(f"\nPython环境: {sys.version.split()[0]}")
print(f"虚拟环境: .venv-livekit")