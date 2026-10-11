# ToolBox

4700+ 个免费在线工具组成的纯前端工具百科。计算、转换、编码、文本处理、生成器、开发辅助和行业工具都在浏览器本地运行，用户数据不上传服务器。

## 项目特点

- 纯 HTML、CSS、原生 JavaScript 和 Python 构建脚本。
- 无账号、无后端业务接口，工具数据默认只在当前浏览器处理。
- 支持中英文界面、拼音搜索、模糊搜索、收藏、最近使用和深浅主题。
- 支持移动端布局、PWA 离线缓存和本地隐私管理。
- GitHub Actions 构建并通过 GitHub Pages 发布静态产物。

## 实时统计

统计数据由 `python3 _build.py` 根据当前工具页面自动更新，禁止手工修改。

<!-- TOOLBOX_STATS_START -->
| 指标 | 实时值 |
|---|---:|
| 工具总数 | 4726 |
| 行业总数 | 207 |
| A 级占比 | 99.5% |
| B 级占比 | 0.2% |
| C 级占比 | 0.3% |
<!-- TOOLBOX_STATS_END -->

## 本地运行

项目使用 `fetch` 加载索引 JSON，不能依赖 `file://` 协议直接打开首页。请在仓库根目录启动本地 HTTP 服务：

```bash
python3 -m http.server 8765
```

然后访问 <http://localhost:8765>。

### 台湾繁体页面

`zh-tw/` 是 `_build.py` 根据简体中文源页面生成的静态发布目录，已通过根目录 `.gitignore` 忽略：

- 本地调试时保留 `zh-tw/`，可直接访问 `http://localhost:8765/zh-tw/`；它不会出现在提交中。
- 首次克隆、主动删除目录或修改中文源页面后，先运行 `python3 _build.py` 重新生成。
- 不要使用 `git add -f zh-tw/`，繁体产物只由本地构建和 GitHub Actions 生成。
- 根 `sitemap.xml` 会始终包含简体与台湾繁体 URL，不以本地 `zh-tw/` 是否存在为判断条件；缺少该目录时，本地繁体链接会暂时返回 404，重新构建即可恢复。

## 构建与质量门禁

新增或修改工具后，运行统一门禁：

```bash
python3 scripts/run_gates.py
```

门禁包含（完整清单见 `scripts/run_gates.py`）：

- `python3 _build.py`：扫描工具页面并生成索引、行业数据、站点地图和 SEO 信息。
- `python3 _test_static.py`：检查静态页面结构、元数据和相关映射。
- `python3 _audit_links.py --check`：检查站内死链。
- `python3 _audit_assets.py --check`：检查局部资源、HTML 语言属性和重复 id。
- `node scripts/check_inline_js_syntax.js`：校验页面内联 JS 语法。
- `node scripts/verify_calc.js`：执行计算工具回归用例（冒烟）。
- `node scripts/verify_it_calc.js`：执行 IT 计算工具正确性用例。
- `node scripts/selfcheck_false_pass.js scripts` / `node scripts/discriminate_check.js`：反回归门禁（禁止假门禁标记 / 校验用例判别力）。

GitHub Actions 会在 pull request 和推送到 `master` 时自动执行同一套门禁。
`master` 门禁通过后，Actions 会上传完整静态 artifact 并部署到 GitHub Pages。
`zh-tw/` 为构建期生成目录，不再提交到源码仓库。
发布前会运行 `scripts/check_pages_artifact.py`，产物达到 900MiB 安全阈值时停止部署。
仓库 Pages 的发布来源必须保持为 **GitHub Actions**，不要切回 `Deploy from a branch`。

## 目录说明

