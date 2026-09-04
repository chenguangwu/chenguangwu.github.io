# ToolBox 多语言开发规范（v2）

> 适用范围：所有新增 / 修改的页面（首页、UI 模板、工具页、guides）。本规范为强制约束，新页面 PR 必须过质量门禁。
> 关联计划：根目录 `DEV-PLAN.md`。引擎实现：`js/i18n.js`。

---

## 1. 支持语言与 fallback

| locale | 说明 | fallback | dir |
|---|---|---|---|
| `zh-CN` | 默认中文 | — | ltr |
| `zh-TW` | 台湾繁体（OpenCC `twp`） | — | ltr |
| `en-US` | 默认 / 唯一全局回退英文 | — | ltr |

- `zh-CN` 是唯一源语言；`zh-TW` 由 `opencc-js` 在构建期生成静态页面和 JSON，不走英文回退。`en-US` 保留既有运行时词包。
- `zh-CN` 为默认语言，其语言包留空，靠 `data-i18n-fb` 回退原始中文。
- 繁体动态公共 UI 使用构建产物 `i18n/locale-zh-TW.json`；页面专有内容以静态 HTML 的繁体 `data-i18n-fb` 为回退。香港浏览器语言和旧 `zh-HK` 偏好统一归一化到 `zh-TW`。

## 2. 语言判定与持久化（优先级 高→低）

1. 物理繁体路径 `/zh-tw/...` —— 最高优先；切换到繁体必须整页导航到该路径
2. URL `?lang=<locale>` —— 英文运行时切换，写回 URL（`history.replaceState`）与 localStorage
3. localStorage `toolbox_lang`
4. `navigator.languages[0]` 的 region 子标签匹配 `REGION_MAP`（不自动把普通简体 URL 重定向到繁体）
5. 页面 `<html lang>`，最终回退 `zh-CN`

约束：每次切换必须 `document.documentElement.lang = locale`；首屏在 `<head>` 内联脚本完成判定，防闪烁。

## 3. 代码约定

### 3.1 静态文案
- 文本：`data-i18n="ns.key"`；placeholder：`data-i18n-ph="ns.key"`；title：`data-i18n-title="ns.key"`；中文兜底：`data-i18n-fb="中文原文"`。
- **禁止**在带 `data-i18n*` 属性的元素内硬写最终文案；最终文案只能来自语言包，兜底来自 `data-i18n-fb`。

### 3.2 语言包
- `I18n.PACKS[locale]` 按命名空间组织：`nav.*` `tool.*` `common.*` `cat_*`（分类）`ind_*`（行业）。
- key 全小写点分，禁中文 key；相同概念跨页面 key 必须一致。

### 3.3 动态 DOM（JS 生成）
- 必须调 `I18n.t(key)` / `indName(info, key)` / `catName(info, key)`，禁字符串硬写中文。
- 渲染后调用 `I18n.apply(root)`；监听 `toolbox:langchange` 事件，触发后所有动态视图须重渲染并 `apply`。
- 首页已内置 `_t/_ind/_cat` 与 `refreshI18nViews()` 钩子，新增动态视图照此模式。
- **工具卡片名/简介**：统一用 `_tn(t)` / `_td(t)`；仅 `en-US` 读取 `t.en` / `t.ed`，繁体静态页读取其目录内已 OpenCC 转换的 `json/*.json`。所有动态列表均经此二函数，**禁止**直接拼 `t.n` / `t.d`。

### 3.4 工具页
- 每生成页 `<head>` 必含 `<script src="js/i18n.js"></script>`（在 `common.js` 之前）。
- 语言切换按钮由 `autoMount()` 挂到 `.nav`（工具页已有 `.nav`）。
- 工具专属文案（标题 / h1 / h2 / intro / desc / 输入标签 / notes）一律走翻译字典，不硬编码中文。

## 4. 工具翻译（两层）

工具翻译分两层，v1 已全量落地**第一层**（卡片名/简介），第二层（页内正文）仅 6 个首页工具，其余留 v2。

### 4.1 工具名 / 简介（规则引擎 · v1 全量 5254 工具）

