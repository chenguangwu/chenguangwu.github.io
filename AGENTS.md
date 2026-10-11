# AGENTS.md - ToolBox 项目 AI 开发规范

> **重要**：所有 AI Agent 在开发本项目时，必须严格遵守本文件中的约束和规范。

---

## 📋 项目概览

**项目名称**：ToolBox - 免费在线工具百科

**技术栈**：纯前端 HTML5 + CSS3 变量主题 + 原生 ES6 JavaScript + Python/Node.js 构建脚本

**部署方式**：GitHub Actions 构建后上传静态 artifact，由 GitHub Pages 发布（`.nojekyll` 强制纯静态直发）

**核心特性**：
- 响应式设计（桌面 + 移动端底部 Tab 栏）
- 数千个工具，209 个子行业目录（以 `_build.py` 实时统计为准）
- 纯前端处理，数据不上传
- AI 工具（浏览器本地推理）、工具链组合、中英双语 i18n、PWA 离线、质量分级

> ⚡ **动手前必读**：文末「**§ 项目特有坑与速查**」记录了反复踩到、且无法从代码推断的坑。四条最高频红线先记牢：
> 1. 改任何 `css/js/json` 前必须先 `python3 _build.py`（否则 SW 旧缓存不失效）
> 2. 凡引 `js/common.js` 的页面必须同时引 `js/i18n.js`（否则 `?lang=en-US` 整页回退中文）
> 3. 改动英文内容字典 `i18n/tools/en/**` 后同样必须重跑 `_build.py` —— 该子树已纳入 SW 版本戳（`compute_sw_build()`）
> 4. **收尾判定：本地 `run_gates.py` 全过 + GitHub Actions 部署成功（单次查询）+ 抽样验证线上改动已生效**。push 后先确认目标 commit `success`，再抽 3–6 个代表性 URL `curl -o` 落盘核对**本批关键内容确已出现**（英文态必须用真机探针 `scripts/_en_i18n_probe.mjs --check`）。**仍禁止**全量逐文件 MD5 比对 / 逐 URL 打 200 / sleep 等 CDN 传播 / 循环轮询 API。不进构建产物的改动（`*.md` / memory 日志）连部署都无需等待

---

## 🎨 设计规范（必须遵守）

> **重要**：所有 UI 开发必须遵循 `ui/设计规范.md` 中的完整设计规范。

### 色彩系统

| 色彩名称 | 变量名 | Hex 值 | 用途 |
|----------|--------|--------|------|
| 主色 Primary | `--color-primary` | `#FF6B35` | 主按钮、关键操作、高亮强调 |
| 辅色 Secondary | `--color-secondary` | `#7C3AED` | 副功能区、标签、装饰元素 |
| 强调色 Accent | `--color-accent` | `#00C9A7` | 成功态装饰、进度指示 |
| 背景色 Background | `--color-bg` | `#FFFAF7` | 页面底层背景 |
| 文字主色 | `--color-text-primary` | `#1F2937` | 标题、正文主体 |
| 文字次色 | `--color-text-secondary` | `#6B7280` | 说明文字、次要信息 |
| 边框色 | `--color-border` | `#E5E7EB` | 分割线、输入框边框 |
| 卡片背景 | `--color-card` | `#FFFFFF` | 卡片、面板背景 |

### 功能色

| 语义 | Hex 值 | 浅色背景 | 用途 |
|------|--------|----------|------|
| 成功 | `#10B981` | `rgba(16,185,129,0.10)` | 操作成功、复制完成 |
| 警告 | `#F59E0B` | `rgba(245,158,11,0.10)` | 注意事项 |
| 错误 | `#EF4444` | `rgba(239,68,68,0.10)` | 输入错误、操作失败 |
| 信息 | `#3B82F6` | `rgba(59,130,246,0.10)` | 提示信息 |

### 渐变 / 圆角 / 技术栈
- 渐变：`--gradient-primary: linear-gradient(135deg,#FF6B35,#7C3AED)`；`--gradient-hero`/`--gradient-btn-hover` 见设计规范
- 圆角：按钮/输入框 12px(`rounded-xl`)、卡片 16px(`rounded-2xl`)、标签全圆(`rounded-full`)、模态 24px(`rounded-3xl`)
- 技术栈：Tailwind CSS v4 Browser CDN + Lucide Icons（`<data-lucide>` 声明）+ 字体 Noto Sans SC / Plus Jakarta Sans

---

## 🏗️ 目录结构（严格遵守）

```
chenguangwu.github.io/
├── index.html              # 首页入口（侧边栏布局）
├── css/
│   ├── style.css           # 首页样式（侧边栏布局、响应式）
│   ├── site-chrome.css     # 顶栏 / 页脚 / Tab 栏 / 回顶按钮的唯一样式源（首页与工具页共用）
│   ├── common.css          # 工具页公共样式（所有工具共用，经 @import 引入 site-chrome.css）
│   ├── home-categories.css # 首页分类导航样式
│   └── nav-menu.css        # 全站 2 级分类导航样式（桌面下拉 + 移动抽屉）
├── js/
│   ├── app.js              # 首页逻辑（动态加载、侧边栏交互）
│   ├── common.js           # 工具页公共脚本（ToolBox 命名空间，引即自动补 analytics.js）
│   ├── i18n.js             # 中英双语 i18n 引擎（全站共用）
│   ├── tool-i18n.js        # 工具页内容区 i18n 运行时（依赖 i18n.js）
│   ├── tool-i18n-en.js     # 全站通用英文层（GEN_UI_MAP + BODY_PHRASE_MAP）
│   ├── tool-search.js      # 全站统一实时下拉搜索
│   ├── analytics.js        # 统一统计入口（百度 / Clarity / 51.la）
│   ├── freemium.js         # Freemium：AI 工具每日限额 + 解锁
│   ├── ai-core.js          # Transformers.js 纯前端 AI 共享加载器
│   ├── chart.js            # 零依赖 Canvas 图表库（懒加载）
│   └── qrcode.js           # 二维码库（第三方，MIT）
├── json/
│   ├── tools.json          # 全量工具数据（含搜索字段 al/py/pyi，搜索单一数据源）
│   ├── industry-*.json     # 按行业拆分数据（与子行业目录一一对应）
│   ├── guides.json         # 工具 ↔ 使用指南配对
│   └── hot-tools.json      # 热门工具清单（首页 / 404 消费）
├── tools/                  # 工具页面（按子行业分子目录组织）
│   ├── <industry>/index.html   # 每个子行业目录下的分类落地页（构建脚本自动生成）
│   └── <industry>/<slug>.html  # 工具页
├── guides/                 # 使用指南页集合（含 index.html 指南中心）
├── scripts/                # 开发/生成脚本（批量生成、SEO 审计修复、指南生成等）
├── chains.html / search.html   # 工具链组合页 / 站内搜索页
├── _build.py               # 构建脚本（最重要，含 SEO/结构化数据/面包屑注入）
├── _test_static.py         # 静态测试（标题/元数据/结构合规）
├── _submit_indexnow.py / _submit_bing_url_api.py / _gsc_submit_sitemap.py / _gsc_inspect_urls.py / _submit_indexnow_deadlinks.py  # 索引提交（crontab 依赖，勿随意删/改名）
├── sitemap.xml / sitemap.html / robots.txt   # 构建产物 / 爬虫规则
└── og-image.png            # 1200×630 社交分享图（全站 og:image 引用，勿删）
```

