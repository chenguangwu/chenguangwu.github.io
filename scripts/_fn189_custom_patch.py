# -*- coding: utf-8 -*-
"""F-N189 定制页局部编辑工具：只替换 8 个修复锚点，逐行保留页面定制逻辑。

用法：
  python3 scripts/_fn189_custom_patch.py --cat=finance --pages=a,b,c [--dry]

背景：`_fn189_rollout.py` 的「整段替换」只适用于归一化后与标准骨架逐字一致的标准页。
定制页在 ResText~Presets 段内插入过前批功能（历史回调重建 / 导出校验 / 结果脱敏等），
整体替换会静默抹掉这些逻辑。本脚本改为 8 处精确小块替换，并用「归一化后相对标准骨架
的增删行集合，替换前后完全一致」证明除了 F-N189 修复外没有动任何其它字节。

自检（全部通过才写盘）：
  - 每个旧锚点在「段内」与「全文」均恰好出现 1 次；
  - 旧段必须含旧过滤正则（防二次替换）、归一化后必须不同于标准骨架（确为定制页）；
  - 新段 __tbScore 恰好 4 处、旧过滤正则消失、Score 函数存在；
  - 定制差异行集合 diff(STD_OLD, old) === diff(BASE_NEW, new)；
  - 新段归一化后仍不同于基准新段（定制仍在）。
"""
import argparse
import difflib
import io
import os
import re
import sys

BASE_CAT = 'finance'
BASE_SLUG = 'cnpj-validator'
OLD_FILTER = "/请输入|无效|不正确|错误|Error|NaN/.test(t)) return '';"
HERE = os.path.dirname(os.path.abspath(__file__))
STD_OLD_NORM = io.open(os.path.join(HERE, '_fn189_std_old_seg_normalized.txt'), encoding='utf-8').read()

# (old, new) —— @@PFN@@ = __<pre>（函数前缀），@@PID@@ = <pre>（DOM id 前缀），@@SLUG@@ = slug
PAIRS = [
    (
        "    if(/请输入|无效|不正确|错误|Error|NaN/.test(t)) return '';\n"
        "    return t.slice(0,80);\n"
        "}\n"
        "function @@PFN@@Time(t){",
        "    if(/^(等待输入|请输入文本|Waiting for input|Please enter text)/.test(t)) return '';\n"
        "    return t.slice(0,80);\n"
        "}\n"
        "function @@PFN@@Score(t){\n"
        "    var s=String(t||'');\n"
        "    if(/[❌]|⚠️|⚠|无效|未通过|不正确|失败|错误|Invalid|Failed|must be|Please enter|请输入|Waiting/i.test(s)) return 0;\n"
        "    return 1;\n"
        "}\n"
        "function @@PFN@@Time(t){",
    ),
    (
        "        var head=[en?'Time':'时间'].concat(keys).concat([rk]);",
        "        var head=[en?'Time':'时间'].concat(keys).concat([en?'Verdict':'结论',rk]);",
    ),
    (
        "            for(var i=0;i<keys.length;i++){var v=it.d[keys[i]];row.push(v==null?'':v);}\n"
        "            var r=it.d[rk];row.push(r==null?'':r);",
        "            for(var i=0;i<keys.length;i++){var v=it.d[keys[i]];row.push(v==null?'':v);}\n"
        "            var sc=parseFloat(it.d.__tbScore);\n"
        "            row.push(isFinite(sc)?(sc>=1?(en?'Pass':'通过'):(en?'Fail':'未通过')):'-');\n"
        "            var r=it.d[rk];row.push(r==null?'':r);",
    ),
    (
        "                    if(k===rk) continue;",
        "                    if(k===rk||k==='__tbScore') continue;",
    ),
    (
        "            var v=parseFloat(arr[j].d[rk]);",
        "            var v=parseFloat(arr[j].d.__tbScore);",
    ),
    (
        "name:en?'Result trend':'结果趋势'",
        "name:en?'Validity trend':'有效性趋势'",
    ),
    (
        "    TBKit.history.record(rec);",
        "    rec.__tbScore=@@PFN@@Score(res);\n    TBKit.history.record(rec);",
    ),
    (
        "    try { TBKit.util.exportTable('#@@PID@@Table','@@SLUG@@.csv'); } catch(e){}",
        "    try{\n"
        "        var box=document.querySelector('#@@PID@@Table');\n"
        "        if(!box||!box.querySelector('tr')){\n"
        "            var snap=@@PFN@@Snap(); var keys=Object.keys(snap);\n"
        "            if(keys.length>12) keys=keys.slice(0,12);\n"
        "            var en=(TBKit.util&&TBKit.util.isEn())?true:false;\n"
        "            @@PFN@@Render(keys,en?'Result':'结果',en);\n"
        "        }\n"
        "    }catch(e){}\n"
        "    try { TBKit.util.exportTable('#@@PID@@Table','@@SLUG@@.csv'); } catch(e){}",
    ),
]


def seg_bounds(s, pre):
    a = s.find('function __%sResText()' % pre)
    b = s.find('function __%sPresets()' % pre)
    return (a, b, s[a:b]) if a >= 0 and b > a else (-1, -1, '')


