#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Real-ize deep-dive content for the `life` category (63 tools).

Replaces generic SOP boilerplate with tool-specific REAL deep-dive content.
json.dump(indent=1).
"""
import json
DD = 'i18n/tools/content_deepdive.json'
data = json.load(open(DD, encoding='utf-8'))
KB = {}

KB['life/age-calculator'] = dict(title='精确年龄计算器',
  scenarios=['由出生日期算周岁与精确到天。'],
  examples=[dict(title='计算', body='生于 2020-01-01，至 2026-09-09 → 6 岁 252 天（按历法逐月逐日算）。')],
  faqs=[dict(q='虚岁与周岁？', a='中国虚岁常+1，本工具给国际周岁。')])

KB['life/age-in-days'] = dict(title='年龄天数计算',
  scenarios=['算出生至今总天数。'],
  examples=[dict(title='计算', body='1990-01-01 至 2026-09-09 ≈ 13390 天（含闰年）。')],
  faqs=[dict(q='包含今天？', a='按区间天数计，是否含当天视设定。')])

KB['life/angle-converter'] = dict(title='角度换算器',
  scenarios=['度/弧度/梯度互转。'],
  examples=[dict(title='换算', body='180°=π rad≈3.1416；90°=π/2；1 rad≈57.30°。')],
  faqs=[dict(q='弧度是什么？', a='弧长/半径，π rad=180°。')])

KB['life/area-converter'] = dict(title='面积换算器',
  scenarios=['m²/ft²/亩/公顷互转。'],
  examples=[dict(title='换算', body='1 m²≈10.764 ft²；1 亩≈666.67 m²；1 公顷=10000 m²。')],
  faqs=[dict(q='亩与公顷？', a='1 公顷=15 亩。')])

KB['life/base-convert'] = dict(title='进制转换',
  scenarios=['2/8/10/16 互转。'],
  examples=[dict(title='换算', body='255(10)=FF(16)=11111111(2)。')],
  faqs=[dict(q='负进制？', a='本工具支持常用正进制。')])

KB['life/bill-splitter'] = dict(title='AA制账单分摊计算器',
  scenarios=['聚餐/合租平摊含小费。'],
  examples=[dict(title='分摊', body='总 300 元、3 人、含 10% 小费 → 每人 (300×1.1)/3=110 元。')],
  faqs=[dict(q='有人免单？', a='可设免单人，余额由其余均摊。')])

KB['life/birthday-paradox'] = dict(title='生日悖论计算器',
  scenarios=['算群体中至少两人生日相同的概率。'],
  examples=[dict(title='计算', body='23 人时至少两人同生日概率≈50.7%；50 人≈97%。')],
  faqs=[dict(q='为何反直觉？', a='是两两组合爆炸，非单人与全年比。')])

KB['life/bra-size-converter'] = dict(title='罩杯尺寸换算器',
  scenarios=['下围+上围定罩杯，跨国标。'],
  examples=[dict(title='换算', body='下围 75 cm、上围 88 cm → 差 13 cm 约 C 杯，标 75C（≈EU 34C）。')],
  faqs=[dict(q='罩杯怎么定？', a='上围−下围差值对应杯型（约每 2.5 cm 一档）。')])

KB['life/calorie-calculator'] = dict(title='卡路里计算器',
  scenarios=['BMR/ TDEE 估每日热量。'],
  examples=[dict(title='Mifflin', body='男 70kg/175cm/30岁：BMR=10×70+6.25×175−5×30+5=1612 kcal；轻活动×1.375≈2217。')],
  faqs=[dict(q='减脂吃多少？', a='TDEE 下浮 300–500 kcal 平稳减重。')])

KB['life/chinese-number'] = dict(title='中文数字 ⇄ 阿拉伯数字',
  scenarios=['金额/读数大写。'],
  examples=[dict(title='转换', body='12345 → 一万二千三百四十五；10086 → 一万零八十六。')],
  faqs=[dict(q='零怎么读？', a='连续零读一个“零”，如 10086。')])

KB['life/clothing-size-converter'] = dict(title='服装尺码换算器',
  scenarios=['国际 S/M/L 与胸围对照。'],
  examples=[dict(title='换算', body='男上装胸围 100 cm ≈ 国际 L（EU 50 / US 40）。')],
  faqs=[dict(q='尺码统一吗？', a='各国品牌有差，以具体尺码表为准。')])

KB['life/color-name-finder'] = dict(title='颜色名称查询',
  scenarios=['由 HEX 查近似颜色名。'],
  examples=[dict(title='查', body='#FF0000 → Red（红）；#00FF00 → Lime；#0000FF → Blue。')],
  faqs=[dict(q='名字唯一？', a='同色可有多个近似名，取最接近。')])

KB['life/concentration-converter'] = dict(title='浓度换算器',
  scenarios=['质量分数/摩尔浓度/ppm 互转。'],
  examples=[dict(title='换算', body='1% w/w = 10000 ppm；稀水溶液中 1 ppm≈1 mg/L。')],
  faqs=[dict(q='ppm 是质量比？', a='通常为质量分数 10⁻⁶。')])

KB['life/cooking-converter'] = dict(title='烹饪单位换算器',
  scenarios=['杯/汤匙/毫升/克互转。'],
  examples=[dict(title='换算', body='1 杯(cup)=240 mL；1 汤匙(tbsp)=15 mL；1 茶匙(tsp)=5 mL。')],
  faqs=[dict(q='杯是美制？', a='是，1 US cup=236.6 mL（标 240 近似）。')])

KB['life/countdown'] = dict(title='倒计时器（设置日期）',
  scenarios=['设定目标日看剩余时间。'],
  examples=[dict(title='设置', body='设 2026-12-25 → 实时显示距该日天/时/分/秒。')],
  faqs=[dict(q='跨时区？', a='以本地时区计剩余。')])

KB['life/countdown-1'] = dict(title='计时器（正计时/倒计时）',
  scenarios=['厨房/锻炼计时。'],
  examples=[dict(title='使用', body='设 25:00 倒计时，归零提醒；正计时记 elapsed。')],
  faqs=[dict(q='后台运行？', a='网页计时依赖页面活跃，后台可能漂移。')])

KB['life/countdown-2'] = dict(title='纪念日倒计时（多组）',
  scenarios=['管理多个纪念日。'],
  examples=[dict(title='管理', body='同时追踪生日/周年，各显示距下次天数。')],
  faqs=[dict(q='数据存哪？', a='本地浏览器存储，不上传。')])

KB['life/countdown-timer'] = dict(title='多功能倒计时器',
  scenarios=['循环/分段倒计时。'],
  examples=[dict(title='使用', body='训练 40s 练/20s 休循环，自动切换。')],
  faqs=[dict(q='循环次数？', a='可设组数，完毕提示。')])

KB['life/csv-json'] = dict(title='CSV ↔ JSON 互转',
  scenarios=['表格与结构化数据互转。'],
  examples=[dict(title='转换', body='CSV `a,b\n1,2` → `[{"a":"1","b":"2"}]`。')],
  faqs=[dict(q='表头缺失？', a='可用列索引。')])

KB['life/csv-to-markdown'] = dict(title='CSV ↔ Markdown 表格互转',
  scenarios=['表格贴入文档。'],
  examples=[dict(title='转换', body='CSV 两行 → `| a | b |\n|---|---|\n| 1 | 2 |`。')],
  faqs=[dict(q='对齐？', a='`:--` 左、`--:` 右。')])

KB['life/currency-converter'] = dict(title='货币换算器',
  scenarios=['按汇率换算币种（需当日汇率）。'],
  examples=[dict(title='换算', body='示例 100 USD × 7.10 ≈ 710 CNY（汇率随市场变动，以实时为准）。')],
  faqs=[dict(q='汇率哪来？', a='接入行情接口或手动填当日汇率才准。')])

KB['life/data-rate-converter'] = dict(title='数据速率换算器',
  scenarios=['bps/kbps/Mbps/Gbps 互转。'],
  examples=[dict(title='换算', body='100 Mbps = 12.5 MB/s（÷8）；1 Gbps=1000 Mbps。')],
  faqs=[dict(q='小 b 与大 B？', a='bit(b) 与 Byte(B) 差 8 倍。')])

KB['life/data-unit-converter'] = dict(title='数据存储单位换算',
  scenarios=['B/KB/MB/GB/TB 互转。'],
  examples=[dict(title='换算', body='1 GB=1024 MB=1048576 KB；十进制 1 GB=1000 MB。')],
  faqs=[dict(q='1024 还是 1000？', a='系统常二进制(1024)，厂商标十进制(1000)。')])

KB['life/date-add-subtract'] = dict(title='日期加减计算器',
  scenarios=['算 N 天后/前的日期。'],
  examples=[dict(title='计算', body='2026-01-01 + 30 天 = 2026-01-31；−7 天 = 2025-12-25。')],
  faqs=[dict(q='月末溢出？', a='自动进位到下一月。')])

KB['life/date-diff'] = dict(title='日期差 / 年龄计算器',
  scenarios=['两日期相隔天数/年。'],
  examples=[dict(title='计算', body='2024-01-01 到 2026-09-09 ≈ 981 天；年龄按年。')],
  faqs=[dict(q='含端日？', a='通常算间隔天数。')])

KB['life/date-difference-calculator'] = dict(title='日期差计算器',
  scenarios=['与 date-diff 同，算间隔。'],
  examples=[dict(title='计算', body='2025-12-25 到 2026-01-01 = 7 天。')],
  faqs=[dict(q='跨年？', a='自动处理闰年与跨年。')])

KB['life/density-converter'] = dict(title='密度换算器',
  scenarios=['g/cm³/kg/m³ 互转。'],
  examples=[dict(title='换算', body='1 g/cm³ = 1000 kg/m³（水）。')],
  faqs=[dict(q='为什么差 1000？', a='cm³ 与 m³ 差 10⁶，g 与 kg 差 10³，比 1000。')])

KB['life/detector-checker-strength'] = dict(title='强密码检测器（检查强度）',
  scenarios=['评估口令熵与弱点。'],
  examples=[dict(title='检测', body='`Password1!` 含四类但常见词 → 中；`Tq7!mK9@pL2#` → 强（高熵）。')],
  faqs=[dict(q='强度看什么？', a='长度、字符集、是否词典词。')])

KB['life/drinking-water-plan'] = dict(title='Drinking Water Plan',
  scenarios=['按体重估每日饮水。'],
  examples=[dict(title='估算', body='体重 70 kg × 35 mL ≈ 2.45 L/日（含食物水分约 30–40 mL/kg）。')],
  faqs=[dict(q='运动要加？', a='要，按出汗额外补。')])

KB['life/energy-converter'] = dict(title='能量换算器',
  scenarios=['J/kJ/kWh/cal 互转。'],
  examples=[dict(title='换算', body='1 kWh=3.6 MJ=860 kcal；1 cal=4.184 J。')],
  faqs=[dict(q='食物卡路里？', a='营养标签 kcal=1000 cal。')])

KB['life/event-countdown'] = dict(title='节日倒计时',
  scenarios=['春节/国庆等倒数。'],
  examples=[dict(title='倒数', body='设春节日期 → 显示距节日天数（农历以当年为准）。')],
  faqs=[dict(q='农历每年变？', a='是，春节公历日期逐年不同。')])

KB['life/flow-rate-converter'] = dict(title='流量换算器',
  scenarios=['L/s/m³/h 互转。'],
  examples=[dict(title='换算', body='1 L/s = 3.6 m³/h；1 m³/h≈0.278 L/s。')],
  faqs=[dict(q='体积流量 vs 质量？', a='质量流量=体积×密度。')])

KB['life/frequency-converter'] = dict(title='频率换算器',
  scenarios=['Hz/kHz/MHz/GHz 互转。'],
  examples=[dict(title='换算', body='1 kHz=1000 Hz；2.4 GHz=2400 MHz。')],
  faqs=[dict(q='周期与频率？', a='T=1/f。')])

KB['life/fuel-converter'] = dict(title='油耗换算器',
  scenarios=['L/100km ↔ MPG 互转。'],
  examples=[dict(title='换算', body='8 L/100km ≈ 29.4 MPG(US)；MPG 越大越省。')],
  faqs=[dict(q='两种 MPG？', a='US 与 UK 加仑不同，数值有别。')])

KB['life/generator-random-1'] = dict(title='随机数生成器（范围任意）',
  scenarios=['得 [min,max] 均匀随机整数/浮点。'],
  examples=[dict(title='生成', body='[1,100] 均匀 → 如 42（密码学安全随机）。')],
  faqs=[dict(q='可重复？', a='随机不可复现，需种子另用。')])

KB['life/generator-strength'] = dict(title='密码生成器（带强度检测）',
  scenarios=['生成并即时评强度。'],
  examples=[dict(title='生成', body='16 位含四类 → `Tq7!mK9@pL2#vX4z`，强度强。')],
  faqs=[dict(q='多长够？', a='12+ 位抗在线爆破。')])

KB['life/holiday-calendar'] = dict(title='中国节假日日历',
  scenarios=['查法定节假日与调休。'],
  examples=[dict(title='查', body='2026 国庆 10/1–10/7 放假（以当年国务院安排为准）。')],
  faqs=[dict(q='调休怎么算？', a='放假前后周末补班，需看具体通知。')])

KB['life/leap-year-checker'] = dict(title='闰年检查器',
  scenarios=['判年份是否闰年。'],
  examples=[dict(title='判断', body='2024 被 4 整除且不被 100 → 闰年（366 天）；2100 被 100 整除但不被 400 → 平年。')],
  faqs=[dict(q='闰年规则？', a='四年一闰、百年不闰、四百年再闰。')])

KB['life/length-converter'] = dict(title='长度换算器',
  scenarios=['m/cm/ft/in/mile 互转。'],
  examples=[dict(title='换算', body='1 m=3.2808 ft；1 in=2.54 cm；1 mile≈1609.34 m。')],
  faqs=[dict(q='英尺英寸？', a='1 ft=12 in。')])

KB['life/magnet-converter'] = dict(title='磁场强度换算器',
  scenarios=['T/Gs 互转。'],
  examples=[dict(title='换算', body='1 T=10000 Gs（高斯）；地磁场约 0.00005 T。')],
  faqs=[dict(q='T 与 A/m？', a='磁感应强度 T 与磁场强度 A/m 经 μ 关联。')])

KB['life/music-practice-timer'] = dict(title='音乐练习计时器',
  scenarios=['分段练习计时。'],
  examples=[dict(title='计时', body='音阶 10 min + 曲目 20 min，累计并记录。')],
  faqs=[dict(q='可设循环？', a='可设段落循环计时。')])

KB['life/number-to-chinese'] = dict(title='数字转中文',
  scenarios=['与 chinese-number 同，数字→大写。'],
  examples=[dict(title='转换', body='2026 → 二千零二十六。')],
  faqs=[dict(q='金额大写？', a='需加“圆整”等，用专门金额大写更准。')])

KB['life/percentage-calculator'] = dict(title='百分比计算器',
  scenarios=['求百分比/增减/占比。'],
  examples=[dict(title='计算', body='150 的 20% = 30；30 是 150 的 20%；150→180 增 20%。')],
  faqs=[dict(q='百分比点？', a='与百分点不同，后者是差值单位。')])

KB['life/power-converter'] = dict(title='功率换算器',
  scenarios=['W/kW/hp 互转。'],
  examples=[dict(title='换算', body='1 hp(公制)=735.5 W；1 kW=1.359 hp。')],
  faqs=[dict(q='公制英制 hp？', a='英制 745.7 W，略高。')])

KB['life/pressure-converter'] = dict(title='压力换算器',
  scenarios=['Pa/kPa/atm/mmHg 互转。'],
  examples=[dict(title='换算', body='1 atm=101.325 kPa=760 mmHg。')],
  faqs=[dict(q='血压单位？', a='mmHg（毫米汞柱）。')])

KB['life/radiation-converter'] = dict(title='辐射剂量换算器',
  scenarios=['Sv/Gy/mSv 互转（科普）。'],
  examples=[dict(title='换算', body='1 Sv=1000 mSv；1 Gy 吸收剂量在组织权重 1 时≈1 Sv。')],
  faqs=[dict(q='Sv 与 Gy？', a='Gy 吸收、Sv 当量（乘组织权重）。')])

KB['life/ring-size-converter'] = dict(title='戒指尺寸换算器',
  scenarios=['内周长/内直径跨国标。'],
  examples=[dict(title='换算', body='内周长 52 mm ≈ CN 12 / US 6；内直径 16.5 mm ≈ US 6。')],
  faqs=[dict(q='量哪个？', a='量内圈周长或直径，指关节需能过。')])

KB['life/roman-numeral'] = dict(title='罗马数字转换',
  scenarios=['与 it/roman-numeral 同，整数↔罗马。'],
  examples=[dict(title='转换', body='1994 → MCMXCIV；2026 → MMXXVI。')],
  faqs=[dict(q='有 0 吗？', a='无，罗马数字最小 I=1。')])

KB['life/shoe-size-converter'] = dict(title='鞋码换算器',
  scenarios=['EU/US/UK/CN 互转。'],
  examples=[dict(title='换算', body='EU 42 ≈ US 9 ≈ CN 260 mm（男）；各系算法不同。')],
  faqs=[dict(q='男女同码？', a='不同，女码通常小 1–1.5。')])

KB['life/speed-converter'] = dict(title='速度换算器',
  scenarios=['m/s/km/h/mph 互转。'],
  examples=[dict(title='换算', body='1 m/s=3.6 km/h；100 km/h≈62.1 mph。')],
  faqs=[dict(q='mph 来源？', a='英里/小时，英制。')])

KB['life/stopwatch'] = dict(title='秒表计时器',
  scenarios=['计圈/分段计时。'],
  examples=[dict(title='计圈', body='总 122.4 s，lap1 12.3、lap2 10.1。')],
  faqs=[dict(q='精度？', a='毫秒显示，依赖浏览器计时。')])

KB['life/temperature-converter'] = dict(title='温度转换器',
  scenarios=['°C/°F/K 互转。'],
  examples=[dict(title='换算', body='25°C=77°F（C×9/5+32）；0°C=273.15 K。')],
  faqs=[dict(q='华氏冰点？', a='32°F，沸点 212°F。')])

KB['life/time-converter'] = dict(title='时间换算器',
  scenarios=['时区与 12/24 小时制。'],
  examples=[dict(title='换算', body='UTC+8 12:00 = UTC 04:00；13:00 → 下午 1:00。')],
  faqs=[dict(q='夏令时？', a='部分时区夏季拨快 1 小时。')])

KB['life/timestamp'] = dict(title='时间戳转换',
  scenarios=['Unix 秒↔日期。'],
  examples=[dict(title='转换', body='1700000000 → 2023-11-14 22:13:20 UTC（按本地时区显示）。')],
  faqs=[dict(q='秒还是毫秒？', a='本工具用秒，毫秒需÷1000。')])

KB['life/tip-calculator'] = dict(title='小费计算器',
  scenarios=['账单+小费+分摊。'],
  examples=[dict(title='计算', body='账单 100、小费 15% → 小费 15、合计 115；4 人均付 28.75。')],
  faqs=[dict(q='国内要给小费？', a='国内一般不含小费，海外按习惯 10–20%。')])

KB['life/todo-list'] = dict(title='待办清单',
  scenarios=['本地任务管理与提醒。'],
  examples=[dict(title='使用', body='添加任务、标记完成、按日期筛选（数据存本地）。')],
  faqs=[dict(q='会同步吗？', a='纯前端，不跨设备同步。')])

KB['life/unit-converter'] = dict(title='单位换算器',
  scenarios=['通用多类单位速转。'],
  examples=[dict(title='换算', body='长度/质量/体积/温度一键切换，如 1 kg=2.2046 lb。')],
  faqs=[dict(q='覆盖哪些类？', a='常用物理量，细分见各专项换算器。')])

KB['life/volume-converter'] = dict(title='体积换算器',
  scenarios=['L/mL/加仑/杯 互转。'],
  examples=[dict(title='换算', body='1 L=1000 mL；1 US 加仑≈3.785 L；1 杯≈240 mL。')],
  faqs=[dict(q='英制加仑？', a='英制 4.546 L，更大。')])

KB['life/weight-converter'] = dict(title='重量换算器',
  scenarios=['kg/g/lb/oz 互转。'],
  examples=[dict(title='换算', body='1 kg=2.2046 lb；1 lb=16 oz≈453.6 g。')],
  faqs=[dict(q='斤与公斤？', a='1 kg=2 斤。')])

KB['life/workday-calculator'] = dict(title='工作日计算器',
  scenarios=['算两日间的法定工作日数。'],
  examples=[dict(title='计算', body='2026-01-01 到 2026-01-31 约 22 个工作日（剔除周末与节假日）。')],
  faqs=[dict(q='节假日表？', a='按地区法定节假日，需维护。')])

KB['life/world-clock'] = dict(title='世界时钟',
  scenarios=['多时区当前时间同屏。'],
  examples=[dict(title='查看', body='北京 12:00 时，东京 13:00、伦敦 04:00、纽约 前日 23:00。')],
  faqs=[dict(q='夏令时自动？', a='依时区规则，部分需手动。')])

KB['life/yaml-json'] = dict(title='YAML/JSON 互转',
  scenarios=['配置格式互转。'],
  examples=[dict(title='转换', body='`name: Tom` → `{"name":"Tom"}`。')],
  faqs=[dict(q='注释保留？', a='JSON 无注释，转换即丢。')])

KB['life/zodiac-calculator'] = dict(title='生肖星座计算器',
  scenarios=['由生日推生肖与星座。'],
  examples=[dict(title='计算', body='1990 年生 → 生肖马；生日 4-10 → 白羊座（3/21–4/19）。')],
  faqs=[dict(q='星座按阳历？', a='是，按公历出生月日。')])

# ---------- apply ----------
changed = 0
for slug, entry in KB.items():
    if slug not in data:
        continue
    new = {'title': entry['title'], 'scenarios': entry['scenarios'],
           'examples': entry['examples'], 'faqs': entry['faqs']}
    if data[slug] != new:
        data[slug] = new
        changed += 1

print(f"KB entries: {len(KB)}  changed: {changed}")
with open(DD, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=1)
    f.write('\n')
print("written.")
