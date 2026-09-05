# -*- coding: utf-8 -*-
"""
生成「高频可见工具」的英文覆盖字典 i18n/tools/_en_override.json。

策略（AI 批量预翻，零外部依赖）：
- 头部行业（it/general/finance/science/design）中、规则引擎仍回退中文的工具，
  其 slug 绝大多数为英文，直接把 slug 还原成自然英文标题（最准确的语义来源，
  非逐字翻中文），如 hex-to-text -> Hex to Text、jwt-debugger -> JWT Debugger。
- 少数占位符 slug（calc-N）按中文名语义手翻（PLACEHOLDER 表）。
- 简介(ed) 按标题中的动作词生成简洁英文描述。
产物被 _build.py 在写出 industry-*/tools.json 前覆盖 en/ed；
gen_tool_i18n_en.py 读 tools.json 即自动继承，无需单独处理。

用法：python3 scripts/gen_en_override.py
"""
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'scripts'))
from zh_en_dict import translate_name, _ZH_RUN  # noqa: E402

TOP_INDUSTRIES = None  # None = 全站；或设为 {'it','general',...} 限定头部行业
SI_PATH = os.path.join(ROOT, 'json', 'tools.json')
OUT_PATH = os.path.join(ROOT, 'i18n', 'tools', '_en_override.json')

ACRONYMS = {
    'http': 'HTTP', 'json': 'JSON', 'md5': 'MD5', 'sha': 'SHA', 'uuid': 'UUID',
    'xml': 'XML', 'html': 'HTML', 'css': 'CSS', 'yaml': 'YAML', 'regex': 'Regex',
    'rot': 'ROT', 'jwt': 'JWT', 'og': 'OG', 'ast': 'AST', 'ascii': 'ASCII',
    'bip39': 'BIP39', 'sql': 'SQL', 'uri': 'URI', 'url': 'URL', 'api': 'API',
    'tcp': 'TCP', 'ip': 'IP', 'qr': 'QR', 'cli': 'CLI', 'csv': 'CSV', 'svg': 'SVG',
    'png': 'PNG', 'pdf': 'PDF', 'dom': 'DOM', 'guid': 'GUID', 'rsa': 'RSA',
    'aes': 'AES', 'des': 'DES', 'xor': 'XOR', 'crc': 'CRC', 'base64': 'Base64',
    'xss': 'XSS', 'npm': 'npm', 'gpu': 'GPU', 'cpu': 'CPU', 'ram': 'RAM',
    'io': 'I/O', 'ui': 'UI', 'db': 'DB', 'id': 'ID', 'oauth': 'OAuth', 'tls': 'TLS',
    'ssh': 'SSH', 'dns': 'DNS', 'mac': 'MAC', 'iso': 'ISO', 'utf8': 'UTF-8',
    'utf': 'UTF',     'rpc': 'RPC', 'grpc': 'gRPC', 'pki': 'PKI', 'tls': 'TLS',
    'lmt': 'LMT', 'lmt d': 'LMTD', 'xmpp': 'XMPP', 'oid': 'OID',
    'typescript': 'TypeScript', 'javascript': 'JavaScript', 'sqlite': 'SQLite',
    'less': 'Less', 'react': 'React', 'vue': 'Vue', 'node': 'Node', 'docker': 'Docker',
    'kubernetes': 'Kubernetes', 'graphql': 'GraphQL', 'webpack': 'Webpack',
    'babel': 'Babel', 'eslint': 'ESLint', 'prettier': 'Prettier', 'postgres': 'PostgreSQL',
    'mysql': 'MySQL', 'mongodb': 'MongoDB', 'redis': 'Redis', 'nginx': 'Nginx',
    'linux': 'Linux', 'macos': 'macOS', 'windows': 'Windows', 'android': 'Android',
    'ios': 'iOS', 'spring': 'Spring', 'django': 'Django', 'flask': 'Flask',
    'redis': 'Redis', 'kafka': 'Kafka', 'tensorflow': 'TensorFlow', 'pytorch': 'PyTorch',
    'numpy': 'NumPy', 'pandas': 'Pandas', 'matplotlib': 'Matplotlib', 'opencv': 'OpenCV',
}
LOWER = {'to', 'and', 'or', 'the', 'a', 'an', 'of', 'for', 'in', 'on', 'with',
         'by', 'from', 'into', 'vs'}

# 常见英文工具词（用于区分「真英文 slug」与「拼音 slug」）
ENGLISH_TOKENS = {
    'speech', 'text', 'char', 'encoder', 'decoder', 'shoe', 'size', 'chord',
    'hashtag', 'chiller', 'efficiency', 'shutter', 'speed', 'confined', 'space',
    'rescue', 'eustachian', 'tube', 'control', 'chart', 'converter', 'generator',
    'calculator', 'frequency', 'torque', 'fuel', 'oil', 'change', 'stretch',
    'growth', 'curve', 'schedule', 'echo', 'audio', 'blueprint', 'tool', 'label',
    'vaccine', 'archive', 'recommender', 'face', 'shape', 'captcha', 'chinese',
    'number', 'words', 'staff', 'overdue', 'fine', 'currency', 'exchange', 'area',
    'shared', 'convert', 'liquefaction', 'time', 'epoch', 'prime', 'check',
    'quantization', 'ratio', 'value', 'best', 'steps', 'per', 'percent', 'reach',
    'shelf', 'capacity', 'life', 'machinery', 'wallpaper', 'quantity', 'oxygen',
    'machine', 'fish', 'weight', 'chest', 'compression', 'depth', 'analysis',
    'strength', 'market', 'share', 'spring', 'design', 'shaft', 'torsion', 'earth',
    'geology', 'seismic', 'pollution', 'environment', 'laser', 'welding',
    'pressure', 'power', 'source', 'logic', 'device', 'system', 'basketball',
    'badminton', 'swimming', 'volleyball', 'tennis', 'ping', 'pong', 'table',
    'marketing', 'short', 'link', 'stopwatch', 'irrigation', 'choreography',
    'timeline', 'ten', 'questions', 'hazard', 'checklist', 'wifi', 'password',
    'show', 'english', 'vocabulary', 'word', 'polisher', 'shuffle', 'interval',
    'distance', 'exposure', 'triangle', 'chi', 'square', 'test', 'sheet', 'calc',
    'motion', 'response', 'lung', 'cancer', 'tnm', 'anemia', 'classification',
    'fund', 'loan', 'grace', 'score', 'rule', 'resistor', 'color', 'code', 'css',
    'box', 'shadow', 'age', 'activity', 'flow', 'cone', 'volume', 'voltage',
    'divider', 'rope', 'buffer', 'ph', 'simulator', 'temp', 'lookup', 'stratum',
    'correlation', 'location', 'qr', 'angle', 'twist', 'blast', 'hole', 'spacing',
    'rater', 'resistance', 'concentration', 'cost', 'formatter', 'viewer',
    'validator', 'checker', 'comparator', 'parser', 'analyzer', 'compiler',
    'runner', 'debugger', 'obfuscator', 'minify', 'picker', 'selector', 'diff',
    'maker', 'creator', 'pvalue', 'naming', 'name', 'schedule', 'reminder',
    'counter', 'meter', 'gauge', 'index', 'rate', 'scale', 'estimator', 'plot',
    'graph', 'model', 'predictor', 'filter', 'sorter', 'merger', 'splitter',
    'extractor', 'recorder', 'player', 'editor', 'monitor', 'alarm', 'scanner',
    'diagnoser', 'identifier', 'classifier', 'screener', 'regulator', 'adapter',
    'splitter', 'breaker', 'searcher', 'finder', 'mapper', 'builder', 'writer',
    'reader', 'converter', 'transformer', 'solver', 'optimizer', 'planner',
    'tracker', 'logger', 'timer', 'clock', 'calendar', 'quiz', 'game', 'sim',
    'widget', 'panel', 'board', 'matrix', 'table', 'list', 'grid', 'map',
    'hash', 'json', 'xml', 'csv', 'yaml', 'toml', 'ini', 'config', 'setting',
    'theme', 'style', 'font', 'image', 'video', 'audio', 'file', 'data', 'db',
    'api', 'sdk', 'cli', 'ui', 'ux', 'web', 'app', 'bot', 'ai', 'ml', 'dl',
    'tag', 'tags', 'note', 'notes', 'doc', 'docs', 'readme', 'guide', 'tutorial',
}

_PINYIN_MARK = re.compile(r'(zh|ch|sh|ng|iao|iang|uang|iong|ü|ue|uan|uen)')
# 拼音专属复韵母/组合：英文词中几乎不出现，命中即可确信该音节为拼音。
# 注意：不含 van（advanced/advantage 含 van，但汉语拼音无 van）、不含 uen
# （influencer/frequent 含 uen，而汉语拼音 uen 写作 un，从不存在 uen 书写）。
_PINYIN_EXCLUSIVE = re.compile(r'(iao|iang|uang|iong|ü)')


