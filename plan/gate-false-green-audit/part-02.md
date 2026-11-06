## 6. 混合锚逃生项全站普查（2026-11-05，只读）

### 6.1 机制与口径

`verify_*_calc.js` 的 `expect` 是「**数组中任一命中即通过**」。因此一条用例只要混进一个「**不注入输入、页面默认态本来就存在**」的字符串，其余精确断言全部作废——整条退化成逃生项（土建线实例：会变的 `M_k=180.00` 与不变的 `δ=24.01` 写进同一条，`δ` 默认态即命中）。

普查方法（只读，不改任何用例）：

1. 对每条 `CASES` 用例以 `inputs:{}`、`checkIds:[]`、`radios:{}`、`checks:[]`、`clicks:[]`、`expect:[]` 跑一遍（`expect` 置空 ⇒ 必失败 ⇒ harness 返回默认态全量文本 blob `fullBlob`）；
2. 逐项做 `blob.includes(expectItem)`，记录**默认态已命中**的项；
3. 与注入后命中项比对：只有 `hit` 无 `miss` = 整条退化；`hit` 与 `miss` 并存 = 同源混合锚。

范围：`scripts/verify_*.js` 中 207 个 `*_calc.js`（`verify_calc.js` 是冒烟式目标清单，无 `CASES/expect` 结构，不在口径内）；逐用例 8s 超时，`uncaughtException`/`unhandledRejection` 兜底推进。

### 6.2 总量

| 指标 | 数量 |
|---|---|
| 参与扫描用例 | **9126**（207 文件） |
| `expect` 混入默认态命中项 | **56** |
| 整条退化（默认态命中全部 expect，**真逃生**） | **49** |
| 同源混合锚（默认态命中部分 expect） | **7** |
| `expect` 长度 ≥3 | **7** |
| 超时无法判定 | 2 |
| 取不到 blob 无法判定 | 19 |

> 56 条里，43 条是 `expect` 只有 1 项的单锚用例（默认态即命中，整条完全判别力为 0）；13 条 `expect` ≥2，因 OR 语义同样整条退化。

### 6.3 清单① 疑似混合锚（`expect` ≥2 且至少一项默认态命中）——13 条，全部退化

| 判定 | 文件 | 用例 | expLen | 默认态命中项 | 仅注入后命中 |
|---|---|---|---|---|---|
| 整条退化 | verify_aerospace_calc.js | aerospace/flight-time | 2 | 16 小时 15 分钟 实际飞行时长；-13.0 时差 | - |
| 整条退化 | verify_design_calc.js | design/spacing-scale | 2 | space-4 9.8px；29.8px | - |
| 整条退化 | verify_engineering_calc.js | engineering/heat-transfer | 2 | 传热量 Q 40.00 W；热阻 R 0.5000 K/W | - |
| 整条退化 | verify_general_calc.js | general/calc-13 | 2 | 100 自然日；2400 小时数 | - |
| 整条退化 | verify_hydraulic_calc.js | hydraulic/pressure-drop | 3 | 1.168；2.67；0.00584 | - |
| 同源混合 | verify_hydraulic_calc.js | hydraulic/qudao-buchong-buyu-liusu | 3 | 0.7708；2.57（默认态计算值，非不变量） | 34.47 |
| 整条退化 | verify_hydraulic_calc.js | hydraulic/daohongxi-shuitousunshi-maishen | 3 | 0.2548；0.3058；0.5607 | - |
| 同源混合 | verify_life_calc.js | life/workday-calculator（3 条） | 3 | 周末（已排除）：0 天（合法恒值） | 自然日总数 / 工作日数 |
| 同源混合 | verify_psychiatry_calc.js | psychiatry/rater-23 | 4 | 默认 LSAS 整段（总分 0/144） | 重度社交焦虑；144/144；78/78 |
| 同源混合 | verify_psychology_calc.js | psychology/calc-12 | 2 | 最短板：生活满意度（0 分） | 幸福感总分 90/100 |
| 同源混合 | verify_science_calc.js | science/science-pressure-converter | 2 | 1.0000 m（默认单位） | 1.0000 μ |

