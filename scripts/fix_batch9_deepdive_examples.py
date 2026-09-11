#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""修正 detector-recorder-fuel / estimate-distance-1 的 deep-dive 示例数字。

① detector-recorder-fuel：原文「均值 8.0L、标准差 0.5L、2σ 上限 9.0L」与页面默认 12 条记录
   （含 10.5L 尖峰）实算不符——若 σ 仅 0.5，10.5 不可能落在 2σ 之外。按页面默认数据实算：
   均值 8.22L、样本标准差 0.74L、2σ 区间 6.73~9.70L。
② estimate-distance-1：原文用 27.8 m/s 近似导致制动距离 39.4m / 总 67m；页面按 100÷3.6=27.78 m/s
   实算为 39.3m / 67.1m。

注意：content_deepdive.json 规范 indent=1。
"""
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PATH = os.path.join(ROOT, 'i18n', 'tools', 'content_deepdive.json')

UPDATES = {
    'automotive/detector-recorder-fuel': (
        '12 次加油记录折算百公里油耗均值 8.0L、标准差 0.5L；2σ 上限=9.0L。'
        '若某次记录 10.5L 超出 9.0L，标记为异常区间，'
        '结合该期是否长途空调/短途拥堵判断是真实工况还是车辆故障前兆。',
        '12 次加油记录折算百公里油耗均值 8.22L、样本标准差 0.74L；2σ 区间≈6.73~9.70L。'
        '若某次记录 10.5L 超出上限 9.70L，标记为异常区间，'
        '结合该期是否长途空调/短途拥堵判断是真实工况还是车辆故障前兆；'
        '标准差占均值约 9%，说明日常波动本身不大，单点越界更值得关注。',
    ),
    'automotive/estimate-distance-1': (
        '车速 100km/h（27.8m/s）、反应时间 1s、干燥 μ≈1.0；反应距离=27.8×1=27.8m，'
        '制动距离=v²/(2μg)=27.8²/(2×1.0×9.81)≈39.4m，总≈67m。'
        '若雨天 μ≈0.6，制动距离增至≈65.6m，总停车≈93m，比干路多出近 40%。',
        '车速 100km/h（27.78m/s）、反应时间 1s、干燥 μ≈1.0；反应距离=27.78×1≈27.8m，'
        '制动距离=v²/(2μg)=27.78²/(2×1.0×9.81)≈39.3m，总停车≈67.1m。'
        '若雨天 μ≈0.6，制动距离增至≈65.5m，总停车≈93.3m，比干燥路面多出约 39%。',
    ),
}


def main():
    with open(PATH, encoding='utf-8') as f:
        data = json.load(f)
    total = len(data)
    for key, (old, new) in UPDATES.items():
        hit = False
        for e in data[key].get('examples', []):
            if old in e.get('body', ''):
                e['body'] = e['body'].replace(old, new)
                hit = True
        print('%-42s %s' % (key, '已修正' if hit else '未命中'))
    with open(PATH, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=1)
        f.write('\n')
    print('键数守恒: %d → %d' % (total, len(data)))


if __name__ == '__main__':
    main()
