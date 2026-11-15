# 营销/销售 · tools/{marketing,advertising,sales}（~70 页）

- `node scripts/verify_marketing_calc.js utm-builder` 为 2/2；此为 DOM 桩及函数级验证，未验证浏览器实际复制/下载；其他既有问题不在本项复核范围。

## 2026-11-06 公关评估和流程静态续审

- `tools/pr/assessor-58.html:223-239,253-259`：合作费和曝光单位均为万，CPM 应为 `cost/expo*1000`，现乘 10000，高 10 倍；默认 5 万元/100 万次应 50 元，页面为 500 元并提示偏高。曝光为 0 时 CPM 和单粉成本都显示 0，后者虽有粉丝分母却错误依赖曝光；清空必填项只改结果文本，旧 `dataset.copyValue` 仍可被复制。
- `tools/pr/assessor-59.html:173-185`：报道、核心报道和曝光空值按 0，无核心报道不超过总报道的校验；总报道 10、核心 20 显示占比 200%，总报道 0 时占比强行显示 0%。评分本身只用三个下拉项。
- `tools/pr/press-conference.html:278-285,288-312,315-378,406`：`renderSteps()` 与 `render()` 都写 `flowList`，初始化及添加环节后前者的编辑表单立刻被后者覆盖，正常路径无法编辑、删除或排序环节；开始时间清空后又按 14:00 排程。模板切换会覆盖原步骤且无确认。
- `tools/pr/media-invite.html:252-267,283-303,369-383`：名单仅存于内存，加载示例和清空直接覆盖现有名单；导出前无持久化。名称和联系人渲染使用转义；未验证实际导出。
- `tools/pr/assessor-56.html:123,169-184`、`assessor-57.html:124,170-185`、`assessor-manager-2.html:124,170-189`、`assessor-risk.html:128,174-192`：下拉变化触发分数或风险矩阵重算，默认分别取各选项首项并立即显示结论；风险页默认全部最低风险不等于已完成评估。均为静态分析，未运行浏览器。

## 2026-11-06 公关工具静态续审

- `tools/pr/analysis-6.html:206-238`：词典逐项匹配，不处理否定及上下文；例如「不推荐」仍命中正向「推荐」，结果为正面倾向。应明确标注词典统计局限，不宜作为可靠情感判断。
- `tools/pr/analysis-assessor.html:203-232`：输入行中权益名 `r.n` 未转义即拼入表格和最高权益的 `innerHTML`，存在 HTML 注入风险，未实际执行注入；无效行被静默丢弃，零或负投入时 ROI 被记为 0，仍给「基本回本」结论，应提示行错误并处理分母边界。
- `tools/pr/analysis-density-1.html:211-237`：关键词计数先区分大小写，只有完全未命中才转小写重算；正文 `Apple apple`、关键词 `Apple` 只统计 1 次而非 2 次。应统一不区分大小写或明确模式。三个页面均以输入事件触发计算；仅源码分析，未运行页面。

## 功能缺陷
- ROI 页缺「多渠道对比表」（同预算分三渠道敏感性）。
- 广告缺「A/B 测试显著性判定」（样本量+转化率→p 值，纯前端可算）。

## 优化点
- ✅ S2 场景（2026-10-26）：ad-roi 加「抖音千川」预设按钮（CPM 模式 预算1万/CPM45/CTR1.8%/CVR4%/客单260/毛利45% ⇒ ROAS 4.16 / ROI 26.5%）；funnel-calculator 加「私域 SOP」模板（进群2万→加微1200→首单180→复购45）。verify marketing 117→118、判别器 0 逃生、Playwright 真机 zh 正常 + EN 零 CJK、门禁 218/218。
- S3 分步：盈亏平衡点图解。

## 受影响范围
- tools/marketing/（46）、tools/advertising/、tools/sales/

## 进度
- 🟡 续批中（S2 已落地；剩余：多渠道对比表 / A-B 显著性缺口确认 / S3 盈亏平衡图解）

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

