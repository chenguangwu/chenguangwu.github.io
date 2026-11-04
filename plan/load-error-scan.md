# 全站「加载期就报错」扫描（只加载、不点击）

> 扫描日期：2026-11-05　范围：`tools/**/*.html` 共 **4916 页**　方式：真实 Chrome（headless）逐页加载，不点击、不输入。
> 脚本：`scripts/scan_load_errors.js`（新增，只读扫描，不改任何页面）　输出：`/tmp/load_error_scan*.jsonl`（隔离目录，未落仓库）。

## 0. 结论（先给可派工结论）

- **可复现的「页面自身加载期抛错」= 0 页 / 0 条**。两遍全量中共出现 36 个异常页（pass1 26 行 / pass2 20 行，含重叠），逐页复核后**全部不复现**，原因分别是扫描器 MIME 缺陷、并发写入瞬态、本机超时抖动（明细见 §4）。
- **已知基线 legal 3 页（`calc-96` / `calculator-calc-6` / `jicheng-yizhu-gongzheng-yichan-fenpei`）当前加载期 0 报错**：确认是真实缺陷（`ReferenceError: calc is not defined` @ 页内 275:1），由 `c16a36530f`（删除通用 calc 模板）引入、由同线 `1a7240e849`（清理 81 页残留顶层 `calc()`）修复。→ 标注「已归商业与HR线修」，本批无需再派工。缺陷态复现证据见 §6.2。
- **② 资源类噪声 7 页**，全部是第一方资源 404（4 个行业索引 JSON + 3 个行业 i18n 字典缺失），页面均有降级兜底、不抛 JS 异常；按本批口径**排除**，但清单见 §3，可另行派给「资源补齐」线。
- **③ 依赖用户操作才触发的一档不在本批范围**，已有两批产出可对照：`plan/inline-handler-scan.md`（6 页真缺陷已修）、`plan/dom-id-scan.md`（13 条必然 null 已修/守卫）。

## 1. 方法与口径

| 项 | 取值 |
|---|---|
| 浏览器 | 本机 Chrome，`headless:"new"`；`puppeteer-core`（`/Users/cgw/node_modules`） |
| 导航 | `page.goto(url, { waitUntil: "domcontentloaded", timeout: 20000 })`，随后固定等待 **800ms** |
| 采集通道 | ① `pageerror`（未捕获异常）② `console` 的 `type=error` ③ `unhandledrejection`（`evaluateOnNewDocument` 注入监听，取 `reason.stack \|\| message`） |
| 去重 | 同一文本归一空白后合并（rejection 常同时以 `pageerror` + `unhandledrejection` 出现） |
| 服务 | 本地 Node http（随机端口），按扩展名返回正确 MIME（含 `.mjs`/`.wasm`/字体，见 §4.1） |
| 分档 | ① 真缺陷：本地来源且非资源类文本 ② 噪声：外部来源（非 127.0.0.1）或资源/字体/网络类文本 ③ 交互触发：本批不点击，天然不覆盖 |
| 两遍 | pass1 并发 8（4916 页）；pass2 并发 6（4916 页），用于区分「稳定缺陷」与「并发写入/抖动」 |

原始行含：页面相对路径、行业、`navErr`、分类后的 `errors[]`（kind / 原文前 200 字 / 文件 / 行号）、`noiseCount`。

## 2. 分档计数（两遍全量）

| 指标 | pass1（并发 8） | pass2（并发 6） |
|---|---|---|
| 总页数 | 4916 | 4916 |
| 正常导航 | 4900 | 4904 |
| 导航失败（20s 超时，记 `navErr`） | 16 | 12 |
| ① 真缺陷页 | 2（pdf×2，扫描器 MIME 缺陷，已排除） | 1（realestate，并发半写入态，已排除） |
| ② 噪声页 | 8（含 1 条瞬态 500） | 7 |
| 无任何错误 | 4890 | 4896 |

**可复现真缺陷 = 两遍都红或单页复核仍红 = 0 页。**

## 3. Top 清单（按 `tools/<行业>/` 分组）

### ① 真缺陷（可派工）——本批 0 页

无。扫描期出现的 3 条「红」逐页复核均不成立，明细见 §4，不计入派工清单。

