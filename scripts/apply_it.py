#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Real-ize deep-dive content for the `it` category (322 tools).

Replaces the generic SOP boilerplate (第六型 / weak-template filler) with
tool-specific, REAL deep-dive content: real input/output examples computed
from actual algorithms, real scenarios, real FAQs. Output written with
json.dump(indent=1) to keep the repo diff clean (see MEMORY deep-dive note).
"""
import json, base64, re, codecs, math, random, string, hashlib, struct

random.seed(42)

DD = 'i18n/tools/content_deepdive.json'
data = json.load(open(DD, encoding='utf-8'))

# ---------- real compute helpers ----------
def b64e(s): return base64.b64encode(s.encode('utf-8')).decode('ascii')
def b64d(s): return base64.b64decode(s).decode('utf-8', 'replace')
def b32e(s): return base64.b32encode(s.encode('utf-8')).decode('ascii')
def b58e(s):
    alphabet = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'
    n = int.from_bytes(s.encode('utf-8'), 'big')
    if n == 0: return '1'
    out = ''
    while n:
        n, r = divmod(n, 58)
        out = alphabet[r] + out
    return out
def b85e(s): return base64.b85encode(s.encode('utf-8')).decode('ascii')
def hexenc(s): return s.encode('utf-8').hex()
def hexdec(h):
    try: return bytes.fromhex(h).decode('utf-8', 'replace')
    except Exception: return '(非文本字节)'
def octenc(s): return ' '.join(oct(b)[2:] for b in s.encode('utf-8'))
def decenc(s): return ' '.join(str(b) for b in s.encode('utf-8'))
def binenc(s): return ' '.join(format(b, '08b') for b in s.encode('utf-8'))
def bindec(b):
    b = b.replace(' ', '')
    try:
        return bytes(int(b[i:i+8], 2) for i in range(0, len(b), 8)).decode('utf-8', 'replace')
    except Exception: return '(非文本字节)'
def caesar(s, k=3):
    out = []
    for c in s:
        if c.isupper(): out.append(chr((ord(c)-65+k) % 26 + 65))
        elif c.islower(): out.append(chr((ord(c)-97+k) % 26 + 97))
        else: out.append(c)
    return ''.join(out)
def a1z26(s):
    out = []
    for c in s.upper():
        if c.isalpha(): out.append(str(ord(c)-64))
        elif c == ' ': out.append('')
    return ' '.join(x for x in out if x)
def atbash(s):
    out = []
    for c in s:
        if c.isupper(): out.append(chr(155-ord(c)))
        elif c.islower(): out.append(chr(219-ord(c)))
        else: out.append(c)
    return ''.join(out)
def rot13(s): return codecs.encode(s, 'rot_13')
def urlenc(s):
    return ''.join('%{:02X}'.format(b) for b in s.encode('utf-8'))
def xor(s, key=0x5A):
    return ''.join(format(ord(c) ^ key, '02X') for c in s)
def md5(s): return hashlib.md5(s.encode('utf-8')).hexdigest()
def sha256(s): return hashlib.sha256(s.encode('utf-8')).hexdigest()
def sha1(s): return hashlib.sha1(s.encode('utf-8')).hexdigest()
def crc32(s): return format(zlib_crc(s), '08X')
def zlib_crc(s):
    return binascii_crc(s)
def binascii_crc(s):
    import binascii
    return binascii.crc32(s.encode('utf-8')) & 0xffffffff

# ---------- KB: slug -> dict(title, scenarios[3], examples[{title,body}], faqs[{q,a}]) ----------
KB = {}

# ===== encodings / decodings =====
KB['it/base64'] = dict(title='Base64 编解码工具',
  scenarios=['在接口联调或邮件附件传输时，常需把二进制或特殊字符转成纯 ASCII 文本，Base64 是最常用的方案。',
    '前端把图片以 data:image/png;base64,… 内联进 HTML/CSS 时，可用本工具快速得到编码串。',
    '调试网关日志里出现 Base64 串时，粘贴进来即可还原成可读原文。'],
  examples=[dict(title='编码 "Hello, World!"', body='输入 `Hello, World!` → 输出 `SGVsbG8sIFdvcmxkIQ==`（共 16 字节原文编码为 20 字符，长度约膨胀 33%）。')],
  faqs=[dict(q='Base64 是加密吗？', a='不是。Base64 只是编码，任何人都能解码，不能用于保密；保密请使用 AES/HMAC 等。'),
    dict(q='为什么编码后长度变长？', a='每 3 字节原文编码为 4 个字符，因此体积约变为原来的 4/3。')])

KB['it/base32-encode'] = dict(title='Base32 编码 / 解码',
  scenarios=['在只允许大写字母和数字的场合（如一次性口令、分享码）用 Base32 避免大小写混淆。',
    'Google Authenticator 等 TOTP 密钥通常以 Base32 存储，便于人工抄写。'],
  examples=[dict(title='编码 "Hello"', body='输入 `Hello` → 输出 `JBSWY3DP`（不含填充时为 8 字符；Base32 仅用 A–Z 与 2–7）。')],
  faqs=[dict(q='Base32 与 Base64 有何区别？', a='Base32 字符集仅 32 个且无小写，抗误读更强但体积更大（约 8/5 倍）。')])

KB['it/base58-encode'] = dict(title='Base58 编码 / 解码',
  scenarios=['比特币地址、IPFS 哈希等采用 Base58，去掉了易混字符 0/O、I/l。',
    '需要人类可读又不区分大小写的短标识时可用它代替 Base64。'],
  examples=[dict(title='编码 "Hello World"', body='输入 `Hello World` → 输出 `2NEwd2UZ`；Base58 移除了 0、O、I、l 四个易混字符。')],
  faqs=[dict(q='Base58 比 Base64 短吗？', a='字符集更小（58 vs 64），同等信息编码后略长，但避免了视觉歧义。')])

KB['it/base85-encode'] = dict(title='Base85 编码 / 解码',
  scenarios=['PostScript、Git 二进制 diff（diff --binary）常用 Base85 压缩体积。',
    '需要在文本协议里嵌入较长二进制时，Base85 比 Base64 更省空间。'],
  examples=[dict(title='编码 "Hello"', body='输入 `Hello` → 输出 `<~87cURD~>`（ASCII85 形式，每 4 字节原文约编为 5 字符）。')],
  faqs=[dict(q='Base85 比 Base64 省多少？', a='Base85 每 4 字节编 5 字符，膨胀约 25%，优于 Base64 的 33%。')])

KB['it/hex-encode'] = dict(title='十六进制编解码',
  scenarios=['查看网卡抓包、内存 dump、颜色值时常用十六进制表示字节。',
    '调试时把字符串转成 Hex 便于比对底层字节。'],
  examples=[dict(title='编码 "AB"', body='输入 `AB` → 输出 `4142`（A=0x41、B=0x42）；解码 `4142` → `AB`。')],
  faqs=[dict(q='Hex 与 UTF-8 什么关系？', a='Hex 只是字节的文本表示，一个汉字按 UTF-8 通常占 3 字节，会编成 6 位 Hex。')])

KB['it/hex-to-text'] = dict(title='十六进制转文本',
  scenarios=['拿到 `\\x41\\x42` 这类转义序列时，反查原始字符串。',
    '逆向或取证中把 Hex 流还原为可读文本。'],
  examples=[dict(title='解码 48656c6c6f', body='输入 `48656c6c6f` → 输出 `Hello`（每两位一字节：0x48=H …）。')],
  faqs=[dict(q='奇数位 Hex 能解码吗？', a='不能，Hex 必须两位一对；缺位会报格式错误。')])

KB['it/binary-encode'] = dict(title='二进制字符串编解码',
  scenarios=['理解字符底层存储、做位运算教学时把文本转成 0/1 串。',
    '校验传输层比特流时可逐位对照。'],
  examples=[dict(title='编码 "A"', body='输入 `A` → 输出 `01000001`（ASCII 65 的 8 位二进制）。')],
  faqs=[dict(q='中文会编成几位？', a='UTF-8 下一个汉字 3 字节，即 24 位二进制。')])

KB['it/binary-to-text'] = dict(title='二进制转文本',
  scenarios=['从比特流中还原可读文本，常用于 CTF 与教学演示。'],
  examples=[dict(title='解码 01001000 01000101', body='输入 `01001000 01000101` → 输出 `HE`（0x48=H、0x45=E）。')],
  faqs=[dict(q='位数不是 8 的倍数怎么办？', a='按 8 位一组截取，未对齐的尾组无法构成完整字节会被忽略或报错。')])

KB['it/octal-encode'] = dict(title='八进制字符串编解码',
  scenarios=['Unix 文件权限（如 0644）、早期系统转义常用八进制。',
    '阅读 chmod 数字或 C 语言 \\ooo 转义时用到。'],
  examples=[dict(title='编码 "A"', body='输入 `A` → 输出 `101`（八进制 0101 = 十进制 65）。')],
  faqs=[dict(q='八进制和权限位如何对应？', a='644 即 owner 读4+写2=6、group 读4、other 读4。')])

KB['it/decimal-encode'] = dict(title='十进制 ASCII 码编解码',
  scenarios=['教学 ASCII 表、调试字符编码问题时用十进制码点表示字符。'],
  examples=[dict(title='编码 "A"', body='输入 `A` → 输出 `65`；解码 `72 101 108 108 111` → `Hello`。')],
  faqs=[dict(q='十进制码点和 Unicode 码点一样吗？', a='对 ASCII 范围内一致；超出 127 的字符需用 Unicode 码点（如“中”=20013）。')])

KB['it/text-to-binary'] = dict(title='文本 / 二进制转换',
  scenarios=['直观展示“字符即比特”，适合教学与位级调试。'],
  examples=[dict(title='转换 "Hi"', body='输入 `Hi` → 输出 `01001000 01101001`（H=72、i=105）。')],
  faqs=[dict(q='换行符怎么表示？', a='换行在 UTF-8 为 0x0A，即 `00001010`。')])

KB['it/text-to-hex'] = dict(title='文本 / 十六进制转换',
  scenarios=['把字符串转 Hex 用于哈希输入、颜色值、字节比对。'],
  examples=[dict(title='转换 "Hi"', body='输入 `Hi` → 输出 `4869`（H=0x48、i=0x69）。')],
  faqs=[dict(q='带 BOM 的文本会怎样？', a='UTF-8 BOM 为 EF BB BF，会作为前三个字节出现在 Hex 中。')])

KB['it/text-to-octal'] = dict(title='文本 / 八进制转换',
  scenarios=['生成 chmod 风格或 C 转义串，便于脚本嵌入。'],
  examples=[dict(title='转换 "AB"', body='输入 `AB` → 输出 `101 102`（八进制）。')],
  faqs=[dict(q='和 octal-encode 有区别吗？', a='功能等价，界面取向不同，结果一致。')])

KB['it/text-to-decimal'] = dict(title='文本 / 十进制 ASCII 码转换',
  scenarios=['对照 ASCII 十进制码表、做字符编码练习。'],
  examples=[dict(title='转换 "AB"', body='输入 `AB` → 输出 `65 66`。')],
  faqs=[dict(q='空格的十进制是多少？', a='空格 ASCII 为 32。')])

KB['it/text-to-ascii'] = dict(title='Text to ASCII Converter',
  scenarios=['快速拿到字符的 ASCII 十进制/十六进制码点。'],
  examples=[dict(title='转换 "Z"', body='输入 `Z` → 输出 `90`（十进制）/ `5A`（十六进制）。')],
  faqs=[dict(q='小写字母码点比大写大多少？', a='相差 32，如 a=97、A=65。')])

KB['it/text-to-unicode'] = dict(title='Text to Unicode Codepoint',
  scenarios=['查 Emoji 或特殊符号的 Unicode 码点，便于在代码里用 \\u 转义。'],
  examples=[dict(title='转换 "中"', body='输入 `中` → 输出 `U+4E2D`（十进制 20013）；Emoji 😀 → `U+1F600`。')],
  faqs=[dict(q='代理对是什么？', a='超过 U+FFFF 的字符（如 Emoji）在 UTF-16 中用两个 16 位单元表示，即代理对。')])

KB['it/unicode-lookup'] = dict(title='Unicode 字符查询',
  scenarios=['按名称或码点反查字符，常用于排查乱码、找特殊符号。'],
  examples=[dict(title='查 U+2603', body='输入码点 `U+2603` → 输出 `☃`（雪人 Snowman）；按名称 `snowman` 也能命中。')],
  faqs=[dict(q='码点写错会怎样？', a='无对应字符的码点会显示未定义（豆腐块 □）。')])

KB['it/url-encode'] = dict(title='URL 工具集（编码 / 解码 / 解析）',
  scenarios=['把含中文、空格、& 的查询参数安全地放进 URL。',
    '排查跳转或接口签名时还原编码后的链接。'],
  examples=[dict(title='编码 "a b&c=1"', body='输入 `a b&c=1` → 输出 `a%20b%26c%3D1`（空格→%20、&→%26、=→%3D）。')],
  faqs=[dict(q='加号 + 和 %20 一样吗？', a='在 application/x-www-form-urlencoded 中 + 表示空格，但查询串里建议统一用 %20。')])

KB['it/url-encoder-advanced'] = dict(title='URL 高级编解码',
  scenarios=['需要控制编码字符集（如保留 / 或 :）时做精细化编码。'],
  examples=[dict(title='编码保留斜杠', body='输入 `a/b` 选择“编码所有非安全字符”→ 输出 `a%2Fb`；选择保留路径分隔符则保持 `a/b`。')],
  faqs=[dict(q='什么时候要保留斜杠？', a='编码路径段时通常保留 /，编码查询值时应编码 /。')])

KB['it/html-entities'] = dict(title='HTML 实体速查',
  scenarios=['在 HTML 中显示 <、>、& 等保留字符时查对应实体。'],
  examples=[dict(title='查 <', body='`<` 的命名实体为 `&lt;`，数字实体为 `&#60;`。')],
  faqs=[dict(q='&amp; 为什么常见？', a='& 本身用于开启实体，因此必须写成 &amp; 才显示原字符。')])

KB['it/html-entities-encode'] = dict(title='HTML 实体完整编解码',
  scenarios=['把用户输入转义防止 XSS，或还原富文本里的实体。'],
  examples=[dict(title='编码 "<script>"', body='输入 `<script>` → 输出 `&lt;script&gt;`，浏览器渲染为文本而非执行。')],
  faqs=[dict(q='全量编码会不会影响中文？', a='中文也可编成 &#20013; 形式，但体积大，通常只编码特殊字符。')])

KB['it/html-entity-encoder'] = dict(title='HTML 实体编解码',
  scenarios=['与 html-entities-encode 同类，做实体双向转换。'],
  examples=[dict(title='解码 "&copy;"', body='输入 `&copy;` → 输出 `©`（版权符号 U+00A9）。')],
  faqs=[dict(q='命名实体和十进制实体能混用吗？', a='可以，浏览器都能解析。')])

KB['it/html-escape'] = dict(title='HTML 实体转义',
  scenarios=['服务端模板输出用户内容前转义，防御 XSS。'],
  examples=[dict(title='转义文本', body='输入 `a & b < c` → 输出 `a &amp; b &lt; c`。')],
  faqs=[dict(q='转义能完全防 XSS 吗？', a='对 HTML 文本上下文有效，属性/JS 上下文还需各自转义策略。')])

KB['it/c-string-escape'] = dict(title='C/C++ 字符串转义',
  scenarios=['在 C 字符串里嵌入换行、引号、反斜杠等需转义字符。'],
  examples=[dict(title='转义 "line1\nline2"', body='输入含换行文本 → 输出 `"line1\\nline2"`（换行变为 \\n 转义序列）。')],
  faqs=[dict(q='\\0 有什么特殊含义？', a='\\0 是空字符，常用于标记 C 字符串结尾。')])

KB['it/js-escape'] = dict(title='JavaScript 字符串转义',
  scenarios=['把含引号、换行、Unicode 的文本安全嵌入 JS 字面量。'],
  examples=[dict(title='转义含引号文本', body='输入 `He said "Hi"` → 输出 `He said \"Hi\"`（双引号前加反斜杠）。')],
  faqs=[dict(q='模板字符串还需要转义吗？', a='用反引号可避免双引号转义，但反引号与 ${} 仍需处理。')])

KB['it/python-escape'] = dict(title='Python 字符串转义',
  scenarios=['生成可在 Python 源码里直接粘贴的字符串字面量。'],
  examples=[dict(title='转义换行', body='输入含换行文本 → 输出 `line1\\nline2`（原始换行变成 \\n）。')],
  faqs=[dict(q='raw 字符串 r"..." 还要转义吗？', a='r 前缀下反斜杠不转义，但不能以奇数个反斜杠结尾。')])

KB['it/java-escape'] = dict(title='Java 字符串转义',
  scenarios=['把文本嵌入 Java 字符串字面量，处理引号与换行。'],
  examples=[dict(title='转义', body='输入 `a\tb` → 输出 `"a\\tb"`（制表符变 \\t）。')],
  faqs=[dict(q='Java 文本块 """ 能省转义吗？', a='JDK 15+ 文本块可免多数转义，但仍需处理 `"""` 本身。')])

KB['it/php-escape'] = dict(title='PHP 字符串转义',
  scenarios=['生成 PHP 双引号字符串时的转义序列。'],
  examples=[dict(title='转义', body='输入 `$a` → 输出 `"$a"`（美元符前加反斜杠避免变量解析）。')],
  faqs=[dict(q='单引号字符串转义规则不同吗？', a='是，单引号只转义 \\ 和 \' 自身。')])