## 2026-11-04 续查（并行批 S）

- 问题：标题、摘要、功能介绍宣称基于 Interbrand 的 7 维品牌审计/评分，实际只输入一个“品牌强度系数”，没有 7 个子项、权重或审计清单；`市场占有率` 只回显，完全不参与估值。
- 证据：`tools/marketing/assessor-51.html:10`（Interbrand 评估思路）、`:123`（structured scorecard / audit maturity）、`:205`/`:232`/`:286`（7 维度）、`:131`（唯一 strength 输入）、`:134`（share 输入）、`:214-232`（calc 只用 `st`，`share` 仅在 `:231` 回显）。
- 复现：node 按 `:218-229` 同式算默认值 → 品牌净利润 3250 万元、调整折现率 13.25%、PV 17460.48 万元；仅把 share 15 改成 90，源码无 share 引用，PV 仍为 17460.48。
- 影响：用户以为完成了“7 维审计/评分”，实际只得到一个线性强度分；SEO 与功能承诺不符。
- 方案：要么补 7 个子评分（每维 0–10 + 权重）并加权成 strength，输出维度得分/雷达图/缺失项清单；要么把标题、meta、功能列表收窄为“单系数品牌资产估值”，删除 7 维与审计表述，并移除 share 或让它进入市场地位调整。

- 问题：深解写“强度 0.8、折现率 10%、5 年 → 品牌资产现值约 1137 万元”，但源码先按 `adjustedDiscount=dr/100+(1−st)×0.05` 得 11%，PV 应为 1108.77；1137 是按 10% 直接折现、未加强度调整的结果。
- 证据：`tools/marketing/assessor-51.html:165`（1137 万元算例）、`:220-222`（调整折现率与折现循环）。
- 复现：node → `300×Σ(1.11^-i, i=1..5)=1108.77`；若按 1.10 折现才得 1137.24，差 28.47 万元。
- 影响：页面示例不可复现，用户用计算器对照会得到不同答案，损害可信度。
- 方案：示例改为 1108.77；若坚持 1137，则明确标注“不考虑品牌强度调整、按 10% 折现”，并同步公式说明；示例值应由同一段逻辑生成。

- 问题：calc 没有输入守卫；空值用 `||0`/`||1` 静默兜底；贡献率可 >100、强度可 <0 或 >1、折现率可为负、年限可负/0（0 被替换为 1）。
- 证据：`tools/marketing/assessor-51.html:215-222`（取值、兜底、adjustedDiscount、循环）。
- 复现：node → `st=3` 时 adjusted=0.02、PV=29193.40（默认 17460.48）；`st=23.4` 时 adjusted≈−1、PV=1.78e82；contribution=200 时品牌净利润翻倍。清空折现率会变成 1% 而非 12%。
- 影响：明显越界/误输入仍输出“权威”估值，可能被用于投融资沟通。
- 方案：显式校验 contribution 0–100、strength 0–1、discount >0、years 1–50 的整数；违规在结果区报错且不写历史；不要用 `||` 把空值变成 0/1。

- 问题：calc 按粉丝量级硬编码 cpmBase=100/200/300/400/500，50 万粉取 400；深解示例明确“基础千粉价 10 元”，5 万粉 ×10×1.2=600 元。按同系数，50 万粉应约 12375 元，页面默认却给 495000 元。
- 证据：`tools/marketing/marketing-influencer-pricing.html:149`（“粉丝数÷1000×CPM”）、`:152-155`（默认 500000/3/1.5/1.5）、`:248-255`（cpmBase 档位与 engBonus）、深解 `:191`（10 元/千粉、600 元）。
- 复现：node 同式 → `500×400×1.1×1.5×1.5=495000`；按深解 10 元/千粉 → `500×10×1.1×1.5×1.5=12375`，差 40 倍。深解 50k 案例若按页面档位 cpm=200，则 `50×200×1.1=11000`，也不是 600。
- 影响：报价锚点高一个数量级，商务议价直接失真；深解与工具互相打脸。
- 方案：把“千粉单价”改为用户输入（默认 10 元/千粉），粉丝量级只做系数或建议区间；若要保留 CPM，则必须按“预估曝光量”而非粉丝数计算；深解案例与代码共用同一基准表。

