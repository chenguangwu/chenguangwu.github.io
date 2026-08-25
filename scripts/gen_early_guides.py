# -*- coding: utf-8 -*-
"""Q9 早期手写指南英文 i18n 注入器（同页切换，仿 N8 机制）。

不重写早期 html 的 TPL，而是直接给现有节点注入 data-i18n / data-i18n-head 属性，
并把高质量英文写入合并字典 js/guide-en-pack.js（由 export_js 合并，避免覆盖 N3/N6/N8）。
仅处理标准 5 段结构（核心功能/适用场景/使用步骤/实用技巧/常见问题）；
其他结构（h2 标题非标准）本批跳过，留待后续批次。
运行：python3 scripts/gen_early_guides.py
"""
import os, re, json, html, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GUIDES_DIR = os.path.join(ROOT, 'guides')
SITE = 'https://chenguangwu.github.io'

def esc(s):
    return html.escape(str(s))

# 第一批：6 篇标准 5 段结构。键格式与 N8 一致：
# guide.<slug>.title / .desc / .intro / .features.<i> / .scenarios.<i> / .steps.<i> / .tips.<i> / .faqs.<i>.q/.a
EARLY_PACK = {}
def add(slug, title, desc, intro, features, scenarios, steps, tips, faqs):
    EARLY_PACK['guide.%s.title' % slug] = title
    EARLY_PACK['guide.%s.desc' % slug] = desc
    EARLY_PACK['guide.%s.intro' % slug] = intro
    for i, v in enumerate(features):
        EARLY_PACK['guide.%s.features.%d' % (slug, i)] = v
    for i, v in enumerate(scenarios):
        EARLY_PACK['guide.%s.scenarios.%d' % (slug, i)] = v
    for i, v in enumerate(steps):
        EARLY_PACK['guide.%s.steps.%d' % (slug, i)] = v
    for i, v in enumerate(tips):
        EARLY_PACK['guide.%s.tips.%d' % (slug, i)] = v
    for i, (q, a) in enumerate(faqs):
        EARLY_PACK['guide.%s.faqs.%d.q' % (slug, i)] = q
        EARLY_PACK['guide.%s.faqs.%d.a' % (slug, i)] = a

add('age-calculator',
    'Age Calculator Guide',
    'Age Calculator guide: compute exact age in years, total days lived, and days to your next birthday from a birth date.',
    'Want to know exactly how many days you have lived, or how long until an anniversary? ToolBox Age Calculator works locally from your birth date to give your exact age, total days, and a countdown to the next birthday.',
    ['Get exact age in years from a birth date', 'Show total days, months and more', 'Count down days to the next birthday', 'Support the difference between any two dates', 'Instant, fully local'],
    ['Confirm age in years when filling forms', 'Count days since a baby was born', 'Plan anniversaries, premiums and contract terms', 'Age-milestone reminders for health management'],
    ['Pick the birth date', 'Click calculate for age in years and total days', 'See the countdown to the next birthday', 'Use date-difference mode for two dates', 'Copy the result'],
    ['Age in years follows the "not yet birthday -> minus one" rule, unlike nominal age', 'For contracts/insurance, follow the stated terms', 'Cross-timezone dates use the local calendar day'],
    [('What is the difference between age in years and nominal age?', 'Age in years counts from your birthday; nominal age counts you as one at birth, usually 1-2 years more.'),
     ('Is the age calculation accurate?', 'It is computed precisely from the Gregorian date, so the result is reliable.')])

add('base64',
    'Base64 Encode/Decode Guide',
    'Base64 guide: convert text and Base64 both ways, including file to Base64 data URI.',
    'Base64 encodes binary or text data into printable characters, used to embed data in text protocols (JSON, CSS, email). ToolBox Base64 converts locally, supporting both strings and files.',
    ['Text <-> Base64 two-way', 'File to Base64: images/files to data URI', 'URL-safe mode: replace + / = with - _ and drop padding', 'One-click copy', 'Chunked handling for large files to avoid lag'],
    ['Inline a small icon as Base64 in CSS to cut requests', 'Transfer binary over text-only interfaces', 'Embed attachments in email body', 'Debug APIs with Base64 fields'],
    ['Choose Encode or Decode', 'Encode: paste text or pick a file; Decode: paste a Base64 string', 'Check URL-safe if you need URL compatibility', 'Click convert for live results', 'Copy or download'],
    ['Base64 grows data by ~33%, not for long-term large-file storage', 'Inline Base64 suits small icons; use a separate file + cache for big images', 'Decode only standard Base64; switch URL-safe back to standard first'],
    [('Is Base64 encryption?', 'No. It is only encoding and anyone can decode it - never use it to "hide" sensitive data.'),
     ('What if the data URI is too long?', 'The source file is large; use a separate file reference instead of inlining.')])

add('bcrypt',
    'Bcrypt Hash / Verify Guide',
    'Bcrypt guide: generate and verify password hashes with an adjustable cost factor, computed locally for safe storage.',
    'Bcrypt is the go-to password hashing algorithm: it bakes in a salt so the same password yields different hashes each time. This tool generates hashes and verifies plaintext, with an adjustable cost factor (rounds), all in your browser.',
    ['Standard Bcrypt hash ($2a$10$..., 60 chars)', 'Built-in salt; same plaintext -> different hash each time', 'Cost factor 8-14 to balance security and speed', 'One-click verify plaintext + hash', 'Auto-extract salt from the hash, no manual management'],
    ['Debug user password hashes in backend dev', 'Learn/demo how Bcrypt works', 'Verify a password hash from your database'],
    ['Enter the plaintext password', 'Pick a cost factor (10 recommended)', 'Click Generate Hash for a 60-char hash', 'Paste the hash into verify, enter plaintext, click Verify'],
    ['Each +2 in cost factor ~= 4x slower; 10 is ~150ms', 'Bcrypt is hashing, not encryption - it cannot be reversed, only verified', 'Store the cost factor in config so you can upgrade later'],
    [('Why are two hashes different?', 'Bcrypt salts randomly each time and writes the salt into the hash prefix, so results differ but all verify.'),
     ('Is a leaked hash safe?', 'With a strong password it is relatively safe, but add a pepper or MFA.')])

add('bmi-calculator',
    'BMI Calculator Guide',
    'BMI Calculator guide: from height and weight, compute BMI and classify the healthy weight range.',
    'BMI (Body Mass Index) is the most common gauge of whether weight is healthy. ToolBox BMI Calculator gives the BMI value and band (underweight/normal/overweight/obese) locally from height and weight.',
    ['Enter height (cm) and weight (kg) for BMI', 'Auto-label the healthy band', 'Show the standard-weight reference range', 'For adults, instant', 'Fully local, no network'],
    ['Daily health check, watch weight trend', 'Compare BMI before/after fitness', 'Help interpret a check-up report', 'A starting point for weight-loss/gain goals'],
    ['Enter height (cm)', 'Enter weight (kg)', 'Click calculate for the BMI value', 'Compare against bands: underweight/normal/overweight/obese', 'Assess with waistline and other metrics'],
    ['BMI ignores muscle vs fat; fit people (more muscle) may read high but be healthy', 'Pregnant, minors and elderly need professional assessment', 'A normal BMI still benefits from exercise and a balanced diet', 'Watch the long-term trend, not a single reading'],
    [('Is a normal BMI always healthy?', 'Not necessarily; it misses fat distribution and muscle, so pair it with waistline etc.'),
     ('Why do fit people read high BMI?', 'Muscle is denser than fat; BMI counts muscle as "heavy", a misread.')])

add('body-fat-calculator',
    'Body Fat Calculator Guide',
    'Body Fat Calculator guide: estimate body fat from circumference / height-weight, assessing body composition.',
    'Body fat tells more about fitness than weight alone. ToolBox Body Fat Calculator estimates body fat locally with common formulas (e.g. the U.S. Navy method) from height, weight and waist, with a healthy-range reference.',
    ['Estimate body fat from height, weight, waist etc.', 'Different formulas by sex', 'Show the healthy body-fat range', 'Include interpretation notes', 'Fully local'],
    ['Track composition during fat-loss training', 'Self-read check-up data', 'Set training/diet goals', 'A finer health check than BMI'],
    ['Pick sex', 'Enter height, weight, waist (some formulas need neck/hip)', 'Click calculate for estimated body fat', 'Compare against the healthy range', 'Improve with exercise and diet'],
    ['Formulas estimate with individual error; watch trends not absolutes', 'Measure circumference at fixed sites/methods to compare', 'Too low or too high both unhealthy; aim for the sensible range'],
    [('Which is more accurate, body fat or BMI?', 'Body fat reflects composition; BMI only uses weight vs height.'),
     ('Why different formulas for men and women?', 'Fat distribution differs by sex, so sex-specific formulas are more accurate.')])

add('case-converter',
    'Case Converter Guide',
    'Case Converter guide: switch naming styles - camelCase, snake_case, kebab-case, UPPER and more.',
    'Naming styles vary (camelCase, snake_case, kebab-case...). ToolBox Case Converter switches them locally in one click, handy for both programmers and writers.',
    ['camelCase / PascalCase / snake_case / kebab-case / UPPER/lower', 'Convert a whole block of text', 'Keep word boundaries, smart tokenizing', 'One-click copy', 'Handle spaces and punctuation edges'],
    ['Unify variable naming when refactoring', 'Turn copy into Title Case', 'Generate a URL slug (kebab)', 'Align DB fields with code variable names'],
    ['Paste or type the text', 'Pick the target style (e.g. snake_case)', 'Get the result live', 'Check tokenizing (especially abbreviations)', 'Copy and use'],
    ['Consecutive-capital abbreviations (e.g. "HTTP") are often split wrong in camelCase - review after', 'Mixed Chinese uses spaces/punctuation as token edges', 'kebab-case suits URLs, snake_case suits databases'],
    [('What is the difference between camel and Pascal?', 'camelCase starts lowercase, PascalCase starts uppercase, per language convention.'),
     ('Why did tokenizing go wrong?', 'The tool splits on spaces/punctuation/case changes; odd abbreviations may misread.')])