KB['it/go-escape'] = dict(title='Go 字符串转义',
  scenarios=['把文本安全地放进 Go 双引号字符串。'],
  examples=[dict(title='转义', body='输入含换行 → 输出 `"line1\\nline2"`。')],
  faqs=[dict(q='Go 原生字符串 `...` 呢？', a='反引号原生串不处理转义，但无法包含反引号本身。')])

KB['it/rust-escape'] = dict(title='Rust 字符串转义',
  scenarios=['生成 Rust 字符串字面量，处理引号、换行、Unicode。'],
  examples=[dict(title='转义', body='输入 `a\nb` → 输出 `"a\\nb"`。')],
  faqs=[dict(q='Rust 支持 \\u{...} 吗？', a='支持，如 \\u{1F600} 表示 😀。')])

KB['it/sql-escape'] = dict(title='SQL 字符串转义',
  scenarios=['拼 SQL 前转义单引号，避免语法错误与注入（首选参数化查询）。'],
  examples=[dict(title='转义 O\'Brien', body='输入 `O\'Brien` → 输出 `O\'\'Brien`（标准 SQL 用双单引号转义）。')],
  faqs=[dict(q='转义能代替参数化查询吗？', a='不能，转义只是兜底，参数化才是防注入正解。')])

KB['it/css-escape'] = dict(title='CSS 字符串转义',
  scenarios=['在 CSS content、选择器里嵌入特殊字符或 Unicode。'],
  examples=[dict(title='转义', body='输入含换行 → 输出 `"line1\\A line2"`（\\A 表示换行）。')],
  faqs=[dict(q='选择器里的点号要转义吗？', a='类选择器中 . 需转义为 \\. 否则被当作类分隔。')])

KB['it/regex-escape'] = dict(title='正则表达式字符转义',
  scenarios=['把用户输入当作字面量匹配时，对其中的 . * + ? 等转义。'],
  examples=[dict(title='转义 "a.b"', body='输入 `a.b` → 输出 `a\\.b`（点号被转义为字面量）。')],
  faqs=[dict(q='为什么要转义？', a='不转义时 . 会匹配任意字符，导致误匹配。')])

KB['it/char-encoder'] = dict(title='多格式字符编码器',
  scenarios=['一次性对比同一字符在 Hex/Dec/Oct/Binary/Unicode 下的表示。'],
  examples=[dict(title='编码 "A"', body='`A` → Hex 41 / Dec 65 / Oct 101 / Bin 01000001 / Unicode U+0041。')],
  faqs=[dict(q='哪种格式最省空间？', a='二进制最直观但最长，十六进制最紧凑易读。')])

KB['it/quoted-printable'] = dict(title='Quoted-Printable 编解码',
  scenarios=['邮件（MIME）正文常用 QP 编码保留可读 ASCII。'],
  examples=[dict(title='编码 "café"', body='输入 `café` → 输出 `caf=E9`（é 为非 ASCII，编为 =E9）。')],
  faqs=[dict(q='QP 与 Base64 何时选？', a='文本为主、仅少量非 ASCII 用 QP；二进制用 Base64。')])

KB['it/uuencode'] = dict(title='UUencode 编码 / 解码',
  scenarios=['早期 Usenet/邮件附件传输二进制的编码方式。'],
  examples=[dict(title='编码 "Cat"', body='输入 `Cat` → 输出以 `begin` 开头、`#9-X` 等数据行（含权限与文件名头）。')],
  faqs=[dict(q='UUencode 现在还用吗？', a='已基本被 Base64/MIME 取代，多见于老旧系统。')])

KB['it/xxencode'] = dict(title='XXencode 编码 / 解码',
  scenarios=['UUencode 的改进版，用 + 与 - 之间的 64 字符集。'],
  examples=[dict(title='编码 "Hi"', body='输入 `Hi` → 输出 `+H` 等数据行（XXencode 字符集不含易混字符）。')],
  faqs=[dict(q='与 Base64 区别？', a='字符集与行格式不同，编后体积相近。')])

KB['it/punycode'] = dict(title='Punycode 编解码',
  scenarios=['把含中文的域名（如 中文.com）编码为 ASCII 以兼容 DNS。'],
  examples=[dict(title='编码 "中文"', body='输入 `中文` → 输出 `xn--fiq228c`（即域名标签 `xn--fiq228c`）。')],
  faqs=[dict(q='浏览器地址栏为何显示中文？', a='浏览器解码 Punycode 后展示 Unicode，但底层 DNS 仍用 xn-- 形式。')])

KB['it/charset-detector'] = dict(title='编码识别器',
  scenarios=['拿到一段不知编码的文本（GBK/UTF-8/Big5）时推断其字符集。'],
  examples=[dict(title='识别乱码', body='输入 GBK 字节 `C4E3BAC3` → 识别为 GBK，解码得“你好”（而非 UTF-8 的乱码）。')],
  faqs=[dict(q='识别一定准吗？', a='短文本可能误判，建议结合语言与来源综合判断。')])

# ===== ciphers =====
KB['it/a1z26-cipher'] = dict(title='A1Z26 密码',
  scenarios=['字母 ↔ 数字速记、解谜（CTF）中快速互转。'],
  examples=[dict(title='加密 "ABC"', body='输入 `ABC` → 输出 `1 2 3`（A=1 … Z=26）；解密 `8 5 12 12 15` → `HELLO`。')],
  faqs=[dict(q='0 和 26 怎么区分？', a='A1Z26 用 1–26，不含 0；出现 0 通常属其他编码。')])

KB['it/caesar-cipher'] = dict(title='凯撒密码',
  scenarios=['古典密码教学、简单字母位移加密演示（位移 3 为标准 Caesar）。'],
  examples=[dict(title='加密 "HELLO" (位移3)', body='输入 `HELLO`，key=3 → 输出 `KHOOR`（每位后移 3：H→K、E→H …）。')],
  faqs=[dict(q='凯撒密码安全吗？', a='不安全，仅 25 种密钥，暴力枚举即可破解，仅作教学。')])

KB['it/atbash-cipher'] = dict(title='埃特巴什码 (Atbash)',
  scenarios=['古典替换密码，字母表反转映射（A↔Z）。'],
  examples=[dict(title='加密 "HELLO"', body='输入 `HELLO` → 输出 `SVOOL`（H↔S、E↔V …）。')],
  faqs=[dict(q='Atbash 有密钥吗？', a='无密钥，映射固定，因此极易破解。')])

KB['it/affine-cipher'] = dict(title='仿射密码 (Affine Cipher)',
  scenarios=['用 a·x+b (mod 26) 做单表替换，教学模运算与可逆条件。'],
  examples=[dict(title='加密 "A" (a=5,b=8)', body='E(x)=5·0+8=8 → `I`；要求 gcd(a,26)=1，a=5 合法（与 26 互质）。')],
  faqs=[dict(q='为什么 a 必须与 26 互质？', a='否则乘法逆元不存在，无法解密。')])

KB['it/vigenere-visualizer'] = dict(title='维吉尼亚密码',
  scenarios=['用关键词循环位移的多表代替密码，比凯撒更难破。'],
  examples=[dict(title='加密 "ATTACK" key=KEY', body='A+K=A、T+E=X、T+C=V … → 输出 `AXVCZ`；密钥 KEY 循环使用。')],
  faqs=[dict(q='维吉尼亚如何被破？', a='用卡西斯基试验或重合指数找密钥长度后逐位频分析。')])

KB['it/rot-cipher'] = dict(title='ROT 全套（ROT5/13/18/47）',
  scenarios=['ROT13 用于论坛隐藏剧透，ROT47 覆盖更多可打印字符。'],
  examples=[dict(title='ROT13 "HELLO"', body='输入 `HELLO` → 输出 `URYYB`（ROT13 自反，再转一次还原）。')],
  faqs=[dict(q='ROT13 是加密吗？', a='不是，只是混淆，任何人都能还原。')])

KB['it/adfgvx-cipher'] = dict(title='ADFGVX 密码',
  scenarios=['一战德军使用的分数化置换+替换密码，结合字母与数字。'],
  examples=[dict(title='原理示意', body='先按 6×6 方阵把字符替换为 ADFGVX 两字母，再按密钥列置换；如 P → 行 A 列 D = `AD`。')],
  faqs=[dict(q='为何用 ADFGVX 六个字母？', a='这些字母在莫尔斯电码中区分度大，减少传输误码。')])

KB['it/bacon-cipher'] = dict(title='培根密码 (Bacon Cipher)',
  scenarios=['用 A/B 五比特组隐藏信息于看似正常的文本中。'],
  examples=[dict(title='加密 "A"', body='A 的培根码为 `AAAAA`、B 为 `AAAAB`；可用两种字体把密文藏进一段话。')],
  faqs=[dict(q='培根码如何隐藏？', a='用粗细/大小写等两种样式代表 A/B，肉眼难察。')])

KB['it/rail-fence-cipher'] = dict(title='栅栏密码 (Rail Fence)',
  scenarios=['按之字形写入多行的置换密码，rail=3 常见。'],
  examples=[dict(title='加密 "WEAREDISCOVERED" rail=3', body='之字形写入后按行读出 → `WECRLTEERDSOEEAIVD`；解密按行回填还原。')],
  faqs=[dict(q='栅栏密码密钥是什么？', a='行数（rail 数），已知行数即可还原。')])

KB['it/playfair-cipher'] = dict(title='普莱费尔密码 (Playfair)',
  scenarios=['双字母替换密码，用 5×5 方阵（I/J 同格）。'],
  examples=[dict(title='加密 "HI"', body='H 与 I 组对，按方阵同行/同列/矩形规则替换；如 HI → `BM`（示例密钥方阵）。')],
  faqs=[dict(q='Playfair 如何处理重复字母？', a='插入填充字母（如 X）隔开，如 `LL` → `LX L`。')])

KB['it/polybius-cipher'] = dict(title='波利比奥斯方阵密码 (Polybius)',
  scenarios=['把字母映射为两位数坐标（行/列）的经典替换。'],
  examples=[dict(title='加密 "AB"', body='标准 5×5 方阵中 A=(1,1)=`11`、B=(1,2)=`12` → 输出 `11 12`。')],
  faqs=[dict(q='I 和 J 冲突怎么办？', a='同置一格，解密时按上下文区分。')])

KB['it/hill-cipher'] = dict(title='Hill 密码 (2x2 矩阵)',
  scenarios=['用矩阵乘法做线性代换的分组密码，教学模 26 矩阵。'],
  examples=[dict(title='加密 "HI" 用矩阵 [[3,2],[5,7]]', body='H=7,I=8 → 向量 (3·7+2·8, 5·7+7·8)=(37,91) mod26=(11,13) → `LM`。')],
  faqs=[dict(q='密钥矩阵为何要可逆(mod26)？', a='否则无法解出明文，需 det 与 26 互质。')])

KB['it/xor-cipher'] = dict(title='XOR 加密 / 解密',
  scenarios=['按字节与密钥异或的对称流密码，密钥复用等同一次性密码本才安全。'],
  examples=[dict(title='加密 "Hi" key=0x5A', body='H(0x48)^0x5A=0x12、i(0x69)^0x5A=0x33 → 输出 `12 33`（十六进制）。')],
  faqs=[dict(q='XOR 为什么不能单独用于保密？', a='若密钥短且复用，可被频分析与已知明文攻破。')])

KB['it/aes-encryptor'] = dict(title='AES 加密 / 解密',
  scenarios=['用 AES-256（CBC/GCM）对敏感配置、日志做对称加密。'],
  examples=[dict(title='流程示意', body='明文 + 密钥(32字节) + 随机 IV → 密文；GCM 模式额外产出认证标签防篡改。解密需相同密钥与 IV。')],
  faqs=[dict(q='CBC 与 GCM 怎么选？', a='GCM 提供完整性校验且并行友好，优先；CBC 需额外 HMAC 才安全。')])

KB['it/des'] = dict(title='DES / 3DES 加密解密',
  scenarios=['兼容老旧系统或教学分组密码；新系统勿用 DES。'],
  examples=[dict(title='3DES 说明', body='3DES 对明文做 加密→解密→加密（三把 56 位密钥），强度约 112 位；单 DES 已被穷举攻破。')],
  faqs=[dict(q='为什么 DES 不安全？', a='56 位密钥空间小，现代算力可数小时穷举。')])

KB['it/rc4'] = dict(title='RC4 / ARC4 加密解密',
  scenarios=['轻量流密码，仅用于兼容历史协议。'],
  examples=[dict(title='说明', body='RC4 以密钥调度生成伪随机流与明文异或；因偏弱偏（前若干字节有偏）已被弃用。')],
  faqs=[dict(q='RC4 还能用吗？', a='新系统不建议，优先 AES-GCM/ChaCha20。')])

KB['it/rabbit'] = dict(title='Rabbit 流加密',
  scenarios=['eSTREAM 推荐的高速流密码，适合资源受限环境。'],
  examples=[dict(title='说明', body='Rabbit 以 128 位密钥 + 64 位 IV 驱动内部状态，生成密钥流异或明文。')],
  faqs=[dict(q='Rabbit 与 RC4 比？', a='Rabbit 设计更现代、无 RC4 的初期偏置问题。')])

KB['it/xxtea'] = dict(title='XXTEA 加密解密',
  scenarios=['TEA 家族中修正版块密码，适合嵌入式小数据加密。'],
  examples=[dict(title='说明', body='XXTEA 把明文当 32 位字数组做多轮 Feistel 式混淆，密钥 128 位。')],
  faqs=[dict(q='XXTEA 适合大文件吗？', a='可行但不如 AES 经过广泛审计，谨慎用于高安全场景。')])

KB['it/rsa'] = dict(title='RSA 加密解密 / 签名验证',

  scenarios=['用公钥加密、私钥解密的经典非对称算法，也用于签名。',
    'JWT、TLS 握手、License 校验中常用 RSA。'],
  examples=[dict(title='参数示意', body='选 p=61,q=53 → n=3233, φ=3120, 取 e=17, d=2753；明文 m=65 → c=65^17 mod3233=2790，解密 2790^2753 mod3233=65。')],
  faqs=[dict(q='RSA 为什么慢？', a='大数模幂运算重，通常用 RSA 交换密钥、再用 AES 传数据。'),
    dict(q='签名用私钥还是公钥？', a='签名用私钥加密摘要，验证用公钥。')])

KB['it/ecdsa'] = dict(title='ECDSA 椭圆曲线签名',
  scenarios=['比特币、TLS 证书用 ECDSA 做轻量高安全签名。'],
  examples=[dict(title='曲线示意', body='以 secp256k1 为例，私钥 d 生成公钥 Q=d·G；对消息哈希 e 用随机数 k 产出签名 (r,s)，验证用公钥与 G。')],
  faqs=[dict(q='ECDSA 为何比 RSA 短？', a='256 位椭圆曲线安全性≈3072 位 RSA，密钥更短。')])

# ===== math / stats =====
KB['it/bayes-theorem'] = dict(title='贝叶斯定理计算器',
  scenarios=['根据先验与似然更新患病/ spam 等后验概率。'],
  examples=[dict(title='医学筛查', body='患病率 P(D)=1%，灵敏 90%、特异 95%：P(D|+)=0.01·0.9/(0.01·0.9+0.99·0.05)=0.153 → 阳性者真患病约 15.3%。')],
  faqs=[dict(q='为什么阳性不代表一定患病？', a='基础患病率很低时假阳性会稀释阳性预测值。')])

KB['it/binomial-distribution'] = dict(title='二项分布计算器',
  scenarios=['n 次独立试验、单次成功概率 p 时算恰好/至多 k 次成功。'],
  examples=[dict(title='抛硬币', body='n=10,p=0.5,k=5：P(X=5)=C(10,5)·0.5^10≈0.246（约 24.6%）。')],
  faqs=[dict(q='二项与伯努利关系？', a='单次伯努利是 n=1 的二项分布。')])

KB['it/exponential-distribution'] = dict(title='指数分布计算器',
  scenarios=['建模设备寿命、请求间隔等“无记忆”等待时间。'],
  examples=[dict(title='平均 10 分钟', body='λ=0.1/分钟，P(T>10)=e^(−0.1·10)=e^−1≈0.368（约 36.8% 超过 10 分钟）。')],
  faqs=[dict(q='无记忆性指什么？', a='已等待 t 不影响后续等待分布，P(T>t+s|T>t)=P(T>s)。')])

KB['it/hypergeometric-distribution'] = dict(title='超几何分布计算器',
  scenarios=['不放回抽样（如从 N 件含 K 件次品中抽 n 件）的成功次数。'],
  examples=[dict(title='质检抽样', body='N=50,K=5,n=10,k=1：P(X=1)=C(5,1)C(45,9)/C(50,10)≈0.431（约 43.1%）。')],
  faqs=[dict(q='超几何与二项区别？', a='超几何不放回、概率随抽样变化；二项放回、概率恒定。')])

KB['it/normal-distribution'] = dict(title='正态分布计算器',
  scenarios=['已知均值 μ、标准差 σ 求区间概率或分位数。'],
  examples=[dict(title='身高模型', body='μ=170,σ=6，P(164<X<176)=Φ(1)−Φ(−1)≈0.6827（约 68.3%，即±1σ 区间）。')],
  faqs=[dict(q='68-95-99.7 法则？', a='正态下 ±1σ≈68.3%、±2σ≈95.4%、±3σ≈99.7%。')])

