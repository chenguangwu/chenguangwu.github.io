#!/usr/bin/env python3
"""通用单分类八项基线审计（用法: python3 scripts/audit_industry.py --ind energy）

检查项：
1. deep-dive 达标率 (§4.5: 场景≥2 且 示例≥1 且 FAQ≥2 且 无套话)
2. UI 缺项 (common.js/i18n.js/viewport/lang)
3. cat 错标 (industry-realestate.json 中 cat 字段)
4. 英文 p 占位 (首个 <p> 为英文套话) + desc-en/title-en 占位
5. formula 缺口 (计算类=数值输入≥2；纯文本/图像 demo 豁免)
6. 计算验证 (现有门禁覆盖)
7. 指南数
8. 英文态维度 (en/ed/title/desc 占位/代号)
"""
import json, re, os, glob, sys, argparse
from collections import Counter

_ap = argparse.ArgumentParser(description='单分类八项基线审计')
_ap.add_argument('--ind', required=True, help='分类目录名，如 energy')
_args = _ap.parse_args()

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IND = _args.ind
if not os.path.isdir(os.path.join(ROOT, 'tools', IND)):
    sys.exit('错误: tools/%s 不存在' % IND)
TOOLS = os.path.join(ROOT, 'tools', IND)
I18N = os.path.join(ROOT, 'i18n', 'tools')
GUIDES = os.path.join(ROOT, 'guides')

# 英文占位串：模板化英文正文/副标题。已收录 5 种历史形态：
#   <名> is available directly in your browser ...   （-body.json 默认 intro）
#   <名> is a free online tool.                      （旧卡片副标题默认值）
#   Checker 5 - check and validate online, free.     （slu 残留代号 + 兜底句）
#   Generate results online for free and instantly.  （slug-en 默认 ed）
PLACEHOLDER_P = re.compile(
    r'^[A-Za-z0-9][^<>]{0,90}?(?:'
    r'\bis\s+(?:a\s+)?(?:free\s+)?online\s+(?:tool|calculator|generator|converter|checker|simulator)\b'
    r'|\bis available directly in your browser\b'
    r'|\bcheck and validate online\b'
    r'|\bGenerate results online for free\b'
    r')', re.I | re.S)
# 真·代号：slug 残留形态（小写字母-数字），或 "英文词 序号" 占位
CODE_P = re.compile(r'[a-z]+-\d+|\b[A-Za-z]{2,} \d{1,3}\b')
# 套话判定（§4.5）
FP = re.compile(r"统一复核|降低上手门槛|可追溯流程|边界样本建议单独标注|减少重复确认成本|"
                r"标准化，再批量|可复核输出|沿用模板逐项核对|形成标准复核清单|统一口径|"
                r"快速复核|高频复用模板|在.{1,20}(业务|场景)里，优先把.{1,40}标准化后再执行|"
                r"复用模板示例|保留复用模板")
def desc_en_ph(t):
    """desc-en 占位判定。

    注意：本站标准化英文描述后缀含 "Free online tool on ToolBox ..."，不能仅凭
    该串判占位，否则会把已治理的真实描述误报。真占位 = 套话句，或含该串但正文过短。
    """
    t = (t or '').lower()
    if 'generate results online' in t or 'is available directly in your browser' in t:
        return True
    if ('free online tool' in t or 'free tool' in t) and len(t) < 150:
        return True
    return False


def load(p):
    with open(p, encoding='utf-8') as f:
        return json.load(f)


deep = load(os.path.join(I18N, 'content_deepdive.json'))
body = load(os.path.join(I18N, f'{IND}-body.json'))
sjson = load(os.path.join(I18N, f'{IND}.json'))
enov = load(os.path.join(I18N, '_en_override.json'))
ind = load(os.path.join(ROOT, 'json', f'industry-{IND}.json'))

def _is_redirect_stub(path):
    """TOOLBOX-REDIRECT 存根 = 迁移占位，不含工具内容。

    构建（_build.py:1609/1759）与门禁已全链路跳过存根，本审计必须同口径，
    否则重定向页会被当成「deep-dive 缺失 / UI 缺项 / cat 为空」的假缺口。
    """
    try:
        with open(path, encoding='utf-8') as f:
            return 'TOOLBOX-REDIRECT' in f.read(400)
    except Exception:
        return False


