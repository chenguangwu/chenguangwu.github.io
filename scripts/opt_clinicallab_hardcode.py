#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""清理 clinical-lab 分类工具页硬编码套话。

范围（基于全面扫描结果）：
- formula-desc 占位 8 页（三变体，仅 formula-desc 块内，meta/JSON-LD 已真实无回灌）
- tool-intro 三段块（简介/功能/场景）套话 25 页全有：
  * 5 页"免费在线工具，纯前端处理，数据不上传，保护隐私安全"隐私套话（analysis-8/9/density-2/convert-39/convert-glucose-1）
  * 20 页"医疗专业工具，基于权威医学标准，仅供参考"医学套话（其余，含 flow/mic 已部分真实）
  → 全部重写为真实检验工具功能/场景
- opt-guide <p> 套话（工作与生活中的相关计算与查询）仅 2 页：flow-cytometry-ratio/mic-breakpoint

用法：
  python3 scripts/opt_clinicallab_hardcode.py --dry
  python3 scripts/opt_clinicallab_hardcode.py
"""
import re
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOOLS = os.path.join(ROOT, "tools", "clinical-lab")
DRY = "--dry" in sys.argv


FD_MAP = {
    "analysis-density-2": "分析物密度/浓度按测定温度或分子量折算（如尿比重温度校正），用于样本前处理与结果可比性；纯前端计算，结果仅供参考。",
    "blood-routine-reference": "按年龄与性别列出 WBC/RBC/Hb/PLT 等血常规参考区间并标越界项，便于报告初读；区间以本实验室为准，结果仅供参考。",
    "mic-breakpoint": "按 CLSI/EUCAST 标准将测得 MIC 与折点比对，判读敏感/中介/耐药；仅供复核，用药由感染科与药师决定。",
    "parasite-egg-id": "对粪便常见寄生虫虫卵形态要点做结构化对照，辅助镜检识别复习；确诊由寄生虫室判读。",
    "semen-analysis": "按 WHO 参考下限对精液量、浓度、活力、形态逐项对照，辅助男科报告初读；结果仅供参考。",
    "urine-sediment-atlas": "对尿沉渣有形成分（红细胞/白细胞/管型/结晶）的形态与提示做图谱式对照，辅助镜检复习。",
    "urinalysis-interpretation": "对尿常规干化学与镜检条目做结构化解释与组合提示，辅助报告初读；仅供复核，不替代诊断。",
    "vaginal-discharge-grading": "按 Nugent 或 AV 评分对阴道分泌物做分级计算，辅助报告理解；诊断与用药由妇科医师决定。",
}

INTRO_MAP = {
    "analysis-8": {
        "intro": "8 项常见检验指标批量对照工具。按各自参考区间标出偏高/偏低项，生成复查清单；仅供复核，不替代诊断。",
        "feats": "<li>8 项组合区间比对</li><li>异常项自动高亮</li><li>前后报告对比</li>",
        "scenes": "<li>体检初读与复查清单</li><li>随访趋势跟踪</li><li>教学演示项目关联</li>",
    },
    "analysis-9": {
        "intro": "9 项检验组合批量对照工具。统一标出越界项并按肝/肾/心方向分类，便于套餐初读；仅供复核。",
        "feats": "<li>9 项组合区间比对</li><li>异常项分类高亮</li><li>前后报告对比</li>",
        "scenes": "<li>门诊套餐初读</li><li>年度健康管理</li><li>教学演示多项目联动</li>",
    },
    "analysis-density-2": {
        "intro": "分析物密度/浓度换算工具。按测定温度或分子量折算（如尿比重温度校正），用于样本前处理与结果可比性；纯前端计算。",
        "feats": "<li>温度/分子量折算</li><li>标准品配制换算</li><li>结果可比性校正</li>",
        "scenes": "<li>尿比重温度校正</li><li>标准品稀释折算</li><li>教学演示密度-浓度关系</li>",
    },
    "autoantibody-interpretation": {
        "intro": "自身抗体（ANA/ENA/dsDNA 等）滴度与模式结构化提示工具。帮助理解报告条目含义，需结合临床；不替代诊断。",
        "feats": "<li>滴度与荧光模式对照</li><li>ENA 多项梳理</li><li>参考提示</li>",
        "scenes": "<li>风湿免疫门诊初读</li><li>抗体谱指向梳理</li><li>教学演示报告逻辑</li>",
    },
    "biochemistry-ratio": {
        "intro": "生化比值（A/G、钠钾比、钙磷乘积、阴离子间隙）计算器。快速识别蛋白/电解质失衡模式；仅供提示。",
        "feats": "<li>多比值一键计算</li><li>异常高亮</li><li>公式说明</li>",
        "scenes": "<li>肝病随访白球比</li><li>肾钙磷乘积评估</li><li>代酸 AG 分型</li>",
    },
    "blood-gas-analysis": {
        "intro": "血气酸碱失衡判断工具。按 pH/PaCO2/HCO3- 与代偿公式判型，辅助报告复核；不替代床旁判断。",
        "feats": "<li>三要素代偿判读</li><li>急慢性与混合失衡提示</li><li>公式说明</li>",
        "scenes": "<li>急诊 ICU 血气复核</li><li>教学演示代偿公式</li><li>术前评估</li>",
    },
    "blood-routine-reference": {
        "intro": "血常规参考区间查询工具。按年龄性别列出 WBC/RBC/Hb/PLT 区间并标越界；区间以本实验室为准。",
        "feats": "<li>年龄性别区间对照</li><li>越界项高亮</li><li>趋势提示</li>",
        "scenes": "<li>儿童成人贫血判定</li><li>化疗随访</li><li>教学演示区间差</li>",
    },
    "cardiac-marker-curve": {
        "intro": "心肌标志物时间序列展示工具。展示 cTn/CK-MB/BNP 变化与 99th 切点，辅助复核；不替代心内判断。",
        "feats": "<li>时序曲线绘制</li><li>99th 切点标注</li><li>升高回落模式提示</li>",
        "scenes": "<li>胸痛 0/3/6h 监测</li><li>心衰 BNP 趋势</li><li>教学演示动力学</li>",
    },
    "coagulation-inr": {
        "intro": "INR 换算工具。按 PT 与 ISI 计算国际标准化比值，用于抗凝监测强度换算；剂量由医师定。",
        "feats": "<li>PT-INR 换算</li><li>跨试剂可比</li><li>目标区间提示</li>",
        "scenes": "<li>房颤抗凝随访</li><li>跨实验室比对</li><li>教学演示 ISI 影响</li>",
    },
    "convert-39": {
        "intro": "约 39 类检验单位换算工具。跨报告与文献统一单位；纯换算，不涉及诊断。",
        "feats": "<li>mmol/L↔mg/dL 等</li><li>物质系数自动选</li><li>批量换算</li>",
        "scenes": "<li>外文文献对照</li><li>跨仪器趋势</li><li>论文单位校对</li>",
    },
    "convert-glucose-1": {
        "intro": "血糖 mg/dL↔mmol/L 换算工具。用于跨系统与报告统一；纯换算。",
        "feats": "<li>双向换算</li><li>诊断切点对照</li><li>即时显示</li>",
        "scenes": "<li>进口血糖仪对照</li><li>外文指南阈值</li><li>糖尿病随访</li>",
    },
    "csf-analysis": {
        "intro": "脑脊液常规对照工具。按压力/细胞/蛋白/糖氯区间提示常见模式；仅供复核。",
        "feats": "<li>多参数区间对照</li><li>模式提示</li><li>参考说明</li>",
        "scenes": "<li>脑膜炎鉴别</li><li>术后复查</li><li>教学演示 CSF 特征</li>",
    },
    "electrophoresis-analysis": {
        "intro": "血清蛋白电泳区带分析工具。计算各带百分比并提示低白蛋白/单克隆增高；不替代血液科诊断。",
        "feats": "<li>五带百分比计算</li><li>M 蛋白提示</li><li>绝对浓度换算</li>",
        "scenes": "<li>肝肾病随访</li><li>骨髓瘤筛查</li><li>教学演示图谱</li>",
    },
    "flow-cytometry-ratio": {
        "intro": "流式细胞术 CD4/CD8 比值与淋巴细胞亚群计算器。输入各亚群百分比或绝对计数，计算 CD4/CD8 比值并对照参考范围，辅助免疫状态评估；结果仅供复核，不替代专科诊断。",
        "feats": "<li>CD4/CD8 比值自动计算</li><li>亚群百分比与绝对计数对照</li><li>参考范围高亮提示</li>",
        "scenes": "<li>HIV 随访免疫监测</li><li>淋巴细胞亚群评估</li><li>教学演示流式设门逻辑</li>",
    },
    "hba1c-converter": {
        "intro": "HbA1c NGSP%↔IFCC mmol/mol 换算工具。便于跨报告与指南对照；纯换算。",
        "feats": "<li>双单位换算</li><li>管理目标对照</li><li>即时显示</li>",
        "scenes": "<li>国内外报告对照</li><li>管理目标统一</li><li>教学演示关系</li>",
    },
    "mic-breakpoint": {
        "intro": "微生物药敏 MIC 折点对照器。输入菌种、药物与测得 MIC，按 CLSI/EUCAST 标准判读敏感(S)/中介(I)/耐药(R)；仅供复核，用药由感染科与药师决定。",
        "feats": "<li>CLSI/EUCAST 折点对照</li><li>S·I·R 自动判读</li><li>多标准差异提示</li>",
        "scenes": "<li>药敏报告复核</li><li>不同标准折点比对</li><li>教学演示 PK/PD 折点含义</li>",
    },
    "parasite-egg-id": {
        "intro": "寄生虫虫卵形态对照工具。结构化提示常见虫卵鉴别要点；确诊由寄生虫室判读。",
        "feats": "<li>形态要点对照</li><li>易混淆项提示</li><li>图谱复习</li>",
        "scenes": "<li>粪检复习</li><li>教学演示虫卵差异</li><li>筛查前温习</li>",
    },
    "pcr-ct-interpretation": {
        "intro": "qPCR Ct 值解释工具。说明 Ct 与模板量关系并对照定性阈值，辅助核酸检测报告理解；仅供复核。",
        "feats": "<li>Ct 含义解释</li><li>阴阳性判读</li><li>灰区提示</li>",
        "scenes": "<li>核酸报告理解</li><li>灰区复测建议</li><li>教学演示扩增</li>",
    },
    "semen-analysis": {
        "intro": "精液参数对照工具。按 WHO 参考下限对量/浓度/活力/形态逐项比对，辅助男科报告初读；仅供复核。",
        "feats": "<li>WHO 下限对照</li><li>越界项高亮</li><li>前后复查对比</li>",
        "scenes": "<li>不育初诊初读</li><li>复查趋势</li><li>教学演示下限</li>",
    },
    "stool-occult-blood": {
        "intro": "粪便潜血结果解释工具。说明 gFOBT/FIT 含义与适用场景；阳性需结肠镜确认，不替代内镜。",
        "feats": "<li>结果含义说明</li><li>干扰因素提示</li><li>下一步建议</li>",
        "scenes": "<li>体检 FIT 理解</li><li>干扰说明</li><li>教学演示筛查</li>",
    },
    "thyroid-function-model": {
        "intro": "甲功模式判断工具。按 TSH/FT4 组合判型，辅助报告初读；不替代内分泌诊断。",
        "feats": "<li>TSH/FT4 组合判读</li><li>亚临床提示</li><li>孕期区间提示</li>",
        "scenes": "<li>体检甲功初读</li><li>妊娠甲功</li><li>教学演示反馈轴</li>",
    },
    "tumor-marker-doubling": {
        "intro": "肿瘤标志物倍增时间计算工具。按序列浓度算 PSADT 等，辅助随访趋势理解；不替代影像与病理。",
        "feats": "<li>倍增时间计算</li><li>趋势量化</li><li>公式说明</li>",
        "scenes": "<li>PSA 随访</li><li>标志物升高量化</li><li>教学演示指数增长</li>",
    },
    "urinalysis-interpretation": {
        "intro": "尿常规条目解释工具。结构化解读干化学与镜检并组合提示，辅助报告初读；仅供复核。",
        "feats": "<li>条目结构化解释</li><li>组合模式提示</li><li>参考说明</li>",
        "scenes": "<li>体检异常初读</li><li>尿感初筛</li><li>教学演示关联</li>",
    },
    "urine-sediment-atlas": {
        "intro": "尿沉渣有形成分图谱工具。对照红细胞/白细胞/管型/结晶形态与提示，辅助镜检复习；判读由检验师确认。",
        "feats": "<li>有形成分对照</li><li>肾实质提示</li><li>结晶类型说明</li>",
        "scenes": "<li>沉渣镜检复习</li><li>管型类型提示</li><li>教学演示结晶</li>",
    },
    "vaginal-discharge-grading": {
        "intro": "阴道分泌物分级工具。按 Nugent/AV 评分计算分级，辅助报告理解；诊断与用药由妇科医师决定。",
        "feats": "<li>Nugent/AV 评分</li><li>分级计算</li><li>参考说明</li>",
        "scenes": "<li>白带常规判读</li><li>AV 评分理解</li><li>教学演示评分</li>",
    },
}

OPT_MAP = {
    "flow-cytometry-ratio": "流式 CD4/CD8 比值计算适用于 HIV 随访免疫监测、淋巴细胞亚群评估与教学演示，辅助理解免疫状态趋势。",
    "mic-breakpoint": "MIC 折点对照适用于微生物药敏报告复核、CLSI 与 EUCAST 标准比对，辅助理解敏感/耐药判读。",
}
OPT_JUNK = "工作与生活中的相关计算与查询。"


def clean_fd(name, real):
    path = os.path.join(TOOLS, name + ".html")
    s = open(path, encoding="utf-8").read()
    new = re.sub(r'<p class="formula-desc">.*?</p>',
                 '<p class="formula-desc">' + real + '</p>', s, flags=re.S)
    c = 1 if new != s else 0
    if not DRY and c:
        open(path, "w", encoding="utf-8").write(new)
    return c


def clean_intro(name, d):
    path = os.path.join(TOOLS, name + ".html")
    s = open(path, encoding="utf-8").read()
    new = re.sub(r'(工具简介</h4>\s*<p>).*?(</p>)',
                 lambda m: m.group(1) + d["intro"] + m.group(2), s, flags=re.S)
    new = re.sub(r'(<ul class="intro-features">).*?(</ul>)',
                 lambda m: m.group(1) + d["feats"] + m.group(2), new, flags=re.S)
    new = re.sub(r'(<ul class="intro-scenes">).*?(</ul>)',
                 lambda m: m.group(1) + d["scenes"] + m.group(2), new, flags=re.S)
    c = 1 if new != s else 0
    if not DRY and c:
        open(path, "w", encoding="utf-8").write(new)
    return c


def clean_opt(name, real):
    path = os.path.join(TOOLS, name + ".html")
    s = open(path, encoding="utf-8").read()
    if OPT_JUNK not in s:
        return 0
    new = s.replace(OPT_JUNK, real)
    c = 1 if new != s else 0
    if not DRY and c:
        open(path, "w", encoding="utf-8").write(new)
    return c


RT_SUFFIX = " - 医疗专业领域的在线工具"


def clean_rtname(name):
    path = os.path.join(TOOLS, name + ".html")
    s = open(path, encoding="utf-8").read()
    new = re.sub(r'<span class="rt-name">([^<]*?)' + re.escape(RT_SUFFIX) + r'</span>',
                 r'<span class="rt-name">\1</span>', s)
    c = 1 if new != s else 0
    if not DRY and c:
        open(path, "w", encoding="utf-8").write(new)
    return c


def main():
    total = 0
    for name, real in FD_MAP.items():
        c = clean_fd(name, real)
        if c:
            total += c
            print(("DRY " if DRY else "") + "formula-desc", name)
    for name, d in INTRO_MAP.items():
        c = clean_intro(name, d)
        if c:
            total += c
            print(("DRY " if DRY else "") + "intro", name)
    for name, real in OPT_MAP.items():
        c = clean_opt(name, real)
        if c:
            total += c
            print(("DRY " if DRY else "") + "opt", name)
    for name in INTRO_MAP:
        c = clean_rtname(name)
        if c:
            total += c
            print(("DRY " if DRY else "") + "rtname", name)
    print(("DRY 预览 " if DRY else "正式 ") + "完成，总替换:", total)


if __name__ == "__main__":
    main()
