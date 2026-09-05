# HTML 大文件优化任务清单

> 生成时间：2026-09-05
> 扫描范围：项目根目录全部 `*.html`（排除 `node_modules/`、`.git/`、`zh-tw/`、`.workbuddy/`）
> 阈值：**原始体积 > 200 KB（204800 字节）**
> 排除项：分类落地页 `tools/<industry>/index.html`（共 276 个，构建脚本 `generate_category_index()` 自动生成，非人工维护）

---

## 〇、优化执行结果（2026-09-05 已完成）

> 老板要求：**sitemap.html 不动，其余全部优化，繁体页关联改动一并处理。**

| 任务 | 状态 | 实测效果 |
|------|------|----------|
| P0-1 `sitemap.html` | ⏭️ 跳过（老板明确不处理） | — |
| P1 移除 critical-css 冗余 | ✅ 完成 | 全站 HTML（含繁体）250.0MB → **113.2MB（-54.7%）**；五道门禁全过；实机验证 `criticalCss=false`、本地资源零错误 |
| P2 五个超大工具页外置 JS | ✅ 完成 | `tools/{chinese-culture, bigfive-personality-test, colorblind-simulator, scl90-assessment, cognitive-assessment}.html` 的 49–74KB 内联脚本外置到 `js/tools/*.js`（绝对路径引用）；繁体页同步；A 级 100% 保持 |
| 繁体页关联改动 | ✅ 完成 | 繁体页 CSS 绝对路径 `/css/common.css`、外置 JS 正确引用、`data-zh` 正确转繁体；实机验证简/繁共 4 页全过 |
| 历史缺陷修复 `lorem-ipsum-advanced` | ✅ 完成 | 修复文案 `<p>` 未转义导致 116 行 JS 被当文本暴露的缺陷；A 级恢复；`data-zh` 注入正确落位 |

**改动文件**：`_build.py`（移除两处 critical-css 注入 + 修复 own_len 统计外置脚本）、`scripts/drop_critical_css_guides.py`、`scripts/extract_inline_scripts.py`、`js/tools/*.js`（5 个外置脚本）、全站 HTML（critical-css 移除 + data-zh 注入 + 外置引用）。

---

## 一、扫描结论（先看这个）

| 指标 | 数值 |
|------|------|
| 全站 HTML 总数 | 5646 个，合计 **250.0 MB** |
| 分类落地页（本次排除） | 276 个，合计 12.4 MB |
| 其余页面 | 5370 个，合计 237.7 MB |
| **>200KB 且排除分类页** | **1 个**（`sitemap.html`，且为构建产物） |
| >200KB 的分类页（已排除） | 1 个（`tools/it/index.html`，275 KB） |

**结论：严格按 200KB 口径，真正的「工具页 / 普通页」一个都没超。** 全站最大的非分类页是 `tools/chinese/chinese-culture.html`（161 KB）。

但文件「感觉很大」是真实的，根因不在单页，而在**全站复制的冗余代码**——见第三节。这是本清单的核心任务。

---

## 二、P0 — 严格命中 >200KB（排除分类页）

| # | 文件 | 原始 | gzip | 类型 | 状态 |
|---|------|------|------|------|------|
| P0-1 | `sitemap.html` | 537 KB | 131 KB | 构建产物（`_build.py:287` `HTML_SITEMAP_FILE` 生成，已 git 跟踪） | ⬜ 待办 |

**P0-1 根因**：单页内平铺全站 5000+ 工具链接，每个链接重复输出完整 HTML 结构，无分页、无折叠。

**优化方向**（改 `_build.py`，不要手改 HTML，手改会被下次构建覆盖）：
1. 按一级行业分组 + `<details>` 折叠，首屏只展开顶层，链接节点改为纯 `<a>`（去掉包裹元素与重复属性）。
2. 或改为分页（每页 ≤500 条），拆成 `sitemap.html` + `sitemap-<industry>.html`。
3. 目标：原始 ≤150 KB / gzip ≤40 KB。

**验收**：`python3 _build.py` 后 `sitemap.html` < 150KB；浏览器打开首屏可正常展开、链接可点击；死链门禁 `python3 _audit_links.py --check` exit 0。

