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
  + pediatrics 4（hearing-screening/ddst-screening/assessor-13/pediatric-asthma）。全站累计 **61 页**。
  顺手修 3 个真 bug：DHI 维度分母互换（P/F 的 28/36 写反）、IRLS 症状特征分母、rater 系满分口径；
  并清理 rater-18/19/22 三条「模板残留假通过」用例（`+j+` 命中页面源码，零判别力，判别力检查从 35 检/3 跳过变为 40 检/0 跳过）。
  - 模板三种变体：① `#result` + 名下 select（nihss 系）；② `#result` + 生成式按钮 `scores`（护理系）；
    ③ `#res`/`#resultBox` + 生成式 select 或 radio（rater/berg 系）。
  - 硬坑：`__emrNote` 容器 id 要可配（`cfg.boxId`）；护理页分级必须自算（harness 的 `scores[undefined]` 会污染页面 total）；
    生成式 select 在 stub DOM 下 `options` 为空，满分要回退 `items[i].o.length-1`；分母以「页面声明的满分」为准。
  - **第三种模板（03-19 起）：记录式钩子**——在 `calc()` 内写 `#result` 之前插 `window.__EMR_SUM={...}`，把页面已算好的分级变量捞出来，
    `__emrData()` 只做排版。适合「计算器型」页（输入→阈值→分级），零逻辑复制、不与页面阈值漂移；问卷型（answers 对象）仍需 clicks 注入。
  - 新增 harness 事实：兜底循环会**无参调用所有顶层 function 声明** ⇒ 新 helper 写成 `var f=function(){}`；复选框注入字段是 `checkIds`；
    `__emrEsc` 会把 `>`/`<`/`&` 转成实体，expect 不能直接写这些字符。
- 🔴 待续：其余 ~90 个量表页按同一模板铺开（每批 3–6 页，逐页核分级口径）；M1 条目结构 / M2 阈值口径仍待老板裁断；
  儿科余 5 页（assessor-spo2 / pediatric-fracture / rater-27 / vaccine-schedule / vanderbilt-adhd）：
  **assessor-spo2 已踩 stub 盲区**（注入后整段 script 不执行，语法正常、errs 空，回滚即恢复）须单独排查；
  vaccine-schedule 依赖「今天」写不出稳定用例。下一批转向 rehabilitation（fim/flacc/nine-hole-peg/walker-height/stretch-duration,
  均为 `#resultBox` + 生成式条目）与 clinical-nursing（iv-drip-rate/gastric-tube-depth/chest-compression-depth 等）；
  「维度雷达图推广」「量表对照模块」未开发。