def parse_meta(s):
    m = re.search(r"exportTable\('#([^']+)Table','([^']+)\.csv'\)", s)
    if not m:
        return None
    pre, slug = m.group(1), m.group(2)
    a, b, seg = seg_bounds(s, pre)
    if a < 0:
        return None
    rm = re.search(r'var r=(document\.(?:getElementById|querySelector)\([^)]*\));', seg)
    cm = re.search(r'\n\s{16}([A-Za-z_][A-Za-z0-9_]*)\(\);', seg)
    if not (rm and cm):
        return None
    return dict(pre=pre, slug=slug, a=a, b=b, seg=seg,
                resexpr=rm.group(1), calc=cm.group(1))


def norm(seg, pre, slug, resexpr, calc):
    return (seg.replace('__' + pre + '_', '__X_')
               .replace('__' + pre, '__X')
               .replace('#' + pre, '#X')
               .replace("'" + slug + ".csv'", "'X.csv'")
               .replace(resexpr, 'RESEXPR')
               .replace('                ' + calc + '();', '                CALC();'))


def diff_lines(a, b):
    """统一 diff 中的增删行（不含文件头），用于证明定制差异行集合未变。"""
    return [l for l in difflib.unified_diff(a.splitlines(), b.splitlines(), lineterm='', n=1)
            if l[:1] in ('+', '-') and not l.startswith(('+++', '---'))]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--cat', default='finance')
    ap.add_argument('--pages', required=True)
    ap.add_argument('--dry', action='store_true')
    args = ap.parse_args()
    slugs = [x.strip() for x in args.pages.split(',') if x.strip()]

    # 基准页（已修新实现）→ 基准新段归一化
    bs = io.open('tools/%s/%s.html' % (BASE_CAT, BASE_SLUG), encoding='utf-8').read()
    binfo = parse_meta(bs)
    assert binfo and '__tbScore' in binfo['seg'], '基准页必须是已修新实现'
    BASE_NEW_NORM = norm(binfo['seg'], binfo['pre'], binfo['slug'], binfo['resexpr'], binfo['calc'])
    assert len(BASE_NEW_NORM) > 2000 and '__tbScore' in BASE_NEW_NORM

    plans = []
    for slug in slugs:
        f = 'tools/%s/%s.html' % (args.cat, slug)
        if not os.path.exists(f):
            print('FAIL %-28s 页面不存在' % slug); sys.exit(1)
        s = io.open(f, encoding='utf-8').read()
        info = parse_meta(s)
        if not info:
            print('FAIL %-28s 抽不到标准参数' % slug); sys.exit(1)
        pre, old_seg = info['pre'], info['seg']
        assert info['slug'] == slug, slug + ' csv 名与 slug 不一致'
        assert s.count('function __%sResText()' % pre) == 1, slug + ' 起始标记不唯一'
        assert s.count('function __%sPresets()' % pre) == 1, slug + ' 结束标记不唯一'
        assert OLD_FILTER in old_seg, slug + ' 不是旧模板（已修或二次替换）'
        assert 'parseFloat(arr[j].d[rk])' in old_seg, slug + ' 旧段缺恒 NaN 图表特征'

        old_norm = norm(old_seg, pre, slug, info['resexpr'], info['calc'])
        assert old_norm != STD_OLD_NORM, slug + ' 是标准页，请用 _fn189_rollout.py'
        custom_diff = diff_lines(STD_OLD_NORM, old_norm)
        assert custom_diff, slug + ' 与标准骨架无差异，异常'

        seg = old_seg
        for i, (old, new) in enumerate(PAIRS):
            old = (old.replace('@@PFN@@', '__' + pre)
                      .replace('@@PID@@', pre).replace('@@SLUG@@', slug))
            new = (new.replace('@@PFN@@', '__' + pre)
                      .replace('@@PID@@', pre).replace('@@SLUG@@', slug))
            assert seg.count(old) == 1, '%s 第 %d 处锚点在段内不唯一 (%d)' % (slug, i + 1, seg.count(old))
            assert s.count(old) == 1, '%s 第 %d 处锚点在全文不唯一 (%d)' % (slug, i + 1, s.count(old))
            seg = seg.replace(old, new, 1)

        new_norm = norm(seg, pre, slug, info['resexpr'], info['calc'])
        assert seg.count('__tbScore') == 4, slug + ' __tbScore 数量异常: %d' % seg.count('__tbScore')
        assert OLD_FILTER not in seg, slug + ' 旧过滤正则仍在'
        assert 'function __%sScore(t)' % pre in seg, slug + ' Score 函数缺失'
        assert diff_lines(BASE_NEW_NORM, new_norm) == custom_diff, \
            slug + ' 定制差异行集合变化（定制逻辑被改动）\n  OLD: %r\n  NEW: %r' % (
                custom_diff, diff_lines(BASE_NEW_NORM, new_norm))
        assert new_norm != BASE_NEW_NORM, slug + ' 定制逻辑丢失（与基准新段同构）'

        s2 = s[:info['a']] + seg + s[info['b']:]
        plans.append((slug, f, s2, len(old_seg), len(seg), len(custom_diff)))
        print('CHECK %-28s 定制差异 %d 行 %d -> %d chars' % (slug, len(custom_diff), len(old_seg), len(seg)))

    print('自检通过 %d/%d 页%s' % (len(plans), len(slugs), '（--dry 不写盘）' if args.dry else ''))
    if args.dry:
        return
    for slug, f, s2, olen, nlen, _ in plans:
        io.open(f, 'w', encoding='utf-8').write(s2)
        print('APPLY %-28s %d -> %d chars' % (slug, olen, nlen))


if __name__ == '__main__':
    main()
