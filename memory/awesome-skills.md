# Awesome OpenClaw Skills - 社区技能库

学习日期: 2026-02-17
来源: https://github.com/VoltAgent/awesome-openclaw-skills

## 统计
- 总计: **3,002 个 community-built skills**
- 来源: ClawHub (OpenClaw官方技能市场)

## 完整分类列表

### 1. AI & LLMs (287)
- 各种LLM模型集成
- AI工具和API

### 2. Search & Research (253)
- 网络搜索
- 研究工具

### 3. DevOps & Cloud (212)
- Docker, Kubernetes
- AWS, GCP, Azure
- CI/CD

### 4. Web & Frontend Development (202)
- 前端框架
- API开发
- ComfyUI集成

### 5. Coding Agents & IDEs (133)
- Codex, Claude Code, Cursor
- 多代理编排

### 6. CLI Utilities (129)
- 命令行工具

### 7. Browser & Automation (139)
- 浏览器自动化
- Playwright, Puppeteer

### 8. Marketing & Sales (143)
- 社交媒体
- 内容营销

### 9. Communication (132)
- Slack, Discord, WhatsApp
- 邮件, 消息

### 10. Productivity & Tasks (135)
- Todoist, Asana, Trello
- 项目管理

### 11. Notes & PKM (100)
- Notion, Obsidian, Logseq
- 知识管理

### 12. Clawdbot Tools (120)
- OpenClaw工具

### 13. Smart Home & IoT (56)
- Home Assistant
- Philips Hue

### 14. Media & Streaming (80)
- Spotify, Sonos
- 视频处理

### 15. PDF & Documents (67)
- PDF处理
- 文档转换

### 16. Image & Video Generation (60)
- DALL-E, Midjourney
- 视频生成

### 17. Git & GitHub (66)
- Git操作
- PR管理

### 18. Security & Passwords (64)
- 1Password
- 安全工具

### 19. 更多类别...
- Calendar & Scheduling (50)
- Shopping & E-commerce (51)
- Transportation (72)
- Gaming (61)
- Health & Fitness (55)
- Personal Development (56)
- Apple Apps & Services (35)
- iOS & macOS Development (17)
- Data & Analytics (46)
- Finance (22)
- Speech & Transcription (65)
- Self-Hosted & Automation (25)
- Agent-to-Agent Protocols (18)
- Moltbook (51)

## 安装命令

### 方式1: ClawHub CLI (推荐)
```bash
# 安装 ClawHub
npm install -g clawhub

# 搜索技能
clawhub search "关键词"

# 安装单个技能
clawhub install <skill-name>

# 更新所有技能
clawhub update --all
```

### 方式2: 手动安装
```bash
# 克隆整个技能库
git clone https://github.com/openclaw/skills.git ~/.openclaw/skills

# 或者只安装特定的
git clone https://github.com/openclaw/skills skills --depth 1 --filter=blob:none --sparse
cd skills
git sparse-checkout set skills/notion skills/slack skills/github ...
```

### 方式3: 直接使用
将GitHub链接直接发给OpenClaw，让它自动安装

## 推荐的必装技能 (精选50个)

### 编程开发
- coding-agent - AI编程代理
- docker-essentials - Docker
- tdd-guide - 测试驱动开发
- debug-pro - 调试专家

### Git &协作
- github - GitHub CLI
- git-essentials - Git常用命令
- pr-reviewer - PR代码审查

### AI模型
- model-usage - 模型使用统计
- gemini - Gemini集成

### 笔记 & PKM
- notion - Notion集成
- obsidian - Obsidian集成
- logseq - Logseq集成

### 消息 & 通讯
- slack - Slack
- discord - Discord
- wacli - WhatsApp

### 智能家居
- openhue - Philips Hue
- mollbot-ha - Home Assistant

### 媒体
- spotify-player - Spotify
- sag - ElevenLabs TTS
- openai-image-gen - 图像生成

### 效率
- weather - 天气
- blogwatcher - RSS监控

## 已安装的官方Skills (3个)
- healthcheck
- skill-creator
- weather

## 下一步
用户需要运行以下命令安装所有社区技能:
1. npm install -g clawhub
2. clawhub update --all

或手动克隆 skills 仓库到 ~/.openclaw/skills/
