# -*- coding: utf-8 -*-
"""清理 railway 5 页 tool-intro-body 内 intro-scenes 的通用默认场景占位，替换为铁路工程真实场景。"""
import re, os

base = 'tools/railway/'
maps = {
    'noise-1.html': [
        '新建铁路沿线声环境评价与达标预判',
        '声屏障、隔声窗等降噪措施效果估算',
        '既有线路敏感点噪声治理方案比选',
    ],
    'power-5.html': [
        '机车选型与功率裕度校核',
        '列车编组质量与限速匹配',
        '山区、长大坡道线路牵引能力核算',
    ],
    'qiaoliang-qiaodun-zhizuo-hezai.html': [
        '桥墩与支座竖向承载力快速校核',
        '多支座受力分配与偏心验算',
        '既有桥梁荷载等级评估与加固判断',
    ],
    'slope-4.html': [
        '选线阶段最大坡度与限制坡度校核',
        '最小曲线半径与限速匹配',
        '山区展线、降坡方案比选',
    ],
    'diaoche-zuoye-xiaolv-youhua.html': [
        '编组站班计划作业量统计与效率核算',
        '取送车、解体溜放作业瓶颈识别',
        '车站作业组织优化与提效评估',
    ],
}

pat = re.compile(r'    <ul class="intro-scenes">.*?</ul>', re.S)
changed = []
for fn, items in maps.items():
    p = base + fn
    c = open(p, encoding='utf-8').read()
    new_ul = '    <ul class="intro-scenes">\n' + ''.join(f'      <li>{x}</li>\n' for x in items) + '    </ul>'
    c2 = pat.sub(new_ul, c, count=1)
    assert c2 != c, f'未替换（结构不符）: {fn}'
    open(p, 'w', encoding='utf-8').write(c2)
    changed.append(fn)

print('已清理 intro-scenes 通用占位的文件:', changed)
