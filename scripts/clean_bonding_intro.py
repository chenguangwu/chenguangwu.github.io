#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""清理 bonding 5 个工具页 tool-intro-body 区块的 intro-scenes 占位（第四处占位残留区）。
将 STY3 占位 li 列表替换为各工具真实使用场景。"""
import re

base = '/Users/cgw/project/cgw/chenguangwu.github.io/tools/bonding/'
scenes = {
  'analysis-cost-4.html': [
    '胶粘剂选型时用批间用胶成本均值与极差判断哪种更省且波动小',
    '同配方多批次实测单耗用标准差监控来料一致性，超差即预警',
    '结构胶与机械紧固的单位连接成本对比，支撑替代决策',
  ],
  'analysis-resolution.html': [
    '粘接失效案例按严重度评分统计，用均值定位整体风险水平',
    '工艺改进前后各采一组评分对比均值与标准差，量化改进效果',
    '到货批次粘接抽检评分用极差与标准差判定某批是否异常',
  ],
  'assessor-cycle-lifespan.html': [
    '胶接/金属连接件输入材料参数估算可达循环寿命与安全系数',
    '抛光/磨削/车削/粗加工不同表面系数比较对疲劳寿命的影响',
    '输入目标设计循环次数判安全(sf≥2)/临界/不安全',
  ],
  'detector-27.html': [
    '金属/复合材料粘接质量超声筛查按回波与底波阈值判定等级',
    '大面积粘接面用可疑信号面积比判断缺陷密集程度',
    '信号异常时给出增大检测比例或辅以 X 射线复检的建议',
  ],
  'detector-26.html': [
    '胶层厚度在线质检算平均厚度、最大偏差与均匀性判定合格/返修',
    '同批次各测点厚度离散度监控，定位涂胶不均工序',
    '结合气泡/脱粘/夹杂缺陷等级综合给出处置建议',
  ],
}

pat = re.compile(r'<ul class="intro-scenes">[\s\S]*?</ul>')
for fn, sc in scenes.items():
    p = base + fn
    t = open(p, encoding='utf-8').read()
    new_ul = '<ul class="intro-scenes">\n      <li>' + '</li><li>'.join(sc) + '</li>\n    </ul>'
    new, n = pat.subn(new_ul, t, count=1)
    if n != 1:
        print('WARN', fn, 'matched', n)
        continue
    open(p, 'w', encoding='utf-8').write(new)
    print('OK', fn, 'intro-scenes 已替换')
