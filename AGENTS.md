# AGENTS.md - ToolBox 项目 AI 开发约束

> **本文件只收录「AI Agent 开发本项目时必须遵守的硬性约束与坑点速查」。**
> 项目概览、设计规范、目录结构、新增工具模板、本地测试、开发流程等**文档性内容**一律在 **README.md**；本文件不重复。

---

## 🚫 硬性约束（必须遵守）

### 0. 动手前最高频红线（先记牢）

1. 改任何 `css/js/json` 前必须先 `python3 _build.py`（否则 Service Worker 旧缓存不失效）。
2. 凡引 `js/common.js` 的页面必须同时引 `js/i18n.js`（否则 `?lang=en-US` 整页回退中文）。
3. 改英文态字典 `i18n/tools/en/**` 后同样必须重跑 `_build.py` —— 该子树已纳入 SW 版本戳（`compute_sw_build()`），否则 `_swv` 不变、CDN 继续下发旧字典。
4. **收尾判定**：本地 `run_gates.py` 全过 + GitHub Actions 部署成功（单次查询）+ 抽样验证线上改动已生效。push 后先确认目标 commit `success`，再抽 3–6 个代表性 URL `curl -o` 落盘核对**本批关键内容确已出现**（英文态必须用真机探针 `scripts/_en_i18n_probe.mjs --check` —— 静态 HTML 不体现运行时替换）；判「生效」看**关键内容命中**，不看「页面能打开」。**仍禁止**全量逐文件 MD5 比对 / 逐 URL 打 200 / sleep 等 CDN 传播 / 循环轮询 API。不进构建产物的改动（`*.md` / memory 日志 / 门禁脚本注释）连部署都无需等待（口诀：**「会不会让线上页面变一个字节？会→等部署成功；不会→不等。」**）。

### 1. 纯前端原则

- **禁止**引入任何后端服务、API 调用（第三方 CDN 除外，但尽量避免）。
- 允许使用 npm/yarn/pnpm/bun 和前端构建工具；新增依赖必须锁定版本并说明用途。
- 可以使用 React/Vue/Vite 等框架，但发布产物必须是 GitHub Pages 可直接提供、搜索引擎无需执行应用脚本即可抓取正文的静态 HTML；不得只发布客户端空壳或 hash 路由。
- 所有工具的最终发布页必须可在浏览器中直接运行；动态 JSON 页面仍需通过 HTTP 服务访问。

#### ❌ 禁止开发的工具类型（需要后端服务）

实时数据类（天气/股票/汇率/加密货币/新闻）、位置服务类（地图/导航/GPS/物流）、社交媒体类（平台数据/分享/登录）、AI 服务类（聊天/生图/TTS/ASR/OCR）、第三方服务类（邮件/短信/支付/快递/航班）、数据库依赖类（品种/药品/保险/教育基金）。

#### ✅ 允许开发的工具类型（纯前端可用）

计算类、文本处理类、生成器类、速查表类、模拟类、文化类、生活工具类。

### 2. 数据安全原则

- **禁止**任何数据上传到服务器；所有计算/处理/存储都在浏览器本地完成。
- 使用 localStorage 做持久化，禁止使用 Cookie / IndexedDB（除非有充分理由）。

### 3. 目录结构约束

- 新工具必须放在 `tools/<industry>/` 对应行业子目录下；**禁止**在 `tools/` 根目录直接放 HTML 文件。
- 公共资源放在 `css/` / `js/` / `json/` 下。
- 下划线开头的根目录文件（如 `_build.py`、`_submit_*.py`）是开发/运维工具，**不要**随意删除或修改其命名（索引提交脚本被 crontab 定时任务依赖）。
- **新的开发脚本一律放 `scripts/` 子目录**，不要放根目录。

### 4. 构建系统约束

