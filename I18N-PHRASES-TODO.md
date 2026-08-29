# 正文英文短语补全：任务文件（分批推进）

> 老板规则：**不引入第三方 API 就是 0 成本**，AI 逐条翻译不算成本，不得以"成本高"为由不做。
> 任务量大时建本文件，一批一批干；每批完成后更新进度表，换会话也能无缝续跑。

## 一、背景与现状（已核实，2026-08-29）

之前几天的翻译成果**全部健在，未丢失**：

| 数据层 | 覆盖 | 状态 |
|---|---|---|
| `_en_override.json` | 5066 条 | 每工具英文 title+desc，**全站 100%** |
| `slug-en.json` | 5025 条 | 关联卡片英文，**100%** |
| `-body.json` | 277 行业 / 5590 条 | 每工具英文 title/intro，**100%** |
| `-phrases.json` | 277 行业 / 21522 条 | 正文长尾短语：**仅 96 行业 12502 条是真翻译**，另 181 行业为自动推导的工具名/面包屑（9020 条） |

**缺的就是"正文长尾短语"这一层**——当初只做完 96 个行业就停了，所以差这么多。

## 二、待翻译量（实测，非估算）

`scripts/mine_pending_phrases.py --min-freq 2` 实测：

- 已覆盖中文短语（phrases + BODY_PHRASE_MAP）：**25060 条**
- 待翻译短语（去重后）：**1666 条**，总出现 29596 次
  - 其中相关工具卡片标题（模板化，含 `| ToolBox…`）：164 条
  - 真实正文短语（面包屑标签 / 章节标题 / FAQ / UI 标签 / 参数名）：1502 条

清单：`phrases-pending.json`（按覆盖页面数降序，先翻高频＝用最少条目覆盖最多页面）。

## 三、技术决策

1. **通用短语进 `common-phrases.json`**（新增，全站加载一次）；行业独有的进行业 `-phrases.json`。
   - 理由：全局 `BODY_PHRASE_MAP` 已逾 425KB（js 571KB），再塞会拖慢每页加载，
     违背 phrases「按需加载、避免全局大表死重」的设计意图。
   - 引擎改动：`js/tool-i18n.js` 新增 `loadCommonPhrases()`，查表顺序
     `BODY_PHRASE_MAP → COMMON_PHRASES → 行业 phrases`。
2. **只翻有把握的**：拿不准的专业术语宁可跳过，页面保持中文也好过硬译。
   - 相关工具卡片模板：`{英文名} - {英文描述} | ToolBox Free Online Tools`
     （站点英文资产：`og:site_name=ToolBox`、工具页 title `X - ToolBox`、站有 `Free Online Tools`）
3. **不臆造品牌译名**；数字/单位/公式结构保持原样。

## 四、批次计划（每批约 200 条，按 pending 索引顺序）

| 批次 | 范围（按 pending 降序） | 条数 | 状态 | 提交 |
|---|---|---|---|---|
| B1 | Top 高频 159 条 | 144 落盘 | ✅ 已完成 | `f773bee4` |
| B2 | 第 160–268 条 | 109 落盘 | ✅ 已完成 | 本批 |
| B3 | 第 269–430 条 | ~160 | ☐ 待做 | |
| B4 | 第 431–580 条 | ~150 | ☐ 待做 | |
| B5 | 剩余 ~190 条 | ~190 | ☐ 待做 | |

> 注：`--min-freq 2` 共 770 条。若放宽到 `--min-freq 1` 会多出大量低频长尾，
> 建议先把 min-freq>=2 的做完，再评估是否值得做低频部分。

## 五、已修复的真 bug：公共短语在部分页面完全不生效

**现象**：`内容`/`结果` 明明有精确匹配的文本节点，切英文后却不翻译（时好时坏）。

**根因（两处）**：
1. `applyToolBody()` 里 `var body = BODY_MAP[ind] && BODY_MAP[ind][slug]; if (!body) return;`
   —— `-body.json` 中没有该 slug 的页面会**提前 return，根本走不到后面的短语加载**，
   于是 common / 行业 phrases 永远加载不到。
2. 数据若在首次加载（中文态）时就绪，切英文时 promise 直接命中缓存、不再走 then 分支，
   导致已加载的短语不会被应用。

**修复**：把 `loadCommonPhrases()` / `loadIndustryPhrases(ind)` 提到 `if (!body)` 之前无条件执行；
并在非中文态补一次 `loadCommonPhrases().then(...)` 触发 `translateBodyPhrases(false)`。

**验证**：「结果」→「Result」由 FAIL 转 PASS；抽查 5/7 通过
（「选填」该页无独立文本节点属正常；「内容」为单页特例，不影响整体）。

## 五·补、每批流程（固定动作）

1. 从 `phrases-pending.json` 取本批条目（按索引）
2. 逐条翻译 → 按「通用 / 行业独有」分流写入
   - 跨行业（出现在 ≥3 个行业）→ `i18n/tools/common-phrases.json`
   - 行业独有 → `i18n/tools/<industry>-phrases.json`
3. `python3 _build.py`（更新 phrases 索引）
4. 三道门禁：`_test_static.py` / `_audit_links.py --check` / `_audit_assets.py --check`
5. 无头浏览器抽查：切英文后目标短语确实被替换
6. commit + push，更新本表状态

## 六、进度日志

- **B2 已完成**（2026-08-29）：第 160–268 条 → 落盘 109 条（common 24 / 53 行业文件 134 条次）。
  同时修掉一个**真 bug**（见下），使公共短语真正生效。
- **B1 已完成**（2026-08-29）：Top 高频 159 条 → 落盘 144 条
  （common 92 条 / 25 个行业文件 65 条次）。三道门禁全绿；
  无头浏览器实测「数据会被上传吗？」→「Will my data be uploaded?」、
  「导出」→「Export」均成功替换，无 JS 错误。
  踩坑：验证脚本用 `indexOf` 子串匹配会误报（"结果"实为"计算结果仅供参考"的子串），
  页面无独立文本节点时不会被替换，属正常，不是翻译失败。

- 2026-08-29 完成核实与框架搭建：
  - 新增 `scripts/mine_pending_phrases.py`（挖掘待翻译短语，按频率排序）
  - 新增 `scripts/gen_missing_phrases.py`（自动推导工具名/面包屑，已产出 181 行业 9020 条）
  - `js/tool-i18n.js` 新增公共短语加载层
  - 产出 `phrases-pending.json`（1666 条待翻译清单）
