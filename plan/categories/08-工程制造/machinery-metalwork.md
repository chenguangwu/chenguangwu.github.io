# 机械/金属加工 · tools/{machinery,metalwork,welding,manufacturing}（~160 页）

## 已知问题### M3. gongyeshebeigonglvpipei 死代码与误导注释
- ✅ 死变量清理（2026-10-26）：torque/loadTorque 两行死变量与注释已删，grep 确认无引用；顺带修该页 #res EN 存量泄漏（calc 动态串 10 处全 __T 化 + location fallback，NO_MODULE 是容器名 #res 非默认所致，--container=res 后 OK_EN）。

## 功能缺陷
- metalwork 7 个「双段通用对比页」功能单薄（carbon-8/diandonggongju-xifen/laxue-ladao/tangxue/wushua/yuanlingongju-xifen/zhineng-duogongneng）：生效 calc 仍是 A/B 两值通用比值-差值输出，非领域公式（carbon-8 第二段有 850-950℃ 渗碳拟合为例外）；建议按主题补真实领域计算（渗碳层深-时间、拉削力-齿升、镗杆刚度等）。
- 切削页缺「材料-刀具匹配表」（45 号钢/不锈钢/铝 的 Vc/Ff 参考静态表）。
- 折弯页缺「回弹补偿」输入项。

## 优化点
- S7 引据：GB/ISO 标准号徽标（本类可信度关键）。→ 已落地 12 页（2026-10-27 批31）：machinery/bearing-1 + estimate-lifespan-bearing + bearing-load + bolt-preload + calc-gear-1 + calc-64 + calc-strength + drive-2、welding/weld-strength + calc-weld + temp-time-6 + detector-25（ISO 281/GB/T 6391、GB/T 3098.1/VDI 2230、GB/T 1357、GB/T 1800.1/ISO 286-1、GB 50017、IIW 碳当量、NB/T 47013）；machinery/metalwork 其余页待续批。
- S3 分步：齿轮/皮带选型链路图（已注入部分 chart，推广 S3 明细）。

## 受影响范围
- tools/machinery/（78）、tools/metalwork/（42）、tools/welding/、tools/manufacturing/

## 进度
- 🔴 待开发
