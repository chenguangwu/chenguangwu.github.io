# 房地产/物业 · tools/{realestate,property,rental}（~80 页）

## 功能缺陷
- 购房页缺「首付比例/税费/中介费合计一口价」整合（和 finance 联动）。
- 租金页缺「租售比/回本年限」联动输出。

## 受影响范围
- tools/realestate/（54）、tools/property/、tools/rental/（~80 页）

## 进度
- 🟢 确认缺陷已清零；剩余为功能增强项：LOFT 税费场景 / 购房一口价整合 / 租售比联动

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

- 本轮实读 2 页：`tools/realestate/depreciation-2.html`、`tools/realestate/cost-depreciation.html`；新增 2 条（高 0/中 2/低 0）；未覆盖：本轮未读 `tools/realestate`、`tools/rental` 其余页面，RE-N11 与既有 RE-N4 同属越界校验族但页面不同，无重号。