---

## 三、P1 — 全站级根因：内嵌 critical-css 冗余（最高价值）

> 这是「HTML 文件非常大」的真正原因，改一处、全站 5646 页同时瘦身。

### 事实

| 项 | 数据 |
|----|------|
| 每页内嵌块 | `<style id="critical-css">…</style>`，由 `_build.py` 注入（`CRITICAL_TOOL_CSS`，第 2804 / 3003 行） |
| 单块体积 | **23–24 KB** |
| 覆盖率 | 抽样 80 个 HTML，**100% 命中**，其中 74 个与基准**逐字节完全相同** |
| 全站冗余 | 约 **132.4 MB**，占全站 HTML 总体积 **53%** |

### 问题定性

23 KB 对「首屏关键 CSS」明显超标。业界共识是 critical CSS 应控制在 **14 KB 以内**（首屏 TCP 初始拥塞窗口），超出部分不会带来首屏收益，只会让每个 HTML 白白膨胀。当前块内混入了大量**非首屏样式**，例如：

```css
body.dark .tb-mobile-drawer-close { background:#252540; color:#94a3b8; }
body.dark .tb-mobile-section-item a:hover { … }
```

移动端抽屉、暗色交互态这类样式属于首屏之后才可能触发的内容，没有内联的必要。

### 优化方案（推荐 B）

| 方案 | 做法 | 收益 | 代价 / 风险 |
|------|------|------|-------------|
| A. 整体外链 | 整块抽成 `css/common.css`，页面改 `<link>` | 每页减 ~23KB，全站减 ~130MB，改动最小 | 新增一次阻塞渲染的 CSS 请求；缓存命中时反而更快，冷访可能略慢 |
| **B. 拆分（推荐）** | 首屏核心样式（布局/字体/主题变量）保留内联，**控制在 ≤14KB**；其余（暗色交互态、移动端抽屉、动画、非首屏组件）外链到 `css/common.css` 并加长效缓存 | 每页减 ~10KB，全站减 ~56MB；保住内联关键 CSS 的首屏优势 | 需人工界定首屏样式边界，改动较大 |
| C. 仅压缩 | 用 cssnano/lightningcss 压缩后再内联 | 每页减约 8–10KB，改动小、风险低 | 收益小于 A/B，且仍无法利用浏览器缓存 |

**稳妥路径**：先做 **C（低风险，立刻见效）**，验证视觉无回归后再推进 **B**。

### 验收（硬性）

1. `python3 _build.py` 重建通过，无报错。
2. 五道门禁全绿：`python3 scripts/run_gates.py`。
3. 关键页面视觉回归：首页、一个工具页、`/zh-tw/` 繁体首页，比对 `_regression_shots/` 基线截图。
4. 目标：抽样工具页原始体积下降 ≥ 8 KB。

---

## 四、P2 — 次级大文件（100–200 KB，工具页）

> 未达 200KB 阈值，但已明显偏大，且都在 P1 之外还有各自的膨胀源。建议 P1 完成后复查实际体积再定优先级。

| # | 文件 | 原始 | gzip | 构成（style / 内联 script / 其他） |
|---|------|------|------|-----------------------------------|
| P2-1 | `tools/chinese/chinese-culture.html` | 161 KB | 56 KB | 31KB / 67KB / 12KB |
| P2-2 | `tools/psychology/bigfive-personality-test.html` | 135 KB | 48 KB | 30KB / 78KB / 7KB |
| P2-3 | `tools/colorvision/colorblind-simulator.html` | 107 KB | 30 KB | 30KB / 54KB / 15KB |
| P2-4 | `tools/psychology/scl90-assessment.html` | 106 KB | 35 KB | — |
| P2-5 | `tools/cognition/cognitive-assessment.html` | 105 KB | 30 KB | — |

**共同特征**：扣除 P1 的 ~23KB critical-css 后，剩余主体是**单个巨型内联 `<script>` 块**（P2-1 为 63KB、P2-2 为 74KB、P2-3 为 50KB），内容基本是**题库 / 词库 / 数据表常量**。

