# 假实现与纯展示工具清单（2026-11-14 全量复核后 · 当前状态）

## 一、结论

- 2026-11-04 的三份快照（本文件旧版、`part-02.md`、`part-03.md`）累计约 **170 行**记录，
  已于 **2026-11-14** 逐页对照当前源码复核完毕。
- 复核结果：**全部不再成立** —— 要么功能已补齐（真实编码/真实查表/真实计时/真实导出），
  要么页面文案已降级到与实际能力一致（明确写出「不做什么」）。**当前待修页 0**。
- 本文件改为「当前状态 + 已销账证据」；`part-02.md`、`part-03.md` 保留原表仅作历史快照，
  顶部已加销账说明，不再作为待修清单使用。

## 二、复核口径

- 只读核验当前工作树源码（grep + 关键函数阅读），不依赖快照里的行号与结论。
- 「已修复」= 控件值真正参与计算 / 输出与输入联动 / 真实编码与查表存在。
- 「文案已对齐」= 功能没变，但 meta、简介、FAQ、深览已如实说明边界，不再承诺未实现能力。
- 本清单不覆盖运行时行为（事件绑定、CSS 隐藏态），仅覆盖静态可复现证据。

## 三、已销账页（按分类）

### 医疗健康
| 页面 | 复核结论 | 关键证据 |
|---|---|---|
| `tools/pulmonology/tb-resistance.html` | 已修复 | PZA/EMB 耐药已进入 DS-TB 分支，勾选后不再套用 2HRZE/4HR |
| `tools/cardiology/calc-3.html` | 已修复 | 公式框、引据表、实现统一为 STEMI 14 分制 Morrow 2000，无 NSTEMI 口径残留 |
| `tools/pediatrics/ddst-screening.html` | 已修复 | `correctGA` 经 `getEvalAge()` 真正参与年龄线判定 |
| `tools/clinical-lab/flow-cytometry-ratio.html` | 已修复 | Treg 参与 Treg/CD4 比例与告警；NK 绝对值 <95/μL 有低值 flag |
| `tools/clinical-lab/semen-analysis.html` | 已修复 | IM 进入必填校验与总活力求和，异常提示按总活力判定 |
| `tools/clinical-nursing/bag-valve-mask.html` | 文案已对齐 | 成人高级气道后 10 次/分、儿童/婴儿 CPR 20–30 次/分，页面口径已统一，无 8~10 冲突 |
| `tools/clinical-lab/parasite-egg-id.html` | 文案已对齐 | 明示「文字版要点速查，不含镜检图片」 |
| `tools/clinical-lab/urine-sediment-atlas.html` | 文案已对齐 | 同上，明示无真实镜检图片 |
| `tools/pulmonology/pulmonary-function.html` | 已修复 | 新增「自定义阈值 / LLN」输入，0.50–0.90 可填 |
| `tools/nephrology/aki-kdigo.html` | 已修复 | 已按 48h/7d 时间窗与 RRT 判定分期 |
| `tools/clinical-nursing/suction-pressure.html` | 已否定 | 成人区间为 80–120 |
| `tools/pulmonology/lung-rads.html` | 已否定 | 实性成分输入参与 4A/4B 判定 |
| `tools/clinical-nursing/ostomy-bag-timing.html` | 已否定 | 70% 预警已实现 |
| `tools/healthcare/map.html` | 已否定 | 四重输入守卫齐全 |
| `tools/healthcare/healthcare.html` | 已否定 | 简介已改为体重折算 + 上限倍数 |
| `tools/nephrology/edema-grading.html` | 已否定 | 深度与恢复时间取较重者 |
| `tools/cardiology/coronary-calcium.html` | 已否定 | Agatston 分段与 MESA 百分位均已实现 |
| `tools/gastroenterology/ercp-success.html` | 已修复 | 操作目的/结石/解剖因素真实参与难度分与成功率区间，并注明本页估算 |
| `tools/rehabilitation/fim-scale.html` | 文案已对齐 | opt-guide 已改为 18 项下拉真实流程 |