| 路径 | 用途 |
|---|---|
| `index.html` | 首页和行业导航 |
| `tools/<industry>/` | 工具页面，禁止直接放在 `tools/` 根目录 |
| `guides/` | 工具使用指南 |
| `css/` | 首页和工具页公共样式 |
| `js/` | 首页、工具页、i18n、PWA 和隐私功能 |
| `json/` | 构建生成的工具索引，不手工修改 |
| `zh-tw/` | 本地与 Actions 生成的台湾繁体静态站点，保留用于本地调试但不提交 |
| `scripts/` | 批量生成、审计和开发辅助脚本 |
| `_build.py` | 项目构建入口 |
| `AGENTS.md` | AI Agent 开发规范（约束与坑点速查） |
| `DEV-PLAN.md` | 全站优化主计划（待办与开发规则） |

## 新增工具规则

1. 新工具必须放在对应的 `tools/<industry>/` 目录。
2. 页面必须声明 `meta name="toolbox"`，包含 `cat`、`industry`、`icon` 和 `bg` 等元数据。
3. 核心功能必须真实可用，不能使用静态假结果或占位逻辑。
4. 所有计算、转换和文件处理优先在浏览器本地完成。
5. 不新增后端服务、登录、支付、实时数据 API 或需要上传用户数据的功能。
6. 新页面遵守 `AGENTS.md`、`docs/i18n-spec.md` 和 `ui/设计规范.md`。
7. 不手工修改 `json/*.json`、`sitemap.xml` 或首页构建注入的工具统计。

## 英文内容（EN）专项

`?lang=en-US` 下工具页的内容区由三层运行时字典提供，全部为源码维护（非构建产物）：

| 层 | 位置 | 说明 |
|---|---|---|
| ① 通用 UI | `js/tool-i18n-en.js` | `GEN_UI_MAP` 与 `BODY_PHRASE_MAP`，全站通用文案 |
| ② 行业层 | `i18n/tools/<ind>-phrases.json`、`<ind>-body.json` | 按行业批量覆盖 |
| ③ 工具层 | `i18n/tools/en/<ind>/<slug>.json` | **一个工具一个文件**，优先级最高 |

- 第三层 `map` 为「简体原文 → 英文译文」，配套 `_index.json` 资源守卫与 `en/_common.json` 共享层。
- **修改或新增第三层后必须重跑 `python3 _build.py`**：该子树已纳入 Service Worker 版本戳，否则缓存键不变、CDN 会继续下发旧字典。
- 英文文案统一使用**美式拼写**（`color` / `center` / `favor` / `customize` 等）。
- 每批验收包含四态烟测 —— 简体、英文、繁体、繁体英文，要求均无 JS 报错与页面异常。

## 发布流程

1. 在本地 HTTP 服务中验证首页、搜索、工具页和移动端布局。
2. 运行 `python3 scripts/run_gates.py`，确保全部门禁全部通过。
3. 提交源文件和需要版本化的构建产物；不提交 `zh-tw/`。
4. 推送到 `master`，等待 `ToolBox Build and Deploy` 完成门禁、artifact 上传和 Pages 部署。
5. **Actions run 成功 + 抽样验证线上生效**（单次查询即可）：先确认 Actions run 为 success，再抽 3–6 个代表性 URL `curl -o` 落盘核对**本批关键内容确已出现**（英文态须用真机探针 `scripts/_en_i18n_probe.mjs --check`，静态 HTML 不体现运行时替换）。仍不要做全量逐文件 MD5 比对、逐 URL 打 200、sleep 等待 CDN 传播或循环轮询 API；线上可用性异常由后续索引/监控任务或用户反馈暴露后再处理。
6. 仅改文档或内存日志等**不进构建产物**的文件时，push 后可直接收尾，无需等待部署结果。
7. 索引提交由用户侧定时任务管理；不要在普通开发会话自动运行 `_submit_*` 脚本。

## 搜索引擎提交注意事项

- Bing URL API 保持小批量流式提交，脚本默认每批 10 条并按日期正序/倒序轮换，避免一次性批量提交 1 万条 URL。
- Bing 密钥通过 `BING_API_KEY` 环境变量提供，不要写进仓库、日志、命令行参数或 crontab 命令文本。
- `_submit_bing_url_api.py` 会先读取 Bing 当日/月度剩余额度并限制提交数量；额度查询失败时应停止，不能盲目全量提交。

---

