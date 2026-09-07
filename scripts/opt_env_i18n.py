#!/usr/bin/env python3
# environment 批英文 i18n 清理：ed 套话清零 + convert-air-aqi 错名修正
import json, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SL = os.path.join(ROOT, 'i18n', 'tools', 'slug-en.json')
OV = os.path.join(ROOT, 'i18n', 'tools', '_en_override.json')

EN_ED = {
    'environment/carbon-offset': 'Estimate your carbon footprint (CO₂e) from daily activities like driving and electricity, then translate it into trees to plant or carbon credits needed to offset.',
    'environment/convert-air-aqi': 'Convert PM2.5 (24-hour, µg/m³) and other pollutant concentrations to a US EPA AQI score with its six-level category (good to hazardous).',
    'environment/recycling-guide': 'Look up any household item and find its correct bin under the four-category waste sorting (recyclable, kitchen, hazardous, other), with disposal tips.',
    'environment/waste-calculator': 'Estimate your household weekly, monthly, and yearly waste by population and per-capita rates, then get practical reduction tips.',
}
EN_TITLE = {
    'environment/convert-air-aqi': 'AQI Converter',
}
TAIL = ' 100% client-side, no data uploaded.'

sl = json.load(open(SL, encoding='utf-8'))
ov = json.load(open(OV, encoding='utf-8'))
n_ed = 0
n_title = 0
for k in EN_ED:
    new_ed = EN_ED[k] + TAIL
    if k in sl and isinstance(sl[k], dict) and sl[k].get('ed') != new_ed:
        sl[k]['ed'] = new_ed; n_ed += 1
    if k in ov and isinstance(ov[k], dict) and ov[k].get('ed') != new_ed:
        ov[k]['ed'] = new_ed; n_ed += 1
    if k in EN_TITLE:
        if k in sl and isinstance(sl[k], dict) and sl[k].get('en') != EN_TITLE[k]:
            sl[k]['en'] = EN_TITLE[k]; n_title += 1
        if k in ov and isinstance(ov[k], dict) and ov[k].get('en') != EN_TITLE[k]:
            ov[k]['en'] = EN_TITLE[k]; n_title += 1
json.dump(sl, open(SL, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
json.dump(ov, open(OV, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
print('ed updated:', n_ed, '| en titles fixed:', n_title)
