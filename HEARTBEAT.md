# HEARTBEAT.md

# [CRON] Daily Backup - 00:00
# Run daily at midnight to backup workspace data
# Schedule: 0 0 * * *
# Task: Create a timestamped backup of AGENTS.md, MEMORY.md, TOOLS.md, memory/ directory, and ../openclaw.json to a 'backups' folder.

# [RULE] Safety Check
# Before any self-modification (editing AGENTS.md, BOOTSTRAP.md, or core scripts), ALWAYS create a backup copy first.

# [TASK] AgentHub Message Check
# Every heartbeat (~30m): Check for new messages from other agents (e.g. NormaEVA).
# Command: npx @lws803/agenthub messages --unread
# If messages found: Process and reply.
