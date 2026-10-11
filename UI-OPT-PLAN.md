# UI-OPT-PLAN.md — ToolBox 全站 UI 专项优化（超长任务）

> 目标：对全站 ~5000 工具页 / 209 分类做 UI 现代化专项优化，按分类分批推进、分批提交。
> 对齐老板 5 点诉求（整体美观 / 日期&下拉统一 / 展示异常 / 布局按钮 / 其它现代化），并补充对项目有帮助的高价值项。
> 动工前必读 `AGENTS.md` 与 `.workbuddy/memory/` 当日日志；约束同 DEV-PLAN（纯前端、URL 稳定、五道门禁、Actions 部署）。

---

## 〇、必须遵守铁律（老板 2026-10-11 明确，覆盖并作废旧规）

> **UI 改动影响面大，必须真机验收，否则不许提交。**

1. 🔴 每批次 UI 改动完成后，**必须在真实浏览器（真机）中跑通所有相关功能并截图验证**，确认日期/下拉/布局/展示均正常、无遮挡/溢出/错位，方可判定完成、方可 `commit`/`push`。
2. 🔴 **禁止仅凭「五道门禁通过」就提交 UI 改动**——门禁只覆盖结构与计算正确性，不覆盖视觉与交互。门禁通过是提交的必要非充分条件。
3. 🔴 真机验收口径（用系统 Chrome `/Applications/Google Chrome.app` 或 Playwright 启动真实浏览器）：
   - 统一组件弹层（日期日历 / 下拉）正常展开、关闭、选中回写；深色模式配色正确。
   - 页面无悬浮遮挡、无横向溢出、内容区对齐一致（参考 investment-roi 的 `.container` 内嵌错宽教训）。
   - 移动端视口（375px）下布局正确堆叠、按钮触达面积 ≥44px、底部抽屉正常。
4. 🔴 截图作为验收证据随批次说明一并汇报；发现异常须修复后**重新截图**，直至全部通过才收尾。
5. 本地服务用 `python3 -m http.server` 起根目录；Playwright 用 `executablePath` 指向系统 Chrome，避免依赖未安装的内置 chromium。

---

## 一、问题清单（对齐 5 点 + 补充项）

### P1 整体不够美观 / 现代化（系统性）
- 设计语言不统一：个别页手写内联样式，配色/圆角/间距与全站 design token 漂移。
- 裸排区：公式、结果、注意事项之间留白与对齐不一致。
- 现代化方向：统一 design token（已具备 CSS 变量）、卡片微交互、留白节奏、三级文字层次（标题/正文/辅助）、轻量阴影与渐变点缀、空/加载态。

### P2 日期 & 下拉组件太丑（全站统一几套）★ 基础设施批次先做
- 日期：原生 `type=date` 弹层跨端丑且不一致 → 统一 `TbDatePicker`（popup / inline 两套）。
- 下拉：原生 `<select>` 弹层丑 → 统一 `TbSelect`（default / capsule / underline 三套），长列表带搜索。
- 时间：已有 `.tb-time-control` 现代化，保持并复用于时间字段。

