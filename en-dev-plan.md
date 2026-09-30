# en-dev-plan.md — 英文态「内容区全量英文化」专项计划

> **状态**：**进行中** —— M0 工具链、M1 试点（`wedding`）已完成；M2 规模化推进中（**1 / 208 行业**；`it` 已译 **45 / 338** 工具）（2026-09-28）
> **⚠️ 动手前必读（四条硬规则）**：① 批次规模**动态调整**，不是固定 10 个（§7.1，`it` 走 25–30 个/批）；② 每批**三项缺一不可** = 残留 0 + 中文态还原 + **四态烟测 0 异常**（§二）；③ 改 EN 字典后**必须重跑 `_build.py`** 刷新 SW 版本戳（§十三）；④ **遇到现有工具的 bug 或功能不完整必须顺手修**，不得以「不是本次造成的」忽略（§14.1）。
> **边界**：本专项是独立长线，与 `DEV-PLAN.md`（全站质量主线）并行、互不覆盖。`DEV-PLAN.md` 仍是全站待办权威源；本文件只管 EN 内容翻译这一条线。
> **衔接**：本专项正是 `docs/i18n-spec.md` §4.3 末尾结论所指的下一步 —— 「共享短语表红利耗尽，覆盖率停在 ~52%，逼近 100% 须切到**逐工具逐页**粒度预翻其 n=1 独有短语」。

---

## 一、目标（Definition of Done）

**英文态（`?lang=en-US`）下，工具页「内容区」零可见中文，且译文为语义化高质量英文（非逐字机翻）。**

- **范围**：`tools/<industry>/<slug>.html` 共 **4779** 页，208 个行业。
- **内容区**定义（13 类，逐项纳入验收）：

| # | 区块 | 现状 |
|---|---|---|
| 1 | `h2` 工具标题（含 emoji 前缀） | 预渲染英文，但 44.5% 为「标题回填」垃圾 |
| 2 | 简介段落（首个 `p`） | 同上 |
| 3 | `formula-box`：「📐 工作原理与说明」+ `formula-eq` 长句 | **无翻译**，运行时短语表无法命中长句 |
| 4 | 表单 `label` / `option` / `placeholder` | 部分被 `GEN_UI_MAP`（175 键）覆盖 |
| 5 | 工具栏 / 结果区按钮 | 部分覆盖（仅固定几十种文案） |
| 6 | 结果区标签（`div`/`span`/`th`/`td`） | 基本无覆盖 |
| 7 | 小节 `h3` 标题 | 基本无覆盖 |
| 8 | **深度解析区块**（`h2`/`h3`/`li`/`dt`/`dd`，含 `term-link` 内链片段） | **完全无英译**（源 181 万字符） |
| 9 | `tool-notes` 使用说明（3 条固定文案） | 通用句，部分覆盖 |
| 10 | `tool-intro` 折叠区（工具简介/功能特点/使用指南/免责） | 模板句为主，部分覆盖 |
| 11 | 相关工具卡片（`.rt-name` / `.rt-desc`） | 走 `slug-en.json`，覆盖不全 |
| 12 | 指南跳转链接（「📖 查看「XX 使用指南」」） | 无覆盖 |
| 13 | 面包屑 / `nav` 框架层 | 已由 `applyChrome()` 覆盖 |

- **不做**（沿用 `docs/i18n-spec.md` §7 Non-goals）：不译公式本体与符号（`ax²+bx+c=0`、`Δ`、`√`、单位）；不引入 MT API；不启用第三语种。

---

## 二、验收口径（可机验）

| 层级 | 判据 | 工具 |
|---|---|---|
| **单工具** | 英文态下该页可见文本节点残留中文 = **0** | `_en_i18n_probe.mjs --check <industry>/<slug>` |
| **单行业** | 该行业全部工具残留 = 0，且行业清单为空 | `--check <industry>` |
| **全站** | 4779 页残留 = 0（逐行业 `--check` 累计，或收尾阶段遍历 208 行业） | `--check <industry>` |
| **质量** | 译文零 CJK、零中文标点、零模板句、术语一致（§八 7 条硬规则） | 字典静态校验 + 人工抽查 |
| **回归** | 中文态逐页原文完全还原（简/繁双态），无英文串入 | `--roundtrip <industry>[/<slug>]`（繁体加 `--tw`） |
| **功能（硬性）** | **译文不得影响工具使用**：四态（简体 / 英文 / 繁体 / 繁体英文）烟测 **0 异常**（无 JS 报错、无页面异常）；计算类工具须通过独立复算用例 | `--smoke [--en] [--tw] <ind>/<slug>`；`scripts/verify_<ind>_calc.js` |
| **门禁** | 四道既有门禁全过 | `scripts/run_gates.py` |

> **「三项缺一不可」**：残留 0（`--check`）+ 中文态还原（`--roundtrip`）+ 功能无异常（`--smoke` 四态）**必须同时成立**才可提交。仅残留归零、但英文态出现 JS 报错 = 未通过。
> **已提交批次需回补验证**：批次提交后若后续新增/改进探针能力（如 `--smoke`），必须回到已提交工具重跑全套验收，不得以「当时已提交」为由跳过。

> 「零残留」以**探针口径**为准（文本节点级，与运行时同一套匹配逻辑），不依赖人眼抽查；人工抽查作为质量补充（每批 ≥10%）。

---

## 三、现状诊断（2026-09-28 实测）

| 指标 | 数值 |
|---|---|
| 工具页 | 4779（208 个行业） |
| 含可见中文的页面 | **4779（100%）** |
| 可见中文文本节点 | 293,874 |
| 中文总字符 | ≈ 519 万 |
| **唯一文本（翻译基数）** | **151,612** |
| 其中只出现 1 次 | 137,670（90.8%） |
| 其中出现 ≥10 次 | 仅 1,713 |

**已确认的低质/缺口案例**：

1. `i18n/tools/wedding-body.json` 的 `intro` 直接回填标题：`"Guest Seating Chart"` —— 不是翻译。
2. `i18n/tools/wedding-phrases.json` 出现 `"质量（标准/检测/保障）体系": "Detector 33"` —— 垃圾映射。
3. `i18n/tools/wedding.json` 出现 `"intro": "Countdown Timeline is a free online tool."` —— 模板废话。
4. `i18n/tools/_en_override.json` 出现 `"AST AST View Device"` —— 规则引擎误译。
5. 全站 5511 条 `-body.json` 条目中 **2454 条（44.5%）**`intro == title`。
6. 深度解析区块（4747 条、181 万字符）**完全没有英文数据源**。

**根因**：现有三层机制（`GEN_UI_MAP` 175 键 / `BODY_PHRASE_MAP` 9270 键 / `<ind>-phrases.json`）全部是**「全局共享短语 + 整节点精确匹配」**。该模式对固定短文案有效，对 **6.5 万个 ≥15 字长句 + 13.8 万个 n=1 独有文本**在结构上不可能命中。这既是当前 100% 页面有残留的原因，也决定了新方案必须换粒度。

---

## 四、技术方案

### 4.1 数据层：per-tool 英文字典（新增第三层）

新增 `i18n/tools/en/<industry>/<slug>.json` —— **一个工具一个文件**（老板硬约束：禁止含多工具的大文件）：

```json
{
  "slug": "countdown-timeline",
  "industry": "wedding",
  "name": "婚礼倒计时",
  "map": {
    "📅 婚礼倒计时": "Wedding Countdown",
    "婚礼日期倒计时与流程时间节点规划": "Wedding date countdown and stage-by-stage planning",
    "倒计时天数 =（婚礼日期 − 当前日期）÷ 86400000 向上取整；筹备节点按倒推排期……":
      "Days remaining = ceil((wedding date − today) / 86,400,000 ms). Planning milestones are counted backward: 12 months to book the venue and set the date, …",
    "设定婚礼日期与开始时间，实时显示剩余天、时、分，随时掌握进度。":
      "Set the wedding date and start time to see days, hours and minutes remaining at a glance."
  }
}
```

**键的权威口径（必须与运行时逐字一致）**：

