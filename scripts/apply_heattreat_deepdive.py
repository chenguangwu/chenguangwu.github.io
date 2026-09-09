#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""heattreat 分类 deep-dive 真实化（替换"统一口径建模"泛化占位）— 全部 2 工具。
- 覆盖：analysis-39（金相组织/晶粒度/评级统计）、recorder-9（热处理控温记录/保温时间）。
- 算例数字均经 node 复算核验（/tmp/verify_b25.js，12/12 通过）。
- 指南页克制：1 篇（recorder-9 保温时间估算，专业度高/有计算依据），analysis-39 为统计型不铺量。
"""
import json, re, sys

SRC = 'i18n/tools/content_deepdive.json'

CONTENT = {
    'heattreat/analysis-39': {
        'title': '金相（组织/晶粒度/评级）分析',
        'scenarios': [
            '批次一致性：对同批试样的晶粒度/评级数据做统计，判离散程度',
            '异常筛查：用均值±标准差找偏离样本，定位可疑视场',
            '报告支撑：输出描述统计量附检测报告',
        ],
        'examples': [
            {'title': '方法', 'body': '算法（描述统计）：输入一组晶粒度级别或评级数值，算数据量 n、总和、均值、中位数、极差(最大−最小)、方差 σ²=Σ(x−x̄)²/n、标准差 σ=√σ²。用于评估批次分布与稳定性。'},
            {'title': '算例', 'body': '例（8 个视场晶粒度级别 G：6,6,7,6,5,7,6,6）：n=8，均值=6.13，中位数=6，极差=2，方差=0.359，标准差=0.60。标准差小说明晶粒度均匀；若某视场 G=3 会显著拉低均值、抬高标准差，提示混晶需复检。'},
        ],
        'faqs': [
            {'q': '晶粒度级别 G 越大越好吗？', 'a': 'G 是 ASTM E112 级别，数值越大晶粒越细；细晶通常强韧性好，但过细可能加工硬化。判据依材料与用途，本工具只做统计不评优劣。'},
            {'q': '标准差多大算异常？', 'a': '无绝对阈值，看工艺要求；一般 σ>1 或单值偏离均值>2σ 重点关注。本统计仅供参考，金相评判须结合图谱与标准。'},
        ],
    },
    'heattreat/recorder-9': {
        'title': '热处理控温记录',
        'scenarios': [
            '保温时间估算：由厚度与工艺估保温时长，便于排产',
            '工艺管理：记录炉温曲线，追溯每炉参数',
            '质量核查：对比实测与目标温度，判工艺合规',
        ],
        'examples': [
            {'title': '方法', 'body': '算法（保温时间）：保温分钟 ≈ 厚度(mm) × 工艺系数 k + 20；系数 k：退火1.8、正火1.2、淬火1.2、回火2.0、调质1.3；渗碳按渗层深度(约0.12–0.15mm/h)另算。钢种温度区间见内置表（如45钢淬火840–860℃、退火820–840℃）。'},
            {'title': '算例', 'body': '例1（45钢 淬火、厚度50mm）：50×1.2+20=80 分钟（约1.3h）。例2（20钢 退火、厚度30mm）：30×1.8+20=74 分钟（约1.2h）。例3（回火、厚度50mm）：50×2.0+20=120 分钟（2.0h）。'},
        ],
        'faqs': [
            {'q': '系数 k 从哪来？', 'a': '是经验估算系数（基于"厚度每增1mm约加 k 分钟+基础20分"），不同工艺导热/相变差异给不同 k；实际须按工艺规程与炉型调整，本工具仅估排产参考。'},
            {'q': '渗碳为什么特殊？', 'a': '渗碳保温由渗层深度决定（约0.12–0.15mm/h），与时间近线性而非厚度主导；薄件也可能长时间，故单列按渗层估算。'},
        ],
    },
}


def main():
    apply = '--apply' in sys.argv
    d = json.load(open(SRC, encoding='utf-8'))
    for k, v in CONTENT.items():
        try:
            assert len(v['scenarios']) == 3 and len(v['examples']) == 2 and len(v['faqs']) == 2, f'{k} 结构不符'
            for ex in v['examples']:
                if not re.search(r'\d', ex['body']):
                    print('⚠️ 缺数字警告:', k, ex['title'])
            d[k] = v
            print('新增/更新', k)
        except Exception as e:
            print('❌ 跳过', k, ':', e)
            continue
    if apply:
        json.dump(d, open(SRC, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
        print('已写入', SRC)
    else:
        print('（dry-run）')


if __name__ == '__main__':
    main()
