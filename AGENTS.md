# AGENTS.md - ToolBox 项目 AI 开发规范

> **重要**：所有 AI Agent 在开发本项目时，必须严格遵守本文件中的约束和规范。

---

## 📋 项目概览

**项目名称**：ToolBox - 6000+ 免费在线工具百科

**技术栈**：纯前端 HTML5 + CSS3 变量主题 + 原生 ES6 JavaScript + Python 3 构建脚本

**部署方式**：GitHub Pages 静态托管（Deploy from a branch，`.nojekyll` 强制纯静态直发）

**核心特性**：
- 响应式设计（桌面 + 移动端底部Tab栏）
- 6277 工具，256 个子行业目录
- 纯前端处理，数据不上传
- 活泼专业的视觉风格
- AI 工具（浏览器本地推理）、工具链组合、中英双语 i18n、PWA 离线、质量分级

---

## 🎨 设计规范（必须遵守）

> **重要**：所有UI开发必须遵循 `ui/设计规范.md` 中的完整设计规范。

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

### 渐变方案

```css
--gradient-primary: linear-gradient(135deg, #FF6B35, #7C3AED);
--gradient-hero: linear-gradient(135deg, #FFF5F0 0%, #F3F0FF 50%, #F0FDFB 100%);
--gradient-btn-hover: linear-gradient(135deg, #E55A25, #6B2FD9);
```

### 圆角规范

| 元素 | 圆角 | Tailwind |
|------|------|----------|
| 按钮 | 12px | `rounded-xl` |
| 卡片 | 16px | `rounded-2xl` |
| 输入框 | 12px | `rounded-xl` |
| 标签 | 全圆 | `rounded-full` |
| 模态框 | 24px | `rounded-3xl` |

### 技术栈要求

- **CSS框架**：Tailwind CSS v4 Browser CDN
- **图标库**：Lucide Icons (通过 `data-lucide` 属性声明)
- **字体**：Noto Sans SC + Plus Jakarta Sans

### Tailwind 配置

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

> 完整设计规范请参阅：`ui/设计规范.md`

---

## 🏗️ 目录结构（严格遵守）

```
chenguangwu.github.io/
├── index.html              # 首页入口（侧边栏布局）
├── css/
│   ├── style.css           # 首页样式（侧边栏布局、响应式）
│   └── common.css          # 工具页公共样式（所有工具共用）
├── js/
│   ├── app.js              # 首页逻辑（动态加载、侧边栏交互）
│   ├── common.js           # 工具页公共脚本（ToolBox 命名空间）
│   ├── i18n.js             # 中英双语 i18n 引擎（首页）
│   ├── freemium.js         # Freemium：AI 工具每日限额 + 解锁（AI 工具页引入）
│   ├── ai-core.js          # Transformers.js 纯前端 AI 共享加载器（AI 工具用）
│   ├── chart.js            # 零依赖 Canvas 图表库（懒加载，data-viz 用）
│   └── qrcode.js           # 二维码库（第三方，MIT）
├── json/
│   ├── tools.json          # 全量工具数据（备用，非首页使用）
│   ├── search-index.json   # 轻量搜索索引（首次搜索时加载）
│   ├── industry-*.json     # 按行业拆分数据（256 个，与子行业目录一一对应）
│   ├── guides.json         # 工具页 → 使用指南映射（common.js 读取注入「📖 使用指南」）
│   └── channel.json        # 渠道/分类配置
├── tools/                  # 工具页面（按 256 个子行业分子目录）
│   ├── it/  finance/  design/  biz/  marketing/  science/  health/
│   ├── life/  edu/  legal/  fun/  travel/   # ← 原始 12 个一级行业
│   ├── ai/  encode/  eco/  photo/  statistics/  healthcare/  ...  # ← 其余细分行业
│   └── <industry>/index.html   # 每个子行业目录下的分类落地页（构建脚本自动生成，非工具）
├── guides/                 # 使用指南（31 篇 + index.html 指南中心）
├── scripts/                # 开发/生成脚本（批量工具生成、SEO 审计修复、指南生成等）
│   ├── gen_itools_t1.py / gen_itools_t2.py / gen_itools_t2b.py / gen_tiny_t1.py  # 批量工具生成器
│   ├── gen_guides2.py      # 指南生成器
│   ├── audit_seo.py        # SEO 审计脚本
│   └── seo_fix2.py         # SEO 批量修复脚本
├── chains.html             # 工具链组合页（B3-05）
├── embed.html              # 工具嵌入 API 文档
├── search.html             # 站内搜索页
├── _build.py               # 构建脚本（最重要的脚本，含 SEO/结构化数据/面包屑注入）
├── _test_static.py         # 静态测试（标题/元数据/结构合规检查，忽略分类落地页与重定向桩）
├── _submit_indexnow.py     # IndexNow 索引提交（每日 14:00 crontab）
├── _submit_bing_url_api.py # Bing URL 提交（每日 15:00 crontab，--yes 非交互）
├── _gsc_submit_sitemap.py  # Google Sitemaps 提交（每日 15:30 crontab）
├── _gsc_inspect_urls.py    # Google 收录监控（每日 16:00 crontab，--limit 1900）
├── _gen_blank_tools.py     # 空白行业批量填充生成器（历史）
├── _gen_guides.py          # 指南生成器（历史 20 篇，新版在 scripts/gen_guides2.py）
├── _add_tools.py           # 批量工具生成脚本（历史）
├── sitemap.xml             # SEO 站点地图（构建产物，全量 urlset ~6600 URL）
├── sitemap.html            # 可视化站点地图（构建产物）
├── robots.txt              # 爬虫规则
├── og-image.png            # 1200×630 社交分享图（全站 og:image 引用，勿删）
├── README.md               # 项目说明
├── AGENTS.md               # 本文件
└── tools.json              # 根目录备份（构建产物）
```

