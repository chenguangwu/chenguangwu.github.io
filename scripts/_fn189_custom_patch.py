# -*- coding: utf-8 -*-
"""F-N189 定制页局部编辑工具：只替换 8 个修复锚点，逐行保留页面定制逻辑。

用法：
  python3 scripts/_fn189_custom_patch.py --cat=finance --pages=a,b,c [--dry]

背景：`_fn189_rollout.py` 的「整段替换」只适用于归一化后与标准骨架逐字一致的标准页。
定制页在 ResText~Presets 段内插入过前批功能（历史回调重建 / 导出校验 / 结果脱敏等），
整体替换会静默抹掉这些逻辑。本脚本改为 8 处精确小块替换，并用「归一化后相对标准骨架
的增删行集合，替换前后完全一致」证明除了 F-N189 修复外没有动任何其它字节。

核心逻辑（load_base_new_norm / build_custom）为模块级函数，供 scripts/_fn189_rollout_all.py 复用。
"""
import argparse
import difflib
import io
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import _fn189_rollout as R  # noqa: E402  复用 parse_meta / norm / STD_OLD_NORM

BASE_CAT = R.BASE_CAT
BASE_SLUG = R.BASE_SLUG
OLD_FILTER = R.OLD_FILTER
# 旧过滤行存在多种变体（`|⚠` / `|请填写` / `|应大于` / `|抽取中` / `|不能为|必须`…），
# 精确串 OLD_FILTER 只覆盖标准形态；判定「是否仍吞失败样本」必须按结构正则。
OLD_FILTER_PAT = re.compile(r"    if\(/(?!\^)[^\n]*输入[^\n]*\.test\(t\)\) return '';\n")

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
        "parseFloat(arr[j].d[rk])",
        "parseFloat(arr[j].d.__tbScore)",
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
        "    try { TBKit.util.exportTable('@@HOST@@','@@SLUG@@.csv'); } catch(e){}",
        "    try{\n"
        "        var box=document.getElementById('@@HOSTID@@')||document.querySelector('@@HOST@@');\n"
        "        if(!box||!box.querySelector('tr')){\n"
        "            var snap=@@PFN@@Snap(); var keys=Object.keys(snap);\n"
        "            if(keys.length>12) keys=keys.slice(0,12);\n"
        "            var en=(TBKit.util&&TBKit.util.isEn())?true:false;\n"
        "            @@PFN@@Render(keys,en?'Result':'结果',en);\n"
        "        }\n"
        "    }catch(e){}\n"
        "    try { TBKit.util.exportTable('@@HOST@@','@@SLUG@@.csv'); } catch(e){}",
    ),
]


# 修复锚点本身会改写的行不计入「定制差异」（否则按行比对会把修复算成定制变更）。
# `.test(t)) return '';` 覆盖 ResText 过滤行的所有变体（`|⚠` / `|请填写` / `|应大于` / `|抽取中`…）。
FIX_MARKERS = ('parseFloat(arr[j].d[', 'chart.line', "name:en?'", "exportTable('",
               ".test(t)) return '';", 'RESEXPR')


def strip_fix_tokens(line):
    """抹掉修复本身注入的 token，让「修复前 / 修复后」的定制行可比。

    历史恢复跳过条件各页写法不同（`if(k===rk||k==='计算模式'||k==='Mode') continue;`），
    锚点 3 是在原条件后追加 `||k==='__tbScore'`，逐字比对会把「追加修复」误判成「定制行丢失」。
    """
    return (line.replace("||k==='__tbScore'", '')
                .replace("k==='__tbScore'||", ''))


def custom_added_lines(norm_seg):
    """归一化段中「相对标准骨架多出来的定制行」（剔除修复锚点相关行）。"""
    std = set(R.STD_OLD_NORM.split('\n'))
    return [strip_fix_tokens(l) for l in norm_seg.split('\n')
            if l.strip() and l not in std and not any(m in l for m in FIX_MARKERS)]


def load_base_new_norm():
    """基准页（已修新实现）的新段归一化串。"""
    bs = io.open('tools/%s/%s.html' % (BASE_CAT, BASE_SLUG), encoding='utf-8').read()
    binfo = R.parse_meta(bs)
    assert binfo and '__tbScore' in binfo['seg'], '基准页必须是已修新实现'
    n = R.norm(binfo['seg'], binfo['pre'], binfo['slug'], binfo['resexpr'], binfo['calc'])
    assert len(n) > 2000 and '__tbScore' in n
    return n


