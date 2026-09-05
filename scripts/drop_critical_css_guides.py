#!/usr/bin/env python3
"""移除 guides/ 静态页中冗余的 critical-css 内联块。

背景（2026-09-05 实测）：
scripts/critical_tool_css.txt 的 178 条选择器 100% 被 css/common.css +
css/nav-menu.css 覆盖，零条独有。_build.py 的 _css_nonblocking() 只把
nav-menu.css 改为非阻塞，common.css 保持阻塞，首次渲染前必生效，因此
凡已引用 common.css 的页面，内联的 critical-css 是纯冗余。

_build.py 的 fix_tool_pages_seo() 只处理 tools/ 下的页面，guides/ 静态页
不在其列，故由本脚本单独清理。脚本幂等：已清理的页面再次运行不产生变化。

用法:
    python3 scripts/drop_critical_css_guides.py          # 实际执行
    python3 scripts/drop_critical_css_guides.py --dry-run  # 只报告不改
"""

import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GUIDES_DIR = os.path.join(ROOT, 'guides')
CRIT_RE = re.compile(r'<style id="critical-css">[\s\S]*?</style>\s*')


def main():
    dry_run = '--dry-run' in sys.argv
    if not os.path.isdir(GUIDES_DIR):
        print('guides/ 目录不存在，跳过')
        return 0

    changed = 0
    skipped_no_common = 0
    saved_bytes = 0

    for name in sorted(os.listdir(GUIDES_DIR)):
        if not name.endswith('.html'):
            continue
        path = os.path.join(GUIDES_DIR, name)
        with open(path, encoding='utf-8') as f:
            content = f.read()

        match = CRIT_RE.search(content)
        if not match:
            continue
        # 未引用 common.css 的页面保留内联兜底，与 _build.py 的判定保持一致
        if 'common.css' not in content:
            skipped_no_common += 1
            continue

        new_content = CRIT_RE.sub('', content, count=1)
        saved_bytes += len(content) - len(new_content)
        changed += 1
        if not dry_run:
            with open(path, 'w', encoding='utf-8') as f:
                f.write(new_content)

    prefix = '[dry-run] ' if dry_run else ''
    print('%sguides critical-css 清理: %d 个页面, 节省 %.1f KB, 跳过(无 common.css) %d 个'
          % (prefix, changed, saved_bytes / 1024, skipped_no_common))
    return 0


if __name__ == '__main__':
    sys.exit(main())