## 开发文档（详细说明）

> 以下为面向开发者的详细说明。AI Agent 的硬性约束与坑点速查见 **AGENTS.md**。

### 项目概览

- **技术栈**：纯前端 HTML5 + CSS3 变量主题 + 原生 ES6 JavaScript + Python/Node.js 构建脚本。
- **部署方式**：GitHub Actions 构建后上传静态 artifact，由 GitHub Pages 发布（`.nojekyll` 强制纯静态直发）。
- **核心特性**：响应式（桌面 + 移动端底部 Tab 栏）、4729 个工具 / 209 个子行业目录（以 `_build.py` 实时统计为准）、纯前端处理、中英双语 i18n、PWA 离线、质量分级。

### 设计规范（必须遵守）

> 完整设计规范另见 `ui/设计规范.md`。

**色彩系统**

| 色彩名称 | 变量名 | Hex 值 | 用途 |
|---|---|---|---|
| 主色 Primary | `--color-primary` | `#FF6B35` | 主按钮、关键操作、高亮强调 |
| 辅色 Secondary | `--color-secondary` | `#7C3AED` | 副功能区、标签、装饰元素 |
| 强调色 Accent | `--color-accent` | `#00C9A7` | 成功态装饰、进度指示 |
| 背景色 Background | `--color-bg` | `#FFFAF7` | 页面底层背景 |
| 文字主色 | `--color-text-primary` | `#1F2937` | 标题、正文主体 |
| 文字次色 | `--color-text-secondary` | `#6B7280` | 说明文字、次要信息 |
| 边框色 | `--color-border` | `#E5E7EB` | 分割线、输入框边框 |
| 卡片背景 | `--color-card` | `#FFFFFF` | 卡片、面板背景 |

**功能色**

| 语义 | Hex 值 | 浅色背景 | 用途 |
|---|---|---|---|
| 成功 | `#10B981` | `rgba(16,185,129,0.10)` | 操作成功、复制完成 |
| 警告 | `#F59E0B` | `rgba(245,158,11,0.10)` | 注意事项 |
| 错误 | `#EF4444` | `rgba(239,68,68,0.10)` | 输入错误、操作失败 |
| 信息 | `#3B82F6` | `rgba(59,130,246,0.10)` | 提示信息 |

**圆角规范**：按钮 12px（`rounded-xl`）/ 卡片 16px（`rounded-2xl`）/ 输入框 12px（`rounded-xl`）/ 标签全圆（`rounded-full`）/ 模态框 24px（`rounded-3xl`）。

**技术栈**：Tailwind CSS v4 Browser CDN、Lucide Icons（`data-lucide`）、Noto Sans SC + Plus Jakarta Sans 字体。

```html
<script src="https://cdn.jsdelivr.net/npm/@tailwindcss/browser@4"></script>
<script src="https://unpkg.com/lucide@latest"></script>
<style type="text/tailwindcss">
  @theme {
    --color-primary: #FF6B35;
    --color-secondary: #7C3AED;
    --color-accent: #00C9A7;
    --color-bg: #FFFAF7;
    --color-card: #FFFFFF;
    --color-dark: #1E1E2E;
    --color-muted: #6B7280;
  }
</style>
```

### 目录结构（严格遵守）

