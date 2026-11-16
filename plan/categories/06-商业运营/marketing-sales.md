# 营销/销售 · tools/{marketing,advertising,sales}（~70 页）

- `node scripts/verify_marketing_calc.js utm-builder` 为 2/2；此为 DOM 桩及函数级验证，未验证浏览器实际复制/下载；其他既有问题不在本项复核范围。

## 2026-11-06 公关评估和流程静态续审

- `tools/pr/assessor-56.html:123,169-184`、`assessor-57.html:124,170-185`、`assessor-manager-2.html:124,170-189`、`assessor-risk.html:128,174-192`：下拉变化触发分数或风险矩阵重算，默认分别取各选项首项并立即显示结论；风险页默认全部最低风险不等于已完成评估。均为静态分析，未运行浏览器。

## 2026-11-06 公关工具静态续审

- `tools/pr/analysis-6.html:206-238`：词典逐项匹配，不处理否定及上下文；例如「不推荐」仍命中正向「推荐」，结果为正面倾向。应明确标注词典统计局限，不宜作为可靠情感判断。

## 功能缺陷
- ~~ROI 页缺「多渠道对比表」（同预算分三渠道敏感性）。~~【915 批核实已覆盖，保留原条目备查】：`marketing-ad-budget-allocator.html` 已实现 3 渠道手写比例/ROAS 加权分配 + 逐渠道点击/转化/CPA 对比 + 整体 ROAS；`ad-roi.html` 含渠道对比场景；verify_marketing_calc 覆盖。
- ~~广告缺「A/B 测试显著性判定」（样本量+转化率→p 值，纯前端可算）。~~【915 批核实已覆盖，保留原条目备查】：`marketing-ab-test-significance.html` 已实现两比例 z 检验 + p 值 + α=0.05 判定 + 样本量/功效，verify 6 条用例。

## 优化点
- S3 分步：盈亏平衡点图解。

## 受影响范围
- tools/marketing/（46）、tools/advertising/、tools/sales/

## 进度
- 🟡 续批中（剩余：S3 盈亏平衡图解）；多渠道对比表与 A-B 显著性缺口已于 915 批核实由现有工具覆盖，不再列为待办。

## 2026-11-06 静态续审：营销 8 页

> 仅阅读当前源码，未运行页面或浏览器；历史条目是当时的证据，以下说明当前关键代码变化，不代表完整回归通过。

## 2026-11-03 第一轮抽样补充

### 覆盖
- 本次抽查上述 2 页，原函数内存 DOM 桩，未实测浏览器、线上和其余营销销售页面。

## 2026-11-03 续查（并行批 F）

### 留存优化
- `tools/sales/stacked-discount.html`：折扣层支持拖动排序（当前只能删后重加才能换顺序），并在结果区并列展示「先折后减 / 先减后折」两种顺序的成交价差，正好呼应页面已写「顺序不同结果不同」的示例。
- `tools/sales/commission-calculator.html`：阶梯档位表增加「区间（上档—本档）× 比例 × 该段佣金」的分解列，让 15000 这类合计可被逐段核对；同时保存档位配置到 localStorage，避免每次重填。
- `tools/sales/cost-price-margin.html`：把「利润率 ↔ 加价率对照表」改为按当前输入高亮对应行，并在结果卡加一行「若按毛利率口径 40%，售价应为 …」，直接消除两种口径的混淆。
- `tools/sales/target-breakdown.html`：结果表增加「差额」列（逐行合计 − 总目标）并允许一键把尾差补给权重最大者，替代当前只能眼看合计对不上。
- `tools/sales/price-calculator.html`：四种定价模式并列对比（同一成本/固定成本下四个建议售价与毛利率），当前需切换模式逐次记录。
- `tools/marketing/marketing-break-even-roas.html`：把「盈亏平衡 ROAS」「目标 ROAS」「当前 ROAS」三值画成一条数轴并标出所处区间，替代纯卡片陈列；参考表可按用户输入的毛利率高亮所属行业行。
- `tools/marketing/marketing-ltv-cac-ratio.html`：增加 LTV 构建器（客单价 × 年购买频次 × 寿命年数 × 毛利率），让 LTV 从「拍一个数」变成可追溯推导，同时把 36 个月假设显式化。

