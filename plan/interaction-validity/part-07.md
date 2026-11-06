## 2026-11-05 it/*-escape 家族 10 页实时绑定 + 5 页裁定 + 6 页探针盲区

### 10 页统一改法（保留原「转义 ↑」按钮）
- `<textarea id="input">` 加 `oninput="__escLive()"`；勾选项（`unicode` / `quoteSingle` 等）加 `onchange="__escLive()"`。
- `esc()` 增加 `live` 参数：空值时实时态只清空输出、不弹 `alert`；按钮态保持原提示。
- 新增 `__escLiveMode` 标志，`__<slug>Extras()` 首行 `if (__escLiveMode) return;` —— 逐键实时只刷新输出，历史记录仍由按钮写入。

真机三态（注入 `a"b\c`，再点「转义 ↑」）：

| 页面 | 默认输出 | 键入后 | 点击后 |
|---|---|---|---|
| `it/c-string-escape` | `"Hello \"World\""` | `"a\"b\\c"` | 同键入 |
| `it/css-escape` | `my\.class` | `a\"b\\c` | 同键入 |
| `it/go-escape` | `"Hello \"World\""` | `"a\"b\\c"` | 同键入 |
| `it/java-escape` | `"Hello \"World\""` | `"a\"b\\c"` | 同键入 |
| `it/js-escape` | `"Hello \"World\""` | `"a\"b\\c"` | 同键入 |
| `it/php-escape` | `'Hello "World"'` | `'a"b\\c'` | 同键入 |
| `it/python-escape` | `"Hello \"World\""` | `"a\"b\\c"` | 同键入 |
| `it/regex-escape` | `Hello \(World\)\? \[a-z\]\+ \$19\.99` | `a"b\\c` | 同键入 |
| `it/rust-escape` | `""` | `"a\"b\\c"` | 同键入 |
| `it/sql-escape` | `Hello \"World\"` | `a\"b\\c` | 同键入 |

10/10 `changedByInput=true`、`clickSameAsType=true`（`regex-escape` 曾误点到「等号转义」，按精确文本 `转义 ↑` 复测后同键入）。

### 旧期望 → 新期望（因修页面而失效）
| 用例 | 旧期望 | 新期望 | 原因 |
|---|---|---|---|
| `it/rust-escape`（自动补强 B 类零用例） | `1 2 3\n1 2 3\nchar` | `1 2 3\nchar\n1 2 3`（旧序保留为备选） | 加 `__escLive` 后 harness fallback 调函数序改变 |

本批未发现「用例固化错误行为」的条目：escape 家族旧用例均为按钮驱动，期望值是真实转义结果。

### 5 页裁定（均不改页面）
| 页面 | 结论 | 依据 |
|---|---|---|
| `office/mindmap` | 已有实时绑定，不改 | `editor.addEventListener('input', __mmPaint)` + 300ms `renderDebounced()`；探针 `boundInline` 只认 inline `oninput` 属性，故漏检 |
| `yi/yi-divination` | 显式动作合理，不改 | 起卦是一次性随机仪式，实时随输入重算会破坏「起卦」语义 |
| `security/emergency-contacts` | 显式动作合理，不改 | 三字段 + 「添加联系人」是 CRUD 写入列表，逐键建条目会污染列表/导出 |
| `ophthalmology/astigmatism-chart` | 已有实时绑定，不改 | 4 个 `select` 的 `change` 与 `asNote` 的 `input` 均已绑定（`render()` 重绘 canvas）；文本快照抓不到 |
| `data/data-cleaner` | 显式动作合理，不改 | 操作项 `toggleOp()` 已即调 `clean()`；文本输入保留「清洗」按钮——含「随机打乱」，实时重算会致输出抖动、导出不稳定 |

