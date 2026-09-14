#!/usr/bin/env python3
"""meteorology 分类 formula 补框：给 11 个计算类缺框页加 class="card formula-box" 公式说明。

用法: python3 scripts/add_meteorology_formula.py [--apply]
公式文本取自各页真实计算逻辑；插入锚点按优先级自动匹配（tip-box / tabs / input-row 之前）。
"""
import os, re, sys

TOOLS = os.path.join(os.path.dirname(__file__), '..', 'tools', 'meteorology')

FB_TPL = ('<div class="card formula-box">\n'
          '  <div class="formula-title">📐 计算方式</div>\n'
          '  <p>%s</p>\n'
          '</div>\n')

FORMULAS = {
  'assessor-29': '干旱评估用两类指标：降水距平百分率 Pa=(当前降水量−同期均值)÷同期均值×100%，按 Pa 阈值分级（≥−15% 无旱、−30% 轻旱、−50% 中旱、−70% 重旱、<−70% 特旱）；标准化降水指数 SPI=(当前−均值)÷标准差，按 SPI 阈值（≥−0.5 无旱、−1.0 轻旱、−1.5 中旱、−2.0 重旱、<−2.0 特旱）分级，用于多时间尺度干旱监测。',
  'capeduiliuyouxiaoweineng': '对流有效位能 CAPE=R·ΔT/Te·ΔP，其中 ΔT=气块温度−环境温度(K)、ΔP=(pLFC−pEL)×100（LFC=自由对流高度、EL=平衡高度），R 为干空气气体常数；CAPE>0 表示对流可用位能，越大越易发展强对流，常配 CIN（对流抑制）判断是否需要强抬升触发。常用阈值：<500 弱、500–1500 中等、1500–2500 强、>2500 极端。',
  'dafengyingxiangpinggu': '大风影响评估以平均风速与阵风风速代入蒲福风级（风速与等级的非线性查表），阵风等级 windWarning 给出预警等级；阵风系数=阵风÷平均风，系数越大结构风振越显著，对广告牌、塔吊、行道树与高空作业风险越高，需结合等级落实加固与停运措施。',
  'detector-protection': '建筑物防雷：雷击大地密度 Ng=0.1·Td（Td 为雷暴日数）；等效面积 Ae 按建筑长 L、宽 W、高 h 估算（h 小于长宽时 Ae=L·W+2(L+W)√(h(200−h))+πh(200−h)，否则简化为 L·W+2(L+W)h+πh²），单位 km²；年预计雷击次数 N=k·Ng·Ae（k 为校正系数），按 N 与建筑重要性判定一/二/三类防雷。滚球法保护范围：保护半径 rx=√(h(2hr−h))−√(hx(2hr−hx))，hr 为滚球半径（一类 30m / 二类 45m / 三类 60m），h 为针高、hx 为被保护物高。',
  'haiyangfengbaochaoyujing': '风暴潮增水由气压减水与风应力增水叠加：气压减水 hP=ΔP×100/(ρg)（ΔP=标准气压−中心气压），风应力增水 hW=C·V²/g×方向系数（V 为最大风速）；总增水=hP+hW，结合台风强度分级（按中心气压）给出蓝/黄/橙/红预警等级，用于沿海防汛调度。',
  'jiaotongqixianganquantishi': '道路气象安全按三项分级综合研判：能见度 vis（<50m 特级、<200m 红、<500m 橙、<1000m 黄、其余良好）、路面温度 rt（<−3℃ 红、<0℃ 橙、<2℃ 黄）、侧风 v（≥24m/s 红，逐级下降）。任一要素达红/橙级即给出对应管制建议（限速、防滑、封闭），保障行车安全。',
  'lvyouqixiangzhishu': '旅游气象指数按温度(T)、湿度(RH)、风速(V)、紫外线(UV)四项舒适度加权：温度分=100−|T−22|×3.5、湿度分=100−|RH−55|×0.9、风速分=100−|V−3|×6、紫外线分=100−UV×9（均截断 0–100）；综合 idx=0.35×T分+0.20×RH分+0.20×V分+0.25×UV分，越高越适宜出游（≥80 极适宜、≥65 适宜、≥50 一般、≥35 不太适宜、<35 不适宜）。',
  'nongyeqixiangjianyi': '农业气象建议基于作物积温：生育进度=累积 GDD÷该作物所需 GDD 上限×100，划分播种-出苗/苗期-分蘖/拔节-抽穗/灌浆-结铃/成熟等生育期；播种适宜性按气温 T 与作物播种温区[sowT]、最适温区[optT]判定；降水量 P<10mm 提示灌溉缺水，依生育期与降水给出收割与防涝建议。',
  'risk-14': '气象健康风险由温度、湿度、风速、气压四要素偏离舒适区的危害函数加权：fT=|T−22|/28、fRH=|RH−55|/60、fV=V/18、fP=|P−1013|/40（均截断 0–1），综合 R=100×(0.35fT+0.20fRH+0.20fV+0.25fP)；R 越高，对心脑血管与呼吸道疾病的诱发风险越大，敏感人群需加强防护。',
  'strength-3': '雷达回波强度：反射率因子 Z=10^(dBZ/10)，降水率 R=(Z/200)^(1/1.6) mm/h；冰雹概率由 dBZ 与回波顶高 h 联合估计；液态水含量 VIL=3.44×10⁻⁶·Z^(4/7)·h（kg/m²）；按 dBZ 阈值（<30 弱对流、<50 强对流、≥55 冰雹可能、≥60 强冰雹）判定对流等级，并结合面积与强度估算降水贡献。',
  'temp': '湿热风体感综合三种经验模型：高温(T≥27℃)用酷热指数 HI=heatIndexC(T,RH)，低温(T≤10℃)用风寒指数 WC=windChillC(T,Vkmh)，中间温区用表观温度 AT=apparentTempC(T,RH,Vms)；三者均由温度、湿度、风速经经验公式换算得到体感温度，风速折算按 Vkmh=V×3.6、Vms=V÷3.6。',
}

ANCHORS = [
  r'(<div class="tip-box")',
  r'(<div class="tabs")',
  r'(<div class="scale-row")',
  r'(<div class="set-row")',
  r'(<div[^>]*class="[^"]*tool-result[^"]*"[^>]*>)',
  r'(<div class="input-row")',
  r'(<div class="subject-row")',
]


def add_one(slug, apply):
    fp = os.path.join(TOOLS, slug + '.html')
    s = open(fp, encoding='utf-8').read()
    if 'class="formula-box"' in s:
        print('  skip %s (已有框)' % slug)
        return False
    if slug not in FORMULAS:
        print('  skip %s (无公式定义)' % slug)
        return False
    fb = FB_TPL % FORMULAS[slug]
    used = None
    for pat in ANCHORS:
        m = re.search(pat, s)
        if m:
            used = pat
            s2 = s[:m.start()] + fb + s[m.start():]
            break
    if used is None:
        print('  WARN %s (无可用锚点)' % slug)
        return False
    if apply:
        open(fp, 'w', encoding='utf-8').write(s2)
    print('  + %s (锚点:%s%s)' % (slug, used, ' [已写]' if apply else ''))
    return True


def main():
    apply = '--apply' in sys.argv
    n = 0
    for slug in FORMULAS:
        if add_one(slug, apply):
            n += 1
    print('==== %s %d 页 ====' % ('已应用' if apply else '预演', n))


if __name__ == '__main__':
    main()
