# 医疗 · 量表评分类（psychiatry/psychology/clinical-nursing/rehabilitation/neurology 等 ~150 页）

## 2026-11-06 静态复核（未运行页面）
- `tools/psychology/attachment-style-test.html`：结果展示后修改答案旧结果不刷新——第1332批已修（change 事件内若 #atResult 已显示则 remove('on') 隐藏，避免与按当前答案重算的复制/导出不一致，源码形态强锚 `ATREFRESH` 已落 psychology verify；旧版无 ⇒ BAD）。余项：隐藏而非自动重算，用户须点"重新计算"才见新结果；心理量表解释与阈值须专业复核。
- `tools/psychology/holland-career-test.html:692-699,943-957,963-1005`：同样修改答案后旧画面不刷新，而复制/导出按当前状态重算；分数并列时 `:728-731` 按固定类型顺序排序，仍把前三名表述为主导型，需标明并列与不确定性。心理测验解释和阈值需专业复核。

## 已知问题

### M1. 条目结构重建项（G01-B 系列，需裁断后开发）
- gags-acne 7→6 分区、rater-21 TWSTRS 题量、psqi 成分 5 缺 2 项。
### M2. 阈值口径待裁断（G01-A8）
- kupperman、vanderbilt、asrs。
## 功能缺陷
- EMR note「门诊记录（答案回显/打印病历）」模板仅铺 4 页（gad7-anxiety / isi-insomnia / cage-substance / asrs-adhd），余下量表按同模板续铺：结果区追加虚线框 `📋 门诊记录`，含「量表中英名 + 总分/分级 + 阳性条目明细（含题目与所选项）+ 临床提示 + 留空的评估日期/评估者 + 免责声明」+「复制门诊记录」按钮；中英双语（EN 态零 CJK，题目文本 EN 态只留 Q 编号）。
- 结果只给总分档，缺「维度雷达图」（DHI/WOMAC 等已补 bar，推广到全量表）。

## 优化点（医疗是本站差异化最大赛道）
- S2 场景预设：「门诊 5 分钟筛查」「老年痴呆年度体检」一键全量表串。
- S7 引据徽标：每个量表标官方文献（PHQ-9 Kroenke 2001 等）——市面竞品几乎无人做，是专业信任的最大杀器。
- 「量表对照」模块：同病种多个量表（如焦虑 GAD-7/HAMA/BAI）并排说明适用场景。
- 打印样式：量表结果页 print CSS（医生工作站打印友好）。

## 受影响范围
- tools/psychiatry/（rater/eat26/asrs 等 14 页）、tools/psychology/（psqi/gad/scl90 等 18 页）、tools/clinical-nursing/（braden/morse/barthel 等 15 页）、tools/rehabilitation/（fim/mmse/berg 等 12 页）、tools/neurology/（dhi/dn4/rater 系 20 页）、tools/cognition/、tools/pediatrics/ 量表页（~150 页合计）

## 进度
- 🟡 进行中（2026-10-26 批次 03-3）：**S7 引据徽标**已落地 8 页高流量量表
  （psychology/phq9-assessment、psychiatry/gad7-anxiety、psychology/psqi-assessment、psychiatry/isi-insomnia、
  psychiatry/asrs-adhd、psychiatry/cage-substance、psychiatry/eat26-eating、psychology/scl90-assessment）。
  - 形态：卡片描述下方一条 `.ref-cite` 块（左侧主色竖线 + 灰底），内容=「原始文献（作者·标题·期刊·年;卷(期):页）｜ 施测方式 · 条目数 · 耗时 · 分值范围 · 划界分」。
  - i18n：正文英文、`data-zh` 放中文（项目既有 data-zh 模式），EN 态零中文。
  - 数据纪律：文献一律取量表原始发表文献（不引二手综述）；卷期页不确定时只写到「期刊+年份」，宁缺毋滥。