### P3 展示异常（太宽 / 太窄 / 悬浮 / 遮挡）
- 容器嵌套错宽（deep-dive 已统一，需复查其它嵌套区如 tool-ad、opt-guide 对齐）。
- 悬浮元素遮挡：全站扫描 `position:fixed` 误用（参考 investment-roi 左下角 fixed 条类名冲突）。
- 溢出：长文本/代码/表格未滚动；图片未 `max-width:100%`。
- ✅ **已修复全站性缺陷（2026-10-11 批次 3）**：**页内 tab 类名 `.tab-bar` 与全局 `css/site-chrome.css` 移动底部导航撞车**（`position:fixed;bottom:0;z-index:1000`，桌面 `display:none` 被页面内联 `display:flex` 覆盖但 fixed 未覆盖）⇒ 页内 tab 条悬浮视口底部遮挡内容、移动端与全局导航叠罗汉。7 页改名 `.page-tabs` 根治（finance 5 页 + fengshui-guide + it/ssl-info）。同批：currency-symbol 弹窗遮罩 z-index 1000→2000（原与全局导航同层，导航浮在遮罩上）。
- ✅ **公式卡错位修复（2026-10-11 批次 3）**：`formula-box` 被插入到字段组 label 与输入行之间（视觉像字段专属说明、撑低输入区），全站扫描共 2 处：finance/currency-converter（移至 result-display 后）+ design/gradient（移至工具卡后）。
- ✅ **已修复全站性缺陷（2026-10-11 批次 1）**：`.related-tool-card`/`.rt-info` 加 `min-width:0`（fertilizer-calculator 656px→375px 实证）；新版 `.related-tools .rt-item` 加 `min-width:0` + 移动端 `minmax(0,1fr)`（yaml-to-json/api-sign-generator 1581px→375px）；`.rt-name`/`.rt-info` 长串由失效的 nowrap+省略号改为换行断行（根治 scrollWidth 沿可见祖先链泄漏撑大 document——被裁剪后代的 scrollWidth 仍会计入 visible 祖先）；全站长内容断行规则（deep-dive/opt-guide/opt-faq/tool-notes/info-box/`.card p`/`.formula-box` 系/`td,th`/`code`）+ `pre,.code-block` 横向滚动 + 内容区 `img,svg max-width:100%`；`.input-row .btn` 后代选择器收窄为直接子选择器（aes-encryptor 380px→375px）；`.cat-tool`/`.tool-ad-card`/nav-menu `.tb-tool-name/.tb-tool-desc` 加 `min-width:0`+断行（分类落地页 209 首页 mega-panel 卡片 392px→375px）。**it/ 全量 339 页复扫溢出 0**。

### P4 布局 / 按钮放置不合适
- 主操作按钮未突出；多按钮挤一行；输入与按钮不对齐。
- 移动端输入行未堆叠、按钮触达面积 <44px。
- 多 tab / 多 section 顺序与信息密度不合理。

### P5 其它不符合现代化样式
- 占位/模板页（calc-X 名不符实、内容单薄）→ 重做（参照 toolbox-stat-template-redo 规范）。
- 标题/描述 SEO 文案裸排、无卡片包裹。

### 我补充的高价值项（对 SEO/留存/体验有帮助）
- A. 统一「加载态 / 空态 / 错误态」组件（toast 已有，补 inline-error、skeleton）。
- B. 统一「分段控件 segmented control」替代散落的互斥 radio/按钮组（提升密度与现代感）。
- C. 统一「复制结果」按钮样式与交互（多页重复实现，收敛为 `.tb-copy-btn`）。
- D. 统一「结果可视化」迷你图表（bar/sparkline）绘制规范，杜绝伪图表（investment-roi 教训）。
- E. 无障碍增强：aria-label 补全、focus-visible（已有）、`prefers-reduced-motion`（已有）。
- F. 字体与排版节奏：行高/字阶统一，避免字号过小、元素挤行（老板关注点）。
- G. 深色模式一致性：新组件深色变量对齐既有 `--bg-card/--border/--text`。

---

## 二、统一组件设计规范（基础设施，全站渐进增强）

> 范式：复用 `common.js` 时间选择器做法——组件 JS 在加载时自动接管 `type=date` 与 `select`，**不改 5000 页源码**，零回归风险。
> verify 门禁在无头桩环境不运行组件 JS（保持原生 input），故不影响判别力。

- **TbSelect**（下拉）：trigger 复刻 input 外观（圆角 12 / 边框 / focus 环），popup 为圆角卡片 + 选项 hover/active 高亮；移动端底部抽屉；>8 项带搜索过滤；完整键盘可达（↑↓/Enter/Esc）+ ARIA listbox。三套视觉：`default`(标准盒) / `capsule`(胶囊) / `underline`(下划线极简)，由 `data-tb-select` 或容器 class 指定。
- **TbDatePicker**（日期）：月历弹层（上/下月、年份切换、今日、选中高亮），写回 `YYYY-MM-DD`（保持 `valueAsDate` 语义），移动端底部抽屉，键盘可达。两套：`popup`(默认) / `inline`(内嵌)，由 `data-tb-date` 指定。原生 `type=date` 在增强后置 `readonly` 以抑制原生丑弹层，自定义图标由触发器承载。
- **注入方式**：组件 IIFE 落在 `js/common.js`（全站已加载，`<script defer>`，无需新建文件/改 `_build.py`）；`DOMContentLoaded` + `MutationObserver` 动态增强（同时间选择器）。已加排除项：`multiple`/`size>1` 下拉、`.lang-switcher` 内 select、`data-tb-select="off"`/`data-tb-date="off"` 显式退出。

