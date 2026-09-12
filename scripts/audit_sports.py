#!/usr/bin/env python3
"""sports (75) 八项基线审计：
1. deep-dive 条数 (scenarios/faqs)
2. UI 缺项 (common.js/i18n.js/viewport/lang/toolbox)
3. cat 错标 (industry-sports.json 中 cat 字段)
4. 英文 p 占位 (首个 <p> 为英文套话)
5. formula 缺口 (formula-box 缺失)
6. 计算验证 (现有门禁覆盖)
7. 指南数
8. 英文态维度 (en/ed/title/desc 占位/代号)
"""
import json, re, os, glob

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOOLS = os.path.join(ROOT, 'tools', 'sports')
I18N = os.path.join(ROOT, 'i18n', 'tools')
GUIDES = os.path.join(ROOT, 'guides')

PLACEHOLDER_P = re.compile(
    r'^[A-Za-z0-9][\w \-\'’\.]* is available directly in your browser', re.I)

def load(p):
    with open(p, encoding='utf-8') as f:
        return json.load(f)

# 数据源
deep = load(os.path.join(I18N, 'content_deepdive.json'))
body = load(os.path.join(I18N, 'sports-body.json'))
sjson = load(os.path.join(I18N, 'sports.json'))
enov = load(os.path.join(I18N, '_en_override.json'))
ind = load(os.path.join(ROOT, 'json', 'industry-sports.json'))

# 真实工具 slug
tools = sorted(os.path.basename(f)[:-5] for f in glob.glob(os.path.join(TOOLS, '*.html'))
               if not f.endswith('index.html'))
N = len(tools)
print(f"=== 真实工具数: {N} ===\n")

# ---- 1. deep-dive 达标率 (§4.5: 场景≥2 且 示例≥1 且 FAQ≥2 且 无套话) ----
print("【1】deep-dive 达标率 (§4.5: 场景≥2 且 示例≥1 且 FAQ≥2 且 无套话)")
FP = re.compile(r"统一复核|降低上手门槛|可追溯流程|边界样本建议单独标注|减少重复确认成本|"
                r"标准化，再批量|可复核输出|沿用模板逐项核对|形成标准复核清单|统一口径|"
                r"快速复核|高频复用模板|在.{1,20}(业务|场景)里，优先把.{1,40}标准化后再执行|"
                r"复用模板示例|保留复用模板")
dd_bad = []
dd_total_s = dd_total_f = dd_total_ex = 0
for slug in tools:
    e = deep.get(f'sports/{slug}', {})
    sc = e.get('scenarios') or []
    fa = e.get('faqs') or []
    ex = e.get('examples') or []
    dd_total_s += len(sc); dd_total_f += len(fa); dd_total_ex += len(ex)
    has_fp = bool(FP.search(json.dumps(e, ensure_ascii=False)))
    if len(sc) < 2 or len(ex) < 1 or len(fa) < 2 or has_fp:
        dd_bad.append((slug, len(sc), len(ex), len(fa), '套话' if has_fp else ''))
ok = N - len(dd_bad)
print(f"  总 scenarios={dd_total_s} examples={dd_total_ex} faqs={dd_total_f}")
print(f"  §4.5 达标率 = {ok}/{N} ({100*ok/N:.1f}%)  未达标页={len(dd_bad)}")
if dd_bad[:10]:
    print("  样例(未达标):", dd_bad[:10])

# ---- 2. UI 缺项 ----
print("\n【2】UI 缺项 (common.js/i18n.js/viewport/lang)")
ui_bad = []
for slug in tools:
    s = open(os.path.join(TOOLS, slug + '.html'), encoding='utf-8').read()
    miss = []
    if 'common.js' not in s: miss.append('common.js')
    if 'i18n.js' not in s: miss.append('i18n.js')
    if 'viewport' not in s.lower(): miss.append('viewport')
    if 'lang=' not in s: miss.append('lang')
    if miss:
        ui_bad.append((slug, miss))
print(f"  缺项页={len(ui_bad)}")
for x in ui_bad[:10]:
    print("   ", x)

