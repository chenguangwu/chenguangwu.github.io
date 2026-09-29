# -*- coding: utf-8 -*-
"""EN i18n 残留批产引擎 v3（审计驱动）
输入：/tmp/en_audit/report.json（真机审计产物）
输出：
  1) 跨页通用串(count>=2) -> i18n/tools/en/_common.json
  2) 单例串 -> 各工具 per-tool 字典 i18n/tools/en/<ind>/<slug>.json
规则分层：R1 中英对照取英文 / R2 使用#色值 / R3 期数年份章节数字 / R4 币种代码 /
          R5 化学元素 / R6 国家地区 / R7 emoji·动植物·食物 / R8 编程术语 / R9 通用 UI 词
硬约束：译文零中文才写入；键=页面原文精确形态；产出统计未覆盖串供人工补。
"""
import json, io, re, collections, os, glob

CJK = re.compile(r'[\u4e00-\u9fff]')
LATIN_IN_PAREN = re.compile(r'^[A-Za-z0-9][A-Za-z0-9 ,\'\.\-×x/%·&+]*$')

# ---------- R1: 「中文 (English)」/「@attr=中文 (English)」 ----------
RE_PAIR = re.compile(r'^(?:@(\w+)=)?([\u4e00-\u9fff][\u4e00-\u9fffA-Za-z0-9·、\s]*?)\s*\(([A-Za-z0-9][A-Za-z0-9 ,\'\.\-×x/%·&+]*)\)$')

def r_pair(s):
    m = RE_PAIR.match(s)
    if not m: return None
    attr, zh, en = m.group(1), m.group(2), m.group(3).strip()
    if CJK.search(en): return None
    en = en[0].upper() + en[1:] if en else en
    return ('@' + attr + '=' + en) if attr else en

# ---------- R3: 序数模式 ----------
RE_QI = re.compile(r'^第 ?(\d+) 期$')
RE_QI2 = re.compile(r'^第(\d+)期$')
RE_YEARR = re.compile(r'^第 ?(\d+) 年$')
RE_YEAR2 = re.compile(r'^第(\d+)年$')
RE_MONTH2 = re.compile(r'^第(\d+)月$')
RE_CHAP = re.compile(r'^第 (\d+) 章$')
RE_DAY = re.compile(r'^第(\d+)天$')
RE_WEEK = re.compile(r'^第(\d+)周$')
RE_RING = re.compile(r'^第(\d+)环·(.+)$')

def r_ordinal(s):
    m = RE_QI.match(s) or RE_QI2.match(s)
    if m: return 'Period ' + m.group(1)
    m = RE_YEARR.match(s) or RE_YEAR2.match(s)
    if m: return 'Year ' + m.group(1)
    m = RE_MONTH2.match(s)
    if m: return 'Month ' + m.group(1)
    m = RE_CHAP.match(s)
    if m: return 'Chapter ' + m.group(1)
    m = RE_DAY.match(s)
    if m: return 'Day ' + m.group(1)
    m = RE_WEEK.match(s)
    if m: return 'Week ' + m.group(1)
    m = RE_RING.match(s)
    if m:
        band = {'有效数字': 'significant figures', '误差': 'tolerance', '乘数': 'multiplier'}.get(m.group(2))
        if band: return 'Band %s · %s' % (m.group(1), band)
    return None

# ---------- R4: 币种 ----------
CURRENCY = {
    '美元': 'US Dollar', '欧元': 'Euro', '日元': 'Japanese Yen', '英镑': 'British Pound',
    '人民币': 'Chinese Yuan', '韩元': 'South Korean Won', '港币': 'Hong Kong Dollar',
    '澳元': 'Australian Dollar', '加元': 'Canadian Dollar', '瑞士法郎': 'Swiss Franc',
    '新加坡元': 'Singapore Dollar', '新西兰元': 'New Zealand Dollar', '印度卢比': 'Indian Rupee',
    '俄罗斯卢布': 'Russian Ruble', '巴西雷亚尔': 'Brazilian Real', '墨西哥比索': 'Mexican Peso',
    '泰铢': 'Thai Baht', '马来西亚林吉特': 'Malaysian Ringgit', '印尼盾': 'Indonesian Rupiah',
    '菲律宾比索': 'Philippine Peso', '越南盾': 'Vietnamese Dong', '土耳其里拉': 'Turkish Lira',
    '沙特里亚尔': 'Saudi Riyal', '阿联酋迪拉姆': 'UAE Dirham', '埃及镑': 'Egyptian Pound',
    '南非兰特': 'South African Rand', '尼日利亚奈拉': 'Nigerian Naira', '阿根廷比索': 'Argentine Peso',
    '智利比索': 'Chilean Peso', '哥伦比亚比索': 'Colombian Peso', '秘鲁索尔': 'Peruvian Sol',
    '波兰兹罗提': 'Polish Zloty', '捷克克朗': 'Czech Koruna', '匈牙利福林': 'Hungarian Forint',
    '瑞典克朗': 'Swedish Krona', '挪威克朗': 'Norwegian Krone', '丹麦克朗': 'Danish Krone',
    '以色列谢克尔': 'Israeli Shekel', '塔吉克斯坦索莫尼': 'Tajikistani Somoni',
}
RE_CUR = re.compile(r'^([A-Z]{2,4}) · (.+)$')
CUR_CODE = {
    'AFN': 'Afghan afghani', 'ALL': 'Albanian lek', 'AMD': 'Armenian dram', 'ANG': 'Netherlands Antillean guilder',
    'AOA': 'Angolan kwanza', 'ARS': 'Argentine peso', 'AUD': 'Australian dollar', 'AWG': 'Aruban florin',
    'AZN': 'Azerbaijani manat', 'BBD': 'Barbadian dollar', 'BDT': 'Bangladeshi taka', 'BGN': 'Bulgarian lev',
    'BHD': 'Bahraini dinar', 'BIF': 'Burundian franc', 'BND': 'Brunei dollar', 'BOB': 'Bolivian boliviano',
    'BSD': 'Bahamian dollar', 'BTN': 'Bhutanese ngultrum', 'BWP': 'Botswana pula', 'BZD': 'Belize dollar',
    'CDF': 'Congolese franc', 'CLF': 'Chilean unidad de fomento', 'CNH': 'Chinese offshore yuan',
    'CRC': 'Costa Rican colón', 'CUP': 'Cuban peso', 'DJF': 'Djiboutian franc', 'DOP': 'Dominican peso',
    'DZD': 'Algerian dinar', 'ERN': 'Eritrean nakfa', 'ETB': 'Ethiopian birr', 'ETH': 'Ethereum',
    'FJD': 'Fiji dollar', 'FKP': 'Falkland Islands pound', 'GGP': 'Guernsey pound', 'GHS': 'Ghanaian cedi',
    'GIP': 'Gibraltar pound', 'GMD': 'Gambian dalasi', 'GTQ': 'Guatemalan quetzal', 'GYD': 'Guyanese dollar',
    'HNL': 'Honduran lempira', 'HRK': 'Croatian kuna', 'HTG': 'Haitian gourde', 'ILS': 'Israeli new shekel',
    'IMP': 'Manx pound', 'IQD': 'Iraqi dinar', 'ISK': 'Icelandic króna', 'JEP': 'Jersey pound',
    'JMD': 'Jamaican dollar', 'JOD': 'Jordanian dinar', 'KES': 'Kenyan shilling', 'KGS': 'Kyrgyzstani som',
    'KHR': 'Cambodian riel', 'KID': 'Kiribati dollar', 'KMF': 'Comorian franc', 'KPW': 'North Korean won',
    'KWD': 'Kuwaiti dinar', 'KZT': 'Kazakhstani tenge', 'LAK': 'Lao kip', 'LBP': 'Lebanese pound',
    'LKR': 'Sri Lankan rupee', 'LRD': 'Liberian dollar', 'LSL': 'Lesotho loti', 'LYD': 'Libyan dinar',
    'MAD': 'Moroccan dirham', 'MGA': 'Malagasy ariary', 'MMK': 'Myanmar kyat', 'MNT': 'Mongolian tögrög',
    'MOP': 'Macanese pataca', 'MUR': 'Mauritian rupee', 'MVR': 'Maldivian rufiyaa',
    'MZN': 'Mozambican metical', 'NAD': 'Namibian dollar', 'NIO': 'Nicaraguan córdoba',
    'NPR': 'Nepalese rupee', 'OMR': 'Omani rial', 'PAB': 'Panamanian balboa', 'PGK': 'Papua New Guinean kina',
    'PKR': 'Pakistani rupee', 'PYG': 'Paraguayan guaraní', 'QAR': 'Qatari riyal', 'RON': 'Romanian leu',
    'RWF': 'Rwandan franc', 'SBD': 'Solomon Islands dollar', 'SCR': 'Seychellois rupee', 'SDG': 'Sudanese pound',
    'SHP': 'Saint Helena pound', 'SLL': 'Sierra Leonean leone', 'SOS': 'Somali shilling',
    'SRD': 'Surinamese dollar', 'SSP': 'South Sudanese pound', 'SVC': 'Salvadoran colón',
    'SYP': 'Syrian pound', 'SZL': 'Swazi lilangeni', 'THB': 'Thai baht', 'TND': 'Tunisian dinar',
    'TOP': 'Tongan paʻanga', 'TRY': 'Turkish lira', 'TTD': 'Trinidad and Tobago dollar',
    'TVD': 'Tuvaluan dollar', 'TWD': 'New Taiwan dollar', 'TZS': 'Tanzanian shilling',
    'UAH': 'Ukrainian hryvnia', 'UGX': 'Ugandan shilling', 'UYU': 'Uruguayan peso',
    'VES': 'Venezuelan bolívar', 'VND': 'Vietnamese dong', 'VUV': 'Vanuatu vatu',
    'WST': 'Samoan tala', 'XAF': 'Central African CFA franc', 'XCD': 'East Caribbean dollar',
    'XOF': 'West African CFA franc', 'XPF': 'CFP franc', 'YER': 'Yemeni rial', 'ZAR': 'South African rand',
    'ZMW': 'Zambian kwacha', 'ZWL': 'Zimbabwean dollar', 'GBX': 'Penny sterling',
    'CNY': 'Chinese yuan', 'BTC': 'Bitcoin', 'USDT': 'Tether',
}

def r_currency(s):
    m = RE_CUR.match(s)
    if m:
        code, zh = m.group(1), m.group(2)
        if zh in CURRENCY: return code + ' · ' + CURRENCY[zh]
        if code in CUR_CODE: return code + ' · ' + CUR_CODE[code]
    if s in CURRENCY: return CURRENCY[s]
    return None

