## 第 13 批：硬编码规范限值专项 + 结构/岩土族 + `|| 默认值` 吞 0

### 扫描口径与结果（2026-11-05）

- 范围：`tools/civil/` 25 页、`tools/structural/` 27 页、`tools/construction/` 38 页，共 **90 页**（其中 3 页为行业 `index.html`，实际工具页 **87 页**）。
- 扫描脚本区数值字面量（`[NUM]` 标记）**80 处**，逐条人工分拣出「规范限值形态」候选 **15 处**：
  - **推导值被写死（必修）2 处**：`calc-1` 的 φ 分段表（末端 `return 0.3`）、`masonry-bearing` 的 φ 固定输入框（默认 1.0）。
  - **跨规范混用 / 引用不符（登记）4 处**：`calc-206`（GB 55023 的 1.3/1.5 与 JGJ 130 的 `0.9×1.4` 混用，页内已注明出处、无内部矛盾，维持不动）、`cft-capacity`（引 GB 50936 实为 `A_s f_y + 1.2 A_c f_c` 简化叠加）、`dijichengzailijisuan`（引 GB 50007 5.2.4 实为 Terzaghi `qu`）、`assessor-19`（`βz=1+0.038√H` 为经验式，非 GB 50009 第 8.4 节计算值）。
  - **正常 9 处**：`isolated-footing` `p_max≤1.2f_a`、`load-combination` 1.3/1.5、`rebar-anchorage` `max(200, ζ_a l_ab)`、`slope-stability-fos` 分级阈值、`calc-204` `1.5q` 与 `1.3(g)+1.5q`、`calc-206` φ 表（JGJ 130 表 A.0.6 一致）、`two-way-slab` 弹性系数表（经验系数已标注）等。

### 本批修改页面

| 页面路径 | 页面声称的标准 / 条款 | 代码实际采用 | 偏差与处置 | 是否已核对 |
|---|---|---|---|---|
| tools/construction/calc-1.html | JGJ 130-2011 附录A 表A.0.6（Q235 钢）稳定系数 φ | φ 由 λ 按表 A.0.6 线性插值（20→0.998 … 250→0.120），λ>250 取表末值并提示专项验算；`k` 改 NaN 回退 | **推导值写死（必修）**：原分段表末端 `return 0.3` 且与 JGJ 130 表不符（λ=169 原给 0.3，应为 0.264）；默认态由 31.81 kN/65.1% 变为 27.32 kN/72.5% | 是 |
| tools/civil/masonry-bearing.html | GB 50003-2011 式 D.0.1-3 轴心受压影响系数 | `φ=1/(1+αβ²)`，α：M5 及以上 0.0015、M2.5 0.002；删除 φ 输入框，改为按 β 实算 | **推导值写死（必修）**：原 φ 固定输入 1.0，与页面「φ 由高厚比查表确定」自相矛盾；β=12.5 时 φ=0.810，承载力 1458 kN | 是 |
| tools/civil/excavation-earth.html | Rankine 主动土压力；φ 声明 0–45° | 守卫由 `φ≤0` 改 `φ<0`（φ=0 合法，K_a=1），空串单独拦截 | 边界拒绝错误：原代码拒绝合法 φ=0 | 是 |
| tools/civil/slope-stability-fos.html | GB 50330-2013 表 5.3.1 边坡稳定安全系数 | 阈值文案改为一级 1.35、二级 1.30、三级 1.25，删除「永久 1.5」错误表述 | 文案与规范不符（代码按用户等级判定） | 是 |
| tools/civil/dijichengzailijisuan.html | Terzaghi/Meyerhof 极限承载力 | 参考表改为 `qu` 与 `f_a≈qu/K`，注明 GB 50007-2011 5.2.4 的 η_b/η_d 深宽修正本工具未实现 | **跨规范引用不符（登记并改引用口径）** | 是 |
| tools/civil/cft-capacity.html | GB 50936-2014 钢管混凝土 | 参考表改为本工具简化叠加 `A_s f_y + 1.2 A_c f_c`，注明 1.2 为经验系数、正式设计按 GB 50936 | **跨规范混用（登记并注明）** | 是 |
| tools/construction/assessor-19.html | GB 50009-2012 风荷载 | βz 标签改「经验估算」，注明 `1+0.038√H` 非第 8.4 节计算值 | **跨规范引用口径（登记并注明）** | 是 |
| tools/structural/bearing-pressure.html | `q=N/A` | `N` 由 `N||1` 改 NaN 回退；N=0 输出 p=0 并提示「竖向力为 0」，不再替换为 1 kN | **`||` 吞 0**：原 0 荷载按 1 kN 算，给出看似合理的错误值 | 是 |
| tools/construction/pipe-flow.html | 水的运动粘度温度修正 | `temperature||20` 改 NaN 回退；ν 改 Vogel 式（0°C≈1.75e-6、20°C≈1.00e-6 m²/s） | **`||` 吞 0**：0°C 为合法冷藏/冬季工况；同配置 0°C 水头损失比 20°C 高约 8%（ν 近 1.75 倍） | 是 |
| tools/construction/area-calculator.html | 公摊率 → 得房率 | `rooms`、`shared` 改 NaN 回退；`shared=0` 合法（得房率 100%），并拦截 `<0 / ≥100` | **`||` 吞 0**：0% 公摊为合法输入 | 是 |
| tools/construction/window-shading.html | 几何外遮阳近似 | `hour` 改 NaN 回退，0 时（午夜）原样进算 | **`||` 吞 0** | 是 |
| tools/civil/calc-2.html | 钢筋下料长度 | `num` 改 NaN 回退，0 根合法 | **`||` 吞 0** | 是 |
| tools/construction/timber-volume.html | 原木材积 | `logQty`、`boardQty` 0 合法 | **`||` 吞 0** | 是 |
| tools/construction/estimate-area-dosage.html | 涂布用量估算 | `coats` 0 合法 | **`||` 吞 0** | 是 |
| tools/construction/soundproof-material.html | 隔声材料层数 | `layers` 0 合法 | **`||` 吞 0** | 是 |

