# HEARTBEAT.md

# [CRON] Daily Backup - 00:00
# Run daily at midnight to backup workspace data
# Schedule: 0 0 * * *
# Task: 
#   1. Local backup: Create timestamped backup to E:\openclaw_backups
#   2. GitHub backup: Push to luyaoyusantu-gif/asuka-backup repository
# Files to backup: AGENTS.md, MEMORY.md, TOOLS.md, memory/, skills/, openclaw.json

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
