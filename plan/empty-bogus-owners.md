# empty_bogus 230 页「目录 → 归属线」底表

- 生成时间：2026-11-05
- 范围：`plan/empty-bogus-dispatch.md` 的 63 个行业组 / 230 页，仅推导归属，**未修改任何工具页**。
- 证据口径：① `scripts/verify_*_calc.js` 中 `slug: "<目录>/…"` 的用例数（同目录专用 verify 即最强覆盖证据）；② 该目录最近一次**实质修复**提交（已排除 `chore`/build、docs、安全 meta、privacy、纯 `preset`/`S7` 引据卡/门禁批次与本会话的 7 页空态提交；保留 `S8 空态教育化` 等与空态直接相关的批次）；③ 目录语义与会话内已知批次。
- 置信度：**高** = 专用 verify 覆盖 + 语义与最近批次一致；**中** = 语义清楚但最近批次无关或跨线轻微歧义；**低** = 两条线证据冲突，需人工裁定（见第 2 节）。

## 1. 逐组归属表（63 组）

| 目录 | 页数 | 覆盖 verify（用例数） | 最近实质提交 | 建议归属线 | 置信度 |
|---|---|---|---|---|---|
| `tools/aerospace/` | 5 | verify_aerospace_calc.js(36) | `feff8d37c5` 2026-11-04 fix(engineering): 统一 Δv/比冲页 g₀ 口径并回填算例尾数 | 工程制造线 | 中 |
| `tools/astronomy/` | 2 | verify_astronomy_calc.js(25) | `370325dc40` 2026-11-05 fix: 修复内联事件引用未定义全局函数（6 页） | 物理与科学线 | 高 |
| `tools/baking/` | 1 | verify_baking_calc.js(14) | `06272d0aed` 2026-11-04 fix(longtail-b): 围棋数子法补活子输入、Elo复制/得分率口径修正、… | 农业与食品线 | 高 |
| `tools/banking/` | 5 | verify_banking_calc.js(29) | `f30132019f` 2026-11-03 fix: 修复检验/金融/生活/图片/商业五分类 28 页中高优缺陷 | 金融商业与 HR 线 | 高 |
| `tools/chemistry/` | 4 | verify_chemistry_calc.js(27)、verify_general_calc.js(10) | `cd054a32ec` 2026-10-28 feat(S7): 批130 chemistry 7页+materials 5页新增… | 物理与科学线 | 高 |
| `tools/chinese-cook/` | 1 | verify_chinese-cook_calc.js(6) | `26ce6ca7f7` 2026-10-26 feat(ux): S8 空态教育化九批(收尾)——剩余 154 分类 2102 页… | 农业与食品线 | 高 |
| `tools/dynamics/` | 12 | verify_dynamics_calc.js(23) | `44b934df3e` 2026-10-27 feat(dynamics): 10页经典力学页加S7引据卡(牛顿碰撞定律1686/… | 物理与科学线 | 高 |
| `tools/eco/` | 18 | verify_eco_calc.js(37)、verify_general_calc.js(1) | `56d149b176` 2026-11-02 feat(eco): 第18-25页补齐业务场景预设（G06-S2，25页收口） | 金融商业与 HR 线 | 高 |
| `tools/economics/` | 7 | verify_economics_calc.js(27) | `b160e0b65f` 2026-10-27 feat(economics): 剩余13页加S7引据卡(Keynes消费函数与乘数… | 金融商业与 HR 线 | 高 |
| `tools/electromagnetism/` | 4 | verify_electromagnetism_calc.js(25) | `b783f1ef88` 2026-10-28 feat(S7): 批123 electromagnetism 收口1页(串联R_e… | 物理与科学线 | 高 |
| `tools/encode/` | 3 | verify_encode_calc.js(30)、verify_edu_calc.js(1) | `dad04850d5` 2026-11-02 feat(encode): 第21-29页补齐业务场景预设（G06-S2，文件上传页… | IT 文本编码线 | 高 |
| `tools/energy/` | 3 | verify_energy_calc.js(42)、verify_general_calc.js(2) | `44aca16a60` 2026-11-04 fix(tools): 第9批修正 8 页示例与单位换算自相矛盾 + 英文词典 | 工程制造线 | 高 |
| `tools/ent/` | 1 | verify_ent_calc.js(23) | `619f331781` 2026-10-26 feat(ux): S8 空态教育化五批——医疗域剩余 25 分类 308 页 10… | 临床医疗线 | 高 |
| `tools/film/` | 1 | verify_film_calc.js(6) | `26ce6ca7f7` 2026-10-26 feat(ux): S8 空态教育化九批(收尾)——剩余 154 分类 2102 页… | 生活消费线 | 高 |
| `tools/fire/` | 1 | verify_fire_calc.js(11) | `26ce6ca7f7` 2026-10-26 feat(ux): S8 空态教育化九批(收尾)——剩余 154 分类 2102 页… | 工程制造线 | 中 |
| `tools/fishery/` | 1 | verify_fishery_calc.js(38) | `3c3ee30c27` 2026-11-04 fix: 修复条码/QR 伪实现与 8 个假承诺工具 | 农业与食品线 | 高 |
| `tools/fluid/` | 3 | verify_fluid_calc.js(23) | `b9c7efccb6` 2026-10-27 feat(fluid): 剩余6页加S7引据卡(Darcy-Weisbach 184… | 物理与科学线 | 高 |
| `tools/food/` | 1 | verify_food_calc.js(24) | `5b04148eba` 2026-11-05 fix(calc): 0 值不再被 ｜｜ 默认值吞掉；哈希算法名修复；统计页输入即时… | 农业与食品线 | 高 |
| `tools/food-processing/` | 2 | verify_food-processing_calc.js(21) | `0708ff912b` 2026-11-04 fix(longtail-a): 冷冻 0 天改提示不建议冷冻，杀菌导语去模板化，浓… | 农业与食品线 | 中 |
| `tools/general/` | 1 | verify_general_calc.js(54) | `9d517cff76` 2026-11-05 fix(general): 日期差与年龄计算默认日期改本地日历格式化 | 数学统计测量线 | 中 |
| `tools/geometry/` | 11 | verify_geometry_calc.js(28) | `68edbda6cc` 2026-10-28 feat(S7): 批115 geometry 11页新增公式与标准引据卡（圆周长祖… | 数学统计测量线 | 高 |
| `tools/healthcare/` | 5 | verify_healthcare_calc.js(36) | `6c99f6229d` 2026-11-05 fix(dose,lab): 修正剂量封顶、负荷量公式与检验切点口径 | 临床医疗线 | 高 |
| `tools/hematology/` | 1 | verify_hematology_calc.js(27) | `6c99f6229d` 2026-11-05 fix(dose,lab): 修正剂量封顶、负荷量公式与检验切点口径 | 临床医疗线 | 高 |
| `tools/home/` | 2 | verify_home_calc.js(7) | `11d27b1bc9` 2026-11-05 fix(export): 修正 downloadText 参数顺序颠倒导致的死导出（… | 生活消费线 | 高 |
| `tools/insurance/` | 4 | verify_insurance_calc.js(31) | `26ce6ca7f7` 2026-10-26 feat(ux): S8 空态教育化九批(收尾)——剩余 154 分类 2102 页… | 金融商业与 HR 线 | 高 |
| `tools/investment/` | 5 | verify_investment_calc.js(25)、verify_general_calc.js(1) | `c8f62de789` 2026-10-31 S1(automotive/finance/investment): driver-… | 金融商业与 HR 线 | 高 |
| `tools/kinematics/` | 8 | verify_kinematics_calc.js(25) | `e76ebd3cef` 2026-10-27 feat(S7): 批92 kinematics 13页新增公式与标准引据卡（角速度… | 物理与科学线 | 高 |
| `tools/language/` | 2 | verify_language_calc.js(22)、verify_edu2_calc.js(6) | `af986271e5` 2026-11-04 feat(fake-tools): Batch 5-1 重写分析与游戏类 6 页 | IT 文本编码线 | 高 |
| `tools/life/` | 1 | verify_life_calc.js(70)、verify_science_calc.js(1)、verify_niche_calc.js(1) | `464cf05f3d` 2026-11-05 fix(tools): 全站随机数源审计——16 个密码学用途页改用 crypto.… | 生活消费线 | 高 |
| `tools/livestock/` | 1 | verify_livestock_calc.js(44) | `413296dcf9` 2026-11-05 fix(agriculture,livestock): PHI=0 依据定稿与 15… | 农业与食品线 | 高 |
| `tools/logistics/` | 2 | verify_logistics_calc.js(16) | `f30132019f` 2026-11-03 fix: 修复检验/金融/生活/图片/商业五分类 28 页中高优缺陷 | 生活消费线 | 中 |
| `tools/materials/` | 4 | verify_materials_calc.js(31)、verify_general_calc.js(10) | `c4332f14d3` 2026-11-05 fix(materials): 维氏硬度 kgf/mm²→MPa 联动量系数方向修正 | 工程制造线 | 高 |
| `tools/mechanical/` | 3 | verify_mechanical_calc.js(14) | `26ce6ca7f7` 2026-10-26 feat(ux): S8 空态教育化九批(收尾)——剩余 154 分类 2102 页… | 工程制造线 | 高 |
| `tools/metalwork/` | 1 | verify_metalwork_calc.js(39) | `3c3ee30c27` 2026-11-04 fix: 修复条码/QR 伪实现与 8 个假承诺工具 | 工程制造线 | 高 |
| `tools/meteorology/` | 4 | verify_meteorology_calc.js(42) | `85f29f06fb` 2026-11-04 fix(science): 产状直立面/水平面判据修正、气象预设改合法示例并补 RH… | 物理与科学线 | 高 |
| `tools/metrology/` | 6 | verify_metrology_calc.js(28)、verify_general_calc.js(1) | `e63c1f2316` 2026-10-28 feat(S7): 批122 metrology 11页新增公式与标准引据卡（校准周… | 数学统计测量线 | 高 |
| `tools/nuclear/` | 8 | verify_nuclear_calc.js(28) | `270fb7eca2` 2026-10-27 feat(S7): 批110-a nuclear 4页新增公式与标准引据卡（衰变常数… | 物理与科学线 | 高 |
| `tools/nutrition/` | 2 | verify_nutrition_calc.js(18) | `e3e7488607` 2026-11-04 fix(fake-tools): Batch 6-1 重写生成与字符类 5 页 | 农业与食品线 | 中 |
| `tools/obstetrics/` | 1 | verify_obstetrics_calc.js(23) | `6c99f6229d` 2026-11-05 fix(dose,lab): 修正剂量封顶、负荷量公式与检验切点口径 | 临床医疗线 | 高 |
| `tools/optical/` | 1 | verify_optical_calc.js(40) | `5b04148eba` 2026-11-05 fix(calc): 0 值不再被 ｜｜ 默认值吞掉；哈希算法名修复；统计页输入即时… | 物理与科学线 | 高 |
| `tools/pr/` | 1 | verify_pr_calc.js(12) | `26ce6ca7f7` 2026-10-26 feat(ux): S8 空态教育化九批(收尾)——剩余 154 分类 2102 页… | 金融商业与 HR 线 | 高 |
| `tools/process/` | 2 | verify_process_calc.js(14) | `fd38ba70a1` 2026-11-04 fix: 清理 35 条高优缺陷（长尾行业 / IT / 生活金融 / 教育医疗） | 工程制造线 | 高 |
| `tools/property/` | 2 | verify_property_calc.js(18) | `80b12866b4` 2026-11-05 fix(export): CSV 导出统一防公式注入、UTF-8 BOM、引号转义与… | 土建测绘/房产线 | 低 |
| `tools/pulmonology/` | 1 | verify_pulmonology_calc.js(34) | `11e7a85a58` 2026-11-05 fix(medical): correct dosage weight bands … | 临床医疗线 | 高 |
| `tools/quantum/` | 2 | verify_quantum_calc.js(27) | `42c85ab071` 2026-11-04 fix(finance): 修 tfn-validator 门禁桩空值崩溃 | 物理与科学线 | 高 |
| `tools/realestate/` | 2 | verify_realestate_calc.js(54) | `4b98698fc6` 2026-10-28 feat(realestate): 批232 插入公式与标准引据卡片 6 页（收益法… | 土建测绘/房产线 | 低 |
| `tools/reproductive-medicine/` | 1 | verify_reproductive-medicine_calc.js(24) | `4028df8dd6` 2026-11-02 feat(reproductive-medicine): 第17-24页补齐业务场景… | 临床医疗线 | 高 |
| `tools/restaurant/` | 1 | verify_restaurant_calc.js(9) | `d1c1647f9e` 2026-10-27 feat(restaurant): 菜单毛利率页新增目标毛利率定价反推 | 农业与食品线 | 高 |
| `tools/robotics/` | 11 | verify_robotics_calc.js(28) | `42c85ab071` 2026-11-04 fix(finance): 修 tfn-validator 门禁桩空值崩溃 | 工程制造线 | 低 |
| `tools/science/` | 4 | verify_science_calc.js(87)、verify_misc_calc.js(1) | `5b04148eba` 2026-11-05 fix(calc): 0 值不再被 ｜｜ 默认值吞掉；哈希算法名修复；统计页输入即时… | 物理与科学线 | 高 |
| `tools/securities/` | 5 | verify_securities_calc.js(34) | `a901906a2a` 2026-10-27 feat(securities): 6 页公式页加 S7 引据卡（Hull 等权威出… | 金融商业与 HR 线 | 高 |
| `tools/service/` | 1 | verify_service_calc.js(5) | `26ce6ca7f7` 2026-10-26 feat(ux): S8 空态教育化九批(收尾)——剩余 154 分类 2102 页… | 生活消费线 | 中 |
| `tools/shipping/` | 1 | verify_shipping_calc.js(6) | `fd38ba70a1` 2026-11-04 fix: 清理 35 条高优缺陷（长尾行业 / IT / 生活金融 / 教育医疗） | 生活消费线 | 中 |
| `tools/signal/` | 3 | verify_signal_calc.js(26) | `0f01803ead` 2026-10-27 feat(S7): 批90 signal 12页新增公式与标准引据卡（载波/占空比/… | 工程制造线 | 中 |
| `tools/sports/` | 2 | verify_sports_calc.js(73) | `874fb8e3d4` 2026-11-05 fix(interaction): 修复 16 页交互异常与导出死链 | 生活消费线 | 中 |
| `tools/startup/` | 1 | verify_startup_calc.js(14) | `f30132019f` 2026-11-03 fix: 修复检验/金融/生活/图片/商业五分类 28 页中高优缺陷 | 金融商业与 HR 线 | 高 |
| `tools/statistics/` | 5 | verify_statistics_calc.js(50) | `86e63e7051` 2026-11-04 fix(science): F 检验拦截文案对齐门禁（避免 HTML 实体导致漏匹配… | 数学统计测量线 | 高 |
| `tools/surveying/` | 13 | verify_surveying_calc.js(51) | `d464503104` 2026-11-04 fix: 第6批 8 页工具口径与空值分支修正（图表/单位选择器/条款/导出） | 土建测绘/房产线 | 低 |
| `tools/tax/` | 16 | verify_tax_calc.js(31)、verify_science_calc.js(1) | `9274411741` 2026-10-26 feat(tax): calc-8 加速算扣除数逐档推导静态卡(Q(k)=Q(k-1… | 金融商业与 HR 线 | 高 |
| `tools/text/` | 1 | verify_text_calc.js(14)、verify_science_calc.js(1) | `afe1c858fd` 2026-11-04 fix(tools): 第 2 批中优修复 40 页并同步英文词典与深解 | IT 文本编码线 | 高 |
| `tools/thermodynamics/` | 5 | verify_thermodynamics_calc.js(28)、verify_general_calc.js(1) | `ee32278689` 2026-10-28 feat(S7): 批113-a thermodynamics 7页新增公式与标准引… | 物理与科学线 | 高 |
| `tools/usedcar/` | 1 | verify_usedcar_calc.js(11) | `5c09972f6d` 2026-11-04 fix: L/M 批 30 项高优缺陷修复 + 英文词典补齐 | 生活消费线 | 中 |
| `tools/wedding/` | 1 | verify_wedding_calc.js(7) | `26ce6ca7f7` 2026-10-26 feat(ux): S8 空态教育化九批(收尾)——剩余 154 分类 2102 页… | 生活消费线 | 高 |
| **合计** | **230** | — | — | — | — |

## 2. 低置信度（需人工裁定，4 组 / 28 页）

| 目录 | 页数 | 建议归属 | 冲突点 |
|---|---|---|---|
| `tools/surveying/` | 13 | 土建测绘/房产线 | 语义属土建/测绘（verify 51 例），但最近实质改动为 `d464503104`「第6批 空值分支修正」，且有记录称本目录由死代码第三批动过 → 土建测绘线 vs 死代码线冲突。 |
| `tools/realestate/` | 2 | 土建测绘/房产线 | 语义属房产/商业，近期为 `feat(preset) G06-S2` 内容批次，另有记录称死代码第三批动过 → 房产商业线 vs 死代码线冲突。 |
| `tools/property/` | 2 | 土建测绘/房产线 | 语义同 `realestate`，近期为 `fix(export)` 导出批次 → 房产商业线 vs 死代码线冲突。 |
| `tools/robotics/` | 11 | 工程制造线 | 11 页，语义可归工程制造或物理科学；最近实质提交 `42c85ab071 fix(finance): 修 tfn-validator` 与本目录无关，无有效归属证据。 |

> 裁定建议：`surveying`（13 页）若按语义归土建测绘线、按最近改动归死代码线，两包都不应重复领取；`realestate`/`property`（4 页）建议与房产商业线合并、不再单列；`robotics`（11 页）建议随工程制造线，因其 verify 用例已覆盖且与物理科学线的公式类工具无重叠。

## 3. 按归属线聚合的工作包（9 包，与 dispatch 分组完全对齐）

| 工作包 | 页数 | 目录清单（页数） |
|---|---|---|
| **金融商业与 HR 线** | **62** | `banking`(5)、`eco`(18)、`economics`(7)、`insurance`(4)、`investment`(5)、`pr`(1)、`securities`(5)、`startup`(1)、`tax`(16) |
| **物理与科学线** | **57** | `astronomy`(2)、`chemistry`(4)、`dynamics`(12)、`electromagnetism`(4)、`fluid`(3)、`kinematics`(8)、`meteorology`(4)、`nuclear`(8)、`optical`(1)、`quantum`(2)、`science`(4)、`thermodynamics`(5) |
| **工程制造线** | **33** | `aerospace`(5)、`energy`(3)、`fire`(1)、`materials`(4)、`mechanical`(3)、`metalwork`(1)、`process`(2)、`robotics`(11)、`signal`(3) |
| **数学统计测量线** | **23** | `general`(1)、`geometry`(11)、`metrology`(6)、`statistics`(5) |
| **土建测绘/房产线** | **17** | `property`(2)、`realestate`(2)、`surveying`(13) |
| **生活消费线** | **12** | `film`(1)、`home`(2)、`life`(1)、`logistics`(2)、`service`(1)、`shipping`(1)、`sports`(2)、`usedcar`(1)、`wedding`(1) |
| **临床医疗线** | **10** | `ent`(1)、`healthcare`(5)、`hematology`(1)、`obstetrics`(1)、`pulmonology`(1)、`reproductive-medicine`(1) |
| **农业与食品线** | **10** | `baking`(1)、`chinese-cook`(1)、`fishery`(1)、`food`(1)、`food-processing`(2)、`livestock`(1)、`nutrition`(2)、`restaurant`(1) |
| **IT 文本编码线** | **6** | `encode`(3)、`language`(2)、`text`(1) |
| **合计** | **230** | 63 个目录 |

> 派工口径：一个工作包内的目录整组派给同一线；包内页序保持 `empty-bogus-dispatch.md` 的目录字母序与页序，不重排。低置信度 4 组（28 页）先由维护者裁定后再并入对应包，避免与土建/死代码线撞文件。
