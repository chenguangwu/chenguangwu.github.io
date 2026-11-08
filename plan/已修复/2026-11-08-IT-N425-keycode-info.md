# 第 25 批 · IT-N425 · keycode-info 不再吞掉键盘默认行为

- 日期：2026-11-08
- 页面：`tools/it/keycode-info.html`
- 条目：IT-N425（中，确认缺陷）
- 顺带修复：英文态动态结果串硬中文残留
- 同批：`i18n/tools/en/it/keycode-info.json`、`scripts/verify_it_calc.js`、本移交档、分类清单

## 一、缺陷：全局 `preventDefault` 破坏键盘可用性

**现象**：`window` 的 `keydown` 监听在「事件目标不是 BUTTON」时无条件 `e.preventDefault()`。页面加载后按空格/方向键不滚动、连续 Tab 焦点停在链接后不再前进，键盘与读屏用户无法正常浏览；`:275` 的 `if(e.key==='F12'){}` 是空分支，注释写「允许默认」但随后照旧执行 `preventDefault`，F12 也一起被吞。

**真机复现（jsdom 派发真实 `cancelable:true` 的 keydown，`git show HEAD` 修复前页面）**：

| 场景 | 修复前 `defaultPrevented` | 修复后 |
|---|---|---|
| Tab | **1** | 0 |
| Space | **1** | 0 |
| ArrowDown | **1** | 0 |
| F12 | **1** | 0 |
| Ctrl+Shift+A | **1** | 0 |
| 目标为 BUTTON | 0 | 0 |

序列 `1/1/1/1/0/1` → `0/0/0/0/0/0`，证实清单对 F12 空分支的判断（注释与行为不符）。

**修复**：按清单方案「本页无输入控件，无需拦截」——把匿名 handler 抽成顶层函数 `__kcOnKeyDown(e)` 并 `window.addEventListener('keydown',__kcOnKeyDown)`，**删除整段 `e.preventDefault()` 与 BUTTON 分支**，也删掉误导性的 F12 空分支。展示逻辑（`keyOut` / `codeOut` / `keyRawOut` / `kcOut` / `modOut` / 结果区）逐字保留，只改「是否拦截」这一件事。

```js
/* IT-N425：本页无输入控件，不拦截任何按键的默认行为。
   Tab 焦点切换、空格/方向键滚动、F12 等浏览器快捷键保持原生可用，仅展示按键信息。 */
function __kcOnKeyDown(e){ ... document.getElementById('result').innerHTML=__h0; }
window.addEventListener('keydown',__kcOnKeyDown);
```

抽成顶层函数是回归可测的前提：harness 的 `win.addEventListener` 对 `keydown` 静默忽略（只收集 `DOMContentLoaded` / `load`），匿名 handler 在 harness 里**根本无法触发**。改成具名顶层函数后，`clicks` 探针可直接调用并统计 `preventDefault` 次数。

## 二、英文态动态结果串（同类漏检）

`/tmp` 真机探针在 `?lang=en-US` 下派发按键，结果区仍输出「捕获到 keydown 事件 · …」。该串是运行时拼进 `innerHTML` 的，`_en_i18n_probe.mjs --check` 只看静态默认态，看不到。

**修复**：新增 `__kcL(zh,en)` helper（带 `TBKit.util &&` 守卫），动态串改 `Captured keydown event · …`；顺带把 `modOut` 的 `None/无` 三元也接入同一 helper，中文态输出逐字不变。

`formula-eq` 原写明「若事件来源是按钮则不拦截默认行为，其余情况阻止默认行为」，与修复后行为矛盾，故改为「不拦截任何按键的默认行为，Tab 焦点切换、空格与方向键滚动、F12 等浏览器快捷键均保持原生可用；结果区文案按当前语言输出」，并**同步替换** `i18n/tools/en/it/keycode-info.json` 中 `map` 的中文原文 key（旧 key 已删，英文值同步改写），避免英文态回落中文。

## 三、测试同步（`scripts/verify_it_calc.js` 新增 7 条，1239 → 1246）

| # | 类别 | 探针驱动 | expect |
|---|---|---|---|
| 1 | N425 | 5 种按键逐一统计 `preventDefault` 调用数 | `KC425 prevent=0/0/0/0/0` |
| 2 | N425 | Tab + 三项展示值 | `KC425_TAB show=Tab\|Tab\|9 prevented=0` |
| 3 | N425 | 空格 + Ctrl/Shift 修饰键 | `KC425_SPACE show=Space mods=Ctrl + Shift prevented=0` |
| 4 | N425 | F12 空分支专项 | `KC425_F12 key=F12 prevented=0` |
| 5 | 护栏 | 目标为 BUTTON | `KC425_BUTTON prevented=0` |
| 6 | 护栏 | 中文态无修饰键 | `KC425_ZH mods=无 prevented=0` |
| 7 | 英文态 | 临时 mock `TBKit.util.isEn=true` | `KC425_EN captured=1` |

探针统一在 `clicks` 里构造带 `preventDefault` 计数器的假事件、调用 `__kcOnKeyDown`，再把计数写进 `#result`。**判别力**：判别器快照态不执行 `clicks`，所有探针串在默认态均不出现 ⇒ 1245/1245 正确变红、逃生 0。所有 `clicks` 只用单引号、不含 `\"` 转义引号与正则/注释字面量（避免 `extractCases()` 字符串感知括号匹配吞掉闭合括号）。

## 四、判别力与真机证据

- 正向：`node scripts/verify_it_calc.js` → **1246/1246 通过**。
- **负向对照**：备份 → `git checkout HEAD -- tools/it/keycode-info.html` → **1239/1246 通过**，恰 7 行 `❌ it/keycode-info`；恢复后 1246/1246。修复前页面是匿名 handler，harness 中 `__kcOnKeyDown` 不存在 ⇒ 7 条探针全部变红，与真机行为证据相互印证。
- `node scripts/discriminate_check.js verify_it_calc.js` → 已检 1245 / 正确变红 1245 / **逃生 0** / 跳过 1（基线跳过 1）。
- `node scripts/audit_verify_input_ids.js` → 僵尸 id ①0（用例无 `inputs` 键，纯 clicks 驱动）；`check_expect_antipattern.py` → 0 处；`_en_i18n_probe.mjs --check` → 0 残留、`--roundtrip` → 0 不一致；`node --check` 内联脚本语法 OK。
- **jsdom 真机（本批主证据）**：修复后中英两态各 6 场景共 12 次真实 `keydown` 派发，`defaultPrevented` 全 0、展示值全正确、英文态 0 UI 中文残留、0 JS 异常；XSS 场景 `key='<img src=x onerror=1>'` 结果区真实 `img/b/script/iframe/svg` 元素数 0；修复前同脚本复跑得 `1/1/1/1/0/1`。
- 按 2026-11-07 门禁节奏，本批只跑秒级轻量项；`_build.py` / 全站门禁继续攒到 ≥5 批统一跑。

## 五、清单清理

`plan/categories/01-IT开发/it.md`：精确边界断言整条删除 `### IT-N425 …`（标题 + 7 条子弹）与覆盖清单行 ``- `keycode-info`：IT-N425（中）；无高优缺陷…``。行数 **3399 → 3389**，`grep 'IT-N425|keycode-info'` 残留 **0**。