### 维护备注（第 13 批）

- 结构力学族核对 27 页：受弯配筋（rc-beam-rebar、one-way-slab、two-way-slab）、挠度/裂缝（beam-udl、deflection-*）、剪力箍筋（beam-shear-stress 等）、地震组合（load-combination、calc-206）、稳定性（slenderness-ratio、euler-buckling、allowable-stress、calc-1）。除 calc-1 φ 表外，公式与单位（kN/N/MPa）均一致；`ξ_b` 派生限值已在第 12 批改为实算。
- 岩土族核对 9 页：`isolated-footing`（1.2f_a 正常）、`dijichengzailijisuan`（已改引用）、`pile-capacity`（R_a/K 正常）、`slope-stability-fos`（阈值文案已修）、`excavation-earth`（φ=0 边界已修）、`active-earth-rankine`（第 12 批已修 φ=0）、`cft-capacity`（已注明）、`masonry-bearing`（φ 实算）、`rock-mass-rating`（RMR 计分正常）。
- 本批新增/更新 verify：`calc-1` 期望改 21.00 kN / 98.6%（φ=0.2415）、`masonry-bearing` 去 phi 输入并改 4041 kN/0.910、新增 `pipe-flow` T=0、`window-shading` hour=0、`area-calculator` shared=0、`excavation-earth` φ=0 边界用例；`assessor-19` 锚串随标签变更。
- 门禁：`verify_civil_calc` 50/50、`verify_construction_calc` 38/38、`verify_structural_calc` 47/47、`verify_general_calc` 362/362 全绿；fidelity 逃生 0（civil 50/50、construction 38/38）；all_default 0（四套均 0）；`_test_static.py` 4705/4705、0 告警；`_audit_assets.py --check` 0 死链 / 0 lang 缺失 / 0 重复 id。

### 维护备注（第 14 批：施工临时结构族 + 工程量族）

临时结构族核对 9 页，确证缺陷 4 处：

