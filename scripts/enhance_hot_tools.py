#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ROADMAP R3 · 热门工具打磨
=======================
给一批「热门但功能单薄」的开发者高频工具注入静态「📚 速查参考」card。
- 纯静态 HTML，零 JS，不修改任何现有 calc() 逻辑，零风险。
- 内容为该领域真实、通用的速查数据（零编造数字）。
- 幂等：已含 TOOLBOX-REF-CARD 标记则跳过。
- 通用锚点：插入到 `<!-- 相关工具 -->` 之前（所有工具页均有此标记）。

用法:
  python3 scripts/enhance_hot_tools.py [--dry-run] [--limit N] [--only file]
"""
import os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ---- 真实速查参考卡内容（按工具相对路径 tools/xxx.html）----
REFCARDS = {
 'encode/base64.html': """
<div class="card tool-refcard">
  <h2>📚 Base64 速查参考</h2>
  <table style="width:100%;border-collapse:collapse;font-size:13px;margin-bottom:10px;">
    <thead><tr style="background:var(--bg);"><th style="padding:8px 10px;text-align:left;">项目</th><th style="padding:8px 10px;text-align:left;">说明</th></tr></thead>
    <tbody>
      <tr><td style="padding:8px 10px;border-top:1px solid var(--border);">编码规则</td><td style="padding:8px 10px;border-top:1px solid var(--border);">每 3 字节原始数据编码为 4 个字符，体积约增加 <strong>33%</strong></td></tr>
      <tr><td style="padding:8px 10px;border-top:1px solid var(--border);">标准字符集</td><td style="padding:8px 10px;border-top:1px solid var(--border);">A–Z a–z 0–9 + / ，填充符 <code>=</code></td></tr>
      <tr><td style="padding:8px 10px;border-top:1px solid var(--border);">URL-safe 变体</td><td style="padding:8px 10px;border-top:1px solid var(--border);">将 <code>+</code> <code>/</code> 替换为 <code>-</code> <code>_</code>，常用于 URL / 文件名</td></tr>
      <tr><td style="padding:8px 10px;border-top:1px solid var(--border);">典型用途</td><td style="padding:8px 10px;border-top:1px solid var(--border);">邮件附件(MIME)、Data URI、令牌传输、二进制转文本</td></tr>
    </tbody>
  </table>
  <p style="font-size:12px;color:var(--text-muted);">提示：Base64 是编码而非加密，不提供任何机密性保护。</p>
</div>
""",
 'it/json-minify.html': """
<div class="card tool-refcard">
  <h2>📚 JSON 规范速查</h2>
  <table style="width:100%;border-collapse:collapse;font-size:13px;margin-bottom:10px;">
    <thead><tr style="background:var(--bg);"><th style="padding:8px 10px;text-align:left;">要点</th><th style="padding:8px 10px;text-align:left;">说明</th></tr></thead>
    <tbody>
      <tr><td style="padding:8px 10px;border-top:1px solid var(--border);">合法值类型</td><td style="padding:8px 10px;border-top:1px solid var(--border);">string / number / object / array / true / false / null</td></tr>
      <tr><td style="padding:8px 10px;border-top:1px solid var(--border);">键与字符串</td><td style="padding:8px 10px;border-top:1px solid var(--border);">必须使用<strong>双引号</strong>，单引号不合法</td></tr>
      <tr><td style="padding:8px 10px;border-top:1px solid var(--border);">转义字符</td><td style="padding:8px 10px;border-top:1px solid var(--border);">\\" \\\\ \\/ \\b \\f \\n \\r \\t \\uXXXX</td></tr>
      <tr><td style="padding:8px 10px;border-top:1px solid var(--border);">压缩本质</td><td style="padding:8px 10px;border-top:1px solid var(--border);">移除所有无意义空白与换行，不改变语义</td></tr>
    </tbody>
  </table>
  <p style="font-size:12px;color:var(--text-muted);">常见错误：使用单引号、末尾多余逗号、含注释、数值带前导零——均会导致解析失败。</p>
</div>
""",
 'it/hash-multi.html': """
