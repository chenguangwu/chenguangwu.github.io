# 医疗 · 量表评分类（psychiatry/psychology/clinical-nursing/rehabilitation/neurology 等 ~150 页）

## 2026-11-06 静态复核（未运行页面）
- `tools/psychology/attachment-style-test.html:501-508,699-706,743-786`：结果展示后修改答案仅更新进度，原结果仍显示；复制和导出则按修改后的答案重新计算，可能与画面不一致。应修改答案时隐藏旧结果或重算。
- `tools/psychology/holland-career-test.html:692-699,943-957,963-1005`：同样修改答案后旧画面不刷新，而复制/导出按当前状态重算；分数并列时 `:728-731` 按固定类型顺序排序，仍把前三名表述为主导型，需标明并列与不确定性。心理测验解释和阈值需专业复核。

## 已知问题
### M1. 条目结构重建项（G01-B 系列，需裁断后开发）
- gags-acne 7→6 分区、rater-21 TWSTRS 题量、psqi 成分 5 缺 2 项。
### M2. 阈值口径待裁断（G01-A8）
- kupperman、vanderbilt、asrs。
## 功能缺陷
- ~~量表页普遍缺「答案回显/打印病历」格式（医生群体要能贴进门诊记录）。~~
  → 2026-10-26 批次 03-9 落地「门诊记录（EMR note）」：结果区追加虚线框 `📋 门诊记录` 段，
  内容为「量表中英名 + 总分/分级 + 阳性条目明细（含题目与所选项）+ 临床提示 + 留空的评估日期/评估者 + 免责声明」，
  配「复制门诊记录」按钮（`ToolBox.copyText`）；中英双语（EN 态零 CJK，题目文本 EN 态只留 Q 编号避免中文残留）。
  已铺 4 页（gad7-anxiety / isi-insomnia / cage-substance / asrs-adhd），余下按同模板续铺即可。
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
- 🟢 收口（2026-10-26 批次 03-39）：**pediatrics/assessor-spo2 铺门诊记录**（CCHD 脉搏血氧筛查）。
  要点：钩在 `calc()` 渲染前捕 `window.__EMR_S={minS,diff,cchd,urg,lvl,tot,sign,risk,rh,ft}`，`__spo2Emr()` 自建
  `cchdMap/urgMap/lvlMap` + `resultEn/extraEn/hintEn` 纯英文映射（EN 态零 CJK）；`boxId:'res'`。
  **推翻旧记「已踩 stub 盲区」**：本批 harness 实测注入 85/80 →「CCHD筛查阳性（SpO2＜90%）」、98/97 → 阴性，
  整段 script 正常执行、判别力成立，旧结论作废。
  旧 verify 用例 `expect:["85%","CCHD筛查阳性"]` 含「85%」输入回显（逃生项类型②）→ 改为门诊记录强串
  「CCHD脉搏血氧筛查：CCHD筛查阳性（SpO2＜90%）」+「综合风险：中风险」，二者均随输入变化、默认态不出现、零交集。
  pediatrics 真实临床页全部铺完。全量门禁 218/218、逃生项 0（基线 0 无新增）、UX 7.46→8.63 无回退。
  全站累计 **130 页**（03-39 再 +1：pediatrics 收口）。
  至此 **psychiatry / psychology(除 scl90) / rehabilitation / neurology / cognition(铺 2) / clinical-nursing / pediatrics(除 vaccine-schedule) 全部真实临床页已铺完**；
  剩余未铺仅：① `psychology/scl90-assessment`（外置 `/js/psych-kit.js` + `/js/tools/scl90-assessment.js` 60KB 引擎，harness 不加载外链 script，无法验证判别力，与 vaccine-schedule 同类排除）；
  ② `pediatrics/vaccine-schedule`（依赖「今天」推算月龄，按铁律④ 排除）；
  ③ psychology 其余 10 页（人格/趣味测验，非病历场景，老板早前定不铺）；④ cognition 其余 6 页（训练/选择器范式，评估定档不铺）。**neurology 已全铺完（26 页，除 index）**、**clinical-nursing 已全铺完（26 工具页，含本批 cycle-7/fall-emergency-flow/generator-pressure/ostomy-bag-timing/reminder-time-1/restraint-duration/tracheostomy-dressing）**、psychiatry 已全铺完，
  rehabilitation 已全铺完，**cognition 已评估定档（铺 2：digit-span/corsi；其余 6 训练/选择器范式不铺）**，psychology 仅剩 scl90（外部 js + psych-kit 通用引擎）与
  若干非临床人格/趣味页（bubble-tea/enneagram/bigfive/holland，非病历场景，不铺门诊记录）。
  顺手修 3 个真 bug：DHI 维度分母互换（P/F 的 28/36 写反）、IRLS 症状特征分母、rater 系满分口径；
  并清理 rater-18/19/22 三条「模板残留假通过」用例（`+j+` 命中页面源码，零判别力，判别力检查从 35 检/3 跳过变为 40 检/0 跳过）。
  - 模板三种变体：① `#result` + 名下 select（nihss 系）；② `#result` + 生成式按钮 `scores`（护理系）；
    ③ `#res`/`#resultBox` + 生成式 select 或 radio（rater/berg 系）。
  - 硬坑：`__emrNote` 容器 id 要可配（`cfg.boxId`）；护理页分级必须自算（harness 的 `scores[undefined]` 会污染页面 total）；
    生成式 select 在 stub DOM 下 `options` 为空，满分要回退 `items[i].o.length-1`；分母以「页面声明的满分」为准。
  - **第三种模板（03-19 起）：记录式钩子**——在 `calc()` 内写 `#result` 之前插 `window.__EMR_SUM={...}`，把页面已算好的分级变量捞出来，
    `__emrData()` 只做排版。适合「计算器型」页（输入→阈值→分级），零逻辑复制、不与页面阈值漂移；问卷型（answers 对象）仍需 clicks 注入。
  - 新增 harness 事实：兜底循环会**无参调用所有顶层 function 声明** ⇒ 新 helper 写成 `var f=function(){}`；复选框注入字段是 `checkIds`；
  - **`clicks` 带参调用的真相（2026-10-26 更正）**：兜底循环确实会无参重调页面函数，但只要 **REC 里对参数加了
    `typeof v==='number'` / `typeof v==='string'` 守卫**，兜底那次（参数 undefined）就被守卫挡掉、**不会覆盖**已捕获的值，
    `clicks:["selectPain(7)"]` / `selectPosition('lithotomy',哑btn)` 都实测可靠（已写入 verify）。
    之前「带参全读回 undefined」是 **未加守卫**时代的结论，已作废——别再因此绕道。
    仍需注意：clicks 的 `window` ≠ page 的 `window`（跨作用域不通）；input 的 `.value` 在 clicks 内改易被兜底重置，
    可靠通道仍是 ① DOM 输入（`inputs` 字段）② page 内对象/数组属性（`checkedState.x[i]=true`、`answers['inatt_0']=3`）
    ③ 带守卫的带参函数调用 ④ 无参 `calc()` 后由页面自身读 DOM。
    **正面做法**：REC 只把值写进 page 内变量 `__EMR_S`，`__emrData()` 无参读它；再用 `calc`/页面函数的 wrapper
    `finally` 触发一次渲染（时序确定，不依赖兜底循环）。
    `__emrEsc` 会把 `>`/`<`/`&` 转成实体，expect 不能直接写这些字符。
  - **EN 态零 CJK 的硬约束（2026-10-26 实测踩坑）**：note 的 `resultEn/hintEn/extraEn` **绝不能引用页面里的中文字段**
    （`d.name`/`d.level`/`d.comm`/`d.desc`/`d.training`/`s.j`/`s.m`/`s.st`/`s.adv` 全是中文小标题与描述），
    否则英文态整块泄漏中文。做法：EN 分支自建**英文数组/映射表**（罗马数字 `['I','II',...]`、`['normal','equivocal',...]`、
    `descEn/trainEn/lvEn/stMap` 等），中文数据只喂 `result/hintZh/extra`。
    验证手段（门禁不含此项，必须自测）：项目根临时脚本，jsdom 加载 `?lang=en-US` → 注入输入/设 radio.checked/调用页面函数
    → **只扫 `#emrPre` 的 textContent**（扫整个 `#resultBox` 会把页面自身未翻译的静态中文算进来，误报），
    CJK 正则含 `\u4e00-\u9fff\u3000-\u303f\uff00-\uffef`；跑完即删临时脚本。
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

