# 全站规范引用台账（standards-map）

> 用途：逐个工具页核对「页面声称的标准/条款」与「代码实际取值」是否一致，并记录标准现行状态。
> 维护：随批次增量追加；已被 GB 550xx-2022 通用规范替代的条文必须在页面注明「现行以 GB 550xx-2022 为准」。
> 状态口径：`现行` / `已修订` / `部分被 GB 550xx-2022 替代` / `已被 GB 550xx-2022 替代`。
> 第 5 列口径：`是` = 已逐行对照页面 `calc()` 取值（有具体修正或明确核对记录）；`否` = 仅抄录页面所述数值，尚未核对代码取值，后续复扫优先补。

| 页面路径 | 页面声称的标准与条款 | 代码实际采用的取值 | 出处与现行状态 | 是否已核对代码取值 |
|---|---|---|---|---|
| tools/fire-rescue/fire-extinguisher-selection.html | GB 50140-2005 表 6.2.1（A 类）；B/C/E 类此前误用同一张 A 类表 | A 类按 100/75/50 m²/A；B/C/E 类改按表 6.2.2 取 1.5/1.0/0.5 m²/B，单具最小 21B/55B/89B；D/F 类不再套算，提示按专项规范 | GB 50140-2005 现行；强制性要求以 GB 55036-2022 为准（已加页内说明）。第 8 批修正 | 是 |
| tools/fire-rescue/calc-4.html | GB 50140-2005 表 6.2.1（原页面对 B/C 类也写 6.2.1） | B/C 类 `coverage` 表取 1.5/1.0/0.5 m²/B，与表 6.2.2 一致；引用改为按火灾类别切换表号 | GB 50140-2005 现行；GB 55036-2022 已加说明。第 8 批修正表号 | 是 |
| tools/fire-rescue/sprinkler-design.html | GB 50084-2017 表 5.0.1；仓库Ⅰ级 6 L/(min·m²)、200 m² | 民用/厂房按表 5.0.1；仓库Ⅰ级按第 5.0.4 条 / 表 5.0.4；设计流量 `Q=K√(10P)`；消防水池按 1 小时 × 3.6 换算 m³（原误按 L/s×60 显示 L，差 60 倍） | GB 50084-2017 现行；与 GB 55036-2022 不一致处已被替代。第 8 批修正表号与水池单位 | 是 |
| tools/fire-rescue/smoke-management.html | GB 51251-2017；NFPA 92 轴对称烟羽；排烟量安全系数 1.2 | 质量流量 `0.071 Qc^(1/3) z^(5/3)(1+0.027 Qc^(2/3)/z)`；体积流量改含 ×1.2；ρ₀/T₀ 统一为 1.2 kg/m³、293 K（原公式行写 1.293/273 与正文冲突） | GB 51251-2017 现行；与 GB 55036-2022 不一致处已被替代。第 8 批修正系数与状态量 | 是 |
| tools/fire-rescue/fire-resistance-rating.html | GB 50016-2014（2018 版）表 5.1.2 / 表 3.2.1 | 民用等级按第 5.1.3 条；厂房按第 3.2.2、3.2.3 条；仓库按第 3.2.5 条（原统一误标 3.2.1） | GB 50016-2014（2018 局部修订）现行；强制性条文已被 GB 55037-2022 替代。第 8 批修正条号并加说明 | 是 |
| tools/fire-rescue/length-distance.html | GB 50974-2014 消防水带沿程损失 | Hazen-Williams（C=140）换算 MPa；「默认参数」预设 DN50 与页面默认 DN65 不一致，已统一为 DN65 | GB 50974-2014 现行；部分被 GB 55036-2022 替代。第 8 批修正预设 | 是 |
| tools/fire-rescue/hydrant-flow.html | GB 50974-2014 §7.4.7；栓口动压 0.35/0.25 MPa、充实水柱 13/10 m | `q=√(P/(1/B+A·L))`、`Sk=Hq/(1+φHq)`；新增 P>0.50 MPa 减压提示（>0.70 MPa 必须减压） | GB 50974-2014 现行；与 GB 55036-2022 不一致处已被替代。第 8 批补超压校核 | 是 |
| tools/fire-rescue/fire-alarm-zone.html | GB 50116-2013 探测区域划分 | 探测区域上限 500 m²（原 5000 m² 多一位）；单层大空间楼层数按 1 计 | GB 50116-2013 现行。第 7 批修正 | 是 |
| tools/fire-rescue/ventilation-tactics.html | GB 51251-2017 §3.4.6 正压送风余压 | 25–30 Pa（原 40–50 Pa） | GB 51251-2017 现行；与 GB 55036-2022 不一致处已被替代。第 7 批修正 | 是 |
| tools/fire-rescue/fire-load.html | GB 50016-2014 火灾荷载密度分级 | 分级表与进度条上限统一为 2000 MJ/m²；总热值 ÷ 面积 | GB 50016-2014 现行。第 7 批修正 | 是 |
| tools/fire-rescue/time-air.html | GB/T 16556-2007 自给开路式压缩空气呼吸器 | 6.8 L/30 MPa 气瓶可用空气量按 2013 L；撤离余量 18%（原 2040 L、25%） | GB/T 16556-2007 现行。第 7 批修正 | 是 |
| tools/fire-rescue/detector-20.html | GB 50166-2019 / GB 50261-2017 / GB 50974-2014 施工验收 | 评分项按各系统验收条款分档，满分 100% | 三项均现行；GB 50974 与 GB 55036-2022 不一致处已被替代。第 7 批复核 | 是 |
| tools/fire-rescue/time-evacuation.html | GB 50016 / GB 51251-2017 疏散与排烟 | ASET−RSET 安全裕度；RSET 三项全 0 时改为报错 | GB 50016 现行；GB 51251-2017 部分被 GB 55036-2022 替代。第 7 批补校验 | 是 |
| tools/fire-rescue/sprinkler-design.html（水锤/流量校核行） | GB 5135.1-2019 / ISO 6182 喷头流量系数 K | K 值按 80/115/160 等档，`q=K√(10P)` | GB 5135.1-2019 现行。已复核 | 否 |
| tools/construction/concrete-calculator.html | JGJ 55-2011 配合比；GB 50666-2011 施工；GB 50010-2010 结构 | 配合比表按强度等级经验值；模板系数按 `m²/m³` 口径（楼板 8.5、梁 9、柱 10、墙 12、基础 2、楼梯 5） | JGJ 55-2011 / GB 50666-2011 / GB 50010-2010 现行。第 8 批修正参考表自相矛盾（楼板原写 2–3、楼梯原写 8–10） | 是 |
| tools/construction/cement-mortar-ratio.html | JGJ/T 98-2010 砌筑砂浆配合比 | 水泥经验基准 M5 220、M7.5 280、M10 330、M15 380 kg/m³；砂=水泥×砂比；M10 统一 1:4.5、M7.5 1:4.8 | JGJ/T 98-2010 现行。第 8 批修正图表水泥基准（原图 M5 用 340 与结果 220 不一致）及示例砂量 | 是 |
| tools/construction/calculator-calc-ratio-2.html | JGJ 55-2011 水灰比/砂率 | C20 水泥 330、水 185、砂 700、石 1185（水灰比 0.56、砂率 37.1%）；C25 水泥 373、砂 660、石 1177、水 190（水灰比 0.51、砂率 35.9%）；示例已与 MIX 表统一 | JGJ 55-2011 现行。第 8 批复核，第 9 批修正 C25 示例（原 350/680/1180 与表不符） | 是 |
| tools/construction/calc-1.html | JGJ 130-2011 扣件式钢管脚手架 | 立杆稳定性 `N/(φA)+Mw/W≤f`；λ=l₀/i（l₀ 由 m 转 mm） | JGJ 130-2011 现行。已复核 | 否 |
| tools/construction/calc-204.html | JGJ 162-2008 模板支架；GB 50009-2012 荷载；GB 50666-2011 | `s=√(Pa/q)`，支撑数 ⌈L/s⌉×⌈H/s⌉，实际荷载 q·sL·sH | JGJ 162-2008 / GB 50009-2012 / GB 50666-2011 现行。已复核 | 否 |
| tools/construction/calc-205.html | JGJ 130-2011 脚手架钢管用量 | 立杆 ⌈L/纵距⌉+1×2 排；横杆 步数×排数×排距；剪刀撑按 6 m 分段 | JGJ 130-2011 现行。已复核 | 否 |
| tools/construction/ac-size-guide.html | GB 21455-2019 能效；GB/T 7725-2022 空调器；GB 50736-2012 供暖通风 | 冷负荷按面积×指标×修正，1 匹=2500 W（原 2324 W） | 三项现行；GB 50736 与 GB 55015-2021 不一致处以其为准。第 7 批修正 | 是 |
| tools/construction/window-shading.html | GB 50189-2015 节能设计；GB 55015-2021 | 外遮阳系数按几何投影近似，并注明不能直接套用 GB 50189 的 SC 限值 | GB 50189-2015 现行；节能强制性指标已被 GB 55015-2021 替代。已复核 | 否 |
| tools/construction/blueprint-tool.html | GB/T 50001-2017 房屋建筑制图；GB/T 14689-2008 图纸幅面 | 图纸比例换算；CAD 单位下拉（mm/cm/m）参与换算（原为死控件） | 两项现行。第 6 批修正 | 是 |
| tools/welding/detector-25.html | NB/T 47013 承压设备无损检测；GB/T 3323 射线检测；ISO 17635 | 角焊缝按 RT/UT 适用性给提示，不套用对接焊缝缺陷等级 | NB/T 47013 现行；GB/T 3323 现行。第 7 批修正 | 是 |
| tools/welding/weld-strength.html | GB 50017 钢结构设计标准 | 对接/角焊缝按有效厚度与设计强度计算 | GB 50017-2017 现行。已复核 | 否 |
| tools/manufacturing/quality-control.html | AIAG SPC 手册（CP/CPK/PP/PPK） | CP=T/(6σ)、CPK=min(USL−μ, μ−LSL)/(3σ)；PPK 改用长期标准差 σ_LT，不再误用 PP=T/(6σ) | AIAG SPC 现行口径。第 7 批修正 | 是 |
| tools/manufacturing/capacity-planning.html | 无外部标准；产能=机台×班产×班次×工作日 | 预设「小规模/大规模」原注入 2.5/7.5 台（非整数，触发校验拦截），改为 3/8 台 | 不引用外部标准。第 8 批修正预设 | 是 |
| tools/manufacturing/defect-rate.html | 无外部标准；FTY/RTY/PPM/DPMO 按题设每件每工序 1 个机会 | `FTY=1−d/t`、`RTY=FTY^工序数`、`DPMO=d/(t×工序数)×10⁶` | 口径已在页内注明；DPMO 假设需与机会数一致。已复核 | 否 |
| tools/surveying/end-area-volume.html | GB 50026-2020 工程测量标准 | 平均断面法 `V=L(A1+A2)/2`，棱柱体校正 `L/3(A1+A2+√A1A2)` | GB 50026-2020 现行。已复核 | 否 |
| tools/surveying/prismoidal-volume.html | GB 50026-2020 工程测量标准 | `V=L/6(A1+4Am+A2)`；示例 20/6×(100+4×80+60)=1600 m³ | GB 50026-2020 现行。已复核 | 否 |
| tools/surveying/earthwork-pyramid-volume.html | GB 50026-2020 工程测量标准 | 棱台 `V=h/3(A1+A2+√A1A2)` | GB 50026-2020 现行。已复核 | 否 |
| tools/surveying/area-calc.html | GB 50026-2020 / ISO 80000-1 | 坐标法面积与单位换算 | GB 50026-2020 现行。已复核 | 否 |
| tools/energy/daily-irradiation.html | IEC 61724 光伏系统性能监测 | 日辐照量按峰值日照小时 × 系统容量 | IEC 61724 现行。已复核（第 6 批修图表口径） | 是 |
| tools/energy/wind-power-estimator.html | IEC 61400-1 / IEC 61400-12-1 | `P=0.5ρA v³ Cp`；风速按轮毂高度幂律修正 | IEC 61400 系列现行。已复核（第 6 批修双轴混装） | 是 |
| tools/energy/air-purifier-area.html | GB/T 18801-2022 空气净化器 | CADR ÷ 适用面积按 0.07–0.12 系数换算 | GB/T 18801-2022 现行。已复核 | 否 |
| tools/energy/water-tds-evaluator.html | GB 5749-2022 生活饮用水卫生标准 | TDS 限值 1000 mg/L 等按标准表 1 取值 | GB 5749-2022 现行。已复核 | 否 |
| tools/construction/calc-5.html | GB 4814-84 原木材积表 | D≤12cm 用 `V=0.00007854·L·(D+0.45L+0.2)²`；D≥14cm 用 `V=0.00007854·L·(D+0.5L+0.005L²+0.000125L(14−L)²(D−10))²`；千板英尺按 1 m³=0.423776 MBF（原误按 ×1000 显示） | GB 4814-84 现行。第 9 批修正（原单式不分径级、示例 D 用米、MBF 换算错误） | 是 |
| tools/construction/estimate-area-dosage.html | 无外部标准；按涂布厚度与材料密度估算（参考产品涂布率） | 总厚=单遍厚×遍数；体积=面积×总厚÷1000；净重=体积×密度；含损耗=净重×(1+损耗%)；桶数=⌈含损耗÷每桶⌉；预设遍数由 1 改为与页面默认 2 一致 | 不引用外部标准。第 9 批修正（原示例算术与工具口径不符、预设与默认不一致） | 是 |
| tools/energy/conductive-heat-rate.html | Fourier 1822 导热定律；Incropera《传热传质基础》 | 平壁稳态 `Q=k·A·ΔT/d`；热流密度 `Q/A`；单位面积热阻 `d/k`；示例按 k=0.04 计算 2.4 W（原误用钢 k=45 且把 2700 写成 270） | Fourier 定律现行教材口径。第 9 批修正示例 | 是 |
| tools/energy/power-factor-calc.html | 无外部标准；PF=有功/视在（cosφ） | `PF=P/S`；`φ=arccos(PF)×180/π`；`Q=S·sin(arccos(PF))`；三相视在电流 `I=P/(√3·U·cosφ)`（示例原漏 √3，300 A 应为 174 A） | 电工基础口径。第 9 批修正示例 | 是 |
| tools/energy/solar-calculator.html | IEC 61724 光伏系统性能监测（沿用同行业口径） | 日发电=`P×峰值日照×效率÷1000`；年发电=日发电×365；年收益=年发电×(电价+补贴)；初投按 8 元/W；回本=初投÷年收益；减排按 0.581 kg CO₂/kWh；示例已按代码口径重算（6424 kWh、17.1 年） | IEC 61724 现行。第 9 批修正示例（原 1300 kWh/kWp、3.5 元/W、7–9 年与代码不符） | 是 |
| tools/fire-rescue/calc-1.html | GB 50974-2014 消火栓充实水柱要求（高层 ≥13 m） | `Sk=Hq/(1+φ·Hq)×折减系数`；φ 按 13/16/19/22mm 取 0.0165/0.0124/0.0097/0.0077；对照表统一为 18.1/19.7/20.9/21.9 m（原 18.6/19.8/21.6 与代码不符）；示例 13mm 改 18.1 m | GB 50974-2014 现行；与 GB 55036-2022 不一致处已被替代。第 9 批修正对照表与示例 | 是 |
| tools/welding/hanjiezidonghuapinggu.html | 无外部标准；焊接自动化投资回收期估算 | 机器人单件时间按人工 40%；运行成本=机时×时薪×0.6+投资×2%；年节省=人工成本−运行成本；回收期=投资÷年节省；示例 5000 件实算 32,000 元、9.4 年（原 25,700 元、11.7 年） | 不引用外部标准。第 9 批修正示例 | 是 |

## 维护备注

- 本批（第 9 批）新增/更新 8 页：construction/calc-5、construction/estimate-area-dosage、construction/calculator-calc-ratio-2（更新 C25 行）、energy/conductive-heat-rate、energy/power-factor-calc、energy/solar-calculator、fire-rescue/calc-1、welding/hanjiezidonghuapinggu。
- 已填 36 行统一补第 5 列：`是` = 已对照页面 `calc()` 取值（本批或前批有具体修正/核对记录）；`否` = 仅抄录页面数值、尚未核对代码，后续复扫优先补（当前 13 行）。
- 第 8 批新增的 10 页已在表内；第 9 批新增 7 行、更新 1 行，当前共 43 个数据行。
- 凡页面引用 GB 50016 / GB 50084 / GB 50974 / GB 51251 / GB 50140 的，均已在本批或前批加注「现行以 GB 55037-2022 / GB 55036-2022 为准」；后续新页必须沿用该写法。
- 尚未覆盖：GB 50116 火灾自动报警剩余页、GB 51309 应急照明、GB 50017 焊接剩余页、GB 50026 测绘剩余页，后续批次增量补入。
