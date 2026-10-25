# 医疗 · 量表评分类（psychiatry/psychology/clinical-nursing/rehabilitation/neurology 等 ~150 页）

## 已知问题
### M1. 条目结构重建项（G01-B 系列，需裁断后开发）
- gags-acne 7→6 分区、rater-21 TWSTRS 题量、psqi 成分 5 缺 2 项。
### M2. 阈值口径待裁断（G01-A8）
- kupperman、vanderbilt、asrs。
## 功能缺陷
- 量表页普遍缺「答案回显/打印病历」格式（医生群体要能贴进门诊记录）。
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
- 🔴 待续：其余 ~115 个量表页按同一模板铺开（每批 8–12 页）；M1 条目结构 / M2 阈值口径仍待老板裁断；
  「答案回显/病历打印格式」「维度雷达图推广」「量表对照模块」未开发。
