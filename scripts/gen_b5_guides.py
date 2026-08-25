#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
B5-06 内容集群与 FAQ 增长 — 生成 6 大主题内容集群

产出（全部写入 guides/，由 _build.py 自动纳入 sitemap）：
  - 18 篇高质量指南/FAQ（每主题 3 篇），均带 Article + BreadcrumbList + FAQPage 结构化数据、
    目录、真实步骤、可验证示例、上下文内链（指向相关工具）。
  - 6 个集群入口页（cluster-<topic>.html）：工具入口 → 指南 → FAQ → 相关工具 的枢纽。
  - 将 18 条 {tool, guide, title} 追加进 json/guides.json，使工具页反向链接到指南（双向内链）。

原则：每篇内容有独立 search intent、真实步骤、可验证示例；复用静态模板，避免空泛批量生成。
Run: python3 scripts/gen_b5_guides.py
"""
import os
import json
import datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GUIDES_DIR = os.path.join(ROOT, "guides")
SITE = "https://chenguangwu.github.io"
TODAY = "2026-08-07"

CLUSTERS = {
    "json":    {"name": "JSON 与数据", "intro": "JSON/YAML 格式化、校验、查询与转换，前端与接口调试的常备工具集群。"},
    "encode":  {"name": "编码与加密", "intro": "Base 系列、URL/HTML 实体、Unicode 等编码转换，安全传输与调试的基础。"},
    "image":   {"name": "图片与视觉", "intro": "二维码、颜色、SVG、ASCII 与 GIF 处理，覆盖常见图片创作与处理场景。"},
    "dev":     {"name": "开发者工具", "intro": "JWT、HTTP、IP/子网、正则等开发者日常高频调试与计算工具。"},
    "finance": {"name": "财务与投资", "intro": "复利、房贷、NPV、ROI、货币等个人与小微决策的财务计算集群。"},
    "health":  {"name": "健康与生活", "intro": "BMI、体脂、血压、热量、血糖等个人健康指标的测算与解读。"},
}

# 每篇指南：slug, cluster, title, desc, primary(tool,ind,name), related[(tool,ind,name)...],
#           sections[(h2, html)...], example{caption,code}, faqs[(q,a)...]
GUIDES = [
    # ---------- JSON ----------
    {
        "slug": "json-schema-validator", "cluster": "json",
        "title": "JSON Schema 校验入门：用模式约束接口数据",
        "desc": "什么是 JSON Schema，如何用它校验 API 返回的 JSON 是否合法，附可复制的 draft-07 示例。",
        "primary": ("json-schema-validator", "it", "JSON Schema 校验器"),
        "related": [("json-formatter", "it", "JSON 格式化"), ("yaml-validator", "it", "YAML 校验器")],
        "sections": [
            ("什么是 JSON Schema", "<p>JSON Schema 是一份描述 JSON 数据「应该长什么样」的 JSON 文档，常见版本为 draft-07。它用 <code>type</code>、<code>required</code>、<code>properties</code>、<code>enum</code> 等关键字声明字段类型与约束，常用来校验接口请求/响应、配置文件是否合规。</p>"),
            ("写一个最小 Schema", "<p>下面这段 schema 要求对象必须包含 <code>name</code>（字符串）和 <code>age</code>（非负整数），<code>role</code> 只能是 user/admin：</p>"),
            ("在 ToolBox 中校验", "<p>打开 JSON Schema 校验器，左侧粘贴数据、右侧粘贴 schema，点击校验即可看到逐字段结果。把示例数据故意改成 <code>\"age\": -3</code> 会立即报「minimum」错误。</p>"),
            ("常见校验错误", "<p><b>type mismatch</b>：字段类型不符；<b>required</b>：缺少必填字段；<b>enum</b>：值不在允许集合；<b>additionalProperties</b>：出现了 schema 未声明的字段（可设为 false 严格校验）。</p>"),
        ],
        "example": {
            "caption": "数据与 schema 示例",
            "code": '// 数据\ndef data = {\n  "name": "Ada",\n  "age": 30,\n  "role": "admin"\n}\n\n// schema (draft-07)\n{\n  "type": "object",\n  "required": ["name", "age"],\n  "properties": {\n    "name": { "type": "string" },\n    "age":  { "type": "integer", "minimum": 0 },\n    "role": { "enum": ["user", "admin"] }\n  }\n}',
        },
        "faqs": [
            ("JSON Schema 能校验数组吗？", "能。用 \"type\":\"array\" 配合 \"items\" 描述每个元素的 schema，还可加 \"minItems\"/\"maxItems\" 限制长度。"),
            ("draft-07 和 2020-12 有什么区别？", "语法大体兼容，2020-12 引入了 $defs、dependentRequired 等更细的约束；多数业务用 draft-07 已足够。"),
            ("前端能用 JSON Schema 校验吗？", "可以。Ajv 等库能在浏览器内按 schema 校验表单与接口数据，ToolBox 的校验器适合快速调试与复制结果。"),
        ],
    },
    {
        "slug": "json-path", "cluster": "json",
        "title": "JSONPath 提取字段：从嵌套 JSON 精准取值",
        "desc": "用 JSONPath 表达式从深层嵌套的 JSON 中提取字段，附 $、..、[*]、过滤器等语法示例。",
        "primary": ("json-path", "it", "JSONPath 提取器"),
        "related": [("json-formatter", "it", "JSON 格式化"), ("json-diff", "it", "JSON 对比")],
        "sections": [
            ("JSONPath 是什么", "<p>JSONPath 类似 XML 的 XPath，用简短表达式在 JSON 中定位数据。它以 <code>$</code> 表示根，<code>.key</code> 取属性，<code>[*]</code> 遍历数组，<code>..</code> 递归查找。</p>"),
            ("核心语法速查", "<p><code>$.store.book[0]</code> 第一个元素；<code>$.store.book[*].title</code> 所有标题；<code>$..price</code> 递归找所有 price；<code>$.store.book[?(@.price<10)]</code> 过滤器取低价书。</p>"),
            ("在 ToolBox 中提取", "<p>把 JSON 粘贴到左侧、在表达式框输入路径，右侧即时显示匹配结果；表达式写错会提示无匹配，便于调试接口返回的复杂结构。</p>"),
        ],
        "example": {
            "caption": "对如下 JSON 执行 $.store.book[*].author",
            "code": '{\n  "store": {\n    "book": [\n      { "author": "金庸", "price": 8 },\n      { "author": "鲁迅", "price": 12 }\n    ]\n  }\n}\n\n// 结果\n[ "金庸", "鲁迅" ]',
        },
        "faqs": [
            ("JSONPath 和 JavaScript 取值有何不同？", "JSONPath 是声明式字符串表达式，便于配置与复用；直接 obj.a.b 是代码，二者可互相转换。"),
            ("过滤器 ?() 支持哪些运算？", "常见支持 ==、!=、<、<=、>、>= 及存在性检查 @.key 存在；复杂逻辑建议先抽取再在代码中处理。"),
            ("为什么我的表达式返回空？", "多半是大小写或路径层级不对；先用 $..字段名 递归查找确认字段确实存在。"),
        ],
    },
    {
        "slug": "yaml-validator", "cluster": "json",
        "title": "YAML 校验与 JSON 互转",
        "desc": "YAML 为什么容易出错，如何用 ToolBox 校验语法并和 JSON 互转，附缩进与锚点注意点。",
        "primary": ("yaml-validator", "it", "YAML 校验器"),
        "related": [("json-formatter", "it", "JSON 格式化"), ("json-schema-validator", "it", "JSON Schema 校验器")],
        "sections": [
            ("YAML 与 JSON 的关系", "<p>YAML 是 JSON 的超集，用缩进表达层级、更易读，常用于配置文件（如 CI、K8s）。它本质仍可转为 JSON，因此「先当 JSON 校验」是常见排错思路。</p>"),
            ("最常见的错误：缩进", "<p>YAML 对空格缩进极其敏感，Tab 与空格混用会直接报错。统一用 2 个空格，且同层必须对齐。</p>"),
            ("在 ToolBox 中校验/转换", "<p>粘贴 YAML 点击校验，错误会定位到行；一键转为 JSON 后可直接用 JSON 工具链继续处理。</p>"),
        ],
        "example": {
            "caption": "YAML → JSON",
            "code": '# YAML\nname: Ada\nage: 30\nhobbies:\n  - 阅读\n  - 编程\n\n// JSON\n{\n  "name": "Ada",\n  "age": 30,\n  "hobbies": ["阅读", "编程"]\n}',
        },
        "faqs": [
            ("YAML 的 & 锚点和 * 别名是什么？", "它们是 YAML 的复用机制：&anchor 定义、*alias 引用，能减少重复；转换 JSON 时会被展开为实际值。"),
            ("布尔值 true/false 会被误转吗？", "会。YAML 把 yes/no/on/off 也当布尔，敏感场景下建议加引号写成 \"yes\" 以避免歧义。"),
            ("Tab 真的不能用吗？", "标准 YAML 不允许 Tab 缩进，很多解析器会直接报错；务必用空格。"),
        ],
    },
    # ---------- 编码 ----------
    {
        "slug": "html-entity-encoder", "cluster": "encode",
        "title": "HTML 实体编码与 XSS 转义",
        "desc": "为什么要把 < > & 转成实体，如何用 ToolBox 做 HTML 实体编解码与基础 XSS 防护。",
        "primary": ("html-entity-encoder", "it", "HTML 实体编码器"),
        "related": [("url-encode", "it", "URL 编码"), ("base64", "it", "Base64 编解码")],
        "sections": [
            ("为什么需要实体编码", "<p>在 HTML 中直接输出 <code><script></code> 会被浏览器当作标签/脚本执行，造成 XSS。把 <code><</code> 转成 <code>&lt;</code>、<code>></code> 转成 <code>&gt;</code>、<code>&</code> 转成 <code>&amp;</code>，可让特殊字符「只显示不执行」。</p>"),
            ("实体 vs 字符引用", "<p><code>&lt;</code> 是命名实体，<code>&#60;</code> 是十进制数字引用，<code>&#x3C;</code> 是十六进制；三者等价，命名实体更易读。</p>"),
            ("在 ToolBox 中使用", "<p>粘贴文本点击编码即可获得实体化结果，适合回填到模板/富文本前做转义；解码则把实体还原为原字符。</p>"),
            ("XSS 防护的边界", "<p>实体编码只是输出层手段之一，不能替代参数化查询、CSP、输入校验等综合防护；对 URL、属性、JS 上下文要分别处理。</p>"),
        ],
        "example": {
            "caption": "编码前后",
            "code": '输入:  <script>alert(1)</script>\n编码:  &lt;script&gt;alert(1)&lt;/script&gt;',
        },
        "faqs": [
            ("属性值里也要转义引号吗？", "要。放在双引号属性中的 \" 应转成 &quot;，单引号属性同理转 &apos;，避免提前闭合属性。"),
            ("转义后还能正常显示吗？", "能。浏览器渲染时会把实体还原为对应字符显示，仅源码层面是转义形态。"),
            ("仅做 HTML 转义够防 XSS 吗？", "对 HTML 正文足够；但若内容进入 URL、on* 事件或 JS 字符串，需要对应场景的编码，单一手段并不万能。"),
        ],
    },
    {
        "slug": "unicode-lookup", "cluster": "encode",
        "title": "Unicode 码点与字符查询",
        "desc": "理解 U+ 码点、emoji 与特殊符号，如何用 ToolBox 查询字符的 Unicode 编码。",
        "primary": ("unicode-lookup", "it", "Unicode 查询器"),
        "related": [("url-encode", "it", "URL 编码"), ("punycode", "it", "Punycode 转换")],
        "sections": [
            ("什么是码点", "<p>Unicode 给每个字符分配一个编号，记作码点，如 <code>U+0041</code> 是字母 A。一个 emoji 可能由多个码点组成（如带肤色的表情）。</p>"),
            ("常见用途", "<p>排查「乱码/问号」时，查看字符的真实码点能定位是编码不一致还是字符本身不存在；特殊符号（如 © ✓ ❤）也靠码点引用。</p>"),
            ("在 ToolBox 中查询", "<p>输入字符或码点（如 U+1F600）即可双向查询，并显示 UTF-8/UTF-16 字节，便于调试传输与存储问题。</p>"),
        ],
        "example": {
            "caption": "查询示例",
            "code": '字符:  😀\n码点: U+1F600\nUTF-8: F0 9F 98 80',
        },
        "faqs": [
            ("一个 emoji 为什么显示成两个方框？", "可能是系统字体缺该码点，或所用字体不含该 emoji 的字形；码点存在但无字形就会显示成豆腐块。"),
            ("U+ 和 &#x 有什么区别？", "U+1F600 是书写约定；&#x1F600; 是 HTML 数字实体写法，二者指向同一码点。"),
            ("中文也是 Unicode 吗？", "是。中文常用码点位于 U+4E00 起的 CJK 统一表意文字区，同样适用码点查询。"),
        ],
    },
    {
        "slug": "base32-encode", "cluster": "encode",
        "title": "Base32 / Base58 / Base85 编码对比",
        "desc": "Base 家族不止 Base64，详解 Base32/58/85 的取舍与适用场景，附 ToolBox 互转示例。",
        "primary": ("base32-encode", "it", "Base32 编码器"),
        "related": [("base64", "it", "Base64 编解码"), ("base85-encode", "it", "Base85 编码")],
        "sections": [
            ("为什么有这么多 Base 家族", "<p>它们都用「安全字符集」表示二进制，但字符表不同：Base64 最紧凑常用；Base32 只用大写字母+数字 2-7，避免易混淆字符，适合手动抄写；Base58 去掉 0/O/l/I 等，用于比特币地址；Base85 更紧凑，用于 PostScript/PDF。</p>"),
            ("Base32 的典型场景", "<p>OTP 密钥（如 Google Authenticator 的 secret）、激活码等需要「人能准确抄写」的场景，Base32 排除易混字符降低出错率。</p>"),
            ("在 ToolBox 中选择", "<p>Base32/58/64/85 工具均支持编码与解码，粘贴内容选择对应算法即可；注意不同算法的填充与字母表差异，解码要用同一算法。</p>"),
        ],
        "example": {
            "caption": "Base32 编码 \"Hello\"",
            "code": '原文:  Hello\nBase32: JBSWY3DPEBLW64TMMQ======',
        },
        "faqs": [
            ("Base32 比 Base64 长很多吗？", "是的。Base32 每个字符只承载 5 bit，比 Base64 的 6 bit 效率低，因此体积更大，换取可读性。"),
            ("Base58 为什么去掉某些字母？", "去掉 0、O、I、l 等视觉相近字符，避免地址在复制/手抄时出错，常见于加密货币。"),
            ("能用 Base64 解码 Base32 的结果吗？", "不能。字符表与编码规则不同，必须用对应算法互转。"),
        ],
    },
    # ---------- 图片 ----------
    {
        "slug": "svg-placeholder-generator", "cluster": "image",
        "title": "SVG 占位图生成：前端原型与邮件都适用",
        "desc": "为什么用 SVG 占位图，如何生成带尺寸/文字/颜色的占位图并内联为 Data URI。",
        "primary": ("svg-placeholder-generator", "it", "SVG 占位图生成器"),
        "related": [("color-picker", "design", "颜色选择器"), ("qrcode-generator", "it", "二维码生成器")],
        "sections": [
            ("为什么用 SVG 占位", "<p>SVG 是矢量、体积极小、可任意缩放不模糊，且能直接内联进 HTML/邮件，不依赖外部图片请求，非常适合原型与骨架屏。</p>"),
            ("常用参数", "<p>宽高、背景色、文字颜色、显示的尺寸文字。生成后可复制 SVG 源码或 Data URI 直接用在 <code><img src></code> 或 CSS 中。</p>"),
            ("在 ToolBox 中生成", "<p>填写尺寸与配色点击生成，预览即时更新；复制得到的 SVG/Data URI 粘贴到项目即可。</p>"),
        ],
        "example": {
            "caption": "生成 300×200 灰色占位图",
            "code": '<svg xmlns="http://www.w3.org/2000/svg" width="300" height="200">\n  <rect width="100%" height="100%" fill="#E5E7EB"/>\n  <text x="50%" y="50%" fill="#6B7280" text-anchor="middle" dominant-baseline="middle">300×200</text>\n</svg>',
        },
        "faqs": [
            ("Data URI 会拖慢页面吗？", "小图内联反而省一次请求；大图则建议用独立文件，避免 HTML 体积过大。"),
            ("邮件里能用 SVG 占位吗？", "部分邮件客户端对 SVG 支持有限，必要时改用 PNG 占位或带兜底alt文本。"),
            ("占位图能加圆角/渐变吗？", "能。SVG 支持 rect 的 rx 圆角与线性渐变，复杂样式可在生成后手动编辑源码。"),
        ],
    },
    {
        "slug": "image-to-ascii", "cluster": "image",
        "title": "图片转 ASCII 艺术",
        "desc": "图片如何变成字符画，亮度映射原理、参数调节与适用边界，附 ToolBox 转换要点。",
        "primary": ("image-to-ascii", "design", "图片转 ASCII"),
        "related": [("color-picker", "design", "颜色选择器"), ("svg-placeholder-generator", "it", "SVG 占位图生成器")],
        "sections": [
            ("原理：亮度映射", "<p>工具先把图片转灰度，再把每个像素的亮度映射到字符集（如 <code>@%#*+=-:. </code>），亮处用疏字符、暗处用密字符，从而得到字符画。</p>"),
            ("关键参数", "<p><b>宽度</b>决定横向字符数；<b>字符集</b>影响质感；<b>反相</b>用于深色背景。宽度过大会让输出过长，过小则看不清。</p>"),
            ("在 ToolBox 中转换", "<p>上传图片后调节宽度与字符集实时预览，复制结果即可贴到终端、README 或聊天中。</p>"),
        ],
        "example": {
            "caption": "简单示意（实际为像素亮度映射）",
            "code": '  ##\n #  #\n ####\n #  #\n #  #',
        },
        "faqs": [
            ("为什么复杂照片效果差？", "字符画分辨率低，复杂明暗细节会丢失；轮廓清晰、对比强的图效果最好。"),
            ("能导出为文件吗？", "复制文本后用 .txt 保存即可；需要彩色可在支持 ANSI 的工具中另存。"),
            ("字符画可以用于 Logo 吗？", "适合极简/极客风格，正式品牌建议仍用矢量 SVG。"),
        ],
    },
    {
        "slug": "gif-split", "cluster": "image",
        "title": "GIF 逐帧拆分与提取",
        "desc": "GIF 为何是多帧动画，如何用 ToolBox 提取单帧或全部帧用于表情包与动图分析。",
        "primary": ("gif-split", "image", "GIF 逐帧拆分"),
        "related": [("svg-placeholder-generator", "it", "SVG 占位图生成器"), ("image-to-ascii", "design", "图片转 ASCII")],
        "sections": [
            ("GIF 是「帧的合集」", "<p>GIF 动图本质是多张静态帧按延迟时间循环播放，因此可以把每一帧单独提取出来使用。</p>"),
            ("常见用途", "<p>截取表情包某一帧、分析动画时序、把动图关键帧做成静态素材等。</p>"),
            ("在 ToolBox 中拆分", "<p>上传 GIF 后预览各帧，可下载单帧或全部帧；注意帧数很多时全部导出文件量较大。</p>"),
        ],
        "example": {
            "caption": "提取示意",
            "code": 'GIF(10帧) → [帧0][帧1]...[帧9]\n可单独保存 帧3 作为静态图',
        },
        "faqs": [
            ("提取的帧会失真吗？", "GIF 本身色域有限（最多 256 色），提取的帧与动图中对应帧一致。"),
            ("能改帧延时吗？", "拆分主要做提取；调整延时/重组建议用专门 GIF 编辑工具或脚本。"),
            ("大文件会卡吗？", "帧数多的 GIF 解析较慢且产出多，建议先确认只需的帧范围。"),
        ],
    },
    # ---------- 开发者 ----------
    {
        "slug": "jwt-debugger", "cluster": "dev",
        "title": "JWT 调试：拆解 Header / Payload / Signature",
        "desc": "JWT 三段结构如何解码，claims 怎么看，签名验证的前提与安全注意（别粘生产密钥）。",
        "primary": ("jwt-debugger", "it", "JWT 调试器"),
        "related": [("base64", "it", "Base64 编解码"), ("timestamp-converter", "it", "时间戳转换")],
        "sections": [
            ("JWT 的三段结构", "<p>JWT（JSON Web Token）形如 <code>header.payload.signature</code>，前两段是 Base64URL 编码的 JSON，第三段是签名。用 . 分割即可分别解码查看。</p>"),
            ("重点看 Payload 的 claims", "<p><code>sub</code> 主体、<code>iss</code> 签发者、<code>exp</code> 过期时间（Unix 秒）、<code>iat</code> 签发时间。exp 过期后 token 应被拒绝。</p>"),
            ("签名验证的边界", "<p>仅解码不验证签名；要验证签名必须持有对应密钥/公钥，且应在服务端完成。前端调试只做可读性解码。</p>"),
            ("安全注意", "<p>JWT 中不要放密码等敏感信息（它只是编码不是加密），且切勿把生产密钥粘贴到不可信页面。</p>"),
        ],
        "example": {
            "caption": "一段示例 JWT（已截断）",
            "code": 'eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiIxMjMiLCJleHAiOjE3MDAwMDAwMDB9.xxxx\n\nHeader : {"alg":"HS256","typ":"JWT"}\nPayload: {"sub":"123","exp":1700000000}',
        },
        "faqs": [
            ("Base64URL 和普通 Base64 一样吗？", "类似但把 + / 换成 - _ 并去掉填充 =，更适合放在 URL 中。"),
            ("为什么解码出 exp 但页面说已过期？", "exp 是 Unix 秒，需对照当前时间；可用时间戳工具核对。"),
            ("能在浏览器里验证签名吗？", "可以持密钥验证，但密钥暴露在前端有风险；生产验证务必放服务端。"),
        ],
    },
    {
        "slug": "http-response-headers", "cluster": "dev",
        "title": "HTTP 响应头详解与常见排查",
        "desc": "Content-Type、Cache-Control、CORS、Set-Cookie 等响应头的作用与典型排错思路。",
        "primary": ("http-response-headers", "it", "HTTP 响应头查看"),
        "related": [("http-status", "it", "HTTP 状态码"), ("url-encode", "it", "URL 编码")],
        "sections": [
            ("常用响应头", "<p><code>Content-Type</code> 声明内容类型；<code>Cache-Control</code> 控制缓存；<code>Set-Cookie</code> 下发会话；<code>Access-Control-Allow-Origin</code> 决定跨域是否放行。</p>"),
            ("用响应头排查问题", "<p>样式/脚本不生效常因 <code>Content-Type</code> 错；刷新没更新看 <code>Cache-Control</code>；跨域报错看 CORS 头；登录态丢失查 <code>Set-Cookie</code> 的 Domain/Path/SameSite。</p>"),
            ("在 ToolBox 中查看", "<p>粘贴响应头文本即可格式化并逐项解释，快速定位配置错误。</p>"),
        ],
        "example": {
            "caption": "典型响应头",
            "code": 'HTTP/1.1 200 OK\nContent-Type: application/json; charset=utf-8\nCache-Control: max-age=3600\nAccess-Control-Allow-Origin: *\nSet-Cookie: sid=abc; Path=/; HttpOnly',
        },
        "faqs": [
            ("Cache-Control: no-store 和 no-cache 区别？", "no-store 禁止缓存任何副本；no-cache 允许缓存但使用前需向源站验证。"),
            ("CORS 报错是谁的责任？", "由服务端响应头决定是否允许跨域；前端无法单方面绕过，需要对方配置 Access-Control-Allow-*。"),
            ("SameSite=Strict 会影响什么？", "它限制第三方上下文携带 Cookie，跨站跳转可能不带会话，需按业务选 Lax/None。"),
        ],
    },
    {
        "slug": "ip-calculator", "cluster": "dev",
        "title": "IP 与子网计算（CIDR）",
        "desc": "IPv4 地址结构、子网掩码与 CIDR，如何算网络地址/广播地址/可用主机数。",
        "primary": ("ip-calculator", "it", "IP 计算器"),
        "related": [("http-response-headers", "it", "HTTP 响应头查看"), ("jwt-debugger", "it", "JWT 调试器")],
        "sections": [
            ("IPv4 与子网基础", "<p>IPv4 是 32 位地址，常写成 4 段十进制。子网掩码/CIDR（如 /24）决定前多少位是网络号、剩下是主机号。</p>"),
            ("关键产出", "<p><b>网络地址</b>=IP 与掩码按位与；<b>广播地址</b>=主机位全 1；<b>可用主机</b>=2^主机位 - 2（去掉网络与广播）。</p>"),
            ("在 ToolBox 中计算", "<p>输入 <code>192.168.1.10/24</code> 即可看到网络地址、广播地址、可用主机范围与数量。</p>"),
        ],
        "example": {
            "caption": "192.168.1.10/24 计算结果",
            "code": '网络地址 : 192.168.1.0\n广播地址 : 192.168.1.255\n可用主机 : 192.168.1.1 ~ 192.168.1.254 (共 254)',
        },
        "faqs": [
            ("/24 为什么是 254 个可用地址？", "主机位 8 bit 共 256 个，去掉网络地址和广播地址剩 254。"),
            ("CIDR 和子网掩码如何换算？", "/24 即掩码 255.255.255.0；前缀长度就是掩码中 1 的个数。"),
            ("IPv6 也能这样算吗？", "IPv6 地址空间巨大且划分方式不同，本工具聚焦 IPv4/CIDR。"),
        ],
    },
    # ---------- 财务 ----------
    {
        "slug": "npv-calculator", "cluster": "finance",
        "title": "NPV 净现值计算与投资决策",
        "desc": "什么是 NPV 与折现率，如何对一系列现金流折现并据此做投资判断，附 ToolBox 用法。",
        "primary": ("npv-calculator", "finance", "NPV 净现值计算器"),
        "related": [("compound-interest", "finance", "复利计算器"), ("roi-calculator", "finance", "ROI 计算器")],
        "sections": [
            ("什么是 NPV", "<p>净现值（Net Present Value）把未来各期现金流按折现率折算到今天再求和，减去初始投入。<b>NPV>0</b> 通常表示项目可行。</p>"),
            ("折现率的意义", "<p>折现率反映资金成本与风险，越高说明对未来收益越「打折」；同一现金流在高折现率下 NPV 更低。</p>"),
            ("在 ToolBox 中计算", "<p>输入各期现金流（首期常为负，代表投入）与折现率，结果给出 NPV 与每期现值，便于横向比较方案。</p>"),
        ],
        "example": {
            "caption": "现金流 -1000, 300, 400, 500 @10%",
            "code": '现值 = -1000 + 300/1.1 + 400/1.1² + 500/1.1³\n    ≈ -1000 + 272.7 + 330.6 + 375.7\nNPV ≈  -21.0  (折现率偏高时不划算)',
        },
        "faqs": [
            ("NPV 和 IRR 哪个更直观？", "NPV 给绝对金额，IRR 给等效收益率；决策时两者结合看更稳。"),
            ("折现率一般取多少？", "可用资本成本、目标回报率或行业基准，没有统一值，需明确假设。"),
            ("NPV<0 就一定不做吗？", "财务上通常不划算，但战略/合规等无形收益需另行权衡。"),
        ],
    },
    {
        "slug": "currency-symbol", "cluster": "finance",
        "title": "货币符号与币种查询",
        "desc": "常见货币符号、ISO 4217 代码与地区差异，如何用 ToolBox 查询币种信息。",
        "primary": ("currency-symbol", "finance", "货币符号查询"),
        "related": [("compound-interest", "finance", "复利计算器"), ("npv-calculator", "finance", "NPV 计算器")],
        "sections": [
            ("符号与代码", "<p>¥(人民币/CNY)、$(美元/USD)、€(欧元/EUR)、£(英镑/GBP) 是常用符号；ISO 4217 用三字母代码唯一标识币种，避免符号歧义（如 $ 多国共用）。</p>"),
            ("地区差异", "<p>同一符号在不同地区含义不同（如 ¥ 也用于日元 JPY），跨市场沟通应优先用代码 CNY/JPY。</p>"),
            ("在 ToolBox 中查询", "<p>输入符号或代码即可看到对应币种名称与代码，方便对账与文案书写。</p>"),
        ],
        "example": {
            "caption": "查询示例",
            "code": '符号: ¥  →  代码: CNY (人民币)\n符号: $  →  代码: USD (美元, 多国共用需谨慎)',
        },
        "faqs": [
            ("¥ 到底代表人民币还是日元？", "两者都用 ¥；正式场景用 CNY/JPY 区分最稳妥。"),
            ("ISO 4217 有什么用？", "它给每个币种唯一三字母代码，是跨境支付与系统的标准写法。"),
            ("货币符号能直接换算金额吗？", "符号只表示币种，换算需汇率；本工具负责识别而非汇率计算。"),
        ],
    },
    {
        "slug": "roi-calculator", "cluster": "finance",
        "title": "ROI 投资回报率计算",
        "desc": "ROI 公式、与 NPV/IRR 的区别，如何用 ToolBox 快速评估一项投入的回报。",
        "primary": ("roi-calculator", "finance", "ROI 计算器"),
        "related": [("npv-calculator", "finance", "NPV 计算器"), ("compound-interest", "finance", "复利计算器")],
        "sections": [
            ("ROI 公式", "<p>ROI = (收益 − 成本) / 成本 × 100%。它简单直观，衡量「投入一元赚回多少」。</p>"),
            ("ROI 的局限", "<p>ROI 不考虑时间维度，一年赚 50% 和十年赚 50% 的 ROI 相同却天差地别；因此常配合 NPV/IRR 使用。</p>"),
            ("在 ToolBox 中计算", "<p>填入总收益与总成本即得 ROI 百分比；多期项目建议再折算时间价值。</p>"),
        ],
        "example": {
            "caption": "收益 15000、成本 10000",
            "code": 'ROI = (15000 - 10000) / 10000 × 100% = 50%',
        },
        "faqs": [
            ("ROI 为负说明什么？", "说明收益低于成本，即亏损；绝对值越大亏损越严重。"),
            ("ROI 和净利率一样吗？", "不一样。净利率是会计口径（含税费等），ROI 是投入产出比，定义更灵活。"),
            ("为什么 ROI 高也可能不投？", "若回收周期过长或风险高，时间价值与风险会削弱高 ROI 的吸引力。"),
        ],
    },
    # ---------- 健康 ----------
    {
        "slug": "blood-pressure-classifier", "cluster": "health",
        "title": "血压分级与家庭自测解读",
        "desc": "收缩压/舒张压怎么读，常用分级标准，如何用 ToolBox 分类并理解注意事项。",
        "primary": ("blood-pressure-classifier", "health", "血压分级器"),
        "related": [("bmi-calculator", "health", "BMI 计算器"), ("calorie-calculator", "food", "热量需求计算器")],
        "sections": [
            ("两个数字的含义", "<p>血压写作「收缩压/舒张压」(如 120/80 mmHg)。收缩压是心脏收缩时的压力，舒张压是心脏舒张时的压力。</p>"),
            ("常用分级（参考）", "<p>正常 <120/80；偏高 120-139/80-89；高血压 1 级 ≥140/90；2 级更高。具体以医嘱为准。</p>"),
            ("在 ToolBox 中分类", "<p>输入两个数值即可看到分级与区间提示；结果仅作参考，不替代诊断。</p>"),
            ("测量注意", "<p>单次测量受情绪、运动、袖带位置影响，应静坐 5 分钟、多次测量取平均，并固定时段记录。</p>"),
        ],
        "example": {
            "caption": "138/88 mmHg",
            "code": '收缩压 138 → 偏高区间\n舒张压 88  → 偏高区间\n提示: 属于「血压偏高」，建议监测并记录趋势',
        },
        "faqs": [
            ("在家量的和医院不一样正常吗？", "白大衣高血压、紧张、姿势都会影响；家庭自测取多次平均更接近日常水平。"),
            ("电子血压计准吗？", "合规电子计日常够用，但需定期校准、正确佩戴袖带。"),
            ("结果能代替医生诊断吗？", "不能。本工具只做分级参考，异常请就医。"),
        ],
    },
    {
        "slug": "calorie-calculator", "cluster": "health",
        "title": "每日热量需求估算（TDEE）",
        "desc": "BMR、活动系数与 TDEE 的关系，如何估算维持/减脂/增肌的热量区间。",
        "primary": ("calorie-calculator", "food", "热量需求计算器"),
        "related": [("bmi-calculator", "health", "BMI 计算器"), ("blood-pressure-classifier", "health", "血压分级器")],
        "sections": [
            ("BMR 是基础", "<p>基础代谢率（BMR）是静止状态下维持生命所需热量，常用 Mifflin-St Jeor 公式，由性别、年龄、身高、体重算出。</p>"),
            ("活动系数得 TDEE", "<p>用 BMR × 活动系数（久坐约 1.2，高强度约 1.7+）得到每日总消耗 TDEE，即「吃持平」的热量。</p>"),
            ("在 ToolBox 中估算", "<p>填基本信息与活动水平，结果给出维持热量，并标注约 15% 上下的减脂/增肌区间。</p>"),
        ],
        "example": {
            "caption": "30 岁女性 165cm/60kg 轻度活动",
            "code": 'BMR   ≈ 1326 kcal\nTDEE  ≈ 1591 kcal (×1.2)\n减脂  ≈ 1350 kcal\n增肌  ≈ 1800 kcal',
        },
        "faqs": [
            ("减脂一定要低于 TDEE 吗？", "通常制造约 300-500 kcal 缺口较稳妥，过猛易掉肌肉且难坚持。"),
            ("为什么算出来和 App 差很多？", "公式与活动系数假设不同；把它当起点，再按体重变化微调。"),
            ("TDEE 是固定值吗？", "会随体重、肌肉量、年龄变化，建议定期重算。"),
        ],
    },
    {
        "slug": "blood-sugar-converter", "cluster": "health",
        "title": "血糖单位换算（mg/dL ↔ mmol/L）",
        "desc": "两种血糖单位的区别、换算系数，如何用 ToolBox 互转并理解参考区间差异。",
        "primary": ("blood-sugar-converter", "health", "血糖单位换算器"),
        "related": [("bmi-calculator", "health", "BMI 计算器"), ("calorie-calculator", "food", "热量需求计算器")],
        "sections": [
            ("两种单位", "<p>中国常用 mmol/L，部分国家用 mg/dL。两者相差约 18.0182 倍：<b>mmol/L = mg/dL ÷ 18.0182</b>。</p>"),
            ("参考区间因单位而异", "<p>空腹正常约 3.9–6.1 mmol/L，对应约 70–110 mg/dL；比较时务必先统一单位。</p>"),
            ("在 ToolBox 中换算", "<p>输入数值与来源单位，一键得到目标单位结果，避免手工除法出错。</p>"),
        ],
        "example": {
            "caption": "100 mg/dL 换算",
            "code": '100 mg/dL ÷ 18.0182 ≈ 5.55 mmol/L',
        },
        "faqs": [
            ("哪个单位更准？", "只是表示方式不同，数值需配合单位解读，不存在谁更准。"),
            ("空腹和餐后标准一样吗？", "不一样。餐后 2 小时上限通常更高，请以检测项目要求为准。"),
            ("换算能代替血糖仪吗？", "不能。本工具只做单位换算，数值仍以测量设备为准。"),
        ],
    },
]


def toold_url(t):
    slug, ind, name = t
    return "/tools/%s/%s.html" % (ind, slug)


def render_guide(g):
    slug = g["slug"]
    title = g["title"]
    desc = g["desc"]
    url = "%s/guides/%s-guide.html" % (SITE, slug)
    cluster = CLUSTERS[g["cluster"]]
    cluster_url = "%s/guides/cluster-%s.html" % (SITE, g["cluster"])

    # TOC + sections
    toc = []
    body = []
    for i, (h2, html) in enumerate(g["sections"]):
        aid = "s%d" % i
        toc.append('<li><a href="#%s">%s</a></li>' % (aid, h2))
        body.append('<h2 id="%s">%s</h2>\n%s' % (aid, h2, html))

    # related tools block
    rel = [g["primary"]] + g["related"]
    rel_html = "\n".join(
        '<a class="tool-chip" href="%s">%s</a>' % (toold_url(t), t[2]) for t in rel
    )

    # FAQ
    faq_qa = "\n".join("<dt>%s</dt><dd>%s</dd>" % (q, a) for q, a in g["faqs"])
    faq_ld = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": q,
             "acceptedAnswer": {"@type": "Answer", "text": a}}
            for q, a in g["faqs"]
        ],
    }

    ld = {
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": title,
        "description": desc,
        "author": {"@type": "Organization", "name": "ToolBox"},
        "datePublished": TODAY,
        "dateModified": TODAY,
        "mainEntityOfPage": {"@type": "WebPage", "@id": url},
    }
    breadcrumb = {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "ToolBox", "item": SITE + "/"},
            {"@type": "ListItem", "position": 2, "name": "使用指南", "item": SITE + "/#guides"},
            {"@type": "ListItem", "position": 3, "name": cluster["name"], "item": cluster_url},
            {"@type": "ListItem", "position": 4, "name": title, "item": url},
        ],
    }

    html = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title} - ToolBox</title>
<meta name="description" content="{desc}">
<meta property="og:title" content="{title} - ToolBox">
<meta property="og:type" content="article">
<meta property="og:site_name" content="ToolBox">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{site}/og-image.png">
<meta name="twitter:card" content="summary_large_image">
<meta property="og:description" content="{desc}">
<meta name="twitter:title" content="{title} - ToolBox">
<meta name="twitter:description" content="{desc}">
<meta name="twitter:image" content="{site}/og-image.png">
<meta name="twitter:image:alt" content="ToolBox - 免费在线工具与使用指南">
<link rel="canonical" href="{url}">
<script type="application/ld+json">{article_ld}</script>
<script type="application/ld+json">{breadcrumb_ld}</script>
<script type="application/ld+json">{faq_ld}</script>
<style>
:root{{--primary:#FF6B35;--text:#1F2937;--muted:#6B7280;--border:#E5E7EB;--bg:#FFFAF7;}}
*{{box-sizing:border-box;}}
body{{margin:0;font-family:"Noto Sans SC","Plus Jakarta Sans",system-ui,sans-serif;color:var(--text);background:var(--bg);line-height:1.75;}}
header{{padding:18px 20px;border-bottom:1px solid var(--border);background:#fff;}}
.breadcrumb a{{color:var(--primary);text-decoration:none;margin-right:6px;}}
.breadcrumb a:hover{{text-decoration:underline;}}
main{{max-width:820px;margin:0 auto;padding:28px 20px 60px;}}
h1{{font-size:28px;margin:0 0 8px;}}
.lead{{font-size:16px;color:var(--muted);margin:0 0 22px;}}
h2{{font-size:20px;margin:28px 0 10px;color:var(--primary);}}
.toc{{background:#fff;border:1px solid var(--border);border-radius:14px;padding:14px 18px;margin:18px 0;}}
.toc ul{{margin:0;padding-left:20px;}}
.toc a{{color:var(--text);text-decoration:none;}}
.toc a:hover{{color:var(--primary);}}
pre{{background:#0f172a;color:#e2e8f0;padding:14px 16px;border-radius:12px;overflow:auto;font-size:13px;line-height:1.6;}}
code{{background:#fff3e0;padding:1px 5px;border-radius:5px;font-size:.92em;}}
pre code{{background:none;padding:0;}}
.related{{margin-top:26px;padding:16px;background:#fff;border:1px solid var(--border);border-radius:14px;}}
.related h3{{margin:0 0 10px;font-size:16px;color:var(--text);}}
.tool-chip{{display:inline-block;margin:4px 6px 4px 0;padding:6px 12px;border:1px solid var(--border);border-radius:999px;color:var(--primary);text-decoration:none;font-size:14px;}}
.tool-chip:hover{{background:var(--primary);color:#fff;}}
.faq{{margin-top:26px;}}
.faq dt{{font-weight:700;margin-top:14px;}}
.faq dd{{margin:4px 0 0;color:var(--muted);}}
.back{{margin-top:30px;padding:16px;background:#fff;border:1px solid var(--border);border-radius:14px;}}
.back a{{color:var(--primary);font-weight:700;text-decoration:none;}}
footer{{text-align:center;color:var(--muted);font-size:13px;padding:24px;border-top:1px solid var(--border);}}
</style>
</head>
<body>
<header><nav class="breadcrumb"><a href="{site}/">ToolBox</a> / <a href="{site}/#guides">使用指南</a> / <a href="{cluster_url}">{cluster_name}</a> / <span>{title}</span></nav></header>
<main>
<h1>{title}</h1>
<p class="lead">{desc}</p>
<div class="toc"><strong>目录</strong><ul>{toc}</ul></div>
{body}
<div class="related"><h3>相关工具</h3>{rel_html}</div>
<div class="faq"><h2>常见问题</h2><dl>{faq_qa}</dl></div>
<div class="back"><a href="{cluster_url}">← 返回「{cluster_name}」内容集群</a></div>
</main>
<footer>© 2026 ToolBox · 纯前端工具，数据不出浏览器</footer>
</body>
</html>
""".format(
        title=title, desc=desc, url=url, site=SITE,
        article_ld=json.dumps(ld, ensure_ascii=False),
        breadcrumb_ld=json.dumps(breadcrumb, ensure_ascii=False),
        faq_ld=json.dumps(faq_ld, ensure_ascii=False),
        cluster_url=cluster_url, cluster_name=cluster["name"],
        toc="".join(toc), body="\n".join(body), rel_html=rel_html,
        faq_qa=faq_qa,
    )
    return html


