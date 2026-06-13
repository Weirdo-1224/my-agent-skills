---
name: java-code-review
description: Review Java code for correctness, concurrency, exception handling, logging, resource management, testing, and maintainability. Use when reviewing Java projects, Git diffs, pull requests, or individual files.
license: MIT
compatibility: Claude Code, Codex, and Kimi Code. Requires access to the current project files or Git repository.
metadata:
  category: java
  source-type: local-curated
  risk-level: L0
---

# Java Code Review

Follow the review process below when asked to review Java code, diffs, or pull requests.

## 1. Preparation

- Identify the review scope: single file, package, module, or full PR.
- Determine the Java version and framework constraints.
- Check the test coverage of changed files if tests are present.

## 2. Correctness

- Verify null checks and edge-case handling.
- Check loop boundaries, recursion termination, and arithmetic overflow risks.
- Validate equals/hashCode contracts, compareTo consistency, and enum usage.
- Look for resource leaks: unclosed streams, connections, or file handles.

## 3. Concurrency and Threading

- Identify shared mutable state and missing synchronization.
- Check for correct use of `volatile`, `synchronized`, `Lock`, and atomic classes.
- Warn about potential deadlocks, race conditions, and thread-local misuse.
- Verify executor service lifecycle and shutdown handling.

## 4. Exception Handling

- Ensure exceptions are caught at the right level.
- Avoid swallowing exceptions with empty catch blocks.
- Prefer specific exceptions over broad `Exception` catches.
- Confirm error messages are actionable and logged appropriately.

## 5. Logging and Observability

- Check that meaningful context is included in log messages.
- Avoid logging sensitive data such as passwords, tokens, or PII.
- Verify log levels are appropriate (DEBUG, INFO, WARN, ERROR).

## 6. Testing

- Check that unit tests cover the changed behavior.
- Look for missing edge-case, negative-case, and concurrency tests.
- Verify test names clearly describe intent.
- Flag tests that depend on external state or ordering.

## 7. Maintainability

- Evaluate method length, class cohesion, and naming clarity.
- Check for duplicated code and opportunities for abstraction.
- Verify comments explain why, not what.
- Confirm constants and configuration are not hard-coded.

## 8. Security

- Review input validation and sanitization.
- Check for SQL injection, command injection, and unsafe deserialization.
- Verify cryptographic APIs are used correctly.
- Flag usage of `Runtime.exec`, `ProcessBuilder`, or reflection without justification.

## 9. Output Format

For each issue found, provide:

- **Location**: file and line range.
- **Severity**: critical / major / minor / suggestion.
- **Category**: correctness / concurrency / exception / logging / testing / maintainability / security.
- **Description**: what the problem is and why it matters.
- **Recommendation**: concrete fix or refactoring.

End the review with a brief summary of overall risk and the most important fixes to prioritize.
