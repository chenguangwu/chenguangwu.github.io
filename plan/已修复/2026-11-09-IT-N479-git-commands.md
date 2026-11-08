# 第 31 批 · IT-N479 · git-commands 58 个复制按钮全量复活

- 日期：2026-11-09
- 页面：`tools/it/git-commands.html`
- 条目：IT-N479（高，承诺未实现）
- 顺带修复：英文态动态按钮文本「复制」硬中文
- 同批：`scripts/verify_it_calc.js`、本移交档、分类清单

## 一、缺陷：58/58 内联 onclick 无法编译

`renderCommands()` 把示例原文（含真实换行）只做 `"→&quot;`、`'→&#39;` 转义后拼进属性：

```js
const exampleForCopy = c.example.replace(/"/g, '&quot;').replace(/'/g, '&#39;');
// ...
<button type="button" class="copy-btn" onclick="copyCode(this, '${exampleForCopy}')">复制</button>
```

HTML 解析保留属性内换行 ⇒ 内联 JS 的单引号字符串出现字面换行 → `SyntaxError: Invalid or unexpected token`；`git tag -l 'v1.*'` 这类含单引号的示例还会因 `&#39;` 被还原成 `'` 提前闭合。真机复现（`git show HEAD` 页面载入 jsdom）：**58/58 onclick 属性值含换行、58/58 `new Function` 编译抛错、点击按钮 `writeText` 调用 0 次** —— 与页面 description/og:description 承诺的「点击示例右上角按钮可一键复制」完全相反。

## 二、修复：`data-idx` + 容器事件委托

按清单方案一，按钮只携带 **COMMANDS 原始下标**，容器上一次性委托：

```js
function __gcL(zh,en){return (typeof TBKit!=='undefined'&&TBKit.util&&TBKit.util.isEn())?en:zh;}
/* IT-N479：示例含真实换行与单引号，禁止把多行/带引号文本拼进内联 onclick。
   按钮只携带 COMMANDS 原始下标，容器上一次性事件委托按索引取回原文复制。 */
function copyCodeByIdx(btn){
  const idx=Number(btn&&btn.dataset?btn.dataset.idx:-1);
  const c=COMMANDS[idx];
  if(c) copyCode(btn,c.example);
}
document.getElementById('cmdList').addEventListener('click', function(e){
  const t=e.target;
  const b=t&&t.closest?t.closest('.copy-btn'):null;
  if(b) copyCodeByIdx(b);
});
```

模板改为 `<button type="button" class="copy-btn" data-idx="${idx}">${__gcL('复制','Copy')}</button>`，其中 `const idx = COMMANDS.indexOf(c)`。**必须用原数组下标而非 `filtered` 的下标** —— 搜索 `push` 后首个按钮的 `data-idx` 是 **25**，若用过滤后索引会复制到 `COMMANDS[0]` 的配置示例。真机已验证该场景。

`copyCode(btn, code)` 去掉了 HTML 实体反转义（旧的 `&quot;`/`&#39;` 只是属性转义产物，现在直接传 `c.example` 原文；继续反转义反而会误伤原文里的字面实体）。搜索/分类过滤、`showToast`、`✅` 反馈全部未改。

**范围说明**：`COMMANDS` 的 `desc`/`cat`/`params` 等数据值本身是中文，属全站既有的数据本地化缺口（`--check` 只扫静态 DOM 与默认态，不覆盖），本批不扩范围，只把**本批新增的按钮文本**双语化；中文态逐字不变。

## 三、测试同步（`scripts/verify_it_calc.js` 新增 3 条，1269 → 1272）

| # | clicks 契约 | expect | 修复前 |
|---|---|---|---|
| 1 | `renderCommands()` 后读 `#cmdList.innerHTML`，断言无 `onclick=` 且有 `data-idx=` | `N479 noinline=1` | ❌ |
| 2 | `String(copyCodeByIdx)+String(copyCode)` 含 `c.example`/`COMMANDS` 且不含 `&quot;` | `N479 src=1` | ❌ 函数不存在 |
| 3 | 注入 `searchInput='push'`，过滤后 4 个按钮且无内联 onclick | `N479 btns=4 inline=0` | ❌ |

第 3 条同时锁住「过滤后索引不错位」；注入失败回到默认空搜索 ⇒ 58 个按钮 ⇒ 变红，非逃生项。沿用第 29 批经验，clicks 全部**无花括号**，真实点击链路交给 jsdom。

## 四、判别力与真机证据

- 正向：`node scripts/verify_it_calc.js` → **1272/1272 通过**（既有 2 条 `共 4 个命令` / 自动补强用例零改动即通过）。
- **负向对照**：`git checkout HEAD -- tools/it/git-commands.html` → **1269/1272**，恰 3 行红；恢复后 **1272/1272**。
- `node scripts/discriminate_check.js verify_it_calc.js` → 已检 **1271 / 正确变红 1271 / 逃生 0 / 跳过 1**；`audit_verify_input_ids.js` 僵尸 id ① **0**（207 文件 / 9688 用例）；`check_expect_antipattern.py` **0** 处；`_en_i18n_probe.mjs --check` **0 残留**、`--roundtrip` **0 不一致**；页面内联脚本 `node --check` OK；全页 `exampleForCopy` / `onclick="copyCode` 残留 **0**。
- **jsdom 真机（`/tmp/gc_probe.cjs`，20 项全 OK）**：
  - 中文态：58 个按钮、0 个内联 onclick 属性、文本「复制」；**58/58 逐一点击后 `writeText` 内容逐字等于 `COMMANDS[idx].example`**，58/58 保留真实换行；idx=29 的 `git tag -l 'v1.*'` 含单引号示例复制完整。
  - 搜索 `push` → 4 个按钮，首个 `data-idx=25`，点击复制到对应 `git push` 原文而非 `COMMANDS[0]`。
  - 英文态：`isEn()===true`、按钮文本 `Copy` 且 0 CJK、点击复制正常；三态 0 JS 异常。
  - **修复前版本**：58/58 onclick 含换行、58/58 `new Function` 编译抛 SyntaxError、点击 `writeText` **0 次**。
  - 探针坑：`const COMMANDS` 是词法声明，多个 `<script>` 分别 `w.eval()` 后不会挂到 `window`，`w.COMMANDS` / `w.eval('COMMANDS')` 均取不到；须在**同一 script 块末尾**追加 `;window.__N479_CMDS=COMMANDS;` 导出引用。

## 五、清单清理与攒批状态

`plan/categories/01-IT开发/it.md`：精确删除 `### IT-N479 …`（标题 + 9 条子弹），覆盖清单行含两个编号，只删 `IT-N479（高，承诺未实现）、`、保留未处理的 **IT-N487**（git 远程分支示例）。行数 **3340 → 3329**，`grep IT-N479` 残留 **0**。X 批的「只读审计方法声明」段落是历史审计记录、不带缺陷编号，保留。

本批为上次 push 后第 **4** 个本地批次（第 28/29/30 批 + 本批），按 2026-11-07 门禁节奏只跑秒级轻量项，不 push。本批改了 `tools/**`，**攒到 ≥5 批统一 `_build.py` 后需 grep 核验 `data-idx` / `copyCodeByIdx` / `__gcL` 未被构建覆盖**。下一批候选：IT-N476（prime-checker 不校验整数）、IT-N469（MD5 UTF-16 填充，高）、IT-N487（同页远程分支示例，中）。