# ---------- R2b: 快捷键/命令图例（左半 ASCII -- 右半中文说明）----------
RE_LEGEND = re.compile(r'^([\x20-\x7e]+?)\s*--\s*(.+)$', re.S)

def r_legend(s):
    if not RE_LEGEND.match(s): return None
    m = RE_LEGEND.match(s)
    left, right = m.group(1), m.group(2)
    if CJK.search(left): return None
    for fn in RULES_CORE + [r_extra]:
        try: out = fn(right)
        except Exception: out = None
        if out and not CJK.search(out) and out != right:
            return left + ' -- ' + out
    return None

# ---------- R2c: HTML/SQL 演示串中逐段中文替换 ----------
SEG_ZH = {
    '粗体文字': 'Bold text', '强调内容': 'Emphasized text', '重要内容': 'Important text',
    '斜体文字': 'Italic text', '删除内容': 'Deleted text', '插入内容': 'Inserted text',
    '高亮内容': 'Highlighted text', '小号文字': 'Small text', '大号文字': 'Large text',
    '下划线文字': 'Underlined text', '等宽文字': 'Monospace text', '删除线': 'Strikethrough',
    '居中文字（不推荐使用）': 'Centered text (not recommended)', '滚动文字': 'Scrolling text',
    '这是一段文字。': 'This is a paragraph.', '这是行内引用': 'Inline quotation',
    '点击展开': 'Click to expand', '单元格': 'Cell', '表头': 'Header',
    '章节标题': 'Section heading', '页面主标题': 'Page main heading', '小节标题': 'Subsection heading',
    '更小节标题': 'Smaller subsection heading', '段落标题': 'Paragraph heading',
    '最小标题': 'Smallest heading', '列表项': 'List item', '描述': 'Description', '术语': 'Term',
    '用户信息': 'User info', '不支持框架': 'Frames not supported', '右到左文字': 'Right-to-left text',
    '用户名': 'Username', '我的网页': 'My Website', '标题': 'Title', '链接': 'Link',
    '提交': 'Submit', '错误：文件未找到': 'Error: file not found', '项目': 'Item',
    '不再相关': 'No longer relevant', '在线': 'Online', '新消息': 'New message',
    '1月15日': 'Jan 15', '匿名': 'Anonymous', '未填': 'Not provided', '成年': 'Adult',
    '未成年': 'Minor', '老年': 'Senior',
}
RE_SEG = re.compile(r'([\u4e00-\u9fff][\u4e00-\u9fffA-Za-z0-9：，。、（）%/·\s]*[\u4e00-\u9fffA-Za-z0-9）%]|[黑蓝绿棕紫灰银红白橙黄金])')

def r_seg(s):
    if '\n' in s: return None
    segs = RE_SEG.findall(s)
    if not segs: return None
    out = s
    for seg in set(segs):
        tr = SEG_ZH.get(seg) or EXTRA.get(seg) or MISC.get(seg) or PROG.get(seg)
        if tr: out = out.replace(seg, tr)
    if CJK.search(out) or out == s: return None
    return out

# ---------- R5: 化学元素 ----------
# 1-98 号按序列枚举；99 号以后逐个显式映射（109-118 用官方汉字，避免错位静默错译）
ELEM_ZH = '氢氦锂铍硼碳氮氧氟氖钠镁铝硅磷硫氯氩钾钙钪钛钒铬锰铁钴镍铜锌镓锗砷硒溴氪铷锶钇锆铌钼锝钌铑钯银镉铟锡锑碲碘氙铯钡镧铈镨钕钷钐铕钆铽镝钬铒铥镱镥铪钽钨铼锇铱铂金汞铊铅铋钋砹氡钫镭锕钍镤铀镎钚镅锔锫锎锿镄钔锘铹'
ELEM_EN = ['Hydrogen','Helium','Lithium','Beryllium','Boron','Carbon','Nitrogen','Oxygen','Fluorine','Neon','Sodium','Magnesium','Aluminium','Silicon','Phosphorus','Sulfur','Chlorine','Argon','Potassium','Calcium','Scandium','Titanium','Vanadium','Chromium','Manganese','Iron','Cobalt','Nickel','Copper','Zinc','Gallium','Germanium','Arsenic','Selenium','Bromine','Krypton','Rubidium','Strontium','Yttrium','Zirconium','Niobium','Molybdenum','Technetium','Ruthenium','Rhodium','Palladium','Silver','Cadmium','Indium','Tin','Antimony','Tellurium','Iodine','Xenon','Caesium','Barium','Lanthanum','Cerium','Praseodymium','Neodymium','Promethium','Samarium','Europium','Gadolinium','Terbium','Dysprosium','Holmium','Erbium','Thulium','Ytterbium','Lutetium','Hafnium','Tantalum','Tungsten','Rhenium','Osmium','Iridium','Platinum','Gold','Mercury','Thallium','Lead','Bismuth','Polonium','Astatine','Radon','Francium','Radium','Actinium','Thorium','Protactinium','Uranium','Neptunium','Plutonium','Americium','Curium','Berkelium','Californium','Einsteinium','Fermium','Mendelevium','Nobelium','Lawrencium']
assert len(ELEM_ZH) == len(ELEM_EN), (len(ELEM_ZH), len(ELEM_EN))
ELEM_MAP = dict(zip(ELEM_ZH, ELEM_EN))
ELEM_MAP.update({
    '锕系': 'Actinides', '镧系': 'Lanthanides',
    '𬬻': 'Rutherfordium', '𬭊': 'Dubnium', '𬭳': 'Seaborgium', '𬭛': 'Bohrium',
    '𬭶': 'Hassium', '鿏': 'Meitnerium', '𫟼': 'Darmstadtium', '𬬭': 'Roentgenium',
    '鿔': 'Copernicium', '鿭': 'Nihonium', '𫓧': 'Flerovium', '镆': 'Moscovium',
    '𫟷': 'Livermorium', '鿬': 'Tennessine', '鿫': 'Oganesson',
})

def r_elem(s):
    return ELEM_MAP.get(s)

# ---------- R6: 国家地区 ----------
COUNTRY = {
    '中国': 'China', '中国台湾': 'Taiwan, China', '中国香港': 'Hong Kong, China', '中国澳门': 'Macao, China',
    '日本': 'Japan', '韩国': 'South Korea', '朝鲜': 'North Korea', '蒙古': 'Mongolia', '印度': 'India',
    '印度尼西亚': 'Indonesia', '泰国': 'Thailand', '越南': 'Vietnam', '菲律宾': 'Philippines',
    '马来西亚': 'Malaysia', '新加坡': 'Singapore', '缅甸': 'Myanmar', '柬埔寨': 'Cambodia',
    '老挝': 'Laos', '孟加拉国': 'Bangladesh', '巴基斯坦': 'Pakistan', '斯里兰卡': 'Sri Lanka',
    '尼泊尔': 'Nepal', '阿富汗': 'Afghanistan', '伊朗': 'Iran', '伊拉克': 'Iraq', '叙利亚': 'Syria',
    '约旦': 'Jordan', '黎巴嫩': 'Lebanon', '以色列': 'Israel', '沙特阿拉伯': 'Saudi Arabia',
    '科威特': 'Kuwait', '卡塔尔': 'Qatar', '巴林': 'Bahrain', '阿联酋': 'United Arab Emirates',
    '阿曼': 'Oman', '也门': 'Yemen', '土耳其': 'Turkey', '塞浦路斯': 'Cyprus',
    '哈萨克斯坦': 'Kazakhstan', '乌兹别克斯坦': 'Uzbekistan', '吉尔吉斯斯坦': 'Kyrgyzstan',
    '塔吉克斯坦': 'Tajikistan', '土库曼斯坦': 'Turkmenistan', '格鲁吉亚': 'Georgia',
    '亚美尼亚': 'Armenia', '阿塞拜疆': 'Azerbaijan',
    '英国': 'United Kingdom', '法国': 'France', '德国': 'Germany', '意大利': 'Italy', '西班牙': 'Spain',
    '葡萄牙': 'Portugal', '荷兰': 'Netherlands', '比利时': 'Belgium', '卢森堡': 'Luxembourg',
    '瑞士': 'Switzerland', '奥地利': 'Austria', '丹麦': 'Denmark', '挪威': 'Norway', '瑞典': 'Sweden',
    '芬兰': 'Finland', '冰岛': 'Iceland', '爱尔兰': 'Ireland', '波兰': 'Poland', '捷克': 'Czechia',
    '斯洛伐克': 'Slovakia', '匈牙利': 'Hungary', '罗马尼亚': 'Romania', '保加利亚': 'Bulgaria',
    '希腊': 'Greece', '克罗地亚': 'Croatia', '斯洛文尼亚': 'Slovenia', '塞尔维亚': 'Serbia',
    '乌克兰': 'Ukraine', '白俄罗斯': 'Belarus', '俄罗斯': 'Russia', '爱沙尼亚': 'Estonia',
    '拉脱维亚': 'Latvia', '立陶宛': 'Lithuania', '马耳他': 'Malta',
    '美国': 'United States', '加拿大': 'Canada', '墨西哥': 'Mexico', '古巴': 'Cuba',
    '危地马拉': 'Guatemala', '洪都拉斯': 'Honduras', '巴拿马': 'Panama',
    '巴西': 'Brazil', '阿根廷': 'Argentina', '智利': 'Chile', '秘鲁': 'Peru', '哥伦比亚': 'Colombia',
    '委内瑞拉': 'Venezuela', '玻利维亚': 'Bolivia', '厄瓜多尔': 'Ecuador', '乌拉圭': 'Uruguay',
    '巴拉圭': 'Paraguay', '埃及': 'Egypt', '利比亚': 'Libya', '突尼斯': 'Tunisia', '阿尔及利亚': 'Algeria',
    '摩洛哥': 'Morocco', '苏丹': 'Sudan', '埃塞俄比亚': 'Ethiopia', '肯尼亚': 'Kenya',
    '坦桑尼亚': 'Tanzania', '乌干达': 'Uganda', '尼日利亚': 'Nigeria', '加纳': 'Ghana',
    '南非': 'South Africa', '津巴布韦': 'Zimbabwe', '赞比亚': 'Zambia', '莫桑比克': 'Mozambique',
    '马达加斯加': 'Madagascar', '厄立特里亚': 'Eritrea', '索马里': 'Somalia',
    '澳大利亚': 'Australia', '新西兰': 'New Zealand', '斐济': 'Fiji',
}

