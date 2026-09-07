# -*- coding: utf-8 -*-
"""
opt_convenience_hardcode.py — 清理 convenience 4 工具页硬编码套话（3 类）

(A) formula-desc 变体（全 4 页，正则替换 <p class="formula-desc"> 内容）：
    analysis-80     工程变体 → 真实损耗核算描述
    analysis-cost-10 财务变体 → 真实成本结构描述
    report-profit    财务变体 → 真实利润核算描述
    assessor-target  校验变体 → 真实选址评分描述
(B) assessor-target 的 opt 套话「工作与生活中的相关计算与查询」3 处（适用场景/opt-faq/JSON-LD）→ 真实选址场景
(C) analysis-80/analysis-cost-10/report-profit 的 tool-intro 三段块 6 类通用套话整体替换为真实便利店场景
    （assessor-target 块内已真实，不处理）

采用组件级正则替换，鲁棒于空白差异。
"""
import re
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def read(n):
    with open(os.path.join(ROOT, "tools", "convenience", n + ".html"), encoding="utf-8") as f:
        return f.read()


def write(n, s):
    with open(os.path.join(ROOT, "tools", "convenience", n + ".html"), "w", encoding="utf-8") as f:
        f.write(s)
    print("  [写回] %s.html" % n)


# (A) 每页真实 formula-desc（替换整段 <p class="formula-desc"> 内容）
FD_NEW = {
    "analysis-80": "按损耗量=应售量−实销量、损耗率=损耗量÷应售量×100% 的口径，分环节（进货/货架/盘点/报损）归集损耗并定位高发环节；结果为门店损耗管控的量化参考，改善决策以实际作业为准。",
    "analysis-cost-10": "按总成本=进货+人工+租金+水电+其他、毛利=营收−进货成本、净利=毛利−费用 的口径核算门店成本结构与盈亏平衡点；结果为成本管控测算参考，具体以真实账目为准。",
    "report-profit": "按毛利=营收−进货成本、营业利润=毛利−费用、经营现金流=收支净额 的口径生成简易利润表；结果为小微门店单期财务测算参考，持续账务请用专业记账，非税务或审计意见。",
    "assessor-target": "按人流量、竞争密度、常住人口、租金、可见性五维加权评分输出综合分与选址等级（A/B/C）；模型量化选址要素，结果为网点布局决策参考，最终盈利还看选品与运营。",
}

# (B) assessor-target opt 套话（3 处）
OPT_REPL = {
    '<p>工作与生活中的相关计算与查询。</p>':
        "<p>便利店新开网点选址打分、多候选点位横向对比、租金与客流匹配度敏感性分析。</p>",
    '<dd>工作与生活中的相关计算与查询。</dd>':
        "<dd>便利店选址评估、商铺投资研判、零售网点规划等需要量化打分的场景。</dd>",
    '"text": "工作与生活中的相关计算与查询。"':
        '"text": "便利店选址评估、商铺投资研判、零售网点规划等需量化打分的场景。"',
}

# (C) tool-intro 三段块真实化（组件级正则）
INTRO_BLOCK = {
    "analysis-80": (
        ["盘点差异归集", "损耗率行业对标", "高发环节定位", "改善前后对比"],
        ["门店月度损耗复盘", "临期与破损管控", "仓储损耗追踪", "改善措施验证"],
        "损耗（控制/分析/改善）体系：录入各环节损耗量与成因，量化损耗率、定位高发环节并输出改善方向，用于便利店与仓储损耗管控。",
    ),
    "analysis-cost-10": (
        ["成本分项汇总", "毛利结构拆解", "盈亏平衡测算", "方案对比模拟"],
        ["单店成本结构查看", "减租排班优化评估", "低动销汰换测算", "月度费用异常排查"],
        "成本（控制/分析/优化）体系：输入进货、人工、租金等成本，计算总成本与毛利结构、测算盈亏平衡点，对比优化方案，辅助门店成本管控。",
    ),
    "report-profit": (
        ["简易利润表生成", "毛利净利核算", "现金流差异提示", "多期趋势对比"],
        ["便利店月度利润核算", "营业利润与现金流差异分析", "多期利润趋势对比", "费用失控点定位"],
        "财务（利润/现金流/报表）核算：输入营收、成本与费用，自动核算营业利润、净利润与经营现金流，生成简易利润表，用于小微门店财务分析。",
    ),
}

