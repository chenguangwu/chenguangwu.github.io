# 2026-11-11 第202批 · IT-N254 regex 替换页尊重 flags 与 worker count 语义

## 清单项
- **IT-N254**：替换页无视用户 flags，恒补 `g`：与"匹配"页口径不一致、替换数恒为全量（中，确认缺陷）

## 改动
`tools/it/regex.html` 三处：
1. `doReplace()`：`flags: flags.includes('g') ? flags : flags+'g'` → `flags: flags`，尊重用户 flags（不勾 g 只替首个）。
2. `copyMatches()`：`flags` 去掉补 g，且 `global:true` → `global: flags.includes('g')`——**附带修掉一个更严重的隐藏缺陷**：非 g 时若仍传 global:true，worker 的 exec 循环因 lastIndex 不前进会把同一条匹配重复 1001 次（node 复现确认）。
3. Worker 源码 replace 分支：`count` 从 `(text.match(re2)||[]).length`（非全局带捕获组时会把捕获组计入，`(\d)`→2、`(a)(b)`→3）改为——全局用 `match().length`，非全局用 `new RegExp(...).test()?1:0`，与实际替换数一致。

## 验证证据
- **真机** `scripts/_verify_it_batch202.mjs`（JSDOM，抽取页面真实 worker 源码用 new Function 执行）：**14/14**——worker 层 replace count 四组（非g无分组/1分组/2分组/全局）、test global 两组（非g 1条/g 2条）；页面层捕获 payload 确认 doReplace/copyMatches 不再补 g、global 跟随 flags、替换结果 aXb2/count=1、复制只 1 条、g 模式回归全替 aXbX/count=2。
- **旧源码真机差分**：换入 HEAD 旧页后 **6/14**（8 项变红：count 捕获组 2 项、doReplace 补 g/结果/count 3 项、copyMatches 补 g/global 2 项、复制 2 条 1 项），恢复 MD5 一致（`de3c694738bbffa727f1c663e1f5d066`）。`/tmp` 备份往返，未用 `git checkout --`。
- verify 全集 **1554/1554**（`it/regex` 无 verify 用例，页面依赖原生 location.hash 不适用 harness stub DOM，同第200–201批；判别力由 JSDOM 真机承担）。

## 备注
- **踩坑（记死）**：真机脚本里 pattern 的 HTML 默认值是 `\\d+`（字面两反斜杠，匹配反斜杠+d+ 而非数字），测数字替换必须先显式设 `pattern='\\d'`（JS 串写 `'\\d'`），否则无匹配导致假失败。worker 回调用 setTimeout(0)，断言前留足等待。
- regex 页覆盖行已追加 N254 销账说明（与 N252/N253 同页归并）。
- 只本地提交、不 push。本批第202批，攒批 201–205 第2批。
