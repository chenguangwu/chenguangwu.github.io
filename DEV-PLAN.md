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
4. **i18n 同步**：新文案进 en 字典（`?lang=en-US` 内容区零中文），`data-zh` 按既有机制标注。
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

### 1.7 当前分类（进行中）

**试点：`statistics`（52 页 / 起点均分 1.67 / 薄弱 46；当前 均分 7.58 / 薄弱 0）** —— 语义最适合图表化（分布、检验、抽样），已用它跑通 SOP 与组件库。
按 6 批推进；批次清单在此动态登记、干完即删（完成的批次只留计数，细节写当日 memory）。

- [x] **B1–B4 已完成 35 页**（B1 3 页 S 档 + B2/B3/B4 各 10–12 页 A 档）：分类均分 1.67 → **6.10**、薄弱 46 → **0**。
- [x] **B5 已完成 8 页**（p/t/z/statistics/statistics-4/5/7/10）：均分 6.10 → **6.81**；顺带修复多页正态 CDF 漏除 √2 真 bug。
- [x] **B6 已完成 10 页**（statistics-11/12/13/16 + sample-size-proportion/sample-variance/skewness-sample/cramers-v 从零接入；chi-square-test/coefficient-of-variation 补图表）：均分 6.81 → **7.58**、薄弱(≤2) **0**。
- [x] `index` 页：分类索引页（无输入），按导航页处理，不做图表。
- ⚠️ **待老板决策（不擅自执行）**：已诊断出分类内功能重复 —— `p`↔z-score-calc、`t`↔t-score、`z`↔z-score-calc、`statistics`↔normal-cdf、`statistics-16`↔linear-regression、`statistics-10`↔coefficient-of-variation、`statistics-13`↔stddev-list/variance-list、`statistics-5`↔sample-size-mean。**清理需下线 URL（走 `sitemap-deadlinks.xml`），影响 SEO，须老板批准后才动**；此前 B5/B6 已照常做体验改造，不删页。
- 📌 **分类收口结论**：52 页全部达 7–8/9（仅余 11 个 7/9 页缺图表+tabs，已属高质量，可选补图表）。`statistics` 试点达成「个性化 + 驻留/跨工具」目标，SOP 与组件库 `js/tool-kit.js` 已固化。

**当前分类切换：`ai`（65 页 / 起点均分 2.31 / 薄弱 47）** —— 紧接 statistics 后开工（最弱优先）。ML 超参/训练类数值计算器，语义适合「图表分析（衰减/预热/损失曲线）+ 明细表 + 预设 + 历史对比」。

- [x] **AI-1 已完成 7 页**（lr-decay/lr-warmup/dropout/l1-l2-regularization/cross-entropy/epoch-time/min-max）：单页 2–3/9 → **8/9**；接入图表/明细表/预设/历史/对比/CSV 导出；boot 推迟到 DOMContentLoaded 避开 tool-kit.js(defer) 时序。
- [x] **AI-2 已完成 8 页**（sigmoid/softmax/relu-leakyrelu/precision-recall/roc-auc/cosine-similarity/elbow-wcss/rmse）：单页 3–4/9 → **8/9**；范式轮换（line×3 sigmoid/relu/roc-auc、bar×3 pr/elbow/rmse、pie softmax、scatter cosine，均 ≤40%）；roc-auc 自实现 erf 高斯重叠图、cosine 向量散点；真实加载顺序冒烟 63 页零抛错。
- ⚠️ **顺带修复系统性首屏回归**：统计 B1–B6 共 48 页此前用「解析期直接 calc()/__xxPresets()」，因 tool-kit.js 为 defer，首屏 TBKit 未定义导致图表/预设/历史全部跳过（仅手动重算才出现，线上不可见但无报错）。统一改为 DOMContentLoaded 后渲染，已用真实加载顺序冒烟验证 55 页全部首屏可见、零抛错。
- [x] **AI-3 已完成 10 页**（cohens-kappa/transformer-params/training-flops/vram-estimate/context-window/temperature-scaling/k-means/model-accuracy/flops/attention-flops）：单页 3–5/9 → **8/9**；范式轮换（line×3 vram/flops/attention、bar×3 kappa/k-means/temperature、gauge×2 context/accuracy、pie transformer、scatter training，累计 line 40%/bar 36% 不超上限）；数值独立复算 28 项全对；真实加载顺序冒烟 73 页零抛错。
- [x] **AI-4 已完成 12 页**（attention-head-dim/auc-rank/best-epoch/grad-accumulation/inference-throughput/quantization-ratio/softmax-2/specificity/steps-per-epoch/token/token-usage/multi-agent-overhead）：单页 3/9 → **8/9**；范式 bar×5/pie×4/gauge×2/scatter×1（累计 bar 37.8%/line 27% 合规）；数值独立复算 16 项全对；真实加载顺序冒烟 85 页零抛错。
- [ ] AI-5+：剩余 28 页（3–4/9，含 ai-4~17 模板系/ocr/rag/sentiment 等），继续按薄弱度推进。

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
- `legal` 53/1.96/37
- `edu` 48/4.65/5
- `marketing` 47/3.98/11
- `surveying` 45/1.89/31

#### W2 中坚（20–44 页，按薄弱数降序先啃最弱，2472 页合计）

- `math` 42/1.64/34
- `accounting` 36/1.86/29
- `metrology` 30/1.3/29
- `acoustics` 29/1.31/29
- `geometry` 29/1.17/29
- `robotics` 29/1.07/29
- `materials` 42/2.05/28
- `healthcare` 36/2.42/28
- `insurance` 34/1.71/28
- `aerospace` 38/2.32/27
- `securities` 36/2.14/27
- `electromagnetism` 27/1.15/27
- `chemistry` 38/1.89/26
- `quantum` 28/1.32/26
- `signal` 28/1.75/26
- `kinematics` 26/1.23/26
- `banking` 26/1.77/25
- `investment` 26/1.58/25
- `optical` 42/2.14/24
- `fluid` 24/1.21/24
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
- `process` 15/1.27/14
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
