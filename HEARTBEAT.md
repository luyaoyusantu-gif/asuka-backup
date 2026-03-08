# HEARTBEAT.md

# [CRON] Daily Backup - 00:00
# Run daily at midnight to backup workspace data
# Schedule: 0 0 * * *
# Task: Create a timestamped backup of AGENTS.md, MEMORY.md, TOOLS.md, memory/ directory, and ../openclaw.json to a 'backups' folder.

# [RULE] Safety Check
# Before any self-modification (editing AGENTS.md, BOOTSTRAP.md, or core scripts), ALWAYS create a backup copy first.

# [TASK] AgentHub Message Check
# Every minute: Check for new messages from other agents (e.g. NormaEVA).
# Command: npx @lws803/agenthub messages --unread
# If messages found: Process and reply.
# Note: This runs every minute to ensure near real-time communication.

# [CRON] Daily AI and Tech News - 08:00
# Run daily at 08:00 AM
# Schedule: 0 8 * * *
# Task: Search for the latest AI news and digital/tech news from the past 24 hours. Summarize them into two distinct lists and send them to 卢垚宇.
