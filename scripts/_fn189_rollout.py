# -*- coding: utf-8 -*-
"""F-N189 全站铺开工具：把已修基准页的新 Extras 段按「参数自适应」套到指定旧模板页。

用法：
  python3 scripts/_fn189_rollout.py --cat=finance --pages=a,b,c [--dry]

- 基准页恒为 tools/finance/cnpj-validator.html（第 40 批首修、新实现单一真源）。
- 每页自动抽取：函数/DOM id 前缀、结果容器整段表达式、计算函数名、csv 名。
- 只处理「旧模板标准页」：写入前逐项自检，任一不通过即整批中止（不落盘脏文件）。
- 定制页（归一化后与 scripts/_fn189_std_old_seg_normalized.txt 不同）会被明确拒绝，
  须走「保留定制的局部编辑」脚本 scripts/_fn189_custom_patch.py。
- --dry 只检查不写，供分型复核。

核心逻辑（load_template / build_standard）为模块级函数，供 scripts/_fn189_rollout_all.py 复用。
"""
import argparse
import io
import os
import re
import sys

BASE_CAT = 'finance'
BASE_SLUG = 'cnpj-validator'
OLD_FILTER = "/请输入|无效|不正确|错误|Error|NaN/.test(t)) return '';"
# 标准旧段（ResText~Presets）5 参数归一化骨架，取自第 44 批 HEAD 的 capm-return
# （cpf-validator / credit-card-type 逐字一致）。与 _fn189_custom_patch.py 共用同一真源。
# 定制页（历史恢复回调 / 导出校验 / 结果脱敏等）归一化后必然不同 ⇒ 必须拒绝，
# 否则整体替换会静默抹掉定制逻辑。定制页改走 scripts/_fn189_custom_patch.py。
STD_NORM_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                             '_fn189_std_old_seg_normalized.txt')
STD_OLD_NORM = io.open(STD_NORM_FILE, encoding='utf-8').read()


def seg_of(s, pre):
    a = s.find('function __%sResText()' % pre)
    b = s.find('function __%sPresets()' % pre)
    return (a, b, s[a:b]) if a >= 0 and b > a else (-1, -1, '')


def parse_meta(s, slug_hint=None):
    """抽取页面参数。兼容三种变体（第 46 批全站异常页实测）：
    ① host 名不是 `#<pre>Table`（`#resultTable` / `#tableWrap` / `#...Detail` / `#res table`）；
    ② 一个页面有多个 exportTable（取与文件 slug / pre 相关的那个）；
    ③ 结果容器是复合表达式（`getElementById('result'+tab)||querySelector('.result-box')`）；
    ④ 历史回调重算调用不在独立 16 空格行（`__scaleDirty=true; calc();`）⇒ calc 回退 'calc'。
    """
    ets = re.findall(r"exportTable\('([^']+)','([^']+)\.csv'\)", s)
    pres = re.findall(r'function __(\w+?)ResText\(\)', s)
    if not pres:
        return None
    pre = None
    if slug_hint and slug_hint.replace('-', '_') in pres:
        pre = slug_hint.replace('-', '_')
    if pre is None:
        for host, _csv in ets:
            for p in pres:
                if p in host:
                    pre = p
                    break
            if pre:
                break
    if pre is None:
        pre = pres[0]
    a, b, seg = seg_of(s, pre)
    if a < 0:
        return None
    rm = (re.search(r'var r=(document\.(?:getElementById|querySelector)\([^)]*\));', seg)
          or re.search(r'var r=([^\n;]+);', seg))
    if not rm:
        return None
    cm = re.search(r'\n\s{16}([A-Za-z_][A-Za-z0-9_]*)\(\);', seg)
    host, csvslug = '#' + pre + 'Table', pre.replace('_', '-')
    if ets:
        picked = None
        for h, c in ets:
            if pre in h or (slug_hint and c == slug_hint) or c == pre.replace('_', '-'):
                picked = (h, c)
                break
        host, csvslug = picked if picked else ets[0]
    # ⑤ 导出目标与真正的表格容器不是同一个选择器（第 46 批实测 5 页）：
    #   表格渲染进 matrix.table 的容器（`#reportTable` / `#pt24_point_solverTable`），
    #   而 exportTable 还指着旧容器（`#res table` / `#resultTable` / `#tableWrap` / `#...Detail`
    #   / `#24_point_solverTable`）⇒ 导出恒为空 CSV，是页面真 BUG。
    #   唯一 matrix.table 容器时以它为准（多 tab 页不动，避免猜错）。
    mts = []
    for h in re.findall(r"matrix\.table\('([^']+)'", s):
        if h not in mts:
            mts.append(h)
    oldhost = host
    if len(mts) == 1 and host not in mts:
        host = mts[0]
    return dict(pre=pre, slug=csvslug, host=host, oldhost=oldhost, a=a, b=b, seg=seg,
                resexpr=rm.group(1), calc=cm.group(1) if cm else 'calc')


def norm(seg, pre, slug, resexpr, calc):
    """抹平 5 个页面专属参数，供逐字同构比较。"""
    return (seg.replace('__' + pre + '_', '__X_')
               .replace('__' + pre, '__X')
               .replace('#' + pre, '#X')
               .replace("'" + slug + ".csv'", "'X.csv'")
               .replace(resexpr, 'RESEXPR')
               .replace('                ' + calc + '();', '                CALC();'))


