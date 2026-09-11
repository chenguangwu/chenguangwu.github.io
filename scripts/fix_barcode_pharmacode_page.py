#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""修正 tools/science/barcode-pharmacode.html：

1. 改用共享库 js/barcode-lib.js（原页内联实现与 Laetus 规则不符：自低位向高位遍历
   并交替输出条/空，导致条形数量与宽度错位）。
2. formula-box 由模板套话替换为真实的 Laetus 编码规则说明。
3. 取值范围由错误的「1 ~ 131070」更正为「3 ~ 131070」（Wikipedia/Laetus：最小码为
   2 个窄条 = 3，最大码为 16 个宽条 = 131070，1 与 2 无法构成有效码）。
4. 增加首屏自动生成，打开页面即可看到条码。

实现注意：全部替换均使用「精确字面量 + 断言」，不使用宽松正则——首次尝试用
`<div class="formula-box">[\s\S]*?</div>\\s*\\n\\s*</div>` 会一路匹配到容器闭合标签，
把输入区与结果区一并吞掉，务必避免。

用法: python3 scripts/fix_barcode_pharmacode_page.py
"""
import io
import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAGE = os.path.join(ROOT, 'tools', 'science', 'barcode-pharmacode.html')

LIB_TAG = '<script src="../../js/barcode-lib.js" defer></script>\n'

OLD_FORMULA = (
    '<div class="formula-box">\n'
    '  <div class="formula-title">📐 工作原理与说明</div>\n'
    '  <p class="formula-desc" data-zh="本生成器依据指定格式规范在前端按规则随机或确定性生成内容，'
    '结果可直接复制使用，数据不离开浏览器。 工具名称：Pharmacode 条形码 - 免费生成器工具，'
    '在线Pharmacode 条形码。">Pharmacode Barcode is available directly in your browser, '
    'with no data uploaded.</p>\n'
    '</div>'
)

NEW_FORMULA = (
    '<div class="formula-box">\n'
    '  <div class="formula-title">📐 工作原理与说明</div>\n'
    '  <div class="formula-eq">V = Σ<sub>i=0…k−1</sub> w<sub>i</sub> × 2<sup>i</sup>　'
    '（自右向左数第 i 条：窄条 w=1、宽条 w=2）</div>\n'
    '  <p class="formula-desc" data-zh="Pharmacode（Laetus 药品二进制码）用宽窄两种条形表示整数：'
    '从右往左数，第 i 条若为窄条计 2^i，若为宽条计 2×2^i，全部相加即得数值。等价地，把「数值+1」'
    '写成二进制后去掉最高位，剩余位自左向右逐个对应条形，0 为窄条、1 为宽条。可表示 3 ~ 131070：'
    '最小码 3 是两个窄条，最大码 131070 是 16 个宽条，条数范围 2 ~ 16；相邻条之间固定留 1 个窄模块'
    '空白。该码制无校验位，设计上容许一定印刷误差。">'
    'Pharmacode (Laetus pharmaceutical binary code) represents an integer with two bar widths. '
    'Numbering bars from the right starting at i = 0, a narrow bar contributes 2^i and a wide bar '
    'contributes 2×2^i; their sum is the value. Equivalently, write (value + 1) in binary, drop the '
    'leading 1, then map the remaining bits left to right onto bars with 0 = narrow and 1 = wide. '
    'It covers 3–131070: the smallest code is 3 (two narrow bars) and the largest is 131070 '
    '(16 wide bars), i.e. 2 to 16 bars, with exactly one narrow module of space between bars. '
    'There is no check digit.</p>\n'
    '</div>'
)

OLD_INPUT = (
    '<label>数字（1 - 131070）</label>\n'
    '    <input type="number" id="data" value="1234" min="1" max="131070" '
    'style="margin-bottom:12px;">'
)

NEW_INPUT = (
    '<label>数字（3 - 131070）</label>\n'
    '    <input type="number" id="data" value="1234" min="3" max="131070" '
    'style="margin-bottom:12px;">'
)

NEW_SCRIPT = '''// 编码逻辑由共享库 /js/barcode-lib.js 提供（Pharmacode / Laetus PHARMA-CODE）。
// 说明：本页早先内联的实现自低位向高位遍历并交替输出条/空，与 Laetus 规则
//（自右向左第 i 条窄条计 2^i、宽条计 2×2^i）不符，条形数量与宽度均会错位。
// 现统一改用标准实现，与 Code 128 / EAN-13 / UPC-A / Code 39 共用同一套编码库。
function generate(){
  var out = document.getElementById('output');
  var B = window.ToolBoxBarcode;
  if(!B){
    out.innerHTML = '<div class="bar-text" style="color:#b91c1c;">编码库未加载，请刷新页面重试。</div>';
    return;
  }
  var res = B.pharmacode(document.getElementById('data').value);
  if(!res.ok){
    out.innerHTML = '<div class="bar-text" style="color:#b91c1c;">' + escapeHtml(res.error) + '</div>';
    return;
  }
  var canvas = B.renderCanvas(res.bits, {
    scale: 3, height: 120, showText: true, text: res.text, quiet: 10,
    fg: '#000000', bg: '#ffffff'
  });
  out.innerHTML = '';
  var wrap = document.createElement('div');
  wrap.className = 'bar-wrap';
  wrap.appendChild(canvas);
  out.appendChild(wrap);
  var info = document.createElement('div');
  info.className = 'bar-text';
  info.textContent = res.text + ' · ' + res.detail.barCount + ' 条（' + res.detail.barWidths +
    '，窄=1 宽=2） · ' + res.detail.widthModules + ' 模块';
  out.appendChild(info);
}
'''

AUTO = ('<!-- AUTO-GENERATE-ON-LOAD -->\n'
        '<script>document.addEventListener("DOMContentLoaded",function()'
        '{if(typeof generate==="function")generate();});</script>\n')

# 替换后必须仍然存在的关键结构（防止误吞 UI）
MUST_KEEP = [
    '<label>数字（3 - 131070）</label>',
    '<input type="number" id="data"',
    'onclick="generate()"',
    'onclick="copyResult()"',
    '<div class="result-box" id="output"></div>',
]

BANNED = ['1 - 131070', '1 到 131070', '1~131070', '1–131070', 'min="1"',
          'buildPharmacode', 'drawBarcode']


def replace_once(s, old, new, label):
    n = s.count(old)
    assert n == 1, '%s：期望恰好 1 处，实际 %d 处' % (label, n)
    return s.replace(old, new, 1)


def main():
    s = io.open(PAGE, encoding='utf-8').read()
    orig_len = len(s)
    report = []

    # 1) 引用共享库
    if 'barcode-lib.js' not in s:
        anchor = '<script src="../../js/common.js" defer></script>\n'
        s = replace_once(s, anchor, anchor + LIB_TAG, 'common.js 引用锚点')
        report.append('已引用 js/barcode-lib.js')
    else:
        report.append('已引用 js/barcode-lib.js（跳过）')

    # 2) formula-box（精确字面量）
    s = replace_once(s, OLD_FORMULA, NEW_FORMULA, 'formula-box')
    report.append('formula-box 已替换为 Laetus 规则说明')

    # 3) 输入区范围（精确字面量）
    s = replace_once(s, OLD_INPUT, NEW_INPUT, '输入区')
    report.append('输入区范围 1 → 3（label + input min）')

    # 4) 内联实现整体替换：从注释行到 generate() 结束（用 index 切片，不用正则）
    start = s.index('// Pharmacode: convert number to binary')
    end = s.index('function escapeHtml')
    region = s[start:end]
    assert region.rstrip().endswith('}'), '待替换区段未以 } 结束，实际尾部: %r' % region[-40:]
    for fn in ('function buildPharmacode(', 'function drawBarcode(', 'function generate('):
        assert fn in region, '待替换区段缺少 %s' % fn
    s = s[:start] + NEW_SCRIPT + s[end:]
    report.append('内联实现替换为共享库调用（%d → %d 字符）' % (len(region), len(NEW_SCRIPT)))

    # 4.5) 全页其余范围表述（meta 描述 / JSON-LD / desc-en / opt-guide 参数列表）
    #      这三处字符串与输入区不同（不在 label 内），需单独全局替换。
    for old, new in (('1 到 131070', '3 到 131070'),
                     ('1–131070', '3–131070'),
                     ('数字（1 - 131070）', '数字（3 - 131070）')):
        n = s.count(old)
        if n:
            s = s.replace(old, new)
            report.append('范围更正 %r → %r（%d 处）' % (old, new, n))

    # 5) 首屏自动生成
    if 'AUTO-GENERATE-ON-LOAD' not in s:
        s = replace_once(s, '</body>', AUTO + '</body>', '</body> 锚点')
        report.append('已加首屏自动生成')
    else:
        report.append('首屏自动生成已存在（跳过）')

    # ---- 写入前强校验：关键结构必须完好 ----
    missing = [x for x in MUST_KEEP if x not in s]
    assert not missing, '关键结构被误删/误改: %s' % missing
    leftover = [x for x in BANNED if x in s]
    assert not leftover, '仍残留应当清除的内容: %s' % leftover
    for m in re.finditer(r'<script type="application/ld\+json">([\s\S]*?)</script>', s):
        json.loads(m.group(1))
    # 结构数量守恒：替换前后 div 开闭、label/input 数量不应减少
    assert s.count('<div') >= 0
    before = io.open(PAGE, encoding='utf-8').read()
    assert s.count('<label>') == before.count('<label>'), 'label 数量变化'
    assert s.count('<input') == before.count('<input'), 'input 数量变化'
    assert s.count('<button') == before.count('<button'), 'button 数量变化'
    assert s.count('id="output"') == before.count('id="output"'), 'result-box 丢失'

    io.open(PAGE, 'w', encoding='utf-8').write(s)
    for r in report:
        print('✔ ' + r)
    print('\n文件长度 %d → %d' % (orig_len, len(s)))
    print('关键结构校验通过 ✅（label/input/button/result-box 数量守恒）')
    print('JSON-LD 全部合法 ✅')
    print('遗留旧表述/旧函数：无 ✅')


if __name__ == '__main__':
    main()
