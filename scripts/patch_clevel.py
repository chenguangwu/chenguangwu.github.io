#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ROADMAP 批次5 · 补 C 级：给 KEEP-2 已真实实现但缺 formula-box 面板的工具补「计算原理」说明卡。
幂等：已含 formula-box 则跳过。纯静态 HTML，不改动现有 calc 逻辑。
"""
import re, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

FB_DESC = {
  'convert-3.html': ('进制转换原理', '基于标准进制定义实时换算：十进制 ↔ 二进制/八进制/十六进制/三十六进制 使用 <code>parseInt(value, base)</code> 与 <code>toString(targetBase)</code>，结果精确无近似。'),
  'convert-2.html': ('颜色空间换算原理', '各颜色空间按标准定义独立换算：HEX↔RGB 逐通道 16 进制映射；RGB↔HSL 按 IEC 61966 近似公式；RGB↔CMYK 按减色法定义。'),
  'convert-rehab.html': ('METs 数据说明', '对照表依据 ACSM 公开标准整理，1 MET ≈ 静息代谢率（3.5 mL O₂/kg/min）。纯前端静态展示，仅供运动强度速查参考，不构成训练处方。'),
  'convert-speed.html': ('变速换算原理', '歌曲变速后时长 = 原时长 × (原 BPM / 新 BPM)，基于音乐播放速度线性关系。节拍越快、时长越短。'),
  'convert-volume-weight.html': ('体积重量规则', '国际货运通用规则：体积重量 = 长×宽×高 ÷ 除数（航空常用 6000，部分 5000，单位 cm/kg）。计费重量取实际重与体积重之较大者。'),
  'convert-fuel-oil.html': ('油耗单位换算原理', '美欧油耗单位标准关系：L/100km = 235.2146 ÷ MPG（美制加仑）。数值越小越省油：美制 MPG 越大越省，欧制 L/100km 越小越省。'),
  'convert-time-1.html': ('SMPTE 时间码原理', '影视剪辑标准时间码：总帧数 = ((时×3600 + 分×60 + 秒) × fps) + 帧。同一时刻在不同帧率下总帧数不同。'),
  'convert-48.html': ('纱支换算定义', '纺织标准定义：特克斯 tex = 克/1000 米；英支 Ne = 590.5 / tex；公支 Nm = 1000 / tex。三者可互转。'),
  'convert-45.html': ('口径换算定义', '国际标准：1 英寸 (in) = 25.4 毫米 (mm)。毫米与英寸为线性换算，因子固定。'),
  'convert-ref-cite.html': ('著录格式规范', '依据国家标准 GB/T 7714（顺序编码制）著录模板整理。纯前端静态展示，用于文献类型格式速查。'),
  'convert-23.html': ('宠物年龄估算说明', '依据常用经验公式（狗/猫年龄 → 人年）估算，非精确生物学换算，仅供趣味对照参考。'),
  'convert-13.html': ('攀岩等级映射说明', 'V 级（Hueco）与 YDS 为美国野外攀岩常用等级近似映射，不同评级体系非完全线性对应。'),
  'convert-41.html': ('LD50 数据说明', '半数致死量（大鼠口服，mg/kg）公开参考近似值，仅作毒理学常识对照，绝非安全摄入剂量。'),
  'convert-20.html': ('斯科维尔辣度说明', '斯科维尔指数（SHU）公开参考范围，因品种、产地差异为区间值，仅供参考。'),
}

def patch(path, title, desc):
    s = open(path, encoding='utf-8').read()
    if 'formula-box' in s:
        return False
    fb = ('\n<div class="formula-box" style="margin-top:14px;">'
          '<div class="formula-title">%s</div>'
          '<div class="formula-desc">%s</div></div>\n' % (title, desc))
    if '<!-- 相关工具 -->' in s:
        s = s.replace('<!-- 相关工具 -->', fb + '<!-- 相关工具 -->', 1)
    else:
        s = s.replace('</body>', fb + '\n</body>', 1)
    open(path, 'w', encoding='utf-8').write(s)
    return True

def main():
    done = 0
    for rel, (title, desc) in FB_DESC.items():
        # 在 tools/ 下查找该 basename（跨行业）
        found = None
        for root, _, files in os.walk(os.path.join(ROOT, 'tools')):
            if rel in files:
                found = os.path.join(root, rel)
                break
        if not found:
            print('SKIP 未找到:', rel)
            continue
        ok = patch(found, title, desc)
        print(('OK   ' if ok else 'SKIP ') + found)
        if ok:
            done += 1
    print('补 C 级完成，新增 %d 个 formula-box。' % done)

if __name__ == '__main__':
    main()
