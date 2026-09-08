# -*- coding: utf-8 -*-
"""fluid 批3（8 工具）deep-dive 校正 + terminal-velocity 源 HTML 套话块清理：
- weber-number：算例笔误 1374 → 正确 13736（node 复核 1000*100*0.01/0.0728=13736.3）
- terminal-velocity：原仅公式无数字算例，增补斯托克斯区可复现算例（vt≈8.7e-3 m/s）
- venturi-flow-rate：原仅公式无数字算例，增补理想式可复现算例（Q≈8.2e-3 m3/s，与工具无 Cd 公式一致）
- 清理 tools/fluid/terminal-velocity.html 的 opt-guide/opt-faq 套话块（构建不剥离，须手工删）
其余 5 个已含真实公式+数字算例+2FAQ，符合标准。
`--apply` 写入；否则预览校验。
"""
import os, json, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DD = os.path.join(ROOT, 'i18n', 'tools', 'content_deepdive.json')
TV = os.path.join(ROOT, 'tools', 'fluid', 'terminal-velocity.html')

PATCH = {
    'fluid/weber-number': {
        'examples': [
            {'title': '公式', 'body': 'We = rho*v^2*L/gamma。例：水 gamma=0.0728 N/m、v=10 m/s、特征长度 L=0.01 m，We=1000*100*0.01/0.0728=1.37e4（约13736）；We>1 惯性主导、液滴易破碎。'},
        ],
    },
    'fluid/terminal-velocity': {
        'examples': [
            {'title': '公式', 'body': '平衡时重力 = 阻力 + 浮力；斯托克斯区 vt=(rho_p-rho_f)*g*d^2/(18*mu)，或一般用阻力公式反解。'},
            {'title': '算例', 'body': '斯托克斯区 vt=(rho_p-rho_f)*g*d²/(18·mu)。例：沙粒 d=100 μm、密度差 Δrho=1600 kg/m³、水 mu=1e-3 Pa·s，vt=1600*9.81*(1e-4)²/(18e-3)=8.7e-3 m/s≈8.7 mm/s；更大颗粒进入牛顿区需用阻力公式反解并计入浮力。'},
        ],
    },
    'fluid/venturi-flow-rate': {
        'examples': [
            {'title': '公式', 'body': 'Q = A2·√(2·Δp/(rho·(1−(A2/A1)²)))。喉部缩径产生压差换算流量（本简化式不计流量系数）。'},
            {'title': '算例', 'body': 'Q=A2·√(2Δp/(rho·(1−(A2/A1)²)))。例：A1=0.01、A2=0.0025、Δp=5 kPa、水 rho=1000，Q=0.0025·√(2·5000/(1000·(1−0.25²)))=0.0025·3.27≈8.2e-3 m³/s（约29.5 m³/h）。'},
        ],
    },
}


def clean_terminal_velocity():
    s = open(TV, encoding='utf-8').read()
    before = s.count('class="opt-guide"') + s.count('class="opt-faq"')
    s = re.sub(r'<section class="opt-guide">.*?</section>\s*', '', s, flags=re.S)
    s = re.sub(r'<section class="opt-faq">.*?</section>\s*', '', s, flags=re.S)
    after = s.count('class="opt-guide"') + s.count('class="opt-faq"')
    open(TV, 'w', encoding='utf-8').write(s)
    print('terminal-velocity opt块清理: 前%d 后%d' % (before, after))


def main():
    d = json.load(open(DD, encoding='utf-8'))
    for k, patch in PATCH.items():
        assert k in d, '缺失条目: %s' % k
        for fld, val in patch.items():
            d[k][fld] = val
        print('PATCH:', k, '| examples=%d' % len(d[k]['examples']))
    if '--apply' not in sys.argv:
        print('预览模式（加 --apply 写入）'); return 0
    json.dump(d, open(DD, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
    clean_terminal_velocity()
    print('已写入', DD)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