---

## 三、执行模型

1. **批次 0 — 基础设施** ✅（2026-10-11 完成）：TbSelect + TbDatePicker 落地 `js/common.js` + `css/common.css` + 现代化原子类。门禁 217/217 通过；playwright 真机验收 13 项通过（桌面弹层/深色/写回/change 派发/语言切换器排除/移动端底部抽屉），截图存证。附带发现：`.related-tool-card` 窄屏溢出（已记入 P3）。
2. **批次 1..N — 按 `tools/` 目录顺序逐分类**：每分类扫描 P1–P5 + 补充项 A–G，修复逐页布局/展示/按钮问题；同类问题在分类内提炼复用样式，必要时沉淀为 `common.css` 原子类。每分类（或每小批）跑门禁 + 提交。
3. **收尾**：全站门禁 + 抽样视觉验收 + 提交纪律（改动进构建产物 → push + 确认 Actions success）。

---

## 四、分类批次清单（209 分类，按 `tools/` 字母序逐批执行）

> 进度标记：⬜ 待办 / 🔄 进行中 / ✅ 完成。每批 commit 后更新。



### 【超大 >80页】（5 分类）

- ✅ `it/` —      339 页（2026-10-11 完成：全量 339 页 375px 真机扫描溢出 10→0；8 项全站性共享 CSS 修复见 P3/执行记录；桌面+移动截图验收；json-formatter「JSON 有效」功能验证）
- ✅ `general/` —      183 页（批次2：375px 全量扫描溢出 0；TbSelect/日期组件真机 12 项验收过；**修复 TbSelect 键盘缺陷**：开放态 ArrowDown 误选当前项→改为 wrap 层统一路由、Arrow 移动高亮、Enter 选中、搜索框按键不劫持；日期弹层年/月下拉排除增强避免搜索框嵌套）
- ✅ `finance/` —      113 页（批次3：375px 全量扫描溢出 0、42 含表页表格无裁剪（均在滚动容器内）；**修复页内 `.tab-bar` 撞全局移动导航**（5 页改 `.page-tabs`，fixed 悬浮遮挡根治，tab 切换真机验证过）；currency-converter 公式卡移出「从」组；currency-symbol 弹窗 z-index 2000 盖过全局导航（截图验证）；TbSelect 真机验收 bond-yield/compound-interest 过（popup+键盘 选值生效））
- ⬜ `design/` —      112 页
- ⬜ `science/` —       99 页

### 【大 40-79】（20 分类）

- ⬜ `sports/` —       79 页
- ⬜ `life/` —       73 页
- ⬜ `biz/` —       70 页
- ⬜ `fun/` —       65 页
- ⬜ `ai/` —       65 页
- ⬜ `agriculture/` —       64 页
- ⬜ `hydraulic/` —       57 页
- ⬜ `automotive/` —       56 页
- ⬜ `realestate/` —       55 页
- ⬜ `legal/` —       55 页
- ⬜ `statistics/` —       52 页
- ⬜ `edu/` —       50 页
- ⬜ `marketing/` —       47 页
- ⬜ `surveying/` —       45 页
- ⬜ `meteorology/` —       43 页
- ⬜ `metalwork/` —       43 页
- ⬜ `optical/` —       42 页
- ⬜ `health/` —       42 页
- ⬜ `fire-rescue/` —       40 页
- ⬜ `energy/` —       40 页

### 【中 20-39】（79 分类）