---

## 🚫 硬性约束（必须遵守）

### 1. 纯前端原则
- **禁止**引入任何后端服务、API 调用（第三方 CDN 除外，但尽量避免）
- **禁止**使用任何需要 npm/yarn/pnpm/bun 的构建工具链（React/Vue/Angular/TS 等都不行）
- **禁止**添加任何构建配置文件（package.json / vite.config / webpack.config 等）
- 所有工具必须能在浏览器中直接运行，双击 HTML 即可用

#### ❌ 禁止开发的工具类型（需要后端服务）
以下类型的工具需要后端 API 或实时数据，禁止添加：
- **实时数据类**：天气预报、股票行情、汇率换算、加密货币价格、新闻资讯
- **位置服务类**：地图导航、路线规划、GPS 定位、附近搜索、物流追踪
- **社交媒体类**：微信/微博/抖音等平台数据、分享功能、登录认证
- **AI 服务类**：AI 聊天、AI 生图、语音识别(TTS/ASR)、OCR 识别
- **第三方服务类**：邮件发送、短信验证、支付接口、快递查询、航班查询
- **数据库依赖类**：品种数据库、药品数据库、保险报价、教育基金

#### ✅ 允许开发的工具类型（纯前端可用）
以下类型的工具可以用纯前端技术实现，允许添加：
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
- **新的开发脚本一律放 `scripts/` 子目录**（批量生成器/审计/修复等），不要放根目录

### 4. 构建系统约束
- 添加/修改工具后，**必须**运行 `python3 _build.py` 更新索引
- 静态测试：`python3 _test_static.py` 必须 0 失败 0 告警
- 死链门禁：`python3 _audit_links.py --check` 必须 exit 0（0 死链）。该脚本智能排除 `<script>/<style>` 块内的教学示例与 JS 运行时伪链（`$1`/`${}`），避免误报；发布前必须跑通
- 资产完整性门禁：`python3 _audit_assets.py --check` 必须 exit 0（0 局部资产死链 / 0 `<html lang>` 缺失 / 0 页面内重复 id）。同样排除 `<script>/<style>` 块示例与 GSC/Bing 验证文件（无 `<html>` 标签），避免误报；发布前必须跑通
- **不要手动修改** `json/*.json` 和 `sitemap.xml`，它们是构建产物
- 不要手动修改 `index.html` 中的工具列表/统计数据，它们由构建脚本注入
- **所有公开页面必须引用 `/js/common.js`**（工具页/行业落地页/首页由 `_build.py` 统一注入；guides/静态页等非 `_build.py` 处理的页面须手动保留该引用，遗漏可用 `python3 scripts/inject_common_js.py` 幂等补全）。`js/common.js` 会在加载时兜底补引统一统计入口 `js/analytics.js`，因此「引 common.js」即同时获得公共功能与百度/Clarity/51.la 统计覆盖。**例外：Google 站点验证文件（`google*.html`）不引入任何脚本、保持原样。**