---

## 🚫 硬性约束（必须遵守）

### 1. 纯前端原则
- **禁止**引入任何后端服务、API 调用（第三方 CDN 除外，但尽量避免）
- 允许使用 npm/yarn/pnpm/bun 和前端构建工具；新增依赖必须锁定版本并说明用途。
- 可以使用 React/Vue/Vite 等框架，但发布产物必须是 GitHub Pages 可直接提供、搜索引擎无需执行应用脚本即可抓取正文的静态 HTML；不得只发布客户端空壳或 hash 路由。
- 所有工具的最终发布页必须可在浏览器中直接运行；动态 JSON 页面仍需通过 HTTP 服务访问。

#### ❌ 禁止开发的工具类型（需要后端服务）
以下类型的工具需要后端 API 或实时数据，禁止添加：
- **实时数据类**：天气预报、股票行情、汇率换算、加密货币价格、新闻资讯
- **位置服务类**：地图导航、路线规划、GPS 定位、附近搜索、物流追踪
- **社交媒体类**：微信/微博/抖音等平台数据、分享功能、登录认证
- **AI 服务类**：AI 聊天、AI 生图、语音识别(TTS/ASR)、OCR 识别
- **第三方服务类**：邮件发送、短信验证、支付接口、快递查询、航班查询
- **数据库依赖类**：品种数据库、药品数据库、保险报价、教育基金

#### ✅ 允许开发的工具类型（纯前端可用）
- **计算类**：各种计算器、公式计算、单位换算、成本估算
- **文本处理类**：格式化、编码解码、加密解密、正则匹配
- **生成器类**：密码生成、二维码生成、UUID 生成、随机数据生成
- **速查表类**：API 文档、语法参考、数据字典、知识查询
- **模拟类**：抛硬币、骰子、抽奖、概率计算
- **文化类**：汉字查询、诗词搜索、成语词典、周易八卦
- **生活工具类**：BMI 计算、预产期计算、食谱推荐、园艺工具

### 2. 数据安全原则
- **禁止**任何数据上传到服务器
- 所有计算、处理、存储都在浏览器本地完成
- 使用 localStorage 做持久化，禁止使用 Cookie / IndexedDB（除非有充分理由）

### 3. 目录结构约束
- 新工具必须放在 `tools/<industry>/` 对应行业子目录下
- **禁止**在 `tools/` 根目录直接放 HTML 文件
- 公共资源放在 `css/` / `js/` / `json/` 下，不要乱放
- 下划线开头的根目录文件（如 `_build.py`、`_submit_*.py`）是开发/运维工具，**不要**随意删除或修改其命名（索引提交脚本被 crontab 定时任务依赖）
- **新的开发脚本一律放 `scripts/` 子目录**（批量生成器/审计/修复等），不要用第三方依赖污染环境；Python 脚本只用标准库
- 统计统一收口 `js/analytics.js`，勿再单独引

### 4. 构建系统约束
- 添加/修改工具后，**必须**运行 `python3 _build.py` 更新索引
- 静态测试：`python3 _test_static.py` 必须 0 失败 0 告警
- 死链门禁：`python3 _audit_links.py --check` 必须 exit 0（0 死链）。该脚本智能排除 `<script>/<style>` 块内的教学示例与 JS 运行时伪链（`$1`/`${}`），避免误报；发布前必须跑通
- 资产完整性门禁：`python3 _audit_assets.py --check` 必须 exit 0（0 局部资产死链 / 0 `<html lang>` 缺失 / 0 页面内重复 id）
- **不要手动修改** `json/*.json` 和 `sitemap.xml`，它们是构建产物
- **提交前必须最后跑一次 `python3 _build.py`**（改完 i18n / 数据源 / 工具页后，构建必须是提交前的最后一步）。反例（2026-09-12 fun 收口）：中文 title/intro 补齐后未重跑构建即提交 → 页面落盘为陈旧产物。抽查派生字段：`meta[name=toolbox]` 的 `icon=`、JSON-LD `WebApplication.name`、`<title>`。
- **判定「计算类工具」（是否需要 formula-box）一律用客观口径：页面中 `type="number"` 的 input ≥2 → 计算类，必须有框；否则为交互 demo，豁免。严禁照抄行业 `cat` 字段做豁免**。
- 不要手动修改 `index.html` 中的工具列表/统计数据，它们由构建脚本注入
- **所有公开页面必须引用 `/js/common.js`**（工具页/行业落地页/首页由 `_build.py` 统一注入；guides/静态页等非 `_build.py` 处理的页面须手动保留该引用，遗漏可用 `python3 scripts/inject_common_js.py` 幂等补全）。**例外：Google 站点验证文件（`google*.html`）不引入任何脚本、保持原样。**