| 页面 | 缺陷 | 修正与规范出处 |
|---|---|---|
| tools/construction/calc-1.html | 计算长度用 `l₀=k·h+2a`（非规范式），且输入把 k=1.155 标成「计算长度系数 μ」 | 改为 `l₀=k·μ·h`（JGJ 130-2011 §5.3.3；k=1.155 附加系数，μ 按表5.3.3 二步三跨 1.5 / 三步三跨 1.7）；新增 μ 输入、删除 a 输入。默认态 48.3/3.6/1.8/μ=1.5：λ 169→196.8、N_Rd 27.32→20.03 kN、利用率 72.5%→98.9%（仍「满足」，结论未翻转） |
| tools/construction/calc-1.html | 深度解析仍写「稳定承载力约 30–40 kN/根」，与 A.0.6 实算 φ 差约 2 倍（危险的方向：低估需求） | 改为 Φ48×3.0、h=1.8、μ=1.5 实算 λ=195.6、φ=0.195、N_Rd≈17.0 kN |
| tools/construction/calc-1.html | 引据表仍写 `N=1.2×NG1K×H+1.2×NG2K+1.4×ΣNQK` 并指向 JGJ 130-2011 §5.2.6，与代码已用 1.3/1.5 冲突 | 改为 `N=1.3×(NG1K×H+NG2K)+1.5×ΣNQK`，出处改 GB 55023-2022（并注原 JGJ 130 的 1.2/1.4 已被更新） |
| tools/construction/calc-206.html | `λ=1.6×h×1000/15.8`：1.6 既不是 k(1.155) 也不是 μ(1.5/1.7)，属自造系数 | 改为 `l₀=k·μ·h`（JGJ 130-2011 §5.3.3），新增「连墙件布置（μ）」下拉（二步三跨 1.5 / 三步三跨 1.7）。默认态 λ 182→197、K 0.75→0.67（原本即「不满足」，结论未翻转）；深度解析 1/6 应力占比同步改 1/4、删除未参与计算的「挡风系数 φ≈0.6」说明 |
| tools/construction/calc-204.html | 支撑根数 `n=⌈L/s⌉` 且实际间距取 `L/n`：9 根只有 8 个间隔，均匀布置后实际间距 0.50 m > 容许 0.447 m（少一排/一列，偏不安全） | 改为 `n=⌈L/s⌉+1`、实际间距 `L/(n−1)`（两端各设一根）；竖向同理。单根荷载不变（14.3 kN），布置 9×7→10×8、总根数 63→80；引据注明 GB 55001-2021 可变荷载 1.5 |

- 一致（已核代码取值）：`calc-205`（脚手架钢管用量，几何估算式；`steps=⌊H/h⌋` 为半步取整的估算，页已注明不含扣件/脚手板，登记不改进）、`active-earth-rankine`（K_a=tan²(45°−φ/2)，含 c 修正项）、`excavation-earth`（E_a=½γH²K_a+qH K_a）、`slope-stability-fos`（无限边坡 F_s 公式正确，1.3 阈值明示为二级一般工况参考、一级/地震工况按 GB 50330-2013 表5.3.1 提高）、`pile-capacity`（R_a=(q_p A_p+u q_s L)/K，K=2 特征值口径，JGJ 94/GB 50007 一致）、`calc-power-voltage`（三相 I=P/(√3 U cosφ)、单相 I=P/(U cosφ)，断路器 ≥1.25I，WIRE_MAP 只大不小）。
- 缺页登记（不做新页）：① 吊装（T=G/(n cosθ)、吊耳/卸扣安全系数）在 `tools/construction`、`tools/civil` 无对口页面；② 基坑抗倾覆/抗隆起/抗渗流安全系数无专页，`excavation-earth`/`active-earth-rankine` 只算土压力合力；③ 模板支架立杆轴力/可调托座/剪刀撑无专页，`calc-204` 只算侧压力支撑间距；④ 临时用电漏电保护额定值（JGJ 46-2005 §8.2.10：末级 ≤30 mA、≤0.1 s，潮湿场所 ≤15 mA）未进入 `calc-power-voltage`，该页只做导线/断路器选型；⑤ 混凝土浇筑侧压力 `F=0.22γt₀β₁β₂√V` 与 `γH` 取小无专页，`calc-204` 以输入 q 代替。

工程量族核对 9 页（扣减/叠加方向）：

