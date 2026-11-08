# 第 29 批 · IT-N475 · math-evaluator 历史「复用」链路收口与构建源防复发

- 日期：2026-11-09
- 页面：`tools/it/math-evaluator.html`
- 条目：IT-N475（中，功能失效）——**清单已修未删**，本批补契约、修构建源、补回归
- 顺带修复：英文态历史区按钮「复用」/空态「暂无记录」硬中文
- 同批：`scripts/gen_itools_t1.py`、`scripts/verify_it_calc.js`、本移交档、分类清单

## 一、定性：清单描述的缺陷已被历史安全提交修掉，但构建源仍会复发

`git log -S 'JSON.stringify(x.e)' -- tools/it/math-evaluator.html` 显示：

- `791a24e0c6` 首次引入内联 onclick 拼接；
- **`5640fa93c6`（fix(security): 修复 IT/文娱 4 页 DOM XSS 与动态执行注入）** 把 `renderHist` 改成 `document.createElement` + `addEventListener`，页面侧缺陷已消失；
- 但清单条目没删，且 **`scripts/gen_itools_t1.py:109` 仍是旧模板**：

```python
return '<div>'+escH(x.e)+' = ... <button ... onclick="document.getElementById(\'expr\').value='
       +JSON.stringify(x.e).replace(/</g,'\u003c')+';calc()">复用</button></div>';
```

该生成器是 10 个 IT 工具的批量生成源（README §scripts），重跑即把 N475 与 XSS 一起写回页面 ⇒ **真实复发风险**。本批按「改源不改 HTML」纪律同步修复构建源，而不是只清条目。

**修复前真机证据**（`git show 5640fa93c6^:tools/it/math-evaluator.html` 载入 jsdom）：`calc()` 生成历史后，按钮 `getAttribute('onclick')` 恰为

```
document.getElementById('expr').value=
```

双引号在 `JSON.stringify` 产物的起始 `"` 处提前闭合，其余片段被浏览器当属性名；改 `#expr='1+1'` 后点击，输入框仍是 `1+1`（功能完全失效）。

## 二、本批实际改动

### 1) 页面：抽顶层复用函数 + 安全属性 + 双语化

```js
function __meL(zh,en){return (typeof TBKit!=='undefined'&&TBKit.util&&TBKit.util.isEn())?en:zh;}
/* IT-N475：历史「复用」统一走此函数。表达式只经 DOM 属性赋值回填，
   不拼进内联 onclick，避免 JSON.stringify 的双引号截断属性与 HTML 注入。 */
function __meReuse(expr){
  document.getElementById('expr').value=String(expr==null?'':expr);
  calc();
}
```

`renderHist` 每个按钮改为 `btn.dataset.expr=String(x.e==null?'':x.e)` + `btn.textContent=__meL('复用','Reuse')` + `btn.addEventListener('click',function(){__meReuse(x.e);})`；空态改 `__meL('暂无记录','No Records Yet')`，与 `js/tool-i18n-en.js` GEN_UI_MAP 的既有译法口径一致。

`__meL` 只是从 `calc()` 之前**前移**到 `renderHist()` 之前（第 28 批已有），中文态输出逐字不变。字符白名单、`MATH_ALLOWED`、取模/百分比判定（N474）一律未动。

### 2) 构建源 `scripts/gen_itools_t1.py`

`renderHist` 整块（原 105–111 行）替换为与页面同构的 `createElement`/`createTextNode`/`addEventListener` 写法，并前置 `__meL` + `__meReuse`。校验：

- 全文件 `JSON.stringify(x.e)` 出现 **0 次**；
- dry-run 导入模块取 `math-evaluator.html` 的 `script` 字段 → `node --check` **SYNTAX_OK**、含 `dataset.expr`、无 `onclick=`；
- `py_compile` OK。生成器不在 `_build.py` 链上，本批**未重跑生成器**、未改 10 个已上线页面。

### 3) 顺带修的英文态真缺陷

`_en_i18n_probe.mjs --check` 只扫静态默认态（当时 0 残留），看不到 `renderHist()` 运行时创建的按钮。真机 `?lang=en-US` + `calc()` 实测 `#hist.textContent = "2^10 + sqrt(144) = 1036 复用"`，CJK 命中 `["复","用"]`。现英文态输出 `Reuse` / `No Records Yet`，`textContent` 零 CJK。

