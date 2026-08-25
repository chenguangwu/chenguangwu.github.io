#!/usr/bin/env python3
# B-OPT25 审计：C 级工具中"有 function calc 计算逻辑但被判 C"的假C（本应升 B）
import sys, os, json, re
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
import _build as B

d = json.load(open(os.path.join(ROOT, 'json/tools.json'), encoding='utf-8'))
cs = [t for t in d if t['quality'] == 'C']
print('C级总数', len(cs))

stat = {'calc': 0, 'intro': 0, 'rich': 0, 'inputs_ge3': 0, 'own_ge800': 0}
fake_calc = []          # 有 function calc 但被判 C（说明 has_intro=False）
own_but_c = []          # 自研脚本长但被判 C（说明被 shared 误判）

for t in cs:
    fp = os.path.join(ROOT, 'tools', t['path'])
    if not os.path.exists(fp):
        print('MISSING', t['path']); continue
    c = open(fp, encoding='utf-8').read()
    q = B.classify_quality(c)
    if q != 'C':
        print('CLASSIFY!=C', t['path'], '->', q); continue
    inputs = len(re.findall(r'<(?:input|select|textarea)', c))
    has_calc = 'function calc' in c
    has_intro = bool(re.search(r'<p style="font-size:13px;color:var\(--text-muted\);margin-bottom:\d+px;">', c))
    rich = ('formula-box' in c) or ('<canvas' in c) or ('data-viz' in c)
    if has_calc: stat['calc'] += 1; fake_calc.append(t['path'])
    if has_intro: stat['intro'] += 1
    if rich: stat['rich'] += 1
    if inputs >= 3: stat['inputs_ge3'] += 1

print('特征统计:', stat)
print('=== C级中含 function calc 的数量(假C候选项，应升B):', len(fake_calc))
for p in fake_calc[:80]:
    print('  ', p)

# 抽样：看几个 fake_calc 的 intro 实际长啥样（为何 has_intro=False）
print('\n=== 抽样 fake_calc 的 intro 段落样式 ===')
for p in fake_calc[:6]:
    c = open(os.path.join(ROOT, 'tools', p), encoding='utf-8').read()
    m = re.search(r'<p[^>]*style="[^"]*"[^>]*>.*?</p>', c, re.S)
    print('---', p)
    print('   intro样例:', (m.group(0)[:160] if m else '无 <p style> 段落'))
