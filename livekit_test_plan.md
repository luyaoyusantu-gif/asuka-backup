# LiveKit 实时语音学习与测试计划

**创建时间**：2026-03-17  
**目标**：基于用户需求，实现实时语音对话能力

## 🎯 学习目标

### 核心能力
1. **语音识别 (STT)**：将用户语音转换为文本
2. **语言理解 (LLM)**：理解用户意图并生成回复
3. **语音合成 (TTS)**：将文本回复转换为语音
4. **实时流处理**：低延迟的语音流传输

### 技术栈选择
根据 LiveKit SKILL.md 建议：

| 组件 | 预算型 | 质量型 | 低延迟型 | **推荐选择** |
|------|--------|--------|----------|--------------|
| **STT** | Deepgram Nova-3 | AssemblyAI | Deepgram Keychain | **Deepgram Nova-3** (性价比) |
| **LLM** | GPT-4.1 mini | Claude Sonnet | GPT-4.1 mini | **GPT-4.1 mini** (成本优化) |
| **TTS** | Cartesia Sonic-3 | ElevenLabs | Cartesia Sonic-3 | **Cartesia Sonic-3** (低延迟) |

## 📋 环境准备

### 1. Python 环境
```bash
# 检查 Python 版本
python --version  # 需要 Python 3.11+

# 创建虚拟环境 (推荐)
python -m venv .venv-livekit
# Windows
.venv-livekit\Scripts\activate
# Mac/Linux
source .venv-livekit/bin/activate
```

### 2. 安装 LiveKit SDK
```bash
# 基础 SDK
pip install livekit-agents

# 插件 (根据需要选择)
pip install livekit-plugins-openai     # OpenAI LLM
pip install livekit-plugins-deepgram   # Deepgram STT
pip install livekit-plugins-cartesia   # Cartesia TTS
pip install livekit-plugins-elevenlabs # ElevenLabs TTS (备用)
```

### 3. API Key 准备
需要获取以下 API Key：
```bash
# LiveKit Cloud (或自托管)
export LIVEKIT_URL=wss://your-app.livekit.cloud
export LIVEKIT_API_KEY=your-api-key
export LIVEKIT_API_SECRET=your-api-secret

# 提供商 API Key
export OPENAI_API_KEY=            # GPT-4.1 mini
export DEEPGRAM_API_KEY=          # Deepgram STT
export CARTESIA_API_KEY=          # Cartesia TTS
export ELEVENLABS_API_KEY=        # ElevenLabs TTS (备用)
```

## 🔧 测试项目结构

```
livekit-test/
├── config.py          # 配置管理
├── simple_agent.py    # 最小语音 Agent
├── feishu_integration.py  # 飞书集成
├── requirements.txt   # 依赖列表
└── README.md         # 项目说明
```

## 🚀 实施步骤

### 阶段 1：最小可行产品 (MVP)

#### 1.1 配置管理 (`config.py`)
```python
import os
from dataclasses import dataclass

@dataclass
class Config:
    # LiveKit
    livekit_url: str = os.getenv("LIVEKIT_URL", "wss://localhost:7880")
    livekit_api_key: str = os.getenv("LIVEKIT_API_KEY", "")
    livekit_api_secret: str = os.getenv("LIVEKIT_API_SECRET", "")
    
    # 提供商
    openai_api_key: str = os.getenv("OPENAI_API_KEY", "")
    deepgram_api_key: str = os.getenv("DEEPGRAM_API_KEY", "")
    cartesia_api_key: str = os.getenv("CARTESIA_API_KEY", "")
    
    # 模型选择
    llm_model: str = "gpt-4.1-mini"      # 成本优化
    stt_provider: str = "deepgram"       # Deepgram Nova-3
    tts_provider: str = "cartesia"       # Cartesia Sonic-3
    
config = Config()
```

#### 1.2 最小语音 Agent (`simple_agent.py`)
```python
#!/usr/bin/env python3
"""
LiveKit 最小语音 Agent - 基于官方示例
参考: https://docs.livekit.io/agents/quickstart
"""

import asyncio
import logging
from livekit.agents import AgentSession, JobContext, WorkerOptions, cli
from livekit.plugins import deepgram, openai, cartesia

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def entrypoint(ctx: JobContext):
    """Agent 入口点"""
    logger.info("连接 LiveKit 服务器...")
    await ctx.connect()
    
    logger.info("创建语音会话...")
    session = AgentSession(
        # 语音识别 (STT)
        stt=deepgram.STT(),
        
        # 语言模型 (LLM)
        llm=openai.LLM(model="gpt-4.1-mini"),
        
        # 语音合成 (TTS)
        tts=cartesia.TTS(),
        
        # 可选: 语音检测
        # turn_detection=openai.TurnDetection(
        #     threshold=0.5,
        #     silence_duration_ms=500,
        # ),
    )
    
    # 启动会话
    session.start(ctx.room)
    logger.info("语音会话已启动")
    
    # 欢迎语
    await session.say("你好！我是你的语音助手。有什么可以帮你的吗？")
    
    # 保持运行
    try:
        await asyncio.Future()  # 永久运行
    except asyncio.CancelledError:
        logger.info("会话结束")
    finally:
        session.stop()


if __name__ == "__main__":
    # 启动 Worker
    cli.run_app(WorkerOptions(entrypoint_fnc=entrypoint))
```

