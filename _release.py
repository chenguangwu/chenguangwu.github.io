#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ToolBox 一键发布流水线（质量闭环收口）

串联：构建 → 静态门禁 → 死链门禁 → 资产门禁 → 发布看板。
任一门禁失败即中止并返回非 0 退出码（可作为 CI / 发布前 gate）。

链路：
  1. python3 _build.py                 重建索引 / sitemap / SEO 注入（幂等）
  2. python3 _test_static.py           静态合规（0 失败 0 告警）
  3. python3 _audit_links.py --check   死链门禁（0 死链）
  4. python3 _audit_assets.py --check  资产门禁（0 死链 / 0 lang缺失 / 0 重复id）
  5. python3 _release_dashboard.py     生成发布看板（只读快照，不阻断）

用法：
  python3 _release.py            # 完整链路（含构建）
  python3 _release.py --no-build # 跳过构建，仅跑门禁+看板（适合未改源码时快速校验）
  python3 _release.py --quiet    # 精简输出

退出码：0=全部通过；1=某门禁失败；2=运行异常。
"""

import os
import sys
import json
import subprocess

ROOT = os.path.abspath(os.path.dirname(os.path.abspath(__file__)))
PY = sys.executable


def run(step, args, quiet=False):
    label, cmd = args
    print('\n' + '=' * 64)
    print('[%s] %s' % (step, label))
    print('=' * 64)
    rc = subprocess.run([PY] + cmd, cwd=ROOT).returncode
    return rc


def check_static():
    """读取 _test_report_static.json，失败返回非 0。"""
    p = os.path.join(ROOT, '_test_report_static.json')
    if not os.path.exists(p):
        print('  ✗ 未找到静态测试报告，请先运行 _test_static.py')
        return 1
    d = json.load(open(p, encoding='utf-8'))
    total = d.get('total', 0)
    passed = d.get('passed', 0)
    warnings = d.get('warnings', 0)
    errors = d.get('errors', 0) or 0
    err_list = d.get('errors', [])
    n_err = len(err_list) if isinstance(err_list, list) else errors
    print('  通过 %s/%s · 告警 %s · 失败 %s' % (passed, total, warnings, n_err))
    if warnings or n_err or passed < total:
        print('  ✗ 静态门禁未通过')
        return 1
    print('  ✓ 静态门禁通过')
    return 0


def main():
    quiet = '--quiet' in sys.argv
    skip_build = '--no-build' in sys.argv

    steps = []
    if not skip_build:
        steps.append(('构建索引 / sitemap / SEO 注入', ['_build.py']))
    steps.append(('静态合规门禁', ['_test_static.py']))
    steps.append(('死链门禁', ['_audit_links.py', '--check'] + (['--quiet'] if quiet else [])))
    steps.append(('资产完整性门禁', ['_audit_assets.py', '--check'] + (['--quiet'] if quiet else [])))
    steps.append(('生成发布看板（不阻断）', ['_release_dashboard.py']))

    print('# ToolBox 发布流水线')
    print('# 步骤：' + ' → '.join(s[0] for s in steps))

    for i, (label, cmd) in enumerate(steps, 1):
        # 静态门禁用 JSON 解析判断，其余用子进程退出码
        if cmd[0] == '_test_static.py':
            print('\n' + '=' * 64)
            print('[%d] %s' % (i, label))
            print('=' * 64)
            rc = subprocess.run([PY] + cmd, cwd=ROOT).returncode
            rc = check_static()  # 以 JSON 为准
        else:
            rc = run(str(i), (label, cmd), quiet)
        if rc != 0:
            print('\n✗ 发布流水线在「%s」失败（exit %d）。中止。' % (label, rc))
            return 1

    print('\n' + '#' * 64)
    print('# ✅ 发布流水线全部通过：构建 / 静态 / 死链 / 资产 / 看板')
    print('#' * 64)
    snap = os.path.join(ROOT, 'release_snapshot.json')
    if os.path.exists(snap):
        try:
            d = json.load(open(snap, encoding='utf-8'))
            print('# 看板摘要：工具 %s · 静态 %s · 死链 %s · 资产 %s' % (
                d.get('tools', {}).get('total', '-'),
                d.get('static', {}).get('verdict', '-'),
                d.get('links', {}).get('verdict', '-'),
                d.get('assets', {}).get('verdict', '-')))
        except Exception:
            pass
    print('# 看板文件：release_dashboard.html')
    return 0


if __name__ == '__main__':
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print('\n中断')
        sys.exit(130)
    except Exception as e:
        print('运行异常：%s' % e)
        sys.exit(2)