def r_country(s):
    return COUNTRY.get(s)

# ---------- R7: emoji / 动物 / 食物 / 表情 / 手势 ----------
EMOJI = {
    '狗': 'Dog', '猫': 'Cat', '狐狸': 'Fox', '狼': 'Wolf', '虎': 'Tiger', '马': 'Horse', '熊': 'Bear',
    '企鹅': 'Penguin', '考拉': 'Koala', '熊猫': 'Panda', '青蛙': 'Frog', '蛇': 'Snake', '鲸': 'Whale',
    '海豚': 'Dolphin', '鲨鱼': 'Shark', '章鱼': 'Octopus', '鱿鱼': 'Squid', '龙虾': 'Lobster',
    '螃蟹': 'Crab', '虾': 'Shrimp', '蜗牛': 'Snail', '蜘蛛': 'Spider', '蜜蜂': 'Bee', '蚂蚁': 'Ant',
    '瓢虫': 'Ladybug', '蝴蝶': 'Butterfly', '蟋蟀': 'Cricket', '蝙蝠': 'Bat', '鹰': 'Eagle',
    '猫头鹰': 'Owl', '鸭子': 'Duck', '热带鱼': 'Tropical fish', '河豚': 'Blowfish', '鳄鱼': 'Crocodile',
    '猴': 'Monkey', '猴子': 'Monkey', '大猩猩': 'Gorilla', '大象': 'Elephant', '狮子': 'Lion',
    '长颈鹿': 'Giraffe', '斑马': 'Zebra', '鹿': 'Deer', '牛': 'Cow', '猪': 'Pig', '羊': 'Sheep',
    '骆驼': 'Camel', '袋鼠': 'Kangaroo', '刺猬': 'Hedgehog', '野猪': 'Boar', '兔': 'Rabbit',
    '仓鼠': 'Hamster', '鸟': 'Bird', '火鸡': 'Turkey', '鸡': 'Chicken', '公鸡': 'Rooster',
    '小鸡': 'Chick', '孔雀': 'Peacock', '鹦鹉': 'Parrot', '天鹅': 'Swan', '鸽子': 'Dove',
    '三明治': 'Sandwich', '便当': 'Bento', '冰淇淋': 'Ice cream', '华夫饼': 'Waffle', '卷饼': 'Burrito',
    '口罩': 'Mask', '巧克力': 'Chocolate', '奶酪': 'Cheese', '大蒜': 'Garlic', '土豆': 'Potato',
    '寿司': 'Sushi', '哈密瓜': 'Cantaloupe', '汉堡': 'Hamburger', '披萨': 'Pizza', '意面': 'Pasta',
    '煎蛋': 'Fried egg', '热狗': 'Hot dog', '米': 'Rice', '米饭': 'Cooked rice', '法棍': 'Baguette',
    '洋葱': 'Onion', '胡萝卜': 'Carrot', '桃子': 'Peach', '梨': 'Pear', '椰子': 'Coconut',
    '樱桃': 'Cherry', '橙子': 'Orange', '草莓': 'Strawberry', '猕猴桃': 'Kiwi fruit', '芒果': 'Mango',
    '菠萝': 'Pineapple', '葡萄': 'Grapes', '薯条': 'French fries', '蛋糕': 'Cake', '糖果': 'Candy',
    '西瓜': 'Watermelon', '苹果': 'Apple', '红苹果': 'Red apple', '青苹果': 'Green apple',
    '青菜': 'Leafy green', '西兰花': 'Broccoli', '鸡蛋': 'Egg', '饼干': 'Cookie', '面包': 'Bread',
    '甜甜圈': 'Doughnut', '生日蛋糕': 'Birthday cake', '牛油果': 'Avocado', '牛角包': 'Croissant',
    '灯泡': 'Light bulb', '蜡烛': 'Candle', '灭火器': 'Fire extinguisher', '油桶': 'Oil drum',
    '警灯': 'Police car light', '钱袋': 'Money bag', '钱飞': 'Money with wings',
    '手表': 'Watch', '座钟': 'Mantelpiece clock', '闹钟': 'Alarm clock', '秒表': 'Stopwatch',
    '手机': 'Mobile phone', '座机': 'Telephone receiver', '电话': 'Telephone', '传真': 'Fax machine',
    '寻呼机': 'Pager', '电池': 'Battery', '电视': 'Television', '收音机': 'Radio', '摄像机': 'Video camera',
    '电影机': 'Movie camera', '胶片': 'Film frames', '相机': 'Camera', '闪光相机': 'Camera with flash',
    '录像带': 'Videocassette', '软盘': 'Floppy disk', '电脑': 'Computer', '台式机': 'Desktop computer',
    '打印机': 'Printer', '键盘': 'Keyboard', '鼠标': 'Computer mouse', '轨迹球': 'Trackball',
    '手电筒': 'Flashlight', '投影仪': 'Projector', '显微镜': 'Microscope', '望远镜': 'Telescope',
    '卫星天线': 'Satellite antenna', '指南针': 'Compass', '地图': 'World map', '火箭': 'Rocket',
    '直升机': 'Helicopter', '飞机': 'Airplane', '消防车': 'Fire engine', '救护车': 'Ambulance',
    '警车': 'Police car', '赛车': 'Racing car', '公交车': 'Bus', '有轨电车': 'Tram car',
    '轻轨': 'Light rail', '火车': 'Train', '高铁': 'High-speed train', '地铁': 'Metro',
    '摩托车': 'Motorcycle', '滑板车': 'Kick scooter', '自行车': 'Bicycle', '卡车': 'Truck',
    '拖拉机': 'Tractor', '出租车': 'Taxi', '汽车': 'Automobile', '过山车': 'Roller coaster',
    '摩天轮': 'Ferris wheel', '体育场': 'Stadium', '东京塔': 'Tokyo Tower', '自由女神': 'Statue of Liberty',
    '身份证明': 'Identification card', '身份证': 'ID card', '信用卡': 'Credit card', '美元符': 'Dollar sign',
    '水滴': 'Droplet', '波浪': 'Wave', '雪': 'Snowflake', '闪光': 'Dizzy', '火花': 'Sparkles',
    '星星': 'Star', '心': 'Heart', '红心': 'Red heart', '橙心': 'Orange heart', '黄心': 'Yellow heart',
    '绿心': 'Green heart', '蓝心': 'Blue heart', '紫心': 'Purple heart', '黑心': 'Black heart',
    '白心': 'White heart', '棕心': 'Brown heart', '叉框': 'Cross mark button', '勾': 'Check mark',
    '勾选': 'Check box with check', '勾选框': 'Checkbox', '爱心眼': 'Smiling face with heart-eyes',
    '微笑': 'Smiling face', '大笑': 'Grinning face with big eyes', '笑哭': 'Face with tears of joy',
    '笑脸': 'Smiling face with smiling eyes', '斜眼笑': 'Smirking face', '露齿笑': 'Grinning face',
    '得意': 'Smug face', '开心': 'Happy face', '眨眼': 'Winking face', '晕': 'Dizzy face',
    '恶心': 'Nauseated face', '呕吐': 'Face vomiting', '心碎': 'Broken heart', '思考': 'Thinking face',
    '叹气': 'Face exhaling', '说谎': 'Lying face', '翻白眼': 'Face with rolling eyes',
    '吐舌': 'Face with tongue', '单眼吐舌': 'Winking face with tongue', '尴尬': 'Flushed face',
    '苦笑': 'Bitter smile', '沉思': 'Pensive face', '睡觉': 'Sleeping face', '望': 'Face without mouth',
    '挑眉': 'Face with raised eyebrow', '挥手': 'Waving hand', '握手': 'Handshake',
    '合十': 'Folded hands', '鼓掌': 'Clapping hands', '庆祝': 'Party popper', '赞': 'Thumbs up',
    '踩': 'Thumbs down', '飞吻': 'Face blowing a kiss', '爱你': 'Smiling face with hearts',
    '睁眼亲': 'Kiss', '闭眼亲': 'Kiss with smiling eyes', '指上': 'Index finger pointing up',
    '指下': 'Index finger pointing down', '指左': 'Index finger pointing left',
    '指右': 'Index finger pointing right', '五指': 'Raised hand', '摇滚': 'Sign of the horns',
    '书呆子': 'Nerd face', '五': 'Five', ' pumping': '',
    '🀄': 'Mahjong red dragon',
    '白旗': 'White flag', '黑旗': 'Black flag', '帆船': 'Sailboat', '独角兽': 'Unicorn',
    '法轮': 'Wheel of Dharma', '交替': 'Alternation',
}

def r_emoji(s):
    return EMOJI.get(s)

