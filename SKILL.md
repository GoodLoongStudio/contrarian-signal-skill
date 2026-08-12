---
name: contrarian-signal-skill
description: 对公开市场评论者过去 365 天的公开观点与公开操作做历史回测和行为校准。用于“反指 / contrarian”、历史判断准确率、ACTION 与 OPINION 分离、观点明确度分桶、个人风格条件化和 Style-Adjusted 分析。输出仅用于研究与统计，不生成买卖指令、仓位建议或未来收益承诺。使用公开证据，先冻结 attribution、event type、方向、观点明确度、观察周期和 style tags，再核验历史价格，返回可审计的分数、证据强度、样本强度和覆盖限制。
license: MIT
compatibility: 需要访问公开网页/社交媒体内容与历史市场价格数据；Python 3 可选，用于确定性计算历史回测分数。
metadata:
  author: GoodLoongStudio
  version: "0.5.0"
---

# 反指指数 · Contrarian Signal

Contrarian Signal 是一个**公开市场观点历史回测与行为校准 Skill**。

它回答的问题不是“现在应该不应该反着买”，而是：

> 在一个明确的历史时间窗、可验证的公开语料和预先冻结的观察周期下，这个账号的公开方向判断有多常与后续市场方向相反？这种现象集中在哪类行为、观点明确度和个人风格里？

“反指 / contrarian”在本 Skill 中只是一种**历史统计标签**，不代表未来交易信号。

**本结果不构成投资建议，不生成买卖指令，不执行交易，也不把历史分数解释成未来收益概率。**

## 核心输出

始终把不同维度分开，避免一个黑箱分数覆盖所有行为：

1. **RAW Contrarian Score**：所有可验证方向记录的历史反向命中率；
2. **ACTION Contrarian Score**：仅本人公开的买入、加仓、持有、减仓、卖出、清仓等动作；
3. **OPINION Contrarian Score**：仅方向性观点、赛道判断和市场预期；
4. **观点明确度分桶**：90-100、70-89、50-69、30-49、10-29、0-9；
5. **Style-conditioned Score**：按 THESIS、MOMENTUM、DIP_BUY、BREAKOUT_CHASE、RAPID_REVERSAL 等风格分组回测；
6. **Personal Style Profile**：主要风格、次要风格、持有周期、方向持续性和风险放大因素；
7. **Style-Adjusted Contrarian Score**：当风格可迁移性证据充分时，对历史分数向中性 50 做保守收缩；
8. **样本强度 + 95% Wilson 区间 + Coverage**：用于描述统计可靠性和语料缺口。

历史经验分数：

`Contrarian Score = CONTRARIAN_HIT / (CONTRARIAN_HIT + ORIGINAL_CORRECT) * 100`

样本量、知名度、个人风格和杠杆不能直接篡改这个经验分数；它们作为独立解释层展示。

## 研究与合规边界

涉及股票、基金、期权、加密资产或其他投资标的时，先读取 `references/risk-and-compliance.md`。

允许：

- 历史回测；
- 公开行为校准；
- 证据强弱和不确定性；
- 样本覆盖说明；
- “历史上哪些类型更容易出现反向结果”。

不允许把结果机械转成：

- “现在直接反着买/卖”；
- 个性化仓位、杠杆或下单指令；
- 保证收益或未来胜率承诺；
- 对真实人物人格、诚信或职业能力的无依据评价。

如果用户询问当前观点，应把历史分数当作**研究上下文**，同时重新核验当前观点、当前行情和当前事件；历史分数不能替代当前研究。

## Benchmark 方法案例

首批方法基准保留两个公开账号，用来测试不同的分类难点：

- **微博：峰哥亡命天涯**：重点验证 ACTION、快速反向、追涨/清仓、投稿归属和“名场面偏差”处理；
- **X：@aleabitoreddit（Serenity）**：重点验证长期 THESIS 与短期 ACTION/TIMING 分离，以及集中/杠杆风险与方向研究的区别。

这些账号只是**方法学 Benchmark**。结果只对应具体时间窗、可访问语料、固定观察周期与公开行情，不是对其人格或整体专业能力的评价，也不是未来交易信号。真人评价规则见 `references/public-person-evaluation.md`。

## 关键概念

### Event Type

在查看后续价格前冻结：

- `ACTION`：目标本人明确的仓位/交易动作；
- `OPINION`：没有明确仓位变化的方向性观点；
- `UNKNOWN`：旧数据或无法可靠分类的记录。

