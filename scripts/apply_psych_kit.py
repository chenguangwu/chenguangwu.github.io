# -*- coding: utf-8 -*-
"""psych-kit 注入脚本（幂等）

向 psychiatry / psychology 下的量表页面注入 js/psych-kit.js 及量表配置。
- clinical：按国际常用临界值配置高危触发条件（score_gte / item_gte / text_any）
- entertainment：不加热线，页头加「娱乐参考 / 自评参考」标识
重复执行不会重复注入；已注入的会刷新 data-psych 配置。
"""
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOOLS_JSON = os.path.join(ROOT, 'json', 'tools.json')

# key: 文件名 -> (name 覆盖, kind, minutes, risk 配置, note)
# risk: score_gte / item_gte:[题索引(0基), 阈值] / text_any:[关键词]
CLINICAL = {
    'psychiatry/phq9-depression.html':      ('PHQ-9 抑郁筛查', 'clinical', 3, {'score_gte': 20, 'item_gte': [8, 1]}, ''),
    'psychiatry/gad7-anxiety.html':         ('GAD-7 焦虑筛查', 'clinical', 2, {'score_gte': 15}, ''),
    'psychiatry/eat26-eating.html':         ('EAT-26 进食障碍筛查', 'clinical', 5, {'score_gte': 20}, ''),
    'psychiatry/cage-substance.html':       ('CAGE 酒精问题筛查', 'clinical', 1, {'score_gte': 2}, ''),
    'psychiatry/pcl5-ptsd.html':            ('PCL-5 创伤后应激筛查', 'clinical', 5, {'score_gte': 31}, ''),
    'psychiatry/lsas-social.html':          ('LSAS 社交焦虑评估', 'clinical', 8, {'score_gte': 80}, ''),
    'psychiatry/mdq-bipolar.html':          ('MDQ 双相障碍筛查', 'clinical', 3, {'text_any': ['筛查阳性']}, ''),
    'psychiatry/panss-schizophrenia.html':  ('PANSS 精神症状评定', 'clinical', 10, {'score_gte': 96}, ''),
    'psychiatry/phq15-somatization.html':   ('PHQ-15 躯体症状评估', 'clinical', 3, {'score_gte': 15}, ''),
    'psychiatry/ybocs-ocd.html':            ('Y-BOCS 强迫严重度评估', 'clinical', 5, {'score_gte': 32}, ''),
    'psychiatry/isi-insomnia.html':         ('ISI 失眠严重度评估', 'clinical', 3, {'score_gte': 22}, ''),
    'psychiatry/pdss-panic.html':           ('PDSS 惊恐障碍严重度评估', 'clinical', 4, {'score_gte': 16}, ''),
    'psychiatry/asrs-adhd.html':            ('ASRS 成人注意缺陷筛查', 'clinical', 3, {'score_gte': 14}, ''),
    'psychiatry/aq-autism.html':            ('AQ 孤独症特质自评', 'clinical', 6, {'score_gte': 32}, ''),
    'psychiatry/bis11-impulse.html':        ('BIS-11 冲动性评估', 'clinical', 5, {'score_gte': 72}, ''),
    'psychiatry/les-stress.html':           ('生活事件压力评估', 'clinical', 5, {'text_any': ['重度', '高危']}, ''),
    'psychiatry/self-assess-4.html':        ('心理健康自评', 'clinical', 4, {'text_any': ['重度', '高危']}, ''),
    'psychiatry/rater-23.html':             ('心理症状评定', 'clinical', 5, {'text_any': ['重度', '高危']}, ''),
    'psychiatry/rater-24.html':             ('心理症状评定', 'clinical', 5, {'text_any': ['重度', '高危']}, ''),
    'psychiatry/calc-1.html':               ('心理量表计算', 'clinical', 2, {'text_any': ['重度', '高危']}, ''),
    'psychiatry/mmpi2-personality.html':    ('MMPI-2 人格临床量表', 'clinical', 15, {'text_any': ['重度', '高危', '显著升高']}, ''),
    'psychiatry/cdrisc-resilience.html':    ('CD-RISC 心理韧性评估', 'clinical', 4, {}, ''),
    # psychology 目录下的临床量表（同一标准的另一份实现）
    'psychology/phq9-assessment.html':      ('PHQ-9 抑郁自评', 'clinical', 3, {'score_gte': 20, 'item_gte': [8, 1]}, ''),
    'psychology/sas-assessment.html':       ('SAS 焦虑自评', 'clinical', 4, {'score_gte': 70}, ''),
    'psychology/psqi-assessment.html':      ('PSQI 睡眠质量自评', 'clinical', 5, {'score_gte': 16}, ''),
    'psychology/rater.html':                ('睡眠质量评分（PSQI 简化版）', 'clinical', 3, {'score_gte': 16}, ''),
    'psychology/scl90-assessment.html':     ('SCL-90 心理健康自评', 'clinical', 15, {'score_gte': 200, 'text_any': ['重度', '显著']}, ''),
    'psychology/self-test-pressure.html':   ('压力水平自评（PSS）', 'clinical', 3, {'score_gte': 27}, ''),
}

