# -*- coding: utf-8 -*-
"""N/Q1i 高价值指南扩容生成器（第二批）：为 Q1 新增的剩余 19 个核心工具补齐使用指南。
复用 scripts/gen_q1h_guides.py 的范式：写指南 HTML + 合并 json/guides.json + 更新 guides/index.html + 导出英文包。
模板用 .replace() 规避 CSS 大括号被 format 误解析。
运行：python3 scripts/gen_q1i_guides.py

本批覆盖 Q1 三批中第一批（gen_q1h，20 篇）未覆盖的剩余 19 个工具：
roman-numeral, mime-type-lookup, http-methods-reference, text-to-braille, text-to-1337,
binary-to-ascii, text-to-ascii-art, triangle-calculator, prime-checker, color-shade-generator,
wifi-qr-generator, gradient-generator, reading-time-estimator, gst-calculator, recipe-scaler,
fuel-cost-calculator, parking-fee, unit-price-compare, color-blindness-sim
"""
import os, json, html, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GUIDES_DIR = os.path.join(ROOT, 'guides')
SITE = 'https://chenguangwu.github.io'

GUIDES = [
 {
  'slug': 'roman-numeral',
  'ind': 'life',
  'base': 'roman-numeral.html',
  'name': '罗马数字转换器',
  'desc': '罗马数字转换器使用指南：在阿拉伯数字与罗马数字（I–MMMCMXCIX）之间互转，并解释转换规则。',
  'intro': '罗马数字用 I/V/X/L/C/D/M 表示 1/5/10/50/100/500/1000，靠左减右加规则组合。本工具双向转换并展示每一步，适合教学、钟表与文档编号场景。纯前端，数据不上传。',
  'features': ['阿拉伯→罗马互转', '逐位规则展示', '范围校验 1–3999', '大数提示', '本地处理'],
  'scenarios': ['文档/章节编号转换', '钟表与纪念碑年份', '教学罗马数字规则'],
  'steps': ['输入阿拉伯数或罗马串', '点击转换', '查看结果与规则'],
  'tips': ['范围上限 3999', '小数/负数不支持', '左小右大相减（IV=4）'],
  'faqs': [('超过 3999 怎么办？', '古罗马用上划线表示千倍，本工具仅覆盖标准 1–3999。'), ('能给个例子吗？', '1994 转为 MCMXCIV。')],
  'en_name': 'Roman Numeral Converter',
  'en_desc': 'Roman Numeral Converter Guide: convert between Arabic and Roman numerals (I–MMMCMXCIX) and explain the rules.',
  'en_intro': 'Roman numerals use I/V/X/L/C/D/M for 1/5/10/50/100/500/1000, combined by subtract-on-left, add-on-right. This tool converts both ways and shows each step, handy for teaching, clocks and outline numbering. Pure front-end, nothing uploaded.',
  'en_features': ['Arabic to Roman both ways', 'Step-by-step rule display', 'Range check 1–3999', 'Large-number note', 'Local processing'],
  'en_scenarios': ['Outline/chapter numbering', 'Clock and monument years', 'Teaching Roman rules'],
  'en_steps': ['Enter an Arabic number or Roman string', 'Click convert', 'See the result and rules'],
  'en_tips': ['Upper limit is 3999', 'No decimals or negatives', 'Small-before-large subtracts (IV=4)'],
  'en_faqs': [('Above 3999?', 'Romans used an overline for x1000; this tool covers standard 1–3999 only.'), ('Example?', '1994 becomes MCMXCIV.')],
 },
 {
  'slug': 'mime-type-lookup',
  'ind': 'it',
  'base': 'mime-type-lookup.html',
  'name': 'MIME 类型查询',
  'desc': 'MIME 类型查询使用指南：按文件扩展名或 MIME 类型互查，给出常见用途与浏览器处理方式。',
  'intro': 'Content-Type 决定浏览器如何解析响应（下载还是预览、图片还是文本）。本工具按扩展名/类型双向查询，列出典型用途。纯前端，无网络请求。',
  'features': ['扩展名→类型', '类型→扩展名', '用途说明', '常见别名提示', '本地处理'],
  'scenarios': ['后端设置 Content-Type', '排查下载而非预览', '确认文件该用什么后缀'],
  'steps': ['输入扩展名或 MIME', '点击查询', '查看类型与用途'],
  'tips': ['text/html 才会渲染', 'application/json 多为下载', 'charset 可追加在类型后'],
  'faqs': [('为什么浏览器下载而不是打开？', 'Content-Type 不匹配常见预览类型时会触发下载。'), ('能给个例子吗？', '.csv 通常是 text/csv，部分浏览器仍下载。')],
  'en_name': 'MIME Type Lookup',
  'en_desc': 'MIME Type Lookup Guide: look up by file extension or MIME type, with common usage and browser handling.',
  'en_intro': 'Content-Type decides how a browser parses a response (download vs preview, image vs text). This tool looks up both ways and lists typical usage. Pure front-end, no network.',
  'en_features': ['Extension to type', 'Type to extension', 'Usage note', 'Common alias hint', 'Local processing'],
  'en_scenarios': ['Set Content-Type on back-end', 'Debug download instead of preview', 'Confirm the right suffix'],
  'en_steps': ['Enter an extension or MIME', 'Click look up', 'See the type and usage'],
  'en_tips': ['text/html renders', 'application/json usually downloads', 'charset can follow the type'],
  'en_faqs': [('Why download instead of open?', 'A Content-Type that is not a known preview type triggers download.'), ('Example?', '.csv is usually text/csv, yet some browsers still download it.')],
 },
 {
  'slug': 'http-methods-reference',
  'ind': 'it',
  'base': 'http-methods-reference.html',
  'name': 'HTTP 方法速查',
  'desc': 'HTTP 方法速查使用指南：对照 GET/POST/PUT/PATCH/DELETE 等方法的语义、幂等与可缓存性。',
  'intro': 'REST 接口常用 HTTP 方法表达操作类型。本工具列出各方法语义、是否幂等、是否安全、典型场景，便于接口设计与排错。纯前端，无请求发出。',
  'features': ['方法语义对照', '幂等/安全性标注', '典型场景示例', '状态码关联', '本地处理'],
  'scenarios': ['设计 REST 接口', '排查 405 方法不允许', '团队接口规范对齐'],
  'steps': ['选或搜方法名', '查看语义与属性', '按场景套用'],
  'tips': ['GET 应无副作用', 'PUT 整替换/POST 新建', 'PATCH 局部更新', 'DELETE 幂等'],
  'faqs': [('PUT 和 POST 区别？', 'PUT 目标已知且幂等，POST 由服务端决定新资源。'), ('能给个例子吗？', 'GET /users 列表，POST /users 新建。')],
  'en_name': 'HTTP Methods Reference',
  'en_desc': 'HTTP Methods Reference Guide: compare GET/POST/PUT/PATCH/DELETE semantics, idempotency and cacheability.',
  'en_intro': 'REST APIs use HTTP methods to express operation types. This tool lists each method’s meaning, idempotency, safety and typical use, handy for API design and debugging. Pure front-end, no requests sent.',
  'en_features': ['Method semantics table', 'Idempotent/safe flags', 'Typical scenario samples', 'Status-code links', 'Local processing'],
  'en_scenarios': ['Design REST APIs', 'Debug 405 Method Not Allowed', 'Align team API conventions'],
  'en_steps': ['Pick or search a method', 'See semantics and flags', 'Apply by scenario'],
  'en_tips': ['GET should be side-effect free', 'PUT replaces / POST creates', 'PATCH is partial update', 'DELETE is idempotent'],
  'en_faqs': [('PUT vs POST?', 'PUT targets a known, idempotent resource; POST lets the server decide the new one.'), ('Example?', 'GET /users lists, POST /users creates.')],
 },
 {
  'slug': 'text-to-braille',
  'ind': 'text',
  'base': 'text-to-braille.html',
  'name': '文本转盲文',
  'desc': '文本转盲文使用指南：把拉丁字母与数字转成盲文点字（英语 Grade-1），支持逐字对照。',
  'intro': '盲文用 6 点单元格表示字符。本工具按英语盲文字母表映射，给出原文与盲文的逐字对照，便于教学与无障碍排版。纯前端，不上传文本。',
  'features': ['字母→盲文映射', '逐字对照', '数字支持', '空格/标点处理', '本地处理'],
  'scenarios': ['无障碍排版预览', '盲文教学演示', '标签/铭牌制作'],
  'steps': ['输入英文文本', '点击转换', '查看盲文对照'],
  'tips': ['仅 Grade-1 字母级', '大小写同为一点', '中文需先转拼音'],
  'faqs': [('支持中文吗？', '盲文按字母，中文需先转拼音或专用汉盲方案。'), ('能给个例子吗？', 'a 对应 ⠁（第1点）。')],
  'en_name': 'Text to Braille',
  'en_desc': 'Text to Braille Guide: convert Latin letters and digits to Braille (English Grade-1) with per-character mapping.',
  'en_intro': 'Braille uses a 6-dot cell per character. This tool maps by the English Braille alphabet and shows source-to-Braille per character, useful for teaching and accessible layout. Pure front-end, text not uploaded.',
  'en_features': ['Letter to Braille map', 'Per-character match', 'Digit support', 'Space/punctuation handling', 'Local processing'],
  'en_scenarios': ['Accessible layout preview', 'Braille teaching demo', 'Label/nameplate making'],
  'en_steps': ['Enter English text', 'Click convert', 'View Braille mapping'],
  'en_tips': ['Grade-1 letter level only', 'Upper/lower same dot', 'Chinese needs pinyin first'],
  'en_faqs': [('Chinese supported?', 'Braille is per-letter; Chinese needs pinyin or a dedicated scheme first.'), ('Example?', 'a maps to ⠁ (dot 1).')],
 },
 {
  'slug': 'text-to-1337',
  'ind': 'text',
  'base': 'text-to-1337.html',
  'name': '文本转 1337',
  'desc': '文本转 1337 使用指南：把字母替换成形似的数字/符号（leet speak），用于昵称与趣味风格。',
  'intro': '1337（leet）用数字与符号替代字母，如 e→3、a→4、t→7。本工具按常见映射转换，可调强度。纯前端，不上传文本。',
  'features': ['字母→符号映射', '常见 leet 表', '整词转换', '可还原提示', '本地处理'],
  'scenarios': ['游戏昵称生成', '趣味文案风格', '教学字符替换'],
  'steps': ['输入普通文本', '点击转换', '复制 leet 结果'],
  'tips': ['同一字母多种写法', '强度越高越难读', '非加密请勿当密码'],
  'faqs': [('能反解吗？', '不能保证唯一，属风格替换。'), ('能给个例子吗？', 'leet 转为 1337。')],
  'en_name': 'Text to 1337',
  'en_desc': 'Text to 1337 Guide: replace letters with look-alike digits/symbols (leet speak) for nicknames and fun style.',
  'en_intro': '1337 (leet) swaps letters for digits and symbols, e.g. e→3, a→4, t→7. This tool converts by common mapping with adjustable strength. Pure front-end, text not uploaded.',
  'en_features': ['Letter to symbol map', 'Common leet table', 'Whole-word convert', 'Reversible note', 'Local processing'],
  'en_scenarios': ['Game nickname', 'Fun copy style', 'Teach char substitution'],
  'en_steps': ['Enter plain text', 'Click convert', 'Copy the leet result'],
  'en_tips': ['One letter has many forms', 'Higher strength is harder to read', 'Not encryption, do not use as password'],
  'en_faqs': [('Reversible?', 'Not guaranteed unique; it is a style swap.'), ('Example?', 'leet becomes 1337.')],
 },
 {
  'slug': 'binary-to-ascii',
  'ind': 'encode',
  'base': 'binary-to-ascii.html',
  'name': '二进制转 ASCII',
  'desc': '二进制转 ASCII 使用指南：把 0/1 比特串按 8 位一组转成字符，也支持反向转换。',
  'intro': 'ASCII 字符用 8 位二进制表示（如 A=01000001）。本工具双向转换并校验位数，便于理解编码与排错。纯前端，不上传。',
  'features': ['二进→字符', '字符→二进', '8 位分组校验', '空格分隔可选', '本地处理'],
  'scenarios': ['理解字符编码', '校验传输比特', '教学二进制'],
  'steps': ['粘贴二进制或文本', '点击转换', '查看结果'],
  'tips': ['按 8 位分组', '非 8 倍数会报错', '可用空格分隔'],
  'faqs': [('中文能用吗？', 'ASCII 仅覆盖英文字符，中文需用 UTF-8 多字节。'), ('能给个例子吗？', '01000001 是 A。')],
  'en_name': 'Binary to ASCII',
  'en_desc': 'Binary to ASCII Guide: turn a 0/1 bit string into characters in 8-bit groups, and convert back.',
  'en_intro': 'ASCII characters are 8 bits (e.g. A=01000001). This tool converts both ways and checks grouping, handy for understanding encoding. Pure front-end, nothing uploaded.',
  'en_features': ['Binary to char', 'Char to binary', '8-bit group check', 'Optional space split', 'Local processing'],
  'en_scenarios': ['Understand character encoding', 'Verify transmitted bits', 'Teach binary'],
  'en_steps': ['Paste binary or text', 'Click convert', 'See the result'],
  'en_tips': ['Group by 8 bits', 'Non-multiple of 8 errors', 'Spaces allowed between groups'],
  'en_faqs': [('Chinese works?', 'ASCII covers English only; Chinese needs multi-byte UTF-8.'), ('Example?', '01000001 is A.')],
 },
 {
  'slug': 'text-to-ascii-art',
  'ind': 'text',
  'base': 'text-to-ascii-art.html',
  'name': '文本转 ASCII 艺术字',
  'desc': '文本转 ASCII 艺术字使用指南：把输入文字渲染成终端风格的 ASCII 大字（figlet 风格）。',
  'intro': '用点阵字体把文字放大成由字符组成的图案，常用于 README 横幅与终端欢迎语。本工具按字体渲染并支持复制。纯前端，不上传。',
  'features': ['多种字体风格', '横幅大字渲染', '一键复制', '宽度自适应', '本地处理'],
  'scenarios': ['README 横幅', '终端欢迎语', '趣味签名'],
  'steps': ['输入文字', '选字体', '点击生成复制'],
  'tips': ['中文需用专用字体', '注意等宽显示', '太长会折行'],
  'faqs': [('能导出图片吗？', '本工具输出文本，可截图或粘到代码块。'), ('能给个例子吗？', '"HI" 渲染成由 # 组成的大字。')],
  'en_name': 'Text to ASCII Art',
  'en_desc': 'Text to ASCII Art Guide: render input text into terminal-style ASCII banner art (figlet style).',
  'en_intro': 'A dot-matrix font enlarges text into character art, common for README banners and terminal greetings. This tool renders by font and supports copy. Pure front-end, nothing uploaded.',
  'en_features': ['Multiple font styles', 'Banner art render', 'One-click copy', 'Width auto-fit', 'Local processing'],
  'en_scenarios': ['README banner', 'Terminal greeting', 'Fun signature'],
  'en_steps': ['Enter text', 'Pick a font', 'Generate and copy'],
  'en_tips': ['Chinese needs a dedicated font', 'Use monospace to view', 'Too long wraps'],
  'en_faqs': [('Export as image?', 'This tool outputs text; screenshot or paste into a code block.'), ('Example?', '"HI" renders as large # art.')],
 },
 {
  'slug': 'triangle-calculator',
  'ind': 'it',
  'base': 'triangle-calculator.html',
  'name': '三角形计算器',
  'desc': '三角形计算器使用指南：按三边/两边夹角/直角条件计算面积、周长、角度与类型。',
  'intro': '给定足够边长与角度，可求面积（海伦公式/底高）、各角与是否为直角/等腰/等边。本工具按输入模式求解并校验构成条件。纯前端，不上传。',
  'features': ['三边求面积', '直角/等腰识别', '角度计算', '构成条件校验', '本地处理'],
  'scenarios': ['几何作业验算', '裁剪/施工尺寸', '教学三角形性质'],
  'steps': ['选输入模式', '填边长/角度', '点击计算看结果'],
  'tips': ['两边和大于第三边', '角度和 180°', '直角三角形可用勾股'],
  'faqs': [('只给两个边能算吗？', '需再加一个角或边才能唯一确定。'), ('能给个例子吗？', '3/4/5 是直角三角形。')],
  'en_name': 'Triangle Calculator',
  'en_desc': 'Triangle Calculator Guide: compute area, perimeter, angles and type from sides/angle or right-triangle conditions.',
  'en_intro': 'Given enough sides and angles, find area (Heron/base-height), angles and whether right/isosceles/equilateral. This tool solves by input mode and validates triangle inequality. Pure front-end, nothing uploaded.',
  'en_features': ['Area from 3 sides', 'Right/isosceles detect', 'Angle compute', 'Validity check', 'Local processing'],
  'en_scenarios': ['Geometry homework check', 'Cutting/building sizes', 'Teach triangle properties'],
  'en_steps': ['Pick input mode', 'Fill sides/angles', 'Click to see results'],
  'en_tips': ['Sum of two sides > third', 'Angles sum to 180°', 'Right triangle uses Pythagoras'],
  'en_faqs': [('Two sides enough?', 'Need one more angle or side to be unique.'), ('Example?', '3/4/5 is a right triangle.')],
 },
 {
  'slug': 'prime-checker',
  'ind': 'it',
  'base': 'prime-checker.html',
  'name': '质数检测',
  'desc': '质数检测使用指南：判断一个整数是否为质数，并给出因数分解与最近质数。',
  'intro': '质数只能被 1 和自身整除。本工具用试除法/优化算法判定，并列出因数与邻近质数，适合学习与校验。纯前端，不上传。',
  'features': ['质数判定', '因数分解', '最近质数', '大数支持', '本地处理'],
  'scenarios': ['数学习题校验', '密钥长度认知', '筛法教学'],
  'steps': ['输入整数', '点击检测', '查看判定与因数'],
  'tips': ['1 不是质数', '负数不参与', '超大数耗时增加'],
  'faqs': [('0 和 1 呢？', '均不视为质数。'), ('能给个例子吗？', '17 是质数，15=3×5。')],
  'en_name': 'Prime Checker',
  'en_desc': 'Prime Checker Guide: test if an integer is prime, with factorization and nearest primes.',
  'en_intro': 'A prime divides only by 1 and itself. This tool decides with optimized trial division and lists factors and neighbor primes, good for study and checks. Pure front-end, nothing uploaded.',
  'en_features': ['Primality test', 'Factorization', 'Nearest primes', 'Big number support', 'Local processing'],
  'en_scenarios': ['Math exercise check', 'Key-length awareness', 'Sieve teaching'],
  'en_steps': ['Enter an integer', 'Click check', 'See verdict and factors'],
  'en_tips': ['1 is not prime', 'Negatives excluded', 'Huge numbers take longer'],
  'en_faqs': [('0 and 1?', 'Neither is prime.'), ('Example?', '17 is prime, 15=3×5.')],
 },
 {
  'slug': 'color-shade-generator',
  'ind': 'design',
  'base': 'color-shade-generator.html',
  'name': '颜色明暗生成器',
  'desc': '颜色明暗生成器使用指南：基于一个基色生成由浅到深的明暗梯度，用于主题与组件配色。',
  'intro': '设计系统常用同一色相的 50–900 梯度。本工具按 HSL 明度变化生成阶梯，便于批量产出一致配色。纯前端，不上传。',
  'features': ['基色→梯度', 'HSL 明度步进', 'CSS 变量输出', '深浅预览', '本地处理'],
  'scenarios': ['设计系统配色', '按钮/状态色阶', '图表色板'],
  'steps': ['输入基色', '选档位数', '生成复制梯度'],
  'tips': ['用 HSL 更均匀', '避免两端过暗/过亮', '可直接出 CSS 变量'],
  'faqs': [('和调色板工具有何不同？', '本工具只做单色明暗梯度，不做互补/类比。'), ('能给个例子吗？', '输出 50/100/.../900 共 10 档。')],
  'en_name': 'Color Shade Generator',
  'en_desc': 'Color Shade Generator Guide: from a base color, generate light-to-dark shade ramps for themes and components.',
  'en_intro': 'Design systems often use a 50–900 ramp of one hue. This tool steps lightness in HSL to produce consistent ramps in bulk. Pure front-end, nothing uploaded.',
  'en_features': ['Base to ramp', 'HSL lightness step', 'CSS variable output', 'Light/dark preview', 'Local processing'],
  'en_scenarios': ['Design-system palette', 'Button/state ramps', 'Chart color board'],
  'en_steps': ['Enter base color', 'Pick steps', 'Generate and copy ramp'],
  'en_tips': ['HSL gives even steps', 'Avoid too dark/bright ends', 'Can emit CSS variables'],
  'en_faqs': [('Different from a palette tool?', 'This only does single-hue shade ramps, not complementary/analogous.'), ('Example?', 'Outputs 10 steps 50/100/.../900.')],
 },
 {
  'slug': 'wifi-qr-generator',
  'ind': 'it',
  'base': 'wifi-qr-generator.html',
  'name': 'WiFi 配网二维码生成器',
  'desc': 'WiFi 配网二维码生成器使用指南：把 SSID 与密码编码成 WiFi 二维码，手机扫码直连。',
  'intro': '遵循 WIFI:S:...;T:...;P:...; 格式生成二维码，访客扫码即可连网，免去口述密码。纯前端，密码仅本地编码不上传。',
  'features': ['SSID/密码编码', '加密类型选择', '扫码直连', '二维码预览', '本地处理'],
  'scenarios': ['访客临时连网', '店铺/活动 WiFi 牌', '家庭共享网络'],
  'steps': ['填 SSID 与密码', '选加密类型', '生成二维码展示'],
  'tips': ['含特殊字符照常', '隐藏网络需勾选', '生成后自测扫码'],
  'faqs': [('安全吗？', '二维码含密码，仅当面分享，勿公开张贴。'), ('能给个例子吗？', '格式 WIFI:S:Home;T:WPA;P:1234;;。')],
  'en_name': 'WiFi QR Generator',
  'en_desc': 'WiFi QR Generator Guide: encode SSID and password into a WiFi QR for one-tap connect.',
  'en_intro': 'Following WIFI:S:...;T:...;P:...; it emits a QR that guests scan to join, no spoken password. Pure front-end, password encoded locally only.',
  'en_features': ['SSID/password encode', 'Encryption pick', 'Scan to connect', 'QR preview', 'Local processing'],
  'en_scenarios': ['Guest temporary access', 'Shop/event WiFi sign', 'Home network share'],
  'en_steps': ['Fill SSID and password', 'Pick encryption', 'Generate and show QR'],
  'en_tips': ['Special chars fine', 'Hidden SSID needs a flag', 'Test-scan after making'],
  'en_faqs': [('Safe?', 'QR holds the password; share in person only, not publicly.'), ('Example?', 'Format WIFI:S:Home;T:WPA;P:1234;;.')],
 },
 {
  'slug': 'gradient-generator',
  'ind': 'design',
  'base': 'gradient-generator.html',
  'name': 'CSS 渐变生成器',
  'desc': 'CSS 渐变生成器使用指南：可视化生成线性/径向渐变，输出可直接使用的 CSS 代码。',
  'intro': '渐变是常用背景装饰。本工具调节起止色、角度与色标，实时预览并复制 linear/radial-gradient 代码。纯前端，不上传。',
  'features': ['线性/径向渐变', '角度与色标调节', '实时预览', 'CSS 代码输出', '本地处理'],
  'scenarios': ['按钮/背景装饰', '卡片封面渐变', '落地页 hero 区'],
  'steps': ['加色标调角度', '实时预览', '复制 CSS'],
  'tips': ['至少两个色标', '角度 0–360', '可用透明度色标'],
  'faqs': [('径向怎么写？', 'radial-gradient(shape at pos, c1, c2)。'), ('能给个例子吗？', 'linear-gradient(135deg,#FF6B35,#7C3AED)。')],
  'en_name': 'CSS Gradient Generator',
  'en_desc': 'CSS Gradient Generator Guide: visually build linear/radial gradients and output ready-to-use CSS.',
  'en_intro': 'Gradients are common background decor. Adjust start/end colors, angle and stops, preview live and copy linear/radial-gradient code. Pure front-end, nothing uploaded.',
  'en_features': ['Linear/radial gradient', 'Angle and stop tuning', 'Live preview', 'CSS code output', 'Local processing'],
  'en_scenarios': ['Button/background decor', 'Card cover gradient', 'Landing hero'],
  'en_steps': ['Add stops, tune angle', 'Preview live', 'Copy CSS'],
  'en_tips': ['At least two stops', 'Angle 0–360', 'Transparent stops allowed'],
  'en_faqs': [('Radial syntax?', 'radial-gradient(shape at pos, c1, c2).'), ('Example?', 'linear-gradient(135deg,#FF6B35,#7C3AED).')],
 },
 {
  'slug': 'reading-time-estimator',
  'ind': 'text',
  'base': 'reading-time-estimator.html',
  'name': '阅读时长估算器',
  'desc': '阅读时长估算器使用指南：按字数/词数估算文章阅读时间，支持中英文与语速设定。',
  'intro': '中文约 300–500 字/分钟、英文约 200–250 词/分钟。本工具按文本长度与设定语速给出阅读时长，便于内容排版标注。纯前端，不上传。',
  'features': ['中英文识别', '语速可调', '字数统计', '时长区间', '本地处理'],
  'scenarios': ['文章标注阅读时长', '播客/讲义准备', '内容排版预估'],
  'steps': ['粘贴正文', '选语言与语速', '查看时长'],
  'tips': ['中英混排取近似', '含代码/表格另算', '语速因人而异'],
  'faqs': [('图片算时间吗？', '一般按张数另估，本工具只算文字。'), ('能给个例子吗？', '1500 中文字约 4–5 分钟。')],
  'en_name': 'Reading Time Estimator',
  'en_desc': 'Reading Time Estimator Guide: estimate article read time by characters/words, with CN/EN and speed settings.',
  'en_intro': 'Chinese ~300–500 chars/min, English ~200–250 words/min. This tool gives read time by length and set speed, useful for labeling content. Pure front-end, nothing uploaded.',
  'en_features': ['CN/EN detect', 'Adjustable speed', 'Word count', 'Time range', 'Local processing'],
  'en_scenarios': ['Label read time', 'Podcast/lecture prep', 'Layout estimate'],
  'en_steps': ['Paste text', 'Pick language and speed', 'See the time'],
  'en_tips': ['Mixed CN/EN is approximate', 'Code/tables differ', 'Speed varies by person'],
  'en_faqs': [('Images counted?', 'Usually estimated per image; this tool counts text only.'), ('Example?', '1500 Chinese chars ≈ 4–5 min.')],
 },
 {
  'slug': 'gst-calculator',
  'ind': 'tax',
  'base': 'gst-calculator.html',
  'name': 'GST 计算器',
  'desc': 'GST 计算器使用指南：在含税/不含税金额与 GST 税率间互算，支持加税与反向还原。',
  'intro': 'GST（商品服务税）常见于多国。本工具按税率在含税价、不含税价、税额间转换，便于报价与开票。纯前端，不上传。',
  'features': ['含税↔不含税', '税额计算', '税率可调', '多档提示', '本地处理'],
  'scenarios': ['报价含稅核算', '发票金额还原', '跨境采购计税'],
  'steps': ['选计算模式', '填金额与税率', '点击计算'],
  'tips': ['含税=不含税×(1+率)', '反向用除法', '小数位注意'],
  'faqs': [('GST 和 VAT 区别？', '机制类似，命名不同。'), ('能给个例子吗？', '不含税 100、率 10%，含税 110。')],
  'en_name': 'GST Calculator',
  'en_desc': 'GST Calculator Guide: convert between inclusive/exclusive amounts and GST rate, with add and reverse modes.',
  'en_intro': 'GST (Goods and Services Tax) is common worldwide. This tool converts among inclusive price, exclusive price and tax by rate, handy for quotes and invoices. Pure front-end, nothing uploaded.',
  'en_features': ['Inclusive to exclusive', 'Tax amount', 'Adjustable rate', 'Multi-rate hint', 'Local processing'],
  'en_scenarios': ['Quote with tax', 'Invoice amount reverse', 'Cross-border purchase'],
  'en_steps': ['Pick mode', 'Fill amount and rate', 'Click calculate'],
  'en_tips': ['Inclusive = exclusive ×(1+rate)', 'Reverse uses division', 'Mind decimals'],
  'en_faqs': [('GST vs VAT?', 'Similar mechanism, different name.'), ('Example?', 'Exclusive 100, rate 10% → inclusive 110.')],
 },
 {
  'slug': 'recipe-scaler',
  'ind': 'baking',
  'base': 'recipe-scaler.html',
  'name': '配方缩放器',
  'desc': '配方缩放器使用指南：按目标份数等比缩放食材用量，保留单位与分数表达。',
  'intro': '烘焙对比例敏感。本工具按原份数与目标份数缩放每种食材，支持分数（1/2 杯）与小数，便于调整产量。纯前端，不上传。',
  'features': ['份数等比缩放', '分数/小数支持', '单位保留', '批量食材', '本地处理'],
  'scenarios': ['加倍/减半配方', '适应模具尺寸', '批量制作换算'],
  'steps': ['填原份数与目标', '列食材用量', '点击缩放'],
  'tips': ['液体按体积', '烤箱温度不缩放', '留意整数进位'],
  'faqs': [('温度也缩放吗？', '不，温度按经验调，本工具只缩用量。'), ('能给个例子吗？', '2 人→4 人，用量全×2。')],
  'en_name': 'Recipe Scaler',
  'en_desc': 'Recipe Scaler Guide: scale ingredient amounts by target servings, keeping units and fractions.',
  'en_intro': 'Baking is ratio-sensitive. This tool scales each ingredient by original vs target servings, with fractions (1/2 cup) and decimals. Pure front-end, nothing uploaded.',
  'en_features': ['Servings scale', 'Fraction/decimal', 'Unit kept', 'Bulk ingredients', 'Local processing'],
  'en_scenarios': ['Double/halve a recipe', 'Fit a mold size', 'Batch conversion'],
  'en_steps': ['Fill original and target', 'List amounts', 'Click scale'],
  'en_tips': ['Liquids by volume', 'Oven temp not scaled', 'Mind integer rounding'],
  'en_faqs': [('Scale temperature too?', 'No, temperature is empirical; this scales amounts only.'), ('Example?', '2→4 servings, amounts ×2.')],
 },
 {
  'slug': 'fuel-cost-calculator',
  'ind': 'automotive',
  'base': 'fuel-cost-calculator.html',
  'name': '油费计算器',
  'desc': '油费计算器使用指南：按里程、油耗与油价估算出行油费，支持往返与多人分摊。',
  'intro': '油费 = 里程 ÷ 100 × 油耗 × 油价。本工具输入里程、百公里油耗与单价即得总费用，可算往返。纯前端，不上传。',
  'features': ['里程油费估算', '往返计算', '单公里成本', '多人分摊', '本地处理'],
  'scenarios': ['通勤成本核算', '自驾游预算', '拼车费用结算'],
  'steps': ['填里程/油耗/油价', '选往返', '点击计算'],
  'tips': ['油耗用 L/100km', '油价用元/升', '高速油耗略高'],
  'faqs': [('电动车怎么算？', '按电耗×电价，公式类似。'), ('能给个例子吗？', '300km、8L、7.5 元≈180 元。')],
  'en_name': 'Fuel Cost Calculator',
  'en_desc': 'Fuel Cost Calculator Guide: estimate trip fuel cost by distance, consumption and price, with round-trip and split.',
  'en_intro': 'Cost = distance ÷ 100 × consumption × price. Enter distance, L/100km and unit price for the total, round-trip supported. Pure front-end, nothing uploaded.',
  'en_features': ['Distance cost', 'Round trip', 'Per-km cost', 'Split by people', 'Local processing'],
  'en_scenarios': ['Commute cost', 'Road-trip budget', 'Carpool settle'],
  'en_steps': ['Fill distance/consumption/price', 'Pick round trip', 'Click calculate'],
  'en_tips': ['Consumption in L/100km', 'Price per liter', 'Highway uses a bit more'],
  'en_faqs': [('EV?', 'Use kWh/100km × electricity price, similar formula.'), ('Example?', '300km, 8L, 7.5 ≈ 180 yuan.')],
 },
 {
  'slug': 'parking-fee',
  'ind': 'daily-goods',
  'base': 'parking-fee.html',
  'name': '停车费计算器',
  'desc': '停车费计算器使用指南：按入场/出场时间与计费规则估算停车费用，支持首时段与封顶。',
  'intro': '停车场常按小时计费，含免费时段、首小时价与每日封顶。本工具按时长与规则算出费用，便于预算与核对。纯前端，不上传。',
  'features': ['时长计算', '首时段/封顶', '免费分钟', '分段单价', '本地处理'],
  'scenarios': ['商场停车预算', '医院/机场长停', '费用核对'],
  'steps': ['填入场出场', '设计费规则', '点击算费'],
  'tips': ['注意免费分钟', '跨日按规则', '封顶很关键'],
  'faqs': [('过夜怎么算？', '按规则跨日累计或重新计费。'), ('能给个例子吗？', '3 小时、首时 10、后续 5/时≈20。')],
  'en_name': 'Parking Fee Calculator',
  'en_desc': 'Parking Fee Calculator Guide: estimate parking cost by entry/exit time and billing rules, with first period and cap.',
  'en_intro': 'Lots bill by hour with free minutes, first-hour price and daily cap. This tool computes cost by duration and rules for budgeting and checks. Pure front-end, nothing uploaded.',
  'en_features': ['Duration calc', 'First period/cap', 'Free minutes', 'Tiered rate', 'Local processing'],
  'en_scenarios': ['Mall parking budget', 'Hospital/airport long stay', 'Cost check'],
  'en_steps': ['Fill entry/exit', 'Set rules', 'Click calculate'],
  'en_tips': ['Mind free minutes', 'Cross-day per rules', 'Cap matters most'],
  'en_faqs': [('Overnight?', 'Accumulates or restarts per rules across days.'), ('Example?', '3h, first 10, then 5/h ≈ 20.')],
 },
 {
  'slug': 'unit-price-compare',
  'ind': 'biz',
  'base': 'unit-price-compare.html',
  'name': '单位价格比较器',
  'desc': '单位价格比较器使用指南：把不同规格商品的总价折算为单价，找出更划算的一档。',
  'intro': '大包装未必更便宜。本工具按总价与净含量算出每单位价格（元/件、元/100g 等），横向比较选出最优。纯前端，不上传。',
  'features': ['折算单价', '多规格对比', '自定义单位', '最优高亮', '本地处理'],
  'scenarios': ['超市比价', '电商规格选择', '采购成本优化'],
  'steps': ['填各规格价格与量', '设单位', '点击比较'],
  'tips': ['统一计量单位', '注意净含量', '促销折算到单'],
  'faqs': [('买大包一定省？', '不一定，按单价比较才准。'), ('能给个例子吗？', '500g/10 元 vs 1kg/18 元，后者更省。')],
  'en_name': 'Unit Price Compare',
  'en_desc': 'Unit Price Compare Guide: convert different pack prices to a unit price to find the better deal.',
  'en_intro': 'Big packs are not always cheaper. This tool computes per-unit price (yuan/piece, yuan/100g) from total price and net content for a fair comparison. Pure front-end, nothing uploaded.',
  'en_features': ['Unit price', 'Multi-pack compare', 'Custom unit', 'Best highlight', 'Local processing'],
  'en_scenarios': ['Supermarket compare', 'E-commerce size pick', 'Procurement optimize'],
  'en_steps': ['Fill price and amount', 'Set unit', 'Click compare'],
  'en_tips': ['Unify the measure', 'Mind net content', 'Promo to per-unit'],
  'en_faqs': [('Big pack always cheaper?', 'Not necessarily; compare by unit price.'), ('Example?', '500g/10 vs 1kg/18, the latter is cheaper.')],
 },
 {
  'slug': 'color-blindness-sim',
  'ind': 'design',
  'base': 'color-blindness-sim.html',
  'name': '色盲模拟器',
  'desc': '色盲模拟器使用指南：模拟红绿/蓝黄色盲等类型下页面与配色的观感，辅助无障碍设计。',
  'intro': '约 8% 男性有色觉差异。本工具按常见色盲矩阵变换图片或取色，预览不同视觉下的效果，帮助检查对比度。纯前端，不上传。',
  'features': ['多类型模拟', '取色预览', '对比度提示', '图片/色块', '本地处理'],
  'scenarios': ['无障碍配色检查', '图表可辨识性', 'UI 红绿区分'],
  'steps': ['选色盲类型', '取色或传图', '预览差异'],
  'tips': ['别仅靠红绿', '加形状/文字区分', '看对比度'],
  'faqs': [('有几种常见类型？', '红绿（最常见）、蓝黄、全色弱等。'), ('能给个例子吗？', '红绿色盲下红绿易混，可用蓝橙替代。')],
  'en_name': 'Color Blindness Simulator',
  'en_desc': 'Color Blindness Simulator Guide: simulate how pages and palettes look under protan/deutan/tritan types for accessible design.',
  'en_intro': 'About 8% of men have color-vision difference. This tool transforms colors or images by common matrices to preview, helping check contrast. Pure front-end, nothing uploaded.',
  'en_features': ['Multiple types', 'Color pick preview', 'Contrast hint', 'Image/block', 'Local processing'],
  'en_scenarios': ['Accessible palette check', 'Chart readability', 'UI red/green split'],
  'en_steps': ['Pick type', 'Pick color or image', 'Preview difference'],
  'en_tips': ['Do not rely on red/green alone', 'Add shape/text cues', 'Check contrast'],
  'en_faqs': [('How many types?', 'Red-green (most common), blue-yellow, monochromacy, etc.'), ('Example?', 'Under red-green, use blue/orange instead of red/green.')],
 },
]

