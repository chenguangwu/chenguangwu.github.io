## 第 21 批（第 20 批返工）：同截面 RC 对照 + 未开裂/开裂分界（2026-11-05）

### 1. 返工原因（用户验收意见）

- **A 截面不可比**：第 20 批弹性解为 φ100 圆钢，RC 块统一 250×500 / A_s=1884 / C30，出现「弹性 2.037 mm vs RC 0.05 mm」，会被读成「混凝土比钢梁刚 40 倍」——差异实际来自截面。本批改为**等面积、等惯性矩反推等效矩形截面**（圆截面 b≈0.907d、h≈0.866d；ss 页只给 I，取 b=200mm 反推 h），并让 RC 准永久荷载默认等于弹性页荷载；结果区并列「弹性解截面 / RC 验算截面 / 等效偏差（面积、惯性矩）」三行，差异可解释而非免责。
- **B ψ 撞 0.200 下限**：σ_s 仅 26.2 / 2.6 / 6.6 MPa，ψ 原始值为负 → 构件实际**未开裂**，裂后刚度公式不适用。本批新增 `M_cr = f_tk·W_0`（W_0=bh²/6，未计塑性影响系数 γ，偏安全）判定：`M_q ≤ M_cr` → 未开裂，`B_s = E_c·I_0`、ψ/σ_s 显示「不适用（未开裂）」；`M_q > M_cr` 才走 `ψ → B_s → B`（式 7.2.3-1 + 7.2.2-2）。上批把「ψ_raw=−31.58 下夹取 0.200」当边界用例的写法**已废弃**——未开裂构件硬套裂后公式，夹取发生在物理无意义区间，属缺陷而非边界素材。
- **C 同类缺陷扩散排查**：`civil/beam-udl` 允许小 `q_q`（qk=2、qq=2 → σ_s=15.0、ψ 撞 0.200），同样未开裂；`civil/rc-beam-rebar`（裂缝宽度，M_k=1 → ψ_raw=−31.58）同病。两页一并按同一口径补 `M_cr` 判定，不只修 3 个 structural 页。

### 2. 同截面默认对照（默认准永久荷载，C30 f_tk=2.01 MPa / E_c=30 GPa）

| 页面 | 弹性截面 | RC 验算截面 | 等效偏差 | 弹性 δ_el | RC 判定 | RC B (kN·m²) | RC δ_lt |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `deflection-cantilever-point` | φ100 mm（A=7854 mm²，I=4.91e6 mm⁴） | 91×87 mm（A=7917 mm²，I=4.99e6 mm⁴，A_s=65 mm²） | 面积 0.8% / 惯性矩 1.7% | 0.272 mm | 未开裂（M_q=0.20 ≤ M_cr=0.23） | 75（B_s=150，θ=2.000） | 3.56 mm |
| `deflection-cantilever-udl` | 同上 φ100 | 同上 91×87 | 面积 0.8% / 惯性矩 1.7% | 2.037 mm | 已开裂（M_q=2.00 > M_cr=0.23） | 19（B_s=39） | 102.77 mm |
| `ss-point-deflection` | 矩形等效 I=1.00e-6 m⁴（上方未给面积） | 200×39 mm（A=7800 mm²，I=9.89e5 mm⁴≈0.989e-6 m⁴，A_s=58 mm²） | 惯性矩 1.1% | 8.333 mm | 已开裂（M_q=5.00 > M_cr=0.10） | 3（B_s=6） | 597.95 mm |

> 同截面下 RC 仍比钢梁柔，主因是材料模量差（E_c=30 GPa vs E_s=200 GPa，约 6.7 倍），不是截面差异；ss 页开裂后 σ_s=3416.8 MPa、B=3 kN·m²，是「等 I 反推 200×39 板 + 1% 配筋」的诚实结果（截面等效但配筋量由 1% 规则给出）。

### 3. 未开裂 / 开裂分支实测（用例注入值）