```
chenguangwu.github.io/
├── index.html              # 首页入口（侧边栏布局）
├── css/
│   ├── style.css           # 首页样式（侧边栏布局、响应式）
│   ├── site-chrome.css     # 顶栏 / 页脚 / Tab 栏 / 回顶按钮的唯一样式源
│   ├── common.css          # 工具页公共样式（所有工具共用，经 @import 引入 site-chrome.css）
│   ├── home-categories.css # 首页分类导航样式
│   └── nav-menu.css        # 全站 2 级分类导航样式
├── js/
│   ├── app.js              # 首页逻辑（动态加载、侧边栏交互）
│   ├── common.js           # 工具页公共脚本（ToolBox 命名空间）
│   ├── i18n.js             # 中英双语 i18n 引擎（全站共用）
│   ├── tool-i18n.js        # 工具页内容区 i18n 运行时
│   ├── tool-i18n-en.js     # 全站通用英文层
│   ├── tool-search.js      # 全站统一实时下拉搜索
│   ├── analytics.js        # 统一统计入口（百度 / Clarity / 51.la）
│   ├── freemium.js         # Freemium：AI 工具每日限额
│   ├── ai-core.js          # Transformers.js 纯前端 AI 共享加载器
│   ├── chart.js            # 零依赖 Canvas 图表库
│   └── qrcode.js           # 二维码库（第三方，MIT）
├── json/
│   ├── tools.json          # 全量工具数据（搜索单一数据源）
│   ├── industry-*.json     # 按行业拆分数据（与子行业目录一一对应）
│   ├── guides.json         # 工具 ↔ 使用指南配对
│   └── hot-tools.json      # 热门工具清单（首页 / 404 消费）
├── tools/                  # 工具页面（按子行业分子目录组织）
│   ├── it/  finance/  design/  biz/  marketing/  science/  health/
│   ├── life/  edu/  legal/  fun/  travel/   # ← 原始 12 个一级行业
│   ├── ai/  encode/  eco/  photo/  statistics/  healthcare/  ...
│   └── <industry>/index.html   # 每个子行业目录下的分类落地页（构建脚本自动生成）
├── guides/                 # 使用指南页集合（含 index.html 指南中心）
├── scripts/                # 开发/生成脚本（批量工具生成、SEO 审计修复、指南生成等）
│   ├── gen_itools_t1.py / gen_itools_t2.py / gen_tiny_t1.py  # 批量工具生成器
│   ├── gen_guides2.py      # 指南生成器
│   └── audit_seo.py / seo_fix2.py  # SEO 审计 / 修复脚本
├── chains.html             # 工具链组合页
├── search.html             # 站内搜索页
├── _build.py               # 构建脚本（最重要的脚本）
├── _test_static.py         # 静态测试
├── _submit_indexnow.py     # IndexNow 索引提交（每日 14:00 crontab）
├── _submit_bing_url_api.py # Bing URL 提交（每日 15:00 crontab）
├── _gsc_submit_sitemap.py  # Google Sitemaps 提交（每日 15:30 crontab）
├── _gsc_inspect_urls.py    # Google 收录监控（每日 16:00 crontab）
├── _submit_indexnow_deadlinks.py # 死链(迁移壳)提交（删/迁 URL 后手动触发）
├── sitemap.xml             # 根站点地图（构建产物）
├── sitemap.html            # 可视化站点地图（构建产物）
├── robots.txt              # 爬虫规则
├── og-image.png            # 1200×630 社交分享图（全站 og:image 引用，勿删）
└── README.md / AGENTS.md / DEV-PLAN.md
```

### 构建脚本 `_build.py` 详解

这是项目最重要的脚本，负责整个项目的索引生成。

**功能清单**：

1. 递归扫描 `tools/` 目录下所有 HTML 文件。
2. 从 `<meta name="toolbox">` 标签提取元数据。
3. 根据文件名和关键词自动分配功能分类（cat）和行业（industry）。
4. 生成 `json/tools.json` 全量数据。
5. 生成 `json/industry-*.json` 按行业拆分数据（与子行业目录一一对应）。
6. 更新 `index.html` 中的统计数据。
7. 生成根 `sitemap.xml`（含简体、台湾繁体、guides/ 与 chains.html）。
8. **SEO 注入**（`fix_tool_pages_seo`，幂等）：h1、面包屑导航、BreadcrumbList + WebApplication JSON-LD、og:image/twitter:image、相关工具区。
9. 生成 `zh-tw/` 台湾繁体静态站点。
10. **质量分级**（`classify_quality`）：按页面独有脚本量分 A/B/C 三级。

**运行方式**：

```bash
cd /Users/cgw/project/cgw/chenguangwu.github.io
python3 _build.py
```

