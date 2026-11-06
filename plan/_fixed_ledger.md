# 已修条目台账（不提交）

> 用途：记录每批已修的中优条目，避免下批重复排查。ID 与页面均对应 `plan/categories/**` 审计条目。
> 维护规则：主流程每批收口后追加；审计线只写分类文件，本台账只由修复线写。

## 批次 2 · commit afe1c858fd（40 页）

| 分区 | 条目 ID | 页面 | 修复类型 | 验证用例 |
|---|---|---|---|---|
| IT | IT-N54 | tools/it/crc-calculator.html | CRC-8/CCITT 参数校正（poly 0x07/init 0/xorout 0x55） | verify_it_calc.js |
| IT | IT-N60 | tools/it/css-minifier.html | 字符串/url()/注释受保护分词 | verify_it_calc.js |
| IT | IT-N63 | tools/it/date-duration.html | 严格日期校验、逆序报错、口径静态化 | verify_it_calc.js |
| IT（已修补例） | IT-N53/N76/N80 | ipv6 / cron / url-encode | 前序提交已修，仅补回归用例 | verify_it_calc.js |
| 医疗 | D-N6 | tools/healthcare/healthcare.html | 成人剂量>0 守卫、封顶语义澄清 | verify_healthcare_calc.js |
| 医疗 | D-N16 | tools/healthcare/antipyretic-dose.html | 年龄支持小数年、<3 月龄拒算 | verify_healthcare_calc.js |
| 医疗 | D-N22 | tools/healthcare/gfr-cockcroft.html | 身高参与 DuBois BSA 归一，删 170cm 硬编码 | verify_healthcare_calc.js |
| 医疗 | D-N30 | tools/healthcare/bsa-calculator.html | 年龄参与：<18 Haycock、≥18 DuBois | verify_healthcare_calc.js |
| 医疗 | D-N33 | tools/healthcare/qtc.html | 4 公式生效、450/460 上限、延长判定 | verify_healthcare_calc.js |
| 医疗 | D-N10 | tools/medical/convert-time-infusion.html | 静态整句告警、独立校验 | verify_medical_calc.js |
| 医疗 | D-N23 | tools/medical/medical-calculator.html | 频率 parseFloat、1–24 校验 | verify_medical_calc.js |
| 医疗 | D-N29 | tools/clinical-nursing/bag-valve-mask.html | 球囊容量参与、频率表统一 | verify_clinical_nursing_calc.js |
| 医疗（已修） | D-N11 | tools/medical/iv-drip-rate.html | HEAD 已修，未重复改动 | 既有 4 条用例 |
| 金融 | F-N38 | tools/finance/provident-fund.html | 年限 1–30 整数、利率 0–10%、0 利率可算 | verify_finance_calc.js |
| 金融 | F-N48 | tools/finance/discount-calculator.html | 反向模式折后价/折扣范围校验 | verify_finance_calc.js |
| 金融 | F-N56 | tools/finance/profit-margin-calculator.html | 毛利<100%、营业<75%、净利可达性 | verify_finance_calc.js |
| 金融 | F-N31 | tools/finance/npv-calculator.html | 折现率 ≤−100% 报错并清空明细/图表 | verify_finance_calc.js |
| 金融 | F-N34 | tools/finance/investment-roi.html | 按年化回报判优、负追加报错 | verify_finance_calc.js |
| 金融 | F-N44 | tools/finance/mutual-fund-calculator.html | 亏损金额补负号 | verify_finance_calc.js |
| 金融 | F-N47 | tools/finance/futures-pnl-calculator.html | 手数/保证金/价格统一校验 | verify_finance_calc.js |
| 金融 | F-N53 | tools/finance/depreciation-calculator.html | 新增各年工作量，按工作量法计算 | verify_finance_calc.js |
| 金融 | F-N57 | tools/finance/stock-profit-calculator.html | 负价/非法输入清空结果并禁用导出 | verify_finance_calc.js |
| 金融（已修补例） | F-N9/N10/N14/N21/N24/N28 | banking / 复利 / 分期 / APY / 贷款 等 | 既有实现已修，仅补判别用例 | verify_finance_calc.js |
| 生活 | LF-N23 | tools/life/daily-calorie-needs.html | 年龄/身高/体重范围校验 | verify_life_calc.js |
| 生活 | LF-N27/N28 | tools/life/candle-burn-time.html | 分钟进位、清空重量复位副行 | verify_life_calc.js |
| 生活 | LF-N50 | tools/life/length-converter.html | 目标单位下拉，swap 真互换 | verify_life_calc.js |
| 生活（已修） | LF-N1/N2/N3/N4/N5 | date-diff / bill-splitter / age-calculator | 前序提交已修，仅补用例 | verify_life_calc.js |
| 设计 | D-N2 | tools/design/color-palette-generator.html | WCAG 亮度选字色并标 AA/AAA | verify_design_calc.js |
| 设计 | D-N7 | tools/design/depth-of-field-calculator.html | 近点恒按公式，仅 s≥h 远点为 ∞ | verify_design_calc.js |
| 设计 | D-N8 | tools/design/focal-length-equivalent.html | 焦距 1–2000mm 校验、空/零清空 | verify_design_calc.js |
| 设计 | D-N16 | tools/design/typography-scale.html | 基准 8–48 夹取回写、非整数报错 | verify_design_calc.js |
| 设计 | D-N17 | tools/design/color-temperature-converter.html | 1000–40000K 校验、清空预览/RGB | verify_design_calc.js |
| 设计 | D-N30 | tools/design/vh-vw.html | 基准空/0/负报错，不回落 1920 | verify_design_calc.js |
| 设计 | D-N34 | tools/design/color-shade-generator.html | 档数 1–20 校验与夹取回写 | verify_design_calc.js |
| 设计 | D-N55 | tools/design/skeleton-loader.html | 圆角 0/时长 0 保留，负数报错 | verify_design_calc.js |
| 设计 | D-N61 | tools/design/pattern-generator.html | 菱形改 conic-gradient，与三角形区分 | verify_design_calc.js |