| 页面 | 未开裂分支 | 跨过 M_cr 分支 |
| --- | --- | --- |
| `deflection-cantilever-point` | `rcQ=0.115` → M_q=0.23 ≤ M_cr=0.2307，未开裂，δ_lt=**4.09 mm** | `rcQ=0.116` → M_q=0.232 > M_cr，已开裂，ψ_raw=−0.277→规范下限 0.200，B_s=78.7、B=39.4，δ_lt=**7.86 mm** |
| `deflection-cantilever-udl` | `rcQ=115` → M_q=0.23 ≤ M_cr，未开裂，δ_lt=**3.07 mm** | `rcQ=116` → M_q=0.232 > M_cr，已开裂，B_s=78.7、B=39.4，δ_lt=**5.89 mm** |
| `ss-point-deflection` | `rcQ=0.1` → M_q=0.05 ≤ M_cr=0.1019，未开裂，δ_lt=**1.12 mm** | `rcQ=0.205` → M_q=0.1025 > M_cr，已开裂，ψ_raw=−0.154→0.200，B_s=11.75、B=5.88，δ_lt=**5.81 mm** |
| `civil/beam-udl` | `qq=2` → M_q=9.00 ≤ M_cr=10.72，未开裂，δ_lt=**2.11 mm** | `qq=2.39` → M_q=10.755 > M_cr，已开裂，ψ_raw=−0.443→0.200，B_s=34328、B=17164，δ_lt=**2.35 mm** |
| `civil/rc-beam-rebar` | `Mk=1` → M_k=1.00 ≤ M_cr=20.94，未开裂，ψ 不适用、w_max=**0.000** | 默认 `Mk=80` → M_k=80 > M_cr，已开裂，σ_s=212.2、ψ=0.692、w_max=**0.214 mm** |

> 说明：未开裂区间已完全不进入裂后公式；开裂初期 ψ_raw 为负而取 0.200，是 GB 50010-2010 式 7.1.3 明文规定的下限（`ψ<0.2 取 0.2`），不再是「未开裂构件被硬套公式」的夹取。beam-udl 在 M_cr 临界处未开裂 δ（2.51 mm @qq=2.38）略大于开裂 δ（2.35 mm @qq=2.39），源于开裂初期 ψ 取下限时公式 B_s 略高于 E_c·I_0，属规范公式在临界点的衔接现象，随 M_q 增大即单调下降。

### 4. 校验与门禁

- `node scripts/verify_structural_calc.js` = **53/53**（原 3 条失效 RC 用例 → 6 条分支用例：point 4.09 / 已开裂，udl 未开裂 / 5.89，ss 未开裂 / 5.81）。
- `node scripts/discriminate_check.js verify_structural_calc.js` = **53/53 变红、0 逃生**。
- `node scripts/verify_civil_calc.js` = **73/73**（beam-udl 原 ψ 夹取用例 → 未开裂 + 跨 M_cr 两条；rc-beam-rebar 原 ψ 夹取用例 → 未开裂判定）。
- `node scripts/discriminate_check.js verify_civil_calc.js` = **73/73 变红、0 逃生**。
- 英文探针 `scripts/_en_i18n_probe.mjs --check`：`structural/deflection-cantilever-point` / `-udl` / `ss-point-deflection` / `civil/beam-udl` / `civil/rc-beam-rebar` = 5 页 **0 残留**（rc-beam-rebar 同批补齐长公式、表单元格、8 个 placeholder 等 12 条历史残留）。
- 构建保留判断：本批只改工具页内联脚本/正文、英文词典与台账；按约定**未跑 `_build.py`、未 push**，英文词典子树版本戳留待维护者构建时更新。

## 第 22 批：挠度页弹性解与长期刚度并列 + 双向板系数口径 + 锚固 200mm 下限（2026-11-05）

### 1. 三个 structural 挠度页：弹性解与 RC 长期刚度并列