- 添加/修改工具后，**必须**运行 `python3 _build.py` 更新索引。
- 静态测试：`python3 _test_static.py` 必须 0 失败 0 告警；死链门禁：`python3 _audit_links.py --check` 必须 exit 0（0 死链，脚本已智能排除 `<script>/<style>` 块内教学示例与 JS 运行时伪链）；资产完整性门禁：`python3 _audit_assets.py --check` 必须 exit 0（0 局部资产死链 / 0 `<html lang>` 缺失 / 0 页面内重复 id）。
- **不要手动修改** `json/*.json` 和 `sitemap.xml`，它们是构建产物。
- **提交前必须最后跑一次 `python3 _build.py`**（改完 i18n / 数据源 / 工具页后，构建必须是提交前的最后一步）。反例（2026-09-12 fun 收口）：中文 title/intro 补齐后未重跑构建即提交 → 页面落盘为陈旧产物（`icon=🎮` 残留行业默认、JSON-LD `name` 残留英文占位），CI 从同一 HEAD 重建产出正确值 → **本地 MD5 ≠ 线上 MD5**。判定方法：从干净 HEAD 重跑 `_build.py`，若本地变为与线上一致，即为「提交前漏构建」。抽查派生字段：`meta[name=toolbox]` 的 `icon=`、JSON-LD `WebApplication.name`、`<title>`。
- **判定「计算类工具」（是否需要 formula-box）一律用客观口径：页面中 `type="number"` 的 input ≥2 → 计算类，必须有框；否则为交互 demo，豁免。严禁照抄行业 `cat` 字段做豁免**（见坑与速查「formula 计算类判定」）。补框时公式须逐条对照页面 `function calc()` 里的 `__vN = (表达式)` 撰写，杜绝错公式。
- 不要手动修改 `index.html` 中的工具列表/统计数据，它们由构建脚本注入。
- **所有公开页面必须引用 `/js/common.js`**（`js/common.js` 会在加载时兜底补引统一统计入口 `js/analytics.js`）。**例外：Google 站点验证文件（`google*.html`）不引入任何脚本、保持原样。**

#### 4.1 台湾繁体构建产物（重要）

- `zh-tw/` 是 `_build.py` 生成的完整静态站点，不是源代码；权威源仍是简体 HTML、i18n 配置和 OpenCC 覆盖词典。
- 根 `.gitignore` 必须持续包含 `/zh-tw/`，**禁止** `git add -f zh-tw/`、修改忽略规则或重新提交该目录。
- 本地调试应保留生成后的 `zh-tw/`；不要把删除它作为日常清理步骤。
- 首次克隆、目录缺失或源页面更新后，先运行 `python3 _build.py`；完整交付前运行 `python3 scripts/run_gates.py`，两者都会重新生成繁体站点。

#### 4.2 GitHub Pages Actions 发布（重要）

- GitHub 仓库 `Settings → Pages → Build and deployment → Source` 必须保持为 **GitHub Actions**，禁止切回 `Deploy from a branch`。
- `.github/workflows/quality-gates.yml` 是唯一 Pages 发布流程：pull request 只执行门禁，推送到 `master` 才构建、上传 artifact 并部署。
- Actions 必须先执行 `scripts/run_gates.py` 生成 `zh-tw/` 并通过全部门禁；任何门禁失败都不得上传或发布。
- 上传前必须移出 `node_modules`，并运行 `scripts/check_pages_artifact.py`；达到 900MiB 安全阈值时应失败，不能绕过检查。
- `actions/upload-pages-artifact` 必须保留隐藏文件以发布 `.nojekyll`，同时不得把 `.git`、`.github` 或依赖目录打进 Pages artifact。

#### 4.5 索引提交约定（重要）