### 4.5 索引提交约定（重要）
- **不要自动执行**索引提交（全量跑约 19 分钟，拖慢会话）
- 每次 `_build.py` 重建后，**只提醒用户手动运行** `python3 _submit_indexnow.py`
- 定时任务已由用户终端 crontab 管理：IndexNow 14:00 / Bing 15:00 / GSC Sitemap 15:30 / GSC 收录监控 16:00

### 5. 兼容性约束
- 不要使用过于激进的新特性，确保主流浏览器（Chrome/Safari/Firefox/Edge 最近两个大版本）可用
- CSS 优先使用变量（CSS Variables），不要硬编码颜色值
- 移动端必须可用，不能只做桌面端

### 6. 单 Agent 串行执行（禁止多 Agent 并行）
**本项目同一时刻只允许一个 agent 对仓库做写操作，全部任务由主 agent 串行推进，一个干完再干下一个。**

- **禁止**为同一批任务派生多个子 agent / 后台 agent 并行干活（包括并行写文件、并行跑 `_build.py`、并行 commit）
- **禁止**创建多 agent 团队（`TeamCreate` / teammate 分工）并发修改本仓库
- **主 agent 自顶向下串行执行**：一个子任务完整收口（改完 → 跑通门禁 → 提交）后，才允许开始下一个子任务，禁止中途开第二条线
- 唯一例外：**纯只读**的检索/探查类子任务（不写任何文件、不动 git、不跑构建）可并行；一旦涉及写入，一律回到串行。拿不准时按串行处理

**为什么必须串行**（本项目共享同一份工作区与 git 仓库，并发会真实出事）：
- `_build.py` 全量重写 `json/*.json`、`sitemap.xml`、`index.html` 等构建产物，并发跑会互相覆盖，产出残缺索引
- 多个 agent 同时 `git add/commit` 会触发 `.git/index.lock` 冲突，导致提交丢失或仓库卡死
- 门禁（`_test_static.py` / `_audit_links.py --check` / `_audit_assets.py --check`）结果依赖"当前工作区是完整且稳定的"，并发改动会让门禁结论不可信
- 批量改动要求合并提交，并行会让提交历史碎片化、难以回滚

**与自动化任务的互斥**：定时看门狗等自动化 agent 与人工会话共用本仓库，靠 `.workbuddy/watchdog.lock`（含 `started_at` / `last_heartbeat` / `run_id`）互斥——检测到心跳仍在有效期即视为"另有 agent 在干"，本次直接跳过，不碰代码、不动 git。任何新增的自动化任务必须遵守同一把锁。

---

## 🛠️ 构建脚本 `_build.py` 详解

这是项目最重要的脚本，负责整个项目的索引生成。

### 功能清单
1. 递归扫描 `tools/` 目录下所有 HTML 文件
2. 从 `<meta name="toolbox">` 标签提取元数据
3. 根据文件名和关键词自动分配功能分类（cat）和行业（industry）
4. 生成 `json/tools.json` 全量数据
5. 生成 `json/industry-*.json` 按行业拆分数据（256 个）
6. 生成 `json/search-index.json` 轻量搜索索引
7. 更新 `index.html` 中的统计数据
8. 生成 `sitemap.xml` 站点地图（**全量 urlset**，含 guides/ 与 chains.html，约 6600 URL）
9. **SEO 注入**（`fix_tool_pages_seo`，幂等）：h1、面包屑导航、BreadcrumbList + WebApplication JSON-LD、og:image/twitter:image、相关工具区
10. **质量分级**（`classify_quality`）：按页面独有脚本量分 A/B/C 三级

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
- 全小写英文，单词用连字符 `-` 分隔
- 如：`bmi-calculator.html`、`json-formatter.html`
- 放入对应行业子目录：`tools/<industry>/xxx.html`

