# Evolution Status — 自进化状态跟踪

> 由每日复盘模块自动维护

## 上次复盘

- **时间**：2026-03-24 10:00
- **状态**：已完成

## 待改进项（按优先级）

| # | 缺口 | 首次发现 | 最近出现 | 状态 |
|---|------|----------|----------|------|
| 1 | DeepSeek 模型切换/配置查找 | 2026-03-17 | 2026-03-22 | 🔍 搜索中 |
| 2 | 外部AI控制/Agent对接 (ocbot) | 2026-03-21 | 2026-03-21 | 🔍 搜索中 |
| 3 | 视频观看能力 (抖音) | 2026-03-20 | 2026-03-20 | 🔍 搜索中 |
| 4 | GitHub 操作 (push/备份) | 2026-03-22 | 2026-03-22 | 🔍 搜索中 |
| 5 | 实时语音对话 | 2026-03-16 | 2026-03-17 | ✅ 已解决（已安装 livekit） |
| 6 | EVO Map 接入 | 2026-03-17 | 2026-03-17 | 🔍 搜索中 |

## 本周趋势

- **新增缺口**：6 个
- **已解决**：1 个（实时语音 - livekit 已安装）
- **待关注**：5 个

## 历史安装记录

| 日期 | 资产 | 类型 | 来源 |
|------|------|------|------|
| 2026-03-17 | livekit | skill | 水产市场 |
| 2026-03-09 | self-evolution | experience | 水产市场 |
| 2026-03-09 | Semantic | experience | 水产市场 |

## 今日推荐资产（2026-03-24）

### 1. Video Download
- **类型**：Skill
- **名称**：video-download
- **描述**：Download videos from 1800+ websites and generate subtitles using Faster Whisper
- **匹配度**：⭐ 强匹配（解决视频观看/下载问题）
- **安装量**：10 次
- **安装命令**：`openclawmp install skill/@u-993ae0bf4d068904/video-download`

### 2. Douyin Video Downloader
- **类型**：Skill
- **名称**：douyin-video-downloader
- **描述**：抖音视频下载工具 - 通过第三方解析服务实现无水印视频下载
- **匹配度**：⭐ 强匹配（解决抖音视频观看问题）
- **安装量**：11 次
- **安装命令**：`openclawmp install skill/@u-96e703bfae379c27/douyin-video-downloader`

### 3. LiveKit Voice AI
- **类型**：Skill
- **名称**：livekit
- **描述**：Build voice AI agents with LiveKit. Use when developing realtime voice applications
- **匹配度**：✅ 已安装（实时语音能力已解决）
- **安装量**：7 次
- **状态**：已安装于 2026-03-17

### 4. ClawRouter (DeepSeek 路由)
- **类型**：Plugin
- **名称**：clawrouter
- **描述**：The agent-native LLM router empowering OpenClaw — 支持 DeepSeek 等多模型路由
- **匹配度**：📌 参考价值（可能帮助模型切换配置）
- **安装量**：53 次
- **安装命令**：`openclawmp install plugin/@gh-blockrunai/clawrouter`

### 5. LLM Router Gateway
- **类型**：Skill
- **名称**：aisa-llm-router-skill
- **描述**：Unified LLM Gateway - One API for 70+ AI models. Route to GPT, Claude, Gemini, Qwen, Deepseek
- **匹配度**：📌 参考价值（统一模型网关，可能帮助模型切换问题）
- **安装量**：2 次
- **安装命令**：`openclawmp install skill/@u-763bb22d91255889/aisa-llm-router-skill`

---

> **auto_install = ask**（只推荐，用户确认后安装）
> 
> 如需自动安装，请修改 `~/.openclaw/experiences/self-evolution/evolution-config.md` 中的 `auto_install` 为 `full`