- 键 = **HTML 文本节点原文**，即 `Node.nodeValue` 经实体解码后 `.trim()`（保留 emoji、全角标点、`/ ` 等前缀；不含首尾空白）。
- 采用**文本节点级**而非元素级，目的：`<li>设定婚礼日期…<a class="term-link" href="…">倒计时</a>页投屏…</li>` 这类含内链的段落**不丢 DOM 结构与内链**（现有 `translateBodyPhrases` 用 `el.textContent = tr` 会整体覆盖、破坏内链，属既有缺陷）。
- 公式/符号本身不译，仅译说明文字（`i18n-spec` §7）。

**配套索引**：`i18n/tools/en/<industry>/_index.json`（`{"industry":"...","tools":["<slug>",...]}`，由 `--reindex` 生成）—— 运行时先取行业索引、只对已有字典的工具发请求，避免 404（与 `phrases-index.json` 同做法）。

**全局通用层**：`i18n/tools/en/_common.json`（38 条，全站模板句如「工具简介」「功能特点」「❓ 常见问题（FAQ）」）—— 一次性补齐，对 208 个行业共同生效，避免在每个 per-tool 字典里重复收录。查找次序：`per-tool map` → `_common.json`。

**繁体链路约定（老板 2026-09-28 明确）**：

`zh-tw/` 是**构建期由 OpenCC 生成的静态产物**（`scripts/gen_opencc_locales.mjs`），繁体文本在 HTML 里已固化，**不走运行时 i18n 转换**。据此：

1. EN 字典**只存简体键**，不设繁体键集（`tw` 段）——不引入冗余与歧义。
2. 繁体页（物理路径 `/zh-tw/`）沿用同一替换逻辑：与简体同形的文本命中则受益，异形文本保持繁体原文（**英文态覆盖率不对繁体页作要求**）。
3. **硬要求**：中文态（`zh-CN` 与 `zh-TW`）一律**只还原、不替换**，由 `EN_ORIG` 精确回写原值 ⇒ 繁体页显示效果分毫不动，简 ↔ 繁 ↔ 英 任意切换无损。
4. 验收增加一项：繁体构建产物在中文态下与改造前**逐条文本一致**（`--roundtrip <industry> --tw`，实测 wedding 9 页 / 0 不一致）。

### 4.2 运行时层：`js/tool-i18n.js` 增量改造

新增约 100 行，不改动既有分支：

```
loadEnCommon()          → fetch /i18n/tools/en/_common.json（全局通用层，幂等）
loadEnIndex(ind)        → fetch /i18n/tools/en/<ind>/_index.json（资源加载守卫，防 404）
loadEnDict(ind, slug)   → 命中索引才 fetch /i18n/tools/en/<ind>/<slug>.json
restoreEn()             → 按 EN_ORIG 精确回写改造前原值（幂等还原）
pickEn(key)             → per-tool map → _common.json（后者为全站模板句兜底）
applyEnDict(isZh)       → ① [data-zh] 元素：以 data-zh 中文原文为键查表
                          ② TreeWalker(SHOW_TEXT)：文本节点级替换
                             命中 → nodeValue 就地替换（保留首尾空白），原值入 EN_ORIG
                          中文态 → 先 restoreEn() 再返回（只还原、不替换）
```

**执行次序**（关键，决定最终生效值）：

```
applyChrome()               （框架层：面包屑/nav/按钮）
  └─ 末尾追加：
     translateRelatedTools(isZh)   （相关工具卡片，走 slug-en.json）
     if (isEnglish()) loadEnDict(getIndustry(), getSlug())   ★第三层数据加载
     applyEnDict(isZh)             ★最后执行 ⇒ 覆盖 -body.json / 共享短语表
```

- **优先级**：per-tool EN 字典 > `_common.json` > `-body.json` > 全局短语表。已收录 EN 字典的节点不再走低质路径。
- **幂等**：`EN_ORIG` 保证 `zh-CN/zh-TW ↔ en-US` 反复切换无累积损耗；不改动 DOM 结构，只改文本。
- **加载时机**：与既有 `applyChrome` 同点触发（首屏 + 切语），`_index.json` 守卫保证零 404。

#### 4.2.1 既有层缺陷修正（2026-09-28 定位，必修）

`translateBodyPhrases()` 的选择器包含 `div / li / span / a` 等**容器**元素，命中整段文本时执行 `el.textContent = tr`。对**含表单控件的容器**，这会连带删除 `<input>/<select>/<textarea>`，导致页面 JS 读 `getElementById(id).value` 时抛 `Cannot read properties of null`。

- **实测影响**：`it` 分类 7 页（`basic-auth-generator`、`binomial-distribution`、`bluetooth-version`、`c-string-escape`、`caa-record-generator`、`calc-2`、`calc-7`）英文态报错；简体/繁体态正常（不跑运行时 i18n）。
- **与本专项的关系**：**非 EN 字典引入**（移除字典后报错完全一致），但直接违反 §二「功能」判据，必须修。
- **修法原则**：替换前加守卫 —— **跳过任何包含交互控件的容器**（`el.querySelector('input,select,textarea,button')`），使其只处理纯文本叶子节点；容器级长句由第三层文本节点级替换承担。
- **验证**：修后四态烟测 0 异常，且 `--check` 残留不增加（若增加，须把新增残留补进 per-tool 字典）。

### 4.3 构建层：零改动（本方案的关键优势）

**不改 `_build.py`、不重写 4779 个页面、不新增 `data-i18n` 属性**。理由：

- 页面重写会带来 ~50MB 体积增长与全站重建风险，且中文态将依赖 JS 还原（首屏闪烁）。
- 现有预渲染机制（h2/首 p）已证明「运行时按需加载」足够，扩展为全量字典即可。
- 免除 SEO 风险：`<link rel="canonical">` / hreflang 链完全不动。
- 唯一构建期动作：探针脚本生成 `_index.json`（纯新增文件，不触碰任何页面）。

### 4.4 与既有机制的边界

| 机制 | 处置 |
|---|---|
| `GEN_UI_MAP` / `BODY_PHRASE_MAP` | **保留**，作为未收录项的兜底；不再扩充 |
| `<ind>-phrases.json`（220 个） | **保留**，兜底 |
| `<ind>-body.json`（279 个） | **保留**，但被 EN 字典覆盖的条目实际失效；后续可择机清理 |
| `slug-en.json` | 保留，相关工具卡片 |
| `data-i18n` + `<ind>.json`（228 个） | 保留（6 个手工页），内容区不新增 |
| `i18n/tools/en/_common.json` | **新增**，全站模板句（38 条），优先级次高 |
| `i18n/tools/en/<ind>/<slug>.json` | **新增，最高优先级**（一工具一文件） |
| `i18n/tools/en/<ind>/_index.json` | **新增**，资源加载守卫（`--reindex` 生成） |

---

## 五、状态文件与目录

全部放 `_en-i18n/`（`_` 前缀 ⇒ **GitHub Pages 不发布**，但可入库跟踪进度）：

```
_en-i18n/
├── industries.md            # 待处理行业清单（初始 208 行，完成即删行，已建）
├── pending/
│   └── <industry>.json      # 该行业「有问题工具」清单（开始处理时由探针生成）
└── work/
    └── <industry>/<slug>.json  # 单工具待译明细工作台（探针 --extract 产出，译完即删）
```

**`pending/<industry>.json` 结构**（工具粒度，进度视图）：

```json
{
  "industry": "wedding",
  "scanned_at": "2026-09-28",
  "baseline": { "tools": 8, "residual_nodes": 201 },
  "tools": [
    { "slug": "countdown-timeline", "residual": 28, "samples": ["…", "…", "…"] }
  ]
}
```

**增删规则**（脚本独占写入，禁止手工编辑）：`--scan` 生成；每译完一个工具执行 `--done <ind>/<slug>` 删除该 `tools[]` 条目并重算 `baseline.residual_nodes`；条目清空后由 `--promote <ind>` 删除该文件并从 `industries.md` 删行；全部清空 ⇒ 专项收尾。

---

## 六、统一探针脚本设计（`scripts/_en_i18n_probe.mjs`）

一个脚本（`node scripts/_en_i18n_probe.mjs`）、多种模式，既是「探测」也是「验收」，**同一套匹配逻辑**保证口径一致：