### 2. 行业分类（200+ 细分行业，256 个子目录）

> 项目已远超最初 12 个一级行业，现按 **256 个子行业目录** 组织（如 `cardiology`、`metallurgy`、`agriculture`、`automotive` 等）。`industry` 字段取值即目录名，由构建脚本从 `<meta name="toolbox">` 读取，**无需在本文穷举**——新增子行业直接新建目录即可，构建会自动生成对应 `industry-<dir>.json` 与分类落地页 `index.html`。

**原始 12 个一级行业（仍是最常用的 industry 取值）：**

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

> `cat` 取值同样由元数据声明，下面为常用值，并非封闭清单。

| 代码 | 名称 |
|------|------|
| `text` | 文本处理 |
| `encode` | 编码解码 |
| `convert` | 格式转换 |
| `generate` | 生成器 |
| `dev` | 开发工具 |
| `design` | 设计工具 |
| `image` | 图片处理 |
| `math` | 数学计算 |
| `validator` | 验证器 |
| `reference` | 速查表 |
| `game` | 游戏趣味 |
| `finance` | 金融投资 |

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
- **路径要正确**：工具在 `tools/it/xxx.html`，所以引用公共资源要用 `../../css/common.css`
- **使用公共样式类**：`.nav`、`.container`、`.card`、`.btn`、`.btn.primary`、`.toolbar`、`.result-box`、`.input-row`
- **使用公共脚本方法**：`ToolBox.showToast()`、`ToolBox.copyText()`、`ToolBox.downloadText()`、`ToolBox.toggleToolTheme()`
- **主题切换按钮必须有**，调用 `ToolBox.toggleToolTheme()`

### 6. 中英文与指南三项同步（强制）

新增任意工具时，必须**一次性同步**以下三项，缺一不可，否则视为该工具未完成：

1. **中文工具页**（默认必备）：`tools/<industry>/<slug>.html`，标题/简介/正文为中文。
2. **英文 i18n 双轨**：
   - 卡片名写入 `i18n/tools/slug-en.json`（键 = `行业/slug`）；
   - 标题/简介写入 `i18n/tools/_en_override.json`，值必须是**嵌套 dict** `{en, ed, ind}`，**绝不能写成字符串**（否则 `_build.py apply_en_override` 报 `AttributeError: 'str' object has no attribute 'get'`）；
   - 注入脚本推荐范式：在 JSON 首 `{` 后插入新键块，避免整体重写破坏其他键格式。
3. **使用指南**：生成 `guides/<slug>-guide.html`，合并进 `json/guides.json`（按 `tool` 字段关联工具页），并向 `js/guide-en-pack.js` 导出英文键；指南需含中英双语全套字段（`name/desc/intro/features/scenarios/steps/tips/faqs` 及对应 `en_*`），且指南页“去使用”链接的 `tools/<industry>/` 必须与工具页**真实目录一致**（构建前用 `tools/` 实际路径核对，勿凭生成器 docstring 推断）。

> 历史教训：Q1 三批 39 个工具曾先上线、后分两批补指南与英文，造成二次返工；此后新增工具必须**三件齐发**，随工具页同一批次提交。

---

## 🎨 首页开发规范

### 1. 布局结构

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

### 2. 数据加载流程

```
页面加载
  ↓
加载默认行业 (it) 的 industry-it.json
  ↓
渲染工具网格
  ↓
用户点击其他行业 → fetch 对应 industry-*.json → 渲染
用户搜索 → 首次搜索时 fetch search-index.json → 全量搜索
  ↓
已加载的行业缓存在内存中（loadedIndustries 对象）
```

### 3. 关键状态变量（在 `js/app.js` 中）