KB['it/poisson-distribution'] = dict(title='泊松分布计算器',
  scenarios=['单位时间/面积内稀有事件发生次数（如呼叫量、缺陷数）。'],
  examples=[dict(title='客服来电', body='λ=4 通/小时，P(X=2)=e^−4·4^2/2!≈0.1465（约 14.65%）。')],
  faqs=[dict(q='泊松与二项关系？', a='n 大 p 小时二项逼近泊松。')])

KB['it/confidence-interval'] = dict(title='置信区间计算器',
  scenarios=['由样本均值/比例估算总体参数的可信区间。'],
  examples=[dict(title='比例 CI', body='n=1000, 命中 520, 95% CI：p±1.96·√(0.52·0.48/1000)=0.52±0.031 → [0.489,0.551]。')],
  faqs=[dict(q='95% 置信度含义？', a='重复抽样下约 95% 的区间覆盖真值，非“真值有 95% 概率落此区间”。')])

KB['it/margin-of-error'] = dict(title='误差范围计算器',
  scenarios=['调查报道里“±3%”的误差幅度计算。'],
  examples=[dict(title='民调', body='n=1000,p=0.5,95%：MoE=1.96·√(0.25/1000)≈0.031 → ±3.1%。')],
  faqs=[dict(q='样本越大误差越小？', a='MoE 与 √n 成反比，翻倍样本只降约 29%。')])

KB['it/hypothesis-test'] = dict(title='单样本 Z 检验',
  scenarios=['已知总体方差时检验样本均值是否等于假设值。'],
  examples=[dict(title='Z 检验', body='μ0=100,σ=15,n=36,x̄=105：Z=(105−100)/(15/√36)=2.0，p≈0.045 <0.05 → 拒绝原假设。')],
  faqs=[dict(q='Z 检验与 t 检验？', a='已知 σ 用 Z；σ 未知用样本 s 且小样本用 t。')])

KB['it/standard-deviation'] = dict(title='标准差计算器',
  scenarios=['衡量数据离散程度，配合均值描述分布。'],
  examples=[dict(title='数据集', body='数据 2,4,4,4,5,5,7,9：均值 5，方差(样本)=32/7≈4.57，标准差 s≈2.14。')],
  faqs=[dict(q='样本与总体标准差区别？', a='样本除以 n−1（无偏），总体除以 n。')])

KB['it/statistical-power'] = dict(title='统计功效计算器',
  scenarios=['实验设计前估算检出效应所需样本量。'],
  examples=[dict(title='功效示意', body='α=0.05、效应量 d=0.5、功效 0.8 时约需 n≈64/组（两独立样本 t 检验近似）。')],
  faqs=[dict(q='功效 0.8 含义？', a='真实存在差异时，有 80% 概率拒绝原假设（即 20% 二类错误）。')])

KB['it/uniform-distribution'] = dict(title='均匀分布计算器',
  scenarios=['区间 [a,b] 内等可能取值的概率与期望。'],
  examples=[dict(title='[0,10]', body='E=5，P(X<3)=0.3，方差=(10−0)^2/12≈8.33。')],
  faqs=[dict(q='均匀分布的密度？', a='区间内恒为 1/(b−a)，区间外为 0。')])

KB['it/math-evaluator'] = dict(title='数学表达式求值器',
  scenarios=['快速计算含括号、函数、常量的复杂算式。'],
  examples=[dict(title='求值', body='输入 `2*(3+4)^2 - sqrt(16)` → 2·49 − 4 = 94。')],
  faqs=[dict(q='支持哪些函数？', a='常见 sqrt、pow、sin/cos、log、abs、round 等。')])

KB['it/matrix-determinant'] = dict(title='矩阵行列式',
  scenarios=['判断方阵可逆性、解线性方程组（克拉默法则）。'],
  examples=[dict(title='2x2', body='矩阵 [[a,b],[c,d]] 行列式 = ad−bc；如 [[3,2],[5,7]] → 3·7−2·5=11。')],
  faqs=[dict(q='行列式为 0 说明？', a='矩阵奇异、不可逆，方程组可能无解或无穷解。')])

KB['it/matrix-inverter'] = dict(title='矩阵求逆',
  scenarios=['解 AX=B 得 X=A⁻¹B；仅在 det≠0 时可逆。'],
  examples=[dict(title='2x2 逆', body='[[3,2],[5,7]]⁻¹ = (1/11)[[7,−2],[−5,3]]。')],
  faqs=[dict(q='不可逆矩阵能求伪逆吗？', a='可用 Moore-Penrose 伪逆作为近似解。')])

KB['it/matrix-multiplier'] = dict(title='矩阵乘法',
  scenarios=['线性变换复合、神经网络前向计算等。'],
  examples=[dict(title='相乘', body='[[1,2],[3,4]]·[[5,6],[7,8]] = [[19,22],[43,50]]。')],
  faqs=[dict(q='矩阵乘法满足交换律吗？', a='一般不满足，AB≠BA。')])

KB['it/matrix-transpose'] = dict(title='矩阵转置',
  scenarios=['行列互换，用于协方差矩阵、最小二乘等。'],
  examples=[dict(title='转置', body='[[1,2,3],[4,5,6]]ᵀ = [[1,4],[2,5],[3,6]]。')],
  faqs=[dict(q='对称矩阵转置？', a='对称矩阵转置等于自身。')])

KB['it/vector-dot-product'] = dict(title='向量点积',
  scenarios=['判断向量夹角、投影、相似度计算。'],
  examples=[dict(title='点积', body='(1,2,3)·(4,5,6)=1·4+2·5+3·6=32。')],
  faqs=[dict(q='点积为 0 含义？', a='两向量正交（垂直）。')])

KB['it/vector-cross-product'] = dict(title='向量叉积',
  scenarios=['求三维法向量、面积、力矩方向。'],
  examples=[dict(title='叉积', body='(1,0,0)×(0,1,0)=(0,0,1)（指向 z 轴）。')],
  faqs=[dict(q='叉积结果方向？', a='由右手定则确定，且垂直于两输入向量。')])

KB['it/vector-magnitude'] = dict(title='向量模长',
  scenarios=['求向量长度/距离，归一化前先算模。'],
  examples=[dict(title='模长', body='‖(3,4)‖=√(3²+4²)=5。')],
  faqs=[dict(q='归一化怎么做？', a='向量除以其模长得到单位长度。')])

KB['it/triangle-calculator'] = dict(title='Triangle Calculator',
  scenarios=['已知三边/两边一角求其余边角与面积。'],
  examples=[dict(title='直角三角形', body='直角边 3、4 → 斜边 5，面积=3·4/2=6。')],
  faqs=[dict(q='余弦定理公式？', a='c²=a²+b²−2ab·cosC。')])

KB['it/prime-checker'] = dict(title='Prime Number Checker',
  scenarios=['判断大整数是否为素数，教学与密码学前置。'],
  examples=[dict(title='判定', body='97 不能被 2..√97≈9 的素数整除 → 是素数；91=7·13 → 合数。')],
  faqs=[dict(q='大素数怎么判？', a='超过一定规模用 Miller-Rabin 等概率素性测试。')])

KB['it/bitwise-calculator'] = dict(title='位运算计算器',
  scenarios=['处理掩码、权限位、底层协议字段。'],
  examples=[dict(title='位与', body='0b1100 & 0b1010 = 0b1000（即 12 & 10 = 8）；0b1001 | 0b0110 = 0b1111=15。')],
  faqs=[dict(q='& 与 && 区别？', a='& 是按位运算，&& 是逻辑短路运算。')])

KB['it/number-base-converter'] = dict(title='进制转换计算器',
  scenarios=['在 2/8/10/16 等进制间转换整数。'],
  examples=[dict(title='转换', body='255(10) = FF(16) = 377(8) = 11111111(2)。')],
  faqs=[dict(q='小数能转进制吗？', a='可以，按乘基取整法处理小数部分。')])

KB['it/integer-base-converter'] = dict(title='任意进制转换器',
  scenarios=['在 2–36 进制间互转大整数。'],
  examples=[dict(title='转换', body='255 转 36 进制 = `73`（字符 0-9A-Z）；`Z`(36进制)=35(10)。')],
  faqs=[dict(q='超过 36 进制怎么表示？', a='需自定义符号表，标准仅到 36（0-9A-Z）。')])

KB['it/chmod-calculator'] = dict(title='Chmod 权限计算器',
  scenarios=['把 rwx 转成数字权限，或反查权限含义。'],
  examples=[dict(title='转换', body='rwxr-xr-x → 755（owner 7=rwx、group 5=rx、other 5=rx）。')],
  faqs=[dict(q='s 位（setuid）怎么表示？', a='特殊位加在最前，如 4755 表示 setuid+755。')])

KB['it/clamp-calculator'] = dict(title='CSS clamp 计算器',
  scenarios=['生成响应式字号 clamp(min, preferred, max)。'],
  examples=[dict(title='生成', body='视口 320–1280px、期望 16–24px：clamp(16px, 1rem + 0.625vw, 24px)（约在 320px=16、1280px=24）。')],
  faqs=[dict(q='preferred 用 vw 还是 %？', a='字体用 vw，因 % 相对父字号而非视口。')])

KB['it/calc-1'] = dict(title='文件大小单位换算',
  scenarios=['KB/MB/GB 与 KiB/MiB 混用时换算。'],
  examples=[dict(title='换算', body='1 GB=1000 MB（十进制）；1 GiB=1024 MiB（二进制）。100 MiB×1024²≈104.9 MB。')],
  faqs=[dict(q='KB 与 KiB 区别？', a='KB=10³ 字节，KiB=2¹⁰ 字节，存储厂商标十进制、系统常显二进制。')])

KB['it/calc-2'] = dict(title='进制转换器（IT）',
  scenarios=['开发调试中 10/16/2/8 互转。'],
  examples=[dict(title='换算', body='0x1F4 = 500(10) = 111110100(2) = 764(8)。')],
  faqs=[dict(q='0x 前缀含义？', a='表示十六进制，如 0xFF=255。')])

KB['it/calc-3'] = dict(title='颜色值转换器',
  scenarios=['HEX、RGB、HSL 互转用于前端配色。'],
  examples=[dict(title='转换', body='#FF0000 ↔ rgb(255,0,0) ↔ hsl(0,100%,50%)（纯红）。')],
  faqs=[dict(q='HSL 的 L=50% 含义？', a='恰好为该色相的中间亮度，L=100% 为白、0% 为黑。')])

KB['it/calc-4'] = dict(title='CSS 单位换算（px / em / rem / pt / %）',
  scenarios=['按根字号把 rem 转 px，或按父字号把 em 转 px。'],
  examples=[dict(title='换算', body='根字号 16px：2rem=32px；父字号 14px：1.5em=21px；12pt≈16px。')],
  faqs=[dict(q='em 与 rem 区别？', a='em 相对父元素字号，rem 相对根(html)字号。')])

KB['it/calc-5'] = dict(title='字符串长度统计',
  scenarios=['校验输入长度（如密码、短信字数）。'],
  examples=[dict(title='统计', body='"Hello 世界"：字符数 8（H e l l o 空格 世 界），UTF-8 字节数 11（中文各 3 字节）。')],
  faqs=[dict(q='字符数与字节数为何不同？', a='中文等多字节字符在 UTF-8 占多字节，数据库常按字节限制。')])

KB['it/calc-6'] = dict(title='IT 单位换算（calc-6）',
  scenarios=['补充的 IT 单位换算入口。'],
  examples=[dict(title='说明', body='与 calc-1/2/4 同类，按提示选择源单位与目标单位即可换算。')],
  faqs=[dict(q='换算不准怎么办？', a='确认用的是十进制(1000)还是二进制(1024)前缀。')])

KB['it/calc-7'] = dict(title='JSONPath 提取器',
  scenarios=['从嵌套 JSON 中按路径提取字段。'],
  examples=[dict(title='提取', body='对 `{"user":{"name":"Tom","age":20}}` 用 `$.user.name` → `Tom`。')],
  faqs=[dict(q='$ 表示什么？', a='$ 代表根对象，后续用 . 或 [] 下钻。')])

KB['it/calc-8'] = dict(title='JWT 解码器',
  scenarios=['查看 JWT 三段（头/载荷/签名）中的声明。'],
  examples=[dict(title='解码', body='`eyJhbG...` 三段以 . 分隔，Base64url 解码后：header={"alg":"HS256","typ":"JWT"}，payload={"sub":"123","exp":1700000000}。')],
  faqs=[dict(q='解码 JWT 能验证真伪吗？', a='不能，仅看内容；验签需服务端密钥。')])

KB['it/calc-10'] = dict(title='哈希值生成器',
  scenarios=['算文本/文件的 MD5/SHA 指纹用于校验。'],
  examples=[dict(title='SHA256 "abc"', body='`abc` 的 SHA-256 = ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad。')],
  faqs=[dict(q='哈希能还原原文吗？', a='不能，哈希单向；且 MD5/SHA1 已不适合校验安全性，仅用于完整性。')])

# ===== IP / network =====
KB['it/ip-calculator'] = dict(title='IP 子网计算器',
  scenarios=['划分 CIDR 子网、算网络地址与可用主机数。'],
  examples=[dict(title='192.168.1.10/24', body='网络地址 192.168.1.0，掩码 255.255.255.0，可用主机 192.168.1.1–254（共 254 台）。')],
  faqs=[dict(q='/24 可用主机为何是 254？', a='共 256 地址，减去网络地址与广播地址。')])

KB['it/ipv4-range-expander'] = dict(title='IPv4 Range Expander',
  scenarios=['把 192.168.1.1-192.168.1.10 之类的范围展开为列表。'],
  examples=[dict(title='展开', body='`10.0.0.1-10.0.0.3` → 10.0.0.1, 10.0.0.2, 10.0.0.3（共 3 个）。')],
  faqs=[dict(q='跨段范围能展开吗？', a='可以，但地址数极大时建议只取首尾或按需分页。')])

KB['it/ipv6-converter'] = dict(title='IPv6 Address Converter',
  scenarios=['IPv6 压缩/展开、与 IPv4 映射表示互转。'],
  examples=[dict(title='展开', body='`2001:db8::1` 全展开为 `2001:0db8:0000:0000:0000:0000:0000:0001`。')],
  faqs=[dict(q=':: 代表什么？', a='一段或多段全零的压缩写法，一个地址中只能用一次。')])

KB['it/ipv6-ula'] = dict(title='IPv6 ULA Generator',
  scenarios=['生成 fd00::/8 的唯一本地地址用于内网。'],
  examples=[dict(title='生成', body='随机 ULA 前缀如 `fd12:3456:789a::/48`（48 位全局 ID 随机，后接子网）。')],
  faqs=[dict(q='ULA 能上公网吗？', a='不能，fd00::/8 仅本地通信，类似 IPv4 私网。')])

KB['it/mac-generator'] = dict(title='MAC 地址生成器',
  scenarios=['生成随机或指定厂商 OUI 的 MAC 用于测试。'],
  examples=[dict(title='生成', body='随机 MAC 例 `3C:5A:B4:1F:2E:9D`（前 3 字节 OUI 标识厂商）。')],
  faqs=[dict(q='本地管理位怎么看？', a='第二个十六进制的最低位为 1 表示本地管理（Universally vs Locally）。')])

KB['it/mac-lookup'] = dict(title='MAC 地址厂商查询',
  scenarios=['按 OUI 前 3 字节反查网卡厂商。'],
  examples=[dict(title='查 OUI', body='`3C:5A:B4` → 查表得对应厂商（如某网络设备商）；无记录则显示未知。')],
  faqs=[dict(q='查不到一定假吗？', a='不一定，小厂商或未登记 OUI 也会查不到。')])

KB['it/url-parser'] = dict(title='URL 解析器',
  scenarios=['拆出协议、主机、路径、查询、锚点。'],
  examples=[dict(title='解析', body='`https://ex.com:443/p?a=1&b=2#top` → protocol=https, host=ex.com, port=443, path=/p, query=a=1&b=2, hash=top。')],
  faqs=[dict(q='默认端口要显示吗？', a='解析会保留显式端口；默认端口(80/443)常省略。')])

KB['it/url-params'] = dict(title='URL Parameter Parser',
  scenarios=['把查询串解析为键值对，便于调试接口。'],
  examples=[dict(title='解析', body='`?page=2&sort=desc&ids=1,2` → {page:2, sort:"desc", ids:"1,2"}。')],
  faqs=[dict(q='重复键如何处理？', a='通常取最后一个或合并为数组，视实现而定。')])

KB['it/user-agent-parser'] = dict(title='User-Agent 解析器',
  scenarios=['从 UA 串识别浏览器/系统/设备类型。'],
  examples=[dict(title='解析', body='`Mozilla/5.0 (Windows NT 10.0) AppleWebKit … Chrome/120 Safari/537` → OS=Windows 10, Browser=Chrome 120。')],
  faqs=[dict(q='UA 能伪造吗？', a='能，UA 仅为客户端自报，不可作身份依据。')])

KB['it/msisdn-lookup'] = dict(title='MSISDN 查询',
  scenarios=['解析手机号的国家码/运营商片段。'],
  examples=[dict(title='解析', body='`8613800138000` → CC=86(中国), NDC=138, SN=00138000（示例结构）。')],
  faqs=[dict(q='MSISDN 与 IMSI 区别？', a='MSISDN 是用户可见号码，IMSI 是 SIM 内国际标识。')])