数据源：`content_deepdive.json` 5 键（gfr-cockcroft / bsa-calculator / qtc / bag-valve-mask / time-format-converter）。
英文键：本批新增/更新约 200 条，41 页探针 0 残留。

## 批次 3 · commit 87b6ccebc7（23 页 / 23 条高优）

| 条目 | 页面 | 修复类型 | 验证用例 |
|---|---|---|---|
| O-1 | tools/it/aes-encryptor.html | ShiftRows/InvShiftRows 补齐第 2 行交换对、删除重复轮转 | 代码复核 + 往返 |
| O-2 | tools/it/rsa.html | OAEP/PSS 分别生成密钥对，签名不再必失败 | verify_it_calc rsa ×3 |
| O-3 | tools/marketing/utm-builder.html | UTM 拼在 fragment 之前 | 页面守卫 |
| O-4 | tools/design/ripple-effect.html | 波纹内联样式 + Web Animations 可见 | 页面预览 |
| O-5 | tools/design/pixel-art-generator.html | 单元格改 .px-cell，点击不再错位 | 页面守卫 |
| O-6 | tools/clinical-nursing/restraint-check.html | 未确认项按实际勾选状态计算 | 页面守卫 |
| O-7 | tools/finance/salary-calculator.html | 切换年薪时缴费基数随新月薪同步 | 页面守卫 |
| O-8 | tools/finance/mortgage-prepayment.html | 基准改用原还款计划月供 | 页面守卫 |
| O-9 | tools/medical/estimate-metabolism.html | kcal 差值改真实百分比 | verify_medical +7.9% |
| O-10 | tools/medical/calculator-calc-due-date.html | 周期校正仅 LMP 生效 | 页面守卫 |
| O-11 | tools/medical/calc-34.html | 删兽医 NRC 表换人用引据；缺口 >500 告警 | 英文探针 0 |
| O-12 | tools/metallurgy/hardness-conversion.html | 按列成对插值，null 不再当 0 | 页面守卫 |
| O-13 | tools/nephrology/ckd-staging.html | G3a/G3b 风险矩阵对齐 KDIGO | 页面守卫 |
| O-14 | tools/beauty/skincare-routine.html | 切肤质触发 renderRoutine | 页面守卫 |
| O-15 | tools/forensic-medicine/death-time-estimation.html | 区间覆盖两法并夹到 0 | verify_forensic ×2 |
| O-16 | tools/life/analysis-cost-10.html | 预算 0 时差异率显示「—」 | 页面守卫 |
| O-17 | tools/life/radiation-converter.html | mSv/uSv 基准改标 Sv | verify_life ×5 期望更新 |
| O-18 | tools/marketing/marketing-roi.html | 删除最终价值/年化回写 | verify_marketing 派生值 |
| O-19 | tools/edu/grade-calculator.html | 目标倒推按总权重归一 | verify_edu 78.00 ×2 |
| O-20 | tools/edu/exam-gpa-calculator.html | 百分制口径统一 ÷25；控件重建 + 空 option 守卫 | 页面守卫 |
| O-21 | tools/edu/exam-score-calculator.html | 历史记录计入每题分值并回填 | 页面守卫 |
| O-22 | tools/edu/word-count-pages.html | 历史页数计入纸张/字号并回填 | 页面守卫 |
| O-23 | tools/edu/essay-word-counter.html | 段落按单换行切分；switchTab 兼容无 event | verify_edu 段落数 3 |

