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
- 静态续审第六批：阅读 `funeral/{ceremony-timeline,funeral-budget-planner,reminder-3}`、`gardening/reminder-cycle-succulent`、`health/{breath-timer,rehab-timer}` 共 6 页主要状态和交互路径，记录日期、排程与计时问题；未做浏览器验证，不计双跑。
- 静态续审第七批：阅读 `healthcare/heart-rate-zones`、`hematology/leukemia-classification`、`home/{furniture-layout,renovation-budget}`、`hotel/tip-calculator`、`hydraulic/cycle-19` 共 6 页的主要状态和交互路径，记录心率区间、预算一致性、复制金额及维护记录问题。白血病分型资料未做医学专业核验；均未做浏览器验证，不计双跑。
- 静态续审第八批：阅读 `it/{area-code-lookup,ascii-table,box-shadow-generator,c-string-escape,calc-1,calc-10}` 共 6 页主要交互路径，记录原始输入 HTML 注入点、转义交互和异常，并注明历史 C 转义问题源码状态变化；未运行注入或浏览器，不计双跑。
- 静态续审第九批：阅读 `it/{calc-3,calc-4,calc-5,calc-8,case-converter,chmod-calculator}` 共 6 页主要交互路径，记录随机颜色、CSS 基准、JWT 时间与历史存储、权限历史恢复问题；旧 Title Case 条目现源码已变更。未运行页面，不计双跑。
- 静态续审第十批：阅读 `it/{color-converter,country-code-lookup,country-flag,cpp-cheatsheet,csharp-cheatsheet,css-escape}` 共 6 页主要路径，记录查询输入 HTML 注入点、颜色对比及 CSS 转义问题，更新旧结论源码状态；未运行页面或注入，不计双跑。
- 静态续审第十一批：阅读 `it/{css-properties,csv-to-html-table,docker-cheatsheet,emacs-cheatsheet,email-normalizer,emoji-cheatsheet}` 共 6 页主要路径，记录邮箱域名误判与历史恢复；CSV 旧问题当前关键路径仍在。仅代码分析及 Node 正则复算，不计双跑。
- 静态续审第十二批：阅读 `it/{emoji-meaning,env-generator,git-commands,go-cheatsheet,go-escape,html-tags}` 共 6 页主要路径，记录表情复制、HTML 标签 CSV 和环境变量预览问题；更正旧 env 与 Go 八进制条目的源码状态。仅代码分析及 Node 表达式复算，不计双跑。
- 静态续审第十三批：阅读 `it/{http-cache,http-cookies,http-headers,http-methods,http-response-headers,http-status}` 共 6 页检索、分类、复制及图表/导出路径；记录状态码导出后的表格状态，既有缓存统计、错误响应头及 Cookie 示例问题的相关代码仍在。未运行浏览器，不计双跑。
- 静态续审第十四批：阅读 `it/{java-cheatsheet,java-escape,js-escape,js-minifier,kubernetes-cheatsheet,language-code-lookup}` 6 页主要交互路径，记录原始输入 HTML 注入点、简化器字符串破坏与旧输出、转义错误处理；Node 抽取简化器原函数复算，未使用浏览器，不计双跑。
- 静态续审第十五批：阅读 `it/{less-compiler,linux-cheatsheet,locale-lookup,markdown-editor,mongodb-cheatsheet,msisdn-lookup}` 6 页主要交互路径，记录 locale 输入 HTML 注入点、Markdown 文本误触数值守卫及 Less 异步竞态；旧 Markdown 属性注入代码已变，待安全回归。纯源码结论，未运行页面或竞态，不计双跑。
- 静态续审第十六批：阅读 `it/{mysql-cheatsheet,nginx-cheatsheet,number-base-converter,password-strength,php-cheatsheet,php-escape}` 6 页主要路径；记录 PHP 不完整 Unicode 转义的索引死循环和模式刷新缺口，进制转换旧实现已变化待回归。Node 仅复算索引与解析值，未运行循环或浏览器，不计双跑。
- 静态续审第十七批：阅读 `it/{pomodoro,postgresql-cheatsheet,python-cheatsheet,python-escape,redis-cheatsheet,regex-cheatsheet}` 6 页主要路径；记录 Python 反转义前缀、码点错误和选项不刷新，番茄钟既有关键路径仍在。未运行浏览器，不计双跑。
- 静态续审第十八批：阅读 `it/{regex-escape,rest-api-cheatsheet,robots-txt-generator,ruby-cheatsheet,rust-cheatsheet,rust-escape}` 6 页主要交互路径；记录 robots 重建注入点与文本误触守卫、Rust 反转义潜在死循环及模式刷新，更新部分历史源码状态。仅静态分析，未运行浏览器或死循环，不计双跑。
- 静态续审第十九批：阅读 `it/{sql-cheatsheet,sql-escape,sqlite-cheatsheet,string-obfuscator,text-statistics,tmux-cheatsheet}` 6 页主要路径；记录 SQL 方言刷新和反转义空白、词频原型属性及总词数口径问题。仅静态分析，未运行浏览器，不计双跑。
- 静态续审第二十批：阅读 `it/{typescript-cheatsheet,typescript-compiler,unicode-lookup,vim-cheatsheet}`、`jewelry/gem-hardness`、`kids/mirror-letter` 6 页主要路径；记录编译器缺库与旧输出、宝石复制筛选、儿童游戏可区分性及定时器问题。仅静态分析，视觉效果和运行结果待验证，不计双跑。
- 静态续审第二十一批：阅读 `kids/multiplication-practice`、`language/{phrase-translator,text-polisher}`、`legal/{calendar,contract-templates}`、`library/clc-classifier` 6 页；记录计分定时器、旧润色结果和农历边界问题，更新历史源码状态。仅静态分析，未运行页面或专业核验，不计双跑。
- 静态续审第二十二批：阅读 `life/{bill-splitter,color-name-finder,cycle-4,cycle-pruning-lawn,data-unit-converter,event-countdown}` 6 页主要输入及输出路径；记录单位输入 HTML 注入、逐项分摊遗漏和状态丢失，更新颜色及草坪历史结论的源码状态；数据单位历史恢复及用品预设覆盖的旧代码仍在。仅静态分析，未运行浏览器或注入，不计双跑。
- 静态续审第二十三批：阅读 `life/{holiday-calendar,number-to-chinese,phone-lookup,reminder-cycle,roman-numeral}` 与 `marketing/email-subject-line-tester` 共 6 页；记录金额精度与大小写、罗马拆解空态及邮件空态示例表格问题，更新历史源码状态。仅静态分析，未运行浏览器，不计双跑。
- 静态续审第二十四批：阅读 `marketing/{funnel-calculator,marketing-ab-test-significance,marketing-ad-budget-allocator,marketing-break-even-roas,marketing-cac-calculator,marketing-chinese-hashtag-generator}` 6 页；记录话题输入 HTML/脚本注入风险、零分母、历史保存校验不一致和 A/B 转化范围问题，更新历史结论源码状态。仅静态分析，未运行页面或注入，不计双跑。
- 静态续审第二十五批：阅读 `marketing/{marketing-churn-rate,marketing-conversion-rate-calculator,marketing-coupon-discount,marketing-cpa-calculator,marketing-cpm-calculator,marketing-discount-rate}` 6 页；记录历史保存校验、空值和零成本边界问题，更新历史结论源码状态。仅静态分析，未运行浏览器，不计双跑。
- 静态续审第二十六批：阅读 `marketing/{marketing-engagement-rate,marketing-free-shipping-threshold,marketing-google-ads-budget,marketing-influencer-pricing,marketing-keyword-density,marketing-ltv-cac-ratio}` 6 页；记录空值和零分母误判，更新旧结论源码状态。仅静态分析，未运行浏览器，不计双跑。
- 静态续审第二十七批：阅读 `marketing/{marketing-ltv-calculator,marketing-nps-calculator,marketing-price-elasticity,marketing-qr-campaign-tracker,marketing-roas-calculator,marketing-sales-funnel,marketing-utm-builder,social-media-image-sizes}` 8 页，记录空值、分母与链接片段问题，核对历史条目关键代码变化。至清单第 443 页，静态续审累计 163 页；仅源码分析，未运行浏览器，不计双跑。
- 静态续审第二十八批：阅读 `marketing/xiaohongshu-counter`、`martial/{routine-timer,strike-resistance}`、`math/{complex-number,formula-calculator}`、`medical/{clinical-tools,drug-info,reminder-2}` 8 页，记录旧结果、默认值、时区和医疗建议等代码风险，更新历史条目关键代码状态。至清单第 451 页，静态续审累计 171 页；仅源码分析，未运行浏览器或专业核验，不计双跑。
- 静态续审第二十九批：阅读 `medical2/{drug-expiry,surgery-duration}`、`metalwork/{recorder-9,thread-spec}`、`meteorology/cloud-identify`、`museum/{era-comparator,historical-calendar,showcase-monitor}` 8 页，记录效期清理、空值、目标温度、历法及评估口径问题，核对旧条目关键代码。至清单第 459 页，静态续审累计 179 页；仅静态分析，未运行浏览器或专业核验，不计双跑。
- 静态续审第三十批：阅读 `music/{music-player,music-theory,piano-keyboard,rhythm-trainer}`、`nutrition/food-calorie-lookup`、`obstetrics/cycle-8`、`office/{excel-formula-reference,mindmap}` 8 页，记录录音回放、训练停止、循环状态、历史导出、离线降级及跨周期最新记录问题，修正旧营养条目对历史表状态的表述。至清单第 467 页，静态续审累计 187 页；仅源码分析，未运行浏览器、音频或医学专业核验，不计双跑。
- 静态续审第三十一批：阅读 `ophthalmology/{amsler-grid-test,astigmatism-chart,axial-length,cd-ratio,eye-chart-toolkit,iol-power,iop-correction,oct-rnfl}` 8 页，记录视标尺寸量级、用户输入 HTML 注入、标记与眼别状态、校验及输出矛盾等问题，并更新 IOL 旧结论的源码状态。至清单第 475 页，静态续审累计 195 页；仅源码分析，未运行浏览器或医学专业核验，不计双跑。
- 静态续审第三十二批：阅读 `ophthalmology/{refraction-error,strabismus-angle,tear-breakup-time,vision-screening-21,visual-field-analysis}` 与 `optical/{accommodation-amplitude,anti-fatigue-design}` 共 7 页，记录换算量级、历史恢复、空值与计算条件等问题；医学模型及阈值须专业复核。至清单第 482 页，静态续审累计 202 页；未运行浏览器，不计双跑。
- 静态续审第三十三批：阅读 `optical/{blue-light-filter,coating-design,convergence-near-point,edge-bevel,frame-pupillary,frame-tilt,lens-refractive-index,peripheral-defocus}` 8 页，记录空值兜底、正负镜边厚、集合和离焦结论冲突及静态图层状态等问题；专业结论须复核。至清单第 490 页，静态续审累计 210 页；仅源码分析，未运行浏览器，不计双跑。
- 静态续审第三十四批：阅读 `optical/{photochromic-lens,polarized-axis,polarized-stress,prism-decentration,progressive-corridor,tinted-lens}` 6 页，记录空值、色序表错位、未使用轴位、模式语义和方案替换等问题；专业结论须复核。至清单第 496 页，静态续审累计 216 页；仅源码分析，未运行浏览器，不计双跑。
- 静态续审第三十五批：阅读 `paper/{basis-weight,paper-grade,roll-length}`、`pediatrics/vaccine-schedule`、`pet-training/{clicker-timing,command-repetition,elimination-predict,leash-length}` 8 页，记录疫苗时间状态、纸张复制换算、宠物排便算式及计时状态等问题。至清单第 504 页，静态续审累计 224 页；仅源码及 Node 算式复算，专业建议须复核，未运行浏览器，不计双跑。
- 静态续审第三十六批：阅读 `pet-training/treat-calories`、`pet/reminder-vaccine-deworming`、`petrochem/{api-gravity,catalyst-calc}`、`photo/{equivalent-focal,ev,exposure-value,field-of-view}` 8 页，更新旧宠物零食条目源码状态，记录时间校验、模式初始化与摄影物理输入问题。至清单第 512 页，静态续审累计 232 页；仅源码分析，未运行浏览器，不计双跑。
- 静态续审第三十七批：阅读 `photo/{flash-gn,golden-hour,hyperfocal,macro-magnification,mired,nd-filter,photo-10,photo-11}` 8 页主要输入及计算路径；复核既有问题并更正微距守卫描述，记录黄金时刻空态、总 EV 口径与负输入等问题。至清单第 520 页，静态续审累计 240 页；仅源码分析，未运行浏览器，不计双跑。
- 静态续审第三十八批：阅读 `photo/photo-{2,3,4,5,6,7,8,9}` 8 页输入、守卫和计算路径；记录画幅比较方向、星空曝光模型、反算边界和页面文案口径问题。至清单第 528 页，静态续审累计 248 页；仅源码分析，摄影模型须专业复核，未运行浏览器，不计双跑。
- 静态续审第三十九批：阅读 `photo/{photo,print-size,raw-size,safe-shutter}` 与 `photo2/{exposure-triangle,focal-length,video-storage,white-balance}` 8 页，更新历史守卫状态，记录曝光表拼接、系数和空态问题。至清单第 536 页，静态续审累计 256 页；仅源码及 Node 表达式复算，未运行浏览器，不计双跑。
- 静态续审第四十批：阅读 `plastic/{blow-molding,extrusion-rate,injection-cycle,material-select,shrinkage-calc}` 和 `pr/{analysis-6,analysis-assessor,analysis-density-1}` 8 页，记录输入校验、旧阶段图、未转义名称与关键词统计问题，更新挤出产量历史问题源码状态。至清单第 544 页，静态续审累计 264 页；仅源码分析，未运行浏览器或注入，不计双跑。
- 静态续审第四十一批：阅读 `pr/{assessor-56,assessor-57,assessor-58,assessor-59,assessor-manager-2,assessor-risk,media-invite,press-conference}` 8 页，记录 CPM 单位、分母与复制状态、流程编辑区覆盖及数据丢失风险。至清单第 552 页，静态续审累计 272 页；仅源码分析，未运行浏览器，不计双跑。


