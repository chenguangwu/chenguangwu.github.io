#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""清理 data 分类硬编码套话（A/B 类），C 类块内套话 0 页无需处理。
A 类：calc-1 的 formula-desc 为「本工具用于单位与格式换算(SI)」错配变体（实际 CSV转JSON 非单位换算），
     替换为 CSV转JSON 真实描述，保留生成器模板拼接的「工具名称：…」后缀（真实信息）。
B 类：random-6/csv-analyzer/chart-generator/data-cleaner/generator-14 的「工作与生活中的相关计算与查询。」
     各 3 处（JSON-LD acceptedAnswer text / 适用场景段 p / FAQ dd）→ 真实数据场景。
支持 --dry 预检（不写文件）。写回前校验 application/ld+json 合法。
"""
import re, os, sys, json

TOOLS = 'tools/data'

# A 类：calc-1 FD 错配前缀
CALC1_OLD = '本工具用于单位与格式换算，换算因子依据国际单位制(SI)及相关标准定义，结果保留输入精度；纯前端本地处理。'
CALC1_NEW = '本工具在浏览器本地将 CSV 文本解析并转换为 JSON 数组，支持自定义分隔符、引号与表头映射，数据不上传、代码不离开浏览器。'

# B 类：5 页 opt 套话 → 真实场景（每页同描述填 3 处）
REAL = {
 'random-6':       '适合抽奖抽样、模拟入参与测试数据构造，在设定范围内批量生成整数或浮点数，结果本地生成不上传。',
 'csv-analyzer':    '适合导入 CSV 后快速统计列类型、空值与分布，辅助清洗前检查与结构确认，数据本地解析不上传。',
 'chart-generator': '适合把数据系列画成柱状、饼图、散点等 SVG 图表并导出，用于汇报配图与占比对比，本地渲染不上传。',
 'data-cleaner':    '适合对文本或 CSV 做去重、去空与格式化规整，用于表格预处理与样本脱敏，本地运行不上传。',
 'generator-14':    '适合把文本或链接生成条码或二维码载体，用于物料标签与信息快速录入，本地编码不上传。',
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
    # A 类 calc-1
    fp = os.path.join(TOOLS, 'calc-1.html')
    s = open(fp, encoding='utf-8').read()
    c = s.count(CALC1_OLD)
    if c:
        s2 = s.replace(CALC1_OLD, CALC1_NEW)
        if not check_jsonld(s2, 'calc-1'): return
        if dry: print('  [calc-1] FD 将替换 %d 处' % c)
        else: open(fp, 'w', encoding='utf-8').write(s2); print('  [calc-1] FD 已替换 %d 处' % c)
    else:
        print('  [calc-1] 未命中错配 FD（跳过）')
    # B 类 5 页
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
    print('data hardcode 完成')

if __name__ == '__main__':
    main()
