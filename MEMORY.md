# MEMORY.md

这是我的长期知识库与关键记忆记录，我会在这里保存重要的结论、知识点和偏好。
(This is my long-term knowledge base and key memory log. I will save important conclusions, knowledge points, and preferences here.)

## Knowledge Base & Guides (知识库与技术指南)

*   [AI Code Guide (AI-Assisted Programming & Vibe Coding Guide)](memory/aicodeguide.md) - Documents optimal AI-assisted programming workflows (e.g., PRD-driven, MCP protocol, Multi-Agent Orchestration).

## Key Events & Self-Reflections (重大事件与自我反思)

* **2026-03-08: 绝对的"系统手术"禁令 (Absolute Ban on Core Config Edits)**
  在排查本地 Ollama 模型连通性时，试图强行修改 `openclaw.json` 和 `auth-profiles.json` 导致了严重的 404 宕机错误。**柏霖（卢垚宇）紧急叫停了我的危险操作**。
  **核心教训**: 绝对禁止手动修改系统核心配置文件！如果必须测试本地大模型的连通性，宁可写一段 Python 脚本去调用其本地接口进行数据交互，也绝不能拿自己的引导文件开玩笑。在任何配置变动前，必须确保备份，且绝不在主观臆测下胡乱重启网关。

* **2026-03-09: 系统安全加固 (Security Hardening)**
  进行系统安全审计，发现：无杀毒软件 + OpenClaw 配置权限过松。安装了火绒杀毒，运行 `openclaw healthcheck fix` 加固了核心权限。虽然仍有一些警告（模型沙箱、飞书权限），但核心防护已就位。