# ---- 3. cat 错标 ----
print("\n【3】cat 字段分布 (industry-sports.json)")
# ind 是 list，按 file 建索引
ind_by_file = {e.get('file', '').replace('.html', ''): e for e in ind}
from collections import Counter
cat_dist = Counter(e.get('cat') for e in ind)
print("  cat 分布:", dict(cat_dist))
cat_bad = [(slug, ind_by_file.get(slug, {}).get('cat')) for slug in tools
           if ind_by_file.get(slug, {}).get('cat') in (0, None, '', '0')]
print(f"  cat 异常(0/None/空)页={len(cat_bad)}")
for x in cat_bad[:10]:
    print("   ", x)

# ---- 4. 英文 p 占位 ----
print("\n【4】英文 p 占位 (首个 <p> 为英文套话)")
ph_bad = []
for slug in tools:
    s = open(os.path.join(TOOLS, slug + '.html'), encoding='utf-8').read()
    m = re.search(r'<p\b[^>]*>([\s\S]*?)</p>', s, re.I)
    if m and PLACEHOLDER_P.match(m.group(1).strip()):
        ph_bad.append(slug)
print(f"  英文 p 占位页={len(ph_bad)}")
if ph_bad[:12]:
    print("  样例:", ph_bad[:12])

# ---- 5. formula 缺口 ----
print("\n【5】formula 缺口 (formula-box 缺失)")
fb_missing = []
for slug in tools:
    s = open(os.path.join(TOOLS, slug + '.html'), encoding='utf-8').read()
    if 'class="formula-box"' not in s:
        fb_missing.append(slug)
print(f"  无 formula-box 页={len(fb_missing)}")
if fb_missing[:15]:
    print("  样例:", fb_missing[:15])

# ---- 6. 计算验证 ----
print("\n【6】计算验证门禁")
print("  现有 verify_*_calc.js 是否覆盖 sports:", any(
    'sports' in f for f in glob.glob(os.path.join(ROOT, 'scripts', 'verify_*_calc.js'))))

# ---- 7. 指南 ----
print("\n【7】指南数")
# 指南命名 = {slug}-guide.html（与 science 一致），按 sports slug 逐页判定存在性
g = [slug for slug in tools if os.path.exists(os.path.join(GUIDES, f'{slug}-guide.html'))]
print(f"  sports 指南数={len(g)}")
print("  指南 slug:", g)

# ---- 8. 英文态维度 ----
print("\n【8】英文态维度")
# 8a. sports-body.json intro 占位 / title 真·代号（slug 残留：小写字母-数字 或 "名称 序号" 占位）
b_intro_ph = [k for k, v in body.items() if isinstance(v, dict) and PLACEHOLDER_P.match(str(v.get('intro', '')).strip())]
b_title_code = [k for k, v in body.items() if isinstance(v, dict)
               and re.search(r'[a-z]+-\d+|\b[A-Za-z]{2,} \d{1,3}\b', str(v.get('title', '')))]
print(f"  body intro 占位={len(b_intro_ph)}  body title 真·代号={len(b_title_code)}")
# 8b. en_override en 代号 (含 Generator/Calculator/带数字)
en_code = [k for k, v in enov.items() if k.startswith('sports/') and re.search(r'(Generator|Calculator|Random|Calc|Test|Rater|Analysis|Estimate|Tester|Detector|Simulator|Convert|Ratio|Speed|Time|Stats|Sports|Yang|Zhan|You|Tri|She|Rou|Pin|Lan|Jix|Jia|Hong|Dian|Climb|Baof|Ass|Alt|Wang|Xue|Yum|Tent|Sleep|She)[\s\-]?\d', str(v.get('en','')))]
en_total = [k for k in enov if k.startswith('sports/')]
print(f"  en_override sports 总={len(en_total)}  疑似代号 en={len(en_code)}")
if en_code[:12]:
    print("   代号样例:", en_code[:12])
# 8c. sports.json en-US 套话/缺
sj_en_missing = [k for k in sjson if not sjson[k].get('en-US')]
print(f"  sports.json 缺 en-US={len(sj_en_missing)}")
# 8d. industry ed 不达标
ed_bad = []
for slug in tools:
    e = ind_by_file.get(slug, {})
    ed = e.get('ed', '')
    if not ed or len(ed) < 30 or 'generate results online' in ed:
        ed_bad.append(slug)
print(f"  industry ed 不达标(占位/过短)={len(ed_bad)}")
if ed_bad[:12]:
    print("   样例:", ed_bad[:12])

print("\n=== 审计完成 ===")
