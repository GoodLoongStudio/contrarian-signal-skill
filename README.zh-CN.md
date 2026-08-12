# 反指指数 · Contrarian Signal

一个用于**公开市场观点历史回测与行为校准**的 Agent Skill。

它可以分析公开账号过去 365 天的市场观点和公开操作，区分 ACTION、OPINION、观点明确度和个人风格，并用后续真实行情计算可审计的历史反向命中率。

> 仅用于公开信息研究与历史统计，不构成投资建议，不生成买卖指令，不预测未来收益。

## v0.5 重点

- RAW / ACTION / OPINION 分开统计；
- 90-100、70-89、50-69、30-49、10-29、0-9 观点明确度分桶；
- THESIS、MOMENTUM、DIP_BUY、BREAKOUT_CHASE、RAPID_REVERSAL 等风格条件化回测；
- Style-Adjusted Score 用于保守描述历史特征的可迁移性；
- attribution gate：TARGET / THIRD_PARTY / UNCERTAIN；
- Evidence Ladder：Strong / Medium / Weak / Needs checking；
- 明确的金融研究边界和真人评价边界；
- `evals/`、`agents/`、独立 validator、SECURITY、CHANGELOG。

## 核心公式

```text
Contrarian Score =
CONTRARIAN_HIT /
(CONTRARIAN_HIT + ORIGINAL_CORRECT) * 100
```

这个分数只描述历史样本。样本量、个人风格和杠杆不会偷偷修改经验分数，而是作为独立解释层报告。

## Benchmark 方法案例

首批方法基准包括：

- 微博：**峰哥亡命天涯** —— 验证清仓、满仓、追涨、快速反向等 ACTION 分类与“名场面偏差”；
- X：**@aleabitoreddit（Serenity）** —— 验证长期 THESIS 与短期 ACTION/TIMING 分离。

Benchmark 只用于验证方法，不代表对真人整体能力或人格作评价，也不代表未来交易信号。

## 目录

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

## 运行计算器

```bash
python3 scripts/calc_score.py calls.json --pretty
```

## 本地校验

```bash
python3 scripts/validate_skill.py .
python3 -m unittest discover -s tests -p 'test_*.py'
```

GitHub Actions 同时运行单元测试、仓库 validator 和官方 Agent Skill specification 校验。

## 研究边界

本 Skill 不执行交易，不连接券商下单，不输出个性化仓位或杠杆指令，不保证收益，也不把历史反指分数解释成未来概率。

当前版本：**0.5.0**
