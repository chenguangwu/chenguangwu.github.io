#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""无 data-zh 的硬编码英文 → 中文 data-zh 锚点词典。

只收录**高置信、明确该中文化**的通用表头/描述词；标准名、文献引用、机构缩写、
英文专名（如 ACOG/KDIGO/ISO/IEC/AAHA、`Practice Bulletin No. 233`）一律不收，
按老板口径保留英文。

用法：给无 data-zh 的 <td>/<th> 纯英文元素补 data-zh="中文"，英文可见文本不动；
中文态由 tool-i18n.js::restoreAllDataZh() 还原为中文，英文态保持英文。
"""

# 精确整串匹配（大小写不敏感由调用方处理，这里存原样 key）
TERMS = {
  # 表头 / 通用 UI
  'Value': '数值', 'Item': '项目', 'Category': '分类', 'Score': '得分',
  'Description': '说明', 'Type': '类型', 'Note': '备注', 'Unit': '单位',
  'Field': '字段', 'Name': '名称', 'Status': '状态', 'Grade': '等级',
  'Parameter': '参数', 'Option': '选项', 'Date': '日期', 'Result': '结果',
  'Symbol': '符号', 'Level': '等级', 'Time': '时间', 'Metric': '指标',
  'Detail': '详情', 'Example': '示例', 'Color': '颜色', 'Rate': '比率',
  'Severity': '严重程度', 'Length': '长度', 'Weight': '重量',
  'Dimension': '尺寸', 'Formula': '公式', 'Word': '单词', 'Step': '步骤',
  'Question': '问题', 'Navigation': '导航', 'Frequency (Hz)': '频率（Hz）',
  'Body Part': '身体部位', 'Instruction': '说明', 'Level Name': '等级名称',
  'Food': '食物', 'Days Left': '剩余天数', 'Next Due': '下次到期',
  'Rounds': '轮次', 'Round': '轮次', 'Total': '合计', 'Count': '计数',
  'Input': '输入', 'Output': '输出', 'Method': '方法', 'Source': '来源',
  'Standard': '标准', 'Range': '范围', 'Average': '平均值', 'Max': '最大值',
  'Min': '最小值', 'Speed': '速度', 'Angle': '角度', 'Area': '面积',
  'Volume': '体积', 'Pressure': '压强', 'Power': '功率', 'Energy': '能量',
  'Temperature': '温度', 'Duration': '时长', 'Duration(s)': '时长（秒）',
  'Label': '标签', 'Code': '代码', 'Group': '组别', 'Section': '章节',
  'Action': '操作', 'Target': '目标', 'Mode': '模式', 'Version': '版本',
  'Language': '语言', 'Country': '国家', 'Region': '地区', 'City': '城市',
  'Year': '年份', 'Month': '月份', 'Day': '日', 'Week': '周',
  'Low': '低', 'Medium': '中', 'High': '高', 'None': '无',
  'Yes': '是', 'No': '否', 'True': '是', 'False': '否',
  'Pass': '通过', 'Fail': '不通过', 'Warning': '警告', 'Error': '错误',
  'OK': '正常', 'Note:': '备注：', 'Units': '单位', 'Notes': '备注',

  # 通用描述词（constRefBox 第2/3列常见）
  'Weighted scoring': '加权评分', 'Bit-byte conversion': '位-字节换算',
  'Glossary': '术语表', 'Overview': '概览', 'Summary': '汇总',
  'Definition': '定义', 'Purpose': '用途', 'Benefit': '益处',
  'Risk': '风险', 'Tips': '提示', 'Example calculation': '计算示例',
  'Common values': '常见数值', 'Reference range': '参考范围',
  'Conversion': '换算', 'Classification': '分级', 'Interpretation': '解读',
  'Measurement': '测量', 'Calculation': '计算', 'Assumption': '假设',
  'Limitation': '局限', 'Accuracy': '精度', 'Precision': '精密度',
}

# 单位/符号类：保留（含国际符号，按口径不译）——调用方据此跳过
KEEP_PATTERNS = [
  r'^mmol/L$', r'^mol/L$', r'^mg/dL$', r'^g/L$', r'^kg$', r'^cm$', r'^mm$',
  r'^Hz$', r'^kHz$', r'^MHz$', r'^dB$', r'^kPa$', r'^MPa$', r'^°C$',
]
