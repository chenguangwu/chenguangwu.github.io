#!/usr/bin/env python3
"""幂等注入基线安全 meta（Referrer-Policy / X-Content-Type-Options / Permissions-Policy）。

用法：
    python3 scripts/security_meta.py            # 全站注入（跳过 zh-tw/ 与依赖目录）
    python3 scripts/security_meta.py --check    # 只检查缺失数量，不写文件

规则：
- 已存在 `<!-- TOOLBOX-SECURITY -->` 标记或已同时含两个目标 meta 的页面跳过；
- 仅注入到包含 `</head>` 的 HTML，插入到 `</head>` 之前；
- 重复执行结果一致（幂等）。
"""
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MARKER = '<!-- TOOLBOX-SECURITY -->'
SEC = (
    '<meta http-equiv="Referrer-Policy" content="strict-origin-when-cross-origin">\n'
    '<meta http-equiv="X-Content-Type-Options" content="nosniff">\n'
    '<meta http-equiv="Permissions-Policy" content="camera=(), microphone=(), geolocation=(), interest-cohort=()">\n'
    + MARKER + '\n'
)
SKIP_DIRS = {'.git', 'node_modules', 'zh-tw', '.trae', '.workbuddy'}


def walk_html(root):
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for fn in filenames:
            if fn.endswith('.html'):
                yield os.path.join(dirpath, fn)


def needs_inject(content):
    if MARKER in content:
        return False
    has_rp = 'http-equiv="Referrer-Policy"' in content or "http-equiv='Referrer-Policy'" in content
    has_xcto = 'http-equiv="X-Content-Type-Options"' in content or "http-equiv='X-Content-Type-Options'" in content
    return not (has_rp and has_xcto)


def inject(root=ROOT, check_only=False):
    changed = 0
    missing = 0
    for path in walk_html(root):
        try:
            with open(path, encoding='utf-8') as f:
                content = f.read()
        except (UnicodeDecodeError, OSError):
            continue
        if not needs_inject(content):
            continue
        if '</head>' not in content:
            continue
        missing += 1
        if check_only:
            continue
        content = content.replace('</head>', SEC + '</head>', 1)
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        changed += 1
    return changed, missing


if __name__ == '__main__':
    check_only = '--check' in sys.argv
    changed, missing = inject(check_only=check_only)
    if check_only:
        print('missing=%d' % missing)
    else:
        print('injected=%d' % changed)