| 变量 | 说明 |
|------|------|
| `currentIndustry` | 当前选中的行业代码，默认 `'it'` |
| `currentCategory` | 当前选中的功能分类，默认 `'all'` |
| `searchQuery` | 当前搜索关键词 |
| `currentTools` | 当前行业的工具数组 |
| `allSearchIndex` | 全量搜索索引（搜索时才加载） |
| `loadedIndustries` | 已加载行业的缓存对象 |
| `favorites` | 收藏列表（localStorage） |
| `recents` | 最近使用（localStorage） |

### 4. CSS 变量规范

定义在 `css/style.css` 和 `css/common.css` 的 `:root` 和 `body.dark` 中：

| 变量 | 用途 |
|------|------|
| `--bg-body` | 页面背景色 |
| `--bg-sidebar` | 侧边栏背景色 |
| `--bg-card` | 卡片背景色 |
| `--bg-hover` | 悬停背景色 |
| `--bg-active` | 激活背景色 |
| `--text-primary` | 主文字色 |
| `--text-secondary` | 次文字色 |
| `--text-muted` | 弱文字色 |
| `--border-color` | 边框色 |
| `--primary` | 主题色（靛蓝） |
| `--primary-hover` | 主题色悬停 |

---

## 🔍 搜索机制

### 两阶段搜索

1. **无搜索时**：只加载当前行业数据（~6-54KB），性能好
2. **有搜索时**：懒加载 `search-index.json`（~89KB，精简字段），在全量数据中搜索

### search-index.json 字段说明

字段都用单字母缩写，减小体积：

| 字段 | 全名 | 说明 |
|------|------|------|
| `n` | name | 工具名称 |
| `d` | desc | 工具描述 |
| `i` | industry | 行业代码 |
| `c` | cat | 功能分类代码 |
| `u` | url | 工具 URL |
| `ic` | icon | 图标 Emoji |
| `b` | bg | 背景色 |

---

## 🧪 本地测试规范

### 启动本地服务器

```bash
cd /Users/cgw/project/cgw/chenguangwu.github.io
python3 -m http.server 8765
```

访问：http://localhost:8765

### 测试清单

修改代码后，至少验证以下内容：

- [ ] 首页加载正常，默认行业工具显示正确
- [ ] 侧边栏点击行业，动态加载正确
- [ ] 搜索功能正常（跨行业搜索）
- [ ] 主题切换正常（浅色/深色）
- [ ] 工具卡片点击跳转正常
- [ ] 工具页面公共样式/脚本加载正常
- [ ] 移动端布局正常（<768px）
- [ ] 收藏功能正常（localStorage 持久化）

### 不要依赖 file:// 协议

因为使用了 `fetch` 加载 JSON，必须通过 HTTP 服务器访问，不能直接双击 HTML。

---

## 📦 发布流程

1. 本地开发和测试完成
2. 运行 `python3 _build.py` 确保索引最新
3. `git add -A` 暂存所有改动
4. `git commit -m "feat: xxx"` 提交
5. `git push origin master` 推送到 GitHub
6. GitHub Pages 会自动部署，几分钟后生效

---

## 📜 代码风格

### HTML
- 2 空格缩进
- 属性用双引号
- 语义化标签优先

### CSS
- 2 空格缩进
- 优先使用 CSS 变量，不要硬编码颜色
- 按布局 → 组件 → 状态的顺序组织
- 移动适配写在底部

### JavaScript
- 2 空格缩进
- 优先使用 `const`，其次 `let`，不用 `var`
- 函数表达式优先，不滥用 class
- 用模板字符串，不用字符串拼接
- DOM 操作尽量精简，避免频繁重排

### Python
- 4 空格缩进（PEP 8）
- 只用标准库，不要引入第三方依赖
- 脚本文件用下划线前缀命名（`_xxx.py`）

---

## ⚠️ 常见坑点

1. **路径错误**：工具页面引用公共资源时，深度是 `../../css/` 和 `../../js/`，不是 `../`
2. **忘记运行构建**：新增工具后必须跑 `_build.py`，否则首页找不到
3. **meta 标签缺失**：没有 `<meta name="toolbox">` 会导致分类错误
4. **file:// 访问**：fetch 会失败，必须用本地服务器
5. **直接修改构建产物**：不要手动改 `tools.json` / `sitemap.xml`，改了也会被覆盖
6. **移动端忘记适配**：新增 UI 组件时记得加 `@media` 查询