数据源：无（本批未改深解）。
英文键：calc-34 9 条、rsa 1 条、exam-gpa 1 条；探针 3 页 0 残留。
门禁：218/218 通过；部署 87b6ccebc7 success；抽样 6 页关键串全部命中。

## 批次 4 · P 批优先组（14 页）

| 编号 | 文件 | 修复 | 备注 |
|---|---|---|---|
| P-01 | tools/it/bluetooth-version.html | 三个 select 补齐全部版本 option | 默认 5.3/5.0/audio；重置改 .value |
| P-02 | tools/it/usb-version.html | 三个 select 补齐全部版本 option | 默认 3.2/2.0/usbc；重置改 .value |
| P-03 | tools/it/caesar-cipher.html | 关闭「仅字母」时模数改 95 | verify_it 新增 `{|}` 用例 |
| P-04 | tools/edu/certificate-check.html | 深解改写为「目录检索与信息对照」，删除编号/姓名核验承诺 | content_deepdive 源 |
| P-05 | tools/edu/exam-timer.html | 正计时累计小数秒，不再恒 00:00:00 | countUp.frac |
| P-06 | tools/it/adfgvx-cipher.html | 解密列号 `order.indexOf(i)` | 原 `order[i]` 取反 |
| P-07 | tools/it/playfair-cipher.html | 解密按密文两两切分，不插 X/不合并重复；预设 setMode('encrypt') | 原无参 setMode |
| P-08 | tools/edu/24-point-solver.html | 表达式保留原始数字与中间层 | verify_edu 期望更新 |
| P-09 | tools/hr/performance-ranking.html | 归一化得分夹到 100 并提示本人>最高 | verify_hr 85.00 |
| P-10 | tools/ecommerce/analysis-70.html | 深解改为多期经营复盘；退款率 0–100 校验 | content_deepdive 源 |
| P-11 | tools/neurology/nihss.html | 上肢/下肢左右分别计分，满分回到 42 | verify_neurology 注入 q5l/q6r |
| P-12 | tools/dermatology/pasi-score.html | 预设键 h_x/h_l 改 h_d/h_a | 三档预设 |
| P-13 | tools/edu/math-quiz.html | 新增难度/题量/每题限时倒计时 | 题量 10/20/30 |
| P-14 | tools/edu/capital-quiz.html | 新增题量/每题限时倒计时；删除「错题库」宣称 | 题量 10/15/24 |