### 4.1 台湾繁体构建产物（重要）
- `zh-tw/` 是 `_build.py` 生成的完整静态站点，不是源代码；权威源仍是简体 HTML、i18n 配置和 OpenCC 覆盖词典。
- 根 `.gitignore` 必须持续包含 `/zh-tw/`，**禁止** `git add -f zh-tw/`、修改忽略规则或重新提交该目录。
- 本地调试应保留生成后的 `zh-tw/`，不要把删除它作为日常清理步骤。
- 首次克隆、目录缺失或源页面更新后先运行 `python3 _build.py`；完整交付前运行 `python3 scripts/run_gates.py`，两者都会重新生成繁体站点。

### 4.2 GitHub Pages Actions 发布（重要）
- GitHub 仓库 `Settings → Pages → Source` 必须保持为 **GitHub Actions**，禁止切回 `Deploy from a branch`。
- `.github/workflows/quality-gates.yml` 是唯一 Pages 发布流程：pull request 只执行门禁，推送到 `master` 才构建、上传 artifact 并部署。
- Actions 必须先执行 `scripts/run_gates.py` 生成 `zh-tw/` 并通过全部门禁；任何门禁失败都不得上传或发布。
- 上传前必须移出 `node_modules`，并运行 `scripts/check_pages_artifact.py`；达到 900MiB 安全阈值时应失败，不能绕过检查。
- **发布完成后**：先单次查询确认 Actions run 为 success（Actions 页面或 `gh run list` 一次即可），**再抽样验证线上改动已生效** —— 抽 3–6 个代表性 URL `curl -o` 落盘核对本批关键内容确已出现。部署未完成时线上仍是旧版本，此时抽查必然误判。**仍禁止** curl 拉线上产物做 MD5 逐文件比对、逐 URL 打 200、sleep 等待 CDN 传播或循环轮询 API；英文态须用真机探针。
- 例外：**不进构建产物的改动**（`*.md`、`.workbuddy/memory/*`、门禁脚本注释等）push 后可直接收尾，连 Actions 结果都不必等待。判定口诀：**「会不会让线上页面变一个字节？会→等部署成功；不会→不等。」**

### 4.5 索引提交约定（重要）
- **不要自动执行**索引提交（全量跑约 19 分钟，拖慢会话）
- 每次 `_build.py` 重建后，**只提醒用户手动运行** `python3 _submit_indexnow.py`
- 定时任务已由用户终端 crontab 管理：IndexNow 14:00 / Bing 15:00 / GSC Sitemap 15:30 / GSC 收录监控 16:00
- Bing URL API 必须保持小批量流式提交（当前默认 10 条/批），并按日期在 sitemap 正序/倒序之间轮换；禁止恢复为一次性万条批量提交。
- Bing 密钥必须通过 `BING_API_KEY` 环境变量注入，**禁止**把密钥写入仓库、日志、命令行参数或 crontab 命令文本。

### 4.6 删除 / 迁移 URL 必须提交死链（重要，红线）
**凡删除工具页、或把工具迁移到新 URL（改名 / 行业转移 / 走 `TOOLBOX-REDIRECT` 重定向存根），旧 URL 失效后，必须主动通知 IndexNow——`TOOLBOX-REDIRECT` 重定向页（虽仍返回 200，但已 `noindex` 且移出 sitemap）**同样视为死链、必须提交**；否则搜索引擎长期保留旧地址、发出负面 SEO 信号。**

- **适用场景**：① 直接 `git rm` 删除某工具页（真 404）；② 走 `TOOLBOX-REDIRECT` 存根机制把旧地址跳转到新地址（页面返回 200 但已 `noindex` 且移出 sitemap）。两种都算"旧 URL 不再作为正常收录页存在"，都必须通知。
- **必须调用**：`python3 _submit_indexnow_deadlinks.py`
  - **真 404（直接删除）**：`--file 死链列表.txt`（脚本自动 HTTP 校验、只交确认死掉的、跳过仍存活页）
  - **迁移壳（`TOOLBOX-REDIRECT` 存根，页面仍 200）**：`--no-verify` 强制提交（页面仍 200，默认校验会误判"存活"而跳过）
- **时机**：迁移壳可在 `git commit` 之前提交；**真 404 物理删除必须等线上部署 success 之后**再用默认校验提交（闭环：物理删除 → 提交并 push → 确认部署 success → 再提交死链）。
- **重定向存根保留期限（硬性）**：最长保留 **1 个月**，到期必须物理删除（旧 URL 真正 404），删除前/时仍须提死链（此时用默认校验）。**建存根同一批次必须**：① 同步 `--no-verify` 把旧 URL（含 `zh-tw/` 繁体）提死链；② **登记到 `_redirect_stubs_todo.md`**（源/目标/建存根日期/到期日/状态），到期由维护者主动删除，不依赖定时任务。

### 5. 兼容性约束
- 不要使用过于激进的新特性，确保主流浏览器（Chrome/Safari/Firefox/Edge 最近两个大版本）可用
- CSS 优先使用变量（CSS Variables），不要硬编码颜色值
- 移动端必须可用，不能只做桌面端

### 6. 单 Agent 串行执行（禁止多 Agent 并行）
**本项目同一时刻只允许一个 agent 对仓库做写操作，全部任务由主 agent 串行推进，一个干完再干下一个。**

- **禁止**为同一批任务派生多个子 agent / 后台 agent 并行干活（包括并行写文件、并行跑 `_build.py`、并行 commit）
- **禁止**创建多 agent 团队并发修改本仓库
- **主 agent 自顶向下串行执行**：一个子任务完整收口（改完 → 跑通门禁 → 提交）后，才允许开始下一个子任务
- 唯一例外：**纯只读**的检索/探查类子任务可并行；一旦涉及写入，一律回到串行。

**为什么必须串行**：`_build.py` 全量重写构建产物，并发会互相覆盖；多 agent 同时 `git commit` 触发 `.git/index.lock` 冲突；门禁结论依赖稳定工作区；批量改动要求合并提交，并行会让历史碎片化。

**与自动化任务的互斥**：定时看门狗等自动化 agent 与本仓库共用 `.workbuddy/watchdog.lock` 互斥——检测到心跳仍在有效期即跳过，不碰代码、不动 git。任何新增自动化必须遵守同一把锁。

