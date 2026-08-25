# ToolBox 稀疏行业决策报告

> 任务：N1-03
> 盘点时间：2026-08-20
> 数据来源：`json/tools.json`
> 本报告只做决策，不移动页面、不修改 URL、不修改行业 meta、不手工修改构建产物。

## 1. 盘点结论

当前共有 31 个工具数不超过 2 的行业。稀疏不等于应当删除：其中一部分具有明确的专业搜索意图，另一部分只是与已有大行业重叠，少数行业值得等待后续补充工具。

| 决策 | 数量 | 处理原则 |
|---|---:|---|
| `KEEP` | 10 | 保持独立行业，后续只补充真实专业工具 |
| `MERGE-LATER` | 13 | 先保留现有 URL，待 i18n 和 SEO 路由稳定后另立迁移任务 |
| `EXPAND-LATER` | 8 | 保持独立行业，先建立候选池，不立即生成页面 |

本报告不执行行业合并。任何合并都必须另立任务，重新评估旧 URL、跳转桩、行业索引、指南映射和 i18n 路由。

## 2. 判定规则

- `KEEP`：行业名称对应独立专业场景，现有工具即使只有 1-2 个也有明确入口价值，且不应被通用行业名称吞并。
- `MERGE-LATER`：现有工具的主要意图与成熟行业高度重合，当前独立目录会制造导航碎片；暂不直接迁移，先保留 URL。
- `EXPAND-LATER`：行业语义独立，且有至少 3 个可以纯前端实现、可测试、非占位的自然候选；候选需进入 `PLAN-TOOLS.md` 后才能开发。

## 3. 详细决策

