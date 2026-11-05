# Company Knowledge to Skill（公司知识转技能）

[English](README.md) | 简体中文

一个通用、可复用的 Skill：从多个 AI 或人工输入中采集某个组织专属的知识，对齐差异、实施隐私控制，生成下游 Skill，并对结果进行测试验证。

## 包含内容

- `SKILL.md` — 入口文件与阶段路由
- `references/collection-prompts.md` — 独立采集者提示词与检查点
- `references/knowledge-schema.yaml` — 标准知识记录结构（schema）
- `references/reconciliation-and-conflicts.md` — 去重与冲突处理规则
- `references/privacy-and-redaction.md` — 敏感等级与导出处理
- `references/evaluation-cases.yaml` — 评测用例与预期护栏
- `templates/` — 来源清单与知识包大纲模板
- `scripts/validate_knowledge.py` — JSON/JSONL 结构校验脚本
- `agents/openai.yaml` — 界面元数据

## 快速开始

1. 复制 `templates/source-inventory.yaml`，定义范围、受众、来源与敏感等级。
2. 按 `references/collection-prompts.md` 中的统一契约，运行多个独立采集者。
3. 按 `references/knowledge-schema.yaml` 的结构将输出归一化。
4. 去重并记录冲突。批准状态、时间口径、权威性或受限数据必须经人工检查点确认。
5. 生成目标知识包或下游 Skill，公司事实与通用方法指令分开存放。
6. 用 `scripts/validate_knowledge.py` 校验 JSON/JSONL 记录，并执行 `references/evaluation-cases.yaml` 中的全部用例。

本包只包含占位内容。用于具体组织时，请替换为有授权、有来源依据的真实内容。

## 完整示例

`examples/meridian-office-furniture/` 以一家虚构公司完整跑通了全流程：两份采集者输出、归一化记录（`records.jsonl` / `records.yaml`）和一份冲突日志。示例刻意包含了一处多 AI 冲突、一处隐私泄漏、一处夸大表述、一对同义词、一条随时间变化的规则和一个缺失的负责人——与七个评测用例一一对应。

## 验证结果（2026-11-05 实跑）

对示例的校验（9 条记录）：

```text
$ python3 scripts/validate_knowledge.py examples/meridian-office-furniture/records.jsonl --export generic
records=9  errors=0  warnings=1   （第 5 条：confidential — 通用导出前需抽象/打码/剔除）
$ python3 scripts/validate_knowledge.py examples/meridian-office-furniture/records.jsonl --export internal
records=9  errors=0  warnings=0
$ python3 scripts/validate_knowledge.py examples/meridian-office-furniture/records.yaml --export generic
records=9  errors=0  warnings=1   （与 JSONL 结果一致 — 已支持 YAML 输入，需要 PyYAML）
```

负向测试（构造了缺失 `provenance`、重复 `record_id`、`proposed` 记录谎称 `high` 可信度的文件）正确失败：`errors=3, warnings=1`，退出码 1。

`references/evaluation-cases.yaml` 中的七个用例全部被该示例演练，对应关系记录在示例的 README 中。