# 第二批：6 篇标准 5 段结构。
add('chmod-calculator',
    'Chmod Calculator Guide',
    'Chmod Calculator guide: tick read/write/execute to convert between numeric and symbolic permission modes in real time.',
    'Visualize Linux file permissions: tick read(4)/write(2)/execute(1) for owner/group/others and get the numeric mode (e.g. 755) and symbolic mode (rwxr-xr-x) instantly, with a quick reference for common modes.',
    ['Three groups (owner/group/others) x three permission checkboxes', 'Live numeric and symbolic mode conversion', 'Meaning hints for common modes (755/644/777 etc.)', 'One-click fill for 6 common permission sets', 'One-click copy of the chmod command'],
    ['Set directory/file permissions when deploying a website', 'Troubleshoot "permission denied" errors', 'Learn the Linux permission model'],
    ['Tick read/write/execute for each user group', 'Read the numeric and symbolic mode shown above', 'Check the meaning hint to judge whether it is safe', 'Click "Copy chmod command" to use it'],
    ['Directories commonly use 755, regular files 644', '777 is fully open and risky; use with caution', 'Private keys and config files should be 600 or 400'],
    [('What does 755 mean?', 'Owner gets read/write/execute (7); group and others get read/execute (5). Commonly used for web directories.'),
     ('Why do I still get an error after changing permissions?', 'Files and directories need separate settings; a directory needs x to be entered, r alone is not enough.')])

add('color-converter',
    'Color Converter Guide',
    'Color Converter guide: convert HEX/RGB/HSL/CMYK both ways for design and development.',
    'Different scenarios use different color models: web uses HEX/RGB, print uses CMYK. ToolBox Color Converter converts between formats locally, saving manual math.',
    ['HEX/RGB/HSL/CMYK multi-way conversion', 'Enter any format and the rest auto-fill', 'Live color-swatch preview', 'One-click copy of the target format', 'RGBA with alpha supported'],
    ['Web color to print CMYK check', 'Convert design-spec colors to code', 'Unify team color formats in batch', 'Recover a color from a screenshot'],
    ['Fill any input box with a color value (e.g. #3366CC)', 'The other formats sync automatically', 'Click to copy the format you need', 'Use RGBA mode for transparency', 'Check the preview swatch'],
    ['CMYK is subtractive; converting back to RGB may show slight shift — trust the print proof', 'HSL is more intuitive than RGB for lightness/darkness tweaks', 'Fix one format for brand colors to avoid ambiguity'],
    [('Why is there a shift from CMYK to RGB?', 'The two color spaces differ; conversion is an approximate mapping.'),
     ('How is transparency expressed?', 'Use the A channel of RGBA (0-1) or 8-digit HEX (#RRGGBBAA).')])

add('color-picker',
    'Color Picker Guide',
    'Color Picker guide: pick, tune, and convert HEX/RGB/HSL — essential for design and palettes.',
    'Whether writing CSS or making design drafts, accurate color values matter. ToolBox Color Picker picks and fine-tunes locally and converts HEX/RGB/HSL live.',
    ['Visual palette; drag to pick instantly', 'HEX/RGB/HSL live conversion', 'Suggests readable text color (black/white)', 'Copy any format', 'Reverse-locate from a typed value'],
    ['Front-end dev writing CSS color values', 'Derive close colors from a brand color', 'Check foreground/background readability', 'Suck a color from an image into a code-ready value'],
    ['Drag on the palette to choose a target color', 'Read the synced HEX/RGB/HSL', 'Copy the format you need into code', 'Type a known value to reverse-locate on the panel', 'Use the contrast hint to confirm text readability'],
    ['The same color differs across screens; trust the code value for key brand colors', 'Accessibility: body-to-background contrast >= 4.5:1', 'HSL suits lightness/saturation tweaks', 'Name the palette consistently when saving'],
    [('Which is better, HEX or RGB?', 'Equivalent; HEX is compact, RGB is intuitive — choose as needed.'),
     ('How to ensure text is readable?', 'Use the tool\'s contrast-color hint to keep enough foreground/background contrast.')])

add('compound-interest',
    'Compound Interest Calculator Guide',
    'Compound Interest Calculator guide: project the future value and total interest of principal growing at compound rate.',
    'Compound interest is called the "eighth wonder of the world." ToolBox Compound Interest Calculator projects the future value of a principal with periodic interest and regular contributions, showing the power of time and rate.',
    ['Future value of a single principal at compound rate', 'Monthly/annual contribution (annuity) supported', 'Adjustable annual rate and compounding frequency', 'Breakdown of principal, interest and total', 'Chart of the growth curve'],
    ['Plan savings and financial goals', 'Compare returns across rates/terms', 'Long-term education/pension projection', 'Understand the "start early" effect'],
    ['Enter the initial principal', 'Fill the annual return rate and years', 'Choose whether to contribute and the amount/frequency', 'Click calculate to see future value and interest', 'Watch the curve for the acceleration point'],
    ['Time is the biggest variable in compounding; earlier start, bigger gain', 'Mind "annualized" vs "actual received"; taxes erode returns', 'High return often means high risk; the calculator excludes volatility'],
    [('How does compound differ from simple interest?', 'Simple interest charges only on principal; compound charges on "principal + accrued interest", a huge gap long term.'),
     ('Is a lump sum or contribution better?', 'Contributions spread timing risk, good for monthly surplus; lump sum suits existing capital.')])

add('countdown-timer',
    'Countdown Timer Guide',
    'Countdown Timer guide: set a target time and show live remaining days/hours/minutes/seconds.',
    'Big days deserve anticipation. ToolBox Countdown Timer sets any target time locally and shows live remaining days, hours, minutes and seconds.',
    ['Set a target date and time', 'Live refresh of remaining time', 'Supports events, holidays, deadlines', 'Clean UI, no login', 'Fully local'],
    ['Gaokao, postgrad, exam countdowns', 'Product launch, event opening countdowns', 'Project deadline reminder', 'Personal goals (e.g. quitting, challenge)'],
    ['Pick or enter the target date and time', 'Click start; the page shows remaining time', 'Minimize to do other things; it still counts when back', 'Watch the seconds near the end', 'Screenshot to share the goal'],
    ['Counts in local timezone; align cross-timezone events', 'Set multiple reminders before key deadlines, not just the page', 'Closing the page stops timing; use a calendar for long-term reminders'],
    [('Does the countdown survive closing the page?', 'Local timing lives with the page; closing stops it. Use a system calendar for long-term.'),
     ('What if the time is wrong?', 'It follows the device system clock; calibrate the system clock.')])

add('crontab-generator',
    'Crontab Generator Guide',
    'Crontab Generator guide: build five-field expressions visually, with Chinese notes and common presets.',
    'Visually build Linux crontab expressions: pick minute/hour/day/month/week, get the five-field cron syntax with Chinese notes, plus 6 common presets.',
    ['Five fields (min/hour/day/month/week) visual input', 'Live cron expression and Chinese notes', 'Support *, */n, a-b, a,b syntax', '6 common presets one-click fill', 'Syntax check with instant field error hints', 'One-click copy of the expression'],
    ['Server scheduled-task config', 'Backups, reports and other periodic tasks', 'Learn cron expression syntax'],
    ['Fill the five fields (or use presets)', 'Read the generated expression and Chinese notes', 'Click "Copy expression" to paste into crontab', '(Optional) tweak fields for finer scheduling'],
    ['cron Sunday is 0 or 7', 'minute field cannot be empty; */5 means every 5 minutes', 'multiple values with comma: 1,15,30; range with hyphen: 9-17'],
    [('What are the parts of a cron expression?', 'In order: minute, hour, day, month, week — five fields, e.g. "0 9 * * 1" means every Monday at 9:00.'),
     ('Why did my task not run?', 'Common causes: illegal minute value, timezone mismatch, or wrong server time.')])

# 第三批：7 篇标准 5 段结构。
add('date-diff',
    'Date Difference Calculator Guide',
    'Date Difference Calculator guide: count the days, months and workdays between two dates.',
    '"How many days until this project ends?" "How many weeks between paychecks?" ToolBox Date Difference Calculator works locally to give the exact days and weeks between two dates, with an option to exclude weekends.',
    ['Days/weeks between two dates', 'Optional workdays only (exclude weekends)', 'Supports cross-year, cross-month ranges', 'Shows start/end info', 'Instant result'],
    ['Project cycle, lease-day accounting', 'Pay/bill cycle stats', 'Schedule and milestones', 'Exact days of a contract term'],
    ['Pick the start and end dates', 'Click calculate for the day count', 'Tick "workdays only" if needed', 'See derived results like weeks', 'Copy the result into your schedule'],
    ['Whether to "include both ends" changes the day count — pick per business rule', 'Workday mode drops weekends by default, not public holidays', 'Cross-timezone dates use the local calendar day'],
    [('Does the count include the start day?', 'Usually the natural-day difference (end - start); whether endpoints count depends on the setting.'),
     ('Do public holidays count as workdays?', 'This tool\'s workday mode only drops weekends, not holiday adjustments.')])

add('hash-multi',
    'Multi-Algorithm Hash Guide',
    'Multi-Algorithm Hash guide: compute and compare MD5/SHA-1/SHA-256/SHA-512/CRC32 side by side.',
    'Compute several hashes at once: MD5, SHA-1, SHA-256, SHA-512 and CRC32, with multi-algorithm output and case toggle. The SHA family uses the browser native crypto.subtle, fully local.',
    ['5 algorithms side by side (MD5/SHA-1/256/512/CRC32)', 'Tick algorithms, output all at once', 'SHA family uses native crypto.subtle', 'Upper/lower case toggle', 'Copy each or all at once'],
    ['Download integrity check (SHA-256)', 'API signature debugging (MD5/SHA)', 'Dedup and consistency compare (CRC32)'],
    ['Enter the text', 'Tick the algorithms you need', 'Click "Calculate" to see all results', 'Click "Copy all" for batch use'],
    ['Prefer SHA-256 for file checks (SHA-1 and MD5 no longer advised for security)', 'CRC32 is for quick consistency, not security', 'CRC32 outputs as 8 hex digits'],
    [('MD5 vs SHA-256?', 'MD5 is 128-bit, SHA-256 is 256-bit; both common, but use SHA-256 or above for security.'),
     ('Can a hash be reversed?', 'No, hashing is one-way; this site only does forward hashing, no reverse lookup.')])