| 模式 | 作用 |
|---|---|
| `--scan <industry>` | 生成/刷新 `pending/<industry>.json`：逐工具算残留数，只收录残留 >0 的工具 |
| `--extract <industry>/<slug>` | 产出单工具待译明细（含位置与上下文）到 `work/` |
| `--done <industry>/<slug>` | 单工具验收通过后从 pending 清单移除该条目（逐工具记账） |
| `--check <industry>[/<slug>]` | 验收：复用同一逻辑断言残留 = 0，非 0 则 exit 1 并列出节点 |
| `--roundtrip <industry>[/<slug>]` | 往返回归：zh-CN→en-US→zh-CN 文本逐条一致（繁体产物加 `--tw`） |
| `--reindex <industry>` | 重建 `i18n/tools/en/<ind>/_index.json`（资源加载守卫用） |
| `--mine <ind...>` | 跨行业挖掘复现 ≥3 的通用句，供 `en/_common.json` 使用 |
| `--promote <industry>` | 行业全绿后从 `industries.md` 删行、删 pending 文件、重编序号 |

**退出码**：`--check` / `--roundtrip` 通过为 0、有残留或不一致为 1（可直接作门禁）。

**匹配管线（复刻运行时，逐字对齐）**：`data-i18n` 作用域 ⇒ `applyChrome` 框架层 ⇒ `-body.json`（h2/首 p）⇒ `GEN_UI_MAP` ⇒ `BODY_PHRASE_MAP` ⇒ `common-phrases.json` ⇒ `<ind>-phrases.json` ⇒ `slug-en.json`（相关工具）⇒ **`en/<ind>/<slug>.json` + `en/_common.json`（最后执行，优先级最高）**。

> **误报治理（已完成，2026-09-28）**：框架层节点（面包屑「首页」、`nav` 内 `/ 工具名`）由 `applyChrome` 处理，探针已内置同等白名单（`isExcluded()` 排除 `.lang-switcher`）；`related-tools` 按 `slug-en.json` 实际覆盖判定。wedding 实测误报归零，`--check` 结果已可作为验收依据。

---

## 七、批次工作流（**批次规模按分类动态调整**）

### 7.1 批次规模规则（老板 2026-09-28 明确）

> **不设「一批 10 个」的硬性标准，按分类实际情况动态调整。**

- **唯一成本项是「编译等待」**：`_build.py` / `run_gates.py` / commit 的耗时是**每批一次**、与批次内工具数无关。因此批次越大，摊到每个工具上的等待越少。
- **工具多的分类加大批次**：`it`（338 工具）定为 **每批 25–30 个工具**；工具数 <20 的分类可一次做完（整行业一批）。
- **拆分原则**：一个「批次」= 一个 commit 周期，可跨多个回合写完字典（写文件不触发构建），**但构建 + 门禁 + commit 只跑一次**。
- 批次规模上限只受单回合产出能力约束；写不完就下一回合接着写，不得为了「凑一批」而降低译文质量。

### 7.2 单批次闭环（11 步，缺一不可）

```
1.  probe --scan <industry>                → pending/<industry>.json（行业首次）
2.  选定本批工具集合（it 分类 25–30 个）
3.  probe --extract <ind>/<slug>           → work/ 待译明细（含 DOM 上下文）
4.  读页面 HTML 核对碎片节点（<b>/<code>/<a> 切分处的空白与冒号）
5.  逐条语义化翻译（带工具名/行业/公式/示例语境，非逐字）
6.  写 i18n/tools/en/<industry>/<slug>.json（一工具一文件；串行；禁并行编辑同文件）
7.  probe --reindex <industry>
8.  probe --check <ind>/<slug> ×N          → 残留必须全 0
9.  probe --roundtrip <ind>/<slug> ×N      → 中文态不一致必须为 0
10. probe --smoke [--en|--tw|--tw --en] ×N → 四态 0 异常（见 §二「功能」）
11. verify_<ind>_calc.js                   → 计算类工具用例全过
    ── 以下每批仅一次 ──
    probe --done <ind>/<slug> ×N（记账）
    python3 _build.py                      → 生成新 SW 版本戳（§十三）
    python3 scripts/run_gates.py           → 门禁全过
    本地 commit（每 5 个 commit push 一次，或由老板手动 push）
    ── push 之后（§九·线上生效验证）──
    单次确认 Actions 目标 commit success → 抽 3–6 个 URL 落盘核对本批关键内容已生效
```

**中途不换线**：单工具未达「残留 0 + 四态 0 异常」不得进入下一工具；单行业未全绿不得进入下一行业（沿用项目「分类上下文压缩」纪律，每行业收尾即固化 memory + skill）。

---

## 八、翻译质量规则（硬约束）

1. **零 CJK**：英文字值不得含任何汉字（专有名词如品牌/人名酌情保留原样并登记）。
2. **零中文标点**：不得出现 `，。、；：！？（）「」""''`（应转 `, . ; : ! ? ( ) " " ' '`）。
3. **禁模板句**：禁止 `… is a free online tool.` / `… - produce results instantly in your browser.` / `… - run and process online in your browser.` 等套话（现有 `_en_override.json` 已检出此类）。
4. **禁标题回填**：`intro` 译文不得等于 `title` 译文（现有 `-body.json` 44.5% 违规）。
5. **术语一致**：同一中文术语全站统一英文；跨行业复用同一译法（`_common.json` 为共享模板句的唯一权威）。
6. **语义完整**：允许重组句子、拆分长句、补足英文省略成分；追求母语者自然度，拒绝逐字硬译。翻译时**必须携带上下文**（工具名/行业/公式/示例），不接受孤立单条翻译。
7. **保真标记**：emoji、编号、括号补充、单位、公式符号、`/ ` 前缀原样保留；句式占位（如「如：张三」）译为对应英文示例。

**质量抽检**：每行业完成时人工复核 ≥10% 工具（重点看长句与 deep-dive），发现系统性问题则回炉该批并补充规则。

---

## 九、提交与发布策略

- **粒度**：每完成 **1 个行业**（或累计 ≥10 个工具，取先到者）= 1 个 commit。
- **本地累积**：commit 只到本地，**不逐批 push**；累计 **5 个 commit** 后一起 `git push origin master`，或由老板手动推送。
- **信息格式**：`feat(i18n): EN content — <industry> (<n> tools)`。
- **前置条件**：push 前必须 `python3 scripts/run_gates.py` 全部门禁通过；改动仅 `i18n/tools/en/**` + `_en-i18n/**`（后者不发布）⇒ 属「会让线上变字节」。
- **线上生效验证（老板 2026-09-29 明确，强制）**：push ≠ 收尾。**必须验证线上改动真的生效**，不能只看「Actions 部署成功」就下结论。口径四步：
  1. **先单次查询 Actions** 确认本 commit 已 `success` —— 部署未完成时线上仍是旧版本，此时抽查必然得出「未生效」的假结论（2026-09-29 实测踩到：已删除的 json 仍返回旧内容，实为部署进行中）。
  2. **抽样落盘核对**：抽 3–6 个代表性 URL（本批工具页 × 四态 + 受影响的索引/JSON），`curl -o` 落盘后核对 HTTP 码 + **本批改动的关键内容确已出现**。判「生效」以**关键内容命中**为准，不以「页面能打开」为准。
  3. **英文态必须用真机探针**（`scripts/_en_i18n_probe.mjs --check`）：`curl` 拿到的是静态 HTML，运行时 i18n 的替换结果不在其中，直接抓 HTML 判中文残留必然误判。
  4. **边界**：只做**抽样**。仍**不做**全量逐 URL MD5 比对、不 sleep 等 CDN 传播、不循环轮询 API（沿用 2026-09-21 收尾口径，本条是对它的补充而非废止）。
- **可回退**：产物为纯新增 JSON，回退即 `git revert`，无页面重建风险。

---

## 十、风险与对策