**元数据提取优先级**：① `<meta name="toolbox" content="cat=xxx,industry=xxx,icon=🎯,bg=#xxx">`（最高）；② `<title>`；③ `<h2>`；④ 文件名关键词匹配（兜底）。

### 热度排序（设计约定）

- 全站「分类内工具」与「分类本身」统一按热度分 `hot`（整数，越大越热）排序，不再按工具名字母序。
- `hot` 由 `_build.py` 的 `compute_hot()` 在 `main()` 统一计算并写入 `json/tools.json`，所有入口（分类页 / sitemap / mega menu / 首页 / 运行时分类页）消费。
- 口径：`hot-tools.json` 的 80 个编辑精选热门工具作为热度金字塔顶端、严格保持原序；其余由 `compute_hot()` 按「类型权重 + 质量等级 + 可发现性 + 分类加成」给确定性热度分（模型可复现、构建幂等）。
- 新增工具无需手动排序，`main()` 会自动为所有工具算 `hot`；真实流量（GSC 逐页 clicks/impressions）到位后只需重算 `hot` 字段，排序逻辑不变。

### 新增工具规范

#### 1. 文件命名

- 全小写英文，单词用连字符 `-` 分隔（如 `bmi-calculator.html`、`json-formatter.html`）。
- 放入对应行业子目录：`tools/<industry>/xxx.html`。
- ⚠️ **已上线的文件禁止因"名不符实"改名**：文件名即 URL 即 SEO 资产，内容不符就**改内容**，不要改文件名。仅分类转移遇同名冲突时才可改名，且必须保留重定向存根（详见 AGENTS.md §7）。

#### 2. 行业分类（200+ 细分行业，当前 209 个子目录）

`industry` 字段取值即目录名，由构建脚本从 `<meta name="toolbox">` 读取，**无需穷举**——新增子行业直接新建目录即可，构建会自动生成对应 `industry-<dir>.json` 与分类落地页 `index.html`。

**原始 12 个一级行业（最常用）：**

| 代码 | 名称 | 代表工具 |
|---|---|---|
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

#### 3. 功能分类（cat，常用值非封闭清单）

`text`(文本处理) / `encode`(编码解码) / `convert`(格式转换) / `generate`(生成器) / `dev`(开发工具) / `design`(设计工具) / `image`(图片处理) / `math`(数学计算) / `validator`(验证器) / `reference`(速查表) / `game`(游戏趣味) / `finance`(金融投资)。

#### 4. 标准工具模板

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">

<meta name="toolbox" content="cat=math,industry=health,icon=❤️,bg=#ffe0e0">
<title>工具名称 - ToolBox</title>

<link rel="stylesheet" href="../../css/common.css">
<script src="../../js/common.js"></script>
</head>
<body>


<div class="nav">
  <a href="../../index.html">← ToolBox</a>
  <span>/ 工具名称</span>
  <button class="theme-btn" onclick="ToolBox.toggleToolTheme()">🌙</button>
</div>

<div class="container">
  <div class="card">
    <h2>❤️ 工具名称</h2>
    <p style="font-size:13px;color:var(--text-muted);margin-bottom:16px;">工具描述说明</p>
    
    
    <div class="input-row">
      <label>输入</label>
      <input type="number" id="input" value="0" oninput="calc()">
    </div>
    
    
    <div class="toolbar">
      <button class="btn primary" onclick="calc()">计算</button>
      <button class="btn" onclick="copyResult()">复制结果</button>
    </div>
    
    
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

#### 5. 关键注意事项

- **meta toolbox 标签必须有**，否则构建脚本无法正确分类。
- **路径要正确**：工具在 `tools/it/xxx.html`，引用公共资源用 `../../css/common.css`。
- **使用公共样式类**：`.nav`、`.container`、`.card`、`.btn`、`.btn.primary`、`.toolbar`、`.result-box`、`.input-row`。
- **使用公共脚本方法**：`ToolBox.showToast()`、`ToolBox.copyText()`、`ToolBox.downloadText()`、`ToolBox.toggleToolTheme()`。
- **主题切换按钮必须有**，调用 `ToolBox.toggleToolTheme()`。