- 扫描时间：2026/11/5 05:04:33
- 覆盖工具页：**4807**
- 有输入控件的页：**4401**
- 无输入控件（纯展示/参考卡，跳过）：**406**
- 有输入但无主按钮（实时计算/表单提交，不计缺陷）：**653** → **2026-11-05 重算后作废**：A 真需点击 23 / B 已可改值 449 / C 误判 113（纯select 97+文件 10+画布 6）/ D 无文本输入 68（D-a 67+D-b 1）。逐页清单见 `/private/tmp/notclicked-653-classified.json`，旧 not-clicked 清单不得再作为派工依据。
- 空态三档（本版已按新口径重扫 **4401** 页）：真空态 `text_empty_no_select` **2422**｜select 默认态 `text_empty_sel_default` **1717**｜控件回读失真 `true_distortion` **262**；其余 **0** 页仍是旧口径记录，待全量重扫后归位
- 命中至少一类问题：**216**

> 口径：① 有效性＝先填值→记录快照→**改一个输入为明显不同的合法值**→再点主按钮→比较前后快照（排除「加载时已自动算过一次」的假阴性）；② 空态＝清空所有输入后点主按钮，结果区给出 NaN/Infinity/undefined/null/0/空串或结论即为缺陷；③ 死控件＝控件 id 在全部 `<script>` 中从未出现（且页面无 `querySelectorAll('input')` / `FormData` 这类泛化读取，内联 oninput 绑定的不计）。快照优先取 `#result/#output/.result*` 等结果容器，无则回退整页正文（剔除控件内的当前值）。