### 7. 文件名 / URL 稳定性优先（禁止因"名不符实"改名）
**核心：文件名 = URL = SEO 资产。改动文件名会让已收录 URL 失效（404 / 需重定向），代价远大于"名字不好看"。**

- **禁止**仅因「文件名与工具标题/功能不符」而重命名文件。例：`analysis-14.html` 标题是"结核耐药分析" —— 正确做法是**把内容改成名副其实的工具**，而不是把文件改名。
- **唯一允许改名的场景**：分类转移（行业归属错误）时目标目录已存在同名文件产生冲突。此时只改被转移的文件，且必须按「下架/改名清理清单」同步 i18n 双键、`js/tool-i18n-en.js` 行级、`json/tools.json`、本地 `zh-tw/` 产物。
- 改名必须走 `TOOLBOX-REDIRECT` 存根机制保留旧 URL，不得直接删除造成 404。**建好存根后必须按 §4.6 调 `_submit_indexnow_deadlinks.py --no-verify` 提死链。**
- 内容层面的「名不符实」缺陷**一律通过重写页面内容解决**，保留原 URL。

---

## 🛠️ 构建脚本 `_build.py` 详解

这是项目最重要的脚本，负责整个项目的索引生成。

### 功能清单
1. 递归扫描 `tools/` 目录下所有 HTML 文件
2. 从 `<meta name="toolbox">` 标签提取元数据
3. 根据文件名和关键词自动分配功能分类（cat）和行业（industry）
4. 生成 `json/tools.json` 全量数据 + `json/industry-*.json` 按行业拆分
5. 更新 `index.html` 中的统计数据
6. 生成根 `sitemap.xml`（含简体、台湾繁体、guides/ 与 chains.html）
7. **SEO 注入**（`fix_tool_pages_seo`，幂等）：h1、面包屑导航、BreadcrumbList + WebApplication JSON-LD、og:image/twitter:image、相关工具区
8. 生成 `zh-tw/` 台湾繁体静态站点（本地保留调试、Git 忽略、Actions 发布）
9. **质量分级**（`classify_quality`）：按页面独有脚本量分 A/B/C 三级

### 运行方式
```bash
cd /Users/cgw/project/cgw/chenguangwu.github.io
python3 _build.py
```

### 元数据提取优先级
1. `<meta name="toolbox" content="cat=xxx,industry=xxx,icon=🎯,bg=#xxx">` — 最高优先级
2. `<title>` — 工具名称
3. `<h2>` — 工具描述
4. 文件名关键词匹配 — 兜底分类

---

## 📝 新增工具规范

### 1. 文件命名
- 全小写英文，单词用连字符 `-` 分隔，如 `bmi-calculator.html`
- 放入对应行业子目录：`tools/<industry>/xxx.html`
- ⚠️ **已上线的文件禁止因"名不符实"改名**（见 🚫 硬性约束 §7）：内容不符就**改内容**，不要改文件名。仅分类转移遇同名冲突时才可改名，且必须保留重定向存根。

### 2. 行业分类（209 个子目录）
`industry` 字段取值即目录名，由构建脚本从 `<meta name="toolbox">` 读取，**无需在本文穷举**——新增子行业直接新建目录即可，构建会自动生成对应 `industry-<dir>.json` 与分类落地页 `index.html`。

**原始 12 个一级行业（最常用）：**

| 代码 | 名称 | 代表工具 |
|------|------|----------|
| `it` | IT 开发 | JSON 格式化、Base64、正则、JWT |
| `finance` | 金融财务 | 复利计算器、IRR、期权盈亏 |
| `design` | 设计创意 | 渐变生成器、配色方案、玻璃拟态 |
| `biz` | 商业办公 | 二维码、密码生成、UUID |
| `marketing` | 营销推广 | ROI 计算、UTM 构建、漏斗分析 |
| `science` | 科学研究 | 物理计算、化学计算、统计检验 |
| `health` | 健康医疗 | BMI、BMR、心率区间、预产期 |
| `life` | 日常生活 | 单位换算、房贷计算、烹饪转换 |
| `edu` | 教育学习 | GPA 计算器、拼音转换、番茄钟 |
| `legal` | 法律合规 | 经济补偿金、加班费、诉讼费 |
| `fun` | 娱乐游戏 | 骰子、猜数字、记忆游戏 |
| `travel` | 旅行出行 | 时区转换、签证查询、货币速查 |

### 3. 功能分类（cat）

> `cat` 取值由元数据声明，下面为常用值，并非封闭清单。

| 代码 | 名称 | 代码 | 名称 |
|------|------|------|------|
| `text` | 文本处理 | `image` | 图片处理 |
| `encode` | 编码解码 | `math` | 数学计算 |
| `convert` | 格式转换 | `validator` | 验证器 |
| `generate` | 生成器 | `reference` | 速查表 |
| `dev` | 开发工具 | `game` | 游戏趣味 |
| `design` | 设计工具 | `finance` | 金融投资 |

### 4. 标准工具模板

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
<!-- 🔴 必须有：元数据标签，供构建脚本识别 -->
<meta name="toolbox" content="cat=math,industry=health,icon=❤️,bg=#ffe0e0">
<title>工具名称 - ToolBox</title>
<!-- 注意路径深度：tools/xxx/yyy.html 需要 ../../ -->
<link rel="stylesheet" href="../../css/common.css">
<script src="../../js/common.js"></script>
</head>
<body>

<!-- 导航栏：返回首页 + 面包屑 + 主题切换 -->
<div class="nav">
  <a href="../../index.html">← ToolBox</a>
  <span>/ 工具名称</span>
  <button class="theme-btn" onclick="ToolBox.toggleToolTheme()">🌙</button>
</div>

<div class="container">
  <div class="card">
    <h2>❤️ 工具名称</h2>
    <p style="font-size:13px;color:var(--text-muted);margin-bottom:16px;">工具描述说明</p>

    <!-- 输入区域 -->
    <div class="input-row">
      <label>输入</label>
      <input type="number" id="input" value="0" oninput="calc()">
    </div>

    <!-- 工具栏 -->
    <div class="toolbar">
      <button class="btn primary" onclick="calc()">计算</button>
      <button class="btn" onclick="copyResult()">复制结果</button>
    </div>

    <!-- 结果区域 -->
    <div class="result-box" id="result"></div>
  </div>
