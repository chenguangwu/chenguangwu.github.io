## Z 批新增假工具候选（2026-11-04）

| 分类 | 页面 | 类型 | 证据（当前行号） | 来源条目 | 说明 |
|---|---|---|---|---|---|
| IT开发 | `tools/it/text-qr.html` | B | `:247-267` 3 个定位图形（`:249-257`）+ 定时线（`:259`），数据区 `:260-265` 按 `strHash(text)` 逐格 `rnd()<0.5` 填色；`:248` `N=29` 写死；无分段/比特流/Reed-Solomon/格式信息/掩码，扫码无内容 | `plan/categories/01-IT开发/it.md` IT-N550 | 伪二维码（同 `email-qr`/`location-qr`） |
| 工程制造 | `tools/machinery/lifespan-20.html` | C | `:209-210,232` 精度因子 1.0–1.5、润滑因子 0.8–1.5 无 ISO 281 依据，且 `precisionLife=L10h*cf*lf` 把润滑二次计入（P2+喷油可放大至疲劳寿命 2.25 倍，与注文相反）；`:235-236,243` dn 值按 `n*25` 写死内径 25 mm，无内径输入 | `plan/categories/08-工程制造/machinery-metalwork.md` MM-H95/H96 | 核心结论失真 |
| 工程制造 | `tools/machinery/speed-26.html` | C | `:206-214,218-219` 链号表每档只有单一 `maxKw/maxRpm`，与转速/齿数/排数无关，却称「查 06B~24A 额定功率/转速表」；`:217-220,228-233` 超表上限静默沿用 24A | `plan/categories/08-工程制造/machinery-metalwork.md` MM-H102/H103 | 额定功率表名不副实 |
| 工程制造 | `tools/metalwork/analysis-36.html` | C | `:117` 英文副标题称 "assess likely causes and remedies"，`:286-292` 实际只做「数量×权重」统计，成因/对策、标准差、控制界限、位置溯源均未实现 | `plan/categories/08-工程制造/machinery-metalwork.md` MM-H114 | 诊断能力未实现 |
| 工程制造 | `tools/metalwork/analysis-cost-price-5.html` | C | `:125` 标题含「成本」、`:191-203` 引据表列材料成本=体积×密度×单价与总成本=材料+加工+损耗+废品率，页面 `:220-256` 只有价格序列统计，无任何成本输入 | `plan/categories/08-工程制造/machinery-metalwork.md` MM-H117 | 成本分析未实现 |
| 农业养殖 | `tools/fishery/calc-39.html` | C | `:10,34` 描述与 JSON-LD 称「输入体重/水温/投喂率算日投喂量」，`:116-123` 实际只有两个数字输入与求部分/百分比/增长率三页签，无体重/水温/投喂率字段 | `plan/categories/10-农业养殖/fishery-aquaculture.md` 10-H34 | 承诺工具与实际不符 |

## AA 批新增假工具候选（2026-11-04）

| 分类 | 页面 | 类型 | 证据（当前行号） | 来源条目 | 说明 |
|---|---|---|---|---|---|
| 工程制造 | `tools/metalwork/calc-gear-2.html` | C | `:127,224-227` 英文副标题承诺 "for spur and helical gears"，但无螺旋角 β 输入，`da=m(z+2)`、`df=m(z−2.5)`、`db=mzcos20°` 全按直齿，斜齿几何未实现 | MM-H125 | 斜齿承诺未实现 |
| 工程制造 | `tools/metalwork/pinpaijiazhipinggujisuan.html` | C | `:127,186-199` 引据表称 ISO 10668 收益法/许可费节省法，实算为「利润×乘数×年限×份额」自定义模型且无折现；`:241-242,436` 科技预设 2 亿营收×20%×10×1.3×2.5 = 13 亿（6.5 倍营收） | MM-H143 | 冒用国标口径 |
| 工程制造 | `tools/metalwork/pressure-casting.html` | C | `:127,130` 承诺输出浇注/冷却工艺参数、引据表列压射比压与 Chvorinov 凝固时间，`:182-195` 均未计算；`:550` ISO 8062-3（尺寸公差）被标为比压出处 | MM-H146 | 工艺参数未实现 |
| 工程制造 | `tools/metalwork/resistance-2.html` | C | `:128,183-197` 承诺推荐工艺参数，结果只有方法/保护气体/质量/成本，无电流、电压、气流量；热输入 Q、碳当量 CE、预热温度三项均未实现 | MM-H152 | 工艺参数未实现 |
| 农业养殖 | `tools/fishery/calc-power.html` | C | `:10,123,126,130-132` 承诺「水体体积+目标温差+保温条件」估越冬加热功率，实际仅电压/电流→`P=V×I`；体积/温差/保温系数/电费均无输入，参考表 `ρVcΔT/t` 未使用 | 10-H36 | 承诺模型未实现 |
| 农业养殖 | `tools/fishery/density-1.html` | C | `:10,126,130-132,152-154` 承诺「面积+产量目标+规格」平衡单产与存活率，实际只算总尾数÷面积；SC/T 2008 参考表未使用；`:380-382` 预设虾苗密度 2000–3000 尾/亩，低于常规 3–10 万尾/亩 10–50 倍 | 10-H40 | 承诺模型未实现且量级错 |
| 农业养殖 | `tools/fishery/estimate-23.html` | C | `:10,152-155,195-197` 承诺「显微镜计数分类数量与体积→生物量与群落结构」，实际只有基准值×(1+增长率/100)；`N=n·V/v` 与 1 mm³/L≈1 mg/L 均未实现 | 10-H42 | 承诺模型未实现 |
| 文娱爱好 | `tools/sports/simulator-18.html` | C | `:10-11,112` 标题/描述称「高原（低氧）适应模拟／不同海拔下血氧与通气量」，`:120-121` 实际只输入模拟次数+概率，`:116` 伯努利蒙特卡洛，`:208` 仅算成功频率与标准误；无海拔/SpO₂/通气量输入 | `plan/categories/05-生活消费/sports-fitness.md` SF-N103 | 通用概率模拟器套壳 |

