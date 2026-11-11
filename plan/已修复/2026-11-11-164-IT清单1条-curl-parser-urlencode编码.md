# 第164批 · IT 清单 1 条 · curl-parser `--data-urlencode` 不编码

- 来源：`plan/categories/01-IT开发/it.md` → IT-D37（问题表格行 + 逐页结论摘要已同步更新）
- 修复日期：2026-11-11
- 类型：中风险计算正确性缺陷（与页面自身声明的 percent-encodes 口径矛盾），纯前端逻辑，无文案/口径变更

## 失败点
`tools/it/curl-parser.html` 把 `--data-urlencode` 与普通 `-d/--data` 一样映射到 `kind==='data'` 并原样拼接 body。页面第162行表格自述"`--data-urlencode` percent-encodes"，实际却不编码：`q=a b` → body `q=a b`（应 `q=a%20b`）。

## 根因
选项映射表把 `--data-urlencode` 折叠进通用 data kind，解析时不区分选项名，丢失了 curl 对该选项的编码语义。

## 修复位点
`parse()` 的 `kind==='data'` 分支：当 `name === '--data-urlencode'` 时调用新增的 `urlEncodeData(val)` 编码后再拼 body。辅助函数按 RFC3986（`encodeURIComponent` 再编码 `!'()*`，空格→`%20` 非 `+`）；`key=value` 形态只编码两端、保留 `=` 分隔符，裸值整体编码。普通 `-d/--data-raw` 不受影响。复用页面既有输出，i18n 0 残留。

## 证据
1. **verify 强锁**：`scripts/verify_it_calc.js` 新增 2 条 curl-parser 用例（`--data-urlencode 'q=a b'`→`q=a%20b`；`'name=a&b=c'`→`name=a%26b%3Dc`）。curl-parser 10/10、it 全量 **1492/1492**。
2. **旧源码差分**：换回 `HEAD` 旧源码 → curl-parser 8/10 红（2条新锁全失败）；恢复修好版 → 10/10 绿。判别力成立。
3. **JSDOM 真机**（`scripts/_verify_it_batch164.mjs`）：**10/10 PASS**，覆盖空格/中文/裸值/特殊符编码、`&`/`=` 编码保留分隔符、普通 `-d`/`--data-raw` 不编码回归、多段 `&` 拼接、POST 语义、URL 不被 body 顶替。踩坑：`out.textContent` 拼接后 `<p>` 间无空格，断言改用结构化 JSON 锚点更稳。
4. **判别力**：单文件 1491 已检 / 1490 正确变红 / 逃生 1（既有 `it/vector-magnitude`，无新增）/ 跳过 1。
5. **门禁辅助**：`audit_verify_input_ids.js` 10286 用例僵尸 id=0；`_en_i18n_probe --check it/curl-parser` 残留 0 页。

## 备注
- 本批只改源码 + verify + 清单条目（表格行+摘要）+ 真机脚本 + 本移交档；攒批后统一跑全站门禁。
