# 全站规范引用台账（standards-map）

> 用途：逐个工具页核对「页面声称的标准/条款」与「代码实际取值」是否一致，并记录标准现行状态。
> 维护：随批次增量追加；已被 GB 550xx-2022 通用规范替代的条文必须在页面注明「现行以 GB 550xx-2022 为准」。
> 状态口径：`现行` / `已修订` / `部分被 GB 550xx-2022 替代` / `已被 GB 550xx-2022 替代`。

| 页面路径 | 页面声称的标准与条款 | 代码实际采用的取值 | 出处与现行状态 |
|---|---|---|---|
| tools/fire-rescue/fire-extinguisher-selection.html | GB 50140-2005 表 6.2.1（A 类）；B/C/E 类此前误用同一张 A 类表 | A 类按 100/75/50 m²/A；B/C/E 类改按表 6.2.2 取 1.5/1.0/0.5 m²/B，单具最小 21B/55B/89B；D/F 类不再套算，提示按专项规范 | GB 50140-2005 现行；强制性要求以 GB 55036-2022 为准（已加页内说明）。第 8 批修正 |
| tools/fire-rescue/calc-4.html | GB 50140-2005 表 6.2.1（原页面对 B/C 类也写 6.2.1） | B/C 类 `coverage` 表取 1.5/1.0/0.5 m²/B，与表 6.2.2 一致；引用改为按火灾类别切换表号 | GB 50140-2005 现行；GB 55036-2022 已加说明。第 8 批修正表号 |
| tools/fire-rescue/sprinkler-design.html | GB 50084-2017 表 5.0.1；仓库Ⅰ级 6 L/(min·m²)、200 m² | 民用/厂房按表 5.0.1；仓库Ⅰ级按第 5.0.4 条 / 表 5.0.4；设计流量 `Q=K√(10P)`；消防水池按 1 小时 × 3.6 换算 m³（原误按 L/s×60 显示 L，差 60 倍） | GB 50084-2017 现行；与 GB 55036-2022 不一致处已被替代。第 8 批修正表号与水池单位 |
| tools/fire-rescue/smoke-management.html | GB 51251-2017；NFPA 92 轴对称烟羽；排烟量安全系数 1.2 | 质量流量 `0.071 Qc^(1/3) z^(5/3)(1+0.027 Qc^(2/3)/z)`；体积流量改含 ×1.2；ρ₀/T₀ 统一为 1.2 kg/m³、293 K（原公式行写 1.293/273 与正文冲突） | GB 51251-2017 现行；与 GB 55036-2022 不一致处已被替代。第 8 批修正系数与状态量 |
| tools/fire-rescue/fire-resistance-rating.html | GB 50016-2014（2018 版）表 5.1.2 / 表 3.2.1 | 民用等级按第 5.1.3 条；厂房按第 3.2.2、3.2.3 条；仓库按第 3.2.5 条（原统一误标 3.2.1） | GB 50016-2014（2018 局部修订）现行；强制性条文已被 GB 55037-2022 替代。第 8 批修正条号并加说明 |
| tools/fire-rescue/length-distance.html | GB 50974-2014 消防水带沿程损失 | Hazen-Williams（C=140）换算 MPa；「默认参数」预设 DN50 与页面默认 DN65 不一致，已统一为 DN65 | GB 50974-2014 现行；部分被 GB 55036-2022 替代。第 8 批修正预设 |
| tools/fire-rescue/hydrant-flow.html | GB 50974-2014 §7.4.7；栓口动压 0.35/0.25 MPa、充实水柱 13/10 m | `q=√(P/(1/B+A·L))`、`Sk=Hq/(1+φHq)`；新增 P>0.50 MPa 减压提示（>0.70 MPa 必须减压） | GB 50974-2014 现行；与 GB 55036-2022 不一致处已被替代。第 8 批补超压校核 |
| tools/fire-rescue/fire-alarm-zone.html | GB 50116-2013 探测区域划分 | 探测区域上限 500 m²（原 5000 m² 多一位）；单层大空间楼层数按 1 计 | GB 50116-2013 现行。第 7 批修正 |
| tools/fire-rescue/ventilation-tactics.html | GB 51251-2017 §3.4.6 正压送风余压 | 25–30 Pa（原 40–50 Pa） | GB 51251-2017 现行；与 GB 55036-2022 不一致处已被替代。第 7 批修正 |
| tools/fire-rescue/fire-load.html | GB 50016-2014 火灾荷载密度分级 | 分级表与进度条上限统一为 2000 MJ/m²；总热值 ÷ 面积 | GB 50016-2014 现行。第 7 批修正 |
| tools/fire-rescue/time-air.html | GB/T 16556-2007 自给开路式压缩空气呼吸器 | 6.8 L/30 MPa 气瓶可用空气量按 2013 L；撤离余量 18%（原 2040 L、25%） | GB/T 16556-2007 现行。第 7 批修正 |
| tools/fire-rescue/detector-20.html | GB 50166-2019 / GB 50261-2017 / GB 50974-2014 施工验收 | 评分项按各系统验收条款分档，满分 100% | 三项均现行；GB 50974 与 GB 55036-2022 不一致处已被替代。第 7 批复核 |
| tools/fire-rescue/time-evacuation.html | GB 50016 / GB 51251-2017 疏散与排烟 | ASET−RSET 安全裕度；RSET 三项全 0 时改为报错 | GB 50016 现行；GB 51251-2017 部分被 GB 55036-2022 替代。第 7 批补校验 |
| tools/fire-rescue/sprinkler-design.html（水锤/流量校核行） | GB 5135.1-2019 / ISO 6182 喷头流量系数 K | K 值按 80/115/160 等档，`q=K√(10P)` | GB 5135.1-2019 现行。已复核 |
| tools/construction/concrete-calculator.html | JGJ 55-2011 配合比；GB 50666-2011 施工；GB 50010-2010 结构 | 配合比表按强度等级经验值；模板系数按 `m²/m³` 口径（楼板 8.5、梁 9、柱 10、墙 12、基础 2、楼梯 5） | JGJ 55-2011 / GB 50666-2011 / GB 50010-2010 现行。第 8 批修正参考表自相矛盾（楼板原写 2–3、楼梯原写 8–10） |
| tools/construction/cement-mortar-ratio.html | JGJ/T 98-2010 砌筑砂浆配合比 | 水泥经验基准 M5 220、M7.5 280、M10 330、M15 380 kg/m³；砂=水泥×砂比；M10 统一 1:4.5、M7.5 1:4.8 | JGJ/T 98-2010 现行。第 8 批修正图表水泥基准（原图 M5 用 340 与结果 220 不一致）及示例砂量 |
| tools/construction/calculator-calc-ratio-2.html | JGJ 55-2011 水灰比/砂率 | C20 水泥 330、水 185、砂 700、石 1185；水灰比 0.56、砂率 37.1% | JGJ 55-2011 现行。第 8 批复核（数值与表一致） |
| tools/construction/calc-1.html | JGJ 130-2011 扣件式钢管脚手架 | 立杆稳定性 `N/(φA)+Mw/W≤f`；λ=l₀/i（l₀ 由 m 转 mm） | JGJ 130-2011 现行。已复核 |
| tools/construction/calc-204.html | JGJ 162-2008 模板支架；GB 50009-2012 荷载；GB 50666-2011 | `s=√(Pa/q)`，支撑数 ⌈L/s⌉×⌈H/s⌉，实际荷载 q·sL·sH | JGJ 162-2008 / GB 50009-2012 / GB 50666-2011 现行。已复核 |
| tools/construction/calc-205.html | JGJ 130-2011 脚手架钢管用量 | 立杆 ⌈L/纵距⌉+1×2 排；横杆 步数×排数×排距；剪刀撑按 6 m 分段 | JGJ 130-2011 现行。已复核 |
| tools/construction/ac-size-guide.html | GB 21455-2019 能效；GB/T 7725-2022 空调器；GB 50736-2012 供暖通风 | 冷负荷按面积×指标×修正，1 匹=2500 W（原 2324 W） | 三项现行；GB 50736 与 GB 55015-2021 不一致处以其为准。第 7 批修正 |
| tools/construction/window-shading.html | GB 50189-2015 节能设计；GB 55015-2021 | 外遮阳系数按几何投影近似，并注明不能直接套用 GB 50189 的 SC 限值 | GB 50189-2015 现行；节能强制性指标已被 GB 55015-2021 替代。已复核 |
| tools/construction/blueprint-tool.html | GB/T 50001-2017 房屋建筑制图；GB/T 14689-2008 图纸幅面 | 图纸比例换算；CAD 单位下拉（mm/cm/m）参与换算（原为死控件） | 两项现行。第 6 批修正 |
| tools/welding/detector-25.html | NB/T 47013 承压设备无损检测；GB/T 3323 射线检测；ISO 17635 | 角焊缝按 RT/UT 适用性给提示，不套用对接焊缝缺陷等级 | NB/T 47013 现行；GB/T 3323 现行。第 7 批修正 |
| tools/welding/weld-strength.html | GB 50017 钢结构设计标准 | 对接/角焊缝按有效厚度与设计强度计算 | GB 50017-2017 现行。已复核 |
| tools/manufacturing/quality-control.html | AIAG SPC 手册（CP/CPK/PP/PPK） | CP=T/(6σ)、CPK=min(USL−μ, μ−LSL)/(3σ)；PPK 改用长期标准差 σ_LT，不再误用 PP=T/(6σ) | AIAG SPC 现行口径。第 7 批修正 |
| tools/manufacturing/capacity-planning.html | 无外部标准；产能=机台×班产×班次×工作日 | 预设「小规模/大规模」原注入 2.5/7.5 台（非整数，触发校验拦截），改为 3/8 台 | 不引用外部标准。第 8 批修正预设 |
| tools/manufacturing/defect-rate.html | 无外部标准；FTY/RTY/PPM/DPMO 按题设每件每工序 1 个机会 | `FTY=1−d/t`、`RTY=FTY^工序数`、`DPMO=d/(t×工序数)×10⁶` | 口径已在页内注明；DPMO 假设需与机会数一致。已复核 |
| tools/surveying/end-area-volume.html | GB 50026-2020 工程测量标准 | 平均断面法 `V=L(A1+A2)/2`，棱柱体校正 `L/3(A1+A2+√A1A2)` | GB 50026-2020 现行。已复核 |
| tools/surveying/prismoidal-volume.html | GB 50026-2020 工程测量标准 | `V=L/6(A1+4Am+A2)`；示例 20/6×(100+4×80+60)=1600 m³ | GB 50026-2020 现行。已复核 |
| tools/surveying/earthwork-pyramid-volume.html | GB 50026-2020 工程测量标准 | 棱台 `V=h/3(A1+A2+√A1A2)` | GB 50026-2020 现行。已复核 |
| tools/surveying/area-calc.html | GB 50026-2020 / ISO 80000-1 | 坐标法面积与单位换算 | GB 50026-2020 现行。已复核 |
| tools/energy/daily-irradiation.html | IEC 61724 光伏系统性能监测 | 日辐照量按峰值日照小时 × 系统容量 | IEC 61724 现行。已复核（第 6 批修图表口径） |
| tools/energy/wind-power-estimator.html | IEC 61400-1 / IEC 61400-12-1 | `P=0.5ρA v³ Cp`；风速按轮毂高度幂律修正 | IEC 61400 系列现行。已复核（第 6 批修双轴混装） |
| tools/energy/air-purifier-area.html | GB/T 18801-2022 空气净化器 | CADR ÷ 适用面积按 0.07–0.12 系数换算 | GB/T 18801-2022 现行。已复核 |
| tools/energy/water-tds-evaluator.html | GB 5749-2022 生活饮用水卫生标准 | TDS 限值 1000 mg/L 等按标准表 1 取值 | GB 5749-2022 现行。已复核 |

## 维护备注

- 本批（第 8 批）新增/更新 10 页：fire-extinguisher-selection、calc-4、sprinkler-design、smoke-management、fire-resistance-rating、length-distance、hydrant-flow、concrete-calculator、cement-mortar-ratio、capacity-planning。
- 已核对但无需改代码的页面：calculator-calc-ratio-2、calc-1、calc-204、calc-205、ac-size-guide、window-shading、blueprint-tool、detector-25、weld-strength、defect-rate、surveying 四页、energy 四页。
- 凡页面引用 GB 50016 / GB 50084 / GB 50974 / GB 51251 / GB 50140 的，均已在本批或前批加注「现行以 GB 55037-2022 / GB 55036-2022 为准」；后续新页必须沿用该写法。
- 尚未覆盖：GB 50116 火灾自动报警剩余页、GB 51309 应急照明、GB 50017 焊接剩余页、GB 50026 测绘剩余页，后续批次增量补入。