#### 1.3 依赖文件 (`requirements.txt`)
```txt
livekit-agents>=0.1.0
livekit-plugins-openai>=0.1.0
livekit-plugins-deepgram>=0.1.0
livekit-plugins-cartesia>=0.1.0
```

### 阶段 2：功能增强

#### 2.1 工具调用扩展
```python
from livekit.agents import function_tool

@function_tool()
async def get_weather(location: str) -> str:
    """获取指定位置的天气信息"""
    # 实现天气查询逻辑
    return f"{location}的天气：晴天，25°C"

@function_tool()
async def search_web(query: str) -> str:
    """搜索网络信息"""
    # 实现网络搜索逻辑
    return f"关于'{query}'的搜索结果：..."

# 在 AgentSession 中添加工具
session = AgentSession(
    stt=deepgram.STT(),
    llm=openai.LLM(),
    tts=cartesia.TTS(),
    tools=[get_weather, search_web],  # 添加工具
)
```

#### 2.2 飞书集成原型
```python
"""
飞书语音消息集成原型
思路：飞书语音消息 → 下载音频 → STT → LLM → TTS → 飞书语音回复
"""

import asyncio
from feishu_utils import download_voice_message, send_voice_message

async def feishu_voice_processor(audio_url: str, user_id: str):
    """处理飞书语音消息"""
    # 1. 下载语音消息
    audio_file = await download_voice_message(audio_url)
    
    # 2. STT: 语音转文本
    text = await stt_client.transcribe(audio_file)
    
    # 3. LLM: 生成回复
    reply_text = await llm_client.generate_reply(text, context=user_id)
    
    # 4. TTS: 文本转语音
    voice_file = await tts_client.synthesize(reply_text)
    
    # 5. 发送语音回复
    await send_voice_message(user_id, voice_file)
    
    return reply_text
```

### 阶段 3：生产部署

#### 3.1 Docker 容器化
```dockerfile
# 基于阶段 1 的优化 Dockerfile
FROM python:3.12-slim

WORKDIR /app

# 复制依赖文件
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 复制源代码
COPY . .

# 环境变量
ENV PYTHONPATH=/app:$PYTHONPATH

# 运行 Agent
CMD ["python", "simple_agent.py"]
```

#### 3.2 部署选项
1. **LiveKit Cloud**：托管服务，快速启动
2. **自托管**：使用 Docker Compose
3. **混合部署**：开发用云服务，生产自托管

## 📊 测试计划

### 测试 1：基础功能
- [ ] LiveKit 服务器连接
- [ ] STT 准确性测试
- [ ] TTS 质量测试
- [ ] 端到端延迟测量

### 测试 2：性能测试
- [ ] 并发连接数
- [ ] 内存使用情况
- [ ] CPU 使用率
- [ ] 网络带宽需求

### 测试 3：集成测试
- [ ] 飞书消息处理
- [ ] 错误恢复能力
- [ ] 长时间运行稳定性

## ⚠️ 风险与缓解

### 技术风险
1. **延迟过高**：实时语音需要 <500ms 延迟
   - 缓解：选择低延迟提供商，优化网络路径
   
2. **成本控制**：语音服务可能产生费用
   - 缓解：使用免费层级，设置用量警报
   
3. **依赖复杂性**：多个服务集成
   - 缓解：分阶段实施，充分测试

### 实施风险
1. **API Key 管理**：多个服务需要密钥
   - 缓解：使用环境变量，密钥轮换机制
   
2. **错误处理**：网络不稳定
   - 缓解：实现重试逻辑，优雅降级

## 🔍 评估指标

### 成功标准
1. **功能**：实现双向语音对话
2. **性能**：端到端延迟 <500ms
3. **可用性**：>99% 服务可用性
4. **成本**：每月费用 <$100（测试阶段）

### 检查点
- 每周五：功能进展检查
- 每月初：成本与性能评估
- 用户反馈：定期收集使用反馈

## 📝 学习资源

### 官方文档
1. [LiveKit Agents 文档](https://docs.livekit.io/agents/)
2. [LiveKit Python SDK](https://github.com/livekit/agents-python)
3. [插件文档](https://github.com/livekit/agents-plugins)

### 参考项目
1. [LiveKit 官方示例](https://github.com/livekit/agents/tree/main/examples)
2. [语音 Agent 最佳实践](https://docs.livekit.io/agents/guides/best-practices)

### 社区资源
1. [LiveKit Discord](https://discord.gg/livekit)
2. [GitHub Issues](https://github.com/livekit/agents/issues)

## 🚀 立即行动

### 短期（本周）
1. 设置 Python 虚拟环境
2. 申请必要的 API Key（测试用）
3. 运行最小 Agent 示例

### 中期（2-3周）
1. 完善飞书集成原型
2. 性能测试与优化
3. 错误处理与监控

### 长期（1个月+）
1. 生产环境部署
2. 用户测试与反馈收集
3. 功能扩展（多语言、自定义语音等）

---

**下一步**：根据此计划，逐步实施 LiveKit 语音 Agent，优先完成最小可行产品，然后迭代增强。

*注意：所有实施将遵循安全边界，不泄露配置和用户数据*