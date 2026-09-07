# -*- coding: utf-8 -*-
"""exhibition 批：定点修复 6 个工具页的可见英文名、英文 fallback，以及 assessor-* 的 cat 错标。

- 全部 6 件：h2 可见英文名、<p data-zh> 英文 fallback 改为真实描述
- assessor-60/61/evacuation：cat=validator→calculator，formula-desc 校验套话→计算说明
每个替换都断言 old 存在，缺失即报错，避免静默漏改。
"""
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOOLS = os.path.join(ROOT, 'tools', 'exhibition')

EDITS = {
    "analysis-61.html": [
        (
            '<h2 data-zh="🔧 预算（费用/控制/优化）分析">🔧 Budget - ( Fee / Control / Optimization ) Analysis</h2>',
            '<h2 data-zh="🔧 预算（费用/控制/优化）分析">🔧 Exhibition Cost Statistics</h2>',
        ),
        (
            '<p style="font-size:13px;color:var(--text-muted);margin-bottom:12px;" data-zh="费用/控制/优化">Budget - ( Fee / Control / Optimization ) Analysis is available directly in your browser, with no data uploaded.</p>',
            '<p style="font-size:13px;color:var(--text-muted);margin-bottom:12px;" data-zh="费用/控制/优化">Exhibition Cost Statistics computes descriptive statistics for your cost and budget line items, entirely in your browser with no data uploaded.</p>',
        ),
    ],
    "analysis-pnl.html": [
        (
            '<h2 data-zh="🎪 预算（收入/支出/盈亏）分析">🎪 Budget</h2>',
            '<h2 data-zh="🎪 预算（收入/支出/盈亏）分析">🎪 Exhibition P&L Statistics</h2>',
        ),
        (
            '<p style="font-size:13px;color:var(--text-muted);margin-bottom:12px;" data-zh="收入/支出/盈亏">Budget is available directly in your browser, with no data uploaded.</p>',
            '<p style="font-size:13px;color:var(--text-muted);margin-bottom:12px;" data-zh="收入/支出/盈亏">Exhibition P&L Statistics summarizes revenue, expense and profit-loss figures with descriptive statistics, entirely in your browser with no data uploaded.</p>',
        ),
    ],
    "assessor-60.html": [
        (
            '<meta name="toolbox" content="cat=validator,industry=exhibition,icon=🎪,bg=#f3e5f5">',
            '<meta name="toolbox" content="cat=calculator,industry=exhibition,icon=🎪,bg=#f3e5f5">',
        ),
        (
            '本校验工具依据对应数据格式与语法规范进行合法性检查，实时给出校验结果与错误定位；纯前端运行，代码不离开浏览器。 工具名称：会后（评估/报告/跟进）总结。',
            '本工具依据会展投入产出与获客转化通用口径计算 ROI、线索转化率与单线索成本，纯前端运行，数据不上传。 工具名称：会后（评估/报告/跟进）总结。',
        ),
        (
            '<h2 data-zh="🎪 会后（评估/报告/跟进）总结">🎪 Assessor 60</h2>',
            '<h2 data-zh="🎪 会后（评估/报告/跟进）总结">🎪 Post-show Evaluation Report</h2>',
        ),
        (
            '<p style="font-size:13px;color:var(--text-muted);margin-bottom:12px;" data-zh="评估/报告/跟进">Assessor 60 is available directly in your browser, with no data uploaded.</p>',
            '<p style="font-size:13px;color:var(--text-muted);margin-bottom:12px;" data-zh="评估/报告/跟进">Post-show Evaluation Report evaluates exhibition ROI, lead conversion and cost-per-lead from your inputs, entirely in your browser with no data uploaded.</p>',
        ),
    ],
    "assessor-61.html": [
        (
            '<meta name="toolbox" content="cat=validator,industry=exhibition,icon=🎪,bg=#f3e5f5">',
            '<meta name="toolbox" content="cat=calculator,industry=exhibition,icon=🎪,bg=#f3e5f5">',
        ),
        (
            '本校验工具依据对应数据格式与语法规范进行合法性检查，实时给出校验结果与错误定位；纯前端运行，代码不离开浏览器。 工具名称：会展（评估/指标/优化）体系。',
            '本工具按 6 个维度（每项 1–5 分）量化评分并汇总，纯前端运行，数据不上传。 工具名称：会展（评估/指标/优化）体系。',
        ),
        (
            '<h2 data-zh="🎪 会展（评估/指标/优化）体系">🎪 Assessor 61</h2>',
            '<h2 data-zh="🎪 会展（评估/指标/优化）体系">🎪 Exhibition Scorecard</h2>',
        ),
        (
            '<p style="font-size:13px;color:var(--text-muted);margin-bottom:12px;" data-zh="评估/指标/优化">Assessor 61 is available directly in your browser, with no data uploaded.</p>',
            '<p style="font-size:13px;color:var(--text-muted);margin-bottom:12px;" data-zh="评估/指标/优化">Exhibition Scorecard rates an exhibition across 6 dimensions on a 1–5 scale and gives a composite score, entirely in your browser with no data uploaded.</p>',
        ),
    ],
    "assessor-evacuation.html": [
        (
            '<meta name="toolbox" content="cat=validator,industry=exhibition,icon=🔧,bg=#f3e5f5">',
            '<meta name="toolbox" content="cat=calculator,industry=exhibition,icon=🔧,bg=#f3e5f5">',
        ),
        (
            '本校验工具依据对应数据格式与语法规范进行合法性检查，实时给出校验结果与错误定位；纯前端运行，代码不离开浏览器。 工具名称：安全（疏散/消防/承重）评估。',
            '本工具依据人员密度、疏散宽度与距离、地面承重及消防设施等通用安全阈值测算风险，纯前端运行，数据不上传。 工具名称：安全（疏散/消防/承重）评估。',
        ),
        (
            '<h2 data-zh="🔧 安全（疏散/消防/承重）评估">🔧 Security</h2>',
            '<h2 data-zh="🔧 安全（疏散/消防/承重）评估">🔧 Venue Safety Assessment</h2>',
        ),
        (
            '<p style="font-size:13px;color:var(--text-muted);margin-bottom:12px;" data-zh="疏散/消防/承重">Security is available directly in your browser, with no data uploaded.</p>',
            '<p style="font-size:13px;color:var(--text-muted);margin-bottom:12px;" data-zh="疏散/消防/承重">Venue Safety Assessment checks evacuation width, egress distance, floor load and fire systems against common thresholds, entirely in your browser with no data uploaded.</p>',
        ),
    ],
    "stats-12.html": [
        (
            '<h2 data-zh="🔧 观众（统计/行为/反馈）研究">🔧 Stats 12</h2>',
            '<h2 data-zh="🔧 观众（统计/行为/反馈）研究">🔧 Audience Statistics</h2>',
        ),
        (
            '<p style="font-size:13px;color:var(--text-muted);margin-bottom:12px;" data-zh="统计/行为/反馈">Stats 12 is available directly in your browser, with no data uploaded.</p>',
            '<p style="font-size:13px;color:var(--text-muted);margin-bottom:12px;" data-zh="统计/行为/反馈">Audience Statistics computes descriptive statistics for traffic, dwell time and survey feedback, entirely in your browser with no data uploaded.</p>',
        ),
    ],
}


def main():
    total = 0
    for fn, repls in EDITS.items():
        p = os.path.join(TOOLS, fn)
        with open(p, 'r', encoding='utf-8') as f:
            s = f.read()
        for old, new in repls:
            assert old in s, "未找到待替换串 [%s]: %s" % (fn, old[:40])
            s = s.replace(old, new, 1)
            total += 1
        with open(p, 'w', encoding='utf-8') as f:
            f.write(s)
    print("HTML 定点修复完成，共 %d 处替换（6 个文件）" % total)


if __name__ == '__main__':
    main()
