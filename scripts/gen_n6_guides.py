# -*- coding: utf-8 -*-
"""N6 高价值指南扩容生成器：12 篇使用指南，一次落地。
复用 scripts/gen_n3_guides.py 的范式：写指南 HTML + 合并 json/guides.json + 更新 guides/index.html。
模板用 .replace() 规避 CSS 大括号被 format 误解析。
运行：python3 scripts/gen_n6_guides.py
"""
import os, json, html, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GUIDES_DIR = os.path.join(ROOT, 'guides')
SITE = 'https://chenguangwu.github.io'

# 每篇：slug(=工具 basename 去 .html), ind, base(工具文件名), name, desc, intro,
#       features, scenarios, steps, tips, faqs[(q,a),...]
GUIDES = [
 {
  'slug': 'aes-encryptor',
  'ind': 'it',
  'base': 'aes-encryptor.html',
  'name': 'AES 加密/解密',
  'desc': 'AES 加密解密使用指南：输入明文/密文与密钥，选择 CBC/GCM 等模式进行对称加密或解密，全程本地处理不上传。',
  'intro': 'AES(高级加密标准)是应用最广的对称加密算法。本工具支持 AES-128/192/256 与常见模式(CBC/GCM/ECB)，输入文本与密钥即可加密为 Base64 密文或反向解密。所有运算在浏览器本地完成，密钥不上传。',
  'features': ['选择密钥长度 128/192/256 位', '支持 CBC/GCM/ECB 等模式', '输入文本与密钥即时加解密', '输出 Base64 密文便于复制', '本地运算不上传密钥'],
  'scenarios': ['保护配置文件中的敏感字段', '学习对称加密的工作原理', '快速验证一段密文能否用某密钥解开'],
  'steps': ['选择密钥长度与加密模式', '输入明文与密钥(或 IV)', '点击加密得到 Base64 密文', '解密时粘贴密文与密钥点解密'],
  'tips': ['GCM 模式自带完整性校验更安全，ECB 不推荐用于真实数据', 'CBC 需正确 IV，否则解密乱码', '密钥务必妥善保存，本工具不存储'],
  'faqs': [('AES 和 RSA 区别？', 'AES 是对称加密(同一密钥加解密)速度快；RSA 是非对称(公私钥)，适合密钥交换。'), ('能给个例子吗？', '明文"hello"、16 字节密钥、AES-128-CBC，加密得一段 Base64，解密还原"hello"。')],
  'en_name': 'AES Encrypt/Decrypt',
  'en_desc': 'AES Encrypt/Decrypt Guide: enter text/ciphertext with a key and pick CBC/GCM modes for symmetric encryption or decryption, all processed locally with no upload.',
  'en_intro': 'AES (Advanced Encryption Standard) is the most widely used symmetric algorithm. This tool supports AES-128/192/256 with common modes (CBC/GCM/ECB). Type text and a key to encrypt into Base64 ciphertext or decrypt back. Everything runs in your browser; the key is never uploaded.',
  'en_features': ['Pick key length 128/192/256', 'CBC/GCM/ECB modes', 'Instant encrypt/decrypt of text and key', 'Base64 ciphertext output for easy copy', 'Local, key not uploaded'],
  'en_scenarios': ['Protect sensitive fields in config files', 'Learn how symmetric encryption works', 'Quickly verify if a ciphertext opens with a given key'],
  'en_steps': ['Pick key length and mode', 'Enter plaintext and key (or IV)', 'Click encrypt for Base64 ciphertext', 'For decrypt, paste ciphertext and key, click decrypt'],
  'en_tips': ['GCM includes integrity checks and is safer; avoid ECB for real data', 'CBC needs a correct IV or decryption is garbled', 'Keep the key safe — this tool does not store it'],
  'en_faqs': [('AES vs RSA?', 'AES is symmetric (one key for both) and fast; RSA is asymmetric (public/private) and suits key exchange.'), ('Can you show an example?', 'Plaintext "hello", 16-byte key, AES-128-CBC → a Base64 string; decrypt restores "hello".')],
 },

 {
  'slug': 'base58-encode',
  'ind': 'it',
  'base': 'base58-encode.html',
  'name': 'Base58 编码/解码',
  'desc': 'Base58 编码解码使用指南：用于比特币等地址的无歧义编码，去除易混字符 0/O/l/I，纯本地转换。',
  'intro': 'Base58 是类似 Base64 但去掉了 0/O/1/l/I 等易混淆字符的编码，广泛用于比特币地址、IPFS 等。输入文本或 Base58 字符串即可互转，纯本地运算。',
  'features': ['文本↔Base58 互转', '避免 0/O/1/l/I 歧义', '支持 UTF-8 文本', '本地运算不上传'],
  'scenarios': ['理解比特币地址编码原理', '生成可读的短标识', '校验一段 Base58 是否能解码'],
  'steps': ['粘贴待编码文本', '点击编码得到 Base58', '解码时粘贴 Base58 点解码'],
  'tips': ['Base58 不含 + / 等符号，适合人工抄写', '与 Base64 不同，它更短且去歧义', '非法字符会解码失败'],
  'faqs': [('为什么比特币用 Base58？', '去掉易混字符减少转账地址抄错风险。'), ('能给个例子吗？', '"hello" 的 Base58 编码为 "Cn8eVZg"，解码还原 "hello"。')],
  'en_name': 'Base58 Encode/Decode',
  'en_desc': 'Base58 Encode/Decode Guide: ambiguity-free encoding for Bitcoin-style addresses, dropping easily-confused chars 0/O/l/I, pure local conversion.',
  'en_intro': 'Base58 is like Base64 but removes easily-confused characters 0/O/1/l/I. It is widely used in Bitcoin addresses and IPFS. Paste text or Base58 to convert both ways, fully locally.',
  'en_features': ['Text to Base58 both ways', 'Avoids 0/O/1/l/I confusion', 'UTF-8 text support', 'Local processing'],
  'en_scenarios': ['Understand Bitcoin address encoding', 'Generate readable short identifiers', 'Validate whether a Base58 string decodes'],
  'en_steps': ['Paste the text to encode', 'Click encode for Base58', 'For decode, paste Base58 and click decode'],
  'en_tips': ['Base58 has no + / symbols, friendly for manual copying', 'Unlike Base64, it is shorter and ambiguity-free', 'Illegal characters cause decode failure'],
  'en_faqs': [('Why does Bitcoin use Base58?', 'Removing confusing chars reduces the risk of mis-copied addresses.'), ('Can you show an example?', '"hello" in Base58 is "Cn8eVZg"; decode restores "hello".')],
 },

 {
  'slug': 'json-diff',
  'ind': 'it',
  'base': 'json-diff.html',
  'name': 'JSON 差异对比',
  'desc': 'JSON 差异对比使用指南：粘贴两份 JSON，高亮新增/删除/变更的字段与值，支持数组对齐。',
  'intro': '逐字段比较两份 JSON，标出结构差异与值变更，适合核对接口返回、配置文件改动。纯前端，数据不上传。',
  'features': ['键级差异高亮', '值变更单独标注', '数组按顺序对齐', '折叠展开大对象', '本地比对不上传'],
  'scenarios': ['核对前后两次接口响应', '比较配置文件版本差异', '排查数据字段缺失'],
  'steps': ['左框贴原始 JSON、右框贴新 JSON', '点击对比', '查看高亮的增删改字段'],
  'tips': ['数组默认按位置对齐，顺序不同会显差异', '格式化后再对比更易读', '敏感数据本地处理更安全'],
  'faqs': [('数组顺序变了算差异吗？', '默认按序对齐，顺序不同会标红，可先排序再比。'), ('能给个例子吗？', 'A={"a":1}, B={"a":2}，对比显示字段 a 值由 1 变为 2。')],
  'en_name': 'JSON Diff',
  'en_desc': 'JSON Diff Guide: paste two JSON blobs and highlight added/removed/changed fields and values, with array alignment.',
  'en_intro': 'Compare two JSON documents field by field, marking structural differences and value changes — ideal for checking API responses or config changes. Pure front-end, data not uploaded.',
  'en_features': ['Key-level diff highlighting', 'Value-change callouts', 'Array alignment by position', 'Collapse/expand large objects', 'Local comparison'],
  'en_scenarios': ['Check before/after API responses', 'Compare config file versions', 'Spot missing data fields'],
  'en_steps': ['Paste original JSON left, new JSON right', 'Click compare', 'Review highlighted adds/removes/changes'],
  'en_tips': ['Arrays align by position by default; different order shows as diff', 'Format first for easier reading', 'Local handling is safer for sensitive data'],
  'en_faqs': [('Does array order change count as a diff?', 'By default yes (position-aligned); sort first if order should not matter.'), ('Can you show an example?', 'A={"a":1}, B={"a":2} → field a changed from 1 to 2.')],
 },

 {
  'slug': 'csv-to-json',
  'ind': 'it',
  'base': 'csv-to-json.html',
  'name': 'CSV 转 JSON',
  'desc': 'CSV 转 JSON 使用指南：上传或粘贴 CSV，按首行表头转成 JSON 数组，支持分隔符与引号配置。',
  'intro': '将表格型 CSV 转换为程序易处理的 JSON 数组，每行成为对象、表头为键。支持自定义分隔符与引号，本地转换不上传。',
  'features': ['CSV→JSON 数组转换', '首行作为键名', '自定义分隔符(逗号/制表符)', '支持引号包裹字段', '预览与下载'],
  'scenarios': ['表格数据接入前端接口', 'Excel 导出后转 JSON', '批量数据处理前置'],
  'steps': ['粘贴或上传 CSV', '确认分隔符与表头行', '点击转换查看 JSON', '下载结果'],
  'tips': ['含逗号的字段需用引号包裹', '表头有重复键会覆盖', '大文件建议先抽样'],
  'faqs': [('表头中文能用吗？', '可以，键名即为表头文本，程序侧按中文键读取。'), ('能给个例子吗？', 'CSV "name,age\\nTom,3" → [{"name":"Tom","age":"3"}]。')],
  'en_name': 'CSV to JSON',
  'en_desc': 'CSV to JSON Guide: upload or paste CSV and turn it into a JSON array using the header row as keys, with delimiter and quote options.',
  'en_intro': 'Turn tabular CSV into a JSON array that programs consume easily: each row becomes an object, the header becomes keys. Custom delimiter and quotes supported, locally.',
  'en_features': ['CSV to JSON array', 'Header row as keys', 'Custom delimiter (comma/tab)', 'Quote-wrapped field support', 'Preview and download'],
  'en_scenarios': ['Feed tabular data into a front-end API', 'Convert after Excel export', 'Preprocess for batch data'],
  'en_steps': ['Paste or upload CSV', 'Confirm delimiter and header row', 'Click convert to view JSON', 'Download the result'],
  'en_tips': ['Fields with commas need quote wrapping', 'Duplicate header keys overwrite', 'Sample large files first'],
  'en_faqs': [('Can the header be Chinese?', 'Yes — the key name is the header text; the program reads by that Chinese key.'), ('Can you show an example?', 'CSV "name,age\\nTom,3" → [{"name":"Tom","age":"3"}].')],
 },

 {
  'slug': 'json-to-yaml',
  'ind': 'it',
  'base': 'json-to-yaml.html',
  'name': 'JSON 转 YAML',
  'desc': 'JSON 转 YAML 使用指南：将 JSON 转为可读性更高的 YAML，常用于配置文件与 Kubernetes 清单。',
  'intro': 'YAML 是 JSON 的超集，用缩进表达层级、更适合人读。输入 JSON 即得等价的 YAML，本地转换不上传。',
  'features': ['JSON→YAML 转换', '保持层级与类型', '支持缩进配置', '可双向校验', '本地处理'],
  'scenarios': ['写 Kubernetes / Docker Compose 配置', '把接口 JSON 转可读文档', '配置文件格式迁移'],
  'steps': ['粘贴 JSON', '点击转换查看 YAML', '复制或下载'],
  'tips': ['YAML 用缩进表示层级，别用 Tab', '字符串含特殊字符会加引号', 'YAML 是 JSON 超集，可转换回去'],
  'faqs': [('YAML 和 JSON 能互转吗？', '能，YAML 是 JSON 超集，本工具专注 JSON→YAML。'), ('能给个例子吗？', '{"a":1,"b":[2,3]} → "a: 1\\nb:\\n  - 2\\n  - 3"。')],
  'en_name': 'JSON to YAML',
  'en_desc': 'JSON to YAML Guide: convert JSON to the more readable YAML, common for config files and Kubernetes manifests.',
  'en_intro': 'YAML is a superset of JSON that uses indentation for hierarchy and reads better for humans. Input JSON to get equivalent YAML, locally.',
  'en_features': ['JSON to YAML conversion', 'Preserve hierarchy and types', 'Indentation options', 'Bidirectional check', 'Local processing'],
  'en_scenarios': ['Write Kubernetes / Docker Compose config', 'Turn API JSON into readable docs', 'Config format migration'],
  'en_steps': ['Paste JSON', 'Click convert to view YAML', 'Copy or download'],
  'en_tips': ['YAML uses indentation, not tabs', 'Strings with special chars get quoted', 'YAML is a superset of JSON, convertible back'],
  'en_faqs': [('Can JSON and YAML convert both ways?', 'Yes — YAML is a superset of JSON.'), ('Can you show an example?', '{"a":1,"b":[2,3]} → "a: 1\\nb:\\n  - 2\\n  - 3".')],
 },

 {
  'slug': 'http-status',
  'ind': 'it',
  'base': 'http-status.html',
  'name': 'HTTP 状态码查询',
  'desc': 'HTTP 状态码查询使用指南：输入或浏览 1xx–5xx 状态码，查看含义、类别与常见触发场景。',
  'intro': 'HTTP 状态码标识请求结果：2xx 成功、3xx 重定向、4xx 客户端错误、5xx 服务端错误。输入码号即查含义与排查方向，开发调试常备。',
  'features': ['1xx–5xx 全类查询', '显示类别与含义', '附常见触发原因', '搜索/浏览定位', '本地速查'],
  'scenarios': ['接口返回 4xx/5xx 快速定位', '写文档标注状态码含义', '面试/教学速查'],
  'steps': ['输入状态码如 404', '查看类别与说明', '按需浏览同类码'],
  'tips': ['4xx 多为请求问题(路径/权限)，5xx 多为服务端 bug', '301/302 是重定向，307/308 更严格', '401 未认证、403 无权限'],
  'faqs': [('404 和 410 区别？', '404 资源未找到(可能临时)，410 明确表示已永久删除。'), ('能给个例子吗？', '输入 429 显示"请求过多"，提示限流需退避重试。')],
  'en_name': 'HTTP Status Code Lookup',
  'en_desc': 'HTTP Status Code Lookup Guide: enter or browse 1xx–5xx codes to see meaning, class and common triggers.',
  'en_intro': 'HTTP status codes mark request outcomes: 2xx success, 3xx redirect, 4xx client error, 5xx server error. Enter a code to see meaning and debugging direction — a dev essential.',
  'en_features': ['Lookup across 1xx–5xx', 'Show class and meaning', 'Common trigger reasons', 'Search/browse locating', 'Local lookup'],
  'en_scenarios': ['Quickly locate a 4xx/5xx from an API', 'Annotate status meaning in docs', 'Interview/teaching reference'],
  'en_steps': ['Enter a status like 404', 'View class and explanation', 'Browse similar codes as needed'],
  'en_tips': ['4xx usually means a request issue (path/permission); 5xx means a server bug', '301/302 redirect, 307/308 stricter', '401 unauthorized, 403 forbidden'],
  'en_faqs': [('404 vs 410?', '404 means not found (maybe temporary); 410 means permanently deleted.'), ('Can you show an example?', 'Input 429 → "Too Many Requests", suggesting throttling and retry with backoff.')],
 },

 {
  'slug': 'emoji-meaning',
  'ind': 'it',
  'base': 'emoji-meaning.html',
  'name': 'Emoji 含义查询',
  'desc': 'Emoji 含义查询使用指南：输入或搜索 Emoji，查看名称、含义与跨平台显示说明。',
  'intro': '每个 Emoji 有 Unicode 名称与语义。本工具按字符或关键词查其官方名称、含义与使用场景，帮助准确表达。',
  'features': ['Emoji→名称/含义', '关键词搜索', '显示 Unicode 码点', '跨平台说明', '本地查询'],
  'scenarios': ['确认某个表情的真实含义', '写文案选合适 Emoji', '教学/翻译参考'],
  'steps': ['输入或粘贴 Emoji', '查看名称与含义', '用关键词搜索同类'],
  'tips': ['同码点在不同平台绘像不同', '组合 ZWJ 序列会显示新表情', '含义随语境变化，注意歧义'],
  'faqs': [('为什么同一表情各平台不一样？', '各系统自带绘像字体，形状不同但语义一致。'), ('能给个例子吗？', '🔥 官方名 "Fire"，常表"热度/火爆/上头"。')],
  'en_name': 'Emoji Meaning Lookup',
  'en_desc': 'Emoji Meaning Lookup Guide: enter or search an Emoji to see its name, meaning and cross-platform notes.',
  'en_intro': 'Each Emoji has a Unicode name and semantics. This tool looks up the official name and meaning by character or keyword to help you express accurately.',
  'en_features': ['Emoji to name/meaning', 'Keyword search', 'Show Unicode code point', 'Cross-platform notes', 'Local lookup'],
  'en_scenarios': ['Confirm the real meaning of an emoji', 'Pick the right emoji for copy', 'Teaching/translation reference'],
  'en_steps': ['Enter or paste an Emoji', 'View name and meaning', 'Search similar by keyword'],
  'en_tips': ['Same code point renders differently per platform', 'ZWJ sequences form new emoji', 'Meaning varies by context, watch ambiguity'],
  'en_faqs': [('Why does the same emoji look different?', 'Each system ships its own font; shape differs but semantics match.'), ('Can you show an example?', '🔥 official name "Fire", often means "hot/trending/obsessed".')],
 },

 {
  'slug': 'morse',
  'ind': 'it',
  'base': 'morse.html',
  'name': '摩斯密码转换',
  'desc': '摩斯密码转换使用指南：文本与摩斯码互转，支持字母数字与常用符号，附分词规则说明。',
  'intro': '摩斯电码用点划表示字符。输入文本即得摩斯串，或反向解码；支持空格分词。纯本地运算。',
  'features': ['文本↔摩斯互转', '支持中英字符与数字', '空格/斜杠分词', '可听化提示', '本地运算'],
  'scenarios': ['业余无线电学习', '趣味加密留言', '教学演示编码'],
  'steps': ['输入文本', '点击编码看摩斯串', '解码时粘贴摩斯点划'],
  'tips': ['字母间空格、单词间斜杠分隔', '中文需先转拼音或对应码', '长短音比例 1:3'],
  'faqs': [('摩斯怎么分词？', '单词间用斜杠(/)或长空格分隔。'), ('能给个例子吗？', '"SOS" → "... --- ..."。')],
  'en_name': 'Morse Code Converter',
  'en_desc': 'Morse Code Converter Guide: convert text and Morse both ways, with letter/digit/symbol rules.',
  'en_intro': 'Morse code represents characters with dots and dashes. Type text to get the Morse string, or decode back; supports spaces between words. Pure local.',
  'en_features': ['Text to Morse both ways', 'Letters, digits and common symbols', 'Space/slash word separation', 'Audible hint', 'Local computation'],
  'en_scenarios': ['Amateur radio learning', 'Fun encrypted messages', 'Teaching demo of encoding'],
  'en_steps': ['Enter text', 'Click encode to see Morse', 'For decode, paste dots/dashes'],
  'en_tips': ['Space between letters, slash between words', 'Chinese needs romanization or its own code first', 'Dot/dash ratio 1:3'],
  'en_faqs': [('How to separate words in Morse?', 'Use a slash (/) or long space between words.'), ('Can you show an example?', '"SOS" → "... --- ...".')],
 },

 {
  'slug': 'curl-parser',
  'ind': 'it',
  'base': 'curl-parser.html',
  'name': 'curl 命令解析',
  'desc': 'curl 命令解析使用指南：粘贴 curl 命令，拆解方法、URL、请求头与请求体，便于调试与转换。',
  'intro': '从一段 curl 命令中提取 HTTP 方法、URL、Header、Body 与参数，帮助复制到代码或 Postman。本地解析不上传。',
  'features': ['拆解方法/URL/Header/Body', '识别 -X -H -d 等参数', '格式化展示', '一键复制各部分', '本地处理'],
  'scenarios': ['把浏览器复制的 curl 转代码', '核对请求头与体是否正确', '分享接口调用给他人'],
  'steps': ['粘贴 curl 命令', '点击解析', '查看结构化字段并复制'],
  'tips': ['从浏览器网络面板"Copy as cURL"最常用', '-d 后为请求体，-H 为请求头', 'Bearer 令牌在 Header 里'],
  'faqs': [('怎么拿到 curl？', '浏览器 DevTools 网络面板右键请求选 Copy as cURL。'), ('能给个例子吗？', 'curl -X POST -H "Authorization: Bearer x" -d "{}" https://api → 拆出 POST 方法、Header、空 Body 与 URL。')],
  'en_name': 'curl Command Parser',
  'en_desc': 'curl Command Parser Guide: break a curl command into method, URL, headers and body for debugging or conversion.',
  'en_intro': 'Extract HTTP method, URL, Header and Body from a curl command to copy into code or Postman. Local parsing, not uploaded.',
  'en_features': ['Extract method/URL/Header/Body', 'Recognize -X -H -d flags', 'Formatted display', 'One-click copy of parts', 'Local processing'],
  'en_scenarios': ['Turn a browser-copied curl into code', 'Verify headers and body are correct', 'Share an API call with others'],
  'en_steps': ['Paste the curl command', 'Click parse', 'View structured fields and copy'],
  'en_tips': ['"Copy as cURL" from the browser network panel is most common', '-d is the body, -H is the header', 'Bearer token sits in the Header'],
  'en_faqs': [('How do I get a curl?', 'In DevTools network panel, right-click a request and choose Copy as cURL.'), ('Can you show an example?', 'curl -X POST -H "Authorization: Bearer x" -d "{}" https://api → method POST, Header, empty Body, URL.')],
 },

 {
  'slug': 'nanoid-generator',
  'ind': 'it',
  'base': 'nanoid-generator.html',
  'name': 'NanoID 生成器',
  'desc': 'NanoID 生成器使用指南：生成安全随机、URL 友好的短 ID，可定制长度与字符集。',
  'intro': 'NanoID 是比 UUID 更短、更 URL 安全的随机 ID，默认 21 字符、使用 A-Za-z0-9_- 等。可设长度与自定义字母表，本地生成。',
  'features': ['生成 URL 友好随机 ID', '可调长度与字符集', '批量生成多个', '基于加密随机', '本地运算'],
  'scenarios': ['给数据库记录生成主键', '短链接/邀请码', '前端临时标识'],
  'steps': ['设长度与字符集', '点生成得单条或多条', '复制使用'],
  'tips': ['默认 21 字符碰撞概率极低', '避免用易混字符可自定义字母表', '比 UUID 更短更适合 URL'],
  'faqs': [('NanoID 和 UUID 区别？', 'NanoID 更短更 URL 安全，UUID 是固定 36 字符标准格式。'), ('能给个例子吗？', '默认生成如 "V1StGXR8Zq5l6pXx" 的 21 位 ID。')],
  'en_name': 'NanoID Generator',
  'en_desc': 'NanoID Generator Guide: generate secure, random, URL-friendly short IDs with customizable length and alphabet.',
  'en_intro': 'NanoID is a shorter, more URL-safe random ID than UUID — default 21 chars using A-Za-z0-9_-. Set length and custom alphabet, generated locally.',
  'en_features': ['Generate URL-friendly random IDs', 'Adjustable length and alphabet', 'Batch generation', 'Crypto-random based', 'Local computation'],
  'en_scenarios': ['Primary keys for database records', 'Short links / invite codes', 'Front-end temporary identifiers'],
  'en_steps': ['Set length and alphabet', 'Click generate for one or many', 'Copy and use'],
  'en_tips': ['Default 21 chars have negligibly low collision probability', 'Avoid confusing chars with a custom alphabet', 'Shorter and more URL-safe than UUID'],
  'en_faqs': [('NanoID vs UUID?', 'NanoID is shorter and more URL-safe; UUID is a fixed 36-char standard.'), ('Can you show an example?', 'A default ID looks like "V1StGXR8Zq5l6pXx" (21 chars).')],
 },

 {
  'slug': 'box-shadow-generator',
  'ind': 'it',
  'base': 'box-shadow-generator.html',
  'name': 'CSS 盒阴影生成器',
  'desc': 'CSS 盒阴影生成器使用指南：可视化调出 box-shadow 参数，实时预览并复制 CSS 代码。',
  'intro': 'box-shadow 用偏移、模糊、扩散与颜色定义元素投影。拖拽调节各参数，实时看效果并复制生成的 CSS，前端必备。',
  'features': ['偏移 X/Y/模糊/扩散滑杆', '颜色与透明度选择', '内阴影 inset 开关', '实时预览', '一键复制 CSS'],
  'scenarios': ['卡片悬浮投影设计', '按钮立体感', '分隔层次'],
  'steps': ['调节 X/Y 偏移与模糊', '选阴影颜色', '开 inset 做内阴影', '复制 CSS 到项目'],
  'tips': ['X/Y 同 0、模糊大→柔和弥散阴影', 'inset 做内凹效果', '避免过度投影显脏'],
  'faqs': [('inset 是什么？', '加 inset 阴影变为元素内部，营造内凹。'), ('能给个例子吗？', 'box-shadow: 0 4px 12px rgba(0,0,0,.15) 是常见卡片投影。')],
  'en_name': 'CSS Box Shadow Generator',
  'en_desc': 'CSS Box Shadow Generator Guide: visually tune box-shadow params with live preview and copyable CSS.',
  'en_intro': 'box-shadow defines an element shadow with offset, blur, spread and color. Drag the controls to tune, see it live, and copy the CSS — a front-end must-have.',
  'en_features': ['Offset X/Y/blur/spread sliders', 'Color and opacity picker', 'Inset shadow toggle', 'Live preview', 'One-click copy CSS'],
  'en_scenarios': ['Card hover shadow design', 'Button depth', 'Separate visual layers'],
  'en_steps': ['Adjust X/Y offset and blur', 'Pick shadow color', 'Toggle inset for inner shadow', 'Copy CSS into your project'],
  'en_tips': ['X/Y 0 with large blur → soft diffuse shadow', 'inset makes an inner recess', 'Avoid heavy shadows that look dirty'],
  'en_faqs': [('What is inset?', 'Adding inset moves the shadow inside the element for a recessed look.'), ('Can you show an example?', 'box-shadow: 0 4px 12px rgba(0,0,0,.15) is a common card shadow.')],
 },

 {
  'slug': 'color-contrast-check',
  'ind': 'design',
  'base': 'color-contrast-check.html',
  'name': '颜色对比度检查',
  'desc': '颜色对比度检查使用指南：输入前景色与背景色，按 WCAG 计算对比度比值与无障碍达标等级。',
  'intro': 'WCAG 要求正文对比度至少 4.5:1、大字 3:1。输入两色即算对比度并提示是否达标 AA/AAA，设计无障碍必备。',
  'features': ['前景/背景色对比度计算', '输出 WCAG 等级(AA/AAA)', '支持普通文本与大文本阈值', '实时预览', '本地计算'],
  'scenarios': ['检查网页文字可读性', '设计无障碍合规', '选配色避免低对比'],
  'steps': ['输入前景色与背景色(HEX/RGB)', '查看对比度比值', '核对 AA/AAA 是否通过'],
  'tips': ['比值 ≥4.5 过 AA 正文、≥7 过 AAA', '大文本(≥18px 或 14px 粗)只需 3:1', '对比度低可用更深的文字色'],
  'faqs': [('AA 和 AAA 区别？', 'AAA 更严(7:1)，AA 是最低合规线(4.5:1)。'), ('能给个例子吗？', '黑字(#000)白底(#fff)对比度 21:1，远超 AAA。')],
  'en_name': 'Color Contrast Checker',
  'en_desc': 'Color Contrast Checker Guide: input foreground and background colors to compute the WCAG contrast ratio and accessibility level.',
  'en_intro': 'WCAG requires at least 4.5:1 for body text and 3:1 for large text. Enter two colors to compute contrast and see if AA/AAA pass — essential for accessible design.',
  'en_features': ['Foreground/background contrast', 'Output WCAG level (AA/AAA)', 'Normal vs large text thresholds', 'Live preview', 'Local computation'],
  'en_scenarios': ['Check web text readability', 'Design accessibility compliance', 'Pick colors avoiding low contrast'],
  'en_steps': ['Enter foreground and background (HEX/RGB)', 'View the contrast ratio', 'Check AA/AAA pass'],
  'en_tips': ['Ratio ≥4.5 passes AA body, ≥7 passes AAA', 'Large text (≥18px or 14px bold) only needs 3:1', 'Low contrast? use a darker text color'],
  'en_faqs': [('AA vs AAA?', 'AAA is stricter (7:1); AA is the minimum compliance line (4.5:1).'), ('Can you show an example?', 'Black text (#000) on white (#fff) is 21:1, far above AAA.')],
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
<script type="application/ld+json">
{"@context":"https://schema.org","@type":"Article","headline":"{title}使用指南","description":"{desc}","author":{"@type":"Organization","name":"ToolBox"}}
</script>
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
    # 合并 guides.json（按 tool 去重）
    jf = os.path.join(ROOT, 'json', 'guides.json')
    old = json.load(open(jf, encoding='utf-8')) if os.path.exists(jf) else []
    existing = {m['tool'] for m in old}
    merged = old + [m for m in guide_map if m['tool'] not in existing]
    json.dump(merged, open(jf, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
    print('guides.json 合并完成，共 %d 条（本批 +%d）' % (len(merged), len(guide_map)))
    # 指南中心 index.html 追加条目
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