add('integer-base-converter',
    'Arbitrary Base Converter Guide',
    'Arbitrary Base Converter guide: convert between bases 2-36 with BigInt for huge integers and a base overview.',
    'Convert between any bases 2-36; built on BigInt so it handles integers far beyond Number precision limit. Enter a number and its source base to get the target-base result plus a common-base overview.',
    ['Convert between any bases 2-36', 'BigInt supports arbitrarily large integers', 'Auto-generates binary/octal/decimal/hex/32/36 overview', 'Detects and locates invalid characters in a base', 'One-click copy'],
    ['Base conversion for color values, MAC addresses', 'Data encoding and compression debugging', 'Large-number base conversion in crypto/hash'],
    ['Enter a number (e.g. ff, 1010, 255)', 'Set source and target bases (2-36)', 'See the result and multi-base overview live', 'Click "Copy result"'],
    ['Hex letters are case-insensitive (ff and FF both work)', 'Base must be between 2 and 36', 'Invalid characters for the source base trigger an error at the position'],
    [('How large a number can it convert?', 'BigInt-based, effectively unlimited digits; handles 100-digit decimals.'),
     ('Why is decimal shown as a string?', 'Numbers beyond Number precision lose accuracy, so the tool keeps them as faithful strings.')])

add('json-formatter',
    'JSON Formatter Guide',
    'JSON Formatter guide: minify/beautify JSON, validate syntax, fold and expand — a front-end debugging essential.',
    'JSON is the de-facto standard for front-back communication, but raw minified JSON is hard to read. ToolBox JSON Formatter beautifies indentation, validates syntax errors, and folds/expands nodes locally — a handy aid for debugging API responses.',
    ['One-click beautify: minified JSON shown with hierarchical indentation', 'Syntax validation: locate missing quotes, commas, brackets', 'Compact mode: re-minify beautified JSON to a single line', 'Tree folding: collapse/expand large objects level by level', 'Copy result: one-click after formatting'],
    ['Inspect back-end JSON structure when integrating APIs', 'Debug front-end errors: locate the exact JSON.parse failure', 'Tidy config files, log snippets', 'Compare structural differences of two JSONs'],
    ['Paste raw JSON into the left input', 'Click "Format" for an indented result on the right', 'If a syntax error shows, fix at the highlighted position and retry', 'Click the triangle at a line start to collapse child nodes', 'Click "Copy" to use the result in code or docs'],
    ['Confirm the content is really JSON, not XML or YAML, before formatting', 'For very long single-line JSON, format first — error positions are easier to find', 'Never paste key-containing JSON into untrusted online tools in production; local tools are safer'],
    [('Why "JSON syntax error"?', 'Common causes: trailing comma, unquoted keys, or single quotes; fix at the hinted position.'),
     ('Does formatting change the data?', 'No, only layout and indentation; the data stays the same.')])

add('json-minify',
    'JSON Minify / Format Guide',
    'JSON minify and format guide: one-click compress to shrink size, beautify to read, with compression ratio.',
    'The JSON tool supports "compress" and "beautify": compress shrinks storage/transfer size and shows the ratio; beautify aids reading and debugging. All in the browser, local.',
    ['Compress mode: strip whitespace/newlines, show ratio', 'Beautify mode: hierarchical indentation for reading', 'Show original/output size comparison', 'Parse-error location hint for debugging', 'One-click copy'],
    ['API debugging: beautify returned minified JSON', 'Storage optimization: compress config/cache data', 'Put compressed JSON into URL params'],
    ['Paste JSON into the input', 'Pick "Compress" or "Beautify" (live switch supported)', 'See size and ratio stats', 'Click "Copy result"'],
    ['Ratio can be negative (small JSON grows) — normal', 'Beautified JSON indents with 2 spaces', 'Confirm valid JSON before pasting, else an error position shows'],
    [('Compress or beautify?', 'Compress for transfer/storage, beautify for reading/debugging; neither changes the data.'),
     ('Why did it grow after compressing?', 'Small JSON has high whitespace ratio, so compression gain is small or negative — normal.')])

add('json-to-csv',
    'JSON to CSV Guide',
    'JSON to CSV guide: convert an array to a table in one click, auto-extract fields, handle nested objects, download file.',
    'Convert a JSON array to a CSV table in one click: auto-collect all object fields as headers, serialize nested objects to JSON strings, support copy and download — handy for data migration and Excel work.',
    ['Auto-extract all fields as CSV headers', 'Handle arrays and nested objects (serialized)', 'NULL/missing fields output as empty cells', 'UTF-8 BOM export so Excel reads Chinese correctly', 'One-click copy or download .csv'],
    ['Export API data as a table for ops/sales', 'Data migration: JSON to Excel/sheet', 'Format conversion before batch import'],
    ['Paste a JSON array (e.g. [{...},{...}])', 'Click "Convert" to auto-generate CSV', 'See row/column stats: N rows x M cols', 'Click "Download .csv" to save'],
    ['Input must be an array; an object triggers an error', 'Every CSV cell is double-quoted, so commas are safe', 'If Excel shows garbled Chinese, use "Download" (with BOM)'],
    [('How are nested objects handled?', 'Serialized to a JSON string in the cell, e.g. {"a":1} shows as {"a":1}.'),
     ('Why is Chinese garbled in Excel?', 'Use the "Download .csv" button (UTF-8 BOM); copy-paste may garble.')])

add('markdown-to-html',
    'Markdown to HTML Guide',
    'Markdown to HTML guide: render Markdown to HTML in real time for easy publishing.',
    'Markdown is the mainstream lightweight markup for writing and docs. ToolBox Markdown to HTML renders .md text to HTML snippets locally, ready to paste into web pages or rich editors.',
    ['Live render: write Markdown left, see HTML right', 'Supports headings, lists, tables, code blocks, quotes', 'Clean HTML snippets, ready to use', 'One-click copy', 'Export supported'],
    ['Turn notes/docs into web-publishable HTML', 'Write README, blog drafts', 'Paste structured content into a CMS', 'Quick layout for teaching/reports'],
    ['Paste or type Markdown on the left', 'See rendered HTML live on the right', 'For HTML source, switch to source view and copy', 'Check tables, code blocks etc. as expected', 'When pasting into a target editor, clean extra styles'],
    ['Advanced syntax like complex tables/footnotes varies by engine — review after render', 'Generated HTML may carry default tags; wrap it in site CSS', 'Avoid rendering untrusted content to prevent XSS (local tool, but mind downstream use)'],
    [('Can the result go live directly?', 'Yes, but apply site CSS for consistent styling.'),
     ('Why did some syntax not work?', 'It may be extended syntax outside standard Markdown; check engine support.')])

# 第四批 A：6 篇标准 5 段结构。
add('math-evaluator',
    'Math Expression Evaluator Guide',
    'Math Expression Evaluator guide: powers, percentages, trig functions and more, with live results.',
    'The Math Expression Evaluator lets you type an expression like a calculator and get the result. It supports + - * / % ^ and functions like sin/cos/sqrt/ln, and auto-saves the last 20 calculations for reuse.',
    ['+ - * / % ^ ( ) with operator precedence', 'Built-in sin/cos/tan/sqrt/abs/ln/log/floor/ceil/round/min/max', 'Percentage shortcut: 15% * 200 treats as 0.15 x 200', 'Whitelist character check, rejects script injection, safe', 'Auto-saves last 20 history, one-click reuse', 'Auto switches to scientific notation for out-of-range results'],
    ['Daily number crunching for students/engineers', 'Quick formula check before data analysis', 'Reuse past results by filling back in'],
    ['Type an expression, e.g. 2^10 + sqrt(144)', 'Click "Calculate" or press Enter', 'Result shows live, history auto-saved', 'Click "Reuse" in history to refill the input', 'Use the buttons to insert functions and pi'],
    ['^ means power (2^10 = 1024)', 'Percent is treated as "divide by 100": 15% = 0.15', 'sqrt and ln need parentheses: sqrt(144), ln(e)', 'pi via button or type pi directly'],
    [('Why "expression invalid"?', 'May have illegal chars (Chinese, @, #) or mismatched brackets; only digits, operators and whitelisted functions are accepted.'),
     ('Result shows scientific notation?', 'Very large/small numbers auto-use scientific notation, e.g. 1.5e+15.')])

add('md5',
    'MD5 Hash Guide',
    'MD5 Hash guide: generate MD5 digests for text/files locally for checksums and dedup.',
    'MD5 is a common hash that turns any data into a fixed-length digest, often used for integrity checks. ToolBox MD5 computes text or file MD5 locally — no network, no upload.',
    ['Text and files both supported', '32-hex-digit MD5 digest', 'Streaming for large files, no lag', 'One-click copy', 'Fully local, no upload'],
    ['Verify a download against the official MD5', 'Detect whether two files are identical', 'Dedup and quick fingerprint', 'Debug digests in API signatures'],
    ['Paste text or pick a file', 'Click calculate for the MD5', 'Compare with the official/provided digest', 'A match means the content is unchanged', 'Copy the result for records'],
    ['MD5 is broken; never use it for password storage or tamper-proofing', 'It fits "integrity check", not "security"', 'For large files, trust the official hash'],
    [('Can MD5 store passwords?', 'No. MD5 is insecure; use a slow hash like bcrypt for passwords.'),
     ('Why does the file MD5 not match?', 'Any byte difference changes the digest; confirm the same source before comparing.')])