- 口径：两套结果**并列输出、互不替代**。弹性解保留 `δ_el = F·L³/(3·E·I)`（悬臂集中力）、`δ_el = w·L⁴/(8·E·I)`（悬臂均布）、`δ_el = P·L³/(48·E·I)`（简支跨中集中力）；RC 长期刚度按 GB 50010-2010 7.1.1（`M_cr = f_tk·W_0`）判未开裂/开裂，未开裂 `B_s = E_c·I_0`、开裂走 `ψ → B_s → B = B_s/θ`（7.2.3-1 / 7.2.5-1 / 7.2.2-2），再按各页弯矩图形系数给 `δ_lt`（悬臂集中力 `(1/3)M_qL²/B`、悬臂均布 `(1/4)M_qL²/B`、简支跨中 `(1/12)M_qL²/B`）。
- `formula-eq` 同步写明两套公式、`M_cr` 判定、ψ 夹取 0.2~1.0、θ 与 `B`，以及各页 `δ_lt` 系数；弹性解在前作对照，RC 长期刚度随后并列。
- 默认实测：`deflection-cantilever-point` δ_el=0.272 mm / δ_lt=3.56 mm（未开裂，M_q=0.20≤M_cr=0.23）；`deflection-cantilever-udl` 2.037 / 102.77 mm（已开裂，M_q=2.00>M_cr=0.23）；`ss-point-deflection` 8.333 / 597.95 mm（已开裂，M_q=5.00>M_cr=0.10）。

### 2. `civil/two-way-slab`：系数口径与 `calc()` 对齐

- 原口径：公式框只写 `M_x = α_x·q·l_x²，M_y = α_y·q·l_x²（系数按 l_y/l_x 查表插值）`，未说明表值、插值方式与封顶；deep-dive 示例误写「3m×3m 四边固定、α≈0.036、3.24 kN·m/m」，FAQ 还把「简支/固定、塑性铰线」混在一起。
- 新口径（逐条对照 `__twsMoments()`）：四边简支、ν=0.2 跨中；`l_s=min(l_x,l_y)`、`l_l=max(...)`、`r=l_l/l_s`，`r>2.0` 按 2.0 封顶；表节点 `(1.0,0.0479,0.0479)`、`(1.2,0.0614,0.0384)`、`(1.4,0.0706,0.0328)`、`(1.6,0.0770,0.0286)`、`(1.8,0.0812,0.0256)`、`(2.0,0.0836,0.0234)`；相邻档按 `r` 线性内插；`M_x=α_x·q·l_s²`、`M_y=α_y·q·l_s²`，比值 `α_x/α_y`。示例改为「3m×3m 四边简支、α=0.0479、M_x=M_y=4.31 kN·m/m」，FAQ 明确本页不覆盖固定边/连续板。
- 算例（node 实跑，含 `toFixed(2)`）：默认 `(10,4,5)` → 10.19 / 5.92 / 1.72；`(10,4,4)` r=1 → 7.66 / 7.66 / 1.00；`(10,3,7)` r=2.333 封顶 → 7.52 / 2.11 / 3.57；`(10,4,4.8)` r=1.2 → 9.82 / 6.14 / 1.60。
- `content_deepdive.json` 的 scenarios / examples / faqs / summary 同批逐字同步（`indent=1`、EOF 无换行，diff 7/7 仅该条目）。

### 3. `civil/rebar-anchorage`：锚固公式与 200mm 下限

- 公式框已按 GB 50010-2010 式 8.3.1 / 8.3.2 校准：`l_ab = 0.14·(f_y/f_t)·d`、`l_a = max(ζ_a·l_ab, 200 mm)`；ζ_a 四款可自动判断项（d>25→1.10、环氧→1.25、扰动→1.10、保护层 3d→0.80/5d→0.70 线性内插、连乘下限 0.6）与代码 `__rebarZetaAutoCalc()` 一致。
- 本批补充 **200mm 构造下限临界**用例：`d=5.6` ⇒ `l_ab=197 mm`、`l_a=200 mm`（默认 705/705，注入后必不同）。

