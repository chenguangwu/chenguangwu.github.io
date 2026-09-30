# -*- coding: utf-8 -*-
"""
science 行业「英文态残留中文」收口补丁（19 页）

数据来源：scripts/_en_i18n_probe.mjs --keysrc science/<slug>
（EN 残留 ↔ zh 源文按 DOM 路径精确配对，同页两态渲染，键为运行时真实中文源文）

策略：
  * 逐 slug 读取 i18n/tools/en/science/<slug>.json，保留既有 map 全部键值；
  * 仅「新增」缺失键（key 已存在则跳过，绝不覆盖/删除）；
  * 值必须 0 汉字 + 0 中文标点，且非空串（空串运行时不会被应用）。
"""
import io
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EN_DIR = os.path.join(ROOT, 'i18n', 'tools', 'en', 'science')

CJK = re.compile(r'[\u4e00-\u9fff]')
ZH_PUNCT = re.compile(r'[，。、；：！？（）「」『』]')

# ---------------------------------------------------------------- 译文数据
DATA = {}

DATA['astro-geo-calculator'] = {
    'name': '天文地理计算器',
    'map': {
        '🌊 地震震级与能量换算': '🌊 Earthquake Magnitude and Energy',
        '根据里氏震级计算地震释放能量，并与TNT当量对比，直观感受地震威力。':
            'Computes the energy released by an earthquake from its Richter magnitude and compares it with the TNT equivalent, making the power of a quake tangible.',
        '里氏震级（0~10）': 'Richter magnitude (0-10)',
        '🔌 计算能量': '🔌 Calculate Energy',
        '📑 能量公式：log': '📑 Energy formula: log',
        '(E) = 1.5 × M + 4.8（E 单位：焦耳）': '(E) = 1.5 × M + 4.8 (E in joules)',
        'TNT当量：1 吨 TNT = 4.184 × 10': 'TNT equivalent: 1 ton of TNT = 4.184 × 10',
        '点击"计算能量"查看结果': 'Click "Calculate Energy" to see results',
        '🌍 地球曲率与地平线距离': '🌍 Earth Curvature and Horizon Distance',
        '根据观察者高度计算到地平线的距离，分别给出标准值和考虑大气折射修正后的值。':
            'Computes the distance to the horizon from the observer height, giving both the standard value and the value corrected for atmospheric refraction.',
        '观察者高度（米）': 'Observer height (m)',
        '🌍 计算地平线': '🌍 Calculate Horizon',
        '📑 标准公式：d = 3.57 × √h（km）': '📑 Standard formula: d = 3.57 × √h (km)',
        '折射修正：d = 3.86 × √h（km）': 'Refraction corrected: d = 3.86 × √h (km)',
        '其中 h 为观察者海拔高度（米）': 'where h is the observer elevation (m)',
        '点击"计算地平线"查看结果': 'Click "Calculate Horizon" to see results',
        '🌀 蒲福风级对照': '🌀 Beaufort Scale Reference',
        '输入风速，自动匹配对应的蒲福风级，显示风名及海面、陆地征象描述。':
            'Enter a wind speed to automatically match the Beaufort force, showing the wind name plus its sea and land characteristics.',
        '🌀 查询风级': '🌀 Look Up Force',
        '📑 蒲福风级（Beaufort Scale）：0级（无风）~ 12级（飓风），基于风速分级，每级对应特定海面和陆地征象':
            '📑 Beaufort Scale: force 0 (calm) to force 12 (hurricane), graded by wind speed, each force matching specific sea and land signs',
        '输入风速后点击"查询风级"查看结果': 'Enter a wind speed and click "Look Up Force" to see results',
        '💧 相对湿度计算（干湿球温度）': '💧 Relative Humidity (Dry / Wet Bulb)',
        '通过干球温度和湿球温度差，估算相对湿度。适用于标准大气压条件下的近似计算。':
            'Estimates relative humidity from the difference between dry-bulb and wet-bulb temperature. Valid as an approximation at standard atmospheric pressure.',
        '干球温度（℃）': 'Dry-bulb temperature (°C)',
        '湿球温度（℃）': 'Wet-bulb temperature (°C)',
        '💧 计算湿度': '💧 Calculate Humidity',
        '📑 简化公式：RH ≈ 100 - (T': '📑 Simplified formula: RH ≈ 100 - (T',
        ') × 5（标准大气压近似值）': ') × 5 (approximation at standard atmospheric pressure)',
        '该公式为经验近似，精度有限，精确计算需使用饱和水汽压公式':
            'This empirical formula has limited accuracy; exact results require the saturation vapor pressure formula',
        '点击"计算湿度"查看结果': 'Click "Calculate Humidity" to see results',
        '📈 大气压与海拔转换': '📈 Atmospheric Pressure vs Altitude',
        '基于国际标准大气模型，根据海拔高度计算当地大气压强，支持多种单位显示。':
            'Based on the International Standard Atmosphere model, computes local atmospheric pressure from altitude, with several display units.',
        '海拔高度（米）': 'Altitude (m)',
        '📈 计算气压': '📈 Calculate Pressure',
        '📑 国际标准大气公式：P = 101325 × (1 - 2.25577×10': '📑 ISA formula: P = 101325 × (1 - 2.25577×10',
        '其中 h 为海拔高度（米），适用于 0~11km 对流层':
            'where h is the altitude (m), valid for the 0-11 km troposphere',
        '点击"计算气压"查看结果': 'Click "Calculate Pressure" to see results',
        '天文地理计算器是一款纯前端综合计算工具，涵盖天文观测、地球科学、气象学三大领域的常用计算，所有运算均在浏览器本地完成，无需网络连接。':
            'A pure front-end calculator covering common computations in astronomy, earth science and meteorology; everything runs locally in the browser with no network needed.',
        '日出日落时间估算': 'Sunrise and sunset time estimation',
        '地震能量与TNT当量对比': 'Earthquake energy vs TNT equivalent',
        '地球曲率与地平线距离': 'Earth curvature and horizon distance',
        '蒲福风级智能对照': 'Beaufort scale lookup',
        '干湿球温度计算湿度': 'Humidity from dry and wet bulb temperature',
        '海拔与大气压换算': 'Altitude and atmospheric pressure conversion',
        '完全离线可用': 'Fully usable offline',
        '户外摄影计划日出日落时间': 'Planning sunrise and sunset times for outdoor photography',
        '教学演示地震能量概念': 'Teaching the concept of earthquake energy',
        '航海观测计算地平线距离': 'Computing horizon distance for marine observation',
        '气象爱好者判断风力等级': 'Judging wind force for weather enthusiasts',
        '环境监测估算相对湿度': 'Estimating relative humidity for environmental monitoring',
        '登山运动了解海拔气压变化': 'Understanding altitude and pressure changes in mountaineering',
    },
}