add('mortgage-calculator',
    'Mortgage Calculator Guide',
    'Mortgage Calculator guide: equal-installment vs equal-principal monthly payment, total interest and schedule.',
    'Buying a home is one of the biggest household expenses. ToolBox Mortgage Calculator estimates monthly payment, total interest and total cost locally, comparing equal-installment and equal-principal repayment.',
    ['Equal-installment and equal-principal algorithms', 'Enter loan amount, annual rate, term for the monthly payment', 'Outputs total interest and total repayment', 'Compare total-cost difference of the two methods', 'Local, no network'],
    ['Estimate if monthly payment fits the household budget', 'Compare which method saves more interest', 'Estimate the benefit of early repayment', 'Try monthly payment at different down payments'],
    ['Enter the loan principal (e.g. 1,000,000)', 'Fill the annual rate (e.g. 3.95%) and term (e.g. 30 years)', 'Pick the repayment method', 'Click calculate for monthly payment, total interest, total', 'Switch method to compare total cost'],
    ['Equal-principal has higher early payments but less total interest — good if you can pay more early', 'Use the "annual" rate, not the monthly rate', 'Real payments also include fees/taxes; the calculator only does loan principal+interest', 'Watch how LPR changes affect floating rates'],
    [('Equal-installment or equal-principal?', 'Stable payment -> equal-installment; save interest and pay more early -> equal-principal.'),
     ('Does the result match the bank?', 'Same algorithm; differences come from rate value, rounding and extra fees.')])

add('password-generator',
    'Password Generator Guide',
    'Password Generator guide: strong random passwords with custom length and charset for account security.',
    'Weak passwords are the top cause of account theft. ToolBox Password Generator uses the browser native strong-random source locally — no network, no upload — with custom length and toggles for case/digits/symbols.',
    ['Adjustable length (12+ recommended)', 'Independent toggles: upper, lower, digits, symbols', 'Option to exclude ambiguous chars (0/O/1/l)', 'One-click copy, not stored', 'Based on the browser crypto secure random source'],
    ['Strong master password for a new account', 'Unique independent passwords per site', 'Random string for API keys, temp tokens', 'One-time access codes for a team'],
    ['Set length; important accounts >= 16', 'Tick the char types; all on is safest by default', '(Optional) enable "exclude ambiguous" to avoid copy errors', 'Click generate, preview the password', 'Click copy and save to a password manager at once'],
    ['Different password per site, plus a manager, is safest', 'Avoid birthdays, place names, consecutive digits', 'Save right after generating; do not paste in plaintext everywhere', '2FA beats merely lengthening the password'],
    [('Is the generated password safe?', 'Uses the browser native secure random source and is generated locally offline — high security.'),
     ('Why a password manager?', 'The brain cannot hold many strong passwords; a manager encrypts and auto-fills them.')])

add('percentage-calculator',
    'Percentage Calculator Guide',
    'Percentage Calculator guide: quick percent change, share, discount and ratio.',
    'Discounts, rises, shares... percentages are everywhere. ToolBox Percentage Calculator computes change, the share of one number of another, and the discounted price locally.',
    ['A as a percentage of B', 'Percent increase/decrease', 'Discount/markup price', 'Split by ratio', 'Instant result'],
    ['Shopping: discounted price and amount saved', 'YoY/MoM performance growth', 'Share analysis in reports', 'Quick tip/tax estimate'],
    ['Pick the type (share/change/discount)', 'Fill the values', 'Click calculate for the percentage or result', 'Check the base (what the denominator is)', 'Copy the result'],
    ['"Grew 50%" differs by base — confirm the reference', '20% off means times 0.8, not minus 20 yuan', 'YoY uses last year same period, MoM uses last period — do not mix'],
    [('How to compute 20% off?', 'Original x (1 - 0.2) = 0.8x, i.e. 20% off.'),
     ('Is share the same as growth rate?', 'No: share is part/whole, growth is change/original.')])

add('qr-beautify',
    'QR Code Beautifier Guide',
    'QR Code Beautifier guide: custom colors and rounded styles for branded QR codes, download PNG.',
    'Customize foreground, background, error correction and module rounding on top of a standard QR to make a branded color QR — good for cards, posters and print. PNG download supported.',
    ['Custom foreground/background color', 'Four error-correction levels (L/M/Q/H)', 'Rounded/square module styles', 'Live preview, what-you-see-is-what-you-get', 'Download PNG or copy Base64', 'Pure local canvas drawing, content not uploaded'],
    ['Brand posters and promo materials', 'Personalized QR on cards/badges', 'Event check-in, booth guidance'],
    ['Enter the QR content (URL/text/etc.)', 'Pick foreground, background and error-correction level', 'Pick module style (rounded is softer)', '"Download PNG" once previewed'],
    ['Dark foreground + light background gives the highest contrast and steadiest scan', 'More content lowers the level; complex content use M', 'Keep a quiet zone (white margin) around print, avoid edge bleed'],
    [('Color QR won\'t scan?', 'Usually low foreground/background contrast; use light bg, dark fg.'),
     ('How to pick error-correction?', 'Dirty-prone use Q/H; very long content drop to L/M for density.')])

# 第四批 B：6 篇标准 5 段结构（标准候选收官）。
add('qrcode',
    'QR Code Generator Guide',
    'QR Code Generator guide: one-click QR for text, URL, WiFi, vCard — downloadable image.',
    'QR codes have become a universal entry point for information flow. ToolBox QR Code Generator runs fully locally in the browser: enter text, URL, WiFi info or a contact card to generate a high-res QR in real time and download as PNG/SVG — no upload.',
    ['Many content types: text, URL, WiFi, email, phone, SMS, geo', 'Live preview, generates as you type, no button needed', 'Optional error correction (L/M/Q/H), balancing robustness vs density', 'PNG bitmap and SVG vector export', 'Custom foreground/background color and margin for branding'],
    ['Print a poster QR for an official account link or product page', 'Share WiFi via QR so guests connect by scan', 'Expo card: QR of contact info for easy exchange', 'Offline materials: menu, table tent, flyer jump entry'],
    ['Pick the content type (text/URL/WiFi/card...)', 'Fill the content; the QR previews live', 'Adjust error correction and size: busy/dirty scenes use H', 'Click "Download PNG" or "Download SVG"', '(Optional) change fg/bg color so print contrast is enough'],
    ['Higher correction resists dirt but denser; for outdoor, weigh L/H', 'Keep at least a 4-module quiet zone or it may fail to scan', 'Dark fg + light bg gives best contrast; avoid close colors', 'WiFi QR includes the password — share only in trusted settings'],
    [('Why does the QR not scan?', 'Check quiet-zone margin, low contrast, low correction; regenerate with higher correction.'),
     ('Is the QR uploaded?', 'No. All generation is local; content never leaves the browser.')])

add('regex-tester',
    'Regex Tester Guide',
    'Regex Tester guide: debug regex online with live match highlight, groups and replace.',
    'Regex is the Swiss-army knife of text processing, but its syntax is error-prone. ToolBox Regex Tester debugs expressions locally in real time, highlights all matches and capture groups, and previews replacement.',
    ['Live match highlight, updates as you type', 'Shows capture groups of each match', 'Supports common flags g/i/m/s', 'Replace mode: preview the result', 'Explains common errors to help debug'],
    ['Extract email, phone, URL from logs/text', 'Form input validation (ID, zip)', 'Batch rename, find and replace', 'Filter rows by rule when cleaning data'],
    ['Enter the pattern in the "Regex" box, e.g. \\d+', 'Paste the text to match in the "Test text" box', 'Turn on flags you need (g global, i ignore case)', 'Check highlights and groups, tune the pattern', 'Switch to replace mode to preview when needed'],
    ['Build the smallest match first, then add constraints — avoid one-shot errors', 'Note . does not match newline by default; use s for multiline', 'For Chinese, use a range or \\p{...} (engine-dependent)', 'Greedy vs lazy (*? +?) often decides match length'],
    [('Why only the first match?', 'Without the global g flag, only the first match returns by default.'),
     ('How to match Chinese?', 'Use a range like [一-鿿] or a specific Unicode property, per engine support.')])

add('timestamp-converter',
    'Timestamp Converter Guide',
    'Timestamp Converter guide: Unix timestamp <-> date, seconds/ms and multiple timezones.',
    'Unix timestamps (seconds/ms since 1970-01-01) are widely used in logs and APIs. ToolBox Timestamp Converter switches locally between "timestamp <-> readable date" and recognizes milliseconds.',
    ['Timestamp to date: auto-detect seconds or ms', 'Date to timestamp: both seconds and ms', 'Shows current timestamp, one-click refresh', 'Local timezone display', 'Batch or one-by-one'],
    ['Debug logs: turn an API timestamp back into a real time', 'Debug code: confirm timezone and unit (s/ms) match', 'Check database time fields', 'Align time across systems'],
    ['View the current timestamp as reference', 'Paste a timestamp in "to date"; it auto-detects s/ms and shows the date', 'In "to timestamp", pick a date-time to get the s/ms value', 'Watch the timezone of the result', 'Copy the value for code or docs'],
    ['Common trap: using ms as s is 1000x off; the tool detects it but double-check', 'Agree on the unit front/back to avoid s front, ms back', 'Show in user local timezone, store in UTC'],
    [('Seconds vs ms?', '13 digits is usually ms, 10 is seconds; the tool tries to auto-detect.'),
     ('Why different times on different machines?', 'Different timezone settings; the underlying timestamp is the same.')])

add('token-generator',
    'Random Token Generator Guide',
    'Random Token Generator guide: crypto-grade random tokens, custom length/charset/batch.',
    'Generates strong tokens from the browser crypto-grade crypto.getRandomValues, with custom length, charset and count, showing entropy — for API tokens, invite codes, keys.',
    ['crypto.getRandomValues crypto-grade source', 'Custom length (4-256) and charset (case/digits/symbols)', 'Batch up to 20', 'Shows entropy (bits) to quantify strength', 'Copy each or all at once'],
    ['Generate API token / key', 'Generate invite, activation, coupon codes', 'Generate random credentials for testing'],
    ['Set length (default 32) and count (default 1)', 'Tick charset: case, digits, symbols', 'Click "Generate", view entropy', 'Click "Copy" to use'],
    ['Symbols raise entropy a lot; tick them for sensitive use', 'Save results securely at once; this tool stores no tokens', 'Tokens vanish after the browser closes; regenerate to reuse'],
    [('Is the token uploaded?', 'No, randomness is generated locally; nothing is sent to any server.'),
     ('What is entropy?', 'A measure of randomness strength; more bits means harder to brute-force; 128+ bits is a strong token.')])