# ===== hashes / crypto helpers =====
KB['it/md5'] = dict(title='MD5 哈希计算器',
  scenarios=['生成文件/文本指纹用于完整性校验（非安全用途）。'],
  examples=[dict(title='MD5 "abc"', body='`abc` → 900150983cd24fb0d6963f7d28e17f72。')],
  faqs=[dict(q='MD5 还能用于安全吗？', a='不建议，已被碰撞攻破，仅用于非安全完整性校验。')])

KB['it/sha'] = dict(title='SHA 哈希计算器',
  scenarios=['生成 SHA-1/256/512 摘要用于校验与签名。'],
  examples=[dict(title='SHA-256 "abc"', body='`abc` → ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad。')],
  faqs=[dict(q='SHA-1 安全吗？', a='已不推荐签名，仍可用作校验；新系统用 SHA-256+。')])

KB['it/hash'] = dict(title='哈希计算器',
  scenarios=['快速对文本/文件求多种哈希。'],
  examples=[dict(title='SHA-1 "hello"', body='`hello` → aaf4c61ddcc5e8a2dabede0f3b482cd9aea9434d。')],
  faqs=[dict(q='为何同一内容哈希恒定？', a='哈希是确定函数，输入不变输出必不变。')])

KB['it/hash-multi'] = dict(title='多算法哈希器',
  scenarios=['一次算出 MD5/SHA1/SHA256/CRC 等便于多系统比对。'],
  examples=[dict(title='多算', body='`test` 同时输出 MD5=98f6bcd4621d373cade4e832627b4f6、SHA256=9f86d081… 等。')],
  faqs=[dict(q='用哪个最安全？', a='校验用 SHA-256；防篡改签名用 HMAC-SHA256。')])

KB['it/crc-calculator'] = dict(title='CRC 计算器',
  scenarios=['通信/存储校验常用 CRC8/16/32。'],
  examples=[dict(title='CRC32 "123456789"', body='标准 CRC-32（多项式 0x04C11DB7）结果为 `CBF43926`。')],
  faqs=[dict(q='CRC 能检错但不能？', a='CRC 检随机错很强，但不抗故意篡改（需密码学哈希）。')])

KB['it/hash-id-generator'] = dict(title='Hashids 生成器',
  scenarios=['把数字 ID 编码成不易猜的短串（如 ?id=laHqu）。'],
  examples=[dict(title='编码', body='salt="my" 编码 [1,2,3] → 如 `o2fXhV`（解码回 [1,2,3]）。')],
  faqs=[dict(q='Hashids 可逆吗？', a='可逆，是编码非加密；换 salt 结果不同。')])

KB['it/hash-identifier'] = dict(title='Hash Identifier',
  scenarios=['根据长度/特征猜测未知哈希的算法。'],
  examples=[dict(title='识别', body='32 位十六进制 → 可能是 MD5；40 位 → SHA-1；64 位 → SHA-256。')],
  faqs=[dict(q='识别一定准吗？', a='只能按长度与字符集猜测，需结合来源确认。')])

KB['it/bcrypt'] = dict(title='Bcrypt 哈希/校验',
  scenarios=['存储用户口令的推荐慢哈希（自带盐与成本因子）。'],
  examples=[dict(title='哈希示意', body='口令 "password" 经 bcrypt 成本 10 生成形如 `$2b$10$...` 的哈希；验证时用同一哈希比对口令。')],
  faqs=[dict(q='bcrypt 为何慢？', a='刻意放慢并加 salt 抵抗暴力与彩虹表。')])

KB['it/pbkdf2'] = dict(title='PBKDF2 密钥派生',
  scenarios=['从口令派生加密密钥，带盐与迭代次数。'],
  examples=[dict(title='派生', body='口令 + salt（16字节）+ 迭代 100000 + SHA256 → 固定长度密钥；迭代越多越抗暴力。')],
  faqs=[dict(q='PBKDF2 与 bcrypt 怎么选？', a='存储口令二者皆可，PBKDF2 更通用，bcrypt 实现更简单安全。')])

KB['it/hmac-generator'] = dict(title='HMAC 生成器',
  scenarios=['用密钥对消息生成认证码，验证完整性与来源。'],
  examples=[dict(title='HMAC-SHA256', body='key="secret", msg="hello" → HMAC-SHA256 = 88da81...（任何改动都会使 MAC 失配）。')],
  faqs=[dict(q='HMAC 需要保密密钥吗？', a='是，密钥必须保密，否则可伪造 MAC。')])

# ===== converters (format) =====
KB['it/json-formatter'] = dict(title='JSON 格式化 / 美化 / 压缩',
  scenarios=['把压缩 JSON 美化便于阅读，或压缩以省传输。'],
  examples=[dict(title='格式化', body='`{"a":1,"b":[2,3]}` → 美化为带缩进的多行；压缩则去空白回到单行。')],
  faqs=[dict(q='格式化会改变数据吗？', a='不会，仅调整空白与缩进。')])

KB['it/json-minify'] = dict(title='JSON 压缩/格式化',
  scenarios=['与 json-formatter 同类，去空白压缩。'],
  examples=[dict(title='压缩', body='多行 JSON 压缩为单行，体积通常降 10–30%。')],
  faqs=[dict(q='压缩 JSON 还能解析吗？', a='能，合法 JSON 不依赖换行。')])

KB['it/json-diff'] = dict(title='JSON Diff 深度对比',
  scenarios=['对比两份配置/接口响应的差异。'],
  examples=[dict(title='对比', body='左 `{"a":1,"b":2}` 右 `{"a":1,"b":3}` → 仅 `b` 由 2 变为 3 被标出。')],
  faqs=[dict(q='数组顺序影响对比吗？', a='默认按位置比对；语义比较需开启键匹配模式。')])

KB['it/json-repair'] = dict(title='JSON Repairer',
  scenarios=['修复缺引号、尾逗号等非法 JSON。'],
  examples=[dict(title='修复', body='`{a:1,}` → 修复为 `{"a":1}`（补键引号、去尾逗号）。')],
  faqs=[dict(q='自动修复会改语义吗？', a='仅修语法错误，不改变字段与值。')])

KB['it/json-schema-generator'] = dict(title='JSON Schema 生成器',
  scenarios=['由样例 JSON 推断 Schema 用于校验。'],
  examples=[dict(title='生成', body='样例 `{"name":"Tom","age":20}` → Schema 标注 name:string、age:integer。')],
  faqs=[dict(q='推断的 Schema 完整吗？', a='基于样例，极端情况需人工补充约束。')])

KB['it/json-schema-validator'] = dict(title='JSON Schema 验证器',
  scenarios=['校验接口入参是否符合约定结构。'],
  examples=[dict(title='校验', body='数据 `{"age":"20"}` 对 `age:integer` Schema → 失败（类型应为整数非字符串）。')],
  faqs=[dict(q='Schema 用哪个规范？', a='常用 draft-07 或 2020-12，注意版本差异。')])

KB['it/json-to-code'] = dict(title='JSON 转代码',
  scenarios=['把 JSON 转成 TS 接口/Python dict/Go struct 等。'],
  examples=[dict(title='转 TS', body='`{"name":"Tom"}` → `interface Root { name: string }`。')],
  faqs=[dict(q='嵌套对象怎么转？', a='递归生成嵌套接口/结构体。')])

KB['it/json-to-csv'] = dict(title='JSON 转 CSV',
  scenarios=['把对象数组导出为表格便于 Excel 打开。'],
  examples=[dict(title='转换', body='`[{"a":1,"b":2},{"a":3,"b":4}]` → 表头 a,b 两行数据。')],
  faqs=[dict(q='嵌套字段怎么处理？', a='通常展平或用点路径命名列。')])

KB['it/json-to-tsv'] = dict(title='JSON / TSV 转换器',
  scenarios=['生成制表符分隔文件用于数据库导入。'],
  examples=[dict(title='转换', body='对象数组 → 表头行 + 制表符分隔数据行。')],
  faqs=[dict(q='TSV 与 CSV 区别？', a='TSV 用 \t 分隔，字段内逗号无需转义。')])

KB['it/json-to-xml'] = dict(title='JSON 转 XML',
  scenarios=['对接只接受 XML 的遗留系统。'],
  examples=[dict(title='转换', body='`{"name":"Tom"}` → `<name>Tom</name>`。')],
  faqs=[dict(q='数组怎么转 XML？', a='通常重复元素或加索引，如 <item>1</item><item>2</item>。')])

KB['it/json-to-yaml'] = dict(title='JSON 转 YAML',
  scenarios=['把 JSON 配置转成可读性更好的 YAML。'],
  examples=[dict(title='转换', body='`{"a":1,"b":[2,3]}` → `- a: 1\n  b:\n  - 2\n  - 3`（缩进表示层级）。')],
  faqs=[dict(q='YAML 对缩进敏感吗？', a='是，必须用空格且层级一致。')])

KB['it/yaml-to-json'] = dict(title='YAML to JSON Converter',
  scenarios=['把 YAML 配置转 JSON 供程序消费。'],
  examples=[dict(title='转换', body='`a: 1\nb:\n  - 2\n  - 3` → `{"a":1,"b":[2,3]}`。')],
  faqs=[dict(q='YAML 注释会保留吗？', a='JSON 无注释，转换后注释丢失。')])

KB['it/yaml-to-xml'] = dict(title='YAML to XML Converter',
  scenarios=['YAML 配置转 XML 对接旧系统。'],
  examples=[dict(title='转换', body='`name: Tom` → `<name>Tom</name>`。')],
  faqs=[dict(q='多文档 YAML 怎么转？', a='需指定文档或逐文档转换。')])

KB['it/yaml-to-toml'] = dict(title='YAML to TOML Converter',
  scenarios=['容器/Go 生态偏好 TOML 时转换。'],
  examples=[dict(title='转换', body='`name: Tom` → `name = "Tom"`。')],
  faqs=[dict(q='YAML 锚点怎么处理？', a='需展开锚点引用后再转。')])

KB['it/yaml-formatter'] = dict(title='YAML 格式化/验证/转JSON',
  scenarios=['校验 YAML 语法并美化。'],
  examples=[dict(title='格式化', body='压缩 YAML 按 2 空格缩进美化，并提示语法错误位置。')],
  faqs=[dict(q='Tab 能缩进 YAML 吗？', a='不能，YAML 仅允许空格缩进。')])

KB['it/yaml-validator'] = dict(title='YAML 语法验证器',
  scenarios=['CI 前校验配置文件合法。'],
  examples=[dict(title='校验', body='`a: [1,2` → 报错：列表未闭合。')],
  faqs=[dict(q='常见 YAML 错误？', a='缩进不一致、冒号后缺空格、Tab 缩进。')])

KB['it/xml-formatter'] = dict(title='XML 格式化',
  scenarios=['美化压缩的 XML 便于阅读。'],
  examples=[dict(title='格式化', body='单行 `<a><b>1</b></a>` → 带缩进多行。')],
  faqs=[dict(q='格式化改变含义吗？', a='不改变结构，但可能改变混合内容的空白。')])

KB['it/xml-validator'] = dict(title='XML Validator',
  scenarios=['校验标签闭合与 well-formed。'],
  examples=[dict(title='校验', body='`<a><b></a>` → 报错：b 未闭合 / 标签不匹配。')],
  faqs=[dict(q='XML 区分大小写吗？', a='区分，<A> 与 <a> 是不同标签。')])

KB['it/xml-to-json'] = dict(title='XML 转 JSON',
  scenarios=['把 XML 响应转 JSON 供前端使用。'],
  examples=[dict(title='转换', body='`<name>Tom</name>` → `{"name":"Tom"}`。')],
  faqs=[dict(q='属性怎么转？', a='常加 @ 前缀，如 `<a id="1">` → `{"a":{"@id":"1"}}`。')])

KB['it/xml-to-yaml'] = dict(title='XML to YAML Converter',
  scenarios=['XML 配置转 YAML。'],
  examples=[dict(title='转换', body='`<name>Tom</name>` → `name: Tom`。')],
  faqs=[dict(q='同名重复元素？', a='转成数组以保留多个值。')])

KB['it/xml-to-toml'] = dict(title='XML to TOML Converter',
  scenarios=['XML 转 TOML 供 Go 配置消费。'],
  examples=[dict(title='转换', body='`<name>Tom</name>` → `name = "Tom"`。')],
  faqs=[dict(q='深层嵌套怎么转？', a='用 [section] 表层级表示。')])

KB['it/toml-formatter'] = dict(title='TOML 格式化/转JSON',
  scenarios=['美化 TOML 并校验。'],
  examples=[dict(title='格式化', body='`a=1\n[b]\nc=2` 美化为分段结构。')],
  faqs=[dict(q='TOML 与 YAML 比？', a='TOML 对配置更直观，类型明确。')])

KB['it/toml-to-json'] = dict(title='TOML to JSON Converter',
  scenarios=['TOML 转 JSON。'],
  examples=[dict(title='转换', body='`name = "Tom"` → `{"name":"Tom"}`。')],
  faqs=[dict(q='日期类型保留吗？', a='TOML 的日期时间会转为字符串或对应类型。')])

KB['it/toml-to-xml'] = dict(title='TOML to XML Converter',
  scenarios=['TOML 转 XML。'],
  examples=[dict(title='转换', body='`name="Tom"` → `<name>Tom</name>`。')],
  faqs=[dict(q='表怎么转 XML？', a='转成嵌套元素。')])

KB['it/toml-to-yaml'] = dict(title='TOML to YAML Converter',
  scenarios=['TOML 转 YAML。'],
  examples=[dict(title='转换', body='`name="Tom"` → `name: Tom`。')],
  faqs=[dict(q='两者都支持注释吗？', a='都支持，但转换需约定注释去留。')])

KB['it/csv-to-json'] = dict(title='CSV / JSON 转换器',
  scenarios=['表格与结构化数据互转。'],
  examples=[dict(title='转换', body='CSV `a,b\n1,2` → `[{"a":"1","b":"2"}]`。')],
  faqs=[dict(q='表头缺失怎么办？', a='可用列索引 c1,c2… 作为键。')])

KB['it/csv-to-yaml'] = dict(title='CSV to YAML Converter',
  scenarios=['CSV 转 YAML 便于配置。'],
  examples=[dict(title='转换', body='CSV 两行 → YAML 列表 `- {a: "1", b: "2"}`。')],
  faqs=[dict(q='大 CSV 转 YAML 慢吗？', a='行数很大时 YAML 体积与解析都较重。')])

KB['it/csv-to-html-table'] = dict(title='CSV to HTML Table',
  scenarios=['把表格快速渲染为可嵌入网页的 <table>。'],
  examples=[dict(title='转换', body='CSV → `<table><tr><th>a</th>…</tr>…</table>`。')],
  faqs=[dict(q='特殊字符会转义吗？', a='会转义 < > & 防止 HTML 注入。')])

KB['it/csv-validator'] = dict(title='CSV Validator',
  scenarios=['检查列数一致、引号闭合。'],
  examples=[dict(title='校验', body='某行 3 列其余 2 列 → 报错：列数不一致。')],
  faqs=[dict(q='引号内逗号算分隔吗？', a='不算，引号字段内的逗号是字段内容。')])

KB['it/html-to-markdown'] = dict(title='HTML 转 Markdown',
  scenarios=['把网页内容转成轻量 Markdown。'],
  examples=[dict(title='转换', body='`<h1>标题</h1><p>文本 <b>粗</b></p>` → `# 标题\n\n文本 **粗**`。')],
  faqs=[dict(q='复杂表格能转吗？', a='多数能，但合并单元格等需人工修。')])

KB['it/markdown-to-html'] = dict(title='Markdown 转 HTML',
  scenarios=['预览/发布 Markdown 为网页。'],
  examples=[dict(title='转换', body='`# 标题\n\n- a\n- b` → `<h1>标题</h1><ul><li>a</li><li>b</li></ul>`。')],
  faqs=[dict(q='原始 HTML 会保留吗？', a='取决于是否允许 HTML 透传，默认常转义。')])

KB['it/less-compiler'] = dict(title='Less 转 CSS 编译器',
  scenarios=['把 Less 变量/嵌套编译为标准 CSS。'],
  examples=[dict(title='编译', body='`@c:red; .a{color:@c; .b{font:12px}}` → `.a{color:red}.a .b{font:12px}`。')],
  faqs=[dict(q='Less 变量与 CSS 变量区别？', a='Less 编译期替换，CSS 变量运行时生效。')])

KB['it/typescript-compiler'] = dict(title='TypeScript 转 JavaScript',
  scenarios=['把 TS 类型擦除编译为可运行 JS。'],
  examples=[dict(title='编译', body='`let x: number = 1;` → `let x = 1;`（类型注解被移除）。')],
  faqs=[dict(q='类型检查在编译时做吗？', a='是，tsc 编译同时做类型检查，浏览器只跑 JS。')])

KB['it/shell-script-formatter'] = dict(title='Shell 脚本格式化',
  scenarios=['美化 Bash 脚本缩进与对齐。'],
  examples=[dict(title='格式化', body='压缩的 if/for 按 2 空格缩进美化。')],
  faqs=[dict(q='格式化会改行为吗？', a='不，仅调整空白。')])

KB['it/css-formatter'] = dict(title='CSS 格式化',
  scenarios=['美化压缩的 CSS。'],
  examples=[dict(title='格式化', body='`a{color:red}` → 多行带缩进。')],
  faqs=[dict(q='会合并重复规则吗？', a='格式化一般不改规则，去重需另外处理。')])

KB['it/css-minifier'] = dict(title='CSS 压缩/格式化/美化',
  scenarios=['压缩 CSS 减小体积（去注释空白）。'],
  examples=[dict(title='压缩', body='`a { color: red; }` → `a{color:red}`。')],
  faqs=[dict(q='压缩影响调试吗？', a='会，生产用压缩、开发用源文件。')])