- **翻译引擎**：`scripts/zh_en_dict.py`（**语义短语级**规则翻译，**非 MT API**，符合纯前端约束）。
  - **禁用单字硬替（v2 硬约束）**：匹配表 `PHRASES` 只认 `>=2` 字中文短语 + 安全函数词（`的/和/与/转` 例外），**绝不许按单字替换**（早期"率→Rate/数→Number"式逐字翻译已移除，杜绝机械垃圾）。原则：**中文几个字 → 一个自然英文词/词组**，如 `贝叶斯后验概率 → Bayesian Posterior Probability`、`数据透视表 → Pivot Table`、`凯撒密码 → Caesar Cipher`。
  - `SEMANTIC`：语义短语层（ML/AI、密码学、数据工具、医疗护理、生活等长尾真实缺口，中文整段→自然英文词组）。
  - `TYPE_SUFFIX`：仅"X器"类真后缀（编解码器/转换器/生成器/计算器/校验器/解析器/模拟器…），按长度降序最长优先匹配，避免短后缀误命中。
  - `DOMAIN`：领域/修饰词→英文大词典（技术/数学/物理/金融/健康/教育/图像/游戏/通用动作等数百条）；弱动作词名词化（生成→Generator、计算→Calculator、转换→Converter、编码→Encoder、解码→Decoder）。
  - `ACTION_SUFFIX` + `X器` 通用后缀推断：按 X 的动作语义选设备后缀（默认 Device），并做**设备词去重**（修 `Score Scorer` 类双后缀）。
  - `translate_name()`：**丢弃**营销模板后缀（含"免费/在线工具/领域"的 `- xxx` 或 `（xxx）` 后缀直接丢弃），仅译主名；`工具` 空化去冗余。
  - `translate_text()`：类型后缀英文化 + 拆 ASCII/中文段 + 中文段短语级翻译 + 清理空格。
  - **安全回退（v2 关键约束）**：`translate_name` / `translate_text` 一旦结果仍含中文（整句未翻出），立即返回**干净原文中文**，绝不输出中英混杂乱码。这是不可违反的硬规则——英文模式最多"显示干净中文"，但永远不显示乱码。
  - **真实覆盖率（v2 实测）**：规则引擎（语义短语级）单用工具名干净英文 `en` 仅 ~19.5%（零中英混排垃圾）；叠加「slug 直译覆盖字典」后达到 **100%（5254/5254）**：`en`/`ed` 均为干净英文（无汉字、无全角标点）。含 ① slug 直译（绝大多数 slug 本就是英文）② 171 个 `calc-N` 占位符逐行业人工翻译 ③ 134 个拼音 slug 工具结合中文名+行业语境逐条人工翻译（老板要求、无 MT）④ 保守拼音判定（仅无连字符长串或拼音专属复韵母 iao/iang/uang/iong/ü 判拼音，剔除 van/uen 误伤英文词）。规则引擎上限根因：5254 工具名含 **4275 个不同"概念头"、长尾极散**——已被「slug 直译」绕过（绝大多数 slug 本就是英文，直接还原比逐字翻中文更准）。
- **构建期注入**：`_build.py` 在写出 `json/search-index.json`、`json/industry-*.json`、`json/tools.json` 前，对每个工具注入 `en = translate_name(name)`、`ed = translate_text(desc)`；带 `try/except` 兜底，缺失引擎不阻断构建。
- **运行时消费**：`js/app.js` 的 `_tn(t)` / `_td(t)` 取 `t.en` / `t.ed`，非 `zh-CN` 且字段存在即显示英文，否则回退 `t.n` / `t.name`。所有动态列表（分类浏览 / 质量筛选 / 热门·最近·收藏 / 搜索结果 / 移动端搜索 / 命令面板 cmdk）经此二函数渲染，无中文残留、无乱码。

