# -*- coding: utf-8 -*-
"""清理 beekeeping 分类探测器类的公式说明套话，替换为真实计算原理说明。"""
import os, re, glob

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CAT = "beekeeping"

# detector-13 的英文套话 formula-desc 替换为真实蜂螨寄生率说明
FD_FIX = {
    "detector-13": '<p class="formula-desc" data-zh="糖粉法检测，即每百只蜂寄生螨数；达阈值需防治。">糖粉法（抖落法）寄生率 = 检出蜂螨数 ÷ 样本蜂数 × 100%（如 100 只蜂检出 4 螨即 4%）；生产上常以每百蜂约 3 只（3%）为参考防治线，超过即安排断子期治螨。结果仅供蜂群健康监测参考，具体用药请遵照当地蜂药使用规范。</p>',
}

def main():
    for base, new_fd in FD_FIX.items():
        f = os.path.join(ROOT, "tools", CAT, base + ".html")
        if not os.path.exists(f):
            print("SKIP no file:", base)
            continue
        s = open(f, encoding="utf-8").read()
        pat = re.compile(r'<p class="formula-desc"[^>]*>.*?</p>', re.S)
        if not pat.search(s):
            print("SKIP no formula-desc:", base)
            continue
        s2 = pat.sub(new_fd, s, count=1)
        if s2 != s:
            open(f, "w", encoding="utf-8").write(s2)
            print("FIXED", base)
        else:
            print("UNCHANGED", base)
    print("beekeeping cleanup done")

if __name__ == "__main__":
    main()
