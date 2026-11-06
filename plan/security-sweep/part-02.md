## 十一、Clarity 判定与移除（2026-11-04）

### 11.1 实测证据

- 探针页面：`it/hash.html`、`healthcare/egfr.html`、`finance/salary-after-tax.html`、`legal/will-template-generator.html`。
- 方法：真机无头 Chrome 输入哨兵串 `SENTINEL-7f3a`（数字控件用 `987654321`），同时在页面注入普通可见文本节点 `PLAINSENTINELabc9`；抓取 `*.clarity.ms/collect` 的 POST 体，按 gzip 解压后检索。
- 判定结果：
  - **普通可见文本 `PLAINSENTINELabc9` 原样出现在上传的 DOM 快照中** → Clarity 确实上传页面文本。
  - 表单控件快照中 `value=` 为空、`placeholder=` 显示为圆点，说明 SDK 会对输入框做本地掩码；但工具页把输入回显到普通 DOM（如 `it/hash` 的历史列表 `<span>`）时，回显文本以**明文**进入快照。
  - 哨兵串在 `it/hash.html` 的上传 payload 中被命中；脱敏只可能发生在服务端，客户端无法自证「未留存」。
- 结论：Clarity 与 `AGENTS.md` §2「禁止任何数据上传到服务器」冲突，**默认执行移除**。

### 11.2 处置

- 已从 `js/analytics.js` 移除 Clarity 初始化、`window.clarity` 桩、`tb-clarity-sdk` 加载，以及 `ToolBox.Analytics.track()` 内的 clarity 事件上报。
- 保留基础统计：51.la、百度统计、百度自动推送、TTZZ（仅页面上报，不含用户输入）。
- 清理验证（4 个哨兵页真机）：
  - `clarity.ms` 请求数 **0/0/0/0**；
  - `window.clarity` 全部为 `undefined`，`__tbClarityLoaded` 为 false；
  - 0 pageerror；
  - `#ttzz` 标签存在且 `push.js` 正常 GET；51.la `collect-v6.51.la`、百度 `hm.gif`、`zz.bdstatic.com/push.js` 均正常上报。

### 11.3 待办（阻塞项）

- **`js/analytics.js` 已改，但未运行构建**：SW 版本戳（`sw.js` 的 `const BUILD`）仍是旧值。
- **需集成线执行 `python3 _build.py` 后本次移除才会随 SW 版本更新生效**；在此之前，联网访问会因 `analytics.js` 网络优先策略即时拿到新文件，但离线/弱网回退仍可能命中旧缓存，且在旧 SW 完全失效前存在残留窗口。
- 恢复录屏分析前，必须先实现「客户端可验证的全量 mask」方案（例如 body 级 `data-clarity-mask` + 复测哨兵不出现在 payload），否则不得重新引入。

---

## 十二、CSP 试点结论（2026-11-04）

- 扫描全站 8344 个 HTML：**0 个工具页满足「无内联可执行脚本 + 无内联事件属性」**，因此无法在 `script-src 'self'` 下做无风险试点。
- 根页面中仅 `ByteDanceVerify.html`、`google*.html` 之类无脚本验证文件满足，但属平台验证文件，不适用 CSP。
- 可选方案与代价：
  - 保留 `'unsafe-inline'`：对 XSS 基本无防护价值，不做；
  - 构建期为内联脚本生成 nonce/hash，并把 `onclick` 等内联事件全部改为事件委托：改造面覆盖全站，暂不实施。
- 处置：**接受风险**，不新增 CSP meta；列入第十节第 10 条。后续若做，先从纯静态展示页（`about`/`privacy`/`404`）试点，再逐步推进工具页。

---

## 十三、上传回显与 iframe 全量结论（2026-11-04）

- **上传回显 55/55 全量完成**：对全部含 `input[type=file]` 的 55 个页面真机注入文件名 `x"><img src=x onerror=alert(1)>.png`，统一断言：
  - 0 弹窗、0 pageerror、0 个属性值含 `alert(1)` 的注入元素、0 个 `img[src="x"]`；
  - **55/55 通过，0 反例**。此前已修的 4 页（md5/sha/image-converter 等）也纳入复测。
- **iframe/srcdoc 全量排查**：全站仅 `tools/it/code-runner.html` 有真实 `<iframe>`；其 `sandbox="allow-scripts allow-modals"` **不含 `allow-same-origin`**，`srcdoc` 仅执行用户代码且隔离于父页面。其余页面无 `<iframe>`；`embed.html` 中的 iframe 示例为 HTML 转义展示文本，不构成实际嵌入。

---

## 十四、下一批方向：开头结论（2026-11-04）