数据源：content_deepdive.json 改 analysis-70 / certificate-check / capital-quiz 三条（indent=1）。
英文键：analysis-70 15 条、certificate-check 9 条、capital-quiz 16 条、math-quiz 14 条、performance-ranking 2 条、nihss 4 条；探针 6 页 0 残留。
门禁：218/218 通过（逃生项 0 = 基线 0）。

## 批次 5 · commit 3f6dec86c0（16 页，含 Q-1/Q-2 红线）

| 条目 ID | 页面 | 修复类型 | 验证用例 |
|---|---|---|---|
| Q-1 | tools/it/html-entities-encode.html | 解码改纯文本实体替换，用户输入不再进 innerHTML | 无实体原样回显；越界码点回退原文 |
| Q-2 | tools/it/basic-auth-generator.html | 历史仅存令牌长度，密码/Authorization/URL 明文不落盘 | 快照仅 1 键 |
| F-05 | tools/clinical-lab/pcr-ct-interpretation.html | Ct=0/空值不判阴性；对照缺项判质控未完成 | 阈值文案统一 |
| F-06 | tools/finance/isbn-validator.html | 补 input 缺尖括号；非 978/979 判 EAN-13；仅有效源才转换 | 双向转换前置校验 |
| F-07 | tools/finance/lease-payment-calculator.html | 输入校验、末期结清、手续费/首付计入、IRR 不重复计残值 | verify_finance 期初 IRR 10.03% |
| F-08 | tools/finance/credit-card-interest.html | 删除假滞纳金开关；按月单利；负利率校验 | verify_finance 明细表头 |
| F-09 | tools/finance/credit-card-type.html | 新增 Luhn；卡组织前缀扩至 8 家；长度分级提示 | 主/自动用例更新 |
| F-10 | tools/finance/currency-symbol.html | 按代码去重；停用/非 ISO 状态标注 | — |
| F-11 | tools/finance/password-generator-advanced.html | 历史只存掩码；清空按钮；拒绝采样；批量按最弱一条评级 | — |
| F-12 | tools/finance/iban-validator.html | 至 41 国；结论须国家+长度+mod97 三项 | 自动用例改错误串 |
| F-13 | tools/finance/bic-validator.html | 清洗空格/连字符全程用 clean；XXX 标注主办公室 | — |
| E-05 | tools/edu/typing-game.html | 删除预设 tab；结果补总字符/CPM；快照改完成态 | — |
| E-06 | tools/edu2/exam-analysis.html | 成绩解析支持多格式；及格/优秀线校验；满分缩放样本 | 趋势图读 __mean |
| M-05 | tools/hematology/dic-scoring.html | D-二聚体阈值 5→2.5，删 +1 分支 | — |
| M-06 | tools/pulmonology/lung-rads.html | 新增实性成分；边界改 <8/<15；部分实性按实性成分 | — |
| M-07 | tools/cardiology/aortic-dissection.html | radio 补 id；弓部受累归 DeBakey II；深解示例可复现 | — |

数据源：content_deepdive.json 改 aortic-dissection / pcr-ct / typing-game 三条（indent=1）。
英文键：16 页共补 46 条（含 6 处 placeholder），探针 16 页 0 残留。
门禁：218/218 通过（逃生项 0 = 基线 0）；线上 5 URL 抽样命中关键串。

## 批次 6 · R 批医疗安全（15 页）

