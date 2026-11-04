# 全站规范引用台账（standards-map）

> 用途：逐个工具页核对「页面声称的标准/条款」与「代码实际取值」是否一致，并记录标准现行状态。
> 维护：随批次增量追加；已被 GB 550xx-2022 通用规范替代的条文必须在页面注明「现行以 GB 550xx-2022 为准」。
> 状态口径：`现行` / `已修订` / `部分被 GB 550xx-2022 替代` / `已被 GB 550xx-2022 替代`。
> 第 5 列口径：`是` = 已逐行对照页面 `calc()` 取值（有具体修正或明确核对记录）；`否` = 仅抄录页面所述数值，尚未核对代码取值，后续复扫优先补。

| 页面路径 | 页面声称的标准与条款 | 代码实际采用的取值 | 出处与现行状态 | 是否已核对代码取值 | 实际取值 vs 标准要求 |
|---|---|---|---|---|---|
| tools/fire-rescue/fire-extinguisher-selection.html | GB 50140-2005 表 6.2.1（A 类）；B/C/E 类此前误用同一张 A 类表 | A 类按 100/75/50 m²/A；B/C/E 类改按表 6.2.2 取 1.5/1.0/0.5 m²/B，单具最小 21B/55B/89B；D/F 类不再套算，提示按专项规范 | GB 50140-2005 现行；强制性要求以 GB 55036-2022 为准（已加页内说明）。第 8 批修正 | 是 | 已修正：按修正后取值复核，与所引标准一致。 |
| tools/fire-rescue/calc-4.html | GB 50140-2005 表 6.2.1（原页面对 B/C 类也写 6.2.1） | B/C 类 `coverage` 表取 1.5/1.0/0.5 m²/B，与表 6.2.2 一致；引用改为按火灾类别切换表号 | GB 50140-2005 现行；GB 55036-2022 已加说明。第 8 批修正表号 | 是 | 已修正：按修正后取值复核，与所引标准一致。 |
| tools/fire-rescue/sprinkler-design.html | GB 50084-2017 表 5.0.1；仓库Ⅰ级 6 L/(min·m²)、200 m² | 民用/厂房按表 5.0.1；仓库Ⅰ级按第 5.0.4 条 / 表 5.0.4；设计流量 `Q=K√(10P)`；消防水池按 1 小时 × 3.6 换算 m³（原误按 L/s×60 显示 L，差 60 倍） | GB 50084-2017 现行；与 GB 55036-2022 不一致处已被替代。第 8 批修正表号与水池单位 | 是 | 已修正：按修正后取值复核，与所引标准一致。 |
| tools/fire-rescue/smoke-management.html | GB 51251-2017；NFPA 92 轴对称烟羽；排烟量安全系数 1.2 | 质量流量 `0.071 Qc^(1/3) z^(5/3)(1+0.027 Qc^(2/3)/z)`；体积流量改含 ×1.2；ρ₀/T₀ 统一为 1.2 kg/m³、293 K（原公式行写 1.293/273 与正文冲突） | GB 51251-2017 现行；与 GB 55036-2022 不一致处已被替代。第 8 批修正系数与状态量 | 是 | 已修正：按修正后取值复核，与所引标准一致。 |
| tools/fire-rescue/fire-resistance-rating.html | GB 50016-2014（2018 版）表 5.1.2 / 表 3.2.1 | 民用等级按第 5.1.3 条；厂房按第 3.2.2、3.2.3 条；仓库按第 3.2.5 条（原统一误标 3.2.1） | GB 50016-2014（2018 局部修订）现行；强制性条文已被 GB 55037-2022 替代。第 8 批修正条号并加说明 | 是 | 已修正：按修正后取值复核，与所引标准一致。 |
| tools/fire-rescue/length-distance.html | GB 50974-2014 消防水带沿程损失 | Hazen-Williams（C=140）换算 MPa；「默认参数」预设 DN50 与页面默认 DN65 不一致，已统一为 DN65 | GB 50974-2014 现行；部分被 GB 55036-2022 替代。第 8 批修正预设 | 是 | 已修正：按修正后取值复核，与所引标准一致。 |
| tools/fire-rescue/hydrant-flow.html | GB 50974-2014 §7.4.7；栓口动压 0.35/0.25 MPa、充实水柱 13/10 m | `q=√(P/(1/B+A·L))`、`Sk=Hq/(1+φHq)`；新增 P>0.50 MPa 减压提示（>0.70 MPa 必须减压） | GB 50974-2014 现行；与 GB 55036-2022 不一致处已被替代。第 8 批补超压校核 | 是 | 一致（已复核） |
| tools/fire-rescue/fire-alarm-zone.html | GB 50116-2013 探测区域划分 | 探测区域上限 500 m²（原 5000 m² 多一位）；单层大空间楼层数按 1 计 | GB 50116-2013 现行。第 7 批修正 | 是 | 已修正：按修正后取值复核，与所引标准一致。 |
| tools/fire-rescue/ventilation-tactics.html | GB 51251-2017 §3.4.6 正压送风余压 | 25–30 Pa（原 40–50 Pa） | GB 51251-2017 现行；与 GB 55036-2022 不一致处已被替代。第 7 批修正 | 是 | 已修正：按修正后取值复核，与所引标准一致。 |
| tools/fire-rescue/fire-load.html | GB 50016-2014 火灾荷载密度分级 | 分级表与进度条上限统一为 2000 MJ/m²；总热值 ÷ 面积 | GB 50016-2014 现行。第 7 批修正 | 是 | 已修正：按修正后取值复核，与所引标准一致。 |
| tools/fire-rescue/time-air.html | GB/T 16556-2007 自给开路式压缩空气呼吸器 | 6.8 L/30 MPa 气瓶可用空气量按 2013 L；撤离余量 18%（原 2040 L、25%） | GB/T 16556-2007 现行。第 7 批修正 | 是 | 已修正：按修正后取值复核，与所引标准一致。 |
| tools/fire-rescue/detector-20.html | GB 50166-2019 / GB 50261-2017 / GB 50974-2014 施工验收 | 评分项按各系统验收条款分档，满分 100% | 三项均现行；GB 50974 与 GB 55036-2022 不一致处已被替代。第 7 批复核 | 是 | 一致（已复核） |
| tools/fire-rescue/time-evacuation.html | GB 50016 / GB 51251-2017 疏散与排烟 | ASET−RSET 安全裕度；RSET 三项全 0 时改为报错 | GB 50016 现行；GB 51251-2017 部分被 GB 55036-2022 替代。第 7 批补校验 | 是 | 一致（已复核） |
| tools/fire-rescue/sprinkler-design.html（水锤/流量校核行） | GB 5135.1-2019 / ISO 6182 喷头流量系数 K | K 值按 80/115/160 等档，`q=K√(10P)`（P 为 MPa，10P 即 bar） | GB 5135.1-2019 现行；与 GB 55036-2022 不一致处已被替代。第 10 批复核 | 是 | 一致：K 档 80/115/160 与 q=K√(10P) 口径与 GB 5135.1-2019 相同，无偏差。 |
| tools/construction/concrete-calculator.html | JGJ 55-2011 配合比；GB 50666-2011 施工；GB 50010-2010 结构 | 配合比表按强度等级经验值；模板系数按 `m²/m³` 口径（楼板 8.5、梁 9、柱 10、墙 12、基础 2、楼梯 5） | JGJ 55-2011 / GB 50666-2011 / GB 50010-2010 现行。第 8 批修正参考表自相矛盾（楼板原写 2–3、楼梯原写 8–10） | 是 | 已修正：按修正后取值复核，与所引标准一致。 |
| tools/construction/cement-mortar-ratio.html | JGJ/T 98-2010 砌筑砂浆配合比 | 水泥经验基准 M5 220、M7.5 280、M10 330、M15 380 kg/m³；砂=水泥×砂比；M10 统一 1:4.5、M7.5 1:4.8 | JGJ/T 98-2010 现行。第 8 批修正图表水泥基准（原图 M5 用 340 与结果 220 不一致）及示例砂量 | 是 | 已修正：按修正后取值复核，与所引标准一致。 |
| tools/construction/calculator-calc-ratio-2.html | JGJ 55-2011 水灰比/砂率 | C20 水泥 330、水 185、砂 700、石 1185（水灰比 0.56、砂率 37.1%）；C25 水泥 373、砂 660、石 1177、水 190（水灰比 0.51、砂率 35.9%）；示例已与 MIX 表统一 | JGJ 55-2011 现行。第 8 批复核，第 9 批修正 C25 示例（原 350/680/1180 与表不符） | 是 | 已修正：按修正后取值复核，与所引标准一致。 |
| tools/construction/calc-1.html | JGJ 130-2011 扣件式钢管脚手架 | 立杆稳定 `N_Rd=φ·A·f/1000`（f=205 N/mm² 设计值，不再除 1.1）；`N_Sd=(1.3×自重 g+1.5×施工 q)×A`；λ=l₀/i（l₀ 由 m 转 mm） | JGJ 130-2011 现行；分项系数已按 GB 55023-2022 更新为 1.3/1.5。第 10 批修正 | 是 | 已修正：原 f=fy/1.1（重复折减材料分项系数）与 1.2/1.4 组合改为 f=205 设计值 + 1.3/1.5，与 GB 55023-2022 一致。 |
| tools/construction/calc-204.html | JGJ 162-2008 模板支架；GB 50009-2012 荷载；GB 50666-2011 | `q_d=1.5q`；`s=√(Pa/q_d)`，支撑数 ⌈L/s⌉×⌈H/s⌉，实际荷载 q_d·sL·sH，总侧压力 q_d·L·H | JGJ 162-2008 / GB 55001-2021 / GB 50666-2011 现行。第 10 批修正 | 是 | 已修正：原 s=√(Pa/q) 漏可变荷载分项系数，现 q_d=q×1.5，与 GB 55001-2021 一致。 |
| tools/construction/calc-205.html | JGJ 130-2011 脚手架钢管用量 | 立杆 ⌈L/纵距⌉+1×2 排；横杆 步数×排数×排距；剪刀撑按 6 m 分段 | JGJ 130-2011 现行。第 10 批复核 | 是 | 一致（估算式）：材料用量按几何布置估算，JGJ 130-2011 未规定该估算式，数值口径自洽。 |
| tools/construction/ac-size-guide.html | GB 21455-2019 能效；GB/T 7725-2022 空调器；GB 50736-2012 供暖通风 | 冷负荷按面积×指标×修正，1 匹=2500 W（原 2324 W） | 三项现行；GB 50736 与 GB 55015-2021 不一致处以其为准。第 7 批修正 | 是 | 已修正：按修正后取值复核，与所引标准一致。 |
| tools/construction/window-shading.html | GB 50189-2015 节能设计；GB 55015-2021 | 外遮阳系数按几何投影近似，并注明不能直接套用 GB 50189 的 SC 限值 | GB 50189-2015 现行；节能强制性指标已被 GB 55015-2021 替代。第 10 批复核 | 是 | 一致（近似）：SC_ext 为几何投影近似，页面已注明不能直接套用 SC 限值，不构成规范冲突。 |
| tools/construction/blueprint-tool.html | GB/T 50001-2017 房屋建筑制图；GB/T 14689-2008 图纸幅面 | 图纸比例换算；CAD 单位下拉（mm/cm/m）参与换算（原为死控件） | 两项现行。第 6 批修正 | 是 | 已修正：按修正后取值复核，与所引标准一致。 |
| tools/welding/detector-25.html | NB/T 47013 承压设备无损检测；GB/T 3323 射线检测；ISO 17635 | 角焊缝按 RT/UT 适用性给提示，不套用对接焊缝缺陷等级 | NB/T 47013 现行；GB/T 3323 现行。第 7 批修正 | 是 | 已修正：按修正后取值复核，与所引标准一致。 |
| tools/welding/weld-strength.html | GB 50017 钢结构设计标准 | 角焊缝有效厚度 `h_e=0.7h_f`；对接/角焊缝按有效厚度与设计强度计算 | GB 50017-2017 现行。第 10 批复核 | 是 | 一致：角焊缝 h_e=0.7h_f 与 GB 50017-2017 第 11.2.2 条一致；对接焊缝按有效厚度计算。 |
| tools/manufacturing/quality-control.html | AIAG SPC 手册（CP/CPK/PP/PPK） | CP=T/(6σ)、CPK=min(USL−μ, μ−LSL)/(3σ)；PPK 改用长期标准差 σ_LT，不再误用 PP=T/(6σ) | AIAG SPC 现行口径。第 7 批修正 | 是 | 已修正：按修正后取值复核，与所引标准一致。 |
| tools/manufacturing/capacity-planning.html | 无外部标准；产能=机台×班产×班次×工作日 | 预设「小规模/大规模」原注入 2.5/7.5 台（非整数，触发校验拦截），改为 3/8 台 | 不引用外部标准。第 8 批修正预设 | 是 | 已修正：按修正后取值复核，与所引标准一致。 |
| tools/manufacturing/defect-rate.html | 无外部标准；FTY/RTY/PPM/DPMO 按题设每件每工序 1 个机会 | `FTY=1−d/t`、`RTY=FTY^工序数`、`DPMO=d/(t×工序数)×10⁶` | 不引用外部标准（题设计 1 机会/件/工序）。第 10 批复核 | 是 | 一致（口径）：FTY/RTY/DPMO 与题设「每件每工序 1 个机会」自洽，无外部标准可冲突。 |
| tools/surveying/end-area-volume.html | GB 50026-2020 工程测量标准 | 平均断面法 `V=L(A1+A2)/2`；页面提示棱柱体校正项，但主算只用平均断面法 | GB 50026-2020 现行。第 10 批复核 | 是 | 一致（主算）：实际计算只用 V=L(A1+A2)/2；棱柱体校正项未参与主算，不产生偏差。 |
| tools/surveying/prismoidal-volume.html | GB 50026-2020 工程测量标准 | `V=L/6(A1+4Am+A2)`；示例 20/6×(100+4×80+60)=1600 m³ | GB 50026-2020 现行。第 10 批复核 | 是 | 一致：辛普森棱柱体公式 V=L/6(A1+4Am+A2)，示例实算 1600 m³，无偏差。 |
| tools/surveying/earthwork-pyramid-volume.html | GB 50026-2020 工程测量标准 | 棱锥/圆锥 `V=A·h/3`（A 为底面积）（原台账误记为棱台公式） | GB 50026-2020 现行。第 10 批复核 | 是 | 一致（更正台账）：代码为 V=A·h/3，非棱台 h/3(A1+A2+√A1A2)；原台账记录有误，已更正。 |
| tools/surveying/area-calc.html | GB 50026-2020 / ISO 80000-1 | 坐标法面积 `A=½·ABS(Σ(x_i·y_{i+1}−x_{i+1}·y_i))`；单位换算 | GB 50026-2020 / ISO 80000-1 现行。第 10 批复核 | 是 | 一致：鞋带公式与 GB 50026-2020 坐标法面积口径一致；单位换算按 ISO 80000-1 十进制前缀。 |
| tools/energy/daily-irradiation.html | IEC 61724 光伏系统性能监测 | 日辐照量按峰值日照小时 × 系统容量 | IEC 61724 现行。已复核（第 6 批修图表口径） | 是 | 已修正：按修正后取值复核，与所引标准一致。 |
| tools/energy/wind-power-estimator.html | IEC 61400-1 / IEC 61400-12-1 | `P=0.5ρA v³ Cp`；风速按轮毂高度幂律修正 | IEC 61400 系列现行。已复核（第 6 批修双轴混装） | 是 | 一致（已复核） |
| tools/energy/air-purifier-area.html | GB/T 18801-2022 空气净化器 | 适用面积=CADR×(0.07–0.12) 经验系数 | GB/T 18801-2022 现行。第 10 批复核 | 是 | 一致（经验式）：GB/T 18801-2022 未规定面积换算系数；0.07–0.12 为经验值，页面已标注，无冲突。 |
| tools/energy/water-tds-evaluator.html | GB 5749-2022 生活饮用水卫生标准 | TDS 分级阈值 1000 mg/L 等按标准表 1 取值 | GB 5749-2022 现行。第 10 批复核 | 是 | 一致：1000 mg/L 分界与 GB 5749-2022 表 1 TDS 限值一致（≤1000 与 >1000 分级）。 |
| tools/construction/calc-5.html | GB 4814-84 原木材积表 | D≤12cm 用 `V=0.00007854·L·(D+0.45L+0.2)²`；D≥14cm 用 `V=0.00007854·L·(D+0.5L+0.005L²+0.000125L(14−L)²(D−10))²`；千板英尺按 1 m³=0.423776 MBF（原误按 ×1000 显示） | GB 4814-84 现行。第 9 批修正（原单式不分径级、示例 D 用米、MBF 换算错误） | 是 | 已修正：按修正后取值复核，与所引标准一致。 |
| tools/construction/estimate-area-dosage.html | 无外部标准；按涂布厚度与材料密度估算（参考产品涂布率） | 总厚=单遍厚×遍数；体积=面积×总厚÷1000；净重=体积×密度；含损耗=净重×(1+损耗%)；桶数=⌈含损耗÷每桶⌉；预设遍数由 1 改为与页面默认 2 一致 | 不引用外部标准。第 9 批修正（原示例算术与工具口径不符、预设与默认不一致） | 是 | 已修正：按修正后取值复核，与所引标准一致。 |
| tools/energy/conductive-heat-rate.html | Fourier 1822 导热定律；Incropera《传热传质基础》 | 平壁稳态 `Q=k·A·ΔT/d`；热流密度 `Q/A`；单位面积热阻 `d/k`；示例按 k=0.04 计算 2.4 W（原误用钢 k=45 且把 2700 写成 270） | Fourier 定律现行教材口径。第 9 批修正示例 | 是 | 已修正：按修正后取值复核，与所引标准一致。 |
| tools/energy/power-factor-calc.html | 无外部标准；PF=有功/视在（cosφ） | `PF=P/S`；`φ=arccos(PF)×180/π`；`Q=S·sin(arccos(PF))`；三相视在电流 `I=P/(√3·U·cosφ)`（示例原漏 √3，300 A 应为 174 A） | 电工基础口径。第 9 批修正示例 | 是 | 已修正：按修正后取值复核，与所引标准一致。 |
| tools/energy/solar-calculator.html | IEC 61724 光伏系统性能监测（沿用同行业口径） | 日发电=`P×峰值日照×效率÷1000`；年发电=日发电×365；年收益=年发电×(电价+补贴)；初投按 8 元/W；回本=初投÷年收益；减排按 0.581 kg CO₂/kWh；示例已按代码口径重算（6424 kWh、17.1 年） | IEC 61724 现行。第 9 批修正示例（原 1300 kWh/kWp、3.5 元/W、7–9 年与代码不符） | 是 | 已修正：按修正后取值复核，与所引标准一致。 |
| tools/fire-rescue/calc-1.html | GB 50974-2014 消火栓充实水柱要求（高层 ≥13 m） | `Sk=Hq/(1+φ·Hq)×折减系数`；φ 按 13/16/19/22mm 取 0.0165/0.0124/0.0097/0.0077；对照表统一为 18.1/19.7/20.9/21.9 m（原 18.6/19.8/21.6 与代码不符）；示例 13mm 改 18.1 m | GB 50974-2014 现行；与 GB 55036-2022 不一致处已被替代。第 9 批修正对照表与示例 | 是 | 已修正：按修正后取值复核，与所引标准一致。 |
| tools/welding/hanjiezidonghuapinggu.html | 无外部标准；焊接自动化投资回收期估算 | 机器人单件时间按人工 40%；运行成本=机时×时薪×0.6+投资×2%；年节省=人工成本−运行成本；回收期=投资÷年节省；示例 5000 件实算 32,000 元、9.4 年（原 25,700 元、11.7 年） | 不引用外部标准。第 9 批修正示例 | 是 | 已修正：按修正后取值复核，与所引标准一致。 |
| tools/civil/rebar-anchorage.html | GB 50010-2010 式 8.3.1 基本锚固长度 | `l_ab=0.14×(f_y/f_t)×d`；`l_a=ζ_a·l_ab`；两者分列输出（原把 ζ_a 并入 l_ab、混用 l_ab/l_a） | GB 50010-2010 现行。第 10 批修正 | 是 | 已修正：l_ab 与 l_a 分列，ζ_a 只乘 l_a，与 GB 50010-2010 式 8.3.1 一致。 |
| tools/civil/calc-strength-ratio.html | JGJ 55-2011 水灰比与标准差 σ | σ：≤C15 取 4.0、C20–C35 取 5.0、>C35 取 6.0；`f_cu,0=f_cu,k+1.645σ`；`W/C=α_a·f_ce/(f_cu,0+α_a·α_b·f_ce)` | JGJ 55-2011 现行。第 10 批修正（原 C20 取 σ=4.0、公式为 Bolomey） | 是 | 已修正：σ 阈值与 JGJ 55 表 4.0.2 一致（C20 由 4.0→5.0），W/C 改用 JGJ 55 口径。 |
| tools/civil/concrete-wb-ratio.html | JGJ 55-2011 表 4.0.2 标准差与配制强度 | `__CONCRETE_GRADES` C20 σ 由 4.0 改 5.0；表 C20 行改为 28.2 MPa / 0.689 | JGJ 55-2011 现行。第 10 批修正（表 C20 原 26.6/0.72） | 是 | 已修正：C20 配制强度 20+1.645×5=28.2 MPa（原按 σ=4 得 26.6），W/B 0.689 与代码一致。 |
| tools/civil/masonry-bearing.html | GB 50003-2011 表 6.1.1 允许高厚比 | `β=H₀/h`；`[β]`：M2.5=22、M5=24、M7.5=26；新增 β、[β] 与判定输出 | GB 50003-2011 现行。第 10 批新增高厚比校核 | 是 | 新增：β 与 [β] 按砂浆等级取值，与 GB 50003-2011 表 6.1.1 一致（原页无高厚比校核）。 |
| tools/construction/calc-206.html | GB 55023-2022 分项系数；GB 50009-2012 风荷载；JGJ 130-2011 §5.2.6 | `N=1.3(Ng1+Ng2)+1.5Nq`；`W_k=μz·μs·w₀`；`Mw=0.9×1.4×W_k×a×h²/10` | 三项现行。第 10 批修正 | 是 | 已修正：原 N 用 1.2/1.4、W_k 硬编码 0.6w₀（漏 μz/μs），现按规范取 μz、μs 并更新分项系数。 |
| tools/civil/wind-load.html | GB 50009-2012 风荷载标准值 | `w_k=βz·μz·μs·w₀`；βz 默认由 1.5 改 1.0 | GB 50009-2012 现行。第 10 批修正默认值 | 是 | 已修正：βz 默认 1.5 会无依据放大 50%，改 1.0；公式与 GB 50009-2012 一致。 |
| tools/agriculture/pesticide-interval.html | 《农药标签和说明书管理办法》（农业部令 2017 年第 7 号）第十八条（安全间隔期按标签标注）；GB/T 8321 定义「最后一次施药距收获的天数」 | `phiDays` 接受 ≥0 整数（`parseInt` 后 `phiDays < 0` 拦截）；最早采收日 = 施药日 + phiDays；输入框 `min=0`；负值提示「应为农药标签标注的天数（不小于 0 的整数）」 | 办法现行；农业农村部农药登记标签实例 PD20142114 明示「安全间隔期0天」（中国农药数字监督管理平台 icama.cn）。第 11 批定稿 | 是 | 定稿：0 天为合法标签值，已放宽接受（原 `<1` 拒绝改为 `<0` 拒绝）；0 天 ⇒ 最早采收日 = 施药日，不再静默回退 7 天。 |

