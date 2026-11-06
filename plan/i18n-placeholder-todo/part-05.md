## 一、静态扫描结论

  - `tools/chinese-cook/sauce-ratio.html` : `如 2`
- **gardening2**
  - `tools/gardening2/fertilizer-ppm.html` : `如 200`
  - `tools/gardening2/fertilizer-ppm.html` : `如 1`
  - `tools/gardening2/fertilizer-ppm.html` : `如 20（0–100）`
  - `tools/gardening2/watering-frequency.html` : `如 15`
- **kids**
  - `tools/kids/focus-timer.html` : `如 15（5–45）`
  - `tools/kids/focus-timer.html` : `如 5（1–20）`
  - `tools/kids/focus-timer.html` : `如 4（1–12）`
  - `tools/kids/memory-palace.html` : `如：电话号码、圆周率、单词表`
- **office**
  - `tools/office/excel-formula-reference.html` : `搜索：VLOOKUP / IF / SUMIFS`
  - `tools/office/flowchart.html` : `在此输入 Mermaid 代码，例如： flowchart TD A[开始] --> B[结束]`
  - `tools/office/mindmap.html` : `# 主题 ## 分支一 - 子节点 ## 分支二`
  - `tools/office/pdf-split.html` : `例如：1-3, 5, 7-10`
- **railway**
  - `tools/railway/diaoche-zuoye-xiaolv-youhua.html` : `如 300`
  - `tools/railway/diaoche-zuoye-xiaolv-youhua.html` : `如 30`
  - `tools/railway/power-5.html` : `如 200`
  - `tools/railway/power-5.html` : `如 60`
- **fengshui**
  - `tools/fengshui/fengshui-calculator.html` : `如 0（0–360）`
  - `tools/fengshui/fengshui-guide.html` : `如:玄关、明堂、财位...`
  - `tools/fengshui/zodiac-lookup.html` : `如 1990（1900–2100）`
- **project**
  - `tools/project/manager-cost.html` : `如：官网改版项目`
  - `tools/project/manager-cost.html` : `如 100000`
  - `tools/project/manager-cost.html` : `如 90`
- **beekeeping**
  - `tools/beekeeping/honey-estimator.html` : `如 10（1–1000）`
  - `tools/beekeeping/honey-estimator.html` : `如 50（1–10000）`
- **express**
  - `tools/express/insurance-fee.html` : `如 5000`
  - `tools/express/insurance-fee.html` : `如 20000`
- **psychology**
  - `tools/psychology/generator-20.html` : `如 5（1–50）`
  - `tools/psychology/random-12.html` : `如 5（1–50）`
- **yi**
  - `tools/yi/64-gua.html` : `卦名/卦象/卦辞...`
  - `tools/yi/yi-divination.html` : `心中默念您要问的问题...`
- **cognition**
  - `tools/cognition/digit-span-test.html` : `在此输入答案`
- **daily-goods**
  - `tools/daily-goods/shoe-size.html` : `如 255（200–320）`

### JS 动态写中文 placeholder 的页面

- data/csv-json : 输入 CSV 内容...
- sales/commission-calculator : 无穷大(最后一档)

### 已知样例（农业线报告）

- `tools/agriculture/pesticide-dose.html`：`#activePct` placeholder `如 40`、`#targetPpm` placeholder `如 500`，两处均不在该页词典 `map` 中；真机 `?lang=en-US` 已复现（见第五节）。

## 二、机制现状（关键更正）

任务前提「全站没有 data-i18n-ph 这类属性级翻译机制」**不成立**，实际存在两套属性翻译路径：