- 🟡 进行中（2026-10-26 批次 03-8）：**S7 引据徽标**再铺 32 页 —— pediatrics 24 页 + cognition 8 页，
  累计 **76 页**。本批要点：
  - 儿科页多基于**指南/规范**而非量表原始文献，引据前缀改为「原始文献/指南」，来源为 WHO（IMCI 腹泻手册、
    WHO 2014 肺炎分类、WHO 2011 贫血血红蛋白界值、WHO 2006 生长标准）、AAP（2022 高胆红素血症指南、
    CCHD 筛查 Kemper 2011）、NICE NG143、CDC/AAP 2022 里程碑、JCIH 2019、ILAE 2017、ICCS 2014、
    Salter-Harris 1963，以及中国国家卫健委《手足口病诊疗指南（2018）》《国家免疫规划疫苗儿童免疫程序（2021）》。
  - cognition 8 页中 3 页（cognitive-assessment / human-benchmark / time-perception）与 schulte-table 为**自研改编**，
    引据前缀写「范式来源」，正文明确标注「非标准化常模量表 / 百分位为在线样本经验参考 / 仅作自我纵向对比」，
    不冒充标准化常模（诚实性红线）。
  - 踩坑修复：上一批 mmse-scoring 的 cite 含裸双引号，导致 `data-zh` 属性被截断（中文引据只剩前半句）。
    已改为破折号；并新增全站属性完整性扫描（判据：`data-zh` 值必须含「｜」分隔符），现 76 页 BROKEN=0。
- 🟡 进行中（2026-10-26 批次 03-11~03-20）：门诊记录铺开 10 批。覆盖
  neurology 6（nihss/moca/edss/adas-cog/dhi/dn4）+ clinical-nursing 3（braden/morse/barthel）+ rehabilitation 1（berg）
  + neurology 4（updrs/qmg/sara/alsfrs-r）+ neurology 2（rls-severity/phq9-stroke）+ psychiatry 1（cdrisc-resilience）
  + neurology 3（rater-18/19/22）+ psychiatry 2（ybocs-ocd/panss-schizophrenia）
  + neurology 3（abcd2/house-brackmann/trigeminal-bni）+ neurology 5（midas/ilae-seizure/twstrs/rater-21/ncs-emg）
  + pediatrics 10（fever/pneumonia/dehydration-assessment/diarrhea-dehydration/neonatal-jaundice/pediatric-anemia/
  chd-assessment/mchat-autism/developmental-milestones/小时胆红素曲线）
  + pediatrics 5（growth-curve-zscore/enuresis-age/hfmd-course/hirschberg-test/seizure-classification）
  + pediatrics 4（hearing-screening/ddst-screening/assessor-13/pediatric-asthma）
  + rehabilitation 5（fim-scale/flacc-scale/nine-hole-peg/walker-height/stretch-duration）
  + clinical-nursing 5（iv-drip-rate/gastric-tube-depth/chest-compression-depth/oxygen-concentration/
  convert-flow-concentration）
  + clinical-nursing 5（bag-valve-mask/cvc-maintenance/assessor-pressure-risk/assessor-rater-risk/calc-rater-risk）。
  + rehabilitation 5（gait-analysis/prosthesis-alignment/respiratory-training/wheelchair-posture/tester-rater）
  + psychiatry 9（assessor-risk-5/mmpi2-personality/les-stress/rater-23/rater-24/self-assess-4/
  cssrs-suicide/lsas-social/calc-1）
  + psychology 4（phq9-assessment/psqi-assessment/sas-assessment/self-test-pressure）
  + psychology 5（assessor/calc-self-assess/rater/self-assess/calc-12）
  + clinical-nursing 1（cold-compress-timer）
  + pediatrics 3（pediatric-fracture/rater-27/vanderbilt-adhd）
  + clinical-nursing 4（pain-nrs/suction-pressure/restraint-check/surgical-position-risk）
  + rehabilitation 4（water-swallow-test/mmt-grading/boston-aphasia/rom-normal-value）
  + rehabilitation 4（asia-impairment-scale/mmse-scoring/physiotherapy-dose/proprioception-error）
  + rehabilitation 2（adl-task-breakdown/assistive-device-fitting，后者轮椅分支另加一条用例）
  + clinical-nursing 1（pressure-injury-description）+ neurology 2（psqi/calc-1）。