---

## 🔗 相关文件速查

| 文件 | 作用 | 修改频率 |
|------|------|----------|
| `index.html` | 首页结构 | 低 |
| `css/style.css` | 首页样式 | 中 |
| `js/app.js` | 首页逻辑 | 中 |
| `css/common.css` | 工具页公共样式 | 低 |
| `js/common.js` | 工具页公共脚本 | 低 |
| `_build.py` | 构建脚本（含 SEO 注入/质量分级） | 中（新增分类时） |
| `scripts/*.py` | 批量生成器/审计/修复脚本 | 中（批量任务时用） |
| `_test_static.py` | 静态测试脚本 | 低（质量检查时用） |
| `tools/<industry>/*.html` | 各工具页面 | 高（新增工具） |
| `json/*.json` | 数据文件 | 从不（构建产物） |
| `sitemap.xml` | 站点地图 | 从不（构建产物） |

---

## 🎯 开发工作流建议

### 新增一个工具

1. 确定工具的行业（industry）和功能分类（cat）
2. 在 `tools/<industry>/` 下创建 HTML 文件，使用标准模板
3. 填写 `<meta name="toolbox">` 元数据
4. 实现工具功能
5. 本地测试工具页面
5.5 同步英文 i18n（`slug-en.json` + `_en_override.json`）并撰写使用指南（`guides/`，见 §6 三项同步），确认指南入口已注入工具页
6. 运行 `python3 _build.py`
7. 测试首页中该工具显示正常
8. 提交并发布

### 修改首页布局

1. 先改 `index.html` 的结构
2. 再改 `css/style.css` 的样式
3. 最后改 `js/app.js` 的逻辑
4. 浏览器中验证桌面端和移动端
5. 运行构建脚本（如果有数据变动）
6. 提交并发布

---

## 📋 todo.md 批量工具开发规则

项目根目录下的 `todo.md` 是推荐工具清单（7000+ 行，数百个工具建议）。AI Agent 继续开发工具时，应遵循以下规则：

### 工作流

> **串行执行**：本节所有步骤由主 agent 一个一个干（见「硬性约束 §6 单 Agent 串行执行」）。禁止把一批 5-10 个工具拆给多个子 agent 并行生成。

1. **读取 todo.md**：每次开发前，读取 `todo.md` 文件，找到尚未开发的工具
2. **标注格式**：每个工具名称后用以下标记标注开发状态：
   - `[已上线]` — 工具已开发并部署，可直接删除该条目（工具已存在于 `tools/` 目录和构建索引中）
   - `[已开发]` — 本次开发完成，确认上线后可直接删除该条目
   - `[重复]` — 与现有工具重复，可直接删除该条目，附说明
   - `[不可开发]` — 需要后端/API/外部依赖，可直接删除该条目，附原因
3. **分批次开发**：按 todo.md 中的分类顺序，每次开发一个类别的 5-10 个工具
4. **每批完成后**：
   - 运行 `python3 _build.py` 更新索引
   - 本地测试新工具页面正常
   - 在 `todo.md` 中标注开发结果，确认无误后删除已处理条目，保持 todo.md 只含待开发项
   - 提交并发布

### 开发优先级

1. 优先开发计算类、转换类、查询类工具（纯前端可实现）
2. 其次开发生成器类、速查表类工具
3. 跳过需要实时数据/API/后端的工具（标注 `[不可开发]`）
4. 跳过与现有工具功能重复的（标注 `[重复]`）

### 判断现有工具的方法

- 检查 `tools/<industry>/` 目录下是否已有类似文件
- 运行 `grep -r "关键词" tools/` 搜索功能相似的工具
- 对照 `json/tools.json` 中的工具列表

### 批量开发脚本参考

批量创建工具时，可参考 `_add_tools.py` 脚本的模板生成方式，但每个工具的功能代码必须独立实现，不能用占位符。

---

> **最后更新**：2026-09-03（新增「硬性约束 §6 单 Agent 串行执行」）
> 
> 本文件是 AI 开发本项目的权威指南，如有疑问以本文件为准。