<div class="card tool-refcard">
  <h2>📚 哈希算法输出长度</h2>
  <table style="width:100%;border-collapse:collapse;font-size:13px;margin-bottom:10px;">
    <thead><tr style="background:var(--bg);"><th style="padding:8px 10px;text-align:left;">算法</th><th style="padding:8px 10px;text-align:left;">摘要长度(bit)</th><th style="padding:8px 10px;text-align:left;">十六进制字符数</th><th style="padding:8px 10px;text-align:left;">适用场景</th></tr></thead>
    <tbody>
      <tr><td style="padding:8px 10px;border-top:1px solid var(--border);">MD5</td><td style="padding:8px 10px;border-top:1px solid var(--border);">128</td><td style="padding:8px 10px;border-top:1px solid var(--border);">32</td><td style="padding:8px 10px;border-top:1px solid var(--border);">文件校验(非安全)</td></tr>
      <tr><td style="padding:8px 10px;border-top:1px solid var(--border);">SHA-1</td><td style="padding:8px 10px;border-top:1px solid var(--border);">160</td><td style="padding:8px 10px;border-top:1px solid var(--border);">40</td><td style="padding:8px 10px;border-top:1px solid var(--border);">已不推荐用于安全</td></tr>
      <tr><td style="padding:8px 10px;border-top:1px solid var(--border);">SHA-256</td><td style="padding:8px 10px;border-top:1px solid var(--border);">256</td><td style="padding:8px 10px;border-top:1px solid var(--border);">64</td><td style="padding:8px 10px;border-top:1px solid var(--border);">通用安全指纹</td></tr>
      <tr><td style="padding:8px 10px;border-top:1px solid var(--border);">SHA-512</td><td style="padding:8px 10px;border-top:1px solid var(--border);">512</td><td style="padding:8px 10px;border-top:1px solid var(--border);">128</td><td style="padding:8px 10px;border-top:1px solid var(--border);">高安全场景</td></tr>
    </tbody>
  </table>
  <p style="font-size:12px;color:var(--text-muted);">哈希是单向不可逆函数，用于完整性校验与指纹；存储密码须加盐并使用慢哈希(bcrypt/argon2)。</p>
</div>
""",
 'it/url-qr.html': """
<div class="card tool-refcard">
  <h2>📚 二维码容量与纠错</h2>
  <table style="width:100%;border-collapse:collapse;font-size:13px;margin-bottom:10px;">
    <thead><tr style="background:var(--bg);"><th style="padding:8px 10px;text-align:left;">版本</th><th style="padding:8px 10px;text-align:left;">尺寸</th><th style="padding:8px 10px;text-align:left;">字节模式容量(纠错L)</th></tr></thead>
    <tbody>
      <tr><td style="padding:8px 10px;border-top:1px solid var(--border);">1</td><td style="padding:8px 10px;border-top:1px solid var(--border);">21×21</td><td style="padding:8px 10px;border-top:1px solid var(--border);">17 字符</td></tr>
      <tr><td style="padding:8px 10px;border-top:1px solid var(--border);">10</td><td style="padding:8px 10px;border-top:1px solid var(--border);">57×57</td><td style="padding:8px 10px;border-top:1px solid var(--border);">271 字符</td></tr>
      <tr><td style="padding:8px 10px;border-top:1px solid var(--border);">40</td><td style="padding:8px 10px;border-top:1px solid var(--border);">177×177</td><td style="padding:8px 10px;border-top:1px solid var(--border);">2953 字符</td></tr>
    </tbody>
  </table>
  <p style="font-size:12px;color:var(--text-muted);">纠错级别 L/M/Q/H 可恢复约 7%/15%/25%/30% 破损；URL 属字节模式，长度越短越易扫。</p>
</div>
""",
 'it/wifi-qr-generator.html': """
<div class="card tool-refcard">
  <h2>📚 WiFi 二维码格式</h2>
  <table style="width:100%;border-collapse:collapse;font-size:13px;margin-bottom:10px;">
    <thead><tr style="background:var(--bg);"><th style="padding:8px 10px;text-align:left;">字段</th><th style="padding:8px 10px;text-align:left;">含义</th></tr></thead>
    <tbody>
      <tr><td style="padding:8px 10px;border-top:1px solid var(--border);">S</td><td style="padding:8px 10px;border-top:1px solid var(--border);">SSID（网络名称）</td></tr>
      <tr><td style="padding:8px 10px;border-top:1px solid var(--border);">T</td><td style="padding:8px 10px;border-top:1px solid var(--border);">加密类型：WPA / WEP / nopass</td></tr>
      <tr><td style="padding:8px 10px;border-top:1px solid var(--border);">P</td><td style="padding:8px 10px;border-top:1px solid var(--border);">密码（nopass 时省略）</td></tr>
      <tr><td style="padding:8px 10px;border-top:1px solid var(--border);">H</td><td style="padding:8px 10px;border-top:1px solid var(--border);">true 表示隐藏 SSID</td></tr>
    </tbody>
  </table>
  <p style="font-size:12px;color:var(--text-muted);">标准格式：WIFI:S:&lt;ssid&gt;;T:WPA;P:&lt;pwd&gt;;H:false;; 手机相机扫码即可免输密码连接。</p>
