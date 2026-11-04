# Canvas 文案英文态待办（i18n-canvas-todo）

> 结论先行：`<canvas>` 里用 `ctx.fillText()` 画出的文字**不参与**运行时 i18n（三层字典都只遍历 DOM 文本节点 / `[data-zh]` / `[data-i18n]`），加 `data-i18n` 也无效。英文态下这些图内文字必然残留中文。
>
> 治理口径：**在绘制函数内按 `document.documentElement.lang` 分支**，取对应语言字串；语言切换后需重绘图（监听 i18n 切换事件或 `popstate`/`?lang=` 变化后调用重绘）。属结构性改造，**后续单独立项**，本批不动手。

## 1. 口径与已知偏差

1. 下表由静态扫描 `fillText('中文字面量')` 生成，**只覆盖直接写字面量的调用**；
2. 经变量/参数传入的文案**不在统计内**，至少包含：
   - `tools/agriculture/irrigation-calculator.html`：`单次灌水（m³/亩）`、`输水损失`、`月累计用水（m³/亩·月）`、`月均水量`、`净灌溉`（经 `panel(title, items, unit)` 传参）
   - `tools/agriculture/crop-water-requirement.html`：图表轴标题按变量拼接
   - 其余同类封装（`drawChart` / `panel` / `renderChart` 的标题与图例参数）
3. 因此**实现时不能按下表逐条替换了事**，必须以「英文态打开页面、逐图目视核对」为准（`?lang=en-US`）。
4. 拼接型文案（如 `'第 ' + i + ' 天'`、`'生长预测：单利 vs 复利（' + years + '年）'`）要按模板整体分支，不能只替换碎片词。

## 2. 优先级

| 级别 | 范围 | 理由 |
|---|---|---|
| P0 | 本线（agriculture / forestry）共 7 页 | 正在持续修复，顺带治理成本最低 |
| P1 | finance / science / astronomy / maritime 等常用图表 | 流量大、图表文字占比高 |
| P2 | fun 游戏画布、image 模板、ophthalmology 视标 | 文字多为开局提示/品牌词，优先级低 |

## 3. 全量清单（扫描命中 62 页 / 177 条中文串）

