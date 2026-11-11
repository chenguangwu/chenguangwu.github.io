# 2026-11-11 第198批 · IT-N246/N247/N248 binary-to-text 严格解码 / 历史评分 / FAQ 口径修正

## 清单项
- **IT-N246**：历史/数据表/图表与 CSV 全恒空——结果写进 textarea 的 `value`，历史读 `textContent`，且以错误词判空（中，确认缺陷）
- **IT-N247**：非法 UTF-8 被静默换成 U+FFFD、首部 BOM 被吞，无 Latin-1/hex 兜底（中，确认缺陷）
- **IT-N248**：FAQ 两处说明与实现相反（空格"无法还原"、尾位"会被丢弃"）（低，确认缺陷）

## 改动
`tools/it/binary-to-text.html`：

**N246**：`__binary_to_textResText()` 的 textarea `.value` 读取由前一 Agent 已修好；本批删除遗留的 `__binary_to_textScore()` 错误词启发式（旧版以 `/错误|Error|Failed|Invalid/` 判 0，会把解码出的正常文本如"页面显示：错误"/"Error 404"误判为无效历史，使有效性趋势图假性掉零）——非法输入已在 `convert()` 里 `alert` 拦下，进入历史的都是有效产物，故恒返回 1。

**N247**：`convert()` 改为严格解码 `new TextDecoder('utf-8',{fatal:true,ignoreBOM:true}).decode(bytes)`；catch 分支逐字节流式喂入统计非法字节数、给 Latin-1 对照串与 `0x..` 十六进制字节列表（中英双语）。合法 UTF-8 与 BOM 保留不再被吞。

**N248**：FAQ「位串里有空格或换行能解吗？」改写为"分隔符仅排版、文本空格由字节 00100000 正常还原、长度非 8 倍数直接报错并中止不丢尾位"；formula-eq 同步严格 UTF-8 / fatal / ignoreBOM / Latin-1 / 字节列表说明。

三源同步：`i18n/tools/en/it/binary-to-text.json`（FAQ 中文键+英译、formula-eq 中文键+英译）、`i18n/tools/content_deepdive.json`（deep-dive FAQ 两条）。

`scripts/verify_it_calc.js` 新增 3 条探针强锁（用例 1548→1551）：
- `B2TBAD OK`：注入 `11111111 01000001`，断言输出含非法 UTF-8 告警 + Latin-1 + `0xFF`
- `B2TBOM OK`：注入 `EF BB BF 41`，断言 BOM 未被吞（U+FEFF / 0xEF）
- `B2TSCORE OK`：探针传 `'页面显示：错误'` 断言 `__binary_to_textScore === 1`（旧启发式判 0 ⇒ 红）

## 验证证据
- **真机** `scripts/_verify_it_batch198.mjs`（JSDOM）：**21/21**——合法 UTF-8 "Hi"、空格字节 `00100000`→"A B"、非法 UTF-8 五项（告警/Latin-1/0xFF/计数/ÿA）、BOM 保留 U+FEFF、错误词评分=1（含 Error 404）、历史链写入 `__tbScore=1`、FAQ/formula 页面文案、en JSON + deep-dive 三源一致、非 8 倍数 alert 中止。
- **旧源码真机差分**：换入 HEAD 旧版三文件后 **6/21**（15 项变红，覆盖非法字节 5 项 + BOM + 中文错误词评分 + 含错误词记录 verdict + FAQ/formula/en/deep-dive 口径；"Error 404" 与合法解码仍绿，符合旧启发式只命中中文错误词的预期）；恢复后三文件 MD5 与修好版一致（`3d3c50029c5050626ff350f9b2b91003` / `0a13475a5be735d7f1b58cf099b3d382` / `3790d3430e81c1311b3f76aaa02fe5eb`）。全程 `/tmp` 备份往返，未用 `git checkout --`。
- verify 全集 **1551/1551**；audit 注入键 **30857**、用例 10347、僵尸 id 0、缺页 0；单文件判别力正确变红 1549/1550，唯一逃生 `it/vector-magnitude` 为既有基线、跳过 1 为既有；i18n check/roundtrip 0。

## 备注
- **踩坑（记死）**：en JSON 是「中文键→英译值」映射，真机 collect 须同时收 key 与 value；英译用 "reports an error and stops" 表达"直接报错并中止"，正则断言要覆盖该译法，不能只匹配中文或 `abort`。
- harness stub DOM 的 `document.body.textContent` 不含完整静态 FAQ，故本批 FAQ 锁不放 verify（会默认态逃逸），改由 JSDOM 真机 + 三源一致性检查承担，与第197批静态数据同理。
- 历史包装形态：`TBKit.history.list()` 返回 `{t,d}`，`last()` 返回裸 `d`，真机 stub 已按此构造。
- 只本地提交、不 push。攒批：196–198 已 3 批，攒满 5 批（196–200）再跑全站判别力 + 完整门禁。
