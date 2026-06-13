# 个人精选 Agent Skill 跨 Agent、跨主机管理方案

## 1. 建设目标

建立一个私有 Git 仓库，用于收藏、整理和维护自己认可的外部 Agent Skills，实现：

1. Skill 只保存一份，不在 Claude Code、Codex、Kimi Code 目录中重复维护。
2. Windows 本机、Linux 服务器和后续新设备使用同一套 Skill。
3. 外部 Skill 固定到自己审查过的版本，不自动追踪上游 `main`。
4. Claude Code、Codex、Kimi Code 能尽可能共享同一套标准 Skill。
5. 对来源、版本、许可证、兼容性和安全风险进行记录。
6. 新设备只需执行“克隆仓库 + 一次安装”即可恢复环境。

本方案不以开发完整 Skill 包管理器为目标，也不自动从互联网执行第三方 Skill 中的脚本。

------

## 2. 核心架构

```text
外部优秀 Skill
       │
       │ 人工筛选、检查、复制
       ▼
私有 Git 仓库 my-agent-skills
       │
       ├── 保存 Skill 唯一真实副本
       ├── 记录来源和版本
       └── Git 负责跨主机同步
              │
              ▼
       本机安装脚本创建目录链接
              │
              ├── ~/.agents/skills
              │      ├── Codex
              │      └── Kimi Code
              │
              └── ~/.claude/skills
                     └── Claude Code
```

职责划分：

```text
Git 仓库：管理内容、版本和跨主机同步
安装脚本：把仓库中的 Skill 接入各 Agent
Agent：发现并按需加载 Skill
```

------

## 3. 仓库目录设计

仓库建议命名：

```text
my-agent-skills
```

完整目录：

```text
my-agent-skills/
├── skills/
│   ├── shared/
│   │   ├── java-code-review/
│   │   │   ├── SKILL.md
│   │   │   ├── SOURCE.md
│   │   │   ├── references/
│   │   │   ├── scripts/
│   │   │   └── assets/
│   │   │
│   │   ├── springboot-code-review/
│   │   │   ├── SKILL.md
│   │   │   └── SOURCE.md
│   │   │
│   │   └── api-contract-review/
│   │       ├── SKILL.md
│   │       └── SOURCE.md
│   │
│   ├── claude-only/
│   ├── kimi-only/
│   └── codex-only/
│
├── scripts/
│   ├── skillhub.py
│   ├── install.ps1
│   └── install.sh
│
├── docs/
│   ├── IMPORT_CHECKLIST.md
│   ├── SECURITY_CHECKLIST.md
│   └── COMPATIBILITY.md
│
├── CATALOG.md
├── README.md
└── .gitignore
```

### 3.1 `skills/shared`

放置符合 Agent Skills 公共格式、能够被多个 Agent 使用的 Skill。

优先收藏这类 Skill。

### 3.2 `skills/claude-only`

放置依赖 Claude Code 专有能力的 Skill，例如：

- 动态 Shell 上下文注入；
- Claude 专有 frontmatter；
- Claude 插件或子 Agent；
- 只适用于 `/skill-name` 的特殊流程。

### 3.3 `skills/kimi-only`

放置依赖 Kimi Code 特性的 Skill，例如：

- `type: flow`；
- Kimi 参数占位符；
- Kimi 专有流程语法；
- Kimi 插件依赖。

### 3.4 `skills/codex-only`

保存依赖 Codex 特性的 Skill，例如：

- `agents/openai.yaml`；
- Codex 插件依赖；
- Codex 特有工具配置；
- Codex 专有工作流。

第一版安装器只需要优先处理 `shared`、`claude-only` 和 `kimi-only`。Codex 专有 Skill 可以先保留归档，确认当前 Codex 版本的独立部署方式后再启用。

------

## 4. Skill 文件标准

共享 Skill 至少应采用以下结构：

```text
skill-name/
├── SKILL.md
├── SOURCE.md
├── references/       可选
├── scripts/          可选
└── assets/           可选
```

共享 `SKILL.md` 的 frontmatter 尽量只使用开放标准字段：