def is_pinyin_slug(slug):
    """仅在高度确信 slug 为拼音时才返回 True（保守策略，避免误伤英文 slug）。

    判定为拼音的强信号：
      1) 无连字符的长串（>5 字符）且含拼音标记 -> 经典拼音连写（tanhuangsheji）。
      2) 带连字符 slug 中，任一 part 含拼音专属复韵母（iao/iang/uang/iong/ü/uen/van）。
    其余（含 ng/ing/zh/ch/sh/ue/uan 但非上述的英文 slug，如 pinyin-typing-practice、
    focal-length-equivalent、wedding-flowers）一律当作英文，由 slug_to_name 直译。
    """
    if not _PINYIN_MARK.search(slug):
        return False
    # 整体即为已知英文词/缩写（含无连字符长英文词，如 stopwatch/stretch/torque），直接判英文
    if slug in ACRONYMS or slug in ENGLISH_TOKENS:
        return False
    parts = slug.split('-')
    # 1) 无连字符长串 -> 拼音连写
    if len(parts) == 1 and len(slug) > 5:
        return True
    # 2) 任一 part 含拼音专属复韵母 -> 拼音
    for tk in parts:
        if tk in ACRONYMS or tk in ENGLISH_TOKENS:
            continue
        if _PINYIN_EXCLUSIVE.search(tk):
            return True
    return False

