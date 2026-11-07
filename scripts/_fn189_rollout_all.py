# -*- coding: utf-8 -*-
"""F-N189 全站批量铺开（老板 2026-11-08 裁断：一次性铺到全站标准页）。

用法：
  python3 scripts/_fn189_rollout_all.py [--dry] [--only=cat1,cat2] [--limit=N] [--report=path]

处理口径（逐页自动分型）：
  std     旧段归一化 == 标准骨架  → _fn189_rollout.build_standard 整体替换
  custom  旧段有定制差异但四特征齐全 → _fn189_custom_patch.build_custom 8 锚点局部编辑
  abnormal 抽不出参数 / 半修       → 只记录清单，不写盘（下一批逐页处置）
  fixed / none                     → 跳过

安全设计：分两遍——先全站自检（--dry 等价）统计，任一类失败只记清单不中断；
正式写盘时重新构建，`--dry` 不写。所有自检断言沿用单页工具，零重复实现。
"""
import argparse
import collections
import glob
import io
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import _fn189_rollout as R        # noqa: E402
import _fn189_custom_patch as C   # noqa: E402

OLD_FILTER = R.OLD_FILTER
NAN_SIG = 'parseFloat(arr[j].d[rk])'


DOMAIN_TREND_PATS = (re.compile(r'arr\[j\]\.d\.(?!__tbScore)[A-Za-z_]'),
                     re.compile(r"arr\[j\]\.d\['(?!__tbScore)"))


def has_domain_trend(s):
    """页面自研了有业务含义的趋势数值源（CD4/D8 比值、密文字节数、平均分…）。"""
    return any(p.search(s) for p in DOMAIN_TREND_PATS)


def has_old_filter(s):
    """旧过滤行按结构正则判，精确串只覆盖标准形态（变体见 _fn189_custom_patch.OLD_FILTER_PAT）。"""
    return bool(C.OLD_FILTER_PAT.search(s))


def classify(s):
    """返回 (kind, info)。kind ∈ fixed / none / std / custom / abnormal。

    `fixed` 的判定必须同时看「过滤行是否仍吞失败样本」：上一版只看 __tbScore/恒 NaN，
    把「已插 Score 但过滤行仍是变体」的半修页误判成 fixed 跳过（insurance 三页实测）。
    """
    o, nan, fixed = has_old_filter(s), NAN_SIG in s, '__tbScore' in s
    # 自研趋势源页即使还留着 parseFloat(arr[j].d[rk]) 的兜底分支，也不该被改成通用
    # 有效性趋势（会把兜底变成死代码）⇒ 已含 __tbScore 即视为修好。
    if fixed and not o and (not nan or has_domain_trend(s)):
        return 'fixed', None
    if not o and not nan:
        return 'none', None
    info = R.parse_meta(s)
    if info is None:
        return 'abnormal', None
    n = R.norm(info['seg'], info['pre'], info['slug'], info['resexpr'], info['calc'])
    if n == R.STD_OLD_NORM and o and nan:
        return 'std', info
    # 半修页（只有旧过滤或只有恒 NaN）也归 custom：局部编辑按幂等补齐缺失修复点
    if o or nan:
        return 'custom', info
    return 'abnormal', info


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--dry', action='store_true')
    ap.add_argument('--only', default='')
    ap.add_argument('--limit', type=int, default=0)
    ap.add_argument('--report', default='/tmp/fn189_rollout_all_report.txt')
    args = ap.parse_args()
    only = set(x.strip() for x in args.only.split(',') if x.strip())

    t = R.load_template()
    base_new = C.load_base_new_norm()

    files = sorted(glob.glob('tools/**/*.html', recursive=True))
    if only:
        files = [f for f in files if f.split('/')[1] in only]
    if args.limit:
        files = files[:args.limit]

    stat = collections.Counter()
    fails = []
    plans = []
    for f in files:
        s = io.open(f, encoding='utf-8').read()
        kind, info = classify(s)
        stat[kind] += 1
        if kind in ('fixed', 'none'):
            continue
        if kind == 'abnormal':
            fails.append((f, kind, '抽不出标准参数 / 半修'))
            continue
        slug = os.path.basename(f)[:-5]
        try:
            if kind == 'std':
                s2, _ = R.build_standard(s, info, t['tpl'], t['base_norm'], slug)
            else:
                s2, _, _ = C.build_custom(s, info, base_new, slug)
        except Exception as e:  # 断言失败也要继续扫描，最后统一看清单
            fails.append((f, kind, str(e)))
            continue
        plans.append((f, s2))

    lines = []
    lines.append('扫描 %d 页' % len(files))
    for k in ('std', 'custom', 'fixed', 'none', 'abnormal'):
        lines.append('  %-9s %d' % (k, stat[k]))
    lines.append('计划写盘 %d 页；自检失败 %d 页' % (len(plans), len(fails)))
    if fails:
        lines.append('失败 / 异常清单：')
        for f, k, msg in fails:
            lines.append('  [%s] %s %s' % (k, f, msg))
    report = '\n'.join(lines)
    print(report)
    io.open(args.report, 'w', encoding='utf-8').write(report + '\n')
    print('报告已写入 ' + args.report)

    if args.dry:
        return
    ok = 0
    for f, s2 in plans:
        io.open(f, 'w', encoding='utf-8').write(s2)
        ok += 1
    print('APPLY %d 页' % ok)


if __name__ == '__main__':
    main()
