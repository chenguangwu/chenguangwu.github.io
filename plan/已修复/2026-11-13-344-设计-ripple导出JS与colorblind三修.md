# 第344批·design 2 项（ripple 兑现 CSS/JS 承诺、colorblind 三处小缺陷）

## 1. D-N95 ripple-effect：文案承诺「导出 CSS/JS」，实际只复制 CSS

**根因**：meta description / og / twitter / 公式框均写「导出 CSS / JS 代码片段」，但 `generate()` 只把 CSS 写进 `#cssOutput`，且 `copyResult` 提示「已复制 CSS」。点击型 ripple 缺了关键的一段 JS（生成 `.ripple` span 并移除），用户拿到的 CSS 单独无法工作。

**改动**（`tools/design/ripple-effect.html`）
```js
let js = '';
if(type === 'click'){
  js = '\n/* JS：事件委托，点击容器时在点击处生成波纹 */\n'
     + 'document.querySelectorAll(\'.ripple-container\').forEach(function (box) {\n'
     + '  box.addEventListener(\'click\', function (e) { ... box.appendChild(s); ... });\n'
     + '});\n';
}
document.getElementById('cssOutput').value = css + js;
```
- JS 片段的 `setTimeout` 时长取当前 `duration`（与 CSS 动画同源）。
- 非 click 型（pulse / multi）本来就只需 CSS，不追加，避免误导。
- 复制提示改为「已复制 CSS/JS 代码」。

**验证**：强锁并入该页第 1 条用例（`inputs` 注入 duration=1.5）：
```
clicks: generate(); 读 #cssOutput → 'RIP css=Y js=Y'
expect: "RIP css=Y js=Y"
```
旧码 `js=N` ⇒ 红（实测 3/4），新码 4/4。

## 2. D-N153 colorblind-simulator 三处小缺陷（`js/tools/colorblind-simulator.js`）

| # | 问题 | 改动 |
|---|---|---|
| ① | UI 模式 `wcagThresholds` 返回 `aaa: 3.0`，表格列出伪 AAA 档（WCAG 2.2 非文本对比度只有 AA 3:1，无 AAA） | `aaa: null`；表头 AAA 列在 UI 模式渲染「—」，`paaa` 判定加 `th.aaa !== null`，结论句「已达 AAA」同口径加保护 |
| ② | `buildCompare()` 每次调用都 `window.addEventListener('mouseup'/'touchend', onUp)`，重渲染累积监听 | 改为 `window.__c3OnUp = onUp` 只换引用；全局 up 用 `window.__c3UpBound` 标志只注册一次，回调转发到当前引用 |
| ③ | 导出名直接拼 `S3.name`（已含扩展名）⇒ `cvd-8types-photo.jpg.png` | `String(S3.name || 'image').replace(/\.[^.]+$/, '')` |

**未补强锁用例**：本页逻辑集中在 `js/tools/colorblind-simulator.js` 的 IIFE 内（`wcagThresholds` / `S3` 均不可达），且 pane 4 表格依赖 canvas 相关初始化；harness 只能通过事件驱动间接观察，判别力弱于源码 diff，故以 `node --check` + 源码审查交付，真机复核项记入下轮清单。

## 验证

- `node scripts/verify_design_calc.js` → **354/354**（ripple 用例改写后仍全绿）。
- `node scripts/check_inline_js_syntax.js` → 12141/12141。
- `node --check js/tools/colorblind-simulator.js` → 通过。
- `python3 _build.py` → EXIT=0。

## 销账

`plan/categories/04-设计创意/design.md` 删除 D-N95 / D-N153，剩余 74 → 72 项。

## harness 认知更正（重要）

第343批记录的「同 slug 第 3 条及以后用例不执行」**不成立**：把 ripple-effect 第 3 条用例的 expect 临时改成不可能值后确实变红（说明执行）。真实原因是那两条用例的 `clicks` 自身抛错，导致探针未写入 —— 新增用例断言不生效时，应先看 `errs` 里是否有 `click:...` 记录。

## 状态

- 已本地 commit（新一轮第 5 批，随后统一跑全量门禁并推送）。