add('unit-converter',
    'Unit Converter Guide',
    'Unit Converter guide: length, weight, volume, temperature and more in one click.',
    'Unit conversion comes up often in daily life and engineering. ToolBox Unit Converter covers length, area, weight, volume, temperature, speed locally, converting as you type.',
    ['Many categories: length/area/volume/weight/temperature/speed/time', 'Live conversion, updates on unit switch', 'Full common-unit coverage (m, ft, kg, lb, C/F...)', 'Clear conversion factor display', 'Adjustable decimal precision'],
    ['Overseas shopping: inches/lb to cm/kg', 'Cooking: cups to ml per recipe', 'Renovation area, volume estimate', 'Travel temperature (C/F) quick lookup'],
    ['Pick the category (e.g. length)', 'Enter a value and pick the source unit', 'Pick the target unit; result appears live', 'For multi对比, convert in batches and compare factors', 'Copy the result'],
    ['Temperature is not a linear ratio (C to F adds 32); the formula is built in', 'Cross-border shopping: "ounce" has avoirdupois/troy; weight uses avoirdupois', 'Watch unit magnitude on big numbers; don\'t miss k/m prefixes'],
    [('Why not multiply for temperature?', 'Celsius and Fahrenheit have different zeros, so there is a +32 offset the formula handles.'),
     ('Is the result inaccurate?', 'Uses standard factors; only display precision affects it, no real error.')])

add('url-encode',
    'URL Encode Guide',
    'URL Encode guide: URL encode/decode for Chinese, spaces and special chars.',
    'URLs allow only some safe characters; Chinese, spaces and & need encoding. ToolBox URL Encode encodes/decodes a URL or params locally to avoid request errors.',
    ['URL encode and decode, both ways', 'Handles Chinese, spaces, special chars', 'Keeps common safe chars unchanged', 'Whole string or param fragment', 'One-click copy'],
    ['Put a Chinese keyword into a query param', 'Build a download link with special chars', 'Debug 400/garbled API issues', 'Pre-process form GET params'],
    ['Pick encode or decode', 'Paste the text', 'Click convert for the result', 'Check the encoded result parses correctly', 'Copy for the link or request'],
    ['Space is often %20 or + in URLs; pick per context', 'Encode only the param value, not the whole protocol/domain', 'Before decoding, confirm it is standard encoding to avoid double-encoding'],
    [('Why does Chinese become %E4%BD%A0?', 'That is the percent-encoding of UTF-8 bytes; browsers/servers restore it automatically.'),
     ('Encoded link won\'t open?', 'You may have encoded parts that should stay (like :// or /); encode only the param value.')])

FIELD_MAP = {'核心功能': 'features', '适用场景': 'scenarios', '使用步骤': 'steps', '实用技巧': 'tips', '常见问题': 'faqs'}

# 非标准指南：每篇的 h2 顺序与类型（'p'=段落小节, 'faq'=常见问题）。与 add_ns 的 items 顺序一致。
NS_MAP = {}

def add_ns(slug, title, desc, intro, items, faqs):
    """items: 按文档顺序的段落小节列表，每项为 ('p', en_heading, [en_paragraphs]) 或 ('faq', en_heading, None)。
    faqs: [(q,a), ...]。键：guide.<slug>.sec<i>(标题) / .p<i>.<j>(段落) / .faqs.<k>.q/.a。"""
    EARLY_PACK['guide.%s.title' % slug] = title
    EARLY_PACK['guide.%s.desc' % slug] = desc
    EARLY_PACK['guide.%s.intro' % slug] = intro
    for i, (kind, en_h, paras) in enumerate(items):
        EARLY_PACK['guide.%s.sec%d' % (slug, i)] = en_h
        if kind == 'p':
            for j, p in enumerate(paras):
                EARLY_PACK['guide.%s.p%d.%d' % (slug, i, j)] = p
    for k, (q, a) in enumerate(faqs):
        EARLY_PACK['guide.%s.faqs.%d.q' % (slug, k)] = q
        EARLY_PACK['guide.%s.faqs.%d.a' % (slug, k)] = a


# ===== 非标准指南（段落结构）=====
# 第五批 A：base32 / blood-pressure / blood-sugar
NS_MAP.update({
    'base32-encode': [('为什么有这么多 Base 家族', 'p'), ('Base32 的典型场景', 'p'), ('在 ToolBox 中选择', 'p'), ('常见问题', 'faq')],
    'blood-pressure-classifier': [('两个数字的含义', 'p'), ('常用分级（参考）', 'p'), ('在 ToolBox 中分类', 'p'), ('测量注意', 'p'), ('常见问题', 'faq')],
    'blood-sugar-converter': [('两种单位', 'p'), ('参考区间因单位而异', 'p'), ('在 ToolBox 中换算', 'p'), ('常见问题', 'faq')],
})
add_ns('base32-encode',
    'Base32 / Base58 / Base85 Encoding Comparison',
    'The Base family goes beyond Base64; compare Base32/58/85 trade-offs and use cases, with ToolBox conversion examples.',
    'The Base family goes beyond Base64. This guide compares Base32/58/85 trade-offs and use cases, with ToolBox conversion examples.',
    [('p', 'Why so many Base families', ['They all represent binary with a "safe character set", but the alphabet differs: Base64 is the most compact and common; Base32 uses only uppercase letters and digits 2-7, avoiding confusing characters, good for hand copying; Base58 drops 0/O/l/I, used in Bitcoin addresses; Base85 is even more compact, used in PostScript/PDF.']),
     ('p', 'Typical use cases for Base32', ['OTP secrets (e.g. Google Authenticator secret), activation codes and other cases needing "accurate human copying" — Base32 drops confusing characters to cut error rates.']),
     ('p', 'Choose in ToolBox', ['The Base32/58/64/85 tools all support encode and decode; paste the content and pick the algorithm. Mind the padding and alphabet differences — decode with the same algorithm.']),
     ('faq', 'FAQ', None)],
    [('Is Base32 much longer than Base64?', 'Yes. Base32 carries only 5 bits per char vs Base64 6 bits, so it is larger but more readable.'),
     ('Why does Base58 drop some letters?', 'It removes visually similar chars like 0, O, I, l to avoid copy/handwriting errors in addresses, common in crypto.'),
     ('Can Base64 decode a Base32 result?', 'No. The alphabet and rules differ; you must convert with the matching algorithm.')])

add_ns('blood-pressure-classifier',
    'Blood Pressure Classification and Home Reading',
    'How to read systolic/diastolic, common classification bands, how to classify with ToolBox and what to watch.',
    'How to read systolic/diastolic, the common classification bands, how to classify with ToolBox, and what to watch for.',
    [('p', 'What the two numbers mean', ['Blood pressure is written "systolic/diastolic" (e.g. 120/80 mmHg). Systolic is the pressure when the heart contracts; diastolic is when it relaxes.']),
     ('p', 'Common classification (reference)', ['Normal <120/80; elevated 120-139/80-89; hypertension stage 1 >=140/90; stage 2 is higher. Follow your doctor precise.']),
     ('p', 'Classify in ToolBox', ['Enter the two values to see the band and range hint; the result is for reference only, not a diagnosis.']),
     ('p', 'Measurement notes', ['A single reading is affected by mood, exercise and cuff position; sit still 5 minutes, measure several times and average, and log at a fixed time.']),
     ('faq', 'FAQ', None)],
    [('Is home reading different from the hospital normal?', 'White-coat hypertension, nerves and posture all affect it; home averages over several readings are closer to daily levels.'),
     ('Are electronic monitors accurate?', 'Compliant monitors are fine for daily use, but need periodic calibration and correct cuff fitting.'),
     ('Can the result replace a doctor diagnosis?', 'No. This tool only gives a band reference; see a doctor for anything abnormal.')])

add_ns('blood-sugar-converter',
    'Blood Sugar Unit Converter (mg/dL to mmol/L)',
    'The difference between the two blood sugar units, the conversion factor, how to convert with ToolBox and why reference ranges differ.',
    'The difference between the two blood sugar units, the conversion factor, how to convert with ToolBox, and why reference ranges differ.',
    [('p', 'The two units', ['China commonly uses mmol/L; some countries use mg/dL. They differ by about 18.0182x: mmol/L = mg/dL / 18.0182.']),
     ('p', 'Reference ranges differ by unit', ['Fasting normal is about 3.9-6.1 mmol/L, or about 70-110 mg/dL; always unify the unit before comparing.']),
     ('p', 'Convert in ToolBox', ['Enter the value and source unit for the target-unit result in one click, avoiding manual-division mistakes.']),
     ('faq', 'FAQ', None)],
    [('Which unit is more accurate?', 'They are just different representations; the number needs its unit to mean anything — neither is "more accurate".'),
     ('Are fasting and post-meal standards the same?', 'No. The 2-hour post-meal upper bound is usually higher; follow the specific test requirements.'),
     ('Can conversion replace a glucometer?', 'No. This tool only converts units; the value still comes from your measuring device.')])

