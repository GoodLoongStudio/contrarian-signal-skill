# Contrarian Signal · 反指指数 — AI Agent Skill for Market Opinion Backtesting

![Agent Skill CI](https://github.com/GoodLoongStudio/contrarian-signal-skill/actions/workflows/ci.yml/badge.svg)
[![skills.sh](https://skills.sh/b/GoodLoongStudio/contrarian-signal-skill)](https://skills.sh/GoodLoongStudio/contrarian-signal-skill)
![MIT License](https://img.shields.io/badge/license-MIT-green.svg)

**判断财经博主、投资评论者和公开市场账号“到底是不是反指”的开源 Agent Skill。**  
**An open Agent Skill for retrospective market-opinion backtesting, contrarian-signal analysis, and behavioral calibration of public market commentators.**

Contrarian Signal 可对 **微博、X / Twitter 等公开社交媒体账号**的历史投资观点与公开操作做回测，区分 ACTION 与 OPINION，在查看后续行情前冻结方向、观点明确度、观察周期与个人风格，再用真实历史市场数据计算可审计的 **Contrarian Score / 反指指数**。

适合用于：**财经博主反指分析、历史观点准确率回测、社交媒体投资观点分析、股票/市场评论者行为研究、contrarian indicator research、market commentator backtesting、behavioral finance research**。

中文：[`README.zh-CN.md`](README.zh-CN.md) · English: [`README.en.md`](README.en.md)

> 仅用于公开信息研究与历史统计，不构成投资建议，不生成买卖指令，不执行交易，也不预测未来收益。  
> Research support only. Not investment advice. No trade execution, order instructions, or future-return promises.

## Install / 安装

```bash
npx skills add GoodLoongStudio/contrarian-signal-skill
```

也可以直接从 GitHub 安装：

```bash
npx skills add https://github.com/GoodLoongStudio/contrarian-signal-skill
```

仓库采用开放 `SKILL.md` 格式。核心定义见 [`SKILL.md`](SKILL.md)，评分规则见 [`references/scoring-rules.md`](references/scoring-rules.md)。

## What it does / 能做什么

输入一个公开市场评论者或财经账号的历史公开内容后，Contrarian Signal 会把研究拆成可审计的独立层，而不是输出一个无法解释的“神秘分数”：

- **RAW Contrarian Score**：所有可验证方向记录的历史反向命中率；
- **ACTION Score**：买入、加仓、减仓、卖出、清仓等公开动作；
- **OPINION Score**：方向性观点、赛道判断和市场预期；
- **Opinion Confidence Buckets**：90-100、70-89、50-69、30-49、10-29、0-9；
- **Personal Style Profile**：THESIS、MOMENTUM、DIP_BUY、BREAKOUT_CHASE、RAPID_REVERSAL 等；
- **Style-Adjusted Score**：对不稳定历史特征向中性 50 做保守收缩；
- **Evidence & Coverage**：证据强度、样本强度、95% Wilson 区间和语料覆盖限制；
- **Attribution Gate**：TARGET / THIRD_PARTY / UNCERTAIN，避免把粉丝投稿或引用内容算到本人头上。

核心经验公式：

```text
Contrarian Score =
CONTRARIAN_HIT /
(CONTRARIAN_HIT + ORIGINAL_CORRECT) * 100
```

这个数字只描述历史样本，不是未来收益概率。

## Typical use cases / 典型使用场景

- **某个财经博主是不是“反指”？** 对过去 365 天公开观点做历史回测；
- **微博 / X 投资观点历史准确率怎么样？** 把观点与真实后续行情逐条核验；
- **他说的和他实际做的是不是一回事？** 分离 ACTION 与 OPINION；
- **高置信表达是不是更容易错？** 按观点明确度分桶统计；
- **某种个人风格是否更容易产生反向结果？** 按 THESIS、追涨、抄底、快速反向等 Style Tags 回测；
- **How often was a public market commentator historically contrarian?** Produce auditable, evidence-backed retrospective statistics.

## Benchmark methodology cases

首批公开方法学 Benchmark：

- **微博：峰哥亡命天涯** —— 用于验证 ACTION、追涨/清仓、快速反向、投稿归属和“名场面偏差”；
- **X：@aleabitoreddit（Serenity）** —— 用于验证长期 THESIS 与短期 ACTION/TIMING 分离。

Benchmark 用于验证方法，不是对真人整体能力或人格的评价，也不是未来交易信号。安全输出示例见 [`examples/benchmark-safe-output.md`](examples/benchmark-safe-output.md)。

## FAQ

### 什么是“反指指数 / Contrarian Score”？

它表示在一个预先定义的历史窗口和观察周期内，可验证方向判断中有多少比例与后续市场方向相反。它是**历史统计指标**，不是未来预测概率。

### 可以分析微博、X / Twitter 上的财经博主吗？

可以，只要内容是公开可访问、能够可靠归属到目标本人，并且能够恢复发布时间、标的、方向和观察周期。证据不足的内容不会强行进入评分。

### 这个 Skill 会告诉我现在买什么股票吗？

不会。它只做公开信息研究、历史回测和行为校准，不输出个性化买卖、仓位、杠杆或收益承诺。

### Can it backtest market commentators on social media?

Yes. The methodology is designed for public market commentary and disclosed actions, with attribution checks, historical price verification, confidence buckets, style conditioning, and explicit coverage limits.

## Repository structure

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

If this project is useful to your research, consider giving it a **GitHub Star ⭐** so more Agent Skill users can discover it.
