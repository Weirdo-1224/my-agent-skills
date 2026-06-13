# Personal Skill Catalog

本目录是个人 Agent Skill 收藏的索引。真正的 Skill 文件位于 `skills/` 目录下。

## Java / Spring Boot

| Skill | 用途 | 兼容性 | 风险 | 来源版本 |
|---|---|---|---|---|
| api-contract-review | REST API 契约审查 | Claude/Codex/Kimi | L0 | decebals/claude-code-java@f81fbd2 |
| architecture-review | Java 项目架构宏观分析 | Claude/Codex/Kimi | L0 | decebals/claude-code-java@f81fbd2 |
| changelog-generator | 根据 Git 提交生成 changelog | Claude/Codex/Kimi | L0 | decebals/claude-code-java@f81fbd2 |
| clean-code | Clean Code 原则与重构建议 | Claude/Codex/Kimi | L0 | decebals/claude-code-java@f81fbd2 |
| concurrency-review | Java 并发与线程安全审查 | Claude/Codex/Kimi | L0 | decebals/claude-code-java@f81fbd2 |
| design-patterns | 常用设计模式 Java 示例 | Claude/Codex/Kimi | L0 | decebals/claude-code-java@f81fbd2 |
| git-commit | 生成约定式提交信息 | Claude/Codex/Kimi | L0 | decebals/claude-code-java@f81fbd2 |
| issue-triage | GitHub Issue 分类与优先级标注 | Claude-only | L0 | decebals/claude-code-java@f81fbd2 |
| java-code-review | Java 综合代码审查 | Claude/Codex/Kimi | L0 | decebals/claude-code-java@f81fbd2 |
| java-migration | Java 大版本升级指南 | Claude/Codex/Kimi | L0 | decebals/claude-code-java@f81fbd2 |
| jpa-patterns | JPA/Hibernate 模式与常见陷阱 | Claude/Codex/Kimi | L0 | decebals/claude-code-java@f81fbd2 |
| logging-patterns | Java 日志最佳实践 | Claude/Codex/Kimi | L0 | decebals/claude-code-java@f81fbd2 |
| maven-dependency-audit | Maven 依赖审计 | Claude/Codex/Kimi | L0 | decebals/claude-code-java@f81fbd2 |
| performance-smell-detection | Java 代码级性能异味检测 | Claude/Codex/Kimi | L0 | decebals/claude-code-java@f81fbd2 |
| security-audit | Java 安全审查清单 | Claude/Codex/Kimi | L0 | decebals/claude-code-java@f81fbd2 |
| solid-principles | SOLID 原则检查 | Claude/Codex/Kimi | L0 | decebals/claude-code-java@f81fbd2 |
| spring-boot-patterns | Spring Boot 最佳实践 | Claude/Codex/Kimi | L0 | decebals/claude-code-java@f81fbd2 |
| test-quality | JUnit 5 / AssertJ 测试质量 | Claude/Codex/Kimi | L0 | decebals/claude-code-java@f81fbd2 |

## 说明

- **兼容性**：Claude Code / Codex / Kimi Code。
- **风险等级**：L0 表示纯文本指令，无脚本；L1 表示只读取代码或日志；L2 表示运行本地脚本；L3 表示访问网络、密钥或删除文件。
- **来源版本**：记录上游 commit/tag 或 local-curated。
