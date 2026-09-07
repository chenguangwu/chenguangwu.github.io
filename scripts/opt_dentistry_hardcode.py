#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""清理 dentistry 分类硬编码套话（A/B/C 三类）。

A 类（FD 错配变体）：
  - rater-risk-2：「本校验工具依据对应数据格式与语法规范进行合法性检查…」校验变体
    → 真实 Cariogram 描述，保留生成器模板「工具名称：」后缀，JSON-LD 合法。
B 类（opt 套话「工作与生活中的相关计算与查询。」）：
  - dental-arch-development / assessor-5 / zirconia-aesthetics 各 3 处
    （JSON-LD "text" / <h2>适用场景</h2><p> / FAQ <dd>）→ 真实口腔场景。
C 类（块内 6 类通用套话，tool-intro-body 块内）：
  - length-3 / analysis-11 / kouqiangai-tnm-shaichagongju：
    简介尾随通用语、功能特点 2 项套话、使用场景 4 项全通用 → 真实口腔内容。
仅改 tools/dentistry/*.html 源文件；--dry 仅校验命中。
"""
import sys, os, re

TOOLS = 'tools/dentistry'

# ---------- A 类：FD 错配 ----------
A_REPLS = {
    'rater-risk-2': (
        '本校验工具依据对应数据格式与语法规范进行合法性检查，实时给出校验结果与错误定位；纯前端运行，代码不离开浏览器。 ',
        '本工具基于 Cariogram 龋病风险模型，综合饮食、菌群、氟暴露、唾液等多因素加权评估未来新龋发生风险，给出风险等级与可控因素建议；纯前端运行，数据不上传。 ',
    ),
}

# ---------- B 类：opt 套话 ----------
SCENE = '工作与生活中的相关计算与查询。'
B_REPLS = {
    'dental-arch-development': '适合替牙期儿童牙弓宽度/长度发育监测、牙列拥挤与间隙不足初筛、早期矫治时机评估，以及正畸治疗前后的牙弓变化跟踪。',
    'assessor-5': '适合前牙全瓷修复比色前的材料代次初筛、修复体透光率与邻牙匹配评估，以及不同牙位（前牙美学区/后牙功能区）的氧化锆选择参考。',
    'zirconia-aesthetics': '适合修复方案制定时按牙位与美学需求选择氧化锆代次（3Y-5Y）、比色透光匹配评估，以及前牙美学区与后牙功能区材料权衡的初筛参考。',
}

# ---------- C 类：块内通用套话 ----------
# 每页：(简介新全文, feat1, feat2, scene1, scene2, scene3, scene4)
C_REPLS = {
    'length-3': (
        '儿童牙弓（长度/宽度）发育。输入儿童年龄与牙弓测量值，对照各年龄段参考范围，评估颌骨发育是否正常，用于正畸初筛参考。',
        '按年龄对照牙弓参考范围', '即时给出发育偏离提示',
        '替牙期牙弓宽度/长度发育监测', '牙列拥挤与间隙不足初筛', '早期矫治时机评估', '正畸治疗前后牙弓变化跟踪',
    ),
    'analysis-11': (
        '桥体跨度（缺牙区间）力学分析。输入缺牙区间跨度与材料弹性模量，估算固定桥挠度与受力分布，辅助修复设计安全评估。',
        '按跨度与材料估算挠度', '即时提示长跨度风险',
        '后牙长跨度固定桥设计评估', '前牙短跨度材料选择', '基牙负荷与挠度复核', '种植/可摘方案对比参考',
    ),
    'kouqiangai-tnm-shaichagongju': (
        '口腔癌（TNM）筛查工具。录入口腔病灶的 T、N、M 分期信息与症状，按 TNM 标准给出分期筛查结论与就医建议。',
        '按 AJCC 标准初筛分期', '即时给出就医提示',
        '口腔黏膜白斑/溃疡久不愈随访', '颈部无痛肿块排查', '病灶 T/N/M 信息录入筛查', '高危人群自我初筛参考',
    ),
}

def apply(path, repls, dry):
    s = open(path, encoding='utf-8').read()
    rep = []
    for old, new in repls:
        c = s.count(old)
        if c != 1 and not dry:
            print('  WARN %s 命中 %d 次(预期1): %s' % (os.path.basename(path), c, old[:30]))
        rep.append((old, new, c))
        s = s.replace(old, new)
    if not dry:
        open(path, 'w', encoding='utf-8').write(s)
    return rep

def main():
    dry = '--dry' in sys.argv
    print('模式:', 'DRY' if dry else '正式')
    total = 0
    # A
    for n, (old, new) in A_REPLS.items():
        p = os.path.join(TOOLS, n + '.html')
        if not os.path.exists(p):
            print('WARN 缺文件', p); continue
        rep = apply(p, [(old, new)], dry)
        total += sum(c for _,_,c in rep)
        for o,ne,c in rep:
            print('  [A] %s FD 命中 %d' % (n, c))
    # B
    for n, scene in B_REPLS.items():
        p = os.path.join(TOOLS, n + '.html')
        if not os.path.exists(p):
            print('WARN 缺文件', p); continue
        repls = [
            ('"text": "%s"' % SCENE, '"text": "%s"' % scene),
            ('<p>%s</p>' % SCENE, '<p>%s</p>' % scene),
            ('<dd>%s</dd>' % SCENE, '<dd>%s</dd>' % scene),
        ]
        rep = apply(p, repls, dry)
        total += sum(c for _,_,c in rep)
        print('  [B] %s opt 3处命中: %s' % (n, [c for _,_,c in rep]))
    # C
    for n, (intro, f1, f2, s1, s2, s3, s4) in C_REPLS.items():
        p = os.path.join(TOOLS, n + '.html')
        if not os.path.exists(p):
            print('WARN 缺文件', p); continue
        # 简介（按页精确）
        intro_old = {
            'length-3': '<p>儿童牙弓（长度/宽度）发育。免费在线工具，纯前端处理，数据不上传，保护隐私安全。</p>',
            'analysis-11': '<p>桥体跨度（缺牙区间）力学分析。免费在线工具，纯前端处理，数据不上传，保护隐私安全。</p>',
            'kouqiangai-tnm-shaichagongju': '<p>口腔癌（TNM）筛查工具。免费在线工具，纯前端处理，数据不上传，保护隐私安全。</p>',
        }[n]
        repls = [
            (intro_old, '<p>%s</p>' % intro),
            ('<li>操作简单，一键完成</li>', '<li>%s</li>' % f1),
            ('<li>实时显示结果，所见即所得</li>', '<li>%s</li>' % f2),
            ('<li>日常办公与学习</li>', '<li>%s</li>' % s1),
            ('<li>开发调试与数据处理</li>', '<li>%s</li>' % s2),
            ('<li>快速计算与格式转换</li>', '<li>%s</li>' % s3),
            ('<li>信息查询与参考</li>', '<li>%s</li>' % s4),
        ]
        rep = apply(p, repls, dry)
        total += sum(c for _,_,c in rep)
        print('  [C] %s 块内7处命中: %s' % (n, [c for _,_,c in rep]))
    print('总替换命中:', total)

if __name__ == '__main__':
    main()