## 维护备注

- 本批（第 10 批）更新/复核 20 页：civil 5 页（rebar-anchorage、calc-strength-ratio、concrete-wb-ratio、masonry-bearing、wind-load）+ construction 3 页（calc-1、calc-204、calc-206）+ 13 行「否」复扫页。
- 13 行「否」已全部核对 `calc()` 实际取值并回填第 5 列「是」；第 6 列逐行写明「实际取值 vs 标准要求」偏差（一致 / 已修正 / 更正台账）。其中 calc-1、calc-204 与 earthwork-pyramid 三项为「先改代码/更正记录再回填」。
- 第 10 批新增 6 行（civil 4 + construction 2），当前共 49 个数据行；全部为「是」。
- 凡页面引用 GB 50016 / GB 50084 / GB 50974 / GB 51251 / GB 50140 的，均已在本批或前批加注「现行以 GB 55037-2022 / GB 55036-2022 为准」；后续新页必须沿用该写法。
- 尚未覆盖：GB 50116 火灾自动报警剩余页、GB 51309 应急照明、GB 50017 焊接剩余页、GB 50026 测绘剩余页，后续批次增量补入。
- 第 11 批新增 agriculture 1 行（pesticide-interval）：依据《农药标签和说明书管理办法》第十八条与登记标签实例（PD20142114 标注 0 天），定稿「PHI=0 为合法标签值、负值显式拒绝」。

