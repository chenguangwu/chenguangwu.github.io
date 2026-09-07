# -*- coding: utf-8 -*-
"""分类落地页自动差异化 SEO 内容生成器。

不再手写逐行业长文案（避免编造与维护成本），而是基于该行业在
tools.json 中的真实工具列表，自动生成独一无二的栏目简介、核心功能
清单与 FAQ，从根本上消除 268 个分类页互为重复内容（Thin Content）的问题。
每个行业的正文主体是该行业真实的工具名清单，因此页面之间天然差异化。
"""
import json


def _esc(s):
    return (str(s).replace('&', '&amp;').replace('<', '&lt;')
            .replace('>', '&gt;').replace('"', '&quot;'))


def _pick_repr(tool_names, n=18):
    """均匀抽取代表工具名，保证清单覆盖行业全貌且不随工具顺序漂移。"""
    if not tool_names:
        return []
    if len(tool_names) <= n:
        return list(tool_names)
    step = len(tool_names) / float(n)
    return [tool_names[int(round(i * step))] for i in range(n)]


def _make_desc_zh(ind_name, count, tool_names):
    # 基准串已含足够信息且 ≥100 字，覆盖绝大多数行业；极短行业名或单工具行业
    # 若仍不足 100 字，再补充代表工具名兜底，整体控制在 150 字以内。
    base = ('本页收录%d个免费%s在线工具，覆盖%s场景下的常见计算、换算、单位转换与查询需求，'
            '帮助你快速完成相关日常任务。所有工具均为纯前端在线工具，无需安装软件、无需注册账号，'
            '数据在浏览器本地计算，不上传服务器，手机与电脑打开网页即可直接使用。'
            % (count, ind_name, ind_name))
    if 100 <= len(base) <= 150:
        return base
    if len(base) < 100:
        extra = ''
        for nm in tool_names[:24]:
            cand = (extra + '、' + nm) if extra else ('包括' + nm)
            if len(base) + len(cand) > 148:
                break
            extra = cand
        if extra:
            head = base[:base.rfind('。所有工具')]
            return '%s，包括%s等。所有工具均为纯前端在线工具，数据不上传服务器，手机电脑打开即用。' % (head, extra)
        return base + '无论你是相关领域从业者、学生还是普通用户，都能在这里找到即用即走的实用小工具。'
    return base[:150]


def build_content(ind, ind_name, en_name, count, tool_names):
    rep = _pick_repr(tool_names, 18)
    title_zh = '%s在线工具集合 - 免费实用的%s工具箱' % (ind_name, ind_name)
    if len(title_zh) > 60:
        title_zh = '%s工具集合(%d) - ToolBox 免费在线工具' % (ind_name, count)
    desc_zh = _make_desc_zh(ind_name, count, tool_names)
    rep6 = '、'.join(rep[:6])
    desc_en = ('Free online %s tools collection with %d calculators and converters. '
               'Includes %s and more. All run client-side in your browser, no data uploaded.'
               % (en_name, count, rep6))
    faq = [
        {'q': '%s工具需要下载或注册吗？' % ind_name,
         'a': '不需要。本页所有%s工具都是纯前端在线工具，打开网页即可直接使用，无需安装软件、无需注册账号，也不上传任何数据。' % ind_name},
        {'q': '%s工具的计算结果准确吗？数据安全吗？' % ind_name,
         'a': '工具基于公开的数学公式与通用行业标准在你的浏览器本地计算，结果即时可得。所有运算都在你的设备本地完成，数据不会上传到服务器，隐私安全有保障。'},
    ]
    return {
        'ind': ind, 'ind_name': ind_name, 'en_name': en_name, 'count': count,
        'rep': rep, 'title_zh': title_zh, 'desc_zh': desc_zh, 'desc_en': desc_en,
        'faq': faq,
    }


def render_body(c, count):
    ind_name = c['ind_name']
    out = []
    out.append('      <h4><span class="h4-icon">📝</span>栏目简介</h4>\n')
    out.append('      <p>%s工具集合收录了 %d 个免费在线工具，覆盖%s场景下的常见计算、换算与查询需求。无论你是相关领域的从业者、学生还是普通用户，都能在这里找到即用即走的实用小工具。所有工具纯前端运行，数据不上传服务器，保护隐私安全。</p>\n' % (_esc(ind_name), count, _esc(ind_name)))
    out.append('      <h4><span class="h4-icon">✨</span>核心功能与适用场景</h4>\n')
    out.append('      <p>本页收录的%s工具包括（部分代表工具）：</p>\n' % _esc(ind_name))
    out.append('      <ul class="intro-features">\n')
    for nm in c['rep']:
        out.append('        <li>%s</li>\n' % _esc(nm))
    out.append('      </ul>\n')
    out.append('      <p>这些工具帮助你快速完成%s相关的常见任务，无需记忆复杂公式或手动换算，输入即可得结果。</p>\n' % _esc(ind_name))
    out.append('      <h4><span class="h4-icon">❓</span>常见问题</h4>\n')
    for f in c['faq']:
        out.append('      <p><strong>%s</strong></p>\n' % _esc(f['q']))
        out.append('      <p>%s</p>\n' % _esc(f['a']))
    return ''.join(out)


def faq_ld(c, count):
    qs = [{'@type': 'Question', 'name': f['q'],
           'acceptedAnswer': {'@type': 'Answer', 'text': f['a']}} for f in c['faq']]
    data = {'@context': 'https://schema.org', '@type': 'FAQPage', 'mainEntity': qs}
    return '<script type="application/ld+json">\n%s\n</script>\n' % json.dumps(data, ensure_ascii=False)