### 6 页「已有实时绑定」探针盲区（不改页面，实测注入均变）
| 页面 | 盲区原因 | 实测 |
|---|---|---|
| `rehabilitation/assistive-device-fitting` | 结果需多字段齐备，单字段注入停留在缺项提示「请输入身高、体重和臀宽」 | 5 字段齐派发 → 输出成立 |
| `science/wire-gauge-converter` | 三种模式输入互斥，非当前模式 `display:none`，需先切 radio | `awg` 24→18 → 输出变化 |
| `geology/mineral-hardness` | 输出取「最近标准矿物」，注入相邻值可能仍映射同一档 | 默认 6、注入 6.5 仍正长石 6（文本不变）；注入 8 → 黄玉 8 |
| `design/css-border-radius` | 变更落在 `.shape-preview` 的 `style.borderRadius`（无文本节点），文本比对抓不到 | 20px → 60px |
| `biz/text-case-advanced` | `oninput="updatePreview()"` 是空实现；转换类型须由按钮指定（20+ 种），实时无法唯一确定 → 属「一次性前置」 | 注入后 preview 仍为「点击下方按钮进行转换...」 |
| `design/shutter-speed-calculator` | 输出快门按标准档位取整，相邻焦距落在同一档 | 50→200mm：`1/15` → `1/60` |

### 门禁
- `scripts/verify_it_calc.js`：999/999 通过。
- `discriminate_check.js verify_it_calc.js`：已检 999 / 正确变红 999 / 逃生 0 / 跳过 0。

## 2026-11-05 rust-escape 用例真机复核 + 逐字段交互探针

### rust-escape 旧用例作废（用例层面假绿）
- 旧用例 `inputs` 为 `{input:"1\n2\n3", output:"1\n2\n3", kind:"char"}`，期望 `1 2 3\nchar\n1 2 3`；桩 `fullBlob` 与期望逐字相同，实为 **input.value + kind.value + output.value 三个注入值的回显**。
- 真机同输入：`char` 只接受单个 Unicode 标量，弹「char 字面量只能包含一个字符（当前 5 个）」，`#output` 保持为空。页面没有产出该期望串。
- 新用例锚定真机：`kind=string`、`input=a"b` ⇒ 真机输出 `"a\"b"`；默认空输入不命中（强判别）。

### 实时绑定连带缺陷（go / rust，本批修复）
- `go-escape` 的 rune 校验、`rust-escape` 的 char / byte 校验位于实时路径上：逐键输入中途必然命中，原实现 `return alert(...)` ⇒ **每按一键弹一次**；按钮模式拦截时还会残留上一次结果。
- 改为：命中即先清空 `#output`；`live` 态直接返回不弹窗，按钮态仍弹提示。
- 真机复测：rust char `1\n2\n3` → 输出空、0 弹窗；char `é` → `'\u{e9}'`；string `a"b` → `"a\"b"`；go rune `ab` → 输出空、0 弹窗；rune `é` → `'é'`。

### 新探针 `scripts/interaction_probe.js`（纯只读）
- **逐字段**注入（每个文本/数字/日期/select 单独注入并恢复）+ 全量注入，不再只改第一个输入。
- 识别三种绑定：inline `on*` 属性、`addEventListener(...)`、页面末尾直接调用渲染函数（`render()/init()/update()...`）。
- 结果签名三类组合：主容器文本（含 readonly textarea 值）+ 全部 `canvas.toDataURL()` 哈希 + 全部 `svg` outerHTML 哈希。
- 结构化输出 `{bindings, changedByField, changedAll, needsClick, emptyState, clickTargets}`，可并入 `plan/page-ledger.json`；支持 `--file` / `--dir` / `--limit` / `--out` / `--timeout` / `--port`。
- 口径细节：排除站点 chrome（header/nav/footer/`.tb-*`/`.nav-menu`）与结果框、搜索框、语言选择；点击探测**保持全量注入态**（否则起卦/清洗类会被「请输入」守卫挡掉，得到 `needsClick=false` 假结论）；点击后轮询 2s 以覆盖起卦动画与 300ms 防抖。
- 三页自检（与人工裁定一致）：
  - `office/mindmap`：`changedAll=true`、`needsClick=false`、`listeners=input` + `autoRender=render` ⇒ 已实时。
  - `yi/yi-divination`：`changedAll=false`、`needsClick=true`（🙏 起卦演示）⇒ 需按钮。
  - `data/data-cleaner`：`changedAll=false`、`needsClick=true`（🔎 清洗）；chip「去首尾空白」点击亦变化 ⇒ 操作项实时、文本需按钮。

### 门禁
- `scripts/verify_it_calc.js`：999/999 通过。
- `discriminate_check.js verify_it_calc.js`：已检 999 / 正确变红 999 / 逃生 0 / 跳过 0。