### 续查覆盖
- `tools/sales/stacked-discount.html`
- `tools/sales/commission-calculator.html`
- `tools/sales/cost-price-margin.html`
- `tools/sales/target-breakdown.html`
- `tools/sales/price-calculator.html`
- `tools/marketing/marketing-break-even-roas.html`
- `tools/marketing/marketing-ltv-cac-ratio.html`
- 本次仅做源码阅读与 node 内存复算（按页面 `calc()` 表达式重写同名函数取输出），未做浏览器、英文态、移动端、门禁或线上验证；`marketing-ltv-cac-ratio` 的 36 个月寿命属产品假设，标注为待验证。

## 2026-11-03 续查（并行批 J）

### 留存优化
- `tools/marketing/marketing-cpa-calculator.html`：把「CPA / CPC / CVR」画成同一漏斗的三段（花费 → 点击 → 新客），让 200% 这类异常在图形上直接暴露。
- `tools/marketing/marketing-roas-calculator.html`：增加「毛利率」输入并把「盈亏平衡 ROAS / 当前 ROAS / 目标 ROAS」并列到同一数轴，替代当前用当前毛利率反推的隐式假设。
- `tools/marketing/marketing-cac-calculator.html`：回收期展示后，增加「营销端/销售端回收期」拆分，直接看出该先压缩哪一段费用。
- `tools/marketing/marketing-churn-rate.html`：结果区加一行口径提示（期初口径 vs 期末口径），并允许按月连续录入多期，画流失率趋势而不是单期快照。
- `tools/marketing/marketing-conversion-rate-calculator.html`：把 CVR 的分子分母做成可切换口径（访问→转化、点击→转化），避免「转化数超过访问量」这类跨口径误填。
- `tools/sales/sales-forecast.html`：置信区间同时给出「残差 σ」与「历史 σ」两种宽度并允许切换，让用户看到模型拟合质量对区间的影响。
- `tools/marketing/marketing-discount-rate.html`：三种模式共用一个「原价 + 折后价」双向滑块，拖动时实时显示折扣率/折数/节省，从交互上消除「折后价高于原价」的录入可能。
- `tools/sales/moving-average.html`：结果表增加一行「下期预测」并高亮，同时把 WMA 的权重序列（1/2/3）直接列在表头，预测口径错误可被肉眼核对。

### 续查覆盖
- `tools/marketing/marketing-cpa-calculator.html`
- `tools/marketing/marketing-roas-calculator.html`
- `tools/marketing/marketing-cac-calculator.html`
- `tools/marketing/marketing-churn-rate.html`
- `tools/marketing/marketing-conversion-rate-calculator.html`
- `tools/sales/sales-forecast.html`
- `tools/marketing/marketing-discount-rate.html`
- `tools/sales/moving-average.html`
- 本次仅做源码阅读与 node 内存复算（按页面 `calc()` / `forecast()` 表达式在 node 中重写同名逻辑取输出），未做浏览器、英文态、移动端、门禁或线上验证；`marketing-cac-calculator` 的 36 个月生命周期属产品假设，`sales-forecast` 的季节周期自动钳制行为仅按源码推断，均标注为待验证。

## 2026-11-04 续查（并行批 M）

> 范围：本轮阅读 3 页（`tools/marketing/marketing-coupon-discount.html`、`tools/marketing/marketing-free-shipping-threshold.html`、`tools/marketing/marketing-ad-budget-allocator.html`）。仅源码 + node 复算，未开浏览器/未做 EN/移动端/门禁验证。

- 本轮实读 3 页：`tools/marketing/marketing-coupon-discount.html`、`tools/marketing/marketing-free-shipping-threshold.html`、`tools/marketing/marketing-ad-budget-allocator.html`；新增 6 条（高 0/中 6/低 0）；未覆盖：本轮未读 `tools/marketing` 其余页面及 `tools/sales` 其余页面；MS-M1 与既有 MS-F1 同属折扣率区间校验族但页面不同，MS-M5/MS-M6 与 MS-J1 同属输入校验/名实不符族但页面不同，编号续本文件 `MS-` 风格改用批 M，无重号。

## 2026-11-04 续查（并行批 N）

> 范围：本轮阅读 3 页（`tools/marketing/marketing-cpm-calculator.html`、`tools/marketing/marketing-markup-margin.html`、`tools/marketing/marketing-sales-funnel.html`）。仅源码 + node 复算，未开浏览器/未做 EN/移动端/门禁验证。