#### 6. 中英文与指南三项同步（强制，详见 AGENTS.md「新增工具强制约束」）

新增任意工具必须**一次性同步**以下三项，缺一不可：

1. **中文工具页**（默认必备）：`tools/<industry>/<slug>.html`。
2. **英文 i18n 双轨**：卡片名写入 `i18n/tools/slug-en.json`（键 = `行业/slug`）；标题/简介写入 `i18n/tools/_en_override.json`，值必须是**嵌套 dict** `{en, ed, ind}`，**绝不能写成字符串**。
3. **使用指南**：生成 `guides/<slug>-guide.html`，合并进 `json/guides.json`（按 `tool` 字段关联工具页），并向 `js/guide-en-pack.js` 导出英文键；指南"去使用"链接的 `tools/<industry>/` 须与工具页真实目录一致。

> 历史教训：Q1 三批 39 个工具曾先上线、后分两批补指南与英文，造成二次返工；此后新增工具必须**三件齐发**，随工具页同一批次提交。

### 首页开发规范

#### 1. 布局结构

```
┌──────────┬─────────────────────────────────┐
│  Sidebar  │  Main Content                   │
│  (280px)  │  (自适应宽度)                   │
│           │                                 │
│  Logo     │  页面标题 + 描述                │
│  搜索框    │                                 │
│  行业导航  │  功能分类标签                   │
│  功能标签  │                                 │
│  底部统计  │  工具卡片网格                   │
│           │                                 │
│           │  Footer                         │
└──────────┴─────────────────────────────────┘
```

#### 2. 数据加载流程

```
页面加载 → 加载默认行业(it)的 industry-it.json → 渲染工具网格
用户点击其他行业 → fetch 对应 industry-*.json → 渲染
用户搜索 → 首次搜索时 fetch search-index.json → 全量搜索
已加载的行业缓存在内存中（loadedIndustries 对象）
```

#### 3. 关键状态变量（`js/app.js`）

| 变量 | 说明 |
|---|---|
| `currentIndustry` | 当前选中的行业代码，默认 `'it'` |
| `currentCategory` | 当前选中的功能分类，默认 `'all'` |
| `searchQuery` | 当前搜索关键词 |
| `currentTools` | 当前行业的工具数组 |
| `allSearchIndex` | 全量搜索索引（搜索时才加载） |
| `loadedIndustries` | 已加载行业的缓存对象 |
| `favorites` | 收藏列表（localStorage） |
| `recents` | 最近使用（localStorage） |

#### 4. CSS 变量规范

定义在 `css/style.css` 和 `css/common.css` 的 `:root` 和 `body.dark` 中：`--bg-body` / `--bg-sidebar` / `--bg-card` / `--bg-hover` / `--bg-active` / `--text-primary` / `--text-secondary` / `--text-muted` / `--border-color` / `--primary` / `--primary-hover`。

### 本地测试规范

#### 启动本地服务器

```bash
cd /Users/cgw/project/cgw/chenguangwu.github.io
# 首次克隆、zh-tw/ 缺失或源页面更新后先构建
python3 _build.py
python3 -m http.server 8765
```

访问：<http://localhost:8765>。

#### 测试清单

- [ ] 首页加载正常，默认行业工具显示正确
- [ ] 侧边栏点击行业，动态加载正确
- [ ] 搜索功能正常（跨行业搜索）
- [ ] 主题切换正常（浅色/深色）
- [ ] 工具卡片点击跳转正常
- [ ] 工具页面公共样式/脚本加载正常
- [ ] 移动端布局正常（<768px）
- [ ] 收藏功能正常（localStorage 持久化）

**不要依赖 `file://` 协议**：因为使用了 `fetch` 加载 JSON，必须通过 HTTP 服务器访问，不能直接双击 HTML。本地需要验证台湾繁体页面时，先确认 `zh-tw/index.html` 存在；若不存在就运行 `python3 _build.py`。

### 代码风格