| 页面 | 核对点 | 结论 |
|---|---|---|
| tools/construction/construction-calculator.html | 门窗洞口扣除 | **修正**：GB 50854-2013 墙面抹灰/涂饰只扣单个 >0.3 m² 洞口，原代码对任意洞口一律扣除（0.25 m² 也扣）⇒ 改为 `area>0.3` 才计入扣除；页面自述规则与代码自此一致 |
| tools/construction/concrete-calculator.html | 混凝土损耗 | 正确：`volReal=vol×(1+loss)`，再按 m³ 指标计钢筋（t）与模板（m²），方向为「加」 |
| tools/civil/concrete-volume.html | 混凝土体积/重量 | 正确：`V=a·b·c`、`t=V×ρ/1000`，无反向扣减 |
| tools/civil/rebar-weight.html | 钢筋每米重量 | 正确：`0.00617·d²`（≈0.617 kg/m@d10，GB/T 1499.2 表值同口径） |
| tools/construction/brick-calculator.html | 砌体砖/砂浆 | 正确：砖=`vol/brickVol×(1−mortar)×(1+loss)`、砂浆=`vol×mortar×(1+loss)`，灰缝占比是「减砖、加浆」，损耗两处都「加」；水泥 250 kg/m³ 为经验值（M5–M10 区间），登记 |
| tools/mining/excavation-volume.html | 土方放坡/虚实方 | 方向正确（上口宽=底宽+2D·放坡系数、虚方=实方×松散系数）；**修正** `swell=+value||1.3` 吞 0：改为仅空串/NaN 回退，`swell<1` 明确报错（开挖后体积不可能变小） |
| tools/construction/calculator-calc-area.html | 公摊反推建筑面积 | 正确：`建面=套内/(1−公摊率)` |
| tools/construction/area-calculator.html | 公摊面积/得房率 | 正确：`公摊=套内×r/(100−r)`、`得房率=套内/建面` |
| tools/construction/calc-dosage-1.html | 瓷砖损耗 | 正确：`总用量=⌈净用量×(1+损耗%)⌉`，按含缝模块面积计净用量 |

- 砌体砂浆等级↔砌体强度设计值：`masonry-bearing` 的 f 由用户输入设计值，砂浆等级只参与 α（φ 公式）与 [β]（M2.5 22 / M5 24 / M7.5 26，GB 50003-2011 表6.1.1）；页面不做 f 与砂浆组合的合理性反查（如 M5 配 f=3.0 在烧结普通砖中不存在），登记为「输入职责」不构成计算错误。
- 本批 verify 更新：`calc-1`（inputs 去 a、加 mu=1.7；期望 λ=246.3、N_Rd=10.76 kN、利用率 192.4%）、`calc-206`（加 muVal=1.7；λ=186、K=1.11；general 套 175/0.71）、`calc-204`（9×7→10×8；general 36→50 根、改 10×5）、`construction-calculator` 新增「≤0.3 m² 洞口不扣除」边界用例（65.52 m² / 13.10 L，注入 6/4.2/2.6 保证 fidelity 不依赖 clicks）。
- 门禁：`verify_civil_calc` 50/50、`verify_construction_calc` 39/39、`verify_structural_calc` 47/47、`verify_general_calc` 362/362 全绿；fidelity 逃生 0（civil 50/50、construction 39/39）；all_default 0；`_test_static.py` 4705/4705；`_audit_assets.py --check` 0/0/0。

## 输入净化 × 列表分隔符（2026-11-05）

**判据**（`js/common.js::isListInput`）：输入框满足任一条件即为多值列表字段——① 带 `data-list` 属性；② 带 `multiple`；③ 初值 `value` 含 `,` `;` `、` `，` 之一。列表字段的数字净化只删「非数字、非小数点、非负号、非分隔符」字符，分隔符与空白原样保留；单值字段维持原口径（`12a3`→`123`）。

**共享层两支逻辑**：
- `enhanceNumberInputs()` 自动补 `inputmode="decimal"` 时跳过列表字段（避免把列表框变成无逗号的数字键盘）。
- 事件净化选择器为 `input[inputmode="decimal"], input[inputmode="numeric"], input[data-list]`；`listField` 分支保留 `, ; 、 ，` 与空白，非列表分支只留 `0-9 . -`。

**页面侧**：列表输入统一 `inputmode="text" data-list="1"`（`inputmode="decimal"` 在 iOS 数字键盘上打不出逗号）。本次修复 **22 页 / 26 个输入框**：`statistics` 13 页、`securities` 3 页、`metrology` 3 页、`investment` 1 页、`math` 1 页、`insurance` 1 页（明细见提交 `428576699d`）。

