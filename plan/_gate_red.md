# 红门禁归集（集成线）

> 规则：红了照推，逐条记录「门禁名 / 页面 slug / 错误摘要 / 归属线」。修完在状态列标记。

## 2026-11-04 · commit `0b75c76762`（CI run 41828144376）

| 门禁 | 页面 slug | 错误摘要 | 归属线 | 状态 |
| --- | --- | --- | --- | --- |
| anti-regression: case discrimination | `agriculture/mulch-coverage` | 逃生项 2 > 基线 0；`expect` 含「0.0%」重叠率，默认态同样输出，回退默认后仍 PASS | 农业线 | 已修（删除静态锚，保留 7.20 / 50.0% / 17.7） |
| anti-regression: case discrimination | `agriculture/greenhouse-rolling-time` | 逃生项；`expect` 含「卷膜通风」，命中页面静态「卷膜通风参考时间表」标题，回退默认后仍 PASS | 农业线 | 已修（改为动态原因串「温度26℃在合理范围，但湿度95%偏高…」） |
| anti-regression: case discrimination | `agriculture/mulch-coverage` / `agriculture/greenhouse-rolling-time`（自动补强块） | 全 42 输入回显型锚，页面新增校验后失效 | 集成线 | 已修（改合法参数 + 派生数值锚：20000 地膜总长 / 12℃ 内外温差） |

### 说明
- 本次 CI 失败在「Run ToolBox quality gates」，部署被跳过（未部署）。
- 本地在干净 HEAD 工作树复现为 1/219 红，红项即上表两个逃生项。
- 农业线本地已同步修正主用例；集成线补齐自动补强块并复核：`agriculture calc 131/131`、判别力 0 逃生。

## 2026-11-04 · 推送批（HEAD `e1395c893a`）

**干净 worktree 全量门禁 219/219 通过（2:11.27），无红项，无需记录失败条目。**

### 本轮已修但未入本批的红项

| 门禁 | 页面 slug | 错误摘要 | 归属线 | 状态 |
| --- | --- | --- | --- | --- |
| general calc correctness | `agriculture/analysis-21` | 用例仍注入 DN 值 1200/800、42/42，页面已收紧 0–1 反射率校验 ⇒ 未匹配期望值 | 集成线 | 已修（改为 0.8/0.4 与 0.6/0.1，锚定实算 0.3333 / 0.7143，提交 `153b5c5a8b`） |

### 主工作区（脏树）发现、未纳入本批的红项

| 门禁 | 页面 slug | 错误摘要 | 归属线 | 状态 |
| --- | --- | --- | --- | --- |
| anti-regression: case discrimination | `fire-rescue/fire-resistance-rating` | 逃生项 1 > 基线 0（via=input event）；`expect "2.00h"` 默认态同样命中 | 土建线（`scripts/verify_fire-rescue_calc.js` / 页面有未提交改动） | 待土建线回批时修；集成线未动其未提交文件 |

### 说明
- 按新流程，全量门禁改在 `git worktree add --detach` 的干净副本上跑，只验证 commit 内容，不验证他人未提交改动。
- 脏树上 `discriminate_check` 的 1 个逃生项来自土建线正在进行中的页面改动，HEAD 上不存在（干净 worktree 为 0 逃生）。

## 2026-11-04 · 门禁总数 219 → 220

新增 `escHtml regression`（`node scripts/verify_esc_html.js`，安全线 `b44a53da52`），注册于分类计算门禁之后、anti-regression 组之前。

## 2026-11-04 · 科学线批次（本地提交 `a112e59303` / `35034a0a2d`）

### 快检结果（主工作区）

- `science calc correctness`：190/190 通过。
- `discriminate_check`：8518 检 / 8517 正确变红 / **1 逃生项**。

| 门禁 | 页面 slug | 错误摘要 | 归属线 | 状态 |
| --- | --- | --- | --- | --- |
| anti-regression: case discrimination | `hr/recruitment-funnel` (via=addStage) | 逃生项 1 > 基线 0；`expect` 在默认态/不依赖计算点即可命中 | 商业HR线（`tools/hr/recruitment-funnel.html` 与 `scripts/verify_hr_calc.js` 均有未提交改动，集成线未动） | 待 HR 线回批时修 |

### 说明
- 科学线本批 10 页，新增 7 条回归用例，科学用例零逃生。
- `i18n/tools/content_deepdive.json` 与 `i18n/tools/en/**` 的 `M` 均来自其他线，**未纳入本批**（待合流）。

断言范围：
- `escHtml` 必须对 `"` `'` `<` `>` `&` 全编码；
- 禁止回退成 `textContent → innerHTML` 实现；
- 属性载荷整串保留（不被截断/二次解码）；
- 抽查 3 个调用页（`it/api-sign-generator`、`advertising/storyboard-timeline`、`metalwork/analysis-35`）确含 `escHtml(` 调用。

门禁位置：分类计算门禁之后、`anti-regression: no fake gates` 之前，编号 `[219/220]`；总数由 219 增至 **220**。


