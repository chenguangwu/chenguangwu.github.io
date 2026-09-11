#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""修正两个条形码工具页的真实缺陷（2026-09-11）。

背景：全站扫描「onclick 调用的函数在本页/共享脚本中均未定义」时确认 4 个页面存在
功能失效，其中：
  - tools/biz/barcode-generator.html —— 页面专属脚本长度为 0，5 个按钮全部无反应（已单独重建）
  - tools/biz/team-roster-generator.html —— 同类僵尸页（另行重建）
  - tools/legal/will-template-generator.html —— addAsset() 动态生成的 onchange 指向
    未定义的 updateAssetPlaceholder（已修）
  - tools/it/code-highlighter.html —— 经核实为误报（startTrial 位于示例代码文本内）

进一步核查条形码类页面时又发现两处真实缺陷：
  1) tools/it/barcode-code128.html 内嵌的 Code 128 编码表错误：数组含大量重复项
     （如 '11000101010' 出现 8 次），value 1 起即与 ISO/IEC 15417 标准表错位，
     且 Stop 写作 11 模块 '11000101010' + '11'，而标准 Stop 为 13 模块
     '1100011101011'。生成的条码并非合法 Code 128，扫码枪无法识别。
     修复：删除伪造表，统一改用 js/barcode-lib.js 的标准实现。
     该页 formula-box 另有一条模板套话（「依据指定格式规范在前端按规则随机或确定性生成内容」），
     一并替换为真实的编码说明。
  2) tools/science/barcode-pharmacode.html 的取值下限写成 1：Pharmacode 送入 1 时
     二进制去掉最高位后为空串，会渲染出一张空白图；送入 2 时只生成一个空白间隙、
     不含任何黑条。标准有效范围为 3 ~ 131070，一并修正。