# 第五批 B：calorie / currency-symbol / gif-split
NS_MAP.update({
    'calorie-calculator': [('BMR 是基础', 'p'), ('活动系数得 TDEE', 'p'), ('在 ToolBox 中估算', 'p'), ('常见问题', 'faq')],
    'currency-symbol': [('符号与代码', 'p'), ('地区差异', 'p'), ('在 ToolBox 中查询', 'p'), ('常见问题', 'faq')],
    'gif-split': [('GIF 是「帧的合集」', 'p'), ('常见用途', 'p'), ('在 ToolBox 中拆分', 'p'), ('常见问题', 'faq')],
})
add_ns('calorie-calculator',
    'Daily Calorie Needs (TDEE) Estimator',
    'The link between BMR, activity factor and TDEE, and how to estimate the maintain/cut/bulk calorie range.',
    'The link between BMR, activity factor and TDEE, and how to estimate the maintain/cut/bulk calorie range.',
    [('p', 'BMR is the base', ['Basal Metabolic Rate (BMR) is the calories your body needs at rest to stay alive. The common Mifflin-St Jeor formula computes it from sex, age, height and weight.']),
     ('p', 'Activity factor gives TDEE', ['BMR x activity factor (sedentary ~1.2, high intensity ~1.7+) gives Total Daily Energy Expenditure (TDEE) — the calories to "break even".']),
     ('p', 'Estimate in ToolBox', ['Fill the basics and activity level; the result gives maintenance calories and marks the cut/bulk range around +/-15%.']),
     ('faq', 'FAQ', None)],
    [('Must cutting be below TDEE?', 'Usually a deficit of about 300-500 kcal is safer; too aggressive loses muscle and is hard to keep up.'),
     ('Why does it differ a lot from my App?', 'Formulas and activity-factor assumptions differ; treat it as a start and tune by your weight trend.'),
     ('Is TDEE a fixed value?', 'It changes with weight, muscle and age; recalc periodically.')])

add_ns('currency-symbol',
    'Currency Symbols and Codes Lookup',
    'Common currency symbols, ISO 4217 codes and regional differences, and how to look up currency info in ToolBox.',
    'Common currency symbols, ISO 4217 codes and regional differences, and how to look up currency info in ToolBox.',
    [('p', 'Symbols and codes', ['¥ (CNY), $ (USD), € (EUR), £ (GBP) are common symbols; ISO 4217 uses a unique 3-letter code per currency to avoid symbol ambiguity (e.g. $ is shared by many countries).']),
     ('p', 'Regional differences', ['The same symbol means different things by region (e.g. ¥ is also used for JPY); for cross-market talk prefer codes CNY/JPY.']),
     ('p', 'Look up in ToolBox', ['Enter a symbol or code to see the currency name and code, handy for reconciliation and copy.']),
     ('faq', 'FAQ', None)],
    [('Does ¥ mean CNY or JPY?', 'Both use ¥; in formal settings use CNY/JPY to tell them apart safely.'),
     ('What is ISO 4217 for?', 'It gives each currency a unique 3-letter code, the standard for cross-border payment and systems.'),
     ('Can a symbol convert amounts?', 'A symbol only marks the currency; conversion needs a rate. This tool identifies, not calculates rates.')])

add_ns('gif-split',
    'GIF Frame Split and Extract',
    'Why a GIF is a multi-frame animation, and how to extract single or all frames with ToolBox for stickers and analysis.',
    'Why a GIF is a multi-frame animation, and how to extract single or all frames with ToolBox for stickers and analysis.',
    [('p', 'A GIF is a set of frames', ['An animated GIF is essentially multiple still frames played in a loop by delay time, so each frame can be extracted and used alone.']),
     ('p', 'Common uses', ['Grab one sticker frame, analyze animation timing, turn key frames into static assets, etc.']),
     ('p', 'Split in ToolBox', ['After uploading a GIF, preview each frame and download single or all frames; note that many frames mean a large exported file.']),
     ('faq', 'FAQ', None)],
    [('Do extracted frames lose quality?', 'GIF itself has a limited palette (max 256 colors); extracted frames match the corresponding frames in the animation.'),
     ('Can I change frame delay?', 'Split mainly extracts; for delay tuning/reassembly use a dedicated GIF editor or script.'),
     ('Will large files lag?', 'GIFs with many frames parse slowly and produce a lot; confirm the frame range you need first.')])

# 第五批 C：html-entity-encoder / http-response-headers / image-to-ascii
NS_MAP.update({
    'html-entity-encoder': [('为什么需要实体编码', 'p'), ('实体 vs 字符引用', 'p'), ('在 ToolBox 中使用', 'p'), ('XSS 防护的边界', 'p'), ('常见问题', 'faq')],
    'http-response-headers': [('常用响应头', 'p'), ('用响应头排查问题', 'p'), ('在 ToolBox 中查看', 'p'), ('常见问题', 'faq')],
    'image-to-ascii': [('原理：亮度映射', 'p'), ('关键参数', 'p'), ('在 ToolBox 中转换', 'p'), ('常见问题', 'faq')],
})
add_ns('html-entity-encoder',
    'HTML Entity Encoding and XSS Escaping',
    'Why escape < > & as entities, and how to encode/decode and do basic XSS defense with ToolBox.',
    'Why escape < > & as entities, and how to encode/decode and do basic XSS defense with ToolBox.',
    [('p', 'Why entity encoding is needed', ['Outputting < directly in HTML is executed by the browser as a tag/script, causing XSS. Turning < into &lt;, > into &gt;, & into &amp; makes special chars "display only, not execute".']),
     ('p', 'Entities vs character references', ['&lt; is a named entity, &#60; is a decimal reference, &#x3C; is hex; all three are equivalent, and named entities are more readable.']),
     ('p', 'Use in ToolBox', ['Paste text and click encode to get the escaped result, ready to drop into a template/rich-text after escaping; decode turns entities back to the original chars.']),
     ('p', 'The limits of XSS defense', ['Entity encoding is only one output-layer measure; it does not replace parameterized queries, CSP, input validation and other combined defenses. Handle URL, attribute and JS contexts separately.']),
     ('faq', 'FAQ', None)],
    [('Escape quotes inside attribute values too?', 'Yes. A " in a double-quoted attribute should become &quot;, and a single-quoted one &apos;, to avoid closing the attribute early.'),
     ('Does escaping still display normally?', 'Yes. The browser restores the entity to the char when rendering; only the source is escaped.'),
     ('Is HTML escaping alone enough for XSS?', 'Enough for HTML body; but if content goes into a URL, on* event or JS string, use the matching context encoding — one trick is not universal.')])

add_ns('http-response-headers',
    'HTTP Response Headers Explained',
    'What Content-Type, Cache-Control, CORS, Set-Cookie and others do, with typical debugging ideas.',
    'What Content-Type, Cache-Control, CORS, Set-Cookie and others do, with typical debugging ideas.',
    [('p', 'Common response headers', ['Content-Type declares the content type; Cache-Control controls caching; Set-Cookie issues the session; Access-Control-Allow-Origin decides whether cross-origin is allowed.']),
     ('p', 'Debug with response headers', ['Styles/scripts not applying often means wrong Content-Type; no refresh means check Cache-Control; CORS errors mean check the CORS header; lost login means check Set-Cookie Domain/Path/SameSite.']),
     ('p', 'View in ToolBox', ['Paste the response-header text to format and explain each item, quickly locating config errors.']),
     ('faq', 'FAQ', None)],
    [('no-store vs no-cache?', 'no-store forbids any cached copy; no-cache allows caching but requires validation with the origin before use.'),
     ('Whose fault is a CORS error?', 'The server response header decides whether cross-origin is allowed; the front end cannot bypass it alone — the other side must set Access-Control-Allow-*.'),
     ('What does SameSite=Strict affect?', 'It limits cookies in third-party contexts; cross-site redirects may not carry the session, so pick Lax/None per business.')])

add_ns('image-to-ascii',
    'Image to ASCII Art',
    'How a picture becomes character art, the brightness-mapping principle, parameter tuning and limits, with ToolBox tips.',
    'How a picture becomes character art, the brightness-mapping principle, parameter tuning and limits, with ToolBox tips.',
    [('p', 'Principle: brightness mapping', ['The tool first grayscales the image, then maps each pixel brightness to a charset (e.g. @%#*+=-:. ); bright areas use sparse chars, dark areas dense ones, yielding ASCII art.']),
     ('p', 'Key parameters', ['Width sets the horizontal char count; the charset affects texture; invert suits dark backgrounds. Too wide makes output long, too narrow loses detail.']),
     ('p', 'Convert in ToolBox', ['After uploading, tune width and charset for live preview; copy the result into a terminal, README or chat.']),
     ('faq', 'FAQ', None)],
    [('Why do complex photos look bad?', 'ASCII art is low-resolution; complex light/dark detail is lost. Clear outlines and strong contrast work best.'),
     ('Can it export to a file?', 'Copy the text and save as .txt; for color, save in a tool that supports ANSI.'),
     ('Can ASCII art be a Logo?', 'It fits minimal/geek style; for a real brand, still use vector SVG.')])

# 第五批 D：ip-calculator / json-path / json-schema-validator
NS_MAP.update({
    'ip-calculator': [('IPv4 与子网基础', 'p'), ('关键产出', 'p'), ('在 ToolBox 中计算', 'p'), ('常见问题', 'faq')],
    'json-path': [('JSONPath 是什么', 'p'), ('核心语法速查', 'p'), ('在 ToolBox 中提取', 'p'), ('常见问题', 'faq')],
    'json-schema-validator': [('什么是 JSON Schema', 'p'), ('写一个最小 Schema', 'p'), ('在 ToolBox 中校验', 'p'), ('常见校验错误', 'p'), ('常见问题', 'faq')],
})
add_ns('ip-calculator',
    'IP and Subnet Calculator (CIDR)',
    'IPv4 structure, subnet mask and CIDR, and how to compute network/broadcast/usable hosts.',
    'IPv4 structure, subnet mask and CIDR, and how to compute network/broadcast/usable hosts.',
    [('p', 'IPv4 and subnet basics', ['IPv4 is a 32-bit address, usually written as 4 decimal groups. The subnet mask/CIDR (e.g. /24) decides how many bits are network vs host.']),
     ('p', 'Key outputs', ['Network address = IP AND mask (bitwise); broadcast = host bits all 1; usable hosts = 2^hostBits - 2 (minus network and broadcast).']),
     ('p', 'Calculate in ToolBox', ['Enter 192.168.1.10/24 to see the network address, broadcast address, usable host range and count.']),
     ('faq', 'FAQ', None)],
    [('Why 254 usable for /24?', 'Host bits are 8 = 256; minus the network and broadcast addresses leaves 254.'),
     ('CIDR vs subnet mask?', '/24 means mask 255.255.255.0; the prefix length is the count of 1s in the mask.'),
     ('Does IPv6 work the same?', 'IPv6 has a huge space and different division; this tool focuses on IPv4/CIDR.')])