# 占位符 slug（calc-N）按中文名 + 行业上下文逐条人工翻译。
# 键为 (行业, basename)，值可为字符串(en) 或 {en,ed} 字典。
# 注意：calc-N 的 basename 在数十个行业间复用（如 calc-1 同时是 Base64/自由落体/增值税…），
# 必须用 (行业, basename) 精确匹配，绝不可用 slug-only 键（会导致跨行业错配）。
PLACEHOLDER_KEY = {
    ('accounting', 'calc-1'): {'en': 'VAT Calculator', 'ed': 'Compute Chinese VAT payable online, free and accurate.'},
    ('auto-beauty', 'calc-1'): {'en': 'Coating / Waxing Cycle Calculator', 'ed': 'Plan car-detailing coating and waxing intervals.'},
    ('automotive', 'calc-1'): {'en': '0-100 km/h Acceleration Estimator', 'ed': 'Estimate a vehicle 0-100 km/h acceleration time.'},
    ('beauty', 'calc-1'): {'en': 'Skin Type Test', 'ed': 'Identify your skin type and get basic care advice via a quick quiz.'},
    ('cardiology', 'calc-1'): {'en': 'Hypertension JNC Grading & Risk Stratification', 'ed': 'Grade blood pressure by JNC 7 and stratify cardiovascular risk.'},
    ('civil', 'calc-1'): {'en': 'Concrete Mix Ratio Calculator', 'ed': 'Compute concrete mix proportions for civil works.'},
    ('construction', 'calc-1'): {'en': 'Scaffold Load Capacity Calculator', 'ed': 'Estimate load capacity of coupler-type steel scaffolds.'},
    ('data', 'calc-1'): {'en': 'CSV to JSON Converter', 'ed': 'Convert CSV data to a JSON array locally in your browser.'},
    ('dentistry', 'calc-1'): {'en': 'DMFT Caries Index', 'ed': 'Record decayed, missing and filled permanent teeth (DMFT).'},
    ('dermatology', 'calc-1'): {'en': 'Burn Area (Rule of Nines) Calculator', 'ed': 'Estimate adult total body surface area (TBSA) burned by the Rule of Nines.'},
    ('electrical', 'calc-1'): {'en': 'Cable Current Carrying Capacity Calculator', 'ed': 'Estimate cable ampacity by conductor and cross-section (IEC 60364).'},
    ('encode', 'calc-1'): {'en': 'Base64 Encode / Decode', 'ed': 'Encode and decode Base64 online, free and secure.'},
    ('endocrinology', 'calc-1'): {'en': 'HOMA-IR Insulin Resistance Index', 'ed': 'Compute HOMA-IR from fasting glucose and insulin.'},
    ('ent', 'calc-1'): {'en': 'Rhinitis Symptom Score (TNSS)', 'ed': 'Total Nasal Symptom Score (TNSS) for rhinitis.'},
    ('fire', 'calc-1'): {'en': 'Fire Hose Solid Stream Calculator', 'ed': 'Compute required fire-hose solid stream reach.'},
    ('gastroenterology', 'calc-1'): {'en': 'Child-Pugh Liver Function Score', 'ed': 'Assess liver reserve and surgical risk in cirrhosis (Child-Pugh).'},
    ('geology', 'calc-1'): {'en': 'Rock Quality Designation (RQD) Calculator', 'ed': 'Compute rock quality designation (RQD).'},
    ('health', 'calc-1'): {'en': 'Daily Water Intake Calculator', 'ed': 'Estimate daily water intake from weight, exercise and climate.'},
    ('hematology', 'calc-1'): {'en': 'Anemia MCV / RDW Classification', 'ed': 'Classify anemia by MCV and RDW.'},
    ('hydraulic', 'calc-1'): {'en': 'Pipe Hydraulics Calculator (Velocity / Pressure Drop)', 'ed': 'Compute pipe flow velocity and pressure drop (Darcy-Weisbach).'},
    ('insurance', 'calc-1'): {'en': 'Premium Waiver Calculator', 'ed': 'Estimate premium waiver benefit for insurance.'},
    ('it', 'calc-1'): {'en': 'File Size Unit Converter', 'ed': 'Convert file sizes between decimal (SI) and binary (IEC) units.'},
    ('language', 'calc-1'): {'en': 'English Vocabulary Size Estimator', 'ed': 'Estimate your English vocabulary size.'},
    ('marketing', 'calc-1'): {'en': 'Ad ROI Calculator', 'ed': 'Compute return on advertising investment.'},
    ('math', 'calc-1'): {'en': 'Percentage Calculator', 'ed': 'Compute the four common percentage operations.'},
    ('mechanical', 'calc-1'): {'en': 'Belt Drive Calculator', 'ed': 'Compute V-belt / flat-belt ratio and belt speed.'},
    ('metallurgy', 'calc-1'): {'en': 'Alloy Composition Converter', 'ed': 'Convert target alloy mass and element contents to raw material amounts.'},
    ('mining', 'calc-1'): {'en': 'Blasting Charge Calculator', 'ed': 'Estimate per-hole charge by volume or Langefors formula.'},
    ('nephrology', 'calc-1'): {'en': 'eGFR Calculator (CKD-EPI)', 'ed': 'Estimate glomerular filtration rate with CKD-EPI.'},
    ('neurology', 'calc-1'): {'en': 'NIHSS Stroke Scale', 'ed': 'National Institutes of Health Stroke Scale (NIHSS) score.'},
    ('nutrition', 'calc-1'): {'en': 'Daily Nutrient Requirement Calculator', 'ed': 'Estimate daily calories and macronutrients by body data and goal.'},
    ('ophthalmology', 'calc-1'): {'en': 'IOP Correction (CCT) Calculator', 'ed': 'Correct intraocular pressure for corneal thickness.'},
    ('packaging', 'calc-1'): {'en': 'Shipping Carton Dimensions Calculator', 'ed': 'Compute outer carton dimensions for packaging.'},
    ('procurement', 'calc-1'): {'en': 'Economic Order Quantity (EOQ) Calculator', 'ed': 'Find the optimal order quantity (EOQ).'},
    ('psychiatry', 'calc-1'): {'en': 'PHQ-9 Depression Screening', 'ed': 'Past-2-week depression screening (PHQ-9).'},
    ('pulmonology', 'calc-1'): {'en': 'Oxygenation Index (PaO2/FiO2) Calculator', 'ed': 'Compute the PaO2/FiO2 oxygenation index.'},
    ('realestate', 'calc-1'): {'en': 'Mortgage Equal Installment vs Principal Comparison', 'ed': 'Compare equal-installment and equal-principal mortgage repayment.'},
    ('sales', 'calc-1'): {'en': 'Sales Commission Calculator', 'ed': 'Compute sales commission.'},
    ('science', 'calc-1'): {'en': 'Free Fall Motion Calculator', 'ed': 'Solve free-fall time, velocity and distance under gravity.'},
    ('securities', 'calc-1'): {'en': 'Stock Profit / Loss Calculator', 'ed': 'Compute stock trading profit and loss.'},
    ('startup', 'calc-1'): {'en': 'Startup Cost Estimator', 'ed': 'Estimate your startup costs.'},
    ('steel', 'calc-1'): {'en': 'Steel Weld Strength Calculator', 'ed': 'Compute fillet weld strength per GB 50017.'},
    ('surveying', 'calc-1'): {'en': 'Leveling Adjustment Calculator', 'ed': 'Adjust differential leveling observations.'},
    ('text', 'calc-1'): {'en': 'Text Diff Compare', 'ed': 'Compare two texts line by line and highlight changes.'},
    ('urology', 'calc-1'): {'en': 'IPSS Prostate Symptom Score', 'ed': 'International Prostate Symptom Score (IPSS).'},
    ('welding', 'calc-1'): {'en': 'Welding Current Selector', 'ed': 'Select welding current by electrode, thickness and position.'},
    ('accounting', 'calc-2'): {'en': 'Corporate Income Tax Prepayment Calculator', 'ed': 'Estimate quarterly corporate income tax prepayment.'},
    ('agriculture', 'calc-2'): {'en': 'Planting Density Calculator (Spacing x Row)', 'ed': 'Compute planting density and seedling count from spacing and area.'},
    ('automotive', 'calc-2'): {'en': 'Engine Power / Torque Converter', 'ed': 'Convert engine power and torque.'},
    ('beauty', 'calc-2'): {'en': 'Foundation Shade Matcher', 'ed': 'Match foundation shade to your skin undertone.'},
    ('cardiology', 'calc-2'): {'en': 'Atrial Fibrillation Stroke Risk (CHA2DS2-VASc)', 'ed': 'Estimate stroke/thromboembolism risk in non-valvular AF.'},
    ('civil', 'calc-2'): {'en': 'Rebar Cutting Length Calculator', 'ed': 'Compute rebar cutting length from bends and hook.'},
    ('data', 'calc-2'): {'en': 'JSON Formatter', 'ed': 'Validate, format and minify JSON locally.'},
    ('edu', 'calc-2'): {'en': 'Z-Score (Standard Score) Calculator', 'ed': 'Compute the z-score of a value in a dataset.'},
    ('electrical', 'calc-2'): {'en': 'Three-Phase Power Calculator', 'ed': 'Compute active and reactive three-phase power.'},
    ('encode', 'calc-2'): {'en': 'URL Encode / Decode', 'ed': 'Encode and decode URLs online, free and secure.'},
    ('finance', 'calc-2'): {'en': 'IRR (Internal Rate of Return) Calculator', 'ed': 'Compute the internal rate of return (IRR).'},
    ('fire', 'calc-2'): {'en': 'Fire Load Calculator', 'ed': 'Estimate fire load for fire safety.'},
    ('fitness', 'calc-2'): {'en': 'BMR (Basal Metabolic Rate) Calculator', 'ed': 'Estimate basal metabolic rate (Mifflin-St Jeor).'},
    ('health', 'calc-2'): {'en': 'Sleep Quality Score', 'ed': 'Assess sleep quality from duration and disruptions.'},
    ('hydraulic', 'calc-2'): {'en': 'Pump Head Calculator', 'ed': 'Compute pump head from suction and discharge geometry.'},
    ('it', 'calc-2'): {'en': 'Number Base Converter (IT)', 'ed': 'Convert numbers between bases 2-36.'},
    ('language', 'calc-2'): {'en': 'Reading Speed Test', 'ed': 'Measure your reading speed.'},
    ('math', 'calc-2'): {'en': 'Ratio Calculator', 'ed': 'Solve for an unknown term in a proportion.'},
    ('mechanical', 'calc-2'): {'en': 'Chain Drive Calculator', 'ed': 'Compute roller-chain ratio, speed and links.'},
    ('nutrition', 'calc-2'): {'en': 'Food Calorie Calculator', 'ed': 'Compute calories of a meal from common foods or macros.'},
    ('packaging', 'calc-2'): {'en': 'Cushioning Material Thickness Calculator', 'ed': 'Compute cushioning thickness for packaging.'},
    ('realestate', 'calc-2'): {'en': 'Rental Yield Calculator', 'ed': 'Compute rental return on property.'},
    ('science', 'calc-2'): {'en': 'Ideal Gas Law Calculator (PV = nRT)', 'ed': 'Compute pressure, volume, temperature or moles of an ideal gas.'},
    ('agriculture', 'calc-3'): {'en': 'Continuous Cropping Obstacle Index', 'ed': 'Estimate continuous-cropping obstacle index from yield comparison.'},
    ('automotive', 'calc-3'): {'en': 'Tire Pressure Converter', 'ed': 'Convert tire pressure units (bar / psi / kPa).'},
    ('cardiology', 'calc-3'): {'en': 'STEMI TIMI Risk Score', 'ed': '30-day mortality risk in STEMI (TIMI).'},
    ('edu', 'calc-3'): {'en': 'Study Schedule Planner', 'ed': 'Plan study time allocation efficiently.'},
    ('finance', 'calc-3'): {'en': 'NPV (Net Present Value) Calculator', 'ed': 'Compute net present value (NPV).'},
    ('fire', 'calc-3'): {'en': 'Evacuation Time Calculator', 'ed': 'Estimate evacuation time for fire safety.'},
    ('fitness', 'calc-3'): {'en': 'Body Fat Calculator (Navy Method)', 'ed': 'Estimate body fat percentage by the US Navy formula.'},
    ('health', 'calc-3'): {'en': 'Screen Time Assessment', 'ed': 'Assess daily screen time and get health tips.'},
    ('hydraulic', 'calc-3'): {'en': 'Pipe Friction Head Loss Calculator', 'ed': 'Compute friction head loss along a pipe.'},
    ('it', 'calc-3'): {'en': 'Color Value Converter (HEX / RGB / HSL)', 'ed': 'Convert colors between HEX, RGB and HSL with live preview.'},
    ('math', 'calc-3'): {'en': 'Pythagorean Theorem Calculator', 'ed': 'Compute sides of a right triangle (a^2 + b^2 = c^2).'},
    ('nutrition', 'calc-3'): {'en': 'Macronutrient Ratio Calculator', 'ed': 'Compute grams and calories of carbs, protein and fat from target ratio.'},
    ('agriculture', 'calc-4'): {'en': 'Greenhouse Film Rolling Time Advisor', 'ed': 'Advise greenhouse film rolling time by temperature trend.'},
    ('automotive', 'calc-4'): {'en': 'Trailer Ball Load Calculator', 'ed': 'Compute trailer ball hitch load.'},
    ('edu', 'calc-4'): {'en': 'Exam Score Target Calculator', 'ed': 'Find the score needed to hit your grade target.'},
    ('finance', 'calc-4'): {'en': 'Loan Monthly Payment Calculator', 'ed': 'Compute monthly loan payment.'},
    ('fire', 'calc-4'): {'en': 'Fire Extinguisher Layout Calculator', 'ed': 'Plan fire extinguisher placement for emergency response.'},
    ('fitness', 'calc-4'): {'en': '1RM (One-Rep Max) Estimator', 'ed': 'Estimate one-rep max from weight and reps.'},
    ('hydraulic', 'calc-4'): {'en': 'Orifice Flow Calculator', 'ed': 'Compute discharge through an orifice.'},
    ('it', 'calc-4'): {'en': 'CSS Unit Converter (px / em / rem / pt / %)', 'ed': 'Convert between CSS length units.'},
    ('math', 'calc-4'): {'en': 'Circle Area / Circumference Calculator', 'ed': 'Compute area and circumference of a circle.'},
    ('science', 'calc-4'): {'en': 'Density / Mass / Volume Converter', 'ed': 'Convert density, mass and volume (rho = m / V).'},
    ('transport', 'calc-4'): {'en': 'Traffic Violation Fine Calculator', 'ed': 'Estimate traffic violation fines.'},
    ('agriculture', 'calc-5'): {'en': 'Greenhouse Ventilation Calculator', 'ed': 'Compute greenhouse ventilation rate from heat balance.'},
    ('automotive', 'calc-5'): {'en': 'Braking Deceleration Calculator', 'ed': 'Compute vehicle braking deceleration.'},
    ('construction', 'calc-5'): {'en': 'Timber Volume Calculator (Log / Lumber)', 'ed': 'Compute volume of logs and lumber (GB 4814).'},
    ('finance', 'calc-5'): {'en': 'ROI (Return on Investment) Calculator', 'ed': 'Compute return on investment (ROI).'},
    ('fitness', 'calc-5'): {'en': 'Daily Protein Requirement Calculator', 'ed': 'Estimate daily protein intake by weight and goal.'},
    ('hydraulic', 'calc-5'): {'en': 'Siphon Height Calculator', 'ed': 'Compute maximum siphon height.'},
    ('it', 'calc-5'): {'en': 'String Length Counter', 'ed': 'Count characters, bytes, lines, words and spaces.'},
    ('science', 'calc-5'): {'en': 'Speed / Distance / Time Calculator', 'ed': 'Compute speed, distance or time in kinematics.'},
    ('agriculture', 'calc-6'): {'en': 'Livestock Stocking Capacity Estimator', 'ed': 'Estimate barn capacity and annual off-take.'},
    ('construction', 'calc-6'): {'en': 'Shading Coefficient Calculator', 'ed': 'Compute shading coefficient from overhang geometry and orientation.'},
    ('it', 'calc-6'): {'en': 'Regex Tester', 'ed': 'Test regular expressions with flags and group capture.'},
    ('agriculture', 'calc-7'): {'en': 'Fertigation (Drip) Ratio Adjuster', 'ed': 'Tune nutrient-to-water ratios for fertigation drip systems.'},
    ('it', 'calc-7'): {'en': 'JSON Path Extractor', 'ed': 'Extract values from JSON by dot-path (e.g. user.name).'},
    ('agriculture', 'calc-8'): {'en': 'Soil pH Adjustment Calculator', 'ed': 'Find soil amendment to reach target pH.'},
    ('it', 'calc-8'): {'en': 'JWT Decoder', 'ed': 'Decode JWT header and payload in your browser.'},
    ('legal', 'calc-8'): {'en': 'Year-End Bonus Income Tax Calculator', 'ed': 'Compare separate vs consolidated taxation for year-end bonuses.'},
    ('it', 'calc-10'): {'en': 'Hash Value Generator', 'ed': 'Compute MD5, SHA-1, SHA-256 hashes locally.'},
    ('agriculture', 'calc-11'): {'en': 'Farm Machinery Work Efficiency Comparison', 'ed': 'Compare field efficiency across machines or parameters.'},
    ('agriculture', 'calc-12'): {'en': 'Irrigation Water Requirement Estimator', 'ed': 'Estimate water for one irrigation by crop schedule.'},
    ('psychology', 'calc-12'): {'en': 'Happiness Index Calculator', 'ed': 'Assess subjective well-being across life, health, relationships and work.'},
    ('agriculture', 'calc-13'): {'en': 'Farm Machinery Fuel Consumption Estimator', 'ed': 'Estimate farm machinery fuel use by engine parameters.'},
    ('general', 'calc-13'): {'en': 'Date Difference Calculator (Workdays / Calendar Days)', 'ed': 'Compute calendar and workday differences between two dates.'},
    ('agriculture', 'calc-14'): {'en': 'Crop Water Requirement Calculator (FAO Kc)', 'ed': 'Estimate crop water demand by FAO crop coefficient method.'},
    ('general', 'calc-14'): {'en': 'Age Calculator (Exact to Day)', 'ed': 'Compute exact age in years, months and days.'},
    ('agriculture', 'calc-15'): {'en': 'Sowing Date Calculator', 'ed': 'Back-calculate sowing date from target harvest.'},
    ('procurement', 'calc-15'): {'en': 'Economic Order Quantity (EOQ) Calculator', 'ed': 'Find optimal order quantity and total cost (EOQ).'},
    ('legal', 'calc-16'): {'en': 'Limitation Period (Statute of Limitations) Calculator', 'ed': 'Compute expiration of general civil limitation under Civil Code Art. 188.'},
    ('legal', 'calc-17'): {'en': 'IP Protection Term Calculator', 'ed': 'Compute terms for invention patents, utility models, designs and trademarks.'},
    ('general', 'calc-21'): {'en': 'Lottery After-Tax Prize Calculator', 'ed': 'Compute windfall tax and net lottery prize.'},
    ('geology', 'calc-25'): {'en': 'Earthquake Epicentral Distance Calculator', 'ed': 'Estimate epicentral distance from P-S wave time difference.'},
    ('hydraulic', 'calc-26'): {'en': 'Open Channel Uniform Flow Calculator (Manning\'s)', 'ed': 'Compute uniform flow in open channels (Manning\'s formula).'},
    ('securities', 'calc-29'): {'en': 'Bollinger Bands Calculator (Upper / Lower / Std Dev)', 'ed': 'Compute Bollinger Bands: midline, bands, %B and bandwidth.'},
    ('securities', 'calc-30'): {'en': 'Maximum Drawdown Calculator', 'ed': 'Analyze portfolio maximum drawdown.'},
    ('medical', 'calc-34'): {'en': 'Daily Energy Requirement (RER) Calculator', 'ed': 'Estimate resting energy requirement (RER).'},
    ('agriculture', 'calc-36'): {'en': 'Crop Water Requirement (ET / Evapotranspiration) Calculator', 'ed': 'Estimate crop water demand by FAO evapotranspiration (ET).'},
    ('agriculture', 'calc-37'): {'en': 'Daily Light Integral (DLI) Calculator', 'ed': 'Compute cumulative light exposure (DLI) for crops.'},
    ('agriculture', 'calc-38'): {'en': 'Irrigation Uniformity (Christiansen\'s Coefficient) Calculator', 'ed': 'Evaluate sprinkler/drip uniformity (CUC).'},
    ('fishery', 'calc-39'): {'en': 'Aquafeed Feeding Rate Calculator (Percent)', 'ed': 'Compute aquaculture feeding rate as body-weight percentage.'},
    ('tcm-chemistry', 'calc-44'): {'en': 'Extraction Stage Calculator (Distribution Coefficient)', 'ed': 'Compute liquid-liquid extraction stages from distribution coefficient.'},
    ('optical', 'calc-47'): {'en': 'Aspheric Surface (Spherical Aberration) Calculator', 'ed': 'Compute spherical-aberration correction for aspheric surfaces.'},
    ('pulmonology', 'calc-48'): {'en': 'Oxygenation Index (PaO2/FiO2) Calculator', 'ed': 'Compute PaO2/FiO2 oxygenation index.'},
    ('obstetrics', 'calc-50'): {'en': 'Postpartum Hemorrhage (Estimated Blood Loss) Calculator', 'ed': 'Estimate maternal blood volume and blood loss (Nadler\'s formula).'},
    ('cosmetic-derm', 'calc-51'): {'en': 'Sunscreen SPF / PA Calculator', 'ed': 'Compute SPF and PA from UVB and UVA blocking rates.'},
    ('transport', 'calc-53'): {'en': 'Traffic Volume (Peak Hour Factor) Calculator', 'ed': 'Compute traffic volume and peak hour factor (PHF).'},
    ('hydraulic', 'calc-54'): {'en': 'Sluice Gate Open/Close Force Calculator', 'ed': 'Estimate opening/closing forces for sluice gate hoists.'},
    ('meteorology', 'calc-55'): {'en': 'Moon Illumination Calculator', 'ed': 'Compute moon illumination and phase name from date or age.'},
    ('forestry', 'calc-57'): {'en': 'Forest Canopy Closure Calculator', 'ed': 'Estimate canopy closure by point sampling.'},
    ('livestock', 'calc-58'): {'en': 'Pedigree Inbreeding Coefficient Calculator', 'ed': 'Compute inbreeding coefficient from pedigree.'},
    ('nutrition', 'calc-60'): {'en': 'Weight-Loss Calorie Deficit Calculator', 'ed': 'Plan calorie deficit for weight loss (Mifflin-St Jeor).'},
    ('sports', 'calc-61'): {'en': 'Energy Expenditure Calculator (Sports)', 'ed': 'Estimate calories burned during sport.'},
    ('sports', 'calc-62'): {'en': 'Baseball Batting Average / ERA Calculator', 'ed': 'Compute batting average and earned run average (ERA).'},
    ('electronics', 'calc-63'): {'en': 'PCB Trace Width & Current Calculator (IPC-2221)', 'ed': 'Find PCB trace width for a given current (IPC-2221).'},
    ('machinery', 'calc-64'): {'en': 'Assembly Clearance / Interference Calculator', 'ed': 'Compute fit clearance or interference.'},
    ('dyeing', 'calc-65'): {'en': 'Dye Uptake & Fixation Rate Calculator', 'ed': 'Compute dye uptake and fixation rates.'},
    ('packaging', 'calc-66'): {'en': 'Carton Compression & Stacking Load Calculator', 'ed': 'Estimate box compression and stacking load (McKee formula).'},
    ('gas', 'calc-68'): {'en': 'Liquefied Gas Vaporization Heat Calculator', 'ed': 'Compute vaporization heat for LPG, LNG, liquid ammonia or chlorine.'},
    ('realestate', 'calc-70'): {'en': 'Land Base Price & Floor Price Calculator', 'ed': 'Estimate land base and floor-area price.'},
    ('automotive', 'calc-72'): {'en': 'Engine Displacement & Compression Ratio Calculator', 'ed': 'Compute displacement and compression ratio from bore, stroke, cylinders.'},
    ('usedcar', 'calc-73'): {'en': 'Used Car Value Retention / Residual Calculator', 'ed': 'Estimate used-car retention and residual value.'},
    ('shipping', 'calc-76'): {'en': 'Vessel Displacement & Deadweight Calculator', 'ed': 'Compute displacement and DWT from dimensions and draft.'},
    ('logistics', 'calc-78'): {'en': 'Freight Rate Calculator (Chargeable Weight & Surcharges)', 'ed': 'Compute shipping rates by chargeable weight plus surcharges.'},
    ('ecommerce', 'calc-79'): {'en': 'Growth Rate Calculator (YoY / MoM)', 'ed': 'Compute year-over-year and month-over-month growth.'},
    ('hr', 'calc-81'): {'en': 'Employee Referral Metrics Calculator', 'ed': 'Estimate referral incentives, process and hiring impact.'},
    ('meteorology', 'calc-84'): {'en': 'Solar Radiation Calculator', 'ed': 'Estimate solar radiation (FAO method).'},
    ('surveying', 'calc-86'): {'en': 'Road Alignment / Cross-Section / Setting-Out Calculator', 'ed': 'Compute road centerline, cross-sections and setting-out.'},
    ('geology', 'calc-87'): {'en': 'Geochemical Anomaly Contrast Calculator', 'ed': 'Compute anomaly contrast from element background values.'},
    ('metallurgy', 'calc-88'): {'en': 'Furnace Charge Mix Calculator', 'ed': 'Compute charge proportions for iron or steel melting.'},
    ('machinery', 'calc-89'): {'en': 'Clutch Torque Calculator', 'ed': 'Compute clutch torque from friction-plate geometry.'},
    ('realestate', 'calc-93'): {'en': 'Comparative Sales Approach Calculator (Adjustments)', 'ed': 'Value property by sales comparison with adjustments.'},
    ('general', 'calc-94'): {'en': 'Construction Cost Adjustment Calculator', 'ed': 'Adjust project cost by material, labor and equipment indices.'},
    ('legal', 'calc-96'): {'en': 'Contract Breach / Penalty Calculator', 'ed': 'Estimate contract breach liability and liquidated damages.'},
    ('research', 'calc-97'): {'en': 'Sample Size / Quota / Margin of Error Calculator', 'ed': 'Compute survey sample size, quotas and margin of error.'},
    ('general', 'calc-196'): {'en': 'Pipe Insulation Thickness Calculator', 'ed': 'Compute insulation thickness to control surface temperature.'},
    ('general', 'calc-197'): {'en': 'Heat Exchanger Sizing Calculator (LMTD)', 'ed': 'Size a heat exchanger by LMTD method.'},
    ('general', 'calc-200'): {'en': 'Motor Sizing Calculator', 'ed': 'Compute required motor power from load and efficiency.'},
    ('general', 'calc-203'): {'en': 'Mold Fit Calculator (ISO 286)', 'ed': 'Compute mold fits per ISO 286 (GB/T).'},
    ('general', 'calc-204'): {'en': 'Formwork Support Spacing Calculator', 'ed': 'Compute formwork support spacing by bearing-area method.'},
    ('general', 'calc-205'): {'en': 'Scaffold Steel Quantity Calculator', 'ed': 'Compute steel quantity for double-row coupler scaffolds.'},
    ('general', 'calc-206'): {'en': 'Scaffold Safety Verification', 'ed': 'Verify single-standard coupler scaffold safety under load.'},
    # ===== 拼音 slug 工具逐条人工翻译（规则引擎与 slug 直译均失败，强制覆盖）=====
    ('livestock', 'yufeirizengzhong-liaoroubiquxian'): {'en': 'Fattening Daily Gain / Feed Conversion Ratio Curve', 'ed': 'Evaluate growth performance (daily gain and FCR) for cattle, pigs and sheep during fattening.'},
    ('science', 'yiyuanercifangchengqiujie'): {'en': 'Quadratic Equation Solver', 'ed': 'Solve quadratic equations (ax^2+bx+c=0) online, step by step.'},
    ('ballistics', 'rangefinder'): {'en': 'Optical Rangefinder Distance Estimator', 'ed': 'Estimate distance from known target size and viewing angle, with parallax and mil-dot ranging.'},
    ('general', 'shachepiangenghuanzhouqi'): {'en': 'Brake Pad Replacement Interval Calculator', 'ed': 'Estimate brake pad replacement interval from current, new and wear-rate thickness.'},
    ('fishery', 'zengyangjikaiqishichang-rongyangxiajiangmoxing'): {'en': 'Aerator Run-Time Estimator (Dissolved Oxygen Model)', 'ed': 'Estimate aerator operating duration using a dissolved-oxygen decline model.'},
    ('sports', 'shejiansanbubanjing'): {'en': 'Archery Dispersion Radius Calculator', 'ed': 'Compute mean point of impact and CEP from arrow impact coordinates.'},
    ('edu', 'ranking'): {'en': 'Exam Score Average / Ranking / Std. Dev.', 'ed': 'Compute class average, ranking and standard deviation for exam scores.'},
    ('meteorology', 'jiangshuigailvguji'): {'en': 'Precipitation Probability Estimator', 'ed': 'Estimate precipitation probability from integrated water vapor flux and Lifted Index (LI).'},
    ('meteorology', 'capeduiliuyouxiaoweineng'): {'en': 'CAPE (Convective Available Potential Energy) Calculator', 'ed': 'Compute CAPE, the convective available potential energy in the atmosphere.'},
    ('general', 'liangshuzhihe-chengjizuida-zuixiao-shuxueti'): {'en': 'Max/Min Sum & Product of Two Numbers', 'ed': 'Solve math problems for the maximum/minimum sum or product of two numbers.'},
    ('sports', 'pingpangqiu-xiangchi-faqiu-defen'): {'en': 'Table Tennis Rally / Serve Scoring', 'ed': 'Track table tennis points for rallies and serves.'},
    ('meteorology', 'jiaotongqixianganquantishi'): {'en': 'Traffic Weather Safety Advisor', 'ed': 'Assess traffic risks from visibility, road temperature and wind speed (fog, etc.).'},
    ('meteorology', 'nongyeqixiangjianyi'): {'en': 'Agrometeorological Advisory', 'ed': 'Get farming advice from temperature, precipitation and accumulated temperature for maize, rice, wheat.'},
    ('general', 'zhilengshebeixuanxing'): {'en': 'Refrigeration Equipment Sizing', 'ed': 'Size refrigeration equipment and estimate ideal Carnot COP from cooling load and temperatures.'},
    ('meteorology', 'taifengdingqiang'): {'en': 'Typhoon Intensity Determination', 'ed': 'Determine tropical cyclone intensity from minimum sea-level central pressure.'},
    ('metalwork', 'pinpaijiazhipinggujisuan'): {'en': 'Brand Value Estimator', 'ed': 'Estimate brand value by the income approach: revenue, brand margin and industry multiplier.'},
    ('machinery', 'zaoyin-shengya-pinpu-jiangzao-yugu'): {'en': 'Noise (SPL / Spectrum / Reduction) Estimator', 'ed': 'Estimate sound pressure level, spectrum and noise reduction.'},
    ('geology', 'diqiuhuaxueyichangjieshi'): {'en': 'Geochemical Anomaly Interpreter', 'ed': 'Compute standardized anomaly Z from element concentration, background and standard deviation.'},
    ('geology', 'diqiuwuliyingyong'): {'en': 'Geophysical Application Parameters', 'ed': 'Estimate parameters for engineering geophysics (electrical, magnetic methods).'},
    ('geology', 'diqiuwulishujujisuan'): {'en': 'Geophysical Data Calculator', 'ed': 'Process integrated gravity, magnetic and electrical geophysical data.'},
    ('fire-rescue', 'dizhensoujiuzhichengjisuan'): {'en': 'Seismic Rescue Shoring Load Calculator', 'ed': 'Compute temporary shoring loads for collapsed-building search and rescue.'},
    ('meteorology', 'dafengyingxiangpinggu'): {'en': 'High Wind Impact Assessment', 'ed': 'Assess high-wind impact by the Beaufort wind scale.'},
    ('aquaculture', 'fuhua-shuiliu-rongyang-tiaojian'): {'en': 'Hatchery (Flow / Dissolved Oxygen) Conditions', 'ed': 'Estimate water flow and dissolved-oxygen conditions for fish hatchery management.'},
    ('general', 'gongyebengxuanxing'): {'en': 'Industrial Pump Selector', 'ed': 'Select an industrial pump from flow rate, head and medium type.'},
    ('dyeing', 'bumianphtiaojie'): {'en': 'Fabric pH Adjustment', 'ed': 'Adjust fabric pH after dyeing to control shade and handle.'},
    ('sports', 'zhangpengfangfengxishu'): {'en': 'Tent Wind-Resistance Factor', 'ed': 'Look up tent wind-resistance factor by type (ultralight / 3-season / 4-season / alpine).'},
    ('textile', 'fukuanpailiaoliyonglv'): {'en': 'Fabric Width Utilization Rate', 'ed': 'Measure fabric width utilization in marker layout.'},
    ('sports', 'pingheng-biyandanjiao-shichang'): {'en': 'Balance (Eyes-Closed Single-Leg) Hold Time', 'ed': 'Record single-leg eyes-closed balance hold time.'},
    ('leather', 'paoguangliangdupinggu'): {'en': 'Polishing Gloss Assessment', 'ed': 'Assess surface gloss from polishing roller speed, pressure and passes.'},
    ('procurement', 'zhaobiao-gongkai-yaoqing-jingzheng-fangshi'): {'en': 'Tender Method (Open / Invited / Competitive)', 'ed': 'Select a tender method: open, invited or competitive negotiation.'},
    ('pediatrics', 'xinshengerhuangdan-xiaoshidanhongsu-quxian'): {'en': 'Neonatal Jaundice (Hour-Specific Bilirubin) Nomogram', 'ed': 'Plot hour-specific serum bilirubin for neonatal jaundice risk.'},
    ('general', 'wurenjixuantingwuchajisuan'): {'en': 'Drone Hovering Error Calculator', 'ed': 'Estimate UAV hover error from GPS, barometer and wind effects.'},
    ('metalwork', 'wushua-zhinengyuqingliangduibijisuanqi'): {'en': 'Brushless / Smart / Lightweight Comparison Calculator', 'ed': 'Compare brushless, smart and lightweight product designs.'},
    ('machinery', 'zhineng-wurenyugaoxiaoduibijisuanqi'): {'en': 'Smart / Unmanned / Efficient Comparison Calculator', 'ed': 'Compare smart, unmanned and high-efficiency equipment designs.'},
    ('fitness', 'zuidasheyanglianggusuan'): {'en': 'VO2max Estimator (Cooper Test)', 'ed': 'Estimate maximal oxygen uptake (VO2max) from the Cooper 12-minute run.'},
    ('urology', 'canyuniaoliang-jingfubchao-tuisuan'): {'en': 'Post-Void Residual Urine Estimator (Abdominal Ultrasound)', 'ed': 'Estimate post-void residual urine volume from abdominal ultrasound.'},
    ('cosmetic-derm', 'maokongcudafenji'): {'en': 'Pore Size Grading', 'ed': 'Grade enlarged pores by diameter, site and pore type.'},
    ('meteorology', 'qiyaxitongyidonglujing'): {'en': 'Pressure System Movement Path', 'ed': 'Estimate pressure-system movement from local pressure and 3-hour change.'},
    ('legal', 'falvwenshuguanjiancizidongtiqu'): {'en': 'Legal Document Keyword Extractor', 'ed': 'Auto-extract keywords from legal documents.'},
    ('meteorology', 'haiyangfengbaochaoyujing'): {'en': 'Storm Surge Warning', 'ed': 'Warn for coastal storm surge from typhoon pressure and max wind.'},
    ('leather', 'tushicenghoudu'): {'en': 'Coating Layer Thickness Calculator', 'ed': 'Compute finishing-coat thickness from usage, solids and density.'},
    ('general', 'jiguangrongfuhoudujisuan'): {'en': 'Laser Cladding Thickness Calculator', 'ed': 'Estimate single-pass laser cladding height from powder mass and parabolic cross-section.'},
    ('welding', 'hancaixuanyongtuijian'): {'en': 'Welding Consumable Recommender', 'ed': 'Recommend welding consumables for base metals (Q235/Q345/304/316).'},
    ('forestry', 'shengwuduoyangxingshannon'): {'en': 'Biodiversity Shannon Index', 'ed': 'Compute the Shannon diversity index for species communities.'},
    ('gas', 'yongqibujunyunxishujisuan'): {'en': 'Gas Non-Uniformity Coefficient', 'ed': 'Compute gas consumption non-uniformity coefficients by period (month/day/hour).'},
    ('sports', 'pilaohuifuqushi'): {'en': 'Fatigue Recovery Trend', 'ed': 'Track recovery trend from creatine kinase (CK) and BUN after exercise.'},
    ('reproductive-medicine', 'baifenbijisuanqi'): {'en': 'Percentage Calculator (Reproductive Medicine)', 'ed': 'Compute sperm progressive motility (PR) percentage and other reproductive ratios.'},
    ('general', 'pidaizhangjinjisuan'): {'en': 'Belt Tension Calculator', 'ed': 'Calculate V-belt tension from pitch, center distance, speed and power.'},
    ('cosmetic-derm', 'pifuphceding'): {'en': 'Skin pH Meter', 'ed': 'Assess skin acid-base state and barrier health from measured pH.'},
    ('general', 'jingmishebeixuanxing'): {'en': 'Precision Equipment Selector', 'ed': 'Select precision equipment by accuracy, load, stroke and speed.'},
    ('fire-rescue', 'shengsuoanquanxishu'): {'en': 'Rope Safety Factor Calculator', 'ed': 'Compute rope safety factors for rescue and working-at-height.'},
    ('textile', 'shrinkage'): {'en': 'Shrinkage Correction', 'ed': 'Adjust garment size by fabric shrinkage rate.'},
    ('sports', 'wangqiudefenlvfenxi'): {'en': 'Tennis Point-Rate Analyzer', 'ed': 'Analyze tennis point rates: serves, aces, double faults, first-serve %.'},
    ('general', 'naimoxingpinggujisuan'): {'en': 'Wear Resistance Evaluator', 'ed': 'Evaluate wear resistance with the Archard wear equation.'},
    ('livestock', 'dongtishouroulv-beibiaohouceding'): {'en': 'Carcass Lean / Backfat Estimator', 'ed': 'Estimate live or carcass lean percentage and backfat thickness.'},
    ('chemical', 'miaomu-guige-zhiliang-yanshou-biaozhun'): {'en': 'Seedling (Spec / Quality / Acceptance) Standard', 'ed': 'Reference standards for seedling specification, quality and acceptance.'},
    ('sports', 'xuerusuanyuzhiceding'): {'en': 'Blood Lactate Threshold Tester', 'ed': 'Determine lactate threshold from graded-exercise heart rate and blood lactate.'},
    ('aerospace', 'huoyun-uld-jizhuangqi-guige'): {'en': 'Cargo (ULD / Unit Load Device) Specs', 'ed': 'Reference specifications for air cargo ULDs / unit load devices.'},
    ('general', 'zhiliangyanshouchouyang'): {'en': 'Acceptance Sampling Planner', 'ed': 'Plan acceptance sampling by lot size N and standard attribute plans.'},
    ('textile', 'fuliao-lalian-niukou-guige'): {'en': 'Trim (Zipper / Button) Specs', 'ed': 'Reference specs for trims: zippers and buttons.'},
    ('general', 'shusongdaixuanxingjisuan'): {'en': 'Conveyor Belt Sizing Calculator', 'ed': 'Size conveyor belt width and drive power from capacity, distance and incline.'},
    ('sports', 'tongqibizhifenxi'): {'en': 'Ventilatory Equivalent Analyzer', 'ed': 'Analyze ventilatory equivalents (VE/VO2) across incremental exercise intensities.'},
    ('machinery', 'banjinzhewanzhankai'): {'en': 'Sheet Metal Bending Flat Pattern', 'ed': 'Compute sheet-metal bend flat pattern from thickness, angle, radius and K-factor.'},
    ('machinery', 'xiao-dingwei-lianjie-chicun'): {'en': 'Pin (Locating / Connecting) Dimensions', 'ed': 'Look up locating and connecting pin dimensions.'},
    ('hydraulic', 'mianbanduishibachenjiangyuce'): {'en': 'CFRD Settlement Predictor', 'ed': 'Predict concrete-face rockfill dam settlement from height and compression modulus.'},
    ('general', 'fengjixuanxingjisuan'): {'en': 'Fan Sizing Calculator', 'ed': 'Size fan shaft and motor power from airflow and pressure.'},
    ('fishery', 'yutangrongyangliang-shuiwen-qiya-yuce'): {'en': 'Pond Dissolved Oxygen Predictor', 'ed': 'Predict pond dissolved oxygen from water temperature and pressure.'},
    ('office', 'flowchart'): {'en': 'Flowchart Drawer (Mermaid)', 'ed': 'Draw flowcharts with the open-source Mermaid diagram engine.'},
    ('usedcar', 'ershouchetanpanyijiakongjianyuce'): {'en': 'Used-Car Negotiation Margin Predictor', 'ed': 'Predict used-car negotiation margin from ask price, condition and market heat.'},
    ('dentistry', 'kouqiangkuiyang-afuta-fenqi'): {'en': 'Aphthous Stomatitis Staging', 'ed': 'Stage recurrent aphthous ulcers (canker sores).'},
    ('realestate', 'shichang-bijiaofa-anlixiuzheng'): {'en': 'Sales Comparison Approach (Case Adjustment)', 'ed': 'Adjust comparable sales cases for real-estate appraisal by the comparison method.'},
    ('dyeing', 'shumayinhuacanshu'): {'en': 'Digital Textile Printing Parameters', 'ed': 'Set digital textile printing parameters; resolution drives precision.'},
    ('metalwork', 'zulinfeilvjisuan'): {'en': 'Lease Rate Calculator', 'ed': 'Compute lease rate from asset value, term, residual, interest and payment mode.'},
    ('general', 'shebeizulinfeilvjisuan'): {'en': 'Equipment Lease Rate Calculator', 'ed': 'Compute equipment lease rate by straight-line depreciation, maintenance and target margin.'},
    ('fitness', 'jianzhinengliangquekoujisuan'): {'en': 'Fat-Loss Energy Deficit Calculator', 'ed': 'Compute daily energy deficit for fat loss (about 7700 kcal per kg of fat).'},
    ('dentistry', 'kouqiangai-tnm-shaichagongju'): {'en': 'Oral Cancer (TNM) Screening Tool', 'ed': 'Screen oral cancer and stage by TNM classification.'},
    ('general', 'gongchengzaojiazhishujisuan'): {'en': 'Construction Cost Index Calculator', 'ed': 'Compute construction cost indices from materials and labor.'},
    ('meteorology', 'lvyouqixiangzhishu'): {'en': 'Travel Weather Index', 'ed': 'Rate travel weather from temperature, humidity, wind and UV.'},
    ('sports', 'shuimianhuifuzhiliang'): {'en': 'Sleep Recovery Quality', 'ed': 'Assess sleep recovery quality from duration and deep-sleep ratio.'},
    ('nephrology', 'shenxiaoqiulvguolv-24h-jiganqingchu-ccr'): {'en': 'Glomerular Filtration Rate (24h Creatinine Clearance, Ccr)', 'ed': 'Estimate GFR from 24-hour creatinine clearance (Ccr).'},
    ('fire-rescue', 'zuranyangzhishupanding'): {'en': 'Limiting Oxygen Index (LOI) Grader', 'ed': 'Grade flame retardancy and burning performance from material LOI.'},
    ('electronics', 'pcbzukangdieceng'): {'en': 'PCB Impedance Stackup', 'ed': 'Compute PCB impedance stackup by IPC-2141 from dielectric constant.'},
    ('geology', 'sanweidizhijianmocanshu'): {'en': '3D Geological Modeling Parameters', 'ed': 'Compute 3D geological modeling params from borehole thickness, dip and ore body size.'},
    ('agriculture', 'nongjijuzuoyexiaolv-mu-xiaoshi-duibi'): {'en': 'Farm Machinery Efficiency (Mu/Hour) Comparison', 'ed': 'Compare farm-machinery work efficiency (mu per hour) by width and speed.'},
    ('leather', 'xueyunhoudukongzhi'): {'en': 'Splitting Thickness Control', 'ed': 'Control leather splitting thickness by target, blade speed and feed.'},
    ('geology', 'dijichengzailijisuan'): {'en': 'Bearing Capacity Calculator (Terzaghi)', 'ed': 'Compute soil bearing capacity by Terzaghi\'s ultimate bearing theory.'},
    ('geology', 'dizhishujutongji'): {'en': 'Geological Data Statistics', 'ed': 'Descriptive statistics for geological, geochemical and assay data.'},
    ('geology', 'dizhiwurandiaochapinggu'): {'en': 'Geological Contamination Assessment', 'ed': 'Assess soil/contamination from measured concentration, background and standards.'},
    ('general', 'gongyeshebeigonglvpipei'): {'en': 'Industrial Equipment Power Matching', 'ed': 'Match motor power to load, speed and drive efficiency.'},
    ('machinery', 'tanhuangsheji'): {'en': 'Spring Designer (Helical Compression)', 'ed': 'Design cylindrical helical compression springs from wire diameter and mean diameter.'},
    ('automotive', 'xuanguatanhuangzunitexing'): {'en': 'Suspension Spring Damping Characteristics', 'ed': 'Compute suspension spring stiffness, damping and sprung mass response.'},
    ('textile', 'kangjingdianbanshuaiqi'): {'en': 'Antistatic Half-Life Meter', 'ed': 'Measure fabric static dissipation half-life.'},
    ('sports', 'sheyangdonglixuebanshi'): {'en': 'VO2 Kinetics Time Constant', 'ed': 'Compute VO2 kinetics time constant from rest and steady-state VO2.'},
    ('railway', 'qiaoliang-qiaodun-zhizuo-hezai'): {'en': 'Bridge (Pier / Bearing) Load', 'ed': 'Reference bridge pier and bearing loads.'},
    ('sports', 'yangmaiboxiaolv'): {'en': 'Oxygen Pulse Efficiency', 'ed': 'Compute oxygen pulse efficiency from VO2 and heart rate.'},
    ('geology', 'shuiwendizhishentoushiyan'): {'en': 'Hydrogeological Permeability Test', 'ed': 'Analyze aquifer permeability by the Dupuit steady well-flow formula.'},
    ('dyeing', 'shuixixiaolvjisuan'): {'en': 'Washing Efficiency Calculator', 'ed': 'Compute washing (soaping) efficiency for unfixed dye removal.'},
    ('automotive', 'qichekongtiaoxuanxing'): {'en': 'Car A/C Sizing Calculator', 'ed': 'Size vehicle A/C by cabin volume, solar load, occupants and ambient temp.'},
    ('general', 'runhuayougenghuanzhouqi'): {'en': 'Lubricant Change Interval Calculator', 'ed': 'Estimate lubricant change interval by Arrhenius law from oil capacity.'},
    ('machinery', 'runhuaxitongsheji'): {'en': 'Lubrication System Designer', 'ed': 'Design lubrication systems from bearing size, speed, load and oil viscosity.'},
    ('hydraulic', 'yeyayouxiangsheji'): {'en': 'Hydraulic Tank Designer', 'ed': 'Design hydraulic reservoirs by empirical and thermal-balance methods.'},
    ('sports', 'youyonghuashuixiaolv-swolf'): {'en': 'Swim Stroke Efficiency (SWOLF)', 'ed': 'Compute SWOLF swim stroke efficiency from time and strokes.'},
    ('cosmetic-derm', 'jiguangbochangbadian'): {'en': 'Laser Wavelength Target Finder', 'ed': 'Look up laser target chromophore and penetration depth by laser type.'},
    ('general', 'jiguanghanjieguangbanjisuan'): {'en': 'Laser Welding Spot Calculator', 'ed': 'Compute laser weld spot size from Gaussian focus, M^2 and defocus.'},
    ('general', 'rechengxiangwenchapandu'): {'en': 'Thermal Imaging Delta-T Reader', 'ed': 'Read infrared thermal delta-T from ambient temp and emissivity.'},
    ('general', 'hanjiegongyicanshu'): {'en': 'Welding Process Parameter Calculator', 'ed': 'Set welding parameters by material thickness and process (SMAW/TIG/MIG).'},
    ('welding', 'hanjiegongzhuangjiajusheji'): {'en': 'Welding Fixture Designer', 'ed': 'Design welding fixtures: clamp points from part size, weight and weld location.'},
    ('welding', 'hanjiezidonghuapinggu'): {'en': 'Welding Automation Evaluator', 'ed': 'Evaluate welding automation ROI from annual output, weld length and labor cost.'},
    ('sports', 'baofali-zongtiao-lidingtiaoyuan'): {'en': 'Explosive Power (Vertical / Standing Long Jump)', 'ed': 'Estimate explosive power from vertical jump and standing long jump.'},
    ('general', 'huanbaonaimopinggu'): {'en': 'Eco-Friendly Wear Resistance Evaluator', 'ed': 'Evaluate eco-friendly wear resistance by material and environment (temp, humidity).'},
    ('geology', 'huanjingdizhipingjia'): {'en': 'Environmental Geological Assessment', 'ed': 'Assess environmental geology by the Nemerow composite index (water, soil).'},
    ('general', 'bearing'): {'en': 'Motor Bearing Maintenance Interval', 'ed': 'Estimate motor bearing maintenance interval from bore and speed (dn factor).'},
    ('electronics', 'dianyuanxiaolvldo-dcdc'): {'en': 'Power Supply Efficiency (LDO / DCDC)', 'ed': 'Compute LDO/DCDC power efficiency from in/out voltage and current.'},
    ('general', 'lizishujianshejisuan'): {'en': 'Ion Beam Sputtering Calculator', 'ed': 'Compute ion beam sputtering yield from energy, angle, target Z and current density.'},
    ('general', 'kongtiaolengfuhejisuan'): {'en': 'AC Cooling Load Calculator', 'ed': 'Compute HVAC cooling load from envelope, solar, occupancy and equipment gains.'},
    ('sports', 'lanqiumingzhonglv-lanbanxiaolv'): {'en': 'Basketball Shooting % / Rebound Efficiency', 'ed': 'Track basketball field-goal percentage and rebound efficiency.'},
    ('general', 'nianjieqiangdujisuan'): {'en': 'Bond Strength Calculator', 'ed': 'Compute adhesive bond strength from area and shear strength.'},
    ('sports', 'yumaoqiushaqiuxiaolv'): {'en': 'Badminton Smash Efficiency', 'ed': 'Analyze badminton smash efficiency from average speed and count.'},
    ('general', 'jienengfanganjisuan'): {'en': 'Energy-Saving Plan Calculator', 'ed': 'Estimate annual energy savings from power, runtime and saving rate.'},
    ('general', 'shebeiweihuzhouqi'): {'en': 'Equipment Maintenance Interval Calculator', 'ed': 'Plan equipment maintenance interval by type and daily runtime.'},
    ('railway', 'diaoche-zuoye-xiaolv-youhua'): {'en': 'Rail Shunting (Operation / Efficiency) Optimizer', 'ed': 'Optimize rail yard shunting operations and efficiency.'},
    ('automotive', 'cheshenkongqizulixishu'): {'en': 'Vehicle Aerodynamic Drag Coefficient', 'ed': 'Compute vehicle Cd drag from frontal area, Cd and speed.'},
    ('general', 'taocizhouchengshoumingjisuan'): {'en': 'Ceramic Bearing Life Calculator', 'ed': 'Compute ceramic bearing L10 rated life by ISO 281.'},
    ('tcm-diagnosis', 'san-jiao-differentiation'): {'en': 'Sanjiao (Triple Burner) Differentiation Locator', 'ed': 'Locate Warm-Disease Sanjiao syndrome by upper/middle/lower burner.'},
    ('geology', 'dizhibianlujilubiao'): {'en': 'Geological Logging Record', 'ed': 'Generate geological logging records from hole, run and stratum depth.'},
    ('geology', 'dizhiyijipinggu'): {'en': 'Geoheritage Assessment', 'ed': 'Assess geoheritage protection grade by type and scale.'},
    ('decor', 'scheduler'): {'en': 'Construction Schedule Planner', 'ed': 'Plan home and small-project schedules with standard task templates.'},
    ('general', 'runhuayouzhanduxuanxing'): {'en': 'Lubricant Viscosity Selector', 'ed': 'Select lubricant viscosity by temperature, load and speed.'},
    ('geology', 'wutanyichangjieyi'): {'en': 'Geophysical Anomaly Interpretation', 'ed': 'Qualitatively interpret geophysical anomalies from amplitude.'},
    ('general', 'dianhuaxuedunhuakongzhi'): {'en': 'Electrochemical Passivation Controller', 'ed': 'Control electrochemical passivation of iron by the Pourbaix (E-pH) diagram.'},
    ('edu', 'flashcards'): {'en': 'Chinese Character Flashcards', 'ed': 'Free online flashcards for learning Chinese characters.'},
    ('chess', 'xiangqi-endgame'): {'en': 'Xiangqi (Chinese Chess) Endgame Hints', 'ed': 'Get hints for Xiangqi endgames: one-move/two-move mates and classic studies.'},
    ('fun', 'hangman'): {'en': 'Hangman Word Game', 'ed': 'Play the classic Hangman word-guessing game online.'},
    ('surveying', 'triangulation-side'): {'en': 'Triangulation Side Calculator', 'ed': 'Compute a triangle side by the law of sines from known side and opposite angles.'},
}