### ② 噪声（资源类，排除）——7 页

| 页面 | 缺失资源 | 报错原文（前 120 字） | 页面行为 |
|---|---|---|---|
| `tools/misc/index.html` | `/json/industry-misc.json` | `Failed to load resource: the server responded with a status of 404 (Not Found)` | `js/app.js` fetch 失败走 catch，显示「加载失败」 |
| `tools/misc2/index.html` | `/json/industry-misc2.json` | 同上 | 同上 |
| `tools/network/index.html` | `/json/industry-network.json` | 同上 | 同上 |
| `tools/niche/index.html` | `/json/industry-niche.json` | 同上 | 同上 |
| `tools/beekeeping/honey-estimator.html` | `/i18n/tools/beekeeping.json` | 同上 | 行业 i18n 字典缺失，英文态回退 |
| `tools/daily-goods/shoe-size.html` | `/i18n/tools/daily-goods.json` | 同上 | 同上 |
| `tools/express/insurance-fee.html` | `/i18n/tools/express.json` | 同上 | 同上 |

> 这 4 个行业（misc / misc2 / network / niche）各有 1 个分类索引页且无对应 `industry-*.json`；3 个行业（beekeeping / daily-goods / express）各有 2 页，只有需要工具级 i18n 的那 1 页触发 404。均属「资源缺失 + 页面自行兜底」，不含 JS 抛错。

### ③ 交互触发（本批不计）

本扫描全程不点击、不输入，故不覆盖。已有对照产物：

- `plan/inline-handler-scan.md`：全站 38,476 个内联事件 / 6,888 个函数名 → 6 个真缺陷（已修）。
- `plan/dom-id-scan.md`：49,882 条 id 引用 → 13 条必然 null（1 真缺陷已修，12 已守卫/死函数）。

## 4. 扫描期异常复核（扫描器/环境噪声，非页面缺陷）

### 4.1 两个 PDF 页（pass1 唯一「缺陷」，扫描器 MIME 缺陷）

| 页面 | 报错原文（前 120 字） | 来源 | 复核 |
|---|---|---|---|
| `tools/office/pdf-rotate.html` | `Failed to load module script: Expected a JavaScript-or-Wasm module script but the server responded with a MIME type of "application/octet-stream". Strict MIME type checking is enforced for module scripts...` | `127.0.0.1/.../vendor/pdfjs/4.2.67/pdf.min.mjs?_swv=d55b1f91fb`（行号 ?） | 扫描器 MIME 表缺 `.mjs` → 补 `text/javascript` 后单页复跑：`cleanPages=1, defect=0` |
| `tools/office/pdf-split.html` | 同上 | 同上 | 同上 |

> 线上 GitHub Pages 原生按 `.mjs` 返回 JS MIME，这两页线上无此问题；属扫描器自身缺陷，已修（`scripts/scan_load_errors.js` MIME 表）。

### 4.2 导航超时（pass1: statistics 16 页；pass2: psychiatry 12 页）

报错原文统一为 `Navigation timeout of 20000 ms exceeded`（`navErr`，无页面状态行号）。两批页面互不重叠，且按行业整批复跑后全绿：

| 批次 | 页面 | 复跑结果 |
|---|---|---|
| pass1 | `tools/statistics/{statistics-10,-11,-12,-13,-16,-5,-4,-7,statistics}.html`、`stddev-list`、`t-score`、`t`、`variance-list`、`z-score-calc`、`z`；`tools/stats/data-distribution.html` | `--match tools/statistics/` → 52/52 clean；`--match tools/stats/` → 5/5 clean；0 navErr |
| pass2 | `tools/psychiatry/{isi-insomnia,les-stress,lsas-social,mdq-bipolar,mmpi2-personality,panss-schizophrenia,pcl5-ptsd,phq15-somatization,phq9-depression,rater-23,pdss-panic,rater-24}.html` | `--match tools/psychiatry/` → 25/25 clean；0 navErr |

> 判定为**本机 8/6 并发渲染压力下的瞬时抖动**（两遍集群不同、单页与整行业复跑均不复现），不在派工范围。