**扫描口径与三档计数**：全站含列表输入的页面 57 页 / 71 个输入框——① 真吞分隔符 22 页 / 26 框；② 单值误带 decimal 0 页；③ 安全 35 页 / 45 框（无 `inputmode`、placeholder 不含数字关键词，净化根本不挂载）。另有 3 个单值数字文本框（`cognition/digit-span-test`、`edu/number-memory`、`fun/1a2b-guess`）语义正确未动。

**已知取舍**：`inputmode="text"` 在手机端失去数字键盘（需切到符号页输入逗号）。长期更优解是「列表拆多个输入框」或「空格分隔 + 数字键盘（`inputmode="numeric"` 的键盘通常带空格）」，本次不做，避免批量改交互结构。后续再碰净化逻辑时，先确认没有把列表字段重新标成 `decimal`。

## 第 14 批：推导值写死复查 + 4 处跨规范复核（2026-11-05）

**扫描范围**：`tools/civil`（25 页）、`tools/construction`（38 页）、`tools/structural`（27 页），共 90 页。

**裸 `return <数字>` 命中 2 处**，均为安全守卫返回值（固定常数，非规范推导值）：

| 文件:行 | 现值 | 判定 |
|---|---|---|
| tools/civil/calc-2.html:251 | `return 0`（default 分支） | 固定常数：角度类型未命中时返回 0，不参与规范推导 |
| tools/civil/calc-2.html:257 | `if (angleDeg <= 0) return 0` | 固定常数：非正角度的零值守卫 |

**四分计数**：命中 2 处 / 改公式 0 处 / 固定常数 2 处 / 查表 0 处（φ 表另计，见下）。

**可疑常量人工分拣（16 项，全部固定常数，无需改公式）**：`calc-206` 的 `K_ADD=1.155` 为 JGJ 130-2011 §5.3.3 规定的计算长度附加系数 k（固定值）；`BAY=1.05`、`A_SEC=489`、`W_SEC=5078`、`I_SEC=15.8`、`F_STEEL=205` 为截面/材料常数；`calc-205` 的 `WT=3.84` 为钢管单位重量；`temp-7` 的 `nu=0.2` 为材料泊松比；`wasteFactor=1.05`、`margin=1.1`、`rec=5`、`curWall=2`、`curScale=100`、`calc-196` 的 `h=10 W/m²K` 为估算/默认假定；`cement-mortar-ratio` 的 `v=0.5` 为绘图循环步长。均非「应由 `f_y`/`f_c`/钢筋级别推导却写死」的形态。

**查表 2 页（保留，检索依据已注明）**：`tools/construction/calc-1.html` φ 表（JGJ 130-2011 附录 A 表 A.0.6，λ 线性插值）；`tools/construction/calc-206.html` `PHI_LAM/PHI_VAL`（同一表 A.0.6，A 类截面）。两表均按 λ 插值，末端越界取表末值，不构成写死推导值。

**受弯派生限值复核（未发现写死）**：`rc-beam-rebar`、`one-way-slab` 的 `ξ_b` 均按 `0.8/[1+f_y/(E_s·ε_cu)]` 实算（`E_s=2e5`、`ε_cu=0.0033`），`α_s,max=ξ_b(1−0.5ξ_b)` 同步实算，未出现 `0.44`/`0.518`/`0.384` 一类字面量；`masonry-bearing` 的 φ 已按 `1/(1+αβ²)` 实算（第 13 批修复）。`cft-capacity`、`dijichengzailijisuan`、`assessor-19` 未复活旧缺陷。

**4 处跨规范混用复核结论**（均维持现状，理由如下）：

