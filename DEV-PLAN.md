# DEV-PLAN.md — 待处理任务清单

> **本文件只放「待处理任务」与「现状基线」。**
> 所有长期开发约束 / 坑 / 反模式 / 门禁口径已收敛至 `AGENTS.md`（动工前必读）。
> 已完成项、批次流水一律不写入本文件（归档走 `.workbuddy/memory/YYYY-MM-DD.md`）。
> **体积红线**：本文件 `wc -c` > 20 KB 即说明有流水混入，先清理再干活。
> **删除纪律**：每批干完删该批行，整分类干完删该分类行，直到队列清空。

---

## 一、P0 主线 · 工具页体验优化专项（UX-Q4）【当前唯一主线】

**定位**：0→1 已完成（5008 页 / 212 分类 / A 级率 100%），本专项只做 1→N 打磨，**主抓质量、不赶速度**。
**北极星**：单页停留时长 ↑、二跳率（切其他工具）↑、回访率 ↑ —— 真实数据由 51.la / Clarity 月度复盘；日常验收用下面可机检的代理指标。

### 1.1 验收口径（可机检，逐批复测，只升不降）

> 口径修正 ①（2026-10-12 夜）：初版测绘漏统计「同目录相对链接」，内链被低估（13.2% → 73.9%）。
> 口径修正 ②（2026-10-13）：**改了也计不上分** —— 页面通过共享组件库 `TBKit.*` 运行时生成图表/表格/历史，静态扫描只认 `<svg>/<table>/localStorage`，一律漏判。已按调用点记账（`TBKit.chart.` / `matrix.table` / `history.` / `preset.bar` / `export.` / `history.diffLast`）。
> 结论修正：**内链不是「没有」，而是「位置靠后、文案无动作、语义不相关」** —— 改造重点从「补链接」改为「让链接更有效」。

| 指标 | 基线（2026-10-13 修正口径） | 目标 |
|---|---|---|
| UX-Score 全站均值（`scripts/_ux_baseline.py`，9 分制） | **3.89** | ≥ 6.5 |
| 薄弱页（score ≤ 2） | **733** 页（14.6%） | 0 |
| 可视化模块覆盖率（图表 / 示意图 / 矩阵） | 8.6% | ≥ 55%（仅限「语义该有图」的页） |
| 跨工具内链（导流到相关工具） | 97.0% | 100%，且每页 ≥ 4 条**动作化**内链（含场景说明，非纯工具名） |
| 预设场景（一键填充真实场景） | 18.6% | ≥ 70%，每页 ≥ 3 个 |
| 本地沉淀（历史 / 收藏 / 记住输入） | 23.0% | ≥ 80% |
| 结果动作（复制 / 导出 / 分享 / 打印） | 65.6% | 100%，每页 ≥ 3 个 |

**单页最低配置（改造后硬门槛）**：① ≥1 个实体模块（图形 / 图表 / 明细表 / 对比 / 矩阵 之一）；② ≥3 个预设场景；③ ≥4 条相关工具内链；④ 历史记录可用；⑤ ≥3 个结果动作；⑥ 一句「人话结论 + 行动建议」的结果解读。

### 1.2 改造深度分档（控制投入产出，禁止一刀切）

- **S 档 旗舰页**（每分类 3–6 页，全站约 800–1000 页）：按工具语义**重做主交互形态**，独特视觉与玩法，逐页手工设计。选页标准：该分类流量担当 + 语义最适合可视化 + 竞品无差异化。
- **A 档 标准页**（约 60%）：不动计算内核，补齐「通用能力包 + 一个语义化实体模块」（图表 / 明细 / 对比 / 矩阵），半自动 + 人工校对。
- **B 档 轻量页**（约 20%）：仅由组件库统一注入通用能力包 + 说明文案个性化校对。
- **不改造**：92 个 `TOOLBOX-REDIRECT` 存根页（按 §二 P0 到期删除）、`pets` 全目录（6 页全为存根）。

### 1.3 个性化形态库（12 范式，按语义匹配；**单分类内同范式占比 ≤ 40%**，杜绝全类同构）