### 4.3 realestate 1 页（pass2 唯一「缺陷」，并发半写入态）

| 页面 | 报错原文（前 120 字） | 来源/行号 | 复核 |
|---|---|---|---|
| `tools/realestate/generator-assessor.html` | `Invalid or unexpected token` | 报错事件无 stack（`file=""`） | 该文件当时 `git status = M`（他线在途）；单页复跑 `cleanPages=1, defect=0`。`pageerror` 的 SyntaxError 若为稳定缺陷不可能自愈，故判为**扫描瞬间的半写入态** |

### 4.4 `general/detector-length-lifespan.html`（pass1 一条 500，pass2 消失）

原文 `Failed to load resource: the server responded with a status of 500 (Internal Server Error)`，本地静态服务不产生 500，判定为 Chrome/网络层瞬态；单页与全量第二遍均未复现。

## 5. 已知基线：legal 3 页复核

| 页面 | 本批实测 | 根因 / 修复 | 归属结论 |
|---|---|---|---|
| `tools/legal/calc-96.html` | `cleanPages=1`，0 error | `c16a36530f` 删除模板 `function calc` 后，同脚本块尾部 `calc();` 失去提升目标 → 加载期 `ReferenceError: calc is not defined`（275:1）；`1a7240e849` 删除残留调用 | 已归商业与HR线修 |
| `tools/legal/calculator-calc-6.html` | `cleanPages=1`，0 error | 同上（275:1） | 同上 |
| `tools/legal/jicheng-yizhu-gongzheng-yichan-fenpei.html` | `cleanPages=1`，0 error | 同上（275:1） | 同上 |

结论：这是**真实缺陷，且确由本扫描能捕获的一类问题**（脚本在 `calc` 定义之前调用它）。同线在 02:34 的 `1a7240e849` 已批量清理 81 页的残留顶层调用，本批扫描（02:40 后）确认已归零；三页按用户要求保留在清单中并标注归属。

## 6. 扫描器自证（防假绿）

1. 三通道探针：注入 `calc()` 未定义 + `console.error` + `Promise.reject` 的页面 → `pageerror` / `console` / `unhandledrejection` 全部命中（`ok:true`）。
2. **缺陷态复现（本批最关键自证）**：把 `c16a36530f` 版本的三页（模板已删、顶层 `calc()` 尚存）原样挂到本地服务加载，三页全部命中：

```
tools/legal/calc-96.html                                → ReferenceError: calc is not defined @ .../calc-96.html:275:1
tools/legal/calculator-calc-6.html                      → ReferenceError: calc is not defined @ .../calculator-calc-6.html:275:1
tools/legal/jicheng-yizhu-gongzheng-yichan-fenpei.html  → ReferenceError: calc is not defined @ .../jicheng-yizhu-gongzheng-yichan-fenpei.html:275:1
```

   对照：`c16a36530f^` 的旧版（模板 `function calc` 仍在、函数提升生效）加载 0 报错 —— 证明错误源自「删模板但留调用」，而非扫描误报。
3. 端到端门禁自证：临时在 `tools/legal/__scan_selfcheck.html` 写入未定义调用 + `console.error` + `Promise.reject`，跑 `--match __scan_selfcheck` →

```json
{ "pages": 1, "defectPages": 1, "noisePages": 0, "cleanPages": 0, "defectErrors": 4, "navErrorPages": 0 }
tools/legal/__scan_selfcheck.html | tools/legal/__scan_selfcheck.html:6 | selfcheckLoadUndefined is not defined
```

   自证文件已在验证后删除（工作区无残留）。
4. 分档口径自证：上述 7 个资源 404 被稳定判为 `noise`（不计缺陷），两个 PDF 页在 MIME 修正后从 `defect` 归零。

## 7. 复跑命令

```bash
# 全量（隔离输出，默认 8 并发）
node scripts/scan_load_errors.js
# 指定并发 / 单页 / 行业
SCAN_CONCURRENCY=6 node scripts/scan_load_errors.js
node scripts/scan_load_errors.js --match legal/calc-96
node scripts/scan_load_errors.js --match tools/psychiatry/
```