DATA['astronomy-toolkit'] = {
    'name': '天文观测工具箱',
    'map': {
        '公式：亮度比 = 2.512^(m2 - m1)，星等越小越亮。':
            'Formula: brightness ratio = 2.512^(m2 - m1); the smaller the magnitude, the brighter.',
        '天体 A 星等 (m1)': 'Body A magnitude (m1)',
        '天体 B 星等 (m2)': 'Body B magnitude (m2)',
        '请输入两个星等数值，计算它们的亮度比。': 'Enter two magnitudes to compute their brightness ratio.',
        '常见天体视星等参考表': 'Apparent Magnitudes of Common Objects',
        '天体': 'Object',
        '视星等': 'Apparent magnitude',
        '白天天空中的恒星': 'The star seen in the daytime sky',
        '满月时的月亮': 'The Moon at full phase',
        '金星（最亮）': 'Venus (brightest)',
        '夜空中最亮的行星': 'Brightest planet in the night sky',
        '木星（最亮）': 'Jupiter (brightest)',
        '太阳系最大行星': 'Largest planet in the solar system',
        '火星（最亮）': 'Mars (brightest)',
        '冲日时最亮': 'Brightest at opposition',
        '天狼星': 'Sirius',
        '全天最亮恒星': 'Brightest star in the sky',
        '老人星': 'Canopus',
        '全天第二亮恒星': 'Second-brightest star in the sky',
        '织女星': 'Vega',
        '夏季大三角之一': 'One of the Summer Triangle stars',
        '牛郎星': 'Altair',
        '北极星': 'Polaris',
        '小熊座 alpha，导航星': 'Alpha Ursae Minoris, the navigation star',
        '肉眼极限（城郊）': 'Naked-eye limit (suburban)',
        '轻度光污染环境': 'Lightly light-polluted sky',
        '肉眼极限（暗天）': 'Naked-eye limit (dark sky)',
        '理想黑暗环境': 'Ideal dark site',
        '冥王星': 'Pluto',
        '需要中型望远镜': 'Requires a medium telescope',
        '哈勃极限': 'Hubble limit',
        '哈勃望远镜最暗目标': 'Faintest targets of the Hubble telescope',
        '星等知识': 'About Magnitude',
        '视星等（Apparent Magnitude）是衡量天体亮度的一个指标，数值越小表示越亮。星等每差 1 等，亮度相差约 2.512 倍；每差 5 等，亮度相差恰好 100 倍。星等可以为负数，太阳 (-26.74) 比满月 (-12.74) 亮约 39.8 万倍。':
            'Apparent magnitude measures the brightness of a celestial object: the smaller the value, the brighter it is. A difference of 1 magnitude is a brightness ratio of about 2.512; a difference of 5 magnitudes is exactly 100. Magnitudes can be negative: the Sun (-26.74) is about 398,000 times brighter than the full Moon (-12.74).',
        '撞击角度 (°)': 'Impact angle (°)',
        '地面密度 (kg/m³)': 'Ground density (kg/m³)',
        '估算撞击坑': 'Estimate Crater',
        '请输入陨石参数，估算撞击坑直径。': 'Enter the meteorite parameters to estimate the crater diameter.',
        '著名撞击坑参考': 'Famous Impact Craters',
        '形成年代': 'Age',
        '美国亚利桑那': 'Arizona, USA',
        '~5 万年前': '~50,000 years ago',
        '墨西哥尤卡坦': 'Yucatan, Mexico',
        '6600 万年前': '66 million years ago',
        '弗里德堡': 'Vredefort',
        '~20 亿年前': '~2 billion years ago',
        '~60 m (扰动区)': '~60 m (disturbed zone)',
        '俄罗斯西伯利亚': 'Siberia, Russia',
        '1908 年': '1908',
        '估算原理': 'How It Works',
        '基于 Pi-Group scaling law 简化公式：先计算撞击动能 E = 0.5 × m × v²，再根据经验关系式估算最终撞击坑直径。实际撞击坑大小还受地层结构、岩石类型、大气层减速等因素影响，本工具结果仅供科普参考。':
            'Based on a simplified Pi-group scaling law: the impact kinetic energy E = 0.5 × m × v² is computed first, then the final crater diameter is estimated from empirical relations. Real crater size also depends on strata, rock type and atmospheric deceleration, so results are for educational reference only.',
        '输入经纬度，转换为 UTM 坐标。': 'Enter latitude and longitude to convert to UTM coordinates.',
        'UTM 区号 (1-60)': 'UTM zone (1-60)',
        '半球 (N/S)': 'Hemisphere (N/S)',
        '北半球 N': 'Northern hemisphere N',
        '南半球 S': 'Southern hemisphere S',
        '东移 (Easting, m)': 'Easting (m)',
        '北移 (Northing, m)': 'Northing (m)',
        '反向转换': 'Reverse Conversion',
        '输入 UTM 坐标，转换为经纬度。': 'Enter UTM coordinates to convert to latitude and longitude.',
        'UTM 坐标系说明': 'About the UTM System',
        'UTM（Universal Transverse Mercator）投影将地球分为 60 个带，每带宽 6°。每个带内的坐标使用东移（Easting，500000m 为中央经线）和北移（Northing，赤道为 0）表示。UTM 坐标广泛应用于地图测绘、GPS 导航和军事地图等领域。':
            'The Universal Transverse Mercator projection divides the Earth into 60 zones, each 6° wide. Positions inside a zone are given as easting (500000 m at the central meridian) and northing (0 at the equator). UTM coordinates are widely used in mapping, GPS navigation and military maps.',
        '纬度 (°, 北纬为正)': 'Latitude (°, north positive)',
        '计算极昼极夜': 'Calculate Polar Day & Night',
        '输入纬度，计算极昼和极夜的日期范围。': 'Enter a latitude to compute the date ranges of polar day and polar night.',
        '典型城市极昼极夜参考': 'Polar Day & Night at Typical Locations',
        '朗伊尔城（斯瓦尔巴）': 'Longyearbyen (Svalbard)',
        '4月18日~8月26日': 'Apr 18 - Aug 26',
        '10月26日~2月16日': 'Oct 26 - Feb 16',
        '特罗姆瑟（挪威）': 'Tromso (Norway)',
        '5月18日~7月26日': 'May 18 - Jul 26',
        '11月27日~1月15日': 'Nov 27 - Jan 15',
        '费尔班克斯（阿拉斯加）': 'Fairbanks (Alaska)',
        '无极昼': 'No polar day',
        '无极夜（白夜现象）': 'No polar night (white nights)',
        '北极点': 'North Pole',
        '3月21日~9月23日': 'Mar 21 - Sep 23',
        '9月23日~3月21日': 'Sep 23 - Mar 21',
        '长城站（南极）': 'Great Wall Station (Antarctica)',
        '无极夜': 'No polar night',
        '中山站（南极）': 'Zhongshan Station (Antarctica)',
        '约11月下旬~1月中旬': 'approx. late Nov - mid Jan',
        '约5月下旬~7月中旬': 'approx. late May - mid Jul',
        '极昼极夜原理': 'How Polar Day & Night Work',
        '极昼和极夜发生在纬度高于 66.5°（北极圈/南极圈）的区域。当太阳直射点到达北回归线（23.5°N，夏至）时，北极圈内出现极昼，南极圈内出现极夜。太阳赤纬 = 23.5° × sin(2π × (N-81)/365)，其中 N 为年内天数。':
            'Polar day and polar night occur above 66.5° latitude (the Arctic and Antarctic Circles). When the subsolar point reaches the Tropic of Cancer (23.5°N, the June solstice), the Arctic has polar day while the Antarctic has polar night. Solar declination = 23.5° × sin(2π × (N-81)/365), where N is the day of the year.',
        '当前月相': 'Current Moon Phase',
        '新月（无月光干扰）': 'New moon (no moonlight interference)',
        '蛾眉月/残月': 'Crescent / waning crescent',
        '上弦月/下弦月': 'First quarter / last quarter',
        '盈凸月/亏凸月': 'Waxing gibbous / waning gibbous',
        '满月（强月光）': 'Full moon (strong moonlight)',
        'Bortle 光污染等级 (1-9)': 'Bortle light pollution class (1-9)',
        '1 - 完美暗天': '1 - Excellent dark site',
        '2 - 典型真正暗天': '2 - Typical truly dark site',
        '3 - 乡村过渡': '3 - Rural transition',
        '5 - 郊区': '5 - Suburban',
        '6 - 郊区/城市过渡': '6 - Suburban/urban transition',
        '7 - 城市/郊区过渡': '7 - Urban/suburban transition',
        '9 - 市中心': '9 - Inner city',
        '评估观测条件': 'Evaluate Conditions',
        '查看今日月相': "View Today's Moon Phase",
        'Bortle 光污染等级说明': 'Bortle Light Pollution Classes',
        '：完美暗天，银河肉眼可见，黄道光明显':
            ': Excellent dark site, Milky Way visible to the naked eye, zodiacal light obvious',
        '：典型真正暗天，M33 肉眼可见':
            ': Typical truly dark site, M33 visible to the naked eye',
        '：乡村过渡，银河仍清晰可见':
            ': Rural transition, Milky Way still clearly visible',
        '：乡村/郊区过渡，银河可见但细节减少':
            ': Rural/suburban transition, Milky Way visible but with less detail',
        '：郊区，银河勉强可见': ': Suburban, Milky Way barely visible',
        '：郊区/城市过渡，银河不可见': ': Suburban/urban transition, Milky Way not visible',
        '：城市/郊区过渡，云层被照亮': ': Urban/suburban transition, clouds lit up',
        '：城市天空，只能看到亮星': ': City sky, only bright stars visible',
        '：市中心，只能看到行星和最亮恒星': ': Inner city, only planets and the brightest stars visible',
        '天文观测工具箱是一款专为天文爱好者和科普学习设计的纯前端工具集合，所有计算均在浏览器本地完成，无需联网。':
            'A pure front-end toolkit for amateur astronomers and science learners; all calculations run locally in the browser with no network needed.',
        '月相查询与可视化': 'Moon phase lookup and visualization',
        '星等亮度对比计算': 'Magnitude and brightness ratio calculation',
        '经纬度与UTM坐标互转': 'Lat/lon and UTM conversion',
        '综合观测条件评估': 'Combined observing-condition evaluation',
        '天文爱好者观星前准备': 'Preparing for a stargazing session',
        '摄影爱好者计算月光影响': 'Estimating moonlight impact for photographers',
        '学生天文课程学习参考': 'Reference for astronomy coursework',
        '地理坐标专业转换需求': 'Professional geodetic coordinate conversion',
    },
}

