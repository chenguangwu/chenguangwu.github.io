# 交互有效性扫描（第二轮：点了到底有没有用）

## 2026-11-06 653 页续审检查点（280/653 双跑有效，未销账）

- 基线 `0781ef7e61`，独立工作树 `audit/interaction-review`，历史清单 `/tmp/all653.txt`、旧桶 `/tmp/notclicked-653-classified.json`。截至本次检查点按路径排序前 160 页两次均有效、0 个缺桶、两次桶位逐页一致：B 124、C 30、D-a 4、D-b 1、A 1；还剩 493 页双跑。
- 旧→新仅反映探针迁移、不能代替真值：A→B 2；B→B 116、B→C 5；C→B 6、C→C 20、C→D-a 1、C→D-b 1；D→A 1、D→C 5、D→D-a 3。首次批跑中的会话错误经单页隔离分别补足两次，详情见临时 JSON `/tmp/toolbox-audit-653-batch01-{a,b}.json`、`/tmp/toolbox-audit-batch01-isolated.json`、`/tmp/toolbox-audit-run-batch01-isolated-b.json`、`/tmp/toolbox-audit-run-batch0{3,4}-*.json`；这些临时文件不是永久交付物。
- 探针盲区确认：隐藏 file input 被可见性过滤漏计，`audio/audio-cut` D-b 因而不能判为无交互；未加载音频，不判实际文件驱动桶位。初始隐藏标签控件也会漏采，`health/rehab-timer` 的 `month` 控件即使打开，探针通用文本值被浏览器拒绝。`grew` 包含列表文字变化而非仅行数增长，`agriculture/cycle-honey` 输出“列表 5→5”不表示行数增长；Chrome 输入名称、位置、周期 10 天、日期 2026-11-06 后点击添加，列表及本地存储确实出现蜂箱。
- 针对性错分复核：`design/contrast-checker` 文本色值 `#1F2937`→`#000000` 时对比度 14.68→21.00，无需点击，应 B 而非探针 C；同理 `color-palette`、`colorblind-simulator`、`css-box-shadow-generator`、`glassmorphism-generator`、`neomorphism-generator` 输入合法 `#1199cc` 后，色卡/模拟色或 CSS 立即改变，均应 B 而非 C。源因为通用文本值非合法色值。这是针对性而非随机样本，不能外推错分率。
- 其他补证：`advertising/generator-time` 数量 5→2→7，分镜数同步 5→2→7，支持 B；`data/data-cleaner` 文本改值不更新，点击清洗才变，支持 A。上述 Chrome DOM 操作及独立浏览器测试不能表述为全部 60 页人工裁决。
- 第 5 批（按路径排序第 161–200 页）已完成两次探针：各 40 页、错误 0、逐页桶位一致；B 27、C 10、D-a 2、A 1。累计前 200 页双跑有效：B 151、C 40、D-a 6、D-b 1、A 2；剩余 453 页等待双跑。结果分别在 `/tmp/toolbox-audit-run-batch05-{a,b}.json`，仅作为本地中间证据。
- 第 6、7 批（第 201–280 页）在停止浏览器前均已双跑完成，各次 40 页且 0 错，路径集合与桶位逐页一致：第 6 批 B 40；第 7 批 B 37、C 1、D-a 2。合计前 280 页：B 228、C 41、D-a 8、D-b 1、A 2。第 8 批第一遍 38 页有效、另 2 页隔离重试有效，第二遍中止，故该批不计双跑完成。
- `edu/english-vocabulary` 探针 A 桶仅代表改动题数不会实时答题：源码 `startQuiz()` 才创建题目，`answer()` 处理选择、计分并延时进入下一题。该工具本就需要先开始再选择，静态证据不能推断浏览器实际交互或作为独立真值抽样。
- 用户要求加速并只分析代码，已停止浏览器、后台探针及本地服务。余下 373 页未双跑，653 页完整迁移矩阵、独立 60 页运行态抽样和错分率未完成，旧分桶仍不能销账；后续静态复核只能标代码结论或待验证，不冒称真实浏览器验证。业务缺陷继续写入 `plan/categories/` 对应分类。
- 静态续审首批：人工复核 `health/{pregnancy-due-date,ovulation-calculator,gfr-calculator,blood-pressure-classifier}` 4 页的输入事件、计算和结果路径；记录胎重、单位与分期、日历未知日期、安全输入和旧结果等问题，详见 `categories/03-医疗健康/specialties.md`。另更正 `units-datetime-family.md` 中两页日期解析的过时记录。代码复算非浏览器实测，不能计入双跑或错分率。
- 静态续审第二批：阅读 `gardening2/{fertilizer-ppm,watering-frequency}`、`geology/{mineral-hardness,richter-scale,rock-identify,stratum-correlation}`、`fun/{keyboard-heatmap,typing-rhythm}` 的主要交互及结果路径，共 8 页。记录浇水量默认值与打字 WPM 算式问题，复核并更正已过时的地震条目；不能将未发现其他问题等同运行通过。
- 静态续审第三批：阅读 `health/{child-bmi-calculator,child-height-predictor,body-surface-area,cholesterol-ratio,calorie-needs}` 5 页主要输入及计算结果路径，记录身高参考公式不连续、清空后子结果残留、单位切换和选填输入用途问题，详见医疗分类。医疗结论仅代码确认，专业性须复核。
- 静态续审第四批：阅读 `health/{alcohol-units,blood-sugar-converter,caffeine-limit,fracture-healing,ibw-calculator,protein-needs}` 6 页主要路径，记录酒精浓度单位量级、饮品累计、默认值和陈旧结果等问题，详见医疗分类。未运行页面、未验证临床标准，不计双跑。
- 静态续审第五批：阅读 `health/{insulin-dose,one-rep-max,sleep-cycle-calculator,smoking-cost-calculator,waist-hip-ratio,water-intake-calculator}` 6 页主要路径，复核既有胰岛素问题并记录训练重量、寿命换算、午夜与空态问题。仅源码及算式复算，详见医疗、运动分类，不计双跑。


- 扫描时间：2026/11/5 05:04:33
- 覆盖工具页：**4807**
- 有输入控件的页：**4401**
- 无输入控件（纯展示/参考卡，跳过）：**406**
- 有输入但无主按钮（实时计算/表单提交，不计缺陷）：**653** → **2026-11-05 重算后作废**：A 真需点击 23 / B 已可改值 449 / C 误判 113（纯select 97+文件 10+画布 6）/ D 无文本输入 68（D-a 67+D-b 1）。逐页清单见 `/private/tmp/notclicked-653-classified.json`，旧 not-clicked 清单不得再作为派工依据。
- 空态三档（本版已按新口径重扫 **4401** 页）：真空态 `text_empty_no_select` **2422**｜select 默认态 `text_empty_sel_default` **1717**｜控件回读失真 `true_distortion` **262**；其余 **0** 页仍是旧口径记录，待全量重扫后归位
- 命中至少一类问题：**216**

> 口径：① 有效性＝先填值→记录快照→**改一个输入为明显不同的合法值**→再点主按钮→比较前后快照（排除「加载时已自动算过一次」的假阴性）；② 空态＝清空所有输入后点主按钮，结果区给出 NaN/Infinity/undefined/null/0/空串或结论即为缺陷；③ 死控件＝控件 id 在全部 `<script>` 中从未出现（且页面无 `querySelectorAll('input')` / `FormData` 这类泛化读取，内联 oninput 绑定的不计）。快照优先取 `#result/#output/.result*` 等结果容器，无则回退整页正文（剔除控件内的当前值）。

## 总览（按类型）

| 类型 | 页数 | 严重度 |
|---|---|---|
| select 默认态输出全 0 且无提示（非真空态，可疑需人工复核） | **67** | 低 |
| 改了输入再点主按钮，输出快照不变（低置信度线索，需人工复验） | **57** | 低 |
| 空输入直接给出 NaN/Infinity/undefined/null/0 | **31** | 高 |
| 重置按钮未改变任何输入 | **31** | 低 |
| 空输入直接给出结论（优秀/正常/合格…） | **30** | 中 |
| 点击主按钮抛异常（含 console 报错） | **1** | 高 |
| 导出/下载按钮 onclick 目标函数不存在（必死） | **1** | 中 |
| 死控件（静态） | **1** 页 / 2 个控件 | 低-中 |

> **置信度分层**：高/中置信度缺陷页 **161** 页（点击抛异常、空态坏值/结论、死按钮、死控件）；`no_effect` **57** 页已改用「0.8× 相对量级变异」主探针，并在无变化时追加「5× 放大探针」——放大后仍无变化才保留本类，放大后才变化的 **128** 页归入 `probe_masked`（显示精度/分档阈值掩蔽，不计缺陷）。剩余 `no_effect` 页的逐页三档结论（真无效 / 阈值掩蔽 / 探针失真）见 `plan/no-effect-recheck.md`。

### 精度/阈值掩蔽：探针被结果区小数位抹平（128 页，不计缺陷）

> 判定：主探针 0.8× 默认值后结果区无变化，但同一控件放大到 5× 后结果变化。说明页面计算链路正常，只是 20% 量级差在 `toFixed(2)`/整数输出下不可见。

