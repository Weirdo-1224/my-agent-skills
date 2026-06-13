# 外部 Skill 安全检查清单

Agent Skill 不只是提示词，还可能携带脚本。收录前必须进行安全检查。

## 高风险路径

以下目录或文件需要重点审查：

```text
scripts/
hooks/
bin/
commands/
.mcp.json
plugin.json
package.json
```

## 高风险行为

搜索以下关键词或模式：

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

## 风险分级

| 等级 | 描述 | 处理建议 |
|---|---|---|
| L0 | 纯文本指令，无脚本 | 可直接收录 |
| L1 | 只读取代码、Git diff、日志 | 检查读取范围后收录 |
| L2 | 运行构建、测试或本地脚本 | 逐个阅读脚本后决定 |
| L3 | 访问网络、密钥、系统配置或删除文件 | 默认不收录，除非完整审计 |

## 审查记录

每个 `SOURCE.md` 必须包含以下结论：

```markdown
## Security review

- Executable scripts: none
- Network access: none
- Credential access: none
- Review status: approved
```

## 免责声明

`skillhub.py doctor` 只能做关键词和结构检查，不能替代人工代码审计。
