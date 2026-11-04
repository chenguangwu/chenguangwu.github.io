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
