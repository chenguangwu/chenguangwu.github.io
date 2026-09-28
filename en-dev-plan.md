# en-dev-plan.md — 英文态「内容区全量英文化」专项计划

> **状态**：**进行中** —— M0 工具链、M1 试点（`wedding`）已完成；M2 规模化推进中（**1 / 208 行业**）（2026-09-28）
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
| **门禁** | 四道既有门禁全过 | `scripts/run_gates.py` |

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

## 七、批次工作流（每工具 8 步）

```
1. 取 industries.md 首个行业            → 标记 in_progress
2. probe --scan <industry>              → 生成 pending/<industry>.json
3. 取清单首个工具
4. probe --extract <ind>/<slug>         → work/ 得到待译明细（含上下文）
5. 逐条语义化翻译（读工具名/行业/公式/示例做语境判断，非逐字）
6. 写入 `i18n/tools/en/<industry>/<slug>.json`（一工具一文件；读-改-写，串行；禁并行编辑同文件）
7. probe --check <ind>/<slug>           → 残留必须 = 0；probe --done <ind>/<slug>（从 pending 移除）
8. 清单空 → probe --promote <ind> → 跑 run_gates.py → 本地 commit → 下一行业
```

**中途不换线**：单工具未达零残留不得进入下一工具；单行业未全绿不得进入下一行业（沿用项目「分类上下文压缩」纪律，每行业收尾即固化 memory + skill）。

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
- **前置条件**：push 前必须 `python3 scripts/run_gates.py` 四道全过；改动仅 `i18n/tools/en/**` + `_en-i18n/**`（后者不发布）⇒ 属「会让线上变字节」，push 后确认一次 Actions 部署成功即闭环，**不做线上 MD5 比对**。
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

---

**进度台账**：`_en-i18n/industries.md` 为唯一权威（当前剩余 **207** 个行业）。每行业闭环 = `--scan` → `--extract` → 翻译写字典 → `--check` 归零 → `--done` 逐工具记账 → `--promote` 删行 → `run_gates.py` → 本地 commit。
