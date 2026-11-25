# 第810批：MAC 地址类型、NATO 数字反向，PIN 重试与复制，MSI 过期图

关闭 `plan/it/` 4 项：

- MAC地址生成器-随机地址未约束组播位
- NATO字母表-数字编码无法反向还原
- PIN生成器-重试耗尽仍输出不符合条件的PIN
- MSI条码-输入修改后仍可下载旧图

## MAC 生成器（`tools/it/mac-generator.html`）

- 随机模式首字节改为本地管理单播：`(b & 0xFC) | 0x02`，即 I/G=0、U/L=1，不会再生成组播地址。
- 结果区新增地址类型说明：
  - 随机模式：本地管理单播，可用于 VM/仿真，不是厂商全球地址；
  - OUI 模式：是否全球管理取决于前缀首字节位，未分配 OUI 仅限测试。
- 中英文动态文案；结果行同步挂 `__macLastLines` 供回归探针检查首字节位。

## NATO 字母表（`tools/it/nato-alphabet.html`）

- 新增 `REV_DIGITS`：由 `NATO_DIGITS` 生成反向映射。
- 反向转换先查数字音标，再查字母表；`Zero One Two Tree Fife Niner` 可还原为 `012359`，未知词仍为 `?`。

## PIN 生成器（`tools/it/pin-generator.html`）

- `generate()` 记录 `ok` 标志：只有通过全部条件才输出；50 次重试耗尽则跳过并累计 `failed`。
- 结果区明确提示「有 X 个 PIN 在 50 次尝试内无法满足全部条件，已跳过；成功生成 Y 个」，英文态同步。
- 新增 `pinCopyText()`：优先按 `.pin-row` 逐条取文本并以换行连接，其次用 `__pinLastRows`；不再把块元素 textContent 直接拼成一串。
- 复制提示改用 `ToolBox.showToast`，避免 `alert` 阻塞。

## MSI 条码（`tools/it/barcode-msi.html`）

- 新增 `__msiStale`：
  - 输入 `#data` 的 input、校验模式 `#checkMode` 的 change 触发 `__msiMarkStale()`；
  - 生成成功置 false，失败保持 true；
  - `downloadBarcodePNG()` 在过期或没有画布时拒绝下载，并提示「输入已改变，请重新生成」/「请先生成条形码」。
- 中英文错误提示。

## 验证

- 定向：MAC 3/3、NATO 9/9、PIN 3/3、MSI 6/6。
- 全量 IT：2414/2414。
- Puppeteer 真机：5/5，验证随机 MAC 首字节位、NATO 数字反向、PIN 递增序列耗尽重试不输出违规、PIN 复制 3 行、MSI 输入修改后标记过期。
- 门禁：static 0 失败 0 告警；links 0 死链；assets 0 死链 / 0 lang 缺失 / 0 重复 id；inline marker 通过。