## 2026-11-03 第一轮抽样补充

### 恢复答案后仍显示旧结果（高，确认）
- `tools/psychiatry/phq15-somatization.html:254-266,282-283,348-355` 历史回调恢复答案后仅 `render()`，不计算结果。原函数内存桩执行先算全 0 再恢复全 2，答案已更新但仍显示 0/30（原公式求和为 30）。未做真实浏览器交互验证。
- 方案：恢复后统一重算结果，未完成时清除结果及导出状态；记录为本机保存并给共享设备提供明确清除入口。

### 重置或未完成后旧标尺残留（高，确认）
- `tools/psychiatry/phq15-somatization.html:261-266,282-283`、`tools/psychiatry/bis11-impulse.html:272-278,296-297` 独立标尺不随重置或未答完路径清除；原函数内存桩验证旧标尺保留。
- 方案：同步清除结果、标尺和可导出状态；在 BIS-11 增加各维度答案复核与示例标识，避免预设结果混入个人历史。

### BIS-11 英文 CSV 题目残留中文（中，源码确认）
- `tools/psychiatry/bis11-impulse.html:300-321` 英文导出翻译表头、选项和汇总，逐题却直接使用中文 `QS`。
- 方案：使用经过核准的英文题目；若无可靠译文则明确标识原语言，勿杜撰标准量表译本。英文导出行为待真实浏览器复验。
- 覆盖：仅抽查上述量表 2 页，其余未逐页覆盖；未核验量表标准与医学阈值，未运行门禁。

## 2026-11-03 续查：精神健康量表