- **不要自动执行**索引提交（全量跑约 19 分钟，拖慢会话）。
- 每次 `_build.py` 重建后，**只提醒用户手动运行** `python3 _submit_indexnow.py`。
- 定时任务已由用户终端 crontab 管理：IndexNow 14:00 / Bing 15:00 / GSC Sitemap 15:30 / GSC 收录监控 16:00。
- Bing URL API 必须保持小批量流式提交（当前默认 10 条/批），并按日期在 sitemap 正序/倒序之间轮换；禁止恢复为一次性万条批量提交。
- Bing 密钥必须通过 `BING_API_KEY` 环境变量注入，**禁止**把密钥写入仓库、日志、命令行参数或 crontab 命令文本。
- `_submit_bing_url_api.py` 必须先查询当日/月度剩余额度并据此限流；额度查询失败时安全停止，不得盲目继续。

#### 4.6 删除 / 迁移 URL 必须提交死链（重要，红线）

**凡删除工具页、或把工具迁移到新 URL（改名 / 行业转移 / 走 `TOOLBOX-REDIRECT` 重定向存根），旧 URL 失效后，必须主动通知 IndexNow——`TOOLBOX-REDIRECT` 重定向页（虽仍返回 200，但已 `noindex` 且移出 sitemap）**同样视为死链、必须提交**；否则搜索引擎长期保留旧地址、发出负面 SEO 信号。

- **适用场景**：① 直接 `git rm` 删除某工具页（真 404）；② 走 `TOOLBOX-REDIRECT` 存根机制把旧地址跳转到新地址（页面返回 200 但已 `noindex` 且移出 sitemap）。两种都算"旧 URL 不再作为正常收录页存在"，都必须通知。
- **必须调用**：`python3 _submit_indexnow_deadlinks.py`，把受影响旧 URL 列出来提交：
  - **真 404（直接删除）**：用默认校验即可——`python3 _submit_indexnow_deadlinks.py --file 死链列表.txt`（脚本会自动 HTTP 校验、只交确认死掉的、跳过仍存活页，防误删正常页索引）。
  - **迁移壳（`TOOLBOX-REDIRECT` 存根，页面仍 200）**：加 `--no-verify` 强制提交——`python3 _submit_indexnow_deadlinks.py --file 死链列表.txt --no-verify`。
  - 也支持 `--url https://…` 单次提交，或从 stdin 传入。
- **时机（分两种，务必区分）**：
  - **迁移壳（`TOOLBOX-REDIRECT` 存根，页面仍 200）**：用 `--no-verify`，提交时机可在 `git commit` 之前（或随批），不依赖线上状态。
  - **真 404 物理删除（`git rm` 直接删页）**：**必须等线上部署成功（Actions run `success`）之后，再用默认校验提交一次死链**——`python3 _submit_indexnow_deadlinks.py --file 死链列表.txt`（不加 `--no-verify`）。**严禁在部署成功前提交**：此时线上仍跑旧部署、旧 URL 仍是 200，默认校验会误判"存活"而跳过，导致死链漏提。即规则闭环：**物理删除 → 提交并 push → 确认部署 success → 再提交一次死链（默认校验）**。
- **批量迁移工具**：先把全站 `TOOLBOX-REDIRECT` 标记的旧 URL 捞出来（简体 + `zh-tw/` 繁体，过滤已在 sitemap 收录的），生成列表再一次性提交，避免遗漏。
- **重定向存根保留期限（硬性）**：`TOOLBOX-REDIRECT` 存根只是**临时过渡**，最长保留 **1 个月**，到期必须物理删除（旧 URL 真正 404），**不得无限期保留**。删除前/删除时仍须按本节约提死链（此时旧 URL 已是真 404，用默认校验提交即可）。**建重定向存根的同一批次，必须**：① 同步用 `--no-verify` 把旧 URL（含 `zh-tw/` 繁体对应页）提死链；② **登记到仓库根目录 `_redirect_stubs_todo.md`**（统一维护所有待删存根的「源 URL / 目标 URL / 建存根日期 / 到期日 / 状态」），到期由维护者**主动删除**，**不依赖定时任务**，确保不漏。
- 该脚本已 commit 入库，属运维工具、被手动触发依赖，勿随意删除或改名。

