# 第811批：ITF 校验位、UPC 静区、Sitemap 日期与 Robots 分组

日期：2026-11-25

## 修复内容

### 1. `tools/it/barcode-itf.html`（ITF-14 校验位与输入静默改写）

- 新增编码模式下拉：`itf14`（默认）与 `general`。
- ITF-14：输入 13 位时按 GTIN-14 规则计算并补第 14 位校验位，明确提示补出的数字；输入 14 位时校验第 14 位，错误则拒绝出图；其他长度直接报错。
- 通用 ITF：要求偶数位；奇数位不再静默补前导 0，而是提示用户自行补位。
- 空输入、非数字字符均明确报错且不出图，不再静默剥离字符。
- 默认样例改为合法的 `12345678901231`；新增打印静区、护边与窄条尺寸说明。

### 2. `tools/it/barcode-upc.html`（静区与英文错误）

- 左右静区由 24px / 10px 统一为 30px（模块宽 3px，即 10 模块），满足 UPC-A 每侧至少 9 模块的静区要求。
- 空、非数字、长度错误、校验位错误四类提示增加英文分支；英文态不再显示中文错误。

### 3. `tools/it/sitemap-generator.html`（lastmod 与 URL 校验）

- 新增可选的 `lastmod` 日期输入。留空时输出中省略 `lastmod`，不再虚构当天日期；填写时校验真实 `YYYY-MM-DD` 日期，非法日期拒绝生成。
- 逐行用 `URL` 解析并校验 `http:` / `https:` 协议；非法行列出原始行号与内容，不再静默丢弃。
- 重复 URL 去重并提示条数；跨站 URL 原样保留并提示涉及的不同主机数。
- 结果区新增 `lastmod` 状态说明；“URL 数”统计口径保持兼容。

### 4. `tools/it/robots-txt-generator.html`（额外通配符组）

- 删除开头无条件写入的 `User-agent: *`，只输出用户配置的规则组，组间空行分隔；Sitemap 作为独立指令追加在末尾。
- 完全无规则时才回退为 `User-agent: *` + `Disallow:`。
- 新增预览摘要：组数、预览首条规则、Sitemap 是否独立置于末尾；同一 User-agent 出现在多个组时提示可能被爬虫合并规则。

## 验证

- 定向用例：ITF / UPC / Sitemap / Robots 共 23/23 通过。
- 全量 IT 回归：`node scripts/verify_it_calc.js` 2421/2421 通过。
- 真机 Puppeteer：ITF 13 位补校验位、非数字拒绝、校验位错误拒绝；UPC 左右静区 30px；Sitemap 默认无 lastmod、无效行与重复行、非法日期拒绝；Robots 首条规则为 Googlebot、Sitemap 置于末尾，共 9/9 通过。
- 四项门禁：`_test_static.py` 0 失败 0 告警；`_audit_links.py --check` 0 死链；`_audit_assets.py --check` 0 资产死链 / 0 lang 缺失 / 0 重复 id；`audit_inline_marker_placement.js` 通过。
- 提交前最后一次 `python3 _build.py` 成功。
