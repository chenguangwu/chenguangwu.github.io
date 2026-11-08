# 第 24 批 · IT-N424 · language-code-lookup 支持 BCP 47 地区标签

- 日期：2026-11-08
- 页面：`tools/it/language-code-lookup.html`
- 条目：IT-N424（中，确认缺陷）
- 顺带修复：「2026-11-06 IT 工具静态续审」的 **XSS 条目（真未修）** + **英文态动态结果区中文残留**
- 同批：`i18n/tools/en/it/language-code-lookup.json`、`scripts/verify_it_calc.js`、本移交档、分类清单

## 一、IT-N424 带地区标签直接查表失败

**缺陷**：`validate()` 把整个 `raw` 转小写后当作查表键，只提供三条路径——ISO 639-1 两字母精确匹配、中文名/英文名子串、ISO 639-3 三字母码。`zh-CN` / `en-US` / `pt-BR` 三段条件全不成立，输出「❌ 未找到匹配的语言」；而页面正文与 deep-dive FAQ 恰恰以 `zh-CN`、`zh-CN vs zh`、`zh-Hans-CN` 为主要讨论对象，工具承诺与实际能力自相矛盾。

**修复**：新增 `__lgParse(raw)`，按 `-` 或 `_` 拆分为 `language[-Script][-REGION]`：

```js
function __lgParse(raw){
  const parts=String(raw==null?'':raw).trim().split(/[-_]/).filter(Boolean);
  const lang=(parts[0]||'').toLowerCase();
  let script='',region='';
  for(let i=1;i<parts.length;i++){
    const p=parts[i];
    if(!script && /^[a-z]{4}$/i.test(p)) script=p.charAt(0).toUpperCase()+p.slice(1).toLowerCase();
    else if(!region && /^(?:[a-z]{2}|\d{3})$/i.test(p)) region=p.toUpperCase();
  }
  return {parts:parts,lang:lang,script:script,region:region};
}
```

- 语言段统一小写、地区段统一大写、书写脚本首字母大写 ⇒ 兼容 `ZH-cn`、`zh_Hans_CN`、`zh-Hant-TW`；
- 查表只取**语言段**，既有的中文名 / 英文名 / ISO 639-3 反查路径逐字保留（回归护栏 4 条验证）；
- 结果区新增「BCP 47 解析： 语言 … / 书写脚本 … / 地区 …」一行，让拆分过程可见、可断言；
- 非 BCP 47 的裸标签（如 `zho`、`fr`、`中文`）不输出解析行，输出形态与修复前完全一致。

覆盖矩阵：`zh-CN`、`en-US`、`pt-BR`（language-REGION）、`zh_Hans_CN`、`zh-Hant-TW`（下划线 + 三段式）、`ZH-cn`（大小写规范化）。

## 二、XSS 续审条目（真未修，本批实修）

清单「2026-11-06 IT 工具静态续审」记录 `raw` 未经转义拼进 `data-zh` 属性与正文后赋给 `innerHTML`。本页**确实没有任何转义**（与第 22 批 area-code-lookup 的「已修未删」性质不同）。

**修复**：新增 `__lgEsc()` 统一转义 `& < > " '`，覆盖原始输入与所有子标签派生值；去掉 `<p data-zh="输入：${raw}">` 属性（用户输入不该作为翻译键）。

**jsdom 真机取证**：`en-US<img src=x onerror=1>` 与 `中文<b>X</b>` 两种输入，结果区真实 `b/img/script/iframe/svg` 元素数 **zh 0 / en 0**，注入内容以字面文本呈现。判据必须是 `querySelectorAll` 的真实元素数，不能用 `innerHTML.includes('<b>')`（会把属性序列化里的字面串误判成注入）。

## 三、英文态动态结果区中文残留（同类漏检）

与第 21/23 批同因：`_en_i18n_probe.mjs --check` 不执行页面脚本，看不到 `validate()` 动态串。真机注入后发现两层中文：

1. UI 标签（`BCP 47 解析：` / `语系：` / `❌ 未找到匹配的语言`）→ 用 `__lgL(zh,en)` helper 双语化；
2. **`LANGS` 数据库字段本身是中文**（`family:'汉藏语系'`、`cn:'中文'`）→ 仅翻标签不够。故新增 `LG_FAMILY_EN`（13 条语系英译，覆盖库内全部 13 种），英文态名称取 `r.en`、语系取映射值；中文态仍为 `r.en（r.cn）` 与原中文语系。

修正后真机 **12 场景 × 中英两态 0 JS 异常、英文态 0 UI 中文残留**；`_en_i18n_probe.mjs --check` → 0 残留、`--roundtrip` → 0 不一致。语系映射覆盖率实测 **13/13 无遗漏**。

**探针口径坑**：查询词本身是中文时（`中文`、`中文<b>X</b>`），`Input: 中文` 是**用户输入的原样回显**，属预期，不算 UI 文案泄漏。扫 CJK 前须先 `text.split(val).join('')` 剔除回显，否则误报 2 处。

