# Source Information

## Upstream

- Repository: https://github.com/decebals/claude-code-java.git
- Original path: `.claude/skills/issue-triage/`
- Imported ref: `f81fbd2adb38c5768e57c15e4f380dfc5c2efe1c`
- Imported date: 2026-06-13
- License: MIT

## Compatibility

- Claude Code: compatible
- Codex: not compatible (references Claude Code-specific commands)
- Kimi Code: not compatible (references Claude Code-specific commands)
- Operating systems: Windows and Linux/macOS

## Local changes

- Added YAML frontmatter fields: `license`, `compatibility`, and `metadata` (`source-type: curated-external`, `risk-level: L0`).
- Updated `compatibility` to `Claude Code only.` and `category` to `workflow`.
- Kept original `README.md` and `SKILL.md` content unchanged.
- Placed in `skills/claude-only/` because the content references Claude Code-specific commands (`claude mcp add`, `claude code`, `view .claude/skills/...`).

## Security review

- Executable scripts: none
- Network access: none (but references GitHub MCP server configuration)
- Credential access: none
- Dangerous keywords: none found
- Review status: approved (L0 — pure text instructions)