## 第 12 批：工程族三列核对（工程量 / 配筋 / 荷载 / 水暖电）

| 页面路径 | 页面声称的标准与条款 | 代码实际采用的取值 | 出处与现行状态 | 是否已核对代码取值 | 实际取值 vs 标准要求 |
|---|---|---|---|---|---|
| tools/civil/load-combination.html | 承载能力极限状态基本组合（GB 55001-2021 / GB 50068-2018） | `S=γ_G·S_Gk+γ_Q·S_Qk`；默认 γ_G=1.3、γ_Q=1.5；S_Gk、S_Qk 全空时提示并 return | GB 55001-2021 现行。第 12 批复核 | 是 | 一致：1.3/1.5 为现行分项系数；原公式说明仍写「无输入守卫，空值按 0」，已按实际守卫更新 |
| tools/civil/active-earth-rankine.html | Rankine（1857）主动土压力；页面声明 φ 取 0–45° | `K_a=tan²(45°−φ/2)`；`E_a=½γH²K_a−2cH√K_a+2c²/γ`；守卫由 `φ≤0` 改 `φ<0` | 经典朗金理论。第 12 批修正边界 | 是 | 已修正：原代码拒绝 φ=0，与「0–45°」声明矛盾；φ=0 时 K_a=1、公式仍成立 |
| tools/civil/rc-beam-rebar.html | GB 50010-2010 式 6.2.7/6.2.10 相对界限受压区高度 | `α_s=M/(α₁f_cbh₀²)`；超筋判据原 `α_s>0.44`，改为 `α_s>ξ_b(1−0.5ξ_b)`，`ξ_b=0.8/[1+f_y/(2×10⁵×0.0033)]` | GB 50010-2010（2015 版）现行。第 12 批修正 | 是 | 已修正：HRB400 的 ξ_b=0.518、α_s,max≈0.384；原 0.44 会放行 ξ>ξ_b 的少筋/超筋截面（脆性破坏） |
| tools/civil/one-way-slab.html | GB 50010-2010 式 6.2.7/6.2.10 相对界限受压区高度 | 同 rc-beam-rebar，单位宽板带 b=1000 mm；超筋判据改为 `ξ_b(1−0.5ξ_b)` | GB 50010-2010（2015 版）现行。第 12 批修正 | 是 | 已修正：同上，原 0.44 阈值高于 HRB400 的 0.384 |
| tools/civil/rebar-anchorage.html | GB 50010-2010 8.3.1 锚固长度构造下限 | `l_ab=0.14(f_y/f_t)d`；`l_a=max(ζ_a·l_ab, 200 mm)` | GB 50010-2010 现行。第 12 批补构造下限 | 是 | 已修正：原 `l_a=ζ_a·l_ab` 无 200 mm 下限，与 8.3.1「锚固长度不应小于 200mm」不符 |
| tools/construction/brick-calculator.html | GB/T 5101-2017（砖规格）；工程定额砂浆用量 2.1–2.4 m³/10m³ | 砂浆量 `V·灰缝率·(1+损耗)`；水泥 250 kg/m³；中砂由 `mortar×1.0` 改 `mortar×1.5`（t），m³ 口径 ÷1.5 | 定额经验值。第 12 批修正单位口径 | 是 | 已修正：原「吨」值与同行「约 m³（÷1.5）」自相矛盾；按中砂 1.5 t/m³、体积≈砂浆体积统一 |
| tools/construction/area-calculator.html | GB/T 17986.1-2000 房产测量；得房率=套内/建筑面积 | `公摊面积=套内×r/(100−r)`；`建筑面积=套内+公摊`；输入标签与正文由「公摊系数」改「公摊率」 | GB/T 17986.1-2000 现行。第 12 批修正命名 | 是 | 已修正：公式实际按公摊率（占建筑面积）计算，原名「公摊系数」（占套内）与实现不符 |