1. **`js/i18n.js` 已有 `data-i18n-ph` / `data-i18n-title` / `data-i18n-aria` / `data-i18n-alt` 机制**（[i18n.js](file:///Users/cgw/project/cgw/chenguangwu.github.io/js/i18n.js#L735-L770)）：`apply()` 对声明了 `data-i18n-ph="key"` 的元素执行 `el.setAttribute('placeholder', t(key, fallback))`，并在 `snapshotFallback()` 把原文快照到 `data-i18n-ph-fb` 以便切回中文。目前全站仅 `common.js` 的搜索框使用（`search.placeholder`），**工具页 0 页声明**。
2. **`js/tool-i18n.js` 的第三层词典已有属性分支**（[tool-i18n.js](file:///Users/cgw/project/cgw/chenguangwu.github.io/js/tool-i18n.js#L881-L911)）：英文态 `applyEnDict()` 会扫描 `placeholder/title/aria-label/alt`，用 per-tool 字典 `i18n/tools/en/<ind>/<slug>.json` 的 `map` 精确匹配替换，并支持「标签：」前缀片段。**但它与文本键共用同一个 `map` 命名空间，且仅当词典恰好收录该 placeholder 原文时才生效**。

因此真正缺口不是「没有机制」，而是：
- 工具页没有声明 `data-i18n-ph`，通用 `i18n.js` 字典也没有对应键；
- 第三层词典的属性翻译是「碰巧命中」，词典未收录的 placeholder 不会翻译；
- 所有基于元素文本的检查（含 `_en_i18n_probe.mjs`）天然看不到属性值；属性分支在 `tool-i18n.js` 里存在，但探针没有单独核对 `el.placeholder`。

## 三、是否已有页面手工处理

- 工具页声明 `data-i18n-ph`：**0 页**。
- JS 里按语言条件改写 `placeholder` 的页面：**2 页**（若为写死中文则不是语言分支，需逐页复核）。
- 未发现工具页自建 `data-i18n-ph` 声明或按 `?lang=` 改写 placeholder 的通用封装；`tool-i18n.js` 的属性分支是唯一站点级处理，属「有人知道（代码里写了注释）但未形成数据侧机制」。

## 四、最小机制建议（只记录，不改代码）

**方案 A（推荐，改动最小）：复用 `data-i18n-ph`，不新增属性名**
1. 在工具页模板/构建期给 `input[placeholder]`、`textarea[placeholder]` 自动补 `data-i18n-ph="ph:<归一化中文>"`，`title` 补 `data-i18n-title="title:<归一化中文>"`。
2. 在 `js/i18n.js` 的 `I18N_DICT`（或行业层字典）增加 **独立属性键空间**：`ph:<中文原文>` / `title:<中文原文>`，避免与文本键冲突（现有 `map` 是文本键，同一个中文串可能同时用于标题和 placeholder，语义不同）。
3. `apply()` 的 `t(key, fallback)` 已支持 fallback；英文态未收录时保留中文并输出一条可统计的缺失信号，避免「静默残留」。
4. `_en_i18n_probe.mjs` 增加属性探针：直接读 `el.placeholder` / `el.title`，含汉字即报错（不复用可见文本的 `getClientRects()` 口径）。

**方案 B（不改页面模板）：扩展现有第三层词典**
- 在 `tool-i18n.js` 属性分支前，先用 `data-i18n-ph` 键查通用字典，再回退 per-tool `map`；构建期校验「页面所有含中文的 placeholder 必须出现在 `map` 或 `ph:` 键空间」。
- 风险：`map` 文本键与属性键同串不同义时会互相覆盖；必须先引入命名空间再加校验。

**影响面与风险**
- 静态影响面：12796 处 placeholder / 153 处 title，涉及 3947 页；其中 11505 处 placeholder、130 处 title 当前无词典键。
- 方案 A 需改构建模板 + `i18n.js` + 探针，属共享文件改动，必须全量 `_build.py` + `run_gates.py`；`data-i18n-ph-fb` 快照机制已存在，切回中文可逆。
- 若直接给现有 `map` 批量补 placeholder 键，会与文本键混用，存在同串不同义覆盖风险；因此建议独立 `ph:`/`title:` 键空间。
- `placeholder` 与 `value` 不同：只改属性、不碰表单值，工具计算逻辑无影响；但 `common.js` 的 `inputmode` 推断会读取 `inp.placeholder`，英文态替换后可能影响数字键盘推断，需回归。

## 五、抽样真机（2026-11-04，Chrome headless + `?lang=en-US`）

本地 `python3 -m http.server 8137` 起服务，puppeteer-core 打开 5 页，延迟 1.2 s 后直接读 `el.placeholder`（不套 `getClientRects()` 可见性过滤）：

| 页面 | 输入框总数 | placeholder 仍含中文 | 典型残留 | 结论 |
|---|---|---|---|---|
| `tools/agriculture/pesticide-dose.html` | 7 | **2** | `如 40` / `如 500` | 与农业线报告一致 |
| `tools/finance/profit-margin-calculator.html` | 26 | 0 | — | 词典命中，现有属性分支已译 |
| `tools/tcm-diagnosis/tcm-medical-record.html` | 29 | 0 | — | 词典命中，现有属性分支已译 |
| `tools/construction/construction-calculator.html` | 23 | **13** | `如 2.8` / `如 1210` / `如 5（0–50）` | 部分命中，未命中项残留 |
| `tools/it/matrix-transpose.html` | 9 | **1** | `如 2` | 3 个中文 placeholder 中 2 个命中，剩余 1 个残留 |

真机口径：

```js
[...document.querySelectorAll('input[placeholder],textarea[placeholder]')]
  .filter(el => /[\u4e00-\u9fff]/.test(el.placeholder))
  .map(el => ({ id: el.id, placeholder: el.placeholder }))
```

**真机结论**：残留不是「机制不存在」，而是「词典未收录 + 页面未声明」双重缺口；`finance`/`tcm` 两页 0 残留证明 `tool-i18n.js` 属性分支确实生效。

