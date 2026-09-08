# -*- coding: utf-8 -*-
"""furniture 分类（2 工具）deep-dive 真实化：把缺数字算例的占位重写为真实可演示内容。"""
import json, re, sys

SRC = 'i18n/tools/content_deepdive.json'

CONTENT = {
    'furniture/desk-dimensions': {
        'title': '人体工学桌椅高度推荐',
        'scenarios': [
            '居家/办公选购桌椅',
            '站立办公台设置',
            '屏幕中心高度校准',
        ],
        'examples': [
            {'title': '方法', 'body': '按身高推算：坐姿桌高≈身高×0.46、椅面高≈身高×0.26、屏幕中心高≈身高×0.71、桌面深度电脑场景约 70 cm；站立桌高≈身高×0.62、屏心≈身高×0.95。'},
            {'title': '算例（演示）', 'body': '身高 170 cm：坐姿桌高 170×0.46≈78 cm、椅面 170×0.26≈44 cm、屏幕中心 170×0.71≈121 cm、深度 70 cm；站立模式桌高 170×0.62≈105 cm、屏心 170×0.95≈162 cm。结果供选购参考，可调升降款更稳。'},
        ],
        'faqs': [
            {'q': '比例为什么这么定？', 'a': '基于坐姿肘高与视线高度的统计均值（约身高 0.46/0.71），属经验推荐区间，个体臂腿比例不同可微调。'},
            {'q': '身高超范围怎么办？', 'a': '公式适用于 150–200 cm 多数人群；极高/极矮者按比例推算后再实测手肘与视线更准。'},
        ],
    },
    'furniture/detector-32': {
        'title': '家具质量等级评估（标准/检测）',
        'scenarios': [
            '采购前质量把关',
            '品控合规自检',
            '认证与检测对比',
        ],
        'examples': [
            {'title': '方法', 'body': '按家具类型选执行标准（木 GB/T 3324、金属 GB/T 3325、软体 QB/T 1952.1），核对甲醛≤1.5 mg/L、加载力≥1000 N、耐久性≥10000 次、稳定性≥0.10 四项是否达标，输出等级。'},
            {'title': '算例（演示）', 'body': '木家具 输入 甲醛 0.8、加载力 1200 N、耐久 10000 次、稳定性 0.15 → 四项全达标且甲醛>0.5，判定「一等品（E1级）」；若甲醛降到 0.4 则升「优等品（E0级）」，若加载力仅 800 N 则「不合格品」。'},
        ],
        'faqs': [
            {'q': 'E0 和 E1 什么区别？', 'a': '指甲醛释放限量等级，E0(≤0.5 mg/L) 严于 E1(≤1.5 mg/L)；以国标检测报告为准，本工具仅做输入核对演示。'},
            {'q': '稳定性系数怎么看？', 'a': '稳定性≥0.10 为一般合格门槛；数值越大越不易倾覆，儿童家具等另有更严要求。'},
        ],
    },
}


def main():
    apply = '--apply' in sys.argv
    d = json.load(open(SRC, encoding='utf-8'))
    for k, v in CONTENT.items():
        assert k in d, f'缺失条目 {k}'
        assert len(v['scenarios']) == 3 and len(v['examples']) == 2 and len(v['faqs']) == 2, f'{k} 结构不符'
        assert any(re.search(r'\d', x['body']) for x in v['examples']), f'{k} 缺数字'
        d[k] = v
        print('更新', k)
    if apply:
        json.dump(d, open(SRC, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
        print('已写入', SRC)
    else:
        print('（dry-run）')


if __name__ == '__main__':
    main()
