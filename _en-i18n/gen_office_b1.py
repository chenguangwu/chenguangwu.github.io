#!/usr/bin/env python3
import os, json, re, sys

ROOT = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(ROOT, 'work', 'office')
OUT = os.path.join(ROOT, '..', 'i18n', 'tools', 'en', 'office')
CJK = re.compile(r'[\u4e00-\u9fff]')
CNP = re.compile(r'[，。、；：！？（）「」『』]')
EXTRA = {}


def build(slug, en_list):
    wj = json.load(open(os.path.join(WORK, slug + '.json'), encoding='utf-8'))
    items = wj.get('items', [])
    if len(en_list) != len(items):
        print('LEN MISMATCH', slug, len(en_list), len(items))
        sys.exit(1)
    mp = {}
    for it, en in zip(items, en_list):
        if it.get('src_diff') and it.get('zh_src') and 'related-tool' not in it.get('loc', ''):
            z = it['zh_src'].strip()
        else:
            z = it.get('zh', '').strip()
        if CJK.search(en) or CNP.search(en):
            print('BAD EN', slug, repr(z), repr(en))
            sys.exit(1)
        mp[z] = en
    for z, en in EXTRA.get(slug, {}).items():
        if CJK.search(en) or CNP.search(en):
            print('BAD EXTRA', slug, repr(z), repr(en))
            sys.exit(1)
        mp[z] = en
    return mp


def write(slug, mp):
    wj = json.load(open(os.path.join(WORK, slug + '.json'), encoding='utf-8'))
    name = wj.get('exist_en') or wj.get('name') or slug
    out = {'slug': slug, 'industry': 'office', 'name': name, 'map': mp}
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, slug + '.json'), 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
        f.write('\n')
    print('WROTE', slug, '(+%d)' % len(mp))
