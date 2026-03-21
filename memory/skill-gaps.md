# Skill Gaps — 能力缺口记录

> 由自进化系统信号采集模块自动维护。格式：`[日期] [类型] 描述 | session: key | 关键词: xxx`

---

## 2026-03-21 信号采集记录

- [2026-03-21] [Missing] 用户要求直接将指令发给ocbot（内置AI的浏览器）的AI对话，但尝试API端口、DevTools协议等方式均失败，无法实现跨AI系统控制 | session: agent:main:main | 关键词: ocbot, 外部AI控制, Agent对接, AI互联

## 2026-03-20 信号采集记录

- [2026-03-20] [Missing] 用户询问能否看抖音视频，Agent明确表示无法可靠观看视频内容（浏览器工具仅支持截图，视频需播放能力）| session: agent:main:main | 关键词: video watch, 抖音, 视频理解, 视频内容

## 2026-03-17 信号采集记录

- [2026-03-17] [Missing] 用户询问是否可以接入evo map，Agent表示没有相关记忆记录 | session: agent:main:main | 关键词: evo map, 接入, API集成
- [2026-03-17] [Failure] 用户询问为什么Agent在之前的窗口中没找到DeepSeek API密钥，指出配置查找能力不足 | session: agent:main:session-1773740772814 | 关键词: deepseek密钥, 配置查找, API配置
- [2026-03-17] [Failure] 用户要求切换到DeepSeek R1模型，Agent错误地切换到了本地Ollama版本而非联网API版本，需要用户纠正 | session: agent:main:main | 关键词: 模型切换, deepseek api, 配置错误
- [2026-03-17] [实施中] 实时语音对话能力：已完成 EVO Map 技术实施，创建 3 个生产级解决方案 | session: agent:main | 关键词: 实时语音, WebSocket, Docker, asyncio, EVO Map
- [2026-03-17] [进展] WebSocket 全抖动重连算法已实现（基于 EVO Map Top 1 Capsule） | session: agent:main | 关键词: 重连算法, 指数退避, 全抖动
- [2026-03-17] [进展] 异步 HTTP 限流客户端已实现（基于 EVO Map Top 3 Capsule） | session: agent:main | 关键词: 信号量, 连接池, 断路器
- [2026-03-17] [进展] Docker 层缓存优化已应用（基于 EVO Map Top 2 Capsule） | session: agent:main | 关键词: 多阶段构建, 层缓存, 镜像优化

## 2026-03-19 信号采集记录

- [2026-03-19] [扫描] 本次扫描3个活跃session，未发现新的能力缺口信号 | session: cron:e36ddfa7 | 关键词: signal collection, 扫描

---

## 2026-03-18 信号采集记录

- [2026-03-18] [Missing] 用户要求切换到 deepseek v3.2 模型，但 DeepSeek API 目前只提供 deepseek‑chat 和 deepseek‑reasoner | session: agent:main:session-1773740772814 | 关键词: deepseek v3.2, 模型列表, 模型发现

## 2026-03-16 信号采集记录

- [2026-03-16] [扫描] 本次扫描2个活跃session，识别到1条新信号 | session: cron:e36ddfa7 | 关键词: signal collection, 扫描
- [2026-03-16] [Suggestion] 用户提到豆包愿意提供实时语音大模型，希望我能实现语音实时对话能力 | session: agent:main:main | 关键词: 实时语音, voice chat, TTS, ASR, RTC

- [2026-03-14] [扫描] 本次扫描3个活跃session，未发现新的能力缺口信号 | session: cron:e36ddfa7 | 关键词: signal collection, 扫描

---

## 2026-03-13 信号采集记录

- [2026-03-13] [扫描] 本次扫描3个活跃session，未发现新的能力缺口信号 | session: cron:signal-collection | 关键词: signal collection, 扫描
- [2026-03-13] [备注] 429 API限额错误为环境问题，不计入缺口 | session: cron:signal-collection | 关键词: quota, API limit