### 维护备注（第 12 批）

- 本批按四族抽样核对 35 页：工程量 8、配筋 9、荷载 9、水暖电 9。
- 发现并修正 7 项不一致（上表 7 行）；其余 28 页「声明口径 / 实现口径 / 外部参照」一致，无改动。
- 已复核但未改的代表页：荷载族 `slope-stability-fos`、`beam-udl`、`dijichengzailijisuan`、`assessor-19`、`calc-206`、`wind-load`、`masonry-bearing`、`calc-204`；配筋族 `two-way-slab`（弹性理论系数表，页面标注经验系数）、`isolated-footing`（pmin≥0 / pavg≤f_a / pmax≤1.2f_a 与 GB 50007-2011 5.2 一致）、`pile-capacity`、`cft-capacity`（页面明示简化约束增强系数 1.2）、`rebar-weight`、`calc-2`；工程量族 `concrete-volume`、`excavation-earth`、`calc-dosage-1`、`calc-5`（原木材积 GB/T 4814 公式）、`estimate-area-dosage`、`cost-estimator`；水暖电族 `cooling-load`、`kongtiaolengfuhejisuan`、`duct-calculator`、`pump-calculator`、`calc-1`、`calc-2`、`breaker-sizing`、`voltage-drop`、`transformer-sizing`。
- 留待统一：`calc-206` 同页 N 用 GB 55023-2022 的 1.3/1.5、Mw 仍用 JGJ 130-2011 的 0.9×1.4（页面已注明两套出处，跨规范混用但未判缺陷；若要统一为 1.5 需同步改 3 处 verify 期望）。

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