| 条目 ID | 页面 | 修复类型 |
|---|---|---|
| R-01 | tools/clinical-lab/semen-analysis.html | 空值返回 NaN 并前置校验，清空不再判「无精子症」 |
| R-02 | tools/clinical-lab/thyroid-function-model.html | 补「激素升高/降低需鉴别」分支，FT3/FT4↑+TSH 未降不再报正常 |
| R-03 | tools/cardiology/hypertension-jnc.html | 风险分层重写为 JNC7 表（1 级/2 级 × RF × TOD/ACC） |
| R-04 | tools/cardiology/cardiac-rehab-mets.html | 深解示例能耗 44.1→220.5 kcal（44.1 L O₂ × 5） |
| R-05 | tools/cardiology/echo-report.html | ICD 指征收窄为 LVEF≤35% + NYHA II–III + GDMT≥3 月，LVESV 不再单独构成指征 |
| R-06 | tools/cardiology/nyha-classification.html | 新增 overallAdvice，IV 级即使 6MWT>450m 仍判重度/预后差 |
| R-07 | tools/pediatrics/neonatal-jaundice.html | 阈值表改为与代码同口径（低危足月 10/13/15/17/18），深解示例 12→13 |
| R-08 | tools/endocrinology/pcos-diagnosis.html | 睾酮单位统一为 >60 ng/dL（≈2.1 nmol/L） |
| R-09 | tools/nephrology/edema-grading.html | 分级取凹陷深度与回弹时间较重档；空值/负值守卫 |
| R-10 | tools/dentistry/periodontal-pocket.html | CAL 负值按 0 计并注明假性袋，不再显示负 mm |
| R-11 | tools/pulmonology/tb-resistance.html | PZA/EMB 耐药改个体化方案并追加提示 |
| R-12 | tools/cardiology/calc-3.html | 引据表/公式框统一为 STEMI 14 分加权 |
| R-13 | tools/pulmonology/pulmonary-function.html | FEV1/FVC 与预计值校验，清空不再输出「混合性 GOLD 4」 |
| R-14 | tools/pediatrics/ddst-screening.html | 延迟项判定方向修正；矫正胎龄实际参与年龄线 |
| R-15 | tools/nephrology/aki-kdigo.html | 新增「距基线时间」，补 48h/7d 时间窗 |

数据源：content_deepdive.json 改 calc-3 / cardiac-rehab-mets / neonatal-jaundice；同步 guides/cardiac-rehab-mets-guide。
英文键：15 页补 60+ 条（含 placeholder），探针 15 页 0 残留。
门禁：218/218 通过（逃生项 0）；verify_cardiology hypertension-jnc 期望改低危 180/365 天。

### 待办（下一批）

- **R 批剩余（技术类 10 条）**：xml-to-yaml 深解注入 textarea/`[object Object]`；qrcode 中文 UTF-8 + 解码宣称；regex 灾难回溯超时；rabbit `t>>>32`；md5 HMAC 长密钥；imei 14 位；calc-price-elasticity 弧弹性/收入；analysis-29 离职率口径；calc-4 负百分比仍可行；reminder-1 `undefined天`。
- **Q 批剩余其他（3 条）**：ein-validator 前缀未参与；marketing-*/eap-* 单位错；word-memory「认识」硬编码 0。
- **假工具剩余（plan/fake-tools.md 27 页已修 7）**：xiangqi-endgame、metabolite-prediction、estimate-ranking、calc-81、gomoku-forbidden、parasite-egg-id、urine-sediment-atlas、stats-funnel-recruit、email-subject-line-tester、eap-xinli-zixun-weiji-ziyuan、marketing-utm-builder、word-search（已降级）等约 20 页；能真做的补实现，依赖麦克风/不可实现的降级描述（禁止改名）。

## 批次 7 · commit b23478b727（源）+ f77713454f（构建）+ c8c960a0ec（英文词典）（20 页）

