# AGENTS.md

> 本文件面向 AI 编程助手。阅读前请假设你对本项目一无所知。以下内容全部基于仓库中的实际文件，不做推测。

## 项目概述

本项目是一个**私有个人 Agent Skill 仓库**，用于集中收藏、整理和维护自己认可的外部 Agent Skills，并支持跨 Agent（Claude Code、Codex、Kimi Code）和跨主机（Windows、Linux/macOS）使用。

核心设计原则：

- 每个 Skill 在仓库中只保留一份真实副本，通过目录链接（Windows Junction / Unix 符号链接）接入各 Agent。
- 不自动追踪上游 `main`，每个外部 Skill 固定到审查过的版本。
- 不自动执行第三方 Skill 中的脚本。
- 不是通用 Skill 商店或包管理器，而是“个人精选集”。

## 仓库结构

```text
.
├── skills/                    # Skill 唯一真实副本
│   ├── shared/                # 可跨 Agent 共享的 Skill（优先放在这里）
│   ├── claude-only/           # 仅 Claude Code 可用的 Skill
│   ├── kimi-only/             # 仅 Kimi Code 可用的 Skill
│   └── codex-only/            # 仅 Codex 可用的 Skill（当前不部署）
├── scripts/
│   ├── skillhub.py            # 核心 Python CLI，无第三方依赖
│   ├── install.ps1            # Windows 安装包装脚本
│   └── install.sh             # Linux/macOS 安装包装脚本
├── docs/
│   ├── IMPORT_CHECKLIST.md    # 外部 Skill 收录检查清单
│   ├── SECURITY_CHECKLIST.md  # 外部 Skill 安全检查清单
│   └── COMPATIBILITY.md       # Skill 兼容性分级说明
├── CATALOG.md                 # Skill 收藏索引（人工维护）
├── README.md                  # 面向人类用户的快速开始
└── .gitignore
```

当前实际包含的 Skill：

- `skills/shared/java-code-review/` —— Java 综合代码审查，风险等级 L0，纯文本指令。

## 技术栈与依赖

- **语言**：Python 3（标准库，目标兼容 Python 3.8+）。
- **无第三方依赖**：`scripts/skillhub.py` 只使用 `argparse`、`json`、`os`、`shutil`、`sys`、`dataclasses`、`pathlib`、`typing` 等标准库。
- **无构建系统**：没有 `pyproject.toml`、`setup.py`、`package.json`、`Cargo.toml`、`Makefile` 等构建配置。
- **无持续集成/自动化测试**：目前未配置 CI，也没有单元测试。所有验证通过 `skillhub.py doctor` 和在各 Agent 中手动调用完成。
- **Shell 包装**：
  - Windows: PowerShell (`scripts/install.ps1`)
  - Linux/macOS: Bash (`scripts/install.sh`)

## 核心架构

```text
外部优秀 Skill
       │
       │ 人工筛选、检查、复制
       ▼
私有 Git 仓库 my-agent-skills
       │
       ├── 保存 Skill 唯一真实副本
       ├── 记录来源和版本 (SOURCE.md)
       └── Git 负责跨主机同步
              │
              ▼
       skillhub.py install 创建目录链接
              │
              ├── ~/.agents/skills   ← Codex / Kimi Code
              ├── ~/.claude/skills   ← Claude Code
              └── ~/.kimi-code/skills ← Kimi Code 专属
```

职责划分：

- **Git 仓库**：管理内容、版本和跨主机同步。
- **Skill Hub（skillhub.py）**：负责本机部署、结构检查和状态管理。
- **各 Agent**：发现并按需加载对应目录中的 Skill。

### 部署目标映射

`scripts/skillhub.py` 中硬编码的 `SCOPE_TARGETS`：