判定口径：默认命中项是**默认态计算值**（qudao / pressure-converter / rater-23 / calc-12）⇒ 真逃生；是**与注入无关的合法恒值**（workday 的「周末 0 天」）⇒ 恒值本身合法，但因 OR 语义让整条失效，仍需拆条或改 AND 语义。

### 6.4 清单② 同源混合锚（恒定值 + 变化值同条）——7 条

即上表 6 条「同源混合」用例（workday ×3 计 3 条）。**共同缺陷**：不变量/默认值单独即可让整条 PASS，变化值断言等于没写。修法二选一：① 把不变量移出 `expect`（只留变化值）；② 若确需同时校验，把该条改用「全部命中才 PASS」的语义（需改 harness，影响面大，先做①）。

### 6.5 清单③ `expect` 长度 ≥3 ——7 条（风险最高）

| 文件 | 用例 | expLen | 判据 |
|---|---|---|---|
| verify_hydraulic_calc.js | hydraulic/pressure-drop | 3 | 3 项全在默认态命中 ⇒ 注入完全无效 |
| verify_hydraulic_calc.js | hydraulic/daohongxi-shuitousunshi-maishen | 3 | 同上 |
| verify_hydraulic_calc.js | hydraulic/qudao-buchong-buyu-liusu | 3 | 2 项默认命中，仅 34.47 需注入 |
| verify_life_calc.js | life/workday-calculator ×3 | 3 | 恒值「周末 0 天」默认命中，两条变化值作废 |
| verify_psychiatry_calc.js | psychiatry/rater-23 | 4 | 默认 LSAS 整段命中，3 条注入断言作废 |

### 6.6 真逃生高亮（49 条整条退化）

这 49 条的**分类门禁现在绿得毫无意义**（不注入任何输入也 100% PASS）：

| 文件（简写） | 用例 |
|---|---|
| acupuncture | needle-retention、needling-depth |
| admin | detector-time |
| aerospace | flight-time |
| agriculture | machinery-efficiency |
| audio | audio-cut |
| beauty | calc-2、skincare-routine |
| ceramics | glaze-temp |
| chess | xiangqi-endgame |
| chinese-cook | wok-heat |
| cognition | human-benchmark |
| dentistry | tongue-oral-health、wisdom-tooth |
| design | photo-print-size、spacing-scale |
| edu | convert-area-volume |
| electromagnetism | free-space-impedance |
| electronics | resistor-calculator |
| engineering | heat-transfer |
| film | color-grading |
| forensic-medicine | drowning-diatom |
| gardening2 | pest-control |
| general | calc-13 |
| hydraulic | pressure-drop、daohongxi-shuitousunshi-maishen |
| image | nine-grid-cutter |
| kids | stroke-order |
| language | idiom-solitaire |
| legal | court-fee |
| library | citation-format |
| life | age-in-days |
| mechanical | spring-rate |
| misc2 | travel/luggage-size |
| misc | science/physics-constants |
| music | ear-trainer |
| office | ~~mindmap~~ **已修复（2026-11-05）**：降级大纲 + 2 条判别用例，跳过 55→54 |
| ophthalmology | amblyopia-stereopsis |
| paper | paper-grade |
| pet | training-planner |
| rheumatology | anca-classification、behcet-hla、ssa-ssb |
| science | convert-power |
| startup | equity-calculator |
| stats | sample-size |
| tcm-diagnosis | etiology-tree |
| text | convert-6 |
| wedding | wedding-banquet |

典型形态：`expect` 锚的是**默认态就存在的静态表/空状态/错误提示**（`请添加会议日程并填写时间`、`请先上传图片`、`请检查网络连接后刷新页面重试`、`请至少输入一台有效农机数据`），或**默认输入的输出值**（`376.73`、`0.224809`、`3.842`、`14 桌`、`2,300`）。

### 6.7 结论