- 🔴 待续（**门诊记录铺开已收口：真实临床页全部铺完，余下为「排除（已决）/ 待裁断」，非待铺**）：
  M1 条目结构 / M2 阈值口径仍待老板裁断。当前未铺（排除 index）共 **42 页**，均为排除项：
  - `rehabilitation` **已全铺完**（23 个文件：22 个实页全铺 + `analysis-time.html` 为
    `TOOLBOX-REDIRECT` 重定向占位页直跳 gait-analysis、`robots=noindex`，不铺门诊记录）。
    该分类原被误记为「已全铺完」而实际只铺 12 页，本轮 03-32/03-33/03-34 三批补齐 10 页。
  - `psychology` 11：analysis-2、attachment-style-test、bigfive-personality-test、bubble-tea-personality-quiz、
    enneagram-test、generator-20、holland-career-test、random-12、tester-2、tester-3（10 页为非病历场景人格/趣味测验，老板早前定不铺）；
    scl90-assessment（外置 `/js/psych-kit.js` + `/js/tools/scl90-assessment.js` 60KB 引擎，harness 不加载外链 script，无法验证判别力，排除）。
  - `cognition` 8（2026-10-26 评估定档）：
    - **已铺 2**：`digit-span-test`（WAIS 数字广度，__dsEmr，按 fwd/bwd/seq 三项对照 WAIS 常模均值）、
      `corsi-block-test`（Corsi 木块广度，__cbEmr，逐年龄组对照 NORMS 差值）。两页钩在 finish() 写 rec 处，强用例用 clicks 注入 __dsResult/__cbResult 触发。
    - **不铺 6**（训练 / 选择器范式，无临床报告式结果，且 harness 无法驱动其点击/计时/随机序列注入，已逐项核查）：
      `cognitive-assessment`（域得分选择器，路由到子测验、无最终汇总分）、`human-benchmark`（36 处 addEventListener + 随机靶位/计时，
      结果存 results[id] 由交互驱动，无表单注入通道，沿用既有 all_default 判定）、`nback-training` / `schulte-table` / `stroop-test` / `time-perception`
      （反应时/工作记忆训练，成绩由点击与计时驱动、无 injectable 计算结果）。此 6 页为自评/训练性质，结果非病历素材，不做门诊记录（已评估，非草率收口）。
  - `clinical-nursing` **本批 03-38 已全铺完（7 页）**：cycle-7、fall-emergency-flow、generator-pressure、
    ostomy-bag-timing、reminder-time-1、restraint-duration、tracheostomy-dressing。
    处置要点：
    · 含 `new Date()` 的页（ostomy/restraint/tracheostomy/cycle/reminder）门诊记录只抓**稳定计算结果**（类型/间隔/次数/计划），
      不抓动态倒计时时刻 → 符合铁律④（用例不依赖今天）；
    · generator-pressure 只断言「共 N 条」稳定部分（随机内容不进 expect）；
    · **fall-emergency-flow 用「注入专属快照 + 渲染后自删」绕过兜底循环**：clicks 注入 `window.__fallSnap=[...]` 完成后调
      `window.__fallEmr()` 渲染并 `delete window.__fallSnap`，兜底循环即便再调也因快照已删而 return → 默认态零门诊记录、判别力成立。
  - `neurology` **已全铺完**（26 页，除 index）；`pediatrics` 真实临床页 **已全铺完**（含 assessor-spo2，03-39 证伪「stub 盲区」误记）；
    `vaccine-schedule` 依赖「今天」推算月龄，按铁律④ 排除不铺。
  - 「维度雷达图推广」「量表对照模块」未开发。
- 剩余未铺：① `psychology/scl90-assessment`（外置 `/js/psych-kit.js` + `/js/tools/scl90-assessment.js` 60KB 引擎，harness 不加载外链 script，无法验证判别力，与 vaccine-schedule 同类排除）；② `pediatrics/vaccine-schedule`（依赖「今天」推算月龄，按铁律④ 排除）；③ psychology 其余 10 页（人格/趣味测验，非病历场景，不铺）；④ cognition 其余 6 页（训练/选择器范式，评估定档不铺）。
- harness 关键事实：兜底循环会无参调用所有顶层 function 声明 ⇒ 新 helper 写成 `var f=function(){}`；复选框注入字段是 `checkIds`；clicks 的 `window` ≠ page 的 `window`，input 的 `.value` 在 clicks 内改易被兜底重置，可靠通道是 DOM 输入、page 内对象属性、带守卫的带参调用、无参 `calc()`。

## 2026-11-03 第一轮抽样补充

### BIS-11 英文 CSV 题目残留中文（待核准英文译本，820 批评估）
- `tools/psychiatry/bis11-impulse.html:300-321` 英文导出翻译表头、选项和汇总，逐题却直接使用中文 `QS`。
- 方案：使用经过核准的英文题目；若无可靠译文则明确标识原语言，勿杜撰标准量表译本。英文导出行为待真实浏览器复验。
- 覆盖：仅抽查上述量表 2 页，其余未逐页覆盖；未核验量表标准与医学阈值，未运行门禁。

## 2026-11-03 续查：精神健康量表