- 本轮实读 3 页：`tools/marketing/marketing-cpm-calculator.html`、`tools/marketing/marketing-markup-margin.html`、`tools/marketing/marketing-sales-funnel.html`；新增 5 条（高 1/中 3/低 1）；未覆盖：本轮未读 `tools/marketing` 其余页面及 `tools/sales` 其余页面；与批 M 的 coupon/free-shipping/ad-budget 三页无重复，MS-N1 为换算公式错误族、MS-N3/N4 为输入上界校验族，均无重号。

## 2026-11-04 续查（并行批 O）

> 范围：本轮阅读 3 页（`tools/marketing/marketing-cpc-calculator.html`、`tools/marketing/marketing-roi.html`、`tools/marketing/utm-builder.html`）。仅源码 + `node -e` 内存复算，未开浏览器/未做 EN/移动端/门禁验证。

#### 留存/优势建议（营销 3 页）
- CPC 页：① 把当前结果卡（花费/点击/展示/CPC/CTR/CPM）做成“导出本次结果”，现在导出按钮导的是历史表；② 参考表选行业后自动切换 CPC 分级阈值（当前写死 ¥1/3/8，与电商 ¥1.5–5 的口径不符）；③ 历史记录支持勾选 2–3 条做并排对比。
- ROI 页：① 营销/广告/投资三个计算器合并成“渠道对比”视图，同一预算下并列 ROI/ROAS；② 广告页增加“目标 ROI 反推可承受 CPA/CPC”；③ 权重/参数方案命名保存到 localStorage 并支持一键套用。
- UTM 页：① 批量表补 `utm_term`/`utm_content` 两列，与单个生成对齐；② 生成前校验协议/域名、检测重复 `utm_*` 与 `#` 片段；③ 历史按“批量组”聚合，支持一键复制整组并标注渠道。

- 本轮实读 3 页：`tools/marketing/marketing-cpc-calculator.html`、`tools/marketing/marketing-roi.html`、`tools/marketing/utm-builder.html`；新增 8 条（高 2/中 4/低 2）；未覆盖：本轮未读 `tools/marketing` 其余页面及 `tools/sales` 全部页面；MS-N9 与既有 MS-N3 同属“点击超展示”族但页面不同，MS-N6/MS-N11 为本批新族（输入回写自覆盖 / URL fragment 拼接），MS-N7 为 `||` 零值吞没族，均无重号。

## 2026-11-04 续查（并行批 P）

> 范围：本轮阅读 3 页（`tools/marketing/marketing-ctr-calculator.html`、`tools/marketing/marketing-ltv-calculator.html`、`tools/marketing/marketing-google-ads-budget.html`）。仅源码 + `node -e` 内存复算，未开浏览器/未做 EN/移动端/门禁验证。

#### 留存/优势建议（营销 3 页）
- CTR 页：① 增加“点击 ≤ 展示、转化 ≤ 点击”的校验与占比条（与 MS-N14 同批修）；② 结果卡支持“按渠道/素材保存基准 CTR”并做环比；③ 补“目标 CTR 反推所需展示量/点击量”的反算视图。
- LTV 页：① simple 与 detail 两种口径并排展示同一客户，避免用户切模式后无法对照；② 加 CAC 敏感性（CAC ±20% 时 LTV:CAC 与回本周期变化）；③ 支持按新客/复购分群保存多组 LTV 并导出。
- Ads 页：① 补“按目标转化量反推预算/点击”模式（兑现 meta）；② 输出 CPA 与盈亏平衡 ROAS（客单价×毛利率），并标“ROAS 低于该值即亏损”；③ 预设改为“行业 CPC × 转化率”组合并持久化到 localStorage。

- 本轮实读 3 页：`tools/marketing/marketing-ctr-calculator.html`、`tools/marketing/marketing-ltv-calculator.html`、`tools/marketing/marketing-google-ads-budget.html`；新增 8 条（高 2/中 5/低 1）；未覆盖：本轮未读 `tools/marketing` 其余页面及 `tools/sales` 全部页面；MS-N14 与既有 MS-N3（CPM 页）/MS-N9（CPC 页）同属“点击超展示”族但页面不同，MS-N16/MS-N17 与 MS-J3（CAC 页 36 个月回本假设）同属“生命周期写死”族但页面不同，MS-N19 为“全字段无界”新族，MS-N19/MS-N20 与 MS-M5/MS-M6（`marketing-ad-budget-allocator.html`）页面不同，均无重号。

## 2026-11-04 续查（并行批 Q）

