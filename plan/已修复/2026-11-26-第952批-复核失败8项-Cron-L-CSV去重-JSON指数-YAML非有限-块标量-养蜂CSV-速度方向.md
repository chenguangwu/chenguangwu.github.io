# 第952批：复核失败 8 项修复

日期：2026-11-26

## 修复内容

1. **Cron 末日列表/步长被接受但不匹配**（`tools/it/cron.html`）
   - `L` 仅允许在日期字段单独出现；`L,15`、`L/2` 等与列表/步长组合的写法在校验阶段明确拒绝，并给出中英文原因。
   - 单独 `L` 仍表示月末并放行；预览、描述与匹配语义保持一致。

2. **CSV 转 YAML 重复键**（`tools/it/csv-to-yaml.html`）
   - 自动去重时所有生成后的表头都登记进 `used`，`a,a,a` 稳定得到 `a / a_2 / a_3`。
   - 多余字段按已占用名称集避让：原表头已有 `extra1` 时，第 3 列生成 `extra1_2`，不再覆盖原值。

3. **JSON 格式化极小指数下溢丢失**（`tools/it/json-formatter.html`）
   - `__isRiskyNumber()` 识别指数下溢/次正规数：`1e-400`、`9e-324` 与超安全整数指数写法均走 `JsonNumber` 原样保留。
   - 格式化、压缩、树视图、复制和下载共用同一保精度节点。

4. **JSON 差异指数形式数字丢精度**（`tools/it/json-diff.html`）
   - `jdParse()` 对含指数数字按完整字面量识别溢出、下溢和精度损失；`9007199254740993e0` 与 `9007199254740992e0` 判为不同，`1e-400` 不再变 0。
   - `jdNumKey` 继续把 `1e3` / `1000`、`1.0` / `1` 视为等值写法。

5. **YAML 压缩与转 JSON 静默丢失非有限数**（`tools/it/yaml-formatter.html`）
   - 压缩改用 `jsyaml.dump(..., flowLevel:0)`，输出 `{a: .inf, b: .nan}`，保留类型与值。
   - YAML→JSON 递归检测非有限数与 JSON 不支持类型，明确拒绝并指出路径（如 `root.a (Infinity)`），不再 `JSON.stringify` 成 `null`。

6. **YAML 转 XML 块标量空行缩进丢失**（`tools/it/yaml-to-xml.html`）
   - 块标量改为按原始行收集：保留空行、相对缩进与尾随空行；正确处理 `|`、`|-`、`|+`、`>` 及折叠。
   - `|` 示例输出 `first\n\n  indented\nlast\n`；`|+` 保留全部尾随空行；`>` 空行分段、额外缩进行独立成行。

7. **越冬糖浆导出缺少计划与差额**（`tools/beekeeping/winter-feed-syrup.html`）
   - `calcData()` 统一计算 `planNeed / gapPer / gapTotal`，页面与导出复用同一口径。
   - CSV 新增每日消耗、计划天数、计划期需糖浆、计划期缺口/剩余（每群与合计）；缺口/剩余/持平三态均有对应标签。
   - 旧测试 `1.0 L` 同步为实际格式 `1.00 L`。

8. **速度平方方向与附表不一致**（`tools/kinematics/velocity-squared.html`）
   - `__vsSolve()` 按速度方程求所有非负时间解；同一距离可有两个时刻时同时展示 `+10.000 / -10.000`，不再无条件取正根。
   - 距离按运动方向取有效符号：初速 0、加速度 −1、距离 10 ⇒ t=4.472 s、v=−4.472 m/s。
   - 附表与历史复用主计算结果；不可达或空输入时清空附表，不再出现 NaN 或正根残留。

## 验证

- `node scripts/verify_it_calc.js`：2481/2481
- `node scripts/verify_beekeeping_calc.js`：13/13
- `node scripts/verify_kinematics_calc.js`：70/70
- 七项轻量门禁全过：静态测试 4654 通过 / 0 失败 / 0 警告；死链 0；资产 0；加固标记 0 越界；expect 反模式 0；假门禁 0；输入 id 僵尸 0。
- 真机探针：Cron 三条 `L` 用例得到 `false/false/true`；CSV `a/a_2/a_3` 与 `extra1_2`；JSON 原样保留三个指数数字且 diff 命中 1 处；YAML 压缩保留 `.inf/.nan`、转 JSON 明确拒绝；块标量 `| / |+ / >` 与 js-yaml 语义一致；养蜂 CSV 含计划天数、每日消耗与每群/合计缺口；速度平方正反双分支与零初速负向用例均通过。

## 复核记录处理

复核通过，删除对应 8 个 `plan/复核失败/` 记录；`plan/复核失败` 剩余 10 项。