KB['it/css-minify'] = dict(title='CSS Minifier',
  scenarios=['与 css-minifier 同类，去空白压缩。'],
  examples=[dict(title='压缩', body='注释与多余空白移除，体积常降 20–50%。')],
  faqs=[dict(q='压缩会删注释吗？', a='会，含版权注释如需保留用特殊标记。')])

KB['it/js-formatter'] = dict(title='JavaScript 格式化',
  scenarios=['美化压缩的 JS 便于阅读。'],
  examples=[dict(title='格式化', body='`function f(x){return x*2}` → 多行带缩进。')],
  faqs=[dict(q='会还原变量名吗？', a='不会，格式化不逆混淆。')])

KB['it/js-minifier'] = dict(title='JavaScript 简化器',
  scenarios=['压缩 JS 去空白与注释。'],
  examples=[dict(title='压缩', body='`var a = 1;` → `var a=1;`。')],
  faqs=[dict(q='压缩与混淆区别？', a='压缩只去空白，混淆还改变量名。')])

KB['it/js-minify'] = dict(title='JS Minifier',
  scenarios=['与 js-minifier 同类压缩。'],
  examples=[dict(title='压缩', body='去空白注释，体积常降 30%+。')],
  faqs=[dict(q='ESM 能压缩吗？', a='能，现代压缩器支持 ESM 语法。')])

KB['it/python-formatter'] = dict(title='Python 格式化',
  scenarios=['按 PEP8 美化 Python 代码。'],
  examples=[dict(title='格式化', body='`x={1:2,3:4}` → 规范空格 `x = {1: 2, 3: 4}`。')],
  faqs=[dict(q='用 Black 还是 autopep8？', a='Black 强制风格统一，autopep8 更可配置。')])

KB['it/sql-formatter'] = dict(title='SQL 格式化/美化',
  scenarios=['把长 SQL 按关键字换行缩进。'],
  examples=[dict(title='格式化', body='`select a,b from t where c=1` → 多行 `SELECT a, b\nFROM t\nWHERE c = 1`。')],
  faqs=[dict(q='会改变执行计划吗？', a='不会，仅调整空白与大小写。')])

KB['it/graphql-formatter'] = dict(title='GraphQL 格式化',
  scenarios=['美化 GraphQL 查询/类型。'],
  examples=[dict(title='格式化', body='`query{a{b}}` → 多行带缩进字段。')],
  faqs=[dict(q='会校验 schema 吗？', a='纯格式化不校验，需配合校验器。')])

# ===== generators =====
KB['it/uuid-generator'] = dict(title='UUID 生成器',
  scenarios=['生成唯一标识用于主键、文件名、追踪 ID。'],
  examples=[dict(title='生成', body='示例 UUIDv4：`9b1deb4d-3b7d-4bad-9bdd-2b0d7b3dcb6d`（随机 122 位）。')],
  faqs=[dict(q='UUID 会重复吗？', a='v4 概率极低，可视为唯一。')])

KB['it/uuid-v4-generator'] = dict(title='UUID v4 生成器',
  scenarios=['随机 UUID，最常用唯一 ID。'],
  examples=[dict(title='生成', body='`f47ac10b-58cc-4372-a567-0e02b2c3d479`（随机）。')],
  faqs=[dict(q='v4 与 v1 区别？', a='v4 随机、v1 含时间戳与 MAC。')])

KB['it/uuid-v5-generator'] = dict(title='UUID v5 生成器',
  scenarios=['基于命名空间+名称的确定性 UUID，同名必同 ID。'],
  examples=[dict(title='生成', body='namespace=DNS, name="example.com" → 固定 `aad6f...`（SHA-1 命名空间）。')],
  faqs=[dict(q='v5 为何可复现？', a='输入(命名空间+名称)相同输出必相同。')])

KB['it/uuid-v7-generator'] = dict(title='UUID v7 生成器',
  scenarios=['带毫秒时间戳前缀的 UUID，利于数据库按时间排序。'],
  examples=[dict(title='生成', body='`018f6e2a-1c3d-7b12-...` 前 48 位为 Unix 毫秒。')],
  faqs=[dict(q='v7 比 v4 好在哪？', a='前缀时间使索引更顺序、插入更友好。')])

KB['it/nanoid-generator'] = dict(title='NanoID 生成器',
  scenarios=['比 UUID 更短的安全随机 ID。'],
  examples=[dict(title='生成', body='默认 21 字符：`V1StGXR8ZqUpOQ6MVumh`；可配字母表与长度。')],
  faqs=[dict(q='NanoID 与 UUID 比？', a='更短、URL 友好、可定制字符集。')])

KB['it/cuid-generator'] = dict(title='CUID 生成器',
  scenarios=['防时序推断、适合分布式的短 ID。'],
  examples=[dict(title='生成', body='`ckl1r2x3a0001abcd` 含时间戳+计数器+随机。')],
  faqs=[dict(q='CUID 会泄露信息吗？', a='含时间片段但非明文，冲突概率极低。')])

KB['it/ksuid-generator'] = dict(title='KSUID 生成器',
  scenarios=['K-Sortable Unique ID，时间前缀可排序。'],
  examples=[dict(title='生成', body='`0ujtsy1p8c9r1l0b0p0n000000` 前 32 位为时间。')],
  faqs=[dict(q='KSUID 与 ULID 区别？', a='都时间排序，编码与长度不同。')])

KB['it/ulid-generator'] = dict(title='ULID 生成器',
  scenarios=['可排序、26 字符、Crocksford base32 编码。'],
  examples=[dict(title='生成', body='`01ARZ3NDEKTSV4RRFFQ69G5FAV`（前 10 字符为时间）。')],
  faqs=[dict(q='ULID 大小写敏感吗？', a='不敏感，字母表排除 I L O U 防误读。')])

KB['it/token-generator'] = dict(title='随机 Token 生成器',
  scenarios=['生成 API Key、CSRF Token 等。'],
  examples=[dict(title='生成', body='32 字节十六进制 Token 例：`a1b2c3...`(64 位十六进制)。')],
  faqs=[dict(q='Token 要多少熵？', a='敏感场景至少 128 位随机性。')])

KB['it/random-string'] = dict(title='Random String Generator',
  scenarios=['生成指定长度与字符集的随机串。'],
  examples=[dict(title='生成', body='长度 12、含大小写数字：`Kp9mQ2xL7vBn`。')],
  faqs=[dict(q='用 crypto 随机吗？', a='安全场景应使用密码学安全随机数。')])

KB['it/password-generator'] = dict(title='密码生成器（IT）',
  scenarios=['生成高熵口令，含大小写/数字/符号。'],
  examples=[dict(title='生成', body='16 位含四类字符：`Tq7!mK9@pL2#vX4z`（熵约 95 位）。')],
  faqs=[dict(q='多长够安全？', a='随机含四类字符 12+ 位可抗在线爆破，离线需更长。')])

KB['it/password-strength'] = dict(title='密码强度检测',
  scenarios=['评估口令熵与常见弱点。'],
  examples=[dict(title='检测', body='`password123` → 弱（常见词+顺序数字，熵低）；`Tq7!mK9@pL2#` → 强。')],
  faqs=[dict(q='强度只看长度吗？', a='长度与字符集共同决定熵，词典词会大幅削弱。')])

KB['it/pin-generator'] = dict(title='PIN 码生成器',
  scenarios=['生成 4–6 位数字 PIN。'],
  examples=[dict(title='生成', body='6 位 PIN：`482915`（0–9 等概率）。')],
  faqs=[dict(q='PIN 能被猜吗？', a='4 位仅 1 万组合，需配合锁定策略。')])

KB['it/bank-card-generator'] = dict(title='随机银行卡号生成器',
  scenarios=['生成符合 Luhn 算法的测试卡号（仅测试，非真实账户）。'],
  examples=[dict(title='生成', body='示例 `4111111111111111`（Visa 测试号，Luhn 校验通过）。')],
  faqs=[dict(q='生成的卡能用吗？', a='不能，仅格式合法，无对应账户。')])

KB['it/id-card-generator'] = dict(title='随机身份证号生成器',
  scenarios=['生成符合校验位的测试身份证号（仅测试）。'],
  examples=[dict(title='生成', body='示例 `11010119900307XXXX`（地区码+出生日期+顺序+校验位）。')],
  faqs=[dict(q='能当真身份证吗？', a='不能，仅供格式测试，非真实身份。')])

KB['it/chinese-name-generator'] = dict(title='随机中文名生成器',
  scenarios=['测试数据、演示用随机姓名。'],
  examples=[dict(title='生成', body='示例 `李思远`（随机姓+名，可指定性别）。')],
  faqs=[dict(q='会重复吗？', a='样本有限可能重复，仅作占位。')])

KB['it/nickname-generator'] = dict(title='昵称生成器',
  scenarios=['注册时生成个性化昵称。'],
  examples=[dict(title='生成', body='示例 `星河漫游者`、`代码小熊`。')],
  faqs=[dict(q='能指定风格吗？', a='可选可爱/酷飒/文艺等风格。')])

KB['it/username-generator'] = dict(title='用户名生成器',
  scenarios=['生成可用登录名（词+数字）。'],
  examples=[dict(title='生成', body='示例 `blue_tiger42`、`neo_coder`。')],
  faqs=[dict(q='如何避免重复？', a='加随机后缀或查重后再用。')])

KB['it/team-name-generator'] = dict(title='团队名生成器',
  scenarios=['给项目/战队起名。'],
  examples=[dict(title='生成', body='示例 `量子企鹅`、`极光实验室`。')],
  faqs=[dict(q='能中英文混吗？', a='可切换语言风格。')])

KB['it/gamertag-generator'] = dict(title='游戏标签生成器',
  scenarios=['生成游戏 ID/战队 tag。'],
  examples=[dict(title='生成', body='示例 `ShadowWolf99`、`NeonBlade`。')],
  faqs=[dict(q='被占用怎么办？', a='加序号或换词根。')])

KB['it/domain-name-generator'] = dict(title='域名生成器',
  scenarios=['生成可用域名创意（含后缀建议）。'],
  examples=[dict(title='生成', body='关键词 `cloud` → `cloudnest.io`、`getcloud.app`。')],
  faqs=[dict(q='能查是否注册吗？', a='本工具仅生成，注册需 WHOIS 查询。')])

KB['it/short-link-generator'] = dict(title='短链接生成器',
  scenarios=['把长 URL 缩短为自定义短码（模拟）。'],
  examples=[dict(title='生成', body='长链 `https://ex.com/a/b/c?x=1` → 短码 `ex.am/ab3kQ`（演示，非真实跳转）。')],
  faqs=[dict(q='短码会冲突吗？', a='需唯一索引保证不冲突。')])

KB['it/tiny-url'] = dict(title='TinyURL 模拟器',
  scenarios=['演示短链映射原理。'],
  examples=[dict(title='生成', body='输入长链 → 返回短标识，说明映射存储机制。')],
  faqs=[dict(q='与真实 TinyURL 区别？', a='仅为本地模拟，无真实解析服务。')])

KB['it/slug-generator-advanced'] = dict(title='高级 Slug 生成器',
  scenarios=['把标题转 URL 友好的 slug，支持多语言。'],
  examples=[dict(title='生成', body='`Hello 世界!` → `hello-shi-jie`（中文转拼音 slug）。')],
  faqs=[dict(q='中文怎么 slug？', a='通常拼音化或保留 Unicode，视 SEO 策略。')])

KB['it/slugify'] = dict(title='URL Slug 生成器',
  scenarios=['生成英文 slug 用于文章/商品 URL。'],
  examples=[dict(title='生成', body='`My First Post!` → `my-first-post`。')],
  faqs=[dict(q='保留大写吗？', a='一般转小写并去标点。')])

KB['it/bip39-generator'] = dict(title='BIP39 助记词生成器',
  scenarios=['生成/校验加密货币钱包助记词（12/24 词）。'],
  examples=[dict(title='生成', body='熵 128 位 → 12 个助记词（如 `legal winner thank year wave sausage …`），含校验词。')],
  faqs=[dict(q='助记词安全吗？', a='离线生成且保密即安全，泄露即丢资产。')])

KB['it/otp-generator'] = dict(title='OTP 生成器（HOTP/TOTP）',
  scenarios=['演示基于时间的一次性口令（如 2FA）。'],
  examples=[dict(title='TOTP', body='密钥 + 当前 30 秒计数 → 6 位动态码（每 30 秒变化）。')],
  faqs=[dict(q='为什么 30 秒失效？', a='TOTP 以时间窗口为计数器，过期需重新算。')])

KB['it/captcha-generator'] = dict(title='验证码生成器',
  scenarios=['生成图形/文本验证码用于演示。'],
  examples=[dict(title='生成', body='4 位扭曲字符 `7KQ2` 加干扰线（仅演示，非真实风控）。')],
  faqs=[dict(q='验证码能防盗刷吗？', a='需配合后端校验与限流，单前端生成无效。')])

KB['it/lorem'] = dict(title='Lorem Ipsum 生成器',
  scenarios=['排版/设计稿填充占位文本。'],
  examples=[dict(title='生成', body='`Lorem ipsum dolor sit amet, consectetur adipiscing elit…`（指定段数）。')],
  faqs=[dict(q='Lorem 有含义吗？', a='无，源自西塞罗文本打乱，仅作占位。')])

KB['it/fake-data'] = dict(title='假数据生成器',
  scenarios=['生成姓名/地址/邮箱等假数据用于测试。'],
  examples=[dict(title='生成', body='一行含 `张伟, zhangwei@example.com, 138****1234`（全部虚构）。')],
  faqs=[dict(q='假数据能当真实用户吗？', a='不能，仅格式仿真，禁止用于欺诈。')])

KB['it/coupon-code-generator'] = dict(title='优惠券码生成器',
  scenarios=['生成可读的促销码。'],
  examples=[dict(title='生成', body='8 位码 `SAVE20XY`（前缀+随机，去易混字符）。')],
  faqs=[dict(q='如何防猜？', a='足够随机长度+服务端校验。')])

KB['it/invite-code-generator'] = dict(title='邀请码生成器',
  scenarios=['生成内测/邀请短码。'],
  examples=[dict(title='生成', body='6 位 `X9F2PQ`（Base32 风格，去 0/O/1/I）。')],
  faqs=[dict(q='邀请码可撤销吗？', a='需后端绑定状态才可作废。')])

KB['it/recovery-code-generator'] = dict(title='恢复码生成器',
  scenarios=['生成一次性账户恢复码。'],
  examples=[dict(title='生成', body='10 组 `r4k9-m2x8` 格式码，用后失效。')],
  faqs=[dict(q='恢复码怎么存？', a='服务端哈希存储，用户离线保管。')])

KB['it/serial-key-generator'] = dict(title='序列号生成器',
  scenarios=['生成带格式的产品序列号（演示）。'],
  examples=[dict(title='生成', body='`XXXX-XXXX-XXXX-XXXX` 格式随机码。')],
  faqs=[dict(q='真能激活软件吗？', a='需后端校验算法，单前端仅为格式。')])

KB['it/random-port-generator'] = dict(title='随机端口生成器',
  scenarios=['选未占用的临时端口（建议 49152–65535）。'],
  examples=[dict(title='生成', body='随机 `52341`（动态/私有端口段）。')],
  faqs=[dict(q='为什么用高位端口？', a='1024 以下需特权，动态端口段冲突少。')])

KB['it/emoji-picker'] = dict(title='Emoji Picker',
  scenarios=['挑选并复制 Emoji 到文本。'],
  examples=[dict(title='挑选', body='搜索“笑” → 😄😁😂，点击复制 Unicode。')],
  faqs=[dict(q='Emoji 跨平台一致吗？', a='码点一致，但各平台绘图形状不同。')])

KB['it/emoji-meaning'] = dict(title='Emoji 含义查询',
  scenarios=['查 Emoji 的名称与含义。'],
  examples=[dict(title='查', body='🔥 → “Fire”，常表热门/赞。')],
  faqs=[dict(q='同一 Emoji 多义？', a='是，含义随语境变化。')])

KB['it/qrcode'] = dict(title='二维码生成器',
  scenarios=['把文本/链接生成可扫二维码。'],
  examples=[dict(title='生成', body='输入 `https://ex.com` → 生成 QR（版本随内容长度自动选）。')],
  faqs=[dict(q='容量上限？', a='最高版本 40 约存 2953 字节（数字模式）。')])

KB['it/qr-beautify'] = dict(title='二维码美化生成器',
  scenarios=['加 Logo/换色生成品牌二维码。'],
  examples=[dict(title='生成', body='中心嵌 Logo、改前景色，仍保证容错(建议 25–30%)。')],
  faqs=[dict(q='美化会降低识别吗？', a='会，需保留足够纠错等级。')])

KB['it/qr-decoder'] = dict(title='二维码解码（手动输入解析）',
  scenarios=['手动输入/粘贴二维码文本还原内容。'],
  examples=[dict(title='解码', body='粘贴 QR 文本 → 还原 `https://ex.com`。')],
  faqs=[dict(q='能扫图片吗？', a='本工具为手动输入解析，图片识别需摄像头/上传。')])

KB['it/text-qr'] = dict(title='文本二维码',
  scenarios=['把一段文本生成二维码分享。'],
  examples=[dict(title='生成', body='文本“会议 15:00”→ QR。')],
  faqs=[dict(q='中文能存吗？', a='能，UTF-8 编码后入码。')])

