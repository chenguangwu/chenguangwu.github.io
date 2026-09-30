#!/usr/bin/env python3
# 手工精译 report5 中所有唯一「标签：」前缀，生成 i18n/tools/en/_prefix.json
# 这些键用于运行时前缀子串替换：文本节点以该键开头时只译前缀，变量值原样保留。
T = {
'还款总额：':'Total repayment:','总利息：':'Total interest:','期限：':'Term:','表达式：':'Expression:',
'净收益：':'Net profit:','年利息收入：':'Annual interest income:','总 ROI：':'Total ROI:',
'税后所得：':'After-tax income:','总收益（利息+本金差）：':'Total return (interest + principal diff):',
'每年利息：':'Annual interest:','原始值：':'Original value:','累计回报率：':'Cumulative return:',
'科学记数法：':'Scientific notation:','相对北京时间（UTC+8）：':'Relative to Beijing time (UTC+8):',
'额定扬程/压力：':'Rated head/pressure:','中文读法：':'Chinese reading:','原模型月供参考：':'Original model monthly payment ref:',
'可用范围：':'Available range:','胜率：':'Win rate:','额定流量：':'Rated flow:','输入值：':'Input value:',
'当前价格：':'Current price:','初始投入：':'Initial investment:','月供：':'Monthly payment:','月供最少：':'Min monthly payment:',
'概率密度 f(x)：':'Probability density f(x):','资产负债率：':'Asset-liability ratio:','工程记数法：':'Engineering notation:',
'搭配解读：':'Matching interpretation:','建议仓位金额：':'Suggested position amount:','历史均值：':'Historical mean:',
'推荐设备类型：':'Recommended device type:','常规表示：':'Conventional notation:','到期收益率 (YTM)：':'Yield to maturity (YTM):',
'期末价值：':'End-of-period value:','搭配色：':'Secondary color:','采购进度：':'Procurement progress:',
'管径 DN200 最大井间距：':'Max well spacing for DN200 pipe:','面值：':'Face value:','质量保障综合评分：':'QA composite score:',
'建议校准周期：':'Recommended calibration interval:','甲醛释放量：':'Formaldehyde emission:',
'距上次校准：':'Time since last calibration:','合规：':'Compliance:','材料类型：':'Material type:','转移：':'Transfer:',
'中文大写：':'Chinese capital numerals:','步骤 1：':'Step 1:','步骤 2：':'Step 2:','步骤 3：':'Step 3:','步骤 4：':'Step 4:',
'选型技术规格：':'Selection specifications:','时间换算：':'Time conversion:','简单年化（不计复利）：':'Simple annualization (no compounding):',
'白平衡设置：':'White balance setting:','各年明细：':'Year-by-year breakdown:','能耗总计：':'Total energy consumption:',
'单位成本已按分摊额 ÷ 产量折算：':'Unit cost converted by allocation / output:',
'校准项目：':'Calibration items:','节省（按原计划对比）：':'Savings (vs original plan):','简介：':'Brief intro:',
'本地时间：':'Local time:','生成 .env 配置：':'Generate .env config:','十进制真值：':'Decimal true value:',
'解码失败：':'Decode failed:','主换行符：':'Primary line break:','偏差额：':'Deviation amount:',
'替代产品/方案推荐：':'Alternative product/solution:','总利息收入：':'Total interest income:','文本行数：':'Text line count:',
'中文说明：':'Chinese note:','设备：':'Device:','带分数：':'Mixed number:','| 故障：':'| Fault:','信用等级：':'Credit rating:',
'约分：':'Fraction reduction:','整改建议：':'Rectification suggestion:','饱和度差：':'Saturation difference:',
'累计盈亏：':'Cumulative P/L:','建议方案：':'Suggested solution:','估算覆盖面积：':'Estimated coverage area:',
'累积概率 P(X≤x)：':'Cumulative probability P(X≤x):','催收策略：':'Collection strategy:','标准小数：':'Standard decimal:',
'实际税率：':'Effective tax rate:','凯利分数：':'Kelly fraction:','建议电机功率：':'Suggested motor power:','判定：':'Determination:',
'贷款本金：':'Loan principal:','购买力缩水：':'Purchasing power loss:','消耗占比图：':'Consumption share chart:',
'需更换部件清单：':'Parts replacement list:','下期预测用量：':'Next-period forecast usage:',
'年化收益率 CAGR：':'Annualized return CAGR:','服务环节：':'Service stage:','苯系物含量：':'BTEX content:',
'英文单词：':'English word:','速算扣除数：':'Quick deduction:','推荐传感器类型：':'Recommended sensor type:',
'保留 4 位有效数字：':'Keep 4 significant figures:','❌ 解析失败：':'❌ Parse failed:',
'（带分数：':'(Mixed number:','未折现净现金流：':'Undiscounted net cash flow:','归一化后权重：':'Normalized weights:',
'应纳税所得额：':'Taxable income:','均值 np：':'Mean np:','评估标准：':'Evaluation criteria:','信用评分：':'Credit score:',
'通分：':'Common denominator:','文本总长度：':'Total text length:','相加：':'Sum:','当期收益率：':'Current yield:',
'国内格式（按位分组）：':'Domestic format (digit grouping):','评级：':'Rating:','第 3 年末：':'End of year 3:',
'管径 DN300 雨水检查井最大间距：':'Max spacing of DN300 rainwater well:',
'第 2 年末：':'End of year 2:','累计应纳税：':'Cumulative taxable:','清洁：':'Cleaning:','润滑：':'Lubrication:',
'生成 5 阶幻方（每行/列/对角线之和 = 65）：':'Generate 5th-order magic square (row/col/diag sum = 65):',
'📏 大圆距离：':'📏 Great-circle distance:','国家/地区代码：':'Country/region code:','流量：':'Flow:',
'内部收益率 IRR：':'Internal rate of return IRR:','本利和：':'Principal & interest sum:','科学计数法：':'Scientific notation:',
'📋 布灯方案：':'📋 Lighting layout plan:','限值要求：':'Limit requirements:','盈利指数 PI：':'Profitability index PI:',
'抗风等级：':'Wind resistance rating:','基本单位：':'Base unit:','原始大小：':'Original size:',
'年化回报率（复利）：':'Annualized return (compound):','第 1 年末：':'End of year 1:','三个内角：':'Three interior angles:',
'综合评分：':'Composite score:','使用年限：':'Service life:','精确：':'Precise:','环保等级：':'Eco grade:',
'保养计划：':'Maintenance plan:','🟢 状态良好：':'🟢 Status good:','成本绩效指数 CPI：':'Cost performance index CPI:',
'保养后测试：':'Post-maintenance test:','公式：':'Formula:','互补色：':'Complementary color:','修复输出：':'Repair output:',
'应用场景：':'Application scenario:','检测到：':'Detected:','第 10 行：':'Line 10:','建议仓位比例：':'Suggested position ratio:',
'年后的购买力相当于现在的：':'Purchasing power after N years vs now:','✅ 良好：':'✅ Good:','基本单位值：':'Base unit value:',
'小数：':'Decimal:','第 8 行：':'Line 8:','分档计算明细：':'Tiered calculation details:','工程总费用：':'Total project cost:',
'明度差：':'Lightness difference:','搭配建议：':'Matching suggestion:','✅ 表达式：':'✅ Expression:',
'电机功率：':'Motor power:','环境要求：':'Environmental requirement:','📌 指数说明：':'📌 Index note:',
'估算轴功率：':'Estimated shaft power:','🏷️ 推荐机型：':'🏷️ Recommended model:','对比完成：':'Comparison complete:',
'标准分 z=(x−μ)/σ：':'Standard score z=(x−μ)/σ:','磨损量：':'Wear amount:','首月还款：':'First month payment:',
'预计总寿命：':'Estimated total life:','落地速度 v：':'Impact velocity v:','含义：':'Meaning:','字符数：':'Character count:',
'步骤：':'Steps:','· 年运行小时数：':'· Annual operating hours:','第 4 行：':'Line 4:','📋 碳钢：':'📋 Carbon steel:',
'效率要求：':'Efficiency requirement:','压缩形式：':'Compression form:','品相等级：':'Grade level:',
'净现值 NPV：':'Net present value NPV:','📍 地点 A：':'📍 Location A:','📦 推荐设备：':'📦 Recommended device:',
'落地时间 t：':'Fall time t:','· 耐磨等级：':'· Wear grade:','📋 校核公式：':'📋 Check formula:',
'· 环保等级：':'· Eco grade:','📊 较A油：':'📊 vs A oil:','📌 dn 正常，常规维护即可。脂润滑：':'📌 dn normal, routine maintenance. Grease lube:',
'🌐 地球半径：':'🌐 Earth radius:','· 推荐润滑油：':'· Recommended lubricant:','💡 推荐涂层体系：':'💡 Recommended coating system:',
'🛡️ 隔爆型：':'🛡️ Flameproof type:','🧪 气体类别 IIB（乙烯类）：':'🧪 Gas group IIB (ethylene):',
'🌡️ 温度组别 T4：':'🌡️ Temperature class T4:','🧭 初始方位角：':'🧭 Initial azimuth:',
'🏠 推荐空调配置：':'🏠 Recommended AC config:','路径：':'Path:','强度：':'Intensity:','调号：':'Key signature:',
'已知：':'Given:','生成表达式：':'Generate expression:','→ 替代：':'→ Alternative:',
'，标点符号：':', Punctuation:','；方差 np(1−p)：':'; Variance np(1−p):','，趋势：':', Trend:',
'，剩余期限：':', Remaining term:','下混淆。建议拉开明暗差（这是色觉缺陷下最可靠的分辨手段）：':'To avoid confusion, increase the lightness difference (most reliable cue under color-vision deficiency):',
'🧪 气体类别 IIB（乙烯类）：':'🧪 Gas group IIB (ethylene):',
}
import json, os
root=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# 去重键（dict 自去重）
out={}
# 保留已有键，避免重跑丢失补译
try:
    out.update(json.load(open(os.path.join(root,'i18n/tools/en/_prefix.json'))))
except Exception:
    pass
for k,v in T.items():
    if not k or not any('\u4e00'<=c<='\u9fff' for c in k):  # 必须含中文
        continue
    out[k]=v
json.dump(out, open(os.path.join(root,'i18n/tools/en/_prefix.json'),'w'), ensure_ascii=False, indent=1)
print('prefix keys written:', len(out))
# 校验：译文不得含中文
bad=[(k,v) for k,v in out.items() if any('\u4e00'<=c<='\u9fff' for c in v)]
print('含中文译文(应0):', bad)
