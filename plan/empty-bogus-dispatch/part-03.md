## `tools/surveying/`（0 页，已全部修复）

> **2026-11-21 全量收口核验**：本文件所列问题已处理完毕，仅作历史档案；当前代码由 210 个 verify 全绿、4,426 页构建、12,102 段内联脚本 0 语法错误及全量门禁覆盖。


## 附：已领取未修好（10 页，不在 230 待分派清单）

| 页面 | 复扫空态文案 | 状态 |
|---|---|---|
| `tools/fishery/salinity-calculator.html` | `⚠️ 四项均需填写有效数值：现有水量须 >0，三个盐度须 ≥0。…` | **扫描误判**：已是提示语，文案含 `>0 / ≥0` 的数字被空态规则误命中，无需修 |
| `tools/mining/convert-grade-ore.html` | `品位需填写 ≥0 的数值（g/t）；矿石量需填写 ≥0 的数值（t）；金属价格需填写 ≥0 的数值（元/g）` | **扫描误判**：已是提示语，数字 `≥0` 被误命中，无需修 |
| `tools/museum/audio-guide-timer.html` | `0秒讲解总时长` | 已有提示「可用时间需大于 0，无法排程」，非缺陷 |

> 结论：10 页已全部处理完毕——**3 页为扫描器数字误判 / 已有提示**（`salinity-calculator`、`convert-grade-ore`、`audio-guide-timer`）、**7 页已修复**（`agri-calculator`、`px-to-rem`、`base32`、`overtime-pay-calc`、`forward-kinematics-2r`、`bearing-from-coordinates`、`hubble-redshift-distance`）。
