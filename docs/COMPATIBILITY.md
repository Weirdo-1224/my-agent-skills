# Skill 兼容性分级

不是所有标有 `SKILL.md` 的项目都能真正跨 Agent 使用。本仓库采用三级分类。

## A 级：完全共享

**特征**：

- 标准 YAML frontmatter。
- 主要内容是自然语言工作流。
- 不依赖某个 Agent 的命令。
- 不依赖专有插件。
- 脚本是可选的。

**存放位置**：

```text
skills/shared/
```

**部署目标**：

- `~/.agents/skills`（Codex / Kimi Code）
- `~/.claude/skills`（Claude Code）

## B 级：内容共享，但部分功能降级

**特征**：

- 核心审查规则可共享。
- 某些动态参数只有一个 Agent 支持。
- 部分脚本需要特定环境。

**处理方式**：

- 保留公共核心。
- 删除或改写专有语法。
- 在 `SOURCE.md` 中记录降级项。

**存放位置**：

经过改写后可放入 `skills/shared/`；无法改写的放入对应 Agent 专属目录。

## C 级：Agent 专用

**特征**：

- Claude 动态命令注入。
- Kimi Flow。
- Codex 插件和 UI 配置。
- 依赖特定内置工具。

**存放位置**：

```text
skills/claude-only/
skills/kimi-only/
skills/codex-only/
```

不要为了“形式上的跨 Agent”，强行让专用 Skill 在所有 Agent 中加载。