### M-N4 多量表首次作答回溯期冲突（高，确认源码路径）
- 证据：`tools/psychiatry/pcl5-ptsd.html:122,542`、`tools/psychiatry/pdss-panic.html:121,498`、`tools/psychiatry/aq-autism.html:544`、`tools/psychiatry/mdq-bipolar.html:237-250,519` 均给 `js/psych-kit.js:195-218` 配置「最近两周」，而页面 PCL-5 说明为过去一月、PDSS 为过去一周、MDQ 问既往、AQ 题干侧重一般特质。实际首次展示待浏览器核验。
- 影响：上述四页；统一说明可能改变用户作答参照，影响结果。
- 方案：专业审核各量表版本后配置对应的时间范围或无回溯期说明，支持既往及特质性文案；回归首访和重访。

### M-N8 英文导出含中文题目（待核准英文译本，820 批评估）
- 证据：`tools/psychiatry/pcl5-ptsd.html:337-346`、`tools/psychiatry/pdss-panic.html:309-318`、`tools/psychiatry/aq-autism.html:356-370`、`tools/psychiatry/mdq-bipolar.html:322-335` 英文分支逐题仍使用中文题干；部分答案亦为中文。导出数据经内存调用验证，实际下载未测。与既有 BIS-11 项同类，按页归并。
- 影响：上述四页；英文报告难以理解及复核。
- 方案：使用经授权、核准的英文版本；无可靠译本时标明原语言，勿自行杜撰标准题目；增加英文 CSV 检查。

### 续查覆盖
- 新抽查 `tools/psychiatry/pcl5-ptsd.html`、`tools/psychiatry/pdss-panic.html`、`tools/psychiatry/aq-autism.html`、`tools/psychiatry/mdq-bipolar.html` 4 页，新增 8 条（5 条高优）；为源码及内存执行证据，未做真实浏览器、线上或门禁验证。预设及历史应标识示例、避免混入个人评估，具体见 M-N3/M-N7。

## 2026-11-03 续查（并行批 I）

> 本批新读 8 页，与 M-N1–M-N8 已覆盖的 pcl5-ptsd / pdss-panic / aq-autism / mdq-bipolar / phq15-somatization / bis11-impulse 无重叠。证据均为源码行号 + `node -e` 按页面原表达式/原数组复算，未开浏览器、未做 EN/移动端/门禁验证。

### M-N21 英文 CSV 表头已翻译、逐题题干仍为中文（待核准英文译本，820 批评估）
- **描述**：英文导出分支翻译了表头、选项与汇总，但逐题题干仍直接取中文 `QS`，英文报告无法阅读与复核。
- **证据**：`tools/psychiatry/gad7-anxiety.html:298,317`（`__gd7Text(i){ return QS[i]; }` 用于英文 CSV）；`tools/psychiatry/isi-insomnia.html:300,319`；`tools/psychiatry/ybocs-ocd.html:306,327`；`tools/psychiatry/eat26-eating.html:331` 直接 `row((i+1),q,...)`。源码确认英文分支仍返回中文题干；未做 `?lang=en-US` 实机导出验证。
- **影响**：上述四页；英文 CSV 题目不可读，与 M-N8 同类但属本批新页。
- **方案**：接入经核准的英文题目层；无可靠译本时在表头标注原语言，不自行翻译标准量表条目；增加英文 CSV 题目非 CJK 断言。

### 留存优化
- 将各量表的「选项→分值」与「总分→分级」抽成页面级单一常量/函数，表格、FAQ、示例、CSV、EMR 全部由它派生，杜绝同一页两套口径（M-N14/M-N22）。
- 统一「未完成 → 不给出分级/不生成 EMR/不可复制」守卫，覆盖结果区、导出与复制三个入口，而不只是 EMR（M-N17/M-N19）。
- 为所有计分方向敏感的条目（反向题、抵抗/控制题）建立「选项标签→分值」显式映射与方向断言，避免数组对调或直加原始分（M-N9/M-N11）。
- 英文导出统一走经核准的题目翻译层；无译本时明确标注原语言，不自行翻译标准量表（M-N21）。
- 增加静态检查：每页至多 1 个 `related-tools` 块、无未定义全局标识符、分级表与代码常量一致（M-N16/M-N23）。
- 本批未改任何 tools/js/css/json/构建产物；以上均为待排期方案。

