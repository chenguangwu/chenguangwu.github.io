#!/usr/bin/env python3
"""通用单分类「英文态根治」脚本（A+B 批次一次成型）。

用法： python3 scripts/fix_industry_body_i18n.py --ind energy

数据源： scripts/enmap/<ind>.json
  {
    "_meta": {"label": "Energy", "orphans": ["slug-1", ...]},
    "<slug>": {"name": "Real English Name", "intro": "Real English description.", "cat": "calculator"}
  }

A 批次（四端数据源同步）：
  i18n/tools/<ind>-body.json          title/h1/intro + en 嵌套
  i18n/tools/<ind>.json               每个 slug 的 en-US
  i18n/tools/_en_override.json        '<ind>/<slug>' -> {en, ed, ind}
  json/industry-<ind>.json            en / ed（+ cat 修正，仅当 map 给出 cat 且与原值不同）
  孤儿键（_meta.orphans）从 body / <ind>.json / _en_override 中清除

B 批次（页面静态英文同步，绕过 _build.py 非 CJK 占位页英文未注入缺陷）：
  meta title-en / meta desc-en / h2 内文（保留 icon 前缀与 data-zh）/
  muted <p> 内文（保留 data-zh）

保持各文件原有缩进：body 与 <ind>.json 用 2；_en_override 与 industry-<ind> 用 1。
"""
import json, os, re, sys, argparse

_ap = argparse.ArgumentParser(description='单分类英文态根治（A+B 批次）')
_ap.add_argument('--ind', required=True, help='分类目录名，如 energy')
_ap.add_argument('--apply', action='store_true', help='落盘（默认 dry-run 只统计）')
_a = _ap.parse_args()

IND = _a.ind
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
I18N = os.path.join(ROOT, 'i18n', 'tools')
JSONDIR = os.path.join(ROOT, 'json')
TOOLS = os.path.join(ROOT, 'tools', IND)
MAPF = os.path.join(ROOT, 'scripts', 'enmap', IND + '.json')

if not os.path.isdir(TOOLS):
    sys.exit('错误: tools/%s 不存在' % IND)
if not os.path.isfile(MAPF):
    sys.exit('错误: 缺少数据文件 %s' % os.path.relpath(MAPF, ROOT))

raw = json.load(open(MAPF, encoding='utf-8'))
META = raw.pop('_meta', {})
LABEL = META.get('label', IND.capitalize())
# orphans: 全站无对应页面的键；cross: 页面在本分类之外（其归属分类 body 已覆盖）的残留键
ORPHANS = META.get('orphans', [])
CROSS = META.get('cross', [])
EN_MAP = {k: v for k, v in raw.items()}
SUF = (" Free online tool on ToolBox — 100% client-side, no data uploaded, no install. "
       "Part of the " + LABEL + " tools.")


def esc_html(s):
    return str(s).replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')


def esc_attr(s):
    return esc_html(s).replace('"', '&quot;')


def load(p):
    with open(p, encoding='utf-8') as f:
        return json.load(f)


body = load(os.path.join(I18N, '%s-body.json' % IND))
sj = load(os.path.join(I18N, '%s.json' % IND))
enov = load(os.path.join(I18N, '_en_override.json'))
ind = load(os.path.join(JSONDIR, 'industry-%s.json' % IND))
ind_by_file = {e.get('file', '').replace('.html', ''): e for e in ind}

pages = sorted(os.path.basename(f)[:-5] for f in os.listdir(TOOLS)
               if f.endswith('.html') and f != 'index.html')

# 覆盖率自检
missing = [s for s in pages if s not in EN_MAP]
extra = [s for s in EN_MAP if s not in pages]
print('=== %s 英文映射自检 ===' % IND)
print('  页面数=%d  映射条目=%d  未覆盖=%d  多余(无页面)=%d' % (len(pages), len(EN_MAP), len(missing), len(extra)))
if missing:
    print('  未覆盖:', missing)
if extra:
    print('  多余:', extra)