- 问题：仅校验 followers/eng 为 NaN 且 followers>0（`:244`）；platformFactor/contentType 为空或负数、eng 为负都不拦截；`engBonus=1+(eng−2)/10` 可为负。
- 证据：`tools/marketing/marketing-influencer-pricing.html:241-255`。
- 复现：node → `eng=−20` 时 engBonus=−1.2、price=−540000 元；platformFactor 留空 → price=NaN；contentType=−1 → 负报价。
- 影响：结果区出现负报价/NaN，用户无法判断是输入错误还是模型结果。
- 方案：eng 限 0–100、platform/content 必须 >0；空值/NaN/负值在结果区报“请填写有效系数”，不输出报价区间。

- 问题：公式把 `粉丝数÷1000×CPM` 称为 CPM，但参考表定义 CPM=报价/预估曝光×1000（千次曝光成本），两者不是同一量纲。
- 证据：`tools/marketing/marketing-influencer-pricing.html:149`、`:188`（“CPM（千粉成本）”）、`:219-220`（参考表 CPM 定义）。
- 复现：静态对照：源码 `:255` 只用 followers/1000 乘 cpmBase，页面没有“预估曝光/阅读”输入，无法计算真正的 CPM。
- 影响：懂投放的用户会误读，跨工具/跨达人比较口径不一致。
- 方案：改名“千粉报价（元/千粉）”，或增加“预估曝光/阅读”输入按 `:220` 真正算 CPM，并与千粉价分列展示。

- 问题：只要正文含汉字，`totalChinese>0` 就一律用中文字数作分母，英文关键词分子只算 `count×1`；纯英文关键词在中文正文里会被系统性低报。中文只做子串计数，没有分词。正文只要出现 1 个汉字，纯英文内容也会切到中文字数分母，密度反而暴增。
- 证据：`tools/marketing/marketing-keyword-density.html:247-259`（尤其 `:257-259` 的注释与实际公式）、`:216`（参考表写“按分词后的出现次数统计”）。
- 复现：node → 500 个汉字中含 5 次“SEO”：`:259` 得 `5×1/500=1.00%`；按字符密度 `5×3/515=2.91%`，低报约 3 倍；若关键词是 15 字符英文短语则低报 15 倍。
- 影响：SEO 健康/堆砌判断错误，用户可能误删内容或继续堆词。
- 方案：按内容主语言选择分母；统一为“关键词字符数/参与统计的总字符数（含中英文数字）”，中文短语用 `keyword.length`、英文单词用整词匹配；页面明示“不做中文分词”，或引入 `Intl.Segmenter('zh',{granularity:'word'})` 提供分词模式。

- 问题：公式框写“1% 至 2.5%”，深解、参考表、结果文案写“1%–3%”，代码判读也用 1–3。
- 证据：`tools/marketing/marketing-keyword-density.html:152`、`:190`、`:221`、`:260`、`:269`。
- 复现：静态检索：`2.5%` 仅出现在 `:152`；`1%-3%` 出现在 `:190`/`:260`/`:269`。以 density=2.8% 跑 `:260` 得“✅ 密度健康”，按 `:152` 已超上限。
- 影响：同一页面给出相反建议。
- 方案：抽 `DENSITY_MIN/MAX` 常量并全页引用；确定采用 1–3 或 1–2.5，深解与参考表同步。

