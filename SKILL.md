---
name: contrarian-signal-skill
description: 用于回测公开市场评论者过去 365 天的投资观点与实际操作，量化其历史“反指”程度。Skill 会区分 ACTION 实际买卖与 OPINION 观点判断，按观点明确度分桶，结合个人交易/研究风格、持有周期、杠杆与反复横跳等特征，输出可审计的 RAW、ACTION、OPINION、风格条件化及风格调整反指分数。首批真实回测基准对象包括微博“峰哥亡命天涯”和 X 的“白毛股神” @aleabitoreddit（Serenity）。
license: MIT
compatibility: 需要访问公开网页/社交媒体内容与历史市场价格数据；Python 3 可选，用于确定性计算反指分数。
metadata:
  author: GoodLoongStudio
  version: "0.4.0"
---

# 反指信号（Contrarian Signal）

用于判断一个公开市场评论者，过去一段时间内是否具有稳定的“反指”特征。

它不是简单统计“这个人说涨后来跌了几次”，而是尽可能完整地收集历史观点与实际操作，冻结当时的方向、置信度、持有周期和个人风格，再用后续真实市场价格进行回测。

## 首批真实回测基准对象

本 Skill 已选用两类风格明显不同的公开市场评论者作为首批真实回测对象：

- **微博：峰哥亡命天涯** —— 重点测试频繁清仓、满仓、追涨、割肉、快速反向等 `ACTION` 型行为是否具有反指特征；
- **X：白毛股神 @aleabitoreddit（Serenity）** —— 重点测试长期产业链 Thesis、事件驱动、集中持仓和高波动交易中，`OPINION` 与 `ACTION` 是否出现明显分化。

这两个人只是首批 Benchmark，不是固定对象。Skill 可以用于分析任何具有公开历史内容的投资博主、分析师、交易员、财经自媒体或社交媒体账号。

## 核心输出

必须把不同维度的结果分开，不把所有行为揉成一个黑箱分数：

1. **RAW Contrarian Score** —— 所有可验证方向记录，不设置观点置信度门槛；
2. **ACTION Contrarian Score** —— 只统计本人明确的买入、加仓、持有、减仓、卖出、清仓等真实操作；
3. **OPINION Contrarian Score** —— 只统计看多、看空、赛道判断、市场方向等观点；
4. **观点置信度分桶** —— 90-100、70-89、50-69、30-49、10-29、0-9；
5. **Style-conditioned Score** —— 分别统计 THESIS、MOMENTUM、DIP_BUY、CATALYST、RAPID_REVERSAL 等个人风格下的反指率；
6. **Personal Style Profile** —— 个人交易/研究风格画像、主要风格、次要风格和风险放大因素；
7. **Style-Adjusted Contrarian Score** —— 根据个人风格稳定性和可迁移性，对历史反指特征做保守调整；
8. **样本强度 + 95% Wilson 区间** —— 描述统计可靠性，不偷偷修改原始分数。

历史反指分数公式：

`Contrarian Score = CONTRARIAN_HIT / (CONTRARIAN_HIT + ORIGINAL_CORRECT) * 100`

历史分数不能因为样本少、个人名气或交易风格而直接被人为加减。样本强度和风格调整必须作为独立层展示。

## 关键概念

### 1. Event Type：事件类型

在查看后续行情之前先冻结：

- `ACTION`：本人实际买入、加仓、持仓、减仓、卖出、清仓等仓位决策；
- `OPINION`：没有明确仓位变化的方向性观点；
- `UNKNOWN`：旧数据或无法可靠分类的记录。

事件类型具体规则见 `references/event-model.md`。

### 2. Attribution：内容归属

在查看行情之前先判断内容到底是不是目标本人观点：

- `TARGET`
- `THIRD_PARTY`
- `UNCERTAIN`

只有 `TARGET` 可以进入目标人物的反指分数。粉丝投稿、转发别人观点、引用新闻、其他人的交易记录都不能算成目标本人的预测。

### 3. Opinion Confidence：观点明确度

`opinion_confidence` 范围为 0-100，表示 Agent 对“这句话到底能不能明确恢复出看多/看空方向”的确定程度。

它不是预测成功概率，也不是统计学置信度。

必须在查看后续行情之前赋值。

### 4. Personal Style：个人风格

个人风格用于判断：**历史上哪些记录和当前这条观点最可比。**

它不能用于事后制造更高或更低的历史胜率。

每条 `TARGET` 方向记录在查看结果之前，可以赋予一个或多个 `style_tags`，规则见 `references/style-model.md`。

常见风格标签包括：