1. **可通过 meta 设置的安全头覆盖**：8344 个 HTML 中，4680 个已有 `Referrer-Policy` + `X-Content-Type-Options`，4624 个另有 `Permissions-Policy`；**3664 个缺失**，集中在根页面（`about`/`404`/`search`/`sitemap`/`ui/*`）与各行业 `index.html` 分类页，工具详情页基本全覆盖。下一批可按「先补根页面与分类页」推进，风险低。
2. **`localStorage` 键名与敏感度**：工具页共 75 个唯一键，绝大多数为历史记录/最佳分数/主题/语言等中性名；`safety/manager.html` 的 `tb_pwd_master` / `tb_pwd_vault`（变量名定义，未进上表）是仅有的敏感命名，值为口令哈希与 XOR 密文、非明文。重命名会破坏既有用户数据，需迁移方案，列为后续评估项而非立即修改。
3. **用户输入拼进 `title`/`og:` 的隐蔽外泄**：全站扫描 `document.title = <变量>`、`meta[content]` 动态写入、`og:title` 动态赋值，**命中 0 处**；页面标题与分享 meta 均为静态文案，不存在「输入进 meta 再被分享/抓取」路径。

---

## 十五、第六批：meta 安全头 / localStorage 命名评估 / 下一批方向扫描（2026-11-04）

### 15.1 meta 安全头补齐（3664 → 0 缺失）

- 缺失结构：指南页 3410、行业分类索引 211、根页面 8、`ui/*` 9、零散工具页 26。
- 是否生成的判定：
  - **行业分类 `tools/<ind>/index.html`**：由 `_build.py::generate_category_indexes()` 每次重写 → 已直接改模板（追加三条 meta + `<!-- TOOLBOX-SECURITY -->`）。
  - **指南页**：由 `scripts/gen_guide_pages.py` 等生成 → 已改该模板；其余历史指南生成器由下面这条兜底。
  - **构建末尾新增统一兜底**：`_build.py` 调用 `scripts/security_meta.py::inject()`，对所有 HTML（含根页面、指南、ui、历史遗留页）按「缺则补」注入，幂等。
- 现存文件：用 `python3 scripts/security_meta.py` 一次性注入，重复执行结果一致；再次 `--check` 为 **missing=0**。
- 覆盖口径与既有 4680 页一致：`Referrer-Policy` + `X-Content-Type-Options` + `Permissions-Policy`。
- 门禁：`_test_static.py` exit 0；`_audit_assets.py --check` exit 0（0 缺 `<html lang>` / 0 重复 id）。
- **待办（需集成线构建）**：`zh-tw/` 繁体产物与 SW 版本戳需 `python3 _build.py` 后刷新；本次未跑构建。另有 4 个分类索引页（hr / nephrology / rehabilitation / sports）同时含其他线未提交改动，未纳入本批路径提交，构建后由模板自动覆盖。

### 15.2 localStorage 敏感键改名评估（结论：不改名）

对象：`tools/safety/manager.html` 的 `tb_pwd_master`（主口令校验哈希）与 `tb_pwd_vault`（条目密文）。

- **多标签页迁移竞态**：一次性「读旧键 → 写新键 → 删旧键」在 A/B 两个标签页同时打开时，B 可能仍以旧键为数据源写回，造成新键被旧数据覆盖或迁移后新写入丢失；本项目无跨标签锁机制，风险真实存在。
- **只读兼容**：若保留旧键只读，则「删除旧键」目标无法达成，等于长期双键并存，复杂度上升而无收益。
- **安全收益**：键名可被任意同源脚本/开发者工具枚举，改名不改变值的可读性；真正敏感的是值（当前为哈希与 XOR 密文），键名本身不泄露内容。
- **结论**：**不改名**。改名收益接近于 0，却引入用户数据丢失与迁移失败风险。当前值非明文；后续若升级加密方案，应连同值格式做一次性迁移，而不是仅重命名键。

### 15.3 下一批方向扫描结果

1. **`postMessage`**：命中 3 页。
   - `it/code-runner.html`：iframe → 父页使用 `targetOrigin="*"`，父页监听未校验 `event.source`；但只接受 `type:"console"` 并把 `data` 经 `escapeConsoleHtml` 转义后写入 `innerHTML`，`method` 仅拼进 class 名，无脚本执行路径 → **接受风险**（`*` 为 srcdoc 不透明源的必需写法）。
   - `it/regex.html`、`it/text-replace.html`：同源 Worker 的 `postMessage`，无跨窗口面 → **已确认安全**。
