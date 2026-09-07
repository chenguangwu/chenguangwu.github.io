#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""真实化 edu2 分类 5 个工具的 content_deepdive 条目。

原 5 key 均为占位变体（summary 原 None、faqs 仅 2 条）。覆盖考试成绩分析/考试倒计时/
课程表冲突检测/学习进度仪表/错题本管理等真实教育场景。
A 类 schedule-conflict 的 formula-desc 为工程错配、B 类 study-progress 含 opt 套话、
C 类 5 页 tool-intro-body 套话，均由 opt_edu2_hardcode.py 清理。
"""
import json

DIS = "。仅供学习辅助与自我评测参考，不替代学校教学、教师评定与官方考试标准；具体以教材与考试院规定为准。"
PATH = "i18n/tools/content_deepdive.json"
data = json.load(open(PATH, encoding="utf-8"))


def setk(slug, summary, sc, ex, faqs):
    key = "edu2/" + slug
    assert key in data, "missing key: " + key
    data[key] = dict(
        summary=summary,
        scenarios=sc,
        example=ex,
        faqs=[dict(q=q, a=a + DIS) for q, a in faqs],
    )


# 1 考试成绩分析
setk("exam-analysis",
     "录入多次考试成绩，统计均值、趋势、波动与薄弱科目，辅助学情诊断与复习重点定位。",
     ["趋势统计：多次成绩变化与斜率。", "波动分析：标准差衡量稳定性。", "薄弱定位：按科目横向对比找弱项。"],
     "示例：三次数学 78/85/82，均值 81.7、升后回落，需巩固。",
     [("看什么？", "趋势反映进步与否，波动大说明发挥不稳。"),
      ("薄弱科目？", "按各科均分与排名横向比较定位。"),
      ("用途？", "学情自查与复习规划，不替代教师评定。")])

# 2 考试倒计时
setk("exam-countdown",
     "统计距多个目标考试的剩余天数与工作日，支持并行倒计时与每日学习打卡。",
     ["并行倒计时：多考试同时提醒。", "工作日统计：自动区分工作日周末。", "每日打卡：记录学习投入。"],
     "示例：高考距 120 天，其中工作日约 86 天。",
     [("工作日？", "按周一至周五估算，忽略调休。"),
      ("多考试？", "可同时添加多个考试分别倒计时。"),
      ("数据？", "进度存本地，不上传。")])

# 3 课程表冲突检测
setk("schedule-conflict",
     "录入多门课程的周次、星期与节次，自动检测时间重叠冲突，辅助排课与选课。",
     ["冲突检测：同时间多课重叠预警。", "周次校验：按上课周范围查冲突。", "可视化：高亮冲突单元格。"],
     "示例：周一第 1-2 节同时排高数与大物，判定冲突。",
     [("规则？", "同星期同节次且周次重叠即冲突。"),
      ("用途？", "选课排课冲突自查，以教务安排为准。"),
      ("本地？", "纯前端计算，不上传。")])

# 4 学习进度仪表
setk("study-progress",
     "按目标总量与已完成量计算完成度、日均速度与预计完成日，可视化学习进度。",
     ["完成度：已完成÷目标。", "日均速度：按投入估进度。", "预计完工：倒推完成日期。"],
     "示例：目标 1000 题、已完成 400、日均 50，预计还需 12 天。",
     [("预计准吗？", "基于当前速度估算，速度变化会影响结果。"),
      ("用途？", "备考节奏管理，非官方进度。"),
      ("数据？", "存浏览器本地，不上传。")])

# 5 错题本管理
setk("wrong-book",
     "按学科与错误类型归类错题，记录订正状态与复习次数，辅助查漏补缺。",
     ["归类：按学科/错因分组。", "订正跟踪：标记已订正与待巩固。", "复习次数：统计重练频次。"],
     "示例：数学计算错归「计算」组，标记已订正、复习 2 次。",
     [("怎么归类？", "手动选学科与错因标签，便于聚合。"),
      ("用途？", "薄弱点复盘，不替代老师批改。"),
      ("数据？", "存本地，不上传。")])

cnt = sum(1 for k in data if k.startswith("edu2/") and data[k].get("summary") and len(data[k].get("faqs") or []) >= 3)
print("edu2 key 总数:", sum(1 for k in data if k.startswith("edu2/")))
print("已真实化(含summary且faqs>=3)数:", cnt)
json.dump(data, open(PATH, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print("已写入", PATH)