# ---- A：四端数据源 ----
n_new = n_cat = 0
for slug, v in EN_MAP.items():
    name, intro = v['name'], v['intro']
    created = slug not in body
    body[slug] = {"title": name, "intro": intro, "h1": name,
                  "en": {"title": name, "h1": name, "intro": intro}}
    e = sj.setdefault(slug, {})
    e['en-US'] = {"title": name, "h1": name, "intro": intro}
    sj[slug] = e
    ed = name + ". " + intro + SUF
    enov['%s/%s' % (IND, slug)] = {"en": name, "ed": ed, "ind": IND}
    it = ind_by_file.get(slug)
    if it is not None:
        it['en'] = name
        it['ed'] = ed
        if v.get('cat') and it.get('cat') != v['cat']:
            it['cat'] = v['cat']
            n_cat += 1
    if created:
        n_new += 1

removed, cross_removed = [], []
for k in ORPHANS + CROSS:
    if k in body:
        del body[k]
        (removed if k in ORPHANS else cross_removed).append(k)
    if k in sj:
        del sj[k]
    ek = '%s/%s' % (IND, k)
    if ek in enov:
        del enov[ek]

print('\n=== A 批次 ===')
print('  写入真实英文 %d 条（新建键 %d），cat 修正 %d，清孤儿键 %d%s'
      % (len(EN_MAP), n_new, n_cat, len(removed), (': ' + ', '.join(removed)) if removed else ''))
print('  清跨分类残留键 %d%s' % (len(cross_removed),
                           (': ' + ', '.join(cross_removed)) if cross_removed else ''))

# ---- B：页面静态英文 ----
n_title = n_desc = n_h2 = n_p = 0
for slug, v in EN_MAP.items():
    fp = os.path.join(TOOLS, slug + '.html')
    if not os.path.exists(fp):
        continue
    s = open(fp, encoding='utf-8').read()
    name, intro = v['name'], v['intro']
    ed = name + ". " + intro + SUF

    s2 = re.sub(r'(<meta\b[^>]*\bname="title-en"[^>]*\bcontent=")[^"]*(")',
                lambda m: m.group(1) + esc_attr(name) + m.group(2), s, count=1)
    n_title += (s2 != s); s = s2

    s2 = re.sub(r'(<meta\b[^>]*\bname="desc-en"[^>]*\bcontent=")[^"]*(")',
                lambda m: m.group(1) + esc_attr(ed) + m.group(2), s, count=1)
    n_desc += (s2 != s); s = s2

    def _h2(m):
        open_tag, inner, close = m.group(1), m.group(2), m.group(3)
        mm = re.match(r'^([^\u4e00-\u9fffA-Za-z0-9]*)([\s\S]*)$', inner)
        icon = mm.group(1) if mm else ''
        return '%s%s%s' % (open_tag, esc_html(icon + name), close)
    s2 = re.sub(r'(<h2\b[^>]*data-zh="[^"]*">)([\s\S]*?)(</h2>)', _h2, s, count=1)
    n_h2 += (s2 != s); s = s2

    # 占位 <p> 有两种形态：muted 样式段 / class="calc-desc" 段；命中其一即替换（幂等）
    for pat in (r'(<p\s+style="font-size:13px;color:var\(--text-muted\)[^"]*"[^>]*>)([\s\S]*?)(</p>)',
                r'(<p\s+class="calc-desc"[^>]*>)([\s\S]*?)(</p>)'):
        s2 = re.sub(pat, lambda m: m.group(1) + esc_html(intro) + m.group(3), s, count=1)
        if s2 != s:
            n_p += 1
            s = s2
            break

    if _a.apply:
        with open(fp, 'w', encoding='utf-8') as f:
            f.write(s)

print('\n=== B 批次（页面静态英文）===')
print('  title-en=%d  desc-en=%d  h2=%d  p=%d  （共 %d 页）' % (n_title, n_desc, n_h2, n_p, len(EN_MAP)))

if _a.apply:
    def dump(p, obj, indt):
        with open(p, 'w', encoding='utf-8') as f:
            json.dump(obj, f, ensure_ascii=False, indent=indt)
            f.write('\n')
    dump(os.path.join(I18N, '%s-body.json' % IND), body, 2)
    dump(os.path.join(I18N, '%s.json' % IND), sj, 2)
    dump(os.path.join(I18N, '_en_override.json'), enov, 1)
    dump(os.path.join(JSONDIR, 'industry-%s.json' % IND), ind, 1)
    print('\n已落盘（--apply）')
else:
    print('\nDRY-RUN：未写任何文件，加 --apply 落盘')