- `tools/acupuncture/pediatric-tuina.html` — 主探针 month [number] "2" → "1.6"｜结果最大小数位 2｜放大探针 month [number] "1.6" → "45"; constitution [select] "normal" → "strong"…
- `tools/advertising/ad-size.html` — 主探针 width [number] "2" → "1.6"｜结果最大小数位 1｜放大探针 width [number] "1.6" → "45"; height [number] "2" → "47"; fromUnit [sel…
- `tools/advertising/assessor-52.html` — 主探针 budget [number] "50000" → "40000"｜结果最大小数位 2｜放大探针 budget [number] "40000" → "200037"; venueCost [number] "15000" → "7503…
- `tools/advertising/assessor-55.html` — 主探针 targetPop [number] "500" → "400"｜结果最大小数位 1｜放大探针 targetPop [number] "400" → "2037"; spots [number] "60" → "337"; rating…
- `tools/agriculture/crop-yield.html` — 主探针 spikes [number] "2" → "1.6"｜结果最大小数位 2｜放大探针 spikes [number] "1.6" → "45"; grains [number] "2" → "47"; weight [numb…
- `tools/agriculture/fertilizer-calculator.html` — 主探针 area [number] "0.2" → "0.16000000000000003"｜结果最大小数位 0｜放大探针 area [number] "0.16000000000000003" → "37.8"; yield [number] "100" → "…
- `tools/agriculture/storage-pest-alert.html` — 主探针 temp [number] "20" → "16"｜结果最大小数位 1｜放大探针 temp [number] "16" → "60"; humidity [number] "50" → "100"; grainMoistu…
- `tools/ai/best-epoch.html` — 主探针 l1 [number] "0.5" → "0.4"｜结果最大小数位 4｜放大探针 l1 [number] "0.4" → "39"; l2 [number] "0.4" → "39"; l3 [number] "0.45"…
- `tools/astronomy/crater-estimator.html` — 主探针 diameter [number] "0.002" → "0.0016"｜结果最大小数位 0｜放大探针 diameter [number] "0.0016" → "37.008"; density [number] "2" → "47"; ve…
- `tools/automotive/fuel-anomaly.html` — 主探针 number [number] "0" → "1"｜结果最大小数位 2｜放大探针 number [number] "1" → "42"; number [number] "42" → "247"; number [numb…
- `tools/biz/char-frequency.html` — 主探针 topN [number] "250.5" → "200.4"｜结果最大小数位 2｜放大探针 topN [number] "200.4" → "500"; input [textarea] "abc 123" → "probe-alp…
- `tools/cardiology/nt-probnp.html` — 主探针 age [number] "72" → "57.6"｜结果最大小数位 0｜放大探针 age [number] "57.6" → "325"; ntprobnp [number] "1850" → "9287"
- `tools/ceramics/glaze-ratio.html` — 主探针 totalW [number] "1" → "1"｜结果最大小数位 1｜放大探针 totalW [number] "1" → "42"; number [number] "50" → "100"; number [numb…
- `tools/cleaning/supply-usage.html` — 主探针 area [number] "1" → "1"｜结果最大小数位 1｜放大探针 area [number] "1" → "42"; period [number] "183" → "365"; safety [numbe…
- `tools/clinical-lab/csf-analysis.html` — 主探针 pressure [number] "150" → "120"｜结果最大小数位 2｜放大探针 pressure [number] "120" → "637"; wbc [number] "10" → "87"; poly [numbe…
- `tools/construction/blueprint-tool.html` — 主探针 customScale [number] "1" → "1"｜结果最大小数位 4｜放大探针 customScale [number] "1" → "42"; distance [number] "100" → "537"; dire…
- `tools/construction/concrete-calculator.html` — 主探针 loss [number] "8" → "6.4"｜结果最大小数位 2｜放大探针 loss [number] "6.4" → "15"; length [number] "0.2" → "38"; width [numbe…
- `tools/dance/choreography-timeline.html` — 主探针 bpm [number] "140" → "112"｜结果最大小数位 0｜放大探针 bpm [number] "112" → "240"; segCount [number] "9" → "16"; barsPerSeg […
- `tools/decor/scheduler.html` — 主探针 number [number] "3" → "2.4000000000000004"｜结果最大小数位 0｜放大探针 number [number] "2.4000000000000004" → "49"; number [number] "7" → "72…
- `tools/dentistry/dental-arch-development.html` — 主探针 age [number] "8" → "6.4"｜结果最大小数位 0｜放大探针 age [number] "6.4" → "69"; ucWidth [number] "28" → "177"; lcWidth [num…
- `tools/dermatology/calc-1.html` — 主探针 age [number] "60" → "48"｜结果最大小数位 1｜放大探针 age [number] "48" → "120"; weight [number] "100.5" → "200"; head [numb…
- `tools/design/analysis-64.html` — 主探针 p1a [number] "50" → "40"｜结果最大小数位 3｜放大探针 p1a [number] "40" → "100"; p1b [number] "50" → "100"; p2a [number] "50…
- `tools/design/color-picker.html` — 主探针 hInput [number] "154" → "123.2"｜结果最大小数位 0｜放大探针 hInput [number] "338" → "360"; sInput [number] "72" → "100"; lInput [n…
- `tools/design/initials-avatar.html` — 主探针 size [number] "166" → "132.8"｜结果最大小数位 2｜放大探针 size [number] "132.8" → "300"; radius [number] "100" → "200"; fontSize…
- `tools/ecommerce/analysis-cost-8.html` — 主探针 fc [number] "60000" → "48000"｜结果最大小数位 0｜放大探针 fc [number] "48000" → "240037"; vc [number] "30" → "187"; price [numbe…
- `tools/edu/generator-4.html` — 主探针 cnt [number] "25.5" → "20.400000000000002"｜结果最大小数位 2｜放大探针 cnt [number] "20.400000000000002" → "50"; srcText [textarea] "abc 123"…
- `tools/electrical/voltage-drop.html` — 主探针 power [number] "0.01" → "0.01"｜结果最大小数位 4｜放大探针 power [number] "0.01" → "37.05"; length [number] "2" → "47"; cosPhi [n…
- `tools/electronics/smt-stencil.html` — 主探针 padW [number] "0.5" → "0.4"｜结果最大小数位 5｜放大探针 padW [number] "0.4" → "39"; padL [number] "2" → "47"; reduce [number] …
- `tools/encode/encode-6.html` — 主探针 value [number] "255" → "204"｜结果最大小数位 0｜放大探针 value [number] "204" → "1057"; base [number] "16" → "117"
- `tools/encode/radix-digits.html` — 主探针 N [number] "256" → "204.8"｜结果最大小数位 0｜放大探针 N [number] "204.8" → "1061"; base [number] "16" → "117"; bytes [number…
- `tools/endocrinology/catecholamine-test.html` — 主探针 mn [number] "0.8" → "0.6400000000000001"｜结果最大小数位 2｜放大探针 mn [number] "0.6400000000000001" → "40.2"; nmn [number] "2.1" → "47.5"…
- `tools/endocrinology/gh-stimulation-test.html` — 主探针 age [number] "8" → "6.4"｜结果最大小数位 3｜放大探针 age [number] "6.4" → "69"; sds [number] "-2.8000000000000003" → "23"; …
- `tools/endocrinology/pituitary-tumor.html` — 主探针 diameter [number] "8" → "6.4"｜结果最大小数位 0｜放大探针 diameter [number] "6.4" → "69"; invasive [select] "0" → "1"
- `tools/endocrinology/thyroid-cancer-risk.html` — 主探针 tumorSize [number] "2.5" → "2"｜结果最大小数位 1｜放大探针 tumorSize [number] "2" → "47"; tg [number] "2.5" → "49.5"; pathology […
- `tools/finance/word-frequency.html` — 主探针 topN [number] "250.5" → "200.4"｜结果最大小数位 2｜放大探针 topN [number] "200.4" → "500"; minLen [number] "5.5" → "10"; input [te…
- `tools/fire-rescue/calc-4.html` — 主探针 area [number] "0.1" → "0.1"｜结果最大小数位 1｜放大探针 area [number] "0.1" → "37.5"; fireClass [select] "A" → "C"; level [sel…
- `tools/fire-rescue/confined-space-rescue.html` — 主探针 o2 [number] "15" → "12"｜结果最大小数位 0｜放大探针 o2 [number] "12" → "30"; lel [number] "50" → "100"; h2s [number] "0" →…
- `tools/fire-rescue/fire-risk-assessment.html` — 主探针 height [number] "24" → "19.200000000000003"｜结果最大小数位 2｜放大探针 height [number] "19.200000000000003" → "133"; area [number] "5000" → "…
- `tools/fire-rescue/rescue-route.html` — 主探针 floors [number] "10" → "8"｜结果最大小数位 0｜放大探针 floors [number] "8" → "77"; entrances [number] "2" → "47"; roadWidth […
- `tools/fishery/feed-protein-fat.html` — 主探针 temp [number] "25" → "20"｜结果最大小数位 2｜放大探针 temp [number] "20" → "137"; species [select] "warm" → "shrimp"; stage …
- `tools/fishery/harvest-size-price.html` — 主探针 number [number] "12" → "9.600000000000001"｜结果最大小数位 1｜放大探针 number [number] "9.600000000000001" → "85"; number [number] "12" → "97…
- `tools/fishery/oxygen-machine.html` — 主探针 volume [number] "1" → "1"｜结果最大小数位 3｜放大探针 volume [number] "1" → "42"; biomass [number] "500" → "2537"; temp [num…
- `tools/fitness/detector-15.html` — 主探针 sitHours [number] "8" → "6.4"｜结果最大小数位 0｜放大探针 sitHours [number] "6.4" → "69"; t1 [select] "0" → "3"; t2 [select] "0"…
- `tools/food-processing/filling-volume.html` — 主探针 dia [number] "0.2" → "0.16000000000000003"｜结果最大小数位 3｜放大探针 dia [number] "0.16000000000000003" → "37.8"; h [number] "0.2" → "38"
- `tools/food-processing/filtration-rate.html` — 主探针 A [number] "0.001" → "0.001"｜结果最大小数位 0｜放大探针 A [number] "0.001" → "37.005"; dP [number] "100" → "537"; mu [number] …
- `tools/food-processing/freeze-thaw-loss.html` — 主探针 w0 [number] "500" → "400"｜结果最大小数位 2｜放大探针 w0 [number] "400" → "2037"; w1 [number] "475" → "2412"; cycles [number…
- `tools/food-processing/homogenization-pressure.html` — 主探针 P0 [number] "0.1" → "0.1"｜结果最大小数位 3｜放大探针 P0 [number] "0.1" → "37.5"; d0 [number] "0.02" → "37.1"; P [number] "0…
- `tools/food-processing/quick-freeze-time.html` — 主探针 d [number] "0.2" → "0.16000000000000003"｜结果最大小数位 1｜放大探针 d [number] "0.16000000000000003" → "37.8"; Tf [number] "-1.5" → "29.5"…
- `tools/food-processing/residual-oxygen.html` — 主探针 vol [number] "500" → "400"｜结果最大小数位 2｜放大探针 vol [number] "400" → "2037"; pvol [number] "400" → "2037"; o2init [num…
- `tools/food-testing/colony-count.html` — 主探针 d1p1 [number] "156" → "124.80000000000001"｜结果最大小数位 0｜放大探针 d1p1 [number] "124.80000000000001" → "661"; d1p2 [number] "168" → "877…
- `tools/food-testing/nutrition-label-nrv.html` — 主探针 servingSize [number] "100" → "80"｜结果最大小数位 0｜放大探针 servingSize [number] "80" → "437"; energy [number] "800" → "4037"; pro…
- `tools/food/oil-absorption-estimator.html` — 主探针 weight [number] "1" → "1"｜结果最大小数位 1｜放大探针 weight [number] "1" → "42"; time [number] "1" → "42"; temp [number] "1…
- `tools/forensic-medicine/bone-age-estimation.html` — 主探针 femurLen [number] "50" → "40"｜结果最大小数位 0｜放大探针 femurLen [number] "40" → "237"; crl [number] "120" → "637"; gender [se…
- `tools/gardening/pot-capacity.html` — 主探针 diameter [number] "0.2" → "0.16000000000000003"｜结果最大小数位 2｜放大探针 diameter [number] "0.16000000000000003" → "37.8"; height [number] "0.2…
- `tools/gastroenterology/detector-7.html` — 主探针 prior [number] "0" → "1"｜结果最大小数位 0｜放大探针 prior [number] "1" → "42"; ab1 [select] "0" → "1"; ab2 [select] "0" → …
- `tools/gastroenterology/ercp-success.html` — 主探针 stoneSize [number] "50.5" → "40.400000000000006"｜结果最大小数位 2｜放大探针 stoneSize [number] "40.400000000000006" → "100"; stoneCount [select] "…
- `tools/gastroenterology/glasgow-pancreatitis.html` — 主探针 age [number] "55" → "44"｜结果最大小数位 2｜放大探针 age [number] "44" → "257"; wbc [number] "15" → "112"; glucose [number]…
- `tools/glass/thickness-selection.html` — 主探针 width [number] "100" → "80"｜结果最大小数位 2｜放大探针 width [number] "80" → "437"; height [number] "100" → "537"; scene [sel…
- `tools/healthcare/apgar.html` — 主探针 appearance [number] "2" → "1.6"｜结果最大小数位 0｜放大探针 appearance [number] "1.6" → "45"; pulse [number] "2" → "47"; grimace […
- `tools/healthcare/tdee-calculator.html` — 主探针 age [number] "30" → "24"｜结果最大小数位 3｜放大探针 age [number] "24" → "157"; height [number] "170" → "887"; weight [numb…
- `tools/hematology/cml-monitoring.html` — 主探针 months [number] "12" → "9.600000000000001"｜结果最大小数位 1｜放大探针 months [number] "9.600000000000001" → "85"; bcrabl [number] "0.5" → "3…
- `tools/hematology/detector-5.html` — 主探针 granCD59 [number] "35" → "28"｜结果最大小数位 1｜放大探针 granCD59 [number] "28" → "177"; granCD55 [number] "32" → "197"; rbcCD5…
- `tools/hematology/m-protein.html` — 主探针 tp [number] "75" → "60"｜结果最大小数位 2｜放大探针 tp [number] "60" → "337"; albumin [number] "35" → "212"; mprotein [num…
- `tools/hematology/ipss-r.html` — 主探针 blasts [number] "5" → "4"｜结果最大小数位 2｜放大探针 blasts [number] "4" → "57"; hgb [number] "85" → "462"; anc [number] "0…
- `tools/hematology/mpn-scoring.html` — 主探针 age [number] "65" → "52"｜结果最大小数位 0｜放大探针 age [number] "52" → "297"; hgb [number] "95" → "512"; wbc [number] "15…
- `tools/hematology/thrombin-generation.html` — 主探针 lagTime [number] "3" → "2.4000000000000004"｜结果最大小数位 0｜放大探针 lagTime [number] "2.4000000000000004" → "49"; peak [number] "180" → "9…
- `tools/hematology/rater-risk-1.html` — 主探针 pltBefore [number] "180" → "144"｜结果最大小数位 0｜放大探针 pltBefore [number] "144" → "757"; pltNadir [number] "15" → "112"; onse…
- `tools/hematology/transfusion-dose.html` — 主探针 pWeight [number] "70" → "56"｜结果最大小数位 0｜放大探针 pWeight [number] "56" → "317"; pCurrentHgb [number] "60" → "337"; pTar…
- `tools/home/paint-calculator.html` — 主探针 surface-area [number] "12" → "9.600000000000001"｜结果最大小数位 2｜放大探针 surface-area [number] "9.600000000000001" → "85"; coats [number] "3" →…
- `tools/hr/analysis-29.html` — 主探针 begin [number] "1" → "1"｜结果最大小数位 4｜放大探针 begin [number] "1" → "42"; head [number] "1" → "42"; left [number] "15…
- `tools/hr/overtime-pay-calc.html` — 主探针 hourly [number] "25" → "20"｜结果最大小数位 2｜放大探针 hourly [number] "20" → "137"; weekday [number] "0" → "49"; weekend [nu…
- `tools/hr/performance-score.html` — 主探针 excellentPct [number] "50" → "40"｜结果最大小数位 3｜放大探针 excellentPct [number] "40" → "100"; failPct [number] "50" → "100"; num…
- `tools/hr/social-insurance.html` — 主探针 salary [number] "10000" → "8000"｜结果最大小数位 17｜放大探针 salary [number] "8000" → "40037"; base [number] "10000" → "50037"; num…
- `tools/hydraulic/flow-velocity.html` — 主探针 inR [number] "0.001" → "0.001"｜结果最大小数位 4｜放大探针 inR [number] "0.001" → "37.005"; inN [number] "0.002" → "37.01"; inJ […
- `tools/hydraulic/spillway-calc.html` — 主探针 inL [number] "0.1" → "0.1"｜结果最大小数位 4｜放大探针 inL [number] "0.1" → "37.5"; inH [number] "0.01" → "37.05"; inM [numbe…
- `tools/it/crc-calculator.html` — 主探针 cw [number] "40" → "32"｜结果最大小数位 1｜放大探针 cw [number] "32" → "64"; input [textarea] "48656c6c6f" → "48656c6c6f21…
- `tools/it/keyword-density.html` — 主探针 minLen [number] "10.5" → "8.4"｜结果最大小数位 2｜放大探针 minLen [number] "8.4" → "20"; inputText [textarea] "abc 123" → "probe-…
- `tools/it/random-string.html` — 主探针 len [number] "16" → "12.8"｜结果最大小数位 0｜放大探针 len [number] "12.8" → "101"; cnt [number] "5" → "62"
- `tools/jewelry/diamond-carat.html` — 主探针 d [number] "0.2" → "0.16000000000000003"｜结果最大小数位 3｜放大探针 d [number] "0.16000000000000003" → "37.8"; w [number] "0" → "49"; h [n…
- `tools/kids/focus-timer.html` — 主探针 focusMin [number] "25" → "20"｜结果最大小数位 0｜放大探针 focusMin [number] "20" → "45"; restMin [number] "10.5" → "20"; goalCou…
- `tools/legal/personal-injury.html` — 主探针 age [number] "35" → "28"｜结果最大小数位 0｜放大探针 age [number] "28" → "177"; income [number] "50000" → "250037"; avgWage…
- `tools/legal/social-security-base.html` — 主探针 salary [number] "12" → "9.600000000000001"｜结果最大小数位 2｜放大探针 salary [number] "9.600000000000001" → "85"; city [select] "北京" → "广州";…
- `tools/library/stats-report.html` — 主探针 colTotal [number] "1" → "1"｜结果最大小数位 0｜放大探针 colTotal [number] "1" → "42"; loanCnt [number] "96000" → "480037"; rea…
- `tools/life/generator-random-1.html` — 主探针 min [number] "1" → "0.8"｜结果最大小数位 0｜放大探针 min [number] "0.8" → "41"; max [number] "100" → "537"; cnt [number] "2…
- `tools/livestock/analysis-18.html` — 主探针 hens [number] "1" → "1"｜结果最大小数位 2｜放大探针 hens [number] "1" → "42"; days [number] "2" → "47"; eggs [number] "630…
- `tools/livestock/calving-interval.html` — 主探针 daysToFirstBreed [number] "75" → "60"｜结果最大小数位 0｜放大探针 daysToFirstBreed [number] "60" → "337"; breedTimes [number] "2" → "47"…
- `tools/logistics/detector-30.html` — 主探针 temp [number] "4" → "3.2"｜结果最大小数位 1｜放大探针 temp [number] "3.2" → "53"; hours [number] "24" → "157"; appearance [n…
- `tools/logistics2/loading-utilization.html` — 主探针 truckL [number] "0.2" → "0.16000000000000003"｜结果最大小数位 3｜放大探针 truckL [number] "0.16000000000000003" → "37.8"; truckW [number] "0.2" …
- `tools/martial/stance-center.html` — 主探针 stepWidth [number] "110" → "88"｜结果最大小数位 2｜放大探针 stepWidth [number] "88" → "200"; height [number] "170" → "220"; frontR…
- `tools/math/magic-square.html` — 主探针 order [number] "3" → "3"｜结果最大小数位 0｜放大探针 order [number] "3" → "15"
- `tools/medical/medical-calculator.html` — 主探针 dose_weight [number] "2" → "1.6"｜结果最大小数位 1｜放大探针 dose_weight [number] "1.6" → "45"; dose_per_kg [number] "0.01" → "37.0…
- `tools/medical2/bed-occupancy.html` — 主探针 beds [number] "2" → "1.6"｜结果最大小数位 2｜放大探针 beds [number] "1.6" → "45"; openBeds [number] "2" → "47"; days [number…
- `tools/metallurgy/analysis-grade.html` — 主探针 qOre [number] "0.1" → "0.1"｜结果最大小数位 3｜放大探针 qOre [number] "0.1" → "37.5"; gradeOre [number] "0.85" → "41.25"; grad…
- `tools/metalwork/detector-21.html` — 主探针 thickness [number] "20" → "16"｜结果最大小数位 0｜放大探针 thickness [number] "16" → "117"; material [select] "ferro" → "weld"; d…
- `tools/metalwork/surface-finish.html` — 主探针 inVal [number] "0.002" → "0.0016"｜结果最大小数位 3｜放大探针 inVal [number] "0.0016" → "37.008"; inType [select] "ra" → "rz"
- `tools/music/bpm-converter.html` — 主探针 bpmInput [number] "170" → "136"｜结果最大小数位 2｜放大探针 bpmInput [number] "136" → "300"; reverseMs [number] "2" → "47"; sample…
- `tools/nephrology/aki-kdigo.html` — 主探针 baselineScr [number] "80" → "64"｜结果最大小数位 0｜放大探针 baselineScr [number] "64" → "357"; currentScr [number] "180" → "937"; …
- `tools/nutrition/calc-2.html` — 主探针 foodWeight [number] "100" → "80"｜结果最大小数位 1｜放大探针 foodWeight [number] "80" → "437"; manualCarb [number] "0" → "49"; manu…
- `tools/obstetrics/ovarian-reserve.html` — 主探针 amh [number] "2.5" → "2"｜结果最大小数位 2｜放大探针 amh [number] "2" → "47"; fsh [number] "6" → "67"; e2 [number] "35" → "…
- `tools/obstetrics/taipanchengshudu-grannumfenji.html` — 主探针 gaWeek [number] "28" → "22.400000000000002"｜结果最大小数位 0｜放大探针 gaWeek [number] "22.400000000000002" → "45"; chorion [select] "0" → "2…
- `tools/pediatrics/assessor-13.html` — 主探针 ageMonth [number] "24" → "19.200000000000003"｜结果最大小数位 0｜放大探针 ageMonth [number] "19.200000000000003" → "133"; weight [number] "12" →…
- `tools/pediatrics/assessor-spo2.html` — 主探针 ageDay [number] "2" → "1.6"｜结果最大小数位 0｜放大探针 ageDay [number] "1.6" → "45"; rhSpO2 [number] "50" → "100"; footSpO2 […
- `tools/pediatrics/chd-assessment.html` — 主探针 age [number] "2" → "1.6"｜结果最大小数位 2｜放大探针 age [number] "1.6" → "45"; rhSpo2 [number] "97" → "522"; llSpo2 [numbe…
- `tools/pediatrics/hfmd-course.html` — 主探针 age [number] "108" → "86.4"｜结果最大小数位 1｜放大探针 age [number] "86.4" → "216"; day [number] "15" → "30"; temp [number] "…
- `tools/pet/checker-diagnosis.html` — 主探针 age [number] "3" → "2.4000000000000004"｜结果最大小数位 2｜放大探针 age [number] "2.4000000000000004" → "49"; temp [number] "38.5" → "229.…
- `tools/rehabilitation/nine-hole-peg.html` — 主探针 domTime [number] "18.5" → "14.8"｜结果最大小数位 1｜放大探针 domTime [number] "14.8" → "111"; nonDomTime [number] "20.3" → "138.5";…
- `tools/rehabilitation/proprioception-error.html` — 主探针 target1 [number] "45" → "36"｜结果最大小数位 1｜放大探针 target1 [number] "36" → "217"; reproduce1 [number] "12" → "97"; target…
- `tools/rehabilitation/stretch-duration.html` — 主探针 holdTime [number] "30" → "24"｜结果最大小数位 0｜放大探针 holdTime [number] "24" → "157"; reps [number] "3" → "52"; dailySession…
- `tools/reproductive-medicine/icsi-success.html` — 主探针 mii [number] "10" → "8"｜结果最大小数位 1｜放大探针 mii [number] "8" → "77"; injected [number] "10" → "87"; survived [numb…
- `tools/reproductive-medicine/pgt-indication.html` — 主探针 ageVal [number] "35" → "28"｜结果最大小数位 0｜放大探针 ageVal [number] "28" → "177"; rplVal [number] "0" → "49"
- `tools/road/pavement-design.html` — 主探针 inW18 [number] "1" → "1"｜结果最大小数位 3｜放大探针 inW18 [number] "1" → "42"; inMR [number] "10" → "87"; inD1 [number] "4…
- `tools/sports/rater-motion.html` — 主探针 n [number] "11" → "8.8"｜结果最大小数位 3｜放大探针 n [number] "8.8" → "20"; r1 [number] "499.5" → "999"; r2 [number] "499…
- `tools/tcm-chemistry/concentration-calc.html` — 主探针 targetTemp [number] "50" → "40"｜结果最大小数位 1｜放大探针 targetTemp [number] "40" → "237"; vacuum [number] "12" → "97"; atm [nu…
- `tools/tcm-chemistry/content-assay.html` — 主探针 stdMass [number] "10" → "8"｜结果最大小数位 4｜放大探针 stdMass [number] "8" → "77"; stdConc [number] "0.5" → "39.5"; isMass […
- `tools/telecom/bandwidth-calculator.html` — 主探针 bandwidth [number] "0.1" → "0.1"｜结果最大小数位 2｜放大探针 bandwidth [number] "0.1" → "37.5"; fileSize [number] "0.001" → "37.005…
- `tools/telecom/path-loss.html` — 主探针 freq [number] "0.001" → "0.001"｜结果最大小数位 2｜放大探针 freq [number] "0.001" → "37.005"; dist [number] "0.001" → "37.005"; pt…
- `tools/textile/pattern-calculator.html` — 主探针 fabricWidth [number] "100" → "80"｜结果最大小数位 1｜放大探针 fabricWidth [number] "80" → "437"; fabricLength [number] "100" → "537"…
- `tools/urban/parking-ratio.html` — 主探针 inArea [number] "1" → "1"｜结果最大小数位 2｜放大探针 inArea [number] "1" → "42"; inRatio [number] "1" → "42"; inVisitor [nu…
- `tools/urban/green-ratio.html` — 主探针 inTotal [number] "1" → "1"｜结果最大小数位 2｜放大探针 inTotal [number] "1" → "42"; inGreen [number] "17500" → "87537"; inCan…
- `tools/urban/land-use.html` — 主探针 inPop [number] "100" → "100"｜结果最大小数位 3｜放大探针 inPop [number] "100" → "537"; area_R [number] "300" → "1537"; area_A […
- `tools/urban/population-density.html` — 主探针 inPop [number] "1" → "1"｜结果最大小数位 3｜放大探针 inPop [number] "1" → "42"; inArea [number] "0.1" → "37.5"; inResArea […
- `tools/urology/urine-flow-rate.html` — 主探针 age [number] "60" → "48"｜结果最大小数位 1｜放大探针 age [number] "48" → "277"; qmax [number] "18" → "127"; vol [number] "2…
- `tools/usedcar/checker-3.html` — 主探针 mileage [number] "8" → "6.4"｜结果最大小数位 0｜放大探针 mileage [number] "6.4" → "69"; carAge [number] "5" → "62"; ck_frame [s…
- `tools/usedcar/rater-37.html` — 主探针 mileage [number] "10" → "8"｜结果最大小数位 0｜放大探针 mileage [number] "8" → "77"; engineSize [number] "1.6" → "45"; ck_star…
- `tools/usedcar/tester-12.html` — 主探针 batteryV [number] "12.4" → "9.920000000000002"｜结果最大小数位 0｜放大探针 batteryV [number] "9.920000000000002" → "86.60000000000001"; chargingV…
- `tools/video/video-converter.html` — 主探针 duration [number] "0.1" → "0.1"｜结果最大小数位 2｜放大探针 duration [number] "0.1" → "37.5"; platform [select] "youtube" → "douyi…
- `tools/video/video-compressor.html` — 主探针 duration [number] "0.1" → "0.1"｜结果最大小数位 0｜放大探针 duration [number] "0.1" → "37.5"; targetSize [number] "2" → "47"; reso…
- `tools/welding/analysis-38.html` — 主探针 cur [number] "1" → "1"｜结果最大小数位 3｜放大探针 cur [number] "1" → "42"; volt [number] "2" → "47"; spd [number] "0.1" …

## 按行业分布（便于分派修复线）

| 类型 | 集中行业（页数） |
|---|---|
| select 默认态输出全 0 且无提示（非真空态，可疑需人工复核） | tools/it/ 10、tools/realestate/ 5、tools/forensic-medicine/ 4、tools/gastroenterology/ 4、tools/edu/ 3、tools/energy/ 2、tools/finance/ 2、tools/fire-rescue/ 2 |
| 改了输入再点主按钮，输出快照不变（低置信度线索，需人工复验） | tools/it/ 13、tools/design/ 3、tools/hematology/ 3、tools/chinese/ 2、tools/food-processing/ 2、tools/forensic-medicine/ 2、tools/image/ 2、tools/life/ 2 |
| 空输入直接给出 NaN/Infinity/undefined/null/0 | tools/eco/ 18、tools/investment/ 4、tools/insurance/ 3、tools/agriculture/ 1、tools/design/ 1、tools/encode/ 1、tools/fishery/ 1、tools/hr/ 1 |
| 重置按钮未改变任何输入 | tools/rheumatology/ 4、tools/it/ 3、tools/rehabilitation/ 3、tools/elderly/ 2、tools/general/ 2、tools/hematology/ 2、tools/audio/ 1、tools/biz/ 1 |
| 空输入直接给出结论（优秀/正常/合格…） | tools/ent/ 3、tools/leather/ 3、tools/agriculture/ 2、tools/biz/ 2、tools/eco/ 2、tools/electronics/ 2、tools/energy/ 2、tools/healthcare/ 2 |
| 点击主按钮抛异常（含 console 报错） | tools/data/ 1 |
| 导出/下载按钮 onclick 目标函数不存在（必死） | tools/it/ 1 |

## Top 50 高影响页面（按严重度加权）

| # | 页面 | 得分 | 类型 | 证据 |
|---|---|---|---|---|
| 1 | `tools/data/data-visualizer.html` | 3 | click_error | 按钮「📈 渲染」｜click: Invalid array length @ drawHistogram (/tools/data/data-visualizer.html:299:18) |
| 2 | `tools/agriculture/agri-calculator.html` | 2.6 | empty_bogus | 空输入点「计算配比」（text_empty_no_select）→ 结果区 氮 (N)0.00kg磷 (P₂O₅)0.00kg钾 (K₂O)0.00kg配方比例：0-0-0施肥面积：0 亩每亩用量：0… |
| 3 | `tools/design/px-to-rem.html` | 2.6 | empty_bogus | 空输入点「计算」（text_empty_no_select）→ 结果区 转换结果 ⏐ 0px = 0.0000rem ⏐ 📋 复制结果⬇️ 导出 TXT |
| 4 | `tools/eco/battery-storage.html` | 2.6 | empty_bogus | 空输入点「计算」（text_empty_no_select）→ 结果区 可用电量：0.00 kWh总能量：0.00 kWh ⏐ 📋 复制结果⬇️ 导出 TXT |
| 5 | `tools/eco/convert-air-aqi.html` | 2.6 | empty_bogus | 空输入点「计算」（text_empty_no_select）→ 结果区 0等级 优 ｜ 输入浓度 0 µg/m³ ｜ 建议 可正常户外活动 ⏐ 📋 复制结果⬇️ 导出 TXT |
| 6 | `tools/eco/eco-10.html` | 2.6 | empty_bogus | 空输入点「计算」（text_empty_no_select）→ 结果区 年发电量：0.00 MWh（千 kWh）年减排量：0.00 吨 CO₂等效植树：0 棵 ⏐ 📋 复制结果⬇️ 导出 TXT |
| 7 | `tools/eco/eco-11.html` | 2.6 | empty_bogus | 空输入点「计算」（text_empty_no_select）→ 结果区 单次额外燃油：0.00 L年额外燃油：0.00 L年额外碳排：0.00 吨 ⏐ 📋 复制结果⬇️ 导出 TXT |
| 8 | `tools/eco/eco-16.html` | 2.6 | empty_bogus | 空输入点「计算」（text_empty_no_select）→ 结果区 年发电量：0.00 MWh（千 kWh）年减排量：0.00 吨 CO₂等效减少汽车：0 辆 ⏐ 📋 复制结果⬇️ 导出 TXT |
| 9 | `tools/eco/eco-4.html` | 2.6 | empty_bogus | 空输入点「计算」（text_empty_no_select）→ 结果区 日产生量：0.00 吨/天年产生量：0.00 吨/年累计吨天数：0 kg·天 ⏐ 📋 复制结果⬇️ 导出 TXT |
| 10 | `tools/eco/eco-7.html` | 2.6 | empty_bogus | 空输入点「计算」（text_empty_no_select）→ 结果区 总标准煤：0.00 kgce总 kWh：0.00 kWh总 MJ：0.00 MJ ⏐ 📋 复制结果⬇️ 导出 TXT |
| 11 | `tools/eco/eco-8.html` | 2.6 | empty_bogus | 空输入点「计算」（text_empty_no_select）→ 结果区 总株数：0 株年碳汇量：0.00 吨/年累计碳汇：0.00 吨 ⏐ 📋 复制结果⬇️ 导出 TXT |
| 12 | `tools/eco/eco.html` | 2.6 | empty_bogus | 空输入点「计算」（text_empty_no_select）→ 结果区 电力碳排：0.00 kg燃煤碳排：0.00 kg天然气碳排：0.00 kg汽油碳排：0.00 kg总碳排：0.00 kg ⏐ �… |
| 13 | `tools/eco/ecological-footprint.html` | 2.6 | empty_bogus | 空输入点「计算」（text_empty_no_select）→ 结果区 生态足迹：0.000 gha ⏐ 📋 复制结果⬇️ 导出 TXT |
| 14 | `tools/eco/electricity-carbon.html` | 2.6 | empty_bogus | 空输入点「计算」（text_empty_no_select）→ 结果区 CO₂ 排放：0.00 kg等效树木吸收天数：0.0 天 ⏐ 📋 复制结果⬇️ 导出 TXT |
| 15 | `tools/eco/env-impact-score.html` | 2.6 | empty_bogus | 空输入点「计算」（text_empty_no_select）→ 结果区 综合评分：0.0 分最高项：0 分 ⏐ 📋 复制结果⬇️ 导出 TXT |
| 16 | `tools/eco/landfill-methane.html` | 2.6 | empty_bogus | 空输入点「计算」（text_empty_no_select）→ 结果区 CH₄ 产量：0.0 kg/年CO₂ 当量：0.0 kgCO₂e ⏐ 📋 复制结果⬇️ 导出 TXT |
| 17 | `tools/eco/rainwater-harvest.html` | 2.6 | empty_bogus | 空输入点「计算」（text_empty_no_select）→ 结果区 收集量：0 L折合吨：0.00 吨 ⏐ 📋 复制结果⬇️ 导出 TXT |
| 18 | `tools/eco/solar-output.html` | 2.6 | empty_bogus | 空输入点「计算」（text_empty_no_select）→ 结果区 发电量：0.0 kWh等效减排：0.00 kgCO₂ ⏐ 📋 复制结果⬇️ 导出 TXT |
| 19 | `tools/eco/water-footprint.html` | 2.6 | empty_bogus | 空输入点「计算」（text_empty_no_select）→ 结果区 总耗水：0 L折合 m³：0.00 m³ ⏐ 📋 复制结果⬇️ 导出 TXT |
| 20 | `tools/eco/water-saving.html` | 2.6 | empty_bogus | 空输入点「计算」（text_empty_no_select）→ 结果区 节约水量：0.0 L折合吨：0.00 吨 ⏐ 📋 复制结果⬇️ 导出 TXT |
| 21 | `tools/eco/wind-power.html` | 2.6 | empty_bogus | 空输入点「计算」（text_empty_no_select）→ 结果区 功率：0.00 kW ⏐ 📋 复制结果⬇️ 导出 TXT |
| 22 | `tools/encode/base32.html` | 2.6 | empty_bogus | 空输入点「计算」（text_empty_no_select）→ 结果区 编码长度：0 字符无填充长度：0 字符 ⏐ 📋 复制结果⬇️ 导出 TXT |
| 23 | `tools/fishery/salinity-calculator.html` | 2.6 | empty_bogus | 空输入点「🐟 计算」（text_empty_no_select）→ 结果区 ⚠️ 四项均需填写有效数值：现有水量须 >0，三个盐度须 ≥0。未测盐度请勿留空（淡水请明确输入 0） ⏐ 📋 复制结果… |
| 24 | `tools/hr/overtime-pay-calc.html` | 2.6 | empty_bogus | 空输入点「计算加班费」（text_empty_no_select）→ 结果区 工作日加班费：0.00 元休息日加班费：0.00 元法定节假日加班费：0.00 元总加班费：0.00 元 ⏐ 📋 复制结… |
| 25 | `tools/insurance/complete-life-expectancy.html` | 2.6 | empty_bogus | 空输入点「计算」（text_empty_no_select）→ 结果区 0.000完全期望寿命 e_x0生命表项数 N0.0000平均预期余命 ⏐ 📋 复制结果⬇️ 导出 TXT |
| 26 | `tools/insurance/ibnr-reserve.html` | 2.6 | empty_bogus | 空输入点「计算」（text_empty_no_select）→ 结果区 0.00IBNR 准备金 (元)0.00最终赔款估计 (元) ⏐ 📋 复制结果⬇️ 导出 TXT |
| 27 | `tools/insurance/life-cover-need.html` | 2.6 | empty_bogus | 空输入点「计算」（text_empty_no_select）→ 结果区 0.00建议保额 (元)0.00收入替代部分 (元)0.00保额下限 (元) ⏐ 📋 复制结果⬇️ 导出 TXT |
| 28 | `tools/investment/bond-price.html` | 2.6 | empty_bogus | 空输入点「计算」（text_empty_no_select）→ 结果区 0.00债券价格 P折价状态 ⏐ 📋 复制结果⬇️ 导出 TXT |
| 29 | `tools/investment/discounted-payback.html` | 2.6 | empty_bogus | 空输入点「计算」（text_empty_no_select）→ 结果区 0.00 年折现回收期 ⏐ 📋 复制结果⬇️ 导出 TXT |
| 30 | `tools/investment/npv-calc.html` | 2.6 | empty_bogus | 空输入点「计算」（text_empty_no_select）→ 结果区 0.00净现值 NPV ⏐ 📋 复制结果⬇️ 导出 TXT |
| 31 | `tools/investment/payback-period.html` | 2.6 | empty_bogus | 空输入点「计算」（text_empty_no_select）→ 结果区 0.00 年静态回收期 ⏐ 📋 复制结果⬇️ 导出 TXT |
| 32 | `tools/life/countdown.html` | 2.6 | empty_bogus | 空输入点「开始倒计时」（text_empty_no_select）→ 结果区 ⚡ 效率工具栏 ✓ 本地处理 0 字符 · 0 行 Ctrl/⌘ + Enter 快速运行 ⏐ 📋 复制结果⬇️ 导出 … |
| 33 | `tools/agriculture/detector-nutrition.html` | 2.2 | empty_conclusion | 空输入点「判读品质」（text_empty_no_select）→ 结果区 综合等级：不合格 优质 2 / 合格 2 / 共 6 项发酵度评价：发酵不足（乳酸 0%）指标实测判读蛋白质0%偏低脂肪0%… |
| 34 | `tools/agriculture/irrigation-uniformity.html` | 2.2 | empty_conclusion | 空输入点「计算」（text_empty_no_select）→ 结果区 0.0%克里斯琴森系数CU0.0%分布均匀度DU0.00平均灌水量(mm)0.0%变异系数CV均匀度评价：均匀性差CU参考标准：… |
| 35 | `tools/automotive/voltage-1.html` | 2.2 | empty_conclusion | 空输入点「🧮 计算」（text_empty_no_select）→ 结果区 38.0用电总电流 (A)38.0含充电总电流 (A)0负载率 (%)-38.0剩余电流 (A)0.55用电功率 (kW)… |
| 36 | `tools/beauty/recommender-face-shape.html` | 2.2 | empty_conclusion | 空输入点「生成」（text_empty_no_select）→ 结果区 生成结果： 1. 椭圆形脸 推荐发型：中长发、波浪卷、空气刘海 妆容建议：标准脸，眉形自然，唇妆可随心尝试 注意：公认理想脸型，… |
| 37 | `tools/biz/checker-8.html` | 2.2 | empty_conclusion | 空输入点「质量评估」（text_empty_no_select）→ 结果区 8服务质量总分服务质量不合格质量等级评估维度权重得分明细状态人员标准25%0持证0%/培训0%/着装0%/出勤0%差服务流程… |
| 38 | `tools/biz/presentation-timer.html` | 2.2 | empty_conclusion | 空输入点「开始演讲」（text_empty_no_select）→ 结果区 进度正常 |
| 39 | `tools/decor/detector-18.html` | 2.2 | empty_conclusion | 空输入点「检测判定」（text_empty_no_select）→ 结果区 室内空气质量检测结果（GB/T 18883-2022）污染物实测值限值判定甲醛0 mg/m³≤0.08✓ 达标 (0%)TV… |
| 40 | `tools/eco/aqi.html` | 2.2 | empty_conclusion | 空输入点「计算」（text_empty_no_select）→ 结果区 健康等级：1 级建议活动时长：0.0 小时PM2.5 估算：0.0 µg/m³ ⏐ 📋 复制结果⬇️ 导出 TXT |
| 41 | `tools/eco/noise-superposition.html` | 2.2 | empty_conclusion | 空输入点「计算叠加」（text_empty_no_select）→ 结果区 叠加后总声压级3.0 dB安静声源数量2最大声源0.0 dB能量平均0.0 dB较最大声源增加+3.0 dB距离衰减参考（点… |
| 42 | `tools/edu/assessor-27.html` | 2.2 | empty_conclusion | 空输入点「知识评估」（text_empty_no_select）→ 结果区 知识管理成熟度评估知识捕获：0/10 ✗知识共享：0/10 ✗知识应用：0/10 ✗知识创新：0/10 ✗知识存储：0/10… |
| 43 | `tools/electronics/bandwidth.html` | 2.2 | empty_conclusion | 空输入点「🧮 计算」（text_empty_no_select）→ 结果区 0.00e+0所需 GBP (Hz)0.00e+0建议 GBP (Hz)0.00e+0-3dB带宽 (Hz)推荐运放：LM… |
| 44 | `tools/electronics/capacitance.html` | 2.2 | empty_conclusion | 空输入点「🧮 计算」（text_empty_no_select）→ 结果区 0.00匹配电容 (pF)8推荐标准值 (pF)0.0晶振CL (pF)0.0杂散电容 (pF)C1=C2=C=2×(CL… |
| 45 | `tools/encode/encode-7.html` | 2.2 | empty_conclusion | 空输入点「计算」（text_empty_no_select）→ 结果区 空间大小：1 近似碰撞概率：0.000000 %安全阈值 n：1 ⏐ 📋 复制结果⬇️ 导出 TXT |
| 46 | `tools/endocrinology/detector-metabolism.html` | 2.2 | empty_conclusion | 空输入点「分析判读」（text_empty_no_select）→ 结果区 儿茶酚胺及代谢产物检测结果项目实测参考范围判定24h尿VMA0 mg/24h1-7↓ 偏低24h尿HVA0 mg/24h1-… |
| 47 | `tools/energy/air-purifier-area.html` | 2.2 | empty_conclusion | 空输入点「计算」（text_empty_no_select）→ 结果区 0最小面积 m²0推荐面积 m²0最大面积 m²0.0换气次数/小时 ⏐ 📋 复制结果⬇️ 导出 TXT ⏐ 📊 结果解读 … |
| 48 | `tools/energy/water-tds-evaluator.html` | 2.2 | empty_conclusion | 空输入点「评估」（text_empty_no_select）→ 结果区 直饮水级🎯 适用场景直饮无需处理高端饮用纯净水实验室超纯水稀释💡 健康提示水质极优，口感清冽。TDS极低可能意味着缺乏有益矿… |
| 49 | `tools/ent/ahi-severity.html` | 2.2 | empty_conclusion | 空输入点「计算评估」（text_empty_no_select）→ 结果区 0AHI(次/h)0AI暂停指数0HI低通气指数0ODI氧减指数0微觉醒指数100%正常 ⏐ 📋 复制结果⬇️ 导出 TX… |
| 50 | `tools/ent/hearing-loss-classification.html` | 2.2 | empty_conclusion | 空输入点「计算分析」（text_empty_no_select）→ 结果区 0PTA气导(dB)0PTA骨导(dB)0气骨导差(dB)0高频平均(dB) ⏐ 📋 复制结果⬇️ 导出 TXT ⏐ 参考… |

## 一、按钮有效性（点了没反应 / 点了报错）

### 点击主按钮抛异常（含 console 报错）（1 页）

- `tools/data/data-visualizer.html` — 按钮「📈 渲染」｜click: Invalid array length @ drawHistogram (/tools/data/data-visualizer.html:299:18)

## 二、空态（没填也敢给结论）

### 空输入直接给出 NaN/Infinity/undefined/null/0（31 页）

- `tools/agriculture/agri-calculator.html` — 空输入点「计算配比」（text_empty_no_select）→ 结果区 氮 (N)0.00kg磷 (P₂O₅)0.00kg钾 (K₂O)0.00kg配方比例：0-0-0施肥面积：0 亩每亩用量：0 kg/亩肥料总量：0.0 kg ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/design/px-to-rem.html` — 空输入点「计算」（text_empty_no_select）→ 结果区 转换结果 ⏐ 0px = 0.0000rem ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/eco/battery-storage.html` — 空输入点「计算」（text_empty_no_select）→ 结果区 可用电量：0.00 kWh总能量：0.00 kWh ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/eco/convert-air-aqi.html` — 空输入点「计算」（text_empty_no_select）→ 结果区 0等级 优 ｜ 输入浓度 0 µg/m³ ｜ 建议 可正常户外活动 ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/eco/eco-10.html` — 空输入点「计算」（text_empty_no_select）→ 结果区 年发电量：0.00 MWh（千 kWh）年减排量：0.00 吨 CO₂等效植树：0 棵 ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/eco/eco-11.html` — 空输入点「计算」（text_empty_no_select）→ 结果区 单次额外燃油：0.00 L年额外燃油：0.00 L年额外碳排：0.00 吨 ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/eco/eco-16.html` — 空输入点「计算」（text_empty_no_select）→ 结果区 年发电量：0.00 MWh（千 kWh）年减排量：0.00 吨 CO₂等效减少汽车：0 辆 ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/eco/eco-4.html` — 空输入点「计算」（text_empty_no_select）→ 结果区 日产生量：0.00 吨/天年产生量：0.00 吨/年累计吨天数：0 kg·天 ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/eco/eco-7.html` — 空输入点「计算」（text_empty_no_select）→ 结果区 总标准煤：0.00 kgce总 kWh：0.00 kWh总 MJ：0.00 MJ ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/eco/eco-8.html` — 空输入点「计算」（text_empty_no_select）→ 结果区 总株数：0 株年碳汇量：0.00 吨/年累计碳汇：0.00 吨 ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/eco/eco.html` — 空输入点「计算」（text_empty_no_select）→ 结果区 电力碳排：0.00 kg燃煤碳排：0.00 kg天然气碳排：0.00 kg汽油碳排：0.00 kg总碳排：0.00 kg ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/eco/ecological-footprint.html` — 空输入点「计算」（text_empty_no_select）→ 结果区 生态足迹：0.000 gha ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/eco/electricity-carbon.html` — 空输入点「计算」（text_empty_no_select）→ 结果区 CO₂ 排放：0.00 kg等效树木吸收天数：0.0 天 ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/eco/env-impact-score.html` — 空输入点「计算」（text_empty_no_select）→ 结果区 综合评分：0.0 分最高项：0 分 ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/eco/landfill-methane.html` — 空输入点「计算」（text_empty_no_select）→ 结果区 CH₄ 产量：0.0 kg/年CO₂ 当量：0.0 kgCO₂e ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/eco/rainwater-harvest.html` — 空输入点「计算」（text_empty_no_select）→ 结果区 收集量：0 L折合吨：0.00 吨 ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/eco/solar-output.html` — 空输入点「计算」（text_empty_no_select）→ 结果区 发电量：0.0 kWh等效减排：0.00 kgCO₂ ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/eco/water-footprint.html` — 空输入点「计算」（text_empty_no_select）→ 结果区 总耗水：0 L折合 m³：0.00 m³ ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/eco/water-saving.html` — 空输入点「计算」（text_empty_no_select）→ 结果区 节约水量：0.0 L折合吨：0.00 吨 ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/eco/wind-power.html` — 空输入点「计算」（text_empty_no_select）→ 结果区 功率：0.00 kW ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/encode/base32.html` — 空输入点「计算」（text_empty_no_select）→ 结果区 编码长度：0 字符无填充长度：0 字符 ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/fishery/salinity-calculator.html` — 空输入点「🐟 计算」（text_empty_no_select）→ 结果区 ⚠️ 四项均需填写有效数值：现有水量须 >0，三个盐度须 ≥0。未测盐度请勿留空（淡水请明确输入 0） ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/hr/overtime-pay-calc.html` — 空输入点「计算加班费」（text_empty_no_select）→ 结果区 工作日加班费：0.00 元休息日加班费：0.00 元法定节假日加班费：0.00 元总加班费：0.00 元 ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/insurance/complete-life-expectancy.html` — 空输入点「计算」（text_empty_no_select）→ 结果区 0.000完全期望寿命 e_x0生命表项数 N0.0000平均预期余命 ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/insurance/ibnr-reserve.html` — 空输入点「计算」（text_empty_no_select）→ 结果区 0.00IBNR 准备金 (元)0.00最终赔款估计 (元) ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/insurance/life-cover-need.html` — 空输入点「计算」（text_empty_no_select）→ 结果区 0.00建议保额 (元)0.00收入替代部分 (元)0.00保额下限 (元) ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/investment/bond-price.html` — 空输入点「计算」（text_empty_no_select）→ 结果区 0.00债券价格 P折价状态 ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/investment/discounted-payback.html` — 空输入点「计算」（text_empty_no_select）→ 结果区 0.00 年折现回收期 ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/investment/npv-calc.html` — 空输入点「计算」（text_empty_no_select）→ 结果区 0.00净现值 NPV ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/investment/payback-period.html` — 空输入点「计算」（text_empty_no_select）→ 结果区 0.00 年静态回收期 ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/life/countdown.html` — 空输入点「开始倒计时」（text_empty_no_select）→ 结果区 ⚡ 效率工具栏 ✓ 本地处理 0 字符 · 0 行 Ctrl/⌘ + Enter 快速运行 ⏐ 📋 复制结果⬇️ 导出 TXT

### 空输入直接给出结论（优秀/正常/合格…）（30 页）

- `tools/agriculture/detector-nutrition.html` — 空输入点「判读品质」（text_empty_no_select）→ 结果区 综合等级：不合格 优质 2 / 合格 2 / 共 6 项发酵度评价：发酵不足（乳酸 0%）指标实测判读蛋白质0%偏低脂肪0%偏低还原糖0%偏低水分0%优质灰分0%优质乳酸(发酵度)0%偏低品质解读：多…
- `tools/agriculture/irrigation-uniformity.html` — 空输入点「计算」（text_empty_no_select）→ 结果区 0.0%克里斯琴森系数CU0.0%分布均匀度DU0.00平均灌水量(mm)0.0%变异系数CV均匀度评价：均匀性差CU参考标准：>90%优秀 \| 80-90%良好 \| 70-80%一般 \| <70%差…
- `tools/automotive/voltage-1.html` — 空输入点「🧮 计算」（text_empty_no_select）→ 结果区 38.0用电总电流 (A)38.0含充电总电流 (A)0负载率 (%)-38.0剩余电流 (A)0.55用电功率 (kW)0.00发电机功率 (kW)负载充足平衡评估负载率: 0.0%（安全线 80%…
- `tools/beauty/recommender-face-shape.html` — 空输入点「生成」（text_empty_no_select）→ 结果区 生成结果： 1. 椭圆形脸 推荐发型：中长发、波浪卷、空气刘海 妆容建议：标准脸，眉形自然，唇妆可随心尝试 注意：公认理想脸型，多数发型都适合 2. 菱形脸 推荐发型：八字刘海、锁骨发、两侧蓬松 妆容…
- `tools/biz/checker-8.html` — 空输入点「质量评估」（text_empty_no_select）→ 结果区 8服务质量总分服务质量不合格质量等级评估维度权重得分明细状态人员标准25%0持证0%/培训0%/着装0%/出勤0%差服务流程30%25巡逻0%/门禁0%/响应0分钟/记录0%差装备设施20%0监控0%…
- `tools/biz/presentation-timer.html` — 空输入点「开始演讲」（text_empty_no_select）→ 结果区 进度正常
- `tools/decor/detector-18.html` — 空输入点「检测判定」（text_empty_no_select）→ 结果区 室内空气质量检测结果（GB/T 18883-2022）污染物实测值限值判定甲醛0 mg/m³≤0.08✓ 达标 (0%)TVOC0 mg/m³≤0.6✓ 达标 (0%)苯0 mg/m³≤0.03✓ 达…
- `tools/eco/aqi.html` — 空输入点「计算」（text_empty_no_select）→ 结果区 健康等级：1 级建议活动时长：0.0 小时PM2.5 估算：0.0 µg/m³ ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/eco/noise-superposition.html` — 空输入点「计算叠加」（text_empty_no_select）→ 结果区 叠加后总声压级3.0 dB安静声源数量2最大声源0.0 dB能量平均0.0 dB较最大声源增加+3.0 dB距离衰减参考（点声源，距最大声源）：1m0.0 dB5m-14.0 dB10m-20.0 d…
- `tools/edu/assessor-27.html` — 空输入点「知识评估」（text_empty_no_select）→ 结果区 知识管理成熟度评估知识捕获：0/10 ✗知识共享：0/10 ✗知识应用：0/10 ✗知识创新：0/10 ✗知识存储：0/10 ✗知识安全：0/10 ✗综合评分：0.00/10成熟度等级：1级-初始级知…
- `tools/electronics/bandwidth.html` — 空输入点「🧮 计算」（text_empty_no_select）→ 结果区 0.00e+0所需 GBP (Hz)0.00e+0建议 GBP (Hz)0.00e+0-3dB带宽 (Hz)推荐运放：LM358 / NE5532 (1~10MHz)。建议选型裕量≥2倍，高频应用还需…
- `tools/electronics/capacitance.html` — 空输入点「🧮 计算」（text_empty_no_select）→ 结果区 0.00匹配电容 (pF)8推荐标准值 (pF)0.0晶振CL (pF)0.0杂散电容 (pF)C1=C2=C=2×(CL−Cs)。推荐就近选取标准容值8pF，C1与C2各接一个。 ⏐ 匹配电容26.…
- `tools/encode/encode-7.html` — 空输入点「计算」（text_empty_no_select）→ 结果区 空间大小：1 近似碰撞概率：0.000000 %安全阈值 n：1 ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/endocrinology/detector-metabolism.html` — 空输入点「分析判读」（text_empty_no_select）→ 结果区 儿茶酚胺及代谢产物检测结果项目实测参考范围判定24h尿VMA0 mg/24h1-7↓ 偏低24h尿HVA0 mg/24h1-4↓ 偏低血去甲肾上腺素0 pg/mL80-520↓ 偏低血肾上腺素0 pg…
- `tools/energy/air-purifier-area.html` — 空输入点「计算」（text_empty_no_select）→ 结果区 0最小面积 m²0推荐面积 m²0最大面积 m²0.0换气次数/小时 ⏐ 📋 复制结果⬇️ 导出 TXT ⏐ 📊 结果解读 估算口径适用面积常按 CADR（洁净空气量）× 系数估算：卧室约 CAD…
- `tools/energy/water-tds-evaluator.html` — 空输入点「评估」（text_empty_no_select）→ 结果区 直饮水级🎯 适用场景直饮无需处理高端饮用纯净水实验室超纯水稀释💡 健康提示水质极优，口感清冽。TDS极低可能意味着缺乏有益矿物质，长期饮用纯净水建议适当补充矿物质。🌍 WHO标准对比完全符合WH…
- `tools/ent/ahi-severity.html` — 空输入点「计算评估」（text_empty_no_select）→ 结果区 0AHI(次/h)0AI暂停指数0HI低通气指数0ODI氧减指数0微觉醒指数100%正常 ⏐ 📋 复制结果⬇️ 导出 TXT ⏐ 参考区间标尺正常00.20.40.60.810
- `tools/ent/hearing-loss-classification.html` — 空输入点「计算分析」（text_empty_no_select）→ 结果区 0PTA气导(dB)0PTA骨导(dB)0气骨导差(dB)0高频平均(dB) ⏐ 📋 复制结果⬇️ 导出 TXT ⏐ 参考区间标尺正常00.20.40.60.810
- `tools/ent/laryngeal-nerve.html` — 空输入点「分析评估」（text_empty_no_select）→ 结果区 F0 基频0 Hz异常 ⏐ Jitter 微扰0%正常 ⏐ Shimmer 振幅微扰0%正常 ⏐ NHR 噪谐比0正常 ⏐ HNR 谐噪比0 dB异常 ⏐ MPT 最长发声0 秒异常 ⏐ 📋 复制结…
- `tools/fitness/weight-capacity-training.html` — 空输入点「🧮 计算」（text_empty_no_select）→ 结果区 0.0 kg训练总容量0.0 kg估算 1RM0.0%强度百分比0总次数强度区间：低强度 （推荐次数 25+）极低强度，适合热身与康复。相对 1RM 强度 0.0%（相对容量系数 -）1RM 百分比建…
- `tools/gardening/recommender.html` — 空输入点「生成」（text_empty_no_select）→ 结果区 浇水频次推荐：1. 发财树 \| 春季·阴雨·疏松透气 → 建议每10-14天1次，见干见湿，浇则浇透2. 兰花 \| 春季·多云·保水性强 → 建议每7-10天1次，忌积水，植料偏干后再浇3. 多肉植物…
- `tools/general/recommender-24.html` — 空输入点「生成」（text_empty_no_select）→ 结果区 替代产品/方案推荐：1. Figma → 替代：Penpot、Lunacy、Sketch2. Google Analytics → 替代：Plausible、Umami、Matomo3. Adobe …
- `tools/healthcare/checker-manager.html` — 空输入点「执行GSP检查」（text_empty_no_select）→ 结果区 📋 GSP质量管理检查报告检查维度评分判定说明质量管理体系与文件0/10需整改质量管理制度、操作规程、记录文件、内审人员与培训管理0/10需整改执业药师配备、岗前培训、年度继续教育设施与设备管理0/…
- `tools/healthcare/water-intake.html` — 空输入点「计算」（text_empty_no_select）→ 结果区 推荐饮水量：0 mL折合杯数(250mL)：0.0 杯 ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/hr/assessor-training-hr.html` — 空输入点「评估培训效果」（text_empty_no_select）→ 结果区 培训效果评估（柯氏前两层）培训主题：参训：0人 \| 时长：0小时能力提升：0→0（+0.0，提升0.0%）L1反应层（满意度）：0/100L2学习层-知识（测试通过率）：0/100L2学习层-技能（能…
- `tools/hr/attendance-stats.html` — 空输入点「📊 统计」（text_empty_no_select）→ 结果区 4员工数0 次迟到合计0 次早退合计0 天旷工合计0 天请假合计0 小时加班合计0 元扣款合计4 人全勤人数0 元全勤奖合计0 元加班费合计 ⏐ 📋 复制结果⬇️ 导出 TXT ⏐ 姓名迟到早退旷工…
- `tools/insurance/pure-premium.html` — 空输入点「计算」（text_empty_no_select）→ 结果区 0.00纯保费 (元/单位)0.00含10%安全边际 (元) ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/leather/temp-9.html` — 空输入点「🧮 计算」（text_empty_no_select）→ 结果区 0.00%收缩率0.0收缩温度 (℃)优秀热稳定性评估：收缩率＜3%，热稳定性优异。收缩温度偏低，需加强鞣制。 ⏐ 收缩率10.00% → 较差 ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/leather/time-34.html` — 空输入点「🧮 计算」（text_empty_no_select）→ 结果区 0推荐软化时间 (min)0基准时间 (min)2.92温度系数1.00活力系数操作建议：温度偏低，酶活性不足，建议升温至37~40℃。软化过度会损伤皮纤维，须密切监控。 ⏐ 软化时间31min ⏐ …
- `tools/leather/yield-rate-1.html` — 空输入点「🧮 计算」（text_empty_no_select）→ 结果区 0.00%铬回收率0.000回收铬量 (kg)较差处理效果回收率 = (废液浓度−回收后浓度) ÷ 废液浓度 × 100%。回收铬量 = 浓度差 × 处理量 ÷ 10⁶ (kg)。 ⏐ 回收率85.0…

## 三、死控件与辅助按钮

### select 默认态输出全 0 且无提示（非真空态，可疑需人工复核）（67 页）

- `tools/dermatology/leprosy-grading.html` — 空输入点「生成分级报告」（text_empty_sel_default｜select 默认 leprosyType=TT,n1=on,n2=on,n3=on,n4=on,n5=on,n6=on）→ 结果区 G0D0级残疾无感觉丧失和可见畸形 ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/forensic-medicine/electrocution-injury.html` — 空输入点「分析电击伤」（text_empty_sel_default｜select 默认 f1=on,f2=on,f3=on,f4=on,f5=on,f6=on,f7=on,f8=on,f9=on,f10=on,currentType=ac,voltage=low,contactSite=hand）→ 结果区 0阳性特征数0%特征符合度 ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/accessibility/braille-translator.html` — 空输入点「转译」（text_empty_sel_default｜select 默认 caseSel=keep）→ 结果区 原文：（空）字母 0 个 · 数字 0 个 · 盲文符号 0 格 ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/advertising/copy-duration.html` — 空输入点「⚡ 计算时长」（text_empty_sel_default｜select 默认 speedType=slow,lang=zh）→ 结果区 0秒朗读时长0中文字数0等效字数 ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/biz/text-remove-duplicates-lines.html` — 空输入点「去重」（text_empty_sel_default｜select 默认 trimLine=on,removeEmpty=on,sortResult=on）→ 结果区 （无内容） ⏐ on ⏐ 📋 复制结果⬇️ 导出 TXT ⏐ 0
- `tools/chemical/convert-capacity-tank.html` — 空输入点「换算」（text_empty_sel_default｜select 默认 type=vcyl）→ 结果区 容积 V = 0.000 m³ 总表面积 ≈ 0.00 m²（筒体加两封头，防腐涂装参考） ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/chess/go-territory.html` — 空输入点「♟️ 计算目数」（text_empty_sel_default｜select 默认 method=japanese）→ 结果区 平局计算方式：日本规则（数目法）贴目：0 目（白方）黑方：围空 0目 + 提子 0目 = 0.0目白方：围空 0目 + 提子 0目 + 贴目 0目 = 0.0目目差：0.0目🤝 平局：双方目数相同 …
- `tools/clinical-lab/electrophoresis-analysis.html` — 空输入点「分析」（text_empty_sel_default｜select 默认 hasMspike=on,hasBspike=on）→ 结果区 白蛋白降低白蛋白0%(0.0g/L)，低于参考下限。见于肝病(合成减少)、肾病综合征(丢失)、慢性炎症、营养不良。 ⏐ γ球蛋白降低γ球蛋白0%降低，见于免疫缺陷病、低丙种球蛋白血症、化疗后免疫抑制。…
- `tools/cosmetic-derm/wrinkle-dynamic-static.html` — 空输入点「评估」（text_empty_sel_default｜select 默认 crow_d=0,crow_s=0,glab_d=0,glab_s=0,fore_d=0,fore_s=0,nas_d=0,nas_s=0,nl_d=0,nl_s=0）→ 结果区 无明显皱纹0肉毒素总量(U)0.0填充总量(ml)0动态总分0静态总分无明显皱纹：当前状态良好。做好防晒、保湿、抗氧化护理即可预防皱纹产生。⚠️ 以上剂量为参考范围，实际用量需医师根据肌肉力量、面部解…
- `tools/dentistry/oral-cancer-screening.html` — 空输入点「分期」（text_empty_sel_default｜select 默认 t=is,n=0,m=0）→ 结果区 0期(原位癌)临床分期 Tis原发肿瘤 T N0淋巴结 N M0远处转移 M ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/edu/convert-2.html` — 空输入点「转换」（text_empty_sel_default｜select 默认 from=hex,to=hex）→ 结果区 #000000 ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/edu/convert-area-volume.html` — 空输入点「换算」（text_empty_sel_default｜select 默认 cat=length,from=m,to=m）→ 结果区 结果 = 0.0000 ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/edu/pinyin-converter.html` — 空输入点「🔄 转换」（text_empty_sel_default｜select 默认 withSpace=on,firstUpper=on,ignorePoly=on）→ 结果区 拼音结果 ⏐ 总字符：0 汉字：0 已转换：0 覆盖率：0% ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/elderly/eldercare-level.html` — 空输入点「生成建议」（text_empty_sel_default｜select 默认 a0=0,a0=1,a0=2,a1=0,a1=1,a1=2,a2=0,a2=1,a2=2,a3=0,a3=1,a3=2,a4=0,a4=1,a4=2,a5=0,a5=1,a5=2,a6=0,a6=1,a6=2）→ 结果区 总分：0建议等级：一级（轻度）照护建议：日常自理能力基本完整，建议日常巡检。提醒：该结果不替代医生或国家评估标准，仅用于家庭自查。 ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/energy/fridge-power-estimator.html` — 空输入点「计算」（text_empty_sel_default｜select 默认 efficiency=1）→ 结果区 0.00日耗电 kWh0年耗电 kWh¥0年电费¥0月均电费 ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/energy/standby-power-calculator.html` — 空输入点「计算」（text_empty_sel_default｜select 默认 chk-tv=on,chk-ac=on,chk-stb=on,chk-pc=on,chk-router=on,chk-washer=on,chk-microwave=on,chk-waterheater=on,chk-speaker=on,chk-console=on,chk-monitor=on,chk-printer=on,chk-charger=on,chk-fan=on,chk-oven=on）→ 结果区 0.0总待机功率 W0.000日耗电 kWh0.0年耗电 kWh¥0.0年电费 ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/finance/irr-calculator.html` — 空输入点「重新计算」（text_empty_sel_default｜select 默认 periodUnit=year）→ 结果区 -- IRR 内部收益率 ⏐ 0.00 NPV 净现值 ⏐ 0.00 总投入 ⏐ 0.00 总回报
- `tools/finance/word-counter.html` — 空输入点「分析」（text_empty_sel_default｜select 默认 showDensity=on）→ 结果区 ⚡ 效率工具栏 ✓ 本地处理 0 字符 · 0 行
- `tools/fire-rescue/fire-fighting-tactics.html` — 空输入点「推荐战术」（text_empty_sel_default｜select 默认 stage=1,structure=1,trapped=0,force=1,water=1）→ 结果区 初起阶段火灾阶段0着火面积(m²)砖混/框架结构建筑结构无被困人员 ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/fire-rescue/fire-investigation.html` — 空输入点「分析」（text_empty_sel_default｜select 默认 t1=on,t2=on,t3=on,t4=on,t5=on,t6=on,c1=on,c2=on,c3=on,c4=on,c5=on,c6=on,btype=residence）→ 结果区 0痕迹线索0原因线索0过火面积(m²)住宅建筑类型 ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/forensic-medicine/burn-assessment.html` — 空输入点「计算总面积」（text_empty_sel_default｜select 默认 ageGroup=adult,ageGroup=child,part_0=0,part_1=0,part_2=0,part_3=0,part_4=0,part_5=0,part_6=0,part_7=0,part_8=0,part_9=0,part_10=0,part_11=0,part_12=0）→ 结果区 0.0%总面积0%手掌法补充 ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/forensic-medicine/fall-injury.html` — 空输入点「综合分析」（text_empty_sel_default｜select 默认 landingPosture=head,surface=concrete,f1=on,f2=on,f3=on,f4=on,f5=on,f6=on,f7=on,f8=on,f9=on,f10=on,f11=on,f12=on,f13=on,f14=on）→ 结果区 0.0冲击速度 (m/s)0.0动能 (kJ)0损伤项数低度严重程度 ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/forensic-medicine/wound-description.html` — 空输入点「生成描述」（text_empty_sel_default｜select 默认 wt_blunt=blunt,wt_sharp=sharp,wt_firearm=firearm,bluntShape=stellate,bluntEdge=abraded,bluntWeapon=flat）→ 结果区 标准化损伤描述报告损伤类型：钝器伤损伤部位未指定创口大小0 cm × 0 cm创口形态星芒状创缘特征创缘有挫伤带/擦伤带推断致伤物平面致伤物（砖块/木板等）法医学意义钝器伤特点为创缘不整、有组织间桥、…
- `tools/gastroenterology/gastrin-level.html` — 空输入点「评估分析」（text_empty_sel_default｜select 默认 ph=low,onPPI=on,hypocalcemia=on）→ 结果区 0胃泌素 (pg/mL)正常范围评估结果 ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/gastroenterology/hepatic-encephalopathy.html` — 空输入点「评估分级」（text_empty_sel_default｜select 默认 consciousness=0,behavior=0,cognition=0,asterixis=0,mheTest=na,hasPrecipitant=on）→ 结果区 0级（无临床HE）HE分级 ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/gastroenterology/hp-dob.html` — 空输入点「解读结果」（text_empty_sel_default｜select 默认 testType=13c,onPPI=on,onAntibiotic=on,onBismuth=on）→ 结果区 0DOB值 (‰)结果不可靠（可能假阴性）检测结果 ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/gastroenterology/stool-occult-quant.html` — 空输入点「评估分析」（text_empty_sel_default｜select 默认 status=screening）→ 结果区 0FIT (μg/g) - 阴性0钙卫蛋白 (μg/g) - 正常 ⏐ screening ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/general/convert-22.html` — 空输入点「换算」（text_empty_sel_default｜select 默认 from=1,to=1）→ 结果区 00 无 (基准) = 0 无 (基准) ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/hematology/m-protein.html` — 空输入点「分析」（text_empty_sel_default｜select 默认 mzone=gamma,igg=on,iga=on,igm=on,igd=on,kappa=on,lambda=on）→ 结果区 0M蛋白 (g/L)未鉴定M蛋白类型-κ/λ比值 - ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/hr/recruitment-funnel.html` — 空输入点「👥 分析」（text_empty_sel_default｜select 默认 preset=custom）→ 结果区 📋 复制结果⬇️ 导出 TXT ⏐ 阶段人数环节通过率环节流失率—0———0———0———0———0———0———0———0——
- `tools/insurance/annuity-present.html` — 空输入点「计算」（text_empty_sel_default｜select 默认 type=ordinary）→ 结果区 📋 计算明细年金类型：普通年金每期金额：¥0.00每期利率：0.00%期数：0计算公式：i=0 时，PV = FV = PMT × n年金现值 PV = ¥0.00年金终值 FV = ¥0.00 ⏐…
- `tools/insurance/claim-reserve.html` — 空输入点「计算」（text_empty_sel_default｜select 默认 period=0.85）→ 结果区 📋 准备金明细当期已赚保费：¥0 万预期最终赔付率：0%损失率法：预期最终赔款 = 0 × 0% = ¥0 万IBNR = 0 - 0 - 0 = ¥0 万未决赔款准备金 = RBNS + IBNR…
- `tools/it/code-runner.html` — 空输入点「▶ 运行」（text_empty_sel_default｜select 默认 sampleSelect=,autoRun=on,showConsole=on）→ 结果区 ⚡ 效率工具栏 ✓ 本地处理 0 字符 · 0 行 Ctrl/⌘ + Enter 快速运行
- `tools/it/graphql-formatter.html` — 空输入点「校验」（text_empty_sel_default｜select 默认 indent=2）→ 结果区 ✅ GraphQL 语法正确 Tokens: 0 括号平衡 ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/it/js-obfuscator.html` — 空输入点「🛡 执行混淆」（text_empty_sel_default｜select 默认 optVarRename=on,optStringEncrypt=on,optRemoveComments=on,optRemoveWhitespace=on,optNumberHex=on,optStringArray=on）→ 结果区 0 ⏐ 0 ⏐ -
- `tools/it/json-formatter.html` — 空输入点「✨ 美化」（text_empty_sel_default｜select 默认 indent=2）→ 结果区 ⚡ 效率工具栏 ✓ 本地处理 0 字符 · 0 行 Ctrl/⌘ + Enter 快速运行 ⏐ 📋 复制结果⬇️ 导出 TXT ⏐ 等待输入...
- `tools/it/jwt-parser.html` — 空输入点「Decode」（text_empty_sel_default｜select 默认 genAlg=HS256,genExp=3600）→ 结果区 ⚡ 效率工具栏 ✓ 本地处理 0 字符 · 0 行 Ctrl/⌘ + Enter 快速运行 ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/it/qrcode.html` — 空输入点「生 成」（text_empty_sel_default｜select 默认 contentTemplate=,errorLevel=L,size=320,fgColor=#000000,bgColor=#000000）→ 结果区 ⚡ 效率工具栏 ✓ 本地处理 0 个参数
- `tools/it/text-cleaner.html` — 空输入点「执行清理」（text_empty_sel_default｜select 默认 opt-trim=trim,opt-empty-lines=empty-lines,opt-merge-spaces=merge-spaces,opt-merge-newlines=merge-newlines,opt-remove-inline-space=remove-inline-space,opt-remove-newlines=remove-newlines,opt-full2half=full2half,opt-half2full=half2full,opt-strip-html=strip-html,opt-decode-entities=decode-entities,opt-remove-invisible=remove-invisible,opt-unify-newlines=unify-newlines,opt-tab2space=tab2space,opt-space2tab=space2tab）→ 结果区 0 ⏐ 0 ⏐ 0 ⏐ 0 ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/it/text-dedupe-sort.html` — 空输入点「↑
升序排序」（text_empty_sel_default｜select 默认 caseSensitive=on,ignoreWhitespace=on,separator=\n）→ 结果区 0 ⏐ 0 ⏐ 0 ⏐ 📋 复制结果⬇️ 导出 TXT ⏐ 处理结果将显示在此处…点击上方操作按钮开始处理
- `tools/it/tiny-url.html` — 空输入点「生成短链接」（text_empty_sel_default｜select 默认 len=8,alias=on）→ 结果区 https://tinyurl.com/j0ezCg原始 URL: https://example.com/very/long/url/that/needs/shortening ⏐ 📋 复制结果⬇…
- `tools/it/xml-formatter.html` — 空输入点「校验」（text_empty_sel_default｜select 默认 indent=2）→ 结果区 ⚡ 效率工具栏 ✓ 本地处理 0 字符 · 0 行 Ctrl/⌘ + Enter 快速运行 ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/machinery/detector-194.html` — 空输入点「生成维修方案」（text_empty_sel_default｜select 默认 v1=1,v2=1,v4=1）→ 结果区 设备：泵类 \| 故障：异响振动使用年限：0年 \| 运行模式：连续运行建议方案：维修修复维修/更换检查清单：检查轴承磨损，测量游隙是否超标检查联轴器对中，校正偏差检查地脚螺栓紧固情况动平衡校验 ⏐ 📋…
- `tools/maritime/compass-correction.html` — 空输入点「计算」（text_empty_sel_default｜select 默认 convertDir=c2t）→ 结果区 000.0° 罗航向 CH 000.0° 磁航向 MH 000.0° 真航向 TH 0.0°E 罗经差 磁差 Var：0.0°E 自差 Dev：0.0°E 罗经差（Dev + Var）：0.0°E 换…
- `tools/maritime/speed-distance.html` — 空输入点「换算」（text_empty_sel_default｜select 默认 calcTarget=distance,speedUnit=knot,timeUnit=hour）→ 结果区 0.00 航速 (节) 0.00 时间 (小时) 0.00 航程 (海里) 计算目标：航程 航速多单位 0.000 节 = 0.000 km/h = 0.000 m/s 航程多单位 0.00 海里 =…
- `tools/mining/ore-grade.html` — 空输入点「计算」（text_empty_sel_default｜select 默认 metalType=gold）→ 结果区 0.00 品位 (g/t) 0.0000% 品位 (%) 0.00 金属含量 (kg) 0.0000 金属含量 (吨) 矿石量：0 吨 金属含量：0.00 千克（0.0000 吨） 品位评价：低于边界…
- `tools/mining/reserve-estimate.html` — 空输入点「估算储量」（text_empty_sel_default｜select 默认 gradeUnit=gt）→ 结果区 0 矿石体积 (m³) 0 地质储量 (吨) 0 可采储量 (吨) 0.00 金属量 (吨) 块段体积：0 立方米（0 m² × 0 m） 地质储量：0 吨（体重 0 t/m³） 平均品位：0.00 …
- `tools/neurology/ncs-emg.html` — 空输入点「分析定位」（text_empty_sel_default｜select 默认 amp=normal,cv=normal,dlat=normal,fwave=normal,block=none,samp=normal,emg_spont=none,emg_mup=normal,emg_recruit=normal）→ 结果区 检查结果基本正常或非特异性改变电生理特征解读电生理特征各参数均在正常范围或仅有轻微非特异性改变鉴别诊断无明显周围神经病变电生理证据建议结合临床评估，必要时复查建议未见明确周围神经或肌肉病变的电生理证据…
- `tools/nutrition/calc-2.html` — 空输入点「计算热量」（text_empty_sel_default｜select 默认 foodSelect=0\|0\|0）→ 结果区 0总热量 kcal 0.0g碳水化合物 0.0g蛋白质 0.0g脂肪 ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/pediatrics/hearing-screening.html` — 空输入点「生成解读报告」（text_empty_sel_default｜select 默认 method=oae,ageUnit=day,leftResult=pass,rightResult=pass,riskFactor=on）→ 结果区 通过左耳通过右耳0日龄无高危因素 ⏐ pass ⏐ pass ⏐ 通过筛查方法：OAE耳声发射 \| 随访：常规随访 ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/pet/convert-25.html` — 空输入点「换算」（text_empty_sel_default｜select 默认 species=dog）→ 结果区 人类年龄 ≈ 0.0 岁 说明：猫的换算系数与犬略有差异，本工具采用通用模型，仅供粗估 阶段提示：青少年期：相当于人类青少年，仍在发育，注意疫苗与驱虫完善 ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/pulmonology/gina-asthma.html` — 空输入点「GINA评估」（text_empty_sel_default｜select 默认 g1=0,g2=0,g3=0,g4=0）→ 结果区 0阳性项数良好控制GINA控制水平 ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/realestate/assessor-38.html` — 空输入点「计算评估」（text_empty_sel_default｜select 默认 ltv=70,rate=3.10,type=0）→ 结果区 0.00可贷额度(万元)0.0000月供(万元)0.00总利息(万元)0.00担保费(万元) ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/realestate/assessor-42.html` — 空输入点「计算评估」（text_empty_sel_default｜select 默认 landComp=6,resettle=4）→ 结果区 0补偿总额(元)0土地补偿费0安置补助费0附着物+青苗 ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/realestate/assessor-43.html` — 空输入点「计算评估」（text_empty_sel_default｜select 默认 equity=100）→ 结果区 0.00企业整体价值(万元)0.00股权价值(万元)0.00净资产(万元)0.0%资产负债率 ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/realestate/assessor-second-hand.html` — 空输入点「计算评估」（text_empty_sel_default｜select 默认 loc=0,floor=0,decor=0,orient=0,age=0）→ 结果区 0.0000评估单价(万/平米)0.00评估总价(万元)0.0000案例均价0%总调整幅度 ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/realestate/calc-assessor.html` — 空输入点「计算评估」（text_empty_sel_default｜select 默认 type=0,method=0,bonus=0）→ 结果区 0补偿总额(元)0房屋补偿费0临时安置费0奖励金 ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/rental/calc-commission-1.html` — 空输入点「🧮 计算」（text_empty_sel_default｜select 默认 type=sale,split=buyer）→ 结果区 买方承担 0 元，卖方承担 0 元。综合费率 = 总费用 ÷ 成交金额，供横向比较不同中介方案。 ⏐ 0中介费合计（元）0佣金（元）0服务费（元）-%综合费率 ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/reproductive-medicine/pgt-indication.html` — 空输入点「评估指征」（text_empty_sel_default｜select 默认 age=on,rpl=on,rif=on,male=on,monogenic=on,translocation=on,prevAneuploid=on,family=on）→ 结果区 无推荐类型0符合指征数未达常规 PGT 指征指征评估 ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/restaurant/safety-stock.html` — 空输入点「🏬 计算库存」（text_empty_sel_default｜select 默认 unit=kg）→ 结果区 库存状态：⚠️ 低于安全库存！ 当前库存：0 kg 距再订货点：0.0 kg （已达到/低于） ⏐ 0.0安全库存（kg） 0.0再订货点（kg） 0.0经济订货量（kg） 0预计可用天数 ⏐ 📋 …
- `tools/rheumatology/ssa-ssb.html` — 空输入点「评估临床意义」（text_empty_sel_default｜select 默认 ssa=neg,ssb=neg,ana=neg,rf=neg,comp=normal,pregnancy=no,dryeye=on,salivary=on,arthralgia=on,raynaud=on,rash=on,fatigue=on）→ 结果区 SSA-抗SSA/RoSSB-抗SSB/La0SS可能性评分 ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/sales/commission-calc.html` — 空输入点「💵 计算提成」（text_empty_sel_default｜select 默认 unit=元,method=progressive）→ 结果区 📋 复制结果⬇️ 导出 TXT ⏐ ¥ 0 佣金 0 元 · 含底薪合计 0 元 · 税后约 0 元
- `tools/sales/conversion-funnel.html` — 空输入点「🎯 分析」（text_empty_sel_default｜select 默认 preset=custom）→ 结果区 📋 复制结果⬇️ 导出 TXT ⏐ 阶段人数环节转化率环节流失率—0———0———0———0——
- `tools/science/convert-power.html` — 空输入点「转换」（text_empty_sel_default｜select 默认 from=N,to=N）→ 结果区 00 N = 0 N ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/sports/rater-motion.html` — 空输入点「计算评估」（text_empty_sel_default｜select 默认 unit=0）→ 结果区 0.00%变异系数(CV)0.000m平均成绩0.000标准差(SD)极稳定稳定性等级 ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/sports/tester-8.html` — 空输入点「计算评估」（text_empty_sel_default｜select 默认 exercise=0）→ 结果区 0.0MAOD(ml/kg)0.0累积氧亏(L)较弱无氧能力0.0min运动时长 ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/usedcar/detector-19.html` — 空输入点「检测泡水风险」（text_empty_sel_default｜select 默认 ck_smell=0,ck_carpet=0,ck_seatbelt=0,ck_seatrail=0,ck_ceiling=0,ck_dashboard=0,ck_electrics=0,ck_harness=0,ck_engbay=0,ck_silt=0,ck_fluid=0,ck_sparetire=0,ck_headlight=0,ck_waterline=0）→ 结果区 0%泡水风险指数未发现泡水痕迹检测结论0确认项数0可疑项数 ⏐ 📋 复制结果⬇️ 导出 TXT

### 改了输入再点主按钮，输出快照不变（低置信度线索，需人工复验）（57 页）

- `tools/dermatology/leprosy-grading.html` — 按钮「生成分级报告」｜构造值 leprosyType [select] "TT" → "BT"｜改前 G0D0级残疾无感觉丧失和可见畸形 ⏐ 📋 复制结果⬇️ 导出 TXT → 点击后 G0D0级残疾无感觉丧失和可见畸形 ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/forensic-medicine/electrocution-injury.html` — 按钮「分析电击伤」｜构造值 currentType [select] "ac" → "dc"｜改前 0阳性特征数0%特征符合度 ⏐ 📋 复制结果⬇️ 导出 TXT → 点击后 0阳性特征数0%特征符合度 ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/agriculture/countdown-4.html` — 按钮「开始孵化」｜构造值 batchName [text] "abc 123" → "abc 123x"｜改前 📖 查看「鸡蛋孵化倒计时（21天）使用指南」 📅 鸡蛋孵化倒计时（21天） ⚠️ 专业工具免责声明 本工具结果为本页… → 点击后 📖 查看「鸡蛋孵化倒计时（21天）使用指南」 📅 鸡蛋孵化倒计时（21天） ⚠️ 专业工具免责声明 本工具结果为本页…
- `tools/cardiology/calc-1.html` — 按钮「评估分级」｜构造值 sbp [number] "175" → "140"｜改前 血压分级：2级高血压 收缩压 ≥160 或 舒张压 ≥100 mmHg 心血管风险分层：中危 2级高血压且无其他危险因素… → 点击后 血压分级：2级高血压 收缩压 ≥160 或 舒张压 ≥100 mmHg 心血管风险分层：中危 2级高血压且无其他危险因素…
- `tools/chinese/chinese-radical-lookup.html` — 按钮「查询」｜构造值 char [text] "abc 123" → "abc 123x"｜改前 未收录「a」，你可以提交 PR 补充更多常用字 ⏐ 📋 复制结果⬇️ 导出 TXT → 点击后 未收录「a」，你可以提交 PR 补充更多常用字 ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/chinese/stroke-order-viewer.html` — 按钮「查看笔顺」｜构造值 word [text] "abc 123" → "abc 123x"｜改前 a 未收录笔顺，可先按拼音/部首分解辅助书写。 ⏐ 笔序笔画状态该字未收录笔顺数据 → 点击后 a 未收录笔顺，可先按拼音/部首分解辅助书写。 ⏐ 笔序笔画状态该字未收录笔顺数据
- `tools/data/pivot-table.html` — 按钮「📊 生成」｜构造值 inputData [textarea] "abc 123" → "probe-a\nprobe-b\nprob"｜改前 🔄 透视表 (sum) 地区 \ 产品 AB 合计 华北 210150 360 华东 200340 540 华南 12… → 点击后 🔄 透视表 (sum) 地区 \ 产品 AB 合计 华北 210150 360 华东 200340 540 华南 12…
- `tools/design/farnsworth-d15-test.html` — 按钮「✅ 完成并分析」｜构造值 fdShuffle [select] "light" → "medium"｜改前 ⚠️ 非选择性排列错误（未检出明确混淆轴向）共有 10 处错位、混淆指数 C = 2.84，但误差向量在各方向上分布均匀… → 点击后 ⚠️ 非选择性排列错误（未检出明确混淆轴向）共有 10 处错位、混淆指数 C = 2.84，但误差向量在各方向上分布均匀…
- `tools/design/flexbox-generator.html` — 按钮「计算」｜构造值 gap [number] "12" → "9.600000000000001"｜改前 生成的 CSS ⏐ 实时预览（3 个项目） ⏐ 📋 复制结果⬇️ 导出 TXT → 点击后 生成的 CSS ⏐ 实时预览（3 个项目） ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/design/mesh-gradient.html` — 按钮「生成」｜构造值 overlay [text] "abc 123" → "abc 123x"｜改前 background-color: #000000; background-image: radial-gradient… → 点击后 background-color: #000000; background-image: radial-gradient…
- `tools/electrical/generator-23.html` — 按钮「生成」｜构造值 expr [text] "abc 123" → "abc 123x"｜改前 ⚠ 表达式解析失败：变量只支持单个字母 A–H：abc ⏐ 📋 复制结果⬇️ 导出 TXT → 点击后 ⚠ 表达式解析失败：变量只支持单个字母 A–H：abc ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/electromagnetism/free-space-impedance.html` — 按钮「计算」｜构造值 x [number] "0" → "1"｜改前 376.73波阻抗 Z₀ (Ω)2.997925真空光速 (×10⁸ m/s)1.256637真空磁导率 μ₀ (μH/… → 点击后 376.73波阻抗 Z₀ (Ω)2.997925真空光速 (×10⁸ m/s)1.256637真空磁导率 μ₀ (μH/…
- `tools/endocrinology/pcos-diagnosis.html` — 按钮「诊断评估」｜构造值 cycle [number] "45" → "36"｜改前 满足① 排卵障碍满足② 高雄激素满足③ 多囊形态 ⏐ 📋 复制结果⬇️ 导出 TXT → 点击后 满足① 排卵障碍满足② 高雄激素满足③ 多囊形态 ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/finance/credit-card-validator.html` — 按钮「校验」｜构造值 cardInput [text] "abc 123" → "abc 123x"｜改前 卡号格式化：123卡组织识别： 未知卡组织原始数字：123长度校验： ⚠️ 当前 3 位（卡组织未知，按通用 13-19… → 点击后 卡号格式化：123卡组织识别： 未知卡组织原始数字：123长度校验： ⚠️ 当前 3 位（卡组织未知，按通用 13-19…
- `tools/food-processing/fermentation-brix.html` — 按钮「计算」｜构造值 vol [number] "100" → "80"｜改前 0g糖消耗量0.00%酒精度 ABV0g酒精生成量0gCO₂生成量 ⏐ 📋 复制结果⬇️ 导出 TXT → 点击后 0g糖消耗量0.00%酒精度 ABV0g酒精生成量0gCO₂生成量 ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/food-processing/ph-adjustment.html` — 按钮「计算」｜构造值 vol [number] "0.001" → "0.001"｜改前 0.00mL需加溶液量0.000g纯物质量0.0000mol物质的量pH 无变化调节方向 ⏐ 📋 复制结果⬇️ 导出 … → 点击后 0.00mL需加溶液量0.000g纯物质量0.0000mol物质的量pH 无变化调节方向 ⏐ 📋 复制结果⬇️ 导出 …
- `tools/forensic-medicine/rigor-mortis.html` — 按钮「评估死后时间」｜构造值 envTemp [select] "low" → "normal"｜改前 2.0平均僵硬度2.0上部关节2.0下部关节 ⏐ 📋 复制结果⬇️ 导出 TXT → 点击后 2.0平均僵硬度2.0上部关节2.0下部关节 ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/fun/chess-fen-viewer.html` — 按钮「初始」｜构造值 fen [text] "rnbqkbnr/pppppppp/8/" → "rnbqkbnr/pppppppp/8/"｜改前 轮到：白方 / 王车易位：KQkq / 吃过路兵：- ⏐ 📋 复制结果⬇️ 导出 TXT → 点击后 轮到：白方 / 王车易位：KQkq / 吃过路兵：- ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/funeral/memorial-date.html` — 按钮「计算」｜构造值 memTitle [text] "abc 123" → "abc 123x"｜改前 • 头七：逝后第 7 天 • 三七 / 五七：逝后第 21 / 35 天 • 百日：逝后第 100 天 • 周年：逝后满… → 点击后 • 头七：逝后第 7 天 • 三七 / 五七：逝后第 21 / 35 天 • 百日：逝后第 100 天 • 周年：逝后满…
- `tools/gardening/plant-calendar.html` — 按钮「📅 月份视图」｜构造值 search [text] "abc 123" → "abc 123x"｜改前 📖 查看「蔬菜种植时间历使用指南」 📅 蔬菜种植日历 按月份/季节/类别查看蔬菜种植时间，含播种、移栽、收获、生长期… → 点击后 📖 查看「蔬菜种植时间历使用指南」 📅 蔬菜种植日历 按月份/季节/类别查看蔬菜种植时间，含播种、移栽、收获、生长期…
- `tools/healthcare/bac-calculator.html` — 按钮「计算」｜构造值 volume [number] "350" → "280"｜改前 BAC：0.000 g/100mL ⏐ 📋 复制结果⬇️ 导出 TXT → 点击后 BAC：0.000 g/100mL ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/hematology/dic-scoring.html` — 按钮「评分」｜构造值 plt [number] "45" → "36"｜改前 5ISTH评分显性DIC诊断倾向 ⏐ 📋 复制结果⬇️ 导出 TXT ⏐ 参考区间标尺不提示 DIC01.63.24.… → 点击后 5ISTH评分显性DIC诊断倾向 ⏐ 📋 复制结果⬇️ 导出 TXT ⏐ 参考区间标尺不提示 DIC01.63.24.…
- `tools/hematology/itp-risk-score.html` — 按钮「评分」｜构造值 drug [select] "heparin" → "quinine"｜改前 8总分 (满分8)确定 (Definite)因果关系等级 ⏐ 📋 复制结果⬇️ 导出 TXT ⏐ 参考区间标尺不太可能… → 点击后 8总分 (满分8)确定 (Definite)因果关系等级 ⏐ 📋 复制结果⬇️ 导出 TXT ⏐ 参考区间标尺不太可能…
- `tools/hematology/mm-staging.html` — 按钮「分期」｜构造值 albumin [number] "35" → "28"｜改前 R-ISS III分期ISS 3ISS分期43个月中位OS ⏐ 📋 复制结果⬇️ 导出 TXT → 点击后 R-ISS III分期ISS 3ISS分期43个月中位OS ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/image/image-compress.html` — 按钮「压缩质量80·输出格式webp·最大尺寸（等比缩放）1920」｜构造值 fmt [select] "webp" → "jpeg"｜改前 ⚡ 效率工具栏 ✓ 本地处理 1 个文件入口 ⏐ 📋 复制结果⬇️ 导出 TXT → 点击后 ⚡ 效率工具栏 ✓ 本地处理 1 个文件入口 ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/image/wechat-cover-maker.html` — 按钮「生成」｜构造值 title [text] "abc 123" → "abc 123x"｜改前 ✨ 公众号封面生成器 纯前端生成 900×383 封面图：标题 + 副标题 + 背景渐变 + 下载。 标题 副标题 背景… → 点击后 ✨ 公众号封面生成器 纯前端生成 900×383 封面图：标题 + 副标题 + 背景渐变 + 下载。 标题 副标题 背景…
- `tools/it/calc-7.html` — 按钮「格式化对象」｜构造值 jsonInput [textarea] "{\"a\":1,\"b\":2}" → "{\"a\":2}"｜改前 对象中不存在键 user。 ⏐ 📋 复制结果⬇️ 导出 TXT → 点击后 对象中不存在键 user。 ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/it/docker-run-converter.html` — 按钮「计算」｜构造值 cmd [textarea] "abc 123" → "probe-a\nprobe-b\nprob"｜改前 docker-compose.yml ⏐ 📋 复制结果⬇️ 导出 TXT → 点击后 docker-compose.yml ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/it/dockerfile-generator.html` — 按钮「计算」｜构造值 port [number] "3000" → "2400"｜改前 Dockerfile ⏐ 📋 复制结果⬇️ 导出 TXT → 点击后 Dockerfile ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/it/hill-cipher.html` — 按钮「加密 ↑」｜构造值 key [text] "abc 123" → "abc 123x"｜改前 密钥矩阵3325行列式9 mod 26行列式逆元3逆矩阵1517209 ⏐ 📋 复制结果⬇️ 导出 TXT → 点击后 密钥矩阵3325行列式9 mod 26行列式逆元3逆矩阵1517209 ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/it/html-nesting-checker.html` — 按钮「检查」｜构造值 html [textarea] "<div><p>hi</p></div>" → "<div><span>x</span…｜改前 ✅ HTML 嵌套结构合法（无未闭合/错误嵌套标签） ⏐ 📋 复制结果⬇️ 导出 TXT ⏐ 📊 结果解读 结果含义… → 点击后 ✅ HTML 嵌套结构合法（无未闭合/错误嵌套标签） ⏐ 📋 复制结果⬇️ 导出 TXT ⏐ 📊 结果解读 结果含义…
- `tools/it/json-to-tsv.html` — 按钮「转换 →」｜构造值 jsonInput [textarea] "{\"a\":1}" → "{\"a\":2}"｜改前 name age city Alice 30 New York Bob 25 London → 点击后 name age city Alice 30 New York Bob 25 London
- `tools/it/mac-lookup.html` — 按钮「查询」｜构造值 macInput [text] "abc 123" → "abc 123x"｜改前 ❌ 长度错误：当前 6 个十六进制字符，应为 12 位 ⏐ 📋 复制结果⬇️ 导出 TXT → 点击后 ❌ 长度错误：当前 6 个十六进制字符，应为 12 位 ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/it/password-generator.html` — 按钮「🎲 生成」｜构造值 length [number] "66" → "52.800000000000004"｜改前 16+ 推荐长度 4种 字符类型 90天 更换周期 2FA 双重验证 ⏐ ⚡ 效率工具栏 ✓ 本地处理 13 个参数 C… → 点击后 16+ 推荐长度 4种 字符类型 90天 更换周期 2FA 双重验证 ⏐ ⚡ 效率工具栏 ✓ 本地处理 13 个参数 C…
- `tools/it/plist-parser.html` — 按钮「压缩」｜构造值 input [textarea] "<root><item>1</item>" → "<root><item>3</it…｜改前 { "name": "Alice", "age": 30, "active": true, "tags": [ "adm… → 点击后 { "name": "Alice", "age": 30, "active": true, "tags": [ "adm…
- `tools/it/protobuf-parser.html` — 按钮「解析」｜构造值 input [textarea] "abc 123" → "probe-a\nprobe-b\nprob"｜改前 { "syntax": "", "package": "", "imports": [], "options": [],… → 点击后 { "syntax": "", "package": "", "imports": [], "options": [],…
- `tools/it/sitemap-generator.html` — 按钮「计算」｜构造值 urls [textarea] "https://example.com/" → "https://example.co…｜改前 sitemap.xml ⏐ 📋 复制结果⬇️ 导出 TXT → 点击后 sitemap.xml ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/it/toml-formatter.html` — 按钮「格式化」｜构造值 input [textarea] "abc 123" → "probe-a\nprobe-b\nprob"｜改前 title = "toolbox" port = 8080 replicas = 3 ⏐ 📋 复制结果⬇️ 导出 TX… → 点击后 title = "toolbox" port = 8080 replicas = 3 ⏐ 📋 复制结果⬇️ 导出 TX…
- `tools/it/uuid-v5-generator.html` — 按钮「生成」｜构造值 ns [text] "abc 123" → "abc 123x"｜改前 example.com → cfbff0d1-9375-5685-968c-48ce8b15ae17example.or… → 点击后 example.com → cfbff0d1-9375-5685-968c-48ce8b15ae17example.or…
- `tools/life/chinese-number.html` — 按钮「转换」｜构造值 inputVal [text] "abc 123" → "abc 123x"｜改前 无法识别输入 ⏐ 简体：〇 一 二 三 四 五 六 七 八 九 十 百 千 万 亿 大写：零 壹 贰 叁 肆 伍 陆 柒… → 点击后 无法识别输入 ⏐ 简体：〇 一 二 三 四 五 六 七 八 九 十 百 千 万 亿 大写：零 壹 贰 叁 肆 伍 陆 柒…
- `tools/life/unit-converter.html` — 按钮「▶ 运行」｜构造值 fromValue [number] "1" → "0.8"｜改前 • 选择分类后，在左侧输入数值即可实时换算到右侧单位 • 点击中间 ⇅ 按钮可交换两个单位 • 常用换算速查可一键填入常… → 点击后 • 选择分类后，在左侧输入数值即可实时换算到右侧单位 • 点击中间 ⇅ 按钮可交换两个单位 • 常用换算速查可一键填入常…
- `tools/manufacturing/quality-control.html` — 按钮「⚖️ 计算 CPK」｜构造值 usl [number] "10.5" → "8.4"｜改前 CPK (综合能力指数) ⏐ 1.111 ⏐ CP (潜在能力) ⏐ 1.111 ⏐ CA (偏移系数) ⏐ 0.0% … → 点击后 CPK (综合能力指数) ⏐ 1.111 ⏐ CP (潜在能力) ⏐ 1.111 ⏐ CA (偏移系数) ⏐ 0.0% …
- `tools/metallurgy/alloy-ratio.html` — 按钮「计算加入量」｜构造值 steelW [number] "0.01" → "0.01"｜改前 总原料加入量 0.000 t ⏐ 📋 复制结果⬇️ 导出 TXT → 点击后 总原料加入量 0.000 t ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/music/chord-notes.html` — 按钮「🔍 分析和弦」｜构造值 chordInput [text] "abc 123" → "abc 123x"｜改前 和弦类型标记示例音程（半音）结构 大三和弦C0, 4, 7根-大三-纯五 小三和弦Am0, 3, 7根-小三-纯五 增三… → 点击后 和弦类型标记示例音程（半音）结构 大三和弦C0, 4, 7根-大三-纯五 小三和弦Am0, 3, 7根-小三-纯五 增三…
- `tools/music/music-analysis.html` — 按钮「🎤 开始分析」｜构造值 sample-rate [number] "12" → "9.600000000000001"｜改前 码率: 1411 kbps 每秒: 172.27 KB/s 60秒总大小: 10.09 MB 每小时: 605.62 M… → 点击后 码率: 1411 kbps 每秒: 172.27 KB/s 60秒总大小: 10.09 MB 每小时: 605.62 M…
- `tools/nuclear/pair-annihilation.html` — 按钮「计算」｜构造值 dummy [number] "1" → "0.8"｜改前 511.0每个光子能量 (keV)1022.0总能量 (keV)0.5110每个光子能量 (MeV)1.0220总能量 … → 点击后 511.0每个光子能量 (keV)1022.0总能量 (keV)0.5110每个光子能量 (MeV)1.0220总能量 …
- `tools/pet/fish-tank-volume.html` — 按钮「计算水量」｜构造值 length [number] "2" → "1.6"｜改前 • 过滤器：流量建议为水量的3-5倍/小时 • 加热棒：每升水约需1-2W加热功率 • 增氧泵：小型缸2-5W，大型缸5… → 点击后 • 过滤器：流量建议为水量的3-5倍/小时 • 加热棒：每升水约需1-2W加热功率 • 增氧泵：小型缸2-5W，大型缸5…
- `tools/rental/cycle-11.html` — 按钮「计算结算」｜构造值 number [number] "260" → "208"｜改前 ⏱️ 水电（读数/周期）结算 记录电表、水表、燃气表读数，自动计算用量与费用，支持阶梯电价，生成结算报告。 📐 工作原… → 点击后 ⏱️ 水电（读数/周期）结算 记录电表、水表、燃气表读数，自动计算用量与费用，支持阶梯电价，生成结算报告。 📐 工作原…
- `tools/rheumatology/sapho-syndrome.html` — 按钮「评估诊断」｜构造值 duration [number] "3" → "2.4000000000000004"｜改前 高度提示SAPHO综合征诊断评估中等活动疾病活动度7诊断评分 ⏐ 📋 复制结果⬇️ 导出 TXT → 点击后 高度提示SAPHO综合征诊断评估中等活动疾病活动度7诊断评分 ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/sales/moving-average.html` — 按钮「🔮 预测」｜构造值 window [number] "11" → "8.8"｜改前 📋 复制结果⬇️ 导出 TXT ⏐ 期数实际值移动平均/预测第3期128128第4期142135第5期150140第6… → 点击后 📋 复制结果⬇️ 导出 TXT ⏐ 期数实际值移动平均/预测第3期128128第4期142135第5期150140第6…
- `tools/science/calc-cycle.html` — 按钮「计算」｜构造值 formula [text] "abc 123" → "abc 123x"｜改前 ❌ 无法识别的字符："a" ⏐ 📋 复制结果⬇️ 导出 TXT → 点击后 ❌ 无法识别的字符："a" ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/science/periodic-table.html` — 按钮「搜索 Fe」｜构造值 search [text] "Fe" → "Fex"｜改前 H氢 Hydrogen原子序数 1 · 第1周期 · 第1族 · 非金属原子量1.008电子排布1s¹密度0.0899 … → 点击后 H氢 Hydrogen原子序数 1 · 第1周期 · 第1族 · 非金属原子量1.008电子排布1s¹密度0.0899 …
- `tools/sports/sports-stats.html` — 按钮「跑步周」｜构造值 aMinutes [number] "2" → "1.6"｜改前 2总记录数 ⏐ 720总消耗 kcal ⏐ 70总时长 分钟 ⏐ 12.0总距离 km ⏐ 日期类型时长(min)距离(… → 点击后 2总记录数 ⏐ 720总消耗 kcal ⏐ 70总时长 分钟 ⏐ 12.0总距离 km ⏐ 日期类型时长(min)距离(…
- `tools/stats/statistical-tests.html` — 按钮「🧮 检验」｜构造值 one-mu [number] "20" → "16"｜改前 样本数 n10样本均值 x̄25.5000样本标准差 s8.6699标准误 SE2.7417假设均值 μ₀20t 统计量… → 点击后 样本数 n10样本均值 x̄25.5000样本标准差 s8.6699标准误 SE2.7417假设均值 μ₀20t 统计量…
- `tools/tcm-chemistry/fingerprint-similarity.html` — 按钮「📋 计算相似度」｜构造值 refData [textarea] "abc 123" → "probe-a\nprobe-b\nprob"｜改前 0.9981平均相关系数0.9995平均夹角余弦0.9985最大相关系数0.9974最小相关系数 ⏐ 📋 复制结果⬇️… → 点击后 0.9981平均相关系数0.9995平均夹角余弦0.9985最大相关系数0.9974最小相关系数 ⏐ 📋 复制结果⬇️…
- `tools/tcm-chemistry/structure-identification.html` — 按钮「📊 解析IR数据」｜构造值 irInput [text] "abc 123" → "abc 123x"｜改前 IR数据解析结果输入1个吸收峰，识别出0个特征基团📊 特征峰归属结构特征推断：未识别到明显特征基团解析提示：IR主要用… → 点击后 IR数据解析结果输入1个吸收峰，识别出0个特征基团📊 特征峰归属结构特征推断：未识别到明显特征基团解析提示：IR主要用…
- `tools/text/text-to-ascii-art.html` — 按钮「计算」｜构造值 src [text] "abc 123" → "abc 123x"｜改前 ASCII 艺术字 ⏐ 📋 复制结果⬇️ 导出 TXT → 点击后 ASCII 艺术字 ⏐ 📋 复制结果⬇️ 导出 TXT

### 重置按钮未改变任何输入（31 页）

- `tools/audio/audio-recorder.html` — 「清空全部」｜点击后所有输入值未变化
- `tools/biz/lorem-ipsum-advanced.html` — 「清空」｜点击后所有输入值未变化
- `tools/cleaning/appliance-cycle.html` — 「重置所有记录」｜点击后所有输入值未变化
- `tools/dentistry/sialography.html` — 「清空」｜点击后所有输入值未变化
- `tools/design/image-to-ascii.html` — 「清空」｜点击后所有输入值未变化
- `tools/edu2/wrong-book.html` — 「清空全部」｜点击后所有输入值未变化
- `tools/elderly/fall-risk.html` — 「重置」｜点击后所有输入值未变化
- `tools/elderly/reminder-time.html` — 「🗑️ 清空全部」｜点击后所有输入值未变化
- `tools/finance/password-generator-advanced.html` — 「清空」｜点击后所有输入值未变化
- `tools/food/nutrition-calculator.html` — 「清空本餐」｜点击后所有输入值未变化
- `tools/funeral/ceremony-timeline.html` — 「清空」｜点击后所有输入值未变化
- `tools/general/calc-13.html` — 「🗑️ 重置」｜点击后所有输入值未变化
- `tools/general/calc-14.html` — 「🗑️ 重置」｜点击后所有输入值未变化
- `tools/hematology/aps-diagnosis.html` — 「重置」｜点击后所有输入值未变化
- `tools/hematology/rater-risk-1.html` — 「重置」｜点击后所有输入值未变化
- `tools/home/furniture-layout.html` — 「🧹 清空布局」｜点击后所有输入值未变化
- `tools/hydraulic/cycle-19.html` — 「清空」｜点击后所有输入值未变化
- `tools/it/nanoid-generator.html` — 「清空」｜点击后所有输入值未变化
- `tools/it/random.html` — 「清空」｜点击后所有输入值未变化
- `tools/it/uuid-v7-generator.html` — 「清空」｜点击后所有输入值未变化
- `tools/property/cycle-10.html` — 「清空」｜点击后所有输入值未变化
- `tools/rehabilitation/berg-balance-scale.html` — 「重置」｜点击后所有输入值未变化
- `tools/rehabilitation/flacc-scale.html` — 「重置」｜点击后所有输入值未变化
- `tools/rehabilitation/mmse-scoring.html` — 「重置」｜点击后所有输入值未变化
- `tools/rheumatology/bvas.html` — 「重置」｜点击后所有输入值未变化
- `tools/rheumatology/rater-16.html` — 「重置」｜点击后所有输入值未变化
- `tools/rheumatology/rater-17.html` — 「重置」｜点击后所有输入值未变化
- `tools/rheumatology/sledai.html` — 「重置」｜点击后所有输入值未变化
- `tools/safety/reminder-cycle-protection.html` — 「清空全部」｜点击后所有输入值未变化
- `tools/tcm-diagnosis/tongue-diagnosis.html` — 「重置」｜点击后所有输入值未变化
- `tools/transport/calc-4.html` — 「🗑️ 清空选择」｜点击后所有输入值未变化

### 导出/下载按钮 onclick 目标函数不存在（必死）（1 页）

- `tools/it/typescript-compiler.html` — 「⬇ 下载 JS」｜onclick 调用 downloadJs() 但该函数不存在（typeof=false）

### 死控件（静态检测，1 页）

> 仅列「控件 id 在整页脚本中零引用、且页面没有泛化读取控件」的页；如需与运行时交叉验证，见 JSON 的 `deadControlPages`。

- `tools/legal/legal-calculator.html` — lit-type-labor(input/radio)、lit-type-ip(input/radio)

### 低置信度线索：导出/下载未观察到触发（352 页）

> 这些页的导出按钮 onclick 函数存在、点击也不报错，但没观察到带 download 的 `a.click()`；多为结果为空时静默 return，需人工复核，不计入缺陷数。

- `tools/accounting/report-2.html` —「导出明细 CSV」（__report_2Export）
- `tools/acupuncture/acupoint-combination.html` —「导出明细 CSV」（__acupoint_combinationExport）
- `tools/admin/analysis-30.html` —「导出明细 CSV」（__analysis_30Export）
- `tools/admin/detector-time.html` —「⬇️ 导出日程 CSV」
- `tools/admin/version-control.html` —「📤 导出JSON」（exportData）
- `tools/advertising/analysis-27.html` —「导出明细 CSV」（__analysis_27Export）
- `tools/advertising/analysis-55.html` —「导出明细 CSV」（__analysis_55Export）
- `tools/agriculture/countdown-cycle.html` —「导出明细 CSV」（__countdown_cycleExport）
- `tools/agriculture/cycle-honey.html` —「📥 导出记录」（exportExtr）
- `tools/ai/ai-10.html` —「导出 CSV」（__b1Export）
- `tools/ai/ai-11.html` —「导出 CSV」（__abExport）
- `tools/ai/ai-12.html` —「导出 CSV」（__b2Export）
- `tools/ai/ai-13.html` —「导出 CSV」（__acExport）
- `tools/ai/ai-14.html` —「导出 CSV」（__b3Export）
- `tools/ai/ai-15.html` —「导出 CSV」（__adExport）
- `tools/ai/ai-16.html` —「导出 CSV」（__aeExport）
- `tools/ai/ai-17.html` —「导出 CSV」（__afExport）
- `tools/ai/ai-4.html` —「导出 CSV」（__a4Export）
- `tools/ai/ai-5.html` —「导出 CSV」（__a5Export）
- `tools/ai/ai-6.html` —「导出 CSV」（__a6Export）
- `tools/ai/ai-7.html` —「导出 CSV」（__a7Export）
- `tools/ai/ai-8.html` —「导出 CSV」（__a8Export）
- `tools/ai/ai-9.html` —「导出 CSV」（__a9Export）
- `tools/ai/ai-code-review.html` —「导出 CSV」（__crExport）
- `tools/ai/ai-prompt-generator.html` —「导出 CSV」（__pgExport）
- `tools/ai/ai.html` —「导出 CSV」（__b4Export）
- `tools/ai/attention-flops.html` —「导出 CSV」（__afExport）
- `tools/ai/attention-head-dim.html` —「导出 CSV」（__ahExport）
- `tools/ai/auc-rank.html` —「导出 CSV」（__arExport）
- `tools/ai/augmentation-multiplier.html` —「导出 CSV」（__b5Export）
- `tools/ai/cohens-kappa.html` —「导出 CSV」（__ckExport）
- `tools/ai/context-window.html` —「导出 CSV」（__cwExport）
- `tools/ai/best-epoch.html` —「导出 CSV」（__beExport）
- `tools/ai/cosine-similarity.html` —「导出 CSV」（__csExport）
- `tools/ai/cross-entropy.html` —「导出 CSV」（__ceExport）
- `tools/ai/dropout.html` —「导出 CSV」（__dpExport）
- `tools/ai/elbow-wcss.html` —「导出 CSV」（__ewExport）
- `tools/ai/epoch-time.html` —「导出 CSV」（__etExport）
- `tools/ai/flops.html` —「导出 CSV」（__flExport）
- `tools/ai/grad-accumulation.html` —「导出 CSV」（__gaExport）
- `tools/ai/inference-throughput.html` —「导出 CSV」（__itExport）
- `tools/ai/k-means.html` —「导出 CSV」（__kmExport）
- `tools/ai/l1-l2-regularization.html` —「导出 CSV」（__l1Export）
- `tools/ai/l1-l2.html` —「导出 CSV」（__l2Export）
- `tools/ai/lr-decay.html` —「导出 CSV」（__ldExport）
- `tools/ai/lr-warmup.html` —「导出 CSV」（__lwExport）
- `tools/ai/min-max.html` —「导出 CSV」（__mxExport）
- `tools/ai/model-accuracy.html` —「导出 CSV」（__maExport）
- `tools/ai/multi-agent-overhead.html` —「导出 CSV」（__moExport）
- `tools/ai/precision-recall.html` —「导出 CSV」（__prExport）
- `tools/ai/quantization-ratio.html` —「导出 CSV」（__qrExport）
- `tools/ai/rag.html` —「导出 CSV」（__rgExport）
- `tools/ai/relu-leakyrelu.html` —「导出 CSV」（__rlExport）
- `tools/ai/rmse.html` —「导出 CSV」（__rmExport）
- `tools/ai/roc-auc.html` —「导出 CSV」（__raExport）
- `tools/ai/sigmoid.html` —「导出 CSV」（__sgExport）
- `tools/ai/softmax-2.html` —「导出 CSV」（__s2Export）
- `tools/ai/softmax.html` —「导出 CSV」（__smExport）
- `tools/ai/specificity.html` —「导出 CSV」（__spExport）
- `tools/ai/steps-per-epoch.html` —「导出 CSV」（__seExport）
- `tools/ai/temperature-scaling.html` —「导出 CSV」（__tsExport）
- `tools/ai/training-flops.html` —「导出 CSV」（__tfExport）
- `tools/ai/transformer-params.html` —「导出 CSV」（__tpExport）
- `tools/ai/vram-estimate.html` —「导出 CSV」（__veExport）
- `tools/astronomy/convert-17.html` —「导出明细 CSV」（__convert_17Export）
- `tools/audio/audio-cut.html` —「⬇
导出 WAV」（exportSelection）
- `tools/audio/audio-echo.html` —「💾 导出 WAV」（exportWav）
- `tools/audio/audio-recorder.html` —「导出音频」（exportAudio）
- `tools/automotive/fuel-anomaly.html` —「💾 下载结果」
- `tools/automotive/lifespan-brake.html` —「导出明细 CSV」（__lifespan_brakeExport）
- `tools/beauty/aging-calculator.html` —「⬇️ 导出 TXT」
- `tools/biz/lorem-ipsum-advanced.html` —「导出明细 CSV」（__lorem_ipsum_advancedExport）
- `tools/biz/summary-rater-csat.html` —「导出明细 CSV」（__summary_rater_csatExport）
- `tools/biz/team-roster-generator.html` —「导出明细 CSV」（__team_roster_generatorExport）
- `tools/biz/text-compare.html` —「导出明细 CSV」（__text_compareExport）
- `tools/biz/text-extract-dates.html` —「导出明细 CSV」（__text_extract_datesExport）
- `tools/biz/text-extract-ips.html` —「导出明细 CSV」（__text_extract_ipsExport）
- `tools/biz/unicode-normalize.html` —「导出明细 CSV」（__unicode_normalizeExport）
- `tools/cardiology/has-bled.html` —「导出明细 CSV」（__has_bledExport）
- `tools/ceramics/glaze-temp.html` —「⬇️ 导出测温锥对照 CSV」
- `tools/chess/bridge-scoring.html` —「导出明细 CSV」（__bridge_scoringExport）
- `tools/chess/gomoku-forbidden.html` —「导出明细 CSV」（__gomoku_forbiddenExport）
- `tools/cleaning/appliance-cycle.html` —「导出明细 CSV」（__appliance_cycleExport）
- `tools/cleaning/cycle-20.html` —「⬇️ 导出养护排期 CSV」
- `tools/cleaning/staff-schedule.html` —「导出明细 CSV」（__staff_scheduleExport）
- `tools/clinical-lab/hba1c-converter.html` —「导出明细 CSV」（__hba1c_converterExport）
- `tools/clinical-lab/urinalysis-interpretation.html` —「⬇️ 导出 TXT」
- `tools/clinical-nursing/cycle-7.html` —「📥 导出记录」（exportData）
- `tools/clinical-nursing/pressure-injury-description.html` —「导出明细 CSV」（__pressure_injury_descriptionExport）
- `tools/clinical-nursing/reminder-time-1.html` —「📥 导出记录」（exportData）
- `tools/clinical-nursing/suction-pressure.html` —「导出明细 CSV」（__suction_pressureExport）
- `tools/cognition/cognitive-assessment.html` —「⬇️ 导出 TXT」
- `tools/cognition/schulte-table.html` —「⬇️ 导出训练记录 CSV」
- `tools/data/csv-analyzer.html` —「制表符导出数据分析」
- `tools/data/csv-json.html` —「导出明细 CSV」（__csv_jsonExport）
- `tools/data/data-cleaner.html` —「导出明细 CSV」（__data_cleanerExport）
- `tools/data/data-visualizer.html` —「导出明细 CSV」（__data_visualizerExport）
- `tools/data/yaml-json.html` —「导出明细 CSV」（__yaml_jsonExport）
- `tools/dentistry/sialography.html` —「导出明细 CSV」（__sialographyExport）
- `tools/dermatology/chilblain-grading.html` —「导出明细 CSV」（__chilblain_gradingExport）
- `tools/dermatology/hdss-hyperhidrosis.html` —「导出明细 CSV」（__hdss_hyperhidrosisExport）
- `tools/dermatology/pityriasis-rosea.html` —「导出明细 CSV」（__pityriasis_roseaExport）
- `tools/design/blueprint-grid.html` —「导出明细 CSV」（__blueprint_gridExport）
- `tools/design/checkerboard-generator.html` —「导出明细 CSV」（__checkerboard_generatorExport）
- `tools/design/dot-pattern.html` —「导出明细 CSV」（__dot_patternExport）
- `tools/design/gradient-from-color.html` —「导出明细 CSV」（__gradient_from_colorExport）
- `tools/design/grid-pattern.html` —「导出明细 CSV」（__grid_patternExport）
- `tools/design/image-cropper.html` —「导出明细 CSV」（__image_cropperExport）
- `tools/design/image-format-converter.html` —「导出转换汇总 CSV」（__ifcExport）
- `tools/design/image-rotator.html` —「下载」（downloadImg）
- `tools/design/image-rounded-corners.html` —「⬇ 下载 PNG」（downloadResult）
- `tools/design/image-to-ascii.html` —「下载 .txt」（downloadResult）
- `tools/design/iso-noise-reference.html` —「导出明细 CSV」（__iso_noise_referenceExport）
- `tools/design/isometric-grid.html` —「导出明细 CSV」（__isometric_gridExport）
- `tools/design/loading-dots.html` —「导出明细 CSV」（__loading_dotsExport）
- `tools/design/music-scale-reference.html` —「⬇️ 导出音阶 CSV」（msExportCsv）
- `tools/design/mesh-gradient.html` —「导出明细 CSV」（__mesh_gradientExport）
- `tools/design/pattern-generator.html` —「导出明细 CSV」（__pattern_generatorExport）
- `tools/design/qr-code-styled.html` —「下载」（downloadImg）
- `tools/design/signature-pad.html` —「⬇ 导出 PNG」（exportPNG）
- `tools/design/spectrum-visualizer.html` —「导出明细 CSV」（__spectrum_visualizerExport）
- `tools/design/spinner-generator.html` —「导出明细 CSV」（__spinner_generatorExport）
- `tools/design/stripe-pattern.html` —「导出明细 CSV」（__stripe_patternExport）
- `tools/design/svg-to-png.html` —「下载 PNG」（downloadPNG）
- `tools/design/tailwind-colors.html` —「⬇️ 导出色板清单 CSV」（__twExport）
- `tools/design/waveform-visualizer.html` —「导出明细 CSV」（__waveform_visualizerExport）
- `tools/ecommerce/cycle-15.html` —「导出数据」（exportData）
- `tools/ecommerce/report.html` —「导出明细 CSV」（__reportExport）
- `tools/edu/24-point-solver.html` —「导出明细 CSV」（__24_point_solverExport）
- `tools/edu/chinese-stroke-counter.html` —「导出明细 CSV」（__chinese_stroke_counterExport）
- `tools/edu/convert-1.html` —「导出明细 CSV」（__convert_1Export）
- `tools/edu/convert-3.html` —「导出明细 CSV」（__convert_3Export）
- `tools/edu/ebbinghaus-curve.html` —「导出明细 CSV」（__ebbinghaus_curveExport）
- `tools/edu/edu-unit-converter.html` —「导出明细 CSV」（__edu_unit_converterExport）
- `tools/edu/exam-gpa-calculator.html` —「⬇️ 导出成绩单 CSV」
- `tools/edu/exam-study-planner.html` —「📤 导出」（exportTasks）
- `tools/edu/pinyin-converter.html` —「导出明细 CSV」（__pinyin_converterExport）
- `tools/edu/reading-speed-calculator.html` —「导出明细 CSV」（__reading_speed_calculatorExport）
- `tools/edu2/wrong-book.html` —「导出明细 CSV」（__wrong_bookExport）
- `tools/elderly/bp-trend.html` —「导出明细 CSV」（__bp_trendExport）
- `tools/elderly/fall-risk.html` —「⬇️ 导出 TXT」
- `tools/elderly/reminder-time.html` —「📥 导出CSV」（exportSchedule）
- `tools/electrical/power-factor-compensation.html` —「导出明细 CSV」（__power_factor_compensationExport）
- `tools/encode/calc-1.html` —「导出明细 CSV」（__calc_1Export）
- `tools/encode/calc-2.html` —「导出明细 CSV」（__calc_2Export）
- `tools/encode/image-to-base64.html` —「下载图片」（downloadImg）
- `tools/endocrinology/cycle-hormone.html` —「⬇️ 导出 TXT」
- `tools/energy/stats-energy.html` —「导出明细 CSV」（__stats_energyExport）
- `tools/energy/water-tds-evaluator.html` —「导出明细 CSV」（__water_tds_evaluatorExport）
- `tools/ent/adenoid-grading.html` —「导出明细 CSV」（__adenoid_gradingExport）
- `tools/ent/tonsil-grading.html` —「导出明细 CSV」（__tonsil_gradingExport）
- `tools/fengshui/fengshui-calculator.html` —「导出明细 CSV」（__fengshui_calculatorExport）
- `tools/finance/compound-interest.html` —「↓ 导出结果」
- `tools/finance/dns-record-info.html` —「⬇️ 导出DNS记录 CSV」
- `tools/finance/gold-price-calculator.html` —「导出明细 CSV」（__gold_price_calculatorExport）
- `tools/finance/housing-fund-loan.html` —「导出明细 CSV」（__housing_fund_loanExport）
- `tools/finance/mortgage-calculator.html` —「↓ 导出结果」
- `tools/finance/number-to-words-chinese.html` —「导出明细 CSV」（__number_to_words_chineseExport）
- `tools/finance/number-to-words.html` —「导出明细 CSV」（__number_to_wordsExport）
- `tools/finance/password.html` —「导出明细 CSV」（__passwordExport）
- `tools/finance/sharpe-ratio.html` —「导出明细 CSV」（__sharpe_ratioExport）
- `tools/finance/register-depreciation.html` —「导出数据」（exportAssets）
- `tools/finance/tax-calculator.html` —「↓ 导出结果」
- `tools/finance/word-counter.html` —「↓ 导出结果」
- `tools/fishery/cycle-6.html` —「⬇️ 导出清淤计划 CSV」
- `tools/fitness/cycle-5.html` —「⬇️ 导出课程表 CSV」
- `tools/fitness/training-volume.html` —「导出明细 CSV」（__training_volumeExport）
- `tools/food/cooking-converter.html` —「导出明细 CSV」（__cooking_converterExport）
- `tools/food/food-pairing.html` —「导出明细 CSV」（__food_pairingExport）
- `tools/food/nutrition-calculator.html` —「⬇️ 导出营养明细 CSV」（__nutriExport）
- `tools/food/stats-ingredient.html` —「导出明细 CSV」（__stats_ingredientExport）
- `tools/food/stats-simulator-flavor.html` —「导出明细 CSV」（__stats_simulator_flavorExport）
- `tools/fun/1a2b-guess.html` —「⬇️ 导出 TXT」
- `tools/fun/keyboard-heatmap.html` —「导出明细 CSV」（__keyboard_heatmapExport）
- `tools/fun/typing-rhythm.html` —「导出明细 CSV」（__typing_rhythmExport）
- `tools/fun/word-scramble.html` —「导出明细 CSV」（__word_scrambleExport）
- `tools/funeral/funeral-budget-planner.html` —「导出明细 CSV」（__funeral_budget_plannerExport）
- `tools/funeral/reminder-3.html` —「导出明细 CSV」（__reminder_3Export）
- `tools/gardening/pest-identifier.html` —「导出明细 CSV」（__pest_identifierExport）
- `tools/gardening/reminder-cycle-succulent.html` —「导出明细 CSV」（__reminder_cycle_succulentExport）
- `tools/general/convert-21.html` —「导出明细 CSV」（__convert_21Export）
- `tools/geology/analysis-33.html` —「导出明细 CSV」（__analysis_33Export）
- `tools/health/calorie-needs.html` —「导出明细 CSV」（__calorie_needsExport）
- `tools/health/milk-tea-calories.html` —「导出明细 CSV」（__milk_tea_caloriesExport）
- `tools/health/rehab-timer.html` —「导出明细 CSV」（__rehab_timerExport）
- `tools/health/symptom-checker.html` —「导出明细 CSV」（__symptom_checkerExport）
- `tools/hematology/leukemia-classification.html` —「导出明细 CSV」（__leukemia_classificationExport）
- `tools/home/furniture-layout.html` —「📥 导出」（exportLayout）
- `tools/home/renovation-budget.html` —「📥 导出」（exportBudget）
- `tools/hydraulic/cycle-19.html` —「⬇️ 导出维护排程 CSV」
- `tools/image/id-photo-crop.html` —「下载」（download）
- `tools/image/image-collage.html` —「↓ 导出结果」
- `tools/image/nine-grid-cutter.html` —「全部下载」（downloadAll）
- `tools/image/image-compress.html` —「⬇️ 导出 TXT」
- `tools/it/affine-cipher.html` —「导出明细 CSV」（__affine_cipherExport）
- `tools/it/ast-viewer.html` —「模块导入导出」
- `tools/it/barcode-ean.html` —「下载 PNG」（downloadBarcodePNG）
- `tools/it/barcode-upc.html` —「下载 PNG」（downloadBarcodePNG）
- `tools/it/calc-10.html` —「导出明细 CSV」（__calc_10Export）
- `tools/it/captcha-generator.html` —「导出明细 CSV」（__captcha_generatorExport）
- …… 其余 152 页见 JSON


## 定向复扫用法

```bash
# 单页复扫
node scripts/runtime_scan.js --interact --only tools/it/whitespace.html --timeout 10000
# 单分类/目录复扫（尾部斜杠=整个目录）
node scripts/runtime_scan.js --interact --only tools/accounting/ --timeout 10000 --concurrency 8
# 通配符 / 多个目标（逗号分隔）
node scripts/runtime_scan.js --interact --only "tools/it/*.html,tools/ai/ai-1*.html"
# 按清单复扫（每行一个相对路径）
node scripts/runtime_scan.js --interact --files /tmp/pages.txt --timeout 10000
```

> 定向复扫会强制重扫命中页，其余记录原样保留，并在结束时自动重算本报告与 JSON；不要与 `--resume` 混用。
> 全量原始数据：`scripts/out/interaction-invalid.jsonl`（逐行、4916 条）与 `scripts/out/interaction-invalid.json`（8 MB），均被 `.gitignore` 忽略，只留本地。
> 精简摘要（401 个高/中置信页）：`plan/interaction-invalid-top100.json`。

## 2026-11-05 口径重定义与 5 页处置

### 判据（旧 653 清单作废，逐页结果见 `/private/tmp/notclicked-653-classified.json`）
- **A 真需点击**（新入桶，三条同时成立）：① 页面无主按钮；② 逐字段改值（不是只改第一个输入）结果签名不变；③ 有文本/数字输入。
- **B 已可改值**；**C 误判**（纯 select 97 / 文件输入 10 / 画布 6）；**D 无文本输入**（D-a 需预设·示例·表格切换 67，D-b 无任何可驱动 1）。
- 653 = A 23 / B 449 / C 113 / D 68。旧 322 条 `changedByInput=true` 中 288 仍为 B、26 实为纯 select、3 含文件输入、5 实为 D-a——旧探针把 select 改动也算作「改值即变」。

### 探针修正
- 注入前按 `type/min/max/step/pattern` 规整值（hex/cmyk/time/date/url/csv 各自合法化）；`file` 输入整页排除；结果签名追加 canvas `toDataURL` 尾段与 svg outerHTML 哈希（图形页不取 textContent）；结果区 fallback 只取非 `header/nav/footer` 的 `.container`，并排除 `.tb-*` 等全局组件。
- 已知盲区（D-a 中 6 页非缺陷）：`fun/keyboard-heatmap`（单次 keyup 不累积）、`science/wire-gauge-converter`（越界注入）、`funeral/ceremony-timeline`（空列表）、`fitness/training-volume`、`rehabilitation/assistive-device-fitting`（需先添加实体）、`edu/english-vocabulary`（需先开始测试）。

### 5 页真问题处置
- `neurology/ncs-emg`：9 项检查加「未选择」默认项；`unselected>0` 时只输出「待检查：还有 N 项未选择」，**不渲染诊断/建议/门诊记录**。
- `usedcar/detector-19`：14 项加「未检查（请选择）」默认项；`unchecked>0` 时只输出「待检测：还有 N 项未检查」，**不输出风险指数/结论/购买建议**；CSV 导出同步标注未检查项、结论改为「待检测」。
- `fluid/buoyancy-force` 与 `process` 13 页同型：数字输入补 `oninput`，保留「计算」按钮。
- `pet-training/clicker-timing`：**不改，审计结论作废**。`duration` 已有 `oninput="updateSettings()"`，且 `scheduleNext()` 每回合实时读取 `duration`；训练型工具，改设置本就不应改写已完成回合的统计，属正确设计。

## 2026-11-05 分桶抽样复核（60 页）：不销账

### 抽样口径
- 分层按桶比例抽 60 页（占 653 的 9.2%，覆盖 42 个行业）：A 5/23、B 30/449、C 15/113（13 纯 select + 1 文件 + 1 画布）、D 10/68（9 D-a + 唯一 D-b）。
- 抽样种子：`sha1(页面路径)` + 按行业轮转，排除人工挑选；清单落 `/tmp/probe_bucket_sample.md`，逐页证据与判定落 `/tmp/probe_bucket_verdict.md`。
- 方法：① 官方探针 `runtime_scan.js --interact` 对 60 页当天跑 2 次（`changedByInput` / 点击按钮两次结果 60/60 一致，探针本身可复现）；② 独立真机 puppeteer 采证，同页全量可见文本对比（排除控件值、计入只读输出），逐字段改值 + 填不同值后逐按钮点击；③ 按 §8「批跑口径 vs 隔离口径」，本批为隔离复跑，结论可作验收依据。

### 结果：桶位错分 5/60 = 8.3%（Wilson 95% CI 3.6%–18.1%）→ ≥5%，不销账
| 页面 | 原桶 | 实测 | 错因 |
|---|---|---|---|
| `library/clc-classifier` | C（纯 select） | **B**（`search` 输入即过滤，搜索结果条数变化） | 搜索框未计入文本驱动，且探针结果区未覆盖列表区 |
| `metalwork/thread-spec` | C（纯 select） | **B**（`search` 输入即过滤表格） | 同上 |
| `rehabilitation/assistive-device-fitting` | D-a（需预设） | **B**（5 个数值全填后，任一改动即刷新适配结果；judge 5/5） | 只改一个字段、其余留空 → 判「改值不变」 |
| `design/shutter-speed-calculator` | D-a（需预设） | **B**（`focal` `oninput=calc()`，实测 50→103 使结果 1/15→1/30） | 固定 0.8× 改值撞上标准快门档位四舍五入，判「不变」 |
| `kids/multiplication-practice` | D-a（需预设） | **C**（`modeSel`/`timeSel` 切换即换题） | select 驱动未计，D 判据「无文本输入」与事实不符 |

另 5 页**桶位正确、子类标签错**（不计入 8.3%，但文案需修）：`cleaning/appliance-cycle`、`life/holiday-calendar`（实为按钮）、`textile/colorfastness`（`type=color`）、`music/piano-keyboard`（复选/按钮）——均被写成「纯 select/无文本」；`medical/reminder-2` 记 D-b「无任何可驱动交互」，但填表后「➕ 添加药品」成功新增 1 行（药品总数 1），应为 D-a。

### 探针盲区（本次全部复现，需改判定再重扫）
1. **只改一个字段**：多输入页需全填才出结果（`assistive-device-fitting`），单字段改值必判「不变」。修法：先全字段填合法值，再逐字段改值并合并判定（即 `changedAll`，不能再用单字段 `changedByInput`）。
2. **结果区漏列表/过滤区**：`search` 类页（`clc-classifier`、`thread-spec`、`tailwind-colors`、`64-gua`）改值确实过滤列表，但探针只比结果区签名。修法：签名改为全量可见文本（排除控件值），并对 `type=search` 单独判定。
3. **固定倍率改值**：0.8× 可能落在同一档位（`shutter-speed-calculator`）。修法：每个字段至少注入 2 个差异较大的合法值，任一变化即判「变」。
4. **select 驱动未纳入**：`multiplication-practice` 等纯 select 交互页仍被塞进 D。修法：D 判据改为「无 select/文件/画布可改变结果」，select 驱动归 C。
5. **D-b 未走「填表→点添加」流程**：`reminder-2` 被误判为无交互。修法：D-b 前必须试跑一次新增实体全流程。
6. **判据文案与数据自相矛盾**：A 判据写「页面无主按钮」，但 A 23 页 `primaryButton` 全部非空（18 页为「计算」）；D 判据写「无文本输入」，但 D 68 页 `textInputs` 为 1–6。实际规则是「A=改值不变+有主按钮」「D=改值不变+其他按钮可驱动」，文案需按此改写，否则后续按错误口径复核。
7. **同名字段口径不同**：分桶 JSON 的 `changedByInput` 与官方探针字段在 14/60 页取值不一致（而官方探针两次自跑 60/60 一致）——分桶不是官方探针的产物，字段不可混用；B=449 中可能混入搜索/多字段页，需按新口径重扫。

### 已知盲区专项确认
- `prompt/confirm/alert` 桩：样本 13 页含对话框调用，全部位于删除/清空/校验分支，常规改值路径不触发，**未造成分桶误判**；`cycle-honey` 的 `prompt` 需先有蜂箱，属 D-a 而非对话框问题。
- `addEventListener` 漏检：探针仍漏（搜索类页），但本批独立采证用真实事件驱动可正常捕获，说明漏检在探针的「结果区选取」，不在事件注入。
- 重渲染冲掉输入：**真实存在 2 例**（不计入分桶，独立缺陷）：`medical2/surgery-duration` 选术式后 `select` 被重渲染清空、`clinical-nursing/reminder-time-1` 的 `noteInput` 输入后被清空。

### 结论
653 页分桶**不销账**：桶位错分 8.3%（CI 上限 18.1%），且 B 桶依赖的单字段 `changedByInput` 在多输入/搜索/select 页系统性失真。先按上列 7 条修探针，重扫 653 后再抽 60 页复核；本批 60/60 页均**不是**「not-clicked 真缺陷」，但 5 页桶位与 5 页子类仍需修正。

### 独立工作树续审检查点（基线 0781ef7e61）
- 探针七项修正已合入 `master`（提交 `5a140de940`）；历史 653 页新口径重扫曾中断，未找到完整新分桶及旧→新迁移矩阵。历史独立 60 页虽有采证，但缺可逐页复核的最终裁决，不能按其口头结果销账。
- 在 `audit/interaction-review` 工作树对原 60 页样本连续运行现有探针两次：均有效 60 页、错误 0；两次桶位分布均为 B 41、C 12、D-a 7，逐页桶位一致 60/60。结果见 `/tmp/toolbox-audit-sample60-a.json` 和 `/tmp/toolbox-audit-sample60-b.json`。本结果只证明桶位可复现，**不证明人工真机判定准确**；历史部分页面在当前基线已有变更，不能直接用旧人工裁决计算现状错分率。
- 历史五个错分案例本次探针分别为：`library/clc-classifier` B、`metalwork/thread-spec` B、`rehabilitation/assistive-device-fitting` B、`design/shutter-speed-calculator` B、`kids/multiplication-practice` C，与历史人工桶位相同；当前基线尚未做独立人工真机复核。
- 待办：固定工作树 commit 与 653 页原始名单，分批重扫并补齐错误页；严格校验两次运行页集合与错误数，再生成迁移矩阵；从新桶位中抽取与旧样本不重叠的 60 页，逐页记录独立真机裁决后再决定是否销账。
## 2026-11-05 A 桶 9 页收口 + 两个异常数值核实

### A 桶 9 页（补实时绑定，保留原按钮）
| 页面 | 处理 |
|---|---|
| `fluid/chezy-velocity`、`capillary-rise`、`capillary-pressure`、`cavitation-number` | 全部 `type="number"` 补 `oninput="calcTool()"` |
| `printing/estimate-ink` | 单色/CMYK 全部数字输入补 `oninput="__inkLive(...)"`，勾选补 `onchange`；**250ms 防抖 + 实时态不写历史**（`calcSingle/calcCmyk` 增 `live` 参数），避免逐键刷屏历史记录 |
| `biz/text-compare` | 两个 `textarea` 补 `oninput`、三个选项补 `onchange`；**250ms 防抖**——`compare()` 是 O(m×n) LCS，长文本逐键直跑会卡顿 |
| `clinical-nursing/reminder-time-1` | 三个时长补 `oninput`；新增 `#planPreview` 方案预览行（冷敷/休息/检查间隔），运行中（`state.running`）不覆盖计时器状态 |
| `edu/exam-study-planner` | 番茄钟 3 项配置补 `oninput` + 新增 `#pomo-plan` 计划行；**任务表单（subject/content/minutes）保持按钮驱动**——那是「添加记录」CRUD，不可预览 |
| `tcm-diagnosis/ten-questions` | 表单区事件委托（`input`/`change`）→ **300ms 防抖**调用 `generate(true)` 静默生成（不弹 toast），姓名/年龄/性别/10 问全部实时出记录 |

> 以上九页默认态均为「未输入/默认参数」，键入后结果区即变；按钮仍保留且点击结果与键入一致。

### 两个异常数值核实
- **`process/rolled-throughput-yield` 764.46% 不是公式错**：RTY=ΠFPY 累乘正确。探针把三工序良率按「默认值×2+1」注成 197/195/199（本身已 >100%，物理不可能），1.97×1.95×1.99=7.6446。**真缺陷是缺上限校验 + 旧预置/旧用例把越界值当正常**：
  - 新增 `>100%` 拦截（只提示「工序良率不能超过 100%」并清空结果表，图表同步不画）；
  - 预置「示例 2×/0.5×」换成「高良率 99.5/99/98.5」「低良率 92/90/95」；
  - 旧 verify 用例 `y1=147 → 期待 141.16%` 已改成 `y1=97 → 93.15%`，另补单字段（y1=95 → 91.23%）与越界（y1=120 → 提示）两例。
- **`process/cpk-with-shift` −0.307 是真实结果，非符号错**：Cpk=min[(USL−μ)/3σ,(μ−LSL)/3σ]，当位移后 μ 超出规格上限时下侧分量为负，Cpk 本就可为负（表示过程中心已在规格外）。该数值来自探针把 `shift` 注成 1.04（远超 0.2 的规格宽度、μ=22.04 > USL=21.1）。默认位移 0.02 时 Cpk 为正值，页面无需改动。

### 用例与判别
- 新增/修正条数：biz 148→149、clinical-nursing 44→45、edu 88→89（含修正 1 条旧自动用例的连续序列期待）、fluid 46→50、printing 9→10、tcm-diagnosis 20→21、process 14→16。
- 判别四项（`discriminate_check.js`，逐文件）：已检=正确变红，逃生项 0，跳过 0（biz 149 / nursing 45 / edu 89 / fluid 50 / printing 10 / tcm 21 / process 16）。

## 2026-11-05 it/*-escape 家族 10 页实时绑定 + 5 页裁定 + 6 页探针盲区

### 10 页统一改法（保留原「转义 ↑」按钮）
- `<textarea id="input">` 加 `oninput="__escLive()"`；勾选项（`unicode` / `quoteSingle` 等）加 `onchange="__escLive()"`。
- `esc()` 增加 `live` 参数：空值时实时态只清空输出、不弹 `alert`；按钮态保持原提示。
- 新增 `__escLiveMode` 标志，`__<slug>Extras()` 首行 `if (__escLiveMode) return;` —— 逐键实时只刷新输出，历史记录仍由按钮写入。

真机三态（注入 `a"b\c`，再点「转义 ↑」）：

| 页面 | 默认输出 | 键入后 | 点击后 |
|---|---|---|---|
| `it/c-string-escape` | `"Hello \"World\""` | `"a\"b\\c"` | 同键入 |
| `it/css-escape` | `my\.class` | `a\"b\\c` | 同键入 |
| `it/go-escape` | `"Hello \"World\""` | `"a\"b\\c"` | 同键入 |
| `it/java-escape` | `"Hello \"World\""` | `"a\"b\\c"` | 同键入 |
| `it/js-escape` | `"Hello \"World\""` | `"a\"b\\c"` | 同键入 |
| `it/php-escape` | `'Hello "World"'` | `'a"b\\c'` | 同键入 |
| `it/python-escape` | `"Hello \"World\""` | `"a\"b\\c"` | 同键入 |
| `it/regex-escape` | `Hello \(World\)\? \[a-z\]\+ \$19\.99` | `a"b\\c` | 同键入 |
| `it/rust-escape` | `""` | `"a\"b\\c"` | 同键入 |
| `it/sql-escape` | `Hello \"World\"` | `a\"b\\c` | 同键入 |

10/10 `changedByInput=true`、`clickSameAsType=true`（`regex-escape` 曾误点到「等号转义」，按精确文本 `转义 ↑` 复测后同键入）。

### 旧期望 → 新期望（因修页面而失效）
| 用例 | 旧期望 | 新期望 | 原因 |
|---|---|---|---|
| `it/rust-escape`（自动补强 B 类零用例） | `1 2 3\n1 2 3\nchar` | `1 2 3\nchar\n1 2 3`（旧序保留为备选） | 加 `__escLive` 后 harness fallback 调函数序改变 |

本批未发现「用例固化错误行为」的条目：escape 家族旧用例均为按钮驱动，期望值是真实转义结果。

### 5 页裁定（均不改页面）
| 页面 | 结论 | 依据 |
|---|---|---|
| `office/mindmap` | 已有实时绑定，不改 | `editor.addEventListener('input', __mmPaint)` + 300ms `renderDebounced()`；探针 `boundInline` 只认 inline `oninput` 属性，故漏检 |
| `yi/yi-divination` | 显式动作合理，不改 | 起卦是一次性随机仪式，实时随输入重算会破坏「起卦」语义 |
| `security/emergency-contacts` | 显式动作合理，不改 | 三字段 + 「添加联系人」是 CRUD 写入列表，逐键建条目会污染列表/导出 |
| `ophthalmology/astigmatism-chart` | 已有实时绑定，不改 | 4 个 `select` 的 `change` 与 `asNote` 的 `input` 均已绑定（`render()` 重绘 canvas）；文本快照抓不到 |
| `data/data-cleaner` | 显式动作合理，不改 | 操作项 `toggleOp()` 已即调 `clean()`；文本输入保留「清洗」按钮——含「随机打乱」，实时重算会致输出抖动、导出不稳定 |

### 6 页「已有实时绑定」探针盲区（不改页面，实测注入均变）
| 页面 | 盲区原因 | 实测 |
|---|---|---|
| `rehabilitation/assistive-device-fitting` | 结果需多字段齐备，单字段注入停留在缺项提示「请输入身高、体重和臀宽」 | 5 字段齐派发 → 输出成立 |
| `science/wire-gauge-converter` | 三种模式输入互斥，非当前模式 `display:none`，需先切 radio | `awg` 24→18 → 输出变化 |
| `geology/mineral-hardness` | 输出取「最近标准矿物」，注入相邻值可能仍映射同一档 | 默认 6、注入 6.5 仍正长石 6（文本不变）；注入 8 → 黄玉 8 |
| `design/css-border-radius` | 变更落在 `.shape-preview` 的 `style.borderRadius`（无文本节点），文本比对抓不到 | 20px → 60px |
| `biz/text-case-advanced` | `oninput="updatePreview()"` 是空实现；转换类型须由按钮指定（20+ 种），实时无法唯一确定 → 属「一次性前置」 | 注入后 preview 仍为「点击下方按钮进行转换...」 |
| `design/shutter-speed-calculator` | 输出快门按标准档位取整，相邻焦距落在同一档 | 50→200mm：`1/15` → `1/60` |

### 门禁
- `scripts/verify_it_calc.js`：999/999 通过。
- `discriminate_check.js verify_it_calc.js`：已检 999 / 正确变红 999 / 逃生 0 / 跳过 0。

## 2026-11-05 rust-escape 用例真机复核 + 逐字段交互探针

### rust-escape 旧用例作废（用例层面假绿）
- 旧用例 `inputs` 为 `{input:"1\n2\n3", output:"1\n2\n3", kind:"char"}`，期望 `1 2 3\nchar\n1 2 3`；桩 `fullBlob` 与期望逐字相同，实为 **input.value + kind.value + output.value 三个注入值的回显**。
- 真机同输入：`char` 只接受单个 Unicode 标量，弹「char 字面量只能包含一个字符（当前 5 个）」，`#output` 保持为空。页面没有产出该期望串。
- 新用例锚定真机：`kind=string`、`input=a"b` ⇒ 真机输出 `"a\"b"`；默认空输入不命中（强判别）。

### 实时绑定连带缺陷（go / rust，本批修复）
- `go-escape` 的 rune 校验、`rust-escape` 的 char / byte 校验位于实时路径上：逐键输入中途必然命中，原实现 `return alert(...)` ⇒ **每按一键弹一次**；按钮模式拦截时还会残留上一次结果。
- 改为：命中即先清空 `#output`；`live` 态直接返回不弹窗，按钮态仍弹提示。
- 真机复测：rust char `1\n2\n3` → 输出空、0 弹窗；char `é` → `'\u{e9}'`；string `a"b` → `"a\"b"`；go rune `ab` → 输出空、0 弹窗；rune `é` → `'é'`。

### 新探针 `scripts/interaction_probe.js`（纯只读）
- **逐字段**注入（每个文本/数字/日期/select 单独注入并恢复）+ 全量注入，不再只改第一个输入。
- 识别三种绑定：inline `on*` 属性、`addEventListener(...)`、页面末尾直接调用渲染函数（`render()/init()/update()...`）。
- 结果签名三类组合：主容器文本（含 readonly textarea 值）+ 全部 `canvas.toDataURL()` 哈希 + 全部 `svg` outerHTML 哈希。
- 结构化输出 `{bindings, changedByField, changedAll, needsClick, emptyState, clickTargets}`，可并入 `plan/page-ledger.json`；支持 `--file` / `--dir` / `--limit` / `--out` / `--timeout` / `--port`。
- 口径细节：排除站点 chrome（header/nav/footer/`.tb-*`/`.nav-menu`）与结果框、搜索框、语言选择；点击探测**保持全量注入态**（否则起卦/清洗类会被「请输入」守卫挡掉，得到 `needsClick=false` 假结论）；点击后轮询 2s 以覆盖起卦动画与 300ms 防抖。
- 三页自检（与人工裁定一致）：
  - `office/mindmap`：`changedAll=true`、`needsClick=false`、`listeners=input` + `autoRender=render` ⇒ 已实时。
  - `yi/yi-divination`：`changedAll=false`、`needsClick=true`（🙏 起卦演示）⇒ 需按钮。
  - `data/data-cleaner`：`changedAll=false`、`needsClick=true`（🔎 清洗）；chip「去首尾空白」点击亦变化 ⇒ 操作项实时、文本需按钮。

### 门禁
- `scripts/verify_it_calc.js`：999/999 通过。
- `discriminate_check.js verify_it_calc.js`：已检 999 / 正确变红 999 / 逃生 0 / 跳过 0。