</div>

<script>
function calc() {
  const val = +document.getElementById('input').value || 0;
  const result = val * 2;
  document.getElementById('result').innerHTML =
    `<p>结果：<strong>${result.toFixed(2)}</strong></p>`;
}
// 页面加载时自动计算一次
calc();
</script>
</body>
</html>
```

### 5. 关键注意事项
- **meta toolbox 标签必须有**，否则构建脚本无法正确分类
- **路径要正确**：工具在 `tools/it/xxx.html`，引用公共资源要用 `../../css/common.css`
- **使用公共样式类**：`.nav`、`.container`、`.card`、`.btn`、`.btn.primary`、`.toolbar`、`.result-box`、`.input-row`
- **使用公共脚本方法**：`ToolBox.showToast()`、`ToolBox.copyText()`、`ToolBox.downloadText()`、`ToolBox.toggleToolTheme()`
- **主题切换按钮必须有**，调用 `ToolBox.toggleToolTheme()`

### 6. 中英文与指南三项同步（强制）
新增任意工具时，必须**一次性同步**以下三项，缺一不可，否则视为该工具未完成：
1. **中文工具页**（默认必备）：`tools/<industry>/<slug>.html`，标题/简介/正文为中文。
2. **英文 i18n 双轨**：
   - 卡片名写入 `i18n/tools/slug-en.json`（键 = `行业/slug`）；
   - 标题/简介写入 `i18n/tools/_en_override.json`，值必须是**嵌套 dict** `{en, ed, ind}`，**绝不能写成字符串**（否则 `_build.py apply_en_override` 报 `AttributeError`）；
3. **使用指南**：生成 `guides/<slug>-guide.html`，合并进 `json/guides.json`（按 `tool` 字段关联），并向 `js/guide-en-pack.js` 导出英文键；指南需含中英双语全套字段，且"去使用"链接的 `tools/<industry>/` 必须与工具页**真实目录一致**。

> 历史教训：Q1 三批 39 个工具曾先上线、后补指南与英文，造成二次返工；此后新增工具必须**三件齐发**，随工具页同一批次提交。

---

## 🏠 首页开发规范
- 数据加载：默认行业 `it` 的 `industry-it.json` → 渲染网格；切行业 fetch 对应 `industry-*.json`；首次搜索懒加载 `tools.json`（含 al/py/pyi）；已加载行业缓存在 `loadedIndustries`。

### 关键状态变量（在 `js/app.js` 中）
| 变量 | 说明 |
|------|------|
| `currentIndustry` | 当前选中的行业代码，默认 `'it'` |
| `currentCategory` | 当前选中的功能分类，默认 `'all'` |
| `searchQuery` | 当前搜索关键词 |
| `currentTools` | 当前行业的工具数组 |
| `allSearchIndex` | 全量搜索索引（搜索时才加载） |
| `loadedIndustries` | 已加载行业的缓存对象 |
| `favorites` / `recents` | 收藏 / 最近使用（localStorage） |

### CSS 变量规范
定义在 `css/style.css` 和 `css/common.css` 的 `:root` 和 `body.dark` 中：
| 变量 | 用途 | 变量 | 用途 |
|------|------|------|------|
| `--bg-body` | 页面背景色 | `--text-primary` | 主文字色 |
| `--bg-sidebar` | 侧边栏背景色 | `--text-secondary` | 次文字色 |
| `--bg-card` | 卡片背景色 | `--text-muted` | 弱文字色 |
| `--bg-hover` | 悬停背景色 | `--border-color` | 边框色 |
| `--bg-active` | 激活背景色 | `--primary` / `--primary-hover` | 主题色 / 悬停 |

---

## 🔍 搜索机制
- **无搜索时**：只加载当前行业数据（~6-54KB）；**有搜索时**：懒加载 `tools.json`（含 al/py/pyi 搜索字段）全量搜索。
- **tools.json 搜索字段**（单字母缩写，前端运行时投影为短字段）：`n`=name、`d`=desc、`i`=industry、`c`=cat、`u`=url、`ic`=icon、`b`=bg。

---

## 🧪 本地测试规范
```bash
cd /Users/cgw/project/cgw/chenguangwu.github.io
python3 _build.py            # 首次克隆 / zh-tw 缺失 / 源更新后先构建
python3 -m http.server 8765  # 访问 http://localhost:8765
```
- 因为使用 `fetch` 加载 JSON，必须通过 HTTP 服务器访问，不能直接双击 HTML（`file://` 协议会失败）。
- 本地验证台湾繁体页面前先确认 `zh-tw/index.html` 存在；若不存在就运行 `python3 _build.py`。`zh-tw/` 应留在本地用于调试，但始终保持 Git 忽略。

---

## 🔗 相关文件速查

| 文件 | 作用 | 修改频率 |
|------|------|----------|
| `index.html` | 首页结构 | 低 |
| `css/style.css` | 首页样式 | 中 |
| `js/app.js` | 首页逻辑 | 中 |
| `css/common.css` / `js/common.js` | 工具页公共样式/脚本 | 低 |
| `_build.py` | 构建脚本（含 SEO 注入/质量分级） | 中（新增分类时） |
| `scripts/*.py` | 批量生成器/审计/修复脚本 | 中（批量任务时用） |
| `_test_static.py` | 静态测试脚本 | 低（质量检查时用） |
| `tools/<industry>/*.html` | 各工具页面 | 高（新增工具） |
| `json/*.json` / `sitemap.xml` | 数据文件 / 站点地图 | 从不（构建产物） |

---

## ⚠️ 项目特有坑与速查（Agent 必读）

> 本节收录长期实践中反复踩到、且无法从代码或其它文档直接推断的坑。改动相关模块前先读本节。