# ---------- R8: 编程 / 技术术语 ----------
PROG = {
    '基础': 'Basics', '函数': 'Functions', '删除': 'Delete', '工程': 'Project', '类': 'Class',
    '继承': 'Inheritance', '集合': 'Sets', '变量': 'Variables', '异常': 'Exceptions', '接口': 'Interfaces',
    '数组': 'Arrays', '客户端': 'Client', '排序': 'Sorting', '控制流': 'Control flow', '枚举': 'Enums',
    '模块': 'Modules', '泛型': 'Generics', '配置': 'Configuration', '面向对象': 'Object-oriented',
    '元组': 'Tuples', '内置类型': 'Built-in types', '分页': 'Pagination', '列表': 'Lists',
    '基本类型': 'Primitive types', '可变参数': 'Variadic parameters', '字符串': 'Strings',
    '数据库': 'Database', '日期时间': 'Date and time', '标签': 'Tags', '帮助': 'Help',
    '循环': 'Loops', '恢复': 'Restore', '扩展': 'Extensions', '全部': 'All', '差': 'Poor',
    '事务': 'Transactions', '代理': 'Proxy', '优化': 'Optimization', '属性': 'Properties',
    '文件': 'Files', '方法': 'Methods', '无穷': 'Infinity', '日志': 'Logs', '权限': 'Permissions',
    '正则': 'Regex', '标准库': 'Standard library', '缓存': 'Cache', '编译': 'Compilation',
    '认证': 'Authentication', '调试': 'Debugging', '过滤': 'Filter', '高级': 'Advanced',
    '备份': 'Backup', '命令': 'Commands', '响应': 'Response', '窗口': 'Window', '异步': 'Async',
    '异常处理': 'Exception handling', '匿名函数': 'Anonymous functions', '变量声明': 'Variable declaration',
    '哈希': 'Hash', '哈希映射': 'Hash map', '字典': 'Dictionary', '动态数组': 'Dynamic arrays',
    '常量': 'Constants', '断言': 'Assertions', '抽象类': 'Abstract class', '迭代器': 'Iterators',
    '闭包': 'Closures', '装饰器': 'Decorators', '结构体': 'Structs', '约束': 'Constraints',
    '模式匹配': 'Pattern matching', '类型推断': 'Type inference', '生命周期': 'Lifetimes',
    '自增': 'Increment', '下标': 'Subscript', '交集': 'Intersection', '不可变': 'Immutable',
    '函数式': 'Functional', '命名空间': 'Namespaces', '条件': 'Conditionals', '定时器': 'Timers',
    '任务': 'Tasks', '连接': 'Connections', '写入': 'Write', '读取': 'Read', '更新': 'Update',
    '替换': 'Replace', '导入': 'Import', '搜索': 'Search', '比较': 'Compare', '分组': 'Grouping',
    '文档': 'Documentation', '文本': 'Text', '性能': 'Performance', '内存': 'Memory',
    '系统': 'System', '索引': 'Indexes', '脚本': 'Scripts', '退出': 'Exit', '启动': 'Start',
    '清理': 'Clean up', '计数': 'Counting', '字节': 'Bytes', '秒': 'Seconds', '微': 'Micro',
    '其他': 'Other', '当前': 'Current', '通用': 'General', '速率': 'Rate', '环境变量': 'Environment variables',
    '创建数据库': 'Create database', '删除数据库': 'Drop database', '切换数据库': 'Switch database',
    '列出数据库': 'List databases', '列出表': 'List tables', '修改表': 'Alter table',
    '创建索引': 'Create index', '查看索引': 'View indexes', '查看日志': 'View logs',
    '查看表结构': 'Describe table', '查看帮助': 'View help', '导出数据库': 'Export database',
    '恢复数据库': 'Restore database', '重命名': 'Rename', '重载配置': 'Reload config',
    '切换用户': 'Switch user', '删除资源': 'Delete resource', '创建资源': 'Create resource',
    '复制文件': 'Copy file', '健康检查': 'Health check', '限流': 'Rate limiting',
    '字段存在': 'Field exists', '总行数': 'Total rows', '分项': 'Breakdown',
    'JSON 函数': 'JSON functions', '文件首/末': 'File start/end', '定长': 'Fixed length',
    '抛出异常': 'Throw exception', '语义错误': 'Semantic error', '格式化日期': 'Format date',
    '最后修改时间': 'Last modified', '资源支持的方法': 'Allowed methods',
    '资源使用': 'Resource usage', '返回变更的行': 'Return changed rows',
    '插入冲突处理': 'Insert conflict handling', '输入命令': 'Enter a command',
    '常用方法': 'Common methods', '数组类型': 'Array types', '网络状态': 'Network status',
    '设备内存': 'Device memory', '设备像素比': 'Device pixel ratio', '时区': 'Time zone',
    '主机名': 'Hostname', '网络地址': 'Network address', '广播地址': 'Broadcast address',
    '可用主机数': 'Usable hosts', '下行带宽': 'Downstream bandwidth', '最大速率': 'Max rate',
    '启动': 'Start', '使用': 'Usage', '中': 'Medium', '外': 'Outer', '无': 'None',
}

def r_prog(s):
    return PROG.get(s)