### M-N1 PCL-5 症状群判定口径与门诊记录不一致（高，确认源码缺陷）
- 证据：`tools/psychiatry/pcl5-ptsd.html:294-298,317,356-360,452-455` 症状群计数按条目 `>0`，门诊记录阳性条目按 `≥2`。第 1、6、8、9、15、16 题各选 1，其余选 0，结果 6/80 却显示「DSM-5 症状群筛查：符合」，门诊记录无阳性条目。美国退伍军人事务部 [PCL-5 计分说明](https://www.ptsd.va.gov/professional/assessment/adult-sr/ptsd-checklist.asp) 的暂定症状群方法采用至少 2 分；量表版本和临床适用性仍需专业审核。
- 影响：`tools/psychiatry/pcl5-ptsd.html`；症状群提示可能假阳性且输出互相矛盾。
- 方案：由专业人员确认版本与条目映射后，统一页面、CSV 和门诊记录阈值；注明筛查不等于诊断，增加 1 分反例及 2 分边界测试。

### M-N2 MDQ 补充题未完成时门诊记录写阴性（高，确认源码缺陷）
- 证据：`tools/psychiatry/mdq-bipolar.html:297-301,423-440` 第一部分 13 题都选是、第二三部分不答时，记录结论为待补充，但提示按 `screen=false` 写「目前未达 MDQ 筛查阳性」，英文写 `screen is currently negative`。
- 影响：`tools/psychiatry/mdq-bipolar.html`；不完整筛查可被错误解释为阴性并复制进门诊记录。
- 方案：未完成时明确「不可判定」，或阻止生成完整记录；中英文提示与结果一致，覆盖各补充题缺答情形。

### M-N3 恢复量表历史后旧结果仍显示（高，确认源码路径）
- 证据：`tools/psychiatry/pcl5-ptsd.html:396-403`、`tools/psychiatry/pdss-panic.html:357-364`、`tools/psychiatry/mdq-bipolar.html:371-379` 恢复答案后只 `render()` 未重算。内存调用原回调：PCL-5 全 0 后恢复全 2，答案和为 40 而结果仍为 0/80；PDSS 同样为 14 与旧 0/28；MDQ 可出现阳性答案配旧阴性。真实浏览器交互待验证。与本文件 PHQ-15 旧结果条目同类，按受影响页面归并。
- 影响：上述三页；旧分数和结论可能被误作恢复记录的结果。
- 方案：恢复后校验并同步重算、更新结果和标尺；未完成时清除旧结果及导出状态，避免恢复操作产生新历史。

### M-N4 多量表首次作答回溯期冲突（高，确认源码路径）
- 证据：`tools/psychiatry/pcl5-ptsd.html:122,542`、`tools/psychiatry/pdss-panic.html:121,498`、`tools/psychiatry/aq-autism.html:544`、`tools/psychiatry/mdq-bipolar.html:237-250,519` 均给 `js/psych-kit.js:195-218` 配置「最近两周」，而页面 PCL-5 说明为过去一月、PDSS 为过去一周、MDQ 问既往、AQ 题干侧重一般特质。实际首次展示待浏览器核验。
- 影响：上述四页；统一说明可能改变用户作答参照，影响结果。
- 方案：专业审核各量表版本后配置对应的时间范围或无回溯期说明，支持既往及特质性文案；回归首访和重访。

### M-N5 MDQ 判定条件与公式、说明不一致（中，确认内部冲突）
- 证据：`tools/psychiatry/mdq-bipolar.html:123-127,150-155,186-190,303-307` 页面代码依「≥7 项、同一时期、问题至少中度」判定，但公式和深度解析对后两项表述不同。
- 影响：`tools/psychiatry/mdq-bipolar.html`；读者难以核对判定。尚未全面核验原量表全文。
- 方案：按经授权版本核对问卷、公式、FAQ、示例和 CSV，并保持三条件一致。

### M-N6 PDSS 把量表分值直接表述为疾病与治疗结论（高，确认表述缺陷）
- 证据：`tools/psychiatry/pdss-panic.html:120-126,152-160,189-193,273-280,300-305` 七题均 2 分为 14/28，页面直接称存在重度惊恐障碍并需药物联合心理治疗，但页面也说不能替代诊断；说明示例称 8 分阈下，分级表和程序却归中度。
- 影响：`tools/psychiatry/pdss-panic.html`；量表自评易被误读为诊断或处方。
- 方案：改为分值范围及建议专业评估，统一示例与阈值；分级医学适用性须经临床及文献审核。

### M-N7 AQ 标尺分段、结果及重置状态不一致（中，确认源码路径）
- 证据：`tools/psychiatry/aq-autism.html:322,336-377` 高分结果称临床显著，标尺分段未对应 32 分边界；重置仅清空结果，旧标尺和已显示明细仍可保留。`js/tool-kit.js:105-107,855-879` 对开放上界的处理也需针对实际渲染复验。
- 影响：`tools/psychiatry/aq-autism.html`；分段和旧明细可能使读者混淆当前结果。
- 方案：专业审核分段后统一标尺、结果及 CSV；重置时清空标尺与明细，核验 25、26、31、32、50 分边界。

### M-N8 英文导出仍含中文题目（中，确认源码路径）
- 证据：`tools/psychiatry/pcl5-ptsd.html:337-346`、`tools/psychiatry/pdss-panic.html:309-318`、`tools/psychiatry/aq-autism.html:356-370`、`tools/psychiatry/mdq-bipolar.html:322-335` 英文分支逐题仍使用中文题干；部分答案亦为中文。导出数据经内存调用验证，实际下载未测。与既有 BIS-11 项同类，按页归并。
- 影响：上述四页；英文报告难以理解及复核。
- 方案：使用经授权、核准的英文版本；无可靠译本时标明原语言，勿自行杜撰标准题目；增加英文 CSV 检查。

### 续查覆盖
- 新抽查 `tools/psychiatry/pcl5-ptsd.html`、`tools/psychiatry/pdss-panic.html`、`tools/psychiatry/aq-autism.html`、`tools/psychiatry/mdq-bipolar.html` 4 页，新增 8 条（5 条高优）；为源码及内存执行证据，未做真实浏览器、线上或门禁验证。预设及历史应标识示例、避免混入个人评估，具体见 M-N3/M-N7。

## 2026-11-03 续查（并行批 I）

> 本批新读 8 页，与 M-N1–M-N8 已覆盖的 pcl5-ptsd / pdss-panic / aq-autism / mdq-bipolar / phq15-somatization / bis11-impulse 无重叠。证据均为源码行号 + `node -e` 按页面原表达式/原数组复算，未开浏览器、未做 EN/移动端/门禁验证。

### M-N9 EAT-26 正向/反向计分数组互换，症状越多得分越低（高，确认）
- **描述**：`NORM` 与 `REV` 两个计分数组被对调。正向症状题选「总是」得 0 分、选「从不」得 3 分，方向与量表通行计分相反；3 道反向题则相反，导致「症状频率越高，总分越低」。
- **证据**：`tools/psychiatry/eat26-eating.html:242-243` 定义 `NORM=[0,0,0,1,2,3]`、`REV=[3,2,1,0,0,0]`，`:272` 反向题为 8/13/25，`:300` 按 `REV_IDX[i]?REV:NORM` 累加；页面自述表 `:152-161` 也写「总是：正向 0、反向 3」。`node` 复算：26 题全选「总是」→ **9 分（低风险）**，全选「从不」→ **69 分（≥20 高风险）**；预设 `:361`「低风险示例」→ **0 分**，`:362`「高风险示例」→ **78 分（满分 78）**。
- **影响**：`tools/psychiatry/eat26-eating.html` 全部结果、临界值 20、预设、CSV、门诊记录及历史分数方向反转；高频症状者可被判低风险，无症状者反被判高风险。深度解析 `:191` 还写「第 4/9 题报告经常/总是 → 达阳性」，与计分表自相矛盾。
- **方案**：把正向数组改为 `[3,2,1,0,0,0]`、反向数组改为 `[0,0,0,1,2,3]`，重新推导三个预设与示例；增加全「总是」=69、全「从不」=9 的回归用例，并由专业人员复核 8/13/25 反向题归属。

### M-N10 EAT-26 高风险行为判定在页面、CSV、门诊记录三处方向相反（中，确认）
- **描述**：页面与门诊记录把暴食/催吐答「经常/总是」判为高风险，CSV 却把「有时/很少/从不」判为高风险；门诊记录「阳性条目」的阈值也把低频率答案收进阳性列表。
- **证据**：`tools/psychiatry/eat26-eating.html:304` 页面 `A[3]<=2 || A[8]<=2`（OPTS 0=总是），`:408` 门诊记录同向；`:325` 导出 `A[3]>=3 || A[8]>=3`。`node` 复算输入 `A[3]=5, A[8]=5`（从不暴食/从不催吐）→ 页面 `risky=false`，导出 `risky=true`，CSV 写「Binge/purge reported (often or always)」。另 `:407` 阳性条目判据 `__eatScore(i)>=2`，对 23 道正向题而言 2/3 分对应「很少/从不」，即把最轻的答案列为阳性。
- **影响**：`tools/psychiatry/eat26-eating.html`；同一份答卷在页面、CSV、病历中出现相反结论。
- **方案**：抽出唯一的 `isHighRiskBehavior(A)` 与 `positiveItems(A)` 供三处共用；按选项频率而非分值判定阳性；补「从不暴食/从不催吐」与「总是暴食」两组用例。

### M-N11 Y-BOCS 抵抗/控制 4 条目未反向计分（高，确认）
- **描述**：第 4/5/9/10 题（思维与行为的「抵抗程度」「控制程度」）与其余条目共用「无→极重度」的 0–4 原始分累加，题面却明写「越努力抵抗得分越低」「越能控制得分越低」。因此「极重度抵抗」反而把总分推高。
- **证据**：`tools/psychiatry/ybocs-ocd.html:240` `OPTS=['无','轻度','中度','重度','极重度']`，`:245-251` 四条抵抗/控制题，`:278` `total=A.reduce(...)` 直接求和，`:427-430` 门诊记录也按 `A[i]` 累加。`node` 复算：`A=[0,0,0,4,0,0,0,0,0,0]`（第 4 题选极重度抵抗）→ **总分 4（亚临床）**；同题选「无」→ **0 分**，即抵抗越强分数越高。
- **影响**：`tools/psychiatry/ybocs-ocd.html`；4 条抵抗/控制题均按原始分直加，其中两道抵抗题与题面「越努力抵抗得分越低」明确相反，控制题的选项语义亦需临床复核；强迫严重度可被系统性高估。
- **方案**：为 4 条抵抗/控制题单独定义「选项标签 → 计分值」映射（抵抗越强/控制越好记低分），保留原始选项文本用于 CSV；加 Q4「无 vs 极重度」方向断言与总分边界测试。

### M-N12 GAD-7 / ISI / Y-BOCS 恢复历史后只重绘不重算（中，确认）
- **描述**：历史记录回调把答案写回 `A` 后只调用 `render()`，不调用 `calc()`；若此前页面处于未答状态，结果区仍停留在旧的「已作答 0/N」，与恢复后的答案和总分不一致。
- **证据**：`tools/psychiatry/gad7-anxiety.html:358-361` 恢复回调、`:250-259` `render()` 不碰 `#result`、`:271` 未完成提示；`tools/psychiatry/isi-insomnia.html:360-363`、`:252-261`、`:273`；`tools/psychiatry/ybocs-ocd.html:370-373`、`:254-260`、`:275`。源码路径复现：先空答案 `calc()` 得「已作答 0/7（或 0/10）」，再把 `A` 全设为 2（GAD/ISI 合计 14、YBOCS 合计 20）后仅执行回调 → 结果串仍为「已作答 0/N」。
- **影响**：上述三页；恢复记录后旧分数/旧提示被误作当前结果。与 M-N3 同类，但属本批新页。
- **方案**：恢复回调统一 `render(); calc();`；未答完时清空旧结果与导出/复制状态，避免旧值残留。

### M-N13 DHI 至少 4 题维度标签错配，三维分与图表错位（高，确认）
- **描述**：DHI 的 P（躯体）/E（情感）/F（功能）标签沿固定数组硬编码分配，未按题干语义逐题核对；多道题被归入错误维度。
- **证据**：`tools/neurology/dhi.html:236-261` 题目数组、`:316-318` 三维分展示、`:559` 柱图、`:363-365` CSV。`node` 解析该数组得 P7/E9/F9 题，但逐题语义核对发现：Q2「感到沮丧/烦恼」标 `F`（应为 E）、Q3「限制社交/家庭活动」标 `E`（应为 F）、Q7「快速移动头部即头晕」标 `F`（应为 P）、Q13「避免快速上下楼梯」标 `P`（应为 F）。复算：仅 Q2 选 4 → **F=4、E=0**；仅 Q3 选 4 → **E=4、F=0**。
- **影响**：`tools/neurology/dhi.html`；三维分、柱图、CSV、门诊记录均把情绪/功能/躯体混算，用户按维度定位主因时被误导。总分不受影响，分维度结论失真。
- **方案**：按题干语义重标 4 题（并全表复核），保持 P/E/F 题数 7/9/9 与满分 28/36/36；增加「单题作答 → 仅对应维度 +4」的断言测试。

### M-N14 DHI 同一分值存在两套分级口径（中，确认）
- **描述**：页面表格与代码用 4 档（0–16 / 18–34 / 36–52 / 54–100），公式、FAQ 与引据表却用 3 档（0–30 / 31–60 / 61–100）；同一分数会得到两个不同等级。
- **证据**：`tools/neurology/dhi.html:149-152` 4 档表、`:303-306` 代码同 4 档、`:190` FAQ「0~30 轻度、31~60 中度、61~100 重度」、`:219` 引据表同 3 档、`:186` 示例又写「52 分…中度（31~60）」。`node` 复算：总分 20 → 代码/表格「轻中度障碍」，FAQ「轻度」；总分 53 → 代码「重度障碍」，FAQ「中度障碍」。
- **影响**：`tools/neurology/dhi.html`；读者无法用同一把尺核对结果，示例与结果引擎也不一致。
- **方案**：由专业人员依据所引文献裁定一套划界分，抽成单一 `DHI_BANDS` 常量，表格、FAQ、示例、CSV、EMR 全部由它生成；补 16/18/34/36/52/54 边界用例。

### M-N15 DHI 英文门诊记录 P/F 满分分母互换（中，确认）
- **描述**：中文门诊记录写 P/28、E/36、F/36，英文同一行却写 Physical/36、Functional/28，两个维度分母对调。
- **证据**：`tools/neurology/dhi.html:429-430`；中文 `'躯体(P) '+sub.P+'/28 · 情感(E) '+sub.E+'/36 · 功能(F) '+sub.F+'/36`，英文 `'Physical (P) '+sub.P+'/36, emotional (E) '+sub.E+'/36, functional (F) '+sub.F+'/28'`。全选「是」复算实际 P=28/E=36/F=36，英文文本却呈现 P/36、F/28。
- **影响**：`tools/neurology/dhi.html` 英文病历摘要的分维度满分错误，影响复核与转抄。
- **方案**：三个分母由同一常量对象提供，中英文都引用；加英文 EMR 字符串断言 `P/28, E/36, F/36`。

### M-N16 SAS 页面重复整块「相关工具」且第二块描述被截断（中，确认）
- **描述**：同一页连续出现两个完全相同的 `related-tools` 区块（同 6 个链接）；第二块的多条卡片描述在句子中途被截断。
- **证据**：`tools/psychology/sas-assessment.html:246-274` 与 `:275-304` 两个 `<div class="related-tools" data-related-tools="1">`；`node` 计数为 2。第二块截断样本：`:285` 结尾「适合心理学学习与」、`:293` 结尾「被下列」、`:297` 结尾「入睡时」。
- **影响**：`tools/psychology/sas-assessment.html`；相关工具重复 6 条、可见残句，页面体积与重复内容增加，且易被误认为两组不同推荐。
- **方案**：删除第二块（`:275-304`），保留完整的第一块；增加静态检查「每页 `data-related-tools` 至多 1 个」。

### M-N17 C-SSRS 行为题未答时「复制结果」仍写「自杀行为无」（高，确认）
- **描述**：`copyResult()` 只校验 5 道意念题是否答完，不校验 4 道行为题与「近 3 个月」补充项；行为题全空时仍输出「自杀行为无」，把未采集信息写成阴性。
- **证据**：`tools/psychiatry/cssrs-suicide.html:459-463` 仅 `doneI<IDE.length` 拦截，`:463` 用 `B.some(v===0)` 判定；而 `calc()` 在 `:344-346` 明确要求 `doneB<BEH.length` 或 `RECENT` 缺失即不评估。`node` 复算 `B=[-1,-1,-1,-1]` → `some(v===0)=false` → 复制文本「意念等级 X/5，自杀行为无」。
- **影响**：`tools/psychiatry/cssrs-suicide.html`；部分完成的危机筛查可被复制成「无自杀行为」的阴性结论，属安全相关的高风险误读。
- **方案**：复制前校验 `doneB===BEH.length` 及 `B[3]===0 → RECENT>=0`；未完成时只提示「未完成，不可复制」，禁止用未答题推断阴性。

### M-N18 C-SSRS 引据写「6 个筛查问题 + 4 个分量表」，页面实际 9 题（中，确认）
- **描述**：引据徽标声称该工具是 6 题筛查版，但页面实际实现 5 道意念题 + 4 道行为题共 9 题，用户无法与原始 6 题筛查版对应。
- **证据**：`tools/psychiatry/cssrs-suicide.html:151` 引据文本「6 个筛查问题 + 4 个分量表」；`:280-286` `IDE` 5 题、`:287-292` `BEH` 4 题，合计 9 题。`node` 计数 5+4=9。
- **影响**：`tools/psychiatry/cssrs-suicide.html`；量表版本、题量与文献描述不一致，影响专业可信度与结果解释。
- **方案**：二选一——改为如实描述「5 意念 + 4 行为（改编自 C-SSRS 筛查版）」并注明改编；或按官方 6 题筛查版收敛条目并给出计分映射。

### M-N19 Berg 仅答 1 项即输出完整平衡分级与跌倒风险（中，确认）
- **描述**：`calcScore()` 只在「0 项已答」时返回；只要有 1 项作答，就用该部分总分套完整分级，标题直接显示「严重平衡障碍 / 高跌倒风险」，未完成提示排在结果之后。
- **证据**：`tools/rehabilitation/berg-balance-scale.html:296-333`，`:304` 仅 `answered === 0` 早退，`:310-314` 用部分 `total` 分级，`:327-329` 才追加「还有 N 项未评分」。`node` 复算：仅第 1 项选 4 → `total=4` → **「严重平衡障碍」「高跌倒风险」，并显示「已完成 1/14 项」**。门诊记录 `:488` 有 `done<bbsItems.length` 守卫，但结果区没有。
- **影响**：`tools/rehabilitation/berg-balance-scale.html`；部分作答被当作完整评估，临床分级与跌倒风险被严重误读。
- **方案**：分级与跌倒风险仅在 14/14 时输出；未完成时只显示当前已得总分与「不可分级」，与 EMR 守卫保持一致。

### M-N20 Berg 跌倒风险线性外推可超过 100%「增加」且无上限（中，确认）
- **描述**：`fallRisk = (45 - total) × 7` 被直接当作「跌倒风险增加百分比」，在低总分时得到远超 100% 的无意义数值。
- **证据**：`tools/rehabilitation/berg-balance-scale.html:316` 结果区、`:359` CSV 同式、`:323` 拼「估算增加约 X%」。`node` 复算：`total=0 → 315%`、`total=4 → 287%`、`total=44 → 7%`；深扒 `:185` 也写「<45 跌倒风险=(45-总分)×7%」。
- **影响**：`tools/rehabilitation/berg-balance-scale.html`；「风险增加约 315%」不符合百分比语义，削弱专业可信度，也可能被误读为真实概率。
- **方案**：去掉「% 增加」表述，改为「低于 45 分 N 分（每分约 7% 线性估算）」或直接引用验证过的分层风险；如需百分比，必须封顶并注明为经验估算。

### M-N21 英文 CSV 表头已翻译、逐题题干仍为中文（中，确认）
- **描述**：英文导出分支翻译了表头、选项与汇总，但逐题题干仍直接取中文 `QS`，英文报告无法阅读与复核。
- **证据**：`tools/psychiatry/gad7-anxiety.html:298,317`（`__gd7Text(i){ return QS[i]; }` 用于英文 CSV）；`tools/psychiatry/isi-insomnia.html:300,319`；`tools/psychiatry/ybocs-ocd.html:306,327`；`tools/psychiatry/eat26-eating.html:331` 直接 `row((i+1),q,...)`。源码确认英文分支仍返回中文题干；未做 `?lang=en-US` 实机导出验证。
- **影响**：上述四页；英文 CSV 题目不可读，与 M-N8 同类但属本批新页。
- **方案**：接入经核准的英文题目层；无可靠译本时在表头标注原语言，不自行翻译标准量表条目；增加英文 CSV 题目非 CJK 断言。

### M-N22 GAD-7 / ISI / Y-BOCS 深度解析示例与分级表冲突（低，确认）
- **描述**：三页的示例标题/描述给出的等级与同页分级表、结果引擎不一致，读者对照时会得到互相矛盾的结论。
- **证据**：`tools/psychiatry/gad7-anxiety.html:189` 示例「总分 12（中度）… ≥14 考虑药物」，分级表 15+ 才是重度；`node` 复算 `grade(12)=中度`、`grade(14)=中度`、`grade(15)=重度`。`tools/psychiatry/isi-insomnia.html:191` 示例 14 分称「中度」，代码 `:279` 14 分是「亚临床失眠」；`:192` 21 分称「重度」，代码 `:280` 21 分是「中度失眠」。`tools/psychiatry/ybocs-ocd.html:190` 20 分称「中重度」、`:194` FAQ 写「16–23 中重、24–32 极重」，而表 `:157-159` 与代码 `:284-286` 为 16–23 中度、24–31 重度、32–40 极重度；`node` 复算 `level(20)=中度`。
- **影响**：上述三页；示例失去教学价值，且暗示与真实分级不同的阈值。
- **方案**：示例分数与等级由同一 `BANDS` 常量生成，禁止手写等级；补边界分数（14/15、21/22、23/24/31/32）快照测试。

### M-N23 ISI `__isiOpts` 引用未定义变量 `OPTS` 的不可达分支（低，确认）
- **描述**：ISI 页面没有定义 `OPTS`，`__isiOpts` 的字符串分支却返回 `OPTS`；当前 `QS` 全为对象故分支不可达，一旦数据改成字符串题干即抛 `ReferenceError`。
- **证据**：`tools/psychiatry/isi-insomnia.html:299` `return typeof q==='string'?OPTS:q.o;`；全文件无 `var OPTS`（对比 GAD-7 `:239` 有定义）。`node` 检查该标识符为 `undefined`，且 `QS` 各项均为 `{o:[...]}` 对象，故当前不触发。
- **影响**：`tools/psychiatry/isi-insomnia.html`；潜在运行时崩溃，属隐藏地雷。
- **方案**：删除该分支直接 `return q.o;`，或补定义 `OPTS`；若支持字符串题面需同时提供选项数组。

### M-N24 Berg 重置后旧柱状图仍保留（低，确认）
- **描述**：`resetAll()` 只取消单选并重置结果区，未清空 `#bergChart`；旧的各项目得分柱图在重置后继续显示。
- **证据**：`tools/rehabilitation/berg-balance-scale.html:415-418` 重置函数；图表在 `:433-438` 由 `__bergExtras()` 绘制，只有 `calcScore`/DOMContentLoaded 触发；`resetAll` 未调用 `__bergExtras` 或清空 `#bergChart`。
- **影响**：`tools/rehabilitation/berg-balance-scale.html`；重置后结果与图表状态不一致，用户可能把旧图当作当前答卷。
- **方案**：重置时同步清空 `#bergChart`、移除 EMR 框并重置导出状态；或将图表重绘纳入统一 `renderEmpty()`。

### M-N25 DHI 本地答案恢复监听为死代码（低，确认）
- **描述**：页面尾部注册了 `input/change` 自动保存与 `DOMContentLoaded` 恢复逻辑，但所有单选框只有 `name` 没有 `id`，保存与恢复函数首行即 `if(!el.id)return;`，整段逻辑永不生效。
- **证据**：`tools/neurology/dhi.html:277-279` 生成 `<input type="radio" name="qN" value=...>`（无 id）；`:513-543` 保存/恢复脚本 `:524`、`:536` 均要求 `el.id`。`node` 读取生成模板确认无 `id=` 属性。
- **影响**：`tools/neurology/dhi.html`；用户以为答案会本机保存，刷新后实际丢失；死代码也增加维护成本。
- **方案**：若不打算持久化则整段删除；若要保留，为每题单选框补稳定 `id`，并在恢复后调用 `calc()` 重算。

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

## 2026-11-04 T 批 psychiatry（rater/CD-RISC/CAGE/LSAS/PHQ-9/C-SSRS/PANSS）

### M-N26 rater-24 25 题默认全选「2-有时」，未作答即出分级（高，确认源码缺陷）
- 问题：`buildList()` 给每一题的 `<option value="2" selected>2-有时</option>` 预选，25 个下拉全部默认 2；`calc()` 直接对全部 select 求和，没有未答状态或完成度校验；页面尾部 `buildList();calc();` 立即执行，因此首次打开就得到 50 分并写入分级/门诊记录。
- 证据：`tools/psychiatry/rater-24.html:200`（默认 `selected`）、`:246-252`（无条件累加、`max=items.length*4`）、`:255-257`（≥50 判「中等」）、`:312`（首屏 `calc()`）。
- 复现：不做任何选择打开页面 → 总分 50/100、等级「中等心理韧性」（`node -e` 复算 25×2=50，命中 ≥50 分支）；只把第 1 题改为 0 → 48/100「低心理韧性」。期望：未答时显示「已作答 0/25」，不给出等级、标尺和门诊记录。
- 影响：`tools/psychiatry/rater-24.html`；默认值被当作受试者作答，只答 1 题也能得到一份完整的 48 分报告，结果系统性偏向中档。
- 方案：默认 `value=""` 或内部 `-1`，`calc()` 首行判 `done<25` 只输出进度提示；门诊记录/导出同样加完成度守卫。

### M-N27 rater-23 恐惧/回避 48 个下拉默认全为「2」，首屏即「显著社交焦虑」（高，确认源码缺陷）
- 问题：每个情境的恐惧与回避两个 select 都写了 `value="2" selected`（24 情境 ×2=48 个控件）；`calc()` 无完成度校验，尾部 `buildList();calc();` 直接计算，打开页面即 96 分「显著社交焦虑」。
- 证据：`tools/psychiatry/rater-23.html:210-211`（两处 `selected`）、`:216-229`（无条件累加，`maxTotal=lsasItems.length*3*2`）、`:232-236`（96<105 判「显著」）、`:322`（首屏 `calc()`）。
- 复现：打开页面 → 恐惧 48 + 回避 48 = 96/144 → 「显著社交焦虑」（`node -e` 复算 24×2×2=96）；只把第 1 情境两项改 0 → 92 仍「显著」。期望：未开始时为 0/48 并提示继续作答。
- 影响：`tools/psychiatry/rater-23.html`；未评估即产出高等级结论与门诊记录，且部分作答永远无法低于默认基线。
- 方案：默认空值 + `done<48` 守卫；结果区、CSV、门诊记录三个入口统一拦截。

### M-N28 cdrisc-resilience 实为 CD-RISC-10（0–40），解析与引据仍写 25 条/0–100（高，确认源码缺陷）
- 问题：页面实现 10 个条目、满分 40（`/40`、分级 ≤19/20–29/≥30），但深度解析、FAQ 与引据表沿用 25 条版本，写「25 题、0–100」，并给出 60、82 这类在 0–40 量程内不可能出现的分数。
- 证据：`tools/psychiatry/cdrisc-resilience.html:126`（公式：10 条/满分 40）、`:13`、`:16`（meta 亦为 CD-RISC-10/0–40）、`:156`（30-40 较高）、`:187-188`（示例「总分 60/100」「高韧性 82」）、`:191`（FAQ「0–100」）、`:215`（引据表「总分范围 0–100」）、`:383`（门诊记录写 10 条目）。
- 复现：10 题全选 4 → 40/40（100%），等级「较高」；页面示例 60、82 无法通过任何作答组合得到（`node -e`：60>40、82>40 均为 false，超出量程）。期望：示例落在 0–40（如 24/40、34/40），引据/FAQ 统一为 10 条、≤19 较低 / 20–29 中等 / ≥30 较高。
- 影响：`tools/psychiatry/cdrisc-resilience.html`；用户按示例核对会得到矛盾结果，FAQ 与引据把简版误作 25 条原版。
- 方案：以 `:126` 为唯一口径改写 `:187-191`、`:209-221`；示例数字用 node 实算后填（如 6/10/8 分组合 = 24）。

### M-N29 lsas-social 参考标尺 ≥91 段误标「无/轻度」绿色（高，确认源码缺陷）
- 问题：结果标尺最后一段为 `{"lo":91,"hi":null,"label":"无/轻度","color":"#10B981"}`，而同一页的结果分级 ≥91 是「极重度」（红色）。
- 证据：`tools/psychiatry/lsas-social.html:301`（refBar 末段 label/颜色）、`:304`（`__lsasSev`：>90 → 极重度）。
- 复现：24 个情境恐惧、回避全选 3 → 总分 144（`node -e` 24×3×2=144）→ 结果区「极重度…功能严重受损」，标尺最右端区间却显示「无/轻度」并着绿色。期望：末段 label「极重度」、颜色 `#EF4444`。
- 影响：`tools/psychiatry/lsas-social.html`；最重的一档在标尺上被显示为正常，视觉结论与文字结论相反。
- 方案：改正末段 label/color；补一条 91 分边界的渲染断言。

### M-N30 lsas-social 公式框「恐惧=11项、回避=11项」与实际 24 项冲突（高，确认源码缺陷）
- 问题：公式框称恐惧、回避各 11 项（对应每维满分 33），实际每个情境同时录入恐惧与回避，共 24 项、每维 0–72、总分 0–144。
- 证据：`tools/psychiatry/lsas-social.html:129`（公式原文）、`:216-229`（逐情境累加两列，`maxTotal=lsasItems.length*3*2`）。
- 复现：全部选 3 → 恐惧 72 + 回避 72 = 144（`node -e` 24×3=72），页面/导出均按 144 计算；若按公式 11 项，每维上限只有 33。期望：公式写「恐惧=24项、回避=24项，各 0–72，总分 0–144」。
- 影响：`tools/psychiatry/lsas-social.html`；临床人员按公式手算会与工具结果相差一倍以上。
- 方案：改公式文案；把 24/72/144 抽成页面常量，公式、标尺、导出统一引用。

### M-N31 self-assess-4 未作答默认「从不」，打开即判「筛查阴性」（高，确认源码缺陷）
- 问题：6 个 select 没有占位/未选态，浏览器默认选中首项 `value="0"`「从不」；`calc()` 把 0 当作真实作答，尾部 `buildList();calc();` 使首屏就输出 0 阳性、总分 0/24 与「筛查阴性」。
- 证据：`tools/psychiatry/self-assess-4.html:181-187`（选项从 0 开始、无 placeholder）、`:191`（select 无默认空值）、`:206-222`（0 分走 `else` 分支「筛查阴性」）、`:330`（首屏 `buildList();calc();`）。
- 复现：打开页面不点任何选项 → 阳性 0/6、原始总分 0/24、结论「筛查阴性…注意力功能在正常范围」（`node -e` 复算 6×0=0，positiveCount=0<4）。期望：未答时显示「已作答 0/6」，不出结论/分型/导出。
- 影响：`tools/psychiatry/self-assess-4.html`；未筛查的人可得到「正常」结论，是最典型的缺答判阴性。
- 方案：插入 `<option value="-1">请选择</option>` 并默认选中，`calc()` 先判 6 项是否全部 ≥0。

### M-N32 self-assess-4 ★ 阳性标记写死在选项上，与各题 positiveFrom 不一致（高，确认源码缺陷）
- 问题：选项标签把「有时 ★ / 经常 ★ / 非常频繁 ★」写死，`buildList()` 里算出的 `isPositive` 变量从未使用；但第 4–6 题 `positiveFrom:3`，选「有时」(2 分) 并不计阳性，界面却仍显示 ★。页面说明又写明「带 ★ 标记的选项为阳性项」。
- 证据：`tools/psychiatry/self-assess-4.html:173-179`（题 4–6 `positiveFrom:3`）、`:184-186`（★ 固定写在 value 2/3/4）、`:192-194`（`isPositive` 计算后未参与模板）。
- 复现：第 4 题选「有时」→ 明细表该行「阳性」列为「否」、阳性计数 0/6 不增加，但选项本身显示「有时 ★」；期望 ★ 只出现在 `v>=item.positiveFrom` 的选项上（题 4–6 应从「经常」起标 ★）。
- 影响：`tools/psychiatry/self-assess-4.html`；用户会把非阳性作答当成阳性项，误判自己达到筛查阈值。
- 方案：按 `item.positiveFrom` 生成标签（`v>=item.positiveFrom` 才追加 ★），并删除未使用的 `isPositive`。

### M-N33 calc-1 PHQ-9 未答默认 0，打开即「无或极轻微抑郁」（高，确认源码缺陷）
- 问题：9 个计分项的 select 从 `0 没有` 开始且无未答态，`DOMContentLoaded` 直接 `renderItems();loadState();calc();`，未作答即按 0 分给出完整分级与建议。
- 证据：`tools/psychiatry/calc-1.html:255-258`（选项 0–3、无 placeholder）、`:324`（首屏 `calc()`）、`:281-288`（`score<=4` → 无/极轻）。
- 复现：打开页面不选任何项 → 总分 0 → 「无或极轻微抑郁」+ 建议；`node -e` 复算 9×0=0 命中 `<=4`。期望：显示「已作答 0/9」并不出分级/导出。
- 影响：`tools/psychiatry/calc-1.html`；空表单被当成「无抑郁」证据，且可复制门诊记录。
- 方案：默认 `-1`/占位选项，`calc()` 首行完成度守卫；`loadState()` 恢复后同样校验。

### M-N34 calc-1 深度解析「总分 15（中度）」与本页分级表 15–19 中重度矛盾（中，内容与分级表冲突）
- 问题：示例给 9 项 `2,2,2,1,2,2,2,1,1`，合计 15，标题与正文都写「中度抑郁」；同页分级表和代码均为 15–19「中重度」。
- 证据：`tools/psychiatry/calc-1.html:169`（分级说明 15–19 中重度）、`:288-289`（`score<=14` 中度、`<=19` 中重度）、`:517`（示例「总分 15（中度）」）。
- 复现：输入上述 9 项 → 总分 15（`node -e` 求和=15）→ 结果区「中重度抑郁」，而示例文案称「中度抑郁」。期望：示例标「中重度」，或改分值组合使 ≤14。
- 影响：`tools/psychiatry/calc-1.html`；用户照示例核对会认为工具分级错误。
- 方案：改示例标题/正文为「中重度」；补 14/15 边界用例。

### M-N35 assessor-risk-5 未评估默认全「否」，首屏即「极低风险/无自杀意念」（高，确认源码缺陷）
- 问题：5 个意念项 + 3 个行为项的 select 只有「否/是」，默认「否」；`calc()` 无完成度守卫，页面尾部 `buildList(...);calc();` 直接执行，未勾选任何一项就输出「极低风险」「当前无自杀意念和行为」，并写入门诊记录数据。
- 证据：`tools/psychiatry/assessor-risk-5.html:252-256`（`<option value="0">否</option>` 默认）、`:323-328`（累加后 `maxIdeation` 初值 -1）、`:356-357`（else 分支「极低风险/当前无自杀意念和行为」）、`:406-408`（首屏 `calc()`）。
- 复现：打开页面不做任何评估 → 风险等级「极低风险」、意念 0 级、自杀行为「无」、非自杀性自伤「无」（`node -e`：8 项全 0 → maxIdeation=-1 → 走 else 分支）。期望：未完成时显示「未完成评估，不可判定」，不生成等级与门诊记录。
- 影响：`tools/psychiatry/assessor-risk-5.html`；自杀风险工具出现假阴性，最严重可被当作「已筛查无风险」写入病历。
- 方案：默认空值 + 8 项全部作答才计算；未完成时禁用复制/导出，结果区显示「不可判定」。

### M-N36 panss-schizophrenia 公式框把一般精神病理写成 7 项（实为 16 项）（高，确认源码缺陷）
- 问题：公式写「一般精神病理分(7项)」，按此 7+7+7=21 项、满分只有 147；实际 QS 为 30 条、G 为 16 条（i≥14），结果卡也标「一般G(16-112)」、总分 /210，meta 同样写 G(16)。
- 证据：`tools/psychiatry/panss-schizophrenia.html:127`（公式「7项」）、`:13`、`:16`、`:215`（meta/说明均 G(16)，共 30 条）、`:243-276`（QS 30 条，`i<7` P、`i<14` N、其余 G）、`:291`（标签「一般G(16-112)」）。
- 复现：30 项各评 1 → 总分 30/210（`node -e` 30×7=210）；若按公式 21 项，满分应为 147（21×7），与结果卡的 /210 冲突。期望：公式写「阳性(7项) + 阴性(7项) + 一般精神病理(16项) = 30 项，30–210」。
- 影响：`tools/psychiatry/panss-schizophrenia.html`；临床人员按公式手算 G 分与工具结果相差 9 项，量程也差 63 分。
- 方案：改公式文案；由 QS 派生子量表长度，避免再出现硬编码 7/16。

### M-N37 phq9-depression 预设「中度（一半天数）」实得 18 分判中重度（高，阈值与标签矛盾）
- 问题：按钮「🟠 中度（一半天数）」调用 `applyQuizPreset(2)`，把 9 项全部置 2；9×2=18，按页面分级为「中重度抑郁」，与按钮标签「中度」不一致。
- 证据：`tools/psychiatry/phq9-depression.html:144`（按钮文案与 `applyQuizPreset(2)`）、`:307-310`（`A=A.map(function(){return j;})` 全项同值）、`:283-284`（≤14 中度、≤19 中重度）。
- 复现：点击该预设 → 9 项均为「一半以上天数」→ 总分 18（`node -e` 9×2=18）→ 结果「中重度抑郁」；期望按钮标「中重度（一半天数）」，或预设改为 1/2 混合使总分落在 10–14。
- 影响：`tools/psychiatry/phq9-depression.html`；预设名称与产出等级不符，演示/教学时会被当成分级错误。
- 方案：改按钮文案为「中重度」，或给 10–14 单独设计一组混合分值；预设与分级表共用同一常量。

### M-N38 phq9-depression 恢复历史后只重绘不重算，结果仍是上一份答卷（高，确认源码缺陷）
- 问题：`__quizMountHist()` 的恢复回调把 `A` 换成历史答案后只调 `render()`；`render()` 仅更新选项高亮和进度，不触发 `calc()`，因此 `#result`（含门诊记录）保留恢复前的分数与结论。
- 证据：`tools/psychiatry/phq9-depression.html:330-333`（恢复回调仅 `render()`）、`:255-263`（`render()` 不清算结果）、`:269`（只有 `pick()` 才 `calc()`）。
- 复现：9 项全选 3 → 27/27「重度」；再全部改 0 → 0/27「无抑郁」；点击历史记录 → 界面 9 项恢复为 3 分高亮，结果区仍写「无抑郁」。期望：恢复后立即重算并显示 27/27「重度」。
- 影响：`tools/psychiatry/phq9-depression.html`；旧结论会被误当作所恢复记录的结果，与 M-N3 同类但属新页面。
- 方案：回调末尾调用 `calc()`；恢复时先清空旧结果与门诊记录，避免生成重复历史。

### M-N39 cage-substance 恢复历史后只重绘不重算，结果仍是上一份答卷（高，确认源码缺陷）
- 问题：`__cageMountHist()` 恢复时只 `render()`，不调用 `calc()`，4 个选项高亮切到历史答案，结果区仍显示恢复前的阳性计数/结论。
- 证据：`tools/psychiatry/cage-substance.html:328-332`（恢复回调仅 `render()`）、`:243-251`（`render()` 只重绘）、`:253-257`（`pick()` 才 `calc()`）、`:386`（首屏 `render();calc();`）。
- 复现：4 项全「是」→ 4/4 阳性；再全改「否」→ 0/4 阴性；点击历史记录 → 4 个「是」恢复高亮，结果仍「0/4 阴性」（`node -e` 按 0 为是的计分复算为 4）。期望：恢复后重算并显示 4/4 阳性。
- 影响：`tools/psychiatry/cage-substance.html`；CAGE 阳性/阴性与界面答案相反，可导致漏判。
- 方案：恢复回调补 `calc()`；同时清理旧门诊记录与导出状态。

## T 批 psychiatry 覆盖（2026-11-04）
- 本轮审计 12 页：`tools/psychiatry/rater-24.html`、`tools/psychiatry/cdrisc-resilience.html`、`tools/psychiatry/cage-substance.html`、`tools/psychiatry/lsas-social.html`、`tools/psychiatry/phq9-depression.html`、`tools/psychiatry/rater-23.html`、`tools/psychiatry/les-stress.html`、`tools/psychiatry/self-assess-4.html`、`tools/psychiatry/assessor-risk-5.html`、`tools/psychiatry/mmpi2-personality.html`、`tools/psychiatry/calc-1.html`、`tools/psychiatry/panss-schizophrenia.html`。
- 新增 14 条（高 13 / 中 1），编号 M-N26–M-N39；假工具候选 0 页（12 页均有真实计分实现；`rater-24`/`rater-23` 属默认预选导致「无输入即出结论」，已按高优缺陷记录，不计为假工具）。
- `les-stress`、`mmpi2-personality` 无高优缺陷，整页跳过（前者 0 事件即「低风险」符合核对表语义，后者默认 T=50 为明示的总体均值；二者仅有文案/钳位类低优问题）。
- 未做浏览器/门禁/线上验证：证据均为源码行号 + `node -e` 按页面原表达式/原数组内存复算，未开浏览器、未跑 `_build.py`/门禁、未核各量表标准阈值与授权译本。

## U 批 · 精神科量表复核（2026-11-04）

> 本批只读复核既有条目：逐页读当前源码并复算，只登记「仍成立的高优」与「已失效需重开」两类；所有量表阈值、分级与临床解读**需临床复核**。未开浏览器、未跑门禁/线上。

### M-N40 PCL-5 症状群仍按 >0 计数，门诊记录按 ≥2（原 M-N1，仍成立，高）
- 页面：`tools/psychiatry/pcl5-ptsd.html`
- 现状：页面与导出仍 `filter(v>0)`（`:294-298`、`:356-360`），门诊记录仍 `A[i]>=2`（`:452-455`）；两套阈值同时存在。
- 复现：第 1/6/8/9/15/16 题各选 1、其余 0 → 实际总分 6/80、页面「DSM-5 症状群筛查：符合」，门诊记录阳性条目 0。期望症状群按每条 ≥2 计，或两处统一口径。
- 结论：仍成立；假工具：否；需临床复核（PCL-5 版本与症状群算法须专业确认）。

### M-N41 MDQ 补充题未完成仍写「目前未达筛查阳性 / screen negative」（原 M-N2，仍成立，高）
- 页面：`tools/psychiatry/mdq-bipolar.html`
- 现状：`:432` 结论写「待补充第二/三部分」，但 `:437-438` 的 hint 只用 `screen`（`:429` 在 P2/P3 未答时为 false），仍输出「未达 MDQ 筛查阳性 / screen is currently negative」。
- 复现：第一部分 13 题全「是」、P2/P3 不答 → 实际同时出现「待补充」与「阴性」；期望统一为「不可判定」并阻止复制门诊记录。
- 结论：仍成立；假工具：否；需临床复核。

### M-N42 恢复量表历史后仍只重绘不重算（原 M-N3，PCL-5/MDQ 仍成立，高）
- 页面：`tools/psychiatry/pcl5-ptsd.html`、`tools/psychiatry/mdq-bipolar.html`
- 现状：恢复回调末尾仍只有 `render()`（PCL-5 `:399-403`、MDQ `:374-379`），未调用 `calc()`；结果区与门诊记录保留上一份答卷。
- 复现：PCL-5 先全 0（0/80）再恢复全 2 → 界面已全 2，结果仍 0/80；MDQ 先阴性再恢复阳性答案 → 结果仍阴性。期望恢复后立即重算。
- 结论：仍成立（PDSS 部分未在本批复核）；假工具：否；需临床复核。

### M-N43 多量表回溯期仍统一为「最近两周」（原 M-N4，PCL-5/AQ/MDQ 仍成立，高）
- 页面：`tools/psychiatry/pcl5-ptsd.html`、`tools/psychiatry/aq-autism.html`、`tools/psychiatry/mdq-bipolar.html`
- 现状：`psych-kit.js` 配置仍写 `period:"最近两周"`（PCL-5 `:542`、AQ `:544`、MDQ `:519`），与 PCL-5「过去一月」、MDQ「既往」、AQ 特质性题干不符。
- 复现：首次打开任一页 → 提示均按两周作答；期望按各量表原始回溯期或无回溯期说明。
- 结论：仍成立；假工具：否；需临床复核（版本授权与回溯期）。

### M-N44 EAT-26 正/反向计分数组仍互换（原 M-N9，仍成立，高）
- 页面：`tools/psychiatry/eat26-eating.html`
- 现状：`OPTS[0]=总是`，但 `NORM=[0,0,0,1,2,3]`、`REV=[3,2,1,0,0,0]`（`:241-243`），`:300` 仍按 `REV_IDX?REV:NORM` 累加。
- 复现：26 题全「总是」→ 实际 9 分（低风险）；全「从不」→ 69 分（≥20 高风险）。期望正向 `[3,2,1,0,0,0]`、反向 `[0,0,0,1,2,3]`，全总是=69、全从不=9。
- 结论：仍成立；假工具：否；需临床复核（8/13/25 反向题归属）。

### M-N45 Y-BOCS 抵抗/控制 4 条仍未反向计分（原 M-N11，仍成立，高）
- 页面：`tools/psychiatry/ybocs-ocd.html`
- 现状：`:278` 仍 `A.reduce(...)` 原始分直加，`:427-430` 门诊记录同；`:240` 选项为「无→极重度」，题面却写「越努力抵抗得分越低」。
- 复现：第 4 题选「极重度抵抗」、其余 0 → 实际总分 4「亚临床」；第 4 题选「无」→ 0 分，抵抗越强分越高。期望 4 条抵抗/控制题反向计分。
- 结论：仍成立；假工具：否；需临床复核。

### M-N46 C-SSRS 行为题未答时「复制结果」仍写「自杀行为无」（原 M-N17，仍成立，高）
- 页面：`tools/psychiatry/cssrs-suicide.html`
- 现状：`:459-463` 的 `copyResult()` 只校验 `doneI`，未校验 `doneB`/`RECENT`；`B.some(v===0)` 在行为全未答时返回 false。
- 复现：5 个意念题答完、4 个行为题不答 → 页面结果被 `:346-347` 拦截为「请完成全部问题」，但点复制仍输出「自杀行为无」。期望复制同样拦截，或写「行为项未评估」。
- 结论：仍成立；假工具：否；需临床复核（自杀风险工具，优先级最高）。

### M-N47 CD-RISC 实为 10 条/0–40，解析与引据仍写 25 条/0–100（原 M-N28，仍成立，高）
- 页面：`tools/psychiatry/cdrisc-resilience.html`
- 现状：实现仍 10 条、满分 40（`:126` `:383`），但 `:187-188` 示例仍写「总分 60/100」「高韧性 82」，`:191` FAQ 与 `:215` 引据仍「0–100」。
- 复现：10 题全 4 → 40/40（100%）；页面示例 60、82 在 0–40 量程内不可能出现。期望示例改 24/40、34/40 等，FAQ/引据统一为 10 条与 ≤19/20–29/≥30 分级。
- 结论：仍成立；假工具：否；需临床复核。

### M-N48 LSAS 参考标尺 ≥91 段仍标「无/轻度」绿色（原 M-N29，仍成立，高）
- 页面：`tools/psychiatry/lsas-social.html`
- 现状：`:301` 末段仍 `{"lo":91,"hi":null,"label":"无/轻度","color":"#10B981"}`，而 `:304` 的 `__lsasSev` ≥91 为「极重度」。
- 复现：24 情境恐惧、回避全 3 → 144 分「极重度…功能严重受损」，标尺最右却绿色「无/轻度」。期望末段 label「极重度」、颜色红。
- 结论：仍成立；假工具：否；需临床复核。

### M-N49 LSAS 公式仍写恐惧/回避各 11 项（原 M-N30，仍成立，高）
- 页面：`tools/psychiatry/lsas-social.html`
- 现状：`:129` 公式仍「恐惧=11项、回避=11项」，实际 `:216-229` 每情境两列共 24 项、每维 0–72、总分 0–144。
- 复现：全选 3 → 恐惧 72 + 回避 72 = 144；按公式 11 项每维上限仅 33、总分 66。期望公式改 24 项/72/144。
- 结论：仍成立；假工具：否；需临床复核。

### M-N50 CAGE 恢复历史后仍只重绘不重算（原 M-N39，仍成立，高）
- 页面：`tools/psychiatry/cage-substance.html`
- 现状：恢复回调仍只 `render()`（`:328-332`），`:243-257` 的 `render()` 不碰结果，只有 `pick()` 才 `calc()`。
- 复现：4 项全「是」→ 4/4 阳性；再全改「否」→ 0/4；点历史恢复 4 个「是」→ 结果仍「0/4 阴性」。期望恢复后重算并显示 4/4。
- 结论：仍成立；假工具：否；需临床复核。

### M-N51 BIS-11 重置或未答完仍残留旧参考标尺（第一轮高优条目，仍成立，高）
- 页面：`tools/psychiatry/bis11-impulse.html`
- 现状：`:272` 的 `resetQuiz()` 只清 `result`，不清理 `#resultRefBar`；`:276-278` 未答完路径直接 return，旧标尺仍保留；标尺在 `:296` 渲染。
- 复现：完成一次高分评估 → 点「重置」→ 答案与文字结果清空，标尺仍显示上一次分值；期望重置与未完成路径同步清空结果、标尺、导出/门诊记录状态。
- 结论：仍成立；假工具：否；需临床复核。

### M-N52 PHQ-15 恢复历史后只重绘、重置不清标尺（第一轮高优条目，仍成立，高）
- 页面：`tools/psychiatry/phq15-somatization.html`（目录实页补入）
- 现状：恢复回调仍只 `render()`（`:351-355`）；`:261` 的 `resetQuiz()` 只清 `result`，`:282` 已绘制的 `#resultRefBar` 不随重置清除。
- 复现：15 题全 2 分 → 30/30；重置 → 结果清空但标尺仍停在 30；或先全 0 再恢复全 2 → 界面全 2、结果仍 0/30。期望恢复后 `calc()`、重置后清标尺。
- 结论：仍成立；假工具：否；需临床复核。

## U 批 精神科复核覆盖（2026-11-04）
- 复核 15 页：任务列出的 13 页（aq-autism、asrs-adhd、bis11-impulse、cage-substance、cdrisc-resilience、cssrs-suicide、eat26-eating、gad7-anxiety、isi-insomnia、les-stress、lsas-social、mdq-bipolar、pcl5-ptsd），另按目录实页补入 `ybocs-ocd.html`、`phq15-somatization.html`；目录中无 `phss.html`。
- 复核结论：13 条高优全部仍成立（M-N40–M-N52，含第一轮 2 条）；已修复 0 条、**已失效 0 条**，无需重开。
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