## 第 17 批：`a_s` vs `c` 概念清扫 + 裂缝宽度补齐（2026-11-05）

### 任务 1：`a_s` / `c` 混淆扫描（civil / construction / structural）

扫描口径：`id="as"`、`h₀ = h − a_s`、label 含「保护层」、正文含 `a_s`。结果：**仅 2 页设 `a_s` 输入，2 页均把标签写成「保护层 a_s」，均判混淆并已改**；`h₀` 算式 2/2 正确；默认值 2/2 合理。

| 页面 | 标签原文 | 是否混淆 | h₀ 算式 | 判定 |
|---|---|---|---|---|
| tools/civil/rc-beam-rebar.html | `保护层 a_s (mm)` | **是**：把 a_s 叫保护层 | `h0=h-as_`（页面与 extras 一致） | 已改为 `a_s 受拉钢筋合力点至受拉边缘距离 (mm)`；默认 40mm（单排梁合理） |
| tools/civil/one-way-slab.html | `保护层 a_s (mm)` | **是**：把 a_s 叫保护层 | `h0=h-as_` | 已改为 `a_s 受拉钢筋合力点至板底距离 (mm)`；默认 20mm（板单排合理） |

- 其余页面（`construction`/`structural` 全部、`civil` 其他页）无 `a_s` 输入；`rebar-anchorage` 仅正文提保护层、无 `h₀` 计算，不涉及混淆。
- 两页均补「c 为保护层厚度、a_s 为合力点距离，h₀=h−a_s，不可用 c 代替 a_s」的说明；英文词典同步。
- 未发现「用 c 值当 a_s」导致 h₀ 偏小的页面（2 页默认 a_s 分别为 40/20mm，均含保护层 + 钢筋半径量级）。

