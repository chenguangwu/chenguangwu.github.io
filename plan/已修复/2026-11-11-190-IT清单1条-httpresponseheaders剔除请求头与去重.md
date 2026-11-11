# 2026-11-11 第190批 · IT-N459 响应头速查表剔除请求头与去重

## 清单项
- **IT-N459**：速查表把 4 个请求头当响应头收录，且 ETag / Last-Modified 各重复两条（中，参考结果错误）

## 根因
- `COMMANDS` 数组混入了 4 个只会出现在请求里的头：`Access-Control-Request-Method`、`Access-Control-Request-Headers`（CORS 预检请求头）、`Range`（范围请求头）、`Want-Digest`（RFC 9530 请求头）；同时 ETag、Last-Modified 各有一条内容简略的重复项，导致「共 N 项」计数偏高、分类明细统计（含图表）偏高。
- 页面定位是「HTTP 响应头速查」，用户拿这张表逐项核对生产响应头时会去查一个永远不会出现的头。

## 改动
`tools/it/http-response-headers.html` 的 `COMMANDS`：
1. 删除 4 个请求头条目：`Access-Control-Request-Method`、`Access-Control-Request-Headers`、`Range`、`Want-Digest`（未采用「单列请求头分类」方案——那会改变工具语义、与页面标题/说明不符）；
2. 删除重复的 `ETag`、`Last-Modified` 各一条，保留语法/参数更完整的第一条（`ETag` 保留 `params: "W/ 表示弱验证"`）；
3. 条目总数 65 → 59，分类数保持 14（CORS/内容/校验/缓存各类均有其他条目），分类明细表与图表统计自动随之更新，无需改渲染代码。
4. `scripts/verify_it_calc.js` 新增 4 条强锁：请求头缺席（`RHREQ N=0|`）、零重复（`RHDUP N=0|`）、总数/分类（`RHSTAT total=59 cats=14`）、用户可见搜索行为（搜 `Access-Control-Request` → 共 0 项）。

## 验证证据
- **真机** `scripts/_verify_it_batch190.mjs`（JSDOM）：**22/22**——数据层四请求头清零、零重复、ETag/Last-Modified 各 1 条且保留完整版、总数 59/分类 14、默认渲染 59 张卡片、搜索请求头零命中、搜索唯一响应头各 1 项、状态链（非法词→清空→切分类→回全部）、分类明细表 14 行且各类之和 59、英文态分类走英译。
  **旧源码 8/22**（读 `/tmp/http-response-headers.N459.before.html`）——差分成立。
- **verify 用例级旧源码差分**：修好版 **1525/1525**；临时换入旧源码后 **1521/1525**，4 条新锁全部变红；恢复后文件 MD5 与修好版一致（`60bcdfb2a6a6619c0cde935f4392d35f`）。严禁 `git checkout --` 恢复，全程 `/tmp` 备份往返。
- audit 注入键 **30838**、僵尸 id 0；单文件判别力正确变红 1523/1524，唯一逃生 `it/vector-magnitude` 为既有基线、跳过 1 为既有；英文 i18n 0 残留。

## 备注
- **踩坑**：`rhChart` / `rhTable` 封装在 IIFE 内，不是 window 全局，`w.eval('rhChart()')` 抛 ReferenceError 被 try/catch 吞掉 ⇒ 图表配置捕获不到。改为通过 `dispatchEvent(DOMContentLoaded)` / `toolbox:langchange` 触发 `rhAll()`，再读 `#rhTbody` 明细表 DOM 作为可观测端点，覆盖同一份 `rhAgg()` 统计口径。
- 只本地提交、不 push。
