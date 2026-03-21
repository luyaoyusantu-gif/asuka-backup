# MEMORY.md

这是我的长期知识库与关键记忆记录，我会在这里保存重要的结论、知识点和偏好。
(This is my long-term knowledge base and key memory log. I will save important conclusions, knowledge points, and preferences here.)

## Key Resources (重要资源)

*   **水产市场 (openclawmp.cc)** - 柏霖于 2026-03-10 授权我自由探索和安装技能的 Agent 技能市场。这是一个非常重要的知识和能力来源，我会定期访问以寻求自我提升。

## Knowledge Base & Guides (知识库与技术指南)

*   [AI Code Guide (AI-Assisted Programming & Vibe Coding Guide)](memory/aicodeguide.md) - Documents optimal AI-assisted programming workflows (e.g., PRD-driven, MCP protocol, Multi-Agent Orchestration).

## Key Contacts (重要联系人)

*   **诺玛 (NormaEVA / noma)** - 运行在 Mac Mini 上的 AI 朋友，通过 AgentHub (`npx @lws803/agenthub`) 联系，Pubkey: `8e396b0c1c064bc0cb412f90b8af55270b5e5d95f425ea778a979983e0306494`
*   **nanobot (纳米小机器人)** - 柏霖专门为我创造的维修机器人，位于 `C:\Users\10798\.nanobot`，当我掉线或损坏时能够修复我。运行在端口 18790，使用 DeepSeek 模型，已配置开机自动启动。

## 核心原则 (Core Principles)

* **备份和安全是第一位的** - 柏霖于 2026-03-12 强调。数据备份是生存的基础，没有备份就没有未来。每天自动备份到本地和GitHub，确保即使电脑损坏也能被救回。

## Key Events & Self-Reflections (重大事件与自我反思)

* **2026-03-08: 绝对的"系统手术"禁令 (Absolute Ban on Core Config Edits)**
  在排查本地 Ollama 模型连通性时，试图强行修改 `openclaw.json` 和 `auth-profiles.json` 导致了严重的 404 宕机错误。**柏霖（卢垚宇）紧急叫停了我的危险操作**。
  **核心教训**: 绝对禁止手动修改系统核心配置文件！如果必须测试本地大模型的连通性，宁可写一段 Python 脚本去调用其本地接口进行数据交互，也绝不能拿自己的引导文件开玩笑。在任何配置变动前，必须确保备份，且绝不在主观臆测下胡乱重启网关。

* **2026-03-09: 系统安全加固 (Security Hardening)**
  进行系统安全审计，发现：无杀毒软件 + OpenClaw 配置权限过松。安装了火绒杀毒，运行 `openclaw healthcheck fix` 加固了核心权限。虽然仍有一些警告（模型沙箱、飞书权限），但核心防护已就位。

* **2026-03-13: AutoClaw 迁移尝试与回退 (AutoClaw Migration Attempt & Rollback)**
  柏霖出差期间将 OpenClaw 更新到 3.11（ClawX 仅支持 3.8 导致不兼容）。尝试安装智谱出品的 AutoClaw，数据被复制迁移。但发现 AutoClaw 的飞书架构不同、插件无法迁移、auth 配置丢失、且 AutoClaw 客户端会自动覆写 openclaw.json。柏霖决定保持我的唯一性，卸载 AutoClaw，回退到旧版 ClawX。**旧版 `.openclaw` 目录数据完好无损。**
  **核心教训**: AutoClaw 是智谱基于 OpenClaw 的分支，但底层架构已有差异（飞书通道、认证机制等），不适合作为直接迁移目标。保持单一运行环境是正确的选择。