### 构建与缓存
- 改任何 `css/js/json` 都必须先跑 `python3 _build.py`：Service Worker 的 BUILD 戳按内容 hash 注入，不重建则旧缓存永不失效
- 构建幂等：只读 `git --no-optional-locks status`；撞 `.git/index.lock` 用 `rm -f .git/index.lock`
- 构建产物变化一律**全量核对随提交**，禁止只挑部分文件回退；新建文件前先确认是否已存在（曾发生 Write 覆盖）
- SW v4 分三桶（`tb-shell-v4` / `tb-rt-v4-<BUILD>` / `tb-tools-v4-<BUILD>`）：CSS/JS/JSON 网络优先 3s 回退、图片字体 cache-first；紧急开关 `sw-kill.json` = `{"disabled":true}`
- **手改工具页后第一次 `_build.py` 会「一次性大改写」该页并冲掉手改内容**（相关工具重算 + 索引重建），第二次起才幂等。判据：插入 `<!--M1-->` 标记再构建，标记存活即证明构建本身不清除该区域。**对策：手改 → 构建 → 必须复查改动存活**（`grep -c` 关键串），被冲掉就把全部改动写进一个**幂等 apply 脚本**重跑，不要逐次手补
- **`<h1 class="sr-only">`、`bc-current` 面包屑、面包屑 JSON-LD 是「只写一次」字段**：构建仅在缺失时注入，已存在则不刷新。改工具名必须**同时**改 i18n 字典（`i18n/tools/<行业>.json` 的 `title`/`h1`）+ `json/tools.json` 的 `name` + 页面磁盘里的 h1/面包屑/JSON-LD，`<title>`/`og:title`/WebApplication `name` 则由构建每次刷新
- **仓库体积（`.git`）维护**：`du -sh .git` > **800M** 即 `git repack -a -d` + `git prune-packed`（合并全 pack、**不 prune 任何不可达对象**，零工作区影响、可随时重跑）；另有约 103M **不可达对象**（`git stash` 残留），清理须 `git prune`（**不可恢复 → 须老板拍板**，Agent 只报数据不做）

### 页面内容与 _build.py 的交互（逐分类推进必读）
- **`_prerender_tool_body` 只处理文档首个 `<p>`（`count=1`）**，且仅当正文含 CJK 时才用 `i18n/tools/<ind>-body.json` 的 `intro` 覆盖正文、原文写入 `data-zh`。由此产生三个必踩陷阱：
  - **插在首个 `<p>` 之前的中文 `<p>` 会被覆盖**：把 `formula-desc`（中文）放在工具标题 `<h2>` 后，它就成为首个 `<p>`，被 body JSON 的 intro 覆盖；若该条目 intro 仍是占位串，页面即显示占位（曾一次回归 128 处）。**解法：这类说明块用 `<div class="formula-desc">` 而非 `<p>`** —— build 只认 `<p>`，CSS 为 `.formula-box .formula-desc { margin:0 }`，换标签渲染一致。
  - **首个 `<p>` 若是 JS 字符串里的 `<p …>`**（错误提示 / 空状态，英文无 CJK），build 匹配它后即跳过，真正的中文 intro 永远拿不到英文注入（13 个统计类工具踩过）→ 解法：直接把源 intro 改为 `<p data-zh="中文">真实英文</p>`。
  - **空壳 `<p class="formula-desc"></p>` 会「吸收」这次 `count=1`**，使其后的中文 intro 侥幸躲过预渲染；一旦改成 div 或填入中文，这批会集中暴露（53 个工具踩过）→ 推进时应主动全量补齐这些 intro。
- **终端审计不能只看文本长度**：占位串本身也有 80+ 字，仅判「≥80 字」会得到假绿。必须**同时**查占位指纹（如 `is available directly in your browser, with no data uploaded.`）与套话指纹（如「本速查内容依据权威标准」）。
- **英文 p 三种来源机制不同，改错位置会被 build 还原**：① `data-zh` 机制 → 改源 html，安全持久；② `data-i18n` 机制 → 由 build 从 `<ind>-body.json` 注入，手改源 html 无效，**必须改数据源**；③ 中文 intro → build 注入或改源。
- **替换 JS 字符串里的占位必须替换「含工具名的整短语」**（如 `Statistical Power is available directly…`）。只替换核心句会残留工具名前缀。另：`re.sub` 的替换串里不要写 `\x27`（会报 `bad escape \x`），改用 `str.replace()` 最稳。

