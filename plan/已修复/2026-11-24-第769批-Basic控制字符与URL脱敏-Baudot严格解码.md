# 第769批：Basic 认证控制字符与 URL 脱敏、Baudot 严格解码与 ASCII 大写

日期：2026-11-24
范围：`tools/it/basic-auth-generator.html`、`tools/it/baudot-code.html`、`scripts/verify_it_calc.js`、英文第三层字典

## 已修复任务（5）

1. **Basic 认证生成：复制空结果没有反馈**
   - `copyField()` 空结果改为明确中英文提示「请先生成凭证后再复制」，不再调用无参 `i18nText()` 得到空串。
   - 复制成功/回退/失败交由 `ToolBox.copyText(v, __basicL('Copied','已复制'))` 内部反馈，避免重复 toast；异常时兜底「复制失败，请手动选择文本复制」。

2. **Basic 认证生成未拒绝控制字符**
   - 生成前校验用户名与密码中的 `\x00-\x1F`、`\x7F`，命中即清空三项输出并提示中英文错误。
   - 覆盖制表符、换行、DEL；合法 Unicode（中文）仍按 UTF-8 编码并保留 charset 提示。

3. **Basic 认证的凭证 URL 缺少使用限制说明**
   - URL 标为「固定 example.com，含凭据，仅演示」，新增说明：部分客户端拒绝、URL 可能进入历史/日志/代理，优先复制请求头。
   - 新增「显示 URL 示例（含凭据，默认关闭）」开关，默认 `urlOut` 为空，不再默认在屏幕/历史暴露凭据；显式勾选后才生成。
   - 公式说明同步改为「可选、默认关闭」。

4. **Baudot 解码：非法码组被截断或跳过**
   - 二进制严格要求 5 位 `[01]`；十进制只接受数字且 0–31；十六进制只接受 1–2 位 hex。
   - 所有码组先完整校验，任一非法即清空输出、拒绝生成不完整结果，并在 `#baudotError` 与 alert 中报告序号、原文与原因（最多 5 条）。
   - 合法码组（含换档）行为不变。

5. **Baudot 编码前 Unicode 大写转换静默改写字符**
   - 只对 ASCII 小写字母 `a-z` 转大写；ß、é、中文等保持原型查表。
   - 不支持字符明确列出「字符 + U+码位」，写入 `#baudotError` 并 alert；`ß` 不再展开成 `SS` 混入编码。

## 验证

- 定向：`node scripts/verify_it_calc.js it/basic-auth-generator it/baudot-code` → 18/18。
- 全量 IT：`node scripts/verify_it_calc.js` → **2143/2143 通过**。
- Puppeteer 真机 `/tmp/test769.js`：11/11（空复制提示、控制字符拒绝、URL 默认空/勾选生成、非法二进制/十进制报错且输出为空、ß 列出且 A 正常编码、ASCII 小写正常）。
- 英文探针 `?lang=en-US`：两页可见中文 0。
- `python3 _test_static.py`：4654 通过 / 0 失败。
- `_audit_assets.py --check`、`_audit_links.py --check`、`audit_inline_marker_placement.js` 全绿。
- 构建后 `grep` 复查 `f_showUrl`、`baudotError`、严格校验/ASCII 大写说明均存活。