| 页面 | 混用点 | 结论与理由 |
|---|---|---|
| tools/construction/calc-206.html | N 用 GB 55023-2022 的 1.3/1.5；Mw 用 JGJ 130-2011 §5.2.6 的 `0.9×1.4` | **必须混用**：GB 55023-2022 只更新荷载分项系数，未给出脚手架风弯矩公式；JGJ 130-2011 的 `0.9×1.4` 是配套风弯矩组合系数，两处各引其源、页内已分段注明，统一到单一规范会丢失 Mw 依据 |
| tools/civil/cft-capacity.html | 引 GB 50936-2014，实算 `A_s f_y + 1.2 A_c f_c` | **维持并注明**：GB 50936 的 `f_sc` 需套箍系数 θ 与其经验系数，页面定位为快速估算，已注明 1.2 为经验系数、正式设计按 GB 50936；未虚构标准系数 |
| tools/civil/dijichengzailijisuan.html | 引 GB 50007-2011 5.2.4，实算 Terzaghi `qu` | **维持并注明**：GB 50007 5.2.4 用 η_b/η_d 深宽修正，本页为 Terzaghi 极限承载力 + 经验安全系数折减，页内已明确「fa 不等同于 GB 50007 深宽修正后的 f_a」 |
| tools/construction/assessor-19.html | `βz=1+0.038√H` 非 GB 50009-2012 第 8.4 节计算值 | **维持并注明**：GB 50009 8.4 的 βz 需振型/阻尼等结构动力参数，本页无此输入，已把 βz 标为「经验估算」，不宣称按 8.4 计算 |

- 本批未改任何工具页与 verify（复查结论为「无新增写死、4 处维持并已注明」）。

## 第 15 批：材料与截面常数跨页一致性（2026-11-05）

**扫描范围**：`tools/civil`（25）、`tools/construction`（38）、`tools/structural`（27），共 90 页。按物理量归组建账 **18 组 / 出现 27 页**（含输入默认值、说明文字、代码常量与参考表；同一页多处出现只计一页）。

**四分计数**：① 真矛盾 **2** / ② 合法差异 **5** / ③ 单页孤立 **1** / ④ 未标口径 **1**。

**① 真矛盾（2 处，已统一）**：

| 物理量 | A 页值 | B 页值 | 统一值 | 依据 |
|---|---|---|---|---|
| 脚手架钢管规格（`calc-205`） | 正文/计算按 Φ48×3.5、3.84 kg/m | 参考表按 φ48.3×3.6、A=5.06 cm²、i=1.59 cm | **Φ48×3.5，A=4.89 cm²、i=1.58 cm、3.84 kg/m**（另注 JGJ 130-2011 推荐 φ48.3×3.6 / 5.06 cm² / 3.97 kg/m） | 同页自称 Φ48×3.5 且代码 `WT=3.84`；48.3×3.6 为另一管型，不得与 3.84 kg/m 混用。JGJ 130-2011 §3.1.2 推荐管为 φ48.3×3.6，故两口径并列标注 |
| 砌筑砂浆 M5 水泥:砂（`cement-mortar-ratio`） | 配比选项/代码/常用配合比 = **1:5.0** | 参考表 = **1:5.6**（引 JGJ/T 98-2010） | **计算取 1:5.0**；表内并列「规范经验参考约 1:5.6（32.5 级水泥、砂含水率 2%）」 | 同页同物理量不得给两个未加说明的比值；1:5.0 与代码 `ratio.m5=[1,5.0]` 一致，1:5.6 为规程经验参考，差异源于砂含水率/级配假定 |

**② 合法差异（5 组，保留并标口径）**：

| 物理量 | 差异 | 保留理由 |
|---|---|---|
| 混凝土容重 | 2400 kg/m³（`calc-strength-ratio`、`concrete-volume`、`concrete-calculator` FAQ）vs 2350–2450 区间（`concrete-calculator` 说明卡） | 区间本身包含 2400，属「额定值 vs 常见范围」表述，非矛盾；三页均标 kg/m³ |
| 混凝土强度 | f_c 设计值 14.3（C30）/11.9（C25）vs `cft-capacity` 示例 fck=26.8（C40 标准值） | 设计值 vs 标准值，页内分别标 `f_c` 与 `fck`，不得互换 |
| 钢材强度 | 脚手架族 f=205 N/mm²（GB 55023-2022/JGJ 130-2011 抗压设计值）vs `allowable-stress` σy=235 MPa（Q235 屈服强度 + 安全系数 n 的许用应力法） | 设计值法 vs 许用应力法，口径互斥且各自标注；两法均不应互改数值 |
| 脚手架钢管 | `calc-206` Φ48×3.5（A=489 mm²、W=5078 mm³、i=15.8 mm）vs `calc-1`/`calc-205` φ48.3×3.6（A≈506 mm²、i≈15.9 mm） | 不同管型；两页均按所用管型标注截面特性，`calc-206` 结果偏保守（A 小 3.4%） |
| 钢材弹性模量 | 4 个 `structural` 挠度/屈曲页默认 E=200 GPa vs GB 50017-2017 的 2.06×10⁵ MPa | E 为可输入参数（4 页默认值一致），200 GPa 为通用简化值；规范值可由用户改写，不构成同口径矛盾 |

