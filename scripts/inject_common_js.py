#!/usr/bin/env python3
"""幂等补注：让所有公开 HTML 页面都引用 /js/common.js。

背景：
- 站点统计已统一收口到 js/analytics.js，js/common.js 会在加载时兜底补引
  analytics.js（见 common.js 内逻辑），因此「引 common.js」即同时获得统计覆盖
  与公共功能（主题/i18n 等）。
- _build.py 已统一处理工具页/行业落地页/首页；本脚本仅补注它不处理的静态页
  （guides/*.html、sitemap.html 等），以及任何遗漏页。
- google 验证文件（google*.html）不动。
- 已含 common.js 或 analytics.js（任意路径形式）的页面跳过，保证幂等。

运行：python3 scripts/inject_common_js.py
"""
import subprocess
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MARKER = '<script src="/js/common.js"></script>\n'

# common.js 一律 defer 加载（避免弱网下阻塞 HTML 解析导致白屏），
# 并在其之前注入 API 兼容桩，收集页面内联脚本的早期 ToolBox.xxx() 调用，
# 待 common.js 就绪后回放。详见 _build.py 的 TOOLBOX_API_STUB 说明。
STUB = (
    '<script>window.__tbq=window.__tbq||[];window.ToolBox=window.ToolBox||{};'
    "['initToolTheme','addToolStyles','showToast','toast','copyText','copyToClipboard',"
    "'copyFromElement','downloadText','injectPrivacyBadge','toggleFavTool','addToRecentTool',"
    "'toggleToolTheme','applyTheme'].forEach(function(k){if(typeof window.ToolBox[k]!=='function')"
    'window.ToolBox[k]=function(){window.__tbq.push([k,[].slice.call(arguments)]);};});</script>'
    '<!-- TOOLBOX-API-STUB -->\n'
)
MARKER = STUB + '<script src="/js/common.js" defer></script>\n'


def main():
    out = subprocess.check_output(['git', 'ls-files', '*.html'], cwd=ROOT, text=True)
    files = [f for f in out.splitlines() if f]

    injected = 0
    skipped_covered = 0
    skipped_google = 0
    for fp in files:
        fn = os.path.basename(fp)
        if fn.startswith('google') and fn.endswith('.html'):
            skipped_google += 1
            continue
        full = os.path.join(ROOT, fp)
        with open(full, 'r', encoding='utf-8') as f:
            content = f.read()
        if 'common.js' in content or 'analytics.js' in content:
            skipped_covered += 1
            continue
        if '</head>' in content:
            content = content.replace('</head>', MARKER + '</head>', 1)
        elif '<head>' in content:
            content = content.replace('<head>', '<head>\n' + MARKER, 1)
        else:
            content = MARKER + content
        with open(full, 'w', encoding='utf-8') as f:
            f.write(content)
        injected += 1

    print('injected=%d skipped_covered=%d skipped_google=%d total=%d'
          % (injected, skipped_covered, skipped_google, len(files)))


if __name__ == '__main__':
    main()