- 问题：深解场景与示例要求录入 30 篇笔记的赞、藏、评、粉，算篇均互动、爆款占比、赞粉比；页面只有一个正文 textarea，没有任何点赞/收藏/评论/粉丝输入或汇总表。
- 证据：`tools/marketing/xiaohongshu-counter.html:391-399`（多笔记/赞粉比深解）、`:127-131`（唯一 textarea 与单一上限）、`:229-246`（calc 只数字符/行/词/话题）。
- 复现：静态：`document.querySelectorAll('input,textarea')` 只有 `#text` 与 `#limit`；深解 `:398` 的 45000/6000/8000 无对应字段，node 无法按该案例构造输入。
- 影响：核心承诺未实现，深解与工具能力错位，属于典型“内容先行、功能未落地”。
- 方案：二选一：① 新增多笔记表格（每行赞/藏/评/粉），汇总篇均互动、赞粉比、爆款占比；② 把深解整段改写为字数、话题、表情统计，删除多笔记与赞粉比表述。

- 问题：meta 说统计“标题与正文字符数”，页面只有正文 textarea 和一个 1000 上限，标题 20 字规则未体现。字符直接用 `text.length`，代理对/ZWJ/旗帜 emoji 被算成 2/11/4 个字符。
- 证据：`tools/marketing/xiaohongshu-counter.html:43`、`:128-131`、`:232`、`:151`、`:156-157`。
- 复现：node → `'😀'.length=2`、`'👨‍👩‍👧‍👦'.length=11`、`'🇨🇳'.length=4`；若平台按 1 个表情计，50 个 emoji 会虚增 50–500 字符，提前报“超出”。
- 影响：标题合规无法检查；emoji 文案误报超限。
- 方案：拆“标题（20 字）/正文（1000 字）”两个输入与各自计数；用 `[...text].length` 或 `Intl.Segmenter` 按字素簇计，并标注“emoji 按 1 个计”，可另留 UTF-16 技术计数。

- 问题：正则 `/#[^#\s]+/g` 不含全角 `＃`；`Number(value)||1000` 把 0/NaN/负数都当 1000。
- 证据：`tools/marketing/xiaohongshu-counter.html:234-235`。
- 复现：node → `'＃秋日穿搭'.match(/#[^#\s]+/g)` 为 null（0 个），`'#a #b'` 为 2；把上限填 0，`:235` 得 1000，仍按 1000 判剩余。
- 影响：手机中文键盘常用全角＃，话题数偏少；上限 0 无法表达“不允许正文”的校验。
- 方案：正则改 `[#＃]`；上限用 `Number.isFinite` + `>0` 校验，0/负数报错而非兜底 1000。

- 问题：meta、正文、深解都说统计线下物料扫码效果、对比各码扫码与转化；实际输入只有 URL/source/location/campaign/qrId，输出只有追踪链接和二维码图，没有扫码数、转化数、汇总或渠道对比。
- 证据：`tools/marketing/marketing-qr-campaign-tracker.html:10`、`:145`、`:188-193`、`:239-266`。
- 复现：静态：`#result` 只插入 `<img>`、trackUrl 与复制按钮（`:259-266`）；源码没有 `scan`/`conversion`/“扫码”输入；深解 `:192-193` 的 1200/800/300、60/120 无字段可填。
- 影响：用户按“追踪器”使用拿不到任何活动数据；SEO 承诺落空。
- 方案：要么增加“每个码的曝光/扫码/转化”手工录入与汇总（localStorage 持久化），输出扫码率、转化率、渠道对比；要么把标题/meta/深解收窄为“UTM 二维码生成器”，删除统计与转化案例。