"""
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)

changed = []


def read(path):
    with open(path, encoding='utf-8') as f:
        return f.read()


def write(path, text):
    with open(path, 'w', encoding='utf-8') as f:
        f.write(text)
    changed.append(path)


def ensure_lib_script(content, rel_prefix='../../'):
    """在 common.js 之后引入共享编码库（幂等）。"""
    marker = '<script src="%sjs/barcode-lib.js" defer></script>' % rel_prefix
    if marker in content:
        return content
    anchor = '<script src="%sjs/common.js" defer></script>' % rel_prefix
    if anchor not in content:
        raise SystemExit('未找到 common.js 引用锚点，无法插入编码库')
    return content.replace(anchor, anchor + '\n' + marker, 1)


# --------------------------------------------------------------------------
# 1) tools/it/barcode-code128.html
# --------------------------------------------------------------------------
p = 'tools/it/barcode-code128.html'
c = read(p)

if 'barcode-lib.js' not in c:
    c = ensure_lib_script(c)

start = c.find('// Code128 subset C (numeric only)')
end = c.find('function escapeHtml(s)')
if start == -1 or end == -1 or end <= start:
    raise SystemExit('barcode-code128：未定位到内嵌编码表代码块')

new_block = """// 编码逻辑由共享库 /js/barcode-lib.js 提供（Code 128，ISO/IEC 15417:2007）。
// 说明：本页早先内嵌的编码表存在重复项与错位（value 1 起即与标准表不符，Stop 亦非
// 标准的 13 模块图案），生成的条码并非合法 Code 128，扫码枪无法识别。现统一改用
// 标准表，与 EAN-13 / UPC-A / Code 39 共用同一套编码实现。
function generate(){
  var out = document.getElementById('output');
  var B = window.ToolBoxBarcode;
  if(!B){ out.innerHTML = '<div class="bar-text">编码库尚未加载完成，请稍后重试。</div>'; return; }
  var text = document.getElementById('data').value || '';
  var res = B.encode('code128', text || ' ');
  if(!res.ok){
    out.innerHTML = '<div class="bar-text" style="color:#b91c1c;">' + escapeHtml(res.error) + '</div>';
    return;
  }
  var canvas = B.renderCanvas(res.bits, {
    scale: 2, height: 120, showText: true, text: res.text, quiet: 10,
    fg: '#000000', bg: '#ffffff'
  });
  out.innerHTML = '';
  var wrap = document.createElement('div');
  wrap.className = 'bar-wrap';
  wrap.appendChild(canvas);
  out.appendChild(wrap);
  var info = document.createElement('div');
  info.className = 'bar-text';
  info.textContent = res.text + ' · Code ' + res.detail.subset + ' · ' +
    res.detail.symbolCount + ' 个符号 · 校验位 ' + res.detail.checksum + ' · ' +
    res.detail.widthModules + ' 模块';
  out.appendChild(info);
}
"""
c = c[:start] + new_block + c[end:]

# formula-box 套话 → 真实公式说明
old_fd = re.search(
    r'<p class="formula-desc" data-zh="本生成器依据指定格式规范[\s\S]*?</p>', c)
if old_fd:
    new_fd = (
        '<div class="formula-eq">总模块数 = 11 × (1 起始符 + n 数据符号 + 1 校验符) + 13 终止符<br>'
        '校验位 C = (V<sub>Start</sub> + Σ<sub>i=1…n</sub> V<sub>i</sub> × i) mod 103</div>\n'
        '  <p class="formula-desc" data-zh="Code 128 的每个符号固定占 11 个模块（3 条 3 空，'
        '条宽之和为偶数、空宽之和为奇数），终止符特殊、占 13 个模块。校验位按加权模 103 计算：'
        '起始符权重为 1，其后第 i 个数据符号权重为 i，把加权和除以 103 取余即得校验符号值。'
        '输入为纯数字且长度为偶数时，本页自动改用 Code C，每两位数字压缩为一个符号，条码更短。">'
        'Each Code 128 symbol is fixed at 11 modules; the stop pattern occupies 13 modules. '
        'The check symbol is a weighted modulo-103 sum: the start symbol has weight 1, and the '
        'i-th data symbol has weight i. Pure-digit even-length input automatically switches to '
        'Code Set C, encoding two digits per symbol.</p>'
    )
    c = c[:old_fd.start()] + new_fd + c[old_fd.end():]

# 首次加载自动生成一次（defer 脚本先于 DOMContentLoaded 执行，库此时已就绪）
if 'AUTO-GENERATE-ON-LOAD' not in c:
    tail = '</body>'
    idx = c.rfind(tail)
    if idx == -1:
        raise SystemExit('barcode-code128：未找到 </body>')
    c = (c[:idx]
         + '<!-- AUTO-GENERATE-ON-LOAD -->\n'
         + '<script>document.addEventListener("DOMContentLoaded",function(){'
           'if(typeof generate==="function")generate();});</script>\n'
         + c[idx:])

write(p, c)
print('✔ %s 已改用标准 Code 128 编码表' % p)

# --------------------------------------------------------------------------
# 2) tools/science/barcode-pharmacode.html
# --------------------------------------------------------------------------
p2 = 'tools/science/barcode-pharmacode.html'
c2 = read(p2)
before = c2

c2 = c2.replace('if(isNaN(num)||num<1||num>131070)return \'\';',
                'if(isNaN(num)||num<3||num>131070)return \'\';')
c2 = c2.replace("alert('请输入 1-131070 之间的数字')",
                "alert('请输入 3-131070 之间的数字（1 与 2 无法构成有效药码）')")

if c2 == before:
    raise SystemExit('barcode-pharmacode：未匹配到需要修正的取值下限，请人工核查')
write(p2, c2)
print('✔ %s 取值下限 1 → 3' % p2)

# --------------------------------------------------------------------------
# 3) 校验
# --------------------------------------------------------------------------
print('\n=== 校验 ===')
for path in changed:
    content = read(path)
    if path.endswith('barcode-code128.html'):
        bad = "CODE128B=[" in content
        print('  %s' % path)
        print('    伪造编码表已移除: %s' % ('✅' if not bad else '❌'))
        print('    已引用共享库: %s' % ('✅' if 'barcode-lib.js' in content else '❌'))
        print('    formula-desc 套话已替换: %s' % ('✅' if '依据指定格式规范' not in content else '❌'))
    if path.endswith('barcode-pharmacode.html'):
        print('  %s' % path)
        print('    下限校验 <3: %s' % ('✅' if 'num<3' in content else '❌'))
        print('    提示文案已更新: %s' % ('✅' if '3-131070' in content else '❌'))

# JSON-LD 合法性（若被改动）
for path in changed:
    for m in re.finditer(r'<script type="application/ld\+json">([\s\S]*?)</script>', read(path)):
        try:
            json.loads(m.group(1))
        except Exception as e:
            print('  ❌ %s 的 JSON-LD 非法: %s' % (path, e))
            sys.exit(1)
print('  JSON-LD 全部合法 ✅')
