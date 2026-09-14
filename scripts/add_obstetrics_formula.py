#!/usr/bin/env python3
"""obstetrics 分类公式框补充（收口批次 C）：为缺框的 16 个计算类工具注入真实公式框。
用法：python3 scripts/add_obstetrics_formula.py [--apply]
锚点优先 'input-row'（位于静态表单 markup，不会落在 <script> 内；脚本内只拼 'tip-box'/'stat-card' 等），
回退 'card'。注入前剔除 <script>/<style> 区域，确保 formula-box 不落入脚本。
"""
import argparse
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOOLS_DIR = os.path.join(ROOT, "tools", "obstetrics")

ANCHORS = ["input-row", "card"]


def strip_script_style(s):
    return re.sub(r"<script[\s\S]*?</script>", "", re.sub(r"<style[\s\S]*?</style>", "", s))


FORMULAS = {
    "afi-normal": (
        "AFI = D\u03b1 + D\u03b2 + D\u03b3 + D\u03b4（四个象限最大羊水池垂直深度之和）；SDP = 单一最大羊水池深度",
        "羊水指数按四象限深度求和；AFI 5\u201324 cm 为正常，<5 cm 羊水过少，>24 cm 羊水过多；SDP 2\u20138 cm 正常。",
    ),
    "calc-risk": (
        "风险值 = 背景风险(\u5b9e\u9f84/\u4f53\u91cd/\u5b55\u5468) \u00d7 MoM \u6821\u6b63\uff1bMoM = \u5b9e\u6d4b\u503c / \u540c\u5b9e\u9f84\u4e2d\u4f4d\u6570\uff08AFP\u3001free \u03b2-hCG\uff09",
        "\u5510\u7b5b\u98ce\u9669\u7531\u5b9e\u9f84\u80cc\u666f\u98ce\u9669\u7ed3\u5408\u8840\u6e05\u6807\u5fd7\u7269 MoM \u503c\u6838\u7b97\uff0c\u8f93\u51fa 1:N \u7684\u51fa\u751f\u7f3a\u9677\u98ce\u9669\u3002",
    ),
    "ctg-fhr": (
        "\u57fa\u7ebf\u7387 110\u2013160 bpm \u6b63\u5e38\uff1b\u57fa\u7ebf\u53d8\u5f02 5\u201325 bpm \u4e3a\u4e2d\u5ea6\u53d8\u5f02\uff08\u6b63\u5e38\uff09",
        "\u7efc\u5408\u8bc4\u4f30\u57fa\u7ebf\u3001\u53d8\u5f02\u3001\u51cf\u901f\u3001\u5b57\u5b99\u7b49\u8981\u7d20\uff1a\u5f02\u5e38\u9879\u22650 \u4e14\u53ef\u7591\u9879\u22650 \u2192 \u6b63\u5e38\uff1b\u5426\u5219\u6309\u53ef\u7591/\u5f02\u5e38\u5206\u7ea7\u3002",
    ),
    "cycle-8": (
        "\u5185\u819c\u539a\u5ea6\u968f\u5468\u671f\uff1a\u589e\u6b96\u671f 4\u201312 mm\u3001\u5206\u6ccc\u671f 10\u201314 mm\uff1b\u6392\u5375\u524d \u22658 mm \u5229\u4e8e\u7740\u5e8a",
        "\u6309\u5468\u671f\u65e5\u6570\u5212\u5206\u589e\u6b96\u671f/\u5206\u6ccc\u671f\uff0c\u4ee5\u8be5\u671f\u53c2\u8003\u8303\u56f4\u8bc4\u4f30\u5185\u819c\u504f\u8584/\u6b63\u5e38/\u504f\u539a\u3002",
    ),
    "down-screening": (
        "\u98ce\u9669\u503c = \u80cc\u666f\u98ce\u9669(\u5b9e\u9f84/\u4f53\u91cd/\u5b55\u5468) \u00d7 MoM \u6821\u6b63\uff1bMoM = \u5b9e\u6d4b\u503c / \u540c\u5b9e\u9f84\u4e2d\u4f4d\u6570\uff08AFP\u3001free \u03b2-hCG\uff09",
        "\u5510\u6c0f\u7b5b\u67e5\u7531\u5b9e\u9f84\u80cc\u666f\u98ce\u9669\u7ed3\u5408\u8840\u6e05\u6807\u5fd7\u7269 MoM \u503c\u6838\u7b97\uff0c\u8f93\u51fa 1:N \u7684\u51fa\u751f\u7f3a\u9677\u98ce\u9669\u3002",
    ),
    "ectopic-hcg": (
        "\u53d8\u5316\u7387 = (hCG\u2082 \u2212 hCG\u2081) / hCG\u2081 \u00d7 100%\uff1b\u500d\u589e\u65f6\u95f4 DT = \u95f4\u9694 \u00d7 ln2 / ln(hCG\u2082/hCG\u2081)",
        "\u6b63\u5e38\u5bae\u5185\u5b55\u5a5a 48h hCG \u589e\u5e45\u2265 66%\uff08<1500\uff09/\u2265 53%\uff081500\u20133000\uff09/\u2265 30%\uff08>3000\uff09\uff1b\u2264 \u6b63\u5e38\u4e0b\u9650\u9700\u8b66\u60d5\u5f02\u4f4d\u5b55\u5a5a\u3002",
    ),
    "endometrial-thickness": (
        "\u6309\u5468\u671f\u65e5\u6570\u5206\u671f\uff1a\u6708\u7ecf\u671f 2\u20135 mm\u3001\u589e\u6b96\u671f 4\u201312 mm\u3001\u5206\u6ccc\u671f 10\u201314 mm",
        "\u4ee5\u5404\u671f\u53c2\u8003\u8303\u56f4\u8bc4\u4f30\u5185\u819c\u504f\u8584/\u6b63\u5e38/\u504f\u539a\uff1b\u7edd\u7ecf\u540e\u5185\u819c \u2264 4\u20135 mm \u591a\u4e3a\u840e\u7f29\u6027\u3002",
    ),
    "fetal-movement-count": (
        "12 \u5c0f\u65f6\u80be\u52a8\u6570 = (\u65e9 + \u4e2d + \u665a \u5404\u6bb5\u8ba1\u6570) \u00d7 4\uff1b\u2265 30 \u6b63\u5e38\uff0c20\u201329 \u4e34\u754c\uff0c< 20 \u504f\u5c11",
        "\u91c7\u7528 Cardiff \u8ba1\u6570\u6cd5\uff1a\u7d2f\u8ba1\u4e09\u6bb5\u80be\u52a8\u540e\u62d3\u5c55\u81f3 12 \u5c0f\u65f6\u4f30\u7b97\uff0c\u8d85\u8fc7\u9608\u503c\u63d0\u793a\u80be\u513f\u5bab\u5185\u72b6\u51b5\u3002",
    ),
    "fetal-weight-hadlock": (
        "Hadlock \u56db\u53c2\u6570 EFW(g) = 10^(1.3596 \u2212 0.00386\u00b7AC\u00b7FL + 0.0064\u00b7HC + 0.00061\u00b7BPD\u00b7AC + 0.0424\u00b7AC + 0.174\u00b7FL)",
        "\u53cc\u9876\u5f84/腹围简化法 EFW ≈ 双顶径×腹围×0.9 − 12\uff1bJohnson 法 EFW = (腹围 − 12) × 155\uff1bB 超测量参数估算胎儿体重\uff0cHadlock 四参数法最常用\uff1b估计体重 ≥ 4000 g 为巨大儿\u3002",
    ),
    "gestational": (
        "\u5b55\u5468 = \u672b\u6b21\u6708\u7ecf(LMP) + 280 \u5929 \u6216 \u8d85\u58f0 CRL/BPD/FL/HC \u751f\u7269\u7edf\u8ba1\u5f84\u7ebf\u53cd\u63a8\u6821\u6b63",
        "\u4ee5\u672b\u6b21\u6708\u7ecf\u6216\u8d85\u58f0\u6d4b\u503c\u786e\u5b9a\u5b55\u5468\uff0c\u8d85\u58f0 CRL \u5728\u65e9\u5b55\u671f\u6821\u6b63\u7cbe\u5ea6\u6700\u9ad8\u3002",
    ),
    "gestational-age": (
        "\u5b55\u5468 = \u672b\u6b21\u6708\u7ecf(LMP) + 280 \u5929 \u6216 \u8d85\u58f0\u5f84\u7ebf\u6821\u6b63\uff1b\u5468\u671f\u957f\u5ea6\u8c03\u6574\u9884\u4ea7\u671f",
        "\u7ed3\u5408 LMP \u4e0e\u8d85\u58f0\u6d4b\u91cf\u91cd\u65b0\u786e\u5b9a\u5b55\u5468\uff0c\u5468\u671f\u5dee\u8c03\u6574\u9884\u4ea7\u671f\uff08\u5468\u671f\u8d85\u8fc7 28 \u5929\u540e\u5ef6/\u524d\u79fb\uff09\u3002",
    ),
    "heart-rate": (
        "\u57fa\u7ebf 110\u2013160 bpm \u6b63\u5e38\uff1b\u53d8\u5f02 5\u201325 bpm \u6b63\u5e38\uff1b\u52a0\u901f \u2265 2/20min \u6b63\u5e38",
        "\u665a\u671f/\u5ef6\u957f/\u6b63\u5f26\u51cf\u901f\u4e3a\u75c5\u7406\u6027\uff1b\u53ef\u7591 1 \u9879\u6216\u75c5\u7406\u6027 \u2265 1 \u9879 \u2192 \u53ef\u7591/\u75c5\u7406\u6027 CTG\u3002",
    ),
    "ovarian-reserve": (
        "AMH \u5206\u7ea7\uff1a<0.5 \u6781\u4f4e\u3001<1.0 \u4f4e\u3001<3.5 \u6b63\u5e38\u3001<6.0 \u504f\u9ad8\u3001\u2265 6.0 \u6781\u9ad8\uff1bFSH < 10 \u6b63\u5e38\uff1bAFC \u2265 8 \u6b63\u5e38",
        "\u7efc\u5408 AMH/FSH/AFC/\u5e74\u9f84 \u8bc4\u5206\uff0c\u2265 4 \u5206\u63d0\u793a\u5375\u5de5\u53f6\u50a8\u51cf\u9000(DOR)\uff0cAMH > 6 \u63d0\u793a\u5375\u5de2\u9ad8\u53cd\u5e94(PCOS)\u3002",
    ),
    "postpartum-hemorrhage": (
        "\u5931\u8840\u91cf = (\u8840\u67d3\u6577\u6599\u6e7f\u91cd \u2212 \u5e72\u91cd) / 1.05\uff08g \u2248 mL\uff09\uff1b\u4f24\u514b\u6307\u6570 SI = \u5fc3\u7387 / \u6536\u7f29\u538b",
        "\u5931\u8840\u91cf \u2265 500 mL \u4e3a\u4ea7\u540e\u51fa\u8840\uff1bSI < 0.9 \u6b63\u5e38\u30010.9\u20131.1 \u8f7b\u5ea6\u30011.1\u20131.5 \u4e2d\u5ea6\u3001> 1.5 \u91cd\u5ea6\u4f24\u514b\u3002",
    ),
    "preeclampsia-prediction": (
        "\u8840\u7ba1\u751f\u6210\u6bd4\u503c = sFlt-1 / PlGF\uff1b< 38 \u6392\u9664\uff081\u5468 NPV 99.3%\uff09\uff0c38\u201385(\u65e9\u53d1)/110(\u665a\u53d1) \u7070\u8272\u533a\uff0c\u2265 \u9608\u503c \u786e\u8bca",
        "\u5b50\u7ba1\u75b2\u75c9\u9884\u6d4b\u4ee5\u8840\u7ba1\u751f\u6210\u56e0\u5b50\u6bd4\u503c\u4e3a\u6838\u5fc3\uff0c\u8d85\u8fc7\u786e\u8bca\u9608\u503c\u63d0\u793a\u5b50\u7ba1\u75b2\u75c9\u3002",
    ),
    "yangshuizhishu-afi-zhengchangfanwei": (
        "AFI = \u56db\u8c61\u9650\u7f8a\u6c34\u6c60\u6df1\u5ea6\u4e4b\u548c\uff1bMVP = \u6700\u5927\u5782\u76f4\u7f8a\u6c34\u6c60\u6df1\u5ea6",
        "AFI < 5 cm \u7f8a\u6c34\u8fc7\u5c11\u30015\u20138 cm \u4e34\u754c\u30018\u201325 cm \u6b63\u5e38\u3001> 25 cm \u7f8a\u6c34\u8fc7\u591a\uff1bMVP < 2 \u8fc7\u5c11\u30012\u20138 \u6b63\u5e38\u3001> 8 \u8fc7\u591a\u3002",
    ),
}