**优化方向**：把纯数据常量抽成 `json/` 下的独立文件，运行时 `fetch` 懒加载（加载时机放在用户点击「开始」之后，首屏零成本）。注意：这会让首屏不再携带题库，需同步处理加载态与失败兜底。

---

## 五、执行顺序与纪律

1. **P1-C → P1-B**（改 `_build.py`，全站生效，收益最大）
2. **P0-1**（改 `_build.py` 的 sitemap.html 生成逻辑）
3. **P2**（逐页抽离数据常量，P1 完成后复查哪些仍 >100KB 再动手）

**纪律**：
- `sitemap.html` 与 `tools/*/index.html` 均为**构建产物**，一律改 `_build.py`，禁止手改 HTML。
- 每步完成后必须跑 `python3 scripts/run_gates.py`，五道门禁全绿才允许提交。
- 体积变化会导致 `zh-tw/` 重建产物变动，属正常，按项目约定全量核对后随提交一并处理。
- 每完成一项，回填本文件对应条目的「状态」列为 ✅。

---

## 附：扫描口径说明

- 阈值按 **200 KB = 204800 字节** 计（非 200,000）。
- 分类页判定正则：`^\./tools/[^/]+/index\.html$`，命中 276 个（首轮扫描按排除项跳过，本次已专项优化，见第六节）。
- gzip 体积取 `gzip` 压缩等级 6，用于衡量真实传输成本（GitHub Pages 默认开启压缩）。
- `zh-tw/` 为构建产物且被 `.gitignore` 忽略，不纳入扫描。

---

## 六、分类落地页优化（2026-09-05 已发布 + 线上验收）

> 老板在 P1/P2 完成后要求：分类 index 页面也优化（首轮按「排除项」跳过）。

### 现状
- 276 个分类页合计 **5.7 MB**，最大 `tools/it/index.html` **256 KB**（it 行业 345 个工具，每个富卡片内联 ~580 字节）。
- CSS **已是公共引用**（P1 已生效，0% 内联 style），体积全部耗在「构建期内联全量工具卡片」。
- 现成数据源 `json/industry-<ind>.json` 已存在（271 个，含 file/icon/en/ed 字段），可直接消费。

### 方案（老板选：静态保 SEO + JSON 增强）
分类页是着陆页，项目 `AGENTS.md` 硬约束「发布产物必须搜索引擎无需执行 JS 即可抓取正文，不得客户端空壳」。故**不采用纯 JSON 渲染空壳**，改为：
- **静态轻量链接**：每个工具仅 `<a href class="cat-tool"><span class="t-zh">中文名</span><span class="t-zh-desc">中文描述</span></a>`（href+中文名作 SEO 锚文本、中文描述可见可被抓；繁体页由 OpenCC 自动转繁体）。
- **运行时增强**：`js/category-index.js` 读容器 `data-ind` → fetch `/json/industry-<ind>.json` → 按 file slug 匹配 → 重建为富卡片（图标+中文名[静态已转繁体]+英文名+中文描述[静态]+英文描述，均取 json）；fetch 失败兜底保留静态链接。

### 改动
- `_build.py` `generate_category_indexes()`：工具循环改精简链接 + 容器加 `data-ind` + head 引入 `category-index.js`（3 处）。
- `js/category-index.js`（新增）：fetch json 增强 + 失败兜底 + 繁体兼容。
- `css/common.css`：`.cat-tool` 补卡片基础外观（与 `.tb-megapanel-tool-card` 视觉一致，JS 未加载时静态也好看）。

### 效果
| 项 | 优化前 | 优化后 |
|----|--------|--------|
| 全部分类页合计 | 5.7 MB | **3.5 MB（-39%）** |
| `tools/it/index.html` | 256 KB | **93 KB（-64%）** |
| 质量分级 | A 5009 | A 5009（100%） |

- 五道门禁全过；无头 Chrome 实机验证：简/繁 it 分类页 345 卡片全增强、json fetch 200、本地资源零错误。
- 提交 `b3134acb0` 推送 master；线上验收：部署生效（线上 it 93KB、category-index.js 引用、data-ind、精简链接 345、旧富卡片残留 0）、`json/industry-it.json` 200。