- 问题：结果图 `src` 把含 campaign/location/qr_id 的完整 trackUrl 编码进第三方 API 查询串；打开页面即发起外部请求，第三方可见落地页与活动参数。meta 仍称“纯前端运行、数据不上传”。
- 证据：`tools/marketing/marketing-qr-campaign-tracker.html:258-261`（第三方 API 与 `<img src>`）、`:10`（数据不上传）。
- 复现：`node -e 'const t="https://a.com/p?utm_source=x&location=y"; console.log("https://api.qrserver.com/v1/create-qr-code/?size=200x200&data="+encodeURIComponent(t))'` → 输出 query 内含完整链接；页面无本地二维码库。
- 影响：违反项目纯前端/数据不外发约束；活动链接（可能含未公开落地页、门店编号）泄露给第三方，离线或被墙时二维码不显示。
- 方案：内置本地二维码生成（打包 qrcode 库或 canvas 实现），禁止运行时第三方请求；若短期保留，必须明示第三方并移除敏感参数，长期替换。

- 问题：`sep` 只看 `?` 不看 `#`，`https://x/p#top` 会拼成 `...#top?utm_...`，参数进不了服务端。已有 `utm_source` 时直接追加同名参数；公式承诺 `utm_term/utm_content` 但无输入；trackUrl 未转义直接进 innerHTML，onclick 的 `replace(/'/g,"\'")` 是无效转义（`\'` 等于 `'`）。
- 证据：`tools/marketing/marketing-qr-campaign-tracker.html:149`、`:151-156`、`:250-257`、`:264-265`。
- 复现：node → `new URL('https://example.com/p#top?utm_medium=qrcode&utm_source=x')` 得 `search=''`、`hash='#top?utm_medium=qrcode&utm_source=x'`，`searchParams.get('utm_source')` 为 null；base 已有 `?utm_source=a` 时输出两个同名参数。
- 影响：最常见的锚点落地页追踪全部失效；重复参数让分析平台取值不确定；含引号/尖括号的 campaign 可破坏复制按钮或注入 DOM。
- 方案：用 `new URL(baseUrl)`，保留/写回 `hash`，统一操作 `searchParams`（自动去重/编码）后 `toString()`；补 term/content 输入或删公式表述；输出用 `ToolBox.escHtml`，复制按钮用事件绑定而非内联 onclick。

#### 留存建议（S 批 5 页）

**留存建议（tools/marketing/assessor-51.html）**
- 若保留“审计”定位：新增 7 维评分表（每维 0–10 + 权重），`strength=加权和/10`，输出维度得分、雷达图与缺失项清单；否则删除 `:205`/`:232`/`:286` 的 7 维文案，标题改为“品牌资产估值（单系数）”。
- 补范围校验与空值报错；`share` 要么进入市场地位调整（如按份额对 strength 加减分），要么删除输入与 `:231` 回显。
- 深解算例改用 `:220-222` 的实算值 1108.77，示例数字由脚本生成，避免再次手写。

**留存建议（tools/marketing/marketing-influencer-pricing.html）**
- 把“千粉单价”做成输入（默认 10 元/千粉），粉丝量级只给建议系数/区间；删除硬编码 100–500 或改成可配置基准表，确保深解 `:191` 与 `:248-255` 同源。
- 校验 eng 0–100、platform/content >0；负值/空值报错，不输出负报价；结果区同时给“报价区间 + 千粉价 + 按曝光计的 CPM”，避免术语混淆。
- 可选：增加预算、预估曝光、转化率、客单输入，给“性价比/ROI”一个可计算口径，而不只比较粉丝数。

**留存建议（tools/marketing/marketing-keyword-density.html）**
- 抽 `density()` 纯函数：按内容主语言选分母，中文短语用字符、英文用整词，分母包含中英文数字；结果区显示“当前分母口径”。
- 统一阈值常量与文案（1–3 或 1–2.5）；在结果卡标明采用哪一档。
- 若要支持分词，提供“分词模式/字符模式”切换，并说明 `Intl.Segmenter` 的切分口径。

