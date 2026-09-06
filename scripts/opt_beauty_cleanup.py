# -*- coding: utf-8 -*-
"""清理 beauty 分类旧套话：10 个 formula-desc、3 个 opt-faq、3 个 适用场景。"""
import os, re, glob, json

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CD = os.path.join(ROOT, "i18n", "tools", "content_deepdive.json")

# 每个 FD 文件的真实计算原理说明（替换套话）
FD_REAL = {
    "analysis-cost-profit": "毛利 = 营业收入 − 直接成本（产品/物料），毛利率 = 毛利 ÷ 营收；净利再扣房租、人工、营销等费用，净利率 = 净利 ÷ 营收。本工具按你填写的科目逐项核算并输出利润率，结果以你输入的数据为准，仅供经营参考。",
    "analysis-detector-diagnosis": "工具按水分、油分、色素、毛孔、敏感等维度给出相对参考值，依据经验区间（如水分 40–60、油分 30–55）判定肤质象限。数值受环境温湿度与近期护肤影响，仅供日常参考，异常或持续不适请到皮肤科评估。",
    "calc-1": "按出油、紧绷、敏感等维度问卷计分，综合得分落入对应区间判定干性/油性/混合/中性/敏感性。T 区与两颊得分差异大提示混合性。结果以你填写的感受为准，换季建议重测。",
    "checker-assessor-1": "按 PDCA 四阶段（计划-执行-检查-改进）逐项评分，均权得到体系成熟度。C（检查）提供数据、A（改进）形成闭环，任一阶段偏低均会拉低综合分，据此定位薄弱环。",
    "face-hair-match": "按圆、方、长、心形、菱形、椭圆、三角七种脸型匹配发型轮廓与修剪要点，以「扬长避短」为原则：长脸增横向体积、圆脸拉纵向、方脸柔化下颌。匹配度按各脸型修饰维度加权。",
    "nail-color-harmony": "基于色相环计算两色角度差：相邻 30° 内为类比色（和谐）、互补 180° 对比强、三角 120° 平衡。结合明度差综合给分，分数反映协调度而非绝对好坏。",
    "perming-rod": "卷度与卷杠直径正相关：φ14 mm 小杠紧卷、φ22 mm 中杠自然波纹、φ30 mm 大杠慵懒大卷。发长需足够绕杠（≥1.5 圈）才能成卷，短发受限难出大卷。",
    "recommender-cycle": "按肤质与目标生成洁面→水→精华→乳液→面霜→防晒步骤，遵循「水质先于油质、分子由小到大」吸收顺序；周期维度给出清洁、面膜、酸类的每周频率上限，以耐受为度。",
    "recommender-face-shape": "以三庭五眼比例分析脸型，匹配修饰发型：中庭偏长用刘海缩短、方脸用侧发遮下颌角。比例略偏仍协调时，发型用于视觉校正五官平衡。",
    "skin-tewl": "按经皮失水率分级：正常 < 10、轻度受损 10–20、重度 > 20 g/(m²·h)。问卷按紧绷、脱屑、刺痛频次映射到区间，高值提示屏障受损，需神经酰胺修护并暂停刷酸。",
    "hair-dye-ratio": "按目标色度差选双氧浓度：同度染用 6%（20 vol）、染浅 2–3 度用 9%（30 vol）、补根用 3%（10 vol）；染膏与双氧多为 1:1 或 1:1.5，严格按品牌说明配比避免色差与损伤。",
}

def main():
    data = json.load(open(CD, encoding="utf-8"))
    files = sorted(f for f in glob.glob(os.path.join(ROOT, "tools", "beauty", "*.html"))
                   if not f.endswith("index.html"))
    changed_fd = 0
    changed_faq = 0
    changed_scen = 0
    still_cliche = 0
    for f in files:
        base = os.path.basename(f)[:-5]
        s = open(f, encoding="utf-8").read()
        # 1) formula-desc
        if base in FD_REAL and 'class="formula-desc"' in s:
            new_fd = '<p class="formula-desc">%s</p>' % FD_REAL[base]
            s2, n = re.subn(r'<p class="formula-desc"[^>]*>.*?</p>', new_fd, s, count=1, flags=re.S)
            if n:
                s = s2
                changed_fd += 1
        # 2) opt-faq (用真实 faqs)
        key = "beauty/" + base
        if key in data and 'class="opt-faq"' in s:
            faqs = data[key].get("faqs", [])
            if faqs:
                new_faq = '<section class="opt-faq"><h2>常见问题</h2><dl class="faq-list">' + "".join(
                    "<dt>%s</dt><dd>%s</dd>" % (q["q"], q["a"]) for q in faqs
                ) + "</dl></section>"
                s2, n = re.subn(r'<section class="opt-faq">.*?</section>', new_faq, s, count=1, flags=re.S)
                if n:
                    s = s2
                    changed_faq += 1
        # 3) 适用场景 (替换 "工作与生活中的相关计算与查询" 套话)
        if '适用场景' in s and "工作与生活中的相关计算与查询" in s:
            key = "beauty/" + base
            if key in data and data[key].get("scenarios"):
                newp = "<h2>适用场景</h2><p>%s</p>" % data[key]["scenarios"][0]
                s2, n = re.subn(r"<h2>适用场景</h2><p>.*?</p>", newp, s, count=1, flags=re.S)
                if n:
                    s = s2
                    changed_scen += 1
        # 残留检查
        CLICHE = ["在对应的输入框或选项中填写", "工具名称：", "本计算器基于标准数学运算",
                   "本工程计算", "本速查内容依据权威标准", "本生成器依据指定格式规范",
                   "本校验工具依据对应数据格式", "本健康工具基于通用生理常数",
                   "本计算依据通用财务与货币规则", "工作与生活中的相关计算与查询",
                   "纯前端本地处理", "可先用该工具生成一版标准结果"]
        if any(w in s for w in CLICHE):
            still_cliche += 1
            print("STILL CLICHE:", base)
        open(f, "w", encoding="utf-8").write(s)
    print("beauty cleanup: FD=%d opt-faq=%d 适用场景=%d still_cliche=%d" % (changed_fd, changed_faq, changed_scen, still_cliche))

if __name__ == "__main__":
    main()