ENTERTAINMENT = {
    'psychology/tester-2.html':             ('MBTI 人格类型测试', 10, '娱乐测试，不用于职业或临床决策'),
    'psychology/enneagram-test.html':       ('九型人格测试', 10, '娱乐测试，不用于职业或临床决策'),
    'psychology/bigfive-personality-test.html': ('大五人格测试', 8, '研究自评参考，不构成诊断'),
    'psychology/holland-career-test.html':  ('霍兰德职业兴趣测试', 10, '职业方向参考，不做人事决策'),
    'psychology/attachment-style-test.html': ('成人依恋类型测试', 8, '关系模式参考，不构成诊断'),
    'psychology/bubble-tea-personality-quiz.html': ('珍珠奶茶人格测试', 3, '纯娱乐测试'),
    'psychology/analysis-2.html':           ('性格色彩分析', 6, '娱乐测试，不用于职业或临床决策'),
    'psychology/self-assess.html':          ('情商（EQ）自评', 6, '自评参考，不构成诊断'),
    'psychology/assessor.html':             ('拖延症程度评估', 5, '自评参考，不构成诊断'),
    'psychology/calc-self-assess.html':     ('乐观指数自评', 4, '自评参考，不构成诊断'),
    'psychology/calc-12.html':              ('幸福感指数计算', 3, '自评参考，不构成诊断'),
    'psychology/tester-3.html':             ('学习风格测试（VARK）', 5, '学习方式参考，不做能力判定'),
}

SKIP = {
    'psychiatry/index.html', 'psychology/index.html',
    'psychiatry/assessor-risk-5.html',   # 已有专用危机弹窗与热线横幅
    'psychiatry/cssrs-suicide.html',     # 已有专用危机弹窗与热线横幅
    'psychology/random-12.html',         # 知识卡片，工单标注无需改
    'psychology/generator-20.html',      # 知识生成，工单标注无需改
}


def build_cfg(rel):
    """rel: tools/<industry>/<file>.html"""
    key = rel[len('tools/'):]
    page_key = os.path.basename(rel)[:-5]
    if key in CLINICAL:
        name, kind, minutes, risk, note = CLINICAL[key]
        cfg = {'key': page_key, 'name': name, 'kind': kind, 'minutes': minutes, 'period': '最近两周'}
        if risk:
            cfg['risk'] = risk
        if note:
            cfg['note'] = note
        return cfg
    if key in ENTERTAINMENT:
        name, minutes, note = ENTERTAINMENT[key]
        return {'key': page_key, 'name': name, 'kind': 'entertainment',
                'minutes': minutes, 'period': '最近两周', 'note': note}
    return None


def inject(path, rel):
    cfg = build_cfg(rel)
    if cfg is None:
        return 'skip-config'
    s = open(path, encoding='utf-8').read()
    tag = '<script src="../../js/psych-kit.js" data-psych=\'%s\' defer></script>' % json.dumps(
        cfg, ensure_ascii=False, separators=(',', ':'))
    m = re.search(r'<script src="(?:\.\./)+js/psych-kit\.js"[^>]*></script>\s*', s)
    if m:
        if m.group(0).strip() == tag:
            return 'unchanged'
        s = s[:m.start()] + tag + '\n' + s[m.end():]
        open(path, 'w', encoding='utf-8').write(s)
        return 'updated'
    if 'psych-kit.js' in s:
        return 'skip-exists'
    idx = s.rfind('</body>')
    if idx < 0:
        return 'no-body'
    s = s[:idx] + tag + '\n' + s[idx:]
    open(path, 'w', encoding='utf-8').write(s)
    return 'injected'


def main():
    targets = []
    for ind in ('psychiatry', 'psychology'):
        d = os.path.join(ROOT, 'tools', ind)
        for fn in sorted(os.listdir(d)):
            if not fn.endswith('.html'):
                continue
            rel = 'tools/%s/%s' % (ind, fn)
            if rel in SKIP:
                continue
            targets.append((os.path.join(d, fn), rel))
    stats = {}
    for path, rel in targets:
        r = inject(path, rel)
        stats[r] = stats.get(r, 0) + 1
    print('targets:', len(targets))
    for k in sorted(stats):
        print('  %-12s %d' % (k, stats[k]))


if __name__ == '__main__':
    main()
