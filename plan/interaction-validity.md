# 交互有效性扫描（第二轮：点了到底有没有用）

- 扫描时间：2026/11/5 01:37:10
- 覆盖工具页：**4916**
- 有输入控件的页：**4512**
- 无输入控件（纯展示/参考卡，跳过）：**404**
- 有输入但无主按钮（实时计算/表单提交，不计缺陷）：**588**
- 命中至少一类问题：**431**

> 口径：① 有效性＝先填值→记录快照→**改一个输入为明显不同的合法值**→再点主按钮→比较前后快照（排除「加载时已自动算过一次」的假阴性）；② 空态＝清空所有输入后点主按钮，结果区给出 NaN/Infinity/undefined/null/0/空串或结论即为缺陷；③ 死控件＝控件 id 在全部 `<script>` 中从未出现（且页面无 `querySelectorAll('input')` / `FormData` 这类泛化读取，内联 oninput 绑定的不计）。快照优先取 `#result/#output/.result*` 等结果容器，无则回退整页正文（剔除控件内的当前值）。

## 总览（按类型）

| 类型 | 页数 | 严重度 |
|---|---|---|
| 空输入直接给出 NaN/Infinity/undefined/null/0 | **296** | 高 |
| 空输入直接给出结论（优秀/正常/合格…） | **56** | 中 |
| 改了输入再点主按钮，输出快照不变（低置信度线索，需人工复验） | **48** | 低 |
| 重置按钮未改变任何输入 | **31** | 低 |
| 点击主按钮抛异常（含 console 报错） | **1** | 高 |
| 清空输入 / 改值时页内抛异常 | **1** | 高 |
| 导出/下载按钮 onclick 目标函数不存在（必死） | **1** | 中 |
| 死控件（静态） | **1** 页 / 2 个控件 | 低-中 |

> **置信度分层**：高/中置信度缺陷页 **384** 页（点击抛异常、空态坏值/结论、死按钮、死控件）；`no_effect` **48** 页已改用「0.8× 相对量级变异」主探针，并在无变化时追加「5× 放大探针」——放大后仍无变化才保留本类，放大后才变化的 **0** 页归入 `probe_masked`（显示精度/分档阈值掩蔽，不计缺陷）。剩余 `no_effect` 页的逐页三档结论（真无效 / 阈值掩蔽 / 探针失真）见 `plan/no-effect-recheck.md`。

## 按行业分布（便于分派修复线）

| 类型 | 集中行业（页数） |
|---|---|
| 空输入直接给出 NaN/Infinity/undefined/null/0 | tools/eco/ 18、tools/ai/ 17、tools/tax/ 16、tools/surveying/ 14、tools/dynamics/ 12、tools/robotics/ 12、tools/geometry/ 11、tools/accounting/ 8 |
| 空输入直接给出结论（优秀/正常/合格…） | tools/leather/ 4、tools/ent/ 3、tools/safety/ 3、tools/agriculture/ 2、tools/biz/ 2、tools/eco/ 2、tools/electronics/ 2、tools/energy/ 2 |
| 改了输入再点主按钮，输出快照不变（低置信度线索，需人工复验） | tools/it/ 11、tools/design/ 2、tools/food-processing/ 2、tools/forensic-medicine/ 2、tools/hematology/ 2、tools/image/ 2、tools/life/ 2、tools/music/ 2 |
| 重置按钮未改变任何输入 | tools/rheumatology/ 4、tools/it/ 3、tools/rehabilitation/ 3、tools/elderly/ 2、tools/general/ 2、tools/hematology/ 2、tools/audio/ 1、tools/biz/ 1 |
| 点击主按钮抛异常（含 console 报错） | tools/it/ 1 |
| 清空输入 / 改值时页内抛异常 | tools/astronomy/ 1 |
| 导出/下载按钮 onclick 目标函数不存在（必死） | tools/it/ 1 |

## Top 50 高影响页面（按严重度加权）

| # | 页面 | 得分 | 类型 | 证据 |
|---|---|---|---|---|
| 1 | `tools/astronomy/hubble-redshift-distance.html` | 5.6 | empty_bogus, interact_error | 空输入点「计算」→ 结果区 0.00距离 d (Mpc)0.00d (百万光年)0.00退行速度 v = cz (km/s)0.0000d (十亿光年) ⏐ 📋 复制结果⬇️ 导出 TXT |
| 2 | `tools/it/matrix-multiplier.html` | 5.6 | empty_bogus, click_error | 空输入点「计算乘法」→ 结果区 结果 C = A × B （0×0）：计算步骤： ⏐ 📋 复制结果⬇️ 导出 TXT |
| 3 | `tools/pr/risk-assessment.html` | 3.4 | empty_bogus, no_effect | 空输入点「📋 评估」→ 结果区 0风险总数0低风险0中风险0高/极高 ⏐ 📋 复制结果⬇️ 导出 TXT |
| 4 | `tools/accounting/cash-conversion-cycle.html` | 2.6 | empty_bogus | 空输入点「计算」→ 结果区 0.00现金转换周期 CCC (天)0.00营业周期（存货 + 应收）(天)0.00应付占营业周期比 (%) ⏐ 📋 复制结果⬇️ 导出 TXT |
| 5 | `tools/accounting/ebit.html` | 2.6 | empty_bogus | 空输入点「计算」→ 结果区 0.00EBIT (万元)0.00毛利 (万元)0.00营业利润率 (%) ⏐ 📋 复制结果⬇️ 导出 TXT |
| 6 | `tools/accounting/ebitda.html` | 2.6 | empty_bogus | 空输入点「计算」→ 结果区 0.00EBITDA (万元)0.00EBIT 占 EBITDA (%)0.00折旧摊销占比 (%)0.00折旧与摊销 (万元) ⏐ 📋 复制结果⬇️ 导出 TXT |
| 7 | `tools/accounting/free-cash-flow.html` | 2.6 | empty_bogus | 空输入点「计算」→ 结果区 0.00自由现金流 FCF (万元)0.00资本支出占经营现金流 (%)0.000经营现金流覆盖资本支出倍数0.00经营活动现金流净额 (万元) ⏐ 📋 复制结果⬇️ 导… |
| 8 | `tools/accounting/gross-profit.html` | 2.6 | empty_bogus | 空输入点「计算」→ 结果区 0.00毛利 (万元)0.00毛利率 (%)0.000收入成本倍数0.0000成本毛利比 ⏐ 📋 复制结果⬇️ 导出 TXT |
| 9 | `tools/accounting/operating-cash-flow.html` | 2.6 | empty_bogus | 空输入点「计算」→ 结果区 0.00经营现金流 OCF (万元)0.0000现金流/净利 比0.000折旧占经营现金流比 (%) ⏐ 📋 复制结果⬇️ 导出 TXT |
| 10 | `tools/accounting/roe-dupont.html` | 2.6 | empty_bogus | 空输入点「计算」→ 结果区 0.00净资产收益率 ROE (%)0.000净利率 NM (%)0.0000资产收益率 ROA (%) ⏐ 📋 复制结果⬇️ 导出 TXT |
| 11 | `tools/accounting/working-capital.html` | 2.6 | empty_bogus | 空输入点「计算」→ 结果区 0.00营运资金 WC (万元)0.000流动比率0.00营运资金占流动资产 (%)0.00流动资产负债合计 (万元) ⏐ 📋 复制结果⬇️ 导出 TXT |
| 12 | `tools/advertising/assessor-52.html` | 2.6 | empty_bogus | 空输入点「评估活动方案」→ 结果区 0.0%活动 ROI¥0净收益/亏损¥0单客获取成本 CPA¥0.00千次曝光成本 CPM ⏐ 📋 复制结果⬇️ 导出 TXT |
| 13 | `tools/advertising/assessor-54.html` | 2.6 | empty_bogus | 空输入点「计算投放效果」→ 结果区 0OTS 接触机会0.0%到达率 Reach0.0平均频次 Frequency0.0GRP 总收视点 ⏐ 📋 复制结果⬇️ 导出 TXT |
| 14 | `tools/advertising/assessor-55.html` | 2.6 | empty_bogus | 空输入点「评估投放效果」→ 结果区 0.0GRP 总收视点0.0%到达率 Reach0.0平均频次¥0CPP 每收视点成本 ⏐ 📋 复制结果⬇️ 导出 TXT |
| 15 | `tools/advertising/convert-26.html` | 2.6 | empty_bogus | 空输入点「换算」→ 结果区 物理尺寸 = NaN mm DPI 与 PPI 同义，均指每英寸像素数 常用 DPI 参考：屏幕 96，高清 150–220，印刷 300，精细宣传册 600 300 dp… |
| 16 | `tools/advertising/reach-frequency.html` | 2.6 | empty_bogus | 空输入点「🧮 计算指标」→ 结果区 0.0%到达率0.00平均频次0GRP 总收视点 ⏐ ¥0.00CPM 千次曝光¥0.00CPR 单人到达¥0.00CP/GRP ⏐ 📋 复制结果⬇️ 导出 T… |
| 17 | `tools/aerospace/descent-rate.html` | 2.6 | empty_bogus | 空输入点「计算」→ 结果区 0.0下降率 (m/min)0.00下降率 (m/s)0.00水平速度 (m/s)0.000下降梯度 (%) ⏐ 📋 复制结果⬇️ 导出 TXT |
| 18 | `tools/aerospace/drag-force.html` | 2.6 | empty_bogus | 空输入点「计算」→ 结果区 0.00阻力 D (N)0.0动压 q = ½ρv² (Pa)0.00阻力 (kgf) ⏐ 📋 复制结果⬇️ 导出 TXT |
| 19 | `tools/aerospace/lift-equation.html` | 2.6 | empty_bogus | 空输入点「计算」→ 结果区 0.00升力 L (N)0.0动压 q = ½ρv² (Pa)0.00升力 (kgf) ⏐ 📋 复制结果⬇️ 导出 TXT |
| 20 | `tools/aerospace/lift-force.html` | 2.6 | empty_bogus | 空输入点「计算」→ 结果区 0.00升力 L (kN)0.0升力 (kgf) ⏐ 📋 复制结果⬇️ 导出 TXT |
| 21 | `tools/aerospace/thrust-required.html` | 2.6 | empty_bogus | 空输入点「计算」→ 结果区 0.000所需推力 (kN)0.0动压 q = ½ρv² (Pa)0.00等效推力 (kgf) ⏐ 📋 复制结果⬇️ 导出 TXT |
| 22 | `tools/agriculture/agri-calculator.html` | 2.6 | empty_bogus | 空输入点「计算配比」→ 结果区 氮 (N)0.00kg磷 (P₂O₅)0.00kg钾 (K₂O)0.00kg配方比例：0-0-0施肥面积：0 亩每亩用量：0 kg/亩肥料总量：0.0 kg ⏐ 📋 … |
| 23 | `tools/ai/ai-11.html` | 2.6 | empty_bogus | 空输入点「计算」→ 结果区 损失差距：0.0000 准确率差距：0.00 %过拟合风险：低 建议：继续训练或早停 ⏐ 📋 复制结果⬇️ 导出 TXT |
| 24 | `tools/ai/ai-12.html` | 2.6 | empty_bogus | 空输入点「计算」→ 结果区 理论扩充量：0 张有效等效量：0 张避免过拟合建议：建议继续收集真实数据 ⏐ 📋 复制结果⬇️ 导出 TXT |
| 25 | `tools/ai/ai-13.html` | 2.6 | empty_bogus | 空输入点「计算」→ 结果区 早停等待时间：0.0 分钟最小训练时间：0.0 分钟最大建议 epoch：0 ⏐ 📋 复制结果⬇️ 导出 TXT |
| 26 | `tools/ai/ai-14.html` | 2.6 | empty_bogus | 空输入点「计算」→ 结果区 点积：0.0000 查询模：0.0000 文档模：0.0000 余弦相似度：0.0000 ⏐ 📋 复制结果⬇️ 导出 TXT |
| 27 | `tools/ai/ai-4.html` | 2.6 | empty_bogus | 空输入点「计算」→ 结果区 欧氏距离：0.0000 曼哈顿距离：0.0000 余弦相似度：0.0000 ⏐ 📋 复制结果⬇️ 导出 TXT |
| 28 | `tools/ai/ai-6.html` | 2.6 | empty_bogus | 空输入点「计算」→ 结果区 全连接参数：0 个卷积核参数：0 个显存估算 MB：0.0000 MB ⏐ 📋 复制结果⬇️ 导出 TXT |
| 29 | `tools/ai/attention-flops.html` | 2.6 | empty_bogus | 空输入点「计算」→ 结果区 单层 FLOPs：0 全模型 GFLOPs：0.0 GFLOP ⏐ 📋 复制结果⬇️ 导出 TXT |
| 30 | `tools/ai/augmentation-multiplier.html` | 2.6 | empty_bogus | 空输入点「计算」→ 结果区 增强后总量：0 样本 ⏐ 📋 复制结果⬇️ 导出 TXT |
| 31 | `tools/ai/flops.html` | 2.6 | empty_bogus | 空输入点「计算」→ 结果区 卷积 FLOPs：0 全连接 FLOPs：0 总 FLOPs：0 MACs（约）：0 ⏐ 📋 复制结果⬇️ 导出 TXT |
| 32 | `tools/ai/lr-decay.html` | 2.6 | empty_bogus | 空输入点「计算」→ 结果区 当前 LR：0.000000 ⏐ 📋 复制结果⬇️ 导出 TXT |
| 33 | `tools/ai/lr-warmup.html` | 2.6 | empty_bogus | 空输入点「计算」→ 结果区 预热步数：0 步预热末 LR：0.000000 ⏐ 📋 复制结果⬇️ 导出 TXT |
| 34 | `tools/ai/multi-agent-overhead.html` | 2.6 | empty_bogus | 空输入点「计算」→ 结果区 消息总数：0 条总流量 KB：0 KB ⏐ 📋 复制结果⬇️ 导出 TXT |
| 35 | `tools/ai/relu-leakyrelu.html` | 2.6 | empty_bogus | 空输入点「计算」→ 结果区 ReLU：0.00 LeakyReLU：0.00 ELU：0.00 ⏐ 📋 复制结果⬇️ 导出 TXT |
| 36 | `tools/ai/token-2.html` | 2.6 | empty_bogus | 空输入点「计算」→ 结果区 输入费用：0.0000 USD输出费用：0.0000 USD总费用：0.0000 USD人民币约：0.0000 CNY ⏐ 📋 复制结果⬇️ 导出 TXT |
| 37 | `tools/ai/token-usage.html` | 2.6 | empty_bogus | 空输入点「计算」→ 结果区 估算 tokens：0 token ⏐ 📋 复制结果⬇️ 导出 TXT |
| 38 | `tools/ai/transformer-params.html` | 2.6 | empty_bogus | 空输入点「计算」→ 结果区 Transformer主体(亿)：0.00 亿嵌入参数(亿)：0.00 亿 ⏐ 📋 复制结果⬇️ 导出 TXT |
| 39 | `tools/ai/vram-estimate.html` | 2.6 | empty_bogus | 空输入点「计算」→ 结果区 权重显存：0.0 GB总显存估算：0.0 GB ⏐ 📋 复制结果⬇️ 导出 TXT |
| 40 | `tools/astronomy/kepler-equation.html` | 2.6 | empty_bogus | 空输入点「计算」→ 结果区 0.000偏近点角 E (°)0.00000E (rad) ⏐ 📋 复制结果⬇️ 导出 TXT |
| 41 | `tools/astronomy/light-travel-time.html` | 2.6 | empty_bogus | 空输入点「计算」→ 结果区 0.000传播时间 t (min)0.0t (s)0.0000距离 (天文单位 AU)0.0000传播时间 (h)0.000e+0距离 (光年) ⏐ 📋 复制结果⬇️ 导… |
| 42 | `tools/baking/recipe-scaler.html` | 2.6 | empty_bogus | 空输入点「计算」→ 结果区 缩放后配方（×0） ⏐ 📋 复制结果⬇️ 导出 TXT |
| 43 | `tools/banking/amortization-first-interest.html` | 2.6 | empty_bogus | 空输入点「计算」→ 结果区 0.00首月利息 I₁0.00首月还本金0.000年利率 (%)0.0000首月利息占本金比 (%) ⏐ 📋 复制结果⬇️ 导出 TXT |
| 44 | `tools/banking/continuous-compounding.html` | 2.6 | empty_bogus | 空输入点「计算」→ 结果区 0.00连续复利终值 A0.00利息总额0.0000年实际收益率 (%)0.0000较年复利增益 (%) ⏐ 📋 复制结果⬇️ 导出 TXT |
| 45 | `tools/banking/effective-annual-rate.html` | 2.6 | empty_bogus | 空输入点「计算」→ 结果区 0.000有效年利率 EAR (%)0.00000EAR (小数)0.0000EAR 高于名义利率 (百分点)0.0000与连续复利之差 (百分点) ⏐ 📋 复制结果⬇️… |
| 46 | `tools/banking/net-worth.html` | 2.6 | empty_bogus | 空输入点「计算」→ 结果区 0净资产 NW (元)0.00负债率 (%)0.000资产覆盖倍数0.00净资产占资产 (%) ⏐ 📋 复制结果⬇️ 导出 TXT |
| 47 | `tools/banking/tax-equivalent-yield.html` | 2.6 | empty_bogus | 空输入点「计算」→ 结果区 0.000税后等效收益率 TEY (%)0.000应税需高出的百分点0.0边际税率 (%)0.0000免税溢价系数减一 ⏐ 📋 复制结果⬇️ 导出 TXT |
| 48 | `tools/chemistry/gibbs-free-energy.html` | 2.6 | empty_bogus | 空输入点「计算」→ 结果区 0.000ΔG (kJ/mol)平衡反应方向 ⏐ 📋 复制结果⬇️ 导出 TXT |
| 49 | `tools/chemistry/kp-kc.html` | 2.6 | empty_bogus | 空输入点「计算」→ 结果区 0.000e+0压力平衡常数 Kp0.0RT (L·atm/(mol·K)) ⏐ 📋 复制结果⬇️ 导出 TXT |
| 50 | `tools/chemistry/mole-fraction.html` | 2.6 | empty_bogus | 空输入点「计算」→ 结果区 0.0000总物质的量 (mol) ⏐ 📋 复制结果⬇️ 导出 TXT |