_FULL_PUNCT = re.compile(r'[\u3000-\u303f\uff00-\uffef]')


def _halfwidth(s):
    """全角标点/空格 -> 半角，避免英文标题残留中文标点（如 AST （ ... ））。"""
    out = []
    for ch in s:
        o = ord(ch)
        if 0xFF01 <= o <= 0xFF5E:
            out.append(chr(o - 0xFEE0))
        elif o == 0x3000:
            out.append(' ')
        elif o == 0x3001:
            out.append(',')
        elif o == 0x3002:
            out.append('.')
        elif o == 0x30FB:
            out.append('\u00b7')
        else:
            out.append(ch)
    return ''.join(out)


def slug_to_name(slug):
    """英文 slug -> 自然英文标题；占位符/拼音/非英文 slug 返回 None。"""
    if not re.match(r'^[a-z0-9][a-z0-9\-]*$', slug):
        return None
    if re.match(r'^(calc|tool|t|gen|util|app|tmp|test)-\d+$', slug):
        return None
    if is_pinyin_slug(slug):
        return None
    parts = slug.split('-')
    words = []
    for p in parts:
        if p in ACRONYMS:
            words.append(ACRONYMS[p])
        else:
            words.append(p[:1].upper() + p[1:])
    # 非首词的小词转小写
    for i in range(1, len(words)):
        low = words[i].lower()
        if low in LOWER:
            words[i] = low
    return ' '.join(words)


