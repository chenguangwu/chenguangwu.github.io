# -*- coding: utf-8 -*-
"""清理 clinical-nursing 26 工具页硬编码套话：
1) formula-desc 11 页（四变体：校验×3/财务×2/工程×1/速查×5）→ 真实护理说明（meta 已真实无回灌）
2) tool-intro 三段块 25 页全覆盖：23 页替换套话（医学/护理/隐私），2 页(cycle-7/reminder-time-1)缺失块→插入真实三段
3) opt-guide <p> 套话 3 页(cycle-7/iv-drip-rate/pain-nrs)→真实护理场景
去诊断化，仅供护理记录参考。
"""
import re, os, sys, json

TOOLS = "tools/clinical-nursing"
DRY = "--dry" in sys.argv
DD = json.load(open("i18n/tools/content_deepdive.json", encoding="utf-8"))

# 1) formula-desc 真实化（按页精确替换块内文本）
FD_MAP = {
    "assessor-pressure-risk": "本工具按临床护理评估量表逐项计算手术体位受压点风险分值，结果仅供参考，不替代床旁专业评估。",
    "assessor-rater-risk": "本工具按 Morse 跌倒评估量表逐项计算风险分值，结果仅供参考，以护士床旁评估与签字为准。",
    "calc-rater-risk": "本工具按 Braden 压疮评分量表自动计算六维度总分与风险分层，结果仅供参考，以床旁评估为准。",
    "braden-score": "本工具按 Braden 护理评分量表逐项计分并分层，结果仅供参考，以护士床旁评估与签字为准。",
    "morse-score": "本工具按 Morse 护理评分量表逐项计分并分层，结果仅供参考，以护士床旁评估与签字为准。",
    "chest-compression-depth": "本工具按 AHA 心肺复苏指南给出年龄别按压深度与频率参考范围，结果仅供参考，以抢救团队指挥与反馈设备为准。",
    "fall-emergency-flow": "本工具依据临床护理规范与公开应急流程整理，供快速查阅参考，具体处置以医嘱与床旁判断为准。",
    "pain-nrs": "本工具依据疼痛评估规范整理 NRS 评分参考，供护理记录使用，用药以医嘱为准。",
    "restraint-check": "本工具依据约束护理规范整理松紧度评估参考，供床旁核查使用，以每班评估记录为准。",
    "suction-pressure": "本工具依据气道护理规范给出年龄别吸痰负压安全范围，供参数设定参考，以设备调节与医嘱为准。",
    "surgical-position-risk": "本工具依据手术体位护理规范整理受压点风险评估参考，供巡回护士核查使用，以床旁观察为准。",
}

