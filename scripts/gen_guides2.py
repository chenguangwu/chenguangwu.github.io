# -*- coding: utf-8 -*-
"""it-tools 新增工具指南扩充：10 篇使用指南 + 合并 guides.json + 指南中心追加条目。
运行：python3 scripts/gen_guides2.py
"""
import os, json, html, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GUIDES_DIR = os.path.join(ROOT, 'guides')
SITE = 'https://chenguangwu.github.io'

GUIDES = [
 {'slug':'math-evaluator','tool':'tools/it/math-evaluator.html','name':'数学表达式求值器',
  'desc':'数学表达式求值器使用指南：支持幂运算、百分比、三角函数等，实时计算结果。',
  'intro':'数学表达式求值器让你像用计算器一样直接输入表达式即可得出结果，支持 + - * / % ^ 等运算符与 sin/cos/sqrt/ln 等函数，还会自动保存最近 20 条计算历史，方便复用。',
  'features':['支持 + - * / % ^ ( ) 运算与优先级','内置 sin/cos/tan/sqrt/abs/ln/log/floor/ceil/round/min/max 函数','百分比速算：15% * 200 自动按 0.15×200 处理','白名单字符校验，拒绝脚本注入，安全可靠','自动保存最近 20 条历史，一键复用','结果超出常规范围自动切换科学计数法'],
  'scenarios':['学生/工程师做日常数值计算','数据分析前快速验证公式','把历史计算结果一键回填继续计算'],
  'steps':['在输入框输入表达式，如 2^10 + sqrt(144)','点击「计算」或按回车键','结果实时显示，历史记录自动保存','点击历史中的「复用」可把表达式填回输入框','使用上方按钮快速插入函数与 π'],
  'tips':['^ 表示幂运算（2^10 = 1024）','百分号按"除以 100"处理：15% = 0.15','sqrt 与 ln 需要括号：sqrt(144)、ln(e)','π 可通过按钮插入，也可直接输入 pi'],
  'faqs':[('为什么提示"表达式无效"？','可能含非法字符（如中文、@、#），或括号不匹配；本工具仅接受数字、运算符与白名单函数。'),('结果太长显示成科学计数法？','数值极大或极小时会自动使用科学计数法，如 1.5e+15。')]},
 {'slug':'json-minify','tool':'tools/it/json-minify.html','name':'JSON 压缩/格式化',
  'desc':'JSON 压缩与格式化使用指南：一键压缩减小体积、美化缩进阅读，显示压缩率。',
  'intro':'JSON 工具支持「压缩」与「美化」两种模式：压缩用于减小存储/传输体积并显示压缩率，美化用于阅读与调试。全程浏览器本地处理。',
  'features':['压缩模式：去除空白与换行，显示压缩率','美化模式：按层级缩进，便于阅读','显示原始/输出体积对比','解析错误定位提示，方便排查','一键复制结果'],
  'scenarios':['接口调试：把返回的压缩 JSON 美化阅读','存储优化：压缩配置/缓存数据减小体积','把 JSON 压缩后放进 URL 参数'],
  'steps':['粘贴 JSON 到输入框','选择「压缩」或「美化」模式（支持实时切换）','查看体积与压缩率统计','点击「复制结果」使用'],
  'tips':['压缩率可能为负（小 JSON 反而变大），属正常现象','美化后的 JSON 缩进为 2 空格','粘贴前确认内容为合法 JSON，否则会提示错误位置'],
  'faqs':[('压缩和美化哪个好？','传输/存储用压缩，阅读/调试用美化；两者不会改变数据本身。'),('为什么压缩后反而更大？','小 JSON 的空格占比高，压缩收益小甚至为负，属正常。')]},
 {'slug':'json-to-csv','tool':'tools/it/json-to-csv.html','name':'JSON 转 CSV',
  'desc':'JSON 转 CSV 使用指南：数组一键转表格，自动提取字段、处理嵌套对象，下载文件。',
  'intro':'把 JSON 数组一键转为 CSV 表格：自动汇总所有对象的字段作为表头，嵌套对象序列化为 JSON 字符串，支持复制与下载，适合数据迁移、Excel 处理。',
  'features':['自动提取所有字段为 CSV 表头','处理数组与嵌套对象（序列化）','NULL/缺失字段输出为空单元格','UTF-8 BOM 导出，Excel 打开不乱码','一键复制或下载 .csv 文件'],
  'scenarios':['把接口返回的数据导出为表格给运营/销售','数据迁移：JSON → Excel/表格','批量导入前的格式转换'],
  'steps':['粘贴 JSON 数组（如 [{...},{...}]）','点击「转换」，自动生成 CSV','查看行列统计：N 行 × M 列','点击「下载 .csv」保存为文件'],
  'tips':['输入必须是数组，对象会提示错误','CSV 中所有单元格用双引号包裹，含逗号也安全','Excel 打开乱码时请使用「下载」功能（自带 BOM）'],
  'faqs':[('嵌套对象怎么处理？','嵌套对象会序列化为 JSON 字符串存入单元格，如 {"a":1} 会显示为 {"a":1}。'),('为什么 Excel 打开中文乱码？','请用「下载 .csv」按钮导出（带 UTF-8 BOM），直接复制粘贴可能乱码。')]},
 {'slug':'token-generator','tool':'tools/it/token-generator.html','name':'随机 Token 生成器',
  'desc':'随机 Token 生成器使用指南：加密级随机数生成令牌，自定义长度/字符集/批量。',
  'intro':'基于浏览器加密级随机数 crypto.getRandomValues 生成高强度令牌，可自定义长度、字符集与数量，显示信息熵，适合 API Token、邀请码、密钥等场景。',
  'features':['crypto.getRandomValues 加密级随机源','自定义长度（4-256）与字符集（大小写/数字/符号）','批量生成最多 20 个','显示信息熵（bit），量化强度','逐个或全部一键复制'],
  'scenarios':['生成 API Token / 密钥','生成邀请码、激活码、优惠券码','生成测试用的随机凭据'],
  'steps':['设置长度（默认 32）与数量（默认 1）','勾选字符集：大小写、数字、符号','点击「生成」，查看熵值','点击「复制」使用'],
  'tips':['符号集能显著提升熵值，敏感场景建议勾选','生成结果请立即安全保存，本工具不存储任何令牌','浏览器关闭后令牌不会保留，重新打开需重新生成'],
  'faqs':[('Token 会被上传吗？','不会，随机数在浏览器本地生成，不上传任何服务器。'),('什么是信息熵？','衡量随机性强弱的指标，位数越高越难被暴力破解；128 bit 以上视为强令牌。')]},
 {'slug':'bcrypt','tool':'tools/it/bcrypt.html','name':'Bcrypt 哈希/校验',
  'desc':'Bcrypt 哈希生成与校验使用指南：成本因子可调，本地计算，密码存储安全实践。',
  'intro':'Bcrypt 是密码存储的主流哈希算法，内置盐值（salt），相同明文每次结果不同。工具支持生成哈希与校验原文，成本因子（rounds）可调，全程浏览器本地计算。',
  'features':['生成标准 Bcrypt 哈希（$2a$10$...，60 位）','内置盐值，相同明文每次生成不同结果','成本因子 8-14 可调，平衡安全与速度','原文 + 哈希一键校验','从哈希自动提取盐值，无需手工管理'],
  'scenarios':['后端开发调试用户密码哈希','学习/演示 Bcrypt 工作方式','验证数据库中的密码哈希是否匹配'],
  'steps':['输入明文密码','选择成本因子（推荐 10）','点击「生成哈希」获取 60 位哈希','粘贴哈希到校验框，输入原文点击「校验」'],
  'tips':['成本因子每增加 2，耗时约增 4 倍；10 约 150ms','Bcrypt 不是加密，无法解密，只能校验','生产环境把成本因子存到配置，方便升级'],
  'faqs':[('为什么两次生成结果不同？','Bcrypt 每次生成随机盐，盐值写入哈希前缀，所以结果不同但都可校验。'),('哈希泄露安全吗？','配合高强度密码相对安全，但仍建议加 PEPPER 或多因素认证。')]},
 {'slug':'crontab-generator','tool':'tools/it/crontab-generator.html','name':'Crontab 生成器',
  'desc':'Crontab 生成器使用指南：五段表达式可视化生成，附中文说明与常用预设。',
  'intro':'可视化生成 Linux crontab 定时任务表达式：选择分钟/小时/日期/月份/星期，实时得到五段 cron 语法并给出中文说明，附 6 个常用预设。',
  'features':['五字段（分/时/日/月/周）可视化填写','实时生成 cron 表达式与中文说明','支持 * 、*/n、a-b、a,b 语法','6 个常用预设一键填充','语法校验，错误字段即时提示','一键复制表达式'],
  'scenarios':['服务器定时任务配置','备份脚本、报表生成等周期性任务','学习 cron 表达式语法'],
  'steps':['填写五个字段（或用预设按钮）','查看生成的表达式与中文说明','点击「复制表达式」粘贴到 crontab','（可选）调整字段实现更精细的调度'],
  'tips':['cron 每周日取 0 或 7 均可','分钟字段不能为空，*/5 表示每 5 分钟','多个值用逗号：1,15,30；范围用短横线：9-17'],
  'faqs':[('cron 表达式有哪些部分？','依次为：分 时 日 月 周，共五段，例如 0 9 * * 1 表示每周一 9 点。'),('为什么我的任务没执行？','常见原因：分钟字段写了非法值、时区不一致、或服务器时间不对。')]},
 {'slug':'chmod-calculator','tool':'tools/it/chmod-calculator.html','name':'Chmod 权限计算器',
  'desc':'Chmod 权限计算器使用指南：勾选读/写/执行权限，实时换算数字与符号模式。',
  'intro':'可视化计算 Linux 文件权限：勾选属主/组/其他用户的读(4)写(2)执行(1)权限，实时得到数字模式（如 755）与符号模式（rwxr-xr-x），附常见权限速查。',
  'features':['三组（属主/组/其他）× 三权限复选','实时换算数字模式与符号模式','常见权限含义提示（755/644/777 等）','6 个常用权限一键填充','一键复制 chmod 命令'],
  'scenarios':['部署网站时设置目录/文件权限','排查"权限不足"报错','学习 Linux 权限模型'],
  'steps':['勾选各用户组的读/写/执行权限','查看上方数字模式与符号模式','参考权限含义提示判断是否安全','点击「复制 chmod 命令」使用'],
  'tips':['目录常用 755，普通文件常用 644','777 全开放有安全风险，谨慎使用','私钥、配置文件建议 600 或 400'],
  'faqs':[('755 是什么意思？','属主可读可写可执行(7)，组与其他可读可执行(5)，常用于网站目录。'),('为什么权限改完还是报错？','文件与目录权限要分别设置；目录需要 x 才能进入，仅 r 不够。')]},
 {'slug':'qr-beautify','tool':'tools/it/qr-beautify.html','name':'二维码美化生成器',
  'desc':'二维码美化生成器使用指南：自定义颜色与圆角样式生成个性化二维码，下载 PNG。',
  'intro':'在标准二维码基础上自定义前景色、背景色、容错级别与模块圆角样式，生成品牌化的彩色二维码，适合名片、海报与物料印刷，支持下载 PNG。',
  'features':['自定义前景色/背景色','四种容错级别（L/M/Q/H）','圆角/直角两种模块样式','实时预览，调整即所见','下载 PNG 图片或复制 Base64','纯 canvas 本地绘制，内容不上传'],
  'scenarios':['品牌海报与宣传物料','名片/工牌上的个性化二维码','活动签到、展台引导'],
  'steps':['输入二维码内容（网址/文本等）','选择前景色、背景色与容错级别','选择模块样式（圆角更柔和）','预览满意后「下载 PNG」'],
  'tips':['深色前景 + 浅色背景对比度最高，扫码最稳','内容越多容错级别越低，复杂内容建议 M 级','印刷前保留静区（四周留白），避免贴边'],
  'faqs':[('彩色二维码扫不出来？','多为前景/背景对比度不足所致，建议背景用浅色、前景用深色。'),('容错级别怎么选？','易污损场景选 Q/H 级；内容很长时降为 L/M 级保证密度合理。')]},
 {'slug':'integer-base-converter','tool':'tools/it/integer-base-converter.html','name':'任意进制转换器',
  'desc':'任意进制转换器使用指南：2-36 进制互转，BigInt 支持超大整数与进制一览。',
  'intro':'支持 2-36 进制任意互转，底层使用 BigInt，可处理远超 Number 精度上限的超大整数；输入数字与源进制，实时得到目标进制结果及常用进制一览。',
  'features':['2-36 进制任意互转','BigInt 支持超大整数（任意位数）','自动生成二进制/八进制/十进制/十六进制/32/36 一览','进制内非法字符检测与定位','一键复制结果'],
  'scenarios':['颜色值、MAC 地址的进制换算','数据编码与压缩调试','密码学/哈希场景的大数进制转换'],
  'steps':['输入数字（如 ff、1010、255）','设置源进制与目标进制（2-36）','实时查看结果与多进制一览','点击「复制结果」'],
  'tips':['十六进制字母不区分大小写（ff 与 FF 均可）','进制必须为 2-36 之间','输入含源进制不支持的字符会提示错误位置'],
  'faqs':[('能转换多大的数？','基于 BigInt 实现，理论上不限位数，可处理百位十进制大数。'),('为什么 10 进制显示为字符串？','大数超出 Number 精度后会丢精度，工具统一用字符串保真处理。')]},
 {'slug':'hash-multi','tool':'tools/it/hash-multi.html','name':'多算法哈希器',
  'desc':'多算法哈希器使用指南：MD5/SHA-1/SHA-256/SHA-512/CRC32 同屏计算对比。',
  'intro':'一键计算多种哈希：MD5、SHA-1、SHA-256、SHA-512 与 CRC32，支持多算法同时输出与大小写切换。SHA 系列走浏览器原生 crypto.subtle，全程本地。',
  'features':['5 种算法同屏输出（MD5/SHA-1/256/512/CRC32）','多算法勾选，一键全出','SHA 系列使用原生 crypto.subtle','大写/小写切换','逐项或全部一键复制'],
  'scenarios':['下载文件完整性校验（SHA-256）','接口签名调试（MD5/SHA）','数据去重与一致性对比（CRC32）'],
  'steps':['输入文本','勾选需要的算法','点击「计算」查看全部结果','点击「复制全部」批量使用'],
  'tips':['文件校验优先 SHA-256（SHA-1 与 MD5 已不建议用于安全场景）','CRC32 用于快速一致性校验，不适合安全场景','CRC32 输出为 8 位十六进制'],
  'faqs':[('MD5 和 SHA-256 有什么区别？','MD5 128 位、SHA-256 256 位；两者均常用，但安全场景建议 SHA-256 及以上。'),('哈希可以逆推原文吗？','不能，哈希是单向函数；本站同时提供彩虹表式查找？不——本站仅做正向计算，无法反查。')]},
]