tools = sorted(os.path.basename(f)[:-5] for f in glob.glob(os.path.join(TOOLS, '*.html'))
               if os.path.basename(f) != 'index.html' and not _is_redirect_stub(f))
N = len(tools)
print(f"=== {IND} 真实工具数: {N} ===\n")

# ---- 1. deep-dive 达标率 ----
print("【1】deep-dive 达标率 (§4.5: 场景≥2 且 示例≥1 且 FAQ≥2 且 无套话)")
dd_bad = []
dd_s = dd_f = dd_ex = 0
for slug in tools:
    e = deep.get(f'{IND}/{slug}', {})
    sc = e.get('scenarios') or []
    fa = e.get('faqs') or []
    ex = e.get('examples') or []
    dd_s += len(sc); dd_f += len(fa); dd_ex += len(ex)
    has_fp = bool(FP.search(json.dumps(e, ensure_ascii=False)))
    if len(sc) < 2 or len(ex) < 1 or len(fa) < 2 or has_fp:
        dd_bad.append((slug, len(sc), len(ex), len(fa), '套话' if has_fp else ''))
ok = N - len(dd_bad)
print(f"  总 scenarios={dd_s} examples={dd_ex} faqs={dd_f}")
print(f"  §4.5 达标率 = {ok}/{N} ({100*ok/N:.1f}%)  未达标页={len(dd_bad)}")
dist = Counter()
for slug in tools:
    e = deep.get(f'{IND}/{slug}', {})
    dist[(len(e.get('scenarios') or []), len(e.get('faqs') or []))] += 1
print("  (scenarios,faqs) 分布:", dict(dist))
if dd_bad[:15]:
    print("  未达标样例:", dd_bad[:15])

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

# ---- 3. cat 分布 ----
print(f"\n【3】cat 字段分布 (industry-{IND}.json)")
ind_by_file = {e.get('file', '').replace('.html', ''): e for e in ind}
print("  cat 分布:", dict(Counter(e.get('cat') for e in ind)))
cat_bad = [(slug, ind_by_file.get(slug, {}).get('cat')) for slug in tools
           if ind_by_file.get(slug, {}).get('cat') in (0, None, '', '0')]
print(f"  cat 异常(0/None/空)页={len(cat_bad)}")
for x in cat_bad[:10]:
    print("   ", x)

# ---- 4. 英文 p 占位 + desc-en/title-en ----
print("\n【4】英文 p 占位 + desc-en/title-en 占位")
ph_bad = []
desc_en_bad = []
title_en_bad = []
for slug in tools:
    s = open(os.path.join(TOOLS, slug + '.html'), encoding='utf-8').read()
    # 候选：首个 <p>（-body.json 预渲染的英文正文）+ 卡片副标题 <p ... data-zh>（英译副标题）
    _cands = []
    m = re.search(r'<p\b[^>]*>([\s\S]*?)</p>', s, re.I)
    if m:
        _cands.append(m.group(1).strip())
    sm = re.search(r'<p\b[^>]*data-zh="[^"]*"[^>]*>([\s\S]*?)</p>', s, re.I)
    if sm:
        _cands.append(sm.group(1).strip())
    if any(c and PLACEHOLDER_P.match(c) for c in _cands):
        ph_bad.append(slug)
    dm = re.search(r'<meta name="desc-en" content="([^"]*)"', s)
    if dm and desc_en_ph(dm.group(1)):
        desc_en_bad.append((slug, dm.group(1)))
    tm = re.search(r'<meta name="title-en" content="([^"]*)"', s)
    if tm and desc_en_ph(tm.group(1)):
        title_en_bad.append((slug, tm.group(1)))
print(f"  英文 p 占位页={len(ph_bad)}")
print(f"  desc-en 占位页={len(desc_en_bad)}")
print(f"  title-en 占位页={len(title_en_bad)}")
if ph_bad[:15]:
    print("   p 占位样例:", ph_bad[:15])
if desc_en_bad[:8]:
    print("   desc-en 样例:", desc_en_bad[:8])

