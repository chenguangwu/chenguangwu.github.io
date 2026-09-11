#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""automotive 空壳页重建通用库。

背景：automotive 行业 44 个 C 级 + 1 个假 A 级（transport-calculator）页面均为
「head-only 死壳」——head 内误置 deep-dive section、无 <body> 开标签、无任何 UI 与
calc 逻辑，线上打开一片空白。本库负责：
  1. clean_head()：保留 head（meta/LD/脚本注入），剔除 head 内错置的 deep-dive 段；
  2. render()：按统一骨架渲染真实 body（导航/面包屑/输入区/结果区/公式框/场景卡/
     注意事项 + deep-dive 占位符 + calc 脚本），保持与站内 A 级工具页同构。
deep-dive 区块由 _build.py 依据 content_deepdive.json 在占位符处重建。
"""
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# deep-dive 兜底样式（_build.py 重建时会在占位符处注入同款样式与内容）
DEEP_STYLE = """<style>
.deep-dive{max-width:960px;margin:16px auto;padding:0 16px;}
.deep-dive > .card{margin-bottom:0;}
@media(max-width:600px){.deep-dive{margin:14px auto;padding:0 12px;}}
.deep-dive .dd-list{margin:8px 0 16px;padding-left:20px;}
.deep-dive .dd-list li{margin:6px 0;line-height:1.75;}
.deep-dive .dd-example{background:var(--card-bg,#fff);border:1px solid var(--border,#eee);border-radius:10px;padding:12px 14px;margin:8px 0 16px;}
.deep-dive .dd-ex-title{font-weight:600;color:var(--tool-accent,#FF6B35);margin-bottom:6px;}
.deep-dive .dd-ex-body{font-size:13px;line-height:1.85;color:var(--text,#333);word-break:break-word;}
.deep-dive .dd-faq{margin:8px 0 4px;}
.deep-dive .dd-faq dt{font-weight:600;margin-top:10px;color:var(--text,#333);}
.deep-dive .dd-faq dd{margin:4px 0 0;font-size:13px;line-height:1.85;color:var(--text-muted,#666);}
</style>"""

BODY_TPL = """<h1 class="sr-only">{{H1}}</h1>
<div class="nav">
  <a href="../../index.html">← ToolBox</a>
  <span>/ {{H1}}</span>
  <button class="theme-btn" onclick="ToolBox.toggleToolTheme()">🌙</button>
</div>
<nav class="breadcrumb" aria-label="面包屑导航" data-breadcrumb="1">
  <a href="../../index.html">首页</a>
  <span class="bc-sep">‹</span>
  <a href="index.html">🚗 汽车交通</a>
  <span class="bc-sep">‹</span>
  <span class="bc-current">{{H1}}</span>
</nav>
<div class="container">
  <div class="card tool-card-accent" style="--tool-accent:{{ACCENT}};">
    <h2>{{H2}}</h2>
    <p style="font-size:13px;color:var(--text-muted);margin-bottom:12px;">{{DESC}}</p>
{{INPUTS}}
    <div class="safe-main" id="result"></div>
    <div class="dist-grid" id="distGrid"></div>
    <div class="formula-box" id="formulaBox"></div>
    <div id="adviceBox"></div>
  </div>
{{CARDS}}
<!-- TOOLBOX-DEEP-DIVE -->
<!-- 注意事项区块 -->
<div class="tool-notes" style="--tool-accent:{{ACCENT}};">
  <div class="tool-notes-title">⚠️ 使用说明与注意事项</div>
  <ul>
    <li>本工具纯前端运行，数据不会上传到服务器</li>
    <li>建议在主流浏览器（Chrome/Safari/Firefox/Edge）中使用</li>
    <li>{{NOTES}}</li>
  </ul>
</div>
</div>
<script>
{{JS}}
</script>"""


def clean_head(path):
    """读源文件，返回清洗后的 head，同时回报是否命中 deep-dive 错置段。"""
    s = open(path, encoding='utf-8').read()
    head = s.split('</head>')[0]
    hit = '<!-- TOOLBOX-DEEP-DIVE -->' in head
    if hit:
        head = re.sub(r'\n?<!-- TOOLBOX-DEEP-DIVE -->[\s\S]*?</section>\s*', '\n', head, count=1)
    return head.rstrip() + '\n</head>'


def render(title, icon, accent, desc, inputs, cards, notes, js):
    """渲染 body 骨架。icon 仅用于 h2 前缀。"""
    h2 = icon + ' ' + title
    out = BODY_TPL
    for k, v in [
        ('{{H1}}', title), ('{{H2}}', h2), ('{{ACCENT}}', accent), ('{{DESC}}', desc),
        ('{{INPUTS}}', inputs.rstrip()), ('{{CARDS}}', cards.rstrip()),
        ('{{NOTES}}', notes), ('{{JS}}', js.rstrip()),
    ]:
        out = out.replace(k, v)
    return out


def rebuild(slug, head_subs=None, **kwargs):
    """重建单个工具页：head 清洗（可选文本替换）+ body 渲染 + 写回。返回 (ok, msg)。"""
    p = os.path.join(ROOT, 'tools/automotive', slug + '.html')
    if not os.path.exists(p):
        return False, '文件不存在: %s' % p
    head = clean_head(p)
    for old, new in (head_subs or []):
        if old not in head:
            return False, 'head 替换未命中: %s' % old[:60]
        head = head.replace(old, new)
    body = render(**kwargs)
    full = head + '\n<body>\n' + body + '\n</body>\n</html>\n'
    checks = {
        '<body>': '<body>' in full,
        '</body>': '</body>' in full,
        'formula-box': 'formula-box' in full,
        'input': len(re.findall(r'<input\b', full)),
        'select': len(re.findall(r'<select\b', full)),
        'calc': 'function calc' in full,
        'head_deepdive': '<!-- TOOLBOX-DEEP-DIVE -->' in full.split('</head>')[0],
    }
    if not (checks['<body>'] and checks['</body>'] and checks['formula-box']
            and (checks['input'] + checks['select']) >= 3 and checks['calc']
            and not checks['head_deepdive']):
        return False, '自检未通过: %s' % checks
    open(p, 'w', encoding='utf-8').write(full)
    return True, 'ok inputs=%d lines=%d' % (checks['input'], full.count('\n'))


# 供各工具 JS 复用的小工具（字符串注入，避免 f-string 与花括号冲突）
JS_HELPERS = """function fmtNum(n,d){d=d==null?2:d;if(!isFinite(n))return '--';return parseFloat(n.toFixed(d)).toString();}
function val(id){return parseFloat(document.getElementById(id).value);}
function str(id){return document.getElementById(id).value;}"""
