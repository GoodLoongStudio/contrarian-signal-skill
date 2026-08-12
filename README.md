# Contrarian Signal · 反指指数

![Agent Skill CI](https://github.com/GoodLoongStudio/contrarian-signal-skill/actions/workflows/ci.yml/badge.svg)

**公开市场观点历史回测与行为校准 / Retrospective public-market opinion backtesting and behavioral calibration.**

中文文档：[`README.zh-CN.md`](README.zh-CN.md)  
English: [`README.en.md`](README.en.md)

> 仅用于公开信息研究与历史统计，不构成投资建议，不生成买卖指令，不执行交易，也不预测未来收益。  
> Research support only. Not investment advice. No trade execution, order instructions, or future-return promises.

## v0.5

Contrarian Signal 现在不再只是一个“反指分数”脚本，而是一个完整的发布级 Agent Skill：

- **RAW / ACTION / OPINION** 历史分数；
- **观点明确度分桶**：90-100、70-89、50-69、30-49、10-29、0-9；
- **Personal Style**：THESIS、MOMENTUM、DIP_BUY、BREAKOUT_CHASE、RAPID_REVERSAL 等；
- **Style-Adjusted Score**：对不稳定历史特征向中性 50 做保守收缩；
- **Attribution Gate**：TARGET / THIRD_PARTY / UNCERTAIN；
- **Evidence Ladder**：Strong / Medium / Weak / Needs checking；
- **Research & Compliance Boundary**；
- **Public-person evaluation guardrails**；
- **evals / agents / validator / SECURITY / CHANGELOG**。

核心经验公式：

```text
Contrarian Score =
CONTRARIAN_HIT /
(CONTRARIAN_HIT + ORIGINAL_CORRECT) * 100
```

这个数字只描述历史样本，不是未来收益概率。

## Benchmark methodology cases

首批方法基准：

- 微博：**峰哥亡命天涯** —— ACTION、追涨/清仓、快速反向、投稿归属与名场面偏差；
- X：**@aleabitoreddit（Serenity）** —— 长期 THESIS 与短期 ACTION/TIMING 分离。

Benchmark 用于验证方法，不是对真人整体能力或人格的评价，也不是未来交易信号。

## Structure

```text
contrarian-signal-skill/
├── SKILL.md
├── README.md
├── README.zh-CN.md
├── README.en.md
├── SECURITY.md
├── CHANGELOG.md
├── agents/
│   └── openai.yaml
├── assets/
│   └── report-template.md
├── evals/
│   └── test-cases.md
├── examples/
│   └── benchmark-safe-output.md
├── references/
│   ├── risk-and-compliance.md
│   ├── evidence-ladder.md
│   ├── research-sources.md
│   ├── public-person-evaluation.md
│   ├── event-model.md
│   ├── scoring-rules.md
│   └── style-model.md
├── scripts/
│   ├── calc_score.py
│   └── validate_skill.py
└── tests/
    └── test_calc_score.py
```

## Validate

```bash
python3 scripts/validate_skill.py .
python3 -m unittest discover -s tests -p 'test_*.py'
```

Current Skill version: **0.5.0**
