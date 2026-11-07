# -*- coding: utf-8 -*-
"""F-N189 全站铺开工具：把已修基准页的新 Extras 段按「参数自适应」套到指定旧模板页。

用法：
  python3 scripts/_fn189_rollout.py --cat=finance --pages=a,b,c [--dry]

- 基准页恒为 tools/finance/cnpj-validator.html（第 40 批首修、新实现单一真源）。
- 每页自动抽取：函数/DOM id 前缀、结果容器整段表达式、计算函数名、csv 名。
- 只处理「旧模板标准页」：写入前逐项自检，任一不通过即整批中止（不落盘脏文件）。
- 定制页（归一化后与基准旧段不同）会被明确拒绝并提示需走「保留定制的局部编辑」。
- --dry 只检查不写，供分型复核。
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


def parse_meta(s):
    m = re.search(r"exportTable\('#([^']+)Table','([^']+)\.csv'\)", s)
    if not m:
        return None
    pre, slug = m.group(1), m.group(2)
    a, b, seg = seg_of(s, pre)
    if a < 0:
        return None
    rm = re.search(r'var r=(document\.(?:getElementById|querySelector)\([^)]*\));', seg)
    cm = re.search(r'\n\s{16}([A-Za-z_][A-Za-z0-9_]*)\(\);', seg)
    if not (rm and cm):
        return None
    return dict(pre=pre, slug=slug, a=a, b=b, seg=seg,
                resexpr=rm.group(1), calc=cm.group(1))


def norm(seg, pre, slug, resexpr, calc):
    """抹平 5 个页面专属参数，供逐字同构比较。"""
    return (seg.replace('__' + pre + '_', '__X_')
               .replace('__' + pre, '__X')
               .replace('#' + pre, '#X')
               .replace("'" + slug + ".csv'", "'X.csv'")
               .replace(resexpr, 'RESEXPR')
               .replace('                ' + calc + '();', '                CALC();'))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--cat', default='finance')
    ap.add_argument('--pages', required=True)
    ap.add_argument('--base', default=BASE_SLUG)
    ap.add_argument('--dry', action='store_true')
    args = ap.parse_args()
    slugs = [x.strip() for x in args.pages.split(',') if x.strip()]

    # 1) 从基准页反推模板
    bf = 'tools/%s/%s.html' % (BASE_CAT, args.base)
    bs = io.open(bf, encoding='utf-8').read()
    binfo = parse_meta(bs)
    assert binfo and '__tbScore' in binfo['seg'], '基准页必须是已修新实现: ' + bf
    bp, bslug = binfo['pre'], binfo['slug']
    tpl = (binfo['seg']
           .replace('__' + bp + '_', '@@PVAR@@')
           .replace('__' + bp, '@@PFN@@')
           .replace('#' + bp, '#@@PID@@')
           .replace(binfo['resexpr'], '@@RESEXPR@@')
           .replace('                ' + binfo['calc'] + '();', '                @@CALC@@();')
           .replace("'" + bslug + ".csv'", "'@@SLUG@@.csv'"))
    for k in ('@@PFN@@', '@@PVAR@@', '@@PID@@', '@@RESEXPR@@', '@@CALC@@', '@@SLUG@@'):
        assert k in tpl, '模板占位符缺失: ' + k
    B = norm(binfo['seg'], bp, bslug, binfo['resexpr'], binfo['calc'])
    assert len(B) > 2000 and '__tbScore' in B, '基准新段归一化异常'

    # 2) 逐页自检（全部通过后才开始写，避免半批落盘）
    plans = []
    for slug in slugs:
        f = 'tools/%s/%s.html' % (args.cat, slug)
        if not os.path.exists(f):
            print('FAIL %-28s 页面不存在' % slug); sys.exit(1)
        s = io.open(f, encoding='utf-8').read()
        info = parse_meta(s)
        if not info:
            print('FAIL %-28s 抽不到标准参数（可能是定制页/异常页）' % slug); sys.exit(1)
        assert info['slug'] == slug, '%s csv 名与 slug 不一致: %s' % (slug, info['slug'])
        assert s.count('function __%sResText()' % info['pre']) == 1, slug + ' 起始标记不唯一'
        assert s.count('function __%sPresets()' % info['pre']) == 1, slug + ' 结束标记不唯一'
        assert OLD_FILTER in info['seg'], slug + ' 不是旧模板（已修或二次替换）'
        assert 'parseFloat(arr[j].d[rk])' in info['seg'], slug + ' 旧段缺恒 NaN 图表特征'
        # 拒绝定制页：旧段归一化后须与标准骨架逐字一致（sha256 比对，非仅长度）
        old_norm = norm(info['seg'], info['pre'], slug, info['resexpr'], info['calc'])
        assert len(old_norm) > 2000, slug + ' 旧段过短，疑似异常'
        if old_norm != STD_OLD_NORM:
            print('FAIL %-28s 定制页（旧段与标准骨架不同）—— 禁止整体替换，请走 _fn189_custom_patch.py' % slug)
            sys.exit(1)
        seg = (tpl.replace('@@PFN@@', '__' + info['pre'])
                  .replace('@@PVAR@@', '__' + info['pre'] + '_')
                  .replace('@@PID@@', info['pre'])
                  .replace('@@RESEXPR@@', info['resexpr'])
                  .replace('@@CALC@@', info['calc'])
                  .replace('@@SLUG@@', slug))
        s2 = s[:info['a']] + seg + s[info['b']:]
        assert s2.count('function __%sResText()' % info['pre']) == 1, slug + ' 替换后标记异常'
        assert s2.count('__tbScore') == 4, slug + ' __tbScore 数量异常'
        assert norm(seg, info['pre'], slug, info['resexpr'], info['calc']) == B, slug + ' 与基准新段不同构'
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