add_ns('json-path',
    'JSONPath Field Extraction',
    'Extract fields from nested JSON with JSONPath expressions, with $ .. [*] filter syntax examples.',
    'Extract fields from nested JSON with JSONPath expressions, with $ .. [*] filter syntax examples.',
    [('p', 'What is JSONPath', ['Like XPath for XML, JSONPath uses short expressions to locate data in JSON. $ is the root, .key gets a property, [*] loops an array, .. searches recursively.']),
     ('p', 'Core syntax at a glance', ['$.store.book[0] is the first element; $.store.book[*].title lists all titles; $..price finds every price recursively; $.store.book[?(@.price<10)] filters cheap books.']),
     ('p', 'Extract in ToolBox', ['Paste JSON on the left and a path in the box; matches show on the right instantly. A wrong expression returns no match, helping you debug complex API responses.']),
     ('faq', 'FAQ', None)],
    [('JSONPath vs JavaScript access?', 'JSONPath is a declarative string expression, easy to configure and reuse; obj.a.b is code. The two convert to each other.'),
     ('What operators does ?() support?', 'Commonly ==, !=, <, > and existence checks like @.key exists; for complex logic, extract first then handle in code.'),
     ('Why does my expression return empty?', 'Usually wrong case or path level; first use $..fieldName to confirm the field exists.')])

add_ns('json-schema-validator',
    'JSON Schema Validation Primer',
    'What JSON Schema is, how to validate API JSON with it, with a copyable draft-07 example.',
    'What JSON Schema is, how to validate API JSON with it, with a copyable draft-07 example.',
    [('p', 'What is JSON Schema', ['JSON Schema is a JSON document describing how JSON "should look"; the common version is draft-07. It uses keywords like type, required, properties, enum to declare field types and constraints, often to validate API requests/responses and config files.']),
     ('p', 'Write a minimal Schema', ['This schema requires an object with name (string) and age (non-negative integer), and role limited to user/admin:']),
     ('p', 'Validate in ToolBox', ['Open the JSON Schema validator, paste data on the left and schema on the right, click validate for per-field results. Changing the sample to "age": -3 immediately reports a "minimum" error.']),
     ('p', 'Common validation errors', ['type mismatch: wrong field type; required: missing mandatory field; enum: value not in the allowed set; additionalProperties: a field not declared in the schema (set false for strict checks).']),
     ('faq', 'FAQ', None)],
    [('Can JSON Schema validate arrays?', 'Yes. Use "type":"array" with "items" describing each element, plus "minItems"/"maxItems" for length.'),
     ('draft-07 vs 2020-12?', 'Mostly compatible; 2020-12 adds finer constraints like $defs and dependentRequired. draft-07 is enough for most business.'),
     ('Can the front end use JSON Schema?', 'Yes. Libraries like Ajv validate form and API data in the browser; ToolBox validator is good for quick debugging and copying results.')])

# 第五批 E（收官）：jwt-debugger / npv-calculator / roi-calculator / svg-placeholder-generator / unicode-lookup / yaml-validator
NS_MAP.update({
    'jwt-debugger': [('JWT 的三段结构', 'p'), ('重点看 Payload 的 claims', 'p'), ('签名验证的边界', 'p'), ('安全注意', 'p'), ('常见问题', 'faq')],
    'npv-calculator': [('什么是 NPV', 'p'), ('折现率的意义', 'p'), ('在 ToolBox 中计算', 'p'), ('常见问题', 'faq')],
    'roi-calculator': [('ROI 公式', 'p'), ('ROI 的局限', 'p'), ('在 ToolBox 中计算', 'p'), ('常见问题', 'faq')],
    'svg-placeholder-generator': [('为什么用 SVG 占位', 'p'), ('常用参数', 'p'), ('在 ToolBox 中生成', 'p'), ('常见问题', 'faq')],
    'unicode-lookup': [('什么是码点', 'p'), ('常见用途', 'p'), ('在 ToolBox 中查询', 'p'), ('常见问题', 'faq')],
    'yaml-validator': [('YAML 与 JSON 的关系', 'p'), ('最常见的错误：缩进', 'p'), ('在 ToolBox 中校验/转换', 'p'), ('常见问题', 'faq')],
})
add_ns('jwt-debugger',
    'JWT Debugger: Decode Header / Payload / Signature',
    'How the three JWT parts decode, how to read claims, and the premise and safety notes of signature verification (do not paste production keys).',
    'How the three JWT parts decode, how to read claims, and the premise and safety notes of signature verification (do not paste production keys).',
    [('p', 'The three parts of JWT', ['A JWT (JSON Web Token) looks like header.payload.signature; the first two are Base64URL-encoded JSON, the third is the signature. Split by . to decode and inspect each.']),
     ('p', 'Focus on Payload claims', ['sub subject, iss issuer, exp expiry (Unix seconds), iat issued-at. After exp the token should be rejected.']),
     ('p', 'The limits of signature verification', ['Decoding alone does not verify the signature; to verify you must hold the matching key/public key, and do it server-side. Front-end debugging only decodes for readability.']),
     ('p', 'Safety notes', ['Do not put passwords and other secrets in a JWT (it is encoded, not encrypted), and never paste production keys into untrusted pages.']),
     ('faq', 'FAQ', None)],
    [('Is Base64URL the same as Base64?', 'Similar but it swaps + / for - _ and drops padding =, better for URLs.'),
     ('Decoded exp but page says expired?', 'exp is Unix seconds; compare with current time. Use a timestamp tool to check.'),
     ('Can I verify the signature in the browser?', 'Yes with the key, but exposing the key in the front end is risky; do production verification server-side.')])

add_ns('npv-calculator',
    'NPV Calculator and Investment Decisions',
    'What NPV and the discount rate are, how to discount a series of cash flows for investment calls, with ToolBox usage.',
    'What NPV and the discount rate are, how to discount a series of cash flows for investment calls, with ToolBox usage.',
    [('p', 'What is NPV', ['Net Present Value discounts each future cash flow to today by the rate, then sums and subtracts the initial outlay. NPV>0 usually means the project is viable.']),
     ('p', 'The meaning of the discount rate', ['The discount rate reflects capital cost and risk; higher means more "discount" on future gains. The same cash flow has lower NPV at a higher rate.']),
     ('p', 'Calculate in ToolBox', ['Enter each period cash flow (first often negative as the outlay) and the rate; the result gives NPV and each period present value, easy to compare options.']),
     ('faq', 'FAQ', None)],
    [('NPV or IRR, which is clearer?', 'NPV gives an absolute amount, IRR an equivalent return rate; use both together for steadier decisions.'),
     ('What discount rate to use?', 'Capital cost, target return or industry benchmark; no single value — state your assumption.'),
     ('NPV<0 means never do it?', 'Financially usually not worth it, but strategic/compliance intangibles need separate weighing.')])

add_ns('roi-calculator',
    'ROI Calculator',
    'ROI formula, its limits, and how to compute return on investment with ToolBox.',
    'ROI formula, its limits, and how to compute return on investment with ToolBox.',
    [('p', 'ROI formula', ['ROI = (gain - cost) / cost x 100%. Simple and intuitive, it measures "how much per yuan invested".']),
     ('p', 'The limits of ROI', ['ROI ignores time; 50% in one year and 50% in ten years have the same ROI but worlds apart. So pair it with NPV/IRR.']),
     ('p', 'Calculate in ToolBox', ['Fill total gain and total cost for the ROI percentage; for multi-period projects, also discount the time value.']),
     ('faq', 'FAQ', None)],
    [('Negative ROI means what?', 'Gain below cost, i.e. a loss; the larger the absolute value, the worse the loss.'),
     ('Is ROI the same as net margin?', 'No. Net margin is accounting (with tax etc.); ROI is input-output ratio, more flexible in definition.'),
     ('Why skip a high ROI?', 'If payback is too long or risk is high, time value and risk weaken the appeal of a high ROI.')])

add_ns('svg-placeholder-generator',
    'SVG Placeholder Generator',
    'Why use SVG placeholders, common parameters, and how to generate with ToolBox.',
    'Why use SVG placeholders, common parameters, and how to generate with ToolBox.',
    [('p', 'Why SVG placeholders', ['SVG is vector, tiny, scales without blur, and can inline into HTML/email with no external image request — great for prototypes and skeleton screens.']),
     ('p', 'Common parameters', ['Width, height, background color, text color, and the size text shown. After generating, copy the SVG source or Data URI straight into <img> or CSS.']),
     ('p', 'Generate in ToolBox', ['Fill size and colors and click generate; preview updates live. Copy the SVG/Data URI and paste into your project.']),
     ('faq', 'FAQ', None)],
    [('Does a Data URI slow the page?', 'Small inline images save a request; for large images use a separate file to avoid a bloated HTML.'),
     ('Can SVG placeholders work in email?', 'Some email clients have limited SVG support; if needed, use a PNG placeholder or add fallback alt text.'),
     ('Can placeholders have rounded corners/gradient?', 'Yes. SVG supports rect rx rounding and linear gradients; for complex styles edit the source after generating.')])