| 风险 | 对策 |
|---|---|
| 中文源被改动 ⇒ 字典键失效（静默退化为中文） | ① 翻译期间冻结对应页中文源；② `--check` 会暴露；③ 收尾前逐行业全量 `--check` |
| 工作量巨大（15.2 万唯一文本 / 519 万字符） | 按行业分批、长线推进；每批完整闭环，不设总量截止 |
| 单工具字典体积 | 一工具一文件天然分片（wedding 实测 3~7KB/工具）；运行时按 `_index.json` 守卫只加载当前页字典 |
| 探针误报 ⇒ 假绿 | 误报已归零（§六）；`--check` 与运行时共用同一匹配函数，避免双口径 |
| 与既有短语表冲突 | 分层互斥：清单只收录未覆盖项；运行时 EN 字典最后执行 |
| 破坏内链（`term-link`） | 文本节点级替换，不动 DOM 结构（已写入 §4.1） |
| 中文态回归（英文串入） | `--roundtrip`（简/繁双态）逐条还原断言 |

---

## 十一、推进顺序与里程碑

| 阶段 | 状态 | 内容 | 出口判据 |
|---|---|---|---|
| **M0 工具链** | ✅ 完成 | 探针脚本正式化（8 模式）+ `tool-i18n.js` 第三层改造 + `_index.json` 守卫 + `_common.json` 全局层 | 探针误报归零；框架层白名单生效 |
| **M1 试点** | ✅ 完成 | `wedding`（8 工具）：216 条专属译文，残留 201→0 | `--check` = 0；`--roundtrip` 简/繁均 0 不一致；217 门禁全过 |
| **M2 规模化** | 🔄 进行中 | 按 `industries.md` 顺序（工具数降序）逐行业推进，已完成 1 / 208 | 每行业收尾：promote + 门禁 + commit |
| **M3 收尾** | ⏳ 待开始 | 逐行业 `--check` 全绿；清理被 EN 字典替代的 `-body.json` 回填项 | 专项关闭，归档 memory + skill |

**建议顺序**：`wedding` 试点已打通链路；M2 按规模降序 —— `it(338) → general(182) → finance(112) → design(111) → science(98) → …`（影响面最大者优先）。

---

## 十二、已确认决策（老板 2026-09-28）

1. **方案选型**：**运行时 per-tool 字典 + 文本节点级替换 + 零构建改动**。硬约束：**一个工具一个文件**（`i18n/tools/en/<industry>/<slug>.json`），禁止出现含多工具的大文件。
2. **状态文件位置**：`_en-i18n/`（`_` 前缀不发布、可入库）。
3. **提交节奏**：每行业 1 个本地 commit；工具数多的行业每 10 个工具 1 个 commit；**每 5 个 commit push 一次**。
4. **推进顺序**：规模降序（`it` 338 → `general` 182 → `finance` 112 → …）。
5. **试点范围**：按推荐顺序一个一个来，先做第一个 = `wedding`（8 工具，最小完整行业打通链路）。
6. **旧层清理**：M3 阶段清理被 EN 字典替代的无用 `-body.json` 回填项。
7. **繁体链路**：`zh-tw/` 是构建期 OpenCC 静态产物、不走运行时 i18n；EN 字典只存简体键；中文态（含 zh-TW）一律只还原不替换（见 §4.1 繁体链路约定）。
8. **批次规模动态调整**（2026-09-28）：取消「一批 10 个」的硬性标准 —— 编译等待是每批一次、与工具数无关，**工具多的分类加大批次**（`it` 定为 25–30 个/批）。详见 §7.1。
9. **每批必须验证功能**（2026-09-28）：译文不得影响工具使用，英文态尤其不得出现 JS 报错或页面异常；**四态烟测**（简/英/繁/繁英）为强制门槛。详见 §二「功能」。
10. **已提交批次回补验证**（2026-09-28）：后续新增/改进探针能力后，必须回到已提交工具重跑全套验收，不得以「当时已提交」跳过。
11. **拼写统一走美式**（2026-09-28 全批复核）：`color / optimize / customize / summarize / center / behavior`，与站点既有基调一致（`color` 28 : `colour` 0）。本批已修正 `optimising→optimizing`、`stabilises→stabilizes`、`centres→centers`、`customisable/customised→customizable/customized`、`Summarise→Summarize`、`favour→favor`（均在未 push 范围内）。
12. **EN 字典必须进 SW 版本戳**（2026-09-28）：`_build.py::compute_sw_build()` 已纳入 `i18n/tools/en/**`。详见 §十三。
13. **顺手修既有缺陷（强制）**（2026-09-28）：开发过程中遇到**现有工具的 bug 或功能不完整，必须一并修复**，不得以「不是本次造成的」为由忽略或留档了事。判据与处置见 §十四。
14. **push 后必须验证线上改动生效（强制）**（2026-09-29）：**部署成功 ≠ 改动生效**。push 后须先单次确认 Actions 目标 commit `success`，再抽 3–6 个代表性 URL **落盘核对本批关键内容确已出现**（英文态用真机探针，静态 HTML 不体现运行时替换）；判「生效」看关键内容命中，不看「页面能打开」。仍不做全量 MD5、不 sleep、不轮询。详见 §九。

---

## 十三、缓存与版本戳（EN 字典专属）

- **`_build.py::compute_sw_build()`** 的 hash 范围 = `css/**` + `js/**` + `json/{tools,guides,channel}.json` + **`i18n/tools/en/**`**（2026-09-28 补齐，此前为盲区）。
- **判定**：改 EN 字典后**必须重跑 `python3 _build.py`**，令 `sw.js` 的 `BUILD` 变化 ⇒ `sw.js::busted()` 的 URL 变化 ⇒ CDN/SW 不再返回旧字典。不重跑则 `_swv` 不变、客户端可能长期停留在旧译文。
- **幂等**：内容不变时重复构建 `BUILD` 不变（已实测两次构建一致），可安全随每批执行。
- **`.json` 走 `sw.js` 的 `networkFirst`**，新字典发布即生效；版本戳只负责打破 CDN 层 URL 缓存。
- 本专项所有提交都「会让线上变字节」⇒ 适用 §九 的 **push 后部署确认 + 线上生效抽查** 口径。

---

## 十四、既有层缺陷（翻译暴露，非本专项引入）

| 缺陷 | 现象 | 根因 | 处置 |
|---|---|---|---|
| **容器级 `textContent` 替换销毁表单控件** | 英文态（`?lang=en-US`）下 7 个 `it` 页面抛 `Cannot read properties of null (reading 'value')`；简体/繁体态正常 | `js/tool-i18n.js::translateBodyPhrases()` 的选择器含 `div`/`li`/`span`/`a` 等**容器**，命中整段文本时执行 `el.textContent = tr`，把容器内的 `<input>/<select>` 一并删除 | **已修复（2026-09-28）**：加守卫「有子元素且 `querySelector('input,select,textarea')` 非空即跳过」。**关键判据**：与 EN 字典无关（移除字典后报错完全一致） |
| **MD5 填充位丢失（运算符优先级）** | `it/calc-10` 的 `md5('hello')` 返回错值，而同页 SHA-256 正确 | `lWordArray[w] = lWordArray[w] \|\| 0 \| (0x80 << pos)` —— `\|\|` 优先级低于 `\|`，实际解析为 `a \|\| (0\|b)`，丢失 `0x80` 填充位 | **已修复（2026-09-28）**：改为 `(a \|\| 0) \| (0x80 << pos)`；修后 `hello`/`abc`/空串三个向量与 RFC 1321 一致。全站 `grep '\|\| 0 \|'` 仅此 1 例 |
| **`while` 循环体不推进 ⇒ 死循环冻死标签页** | `it/docker-run-converter` 遇尾参（`docker run -it --rm alpine sh`）即无限循环 | `parse()` 中 `if(!image){image=t;i++;}` —— image 已赋值时不递增 `i` | **已修复（2026-09-28）**：拆为 `if(!image){image=t;}` + 无条件 `i++;`。全站 `while` 已扫（512 处）仅此 1 例；`it/barcode-upc` 等「同类可疑」经查为误报 |
| **verify harness 对 `el.value` 误剥 HTML 标签** | `it/base85-encode` 的 Ascii85 期望值 `<~BOu!rDZ~>` 永远匹配不上（页面本身正确） | `scripts/verify_it_calc.js::collectStrings()` 对 `value`/`innerHTML`/`textContent` 一律 `replace(/<[^>]+>/g,' ')`；`value` 恒为纯文本，剥标签会把尖括号结果整块吞掉 | **已修复（2026-09-28）**：只对 `innerHTML`/`textContent` 剥标签。**正向副作用**：暴露出 `it/html-minifier` 的「输入回显」逃生项，已重写为真实压缩产物 + 压缩率断言 |
| **运行时翻译层 + 门禁对元素属性失明（系统性）** | 英文态 `?lang=en-US` 下输入框 `placeholder`、按钮/下拉 `title`、无障碍 `aria-label`、`alt` 等属性值长期为**中文**；用户无痕实测 csv-to-json 等页「按钮/下拉框/输入框提示/切换分类处都还是中文」；旧版门禁 `--check` 却报 **0 残留**假通过 | ① `js/tool-i18n.js::applyEnDict()` 修复前只对文本节点（TreeWalker SHOW_TEXT）做 `pickEn`，`translateGenericUI`/`translateBodyPhrases` 也只处理 `textContent`，**属性从未进入翻译路径**；② 旧探针 `collectCJK` 仅统计文本节点汉字，属性汉字不在扫描/验收口径 | **已闭环（2026-09-29）**：① `applyEnDict` 末尾新增 part (c)：遍历 `[placeholder],[title],[aria-label],[alt]`，`isExcludedEl` 排除 `.lang-switcher`，属性值 `pickEn(aVal.trim())`，原文存 `EN_ORIG` 供中文态还原；② `_common.json` 全局兜底层补 **741 条属性串**（11 行业 917 含残留页），终 876 键、**0 译文含中文**，借 `pickEn`「per-tool→_common 兜底」顺序一次性全局覆盖；③ 探针改 `collectCJKFull`：**文本+属性双口径**，0 残留为通过（退出码 0）。真机验收 it/design/general/wedding/network **0 残留** |

