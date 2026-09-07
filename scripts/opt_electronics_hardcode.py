#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""清理 electronics 分类下硬编码 tool-intro-body 套话。

清理对象（仅 C 类，不动 deep-dive / 不动名称）：
- 6 页 intro 段后缀"专为电子工程师与爱好者打造。"+ 4 句通用 li：
    capacitor-calculator / resistor-calculator / voltage-divider /
    convert-capacitance / ohms-law / circuit-calculator
- 5 页 intro 段"免费在线电子工具。。专为开发者打造的在线工具，纯前端运行，代码不离开浏览器。"：
    smt-stencil / pcb-power / rc-time-constant / crystal-divider / resistor-color-code

名称（title / h1）保持不变，仅把套话描述替换为真实电子领域描述。
"""
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOOLS = os.path.join(ROOT, 'tools', 'electronics')

# 4 句通用 li（仅出现在 group(a) 的 intro-features ul）
GENERIC_LIS = [
    '支持常见电路参数计算',
    '纯前端运算，离线可用',
    '实时计算，结果即时显示',
    '支持多种元器件参数',
]

# group(a) intro 段：以"专为电子工程师与爱好者打造。"收尾 → 整段替换
A_INTRO_RE = re.compile(r'<p>[^<]*?专为电子工程师与爱好者打造。</p>')
# group(b) intro 段：含"专为开发者打造的在线工具，纯前端运行，代码不离开浏览器。"→ 整段替换
B_INTRO_RE = re.compile(r'<p>[^<]*?专为开发者打造的在线工具，纯前端运行，代码不离开浏览器。</p>')

# 各工具真实 intro 段（替换套话后缀，保留工具名语义、不改动名称）
INTRO_REPLACEMENTS = {
    # group(a)
    'capacitor-calculator': '电容计算支持串联/并联等效电容、RC 时间常数与储能计算，是电路设计与电容选型的一站式辅助工具，纯前端运行、数据不上传。',
    'resistor-calculator': '电阻计算支持串联/并联等效电阻、分压与功率核算，是电子电路设计与元器件选型的基础工具，纯前端运行、数据不上传。',
    'voltage-divider': '分压电路根据输入电压与电阻比计算分压点及带载分压结果，是偏置与信号调理设计的基础工具，纯前端运行、数据不上传。',
    'convert-capacitance': '电容（代码/耐压）换算支持 pF/nF/μF/mF/F 单位与 EIA 代码、耐压等级快速换算，是选型与读料的辅助工具，纯前端运行、数据不上传。',
    'ohms-law': '欧姆定律根据电压/电流/电阻/功率任意两项求其余两项，是电路分析与故障排查的基础计算工具，纯前端运行、数据不上传。',
    'circuit-calculator': '电路分析支持串并联电阻、分压与戴维南等效等常用电路量的快速求解，是电子电路设计的基础辅助工具，纯前端运行、数据不上传。',
    # group(b)
    'smt-stencil': 'SMT 钢网设计根据 PCB 焊盘尺寸与工艺要求计算开孔面积比、宽厚比与焊膏体积，是 SMT 焊接工艺设计的基础工具，纯前端运行、数据不上传。',
    'pcb-power': 'PCB 功耗温升估算根据板载功耗、散热面积与对流条件估算板温，是电源与功率板热设计校核的辅助工具，纯前端运行、数据不上传。',
    'rc-time-constant': 'RC 时间常数计算根据电阻与电容值计算时间常数 τ、各时间点充放电电压与截止频率，是暂态分析与滤波器设计的基础工具，纯前端运行、数据不上传。',
    'crystal-divider': '晶振分频计算根据目标输出频率与晶振频率计算 PLL 倍频/分频比并支持反向求分频系数，是时钟电路设计的基础工具，纯前端运行、数据不上传。',
    'resistor-color-code': '色环电阻识别支持 4/5 环色码识别与阻值计算，并提供阻值反查色环，是识别电阻标称值的必备工具，纯前端运行、数据不上传。',
}

GROUP_A = ['capacitor-calculator', 'resistor-calculator', 'voltage-divider',
           'convert-capacitance', 'ohms-law', 'circuit-calculator']
GROUP_B = ['smt-stencil', 'pcb-power', 'rc-time-constant', 'crystal-divider', 'resistor-color-code']


def strip_generic_li(body: str) -> str:
    """删 tool-intro-body 内 4 句通用 li，并清理由此产生的空 ul 与孤立『功能特点』h4。"""
    for li_text in GENERIC_LIS:
        body = re.sub(r'<li[^>]*>\s*' + re.escape(li_text) + r'\s*</li>\s*', '', body)
    # 删空 ul
    body = re.sub(r'<ul[^>]*>\s*</ul>', '', body)
    # 删孤立的『功能特点』h4（其后已无 ul；保留『使用场景』真实 ul）
    body = re.sub(
        r'<h4[^>]*>\s*<span class="h4-icon">[^<]+</span>功能特点\s*</h4>(?!\s*<ul)',
        '',
        body,
    )
    return body


def fix_file(path: str) -> bool:
    text = open(path, encoding='utf-8').read()
    new = text
    fn = os.path.basename(path).replace('.html', '')
    if fn in INTRO_REPLACEMENTS:
        repl = '<p>' + INTRO_REPLACEMENTS[fn] + '</p>'
        if fn in GROUP_A:
            new = A_INTRO_RE.sub(repl, new)
        else:
            new = B_INTRO_RE.sub(repl, new)
    if fn in GROUP_A:
        # 清理 intro-features 通用 li（仅 tool-intro-body 块内）
        def strip(m):
            return m.group(0).replace(m.group(1), strip_generic_li(m.group(1)))
        new = re.sub(r'class="tool-intro-body"[^>]*>(.*?)</div>', strip, new, flags=re.S)
    if new != text:
        open(path, 'w', encoding='utf-8').write(new)
        return True
    return False


def residual(text: str) -> dict:
    return {
        'A': 1 if A_INTRO_RE.search(text) else 0,
        'B': 1 if B_INTRO_RE.search(text) else 0,
        'li': sum(text.count(x) for x in GENERIC_LIS),
    }


def main():
    dry = '--dry' in sys.argv
    targets = [(f + '.html') for f in GROUP_A + GROUP_B]
    total = 0
    for fn in sorted(targets):
        path = os.path.join(TOOLS, fn)
        if not os.path.exists(path):
            print(f'  ⚠️  missing: {fn}')
            continue
        text = open(path, encoding='utf-8').read()
        before = residual(text)
        if dry:
            print(f'  [DRY] {fn}: residual={before}')
            continue
        changed = fix_file(path)
        if changed:
            after = residual(open(path, encoding='utf-8').read())
            ok = all(v == 0 for v in after.values())
            print(f'  {fn}: before={before} -> after={after}  {"✅" if ok else "❌残留"}')
            total += 1
        else:
            print(f'  {fn}: 无变化 before={before}')
    print(f'\n{"若 DRY 无误再正式运行" if dry else f"已修改文件 {total} 个"}')


if __name__ == '__main__':
    main()