> 2026-11-06 静态复核：感叹号已匹配中英文（`tools/marketing/email-subject-line-tester.html:560-564`），且预览正文现参与垃圾词得分（`:537-554`），旧 85 分复算不再适用；示例一致性需用当前默认正文重新核验。
- 问题：深度解析把「【限时】点击领取你的专属优惠券！！！」当作“过长、3 个感叹号、含「领取/免费」类触发词”的低分案例，但该串实际长度 18（未过长）、用的是全角“！”（不触发扣分）、词表里没有“领取”且标题根本没有“免费”，评分器给它 85 分，落在“优秀 👍”档（≥80）。深层原因是全角感叹号不触发扣分、垃圾词扣分被正面词加分抵消。
- 证据：`tools/marketing/email-subject-line-tester.html:314`（深解“低分标题”）、`:535-545`（垃圾词累加）、`:557-560`（仅匹配 ASCII `!` 且数量 >2 才扣 5）、`:581-587`（正面词 +3）、`:592-595`（≥80 判“优秀”）
- 复现：`【限时】点击领取你的专属优惠券！！！` → 字符 18（不扣）、方括号 −2、垃圾词 限时 −3/点击 −8/优惠 −5、全角“！”不触发 −5、正面词“优惠”使 `posPct=80` 再加 +3 → 总分 `85`，输出“优秀 👍”（node 复算）。页面自己的反例被判为优秀。
- 影响：`tools/marketing/email-subject-line-tester.html` 评分主结论与深解/示例直接冲突，用户无法判断该信谁的分数。
- 方案：感叹号检测改为同时匹配全角 `！` 并统计总数量；正面词与垃圾词去重（同一词不得既加又减）；把 `:314` 的示例改为真实低分串（如含“免费/中奖/100%”），或用该串回归测试锁定分数。

> 2026-11-06 静态复核：当前 `scanText = subject + ' ' + preview`，垃圾词检测及扣分已覆盖正文（`tools/marketing/email-subject-line-tester.html:537-554`）；情感与长度仍只按标题，以下「从不参与」为历史证据，未运行回归。
- 问题：页面收集 `previewText` 并渲染到两个预览框，但 `analyze()` 只读取 `subject`；垃圾词、长度、情感、建议全部不看预览正文。真实邮件客户端会同时展示 preheader，垃圾过滤也会扫描它。
- 证据：`tools/marketing/email-subject-line-tester.html:193-194`（输入与 `oninput="analyze()"`）、`:470-595`（`analyze()` 内仅出现 `subject`，无 `previewText`）、`:485-488`（预览框使用 preview）
- 复现：标题“会议纪要”，预览正文填“免费 中奖 !!!”——分数、垃圾词命中、情感三项与留空预览完全一致（源码核对 + 逻辑复算）。
- 影响：`tools/marketing/email-subject-line-tester.html`。用户以为补全预览正文能提高检测覆盖，实际该字段只影响下方 mock 预览的展示。
- 方案：检测文本改为 `subject + ' ' + previewText`（长度分仍只对标题）；或把该字段改名“预览正文（仅展示）”，避免被当作检测输入。

#### 留存建议（营销 3 页）

**留存建议（tools/marketing/ad-roi.html）**
- 把三种 ROI 口径合成一个可切换的下拉（利润/总成本、广告毛利/花费、毛利/预算），结果卡同步显示所选公式与分子分母，避免同屏三个数。
- 盈亏平衡区补“保本转化数/保本客单价/保本 ROAS”三件套，并加入固定成本灵敏度（0/当前值/2 倍）并列对比。

**留存建议（tools/marketing/email-subject-line-tester.html）**
- 评分卡改成“100 分构成条”：长度/垃圾词/标点/情感各扣多少分逐项展开，点每一项可高亮标题中的命中片段。
- 增加“Gmail 桌面/iPhone 收件箱”两种真实像素宽度截断预览（按 CSS `ch` 或 canvas 测宽），并把预览正文纳入垃圾词扫描。

**留存建议（tools/marketing/marketing-utm-builder.html）**
- 生成前先解析 URL（协议/域名/查询/锚点），自动把参数插到 `?` 与 `#` 之间，并对已有 `utm_*`、大小写重复给出“将覆盖”的确认。
- 增加多行批量模式（每行一组 source/medium/campaign），一次生成 N 条并导出 CSV，兑现深度解析 `:191` 的“批量生成”承诺。

### 承诺 vs 实际（Q 批专项）