- **迁移后新 URL 也必须提交收录通知（含繁体）**：删除/迁移只提旧 URL 死链不够——搜索引擎只知道"旧地址没了"，未必及时发现"新地址在哪"。**真迁移（`git mv` 到新路径）的目标页，与 `TOOLBOX-REDIRECT` 存根跳转的「目标 URL」，都必须随批用 IndexNow + Bing SubmitUrlbatch 各提交一次**，让 Bing 重新发现并收录新位置，完成「旧 URL 掉收录 + 新 URL 入收录」闭环。通道：① IndexNow（`_submit_indexnow.py` 走 sitemap 全量；针对特定新 URL 直接用 `https://api.indexnow.org/IndexNow` 投递 `urlList`）；② Bing Webmaster `SubmitUrlbatch`（`_submit_bing_url_api.py`，读 sitemap 批量）。**每条 URL 都须同时生成简体 `tools/X.html` 与繁体 `zh-tw/tools/X.html` 两个变体一并提交**（key 走脚本既有配置 / 环境变量注入，禁止明文入库，见 §3 密钥纪律）。

### 5. 兼容性约束

- 不要使用过于激进的新特性，确保主流浏览器（Chrome/Safari/Firefox/Edge 最近两个大版本）可用。
- CSS 优先使用变量（CSS Variables），不要硬编码颜色值。
- 移动端必须可用，不能只做桌面端。

### 6. 单 Agent 串行执行（禁止多 Agent 并行）

**本项目同一时刻只允许一个 agent 对仓库做写操作，全部任务由主 agent 串行推进，一个干完再干下一个。**

- **禁止**为同一批任务派生多个子 agent / 后台 agent 并行干活（包括并行写文件、并行跑 `_build.py`、并行 commit）。
- **禁止**创建多 agent 团队（`TeamCreate` / teammate 分工）并发修改本仓库。
- **主 agent 自顶向下串行执行**：一个子任务完整收口（改完 → 跑通门禁 → 提交）后，才允许开始下一个子任务，禁止中途开第二条线。
- 唯一例外：**纯只读**的检索/探查类子任务可并行；一旦涉及写入，一律回到串行。拿不准时按串行处理。

**为什么必须串行**：`_build.py` 全量重写构建产物，并发跑会互相覆盖；多 agent 同时 `git add/commit` 会触发 `.git/index.lock` 冲突；门禁结果依赖稳定工作区；批量改动要求合并提交，并行会让历史碎片化。

**与自动化任务的互斥**：定时看门狗等自动化 agent 与人工会话共用本仓库，靠 `.workbuddy/watchdog.lock`（含 `started_at` / `last_heartbeat` / `run_id`）互斥——检测到心跳仍在有效期即视为"另有 agent 在干"，本次直接跳过，不碰代码、不动 git。任何新增的自动化任务必须遵守同一把锁。

### 7. 文件名 / URL 稳定性优先（禁止因"名不符实"改名）

**核心：文件名 = URL = SEO 资产。改动文件名会让已收录 URL 失效（404 / 需重定向），代价远大于"名字不好看"。**

- **禁止**仅因「文件名与工具标题/功能不符」而重命名文件。例：`analysis-14.html` 标题是"结核耐药分析"、内容是占位页 —— 正确做法是**把内容改成名副其实的工具**，而不是把文件改名。
- **唯一允许改名的场景**：分类转移（行业归属错误）时，目标目录**已存在同名文件**产生冲突。此时只改**被转移的那个文件**，且必须按「下架/改名清理清单」同步 i18n 双键、`js/tool-i18n-en.js` 行级、`json/tools.json`、本地 `zh-tw/` 产物。
- 改名必须走项目已有的 `TOOLBOX-REDIRECT` 存根机制保留旧 URL，不得直接删除造成 404。**建好存根后，必须按 §4.6 调用 `python3 _submit_indexnow_deadlinks.py --no-verify` 把旧 URL 提交 IndexNow。**
- 内容层面的「名不符实」缺陷（如通用统计模板占位页）**一律通过重写页面内容解决**，保留原 URL。

