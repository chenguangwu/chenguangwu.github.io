# 414 批：认知基准测评切换/重置时定时器写入已删除节点

日期：2026-11-14
页面：`tools/cognition/human-benchmark.html`

## 一、问题

用户从指南页进入后，在序列记忆 / 数字记忆中途重置或切换子测验，控制台报：

```
Uncaught TypeError: Cannot set properties of null (setting 'textContent')
```

原因：各子测验用 `setTimeout/setInterval` 串联回合，回调里重新 `$('sHint')`、
`$('nHint')` 等查询节点；但「重置进度」「切换子测验」只清空 `#hbStage`，
**没有取消上一局的定时器**。定时器随后触发时节点已被移除，`getElementById` 返回 null，
写 `textContent` 直接抛错。数字记忆 1100 ms 的「隐藏数字」回调窗口尤其容易命中。

## 二、修复

在 IIFE 内加入统一的计时器登记与取消：

- `HB_TIMERS` 数组 + `hbLater(fn, ms)` / `hbEvery(fn, ms)`，回调触发后自动出栈；
- `hbCancelAll()` 清空全部 timeout / interval；
- `clearStage()`（切换测验、重置进度都会走）先调用 `hbCancelAll()`；
- `handleResult()` 进入结算页面前也调用一次，避免同局残留回调写入结果页。
- 页面内 15 处 `setTimeout` / 2 处 `setInterval` 全部改走登记接口。

## 三、验证

- 用 Playwright 对同一操作序列做前后对比：
  - 启动序列记忆 → 250 ms 后重置；启动数字记忆 → 400 ms 后重置；启动打字 → 300 ms 后重置。
  - **修复前：2 条 `Cannot set properties of null (setting 'textContent')`**；
  - **修复后：0 条错误**。
- 同类页面冒烟：数字记忆、序列记忆、图案记忆、形状记忆、Corsi、n-back、颜色猜谜、
  反应测试、乘法表、时间知觉、三个心理测验、单词拼写、冷敷计时器，共 15 页，
  开始→重置后均无 pageerror。

## 四、同类扫描结论

- 全站搜索「延迟回调重新查节点 + 动态替换容器」模式，其余页面均使用**渲染时捕获的元素引用**
  或已有 `pendingTimers` / 局次 session 守卫（如 `fun/sequence-memory.html`、`fun/color-guess.html`），
  不会在节点删除后写 DOM。
- `it/` 下 6 个解析页存在未被调用的 `getIndent()`（读取不存在的 `#indent`），属死代码，
  不触发运行时错误；未在本批改动。
- 全站静态测试：**4714/4714 通过**；构建两次幂等。