**`_verify_en_cjk.mjs --container=output` 报 `：` 的处置**：该脚本用 `runScripts:'dangerously'` 但不加载外链 `/js/tool-kit.js`，`TBKit.util.isEn()` 不存在 ⇒ helper 回落中文 ⇒ 报全角冒号。取 `git show HEAD:tools/it/language-code-lookup.html`（修复前页面）同条件复跑，**同样报 `：`**，确认是脚本既有 harness 局限、非本批回归；正式 EN 验收以 `_en_i18n_probe.mjs --check/--roundtrip` 与自建加载 `tool-kit.js` 的 jsdom 探针为准。

## 四、测试同步（`scripts/verify_it_calc.js` 新增 10 条，1229 → 1239）

| # | 类别 | 输入 | expect 要点 | 修复前 |
|---|---|---|---|---|
| 1 | N424 | `zh-CN` | 「Input: zh-CN BCP 47 解析： 语言 zh / 地区 CN ISO 639-1： zh ISO 639-3： zho」 | ❌ 未找到 |
| 2 | N424 | `en-US` | 同上形态，地区 US / 639-3 `eng` | ❌ 未找到 |
| 3 | N424 | `pt-BR` | 639-3 `por`（非机械补字母） | ❌ 未找到 |
| 4 | N424 | `zh_Hans_CN` | 「书写脚本 Hans / 地区 CN」 | ❌ 未找到 |
| 5 | N424 | `zh-Hant-TW` | 「书写脚本 Hant / 地区 TW」，与 #4 双向对照 | ❌ 未找到 |
| 6 | N424 | `ZH-cn` | 大写原始输入 + 规范化解析，避开默认态命中 | ❌ 未找到 |
| 7 | 护栏 | `zho` | 「ISO 639-1： zh ISO 639-3： zho」 | 同绿 |
| 8 | 护栏 | `中文` | 中文名子串匹配不回归 | 同绿 |
| 9 | 护栏 | `qq` | 无匹配文案逐字不变 | 同绿 |
| 10 | 护栏 | `fr` | 「语言名称： French（法语）」常规精确匹配不回归 | 同绿 |

**判别力设计**：页面默认输入是 `en`，默认 blob 已含「ISO 639-1： en ISO 639-3： eng」。故 6 条功能用例的 expect 一律以 `Input: <原始标签>` + 「BCP 47 解析」输入派生段开头并串接 639-1/639-3，避免任何单条在默认态命中（expect 是「或」语义，任一静态串命中即整条逃生）。判别器实测 **1238/1238 正确变红、逃生 0**。

## 五、判别力与真机证据

- 正向：`node scripts/verify_it_calc.js` → **1239/1239 通过**。
- **负向对照**：备份 → `git checkout HEAD -- tools/it/language-code-lookup.html` → **1233/1239 通过**，恰 6 行 `❌ it/language-code-lookup 未匹配期望值`（6 条功能用例真变红），4 条**回归护栏**按设计前后同绿 → 恢复后 1239/1239。
- `node scripts/discriminate_check.js verify_it_calc.js` → 已检 1238 / 正确变红 1238 / **逃生 0** / 跳过 1（基线跳过 1）。
- `node scripts/audit_verify_input_ids.js` → 僵尸 id ①0；`check_expect_antipattern.py` → 0 处；`_en_i18n_probe.mjs --check` → 0 残留，`--roundtrip` → 0 不一致；`node --check` 内联脚本语法 OK。
- **jsdom 真机 12 场景 × 两态 + XSS 专项 2 种输入**：0 JS 异常、英文态 0 UI 中文残留、0 真实注入元素。
- `formula-eq` 改描述 BCP 47 拆分 / ISO 639-1 精确匹配 / 名称与 639-3 反查 / HTML 转义，并同步替换 `i18n/tools/en/it/language-code-lookup.json` 的中文原文 key（旧 key 已删，避免英文态回落中文）。按 2026-11-07 门禁节奏，本批只跑秒级轻量项；本批是上次 push 后的第 2 个本地批次，`_build.py` / 全站门禁继续攒到 ≥5 批统一跑。

## 六、清单清理

`plan/categories/01-IT开发/it.md`：精确边界断言整条删除 3 处——`### IT-N424 …`（标题 + 6 条子弹）、`### 语言代码查询将原始输入拼入 HTML …`（XSS 续审条目，标题 + 子弹）、覆盖清单行 ``- `language-code-lookup`：IT-N424（中）；无高优缺陷…``。行数 **3411 → 3399**，`grep 'IT-N424|language-code-lookup|语言代码查询将原始输入'` 残留 **0**。

## 七、IT-N423 暂缓说明（不算通过，仍留在清单）

`country-code-lookup` 的 IT-N423 需扩充 ISO 3166-1 全表：本地无权威数据源（`pycountry` 未安装、项目 `json/` 无可复用全表），手写 170+ 条 cc / ISO3 / 首都 / 货币值易引入标准值错误。按「标准值查权威源」纪律暂缓，本批改做同清单的 IT-N424；IT-N423 **仍原样保留在分类清单**，不得标为已修。