## 一、按钮有效性（点了没反应 / 点了报错）

### 点击主按钮抛异常（含 console 报错）（1 页）

- `tools/it/matrix-multiplier.html` — 按钮「计算乘法」｜click: Cannot read properties of null (reading 'value') @ getM (/tools/it/matrix-multiplier.html:283:68)

### 清空输入 / 改值时页内抛异常（1 页）

- `tools/astronomy/hubble-redshift-distance.html` — 清空/改值阶段｜empty: __charDistUpdate is not defined @ oninput (/tools/astronomy/hubble-redshift-distance.html:403:252) \| fill: __charDistUpdate…

## 二、空态（没填也敢给结论）

### 空输入直接给出 NaN/Infinity/undefined/null/0（296 页）

- `tools/astronomy/hubble-redshift-distance.html` — 空输入点「计算」→ 结果区 0.00距离 d (Mpc)0.00d (百万光年)0.00退行速度 v = cz (km/s)0.0000d (十亿光年) ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/it/matrix-multiplier.html` — 空输入点「计算乘法」→ 结果区 结果 C = A × B （0×0）：计算步骤： ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/pr/risk-assessment.html` — 空输入点「📋 评估」→ 结果区 0风险总数0低风险0中风险0高/极高 ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/accounting/cash-conversion-cycle.html` — 空输入点「计算」→ 结果区 0.00现金转换周期 CCC (天)0.00营业周期（存货 + 应收）(天)0.00应付占营业周期比 (%) ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/accounting/ebit.html` — 空输入点「计算」→ 结果区 0.00EBIT (万元)0.00毛利 (万元)0.00营业利润率 (%) ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/accounting/ebitda.html` — 空输入点「计算」→ 结果区 0.00EBITDA (万元)0.00EBIT 占 EBITDA (%)0.00折旧摊销占比 (%)0.00折旧与摊销 (万元) ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/accounting/free-cash-flow.html` — 空输入点「计算」→ 结果区 0.00自由现金流 FCF (万元)0.00资本支出占经营现金流 (%)0.000经营现金流覆盖资本支出倍数0.00经营活动现金流净额 (万元) ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/accounting/gross-profit.html` — 空输入点「计算」→ 结果区 0.00毛利 (万元)0.00毛利率 (%)0.000收入成本倍数0.0000成本毛利比 ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/accounting/operating-cash-flow.html` — 空输入点「计算」→ 结果区 0.00经营现金流 OCF (万元)0.0000现金流/净利 比0.000折旧占经营现金流比 (%) ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/accounting/roe-dupont.html` — 空输入点「计算」→ 结果区 0.00净资产收益率 ROE (%)0.000净利率 NM (%)0.0000资产收益率 ROA (%) ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/accounting/working-capital.html` — 空输入点「计算」→ 结果区 0.00营运资金 WC (万元)0.000流动比率0.00营运资金占流动资产 (%)0.00流动资产负债合计 (万元) ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/advertising/assessor-52.html` — 空输入点「评估活动方案」→ 结果区 0.0%活动 ROI¥0净收益/亏损¥0单客获取成本 CPA¥0.00千次曝光成本 CPM ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/advertising/assessor-54.html` — 空输入点「计算投放效果」→ 结果区 0OTS 接触机会0.0%到达率 Reach0.0平均频次 Frequency0.0GRP 总收视点 ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/advertising/assessor-55.html` — 空输入点「评估投放效果」→ 结果区 0.0GRP 总收视点0.0%到达率 Reach0.0平均频次¥0CPP 每收视点成本 ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/advertising/convert-26.html` — 空输入点「换算」→ 结果区 物理尺寸 = NaN mm DPI 与 PPI 同义，均指每英寸像素数 常用 DPI 参考：屏幕 96，高清 150–220，印刷 300，精细宣传册 600 300 dpi 常见尺寸像素：A4 约 …
- `tools/advertising/reach-frequency.html` — 空输入点「🧮 计算指标」→ 结果区 0.0%到达率0.00平均频次0GRP 总收视点 ⏐ ¥0.00CPM 千次曝光¥0.00CPR 单人到达¥0.00CP/GRP ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/aerospace/descent-rate.html` — 空输入点「计算」→ 结果区 0.0下降率 (m/min)0.00下降率 (m/s)0.00水平速度 (m/s)0.000下降梯度 (%) ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/aerospace/drag-force.html` — 空输入点「计算」→ 结果区 0.00阻力 D (N)0.0动压 q = ½ρv² (Pa)0.00阻力 (kgf) ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/aerospace/lift-equation.html` — 空输入点「计算」→ 结果区 0.00升力 L (N)0.0动压 q = ½ρv² (Pa)0.00升力 (kgf) ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/aerospace/lift-force.html` — 空输入点「计算」→ 结果区 0.00升力 L (kN)0.0升力 (kgf) ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/aerospace/thrust-required.html` — 空输入点「计算」→ 结果区 0.000所需推力 (kN)0.0动压 q = ½ρv² (Pa)0.00等效推力 (kgf) ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/agriculture/agri-calculator.html` — 空输入点「计算配比」→ 结果区 氮 (N)0.00kg磷 (P₂O₅)0.00kg钾 (K₂O)0.00kg配方比例：0-0-0施肥面积：0 亩每亩用量：0 kg/亩肥料总量：0.0 kg ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/ai/ai-11.html` — 空输入点「计算」→ 结果区 损失差距：0.0000 准确率差距：0.00 %过拟合风险：低 建议：继续训练或早停 ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/ai/ai-12.html` — 空输入点「计算」→ 结果区 理论扩充量：0 张有效等效量：0 张避免过拟合建议：建议继续收集真实数据 ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/ai/ai-13.html` — 空输入点「计算」→ 结果区 早停等待时间：0.0 分钟最小训练时间：0.0 分钟最大建议 epoch：0 ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/ai/ai-14.html` — 空输入点「计算」→ 结果区 点积：0.0000 查询模：0.0000 文档模：0.0000 余弦相似度：0.0000 ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/ai/ai-4.html` — 空输入点「计算」→ 结果区 欧氏距离：0.0000 曼哈顿距离：0.0000 余弦相似度：0.0000 ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/ai/ai-6.html` — 空输入点「计算」→ 结果区 全连接参数：0 个卷积核参数：0 个显存估算 MB：0.0000 MB ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/ai/attention-flops.html` — 空输入点「计算」→ 结果区 单层 FLOPs：0 全模型 GFLOPs：0.0 GFLOP ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/ai/augmentation-multiplier.html` — 空输入点「计算」→ 结果区 增强后总量：0 样本 ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/ai/flops.html` — 空输入点「计算」→ 结果区 卷积 FLOPs：0 全连接 FLOPs：0 总 FLOPs：0 MACs（约）：0 ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/ai/lr-decay.html` — 空输入点「计算」→ 结果区 当前 LR：0.000000 ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/ai/lr-warmup.html` — 空输入点「计算」→ 结果区 预热步数：0 步预热末 LR：0.000000 ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/ai/multi-agent-overhead.html` — 空输入点「计算」→ 结果区 消息总数：0 条总流量 KB：0 KB ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/ai/relu-leakyrelu.html` — 空输入点「计算」→ 结果区 ReLU：0.00 LeakyReLU：0.00 ELU：0.00 ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/ai/token-2.html` — 空输入点「计算」→ 结果区 输入费用：0.0000 USD输出费用：0.0000 USD总费用：0.0000 USD人民币约：0.0000 CNY ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/ai/token-usage.html` — 空输入点「计算」→ 结果区 估算 tokens：0 token ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/ai/transformer-params.html` — 空输入点「计算」→ 结果区 Transformer主体(亿)：0.00 亿嵌入参数(亿)：0.00 亿 ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/ai/vram-estimate.html` — 空输入点「计算」→ 结果区 权重显存：0.0 GB总显存估算：0.0 GB ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/astronomy/kepler-equation.html` — 空输入点「计算」→ 结果区 0.000偏近点角 E (°)0.00000E (rad) ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/astronomy/light-travel-time.html` — 空输入点「计算」→ 结果区 0.000传播时间 t (min)0.0t (s)0.0000距离 (天文单位 AU)0.0000传播时间 (h)0.000e+0距离 (光年) ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/baking/recipe-scaler.html` — 空输入点「计算」→ 结果区 缩放后配方（×0） ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/banking/amortization-first-interest.html` — 空输入点「计算」→ 结果区 0.00首月利息 I₁0.00首月还本金0.000年利率 (%)0.0000首月利息占本金比 (%) ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/banking/continuous-compounding.html` — 空输入点「计算」→ 结果区 0.00连续复利终值 A0.00利息总额0.0000年实际收益率 (%)0.0000较年复利增益 (%) ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/banking/effective-annual-rate.html` — 空输入点「计算」→ 结果区 0.000有效年利率 EAR (%)0.00000EAR (小数)0.0000EAR 高于名义利率 (百分点)0.0000与连续复利之差 (百分点) ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/banking/net-worth.html` — 空输入点「计算」→ 结果区 0净资产 NW (元)0.00负债率 (%)0.000资产覆盖倍数0.00净资产占资产 (%) ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/banking/tax-equivalent-yield.html` — 空输入点「计算」→ 结果区 0.000税后等效收益率 TEY (%)0.000应税需高出的百分点0.0边际税率 (%)0.0000免税溢价系数减一 ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/chemistry/gibbs-free-energy.html` — 空输入点「计算」→ 结果区 0.000ΔG (kJ/mol)平衡反应方向 ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/chemistry/kp-kc.html` — 空输入点「计算」→ 结果区 0.000e+0压力平衡常数 Kp0.0RT (L·atm/(mol·K)) ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/chemistry/mole-fraction.html` — 空输入点「计算」→ 结果区 0.0000总物质的量 (mol) ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/chemistry/partial-pressure.html` — 空输入点「计算」→ 结果区 0.00分压 Pᵢ (kPa)0.00其余组分分压 (kPa)0.000摩尔分数 (%)0.000其余组分占比 (%) ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/chinese-cook/estimate-16.html` — 空输入点「🧮 计算」→ 结果区 0% of 0 = 0.00 ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/civil/load-combination.html` — 空输入点「计算」→ 结果区 0.0γ_G·S_Gk0.0γ_Q·S_Qk0.0组合效应 S (kN·m) ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/civil/rock-mass-rating.html` — 空输入点「计算」→ 结果区 0RMR 总分V 级（极差）围岩级别 ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/construction/tax.html` — 空输入点「🧮 计算」→ 结果区 0增值税 (元)0城建税 (元)0教育费附加 (元)0地方教育附加 (元)0附加税费合计 (元)0含税造价 (元)0价税合计含附加 (元)0.00%综合税费率 ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/design/px-to-rem.html` — 空输入点「计算」→ 结果区 转换结果 ⏐ 0px = 0.0000rem ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/dynamics/angular-momentum.html` — 空输入点「计算」→ 结果区 0.000角动量 L (kg·m²/s)0.000两倍角动量0.0000由 L 反推角速度0.000转动动能 (J) ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/dynamics/impulse.html` — 空输入点「计算」→ 结果区 0.00冲量 J (N·s)0.0冲量 (N·ms 牛毫秒)0.0000冲量 (kgf·s 千克力秒)0.0000力与作用时间之比 (N/s) ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/dynamics/inclined-plane-accel.html` — 空输入点「计算」→ 结果区 0.000加速度 a (m/s²)静止/需外力状态 ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/dynamics/kinetic-friction.html` — 空输入点「计算」→ 结果区 0.00动摩擦力 F_k (N)0.0000正压力与摩擦系数之比0.0000摩擦力 (kgf 千克力)0.0000摩擦系数平方 ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/dynamics/momentum.html` — 空输入点「计算」→ 结果区 0.0动量 p (kg·m/s)0.0动能 Ek (J)0.0动量乘速度 (kg·m²/s²)0.0000质量与速度之比 (kg·s/m) ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/dynamics/power-force.html` — 空输入点「计算」→ 结果区 0.0功率 P (W)0.00P (kW)0.000功率 (公制马力 PS)0.000功率 (英制马力 hp)0.000每小时做功 (kJ/h) ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/dynamics/power-rotational.html` — 空输入点「计算」→ 结果区 0.00旋转功率 P (W)0.0000旋转功率 (hp)0.0000旋转功率 (kW)0.0000旋转功率 (PS) ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/dynamics/rotational-kinetic-energy.html` — 空输入点「计算」→ 结果区 0.000转动动能 E (J)0.000两倍转动动能（I 乘 ω²）0.0000角动量 L0.0000转速 (转/秒) ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/dynamics/spring-potential.html` — 空输入点「计算」→ 结果区 0.000弹性势能 U (J)0.000对应弹力 F (N)0.0000劲度与位移平方之积 (J)0.0000弹性势能 (mJ 毫焦) ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/dynamics/torque-force.html` — 空输入点「计算」→ 结果区 0.00力矩 τ (N·m)0.0000有效力臂 (m)0.000径向分量 (N) ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/dynamics/weight-force.html` — 空输入点「计算」→ 结果区 0.00重力 W (N)0.00W (kgf)0.00月球表面重力 (N)0.00火星表面重力 (N)0.000重力 W (kgf 标准重力) ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/dynamics/work-energy-theorem.html` — 空输入点「计算」→ 结果区 0.00合外力功 W (J)0.00末动能 (J)0.00初动能 (J) ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/eco/battery-storage.html` — 空输入点「计算」→ 结果区 可用电量：0.00 kWh总能量：0.00 kWh ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/eco/convert-air-aqi.html` — 空输入点「计算」→ 结果区 0等级 优 ｜ 输入浓度 0 µg/m³ ｜ 建议 可正常户外活动 ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/eco/eco-10.html` — 空输入点「计算」→ 结果区 年发电量：0.00 MWh（千 kWh）年减排量：0.00 吨 CO₂等效植树：0 棵 ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/eco/eco-11.html` — 空输入点「计算」→ 结果区 单次额外燃油：0.00 L年额外燃油：0.00 L年额外碳排：0.00 吨 ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/eco/eco-16.html` — 空输入点「计算」→ 结果区 年发电量：0.00 MWh（千 kWh）年减排量：0.00 吨 CO₂等效减少汽车：0 辆 ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/eco/eco-4.html` — 空输入点「计算」→ 结果区 日产生量：0.00 吨/天年产生量：0.00 吨/年累计吨天数：0 kg·天 ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/eco/eco-7.html` — 空输入点「计算」→ 结果区 总标准煤：0.00 kgce总 kWh：0.00 kWh总 MJ：0.00 MJ ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/eco/eco-8.html` — 空输入点「计算」→ 结果区 总株数：0 株年碳汇量：0.00 吨/年累计碳汇：0.00 吨 ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/eco/eco.html` — 空输入点「计算」→ 结果区 电力碳排：0.00 kg燃煤碳排：0.00 kg天然气碳排：0.00 kg汽油碳排：0.00 kg总碳排：0.00 kg ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/eco/ecological-footprint.html` — 空输入点「计算」→ 结果区 生态足迹：0.000 gha ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/eco/electricity-carbon.html` — 空输入点「计算」→ 结果区 CO₂ 排放：0.00 kg等效树木吸收天数：0.0 天 ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/eco/env-impact-score.html` — 空输入点「计算」→ 结果区 综合评分：0.0 分最高项：0 分 ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/eco/landfill-methane.html` — 空输入点「计算」→ 结果区 CH₄ 产量：0.0 kg/年CO₂ 当量：0.0 kgCO₂e ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/eco/rainwater-harvest.html` — 空输入点「计算」→ 结果区 收集量：0 L折合吨：0.00 吨 ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/eco/solar-output.html` — 空输入点「计算」→ 结果区 发电量：0.0 kWh等效减排：0.00 kgCO₂ ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/eco/water-footprint.html` — 空输入点「计算」→ 结果区 总耗水：0 L折合 m³：0.00 m³ ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/eco/water-saving.html` — 空输入点「计算」→ 结果区 节约水量：0.0 L折合吨：0.00 吨 ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/eco/wind-power.html` — 空输入点「计算」→ 结果区 功率：0.00 kW ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/economics/balance-of-trade.html` — 空输入点「计算」→ 结果区 0贸易差额 BoT0.00差额占出口比 (%)0.000出口进口比0进出口总额 ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/economics/compound-amount.html` — 空输入点「计算」→ 结果区 0.00复利终值 F0.00利息总额 ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/economics/fv-annuity.html` — 空输入点「计算」→ 结果区 0.00年金终值 FV0.00利息总额 ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/economics/labor-force.html` — 空输入点「计算」→ 结果区 0劳动力 LF0.00失业率 (%)0.00就业率 (%)0.0000就业与失业人数比 ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/economics/okuns-law.html` — 空输入点「计算」→ 结果区 0.00失业率变化 Δu (百分点)0.00增长缺口0.00失业率变化幅值 (百分点)0.000相对增长缺口 (%) ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/economics/pv-annuity.html` — 空输入点「计算」→ 结果区 0.00年金现值 PV0.00贴现总额 ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/economics/real-gdp.html` — 空输入点「计算」→ 结果区 0.00实际 GDP0.00价格扭曲部分0.00实际占名义比重 (%)0.00价格扭曲占比 (%) ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/electrical/current-divider.html` — 空输入点「计算」→ 结果区 电阻须>0。 ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/electrical/led-resistor.html` — 空输入点「计算」→ 结果区 电流须>0。 ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/electrical/load-curve.html` — 空输入点「计算并绘制」→ 结果区 0最大负荷 (kW)0最小负荷 (kW)0.0平均负荷 (kW)—%负荷率0峰谷差 (kW)—%峰谷差率 ⏐ 日用电量 0 kWh 负荷率 —% ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/electrical/opamp-gain.html` — 空输入点「计算」→ 结果区 R_in 须>0。 ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/electrical/rc-filter.html` — 空输入点「计算」→ 结果区 R、C 须>0。 ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/electrical/rlc-resonance.html` — 空输入点「计算」→ 结果区 L、C 须>0。 ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/electromagnetism/coil-torque.html` — 空输入点「计算」→ 结果区 0.0000磁力矩 τ (N·m) ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/electromagnetism/energy-capacitor.html` — 空输入点「计算」→ 结果区 0.000储能 E (µJ)0.000e+0储能 E (J)0.000电荷量 (mC)0.0000e+0电荷量 Q = CV (C) ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/electromagnetism/magnetic-flux.html` — 空输入点「计算」→ 结果区 0.000e+0磁通 Φ (Wb)0.00Φ (µWb)0.0000磁通 (mWb)0.0000磁感应强度复算 (T) ⏐ 📋 复制结果⬇️ 导出 TXT ⏐ 📊 结果解读 结果含义磁通量 Φ=B…
- `tools/electromagnetism/solenoid-field.html` — 空输入点「计算」→ 结果区 0.000e+0磁感应强度 B (T)0.000B (mT)0.0000e+0单位电流磁场 (T/A)0.000磁感应强度 B (Gauss) ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/encode/base32.html` — 空输入点「计算」→ 结果区 编码长度：0 字符无填充长度：0 字符 ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/encode/encode-2.html` — 空输入点「计算」→ 结果区 估算差异比特数：0 位采样差异：0 位汉明距离：0 位 ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/encode/shannon-entropy.html` — 空输入点「计算」→ 结果区 信息熵 H：0.0000 bit/符号 ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/encode/url-encoded-length.html` — 空输入点「计算」→ 结果区 编码后长度：0 字符膨胀率：0.0 % ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/energy/carbon-footprint.html` — 空输入点「♻️ 计算」→ 结果区 年度总排放 ⏐ 0 kg CO₂e ⏐ 约合 ⏐ 0.00 吨 ⏐ 对比中国人均 ⏐ 0% ⏐ 对比全球人均 ⏐ 0% ⏐ 🌳 抵消需种树 ⏐ 0 棵 / 年 ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/energy/energy-calculator.html` — 空输入点「计算碳排放」→ 结果区 0.0月用电碳排放 kg ⏐ 0.0月用气碳排放 kg ⏐ 0.0月驾车碳排放 kg ⏐ 0年总碳排放 kg CO₂ ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/energy/power-consumption.html` — 空输入点「🧮 计算」→ 结果区 总耗电 ⏐ 0.0 kWh ⏐ 总电费 ⏐ ¥ 0.00 ⏐ 日均电费 ⏐ ¥ 0.00 ⏐ 日均耗电 ⏐ 0.0 kWh ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/ent/caloric-test.html` — 空输入点「计算分析」→ 结果区 0%单侧减弱 UW0%方向优势 DP0.0右耳总和(°/s)0.0左耳总和(°/s) ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/film/convert-time-1.html` — 空输入点「计算」→ 结果区 帧率需>0 ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/finance/calc-5.html` — 空输入点「🧮 计算」→ 结果区 总 ROI：0.00%净收益：0.00 元（投资成本 0.00 元，最终价值 0.00 元） ⏐ 0.00%总 ROI0.00净收益（元）—年化回报率 ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/fire/calc-water-pressure-hydrant.html` — 空输入点「🧮 计算所需压力」→ 结果区 满足压力校核0.000 MPa所需入口压力0.000 MPa可用入口压力+0.000 MPa安全余量高程折算 0.000 MPa = 栓口 0.000 MPa + 管损 0.000 MPa。 ⏐ 📋…
- `tools/fishery/calc-39.html` — 空输入点「🧮 计算」→ 结果区 0% of 0 = 0.00 ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/fishery/salinity-calculator.html` — 空输入点「🐟 计算」→ 结果区 ⚠️ 四项均需填写有效数值：现有水量须 >0，三个盐度须 ≥0。未测盐度请勿留空（淡水请明确输入 0） ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/fluid/bernoulli-pressure.html` — 空输入点「计算」→ 结果区 0.0压力 P₂ (Pa)0.00压差 (kPa) ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/fluid/buoyancy-force.html` — 空输入点「计算」→ 结果区 0.00浮力 F_b (N)0.0000排开液体质量 (kg)0.00排开液体质量 (g) ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/fluid/stagnation-pressure.html` — 空输入点「计算」→ 结果区 0.0驻点压力 p₀ (Pa)0.0动压 q (Pa)0.0000驻点压比 p0/p ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/food-processing/material-balance.html` — 空输入点「核算」→ 结果区 0.00总投入0.00总产出0.00损耗0.0%得率 ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/food-processing/recipe-cost-calculator.html` — 空输入点「核算成本」→ 结果区 ¥0.00总成本0g配方总用量0g实际耗用-每kg成本 ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/food/calc-concentration.html` — 空输入点「🐟 计算」→ 结果区 0% of 0 = 0.00 ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/general/wurenjixuantingwuchajisuan.html` — 空输入点「🧮 计算」→ 结果区 0.00水平误差 (m)0.00垂直误差 (m)0.00三维综合误差 (m)0.00开环飘移量 (m)高精度悬停悬停精度评定 ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/geometry/arc-length.html` — 空输入点「计算」→ 结果区 0.0000弧长 L (m)0.0000圆心角 (rad)0.000占整圆比例 (%)0.0000对应扇形面积 (m²) ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/geometry/chord-length.html` — 空输入点「计算」→ 结果区 0.0000弦长 c (m)0.0000半弦长 (m)0.0000对应弧长 (m)0.0000矢高 (m) ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/geometry/circle-area.html` — 空输入点「计算」→ 结果区 0.0000圆面积 A (m²)0.0000圆周长 (m)0.0000球体积 (m³)0.0000直径 (m)0.0000半圆面积 (m²) ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/geometry/circle-circumference.html` — 空输入点「计算」→ 结果区 0.0000圆周长 C (m)0.0000直径 (m)0.0000圆面积 (m²)0.0000球体积 (m³)0.0000内接正方形面积 (m²) ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/geometry/distance-3d.html` — 空输入点「计算」→ 结果区 0.000三维距离 d ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/geometry/ellipse-area.html` — 空输入点「计算」→ 结果区 0.000椭圆面积 A (m²)0.000000长短半轴之比0.000椭圆周长近似 (m)0.000等面积圆面积 π√(ab)（半径=√(ab)） ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/geometry/midpoint-2d.html` — 空输入点「计算」→ 结果区 0.000中点 x_M0.000中点 y_M ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/geometry/sector-area.html` — 空输入点「计算」→ 结果区 0.0000扇形面积 A (m²)0.000占整圆比例 (%)0.0000弧长 L = r·θ (m) ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/geometry/sphere-volume.html` — 空输入点「计算」→ 结果区 0.000球体体积 V (m³)0.000球表面积 (m²)0.000大圆周长 (m)0.000球体积 (L 升)0.000球体积 (cm³) ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/geometry/torus-volume.html` — 空输入点「计算」→ 结果区 0.000环体体积 V (m³)0.000环体表面积 (m²)0.000中心圆周长 (m)0.0000体积与环半径之比 ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/geometry/triangle-heron.html` — 空输入点「计算」→ 结果区 这三条边不能构成三角形：需满足任意两边之和大于第三边（当前 0、0、0）。 ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/healthcare/apgar.html` — 空输入点「计算」→ 结果区 Apgar 总分：0 分临床意义：重度窒息 ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/healthcare/chads-vasc.html` — 空输入点「计算」→ 结果区 评分：0 分风险分层：低危 ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/healthcare/healthcare-5.html` — 空输入点「计算」→ 结果区 维持需求：0.0 g目标需求：0.0 g每餐建议：0.0 g ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/healthcare/morse.html` — 空输入点「计算」→ 结果区 总分：0 分风险等级：低风险 ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/healthcare/wells.html` — 空输入点「计算」→ 结果区 评分：0 分临床概率：低度 ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/hematology/detector-5.html` — 空输入点「解读检测结果」→ 结果区 0.0%PNH总克隆（粒细胞）未检测到 PNH 克隆诊断评估无显著溶血风险溶血风险0 U/LLDH 水平 ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/home/lighting-calculator.html` — 空输入点「💡 计算」→ 结果区 0 所需总光通量 (lm)
- `tools/home/room-calculator.html` — 空输入点「🧮 计算」→ 结果区 0.00 面积 (m²)
- `tools/hr/overtime-pay-calc.html` — 空输入点「计算加班费」→ 结果区 工作日加班费：0.00 元休息日加班费：0.00 元法定节假日加班费：0.00 元总加班费：0.00 元 ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/insurance/complete-life-expectancy.html` — 空输入点「计算」→ 结果区 0.000完全期望寿命 e_x0生命表项数 N0.0000平均预期余命 ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/insurance/ibnr-estimate.html` — 空输入点「计算」→ 结果区 0.00IBNR 准备金 (元)0.00已付赔款比例 (%)0.00已付赔款 (元)0.00最终赔款 (元) ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/insurance/ibnr-reserve.html` — 空输入点「计算」→ 结果区 0.00IBNR 准备金 (元)0.00最终赔款估计 (元) ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/insurance/life-cover-need.html` — 空输入点「计算」→ 结果区 0.00建议保额 (元)0.00收入替代部分 (元)0.00保额下限 (元) ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/investment/bond-price.html` — 空输入点「计算」→ 结果区 0.00债券价格 P折价状态 ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/investment/discounted-payback.html` — 空输入点「计算」→ 结果区 0.00 年折现回收期 ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/investment/npv-calc.html` — 空输入点「计算」→ 结果区 0.00净现值 NPV ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/investment/payback-period.html` — 空输入点「计算」→ 结果区 0.00 年静态回收期 ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/investment/yield-spread.html` — 空输入点「计算」→ 结果区 0利差 Spread (bps)0.0000利差 (%)0.000基准收益率 (%)0.000对比收益率 (%) ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/it/json-to-csv.html` — 空输入点「转换」→ 结果区 ⚡ 效率工具栏 ✓ 本地处理 0 个参数 ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/it/vector-cross-product.html` — 空输入点「计算」→ 结果区 A × B = (0, 0, 0) ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/kinematics/angular-displacement.html` — 空输入点「计算」→ 结果区 0.000角位移 θ (rad)0.000末角速度 (rad/s)0.000平均角速度 (rad/s) ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/kinematics/angular-final-velocity.html` — 空输入点「计算」→ 结果区 0.000末角速度 ω (rad/s)0.000角位移 (rad)0.000平均角速度 (rad/s) ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/kinematics/final-velocity-accel.html` — 空输入点「计算」→ 结果区 0.000末速度 v (m/s)0.000v (km/h)0.000位移 s (m)0.000速度增量 (m/s) ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/kinematics/projectile-velocity-components.html` — 空输入点「计算」→ 结果区 0.000水平分量 vₓ (m/s)0.000竖直分量 vᵧ (m/s)0.00合矢量方向 (°)0.0000水平/竖直分量比 vx/vy ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/kinematics/relativistic-velocity-add.html` — 空输入点「计算」→ 结果区 0.000000合成速度 u (c)0.000e+0u (m/s) ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/kinematics/rpm-to-radps.html` — 空输入点「计算」→ 结果区 0.000角速度 ω (rad/s)0.0000转速 (转/秒)0.000角速度 (rad/min)0.0000频率 f (Hz)0.0000角速度平方 (rad²/s²) ⏐ 📋 复制结果⬇️ 导…
- `tools/kinematics/tangential-velocity.html` — 空输入点「计算」→ 结果区 0.000切向速度 v (m/s)0.000切向速度 (km/h)0.0000转速 (转/秒)0.0000角速度复核 (rad/s) ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/kinematics/velocity-squared.html` — 空输入点「计算」→ 结果区 0.000末速度 v (m/s)0.000速度平方增量 v²−v₀²0.000速度增量 Δv (m/s) ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/language/language-toolkit.html` — 空输入点「🔢 字符统计」→ 结果区 0总字符数 0汉字数 0英文字母 0数字数 0标点符号 0空格数 0英文单词数 0句子数
- `tools/language/stats-2.html` — 空输入点「统计字符」→ 结果区 总字符数（含空格）：0不含空格字符数：0汉字数：0英文字母数：0英文单词数：0数字字符数：0标点数：0（中文 0 / 西文 0）空白符：0行数：0 ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/life/countdown.html` — 空输入点「开始倒计时」→ 结果区 ⚡ 效率工具栏 ✓ 本地处理 0 字符 · 0 行 Ctrl/⌘ + Enter 快速运行 ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/livestock/milk-yield-scc.html` — 空输入点「分析趋势」→ 结果区 0.0平均产奶量(kg)0平均SCC(万/ml)0.0最高产奶量(kg)优秀最新SCC等级 ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/logistics/express-freight-calc.html` — 空输入点「计算运费」→ 结果区 计费重量：0.00 kg超首重：0.00 kg（进位计费 0 kg）预计运费：0.00 元 ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/logistics/package-volume-calc.html` — 空输入点「计算」→ 结果区 尺寸体积：0.0 cm³体积（m³）：0.0000材积重：0.00 kg ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/marketing/ad-roi.html` — 空输入点「📣 模拟 ROI」→ 结果区 📋 复制结果⬇️ 导出 TXT ⏐ — 综合 ROI · 利润 0 元 · ROAS 0.00
- `tools/materials/linear-thermal-expansion.html` — 空输入点「计算」→ 结果区 0.000伸长量 ΔL (mm)0.0000热应变 (微应变)0.000000膨胀后长度 (m) ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/materials/rule-of-mixtures.html` — 空输入点「计算」→ 结果区 0.00复合模量 E_c (GPa)0.000e+0E_c (Pa) ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/materials/tensile-force-area.html` — 空输入点「计算」→ 结果区 0.0拉力 F (N)0.00F (kN)0.0000应力复算 (Pa)0.000应力 (MPa) ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/materials/volumetric-strain.html` — 空输入点「计算」→ 结果区 0.00000体积应变 ε_v0.0000体积变化率 (%)0.000000平均正应变 ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/math/arithmetic-series-sum.html` — 空输入点「计算」→ 结果区 0.00前 n 项和 S_n—公差 d0.0000各项平均值 ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/math/determinant-2x2.html` — 空输入点「计算」→ 结果区 0.00行列式 \|A\|0.000迹 tr(A) = a + d奇异矩阵（不可逆）可逆性判定 ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/math/distance-2d.html` — 空输入点「计算」→ 结果区 0.0000距离 d ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/math/dot-product.html` — 空输入点「计算」→ 结果区 0.00点积 A·B ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/math/herons-area.html` — 空输入点「计算」→ 结果区 这三条边不能构成三角形：需满足任意两边之和大于第三边（当前 0、0、0）。 ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/math/law-of-cosines.html` — 空输入点「计算」→ 结果区 0.000边长 c0.000三角形面积 (m²)—角 A (°)—角 B (°) ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/math/modulo-calc.html` — 空输入点「计算」→ 结果区 除数 b 不能为 0（a mod 0 无定义）。 ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/math/quadratic-solver.html` — 空输入点「计算」→ 结果区 恒等式（无穷多解）a = 0 时不是二次方程 ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/mechanical/gear-ratio.html` — 空输入点「计算」→ 结果区 齿数须>0。 ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/mechanical/lever-advantage.html` — 空输入点「计算」→ 结果区 臂长须>0。 ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/mechanical/torque-power.html` — 空输入点「计算」→ 结果区 转速须>0。 ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/metalwork/detector-mold.html` — 空输入点「计算偏差」→ 结果区 测量点：各轴偏差：X轴：+0.000 mm ✓ 合格Y轴：+0.000 mm ✓ 合格Z轴：+0.000 mm ✓ 合格空间偏差：0.0000 mm公差要求：±0.000 mm综合判定：合格该测量点三…
- `tools/meteorology/beaufort-scale.html` — 空输入点「计算」→ 结果区 0 级蒲福风级无风风力名称 ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/meteorology/dafengyingxiangpinggu.html` — 空输入点「🧮 计算」→ 结果区 阵风风力等级0级无风风力较小，无大风影响0.0平均风速 (m/s)0.0阵风风速 (m/s)0.00阵风系数 G0.0阵风差 (m/s)项目风速 (m/s)蒲福等级名称平均风0.00级无风阵风0.00…
- `tools/meteorology/jiaotongqixianganquantishi.html` — 空输入点「🧮 计算」→ 结果区 交通气象综合预警等级特级预警(黑)气象条件极端，立即封闭道路，禁止通行。风险项当前值等级说明能见度0 m特级预警强浓雾(特级)，能见度极低，严禁通行。路面结冰0.0°C黄色预警路面接近冰点(黄色)，注…
- `tools/meteorology/strength-3.html` — 空输入点「🧮 计算」→ 结果区 0%冰雹概率 PH0.0VIL 近似 (kg/m²)0.0降水强度 (mm/h)0水量通量 (m³/s)弱对流/层状云回波顶高：0.0 km（低顶(浅对流)）冰雹概率对流较弱，降水以稳定性为主。 ⏐ …
- `tools/metrology/bias-absolute.html` — 空输入点「计算」→ 结果区 0.000绝对偏倚 Bias0.000相对偏倚 (%)0.00000测量与参考比0.000偏倚绝对值 ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/metrology/dimensional-tolerance.html` — 空输入点「计算」→ 结果区 0.000公差 (mm)0.000最大极限尺寸 (mm)0.000最小极限尺寸 (mm)0.000公差带中心偏差 (mm)0.000公差带中值尺寸 (mm) ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/metrology/flatness-deviation.html` — 空输入点「计算」→ 结果区 0.000平面度误差 (mm)0.0平面度误差 (μm)0.000中位高度 (mm)0.00相对平面度 (ppm) ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/metrology/roundness-deviation.html` — 空输入点「计算」→ 结果区 0.000圆度误差 (mm)0.0圆度误差 (μm)0.000平均半径 (mm)0.00相对圆度 (ppm) ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/metrology/tolerance-stackup-worst.html` — 空输入点「计算」→ 结果区 0.000总公差 (最坏) (mm)0.000平均单环 (mm)0.000统计平方根（RSS）总公差 (mm)0.000极端法与统计法之差 (mm) ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/metrology/uncertainty-propagation-sum.html` — 空输入点「计算」→ 结果区 0.0000合成标准不确定度 u_c ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/mining/convert-grade-ore.html` — 空输入点「换算」→ 结果区 品位需填写 ≥0 的数值（g/t）；矿石量需填写 ≥0 的数值（t）；金属价格需填写 ≥0 的数值（元/g） ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/museum/audio-guide-timer.html` — 空输入点「计算」→ 结果区 0秒讲解总时长 ⏐ 0秒可用时间 ⏐ +0秒时间差 ⏐ 0 秒每件可用时长 ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/nuclear/activity-decay.html` — 空输入点「计算」→ 结果区 0.000活度 A (Bq) ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/nuclear/activity.html` — 空输入点「计算」→ 结果区 0.000e+0活度 A (Bq)0.000e+0A (Ci) ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/nuclear/binding-energy.html` — 空输入点「计算」→ 结果区 0.000e+0结合能 BE (J)0.000BE (MeV) ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/nuclear/dose-equivalent.html` — 空输入点「计算」→ 结果区 0.00剂量当量 H (Sv)0.00吸收剂量 (rad 拉德)0.0剂量当量 (mSv 毫希沃特)0.0剂量当量 (rem 雷姆) ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/nuclear/fission-energy-yield.html` — 空输入点「计算」→ 结果区 0.000e+0总能量 E (J)0.000E (kWh) ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/nuclear/mass-defect.html` — 空输入点「计算」→ 结果区 0.00000质量亏损 Δm (u)0.000对应能量 (MeV) ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/nuclear/nuclear-radius.html` — 空输入点「计算」→ 结果区 0.000核半径 R (fm)0.000核直径 (fm)0.000核体积近似 (fm³)0.000000核子数密度 (个/fm³) ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/nuclear/q-value.html` — 空输入点「计算」→ 结果区 0.0000Q 值 (MeV)吸能反应类型 ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/nutrition/estimate-2.html` — 空输入点「估算摄入量」→ 结果区 0.0g 控盐优秀 钠摄入约 0 mg · 相当于食盐 0.0 g 继续保持低盐饮食，对血压和心血管有益。 ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/nutrition/nutrition-1.html` — 空输入点「🧮 计算」→ 结果区 0% of 0 = 0.00 ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/obstetrics/afi-normal.html` — 空输入点「评估羊水量」→ 结果区 0.0羊水指数AFI(cm)羊水过少评估结果 ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/optical/numerical-aperture.html` — 空输入点「计算」→ 结果区 0.000数值孔径 NA = n·sinθ0.000由 NA 反推半角 (°)0.00000NA 平方0.0000n 与 NA 之比 ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/process/tolerance-rss.html` — 空输入点「计算」→ 结果区 0.000总公差 (RSS)0.000线性叠加总公差0.00RSS 占线性叠加比 (%) ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/process/tolerance-worst-case.html` — 空输入点「计算」→ 结果区 0.000总公差 (最差)0.000统计公差 (RSS)0.000平均单项公差 ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/property/elevator-energy.html` — 空输入点「估算能耗」→ 结果区 0.00 kWh单台日能耗 ⏐ 0.00 kWh全部日能耗 ⏐ 0.0 kWh月能耗 ⏐ 0 kWh年能耗 ⏐ ¥0.00月电费 ⏐ ¥0.00年电费 ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/property/shared-area.html` — 空输入点「核算」→ 结果区 0.00 ㎡套内总面积 ⏐ 0.00 ㎡公摊总面积 ⏐ 0.00 ㎡建筑面积 ⏐ 0.0000公摊系数 ⏐ 0.00 ㎡每户公摊 ⏐ 0.00%得房率 ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/pulmonology/light-criteria.html` — 空输入点「鉴别判读」→ 结果区 0.00蛋白比值0.00LDH比值0胸水LDH(U/L)漏出液积液性质 ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/quantum/bohr-orbit-radius.html` — 空输入点「计算」→ 结果区 0.0000轨道半径 r_n (Å)0.0000r_n (nm) ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/quantum/quantum-oscillator-energy.html` — 空输入点「计算」→ 结果区 0.0000能量 E (eV)0.0000e+0角频率 omega (rad/s)0.0000零点能 (eV) ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/realestate/calc-2.html` — 空输入点「🧮 计算」→ 结果区 年租金收入：0.00 元（月租 0.00 元）毛租金回报率：0.00%净租金回报率：0.00% ⏐ 0.00%毛租金回报率0.00%净租金回报率—静态回本年限 ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/realestate/convert-area-shared.html` — 空输入点「换算」→ 结果区 公摊面积 = 0.00 ㎡ 建筑面积 = 0.00 ㎡ 得房率 = NaN % 参考：多层住宅得房率一般 85% 以上，高层 75% 左右，超高层 70% 左右 ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/reproductive-medicine/baifenbijisuanqi.html` — 空输入点「🧬 计算」→ 结果区 0% of 0 = 0.00 ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/restaurant/menu-pricing.html` — 空输入点「估算售价」→ 结果区 成本合计：0.00 元建议售价：0.00 元建议毛利：0.00 元 ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/robotics/belt-linear-speed.html` — 空输入点「计算」→ 结果区 0.0000带速 v (m/s) ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/robotics/cable-tension-pulley.html` — 空输入点「计算」→ 结果区 0.00绳张力 T (N)0.000机械效益 F/T0.00三绳组单绳张力 (N) ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/robotics/centripetal-speed-limit.html` — 空输入点「计算」→ 结果区 0.000最大速度 v_max (m/s) ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/robotics/dc-motor-back-emf.html` — 空输入点「计算」→ 结果区 0.00反电动势 E (V)0.0转速 (r/min) ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/robotics/forward-kinematics-2r.html` — 空输入点「计算」→ 结果区 0.0000末端 x (m)0.0000末端 y (m) ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/robotics/gear-ratio-torque.html` — 空输入点「计算」→ 结果区 0.00输出扭矩 τ_out (N·m) ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/robotics/lead-screw-speed.html` — 空输入点「计算」→ 结果区 0.00000线速度 v (m/s)0.00v (mm/s) ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/robotics/lifting-torque.html` — 空输入点「计算」→ 结果区 0.000关节转矩 τ (N·m) ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/robotics/linear-accel-force.html` — 空输入点「计算」→ 结果区 0.00驱动力 F (N)0.000驱动力 (kgf)0.0000驱动力 (kN) ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/robotics/motor-power.html` — 空输入点「计算」→ 结果区 0.00机械功率 P (W)0.0转速 (r/min)0.0000机械功率 (hp) ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/robotics/motor-torque-current.html` — 空输入点「计算」→ 结果区 0.0000转矩 τ (N·m)0.0τ (mN·m) ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/robotics/rotational-inertia-torque.html` — 空输入点「计算」→ 结果区 0.00所需扭矩 τ (N·m)0.00角加速度 (°/s²)0.0000所需扭矩 (kgf·m) ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/science/gravitational-potential.html` — 空输入点「计算」→ 结果区 0.0 J重力势能 E_p = mgh0.0000重力势能 (MJ)0.000高度复算 (m) ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/science/kinetic-energy.html` — 空输入点「计算」→ 结果区 0.0 J动能 E_k = ½mv²0.0000速度平方 v² (m²/s²)0.000000动能 (kJ)0.000质量与动能之积 ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/science/mechanical-power.html` — 空输入点「计算」→ 结果区 0 W功率 P = F·v0.000000功率 (kW)0.000000功率 (hp 英制马力)0.0000功率 (kgf·m/s) ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/science/work-done.html` — 空输入点「计算」→ 结果区 0.0 J功 W = F·d·cosθ0.000沿位移分力 (N)0.000垂直分力 (N) ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/securities/calc-1.html` — 空输入点「🧮 计算」→ 结果区 净盈亏：+0.00 元收益率：0.00%买入总成本：0.00 元（金额 0.00 + 佣金 0.00 + 过户费 0.00）卖出净收入：0.00 元（金额 0.00 - 佣金 0.00 - 印花税 0…
- `tools/securities/enterprise-value.html` — 空输入点「计算」→ 结果区 0.00企业价值 EV (万元)0.00净市值（市值 − 现金）0.0000债务/市值 比 ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/securities/market-cap.html` — 空输入点「计算」→ 结果区 0.00总市值 (亿元)0总市值 (元)0总市值 (万元)0.0000股数 (亿股)0.000000总市值 (万亿元) ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/securities/market-risk-premium.html` — 空输入点「计算」→ 结果区 0.00市场风险溢价 (%)0.00市场收益率 (%)0.00无风险利率 (%)0.00溢价与无风险利率之比 (%) ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/securities/option-breakeven-put.html` — 空输入点「计算」→ 结果区 0.00盈亏平衡价 BE (元)0.0000执行价与盈亏平衡价之比0.000权利金占执行价 (%)0.00执行价与权利金之和 ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/service/complaint-analysis.html` — 空输入点「🔍 分析」→ 结果区 暂无数据 ⏐ 暂无数据 ⏐ 0投诉总数0问题类型0未分类0%分类覆盖率 ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/shipping/convert-time-speed.html` — 空输入点「换算」→ 结果区 航程 = 0.00 海里 (≈ 0.00 km) ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/signal/carrier-freq.html` — 空输入点「计算」→ 结果区 0.000载波频率 f_c (kHz)0.000带宽 B (kHz)0.0000上边频与载波比0.000几何中心频率 (kHz) ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/signal/energy-discrete.html` — 空输入点「计算」→ 结果区 0.000信号能量 E0采样点数 N0.0000平均功率 (E/N)0.0000均方根值 RMS ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/signal/pll-lock-range.html` — 空输入点「计算」→ 结果区 0锁定范围 Δf (Hz)0.000Δf (MHz)0.0000e+0锁定范围 (rad/s)0半锁定范围 (Hz) ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/sports/calc-angle-slope.html` — 空输入点「🗺️ 计算」→ 结果区 0% of 0 = 0.00 ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/sports/convert-29.html` — 空输入点「换算」→ 结果区 柔韧指数 = NaN 踢腿点距头顶 = 0.0 cm 测量规范：支撑腿伸直，量地面至踢腿最高点的垂直距离 双腿差异超过 10% 提示不对称，需针对性平衡训练 本指数与坐位体前屈、纵跳共同构成下肢柔韧评…
- `tools/startup/calc-1.html` — 空输入点「🧮 估算」→ 结果区 建议启动资金：0.00 元其中一次性投入 0.00 元，运营资金 0.00 元，应急储备 0.00 元月运营成本：0.00 元，按此标准资金可支撑约 0.0 个月 ⏐ 0.00建议启动资金（元）0.0…
- `tools/statistics/iqr.html` — 空输入点「计算」→ 结果区 IQR：0.0000 异常值下限：0.0000 异常值上限：0.0000 中位数：0.0000 ⏐ 📋 复制结果⬇️ 导出 TXT
- …… 其余 46 页见 JSON