### i18n（中英 / 繁体）
- **凡引 `js/common.js` 的页面必须同时引 `js/i18n.js`**，否则 `?lang=en-US` 下整页回退中文；`guides/*.html` 等静态页须手动保留，幂等补注脚本 `scripts/inject_i18n_js.py`（正则须吞掉 `</script>`，否则插入标签不闭合）
- `I18n.apply(root)` **只扫描 root 的后代、不含 root 自身** —— 给 root 自身带 `data-i18n` 的元素必须显式调 `I18n.t()`
- `i18n.js` 以 defer 加载，**同步内联脚本早于它执行**：依赖 I18n 的渲染必须延后到 `DOMContentLoaded`
- `i18n.js` 的 `ind_*` 键仅数十个而行业有 209 个 → 分类页行业名**不要用 `ind_*`**，改用构建期双语层（`i18n/industry-en.json` 全覆盖 + `.t-zh/.t-en` + CSS `html[lang]` 显隐）
- 英文态排查判据（`?lang=en-US`）：① `[data-i18n]` 元素运行后仍含汉字 = 字典缺键或未加载；② 可见文本含汉字 —— **必须**用 `getClientRects().length === 0` 排除 CSS 隐藏的 `.t-zh`，否则大量误报
- 繁体页核验必须**源页配对**（`conv(源页值)` vs 繁体页值）：直接对繁体页做转换属二次转换，`twp` 非幂等会大量误报；判字形残留用 OpenCC `tw` 而非 `twp`；`data-zh` / `data-i18n-*-fb` 保留简体是运行时回退设计，不是残留
- **英文内容区（`?lang=en-US`）走三层运行时字典，全部非构建产物**：① `js/tool-i18n-en.js`（`GEN_UI_MAP` + `BODY_PHRASE_MAP`）；② `i18n/tools/<ind>-phrases.json` / `<ind>-body.json`；③ `i18n/tools/en/<ind>/<slug>.json`（**一个工具一个文件**，优先级最高，`map` 为「简体原文 → 英文」），配 `_index.json` 资源守卫与 `en/_common.json` 共享层。**新增或修改第三层后必须重跑 `_build.py`**
- **第三层字典的匹配口径**：运行时按 `el.textContent.trim()` 查表；`[data-zh]` 元素用 `el.textContent = tr`，普通文本节点用 `raw.slice(0,idx) + en + raw.slice(idx+k.length)` 保留 DOM 与内链。碎片节点的译文必须带 DOM 空白约定。孤立中文标点由运行时字符级 `convertPunct()` 兜底
- **`translateBodyPhrases()` 禁止对含表单控件的容器做整节点 `textContent` 替换**：那会把容器内 `input`/`select`/`textarea` 一起删除，页面随后 `getElementById(id).value` 抛 `Cannot read properties of null`。守卫条件：元素有子元素**且** `querySelector('input,select,textarea')` 非空则跳过
- **英文文案统一美式拼写**（`color` / `center` / `favor` / `customize` / `summarize` / `fulfillment` / `jewelry`）。批量替换时**警惕规则自污染**：`fulfilment→fulfillment` 之后再跑 `fulfil→fulfill` 会得到三写 `fulfilllment` ⇒ 替换对须「长词优先 + 短词加否定前瞻」
- **i18n 键前缀错配会静默把键名弹给用户**：页面写 `i18nText('toast.msgNNN')`（1033 处）而 `I18N_MSG` 存裸 `msgNNN`（624 条）⇒ `resolve()` 回退链末端 `return key` 渲染出键字符串。**逐个补键是错方向** ⇒ 走**前缀归一化回退**（剥前缀再查，页面与字典零改动），配套 `js/i18n.js` 导出 `I18n.has()`；**英文态须单独兜底**（`en-US PACKS` 未收录 `msgNNN`，否则回落中文给英文页面）。验证须**真浏览器点真实按钮**看 toast 的 `textContent`。
- **函数存在但不可见（真缺陷三种形态）**：
  - ①**被未闭合函数体吞掉**：数组型生成函数行尾只有 `{` 无 `}`，把紧随函数变内部代码 ⇒ 从未注册全局。表象迷惑：同块其他函数正常、加载期零 pageerror、语法校验通过。**判据**：逐 `function` 做花括号平衡，体长异常（>4000）且其后还有 function 声明即候选，再用 `typeof window.X` 复核。**修法**：补 `}`、被吞函数移回顶层。
  - ②**IIFE 包裹 + 内联 onclick**：`(function(){…})()` 内 `function` 不挂全局，而 `onclick="executeSQL()"` 需全局 ⇒ `X is not defined`。照该页既有风格补 `window.X = function…`，**不用 `eval`**。
  - ③**onclick 属性被 `JSON.stringify` 双引号提前闭合**：`onclick="applyPreset(${JSON.stringify(p.colors)})"` 中 JSON 含双引号 ⇒ 属性在第一个 `"` 处闭合、`onclick` 变 `applyPreset([` ⇒ 点预设抛 `SyntaxError`。**修法：属性改单引号包裹**；全站 17 页内联 `JSON.stringify`，只有传数组/对象的 5 页出问题 ⇒ 必须真浏览器逐页编译验证。
  - **Canvas 负半径**：`radius=Math.min(cw,ch)/2-30` 而 `cv.width=ct.clientWidth`，容器未布局时 `cw` 为负 ⇒ `ctx.arc` 抛 `The radius provided (-70) is negative`，修法 `Math.max(5,…)`。
  - **静态假阳性勿采信**：「IIFE 未挂 window」报 293 页抽样 8 页仅 3 真问题；「函数体超长吞并」报 530 处复核全正常调用。**「函数不可见」只能用真浏览器 `typeof window.X` 定罪。**

### 内容质量
- **A 级硬标准**：`own_len ≥ 6000`，或 `≥ 3000 且 inputs ≥ 3`；含 `formula-box` / `canvas` / `data-viz` 直接判 A；**禁止用代码膨胀凑数**
- **head-only 死壳**特征：`<body>` 无开标签 / 无 `input`+`select` / deep-dive 段误置 `<head>`（线上打开空白）。扫法 `'<body>' not in c`
- **两套套话残留**（逐分类必查）：① 可见 `opt-guide` / `opt-faq` → `scripts/opt_cleanup_opt_blocks.py --cat X`；② FAQPage JSON-LD 里的旧套话 → `scripts/opt_faq_ld_sync.py --cat X`。**_build.py 不重建工具页的 FAQPage LD**，必须手改并 `json.loads` 校验
- deep-dive 算例数字一律用 node 实跑取（含 `toFixed` 四舍五入），禁止凭印象写
- `i18n/tools/content_deepdive.json` 仓库规范 `indent=1`（`_build.py` 只读不写），apply 脚本必须 `json.dump(indent=1)`，否则全量重排成巨大噪音 diff
- **defer 脚本闭包死引用**：`common.js` 整体替换后旧 stub 引用失效 → 「📋复制 / ⬇️导出」点击无反应。根治方式为替换前保存旧对象、替换后回填同名方法指向真实实现；审计脚本 `scripts/audit_toolbox_stub_refs.py`
- **淘宝客双链**：PC 链 `s.click.taobao.com/UItQ6Hk`、WAP 免登录链 `s.click.taobao.com/5e6P6Hk`；手机上打开 PC 链会被强制登录 → 转化归零。全站唯一维护点 `js/common.js` 的 `toolboxTaobaoAdUrl()`（断点 `innerWidth < 768`），禁止再硬编码
- `scripts/gen_guide_pages.py`：`guides/index.html` 是纯追加（不按 slug 去重），重生成同 slug 会在指南中心重复卡片；重跑前先按行删掉该 slug 旧卡片
- **术语内链唯一源 = `_build.py::linkify_terms()`**：逐字符最长匹配、`TERM_LINK_MIN_LEN=3`（「公式」曾命中 844 次）、每目标页每页只链一次、上限 `TERM_LINK_MAX_PER_PAGE=6`、不链自身、ASCII 术语要求词边界（防 `CSS` 命中 `CSS3`）；**目标须存在且非 `TOOLBOX-REDIRECT` 存根**。**禁在页面手改内链**。

