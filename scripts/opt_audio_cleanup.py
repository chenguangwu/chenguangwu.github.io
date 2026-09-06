#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""audio 分类旧套话清理（三处清理之二/三的残留部分）。
- audio 仅 analysis-1 的 formula-desc 为机器套话，替换为真实频谱分析原理说明。
- audio 无旧 opt-faq / 适用场景 区块，故仅需清理 formula-desc 一处。
- 不计 ASCII 双引号，内部一律中文引号。
"""
import os, re

ROOT = "tools/audio"

NEW_FD = {
    "analysis-1": (
        "频谱分析对输入时域信号做快速傅里叶变换（FFT），把各采样点映射为不同频率分量的"
        "复数系数；其模长代表该频率的能量（常取 20·log10 转成 dB 显示），相位代表时间偏移。"
        "频率分辨率等于采样率除以 FFT 长度，加汉宁窗可抑制帧边界不连续带来的频谱泄漏。"
        "全部在浏览器本地计算，数据不上传服务器。"
    ),
}


def main():
    dry = "--dry" in __import__("sys").argv
    changed = 0
    for base, new_text in NEW_FD.items():
        path = os.path.join(ROOT, base + ".html")
        if not os.path.exists(path):
            print("MISSING:", path)
            continue
        s = open(path, encoding="utf-8").read()
        new_p = '<p class="formula-desc">%s</p>' % new_text
        s2 = re.sub(r'<p class="formula-desc">.*?</p>', new_p, s, count=1, flags=re.S)
        if s2 == s:
            print("UNCHANGED:", base)
            continue
        if dry:
            print("DRY changed:", base)
        else:
            open(path, "w", encoding="utf-8").write(s2)
            print("OK changed:", base)
            changed += 1
    print("done, changed=%d" % changed)


if __name__ == "__main__":
    main()
