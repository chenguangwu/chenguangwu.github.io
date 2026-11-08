# 第 27 批 · IT-N473 · slug-generator-advanced 补 NFD 去变音

- 日期：2026-11-08
- 页面：`tools/it/slug-generator-advanced.html`
- 条目：IT-N473（中，承诺未实现）
- 顺带修复：`copyResult` 的 `TBKit.util` 守卫
- 同批：`i18n/tools/en/it/slug-generator-advanced.json`、`scripts/verify_it_calc.js`、本移交档、分类清单

## 一、缺陷：文案承诺 é→e，实现却整字符删除

`formula-list :162` 明写「转小写 → 去除变音符号（如 é→e）→ …」，但 `slugify()` 里没有任何 NFD 规范化：非 CJK 字符先 `out+=c`，随后被 `s.replace(new RegExp('[^a-zA-Z0-9'+escSep+']','g'),'')` 整字符删掉。重音字母直接消失，用户看到的是「少了一个字母」而非「输入有误」。

| 输入 | 修复前 | 修复后 |
|---|---|---|
| `café` | `caf` | `cafe` |
| `naïve résumé` | `nave-rsum` | `naive-resume` |
| `ÉCOLE` | `COLE` | `ECOLE` |
| `e\u0301clair`（分解式） | `eclair` 之外的形态 | `eclair` |
| `Hello World 2024` | `Hello_World_2024` | `Hello_World_2024`（护栏） |

**修复**：按清单方案一，在 `slugify()` 最前端预处理，且带无参守卫（harness 会兜底调用顶层函数，`text` 可能为 `undefined`）：

```js
// IT-N473：先 NFD 分解并删除组合变音标记（é→e、ñ→n），再走后续处理链
let s=String(text==null?'':text).normalize('NFD').replace(/\p{M}/gu,'');
```

用 `\p{M}`（Unicode 组合标记）而非只写 `[\u0300-\u036f]`，覆盖扩展组合区；放在大小写转换之前，故 `É` 与 `é` 都能还原。西里尔等非拉丁字母仍按原策略删除，deep-dive 表本来就写明「非 ASCII 字符需音译或转写」，不构成新矛盾；IT-N472（拼音表仅 59 汉字）是独立缺陷，**仍留在清单**。

`formula-eq` 处理链末尾补「；预处理先做 NFD 规范化并删除组合变音标记（如 é→e）」，并同步替换 `i18n/tools/en/it/slug-generator-advanced.json` 中 `map` 的中文原文 key（旧 key 删除、英文值补 NFD 说明），避免英文态回落中文。

顺带把 `copyResult` 的 `(typeof TBKit!=='undefined'&&TBKit.util.isEn())` 补成 `...&&TBKit.util&&TBKit.util.isEn()`，与前几批 helper 守卫口径统一。

## 二、测试同步（`scripts/verify_it_calc.js` 新增 4 条，1250 → 1254）

| # | 类别 | 输入 | expect | 修复前 |
|---|---|---|---|---|
| 1 | N473 | `café` / sep `-` | `cafe ← café` | ❌ `caf ← café` |
| 2 | N473 | `naïve résumé` / sep `-` | `naive-resume ← naïve résumé` | ❌ `nave-rsum ← …` |
| 3 | N473 | `ÉCOLE` / sep `-` | `ECOLE ← ÉCOLE` | ❌ `COLE ← ÉCOLE` |
| 4 | 护栏 | `Hello World 2024` / sep `_` | `Hello_World_2024 ← Hello World 2024` | 同绿 |

expect 一律用「产物 ← 原文」整段（页面 `generate()` 会回显原文），既绑定输入派生值，又避免只断言 `cafe` 时与回显串的歧义。默认样例是 `Hello World! 这是一条 测试…`，不含任何新 expect ⇒ 判别器 1253/1253 正确变红、逃生 0。

## 三、判别力与真机证据

- 正向：`node scripts/verify_it_calc.js` → **1254/1254 通过**。
- **负向对照**：备份 → `git checkout HEAD -- tools/it/slug-generator-advanced.html` → **1251/1254 通过**，恰 3 行 `❌ it/slug-generator-advanced`（3 条功能用例变红），1 条 ASCII 护栏前后同绿 → 恢复后 1254/1254。
- `node scripts/discriminate_check.js verify_it_calc.js` → 已检 1253 / 正确变红 1253 / **逃生 0** / 跳过 1；`audit_verify_input_ids.js` 僵尸 id ①0；`check_expect_antipattern.py` 0 处；`_en_i18n_probe.mjs --check` → 0 残留、`--roundtrip` → 0 不一致；`node --check` 内联脚本 OK。
- **jsdom 真机**：修复后 5 组输入全部命中预期（含分解式 `e\u0301clair`），`formula-eq` 含 NFD 说明，`<img src=x onerror=1>` 输入下 `#output` 真实 `img/b/script/iframe/svg` 元素数 0（既有 `escapeHtml` 未被破坏），0 JS 异常；`git show HEAD` 修复前页面同探针复跑，`café`/`naïve résumé`/`ÉCOLE` 三项均确认丢字母。
- 探针口径：jsdom 的 `textContent` 里产物与 `←` 之间**没有空格**（`cafe← café`），而 harness `collectStrings()` 会归一出单空格（`cafe ← café`）——两套断言不可混用，真机判据按无空格写。
- 本批是上次 push 后的第 5 个本地批次，按 2026-11-07 门禁节奏在此触发统一 `_build.py` + 全站判别器 + `run_gates.py` + push。

## 四、清单清理

`plan/categories/01-IT开发/it.md`：精确边界断言整条删除 `### IT-N473 …`（标题 + 7 条子弹）；覆盖清单行含**两个编号**，只把 `、IT-N473（中）` 删掉，保留未处理的 `IT-N472（高，承诺未实现）`，避免误销账。行数 **3380 → 3371**，`grep IT-N473` 残留 **0**。