GEN_FEATURES = ["纯前端处理，数据不上传服务器", "操作简单，一键完成", "实时显示结果，所见即所得", "支持复制和下载结果"]
GEN_SCENES = ["日常办公与学习", "开发调试与数据处理", "快速计算与格式转换", "信息查询与参考"]


def build_block(intro_text, features, scenes):
    fe = "\n".join("      <li>%s</li>" % x for x in features)
    sc = "\n".join("      <li>%s</li>" % x for x in scenes)
    return (
        '    <h4><span class="h4-icon">📝</span>工具简介</h4>\n'
        "    <p>%s</p>\n"
        '    <h4><span class="h4-icon">✨</span>功能特点</h4>\n'
        '    <ul class="intro-features">\n%s\n    </ul>\n'
        '    <h4><span class="h4-icon">🎯</span>使用场景</h4>\n'
        '    <ul class="intro-scenes">\n%s\n    </ul>\n    ' % (intro_text, fe, sc)
    )


def main():
    dry = "--dry" in sys.argv
    total = 0

    # (A) formula-desc
    for n, new in FD_NEW.items():
        s = read(n)
        new_s, cnt = re.subn(r'<p class="formula-desc">.*?</p>',
                             '<p class="formula-desc">%s</p>' % new, s, flags=re.S)
        if cnt == 0:
            print("  [警告-A] %s 未找到 formula-desc" % n)
            continue
        if not dry:
            write(n, new_s)
        else:
            print("  [DRY-A] %s 将替换 formula-desc ×%d" % (n, cnt))
        total += cnt

    # (B) opt 套话（assessor-target）
    s = read("assessor-target")
    for old, new in OPT_REPL.items():
        if old not in s:
            print("  [警告-B] assessor-target 未找到: %s" % old[:30])
            continue
        cnt = s.count(old)
        if not dry:
            s = s.replace(old, new)
            write("assessor-target", s)
        else:
            print("  [DRY-B] assessor-target 将替换 opt 套话 ×%d: %s" % (cnt, old[:30]))
        total += cnt

    # (C) tool-intro 块（组件级）
    for n, (feats, scenes, intro) in INTRO_BLOCK.items():
        s = read(n)
        # 是否含 6 类通用套话（任一类即视为待替换）
        if not any(g in s for g in GEN_FEATURES) and not any(g in s for g in GEN_SCENES):
            print("  [跳过-C] %s 无通用块套话" % n)
            continue
        # 1) 工具简介 <p>
        s2 = re.sub(r'(工具简介</h4>\s*<p>).*?(</p>)',
                    lambda m: m.group(1) + intro + m.group(2), s, flags=re.S)
        # 2) 功能特点 ul
        s2 = re.sub(r'<ul class="intro-features">.*?</ul>',
                    '<ul class="intro-features">\n' + "\n".join("      <li>%s</li>" % x for x in feats) + "\n    </ul>",
                    s2, flags=re.S)
        # 3) 使用场景 ul
        s2 = re.sub(r'<ul class="intro-scenes">.*?</ul>',
                    '<ul class="intro-scenes">\n' + "\n".join("      <li>%s</li>" % x for x in scenes) + "\n    </ul>",
                    s2, flags=re.S)
        if s2 == s:
            print("  [警告-C] %s 块替换无变化" % n)
            continue
        if not dry:
            write(n, s2)
        else:
            print("  [DRY-C] %s 将替换 tool-intro 三段块" % n)
        total += 1

    print("完成：%s，预计改动 %d 处" % ("DRY" if dry else "已执行", total))


if __name__ == "__main__":
    main()
