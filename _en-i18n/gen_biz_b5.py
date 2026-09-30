# -*- coding: utf-8 -*-
"""biz batch5（10 工具）per-tool 英文词典生成器。"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gen_biz_apply import apply_tool, IND

# ===== text-extract-numbers =====
apply_tool('text-extract-numbers', '提取数字', 'Number Extractor', {
    '整数': 'Integers', '小数': 'Decimals', '负数': 'Negatives',
    '科学计数法': 'Scientific notation', '百分数': 'Percentages',
    '去重': 'Deduplicate', '排序（数值升序）': 'Sort (ascending numeric)',
    '共找到:': 'Found:', '个': ' numbers', '求和:': 'Sum:', '平均:': 'Average:',
    '📋 提取结果': '📋 Extracted results',
    '数据清洗': 'Data cleaning',
    '数据清洗：把夹杂文字的数字单独抽出，准备入库。': 'Data cleaning: pull out numbers tangled with text on their own, ready for import.',
    '：把夹杂文字的数字单独抽出，准备入库。': ': pull out numbers tangled with text on their own, ready for import.',
    '从报表/文本抽金额与数值：得到可求和的数字列表，做快速统计。': 'Pull amounts and values from reports or text: get a summable number list for quick stats.',
    '校验合计：抽全部数值后核对是否等于预期总额。': 'Verify totals: after extracting all values, check they equal the expected sum.',
    '从明细抽金额': 'Extract amounts from line items',
    '文本「苹果 9.9 元，香蕉 5.5 元，共 15.4 元」，提取数字得 9.9、5.5、15.4，可一键求和验证 15.4 是否正确。': 'The text "Apple 9.9, Banana 5.5, total 15.4" yields 9.9, 5.5, 15.4; one-click sum verifies whether 15.4 is correct.',
    '千分位和小数点怎么处理？': 'How are thousands separators and decimal points handled?',
    '默认识别「1,234.56」为单值；若把逗号当分隔符需切换模式，否则「1,234」会被拆成 1 和 234。': 'By default "1,234.56" is one value; if commas are separators, switch mode, otherwise "1,234" splits into 1 and 234.',
    '负数和小数保留吗？': 'Are negatives and decimals kept?',
    '保留。负号与小数点均识别，输出为数值便于后续计算。': 'Yes. Minus signs and decimal points are recognised, output as numbers for further calculation.',
    '如何使用提取数字': 'How to use Number Extractor',
}, display='提取数字')

# ===== text-extract-urls =====
apply_tool('text-extract-urls', '提取 URL', 'URL Extractor', {
    '去重': 'Deduplicate', '仅 http/https': 'HTTP/HTTPS only',
    '移除查询参数': 'Strip query parameters', '竖线': 'Pipe',
    '共找到:': 'Found:', '个 URL': ' URLs',
    '📋 提取结果': '📋 Extracted results',
    '从文本批量抽链接：得到可点击/可采集的 URL 清单。': 'Batch-extract links from text: get a clickable / crawlable URL list.',
    '资源盘点：抽页面里所有 http(s) 链接做死链与外链检查。': 'Inventory: pull all http(s) links from a page for dead-link and outbound checks.',
    '数据准备：把散落 URL 汇总去重，导入爬虫或书签。': 'Data prep: gather scattered URLs, deduplicate, import to crawler or bookmarks.',
    '从公告抽链接': 'Extract links from an announcement',
    '文本含「详见 https://a.com/doc 与 http://b.cn/help」，工具抽得两个 URL 并去重，可直接用于批量探测可达性。': 'Text "see https://a.com/doc and http://b.cn/help" yields two URLs and dedupes them, ready for batch reachability probing.',
    '带参数的长链接完整吗？': 'Are long links with parameters kept intact?',
    '完整保留 query（?id=1&t=2）；但末尾标点若紧贴会被误含，建议抽取后 trim 或启用「止于标点」模式。': 'The query (?id=1&t=2) is fully kept; but trailing punctuation stuck to the end may be wrongly included - trim after extraction or enable the "stop at punctuation" mode.',
    '相对路径能抽吗？': 'Can relative paths be extracted?',
    '相对路径（/doc/a）不以 http 开头，默认不抽；需结合基址拼接时才算完整 URL。': 'Relative paths (/doc/a) do not start with http and are skipped by default; they count as a full URL only when joined with a base address.',
}, display='提取 URL')

# ===== text-extract =====
apply_tool('text-extract', '文本提取', 'Smart Text Extractor', {
    '换行符': 'line break',
    '（正则）': ' (regex)',
    '提取结果（每行一项）': 'Extraction results (one per line)',
    '📖 查看「文本智能提取使用指南」': '📖 View the "Smart Text Extractor Guide"',
    '按模式从杂乱文本抽取目标：用正则表达式提取符合规则的片段，如订单号、手机号。': 'Extract targets from messy text by pattern: use regex to pull rule-matching fragments like order numbers or phone numbers.',
    '日志关键信息抽取：从大段日志里捞出报错行或特定字段。': 'Key-info extraction from logs: fish out error lines or specific fields from large log dumps.',
    '数据预处理：为后续表格化先做结构化抽取。': 'Data pre-processing: structure the extraction before tabulating.',
    '抽取订单号': 'Extract order numbers',
    '在长文本里用正则「ORD[0-9]{6}」抽取，得到 ORD100234、ORD100235 等全部订单号列表，可一键导出进一步处理。': 'Use regex "ORD[0-9]{6}" in long text to pull the full order-number list (ORD100234, ORD100235, ...) and export with one click for further processing.',
    '不会写正则怎么办？': 'What if I cannot write regex?',
    '优先用专用提取工具（邮箱/URL/数字等）免写正则；确需自定义时，常用语法如 [0-9] 数字、. 任意、* 重复可在说明里查，或先用小样本试。': 'Prefer dedicated extractors (email / URL / number) to avoid regex; if custom is truly needed, common syntax such as [0-9] for digits, . for any, * for repeat is in the docs, or test on a small sample first.',
    '多行匹配怎么设？': 'How to set multi-line matching?',
    '默认单行；需跨行抽取时开启多行/点号匹配模式（dotall），并注意': 'Single line by default; for cross-line extraction enable multi-line / dotall mode, and mind the ',
    '处理，否则匹配会断。': 'handling, otherwise the match breaks.',
}, display='文本提取')

# ===== text-filter-lines =====
apply_tool('text-filter-lines', '按行过滤', 'Line Filter', {
    '过滤关键词': 'Filter keyword', '匹配模式': 'Match mode', '不包含': 'Exclude',
    '以...开头': 'Starts with', '以...结尾': 'Ends with', '完全匹配': 'Exact match',
    '正则匹配': 'Regex match', '长度大于': 'Length greater than', '长度小于': 'Length less than',
    '忽略大小写': 'Case-insensitive', '去除每行首尾空格': 'Trim each line',
    '跳过空行': 'Skip blank lines', '反选结果': 'Invert selection', '结果:': 'Result:',
    '📋 结果': '📋 Result',
    '大小写': 'letter case', '敏感吗？': 'sensitivity?',
    '大小写敏感吗？': 'Is it case-sensitive?',
    '日志筛选：只保留含「ERROR」或排除「DEBUG」的行，聚焦问题。': 'Log screening: keep only lines containing "ERROR" or excluding "DEBUG" to focus on issues.',
    '名单处理：按关键词包含/不包含过滤，得到目标子集。': 'List processing: filter by keyword include / exclude to get the target subset.',
    '数据预处理：过滤掉空行或特定前缀行，准备下游处理。': 'Data pre-processing: drop blank lines or specific prefixes, ready for downstream use.',
    '只留错误日志': 'Keep error logs only',
    '粘贴 5000 行日志，设「包含 ERROR」，输出仅 23 行错误；再叠加「排除 timeout」可进一步排除已知噪声。': 'Paste 5000 log lines, set "contains ERROR", output only 23 error lines; stacking "exclude timeout" further removes known noise.',
    '支持正则吗？': 'Does it support regex?',
    '支持。简单子串与正则模式两种；复杂条件（如「A 且非 B」）可用正则或组合多次过滤实现。': 'Yes. Both simple substring and regex modes; complex conditions (like "A and not B") use regex or combined multiple passes.',
    '默认敏感，可开忽略大小写；「error」与「ERROR」在敏感模式下是两条不同匹配。': 'Case-sensitive by default; you can enable ignore-case; "error" and "ERROR" are two different matches in sensitive mode.',
}, display='按行过滤')

# ===== text-indent =====
apply_tool('text-indent', '自动缩进', 'Auto Indent Tool', {
    '代码注释': 'code comment', 'Python': 'Python',
    '缩进字符': 'Indent character', '缩进规则': 'Indent rules',
    '大括号 { }': 'Curly braces { }', '小括号 ( )': 'Parentheses ( )',
    '中括号 [ ]': 'Square brackets [ ]', '所有括号': 'All brackets',
    'XML/HTML 标签': 'XML/HTML tags', '去除每行原首尾空格': 'Trim original lines',
    '闭合括号也缩进': 'Indent closing brackets too',
    '📋 结果': '📋 Result',
    '代码格式化：为选中块统一加 2/4 空格或 Tab 缩进。': 'Code formatting: uniformly add 2/4 spaces or Tab indentation to the selected block.',
    '引用与列表排版：给段落批量加悬挂缩进。': 'Quotes and list layout: batch-add hanging indents to paragraphs.',
    '多级结构展示：按层级加缩进，呈现树状层级。': 'Multi-level structure: indent by level to show a tree hierarchy.',
    '给 3 行加 4 空格': 'Add 4 spaces to 3 lines',
    '粘贴 3 行文字，设缩进 4 空格，每行前补「    」，输出整齐缩进块；用于把草稿快速变': 'Paste 3 lines, set 4-space indent, each line gets "    " prepended, output a tidy indented block; quickly turn a draft into ',
    '或引用样式。': 'or a quote style.',
    '空格和 Tab 怎么选？': 'How to choose between spaces and Tab?',
    '团队规范优先；': 'Team convention first; ',
    ' 一般 4 空格、Makefile 必须 Tab。建议统一一种，混用会导致部分语言缩进报错。': ' Generally 4 spaces, Makefile must use Tab. Stick to one; mixing causes indentation errors in some languages.',
    '已有缩进会叠加吗？': 'Does existing indentation stack up?',
    '默认在原有基础上加；如需「设为固定缩进」请先去旧缩进或用「替换模式」，避免越缩越深。': 'By default it adds on top of the original; for "set fixed indent", remove old indentation first or use "replace mode" to avoid runaway nesting.',
}, display='自动缩进')

# ===== text-keep-only =====
apply_tool('text-keep-only', '仅保留指定字符', 'Keep-Only Character Filter', {
    '保留选项': 'Keep options', '数字 (0-9)': 'Digits (0-9)',
    '小写字母 (a-z)': 'Lowercase (a-z)', '大写字母 (A-Z)': 'Uppercase (A-Z)',
    '标点符号': 'Punctuation', '空白字符': 'Whitespace',
    '所有字母（含大小写）': 'All letters (a-z, A-Z)',
    '自定义保留字符集': 'Custom keep set', '自定义保留正则': 'Custom keep regex',
    '启用正则（取匹配项）': 'Enable regex (keep matches)', '区分大小写': 'Case-sensitive',
    '多个匹配用换行连接': 'Join matches with newlines',
    '📋 结果': '📋 Result',
    '反向过滤：只留含目标词的行，删掉其余，聚焦关键内容。': 'Reverse filter: keep only lines containing the target word, drop the rest, focus on key content.',
    '白名单抽取：从混合文本保留特定模式（如保留含订单号行）。': 'Whitelist extraction: keep specific patterns from mixed text (e.g. keep lines with order numbers).',
    '降噪：在混乱日志里只留关心的信号。': 'Noise reduction: keep only the signals you care about in messy logs.',
    '只留含「支付」的行': 'Keep only lines containing "payment"',
    '1000 行文本里设保留「支付」，输出仅 42 行支付相关；与「按条件过滤」的区别是它直接丢弃不匹配行而非仅隐藏。': 'In 1000 lines, set keep "payment", output only 42 payment-related lines; unlike "conditional filter" it drops non-matching lines instead of merely hiding them.',
    '和文本过滤有什么区别？': 'How is it different from text filtering?',
    '文本过滤多为「显示/排除」，本工具是「仅保留匹配、丢弃其余」，输出即子集，适合直接产出目标清单。': 'Text filtering is mostly "show / exclude"; this tool "keeps matches only, drops the rest", output is the subset, ideal for producing a target list directly.',
    '多关键词怎么算？': 'How do multiple keywords work?',
    '可设「任一匹配即保留」或「全部匹配才保留」，按是否需要 AND/OR 语义选择。': 'Set "keep if any matches" or "keep only if all match", choosing by whether you need AND / OR semantics.',
}, display='仅保留指定字符')

# ===== text-line-numbers =====
apply_tool('text-line-numbers', '添加行号', 'Line Number Adder', {
    '行号格式': 'Line number format', '1. （数字+点）': '1. (number + dot)',
    '1) （数字+右括号）': '1) (number + paren)', '[1] （方括号）': '[1] (brackets)',
    '{1} （花括号）': '{1} (braces)', '1: （数字+冒号）': '1: (number + colon)',
    '1 | （数字+竖线）': '1 | (number + pipe)', '1- （数字+短横线）': '1- (number + dash)',
    '> 1 （箭头）': '> 1 (arrow)', '1 （仅数字）': '1 (number only)',
    '起始行号': 'Start number', '填充宽度（0=自动）': 'Pad width (0=auto)',
    '空行不编号': 'Skip blank lines', '用空格分隔行号': 'Separate number with space',
    '行号右对齐': 'Right-align numbers',
    '📋 结果': '📋 Result',
    '代码展示与引用：给片段加 1. 2. 行号，便于讨论时定位「第 N 行」。': 'Code display and citation: add 1. 2. line numbers to a snippet, making it easy to refer to "line N" in discussion.',
    '教学与文档：标注步骤序号，读者可对照。': 'Teaching and docs: label step numbers so readers can follow along.',
    '日志对齐：给截取日志加行号便于回溯。': 'Log alignment: number clipped logs for easy trace-back.',
    '给 5 行加行号': 'Add numbers to 5 lines',
    '粘贴 5 行，设起始 1、格式「N. 」，输出「1. …/2. …」；导出后引用「见第 3 行」一目了然。': 'Paste 5 lines, set start 1, format "N. ", output "1. …/2. …"; after export, "see line 3" is self-explanatory.',
    '能从指定数开始吗？': 'Can it start from a specific number?',
    '可以设起始值（如从 10 开始），适合接在上一段之后连续编号。': 'Yes, set a start value (e.g. from 10), handy for continuous numbering after the previous block.',
    '加号还是点？': 'Plus sign or dot?',
    '支持「N.」「N)」「[N]」等；纯展示用，不影响原文本逻辑。': 'Supports "N.", "N)", "[N]" etc.; display only, does not affect the original text logic.',
}, display='添加行号')

# ===== text-merge =====
apply_tool('text-merge', '多段文本合并', 'Multi-Text Merger', {
    '输入多段文本（每行一段，或用 --- 分隔）': 'Enter text blocks (one per line, or separate with ---)',
    '合并选项': 'Merge options', '无（直接连接）': 'None (direct concat)',
    '每段前缀': 'Prefix per block', '每段后缀': 'Suffix per block',
    '去除每段首尾空格': 'Trim each block', '跳过空段': 'Skip empty blocks',
    '添加序号': 'Add serial numbers', '合并': 'Merge',
    '📋 合并结果': '📋 Merged result',
    '如何使用多段文本合并': 'How to use Multi-Text Merger',
    '多段/多列拼接：把两个列表按行合并（如名字+邮箱成一行）。': 'Multi-block / multi-column join: merge two lists by row (e.g. name + email into one line).',
    '文件片段连接：把分块文本拼成整体，准备发布。': 'File fragment join: stitch chunked text into one whole, ready to publish.',
    '分隔符定制：用逗号/制表符/换行连接，产出 CSV 或表格源。': 'Custom separators: join with comma / tab / newline to produce CSV or table sources.',
    '名字与邮箱按行合并': 'Merge names and emails by row',
    'A 列「张三/李四」、B 列「z@x.com/l@y.com」，按行合并得「张三,z@x.com」「李四,l@y.com」，直接成 CSV 两列。': 'Column A "Zhang/Li", column B "z@x.com/l@y.com", merged by row gives "Zhang,z@x.com" "Li,l@y.com", directly a two-column CSV.',
    '两列行数不等怎么办？': 'What if the two columns have unequal rows?',
    '默认按较短截断或留空补齐（可选）；行数不等会错位，合并前先核对长度。': 'By default truncate to the shorter or pad with blanks (optional); unequal rows misalign, so check lengths before merging.',
    '用什么分隔符？': 'Which separator to use?',
    '逗号/制表符/空格/自定义均可；做 CSV 用逗号时，内容含逗号需转义，建议用制表符更稳。': 'Comma / tab / space / custom all work; for CSV with comma, escape embedded commas - a tab is more robust.',
}, display='多段文本合并')

# ===== text-pad =====
apply_tool('text-pad', '文本填充', 'Text Padding Tool', {
    '文本填充': 'Text Padding', '输入文本（每行单独处理）': 'Input text (each line processed separately)',
    '填充选项': 'Padding options', '填充方向': 'Padding direction',
    '左侧填充（右对齐）': 'Left pad (right align)', '右侧填充（左对齐）': 'Right pad (left align)',
    '两侧填充（居中）': 'Both sides (center)', '目标长度': 'Target length',
    '按字节计算（中文 2 字节）': 'Count by bytes (CJK = 2 bytes)',
    '先去除每行首尾空格': 'Trim each line first',
    '📋 填充结果': '📋 Padded result',
    '📖 查看「文本填充工具使用指南」': '📖 View the "Text Padding Tool Guide"',
    '固定宽度输出：把不等长字符串左补零或右补空格，便于对齐与排序。': 'Fixed-width output: left-pad with zeros or right-pad with spaces for alignment and sorting.',
    '报表与编号：订单号补零到固定位（000123），字典序即数值序。': 'Reports and numbering: zero-pad order numbers to fixed width (000123), so lexicographic order equals numeric order.',
    '终端表格：用空格填充使列对齐。': 'Terminal tables: pad with spaces to align columns.',
    '编号补零到 6 位': 'Zero-pad numbers to 6 digits',
    '输入「123」，左补零到 6 位得「000123」；配合排序时「000123」自然小于「000999」，避免「123」排在「99」后的乱序。': 'Input "123", left-pad to 6 digits gives "000123"; when sorting, "000123" naturally precedes "000999", avoiding the "123 after 99" disorder.',
    '中文怎么算宽度？': 'How is CJK width counted?',
    '中文按 2 字符宽、英文 1 宽；填充对齐时若要视觉对齐需用支持 CJK 宽度的计算，否则出现错位。': 'CJK counts as 2 wide, English as 1; for visual alignment use a CJK-aware width calculation, otherwise misalignment appears.',
    '超出目标长度呢？': 'What if it exceeds the target length?',
    '超长默认截断或原样保留（可选）；补零编号建议先确认最大位数，避免截断高位。': 'By default over-long is truncated or kept as-is (optional); for zero-padded numbers confirm the max digits first to avoid truncating high-order digits.',
}, display='文本填充')

# ===== text-prefix-suffix =====
apply_tool('text-prefix-suffix', '批量添加前缀后缀', 'Prefix & Suffix Adder', {
    'SQL': 'SQL',
    '输入文本（每行处理）': 'Input text (each line processed)',
    '前缀（可留空）': 'Prefix (may be empty)', '后缀（可留空）': 'Suffix (may be empty)',
    '前缀与后缀相互独立，可只填前缀、只填后缀，或两者都留空（仅做去空格 / 跳空行 / 加序号处理）。': 'Prefix and suffix are independent; fill only prefix, only suffix, or leave both empty (just trim / skip blanks / add serial numbers).',
    '去除每行首尾空格': 'Trim each line', '跳过空行': 'Skip blank lines',
    '添加序号': 'Add serial numbers', '序号零填充': 'Zero-pad serial', '反向序号': 'Reverse serial',
    '序号起始值': 'Serial start value', '序号格式': 'Serial format',
    '前缀中：1. text': 'Prefix form: 1. text', '独立：1) text': 'Standalone: 1) text',
    '括号：[1] text': 'Brackets: [1] text', '大括号：{1} text': 'Braces: {1} text',
    '📋 结果': '📋 Result',
    '批量加引号/括号：给每行内容包上单引号或圆括号，快速拼': 'Batch quotes / brackets: wrap each line in single quotes or parentheses, quickly build ',
    ' IN 列表或数组。': ' IN list or array.',
    "生成 SQL/代码列表：把名字列表加「'」与逗号，直接贴进查询。": 'Generate SQL / code lists: add "\'" and commas to a name list, paste straight into a query.',
    '标注与包装：给每项加统一前缀（如「TODO:」）或后缀（如「.com」）。': 'Label and wrap: add a uniform prefix (e.g. "TODO:") or suffix (e.g. ".com") to each item.',
    '拼 SQL IN 列表': 'Build a SQL IN list',
    "粘贴「a/b/c」每行一个，加前缀「'」后缀「',」得「'a',『b',『c',」，最后一项去掉尾逗号即得 ('a','b','c')，省去手敲。": 'Paste "a/b/c" one per line, add prefix "\'" and suffix "\',", to get "\'a\',\'b\',\'c\',"; drop the trailing comma on the last item to get (\'a\',\'b\',\'c\'), saving manual typing.',
    '尾逗号怎么处理？': 'How to handle the trailing comma?',
    '可在选项去掉末行后缀，或用「末行不加」模式，避免 SQL 语法错误；也可生成后手动删最后一个逗号。': 'You can drop the last-line suffix via options, or use "skip last line" mode to avoid SQL syntax errors; or just delete the final comma after generation.',
    '内容含引号会冲突吗？': 'Do embedded quotes conflict?',
    '会。若原文本已有单引号，再包单引号会破坏字符串；此时改用双引号或转义，或选无冲突的分隔。': 'Yes. If the original text already has single quotes, wrapping again breaks the string; switch to double quotes or escape, or pick a non-conflicting delimiter.',
    '如何使用批量添加前缀后缀': 'How to use Prefix & Suffix Adder',
}, display='批量添加前缀后缀')


# ===== batch5 补充键（示例/长描述/标签/placeholder/deep-dive 小标题）=====
apply_tool('text-extract-numbers', '提取数字', 'Number Extractor', {
    '输入文本': 'Input text',
    '在线提取数字工具，从混合文本中快速抽取所有整数或小数，可保留正负号与小数位，按行或整体输出，适合报表与日志数据清洗，纯前端。': 'Online number extractor: quickly pull all integers or decimals from mixed text, keeping signs and decimal places, output by line or whole; ideal for report and log data cleaning; fully client-side.',
    '价格 99.99 元，库存 -25 件，速度 3.14e2 m/s。\n2024年增长 15.5%，比 2023 年的 12% 高。\n颜色 #FF0000，端口 8080，IP 192.168.1.1。': 'Price 99.99, stock -25, speed 3.14e2 m/s.\n2024 growth 15.5%, up from 12% in 2023.\nColor #FF0000, port 8080, IP 192.168.1.1.',
    '输入包含数字的文本...': 'Paste text containing numbers...',
}, auto=False)

apply_tool('text-extract-urls', '提取 URL', 'URL Extractor', {
    '访问 https://www.example.com 了解更多。\nAPI 文档见 https://api.toolbox.dev/v1/docs?key=abc123\n或访问 http://localhost:3000/path?x=1#anchor\n也可以是 ftp://files.example.org': 'Visit https://www.example.com for details.\nAPI docs at https://api.toolbox.dev/v1/docs?key=abc123\nOr http://localhost:3000/path?x=1#anchor\nAlso ftp://files.example.org',
    '输入包含 URL 的文本...': 'Paste text containing URLs...',
}, auto=False)

apply_tool('text-extract', '文本提取', 'Smart Text Extractor', {
    '联系我：邮箱 abc@example.com 或 test123@domain.org\n电话：13800138000，010-12345678\n网址：https://www.example.com/path?id=1\nIP：192.168.1.1，127.0.0.1\n金额：$199.99，￥888\n日期：2024-01-15，2024/02/20': 'Contact: email abc@example.com or test123@domain.org\nPhone: 13800138000, 010-12345678\nURL: https://www.example.com/path?id=1\nIP: 192.168.1.1, 127.0.0.1\nAmount: $199.99, RMB 888\nDate: 2024-01-15, 2024/02/20',
    '粘贴要提取的文本...': 'Paste the text to extract...',
    '📚 深度解析：文本提取（正则）': '📚 In-Depth: Smart Text Extractor (regex)',
}, auto=False)

apply_tool('text-filter-lines', '按行过滤', 'Line Filter', {
    '每行一条...': 'One per line...',
    '输入关键词或正则': 'Enter keyword or regex',
    '📚 深度解析：按条件过滤行': '📚 In-Depth: Filtering Lines by Condition',
}, auto=False)

apply_tool('text-indent', '自动缩进', 'Auto Indent Tool', {
    '📚 深度解析：文本缩进': '📚 In-Depth: Text Indentation',
}, auto=False)

apply_tool('text-keep-only', '仅保留指定字符', 'Keep-Only Character Filter', {
    '只留含『支付』的行': 'Keep only lines containing "payment"',
    '如：abc123': 'e.g. abc123',
    '如：[a-z]+': 'e.g. [a-z]+',
    '📚 深度解析：仅保留匹配项': '📚 In-Depth: Keep-Only Matches',
}, auto=False)

apply_tool('text-line-numbers', '添加行号', 'Line Number Adder', {
    '第一行': 'First line', '第二行': 'Second line', '第三行': 'Third line', '第四行': 'Fourth line',
    '第一行\n第二行\n第三行\n第四行': 'First line\nSecond line\nThird line\nFourth line',
    '📚 深度解析：加行号': '📚 In-Depth: Adding Line Numbers',
}, auto=False)

apply_tool('text-merge', '多段文本合并', 'Multi-Text Merger', {
    '第一段内容': 'First paragraph', '第二段内容': 'Second paragraph', '第三段内容': 'Third paragraph', '第四段内容': 'Fourth paragraph',
    '第一段内容\n第二段内容\n第三段内容\n第四段内容': 'First paragraph\nSecond paragraph\nThird paragraph\nFourth paragraph',
    '将多段分散文本按行或自定义分隔符合并为一段，可去空行与去重，适用于整理笔记、拼接日志与批量文本重组，本地处理不泄露内容。': 'Merge scattered text blocks into one by line or custom separator, dropping blank lines and duplicates; for tidying notes, stitching logs and batch text restructuring; processed locally, nothing leaves your browser.',
    '第一段\n第二段\n第三段': 'First\nSecond\nThird',
    '例如：--> 或 ===': 'e.g. --> or ===',
    '如：「 或 (': 'e.g. " or (',
    '如：」 或 )': 'e.g. " or )',
    '📚 深度解析：文本合并': '📚 In-Depth: Merging Text Blocks',
}, auto=False)

apply_tool('text-pad', '文本填充', 'Text Padding Tool', {
    '📚 深度解析：文本填充对齐': '📚 In-Depth: Text Padding & Alignment',
}, auto=False)

apply_tool('text-prefix-suffix', '批量添加前缀后缀', 'Prefix & Suffix Adder', {
    '后缀': 'Suffix',
    '批量加引号/括号：给每行内容包上单引号或圆括号，快速拼 SQL IN 列表或数组。': 'Batch quotes / brackets: wrap each line in single quotes or parentheses, quickly build SQL IN list or array.',
    '为每行文本批量添加固定的前缀或后缀（如编号、符号），支持正则与分隔符，适合清单批量处理与格式整理。': 'Batch-add a fixed prefix or suffix (such as numbering or symbols) to every line, with regex and separator support; ideal for bulk list processing and formatting.',
    "生成 SQL/代码列表：把名字列表加『'』与逗号，直接贴进查询。": 'Generate SQL / code lists: add "\'" and commas to a name list, paste straight into a query.',
    '每行一条...': 'One per line...',
    '可留空，例如 - 或 [': 'Optional, e.g. - or [',
    '可留空，例如 ; 或 ]': 'Optional, e.g. ; or ]',
    '📚 深度解析：加前后缀': '📚 In-Depth: Adding Prefix & Suffix',
}, auto=False)