## 三、测试同步（`scripts/verify_it_calc.js` 新增 4 条，1260 → 1264）

| # | 类别 | clicks 契约 | expect | 负向变体 |
|---|---|---|---|---|
| 1 | 功能 | `__meReuse('2^10 + sqrt(144)')` 回填并重算 | `N475 reuse=2^10 + sqrt(144)\|hit=1` | ❌ |
| 2 | 功能 | `__meReuse('7%3')` 完整走 N474 取模链 | `N475 mod=1` | ❌ |
| 3 | 结构 | `String(renderHist)+String(__meReuse)` 含 `addEventListener`/`dataset.expr` 且无 `onclick=` | `N475 src=1` | ❌ |
| 4 | 双语 | `String(renderHist)` 含 `__meL` 与 `Reuse` | `N475 i18n=1` | ❌ |

**harness 坑（本批新增经验）**：首版 C3/C4 在 `clicks` 里写 `for` 循环 / 对象字面量 / `function(){…}` 等花括号，用例恒红且 `errs` 为空、blob 只剩 `#hist` 内容 —— 长 clicks 串里的 `{`/`}` 影响 `extractCases()` 的字符串感知括号匹配，探针语句被吞掉。极简单段 PING 探针 1264/1264 通过可反证。定稿改为**无花括号单段 clicks + `String(fn)` 源码契约**；真实 DOM 点击链路由 jsdom 真机探针覆盖，判别力不降级。同类既有纪律：「长 clicks 禁写 `\"` 转义引号」应扩展为「长 clicks 尽量不写花括号 / 复杂控制流，状态用 `globalThis` 传递或改源码契约」。

## 四、判别力与真机证据

- 正向：`node scripts/verify_it_calc.js` → **1264/1264 通过**。
- **负向对照（内存变体，非 `git checkout HEAD`）**：HEAD 页面已修，直接回退不会让新用例变红。故从修复后页面构造「缺陷复发」变体（删 `__meReuse` + `renderHist` 换回 `h.map` 内联 onclick + 硬中文），落 `/tmp/me475_neg.html` 覆盖页面 → **1260/1264**，恰 4 行 `❌ it/math-evaluator`；恢复后 **1264/1264**。
- `node scripts/discriminate_check.js verify_it_calc.js` → 已检 **1263 / 正确变红 1263 / 逃生 0 / 跳过 1**；`audit_verify_input_ids.js` 僵尸 id ① **0**（207 文件 / 9680 用例）；`check_expect_antipattern.py` **0** 处；`_en_i18n_probe.mjs --check` **0 残留**、`--roundtrip` **0 不一致**；页面内联脚本 `node --check` OK。
- **jsdom 真机（`/tmp/me475_probe.cjs`，共 21 项全 OK）**：
  - 中文态：生成按钮无 `onclick` 属性、`data-expr="2^10 + sqrt(144)"`、标签 `复用`；改输入为 `1+1` 后点击 → 回填 `2^10 + sqrt(144)`、结果 `结果：1036`。
  - 英文态：`isEn()===true`、标签 `Reuse`、`#hist` 0 CJK；点击回填 `7%3` 并重算 `Result: 1`；`clearHist()` 后 `No Records Yet` 且 0 CJK；两态 0 JS 异常。
  - 修复前版本：`onclick` 属性值截断为 `document.getElementById('expr').value=`、点击不回填。
  - 构建源：0 处旧写法、产出脚本无 `onclick=`。

## 五、清单清理与攒批状态

`plan/categories/01-IT开发/it.md`：精确边界断言整条删除 `### IT-N475 …`（标题 + 7 条子弹），覆盖清单行含两个编号，只删 `、IT-N475（中）`、保留未处理的 `IT-N470（高，安全）`。行数 **3362 → 3353**，`grep IT-N475` 残留 **0**。

本批为上次 push 后第 **2** 个本地批次（第 28 批 `dba232a210` + 本批），按 2026-11-07 门禁节奏只跑秒级轻量项。本批改了 `tools/**`（进构建产物）与 `scripts/gen_itools_t1.py`，**攒到 ≥5 批统一 `_build.py` 后需 grep 核验 `__meReuse` / `dataset.expr` / `No Records Yet` 未被构建覆盖**。