TPL = '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}使用指南 - ToolBox</title>
<meta name="description" content="{desc}">
<meta property="og:title" content="{title}使用指南 - ToolBox">
<meta property="og:type" content="article">
<meta property="og:site_name" content="ToolBox">
<meta property="og:url" content="{canonical}">
<meta property="og:description" content="{desc}">
<meta property="og:image" content="https://chenguangwu.github.io/og-image.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="ToolBox - 免费在线工具与使用指南">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title}使用指南 - ToolBox">
<meta name="twitter:description" content="{desc}">
<meta name="twitter:image" content="https://chenguangwu.github.io/og-image.png">
<meta name="twitter:image:alt" content="ToolBox - 免费在线工具与使用指南">
<link rel="canonical" href="{canonical}">
<script type="application/ld+json">
{{"@context":"https://schema.org","@type":"Article","headline":"{title}使用指南","description":"{desc}","author":{{"@type":"Organization","name":"ToolBox"}}}}
</script>
<style>
:root{{--primary:#FF6B35;--text:#1F2937;--muted:#6B7280;--border:#E5E7EB;--bg:#FFFAF7;}}
*{{box-sizing:border-box;}}
body{{margin:0;font-family:"Noto Sans SC","Plus Jakarta Sans",system-ui,sans-serif;color:var(--text);background:var(--bg);line-height:1.75;}}
header{{padding:18px 20px;border-bottom:1px solid var(--border);background:#fff;}}
.breadcrumb a{{color:var(--primary);text-decoration:none;margin-right:6px;}}
main{{max-width:780px;margin:0 auto;padding:28px 20px 60px;}}
h1{{font-size:28px;margin:0 0 8px;}}
.lead{{font-size:16px;color:var(--muted);margin:0 0 22px;}}
h2{{font-size:20px;margin:28px 0 10px;color:var(--primary);}}
ul,ol{{padding-left:22px;}}
li{{margin:6px 0;}}
dl{{margin:0;}}
dt{{font-weight:700;margin-top:12px;}}
dd{{margin:4px 0 0;color:var(--muted);}}
.back{{margin-top:30px;padding:16px;background:#fff;border:1px solid var(--border);border-radius:14px;}}
.back a{{color:var(--primary);font-weight:700;text-decoration:none;}}
footer{{text-align:center;color:var(--muted);font-size:13px;padding:24px;border-top:1px solid var(--border);}}
</style>
</head>
<body>
<header><nav class="breadcrumb"><a href="{home}">ToolBox</a> / <a href="{home}#guides">使用指南</a> / <span>{title}</span></nav></header>
<main>
<h1>{title} 使用指南</h1>
<p class="lead">{intro}</p>
<h2>核心功能</h2>
<ul>{features}</ul>
<h2>适用场景</h2>
<ul>{scenarios}</ul>
<h2>使用步骤</h2>
<ol>{steps}</ol>
<h2>实用技巧</h2>
<ul>{tips}</ul>
<h2>常见问题</h2>
<dl>{faqs}</dl>
<div class="back"><a href="{tool_url}">→ 去使用 {title}（免费 · 纯前端 · 数据不上传）</a></div>
</main>
<footer>© 2026 ToolBox · 纯前端在线工具 · 数据不上传，安全可靠</footer>
</body>
</html>
'''

def li(items):
    return ''.join('<li>%s</li>' % html.escape(str(x)) for x in items)

def main():
    guide_map = []
    os.makedirs(GUIDES_DIR, exist_ok=True)
    for g in GUIDES:
        fn = '%s-guide.html' % g['slug']
        canonical = '%s/guides/%s' % (SITE, fn)
        page = (TPL
            .replace('{title}', html.escape(g['name']))
            .replace('{desc}', html.escape(g['desc']))
            .replace('{canonical}', canonical)
            .replace('{intro}', html.escape(g['intro']))
            .replace('{features}', li(g['features']))
            .replace('{scenarios}', li(g['scenarios']))
            .replace('{steps}', li(g['steps']))
            .replace('{tips}', li(g['tips']))
            .replace('{faqs}', ''.join('<dt>%s</dt><dd>%s</dd>' % (html.escape(q), html.escape(a)) for q, a in g['faqs']))
            .replace('{tool_url}', SITE + '/' + g['tool'])
            .replace('{home}', SITE + '/'))
        open(os.path.join(GUIDES_DIR, fn), 'w', encoding='utf-8').write(page)
        guide_map.append({'tool': os.path.basename(g['tool']), 'guide': '../../guides/%s' % fn, 'title': g['name'] + '使用指南'})
        print('OK: guides/%s' % fn)

    # 合并 guides.json
    jf = os.path.join(ROOT, 'json', 'guides.json')
    old = json.load(open(jf, encoding='utf-8')) if os.path.exists(jf) else []
    existing = {m['tool'] for m in old}
    merged = old + [m for m in guide_map if m['tool'] not in existing]
    json.dump(merged, open(jf, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
    print('guides.json 合并完成，共 %d 条' % len(merged))

    # 指南中心 index.html 追加条目
    ip = os.path.join(GUIDES_DIR, 'index.html')
    if os.path.exists(ip):
        s = open(ip, encoding='utf-8').read()
        new_li = ''.join('<li><a href="https://chenguangwu.github.io/guides/%s-guide.html">%s使用指南</a><span style="color:var(--muted);font-size:13px;"> — %s</span></li>'
                         % (g['slug'], html.escape(g['name']), html.escape(g['desc'])) for g in GUIDES)
        if '</ul>' in s:
            s = s.replace('</ul>', new_li + '</ul>', 1)
            open(ip, 'w', encoding='utf-8').write(s)
            print('guides/index.html 追加 %d 条' % len(GUIDES))

if __name__ == '__main__':
    main()