产物：`/tmp/load_error_scan.jsonl`（逐页）、`/tmp/load_error_summary.json`（汇总 + 明细）；环境变量 `SCAN_OUT` 可改路径。

**入清单门槛（建议作为后续批次口径）**：同一页两遍全量都红，或单页复核仍红，才进入派工清单；只在一遍出现的异常必须先逐页复核，避免把并发写入/超时抖动当缺陷。

## 8. 7 页资源 404 的根因与修复（同日第二批）

### 8.1 三列表

| 页面 | 根因 | 修法（理由） |
|---|---|---|
| `tools/misc/index.html` | 空壳分类页：目录下只有 `index.html`、`json/tools.json` 中 `misc` 行业 0 工具、行业不在 `INDUSTRY_INFO` 也不在 sitemap；`js/category-index.js` 无条件 `fetch('/json/industry-misc.json')`，而 `_build.py` 只为「有工具的行业」生成该文件 → 404 | **③ 物理下线**：页面与目录均为空壳，且该 URL 早在 2026-10-13 已登记进 `sitemap-deadlinks.xml`，保留只会造成「死链地图说已死、实际仍 200 可索引」的矛盾 |
| `tools/misc2/index.html` | 同上（`misc2` 行业 0 工具、不在导航/sitemap） | **③ 物理下线**（同上，已在死链地图登记） |
| `tools/network/index.html` | 同上（`network` 行业 0 工具） | **③ 物理下线**（同上） |
| `tools/niche/index.html` | 同上（`niche` 行业 0 工具） | **③ 物理下线**（同上） |
| `tools/beekeeping/honey-estimator.html` | 页面没有任何 `data-i18n`，但 `js/tool-i18n.js::init()` 无条件调用 `loadIndustryDict('<ind>')`，请求 `i18n/tools/beekeeping.json`；该行业只有 `-body.json`、没有 `<ind>.json` 源文件 → 404 | **① 加「存在才加载」守卫**：行业字典只服务 `data-i18n="<industry>.<slug>.*"` 元素，页面无此命名空间就不发请求（与既有 `-phrases.json` 的索引守卫同一思路；不补空字典糊门禁） |
| `tools/daily-goods/shoe-size.html` | 同上（缺 `i18n/tools/daily-goods.json`） | **① 同上** |
| `tools/express/insurance-fee.html` | 同上（缺 `i18n/tools/express.json`） | **① 同上** |

> 全站只有 22 页真正使用 `<industry>.<slug>.*` 命名空间（design / energy / health / it / life / optical / ai，均有对应字典文件），其余页的 `loadIndustryDict` 请求本来就是无效请求。

### 8.2 修复明细

- `js/tool-i18n.js`：新增 `needsIndustryDict(industry)`，按 `document.querySelector('[data-i18n^="<ind>."]')` 判定，`loadIndustryDict` 无匹配直接返回。
- 删除 4 个空壳分类页（`tools/misc|misc2|network|niche/index.html`）。
- 连带修正 `tools/life/date-diff.html`：其面包屑 JSON-LD 原指向 `tools/misc/index.html`（删页后会成为 JSON-LD 死链），已改为 `tools/life/index.html` + 「日常生活」，可见面包屑文案同步修正。
- **未改任何 `json/*.json`**（构建产物）；也未新增 `i18n/tools/<ind>.json` 空壳。

### 8.3 复扫与验证

- `node scripts/scan_load_errors.js --match tools/beekeeping/`、`tools/daily-goods/`、`tools/express/` → 各 2 页 `cleanPages=2, noisePages=0, defect=0`（404 消失）。
- 守卫不回归（真机 + `?lang=en-US`）：`tools/it/regex.html` 仍请求 `/i18n/tools/it.json` → **200**，`data-i18n^="it."` 元素显示 `Regex Tester`；`tools/legal/calc-96.html` 不再请求 `legal.json`，0 报错。
- 删除后剩余分类页一致性：207 个 `tools/*/index.html` 与 208 个 `json/industry-*.json` 比对，**0 缺失**（不会再有同类 404）。
- `python3 _audit_links.py --check` → 16689 文件 / 165820 内链 / **0 死链**（exit 0）。

### 8.4 运维提示（本批未执行）

