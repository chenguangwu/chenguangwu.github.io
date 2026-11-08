# 第 35 批 · IT-N470 · math-evaluator 安全白名单（已修未删 + 构建源防复发）

- 日期：2026-11-09
- 页面：`tools/it/math-evaluator.html`（本批**未改页面**）
- 条目：IT-N470（高，安全）
- 同批：`scripts/gen_itools_t1.py`（生成源）、`scripts/verify_it_calc.js`、本移交档、分类清单

## 一、定性：页面缺陷早已修掉，条目属「已修未删」

`git log -S 'MATH_ALLOWED' -- tools/it/math-evaluator.html` → 唯一引入提交 `5640fa93c6`（`fix(security): 修复 IT/文娱 4 页 DOM XSS 与动态执行注入`），与第 29 批 IT-N475 同源。当前 `calc()` 已有三层防护：

1. 字符白名单 `/^[0-9+\-*\/%^().,\sA-Za-z%]+$/`（仍放行字母，但只是第一层）；
2. **标识符白名单** `MATH_ALLOWED={sin,cos,tan,sqrt,abs,ln,log,floor,ceil,round,min,max,pi,e}` + `expr.match(/[A-Za-z]+/g)` 逐词校验 ⇒ `eval` / `fetch` / `String` / `document` / `constructor` 全部拒绝；
3. **成员访问拦截**：`expr.replace(/\d*\.?\d+/g,'0').indexOf('.')>=0` ⇒ 非数字字面量的 `.` 一律拒绝，`sin(0).constructor` 这类原型链绕过也封死。

`new Function` 只注入数学函数与常量作参数，且不接收全局对象。`vm` 抽页面真实脚本实跑 8 类注入（`eval(String.fromCharCode(50,42,51))`、两条 eval 变体、`fetch(...)`、`localStorage.getItem(...)`、`document.title`、`sin(0).constructor`、裸 `constructor`、`alert(1)`）→ **8/8 输出「表达式含非法字符」**；5 类合法表达式（含 `15.5%`、`7%3`）结果正确。条目描述的「直接返回数字 6 / 真的调用 fetch」在当前页面已不复现。

## 二、本批真正修的缺陷：生成源会复发

`scripts/gen_itools_t1.py:137-155` 的 `math-evaluator.html` 模板**仍是旧 calc**：既无 `MATH_ALLOWED` 也无成员访问检查，`%` 正则还是 IT-N474 之前的 `/(\d+)\s*%/g`。第 29 批只同步了该模板的 `renderHist`（防 N475 复发），calc 本体漏了 ⇒ **重跑生成器会把 IT-N470（安全）、IT-N474（取模/小数百分比）一起写回线上**。

**决定性证据**（`git show HEAD:scripts/gen_itools_t1.py` → `ast` 静态提取 script 字面量，避免执行模块时 `os.makedirs('/tools')` 只读报错 → `vm` 实跑）：

| 旧模板输入 | 实际输出 |
|---|---|
| `eval(String.fromCharCode(50,42,51))` | **结果： 6**（真的执行了 eval） |
| `document.title` | `表达式无效：结果不是有效数字` |
| `fetch(String.fromCharCode(47,47,120,46,99))` | `表达式无效：fetch is not defined` |

3/3 未拦截。旧模板 `MATH_ALLOWED` 命中 0、旧 `%` 正则仍在。

### 修复

把生成器 `calc()` 模板（按行号 `L[136:155]` 精确替换）同步为页面等价实现：标识符白名单、成员访问拦截、IT-N474 的 `/(\d+(?:\.\d+)?)\s*%(?!\s*[0-9A-Za-z_(])/g`、动态串过现有 `__meL`，并保留生成器简洁风格（不复制页面构建注入的 `__gN` NaN 守卫）。**未重跑生成器**、未改其它 9 个工具页模板。

证据：`python3 -m py_compile` OK；dry-run 导入模块取 `fn='math-evaluator.html'` 的 script → `node --check` OK，含 `MATH_ALLOWED`、含 N474 正则、旧 `%` 正则 0 处、含 `__meReuse`、无 `onclick=`；**页面 vs 新生成器 13/13 行为等价**（8 注入同被拒、5 合法表达式结果逐字相同：`2+3→5`、`sin(pi/2)→1`、`15.5%→0.155`、`7%3→1`、`sqrt(144)→12`）。

