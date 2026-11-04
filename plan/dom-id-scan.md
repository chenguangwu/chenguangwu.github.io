# DOM id 引用扫描（全站）

扫描器：[scripts/scan_dom_ids.js](file:///Users/cgw/project/cgw/chenguangwu.github.io/scripts/scan_dom_ids.js)
口径：抽取 `document.getElementById('X')` / `querySelector('#X')` 的字面量 id，与页面内真实 id 集合比对。
`getElementById(variable)`、模板串拼 id 单列为「动态引用」，不进入三档。

## 总量统计（2026-11-05）

| 指标 | 数值 |
|---|---|
| 扫描页面 | 4916（`tools/**/*.html`） |
| 字面量 id 引用 | 49,882 |
| 页面内 id 总数（按页累计） | 72,825 |
| 含动态 id 引用的页面 | 4,334 |
| 正常 | 49,855 |
| 可能动态生成 | 14 |
| **必然为 null** | **13（涉及 10 页；真缺陷 1 处，已修）** |
| 已修页数 | **1**（`tools/finance/stock-profit-calculator.html`） |

> 说明：13 条「必然为 null」里 12 条已有守卫 / 属未调用死函数，运行时不会触碰 null；只有 stock 页
> 的 `modeTag` 是无守卫的直接赋值，已修复。

## 必然为 null 清单（13 条，含前 20 全量）

| 页面 | id | 使用处 | 结论 / 处理 |
|---|---|---|---|
| tools/finance/stock-profit-calculator.html | `modeTag` | L434 `switchMode()` 内 `tag.className` / `tag.textContent` | **真缺陷：已修**。在模式单选行补 `<span id="modeTag" class="mode-tag sell">` |
| tools/clinical-nursing/cold-compress-timer.html | `result` | L429 `__emrData()` | 已有守卫 `if(!el) return;`，不抛错，不改 |
| tools/it/ini-parser.html | `indent` | L361 `getIndent()` | 死函数：全页仅此一处出现，无调用点，不改 |
| tools/it/plist-parser.html | `indent` | L326 `getIndent()` | 同上（死函数） |
| tools/it/properties-parser.html | `indent` | L333 `getIndent()` | 同上（死函数） |
| tools/it/protobuf-parser.html | `indent` | L434 `getIndent()` | 同上（死函数） |
| tools/it/xml-to-json.html | `indent` | L296 `getIndent()` | 同上（死函数） |
| tools/music/web-tuner.html | `refFreqSelect` | L541 `getElementById(...) \|\| getElementById('refFreq')` | 回退到真实存在的 `refFreq`，绑定 change 前有 `if (refFreqSelect)`，无风险 |
| tools/nephrology/jixingshensunshang-kdigo-fenqi.html | `historyBox` | L350 `renderHistory()` | 已有守卫 `if(!box)return;`，不改 |
| tools/office/flowchart.html | `graphDiv` | L528 清理 Mermaid 残留节点 | 已有守卫 `if (old) old.remove();`，属正常清理 |
| tools/office/flowchart.html | `dgraphDiv` | L530 同上 | 已有守卫 `if (oldD) oldD.remove();` |
| tools/rehabilitation/flacc-scale.html | `quickScore` | L308 更新预览区 | 已有守卫 `if (preview) {`，缺失即跳过 |
| tools/rehabilitation/mmt-grading.html | `muscleInput` | L304 取可选肌名 | 三元守卫 `getElementById('muscleInput') ? … : ''` |

## 可能动态生成清单（14 条，不修）

| 页面 | id | 生成方式 |
|---|---|---|
| tools/clinical-lab/urinalysis-interpretation.html | `ua_sg` / `ua_ph` | `buildForm` 循环 `id="ua_'+it.key+'"`，条目 `key` 为 `sg` / `ph` |
| tools/clinical-nursing/bag-valve-mask.html | `dot_0` | `id="dot_'+i+'"` 循环生成 |
| tools/design/tester-assessor.html | `sus4` / `sus9` | `id="sus'+i+'"` 循环生成 |
| tools/psychiatry/assessor-risk-5.html | `ide2` / `beh0` | `var id = prefix + i`，再写 `id="'+id+'"` |
| tools/psychiatry/calc-1.html | `q8` | 模板串 `id="q${i}"` |
| tools/rehabilitation/asia-impairment-scale.html | `sens_S4-S5_lt_l` 等 4 条 | `'sens_' + d + '_' + seg + '_' + side` 动态拼接 |

## 扫描器防误报设计

1. **`<script id=...>` 标签本身也算真实 id**：初版把整个 `<script>` 块挖空，误杀了
   `typescript-compiler` 的 `sampleTs`、`url-params` 的 `paramRowTpl`、`regex`/`text-replace` 的
   `rx-worker-src` / `tr-worker-src`；现改为只挖内容、保留标签。
2. **样例代码字符串不算真实调用**：`ai-code-review` 的 `getElementById('userName')` 位于给编辑器的
   示例代码模板串里，从未执行；现按字符位置标记字符串/模板串内部，命中即跳过。
3. **动态生成 id 单列**：支持 `id="prefix'+i+'"`、`id="q${i}"`、配置对象 `id:'n'`、
   以及 `id="'+variable+'"` 整页归入「可能动态生成」。
4. **`getElementById(variable)` / 模板引用** 不计入三档，只在统计里保留页数。

## 修复与验证（stock-profit-calculator）

- 根因：`switchMode()` 读取 `modeTag` 后直接 `tag.className = ...` / `tag.textContent = ...`，
  页面上从来没有该元素；加载时不调用所以默认态正常，**切换买卖模式必抛 `Cannot set properties of null`**。
- 修法：在模式单选行补 `<span id="modeTag" class="mode-tag sell">卖出模式</span>`，与既有
  `.mode-tag` 样式、`switchMode()` 的 class/文案切换逻辑对齐。
- headless 实测：初始 `卖出模式|mode-tag sell` → 切「浮动盈亏」后 `浮动盈亏|mode-tag float`
  且卖出价标签同步为「浮动盈亏基准价」→ 切回卖出后 `卖出模式|mode-tag sell`，
  `summaryArea` 文本与初始完全一致，**0 条 `Cannot read/set`、0 条 `is not defined`**。