| 页面路径（`tools/` 下） | 图中中文文本（前 6 条，`…` 表示还有） | 图类型 |
|---|---|---|
| `admin/supplies-forecast.html` | 预测 ／ 实际 ／ 移动平均 | 折线 |
| `aerospace/lift-coefficient.html` | 攻角 α (°) ／ 升力系数 Cl ／ 失速点 ／ Cl-α 曲线 | 曲线 |
| `agriculture/crop-yield.html` | 本次测产 ／ 参考产量 | 柱状对比 |
| `agriculture/harvest-planner.html` | 第 ／ 每日累计收获进度 ／ 合计 | 柱状 |
| `astronomy/earth-curvature.html` | 地平线 ／ 观察者 ／ 目标 ／ 目标位置 ／ 距离 ／ 视线 | 示意图 |
| `astronomy/solar-elevation.html` | 请输入参数以生成轨迹图 ／ 此刻 | 轨迹曲线 |
| `astronomy/tide-estimator.html` | 平均海平面 | 潮位曲线 |
| `audio/audio-cut.html` | 请先上传音频文件 | 波形 |
| `audio/audio-echo.html` | 上传音频后显示波形 | 波形 |
| `cognition/corsi-block-test.html` | 成人常模≈5.5 | 常模标注（待确认） |
| `cognition/human-benchmark.html` | Human Benchmark 认知基准测评 ／ 综合脑力指数 · 你击败了约 ／ 子测验 ／ 原始分 ／ 百分位 ／ 击败 … | 结果图（待确认） |
| `cognition/nback-training.html` | 暂无数据 ／ ■ 平均正确率 ／ ■ 每日最高 N | 折线 |
| `cognition/schulte-table.html` | 暂无该规格的练习记录 ／ — — 平均 | 柱状 |
| `cognition/stroop-test.html` | 反应时 (ms) ／ 无数据 ／ 无计分数据 ／ 试次顺序 ／ ● 一致 ／ ● 不一致 … | 柱状 |
| `cognition/time-perception.html` | −偏短 ／ + 偏长 ／ 提前(−) ／ 滞后( + ) | 散点/柱状 |
| `construction/brick-calculator.html` | 砌体: | 砌体示意图 |
| `elderly/bp-trend.html` | 暂无数据，请先记录 | 折线 |
| `ent/pure-tone-audiometry.html` | 频率 (Hz，对数轴) → ／ ● 右耳 O ／ ✕ 左耳 X | 听力图（折线） |
| `ent/temporal-resolution-hearing.html` | 轮次 → | 折线 |
| `finance/bond-yield-calculator.html` | 年份 ／ 现金流 (元) ／ 第 | 柱状（现金流） |
| `finance/break-even-calculator.html` | 盈亏平衡点: ／ 销量（件） ／ 金额（元） ／ 因素变动幅度 ／ 盈亏平衡销量(件) | 折线 |
| `finance/compound-interest.html` | 总资产 ／ 累计投入 | 折线 |
| `finance/dca-calculator.html` | 第 | 折线 |
| `finance/inflation-calculator.html` | 第 | 折线 |
| `finance/investment-roi.html` | 成本: ／ 总价值 ／ 投入本金 ／ 方案A ／ 方案B | 柱状对比 |
| `finance/irr-calculator.html` | 流入 ／ 流出 | 柱状（现金流） |
| `finance/lease-payment-calculator.html` | 第 | 折线 |
| `finance/loan-amortization.html` | 本金 ／ 利息 ／ 本金利息占比 ／ 还款曲线 ／ 剩余本金 ／ 累计利息 | 饼/环 + 折线 |
| `finance/mutual-fund-calculator.html` | 第 | 折线 |
| `finance/npv-calculator.html` | 投资/流出 ／ 流入 ／ 累计现金流 | 柱状 + 累计折线 |
| `finance/option-profit-calculator.html` | 盈亏平衡 ／ 标的价格 ／ 每股盈亏 | 损益折线 |
| `finance/position-size-calculator.html` | 胜率 (%) ／ 仓位比例 (%) ／ 价格 (元) ／ 盈亏 (元) ／ 加仓层级 ／ 累计投入 (元) … | 折线/柱状 |
| `finance/profit-margin-calculator.html` | 总成本 | 饼图 |
| `finance/retirement-calculator.html` | 退休 ／ 资产增长曲线 ／ 名义资产 ／ 实际资产（通胀调整） | 折线 |
| `forestry/forest-volume.html` | 当前: ／ 柱：典型阶段参考值｜单位：m³/公顷 | 柱状 |
| `forestry/growth-rate.html` | 普雷斯勒(单利) ／ 复利 ／ 生长预测：单利 vs 复利（ | 折线（双曲线对比） |
| `forestry/planting-density.html` | 单位：株/亩 | 示意图 |
| `forestry/tree-age.html` | 树龄(年) | 曲线（胸径-树龄） |
| `forestry/tree-volume.html` | 胸径(cm) - 材积曲线（ | 曲线 |
| `fun/breakout.html` | 按空格键或点击发球 ／ ⏸ 暂停中 ／ 按空格键继续 | 游戏画布 |
| `fun/snake-game.html` | 暂停 ／ 按空格继续 | 游戏画布 |
| `fun/space-shooter.html` | 🚀 太空射击 ／ 点击「开始游戏」或按 Enter 开始 | 游戏画布 |
| `fun/tetris.html` | 点击「开始游戏」 ／ 开始经典俄罗斯方块 | 游戏画布 |
| `fun/typing-rhythm.html` | 开始打字后显示节奏波形 ／ 间隔(ms) ／ 均值 | 波形 |
| `futures/option-payoff.html` | 盈亏平衡 ／ 标的价格 S ／ 损益 | 损益折线 |
| `health/calorie-needs.html` | 第 ／ 体重 (kg) | 折线 |
| `healthcare/tdee-calculator.html` | TDEE kcal/日 ／ 第 ／ 体重 (kg) | 折线 |
| `hematology/thrombin-generation.html` | 时间 (min) ／ 凝血酶 (nM) | 曲线 |
| `image/wechat-cover-maker.html` | ToolBox · 在线工具集 | 画布模板（非图表） |
| `maritime/tide-window.html` | 所需潮高 ／ 高潮 ／ 低潮 ／ 次低潮 ／ 潮位曲线 ／ 可通航窗口 | 曲线 |
| `marketing/price-elasticity.html` | 价格 → ／ 销量 → | 曲线 |
| `medical/medical-calculator.html` | 正常 36.0-37.2℃ ／ 发热 37.3℃ ／ 暂无体温数据，请添加记录 | 体温折线 |
| `ophthalmology/eye-chart-toolkit.html` | 哪一组线条最模糊 / 最深？ | 视标画布（非图表） |
| `pet-training/command-repetition.html` | 保留率 (%) | 曲线 |
| `procurement/eoq.html` | 总成本 ／ 订货成本 ／ 持有成本 | 曲线 |
| `psychology/attachment-style-test.html` | 回避维度 →（越右越回避） ／ 焦虑维度 ↑（越上越焦虑） ／ 安全型 ／ 疏离型 ／ 痴迷型 ／ 恐惧型 … | 象限散点 |
| `psychology/bubble-tea-personality-quiz.html` | 你是哪款珍珠奶茶 ／ 契合度 ／ 🧋 ToolBox · 珍珠奶茶人格测试 | 结果卡渲染 |
| `psychology/enneagram-test.html` | ● 主导型 ／ --- 压力态 ／ 安全态 ／ 九型人格测试结果 ／ 翼型 ／ 核心恐惧： … | 九型结构图 |
| `sales/moving-average.html` | 实际 ／ 移动平均 ／ 预测 | 折线 |
| `science/rc-time-constant.html` | 充电 ／ 放电 | 曲线 |
| `science/statistics-calculator.html` | 频数 ／ 数值 | 直方图 |
| `science/vector-calculator.html` | 向量 A = ／ 向量 B = ／ 结果 C | 矢量示意图 |

## 4. 实现要点（立项时照此做）

1. 统一入口：每个页面在 `drawChart()` 顶部取 `var EN = String(document.documentElement.lang||'').indexOf('en')===0;`，所有文字走 `EN ? '...' : '...'`；不在绘制函数里散写判断。
2. 语言切换须重绘：`?lang=en-US` 是运行时切换，`drawChart` 依赖初始化时机 → 在 `i18n` 应用完成后（`DOMContentLoaded` 之后再 `requestAnimationFrame`）重绘一次。
3. 数字/单位统一：轴标题与图例的单位符号（`m³/亩`、`kg/天`、`株/亩`）两语言共用同一写法，只翻译说明词，避免单位也被意译。
4. 验收：`?lang=en-US` 打开页面，`getClientRects()` 可见的 canvas 区域内不得出现汉字（目视 + 截图），简体/繁体态不受影响。
5. 与既有约定一致：canvas 文案**不写入** `i18n/tools/en/**` 字典（该层只服务 DOM），避免出现「字典有键但永远不生效」的假覆盖。