```markdown
---
name: springboot-code-review
description: Review Java Spring Boot code for correctness, transaction boundaries, API design, security, MyBatis usage, testing, and maintainability. Use when reviewing Spring Boot projects, Git diffs, pull requests, or architecture.
license: MIT
compatibility: Claude Code, Codex, and Kimi Code. Requires access to the current Git repository.
metadata:
  category: java
  source-type: curated-external
---

# Spring Boot Code Review

Follow the review process below.
```

共享 Skill 中不建议依赖：

```text
Claude 专属命令插值
Kimi Flow Skill 语法
Codex 专属 UI 或插件文件
某个 Agent 独有的工具名称
未经声明的本机绝对路径
```

------

## 5. 来源记录规范

每个外部 Skill 旁边增加：

```text
SOURCE.md
```

模板：

```markdown
# Source Information

## Upstream

- Repository: https://github.com/example/example-skills
- Original path: skills/springboot-code-review
- Imported ref: 8f40c1a26fd7
- Imported date: 2026-06-13
- License: MIT

## Compatibility

- Claude Code: verified
- Codex: verified
- Kimi Code: verified
- Operating systems: Windows and Linux

## Local changes

- Removed JPA-only review rules.
- Added MyBatis-Plus review rules.
- Replaced agent-specific invocation syntax.
- Standardized severity levels.

## Security review

- Executable scripts: none
- Network access: none
- Credential access: none
- Review status: approved
```

不要只记录仓库的 `main` 分支，应记录具体：

```text
commit hash
tag
release version
```

这样将来上游发生变化时，你仍然知道自己收藏的是哪个版本。

------

## 6. Skill 兼容性分级

不是所有标有 `SKILL.md` 的项目都能真正跨 Agent 使用，应分为三级。

### A 级：完全共享

特征：

- 标准 YAML frontmatter；
- 主要内容是自然语言工作流；
- 不依赖某个 Agent 的命令；
- 不依赖专有插件；
- 脚本是可选的。

存放到：

```text
skills/shared/
```

### B 级：内容共享，但部分功能降级

例如：

- 核心审查规则可共享；
- 某些动态参数只有一个 Agent 支持；
- 部分脚本需要特定环境。

处理方式：

- 保留公共核心；
- 删除或改写专有语法；
- 在 `SOURCE.md` 中记录降级项。

### C 级：Agent 专用

例如：

- Claude 动态命令注入；
- Kimi Flow；
- Codex 插件和 UI 配置；
- 依赖特定内置工具。

存放到对应的：

```text
skills/claude-only/
skills/kimi-only/
skills/codex-only/
```

不要为了“形式上的跨 Agent”，强行让专用 Skill 在所有 Agent 中加载。

------

## 7. 本机部署目录

### Windows

仓库建议放在：

```text
C:\Users\<用户名>\my-agent-skills
```

Agent 入口：

```text
C:\Users\<用户名>\.agents\skills
C:\Users\<用户名>\.claude\skills
C:\Users\<用户名>\.kimi-code\skills
```

### Linux

仓库建议放在：

```text
~/my-agent-skills
```

Agent 入口：

```text
~/.agents/skills
~/.claude/skills
~/.kimi-code/skills
```

部署关系：

```text
skills/shared/*
    ├── ~/.agents/skills/*
    └── ~/.claude/skills/*

skills/claude-only/*
    └── ~/.claude/skills/*

skills/kimi-only/*
    └── ~/.kimi-code/skills/*
```

`shared` 通过 `~/.agents/skills` 同时提供给 Codex 和 Kimi Code，通过 `~/.claude/skills` 提供给 Claude Code。

------

## 8. 安装脚本的职责

安装脚本不负责下载外部 Skill，只负责本机部署。

它需要完成：

1. 检查仓库结构。
2. 检查每个目录是否包含 `SKILL.md`。
3. 检查 Skill 名称是否重复。
4. 创建 Agent 所需目录。
5. 创建 Junction 或符号链接。
6. 记录本次由 Skill Hub 管理的链接。
7. 不删除用户手动安装的其他 Skill。
8. 提供链接失败时的复制模式。
9. 输出部署结果和错误信息。

建议提供两种模式：

```text
link：默认模式，只保存一份 Skill
copy：兼容模式，将 Skill 复制到 Agent 目录
```

### Link 模式

优点：

- Skill 只有一份；
- 修改仓库后立即生效；
- `git pull` 后不需要重复复制；
- 不会产生版本漂移。

### Copy 模式