# ---------- R9: 通用 UI / 报告 / 单位杂项 ----------
MISC = {
    '实测值': 'Measured', '合格': 'Pass', '不合格': 'Fail', '标准要求': 'Standard requirement',
    '检测项目': 'Test item', '复制': 'Copy', '分类：': 'Category: ', '参数：': 'Parameters: ',
    '语法：': 'Syntax: ', '生成结果：': 'Result: ', '环保达标率': 'Eco-compliance rate',
    '温度因子': 'Temperature factor', '温度系数': 'Temperature coefficient', 'PH值': 'pH value',
    '≤1级': 'Level ≤1', '≤2级': 'Level ≤2', '求解目标：': 'Objective: ',
    '水分含量': 'Moisture content', '纯度': 'Purity', '硬度': 'Hardness', '磨耗量': 'Abrasion',
    '耐压': 'Withstand voltage', '认证': 'Certification', '寿命等级': 'Life class',
    '使用寿命': 'Service life', '剩余寿命 (年)': 'Remaining life (years)',
    '预计寿命 (年)': 'Estimated life (years)', '预计寿命 (小时)': 'Estimated life (hours)',
    '当年投入': 'Year-1 investment', '总收益': 'Total return', '总投入': 'Total investment',
    '总预算': 'Total budget', '当年收益': 'Year-1 return', '累计收益率': 'Cumulative return',
    '净利润：': 'Net profit: ', '净收益 (元)': 'Net gain (CNY)', '期初': 'Beginning balance',
    '期末资产': 'End assets', '本期还款': 'Period payment', '还款期数': 'Number of payments',
    '第 1 期': 'Period 1', '第 2 期': 'Period 2', '第 3 期': 'Period 3', '第 4 期': 'Period 4',
    '第 5 期': 'Period 5', '5 期': '5 periods',
    '建议检测周期 (年)': 'Recommended test interval (years)', '应力利用率': 'Stress utilization',
    '应力截面积 (mm²)': 'Stress area (mm²)', '综合校正系数': 'Combined correction factor',
    '综合涨跌幅度': 'Overall change', '综合等级': 'Overall grade', '综合评分 (100)': 'Overall score (100)',
    '改进建议': 'Improvement suggestions', '评估维度': 'Assessment dimensions',
    '权重合计': 'Total weight', '校验结果': 'Validation result', '解析结果': 'Parsed result',
    '计算结果': 'Result', '📋 计算结果': '📋 Result', '📋 计算明细': '📋 Breakdown',
    '换算结果': 'Conversion result', '结论：': 'Conclusion: ', '描述：': 'Description: ',
    '数字：': 'Number: ', '设备：': 'Device: ', '合规判定：': 'Compliance: ',
    '✅ 综合判定：合格': '✅ Overall: PASS',
    '❌ 综合判定：不合格': '❌ Overall: FAIL',
    '所有检测项目均符合标准要求，检测报告可用于质量验收': 'All test items meet the standard requirements; this report can be used for quality acceptance.',
    '部分项目不符合标准要求，请整改后重新检测': 'Some items do not meet the standard; rectify and retest.',
    '@aria-label=结果操作': '@aria-label=Result actions', '@alt=头像': '@alt=Avatar',
    '@aria-label=选择时间': '@aria-label=Select time', '@title=点击复制': '@title=Click to copy',
    '@title=删除': '@title=Delete',
    '@title=凸起': '@title=Raised', '@title=厚重': '@title=Heavy', '@title=多彩': '@title=Colorful',
    '@title=大圆角': '@title=Large radius', '@title=小圆角': '@title=Small radius',
    '@title=方形': '@title=Square', '@title=柔和': '@title=Soft', '@title=浮起': '@title=Lifted',
    '@title=深陷': '@title=Sunken', '@title=长阴影': '@title=Long shadow', '@title=卡片': '@title=Card',
    '50,000.00 元': 'CNY 50,000.00', '8 字节': '8 bytes', '原始字节': 'Raw bytes',
    '压缩后': 'Compressed', '宽高比': 'Aspect ratio', '平均粒度': 'Average grain size',
    '年节电量 (kWh)': 'Annual energy saving (kWh)', '基准': 'Baseline',
    '基准根字号 root font-size = 16px（1rem = 16px）': 'Baseline root font-size = 16px (1rem = 16px)',
    '基准载流量 (A)': 'Base ampacity (A)', '另存为': 'Save as', '可多个': 'Multiple allowed',
    '写入': 'Write', '写字': 'Writing', '广场': 'Plaza', '已废弃': 'Deprecated', '废弃': 'Deprecated',
    '带速 (m/s)': 'Belt speed (m/s)', '周期 (ms)': 'Period (ms)', '切缝宽度 (mm)': 'Kerf width (mm)',
    '地面覆盖宽度 (m)': 'Ground coverage width (m)', '功率密度 (W/cm²)': 'Power density (W/cm²)',
    '功率密度 (W/mm²)': 'Power density (W/mm²)', '最大间距': 'Max spacing', '实际井间距：': 'Actual well spacing: ',
    '管径范围': 'Pipe diameter range', '推荐中心距 (mm)': 'Recommended center distance (mm)',
    '推荐截面 (mm²)': 'Recommended cross-section (mm²)', '推荐泵型': 'Recommended pump',
    '推荐电机 (kW)': 'Recommended motor (kW)', '电机功率 (kW)': 'Motor power (kW)',
    '轴功率 (kW)': 'Shaft power (kW)', '计算电流 (A)': 'Calculated current (A)',
    '进给速度 (mm/min)': 'Feed rate (mm/min)', '选型扭矩 (N·m)': 'Selection torque (N·m)',
    '拧紧扭矩': 'Tightening torque', '抗渗等级': 'Impermeability grade', '热输入等级': 'Heat input class',
    '体积电阻率': 'Volume resistivity', '绝缘电阻': 'Insulation resistance',
    '老化后强度保持率': 'Strength retention after aging', '无损检测合格率': 'NDT pass rate',
    '沉积速率 (g/min)': 'Deposition rate (g/min)', '酸值': 'Acid value',
    '磨损系数 K': 'Wear coefficient K', '角频率 ω (rad/s)': 'Angular frequency ω (rad/s)',
    '总冷负荷 (W)': 'Total cooling load (W)', '矩阵 A (2×2)': 'Matrix A (2×2)',
    '行列式': 'Determinant', '设备像素比': 'Device pixel ratio',
    ' '*0: None,
    '甲基橙': 'Methyl orange', '与分析': 'Analytics', '中文': 'Chinese', '英文': 'English',
    '* 或 ETag': '* or ETag', '* 或具体头': '* or specific headers',
    'TOML 输出': 'TOML output', 'XML 输出': 'XML output', 'A实际占比': 'Actual share of A',
    '🀄 物品': '🀄 Items', '⌚ 物品': '⌚ Items', '🐶 动物': '🐶 Animals', '👍 手势': '👍 Gestures',
    '😀 笑脸': '😀 Faces', ' Temporary': None,
    '永久重定向': '308 Permanent Redirect', '临时重定向': '307 Temporary Redirect',
    '方法不允许': '405 Method Not Allowed', '网关超时': '504 Gateway Timeout',
    '网关错误': '502 Bad Gateway', '服务不可用': '503 Service Unavailable',
    '请求错误': '400 Bad Request', '浏览器 XSS 过滤（已废弃）': 'XSS auditor (deprecated)',
    '禁止 MIME 嗅探': 'MIME sniffing prevention', '设置 Cookie': 'Set-Cookie',
    '设置标记': 'Set flag', '版本对比': 'Version comparison', '下/上一页': 'Next/previous page',
    '共 25 项': '25 items in total', '共 30 项': '30 items in total', '共 32 项': '32 items in total',
    '共 33 项': '33 items in total', '共 37 项': '37 items in total', '共 40 项': '40 items in total',
    '共 48 项': '48 items in total', '共 51 项': '51 items in total',
    '红色弱': 'Protanomaly', '红色盲': 'Protanopia', '绿色弱': 'Deuteranomaly',
    '绿色盲': 'Deuteranopia', '蓝色弱': 'Tritanomaly', '蓝色盲': 'Tritanopia', '全色盲': 'Achromatopsia',
    '蓝色': 'Blue', '红色': 'Red', '绿色': 'Green', '白色': 'White', '黑色': 'Black',
    '白底对比度': 'Contrast on white', '黑底对比度': 'Contrast on black', '推荐文字色': 'Recommended text color',
    '颜色名称': 'Color name', '像素': 'Pixels', '第一行': 'First row', '等号': 'Equals sign',
    '问号': 'Question mark', '三角': 'Triangle', 'V 字': 'Victory hand', '五指': 'Raised hand',
    '生命': 'Life', '时间': 'Time', '日期': 'Date', '金额': 'Amount', '数量': 'Quantity',
    '单位': 'Unit', '备注': 'Notes', '状态': 'Status', '类型': 'Type', '名称': 'Name',
    '标题': 'Title', '内容': 'Content', '操作': 'Actions', '详情': 'Details', '汇总': 'Summary',
    '合计': 'Total', '平均': 'Average', '最小': 'Min', '最大': 'Max', '示例': 'Example',
    '说明': 'Description', '警告': 'Warning', '错误': 'Error', '成功': 'Success', '失败': 'Failed',
    '保存': 'Save', '取消': 'Cancel', '确认': 'Confirm', '提交': 'Submit', '重置': 'Reset',
    '清空': 'Clear', '全选': 'Select all', '展开': 'Expand', '收起': 'Collapse', '预览': 'Preview',
    '下载': 'Download', '上传': 'Upload', '导出': 'Export', '导入': 'Import', '编辑': 'Edit',
    '新建': 'New', '添加': 'Add', '移除': 'Remove', '关闭': 'Close', '打开': 'Open',
    '刷新': 'Refresh', '加载中': 'Loading', '计算': 'Calculate', '运行': 'Run', '执行': 'Execute',
    '停止': 'Stop', '暂停': 'Pause', '继续': 'Resume', '下一步': 'Next', '上一步': 'Previous',
    '完成': 'Done',     '取消选择': 'Deselect', '复制成功': 'Copied', '已复制': 'Copied',
    '元': 'CNY', '原子量': 'Atomic mass', '数据类型': 'Data types', '程序入口': 'Entry point',
    # 上下文标签（审计新增）
    '删除参数': 'Delete parameter', '右移': 'Move right', '左移': 'Move left', '折叠': 'Collapse',
    '示例图片': 'Sample image', '参数值': 'Parameter value', '参数名': 'Parameter name',
    '停留分钟': 'Stop duration (min)', '地点名称': 'Place name', '距离km': 'Distance in km',
    '金额（负=投入，正=收入）': 'Amount (negative = outlay, positive = income)',
    '如 97': 'e.g. 97', '例如：H2O, NaCl, Ca(OH)2': 'e.g. H2O, NaCl, Ca(OH)2',
    '浅色透明': 'Light transparent', '测试': 'Test', '浮雕效果': 'Emboss', '深色': 'Dark',
    '深色玻璃': 'Dark glass', '渐变阴影': 'Gradient shadow', '火焰效果': 'Fire effect',
    '点击加载示例': 'Click to load sample', '点击复制值': 'Click to copy value',
    '点击复制对象': 'Click to copy object', '点击复制数组': 'Click to copy array',
    '点击复制键': 'Click to copy key', '玻璃': 'Glass', '玻璃态': 'Glassmorphism',
    '磨砂玻璃': 'Frosted glass', '粉色': 'Pink', '粉色玻璃': 'Pink glass', '紫色': 'Purple',
    '经典阴影': 'Classic shadow', '绿色玻璃': 'Green glass', '胶囊': 'Pill',
    '蓝色玻璃': 'Blue glass', '超透明': 'Ultra transparent', '轻柔': 'Gentle',
    '边框阴影': 'Border shadow', '透明度': 'Opacity', '锁定': 'Locked', '霓虹': 'Neon',
    '霓虹效果': 'Neon effect', '霓虹紫': 'Neon purple', '中圆角': 'Medium radius',
    '内发光': 'Inner glow', '内嵌效果': 'Inset effect', '厚重玻璃': 'Heavy glass',
    '双层': 'Double layer', '双层阴影': 'Double shadow', '反叶子': 'Reversed leaf',
    '发光': 'Glow', '发光效果': 'Glow effect', '发光边': 'Glowing border', '叶子': 'Leaf',
    '圆形': 'Circle', '圆角玻璃': 'Rounded glass', '复古印刷': 'Retro print', '平': 'Flat',
    '彩色玻璃': 'Stained glass', '效果': 'Effect', '斜角': 'Bevel', '方形玻璃': 'Square glass',
    '有机 1': 'Organic 1', '有机 2': 'Organic 2', '极光': 'Aurora', '极简': 'Minimal',
    '柔和阴影': 'Soft shadow', '标准': 'Standard', '标准玻璃': 'Standard glass',
    '梦幻光晕': 'Dreamy halo', '模糊': 'Blur', '厚重': 'Heavy', '多功能': 'Multifunction',
    # 量化标签
    '0 或 1 次': '0 or 1 time', '0 次或多次': '0 or more times', '1 次或多次': '1 or more times',
    '0/1 编码': '0/1 encoding', '0=不限速': '0 = no rate limit',
    '0=允许跟踪, 1=禁止': '0 = allow tracking, 1 = block',
    '1 包含 0 排除': '1 include, 0 exclude', '1 字节整数': '1-byte integer',
    '4 字节整数': '4-byte integer', '8 字节整数': '8-byte integer',
    '4 字节, 1970~2038': '4 bytes, 1970-2038', '1 类': 'Class 1', '24 位': '24 characters',
    '24 位十六进制': '24 hex digits', '256 位（64 位十六进制）': '256-bit (64 hex digits)',
    '8 种基本类型': '8 primitive types', '8 莫氏': 'Mohs 8', '8 段：': '8 segments: ',
    '3种算法': '3 algorithms', '3D立体': '3D', '1em 间距': '1em spacing', '2em 间距': '2em spacing',
    '73 行': '73 lines', '100分': '100 points', '10寸 (8R)': '10 in (8R)', '5寸 (3R)': '5 in (3R)',
    '6寸 (4R)': '6 in (4R)', '7寸 (5R)': '7 in (5R)', '8寸 (6R)': '8 in (6R)',
    '100.00 🇨🇳 CNY 人民币': 'CNY 100.00', '64 GB 存储卡': '64 GB memory card',
    '25mm² 铜芯导线': '25mm² copper conductor', '315kVA 变压器': '315 kVA transformer',
    '80A 断路器': '80 A circuit breaker', '18.5kW / 4极 / 380V YE3/YE4（三相低压）': '18.5 kW / 4-pole / 380V YE3/YE4 (three-phase LV)',
    '193nm 光源、NA=1.35 时，理论分辨率约': 'With a 193 nm light source and NA=1.35, the theoretical resolution is about ',
    '5,800 MHz 理想视距最大传输距离约': 'At 5,800 MHz the ideal line-of-sight max range is about ',
    '1920 × 1080 像素 @ 300 DPI = 162.56 × 91.44 mm': '1920 × 1080 px @ 300 DPI = 162.56 × 91.44 mm',
    '16.3×9.1cm打印': 'Prints 16.3×9.1 cm', '50mm 全画幅等效': '50mm full-frame equivalent',
    '5500K 用于相机白平衡预设': '5500K for camera white-balance presets',
    '1984 的罗马数字写法为 MCMLXXXIV': '1984 in Roman numerals is MCMLXXXIV',
    '97 是质数 ✅': '97 is prime ✅', '1000h 磨损深度 (mm)': 'Wear depth at 1000 h (mm)',
    '10年投资回报率': '10-year ROI', '10年节约电费 (元)': '10-year electricity savings (CNY)',
    '20年后购买力': 'Purchasing power in 20 years', '200万 (年收入×10)': '2M (10x annual income)',
    '200 章以上': '200+ chapters', '50 万字以上': '500k+ characters', '10~30 万字': '100k-300k characters',
    '1~3 万字': '10k-30k characters', '72法则: 14.4年翻倍 | 115法则: 23.0年翻3倍': 'Rule of 72: doubles in 14.4 years | Rule of 115: triples in 23.0 years',
    '40%~60% 适中 / > 70% 警戒 / < 30% 偏低': '40%-60% moderate / > 70% warning / < 30% low',
    '1.5~2.5 常见 / > 3 高杠杆': '1.5-2.5 common / > 3 high leverage',
    '< 1 稳健 / 1~2 一般 / > 2 高杠杆': '< 1 robust / 1-2 average / > 2 high leverage',
    '3% (温和)': '3% (mild)', '5% (较高)': '5% (high)', '8% (高通胀)': '8% (high inflation)',
    '9%（差异适中）': '9% (moderate difference)', '10% ✓ 适用': '10% ✓ applicable',
    '66.67%  (距离: 5)': '66.67%  (distance: 5)', '95% 置信区间 · z 分布 · 临界值=1.960': '95% CI · z distribution · critical value = 1.960',
    '= 精确 ~ 正则 ~* 忽略大小写': '= exact, ~ regex, ~* case-insensitive',
    '> - 大于号': '> - Greater-than sign', '< - 小于号': '< - Less-than sign', '? 运算符': '? operator',
    '// 不要使用': '// Do not use', '// 多次 PUT 同一资源结果相同': '// Multiple PUTs of the same resource yield the same result',
    '// 控制每个 Cookie < 4KB': '// Keep each Cookie under 4KB', '// 无法通过 document.cookie 读取 HttpOnly Cookie': '// HttpOnly cookies cannot be read via document.cookie',
    '// 超出会被丢弃最早的': '// Oldest entries are evicted when exceeded',
    '/api/users  而非  /api/user': '/api/users  instead of  /api/user',
    '/搜索 q退出': '/ to search, q to quit',
    'A4（基准）Hz': 'A4 (reference) Hz', 'A5（八度）Hz': 'A5 (octave) Hz', 'C4（中央C）Hz': 'C4 (middle C) Hz',
    'AA 标准': 'AA standard', 'AA 正文': 'AA body text', 'AA（优秀）': 'AA (good)',
    'AAA 优秀': 'AAA excellent', 'AAA 标准': 'AAA standard', 'AAA 正文': 'AAA body text',
    'AAA级要求（正常文字）': 'AAA requirement (normal text)', 'AAA（最佳）': 'AAA (best)',
    'AAA级（最佳）': 'AAA (best)', 'AA级要求（正常文字）': 'AA requirement (normal text)',
    'AA级（推荐）': 'AA (recommended)', 'AA（优秀）': 'AA (good)',
    'A级（基础）': 'Class A (basic)', 'E2级（限室内）': 'Class E2 (indoor only)',
    'MS-70（完美未流通）': 'MS-70 (perfect uncirculated)',
    'ASC 升序（默认）, DESC 降序': 'ASC ascending (default), DESC descending',
    'ASC 升序, DESC 降序': 'ASC ascending, DESC descending',
    'A - 极低磨损（优秀）': 'A - Very low wear (excellent)', 'B - 良好': 'B - Good',
    'C - 中等': 'C - Fair', 'A 方案': 'Plan A', 'A 产品': 'Product A', 'B 产品': 'Product B',
    'C 产品': 'Product C', 'C 为主': 'Mainly C', 'A 模 |A|': 'A modulus |A|',
    'B 模 |B|': 'B modulus |B|', 'A 辐角（角度）': 'A argument (degrees)', 'B 辐角（角度）': 'B argument (degrees)',
    'A（蓝芯）/C': 'A (blue core)/C', 'AND OR NOT 前缀': 'AND OR NOT prefixes',
    'API 密钥': 'API key', 'APS-C (佳能)等效': 'APS-C (Canon) equivalent',
    'AQI 空气质量指数': 'AQI air quality index', 'ARIA属性正确使用（必要时）': 'Use ARIA attributes correctly (when needed)',
    'ASCII 码': 'ASCII code', 'ASP.NET 版本': 'ASP.NET version', 'BSON 类型': 'BSON types',
    'Bearer Token 认证': 'Bearer token authentication', 'Block 方块': 'Block',
    'Box 实心': 'Box (solid)', 'CIDR 前缀': 'CIDR prefix', 'CIDR 表示': 'CIDR notation',
    'CLI 命令': 'CLI commands', 'Cookie 优先级（Chrome）': 'Cookie priority (Chrome)',
    'Cookie 作用域名': 'Cookie domain', 'Cookie 作用路径': 'Cookie path', 'Cookie 写入': 'Cookie write',
    'Cookie 删除': 'Cookie delete', 'Cookie 头': 'Cookie header', 'Cookie 读取': 'Cookie read',
    'Cookie 键值对': 'Cookie key-value pairs', 'Copy 类型不转移': 'Copy does not transfer type',
    'Crawl-Delay（可选）': 'Crawl-Delay (optional)', 'Ctrl+p Ctrl+q 脱离': 'Ctrl+p Ctrl+q detach',
    'Ctrl+x 前缀': 'Ctrl+x prefix', 'Cv 值': 'Cv value', 'Kv 值': 'Kv value',
    'DDB首年折旧': 'DDB first-year depreciation', 'SYD首年折旧': 'SYD first-year depreciation',
    'DISCARD 取消': 'DISCARD cancels', 'DNS 查询': 'DNS lookup', 'DNS 查询（旧）': 'DNS lookup (legacy)',
    'DNS 预解析控制': 'DNS prefetch control', 'EBIT 变动': 'EBIT change', 'EPS 变动': 'EPS change',
    'EPS（元）': 'EPS (CNY)', 'EDR 增强速率': 'EDR enhanced data rate', 'ENUM, 复合类型': 'ENUM, composite types',
    'EX 秒, PX 毫秒, NX 不存在, XX 已存在': 'EX seconds, PX ms, NX if not exists, XX if exists',
    'F(1) 到 F(20)': 'F(1) to F(20)', 'FTS 函数': 'FTS functions', 'Fa / Fr 比值': 'Fa/Fr ratio',
    'Fetch 元数据': 'Fetch metadata', 'Files.readAllBytes 等': 'Files.readAllBytes and more',
    'Flex 主轴方向': 'Flex main axis', 'Flex 换行': 'Flex wrap', 'Flex 方向与换行': 'Flex direction and wrap',
    'Flex 简写': 'Flex shorthand', 'Frame 操作': 'Frame operations', 'Gap 间距': 'Gap',
    'Gerber寿命 Nf': 'Gerber life Nf', 'Git Flow 功能分支': 'Git Flow feature branch',
    'Git Flow 发布分支': 'Git Flow release branch', 'Git Flow 热修复': 'Git Flow hotfix',
    'Goodman利用率': 'Goodman utilization', 'Goodman安全系数': 'Goodman safety factor',
    'Goodman等效应力幅 (MPa)': 'Goodman equivalent stress amplitude (MPa)',
    'Gradle 构建': 'Gradle build', 'Grid 列模板': 'Grid columns', 'Grid 列跨度': 'Grid column span',
    'Grid 区域': 'Grid areas', 'Grid 简写': 'Grid shorthand', 'Grid 自动流': 'Grid auto flow',
    'Grid 行模板': 'Grid rows', 'Grid 行跨度': 'Grid row span', 'Grid 项目区域': 'Grid item areas',
    'Gzip 压缩': 'Gzip compression', 'H (氢)': 'H (Hydrogen)', 'O (氧)': 'O (Oxygen)',
    'H1 到 H6': 'H1 to H6', 'HEX (大写)': 'HEX (uppercase)', 'HS 高速（WiFi 辅助）': 'HS high speed (Wi-Fi assisted)',
    'HTML 十六进制': 'HTML hex', 'HTML 十进制': 'HTML decimal', 'HTML 命名': 'HTML named entities',
    'HTML 文档的根元素': 'Root element of an HTML document', 'HTML 结构': 'HTML structure',
    'HTML5 新增：': 'Added in HTML5: ', 'HTML命名 · 转义 · 09/30 00:44': 'HTML entities · escaping · 09/30 00:44',
    'HTML符合规范，通过W3C验证': 'HTML is valid and passes W3C validation',
    'HTTP 客户端': 'HTTP client', 'HTTP 版本不支持': 'HTTP version not supported',
    'HTTP 跳 HTTPS': 'HTTP to HTTPS redirect', 'HTTP 页面无法设置/读取 Secure Cookie': 'Secure cookies cannot be set/read over HTTP',
    'HTTP/1.0 兼容的不缓存': 'HTTP/1.0-compatible no-cache', 'HTTP/2 流优先级': 'HTTP/2 stream priority',
    'HttpOnly Cookie 无法被 JS 读取': 'HttpOnly cookies cannot be read by JS', 'HttpOnly 限制': 'HttpOnly restriction',
    'IE 下载选项': 'IE download options', 'IE 兼容模式': 'IE compatibility mode', 'IF 点': 'IF point',
    'INNER 可省略': 'INNER is optional', 'IO 流': 'IO streams', 'IP 类别': 'IP category',
    'IP 类型': 'IP type', 'IP: 192.168.1.100   掩码: 24': 'IP: 192.168.1.100   mask: 24',
    'IRR < 折现率：': 'IRR < discount rate: ', 'IRR 月利率': 'IRR monthly rate',
    'ISO 6,400 · 较重': 'ISO 6,400 · heavy', 'ISO VG 32/46 全损耗系统用油': 'ISO VG 32/46 machine oil',
    'Insert 模式': 'Insert mode', 'Command 模式': 'Command mode', 'Normal 模式': 'Normal mode',
    'JSON Patch 应用': 'JSON Patch apply', 'JSON 操作': 'JSON operations', 'JSON 操作符': 'JSON operators',
    'JSON 文本': 'JSON text', 'JSON 类型（MySQL 5.7+）': 'JSON type (MySQL 5.7+)',
    'JSON1 函数': 'JSON1 functions', 'JSONB 操作符': 'JSONB operators', 'JSONB/数组索引': 'JSONB/array indexes',
    'Lambda 表达式': 'Lambda expressions', 'Larson-Miller参数': 'Larson-Miller parameter',
    'L10 寿命 (百万转)': 'L10 life (million revolutions)', 'L10寿命 (百万转)': 'L10 life (million revolutions)',
    'L10疲劳寿命 (h)': 'L10 fatigue life (h)', 'L₁₀ 寿命（百万转）': 'L10 life (million revolutions)',
    'L₁₀h 寿命（小时）': 'L10h life (hours)', 'L₁₀y 寿命（年）': 'L10y life (years)',
    'LE Audio 音频': 'LE Audio', 'M 总位数, D 小数位': 'M total digits, D decimals',
    'Magit Git 客户端': 'Magit Git client', 'Markdown编辑器': 'Markdown editor',
    'MathML 数学公式': 'MathML formulas', 'Maven 构建': 'Maven build', 'Meta 标签': 'Meta tags',
    'Meta(Alt/Option)+x 命令': 'Meta(Alt/Option)+x command', 'MySQL 不支持': 'Not supported in MySQL',
    'Nginx 内部重定向': 'Nginx internal redirect', 'Nginx 缓冲控制': 'Nginx buffering',
    'Nginx 限速': 'Nginx rate limiting', 'NULL 判断': 'NULL checks', 'ObjectId 类型': 'ObjectId type',
    'Oracle 用 MINUS': 'Oracle uses MINUS', 'OVER 子句': 'OVER clause', 'P/C 载荷比': 'P/C load ratio',
    'P/C载荷比': 'P/C load ratio', 'PD 3.1 最高 240W': 'PD 3.1 up to 240W',
    'PHP 标记': 'PHP tags', 'POSIX 字符类': 'POSIX character classes', 'GET 子资源': 'GET subresource',
    'POST 子资源': 'POST subresource', 'PV值 (MPa·m/s)': 'PV value (MPa·m/s)',
    'PV值 (Pa·m/s)': 'PV value (Pa·m/s)', 'PV值超限，可能严重磨损': 'PV exceeded; severe wear possible',
    'PV评估': 'PV assessment', 'Pod 定义': 'Pod definition', 'PostgreSQL 特性': 'PostgreSQL features',
    'Prosigns（特殊信号）': 'Prosigns (special signals)', 'R407C/R410A(中低温)': 'R407C/R410A (medium-low temp)',
    'RAII 指针': 'RAII pointers', 'RENAMENX 不覆盖': 'RENAMENX does not overwrite',
    'RET 当前': 'RET current', 'REV 降序': 'REV descending', 'Referer 策略': 'Referer policy',
    'SQL 标准, Oracle/PostgreSQL': 'SQL standard, Oracle/PostgreSQL', 'SQL 标准分页': 'SQL standard paging',
    'SSL 协议': 'SSL protocol', 'SSL 证书': 'SSL certificate', 'STORE 可存结果': 'STORE can save results',
    'STRICT 表': 'STRICT tables', 'SUS得分（等级D）': 'SUS score (grade D)', 'SUS总分': 'SUS total score',
    'SUS等级': 'SUS grade', 'SUS贡献分': 'SUS contribution', 'SUS量表分析': 'SUS scale analysis',
    'SVG 尺寸': 'SVG size', 'SVG 矢量图': 'SVG vector', 'Allow（每行一个路径）': 'Allow (one path per line)',
    'Disallow（每行一个路径）': 'Disallow (one path per line)', 'Apache/Nginx 静态文件': 'Apache/Nginx static files',
    'AUD · 澳大利亚元': 'AUD · Australian dollar',
    "SELECT * FROM users WHERE name LIKE '张%' OR email LIKE '%@example.com';": "SELECT * FROM users WHERE name LIKE 'Zhang%' OR email LIKE '%@example.com';",
    '复杂': 'Complex', '简单': 'Simple', '切换': 'Switch', '查看': 'View', '显示': 'Show',
    '隐藏': 'Hide', '启用': 'Enable', '禁用': 'Disable', '手动': 'Manual', '自动': 'Auto',
}