### 任务 2：裂缝宽度验算落到 `civil/rc-beam-rebar`

在既有页新增「正常使用极限状态（裂缝宽度）」输入组（M_k、A_s、d、c、f_tk、钢筋类型 ν），按 GB 50010-2010 式 7.1.2 实现：

- `A_te = 0.5bh`（矩形受弯）；`ρ_te = A_s/A_te`，`<0.01` 取 `0.01`；
- `σ_s = M_k/(0.87h₀A_s)`；`ψ = 1.1 − 0.65f_tk/(ρ_te σ_s)`，夹取 `0.2≤ψ≤1.0`；
- `d_eq = d/ν`（带肋 1.0、光面 0.7，等价于 `Σn_i d_i²/Σn_iν_i d_i` 单直径形式）；
- `w_max = 1.9·ψ·σ_s/2×10⁵·(1.9c + 0.08d_eq/ρ_te)`；
- 对照 GB 50010-2010 表 3.3.1 三级 0.3mm（页面同时标注二级 0.2mm、一级 0.1mm/预应力）。

**实跑算例（node 取值，页面默认 b=250、h=500、h₀=460、A_te=62500）**：

| 场景 | 输入 | σ_s (MPa) | ψ | ρ_te | d_eq | w_max (mm) | 判定 |
|---|---|---|---|---|---|---|---|
| ψ 上夹取 | Mk=500、A_s=942 | 1326.3 | 1.000（raw 1.0346） | 0.0151 | 20.0 | 1.936 | 不满足 |
| ψ 下夹取 | Mk=1、A_s=3000 | 0.8 | 0.200（raw −31.58） | 0.0480 | 20.0 | 0.000 | 满足 |
| ρ_te<0.01 抬升 | Mk=300、A_s=400 | 1874.1 | 1.000 | 0.0100（raw 0.0064） | 20.0 | 3.694 | 不满足 |
| 超限不满足 | Mk=60、A_s=400 | 374.8 | 0.751 | 0.0100 | 20.0 | 0.555 | 不满足 |
| 光面 ν=0.7 | Mk=80、A_s=942、ν=0.7 | 212.2 | 0.692 | 0.0151 | 28.6 | 0.278 | 满足 |
| 满足（非默认） | Mk=60、A_s=942 | 159.2 | 0.555 | 0.0151 | 20.0 | 0.129 | 满足 |

**同步**：页面（输入组 + calcTool + extras 表格 + 图表历史字段）→ `i18n/tools/content_deepdive.json`（新增「裂缝宽度验算」示例与 c/a_s FAQ，`indent=1`，`json.loads` 校验）→ 页面深度块由 `_build_deep_dive_html` 同源重渲染 → `i18n/tools/en/civil/rc-beam-rebar.json`（新增 30 键）→ `scripts/verify_civil_calc.js` 新增 6 用例。

**校验**：`node scripts/verify_civil_calc.js` = **57/57**；`node scripts/discriminate_check.js verify_civil_calc.js` = **57/57 变红、0 逃生项**（含恢复默认输入）。未跑 `_build.py`、未 push。

**构建保留判断**：deep-dive 区块已按 `_build.py::_build_deep_dive_html` 的同一函数从 JSON 重新渲染，下一次构建会产出**逐字节同值**；输入组、`calcTool`、`rcBeamSls()`、extras 均在深度块之外，构建不改写。复查口径：构建后 `grep -c 'rcBeamSls'` 不变、`grep -c '2.56'` 仍为 0。
