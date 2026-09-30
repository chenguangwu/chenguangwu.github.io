# -*- coding: utf-8 -*-
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gen_sports_apply import apply_tool

IND = 'life'

# ---------------- 1. 生肖星座计算器 ----------------
apply_tool('zodiac-calculator', '生肖星座计算', 'Zodiac Calculator', {
 '生肖星座计算': 'Chinese Zodiac & Western Zodiac',
 '/ 生肖星座计算': '/ Zodiac Calculator',
 '📖 查看「生肖星座计算器使用指南」': '📖 View the "Zodiac Calculator Guide"',
 '生肖按（年份 − 4）÷ 12 的余数取序（余 0 为鼠、1 为牛，依次至 11 为猪），出生在春节前的按上一年计；星座按出生月日落在的日期区间判定，如 3 月 21 日至 4 月 19 日为白羊座、4 月 20 日至 5 月 20 日为金牛座，依此类推按 12 星座的黄道日期分界。': 'The Chinese zodiac is ordered by the remainder of (year - 4) ÷ 12 (remainder 0 is Rat, 1 is Ox, and so on up to 11 for Pig), with those born before the Spring Festival counted as the previous year; the Western zodiac is determined by the date range the birth month and day fall into, e.g. 21 March to 19 April is Aries and 20 April to 20 May is Taurus, and so on across the 12 zodiac ecliptic date boundaries.',
 '中国生肖': 'Chinese zodiac',
 '：按农历年份计算': ': calculated by lunar year',
 '鼠、牛、虎、兔、龙、蛇、马、羊、猴、鸡、狗、猪': 'Rat, Ox, Tiger, Rabbit, Dragon, Snake, Horse, Goat, Monkey, Rooster, Dog, Pig',
 '注：本工具按公历年份估算，1-2 月初出生者可能需按农历调整': 'Note: this tool estimates by Gregorian year; those born in early January or February may need adjustment by the lunar calendar.',
 'Note:本工具按公历年份估算，1-2 月初出生者可能需按农历调整': 'Note: this tool estimates by Gregorian year; those born in early January or February may need adjustment by the lunar calendar.',
 '西方星座': 'Western zodiac',
 '：按公历日期计算': ': calculated by Gregorian date',
 '白羊(3/21-4/19) 金牛(4/20-5/20) 双子(5/21-6/21) 巨蟹(6/22-7/22)': 'Aries (3/21-4/19) Taurus (4/20-5/20) Gemini (5/21-6/21) Cancer (6/22-7/22)',
 '狮子(7/23-8/22) 处女(8/23-9/22) 天秤(9/23-10/23) 天蝎(10/24-11/22)': 'Leo (7/23-8/22) Virgo (8/23-9/22) Libra (9/23-10/23) Scorpio (10/24-11/22)',
 '射手(11/23-12/21) 摩羯(12/22-1/19) 水瓶(1/20-2/18) 双鱼(2/19-3/20)': 'Sagittarius (11/23-12/21) Capricorn (12/22-1/19) Aquarius (1/20-2/18) Pisces (2/19-3/20)',
 '📚 深度解析：生肖星座计算器': '📚 In-Depth: Zodiac Calculator',
 '由生日推生肖与星座。': 'Derive the Chinese zodiac and Western zodiac from a birthday.',
 '填写出生日期快速得知星座与生肖，用于社交或资料填写。': 'Enter a birth date to quickly learn your Western zodiac sign and Chinese zodiac animal, useful for social profiles or filling in forms.',
 '1990 年生 → 生肖马；生日 4-10 → 白羊座（3/21–4/19）。': 'Born in 1990 → Chinese zodiac Horse; birthday 4-10 → Aries (3/21-4/19).',
 '星座按阳历？': 'Is the zodiac based on the solar calendar?',
 '是，按公历出生月日。': 'Yes, by the Gregorian birth month and day.',
 '生肖是按立春还是春节算？': 'Is the Chinese zodiac based on Lichun or the Spring Festival?',
 '民俗与命理口径不一：有按春节（正月初一）也有按立春划分，页面按常见口径给出结果，精确排盘建议咨询专业历法工具。': 'Folk and fortune-telling conventions differ: some use the Spring Festival (the first day of the first lunar month) and some use Lichun, and the page gives its result by the common convention, so for an exact chart consult a professional calendar tool.',
 '生肖星座计算。日常生活工具，贴近生活，实用便捷。': 'Zodiac Calculator. A daily-life tool that is practical and convenient.',
}, ind=IND)

# ---------------- 2. YAML/JSON 互转 ----------------
apply_tool('yaml-json', 'YAML/JSON 互转', 'YAML/JSON Converter', {
 '📖 查看「YAML/JSON 互转使用指南」': '📖 View the "YAML/JSON Converter Guide"',
 '📖 YAML 语法说明': '📖 YAML syntax notes',
 '：必须用空格，不能用 Tab，相同层级缩进相同': ': must use spaces rather than tabs, with the same indentation for the same level',
 '键值对': 'Key-value pairs',
 '：key: value（冒号后有空格）': ': key: value (with a space after the colon)',
 '：用 - 开头，或 [a, b, c]': ': start with -, or use [a, b, c]',
 '对象': 'Objects',
 '：用 {key: value} 内联格式': ': use the inline {key: value} format',
 '：通常无需引号，含特殊字符时用单/双引号': ': usually no quotes are needed; use single or double quotes when special characters are present',
 '多行字符串': 'Multi-line strings',
 '：| 保留换行，> 折叠换行': ': | keeps line breaks, > folds them',
 '注释': 'Comments',
 '：# 开头': ': start with #',
 '布尔': 'Booleans',
 '空值': 'Null values',
 '：null 或 ~': ': null or ~',
 '📚 深度解析：YAML/JSON 互转': '📚 In-Depth: YAML/JSON Converter',
 '配置格式互转。': 'Converting between configuration formats.',
 '把 Kubernetes 或 CI 配置在 YAML 与': 'Convert Kubernetes or CI configuration between YAML and',
 '间互转，便于程序读取或人读。': 'so it is easy for programs to parse or people to review.',
 '注释保留？': 'Are comments preserved?',
 'JSON 无注释，转换即丢。': 'JSON has no comments, so they are lost on conversion.',
 '注释会保留吗？': 'Will comments be preserved?',
 '不会。YAML 注释在解析为数据结构时即被丢弃，转向 JSON 或转回 YAML 都不保留注释，需另行备份。': 'No. YAML comments are discarded as soon as the document is parsed into a data structure; converting to JSON or back to YAML both drop them, so back them up separately.',
 'YAML/JSON 互转。日常生活工具，贴近生活，实用便捷。': 'YAML/JSON Converter. A daily-life tool that is practical and convenient.',
}, ind=IND)

print('DONE batch8: 2 tools')