def build_box(eq, desc):
    return (
        '<div class="card formula-box">\n'
        '  <h3>\U0001f4d0 \u8ba1\u7b97\u516c\u5f0f</h3>\n'
        '  <div class="formula-eq">%s</div>\n'
        '  <p class="formula-desc">%s</p>\n'
        '</div>\n'
    ) % (eq, desc)


def find_anchor(s):
    clean = strip_script_style(s)
    for a in ANCHORS:
        m = re.search(
            r'<(?:\w+)\b[^>]*\bclass="[^"]*\b%s\b[^"]*"[^>]*>' % re.escape(a), clean)
        if m:
            # 在原文（含 script）中定位同一锚点，确保落在 markup
            orig = re.search(
                r'<(?:\w+)\b[^>]*\bclass="[^"]*\b%s\b[^"]*"[^>]*>' % re.escape(a), s)
            return orig.start() if orig else m.start()
    return -1


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    a = ap.parse_args()

    total = len(FORMULAS)
    done = skipped = 0
    for slug, (eq, desc) in FORMULAS.items():
        fp = os.path.join(TOOLS_DIR, slug + ".html")
        if not os.path.isfile(fp):
            print("  \u7f3a\u5931: %s" % slug)
            continue
        s = open(fp, encoding="utf-8").read()
        if 'class="formula-box"' in s:
            skipped += 1
            continue
        pos = find_anchor(s)
        if pos < 0:
            print("  \u65e0\u951a\u70b9(\u8df3\u8fc7): %s" % slug)
            continue
        box = build_box(eq, desc)
        s2 = s[:pos] + box + s[pos:]
        if a.apply:
            open(fp, "w", encoding="utf-8").write(s2)
        done += 1
        print("  \u8865\u6846: %s" % slug)
    print("\u516c\u5f0f\u6846\uff1a\u5df2\u8865 %d / \u7f3a\u6846 0 / \u8df3\u8fc7(\u5df2\u6709) %d\uff08\u5171 %d\uff09" % (done, skipped, total))


if __name__ == "__main__":
    main()
