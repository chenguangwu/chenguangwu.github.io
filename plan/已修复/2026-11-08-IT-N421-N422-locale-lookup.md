# 第 23 批 · IT-N421 / N422 · locale-lookup BCP 47 校验与查表

- 日期：2026-11-08
- 页面：`tools/it/locale-lookup.html`
- 条目：IT-N421（中，确认缺陷）、IT-N422（中，确认缺陷）
- 顺带修复：「2026-11-06 IT 工具静态续审」的 **XSS 条目（真未修）** + **英文态动态结果区中文残留**
- 同批：`i18n/tools/en/it/locale-lookup.json`、`scripts/verify_it_calc.js`、本移交档、分类清单

## 一、IT-N421 BCP 47 正则过窄

**缺陷**：兜底正则 `^[a-z]{2,3}(-[A-Z][a-z]{3})?(-[A-Z]{2})?(-[A-Z0-9]{5,8})?$` 把 variant 限死 5–8 位、region 限两位字母、完全不支持扩展子标签。`de-DE-1996`（4 位数字 variant）、`es-419`（UN M.49 数字地区）、`en-US-u-ca-gregory`（扩展）全部误判「❌ 不符合 BCP 47 格式」。

**修复**：改为 RFC 5646 语法子集：

```js
const LC_RE = /^(?:[a-z]{2,3}(?:-[a-z]{3}){0,3}|[a-z]{4}|[a-z]{5,8})
  (?:-[a-z]{4})?                              // script
  (?:-(?:[a-z]{2}|\d{3}))?                   // region：两位字母或三位 UN M.49
  (?:-(?:[a-z0-9]{5,8}|\d[a-z0-9]{3}))*     // variant：含 4 位数字
  (?:-[0-9a-wy-z](?:-[a-z0-9]{2,8})+)*      // extension：singleton ≠ x
  (?:-x(?:-[a-z0-9]{1,8})+)?                 // privateuse
$/i;
```

校验前把 `_` 统一成 `-`（兼容 `en_us`），并在**查表之前**先做格式校验：非法标签不得进入回退链，避免 `de-DE-XXXXXXXXX` 之类靠前缀命中 `de-DE` 把乱码显示成「已识别 locale」。

**顺带修解析段**：原逻辑「第 2 段不是 4 字母就当国家」会把 `sl-rozaj-biske-1994` 的 variant `rozaj` 输出成「国家（ISO 3166-1）：ROZAJ」。现只在子标签符合 `^[a-z]{2}$|^\d{3}$` 时才写国家行；script 分支后的 `parts[2]` 同样加形态判断。

## 二、IT-N422 查表区分大小写、缺规范标签

**缺陷**：`LOCALES[raw] || LOCALES[raw.replace('_','-')]` 原样比对，`EN-US` / `en_us` / `zh-Hans-CN` 全部退化成「✅ BCP 47 格式有效（数据库中无此条目）」，而 deep-dive FAQ 正以 `zh-Hans-CN` 为规范示例。

**修复**：新增 `__lcNorm()` canonical 化（language 小写 / script 首字母大写 / region 大写 / 其余小写 / 分隔符统一 `-`），`__lcLookup()` 三级回退：

| 顺序 | 规则 | 例 |
|---|---|---|
| 1 | 精确匹配规范化标签 | `EN-US` / `en_us` → `en-US` |
| 2 | `language + region`，**script 须与命中项一致** | `zh-Hans-CN` → `zh-CN`（Hans 一致）；`en-Latn-US` → `en-US` |
| 3 | 逐级截尾 `language-script-region → language-script → language` | `zh-Hant-CN` 因 Hant ≠ 简体 zh-CN 的 Hans，跳过第 2 级 → `zh-Hant` |

「script 一致性」是关键：`zh-Hant-CN` 绝不能回退到简体的 `zh-CN`。结果区新增「规范化标签 / 匹配键」两行，让回退过程可见、可断言。

## 三、XSS 条目（真未修，本批实修）

清单「2026-11-06 IT 工具静态续审」记录 `raw` 与 `parts[]` 未经转义拼进 `data-zh` 属性与正文后赋给 `innerHTML`。本页**确实没有任何转义**（与第 22 批 area-code-lookup 的「已修未删」不同）。

**修复**：新增 `__lcEsc()` 统一转义 `& < > " '`，覆盖原始输入与所有子标签派生值；去掉 `<p data-zh="输入：${raw}">` 属性（用户输入不该作为翻译键）。

**jsdom 真机取证**：`en-US<img src=x onerror=1>` 与 `zh-Hans"><b>X</b>` 两种输入，结果区真实 `img/script/b` 元素数 **zh 0 / en 0**，注入内容以字面文本呈现。

## 四、英文态动态结果区中文残留（同类漏检）

与第 21 批 msisdn-lookup 同因：`_en_i18n_probe.mjs --check` 不执行页面脚本，看不到 `validate()` 动态串。真机注入后发现两层中文：