| 条目 | 页面 | 修复 | 验证 |
|---|---|---|---|
| R-16 | tools/it/xml-to-yaml | 深解块移出 textarea（改由构建注入到正文）；数组内对象递归展开，不再 `[object Object]` | 页面复核 |
| R-17 | tools/it/qrcode | 强制 UTF-8 字节编码（原 Latin-1 截断致中文乱码）；删「识别/解析」宣称，改名二维码生成器 | 名称/字典同步 |
| R-18 | tools/it/regex | 主线程执行改 Web Worker + 800ms 超时终止；替换/复制同走保护 | verify_it 850/850 |
| R-19 | tools/it/rabbit | `carry=t>>>32` 改为 `Math.floor(t/2^32)`（原恒 0，偏离 RFC 4503） | 用例改回显断言 |
| R-20 | tools/it/md5 | HMAC 超长密钥取 MD5 原始 16 字节摘要（原传数组 → TypeError） | 代码复核 |
| R-21 | tools/finance/imei-validator | 14 位本体不再补 0 判无效；校验位由前 14 位反推，15 位期望值同步修正 | node 复算 |
| R-22 | tools/marketing/calc-price-elasticity | 深解收入 113300→106700（110×970）；market-price-elasticity 同步 | JSON 源同步 |
| R-23 | tools/hr/analysis-29 | 引据表口径改为「离职/期末在职」，与代码一致并注明平均口径需期初数 | 页面复核 |
| R-24 | tools/edu/calc-4 | 目标公式改 `(目标×100−当前成绩×权重)/剩余权重`；150 分不可能再判可行；新增当前成绩 0–100 校验与「已达成」分支 | verify_edu 105.00 |
| R-25 | tools/edu/reminder-1 | stage=3 不再显示「undefined 天」，改为「不再安排复习」 | 页面复核 |
| Q-20 | tools/finance/ein-validator | 前缀参与判据（IRS 未分配前缀黑名单，00 判无效）；有效性表述收紧 | 页面复核 |
| Q-21 | tools/hr/eap-xinli-zixun-weiji-ziyuan | 咨询师配比 8.0→10.0 名/千人（1:100） | verify_hr 22/22 |
| Q-22 | tools/edu/word-memory | 「认识」计数改为 level===2 实际统计（原硬编码 0） | 页面复核 |
| F-07 | tools/clinical-lab/flow-cytometry-ratio | CD8/CD4 空值不再得 0.00 倒置；各指标空值不判异常；Treg 参与（绝对值 + 占 CD4% 5–10%） | 页面复核 |
| F-08 | tools/finance/housing-fund-loan | 利率改为可填输入（默认 2.85%）；深解月供/利息同步 3102/36.7 万 | verify_finance 2/2 |
| F-09 | tools/finance/salary-after-tax | 工作月数参与（月度×月数到手/个税合计）；税率表补 6/7 级 | 页面复核 |
| F-10 | tools/legal/court-fee | 知识产权有金额按财产案件分段计费（原统一封顶 1000） | 抽取 propertyFee |
| F-11 | tools/legal/child-support | 子女数量参与：每名子女金额 + 总比例 50% 上限 | verify_legal 2/2 |
| 红线 | tools/marketing/marketing-qr-campaign-tracker | 删除 qrserver 第三方请求，改用本地 js/qrcode.js 生成；链接转义输出 | verify_marketing 120/120 |
| 红线 | tools/it/markdown-editor | 图片/链接 URL 白名单 + 属性转义，阻断 `" onerror=` 注入 | 代码复核 |

门禁：218/218 通过（逃生项 0 = 基线 0）；deploy f77713454f。

### 待办
- 假工具（61 页清单）剩余约 39 页：xiangqi-endgame、metabolite-prediction、estimate-ranking、calc-81、gomoku-forbidden、parasite-egg-id、urine-sediment-atlas、stats-funnel-recruit、email-subject-line-tester、marketing-utm-builder、word-search 等。
- S 批：it/phone-qr 伪二维码、des 密钥编排、csv-to-html-table、js/python formatter、finance tfn/curp/tin/gstin 校验器。
