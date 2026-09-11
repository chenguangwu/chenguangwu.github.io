#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""修正 cheshenkongqizulixishu 的 deep-dive 示例数字与倍数表述。

原文：…风阻 F=0.5·ρ·Cd·A·v²=0.5×1.225×0.30×2.2×27.8²≈311N，所需功率 P=F·v≈311×27.8≈8650W≈8.6kW。
      车速翻倍到 200km/h 时功率约增为 4 倍（约 69kW）。
问题：① 按 100 km/h = 27.78 m/s 精确计算 F≈312 N（原文 311 N 偏低约 0.3%）；
      ② 风阻功率 P=F·v 与车速立方成正比，车速翻倍应为约 8 倍（69 kW 数值本身正确，倍数表述矛盾）。

注意：content_deepdive.json 规范 indent=1，写回必须沿用。
"""
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PATH = os.path.join(ROOT, 'i18n', 'tools', 'content_deepdive.json')

KEY = 'automotive/cheshenkongqizulixishu'
OLD = ('风阻 F=0.5·ρ·Cd·A·v²=0.5×1.225×0.30×2.2×27.8²≈311N，所需功率 P=F·v≈311×27.8≈8650W≈8.6kW。'
       '车速翻倍到 200km/h 时功率约增为 4 倍（约 69kW）。')
NEW = ('风阻 F=0.5·ρ·Cd·A·v²=0.5×1.225×0.30×2.2×27.78²≈312N，所需功率 P=F·v≈312×27.78≈8660W≈8.7kW。'
       '车速翻倍到 200km/h 时，阻力随速度平方增至约 4 倍（≈1248N），'
       '而风阻功率随速度立方增至约 8 倍（≈69kW）。')


def main():
    with open(PATH, encoding='utf-8') as f:
        data = json.load(f)
    total = len(data)
    v = data[KEY]
    hit = False
    for e in v.get('examples', []):
        if OLD in e.get('body', ''):
            e['body'] = e['body'].replace(OLD, NEW)
            hit = True
    if not hit:
        print('未命中，请检查原文是否已变更')
        return
    with open(PATH, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=1)
        f.write('\n')
    print('已修正 cheshenkongqizulixishu 示例；键数守恒: %d → %d' % (total, len(data)))


if __name__ == '__main__':
    main()
