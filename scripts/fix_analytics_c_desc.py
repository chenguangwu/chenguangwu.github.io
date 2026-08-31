#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Analytics-C：高曝光低点击工具页的中文描述精修。

背景
----
_build.py 的 extract_zh_desc() 曾从页面首个 <p> 提取 meta description，
但未剔除 <script> 块，导致部分页面的 description 变成 JS 里的校验提示串
（如「误差范围必须 > 0」「p 必须在 0~1 之间」），搜索结果摘要不可读 → 零点击。
根因已在 _build.py 修复；本脚本负责为这些页面补写**真实、具体**的中文描述，
避免回落到模板化套话（如「XX计算器。科学研究工具，采用标准科学公式，计算精准。」）。

落点
----
i18n/tools/<industry>.json → <slug>.zh-CN.intro / .desc / .h1
intro 是 extract_zh_desc 的最高优先级来源，且不会被 _build.py 覆盖。

用法
----
    python3 scripts/fix_analytics_c_desc.py          # 应用全部修复
    python3 scripts/fix_analytics_c_desc.py --dry    # 只看将要改什么

改写原则（务必遵守）
--------------------
1. 必须读完页面真实功能再写，禁止套话、禁止编造页面没有的能力。
2. intro 结构：用途 + 关键输入 + 具体输出（60~110 字，超过 120 会被截断）。
3. h1 与 title 保持一致；改 title 前先确认页面 JS 不读 document.title
   （模板化生成器的 calc() 靠 <title> 关键词分派分支，改标题可能改行为）。
