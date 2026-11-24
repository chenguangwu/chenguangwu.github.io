# SWIFT/BIC：说明机构范围及核验边界

- **受影响工具路径**：`tools/finance/swift-bic-validator.html`
- **问题**：页面将 BIC 的前四位一律称作“银行代码”，FAQ 也将 BIC 写作 Bank Identifier Code，容易让用户认为该编码仅适用于银行；本地只做字符与国家代码检查，未验证机构注册或汇款能力。
- **解决方案**：将术语统一为机构代码及 Business Identifier Code，说明 BIC 也可标识非银行机构；在结果附近明确仅检查格式、不能确认注册状态或可收款，并同步中英文及结构化 FAQ。