DATA['battery-life-calculator'] = {
    'name': '电池续航计算器',
    'map': {
        '/ 电池续航计算器': '/ Battery Life Calculator',
        '理想 100%': 'Ideal 100%',
        '高效率 95%': 'High efficiency 95%',
        '标准 85%': 'Standard 85%',
        '考虑老化 70%': 'With aging 70%',
        '低效率 50%': 'Low efficiency 50%',
        '📐 基本续航公式': '📐 Basic Runtime Formula',
        'T：续航时间（小时）': 'T: runtime (hours)',
        'C：电池容量（mAh 或 Ah）': 'C: battery capacity (mAh or Ah)',
        'I：负载电流（mA 或 A）': 'I: load current (mA or A)',
        'η：电路效率（0-1）': 'η: circuit efficiency (0-1)',
        '⚡ 功率与能量计算': '⚡ Power and Energy',
        'P：功率（W），V：电压（V），I：电流（A）': 'P: power (W), V: voltage (V), I: current (A)',
        'E：能量（Wh），C：容量（Ah）': 'E: energy (Wh), C: capacity (Ah)',
        '🔋 电池原理简介': '🔋 Battery Basics',
        '容量单位': 'Capacity unit',
        '：mAh（毫安时）表示电池以1mA电流放电可持续1小时':
            ': mAh (milliampere-hour) means the cell can supply 1 mA for 1 hour',
        '：锂电池约150-350 Wh/kg，铅酸电池约30-50 Wh/kg':
            ': Li-ion cells about 150-350 Wh/kg, lead-acid about 30-50 Wh/kg',
        '放电效率': 'Discharge efficiency',
        '：实际使用中需考虑DCDC转换效率、自放电、温度影响':
            ': in practice, account for DC-DC conversion efficiency, self-discharge and temperature',
        'Peukert定律': "Peukert's law",
        '：大电流放电时实际容量会降低': ': usable capacity drops at high discharge currents',
        '截止电压': 'Cut-off voltage',
        '：锂电池通常3.0V截止，镍氢电池1.0V/节':
            ': Li-ion cells typically cut off at 3.0 V, NiMH at 1.0 V per cell',
        '🌡️ 温度对电池的影响': '🌡️ Temperature Effects',
        '低温': 'Low temperature',
        '：0°C时容量约为常温的80-90%，-20°C时约50-60%':
            ': at 0°C capacity is about 80-90% of room temperature, at -20°C about 50-60%',
        '高温': 'High temperature',
        '：40°C以上会加速老化，缩短电池寿命': ': above 40°C aging accelerates and service life shortens',
        '最佳工作温度': 'Best operating temperature',
        '：20-25°C，此时性能最优': ': 20-25°C, where performance is optimal',
        '充电温度': 'Charging temperature',
        '：通常0-45°C，超出范围可能损坏电池':
            ': typically 0-45°C; outside this range the cell may be damaged',
        '⚡ 常见电池参数参考': '⚡ Typical Battery Parameters',
        '标称电压': 'Nominal voltage',
        '典型容量': 'Typical capacity',
        'AA碱性电池': 'AA alkaline',
        'AAA碱性电池': 'AAA alkaline',
        '9V电池': '9 V battery',
        '18650锂电池': '18650 Li-ion',
        '21700锂电池': '21700 Li-ion',
        '26650锂电池': '26650 Li-ion',
        '手机电池': 'Phone battery',
        '充电宝': 'Power bank',
        '铅酸蓄电池': 'Lead-acid battery',
        '镍氢电池(AA)': 'NiMH battery (AA)',
        '纽扣电池CR2032': 'Coin cell CR2032',
        '📱 常见设备功耗参考': '📱 Typical Device Power Draw',
        '待机功耗': 'Standby power',
        '工作功耗': 'Active power',
        '智能手表': 'Smart watch',
        '蓝牙耳机': 'Bluetooth earbuds',
        '智能手机(待机)': 'Smartphone (standby)',
        '智能手机(使用)': 'Smartphone (in use)',
        '单片机/Arduino': 'MCU / Arduino',
        'LED灯珠': 'LED',
        '小型电机': 'Small motor',
    },
}

