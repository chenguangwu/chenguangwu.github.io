# 房地产/物业 · tools/{realestate,property,rental}（~80 页）

## 功能缺陷
- 购房页缺「首付比例/税费/中介费合计一口价」整合（和 finance 联动）。
- 租金页缺「租售比/回本年限」联动输出。

## 受影响范围
- tools/realestate/（54）、tools/property/、tools/rental/（~80 页）

## 进度
- 🟡 续批中（剩余：LOFT 税费场景 / 购房一口价整合 / 租售比联动）

## 2026-11-03 第一轮抽样补充

### 租金估算接受负单价或负面积（中，确认源码缺陷）
- 问题与证据：`tools/realestate/rent-1.html:525-542` 生效的后一个 calc 仅校验数值有限，单价 −10、面积 100 时输出月潜在毛收入 −1000，且调用 saveHistory。
- 影响：`tools/realestate/rent-1.html`，无意义输入成为正常结果和历史。
- 方案：按业务规则限制输入范围，非法值不保存；可编辑出租率并对比空置情景，明确是假设不是实际值。

### 覆盖
- 本次核查首付页与租金页 2 页（首付页递减额已修复清账，租金页负输入仍待修），首付例使用内存 DOM 桩，未验证浏览器、线上及其他房地产页面。

## 2026-11-03 续查（并行批 H）

本批覆盖 8 页：`tools/realestate/convert-area-shared.html`、`tools/realestate/fund-loan.html`、`tools/realestate/price-discount-1.html`、`tools/realestate/market-valuation.html`、`tools/realestate/layout-score.html`、`tools/rental/rent-2.html`、`tools/realestate/return-1.html`、`tools/rental/rental-yield.html`。下列结论均来自只读源码阅读 + node 内存复刻页内公式，未在浏览器执行；文件原有两条为无编号标题，本批沿用同目录兄弟文件「前缀-N」格式取 `RE-N`，与该文件既有标题不重号，也不与 `06-F*` / `MS-F*` / `L-N*` 冲突。

### 留存优化
- 公摊换算与户型评分可互填：把 `convert-area-shared` 的套内/建面结果一键带入 `layout-score`，避免用户两页重复录入（呼应既有「购房页缺一口价整合」诉求）。
- 二手房评估页把「单项修正」与「累计修正」分成两栏展示（累计超 25% 的黄色提示已于第 1039 批落地）。
- 公积金两页统一口径：`fund-loan-1` 的 15 倍/12% 与 `fund-loan` 的可调倍数应共用一份「城市常用参数」静态预设（纯前端常量表），避免同主题两页给出不同假设。
- 租赁两页（`rental-yield` 与 `rent-2`）可共用「空置率 / 净收益 / 回本年限」联动卡片，直接落地文档既有「租金页缺租售比、回本年限联动输出」。
- `rental-yield` 补「毛回报率（年租金÷总价）」一行：公式框已承诺该口径，当前只输出净回报率。
- 两输入直算页（`return-1`、`price-discount-1`、`convert-area-shared`、`fund-loan-1`）建议统一加区间守卫，避免同一类负数/越界问题逐页复发。

### 续查覆盖
- 已读源码并 node 内存复算：`tools/realestate/convert-area-shared.html`、`tools/realestate/fund-loan.html`、`tools/realestate/price-discount-1.html`、`tools/realestate/market-valuation.html`、`tools/realestate/layout-score.html`、`tools/rental/rent-2.html`、`tools/realestate/return-1.html`、`tools/rental/rental-yield.html`。
- 与第一轮不重复：第一轮已覆盖 `down-payment.html`、`rent-1.html`，本批未再审计这两页。
- 方法：node 内存复刻页内公式与边界分支，证据均为「文件:行号 + 复现输入 → 实际输出」；本批 10 条均为确认，无待验证项。
- 未做：真实浏览器点击验证、英文态（`?lang=en-US`）验证、移动端验证、构建与门禁（`_build.py` / `run_gates.py`）验证、线上部署验证。

## 2026-11-04 续查（并行批 L）

> 范围：本轮阅读 2 页（`tools/realestate/depreciation-2.html`、`tools/realestate/cost-depreciation.html`）。仅源码 + node 复算，未开浏览器/未做 EN/移动端/门禁验证。

### RE-N11 成新率法折旧页成新率越界，输出负折旧/超 100% 现值（中，确认）
- 描述：重置成本与成新率均无正负/区间守卫，`已提折旧 = 重置成本×(1-成新率/100)`、`现值 = 重置成本×成新率/100` 直接计算；成新率 >100% 得到负折旧，<0 得到负现值。
- 证据：`tools/realestate/depreciation-2.html:130,132,557-565`
- 复现：重置成本 1,000,000、成新率 150 → 已提折旧 -500,000.00、现值 1,500,000.00、折旧率 -50.00%，判读仍为“成新度较高”；成新率 -20 → 已提折旧 1,200,000.00、现值 -200,000.00、折旧率 120.00%。
- 影响：越界成新率会产生负折旧或超过重置成本的现值，且结果卡与文字结论仍按正常区间措辞，容易被当作估值结果使用；与既有 RE-N4 折扣区间问题同类，但页面与字段不同。
- 方案：成新率限制在 0–100、重置成本要求 >0；越界标红停止计算，并修正“成新度”判读只在 0–100 内生效。

### RE-N12 年限法折旧页负使用年限不被拦截，过小年限使 10 年累计折旧超重建成本（中，确认）
- 描述：`__tbInputGuard` 只把使用年限为 0 视为分母非法，负数照常通过；`年折旧 = 重建成本×95%÷年限`，且“10 年累计折旧”固定按年折旧×10、“30 年半程账面成本”固定按重建成本÷2，均未随年限收敛到残值。
- 证据：`tools/realestate/cost-depreciation.html:130,132,634,641-645`
- 复现：重建成本 900,000、使用年限 1 → 年折旧 855,000.00、10 年累计 8,550,000.00（为重建成本的 9.5 倍）、30 年半程账面成本仍为 450,000.00；使用年限 -30 → 年折旧 -28,500.00、10 年累计 -285,000.00。
- 影响：负年限直接产出负折旧；年限小于 10 年时累计折旧超过应折旧总额（95%），30 年账面值也与实际年限脱节，三张结果卡互相矛盾。
- 方案：使用年限要求 >0（建议 ≥1）；“10 年累计折旧”按 `min(10, 年限)×年折旧` 并封顶 95% 重建成本；“30 年半程账面成本”按 `重建成本×(1-95%×min(30,年限)/年限)` 推导，年限 ≥30 时显示残值 5%。

- 本轮实读 2 页：`tools/realestate/depreciation-2.html`、`tools/realestate/cost-depreciation.html`；新增 2 条（高 0/中 2/低 0）；未覆盖：本轮未读 `tools/realestate`、`tools/rental` 其余页面，RE-N11 与既有 RE-N4 同属越界校验族但页面不同，无重号。