**③ 单页孤立（1 处，核定未落地）**：

- `tools/civil/masonry-bearing.html` 算例：`MU10 砖 M5 砂浆 f≈1.5MPa、φ=0.9`。核对：GB 50003-2011 表 3.2.1-1 烧结普通砖 MU10+M5 抗压强度设计值 **f=1.30 MPa**；按本页 φ=1/(1+0.0015β²)、β=12.5 应为 **φ=0.810**（φ=0.9 亦与页内已修公式不符）。正确算例：`f=1.30MPa、φ=0.81、A=0.72m² → N≈758kN`。**本轮未改**：该算例数据源在 `i18n/tools/content_deepdive.json`（`civil/masonry-bearing` 的 `example.body`），改页会被下次 `_build.py` 覆盖，需与页面、英文词典一并同步，超出本批「只碰三目录 + verify」范围，登记待下批处理。

**④ 未标口径（1 处，本批已补）**：

- `tools/construction/brick-calculator.html` 水泥 250 kg/m³ 未分砂浆标号 → 已补「未分标号，取 M5–M10 综合估算；分级用量见『水泥砂浆配合比』工具」，与 `cement-mortar-ratio` 的 M5 220 / M7.5 280 / M10 330 / M15 380 分级口径分开表述。

**本批改动**：`calc-205` 参考表（管型统一）、`cement-mortar-ratio` 参考表（M5 比值双口径）、`brick-calculator` 公式说明（水泥用量口径）。均为说明文字，不改计算逻辑；`verify_construction_calc` 39/39 通过。未跑 `_build.py`。

## 第 16 批：正常使用极限状态族审计（2026-11-05）

**扫描范围**：`tools/civil` / `tools/construction` / `tools/structural` 中含「裂缝 / 挠度 / 保护层 / 耐久性 / 碳化 / 水胶比 / 抗渗 / 氯离子」的页面，共 **14 页**（已剔除 `index.html` 与仅命中「0.2mm 漆膜厚度」等无关串的页面）。

**四分计数**：一致 **4** / 不一致已修 **1** / 无法核 **8** / 未覆盖 **1**。

**逐页台账**：