DATA['heat-transfer-calculator'] = {
    'name': '热传递计算器',
    'map': {
        '铜 (401)': 'Copper (401)',
        '铝 (237)': 'Aluminum (237)',
        '铁 (80)': 'Iron (80)',
        '钢 (50)': 'Steel (50)',
        '不锈钢 (16)': 'Stainless steel (16)',
        '空气 (0.026)': 'Air (0.026)',
        '水 (0.6)': 'Water (0.6)',
        '玻璃 (0.8)': 'Glass (0.8)',
        '保温棉 (0.04)': 'Mineral wool (0.04)',
        '泡沫塑料 (0.03)': 'Foam plastic (0.03)',
        '水 (4186)': 'Water (4186)',
        '铁/钢 (450)': 'Iron/steel (450)',
        '铝 (900)': 'Aluminum (900)',
        '铜 (385)': 'Copper (385)',
        '铅 (130)': 'Lead (130)',
        '玻璃 (800)': 'Glass (800)',
        '冰 (2000)': 'Ice (2000)',
        '空气 (1005)': 'Air (1005)',
        '橄榄油 (2100)': 'Olive oil (2100)',
        '木材 (1700)': 'Wood (1700)',
        '比热容 c (J/kg·°C)': 'Specific heat c (J/kg·°C)',
        '初始温度 T1 (°C)': 'Initial temperature T1 (°C)',
        '最终温度 T2 (°C)': 'Final temperature T2 (°C)',
        '对流系数 h (W/m²·K)': 'Convection coefficient h (W/m²·K)',
        '自然对流-空气 (5)': 'Natural convection - air (5)',
        '强制对流-空气 (25)': 'Forced convection - air (25)',
        '自然对流-水 (100)': 'Natural convection - water (100)',
        '强制对流-水 (500)': 'Forced convection - water (500)',
        '沸水冷凝 (3000)': 'Boiling water condensation (3000)',
        '核态沸腾 (10000)': 'Nucleate boiling (10000)',
        '自定义 h 值': 'Custom h value',
        '换热面积 A (cm²)': 'Heat transfer area A (cm²)',
        '壁面温度 Tw (°C)': 'Wall temperature Tw (°C)',
        '流体温度 Tf (°C)': 'Fluid temperature Tf (°C)',
        '热量传递有三种基本方式:': 'Heat is transferred in three basic ways:',
        '传导': 'Conduction',
        '(傅里叶定律):': "(Fourier's law):",
        '(k 导热系数)。': '(k thermal conductivity).',
        '对流': 'Convection',
        '(牛顿冷却):': "(Newton's law of cooling):",
        '(h 表面传热系数)。': '(h surface heat transfer coefficient).',
        '辐射': 'Radiation',
        '(斯特藩-玻尔兹曼):': '(Stefan-Boltzmann):',
        '(σ=5.67×10⁻⁸ W/m²K⁴,ε 发射率)。': '(σ=5.67×10⁻⁸ W/m²K⁴, ε emissivity).',
        '复合传热用总传热系数 U:': 'Combined transfer uses the overall coefficient U:',
        '。温度请使用绝对温标(K),面积 A、温差 ΔT 单位需统一。':
            '. Use the absolute temperature scale (K); the units of area A and temperature difference ΔT must be consistent.',
        'Q：热传导速率（W）': 'Q: heat conduction rate (W)',
        'k：导热系数（W/m·K）': 'k: thermal conductivity (W/m·K)',
        'A：接触面积（m²）': 'A: contact area (m²)',
        'ΔT：两侧温差（K）': 'ΔT: temperature difference across (K)',
        'L：材料厚度（m）': 'L: material thickness (m)',
        '🧪 常见物质导热系数': '🧪 Thermal Conductivity of Common Materials',
        '水 (20°C)': 'Water (20°C)',
        '液体': 'Liquid',
        '空气 (静止)': 'Air (still)',
        '玻璃棉': 'Glass wool',
        '保温材料': 'Insulation',
        '聚苯乙烯泡沫': 'Polystyrene foam',
        '聚氨酯泡沫': 'Polyurethane foam',
        '真空': 'Vacuum',
        '🌡️ 常见物质比热容': '🌡️ Specific Heat of Common Materials',
        '比热容最大的常见物质': 'Highest specific heat of common substances',
        '固态水': 'Solid water',
        '水蒸气': 'Water vapor',
        '气态水': 'Gaseous water',
        '比热容小的金属': 'Metal with low specific heat',
        '橄榄油': 'Olive oil',
        '酒精': 'Ethanol',
        '💨 对流换热系数参考': '💨 Convection Coefficients',
        '气体自然对流': 'Natural convection, gas',
        '液体自然对流': 'Natural convection, liquid',
        '气体强制对流': 'Forced convection, gas',
        '液体强制对流': 'Forced convection, liquid',
        '水沸腾': 'Boiling water',
        '蒸汽冷凝': 'Steam condensation',
    },
}

DATA['latlon-utm-converter'] = {
    'name': '经纬度与UTM坐标转换',
    'map': {
        'UTM带号 (1-60)': 'UTM zone (1-60)',
        '北半球 (N)': 'Northern hemisphere (N)',
        '南半球 (S)': 'Southern hemisphere (S)',
        '东移值 (Easting, m)': 'Easting (m)',
        '北移值 (Northing, m)': 'Northing (m)',
    },
}

DATA['led-resistor-calculator'] = {
    'name': 'LED电阻计算器',
    'map': {
        '/ LED电阻计算器': '/ LED Resistor Calculator',
        '红色 LED (1.8V)': 'Red LED (1.8V)',
        '橙色 LED (2.0V)': 'Orange LED (2.0V)',
        '黄色 LED (2.1V)': 'Yellow LED (2.1V)',
        '绿色 LED (2.2V)': 'Green LED (2.2V)',
        '黄绿色 LED (2.6V)': 'Yellow-green LED (2.6V)',
        '青色 LED (3.0V)': 'Cyan LED (3.0V)',
        '蓝色 LED (3.2V)': 'Blue LED (3.2V)',
        '白色 LED (3.2V)': 'White LED (3.2V)',
        '紫外 LED (3.4V)': 'UV LED (3.4V)',
        '红外 LED (1.5V)': 'Infrared LED (1.5V)',
        '自定义 Vf': 'Custom Vf',
        '绿色 LED': 'Green LED',
        '📐 串联LED限流电阻公式': '📐 Series LED Current-Limiting Resistor Formula',
        'R：限流电阻阻值（Ω）': 'R: current-limiting resistance (Ω)',
        'Vs：电源电压（V）': 'Vs: supply voltage (V)',
        'Vf：LED正向压降（V）': 'Vf: LED forward voltage (V)',
        'n：串联LED数量': 'n: number of LEDs in series',
        'If：LED正向电流（A）': 'If: LED forward current (A)',
        '⚡ 并联LED限流电阻公式': '⚡ Parallel LED Current-Limiting Resistor Formula',
        '注意：并联LED建议每个LED串联独立电阻，避免电流分配不均':
            'Note: for parallel LEDs, give each LED its own series resistor to avoid uneven current sharing',
        '🔥 电阻功率计算公式': '🔥 Resistor Power Formula',
        'P：电阻消耗功率（W）': 'P: power dissipated by the resistor (W)',
        'I：流过电阻的电流（A）': 'I: current through the resistor (A)',
        'R：电阻阻值（Ω）': 'R: resistance (Ω)',
        'V：电阻两端电压（V）': 'V: voltage across the resistor (V)',
        '💡 设计裕量：建议选择额定功率为实际功耗1.5~2倍的电阻':
            '💡 Design margin: choose a resistor rated at 1.5-2x the actual dissipated power',
        '💡 LED工作原理': '💡 How LEDs Work',
        '• LED是电流驱动器件，必须串联限流电阻':
            '• LEDs are current-driven devices and need a series current-limiting resistor',
        '• 正向压降Vf随材料/颜色不同而变化': '• The forward voltage Vf varies with material and color',
        '• 工作电流决定LED亮度，超过额定电流会烧毁':
            '• Brightness follows the operating current; exceeding the rated current destroys the LED',
        '• 普通小功率LED典型工作电流：5~20mA': '• Typical current for small LEDs: 5-20 mA',
        '• 大功率LED：350mA、700mA、1A或更高': '• High-power LEDs: 350 mA, 700 mA, 1 A or more',
        '🌈 常见LED参数表': '🌈 Typical LED Parameters',
        '典型电流': 'Typical current',
        '红外': 'Infrared',
        '白': 'White',
        '蓝光+荧光粉': 'Blue chip + phosphor',
        '🔧 标准电阻功率等级': '🔧 Standard Resistor Power Ratings',
        '额定功率': 'Rated power',
        '典型封装': 'Typical package',
        '极小功率信号电阻': 'Very small signal resistor',
        '小功率信号电阻': 'Small signal resistor',
        '最常用，普通LED适用': 'Most common, suits ordinary LEDs',
        '中等功率': 'Medium power',
        '大功率': 'High power',
        '插件/功率电阻': 'Through-hole / power resistor',
        '大功率LED驱动': 'High-power LED driver',
        '插件/水泥电阻': 'Through-hole / cement resistor',
        '大电流应用': 'High-current applications',
        '📋 E24标准电阻值 (±5%)': '📋 E24 Standard Resistor Values (±5%)',
        '标准值': 'Standard values',
    },
}

