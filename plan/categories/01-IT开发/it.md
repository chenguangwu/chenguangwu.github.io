# IT 开发 · tools/it（340 页，全站第一大分类）

## 已知问题
### I1. hash/编码类页深度参差
- 部分页（sha、bcrypt、pbkdf2）仅做单次哈希，缺「加盐/迭代次数/慢哈希耗时对比」这类开发者真正要查的东西。
- 受影响：tools/it/sha.html、bcrypt.html、pbkdf2.html 等
- 方案：补参数化（盐、iterations、并行度）与耗时实测（performance.now 本地跑）。

### I2. 正则/格式化器错误提示原始
- 描述：json/yaml/toml 解析失败直接抛异常串，无行号定位。
- 受影响：tools/it/json-formatter*、yaml-*、toml-*（~20 页）
- 方案：接入带行列定位的轻量 parser（纯前端库锁定版本）或自研错误映射。

### I3. barcode/QR 系列仅静态生成
- 描述：QR 页不支持 logo/纠错级别可视化对比；barcode 页缺导出 SVG/PNG 一键。
- 受影响：tools/it/*qr*、barcode-*（~15 页）
- 方案：QR 加中心 logo 与纠错级别滑杆（前后对比可读性）；barcode 统一导出按钮。

## 功能缺陷
- 时间戳页（timestamp-converter 等）：不支持毫秒/秒自动识别与「当前时间」常驻表。
- IP 计算器：无「粘贴整段 CIDR 批量」模式。

## 优化点（G06 联动）
- S6 输入智能化最佳试点：正则速查（输入样例文本高亮命中组）、cron 页「人类语翻译」双向。
- S3 分步：base64/进制约 30 页加「逐步位运算」可视化。
- 高流量页优先做 S4 分享卡（uuid/password/hash）。

## 受影响范围
- tools/it/（340 页，全站第一大分类）

## 进度
- 🔴 待开发（I1-I3 + 优化点均未动）
