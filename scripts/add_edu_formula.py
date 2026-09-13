#!/usr/bin/env python3
"""edu 分类 formula 补框：给 11 个计算类缺框页加 class="card formula-box" 公式说明。

用法: python3 scripts/add_edu_formula.py [--apply]
公式文本取自各页真实计算逻辑；插入锚点按优先级自动匹配（tip-box / tabs / tool-result / input-row / subject-row 之前）。
"""
import os, re, sys

TOOLS = os.path.join(os.path.dirname(__file__), '..', 'tools', 'edu')

FB_TPL = ('<div class="card formula-box">\n'
          '  <div class="formula-title">📐 计算方式</div>\n'
          '  <p>%s</p>\n'
          '</div>\n')

FORMULAS = {
  'calc-3': '按权重分配每日学习时长：科目 i 时长 = 总可用时长 × 该科目权重 ÷ 全部科目权重之和。权重越高分配时长越多，便于把有限时间集中到重点科目。',
  'countdown-5': '剩余天数 = 目标日期 − 今天（按自然日取整）；工作日 = 区间内周一至周五的天数，自动跳过周末，用于估算可投入备考的工作日数量。',
  'exam-gpa-calculator': 'GPA = Σ(课程绩点 × 学分) ÷ Σ学分。百分制按内置换算表转为绩点（如 90+→4.0、60+→1.0、不及格 0）；切换院校等级制时换算口径随之变化。',
  'exam-score-calculator': '得分 = 正确题数 × 每题分值（或 正确率 × 总分）；通过线 = 总分 × 及格比例；正确率 = 正确数 ÷ 总题数 × 100%。',
  'exam-study-planner': '累计专注时长 = 单次专注分钟数 × 完成轮数；当日目标达成 = 完成轮数 ÷ 目标轮数。番茄钟按「专注 + 休息」交替，帮助维持注意力。',
  'exam-timer': '进度 = (1 − 剩余秒数 ÷ 总秒数) × 100%；已用时长 = 总时长 − 剩余时长。分段提醒用于合理分配答题与检查时间。',
  'gpa-calculator': '累积 GPA = Σ(各学期 Σ(课程绩点 × 学分)) ÷ Σ总学分。多学期累计时，高学分课程对总绩点影响更大。',
  'grade-calculator': '加权总分 = Σ(分项得分 × 权重) ÷ Σ权重；权重之和通常归一为 1，未归一时自动按总和分摊权重影响。',
  'quiz-score-percentage': '正确率 = 正确题数 ÷ 总题数 × 100%；得分 = 正确数 × 每题分；错误数 = 总数 − 正确数；按设定及格比例判定是否通过。',
  'study-planner': '番茄钟累计专注 = 单次专注分钟数 × 完成轮数；任务完成率 = 已完成任务数 ÷ 任务总数。按优先级排序后优先推进高优先任务。',
  'timezone-converter': '目标地当地时刻 = 本地时刻 + (目标地 UTC 偏移 − 本地 UTC 偏移)；UTC 偏移含半小时制与夏令时调整，跨日时自动进位。',
}

ANCHORS = [
  r'(<div class="tip-box)',
  r'(<div class="tabs")',
  r'(<div class="scale-row")',
  r'(<div class="set-row")',
  r'(<div[^>]*class="[^"]*tool-result[^"]*"[^>]*>)',
  r'(<div class="input-row")',
  r'(<div class="subject-row")',
]


def add_one(slug, apply):
    fp = os.path.join(TOOLS, slug + '.html')
    s = open(fp, encoding='utf-8').read()
    if 'class="formula-box"' in s:
        print('  skip %s (已有框)' % slug)
        return False
    if slug not in FORMULAS:
        print('  skip %s (无公式定义)' % slug)
        return False
    fb = FB_TPL % FORMULAS[slug]
    used = None
    for pat in ANCHORS:
        m = re.search(pat, s)
        if m:
            used = pat
            s2 = s[:m.start()] + fb + s[m.start():]
            break
    if used is None:
        print('  WARN %s (无可用锚点)' % slug)
        return False
    if apply:
        open(fp, 'w', encoding='utf-8').write(s2)
    print('  + %s (锚点:%s%s)' % (slug, used, ' [已写]' if apply else ''))
    return True


def main():
    apply = '--apply' in sys.argv
    n = 0
    for slug in FORMULAS:
        if add_one(slug, apply):
            n += 1
    print('==== %s %d 页 ====' % ('已应用' if apply else '预演', n))


if __name__ == '__main__':
    main()