2. **`eval` / `new Function` / 字符串定时器**：仅 `it/math-evaluator.html` 仍运行时使用 `new Function`，但入口已做字符白名单 + 标识符白名单（仅数学函数/常量）+ 拒绝成员访问，`Math`、`constructor`、`this`、`arguments` 等均被拒 → **已确认安全**；`ai-code-review.html` 中的 `eval` 仅为检测规则与示例字符串，不执行。无 `setTimeout('string')` 命中。
3. **`document.write` / `innerHTML +=` 残余**：`document.write` 仅 2 页（`ophthalmology/amsler-grid-test.html`、`astigmatism-chart.html`）向新窗口打印报告，备注字段经 `esc()` 转义 → 安全。`innerHTML +=` 多为数值/静态常量拼接；抽查 `it/whitespace`（`escH`）、`medical2/surgery-duration`（`PROCEDURES` 常量）、`clinical-lab/blood-routine-reference`（`DATA` 常量）均无用户输入未转义路径，本批 **0 新命中**。
4. **CDN 版本锁定复核**：静态 HTML 内共 15 个 jsdelivr/unpkg/cdnjs 标签，**15/15 固定到确切版本、15/15 带 SRI，未固定 0 个**。剩余无法 SRI 的仅为运行时动态下发（pdf.js worker、transformers 模型分片、sql.js wasm、统计 SDK），已在第十节列明。
5. **密码管理器加密评估**：`manager.html` 的 XOR 密钥由主口令字节循环生成，**密钥不落 localStorage**；localStorage 仅存主口令校验哈希与 XOR 密文。XOR 流对已知明文攻击强度弱，但无固定密钥硬编码、密钥也不在本地持久层 → **接受风险**（页面已有本地演示警示）。

---

## 十六、第七批：AB 安全条目（2026-11-04）

### 16.1 SRI 口径统一（审计线「life 71 页缺 SRI」）

- **统一口径**：只有「静态 HTML 中的跨域 `<script src>`」需要 SRI；自站 `js/*.js`（同源）与运行时动态注入的第三方脚本不在此口径。
- **全站静态跨域 script 统计**：**需要 SRI 15 个 / 已带 SRI 15 个 / 缺失 0 个**（15/15 固定确切版本，无 `@latest`）。
- **审计线 71 页的来源**：`tools/life/*` 71 页全部含 TTZZ 统计脚本，但它是构建期写入的内联 JS，运行时用 `document.createElement("script")` + `el.src = "https://lf1-cdn-tos.bytegoofy.com/goofy/ttzz/push.js?<token>"` 动态插入（全站 8333 页同形态）。URL 带随机 token、内容随下发变化，**技术上无法计算稳定 SRI**，且不是静态 `<script src>`，不属于「需要 SRI」的统计范围。
- **处置**：不为 71 页静态加 SRI；TTZZ 作为已接受的运行时动态下发依赖，单列记录（与第十节 pdf.js worker / transformers / sql.js wasm 同口径）。

### 16.2 CSV 公式注入修复（含同族）

- **中心修复**：`js/tool-kit.js::exp.csv()` —— `TBKit.util.exportTable` / `exportCsv` 的唯一落地点，对以 `= + - @`、`\t`、`\r` 开头的单元格统一前置 `'`。一处覆盖 `data/`、`biz/`、`it/` 及全站所有走 TBKit 导出的 CSV 页面。
- **页面级修复（自建 Blob/文本导出）**：
  - `tools/it/csv-to-json.html`：新增 `csvExportSafe`，复制/下载用安全版，页面预览保持原始数据；
  - `tools/it/json-to-csv.html`：新增 `__jsonToCsvExportSafe`，复制/下载用安全版；
  - `tools/it/keyword-density.html`：导出前对词条加前缀。
  - `matrix-transpose`（仅数字）、`stopwatch` / `pomodoro`（仅数字/时长）经验证不含文本单元格，无需改动。
- 页面已加可见说明（`csv-to-json`、`json-to-csv`）：导出会给公式前缀加单引号。
- verify 新增两条：`it/json-to-csv`、`it/csv-to-json` 注入 `=cmd|' /C calc'!A0`，断言安全导出串以 `'=cmd|` 开头。

### 16.3 另外三条

- **`it/*` 密钥明文 localStorage**：全量检索 `localStorage` 键名与写入点，**未发现 API key/secret/token 持久化**；DES/Rabbit/HMAC/XOR 等加密工具的密钥字段无本页自动保存逻辑（`tb_uxp_` 持久化名单不含这些页面），密码类输入为 `type="password"` 且被持久化代码显式排除 → 无需改动。
- **`it/base64` 历史写入**：`addHistory()` 仅在用户点击编码/解码时调用，非加载即写；已有「清空历史」按钮 → 无需改动。
- **`it/json-formatter` 明文 JSON**：仅在用户输入事件后保存（非加载无条件写入）；`clearAll()` 之前只清空 textarea、不清 localStorage → 已补 `localStorage.removeItem('tb_uxp_tools/it/json-formatter.html#input')`，确保「清空」真正删除明文，并已有清空入口。

### 16.4 门禁与边界

- `node scripts/verify_it_calc.js it/csv-to-json it/json-to-csv` → **12/12 通过**。
- `node scripts/discriminate_check.js verify_it_calc.js` → 已检 896 / 正确变红 896 / 逃生项 0 / 跳过 1。
- `node scripts/selfcheck_false_pass.js scripts/verify_it_calc.js` → checked=897 risk=0 skipped=0。
- `python3 _test_static.py` → 通过 4705 / 失败 0。
- `python3 _audit_assets.py --check` → 0 死链 / 0 lang 缺失 / 0 重复 id。
- 未跑 `_build.py`、未 push；`js/tool-kit.js` 与页面改动需集成线构建后刷新 SW 版本戳与 `zh-tw/` 产物。

---

