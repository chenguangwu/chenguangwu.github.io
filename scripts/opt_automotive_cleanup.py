# -*- coding: utf-8 -*-
"""清理 automotive：7 个旧 opt-faq/适用场景 套话→真实 faqs/scenarios[0]；13 个 formula-desc 套话→真实用途说明。"""
import re, glob, os, json

DATA = json.load(open("i18n/tools/content_deepdive.json", encoding="utf-8"))

# 7 个带旧 opt-faq + 适用场景 的文件：用 content_deepdive 真实 faqs 重建可见 opt-faq 区块
OPTFAQ_FILES = ["brake-pad-life", "calc-1", "cycle-belt", "fuel-anomaly",
                "pressure-fuel-oil", "tire-wear", "voltage-1"]

# 13 个 formula-desc 真实用途说明（整段替换）
FD_REPLACE = {
    "automotive/analysis-diagnosis": "按 OBD 故障码体系（P/C/B/U 与首位 0/1）归类动力、底盘、车身、网络故障，结合实时数据流定位异常传感器或执行器；结果仅供参考，实际以专业诊断仪与维修手册为准。",
    "automotive/analysis-strength": "按车架/车桥的载荷、截面与材料估算刚度和强度安全系数，辅助改装或承载校核；结果为理论估算，实际以厂家结构与有限元分析为准。",
    "automotive/calc-2": "发动机功率与扭矩单位换算（kW/PS/hp、N·m/kgf·m），按标准换算因子在浏览器本地完成，数据不上传；结果保留输入精度。",
    "automotive/calc-3": "胎压单位换算（bar/psi/kPa）与不同标准对照，纯前端本地计算，数据不离开浏览器。",
    "automotive/calc-4": "拖车球头垂直载荷按总重的 10%–15% 经验估算并校核球头额定值，纯前端本地计算，数据不离开浏览器。",
    "automotive/calc-5": "制动减速度按 v²/(2s) 由初速度与制动距离估算，纯前端本地计算；实际受路面附着与 ABS 影响。",
    "automotive/detector-recorder-fuel": "按油耗记录的时间序列检测异常波动（突变、趋势漂移），辅助发现喷油、氧传感器或驾驶习惯问题；纯前端运行，数据不离开浏览器。",
    "automotive/fuel-cost-calculator": "按里程、油耗与油价估算单程/周期油费，支持往返与多段核算，纯前端本地计算，数据不离开浏览器。",
    "automotive/recommender-6": "按胎压监测/充气建议给出目标值与补气提示，结合载重与季节微调；结果仅供参考，以车门框标贴为准。",
    "automotive/shipping-cost-compare": "按重量、体积与区域对比主流承运方式运费，含体积重取大逻辑，纯前端本地计算。",
    "automotive/tester-10": "喷油嘴测试按喷油量、均匀性与密封性判级，辅助判断是否需清洗或更换；结果仅供参考，以厂家标准为准。",
    "automotive/tester-11": "蓄电池按 CCA 冷启动电流与内阻评估健康度，辅助判断是否需更换；结果仅供参考，以专业检测仪为准。",
    "automotive/tire-pressure": "按原厂标准胎压结合季节与载重给出目标值，并说明温升对胎压的影响；结果仅供参考，以车门框标贴为准。",
}

n = 0
still_cliche = 0
CLICHE = ["工具名称：", "本计算器基于标准数学运算", "本工程计算基于标准物理", "本工具用于单位与格式换算",
          "本生成器依据指定格式规范", "在对应的输入框或选项中填写", "纳入现场复核清单",
          "工作与生活中的相关计算与查询", "高频复用模板", "本健康工具基于通用生理常数",
          "本校验工具依据对应数据格式", "本汽车计算基于标准工程公式", "结果保留输入精度；纯前端本地处理"]

for f in sorted(glob.glob("tools/automotive/*.html")):
    if f.endswith("index.html"):
        continue
    base = os.path.basename(f)[:-5]
    key = "automotive/" + base
    s = open(f, encoding="utf-8").read()
    changed = False

    # 1) 旧 opt-faq + 适用场景 → 真实内容
    if base in OPTFAQ_FILES:
        e = DATA.get(key, {})
        faqs = e.get("faqs", [])
        if faqs:
            new_faq = '<section class="opt-faq">\n<h2>常见问题</h2>\n' + "\n".join(
                '<div class="opt-faq-item"><div class="opt-faq-q">%s</div><div class="opt-faq-a">%s</div></div>' % (q["q"], q["a"])
                for q in faqs
            ) + '\n</section>'
            s2 = re.sub(r'<section class="opt-faq">.*?</section>', new_faq, s, count=1, flags=re.S)
            if s2 != s:
                s = s2
                changed = True
        # 适用场景替换
        scen = e.get("scenarios", [])
        if scen:
            newp = '<h2>适用场景</h2>\n<p>%s</p>' % scen[0]
            s3 = re.sub(r'<h2>适用场景</h2>.*?</p>', newp, s, count=1, flags=re.S)
            if s3 != s:
                s = s3
                changed = True

    # 2) formula-desc 套话替换
    new = FD_REPLACE.get(key)
    if new:
        pat = re.compile(r'<p class="formula-desc"[^>]*>.*?</p>', re.S)
        if pat.search(s):
            s4 = pat.sub('<p class="formula-desc">' + new + "</p>", s, count=1)
            if s4 != s:
                s = s4
                changed = True

    for c in CLICHE:
        if c in s:
            still_cliche += 1
            print("STILL CLICHE", base, ":", c)
            break

    if changed:
        open(f, "w", encoding="utf-8").write(s)
        n += 1
        print("OK", base)

print("cleaned", n, "| still_cliche_files", still_cliche)
