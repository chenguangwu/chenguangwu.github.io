# 第 16 批 · IT-N405 · text-to-unicode 辅助平面代理对（已修未删清理）

- 日期：2026-11-08
- 页面：`tools/it/text-to-unicode.html`
- 条目：IT-N405（中，确认缺陷）
- 性质：**「已修未删」清理** —— 缺陷本身已由历史提交 `30d2966f57`（fix(it): 编码往返、组合字符与时间戳 8 页修正）修好，但分类清单条目、覆盖清单行未删，且**修复当时没有补回归用例**。本轮补齐契约用例与负向对照证据，然后整条下线。

## 一、缺陷与既有修复核对

原文条目：逐字符用 `Array.from` 按码点迭代（正确），但 UTF-16 转义只取 `c.charCodeAt(0)`；对 `🚀`（U+1F680）只得高代理 `D83D`，低代理 `DE80` 丢失，输出非法孤立代理转义。

修复前代码（`git show 30d2966f57^:tools/it/text-to-unicode.html` 第 225 行，已核实）：
```js
var utf16='\\u'+c.charCodeAt(0).toString(16).toUpperCase();
while(utf16.length<6){ utf16='\\u0'+utf16.slice(2); }
```

当前代码（已正确）：
```js
if(cp>0xFFFF){
  // 非 BMP 需拆成 UTF-16 代理对，单独取 charCodeAt(0) 只能得到半个代理
  var v=cp-0x10000, hi=0xD800+(v>>10), lo=0xDC00+(v&0x3FF);
  utf16='\\u'+hi.toString(16).toUpperCase()+'\\u'+lo.toString(16).toUpperCase();
}else{
  utf16='\\u'+cp.toString(16).toUpperCase();
  while(utf16.length<6){ utf16='\\u0'+utf16.slice(2); }
}
```
按 UTF-16 标准代理对公式从码点算高低代理，非对特定 emoji 硬编码；BMP 分支保留原有 4 位补零。`hex` 列本来就是 `cp.toString(16)` 按码点输出，无需改。

**本轮不改页面源码**（已正确，避免动线上已验证内容）。

## 二、本轮补齐：回归契约用例

`scripts/verify_it_calc.js` 新增 2 条（累计 1163 → 1165）：

| # | 输入 | expect | 判别设计 |
|---|---|---|---|
| 1 | `txt: "A😀B"` | `U+1F600 \uD83D\uDE00` | 默认样例是「你好 ToolBox 🚀」，**不含 U+1F600** ⇒ 默认态不会命中；修复前只输出 `\uD83D` ⇒ 必红 |
| 2 | `txt: "𝄞A"` | `U+1D11E \uD834\uDD1E` | 高代理不是 D83D 的码点，验证「按公式算」而非硬编码；且辅助平面字符后紧跟 BMP 字符 |

两条都是输入依赖的单一 expect，无静态串、无 OR 逃生。

**为什么不直接用默认样例 🚀 断言**：默认 textarea 就是 `你好 ToolBox 🚀`，修复后默认态 blob 已含 `U+1F680 \uD83D\uDE80` ⇒ 判别器 `snapshotOf` 会判「默认态仍 PASS」＝逃生项。故改用默认样例里不存在的码点。

## 三、判别力实测

- 正向：`node scripts/verify_it_calc.js` → **1165/1165 通过**。
- **负向对照**：`git show 30d2966f57^:tools/it/text-to-unicode.html > tools/it/text-to-unicode.html` 回退到修复前，重跑 → **1163/1165 通过**，日志里恰有 2 行 `❌ it/text-to-unicode 未匹配期望值`（与新增 2 条一一对应）；随后 `git checkout -- tools/it/text-to-unicode.html` 恢复，工作区该页零 diff。
- 僵尸 id：`node scripts/audit_verify_input_ids.js` → ①0。
- 反模式：`python3 scripts/check_expect_antipattern.py` → 0 处。

## 四、清单清理

`plan/categories/01-IT开发/it.md`：
- 整条删除 `### IT-N405`（标题 + 7 条子弹 + 空行，共 9 行）；
- 整行删除覆盖清单 `- text-to-unicode：IT-N405（中）；无高优缺陷…`。

按「分类清单只留未处理项」纪律，不留 `✅ 已修` 占位；本文件为唯一档案。
