#!/usr/bin/env python3
"""
B5-04 Tool data-quality gate (cross-page).

Runs after `_build.py`. Enforces that the published tool set has:
  - no duplicate tool titles (B1-07)
  - no duplicate published URLs
  - no broken redirect stubs (B1-05 rename legacy URLs)
  - 100% SEO field coverage (canonical + description + JSON-LD)
  - no orphaned internal tool links
Reports machine-readable summary to _qa_gates.json and exits non-zero on
any blocking violation.

Run: python3 scripts/qa_gates.py
"""
import os, re, sys, json
from collections import defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOOLS_DIR = os.path.join(ROOT, 'tools')
IND_DIR = os.path.join(ROOT, 'json')
SLUG_PATH = os.path.join(ROOT, 'i18n', 'tools', 'slug-en.json')

def parse_toolbox_meta(content):
    m = re.search(r'<meta name="toolbox" content="([^"]+)"', content)
    meta = {}
    if m:
        for pair in m.group(1).split(','):
            if '=' in pair:
                k, v = pair.split('=', 1)
                meta[k.strip()] = v.strip()
    return meta

def collect():
    pages, stubs, links = [], [], defaultdict(set)
    for root, dirs, files in os.walk(TOOLS_DIR):
        for f in files:
            if f == 'index.html' or not f.endswith('.html'):
                continue
            fp = os.path.join(root, f)
            rel = os.path.relpath(fp, ROOT)
            try:
                with open(fp, encoding='utf-8') as fh:
                    c = fh.read()
            except Exception:
                continue
            if 'TOOLBOX-REDIRECT' in c[:300]:
                tgt = None
                mm = re.search(r'location\.href\s*=\s*[\'"]([^\'"]+)[\'"]', c)
                if mm:
                    tgt = mm.group(1)
                else:
                    mm = re.search(r'<a [^>]*href=[\'"]([^\'"]+)[\'"]', c)
                    if mm:
                        tgt = mm.group(1)
                stubs.append({'rel': rel, 'target': tgt})
                continue
            tm = re.search(r'<title>(.+?)\s*-\s*ToolBox\s*</title>', c) or re.search(r'<title>([^<]+)</title>', c)
            title = tm.group(1).strip() if tm else ''
            meta = parse_toolbox_meta(c)
            ind = meta.get('industry') or ''
            dirname = os.path.basename(root)
            url = 'tools/' + os.path.relpath(fp, TOOLS_DIR).replace(os.sep, '/')
            pages.append({
                'rel': rel, 'slug': f, 'title': title, 'ind': ind, 'dir': dirname,
                'url': url,
                'canonical': 'rel="canonical"' in c,
                'desc': 'name="description"' in c,
                'jsonld': ('"@type":"WebApplication"' in c or '"@type":"SoftwareApplication"' in c),
            })
            # internal tool links for orphan check
            for href in re.findall(r'href="([^"]+)"', c):
                if href.startswith('tools/') and href.endswith('.html'):
                    links[url].add(href)
    return pages, stubs, links


def collect_related_tool_keys():
    """Collect normalized keys from json/industry-*.json and report non-standard urls."""
    tool_keys = set()
    bad_urls = []

    for name in sorted(os.listdir(IND_DIR)):
        if not (name.startswith('industry-') and name.endswith('.json')):
            continue
        path = os.path.join(IND_DIR, name)
        try:
            with open(path, encoding='utf-8') as fh:
                data = json.load(fh)
        except Exception:
            continue
        for item in data:
            url = item.get('url')
            if not isinstance(url, str):
                continue
            if not url.startswith('tools/'):
                bad_urls.append(url)
                continue
            if not url.endswith('.html') or url.count('/') != 2:
                bad_urls.append(url)
                continue
            if not re.match(r'^tools/[^/]+/[^/]+\.html$', url):
                bad_urls.append(url)
                continue
            tool_keys.add(url[6:-5])

    return tool_keys, bad_urls