# 2) tool-intro 真实三段（25 页全覆盖）
INTRO_MAP = {
    "assessor-pressure-risk": {
        "intro": "手术体位摆放后评估骶尾、足跟等骨突受压风险，辅助巡回护士制定减压与体位垫方案。",
        "feats": ["受压点风险分级", "手术时长分段标注", "BMI/营养状态联动评级"],
        "scenes": ["俯卧位或侧卧位术前初评", "长时间固定体位术中减压提醒", "肥胖或低蛋白患者上调风险"],
    },
    "assessor-rater-risk": {
        "intro": "按 Morse 量表六维度量化住院患者跌倒风险，辅助分级陪护与防跌倒管理。",
        "feats": ["六维度逐项评分", "自动风险分层（低/中/高）", "高危标识提示"],
        "scenes": ["新入院 24h 内评估", "术后下床活动前复评", "镇静或降压用药后复评"],
    },
    "bag-valve-mask": {
        "intro": "按患者年龄设定球囊面罩人工呼吸频率与潮气量参考，辅助 CPR 通气参数核对。",
        "feats": ["年龄别频率区间", "潮气量轻柔提示", "30:2 比例适配"],
        "scenes": ["成人 CPR 通气 10–12 次/分", "婴幼儿小潮气量防胃胀气", "有自主节律辅助通气"],
    },
    "barthel-index": {
        "intro": "按 Barthel 十项 ADL 评分量化自理能力，辅助康复进展与照护等级判定。",
        "feats": ["十项条目评分", "总分 0–100", "依赖等级划分"],
        "scenes": ["卒中康复双周复评", "骨科术后转移与行走评分", "长护险等级申请"],
    },
    "braden-score": {
        "intro": "按 Braden 六维度识别压力性损伤风险，指导翻身频次与减压床垫使用。",
        "feats": ["六维度评分", "风险分层（≤18 高危）", "动态复评提醒"],
        "scenes": ["卧床或 ICU 入院 24h 评估", "失禁或制动患者复评", "营养异常上调风险"],
    },
    "calc-rater-risk": {
        "intro": "Braden 评分自动化计算入口，输入六维度即得总分与分层，便于床旁快速建档。",
        "feats": ["六维度输入", "即时总分与分层", "批量录入高危名单"],
        "scenes": ["夜班交接批量建档", "病情变化时复算", "教学演示维度权重"],
    },
    "chest-compression-depth": {
        "intro": "按年龄给出 CPR 胸外按压深度参考，辅助按压质量核查与培训考核。",
        "feats": ["年龄别深度区间", "频率提示", "反馈仪阈值校准"],
        "scenes": ["成人 5–6 cm", "儿童约 5 cm、婴儿约 4 cm", "反馈式 CPR 传感器校准"],
    },
    "cold-compress-timer": {
        "intro": "按部位与皮肤耐受设定冷敷时长与间隔，预防冻伤并规范急性期消肿。",
        "feats": ["单次时长设定", "间隔提醒", "皮肤敏感自动缩短"],
        "scenes": ["扭伤急性期 15–20 min/次", "术后垫纱布隔离皮肤", "小儿或糖尿病加强巡视"],
    },
    "convert-flow-concentration": {
        "intro": "按吸氧装置与流量估算 FiO2，辅助氧疗处方核对与方案选择。",
        "feats": ["鼻导管 FiO2≈21+4×流量", "文丘里/面罩标称 FiO2", "HFNC 参数校准"],
        "scenes": ["鼻导管 1–6 L/min 估算", "文丘里面罩选 FiO2", "目标 SpO2 回推流量"],
    },
    "cvc-maintenance": {
        "intro": "按导管类型与封管液给出冲管封管剂量频次，规范静脉治疗维护。",
        "feats": ["脉冲式冲管剂量", "肝素或生理盐水封管", "配伍沉淀预防"],
        "scenes": ["输液前后 10 ml 冲管", "间歇期正压封管", "输血或脂肪乳后增量"],
    },
    "cycle-7": {
        "intro": "按保护性约束规范给出每班松解与观察周期，平衡安全与末梢循环。",
        "feats": ["每 2h 松解提醒", "末梢循环观察", "指征解除提示"],
        "scenes": ["肢体约束每 2h 松解 15 min", "夜间按躁动调整频次", "指征解除即撤除"],
    },
    "fall-emergency-flow": {
        "intro": "模拟跌倒或坠床后应急处置步骤，辅助培训与预案核对。",
        "feats": ["意识—制动—伤情流程", "上报提示", "记录模板"],
        "scenes": ["倒地先评意识禁盲扶", "疑骨折原位制动", "24h 内上报不良事件"],
    },
    "gastric-tube-depth": {
        "intro": "按 NEX 体表标志估算成人胃管置入深度，辅助鼻饲置管定位。",
        "feats": ["NEX 距离估算", "置管后验证提示", "小儿按身长"],
        "scenes": ["成人 45–55 cm", "回抽 pH 或听气过水声验证", "小儿 X 线定深"],
    },
    "generator-pressure": {
        "intro": "按 NPUAP 分期生成压力性损伤描述文本，辅助护理记录。",
        "feats": ["1–4 期描述模板", "不可分期/深部标注", "结构化输出"],
        "scenes": ["1–2 期皮肤完整性描述", "3–4 期组织丢失描述", "深部损伤按覆盖物标注"],
    },
    "iv-drip-rate": {
        "intro": "按总量时间与滴系数换算滴速，辅助重力输液与微泵参数设定。",
        "feats": ["滴速换算公式", "限速反算", "控速药品上限"],
        "scenes": ["常规 500 ml/6h 滴速", "老年或心肾限速", "输血或钾盐控速"],
    },
    "morse-score": {
        "intro": "Morse 跌倒评估量表逐项评分入口，六维度累加分层，便于床旁建档。",
        "feats": ["六项逐项录入", "总分与分层", "临界值提示"],
        "scenes": ["入院 24h 内评估", "用药变更后复评", "高危者每周复评"],
    },
    "ostomy-bag-timing": {
        "intro": "按造口类型与渗漏给出更换周期，规范肠造口居家护理。",
        "feats": ["结肠/回肠周期差异", "渗漏即刻换", "皮肤保护提示"],
        "scenes": ["结肠造口 3–7 天", "回肠造口 2–4 天", "术后观察造口血运"],
    },
    "oxygen-concentration": {
        "intro": "按装置与流量计算 FiO2 参考，辅助氧疗方案核对与 SpO2 管理。",
        "feats": ["鼻导管 FiO2 估算", "面罩标称 FiO2", "目标 SpO2 回推"],
        "scenes": ["鼻导管 1–6 L/min 估算", "面罩选 FiO2", "长时高流量湿化监测"],
    },
    "pain-nrs": {
        "intro": "按 NRS 0–10 结合面部表情量化疼痛，辅助动态评估与用药反馈。",
        "feats": ["0–10 评分", "静息/活动双评", "面部表情辅助"],
        "scenes": ["术后每 4–6h 双评", "癌痛暴发与基础分记", "语言障碍用表情量表"],
    },
    "pressure-injury-description": {
        "intro": "生成压力性损伤分期描述规范文本，便于护理文书与交接。",
        "feats": ["分期描述模板", "坏死/潜行范围", "动态改期"],
        "scenes": ["1–2 期完整性描述", "3–4 期组织描述", "不可分期标注"],
    },
    "reminder-time-1": {
        "intro": "冷敷计时提醒，按部位设定单次时长与间隔，预防冻伤。",
        "feats": ["单次时长设定", "间隔提醒", "感觉迟钝者缩短"],
        "scenes": ["急性期 15–20 min/次", "术后垫纱布隔离", "感觉迟钝加强巡视"],
    },
    "restraint-check": {
        "intro": "按一指法则评估约束带松紧，保障末梢循环并防挣脱。",
        "feats": ["一指可伸入判定", "每班循环检查", "小儿或水肿调整"],
        "scenes": ["肢体约束一指为度", "查末梢脉搏与皮温", "过紧发绀立即松解"],
    },
    "restraint-duration": {
        "intro": "给出约束累计时长与每班松解周期，规范时限管理。",
        "feats": ["累计时长统计", "每 2h 松解", "每日复评续开"],
        "scenes": ["每 2h 松解 15 min", "每日医嘱续开", "指征解除即撤"],
    },
    "suction-pressure": {
        "intro": "按年龄给出吸痰负压安全范围，辅助气道管理参数设定。",
        "feats": ["年龄别范围", "密闭式校准", "单次时限"],
        "scenes": ["成人 100–150 mmHg", "儿童 80–100 mmHg", "痰液黏稠调湿化≤15s"],
    },
    "surgical-position-risk": {
        "intro": "手术体位摆放后受压点风险初评，指导减压垫与术中减压。",
        "feats": ["体位别受压点", "时长风险标注", "小儿上调"],
        "scenes": ["俯卧位评颜面与膝", "侧卧位评耳廓与大转子", "截石位评腘窝"],
    },
    "tracheostomy-dressing": {
        "intro": "按分泌物量给出气切换药间隔，规范气道护理。",
        "feats": ["分泌物量分级", "渗湿即刻换", "周围皮肤观察"],
        "scenes": ["分泌物多每日 1–2 次", "敷料污染即刻换", "观察造口周围皮肤"],
    },
}