- 4 个旧 URL（简体 + `zh-tw/` 变体）已在 `sitemap-deadlinks.xml` 中登记，无需重复加入；部署成功（Actions `success`）后按 AGENTS §4.6 用**默认校验**跑一次 `python3 _submit_indexnow_deadlinks.py` 即可。
- 本批修改了 `js/tool-i18n.js`：按项目红线，正式部署前需由维护者执行 `python3 _build.py` 刷新 Service Worker 版本戳；本批按要求未跑 `_build.py`、未 push。

---

## 9. 本地存储与持久化健壮性（全站三档扫描）

### 9.1 普查口径与用量

- 扫描器：`scripts/scan_local_storage.js`（只读）。
- 口径：页面内联脚本 + 页面引用的本地 `/js/tools/*.js`；先把注释、字符串、正则字面量内容抹成空格（保留长度与换行）再做 `try` 块配对，避免模板串/正则里的 `{}`、`//` 干扰块结构。
- 判定：
  - **① 写无防护**：`localStorage/sessionStorage.setItem(...)` 不在任何 `try` 块内；
  - **② 解析无防护**：`JSON.parse(<存储值>)` 不在任何 `try` 块内（含「先存变量再解析」两步写法）；
  - **③ 安全**：以上均无（含已 try/catch、只读且自带默认回退、写失败不影响主流程）。
- **用量**：4912 个工具页中 **1457 页**引用 `localStorage`/`sessionStorage`；其中 1443 页有写入、1005 页有解析。

### 9.2 三档计数

| 档位 | 修复前 | 修复后（静态） | 说明 |
|---|---|---|---|
| ① 写无防护 | **371 页 / 663 处** | **371 页**（调用点仍在，但已被共享层运行时兜底） | 页内联脚本写法各异，逐页改写成本高；改为共享层收口 |
| ② 解析无防护 | **61 页 / 110 处**（其中 45 页同时属①） | **0 页** | 逐页包 `try/catch` + 清理脏键 + 回退原兜底值 |
| ③ 安全 | 4541 页 | 4541 页 | — |
| 去重后受影响页 | **387 页** | 371 页（仅静态①） | 387 = 371 + (61-45) |

> 首轮扫描器曾误报（380/69），根因是抹码器在字符串收尾引号处多跳 1 字符、导致括号/换行对齐漂移；已修正并复核 `tools/agriculture/temp-2.html` 不再误报。

### 9.3 修法：共享层一次收口（不是逐页）

**① 写无防护 → 共享层全局兜底**

- `js/common.js` 顶部新增 `hardenStorage()`：包装 `Storage.prototype.setItem`，捕获异常后置 `window.__tbStorageWriteFailed=true` 并**只提示一次**「本次无法保存到本地存储，不影响本次计算」，返回 `undefined`。
- **覆盖**：4912/4912 个工具页全部引用 `js/common.js`（实测 0 缺失），defer 脚本在 `DOMContentLoaded` 前执行 → 覆盖所有「加载后」写入（含 `setCustom` / `setRun` / `LS_PAYLOAD`）。
- **例外：9 页在「解析期」就写入**（早于 defer 的 `common.js`，实测 `document.readyState==='loading'`）：
  `tools/biz/name-generator.html`、`tools/edu/pinyin-converter.html`、`tools/it/atbash-cipher.html`、`tools/it/caesar-cipher.html`、`tools/it/html-escape.html`、`tools/it/morse.html`、`tools/it/playfair-cipher.html`、`tools/it/vigenere-visualizer.html`、`tools/usedcar/recorder-maintenance.html`。
  这 9 页在首个内联脚本顶部插入同步 setItem 兜底（`__tbSafe` 幂等标记），实测解析期写入仍被触发但 0 报错。
- 原有已安全的共享封装未改动：`js/tool-kit.js::history.*`、`js/tool-ux.js::saveField/回填` 均自带 `try/catch`。

**② 解析无防护 → 逐页（无法共享，因为页面在解析期就调用）**

- 61 页中 110 处统一改写为：
  `(function(){try{return JSON.parse(localStorage.getItem(K)||'<兜底>')}catch(e){try{localStorage.removeItem(K)}catch(_){ }return <兜底值>}})()`
