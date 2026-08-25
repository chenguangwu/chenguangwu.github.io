# N3 高价值指南扩容 · 选题池与落地账本

> 制定：2026-08-20  
> 来源：NEXT-DEV-PLAN.md 第 9 章（N3-01 选题池 + N3-02 指南开发）  
> 目标：指南从现有 55 篇扩展到 ≥80 篇（本池 25 篇 + 现有 55 篇 = 80 篇）  
> 数据说明：无实时 GSC 流量数据，选题依据为「功能复杂度 + 用户常见问题 + 跨行业覆盖 + 与现有指南无主题重复」。

## 选题统计

| 维度 | 值 |
|---|---|
| 选题总数 | 25 |
| 覆盖行业数 | 11（accounting / banking / science / health / fitness / design / biz / realestate / securities / automotive / baking） |
| 单行业最多 | science = 5（≤8 ✓） |
| 与现有 55 篇重复 | 0（已逐条比对 title/slug/工具 URL） |
| 全部映射到真实工具 | 25/25（已校验 `tools/<ind>/<base>.html` 存在且入索引） |

## 选题明细（25 条）

批次按 N3-02 落地顺序编排，每批 5 篇。

### 批次 01（金融 + 科学）

| # | 指南 slug | 工具 URL | 主关键词 | 用户问题 | 差异（vs 现有 55 篇） |
|---|---|---|---|---|---|
| 1 | calc-1 | tools/accounting/calc-1.html | 增值税计算 | 当期应纳增值税怎么算？含税价如何反推？ | 现有无税务类指南 |
| 2 | simple-interest | tools/banking/simple-interest.html | 单利利息 | 单利和复利差多少？到期利息怎么算？ | 现有无利息计算指南 |
| 3 | break-even-units | tools/accounting/break-even-units.html | 盈亏平衡产量 | 最少卖多少才不亏本？ | 现有无盈亏平衡指南 |
| 4 | effective-annual-rate | tools/banking/effective-annual-rate.html | 有效年利率 EAR | 名义利率和实际年化差多少？ | 现有无 EAR 指南 |
| 5 | fd-quarterly | tools/banking/fd-quarterly.html | 定期存款按季复利 | 定期到期能拿多少？ | 现有 mortgage 指南不含定期存款 |

### 批次 02（科学）

| # | 指南 slug | 工具 URL | 主关键词 | 用户问题 | 差异 |
|---|---|---|---|---|---|
| 6 | fraction-calculator | tools/science/fraction-calculator.html | 分数计算 | 分数加减乘除/约分 | 现有无分数指南 |
| 7 | gcd-calculator | tools/science/gcd-calculator.html | 最大公约数 | 辗转相除法怎么算 | 现有无 GCD 指南 |
| 8 | lcm-calculator | tools/science/lcm-calculator.html | 最小公倍数 | 通分/周期对齐怎么算 | 现有无 LCM 指南 |
| 9 | quadratic-equation | tools/science/quadratic-equation.html | 一元二次方程 | 求根公式/判别式 | 现有无方程求解指南 |
| 10 | equation-balancer | tools/science/equation-balancer.html | 化学方程式配平 | 反应式怎么配平 | 现有无化学配平指南 |

### 批次 03（健康 + 健身）

| # | 指南 slug | 工具 URL | 主关键词 | 用户问题 | 差异 |
|---|---|---|---|---|---|
| 11 | pregnancy-due-date | tools/health/pregnancy-due-date.html | 预产期计算 | 预产期怎么算？几周了？ | 现有无孕产指南 |
| 12 | water-intake-calculator | tools/health/water-intake-calculator.html | 每日饮水量 | 一天该喝多少水？ | 现有无饮水指南 |
| 13 | heart-rate-zones | tools/health/heart-rate-zones.html | 心率区间 | 有氧心率多少合适？ | 现有 blood-pressure 不同主题 |
| 14 | waist-hip-ratio | tools/health/waist-hip-ratio.html | 腰臀比 | 腹部肥胖怎么判断？ | 现有 BMI/体脂不同指标 |
| 15 | convert | tools/fitness/convert.html | 跑步配速 | 配速和速度怎么换？ | 现有无配速指南 |

### 批次 04（设计 + 商务）

| # | 指南 slug | 工具 URL | 主关键词 | 用户问题 | 差异 |
|---|---|---|---|---|---|
| 16 | favicon-generator | tools/design/favicon-generator.html | Favicon 生成 | 网站图标怎么做？ | 现有 color/qr 不同 |
| 17 | image-compress | tools/design/image-compress.html | 图片压缩 | 图片怎么瘦身不糊？ | 现有无压缩指南 |
| 18 | image-format-converter | tools/design/image-format-converter.html | 图片格式转换 | PNG/JPG/WebP 怎么转？ | 现有无格式转换指南 |
| 19 | text-diff | tools/biz/text-diff.html | 文本差异对比 | 两段文字哪里不同？ | 现有无文本对比指南 |
| 20 | text-extract-urls | tools/biz/text-extract-urls.html | 提取 URL | 从文本批量提取链接 | 现有无提取 URL 指南 |

### 批次 05（商务 + 房产 + 证券 + 汽车 + 烘焙）

| # | 指南 slug | 工具 URL | 主关键词 | 用户问题 | 差异 |
|---|---|---|---|---|---|
| 21 | text-compare | tools/biz/text-compare.html | 文本并排对比 | 中英/两版怎么并排看 | 与 text-diff 互补（并排 vs 差异摘要） |
| 22 | summary-second-hand | tools/realestate/summary-second-hand.html | 二手房税费 | 买房过户要交多少税？ | 现有无房产税费指南 |
| 23 | option-breakeven-call | tools/securities/option-breakeven-call.html | 看涨期权盈亏平衡 | 期权多久回本？ | 现有无期权指南 |
| 24 | oil-change-countdown | tools/automotive/oil-change-countdown.html | 机油更换倒计时 | 什么时候该换机油？ | 现有无保养提醒指南 |
| 25 | baker-percentage | tools/baking/baker-percentage.html | 烘焙百分比 | 配方怎么按比例缩放？ | 现有无烘焙指南 |

## 重复检查结论

- 逐条比对 `json/guides.json`（49 条映射）与 `guides/*.html`（55 篇）的 title / slug / 目标工具：25 个选题的工具均不在现有映射中，主题无重叠。
- 健康类选题（预产期/饮水/心率区间/腰臀比）与现有 blood-pressure/blood-sugar/bmi/body-fat/calorie 指南指标不同，非改名复制。
- 文本类（text-diff / text-extract-urls / text-compare）三者定位互补：差异高亮 / 链接提取 / 并排审阅，非同模板复制。

## 落地机制

- 生成器：`scripts/gen_n3_guides.py <batch>`（batch=1..5），复用 `scripts/gen_guides2.py` 的 TPL 模板。
- 每批动作：写 5 篇 `guides/<slug>-guide.html` + 合并对应 5 条到 `json/guides.json` + 向 `guides/index.html` 追加 5 个 `<li>`。
- 每批验收：`python3 scripts/run_gates.py` 全绿；新指南从指南中心或工具页可达；无重复 title/id/死链。
- 每批独立 commit：`feat(guides): N3-02 publish guide batch XX`。

## 完成账本

| 批次 | 状态 | commit | 指南数累计 |
|---|---|---|---|
| 01 | 待生成 | - | 55→60 |
| 02 | 待生成 | - | 60→65 |
| 03 | 待生成 | - | 65→70 |
| 04 | 待生成 | - | 70→75 |
| 05 | 待生成 | - | 75→80 |