用于某个 Agent 或系统环境无法识别目录链接的情况。

缺点：

- `git pull` 后必须重新部署；
- 存在多个副本；
- 需要安装器负责覆盖更新。

------

## 9. 推荐实现：单一 Python CLI

为避免分别维护复杂的 PowerShell 和 Bash 逻辑，核心功能使用一个无第三方依赖的 Python 脚本：

```text
scripts/skillhub.py
```

PowerShell 和 Bash 只作为启动包装。

CLI 设计：

```bash
python scripts/skillhub.py list
python scripts/skillhub.py install
python scripts/skillhub.py install --mode copy
python scripts/skillhub.py doctor
python scripts/skillhub.py status
python scripts/skillhub.py uninstall
```

### 9.1 `list`

扫描仓库并显示：

```text
NAME                       SCOPE          STATUS
java-code-review           shared         valid
springboot-code-review     shared         valid
claude-debug-workflow      claude-only    valid
kimi-review-flow           kimi-only      valid
```

### 9.2 `install`

默认创建链接：

```bash
python scripts/skillhub.py install --mode link
```

Windows：

- 优先创建 Junction；
- Junction 创建失败后给出清晰错误；
- 用户可改用 `--mode copy`。

Linux/macOS：

- 创建符号链接。

### 9.3 `doctor`

检查：

- `SKILL.md` 是否存在；
- frontmatter 是否存在；
- `name` 和目录名是否一致；
- `description` 是否为空；
- 是否存在重名；
- 链接是否失效；
- 来源文件是否缺失；
- 是否存在高风险脚本；
- Agent 目标目录是否可写。

输出：

```text
[PASS] java-code-review
[WARN] security-audit contains scripts/
[FAIL] api-review name does not match directory
```

### 9.4 `status`

显示每个 Skill 的部署状态：

```text
java-code-review
  Source:  C:\Users\...\my-agent-skills\skills\shared\java-code-review
  Claude:  linked
  Codex:   linked
  Kimi:    linked
```

### 9.5 `uninstall`

只移除 Skill Hub 创建的链接或副本，不碰用户手动安装的 Skill。

状态记录建议保存在：

```text
~/.skillhub/state.json
```

示例：

```json
{
  "managed": [
    {
      "name": "java-code-review",
      "target": "C:/Users/user/.agents/skills/java-code-review",
      "mode": "junction"
    },
    {
      "name": "java-code-review",
      "target": "C:/Users/user/.claude/skills/java-code-review",
      "mode": "junction"
    }
  ]
}
```

------

## 10. PowerShell 和 Bash 包装脚本

### Windows：`scripts/install.ps1`

职责仅为找到 Python 并调用 CLI：

```powershell
$ErrorActionPreference = "Stop"

$RepoRoot = Split-Path -Parent $PSScriptRoot
$Script = Join-Path $RepoRoot "scripts\skillhub.py"

if (Get-Command py -ErrorAction SilentlyContinue) {
    py -3 $Script install @args
}
elseif (Get-Command python -ErrorAction SilentlyContinue) {
    python $Script install @args
}
else {
    throw "Python 3 was not found."
}
```

运行：

```powershell
Set-ExecutionPolicy -Scope Process Bypass
.\scripts\install.ps1
```

复制模式：

```powershell
.\scripts\install.ps1 --mode copy
```

### Linux：`scripts/install.sh`

```bash
#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

python3 "$REPO_ROOT/scripts/skillhub.py" install "$@"
```

运行：

```bash
chmod +x scripts/install.sh
./scripts/install.sh
```

------

## 11. 外部 Skill 收录流程

第一版不实现“一键从 GitHub 自动安装”，而采用安全、可控的人工收录。

### 第一步：临时克隆上游仓库

```bash
git clone <外部仓库地址> temp-skill-repo
```

### 第二步：只选择需要的 Skill

不要把包含几十个 Skill 的仓库整体塞进自己的仓库。

复制：

```text
temp-skill-repo/path/to/skill
```

到：

```text
my-agent-skills/skills/shared/skill-name
```

### 第三步：检查格式

确认：

```text
skill-name/
└── SKILL.md
```

并检查：

```text
目录名和 name 一致
description 能准确描述触发场景
没有绝对路径
没有未经说明的环境依赖
没有危险脚本
```

### 第四步：判断兼容性

决定放入：

