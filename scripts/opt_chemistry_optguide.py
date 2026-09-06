#!/usr/bin/env python3
"""清理 chemistry 4 页（buffer-ph/molality/poh-to-ph/empirical-formula）opt-guide/opt-faq 通用套话。

套话「工作与生活中的相关计算与查询。」出现在三处：
  1) JSON-LD FAQ 第4问 acceptedAnswer text
  2) <section class="opt-guide"> 内 <h2>适用场景</h2><p>...</p>
  3) <section class="opt-faq"> 内 <dt>XXX适合哪些场景？</dt><dd>...</dd>
三处同步替换为真实化学场景。chemistry 其余 24 页无独立 opt-guide 区块（只有 deep-dive 区，由 content 驱动），不需清。
"""
import re
import sys

PLACEHOLDER = '工作与生活中的相关计算与查询。'

REAL = {
    'buffer-ph': '适用于缓冲溶液（如乙酸/乙酸钠、氨/铵盐）的 pH 估算与配制：生化实验维持酶反应最适 pH、分析化学滴定体系设计、教学演示缓冲容量与共轭酸碱比对 pH 的对数关系。',
    'molality': '适用于依数性相关计算：由质量摩尔浓度估算溶液冰点降低与沸点升高、计算渗透压（如植物细胞质壁分离、反渗透设计）、配制不受温度体积影响的基准溶液用于物理化学实验。',
    'poh-to-ph': '适用于碱性体系 pH 速算：实验室配制 NaOH/氨水等碱液的 pH 核对、废水与清洗液碱度评估、酸碱滴定终点前后 pH 变化预判。',
    'empirical-formula': '适用于化合物组成分析：由元素质量分数（元素分析仪数据）换算原子最简整数比、估算实验式并进一步推导分子式、有机与无机化学教学中的组成计算练习。',
}

FILES = {name: f'tools/chemistry/{name}.html' for name in REAL}


def process(dry=False):
    for name, real in REAL.items():
        path = FILES[name]
        s = open(path, encoding='utf-8').read()
        n = s.count(PLACEHOLDER)
        if n == 0:
            print(f'[skip] {name}: 未找到套话（可能已清理）')
            continue
        new = s.replace(PLACEHOLDER, real)
        if dry:
            print(f'[dry] {name}: 将替换 {n} 处套话（每页应 3 处）')
        else:
            open(path, 'w', encoding='utf-8').write(new)
            print(f'[ok] {name}: 已替换 {n} 处套话为真实场景')


if __name__ == '__main__':
    dry = '--dry' in sys.argv
    process(dry=dry)
