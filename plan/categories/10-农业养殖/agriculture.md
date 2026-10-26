# 农业 · tools/agriculture（64 页）

## 已知问题
## 功能缺陷
- 施肥页缺「N-P-K 折纯汇总表」（多肥合计输入）。
- 无「农时日历」（节气↔农事静态模块，SEO 流量入口）。

## 优化点
- ✅ 真缺陷修复（2026-10-26）：crop-yield 穗数法公式量纲错 10 倍（/100/10 多除 10，默认小麦 40×35×45 只算 63kg/亩、相对参考 500 恒判「低产」；正确 = 万穗×粒数×千粒重÷100 = 630kg）；calc 与 saveHistory 两处同修，formula-eq 文案同步改 ÷100，既有 verify 用例 370.8→3708.4 同批更新。
- ✅ S2 场景（2026-10-26）：crop-yield 加 3 预设「水稻测产」（22×120×27→708.7kg/亩）「玉米测产」（0.45×550×350→856.3）「样方实测(小麦)」（2m²/1.8kg→510.0）；verify agriculture 118→122（clicks 后置注入绕过 boot 期 initCrops→applyCrop 重置）；判别器 0 逃生；顺带修 #result EN 存量泄漏（作物名/等级/标签全 __T 化）→ OK_EN；门禁 218/218。
- ✅ 追肥场景（2026-10-26）：fertilizer-calculator 加 4 个追肥预设（小麦返青期/水稻穗肥/玉米大喇叭口期/番茄膨果期，period=top）；顺带修 __tbInputGuard 分母误判（原 needP→ 应为 needN，否则错误拦截『仅追氮肥』needP=0 合法输入）；verify 122→126，判别器 0 逃生。
- ✅ N-P-K 折纯汇总表（2026-10-26）：fertilizer-calculator 新增「折纯汇总」tab，4 行肥料品种下拉 + 施用量(kg)，calcPurity 逐行折纯 N/P₂O₅/K₂O 并合计（例 尿素50kg+过磷酸钙30kg ⇒ N 23.00 / P₂O₅ 4.80 kg）；含重置、导出 CSV；verify 126→127，判别器 0 逃生。

## 受影响范围
- tools/agriculture/（64 页）

## 进度
- 🟡 续批中（测产真 bug 已修 + S2/追肥/折纯表已落地；剩余：农时日历）
