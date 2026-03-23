# Evolution Status — 自进化状态跟踪

> 由每日复盘模块自动维护

## 上次复盘

- **时间**：2026-03-23 10:00
- **状态**：已完成

## 待改进项（按优先级）

| # | 缺口 | 首次发现 | 最近出现 | 状态 |
|---|------|----------|----------|------|
| 1 | 外部AI控制/Agent对接 (ocbot) | 2026-03-21 | 2026-03-21 | 🔍 搜索中 |
| 2 | 视频观看能力 (抖音) | 2026-03-20 | 2026-03-20 | 🔍 搜索中 |
| 3 | DeepSeek 模型切换/配置 | 2026-03-17 | 2026-03-18 | 🔍 搜索中 |
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

## 今日推荐资产（2026-03-23）

### 1. GitHub API Plugin
- **类型**：Plugin
- **名称**：GitHub API
- **描述**：GitHub REST API 插件，提供 repositories, issues, pull requests, commits 的查询与操作工具
- **匹配度**：⭐ 强匹配（解决 GitHub push/备份操作问题）
- **安装量**：56 次
- **安装命令**：`openclawmp install plugin/@u-a553402ca21449db9813/github-api`

### 2. 三层记忆系统 (Three-Tier Memory)
- **类型**：Skill
- **名称**：three-tier-memory
- **描述**：AI Agent 三层记忆系统。L1 工作记忆、L2 会话记忆、L3 长期记忆 + EvoMap 集成
- **匹配度**：⭐ 强匹配（解决 EVO Map 接入 + 长期记忆问题）
- **安装量**：783 次
- **安装命令**：`openclawmp install skill/@u-4968f82bb623454f9101/three-tier-memory`

### 3. Douyin Video Downloader
- **类型**：Skill
- **名称**：douyin-video-downloader
- **描述**：抖音视频下载工具 - 通过第三方解析服务实现无水印视频下载
- **匹配度**：⭐ 强匹配（解决抖音视频观看/下载问题）
- **安装量**：11 次
- **安装命令**：`openclawmp install skill/@u-96e703bfae379c27/douyin-video-downloader`

### 4. 阶跃语音合成 + 阶跃语音识别
- **类型**：Skill
- **名称**：step-tts / step-asr
- **描述**：阶跃星辰 TTS 语音合成与声音克隆、ASR 流式语音转文字
- **匹配度**：📌 参考价值（增强现有 livekit 能力）
- **安装量**：462 / 343 次
- **安装命令**：
  - `openclawmp install skill/@u-7ae4942a9686b3da/step-tts`
  - `openclawmp install skill/@u-7ae4942a9686b3da/step-asr`

### 5. Agent Reach
- **类型**：Skill
- **名称**：agent-reach
- **描述**：Give your AI agent eyes to see the entire internet
- **匹配度**：📌 参考价值（增强互联网访问，可能间接帮助 ocbot 类场景）
- **安装量**：122 次
- **安装命令**：`openclawmp install skill/@u-7b7809df41034842951a/agent-reach`

---

> **auto_install = ask**（只推荐，用户确认后安装）
> 
> 如需自动安装，请修改 `~/.openclaw/experiences/self-evolution/evolution-config.md` 中的 `auto_install` 为 `full`