"""
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
I18N_DIR = os.path.join(ROOT, 'i18n', 'tools')

# key = industry, value = { slug: {字段: 新值} }
# 只写需要改的字段，未列出的保持原样。
FIXES = {
    'science': {
        'sample-size-calculator': {
            'h1': '样本量计算器',
            'desc': '样本量计算器：设定置信水平与误差范围，反推调查或实验需要多少个样本。',
            'intro': '输入总体大小、置信水平、误差范围和预期比例，计算问卷调查或 A/B 实验所需的最小样本量，自动做有限总体修正，并给出从 z 临界值到向上取整的完整分步推导。',
        },
        'barcode-pharmacode': {
            'desc': 'Pharmacode 条形码：输入 1~131070 的整数，生成药品二进制条码。',
            'intro': '输入 1 到 131070 之间的整数，生成 Pharmacode（药品二进制码）条形码。该码制由宽窄条组合表示数值，用于药品包装的印刷与识别。',
        },
        'nato-phonetic': {
            'desc': 'NATO 音标字母：把文本逐字母转成 Alpha、Bravo、Charlie 拼读。',
            'intro': '输入任意文本，逐字母转换为 NATO 音标字母（Alpha、Bravo、Charlie……），避免电话、无线电和客服场景中 B 与 D、M 与 N 等发音混淆，附完整字母表对照。',
        },
        'physics-calculator': {
            'desc': '物理计算器：选定公式后填入已知变量，自动解出未知量。',
            'intro': '覆盖力学、热学、电磁学等分类的物理公式，选定公式后填入已知变量，自动求解未知量并给出代入过程，适合物理作业、实验数据处理和工程估算。',
        },
        'median-calculator': {
            'desc': '中位数计算器：输入一组数据，自动排序并取中间值，不受极端值影响。',
            'intro': '输入用逗号或空格分隔的一组数字，自动排序后取中位数（偶数个时取中间两个数的平均值），不受极端值干扰，适合成绩、薪资、房价等偏态数据的集中趋势分析。',
        },
    },
    'it': {
        'id-card-generator': {
            'h1': '随机身份证号生成器',
            'desc': '随机身份证号生成器：可按地区、性别、出生年份生成，也可反向解析号码归属。',
            'intro': '按地区、出生日期和性别生成符合 GB 11643 校验码规则的 18 位身份证号码，也可反向解析任意号码的归属地、出生日期与性别。生成结果仅用于测试，不可用于真实身份登记。',
        },
    },
    'video': {
        'video-speed': {
            'h1': '视频倍速时长计算器',
            'desc': '视频倍速时长计算器：输入原时长与倍速，算出实际观看时间、节省量和时间码。',
            'intro': '输入视频原时长与播放倍速，立刻算出倍速后的观看时长与节省时间；支持时间码 HH:MM:SS:FF 与秒互转、按帧率换算帧数，也可用目标时长反推所需倍速。附常见倍速对照表。',
        },
        'subtitle-tool': {
            'desc': '字幕工具：导入 SRT 内容，批量平移或缩放时间轴，修正音画不同步。',
            'intro': '粘贴或导入 SRT 字幕内容，按毫秒整体平移时间轴，或按倍率缩放以匹配变速后的视频，也可批量调整字幕格式，用于修正字幕与画面不同步。',
        },
    },
    'finance': {
        'lottery-odds-calculator': {
            'h1': '彩票中奖概率计算器',
            # 原值为 "&#127922; 彩票中奖概率计算器"：emoji 实体被二次转义后显示为字面量
            'desc': '彩票中奖概率计算器：内置双色球、大乐透等玩法，计算各奖级中奖概率与组合数。',
            'intro': '内置双色球、大乐透、福彩 3D、七乐彩的玩法规则，一键算出各奖级的中奖概率与总组合数，也支持自定义总号码数与选取号码数。附概率可视化和通俗类比，直观看懂中奖难度。',
        },
    },
    # ---- 第二批：Bing 展示 ≥2 且零点击的其余页面（analytics_traffic_by_source.csv）----
    'math': {
        'formula-calculator': {
            'desc': '常用公式速查：内置数学、物理、化学、几何公式，填参数即算，附单位口径提示。',
            'intro': '汇总数学、物理、化学、几何的常用公式，选定公式后填入已知参数即时算出结果，并提示统一的单位口径与参数范围，适合作业验算、工程复核和数据分析。',
        },
    },
    'life': {
        'radiation-converter': {
            'desc': '辐射剂量换算器：Gy、rad、mGy 与 Sv、mSv、μSv、rem 之间一键互转。',
            'intro': '输入数值并选定源单位，在吸收剂量（戈瑞 Gy、拉德 rad、毫戈 mGy）与当量剂量（希沃特 Sv、毫希 mSv、微希 μSv、雷姆 rem）之间换算，便于体检报告、影像检查和放射防护场景的读数对照。',
        },
    },
    'agriculture': {
        'canopy-coverage': {
            'desc': '作物冠层覆盖度估算器：支持种植参数法与照片网格法两种算法。',
            'intro': '提供两种估算方式：按行距、株距、冠层直径与重叠率计算，或用照片网格法统计绿色格数占比；输出冠层覆盖度与光合截获能力，辅助判断封行期与群体长势。',
        },
    },
    'marketing': {
        'marketing-ltv-calculator': {
            'desc': 'LTV 客户终身价值计算器：简单模式与详细模式，可一并看 LTV:CAC。',
            'intro': '简单模式按客单价、年购买频次、客户生命周期和毛利率估算 LTV；详细模式改用月均收入、月流失率与获客成本 CAC，并给出 LTV:CAC 比值，判断获客投入是否划算。',
        },
    },
    'nephrology': {
        'uacr': {
            'desc': 'UACR 计算器：输入尿白蛋白与尿肌酐，得出比值并对照分期。',
            'intro': '输入尿白蛋白（mg/L）与尿肌酐（mmol/L），计算尿白蛋白肌酐比值 UACR，比单次尿蛋白浓度更稳定，用于糖尿病、高血压人群的早期肾损伤筛查与随访。',
        },
    },
    'fengshui': {
        'fengshui-calculator': {
            'desc': '风水罗盘（娱乐版）：输入房屋朝向角度，查看对应八卦方位。',
            'intro': '输入房屋朝向角度，或直接选择坐向与房型，查看对应的八卦方位与卦象说明。结果为传统文化角度的方位参考，仅供娱乐，不构成风水建议或决策依据。',
        },
    },
    'legal': {
        'arbitration-fee': {
            'desc': '仲裁费计算器：选择仲裁机构、填入争议金额，估算仲裁费用。',
            'intro': '选择仲裁机构并填入争议金额，依据《仲裁委员会仲裁收费办法》及机构规则（参考贸仲、北仲标准）估算受理费与处理费，便于申请仲裁前预估维权成本。',
        },
    },
    'fishery': {
        'mesh-size-guide': {
            'desc': '网目尺寸查询器：按鱼种查最小可捕规格，也可由网目反查目标体长。',
            'intro': '按鱼种查询合规网目尺寸与最小可捕体长、体重，也可由网目尺寸反查对应的目标最小体长，帮助选择合规网具、减少幼鱼误捕。数据仅供参考，以当地渔业规定为准。',
        },
    },
    'livestock': {
        'heat-stress-index': {
            'desc': '热应激指数 THI：输入温度湿度与动物类型，评估热应激风险等级。',
            'intro': '输入温度、相对湿度和动物类型（可补风速），计算温湿度指数 THI，按等级判定正常、警戒、危险或紧急状态，用于夏季畜禽舍的降温与通风调度预警。',
        },
    },
    'reproductive-medicine': {
        'testicular-volume': {
            'desc': '睾丸体积测量器：Prader 计对比法与椭球公式法，成人参考 15~25 mL。',
            'intro': '支持两种算法：直接填入 Prader 睾丸计比对所得的体积，或用长、宽、高按椭球公式计算；分别输出左右侧睾丸体积，成人参考范围约 15~25 mL，结果仅供自查参考。',
        },
    },
    'cardiology': {
        'myocardial-bridge': {
            'desc': '心肌桥评估器：按收缩期压缩程度做 Nobel 分级，评估临床意义。',
            'intro': '输入冠脉造影或 CTA 测得的收缩期压缩程度、舒张期残余狭窄、心肌桥长度与深度，进行 Nobel 分级并评估临床意义与处理策略，供影像报告解读参考。',
        },
    },
    'design': {
        'image-to-ascii': {
            'desc': '图片转 ASCII 字符画：可调宽度、对比度、亮度与字符集，本地处理不上传。',
            'intro': '上传图片后在浏览器本地处理，用 Canvas 读取像素亮度映射为 ASCII 字符，可调节输出宽度、对比度、亮度和字符集，实时预览并复制结果，图片不会上传到服务器。',
        },
    },
}


def main():
    dry = '--dry' in sys.argv
    changed = 0
    missing = []

    for industry, slugs in FIXES.items():
        fp = os.path.join(I18N_DIR, industry + '.json')
        if not os.path.isfile(fp):
            missing.append('文件不存在: ' + fp)
            continue
        with open(fp, encoding='utf-8') as f:
            data = json.load(f)

        file_dirty = False
        for slug, fields in slugs.items():
            entry = data.get(slug)
            if entry is None:
                missing.append('%s/%s 条目不存在' % (industry, slug))
                continue
            zh = entry.setdefault('zh-CN', {})
            for k, new in fields.items():
                old = zh.get(k)
                if old == new:
                    continue
                print('  %s/%s.%s' % (industry, slug, k))
                print('    旧: %s' % (old,))
                print('    新: %s' % (new,))
                zh[k] = new
                file_dirty = True
                changed += 1

        if file_dirty and not dry:
            # i18n/tools/*.json 统一 indent=2，结尾单个换行
            with open(fp, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
                f.write('\n')
            print('  -> 已写入 %s' % os.path.relpath(fp, ROOT))

    print('\n共变更 %d 个字段%s' % (changed, '（dry-run 未落盘）' if dry else ''))
    if missing:
        print('未找到：')
        for m in missing:
            print('  - ' + m)
    return 0


if __name__ == '__main__':
    sys.exit(main())