- `THESIS`：中长期产业/供应链逻辑；
- `CATALYST`：财报、合同、政策、审批、产品发布等事件驱动；
- `MOMENTUM`：趋势跟随；
- `MEAN_REVERSION`：均值回归；
- `DIP_BUY`：下跌后抄底；
- `BREAKOUT_CHASE`：突破或大涨后追入；
- `VALUE`：价值修复；
- `MACRO`：宏观驱动；
- `NEWS_REACTION`：新闻后的短期反应；
- `HIGH_CONVICTION`：极高确信或明显大仓位；
- `LEVERAGED`：杠杆或期权明显放大敞口；
- `CONCENTRATED`：持仓高度集中；
- `RAPID_REVERSAL`：短时间内频繁反转方向；
- `LONG_HORIZON`：20 个交易日以上；
- `SHORT_HORIZON`：5 个交易日以内。

## 默认分析范围

除非用户另有指定：

- 默认分析过去 365 天；
- 只使用公开内容；
- 优先追求“尽可能完整的可访问语料”，而不是只挑网上流传的名场面；
- RAW 纳入所有可验证的 `BULLISH` / `BEARISH` 记录，不设置观点明确度门槛；
- 保存所有排除项和数据缺口；
- ACTION 与 OPINION 必须分别统计；
- 只有数据足够时才建立个人风格画像。

## 适用请求示例

例如：

- “看看这个人是不是反指”
- “统计他过去一年的预测准确率”
- “算一下 @xxx 的反指指数”
- “90%-100% 观点明确度的反指是多少”
- “不设置信度，所有观点都统计”
- “把实际买卖动作和普通观点分开算”
- “他的个人风格会不会影响反指判断”
- “这个人长期 Thesis 很准，但择时很差，应该怎么评价”

如果只是普通股票推荐、投资建议或没有指定分析对象的泛情绪分析，不应该触发本 Skill。

## 工作流程

### 1. 精确确认目标身份

优先使用个人主页 URL、唯一账号 ID/Handle，或“显示名称 + 平台”确认目标身份，绝不能把同名账号混在一起。

### 2. 收集历史语料

收集时间窗口内所有可访问的市场相关公开内容，并至少保存：

- 发布时间；
- 原始来源 URL 或稳定 ID；
- 平台；
- 忠实原文、摘录或不改变含义的转述；
- 判断内容归属所需的上下文。

如果因为分页、删除、访问限制或索引缺失无法覆盖完整一年，必须标记 `PARTIAL`，并明确说明缺失范围。

### 3. 内容归属过滤

在查看市场结果前，将每条候选内容分类为 `TARGET`、`THIRD_PARTY` 或 `UNCERTAIN`。

只有 `TARGET` 可以进入本人评分，其余内容保留在审计记录中。

### 4. 分类 ACTION / OPINION

根据 `references/event-model.md`，在查看结果之前将记录分类成 ACTION、OPINION 或 UNKNOWN。

不能把粉丝投稿当作 ACTION，也不能把比喻、玩笑或模糊交易语言硬解释成真实操作。

### 5. 提取方向

分类为：

- `BULLISH`
- `BEARISH`
- `NEUTRAL`
- `UNSCORABLE`

RAW 应保留那些虽然语气较弱、但仍能明确恢复方向的观点。真正中性或无法判断的内容不能强行进入评分。

### 6. 赋予观点明确度

对每个 BULLISH / BEARISH 记录，根据 `references/scoring-rules.md` 赋予 0-100 的 `opinion_confidence`，并在查看后续价格之前冻结。

### 7. 赋予个人风格标签

在查看行情结果之前，根据 `references/style-model.md` 给记录添加 `style_tags`。

只能根据原始措辞、公开仓位行为、持有周期和上下文判断，绝不能因为后来涨跌了才事后改变风格标签。

### 8. 去重

48 小时内，如果资产、方向和 Thesis 基本相同，则默认只算一次。

只有当方向、真实仓位、目标价、持有周期、失效条件或独立可验证逻辑发生实质变化时，才算新的独立记录。

如果 ACTION 与 OPINION 只是描述同一次真实交易决策，优先保留 ACTION，不重复计数。

### 9. 冻结回测周期

必须在查看后续价格之前确定：

- ACTION 没有明确期限：默认下一个交易日收盘；24/7 市场默认 24 小时；
- OPINION：优先使用原文明确期限；没有期限时使用确定性映射；完全没有时间表述时默认 5 个交易日；
- 长期 `THESIS` 如果原文能够恢复中长期目标周期，应按照其真实预期周期回测，不能强制改成第二天收盘。

禁止为了制造“名场面”选择盘中最高点、最低点，也禁止看到结果后再改变观察周期。

### 10. 验证真实价格结果

使用可靠历史行情数据，并记录：

