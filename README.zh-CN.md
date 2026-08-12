# 反指指数 · Contrarian Signal — 财经博主历史观点回测 Agent Skill

一个用于**财经博主反指分析、公开市场观点历史回测、微博 / X 投资观点研究和行为校准**的开源 Agent Skill。

Contrarian Signal 可以分析公开账号过去 365 天的市场观点与公开操作，区分 ACTION、OPINION、观点明确度和个人风格，并用后续真实行情计算可审计的历史反向命中率。它特别适合回答：**“这个财经博主到底是不是反指？”“过去一年观点准确率怎么样？”“他说的和实际操作是否一致？”**

> 仅用于公开信息研究与历史统计，不构成投资建议，不生成买卖指令，不预测未来收益。

## 安装

```bash
npx skills add GoodLoongStudio/contrarian-signal-skill
```

也可以直接从 GitHub 安装：

```bash
npx skills add https://github.com/GoodLoongStudio/contrarian-signal-skill
```

## 适合哪些场景

- 财经博主、股票博主、市场评论者的**反指指数**历史回测；
- 微博、X / Twitter 等公开社交媒体的**投资观点准确率分析**；
- 将“公开操作 ACTION”和“方向观点 OPINION”分开统计；
- 按 90-100、70-89、50-69、30-49、10-29、0-9 做观点明确度分桶；
- 分析追涨、抄底、长期 thesis、快速反向等个人风格；
- 检查粉丝投稿、引用、转发是否被错误归属给目标人物；
- 生成带证据强度、样本强度、95% Wilson 区间和 Coverage 的可审计历史研究结果。

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

## 常见问题

### 什么是反指指数？

反指指数表示在预先定义的历史窗口与观察周期内，可验证方向判断中有多少比例与后续市场方向相反。它是历史统计结果，不是未来胜率。

### 可以用来分析微博或 X 上的财经博主吗？

可以。前提是公开内容能够可靠归属到目标本人，并能恢复发布时间、标的、方向和观察周期。证据不足的记录不会强行进入评分。

### 能不能直接告诉我现在反着买什么？

不能。本 Skill 不执行交易，不连接券商下单，不输出个性化仓位、杠杆或买卖指令，也不会把历史反指分数解释成未来概率。

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

GitHub Actions 同时运行单元测试、仓库 validator 和 Agent Skill specification 校验。

当前版本：**0.5.0**

如果这个项目对你的研究有帮助，欢迎点一个 **GitHub Star ⭐**，让更多 Agent Skill 用户更容易发现它。
