# 第230批 · IT-N227、IT-N230 ~ IT-N232（申请复核）

- 分类：`tools/it`
- 修复页：`tools/it/rabbit.html`、`tools/it/sms-qr.html`
- 同步源：`i18n/tools/en/it/rabbit.json`、`i18n/tools/en/it/sms-qr.json`、`i18n/tools/content_deepdive.json`
- 验证脚本：`scripts/_verify_it_batch230.mjs`

## 逐条结果

### IT-N227 密文基数靠猜 / 非法 IV 静默全 0（中）
- 修复：`getIV()` 只接受空值或 16 位 hex（8 字节），否则抛双语错误；`hexToBytes()` 先校验纯 hex + 偶数长度，杜绝 `parseInt(NaN)→0`；解密格式严格跟随 `#outputFormat`（Hex 分支不再退回 Base64，Base64 分支捕获 `atob` 失败）；失败态清空旧输出。
- 证据：JSDOM 中非 hex IV、3 字符 IV、Hex 模式 `zzzz` 均报错且输出清空；官方向量密文仍可正常解密。旧源码三种非法输入都显示「解密成功」并产出乱码。

### IT-N230 SMS 页伪随机二维码（高 · 其他 Agent 已修，补证据）
- 进批探测：页面已加载本地 `js/qrcode.js`（Kazuhiko Arase 的 MIT qrcode-generator，56694 字节），`drawQR()` 用 `qrcode(0,'M')` 真实编码，伪随机 LCG 与固定 `N=27` 已删除。
- 证据：JSDOM 注入同源库后，对 `sms:13800138000?body=Hi` 生成 25×25、328 个暗模块；非固定矩阵。旧备份同样通过（如实记录：该项在进批前已修）。

### IT-N231 号码未编码 / `#`、`&`、空格截断（中）
- 修复：`buildSms()` 去除号码中的空格/连字符，严格校验 `^\+?\d{5,15}$`，不合法抛双语错误；正文仍 `encodeURIComponent`。错误提示为统一文案，不回显用户输入。
- 证据：`138 0013-8000 → sms:13800138000?body=Hi`；`+86 139-1234-5678` 保留 `+`；`13800138000#test&x` 报错；正文 `a b&c#中文` 编码为 `%20/%26/%23/%E4%B8%AD%E6%96%87`；`<img ...>` 号码不产生 DOM 节点。

### IT-N232 NaN 守卫吞掉合法短信正文（中）
- 修复：删除 `generate()` 中对结果 HTML 的 `NaN/Infinity` 正则扫描；文本/URI 结果按内容本身渲染。
- 证据：正文 `NaN` 正常输出 `sms:13800138000?body=NaN`，无「计算结果含无效值」；旧源码直接吞掉结果。

## 三源同步
- Rabbit 公式说明补「解密格式跟随下拉、IV 必须 16 hex 或留空」并与 en 映射整键同步。
- SMS 公式说明补号码校验规则；deep-dive 示例由错误的 `smsto:…` 改为 `sms:13800138000?body=Hi`，同步 en 映射与 `content_deepdive.json`。

## 验证结果
- `node scripts/_verify_it_batch230.mjs`：新源码 20/20；同一脚本跑旧源码 4/17（N230 两项旧态已绿，其余 13 项变红）。
- `env -u NODE_OPTIONS node scripts/verify_it_calc.js`：1588/1588（新增 3 条强锁：非法 IV、NaN 正文、`#` 号码；同批改写 sms-qr B 类旧 expect）。
- `env -u NODE_OPTIONS node scripts/discriminate_check.js verify_it_calc.js`：已检 1587、正确变红 1586、逃生 1（`it/vector-magnitude` 基线）、跳过 1。
- 输入 ID audit：10384 用例、缺页 0、僵尸 id 0；deepdive audit：4573 页、0 不一致；`git diff --check` 通过。

## 留待后续
- IT-N228/N229（MySQL 8.0 废弃语法）与 IT-N233–N235 等仍在分类清单，未在本批处理。
- 未跑全站门禁与 `_build.py`（攒批 227–231 后统一执行）；未做真实扫码与跨端验证。