## 三、测试同步（`scripts/verify_it_calc.js` 1287 → 1292，+5）

页面侧补 5 条安全护栏，防止白名单被后续改动回退：

| # | 探针 | expect | 缺陷态 |
|---|---|---|---|
| 1 | `eval(String.fromCharCode(50,42,51))` 被拒 | `N470 eval=1` | ❌ |
| 2 | `fetch(...)` 被拒 | `N470 fetch=1` | ❌ |
| 3 | `document.title` 被拒 | `N470 doc=1` | ❌ |
| 4 | `sin(0).constructor` 被拒（原型链绕过） | `N470 member=1` | ❌ |
| 5 | 护栏：`sqrt(144)+3` 仍算出 `>15<` | `N470 ok=1` | 同绿 |

**写法约束**：本页 `inputs` 注入会被初始样例表达式覆盖（第 28 批 N474 用例已踩过），故 5 条均为**纯 clicks**，在探针里显式 `document.getElementById('expr').value=…;calc();` 再读 `#result.innerHTML`；全部单引号、无花括号、无 `\"` 转义（沿用第 29 批经验）；判据写进 `#stats` / `#result`，快照态不执行 clicks 必变红。

## 四、判别力与负向对照

- 正向 **1292/1292**；单文件判别器 **1291/1291 正确变红、逃生 0、跳过 1**；僵尸 id **0**、反模式 **0**、`py_compile` / 生成器 `node --check` OK；`--check it/math-evaluator` **0 残留**、`--roundtrip` **0 不一致**。
- **负向对照用内存变体**（页面本来就是修好的，`git checkout HEAD` 不会变红）：删掉 `MATH_ALLOWED` 块与成员访问检查块（8 行），保留 IT-N474 正则与其余修复 → **1288/1292**，恰 **4 行 `❌ it/math-evaluator`** + 1 条护栏同绿；恢复后 **1292/1292**，`RESTORED True`。
- **负向对照新坑（重要）**：缺陷态下 `fetch('//x.c')` 在 Node 24 会真的调用全局 `fetch`，产生**异步未捕获 Promise rejection**，同步 `try/catch` 挡不住 ⇒ `verify_it_calc.js` 进程直接退出、统计行打不出（首次负向只见 4 红行、无汇总）。在页面脚本里写 `var fetch=…` **不生效**（`var` 在 eval 作用域，遮蔽不到 `new Function` 看到的全局）；必须 `globalThis.fetch=function(){return Promise.resolve({ok:false});};` 才改到 vm 全局，统计才能干净落地。这同时也是 IT-N470 危害的最强实证：旧实现确实会发起网络请求。
- 生成器侧复发证据见第二节（旧模板 `eval → 结果：6`）。

## 五、未扩范围

- 清单方案之一「彻底移除 `new Function` / 换 Shunting-yard」未实施：当前三层防护已封闭已知逃逸路径，且替换解析器会改动全部既有计算语义与 13 条用例；本批按「已修未删 + 防复发」收口。
- 生成器其它 9 个工具页模板未逐一审计（本批只处理 `math-evaluator.html` 的 calc；其 `renderHist` 已由第 29 批同步）。
- 未重跑生成器，线上页面本批零字节变化。

## 六、清单清理与攒批

`plan/categories/01-IT开发/it.md`：整条删除 `### IT-N470 …`（标题 + 子弹 + 空行，13 行）与覆盖清单行 ``- `math-evaluator`：IT-N470（高，安全）。``（该页已无未处理项）；W 批「方法声明」历史记录保留。行数 **3292 → 3278**，`grep IT-N470` 残留 **0**。历史移交档中把 IT-N470 列为候选/说明的陈述属当时档案，未改。

本批是上次 push `5e0e9e39ca` 后**第 3 个本地批次**（3/5），按 2026-11-07 门禁节奏只跑秒级轻量项，**不 push**。本批未改 `tools/**`，但改了生成源与门禁用例；攒到 ≥5 批统一 `_build.py` 后需 grep 核验生成器 `MATH_ALLOWED` / N474 正则与页面白名单均未被覆盖。