- **56/9126 ≈ 0.61%** 的用例存在默认态命中项；其中 **49 条完全丧失判别力**（`office/mindmap` 已于 2026-11-05 修复，**待修 48 条**）。
- 这批不是「用例写得不够精确」，而是**门禁语义（OR）与用例设计（多锚）冲突**。只要 harness 保持「任一命中即通过」，多锚用例必须满足「**每一项都只能由注入输入产生**」。
- 只出清单，不改用例；各分类线按 §6.3–§6.5 自行修条。优先级：清单③（expect≥3）→ 清单② → 清单① → 剩余单锚全命中。
- 2 条超时与 19 条无 blob 的用例**未判定**（可能含同类缺陷），需各线在页面可跑后复扫。

### 6.8 mindmap 修复记录（2026-11-05，本线）

- **页面**：库缺失分支新增纯 JS 降级大纲（嵌套 `<ul>` + `data-zh` 双语提示 + 「大纲节点：N」计数），并绑定 `input` 实时刷新；保留原加载失败提示，**未改** PNG/SVG 导出路径。
- **用例**：`office/mindmap` 由锚「库加载失败文案」（默认态必命中）重写为锚降级产物；另加 1 条反向用例（仅该条注入 `window.markmap` 桩，断言 `MARKMAP-STUB-OK` 只可能来自 markmap 分支）。
- **判别**：office 单文件 `已检 9 / 正确变红 9 / 逃生 0 / 跳过 0`；跳过基线 55 → 54（已检 4920 → 4922）。
- **断 CDN 真机**（Chrome headless，拦截 `cdn.jsdelivr.net` 3 个请求）：中/英两态均渲染 7 节点、层级 `1,2,3,3,2,3,4`，`pageerror = 0`。

### 6.9 待修 48 条的分派建议（按分类归属）

| 建议归属 | 条数 | 用例 |
|---|---|---|
| 临床/医学线 | 9 | dentistry/tongue-oral-health、dentistry/wisdom-tooth、ophthalmology/amblyopia-stereopsis、rheumatology/anca-classification、behcet-hla、ssa-ssb、forensic-medicine/drowning-diatom、tcm-diagnosis/etiology-tree、psychiatry/rater-23（同源）、psychology/calc-12（同源） |
| 土建/工程线 | 8 | hydraulic/pressure-drop、daohongxi-shuitousunshi-maishen、qudao-buchong-buyu-liusu（同源）、engineering/heat-transfer、mechanical/spring-rate、ceramics/glaze-temp、agriculture/machinery-efficiency、gardening2/pest-control |
| 数理/科学线 | 10 | science/convert-power、science/science-pressure-converter（同源）、stats/sample-size、misc/science/physics-constants、electromagnetism/free-space-impedance、electronics/resistor-calculator、general/calc-13、edu/convert-area-volume、aerospace/flight-time、design/spacing-scale |
| 生活/文化线 | 11 | life/age-in-days、life/workday-calculator ×3（同源）、wedding/wedding-banquet、kids/stroke-order、music/ear-trainer、chess/xiangqi-endgame、language/idiom-solitaire、library/citation-format、text/convert-6、chinese-cook/wok-heat |
| 设计/影像/内容线 | 6 | design/photo-print-size、image/nine-grid-cutter、film/color-grading、audio/audio-cut、beauty/calc-2、beauty/skincare-routine |
| 杂项线 | 5 | admin/detector-time、pet/training-planner、startup/equity-calculator、legal/court-fee、cognition/human-benchmark、misc2/travel/luggage-size、paper/paper-grade |
| 办公线（本线） | 0（已修） | office/mindmap（降级渲染 + 反向桩用例） |

注：同源混合锚的修法统一为「把恒定值/默认值移出 `expect`，只留注入后才出现的变化值」；`expect≥3` 的三条（pressure-drop / daohongxi / qudao）需优先拆条。

## 7. 新增门禁登记（两条均已接入：verify input ids #228 / deepdive source sync #229）

