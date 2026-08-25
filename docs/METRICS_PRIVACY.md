# ToolBox 匿名使用指标与隐私说明（B5-10）

> 本文档说明 ToolBox 的隐私优先指标采集机制：事件字典、采样/保留策略、默认关闭原则，以及如何查看与清空本地数据。

## 1. 设计原则

1. **纯前端、无后端**：ToolBox 没有任何服务器，所有功能在浏览器本地运行。
2. **默认关闭（opt-in）**：匿名使用指标默认**不采集**。只有用户在「🗂️ 管理本地数据」弹窗中显式开启后才会记录。
3. **绝不向第三方发送**：指标数据仅写入浏览器 `localStorage`，**不发起任何网络请求**，不会上传到任何服务器（包括分析平台、广告或 CDN）。
4. **只记匿名聚合字段**：仅记录事件类型、工具文件名、行业、AI 模型名、成功/失败布尔值。
5. **禁止记录个人数据**：**不记录**用户输入内容、URL 查询参数内容、上传文件内容、IP、设备指纹或个人标识。
6. **可被用户完全控制**：用户可随时关闭、清空本地指标，也可一键清空全部本地数据（收藏/历史/周报/工具链/AI 配额/主题/语言均一并清除）。

## 2. 指标事件字典

| 事件类型 | 中文说明 | 记录字段 |
|----------|----------|----------|
| `tool_launch` | 打开一个工具页 | `tool`（文件名）、`industry`（行业） |
| `tool_complete` | 工具完成计算/产出 | `tool`、`industry` |
| `copy` | 点击「复制结果」 | `tool`、`industry` |
| `download` | 下载文件 | `tool`、`industry` |
| `guide_click` | 点击「使用指南」 | `tool` |
| `chain_complete` | 完成一条工具链 | `tool` |
| `ai_model_success` | AI 模型推理成功 | `model`（模型名） |
| `ai_model_failure` | AI 模型推理失败 | `model`（模型名） |

> 字段语义：`tool` 为工具 HTML 文件名（如 `bmi-calculator.html`），`industry` 为目录名（如 `health`），`model` 为 Hugging Face 模型标识（如 `Xenova/whisper-base`）。以上均为**工具元数据**，不含任何用户输入。

## 3. 采样与保留策略

| 参数 | 值 | 说明 |
|------|----|----|
| 开关 | `toolbox_metrics_optin` | 值为 `'1'` 时开启，默认不存在（关闭） |
| 事件存储 | `toolbox_metrics_events` | 本地事件环形缓冲（JSON 数组） |
| 采样上限 | `MAX_EVENTS = 500` | 超出后仅保留最近 500 条 |
| 保留天数 | `RETENTION_DAYS = 30` | 超过 30 天的事件在写入时自动裁剪 |

## 4. 如何查看与清空

- **开启/关闭**：首页或工具页底部点击「🗂️ 管理本地数据」→「📊 匿名使用指标（可选）」→ 点击切换开关。
- **查看汇总**：同一弹窗内显示本机累计事件数与各事件计数。
- **清空指标**：弹窗内「清空指标数据」按钮（仅删指标，不影响收藏/历史等）。
- **导出全部本地数据**：弹窗内「导出备份」下载 `toolbox-local-data.json`（用户自检用）。
- **清空全部本地数据**：弹窗内「清空全部本地数据」（含收藏、历史、周报、工具链、AI 配额、主题、语言）。

## 5. 代码位置

- 采集器：`js/metrics.js`（`window.ToolBox.Metrics`）
- 弹窗与开关：`js/privacy.js`（`ToolBox.Privacy.open`）
- 事件埋点：`js/common.js`（tool_launch / copy / download / guide_click / chain_complete）、`js/ai-core.js`（ai_model_success / ai_model_failure）

## 6. 与发布看板的关系

维护者可在本地运行 `python3 _release_dashboard.py` 生成 `release_dashboard.html`——它聚合**构建、静态测试、性能、收录、内容增长**等快照，用于发布前质量核对。该看板**只读已有快照文件，不触发任何网络请求，也不依赖用户指标数据**；看板异常仅告警、绝不阻塞纯前端工具使用。