**留存建议（tools/marketing/xiaohongshu-counter.html）**
- 拆标题/正文两栏：标题上限 20、正文上限 1000（可改），各自计数与超限提示；话题、链接单列。
- 字符计数改字素簇（`[...text]` 或 `Intl.Segmenter`），结果注明“emoji 按 1 个计”；UTF-16 计数可作为可选技术口径。
- 若保留 `:391-399` 深解，新增多笔记表（赞/藏/评/粉）与篇均、赞粉比、爆款占比；否则整段改写为字数规则。

**留存建议（tools/marketing/marketing-qr-campaign-tracker.html）**
- 若保留“追踪器”：增加曝光/扫码/转化手工录入，按 `qr_id` 汇总扫码率、转化率、渠道对比，localStorage 持久化；深解案例改为可填字段。
- 二维码改本地生成（qrcode 库或 canvas），移除 `api.qrserver.com`，页面明示“所有数据留在浏览器”。
- 链接拼接改用 `new URL` + `searchParams`，处理 `#`、去重、补 term/content 或删公式；输出统一 `escHtml` 与事件绑定复制。

### 承诺 vs 实际（S 批专项）

- `tools/marketing/assessor-51.html:10`/`:123`/`:205` 宣称 Interbrand 7 维评分与品牌审计，实际 `:131` 只有一个 strength 系数、`:134` 的 share 仅在 `:231` 回显，`:214-232` 无 7 维加权；深解 `:165` 的 1137 也与 `:220-222` 的 1108.77 不符（见 MS-N41/N42）。
- `tools/marketing/marketing-influencer-pricing.html:149` 宣称按 CPM 估算报价，`:248-255` 实际用 100–500 元/千粉，深解 `:191` 却用 10 元/千粉，默认输出 495000 元 vs 同系数 12375 元（见 MS-N44）；`:241-255` 无负值/空值校验（MS-N45）。
- `tools/marketing/marketing-keyword-density.html:152` 写 1%–2.5%，`:190`/`:221`/`:260`/`:269` 写 1%–3%；`:247-259` 的混排分母导致英文词低报，且 `:216` 宣称“按分词”但实际只做子串计数（见 MS-N47/N48）。
- `tools/marketing/xiaohongshu-counter.html:43` 宣称统计“标题与正文”，实际 `:128-131` 只有正文与单一上限；深解 `:391-399` 的多笔记赞藏评粉/赞粉比在 `:229-246` 无任何实现（见 MS-N49/N50）。
- `tools/marketing/marketing-qr-campaign-tracker.html:10`/`:145`/`:188-193` 宣称统计扫码与转化，实际 `:239-266` 只生成链接/图片；`:258-261` 又把 trackUrl 发给第三方 `api.qrserver.com`，与 `:10` 的“数据不上传”冲突（见 MS-N52/N53）；`:256` 未处理 `#`（MS-N54）。

### 覆盖

- 本轮实读 5 页：`tools/marketing/assessor-51.html`、`tools/marketing/marketing-influencer-pricing.html`、`tools/marketing/marketing-keyword-density.html`、`tools/marketing/xiaohongshu-counter.html`、`tools/marketing/marketing-qr-campaign-tracker.html`。
- 新增 14 条：高 5（MS-N41/44/49/52/53）、中 6（MS-N42/43/45/47/50/54）、低 3（MS-N46/48/51）。
- 未覆盖：本轮未读 `tools/marketing` 其余页面及 `tools/sales` 全部页面；MS-N41 为“多维度/审计承诺未实现”族，MS-N44 为“基准单价与深解差一个数量级”族，MS-N52 为“追踪器无追踪”族，均与既有编号无重号。
- 未做浏览器实测、英文态（`?lang=en-US`）核对、移动端视口验证与门禁运行；金额/比率/密度均由 node 按源码同式复算，二维码 fragment 用 `new URL()` 验证。

## 2026-11-06 静态续审：营销工具第 418–423 页