def main():
    # ---------------- excel-formula-reference (16) ----------------
    write('excel-formula-reference', build('excel-formula-reference', [
        "📊 Excel Formula Quick Reference",
        "Enter a keyword to quickly look up common formulas and their usage.",
        "/ Excel Formula Quick Reference",
        "📖 Read the \"excel-formula-reference User Guide\"",
        "Common function meanings: SUM for totals, AVERAGE for means, IF for conditional logic, VLOOKUP for vertical lookup, COUNTIF for conditional counting, SUMIFS for multi-condition totals, and INDEX combined with MATCH for lookup. Relative references shift as you fill, absolute references lock rows and columns with $, and mixed references lock only the row or only the column.",
        "📚 Deep dive: Excel Formula Quick Reference",
        "When writing a monthly sales report, you often need to recall the parameter order and syntax of VLOOKUP, SUMIFS, IF and similar functions; just type the function name in the search box of the quick reference to jump straight to the syntax template and example.",
        "Before building a dashboard, compare the applicable scenarios of XLOOKUP and VLOOKUP, and confirm whether your Excel version supports dynamic array functions, so you avoid writing the wrong reference style.",
        "When training colleagues, turn the key points of high-frequency formulas such as SUMIFS multi-condition totals and COUNTIFS counting into quick-reference entries, cutting the repeated cost of digging through help docs.",
        "Example: use SUMIFS to total sales for a given region",
        "Assume column A holds regions and column B holds sales; to total the East China region: =SUMIFS(B:B, A:A, \"East China\"). You can copy this syntax template straight from the quick reference and swap the region and criteria for your own fields, with no need to memorize parameter order.",
        "How do I look up a function quickly?",
        "Type the function name (such as VLOOKUP, IF, SUMIFS) into the search box at the top of the page to filter and highlight the matching entry, without scrolling through a long list.",
        "What if I cannot remember the parameter order?",
        "Every formula gives a standard syntax template with parameter notes, so you can fill in the blanks from the template; optional parameters are flagged separately, which avoids wrong entries that trigger #VALUE! errors.",
        "Search: VLOOKUP / IF / SUMIFS",
    ]))

    # ---------------- flowchart (26) ----------------
    write('flowchart', build('flowchart', [
        "📄 Flowchart Drawing Tool",
        "The flowchart drawing tool is built on the open-source diagram engine Mermaid and generates professional, polished diagrams from concise text code. It supports seven common diagram types - flowchart, sequence diagram, Gantt chart, class diagram, state diagram, ER diagram and pie chart. You edit the code on the left and see a live preview on the right for WYSIWYG results, and can export SVG vector graphics or PNG images with one click. All computation and rendering happen locally in your browser, so no data is uploaded and your work stays private.",
        "/ Flowchart Drawing",
        "📖 Read the \"Flowchart Drawing Tool User Guide\"",
        "Flowchart",
        "Sequence Diagram",
        "Gantt Chart",
        "Class Diagram",
        "State Diagram",
        "ER Diagram",
        "Pie Chart",
        "Mermaid Code",
        "Indent · Auto-saved)",
        "💡 Tip: pick a diagram type above to load its example; after you edit the code the diagram renders automatically (500ms debounce). Everything is processed only in your local browser and is never uploaded to a server.",
        "📚 Deep dive: Flowchart Drawing Tool",
        "When mapping out a business process or approval flow, use shapes to spell out the nodes and branches of start -> decision -> handling -> end, which makes it easier to explain and align with your team.",
        "When writing a technical proposal, draw an interface-call sequence diagram that visualizes the request and response order between services, reducing communication ambiguity.",
        "When preparing a project report, use architecture or class diagrams to express module relationships, switch among the seven diagram types and export an image to drop into your document.",
        "Example: draw a decision flowchart with Mermaid syntax",
        "Input:\ngraph TD\n  A[Start] --> B{Decision}\n  B -->|Yes| C[Process]\n  B -->|No| D[End]\nThe page renders in real time (500ms debounce); once it looks right, click \"Export SVG / PNG\" to get a vector or raster image.",
        "Which diagram types are supported?",
        "Seven built-in diagram types can be switched with one click, covering flowchart, sequence diagram, class diagram, state diagram and other common structures, and each switch re-renders with the matching syntax.",
        "Will my drawing be lost?",
        "Edits are auto-saved to local browser storage, so refreshing the page loses nothing; export supports both SVG (vector, editable afterwards) and PNG (raster).",
        "About \"Flowchart Drawing Tool\"",
        "Enter Mermaid code here, for example:\nflowchart TD\n    A[Start] --> B[End]",
    ]))

    # ---------------- index (23) ----------------
    write('index', build('index', [
        "📄 Office Document Tools",
        "Office Documents",
        "Office Document Tools",
        "PDF Merge Tool",
        "Select multiple PDF files, drag to reorder them, then merge them with one click. All processing happens locally in your browser and files are never uploaded to the server.",
        "PDF Split Tool",
        "Upload a PDF and extract the pages you want by page range or visual selection to build a new PDF. All processing happens locally in your browser and files are never uploaded.",
        "PDF Page Rotate Tool",
        "Rotate PDF page orientation entirely in the browser, supporting single-page, batch and rotate-all modes with live preview, and files are never uploaded to the server.",
        "Excel Formula Quick Reference",
        "Quick reference for common Excel functions and syntax",
        "Flowchart Drawing Tool",
        "Online flowchart drawing with draggable nodes and connectors for flows, algorithms and org charts, built-in common shapes and styles, exports PNG/SVG, ideal for documents and reports, pure front-end.",
        "Mind Map Editor",
        "Write the hierarchy on the left using Markdown indentation and see the mind map generated live on the right, with zoom, drag and export support.",
        "About \"Office Document Tools\"",
        "The Office Document Tools collection gathers 6 free online tools covering the common calculation, conversion and lookup needs of office document scenarios. Whether you are a practitioner in the field, a student or an ordinary user, you will find ready-to-use utilities here. Every tool runs entirely in the browser and never uploads data to the server, so your privacy is protected.",
        "The office document tools listed on this page include (a few representative tools):",
        "These tools help you finish common office document tasks quickly, with no need to memorize complex formulas or do manual conversions - just enter the inputs and get the result.",
        "Do the office document tools require a download or an account?",
        "No. Every tool on this page is a pure front-end online tool: open the page and use it right away, with no software to install, no account to register, and no data uploaded.",
        "Are the office document tool results accurate? Is the data safe?",
        "The tools compute locally in your browser based on public mathematical formulas and general industry standards, so results are available instantly. All computation happens locally on your device and no data is uploaded to the server, so your privacy is fully protected.",
    ]))


if __name__ == '__main__':
    main()