# ---- 5. formula 缺口 ----
print("\n【5】formula 缺口 (计算类=数值输入≥2；纯文本/图像 demo 豁免)")
fb_missing, fb_exempt = [], []
calc_total = 0
for slug in tools:
    s = open(os.path.join(TOOLS, slug + '.html'), encoding='utf-8').read()
    n_num = len(re.findall(r'<input\b[^>]*type="number"[^>]*>', s))
    if n_num >= 2:
        calc_total += 1
        # 必须按 class 属性匹配：既有页面多用 class="card formula-box"，
        # 直接判 'class="formula-box"' 会把 30 页复合类名误判为缺框（2026-09-14 实证）
        if not re.search(r'class="[^"]*\bformula-box\b[^"]*"', s):
            fb_missing.append(slug)
    else:
        fb_exempt.append(slug)
print(f"  计算类工具={calc_total}  计算类缺框={len(fb_missing)}  豁免(交互 demo)={len(fb_exempt)}")
print(f"  计算类 formula 覆盖率 = {calc_total - len(fb_missing)}/{calc_total}"
      f" ({100*(calc_total-len(fb_missing))/max(calc_total,1):.1f}%)")
if fb_missing[:15]:
    print("  必补样例:", fb_missing[:15])

# ---- 6. 计算验证 ----
print("\n【6】计算验证门禁")
print(f"  现有 verify_*_calc.js 是否覆盖 {IND}:", any(
    IND in os.path.basename(f) for f in glob.glob(os.path.join(ROOT, 'scripts', 'verify_*_calc.js'))))

# ---- 7. 指南 ----
print("\n【7】指南数")
g = [slug for slug in tools if os.path.exists(os.path.join(GUIDES, f'{slug}-guide.html'))]
print(f"  {IND} 指南数={len(g)}")
if g:
    print("  指南 slug:", g)

# ---- 8. 英文态维度 ----
print("\n【8】英文态维度")
b_intro_ph = [k for k, v in body.items() if isinstance(v, dict)
              and PLACEHOLDER_P.match(str(v.get('intro', '')).strip())]
b_title_code = [k for k, v in body.items() if isinstance(v, dict)
                and CODE_P.search(str(v.get('title', '')))]
print(f"  body intro 占位={len(b_intro_ph)}  body title 真·代号/全英文={len(b_title_code)}")
if b_title_code[:12]:
    print("   title 命中样例:", [(k, body[k].get('title')) for k in b_title_code[:12]])

en_total = [k for k in enov if k.startswith(f'{IND}/')]
en_code = [k for k in en_total if CODE_P.search(str(enov.get(k, {}).get('en', '')))]
print(f"  en_override {IND} 总={len(en_total)}  疑似代号 en={len(en_code)}")
if en_code[:12]:
    print("   en 代号样例:", [(k, enov[k].get('en')) for k in en_code[:12]])

sj_missing = [k for k in sjson if not sjson[k].get('en-US')]
print(f"  {IND}.json 缺 en-US={len(sj_missing)}")

ed_bad = [slug for slug in tools
          if (lambda e: not e or len(e) < 30 or 'generate results online' in e)(
              ind_by_file.get(slug, {}).get('ed', ''))]
print(f"  industry ed 不达标(占位/过短)={len(ed_bad)}")
if ed_bad[:12]:
    print("   ed 样例:", ed_bad[:12])

# 孤儿键（body 中存在但全站无对应页面）
all_basenames = {os.path.basename(f)[:-5] for f in glob.glob(os.path.join(ROOT, 'tools', '*', '*.html'))}
orphans = [k for k in body if k not in all_basenames]
print(f"  {IND}-body.json 孤儿键(全站无页面)={len(orphans)}")
if orphans[:12]:
    print("   孤儿键:", orphans[:12])

# 全站性：body 里有键但本分类目录无
bkeys = set(body.keys())
for slug in tools:
    bkeys.discard(slug)
print(f"  {IND}-body.json 中不在本目录但全站有的键={len([k for k in bkeys if k in all_basenames])}")
print("   (示例):", [k for k in bkeys if k in all_basenames][:10])

print("\n=== 审计完成 ===")