TPL = '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title{head_title_attr}>{title}使用指南 - ToolBox</title>
<meta name="description"{head_desc_attr} content="{desc}">
<meta property="og:title"{head_title_attr2} content="{title}使用指南 - ToolBox">
<meta property="og:type" content="article">
<meta property="og:site_name" content="ToolBox">
<meta property="og:url" content="{canonical}">
<meta property="og:description"{head_desc_attr} content="{desc}">
<meta property="og:image" content="https://chenguangwu.github.io/og-image.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="ToolBox - 免费在线工具与使用指南">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title"{head_title_attr2} content="{title}使用指南 - ToolBox">
<meta name="twitter:description"{head_desc_attr} content="{desc}">
<meta name="twitter:image" content="https://chenguangwu.github.io/og-image.png">
<meta name="twitter:image:alt" content="ToolBox - 免费在线工具与使用指南">
<link rel="canonical" href="{canonical}">
<link rel="alternate" hreflang="zh-CN" href="{canonical}">
<link rel="alternate" hreflang="en-US" href="{canonical}">
<link rel="alternate" hreflang="x-default" href="{canonical}">
<script type="application/ld+json">
{"@context":"https://schema.org","@type":"Article","headline":"{title}使用指南","description":"{desc}","author":{"@type":"Organization","name":"ToolBox"},"inLanguage":"zh-CN"}
</script>
<script defer src="https://chenguangwu.github.io/js/i18n.js"></script>
<script defer src="https://chenguangwu.github.io/js/guide-en-pack.js"></script>
<script defer src="https://chenguangwu.github.io/js/guide-i18n.js"></script>
<style>
:root{--primary:#FF6B35;--text:#1F2937;--muted:#6B7280;--border:#E5E7EB;--bg:#FFFAF7;}
*{box-sizing:border-box;}
body{margin:0;font-family:"Noto Sans SC","Plus Jakarta Sans",system-ui,sans-serif;color:var(--text);background:var(--bg);line-height:1.75;}
header{padding:18px 20px;border-bottom:1px solid var(--border);background:#fff;}
.breadcrumb a{color:var(--primary);text-decoration:none;margin-right:6px;}
.breadcrumb a:hover{text-decoration:underline;}
main{max-width:780px;margin:0 auto;padding:28px 20px 60px;}
h1{font-size:28px;margin:0 0 8px;}
.lead{font-size:16px;color:var(--muted);margin:0 0 22px;}
h2{font-size:20px;margin:28px 0 10px;color:var(--primary);}
ul,ol{padding-left:22px;}
li{margin:6px 0;}
dl{margin:0;}
dt{font-weight:700;margin-top:12px;}
dd{margin:4px 0 0;color:var(--muted);}
.back{margin-top:30px;padding:16px;background:#fff;border:1px solid var(--border);border-radius:14px;}
.back a{color:var(--primary);font-weight:700;text-decoration:none;}
footer{text-align:center;color:var(--muted);font-size:13px;padding:24px;border-top:1px solid var(--border);}
</style>
</head>
<body>
<header><nav class="breadcrumb"><a href="{home}">ToolBox</a> / <a href="{home}#guides"{nav_guides}>{nav_guides_fb}使用指南</a> / <span{title_attr}>{title}</span></nav></header>
<main>
<h1{title_attr}>{title} 使用指南</h1>
<p class="lead"{intro_attr}>{intro}</p>
<h2{sec_features}>核心功能</h2>
<ul>{features}</ul>
<h2{sec_scenarios}>适用场景</h2>
<ul>{scenarios}</ul>
<h2{sec_steps}>使用步骤</h2>
<ol>{steps}</ol>
<h2{sec_tips}>实用技巧</h2>
<ul>{tips}</ul>
<h2{sec_faqs}>常见问题</h2>
<dl>{faqs}</dl>
<div class="back"><a href="{tool_url}">→ 去使用 {title}（免费 · 纯前端 · 数据不上传）</a></div>
</main>
<footer>© 2026 ToolBox · 纯前端在线工具 · 数据不上传，安全可靠</footer>
</body>
</html>
'''

def li(items, slug, field, en_items=None):
    out = []
    for i, x in enumerate(items):
        if en_items and i < len(en_items) and en_items[i]:
            key = 'guide.%s.%s.%d' % (slug, field, i)
            out.append('<li data-i18n="%s" data-i18n-fb="%s">%s</li>'
                       % (key, html.escape(str(x)), html.escape(str(x))))
        else:
            out.append('<li>%s</li>' % html.escape(str(x)))
    return ''.join(out)

def render_faqs(g):
    out = []
    en = g.get('en_faqs')
    for i, (q, a) in enumerate(g['faqs']):
        if en and i < len(en) and en[i]:
            qk = 'guide.%s.faqs.%d.q' % (g['slug'], i)
            ak = 'guide.%s.faqs.%d.a' % (g['slug'], i)
            out.append('<dt data-i18n="%s" data-i18n-fb="%s">%s</dt><dd data-i18n="%s" data-i18n-fb="%s">%s</dd>'
                       % (qk, html.escape(q), html.escape(q), ak, html.escape(a), html.escape(a)))
        else:
            out.append('<dt>%s</dt><dd>%s</dd>' % (html.escape(q), html.escape(a)))
    return ''.join(out)

GUIDE_EN_PACK = {
    'guide._section.features': 'Key Features',
    'guide._section.scenarios': 'Use Cases',
    'guide._section.steps': 'How to Use',
    'guide._section.tips': 'Pro Tips',
    'guide._section.faqs': 'FAQ',
    'guide._nav.guides': 'Guides',
}

def render(g):
    fn = '%s-guide.html' % g['slug']
    canonical = '%s/guides/%s' % (SITE, fn)
    has_en = 'en_name' in g
    if has_en:
        for fld in ('name', 'desc', 'intro', 'features', 'scenarios', 'steps', 'tips', 'faqs'):
            ek = 'en_' + fld
            if ek not in g:
                continue
            if fld in ('features', 'scenarios', 'steps', 'tips'):
                for i, v in enumerate(g[ek]):
                    GUIDE_EN_PACK['guide.%s.%s.%d' % (g['slug'], fld, i)] = v
            elif fld == 'faqs':
                for i, (q, a) in enumerate(g[ek]):
                    GUIDE_EN_PACK['guide.%s.faqs.%d.q' % (g['slug'], i)] = q
                    GUIDE_EN_PACK['guide.%s.faqs.%d.a' % (g['slug'], i)] = a
            elif fld == 'name':
                GUIDE_EN_PACK['guide.%s.title' % g['slug']] = g[ek]
                GUIDE_EN_PACK['guide.%s.back' % g['slug']] = 'Open %s (Free · client-side · no upload)' % g[ek]
            else:
                GUIDE_EN_PACK['guide.%s.%s' % (g['slug'], fld)] = g[ek]
        title_attr = ' data-i18n="guide.%s.title" data-i18n-fb="%s 使用指南"' % (g['slug'], html.escape(g['name']))
        intro_attr = ' data-i18n="guide.%s.intro" data-i18n-fb="%s"' % (g['slug'], html.escape(g['intro']))
        nav_guides = ' data-i18n="guide._nav.guides" data-i18n-fb="'
        nav_guides_fb = ' '
        back_attr = ' data-i18n="guide.%s.back" data-i18n-fb="→ 去使用 %s（免费 · 纯前端 · 数据不上传）"' % (g['slug'], html.escape(g['name']))
        sec_features = ' data-i18n="guide._section.features" data-i18n-fb="核心功能"'
        sec_scenarios = ' data-i18n="guide._section.scenarios" data-i18n-fb="适用场景"'
        sec_steps = ' data-i18n="guide._section.steps" data-i18n-fb="使用步骤"'
        sec_tips = ' data-i18n="guide._section.tips" data-i18n-fb="实用技巧"'
        sec_faqs = ' data-i18n="guide._section.faqs" data-i18n-fb="常见问题"'
        head_title_attr = ' data-i18n-head="guide.%s.title" data-i18n-head-fb="%s使用指南 - ToolBox"' % (g['slug'], html.escape(g['name']))
        head_title_attr2 = ' data-i18n-head="guide.%s.title" data-i18n-head-fb="%s使用指南 - ToolBox" data-attr="content"' % (g['slug'], html.escape(g['name']))
        head_desc_attr = ' data-i18n-head="guide.%s.desc" data-i18n-head-fb="%s" data-attr="content"' % (g['slug'], html.escape(g['desc']))
    else:
        title_attr = intro_attr = nav_guides = nav_guides_fb = back_attr = ''
        sec_features = sec_scenarios = sec_steps = sec_tips = sec_faqs = ''
        head_title_attr = head_title_attr2 = head_desc_attr = ''
    page = (TPL
        .replace('{title}', html.escape(g['name']))
        .replace('{desc}', html.escape(g['desc']))
        .replace('{canonical}', canonical)
        .replace('{intro}', html.escape(g['intro']))
        .replace('{features}', li(g['features'], g['slug'], 'features', g.get('en_features')))
        .replace('{scenarios}', li(g['scenarios'], g['slug'], 'scenarios', g.get('en_scenarios')))
        .replace('{steps}', li(g['steps'], g['slug'], 'steps', g.get('en_steps')))
        .replace('{tips}', li(g['tips'], g['slug'], 'tips', g.get('en_tips')))
        .replace('{faqs}', render_faqs(g))
        .replace('{tool_url}', SITE + '/tools/%s/%s' % (g['ind'], g['base']))
        .replace('{home}', SITE + '/')
        .replace('{title_attr}', title_attr)
        .replace('{intro_attr}', intro_attr)
        .replace('{nav_guides}', nav_guides)
        .replace('{nav_guides_fb}', nav_guides_fb)
        .replace('{back_attr}', back_attr)
        .replace('{sec_features}', sec_features)
        .replace('{sec_scenarios}', sec_scenarios)
        .replace('{sec_steps}', sec_steps)
        .replace('{sec_tips}', sec_tips)
        .replace('{sec_faqs}', sec_faqs)
        .replace('{head_title_attr}', head_title_attr)
        .replace('{head_title_attr2}', head_title_attr2)
        .replace('{head_desc_attr}', head_desc_attr))
    return fn, page

def main():
    os.makedirs(GUIDES_DIR, exist_ok=True)
    guide_map = []
    for g in GUIDES:
        fn, page = render(g)
        open(os.path.join(GUIDES_DIR, fn), 'w', encoding='utf-8').write(page)
        guide_map.append({'tool': g['base'], 'guide': '../../guides/%s' % fn, 'title': g['name'] + '使用指南'})
        print('OK: guides/%s' % fn)
    export_js(GUIDE_EN_PACK)
    jf = os.path.join(ROOT, 'json', 'guides.json')
    old = json.load(open(jf, encoding='utf-8')) if os.path.exists(jf) else []
    existing = {m['tool'] for m in old}
    merged = old + [m for m in guide_map if m['tool'] not in existing]
    json.dump(merged, open(jf, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
    print('guides.json 合并完成，共 %d 条（本批 +%d）' % (len(merged), len(guide_map)))
    ip = os.path.join(GUIDES_DIR, 'index.html')
    if os.path.exists(ip):
        s = open(ip, encoding='utf-8').read()
        new_li = ''.join(
            '<li><a href="https://chenguangwu.github.io/guides/%s-guide.html">%s使用指南</a><span style="color:var(--muted);font-size:13px;"> — %s</span></li>'
            % (g['slug'], html.escape(g['name']), html.escape(g['desc'])) for g in GUIDES)
        if '</ul>' in s:
            s = s.replace('</ul>', new_li + '</ul>', 1)
            open(ip, 'w', encoding='utf-8').write(s)
            print('guides/index.html 追加 %d 条' % len(GUIDES))

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

if __name__ == '__main__':
    main()