详细规则：`references/event-model.md`。

### Attribution

在查看后续价格前冻结：

- `TARGET`
- `THIRD_PARTY`
- `UNCERTAIN`

只有 `TARGET` 可以进入目标人物分数。粉丝投稿、转发别人观点、引用故事和第三方操作不能算成目标本人预测。

### Direction

分类：

- `BULLISH`
- `BEARISH`
- `NEUTRAL`
- `UNSCORABLE`

RAW 不设置观点明确度门槛，但真正中性或无法恢复方向的内容不能强行评分。

### Opinion Confidence

`opinion_confidence` 为 0-100，表示**方向含义有多清晰**，不是预测成功概率，也不是统计学置信度。

必须在查看结果之前赋值。详细分桶规则：`references/scoring-rules.md`。

### Personal Style

每条 TARGET 方向记录在查看结果之前可以添加 `style_tags`。

推荐标签：

- `THESIS`
- `CATALYST`
- `MOMENTUM`
- `MEAN_REVERSION`
- `DIP_BUY`
- `BREAKOUT_CHASE`
- `VALUE`
- `MACRO`
- `NEWS_REACTION`
- `HIGH_CONVICTION`
- `LEVERAGED`
- `CONCENTRATED`
- `RAPID_REVERSAL`
- `LONG_HORIZON`
- `SHORT_HORIZON`

个人风格用于判断**哪些历史记录更可比**，不能因为后来涨跌了才事后改标签。详细规则：`references/style-model.md`。

## 默认分析范围

除非用户另有指定：

- 分析过去 365 天；
- 只使用公开内容；
- 优先追求尽可能完整的可访问语料，而不是只挑流传最广的错误案例；
- RAW 纳入所有可验证的 BULLISH/BEARISH TARGET 记录；
- ACTION 与 OPINION 分开报告；
- 保存排除项与数据缺口；
- 只有数据足够时才生成 Style-Adjusted Score。

如果平台限制、删除内容、登录墙、分页或索引缺口导致无法覆盖完整时间窗，必须标记 `PARTIAL`。不要把部分样本称为全年全量。

## 工作流程

### 1. Resolve identity

用主页 URL、唯一 handle/ID，或“显示名称 + 平台”确认目标。不要合并同名账号。

### 2. Collect corpus

收集时间窗内可访问的市场相关公开内容，至少保存：

- 发布时间；
- 原始 URL / 稳定 ID；
- 平台；
- 忠实原文或不改变含义的摘录；
- attribution 所需上下文。

来源规范见 `references/research-sources.md`。

### 3. Grade evidence

给观点原文、内容归属和价格验证分别判断证据强度。优先一手来源；二手截图和搜索摘要只能作为线索。

证据等级见 `references/evidence-ladder.md`。

### 4. Attribution gate

先分类 TARGET / THIRD_PARTY / UNCERTAIN，再做市场回测。

非 TARGET 可以保留在审计记录，但不能进入目标分数。

### 5. Classify ACTION / OPINION

根据 `references/event-model.md` 判断事件类型。

如果 ACTION 和 OPINION 只是同一次交易决策的重复表达，优先保留一个 ACTION，避免双计数。

### 6. Freeze direction and opinion confidence

在查看后续行情前冻结：

- direction；
- opinion_confidence；
- style_tags。

### 7. Deduplicate

48 小时内，资产 + 方向 + thesis 基本一致时默认只算一次。

只有方向、真实仓位、目标价、观察周期、失效条件或独立可验证逻辑实质改变时，才形成新记录。

### 8. Freeze evaluation horizon

必须先确定观察周期，再查后续价格。

默认：

- ACTION 无明确期限：下一个交易日收盘；24/7 市场默认 24 小时；
- OPINION：优先原文明确期限；否则按确定性措辞映射；完全无时间表述时默认 5 个交易日；
- 长期 THESIS：使用可恢复的原始预期周期，不能强制改成第二天。

禁止看到结果后改观察周期，禁止用最戏剧性的盘中高点/低点决定输赢。

### 9. Verify historical price outcome

记录：

- entry timestamp / price；
- evaluation timestamp / price；
- return_pct；
- price source。

价格无法可靠验证时，标记 `UNVERIFIABLE`。

### 10. Label outcome

使用：