def render_cluster(key):
    c = CLUSTERS[key]
    url = "%s/guides/cluster-%s.html" % (SITE, key)
    guides_in = [g for g in GUIDES if g["cluster"] == key]
    guide_cards = "\n".join(
        '<a class="g-card" href="{site}/guides/{slug}-guide.html"><b>{title}</b><span>{desc}</span></a>'
        .format(site=SITE, slug=g["slug"], title=g["title"], desc=g["desc"])
        for g in guides_in
    )
    # related tools: union of primary+related across guides in cluster
    tools = []
    seen = set()
    for g in guides_in:
        for t in [g["primary"]] + g["related"]:
            if t[0] not in seen:
                seen.add(t[0])
                tools.append(t)
    tool_chips = "\n".join(
        '<a class="tool-chip" href="{u}">{n}</a>'.format(u=toold_url(t), n=t[2]) for t in tools
    )
    breadcrumb = {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "ToolBox", "item": SITE + "/"},
            {"@type": "ListItem", "position": 2, "name": "使用指南", "item": SITE + "/#guides"},
            {"@type": "ListItem", "position": 3, "name": c["name"] + "内容集群", "item": url},
        ],
    }
    ld = {
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": c["name"] + "内容集群",
        "description": c["intro"],
        "author": {"@type": "Organization", "name": "ToolBox"},
        "datePublished": TODAY,
        "dateModified": TODAY,
    }
    html = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{name}内容集群 - ToolBox</title>