# 3) opt-guide <p> 套话替换
OPT_MAP = {
    "cycle-7": "适用于保护性约束患者的每班松解与末梢循环观察安排，按规范设定松解周期。",
    "iv-drip-rate": "适用于住院输液患者的滴速设定与控速核对，结合医嘱与微泵参数执行。",
    "pain-nrs": "适用于术后、癌痛等患者的疼痛动态评估记录，结合静息与活动双评指导干预。",
}
OPT_JUNK = "工作与生活中的相关计算与查询"

# 缺失 tool-intro 块的两页真实工具名（header「关于「工具名」」用）
MISSING_NAMES = {
    "cycle-7": "约束用具使用时长松解周期",
    "reminder-time-1": "冰袋冷敷时间提醒",
}



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
    intro = d["intro"]
    feats = "".join("<li>" + x + "</li>" for x in d["feats"])
    scenes = "".join("<li>" + x + "</li>" for x in d["scenes"])
    total = 0
    if "功能特点</h4>" in s:
        def r1(m): return m.group(1) + intro + m.group(2)
        def r2(m): return m.group(1) + feats + m.group(2)
        def r3(m): return m.group(1) + scenes + m.group(2)
        new = re.sub(r'(工具简介</h4>\s*<p>).*?(</p>)', r1, s, flags=re.S)
        new = re.sub(r'(<ul class="intro-features">).*?(</ul>)', r2, new, flags=re.S)
        new = re.sub(r'(<ul class="intro-scenes">).*?(</ul>)', r3, new, flags=re.S)
        c = 1 if new != s else 0
        if not DRY and c:
            open(path, "w", encoding="utf-8").write(new)
        return c
    else:
        # 缺失块：插入完整 tool-intro 手风琴到 </body> 前（与 23 页结构/位置完全一致，
        # 位于 deep-dive 区块之后，避免被 _build.py 的 _DEEP_DIVE_BLOCK_RE 整体替换吃掉）。
        _title = MISSING_NAMES.get(name, name)
        folding = ('<script>\n'
                   '// tool-intro折叠交互\n'
                   'document.addEventListener(\'DOMContentLoaded\',function(){\n'
                   '  var headers=document.querySelectorAll(\'.tool-intro-header\');\n'
                   '  headers.forEach(function(h){\n'
                   '    h.addEventListener(\'click\',function(){\n'
                   '      this.parentElement.classList.toggle(\'open\');\n'
                   '    });\n'
                   '  });\n'
                   '});\n'
                   '</script>')
        block = ('<div class="tool-intro open" id="toolIntro">\n'
                 '  <div class="tool-intro-header">\n'
                 '    <span class="intro-icon-wrap"><span class="intro-icon">📖</span>关于「' + _title + '」</span>\n'
                 '    <span class="arrow">▼</span>\n'
                 '  </div>\n'
                 '  <div class="tool-intro-body">\n'
                 '    <h4><span class="h4-icon">📝</span>工具简介</h4>\n'
                 '    <p>' + intro + '</p>\n'
                 '    <h4><span class="h4-icon">✨</span>功能特点</h4>\n'
                 '    <ul class="intro-features">' + feats + '</ul>\n'
                 '    <h4><span class="h4-icon">🎯</span>使用场景</h4>\n'
                 '    <ul class="intro-scenes">' + scenes + '</ul>\n'
                 '  </div>\n'
                 '</div>\n'
                 '<!-- /SEO 介绍区块 -->\n\n' + folding)
        new = s.replace('</body>', block + '\n</body>', 1)
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


total = 0
for name, real in FD_MAP.items():
    c = clean_fd(name, real)
    if c:
        total += c
        print((("DRY " if DRY else "") + "fd " + name))
for name, d in INTRO_MAP.items():
    c = clean_intro(name, d)
    if c:
        total += c
        print((("DRY " if DRY else "") + "intro " + name + ("(insert)" if "功能特点</h4>" not in open(os.path.join(TOOLS, name + ".html"), encoding="utf-8").read() else "")))
for name, real in OPT_MAP.items():
    c = clean_opt(name, real)
    if c:
        total += c
        print((("DRY " if DRY else "") + "opt " + name))
print("total changed:", total)