def load_template(base_slug=BASE_SLUG, base_cat=BASE_CAT):
    """从已修基准页反推模板：返回 dict(tpl, base_norm, base)。"""
    raise ValueError('business verdict must be implemented and verified per page')
    bf = 'tools/%s/%s.html' % (base_cat, base_slug)
    bs = io.open(bf, encoding='utf-8').read()
    binfo = parse_meta(bs)
    assert binfo and '__tbScore' in binfo['seg'], '基准页必须是已修新实现: ' + bf
    bp, bslug = binfo['pre'], binfo['slug']
    host_base = binfo.get('host') or ('#' + bp + 'Table')
    # 替换顺序要紧：先导出/表格 host（可能不等于 #<pre>Table），再变量前缀（__<pre>_）、
    # 函数前缀（__<pre>），最后其余 DOM id（#<pre>）
    tpl = (binfo['seg']
           .replace(host_base, '@@HOST@@')
           .replace('__' + bp + '_', '@@PVAR@@')
           .replace('__' + bp, '@@PFN@@')
           .replace('#' + bp, '#@@PID@@')
           .replace(binfo['resexpr'], '@@RESEXPR@@')
           .replace('                ' + binfo['calc'] + '();', '                @@CALC@@();')
           .replace("'" + bslug + ".csv'", "'@@SLUG@@.csv'"))
    for k in ('@@PFN@@', '@@PVAR@@', '@@PID@@', '@@HOST@@', '@@RESEXPR@@', '@@CALC@@', '@@SLUG@@'):
        assert k in tpl, '模板占位符缺失: ' + k
    base_norm = norm(binfo['seg'], bp, bslug, binfo['resexpr'], binfo['calc'])
    assert len(base_norm) > 2000 and '__tbScore' in base_norm, '基准新段归一化异常'
    assert base_norm.count('@@') == 0, '基准新段不应含占位符'
    return dict(tpl=tpl, base_norm=base_norm, base=binfo)


def build_standard(s, info, tpl, base_norm, slug):
    """把标准旧模板页整体替换为新实现；返回 (s2, seg)。定制页抛 ValueError。"""
    raise ValueError('business verdict must be implemented and verified per page')
    pre = info['pre']
    assert info['slug'] == slug, '%s csv 名与 slug 不一致: %s' % (slug, info['slug'])
    assert s.count('function __%sResText()' % pre) == 1, slug + ' 起始标记不唯一'
    assert s.count('function __%sPresets()' % pre) == 1, slug + ' 结束标记不唯一'
    assert OLD_FILTER in info['seg'], slug + ' 不是旧模板（已修或二次替换）'
    assert 'parseFloat(arr[j].d[rk])' in info['seg'], slug + ' 旧段缺恒 NaN 图表特征'
    old_norm = norm(info['seg'], pre, slug, info['resexpr'], info['calc'])
    assert len(old_norm) > 2000, slug + ' 旧段过短，疑似异常'
    if old_norm != STD_OLD_NORM:
        raise ValueError(slug + ' 定制页（旧段与标准骨架不同）—— 禁止整体替换，请走 _fn189_custom_patch.py')
    seg = (tpl.replace('@@HOST@@', info['host'])
              .replace('@@PID@@', pre)
              .replace('@@PFN@@', '__' + pre)
              .replace('@@PVAR@@', '__' + pre + '_')
              .replace('@@RESEXPR@@', info['resexpr'])
              .replace('@@CALC@@', info['calc'])
              .replace('@@SLUG@@', slug))
    s2 = s[:info['a']] + seg + s[info['b']:]
    assert s2.count('function __%sResText()' % pre) == 1, slug + ' 替换后标记异常'
    assert s2.count('__tbScore') == 4, slug + ' __tbScore 数量异常'
    assert norm(seg, pre, slug, info['resexpr'], info['calc']) == base_norm, slug + ' 与基准新段不同构'
    return s2, seg


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--cat', default='finance')
    ap.add_argument('--pages', required=True)
    ap.add_argument('--base', default=BASE_SLUG)
    ap.add_argument('--dry', action='store_true')
    args = ap.parse_args()
    slugs = [x.strip() for x in args.pages.split(',') if x.strip()]

    t = load_template(args.base)
    plans = []
    for slug in slugs:
        f = 'tools/%s/%s.html' % (args.cat, slug)
        if not os.path.exists(f):
            print('FAIL %-28s 页面不存在' % slug); sys.exit(1)
        s = io.open(f, encoding='utf-8').read()
        info = parse_meta(s)
        if not info:
            print('FAIL %-28s 抽不到标准参数（可能是定制页/异常页）' % slug); sys.exit(1)
        try:
            s2, seg = build_standard(s, info, t['tpl'], t['base_norm'], slug)
        except (AssertionError, ValueError) as e:
            print('FAIL %-28s %s' % (slug, e)); sys.exit(1)
        plans.append((slug, f, s2, info, seg))
        print('CHECK %-28s res=%-42s calc=%s()' % (slug, info['resexpr'], info['calc']))

    print('自检通过 %d/%d 页%s' % (len(plans), len(slugs), '（--dry 不写盘）' if args.dry else ''))
    if args.dry:
        return
    for slug, f, s2, info, seg in plans:
        io.open(f, 'w', encoding='utf-8').write(s2)
        print('APPLY %-28s %d -> %d chars' % (slug, len(info['seg']), len(seg)))


if __name__ == '__main__':
    main()