- `tools/marketing/ad-roi.html:10` 宣称“盈亏平衡点”，实际只有 `:320-325` 的 ROAS 阈值，没有保本单量/保本销售额；`:140` 宣称“调整 CTR 即可比较”，CPC 模式下 CTR 不进 ROI（见 MS-N25）。
- `tools/marketing/email-subject-line-tester.html:10` 宣称“帮助提升邮件打开率与送达率”，`:187` 副标题写“likely open rate”，但 `:470-595` 只有关键词启发式打分，无打开率预测、无 SPF/DKIM/垃圾过滤送达率检测；`:682-684` 宣称“多维度数据分析/图表可视化”，页面无任何图表元素。
- `tools/marketing/marketing-utm-builder.html:191` 宣称“批量生成多活动链接导入投放后台”，实际只有 `:241-265` 的单链接生成；`:442` 宣称“图表可视化”，但 `:338-342` 用 `parseFloat` 解析以“生成的UTM追踪链接：”开头的结果串恒为 NaN，图表永不渲染；`:440` “多维度数据分析”仅有单条链接输入。

### 覆盖
- 本轮实读 3 页：`tools/marketing/ad-roi.html`、`tools/marketing/email-subject-line-tester.html`、`tools/marketing/marketing-utm-builder.html`。
- 新增 11 条：高 5（MS-N22/23/24/26/29）、中 6（MS-N25/27/28/30/31/32）、低 0。
- 未覆盖：本轮未读 `tools/marketing` 其余页面及 `tools/sales` 全部页面；MS-N29 与既有 MS-N11（`utm-builder.html`）同属“fragment 拼接”族但页面不同，MS-N22/23/24 为“ROI 口径/保本判定”新族，其余为评分词表、必填校验、内联转义族，均无重号。
- 未做浏览器实测、英文态（`?lang=en-US`）核对、移动端视口验证与门禁运行；金额/比率均由 node 按源码同式复算。

#### 留存建议（R 批 3 页）

**留存建议（tools/marketing/calc-price-elasticity.html）**
- 在 `calc()` 中统一 `elasticity(p1,q1,p2,q2)` 返回 `{ed, defined}`，`dP=0` 或 `q1=q2` 时输出“弹性无定义”，并由同一函数生成表格/图表/深解算例，杜绝 100/0 分叉。
- 深解算例改为中点法实算值（−1.7027、−0.3198）并把收入 106700 写进页面；参考表去掉负号或统一注明“取绝对值”。

**留存建议（tools/marketing/cpc-calculator.html）**
- 预算分配在输入合计≠100% 时显示“合计 X%，已按比例归一”：表内“占比”用 `c.ratio/totalRatio*100`，并补“剩余/超出”提示；否则禁止分配。
- 统一入口校验：预算、单价、CTR/CVR、目标转化、CPA、客单价 >0，毛利率 0–100；不合规时在结果区给红色错误，不写历史。

**留存建议（tools/marketing/funnel-calculator.html）**
- 抽一个 `rate(prev,val)` 返回 `null`（`prev<=0`），summary/visual/CSV 共用，0 级显示“—/不可计算”，不再用 100 兜底。
- 增加“流失人数=prev-val”列并按降序高亮 Top1 瓶颈，同步在结果卡显示“最大流失环节 + 流失人数”，兑现 meta。

### 承诺 vs 实际（R 批专项）

- `tools/marketing/calc-price-elasticity.html:10`、`:123` 宣称“采用弧弹性（中点法）…给出定价策略建议”，`:166-183` 核心计算已实现；但 `:386-387` 两个深解算例仍用简单百分比、`:387` 收入写成 113300，`:351` 参考表又给公式加负号，形成三处口径冲突（见 MS-N33/N35）。
- `tools/marketing/cpc-calculator.html:10` 宣称“在 CPC/CPM/CPA 间换算…估算投放效果”，`:399-428`、`:514-534` 三种计费换算与效果估算已实现；但 `:483` 按合计归一分配而 `:491`/`:503` 仍显示输入占比，“预算分配”的承诺与实际分配不一致（见 MS-N36），且全页无正数范围校验（MS-N37）。
- `tools/marketing/funnel-calculator.html:10`、`:15` 宣称“定位转化流失瓶颈”，`:454-468` 只输出各级环比/总体转化率，`:459` 仅按 <50% 标红，未计算流失人数和最大流失环节；深解 `:307` 的“最严重”是人工结论（见 MS-N39）。