### 商业运营 / 金融
| 页面 | 复核结论 | 关键证据 |
|---|---|---|
| `tools/hr/calc-81.html` | 已修复 | 分岗位人数/推荐/录用/外部成本均参与，输出转化率、单位录用成本与 ROI |
| `tools/ecommerce/estimate-ranking.html` | 已修复 | 按 CTR/CVR/销量/评分/评价数五因子加权 |
| `tools/ecommerce/report.html` | 已修复 | 支持粘贴与拖入文件，输出环比、升降项数与均值 |
| `tools/hr/stats-funnel-recruit.html` | 已修复 | 逐渠道花费、CPO、单入职成本与最优渠道 |
| `tools/hr/attendance-stats.html` | 已修复 | 加班费、全勤奖、逐员工评级均实现 |
| `tools/hr/bandwidth-1.html` | 已修复 | 重写为中位值/带宽/Compa-ratio/区间位置模型 |
| `tools/hr/hris-zizhuyuaiduibijisuanqi.html` | 文案已对齐 | 简介如实写明「两个成熟度分对比」，不再承诺成本/效率明细 |
| `tools/legal/child-support.html` | 已修复 | `childCount` 参与每名子女分摊与总额 |
| `tools/legal/court-fee.html` | 已修复 | 知识产权有金额时按财产案件分段累进 |
| `tools/finance/salary-after-tax.html` | 已修复 | `months` 参与累计预扣；展示 7 档含 35%/45% |
| `tools/marketing/marketing-ltv-calculator.html` | 已修复 | 回本周期已渲染 |
| `tools/marketing/email-subject-line-tester.html` | 文案已对齐 | 明示启发式打分、不是打开率/送达率预测 |
| `tools/hr/eap-xinli-zixun-weiji-ziyuan.html` | 文案已对齐 | 明示只按两个输入分档，不生成资源清单/热线 |
| `tools/biz/stats-time-response.html` | 已修复 | 已含 P90 与 FCR |
| `tools/biz/text-to-banner.html` | 文案已对齐 | 改为 ASCII/Unicode 字符横幅，明示不出图片 |
| `tools/biz/text-extract-html-tags.html` | 已修复 | 开关与 uniqueCount 已接入实际过滤 |
| `tools/ecommerce/analysis-cost-8.html` | 已修复 | 增加优化后方案对比、成本率与保本销量 |
| `tools/finance/housing-fund-loan.html` | 已否定 | 利率可输入 |

### 教育 / 语言 / 文博
| 页面 | 复核结论 | 关键证据 |
|---|---|---|
| `tools/edu/word-memory.html` | 已修复 | `lastReview` 驱动 1/3/7/15/30 天到期队列与「复习到期」 |
| `tools/edu/chinese-zodiac.html` | 已修复 | 生日 + 1980–2040 春节表，春节前按上一年 |
| `tools/edu/study-planner.html` | 已修复 | 重复公式框已去重；完成率/优先级排序已实现 |
| `tools/research/analysis-49.html` | 已修复 | 已含 KMO/Bartlett 与矩阵运算 |
| `tools/cognition/human-benchmark.html` | 已修复 | 粘贴被拦截，粘贴内容不计分 |
| `tools/museum/index.html` | 已修复 | 8 张卡片均为页面专属描述 |
| `tools/museum/visitor-route.html` | 已修复 | 必看节点按序串联，不可达时报错 |
| `tools/language/grammar-checker.html` | 文案已对齐 | 明确「纯规则匹配」并已输出问题密度 |
| `tools/language/translator.html` | 已否定 | 文案只称本地词表并显示实际条数 |
| `tools/it/http-cookies.html` | 文案已对齐 | 明示「不解析、不构造」 |
| `tools/it/whitespace.html` | 已修复 | 「压成一行」存在，预览错位已修 |
| `tools/it/timestamp-converter.html` | 已修复 | 按目标日期取偏移，处理夏令时 |
| `tools/it/markdown-to-html.html` | 已否定 | 图片语法已实现 |
| `tools/it/phone-parser.html` | 文案已对齐 | 改为国家码/trunk prefix 解析，明示不做归属地/运营商 |
| `tools/it/charset-detector.html` | 文案已对齐 | 明示「本地静态识别常见乱码特征」 |
| `tools/it/text-qr.html` | 已修复 | 使用真实版本/纠错/掩码矩阵 |
| `tools/it/url-qr.html`、`email-qr.html`、`location-qr.html` | 已修复 | 走本地 ISO/IEC 18004 编码器（含 Reed-Solomon） |
| `tools/it/morse-decode-advanced.html` | 文案已对齐 | 明确不做时序推断/噪声容错 |

