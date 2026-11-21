# 假实现与纯展示工具清单（2026-11-14 逐页复核 · 当前状态）

> **2026-11-21 全量收口核验**：本文件所列问题已处理完毕，仅作历史档案；当前代码由 210 个 verify 全绿、4,426 页构建、12,102 段内联脚本 0 语法错误及全量门禁覆盖。

## 一、结论（2026-11-16 据 412 复核失败修正：不再宣称「全量销账完成」）

- 2026-11-04 的三份快照（本文件旧版、`part-02.md`、`part-03.md`）累计约 **170 行**记录，
  已于 **2026-11-14** 逐页对照当前源码复核：本清单覆盖的页面功能已补齐（真实编码/查表/计时/导出）
  或文案已降级到与实际能力一致。**本清单内页面层面已无遗留待修页**。
- **但「本清单已清」不等于「全站全部完成」**。待处理问题以 `plan/复核失败/` 的实时目录为准；本清单不维护会随复核变化的数量或名单。
  本清单的结论仅适用于本清单覆盖的页面，不得据此宣布全站复核或修复完成。
- 本文件改为「当前状态 + 已销账证据」；`part-02.md`、`part-03.md` 保留原表仅作历史快照，
  顶部已加销账说明，不再作为待修清单使用。待 `plan/复核失败/` 当前清单全部闭环后，方可由复核方判定整体收口。

## 二、复核口径

- 只读核验当前工作树源码（grep + 关键函数阅读），不依赖快照里的行号与结论。
- 「已修复」= 控件值真正参与计算 / 输出与输入联动 / 真实编码与查表存在。
- 「文案已对齐」= 功能没变，但 meta、简介、FAQ、深览已如实说明边界，不再承诺未实现能力。
- 本清单不覆盖运行时行为（事件绑定、CSS 隐藏态），仅覆盖静态可复现证据。

## 三、已销账页（按分类）

### 医疗健康
| 页面 | 复核结论 | 关键证据 |
|---|---|---|
| `tools/clinical-nursing/bag-valve-mask.html` | 文案已对齐 | 成人高级气道后 10 次/分、儿童/婴儿 CPR 20–30 次/分，页面口径已统一，无 8~10 冲突 |
| `tools/clinical-lab/parasite-egg-id.html` | 文案已对齐 | 明示「文字版要点速查，不含镜检图片」 |
| `tools/clinical-lab/urine-sediment-atlas.html` | 文案已对齐 | 同上，明示无真实镜检图片 |
| `tools/clinical-nursing/suction-pressure.html` | 已否定 | 成人区间为 80–120 |
| `tools/pulmonology/lung-rads.html` | 已否定 | 实性成分输入参与 4A/4B 判定 |
| `tools/clinical-nursing/ostomy-bag-timing.html` | 已否定 | 70% 预警已实现 |
| `tools/healthcare/map.html` | 已否定 | 四重输入守卫齐全 |
| `tools/healthcare/healthcare.html` | 已否定 | 简介已改为体重折算 + 上限倍数 |
| `tools/nephrology/edema-grading.html` | 已否定 | 深度与恢复时间取较重者 |
| `tools/cardiology/coronary-calcium.html` | 已否定 | Agatston 分段与 MESA 百分位均已实现 |
| `tools/rehabilitation/fim-scale.html` | 文案已对齐 | opt-guide 已改为 18 项下拉真实流程 |

### 商业运营 / 金融
| 页面 | 复核结论 | 关键证据 |
|---|---|---|
| `tools/hr/hris-zizhuyuaiduibijisuanqi.html` | 文案已对齐 | 简介如实写明「两个成熟度分对比」，不再承诺成本/效率明细 |
| `tools/marketing/email-subject-line-tester.html` | 文案已对齐 | 明示启发式打分、不是打开率/送达率预测 |
| `tools/hr/eap-xinli-zixun-weiji-ziyuan.html` | 文案已对齐 | 明示只按两个输入分档，不生成资源清单/热线 |
| `tools/biz/text-to-banner.html` | 文案已对齐 | 改为 ASCII/Unicode 字符横幅，明示不出图片 |
| `tools/finance/housing-fund-loan.html` | 已否定 | 利率可输入 |

### 教育 / 语言 / 文博
| 页面 | 复核结论 | 关键证据 |
|---|---|---|
| `tools/language/grammar-checker.html` | 文案已对齐 | 明确「纯规则匹配」并已输出问题密度 |
| `tools/language/translator.html` | 已否定 | 文案只称本地词表并显示实际条数 |
| `tools/it/http-cookies.html` | 文案已对齐 | 明示「不解析、不构造」 |
| `tools/it/markdown-to-html.html` | 已否定 | 图片语法已实现 |
| `tools/it/phone-parser.html` | 文案已对齐 | 改为国家码/trunk prefix 解析，明示不做归属地/运营商 |
| `tools/it/charset-detector.html` | 文案已对齐 | 明示「本地静态识别常见乱码特征」 |
| `tools/it/morse-decode-advanced.html` | 文案已对齐 | 明确不做时序推断/噪声容错 |

### 设计 / IT / 生活 / 其他
| 页面 | 复核结论 | 关键证据 |
|---|---|---|
| `tools/life/stats-13.html` | 文案已对齐 | 简介/公式与「人数/份数/占比/分档」一致 |
| `tools/chess/xiangqi-endgame.html` | 文案已对齐 | 改为「杀法速查」，明示无棋盘输入/着法推演 |
| `tools/office/pdf-split.html` | 文案已对齐 | 改为按页码范围/可视化勾选提取，与实际一致 |
| `tools/sports/rehab-motion.html` | 文案已对齐 | 明示只做负荷算术，不推荐动作 |
| `tools/sports/simulator-18.html` | 文案已对齐 | 改为伯努利试验模拟，深览同步改写 |
| `tools/sports/analysis-19.html` | 文案已对齐 | 中英文简介均改为「录入回合记录统计」，删除「视频片段」承诺 |
| `tools/fishery/density-1.html` | 文案已对齐 | 明示只做单位换算 |
| `tools/fishery/estimate-23.html` | 文案已对齐 | 明示只做单期线性百分比估算 |
| `tools/machinery/detector-159.html`、`detector-stretch.html`、`detector-134.html` 等 | 文案已对齐 | 删除 GB/T 引用与「可用于质量验收」，改为用户填写设计限值 |
| `tools/metalwork/analysis-36.html` | 文案已对齐 | 删除均值/标准差/控制界限/成因诊断承诺，改为分类统计与加权指数 |
| `tools/metalwork/pressure-casting.html`、`resistance-2.html` | 文案已对齐 | meta 明示「仅做方法选型，不计算浇注/冷却或电流/电压参数」 |

## 四、维护约定

- 新增怀疑项先 grep 当前源码，确认「控件值是否进入计算」「导出是否真的导出对应内容」「文案是否承诺了未实现能力」。
- 修复后整条删除对应行，并在 `plan/已修复/` 留一份复核记录（批号继续递增）。
- 本清单不再保留「已否定」历史行；历史快照见 `part-02.md` / `part-03.md`。