### 覆盖
- 本轮实读 3 页：`tools/marketing/calc-price-elasticity.html`、`tools/marketing/cpc-calculator.html`、`tools/marketing/funnel-calculator.html`。
- 新增 8 条：高 1（MS-N33）、中 5（MS-N34/36/37/38/39）、低 2（MS-N35/40）。
- 未覆盖：本轮未读 `tools/marketing` 其余页面及 `tools/sales` 全部页面；MS-N35 为“同页符号/口径矛盾”新族，MS-N36/37 为“占比归一化/范围校验”新族，MS-N38/39 为“零值兜底分叉/瓶颈未实现”新族，均无重号。
- 未做浏览器实测、英文态（`?lang=en-US`）核对、移动端视口验证与门禁运行；金额/比率/弹性均由 node 按源码同式复算。

## 2026-11-06 静态续审：营销工具第 418–423 页

- **历史结论状态更新**：MS-M5 所述负比例现已由 `marketing-ad-budget-allocator.html:254-257` 拒绝，非 100% 合计也在 `:259-262` 明示归一化；仍需运行回归，MS-M6 的手动比例而非智能分配逻辑仍在。MS-J3 所述回收期不展示已过时：`marketing-cac-calculator.html:463-465` 已展示回收期并声明 36 个月假设。MS-N38 的表格/图表/CSV 零分母不一致仍在，MS-N60 的 A 组零转化守卫仍在；MS-F7 目标利润率不可达时无说明仍在。
- 本批共阅读 `funnel-calculator`、`marketing-ab-test-significance`、`marketing-ad-budget-allocator`、`marketing-break-even-roas`、`marketing-cac-calculator`、`marketing-chinese-hashtag-generator` 6 页；仅源码分析，未运行页面、注入或浏览器，未计入双跑。

## 2026-11-06 静态续审：营销工具第 424–429 页

- **历史结论状态更新**：MS-J4（期末超过期初加新增）、MS-J5（转化超过访问）、MS-J7（折后价或优惠超原价）、MS-M1（零折及越界）、MS-N3（点击超过展示）和 MS-J2（新增客户超过点击及毛利率越界）原述计算路径已分别加入校验；`marketing-coupon-discount.html:380-398` 区分空值与零值并由计算和保存共用校验。上述结论仅按源码更新，未做运行回归；优惠券按订单减一次仍是现行计算，公式框须另对照。
- 本批共阅读 `marketing-churn-rate`、`marketing-conversion-rate-calculator`、`marketing-coupon-discount`、`marketing-cpa-calculator`、`marketing-cpm-calculator`、`marketing-discount-rate` 6 页；仅源码分析，未运行浏览器，不计双跑。

## 2026-11-06 静态续审：营销工具第 430–435 页

- **历史结论状态更新**：MS-N78 所述互动数负值现由 `marketing-engagement-rate.html:245-247` 拦截；MS-M3 的包邮毛利率缺失及越界现由 `marketing-free-shipping-threshold.html:244-255` 拦截；MS-F8 的 LTV 零值路径现被拒绝，回本周期已标明按 36 个月分摊（`marketing-ltv-cac-ratio.html:422-424,456`）。仅按源码确认，未做运行回归。Google 广告负数输入、达人报价参数缺校验、关键词混排口径的既有关键路径仍在。
- 本批共阅读 `marketing-engagement-rate`、`marketing-free-shipping-threshold`、`marketing-google-ads-budget`、`marketing-influencer-pricing`、`marketing-keyword-density`、`marketing-ltv-cac-ratio` 6 页；仅源码分析，未运行浏览器，不计双跑。

## T 批收口

- 本轮审计 13 页：`market-share`、`estimate-sample-size-confidence`、`marketing-ab-test-significance`、`price-elasticity`、`tagline-generator`、`hashtag-generator`、`slogan-generator`、`social-media-image-sizes`、`marketing-chinese-hashtag-generator`、`calc-1`、`assessor-65`、`marketing-price-elasticity`、`marketing-engagement-rate`（均在 `tools/marketing/`）。
- 新增 24 条（高 20 / 中 4）：MS-N55～MS-N78；假工具候选 4 页（`tagline-generator` C、`hashtag-generator` C、`slogan-generator` A、`marketing-chinese-hashtag-generator` A）。
- 数值均由 `node -e` 按源码同式复算：样本量 271/664、A/B z=2.9737/p=0.00294、中点弹性 -1.727/-1.703、ROAS 盈亏平衡 1.667、评估分 -790.75、互动率 4.4%、HHI 5800/970。
- 未做浏览器、门禁、线上与英文态验证；仅静态阅读 + node 复算。
