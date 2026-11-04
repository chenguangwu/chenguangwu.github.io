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
