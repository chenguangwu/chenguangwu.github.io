# -*- coding: utf-8 -*-
"""Batch 11: 气象计算深化（industry=meteorology，14 个公式计算器）。

复用 scripts/tool_template.py。经验公式（露点/Magnus、体感/Steadman、湿球/Stull 等）均经手算核对。
"""
from tool_template import main

ICON = "🌤️"
BG = "#0284c7"
CAT = "calculator"

TOOLS = [
    {
        "slug": "dew-point",
        "industry": "meteorology", "cat": CAT, "icon": ICON, "bg": BG,
        "title": "露点温度计算器",
        "h1": "露点温度计算器",
        "h2": "露点（Magnus 公式）",
        "intro": "由气温与相对湿度，按 Magnus 公式反算露点温度 Td。",
        "desc": "露点温度计算器：输入气温与相对湿度，按 Magnus 公式求露点温度（空气冷却至饱和时的温度）。",
        "inputs": [
            {"id": "T", "label": "气温 T", "value": 25, "step": "0.5", "unit": "°C"},
            {"id": "RH", "label": "相对湿度 RH", "value": 60, "step": "1", "unit": "%", "min": "0", "max": "100"},
        ],
        "calc": """
            const T=num('T'), RH=num('RH');
            const a=17.625, b=243.04;
            const g = Math.log(Math.max(RH,1)/100) + a*T/(b+T);
            const Td = b*g/(a-g);
            ToolBox.setResult('result', dataGrid([ [Td.toFixed(2)+' °C', '露点温度 Td'] ]));
        """,
        "notes": ["Magnus 经验式，适用 0–50℃ 精度良好。", "露点越高，空气越潮湿。"],
    },
    {
        "slug": "apparent-temperature",
        "industry": "meteorology", "cat": CAT, "icon": ICON, "bg": BG,
        "title": "体感温度计算器",
        "h1": "体感温度（Steadman）计算器",
        "h2": "体感温度 AT",
        "intro": "由气温、相对湿度与风速，按 Steadman 公式估算人体体感温度。",
        "desc": "体感温度计算器：输入气温、相对湿度与风速，按 Steadman 公式估算体感温度。",
        "inputs": [
            {"id": "T", "label": "气温 T", "value": 30, "step": "0.5", "unit": "°C"},
            {"id": "RH", "label": "相对湿度 RH", "value": 70, "step": "1", "unit": "%", "min": "0", "max": "100"},
            {"id": "ws", "label": "风速 ws", "value": 2, "step": "0.5", "unit": "m/s", "min": "0"},
        ],
        "calc": """
            const T=num('T'), RH=num('RH'), ws=num('ws');
            const e = (RH/100)*6.105*Math.exp(17.27*T/(237.7+T)); // hPa
            const AT = T + 0.33*e - 0.70*ws - 4.0;
            ToolBox.setResult('result', dataGrid([ [AT.toFixed(1)+' °C', '体感温度 AT（Steadman 简化）'] ]));
        """,
        "notes": ["湿度高、风速低时体感更热；风速大时体感更冷。", "简化式忽略太阳辐射项，作近似参考。"],
    },
    {
        "slug": "wind-chill",
        "industry": "meteorology", "cat": CAT, "icon": ICON, "bg": BG,
        "title": "风寒指数计算器",
        "h1": "风寒指数（WCT）计算器",
        "h2": "风寒指数",
        "intro": "由气温与风速（km/h），按加拿大环境部 WCT 公式估算体感寒冷程度。",
        "desc": "风寒指数计算器：输入气温与风速，按 WCT 公式求风寒体感温度。",
        "inputs": [
            {"id": "T", "label": "气温 T", "value": -5, "step": "0.5", "unit": "°C"},
            {"id": "v", "label": "风速 v", "value": 20, "step": "1", "unit": "km/h", "min": "0"},
        ],
        "calc": """
            const T=num('T'), v=num('v');
            const WCT = 13.12 + 0.6215*T - 11.37*Math.pow(v,0.16) + 0.3965*T*Math.pow(v,0.16);
            ToolBox.setResult('result', dataGrid([ [WCT.toFixed(1)+' °C', '风寒指数 WCT'] ]));
        """,
        "notes": ["仅适用于气温 ≤10℃ 且风速 >4.8 km/h 的寒冷场景。"],
    },
    {
        "slug": "saturation-vapor-pressure",
        "industry": "meteorology", "cat": CAT, "icon": ICON, "bg": BG,
        "title": "饱和水汽压计算器",
        "h1": "饱和水汽压（Magnus）计算器",
        "h2": "饱和水汽压 e_s",
        "intro": "由气温，按 Magnus 公式 e_s = 6.1094·exp(17.625T/(T+243.04)) 计算饱和水汽压。",
        "desc": "饱和水汽压计算器：输入气温，按 Magnus 公式求饱和水汽压（hPa）。",
        "inputs": [
            {"id": "T", "label": "气温 T", "value": 25, "step": "0.5", "unit": "°C"},
        ],
        "calc": """
            const T=num('T');
            const es = 6.1094*Math.exp(17.625*T/(T+243.04));
            ToolBox.setResult('result', dataGrid([ [es.toFixed(2)+' hPa', '饱和水汽压 e_s'] ]));
        """,
        "notes": ["饱和水汽压随温度升高呈指数增长。"],
    },
    {
        "slug": "relative-humidity",
        "industry": "meteorology", "cat": CAT, "icon": ICON, "bg": BG,
        "title": "相对湿度反算计算器",
        "h1": "由气温与露点求相对湿度",
        "h2": "相对湿度 RH",
        "intro": "由气温与露点，按 Magnus 关系反算相对湿度。",
        "desc": "相对湿度计算器：输入气温与露点温度，反算空气相对湿度。",
        "inputs": [
            {"id": "T", "label": "气温 T", "value": 25, "step": "0.5", "unit": "°C"},
            {"id": "Td", "label": "露点 Td", "value": 16.7, "step": "0.5", "unit": "°C"},
        ],
        "calc": """
            const T=num('T'), Td=num('Td');
            const a=17.625, b=243.04;
            const RH = 100*Math.exp((a*Td/(b+Td)) - (a*T/(b+T)));
            ToolBox.setResult('result', dataGrid([ [RH.toFixed(1)+' %', '相对湿度 RH'] ]));
        """,
        "notes": ["RH=100·exp[ aTd/(b+Td) − aT/(b+T) ]，Magnus 推导。"],
    },
    {
        "slug": "absolute-humidity",
        "industry": "meteorology", "cat": CAT, "icon": ICON, "bg": BG,
        "title": "绝对湿度计算器",
        "h1": "绝对湿度计算器",
        "h2": "绝对湿度 AH",
        "intro": "由气温与相对湿度，按经验式计算单位体积空气中的水蒸气质量（g/m³）。",
        "desc": "绝对湿度计算器：输入气温与相对湿度，求绝对湿度（g/m³）。",
        "inputs": [
            {"id": "T", "label": "气温 T", "value": 25, "step": "0.5", "unit": "°C"},
            {"id": "RH", "label": "相对湿度 RH", "value": 60, "step": "1", "unit": "%", "min": "0", "max": "100"},
        ],
        "calc": """
            const T=num('T'), RH=num('RH');
            const AH = 1320.65 * (RH/100) * Math.exp(17.67*T/(T+243.5)) / (T+273.15);
            ToolBox.setResult('result', dataGrid([ [AH.toFixed(2)+' g/m³', '绝对湿度 AH'] ]));
        """,
        "notes": ["表示每立方米空气中水蒸气的质量。"],
    },
    {
        "slug": "wet-bulb-temperature",
        "industry": "meteorology", "cat": CAT, "icon": ICON, "bg": BG,
        "title": "湿球温度计算器",
        "h1": "湿球温度（Stull 经验式）计算器",
        "h2": "湿球温度 T_w",
        "intro": "由气温与相对湿度，按 Stull(2011) 经验多项式估算湿球温度，适用 5–95%RH、-20–50℃。",
        "desc": "湿球温度计算器：输入气温与相对湿度，按 Stull 经验式估算湿球温度。",
        "inputs": [
            {"id": "T", "label": "气温 T", "value": 25, "step": "0.5", "unit": "°C"},
            {"id": "RH", "label": "相对湿度 RH", "value": 60, "step": "1", "unit": "%", "min": "0", "max": "100"},
        ],
        "calc": """
            const T=num('T'), RH=num('RH');
            const Tw = T*Math.atan(0.151977*Math.sqrt(RH+8.313659))
                     + Math.atan(T+RH) - Math.atan(RH-1.676331)
                     + 0.00391838*Math.pow(RH,1.5)*Math.atan(0.023101*RH) - 4.686035;
            ToolBox.setResult('result', dataGrid([ [Tw.toFixed(2)+' °C', '湿球温度 T_w（Stull）'] ]));
        """,
        "notes": ["Stull 2011 单方程近似，免迭代，工程与气象科普常用。"],
    },
    {
        "slug": "pressure-altitude",
        "industry": "meteorology", "cat": CAT, "icon": ICON, "bg": BG,
        "title": "气压高度计算器",
        "h1": "气压高度计算器",
        "h2": "气压高度 h",
        "intro": "由气压按国际标准大气反算海拔高度：h = 44330·(1 − (P/P₀)^0.1903)。",
        "desc": "气压高度计算器：输入气压，按国际标准大气反算海拔高度（米）。",
        "inputs": [
            {"id": "P", "label": "气压 P", "value": 900, "step": "1", "unit": "hPa", "min": "0"},
            {"id": "P0", "label": "海平面气压 P₀", "value": 1013.25, "step": "1", "unit": "hPa", "min": "0"},
        ],
        "calc": """
            const P=num('P'), P0=num('P0');
            const h = 44330*(1 - Math.pow(P/P0,0.1903));
            ToolBox.setResult('result', dataGrid([ [h.toFixed(0)+' m', '海拔（气压高度）'] ]));
        """,
        "notes": ["适用于对流层；实际地形还受温度层结影响。"],
    },
    {
        "slug": "isa-temperature",
        "industry": "meteorology", "cat": CAT, "icon": ICON, "bg": BG,
        "title": "国际标准大气温度计算器",
        "h1": "国际标准大气（ISA）温度计算器",
        "h2": "ISA 温度",
        "intro": "由海拔高度按 ISA 模型求气温：对流层（≤11km）每千米降 6.5℃，平流层底部恒温。",
        "desc": "国际标准大气温度计算器：输入海拔高度，按 ISA 模型求标准气温。",
        "inputs": [
            {"id": "h", "label": "海拔高度 h", "value": 5, "step": "0.5", "unit": "km", "min": "0"},
        ],
        "calc": """
            const h=num('h');
            let T;
            if (h<=11) T = 15 - 6.5*h;
            else T = -56.5;
            ToolBox.setResult('result', dataGrid([ [T.toFixed(1)+' °C', '标准气温 T（ISA）'] ]));
        """,
        "notes": ["海平标准温 15℃，11km 处约 −56.5℃ 为对流层顶。"],
    },
    {
        "slug": "beaufort-scale",
        "industry": "meteorology", "cat": CAT, "icon": ICON, "bg": BG,
        "title": "蒲福风级计算器",
        "h1": "蒲福风力等级计算器",
        "h2": "蒲福风级",
        "intro": "由 10 米高风速（m/s）映射到蒲福风级（0–12）及名称。",
        "desc": "蒲福风级计算器：输入风速，换算为蒲福风力等级与对应名称。",
        "inputs": [
            {"id": "v", "label": "风速 v（10m 高）", "value": 10, "step": "0.5", "unit": "m/s", "min": "0"},
        ],
        "calc": """
            const v=num('v');
            const names=['无风','软风','轻风','微风','和风','清劲风','强风','疾风','大风','烈风','狂风','暴风','飓风'];
            const ub=[0.2,1.5,3.3,5.4,7.9,10.7,13.8,17.1,20.7,24.4,28.4,32.6,1e9];
            let lvl=0; for(let i=0;i<ub.length;i++){ if(v<=ub[i]){lvl=i;break;} }
            ToolBox.setResult('result', dataGrid([ [lvl+' 级', '蒲福风级'], [names[lvl], '风力名称'] ]));
        """,
        "notes": ["蒲福风级描述海面/地面风力，0 级静风、12 级飓风。"],
    },
    {
        "slug": "cloud-base-height",
        "industry": "meteorology", "cat": CAT, "icon": ICON, "bg": BG,
        "title": "云底高度估算计算器",
        "h1": "云底高度（抬升凝结高度）估算",
        "h2": "云底高度",
        "intro": "由气温与露点差，按经验规则 H ≈ (T − Td) × 125（米/℃）估算云底高度。",
        "desc": "云底高度计算器：输入气温与露点，按温差经验规则估算云底高度。",
        "inputs": [
            {"id": "T", "label": "气温 T", "value": 25, "step": "0.5", "unit": "°C"},
            {"id": "Td", "label": "露点 Td", "value": 15, "step": "0.5", "unit": "°C"},
        ],
        "calc": """
            const T=num('T'), Td=num('Td');
            const H = (T - Td) * 125;
            ToolBox.setResult('result', dataGrid([ [H.toFixed(0)+' m', '估算云底高度 H=(T−Td)×125'] ]));
        """,
        "notes": ["经验规则（约 125 m/℃），与气压、抬升率有关，作近似。"],
    },
    {
        "slug": "precipitation-rate",
        "industry": "meteorology", "cat": CAT, "icon": ICON, "bg": BG,
        "title": "降雨强度分级计算器",
        "h1": "降雨强度分级计算器",
        "h2": "降雨等级",
        "intro": "由小时降雨量（mm/h）判定小雨/中雨/大雨/暴雨/大暴雨等级。",
        "desc": "降雨强度分级计算器：输入小时降雨量，判定降雨等级。",
        "inputs": [
            {"id": "mm", "label": "小时降雨量", "value": 12, "step": "0.5", "unit": "mm/h", "min": "0"},
        ],
        "calc": """
            const mm=num('mm');
            let lv = mm<2.5?'小雨' : mm<8?'中雨' : mm<16?'大雨' : mm<50?'暴雨' : mm<100?'大暴雨':'特大暴雨';
            ToolBox.setResult('result', dataGrid([ [lv, '降雨等级（mm/h）'] ]));
        """,
        "notes": ["采用中国气象局常用分级：小雨<2.5、中雨<8、大雨<16、暴雨<50、大暴雨<100。"],
    },
    {
        "slug": "humidex",
        "industry": "meteorology", "cat": CAT, "icon": ICON, "bg": BG,
        "title": "湿热指数（Humidex）计算器",
        "h1": "湿热指数 Humidex 计算器",
        "h2": "Humidex",
        "intro": "由气温与相对湿度，先求水汽压 e，再按 Humidex = T + 0.5555·(e − 10) 计算湿热体感指数。",
        "desc": "湿热指数计算器：输入气温与相对湿度，求加拿大 Humidex 湿热体感指数。",
        "inputs": [
            {"id": "T", "label": "气温 T", "value": 30, "step": "0.5", "unit": "°C"},
            {"id": "RH", "label": "相对湿度 RH", "value": 70, "step": "1", "unit": "%", "min": "0", "max": "100"},
        ],
        "calc": """
            const T=num('T'), RH=num('RH');
            const e = (RH/100)*6.1094*Math.exp(17.625*T/(T+243.04)); // hPa
            const H = T + 0.5555*(e - 10);
            ToolBox.setResult('result', dataGrid([ [H.toFixed(1), '湿热指数 Humidex'] ]));
        """,
        "notes": ["30–39 需注意，40+ 危险，45+ 极危险（加拿大标准）。"],
    },
    {
        "slug": "wind-direction",
        "industry": "meteorology", "cat": CAT, "icon": ICON, "bg": BG,
        "title": "风向方位计算器",
        "h1": "风向（16 方位）计算器",
        "h2": "风向方位",
        "intro": "由风向角度（°）映射到 16 方位罗盘名称（如 N、NE、SSW）。",
        "desc": "风向方位计算器：输入风向角度，转换为 16 方位罗盘名称。",
        "inputs": [
            {"id": "deg", "label": "风向角（°）", "value": 225, "step": "1", "unit": "°", "min": "0", "max": "360"},
        ],
        "calc": """
            const deg=((num('deg')%360)+360)%360;
            const names=['N','NNE','NE','ENE','E','ESE','SE','SSE','S','SSW','SW','WSW','W','WNW','NW','NNW'];
            const idx = Math.round(deg/22.5)%16;
            ToolBox.setResult('result', dataGrid([ [names[idx], '16 方位（'+deg.toFixed(0)+'°）'] ]));
        """,
        "notes": ["气象风向指风的来向：225° 表示西南风（从西南吹来）。"],
    },
]


if __name__ == "__main__":
    main(TOOLS)