- ⬜ `fishery/` —       39 页
- ⬜ `eco/` —       39 页
- ⬜ `machinery/` —       38 页
- ⬜ `geology/` —       38 页
- ⬜ `aerospace/` —       38 页
- ⬜ `math/` —       37 页
- ⬜ `fitness/` —       37 页
- ⬜ `securities/` —       36 页
- ⬜ `healthcare/` —       36 页
- ⬜ `accounting/` —       36 页
- ⬜ `insurance/` —       34 页
- ⬜ `cosmetic-derm/` —       34 页
- ⬜ `photo/` —       33 页
- ⬜ `ophthalmology/` —       33 页
- ⬜ `materials/` —       32 页
- ⬜ `encode/` —       31 页
- ⬜ `tax/` —       30 页
- ⬜ `robotics/` —       29 页
- ⬜ `obstetrics/` —       29 页
- ⬜ `nuclear/` —       29 页
- ⬜ `metrology/` —       29 页
- ⬜ `geometry/` —       29 页
- ⬜ `acoustics/` —       29 页
- ⬜ `thermodynamics/` —       28 页
- ⬜ `signal/` —       28 页
- ⬜ `quantum/` —       28 页
- ⬜ `livestock/` —       28 页
- ⬜ `hematology/` —       28 页
- ⬜ `food-testing/` —       28 页
- ⬜ `economics/` —       28 页
- ⬜ `chemistry/` —       28 页
- ⬜ `structural/` —       27 页
- ⬜ `reproductive-medicine/` —       27 页
- ⬜ `electromagnetism/` —       27 页
- ⬜ `dentistry/` —       27 页
- ⬜ `clinical-nursing/` —       27 页
- ⬜ `textile/` —       26 页
- ⬜ `rheumatology/` —       26 页
- ⬜ `pulmonology/` —       26 页
- ⬜ `neurology/` —       26 页
- ⬜ `kinematics/` —       26 页
- ⬜ `construction/` —       26 页
- ⬜ `clinical-lab/` —       26 页
- ⬜ `banking/` —       26 页
- ⬜ `urology/` —       25 页
- ⬜ `psychiatry/` —       25 页
- ⬜ `pediatrics/` —       25 页
- ⬜ `investment/` —       25 页
- ⬜ `food/` —       25 页
- ⬜ `cardiology/` —       25 页
- ⬜ `nephrology/` —       24 页
- ⬜ `fluid/` —       24 页
- ⬜ `ent/` —       24 页
- ⬜ `ecommerce/` —       24 页
- ⬜ `dynamics/` —       24 页
- ⬜ `dermatology/` —       24 页
- ⬜ `astronomy/` —       24 页
- ⬜ `acupuncture/` —       24 页
- ⬜ `tcm-pharmacy/` —       23 页
- ⬜ `tcm-chemistry/` —       23 页
- ⬜ `rehabilitation/` —       23 页
- ⬜ `gastroenterology/` —       23 页
- ⬜ `endocrinology/` —       23 页
- ⬜ `travel/` —       22 页
- ⬜ `tcm-diagnosis/` —       22 页
- ⬜ `property/` —       22 页
- ⬜ `optics/` —       22 页
- ⬜ `hr/` —       22 页
- ⬜ `food-processing/` —       22 页
- ⬜ `electronics/` —       22 页
- ⬜ `civil/` —       22 页
- ⬜ `beauty/` —       22 页
- ⬜ `psychology/` —       21 页
- ⬜ `metallurgy/` —       21 页
- ⬜ `forensic-medicine/` —       21 页
- ⬜ `music/` —       20 页
- ⬜ `language/` —       20 页
- ⬜ `forestry/` —       20 页
- ⬜ `electrical/` —       20 页

### 【小 <20】（105 分类）