def main():
    pages, stubs, links = collect()
    errors, warns = [], []
    summary = {'total': len(pages), 'stubs': len(stubs)}

    # 1) duplicate titles
    tm = defaultdict(list)
    for p in pages:
        if p['title']:
            tm[p['title']].append(p['url'])
    dup_titles = {t: u for t, u in tm.items() if len(u) > 1}
    if dup_titles:
        for t, u in list(dup_titles.items())[:20]:
            errors.append(f'duplicate title "{t}": {u}')

    # 2) duplicate URLs (path-level, always unique; defensive)
    um = defaultdict(list)
    for p in pages:
        um[p['url']].append(p['rel'])
    dup_urls = {u: r for u, r in um.items() if len(r) > 1}
    for u, r in dup_urls.items():
        errors.append(f'duplicate url {u}: {r}')

    # 3) SEO coverage
    no_canonical = [p['url'] for p in pages if not p['canonical']]
    no_desc = [p['url'] for p in pages if not p['desc']]
    no_jsonld = [p['url'] for p in pages if not p['jsonld']]
    summary['canonical_pct'] = round(100 * (len(pages) - len(no_canonical)) / max(1, len(pages)), 2)
    summary['desc_pct'] = round(100 * (len(pages) - len(no_desc)) / max(1, len(pages)), 2)
    summary['jsonld_pct'] = round(100 * (len(pages) - len(no_jsonld)) / max(1, len(pages)), 2)
    if no_canonical:
        errors.append(f'{len(no_canonical)} pages missing canonical (e.g. {no_canonical[:3]})')
    if no_desc:
        errors.append(f'{len(no_desc)} pages missing description (e.g. {no_desc[:3]})')
    if no_jsonld:
        errors.append(f'{len(no_jsonld)} pages missing JSON-LD (e.g. {no_jsonld[:3]})')

    # 4) broken redirect stubs
    broken = []
    for s in stubs:
        t = s['target']
        if not t:
            broken.append(s['rel'] + ' -> (no target)')
            continue
        if t.startswith('http'):
            continue
        base = os.path.dirname(s['rel'])
        if t.startswith('/'):
            tp = os.path.normpath(os.path.join(ROOT, t.lstrip('/')))
        else:
            tp = os.path.normpath(os.path.join(ROOT, base, t))
        if not os.path.exists(tp):
            broken.append(s['rel'] + ' -> ' + t)
    summary['broken_stubs'] = len(broken)
    if broken:
        for b in broken[:20]:
            errors.append('broken redirect stub: ' + b)

    # 5) industry vs physical directory mismatch (warning, not fatal)
    mism = [p['url'] for p in pages if p['ind'] and p['dir'] and p['ind'] != p['dir']]
    summary['industry_dir_mismatch'] = len(mism)
    for m in mism[:20]:
        warns.append('industry/dir mismatch: ' + m)

    # 6) orphan internal links
    all_urls = set(p['url'] for p in pages)
    orphan = defaultdict(list)
    for src, targets in links.items():
        for tg in targets:
            if tg not in all_urls and not tg.startswith('http'):
                orphan[src].append(tg)
    summary['orphan_links'] = sum(len(v) for v in orphan.values())
    if orphan:
        for src, tg in list(orphan.items())[:20]:
            warns.append(f'orphan link {src} -> {tg[:3]}')

    # 7) related-tools slug mapping consistency (must be one-to-one with slug-en)
    tool_keys, bad_urls = collect_related_tool_keys()
    if os.path.exists(SLUG_PATH):
        try:
            with open(SLUG_PATH, encoding='utf-8') as fh:
                slug = json.load(fh)
            if isinstance(slug, dict):
                slug_keys = set(slug.keys())
            else:
                errors.append(f'invalid slug map format in {SLUG_PATH}, expect JSON object')
                slug_keys = set()
        except Exception as exc:
            errors.append(f'fail to load slug map file {SLUG_PATH}: {exc}')
            slug_keys = set()
    else:
        errors.append(f'missing slug map file {SLUG_PATH}')
        slug_keys = set()

    summary['related_total'] = len(tool_keys)
    summary['slug_keys'] = len(slug_keys)
    missing = sorted(tool_keys - slug_keys)
    extra = sorted(slug_keys - tool_keys)
    summary['related_missing'] = len(missing)
    summary['related_extra'] = len(extra)
    summary['related_bad_urls'] = len(bad_urls)
    if missing:
        for m in missing[:20]:
            errors.append(f'related tool missing in slug map: {m}')
    if extra:
        for e in extra[:20]:
            errors.append(f'slug map has extra key: {e}')
    if bad_urls:
        for b in bad_urls[:20]:
            errors.append(f'non-standard industry-json url: {b}')

    print('=' * 56)
    print('B5-04 Tool data-quality gate')
    print('=' * 56)
    print(f'  tools: {summary["total"]}  redirect stubs: {summary["stubs"]}')
    print(f'  canonical: {summary["canonical_pct"]}%  description: {summary["desc_pct"]}%  JSON-LD: {summary["jsonld_pct"]}%')
    print(f'  duplicate titles: {len(dup_titles)}  broken stubs: {summary["broken_stubs"]}')
    print(f'  industry/dir mismatch: {summary["industry_dir_mismatch"]} (warn)  orphan links: {summary["orphan_links"]} (warn)')
    print('  related map: tools', summary['related_total'], 'slug keys', summary['slug_keys'], 'missing', summary['related_missing'], 'extra', summary['related_extra'], 'bad urls', summary['related_bad_urls'])
    if errors:
        print('\n❌ BLOCKING ERRORS:')
        for e in errors[:40]:
            print('  ' + e)
    if warns:
        print(f'\n⚠️  warnings ({len(warns)}):')
        for w in warns[:20]:
            print('  ' + w)

    json.dump(summary, open(os.path.join(ROOT, '_qa_gates.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=2)

    if errors:
        print('\nFAIL: quality gate blocked')
        return 1
    print('\nPASS: B5-04 quality gate clean')
    return 0

if __name__ == '__main__':
    sys.exit(main())