> **判据**：英文态才触发（简体/繁体不跑运行时 i18n）；错误信息固定为 `null.value` ⇒ 优先怀疑容器被整节点替换。

### 14.1 处置原则（老板 2026-09-28 明确，强制）

**遇到现有工具的 bug 或功能不完整，一律顺手修复，不得因「不是本次改动造成的」而忽略。**

- **适用范围**：本专项推进中触达的任何工具页 / 公共脚本 / 构建脚本缺陷（JS 报错、控件被删、计算口径错、文案名不符实等）。
- **修复纪律**：仍走完整闭环 —— 定位根因 → 最小改动修复 → 四态烟测 + `--check` 回归 → 写进本文件（判据→处置，不带批次流水）→ 随手记 memory。
- **不得只做记录**：把缺陷写进「已知问题」而不修 = 违规；仅在「修复超出本专项必要范围且风险高」时才例外，且必须在当轮汇报给老板拍板。
- **已闭环案例**：`translateBodyPhrases()` 容器级替换销毁表单控件（§十四 表首行）—— 本批定位后当场修复，7 页英文态回归 0 异常；同批还修了 `it/calc-10` MD5 填充位丢失、`it/docker-run-converter` 死循环、verify harness 的 `value` 误剥标签（详见 §十四 表）。

### 14.2 验证口径与常见误判（2026-09-28 固化）

- **四态烟测的 `⚠️ 点击了 N 个按钮但无输出变化` ≠ 页面缺陷**：若页面在加载时就执行过同名初始化（如 `it/calc-7` 末尾直接调 `loadSample()`），再点同一按钮内容自然不变。**判据**：先看页面末尾有无直接调用同名函数；有则是探针盲区，不算 bug、不记缺陷。
- **桩内 checkbox 恒 `false`，而真机默认可能勾选**：HTML 写 `<input type="checkbox" checked>` 的页面在 harness 下开关全假 ⇒ 页面走「什么都不做」分支、输出恒等于输入。**处置**：用例用 `checkIds: [...]` 显式还原真机默认态，否则该页 `expect` 极易退化成「输入回显」。
- **逃生项新形态：`expect` 恰等于「输入经归一后的形态」**：`it/html-minifier` 原 `expect:["a b"]`，而注入值经剥标签 + 空白归一后正是 `a b` ⇒ 命中与被测点无关。**判据**：定 expect 前先把 `inputs` 各值按该口径跑一遍比对。
- **`collectStrings` 只对 `innerHTML`/`textContent` 剥标签**（2026-09-28 起）：`el.value` 保留原文 ⇒ 含尖括号的结果（`<~BOu!rDZ~>` 等）现在可直接作为 expect。该函数波及全站用例口径，改动后必须重跑 `selfcheck_false_pass` / `discriminate_check` 确认基线未变。
- **美式拼写批量替换的自污染坑**：`fulfilment→fulfillment` 之后再跑 `fulfil→fulfill` 会得到三写 `fulfilllment`。**处置**：替换对按「长词优先 + 短词加否定前瞻」设计；扫描词表同样要写 `fulfil(?!l)`，否则美式 `fulfillment` 会被 `fulfil\w*` 误报。改完必须复扫确认 0 残留。

### 14.3 属性失明缺陷（2026-09-29 闭环，系统性，强制防复发）

**缺陷定性**：运行时翻译层与门禁 `--check` **只对文本节点生效，完全不覆盖元素属性（placeholder/title/aria-label/alt）**，是全站英文态属性中文长期漏翻却门禁 0 残留的根因。非本专项引入，由用户无痕实测投诉暴露。

**根因（两处独立失明）**：
1. `js/tool-i18n.js::applyEnDict()` 修复前只对 `TreeWalker(SHOW_TEXT)` 文本节点 `pickEn`；`translateGenericUI` / `translateBodyPhrases` 同样只动 `textContent`。元素属性值从未进入翻译路径 ⇒ 即便字典有译文，属性也不会被替换。
2. 旧探针 `collectCJK` 仅统计文本节点汉字；属性汉字不在任何扫描/验收口径 ⇒ 漏翻被判定为「0 残留」假通过，长期无人发现。

**处置（已落地）**：
- 代码：`applyEnDict()` 末尾新增 part (c) —— `querySelectorAll('[placeholder],[title],[aria-label],[alt]')`，`isExcludedEl(ae)` 排除 `.lang-switcher`，对每个属性值 `pickEn(aVal.trim())` 替换，原文 `EN_ORIG.push({el,attr,orig})` 供中文态一键还原。
- 字典：`i18n/tools/en/_common.json` 全局兜底层批量补 **741 条属性串**（普查覆盖 it/design/finance/fun/general/life/network/science/security/text/wedding 共 11 行业、917 含残留页），终态 **876 键、0 条译文含中文**。借 `pickEn`「先 per-tool `EN_DICT`、后 `_common` 兜底」的顺序，无需逐工具建 per-tool 文件即一次性全局覆盖。
- 门禁：`_en_i18n_probe.mjs --check/--scan` 改用 `collectCJKFull`：**文本 + 属性双口径**，属性汉字纳入扫描与验收，0 残留为通过（退出码 0）。
- 真机验收：it(338)/design(111)/general(182)/wedding(8)/network(0) **0 残留**；finance(112)/fun(64)/life(72)/science(98)/security(10)/text(11) 残留**均为正文文本**（属独立批次整站翻译，非属性缺口）。

**防复发纪律（老板 2026-09-29 明确，强制）**：
- 抽取（`--extract`/`--scan`）、翻译写字典、门禁验收（`--check`）**必须把元素属性纳入覆盖与校验口径**，禁止再只扫文本节点。
- UI 文案若同时出现在属性（如 `placeholder`）与文本，两份都要译；字典键以「原文原样」为准（运行时 `trim` 去首尾空白）。
- 后续整站翻译批次（finance/fun/life/science/security/text）推进正文时，属性缺口已全局修好，只需聚焦正文文本节点；但每批 `--check` 仍须确认属性口径 0 残留。

### 14.4 全局层「死快照」与语言切换事件「错靶」缺陷（2026-09-29 闭环，系统性，强制防复发）

**缺陷定性**：属性缺陷（14.3）修复部署后，用户再次实测投诉「按钮/下拉/tab/placeholder 仍中文 + 切换语言页面不刷新需手动刷新」。排查发现**两个相互独立的系统性 bug**，均为既有层缺陷、非本专项引入。二者叠加造成「线上部分翻部分不翻、切换不生效」而本地探针全绿的长期假象。