---

## ⚠️ 新增工具强制约束

> 模板与完整 howto 见 README.md「新增工具规范」；此处只列**不可省略的强制项**，漏做即视为工具未完成。

- **`<meta name="toolbox">` 必须有**（含 `cat` / `industry` / `icon` / `bg`），否则构建脚本无法正确分类。
- **中英文与指南三项同步（强制，缺一不可）**：① 中文工具页；② 英文 i18n 双轨（`i18n/tools/slug-en.json` 写卡片名 + `i18n/tools/_en_override.json` 写标题/简介，值必须嵌套 dict `{en, ed, ind}`，**绝不能写成字符串**，否则 `_build.py apply_en_override` 报 `AttributeError`）;③ 使用指南 `guides/<slug>-guide.html`（合并进 `json/guides.json`，向 `js/guide-en-pack.js` 导出英文键，指南"去使用"链接的 `tools/<industry>/` 须与工具页真实目录一致）。
- **禁止因名不符实改名**（见 §7）：内容不符就改内容，不要改文件名。

---

## ⚠️ 项目特有坑与速查（Agent 必读）

> 本节收录长期实践中反复踩到、且无法从代码或其它文档直接推断的坑。改动相关模块前先读本节。

### 构建与缓存

- 改任何 `css/js/json` 都必须先跑 `python3 _build.py`：Service Worker 的 BUILD 戳按内容 hash 注入，不重建则旧缓存永不失效。
- 构建幂等：只读 `git --no-optional-locks status`；撞 `.git/index.lock` 用 `rm -f .git/index.lock`。
- 构建产物变化一律**全量核对随提交**，禁止只挑部分文件回退；新建文件前先确认是否已存在（曾发生 Write 覆盖）。
- SW v4 分三桶（`tb-shell-v4` / `tb-rt-v4-<BUILD>` / `tb-tools-v4-<BUILD>`）：CSS/JS/JSON 网络优先 3s 回退、图片字体 cache-first；紧急开关 `sw-kill.json` = `{"disabled":true}`。
- 统计统一收口 `js/analytics.js`（引 `common.js` 即自动获得，勿再单独引）。
- **手改工具页后第一次 `_build.py` 会「一次性大改写」该页并冲掉手改内容**（相关工具重算 + 索引重建），第二次起才幂等。判据：插入 \`\` 标记再构建，标记存活即证明构建本身不清除该区域。**对策：手改 → 构建 → 必须复查改动存活**（`grep -c` 关键串），被冲掉就把全部改动写进一个**幂等 apply 脚本**重跑，不要逐次手补。
- **`<h1 class="sr-only">`、`bc-current` 面包屑、面包屑 JSON-LD 是「只写一次」字段**：构建仅在缺失时注入，已存在则不刷新。改工具名必须**同时**改 i18n 字典（`i18n/tools/<行业>.json` 的 `title`/`h1`）+ `json/tools.json` 的 `name` + 页面磁盘里的 h1/面包屑/JSON-LD，`<title>`/`og:title`/WebApplication `name` 则由构建每次刷新。

### 页面内容与 \_build.py 的交互（逐分类推进必读）

- **`_prerender_tool_body` 只处理文档首个 `<p>`（`count=1`）**，且仅当正文含 CJK 时才用 `i18n/tools/<ind>-body.json` 的 `intro` 覆盖正文、原文写入 `data-zh`。由此产生三个必踩陷阱：
  - **插在首个 `<p>` 之前的中文 `<p>` 会被覆盖**：把 `formula-desc`（中文）放在工具标题 `<h2>` 后，它就成为首个 `<p>`，被 body JSON 的 intro 覆盖；若该条目 intro 仍是占位串，页面即显示占位（曾一次回归 128 处）。**解法：这类说明块用 `<div class="formula-desc">` 而非 `<p>`** —— build 只认 `<p>`，CSS 为 `.formula-box .formula-desc { margin:0 }`，换标签渲染一致。
  - **首个 `<p>` 若是 JS 字符串里的 `<p …>`**（错误提示 / 空状态，英文无 CJK），build 匹配它后即跳过，真正的中文 intro 永远拿不到英文注入（13 个统计类工具踩过）→ 解法：直接把源 intro 改为 `<p data-zh="中文">真实英文</p>`，不要指望 body JSON 注入。
  - **空壳 `<p class="formula-desc"></p>` 会「吸收」这次 `count=1`**，使其后的中文 intro 侥幸躲过预渲染；一旦改成 div 或填入中文，这批会集中暴露（53 个工具踩过）→ 推进时应主动全量补齐这些 intro，别依赖这个巧合。
- **终端审计不能只看文本长度**：占位串本身也有 80+ 字，仅判「≥80 字」会得到假绿（曾出现「345/345 合格」实为占位）。必须**同时**查占位指纹（如 `is available directly in your browser, with no data uploaded.`）与套话指纹（如「本速查内容依据权威标准」「本计算基于标准数学定义」）。
- **英文 p 三种来源机制不同，改错位置会被 build 还原**：① `data-zh` 机制 → 改源 html，安全持久；② `data-i18n` 机制 → 由 build 从 `<ind>-body.json` 注入，手改源 html 无效，**必须改数据源**；③ 中文 intro → build 注入或改源。
- **替换 JS 字符串里的占位必须替换「含工具名的整短语」**（如 `Statistical Power is available directly…`）。只替换核心句会残留工具名前缀，显示成 `Bayes Theorem Please enter valid parameters.` 这类串味文本。另：`re.sub` 的替换串里不要写 `\x27`（会报 `bad escape \x`），改用 `str.replace()` 最稳。

### i18n（中英 / 繁体）

- **凡引 `js/common.js` 的页面必须同时引 `js/i18n.js`**，否则 `?lang=en-US` 下整页回退中文；`guides/*.html` 等静态页须手动保留，幂等补注脚本 `scripts/inject_i18n_js.py`（正则须吞掉 `</script>`，否则插入标签不闭合）。
- `I18n.apply(root)` **只扫描 root 的后代、不含 root 自身** —— 给 root 自身带 `data-i18n` 的元素必须显式调 `I18n.t()`。
- `i18n.js` 以 defer 加载，**同步内联脚本早于它执行**：依赖 I18n 的渲染（如 404 的热门工具/分类）必须延后到 `DOMContentLoaded`。
- `i18n.js` 的 `ind_*` 键仅数十个而行业有 209 个 → 分类页行业名**不要用 `ind_*`**，改用构建期双语层（`i18n/industry-en.json` 全覆盖 + `.t-zh/.t-en` + CSS `html[lang]` 显隐）；双语容器为 `.cat-tool` / `.tb-bi` / `.tool-intro` / `.tool-link`，分类页正文由 `scripts/category_auto_content.py` 生成。
- 英文态排查判据（`?lang=en-US`）：① `[data-i18n]` 元素运行后仍含汉字 = 字典缺键或未加载；② 可见文本含汉字 —— **必须**用 `getClientRects().length === 0` 排除 CSS 隐藏的 `.t-zh`，否则大量误报。
- 繁体页核验必须**源页配对**（`conv(源页值)` vs 繁体页值）：直接对繁体页做转换属二次转换，`twp` 非幂等（文档→文件→檔案）会大量误报；判字形残留用 OpenCC `tw` 而非 `twp`；`data-zh` / `data-i18n-*-fb` 保留简体是运行时回退设计，不是残留。
- **英文内容区（`?lang=en-US`）走三层运行时字典，全部非构建产物**：① `js/tool-i18n-en.js`（`GEN_UI_MAP` 通用 UI + `BODY_PHRASE_MAP` 全站短语）；② `i18n/tools/<ind>-phrases.json` / `<ind>-body.json`（行业层）；③ `i18n/tools/en/<ind>/<slug>.json`（**一个工具一个文件**，优先级最高，`map` 为「简体原文 → 英文」译文），配 `_index.json` 资源守卫与 `en/_common.json` 共享层。**新增或修改第三层后必须重跑 `_build.py`**（版本戳已纳入该子树，见红线 3）。
- **第三层字典的匹配口径**：运行时按 `el.textContent.trim()` 查表（key 与原文都 trim）；`[data-zh]` 元素用 `el.textContent = tr`，普通文本节点用 `raw.slice(0,idx) + en + raw.slice(idx+k.length)` 保留 DOM 与内链。碎片节点的译文必须带 DOM 空白约定（`"：xxx"`、`"（…）而非"`）。孤立中文标点由运行时字符级 `convertPunct()` 兜底（判据：含中文标点且不含汉字）。
- **`translateBodyPhrases()` 禁止对含表单控件的容器做整节点 `textContent` 替换**：那会把容器内 `input`/`select`/`textarea` 一起删除，页面随后 `getElementById(id).value` 抛 `Cannot read properties of null`（英文态实测 7 页中招，简体/繁体态不跑运行时 i18n 故不受影响）。守卫条件：元素有子元素**且** `querySelector('input,select,textarea')` 非空则跳过，该段正文交第三层文本节点级替换处理。
- **英文文案统一美式拼写**（`color` / `center` / `favor` / `customize` / `summarize` / `fulfillment` / `jewelry`）。批量替换时**警惕规则自污染**：`fulfilment→fulfillment` 之后再跑 `fulfil→fulfill` 会得到三写 `fulfilllment` ⇒ 替换对须「长词优先 + 短词加否定前瞻」，扫描词表同样要写 `fulfil(?!l)`，否则美式 `fulfillment` 会被 `fulfil\w*` 误报。

### 内容质量

- **A 级硬标准**：`own_len ≥ 6000`，或 `≥ 3000 且 inputs ≥ 3`；含 `formula-box` / `canvas` / `data-viz` 直接判 A；**禁止用代码膨胀凑数**。
- **`own_len` 度量口径**（`_build.py::classify_quality`）：非共享内联 `<script>` + 外置 `/js/tools/*.js` + **`<script type="module">` 内联块**（2026-10-12 修正，此前漏算致 ai 5 个浏览器本地 AI 页评级失真）；均走 shared md5 去重。新增 module 脚本页无须为提级凑数，逻辑真实即计。
- **head-only 死壳**特征：`<body>` 无开标签 / 无 `input`+`select` / deep-dive 段误置 `<head>`（线上打开空白）。扫法 `'<body>' not in c`；重建库 `scripts/auto_shell_lib.py` + `rebuild_<cat>_batchN.py`；收口前必做三方终检（title = h1 = i18n 标题、deep-dive 仅注入 body、每页有输入控件）。
- **两套套话残留**（逐分类必查）：① 可见 `opt-guide` / `opt-faq` → `scripts/opt_cleanup_opt_blocks.py --cat X`；② FAQPage JSON-LD 里的旧套话 → `scripts/opt_faq_ld_sync.py --cat X`。**_build.py 不重建工具页的 FAQPage LD**，必须手改并 `json.loads` 校验。
- deep-dive 算例数字一律用 node 实跑取（含 `toFixed` 四舍五入），禁止凭印象写。
- `i18n/tools/content_deepdive.json` 仓库规范 `indent=1`（`_build.py` 只读不写），apply 脚本必须 `json.dump(indent=1)`，否则全量重排成巨大噪音 diff。
- **defer 脚本闭包死引用**：`common.js` 整体替换后旧 stub 引用失效 → 「📋复制 / ⬇️导出」点击无反应。根治方式为替换前保存旧对象、替换后回填同名方法指向真实实现；审计脚本 `scripts/audit_toolbox_stub_refs.py`。
- **淘宝客双链**：PC 链 `s.click.taobao.com/UItQ6Hk`、WAP 免登录链 `s.click.taobao.com/5e6P6Hk`；手机上打开 PC 链会被强制登录 → 转化归零。全站唯一维护点 `js/common.js` 的 `toolboxTaobaoAdUrl()`（断点 `innerWidth < 768`），禁止再硬编码。
- `scripts/gen_guide_pages.py`：`guides/index.html` 是纯追加（不按 slug 去重），重生成同 slug 会在指南中心重复卡片；重跑前先按行删掉该 slug 旧卡片。

### 无头浏览器验证

- Chrome 绝对路径 `/Applications/Google Chrome.app/Contents/MacOS/Google Chrome`（不在 PATH）；`puppeteer-core` 用 managed 绝对路径 require；启动参数 `headless:'new'` + `--no-sandbox --disable-setuid-sandbox --disable-dev-shm-usage`。
- 本地服务 `python3 -m http.server 8137 --directory <项目根>`（后台），用完 `pkill -f "http.server 8137"`。
- 须真触发事件（`.tb-nav-link` click 才生成 megapanel）；繁体页 `set()` 会整页跳转，`goto` 后轮询 `page.url()` 稳定后再 evaluate。

### verify 脚本口径（`scripts/verify_*_calc.js`）

- **`collectStrings` 只对 `innerHTML` / `textContent` 剥 HTML 标签，`el.value` 保留原文**（2026-09-28 修正）—— `value` 恒为纯文本，对它剥标签会把尖括号形态的结果整块吞掉（`it/base85-encode` 的 `<~BOu!rDZ~>` 此前永远匹配不上，而页面本身正确）。改动该函数会波及全站用例口径，**必须重跑 `run_gates.py` 的 `selfcheck_false_pass` / `discriminate_check` 两项**确认逃生项与弱用例基线未变。
- **逃生项新判据**：`expect` 恰好等于「`inputs` 各值经剥标签 + 空白归一」的形态即逃生项（`it/html-minifier` 原 `expect:["a b"]`，而输入 `<p>a</p>` + 换行 + `<p>b</p>` 归一后正是 `a b`）⇒ 定 expect 前先把注入输入按该口径跑一遍比对。
- **HTML 里带 `checked` 的 checkbox 在桩内恒 `false`**（真机默认勾选）⇒ 必须用 `checkIds` 显式还原真机默认态，否则页面走「开关全假」分支、输出恒等于输入（`it/html-minifier` 即因此退化成回显）。
- **循环体内无任何推进语句 = 真死循环**：`it/docker-run-converter` 的 `parse()` 在 image 已赋值时不递增 `i`，遇尾参（`docker run -it --rm alpine sh`）即无限循环冻死标签页，已修。判据：循环体含 `i++` / 赋值 / `next()` 任一即安全。全站 `while` 已扫（512 处，仅此 1 例）。
- **烟测 ⚠️「点击了 N 个按钮但无输出变化」≠ 页面缺陷**：若页面在加载时就执行过同名初始化（如 `it/calc-7` 末尾直接调 `loadSample()`），再点同一按钮内容自然不变。判定真伪先看页面末尾有无直接调用。

---

---

> **最后更新**：2026-10-11（结构调整：文档性内容迁至 README.md，本文件只保留 AI 开发约束与坑点速查）
> 本文件是 AI 开发本项目的约束权威；如有疑问以本文件为准，上下文文档见 README.md。