### 空输入直接给出结论（优秀/正常/合格…）（56 页）

- `tools/accounting/assessor-risk-11.html` — 空输入点「评估风险」→ 结果区 Altman Z-Score破产风险模型X1(流动资产/总资产)：0X2(留存收益/总资产)：0X3(EBIT/总资产)：0X4(权益市值/负债)：0X5(销售/总资产)：0Z-Score：0.000…
- `tools/aerospace/weight-balance.html` — 空输入点「计算重心」→ 结果区 载荷项重量 (kg)力臂 (m)力矩 (kg·m)使用空机00.000未命名00.000未命名00.000未命名00.000未命名00.000未命名00.000 0 总重量 (kg) 0 总力矩 (k…
- `tools/agriculture/detector-nutrition.html` — 空输入点「判读品质」→ 结果区 综合等级：不合格 优质 2 / 合格 2 / 共 6 项发酵度评价：发酵不足（乳酸 0%）指标实测判读蛋白质0%偏低脂肪0%偏低还原糖0%偏低水分0%优质灰分0%优质乳酸(发酵度)0%偏低品质解读：多…
- `tools/agriculture/irrigation-uniformity.html` — 空输入点「计算」→ 结果区 0.0%克里斯琴森系数CU0.0%分布均匀度DU0.00平均灌水量(mm)0.0%变异系数CV均匀度评价：均匀性差CU参考标准：>90%优秀 \| 80-90%良好 \| 70-80%一般 \| <70%差…
- `tools/automotive/voltage-1.html` — 空输入点「🧮 计算」→ 结果区 38.0用电总电流 (A)38.0含充电总电流 (A)0负载率 (%)-38.0剩余电流 (A)0.55用电功率 (kW)0.00发电机功率 (kW)负载充足平衡评估负载率: 0.0%（安全线 80%…
- `tools/beauty/recommender-face-shape.html` — 空输入点「生成」→ 结果区 生成结果： 1. 椭圆形脸 推荐发型：中长发、波浪卷、空气刘海 妆容建议：标准脸，眉形自然，唇妆可随心尝试 注意：公认理想脸型，多数发型都适合 2. 长形脸 推荐发型：法式刘海、齐肩发、横向蓬松卷发 …
- `tools/biz/checker-8.html` — 空输入点「质量评估」→ 结果区 8服务质量总分服务质量不合格质量等级评估维度权重得分明细状态人员标准25%0持证0%/培训0%/着装0%/出勤0%差服务流程30%25巡逻0%/门禁0%/响应0分钟/记录0%差装备设施20%0监控0%…
- `tools/biz/presentation-timer.html` — 空输入点「开始演讲」→ 结果区 进度正常
- `tools/clinical-lab/thyroid-function-model.html` — 空输入点「分析」→ 结果区 结果分析参考区间定位TSH 2 mIU/L → 落在 正常（0.27–4.2 mIU/L 正常）FT3 5 pmol/L → 落在 正常（3.1–6.8 pmol/L 正常）FT4 16 pmol/L…
- `tools/decor/detector-18.html` — 空输入点「检测判定」→ 结果区 室内空气质量检测结果（GB/T 18883-2022）污染物实测值限值判定甲醛0 mg/m³≤0.08✓ 达标 (0%)TVOC0 mg/m³≤0.6✓ 达标 (0%)苯0 mg/m³≤0.03✓ 达…
- `tools/eco/aqi.html` — 空输入点「计算」→ 结果区 健康等级：1 级建议活动时长：0.0 小时PM2.5 估算：0.0 µg/m³ ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/eco/noise-superposition.html` — 空输入点「计算叠加」→ 结果区 叠加后总声压级3.0 dB安静声源数量2最大声源0.0 dB能量平均0.0 dB较最大声源增加+3.0 dB距离衰减参考（点声源，距最大声源）：1m0.0 dB5m-14.0 dB10m-20.0 d…
- `tools/edu/assessor-27.html` — 空输入点「知识评估」→ 结果区 知识管理成熟度评估知识捕获：0/10 ✗知识共享：0/10 ✗知识应用：0/10 ✗知识创新：0/10 ✗知识存储：0/10 ✗知识安全：0/10 ✗综合评分：0.00/10成熟度等级：1级-初始级知…
- `tools/electronics/bandwidth.html` — 空输入点「🧮 计算」→ 结果区 0.00e+0所需 GBP (Hz)0.00e+0建议 GBP (Hz)0.00e+0-3dB带宽 (Hz)推荐运放：LM358 / NE5532 (1~10MHz)。建议选型裕量≥2倍，高频应用还需…
- `tools/electronics/capacitance.html` — 空输入点「🧮 计算」→ 结果区 0.00匹配电容 (pF)8推荐标准值 (pF)0.0晶振CL (pF)0.0杂散电容 (pF)C1=C2=C=2×(CL−Cs)。推荐就近选取标准容值8pF，C1与C2各接一个。 ⏐ 匹配电容26.…
- `tools/encode/encode-7.html` — 空输入点「计算」→ 结果区 空间大小：1 近似碰撞概率：0.000000 %安全阈值 n：1 ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/endocrinology/detector-metabolism.html` — 空输入点「分析判读」→ 结果区 儿茶酚胺及代谢产物检测结果项目实测参考范围判定24h尿VMA0 mg/24h1-7↓ 偏低24h尿HVA0 mg/24h1-4↓ 偏低血去甲肾上腺素0 pg/mL80-520↓ 偏低血肾上腺素0 pg…
- `tools/energy/air-purifier-area.html` — 空输入点「计算」→ 结果区 0最小面积 m²0推荐面积 m²0最大面积 m²0.0换气次数/小时 ⏐ 📋 复制结果⬇️ 导出 TXT ⏐ 📊 结果解读 估算口径适用面积常按 CADR（洁净空气量）× 系数估算：卧室约 CAD…
- `tools/energy/water-tds-evaluator.html` — 空输入点「评估」→ 结果区 直饮水级🎯 适用场景直饮无需处理高端饮用纯净水实验室超纯水稀释💡 健康提示水质极优，口感清冽。TDS极低可能意味着缺乏有益矿物质，长期饮用纯净水建议适当补充矿物质。🌍 WHO标准对比完全符合WH…
- `tools/ent/ahi-severity.html` — 空输入点「计算评估」→ 结果区 0AHI(次/h)0AI暂停指数0HI低通气指数0ODI氧减指数0微觉醒指数100%正常 ⏐ 📋 复制结果⬇️ 导出 TXT ⏐ 参考区间标尺正常00.20.40.60.810
- `tools/ent/hearing-loss-classification.html` — 空输入点「计算分析」→ 结果区 0PTA气导(dB)0PTA骨导(dB)0气骨导差(dB)0高频平均(dB) ⏐ 📋 复制结果⬇️ 导出 TXT ⏐ 参考区间标尺正常00.20.40.60.810
- `tools/ent/laryngeal-nerve.html` — 空输入点「分析评估」→ 结果区 F0 基频0 Hz异常 ⏐ Jitter 微扰0%正常 ⏐ Shimmer 振幅微扰0%正常 ⏐ NHR 噪谐比0正常 ⏐ HNR 谐噪比0 dB异常 ⏐ MPT 最长发声0 秒异常 ⏐ 📋 复制结…
- `tools/fitness/ratio-19.html` — 空输入点「🧮 计算」→ 结果区 100.0综合对称评分优秀对称等级0差异>10%部位数部位左 (cm)右 (cm)差异差异%对称分上臂0.00.00.0 cm 0.00%100.0大腿0.00.00.0 cm 0.00%100.0小…
- `tools/fitness/weight-capacity-training.html` — 空输入点「🧮 计算」→ 结果区 0.0 kg训练总容量0.0 kg估算 1RM0.0%强度百分比0总次数强度区间：低强度 （推荐次数 25+）极低强度，适合热身与康复。相对 1RM 强度 0.0%（相对容量系数 -）1RM 百分比建…
- `tools/gardening/recommender.html` — 空输入点「生成」→ 结果区 浇水频次推荐：1. 月季 \| 春季·多云·疏松透气 → 建议每周1次，见干见湿，浇则浇透2. 兰花 \| 冬季·晴天·保水性强 → 建议每10-14天1次，忌积水，植料偏干后再浇3. 月季 \| 冬季·晴…
- `tools/general/recommender-24.html` — 空输入点「生成」→ 结果区 替代产品/方案推荐：1. Docker Desktop → 替代：Podman、Rancher Desktop、Colima2. Zoom → 替代：Jitsi Meet、BigBlueButton、…
- `tools/healthcare/checker-manager.html` — 空输入点「执行GSP检查」→ 结果区 📋 GSP质量管理检查报告检查维度评分判定说明质量管理体系与文件0/10需整改质量管理制度、操作规程、记录文件、内审人员与培训管理0/10需整改执业药师配备、岗前培训、年度继续教育设施与设备管理0/…
- `tools/healthcare/water-intake.html` — 空输入点「计算」→ 结果区 推荐饮水量：0 mL折合杯数(250mL)：0.0 杯 ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/hr/assessor-training-hr.html` — 空输入点「评估培训效果」→ 结果区 培训效果评估（柯氏前两层）培训主题：参训：0人 \| 时长：0小时能力提升：0→0（+0.0，提升0.0%）L1反应层（满意度）：0/100L2学习层-知识（测试通过率）：0/100L2学习层-技能（能…
- `tools/hr/attendance-stats.html` — 空输入点「📊 统计」→ 结果区 4员工数0 次迟到合计0 次早退合计0 天旷工合计0 天请假合计0 小时加班合计0 元扣款合计4 人全勤人数0 元全勤奖合计0 元加班费合计 ⏐ 📋 复制结果⬇️ 导出 TXT ⏐ 姓名迟到早退旷工…
- `tools/hvac/supply-air.html` — 空输入点「计算」→ 结果区 冷负荷 2,500 W，送风温差 8.0 °C → 送风量 933 m³/h，换气次数 7.8 次/h，推荐送风口 2 个。 ⏐ 📋 复制结果⬇️ 导出 TXT ⏐ 📊 计算结果 933送风量 L…
- `tools/hydraulic/dam-stability.html` — 空输入点「🧮 计算」→ 结果区 坝体自重 W：21189.60 kN水平水压力 P：11301.12 kN（作用点 h/3=16.00 m）扬压力 U：4237.92 kN（折减系数 α=0.5）抗滑稳定安全系数 Ks：0.975 …
- `tools/insurance/pure-premium.html` — 空输入点「计算」→ 结果区 0.00纯保费 (元/单位)0.00含10%安全边际 (元) ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/leather/temp-9.html` — 空输入点「🧮 计算」→ 结果区 0.00%收缩率0.0收缩温度 (℃)优秀热稳定性评估：收缩率＜3%，热稳定性优异。收缩温度偏低，需加强鞣制。 ⏐ 收缩率10.00% → 较差 ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/leather/time-34.html` — 空输入点「🧮 计算」→ 结果区 0推荐软化时间 (min)0基准时间 (min)2.92温度系数1.00活力系数操作建议：温度偏低，酶活性不足，建议升温至37~40℃。软化过度会损伤皮纤维，须密切监控。 ⏐ 软化时间31min ⏐ …
- `tools/leather/yield-rate-1.html` — 空输入点「🧮 计算」→ 结果区 0.00%铬回收率0.000回收铬量 (kg)较差处理效果回收率 = (废液浓度−回收后浓度) ÷ 废液浓度 × 100%。回收铬量 = 浓度差 × 处理量 ÷ 10⁶ (kg)。 ⏐ 回收率85.0…
- `tools/leather/yield-rate.html` — 空输入点「🧮 计算」→ 结果区 0.00%铬吸收率0.000铬吸收量 (kg)0.0液量 (L)较差利用率吸收率 = (初始−废液) ÷ 初始 × 100%。提高吸收率可降低废液铬污染，常用提碱、升温等手段。 ⏐ 吸收率84.0% …
- `tools/life/generator-price.html` — 空输入点「生成」→ 结果区 生成结果： 1. 《设备维修合同》草案 合同编号：HT-6683-7869 第一条 服务内容 乙方为甲方提供设备维修服务，具体需求以双方确认的《需求确认单》为准。 第二条 合同金额 本合同总金额为人民…
- `tools/life/recommender-8.html` — 空输入点「生成」→ 结果区 生成结果： 1. 家庭财产 场景 推荐险种：水管爆裂险 建议保额：198 万元 \| 年保费参考：5680 元 选购要点：留意保障地域范围 2. 个人意外 场景 推荐险种：交通意外险 建议保额：89 万…
- `tools/manufacturing/production-efficiency.html` — 空输入点「⚡ 计算 OEE」→ 结果区 可用率 (Availability) ⏐ 87.5% ⏐ 性能率 (Performance) ⏐ 59.5% ⏐ 合格率 (Quality) ⏐ 95.0% ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/meteorology/risk-14.html` — 空输入点「🧮 计算」→ 结果区 综合气象健康风险指数71中高风险气象要素当前值偏离度风险贡献温度0.0°C79%27.5湿度0%92%18.3风速0.0m/s0%0.0气压0hPa100%25.0气象条件较差，老人儿童及慢性病患者减…
- `tools/mining/checker-training-hr.html` — 空输入点「执行安全评估」→ 结果区 📋 矿山安全体系评估报告检查项目实测值判定回风巷瓦斯浓度0% (限值≤1.0%)达标通风量满足度0.00倍需求 (≥1.0)不达标安全设备完好率0% (≥95%)不达标安全培训完成0% / 0学时 …
- `tools/museum/exhibit-spacing.html` — 空输入点「计算」→ 结果区 559.8 cm最佳观看距离 ⏐ 0.0 cm最小观看距离 ⏐ 48.0 cm推荐展品间距 ⏐ 2 幅/m每米布展数 ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/nephrology/vascular-calcification.html` — 空输入点「评分」→ 结果区 0Kauppila总分 (0-24)无钙化钙化分级无钙化（总分0分）腹主动脉未见明显钙化，血管钙化风险低。建议定期复查(每年)，控制传统心血管危险因素。各节段评分明细节段前壁后壁小计L1000/6L2…
- `tools/optical/recommender-1.html` — 空输入点「生成」→ 结果区 驾驶镜（偏振+UV）推荐方案：1. 琥珀色偏光驾驶镜（强光雪地）核心功能：抗冲击材质、防油污镀膜；紫外线防护：UV3802. 灰色偏光驾驶镜（阴雨天气）核心功能：防雾涂层、UV400全防护；紫外线防护…
- `tools/optical/recommender-11.html` — 空输入点「生成」→ 结果区 镜架（材质/风格/适配）推荐：1. 轻量无框镜架 — β钛适配脸型：椭圆脸；舒适设计：镜腿防滑套、轻量前框2. 商务经典镜架 — TR90超轻适配脸型：圆脸；舒适设计：加宽镜腿、轻量前框3. 潮流眉线…
- `tools/rental/recommender-5.html` — 空输入点「生成」→ 结果区 网络（宽带/安装）推荐：1. 智能家居多设备 — 推荐200M 光纤到户（FTTH）安装建议：优先选择光纤到户，延迟更低2. 单人租房办公 — 推荐1000M 5G无线宽带安装建议：租房短期可选月付/…
- `tools/reproductive-medicine/sperm-dfi.html` — 空输入点「评估」→ 结果区 0%DFI0%HDS优秀分级 ⏐ 📋 复制结果⬇️ 导出 TXT ⏐ 📊 结果解读 分级参考精子 DNA 碎片指数（DFI）：<30% 通常视为正常；30%–50% 临界/偏高；>50% 高碎片，…
- `tools/safety/generator-21.html` — 空输入点「生成」→ 结果区 急救包物品清单（按场景）：1. 创可贴 — 日常割伤、擦伤备注：多种尺寸各若干2. 无菌纱布 — 包扎较大伤口备注：配合医用胶带使用3. 体温计 — 监测体温备注：电子体温计更安全4. 医用胶带 — …
- `tools/safety/generator-hazard.html` — 空输入点「生成」→ 结果区 隐患排查清单与闭环：1. 压力容器超期未检（风险等级：高）整改建议：立即停用，联系有资质机构检验，更新台账。闭环状态：待整改2. 配电箱未上锁（风险等级：中）整改建议：加装锁具，张贴警示标签，指定专人…
- `tools/safety/random-13.html` — 空输入点「生成」→ 结果区 防诈骗知识卡片：1. 游戏账号交易常见套路：私下交易后被拉黑，或收到虚假付款截图。防范要点：通过正规平台交易，不要脱离平台担保。2. 冒充公检法常见套路：声称涉嫌洗钱，要求资金转入“安全账户”。防范要…
- `tools/seismology/generator-drill.html` — 空输入点「生成」→ 结果区 应急预案（生成/演练）：1. 地震应急疏散预案（办公楼、学校等人员密集场所）关键步骤：就近躲避→保护头部→听从指挥→有序撤离→清点人数→集合汇报演练周期：每半年演练1次2. 户外地震避险预案（山区、河…
- `tools/tax/calc-8.html` — 空输入点「🧮 计算」→ 结果区 ① 单独计税推荐省税¥0年终奖应纳税额（全年合计应纳税 ¥0）年终奖 ÷ 12 = ¥0 → 适用税率 3%，速算扣除数 ¥0应纳税额 = ¥0 × 3% − ¥0 = ¥0② 并入综合所得¥0并入后…
- `tools/textile/strength-color-diff.html` — 空输入点「🧮 计算」→ 结果区 0.00色差 ΔE5灰卡色牢度等级0.00明度差 ΔL0.00红绿差 Δa0.00黄蓝差 Δb0.00饱和度差 ΔC0.00色相差 ΔH合格判定（阈值0） ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/travel/recommender-10.html` — 空输入点「生成」→ 结果区 生成结果：1. 武汉 · 特色：热干面 · 分布：户部巷、吉庆街 · 推荐：蔡林记 · 芝麻酱拌面，配蛋酒或豆浆2. 昆明 · 特色：过桥米线 · 分布：南屏街、文化巷 · 推荐：建新园 · 高汤烫熟…
- `tools/travel/recommender-9.html` — 空输入点「生成」→ 结果区 生成结果：1. 大理古城 · 住宿类型：白族庭院/设计师民宿 · 推荐区域：人民路、洱海门、才村 · 预订建议：洱海生态廊道周边安静，古城内夜生活丰富，按需求选址 · 评价维度：洱海/民谣/慢节奏2.…

## 三、死控件与辅助按钮

### 改了输入再点主按钮，输出快照不变（低置信度线索，需人工复验）（48 页）

- `tools/pr/risk-assessment.html` — 按钮「📋 评估」｜构造值 riskProb [number] "3" → "2.4000000000000004"｜改前 0风险总数0低风险0中风险0高/极高 ⏐ 📋 复制结果⬇️ 导出 TXT → 点击后 0风险总数0低风险0中风险0高/极高 ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/agriculture/countdown-4.html` — 按钮「开始孵化」｜构造值 batchName [text] "abc 123" → "abc 123x"｜改前 📖 查看「鸡蛋孵化倒计时（21天）使用指南」 📅 鸡蛋孵化倒计时（21天） ⚠️ 专业工具免责声明 本工具结果为本页… → 点击后 📖 查看「鸡蛋孵化倒计时（21天）使用指南」 📅 鸡蛋孵化倒计时（21天） ⚠️ 专业工具免责声明 本工具结果为本页…
- `tools/cardiology/calc-1.html` — 按钮「评估分级」｜构造值 sbp [number] "175" → "140"｜改前 血压分级：2级高血压 收缩压 ≥160 或 舒张压 ≥100 mmHg 心血管风险分层：中危 2级高血压且无其他危险因素… → 点击后 血压分级：2级高血压 收缩压 ≥160 或 舒张压 ≥100 mmHg 心血管风险分层：中危 2级高血压且无其他危险因素…
- `tools/data/pivot-table.html` — 按钮「📊 生成」｜构造值 inputData [textarea] "abc 123" → "probe-a\nprobe-b\nprob"｜改前 🔄 透视表 (sum) 地区 \ 产品 AB 合计 华北 210150 360 华东 200340 540 华南 12… → 点击后 🔄 透视表 (sum) 地区 \ 产品 AB 合计 华北 210150 360 华东 200340 540 华南 12…
- `tools/dermatology/leprosy-grading.html` — 按钮「生成分级报告」｜构造值 leprosyType [select] "TT" → "BT"｜改前 G0D0级残疾无感觉丧失和可见畸形 ⏐ 📋 复制结果⬇️ 导出 TXT → 点击后 G0D0级残疾无感觉丧失和可见畸形 ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/design/flexbox-generator.html` — 按钮「计算」｜构造值 gap [number] "12" → "9.600000000000001"｜改前 生成的 CSS ⏐ 实时预览（3 个项目） ⏐ 📋 复制结果⬇️ 导出 TXT → 点击后 生成的 CSS ⏐ 实时预览（3 个项目） ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/design/mesh-gradient.html` — 按钮「生成」｜构造值 overlay [text] "abc 123" → "abc 123x"｜改前 background-color: #000000; background-image: radial-gradient… → 点击后 background-color: #000000; background-image: radial-gradient…
- `tools/electromagnetism/free-space-impedance.html` — 按钮「计算」｜构造值 x [number] "0" → "1"｜改前 376.73波阻抗 Z₀ (Ω)2.997925真空光速 (×10⁸ m/s)1.256637真空磁导率 μ₀ (μH/… → 点击后 376.73波阻抗 Z₀ (Ω)2.997925真空光速 (×10⁸ m/s)1.256637真空磁导率 μ₀ (μH/…
- `tools/endocrinology/pcos-diagnosis.html` — 按钮「诊断评估」｜构造值 cycle [number] "45" → "36"｜改前 满足① 排卵障碍满足② 高雄激素满足③ 多囊形态 ⏐ 📋 复制结果⬇️ 导出 TXT → 点击后 满足① 排卵障碍满足② 高雄激素满足③ 多囊形态 ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/food-processing/fermentation-brix.html` — 按钮「计算」｜构造值 vol [number] "100" → "80"｜改前 0g糖消耗量0.00%酒精度 ABV0g酒精生成量0gCO₂生成量 ⏐ 📋 复制结果⬇️ 导出 TXT → 点击后 0g糖消耗量0.00%酒精度 ABV0g酒精生成量0gCO₂生成量 ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/food-processing/ph-adjustment.html` — 按钮「计算」｜构造值 vol [number] "0.001" → "0.001"｜改前 0.00mL需加溶液量0.000g纯物质量0.0000mol物质的量pH 无变化调节方向 ⏐ 📋 复制结果⬇️ 导出 … → 点击后 0.00mL需加溶液量0.000g纯物质量0.0000mol物质的量pH 无变化调节方向 ⏐ 📋 复制结果⬇️ 导出 …
- `tools/forensic-medicine/electrocution-injury.html` — 按钮「分析电击伤」｜构造值 currentType [select] "ac" → "dc"｜改前 0阳性特征数0%特征符合度 ⏐ 📋 复制结果⬇️ 导出 TXT → 点击后 0阳性特征数0%特征符合度 ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/forensic-medicine/rigor-mortis.html` — 按钮「评估死后时间」｜构造值 envTemp [select] "low" → "normal"｜改前 2.0平均僵硬度2.0上部关节2.0下部关节 ⏐ 📋 复制结果⬇️ 导出 TXT → 点击后 2.0平均僵硬度2.0上部关节2.0下部关节 ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/funeral/memorial-date.html` — 按钮「计算」｜构造值 memTitle [text] "abc 123" → "abc 123x"｜改前 • 头七：逝后第 7 天 • 三七 / 五七：逝后第 21 / 35 天 • 百日：逝后第 100 天 • 周年：逝后满… → 点击后 • 头七：逝后第 7 天 • 三七 / 五七：逝后第 21 / 35 天 • 百日：逝后第 100 天 • 周年：逝后满…
- `tools/gardening/plant-calendar.html` — 按钮「📅 月份视图」｜构造值 search [text] "abc 123" → "abc 123x"｜改前 📖 查看「蔬菜种植时间历使用指南」 📅 蔬菜种植日历 按月份/季节/类别查看蔬菜种植时间，含播种、移栽、收获、生长期… → 点击后 📖 查看「蔬菜种植时间历使用指南」 📅 蔬菜种植日历 按月份/季节/类别查看蔬菜种植时间，含播种、移栽、收获、生长期…
- `tools/hematology/itp-risk-score.html` — 按钮「评分」｜构造值 drug [select] "heparin" → "quinine"｜改前 9总分 (满分8)确定 (Definite)因果关系等级 ⏐ 📋 复制结果⬇️ 导出 TXT ⏐ 参考区间标尺不太可能… → 点击后 9总分 (满分8)确定 (Definite)因果关系等级 ⏐ 📋 复制结果⬇️ 导出 TXT ⏐ 参考区间标尺不太可能…
- `tools/hematology/mm-staging.html` — 按钮「分期」｜构造值 albumin [number] "35" → "28"｜改前 R-ISS III分期ISS 3ISS分期43个月中位OS ⏐ 📋 复制结果⬇️ 导出 TXT → 点击后 R-ISS III分期ISS 3ISS分期43个月中位OS ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/image/image-compress.html` — 按钮「压缩质量80·输出格式webp·最大尺寸（等比缩放）1920」｜构造值 fmt [select] "webp" → "jpeg"｜改前 ⚡ 效率工具栏 ✓ 本地处理 1 个文件入口 ⏐ 📋 复制结果⬇️ 导出 TXT → 点击后 ⚡ 效率工具栏 ✓ 本地处理 1 个文件入口 ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/image/wechat-cover-maker.html` — 按钮「生成」｜构造值 title [text] "abc 123" → "abc 123x"｜改前 ✨ 公众号封面生成器 纯前端生成 900×383 封面图：标题 + 副标题 + 背景渐变 + 下载。 标题 副标题 背景… → 点击后 ✨ 公众号封面生成器 纯前端生成 900×383 封面图：标题 + 副标题 + 背景渐变 + 下载。 标题 副标题 背景…
- `tools/it/ast-viewer.html` — 按钮「解析 AST」｜构造值 codeInput [textarea] "abc 123" → "probe-a\nprobe-b\nprob"｜改前 ⬇️ 导出统计 CSV ⏐ 0 ⏐ 0 ⏐ 0 ⏐ 0 → 点击后 ⬇️ 导出统计 CSV ⏐ 0 ⏐ 0 ⏐ 0 ⏐ 0
- `tools/it/docker-run-converter.html` — 按钮「计算」｜构造值 cmd [textarea] "abc 123" → "probe-a\nprobe-b\nprob"｜改前 docker-compose.yml ⏐ 📋 复制结果⬇️ 导出 TXT → 点击后 docker-compose.yml ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/it/dockerfile-generator.html` — 按钮「计算」｜构造值 port [number] "3000" → "2400"｜改前 Dockerfile ⏐ 📋 复制结果⬇️ 导出 TXT → 点击后 Dockerfile ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/it/hill-cipher.html` — 按钮「加密 ↑」｜构造值 key [text] "abc 123" → "abc 123x"｜改前 密钥矩阵3325行列式9 mod 26行列式逆元3逆矩阵1517209 ⏐ 📋 复制结果⬇️ 导出 TXT → 点击后 密钥矩阵3325行列式9 mod 26行列式逆元3逆矩阵1517209 ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/it/html-nesting-checker.html` — 按钮「检查」｜构造值 html [textarea] "<div><p>hi</p></div>" → "<div><span>x</span…｜改前 ✅ HTML 嵌套结构合法（无未闭合/错误嵌套标签） ⏐ 📋 复制结果⬇️ 导出 TXT ⏐ 📊 结果解读 结果含义… → 点击后 ✅ HTML 嵌套结构合法（无未闭合/错误嵌套标签） ⏐ 📋 复制结果⬇️ 导出 TXT ⏐ 📊 结果解读 结果含义…
- `tools/it/json-to-tsv.html` — 按钮「转换 →」｜构造值 jsonInput [textarea] "{\"a\":1}" → "{\"a\":2}"｜改前 行数：2 列数：3 字符数：31 ⏐ name age city 张三 30 上海 李四 25 北京 → 点击后 行数：2 列数：3 字符数：31 ⏐ name age city 张三 30 上海 李四 25 北京
- `tools/it/password-generator.html` — 按钮「🎲 生成」｜构造值 length [number] "66" → "52.800000000000004"｜改前 16+ 推荐长度 4种 字符类型 90天 更换周期 2FA 双重验证 ⏐ ⚡ 效率工具栏 ✓ 本地处理 13 个参数 C… → 点击后 16+ 推荐长度 4种 字符类型 90天 更换周期 2FA 双重验证 ⏐ ⚡ 效率工具栏 ✓ 本地处理 13 个参数 C…
- `tools/it/protobuf-parser.html` — 按钮「解析」｜构造值 input [textarea] "abc 123" → "probe-a\nprobe-b\nprob"｜改前 { "syntax": "", "package": "", "imports": [], "options": [],… → 点击后 { "syntax": "", "package": "", "imports": [], "options": [],…
- `tools/it/sitemap-generator.html` — 按钮「计算」｜构造值 urls [textarea] "https://example.com/" → "https://example.co…｜改前 sitemap.xml ⏐ 📋 复制结果⬇️ 导出 TXT → 点击后 sitemap.xml ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/it/toml-formatter.html` — 按钮「格式化」｜构造值 input [textarea] "abc 123" → "probe-a\nprobe-b\nprob"｜改前 title = "toolbox" port = 8080 replicas = 3 ⏐ 📋 复制结果⬇️ 导出 TX… → 点击后 title = "toolbox" port = 8080 replicas = 3 ⏐ 📋 复制结果⬇️ 导出 TX…
- `tools/it/uuid-v5-generator.html` — 按钮「生成」｜构造值 ns [text] "abc 123" → "abc 123x"｜改前 example.com → cfbff0d1-9375-5685-968c-48ce8b15ae17example.or… → 点击后 example.com → cfbff0d1-9375-5685-968c-48ce8b15ae17example.or…
- `tools/life/chinese-number.html` — 按钮「转换」｜构造值 inputVal [text] "abc 123" → "abc 123x"｜改前 无法识别输入 ⏐ 简体：〇 一 二 三 四 五 六 七 八 九 十 百 千 万 亿 大写：零 壹 贰 叁 肆 伍 陆 柒… → 点击后 无法识别输入 ⏐ 简体：〇 一 二 三 四 五 六 七 八 九 十 百 千 万 亿 大写：零 壹 贰 叁 肆 伍 陆 柒…
- `tools/life/unit-converter.html` — 按钮「▶ 运行」｜构造值 fromValue [number] "1" → "0.8"｜改前 • 选择分类后，在左侧输入数值即可实时换算到右侧单位 • 点击中间 ⇅ 按钮可交换两个单位 • 常用换算速查可一键填入常… → 点击后 • 选择分类后，在左侧输入数值即可实时换算到右侧单位 • 点击中间 ⇅ 按钮可交换两个单位 • 常用换算速查可一键填入常…
- `tools/metallurgy/alloy-ratio.html` — 按钮「计算加入量」｜构造值 steelW [number] "0.01" → "0.01"｜改前 总原料加入量 0.000 t ⏐ 📋 复制结果⬇️ 导出 TXT → 点击后 总原料加入量 0.000 t ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/music/chord-notes.html` — 按钮「🔍 分析和弦」｜构造值 chordInput [text] "abc 123" → "abc 123x"｜改前 和弦类型标记示例音程（半音）结构 大三和弦C0, 4, 7根-大三-纯五 小三和弦Am0, 3, 7根-小三-纯五 增三… → 点击后 和弦类型标记示例音程（半音）结构 大三和弦C0, 4, 7根-大三-纯五 小三和弦Am0, 3, 7根-小三-纯五 增三…
- `tools/music/music-analysis.html` — 按钮「🎤 开始分析」｜构造值 sample-rate [number] "12" → "9.600000000000001"｜改前 码率: 1411 kbps 每秒: 172.27 KB/s 60秒总大小: 10.09 MB 每小时: 605.62 M… → 点击后 码率: 1411 kbps 每秒: 172.27 KB/s 60秒总大小: 10.09 MB 每小时: 605.62 M…
- `tools/nuclear/pair-annihilation.html` — 按钮「计算」｜构造值 dummy [number] "1" → "0.8"｜改前 511.0每个光子能量 (keV)1022.0总能量 (keV)0.5110每个光子能量 (MeV)1.0220总能量 … → 点击后 511.0每个光子能量 (keV)1022.0总能量 (keV)0.5110每个光子能量 (MeV)1.0220总能量 …
- `tools/pet/fish-tank-volume.html` — 按钮「计算水量」｜构造值 length [number] "2" → "1.6"｜改前 • 过滤器：流量建议为水量的3-5倍/小时 • 加热棒：每升水约需1-2W加热功率 • 增氧泵：小型缸2-5W，大型缸5… → 点击后 • 过滤器：流量建议为水量的3-5倍/小时 • 加热棒：每升水约需1-2W加热功率 • 增氧泵：小型缸2-5W，大型缸5…
- `tools/rental/cycle-11.html` — 按钮「计算结算」｜构造值 number [number] "260" → "208"｜改前 ⏱️ 水电（读数/周期）结算 记录电表、水表、燃气表读数，自动计算用量与费用，支持阶梯电价，生成结算报告。 📐 工作原… → 点击后 ⏱️ 水电（读数/周期）结算 记录电表、水表、燃气表读数，自动计算用量与费用，支持阶梯电价，生成结算报告。 📐 工作原…
- `tools/rheumatology/sapho-syndrome.html` — 按钮「评估诊断」｜构造值 duration [number] "3" → "2.4000000000000004"｜改前 高度提示SAPHO综合征诊断评估中等活动疾病活动度7诊断评分 ⏐ 📋 复制结果⬇️ 导出 TXT → 点击后 高度提示SAPHO综合征诊断评估中等活动疾病活动度7诊断评分 ⏐ 📋 复制结果⬇️ 导出 TXT
- `tools/safety/haxijisuan.html` — 按钮「🔐 计算」｜构造值 input [textarea] "abc 123" → "probe-a\nprobe-b\nprob"｜改前 ❌ Failed to execute 'digest' on 'SubtleCrypto': Algorithm: U… → 点击后 ❌ Failed to execute 'digest' on 'SubtleCrypto': Algorithm: U…
- `tools/sales/moving-average.html` — 按钮「🔮 预测」｜构造值 window [number] "11" → "8.8"｜改前 📋 复制结果⬇️ 导出 TXT ⏐ 期数实际值移动平均/预测第3期128128第4期142135第5期150140第6… → 点击后 📋 复制结果⬇️ 导出 TXT ⏐ 期数实际值移动平均/预测第3期128128第4期142135第5期150140第6…
- `tools/science/periodic-table.html` — 按钮「搜索 Fe」｜构造值 search [text] "Fe" → "Fex"｜改前 H氢 Hydrogen原子序数 1 · 第1周期 · 第1族 · 非金属原子量1.008电子排布1s¹密度0.0899 … → 点击后 H氢 Hydrogen原子序数 1 · 第1周期 · 第1族 · 非金属原子量1.008电子排布1s¹密度0.0899 …
- `tools/sports/sports-stats.html` — 按钮「跑步周」｜构造值 aMinutes [number] "2" → "1.6"｜改前 2总记录数 ⏐ 720总消耗 kcal ⏐ 70总时长 分钟 ⏐ 12.0总距离 km ⏐ 日期类型时长(min)距离(… → 点击后 2总记录数 ⏐ 720总消耗 kcal ⏐ 70总时长 分钟 ⏐ 12.0总距离 km ⏐ 日期类型时长(min)距离(…
- `tools/stats/regression-analysis.html` — 按钮「🧮 计算」｜构造值 pred-x [number] "11" → "8.8"｜改前 样本数 n10斜率 b1.9867截距 a0.0733相关系数 r0.9994决定系数 R²0.9989剩余标准差 s0… → 点击后 样本数 n10斜率 b1.9867截距 a0.0733相关系数 r0.9994决定系数 R²0.9989剩余标准差 s0…
- `tools/stats/statistical-tests.html` — 按钮「🧮 检验」｜构造值 one-mu [number] "20" → "16"｜改前 样本数 n10样本均值 x̄25.5000样本标准差 s8.6699标准误 SE2.7417假设均值 μ₀20t 统计量… → 点击后 样本数 n10样本均值 x̄25.5000样本标准差 s8.6699标准误 SE2.7417假设均值 μ₀20t 统计量…
- `tools/tcm-chemistry/fingerprint-similarity.html` — 按钮「📋 计算相似度」｜构造值 refData [textarea] "abc 123" → "probe-a\nprobe-b\nprob"｜改前 0.9981平均相关系数0.9995平均夹角余弦0.9985最大相关系数0.9974最小相关系数 ⏐ 📋 复制结果⬇️… → 点击后 0.9981平均相关系数0.9995平均夹角余弦0.9985最大相关系数0.9974最小相关系数 ⏐ 📋 复制结果⬇️…
- `tools/tcm-chemistry/structure-identification.html` — 按钮「📊 解析IR数据」｜构造值 irInput [text] "abc 123" → "abc 123x"｜改前 IR数据解析结果输入1个吸收峰，识别出0个特征基团📊 特征峰归属结构特征推断：未识别到明显特征基团解析提示：IR主要用… → 点击后 IR数据解析结果输入1个吸收峰，识别出0个特征基团📊 特征峰归属结构特征推断：未识别到明显特征基团解析提示：IR主要用…
- `tools/text/text-to-ascii-art.html` — 按钮「计算」｜构造值 src [text] "abc 123" → "abc 123x"｜改前 ASCII 艺术字 ⏐ 📋 复制结果⬇️ 导出 TXT → 点击后 ASCII 艺术字 ⏐ 📋 复制结果⬇️ 导出 TXT

### 重置按钮未改变任何输入（31 页）

- `tools/audio/audio-recorder.html` — 「清空全部」｜点击后所有输入值未变化
- `tools/biz/lorem-ipsum-advanced.html` — 「清空」｜点击后所有输入值未变化
- `tools/cleaning/appliance-cycle.html` — 「重置所有记录」｜点击后所有输入值未变化
- `tools/dentistry/sialography.html` — 「清空」｜点击后所有输入值未变化
- `tools/design/image-to-ascii.html` — 「清空」｜点击后所有输入值未变化
- `tools/edu2/wrong-book.html` — 「清空全部」｜点击后所有输入值未变化
- `tools/elderly/fall-risk.html` — 「重置」｜点击后所有输入值未变化
- `tools/elderly/reminder-time.html` — 「🗑️ 清空全部」｜点击后所有输入值未变化
- `tools/finance/password-generator-advanced.html` — 「清空」｜点击后所有输入值未变化
- `tools/food/nutrition-calculator.html` — 「清空本餐」｜点击后所有输入值未变化
- `tools/funeral/ceremony-timeline.html` — 「清空」｜点击后所有输入值未变化
- `tools/general/calc-13.html` — 「🗑️ 重置」｜点击后所有输入值未变化
- `tools/general/calc-14.html` — 「🗑️ 重置」｜点击后所有输入值未变化
- `tools/hematology/aps-diagnosis.html` — 「重置」｜点击后所有输入值未变化
- `tools/hematology/rater-risk-1.html` — 「重置」｜点击后所有输入值未变化
- `tools/home/furniture-layout.html` — 「🧹 清空布局」｜点击后所有输入值未变化
- `tools/hydraulic/cycle-19.html` — 「清空」｜点击后所有输入值未变化
- `tools/it/nanoid-generator.html` — 「清空」｜点击后所有输入值未变化
- `tools/it/random.html` — 「清空」｜点击后所有输入值未变化
- `tools/it/uuid-v7-generator.html` — 「清空」｜点击后所有输入值未变化
- `tools/property/cycle-10.html` — 「清空」｜点击后所有输入值未变化
- `tools/rehabilitation/berg-balance-scale.html` — 「重置」｜点击后所有输入值未变化
- `tools/rehabilitation/flacc-scale.html` — 「重置」｜点击后所有输入值未变化
- `tools/rehabilitation/mmse-scoring.html` — 「重置」｜点击后所有输入值未变化
- `tools/rheumatology/bvas.html` — 「重置」｜点击后所有输入值未变化
- `tools/rheumatology/rater-16.html` — 「重置」｜点击后所有输入值未变化
- `tools/rheumatology/rater-17.html` — 「重置」｜点击后所有输入值未变化
- `tools/rheumatology/sledai.html` — 「重置」｜点击后所有输入值未变化
- `tools/safety/reminder-cycle-protection.html` — 「清空全部」｜点击后所有输入值未变化
- `tools/tcm-diagnosis/tongue-diagnosis.html` — 「重置」｜点击后所有输入值未变化
- `tools/transport/calc-4.html` — 「🗑️ 清空选择」｜点击后所有输入值未变化

### 导出/下载按钮 onclick 目标函数不存在（必死）（1 页）

- `tools/it/typescript-compiler.html` — 「⬇ 下载 JS」｜onclick 调用 downloadJs() 但该函数不存在（typeof=false）

### 死控件（静态检测，1 页）

> 仅列「控件 id 在整页脚本中零引用、且页面没有泛化读取控件」的页；如需与运行时交叉验证，见 JSON 的 `deadControlPages`。

- `tools/legal/legal-calculator.html` — lit-type-labor(input/radio)、lit-type-ip(input/radio)

### 低置信度线索：导出/下载未观察到触发（367 页）

> 这些页的导出按钮 onclick 函数存在、点击也不报错，但没观察到带 download 的 `a.click()`；多为结果为空时静默 return，需人工复核，不计入缺陷数。

- `tools/accounting/report-2.html` —「导出明细 CSV」（__report_2Export）
- `tools/acupuncture/acupoint-combination.html` —「导出明细 CSV」（__acupoint_combinationExport）
- `tools/admin/analysis-30.html` —「导出明细 CSV」（__analysis_30Export）
- `tools/admin/detector-time.html` —「⬇️ 导出日程 CSV」
- `tools/admin/version-control.html` —「📤 导出JSON」（exportData）
- `tools/advertising/analysis-27.html` —「导出明细 CSV」（__analysis_27Export）
- `tools/advertising/analysis-55.html` —「导出明细 CSV」（__analysis_55Export）
- `tools/advertising/storyboard-timeline.html` —「导出脚本」（exportScript）
- `tools/agriculture/countdown-cycle.html` —「导出明细 CSV」（__countdown_cycleExport）
- `tools/agriculture/cycle-honey.html` —「📥 导出记录」（exportExtr）
- `tools/ai/ai-10.html` —「导出 CSV」（__b1Export）
- `tools/ai/ai-11.html` —「导出 CSV」（__abExport）
- `tools/ai/ai-12.html` —「导出 CSV」（__b2Export）
- `tools/ai/ai-13.html` —「导出 CSV」（__acExport）
- `tools/ai/ai-14.html` —「导出 CSV」（__b3Export）
- `tools/ai/ai-15.html` —「导出 CSV」（__adExport）
- `tools/ai/ai-16.html` —「导出 CSV」（__aeExport）
- `tools/ai/ai-17.html` —「导出 CSV」（__afExport）
- `tools/ai/ai-4.html` —「导出 CSV」（__a4Export）
- `tools/ai/ai-5.html` —「导出 CSV」（__a5Export）
- `tools/ai/ai-6.html` —「导出 CSV」（__a6Export）
- `tools/ai/ai-8.html` —「导出 CSV」（__a8Export）
- `tools/ai/ai-7.html` —「导出 CSV」（__a7Export）
- `tools/ai/ai-9.html` —「导出 CSV」（__a9Export）
- `tools/ai/ai-code-review.html` —「导出 CSV」（__crExport）
- `tools/ai/ai-prompt-generator.html` —「导出 CSV」（__pgExport）
- `tools/ai/ai.html` —「导出 CSV」（__b4Export）
- `tools/ai/attention-head-dim.html` —「导出 CSV」（__ahExport）
- `tools/ai/attention-flops.html` —「导出 CSV」（__afExport）
- `tools/ai/auc-rank.html` —「导出 CSV」（__arExport）
- `tools/ai/augmentation-multiplier.html` —「导出 CSV」（__b5Export）
- `tools/ai/cohens-kappa.html` —「导出 CSV」（__ckExport）
- `tools/ai/context-window.html` —「导出 CSV」（__cwExport）
- `tools/ai/best-epoch.html` —「导出 CSV」（__beExport）
- `tools/ai/cosine-similarity.html` —「导出 CSV」（__csExport）
- `tools/ai/cross-entropy.html` —「导出 CSV」（__ceExport）
- `tools/ai/dropout.html` —「导出 CSV」（__dpExport）
- `tools/ai/elbow-wcss.html` —「导出 CSV」（__ewExport）
- `tools/ai/flops.html` —「导出 CSV」（__flExport）
- `tools/ai/epoch-time.html` —「导出 CSV」（__etExport）
- `tools/ai/grad-accumulation.html` —「导出 CSV」（__gaExport）
- `tools/ai/inference-throughput.html` —「导出 CSV」（__itExport）
- `tools/ai/k-means.html` —「导出 CSV」（__kmExport）
- `tools/ai/l1-l2-regularization.html` —「导出 CSV」（__l1Export）
- `tools/ai/l1-l2.html` —「导出 CSV」（__l2Export）
- `tools/ai/lr-decay.html` —「导出 CSV」（__ldExport）
- `tools/ai/lr-warmup.html` —「导出 CSV」（__lwExport）
- `tools/ai/min-max.html` —「导出 CSV」（__mxExport）
- `tools/ai/model-accuracy.html` —「导出 CSV」（__maExport）
- `tools/ai/multi-agent-overhead.html` —「导出 CSV」（__moExport）
- `tools/ai/precision-recall.html` —「导出 CSV」（__prExport）
- `tools/ai/quantization-ratio.html` —「导出 CSV」（__qrExport）
- `tools/ai/rag.html` —「导出 CSV」（__rgExport）
- `tools/ai/relu-leakyrelu.html` —「导出 CSV」（__rlExport）
- `tools/ai/rmse.html` —「导出 CSV」（__rmExport）
- `tools/ai/roc-auc.html` —「导出 CSV」（__raExport）
- `tools/ai/sigmoid.html` —「导出 CSV」（__sgExport）
- `tools/ai/softmax.html` —「导出 CSV」（__smExport）
- `tools/ai/softmax-2.html` —「导出 CSV」（__s2Export）
- `tools/ai/specificity.html` —「导出 CSV」（__spExport）
- `tools/ai/temperature-scaling.html` —「导出 CSV」（__tsExport）
- `tools/ai/steps-per-epoch.html` —「导出 CSV」（__seExport）
- `tools/ai/training-flops.html` —「导出 CSV」（__tfExport）
- `tools/ai/transformer-params.html` —「导出 CSV」（__tpExport）
- `tools/ai/vram-estimate.html` —「导出 CSV」（__veExport）
- `tools/astronomy/convert-17.html` —「导出明细 CSV」（__convert_17Export）
- `tools/audio/audio-cut.html` —「⬇
导出 WAV」（exportSelection）
- `tools/audio/audio-echo.html` —「💾 导出 WAV」（exportWav）
- `tools/audio/audio-recorder.html` —「导出音频」（exportAudio）
- `tools/automotive/fuel-anomaly.html` —「💾 下载结果」
- `tools/beauty/aging-calculator.html` —「⬇️ 导出 TXT」
- `tools/biz/lorem-ipsum-advanced.html` —「导出明细 CSV」（__lorem_ipsum_advancedExport）
- `tools/biz/summary-rater-csat.html` —「导出明细 CSV」（__summary_rater_csatExport）
- `tools/biz/team-roster-generator.html` —「导出明细 CSV」（__team_roster_generatorExport）
- `tools/biz/text-compare.html` —「导出明细 CSV」（__text_compareExport）
- `tools/biz/text-extract-dates.html` —「导出明细 CSV」（__text_extract_datesExport）
- `tools/biz/text-extract-ips.html` —「导出明细 CSV」（__text_extract_ipsExport）
- `tools/cardiology/has-bled.html` —「导出明细 CSV」（__has_bledExport）
- `tools/ceramics/glaze-temp.html` —「⬇️ 导出测温锥对照 CSV」
- `tools/chess/bridge-scoring.html` —「导出明细 CSV」（__bridge_scoringExport）
- `tools/chess/gomoku-forbidden.html` —「导出明细 CSV」（__gomoku_forbiddenExport）
- `tools/cleaning/appliance-cycle.html` —「导出明细 CSV」（__appliance_cycleExport）
- `tools/cleaning/cycle-20.html` —「⬇️ 导出养护排期 CSV」
- `tools/cleaning/staff-schedule.html` —「导出明细 CSV」（__staff_scheduleExport）
- `tools/clinical-lab/hba1c-converter.html` —「导出明细 CSV」（__hba1c_converterExport）
- `tools/clinical-lab/urinalysis-interpretation.html` —「⬇️ 导出 TXT」
- `tools/clinical-nursing/cycle-7.html` —「📥 导出记录」（exportData）
- `tools/clinical-nursing/pressure-injury-description.html` —「导出明细 CSV」（__pressure_injury_descriptionExport）
- `tools/clinical-nursing/reminder-time-1.html` —「📥 导出记录」（exportData）
- `tools/clinical-nursing/suction-pressure.html` —「导出明细 CSV」（__suction_pressureExport）
- `tools/cognition/cognitive-assessment.html` —「⬇️ 导出 TXT」
- `tools/cognition/schulte-table.html` —「⬇️ 导出训练记录 CSV」
- `tools/data/calc-2.html` —「导出明细 CSV」（__calc_2Export）
- `tools/data/csv-analyzer.html` —「制表符导出数据分析」
- `tools/data/csv-json.html` —「导出明细 CSV」（__csv_jsonExport）
- `tools/data/data-cleaner.html` —「导出明细 CSV」（__data_cleanerExport）
- `tools/data/yaml-json.html` —「导出明细 CSV」（__yaml_jsonExport）
- `tools/dentistry/sialography.html` —「导出明细 CSV」（__sialographyExport）
- `tools/dermatology/chilblain-grading.html` —「导出明细 CSV」（__chilblain_gradingExport）
- `tools/dermatology/hdss-hyperhidrosis.html` —「导出明细 CSV」（__hdss_hyperhidrosisExport）
- `tools/dermatology/pityriasis-rosea.html` —「导出明细 CSV」（__pityriasis_roseaExport）
- `tools/design/blueprint-grid.html` —「导出明细 CSV」（__blueprint_gridExport）
- `tools/design/checkerboard-generator.html` —「导出明细 CSV」（__checkerboard_generatorExport）
- `tools/design/dot-pattern.html` —「导出明细 CSV」（__dot_patternExport）
- `tools/design/gradient-from-color.html` —「导出明细 CSV」（__gradient_from_colorExport）
- `tools/design/grid-pattern.html` —「导出明细 CSV」（__grid_patternExport）
- `tools/design/image-cropper.html` —「导出明细 CSV」（__image_cropperExport）
- `tools/design/image-rounded-corners.html` —「⬇ 下载 PNG」（downloadResult）
- `tools/design/image-to-ascii.html` —「下载 .txt」（downloadResult）
- `tools/design/iso-noise-reference.html` —「导出明细 CSV」（__iso_noise_referenceExport）
- `tools/design/loading-dots.html` —「导出明细 CSV」（__loading_dotsExport）
- `tools/design/isometric-grid.html` —「导出明细 CSV」（__isometric_gridExport）
- `tools/design/music-scale-reference.html` —「⬇️ 导出音阶 CSV」（msExportCsv）
- `tools/design/pattern-generator.html` —「导出明细 CSV」（__pattern_generatorExport）
- `tools/design/qr-code-styled.html` —「下载」（downloadImg）
- `tools/design/signature-pad.html` —「⬇ 导出 PNG」（exportPNG）
- `tools/design/spectrum-visualizer.html` —「导出明细 CSV」（__spectrum_visualizerExport）
- `tools/design/spinner-generator.html` —「导出明细 CSV」（__spinner_generatorExport）
- `tools/design/stripe-pattern.html` —「导出明细 CSV」（__stripe_patternExport）
- `tools/design/svg-to-png.html` —「下载 PNG」（downloadPNG）
- `tools/design/tailwind-colors.html` —「⬇️ 导出色板清单 CSV」（__twExport）
- `tools/design/waveform-visualizer.html` —「导出明细 CSV」（__waveform_visualizerExport）
- `tools/ecommerce/cycle-15.html` —「导出数据」（exportData）
- `tools/ecommerce/report.html` —「导出明细 CSV」（__reportExport）
- `tools/edu/24-point-solver.html` —「导出明细 CSV」（__24_point_solverExport）
- `tools/edu/chinese-stroke-counter.html` —「导出明细 CSV」（__chinese_stroke_counterExport）
- `tools/edu/convert-1.html` —「导出明细 CSV」（__convert_1Export）
- `tools/edu/convert-3.html` —「导出明细 CSV」（__convert_3Export）
- `tools/edu/ebbinghaus-curve.html` —「导出明细 CSV」（__ebbinghaus_curveExport）
- `tools/edu/edu-unit-converter.html` —「导出明细 CSV」（__edu_unit_converterExport）
- `tools/edu/exam-gpa-calculator.html` —「⬇️ 导出成绩单 CSV」
- `tools/edu/exam-study-planner.html` —「📤 导出」（exportTasks）
- `tools/edu/pinyin-converter.html` —「导出明细 CSV」（__pinyin_converterExport）
- `tools/edu/reading-speed-calculator.html` —「导出明细 CSV」（__reading_speed_calculatorExport）
- `tools/edu2/wrong-book.html` —「导出明细 CSV」（__wrong_bookExport）
- `tools/elderly/bp-trend.html` —「导出明细 CSV」（__bp_trendExport）
- `tools/elderly/fall-risk.html` —「⬇️ 导出 TXT」
- `tools/elderly/reminder-time.html` —「📥 导出CSV」（exportSchedule）
- `tools/electrical/power-factor-compensation.html` —「导出明细 CSV」（__power_factor_compensationExport）
- `tools/encode/calc-1.html` —「导出明细 CSV」（__calc_1Export）
- `tools/encode/calc-2.html` —「导出明细 CSV」（__calc_2Export）
- `tools/encode/image-to-base64.html` —「下载图片」（downloadImg）
- `tools/endocrinology/cycle-hormone.html` —「⬇️ 导出 TXT」
- `tools/energy/stats-energy.html` —「导出明细 CSV」（__stats_energyExport）
- `tools/energy/water-tds-evaluator.html` —「导出明细 CSV」（__water_tds_evaluatorExport）
- `tools/ent/adenoid-grading.html` —「导出明细 CSV」（__adenoid_gradingExport）
- `tools/ent/tonsil-grading.html` —「导出明细 CSV」（__tonsil_gradingExport）
- `tools/fengshui/fengshui-calculator.html` —「导出明细 CSV」（__fengshui_calculatorExport）
- `tools/finance/dns-record-info.html` —「⬇️ 导出DNS记录 CSV」
- `tools/finance/gold-price-calculator.html` —「导出明细 CSV」（__gold_price_calculatorExport）
- `tools/finance/housing-fund-loan.html` —「导出明细 CSV」（__housing_fund_loanExport）
- `tools/finance/mortgage-calculator.html` —「↓ 导出结果」
- `tools/finance/number-to-words-chinese.html` —「导出明细 CSV」（__number_to_words_chineseExport）
- `tools/finance/number-to-words.html` —「导出明细 CSV」（__number_to_wordsExport）
- `tools/finance/register-depreciation.html` —「导出数据」（exportAssets）
- `tools/finance/sharpe-ratio.html` —「导出明细 CSV」（__sharpe_ratioExport）
- `tools/finance/tax-calculator.html` —「↓ 导出结果」
- `tools/finance/word-counter.html` —「↓ 导出结果」
- `tools/fishery/cycle-6.html` —「⬇️ 导出清淤计划 CSV」
- `tools/fitness/cycle-5.html` —「⬇️ 导出课程表 CSV」
- `tools/fitness/training-volume.html` —「导出明细 CSV」（__training_volumeExport）
- `tools/food/cooking-converter.html` —「导出明细 CSV」（__cooking_converterExport）
- `tools/food/food-pairing.html` —「导出明细 CSV」（__food_pairingExport）
- `tools/food/nutrition-calculator.html` —「⬇️ 导出营养明细 CSV」（__nutriExport）
- `tools/food/stats-ingredient.html` —「导出明细 CSV」（__stats_ingredientExport）
- `tools/food/stats-simulator-flavor.html` —「导出明细 CSV」（__stats_simulator_flavorExport）
- `tools/fun/1a2b-guess.html` —「⬇️ 导出 TXT」
- `tools/fun/keyboard-heatmap.html` —「导出明细 CSV」（__keyboard_heatmapExport）
- `tools/fun/word-scramble.html` —「导出明细 CSV」（__word_scrambleExport）
- `tools/fun/typing-rhythm.html` —「导出明细 CSV」（__typing_rhythmExport）
- `tools/funeral/funeral-budget-planner.html` —「导出明细 CSV」（__funeral_budget_plannerExport）
- `tools/funeral/reminder-3.html` —「导出明细 CSV」（__reminder_3Export）
- `tools/gardening/pest-identifier.html` —「导出明细 CSV」（__pest_identifierExport）
- `tools/gardening/reminder-cycle-succulent.html` —「导出明细 CSV」（__reminder_cycle_succulentExport）
- `tools/general/convert-21.html` —「导出明细 CSV」（__convert_21Export）
- `tools/geology/analysis-33.html` —「导出明细 CSV」（__analysis_33Export）
- `tools/health/calorie-needs.html` —「导出明细 CSV」（__calorie_needsExport）
- `tools/health/milk-tea-calories.html` —「导出明细 CSV」（__milk_tea_caloriesExport）
- `tools/health/rehab-timer.html` —「导出明细 CSV」（__rehab_timerExport）
- `tools/health/symptom-checker.html` —「导出明细 CSV」（__symptom_checkerExport）
- `tools/hematology/leukemia-classification.html` —「导出明细 CSV」（__leukemia_classificationExport）
- `tools/home/furniture-layout.html` —「📥 导出」（exportLayout）
- `tools/home/renovation-budget.html` —「📥 导出」（exportBudget）
- `tools/hydraulic/cycle-19.html` —「⬇️ 导出维护排程 CSV」
- `tools/image/image-collage.html` —「↓ 导出结果」
- `tools/it/barcode-ean.html` —「下载 PNG」（downloadBarcodePNG）
- `tools/it/barcode-upc.html` —「下载 PNG」（downloadBarcodePNG）
- `tools/it/calc-10.html` —「导出明细 CSV」（__calc_10Export）
- `tools/it/calc-8.html` —「导出明细 CSV」（__calc_8Export）
- `tools/it/captcha-generator.html` —「导出明细 CSV」（__captcha_generatorExport）
- `tools/it/chmod-calculator.html` —「导出明细 CSV」（__chmod_calculatorExport）
- `tools/it/code-runner.html` —「↓ 导出结果」
- `tools/it/convert-11.html` —「导出明细 CSV」（__convert_11Export）
- `tools/it/crontab-generator.html` —「导出明细 CSV」（__crontab_generatorExport）
- `tools/it/css-minifier.html` —「↓ 导出结果」
- `tools/it/css-properties.html` —「⬇️ 导出属性速查 CSV」
- `tools/it/des.html` —「导出明细 CSV」（__desExport）
- `tools/it/env-generator.html` —「导出明细 CSV」（__env_generatorExport）
- `tools/it/hmac-generator.html` —「导出明细 CSV」（__hmac_generatorExport）
- `tools/it/html-entities.html` —「导出明细 CSV」（__html_entitiesExport）
- …… 其余 167 页见 JSON


## 定向复扫用法

```bash
# 单页复扫
node scripts/runtime_scan.js --interact --only tools/it/whitespace.html --timeout 10000
# 单分类/目录复扫（尾部斜杠=整个目录）
node scripts/runtime_scan.js --interact --only tools/accounting/ --timeout 10000 --concurrency 8
# 通配符 / 多个目标（逗号分隔）
node scripts/runtime_scan.js --interact --only "tools/it/*.html,tools/ai/ai-1*.html"
# 按清单复扫（每行一个相对路径）
node scripts/runtime_scan.js --interact --files /tmp/pages.txt --timeout 10000
```

> 定向复扫会强制重扫命中页，其余记录原样保留，并在结束时自动重算本报告与 JSON；不要与 `--resume` 混用。
> 全量原始数据：`scripts/out/interaction-invalid.jsonl`（逐行、4916 条）与 `scripts/out/interaction-invalid.json`（8 MB），均被 `.gitignore` 忽略，只留本地。
> 精简摘要（401 个高/中置信页）：`plan/interaction-invalid-top100.json`。