```text
shared
claude-only
kimi-only
codex-only
```

### 第五步：补充 `SOURCE.md`

记录仓库、路径、commit、许可证、修改内容和安全结论。

### 第六步：运行检查

```bash
python scripts/skillhub.py doctor
```

### 第七步：部署并测试

```bash
python scripts/skillhub.py install
```

### 第八步：提交到私人仓库

```bash
git add .
git commit -m "add springboot code review skill"
git push
```

------

## 12. 外部 Skill 安全检查

Agent Skill 不一定只是提示词，还可能携带脚本。收录前至少检查以下内容。

### 12.1 高风险路径

```text
scripts/
hooks/
bin/
commands/
.mcp.json
plugin.json
package.json
```

### 12.2 高风险行为

搜索：

```text
rm -rf
Remove-Item -Recurse
curl | bash
wget | sh
Invoke-Expression
~/.ssh
.env
API_KEY
TOKEN
git config --global
sudo
上传源码
发送网络请求
```

### 12.3 风险分级

```text
L0：纯文本指令，无脚本
L1：只读取代码、Git diff、日志
L2：运行构建、测试或本地脚本
L3：访问网络、密钥、系统配置或删除文件
```

建议：

- L0：可直接收录；
- L1：检查读取范围后收录；
- L2：逐个阅读脚本；
- L3：默认不收录，除非完整审计。

Skill Hub 的 `doctor` 只能做关键词和结构检查，不能替代人工代码审计。

------

## 13. 许可证处理

复制外部 Skill 前检查其许可证。

需要保留：

- 原仓库地址；
- 原始许可证；
- 作者版权信息；
- 许可证要求的 NOTICE；
- 本地修改说明。

没有明确许可证的仓库，不应默认认为可以自由复制和再分发。

私人仓库中也建议保留完整来源记录。

------

## 14. `CATALOG.md` 设计

`CATALOG.md` 用作个人 Skill 收藏索引。

示例：

```markdown
# Personal Skill Catalog

## Java / Spring Boot

| Skill | 用途 | 兼容性 | 风险 | 来源版本 |
|---|---|---|---|---|
| java-code-review | Java 综合审查 | Claude/Codex/Kimi | L0 | 8f40c1a |
| springboot-code-review | Spring Boot 专项审查 | Claude/Codex/Kimi | L0 | 本地调整版 |
| api-contract-review | REST API 契约审查 | Claude/Codex/Kimi | L0 | v1.2.0 |
| maven-dependency-audit | Maven 依赖检查 | Claude/Codex/Kimi | L1 | c8a3412 |

## Agent Development

| Skill | 用途 | 兼容性 | 风险 | 来源版本 |
|---|---|---|---|---|
| prompt-review | Prompt 质量审查 | Claude/Codex/Kimi | L0 | 12ab9de |
| mcp-tool-design | MCP 工具设计 | Claude/Codex | L0 | v2.0.0 |
```

`CATALOG.md` 是面向人阅读的索引，真正的 Skill 仍位于 `skills/`。

------

## 15. Git 仓库管理策略

推荐使用私有 GitHub、Gitee 或 GitLab 仓库。

提交：

```text
skills/
scripts/
docs/
CATALOG.md
README.md
```

不提交：

```text
本机状态文件
临时克隆目录
Python 缓存
IDE 配置
密钥
```

`.gitignore`：

```gitignore
__pycache__/
*.pyc
.temp/
tmp/
.local/
.vscode/
.idea/
```

不要在仓库中保存：

```text
API Key
Token
账号密码
SSH 私钥
服务器地址和敏感配置
```

------

## 16. 跨主机初始化

### Windows 新电脑

```powershell
git clone <私人仓库地址> "$env:USERPROFILE\my-agent-skills"

cd "$env:USERPROFILE\my-agent-skills"

Set-ExecutionPolicy -Scope Process Bypass

.\scripts\install.ps1

python .\scripts\skillhub.py doctor
```

### Linux 服务器

```bash
git clone <私人仓库地址> ~/my-agent-skills

cd ~/my-agent-skills

chmod +x scripts/install.sh

./scripts/install.sh

python3 scripts/skillhub.py doctor
```

------

## 17. 日常更新流程

### 修改已有 Skill