- **历史结论状态更新**：MS-M5 所述负比例现已由 `marketing-ad-budget-allocator.html:254-257` 拒绝，非 100% 合计也在 `:259-262` 明示归一化；仍需运行回归，MS-M6 的手动比例而非智能分配逻辑仍在。MS-J3 所述回收期不展示已过时：`marketing-cac-calculator.html:463-465` 已展示回收期并声明 36 个月假设。MS-N38 的表格/图表/CSV 零分母不一致仍在，MS-N60 的 A 组零转化守卫仍在；MS-F7 目标利润率不可达时无说明仍在。
- **中文话题输入进入 HTML 和内联脚本，存在注入及复制损坏风险**：`marketing-chinese-hashtag-generator.html:241-243,258-276` 将关键词和行业直接拼入 `innerHTML` 的标签文本、单标签 `onclick` 字符串和全部复制按钮模板字面量，无 HTML 或 JS 上下文转义。含单引号、反引号或 HTML 标记的用户输入可破坏对应结构；潜在脚本注入仅由源码推断，未执行攻击或验证可利用性。建议用文本节点渲染并通过事件监听器绑定复制值。
- **零预算和零获客成本的除数未定义**：`marketing-ad-budget-allocator.html:250-267,272,281` 允许预算为 0，收入也为 0，整体 ROAS 的 `0/0` 最终被替换为 `—`；`marketing-cac-calculator.html:409-428,455-465,489-505` 允许营销和销售费用同时为 0，LTV 存在时比率及 ROI 除以零、替换为 `—` 却仍显示“健康”，LTV 留空时费用占比也是 `0/0`。应保留零成本的 CAC，明确相关比率不可计算并避免给出健康结论。
- **CAC 保存校验与计算不一致**：`marketing-cac-calculator.html:413-420,508-525` 的计算会拒绝负费用和非正 LTV，但保存仅检查数值及客户数；因此无效费用或 LTV 仍可存历史，历史列表还会根据无效 CAC 分级。应共用校验逻辑。
- 本批共阅读 `funnel-calculator`、`marketing-ab-test-significance`、`marketing-ad-budget-allocator`、`marketing-break-even-roas`、`marketing-cac-calculator`、`marketing-chinese-hashtag-generator` 6 页；仅源码分析，未运行页面、注入或浏览器，未计入双跑。

## 2026-11-06 静态续审：营销工具第 424–429 页

- **历史结论状态更新**：MS-J4（期末超过期初加新增）、MS-J5（转化超过访问）、MS-J7（折后价或优惠超原价）、MS-M1（零折及越界）、MS-N3（点击超过展示）和 MS-J2（新增客户超过点击及毛利率越界）原述计算路径已分别加入校验；`marketing-coupon-discount.html:380-398` 区分空值与零值并由计算和保存共用校验。上述结论仅按源码更新，未做运行回归；优惠券按订单减一次仍是现行计算，公式框须另对照。
- **保存历史绕过计算校验**：`marketing-churn-rate.html:393-401,475-487`、`marketing-conversion-rate-calculator.html:398-405,491-502`、`marketing-cpa-calculator.html:429-439,567-580`、`marketing-cpm-calculator.html:402-405,490-500`、`marketing-discount-rate.html:436-465,531-554` 的保存路径均缺少部分计算约束。例如期初 100、期末 150、新增 0 在流失页显示口径错误，但历史仍可存流失率 -50%；折后价高于原价也可存负折扣。应让保存与计算共用同一校验。
- **折扣页清空数值被当成 0**：`marketing-discount-rate.html:429-431,442-444,455-457` 对折扣率、折后价、优惠额使用 `parseFloat(...) || 0`；清空折后价会直接得到 0 元和 100% 优惠，清空折扣率则得到无折扣结果。应区分空串与合法 0，在缺失时停止结果和历史保存。
- **零转化历史 CPA 与当前结果不一致**：`marketing-conversion-rate-calculator.html:407-411,426-430,533-545` 对零转化显示 CPA 不可计算，但历史列表仍将花费除以零并把 `Infinity` 替换为 `—`，未附不可计算原因；且花费大于 0、收入为 0 时 ROI 卡被隐藏，不能呈现零收入对应的亏损。应区分输入缺失与真实零收入并统一结果与历史口径。
- **零花费边界处理有缺口**：`marketing-cpm-calculator.html:398-400` 把 0 花费当无效，尽管展示量非零时 CPM 为 0；`marketing-cpa-calculator.html:449-450,464-485` 对 0 花费强制 ROI 为 0，并在客单和毛利均正时显示 `+0.0%`，而该 ROI 的分母为 0。应分别保留可算的零成本与标注不可计算的比率。
- 本批共阅读 `marketing-churn-rate`、`marketing-conversion-rate-calculator`、`marketing-coupon-discount`、`marketing-cpa-calculator`、`marketing-cpm-calculator`、`marketing-discount-rate` 6 页；仅源码分析，未运行浏览器，不计双跑。

