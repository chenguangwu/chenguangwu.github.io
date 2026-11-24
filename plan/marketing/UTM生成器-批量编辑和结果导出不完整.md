# UTM 生成器：批量输入与导出体验不足

受影响工具：`tools/marketing/utm-builder.html`

## 问题描述
批量行只有 source、medium、campaign，不支持单条中的 term、content；输入用 `change` 更新，编辑时结果在失焦前仍是旧值。批量区“导出明细 CSV”调用通用快照导出，而非页面已有的 `exportBatch()`；因此不能直接得到逐行生成的 UTM 链接清单。

## 解决方案
批量模式支持完整字段、粘贴表格并实时更新，导出逐行参数、有效状态和链接；明确无效行处理并保留 CSV 公式注入防护。验证编辑后不失焦即复制、包含多个渠道及特殊字符的 CSV 往返。