```bash
cd ~/my-agent-skills
编辑 skills/shared/xxx/SKILL.md
git add .
git commit -m "improve xxx skill"
git push
```

使用链接模式时，各 Agent 立即读取同一份文件，无需重新安装。

### 另一台主机同步

```bash
cd ~/my-agent-skills
git pull
```

对于已有 Skill，通常无需重新运行安装。

### 新增或删除 Skill

```bash
git pull
python scripts/skillhub.py install
```

重新运行安装器，让它创建新链接并清理已经由 Skill Hub 管理的失效链接。

### 更新外部 Skill

不要直接覆盖。

推荐流程：

```text
查看上游新版本
→ 对比旧 commit 和新 commit
→ 人工审查变更
→ 更新本地副本
→ 更新 SOURCE.md
→ doctor 检查
→ 分别在三个 Agent 中测试
→ Git 提交
```

------

## 18. Agent 中的验证方法

### Claude Code

启动 Claude Code 后检查：

```text
/skill-name
```

例如：

```text
/java-code-review
```

### Codex

查看可用 Skills：

```text
/skills
```

或显式引用：

```text
$java-code-review
```

### Kimi Code

显式调用：

```text
/skill:java-code-review
```

还需要测试隐式触发，例如：

```text
请审查当前 Spring Boot 项目的 Git 变更。
```

观察 Agent 是否根据 `description` 自动加载相关 Skill。

------

## 19. 验收标准

方案完成后应满足：

### 仓库层

- 每个 Skill 都有 `SKILL.md`；
- 每个外部 Skill 都有 `SOURCE.md`；
- Skill 来源和 commit 可追踪；
- Skill 不依赖未声明的环境；
- Git 仓库不包含敏感信息。

### 部署层

- `shared` Skill 能部署到 `.agents/skills`；
- `shared` Skill 能部署到 `.claude/skills`；
- Claude 专属 Skill 只进入 Claude 目录；
- Kimi 专属 Skill 只进入 Kimi 目录；
- 安装器不会删除非 Skill Hub 管理的文件；
- `uninstall` 只清理自身创建的内容。

### 使用层

- Claude Code 能显式调用共享 Skill；
- Codex 能在 Skills 列表中发现共享 Skill；
- Kimi Code 能显式调用共享 Skill；
- 修改仓库中的 `SKILL.md` 后，链接模式下各 Agent 能读取新内容；
- 新主机通过 clone + install 能恢复相同 Skill 集合。

------

## 20. 第一阶段实施范围

第一版只实现以下内容：

```text
1. 私有 Git 仓库
2. shared / claude-only / kimi-only 分类
3. SOURCE.md 来源记录
4. CATALOG.md 收藏索引
5. skillhub.py 的 list、install、doctor、status、uninstall
6. Windows Junction
7. Linux 符号链接
8. Copy fallback
```

第一版暂不实现：

```text
自动搜索 GitHub Skill
自动跟踪上游 main
自动执行第三方脚本
在线 Skill 市场
复杂版本解析
远程 registry
Web 管理界面
自动改写不兼容 Skill
```

------

## 21. 推荐的首批 Skill 分类

结合 Java 后端和 Agent 开发方向，第一批控制在 8～12 个。

### Java / Spring Boot

```text
java-code-review
springboot-code-review
api-contract-review
security-audit
maven-dependency-audit
test-quality-review
architecture-review
```

### Agent 开发

```text
agent-architecture-review
prompt-review
mcp-tool-design
context-engineering-review
```

先保证每个 Skill 都确实会使用，不建议一开始收藏几十个同质化代码审查 Skill。

------

## 22. 最终结论

该方案采用：

```text
精选外部 Skill 的稳定快照
+ 私有 Git 仓库
+ 开放 SKILL.md 格式
+ shared 与 Agent 专属分类
+ Junction / Symlink 单一真实副本
+ Python 跨平台安装器
+ SOURCE.md 来源审计
+ doctor 安全和结构检查
```

它解决了四个核心问题：

```text
跨 Agent：共享 Skill 同时供 Claude、Codex、Kimi 使用
跨主机：Git 在 Windows 和 Linux 之间同步
版本稳定：不自动追踪外部 main
维护简单：Skill 只保留一份，安装脚本只负责创建入口
```

整个系统定位为“个人精选 Skill 仓库”，而不是通用 Skill 商店或包管理器。