1. UI 标签（`语言（ISO 639-1）：` / `完整名称：` / 结果结论）→ 用 `__lcL(zh,en)` helper 双语化；
2. **`LOCALES` 数据库字段本身是中文**（`英语（美国）`、`简体中文（中国大陆）` 等）→ 仅翻标签不够，真机仍报 8/11 场景残留。故新增 `LC_EN_LANG`（25 条）、`LC_EN_COUNTRY`（43 条，港/澳/台按 `Hong Kong, China` / `Macao, China` / `Taiwan, China` 合规标注）、`LC_EN_SORT`（2 条）与 `__lcFullEn()` 组合英文完整名。

修正后真机 **11/11 场景英文态 0 中文残留、0 JS 异常**；`--check` / `--roundtrip` 均 0。中文态输出逐字保持不变，既有两条用例零改动即通过。

## 五、测试同步（`scripts/verify_it_calc.js` 新增 11 条，1218 → 1229）

| # | 条目 | 输入 | expect 要点 | 修复前 |
|---|---|---|---|---|
| 1 | N421 | `de-DE-1996` | 「Input: de-DE-1996 … 完整名称： 德语（德国）」 | ❌ 不符合 BCP 47 格式 |
| 2 | N421 | `es-419` | 「国家 419 ✅ BCP 47 格式有效（数据库中无此条目）」 | ❌ |
| 3 | N421 | `en-US-u-ca-gregory` | 扩展标签 + 「完整名称： 英语（美国）」 | ❌ |
| 4 | N421 | `sl-rozaj-biske-1994` | 多 variant 合法；且**不再**出现「国家：ROZAJ」 | ❌ |
| 5–6 | N422 | `EN-US` / `en_us` | 「Input: EN-US（或 en_us）… 完整名称： 英语（美国）」 | 仅「格式有效 / 无此条目」 |
| 7 | N422 | `zh-Hans-CN` | 「书写脚本 Hans … 规范化标签 zh-Hans-CN 匹配键 zh-CN」 | 无此条目 |
| 8 | N422 | `zh-Hant-CN` | 「完整名称 繁体中文（语言）… 匹配键 zh-Hant」 | 无此条目 |
| 9 | N422 | `en-Latn-US` | 「书写脚本 Latn … 完整名称 英语（美国）」 | 无此条目 |
| 10 | 护栏 | `123` | 「❌ 不符合 BCP 47 格式」 | 同绿（收紧后仍拒绝纯数字） |
| 11 | 护栏 | `pt-BR` | 「完整名称 葡萄牙语（巴西）」 | 同绿（常规精确匹配不回归） |

**判别力设计**：默认态是 `en-US`，修复后默认 blob 已含「完整名称： 英语（美国）」与「规范化标签： en-US」。故所有命中查表的 expect 一律以 `Input: <原始大小写/下划线>` 或「书写脚本 / 匹配键」等**输入派生形态**开头，避开默认态命中；判别器实测 **1228/1228 正确变红、逃生 0**。

## 六、判别力与真机证据

- 正向：`node scripts/verify_it_calc.js` → **1229/1229 通过**。
- **负向对照**：备份 → `git checkout HEAD -- tools/it/locale-lookup.html` → **1220/1229 通过**，恰 9 行 `❌ it/locale-lookup`（新增 11 条中 9 条真变红），2 条**回归护栏**按设计前后同绿 → 恢复后 1229/1229。
- `node scripts/discriminate_check.js verify_it_calc.js` → 已检 1228 / 正确变红 1228 / **逃生 0** / 跳过 1（基线跳过 1）。
- `node scripts/audit_verify_input_ids.js` → 僵尸 id ①0；`check_expect_antipattern.py` → 0 处；`_en_i18n_probe.mjs --check` → 0 残留，`--roundtrip` → 0 不一致；`node --check` 语法 OK。
- **jsdom 真机 11/11 + XSS 专项 2/2**：中英两态逐场景 0 JS 异常、英文态 0 中文残留、两种注入 0 真实元素。
- `formula-eq` 改描述 canonical 化 / 三级回退 / RFC 5646 语法 / HTML 转义，并同步替换 `i18n/tools/en/it/locale-lookup.json` 的中文原文 key。按 2026-11-07 门禁节奏，本批只跑秒级轻量项；本批是上次 push 后的第 1 个本地批次，`_build.py` / 全站门禁继续攒到 ≥5 批统一跑。

## 七、清单清理

`plan/categories/01-IT开发/it.md`：整条删除 `### IT-N421`、`IT-N422`、XSS 续审条目 `### Locale 查询将原始输入拼入 HTML`（标题 + 全部子弹），删除覆盖清单行 ``- `locale-lookup`：IT-N421、IT-N422（中）；无高优缺陷。`` 与「历史结论状态」中的 `- IT-N421、N422 的 locale 查表与正则仍在。`。条目数 **326 → 324**，相关关键词残留 0。