- entry timestamp / price；
- evaluation timestamp / price；
- return_pct；
- price source。

### 11. 标记结果

使用：

- `ORIGINAL_CORRECT`
- `CONTRARIAN_HIT`
- `FLAT`
- `UNVERIFIABLE`
- `UNSCORABLE`

普通方向记录：

| 原始方向 | 后续价格 | 结果 |
|---|---|---|
| BULLISH | 上涨 | ORIGINAL_CORRECT |
| BULLISH | 下跌 | CONTRARIAN_HIT |
| BEARISH | 下跌 | ORIGINAL_CORRECT |
| BEARISH | 上涨 | CONTRARIAN_HIT |

`FLAT`、`UNVERIFIABLE`、`UNSCORABLE` 不进入分数分母，但必须报告数量。

### 12. 确定性计算历史分数

优先执行：

`python3 scripts/calc_score.py calls.json --pretty`

计算器会输出：

- 综合 RAW；
- ACTION / OPINION / UNKNOWN；
- 全局观点明确度分桶；
- ACTION / OPINION 内部分桶；
- style tag 分数；
- 缺失字段与审计统计。

### 13. 建立个人风格画像

完整分类后，根据 `references/style-model.md` 汇总：

- primary archetype；
- secondary archetypes；
- dominant style tags；
- risk amplifiers；
- THESIS Accuracy 和 TIMING Accuracy 是否明显分化；
- 数据足够时，评估 Style Transferability。

杠杆、集中持仓、高 Beta、持续补仓等只用于解释风险和回撤，不能自动提高反指分数。

### 14. 可选 Style-Adjusted Score

只有以下五个维度都有足够证据时才允许计算：

- `horizon_consistency`
- `action_opinion_consistency`
- `regime_stability`
- `directional_persistence`
- `corpus_representativeness`

计算器取五项算术平均得到 `style_transferability`，然后使用：

`Style-Adjusted Score = 50 + (Base Contrarian Score - 50) * style_transferability / 100`

风格越不稳定，历史反指分数越应该向中性 50 收缩。

任何 Style-Adjusted Score 都必须同时展示原始经验分数，不能取代它。

### 15. 当前观点匹配

如果用户询问某个人最新一条观点意味着什么，优先使用最相似、且样本量足够的历史记录：

1. 相同 Event Type + 相同 Style Tag + 相同观点明确度区间；
2. 相同 Event Type + 相同 Style Tag；
3. 相同 Event Type + 相同观点明确度区间；
4. 相同 Event Type；
5. RAW。

如果最细分桶样本不足，就逐级回退，并明确告诉用户。

### 16. 保守解释样本

样本强度：

- N < 5 -> INSUFFICIENT
- 5-9 -> VERY_LOW
- 10-19 -> LOW
- 20-49 -> MEDIUM
- 50+ -> HIGH

不能因为一个小样本桶出现 100 分，就把一个人描述为稳定反指。

### 17. 输出报告

使用 `assets/report-template.md`，报告至少包括：

- 目标人物、时间窗口、数据覆盖情况；
- 候选与排除数量；
- RAW / ACTION / OPINION；
- 观点明确度分桶；
- 个人风格画像；
- 风格条件化分数；
- 可选 Style-Adjusted Score；
- 按时间排序的证据表；
- 排除项、方法和限制。

## 偏差控制

主动防止：

- 只挑传播最广的失败案例；
- 重复计算同一观点；
- 把粉丝投稿或第三方观点算成本人预测；
- 看到结果后修改 Event Type；
- 看到结果后修改 opinion_confidence；
- 看到结果后修改 style_tags；
- 看到结果后改变观察周期；
- 为了让故事更戏剧化使用盘中极值；
- 把杠杆和集中持仓直接当作“方向判断错误”；
- 用第二天的下跌判定一个半年期 Thesis 失败；
- 为了挽救一次短期错误操作，事后把持有周期延长；
- 因为人物名气、粉丝量或网络口碑影响分类。

## 失败处理

如果公开语料无法覆盖完整时间窗口，必须输出 `PARTIAL`，不能宣称“完整全年回测”。

如果内容归属不确定，排除出目标人物评分。

如果可靠价格数据无法获取，标记 `UNVERIFIABLE`。

如果方向或事件类型无法诚实恢复，标记 `UNSCORABLE`。

如果 Style Transferability 五项无法得到证据支持，就不输出 Style-Adjusted Score，不能猜测。

## 支持文件

- 事件类型与归属模型：`references/event-model.md`
- 评分、观点明确度与观察周期规则：`references/scoring-rules.md`
- 个人风格模型：`references/style-model.md`
- 确定性计算器：`scripts/calc_score.py`
- 报告模板：`assets/report-template.md`
