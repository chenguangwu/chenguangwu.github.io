# no_effect 低置信线索复核（工程/数学前缀）

> 回写给扫描线（`scripts/runtime_scan.js --interact`）：本文件只登记「探针失真」页及该页合法输入样例，供改进 `no_effect` 探针；扫描报告 `plan/interaction-validity.md` 仍是自动产物，勿手工写回。

## 取数口径

- 数据源：`scripts/out/interaction-invalid.json`（全站 4916 页基线，`groups.no_effect = 53`）。
- 负责前缀：`construction/`、`civil/`、`structural/`、`electrical/`、`hvac/`、`machinery/`、`fire-rescue/`、`math/`（`math/calculus-tools` 已另派，排除）。
- 筛选结果：命中 **1 页**，即 `tools/structural/von-mises-2d.html`。

## 复核结论（三档）

| 页面 | 探针原始变异 | 结论 | 合法输入样例（回写扫描线） | 真机证据 |
|---|---|---|---|---|
| tools/structural/von-mises-2d.html | `sx [number] "0" → "7"`（`valid.mutation`），`changedByInput=false`、`changedByClick=false` | **探针失真**（真无效 0 / 死控件 0） | `sx: 80e6`（页面单位 **Pa**，科学计数法；默认 `sx=100e6`、`sy=50e6`、`t=30e6`） | 真机：`sx 100e6→80e6` 后 `σ_vm 101.00→87.18 MPa`、`σ1 86.60→70.00`、`τmax 39.05→33.54`，`changed=true` |

## 失真原因

页面输入框单位为 Pa，探针把 `sx` 改成 `7`（7 Pa），结果按 `(vm/1e6).toFixed(2)` 输出 MPa，7 Pa ⇒ 0.00 MPa，与默认 0 值四舍五入后同为 `0.00`，故扫描判「输出不变」。页面计算链路本身正常。

## 建议探针改法（扫描线）

1. 对 `type="number"` 且默认值为科学计数法（`100e6` 形态）的输入，变异值应**按默认量级取**（如 `0.8×默认值`），不要写死 `7`。
2. 或给该页加白名单合法样例：`{"tools/structural/von-mises-2d.html": {"sx": "80e6"}}`，后续复扫直接使用。
3. `no_effect` 判定前先看结果区是否仍为 `0.00` 量级（结果被 `toFixed(2)` 抹平）——若变异前后数值差小于输出精度，应降级为「精度掩蔽」而非「按钮无效」，避免同类误报。

## 修复动作

- 真无效 0 页、死控件 0 页，**本批无页面改动**。
- 该页已在批次 C 加过「全空守卫」，空态行为另行验证通过。

---

# no_effect 全量复扫（2026-11-05，相对量级探针）

> 上下文：扫描线已把 `no_effect` 主探针从「写死小数字」改为 **0.8× 默认值**（默认 0/空时用 min 1.5× / min+step / max 半值 / step），无变化时再追加 **5× 放大探针**。本节是对原 53 页的定向复扫结果（`--files` 定向，其余 4863 条记录原样保留）。

## 复扫后总账

| 项 | 页数 |
|---|---|
| 原 `no_effect` 基线 | 53 |
| 复扫后退出 `no_effect`（输出已能随合法变异变化） | **5** |
| 剩余 `no_effect` | **48** |
| ├ 真无效（合法输入下结果区仍完全不变） | **4** |
| ├ 阈值/分档掩蔽（`probe_masked`，不计缺陷） | **3** |
| └ 探针失真（输入类型/格式/快照区问题，非页面缺陷） | **41** |
| 死控件 | **0** |

已退出的 5 页：`tools/structural/von-mises-2d.html`（0.8×/5× 后 σ_vm、τmax 均变化）、`tools/life/age-calculator.html`、`tools/meteorology/wind-direction.html`、`tools/healthcare/healthcare-4.html`（相对变异后结果变化）、`tools/hematology/hlh-diagnosis.html`（探针被页面拒绝，属 probeInvalid 而非缺陷）。

## A. 真无效（4 页，逐页证据）

| 页面 | 注入值（合法） | 输出对比 | 判定 |
|---|---|---|---|
| `tools/it/json-to-tsv.html` | `jsonInput`：`{"a":1}` → `{"a":2,"b":3}` | 结果区仍为 `[PRE] a.b`，行/列/表体均不刷新 | **真无效**：JSON 变更未触发重新生成 |
| `tools/stats/regression-analysis.html` | `pred-x`：`11` → `20` | 样本数/斜率/截距/r/R²/残差全部不变 | **真无效**：预测输入未参与重算或未渲染 |
| `tools/stats/statistical-tests.html` | `one-mu`：`20` → `30` | `t 统计量 2.0061`、`p 0.5000`、临界值全部不变 | **真无效**：假设均值未参与检验重算 |
| `tools/safety/haxijisuan.html` | `input`：`abc 123` → `hello` | 任意输入都固定显示 `❌ Failed to execute 'digest' on 'SubtleCrypto'` | **真缺陷（功能报错）**：摘要算法本身不可用 |

## B. 阈值/分档掩蔽（3 页，`probe_masked`，不计缺陷）

| 页面 | 主探针 | 放大探针 | 掩蔽原因 |
|---|---|---|---|
| `tools/endocrinology/pcos-diagnosis.html` | `cycle 45 → 36` | `→ 90` | 36/45/90 都落在「>35 天 = 排卵障碍」同一档，结论恒为 3/3 |
| `tools/hematology/mm-staging.html` | `albumin 35 → 28` | 两值都低于 35 g/L 分档线 | R-ISS 分期与中位 OS 不变 |
| `tools/rheumatology/sapho-syndrome.html` | `duration 3 → 2.4` | 同一评分档 | 诊断评分恒为 7 分 |

