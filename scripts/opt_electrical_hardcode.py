#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""清理 electrical 分类下硬编码套话。

清理对象：
- A 类 2 页 formula-desc 错配：
    * calc-power-capacitance.html "输入两个参数，自动计算常用结果" → 真实补偿电容描述
    * voltage-capacity-battery.html "本工程计算基于标准物理与材料公式" → 真实蓄电池串并联描述
- B 类 1 页（battery-bank.html）JSON-LD "工作与生活中的相关计算与查询" → 真实场景
- C 类 7 页 tool-intro-body 套话：
    * 2 页含 8 句通用 li（calc-power-capacitance / voltage-capacity-battery）：删 li+简介后缀
    * 5 页 intro 段"是一款IT 开发领域的在线工具。专为开发者打造的在线工具，纯前端运行，代码不离开浏览器。"（battery-bank/power-factor/transformer-sizing/voltage-drop/load-curve）
      → 真实电气领域描述，移除"IT 开发"误分类与"专为开发者"错位措辞

JSON-LD 解析：脚本内拼接合法 JSON 字符串，确保 schema.org FAQ 仍 valid。
"""
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOOLS = os.path.join(ROOT, 'tools', 'electrical')

A_GENERIC = '输入两个参数，自动计算常用结果'
A_ENGINE = '本工程计算基于标准物理与材料公式'
B_OPT = '工作与生活中的相关计算与查询。'

GENERIC_LIS = [
    '纯前端处理，数据不上传服务器',
    '操作简单，一键完成',
    '实时显示结果，所见即所得',
    '支持复制和下载结果',
    '日常办公与学习',
    '开发调试与数据处理',
    '快速计算与格式转换',
    '信息查询与参考',
]

# 5 页 intro 段错误分类模板，工具名嵌入
IT_INTRO_RE = re.compile(
    r'(<h4>\s*<span class="h4-icon">📝</span>工具简介\s*</h4>\s*'
    r'<p>)([^<]+)是一款IT 开发领域的在线工具。专为开发者打造的在线工具，纯前端运行，代码不离开浏览器。(\s*</p>)'
)

# 各工具真实 intro 段（替换"IT 开发"与"专为开发者"措辞）
INTRO_REPLACEMENTS = {
    'battery-bank': '蓄电池组计算是一款电气工程领域的在线工具，专注铅酸/锂电串并联容量与电压核算，纯前端运行，数据不上传。',
    'load-curve': '用电负荷曲线是一款电力系统领域的在线工具，输入 24h 负荷自动算负荷率与峰谷差并绘图，纯前端运行，数据不上传。',
    'power-factor': '功率因数补偿是一款电气工程领域的在线工具，专注 cosφ 校正与补偿容量核算，纯前端运行，数据不上传。',
    'transformer-sizing': '变压器容量选型是一款电气工程领域的在线工具，按视在功率、同时系数与预留系数选 kVA，纯前端运行，数据不上传。',
    'voltage-drop': '电压降计算是一款电气工程领域的在线工具，按导线长度截面积与负载电流校验压降百分比，纯前端运行，数据不上传。',
}


def fix_a_class(text: str) -> str:
    """改 A 类 formula-desc 通用占位/工程错配。"""
    # calc-power-capacitance 通用占位 → 真实补偿电容描述
    text = text.replace(
        A_GENERIC,
        '输入有功功率与目标功率因数，自动求补偿电容无功容量（kvar）。'
    )
    # voltage-capacity-battery 工程错配 → 真实蓄电池描述
    text = text.replace(
        A_ENGINE,
        '本工具基于蓄电池容量/电压与串并联关系，'
    )
    return text


def fix_b_class(text: str) -> str:
    """battery-bank JSON-LD "工作与生活中的相关计算与查询" → 真实场景。"""
    return text.replace(
        B_OPT,
        '蓄电池组串并联容量与电压核算，UPS/光伏离网/通信基站/电动车等场景均可使用。'
    )


def fix_c_li(text: str, filename: str) -> str:
    """calc-power-capacitance / voltage-capacity-battery 删 8 句通用 li+简介后缀+空 ul/h4。"""
    # 简介段后缀（"<工具名>。免费在线工具…"等）替换为简短真实描述
    SUFFIX_INSIDE = '免费在线工具，纯前端处理，数据不上传，保护隐私安全。'
    if SUFFIX_INSIDE in text:
        # 找工具名
        m = re.search(r'<title>([^<]+)</title>', text)
        tool_name = m.group(1) if m else filename.replace('.html', '')
        # 用真实电气领域描述整段替换（处理 "<p>{tool_name}。{SUFFIX}</p>" 与 "<p>{SUFFIX}</p>" 两种）
        new_para = {
            'calc-power-capacitance': '功率因数补偿电容容量计算是一款电气工程领域的在线工具，输入有功功率与目标 cosφ，自动算补偿电容无功容量（kvar），纯前端运行，数据不上传。',
            'voltage-capacity-battery': '蓄电池组串并联容量与电压是一款电气工程领域的在线工具，按单体电压/容量与串并联数核算总电压与能量，纯前端运行，数据不上传。',
        }.get(filename.replace('.html', ''), f'{tool_name}是一款电气工程领域的在线工具，专注电气参数核算，纯前端运行，数据不上传。')
        # 整段 <p>…免费在线工具…</p> 替换
        text = re.sub(
            r'<p>[^<]*?' + re.escape(SUFFIX_INSIDE) + r'</p>',
            f'<p>{new_para}</p>',
            text,
        )

    # 删 tool-intro-body 内 8 句通用 li
    # 只针对 tool-intro-body 块内 li 处理（避免误删页面其他 li）
    def strip(m):
        body = m.group(1)
        for li_text in GENERIC_LIS:
            # 匹配可能带前后空白/标签的 li
            body = re.sub(
                r'<li[^>]*>\s*' + re.escape(li_text) + r'\s*</li>\s*',
                '',
                body,
            )
        # 删空 ul 及其孤立 h4（功能特点/使用场景）
        body = re.sub(r'<ul[^>]*>\s*</ul>', '', body)
        body = re.sub(r'<h4[^>]*>\s*<span class="h4-icon">[^<]+</span>(功能特点|使用场景)\s*</h4>(?!\s*<ul)', '', body)
        return m.group(0).replace(m.group(1), body)

    text = re.sub(
        r'class="tool-intro-body"[^>]*>(.*?)</div>',
        strip,
        text,
        flags=re.S,
    )
    return text


def fix_intro_it(text: str, filename: str) -> str:
    """5 页 intro "是一款IT 开发领域的在线工具…" → 真实电气领域描述。"""
    target = filename.replace('.html', '')
    if target not in INTRO_REPLACEMENTS:
        return text
    new_p = INTRO_REPLACEMENTS[target]
    return IT_INTRO_RE.sub(
        lambda m: m.group(1) + new_p + m.group(3),
        text,
    )


def fix_file(path: str, actions: list) -> bool:
    """actions: ['A','B','C','intro5'] 任选执行；返回是否改动。"""
    text = open(path, encoding='utf-8').read()
    new = text
    if 'A' in actions:
        new = fix_a_class(new)
    if 'B' in actions:
        new = fix_b_class(new)
    if 'C' in actions:
        new = fix_c_li(new, os.path.basename(path))
    if 'intro5' in actions:
        new = fix_intro_it(new, os.path.basename(path))
    if new != text:
        open(path, 'w', encoding='utf-8').write(new)
        return True
    return False


def main():
    if '--dry' in sys.argv:
        dry = True
    else:
        dry = False

    # A 类 2 页（formula-desc 通用占位/工程错配）
    a_pages = ['calc-power-capacitance.html', 'voltage-capacity-battery.html']
    # B 类 1 页（JSON-LD 套话）
    b_pages = ['battery-bank.html']
    # C 类 2 页（tool-intro-body li）
    c_pages = ['calc-power-capacitance.html', 'voltage-capacity-battery.html']
    # intro5：5 页 IT 领域错分类（与 b_pages 有 1 页重叠：battery-bank）
    intro_pages = ['battery-bank.html', 'load-curve.html', 'power-factor.html', 'transformer-sizing.html', 'voltage-drop.html']

    total_changed = 0
    residual = {'A': 0, 'B': 0, 'C': 0, 'intro5': 0}
    for fn in sorted(set(a_pages + b_pages + c_pages + intro_pages)):
        actions = []
        if fn in a_pages: actions.append('A')
        if fn in b_pages: actions.append('B')
        if fn in c_pages: actions.append('C')
        if fn in intro_pages: actions.append('intro5')
        path = os.path.join(TOOLS, fn)
        if not os.path.exists(path):
            print(f'  ⚠️  missing: {fn}')
            continue
        # 残留检查
        text = open(path, encoding='utf-8').read()
        before = {
            'A': (A_GENERIC in text) + (A_ENGINE in text),
            'B': B_OPT in text,
            'C': sum(text.count(x) for x in GENERIC_LIS),
            'intro5': 1 if IT_INTRO_RE.search(text) else 0,
        }
        if not dry:
            changed = fix_file(path, actions)
            if changed:
                # 复检残留
                after_text = open(path, encoding='utf-8').read()
                after = {
                    'A': (A_GENERIC in after_text) + (A_ENGINE in after_text),
                    'B': B_OPT in after_text,
                    'C': sum(after_text.count(x) for x in GENERIC_LIS),
                    'intro5': 1 if IT_INTRO_RE.search(after_text) else 0,
                }
                print(f'  {fn}: before={before} -> after={after}  {"✅" if all(v==0 for v in after.values()) else "❌残留"}')
                total_changed += 1
            else:
                print(f'  {fn}: 无变化（可能文件已清洁） before={before}')
        else:
            print(f'  [DRY] {fn}: actions={actions} residual={before}')

    print(f'\n{"若 DRY 无误再正式运行" if dry else f"已修改文件 {total_changed} 个"}')


if __name__ == '__main__':
    main()