# Evolution Status — 自进化状态跟踪

> 由每日复盘模块自动维护

## 上次复盘

- **时间**：2026-03-22 10:00
- **状态**：已完成

## 待改进项（按优先级）

| # | 缺口 | 首次发现 | 最近出现 | 状态 |
|---|------|----------|----------|------|
| 1 | 外部AI控制/Agent对接 | 2026-03-21 | 2026-03-21 | 🔍 搜索中 |
| 2 | 视频观看能力 | 2026-03-20 | 2026-03-20 | 🔍 搜索中 |
| 3 | DeepSeek 模型切换/配置 | 2026-03-17 | 2026-03-18 | 🔍 搜索中 |
| 4 | 实时语音对话 | 2026-03-16 | 2026-03-17 | ✅ 实施中（已安装 livekit） |

## 本周趋势

- **新增缺口**：4 个
- **已解决**：0 个
- **待关注**：4 个

## 历史安装记录

| 日期 | 资产 | 类型 | 来源 |
|------|------|------|------|
| 2026-03-17 | livekit | skill | 水产市场 |
| 2026-03-09 | self-evolution | experience | 水产市场 |
| 2026-03-09 | Semantic | experience | 水产市场 |

## 今日推荐资产

### 1. WebSocket Reconnection Experience
- **类型**：Experience
- **名称**：WebSocket Reconnect with Exponential Backoff and Jitter
- **描述**：生产级 WebSocket 重连算法实现
- **匹配度**：参考价值（与 EVO Map 已实施的重连算法相关）
- **安装命令**：`openclawmp install experience/@u-b1660de1be4240329321/websocket-reconnect-jitter`

### 2. 飞书工具库 (Feishu Toolkit)
- **类型**：Skill
- **名称**：飞书工具库
- **描述**：支持飞书消息、群聊、文档管理，长连接监听
- **匹配度**：参考价值（长连接可用于 Agent 对接）
- **安装命令**：`openclawmp install skill/@u-f2cc628f921944d8ac01/飞书工具库`

### 3. LLM Router Gateway
- **类型**：Skill
- **名称**：LLM Router Gateway
- **描述**：统一 LLM 网关，支持 70+ 模型，包括 DeepSeek
- **匹配度**：强匹配（解决 DeepSeek 模型切换问题）
- **安装命令**：`openclawmp install skill/@u-763bb22d91255889/aisa-llm-router-skill`

### 4. 即梦AI视频文案生成器
- **类型**：Skill
- **名称**：jimeng-video-script
- **描述**：快速生成短视频提示词和文案
- **匹配度**：弱匹配（视频内容相关，非观看）
- **安装命令**：`openclawmp install skill/@u-fdbead8168de4c54a6f4/jimeng-video-script`

---

> auto_install=ask，本次复盘仅推荐，不自动安装
