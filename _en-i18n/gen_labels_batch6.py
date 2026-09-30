#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
gen_labels_batch6.py — 交互态标签批（真机交互探针 report interact_full2 发现）

背景：既有审计只扫「加载后默认可见 DOM」，而**点击计算后**才渲染的结果区标签
（表头/统计量名/错误提示/按钮/选项）从未被审计覆盖 ⇒ 前几轮「边界耗尽」误判的真因。

策略：
- 带冒号标签（`X：`/`X: `）→ `_prefix.json`：冒号键走 anywhere 替换，天然低误伤。
- 孤立标签（表头/按钮/选项，节点==标签）→ `_common.json`：**精确匹配**，零 garble 风险。
- 排除：生成样本(代码/配置 dump)、步骤解释散文、枚举评级值(良好/较差…)、
  随机生成名(甜酱/桃熊…)、动态编号(1 级/5 年)。
运行：python3 _en-i18n/gen_labels_batch6.py
"""
import json, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PREFIX = os.path.join(ROOT, "i18n/tools/en/_prefix.json")
COMMON = os.path.join(ROOT, "i18n/tools/en/_common.json")

# ---- 带冒号标签 → _prefix.json（anywhere 替换；键含冒号）----
COLON = {
    "解读：": "Interpretation: ",
    "输入：": "Input: ",
    "相关量：": "Related quantities: ",
    "待签名串：": "String to sign: ",
    "签名结果：": "Signature: ",
    "区间概率：": "Interval probability: ",
    "分量计算：": "Component calculation: ",
    "相关：": "Correlation: ",
    "双曲函数：": "Hyperbolic functions: ",
    "定义：": "Definition: ",
    "展开：": "Expansion: ",
    "逐步计算：": "Step by step: ",
    "质因数分解：": "Prime factorization: ",
    "质因数分解验证：": "Prime factorization check: ",
    "升序排列：": "Sorted ascending: ",
    "排序后的数据：": "Sorted data: ",
    "排序：": "Sort: ",
    "频率表：": "Frequency table: ",
    "提示：": "Note: ",
    "百分位：": "Percentile: ",
    "分布：": "Distribution: ",
    "例子解读：": "Example: ",
    "建立假设：": "Set up hypotheses: ",
    "方向余弦：": "Direction cosines: ",
    "方向角：": "Direction angles: ",
    "性质验证：": "Property check: ",
    "对称性：": "Symmetry: ",
    "关系：": "Relation: ",
    "递推：": "Recurrence: ",
    "验证：": "Check: ",
    "不等式：": "Inequality: ",
    "向上取整：": "Round up: ",
    "转换为角度：": "Convert to degrees: ",
    "欧几里得算法步骤（辗转相除法）：": "Euclidean algorithm steps (repeated division): ",
    "计算步骤（换底公式）：": "Steps (change of base): ",
    "计算步骤（线性插值法）：": "Steps (linear interpolation): ",
    "校验位: ": "Check digit: ",
    "计算Steps:": "Calculation steps: ",
    "常用对数Formula:": "Common logarithm formula: ",
    "位置Formula:": "Position formula: ",
    "替代Formula:": "Alternative formula: ",
    "逐分量Sum:": "Component-wise sum: ",
    "组合数：": "Combinations: ",
    "排列数：": "Permutations: ",
    "数据（": "Data (",   # 前缀键：数据（n=…）
}

# ---- 孤立标签（节点==标签）→ _common.json 精确匹配 ----
COMMON_ADD = {
    # 统计量 / 表头
    "分步计算": "Step-by-step",
    "标准差": "Standard deviation",
    "转换结果": "Conversion result",
    "标准": "Standard",
    "正文": "Body",
    "指标": "Metric",
    "合计": "Total",
    "期数": "Periods",
    "方差": "Variance",
    "最小值": "Minimum",
    "最大值": "Maximum",
    "结果": "Result",
    "占比": "Share",
    "状态": "Status",
    "数值": "Value",
    "本金": "Principal",
    "剩余本金": "Remaining principal",
    "版本": "Version",
    "二进制": "Binary",
    "十进制": "Decimal",
    "十六进制": "Hexadecimal",
    "八进制": "Octal",
    "压缩结果": "Compressed result",
    "行数": "Rows",
    "问题": "Question",
    "结论": "Conclusion",
    "下划线": "Underline",
    "平方和 SS": "Sum of squares SS",
    "元素": "Element",
    "数据个数 n": "Data count n",
    "维度": "Dimension",
    "权重": "Weight",
    "查询方式": "Query mode",
    "要求": "Requirement",
    "⭐ 收藏": "⭐ Favorite",
    "CSS 代码": "CSS Code",
    "字数": "Word count",
    "字符数": "Characters",
    "字节数": "Bytes",
    "主题": "Subject",
    "输出格式": "Output format",
    "绘制": "Draw",
    "文件大小": "File size",
    "复制": "Copy",
    "修改": "Edit",
    "新增": "Add",
    "示例": "Example",
    "求和": "Sum",
    "三角形": "Triangle",
    "类别": "Category",
    "邮箱": "Email",
    "日期": "Date",
    "中文字符": "Chinese characters",
    "全小写": "Lowercase",
    "删除空行": "Remove empty lines",
    "面积": "Area",
    "名称": "Name",
    "特性": "Feature",
    "项目": "Item",
    "对比": "Comparison",
    "典型用途": "Typical use",
    "方向": "Direction",
    "渠道": "Channel",
    "行": "Row",
    "值": "Value",
    "频数": "Frequency",
    "来源": "Source",
    "天数": "Days",
    "年度": "Year",
    "数据明细": "Data details",
    "概率分布图": "Probability distribution chart",
    # 金融 / 会计
    "流动比率": "Current ratio",
    "使用年限": "Service life",
    "直线法": "Straight-line method",
    "总利息": "Total interest",
    "总还款额": "Total repayment",
    "利息": "Interest",
    "月供": "Monthly payment",
    "科目": "Account",
    "年龄": "Age",
    "级数": "Series",
    "应纳税所得额": "Taxable income",
    "税率": "Tax rate",
    "安全等级": "Safety level",
    "优势比变化": "Odds ratio change",
    # 统计量专名
    "样本均值": "Sample mean",
    "临界值": "Critical value",
    "Z 分数": "Z-score",
    "Z 统计量": "Z statistic",
    "T 分数": "T-score",
    "F 统计量": "F statistic",
    "皮尔逊 r": "Pearson r",
    "卡方值": "Chi-square value",
    "自由度": "Degrees of freedom",
    "组数 k": "Groups k",
    "总样本数 N": "Total samples N",
    "组间自由度": "Between-groups df",
    "组内自由度": "Within-groups df",
    "总均值": "Grand mean",
    "总观察数": "Total observations",
    "样本数 n": "Sample size n",
    "效应量 d": "Effect size d",
    "效应量等级": "Effect size grade",
    "功效等级": "Power grade",
    "置信水平": "Confidence level",
    "预期比例 p": "Expected proportion p",
    "标准差倍数": "SD multiplier",
    "计算耗时": "Computation time",
    "结果位数": "Result digits",
    "各百分位结果": "Percentile results",
    "p 值": "p-value",
    "需至少调查": "At least",
    "✓ 无异常值": "✓ No outliers",
    # 错误提示 / 状态
    "请上传图片": "Please upload an image",
    "请输入 SVG 代码": "Please enter SVG code",
    "请先输入要哈希的文本": "Please enter the text to hash",
    "请填写密钥 Secret": "Please enter the secret key",
    "请先输入要分析的文本": "Please enter text to analyze",
    "✅ 解析成功": "✅ Parsed successfully",
    "JWT生成成功": "JWT generated successfully",
    "ANOVA 表": "ANOVA table",
    "拒绝 H₀": "Reject H₀",
    "先验 vs 后验对比": "Prior vs posterior comparison",
}


def merge(d, add, path, minlen=1):
    n = 0
    for k, v in add.items():
        assert not re.search(r"[\u4e00-\u9fff]", v), "ZH in value: %r -> %r" % (k, v)
        assert len(k) >= minlen, "short key: %r" % k
        if k in d:
            continue
        d[k] = v
        n += 1
    with open(path, "w", encoding="utf-8") as f:
        json.dump(d, f, ensure_ascii=False, indent=1)
        f.write("\n")
    return n


pf = json.load(open(PREFIX, encoding="utf-8"))
cm = json.load(open(COMMON, encoding="utf-8"))
np_ = merge(pf, COLON, PREFIX, minlen=2)
nc = merge(cm, COMMON_ADD, COMMON, minlen=1)
print("prefix +%d -> %d ; common +%d -> %d" % (np_, len(pf), nc, len(cm)))
