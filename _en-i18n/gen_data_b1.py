#!/usr/bin/env python3
import os, json, re, sys
ROOT = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(ROOT, 'work', 'data')
OUT = os.path.join(ROOT, '..', 'i18n', 'tools', 'en', 'data')
CJK = re.compile(r'[\u4e00-\u9fff]')
CNP = re.compile(r'[，。、；：！？（）「」『』]')
DISCL = "Free online tool, processed entirely in the browser, no data uploaded, your privacy and security protected."
EXTRA = {}
def build(slug, en_list):
    wj = json.load(open(os.path.join(WORK, slug + '.json'), encoding='utf-8'))
    items = wj.get('items', [])
    if len(en_list) != len(items):
        print('LEN MISMATCH', slug, len(en_list), len(items)); sys.exit(1)
    mp = {}
    for it, en in zip(items, en_list):
        if it.get('src_diff') and it.get('zh_src') and 'related-tool' not in it.get('loc', ''):
            z = it['zh_src'].strip()
        else:
            z = it.get('zh', '').strip()
        if CJK.search(en) or CNP.search(en):
            print('BAD EN', slug, repr(z), repr(en)); sys.exit(1)
        mp[z] = en
    for z, en in EXTRA.get(slug, {}).items():
        if CJK.search(en) or CNP.search(en):
            print('BAD EXTRA', slug, repr(z), repr(en)); sys.exit(1)
        mp[z] = en
    return mp
def write(slug, mp):
    wj = json.load(open(os.path.join(WORK, slug + '.json'), encoding='utf-8'))
    name = wj.get('exist_en') or wj.get('name') or slug
    out = {'slug': slug, 'industry': 'data', 'name': name, 'map': mp}
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, slug + '.json'), 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1); f.write('\n')
    print('WROTE', slug, '(+%d)' % len(mp))
