#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""真实化 embedded 分类（仅 1 工具 analysis-22）。

原工具名/描述为「功耗（动态/静态）分析」（嵌入式功耗分析），但实际 JS 只是通用统计
（均值/中位数/方差），名称与逻辑严重错配、误导用户。本脚本：
1. content_deepdive.json：写入真实嵌入式功耗分析 deep-dive（summary+3 scenarios+1 example+3 faqs）。
2. analysis-22.html：
   - formula-desc → 真实功耗公式说明（中文）
   - h2 英文显示 → "Power (Dynamic/Static) Analysis"
   - 副标题英文 → 真实英文
   - 输入区 + calc JS → 真实功耗分析（V / I_active / I_sleep / duty / 电池容量 → 平均电流/平均功耗/续航）
   - tool-intro-body：真实简介 + 删 4 通用 li + 真实「使用场景」
3. i18n/tools/_en_override.json + slug-en.json：英文标题/描述改为真实功耗分析。
名称（中文 title / h1 / 面包屑）保持不变。
"""
import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOOLS = os.path.join(ROOT, 'tools', 'embedded')
PAGE = os.path.join(TOOLS, 'analysis-22.html')
DEEP = os.path.join(ROOT, 'i18n', 'tools', 'content_deepdive.json')
EN_OV = os.path.join(ROOT, 'i18n', 'tools', '_en_override.json')
SLUG_EN = os.path.join(ROOT, 'i18n', 'tools', 'slug-en.json')

GENERIC_LIS = [
    '纯前端处理，数据不上传服务器',
    '操作简单，一键完成',
    '实时显示结果，所见即所得',
    '支持复制和下载结果',
]

NEW_DEEP = {
    'embedded/analysis-22': {
        'title': '功耗（动态/静态）分析',
        'summary': '输入供电电压、动态（工作）电流、静态（休眠）电流与占空比，估算嵌入式系统的平均电流、平均功耗与电池续航，辅助低功耗设计与电池容量选型。',
        'scenarios': [
            '物联网终端休眠/唤醒电流核算：设备在睡眠态仅耗 μA 级电流、工作态 mA 级，按占空比加权得平均电流，评估对续航的影响。',
            '电池供电产品续航预估：给定电池容量（mAh）与平均电流，估算可工作时长，指导容量选型与充电周期规划。',
            '占空比与功耗权衡优化：在响应时延允许范围内降低占空比可显著延长续航，用于低功耗策略的量级验证。',
        ],
        'examples': [
            {'title': '示例：纽扣电池物联网节点',
             'body': 'V=3.7V、I_active=25mA、I_sleep=0.05mA、占空比 5%、电池 2000mAh。平均电流≈1.27mA，平均功耗≈4.7mW，理论续航≈65 天。'},
        ],
        'faqs': [
            {'q': '平均电流如何计算？', 'a': 'I_avg = I_active×占空比 + I_sleep×(1−占空比)，即按工作时间占比对动态/静态电流加权，单位与输入电流一致（mA）。'},
            {'q': '结果可直接用于正式电池选型吗？', 'a': '适合方案预研与量级估算；正式选型应叠加电源转换效率、自放电、温度与老化折减，并以实测为准。'},
            {'q': '为什么静态电流很重要？', 'a': '低占空比设备大部分时间处于休眠，静态电流虽小却主导平均电流与续航，μA 级差异即可显著改变电池寿命。'},
        ],
    }
}

FORMULA_DESC = ('本工具按 I_avg = I_active×占空比 + I_sleep×(1−占空比) 求平均电流，'
                '平均功耗 P_avg = V × I_avg（电压 V 单位 V、电流单位 mA，得 mW），'
                '给定电池容量 C(mAh) 时续航 t = C / I_avg（小时）。纯前端本地计算，数据不上传服务器。')

H2_EN = '🔧 Power (Dynamic/Static) Analysis'
SUB_EN = 'Power (Dynamic/Static) Analysis runs entirely in your browser — enter supply voltage, active/sleep current and duty cycle to estimate average current, average power and battery life. No data uploaded.'

INTRO_P = ('功耗（动态/静态）分析是一款嵌入式系统功耗评估工具，输入供电电压、动态/静态电流与占空比，'
          '估算平均电流、平均功耗与电池续航，辅助低功耗设计与电池容量选型，纯前端运行、数据不上传。')

SCENES = [
    '低功耗 MCU 休眠/唤醒电流核算',
    '电池供电设备续航预估',
    '占空比与功耗权衡优化',
    '物联网终端能效评估',
]

NEW_INPUT_UI = '''<label>供电电压 V (V)</label>
<input type="number" id="V" value="3.7" step="0.1" min="0">
<label>动态（工作）电流 I_active (mA)</label>
<input type="number" id="Ia" value="25" step="0.1" min="0">
<label>静态（休眠）电流 I_sleep (mA)</label>
<input type="number" id="Is" value="0.05" step="0.001" min="0">
<label>占空比 duty (%) — 工作时间占比</label>
<input type="number" id="duty" value="5" step="0.1" min="0" max="100">
<label>电池容量 C (mAh，可选 — 用于估算续航)</label>
<input type="number" id="C" value="2000" step="1" min="0">
<div class="toolbar"><button type="button" class="btn primary" onclick="calc()">计算</button><button type="button" class="btn" onclick="copyRes()">复制</button></div>
<div class="result-box" id="res"></div>'''

NEW_JS = '''<script>
function calc(){
  const V=+document.getElementById("V").value||0;
  const Ia=+document.getElementById("Ia").value||0;
  const Is=+document.getElementById("Is").value||0;
  const duty=Math.min(100,Math.max(0,+document.getElementById("duty").value||0));
  const C=+document.getElementById("C").value||0;
  if(V<=0||Ia<0||Is<0){document.getElementById("res").innerHTML='<p>请输入有效电压与电流</p>';return;}
  const d=duty/100;
  const Iavg=Ia*d+Is*(1-d);          // mA
  const Pavg=V*Iavg;                 // mW
  const Pactive=V*Ia;                // mW 动态峰值
  const Psleep=V*Is;                 // mW 静态
  let html='';
  html+='<p>平均电流：<strong style="color:var(--primary);">'+Iavg.toFixed(4)+' mA</strong></p>';
  html+='<p>平均功耗：<strong style="color:var(--primary);">'+Pavg.toFixed(3)+' mW</strong>（'+(Pavg/1000).toFixed(5)+' W）</p>';
  html+='<p>动态峰值功耗：<strong>'+Pactive.toFixed(3)+' mW</strong></p>';
  html+='<p>静态休眠功耗：<strong>'+Psleep.toFixed(4)+' mW</strong></p>';
  html+='<p>占空比：<strong>'+duty.toFixed(1)+' %</strong></p>';
  if(C>0){
    const lifeH=C/Iavg;
    html+='<p>理论续航：<strong>'+(isFinite(lifeH)?lifeH.toFixed(2):'∞')+' 小时</strong>（'+(lifeH/24).toFixed(2)+' 天，容量 '+C+' mAh）</p>';
  }else{
    html+='<p>续航：<span style="color:var(--text-muted)">未填电池容量，仅给出平均电流与平均功耗</span></p>';
  }
  document.getElementById("res").innerHTML=html;
}
calc();
function copyRes(){ToolBox.copyText(document.getElementById("res").innerText);}
</script>'''

OLD_INPUT_UI = '''<label>输入数据（逗号或换行分隔）</label>
<textarea id="data" rows="4" oninput="calc()" placeholder="例如: 10,20,30,40,50">10,20,30,40,50,60,70,80</textarea>
<div class="toolbar"><button type="button" class="btn primary" onclick="calc()">统计分析</button><button type="button" class="btn" onclick="copyRes()">复制</button></div>
<div class="result-box" id="res"></div>'''

OLD_JS_RE = re.compile(r'<script>\s*function calc\(\)\{.*?function copyRes\(\)\{ToolBox\.copyText\(document\.getElementById\("res"\)\.innerText\);\}\s*</script>', re.S)


def strip_generic_li(body: str) -> str:
    for li_text in GENERIC_LIS:
        body = re.sub(r'<li[^>]*>\s*' + re.escape(li_text) + r'\s*</li>\s*', '', body)
    body = re.sub(r'<ul[^>]*>\s*</ul>', '', body)
    body = re.sub(r'<h4[^>]*>\s*<span class="h4-icon">[^<]+</span>功能特点\s*</h4>(?!\s*<ul)', '', body)
    return body


def main():
    # 1) deep-dive
    d = json.load(open(DEEP, encoding='utf-8'))
    d.update(NEW_DEEP)
    json.dump(d, open(DEEP, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
    print('  ✅ deep-dive updated: embedded/analysis-22')

    # 2) html
    t = open(PAGE, encoding='utf-8').read()
    new = t
    # formula-desc
    new = re.sub(r'<p class="formula-desc">[^<]*</p>',
                 '<p class="formula-desc">' + FORMULA_DESC + '</p>', new)
    # h2 英文显示
    new = new.replace('🔧 Analysis 22', H2_EN)
    # 副标题英文
    new = new.replace('Analysis 22 is available directly in your browser, with no data uploaded.', SUB_EN)
    # 输入区
    if OLD_INPUT_UI in new:
        new = new.replace(OLD_INPUT_UI, NEW_INPUT_UI)
    else:
        print('  ⚠️  未匹配输入区，跳过 UI 替换')
    # JS
    if OLD_JS_RE.search(new):
        new = OLD_JS_RE.sub(NEW_JS, new)
    else:
        print('  ⚠️  未匹配 JS 块，跳过 JS 替换')
    # tool-intro-body
    new = new.replace(
        '<p>功耗（动态/静态）分析。免费在线工具，纯前端处理，数据不上传，保护隐私安全。</p>',
        '<p>' + INTRO_P + '</p>')
    # 使用场景 li
    new = new.replace(
        '<li>日常办公与学习</li>\n      <li>开发调试与数据处理</li>\n      <li>快速计算与格式转换</li>\n      <li>信息查询与参考</li>',
        '\n'.join('      <li>%s</li>' % s for s in SCENES))
    # 删 4 通用 li（仅 tool-intro-body 内）
    def strip(m):
        return m.group(0).replace(m.group(1), strip_generic_li(m.group(1)))
    new = re.sub(r'class="tool-intro-body"[^>]*>(.*?)</div>', strip, new, flags=re.S)

    if new != t:
        open(PAGE, 'w', encoding='utf-8').write(new)
        print('  ✅ analysis-22.html 已重写逻辑与描述')
    else:
        print('  ⚠️  analysis-22.html 无变化')

    # 3) i18n 英文
    for f, key in [(EN_OV, 'embedded/analysis-22'), (SLUG_EN, 'embedded/analysis-22')]:
        j = json.load(open(f, encoding='utf-8'))
        if key in j:
            j[key]['en'] = 'Power (Dynamic/Static) Analysis'
            if f == EN_OV:
                j[key]['ed'] = ('Power (Dynamic/Static) Analysis - free online tool. '
                                'Free online tool on ToolBox — 100% client-side, no data uploaded, no install. '
                                'Part of the Embedded Systems tools.')
            else:
                j[key]['ed'] = 'Power (Dynamic/Static) Analysis is a free online tool.'
            json.dump(j, open(f, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
            print('  ✅', os.path.basename(f), '英文已更新')
        else:
            print('  ⚠️ ', os.path.basename(f), '无', key, '条目')


if __name__ == '__main__':
    main()
