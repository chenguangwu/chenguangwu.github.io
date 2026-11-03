# 机械/金属加工 · tools/{machinery,metalwork,welding,manufacturing}（~160 页）

## 已知问题### M3. gongyeshebeigonglvpipei 死代码与误导注释
- ✅ 死变量清理（2026-10-26）：torque/loadTorque 两行死变量与注释已删，grep 确认无引用；顺带修该页 #res EN 存量泄漏（calc 动态串 10 处全 __T 化 + location fallback，NO_MODULE 是容器名 #res 非默认所致，--container=res 后 OK_EN）。

## 功能缺陷
- metalwork 7 个「双段通用对比页」功能单薄（carbon-8/diandonggongju-xifen/laxue-ladao/tangxue/wushua/yuanlingongju-xifen/zhineng-duogongneng）：生效 calc 仍是 A/B 两值通用比值-差值输出，非领域公式（carbon-8 第二段有 850-950℃ 渗碳拟合为例外）；建议按主题补真实领域计算（渗碳层深-时间、拉削力-齿升、镗杆刚度等）。
- ✅ 切削页「材料-刀具匹配表」已具备（2026-10-30 复核）：`mechanical/cutting-speed.html` 的 `#refList` 已渲染 碳钢/合金钢/铸铁/铝合金/不锈钢 × 高速钢/硬质合金 的速度区间矩阵，deep-dive 亦列同口径推荐区间；该项销案（`machinery/speed-cutting-feed` 为跳转存根）。
- 折弯页缺「回弹补偿」输入项。

## 优化点
- S7 引据：GB/ISO 标准号徽标（本类可信度关键）。→ 已落地 12 页（2026-10-27 批31）：machinery/bearing-1 + estimate-lifespan-bearing + bearing-load + bolt-preload + calc-gear-1 + calc-64 + calc-strength + drive-2、welding/weld-strength + calc-weld + temp-time-6 + detector-25（ISO 281/GB/T 6391、GB/T 3098.1/VDI 2230、GB/T 1357、GB/T 1800.1/ISO 286-1、GB 50017、IIW 碳当量、NB/T 47013）；累计 24 页（批31+32）：批32 加 shaft-torsion/tolerance(-1)/thread-4/torque/strength-34/strength-6/tanhuangsheji + metalwork/surface-finish + assessor-34 + analysis-39 + calc-pressure-mold；两目录其余页待续批。
- S3 分步：齿轮/皮带选型链路图（已注入部分 chart，推广 S3 明细）。

## 受影响范围
- tools/machinery/（78）、tools/metalwork/（42）、tools/welding/、tools/manufacturing/

## 进度
- 🔴 待开发

## 2026-11-03 审计补充

### 线膨胀计算错误时明细/图表可能保留旧值（高，确认源码缺陷）
- 问题：清空原长后主结果显示错误，但附属数据表、图表计算分支提前退出不清理旧图表或明细，CSV 仍指向原表。
- 证据：`tools/engineering/thermal-expansion.html:220-224,238-251,258-261,270-274,316-319`；主函数错误退出后包装函数继续运行，extras 对空值直接 return，导出读取 `#thermal_expansionTable`。仅静态核查，图表初次绘制及点击导出需浏览器复验。
- 影响：`tools/engineering/thermal-expansion.html`；错误输入下旧工程数据可能被误认为当前输出。
- 方案：统一校验并同时清空/禁用结果、明细、图表及导出，恢复合法值时一并更新；增加合法→清空→导出测试。

### 留存优化：材料温度变化对照（低，建议）
- 证据：同页 `:223-230,246-251,264-267` 已提供线膨胀公式、明细和数值预设。
- 影响：同页；方案：预设可标注材料来源与适用温度，并并排展示用户选择的两种材料伸长量；注明线性系数为近似。

### 皮带历史恢复遗漏带轮直径（高，确认源码缺陷）
- 问题与证据：`tools/machinery/pidaizhangjinjisuan.html:212-225,245-252` 用直径计算带速及张力，但历史保存、恢复和复制摘要均缺直径。B 型、500 mm、1450 rpm、5.5 kW、125 mm 时单根约 289.8 N；保存后改为 250 mm 再恢复，仍使用 250 mm，计算约 144.9 N。
- 影响：`tools/machinery/pidaizhangjinjisuan.html`，历史工况无法准确复现，复制结果缺关键输入。
- 方案：保存、恢复并显示节径；旧记录缺字段时提示，增加保存—更改直径—恢复的回归测试。

### 焊接热输入超限及单位示例错误（高，确认源码缺陷）
- 问题与证据：`tools/metalwork/welding-heat.html:132-148,195,245-256` 输入控件标明效率最大 1，但计算只拒绝非正数；180 A、24 V、25 cm/min、η=2 输出 2.074 kJ/mm。页面示例将 4320 J/cm 写成 43.2 kJ/m，正确换算为 432 kJ/m。
- 影响：`tools/metalwork/welding-heat.html`，非法效率仍出具热输入，示例单位错误影响核对。
- 方案：计算时校验 0<η≤1，修正示例并补边界和跨单位测试；保留工艺预设并展示换算明细。

### 覆盖
- 本轮人工及只读子代理核查 `tools/engineering/thermal-expansion.html`、`tools/machinery/pidaizhangjinjisuan.html`、`tools/metalwork/welding-heat.html` 共 3 页；仅源码和算术推导，未做浏览器验证，其余未逐页覆盖。
