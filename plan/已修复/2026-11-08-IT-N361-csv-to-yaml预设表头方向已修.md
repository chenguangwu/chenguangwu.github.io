# IT-N361 csv-to-yaml 预设「含表头/无表头」方向相反 —— 已修复，申请复核

- 分类：01-IT开发 / it
- 工具：`tools/it/csv-to-yaml.html` + 共享库 `js/tool-kit.js`
- 移交批次：2026-11-08 批次（真缺陷修复）

## 缺陷

页面 `top_1` 是「无表头」开关（勾选 ⇒ 每行输出为数组）。四个预设却用 `'0'/'1'/''` 表达开/关：

```
默认参数  top_1:'0'   → !!'0' === true  ⇒ 勾上「无表头」（应为不勾）
含表头    top_1:'1'   → 勾上「无表头」（与标签完全相反）
无表头    top_1:''    → !!'' === false ⇒ 不勾（与标签完全相反）
多列      top_1:'1'   → 勾上「无表头」（该预设 CSV 带表头，应为不勾）
```

根因在 `js/tool-kit.js` 的 `setValue`：`f.checked = !!val`，字符串 `'0'` 是真值。

## 修复

1. **`js/tool-kit.js`（共享库，系统性修）**

```js
var isOff = val === false || val === 0 || val === '0' || val === 'false' || val === 'off' || val === '' || val == null;
f.checked = !isOff;
```

`'0'`/`'false'`/`'off'`/`''`/`null` 一律视为「未勾选」；其余仍按真值处理。仅影响 checkbox/radio，text/select/textarea 分支不动。

2. **`tools/it/csv-to-yaml.html`（预设方向改对 + 改用布尔值）**

```js
{label:'默认参数', values:{'top_1':false}}
{label:'含表头',   values:{'top_1':false, csv:'name,age\nAlice,30\nBob,25'}}
{label:'无表头',   values:{'top_1':true,  csv:'Alice,30\nBob,25'}}
{label:'多列',     values:{'top_1':false, csv:'id,name,score\n1,Tom,90\n2,Jerry,85'}}
```

## 判别力实测

**jsdom + 本地 HTTP 真机**（页面用绝对路径 `/js/tool-kit.js`，file:// 加载不到脚本，故起 127.0.0.1 静态服务）：

```
preset chips: 默认参数 | 含表头 | 无表头 | 多列
含表头   | top_1.checked = false | 输出: - name: "Alice" age: "30" - name: "Bob" age: "25"
无表头   | top_1.checked = true  | 输出: - ["Alice", "30"] - ["Bob", "25"]
默认参数 | top_1.checked = false | 输出: 键值对形态（沿用当前 CSV）
多列     | top_1.checked = false | 输出: - id: "1" name: "Tom" score: "90" ...
```

四个预设的勾选方向与标签一致，数组/键值对形态也对上。

**门禁护栏（harness 覆盖不到预设芯片，故护栏钉在勾选语义上）**

```
slug:   it/csv-to-yaml
inputs: { csv: "Alice,30\nBob,25" }
clicks: ["document.getElementById('top_1').checked=true; calcTool()"]
expect: ['- ["Alice", "30"]', '- ["Bob", "25"]']
```

勾选「无表头」必须输出数组形态；若方向被改回相反，输出变成 `- Alice: "Bob"` 键值对 ⇒ 断言失败。

## 影响面核查

`'0'` 字符串传给 checkbox/radio 的预设全站只有本页 `top_1`（其余 `'0'` 如 box-shadow 的 `x/y/blur/spread`、crontab 的 `f_min`、caa 的 `flag`、wifi 的 `hidden` 都是 text/select 元素，不走该分支）。

`node scripts/verify_it_calc.js` → **1079/1079 通过**；`discriminate_check.js verify_it_calc.js` → **已检 1078 / 正确变红 1078 / 逃生 0**。全站门禁在批次推送前统一跑（含 build）。