| 项 | 状态 | 条目原文 | 脚本 / 语义 | 造红方式 | CI 耗时 | 当前是否预期红 |
|---|---|---|---|---|---|---|
| `verify input ids` | **已接入（#228）** | `("verify input ids", ("node", "scripts/audit_verify_input_ids.js"))` | `scripts/audit_verify_input_ids.js`：扫描 207 个 verify 文件 / 8963 条用例 / 28180 个注入键，比对注入键在对应页面 HTML 是否存在；**僵尸 id 即 exit 1**（动态生成/模板拼接判为存疑不算违规） | 修好某条僵尸 id 用例前天然红；绿路径已用 `verify_sports_calc.js` 单文件验证 exit 0 | **1.3s**（纯 node 标准库，无 node_modules/浏览器） | **是，41 条僵尸 id**（22 条 `detector-*` 优先），由用例修复线收口，禁止调口径改绿 |
| `deepdive source sync` | **已接入（#229）** | `("deepdive source sync", ("python3", "scripts/audit_deepdive_source_sync.py", "--check"))` | 页面 deep-dive 段与 `content_deepdive.json` 逐字不一致即 exit 1（`--report` 只列不判红） | 临时改某页 deep-dive 段一个字 → `--check` 必须 exit 1 | **0.9s**（扫描 4573 页，纯 python3 标准库） | 接入时已绿：土建线 `a9c57d5a2f` 已同步 `civil/rc-beam-rebar` scenarios，`--check` 0 不一致 |

### 7.1 验收时发现并修复的脚本缺陷（verify input ids）

`audit_verify_input_ids.js` 通过 `require(verify_it_calc.js)` 复用 `extractCases`，而 harness 的 `beforeExit` 兜底会在「0 用例执行」时打印 `❌ 0 个用例实际执行…` 并**覆盖 `process.exitCode = 1`** —— 即使 41 条僵尸 id 全部修完，该门禁也**永远无法转绿**。已加 1 行 `process.env.TB_DISCRIM_PARENT = "1"`（harness 已有的父进程逃生口）抑制兜底；已验证：全量 exit 1（41 条僵尸）、`verify_sports_calc.js` 单文件 exit 0，且不再出现该误导行。

### 7.2 条目数口径

- 当前：**229**（227 + `verify input ids` #228 + `deepdive source sync` #229）；
- `--skip-build` 后实际执行 **228**（摘除 `build`，首项仍为 `expect anti-pattern`）；
- 每次变更必须同批更新 `scripts/gates_manifest.txt`，否则清单棘轮在启动时判红（已验证「少一条 / 多一条 / 乱序」三个方向均 `SystemExit`）。

背景：设计生活线普查 4726 条 deep-dive（一致 4569 / 无对应页面 153 / **有差异 4**）。那 4 条（`dic-scoring`、`ipss-r`、`cml-monitoring`、`mpn-scoring`）页面已由临床线修正，但 `content_deepdive.json` 仍是 2026-09-09 旧值；`_build.py` 在页面找不到 deep-dive 段时会用 JSON **重建整段**，因此跑一次构建就会把修复回退。门禁用于拦截「页面已改、JSON 未同批改（indent=1）」的状态。

接入约束（插入时必做）：

1. **条目总数 227 → 228**，同批更新 `scripts/gates_manifest.txt`（清单棘轮会拦「多一条未登记」）；
2. 插入位置按运行时线惯例放 `GATES` 末尾（不影响「首项 expect anti-pattern」与「--skip-build 摘除恰为 {build}」两条断言）；
3. 插后重跑 `--skip-build` 造红（首项改名 / build 改名），并在干净 worktree 口径验证脚本无依赖（纯 python3 标准库）；
4. 造红：临时把某页 deep-dive 段改一个字 → `--check` 必须 exit 1 并报「页面与 source 不一致」。

### 7.3 【硬条款】全量门禁只在 detached worktree 跑，主工作区只允许 `--skip-build`

> **2026-11-05 事故定论**：`run_gates.py` 第 2 项 `build`（`_build.py`）**不是只读门禁，是对共享工作区的写操作** —— 它会重写 `json/*.json`、`sitemap.xml`、`zh-tw/`，并在页面里找不到 `_dd_html` 时**用 `i18n/tools/content_deepdive.json` 整段重建 deep-dive**。实测 05:08:43/44 把 `hematology/cml-monitoring`、`hematology/mpn-scoring` 两页 clinical 线刚修好的 deep-dive 按旧 JSON 回写；**回写后全量门禁仍全绿**，因为它验证的就是回写后的状态。在 11 条线并行改同一仓库的前提下，任何一次主工作区全量都可能静默回退他线在途修复。

