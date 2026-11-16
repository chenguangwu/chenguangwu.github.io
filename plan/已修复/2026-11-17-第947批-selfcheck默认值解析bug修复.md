# 第947批：selfcheck 默认值解析器 selected 属性顺序 bug 修复

## 缺陷根因
`scripts/selfcheck_false_pass.js::_pageDefaults()` 取 `<select>` 默认值时，正则
`/<option[^>]*\bselected\b[^>]*value=.../i` 只认「selected 在 value 前」的写法。
但全站 1465 个 `selected` 选项**全部**是 `<option value="x" selected>`（value 在前），
旧正则全部落空 → 回退取「第一个 option 的 value」→ 默认值判错。

后果（双向误判）：
- **误伤真非默认用例**：如 `chinese-cook/wok-heat`（heat=wang，页面默认 zhong 在第 2 项）、
  `rheumatology/behcet-hla`（age=young，默认 middle 在第 2 项），被错判 all_default。
- **漏判真弱用例**：`cognition/time-perception`(bSel=90)、`it/margin-of-error`(n=1000)、
  `music/web-tuner`(refFreq=440)、`sports/sports-calculator`(cyc 50/11/2096/90) 注入值恰等于
  真实默认值，却因默认值被错认成「第一个 option/input」而漏报。

判别器层（`discriminate_check.js`）读页面默认值口径不同，早已正确识别（REPORT 标
`default-snapshot-no-hit`），只有 selfcheck 这一处判错——两工具结论曾矛盾。

## 修复
先定位「带 selected 的那个 `<option>` 标签」，再从该标签内取 value，属性顺序无关：
```js
const selTag = ms[1].match(/<option\b[^>]*\bselected\b[^>]*>/i);
const sel = (selTag && selTag[0].match(/\bvalue=["']([^"']*)["']/i))
         || ms[1].match(/<option[^>]*value=["']([^"']*)["']/i);
```
input/textarea 分支未动。

## 验证（小门禁）
- 修复前 selfcheck：no_inputs=7 / all_default=3（错）
- 修复后 selfcheck：no_inputs=7 / **all_default=4**（准），risk=0，退出码 0，**未突破基线**（10/4）
- 只读模拟（`_sim_fix`）与修复后实测一致；all_default 明细 = 上述 4 条真弱用例
- 相关 verify 抽样全绿：cognition 14/14、it 1783/1783、music 53/53、sports 236/236
- 判别器抽样逃生 0：chinese-cook 7/7、rheumatology 29/29（确认误判的 2 条本就非默认）
- `node --check` 语法通过

## 影响
不进构建产物（scripts 门禁工具），不需跑全量/不触发部署。
all_default 从误报 3 校正为准确 4，压在基线上（只减不增规则未违反）。
修复后弱用例统计口径变准，避免未来维护被误判误导去「加固」本就有效的用例。
