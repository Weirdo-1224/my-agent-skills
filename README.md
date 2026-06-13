# 个人精选 Agent Skill 仓库

本仓库用于集中收藏、整理和维护个人认可的外部 Agent Skills，支持跨 Agent（Claude Code、Codex、Kimi Code）和跨主机（Windows、Linux）使用。

## 设计文档

详细方案见：[`个人精选 Agent Skill 跨 Agent、跨主机管理方案.md`](./个人精选%20Agent%20Skill%20跨%20Agent、跨主机管理方案.md)

## 仓库结构

```text
.
├── skills/
│   ├── shared/        # 可跨 Agent 共享的 Skill
│   ├── claude-only/   # Claude Code 专用 Skill
│   ├── kimi-only/     # Kimi Code 专用 Skill
│   └── codex-only/    # Codex 专用 Skill（暂不部署）
├── scripts/
│   ├── skillhub.py    # 核心 Python CLI
│   ├── install.ps1    # Windows 安装包装脚本
│   └── install.sh     # Linux/macOS 安装包装脚本
├── docs/
│   ├── IMPORT_CHECKLIST.md
│   ├── SECURITY_CHECKLIST.md
│   └── COMPATIBILITY.md
├── CATALOG.md         # Skill 收藏索引
├── README.md
└── .gitignore
```

## 快速开始

### Windows

```powershell
git clone <私人仓库地址> "$env:USERPROFILE\my-agent-skills"
cd "$env:USERPROFILE\my-agent-skills"

Set-ExecutionPolicy -Scope Process Bypass
.\scripts\install.ps1

python .\scripts\skillhub.py doctor
```

### Linux / macOS

```bash
git clone <私人仓库地址> ~/my-agent-skills
cd ~/my-agent-skills

chmod +x scripts/install.sh
./scripts/install.sh

python3 scripts/skillhub.py doctor
```

## 常用命令

```bash
# 列出所有 Skill
python scripts/skillhub.py list

# 默认以链接方式部署（推荐）
python scripts/skillhub.py install

# 以复制方式部署（兼容模式）
python scripts/skillhub.py install --mode copy

# 检查 Skill 结构和部署健康
python scripts/skillhub.py doctor

# 查看部署状态
python scripts/skillhub.py status

# 卸载 Skill Hub 管理的所有链接/副本
python scripts/skillhub.py uninstall
```

## 添加新 Skill

参见 [`docs/IMPORT_CHECKLIST.md`](./docs/IMPORT_CHECKLIST.md)。

## 注意事项

- Skill 只保留一份真实副本，通过 Junction / 符号链接接入各 Agent。
- 不自动追踪上游 `main`，每个外部 Skill 固定到审查过的版本。
- 不自动执行第三方 Skill 中的脚本。
- 本方案定位为个人精选仓库，不是通用 Skill 商店或包管理器。
