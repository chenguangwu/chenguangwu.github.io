#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""清理 decor 分类硬编码套话（A/B 类），C 类块内套话 0 页无需处理。
A 类：detector-18 的 formula-desc 为「本校验工具依据对应数据格式与语法规范进行合法性检查…」错配校验变体
     （实际是室内空气质量检测判定工具），替换为 GB/T 18883 真实描述，保留生成器模板拼接的「工具名称：…」后缀。
B 类：wallpaper-quantity/skirting-length 的「工作与生活中的相关计算与查询。」各 3 处
     （JSON-LD acceptedAnswer text / 适用场景段 p / FAQ dd）→ 真实装修场景。
支持 --dry 预检（不写文件）。写回前校验 application/ld+json 合法。
"""
import re, os, sys, json

TOOLS = 'tools/decor'

# A 类：detector-18 FD 错配前缀（保留「工具名称：…」后缀）
DET_OLD = '本校验工具依据对应数据格式与语法规范进行合法性检查，实时给出校验结果与错误定位；纯前端运行，代码不离开浏览器。 '
DET_NEW = '本工具依据 GB/T 18883《室内空气质量标准》限值，对输入的甲醛、TVOC、苯、氨等污染物浓度逐项判定是否达标，并给出超标倍数与改善建议；纯前端运行，数据不离开浏览器。 '

# B 类：2 页 opt 套话 → 真实装修场景（每页同描述填 3 处）
REAL = {
 'wallpaper-quantity': '适合装修贴壁纸前按墙面尺寸与壁纸幅宽、幅长估算所需卷数与幅数，考虑对花损耗与同批备货，结果本地计算不上传。',
 'skirting-length':    '适合装修按房间各墙长与门洞宽度估算踢脚线净长度，窗台不扣减、阳角计入切角损耗，结果本地计算不上传。',
}
JUNK = '工作与生活中的相关计算与查询。'

def check_jsonld(s, n):
    m = re.search(r'<script type="application/ld\+json">(.*?)</script>', s, re.S)
    if not m: return True
    try:
        json.loads(m.group(1)); return True
    except Exception as e:
        print('  [ERROR] %s JSON-LD 非法: %s' % (n, e)); return False

def main():
    dry = '--dry' in sys.argv
    print('模式:', 'DRY(预检)' if dry else '正式写入')
    # A 类 detector-18
    fp = os.path.join(TOOLS, 'detector-18.html')
    s = open(fp, encoding='utf-8').read()
    c = s.count(DET_OLD)
    if c:
        s2 = s.replace(DET_OLD, DET_NEW)
        if not check_jsonld(s2, 'detector-18'): return
        if dry: print('  [detector-18] FD 将替换 %d 处' % c)
        else: open(fp, 'w', encoding='utf-8').write(s2); print('  [detector-18] FD 已替换 %d 处' % c)
    else:
        print('  [detector-18] 未命中错配 FD（跳过）')
    # B 类 2 页
    for n, real in REAL.items():
        fp = os.path.join(TOOLS, n + '.html')
        s = open(fp, encoding='utf-8').read()
        repls = [
            ('<h2>适用场景</h2><p>' + JUNK + '</p>', '<h2>适用场景</h2><p>' + real + '</p>'),
            ('<dd>' + JUNK + '</dd>', '<dd>' + real + '</dd>'),
            ('"text": "' + JUNK + '"', '"text": "' + real + '"'),
        ]
        total = 0; s2 = s
        for old, new in repls:
            cc = s2.count(old); s2 = s2.replace(old, new); total += cc
        if total == 0:
            print('  [%s] 无 opt 套话（跳过）' % n); continue
        if not check_jsonld(s2, n): return
        if dry:
            print('  [%s] opt 将替换 %d 处' % (n, total))
        else:
            open(fp, 'w', encoding='utf-8').write(s2)
            print('  [%s] opt 已替换 %d 处' % (n, total))
    print('decor hardcode 完成')

if __name__ == '__main__':
    main()