## 2026-11-06 静态续审：营销工具第 430–435 页

- **历史结论状态更新**：MS-N78 所述互动数负值现由 `marketing-engagement-rate.html:245-247` 拦截；MS-M3 的包邮毛利率缺失及越界现由 `marketing-free-shipping-threshold.html:244-255` 拦截；MS-F8 的 LTV 零值路径现被拒绝，回本周期已标明按 36 个月分摊（`marketing-ltv-cac-ratio.html:422-424,456`）。仅按源码确认，未做运行回归。Google 广告负数输入、达人报价参数缺校验、关键词混排口径的既有关键路径仍在。
- **关键词正文只有标点时仍给密度结论**：`marketing-keyword-density.html:243-260` 仅判断内容非空，标点正文经清洗后 `totalWords=0`；例如正文 `!!!`、关键词 `a`，密度为 `0/0`，展示时替换成 `—`，但比较 NaN 均不成立，最终建议“密度过高”。应在分母为零时说明缺少可统计内容，不输出评价。
- **互动数清空被当作零**：`marketing-engagement-rate.html:233-249` 的点赞、评论、分享通过 `parseFloat(...) || 0` 处理；清空这三个字段仍按零生成总互动及互动率。展示量标为可选，其他字段若为必填应区分空串与合法 0，避免缺失数据被解释为零互动。
- **目标日点击为 0 时 ROAS 无定义**：`marketing-google-ads-budget.html:244-263` 允许日点击为 0，日预算与收入均为 0，`0/0` 被替换为 `—x` 而没有说明。应保留零预算及零收入，并明确 ROAS 不可计算；负值和转化率越界的既有问题见历史记录。
- 本批共阅读 `marketing-engagement-rate`、`marketing-free-shipping-threshold`、`marketing-google-ads-budget`、`marketing-influencer-pricing`、`marketing-keyword-density`、`marketing-ltv-cac-ratio` 6 页；仅源码分析，未运行浏览器，不计双跑。

## T 批收口

- 本轮审计 13 页：`market-share`、`estimate-sample-size-confidence`、`marketing-ab-test-significance`、`price-elasticity`、`tagline-generator`、`hashtag-generator`、`slogan-generator`、`social-media-image-sizes`、`marketing-chinese-hashtag-generator`、`calc-1`、`assessor-65`、`marketing-price-elasticity`、`marketing-engagement-rate`（均在 `tools/marketing/`）。
- 新增 24 条（高 20 / 中 4）：MS-N55～MS-N78；假工具候选 4 页（`tagline-generator` C、`hashtag-generator` C、`slogan-generator` A、`marketing-chinese-hashtag-generator` A）。
- 数值均由 `node -e` 按源码同式复算：样本量 271/664、A/B z=2.9737/p=0.00294、中点弹性 -1.727/-1.703、ROAS 盈亏平衡 1.667、评估分 -790.75、互动率 4.4%、HHI 5800/970。
- 未做浏览器、门禁、线上与英文态验证；仅静态阅读 + node 复算。
