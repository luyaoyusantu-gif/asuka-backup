---
name: self-improvement
description: "Captures learnings, errors, and corrections to enable continuous improvement. Use when: (1) A command or operation fails unexpectedly, (2) User corrects Claude ('No, that's wrong...', 'Actually...'), (3) User requests a capability that doesn't exist, (4) An external API or tool fails, (5) Claude realizes its knowledge is outdated or incorrect, (6) A better approach is discovered for a recurring task. Also review learnings before major tasks."
---

# Self-Improvement Skill

Log learnings and errors to markdown files for continuous improvement. Coding agents can later process these into fixes, and important learnings get promoted to project memory.

## Quick Reference

| Situation | Action |
|-----------|--------|
| Command/operation fails | Log to `.learnings/ERRORS.md` |
| User corrects you | Log to `.learnings/LEARNINGS.md` with category `correction` |
| User wants missing feature | Log to `.learnings/FEATURE_REQUESTS.md` |
| API/external tool fails | Log to `.learnings/ERRORS.md` with integration details |
| Knowledge was outdated | Log to `.learnings/LEARNINGS.md` with category `knowledge_gap` |
| Found better approach | Log to `.learnings/LEARNINGS.md` with category `best_practice` |
| Similar to existing entry | Link with `**See Also**`, consider priority bump |
| Broadly applicable learning | Promote to `CLAUDE.md`, `AGENTS.md`, and/or `.github/copilot-instructions.md` |
| Workflow improvements | Promote to `AGENTS.md` (OpenClaw workspace) |
| Tool gotchas | Promote to `TOOLS.md` (OpenClaw workspace) |
| Behavioral patterns | Promote to `SOUL.md` (OpenClaw workspace) |

## Installation

**Via ClawHub:**
```bash
clawhub install self-improving-agent
```

**Manual:**
```bash
git clone https://github.com/peterskoett/self-improving-agent.git ~/.openclaw/skills/self-improving-agent
```

## Learning Types

### 1. LEARNINGS.md
- Corrections from users
- Knowledge gaps discovered
- Best practices found

### 2. ERRORS.md
- Command failures
- Exceptions
- Unexpected behavior

### 3. FEATURE_REQUESTS.md
- User-requested capabilities
- Missing features

## ID Format
- `LRN-YYYYMMDD-XXX` - Learning
- `ERR-YYYYMMDD-XXX` - Error
- `FEAT-YYYYMMDD-XXX` - Feature Request

## Promotion

When learnings are broadly applicable, promote to:
| Target | What Goes There |
|--------|-----------------|
| `SOUL.md` | Behavioral guidelines, personality |
| `AGENTS.md` | Agent workflows, delegation patterns |
| `TOOLS.md` | Tool capabilities, integration gotchas |
| `CLAUDE.md` | Project facts, conventions |

## Periodic Review

Review `.learnings/` before:
- New major tasks
- After completing features
- Weekly during active development

## Setup Commands

```bash
# Create learning directory
mkdir -p ~/.openclaw/workspace/.learnings

# Create log files
touch ~/.openclaw/workspace/.learnings/LEARNINGS.md
touch ~/.openclaw/workspace/.learnings/ERRORS.md
touch ~/.openclaw/workspace/.learnings/FEATURE_REQUESTS.md
```