| Scope | 部署到的 Agent 目录 |
|-------|--------------------|
| `shared` | `~/.agents/skills`（Codex / Kimi Code）<br>`~/.claude/skills`（Claude Code） |
| `claude-only` | `~/.claude/skills` |
| `kimi-only` | `~/.kimi-code/skills` |
| `codex-only` | 当前不部署（空列表） |

本地状态文件：`~/.skillhub/state.json`，记录 Skill Hub 创建的所有链接/副本，**不提交到仓库**。

## Skill 文件规范

每个 Skill 目录至少应包含：

```text
skill-name/
├── SKILL.md          # 必须，包含 YAML frontmatter
├── SOURCE.md         # 外部 Skill 必须；本地原创可选
├── references/       # 可选
├── scripts/          # 可选，需人工安全审查
└── assets/           # 可选
```

`SKILL.md` frontmatter 示例：

```markdown
---
name: java-code-review
description: Review Java code for correctness, ...
license: MIT
compatibility: Claude Code, Codex, and Kimi Code.
metadata:
  category: java
  source-type: local-curated
  risk-level: L0
---
```

必填检查项：

- `name` 必须与目录名一致。
- `description` 不能为空，应准确描述触发场景。
- 外部来源的 Skill 建议设置 `source-type: external` / `curated-external`，并必须提供 `SOURCE.md`。

## 常用命令

所有核心命令都通过 `scripts/skillhub.py` 执行：

```bash
# 列出仓库中所有 Skill 及其结构检查状态
python scripts/skillhub.py list

# 以链接方式部署（默认，推荐）
python scripts/skillhub.py install

# 以复制方式部署（兼容模式，无法创建链接时使用）
python scripts/skillhub.py install --mode copy

# 检查 Skill 结构和已部署链接的健康状态
python scripts/skillhub.py doctor

# 查看每个 Skill 在各 Agent 目录中的部署状态
python scripts/skillhub.py status

# 卸载 Skill Hub 管理的所有链接/副本
python scripts/skillhub.py uninstall
```

Windows 一键安装包装：

```powershell
Set-ExecutionPolicy -Scope Process Bypass
.\scripts\install.ps1
```

Linux/macOS 一键安装包装：

```bash
chmod +x scripts/install.sh
./scripts/install.sh
```

## 开发与收录约定

### 兼容性分级

参考 `docs/COMPATIBILITY.md`：

- **A 级**：完全共享。标准 YAML frontmatter、自然语言工作流、不依赖 Agent 专有命令 → 放入 `skills/shared/`。
- **B 级**：内容可共享但部分功能降级 → 改写后放入 `skills/shared/`，无法改写则放入对应 Agent 专属目录。
- **C 级**：Agent 专用 → 放入 `skills/claude-only/`、`skills/kimi-only/` 或 `skills/codex-only/`。

### 风险分级

参考 `docs/SECURITY_CHECKLIST.md`：

| 等级 | 含义 | 处理建议 |
|------|------|----------|
| L0 | 纯文本指令，无脚本 | 可直接收录 |
| L1 | 只读取代码、Git diff、日志 | 检查读取范围后收录 |
| L2 | 运行构建、测试或本地脚本 | 逐个阅读脚本后决定 |
| L3 | 访问网络、密钥、系统配置或删除文件 | 默认不收录，除非完整审计 |

### 收录外部 Skill 的标准流程

1. 临时克隆上游仓库，只复制需要的单个 Skill 目录。
2. 检查格式：目录名与 `name` 一致、`description` 准确、无未说明的绝对路径、无危险脚本。
3. 按兼容性分级放入对应目录。
4. 补充 `SOURCE.md`：上游仓库、原始路径、导入的 commit/tag、导入日期、许可证、本地修改、兼容性声明、安全审查结论。
5. 运行 `python scripts/skillhub.py doctor`。
6. 运行 `python scripts/skillhub.py install` 并在各 Agent 中测试调用。
7. 提交到私有 Git 仓库。

### 代码风格