SCORE_FN = ("function @@PFN@@Score(t){\n"
            "    var s=String(t||'');\n"
            "    if(/[❌]|⚠️|⚠|无效|未通过|不正确|失败|错误|Invalid|Failed|must be|Please enter|请输入|Waiting/i.test(s)) return 0;\n"
            "    return 1;\n"
            "}\n")

# 幂等判定：某锚点已 0 次匹配时，检查该修复点是否已在页面里（半修页 / 重复执行）
ALREADY = {
    0: lambda seg, pre: 'function __%sScore(t)' % pre in seg,
    1: lambda seg, pre: "en?'Verdict':'结论'" in seg,
    2: lambda seg, pre: 'isFinite(sc)?' in seg,
    3: lambda seg, pre: "k==='__tbScore'" in seg,
    4: lambda seg, pre: 'parseFloat(arr[j].d.__tbScore)' in seg or 'parseFloat(arr[j].d[rk])' not in seg,
    5: lambda seg, pre: "en?'Validity trend':'有效性趋势'" in seg,
    6: lambda seg, pre: '__tbScore=' in seg,
    7: lambda seg, pre: "box.querySelector('tr')" in seg,
}


def build_custom(s, info, base_new_norm, slug):
    """对定制页 / 半修页做 8 处精确局部编辑；返回 (s2, seg, custom_added)。"""
    pre, old_seg = info['pre'], info['seg']
    assert info['slug'] == slug, '%s csv 名与 slug 不一致: %s' % (slug, info['slug'])
    assert s.count('function __%sResText()' % pre) == 1, slug + ' 起始标记不唯一'
    assert s.count('function __%sPresets()' % pre) == 1, slug + ' 结束标记不唯一'
    has_filter = bool(OLD_FILTER_PAT.search(old_seg))
    has_nan = 'parseFloat(arr[j].d[rk])' in old_seg
    if not (has_filter or has_nan):
        raise ValueError(slug + ' 无旧过滤也无恒 NaN，已是完整新实现')

    old_norm = R.norm(old_seg, pre, slug, info['resexpr'], info['calc'])
    if old_norm == R.STD_OLD_NORM:
        raise ValueError(slug + ' 是标准页，请用 _fn189_rollout.py')
    # 允许为空：host 名变体页（#resultTable / #tableWrap / #...Detail）的差异只在
    # exportTable / querySelector 行上，已被 FIX_MARKERS 过滤；旧段 != 骨架已保证非标准页。
    custom_added = custom_added_lines(old_norm)

    seg = old_seg

    # 表格容器已被纠正（`#res table` / `#tableWrap` / `#...Detail` → 真正渲染表的那只）时，
    # 页面 Export 里「有没有数据」的前置守卫仍指着旧容器（thread-spec 实测：守卫读 #tableWrap
    # 恒为空 ⇒ 补渲染逻辑永远走不到、导出永远提前 return）。只改 Export 函数体内的引用，
    # 绝不能全局替换——同一个旧 id 可能还是 ResText / calc 的输出容器（thread-spec 的
    # `var r=document.getElementById('tableWrap')` 就是 ResText，改了会把结果读空）。
    old_host = info.get('oldhost') or info['host']
    if old_host != info['host']:
        oid = old_host[1:] if old_host.startswith('#') else old_host
        nid = info['host'][1:] if info['host'].startswith('#') else info['host']
        m = re.search(r'function __%sExport\(\)\{' % re.escape(pre), seg)
        if m:
            k = seg.index('{', m.start())
            depth, j = 0, k
            while j < len(seg):
                if seg[j] == '{':
                    depth += 1
                elif seg[j] == '}':
                    depth -= 1
                    if depth == 0:
                        break
                j += 1
            body = seg[m.start():j + 1]
            body2 = (body.replace("document.getElementById('%s')" % oid,
                                  "document.getElementById('%s')" % nid)
                         .replace("querySelector('%s')" % old_host, "querySelector('%s')" % info['host']))
            seg = seg[:m.start()] + body2 + seg[j + 1:]

    def rep(x, _pre=pre, _slug=slug, _host=info['host']):
        # @@HOSTID@@：host 去掉前导 '#'，供 getElementById 用。id 以数字开头时
        # querySelector('#64_guaTable') 是非法 CSS 选择器（浏览器抛 SyntaxError、
        # JSDOM 抛 DOMException），必须走 getElementById 才不会静默失效。
        _hid = _host[1:] if _host.startswith('#') else _host
        return (x.replace('@@PFN@@', '__' + _pre).replace('@@PID@@', _pre)
                 .replace('@@SLUG@@', _slug).replace('@@HOSTID@@', _hid)
                 .replace('@@HOST@@', _host))

    # 锚点 0 特例：旧模板替换过滤行并追加 Score；半修页（过滤行已改）只补插 Score。
    # 过滤行还存在变体形态（如额外排除 ⚠：`/请输入|无效|…|NaN|⚠/.test(t)`），精确串匹配不上，
    # 必须再给一条「按结构正则改写」的兜底路径，否则失败样本照样被吞掉（depreciation-declining 实测）。
    NEW_FILTER = rep("    if(/^(等待输入|请输入文本|Waiting for input|Please enter text)/.test(t)) return '';\n")
    FILTER_PAT = OLD_FILTER_PAT
    old0, new0 = rep(PAIRS[0][0]), rep(PAIRS[0][1])
    if seg.count(old0) == 1:
        assert s.count(old0) == 1, slug + ' 第 1 处锚点在全文不唯一'
        seg = seg.replace(old0, new0, 1)
    else:
        if NEW_FILTER not in seg:
            hits = FILTER_PAT.findall(seg)
            assert len(hits) == 1, slug + ' 旧过滤行形态无法自动改写（命中 %d 行）' % len(hits)
            seg = FILTER_PAT.sub(NEW_FILTER, seg, count=1)
        if not ALREADY[0](seg, pre):
            anchor = 'function __%sTime(t){' % pre
            assert seg.count(anchor) == 1, slug + ' Time 函数锚点不唯一，无法补插 Score'
            seg = seg.replace(anchor, rep(SCORE_FN) + anchor, 1)

    numeric_fixed = False
    # 页面已自研「有业务含义且不会恒 NaN」的趋势数值源（如 CD4/CD8 比值兜底、密文输出字节数、
    # 平均分 __mean）时，强行换成本工具通用的有效性 0/1 趋势会把原有兜底逻辑变成死代码
    # （实测 flow-cytometry-ratio / aes-encryptor / exam-analysis）。点号与方括号两种写法都要认。
    has_domain_trend = bool(re.search(r'arr\[j\]\.d\.(?!__tbScore)[A-Za-z_]', old_seg)) or \
        bool(re.search(r"arr\[j\]\.d\['(?!__tbScore)", old_seg))
    for i in range(1, len(PAIRS)):
        # 幂等闸：该修复点已存在就跳过。否则对已修页重复执行会二次插入
        # （锚点 6 `TBKit.history.record(rec);` 每页都有，重复插入 `rec.__tbScore=` ⇒ 5 处）。
        if i in (1, 2, 3, 5, 6, 7) and ALREADY[i](seg, pre):
            continue
        if has_domain_trend and i in (4, 5):
            continue
        old, new = rep(PAIRS[i][0]), rep(PAIRS[i][1])
        if i == 3 and seg.count(old) == 0:
            # 历史恢复跳过字段写法各页不同（`if(k===rk||k==='计算模式'||k==='Mode') continue;`）
            if not ALREADY[3](seg, pre):
                pat = re.compile(r'k===rk')
                assert len(pat.findall(seg)) == 1, slug + ' 历史恢复跳过条件不唯一'
                seg = pat.sub("k===rk||k==='__tbScore'", seg, count=1)
            continue
        if i == 4:
            if seg.count(old) == 1:
                seg = seg.replace(old, new, 1)
                numeric_fixed = True
            else:
                assert ALREADY[4](seg, pre), slug + ' 第 5 处锚点缺失且未修'
                # 页面已单独修好数值源：若用的是 __tbScore 则应改名，否则保留原语义（如输出字节数）
                numeric_fixed = 'parseFloat(arr[j].d.__tbScore)' in seg
            continue
        if i == 5:
            if not numeric_fixed:
                continue
            if seg.count(old) == 0:
                # 趋势图名称各页文案不同（如 CD4/CD8 比值趋势），精确串缺失时按结构正则替换
                pat = r"name:en\?'[^']*':'[^']*'"
                if len(re.findall(pat, seg)) == 1:
                    seg = re.sub(pat, new, seg, count=1)
                    continue
                assert ALREADY[5](seg, pre), slug + ' 趋势图名称缺失且未修'
                continue
        if seg.count(old) == 0:
            if i == len(PAIRS) - 1:
                # 末位锚点（导出补渲染）：部分页用 exportCsv / Blob 导出，不存在 exportTable。
                # 存在时按「任意 host」的结构正则命中——表格容器可能已被本工具纠正
                # （`#res table` → `#reportTable` 等），精确串里带着新 host，必然对不上原行。
                if 'exportTable(' in old_seg:
                    pat = re.compile(
                        r"    try \{ TBKit\.util\.exportTable\('[^']+','"
                        + re.escape(slug) + r"\.csv'\); \} catch\(e\)\{\}")
                    if len(pat.findall(seg)) == 1:
                        seg = pat.sub(lambda m: new, seg, count=1)
                        continue
                assert ALREADY[7](seg, pre) or 'exportTable(' not in old_seg, \
                    slug + ' 导出锚点缺失但页面存在 exportTable'
            else:
                assert ALREADY[i](seg, pre), slug + ' 第 %d 处锚点缺失且未修' % (i + 1)
            continue
        assert seg.count(old) == 1, '%s 第 %d 处锚点在段内不唯一 (%d)' % (slug, i + 1, seg.count(old))
        assert s.count(old) == 1, '%s 第 %d 处锚点在全文不唯一 (%d)' % (slug, i + 1, s.count(old))
        seg = seg.replace(old, new, 1)

    new_norm = R.norm(seg, pre, slug, info['resexpr'], info['calc'])
    # 标准新实现是 4 处；页面已自研更贴切的趋势数值源（如 aes-encryptor 的「输出字节数」）时
    # 锚点 4/5 合法跳过 ⇒ 3 处。低于 3 或关键位点缺失说明修复没落地。
    n_score = seg.count('__tbScore')
    assert 3 <= n_score <= 4, slug + ' __tbScore 数量异常: %d' % n_score
    assert 'isFinite(sc)?' in seg, slug + ' 结论列缺失'
    assert 'rec.__tbScore=' in seg, slug + ' __tbScore 未写入历史记录'
    assert "k==='__tbScore'" in seg, slug + ' 历史恢复未跳过 __tbScore'
    assert not OLD_FILTER_PAT.search(seg), slug + ' 旧过滤正则仍在'
    assert 'function __%sScore(t)' % pre in seg, slug + ' Score 函数缺失'
    new_set = set(strip_fix_tokens(l) for l in new_norm.split('\n'))
    missing = [l for l in custom_added if l not in new_set]
    assert not missing, slug + ' 前批定制行丢失：%r' % (missing[:3],)
    assert new_norm != base_new_norm, slug + ' 定制逻辑丢失（与基准新段同构）'
    return s[:info['a']] + seg + s[info['b']:], seg, custom_added


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--cat', default='finance')
    ap.add_argument('--pages', required=True)
    ap.add_argument('--dry', action='store_true')
    args = ap.parse_args()
    slugs = [x.strip() for x in args.pages.split(',') if x.strip()]

    base_new_norm = load_base_new_norm()
    plans = []
    for slug in slugs:
        f = 'tools/%s/%s.html' % (args.cat, slug)
        if not os.path.exists(f):
            print('FAIL %-28s 页面不存在' % slug); sys.exit(1)
        s = io.open(f, encoding='utf-8').read()
        info = R.parse_meta(s, slug)
        if not info:
            print('FAIL %-28s 抽不到标准参数' % slug); sys.exit(1)
        try:
            s2, seg, cd = build_custom(s, info, base_new_norm, slug)
        except (AssertionError, ValueError) as e:
            print('FAIL %-28s %s' % (slug, e)); sys.exit(1)
        plans.append((slug, f, s2, len(info['seg']), len(seg), len(cd)))
        print('CHECK %-28s 定制差异 %d 行 %d -> %d chars' % (slug, len(cd), len(info['seg']), len(seg)))

    print('自检通过 %d/%d 页%s' % (len(plans), len(slugs), '（--dry 不写盘）' if args.dry else ''))
    if args.dry:
        return
    for slug, f, s2, olen, nlen, _ in plans:
        io.open(f, 'w', encoding='utf-8').write(s2)
        print('APPLY %-28s %d -> %d chars' % (slug, olen, nlen))


if __name__ == '__main__':
    main()