DATA['logic-gate-simulator'] = {
    'name': '逻辑门模拟器',
    'map': {
        '组合输出': 'Combined output',
        '逻辑门（Logic Gate）是数字电路的基本组成单元，执行基本布尔逻辑运算。本工具提供 8 种常见逻辑门的交互式模拟，支持实时输入切换、LED 输出指示、真值表高亮和多门组合功能。':
            'Logic gates are the basic building blocks of digital circuits, performing elementary Boolean operations. This tool simulates 8 common gates interactively, with live input toggling, LED output indicators, truth-table highlighting and multi-gate combinations.',
        '8 种基本逻辑门': '8 basic logic gates',
        '交互式开关输入': 'Interactive switch inputs',
        'LED 灯输出指示': 'LED output indicators',
        '实时布尔表达式': 'Live Boolean expression',
        '真值表高亮显示': 'Highlighted truth table',
        '多门组合模拟': 'Multi-gate combination',
        'SVG 门电路符号': 'SVG gate symbols',
        '数字电路教学演示': 'Digital circuit teaching demos',
        '计算机组成原理学习': 'Learning computer organization',
        '布尔代数验证': 'Boolean algebra verification',
        '逻辑设计辅助分析': 'Logic design analysis aid',
    },
}

DATA['meteor-crater-estimator'] = {
    'name': '陨石撞击坑直径估算',
    'map': {
        '石陨石 (3000 kg/m³)': 'Stony meteorite (3000 kg/m³)',
        '铁陨石 (7800 kg/m³)': 'Iron meteorite (7800 kg/m³)',
        '石铁陨石 (4500 kg/m³)': 'Stony-iron meteorite (4500 kg/m³)',
        '彗星 (1500 kg/m³)': 'Comet (1500 kg/m³)',
        '结晶岩': 'Crystalline rock',
        '水面/海洋': 'Water surface / ocean',
        '冰川/冰盖': 'Glacier / ice sheet',
    },
}

DATA['ohms-law-calculator'] = {
    'name': '欧姆定律计算器',
    'map': {
        '空调(1匹)': 'Air conditioner (1 hp)',
        '📐 欧姆定律基本公式': "📐 Ohm's Law Basic Formula",
        'V：电压（伏特，V）': 'V: voltage (volts, V)',
        'I：电流（安培，A）': 'I: current (amperes, A)',
        'R：电阻（欧姆，Ω）': 'R: resistance (ohms, Ω)',
        '⚡ 电功率计算公式': '⚡ Electric Power Formula',
        'P：功率（瓦特，W）': 'P: power (watts, W)',
        '1千瓦时(kWh) = 1度电': '1 kilowatt-hour (kWh) = 1 unit of electricity',
        '🔬 电导与电阻率': '🔬 Conductance and Resistivity',
        'G：电导（西门子，S）': 'G: conductance (siemens, S)',
        'ρ：电阻率（Ω·m）': 'ρ: resistivity (Ω·m)',
        'L：导体长度（m）': 'L: conductor length (m)',
        'A：导体截面积（m²）': 'A: conductor cross-section (m²)',
        '💡 欧姆定律的物理意义': "💡 Physical Meaning of Ohm's Law",
        '• 欧姆定律描述了电压、电流、电阻三者的关系': "• Ohm's law relates voltage, current and resistance",
        '• 在恒定温度下，金属导体的电流与电压成正比':
            '• At constant temperature, current in a metallic conductor is proportional to voltage',
        '• 电阻是导体对电流的阻碍作用的度量':
            '• Resistance measures how strongly a conductor opposes current',
        '• 适用于线性电阻（欧姆导体），如金属、碳膜电阻等':
            '• Applies to linear (ohmic) conductors such as metals and carbon-film resistors',
        '• 不适用于二极管、三极管等非线性器件':
            '• Does not apply to non-linear devices such as diodes and transistors',
        '🔌 常见电器功率参考': '🔌 Typical Appliance Power',
        '电流': 'Current',
        'LED灯泡': 'LED bulb',
        '节能灯': 'CFL',
        '白炽灯': 'Incandescent lamp',
        '笔记本电脑': 'Laptop',
        '台式电脑': 'Desktop PC',
        '电视机': 'TV',
        '微波炉': 'Microwave oven',
        '电热水壶': 'Electric kettle',
        '电热水器': 'Electric water heater',
        '手机充电': 'Phone charging',
        '🧪 常见材料电阻率 (20°C)': '🧪 Resistivity of Common Materials (20°C)',
        '电阻率 (Ω·m)': 'Resistivity (Ω·m)',
        '导电性能': 'Conductivity',
        '最好': 'Best',
        '优良': 'Excellent',
        '铂 (Pt)': 'Platinum (Pt)',
        '镍铬合金': 'Nichrome',
        '差(加热用)': 'Poor (used for heating)',
        '硅 (Si)': 'Silicon (Si)',
        '半导体': 'Semiconductor',
        '绝缘体': 'Insulator',
        '📏 国际单位制词头': '📏 SI Prefixes',
        '词头': 'Prefix',
        '兆': 'Mega',
        'MΩ (兆欧)': 'MΩ (megohm)',
        'kV (千伏)': 'kV (kilovolt)',
        '毫': 'Milli',
        'mA (毫安)': 'mA (milliampere)',
        'μA (微安)': 'μA (microampere)',
        '纳': 'Nano',
        'nS (纳西门子)': 'nS (nanosiemens)',
    },
}

DATA['pcb-trace-width'] = {
    'name': 'PCB走线宽度计算器',
    'map': {
        '📐 IPC-2221 公式': '📐 IPC-2221 Formula',
        'W：走线宽度 (mils)': 'W: trace width (mils)',
        'I：电流 (A)': 'I: current (A)',
        'ΔT：温升 (°C)': 'ΔT: temperature rise (°C)',
        't：铜箔厚度 (oz)': 't: copper thickness (oz)',
        'k, b, c：经验系数': 'k, b, c: empirical coefficients',
        '🔢 经验系数': '🔢 Empirical Coefficients',
        '外层 (External)': 'Outer layer (External)',
        '内层 (Internal)': 'Inner layer (Internal)',
        '⚡ 物理原理': '⚡ Physical Principles',
        '焦耳热': 'Joule heating',
        '：电流通过导体产生热量 Q = I²Rt': ': current through a conductor generates heat Q = I²Rt',
        '散热方式': 'Heat dissipation',
        '：外层走线通过对流和辐射散热，效果更好':
            ': outer-layer traces dissipate heat by convection and radiation, and do so better',
        '：1 oz = 35μm，2 oz = 70μm，以此类推': ': 1 oz = 35 μm, 2 oz = 70 μm, and so on',
        '：实际设计建议预留20-50%的安全裕量': ': in real designs keep a 20-50% safety margin',
        '温升影响': 'Effect of temperature rise',
        '：温升越高，允许电流越大，但可靠性降低':
            ': a higher temperature rise allows more current but reduces reliability',
        '⚠️ 设计注意事项': '⚠️ Design Notes',
        '• 大电流走线尽量短、宽、直': '• Keep high-current traces short, wide and straight',
        '• 多层层间过孔会增加阻抗和发热': '• Vias between layers add impedance and heating',
        '• 考虑PCB基材的耐热等级': '• Consider the thermal rating of the PCB substrate',
        '• 高频信号需考虑趋肤效应': '• High-frequency signals need the skin effect considered',
        '• 差分对走线需等长等宽': '• Differential pairs must be equal in length and width',
        '📋 1 oz铜箔 走线电流参考表': '📋 Trace Current Table for 1 oz Copper',
        '外层宽度 (mm)': 'Outer layer width (mm)',
        '内层宽度 (mm)': 'Inner layer width (mm)',
        '温升 10°C': 'Temperature rise 10°C',
        '🔩 铜箔厚度换算': '🔩 Copper Thickness Conversion',
        '厚度 (μm)': 'Thickness (μm)',
        '厚度 (mil)': 'Thickness (mil)',
        '信号层、细线': 'Signal layers, fine traces',
        '标准电源/信号': 'Standard power / signal',
        '大电流电源': 'High-current power',
        '大功率电源': 'High-power supply',
        '大电流母线': 'High-current busbar',
        '特殊厚铜': 'Special heavy copper',
    },
}

