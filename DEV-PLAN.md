# DEV-PLAN

## 当前未完成任务

### Analytics-B：补齐可用的站点流量数据

- [进行中] 51.la 当前 AccessKey 可认证，但站点列表为空，真实统计 ID 查询返回 401；待在 51.la 控制台确认 API 应用与统计站点的授权关系后重新抓取。
- [已完成] Microsoft Clarity 聚合导出已生成，结果文件为 `clarity_traffic_export.csv`。
- [已完成] Bing Webmaster 查询与页面统计已生成，结果文件为 `bing_traffic_export.csv`，共 156 条查询、57 条页面记录。
- [已完成] Bing 与 Clarity 已合并为 `analytics_traffic_merged.csv`，每行带有 `source` 和统一分析字段。
- [已完成] 合并数据过滤规则已加入：移除 `evernode/` 页面及当前项目中已不存在的页面。
- [已完成] 51.la Open API 拉取脚本已加入 `scripts/fetch_51la_overview.py`，密钥通过环境变量提供，不写入仓库。
- 百度统计暂不纳入本轮数据源。

## 数据使用边界

- Clarity 只使用聚合统计，不导出会话明细、消息、时间线或可识别个人的数据。
- 51.la 仅保留聚合指标；认证失败或站点未授权时不生成候选数据。
- 站点内容优化需等 51.la 数据可读后，再结合 Clarity 结果确定优先级。
