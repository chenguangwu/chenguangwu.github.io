# DEV-PLAN

## GSC 优化（无数据方向）— 老板 8-29 22:38 批准启动
> 背景：技术 SEO 8-26 审计已 100% 覆盖零缺口；无数据可做的站内项已做完。
> 唯一真活 = 内容深度（打掉模板化页过滤 = 收录极低根因）+ 英文重复描述去重。

### ✅ 已完成（试点，commit 1e051b92）
- [GSC-A1] it/ 15 高频工具内容深度块（使用场景/示例/FAQ），`_build.py` step6 + `i18n/tools/content_deepdive.json`，幂等注入，四门禁全绿。
- [GSC-A2] 12 个同行业工具英文标题+描述去重（`_en_override.json` 写具体功能）。

### ⏳ 进行中（老板 8-29 已批"铺开"，同机制按行业分批）
- [GSC-A3] 内容深度铺开，已落地 10 行业共 242 页 deep-dive：
  - 试点 it/ 15（1e051b92）→ math/ 25 → design/ 22 → finance/ 22 → statistics/ 23 → science/ 23 → materials/ 28 → electromagnetism/ 28 → fluid/ 28 → metrology/ 28（共 242 页）
  - 机制：`_build.py` step6 + `i18n/tools/content_deepdive.json`，幂等注入，四门禁每批全绿
  - 剩余候选：fluid/metrology/signal/investment/economics/process 等理工类，及 engineering/automotive/hydraulic/ai 等高质量行业
- [GSC-B] CTR 精修：等 GSC 查询 CSV（高展示低点击页定向改写 description）再动。

### 不做（已决策）
- 953 编号 URL / 104 basename 重复治理：SEO 风险>收益，8-24 已否决。
- 盲目全站 description 重写：8-24 否过的通用填充废话，禁止。

---

## 首页大改版：2 级分类导航（老板 8-30 14:00 指示，参考 tool.chinaz.com/tools/nav）

### 调研结论（真实数据，非推测）
- **行业总数 266**，但 `js/app.js` 的 `INDUSTRY_INFO` **仅 77 个**有中文名+图标 → **192 个行业缺中文名**，导航里只能显示英文 slug（`accounting`/`acoustics`…）。
- 补全数据源已确认可用：行业页 `tools/<key>/index.html` 的 `<title>`/`<h1>` 里有中文名（accounting→会计审计、acoustics→声学、aerospace→航空航天）。
- 现状首页分类导航是 `.breadcrumb-track` 平铺网格（刚由 8 列改 4 列），**无层级**。266 个行业平铺不可能好用 → 必须做 2 级，这也正是老板要的形态。

### 目标形态（布局学 chinaz，UI 用 ToolBox 橙 #FF6B35 / 紫 #7C3AED 风格）
- **顶部固定导航条**：Logo + 一级分类横向菜单 + 搜索框。
- **一级分类（约 10 个）**：IT开发 / 设计创意 / 金融财务 / 健康医疗 / 工程制造 / 科学研究 / 生活实用 / 教育培训 / 商业办公 / 休闲娱乐。
- **2 级下拉面板**：左侧=该大类的子行业列表（带工具数），右侧=选中子行业的热门工具网格（名称 + 一句话描述，学 chinaz 的卡片样式）。
- **首页主体**：导航 → 精简 Hero → **按大类分区块的分类导航主体**（区块标题=一级分类，内部=子行业 + 工具，学 chinaz nav 页面主体）→ 热门工具 → 为什么选我们 → Footer。
- **移动端**：顶部汉堡 → 抽屉式 2 级分类（一级手风琴展开二级），底部 Tab 栏保留。

### 分批计划
| 批次 | 内容 | 状态 |
|------|------|------|
| **B0** | 脚本从 266 个行业页提取中文名+图标，写回 `INDUSTRY_INFO`，覆盖 192 个缺失项（数据基础，无此则导航不可用） | ✅ `bafc36e9` |
| **B1** | 设计一级分类映射（266 子行业 → 10 大类），`_build.py` 产出 `json/industry-groups.json`（含子行业工具数 + 热门工具） | ✅ `bafc36e9` |
| **B2** | 新建 `js/nav-menu.js` + `css/nav-menu.css`：顶部导航 + 2 级下拉面板（左子行业/右工具）+ 移动端抽屉，首页与工具页共用 | ✅ `bafc36e9` |
| **B3** | `index.html` 首页大改版：导航移到最上部，主体改为按 10 大分类分区块，去掉平铺 breadcrumb 网格 | ✅ `5affcbe9` |
| **B4** | `_build.py` 幂等注入导航到 5014 工具页 + 266 分类页（共 5280 页），实现"其他页面同步" | ✅ `5affcbe9` |
| **B5** | 移动端：抽屉 + 手风琴、隐藏旧 `nav-mobile` 避免双层、搜索/主题并入新导航 | ✅ `bfa7020` |
| **B6** | 展示名统一中文 + 中英切换（见下方"踩坑·中英互换"） | ✅ `eb370e9` |
| **B7** | 移动端横向溢出修复：grid item 缺 `min-width:0` 撑破 1fr | ✅ `4e7d6d6` |
| **B8** | 全站统一两层顶栏停靠：滚动后分类导航被旧 fixed 顶栏遮挡 | ✅ `405988f` |

### 踩坑记录（本轮真实踩到，均为实测数据）
1. **中英互换（B6 根因）**：`_build.py` 对部分页面做英文 title 预渲染，导致 `tools.json` 里
   `name`/`desc` 的中英属性互换——4905 条 `name`=中文，109 条 `desc`=中文。前端固定取 `name`
   就拿到英文名（`.gitignore Generator`、`Advanced Unit Converter`）。
   → 规则：**谁含中日韩字符谁就是中文那一侧**；描述改从工具页 `<meta name="description">` 取。
2. **grid item 撑破 1fr（B7 根因）**：`.hc-grid` 用 `repeat(2,1fr)`，但 grid item 默认
   `min-width:auto`（最小尺寸取 min-content），长工具名把轨道撑破。390px 视口下
   `scrollWidth` 584 > 390，两列变 192.7px + 239.1px 不等宽。
   → 卡片本身要加 `min-width:0`（只给内层 `.hc-tool-body` 加没用）。
3. **内联样式不同步（B8 根因）**：B5 把 `.nav-top` 的 `top:56px/height:60px` 写在
   `index.html` 内联里，只影响首页；5280 个工具页/分类页仍是 `top:0/height:68`，
   滚动后旧顶栏（z-index 1000）把新导航（z-index 90）完全盖住。
   → 定位/停靠规则必须进全站 CSS，内联样式只留首页视觉微调。
4. **验证被缓存误导**：Pages 静态资源 `max-age=600`，旧 `sw.js` 自身也被缓存 →
   浏览器执行旧 JS，改了线上文件却测不出效果。验证前先注销 SW，或等缓存过期再复测。

### 硬约束
- 纯前端，不引新依赖；新增文件一律 `js/` `css/` `json/` `scripts/`，根目录不新增。
- 每批走 `改 → build → 三道门禁 → 真实验证 → commit`。
- i18n：新导航文案走 `data-i18n` + 中文兜底，英文模式可切。