- **slug 直译覆盖字典（已落地 · 老板拍板「批量预翻高频工具」）**：`scripts/gen_en_override.py` 构建期生成 `i18n/tools/_en_override.json`（覆盖字典现为全站 **5254 条**，每个工具一份 `en`/`ed`，构建期由 `gen_en_override.py` 一次性算出），`_build.py` 于三处注入点（industry JSON / search-index / tools.json）优先采用 `apply_en_override()` 覆盖规则引擎结果。机制：
  - ① 绝大多数工具 slug 本就是英文（如 `hex-to-text`），直接还原成自然英文标题 `Hex to Text`，质量高于逐字翻中文——这是覆盖率从 ~20% 跃升到 100% 的关键；
  - ② `calc-N` 占位符 slug 按中文名语义手翻（如 `finance/calc-2`→`IRR (Internal Rate of Return) Calculator`、`general/calc-13`→`Date Difference Calculator (Workdays / Calendar Days)`），共 171 个；
  - ③ 拼音 slug（`tanhuangsheji` 等长串 / `kouqiangai-tnm-shaichagongju` 含拼音专属复韵母）保守判定为拼音并回退干净中文，避免拼音直译垃圾；判定仅触发于「无连字符长串(>5字符)」或「含拼音专属复韵母 iao/iang/uang/iong/ü」——已剔除 `van`(advanced)、`uen`(influencer) 等英文词误判，且整体英文词/缩写优先（如 `stopwatch`/`stretch`/`torque` 不再误判）；
  - ④ 安全回退硬规则保证零中英混排垃圾。`_en_override.json` 为构建产物，重跑 `python3 scripts/gen_en_override.py` 刷新后由 `_build.py` 注入。覆盖字典对规则引擎已翻出英文 `en` 的工具统一写入 `slug_to_intro` 英文 `ed` 模板，消除工具页中文 `desc` 残留；写入逻辑不依赖 search-index 旧 `ed`，避免 `_build` 每轮重建致中文 `ed` 回流（已连跑两轮 gen+build 验证稳定）。若日后要更自然的描述，仍可选构建期接 MT 逐工具结合上下文产出 `en`/`ed`（产物仍是静态 JSON，与纯前端约束不冲突）。

### 4.2 工具页正文（字典 · v2 已全量落地 5254 工具）

- **两层字典并存**：
  - 第一层 `i18n/tools/<industry>.json`：`data-i18n` 驱动的页内专属内容（v1 仅 6 个首页工具含 `en-US`）。
  - 第二层 `i18n/tools/<industry>-body.json`：**v2 新增**，扁平 `{ "<slug>": { "title": <en>, "intro": <en> } }`，由 `scripts/gen_tool_i18n_en.py` 从 search-index 的 `en`/`ed` 生成（缺失则回退规则引擎），合并第一层手工 en-US（按工具真实行业路由，跨行业登记也能正确落入对应 `-body.json`）。供运行时动态翻译 h2 标题与简介段落。
- 运行时：`js/tool-i18n.js` 的 `loadIndustryBody(industry)` 拉取 `<industry>-body.json`，`applyToolBody()` 在加载/切语时按 slug 查表翻译 `.tool-card-accent h2` 与简介 `<p>`：保留 emoji 前缀、跳过公式 h2（`∑∫∂√≈≠≥≤×÷²³⁴⁵πΔΩμλσφθ`）、`data-i18n` 已管理页不重复处理、切回中文还原原文。英文模式下工具名/简介显示干净英文（高覆盖子集）或干净中文（安全回退，无乱码）。
- **生成流程**：`python3 scripts/gen_tool_i18n_en.py`（幂等；依赖最新 search-index，故须在 `_build.py` 之后运行）。

### 4.3 工具页正文（运行时精确短语映射 · 已全量部署）
- **机制（v2 实际落地）**：`js/tool-i18n.js` 在英文模式下对正文节点（h1/h3/h4/li/th/td/label/button/option/textarea/span/a/div）做**整节点精确匹配替换**，而非逐个加 `data-i18n`（给 5374 页逐个加 data-i18n 全站不现实）。
  - `GEN_UI_MAP`(~147 条)：label/button/option 等确定性 UI 词；
  - `BODY_PHRASE_MAP`(9069 条，逐批增长)：正文共享短语，零 MT、整节点精确匹配；
  - `translateBodyPhrases()`：英文模式遍历正文节点，命中映射即整段替换；未命中中文**原样保留**（安全回退，零中英混排）。