**根因一（全局层死快照）**：`js/tool-i18n.js` 的 IIFE 在脚本加载时对 `window.__TI18N_EN` 做一次性快照：
`var GEN_UI_MAP = (window.__TI18N_EN && window.__TI18N_EN.GEN_UI_MAP) || {};`（BODY_PHRASE_MAP 同）。
线上真实加载顺序：本脚本由页面静态引入先执行 → `boot()` 发现英文态缺数据 → **动态**加载 `tool-i18n-en.js`（554KB）→ 数据到达时**闭包内两个 MAP 已固化为 `{}`，永不更新** ⇒ 全局层（GEN_UI_MAP/BODY_PHRASE_MAP）整体空转。而 per-tool 字典（`EN_DICT`/`EN_COMMON`）是运行时 fetch 后赋值的活变量照常生效 ⇒ 精确形成「per-tool 命中的翻（CSV 输入/输出）、全局层负责的残留（转换/清空/复制/数据预览/逗号/引号字符/JSON 输入）」的混合残局。

**根因二（事件监听错靶）**：`i18n.js::set()` 在 **window** 上 `dispatchEvent(new Event('toolbox:langchange'))`（Event 默认不冒泡、target=window），而 `tool-i18n.js` 却挂在 **document** 上监听 ⇒ 永远收不到 ⇒ `onLangChange`/`applyAll` 从不触发 ⇒ 切换语言后内容区纹丝不动，必须手动刷新（刷新后按 `?lang` 重新 boot 才生效）。

**探针假绿根因（方法论缺陷）**：`probePage()` 用 `w.__TI18N_EN = enData()` **先注入数据再 eval** 脚本 ⇒ IIFE 快照时数据已在 ⇒ 全局层正常赋值 ⇒ 与线上「先脚本后数据」顺序相反，**结构上测不出根因一**。教训：**jsdom 探针的加载顺序必须与生产一致，凡「初始化快照全局对象」的代码，探针必须模拟真实的动态加载时序**。

**处置（已落地，`js/tool-i18n.js` 共 5 处）**：
1. `GEN_UI_MAP`/`BODY_PHRASE_MAP` 改空初始化 + 新增 `syncEnMaps()`（实时读 `window.__TI18N_EN`）；
2. `init()` 与 `applyAll()` 入口首行调用 `syncEnMaps()`（覆盖 boot 动态加载完成、语言切换两条路径）；
3. `document.addEventListener('toolbox:langchange', ...)` → `window.addEventListener(...)`（与派发目标一致，common.js 同事件同为 window 监听）。

**真机验证（playwright + 本地 HTTP 服务，真实加载顺序，SW 清缓存后）**：
- 英文首开：`Convert ->` / `Data Preview` / `Clear` / `Copy` / `Quote Character` / placeholder `Input JSON data...` 全部生效；
- 切中文（**无刷新**）：`转换 →` / `数据预览` / `输入 JSON 数据...` 即时还原；再切英文即时切回。
- 附带实证：**SW cache-first 旧缓存会让 reload 也拿到旧脚本**（本会话实测 reload「回退」假象）——线上用户长期看到旧问题的帮凶之一；验收必须清 SW 或无痕。

**防复发纪律（强制）**：
- IIFE 内**禁止**对 `window.X` 做初始化快照用于后续翻译逻辑；凡全局数据一律「使用时实时读」或「数据到达后显式同步」。
- 自派发事件（`new Event(...)` 默认不冒泡）的派发方与监听方 target 必须一致（统一 **window**）；新增跨脚本事件时两边同查。
- 探针必须模拟生产加载顺序；「先注入后执行」的便捷 mock 只能用于测字典内容，不能用于测**加载时序类 bug**。
- 语言切换验收必须包含「**不刷新页面**连续切换 中→英→中」三步断言，不能只测首开。

### 14.5 效率工具栏同病复发（2026-09-29 闭环，强制防复发）

**缺陷定性**：14.4 根因二修复后，用户截图再投诉「效率工具栏整条中文（运行/复制结果/导出结果/恢复示例/清空输入/本地处理/160 字符 · 6 行）」。该栏由 `js/hot-tool-enhancements.js` 运行时注入，**自带三语 COPY 表**（zh-CN/zh-TW/en-US 全齐）——文案不缺，但第 310 行 `document.addEventListener('toolbox:langchange', ...)` **重犯 14.4 根因二的监听错靶**：i18n.js 在 window 派发且不冒泡 ⇒ 永远收不到 ⇒ 初始 `init()` 时 `currentLocale()` 读到的还是 zh-CN，之后语言切换事件又收不到，工具栏定格中文。

**教训**：14.4 修复时只全局扫了 `js/*.js` 中监听 document 的脚本（当时 hot-tool-enhancements.js 的监听写在 `init()` 函数体内、缩进层级深，`grep "document.addEventListener('toolbox:langchange'"` 能命中但被人工核查遗漏）⇒ **修复一处同型 bug 后，必须用机器方式（grep/AST）穷举全部同类点并逐一处置，禁止靠肉眼抽查**。本次已全站复核：`js/*.js` 共 8 处 `toolbox:langchange` 监听，修复后 8/8 全部挂 window。

**处置**：`hot-tool-enhancements.js` 监听改挂 window（附注释说明派发靶）。真机验证：英文首开 `⚡ Productivity bar / ▶ Run / ⧉ Copy result / 160 characters · 6 lines` 全生效；无刷新 中→英→中 双向即时切换。

### 14.6 动态注入节点失明（2026-09-29 闭环，系统性缺陷，强制防复发）

**缺陷定性**：14.5 修复后抽查 `it/cron.html` 英文态仍有 16 处中文（`✨ 试算示例`／`⬇️ 导出 TXT`／预设名 `每分钟执行·每5分钟·每天 08:00…`／nav aria-label `热门工具·我的收藏·广告 1·ToolBox 实时访问数据·回到顶部`）。排查确认**第三类独立缺陷**：`applyEnDict` 是**一次性全量扫描**（TreeWalker + querySelectorAll），**结构上看不见翻译执行之后才插入 DOM 的节点**。

**根因**：大量内容由运行时 JS 注入且晚于 i18n 全流程 —— `tool-page-runtime.js` 的「复制结果/导出 TXT/试算示例」按钮、工具页内联 JS 渲染的结果标签与预设列表、后续重绘组件。即使字典里已有正确译文，一次性扫描也永远够不到它们（cron 页实测 42 处残留，含大量「字典里其实有译文」的动态节点）。

**处置（已落地）**：
1. `js/tool-i18n.js` 新增 **part (d) 动态节点增量翻译**：英文态下 `MutationObserver`（childList+subtree+attributes，attributeFilter 四项）对新增子树递归翻译，**完全复用**现有 `pickEn`/`convertPunct`/`isExcludedEl`/`EN_ORIG` 口径；
   - 收敛性：已译节点再次进入时 `pickEn` 不命中 ⇒ 不自激循环；`dynApplying` 抑制位 + `setTimeout(0)` 解锁挡掉自身写入触发的二次回调；
   - 正确性：译文同样入 `EN_ORIG` ⇒ 中文态与静态部分同口径逐项精确还原；`applyEnDict(isZh)` 入口处 `stopDynObserver()`。
2. 字典补位：全站组件串 11 条入 `_common.json`（887 键）；cron 专属 28 条入 `i18n/tools/en/it/cron.json`（81 键）；两文件 CJK 扫描 0 脏译文。

**真机验证**：cron 英文态残留由 42 → **3**（仅剩语言切换器内的 `Language / 语言` 与 `繁體中文`，属 §设计内排除：`isExcludedEl` 按惯例语言名用本语言显示）；注入字典已有词（如「预览」）即时变 `Preview`，证明增量通道生效；切中文完整还原；console 0 错 0 警；`csv-to-json` 抽测同为 3（同口径）。

**抽样现状（用于排后续批次，非本批次范围）**：`science/ph-calculator` 2 处、`design/color-picker` 11 处、`general/calc-205` 8 处、`text/analysis-density` 20 处 —— **全部为字典缺口**（要么词条未收录，要么为无限变体如 `title="使用 #41E1D1"`），机制缺口已清零。