### 4. 校验与门禁

- `node scripts/verify_civil_calc.js` = **77/77**（新增 two-way-slab 3 条：方形 7.66、r 封顶 7.52/2.11、节点 1.2 的 9.82；新增 rebar-anchorage 200mm 下限 1 条）。
- `node scripts/verify_structural_calc.js` = **53/53**（第 21 批 6 条分支用例继续通过）。
- `node scripts/discriminate_check.js` = **9177 变红、0 逃生**，跳过 34（基线 35，需维护者同步下调）。
- 英文第三层词典同批更新：`i18n/tools/en/civil/two-way-slab.json`（新 formula-eq / formula-desc / 3 条 scenarios / 示例 / FAQ 答案）、`i18n/tools/en/structural/*.json`（三页新 formula-eq），`_en_override.json` 5 个 slug 的 `ed` 由占位串改为真实英文简介。
- 新增指南页：`guides/two-way-slab-guide.html`、`guides/rebar-anchorage-guide.html`（只建 html，未改 `json/guides.json`）。
- 构建保留判断：按本批纪律**未跑 `_build.py`、未 push**；英文词典子树版本戳与指南索引留待维护者构建时更新。

## 第 23 批：structural 公式框 ↔ calc() 一致性普查 + 前 10 页修正（2026-11-05）

### 1. 普查（27 页，四档）

- **A 档（公式/校验口径与代码不一致）6 页**：`beam-shear-center`、`bearing-pressure`、`moment-of-inertia-circle`、`polar-moment-circle`、`ss-udl-moment`、`von-mises-2d`。
- **B 档（≥2 个 number 输入却无 formula-box）0 页**：26 个工具页均有公式框。
- **C 档（公式正确但符号/单位/校验写法不严谨）4 页**：`cantilever-end-moment`、`slenderness-ratio`、`euler-buckling`、`section-modulus-circle`。
- **D 档（一致）17 页**：allowable-stress、angle-of-twist、axial-strain、beam-shear-stress、deflection-cantilever-point/udl、hoop-stress、longitudinal-stress、moment-of-inertia-rect、radius-of-gyration、section-modulus-rect、ss-point-deflection、stress-concentration、thermal-strain、torsion-polar-j、torsional-shear-shaft（另 index 不计）。

### 2. 前 10 页修正要点

- **A 档**：把「无强校验/按 0 兜底」「A=0 按 1 兜底」等与 `__tbInputGuard` 实况不符的表述，改为真实提示：缺项「请填写「X」后再计算。」、分母为 0「⚠「X」是本计算的分母，不能为 0。」；无守卫页保持「请输入必要参数后再计算。」。
- **C 档**：`euler-buckling` 补单位、守卫、算例与 K=1 适用条件；`section-modulus-circle` 明确 `S÷A` 的 mm 口径与 `max(A,10⁻⁹)` 兜底；`cantilever-end-moment` 明确 L=0 由分母守卫先拦截、公式内 1 兜底不可达；`slenderness-ratio` 补 λ 符号、r=0 守卫与 100 分级判据。
- 10 页默认态/注入态均不同（见 verify 用例 54/54）。
- 英文第三层词典 10 个文件同批补齐公式长键与 placeholder 译文；英文探针 10 页均 0 残留。

### 3. 校验

- `node scripts/verify_structural_calc.js` = **54/54**（新增 `bearing-pressure` A=0 分母守卫用例）。
- `node scripts/discriminate_check.js verify_structural_calc.js` = **54 变红、0 逃生、0 跳过**。
- `_test_static.py` = 4705/4705，0 失败 0 告警；inline marker 0 违规。
- 未跑 `_build.py`、未 push。

