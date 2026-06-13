# 外部 Skill 收录检查清单

在将外部 Skill 纳入本仓库之前，请按以下步骤人工审查。

## 第一步：临时克隆上游仓库

```bash
git clone <外部仓库地址> temp-skill-repo
cd temp-skill-repo
```

## 第二步：只选择需要的 Skill

- 不要整体复制包含几十个 Skill 的仓库。
- 仅复制需要的单个 Skill 目录。

```bash
cp -r temp-skill-repo/path/to/skill ../my-agent-skills/skills/shared/skill-name
```

## 第三步：检查格式

- [ ] 目录名与 `SKILL.md` frontmatter 中的 `name` 一致。
- [ ] `SKILL.md` 存在且包含标准 YAML frontmatter。
- [ ] `description` 准确描述触发场景。
- [ ] 内容中没有未经说明的绝对路径。
- [ ] 没有未经说明的环境依赖。
- [ ] 没有危险脚本或命令。

## 第四步：判断兼容性

根据兼容性分级，放入对应目录：

- [ ] `skills/shared/`：A 级，可跨 Agent 共享。
- [ ] `skills/claude-only/`：C 级，依赖 Claude 专有特性。
- [ ] `skills/kimi-only/`：C 级，依赖 Kimi 专有特性。
- [ ] `skills/codex-only/`：C 级，依赖 Codex 专有特性（暂不部署）。

## 第五步：补充 SOURCE.md

记录：

- [ ] 上游仓库地址。
- [ ] 原始路径。
- [ ] 导入的具体 commit hash / tag / release version。
- [ ] 导入日期。
- [ ] 许可证。
- [ ] 本地修改内容。
- [ ] 兼容性声明。
- [ ] 安全审查结论。

## 第六步：运行检查

```bash
python scripts/skillhub.py doctor
```

## 第七步：部署并测试

```bash
python scripts/skillhub.py install
```

在各 Agent 中测试调用：

- Claude Code：`/java-code-review`
- Codex：`/skills` 或 `$java-code-review`
- Kimi Code：`/skill:java-code-review`

## 第八步：提交到私有仓库

```bash
git add .
git commit -m "add <skill-name> skill"
git push
```