- **HTML**：2 空格缩进、属性用双引号、语义化标签优先。
- **CSS**：2 空格缩进、优先使用 CSS 变量、按布局 → 组件 → 状态组织、移动适配写在底部。
- **JavaScript**：2 空格缩进、优先 `const` 其次 `let` 不用 `var`、函数表达式优先、用模板字符串。
- **Python**：4 空格缩进（PEP 8）、只用标准库、脚本文件用下划线前缀命名（`_xxx.py`）。

### 常见坑点（开发自查）

1. **路径错误**：工具页面引用公共资源时，深度是 `../../css/` 和 `../../js/`，不是 `../`。
2. **忘记运行构建**：新增工具后必须跑 `_build.py`，否则首页找不到。
3. **meta 标签缺失**：没有 `<meta name="toolbox">` 会导致分类错误。
4. **file:// 访问**：fetch 会失败，必须用本地服务器。
5. **直接修改构建产物**：不要手动改 `tools.json` / `sitemap.xml`，改了也会被覆盖。
6. **移动端忘记适配**：新增 UI 组件时记得加 `@media` 查询。

### 相关文件速查

| 文件 | 作用 | 修改频率 |
|---|---|---|
| `index.html` | 首页结构 | 低 |
| `css/style.css` | 首页样式 | 中 |
| `js/app.js` | 首页逻辑 | 中 |
| `css/common.css` | 工具页公共样式 | 低 |
| `js/common.js` | 工具页公共脚本 | 低 |
| `_build.py` | 构建脚本（含 SEO 注入/质量分级） | 中（新增分类时） |
| `scripts/*.py` | 批量生成器/审计/修复脚本 | 中（批量任务时用） |
| `_test_static.py` | 静态测试脚本 | 低 |
| `tools/<industry>/*.html` | 各工具页面 | 高（新增工具） |
| `json/*.json` | 数据文件 | 从不（构建产物） |
| `sitemap.xml` | 站点地图 | 从不（构建产物） |

### 开发工作流建议

#### 新增一个工具

1. 确定工具的行业（industry）和功能分类（cat）。
2. 在 `tools/<industry>/` 下创建 HTML 文件，使用标准模板。
3. 填写 `<meta name="toolbox">` 元数据。
4. 实现工具功能。
5. 本地测试工具页面（同时同步英文 i18n 与撰写使用指南，确认指南入口已注入工具页）。
6. 运行 `python3 _build.py`。
7. 测试首页中该工具显示正常。
8. 提交并发布。

#### 修改首页布局

1. 先改 `index.html` 的结构。
2. 再改 `css/style.css` 的样式。
3. 最后改 `js/app.js` 的逻辑。
4. 浏览器中验证桌面端和移动端。
5. 运行构建脚本（如果有数据变动）。
6. 提交并发布。

### todo.md 批量工具开发规则

> 项目维护的工具候选清单 `todo.md`（约 7000 行）用于指导后续开发 —— **该文件不入库**，本地缺失时向维护者索取。

**工作流（串行执行，见 AGENTS.md §6）**：

1. 读取 `todo.md`，找到尚未开发的工具。
2. 标注格式：`[已上线]` / `[已开发]` / `[重复]` / `[不可开发]`（附说明），处理完删除该条目。
3. 按分类顺序，每次开发一个类别的 5-10 个工具。
4. 每批完成后：运行 `python3 _build.py` → 本地测试 → 标注并删除已处理条目 → 提交并发布。

**开发优先级**：优先计算类/转换类/查询类（纯前端可实现）→ 生成器类/速查表类 → 跳过需实时数据/API/后端（标 `[不可开发]`）→ 跳过与现有重复（标 `[重复]`）。

**判断现有工具的方法**：检查 `tools/<industry>/` 目录、运行 `grep -r "关键词" tools/`、对照 `json/tools.json`。

---

## 相关文档

- [开发规范（AI 约束与坑点）](AGENTS.md)
- [全站优化计划](DEV-PLAN.md)
- [i18n 规范](docs/i18n-spec.md)
- [UI 设计规范](ui/设计规范.md)