def slug_to_intro(en_name, slug):
    """按标题/动作词生成简洁英文简介。"""
    s = slug
    if re.search(r'(\w+)-to-(\w+)$', s) or 'converter' in s or 'convert' in s:
        return en_name + ' - convert values online, free and instant.'
    if 'generator' in s:
        return en_name + ' - generate results online, free and instant.'
    if 'encoder' in s or 'decode' in s or 'encrypt' in s or 'decrypt' in s:
        return en_name + ' - encode and decode online, free and secure.'
    if 'calculator' in s or 'calc' in s:
        return en_name + ' - calculate online, free and accurate.'
    if 'formatter' in s or 'format' in s:
        return en_name + ' - format text online, free and instant.'
    if 'viewer' in s or 'preview' in s:
        return en_name + ' - view and preview online, free.'
    if 'checker' in s or 'validator' in s or 'verify' in s:
        return en_name + ' - check and validate online, free.'
    if 'runner' in s or 'debugger' in s or 'compiler' in s or 'parser' in s:
        return en_name + ' - run / process online, free and in your browser.'
    if 'obfuscator' in s or 'minify' in s:
        return en_name + ' - obfuscate and minify online, free.'
    if 'comparator' in s or 'compare' in s or 'diff' in s:
        return en_name + ' - compare online, free and clear.'
    if 'picker' in s or 'selector' in s:
        return en_name + ' - pick and choose online, free.'
    return en_name + ' - free online tool.'


