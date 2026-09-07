# -*- coding: utf-8 -*-
"""opt_cosmetic_derm_hardcode.py — 清理 cosmetic-derm 6 页 opt 套话。

范围（探查确认）：
  (A) formula-desc 变体：0 页（cosmetic-derm 33 页均无 FD 占位）→ 不处理
  (C) tool-intro 块内 6 类通用套话：0 页（块已真实）→ 不处理
  (B) opt 套话「工作与生活中的相关计算与查询」：6 页各 3 处
       位置 = JSON-LD FAQ answer / <h2>适用场景</h2><p> / FAQ <dd>（「适合哪些场景？」回答）
       三处文本一致，替换为各页真实适用场景描述即可。
含 meta 回灌检测：替换后重新校验全站 JSON-LD 合法性（文本不含破坏引号）。
"""
import re, os, json, sys

PAGES = {
    'aging-1': '适用于护肤门诊初诊做光老化分级、居家自评当前光损伤阶段，以及 3–6 个月后按同一标准复评疗效。',
    'jiguangbochangbadian': '适用于选择激光设备时理解波长与靶色基的关系、评估深肤色治疗风险，以及医患沟通治疗方案。',
    'maokongcudafenji': '适用于每月同倍率拍照定级追踪毛孔变化、测评控油与酸类护肤效果，以及区分油性与衰老性毛孔成因。',
    'post-procedure-recovery': '适用于安排医美项目后的作息与约会、了解各项目红肿结痂的时间窗，以及识别异常恢复需及时就医。',
    'thread-lift': '适用于医患沟通线雕走线方向与提拉区域、理解即时提拉加渐进胶原的效果，以及认知走线深浅的风险边界。',
    'visia-spots': '适用于祛斑前区分表皮斑与真皮斑、治疗前后按面积量化对比，以及设定淡化而非根除的合理预期。',
}
OLD = '工作与生活中的相关计算与查询。'

def main():
    dry = '--dry' in sys.argv
    total = 0
    for n, new in PAGES.items():
        f = 'tools/cosmetic-derm/%s.html' % n
        assert os.path.exists(f), f
        s = open(f, encoding='utf-8').read()
        cnt = s.count(OLD)
        assert cnt > 0, '%s 未找到 opt 套话' % n
        if dry:
            print('[dry] %s 将替换 %d 处' % (n, cnt))
            continue
        s2 = s.replace(OLD, new)
        assert s2.count(OLD) == 0, '%s 替换后仍有残留' % n
        open(f, 'w', encoding='utf-8').write(s2)
        total += cnt
        print('已清理 %s: %d 处' % (n, cnt))
    if not dry:
        # meta 回灌检测：全站 JSON-LD 仍合法
        bad = []
        for f in os.listdir('tools/cosmetic-derm'):
            if not f.endswith('.html') or f == 'index.html':
                continue
            s = open('tools/cosmetic-derm/' + f, encoding='utf-8').read()
            m = re.search(r'<script type="application/ld\+json">(.*?)</script>', s, re.S)
            if m:
                try:
                    json.loads(m.group(1))
                except Exception as e:
                    bad.append((f, str(e)))
        print('JSON-LD 合法性检查: %s' % ('通过' if not bad else '失败 ' + str(bad)))
        print('合计清理 opt 套话: %d 处' % total)

if __name__ == '__main__':
    main()