### 续查覆盖
- 新查 8 页：`tools/psychiatry/gad7-anxiety.html`、`tools/psychiatry/isi-insomnia.html`、`tools/psychiatry/eat26-eating.html`、`tools/psychiatry/ybocs-ocd.html`、`tools/psychiatry/cssrs-suicide.html`、`tools/psychology/sas-assessment.html`、`tools/neurology/dhi.html`、`tools/rehabilitation/berg-balance-scale.html`。
- 新增 17 条（M-N9–M-N25），其中高优 4 条（M-N9、M-N11、M-N13、M-N17）；与 M-N1–M-N8 页面无重复。
- 证据口径：逐页读源码 + `node -e` 按原数组/原表达式内存复算；未做真实浏览器交互、`?lang=en-US` 实机、移动端、线上或门禁验证，也未核验各量表标准阈值与授权译本。

## T 批 psychiatry 覆盖（2026-11-04）
- 本轮审计 12 页：`tools/psychiatry/rater-24.html`、`tools/psychiatry/cdrisc-resilience.html`、`tools/psychiatry/cage-substance.html`、`tools/psychiatry/lsas-social.html`、`tools/psychiatry/phq9-depression.html`、`tools/psychiatry/rater-23.html`、`tools/psychiatry/les-stress.html`、`tools/psychiatry/self-assess-4.html`、`tools/psychiatry/assessor-risk-5.html`、`tools/psychiatry/mmpi2-personality.html`、`tools/psychiatry/calc-1.html`、`tools/psychiatry/panss-schizophrenia.html`。
- 新增 14 条（高 13 / 中 1），编号 M-N26–M-N39；假工具候选 0 页（12 页均有真实计分实现；`rater-24`/`rater-23` 属默认预选导致「无输入即出结论」，已按高优缺陷记录，不计为假工具）。
- `les-stress`、`mmpi2-personality` 无高优缺陷，整页跳过（前者 0 事件即「低风险」符合核对表语义，后者默认 T=50 为明示的总体均值；二者仅有文案/钳位类低优问题）。
- 未做浏览器/门禁/线上验证：证据均为源码行号 + `node -e` 按页面原表达式/原数组内存复算，未开浏览器、未跑 `_build.py`/门禁、未核各量表标准阈值与授权译本。

## U 批 · 精神科量表复核（2026-11-04）

> 本批只读复核既有条目：逐页读当前源码并复算，只登记「仍成立的高优」与「已失效需重开」两类；所有量表阈值、分级与临床解读**需临床复核**。未开浏览器、未跑门禁/线上。

### M-N45 Y-BOCS 抵抗/控制 4 条是否反向计分（原 M-N11，待临床确认，820 批评估）
- 页面：`tools/psychiatry/ybocs-ocd.html`
- 现状：`:278` 仍 `A.reduce(...)` 原始分直加，`:427-430` 门诊记录同；`:240` 选项为「无→极重度」，题面却写「越努力抵抗得分越低」。
- 复现：第 4 题选「极重度抵抗」、其余 0 → 实际总分 4「亚临床」；第 4 题选「无」→ 0 分，抵抗越强分越高。期望 4 条抵抗/控制题反向计分。
- 结论：仍成立；假工具：否；需临床复核。
- 评估（2026-11-16，820 批）：Y-BOCS 第 4 项（抵抗）与第 5 项（控制）的量表原文计分方向需按授权版本核对——「抵抗」通常 0=完全抵抗、4=完全屈服，「控制」0=完全控制、4=无法控制，二者是否需反向取决于题面措辞。当前页面题面「越努力抵抗得分越低」与选项方向可能已自洽，贸然反向会反向放大症状。故本批不改代码，保留待临床/授权版本确认。

## U 批 精神科复核覆盖（2026-11-04）
- 复核 15 页：任务列出的 13 页（aq-autism、asrs-adhd、bis11-impulse、cage-substance、cdrisc-resilience、cssrs-suicide、eat26-eating、gad7-anxiety、isi-insomnia、les-stress、lsas-social、mdq-bipolar、pcl5-ptsd），另按目录实页补入 `ybocs-ocd.html`、`phq15-somatization.html`；目录中无 `phss.html`。
- 复核结论：13 条高优中 M-N49（LSAS 公式已改 24 项/72/144）、M-N50（CAGE 恢复回调已 `render();calc()`）经源码核对已修，记录删除；其余仍成立项涉专业量表口径，待临床/授权版本确认，不自判销账。
- `asrs-adhd`、`gad7-anxiety`、`isi-insomnia`、`les-stress` 无既有高优条目；GAD/ISI 的 M-N12 为中优，未按本批「只登记高优/已失效」口径展开。
- 未开浏览器、未跑构建/门禁/线上；所有量表阈值与临床解读需临床复核。