- **框架层**由 `applyChrome()` 处理（面包屑/按钮/等待输入/相关工具标题/使用说明标题）；h2+intro 由 `applyToolBody()` 走 `-body.json`（§4.2）；工具专属确定性内容由上述两映射表覆盖。
- **批译工程（2026-08）**：按正文短语节点频次 n 降序逐批人工手翻（老板要求无 MT、逐条认真），固化候选列表 `/tmp/cand_n2.json`（3474 条 n=2 共享词，即长尾硬上限）按切片取批。BODY_PHRASE_MAP 从 5795 增至 **9069 唯一键**，共享覆盖 **52.1%**（GENFRAME 19898 + BODY 113229 / 可见中文节点 255418）。
- **覆盖率见顶根因（如实告知）**：n=2 长尾（3474 条）已全部翻完；剩余可见中文节点全部来自 **n=1 长尾（86,110 条，单条仅出现 1 次，单会话不可穷尽）**。共享短语表「翻一条覆盖最多节点」红利耗尽后，覆盖率停在 ~52%——这是纯人工逐条翻译的物理天花板。运行时保证残留中文安全保留、零混排，英文模式最坏仅显示干净中文。
- **注入与键转义**：`/tmp/inject_body.py` 跳过已存在键、键值均转义 `\\` 与 `'`；健壮键提取正则 `re.findall(r"'(?:\\.|[^'\\])*':", block)` 后还原转义，根治转义键顽疾。
- **门禁**：四道全过（`_test_static.py` / `_audit_links.py --check` / `_audit_assets.py --check` / `node scripts/verify_calc.js`）。
- **后续若逼近 100%**：须切到「逐工具逐页」粒度预翻其 n=1 独有短语，成本随 5374 页线性放大；或接受 ~52% 共享覆盖 + 运行时安全回退现状。

## 5. SEO 约定（构建期注入，禁手工维护）

由 `_build.py` 基于 `I18N_LOCALES`（`zh-CN`、`zh-TW`、`en-US`）自动生成：

- 每页 `<head>` 注入完整 hreflang 链；`zh-TW` 指向物理目录，只有 `en-US` 使用 `?lang=en-US` 运行时切换。
- `/zh-tw/...` 是独立可抓取的实体 HTML且 canonical 自指；`zh-CN` 指向源路径，`en-US` 继续是源路径的 `?lang=en-US` 运行时版本。
- `hreflang="x-default"` 指向简体源 URL；根 sitemap 为简体和台湾繁体 URL 输出独立 `<url>`。语言 alternate 关系由每页静态 `<head>` 声明，不在 sitemap 内重复数万次。
- `<meta property="og:locale" content="zh_CN">`（页面原生语言，下划线写法） + `og:locale:alternate` 列出其余 locale（如 `en_US`）。
- JSON-LD `@type: WebApplication` 块含 `"inLanguage": ["zh-CN", "en-US"]`，声明该页覆盖当前 2 种语言。
- `<link rel="canonical">` **保持**指向页面原生裸 URL（标准做法，不随语言变 `?lang`）。
- 全站只生成根 `sitemap.xml`，不再生成各行业重复 sitemap。

**索引性保障**：GitHub Pages 直接响应繁体正文与完整 SEO head，不依赖爬虫执行应用脚本。生成器只复制 HTML 与 JSON；CSS、JS、字体、图片保持根路径共享，避免重复公共资产。OpenCC 仅用于构建期通用转换；品牌、术语等需要精校时在 `twp` 覆盖层处理，不修改 `zh-CN` 源文。

## 6. 质量门禁

- 既有（发布前必过）：`_test_static.py`（0 失败 0 告警）、`_audit_links.py --check`（0 死链）、`_audit_assets.py --check`（0 资产死链 / 0 lang 缺失 / 0 重复 id）、`node scripts/verify_calc.js`（公式 ALL OK）。
- 新增 i18n 检查：
  - (a) 所有 `.html` 含 `js/i18n.js` 与 `<html lang>`；
  - (b) 带 `data-i18n*` 属性的元素无硬编码最终文案（正文 ≠ 其 en-US 翻译）；
  - (c) 每 locale 的 `nav.*/common.*` 键全覆盖，缺失 CI 失败；
  - (d) hreflang 链含 `x-default` 且链接可达；
  - (e) 工具字典 key 与 `gen` 脚本 `TOOLS` 的 slug/input.id 一一对应。
- PR 未过门禁不得合并。

## 7. Non-goals（v1 不做什么）

- 仅保留 `zh-CN` / `zh-TW` / `en-US`，不启用其他语种、不启用 RTL。
- 翻译数学公式 / 符号 / 单位本身（如 `ax²+bx+c=0`、`Δ`、`√` 保持原样），仅译说明文字。
- 后端 / SSR i18n，维持纯前端 + 构建期注入。
- 接入机器翻译 API（字典由人工 / 构建脚本维护）。

## 8. 提交与上线

- 每批次独立 commit/push：`git add -A && git commit -m "feat(i18n): <批次>" && git push origin master`（触发 GitHub Pages）。
- 异常即 `git revert <sha>` 后 push，纯前端回退即恢复旧 JS/HTML。
- 索引提交（IndexNow/Bing/GSC）由用户侧 cron 自动运行，会话内不手动触发。