def r_misc(s):
    return MISC.get(s)

# ---------- R3b: 归一化与数值模式 ----------
RE_CHAP2 = re.compile(r'^第(\d+)章$')
RE_AGE = re.compile(r'^(\d{1,3})岁$')
RE_YUAN = re.compile(r'^¥([\d,\.]+)(/月|/年|/天|/时|/小时)?$')
RE_NUMUNIT = re.compile(r'^第 ?(\d+) (期|年|月|天|周|章|环|步|季|轮|批|组|关|层|级|号)$')
UNIT_EN = {'期':'Period','年':'Year','月':'Month','天':'Day','周':'Week','章':'Chapter','环':'Ring','步':'Step','季':'Season','轮':'Round','批':'Batch','组':'Group','关':'Level','层':'Floor','级':'Grade','号':'No.'}

def r_norm(s):
    m = RE_CHAP2.match(s)
    if m: return 'Chapter ' + m.group(1)
    m = RE_AGE.match(s)
    if m: return m.group(1) + ' years old'
    m = RE_YUAN.match(s)
    if m:
        per = {'/月': '/month', '/年': '/year', '/天': '/day', '/时': '/hour', '/小时': '/hour'}.get(m.group(2) or '', '')
        return 'CNY ' + m.group(1) + per
    m = RE_NUMUNIT.match(s)
    if m: return UNIT_EN[m.group(2)] + ' ' + m.group(1)
    # 全角括号/全角冒号归一化后再查 MISC/PROG
    alt = s.replace('（', '(').replace('）', ')').replace('：', ': ')
    if alt != s:
        for table in (MISC, PROG):
            if alt in table: return table[alt]
    return None