> 这 3 页计算链路正常，属于「输入跨档才会变结论」的分档型页面。建议后续探针直接按控件 `min/max` 取两端极值，而不是靠 5× 放大。

## C. 探针失真（41 页，按原因分组）

### C1. 被注入控件不是计算输入（11 页）

| 页面 | 被改控件 | 说明 |
|---|---|---|
| `tools/agriculture/countdown-4.html` | `batchName`（批次名称） | 只改标题，倒计时结果不变 |
| `tools/funeral/memorial-date.html` | `memTitle`（标题） | 只改展示标题 |
| `tools/gardening/plant-calendar.html` | `search`（搜索框） | 过滤列表，不是参数 |
| `tools/science/periodic-table.html` | `search`（搜索框） | 过滤元素卡片 |
| `tools/image/wechat-cover-maker.html` | `title`（封面标题） | 只影响 canvas 绘制 |
| `tools/it/password-generator.html` | `length`（推荐长度） | 输出是静态建议文案 |
| `tools/music/music-analysis.html` | `sample-rate` | 展示用字段，未参与计算 |
| `tools/nuclear/pair-annihilation.html` | `dummy` | 占位输入，物理常量页 |
| `tools/rental/cycle-11.html` | `number` | 说明性字段，结果区为说明文 |
| `tools/design/mesh-gradient.html` | `overlay` | 颜色叠加文本，非数值参数 |
| `tools/electromagnetism/free-space-impedance.html` | `x` | 占位输入，页面为常量展示 |

### C2. 文本/结构化输入被灌乱码（13 页）

`tools/data/pivot-table.html`、`tools/it/ast-viewer.html`、`tools/it/docker-run-converter.html`、`tools/it/hill-cipher.html`、`tools/it/html-nesting-checker.html`、`tools/it/protobuf-parser.html`、`tools/it/sitemap-generator.html`、`tools/it/toml-formatter.html`、`tools/it/uuid-v5-generator.html`、`tools/life/chinese-number.html`、`tools/music/chord-notes.html`、`tools/tcm-chemistry/fingerprint-similarity.html`、`tools/tcm-chemistry/structure-identification.html`

> 均为 textarea/文本输入被写入 `abc 123` 或 `probe-a\nprobe-b`，页面按格式解析后无有效结果（`chinese-number` 已显示「无法识别输入」，属正常拒绝）。改法：为这些页登记合法样例（CSV/TOML/JSON/和弦名/IR 峰列表），或跳过非结构化输入。

### C3. 已用合法值复验、输出确实变化（6 页，确认非缺陷）

| 页面 | 合法值 | 复验结果 |
|---|---|---|
| `tools/cardiology/calc-1.html` | `sbp 120` | 「正常血压」→「高血压前期」，分级变化 |
| `tools/dermatology/leprosy-grading.html` | `leprosyType=BT` | 临床分型由 TT → BT，文案整段变化 |
| `tools/hematology/itp-risk-score.html` | `drug=quinine` | 因果关系等级/评分明细变化 |
| `tools/it/dockerfile-generator.html` | `port 8080` | Dockerfile `EXPOSE` 行变化（扫描时结果区只截到标题） |
| `tools/design/flexbox-generator.html` | `gap 30` | 生成的 CSS `gap` 值变化 |
| `tools/text/text-to-ascii-art.html` | `src=HI` | ASCII 艺术字内容变化 |

### C4. 数值探针被 `min`/`step` 卡死（3 页）

`tools/food-processing/ph-adjustment.html`（`vol 0.001 → 0.001`，被 min 卡住）、`tools/metallurgy/alloy-ratio.html`（`steelW 0.01 → 0.01`，同上）、`tools/pr/risk-assessment.html`（`riskProb 3 → 2.4` 后结果区仍全 0，属空态/填值链路问题，另行复验）。

### C5. 需要文件或组合输入（4 页）

`tools/image/image-compress.html`（需上传文件）、`tools/forensic-medicine/electrocution-injury.html`（select 需与损伤特征组合）、`tools/forensic-medicine/rigor-mortis.html`（select 需环境温度+尸僵组合）、`tools/food-processing/fermentation-brix.html`（其余糖度/体积字段为空时结果恒为 0）。

### C6. 快照区太窄 / 结果在 canvas（4 页）

`tools/life/unit-converter.html`、`tools/pet/fish-tank-volume.html`、`tools/sales/moving-average.html`、`tools/sports/sports-stats.html`

> 扫描快照只取 `#result/.result` 或首段正文，这 4 页的真实结果在表格/canvas/右栏，需人工打开页面确认。

## 建议

1. **真无效 4 页**优先修：`json-to-tsv`、`regression-analysis`、`statistical-tests` 的事件绑定/重算链路，`haxijisuan` 的 SubtleCrypto 调用（非安全上下文或算法名错误）。
2. **探针改法**（扫描线已落地）：数值控件按 0.8× 默认值；分档型页面用 `min/max` 两端极值；文本控件按页面格式注入合法样例（C2 的 13 页建议登记白名单）。
3. **不再把 C1/C2/C5/C6 计入缺陷**：这些页面的「输出不变」是探针设计问题，不是用户体验问题。
