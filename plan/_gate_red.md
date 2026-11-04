# 红门禁归集（集成线）

> 规则：红了照推，逐条记录「门禁名 / 页面 slug / 错误摘要 / 归属线」。修完在状态列标记。

## 2026-11-04 · commit `0b75c76762`（CI run 41828144376）

| 门禁 | 页面 slug | 错误摘要 | 归属线 | 状态 |
| --- | --- | --- | --- | --- |
| anti-regression: case discrimination | `agriculture/mulch-coverage` | 逃生项 2 > 基线 0；`expect` 含「0.0%」重叠率，默认态同样输出，回退默认后仍 PASS | 农业线 | 已修（删除静态锚，保留 7.20 / 50.0% / 17.7） |
| anti-regression: case discrimination | `agriculture/greenhouse-rolling-time` | 逃生项；`expect` 含「卷膜通风」，命中页面静态「卷膜通风参考时间表」标题，回退默认后仍 PASS | 农业线 | 已修（改为动态原因串「温度26℃在合理范围，但湿度95%偏高…」） |
| anti-regression: case discrimination | `agriculture/mulch-coverage` / `agriculture/greenhouse-rolling-time`（自动补强块） | 全 42 输入回显型锚，页面新增校验后失效 | 集成线 | 已修（改合法参数 + 派生数值锚：20000 地膜总长 / 12℃ 内外温差） |

### 说明
- 本次 CI 失败在「Run ToolBox quality gates」，部署被跳过（未部署）。
- 本地在干净 HEAD 工作树复现为 1/219 红，红项即上表两个逃生项。
- 农业线本地已同步修正主用例；集成线补齐自动补强块并复核：`agriculture calc 131/131`、判别力 0 逃生。