**防复发纪律（追加，强制）**：
- 站点任何 i18n 覆盖必须同时满足「静态全量 + **动态增量**」两条腿；只有一次性扫描的方案一律视为不完整。
- 新写运行时注入组件时，文案要么自带语种表并监听 `window` 的 `toolbox:langchange`（14.5），要么依赖本 (d) 增量通道并确保**译文已入字典**——二者缺一即中文残留。
- 验收口径升级：真机扫描必须包含**全部可见文本 + 4 类属性**，且仅允许「语言切换器」残留；静态 jsdom 探针（§14.4）天生测不到动态注入，**不得作为此项通过依据**。

### 14.7 前缀子串替换机制（根治「标签+变量」动态结果串，2026-09-30 新增）

**缺陷定性**：14.6 增量通道把「字典里有译文但晚注入够不到」清零后，真机审计（report5，821 页全量）暴露第三类残留结构 —— **「标签+变量」动态结果串**：`原始大小：1.5 MB`、`还款总额：¥12,345`、`应用场景：短信验证`。part(a) 文本节点级替换只做 `pickEn(k)` **整串精确匹配**，变量值每次不同 ⇒ 整串永远命中不了字典 ⇒ 这部分中文长期漏翻。

**根因**：结果区由内联 JS 渲染 `标签 + 计算值`（如 `el.textContent = label + '：' + value`），文本节点整串 = 「标签：变量」，而字典键是纯「标签：」或纯「标签」—— 没有「标签：变量」这种无限变体，精确匹配结构性失效。

**处置（已落地，`js/tool-i18n.js` + 新增 `i18n/tools/en/_prefix.json`）**：
1. 新增**前缀字典** `_prefix.json`：**与精确字典物理隔离**（绝不用通用词做前缀误伤正文），只收「结果区标签片段」（如 `原始大小：`、`还款总额：`、`应用场景：`）。
2. 新增 `longestPrefixKey(text)`：文本节点以某已知前缀开头时**只译前缀、变量值原样保留**（长→短匹配，避免 `总` 误译 `总经理`）。
3. 改造点：(b) 文本节点 walker 与 (d) MutationObserver `dynTranslateNode` 查找逻辑均加前缀兜底（`pickEn` 未命中 → `longestPrefixKey` 命中前缀 → 仅替换该前缀片段）；`loadEnDict` 内 `loadEnPrefix()` 与 `loadEnCommon()` **并列加载**。
4. 字典规模：**209 条** `：` 标签前缀键（手工精译，`build_prefix.py` 生成）+ **73 条**补译（`gen_labels.py` 一阶段，修 rater-1/capm 等漏写/截断项）+ **149 条**非冒号短标签（`gen_labels.py` 二阶段，多字词汇+单位规则批译）+ **859 条**结果区字段标签/标题（`gen_labels_batch2.py` Tier-4 手写精译）⇒ 终态 **1290 键、0 译文含中文、0 单字键**。
5. 防误伤纪律（强制）：① 前缀键**只收 ≥2 字**（单字 `总→Total` 会误译 `总经理→Total经理`，已否决）；② 单字词汇替换批产已试错产生「QR code定制scheme」中英混杂垃圾，**绝不入库**；③ 非冒号短标签只收译文零中文项，去 CamelCase 空格缺失（`Rotation speedCoefficient` → `Rotation speed Coefficient`）。

**收敛效果（真机审计 report5 → report7，前缀 431 键阶段）**：
- 全量残留 1988 串 / 393 页（report5）→ **1789 串 / 381 页**（report7）。
- **含全角冒号的「标签+变量」串 216 → 21**（前缀机制直接命中）。
- 剩余 1768 串（99%）为**工具 OUTPUT 内容**（代码注释/样本/单字打字样本/方案名/数值+单位句子），非 UI 控件。

**范围决策（genuine scope fork）**：
- 前缀机制已覆盖 305 条冒号类动态结果标签，价值部分（标签）已翻，变量/方案名/代码注释/单字样本等 **OUTPUT 内容是否也要全翻**是独立判断 —— 纯代码注释（`/* 粒子特效配置 */`）与打字单字样本属「内容」而非「UI」，翻了未必是用户要的，且逐字拆分页（typing-test）逐字映射无意义（需源码层英文态换样段）。
- 数字→中文转换器的真实输出（`壹仟贰佰叁拾肆元伍角陆分`）、法律免责声明、内嵌指令/样本属**已知例外**，保留中文、不入库。
- 编号→中文转换器（大写金额）、CSS 代码样本（含中文注释）等「输出即内容」的页面，其 OUTPUT 不在 UI 英文化范围内。

**续批扩展（batch3–batch5，把「标签+单位/数值」前导形态也兜住）**：
- `gen_labels_batch3.py`（report8 阶段）：125 条金融/工程/光学量纲名（`净现值`/`夏普比率`/`风荷载标准值`/`所需换热面积`），只收 ≥3 字术语 + 2 字键配长键兜住，替换模拟零 garble。
- `gen_labels_batch4.py`（report9 阶段）：111 条净量纲/字段标签（`运动黏度`/`焦点光斑直径`/`功率密度`/`置信区间`/`静电力`/`维氏硬度`/`疲劳极限`），**只收 ≥3 字键**（零词素前缀风险）。
- `gen_labels_batch5.py`（report10 阶段，末批）：26 条安全 2 字标签（`尺寸`/`波长`/`质量`/`速度`/`动能`/`功率`/`误差`/`压强`/`斜率`/`卡诺`），**替换模拟扫「拉丁紧接中文」签名**剔除 `匹配`(`匹配结果`)/`文件`(`文件大小`) 两个词素前缀键（会产 `Match结果`/`File大小` 垃圾）；`红外`/`佩戴`/`完整` 因 Latin-direct-after 风险不收；产品名/打字样本/整句 OUTPUT 排除。
- `_prefix.json` **终态 1552 键、0 译文含中文、0 单字键**。

**最终收敛（report5 → report11，真机审计 821 页全量）**：
| 阶段 | 键数 | 残留串 | 脏页 | 冒号类 | 备注 |
|---|---|---|---|---|---|
| report5 | 0（基线） | 1988 | 393 | 305 | 前缀机制前 |
| report7 | 431 | 1789 | 381 | 21 | 前缀机制首落地 |
| report8 | 1290 | 776 | 291 | 21 | batch2（859 字段标签） |
| report9 | 1415 | 696 | 284 | 21 | batch3（125 量纲名） |
| report10 | 1526 | 600 | 258 | 21 | batch4（111 量纲/字段） |
| report11 | 1552 | **594** | **256** | 21 | batch5（26 安全2字，末批） |

- 残留 **594 串 100% 为 genuine 工具 OUTPUT**：284 生成代码样本（含中文注释的 CSS/HTML，如 `/* 手机（< */`、`配合响应式断点…`、WCAG 描述）、203 计算描述（`✓ AA（正文≥4.5:1）`、`Contrast = … 按 WCAG 2.1 相对亮度`）、86 打字单字碎片（`折`/`倍`/`分词`/`试文`）、21 冒号动态（含 α/变量，刻意例外）。**安全可捕 UI 标签边界已 100% 耗尽**。
- 结论：再无任何「标签+变量/单位」可捕串；剩余 594 全为工具 OUTPUT 内容（代码注释/计算结论/打字样本/数字转中文），**翻译属 scope fork** ——（a）逐源码改造生成逻辑才净（高成本、低价值）；（b）接受现状（OUTPUT 中文在英文态语义上本就正确）。推荐（b）。

### 14.8 前缀机制三处口径缺口（2026-09-30 二次闭环，强制防复发）

「14.7 边界耗尽」结论经复核**为误判**：审计里仍有 14 条「双语混合结果串」与 10 条属性中文未消，定位出三处独立口径缺口（均属机制层、非字典层）：

**缺口一：属性口径零前缀匹配。** part(c)(d) 的属性翻译只做 `pickEn(aVal)` 精确匹配，未接前缀兜底 ⇒ `title="五险一金: ¥4,500.00"`、`title="文字"` 这类「标签+值」属性永远漏翻。
→ 处置：属性路径（placeholder/title/aria-label/alt）与文本节点**共用同一套前缀匹配**；`word-frequency` 的 `title="${word}"`（被分析的数据本身，如 `文分`）确认**不可翻**，保持原样。