# ---------- R0: @attr=包装（先于其余规则，递归翻译余部）----------
RE_ATTRWRAP = re.compile(r'^@(\w+)=(.+)$', re.S)
COLOR_CN = {'黑':'Black','蓝':'Blue','绿':'Green','棕':'Brown','紫':'Purple','灰':'Gray',
            '银':'Silver','红':'Red','白':'White','橙':'Orange','黄':'Yellow','金':'Gold',
            '青':'Cyan','粉':'Pink'}

def r_attrwrap(s):
    m = RE_ATTRWRAP.match(s)
    if not m: return None
    attr, rest = m.group(1), m.group(2)
    for fn in RULES_CORE:
        if fn is r_attrwrap: continue
        try: out = fn(rest)
        except Exception: out = None
        if out and not CJK.search(out) and out != rest:
            return '@' + attr + '=' + out
    # 使用 #HEX
    mu = re.match(r'^使用 (#(?:[0-9A-Fa-f]{3}|[0-9A-Fa-f]{6}))$', rest)
    if mu: return 'Use ' + mu.group(1)
    # 第 N 个色帽，可拖动或用左右方向键移动
    mc = re.match(r'^第 ?(\d+) 个色帽，可拖动或用左右方向键移动$', rest)
    if mc: return 'Color stop ' + mc.group(1) + ', drag or move with arrow keys'
    return None

def r_fold(s):
    m = re.match(r'^([\d\.]+) ?折$', s)
    if m:
        d = float(m.group(1))
        off = round((10 - d) / 10 * 100)
        return ('%d%% off' % off) if off else 'Full price'
    m = re.match(r'^(\d{1,3})分$', s)
    if m: return m.group(1) + ' points'
    return None

def r_colorchip(s):
    m = re.match(r'^(<span[^>]*></span>)([\u4e00-\u9fff])$', s)
    if m and m.group(2) in COLOR_CN: return m.group(1) + COLOR_CN[m.group(2)]
    if s in COLOR_CN: return COLOR_CN[s]
    return None

def r_regex(s):
    # /regex/ 匹配 X 形态 → /regex/ matches X（仅替换动词与常见中文段，保留代码原样）
    m = re.match(r'^(/.+?/\w*) 匹配 (.+)$', s)
    if m:
        rest = m.group(2)
        for zh, en in (('而非', ' instead of '), ('中的', ' in '), ('不匹配', ' does not match '),
                       ('而非', ' instead of '), ('所有', 'all '), ('每行的', 'foo in each line: ')):
            rest = rest.replace(zh, en)
        if not CJK.search(rest): return m.group(1) + ' matches ' + rest
    return None

RULES_CORE = []
RULES = []

# ---------- R10: 人工批产增量词典（/tmp/en_audit/extra_*.json）----------
EXTRA = {}
import glob as _glob
for _p in sorted(_glob.glob('/tmp/en_audit/extra_*.json')):
    try:
        EXTRA.update(json.load(io.open(_p, encoding='utf-8')))
    except Exception as e:
        print('!! extra 词表加载失败:', _p, e)

def r_extra(s):
    return EXTRA.get(s)

RULES_CORE.extend([r_pair, r_ordinal, r_currency, r_elem, r_country, r_emoji, r_prog, r_misc, r_norm])
RULES.extend([r_attrwrap, r_fold, r_colorchip, r_regex, r_legend])
RULES.extend(RULES_CORE)
RULES.append(r_extra)
RULES.append(r_fold)
RULES.append(r_seg)

# ---------- R11: 数值+中文单位（金额/计数/时长/进制）----------
NUM = r'([\d,]+(?:\.\d+)?)'
SCALE = {'万': 10000, '亿': 100000000}
PER_EN = {'/月': '/month', '/年': '/year', '/天': '/day', '/时': '/hour', '/小时': '/hour',
          '/股': '/share', '/次': '/use', '/单': '/order', '/台': '/unit', '/人': '/person',
          '/月收入': '/month', '/公里': '/km', '/公里/时': '/km/h', '/百公里': '/100 km',
          '/千瓦时': '/kWh', '/度': '/kWh'}
RE_MONEY = re.compile(r'^' + NUM + r'\s*(万|亿)?\s*元\s*(/[\u4e00-\u9fffA-Za-z]+)?$')
UNIT_CN = {'字': 'characters', '章': 'chapters', '项': 'items', '列': 'columns', '条': 'entries',
           '张': 'cards', '个': 'items', '款': 'models', '家': 'companies', '人': 'people',
           '名': 'people', '篇': 'articles', '题': 'questions', '页': 'pages', '期': 'periods',
           '环': 'rings', '次': 'times', '盏': 'lamps', '亩': 'mu (1/15 ha)', '档': 'levels',
           '级': 'levels', '天': 'days', '日': 'days', '周': 'weeks', '个月': 'months', '月': 'months',
           '年': 'years', '小时': 'hours', '分钟': 'minutes', '秒': 'seconds', '倍': 'x',
           '步': 'steps', '层': 'floors', '间': 'rooms', '台': 'units', '套': 'sets', '件': 'pieces',
           '笔': 'entries', '座': 'units', '批': 'batches', '轮': 'rounds', '道': 'dishes',
           '吨': 'tons', '克': 'g', '公斤': 'kg', '斤': 'jin (0.5 kg)', '米': 'm', '公里': 'km',
           '公里/时': 'km/h', '千瓦时': 'kWh', '度': 'kWh', '升': 'L', '毫升': 'mL', '磅': 'lb',
           '英尺': 'ft', '英寸': 'in', '海里': 'nautical miles', '摄氏度': '°C', '卡路里': 'cal',
           '字符': 'characters', '批次': 'batches', '棵': 'trees', '只': 'animals', '头': 'head',
           '羽': 'birds', '间夜': 'room-nights', '人次': 'visits', '单': 'orders', 'frames': ''}
RE_COUNT = re.compile(r'^' + NUM + r'\s*(万|亿)?\s*(' + '|'.join(sorted([k for k in UNIT_CN if len(k) > 1], key=len, reverse=True)) + r'|[' + ''.join([k for k in UNIT_CN if len(k) == 1 and k not in '亿']) + r'])$')
RE_BASE = re.compile(r'^' + NUM + r'进制$')
RE_PCT = re.compile(r'^' + NUM + r'%\s*/\s*(年|月|天|次|小时|单)$')
PCT_PER = {'年': 'year', '月': 'month', '天': 'day', '次': 'use', '小时': 'hour', '单': 'order'}

def _num(raw, sc):
    v = float(raw.replace(',', ''))
    if sc: v *= SCALE[sc]
    if v == int(v):
        s = '{:,.0f}'.format(int(v))
    else:
        s = '{:,.2f}'.format(v).rstrip('0').rstrip('.')
    return s

