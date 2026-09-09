#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""kinematics 分类 28 工具 deep-dive 真实化：替换第六型「快速复核」泛化模板。
范式对齐前述 apply 脚本：title/scenarios/examples/faqs 四字段覆盖，json.dump(indent=1) 保持仓库规范。
检测词（六型+弱模板）全规避。kinematics 为经典运动学计算类，算例基于真实公式与默认数字。
用法：--dry 仅校验；默认 --apply 写入 JSON。
"""
import json, re, sys

PATH = "i18n/tools/content_deepdive.json"

DATA = {
    "kinematics/angular-accel": {
        "title": "角加速度（Δω/Δt）",
        "scenarios": [
            "转盘转速变化快慢，求角加速度。",
            "电机启停过程分析。",
        ],
        "examples": [
            {"title": "Δω=10、Δt=2", "body": "α = 10/2 = 5 rad/s²。即 2 秒内角速度增 10 rad/s，角加速度 5 rad/s²。"},
        ],
        "faqs": [
            {"q": "和线加速度关系？", "a": "切向加速度 a_t = α·r，同一刚体上半径越大切向加速度越大；角加速度是转动侧的对应量。"},
        ],
    },
    "kinematics/angular-displacement": {
        "title": "角位移（ω₀t + ½αt²）",
        "scenarios": [
            "匀角加速下求转过角度。",
            "转台/飞轮转过弧度估算。",
        ],
        "examples": [
            {"title": "ω₀=2、α=1、t=3", "body": "θ = 2×3 + 0.5×1×3² = 6 + 4.5 = 10.5 rad。即 3 秒转过 10.5 弧度（约 1.67 圈）。"},
        ],
        "faqs": [
            {"q": "弧度怎么换圈数？", "a": "1 圈 = 2π rad ≈ 6.283 rad；10.5 rad ÷ 6.283 ≈ 1.67 圈。"},
        ],
    },
    "kinematics/angular-final-velocity": {
        "title": "末角速度（ω₀ + αt）",
        "scenarios": [
            "匀角加速求某时刻角速度。",
            "电机加速到目标转速。",
        ],
        "examples": [
            {"title": "ω₀=2、α=1、t=3", "body": "ω = 2 + 1×3 = 5 rad/s。即 3 秒末角速度 5 rad/s。"},
        ],
        "faqs": [
            {"q": "和频率怎么换？", "a": "f = ω/(2π)；5 rad/s 对应约 0.796 Hz，即每秒约 0.8 圈。"},
        ],
    },
    "kinematics/angular-velocity": {
        "title": "角速度（v/r）",
        "scenarios": [
            "由线速度与半径求角速度。",
            "车轮/转盘转速换算。",
        ],
        "examples": [
            {"title": "v=10、r=2", "body": "ω = 10/2 = 5 rad/s。即线速 10 m/s、半径 2 m 时角速度 5 rad/s。"},
        ],
        "faqs": [
            {"q": "rpm 怎么转 rad/s？", "a": "ω = 2πn/60；3000 rpm = 2π×3000/60 ≈ 314.16 rad/s。"},
        ],
    },
    "kinematics/avg-acceleration": {
        "title": "平均加速度（Δv/Δt）",
        "scenarios": [
            "速度变化除以时间得平均加速度。",
            "车辆加减速过程评估。",
        ],
        "examples": [
            {"title": "20→10、2s", "body": "a = (10−20)/2 = −5 m/s²。即 2 秒内减速 10 m/s，平均加速度 −5 m/s²（负号表示减速）。"},
        ],
        "faqs": [
            {"q": "负号什么意思？", "a": "方向与初速相反，表示减速；大小 5 m/s² 是减速度。"},
        ],
    },
    "kinematics/avg-velocity": {
        "title": "平均速度（Δx/Δt）",
        "scenarios": [
            "位移除以时间得平均速度。",
            "行程整体快慢评估。",
        ],
        "examples": [
            {"title": "Δx=100、Δt=10", "body": "v̄ = 100/10 = 10 m/s。即 10 秒走 100 米，平均 10 m/s（不反映中途快慢）。"},
        ],
        "faqs": [
            {"q": "平均速度和瞬时速度？", "a": "平均是总位移/总时间；瞬时是某时刻速率。变速运动时两者常不同。"},
        ],
    },
    "kinematics/centripetal-accel": {
        "title": "向心加速度（v²/r）",
        "scenarios": [
            "圆周运动指向圆心的加速度。",
            "弯道设计限速分析。",
        ],
        "examples": [
            {"title": "v=20、r=50", "body": "a = 20²/50 = 400/50 = 8 m/s²。即 20 m/s 过半径 50 m 弯，向心加速度 8 m/s²。"},
        ],
        "faqs": [
            {"q": "速度翻倍影响多大？", "a": "向心加速度与 v² 成正比；速度翻倍加速度变 4 倍，故弯道限速很关键。"},
        ],
    },
    "kinematics/centripetal-force": {
        "title": "向心力（mv²/r）",
        "scenarios": [
            "维持圆周运动所需合力。",
            "车辆过弯摩擦力是否够。",
        ],
        "examples": [
            {"title": "m=1000、v=20、r=50", "body": "F = 1000×20²/50 = 8000 N = 8 kN。即需 8 kN 向心力，由摩擦或轨道提供。"},
        ],
        "faqs": [
            {"q": "向心力是谁给的？", "a": "不是额外力，是合力的效果名；由重力/支持/摩擦力或拉力充当，指向圆心。"},
        ],
    },
    "kinematics/displacement-accel": {
        "title": "位移公式（v₀t + ½at²）",
        "scenarios": [
            "匀加速下求位移。",
            "起步加速距离估算。",
        ],
        "examples": [
            {"title": "v₀=10、a=2、t=5", "body": "x = 10×5 + 0.5×2×25 = 50 + 25 = 75 m。即 5 秒匀加速走 75 米。"},
        ],
        "faqs": [
            {"q": "和 v̄t 一致吗？", "a": "匀加速时平均速 = (v₀+v)/2，位移 = v̄×t，与该式等价；非匀加速不可用。"},
        ],
    },
    "kinematics/displacement-va": {
        "title": "位移（速度平方差/2a）",
        "scenarios": [
            "不知时间，用起末速度与加速度求位移。",
            "刹车距离（已知初末速）估算。",
        ],
        "examples": [
            {"title": "v=20、v₀=10、a=5", "body": "s = (20²−10²)/(2×5) = (400−100)/10 = 30 m。即速度 10→20 匀加速走 30 米。"},
        ],
        "faqs": [
            {"q": "减速度怎么用？", "a": "a 取负值即可；如 20→10、a=−5，s=(100−400)/(−10)=30 m，距离为正。"},
        ],
    },
    "kinematics/final-velocity-accel": {
        "title": "末速度（v₀ + at）",
        "scenarios": [
            "匀加速求某时刻速度。",
            "自由落体末速（v₀=0）。",
        ],
        "examples": [
            {"title": "自由落体 5s", "body": "v = 0 + 9.8×5 = 49 m/s。即自由下落 5 秒速度约 49 m/s（忽略空气阻力）。"},
        ],
        "faqs": [
            {"q": "空气阻力影响？", "a": "理想模型忽略；实际高速时阻力显著，末速趋于终端速度，本式仅适用低速/短程。"},
        ],
    },
    "kinematics/free-fall-time": {
        "title": "自由落体时间（√(2h/g)）",
        "scenarios": [
            "已知高度求下落时间。",
            "掉落物到达时间估算。",
        ],
        "examples": [
            {"title": "h=100、g=9.8", "body": "t = √(2×100/9.8) = √20.41 ≈ 4.52 s。即百米高自由下落约 4.5 秒触地。"},
        ],
        "faqs": [
            {"q": "和质量有关吗？", "a": "理想自由落体无关（伽利略）；实际受空气阻力大物体略慢。"},
        ],
    },
    "kinematics/freq-from-omega": {
        "title": "由角速度求频率（f=ω/2π）",
        "scenarios": [
            "角速度转每秒圈数。",
            "旋转设备频率换算。",
        ],
        "examples": [
            {"title": "ω=6.283", "body": "f = 6.283/(2π) = 6.283/6.283 = 1 Hz。即每秒转 1 圈。"},
        ],
        "faqs": [
            {"q": "和周期关系？", "a": "f = 1/T；频率是单位时间圈数，周期是一圈耗时，互为倒数。"},
        ],
    },
    "kinematics/height-fall-distance": {
        "title": "下落距离（½gt²）",
        "scenarios": [
            "已知下落时间求高度。",
            "自由落体高度反推。",
        ],
        "examples": [
            {"title": "t=2、g=9.81", "body": "h = 0.5×9.81×2² = 0.5×9.81×4 = 19.62 m。即下落 2 秒约 19.6 米。"},
        ],
        "faqs": [
            {"q": "和 free-fall-time 互逆？", "a": "是。t=√(2h/g) 与 h=½gt² 互为变形，已知其一可求另一。"},
        ],
    },
    "kinematics/period-from-omega": {
        "title": "由角速度求周期（T=2π/ω）",
        "scenarios": [
            "角速度转一圈耗时。",
            "旋转周期计算。",
        ],
        "examples": [
            {"title": "ω=6.283", "body": "T = 2π/6.283 = 1 s。即角速度 6.283 rad/s 时每圈 1 秒。"},
        ],
        "faqs": [
            {"q": "和频率？", "a": "T=1/f；周期 1 秒即频率 1 Hz，两者一致。"},
        ],
    },
    "kinematics/projectile-max-height": {
        "title": "抛射最大高度（v²sin²θ/2g）",
        "scenarios": [
            "斜抛顶点高度。",
            "喷泉/投掷最高点估算。",
        ],
        "examples": [
            {"title": "v=30、θ=60°、g=9.8", "body": "H = 30²×sin²60/(2×9.8) = 900×0.75/19.6 ≈ 34.4 m。即 60° 抛 30 m/s 最高约 34.4 米。"},
        ],
        "faqs": [
            {"q": "什么角度最高？", "a": "垂直抛(90°)最高；但射程在 45° 最大，高度与射程目标不同取角不同。"},
        ],
    },
    "kinematics/projectile-range": {
        "title": "抛射射程（v²sin2θ/g）",
        "scenarios": [
            "斜抛水平射程（同高落地）。",
            "投掷/炮弹距离估算。",
        ],
        "examples": [
            {"title": "v=30、θ=45°、g=9.8", "body": "R = 30²×sin90/9.8 = 900/9.8 ≈ 91.84 m。即 45° 抛 30 m/s 射程约 91.8 米（此角最大）。"},
        ],
        "faqs": [
            {"q": "为什么 45° 最远？", "a": "sin2θ 在 θ=45° 取最大 1；同等初速下 45° 射程最大，高低角互补(如 30°/60°)射程相同。"},
        ],
    },
    "kinematics/projectile-time-flight": {
        "title": "抛射飞行时间（2v·sinθ/g）",
        "scenarios": [
            "斜抛从发射到落地总时长。",
            "投掷滞空时间估算。",
        ],
        "examples": [
            {"title": "v=30、θ=45°、g=9.8", "body": "T = 2×30×sin45/9.8 = 60×0.707/9.8 ≈ 4.33 s。即空中约 4.3 秒。"},
        ],
        "faqs": [
            {"q": "落点和发射点不同高？", "a": "本式假设同高落地；若落地更低需解二次方程，时间更长。"},
        ],
    },
    "kinematics/projectile-velocity-components": {
        "title": "抛射速度分量（v_x=v·cosθ, v_y=v·sinθ）",
        "scenarios": [
            "分解初速为水平竖直分量。",
            "弹道分析基础。",
        ],
        "examples": [
            {"title": "v=20、θ=30°", "body": "v_x = 20×cos30 = 17.32 m/s，v_y = 20×sin30 = 10 m/s。水平匀速、竖直受重力。"},
        ],
        "faqs": [
            {"q": "分量为什么分开算？", "a": "水平不受力匀速、竖直受重力匀变，拆开后各自独立再用运动学公式，是弹道标准做法。"},
        ],
    },
    "kinematics/relative-velocity-1d": {
        "title": "一维相对速度（v₁−v₂）",
        "scenarios": [
            "同直线两物体相对速度。",
            "超车/追及分析。",
        ],
        "examples": [
            {"title": "v₁=30、v₂=20（同向）", "body": "v_r = 30−20 = 10 m/s。即前者相对后者以 10 m/s 靠近/拉开。"},
        ],
        "faqs": [
            {"q": "反向怎么算？", "a": "取同向为正，反向则一正一负，v_r = v₁−v₂ 仍成立；结果为负表示反向远离。"},
        ],
    },
    "kinematics/relativistic-velocity-add": {
        "title": "相对论速度叠加",
        "scenarios": [
            "接近光速时速度不能简单相加。",
            "亚光速运动合成。",
        ],
        "examples": [
            {"title": "0.6c + 0.6c", "body": "u = (0.6c+0.6c)/(1+0.6×0.6) = 1.2c/1.36 ≈ 0.882c。即两 0.6c 叠加仍小于 c，不超光速。"},
        ],
        "faqs": [
            {"q": "为什么不超过 c？", "a": "经典相加得 1.2c 错；相对论分母 1+u′v/c² 修正后结果恒 < c，光速不可超越。"},
        ],
    },
    "kinematics/rpm-to-radps": {
        "title": "转速转角速度（2πn/60）",
        "scenarios": [
            "rpm 转 rad/s 做转动计算。",
            "电机参数换算。",
        ],
        "examples": [
            {"title": "n=3000 rpm", "body": "ω = 2π×3000/60 ≈ 314.16 rad/s。即 3000 转/分约合 314 rad/s。"},
        ],
        "faqs": [
            {"q": "为什么除 60？", "a": "rpm 是每分转数，除以 60 得每秒转数，再乘 2π 得 rad/s。"},
        ],
    },
    "kinematics/stopping-distance": {
        "title": "刹车制动距离（v₀t_r + v₀²/2a）",
        "scenarios": [
            "含反应距离的全程刹停距离。",
            "安全车距评估。",
        ],
        "examples": [
            {"title": "100km/h、反应1s、减速度7", "body": "v₀=27.78 m/s，d = 27.78×1 + 27.78²/(2×7) = 27.78 + 55.1 ≈ 82.9 m。即约 83 米才停。"},
        ],
        "faqs": [
            {"q": "反应距离占比大吗？", "a": "100km/h 下反应 1 秒就走 27.8 米，占全程约 1/3；疲劳/分神会显著拉长，故保持车距。"},
        ],
    },
    "kinematics/stopping-time": {
        "title": "制动时间（v₀/a）",
        "scenarios": [
            "初速除以减速度得刹停时长。",
            "刹车响应评估。",
        ],
        "examples": [
            {"title": "v₀=20、a=5", "body": "t = 20/5 = 4 s。即从 20 m/s 匀减速到停需 4 秒（不含反应时间）。"},
        ],
        "faqs": [
            {"q": "和制动距离关系？", "a": "距离 = v₀t − ½at²，代入 t=v₀/a 得 v₀²/2a，二者由同一运动学导出。"},
        ],
    },
    "kinematics/tangential-accel": {
        "title": "切向加速度（α·r）",
        "scenarios": [
            "转动角加速度对应的切向加速度。",
            "转盘边缘线加速分析。",
        ],
        "examples": [
            {"title": "α=2、r=0.5", "body": "a_t = 2×0.5 = 1 m/s²。即角加速度 2、半径 0.5 m 时边缘切向加速 1 m/s²。"},
        ],
        "faqs": [
            {"q": "还有法向加速度？", "a": "有。法向(向心) a_n=ω²r 改方向、切向 a_t=αr 改大小，总加速度为二者矢量合。"},
        ],
    },
    "kinematics/tangential-velocity": {
        "title": "切向速度（ω·r）",
        "scenarios": [
            "角速度对应的线速度。",
            "转盘边缘速度分布。",
        ],
        "examples": [
            {"title": "ω=10、r=0.5", "body": "v_t = 10×0.5 = 5 m/s。即角速度 10 rad/s、半径 0.5 m 处线速 5 m/s。"},
        ],
        "faqs": [
            {"q": "半径越大越快？", "a": "同角速度下 v_t=ωr，外缘线速更大；这也是转盘外缘离心感更强的原因。"},
        ],
    },
    "kinematics/uniform-displacement": {
        "title": "匀速位移（s=vt）",
        "scenarios": [
            "匀速运动位移。",
            "定速行程估算。",
        ],
        "examples": [
            {"title": "v=5、t=10", "body": "s = 5×10 = 50 m。即 5 m/s 匀速走 10 秒为 50 米。"},
        ],
        "faqs": [
            {"q": "和平均速度关系？", "a": "匀速时瞬时=平均，s=vt 即 v̄t 的特例。"},
        ],
    },
    "kinematics/velocity-squared": {
        "title": "速度位移关系（v²=v₀²+2aΔx）",
        "scenarios": [
            "不知时间，由位移求末速。",
            "自由落体末速（已知高度）。",
        ],
        "examples": [
            {"title": "v₀=0、a=9.8、Δx=100", "body": "v = √(0+2×9.8×100) = √1960 ≈ 44.27 m/s。即自由下落 100 米末速约 44.3 m/s。"},
        ],
        "faqs": [
            {"q": "和 free-fall-time 一致？", "a": "一致：由 h=½gt² 与 v=gt 消去 t 即 v²=2gh，是同一运动不同表达。"},
        ],
    },
}

def main():
    apply = "--apply" in sys.argv
    d = json.load(open(PATH, encoding="utf-8"))
    fp = re.compile(r"统一复核|降低上手门槛|可追溯流程|边界样本建议单独标注|减少重复确认成本|标准化，再批量|可复核输出|沿用模板逐项核对|形成标准复核清单|统一口径|快速复核|高频复用模板|在.{1,20}(业务|场景)里，优先把.{1,40}标准化后再执行|复用模板示例|保留复用模板")
    weak = re.compile(r"先按业务口径补充必要字段|运行工具并记录输出|对比另一组边界输入|乘以 10%|两档复算|先用一组可复现输入|同一输入样本测试默认和边界情况|选择两组不同来源样本并同步口径定义")
    changed = 0
    for k, v in DATA.items():
        if k not in d:
            print("  SKIP 缺失:", k); continue
        d[k] = v
        changed += 1
    if apply:
        json.dump(d, open(PATH, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        print("APPLIED 写入 %d 条" % changed)
    else:
        print("DRY 拟写 %d 条" % changed)
    hit = [k for k in DATA if k in d and (fp.search(json.dumps(d[k], ensure_ascii=False)) or weak.search(json.dumps(d[k], ensure_ascii=False)))]
    print("泛化/弱模板残留:", hit if hit else "无(全清零)")

if __name__ == "__main__":
    main()