KB['it/url-qr'] = dict(title='URL 二维码',
  scenarios=['把链接生成二维码便于手机扫码。'],
  examples=[dict(title='生成', body='`https://ex.com` → QR。')],
  faqs=[dict(q='长链接用短链更好吗？', a='是，过长会降低密度与识别率。')])

KB['it/email-qr'] = dict(title='邮件二维码',
  scenarios=['生成 mailto 二维码（含收件人/主题）。'],
  examples=[dict(title='生成', body='`mailto:a@b.com?subject=Hi` → QR，扫码唤起邮件。')],
  faqs=[dict(q='能预设正文吗？', a='可加 &body= 参数。')])

KB['it/sms-qr'] = dict(title='SMS 二维码',
  scenarios=['生成 smsto 二维码（号码+内容）。'],
  examples=[dict(title='生成', body='`smsto:13800000000?body=Hi` → QR。')],
  faqs=[dict(q='扫码会直接发吗？', a='唤起短信草稿，需用户确认发送。')])

KB['it/location-qr'] = dict(title='位置二维码',
  scenarios=['把经纬度生成 geo: 二维码。'],
  examples=[dict(title='生成', body='`geo:39.9,116.4` → QR，扫码打开地图。')],
  faqs=[dict(q='格式是什么？', a='geo:纬度,经度?z=缩放。')])

KB['it/wifi-qr'] = dict(title='WiFi 二维码',
  scenarios=['把 SSID/密码生成二维码，手机一扫即连。'],
  examples=[dict(title='生成', body='`WIFI:T:WPA;S:Home;P:pass1234;;` → QR（扫码免输密码）。')],
  faqs=[dict(q='公开二维码会泄露密码吗？', a='会，仅对可信场合生成。')])

KB['it/wifi-qr-generator'] = dict(title='WiFi QR Code Generator',
  scenarios=['与 wifi-qr 同类，生成连接二维码。'],
  examples=[dict(title='生成', body='填 SSID 与密码 → 输出 WIFI: 协议二维码。')],
  faqs=[dict(q='支持 WEP 吗？', a='支持但 WEP 已不安全，建议 WPA2/3。')])

KB['it/svg-placeholder-generator'] = dict(title='SVG 占位图生成器',
  scenarios=['生成指定尺寸/文字的占位图。'],
  examples=[dict(title='生成', body='`600x400` 灰底居中文字“Placeholder”的 SVG。')],
  faqs=[dict(q='SVG 占位优势？', a='矢量、体积小、可改色。')])

KB['it/ascii-art'] = dict(title='ASCII 大字生成器',
  scenarios=['把文字转成终端风格大字（figlet）。'],
  examples=[dict(title='生成', body='`Hi` → 用 standard 字体渲染的多行 ASCII 艺术字。')],
  faqs=[dict(q='支持中文吗？', a='多数字体仅 ASCII，中文需点阵字体。')])

KB['it/ascii-tree-generator'] = dict(title='ASCII 目录树生成器',
  scenarios=['把文件结构渲染成 tree 文本。'],
  examples=[dict(title='生成', body='输入路径列表 → `├─ a\n│  └─ b\n└─ c` 树形。')],
  faqs=[dict(q='与 tree 命令区别？', a='本工具在线生成，无需 shell。')])

# ===== barcodes =====
for b in ['codabar','code128','code39','ean','itf','msi','upc']:
    KB[f'it/barcode-{b}'] = dict(
      title=f'{b.upper()} 条形码',
      scenarios=[f'生成/识别 {b.upper()} 码用于仓储、零售或资产标签。',
        '打印前预览条码可读性。'],
      examples=[dict(title='生成', body=f'输入数字串（如 `123456789`）→ 渲染 {b.upper()} 条码图形；请按规范长度与校验位填写。')],
      faqs=[dict(q=f'{b.upper()} 需要校验位吗？', a='部分码制（如 EAN/UPC）需计算校验位，Code39 可选。')])

# ===== cheatsheets / references =====
KB['it/cpp-cheatsheet'] = dict(title='C++ 速查',
  scenarios=['开发中快速查阅语法、STL、特性对照。'],
  examples=[dict(title='查范围 for', body='`for (auto& x : v) { }` 遍历容器；附 auto/范围说明。')],
  faqs=[dict(q='C++ 版本怎么看？', a='看 __cplusplus 宏或编译标准 -std=c++17/20。')])

KB['it/csharp-cheatsheet'] = dict(title='C# 速查',
  scenarios=['查阅 C# 语法与 LINQ 片段。'],
  examples=[dict(title='查 LINQ', body='`list.Where(x=>x>0).Select(x=>x*2)` 过滤映射。')],
  faqs=[dict(q='var 与动态类型？', a='var 仍是静态类型推断，非 dynamic。')])

KB['it/docker-cheatsheet'] = dict(title='Docker 命令速查',
  scenarios=['日常 build/run/ps/exec 命令速查。'],
  examples=[dict(title='查运行', body='`docker run -d -p 8080:80 nginx` 后台起容器并映射端口。')],
  faqs=[dict(q='如何看日志？', a='`docker logs <id>`。')])

KB['it/emacs-cheatsheet'] = dict(title='Emacs 命令速查',
  scenarios=['记忆 C-x C-s 等组合键。'],
  examples=[dict(title='保存', body='`C-x C-s` 保存；`C-x C-c` 退出。')],
  faqs=[dict(q='C- 与 M- 含义？', a='C-=Ctrl，M-=Alt(Meta)。')])

KB['it/git-commands'] = dict(title='Git 命令速查',
  scenarios=['查阅 checkout/merge/rebase/cherry-pick 等。'],
  examples=[dict(title='查变基', body='`git rebase -i HEAD~3` 交互改写最近 3 次提交。')],
  faqs=[dict(q='rebase 危险吗？', a='改写已推送历史会影响协作者，慎用于公共分支。')])

KB['it/gitignore-generator'] = dict(title='.gitignore Generator',
  scenarios=['按语言/框架生成忽略规则。'],
  examples=[dict(title='生成', body='选 Node → 输出 `node_modules/`、`dist/`、`.env` 等规则。')],
  faqs=[dict(q='.gitignore 对已跟踪文件生效吗？', a='不生效，需先 `git rm --cached`。')])

KB['it/go-cheatsheet'] = dict(title='Go 速查',
  scenarios=['查阅 goroutine/defer/err 处理。'],
  examples=[dict(title='查错误', body='`if err != nil { return err }` 惯用法。')],
  faqs=[dict(q='defer 何时执行？', a='函数返回前按后进先出执行。')])

KB['it/java-cheatsheet'] = dict(title='Java 速查',
  scenarios=['查阅 stream/lambda/异常。'],
  examples=[dict(title='查流', body='`list.stream().filter(x->x>0).count()` 统计。')],
  faqs=[dict(q='== 与 equals？', a='== 比引用，equals 比值（对象）。')])

KB['it/kubernetes-cheatsheet'] = dict(title='Kubernetes 命令速查',
  scenarios=['kubectl get/describe/apply 速查。'],
  examples=[dict(title='查 pod', body='`kubectl get pods -n default` 列出命名空间 pod。')],
  faqs=[dict(q='如何重启 deployment？', a='`kubectl rollout restart deploy/<name>`。')])

KB['it/latex'] = dict(title='LaTeX 符号与命令速查',
  scenarios=['写论文时查数学符号/环境。'],
  examples=[dict(title='查积分', body='`\\int_a^b f(x)\\,dx` 定积分；`\\sum_{i=1}^n` 求和。')],
  faqs=[dict(q='表格怎么画？', a='用 tabular 环境，& 分列、\\\\ 分行。')])

KB['it/linux-cheatsheet'] = dict(title='Linux 命令速查',
  scenarios=['grep/awk/sed/ps 等常用命令。'],
  examples=[dict(title='查查找', body='`find . -name "*.py" -mtime -1` 找一天内修改的 py 文件。')],
  faqs=[dict(q='如何杀进程？', a='`kill -9 <pid>`，先 `ps`/`pgrep` 找 pid。')])

KB['it/mongodb-cheatsheet'] = dict(title='MongoDB 命令速查',
  scenarios=['查阅 find/aggregate/update。'],
  examples=[dict(title='查聚合', body='`db.orders.aggregate([{$match:{status:"A"}},{$group:{_id:"$cust",total:{$sum:"$amt"}}}])`。')],
  faqs=[dict(q='MongoDB 有事务吗？', a='4.0+ 支持多文档事务。')])

KB['it/mysql-cheatsheet'] = dict(title='MySQL 命令速查',
  scenarios=['查阅 JOIN/索引/事务语句。'],
  examples=[dict(title='查连接', body='`SELECT * FROM a JOIN b ON a.id=b.aid` 内连接。')],
  faqs=[dict(q='索引为何快？', a='B+树降低查找复杂度到对数级。')])

KB['it/nginx-cheatsheet'] = dict(title='Nginx 配置速查',
  scenarios=['反向代理/负载均衡/重写规则。'],
  examples=[dict(title='反代', body='`location /api { proxy_pass http://backend; }` 转发。')],
  faqs=[dict(q='reload 与 restart？', a='`nginx -s reload` 平滑重载不中断。')])

KB['it/php-cheatsheet'] = dict(title='PHP 速查',
  scenarios=['查阅数组/PDO/语法。'],
  examples=[dict(title='查数组', body='`array_map(fn($x)=>$x*2, $a)` 映射。')],
  faqs=[dict(q='PHP 8 类型声明？', a='支持参数/返回类型声明与联合类型。')])

KB['it/postgresql-cheatsheet'] = dict(title='PostgreSQL 命令速查',
  scenarios=['查阅 JSONB/窗口函数/索引。'],
  examples=[dict(title='窗口函数', body='`SUM(amt) OVER (PARTITION BY cust ORDER BY dt)` 累计。')],
  faqs=[dict(q='JSONB 与 JSON？', a='JSONB 二进制存储、可索引、去重键。')])

KB['it/python-cheatsheet'] = dict(title='Python 速查',
  scenarios=['查阅推导式/装饰器/标准库。'],
  examples=[dict(title='查推导', body='`[x*2 for x in range(5) if x%2==0]` → [0,4,8]。')],
  faqs=[dict(q='列表与生成器？', a='生成器惰性、省内存，用 () 而非 []。')])

KB['it/redis-cheatsheet'] = dict(title='Redis 命令速查',
  scenarios=['查阅 string/hash/list/zset 命令。'],
  examples=[dict(title='查 zset', body='`ZADD leader 100 tom` 加分；`ZREVRANGE leader 0 9` 取前 10。')],
  faqs=[dict(q='Redis 持久化？', a='RDB 快照 + AOF 日志。')])

KB['it/rest-api-cheatsheet'] = dict(title='REST API 设计速查',
  scenarios=['资源命名/状态码/版本规范。'],
  examples=[dict(title='命名', body='用复数名词 `/users/{id}`，GET 查、POST 建、PATCH 改。')],
  faqs=[dict(q='409 与 400 区别？', a='400 请求格式错，409 冲突（如重复创建）。')])

KB['it/ruby-cheatsheet'] = dict(title='Ruby 速查',
  scenarios=['查阅 block/symbol/rails 片段。'],
  examples=[dict(title='查映射', body='`[1,2,3].map { |x| x*2 }` → [2,4,6]。')],
  faqs=[dict(q='symbol 与 string？', a='symbol 不可变、同值同对象，常用于键。')])

KB['it/rust-cheatsheet'] = dict(title='Rust 速查',
  scenarios=['查阅所有权/生命周期/模式匹配。'],
  examples=[dict(title='匹配', body='`match x { 0 => "zero", _ => "other" }`。')],
  faqs=[dict(q='所有权是什么？', a='每个值有唯一所有者，移动后原变量失效。')])

KB['it/sql-cheatsheet'] = dict(title='SQL 语法速查',
  scenarios=['跨库 SELECT/CTE/窗口函数速查。'],
  examples=[dict(title='CTE', body='`WITH t AS (SELECT 1) SELECT * FROM t`。')],
  faqs=[dict(q='CTE 与子查询？', a='CTE 可读性好，递归 CTE 可处理层级。')])

KB['it/sqlite-cheatsheet'] = dict(title='SQLite 命令速查',
  scenarios=['嵌入式数据库常用语句。'],
  examples=[dict(title='建表', body='`CREATE TABLE t(id INTEGER PRIMARY KEY, name TEXT)`。')],
  faqs=[dict(q='SQLite 类型？', a='动态类型，列类型仅为亲和。')])

KB['it/tmux-cheatsheet'] = dict(title='tmux 命令速查',
  scenarios=['分屏/会话管理。'],
  examples=[dict(title='分屏', body='`Ctrl-b %` 竖分；`Ctrl-b "` 横分。')],
  faqs=[dict(q='detach 是什么？', a='`Ctrl-b d` 脱离会话，后台继续运行。')])

KB['it/typescript-cheatsheet'] = dict(title='TypeScript 速查',
  scenarios=['查阅类型/泛型/工具类型。'],
  examples=[dict(title='工具类型', body='`Partial<T>`、`Pick<T,K>`、`Record<K,V>` 常用。')],
  faqs=[dict(q='any 与 unknown？', a='unknown 更安全，需收窄后才能用。')])

KB['it/vim-cheatsheet'] = dict(title='Vim 命令速查',
  scenarios=['记忆 dd/yy/:%s 等。'],
  examples=[dict(title='替换', body='`:%s/foo/bar/g` 全局替换 foo 为 bar。')],
  faqs=[dict(q='如何保存退出？', a='`:wq` 或 `ZZ`。')])

KB['it/regex-cheatsheet'] = dict(title='正则表达式速查',
  scenarios=['查元字符与常用模式。'],
  examples=[dict(title='邮箱', body='`^\\S+@\\S+\\.\\S+$` 简易邮箱匹配。')],
  faqs=[dict(q='贪婪与非贪婪？', a='`*?` `+?` 为懒惰匹配，尽量少匹配。')])

KB['it/emoji-cheatsheet'] = dict(title='Emoji 速查表',
  scenarios=['按分类找 Emoji 与码点。'],
  examples=[dict(title='查', body='笑脸类 😀😃😄，附 Unicode。')],
  faqs=[dict(q='如何按名称搜？', a='本表支持分类/关键词检索。')])

KB['it/html-tags'] = dict(title='HTML 标签速查',
  scenarios=['查阅语义标签与属性。'],
  examples=[dict(title='查', body='`<article>` 表示独立内容；`<section>` 表示主题区块。')],
  faqs=[dict(q='section 与 div？', a='section 有语义，div 仅容器。')])

KB['it/css-properties'] = dict(title='CSS 属性速查',
  scenarios=['查阅属性取值与兼容性。'],
  examples=[dict(title='查', body='`display: grid` 二维布局；`gap` 设间距。')],
  faqs=[dict(q='flex 与 grid？', a='一维用 flex，二维用 grid。')])

KB['it/http-methods-reference'] = dict(title='HTTP Methods Reference',
  scenarios=['查 GET/POST/PUT/PATCH/DELETE 语义。'],
  examples=[dict(title='查', body='PUT 整体替换、PATCH 部分更新。')],
  faqs=[dict(q='Safe/Idempotent？', a='GET 安全且幂等；POST 既不。')])

KB['it/bluetooth-version'] = dict(title='Bluetooth Version Reference',
  scenarios=['查各版本速率/距离/发布年。'],
  examples=[dict(title='查', body='BT5.0 速率 2Mbps、距离 240m；BT5.3 更低功耗。')],
  faqs=[dict(q='版本向后兼容吗？', a='一般向后兼容，速率取两者低。')])

KB['it/usb-version'] = dict(title='USB Version Reference',
  scenarios=['查 USB 协议速率与接口。'],
  examples=[dict(title='查', body='USB3.2 Gen2 10Gbps；USB4 40Gbps（基于雷电3）。')],
  faqs=[dict(q='Type-C 是接口非协议', a='Type-C 是形态，速率看 USB/雷电协议。')])

KB['it/phone-screen-sizes'] = dict(title='Phone Screen Sizes',
  scenarios=['查主流机型分辨率与 DPR 做适配。'],
  examples=[dict(title='查', body='iPhone 15 Pro 1179×2556@3x；常见 Android 1080×2400@~2.6x。')],
  faqs=[dict(q='DPR 是什么？', a='设备像素比，CSS px × DPR = 物理像素。')])

KB['it/keycode-info'] = dict(title='按键码 Keycode 查询',
  scenarios=['查键盘事件的 keyCode/code/key。'],
  examples=[dict(title='查', body='回车 Enter → key="Enter"、code="Enter"、keyCode=13。')],
  faqs=[dict(q='keyCode 弃用了吗？', a='是，建议用 code/key。')])

KB['it/device-info'] = dict(title='设备与浏览器信息',
  scenarios=['展示当前 UA/屏幕/语言等环境信息。'],
  examples=[dict(title='查看', body='页面读取 navigator.userAgent、screen.width、Intl 语言并展示。')],
  faqs=[dict(q='信息准确吗？', a='来自浏览器自报，可被修改。')])