### 设计 / IT / 生活 / 其他
| 页面 | 复核结论 | 关键证据 |
|---|---|---|
| `tools/design/pixel-art-generator.html` | 已修复 | 导出字符画 .txt 与 CSS box-shadow |
| `tools/design/gradient.html` | 已修复 | 相邻色标 WCAG 对比度已计算并注明不适用文字等级 |
| `tools/design/mesh-gradient.html` | 已修复 | 拖拽控制点、PNG 导出、WCAG 校验均已实现 |
| `tools/design/color-palette.html` | 已修复 | WCAG 对比度与红标已实现 |
| `tools/electronics/capacitor-calculator.html` | 已修复 | τ = R×C/1e6，随 R/C 输入变化 |
| `tools/acupuncture/acupoint-location.html` | 已修复 | `revCun` 参与反算并输出寸数 |
| `tools/quantum/pair-production-threshold.html` | 已修复 | 按粒子静止质量计算 2mₑc² 等阈值 |
| `tools/life/stats-13.html` | 文案已对齐 | 简介/公式与「人数/份数/占比/分档」一致 |
| `tools/life/analysis-cost-9.html` | 已修复 | 固定/变动拆分、单位成本、盈亏平衡、降本排序 |
| `tools/life/assessor-target.html` | 已修复 | 面积参与六维加权 |
| `tools/finance/word-wrap.html` | 已修复 | CSV 导出含换行结果 |
| `tools/chess/xiangqi-endgame.html` | 文案已对齐 | 改为「杀法速查」，明示无棋盘输入/着法推演 |
| `tools/chess/gomoku-forbidden.html` | 已修复 | 15×15 可落子/粘贴棋盘 + 坐标判禁手 |
| `tools/audio/audio-recorder.html` | 已修复 | 按当前音量/速度离线渲染 16-bit WAV |
| `tools/office/pdf-split.html` | 文案已对齐 | 改为按页码范围/可视化勾选提取，与实际一致 |
| `tools/sports/rehab-motion.html` | 文案已对齐 | 明示只做负荷算术，不推荐动作 |
| `tools/sports/training-planner.html` | 已修复 | 按每周 3–6 天取前 N 天模板 |
| `tools/sports/simulator-18.html` | 文案已对齐 | 改为伯努利试验模拟，深览同步改写 |
| `tools/sports/analysis-19.html` | 文案已对齐 | 中英文简介均改为「录入回合记录统计」，删除「视频片段」承诺 |
| `tools/sports/pingpangqiu-xiangchi-faqiu-defen.html` | 已修复 | 相持/发球/关键分得分率真实计算 |
| `tools/sports/baofali-zongtiao-lidingtiaoyuan.html` | 已修复 | 速度/体重/蹬伸时间参与高度与功率 |
| `tools/fun/sequence-puzzle.html` | 已修复 | 9 类数字规律含质数/阶乘/交替 |
| `tools/fun/generator-laugh.html` | 已修复 | 已含 AudioContext/OscillatorNode |
| `tools/nutrition/generator-nutrition-label.html` | 已修复 | 能量按 Atwater 由蛋白/脂肪/碳水核算 |
| `tools/leather/xueyunhoudukongzhi.html` | 已修复 | 来料/目标厚度参与切除量 |
| `tools/gardening/balcony-sunlight.html` | 已修复 | 朝向/楼层/季节下拉均有选项并参与查表 |
| `tools/agriculture/assessor-1.html` | 已修复 | 落粒/脱粒分项进入总损失率与分母 |
| `tools/agriculture/calc-6.html` | 已修复 | 饲养周期参与 365÷周期批次上限 |
| `tools/fishery/calc-39.html` | 已修复 | 群体重量 × 水温分段投喂率 |
| `tools/fishery/calc-power.html` | 已修复 | V×ΔT÷η 与时长计算加热功率 |
| `tools/fishery/density-1.html` | 文案已对齐 | 明示只做单位换算 |
| `tools/fishery/estimate-23.html` | 文案已对齐 | 明示只做单期线性百分比估算 |
| `tools/fishery/ratio-hormone.html` | 已修复 | 按体重 × 方案剂量率计算总剂量与两针分配 |
| `tools/fishery/temp-density.html` | 已修复 | 更名为「水温饱和溶氧与饱和度计算器」，简介/功能/场景与溶氧饱和度换算一致 |
| `tools/machinery/detector-159.html`、`detector-stretch.html`、`detector-134.html` 等 | 文案已对齐 | 删除 GB/T 引用与「可用于质量验收」，改为用户填写设计限值 |
| `tools/metalwork/analysis-36.html` | 文案已对齐 | 删除均值/标准差/控制界限/成因诊断承诺，改为分类统计与加权指数 |
| `tools/metalwork/pressure-casting.html`、`resistance-2.html` | 文案已对齐 | meta 明示「仅做方法选型，不计算浇注/冷却或电流/电压参数」 |
| `tools/metalwork/calc-gear-2.html` | 已修复 | 增加螺旋角 β 输入与斜齿几何修正 |
| `tools/tcm-chemistry/metabolite-prediction.html` | 已修复 | `compound` 下拉参与预测 |
| `tools/pediatrics/ddst-screening.html` | 已修复 | 见上 |

## 四、维护约定

- 新增怀疑项先 grep 当前源码，确认「控件值是否进入计算」「导出是否真的导出对应内容」「文案是否承诺了未实现能力」。
- 修复后整条删除对应行，并在 `plan/已修复/` 留一份复核记录（批号继续递增）。
- 本清单不再保留「已否定」历史行；历史快照见 `part-02.md` / `part-03.md`。
