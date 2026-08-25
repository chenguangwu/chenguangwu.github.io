# -*- coding: utf-8 -*-
"""N8 高价值指南扩容生成器（第二期）：18 篇使用指南，一次落地。
复用 scripts/gen_n6_guides.py 的范式：写指南 HTML + 合并 json/guides.json + 更新 guides/index.html。
模板用 .replace() 规避 CSS 大括号被 format 误解析。
运行：python3 scripts/gen_n8_guides.py

本批聚焦 it-tools 核心对标、确定存在且 Q5 未覆盖的高频开发/设计工具：
uuid-generator, slugify, xml-formatter, xml-to-json, json-to-toml, toml-to-json,
yaml-to-json, json-to-xml, hmac-generator, sql-formatter, base85-encode, bip39-generator,
user-agent-parser, password-strength, number-base-converter, basic-auth-generator,
api-sign-generator, bitwise-calculator
"""
import os, json, html, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GUIDES_DIR = os.path.join(ROOT, 'guides')
SITE = 'https://chenguangwu.github.io'

# 每篇：slug(=工具 basename 去 .html), ind, base(工具文件名), name, desc, intro,
#       features, scenarios, steps, tips, faqs[(q,a),...]
GUIDES = [
 {
  'slug': 'uuid-generator',
  'ind': 'it',
  'base': 'uuid-generator.html',
  'name': 'UUID 生成器',
  'desc': 'UUID 生成器使用指南：生成 v1/v4/v5 版本的全局唯一标识符，支持批量与命名空间，纯本地随机生成。',
  'intro': 'UUID(通用唯一识别码)是 128 位标识符，v4 基于随机数最常用，v5 基于命名空间哈希可复现。本工具可选版本、批量生成，用于数据库主键、追踪 ID 等。本地生成不上传。',
  'features': ['生成 v1/v4/v5 版本', '批量生成多条', 'v5 支持命名空间+名称', '大写/去横线格式切换', '本地随机运算'],
  'scenarios': ['数据库主键或记录 ID', '分布式系统去重标识', '日志追踪 correlation id'],
  'steps': ['选择版本(常用 v4)', '设数量与格式', '点击生成', '复制使用'],
  'tips': ['v4 随机碰撞概率极低，无需中心化分配', 'v5 同名同名空间输出稳定，适合可复现 ID', '去掉横线更紧凑'],
  'faqs': [('v4 和 v5 怎么选？', '要随机唯一用 v4；要按"名称"稳定复现用 v5。'), ('能给个例子吗？', 'v4 形如 "f47ac10b-58cc-4372-a567-0e02b2c3d479"，每次不同。')],
  'en_name': 'UUID Generator',
  'en_desc': 'UUID Generator Guide: create v1/v4/v5 universally unique identifiers, with batch generation and namespace support. All randomness runs locally in your browser.',
  'en_intro': 'A UUID (Universally Unique Identifier) is a 128-bit identifier. v4, the most common variant, is random-based; v5 is namespace-hash based and reproducible. This tool lets you pick a version, generate in bulk, and use the IDs as database primary keys or tracking IDs. Generation is local and nothing is uploaded.',
  'en_features': ['Generate v1 / v4 / v5 versions', 'Create multiple IDs in bulk', 'v5 supports namespace + name', 'Toggle uppercase / hyphen-free format', 'Local random generation'],
  'en_scenarios': ['Database primary keys or record IDs', 'Deduplication IDs in distributed systems', 'Correlation IDs for log tracing'],
  'en_steps': ['Choose a version (v4 by default)', 'Set the count and format', 'Click generate', 'Copy and use'],
  'en_tips': ['v4 collisions are astronomically unlikely, no central authority needed', 'v5 yields the same ID for the same name+namespace — great for reproducible IDs', 'Hyphen-free form is more compact'],
  'en_faqs': [('v4 or v5?', 'Use v4 for random uniqueness; use v5 when you need a stable ID derived from a name.'), ('Can you show an example?', 'A v4 looks like "f47ac10b-58cc-4372-a567-0e02b2c3d479" and differs every time.')],
 },

 {
  'slug': 'slugify',
  'ind': 'it',
  'base': 'slugify.html',
  'name': 'URL Slug 生成器',
  'desc': 'URL Slug 生成器 使用指南：把中文/空格/特殊字符标题转成 SEO 友好的 URL 片段，支持多语言与分隔符。',
  'intro': 'Slug 是 URL 中可读的路径段，如 "how-to-use-toolbox"。本工具把标题转小写、去标点、空格换连字符，并尽量保留语义，利于 SEO 与分享。本地转换。',
  'features': ['标题→slug 转换', '空格/下划线转连字符', '去除或保留停用词', '支持中文转拼音', '本地处理'],
  'scenarios': ['博客/文章 URL 生成', '商品页友好链接', '批量处理标题'],
  'steps': ['粘贴标题文本', '选分隔符与语言策略', '点击生成', '复制 slug'],
  'tips': ['slug 短而含关键词更利 SEO', '避免连续连字符', '中文建议转拼音或保留英文关键词'],
  'faqs': [('slug 为什么重要？', '清晰 slug 提升可读性与搜索点击率。'), ('能给个例子吗？', '"Hello World! 2026" → "hello-world-2026"。')],
  'en_name': 'URL Slug Generator',
  'en_desc': 'URL Slug Generator Guide: turn Chinese/spaces/special-character titles into SEO-friendly URL segments, with multi-language and delimiter support.',
  'en_intro': 'A slug is the human-readable path segment in a URL, e.g. "how-to-use-toolbox". This tool lowercases the title, strips punctuation, swaps spaces for hyphens, and preserves meaning as much as possible — great for SEO and sharing. Conversion runs locally.',
  'en_features': ['Title to slug conversion', 'Spaces/underscores to hyphens', 'Keep or drop stop words', 'Chinese to pinyin support', 'Local processing'],
  'en_scenarios': ['Blog/article URL generation', 'Friendly product-page links', 'Batch-processing titles'],
  'en_steps': ['Paste the title text', 'Pick delimiter and language policy', 'Click generate', 'Copy the slug'],
  'en_tips': ['Short slugs with keywords help SEO', 'Avoid consecutive hyphens', 'For Chinese, use pinyin or keep English keywords'],
  'en_faqs': [('Why does the slug matter?', 'A clear slug improves readability and search click-through.'), ('Can you show an example?', '"Hello World! 2026" → "hello-world-2026".')],
 },

 {
  'slug': 'xml-formatter',
  'ind': 'it',
  'base': 'xml-formatter.html',
  'name': 'XML 格式化',
  'desc': 'XML 格式化使用指南：粘贴杂乱 XML，一键缩进美化并校验结构，支持属性与 CDATA 处理。',
  'intro': 'XML 常用于配置与数据交换。本工具对缩进混乱的 XML 重新排版、高亮层级，并可检测标签是否闭合。纯前端，数据不上传。',
  'features': ['缩进美化 XML', '标签闭合校验', '折叠展开节点', '支持大文件分段', '本地处理'],
  'scenarios': ['查看接口返回的 XML', '整理配置文件', '排查标签缺失'],
  'steps': ['粘贴 XML', '点击格式化', '查看缩进结果或错误提示'],
  'tips': ['属性与子元素混排时注意层级', 'CDATA 内文本不被解析', '错误会标出大致行号'],
  'faqs': [('和 JSON 比 XML 还常用吗？', '旧系统/SOAP 仍大量用 XML，新接口多 JSON。'), ('能给个例子吗？', '"<a><b>1</b></a>" 格式化为带缩进的多行结构。')],
  'en_name': 'XML Formatter',
  'en_desc': 'XML Formatter Guide: paste messy XML and pretty-print it with one click, validating structure and handling attributes and CDATA.',
  'en_intro': 'XML is widely used for config and data exchange. This tool re-indents messy XML, highlights nesting, and detects unclosed tags. Pure front-end, nothing uploaded.',
  'en_features': ['Pretty-print XML with indentation', 'Tag-closing validation', 'Collapse/expand nodes', 'Large-file chunking', 'Local processing'],
  'en_scenarios': ['Inspect XML returned by an API', 'Tidy up config files', 'Find missing tags'],
  'en_steps': ['Paste the XML', 'Click format', 'View the indented result or error hint'],
  'en_tips': ['Mind hierarchy when attributes and children mix', 'Text inside CDATA is not parsed', 'Errors point to an approximate line number'],
  'en_faqs': [('Is XML still common vs JSON?', 'Legacy systems / SOAP still use a lot of XML; new APIs mostly use JSON.'), ('Can you show an example?', '"<a><b>1</b></a>" becomes a multi-line indented structure.')],
 },

 {
  'slug': 'xml-to-json',
  'ind': 'it',
  'base': 'xml-to-json.html',
  'name': 'XML 转 JSON',
  'desc': 'XML 转 JSON 使用指南：把 XML 文档转为等价的 JSON 结构，处理属性、数组与文本节点。',
  'intro': '将 XML 映射为 JSON：标签为键、属性前缀化、重复标签转数组。便于前端用 JS 直接消费。本地转换不上传。',
  'features': ['XML→JSON 映射', '属性转 @ 前缀键', '重复兄弟标签转数组', '文本节点抽取', '本地处理'],
  'scenarios': ['旧接口 XML 接入前端', '配置 XML 转可读对象', '数据格式迁移'],
  'steps': ['粘贴 XML', '点击转换', '查看 JSON 并复制'],
  'tips': ['属性默认加 @ 前缀避免与子节点冲突', '无子节点无属性的标签直接变字符串', '同名多子节点自动成数组'],
  'faqs': [('属性怎么表示？', '通常加 "@" 前缀，如 <a id="1"> → {"a":{"@id":"1"}}。'), ('能给个例子吗？', '"<a><b>1</b><b>2</b></a>" → {"a":{"b":["1","2"]}}。')],
  'en_name': 'XML to JSON',
  'en_desc': 'XML to JSON Guide: convert an XML document into an equivalent JSON structure, handling attributes, arrays and text nodes.',
  'en_intro': 'Maps XML to JSON: tags become keys, attributes get a prefix, repeated tags become arrays. Easy for the front-end to consume directly with JS. Local conversion, nothing uploaded.',
  'en_features': ['XML to JSON mapping', 'Attributes to @-prefixed keys', 'Repeated sibling tags to arrays', 'Text node extraction', 'Local processing'],
  'en_scenarios': ['Feed legacy XML into the front-end', 'Convert config XML to a readable object', 'Data format migration'],
  'en_steps': ['Paste the XML', 'Click convert', 'View and copy the JSON'],
  'en_tips': ['Attributes get a default @ prefix to avoid clashing with child nodes', 'A tag with no children/attributes becomes a plain string', 'Multiple same-name children auto-become an array'],
  'en_faqs': [('How are attributes represented?', 'Usually with a "@" prefix, e.g. <a id="1"> → {"a":{"@id":"1"}}.'), ('Can you show an example?', '"<a><b>1</b><b>2</b></a>" → {"a":{"b":["1","2"]}} .')],
 },

 {
  'slug': 'json-to-toml',
  'ind': 'it',
  'base': 'json-to-toml.html',
  'name': 'JSON 转 TOML',
  'desc': 'JSON 转 TOML 使用指南：把 JSON 对象转为 TOML 配置文件格式，保留嵌套与类型。',
  'intro': 'TOML 是易读的配置文件格式（Rust/Cargo、Python pyproject 用）。本工具将 JSON 转成等效 TOML，保持层级与类型。本地转换。',
  'features': ['JSON→TOML 转换', '嵌套表与数组表达', '类型保真(数字/布尔/字符串)', '本地处理'],
  'scenarios': ['写 Cargo.toml / pyproject 片段', '配置格式迁移', '人读化 JSON 配置'],
  'steps': ['粘贴 JSON', '点击转换', '复制 TOML'],
  'tips': ['TOML 表用 [section] 表达嵌套', '数组用双方括号 [[ ]]', '键含特殊字符需加引号'],
  'faqs': [('TOML 和 YAML 选谁？', 'TOML 更贴近 ini、类型明确；YAML 更紧凑但缩进敏感。'), ('能给个例子吗？', '{"a":{"b":1}} → "[a]\nb = 1"。')],
  'en_name': 'JSON to TOML',
  'en_desc': 'JSON to TOML Guide: convert a JSON object into TOML config format, preserving nesting and types.',
  'en_intro': 'TOML is a readable config format (used by Rust/Cargo, Python pyproject). This tool turns JSON into equivalent TOML, keeping hierarchy and types. Local conversion.',
  'en_features': ['JSON to TOML conversion', 'Nested tables and arrays', 'Type fidelity (number/bool/string)', 'Local processing'],
  'en_scenarios': ['Write Cargo.toml / pyproject snippets', 'Config format migration', 'Human-readable JSON config'],
  'en_steps': ['Paste the JSON', 'Click convert', 'Copy the TOML'],
  'en_tips': ['TOML tables use [section] for nesting', 'Arrays use double brackets [[ ]]', 'Keys with special chars need quotes'],
  'en_faqs': [('TOML or YAML?', 'TOML is closer to ini with explicit types; YAML is more compact but indentation-sensitive.'), ('Can you show an example?', '{"a":{"b":1}} → "[a]\\n b = 1".')],
 },

 {
  'slug': 'toml-to-json',
  'ind': 'it',
  'base': 'toml-to-json.html',
  'name': 'TOML 转 JSON',
  'desc': 'TOML 转 JSON 使用指南：把 TOML 配置解析为 JSON，便于程序消费与校验。',
  'intro': '将 TOML 片段解析为 JSON 对象，支持嵌套表、数组与标准类型。适合把配置文件喂给 JS/接口。本地解析。',
  'features': ['TOML→JSON 解析', '嵌套表展开', '数组与类型还原', '错误定位', '本地处理'],
  'scenarios': ['读 Cargo.toml 配置', '配置文件校验', 'TOML→接口数据'],
  'steps': ['粘贴 TOML', '点击解析', '查看 JSON'],
  'tips': ['表顺序在 JSON 中会被打乱(对象无序)', '点号键如 a.b 会成嵌套', '日期时间转字符串'],
  'faqs': [('TOML 日期能转吗？', '能，按 ISO 字符串输出。'), ('能给个例子吗？', '"[a]\nb = 1" → {"a":{"b":1}}。')],
  'en_name': 'TOML to JSON',
  'en_desc': 'TOML to JSON Guide: parse TOML config into JSON for programmatic consumption and validation.',
  'en_intro': 'Parses a TOML snippet into a JSON object, supporting nested tables, arrays and standard types. Handy for feeding config to JS/APIs. Local parsing.',
  'en_features': ['TOML to JSON parsing', 'Nested table expansion', 'Array and type restoration', 'Error location', 'Local processing'],
  'en_scenarios': ['Read Cargo.toml config', 'Config file validation', 'TOML to API data'],
  'en_steps': ['Paste the TOML', 'Click parse', 'View the JSON'],
  'en_tips': ['Table order is lost in JSON (objects are unordered)', 'Dotted keys like a.b become nested', 'Date/time becomes a string'],
  'en_faqs': [('Can TOML dates convert?', 'Yes, output as an ISO string.'), ('Can you show an example?', '"[a]\\n b = 1" → {"a":{"b":1}} .')],
 },

 {
  'slug': 'yaml-to-json',
  'ind': 'it',
  'base': 'yaml-to-json.html',
  'name': 'YAML 转 JSON',
  'desc': 'YAML 转 JSON 使用指南：把 YAML 配置转为 JSON，常用于 Kubernetes/Docker Compose 数据处理。',
  'intro': 'YAML 是 JSON 超集、用缩进表达层级。本工具把 YAML 解析为等效 JSON，方便程序读取与转换。本地解析不上传。',
  'features': ['YAML→JSON 转换', '缩进层级解析', '支持锚点/引用', '类型推断', '本地处理'],
  'scenarios': ['K8s/Docker Compose 配置转数据', '写文档示例', '格式校验'],
  'steps': ['粘贴 YAML', '点击转换', '查看 JSON'],
  'tips': ['缩进务必用空格不用 Tab', '锚点 & 与 * 会被展开', '多文档 --- 取首个'],
  'faqs': [('YAML 和 JSON 能互转吗？', '能，YAML 是 JSON 超集。'), ('能给个例子吗？', '"a:\n  b: 1" → {"a":{"b":1}}。')],
  'en_name': 'YAML to JSON',
  'en_desc': 'YAML to JSON Guide: convert YAML config into JSON, commonly used for Kubernetes/Docker Compose data.',
  'en_intro': 'YAML is a superset of JSON that uses indentation for hierarchy. This tool parses YAML into equivalent JSON for easy programmatic reading. Local parsing, nothing uploaded.',
  'en_features': ['YAML to JSON conversion', 'Indentation hierarchy parsing', 'Anchor/reference support', 'Type inference', 'Local processing'],
  'en_scenarios': ['K8s/Docker Compose config to data', 'Write doc examples', 'Format validation'],
  'en_steps': ['Paste the YAML', 'Click convert', 'View the JSON'],
  'en_tips': ['Always use spaces, never Tab, for indentation', 'Anchors & and * get expanded', 'For multi-doc ---, the first is taken'],
  'en_faqs': [('Can YAML and JSON convert both ways?', 'Yes, YAML is a superset of JSON.'), ('Can you show an example?', '"a:\\n  b: 1" → {"a":{"b":1}} .')],
 },

 {
  'slug': 'json-to-xml',
  'ind': 'it',
  'base': 'json-to-xml.html',
  'name': 'JSON 转 XML',
  'desc': 'JSON 转 XML 使用指南：将 JSON 对象序列化为 XML，便于对接旧系统或 SOAP 接口。',
  'intro': '把 JSON 键变标签、值变文本/子节点，数组转重复标签。适合把现代接口数据推给只认 XML 的系统。本地转换。',
  'features': ['JSON→XML 序列化', '数组转重复标签', '可选根节点', '属性化开关', '本地处理'],
  'scenarios': ['对接 SOAP/老系统', '生成 RSS 类结构', '数据格式桥接'],
  'steps': ['粘贴 JSON', '设根节点名', '点击转换', '复制 XML'],
  'tips': ['数组元素用同一标签名重复', '无键的值需给默认标签', '深层嵌套注意可读性'],
  'faqs': [('数组怎么表达？', '同一标签重复出现即可，如 <i>1</i><i>2</i>。'), ('能给个例子吗？', '{"a":[1,2]} → "<a><i>1</i><i>2</i></a>"。')],
  'en_name': 'JSON to XML',
  'en_desc': 'JSON to XML Guide: serialize a JSON object into XML for legacy systems or SOAP interfaces.',
  'en_intro': 'Turns JSON keys into tags and values into text/child nodes; arrays become repeated tags. Ideal for pushing modern API data to XML-only systems. Local conversion.',
  'en_features': ['JSON to XML serialization', 'Arrays to repeated tags', 'Optional root node', 'Attribute toggle', 'Local processing'],
  'en_scenarios': ['Integrate with SOAP/legacy systems', 'Generate RSS-like structures', 'Data format bridging'],
  'en_steps': ['Paste the JSON', 'Set a root node name', 'Click convert', 'Copy the XML'],
  'en_tips': ['Array items repeat under the same tag name', 'Valueless entries need a default tag', 'Watch readability on deep nesting'],
  'en_faqs': [('How are arrays expressed?', 'Repeat the same tag, e.g. <i>1</i><i>2</i> .'), ('Can you show an example?', '{"a":[1,2]} → "<a><i>1</i><i>2</i></a>" .')],
 },

 {
  'slug': 'hmac-generator',
  'ind': 'it',
  'base': 'hmac-generator.html',
  'name': 'HMAC 生成器',
  'desc': 'HMAC 生成器使用指南：用密钥对消息做 HMAC 签名(SHA256 等)，用于接口鉴权与数据完整性校验。',
  'intro': 'HMAC 是带密钥的哈希消息认证码，服务端用同一密钥验证请求未被篡改。本工具选算法、输入消息与密钥即得签名。本地运算不上传密钥。',
  'features': ['支持 SHA1/256/512 等', '文本或十六进制输出', '密钥与消息分离', 'Base64/Hex 切换', '本地运算'],
  'scenarios': ['Webhook 签名校验', 'API 请求鉴权', '验证数据完整性'],
  'steps': ['选哈希算法(常用 SHA256)', '输入消息与密钥', '点生成得签名', '复制给对方校验'],
  'tips': ['密钥务必保密、两端一致', '签名用于防篡改非加密', '十六进制与 Base64 需约定一致'],
  'faqs': [('HMAC 和哈希区别？', 'HMAC 多了密钥，单方无法伪造。'), ('能给个例子吗？', '消息"hello"、密钥"key"、HMAC-SHA256 得一段 64 位十六进制串。')],
  'en_name': 'HMAC Generator',
  'en_desc': 'HMAC Generator Guide: sign a message with a key (SHA256, etc.) for API auth and data integrity checks.',
  'en_intro': 'HMAC is a keyed hash message authentication code; the server verifies with the same key that the request was not tampered with. Pick an algorithm, enter the message and key, get the signature. Local, key not uploaded.',
  'en_features': ['SHA1/256/512 and more', 'Text or hex output', 'Separate key and message', 'Base64/Hex toggle', 'Local computation'],
  'en_scenarios': ['Webhook signature verification', 'API request authentication', 'Verify data integrity'],
  'en_steps': ['Pick a hash algorithm (SHA256 common)', 'Enter message and key', 'Click generate for the signature', 'Copy to the other party for verification'],
  'en_tips': ['Keep the key secret and identical on both sides', 'Signatures prevent tampering, not encryption', 'Hex and Base64 must be agreed upon'],
  'en_faqs': [('HMAC vs hash?', 'HMAC adds a key so one side cannot forge it.'), ('Can you show an example?', 'Message "hello", key "key", HMAC-SHA256 yields a 64-char hex string.')],
 },

 {
  'slug': 'sql-formatter',
  'ind': 'it',
  'base': 'sql-formatter.html',
  'name': 'SQL 格式化',
  'desc': 'SQL 格式化使用指南：把挤在一行的 SQL 美化为缩进清晰的语句，支持多方言与关键字大写。',
  'intro': '将杂乱 SQL 重新排版：关键字换行、缩进子查询、统一大小写。便于 Code Review 与排查。纯前端，SQL 不上传。',
  'features': ['缩进美化 SQL', '关键字大写/小写', '多方言(MySQL/PG/SQLite)', '支持多语句', '本地处理'],
  'scenarios': ['读他人写的紧凑 SQL', '排查长查询结构', '提交前规范化'],
  'steps': ['粘贴 SQL', '选方言与风格', '点击格式化', '复制结果'],
  'tips': ['子查询会自动缩进', 'JOIN 多时分层更易读', '只是排版不改语义'],
  'faqs': [('会改我的 SQL 逻辑吗？', '不会，仅排版。'), ('能给个例子吗？', '"select a from t where b=1" 展开为多行带缩进。')],
  'en_name': 'SQL Formatter',
  'en_desc': 'SQL Formatter Guide: prettify one-line SQL into clearly indented statements, with multi-dialect and keyword-case support.',
  'en_intro': 'Re-indents messy SQL: keywords on new lines, subqueries indented, case unified. Great for code review and debugging. Pure front-end, SQL not uploaded.',
  'en_features': ['Pretty-print SQL', 'Uppercase/lowercase keywords', 'Multiple dialects (MySQL/PG/SQLite)', 'Multi-statement support', 'Local processing'],
  'en_scenarios': ["Read someone else's compact SQL", 'Debug a long query structure', 'Normalize before committing'],
  'en_steps': ['Paste the SQL', 'Pick dialect and style', 'Click format', 'Copy the result'],
  'en_tips': ['Subqueries auto-indent', 'Many JOINs become layered and clearer', 'It only reformats, not changes semantics'],
  'en_faqs': [('Does it change my SQL logic?', 'No, formatting only.'), ('Can you show an example?', '"select a from t where b=1" expands to multi-line indented SQL.')],
 },

 {
  'slug': 'base85-encode',
  'ind': 'it',
  'base': 'base85-encode.html',
  'name': 'Base85 编解码',
  'desc': 'Base85 编解码使用指南：用 ASCII85/Base85 对二进制或文本做紧凑编码，比 Base64 更短。',
  'intro': 'Base85 把 4 字节映射为 5 个可打印字符，体积比 Base64 小约 25%。本工具支持文本/二进制互转，常用于 PostScript/PDF 嵌入。本地运算。',
  'features': ['文本↔Base85 互转', 'ASCII85 变体支持', '比 Base64 更紧凑', '本地运算'],
  'scenarios': ['PDF/PostScript 数据嵌入', '二进制文本化传输', '学习编码原理'],
  'steps': ['粘贴待编码文本', '点击编码看 Base85', '解码时粘贴 Base85 点解码'],
  'tips': ['含 0–9 与多数字母，去除了引号等', '解码失败多为非法字符', '体积比 Base64 省约 1/4'],
  'faqs': [('Base85 比 Base64 好在哪？', '更紧凑，约省 25% 长度。'), ('能给个例子吗？', '"hello" 的 ASCII85 编码为 "<~BOu!rDZ~>"(含定界符)。')],
  'en_name': 'Base85 Encode/Decode',
  'en_desc': 'Base85 Encode/Decode Guide: compact ASCII85/Base85 encoding for binary or text, shorter than Base64.',
  'en_intro': 'Base85 maps 4 bytes to 5 printable characters, about 25% smaller than Base64. Supports text/binary conversion, common in PostScript/PDF embedding. Local computation.',
  'en_features': ['Text to Base85 both ways', 'ASCII85 variant support', 'More compact than Base64', 'Local computation'],
  'en_scenarios': ['PDF/PostScript data embedding', 'Binary-as-text transport', 'Learn encoding principles'],
  'en_steps': ['Paste text to encode', 'Click encode to see Base85', 'Paste Base85 and click decode'],
  'en_tips': ['Contains digits 0-9 and many letters, quotes removed', 'Decode failures are mostly illegal chars', 'About 1/4 smaller than Base64'],
  'en_faqs': [('Where is Base85 better than Base64?', 'More compact, ~25% shorter.'), ('Can you show an example?', '"hello" in ASCII85 is "<~BOu!rDZ~>" (with delimiters).')],
 },

 {
  'slug': 'bip39-generator',
  'ind': 'it',
  'base': 'bip39-generator.html',
  'name': 'BIP39 助记词生成器',
  'desc': 'BIP39 助记词生成器使用指南：生成符合标准的加密货币助记词(12/24 词)，可派生种子与地址。',
  'intro': 'BIP39 用一组易记英文单词表示种子，是钱包恢复的基础。本工具可生成随机助记词或反向由词算种子。本地生成不上传，请离线保管。',
  'features': ['生成 12/24 词助记词', '多语言词表', '由助记词派生种子', '熵强度可选', '纯本地'],
  'scenarios': ['创建新钱包助记词', '钱包备份恢复演练', '学习 BIP39 原理'],
  'steps': ['选词数(12/24)与语言', '点生成记录助记词', '妥善离线备份'],
  'tips': ['助记词即资产，切勿截图上传', '顺序错一位都无法恢复', '仅用于学习或自建离线钱包'],
  'faqs': [('助记词能告诉别人吗？', '绝对不能，等同于私钥。'), ('能给个例子吗？', '12 词如 "apple bear cat ... zoo"，顺序固定才有效。')],
  'en_name': 'BIP39 Mnemonic Generator',
  'en_desc': 'BIP39 Mnemonic Generator Guide: generate standard crypto mnemonics (12/24 words), derivable to seed and addresses.',
  'en_intro': 'BIP39 represents a seed with easy-to-remember English words, the basis of wallet recovery. Generate random mnemonics or reverse from words to seed. Local, not uploaded — keep offline.',
  'en_features': ['Generate 12/24-word mnemonics', 'Multi-language wordlists', 'Derive seed from mnemonic', 'Selectable entropy', 'Fully local'],
  'en_scenarios': ['Create a new wallet mnemonic', 'Wallet backup recovery drill', 'Learn BIP39 principles'],
  'en_steps': ['Pick word count (12/24) and language', 'Click generate and record the mnemonic', 'Back it up offline safely'],
  'en_tips': ['The mnemonic IS the asset — never screenshot or upload it', 'One wrong word order and recovery fails', 'For learning or your own offline wallet only'],
  'en_faqs': [('Can I tell someone the mnemonic?', 'Absolutely not — it equals the private key.'), ('Can you show an example?', '12 words like "apple bear cat ... zoo", order fixed to be valid.')],
 },

 {
  'slug': 'user-agent-parser',
  'ind': 'it',
  'base': 'user-agent-parser.html',
  'name': 'User-Agent 解析器',
  'desc': 'User-Agent 解析器使用指南：拆解 UA 字符串，识别浏览器、操作系统、设备类型与引擎。',
  'intro': 'UA 串包含浏览器、系统、设备等信息。本工具把一段 UA 解析为结构化字段，便于日志分析、兼容判断。本地解析。',
  'features': ['解析浏览器/版本', '识别 OS 与设备', '判别爬虫/移动端', '结构化展示', '本地处理'],
  'scenarios': ['分析访问日志来源', '做浏览器兼容分支', '识别爬虫流量'],
  'steps': ['粘贴 UA 字符串', '点击解析', '查看结构化字段'],
  'tips': ['UA 可被伪造，判断需谨慎', '移动端含 "Mobile" 关键字', '新版 Chrome 带 "Edg"/"Chrome" 双标识'],
  'faqs': [('UA 可靠吗？', '客户端可控，仅作参考。'), ('能给个例子吗？', '"Mozilla/5.0 (iPhone...) Safari" → 设备:手机, OS:iOS。')],
  'en_name': 'User-Agent Parser',
  'en_desc': 'User-Agent Parser Guide: break down a UA string to identify browser, OS, device type and engine.',
  'en_intro': 'A UA string carries browser, OS and device info. This tool parses a UA into structured fields for log analysis and compatibility checks. Local parsing.',
  'en_features': ['Parse browser/version', 'Detect OS and device', 'Identify bots/mobile', 'Structured display', 'Local processing'],
  'en_scenarios': ['Analyze access-log sources', 'Branch on browser compatibility', 'Spot bot traffic'],
  'en_steps': ['Paste the UA string', 'Click parse', 'View the structured fields'],
  'en_tips': ['UA can be spoofed, judge with caution', 'Mobile contains the "Mobile" keyword', 'New Chrome shows both "Edg"/"Chrome" markers'],
  'en_faqs': [('Is UA reliable?', 'Client-controllable, reference only.'), ('Can you show an example?', '"Mozilla/5.0 (iPhone...) Safari" → device: phone, OS: iOS.')],
 },

 {
  'slug': 'password-strength',
  'ind': 'it',
  'base': 'password-strength.html',
  'name': '密码强度检测',
  'desc': '密码强度检测使用指南：实时评估密码安全等级，检查长度、字符多样性与常见弱点。',
  'intro': '输入密码即时给出强度评分与改进建议（长度、大小写、数字、符号、常见弱口令）。本地检测不上传密码。',
  'features': ['实时强度评分', '字符类型检查', '弱口令/重复检测', '建议提示', '本地运算'],
  'scenarios': ['注册时评估口令', '审计现有密码', '教学密码安全'],
  'steps': ['输入密码', '查看强度条与建议', '按提示增强复杂度'],
  'tips': ['越长越好，12 位以上更稳', '混合四类字符显著提升', '避免生日/字典词'],
  'faqs': [('多长算安全？', '建议 ≥12 位且含多类字符。'), ('能给个例子吗？', '"123456" 判弱；"Tg7$mK9pQw2!" 判强。')],
  'en_name': 'Password Strength Detector',
  'en_desc': 'Password Strength Detector Guide: evaluate password security in real time, checking length, character diversity and common weaknesses.',
  'en_intro': 'Get an instant strength score and improvement tips (length, case, digits, symbols, common weak passwords) as you type. Local detection, password not uploaded.',
  'en_features': ['Real-time strength score', 'Character-type checks', 'Weak/duplicate detection', 'Suggestion hints', 'Local computation'],
  'en_scenarios': ['Assess a password at signup', 'Audit an existing password', 'Teach password safety'],
  'en_steps': ['Type the password', 'View the strength bar and tips', 'Strengthen per the hints'],
  'en_tips': ['Longer is better, 12+ chars is safer', 'Mixing four character classes helps a lot', 'Avoid birthdays/dictionary words'],
  'en_faqs': [('How long is safe?', 'Recommended ≥12 chars with multiple character classes.'), ('Can you show an example?', '"123456" is weak; "Tg7$mK9pQw2!" is strong.')],
 },

 {
  'slug': 'number-base-converter',
  'ind': 'it',
  'base': 'number-base-converter.html',
  'name': '进制转换计算器',
  'desc': '进制转换计算器使用指南：在 2/8/10/16 等进制间互转整数，支持大数与有符号表示。',
  'intro': '在二进制、八进制、十进制、十六进制之间转换数值，常用于底层开发、网络与颜色处理。本地运算。',
  'features': ['2/8/10/16 互转', '支持自定义进制', '大数支持', '有符号/无符号', '本地处理'],
  'scenarios': ['调试位运算结果', '读内存/颜色十六进制', '协议字段解析'],
  'steps': ['选源进制与目标的进制', '输入数值', '查看各进制结果'],
  'tips': ['十六进制每两位=一字节', '负数用补码表示', '字母 A–F 不区分大小写'],
  'faqs': [('0xFF 是多少？', '十进制 255。'), ('能给个例子吗？', '十进制 255 → 二进制 11111111、十六进制 FF。')],
  'en_name': 'Base Converter Calculator',
  'en_desc': 'Base Converter Calculator Guide: convert integers between bases 2/8/10/16, with big-number and signed support.',
  'en_intro': 'Convert values across binary, octal, decimal and hexadecimal — common in low-level dev, networking and color work. Local computation.',
  'en_features': ['Convert between 2/8/10/16', 'Custom base support', 'Big-number support', 'Signed/unsigned', 'Local processing'],
  'en_scenarios': ['Debug bit-operation results', 'Read memory/color hex', 'Parse protocol fields'],
  'en_steps': ['Pick source and target bases', 'Enter the value', 'View results in each base'],
  'en_tips': ['Two hex digits = one byte', "Negatives use two's complement", 'Letters A-F are case-insensitive'],
  'en_faqs': [('What is 0xFF?', 'Decimal 255.'), ('Can you show an example?', 'Decimal 255 → binary 11111111, hex FF.')],
 },

 {
  'slug': 'basic-auth-generator',
  'ind': 'it',
  'base': 'basic-auth-generator.html',
  'name': 'Basic Auth 生成器',
  'desc': 'Basic Auth 生成器使用指南：一键生成 HTTP Basic 认证所需的 Authorization 头与 curl 片段。',
  'intro': 'Basic Auth 把"用户名:密码"Base64 后放入请求头。本工具生成标准头值与可复制的 curl 命令，便于联调。本地生成不上传凭据。',
  'features': ['生成 Authorization 头', 'Base64 编码凭据', '输出 curl 示例', '本地运算'],
  'scenarios': ['调试受保护接口', '快速联调后台', '生成测试请求'],
  'steps': ['输入用户名与密码', '点生成得头值', '复制 curl 或请求头'],
  'tips': ['Basic Auth 明文传输，务必配 HTTPS', '头格式 "Basic <base64>"', '凭据勿硬编码进前端'],
  'faqs': [('为什么要 Base64？', '仅编码非加密，配合 HTTPS 才安全。'), ('能给个例子吗？', '"user:pass" → "Authorization: Basic dXNlcjpwYXNz"。')],
  'en_name': 'Basic Auth Generator',
  'en_desc': 'Basic Auth Generator Guide: one-click generate the Authorization header and curl snippet for HTTP Basic auth.',
  'en_intro': 'Basic Auth Base64-encodes "user:pass" into the request header. This tool generates the standard header value and a copyable curl command for quick testing. Local, credentials not uploaded.',
  'en_features': ['Generate Authorization header', 'Base64-encode credentials', 'Output a curl example', 'Local computation'],
  'en_scenarios': ['Debug a protected endpoint', 'Quick back-end integration', 'Generate a test request'],
  'en_steps': ['Enter username and password', 'Click generate for the header value', 'Copy the curl or request header'],
  'en_tips': ['Basic Auth is plaintext — always use HTTPS', 'Header format "Basic <base64>"', 'Never hardcode credentials in the front-end'],
  'en_faqs': [('Why Base64?', 'It only encodes, not encrypts; pair with HTTPS for safety.'), ('Can you show an example?', '"user:pass" → "Authorization: Basic dXNlcjpwYXNz".')],
 },

 {
  'slug': 'api-sign-generator',
  'ind': 'it',
  'base': 'api-sign-generator.html',
  'name': 'API 签名生成器',
  'desc': 'API 签名生成器使用指南：按常见签名规则(拼接+密钥+哈希)生成请求签名，用于接口鉴权联调。',
  'intro': '许多开放平台要求把参数按规则排序拼接、加密钥后哈希作为 sign。本工具按常用算法生成签名，便于服务端比对。本地运算。',
  'features': ['参数排序拼接', 'MD5/SHA 等哈希', '密钥拼接', '输出 sign 值', '本地处理'],
  'scenarios': ['开放平台接口联调', '服务端 sign 比对', '排查签名不一致'],
  'steps': ['填入参数键值与密钥', '选算法与拼接规则', '点生成得 sign', '放入请求校验'],
  'tips': ['参数需按约定排序(常按 key 字典序)', '空值参数是否参与需看文档', '时间戳防重放常一起用'],
  'faqs': [('sign 失败先看什么？', '排序规则与是否含空值、密钥位置。'), ('能给个例子吗？', 'a=1&b=2 + key → 拼接 "a=1&b=2&key=K" 再 MD5 得 sign。')],
  'en_name': 'API Signature Generator',
  'en_desc': 'API Signature Generator Guide: generate a request signature by common rules (concat + key + hash) for API auth integration.',
  'en_intro': 'Many open platforms require parameters sorted/concatenated with a key then hashed as "sign". This tool generates the signature by common algorithms for server-side comparison. Local computation.',
  'en_features': ['Sort and concatenate params', 'MD5/SHA and other hashes', 'Key concatenation', 'Output sign value', 'Local processing'],
  'en_scenarios': ['Open-platform API integration', 'Server-side sign comparison', 'Troubleshoot sign mismatch'],
  'en_steps': ['Fill param key-values and key', 'Pick algorithm and concat rule', 'Click generate for sign', 'Put into the request for verification'],
  'en_tips': ['Params are usually sorted by key (often lexicographic)', 'Whether empty params participate depends on docs', 'Timestamp for replay protection is often used together'],
  'en_faqs': [('What to check first when sign fails?', 'Sort rule, and whether empty values / key position are involved.'), ('Can you show an example?', 'a=1&b=2 + key → concat "a=1&b=2&key=K" then MD5 for sign.')],
 },

 {
  'slug': 'bitwise-calculator',
  'ind': 'it',
  'base': 'bitwise-calculator.html',
  'name': '位运算计算器',
  'desc': '位运算计算器使用指南：对整数做 AND/OR/XOR/NOT/移位，支持十进制与十六进制输入。',
  'intro': '位运算直接操作二进制位，广泛用于权限掩码、协议字段、性能优化。本工具输入两数与运算符即得结果。本地运算。',
  'features': ['AND/OR/XOR/NOT', '左移/右移', '十进制/十六进制输入', '32 位结果', '本地处理'],
  'scenarios': ['权限位掩码计算', '协议标志位解析', '算法底层调试'],
  'steps': ['输入两个数值', '选运算符', '查看十进制/十六进制结果'],
  'tips': ['移位等价于乘除以 2 的幂', 'XOR 常用于翻转/校验', '负数用 32 位补码'],
  'faqs': [('权限掩码怎么用？', '用位表示权限，AND 检测、OR 赋予。'), ('能给个例子吗？', '5(101) AND 3(011) = 1(001)。')],
  'en_name': 'Bitwise Calculator',
  'en_desc': 'Bitwise Calculator Guide: AND/OR/XOR/NOT/shift integers, with decimal and hex input.',
  'en_intro': 'Bit operations act directly on binary bits, widely used for permission masks, protocol fields and performance. Enter two numbers and an operator to get the result. Local computation.',
  'en_features': ['AND/OR/XOR/NOT', 'Left/right shift', 'Decimal/hex input', '32-bit result', 'Local processing'],
  'en_scenarios': ['Permission bit-mask computation', 'Protocol flag parsing', 'Low-level algorithm debugging'],
  'en_steps': ['Enter two values', 'Pick the operator', 'View decimal/hex result'],
  'en_tips': ['Shifts equal multiply/divide by powers of two', 'XOR is often used to flip/check', "Negatives use 32-bit two's complement"],
  'en_faqs': [('How to use a permission mask?', 'Bits represent permissions: AND to test, OR to grant.'), ('Can you show an example?', '5 (101) AND 3 (011) = 1 (001).')],
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

# 全站通用 section / 导航词（固定，不随 slug 变化）
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
    # 导出英文字典到 js/guide-en-pack.js（多批次脚本共享合并）
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
    # 合并到 js/guide-en-pack.js（多批次脚本共享同一字典，避免互相覆盖）
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