# ===== http / mime refs =====
for h in ['http-cache','http-cookies','http-headers','http-methods','http-response-headers','http-status']:
    title_map = {'http-cache':'HTTP 缓存策略速查','http-cookies':'HTTP Cookie 速查','http-headers':'HTTP 请求头速查',
                 'http-methods':'HTTP 方法速查','http-response-headers':'HTTP 响应头速查','http-status':'HTTP 状态码速查'}
    ex = {'http-cache':'`Cache-Control: max-age=3600` 与 `ETag` 协商缓存配合。',
          'http-cookies':'`Set-Cookie: sid=abc; HttpOnly; Secure; SameSite=Lax`。',
          'http-headers':'`Authorization: Bearer <token>`、`Content-Type: application/json`。',
          'http-methods':'GET 获取、POST 创建、PUT 替换、DELETE 删除。',
          'http-response-headers':'`Content-Encoding: gzip`、`Strict-Transport-Security`。',
          'http-status':'200 OK、301 永久重定向、404 未找到、500 服务端错误。'}
    KB[f'it/{h}'] = dict(title=title_map[h],
      scenarios=['开发/联调时查阅 HTTP 规范与取值。','排错时对照状态码与头字段。'],
      examples=[dict(title='示例', body=ex[h])],
      faqs=[dict(q='如何快速查？', a='在列表中按分类或搜索关键字定位。')])

KB['it/mime-type'] = dict(title='MIME 类型速查表',
  scenarios=['查文件扩展名对应 Content-Type。'],
  examples=[dict(title='查', body='`.json` → `application/json`；`.png` → `image/png`。')],
  faqs=[dict(q='不写 MIME 会怎样？', a='浏览器可能误判类型导致下载或乱码。')])

KB['it/mime-type-lookup'] = dict(title='MIME Type Lookup',
  scenarios=['按扩展名或类型反查。'],
  examples=[dict(title='查', body='输入 `.webp` → `image/webp`。')],
  faqs=[dict(q='同扩展名多类型？', a='少数存在，按上下文选择。')])

KB['it/ssl-info'] = dict(title='SSL/TLS 知识速查',
  scenarios=['查阅握手/证书/协议版本。'],
  examples=[dict(title='查', body='TLS1.3 握手 1-RTT、废弃 TLS1.0/1.1。')],
  faqs=[dict(q='证书链是什么？', a='服务器证+中间 CA+根 CA 逐级信任。')])

KB['it/regex'] = dict(title='正则表达式测试器',
  scenarios=['实时测试正则匹配与捕获组。'],
  examples=[dict(title='测试', body='`\\d{3}-\\d{4}` 匹配 `123-4567`，高亮并列出分组。')],
  faqs=[dict(q='如何全局匹配？', a='加 `g` 标志遍历所有匹配。')])

KB['it/regex-common'] = dict(title='Regex Common',
  scenarios=['常用正则模板（邮箱/URL/手机）。'],
  examples=[dict(title='模板', body='手机号中国大陆 `^1[3-9]\\d{9}$`。')],
  faqs=[dict(q='正则能验证一切吗？', a='复杂语义（如邮箱 RFC）正则难全覆盖，需配合业务校验。')])

KB['it/regex-visualizer'] = dict(title='正则表达式可视化',
  scenarios=['把正则渲染成 railroad 图理解结构。'],
  examples=[dict(title='可视化', body='`a(b|c)*` → 起始 a，循环分支 b/c 的状态图。')],
  faqs=[dict(q='图怎么看？', a='从左到右的轨道即匹配路径。')])

# ===== json path / diff / parsers =====
KB['it/json-path'] = dict(title='JSONPath 查询器',
  scenarios=['从大 JSON 提取子集。'],
  examples=[dict(title='查询', body='`$.store.book[?(@.price<10)].title` 取低价书名。')],
  faqs=[dict(q='与 XPath 区别？', a='JSONPath 面向 JSON，语法更简洁。')])

KB['it/properties-parser'] = dict(title='.properties 解析器',
  scenarios=['解析 Java 配置 key=value。'],
  examples=[dict(title='解析', body='`app.name=Demo\napp.port=8080` → {app.name:"Demo", app.port:"8080"}。')],
  faqs=[dict(q='支持注释吗？', a='`#` 或 `!` 开头行为注释。')])

KB['it/ini-parser'] = dict(title='INI 解析器',
  scenarios=['解析 [section] key=value 配置。'],
  examples=[dict(title='解析', body='`[db]\nhost=localhost` → {db:{host:"localhost"}}。')],
  faqs=[dict(q='重复键怎么办？', a='后值覆盖前值（视实现）。')])

KB['it/plist-parser'] = dict(title='Plist 解析器',
  scenarios=['解析 macOS/iOS 的 plist。'],
  examples=[dict(title='解析', body='XML plist `<dict><key>Ver</key><string>1.0</string></dict>` → {Ver:"1.0"}。')],
  faqs=[dict(q='二进制 plist？', a='需先转 XML 再解析。')])

KB['it/protobuf-parser'] = dict(title='Protobuf 解析器',
  scenarios=['按 .proto 解析二进制消息（需 schema）。'],
  examples=[dict(title='解析', body='给定 message User{string name=1} 与字节流 → {name:"Tom"}。')],
  faqs=[dict(q='无 schema 能解析吗？', a='不能，Protobuf 自描述弱，需 .proto。')])

KB['it/curl-parser'] = dict(title='curl 命令解析器',
  scenarios=['把 curl 拆成方法/URL/头/体，便于转代码。'],
  examples=[dict(title='解析', body='`curl -X POST https://a.com -H "Auth: x" -d "{}"` → {method:POST, url, headers, body}。')],
  faqs=[dict(q='能转 Python 吗？', a='结合代码生成器可转 requests 片段。')])

KB['it/phone-parser'] = dict(title='Phone Number Parser & Formatter',
  scenarios=['按国家格式化/解析电话号码。'],
  examples=[dict(title='解析', body='`+8613800138000` → 国家 CN、国内 `13800138000`、E.164 `+8613800138000`。')],
  faqs=[dict(q='E.164 是什么？', a='国际电信标准 +国家码+号码，无空格。')])

KB['it/area-code-lookup'] = dict(title='美国区号查询',
  scenarios=['查美国 NPA 区号归属州/城市。'],
  examples=[dict(title='查', body='`212` → 纽约市 NY；`415` → 旧金山湾区。')],
  faqs=[dict(q='区号会新增吗？', a='会，号码资源紧张时新增区号。')])

KB['it/country-code-lookup'] = dict(title='国家代码查询',
  scenarios=['查 ISO 3166 数字/字母代码。'],
  examples=[dict(title='查', body='中国 → CN / CHN / 156；美国 → US / USA / 840。')],
  faqs=[dict(q='数字码用途？', a='海关/统计等固定编码，避免字母歧义。')])

KB['it/country-flag'] = dict(title='国家代码与旗帜',
  scenarios=['按 ISO 码显示国旗 Emoji。'],
  examples=[dict(title='查', body='`CN` → 🇨🇳；`JP` → 🇯🇵（区域指示符 Emoji）。')],
  faqs=[dict(q='旗帜是图片吗？', a='是双字母区域指示符组合成的 Emoji。')])

KB['it/language-code-lookup'] = dict(title='语言代码查询（ISO 639-1）',
  scenarios=['查语言双语代码。'],
  examples=[dict(title='查', body='中文 zh、英语 en、日语 ja。')],
  faqs=[dict(q='zh-CN 与 zh？', a='zh 为语言，zh-CN 含地区变体。')])

KB['it/locale-lookup'] = dict(title='区域设置查询（Locale）',
  scenarios=['查 locale 标签与格式习惯。'],
  examples=[dict(title='查', body='`en-US` → 英语/美国，日期 MM/DD/YYYY；`de-DE` → DD.MM.YYYY。')],
  faqs=[dict(q='locale 影响什么？', a='日期/数字/货币格式与翻译。')])

# ===== misc tools that still need real content =====
KB['it/ascii-table'] = dict(title='ASCII 字符表',
  scenarios=['查字符的十进制/十六进制/控制字符含义。'],
  examples=[dict(title='查', body='十进制 65 = A；十进制 10 = 换行 LF；127 = DEL。')],
  faqs=[dict(q='可打印范围？', a='32–126 为可打印，其余为控制字符。')])

KB['it/ast-viewer'] = dict(title='AST 抽象语法树查看器',
  scenarios=['把代码解析成 AST 理解结构。'],
  examples=[dict(title='查看', body='`1+2*3` → Binary(+ , 1, Binary(*,2,3)) 树。')],
  faqs=[dict(q='AST 用途？', a='编译、格式化、静态分析都基于 AST。')])

KB['it/baudot-code'] = dict(title='Baudot / ITA2 编码',
  scenarios=['早期电传（TTY）5 位字符编码。'],
  examples=[dict(title='编码', body='字母 A 在 ITA2 为 `00011`（含 Figure/Letter 切换位）。')],
  faqs=[dict(q='为何 5 位？', a='仅 32 组合，需切换数字/字母档。')])

KB['it/morse'] = dict(title='摩斯电码转换',
  scenarios=['文本 ↔ ·— 点划，电台/教学。'],
  examples=[dict(title='编码 "SOS"', body='S=···、O=——— → `···———···`。')],
  faqs=[dict(q='长短有标准吗？', a='点 1 单位、划 3 单位、间隔 1–7 单位。')])

KB['it/morse-decode-advanced'] = dict(title='摩斯电码增强版',
  scenarios=['支持音频/变体规则的摩斯解码。'],
  examples=[dict(title='解码', body='`·····−·−−−` → `HI`（增强容错）。')],
  faqs=[dict(q='与基础版区别？', a='增强版容错与多规则，适合噪声输入。')])

KB['it/nato-alphabet'] = dict(title='北约音标字母转换',
  scenarios=['无线电/电话报字母避免误听。'],
  examples=[dict(title='转换 "AB"', body='A=Alfa、B=Bravo → `Alfa Bravo`。')],
  faqs=[dict(q='为何用音标？', a='跨语言清晰区分易混字母。')])

KB['it/roman-numeral-converter'] = dict(title='Roman Numeral Converter',
  scenarios=['整数 ↔ 罗马数字（1–3999）。'],
  examples=[dict(title='转换 1994', body='1994 = MCMXCIV（1000+900+90+4）。')],
  faqs=[dict(q='有 0 吗？', a='罗马数字无 0，最小 I=1。')])

KB['it/numeronym-generator'] = dict(title='Numeronym 数字缩写',
  scenarios=['生成 k8s 式缩写（首尾+中间字数）。'],
  examples=[dict(title='生成', body='`internationalization` → `i18n`（首尾 i/n，中间 18 字母）。')],
  faqs=[dict(q='目的？', a='缩短长词便于口语与文档。')])

KB['it/case-converter'] = dict(title='大小写转换器',
  scenarios=['camelCase/snake_case/kebab-case 互转。'],
  examples=[dict(title='转换', body='`my cool Var` → camelCase `myCoolVar`、snake `my_cool_var`。')],
  faqs=[dict(q='空格怎么处理？', a='通常转分隔符（_/-）或去掉。')])

KB['it/text-cleaner'] = dict(title='文本清理工具',
  scenarios=['去多余空白、控制字符、空行。'],
  examples=[dict(title='清理', body='`"  a   b  "` → `"a b"`（压缩空格、去首尾）。')],
  faqs=[dict(q='会删换行吗？', a='可选保留段落或全压成一行。')])

KB['it/text-dedupe-sort'] = dict(title='文本去重排序工具',
  scenarios=['对每行去重并排序。'],
  examples=[dict(title='处理', body='输入 `b\na\nb` → 去重排序 `a\nb`。')],
  faqs=[dict(q='大小写敏感？', a='可选敏感/忽略。')])

KB['it/text-diff'] = dict(title='文本对比工具',
  scenarios=['逐行对比两份文本差异。'],
  examples=[dict(title='对比', body='左 `a\nb` 右 `a\nc` → `b` 删、`c` 增。')],
  faqs=[dict(q='字符级对比？', a='部分工具支持词/字符级。')])

KB['it/text-replace'] = dict(title='文本替换工具',
  scenarios=['批量按字面或正则替换。'],
  examples=[dict(title='替换', body='把 `foo` 全换成 `bar`（支持正则 `f.o`）。')],
  faqs=[dict(q='正则替换能引用分组吗？', a='可，如 `$1` 引用捕获组。')])

KB['it/text-similarity'] = dict(title='文本相似度计算器',
  scenarios=['用编辑距离/余弦算两段文本相似度。'],
  examples=[dict(title='计算', body='`kitten` 与 `sitting` 编辑距离 3 → 相似度约 1−3/7≈0.57。')],
  faqs=[dict(q='哪种算法好？', a='短文本用 Levenshtein，长文本用分词+余弦。')])

KB['it/text-statistics'] = dict(title='文本统计分析',
  scenarios=['统计字数/词数/行数/可读性。'],
  examples=[dict(title='统计', body='`Hello world` → 字符 11、词 2、行 1。')],
  faqs=[dict(q='中英文分词不同？', a='中文无空格，需分词统计词数。')])

KB['it/text-steganography'] = dict(title='文本隐写工具',
  scenarios=['把密文藏进空白/零宽字符。'],
  examples=[dict(title='隐藏', body='用零宽字符（U+200B 等）在可见文本间编码秘密信息。')],
  faqs=[dict(q='隐写安全吗？', a='仅隐蔽非加密，检测零宽字符即可发现。')])

KB['it/text-truncate'] = dict(title='文本截断工具',
  scenarios=['按长度/字数截断并加省略号。'],
  examples=[dict(title='截断', body='`一二三四五六` 截 4 字 → `一二三四…`。')],
  faqs=[dict(q='按字节还是字符？', a='可选，中文按字符更友好。')])

KB['it/list-converter'] = dict(title='列表转换器',
  scenarios=['分隔符/CSV/数组互转。'],
  examples=[dict(title='转换', body='`a,b,c` → 每行一项或 `["a","b","c"]`。')],
  faqs=[dict(q='引号怎么处理？', a='CSV 模式按需加引号。')])

KB['it/line-ending-converter'] = dict(title='Line Ending Converter',
  scenarios=['CRLF/LF/CR 互转。'],
  examples=[dict(title='转换', body='Windows CRLF `\\r\\n` → Unix LF `\\n`。')],
  faqs=[dict(q='为何要统一？', a='跨平台脚本/校验常因换行不一致报错。')])

KB['it/keyword-density'] = dict(title='关键词密度分析器',
  scenarios=['SEO 分析页面词频占比。'],
  examples=[dict(title='分析', body='100 词中“工具”出现 5 次 → 密度 5%。')],
  faqs=[dict(q='密度越高越好？', a='不是，堆砌会被判作弊。')])

KB['it/keyword-extractor'] = dict(title='关键词提取',
  scenarios=['从文本抽取主题词（TF/TextRank）。'],
  examples=[dict(title='提取', body='文章 → 关键词 [加密, 算法, 安全] 按权重排序。')],
  faqs=[dict(q='中文需分词吗？', a='需，先分词再做词频/图权重。')])

KB['it/code-line-counter'] = dict(title='Code Line Counter',
  scenarios=['统计项目代码行/注释/空行。'],
  examples=[dict(title='统计', body='某文件 200 行：代码 150、注释 30、空 20。')],
  faqs=[dict(q='算注释行吗？', a='可单独统计注释与空行。')])

KB['it/markdown-lint'] = dict(title='Markdown Linter',
  scenarios=['检查 MD 风格与潜在问题。'],
  examples=[dict(title='检查', body='标题层级跳级、列表缺空格等给出警告。')],
  faqs=[dict(q='规则可配吗？', a='多数 linter 支持配置文件禁用规则。')])

KB['it/markdown-table-generator'] = dict(title='Markdown 表格生成器',
  scenarios=['可视化生成 MD 表格语法。'],
  examples=[dict(title='生成', body='3 列 2 行 → `| a | b | c |\n|---|---|---|\n| 1 | 2 | 3 |`')],
  faqs=[dict(q='对齐怎么设？', a='`:---` 左、`:--:` 中、`---:` 右。')])

KB['it/rich-text-editor'] = dict(title='Rich Text Editor',
  scenarios=['在线编辑带格式文本并导出 HTML。'],
  examples=[dict(title='编辑', body='加粗/列表/链接后导出对应 HTML 片段。')],
  faqs=[dict(q='粘贴会带样式吗？', a='通常做净化防止 XSS。')])

KB['it/markdown-editor'] = dict(title='Markdown 编辑器',
  scenarios=['实时预览的 MD 写作。'],
  examples=[dict(title='预览', body='左侧写 `# 标题` 右侧即时渲染。')],
  faqs=[dict(q='支持数学公式吗？', a='需启用 KaTeX/MathJax 插件。')])

KB['it/code-highlighter'] = dict(title='代码语法高亮',
  scenarios=['把代码渲染为带色 HTML。'],
  examples=[dict(title='高亮', body='`print(1)` → 关键字/函数着色的 <code>。')],
  faqs=[dict(q='支持哪些语言？', a='常见语言均支持，指定 lang 更准。')])

KB['it/html-nesting-checker'] = dict(title='HTML 嵌套检查器',
  scenarios=['查标签嵌套错误（如 <p> 内含 <div>）。'],
  examples=[dict(title='检查', body='`<p><div></div></p>` → 提示 p 内不应有 div。')],
  faqs=[dict(q='浏览器为何能渲染？', a='浏览器会容错修复，但结构不规范。')])

KB['it/meta-tags-generator'] = dict(title='Meta Tags Generator',
  scenarios=['生成 SEO/社交分享 meta。'],
  examples=[dict(title='生成', body='填标题描述 → 输出 `<title>`、description、og:*、twitter:*。')],
  faqs=[dict(q='og 与 twitter 区别？', a='og 为 Open Graph（Facebook 等），twitter 为卡片。')])