DATA['pi-digits'] = {
    'name': '圆周率位数查询',
    'map': {
        '/ 圆周率位数查询': '/ Pi Digits Explorer',
    },
}

DATA['polar-day-night'] = {
    'name': '极昼极夜日期判断',
    'map': {
        '北半球': 'Northern hemisphere',
        '南半球': 'Southern hemisphere',
    },
}

DATA['science-flow-rate'] = {
    'name': '流量计算器',
    'map': {
        '/ 流量计算器': '/ Flow Rate Calculator',
        '容器体积': 'Container volume',
        '充满时间': 'Fill time',
        '💡 输入容器体积和充满时间，计算平均流量':
            '💡 Enter the container volume and fill time to get the average flow rate',
        '📐 体积流量基本公式': '📐 Basic Volumetric Flow Formula',
        'Q：体积流量（m³/s）': 'Q: volumetric flow rate (m³/s)',
        'A：管道截面积（m²）': 'A: pipe cross-sectional area (m²)',
        'v：流体平均流速（m/s）': 'v: mean fluid velocity (m/s)',
        '⭕ 圆形管道截面积': '⭕ Circular Pipe Cross-section',
        'd：管道内径（m）': 'd: pipe inner diameter (m)',
        'π：圆周率 ≈ 3.14159': 'π: pi ≈ 3.14159',
        '⬜ 矩形管道截面积': '⬜ Rectangular Duct Cross-section',
        'w：管道宽度（m）': 'w: duct width (m)',
        'h：管道高度（m）': 'h: duct height (m)',
        '⚖️ 质量流量': '⚖️ Mass Flow Rate',
        'ṁ：质量流量（kg/s）': 'ṁ: mass flow rate (kg/s)',
        'ρ：流体密度（kg/m³）': 'ρ: fluid density (kg/m³)',
        '水的密度 ≈ 1000 kg/m³': 'Density of water ≈ 1000 kg/m³',
        '🌊 雷诺数 (Re)': '🌊 Reynolds Number (Re)',
        'Re：雷诺数（无量纲）': 'Re: Reynolds number (dimensionless)',
        'v：流速（m/s）': 'v: velocity (m/s)',
        'd：管径（m）': 'd: pipe diameter (m)',
        'ν：运动粘度（m²/s）': 'ν: kinematic viscosity (m²/s)',
        '流态判断：': 'Flow regime:',
        '• Re < 2300：层流': '• Re < 2300: laminar flow',
        '• 2300 < Re < 4000：过渡流': '• 2300 < Re < 4000: transitional flow',
        '• Re > 4000：湍流': '• Re > 4000: turbulent flow',
        '💧 常见管道流速参考': '💧 Typical Pipe Velocities',
        '流体类型': 'Fluid type',
        '推荐流速': 'Recommended velocity',
        '自来水(低压)': 'Tap water (low pressure)',
        '家庭供水': 'Domestic supply',
        '自来水(市政)': 'Tap water (municipal)',
        '市政管网': 'Municipal network',
        '消防水': 'Firefighting water',
        '消防系统': 'Fire protection system',
        '冷却水': 'Cooling water',
        '工业冷却': 'Industrial cooling',
        '油类(低粘度)': 'Oil (low viscosity)',
        '润滑油等': 'Lubricating oil, etc.',
        '油类(高粘度)': 'Oil (high viscosity)',
        '重油等': 'Heavy oil, etc.',
        '气体(低压)': 'Gas (low pressure)',
        '气体(高压)': 'Gas (high pressure)',
        '高压气体': 'High-pressure gas',
        '蒸汽(饱和)': 'Steam (saturated)',
        '工业蒸汽': 'Industrial steam',
        '蒸汽(过热)': 'Steam (superheated)',
        '过热蒸汽': 'Superheated steam',
        '📏 公称管径对照': '📏 Nominal Pipe Size',
        '普通壁厚 (mm)': 'Standard wall thickness (mm)',
        '📦 流量单位换算': '📦 Flow Unit Conversion',
        '换算 (m³/s)': 'Equivalent (m³/s)',
        '立方米/秒': 'Cubic meter per second',
        '立方米/小时': 'Cubic meter per hour',
        '升/秒': 'Liter per second',
        '升/分钟': 'Liter per minute',
        '加仑/分钟': 'Gallon per minute',
        '立方英尺/分': 'Cubic foot per minute',
        '🌊 20°C时常见流体性质': '🌊 Fluid Properties at 20°C',
        '流体': 'Fluid',
        '汽油': 'Gasoline',
        '柴油': 'Diesel',
        '机油(SAE30)': 'Engine oil (SAE30)',
        '甘油': 'Glycerin',
    },
}