| # | 范式 | 形态要点 | 典型适用 |
|---|---|---|---|
| P1 | 图形联动 | 输入即重绘 SVG 示意图，随参数变形 | geometry / kinematics / optics / electromagnetism / structural |
| P2 | 图表分析 | 折线 / 柱 / 面积 / 正态曲线 + 悬停读数 | statistics / math / securities / investment / finance |
| P3 | 明细推演 | 分期 / 逐年明细表 + 折叠 + 导出 | finance / banking / tax / realestate / insurance |
| P4 | 情景对比 | A/B/C 方案并列卡 + 差异高亮 + 最优标记 | biz / marketing / decision 类 |
| P5 | 滑块推演 | 主参数滑块 + 敏感性曲线 + 临界点标注 | engineering / energy / thermodynamics / materials |
| P6 | 诊断清单 | 逐项校验（✅/⚠️/❌）+ 失败原因 + 修复建议 | 全部 `*-validator` / 合规校验类 |
| P7 | 双栏处理 | 左输入右输出 + 实时统计 + diff + 行号 | text / encode / json / 格式转换类 |
| P8 | 速查矩阵 | 可搜索筛选对照表 + 命中高亮 + 单击复制 | 单位换算 / 编码表 / 对照表类 |
| P9 | 分步向导 | step 1..n + 进度条 + 逐步解读 + 可回退 | 测评 / 申报 / 方案生成类 |
| P10 | 时间轴日历 | 日期推演 + 甘特 / 日历网格 + 关键节点 | agriculture / project / edu / 孕产类 |
| P11 | 模拟随机 | 固定种子可复现 + 分布直方图 + 批量次数 | fun / 概率模拟 / 抽样类 |
| P12 | 打分雷达 | 多维打分 + 雷达图 + 短板定位 + 改进建议 | 全部 `assessor-*` / 量表评分类 |

### 1.4 工程基建（W0，先于任何分类批量开工）

