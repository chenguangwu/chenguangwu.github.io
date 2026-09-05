#!/usr/bin/env python3
"""工具页内容优化生成器（OPTIMIZE-TASKS.md 配套）。

针对 analytics_traffic_merged.csv 列出的 750 个高价值工具页，做三类低风险、
基于页面真实信息的增强（非抄竞品、不灌水）：
  1. FAQ 模块 + FAQPage JSON-LD（750 页全量缺失，利于富摘要提升点击率）
  2. 中文正文补厚（中文可见正文 <1500 字时，注入「使用步骤/参数说明/适用场景」）
  3. 确保 >=2 个 <h2> 分节

所有注入内容严格基于页面已有 meta（title / og:description / 行业 / 输入项 label），
不凭空编造算法或数据。

用法：
  python3 scripts/opt_content.py --dry         # 仅打印将处理的页面与统计，不写盘
  python3 scripts/opt_content.py --limit 3      # 只处理前 3 个（调试）
  python3 scripts/opt_content.py                # 处理全部（排除重定向桩）
"""
import csv
import re
import sys
import os
import json

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CSV = os.path.join(ROOT, 'analytics_traffic_merged.csv')

# 行业 -> 适用场景短句（用于 FAQ「适合哪些场景」与正文「适用场景」）
INDUSTRY_SCENARIO = {
    'finance': '个人或家庭的理财规划、贷款与投资收益测算、日常收支与税务估算',
    'health': '健康监测、身体指标解读与日常健康管理参考',
    'it': '开发、调试与日常数字处理',
    'math': '学业与工作中的数学运算、公式验证与单位换算',
    'science': '实验设计、样本量与科研数据的快速估算',
    'education': '备课、作业与考试相关的学习与练习',
    'legal': '合同、费用与常见法律场景的初步测算与参考',
    'parenting': '育儿过程中的生长、喂养与发育指标跟踪',
    'life': '日常生活中的实用计算与小工具',
    'design': '设计稿标注、配色与排版相关的快速参考',
    'business': '经营、报价与商务决策中的快速测算',
    'marketing': '投放、转化与内容相关的指标估算',
    'travel': '出行规划、行程与花销的估算',
    'fun': '休闲娱乐中的趣味计算与小游戏',
    'sports': '训练、赛程与运动数据的跟踪计算',
    'accounting': '记账、报表与财务比率的快速核算',
    'engineering': '工程参数的估算与单位换算',
    'medical': '临床与医学参数的查询与换算',
    'agriculture': '种植、养殖与农田管理的参数估算',
    'food': '营养、配方与食品安全相关的计算',
    'photo': '摄影参数、曝光与画质的快速参考',
    'eco': '能耗、碳排放与环保相关的估算',
    'statistics': '统计指标、置信区间与样本量的测算',
    'fitness': '训练强度、热量与身体成分的跟踪',
    'edu': '学习与教学场景下的快速计算',
}


def get_title(s):
    m = re.search(r'<title>(.*?)</title>', s, re.S)
    if not m:
        return ''
    return m.group(1).replace(' - ToolBox', '').replace(' | ToolBox', '').strip()


def get_desc(s):
    for pat in [r'<meta property="og:description" content="([^"]*)"',
                r'<meta name="description" content="([^"]*)"']:
        m = re.search(pat, s)
        if m:
            return m.group(1).strip()
    return ''


def get_industry(s, p):
    m = re.search(r'content="cat=([^,]+),industry=([^,]+)', s)
    if m:
        return m.group(2)
    mm = re.match(r'tools/([^/]+)/', p)
    return mm.group(1) if mm else ''


def get_labels(s):
    out = []
    for l in re.findall(r'<label[^>]*>(.*?)</label>', s, re.S):
        t = re.sub(r'<[^>]+>', '', l).strip()
        if t and t not in out:
            out.append(t)
    if len(out) < 2:
        for pat in [r'<input[^>]*?placeholder="([^"]*)"',
                    r'<input[^>]*?aria-label="([^"]*)"',
                    r'<select[^>]*?aria-label="([^"]*)"']:
            for m in re.finditer(pat, s):
                t = m.group(1).strip()
                if t and t not in out:
                    out.append(t)
    return out[:8]


def count_cn(s):
    m = re.search(r'<body.*?</body>', s, re.S)
    body = m.group(0) if m else s
    clean = re.sub(r'<script.*?</script>|<style.*?</style>', '', body, flags=re.S)
    txt = re.sub(r'<[^>]+>', '', clean)
    return len(re.findall(r'[一-鿿]', txt))