- ⬜ `nutrition/` —       19 页
- ⬜ `data/` —       18 页
- ⬜ `niche/` —       17 页
- ⬜ `advertising/` —       17 页
- ⬜ `welding/` —       16 页
- ⬜ `transport/` —       16 页
- ⬜ `safety/` —       16 页
- ⬜ `logistics/` —       16 页
- ⬜ `leather/` —       16 页
- ⬜ `process/` —       15 页
- ⬜ `medical/` —       15 页
- ⬜ `mechanical/` —       15 页
- ⬜ `image/` —       15 页
- ⬜ `engineering/` —       15 页
- ⬜ `dyeing/` —       14 页
- ⬜ `pr/` —       13 页
- ⬜ `pet/` —       13 页
- ⬜ `paper/` —       13 页
- ⬜ `mining/` —       13 页
- ⬜ `gardening/` —       13 页
- ⬜ `usedcar/` —       12 页
- ⬜ `text/` —       12 页
- ⬜ `gas/` —       12 页
- ⬜ `fire/` —       12 页
- ⬜ `elderly/` —       12 页
- ⬜ `chemical/` —       12 页
- ⬜ `security/` —       11 页
- ⬜ `hvac/` —       11 页
- ⬜ `sales/` —       10 页
- ⬜ `procurement/` —       10 页
- ⬜ `misc2/` —       10 页
- ⬜ `misc/` —       10 页
- ⬜ `baking/` —       10 页
- ⬜ `wedding/` —        9 页
- ⬜ `telecom/` —        9 页
- ⬜ `restaurant/` —        9 页
- ⬜ `research/` —        9 页
- ⬜ `rental/` —        9 页
- ⬜ `quality/` —        9 页
- ⬜ `museum/` —        9 页
- ⬜ `library/` —        9 页
- ⬜ `decor/` —        9 页
- ⬜ `cognition/` —        9 页
- ⬜ `cleaning/` —        9 页
- ⬜ `admin/` —        9 页
- ⬜ `woodwork/` —        8 页
- ⬜ `printing/` —        8 页
- ⬜ `hotel/` —        8 页
- ⬜ `dance/` —        8 页
- ⬜ `audio/` —        8 页
- ⬜ `video/` —        7 页
- ⬜ `urban/` —        7 页
- ⬜ `startup/` —        7 页
- ⬜ `road/` —        7 页
- ⬜ `parenting/` —        7 页
- ⬜ `packaging/` —        7 页
- ⬜ `office/` —        7 页
- ⬜ `media/` —        7 页
- ⬜ `jewelry/` —        7 页
- ⬜ `home/` —        7 页
- ⬜ `funeral/` —        7 页
- ⬜ `floral/` —        7 页
- ⬜ `film/` —        7 页
- ⬜ `exhibition/` —        7 页
- ⬜ `chinese-cook/` —        7 页
- ⬜ `archaeology/` —        7 页
- ⬜ `yi/` —        6 页
- ⬜ `woodworking/` —        6 页
- ⬜ `tunnel/` —        6 页
- ⬜ `stage/` —        6 页
- ⬜ `shipping/` —        6 页
- ⬜ `service/` —        6 页
- ⬜ `seismology/` —        6 页
- ⬜ `rubber/` —        6 页
- ⬜ `railway/` —        6 页
- ⬜ `project/` —        6 页
- ⬜ `plastic/` —        6 页
- ⬜ `pets/` —        6 页
- ⬜ `petrochem/` —        6 页
- ⬜ `pet-training/` —        6 页
- ⬜ `medical2/` —        6 页
- ⬜ `martial/` —        6 页
- ⬜ `maritime/` —        6 页
- ⬜ `manufacturing/` —        6 页
- ⬜ `logistics2/` —        6 页
- ⬜ `legal2/` —        6 页
- ⬜ `kids/` —        6 页
- ⬜ `glass/` —        6 页
- ⬜ `gardening2/` —        6 页
- ⬜ `futures/` —        6 页
- ⬜ `forex/` —        6 页
- ⬜ `fengshui/` —        6 页
- ⬜ `edu2/` —        6 页
- ⬜ `chinese/` —        6 页
- ⬜ `chess/` —        6 页
- ⬜ `ceramics/` —        6 页
- ⬜ `bridge/` —        6 页
- ⬜ `bonding/` —        6 页
- ⬜ `audit/` —        6 页
- ⬜ `aquaculture/` —        6 页
- ⬜ `antiques/` —        6 页
- ⬜ `accessibility/` —        6 页
- ⬜ `stats/` —        5 页
- ⬜ `photo2/` —        5 页
- ⬜ `network/` —        1 页

---

## 五、验收口径

- 五道质量门禁全过（含 verify 判别力 0 逃生项、expect anti-pattern 静态门禁）。
- 统一组件：playwright 真机截图确认日期/下拉弹层正常、深色模式、移动端底部抽屉；不改页面源码故无回归。
- 每批提交前 `git diff` 自查 + 本地 `python3 _build.py` 通过。
- 日志归档：批次结论写入 `.workbuddy/memory/YYYY-MM-DD.md`，本文件只更新进度标记与待办。
