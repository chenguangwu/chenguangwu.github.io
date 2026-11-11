# 2026-11-11 第219批 · IT-N178~N180 http-cookies（1 条补证据 + 2 条真修 + 全站同类扩散修复）

## 清单项
- **IT-N178**（中）：英文简介宣称 "Parse and build ... headers"，页面只有静态速查
- **IT-N179**（中）：`Expires=Wed, 21 Oct 2025 ...` 星期与日期不符且已过期
- **IT-N180**（低）：`Max-Age` ≤0 即删除未说明，中文界面表头固定英文

## 进批探测
清单行号已偏移（`:169`/`:280`/`:658` → 实际 `:158`/`:269`/`:647`）。真机 + 静态检查结论：
- N178 **已修**：英文简介已是 "Cookie attributes (...) and JavaScript APIs, as a searchable quick reference."，中文 `data-zh` 为「Cookie 属性…和 JS 操作方法」，与页面仅有 `searchInput` + 静态 COMMANDS 的能力一致；全页无解析/构建控件 → 漏销账，本批补证据。
- N179 **仍在**：`Wed, 21 Oct 2025 07:28:00 GMT`，实算 `new Date('2025-10-21T07:28:00Z').toUTCString()` = `Tue, 21 Oct 2025`（周二），且相对 2026-11 已过期。
- N180 **仍在**：`Max-Age` desc 仅「存活秒数（相对，优先于 Expires）」、params「正数/0/负数」无删除语义；`__ckTable()` 的 `th1.textContent='Attribute'` 无条件英文。

## 改动
1. **N179 全站同类扩散修复**：清单只点了 http-cookies 1 处，grep 发现同一错误串在 4 个 HTTP 页共 **11 处**（http-cookies 1 / http-headers 2 / http-response-headers 3 / http-cache 5），统一替换为 `Thu, 21 Oct 2027 07:28:00 GMT`——实算周四、相对当前未过期。`example` 是页内 `COMMANDS` 静态数据，en JSON 与 verify 均不引用（已 grep 确认），无需三源同步。
   - **刻意保留**星期正确的历史示例：`Thu, 01 Jan 1970 00:00:00 GMT`（JS 删除 Cookie 的标准写法，1970-01-01 确为周四）、`Wed, 21 Oct 2015`（RFC 6265 原文，条件请求示例）、`Wed, 21 Oct 2026`（实算周三）。这些是过去时间点但语义正确，不是缺陷。
2. **N180 Max-Age 语义**：desc 改「存活秒数（相对，优先于 Expires）；设为 0 或负数立即删除该 Cookie」、params 改「正数存活/0 或负数删除」；`i18n/tools/en/it/http-cookies.json` 的中文 key 与英译同步（含 `delete the cookie immediately` / `Positive = lifetime / 0 or negative = delete`）。
3. **N180 表头双语**：`var th1=...; if(th1) th1.textContent=en?'Attribute':'属性';`。

## 验证证据
- **真机** `scripts/_verify_it_batch219.mjs`：**19/19**——N178 简介口径 + 无解析器控件（4 项）；N179 四页 2025 错误串清零、所有 HTTP-date 星期与 `new Date().toUTCString()` 实算一致（含保留的 1970/2015/2026）、替换值周四且未过期（7 项）；N180 Max-Age 中英删除语义、中文态表头 `["#","属性","分类","说明"]`、英文态 `["#","Attribute","Category","Description"]`（7 项）。
- **旧源码差分**：5 个文件（4 页 + en JSON）一起 `git show HEAD` 还原 → **9/19**（10 项红）；从 `/tmp/bk219/` 逐个恢复，5 个 MD5 全部 `OK` → 19/19。
- verify 全集 **1554/1554**（该页 2 例只锚「共 0 项」过滤计数，与日期/表头/简介无关）；判别单检基线不变；`audit_deepdive_source_sync.py --check` **不一致 0 页**；`git diff --check` 干净。

## 备注
- **铁律复验**：清单「确认源码缺陷」仍可能是漏销账（N178）；而清单只点 1 处的缺陷往往已扩散（N179 实际 11 处），修一处必须 grep 全站同类。
- **判据收窄的价值**：初版脚本要求「所有示例日期未过期」会误伤 `Thu, 01 Jan 1970`（删 Cookie 标准写法）与 RFC 2015 原文；正确判据是「星期与实算一致 + 2025 错误串清零 + 替换值未过期」，不把刻意的过去时间点当缺陷。
- **踩坑**：`__ckTable()` 在 IIFE 内不可外部调用，需派发 `toolbox:langchange` 事件触发；`### IT-N18` 前缀会误匹配 N180 自身，删清单段要用精确 `### IT-N181 ` 作终点。
- 清单 3 段 + 留存建议行删除、补覆盖行，开头待办改指 IT-N181–N182。
- 只本地提交、不 push。攒批 217–221 第3批（本批未单独 build；改了 4 页静态数据 + en JSON，攒满后统一跑门禁，届时 `sw.js` 若刷新再补 chore）。
