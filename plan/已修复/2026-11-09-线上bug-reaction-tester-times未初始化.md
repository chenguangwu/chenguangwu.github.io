# 线上 bug 修复 · 申请复核（非复核失败清单条目）

- 来源：老板本回合转述线上会话回放 —— 用户从 Yahoo 搜索进入「反应测试」页，00:02 点「开始」，随后 00:09 / 00:10 / 00:11 多次点「立即点击！」时持续报 `Cannot read properties of undefined (reading 'push')`，按提示「等待变绿后立即点选」无法完成测试。
- 修复日期：2026-11-09；仅本地提交，**未 push、未跑 `_build.py` / `run_gates.py` / 全站判别力 / CI**（老板本回合指令：只本地提交、门禁暂不运行、加快速度）。

## 问题与修复

- 失败点：`onClick()` 在 `state==='ready'` 分支执行 `times.push(rt)` 时抛 TypeError。异常发生在 `times.push` 之后的所有语句之前，因此末尾的 `state='idle'` 永不执行，状态卡在 `ready` ⇒ 用户后续每次点击都重复走进该分支、重复抛错，与回放里 00:09/00:10/00:11 连续三次报错完全吻合。
- 根因：`tools/fun/reaction-tester.html` 声明为 `let state,times,startTime,timeoutId,best;`，五个变量初值全是 `undefined`；`times=[]` 只写在 `reset()` 里，而**页面加载时从未调用 `reset()`**，「开始」按钮直接 `onclick="start()"`，`start()` 也不初始化 `times`。故首次进入「开始 → 变绿 → 点击」这条最正常路径必然崩。附带两个同源缺陷：`state` 初值 `undefined` 使首次点击目标区域（提示「点击"开始"或此处」）不响应；统计包装 `onClick=function(){__f0.apply(...);__tbn();}` 未隔离异常，次要的练习历史/统计模块一旦抛错会反噬主交互。
- 修复位点（均在 `tools/fun/reaction-tester.html`）：
  1. 声明处直接完成初始化：`let state='idle',times=[],startTime=0,timeoutId=null,best=null;`，保证任何加载路径下状态机与成绩数组都可用；
  2. `start()` 首行加 `if(!Array.isArray(times))times=[];` 防御外部改写 / 任何绕过初始化的调用；
  3. `calcReactionAvg(arr)` 加 `Array.isArray(arr)` 守卫（顺带消除 harness 兜底无参调用抛错）；
  4. 统计包装改为 `try{__tbn();}catch(e){}`，次要能力异常不再阻断点击主流程，主流程自身异常照常向上抛出、不掩盖。
- 未改动文案、公式区、默认参数、输入初值，故不涉及 i18n 映射同步。

## 证据

- 4 条回归用例同批落入 `scripts/verify_fun_calc.js`（紧随原 `calcReactionAvg` 纯函数用例之后），全部走真实交互链路：harness 的 `setTimeout` 桩立即执行 ⇒ `start()` 后立即进入 `ready`，再 `onClick()` 复现线上路径。
  - ① `RTINIT=Y STATE=idle BEST=null` —— 页面刚加载即已初始化（旧代码为 `RTINIT=N STATE=undefined BEST=undefined`，本例在旧代码上必然 FAIL）；
  - ② `RTCLICK=N N=1 OK=Y STATE=idle` —— 开始→变绿→点击不抛错、记录 1 次成绩、cur 有值、回到 idle；
  - ③ `RTMULTI=NNN N=3` —— 连续 3 次测试全部成功且成绩累加（对应回放的三次点击）；
  - ④ `RTEARLY=early N=1 STATE=idle` —— 抢跳不记成绩、重试正常记录，覆盖 early/idle/ready 全状态机。
- expect 全部是注入 clicks 才出现的探针串，不含任何时钟相关 ms 数值，避免时间漂移；未使用 `\"` 转义引号。
- 轻量门禁：`verify_fun_calc.js 41/41`；单文件 `discriminate_check.js verify_fun_calc.js` → 已检 41 / 正确变红 41 / **逃生项 0** / 跳过 0；`audit_verify_input_ids.js` → 9875 条用例 / 30066 注入键 / **缺页 0**；页面内联脚本 `node --check` 通过。

## 待复核提示

- 真机复现路径：打开 `/tools/fun/reaction-tester.html` → 点「开始」→ 等待变绿 → 连续点击「立即点击！」3 次，应每次都显示反应时间、最佳/平均与历史，控制台无 TypeError；再点「重置」后重复一轮。
- 本批未 push，线上生效需后续统一攒批发版；依老板指令，全量门禁与正式再次复核在攒批后一并发起。
