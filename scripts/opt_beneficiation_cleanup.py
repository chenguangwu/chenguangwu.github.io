# -*- coding: utf-8 -*-
"""beneficiation 分类 formula-desc 套话清理（analysis-grade 1 文件）。"""
import os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOOLS_DIR = os.path.join(ROOT, "tools", "beneficiation")

FD_RE = re.compile(r'<p class="formula-desc"[^>]*>.*?</p>', re.S)

FD_TEXT = (
    "本工具按质量守恒做选矿金属平衡：原矿金属量 = 原矿处理量 × 原矿品位；"
    "尾矿金属量 = 尾矿产率 ×（1 − 精矿产率）× 原矿处理量 × 尾矿品位。"
    "回收率 =（原矿金属量 − 尾矿金属量）÷ 原矿金属量 × 100%，尾矿品位越低、回收率越高。"
    "产率与品位需与现场计量、化验值核对，本结果仅供工艺估算与教学演示。"
)

MAP = {
    "analysis-grade": FD_TEXT,
}


def main():
    for base, text in MAP.items():
        fn = os.path.join(TOOLS_DIR, base + ".html")
        if not os.path.exists(fn):
            print("SKIP missing:", base); continue
        s = open(fn, encoding="utf-8").read()
        new = '<p class="formula-desc">%s</p>' % text
        s2 = FD_RE.sub(new, s, count=1)
        still = 0
        for m in re.finditer(r'<p class="formula-desc"[^>]*>(.*?)</p>', s2, re.S):
            t = re.sub(r'<[^>]+>', '', m.group(1)).strip()
            if "本计算器基于标准数学运算" in t or "工具名称：" in t:
                still += 1
        if still:
            print("STILL CLICHE:", base)
        open(fn, "w", encoding="utf-8").write(s2)
        print("cleaned:", base)
    print("beneficiation formula-desc cleanup done")


if __name__ == "__main__":
    main()