- `<兜底值>` 由原兜底字面量反解为 JSON（如 `'[]'→[]`、`'{"days":0,"last":null}'→{"days":0,"last":null}`、时区页 `'["北京/上海",…]'→["北京/上海",…]`），**不是一律退化成 null**，避免脏数据时把非空默认值丢成 null 再触发二次 TypeError。
- 两步写法单独处理：`tools/it/pomodoro.html`（`const saved=localStorage.getItem(...)` → 解析处包 try/catch + 清键 + `data=null`，后续补 `data &&` 判空）。

### 9.4 真机取证（修复前原文 → 修复后 0 报错）

**① `setItem` 抛 `QuotaExceededError`（Safari 隐私模式/配额满等价注入）**

修复前（`common.js` 兜底移除 + 冻结 `Storage.prototype.setItem` 抛错）：

| 页面 | 报错原文（首行 + 调用点） |
|---|---|
| `tools/science/ohms-law-calculator.html` | `DOMException: QuotaExceededError: Failed to execute 'setItem' on 'Storage': Setting the value of the item exceeded the quota.` @ `saveHistory (…:569:16)` |
| `tools/automotive/cycle-belt.html` | 同上 @ `save (…:299:30)` |
| `tools/fun/rock-paper-scissors.html` | 同上 @ `saveState (…:508:16)` |
| `tools/science/fraction-calculator.html` | 同上 @ `saveHistory (…:486:16)` |
| `tools/health/blood-type-calculator.html` | 同上 @ `saveResult (…:427:16)` |
| `tools/science/led-resistor-calculator.html` | 同上 @ `saveHistory (…:620:16)` |

修复后（保留页面现状，仅注入 `setItem` 抛错）：同样 6 页 + `crop-yield` / `cycle-honey` / `css-minifier` / `coin-flip` 共 10 页，`setItemThrows=4`（写入确实发生）但 **0 个 `pageerror` / console error**；9 个解析期写入页同样 **0 报错**。

**② 存储键写成 `"{broken"` 后重载**

修复前：

| 页面 | 报错原文 | 触发点 |
|---|---|---|
| `tools/fun/rock-paper-scissors.html` | `SyntaxError: Expected property name or '}' in JSON at position 1 (line 1 column 2)` | `init (…:339:22)` |
| `tools/it/sql-formatter.html` | 同上 | `renderHistory (…:446:18)` |
| `tools/edu/exam-timer.html` | 同上 | `loadHistory (…:301:38)` |
| `tools/biz/name-generator.html` | 同上 | `saveHistory (…:620:21)` |
| `tools/it/css-minifier.html` | 同上 | `renderHistory (…:491:18)` |
| `tools/science/fraction-calculator.html` | 同上 | `renderHistory (…:490:21)` |

修复后：全部 68 个改动页分 3 片复验，**68/68 `pagesWithError=0`**（脏键被清理并回退默认值，页面初始渲染正常）。
另发现并修正一处二次错误：时区页原兜底是非空 JSON 数组，首版兜底退化成 `null` 引出 `TypeError: Cannot read properties of null (reading 'includes')`；按 9.3 的 JSON 反解后复验 0 报错。

### 9.5 验证与交付

- `node scripts/scan_local_storage.js` 复扫：**tier2 = 0**；tier1 仍为 371（调用点在，运行时已被共享层兜底）。
- `python3 _test_static.py`：**4705/4705 通过，0 失败 0 告警**（改动页内联脚本全部通过 `new Function` 语法校验）。
- 未改任何 `json/*.json`；未跑 `_build.py`；未 push。
- 改动清单：
  - `js/common.js`（新增 `hardenStorage()` 全局兜底）
  - 61 个工具页（`JSON.parse` 包 `try/catch` + 清脏键 + 原兜底值）
  - 9 个工具页（解析期同步 `setItem` 兜底）
  - `scripts/scan_local_storage.js`、`scripts/scan_ls_evidence.js`、`scripts/harden_ls_parse.js`
- 运维提示：本批修改了 `js/common.js`，正式部署前需由维护者执行 `python3 _build.py` 刷新 Service Worker 版本戳（本批按要求未跑、未 push）。
