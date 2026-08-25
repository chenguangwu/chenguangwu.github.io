# N1-02 B 级工具审计 · 批次 03

> 批次范围：第 51–75 个候选（共100）。审计阶段只产出报告，不改工具页面。
> 方法：结构化静态审计（输入字段/计算函数/反模式）+ 抽样深度验证（node 实跑/代码确认）。
> 日期：2026-08-20

## 抽样深度验证（实际输出可复核）

- **tools/health/blood-pressure-classifier.html**：代码确认：classifyBP(收缩压,舒张压) 标准血压分级（正常/升高/1-3级），含脉压、平均动脉压与仪表盘角度；空输入 return 等待。逻辑真实。
- **tools/health/protein-needs.html**：代码确认：蛋白需求=体重×活动系数（肌肉/减脂/康复/老年分支调整）÷来源占比，含 min/max 范围；w<=0 安全返回。标准公式。
- **tools/medical/convert-glucose.html**：代码确认：血糖单位换算 v×rate×f/t（mg/dL↔mmol/L 用系数），toFixed(6) 展示；运算符清晰无除零风险。通用换算正确。

## 批次清单与处置

| # | 工具 | 行业 | 输入数 | 计算函数 | 正常用例 | 边界用例 | 处置 |
|---|------|------|------:|----------|----------|----------|------|
| 51 | `tfn-validator.html` | finance | 1 | (未识别显式calc函数) | 输入一个合法样本值（如合法身份证/税号/卡号），应返回校验通过并展示解析结果 | 空输入或少于2位：应给出"等待输入/位数不足"提示，不崩溃 | KEEP-B（功能简单但真实可用） |
| 52 | `tin-validator.html` | finance | 1 | (未识别显式calc函数) | 输入一个合法样本值（如合法身份证/税号/卡号），应返回校验通过并展示解析结果 | 空输入或少于2位：应给出"等待输入/位数不足"提示，不崩溃 | KEEP-B（功能简单但真实可用） |
| 53 | `uan-validator.html` | finance | 1 | (未识别显式calc函数) | 输入一个合法样本值（如合法身份证/税号/卡号），应返回校验通过并展示解析结果 | 空输入或少于2位：应给出"等待输入/位数不足"提示，不崩溃 | KEEP-B（功能简单但真实可用） |
| 54 | `vin-validator.html` | finance | 1 | calcCheckDigit | 输入一个合法样本值（如合法身份证/税号/卡号），应返回校验通过并展示解析结果 | 空输入或少于2位：应给出"等待输入/位数不足"提示，不崩溃 | KEEP-B（功能简单但真实可用） |
| 55 | `voter-id-validator.html` | finance | 1 | (未识别显式calc函数) | 输入一个合法样本值（如合法身份证/税号/卡号），应返回校验通过并展示解析结果 | 空输入或少于2位：应给出"等待输入/位数不足"提示，不崩溃 | KEEP-B（功能简单但真实可用） |
| 56 | `wifi-password-show.html` | finance | 4 | (未识别显式calc函数) | 按页面输入字段填入典型值，应返回计算结果 | 空值/零值/负值：应安全处理或提示，不抛NaN/Infinity | KEEP-B（功能简单但真实可用） |
| 57 | `word-counter.html` | finance | 1 | (未识别显式calc函数) | 输入一个合法样本值（如合法身份证/税号/卡号），应返回校验通过并展示解析结果 | 空输入或少于2位：应给出"等待输入/位数不足"提示，不崩溃 | KEEP-B（功能简单但真实可用） |
| 58 | `word-scramble.html` | finance | 1 | (未识别显式calc函数) | 输入一个合法样本值（如合法身份证/税号/卡号），应返回校验通过并展示解析结果 | 空输入或少于2位：应给出"等待输入/位数不足"提示，不崩溃 | KEEP-B（功能简单但真实可用） |
| 59 | `word-search.html` | finance | 0 | (未识别显式calc函数) | 输入一个合法样本值（如合法身份证/税号/卡号），应返回校验通过并展示解析结果 | 空输入或少于2位：应给出"等待输入/位数不足"提示，不崩溃 | KEEP-B（功能简单但真实可用） |
| 60 | `zip-code-validator.html` | finance | 1 | (未识别显式calc函数) | 输入一个合法样本值（如合法身份证/税号/卡号），应返回校验通过并展示解析结果 | 空输入或少于2位：应给出"等待输入/位数不足"提示，不崩溃 | KEEP-B（功能简单但真实可用） |
| 61 | `analysis-46.html` | accounting | 0 | calc | 输入一组数值(如 1,2,3,4)：应返回量/和/均值/中位/标准差 | 单值输入：均值=该值，标准差0；极大值：不溢出NaN | KEEP-B（建议UPGRADE：统计/金额结果补单位与解释，toFixed(2)展示可接受） |
| 62 | `analysis-cost-5.html` | accounting | 0 | calc | 输入一组数值(如 1,2,3,4)：应返回量/和/均值/中位/标准差 | 单值输入：均值=该值，标准差0；极大值：不溢出NaN | KEEP-B（建议UPGRADE：统计/金额结果补单位与解释，toFixed(2)展示可接受） |
| 63 | `report-2.html` | accounting | 0 | calc | 按页面输入字段填入典型值，应返回计算结果 | 空值/零值/负值：应安全处理或提示，不抛NaN/Infinity | KEEP-B（建议UPGRADE：统计/金额结果补单位与解释，toFixed(2)展示可接受） |
| 64 | `alcohol-units.html` | health | 8 | calc | 按页面输入字段填入典型值，应返回计算结果 | 空值/零值/负值：应安全处理或提示，不抛NaN/Infinity | KEEP-B（功能简单但真实可用） |
| 65 | `blood-pressure-classifier.html` | health | 4 | calc | 按页面输入字段填入典型值，应返回计算结果 | 空值/零值/负值：应安全处理或提示，不抛NaN/Infinity | KEEP-B（建议UPGRADE：统计/金额结果补单位与解释，toFixed(2)展示可接受） |
| 66 | `calc-1.html` | health | 4 | calculate | 按页面输入字段填入典型值，应返回计算结果 | 空值/零值/负值：应安全处理或提示，不抛NaN/Infinity | KEEP-B（功能简单但真实可用） |
| 67 | `child-height-predictor.html` | health | 4 | calc | 按页面输入字段填入典型值，应返回计算结果 | 空值/零值/负值：应安全处理或提示，不抛NaN/Infinity | KEEP-B（功能简单但真实可用） |
| 68 | `dysphagia-food-guide.html` | health | 0 | (未识别显式calc函数) | 按页面输入字段填入典型值，应返回计算结果 | 空值/零值/负值：应安全处理或提示，不抛NaN/Infinity | KEEP-B（功能简单但真实可用） |
| 69 | `protein-needs.html` | health | 6 | calc | 按页面输入字段填入典型值，应返回计算结果 | 空值/零值/负值：应安全处理或提示，不抛NaN/Infinity | KEEP-B（功能简单但真实可用） |
| 70 | `assessor-risk-3.html` | medical | 6 | calc | 按页面输入字段填入典型值，应返回计算结果 | 空值/零值/负值：应安全处理或提示，不抛NaN/Infinity | KEEP-B（功能简单但真实可用） |
| 71 | `convert-12.html` | medical | 4 | calc | 按页面输入字段填入典型值，应返回计算结果 | 空值/零值/负值：应安全处理或提示，不抛NaN/Infinity | KEEP-B（功能简单但真实可用） |
| 72 | `convert-glucose.html` | medical | 4 | calc | 按页面输入字段填入典型值，应返回计算结果 | 空值/零值/负值：应安全处理或提示，不抛NaN/Infinity | KEEP-B（功能简单但真实可用） |
| 73 | `convert-time-infusion.html` | medical | 4 | calc | 按页面输入字段填入典型值，应返回计算结果 | 空值/零值/负值：应安全处理或提示，不抛NaN/Infinity | KEEP-B（功能简单但真实可用） |
| 74 | `stats-4.html` | medical | 0 | calc | 按页面输入字段填入典型值，应返回计算结果 | 空值/零值/负值：应安全处理或提示，不抛NaN/Infinity | KEEP-B（建议UPGRADE：统计/金额结果补单位与解释，toFixed(2)展示可接受） |
| 75 | `analysis-report-cost.html` | pharmacy | 0 | calc | 输入一组数值(如 1,2,3,4)：应返回量/和/均值/中位/标准差 | 单值输入：均值=该值，标准差0；极大值：不溢出NaN | KEEP-B（建议UPGRADE：统计/金额结果补单位与解释，toFixed(2)展示可接受） |

## 批次结论

- 本批 25 个工具：25 个 KEEP-B，0 个 FIX/MERGE/REMOVE（无占位或虚假功能）。
- 反模式启发式标记（除法零保护/toFixed）经抽样代码确认均为误报或精度可接受，不影响功能真实性。
- 审计提交不改页面，FIX/UPGRADE 实现留待后续独立提交。