DATA['science-pressure-converter'] = {
    'name': '压力转换器',
    'map': {
        '/ 压力转换器': '/ Pressure Unit Converter',
        '📐 压力定义': '📐 Definition of Pressure',
        'P：压力（Pa）': 'P: pressure (Pa)',
        'F：垂直作用力（N）': 'F: normal force (N)',
        'A：受力面积（m²）': 'A: area over which the force acts (m²)',
        '1帕斯卡(Pa) = 1牛顿/平方米(N/m²)': '1 pascal (Pa) = 1 newton per square meter (N/m²)',
        '🌊 液体静压力': '🌊 Hydrostatic Pressure',
        'ρ：液体密度（kg/m³）': 'ρ: liquid density (kg/m³)',
        'g：重力加速度 ≈ 9.80665 m/s²': 'g: gravitational acceleration ≈ 9.80665 m/s²',
        'h：液体深度（m）': 'h: liquid depth (m)',
        '💡 10米水深约等于1个大气压': '💡 10 m of water is roughly one atmosphere',
        '💨 理想气体定律': '💨 Ideal Gas Law',
        'V：体积（m³）': 'V: volume (m³)',
        'n：物质的量（mol）': 'n: amount of substance (mol)',
        'R：气体常数 ≈ 8.314 J/mol·K': 'R: gas constant ≈ 8.314 J/mol·K',
        'T：绝对温度（K）': 'T: absolute temperature (K)',
        '🏔️ 大气压与海拔': '🏔️ Atmospheric Pressure and Altitude',
        '• 标准大气压：1 atm = 101325 Pa': '• Standard atmosphere: 1 atm = 101325 Pa',
        '• 海拔每升高100米，气压约下降1.2 kPa': '• Pressure drops about 1.2 kPa per 100 m of altitude',
        '• 海拔每升高1000米，水的沸点下降约3°C':
            '• The boiling point of water drops about 3°C per 1000 m of altitude',
        '• 海拔5500米处，气压约为海平面的一半':
            '• At 5500 m the pressure is about half that at sea level',
        '📋 压力单位对照': '📋 Pressure Unit Reference',
        '帕斯卡': 'Pascal',
        '国际标准单位': 'International standard unit',
        '千帕': 'Kilopascal',
        '工程常用': 'Common in engineering',
        '兆帕': 'Megapascal',
        '高压系统': 'High-pressure systems',
        '巴': 'Bar',
        '毫巴': 'Millibar',
        '气象': 'Meteorology',
        '标准大气压': 'Standard atmosphere',
        '物理参考': 'Physical reference',
        '磅/平方英寸': 'Pound per square inch',
        '英制/轮胎': 'Imperial / tires',
        '毫米汞柱': 'Millimeter of mercury',
        '血压/气压': 'Blood pressure / barometric pressure',
        '英寸汞柱': 'Inch of mercury',
        '英制气压': 'Imperial barometric pressure',
        '毫米水柱': 'Millimeter of water',
        '微压测量': 'Micro-pressure measurement',
        '千克力/平方厘米': 'Kilogram-force per square centimeter',
        '工程大气压': 'Technical atmosphere',
        '托': 'Torr',
        '真空测量': 'Vacuum measurement',
        '🌍 常见压力参考值': '🌍 Typical Pressure Values',
        '压力值': 'Pressure',
        '海平面，0°C': 'Sea level, 0°C',
        '汽车轮胎': 'Car tire',
        '自行车胎': 'Bicycle tire',
        '家用自来水': 'Household tap water',
        '消防水压': 'Firefighting water pressure',
        '氧气瓶': 'Oxygen cylinder',
        '高压锅炉': 'High-pressure boiler',
        '电站锅炉': 'Power plant boiler',
        '人的血压(收缩压)': 'Human blood pressure (systolic)',
        '正常参考值': 'Normal reference value',
        '海拔1000米': '1000 m altitude',
        '气压下降11%': 'Pressure down 11%',
        '海拔4000米': '4000 m altitude',
        '气压下降39%': 'Pressure down 39%',
        '万米高空': '10,000 m altitude',
        '民航巡航高度': 'Commercial cruise altitude',
        '🔬 真空等级划分': '🔬 Vacuum Levels',
        '压力范围': 'Pressure range',
        '低真空': 'Low vacuum',
        '真空包装、吸尘器': 'Vacuum packaging, vacuum cleaners',
        '中真空': 'Medium vacuum',
        '灯泡、真空管': 'Light bulbs, vacuum tubes',
        '高真空': 'High vacuum',
        '电子显微镜、镀膜': 'Electron microscopes, coating',
        '超高真空': 'Ultra-high vacuum',
        '加速器、表面分析': 'Accelerators, surface analysis',
        '极高真空': 'Extreme-high vacuum',
        '空间模拟、粒子物理': 'Space simulation, particle physics',
    },
}

DATA['tide-height-estimator'] = {
    'name': '潮汐高度估算',
    'map': {
        '开阔海岸': 'Open coast',
        '半封闭海湾': 'Semi-enclosed bay',
        '漏斗形海湾': 'Funnel-shaped bay',
        '根据日期自动计算': 'Calculate automatically from the date',
        '手动选择': 'Select manually',
        '月相': 'Moon phase',
        '新月 (朔)': 'New moon',
        '满月 (望)': 'Full moon',
    },
}

DATA['torque-converter'] = {
    'name': '扭矩转换器',
    'map': {
        '/ 扭矩转换器': '/ Torque Unit Converter',
        '📐 扭矩定义': '📐 Definition of Torque',
        'τ：扭矩（N·m）': 'τ: torque (N·m)',
        'r：力臂长度（m）': 'r: lever arm length (m)',
        'F：作用力（N）': 'F: applied force (N)',
        'θ：力与力臂的夹角': 'θ: angle between the force and the lever arm',
        '⚡ 扭矩与功率关系': '⚡ Torque and Power',
        'P：功率（W）': 'P: power (W)',
        'ω：角速度（rad/s）': 'ω: angular velocity (rad/s)',
        '常用：P (kW) = τ (N·m) × n (rpm) / 9550': 'Commonly used: P (kW) = τ (N·m) × n (rpm) / 9550',
        '🔄 常用换算关系': '🔄 Common Conversions',
        '💡 物理原理': '💡 Physical Principles',
        '• 扭矩是使物体发生转动的力': '• Torque is the force that makes an object rotate',
        '• 扭矩单位为力乘以长度': '• The unit of torque is force times length',
        '• 重力单位（kgf·m）基于标准重力加速度 g=9.80665 m/s²':
            '• Gravitational units (kgf·m) are based on standard gravity g = 9.80665 m/s²',
        '• 英制单位中，磅既是质量单位也是力单位':
            '• In imperial units the pound is both a mass and a force unit',
        '🚗 常见扭矩参考值': '🚗 Typical Torque Values',
        '物体/设备': 'Object / device',
        '典型扭矩': 'Typical torque',
        '手表发条': 'Watch mainspring',
        '微型机械': 'Micro mechanism',
        '螺丝刀拧紧': 'Screwdriver tightening',
        '小螺丝': 'Small screw',
        '手机振动电机': 'Phone vibration motor',
        '微型电机': 'Micro motor',
        '自行车脚踏力': 'Bicycle pedal force',
        '普通人骑行': 'Average rider',
        '家用电钻': 'Household drill',
        '普通电钻': 'Standard drill',
        '汽车发动机': 'Car engine',
        '家用轿车': 'Family sedan',
        '卡车发动机': 'Truck engine',
        '重型卡车': 'Heavy truck',
        '火车头': 'Locomotive',
        '大功率机车': 'High-power locomotive',
        '轮胎螺栓扭矩': 'Wheel bolt torque',
        '乘用车': 'Passenger car',
        '气缸盖螺栓': 'Cylinder head bolts',
        '⚡ 功率-扭矩-转速换算 (kW-N·m-rpm)': '⚡ Power-Torque-Speed Conversion (kW-N·m-rpm)',
        '扭矩 (N·m)': 'Torque (N·m)',
    },
}

DATA['voltage-divider-calculator'] = {
    'name': '分压器计算器',
    'map': {
        '/ 分压器计算器': '/ Voltage Divider Calculator',
        '期望输出电压 Vout (V)': 'Desired output voltage Vout (V)',
        '📐 分压公式': '📐 Voltage Divider Formula',
        'Vin：输入电压': 'Vin: input voltage',
        'Vout：输出电压': 'Vout: output voltage',
        'R1：上拉电阻': 'R1: upper resistor',
        'R2：下拉电阻': 'R2: lower resistor',
        '已知目标输出电压时，可计算所需电阻值':
            'When the target output voltage is known, the required resistor values can be calculated',
        '⚡ 电路参数': '⚡ Circuit Parameters',
        'R1功耗': 'R1 power dissipation',
        'R2功耗': 'R2 power dissipation',
        '💡 设计要点': '💡 Design Notes',
        '• 电阻值不宜过小，以免功耗过大': '• Do not use values that are too small, or power dissipation grows',
        '• 电阻值不宜过大，以免受负载影响': '• Do not use values that are too large, or the load will affect the output',
        '• 建议选择E24或E96系列标准电阻': '• Prefer standard E24 or E96 series values',
        '• 考虑电阻精度对输出的影响': '• Consider the effect of resistor tolerance on the output',
        '• 输出端接负载时需考虑负载效应': '• Account for loading effects when a load is connected',
        '📋 标准E24电阻值': '📋 Standard E24 Resistor Values',
        '⚡ 常见分压比参考 (R1:R2)': '⚡ Common Divider Ratios (R1:R2)',
        'Vin=5V时Vout': 'Vout at Vin = 5 V',
        'Vin=12V时Vout': 'Vout at Vin = 12 V',
    },
}

