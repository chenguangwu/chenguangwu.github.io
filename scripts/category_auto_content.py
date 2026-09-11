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


def build_content(ind, ind_name, en_name, count, tool_names, tool_names_en=None):
    rep = _pick_repr(tool_names, 18)
    rep_en = _pick_repr(tool_names_en or tool_names, 18)
    title_zh = '%s在线工具集合 - 免费实用的%s工具箱' % (ind_name, ind_name)
    if len(title_zh) > 60:
        title_zh = '%s工具集合(%d) - ToolBox 免费在线工具' % (ind_name, count)
    desc_zh = _make_desc_zh(ind_name, count, tool_names)
    # 英文 description 的代表工具名同样取英文名（原先误用中文名，导致英文描述夹中文）
    rep6 = ', '.join(rep_en[:6])
    desc_en = ('Free online %s tools collection with %d calculators and converters. '
               'Includes %s and more. All run client-side in your browser, no data uploaded.'
               % (en_name, count, rep6))
    faq = [
        {'q': '%s工具需要下载或注册吗？' % ind_name,
         'a': '不需要。本页所有%s工具都是纯前端在线工具，打开网页即可直接使用，无需安装软件、无需注册账号，也不上传任何数据。' % ind_name,
         'q_en': 'Do %s tools require any download or sign-up?' % en_name,
         'a_en': 'No. Every tool on this page is a pure front-end online tool — just open the page and start using it. No software to install, no account needed, and no data is uploaded.'},
        {'q': '%s工具的计算结果准确吗？数据安全吗？' % ind_name,
         'a': '工具基于公开的数学公式与通用行业标准在你的浏览器本地计算，结果即时可得。所有运算都在你的设备本地完成，数据不会上传到服务器，隐私安全有保障。',
         'q_en': 'Are the results accurate? Is my data safe?',
         'a_en': 'Calculations are based on published formulas and common industry standards, computed locally in your browser for instant results. Everything runs on your own device — nothing is uploaded to a server.'},
    ]
    return {
        'ind': ind, 'ind_name': ind_name, 'en_name': en_name, 'count': count,
        'rep': rep, 'rep_en': rep_en, 'title_zh': title_zh, 'desc_zh': desc_zh, 'desc_en': desc_en,
        'faq': faq,
    }


def render_body(c, count):
    """正文输出中英双语层（.t-zh/.t-en，由 css 的 html[lang] 规则切换显隐）。

    英文层用行业英文名与英文工具名，避免英文态正文夹中文。
    """
    ind_name = c['ind_name']
    en_name = c.get('en_name') or ind_name
    rep = c['rep']
    rep_en = c.get('rep_en') or rep
    out = []
    out.append('      <h4><span class="h4-icon">📝</span><span data-i18n="cat.h_about" data-i18n-fb="栏目简介">栏目简介</span></h4>\n')
    out.append('      <p><span class="t-zh">%s工具集合收录了 %d 个免费在线工具，覆盖%s场景下的常见计算、换算与查询需求。无论你是相关领域的从业者、学生还是普通用户，都能在这里找到即用即走的实用小工具。所有工具纯前端运行，数据不上传服务器，保护隐私安全。</span>'
               '<span class="t-en">This collection gathers %d free online %s tools for everyday calculations, conversions and lookups. Whether you are a professional, a student or a casual user, you will find handy tools you can use right away. Everything runs client-side — no data is uploaded.</span></p>\n'
               % (_esc(ind_name), count, _esc(ind_name), count, _esc(en_name)))
    out.append('      <h4><span class="h4-icon">✨</span><span data-i18n="cat.h_feature" data-i18n-fb="核心功能与适用场景">核心功能与适用场景</span></h4>\n')
    out.append('      <p><span class="t-zh">本页收录的%s工具包括（部分代表工具）：</span><span class="t-en">Featured %s tools on this page include:</span></p>\n' % (_esc(ind_name), _esc(en_name)))
    out.append('      <ul class="intro-features">\n')
    for i, nm in enumerate(rep):
        en = rep_en[i] if i < len(rep_en) else nm
        out.append('        <li><span class="t-zh">%s</span><span class="t-en">%s</span></li>\n' % (_esc(nm), _esc(en)))
    out.append('      </ul>\n')
    out.append('      <p><span class="t-zh">这些工具帮助你快速完成%s相关的常见任务，无需记忆复杂公式或手动换算，输入即可得结果。</span>'
               '<span class="t-en">These tools help you complete %s tasks quickly — no formulas to memorise and no manual conversion, just enter your values and get the result.</span></p>\n'
               % (_esc(ind_name), _esc(en_name)))
    out.append('      <h4><span class="h4-icon">❓</span><span data-i18n="cat.h_faq" data-i18n-fb="常见问题">常见问题</span></h4>\n')
    for f in c['faq']:
        out.append('      <p><strong><span class="t-zh">%s</span><span class="t-en">%s</span></strong></p>\n'
                   % (_esc(f['q']), _esc(f.get('q_en') or f['q'])))
        out.append('      <p><span class="t-zh">%s</span><span class="t-en">%s</span></p>\n'
                   % (_esc(f['a']), _esc(f.get('a_en') or f['a'])))
    return ''.join(out)


def faq_ld(c, count):
    qs = [{'@type': 'Question', 'name': f['q'],
           'acceptedAnswer': {'@type': 'Answer', 'text': f['a']}} for f in c['faq']]
    data = {'@context': 'https://schema.org', '@type': 'FAQPage', 'mainEntity': qs}
    return '<script type="application/ld+json">\n%s\n</script>\n' % json.dumps(data, ensure_ascii=False)