def main():
    write('index', build('index', [
        "📊 Data Analysis Tools",
        "Data Analysis",
        "Data analysis tools",
        "Enter a data series to generate bar, pie, scatter, radar, area and other SVG charts with export support, completing data visualization without any backend.",
        "Enter text or a link to generate the matching barcode or QR code payload in common encoding formats, making it easy to record material labels and information quickly.",
        "A JSON formatting tool that validates, formats and minifies JSON data entirely in the local browser with no upload, ideal for API debugging.",
        "Generate random passwords of a given length and character set, with adjustable ratios of upper/lower case, digits and symbols, produced purely in the browser with no storage, suitable for account signup and temporary passcodes.",
        "Generate random verification codes of a given length and character set (digits / letters / mixed) for form demos, teaching samples and local testing, and the result can be copied.",
        "Report (auto-generate/send) templates",
        "Generate fillable report templates from fields and styles, with preset headers, footers and summary rows, ready to export as printable or fill-in reports; the structure is produced purely in the browser and can be copied.",
        "Enter a data set to group it automatically and draw a frequency distribution histogram, with adjustable bin width and boundaries, for statistics exploration and distribution visualization, rendered instantly in the browser.",
        "Generate random dates within a given start and end range with a custom format, for quickly building test data, scheduling simulations and demo samples.",
        "Randomly generate HEX or RGB colors, lock the values you like and copy them, for color inspiration, placeholder colors and interface prototypes, generated locally with no upload.",
        "Convert CSV data to a JSON array locally in the browser, with customizable delimiter and header handling.",
        "Randomly combine built-in surname and given-name pools to generate Chinese names, with settable gender and character count, for test data, novel characters and sample information, generated purely in the browser.",
        "Randomly draw and stitch sentences or paragraphs from a built-in corpus for placeholder copy, layout demos and writing inspiration, generated in the browser and copyable.",
        "Generate random integers or floats within a set range, with batch and deduplication support, for draws, sampling, simulation and test data construction, generated instantly in the browser.",
        "Paste or upload CSV data to automatically parse the column structure and count the type, null count and distribution of each column, helping with data preview and pre-cleaning checks.",
        "Import tabular data and choose rows, columns and an aggregation (sum / count / average) to build a two-dimensional pivot summary table for multi-dimensional analysis and reporting.",
        "Import a numeric matrix to automatically draw a histogram, box plot or heatmap where color depth maps to value, for insight into the distribution and correlation of multi-dimensional data.",
        "A data cleaning tool that tidies text and CSV data (dedupe, drop empties, format), running purely in the browser with no upload, suited to table preprocessing.",
        "About Data Analysis Tools",
        "This Data Analysis Tools collection gathers 17 free online tools covering the common calculation, conversion and lookup needs of data analysis scenarios. Whether you are a practitioner in the field, a student or an ordinary user, you will find ready-to-use practical tools here. Every tool runs purely in the browser and never uploads data to a server, so your privacy is protected.",
        "The data analysis tools collected on this page include (some representative tools):",
        "These tools help you finish common data analysis tasks quickly, with no need to memorize complex formulas or convert values by hand: enter and you get the result.",
        "Do the data analysis tools need a download or registration?",
        "No. All data analysis tools on this page are pure front-end online tools: open the page and use them right away, with no software to install, no account to register and no data uploaded.",
        "Are the results of the data analysis tools accurate, and is my data safe?",
        "The tools compute in your local browser based on public mathematical formulas and general industry standards, so results are available instantly. All computation happens on your own device, data is never uploaded to a server, and your privacy is protected.",
    ]))
    write('data-cleaner', build('data-cleaner', [
        "🔎 Data Cleaner",
        "Clean text and CSV data (dedupe / drop empties / format)",
        "Data cleaning processes row by row according to rules: dedupe = compare whole rows or a chosen column and keep the first occurrence; drop empties = remove fully empty rows and cells containing only whitespace; format = uniformly trim leading and trailing whitespace, convert full-width to half-width, and normalize dates to YYYY-MM-DD; rows after cleaning = original rows − duplicate rows − empty rows.",
        "Input data (one record per line)",
        "Zhang San\nLi Si\nZhang San\nWang Wu\n\nZhao Liu\n  Li Si\nWang Wu\nQian Qi\nSun Ba\nWang Wu\nabc",
        "Cleaning operations (multi-select)",
        "Maximum length per line (0 = no limit)",
        "🔎 Clean",
        "📋 Result",
        "Original count / after processing",
        "Executed",
        "📚 Deep Dive: Data Cleaning",
        "List dedupe: deduplicate collected lists of phone numbers or email addresses to avoid duplicate records when bulk mailing or importing.",
        "Null cleanup: batch delete blank rows and leading/trailing spaces to tidy irregular text copied from web pages.",
        "Format unification: normalize fields that mix full-width and half-width,",
        "so that later matching and comparison work properly.",
        "Dedupe a signup sheet by dropping empties",
        "Paste a name list containing blank lines and duplicates, choose drop empty lines plus exact dedupe, and the tool outputs a clean deduplicated list with the number of removed records, ready to paste back into the spreadsheet.",
        "Does dedupe work on the whole row or on a column?",
        "By default duplicates are judged by the whole row content; to dedupe by a specific column, first reshape the data into a single column or use the page's designated column function (as the page states).",
        "Does it modify the original data?",
        "No, cleaning produces a new result locally while the original text stays in the input box, so you can adjust the rules at any time.",
        "Is sensitive data safe?",
        "Everything is processed locally in the browser with no upload, which suits tidying internal lists that contain phone numbers and similar data.",
        "About Data Cleaner",
        "Data Cleaner is an online tool in the data analysis field. Data analysis tools that help you process and visualize data quickly.",
        "One record per line",
        "Data after cleaning",
    ]))
    write('chart-generator', build('chart-generator', [
        "📈 Chart Generator",
        "Generate SVG charts from data",
        "Chart type",
        "Data (per line: label, value, optional color)",
        "Jan,30,#3b82f6\nFeb,45,#10b981\nMar,60,#f59e0b\nApr,50,#ef4444\nMay,75,#8b5cf6\nJun,90,#ec4899",
        "👆 Enter data",
        "📚 Deep Dive: Chart Generator",
        "Reporting graphics: draw quarterly metrics directly as bar or pie charts and export SVG to embed in documents and slides, avoiding blurry screenshots.",
        "Share comparison: use a pie chart to show traffic share by channel, quickly judge whether the structure is imbalanced, and support an operations review.",
        "Correlation observation: use a scatter plot to observe the relationship between two variables and initially identify linear trends or outlier points.",
        "Channel share pie chart",
        "Enter \"Search 40 / Direct 25 / Social 20 / Other 15\", pick the pie chart, and the tool splits by share and annotates",
        "each slice, then the exported SVG is ready for a weekly report.",
        "Which chart types are supported?",
        "Common types such as bar, pie, scatter, radar and area are built in; the page's selectable list is authoritative, and all rendering is local SVG.",
        "What is the export format?",
        "SVG vector output is the default and scales without loss; some scenarios also support PNG, so the page buttons are authoritative.",
        "Is the data saved to a server?",
        "No, the data only takes part in drawing inside your local browser and is not retained after a refresh or a page close, which suits quickly charting sensitive internal data.",
        "About Chart Generator",
        "Chart Generator is an online tool in the data analysis field. Data analysis tools that help you process and visualize data quickly.",
        "📈 Reading the Result",
        "Chart Generator: renders the input data into a visual chart (bar / line / pie / scatter and more), and the result is the graphic itself.",
        "Used for reporting, trend observation and data communication; pick a suitable chart type (bar for category comparison, line for trends, pie for shares). Data anomalies show up directly in the chart.",
    ]))
    write('csv-analyzer', build('csv-analyzer', [
        "📊 CSV Analyzer",
        "Parse CSV data and profile every column",
        "/ CSV Analysis",
        "CSV analysis profiles each column: row count = data rows (excluding the header), column count = number of fields in the first row; numeric columns report the minimum, maximum, mean = Σvalue ÷ valid count and median (the middle value after sorting, or the average of the two middle values); null rate = empty cells ÷ total cells × 100%; column type is judged by the share of numeric, date and text among the non-null values.",
        "Tab (\\t)",
        "name,age,score,city\nZhang San,25,85.5,Beijing\nLi Si,30,92.0,Shanghai\nWang Wu,28,78.5,Guangzhou\nZhao Liu,35,88.0,Shenzhen\nQian Qi,22,95.5,Hangzhou\nSun Ba,40,72.0,Chengdu",
        "👆 Paste CSV data",
        "📚 Deep Dive: CSV Analyzer",
        "Pre-cleaning check: before importing a CSV, profile the null rate and type of each column to decide which columns need filling or converting first.",
        "Anomaly prescreen: look at the min, max and distribution of numeric columns to quickly spot inconsistent units or obviously mis-entered outliers.",
        "Structure confirmation: check column names and row counts to confirm the exported fields match expectations and avoid misalignment in later pivots or joins.",
        "Null check on a user table",
        "Upload a CSV with \"name, phone, city\" and the tool shows a null rate of 8% for the phone column and 2% for city, so you can fill the missing fields before aggregating.",
        "How large a file can it handle?",
        "Parsing runs locally and is limited by browser memory; for very large files, sample or split the data before analyzing to avoid freezing.",
        "Is the type detection accurate?",
        "Types such as text, numeric and date are inferred from sample values and are for reference only; mixed content is marked as text, and key columns should be reviewed by hand.",
        "Can the analysis results be exported?",
        "Usually you can copy the statistics or export a summary; the page buttons are authoritative, and the whole process runs locally.",
        "About CSV Analyzer",
        "CSV Analyzer. Data analysis tools that help you process and visualize data quickly.",
        "CSV analysis: gives a summary profile of tabular data, missing-value detection and a basic pivot; the result shows row/column counts, missing items and key statistics such as the mean and extremes.",
        "Used for a health check before data cleaning and quick insight; complex analysis is better done in a dedicated tool. This tool processes data locally and never uploads it.",
    ]))
    write('pivot-table', build('pivot-table', [
        "📊 Pivot Table",
        "Two-dimensional aggregation table (sum / count / average)",
        "/ Data Pivot",
        "region,product,sales,profit\nNorth,A,100,20\nNorth,B,150,30\nEast,A,200,40\nEast,B,180,36\nSouth,A,120,24\nSouth,B,90,18\nNorth,A,110,22\nEast,B,160,32",
        "Row field (column name)",
        "Column field (column name)",
        "Value field (column name)",
        "Aggregation",
        "👆 Configure and generate",
        "📚 Deep Dive: Pivot Table",
        "Sales summary: pivot the sum by region and month to see each area's month-by-month trend at a glance.",
        "Frequency count: count by category to find which record type has the largest share.",
        "Average comparison: average by group to compare the average order value or session length across channels.",
        "Sales by region × month",
        "Import the three columns \"region, month, amount\", pick region as the row, month as the column and amount (sum) as the value; the tool outputs a two-dimensional table where each cell is the total for that region and month, ready to report directly.",
        "Which aggregations are supported?",
        "Common ones such as sum, count and average; the page's selectable list is authoritative, and all computation is local.",
        "How are nulls handled?",
        "Empty cells are usually ignored during aggregation; if they should count as 0, clean the data first, and follow the page's description for the conclusion.",
        "Will big data be slow?",
        "Computation runs locally and is limited by browser performance; for very large data, filter or sample before pivoting.",
        "About Pivot Table",
        "Pivot Table is an online tool in the data analysis field. Data analysis tools that help you process and visualize data quickly.",
    ]))
    write('data-visualizer', build('data-visualizer', [
        "📈 Data Visualizer",
        "Histogram / box plot / heatmap",
        "Numeric data (separated by space, comma or newline)",
        "Number of bins (histogram)",
        "📈 Render",
        "📦 Box Plot",
        "🌡️ Heatmap (time distribution)",
        "📚 Deep Dive: Data Visualizer",
        "Distribution exploration: plot a sample as a histogram to quickly judge central tendency and skewness, helping you choose later statistical methods.",
        "Outlier identification: use a box plot to inspect each group's",
        "and interquartile range, locating samples that are unusually high or low.",
        "Correlation observation: use a heatmap to show correlation strength between variables and initially surface strongly correlated dimensions for deeper investigation.",
        "Histogram of score distribution",
        "Import 200 scores, pick the histogram and set the bin width to 10; the tool shows frequencies for bands such as 60-70 and 70-80, so you can see at a glance that the peak sits in the 80s.",
        "Which charts are supported?",
        "Common statistical charts such as histogram, box plot and heatmap are built in; the page's selectable list is authoritative, and all rendering is local.",
        "How should the bin width be chosen?",
        "You can set the bin width and boundaries manually; too small a width brings out noise, too large hides the structure, so try a few",
        "values.",
        "How should a heatmap be read?",
        "A deeper color usually means a larger value (or a stronger correlation); the exact mapping follows the page legend, and it is for exploratory reference only.",
        "About Data Visualizer",
        "Data Visualizer is an online tool in the data analysis field. Data analysis tools that help you process and visualize data quickly.",
    ]))


if __name__ == '__main__':
    main()