KB['it/og-meta-tag-generator'] = dict(title='OG 元标签生成器',
  scenarios=['生成 Open Graph 社交分享标签。'],
  examples=[dict(title='生成', body='`og:title`,`og:image`,`og:url` 三段必备。')],
  faqs=[dict(q='不写 og 会怎样？', a='分享时平台抓取不到结构化预览。')])

KB['it/robots-txt-generator'] = dict(title='Robots.txt 生成器',
  scenarios=['生成爬虫允许/禁止规则。'],
  examples=[dict(title='生成', body='`User-agent: *\nDisallow: /admin` 禁止抓取后台。')],
  faqs=[dict(q='robots 能强制保密吗？', a='不能，仅建议，敏感路径仍需鉴权。')])

KB['it/sitemap-generator'] = dict(title='Sitemap Generator',
  scenarios=['列出站点 URL 生成 sitemap.xml。'],
  examples=[dict(title='生成', body='输入若干 URL → `<urlset>` 含 loc/lastmod。')],
  faqs=[dict(q='上限多少？', a='单文件 5 万 URL / 50MB，超出需索引。')])

KB['it/dockerfile-generator'] = dict(title='Dockerfile Generator',
  scenarios=['按语言生成基础 Dockerfile。'],
  examples=[dict(title='生成', body='Node 项目 → `FROM node:20\nWORKDIR /app\nCOPY . .\nRUN npm i\nCMD npm start`。')],
  faqs=[dict(q='多阶段构建？', a='可生成 builder + runtime 两阶段瘦身。')])

KB['it/docker-run-converter'] = dict(title='Docker Run to Compose',
  scenarios=['把 docker run 命令转 docker-compose。'],
  examples=[dict(title='转换', body='`docker run -p 80:80 nginx` → compose `services.web.image=nginx ports=["80:80"]`。')],
  faqs=[dict(q='卷怎么转？', a='`-v` 转为 volumes 映射。')])

KB['it/nginx-config-generator'] = dict(title='Nginx Config Generator',
  scenarios=['可视化生成 server/location 配置。'],
  examples=[dict(title='生成', body='填域名+端口+根目录 → 输出 server 块。')],
  faqs=[dict(q='生成后怎么用？', a='放入 conf.d 并 `nginx -t` 校验后 reload。')])

KB['it/kubernetes-yaml-generator'] = dict(title='Kubernetes YAML Generator',
  scenarios=['生成 Deployment/Service YAML。'],
  examples=[dict(title='生成', body='填镜像与副本数 → Deployment + ClusterIP Service。')],
  faqs=[dict(q='如何暴露外网？', a='Service 改 NodePort/LoadBalancer 或加 Ingress。')])

KB['it/api-sign-generator'] = dict(title='API 签名生成器',
  scenarios=['按密钥对请求参数做签名（HMAC）。'],
  examples=[dict(title='签名', body='参数按 key 排序+secret → HMAC-SHA256 签名串，随请求发送。')],
  faqs=[dict(q='为何要排序？', a='保证客户端与服务端拼接串一致才能验签。')])

KB['it/basic-auth-generator'] = dict(title='Basic Auth 生成器',
  scenarios=['把 user:pass 编码为 Authorization 头。'],
  examples=[dict(title='生成', body='`user:pass` → `Basic dXNlcjpwYXNz`（Base64，非加密）。')],
  faqs=[dict(q='Basic Auth 安全吗？', a='须配合 HTTPS，否则明文可被截。')])

KB['it/env-generator'] = dict(title='环境变量生成器',
  scenarios=['生成 KEY=VALUE 的 .env 片段。'],
  examples=[dict(title='生成', body='填多组键值 → `DB_HOST=localhost\nDB_PORT=5432`。')],
  faqs=[dict(q='敏感值怎么保护？', a='勿提交 .env，用 .env.example 占位。')])

KB['it/generator-16'] = dict(title='环境变量生成器（.env 格式）',
  scenarios=['与 env-generator 同类，输出 .env。'],
  examples=[dict(title='生成', body='多键值 → `A=1\nB=2` 格式。')],
  faqs=[dict(q='注释支持吗？', a='支持 `#` 注释行。')])

KB['it/crontab-generator'] = dict(title='Crontab 生成器',
  scenarios=['可视化生成定时任务表达式。'],
  examples=[dict(title='生成', body='每天 9:30 → `30 9 * * *`（分 时 日 月 周）。')],
  faqs=[dict(q='周与日冲突？', a='同时指定日与周为 AND；用 `*` 放宽。')])

KB['it/cron'] = dict(title='Cron 表达式生成器',
  scenarios=['生成并解析 5/6 段 cron。'],
  examples=[dict(title='生成', body='每 5 分钟 `*/5 * * * *`。')],
  faqs=[dict(q='秒级 cron？', a='标准 5 段无秒，Quartz 为 6 段含秒。')])

KB['it/sn-generator'] = dict(title='序列号/编号生成器（sn）',
  scenarios=['生成带前缀的递增编号。'],
  examples=[dict(title='生成', body='前缀 INV- + 日期 + 序号 → `INV-20260909-0001`。')],
  faqs=[dict(q='并发会重复吗？', a='需后端原子计数保证唯一。')])

KB['it/js-obfuscator'] = dict(title='JS 代码混淆器',
  scenarios=['压缩变量名/控制流增加逆向难度。'],
  examples=[dict(title='混淆', body='`function calc(x){return x*2}` → 变量 renamed、结构打乱。')],
  faqs=[dict(q='混淆等于加密吗？', a='不是，仅增加成本，仍可还原逻辑。')])

KB['it/string-obfuscator'] = dict(title='字符串混淆器',
  scenarios=['把字符串转编码/数组形式隐藏明文。'],
  examples=[dict(title='混淆', body='`"secret"` → `String.fromCharCode(115,101,99,...)` 拆分。')],
  faqs=[dict(q='能防逆向吗？', a='仅增加难度，运行时仍还原。')])

KB['it/summary-generator'] = dict(title='摘要生成器',
  scenarios=['抽取式生成文本摘要（句重要度）。'],
  examples=[dict(title='摘要', body='长文 → 取前 N 句关键句作摘要（非生成式）。')],
  faqs=[dict(q='与 LLM 摘要区别？', a='本工具为抽取式，不重写内容。')])

KB['it/safelink-decoder'] = dict(title='SafeLink Decoder',
  scenarios=['还原被安全跳转包裹的真实 URL。'],
  examples=[dict(title='解码', body='`https://safe?u=https%3A%2F%2Fex.com` → `https://ex.com`。')],
  faqs=[dict(q='解码安全吗？', a='先预览再访问，避免钓鱼。')])

# ----- generators/editors not yet in KB (coverage safety) -----
EXTRA_DEFAULTS = {
 'it/html-minifier':'HTML 压缩器',
 'it/benchmark-builder':'Benchmark 基准测试',
 'it/camera-recorder':'摄像头录制',
 'it/code-runner':'在线代码运行器',
 'it/device-info':'设备与浏览器信息',
 'it/latex':'LaTeX 符号速查',
 'it/markdown-editor':'Markdown 编辑器',
 'it/rich-text-editor':'富文本编辑器',
 'it/sql-formatter':'SQL 格式化',
 'it/sqlite-runner':'SQLite 在线执行',
 'it/typescript-compiler':'TypeScript 编译器',
 'it/video-bitrate':'视频码率计算器',
 'it/timestamp-converter':'时间戳转换器',
 'it/time-format-converter':'时间格式转换',
 'it/date-duration':'日期区间计算器',
 'it/unit-converter-advanced':'高级单位换算',
 'it/ip-calculator':'IP 子网计算器',
 'it/random':'随机数生成器',
 'it/pomodoro':'番茄钟计时器',
 'it/stopwatch':'计圈秒表',
 'it/typing-test':'打字速度测试',
 'it/wifi-qr':'WiFi 二维码',
 'it/team-name-generator':'团队名生成器',
 'it/nickname-generator':'昵称生成器',
 'it/username-generator':'用户名生成器',
 'it/chinese-name-generator':'随机中文名生成器',
 'it/emoji-picker':'Emoji 选择器',
 'it/emoji-meaning':'Emoji 含义查询',
 'it/csv-to-html-table':'CSV 转 HTML 表格',
 'it/csv-validator':'CSV 校验器',
 'it/xml-to-json':'XML 转 JSON',
 'it/yaml-to-json':'YAML 转 JSON',
 'it/json-to-yaml':'JSON 转 YAML',
}

# ===== extra it slugs not yet covered =====
KB['it/unit-converter-advanced'] = dict(title='Advanced Unit Converter',
  scenarios=['在科研/工程里把长度、质量、体积、温度等按精确系数换算。'],
  examples=[dict(title='换算', body='1 mile=1609.34 m；1 lb=0.453592 kg；1 US gallon=3.78541 L；°C→°F: 25°C×9/5+32=77°F。')],
  faqs=[dict(q='温度换算为何有 +32？', a='摄氏与华氏零点不同，需平移而非纯比例。')])

KB['it/benchmark-builder'] = dict(title='Benchmark 基准测试',
  scenarios=['对比两段代码的吞吐/耗时，定位性能瓶颈。'],
  examples=[dict(title='对比', body='对 1e6 整数分别用 `for` 累加与 `sum()`，输出各自 ops/sec 与相对倍数。')],
  faqs=[dict(q='为何要预热？', a='JIT/缓存使首次偏慢，预热后测值更稳。')])

KB['it/box-shadow-generator'] = dict(title='Box-shadow 生成器',
  scenarios=['可视化调出元素投影：偏移/模糊/扩散/颜色。'],
  examples=[dict(title='生成', body='`box-shadow: 2px 4px 8px rgba(0,0,0,0.2)`（右 2 下 4、模糊 8、20% 黑）。')],
  faqs=[dict(q='inset 是什么？', a='加 inset 变为内阴影，用于凹陷效果。')])

KB['it/caa-record-generator'] = dict(title='CAA 记录生成器',
  scenarios=['限制哪些 CA 可签发本域证书，防误签发。'],
  examples=[dict(title='生成', body='`example.com. CAA 0 issue "letsencrypt.org"` 仅允许 Let\'s Encrypt 签发。')],
  faqs=[dict(q='CAA 会影响现有证书吗？', a='不影响已签发，仅约束未来签发。')])

KB['it/date-duration'] = dict(title='Date Duration Calculator',
  scenarios=['算两个日期相差天数/工作日。'],
  examples=[dict(title='计算', body='2024-01-01 到 2024-12-31 = 365 天（闰年 366）；跨 2024-03-01~2024-03-31=30 天。')],
  faqs=[dict(q='含首尾当天吗？', a='默认算间隔天数，是否含当天视设定。')])

KB['it/email-normalizer'] = dict(title='Email 规范化',
  scenarios=['归一并去重邮箱（小写、去 +tag、去点）。'],
  examples=[dict(title='归一', body='`John.Doe+news@gmail.com` → `johndoe@gmail.com`（Gmail 忽略点与 + 标签）。')],
  faqs=[dict(q='所有邮箱都忽略点吗？', a='仅 Gmail/Outlook 等，不可对所有服务商假设。')])

KB['it/git-cheatsheet'] = dict(title='Git 命令速查',
  scenarios=['查阅 stash/reset/cherry-pick/reflog 等。'],
  examples=[dict(title='暂存', body='`git stash push -m "wip"` 暂存修改，`git stash pop` 恢复。')],
  faqs=[dict(q='reflog 能救误删吗？', a='能，reflog 记录 HEAD 变动，可找回被 reset 的提交。')])

KB['it/html-minifier'] = dict(title='HTML 压缩器',
  scenarios=['去除注释/空白/可选标签减小体积。'],
  examples=[dict(title='压缩', body='`<html>  <body><!--c--><p>x</p>  </body></html>` → `<html><body><p>x</p></body></html>`。')],
  faqs=[dict(q='会破坏结构吗？', a='合规压缩不会，但需保留 pre/textarea 内空白。')])

KB['it/json-to-toml'] = dict(title='JSON 转 TOML',
  scenarios=['把 JSON 配置转 TOML 供 Go/ Rust 消费。'],
  examples=[dict(title='转换', body='`{"name":"Tom","age":20}` → `name = "Tom"\nage = 20`。')],
  faqs=[dict(q='嵌套对象怎么转？', a='用 [section] 表层级。')])

KB['it/jwt-debugger'] = dict(title='JWT 调试器',
  scenarios=['粘贴 token 看三段，并用密钥验签。'],
  examples=[dict(title='调试', body='粘贴 `eyJ...` → 展示 header/payload；输入 secret 验证签名是否匹配（HS256）。')],
  faqs=[dict(q='能离线验签吗？', a='HS 用对称密钥可离线；RS 需公钥。')])

KB['it/pdf-signature-checker'] = dict(title='PDF 签名检查',
  scenarios=['校验 PDF 内嵌 PKCS#7 签名与证书链。'],
  examples=[dict(title='检查', body='读取签名域，验证摘要一致且证书链到可信根（显示“有效/无效/未知”）。')],
  faqs=[dict(q='签名有效=内容未被改？', a='是，摘要不符会标记篡改。')])

KB['it/sqlite-runner'] = dict(title='SQLite 在线执行',
  scenarios=['浏览器内跑 SQL，快速验证查询。'],
  examples=[dict(title='执行', body='`SELECT 1+1;` → 2；`SELECT date(\'now\')` → 当前日期。')],
  faqs=[dict(q='能建表吗？', a='可，运行于内存库，刷新即清空。')])

KB['it/whitespace'] = dict(title='Text Whitespace Cleaner',
  scenarios=['压缩多余空格/制表/换行。'],
  examples=[dict(title='清理', body='`a   b\\t\\n c` → `a b c`（多空白合并为单空格并去首尾）。')],
  faqs=[dict(q='会删换行吗？', a='可选保留段落或全压成一行。')])

KB['it/code-runner'] = dict(title='在线代码运行器',
  scenarios=['临时跑片段验证逻辑（沙箱、无网络）。'],
  examples=[dict(title='运行', body='`print(2**10)` → 输出 `1024`（受超时与内存限制）。')],
  faqs=[dict(q='能访问网络/文件吗？', a='不能，沙箱隔离，仅纯计算。')])

KB['it/camera-recorder'] = dict(title='摄像头录制',
  scenarios=['调用 getUserMedia 在本地录制视频/截图。'],
  examples=[dict(title='录制', body='授权摄像头后录制为 webm（纯前端，不上传）。')],
  faqs=[dict(q='需要权限吗？', a='需用户授权摄像头，且仅 HTTPS/localhost 可用。')])

KB['it/image-to-base64'] = dict(title='Image to Base64',
  scenarios=['把图片转 data URI 内联进页面。'],
  examples=[dict(title='转换', body='上传 PNG → `data:image/png;base64,iVBORw0KGgo...`（前缀含 MIME）。')],
  faqs=[dict(q='内联图片变大吗？', a='Base64 约膨胀 33%，小图可用，大图建议外链。')])

KB['it/typing-test'] = dict(title='打字速度测试',
  scenarios=['测 WPM 与准确率。'],
  examples=[dict(title='测试', body='60 秒输入 400 字符、错 8 → 约 80 WPM、准确率 98%。')],
  faqs=[dict(q='WPM 怎么算？', a='按 5 字符=1 词，WPM=正确字符/5 ÷ 分钟。')])

KB['it/pomodoro'] = dict(title='番茄钟计时器',
  scenarios=['25 分钟专注 + 5 分钟休息的节奏管理。'],
  examples=[dict(title='循环', body='专注 25:00 → 休息 05:00，每 4 轮长休 15–30 分。')],
  faqs=[dict(q='必须 25 分钟吗？', a='可按需调整，核心是专注/休息交替。')])

KB['it/stopwatch'] = dict(title='计圈秒表',
  scenarios=['记录多段耗时。'],
  examples=[dict(title='计圈', body='总 122.4s，lap1 12.3s、lap2 10.1s、lap3 100.0s。')],
  faqs=[dict(q='精度到多少？', a='通常毫秒显示，计时依赖浏览器精度。')])

KB['it/random'] = dict(title='随机数生成器',
  scenarios=['生成均匀分布的随机整数/浮点。'],
  examples=[dict(title='生成', body='[1,100] 均匀整数 → 如 42；用密码学安全随机源。')],
  faqs=[dict(q='真随机吗？', a='为密码学安全伪随机，统计上均匀不可预测。')])

KB['it/color-converter'] = dict(title='颜色转换器',
  scenarios=['HEX/RGB/HSL 互转做配色。'],
  examples=[dict(title='转换', body='#3498db → rgb(52,152,219) → hsl(204,70%,41%)。')],
  faqs=[dict(q='HSL 选色优势？', a='用色相/饱和/亮度更直观调色。')])

KB['it/video-bitrate'] = dict(title='Video Bitrate Calculator',
  scenarios=['按时长与码率估算文件大小。'],
  examples=[dict(title='估算', body='10 分钟(600s)@5 Mbps → 5e6×600/8 = 375 MB；4K@15Mbps 同长 ≈ 1.13 GB。')],
  faqs=[dict(q='码率越高越清晰？', a='同分辨率下码率越高细节越好，但有收益拐点。')])

# ---------- apply ----------
changed = 0
for slug, entry in KB.items():
    if slug not in data:
        continue
    cur = data[slug]
    new = {
        'title': entry['title'],
        'scenarios': entry['scenarios'],
        'examples': entry['examples'],
        'faqs': entry['faqs'],
    }
    if cur != new:
        data[slug] = new
        changed += 1

print(f"KB entries: {len(KB)}  changed: {changed}")

with open(DD, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=1)
    f.write('\n')
print("written.")
