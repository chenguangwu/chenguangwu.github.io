# 医疗 · 量表评分类（psychiatry/psychology/clinical-nursing/rehabilitation/neurology 等 ~150 页）

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
