#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""biz (69) 分类英文态数据源根治：同步三端 + 补中文态缺口。

三处数据源（与 science/sports/fun/ai 同坑，§6「英文态数据源三处」）：
  ① i18n/tools/biz-body.json   -> build `_prerender_tool_body` 预渲染 h2 + 首个 <p>
  ② i18n/tools/biz.json en-US  -> industry JSON 的 ed 最高优先级源
  ③ i18n/tools/_en_override.json -> 运行时 en（h2/h1）与 ed

本轮额外缺口：8 个工具（analysis-47 / analysis-manager / assessor-49 /
assessor-risk-8 / checker-8 / random-script / stats-time-response /
summary-rater-csat）在 biz.json 中无 zh-CN 条目（中文名与简介全空），
导致 deep-dive/指南/英文态全部缺失，由 ZH_TITLE / ZH_INTRO 一并补齐。

用法：
  python3 scripts/fix_biz_body_i18n.py --dry-run
  python3 scripts/fix_biz_body_i18n.py --apply
"""
import argparse
import glob
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOOLS = os.path.join(ROOT, 'tools', 'biz')
OV = os.path.join(ROOT, 'i18n', 'tools', '_en_override.json')
BODY = os.path.join(ROOT, 'i18n', 'tools', 'biz-body.json')
GIS = os.path.join(ROOT, 'i18n', 'tools', 'biz.json')

# 8 个在 biz.json 中缺 zh-CN 条目的工具：补齐中文名与简介（依据页面 <title> 与实际功能）
ZH_TITLE = {
    'analysis-47': '战略（分析/定位/实施）框架',
    'analysis-manager': '财务（管理/分析/决策）咨询',
    'assessor-49': '胜任力（模型/评估/发展）',
    'assessor-risk-8': '风险（排查/评估/防控）措施',
    'checker-8': '质量（服务标准/检查/改进）',
    'random-script': '标准话术模板随机抽取器',
    'stats-time-response': '客服平均响应时间/解决率统计',
    'summary-rater-csat': '客户满意度（CSAT）评分汇总',
}

ZH_INTRO = {
    'analysis-47': '输入关键经营数据，按「分析—定位—实施」三段框架输出战略梳理结果与行动要点，辅助咨询顾问与管理层做战略研讨、立项与汇报。',
    'analysis-manager': '输入财务与经营数据（逗号或换行分隔），输出均值、极值、波动等管理分析指标与决策提示，辅助财务管理、预算复盘与经营决策。',
    'assessor-49': '按六个维度评分并结合岗位类型加权，输出胜任力总分、等级与发展建议，适用于人才盘点、晋升评估与培养规划。',
    'assessor-risk-8': '按安防场景逐条登记风险点，评估可能性与影响并生成分级防控措施清单，适用于楼宇园区、大型活动、仓储物流与生产安全排查。',
    'checker-8': '按人员、执行、装备、服务四类共十四项指标评分并加权得出服务质量总分与待改进项，适用于保安服务与现场服务质量检查。',
    'random-script': '按设定数量从标准话术模板库中随机抽取话术条目，辅助客服培训、话术演练与抽检考核，纯前端运行不上传数据。',
    'stats-time-response': '输入客服响应或处理时长数据，统计平均响应时间、解决率与分布区间，辅助客服团队效率评估、排班与流程优化。',
    'summary-rater-csat': '输入 CSAT 评分数据，汇总均分、分布与各档位占比，输出满意度结论与改进方向，适用于客服与售后质量复盘。',
}

# NAME = 英文名（h2 / h1 / 导航 / 英文态标题），INTRO = 真实英文描述（intro / ed）。
NAME = {
    'analysis-47': 'Strategic Analysis Framework',
    'analysis-manager': 'Financial Management & Decision Analysis',
    'app-name-generator': 'App Name Generator',
    'assessor-49': 'Competency Model Assessor',
    'assessor-risk-8': 'Security Risk Assessment & Control Planner',
    'barcode-generator': 'Barcode Generator',
    'brand-name-generator': 'Brand Name Generator',
    'char-frequency': 'Character Frequency Analyzer',
    'checker-8': 'Service Quality Inspection Checker',
    'comment-generator': 'Code Comment Generator',
    'fancy-text': 'Fancy Text Converter',
    'fullwidth-halfwidth': 'Full-width & Half-width Converter',
    'justify-text': 'Text Justify Tool',
    'lorem-ipsum-advanced': 'Advanced Lorem Ipsum Generator',
    'markdown': 'Markdown Live Preview',
    'markdown-quote': 'Markdown Blockquote Converter',
    'meeting-cost-calculator': 'Meeting Cost Calculator',
    'motto-generator': 'Motto & Slogan Generator',
    'name-generator': 'Random Nickname Generator',
    'presentation-timer': 'Presentation Timer',
    'product-name-generator': 'Product Name Generator',
    'random-script': 'Standard Script Template Picker',
    'simplified-traditional': 'Simplified–Traditional Chinese Converter',
    'small-caps': 'Small Caps Converter',
    'stats-time-response': 'Support Response Time Statistics',
    'strawberry-text': 'Strawberry Text Generator',
    'summary-rater-csat': 'CSAT Score Summary',
    'superscript-text': 'Superscript Text Converter',
    'team-roster-generator': 'Random Team Grouping Generator',
    'text-box-drawing': 'Text Box Drawing Tool',
    'text-case': 'Text Case Converter',
    'text-case-advanced': 'Advanced Text Case Converter',
    'text-compare': 'Side-by-Side Text Diff',
    'text-dedup': 'Text Deduplicator',
    'text-extract': 'Smart Text Extractor',
    'text-extract-chinese': 'Chinese Character Extractor',
    'text-extract-dates': 'Date Extractor',
    'text-extract-emails': 'Email Address Extractor',
    'text-extract-english': 'English Character Extractor',
    'text-extract-html-tags': 'HTML Tag Extractor',
    'text-extract-ips': 'IP Address Extractor',
    'text-extract-numbers': 'Number Extractor',
    'text-extract-urls': 'URL Extractor',
    'text-filter-lines': 'Line Filter',
    'text-indent': 'Auto Indent Tool',
    'text-keep-only': 'Keep-Only Character Filter',
    'text-line-numbers': 'Line Number Adder',
    'text-merge': 'Multi-Text Merger',
    'text-pad': 'Text Padding Tool',
    'text-prefix-suffix': 'Prefix & Suffix Adder',
    'text-remove-duplicates-lines': 'Duplicate Line Remover',
    'text-remove-numbers': 'Character Remover',
    'text-repeat': 'Text Repeater',
    'text-replace-advanced': 'Advanced Find & Replace',
    'text-reverse': 'Text Reverser',
    'text-reverse-lines': 'Line Order Reverser',
    'text-shuffle': 'Text Shuffler',
    'text-sort': 'Text Line Sorter',
    'text-sort-advanced': 'Advanced Text Sorter',
    'text-split': 'Text Splitter',
    'text-stats': 'Text Statistics Tool',
    'text-to-banner': 'Text to Banner',
    'text-to-slug': 'Text to URL Slug',
    'text-trim': 'Text Trimmer',
    'text-wrap': 'Text Wrap & Fill Tool',
    'unicode-normalize': 'Unicode Normalizer',
    'unit-price-compare': 'Unit Price Comparison Calculator',
    'upside-down-text': 'Upside-Down Text Converter',
    'zalgo-text': 'Zalgo Text Generator',
}

INTRO = {
    'analysis-47': 'Enter key business figures and get a structured strategy output along the analysis–positioning–execution framework, with action points for consulting workshops, planning sessions and management reviews.',
    'analysis-manager': 'Enter financial or operating figures (comma or newline separated) to get mean, extremes and dispersion indicators plus decision hints, supporting budgeting reviews and management decisions.',
    'app-name-generator': 'Generate app name candidates by combining industry keywords with naming styles, each with a short rationale to support product kick-off and early branding decisions.',
    'assessor-49': 'Score six competency dimensions and weight them by job type to produce an overall competency score, level and development suggestions for talent review, promotion assessment and training planning.',
    'assessor-risk-8': 'Register risk items by security scenario, rate likelihood and impact, and generate a graded control-measure checklist for buildings, campuses, events, warehousing and production safety inspections.',
    'barcode-generator': 'Generate Code128, EAN-13, UPC-A, Code39 and other barcode symbologies entirely in the browser, with preview and download for packaging, inventory and internal labelling.',
    'brand-name-generator': 'Combine industry, tone and keyword inputs to generate brand name candidates with notes on registrability, supporting startup naming, marketing planning and brand screening.',
    'char-frequency': 'Count how often each character appears in your text and show the share of total with sorted results, useful for word-frequency analysis, password strength checks and log profiling.',
    'checker-8': 'Rate fourteen indicators across the people, execution, equipment and service groups to produce a weighted service-quality score and an improvement list for security and on-site service inspections.',
    'comment-generator': 'Generate a standardised comment template (description, parameters, return value) from a function or variable name to improve code readability and documentation consistency.',
    'fancy-text': 'Convert plain text into dozens of decorative Unicode styles such as gothic, circled and full-width, ready to copy for social profiles, posts and creative typography.',
    'fullwidth-halfwidth': 'Convert bidirectionally between Chinese full-width and English half-width characters, handling punctuation and spaces for mixed-language typesetting and data cleaning.',
    'justify-text': 'Insert spaces between words so every line reaches the same width, producing justified English paragraphs or comment blocks with configurable line width.',
    'lorem-ipsum-advanced': 'Generate Lorem Ipsum placeholder text by paragraph count, sentence count or word count, with Chinese/English options and a custom opening phrase for design mockups.',
    'markdown': 'Type Markdown on the left and see headings, lists and code blocks rendered on the right in real time, making it easy to check formatting while writing.',
    'markdown-quote': 'Turn pasted multi-line text into a Markdown blockquote by prefixing every line with ">", ready to paste into documentation, issues or knowledge-base articles.',
    'meeting-cost-calculator': 'Enter attendee count, average hourly rate and meeting duration to calculate total labour cost, cost per minute and cost per person, and judge whether the meeting is worth its price.',
    'motto-generator': 'Generate motivational mottos and team slogans from keywords or a preferred style; everything is created locally and never uploaded, suitable for team culture and event material.',
    'name-generator': 'Generate random Chinese names, English names, online nicknames or game IDs with one click; runs entirely in the browser and never uploads data.',
    'presentation-timer': 'Allocate a time budget to each slide and track progress with full-screen support, helping speakers keep pace during rehearsals and live presentations.',
    'product-name-generator': 'Combine category, selling points and style keywords to generate product name candidates with slogan ideas, supporting e-commerce listings and packaging copy.',
    'random-script': 'Draw a set number of standard response templates from the built-in script library for agent training, script drills and random quality checks; runs fully in the browser.',
    'simplified-traditional': 'Convert text between Simplified and Traditional Chinese character by character using a character-map, accounting for mainland and Taiwan variant differences in documents and typesetting.',
    'small-caps': 'Convert English text into small-caps style code points for brand marks, paper typesetting and stylised headings that stay copy-pasteable.',
    'stats-time-response': 'Enter response or handling durations to get average response time, resolution rate and distribution, supporting support-team efficiency reviews, staffing and process tuning.',
    'strawberry-text': 'Generate decorative text with strawberry motifs and a pink style that can be copied into social nicknames, greeting cards and chat messages, all rendered instantly in the browser.',
    'summary-rater-csat': 'Enter CSAT scores to summarise the average, distribution and share of each rating band, with a satisfaction verdict and improvement directions for support and after-sales reviews.',
    'superscript-text': 'Convert selected text into superscript and produce copyable Unicode or HTML superscript code for chemical formulas, footnotes and mathematical notation.',
    'team-roster-generator': 'Paste a name list and split it into random groups by group count or group size, useful for activity teams, classroom grouping and random draws.',
    'text-box-drawing': 'Wrap text in a variety of ASCII or Unicode border styles to create boxed callouts for terminal output, documentation and readme files.',
    'text-case': 'Switch English text between lower case, UPPER CASE, Title Case and Sentence case in one click for variable naming, headings and document formatting.',
    'text-case-advanced': 'Apply sentence-case and title-case rules on top of basic case conversion while preserving proper nouns, designed for long documents and editorial cleanup.',
    'text-compare': 'Compare two pieces of text side by side and highlight differences line by line or word by word, making added, removed and changed parts easy to spot in code review and editing.',
    'text-dedup': 'Automatically find and remove duplicated content while keeping the first or last occurrence, with options to ignore case and surrounding whitespace.',
    'text-extract': 'Pull key fragments such as emails, phone numbers, links or custom patterns out of long pasted text, filtering noise and removing duplicates for fast data collection.',
    'text-extract-chinese': 'Strip out English letters, digits and punctuation and keep only Chinese characters, useful for cleaning scraped foreign pages or preparing Chinese-language corpora.',
    'text-extract-dates': 'Recognise and extract date expressions (absolute and relative) from paragraphs, then sort, deduplicate and export them for contract review and timeline building.',
    'text-extract-emails': 'Extract every email address from text, deduplicate the list and copy it in one step for batch outreach and contact-list cleanup.',
    'text-extract-english': 'Filter English letters and words out of mixed text while dropping Chinese characters and symbols, handy for collecting identifiers and foreign terminology.',
    'text-extract-html-tags': 'Pull all tag names or a specific tag out of an HTML snippet and count occurrences with deduplication, useful for checking page structure and cleaning markup.',
    'text-extract-ips': 'Extract all IPv4 and IPv6 addresses from logs or documents and list them deduplicated for network troubleshooting, traffic statistics and security reviews.',
    'text-extract-numbers': 'Pull all integers or decimals out of mixed text, keeping signs and decimal places, and output per line or as a whole for data preparation.',
    'text-extract-urls': 'Extract every URL from long text or page source and deduplicate the list, handy for batch reference collection, backlink audits and link validation.',
    'text-filter-lines': 'Filter multi-line text by keyword inclusion, exclusion or regular expression to keep target lines and drop noise quickly.',
    'text-indent': 'Add indentation to text or code by hierarchy and unify indentation width, supporting JSON and multi-line text formatting for cleaner diffs and reviews.',
    'text-keep-only': 'Reverse filtering that keeps only the characters or character classes you specify (for example Chinese or digits) and drops everything else from mixed text.',
    'text-line-numbers': 'Add continuous line numbers to every line with a configurable start value and separator, useful for pasting code, quoting manuscripts and numbering step lists.',
    'text-merge': 'Merge several scattered text blocks into one by line or with a custom separator, optionally removing blank lines and duplicates for notes, logs and batch copy.',
    'text-pad': 'Pad each line with spaces or a chosen character to a target width, aligned left, right or centre, for aligning tables, logs and fixed-width output.',
    'text-prefix-suffix': 'Add a fixed prefix or suffix (such as numbering or symbols) to every line, with regex and separator support for batch list formatting.',
    'text-remove-duplicates-lines': 'Compare lines and remove duplicates while optionally preserving order and ignoring case or whitespace, suitable for cleaning exported lists and logs.',
    'text-remove-numbers': 'Remove digits or specified characters according to your rules, cleaning redundant symbols in bulk from text copied out of PDFs and web pages.',
    'text-repeat': 'Repeat a piece of text a set number of times, per block or per line, with prefix, suffix and separator options for test data, placeholders and bulk content.',
    'text-replace-advanced': 'Bulk replace text using plain or regex rules with case sensitivity, whole-word matching and group references, ideal for cleaning logs and batch rewriting.',
    'text-reverse': 'Reverse the character or line order of your text for palindrome checks, playful copy and encoding debugging, all done locally.',
    'text-reverse-lines': 'Reverse the order of lines with an option to keep or drop blank lines, useful for reversing checklists, replaying steps and handling reverse-chronological data.',
    'text-shuffle': 'Randomly reorder lines or character sequences for draws, random sampling and classroom demos, with a repeatable shuffle in the browser.',
    'text-sort': 'Sort text lines alphabetically, numerically or by length in ascending or descending order with optional deduplication for rosters, parameter tables and log entries.',
    'text-sort-advanced': 'Sort with lexicographic, numeric, line-length, random or multi-column field modes plus ascending/descending and dedup options for structured text cleanup.',
    'text-split': 'Split long text into chunks by line, paragraph, custom delimiter or fixed length for batch processing and block-wise handling.',
    'text-stats': 'Count characters, words, lines, word frequency and readability metrics with separate Chinese and English counts for drafting, length-limit checks and content review.',
    'text-to-banner': 'Turn text into a horizontal banner preview with adjustable colours and fonts, exportable as an image for headline graphics, covers and social posts.',
    'text-to-slug': 'Turn a title or Chinese text into a URL-friendly slug (lower case, hyphen separated, stop words removed) for permalinks, routes and file names.',
    'text-trim': 'Strip leading, trailing and in-line extra whitespace, compress consecutive blank lines and optionally remove full-width spaces after copying from web pages or spreadsheets.',
    'text-wrap': 'Wrap paragraphs automatically at a given width or pad each line to a fixed length with prefixes or suffixes, for terminals, emails and fixed-width reports.',
    'unicode-normalize': 'Normalise text with NFC, NFD, NFKC or NFKD to unify visually identical characters before comparison, search or storage.',
    'unit-price-compare': 'Enter price, quantity or weight for several products to compute and compare unit prices, showing the best value per standard unit for purchasing decisions.',
    'upside-down-text': 'Flip text upside down to generate inverted characters that can be copied into playful signatures, puzzles and social nicknames, converted instantly in the browser.',
    'zalgo-text': 'Stack combining characters over your text to create a Zalgo glitch effect with adjustable intensity for memes, headlines and playful styling.',
}

DEFAULT_NOTE = [
    '本工具纯前端运行，数据不会上传到服务器',
    '建议在主流浏览器（Chrome/Safari/Firefox/Edge）中使用',
    '计算结果仅供参考，请以实际应用场景为准',
]


def load(path):
    with open(path, encoding='utf-8') as f:
        return json.load(f)


# 候选写盘格式（biz-body.json 现为紧凑格式，盲目 indent=2 重写会造成整文件 diff，
# 故按原格式探测后回写）
_CANDIDATES = (
    dict(indent=0, separators=(',', ':')),
    dict(indent=1, separators=(',', ':')),
    dict(indent=1),
    dict(indent=2, separators=(',', ':')),
    dict(indent=2),
    dict(indent=None, separators=(',', ':')),
    dict(indent=None),
)


def dump_like(path, data, orig_raw):
    """按文件原有 JSON 格式回写：逐一尝试候选格式，取能无损还原原串的那个。"""
    body_raw = orig_raw.rstrip('\n')
    trailing = '\n' if orig_raw.endswith('\n') else ''
    try:
        orig = json.loads(orig_raw)
    except Exception:
        orig = None
    if orig is not None:
        for c in _CANDIDATES:
            try:
                if json.dumps(orig, ensure_ascii=False, **c) == body_raw:
                    return json.dumps(data, ensure_ascii=False, **c) + trailing
            except Exception:
                continue
    return json.dumps(data, ensure_ascii=False, indent=2) + trailing


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--dry-run', action='store_true')
    ap.add_argument('--apply', action='store_true')
    a = ap.parse_args()
    if not a.dry_run and not a.apply:
        ap.error('需指定 --dry-run 或 --apply')

    slugs = sorted(
        os.path.basename(f)[:-5]
        for f in glob.glob(os.path.join(TOOLS, '*.html'))
        if os.path.basename(f) != 'index.html'
    )
    missing_name = [s for s in slugs if s not in NAME]
    missing_intro = [s for s in slugs if s not in INTRO]
    if missing_name or missing_intro:
        print('!! NAME/INTRO 缺条目:', missing_name, missing_intro)
        return 1

    ov_raw = open(OV, encoding='utf-8').read()
    body_raw = open(BODY, encoding='utf-8').read()
    gis_raw = open(GIS, encoding='utf-8').read()
    ov = json.loads(ov_raw)
    body = json.loads(body_raw)
    gis = json.loads(gis_raw)

    chg_en = chg_ed = chg_body = added_body = added_gis = chg_zh = 0

    for slug in slugs:
        name = NAME[slug]
        intro = INTRO[slug]
        k = 'biz/' + slug

        e = ov.get(k)
        if not isinstance(e, dict):
            e = {'ind': 'biz'}
        if e.get('en') != name:
            chg_en += 1
        if e.get('ed') != intro:
            chg_ed += 1
        e['en'] = name
        e['ed'] = intro
        e.setdefault('ind', 'biz')
        ov[k] = e

        b = body.get(slug)
        if not isinstance(b, dict):
            b = {}
            added_body += 1
            print('  + biz-body.json 新增条目:', slug)
        if b.get('title') != name or b.get('h1') != name or b.get('intro') != intro:
            chg_body += 1
        b['title'] = name
        b['h1'] = name
        b['intro'] = intro
        en = b.get('en')
        if not isinstance(en, dict):
            en = {}
        en['title'] = name
        en['h1'] = name
        en['intro'] = intro
        b['en'] = en
        body[slug] = b

        g = gis.get(slug)
        if not isinstance(g, dict):
            g = {}
            added_gis += 1
            print('  + biz.json 新增条目:', slug)
        # 中文态缺口补齐：只填空，不覆盖已有中文
        z = g.get('zh-CN')
        if not isinstance(z, dict):
            z = {}
        if not (z.get('title') or '').strip():
            zt = ZH_TITLE.get(slug)
            if zt:
                z['title'] = zt
                z['h1'] = zt
                chg_zh += 1
        if not (z.get('intro') or '').strip():
            zi = ZH_INTRO.get(slug)
            if zi:
                z['intro'] = zi
                chg_zh += 1
        g['zh-CN'] = z
        eu = g.get('en-US')
        if not isinstance(eu, dict):
            eu = {}
        eu['title'] = name
        eu['h1'] = name
        eu['intro'] = intro
        g['en-US'] = eu
        if 'note' not in g:
            g['note'] = list(DEFAULT_NOTE)
        gis[slug] = g

    # 孤儿/跨行业残留键清理：本行业数据源中不属于 biz 工具页的键一律删除。
    # 注意：不能只判「全站无同名页面」——text-diff 实属 it 行业（tools/it/text-diff.html），
    # 全站有同名页但不属于 biz，按旧口径会被漏掉并残留英文占位串（与 fun 的 number-memory 同坑）。
    biz_slugs = set(slugs)
    orph_body = [k for k in list(body.keys()) if k not in biz_slugs]
    for k in orph_body:
        del body[k]
    orph_ov = [k for k in list(ov.keys())
               if k.startswith('biz/') and k.split('/', 1)[1] not in biz_slugs]
    for k in orph_ov:
        del ov[k]
    orph_gis = [k for k in list(gis.keys()) if k not in biz_slugs]
    for k in orph_gis:
        del gis[k]

    print('\n--- 汇总 ---')
    print('biz 工具页:', len(slugs))
    print('_en_override  en 更新:', chg_en, ' ed 更新:', chg_ed)
    print('biz-body 更新:', chg_body, ' 新增:', added_body)
    print('biz.json 更新 en-US:', len(slugs), ' 新增条目:', added_gis, ' 中文 title/intro 补齐:', chg_zh)
    print('孤儿键删除  body:', len(orph_body), ' _en_override:', len(orph_ov), ' biz.json:', len(orph_gis))
    if orph_body:
        print('   body:', orph_body)
    if orph_ov:
        print('   ov  :', orph_ov)
    if orph_gis:
        print('   gis :', orph_gis)

    if a.dry_run:
        print('\n[dry-run] 未写盘')
        return 0

    open(OV, 'w', encoding='utf-8').write(dump_like(OV, ov, ov_raw))
    open(BODY, 'w', encoding='utf-8').write(dump_like(BODY, body, body_raw))
    open(GIS, 'w', encoding='utf-8').write(dump_like(GIS, gis, gis_raw))
    print('\n已写盘:', OV, BODY, GIS)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
