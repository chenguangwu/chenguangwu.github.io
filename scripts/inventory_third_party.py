#!/usr/bin/env python3
"""
B5-08 Third-party dependency inventory.

Scans HTML/JS/CSS for external URLs (anything not on the same origin),
classifies them, detects version pinning, and lists the consuming files.

Categories:
  namespace   - JSON-LD / SVG / schema identifiers, never fetched at runtime
  analytics   - user-tracking / SEO auto-submit scripts
  cdn-script  - executable libraries loaded from a CDN (must be pinned)
  font        - web font CSS loaded on demand
  outbound    - example / placeholder / outbound links in content (not deps)

Run: python3 scripts/inventory_third_party.py
"""
import os, re, json
from urllib.parse import urlparse
from collections import defaultdict

ROOT = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
SELF_HOSTS = {'chenguangwu.github.io', 'localhost', '127.0.0.1', ''}
URL_RE = re.compile(r'https?://[a-zA-Z0-9._:-]+(?:/[^\s"\'`,)>\]]*)?')

# Hosts that are identifiers, not network resources
NAMESPACE_HOSTS = {'schema.org', 'www.w3.org', 'json-schema.org', 'www.w3.org'}
ANALYTICS_HOSTS = {'hm.baidu.com', 'zz.bdstatic.com', 'push.zhanzhang.baidu.com'}
FONT_HOSTS = {'fonts.googleapis.com', 'fonts.gstatic.com'}
CDN_HOSTS = {'cdn.jsdelivr.net', 'cdnjs.cloudflare.com'}

# Known example / placeholder / outbound-link hosts (content only, not deps)
EXAMPLE_HOSTS = {
    'example.com', 'www.example.com', 'api.example.com', 'cdn.example.com',
    'toolbox.example.com', 'www.toolbox.example.com', 'api.com', 'app.com',
    'site.com', 'localhost:3000', 'www.example.com:8080', 'short.link',
    'tinyurl.com', 'api.toolbox.dev', 'toolbox.dev', 'toolbox.521789.xyz',
    'toolbox.1010tools.com', 'toolbox.chenguangwu.com',
}

def classify(host):
    if host in NAMESPACE_HOSTS: return 'namespace'
    if host in ANALYTICS_HOSTS: return 'analytics'
    if host in FONT_HOSTS: return 'font'
    if host in CDN_HOSTS: return 'cdn-script'
    if host in EXAMPLE_HOSTS: return 'outbound'
    return 'other'

def pinned(u):
    # exact version pinned if URL contains @x.y.z or /x.y.z/ with digits
    if re.search(r'@\d+\.\d+(\.\d+)?', u): return True
    if re.search(r'/\d+\.\d+(\.\d+)?/', u): return True
    return False

def scan():
    cats = defaultdict(lambda: {'count': 0, 'hosts': {}})
    for root, dirs, files in os.walk(ROOT):
        parts = root.split(os.sep)
        if 'node_modules' in parts or '.git' in parts:
            continue
        for f in files:
            if not f.endswith(('.html', '.js', '.css')):
                continue
            fp = os.path.join(root, f)
            try:
                c = open(fp, encoding='utf-8', errors='ignore').read()
            except Exception:
                continue
            for m in URL_RE.finditer(c):
                u = m.group(0)
                host = urlparse(u).netloc
                if host in SELF_HOSTS:
                    continue
                cat = classify(host)
                entry = cats[cat]
                entry['count'] += 1
                h = entry['hosts'].setdefault(host, {
                    'count': 0, 'pinned': None, 'sample': u, 'files': set()})
                h['count'] += 1
                h['sample'] = u
                h['files'].add(os.path.relpath(fp, ROOT))
                p = pinned(u)
                if h['pinned'] is None:
                    h['pinned'] = p
                else:
                    h['pinned'] = h['pinned'] and p
    return cats

def main():
    cats = scan()
    print('=' * 60)
    print('B5-08 Third-party resource inventory')
    print('=' * 60)
    summary = {}
    for cat in ['cdn-script', 'analytics', 'font', 'namespace', 'outbound', 'other']:
        if cat not in cats:
            continue
        entry = cats[cat]
        print('\n## %s  (%d refs)' % (cat, entry['count']))
        for host, h in sorted(entry['hosts'].items(), key=lambda x: -x[1]['count']):
            flag = 'pinned' if h['pinned'] else 'UNPINNED'
            print('  %-28s x%-4d [%s]  %d files' % (host, h['count'], flag, len(h['files'])))
            print('      e.g. %s' % h['sample'][:90])
        summary[cat] = {
            'count': entry['count'],
            'hosts': {host: {
                'count': h['count'], 'pinned': bool(h['pinned']),
                'sample': h['sample'], 'files': sorted(h['files'])}
                for host, h in entry['hosts'].items()}
        }
    # Loadable deps = cdn-script + analytics + font
    loadable = sum(cats[c]['count'] for c in ('cdn-script', 'analytics', 'font') if c in cats)
    unpinned_loadable = sum(
        h['count'] for c in ('cdn-script', 'analytics', 'font') if c in cats
        for h in cats[c]['hosts'].values() if not h['pinned'])
    print('\nLoadable third-party refs: %d  (unpinned: %d)' % (loadable, unpinned_loadable))
    json.dump({'summary': {k: v['count'] for k, v in cats.items()}, 'categories': summary},
              open(os.path.join(ROOT, '_third_party_inventory.json'), 'w', encoding='utf-8'),
              ensure_ascii=False, indent=2)
    print('\nReport -> _third_party_inventory.json')

if __name__ == '__main__':
    main()
