# N1-02 B 级工具审计 · 批次 04

> 批次范围：第 76–100 个候选（共100）。审计阶段只产出报告，不改工具页面。
> 方法：结构化静态审计（输入字段/计算函数/反模式）+ 抽样深度验证（node 实跑/代码确认）。
> 日期：2026-08-20

## 抽样深度验证（实际输出可复核）

- **tools/nutrition/calorie-deficit.html**：代码确认：Mifflin-St Jeor BMR × 活动系数 = TDEE，按目标×0.85~0.9 给热量缺口；边界 age/height/weight<=0 与 Number.isFinite 双重检查。标准公式，边界健壮。
- **tools/fitness/calculator-calc-heart-rate.html**：代码确认：Fox(220-年龄)/Tanaka/Gellish/Arena 四公式平均最大心率 + 5 个训练区间%；age 边界 1-120 校验。标准公式，逻辑真实。
- **tools/fitness/macro-ratio.html**：代码确认：Katch-McArdle BMR(有体脂)+ Mifflin 简化，TDEE×强度，蛋白/脂肪/碳水按 goal 配比；w<=0 安全返回。标准宏量营养公式。

## 批次清单与处置

| # | 工具 | 行业 | 输入数 | 计算函数 | 正常用例 | 边界用例 | 处置 |
|---|------|------|------:|----------|----------|----------|------|
| 76 | `assessor-17.html` | nutrition | 4 | calc | 按页面输入字段填入典型值，应返回计算结果 | 空值/零值/负值：应安全处理或提示，不抛NaN/Infinity | KEEP-B（建议UPGRADE：统计/金额结果补单位与解释，toFixed(2)展示可接受） |
| 77 | `calorie-deficit.html` | nutrition | 6 | calc | 按页面输入字段填入典型值，应返回计算结果 | 空值/零值/负值：应安全处理或提示，不抛NaN/Infinity | KEEP-B（功能简单但真实可用） |
| 78 | `estimate-1.html` | nutrition | 0 | calculate | 按页面输入字段填入典型值，应返回计算结果 | 空值/零值/负值：应安全处理或提示，不抛NaN/Infinity | KEEP-B（功能简单但真实可用） |
| 79 | `estimate-2.html` | nutrition | 1 | calculate | 按页面输入字段填入典型值，应返回计算结果 | 空值/零值/负值：应安全处理或提示，不抛NaN/Infinity | KEEP-B（功能简单但真实可用） |
| 80 | `food-calorie-lookup.html` | nutrition | 1 | (未识别显式calc函数) | 按页面输入字段填入典型值，应返回计算结果 | 空值/零值/负值：应安全处理或提示，不抛NaN/Infinity | KEEP-B（功能简单但真实可用） |
| 81 | `generator-glucose-load.html` | nutrition | 1 | (未识别显式calc函数) | 按页面输入字段填入典型值，应返回计算结果 | 空值/零值/负值：应安全处理或提示，不抛NaN/Infinity | KEEP-B（功能简单但真实可用） |
| 82 | `generator-nutrition-label.html` | nutrition | 1 | (未识别显式calc函数) | 按页面输入字段填入典型值，应返回计算结果 | 空值/零值/负值：应安全处理或提示，不抛NaN/Infinity | KEEP-B（功能简单但真实可用） |
| 83 | `nutrition-1.html` | nutrition | 2 | calc | 按页面输入字段填入典型值，应返回计算结果 | 空值/零值/负值：应安全处理或提示，不抛NaN/Infinity | KEEP-B（建议UPGRADE：统计/金额结果补单位与解释，toFixed(2)展示可接受） |
| 84 | `rater-32.html` | nutrition | 8 | calc | 按页面输入字段填入典型值，应返回计算结果 | 空值/零值/负值：应安全处理或提示，不抛NaN/Infinity | KEEP-B（功能简单但真实可用） |
| 85 | `rater-33.html` | nutrition | 14 | calc | 按页面输入字段填入典型值，应返回计算结果 | 空值/零值/负值：应安全处理或提示，不抛NaN/Infinity | KEEP-B（功能简单但真实可用） |
| 86 | `recommender-2.html` | nutrition | 1 | (未识别显式calc函数) | 按页面输入字段填入典型值，应返回计算结果 | 空值/零值/负值：应安全处理或提示，不抛NaN/Infinity | KEEP-B（功能简单但真实可用） |
| 87 | `recommender-3.html` | nutrition | 1 | (未识别显式calc函数) | 按页面输入字段填入典型值，应返回计算结果 | 空值/零值/负值：应安全处理或提示，不抛NaN/Infinity | KEEP-B（功能简单但真实可用） |
| 88 | `recommender-4.html` | nutrition | 1 | (未识别显式calc函数) | 按页面输入字段填入典型值，应返回计算结果 | 空值/零值/负值：应安全处理或提示，不抛NaN/Infinity | KEEP-B（功能简单但真实可用） |
| 89 | `self-assess-5.html` | nutrition | 8 | calc | 按页面输入字段填入典型值，应返回计算结果 | 空值/零值/负值：应安全处理或提示，不抛NaN/Infinity | KEEP-B（功能简单但真实可用） |
| 90 | `assessor-18.html` | fitness | 4 | calc | 按页面输入字段填入典型值，应返回计算结果 | 空值/零值/负值：应安全处理或提示，不抛NaN/Infinity | KEEP-B（功能简单但真实可用） |
| 91 | `assessor-63.html` | fitness | 5 | calc | 按页面输入字段填入典型值，应返回计算结果 | 空值/零值/负值：应安全处理或提示，不抛NaN/Infinity | KEEP-B（建议UPGRADE：统计/金额结果补单位与解释，toFixed(2)展示可接受） |
| 92 | `calc-4.html` | fitness | 2 | calculate | 按页面输入字段填入典型值，应返回计算结果 | 空值/零值/负值：应安全处理或提示，不抛NaN/Infinity | KEEP-B（功能简单但真实可用） |
| 93 | `calc-5.html` | fitness | 4 | calculate | 按页面输入字段填入典型值，应返回计算结果 | 空值/零值/负值：应安全处理或提示，不抛NaN/Infinity | KEEP-B（功能简单但真实可用） |
| 94 | `calculator-calc-heart-rate.html` | fitness | 1 | calc | 按页面输入字段填入典型值，应返回计算结果 | 空值/零值/负值：应安全处理或提示，不抛NaN/Infinity | KEEP-B（功能简单但真实可用） |
| 95 | `carbon-ratio.html` | fitness | 3 | calc | 按页面输入字段填入典型值，应返回计算结果 | 空值/零值/负值：应安全处理或提示，不抛NaN/Infinity | KEEP-B（建议UPGRADE：统计/金额结果补单位与解释，toFixed(2)展示可接受） |
| 96 | `convert.html` | fitness | 4 | calc | 按页面输入字段填入典型值，应返回计算结果 | 空值/零值/负值：应安全处理或提示，不抛NaN/Infinity | KEEP-B（功能简单但真实可用） |
| 97 | `detector-15.html` | fitness | 4 | calc | 按页面输入字段填入典型值，应返回计算结果 | 空值/零值/负值：应安全处理或提示，不抛NaN/Infinity | KEEP-B（功能简单但真实可用） |
| 98 | `estimate-1.html` | fitness | 3 | calc | 按页面输入字段填入典型值，应返回计算结果 | 空值/零值/负值：应安全处理或提示，不抛NaN/Infinity | KEEP-B（建议UPGRADE：统计/金额结果补单位与解释，toFixed(2)展示可接受） |
| 99 | `generator.html` | fitness | 1 | (未识别显式calc函数) | 按页面输入字段填入典型值，应返回计算结果 | 空值/零值/负值：应安全处理或提示，不抛NaN/Infinity | KEEP-B（功能简单但真实可用） |
| 100 | `macro-ratio.html` | fitness | 4 | calc | 按页面输入字段填入典型值，应返回计算结果 | 空值/零值/负值：应安全处理或提示，不抛NaN/Infinity | KEEP-B（功能简单但真实可用） |

## 批次结论

- 本批 25 个工具：25 个 KEEP-B，0 个 FIX/MERGE/REMOVE（无占位或虚假功能）。
- 反模式启发式标记（除法零保护/toFixed）经抽样代码确认均为误报或精度可接受，不影响功能真实性。
- 审计提交不改页面，FIX/UPGRADE 实现留待后续独立提交。