- [x] **基线测绘脚本** `scripts/_ux_baseline.py`（只读扫描，产出 `scripts/_ux_baseline.json`；`--slug` 逐页薄弱清单、`--gate` 门槛判定，2026-10-12 已完成）
- [x] **组件库 `js/tool-kit.js`**（41KB，零依赖）：SVG 图表 line/bar/pie/gauge/radar/histogram/timeline/**bell**（正态密度 + 区间阴影 + 标注线）/**scatter**（散点 + 回归线）、预设场景条、历史记录（含去重、回填、与上次对比 `diffLast`）、导出 CSV/TXT/SVG、复制、分享链接（URL hash 回填）、速查矩阵（可搜索 + 点击复制）；**内置中英双语**（英文态自动切英文，无中文残留），并导出 `util.isEn` 供页面脚本做双语分支。全站 4705 页已由 `_build.py` 注入（标记 `<!-- TOOLBOX-TOOL-KIT -->`，幂等）。
- [x] **UX 门禁接入 `scripts/run_gates.py`**：新增 `ux baseline regression` 项，比对 `scripts/_ux_baseline_snapshot.json`，分类均分/薄弱数/全站均分任一回退即失败。
- [x] **S 档样板页** `geometry/triangle-heron`：**1/9 → 5/9**（图形联动 SVG 随边长重绘 + 高的虚线标注、5 个预设场景、历史记录与回填、复制/分享动作、5 条动作化相关工具内链）；en 字典已同步；geometry 用例 62/62 通过。
- [x] **相关工具内链构建期注入**（2026-10-13 已完成）：真因是 `_build.py` 注入锚点只有三级回退（tool-intro / 注意事项区块 / 两层 `</div>`+script），**生成页普遍是三层 `</div>`（tool-notes/card/container）才到 `<script>`，三级全落空 ⇒ 1164 页永久无内链**。已加第四级兜底（`(</div>\s*)+(?=<script)` 之后插入），覆盖 3541 → **4700 页（97.0%）**，跨工具导流 + SEO 双补。后续若发现相关工具卡 `rt-desc` 退化成工具名，属描述源缺失，另行处理。
- [x] **A / B 档样板页**：并入试点 `statistics` 批次（A 档图表分析、B 档仅组件注入）。

### 1.5 每批标准作业链（SOP，8–12 页/批，完整收口再开下一批）

1. **诊断**：`python3 scripts/_ux_baseline.py <ind>` → 取该分类 slug 级薄弱清单，按「薄弱度 × 语义可塑性」排批次。
2. **定档定形态**：每页标 S/A/B + P1–P12 范式，检查同范式占比 ≤40%。
3. **改造**：只改 `tools/<ind>/<slug>.html` 源正文区；**不改文件名、不改 URL、不动已验证的计算内核**（发现真 bug 才动，并按「四真缺陷」口径记录）。
4. **i18n 同步（硬性规则见 §1.6，每批必查）**：所有新增动态文案中英双语齐全（helper/dataGrid 包装/InputGuard/preset labelEn/静态按钮 GEN_UI_MAP），跑 EN 零中文门禁（含防真空断言），`?lang=en-US` 内容区零中文。
5. **verify 用例同步**：功能变化必须同步改 expect，**禁降判别力**；跑 `discriminate_check.js`，逃生项须 0。
6. **构建 + 门禁**：`python3 _build.py` → `python3 scripts/run_gates.py`（218/218 不退、A 级率 100% 不退、UX 门禁无回退）。
7. **复测**：`python3 scripts/_ux_baseline.py <ind>` 分数只升不降。
8. **提交**：改动进构建产物 ⇒ commit → push → Actions 单次查询 success → 抽 3–5 个 URL `curl -o` 落盘核对关键内容命中（英文态用真机探针）。
9. **删行**：本批行删除；整分类完成 ⇒ 删除该分类行（W1/W2/W3 队列）。

### 1.6 硬纪律

- 单 Agent 串行：一批完整收口（改造→门禁→提交）再开下一批；禁多 agent 并行写仓库。
- 质量优先于速度：每批允许慢，但不允许「加模块不加价值」——**禁止为凑分堆砌装饰性卡片**，每个新增模块必须回答「用户为什么愿意多停留 30 秒」。
- 不得降 A 级率、不得降门禁通过数、不得引入新外部依赖（CDN 亦禁，组件自绘）。
- 页面体积增速受控：单页增量 ≤ 8KB（组件走共享 `js/tool-kit.js`，不内联堆代码）。
- 🔴 **`__xxBoot` 启动判定唯一正确形态**：`if (document.readyState && document.readyState !== "loading") __xxBoot(); else document.addEventListener("DOMContentLoaded", __xxBoot);` —— harness 的 document 桩不提供 readyState（undefined），旧写法 `=== "loading"` 会走 else 在**脚本求值时**立即启动 boot，早于页面自身 DOMContentLoaded init ⇒ 元素创建顺序改变 ⇒ verify 跨元素多行 expect 失配（surveying/calc-angle-2 门禁事故 84/85）。生产浏览器解析期/已加载两种 readyState 行为与旧写法逐字节一致 ⇒ 线上零影响，仅修桩路径（2026-10-13 已批量修正 149 页：ai 64/statistics 48/surveying 37）。

#### i18n 双语硬性规则（2026-10-13 立；每批必查，违反即打回）

UX-Q4 所有新增/改动的动态文案（图表标题/序列/labels、表格单元格、结果区 `setResult`/innerHTML、preset 文案、InputGuard 提示、aria-label）必须中英双语齐全，`?lang=en-US` 内容区零中文。硬规则：

1. **helper 唯一正确形态**：`(typeof TBKit!=='undefined'&&TBKit.util.isEn())?en:zh` —— TBKit 未加载走中文、isEn 走英文。**禁止写反条件**（曾因漏 `!` 导致英文态图表标题/序列全中文，20 页批量返工）。
2. **extras 动态串全部过 helper**：图表 title/series/labels、gauge 标签、`labs.push()`、象限/档位三元式等运行时生成串一律 `__xxL('EN','中文')`；**禁止裸中文串直出**。
3. **原始 dataGrid 标签/值位**：页面原有 `dataGrid(rows)` 的中文标签与档位值，用 `__xxT` 键名表 + 包装器翻译（`var __tb_xx_dg=dataGrid; dataGrid=function(rows){…}`），键名必须与页面实际标签**逐字一致**（提取时勿丢字，曾因丢字出 EN 残龙）。
4. **InputGuard 模板 isEn 分支**：`请填写「%s」后再计算。` 类提示须 `(isEn)?'Please fill in "%s" before calculating.':中文`。
5. **preset.bar 的 label/labelEn 成对**：新增预设必须同时给 `labelEn`（tool-kit 英文态自动切）。
6. **静态按钮文案进 `GEN_UI_MAP`**（`js/tool-i18n-en.js`，精确短语匹配 label/button/.toolbar .btn/select option）；漏配则英文态按钮直出中文（本轮补了「导出 CSV」→「Export CSV」）。**改 `js/**` 必须连 `sw.js` 一起提交**。
7. **每批必跑 EN 零中文门禁**（chart 标题/序列/labels/gauge、table 单元格、resHtml、preset labelEn 完备性、注入容器 aria-label），且**必须带防真空断言**（`charts.length===0` 判失败——曾因守卫翻转变异导致图表全挂、门禁真空通过）。
8. **结果可视化容器**：不写 `role="img" aria-label="结果可视化"` 类中文 aria（图表自带语义，英文态会残留）。
9. 🔴 **严禁对守卫/符号形态做批量正则「统一」**：曾用两遍 blanket 正则把 extras 守卫 `===` 误翻 `!==`，TBKit 一加载 extras 提前返回、图表全挂，而冒烟与门禁都没发现。批量脚本只准靶向替换具体串；apply 脚本结尾必须带 SELF-CHECK（守卫计数、无翻转守卫）；中途断言失败 ⇒ `git checkout` 整批还原重跑，禁止续跑。

### 1.7 当前分类（进行中）

（surveying/legal/robotics/electromagnetism/process/geometry/fluid/metrology/kinematics/quantum/acoustics/insurance 已收口（insurance 仅生成器可接的 17 页，余 16 页含嵌套函数/无 calcTool 留手动 A 档精做），见下方存档；下一分类从 §1.8 最弱候选起，按「最弱优先」开：当前最弱 `chemistry` 2.89/47% → `optical` 3.12/38% → `materials` 2.05/28 → `healthcare` 2.42/28 等）

**已完成分类存档**（批次细节见当日 memory）：`statistics` 52 页 1.67→7.58、薄弱 46→0（⚠️ 8 组功能重复工具待老板决策：`p`↔z-score-calc、`t`↔t-score、`z`↔z-score-calc、`statistics`↔normal-cdf、`statistics-16`↔linear-regression、`statistics-10`↔coefficient-of-variation、`statistics-13`↔stddev-list/variance-list、`statistics-5`↔sample-size-mean；清理需下线 URL 走 `sitemap-deadlinks.xml`，不擅自执行）；`ai` 65 页 2.31→7.77、薄弱 47→0（AI-1~AI-7 七批；数值页全部 8/9，文本/文件页 6–7/9 为其实时上限）；**`surveying` 45 页 1.89→7.78、薄弱 31→1（仅 `distance-4` 重定向存根不可改造、`index` 导航页不动；SV-1~SV-5 五批；图表范式 line 31.1%/bar 35.6% 合规；calc-1 EN 态动态标签时序 bug + convert-46 字典遗漏已修；4 个 `type="number"` 逗号输入框待修见 §2 P1）**；`legal` 53 页 1.96→6.19、薄弱 37→5（图表+速查表+历史+预设+导出+i18n 双语全量收口；剩余 5 页为模板/检索型无计算内核，留最后单独一档）；**`robotics` 29 页 1.07→6.86、薄弱 29→0（28 页用 `scripts/_ux_wire.py` 批量补线 table+history+presets+export+i18n 双语；1 页重定向/导航存根不可改造；harness 56/56 全过）**；**`electromagnetism` 27 页 1.15→（均分待基线刷新）薄弱 23→0（25 页用 `_ux_wire.py` 补线，ohms-law 为 tool-page-runtime 三模式计算器无 calcTool 跳过；harness 51/51 全过；生成器修复空输入页语法错误）**；**`process` 15 页 1.27→（均分待基线刷新）薄弱 14→2（12 页用 `_ux_wire.py` 补线，harness 14/14 全过；`defect-probability`/`sigma-level` 含嵌套函数 erf/invNorm，生成器跳过留手动 A 档精做；生成器新增「嵌套函数 skip + const/let→var」防重复声明）**；**`geometry` 29 页 1.17→（均分待基线刷新）薄弱 29→0（28 页用 `_ux_wire.py` 补线，harness 62/62 全过；生成器改为括号匹配提取完整 calcTool 体（支持带参 `calcTool(force)` 与早现行首 `}` 页），原误跳 6 页全部解锁）**；**`fluid` 24 页 1.21→（均分待基线刷新）薄弱 24→0（23 页用 `_ux_wire.py` 补线，harness 46/46 全过）**；**`metrology` 30 页 1.3→（均分待基线刷新）薄弱 29→1（`detector-139` 无 calcTool 跳过；28 页用 `_ux_wire.py` 补线，harness 56/56 全过）**；**`kinematics` 26 页 1.23→（均分待基线刷新）薄弱 26→0（25 页用 `_ux_wire.py` 补线，harness 50/50 全过）**；**`quantum` 28 页 1.32→（均分待基线刷新）薄弱 26→0（27 页用 `_ux_wire.py` 补线，harness 53/53 全过）**；**`acoustics` 29 页 1.31→（均分待基线刷新）薄弱 29→0（28 页用 `_ux_wire.py` 补线，harness 56/56 全过）**；**`insurance` 34 页 1.71→（均分待基线刷新）薄弱 28→（生成器接 17 页 harness 59/59 全过；余 16 页含嵌套函数 erf/actuarial 或 `calc-1`/`premium-calc` 等无 calcTool 模式，留手动 A 档精做）**。

### 1.8 分类队列（未开工；干完一个删一行）

<!-- 格式：`分类` 页数/均分/薄弱数 -->

#### W1 头部流量（≥45 页，1628 页合计）

- `it` 341/3.21/98
- `finance` 116/4.03/11
- `design` 112/3.47/24
- `science` 94/3.37/28
- `machinery` 79/3.73/10
- `sports` 78/3.14/11
- `life` 71/3.14/26
- `biz` 70/2.96/21
- `agriculture` 66/3.0/26
- `fun` 63/2.94/16
- `automotive` 60/2.98/11
- `general` 57/3.4/4
- `hydraulic` 56/3.0/11
- `realestate` 55/4.07/0
- `legal` 53/6.19/5（已收口：图表+速查表+历史+预设+导出+i18n 双语全量；剩余 5 页为模板/检索型无计算内核，留最后单独一档，见上方存档）
- `edu` 48/4.65/5
- `marketing` 47/3.98/11

#### W2 中坚（20–44 页，按薄弱数降序先啃最弱，2472 页合计）

- `math` 42/1.64/34
- `accounting` 36/1.86/29
- `materials` 42/2.05/28
- `healthcare` 36/2.42/28
- `aerospace` 38/2.32/27
- `securities` 36/2.14/27
- `chemistry` 38/1.89/26
- `signal` 28/1.75/26
- `banking` 26/1.77/25
- `investment` 26/1.58/25
- `optical` 42/2.14/24
- `tax` 32/2.25/23
- `nuclear` 29/2.14/23
- `thermodynamics` 29/1.52/23
- `structural` 27/1.59/23
- `energy` 42/2.95/21
- `photo` 33/2.45/21
- `civil` 25/1.64/21
- `optics` 22/1.27/21
- `dynamics` 24/2.21/19
- `electrical` 38/2.58/16
- `economics` 28/2.46/15
- `meteorology` 43/3.02/13
- `clinical-nursing` 27/2.67/13
- `ophthalmology` 33/2.88/12
- `travel` 25/3.0/11
- `data` 22/2.95/9
- `tcm-pharmacy` 23/2.87/8
- `beauty` 22/3.09/8
- `language` 20/2.8/8
- `hematology` 28/2.96/7
- `dentistry` 27/2.7/7
- `clinical-lab` 26/3.0/7
- `music` 22/3.0/7
- `forensic-medicine` 21/3.0/7
- `welding` 22/2.86/6
- `metalwork` 43/3.86/5
- `geology` 37/3.05/5
- `obstetrics` 29/3.93/5
- `textile` 29/3.93/5
- `food-testing` 28/3.29/5
- `tcm-chemistry` 23/3.65/5
- `electronics` 22/2.77/5
- `tcm-diagnosis` 22/3.14/5
- `metallurgy` 21/3.52/5
- `health` 41/4.27/4
- `eco` 40/3.4/4
- `fitness` 40/3.65/4
- `cardiology` 25/2.88/4
- `food` 25/3.64/4
- `hr` 22/3.09/4
- `fishery` 39/3.44/3
- `construction` 38/3.89/3
- `livestock` 28/3.46/3
- `psychiatry` 25/3.08/3
- `urology` 25/2.96/3
- `acupuncture` 24/3.08/3
- `astronomy` 24/3.54/3
- `ent` 24/3.42/3
- `gastroenterology` 23/2.87/3
- `rehabilitation` 23/3.57/3
- `food-processing` 22/2.95/3
- `encode` 32/3.5/2
- `pulmonology` 26/3.04/2
- `rheumatology` 26/3.19/2
- `nephrology` 24/3.29/2
- `psychology` 21/4.52/2
- `fire-rescue` 40/3.67/1
- `reproductive-medicine` 27/3.96/1
- `neurology` 26/3.62/1
- `pediatrics` 25/3.2/1
- `endocrinology` 23/4.22/1
- `property` 22/4.0/1
- `cosmetic-derm` 34/3.82/0
- `dermatology` 24/4.04/0
- `ecommerce` 24/4.21/0
- `forestry` 20/3.95/0

#### W3 长尾（<20 页，908 页合计；`pets` 全目录为存根、已剔除）

- `nutrition` 19/3.0/8
- `safety` 17/2.94/9
- `advertising` 17/3.76/2
- `gardening` 16/2.44/8
- `leather` 16/3.12/3
- `pet` 16/3.88/3
- `logistics` 16/3.56/2
- `transport` 16/3.81/1
- `mechanical` 15/2.47/9
- `chemical` 15/3.07/5
- `medical` 15/3.47/3
- `image` 15/3.6/1
- `dyeing` 14/4.0/2
- `hvac` 14/3.86/1
- `usedcar` 14/3.93/1
- `mining` 13/2.92/5
- `paper` 13/3.69/2
- `text` 13/3.62/1
- `pr` 13/3.85/0
- `engineering` 12/1.75/9
- `elderly` 12/3.33/7
- `security` 12/3.25/3
- `gas` 12/3.0/1
- `fire` 12/3.5/0
- `restaurant` 11/4.09/1
- `baking` 10/3.2/4
- `sales` 10/4.2/2
- `cleaning` 10/4.5/1
- `procurement` 10/4.0/1
- `telecom` 10/4.1/1
- `wedding` 10/3.7/1
- `audio` 9/3.33/3
- `library` 9/3.22/3
- `research` 9/3.33/3
- `museum` 9/4.33/2
- `decor` 9/4.0/1
- `quality` 9/3.78/1
- `cognition` 9/5.22/0
- `rental` 9/3.67/0
- `woodwork` 8/3.62/3
- `printing` 8/3.5/2
- `video` 8/4.0/2
- `admin` 8/4.12/1
- `dance` 8/4.88/1
- `hotel` 8/3.25/0
- `parenting` 7/1.71/7
- `home` 7/2.57/4
- `antiques` 7/2.86/2
- `archaeology` 7/2.86/2
- `floral` 7/3.29/2
- `media` 7/2.86/2
- `road` 7/3.43/2
- `ceramics` 7/4.0/1
- `chinese-cook` 7/3.0/1
- `exhibition` 7/3.43/1
- `film` 7/3.57/1
- `funeral` 7/3.71/1
- `jewelry` 7/4.43/1
- `office` 7/3.86/1
- `packaging` 7/3.57/1
- `startup` 7/4.57/1
- `urban` 7/3.71/1
- `niche` 6/0.33/6
- `fengshui` 6/2.5/5
- `yi` 6/1.83/5
- `legal2` 6/2.83/4
- `railway` 6/1.67/4
- `chinese` 6/2.5/3
- `project` 6/3.0/3
- `gardening2` 6/3.33/2
- `kids` 6/3.33/2
- `manufacturing` 6/2.83/2
- `accessibility` 6/3.67/1
- `aquaculture` 6/3.33/1
- `bonding` 6/3.17/1
- `bridge` 6/4.33/1
- `edu2` 6/4.17/1
- `forex` 6/4.5/1
- `futures` 6/4.0/1
- `glass` 6/4.17/1
- `maritime` 6/4.17/1
- `medical2` 6/4.33/1
- `pet-training` 6/3.67/1
- `petrochem` 6/3.67/1
- `plastic` 6/4.67/1
- `rubber` 6/3.5/1
- `seismology` 6/2.83/1
- `service` 6/4.83/1
- `shipping` 6/4.0/1
- `tunnel` 6/3.67/1
- `woodworking` 6/5.33/1
- `audit` 6/4.83/0
- `chess` 6/3.83/0
- `logistics2` 6/4.0/0
- `martial` 6/4.17/0
- `stage` 6/3.83/0
- `misc` 5/0.4/5
- `stats` 5/3.0/2
- `photo2` 5/4.2/0
- `misc2` 4/0.75/3
- `beekeeping` 2/2.5/1
- `daily-goods` 2/2.5/1
- `express` 2/3.0/0
- `network` 1/2.0/1

---

## 二、其他待处理

### P0 · 定时到期（不可忘）

- **重定向存根到期物理删除**：`_redirect_stubs_todo.md` 登记 6 个 `tools/pets/` URL，建存根 2026-10-10，**到期日 2026-11-10**。动作：① 物理删除存根（简体；zh-tw 由 CI 自动消失）→ ② commit/push → Actions success → ③ `python3 _submit_indexnow_deadlinks.py --file <死链列表.txt>`（默认校验）→ ④ 登记表改「已删（commit xxx）」。

### P1 · 真 bug（专项中挖出，未在本分类内清完）

- **全站 19 个「`type="number"` 却装逗号序列」输入框**：浏览器按 number 规则把非法值清空 ⇒ 默认样例失效、页面一进来就弹「请填写」。statistics 已清 14 个，余 **securities 4 / surveying 4 / metrology 3 / hotel 1 / insurance 1 / investment 1 / math 1**（`itinerary-planner`、`complete-life-expectancy`、`geometric-mean-return`、`arithmetic-mean-math`、`combined-uncertainty`、`tolerance-stackup-worst`、`type-a-uncertainty`、`capm-beta`×2、`information-ratio`、`tracking-error`）。修法：`type="number"` → `type="text" inputmode="decimal"`，改完跑对应分类 verify。
- **`_build.py` 相关工具卡 `rt-desc` 退化为工具名**：部分页卡片描述与名称完全相同（`Z 分数计算器 / Z 分数计算器`），降导流效果；需查 `_zh_desc_of` 取数源。

### P2 · 数据驱动 / 仓库卫生（择机）

- **GSC 收录数据刷新**：`_gsc_inspect_progress.json` / `_gsc_unindexed.csv` 停留 2026-08-07（6155 URL），可择机重跑 `scripts/_gsc_inspect_urls.py`（单次查询不循环）。
- **51.la / Clarity 月度复盘**：拉 PV、停留时长、二跳率，校准 UX 专项优先级（真实指标，验证 §1.1 代理指标是否奏效）。
- **`.git` 730MB 压缩**：`git gc --aggressive --prune=now`（执行前 `git status` 干净，执行后 `git fsck`）。

### P3 · 待老板定夺（不擅自开工）

- **新工具扩充**：受纯前端红线约束，如有方向走 `scripts/gen_*` 批量生成 + 中英文/指南三件套。
- **英文 i18n 残余全量审计**：`scripts/audit_all.mjs` 真机跑一轮确认 `?lang=en-US` 内容区零中文残留。

---

## 三、项目现状基线（实测，2026-10-13）

- 门禁 `scripts/run_gates.py` **218/218 全过**（含新增 UX 门禁项）；verify 逃生项 0；判别力 7733/7733。
- 工具 **5008 页 / 212 分类**（索引页 207），A 级率 **100%**；平均页大小 20KB。
- 交互形态基线（修正口径 ② 后）：UX-Score 均值 **3.89/9**，薄弱页 **733**；图表 8.7% / 明细表 29.3% / 导出 65.6% / 本地沉淀 23.1% / 预设 18.7% / 分步 16.7% / 对比 31.5% / 跨工具内链 **97.0%** / FAQ 98.2%（模板三件套「参数说明·适用场景·常见问题」高度同质，是「看一眼就走」的主因之一）。
- UX-Q4 基建已上线：组件库 `js/tool-kit.js` 全站注入、`_ux_baseline.py --gate` 门禁、S 档样板页 `geometry/triangle-heron`（1/9 → 5/9）。
- 试点 `statistics` B1–B4 已上线（35 页：3 页 S 档 + 32 页 A 档），**分类薄弱页已归零**，均分 1.67 → **6.10**；全站均分 3.65 → **3.92**、薄弱 1119 → **713**。
- 试点经验（下个分类直接照抄）：单分类从「最弱的一批」开始，每批 10–12 页，形态强制轮换；不碰计算内核，只追加包装器 + 语义 extras；每批必做页面级冒烟（静态用例全过 ≠ 页面不白屏）。
- 测绘口径已修正三次（同目录相对链接 / TBKit 运行时调用点 / diffBox 真实 API），**每次修正都会抬高基线**——因此跨批次对比分数时必须先确认口径版本，勿把口径修正误记为改造收益。
- 统计三件套已集成：百度统计 + 51.la + Microsoft Clarity，统一收口 `js/analytics.js`；广告埋点 `js/ad_metrics.js`。
- 索引三通道（IndexNow / Bing URL API / GSC Sitemap）crontab 运行中。