## AB 批新增假工具候选（2026-11-04）

| 分类 | 页面 | 类型 | 证据（当前行号） | 来源条目 | 说明 |
|---|---|---|---|---|---|
| 农业养殖 | `tools/fishery/ratio-hormone.html` | C | `:10-11,122,126,130-132,382-384` meta/JSON-LD 写「输入亲鱼体重与催产方案，计算 PG/HCG/LRH-A 适宜剂量与配比」，实际只有「数值 A/数值 B」通用字段，无体重/药种/方案/单尾总量；`formula-eq` 自述为代码口径的最简整数比；`:198-202` 「A 占比」实为 A÷B×100（100/50→200%） | 10-H52 | 激素剂量承诺未实现 |
| 农业养殖 | `tools/fishery/temp-density.html` | C | `:10-11,111,122,126-132,193-204` 标题/描述/JSON-LD 称「鱼苗运输成活率（温度/密度）」，实际无密度/时长/成活率字段，只按水温算饱和溶氧并给饱和度；英文 h2 `:111` 仍写 "Fry Transport Survival (Temperature/Density)" | 10-H56 | 运输成活率承诺未实现 |

## AC 批新增假工具候选（2026-11-04）

| 分类 | 页面 | 类型 | 证据（当前行号） | 来源条目 | 说明 |
|---|---|---|---|---|---|
| 文娱爱好 | `tools/audio/audio-recorder.html` | C | `:856-874` 宣称「导出 WebM/Opus 或 WAV、导出处理后的音频」，`exportAudio()` 仅下载原始 `loadedBlob`，增益/速度未应用、无 WAV 编码；`:516,693` 扩展名恒 `.webm`，未读 `mediaRecorder.mimeType` | FE-N114/FE-N118 | 导出处理承诺未实现 |
| 文娱爱好 | `tools/audio/analysis-1.html` | C | `:10,123` meta/副标题称「频谱分析（可视化）」「实时绘制频谱图、输入时域信号或采样数据」，全文无 `AnalyserNode`/`canvas`/FFT/文件入口，只有 4 条算术输出 | FE-N117 | 频谱可视化未实现 |
| 设计创意 | `tools/design/color-palette.html` | C | `:248,278` FAQ「会按 WCAG 算出对比度、未达标标红」+ 引据表 4.5:1 条目，全页无相对亮度/对比度计算与红标，仅 `lum>0.5` 选字；默认 #788EED 白字仅 3.05:1 | D-N229 | WCAG 校验承诺未实现 |
| 设计创意 | `tools/design/gradient.html` | C | `:270` 引据表称「按 sRGB 或 oklab 插值，oklab 可用」，页面无 oklab 选项/代码，输出一律浏览器 sRGB 插值 | D-N233 | oklab 插值承诺未实现 |
| 办公文档 | `tools/office/pdf-split.html` | C | `:568,455-466` 宣称「拆分 PDF 为多个小文件」「段数=ceil(总页数/每段页数)」「文件数=段数」，实际无「每段页数」输入且只产出 1 个 PDF | IT-D34 | 多文件拆分承诺未实现 |

