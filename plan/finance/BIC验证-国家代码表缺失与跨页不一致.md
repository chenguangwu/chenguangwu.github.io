# BIC 验证：国家代码离线表与查询页不一致

- **受影响工具路径**：`tools/finance/bic-validator.html`、`tools/finance/swift-bic-validator.html`、`tools/finance/bic-lookup.html`
- **问题**：两个验证页的国家代码数组缺少 `AS`，而 BIC 查询页包含该 ISO 国家/地区代码；其余字符符合规则的 `AS` 输入会在不同页面得到相反国家码结论。离线数组也未标明来源和版本。
- **解决方案**：核对 BIC 国家代码适用范围与权威代码表，统一维护版本化数据；对未收录项区分数据缺失与明确无效，加入跨页面一致性与边界用例。
