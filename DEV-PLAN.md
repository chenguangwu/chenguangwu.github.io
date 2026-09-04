# DEV-PLAN

## 当前未完成任务

### Analytics-B：补齐可用的站点流量数据
- [阻塞] 51.la URL 级明细接口（`/page/all`、`/visit/detail`）仍返回 `5005`，需在 51.la 控制台为 API 应用开通「页面分析/访问明细」接口权限后，才能提取 URL 并参与合并。当前仅 level-2 签名 `/overview/get` 可用（站点级 UV/PV 概览已存档 `json/analytics_51la_overview.json`），URL 级暂缺。
- 百度统计暂不纳入本轮数据源。

### SEO-D：长期无流量页治理（进行中）
- [进行中] 无流量页候选清单已生成（`json/seo_d_lowtraffic.json`：4320/4983 工具页无流量，按行业 it279/general154/finance94/design88…）；noindex/合并/删除动作按原要求需连续周期数据到位后执行，单期数据不立即治理。
- [保留] 禁止全站批量重写 Description，所有改动先基于页面数据和搜索意图确认。

## 数据使用边界
- Clarity 只使用聚合统计，不导出会话明细、消息、时间线或可识别个人的数据。
- 51.la 仅保留聚合指标；认证失败或站点未授权时不生成候选数据。
- 站点内容优化需等 51.la 数据可读后，再结合 Clarity 结果确定优先级。

## 待续 / 滚动扩面
- Analytics-C 高曝光低点击优化：首批 21 页已重写 Title/Description/H1/首段并补使用指南，Bing 数据仍稀疏（站点爬取爬升期），后续周期数据到位后再滚动扩面。