def r_numeric(s):
    m = RE_MONEY.match(s)
    if m:
        per = PER_EN.get(m.group(3) or '', '')
        return ('CNY ' + _num(m.group(1), m.group(2)) + per).strip()
    m = RE_BASE.match(s)
    if m: return 'Base-' + str(int(float(m.group(1).replace(',', ''))))
    m = RE_PCT.match(s)
    if m: return m.group(1) + '%/' + PCT_PER[m.group(2)]
    m = RE_COUNT.match(s)
    if m:
        u = UNIT_CN[m.group(3)]
        return _num(m.group(1), m.group(2)) + ' ' + u
    # 裸万/亿：10.00万 / 176.0万 / 10.00 亿
    m = re.match(r'^' + NUM + r'\s*(万|亿)$', s)
    if m: return _num(m.group(1), m.group(2))
    # 复合时长：2时1分 / 1 小时 11 分 / 3分58秒 / 35.0分钟
    m = re.match(r'^' + NUM + r'\s*(?:小时|时)\s*' + NUM + r'\s*(?:分钟|分)$', s)
    if m: return _num0(m.group(1)) + ' h ' + _num0(m.group(2)) + ' min'
    m = re.match(r'^' + NUM + r'\s*(?:分钟|分)\s*' + NUM + r'\s*(?:秒钟|秒)$', s)
    if m: return _num0(m.group(1)) + ' min ' + _num0(m.group(2)) + ' s'
    # N 天（约 X 周）/ N年（N期）/ N 岁 N 个月 N 天
    m = re.match(r'^' + NUM + r'\s*天（约\s*' + NUM + r'\s*周）$', s)
    if m: return _num0(m.group(1)) + ' days (about ' + m.group(2) + ' weeks)'
    m = re.match(r'^' + NUM + r'\s*年（' + NUM + r'期）$', s)
    if m: return _num0(m.group(1)) + ' years (' + m.group(2) + ' periods)'
    m = re.match(r'^' + NUM + r'\s*岁\s*' + NUM + r'\s*个月\s*' + NUM + r'\s*天$', s)
    if m: return _num0(m.group(1)) + ' years ' + _num0(m.group(2)) + ' months ' + _num0(m.group(3)) + ' days'
    # N 行 · 只读 / N 字段
    m = re.match(r'^' + NUM + r'\s*行\s*·\s*只读$', s)
    if m: return _num0(m.group(1)) + ' lines · read-only'
    m = re.match(r'^' + NUM + r'\s*字段$', s)
    if m: return _num0(m.group(1)) + ' fields'
    return None

def _num0(raw):
    v = float(raw.replace(',', ''))
    return '{:,.0f}'.format(v) if v == int(v) else str(v)

RULES.append(r_numeric)

def r_reference(s):
    m = re.match(r'^小写希腊字母 (\w+)$', s)
    if m: return 'Lowercase Greek ' + m.group(1)
    m = re.match(r'^大写希腊字母 (\w+)$', s)
    if m: return 'Uppercase Greek ' + m.group(1)
    m = re.match(r'^圆周率 (\w+)$', s)
    if m: return 'Pi (' + m.group(1) + ')'
    m = re.match(r'^共 (\d+) 条（点击命令复制）$', s)
    if m: return m.group(1) + ' commands (click to copy)'
    m = re.match(r'^共 (\d+) 个属性$', s)
    if m: return m.group(1) + ' properties in total'
    return None

REF_MAP = {
    '🍎 食物': '🍎 Food', '⚽ 运动': '⚽ Sports', '🚗 旅行': '🚗 Travel', '❤️ 符号': '❤️ Symbols',
    '😀 表情': '😀 Faces', '🐶 动物': '🐶 Animals', '👍 手势': '👍 Gestures', '⌚ 物品': '⌚ Objects',
    '🍕 食物': '🍕 Food', '🚙 交通': '🚙 Vehicles', '🎉 活动': '🎉 Events',
    '布局': 'Layout', '盒模型': 'Box model', '背景': 'Background', '边框': 'Border',
    '变换过渡': 'Transform & transition', '显示类型': 'Display type', '不继承': 'Not inherited',
    '属性名：': 'Property: ', '初始值：': 'Initial value: ', '是否继承：': 'Inherited: ',
    '浏览器支持：': 'Browser support: ', '可用值：': 'Valid values: ',
    '定位方式': 'Positioning', '全部（sticky 需现代浏览器）': 'All (sticky needs modern browsers)',
    '顶部偏移': 'Top offset', '右侧偏移': 'Right offset', '底部偏移': 'Bottom offset',
    '左侧偏移': 'Left offset', '浮动': 'Float', '清除浮动': 'Clear float', '层叠顺序': 'Stacking order',
    '溢出处理': 'Overflow', '水平溢出': 'Horizontal overflow', '垂直溢出': 'Vertical overflow',
    '弹性布局': 'Flexbox', '网格布局': 'Grid', '多列布局': 'Multi-column', '表格布局': 'Table',
    '列表样式': 'List style', '文字字体': 'Font', '文本样式': 'Text style', '间距尺寸': 'Spacing & size',
    '视觉效果': 'Visual effects', '用户界面': 'User interface', '动画过渡': 'Animation & transition',
    '变形转换': 'Transform', '其他属性': 'Other properties',
}

def r_refmap(s):
    return REF_MAP.get(s)

RULES.append(r_reference)
RULES.append(r_refmap)

RULES.append(r_numeric)

def translate(s):
    for fn in RULES:
        try:
            out = fn(s)
        except Exception:
            out = None
        if out and not CJK.search(out) and out != s:
            return out
    return None

def main():
    report = json.load(io.open('/tmp/en_audit/report.json', encoding='utf-8'))
    # 汇总全部残留串与出现页
    str_pages = collections.defaultdict(set)
    for page, v in report.items():
        for s in v.get('strings', []):
            str_pages[s].add(page)

    # 读取现有 _common
    common_path = 'i18n/tools/en/_common.json'
    common = json.load(io.open(common_path, encoding='utf-8'))

    global_added, per_added = 0, 0
    uncovered = collections.Counter()
    # 按 ind/slug 分桶
    per_tool = collections.defaultdict(dict)

    for s, pages in sorted(str_pages.items(), key=lambda x: (-len(x[1]), x[0])):
        en = translate(s)
        if not en:
            uncovered[s] = len(pages)
            continue
        # 审计记录形态是 '@attr=原文'，运行时查的是裸串：入库一律用裸键裸值
        am = re.match(r'^@(\w+)=(.+)$', s, re.S)
        store_key = am.group(2) if am else s
        store_val = en.split('=', 1)[1] if am and en.startswith('@' + am.group(1) + '=') else en
        if len(pages) >= 2:
            if store_key not in common:
                common[store_key] = store_val
                global_added += 1
        else:
            page = sorted(pages)[0]
            m = re.match(r'^/tools/([a-z-]+)/([a-z0-9-]+)\.html$', page)
            if not m:
                uncovered[s] = 1
                continue
            ind, slug = m.group(1), m.group(2)
            path = 'i18n/tools/en/%s/%s.json' % (ind, slug)
            if not os.path.exists(path):
                uncovered[s] = 1
                continue
            if store_key not in per_tool[(ind, slug)]:
                per_tool[(ind, slug)][store_key] = store_val

    # 写 per-tool 字典
    for (ind, slug), add in per_tool.items():
        path = 'i18n/tools/en/%s/%s.json' % (ind, slug)
        d = json.load(io.open(path, encoding='utf-8'))
        mp = d.setdefault('map', {})
        n0 = len(mp)
        for k, v in add.items():
            if k not in mp:
                mp[k] = v
        with io.open(path, 'w', encoding='utf-8') as f:
            json.dump(d, f, ensure_ascii=False, indent=1)
            f.write('\n')
        per_added += len(mp) - n0

    # 写 _common
    with io.open(common_path, 'w', encoding='utf-8') as f:
        json.dump(common, f, ensure_ascii=False, indent=1)
        f.write('\n')

    bad = [k for k, v in common.items() if CJK.search(v)]
    print('global_added:', global_added, '| common total:', len(common), '| common CJK values:', len(bad))
    print('per_tool dicts updated:', len(per_tool), '| per-tool entries added:', per_added)
    print('uncovered strings:', len(uncovered))
    with io.open('/tmp/en_audit/uncovered.txt', 'w', encoding='utf-8') as f:
        for s, c in uncovered.most_common():
            f.write('%d\t%s\n' % (c, s))

def fix_elements():
    """强制回写元素映射：任何字典里 key∈ELEM_MAP 而 value≠正确译名的，一律纠正（防静默错译）。"""
    fixed = 0
    files = ['i18n/tools/en/_common.json'] + [f for f in glob.glob('i18n/tools/en/*/*.json') if not f.endswith('_index.json')]
    for path in files:
        d = json.load(io.open(path, encoding='utf-8'))
        mp = d.get('map', d if isinstance(d, dict) else {})
        changed = False
        for k, correct in ELEM_MAP.items():
            if k in mp and mp[k] != correct:
                mp[k] = correct
                changed = True
                fixed += 1
        if changed:
            with io.open(path, 'w', encoding='utf-8') as f:
                json.dump(d, f, ensure_ascii=False, indent=1)
                f.write('\n')
    print('element fixes applied:', fixed)

def fix_attrkeys():
    """迁移：字典里 '@attr=中文' 形态的键改为裸键（运行时 pickEn 查的是属性值本身），
    值里的 '@attr=' 前缀同步剥掉。返回修正数。"""
    n = 0
    files = ['i18n/tools/en/_common.json'] + [f for f in glob.glob('i18n/tools/en/*/*.json') if not f.endswith('_index.json')]
    for path in files:
        d = json.load(io.open(path, encoding='utf-8'))
        mp = d.get('map', d if isinstance(d, dict) else {})
        pairs = [(k, v) for k, v in list(mp.items()) if isinstance(k, str) and k.startswith('@') and '=' in k]
        changed = False
        for k, v in pairs:
            key = k.split('=', 1)[1]
            val = v.split('=', 1)[1] if isinstance(v, str) and v.startswith('@') and '=' in v else v
            if key and not CJK.search(val):
                mp[key] = val
                changed = True
            del mp[k]
        if changed:
            with io.open(path, 'w', encoding='utf-8') as f:
                json.dump(d, f, ensure_ascii=False, indent=1)
                f.write('\n')
            n += 1
    print('attr-key migration done, files touched:', n)

if __name__ == '__main__':
    fix_attrkeys()
    main()