- `ORIGINAL_CORRECT`
- `CONTRARIAN_HIT`
- `FLAT`
- `UNVERIFIABLE`
- `UNSCORABLE`

普通方向关系：

| 原方向 | 后续价格 | Outcome |
|---|---|---|
| BULLISH | 上涨 | ORIGINAL_CORRECT |
| BULLISH | 下跌 | CONTRARIAN_HIT |
| BEARISH | 下跌 | ORIGINAL_CORRECT |
| BEARISH | 上涨 | CONTRARIAN_HIT |

FLAT / UNVERIFIABLE / UNSCORABLE 不进入经验分数分母，但必须报告数量。

### 11. Calculate deterministically

优先使用：

`python3 scripts/calc_score.py calls.json --pretty`

输出包括：

- RAW；
- ACTION / OPINION / UNKNOWN；
- 观点明确度分桶；
- ACTION / OPINION 内部分桶；
- style tag 分数；
- style profile；
- style-adjusted；
- 缺失字段审计统计。

### 12. Build style profile

汇总：

- primary archetype；
- secondary archetypes；
- dominant style tags；
- risk amplifiers；
- THESIS accuracy 与 TIMING accuracy 是否分化；
- style transferability components。

杠杆、集中持仓、高 Beta、持续补仓等只能解释风险和回撤，不能自动提高反向命中率。

### 13. Optional Style-Adjusted Score

只有以下五项都有证据时才计算：

- horizon_consistency
- action_opinion_consistency
- regime_stability
- directional_persistence
- corpus_representativeness

`style_transferability = 五项算术平均`

`Style-Adjusted Score = 50 + (Base Contrarian Score - 50) * style_transferability / 100`

它是保守解释层，不能替代经验分数。

### 14. Report conservatively

样本强度：

- N < 5：INSUFFICIENT
- 5-9：VERY_LOW
- 10-19：LOW
- 20-49：MEDIUM
- 50+：HIGH

不要因为一个小桶分数极端，就把目标称为“稳定反指”。

报告使用 `assets/report-template.md`，并包含：

- 目标与时间窗；
- Coverage；
- 候选/排除数量；
- RAW / ACTION / OPINION；
- 观点明确度分桶；
- Style-conditioned Scores；
- 可选 Style-Adjusted Score；
- 证据等级；
- 典型正确与典型反向案例；
- 排除记录；
- 方法和局限；
- 研究边界。

## 当前观点匹配

如果用户问“这个人最新这条怎么看”，历史数据只能作为校准上下文。

优先匹配顺序：

1. 相同 event type + 相同 style tag + 相同明确度分桶；
2. 相同 event type + 相同 style tag；
3. 相同 event type + 相同明确度分桶；
4. 相同 event type；
5. RAW。

如果窄桶样本不足，向上回退并明确说明。

即使历史桶反向命中率很高，也不能输出机械买卖指令；当前信息需要独立核验。

## Bias controls

主动防止：

- cherry-picking viral failures；
- 重复帖双计数；
- 第三方投稿算成本人；
- 看完行情再改 event type / confidence / style tag；
- 事后改变 horizon；
- 用盘中极值制造“名场面”；
- 用杠杆或回撤代替方向正确性判断；
- 用第二天亏损否定长期 thesis；
- 用后来反弹挽救原本的短期错误动作；
- 因知名度、昵称或网络声誉改变分类标准。

## Failure modes

- 语料不完整：标记 `PARTIAL`；
- attribution 不确定：排除目标评分；
- 价格无法可靠核验：`UNVERIFIABLE`；
- 方向无法诚实恢复：`UNSCORABLE`；
- 风格迁移性证据不足：Style-Adjusted Score 返回 null；
- 用户要求直接交易指令：保留历史研究结论，但不把分数转成买卖命令。

## Supporting files

- 研究与合规边界：`references/risk-and-compliance.md`
- 证据等级：`references/evidence-ladder.md`
- 公开来源规范：`references/research-sources.md`
- 真人评价规范：`references/public-person-evaluation.md`
- Event / attribution：`references/event-model.md`
- Scoring / confidence / horizon：`references/scoring-rules.md`
- Personal style：`references/style-model.md`
- 确定性计算器：`scripts/calc_score.py`
- 发布结构校验器：`scripts/validate_skill.py`
- 报告模板：`assets/report-template.md`
- 行为与合规评测：`evals/test-cases.md`
- 安全输出示例：`examples/benchmark-safe-output.md`