<meta name="description" content="{intro}">
<meta property="og:title" content="{name}内容集群 - ToolBox">
<meta property="og:type" content="article">
<meta property="og:site_name" content="ToolBox">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{site}/og-image.png">
<link rel="canonical" href="{url}">
<script type="application/ld+json">{article_ld}</script>
<script type="application/ld+json">{breadcrumb_ld}</script>
<style>
:root{{--primary:#FF6B35;--text:#1F2937;--muted:#6B7280;--border:#E5E7EB;--bg:#FFFAF7;}}
*{{box-sizing:border-box;}}
body{{margin:0;font-family:"Noto Sans SC","Plus Jakarta Sans",system-ui,sans-serif;color:var(--text);background:var(--bg);line-height:1.75;}}
header{{padding:18px 20px;border-bottom:1px solid var(--border);background:#fff;}}
.breadcrumb a{{color:var(--primary);text-decoration:none;margin-right:6px;}}
main{{max-width:860px;margin:0 auto;padding:28px 20px 60px;}}
h1{{font-size:28px;margin:0 0 8px;}}
.lead{{font-size:16px;color:var(--muted);margin:0 0 22px;}}
.grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(240px,1fr));gap:14px;margin:18px 0;}}
.g-card{{display:flex;flex-direction:column;gap:6px;padding:16px;border:1px solid var(--border);border-radius:14px;background:#fff;text-decoration:none;color:var(--text);}}
.g-card:hover{{border-color:var(--primary);}}
.g-card b{{color:var(--primary);font-size:16px;}}
.g-card span{{color:var(--muted);font-size:14px;}}
.related{{margin-top:26px;padding:16px;background:#fff;border:1px solid var(--border);border-radius:14px;}}
.related h3{{margin:0 0 10px;font-size:16px;}}
.tool-chip{{display:inline-block;margin:4px 6px 4px 0;padding:6px 12px;border:1px solid var(--border);border-radius:999px;color:var(--primary);text-decoration:none;font-size:14px;}}
.tool-chip:hover{{background:var(--primary);color:#fff;}}
footer{{text-align:center;color:var(--muted);font-size:13px;padding:24px;border-top:1px solid var(--border);}}
</style>
</head>
<body>
<header><nav class="breadcrumb"><a href="{site}/">ToolBox</a> / <a href="{site}/#guides">使用指南</a> / <span>{name}</span></nav></header>
<main>
<h1>{name} 内容集群</h1>
<p class="lead">{intro}</p>
<div class="grid">{guide_cards}</div>
<div class="related"><h3>相关工具</h3>{tool_chips}</div>
</main>
<footer>© 2026 ToolBox · 纯前端工具，数据不出浏览器</footer>
</body>
</html>
""".format(name=c["name"], intro=c["intro"], url=url, site=SITE,
           article_ld=json.dumps(ld, ensure_ascii=False),
           breadcrumb_ld=json.dumps(breadcrumb, ensure_ascii=False),
           guide_cards=guide_cards, tool_chips=tool_chips)
    return html


def main():
    os.makedirs(GUIDES_DIR, exist_ok=True)
    written = []
    for g in GUIDES:
        fn = os.path.join(GUIDES_DIR, "%s-guide.html" % g["slug"])
        with open(fn, "w", encoding="utf-8") as f:
            f.write(render_guide(g))
        written.append(fn)
    for key in CLUSTERS:
        fn = os.path.join(GUIDES_DIR, "cluster-%s.html" % key)
        with open(fn, "w", encoding="utf-8") as f:
            f.write(render_cluster(key))
        written.append(fn)

    # 追加 guides.json 映射（工具页 → 指南，反向内链）
    gj = os.path.join(ROOT, "json", "guides.json")
    data = []
    if os.path.exists(gj):
        try:
            data = json.load(open(gj, encoding="utf-8"))
        except Exception:
            data = []
    existing = {(d.get("tool"), d.get("guide")) for d in data}
    added = 0
    for g in GUIDES:
        slug = g["slug"]
        tool = "%s.html" % g["primary"][0]
        guide = "../../guides/%s-guide.html" % slug
        if (tool, guide) not in existing:
            data.append({"tool": tool, "guide": guide, "title": g["title"]})
            existing.add((tool, guide))
            added += 1
    json.dump(data, open(gj, "w", encoding="utf-8"), ensure_ascii=False, indent=2)

    print("生成指南 %d 篇 + 集群入口 %d 个，guides.json 新增 %d 条映射" % (len(GUIDES), len(CLUSTERS), added))
    print("总计写入文件 %d 个" % len(written))


if __name__ == "__main__":
    main()