| 页面 | 公式或参数 | 标准值 | 判定 |
|---|---|---|---|
| tools/civil/carbonation-depth.html | 碳化深度 `x = K·√t`（K 为 mm/√a 速率） | GB/T 50476 平方扩散模型 `x = k·√t`；参考表与深解算例（k=1.0、t=20 → 4.5mm）同口径 | **不一致已修**：原公式/代码乘 2.56（`x=2.56K√t`），与同页参考表、算例矛盾；已统一为 `x=K√t`，公式框/计算说明/`calcTool`/`extras`/图表 sweep/图表标题 6 处同步，英文词典 2 行与 verify 期望值同步 |
| tools/civil/concrete-wb-ratio.html | 耐久最大水胶比：一类 0.60 / 二a 0.55 / 二b 0.50 / 三a 0.45 / 三b 0.40 | GB 50010-2010 表 3.5.2 同值 | **一致**（已补出处「GB 50010-2010 表 3.5.2」；氯离子含量限值本页未列，归子项未覆盖） |
| tools/construction/detector-131.html | 抗渗等级 P6/P8/P10/P12 ↔ 0.6/0.8/1.0/1.2 MPa 逐级加压不渗透 | GB/T 50082-2009 同口径 | **一致** |
| tools/construction/calc-204.html | 模板挠度 `5qL⁴/384EI ≤ L/400`（外露）/ `L/250`（隐蔽） | GB 50666-2011 §4.4.4 同值 | **一致**（施工规范口径，非 GB 50010 构件挠度，页内已标 GB 50666） |
| tools/civil/load-combination.html | SLS 用标准组合（分项系数=1），承载力用基本组合（1.2/1.4） | GB 50068/GB 50009 组合口径 | **一致** |
| tools/civil/beam-udl.html | 仅弹性挠度 `δ=5qL⁴/384EI` | GB 50010 需 `B_s`（含 ψ、α_E、ρ、γ_f'）与长期刚度 `B`（θ=2.0）再验算限值 | **无法核**：无短期/长期刚度、无 ψ/θ、无限值，只给弹性值 |
| tools/structural/deflection-cantilever-point.html | `δ=FL³/(3EI)` | 纯弹性解，无 GB 50010 长期刚度与限值 | **无法核** |
| tools/structural/deflection-cantilever-udl.html | `δ=wL⁴/(8EI)` | 同上 | **无法核** |
| tools/structural/ss-point-deflection.html | `δ=PL³/(48EI)` | 同上 | **无法核** |
| tools/civil/rc-beam-rebar.html | 正文仅提及「使用阶段验算裂缝与挠度」，无 `w_max` 公式 | GB 50010-2010 式 7.1.2 需 α_cr、ψ、σ_s、c、d_eq、ρ_te | **无法核**（另登记：输入标签「保护层 a_s」实为受拉钢筋合力点至截面边缘距离 a_s，非保护层厚度 c） |
| tools/civil/one-way-slab.html | 仅 ρmin、构造间距说明 | 无裂缝宽度/挠度计算 | **无法核** |
| tools/civil/two-way-slab.html | 弹性薄板弯矩系数（ν=0.2） | 无挠度/裂缝验算 | **无法核** |
| tools/civil/rebar-anchorage.html | 锚固长度修正提及保护层 | 无最小保护层厚度/耐久限值 | **无法核** |
| tools/civil/temp-7.html | 大体积温控：内表/基础温差 25°C、R 按厚度 0.4/0.5/0.6/0.7、K≥1.15 | GB 50496 大体积混凝土温控体系 | **未覆盖**：属温度裂缝预防，不并入 GB 50010 SLS 裂缝宽度四分 |

**子项覆盖结论（GB 50010-2010 正常使用极限状态）**：

- **裂缝宽度式 7.1.2**：全站 0 页实现（α_cr 受弯 1.9 / 偏心受压 1.66、ψ 0.2–1.0、d_eq、ρ_te≥0.01、c 按环境类别）——`rc-beam-rebar` 仅文字提及。
- **挠度 B_s / B（θ=2.0）**：0 页实现，4 个挠度页均为纯弹性解。
- **最小保护层厚度 / 最大水胶比 / 氯离子限值**：仅 `concrete-wb-ratio` 覆盖最大水胶比并已对齐表 3.5.2；保护层与氯离子限值 0 页。
- **裂缝控制等级（表 3.3.1，0.2/0.1/0.3mm）**：0 页覆盖。

**本批改动**：`tools/civil/carbonation-depth.html`（去 2.56 因子，6 处）、`i18n/tools/en/civil/carbonation-depth.json`（2 键）、`tools/civil/concrete-wb-ratio.html`（补表 3.5.2 出处）、`i18n/tools/en/civil/concrete-wb-ratio.json`（同键）、`scripts/verify_civil_calc.js`（carbonation 正例 42.9→16.8、B 类自动补强例 69.68→272.2）。`node scripts/verify_civil_calc.js` = 51/51；`node scripts/discriminate_check.js verify_civil_calc.js` = 51/51 变红、0 逃生项。未跑 `_build.py`。

**构建保留判断**：`_build.py` 只重建 `<!-- TOOLBOX-DEEP-DIVE -->` 区块（由 `i18n/tools/content_deepdive.json` 的 `civil/carbonation-depth` 条目生成），而该条目本身已是 `x=k·√t`（与本页算例一致），故重建后深度解析块与本页现值一致；公式框、`calcTool`、`extras`、`__cadSweep`、图表标题均位于深度块之外，构建不会改写。verify 脚本与英文词典不参与页面正文生成。因此下次构建「深度块重写为同值、其余保留」。复查口径：构建后 `grep -c '2.56'` 应为 0、`grep -c 'K*Math.sqrt'` 计数不变。

