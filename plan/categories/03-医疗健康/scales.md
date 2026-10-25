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
  + clinical-nursing 1（pressure-injury-description）+ neurology 1（psqi）。
  全站累计 **116 页**。psychiatry 已全铺完，psychology 仅剩 scl90（外部 js + psych-kit 通用引擎）与
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
- 🔴 待续（**未铺清单以 2026-10-26 全站 grep 实测为准，勿信早前「已全铺完」口径**）：
  M1 条目结构 / M2 阈值口径仍待老板裁断。当前实测未铺（排除 index）共 **42 页**：
  - `rehabilitation` **已全铺完**（23 个文件：22 个实页全铺 + `analysis-time.html` 为
    `TOOLBOX-REDIRECT` 重定向占位页直跳 gait-analysis、`robots=noindex`，不铺门诊记录）。
    该分类原被误记为「已全铺完」而实际只铺 12 页，本轮 03-32/03-33/03-34 三批补齐 10 页。
  - `psychology` 11：analysis-2、attachment-style-test、bigfive-personality-test、bubble-tea-personality-quiz、
    enneagram-test、generator-20、holland-career-test、random-12、scl90-assessment、tester-2、tester-3
    （多为非病历场景的人格/趣味页；scl90 走外置 js + psych-kit 通用引擎，需另设计）。
  - `cognition` 8：cognitive-assessment、corsi-block-test、digit-span-test、human-benchmark、nback-training、
    schulte-table、stroop-test、time-perception（训练范式，需谨慎标注非标准化常模）。
  - `clinical-nursing` 7：cycle-7、fall-emergency-flow、generator-pressure、ostomy-bag-timing、
    reminder-time-1、restraint-duration、tracheostomy-dressing。
    其中 ostomy-bag-timing / restraint-duration / tracheostomy-dressing / cycle-7 / reminder-time-1
    **用 `new Date()` 算具体时刻**，按铁律④ 暂不纳入稳定用例；generator-pressure 的 `pick()` 走 Math.random，
    输出不稳定（仅「共 N 条」随 `cnt` 变，判别力弱），亦暂缓。
    **fall-emergency-flow 另有硬障碍（2026-10-26 实测，已回滚未提交）**：该页完成度靠全局
    `completedSteps` 数组，而 harness 兜底循环会无参调用 `nextStep()/toggleStep()` 把步骤推满——
    **默认态与注入态实测都是「已完成 8/8 步（全部完成）」**，无法构造判别用例（必成逃生项）。
    想铺此页须先找到绕过兜底的状态通道，否则不动（避免留无测试覆盖的功能）。
  - `neurology` 1：calc-1（NIHSS）；`pediatrics` 2：assessor-spo2（**已踩 stub 盲区**：注入后整段 script 不执行、
    语法正常、errs 空、回滚即恢复，须单独排查）、vaccine-schedule（依赖「今天」，按铁律④ 暂缓）。
  - 「维度雷达图推广」「量表对照模块」未开发。