def main():
    si = json.load(open(SI_PATH, encoding='utf-8'))
    ov = {}
    for t in si:
        ind = t.get('i') or ''
        if TOP_INDUSTRIES is not None and ind not in TOP_INDUSTRIES:
            continue
        name = t.get('name') or t.get('n') or ''
        if not name:
            continue
        url = t.get('u') or t.get('url') or ''
        base = url.split('/')[-1].replace('.html', '')
        if not base:
            continue
        # 覆盖字典 key 用「行业/basename」精确匹配，杜绝 calc-N 跨行业错配
        key = (ind + '/' + base) if ind else base
        # 占位符优先：人工逐条翻译强制覆盖规则引擎产物（即使规则引擎已翻出英文）
        ph = PLACEHOLDER_KEY.get((ind, base))
        if isinstance(ph, dict):
            ov[key] = {'en': ph.get('en'), 'ed': ph.get('ed') or slug_to_intro(ph.get('en'), base), 'ind': ind}
            continue
        if isinstance(ph, str):
            ov[key] = {'en': ph, 'ed': slug_to_intro(ph, base), 'ind': ind}
            continue
        rn = _halfwidth(translate_name(name))
        if not _ZH_RUN.search(rn):
            # 规则引擎已翻出英文 en：统一写入英文 ed（slug_to_intro 模板），
            # 消除工具页中文 desc 经 translate_text 残留的中文简介。
            # 注意：不能依赖 search-index 旧 ed 判断，否则 _build 每轮重建会令中文 ed 回流。
            ov[key] = {'en': rn, 'ed': slug_to_intro(rn, base), 'ind': ind}
            continue
        en = slug_to_name(base)
        if not en:
            continue
        ov[key] = {'en': en, 'ed': slug_to_intro(en, base), 'ind': ind}
    os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)
    json.dump(ov, open(OUT_PATH, 'w', encoding='utf-8'),
              ensure_ascii=False, indent=0, separators=(',', ':'))
    print('[gen_en_override] tools=%d -> %s' % (len(ov), OUT_PATH))


if __name__ == '__main__':
    main()