</div>
""",
 'it/qr-beautify.html': """
<div class="card tool-refcard">
  <h2>📚 二维码可读性提示</h2>
  <table style="width:100%;border-collapse:collapse;font-size:13px;margin-bottom:10px;">
    <thead><tr style="background:var(--bg);"><th style="padding:8px 10px;text-align:left;">要点</th><th style="padding:8px 10px;text-align:left;">建议</th></tr></thead>
    <tbody>
      <tr><td style="padding:8px 10px;border-top:1px solid var(--border);">纠错级别</td><td style="padding:8px 10px;border-top:1px solid var(--border);">越高容错越强，H 可遮挡约 30%</td></tr>
      <tr><td style="padding:8px 10px;border-top:1px solid var(--border);">对比度</td><td style="padding:8px 10px;border-top:1px solid var(--border);">前景/背景须足够对比，浅色渐变可能扫不出</td></tr>
      <tr><td style="padding:8px 10px;border-top:1px solid var(--border);">静默区</td><td style="padding:8px 10px;border-top:1px solid var(--border);">四周留白至少 4 个模块宽，避免被裁切</td></tr>
    </tbody>
  </table>
  <p style="font-size:12px;color:var(--text-muted);">美化时优先提升纠错级别，再调整配色，确保主流扫码器可识别。</p>
</div>
""",
 'it/password-strength.html': """
<div class="card tool-refcard">
  <h2>📚 密码强度标准</h2>
  <table style="width:100%;border-collapse:collapse;font-size:13px;margin-bottom:10px;">
    <thead><tr style="background:var(--bg);"><th style="padding:8px 10px;text-align:left;">要素</th><th style="padding:8px 10px;text-align:left;">建议</th></tr></thead>
    <tbody>
      <tr><td style="padding:8px 10px;border-top:1px solid var(--border);">长度</td><td style="padding:8px 10px;border-top:1px solid var(--border);">≥ 12 位（口令短语更佳）</td></tr>
      <tr><td style="padding:8px 10px;border-top:1px solid var(--border);">字符集</td><td style="padding:8px 10px;border-top:1px solid var(--border);">大小写字母 + 数字 + 符号组合</td></tr>
      <tr><td style="padding:8px 10px;border-top:1px solid var(--border);">避免</td><td style="padding:8px 10px;border-top:1px solid var(--border);">字典词、个人信息、连续/重复序列</td></tr>
      <tr><td style="padding:8px 10px;border-top:1px solid var(--border);">熵值</td><td style="padding:8px 10px;border-top:1px solid var(--border);">越高越难暴力破解，随机性是关键</td></tr>
    </tbody>
  </table>
  <p style="font-size:12px;color:var(--text-muted);">参考 OWASP / NIST 指南：优先使用长口令短语，而非强制频繁更换短密码。</p>
</div>
""",
}

ANCHOR = '\n<!-- 相关工具 -->'
MARK = 'TOOLBOX-REF-CARD'

def inject(filepath, html, dry_run):
    if not os.path.exists(filepath):
        print('  SKIP 不存在:', filepath); return False
    s = open(filepath, encoding='utf-8', errors='ignore').read()
    if MARK in s:
        print('  SKIP 已有参考卡:', filepath); return False
    card = '<!-- ' + MARK + ' -->\n' + html
    if ANCHOR in s:
        s = s.replace(ANCHOR, card + ANCHOR, 1)
    else:
        s = s.replace('</body>', card + '\n</body>', 1)
    if dry_run:
        print('  [DRY] 将注入:', filepath)
        return True
    open(filepath, 'w', encoding='utf-8').write(s)
    print('  OK 已注入:', filepath)
    return True

def main():
    dry = '--dry-run' in sys.argv
    only = None
    for a in sys.argv[1:]:
        if a.startswith('--only='): only = a.split('=',1)[1]
    items = [(k,v) for k,v in REFCARDS.items() if (only is None or k==only)]
    if '--limit' in sys.argv:
        i = sys.argv.index('--limit'); items = items[:int(sys.argv[i+1])]
    print('模式:', 'DRY-RUN' if dry else 'WRITE', '| 目标数:', len(items))
    for rel, html in items:
        inject(os.path.join(ROOT, 'tools', rel), html, dry)

if __name__ == '__main__':
    main()