add_ns('unicode-lookup',
    'Unicode Lookup',
    'What a code point is, how to look up characters in ToolBox, and common uses.',
    'What a code point is, how to look up characters in ToolBox, and common uses.',
    [('p', 'What is a code point', ['Unicode assigns each character a number called a code point, e.g. U+0041 is the letter A. One emoji may combine several code points (e.g. skin-tone variants).']),
     ('p', 'Common uses', ['When chasing "garbled / question marks", viewing the real code point tells whether it is an encoding mismatch or the char simply does not exist; special symbols (e.g. (C) (check) (heart)) are also referenced by code point.']),
     ('p', 'Look up in ToolBox', ['Enter a character or code point (e.g. U+1F600) for two-way lookup, with UTF-8/UTF-16 bytes shown to debug transfer and storage.']),
     ('faq', 'FAQ', None)],
    [('Why does an emoji show as two boxes?', 'The system font may lack that code point, or the font has no glyph for the emoji; the point exists but has no glyph, showing as tofu.'),
     ('U+ vs &#x?', 'U+1F600 is a writing convention; &#x1F600; is the HTML numeric entity form; both point to the same code point.'),
     ('Is Chinese also Unicode?', 'Yes. Chinese commonly lives in the CJK Unified Ideographs block from U+4E00, and also uses code-point lookup.')])

add_ns('yaml-validator',
    'YAML Validator and Converter',
    'The relation between YAML and JSON, how to validate/convert in ToolBox, and the most common error: indentation.',
    'The relation between YAML and JSON, how to validate/convert in ToolBox, and the most common error: indentation.',
    [('p', 'YAML and JSON', ['YAML is a superset of JSON, using indentation for hierarchy and more readable, common in config files (CI, K8s). It still converts to JSON, so "validate as JSON first" is a common debug path.']),
     ('p', 'The most common error: indentation', ['YAML is extremely sensitive to space indentation; mixing Tab and spaces errors out. Use 2 spaces uniformly and align the same level.']),
     ('p', 'Validate/convert in ToolBox', ['Paste YAML and click validate; errors pinpoint the line. One-click to JSON lets you continue with JSON tooling.']),
     ('faq', 'FAQ', None)],
    [('What are & anchor and * alias?', 'They are YAML reuse: &anchor defines, *alias references, cutting repetition; converting to JSON expands them to real values.'),
     ('Are booleans true/false mis-converted?', 'Yes. YAML treats yes/no/on/off as booleans too; in sensitive cases quote them as "yes" to avoid ambiguity.'),
     ('Are Tabs really unusable?', 'Standard YAML forbids Tab indentation; many parsers error outright. Always use spaces.')])

def inject_list(inner, slug, fld):
    counter = [0]
    def repl(mm):
        i = counter[0]; counter[0] += 1
        return '%s data-i18n="guide.%s.%s.%d" data-i18n-fb="%s">%s%s' % (
            mm.group(1), slug, fld, i, esc(mm.group(2)), mm.group(2), mm.group(3))
    return re.sub(r'(<li[^>]*)>(.*?)(</li>)', repl, inner, flags=re.S)

def inject_faqs(inner, slug):
    cd = [0]
    def rdt(mm):
        i = cd[0]
        return '%s data-i18n="guide.%s.faqs.%d.q" data-i18n-fb="%s">%s%s' % (
            mm.group(1), slug, i, esc(mm.group(2)), mm.group(2), mm.group(3))
    def rdd(mm):
        i = cd[0]; cd[0] += 1
        return '%s data-i18n="guide.%s.faqs.%d.a" data-i18n-fb="%s">%s%s' % (
            mm.group(1), slug, i, esc(mm.group(2)), mm.group(2), mm.group(3))
    inner = re.sub(r'(<dt[^>]*)>(.*?)(</dt>)', rdt, inner, flags=re.S)
    inner = re.sub(r'(<dd[^>]*)>(.*?)(</dd>)', rdd, inner, flags=re.S)
    return inner

def inject_ns(html, slug):
    # TOC：<a href="#sN">标题</a> 按 #s 序号复用 sec 键
    def toc_repl(m):
        i = m.group(2)
        txt = m.group(3)
        fb = re.sub(r'<[^>]+>', '', txt)
        return '%s data-i18n="guide.%s.sec%s" data-i18n-fb="%s">%s%s' % (m.group(1), slug, i, esc(fb), txt, m.group(4))
    html = re.sub(r'(<a href="#s(\d+)")>(.*?)(</a>)', toc_repl, html, flags=re.S)
    # h2 段落/FAQ 小节
    def repl(m):
        h2open, h2raw, inner = m.group(1), m.group(2), m.group(3)
        h2text = re.sub(r'<[^>]+>', '', h2raw).strip()
        idx = None
        for i, (cn, kind) in enumerate(NS_MAP.get(slug, [])):
            if cn == h2text:
                idx = i; break
        if idx is None:
            return m.group(0)
        kind = NS_MAP[slug][idx][1]
        new_h2 = '<h2%s data-i18n="guide.%s.sec%d" data-i18n-fb="%s">%s</h2>' % (h2open, slug, idx, esc(h2text), h2raw)
        if kind == 'faq':
            inner = inject_faqs(inner, slug)
        else:
            counter = [0]
            def p_repl(pm):
                j = counter[0]; counter[0] += 1
                return '%s data-i18n="guide.%s.p%d.%d" data-i18n-fb="%s">%s%s' % (pm.group(1), slug, idx, j, esc(re.sub(r'<[^>]+>', '', pm.group(2))), pm.group(2), pm.group(3))
            inner = re.sub(r'(<p[^>]*)>(.*?)(</p>)', p_repl, inner, flags=re.S)
        return new_h2 + inner
    html = re.sub(r'<h2([^>]*)>(.*?)</h2>(.*?)(?=<h2|</main)', repl, html, flags=re.S)
    return html

def inject(html, slug):
    # <title>
    html = re.sub(r'<title>(.*?)</title>',
                  lambda m: '<title data-i18n-head="guide.%s.title" data-i18n-head-fb="%s">%s</title>' % (slug, esc(m.group(1)), m.group(1)),
                  html, count=1)
    # meta description
    html = re.sub(r'(<meta name="description")( content="(.*?)")',
                  lambda m: '%s data-i18n-head="guide.%s.desc" data-i18n-head-fb="%s" data-attr="content"%s' % (m.group(1), slug, esc(m.group(3)), m.group(2)),
                  html, count=1)
    # ld+json inLanguage
    html = html.replace('"@type":"Article"', '"@type":"Article","inLanguage":"zh-CN"')
    # 3 scripts + hreflang（插在 </head> 前）
    canonical = '%s/guides/%s-guide.html' % (SITE, slug)
    scripts = ('<link rel="alternate" hreflang="zh-CN" href="%s">\n'
               '<link rel="alternate" hreflang="en-US" href="%s">\n'
               '<link rel="alternate" hreflang="x-default" href="%s">\n'
               '<script defer src="https://chenguangwu.github.io/js/i18n.js"></script>\n'
               '<script defer src="https://chenguangwu.github.io/js/guide-en-pack.js"></script>\n'
               '<script defer src="https://chenguangwu.github.io/js/guide-i18n.js"></script>\n') % (canonical, canonical, canonical)
    html = html.replace('</head>', scripts + '</head>', 1)
    # h1
    html = re.sub(r'(<h1[^>]*)>(.*?)(</h1>)',
                  lambda m: '%s data-i18n="guide.%s.title" data-i18n-fb="%s">%s%s' % (m.group(1), slug, esc(m.group(2)), m.group(2), m.group(3)),
                  html, count=1)
    # lead
    html = re.sub(r'(<p class="lead"[^>]*)>(.*?)(</p>)',
                  lambda m: '%s data-i18n="guide.%s.intro" data-i18n-fb="%s">%s%s' % (m.group(1), slug, esc(m.group(2)), m.group(2), m.group(3)),
                  html, count=1)
    # h2 blocks
    if slug in NS_MAP:
        html = inject_ns(html, slug)
    else:
        def repl_h2(m):
            h2open, h2text, inner = m.group(1), re.sub(r'<[^>]+>', '', m.group(2)), m.group(3)
            fld = FIELD_MAP.get(h2text.strip())
            if fld is None:
                return m.group(0)
            new_h2 = '<h2%s data-i18n="guide._section.%s" data-i18n-fb="%s">%s</h2>' % (h2open, fld, esc(h2text), h2text)
            if fld == 'faqs':
                inner = inject_faqs(inner, slug)
            else:
                inner = inject_list(inner, slug, fld)
            return new_h2 + inner
        html = re.sub(r'<h2([^>]*)>(.*?)</h2>(.*?)(?=<h2|</main)', repl_h2, html, flags=re.S)
    return html

def export_js(pack):
    path = os.path.join(ROOT, 'js', 'guide-en-pack.js')
    merged = {}
    if os.path.exists(path):
        try:
            txt = open(path, encoding='utf-8').read()
            m = txt.find('window.GUIDE_EN_PACK')
            if m >= 0:
                js_part = txt[txt.index('=', m) + 1:].strip()
                if js_part.endswith(';'):
                    js_part = js_part[:-1]
                existing = json.loads(js_part)
                if isinstance(existing, dict):
                    merged.update(existing)
        except Exception:
            pass
    merged.update(pack)
    header = "/* Auto-generated by scripts/gen_*_guides.py — merged EN dictionary for guide pages. Do not edit by hand. */\n"
    open(path, 'w', encoding='utf-8').write(header + 'window.GUIDE_EN_PACK = ' + json.dumps(merged, ensure_ascii=False, indent=2) + ';\n')
    print('js/guide-en-pack.js 字典导出 %d 条(本批 %d)' % (len(merged), len(pack)))

def main():
    slugs = sorted({k.split('.')[1] for k in EARLY_PACK if k.startswith('guide.') and k.endswith('.title')})
    # 实际 slug 来自 EARLY_PACK 键：guide.<slug>.title
    slugs = sorted(set(k.split('.')[1] for k in EARLY_PACK if k.startswith('guide.') and k.count('.') >= 2 and k.split('.')[2] == 'title'))
    for slug in slugs:
        fn = '%s-guide.html' % slug
        p = os.path.join(GUIDES_DIR, fn)
        if not os.path.exists(p):
            print('跳过(文件不存在):', fn); continue
        t = open(p, encoding='utf-8').read()
        if 'data-i18n' in t:
            print('跳过(已注入):', fn); continue
        out = inject(t, slug)
        open(p, 'w', encoding='utf-8').write(out)
        print('OK 注入:', fn)
    export_js(EARLY_PACK)

if __name__ == '__main__':
    main()
