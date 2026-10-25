# 机械/金属加工 · tools/{machinery,metalwork,welding,manufacturing}（~160 页）

## 已知问题### M3. gongyeshebeigonglvpipei 死代码与误导注释
- 描述：`var torque=F*v/(2π*1500/60)*0; // placeholder` 后紧跟重算的 loadTorque（未用于输出），残留 `*0` 占位与 "actually" 注释，易误导后续维护。
- 方案：删除两行死变量与注释。
- 受影响：tools/machinery/gongyeshebeigonglvpipei.html
- 置信度：低（不影响输出）

## 功能缺陷
- metalwork 7 个「双段通用对比页」功能单薄（carbon-8/diandonggongju-xifen/laxue-ladao/tangxue/wushua/yuanlingongju-xifen/zhineng-duogongneng）：生效 calc 仍是 A/B 两值通用比值-差值输出，非领域公式（carbon-8 第二段有 850-950℃ 渗碳拟合为例外）；建议按主题补真实领域计算（渗碳层深-时间、拉削力-齿升、镗杆刚度等）。
- 切削页缺「材料-刀具匹配表」（45 号钢/不锈钢/铝 的 Vc/Ff 参考静态表）。
- 折弯页缺「回弹补偿」输入项。

## 优化点
- S7 引据：GB/ISO 标准号徽标（本类可信度关键）。
- S3 分步：齿轮/皮带选型链路图（已注入部分 chart，推广 S3 明细）。

## 受影响范围
- tools/machinery/（78）、tools/metalwork/（42）、tools/welding/、tools/manufacturing/

## 进度
- 🔴 待开发