**硬性规矩（无例外）**：

1. **全量（含 `_build.py`）只在 detached worktree 里跑**：
   ```bash
   git worktree add --detach /tmp/gate-run HEAD
   cd /tmp/gate-run && python3 scripts/run_gates.py            # 完整 229 项
   cd /tmp/gate-run && python3 scripts/run_gates.py --skip-build  # 快速反馈
   ```
   跑完 `git worktree remove --force /tmp/gate-run`。worktree 里 `_build.py` 的写入全部落在 `/tmp/gate-run`，**主工作区字节不动**。
2. **主工作区只允许 `--skip-build`**：它摘除 `build`（按命令首项 `python3 _build.py` 识别，`prune_build_gate` 断言摘除集合恰为 `{build}`），不产生任何构建写入。
3. **每次全量跑完必须报 `git status --short` 的条数**（worktree 内跑则报主工作区的条数，作为「这次跑动了什么」的证据；条数较上次异常增减即需逐条解释）。
4. **发现他线页面/JSON 被回退，只报告清单，不得自行 revert**：涉及别线在途内容，由统一维护者处置；本线只提供证据（文件路径 + 差异字段 + 回写时间）。
5. **本线自己改页面的批次**：仍按项目原流程在**主工作区**手改 + 收尾构建 + 提交（构建是提交前的最后一步）；**门禁全量验证**改用 worktree 对同一 HEAD 复跑，避免二次构建写主工作区。
6. **【验收口径】** 全量门禁的「通过」必须来自 **detached worktree @ HEAD**，且必须同时报 `git status --short` 条数；主工作区的 `--skip-build` 结果**只作快速反馈，不作为发布依据**。理由：主工作区的树随时被 11 条线改动，**在主工作区跑出来的绿，绿的可能是别人未提交的半成品**。
7. **【构建产物归属】主工作区的构建产物不由本线 revert / 不由本线提交**：留给集成线统一入库（它们本来就是构建输出，push 时必须带上）。
   - 2026-11-05 报告时点待集成入库 **124 条**：构建产物类 **18**（`json/*.json` 14 + `sitemap.xml` + `sitemap.html` + `index.html` + `sw.js`）+ 分类索引 **15**（`tools/<行业>/index.html`）+ 工具页 **79**（他线在途源码改动）+ 源文件 **12**（i18n/js/scripts/`AGENTS.md`）；`zh-tw/` 为 gitignore，不进 status。
   - 任何人不得把上述产物当垃圾清掉；数量随他线提交变动，以跑全量时实测条数为准。

### 7.4 防回退措施有效性证据（幂等重放）

`hematology/cml-monitoring.html`、`hematology/mpn-scoring.html` 的 mtime 为 **05:09:55 / 05:09:57**（构建确实写了这两页），但**内容与 HEAD 逐字一致、`git status` 为 clean**，且全站 `audit_deepdive_source_sync.py --check` 为 **0 页不一致**。

即：当「页面修复」与 `content_deepdive.json` 源头**同批同步**之后，`_build.py` 的 deep-dive 回写从**破坏性覆盖**变成**幂等重放**（写入但产出与 HEAD 相同，不产生 diff）。这是 §7.3 与 `deepdive source sync` 门禁有效的正面证据，不只是「又加了一条门禁」。

## 8. 第 ⑧ 种假绿形态：判别器「模拟注入失败」仍派发事件（2026-11-05，本线）

**编号**：⑧。前七种为：① 汇总行在检查前打印（检查结果不进汇总/退出码）　② `except: pass` 吞异常　③ 未完成即 `return 0`　④ 阈值吞失败　⑤ 子进程红、父进程报通过　⑥ 脚本没挂进 `run_gates.py`　⑦ 同名函数遮蔽（后定义覆盖前定义）。本形态与它们同级：**检查确实跑了，但「失败态」本身构造错了**，因此结果反向。