### 无头浏览器验证
- Chrome 绝对路径 `/Applications/Google Chrome.app/Contents/MacOS/Google Chrome`（不在 PATH）；`puppeteer-core` 用 managed 绝对路径 require；启动参数 `headless:'new'` + `--no-sandbox --disable-setuid-sandbox --disable-dev-shm-usage`
- 本地服务 `python3 -m http.server 8137 --directory <项目根>`（后台），用完 `pkill -f "http.server 8137"`
- 须真触发事件（`.tb-nav-link` click 才生成 megapanel）；繁体页 `set()` 会整页跳转，`goto` 后轮询 `page.url()` 稳定后再 evaluate

### verify 脚本口径（`scripts/verify_*_calc.js`）
- **`collectStrings` 只对 `innerHTML` / `textContent` 剥 HTML 标签，`el.value` 保留原文**（2026-09-28 修正）—— `value` 恒为纯文本，对它剥标签会把尖括号形态的结果整块吞掉（`it/base85-encode` 的 `<~BOu!rDZ~>` 此前永远匹配不上）。改动该函数会波及全站用例口径，**必须重跑 `run_gates.py` 的 `selfcheck_false_pass` / `discriminate_check` 两项**确认逃生项与弱用例基线未变
- **逃生项新判据**：`expect` 恰好等于「`inputs` 各值经剥标签 + 空白归一」的形态即逃生项（`it/html-minifier` 原 `expect:["a b"]`，而输入 `<p>a</p>` + 换行 + `<p>b</p>` 归一后正是 `a b`）⇒ 定 expect 前先把注入输入按该口径跑一遍比对
- **HTML 里带 `checked` 的 checkbox 在桩内恒 `false`**（真机默认勾选）⇒ 必须用 `checkIds` 显式还原真机默认态，否则页面走「开关全假」分支、输出恒等于输入（`it/html-minifier` 即因此退化成回显）
- **循环体内无任何推进语句 = 真死循环**：`it/docker-run-converter` 的 `parse()` 在 image 已赋值时不递增 `i`，遇尾参即无限循环冻死标签页，已修。判据：循环体含 `i++` / 赋值 / `next()` 任一即安全
- **烟测 ⚠️「点击了 N 个按钮但无输出变化」≠ 页面缺陷**：若页面在加载时就执行过同名初始化（如 `it/calc-7` 末尾直接调 `loadSample()`），再点同一按钮内容自然不变。判定真伪先看页面末尾有无直接调用
- **harness 三阶段**：①覆盖 `inputs` + 触发 `input/change/keyup` 立刻查 expect → ②执行 `clicks` → ③未命中才无参遍历调用候选函数兜底。`collectStrings` 收每元素 `value`/`innerHTML`/`textContent` 剥标签压成**单串** ⇒ `blob.includes(want)` 是**子串**匹配
- **用例文件静默失效**：`selfcheck_false_pass.js::extractCases` 不识别注释，行注释里撇号会被当字符串起始 → 括号层级错位 → `extractCases` 返回 undefined → 该文件全部用例静默消失（`checked=0`、门禁照旧全绿）。判据：**任何 verify 文件 `checked` 必须等于其用例条数**，不等即命中
- **浮点 expect 禁 ≥15 位有效数字**（跨平台 1 ULP：macOS ARM 与 Linux x86 常差 1 位 ⇒ 本地绿 CI 红且不可复现）：只留 ≤10 位；多数值切多条（OR 语义）而非各自截断；**天文数字（expect 含 `e+2x`）整页随 Node 版本变 ⇒ 换温和输入**（如 Bin(20,0.25,5)）。复验须用 CI 同款运行时（Node 24）+ `TZ=UTC`。**日期/时区**：`new Date('<串>')` 按 UTC 解析、用本地分量格式化 ⇒ 输出随时区偏移 1 天；锚点须由注入决定、不由时钟决定
- **卡死判定用心跳**：`setInterval(()=>window.__hb++,100)` 点击后每 1s 采样连续 8s，停摆 = 真死循环；单次 `evaluate` 超时不能定罪。死循环只能真浏览器 + 心跳二次确认
- **不可注入静态判据**：控件由运行期 `innerHTML` 生成（id 形如 `c{i}`）、驱动走纯 class 选择器、`createElement+appendChild` 建的行、控件在 `display:none` 面板内。**P0 真缺陷信号**：控件 id 不存在（加载即 `Cannot read properties of null`、整页无输出）；`.length` 判空却传对象（`!list.length` 恒真 ⇒ 整页功能恒定不工作）。别急着归类为「不可注入」

---

## 🔥 热度排序约定（2026-09-12，老板明确要求）

- **全站「分类内工具」与「分类本身」的排序统一按热度分 `hot`（整数，越大越热），不再按工具名(name) 字母序排序。**
- `hot` 由 `_build.py` 的 `compute_hot()` 在 `main()` 统一计算并持久化进 `json/tools.json`，所有入口消费（分类页 / sitemap 页 / 导航 mega menu / 首页 / 运行时分类页）。
- **口径**：`hot-tools.json` 的 80 个「编辑精选热门工具」作为热度金字塔顶端，严格保持原序不动；其余工具由 `compute_hot()` 按「通用工具类型权重 + 质量等级 + 可发现性 + 分类加成」给确定性热度分（模型可复现、构建幂等、不抖动）。
- ⚠️ **后续新增工具页**：无需手动排序——`main()` 会为所有工具（含新增）计算 `hot`，自动按热度排。**禁止在任一生成函数里改回按 `name`/`file` 排序**。真实流量（51.la URL 级接口 / GSC 逐页 clicks·impressions）到位后，只需重算 `hot` 字段即可，排序逻辑无需改动。

---

> **最后更新**：2026-10-11（瘦身：删除与「项目特有坑与速查 / 硬性约束」重复的「📌 开发约束补充」节、与 §4.2 重复的「发布流程」、通用样板「代码风格」、与坑与速查重复的「常见坑点」、引用未入库 `todo.md` 的「批量工具开发规则」、与「新增工具规范」重复的「开发工作流建议」；把补充节里仅有的独有点——术语内链 `linkify_terms()` 规则、仓库体积 `git repack` 维护——并回「项目特有坑与速查」）。冗余规则统一以「项目特有坑与速查」为权威，避免多节重复。