| 行业 | 工具数 | 当前工具 | 决策 | 后续建议 |
|---|---:|---|---|---|
| `auto-beauty` | 2 | 镀晶/打蜡周期；雨刷更换周期 | `KEEP` | 维持汽车美容专业入口；后续可补轮胎、保养和美容周期类本地计算 |
| `beneficiation` | 1 | 尾矿品位/流失/利用分析 | `KEEP` | 保持选矿专业入口；候选应围绕品位、回收率和物料平衡 |
| `brand` | 1 | 品牌资产评估 | `EXPAND-LATER` | 可补品牌估值、品牌健康度、渠道一致性等确定性评估工具 |
| `building-material` | 2 | 建材成本利润；建材质量检测 | `MERGE-LATER` | 评估并入 `construction` 或 `materials`，迁移前需确认行业导航和旧 URL |
| `cable` | 2 | 电缆价格分析；电缆安装测试 | `MERGE-LATER` | 评估并入 `electrical` 或 `energy`，保留电缆专业关键词 |
| `casting` | 2 | 铸造缺陷分析；无损探伤 | `KEEP` | 铸造与缺陷/探伤有明确专业意图，可继续保留独立目录 |
| `cnc` | 2 | CAM 后处理转换；尺寸检测反馈 | `KEEP` | CNC 属独立制造工作流，后续可补刀具、进给和加工参数计算 |
| `cosmetics` | 1 | 化妆品注册备案评估 | `EXPAND-LATER` | 可补配方合规、成分浓度和备案材料清单；需注明非监管结论 |
| `defense` | 2 | 军体评分；弹道评分 | `KEEP` | 专业场景独立；新增内容需审查安全边界和数据来源 |
| `embedded` | 1 | 嵌入式功耗分析 | `MERGE-LATER` | 评估并入 `electronics` 或 `it`，保留嵌入式功耗关键词入口 |
| `event` | 1 | 活动效果评估 | `MERGE-LATER` | 评估并入 `marketing` 或 `biz`，避免与营销分析入口重复 |
| `express` | 1 | 快递品控流程 | `MERGE-LATER` | 评估并入 `logistics`，保留快递服务和处理量相关关键词 |
| `furniture` | 1 | 家具质量检测 | `EXPAND-LATER` | 可补板材用量、家具尺寸、承重和成本估算工具 |
| `interior` | 1 | 装修材料环保控制 | `MERGE-LATER` | 评估并入 `construction`、`home` 或 `environment`，需要专业边界确认 |
| `knowledge` | 1 | 企业知识管理成熟度评估 | `EXPAND-LATER` | 可补知识库覆盖率、培训效果和组织成熟度评估 |
| `landscape` | 2 | 景观视线分析；草坪养护周期 | `KEEP` | 园林场景独立；后续可补灌溉、种植密度和养护周期 |
| `livestream` | 2 | 直播复盘；竞品研究 | `EXPAND-LATER` | 可补直播 ROI、留存、转化和排班等本地分析工具 |
| `martial-arts` | 2 | 踢腿柔韧度；抗击打评估 | `KEEP` | 武术训练场景独立；健康风险提示必须保留 |
| `outdoor` | 1 | 攀岩挂片间距与受力 | `KEEP` | 户外安全计算有独立搜索意图；新增工具需明确安全免责声明 |
| `paint` | 1 | 涂料质量环保检测 | `MERGE-LATER` | 评估并入 `chemical`、`construction` 或 `surface` |
| `pharmacy` | 2 | 药房成本分析；GSP 质量管理 | `EXPAND-LATER` | 可补库存周转、有效期和采购成本工具；不得替代监管判断 |
| `security-guard` | 2 | 保安服务质量；风险排查 | `MERGE-LATER` | 评估并入 `security` 或 `safety`，保留安保服务语义 |
| `sports-event` | 2 | 赛事成绩统计；满意度评估 | `EXPAND-LATER` | 可补赛程、积分、排名和证书数据生成工具 |
| `steel` | 2 | 钢材价格；钢结构焊缝计算 | `MERGE-LATER` | 评估并入 `metalwork`、`structural` 或 `construction` |
| `stone` | 1 | 石材色差/强度检测 | `MERGE-LATER` | 评估并入 `building-material` 或 `materials`，暂不改变现有 URL |
| `supplychain` | 1 | 供应链 KPI | `MERGE-LATER` | 评估并入 `logistics` 或 `biz`，保留供应链 KPI 搜索别名 |
| `surface` | 2 | 涂层检测；盐雾评估 | `KEEP` | 表面工程检测场景独立；可补厚度、硬度和附着力计算 |
| `timber` | 2 | 木材价格；木材质量检测 | `MERGE-LATER` | 评估并入 `forestry` 或 `woodworking`，迁移前需做 URL 兼容设计 |
| `warehouse` | 2 | 仓储盘点；仓储财务 | `MERGE-LATER` | 评估并入 `logistics` 或 `biz`，拆分库存与财务搜索意图 |
| `water` | 2 | 管径计算；节水评估 | `KEEP` | 水务工程和节水有独立专业入口，可补流量、泵和水效工具 |
| `yoga` | 2 | 会员留存；课程质量评估 | `EXPAND-LATER` | 可补瑜伽排课、训练计划和会员指标分析 |

## 4. `EXPAND-LATER` 候选池建议

以下只是后续候选方向，不代表已批准开发。真正开发前必须写入 `PLAN-TOOLS.md` 并完成四层重复检查。

| 行业 | 候选方向 |
|---|---|
| `brand` | 品牌健康度评分、品牌一致性检查、品牌资产增长率 |
| `cosmetics` | 成分浓度换算、备案资料清单、配方风险提示 |
| `furniture` | 板材用量、家具承重、尺寸与成本估算 |
| `knowledge` | 知识库覆盖率、培训完成率、知识管理成熟度 |
| `livestream` | 直播 ROI、留存率、转化漏斗 |
| `pharmacy` | 库存周转、有效期预警、采购成本分析 |
| `sports-event` | 赛事积分、排名、赛程和证书生成 |
| `yoga` | 排课、训练计划、会员留存指标 |

## 5. 后续实施边界

1. `MERGE-LATER` 不得直接移动目录或修改 `meta toolbox industry`。
2. 行业迁移必须单独提供旧 URL、目标 URL、跳转策略、sitemap 变化和 i18n 路由影响清单。
3. `EXPAND-LATER` 不得为了凑行业数量开发静态假结果或简单记录本。
4. 健康、法律、金融、军事和安全相关工具必须记录数据来源、适用范围和免责声明。
5. 新工具仍须遵守纯前端约束，不能接入实时数据、后端数据库或外部业务 API。
6. 本报告完成后，后续开发从 `N1-01`、`N1-02` 或 `N2-01` 中按负责人选择，不自动启动合并或扩展。