**现象**：`scripts/discriminate_check.js` 全站报「仍 PASS(逃生项): 0」，同一时刻按「纯默认态」普查 `expect`，却有 76 条用例的锚在默认态即命中（见 §6）。两份结果直接矛盾。

**根因（代码级）**：旧 `sweepFile()` 的「模拟注入失败」= 把 `inputs` 逐键换回页面 HTML 默认值 + 清空 `checkIds/radios/checks/clicks`，然后**仍然走 `runCase` 正常流程**。`runCase` 在注入阶段对每个控件派发 `input/change/keyup`（见 `verify_it_calc.js` 的 `if (c.inputs)` 段），页面 `calc()` 随即重渲染，把**加载期扫描表 / 枚举表**冲掉：

- `acoustics/critical-distance`：纯默认快照含 `1.14 临界距离 r_c (m)`（Q=2 那一行来自加载期扫描表），回退路径却判成「正确变红」；
- `thermodynamics/heat-conduction`：`600000.0 热流密度` 同理（扫描表被事件重绘覆盖）；
- `quantum/hydrogen-energy-level`：能级表同理。

**真实注入失败 = 纯默认态、不触发任何事件**：页面从未收到事件，加载期表格仍在，锚照样命中 ⇒ 该用例本来就没有判别力。

**判据（硬性，混合锚必须按此口径）**：

1. 用 `snapshotOnly: true` 取快照（只执行页面脚本与 `DOMContentLoaded`，只还原浏览器默认态：select 首项、HTML 已勾选的 checkbox/radio）；
2. 只传 `slug` + 保真开关 `afterLoad / dynDom / dynInputs`，**不传** `inputs / checkIds / radios / checks / clicks`；
3. 不跑无参兜底函数、不派发任何 `input/change/keyup`；
4. `expect` 任一锚在快照 blob 中命中即「逃生项」；匹配口径与 harness 的 OR 语义、`blobHasWant` 的「原文 / HTML 转义」双路一致。

**口径切换实测（旧 → 新）**：

| 项 | 旧口径（回退值 + 事件） | 新口径（纯默认快照） |
|---|---|---|
| 已检 | 9196 | 9177 |
| 正确变红 | 9196 | 9123 |
| **逃生项** | **0（假绿）** | **54** |
| 跳过 | 21 | 40 |

基线 `scripts/discriminate_baseline.json` 同批改为 `54 / 9177 / 40`；随后本批换锚 25 个（23 条用例，11 文件）后逃生 **54 → 31**。

**推论（校准其他线的口径）**：「0 逃生」在未按本口径复跑前**不可信**，尤其依赖加载期扫描表 / 枚举表的页面。凡线报「逃生 0」，应要求同时给出「纯默认快照 vs `expect`」的命中清单，而不是只看判别器汇总行。

**提交**：`c0d5626448`（判别器口径 + 基线）、`69535cbdd0`（批 2 锚清理）、`0068a3ec59`（批 3 锚清理）。

### 8.1 影响面（2026-11-05 实测，供其他线按图复跑）

**结论**：凡以「批跑 / 带事件快照」报出的「0 逃生」一律不可信，必须按**纯默认态快照**（§8 判据）复跑。实测纯默认快照命中 **86 个锚 / 76 条用例 / 39 个 verify 文件**——这 39 个文件此前任何「0 逃生」的结论都应视为未验证。

| 行业验证文件 | 默认即命中用例 | 锚 |
|---|---|---|
| acoustics | 10 | 11 |
| aerospace | 5 | 6 |
| thermodynamics | 5 | 5 |
| electromagnetism | 5 | 5 |
| ai | 4 | 4 |
| quantum | 3 | 4 |
| economics | 3 | 3 |
| metrology | 3 | 3 |
| statistics | 3 | 3 |
| design | 2 | 3 |
| optics | 2 | 3 |
| life | 2 | 2 |
| surveying | 2 | 2 |
| dermatology | 1 | 2 |
| general | 1 | 2 |
| reproductive-medicine | 1 | 2 |
| rheumatology | 1 | 2 |
| welding | 1 | 3 |
| accounting / biz / chemistry / chess / chinese-cook / civil / construction / cosmetic-derm / dynamics / energy / geometry / hematology / investment / kinematics / legal / nuclear / obstetrics / pulmonology / science / securities / urban（21 个） | 1 | 1 |