- `scripts/skillhub.py` 使用 Python 类型注解、`pathlib`、标准库 `argparse` 子命令。
- 所有用户可见输出使用中文或英文状态标签，如 `[OK]`、`[FAIL]`、`[WARN]`、`[PASS]`、`[INFO]`、`[SKIP]`。
- 不引入第三方依赖；如需增强功能，优先考虑标准库实现。

## 测试与验证

- **无自动化单元测试**。
- 验证方式：
  1. `python scripts/skillhub.py doctor` —— 结构检查、重复名检查、链接有效性检查。
  2. `python scripts/skillhub.py status` —— 查看部署状态。
  3. 在对应 Agent 中手动调用：
     - Claude Code: `/java-code-review`
     - Codex: `/skills` 或 `$java-code-review`
     - Kimi Code: `/skill:java-code-review`

## 安全注意事项

- 收录外部 Skill 前必须检查 `scripts/`、`hooks/`、`bin/`、`commands/`、`.mcp.json`、`plugin.json`、`package.json` 等高风险路径。
- 搜索危险关键词：`rm -rf`、`Remove-Item -Recurse`、`curl | bash`、`wget | sh`、`Invoke-Expression`、`~/.ssh`、`.env`、`API_KEY`、`TOKEN`、`sudo`、`上传源码`、`发送网络请求` 等。
- `skillhub.py doctor` 只做关键词和结构检查，**不能替代人工代码审计**。
- **不要在仓库中保存任何密钥、Token、密码、SSH 私钥或服务器敏感配置**。
- 状态文件 `~/.skillhub/state.json` 只保存在本机，不提交到 Git。

## 部署与运维

### 部署模式

- **link（默认）**：
  - Windows 优先创建 Junction（无需管理员权限）；失败则回退到目录符号链接。
  - Linux/macOS 创建符号链接。
  - 优点：一份副本、修改即时生效、`git pull` 后无需重新安装。
- **copy**：将 Skill 目录完整复制到 Agent 目录。用于无法使用链接的环境；缺点是 `git pull` 后需重新部署，且存在多份副本。

### 日常运维流程

- **修改已有 Skill**：直接编辑 `skills/shared/xxx/SKILL.md`，链接模式下 Agent 立即生效，提交并推送即可。
- **同步到另一台主机**：`git pull`；已有 Skill 通常无需重新安装。
- **新增或删除 Skill**：`git pull` 后运行 `python scripts/skillhub.py install`。
- **更新外部 Skill**：不要直接覆盖。应查看上游新版本 → 对比 commit → 人工审查 → 更新本地副本和 `SOURCE.md` → `doctor` → 各 Agent 测试 → Git 提交。

### 跨主机初始化

Windows：

```powershell
git clone <私人仓库地址> "$env:USERPROFILE\my-agent-skills"
cd "$env:USERPROFILE\my-agent-skills"
Set-ExecutionPolicy -Scope Process Bypass
.\scripts\install.ps1
python .\scripts\skillhub.py doctor
```

Linux/macOS：

```bash
git clone <私人仓库地址> ~/my-agent-skills
cd ~/my-agent-skills
chmod +x scripts/install.sh
./scripts/install.sh
python3 scripts/skillhub.py doctor
```

## 给 AI 助手的特别提醒

- 修改 `scripts/skillhub.py` 时，保持无第三方依赖的约束，维持 Python 3.8+ 兼容。
- 新增 Skill 时，优先放入 `skills/shared/`；只有确实依赖某个 Agent 专有特性时，才放入对应 `*-only/` 目录。
- 任何外部 Skill 都必须经过 `docs/SECURITY_CHECKLIST.md` 审查并补充 `SOURCE.md`。
- 不要修改 `.gitignore` 中忽略的本地状态文件逻辑，也不要把 `~/.skillhub/state.json` 提交进仓库。
- 当前项目没有测试框架，修改后请用 `python scripts/skillhub.py doctor` 和 `python scripts/skillhub.py status` 验证。