## 2026-11-05 量表默认态收口（专项：dirty 守卫 + 重置评分）
- 目标：未评估（默认态）只出分数与提示，**不出分级/建议/诊断/治疗/风险**；任一量表项 input/change 置 dirty 后才渲染分级、解读与门诊记录。默认态 sentinel 断言固定为「结果区不含 分级/建议/诊断/治疗/风险」，每页三态（默认/改动态/重置）真机各验一次。
- 重置：新增「重置评分」按钮（工具栏，`title="恢复为未评估状态"`，复用既有 `.btn`），`resetAll()` 先 `__scaleDirty=false` 再复算，并清 `#emrBox`；已有重置按钮的页面直接复用、不重复加。
- **单选量表页加载态口径（用户确认，同类页统一照此处理）**：页面加载时若某组选中值非默认 `0`（浏览器恢复/外部赋值），即视为「已评估」置 `__scaleDirty=true`，避免刷新后被恢复的填报值被当成默认态、决策被吞掉这类反向坑。真机默认全 0 时仍走默认态。
- 分数自带档位语义的页面（如 Braden 21/23 对应「无风险」）：默认态可显示分数，但档位名属决策文案，必须走 dirty 守卫；遇歧义先报，不自行放宽。
- 进度：样板 3 页 `e3fc4da26e`（NIHSS/UPDRS-III/Braden）；批 1 `0ed5547503`（neurology 6 页）；批 2 `f01e3cfcf2`（neurology 7 页）；已完成 16 页，剩余 21 页（批 3–5）。

## 2026-11-06 康复工具静态续审

- `rehabilitation/asia-impairment-scale`：`evaluate()` 的正常检查只查轻触和肌力，漏查针刺（`:424-434`）。例如其余正常、单侧针刺为 0，仍可能显示 AIS E；平面判断用两侧轻触任一正常（`:370-375`），运动保留遍历全部关键肌而非损伤平面以下（`:394-400`），C/D 也统计全部关键肌（`:409-420`）。NT 被求和时跳过，却仍显示固定满分（`:320-330`、`:353-361`），信息不完整时亦可给出确定分级。结果与界面逻辑冲突；临床判定必须由专业人员复核。
- 同页选择变化只更新感觉/运动总分（`:308`、`:338`），不清空上次 `window._evalResult`；保存读取该缓存（`:492-497`）。完成评定后修改任一选项再保存，保存的仍是此前分级，须重新评定或在修改时清空旧结论。
- `rehabilitation/rom-normal-value`：肘或膝伸直正常上限为 0（`:258`、`:278`），`evaluateROM()` 在零上限特殊分支前先计算 `angle / data.max`（`:341-344`），0° 得 NaN、非零得 Infinity，随后字符串守卫将结果替换为无效值提示（`:367-373`）；零上限分支写出的正常/过伸等状态无法显示。保存仅检查 `isNaN(angle)`（`:389-401`），仍可保存该测量。
- `rehabilitation/water-swallow-test`：一次饮完无呛咳且超过 5 秒时，结果按 Ⅱ级修正（`:295-305`），但保存直接取下拉原始值（`:316-324`）；例如选择 Ⅰ级、输入 8 秒，显示 Ⅱ级而历史记录存 Ⅰ级。顶部标题也在修正前写出原 Ⅰ级（`:290-301`），同屏存在两个等级。专业分级规则需另行核验。
- `rehabilitation/assistive-device-fitting`：`_deviceResult` 被三个分支共用，切换标签仅改变显示（`:367-375`）；初始化依次计算各分支（`:590-593`）。当前轮椅页尚无结果时，保存可取其他标签的旧结果；清空必填参数或重置也未清该缓存（`:385-388`、`:583-588`）。此外未填小腿长时座深/座高采用 40/45，而表格仍称「小腿长 −3/+5」（`:390-409`）。
- `rehabilitation/physiotherapy-dose`：旧条目 12-N124–126 的阶段映射、负值和时间下限相关源码仍在（`:359-374`、`:401-413`、`:442-459`）；专业剂量与安全性未做临床核验。
- `rehabilitation/adl-task-breakdown` 的选项变更重绘步骤、保存与文本导出分别读取当前选择（`:356-366`、`:424-443`）；`rehabilitation/mmt-grading` 选级触发描述、保存读取当前选级、重置清选择与结果（`:120-135`、`:261-278`、`:300-303`、`:345-348`）。以上仅为主要路径源码阅读，不代表运行通过。
- 本批均为静态分析，未运行浏览器；医疗结果及建议需专业复核。
