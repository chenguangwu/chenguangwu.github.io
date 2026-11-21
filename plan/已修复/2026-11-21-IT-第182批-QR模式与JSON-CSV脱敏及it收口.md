# 第 182 批（IT）QR 编码模式 / JSON-CSV 历史脱敏 / it.md 收口

## 修复项

1. `tools/it/qrcode.html`
   - `qr.addData(text)` 未传 mode，库默认 Byte，纯数字/大写字母也被抬到更高版本。改为按内容选择 `Numeric` / `Alphanumeric` / `Byte`，与页面「自动选最短模式」说明一致。
2. `tools/it/json-to-csv.html`
   - 历史快照原把 `#input`（JSON）与 `#output`（CSV）原文写入 localStorage。改为只保留「输入长度 / 输出长度」，历史结果列写「（结果未存储）」。

## 任务文件收口

- `plan/categories/01-IT开发/it.md` 顶部已标明「2026-11-21 全量收口核验：本文件所列问题已处理完毕」，且文件内 AA/AB/AC 各问题表均已在本轮及此前批次修复（EAN G 表、QR 模式、静区、SHA-224、RC4、YAML、JSON、Text diff、PDF 合并、签名检查等）。按「文件内问题全部修完才删除」规则，本批删除该任务文件。

## 验证

- `verify_it_calc.js it/qrcode` 3/3、`it/json-to-csv` 6/6 通过。
- `node scripts/check_inline_js_syntax.js` 0 错误；`python3 _build.py` 成功，QR 模式与历史脱敏构建后存活。
