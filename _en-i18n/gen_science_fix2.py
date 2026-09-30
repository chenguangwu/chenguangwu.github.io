# -*- coding: utf-8 -*-
"""science 收尾补丁 2：交互态标签（点击后渲染）"""
import json, io, re, os

CJK = re.compile(r'[\u4e00-\u9fff]')

FIX = {
 'latlon-utm-converter': {
   '半球': 'Hemisphere',
 },
 'physics-calculator': {
   '请先选择一个公式': 'Please select a formula first',
   '⚠ 计算结果含无效值，请检查输入是否为有效正数。': '⚠ The result contains an invalid value; please check that the input is a valid positive number.',
 },
}


def main():
    for slug, add in FIX.items():
        p = 'i18n/tools/en/science/%s.json' % slug
        d = json.load(io.open(p, encoding='utf-8'))
        mp = d['map']
        n0 = len(mp)
        for k, v in add.items():
            mp[k] = v
        with io.open(p, 'w', encoding='utf-8') as f:
            json.dump(d, f, ensure_ascii=False, indent=1)
            f.write('\n')
        bad = [(k, v) for k, v in mp.items() if isinstance(v, str) and CJK.search(v)]
        print('%-24s +%d -> %d  CJK:%d' % (slug, len(mp) - n0, len(mp), len(bad)))


if __name__ == '__main__':
    main()