DATA['wavelength-to-rgb'] = {
    'name': '波长转RGB',
    'map': {
        '/ 波长转RGB': '/ Wavelength to RGB',
        '🌈 可见光谱': '🌈 Visible Spectrum',
        '可见光波长范围约为 380nm - 780nm：': 'Visible light ranges roughly from 380 nm to 780 nm:',
        '紫色': 'Violet',
        '青色': 'Cyan',
        '绿色': 'Green',
        '黄色': 'Yellow',
        '橙色': 'Orange',
        '红色': 'Red',
        '⚡ 基本物理公式': '⚡ Basic Physics Formulas',
        'c：光速 ≈ 3×10⁸ m/s': 'c: speed of light ≈ 3×10⁸ m/s',
        'λ：波长 (m)': 'λ: wavelength (m)',
        'f：频率 (Hz)': 'f: frequency (Hz)',
        'E：光子能量 (J)': 'E: photon energy (J)',
        'h：普朗克常数 ≈ 6.626×10⁻³⁴ J·s': 'h: Planck constant ≈ 6.626×10⁻³⁴ J·s',
        '🎨 波长转RGB算法': '🎨 Wavelength to RGB Algorithm',
        '将可见光波长转换为RGB颜色值的近似算法：':
            'An approximate algorithm for converting visible wavelength to RGB:',
        '• 按波长区间分段线性插值': '• Piecewise linear interpolation over wavelength bands',
        '• 两端（紫外/红外边缘）添加衰减因子': '• An attenuation factor at both ends (UV/IR edges)',
        '• 使用伽马校正（γ≈0.8）调整人眼感知': '• Gamma correction (γ≈0.8) to match human perception',
        '• 注意：这只是近似，实际颜色感知更复杂':
            '• Note: this is only an approximation; real color perception is more complex',
        '👁️ 人眼视觉特性': '👁️ Human Vision',
        '• 人眼对555nm（黄绿色）最敏感': '• The eye is most sensitive at 555 nm (yellow-green)',
        '• 明视觉（亮环境）：视锥细胞主导，峰值555nm':
            '• Photopic vision (bright): cones dominate, peak at 555 nm',
        '• 暗视觉（暗环境）：视杆细胞主导，峰值507nm':
            '• Scotopic vision (dark): rods dominate, peak at 507 nm',
        '• 三种视锥细胞：S(蓝420nm)、M(绿534nm)、L(红564nm)':
            '• Three cone types: S (blue 420 nm), M (green 534 nm), L (red 564 nm)',
        '• 颜色是大脑对不同波长光的主观感知':
            "• Color is the brain's subjective perception of different wavelengths",
        '🎨 常见波长对应颜色': '🎨 Colors at Common Wavelengths',
        'RGB近似值': 'Approximate RGB',
        '典型来源': 'Typical source',
        '紫外线LED边缘': 'UV LED edge',
        '蓝光LED': 'Blue LED',
        '天蓝': 'Sky blue',
        '蓝光激光': 'Blue laser',
        '绿光激光': 'Green laser',
        '人眼最敏感': 'Peak eye sensitivity',
        '钠灯': 'Sodium lamp',
        '橙光': 'Orange light',
        '橙红': 'Orange-red',
        '红激光': 'Red laser',
        '红光LED': 'Red LED',
        '深红': 'Deep red',
        '红光边缘': 'Red edge',
        '🔬 电磁波谱': '🔬 Electromagnetic Spectrum',
        '波段': 'Band',
        '波长范围': 'Wavelength range',
        'γ射线': 'Gamma rays',
        'X射线': 'X-rays',
        '紫外线': 'Ultraviolet',
        '可见光': 'Visible light',
        '红外线': 'Infrared',
        '微波': 'Microwaves',
        '无线电波': 'Radio waves',
    },
}

DATA['wire-gauge-converter'] = {
    'name': '线规转换器',
    'map': {
        '/ 线规转换器': '/ Wire Gauge Converter',
        '📐 AWG线径公式': '📐 AWG Diameter Formula',
        'd：线径 (mm)': 'd: wire diameter (mm)',
        'AWG：美国线规编号（0-40，数字越小线越粗）':
            'AWG: American Wire Gauge number (0-40; the smaller the number, the thicker the wire)',
        '基准：36AWG = 0.127mm，每3个号直径减半':
            'Reference: 36 AWG = 0.127 mm, and the diameter halves every 3 gauge numbers',
        '已知线径计算AWG编号': 'Compute the AWG number from a known diameter',
        '⚡ 电阻与截面积': '⚡ Resistance and Cross-section',
        'A：截面积 (mm²)': 'A: cross-sectional area (mm²)',
        'ρ：铜电阻率 ≈ 0.0172 Ω·mm²/m (20°C)': 'ρ: copper resistivity ≈ 0.0172 Ω·mm²/m (20°C)',
        'L：导线长度 (m)': 'L: wire length (m)',
        'R：电阻 (Ω)': 'R: resistance (Ω)',
        '💡 线规知识': '💡 About Wire Gauges',
        '编号规律': 'Numbering',
        '：AWG数越小，导线越粗': ': the smaller the AWG number, the thicker the wire',
        '直径比例': 'Diameter ratio',
        '：每增加3个AWG号，直径减半': ': the diameter halves for every 3 AWG numbers',
        '面积比例': 'Area ratio',
        '：每增加3个AWG号，截面积减半': ': the cross-sectional area halves for every 3 AWG numbers',
        '载流量估算': 'Ampacity estimate',
        '：一般铜线可按 4-6 A/mm² 估算': ': copper wire is usually estimated at 4-6 A/mm²',
        '趋肤效应': 'Skin effect',
        '：高频时电流集中在导体表面': ': at high frequencies current concentrates near the conductor surface',
        '📋 AWG线规对照表 (铜导线)': '📋 AWG Chart (Copper Wire)',
        '直径(mm)': 'Diameter (mm)',
        '截面积(mm²)': 'Cross-section (mm²)',
        '电阻(Ω/km)': 'Resistance (Ω/km)',
        '载流量(A)': 'Ampacity (A)',
        '🌡️ 温度对电阻的影响': '🌡️ Temperature Effect on Resistance',
        '铜电阻率 (Ω·mm²/m)': 'Copper resistivity (Ω·mm²/m)',
        '电阻变化': 'Resistance change',
    },
}


# ---------------------------------------------------------------- 校验 & 落地
def validate(slug, zh, en):
    errs = []
    if en == '':
        errs.append('空串（运行时不生效，应为 " "）')
    if CJK.search(en):
        errs.append('含汉字: %r' % CJK.findall(en))
    if ZH_PUNCT.search(en):
        errs.append('含中文标点: %r' % ZH_PUNCT.findall(en))
    for e in errs:
        sys.stderr.write('[FATAL] %s | key=%r -> %s\n' % (slug, zh, e))
    return not errs


def main():
    ok = True
    total_added = 0
    for slug in sorted(DATA):
        spec = DATA[slug]
        path = os.path.join(EN_DIR, slug + '.json')
        if os.path.exists(path):
            with io.open(path, encoding='utf-8') as f:
                d = json.load(f)
        else:
            d = {'slug': slug, 'industry': 'science', 'name': spec['name'], 'map': {}}
        d.setdefault('slug', slug)
        d['industry'] = 'science'
        d.setdefault('name', spec['name'])
        mp = d.setdefault('map', {})

        added = 0
        for zh, en in spec['map'].items():
            if not validate(slug, zh, en):
                ok = False
                continue
            if zh in mp:
                continue          # MERGE：已有键绝不覆盖
            mp[zh] = en
            added += 1
        total_added += added
        with io.open(path, 'w', encoding='utf-8') as f:
            json.dump(d, f, ensure_ascii=False, indent=1)
            f.write('\n')
        print('%-32s +%-4d -> map %d' % (slug, added, len(mp)))

    if not ok:
        sys.exit(1)
    print('\n新增键合计: %d' % total_added)


if __name__ == '__main__':
    main()