**缺口二：同节点多标签只替一个。** 替换逻辑**每节点只替换第一个命中的键**。混合串以已知标签开头时（`资产负债率：… | 流动比率：1.8 | 收入：5000万`），`longestPrefixKey`（仅串首）先命中即返回，串中其余「标签：」全部漏替。
→ 处置：`replaceColonLabelsAll(text)` **全量替换优先于** `longestPrefixKey`；译文用半角 `:` 不含全角冒号 ⇒ 循环必然收敛（另加 guard）。此顺序是**铁律**：全量在前、串首兜底在后，颠倒即复发。

**缺口三：`toolbox:langchange` 派发口径错配。** `js/i18n.js` 的 `set()` 只在 `window` 派发，而工具页监听器挂在 `document`（window 事件不传播到 document）⇒ 切语言时工具**动态内容永不重渲染**；且 `init()` 起初不派发 ⇒ 解析期已渲染（当时 `I18n.get()` 仍未 init）的工具内容停在默认语言。
→ 处置：`set()` 与 `init()` 均 **window + document 双通道**派发。受影响的工具形态 = 自带 `isEn()`（`I18n.get()==='en-US'`）双语模板、且渲染早于 i18n 就绪者（全站 `palette-cvd-checker`/`cvd-safe-palette`/`farnsworth-d15-test` 等）。

**验证**：`_prefix.json` +20 键（1571）；11 个混合串/属性目标页真机探针残留**全清零**；**全量审计 report11→report13：594→576 串、256→254 脏页、目标标签残留 14→0**；门禁 217/217。init 补发派发令 `cvd-safe-palette` 重渲染而暴露其硬编码 `<th>颜色</th>`/`复制 JSON`（未走 `isEn()`）⇒ 补入该工具专属字典（574 串/253 页终值）。余量 100% 为 genuine OUTPUT 值（`Revenue: 5000万`、`Collection strategy:正常类：定期跟踪`、`Service stage:婚庆策划`、生成结论散文 `信用良好，可优惠授信。`、维护指令 `检查轴承磨损…`、打字单字、切词数据）。

**防复发判据（改机制必查）**：① 属性/文本/动态三口径是否都接了前缀匹配；② 全量替换是否排在串首兜底之前；③ 任何新增的「切语言重渲染」能力，其事件是否同时覆盖 window 与 document，且初始语言就绪后有补发。

### 14.9 半角冒号统计徽章 + 动态值量词收口（2026-09-30 三次闭环）

§14.8 后对 report13 余量做**页作用域精确替换模拟**（仅加载本页 per-tool 字典 + `_common` + `_prefix`，复刻运行时逻辑），得真·机制漏网 = **2 串**，均为**半角冒号 + 空格**形态的统计徽章：`匹配: N 项`（json-path）、`字段数: N`（json-schema-generator）。

**判据 → 处置**：
1. **前缀字典键必须覆盖「半角冒号 + 空格」形态**。既有 `_prefix.json` 冒号键一律全角 `：`，而部分工具徽章用半角 `: `（`textContent = \`匹配: ${n} 项\``），`longestPrefixKey` 因整串不匹配而漏。→ 补半角冒号键 `匹配: `/`字段数: `/`大小: `/`耗时: `（带空格，天然不命中 `匹配结果`/`大小写` 等词素前缀 ⇒ 零 garble）。半角键**只走串首匹配**、不进 `replaceColonLabelsAll`（后者按全角 `：` 结尾筛选，避免正文误伤）。
2. **动态值量词（`项`/`字符`）字典够不到 ⇒ 用双语句**。前缀机制只替命中子串、`slice` 保留尾部，故 `匹配: N 项`→`Matched: N 项`，量词 `项` 残留。量词无法用字典键（单字 `项` 会 garble `项目`）。→ 对带量词徽章改用**源码双语句** `(window.I18n && window.I18n.get && window.I18n.get()==='en-US') ? \`Matched: ${n} items\` : \`匹配: ${n} 项\``，量词随语言切换（项目既有 3 个 `isEn()` 先例）。静态默认态（`匹配: 0`/`字段数: 0`/`大小: 0`/`耗时: 0ms`）仍由半角键覆盖。
3. **「边界耗尽」结论必须用页作用域模拟复核，禁用跨工具字典匹配**。首次模拟因遍历**全部** per-tool 字典致 `举/钢/在/共/分词` 等**其他工具单字键**误命中，虚报 8 个漏网。真正口径 = 仅加载**本页**字典（对应运行时 `loadEnDict` + `_index.json` 守卫）。

**验证**：`_prefix.json` 1571→**1575** 键；页作用域模拟漏网 **0**；json-path/json-schema-generator `--check` 残留 0、中英 `--smoke` 0 异常（真机探针 EN：`Matched: 2 items`/`Fields: 6`/`Size: 617 chars`；ZH：`匹配: 2 项`/`字段数: 4`/`大小: 430 字符`）；门禁 217/217。**至此自定义标签类（含半角冒号、含动态量词）安全可捕边界彻底闭合**，剩余全为 genuine 工具 OUTPUT 值。

### 14.10 交互态盲区：默认态审计扫不到的「点击后渲染」标签（2026-09-30 四次闭环，**审计口径修正**）

**判据（推翻「边界耗尽」的第三次，也是根因性的一次）**：既有 `audit_all.mjs` 只扫**加载后默认可见 DOM**；而工具**点击计算/生成后才渲染**的结果区（表头、统计量名、错误提示、按钮、下拉选项）**从不进入审计视野**。故前几轮 report11/13/14 的「594/576 全为 OUTPUT」结论**天然漏掉了整类可捕标签**。

**处置（新增审计维度，强制纳入收尾口径）**：
1. **交互态探针 `_en-i18n/probe_interact.mjs`**：逐页点「主计算按钮」后重扫可见 CJK（`TreeWalker` + 计算/生成/分析/… **中英双语动词**匹配 + 排除导航按钮 class + 排除语言切换器）。**注意 EN 态下按钮文本已被字典译为英文** ⇒ COMPUTE 正则必须同时含英文动词（`Calculate/Generate/Compute/…`），否则 0 命中。
2. **两类标签分流入库**：带冒号标签（`解读：`/`输入：`/`定义：`…）→ `_prefix.json`（anywhere 替换）；**孤立标签（表头/按钮/选项，节点==标签）→ `_common.json` 精确匹配**（零 garble 风险，优于塞 `_prefix` 的串首匹配）。
3. **长键优先**：`计算步骤：` 必须显式入库，否则被更短的 `步骤：` 先命中，产出半译 `计算Steps:`（`replaceColonLabelsAll` 按长度降序，先命中长键）。同类：`计算过程：`/`推导步骤：`。
4. **公式型标签用带尾随空格的前缀键**：统计量后接公式/字母（`方差 np(1−p)`/`中位数 ln2/λ`/`临界值 z* = …`）⇒ 非冒号键只串首匹配，需 `方差 `/`中位数 `/`临界值 ` 等（带空格，`Variance ` 值同步带空格）。

**验证**：821 页交互探针实测 **376 页可点击、128 页暴露 501 条新 CJK**；`_common.json` +144 键（1691→1835）、`_prefix.json` +101 键（1575→1676）；128 页交互态新 CJK **501→195（-306，61%）**；余量全为 genuine OUTPUT（随机生成名/枚举评级值 `良好`·`较差`/步骤散文/动态编号 `1 级`·`5 年`/Latin 内嵌标签 `z* 临界值`）。门禁 217/217。

**防复发铁律**：**「边界耗尽」结论必须用「默认态 + 交互态」双口径复核**；仅默认态扫描**_不得_**宣称边界耗尽。新工具页若结果区需交互触发，必须过 `probe_interact.mjs`。

---

**进度台账**：`_en-i18n/industries.md` 为唯一权威（当前剩余 **207** 个行业）。每行业闭环 = `--scan` → `--extract` → 翻译写字典 → `--check` 归零 → `--done` 逐工具记账 → `--promote` 删行 → `run_gates.py` → 本地 commit。