**优先复跑序**：acoustics、thermodynamics、quantum（加载期扫描表/能级表）、aerospace、electromagnetism、metrology、statistics（枚举/表格类），其余按上表。

本线进度：批 1 `bfc76248c9`（21 锚 / 13 文件，旧口径下识别）、批 2 `69535cbdd0`（25 锚 / 23 用例 / 11 文件，新口径）、批 3 `0068a3ec59`（6 锚 / 5 文件）；逃生 54 → 25，剩余 **19 条全锚命中 + 6 条部分命中**。

## 9. 批跑口径 vs 隔离口径（2026-11-05，只读）

> 起因：`js/tool-i18n.js` 的 `isNumericSep` 收窄时需要报「全站 `--check` 残留前后对比」，实测发现**同一页在批跑里 7 条、隔离单页跑 0 条**——批跑数字不可用。

### 9.1 现象

| 观测 | 结果 |
|---|---|
| 全站一次性批跑 `node scripts/_en_i18n_probe.mjs --check <所有行业>`（4705 页同进程） | `marketing/assessor-51` 残留 **7 条** |
| 同一页隔离跑 `node scripts/_en_i18n_probe.mjs --check marketing/assessor-51` | 残留 **0 条**（重复 2 次一致） |
| 同版本两次全站批跑 | 页级结果相差 **153 页**（`marketing` 32 / `realestate` 50 / `science` 73 等整行业凭空多出） |
| 反向校验（`isNumericSep` 收窄只会多转、不会多留） | 批跑却出现「新判据残留更多」，**违反单调性** ⇒ 证明是采样噪声 |

### 9.2 根因

`_en_i18n_probe.mjs` 用 jsdom 加载页面，第三层英文词典（`i18n/tools/en/<ind>/<slug>.json`）与行业短语包是**异步加载**的；探针的 `settleStable()` 只等一小段时间。批跑时进程内累积了大量页面/资源句柄，事件循环被拖慢，**部分词典还没落地就完成采样**，页面仍是中文 → 计为「残留」。隔离单页时加载压力小，词典必然在窗口内完成，故为 0。

同一机制解释了「整行业凭空多出」：一个进程里某行业的词典加载失败，该行业所有页同时变红。

### 9.3 判据（写死）

- **任何「全站批跑」得出的数字只能作候选发现，不能作验收结论**；
- **验收必须逐页隔离复跑**（单页一进程，或 ≤14 页小批并**重复跑一次取一致值**）；重复跑不一致即该批作废；
- 报告里出现「扫 N 页得 M 条」时，必须写明：进程数、批大小、是否重复跑一致；
- 对**单调性可证**的改动（如判据收窄），批跑结果若违反单调性，直接判为噪声、以隔离口径为准。

### 9.4 影响面

1. **i18n 残留统计**：`_en_i18n_probe.mjs --check` 的所有批跑结论（含此前若干批「0 命中」「残留 2834 页」）；
2. **探针类扫描**：任何依赖异步资源加载后取快照的脚本（`runtime_scan.js` 的 `settleStable` 同类风险；其单页模式受影响小，多页连续跑需抽验）；
3. **任何「扫 N 页得 M 条」的结论**：门禁/审计报告里的聚合数字，一律需注明采集口径；批跑数字只能写「候选」，不能写「通过」。

### 9.5 本次实证（用于校准）

- 14 页回归清单：小批同进程、重复 2 次结果一致（31 条/9 页 → 21 条/8 页）；
- 全站确定性替代口径：对 4912 个 HTML 做**静态文本节点**模拟同一算法，17 → 3（修复 14 节点/12 页，反向新增 0），与 jsdom 无关、可重复。