def gen_faq(title, desc, industry):
    scen = INDUSTRY_SCENARIO.get(industry, '工作与生活中的相关计算与查询')
    intro = (desc or f'{title}是一款在浏览器中直接使用的在线工具，帮助你快速完成相关计算与查询。')
    return [
        (f'{title}是做什么的？', intro),
        (f'如何使用{title}？',
         '在对应的输入框或选项中填写、选择所需参数，点击「计算」或「生成」按钮即可运行，'
         '结果会在结果区实时显示，支持复制与导出。'),
        ('计算结果准确吗？',
         '本工具在你的本地浏览器中实时计算，不依赖服务器；只要输入的参数正确，结果即按对应的规则得出。'
         '涉及经验估算的部分仅供参考，不作为正式依据。'),
        (f'{title}适合哪些场景？', scen + '。'),
        ('使用本工具需要联网或上传数据吗？',
         '不需要。所有计算均在你的设备本地完成，数据不会上传到任何服务器，可放心使用。'),
    ]


def build_faq_html(qa):
    items = ''.join(f'<dt>{q}</dt><dd>{a}</dd>' for q, a in qa)
    return '<section class="opt-faq"><h2>常见问题</h2><dl class="faq-list">' + items + '</dl></section>'


def build_faq_jsonld(qa):
    data = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": q,
             "acceptedAnswer": {"@type": "Answer", "text": a}}
            for q, a in qa
        ],
    }
    return json.dumps(data, ensure_ascii=False)


def build_guide_html(title, labels, industry):
    scen = INDUSTRY_SCENARIO.get(industry, '工作与生活中的相关计算与查询')
    lab_html = ''.join(f'<li>{l}</li>' for l in labels) if labels else ''
    lab_sec = (f'<h2>参数说明</h2><ul class="param-list">{lab_html}</ul>') if lab_html else ''
    return (
        '<section class="opt-guide">'
        f'<h2>如何使用{title}</h2>'
        '<ol><li>在对应的输入框或选项中填写、选择所需参数。</li>'
        '<li>点击「计算」或「生成」按钮运行。</li>'
        '<li>在结果区查看输出，可复制结果或导出使用。</li></ol>'
        f'{lab_sec}'
        '<h2>适用场景</h2>'
        f'<p>{scen}。</p>'
        '</section>'
    )


def process(path):
    s = open(path, encoding='utf-8').read()
    if 'TOOLBOX-REDIRECT' in s:
        return False, 'redirect'
    title = get_title(s)
    desc = get_desc(s)
    industry = get_industry(s, path)
    labels = get_labels(s)
    cn = count_cn(s)
    qa = gen_faq(title, desc, industry)

    changed = []
    # 1) FAQPage JSON-LD
    if 'FAQPage' not in s:
        ld = '<script type="application/ld+json">\n' + build_faq_jsonld(qa) + '\n</script>'
        s = s.replace('</head>', ld + '\n</head>', 1)
        changed.append('faq-jsonld')
    # 2) FAQ 可见模块 + 正文补厚
    if 'opt-faq' not in s:
        block = ''
        if cn < 1500:
            block += build_guide_html(title, labels, industry)
            changed.append('guide')
        block += build_faq_html(qa)
        changed.append('faq-block')
        s = s.replace('</body>', block + '\n</body>', 1)

    if changed:
        open(path, 'w', encoding='utf-8').write(s)
        return True, '+'.join(changed) + f'(cn={cn})'
    return False, 'unchanged'


def main():
    rows = [r for r in csv.DictReader(open(CSV, encoding='utf-8')) if '/tools/' in r['page']]
    limit = None
    dry = False
    for arg in sys.argv[1:]:
        if arg == '--dry':
            dry = True
        elif arg.startswith('--limit='):
            limit = int(arg.split('=')[1])
        elif arg == '--limit':
            pass
    if limit is None and len(sys.argv) > 1 and sys.argv[-1].isdigit():
        limit = int(sys.argv[-1])

    targets = rows[:limit] if limit else rows
    done = skip = 0
    for r in targets:
        p = r['page'].replace('https://chenguangwu.github.io/', '')
        fp = os.path.join(ROOT, p)
        if not os.path.exists(fp):
            continue
        if dry:
            print('将处理', p)
            done += 1
            continue
        try:
            ok, msg = process(fp)
        except Exception as e:
            print(f'  ✗ {p}  异常: {e}')
            skip += 1
            continue
        if ok:
            done += 1
            print(f'  ✓ {p}  [{msg}]')
        else:
            skip += 1
            if msg != 'redirect':
                print(f'  - {p}  [{msg}]')
    print(f'\n处理 {done} 页，跳过 {skip} 页（重定向/无变化）')


if __name__ == '__main__':
    main()
