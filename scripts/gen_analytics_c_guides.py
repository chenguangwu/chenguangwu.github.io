# -*- coding: utf-8 -*-
"""Analytics-C 配套使用指南：为 21 个高曝光低点击的工具页补写真实使用指南。

选取依据：analytics_traffic_by_source.csv 中 Bing 展示量较高但点击为 0 的页面
（design/image-to-ascii 已有指南，跳过）。内容全部基于各工具页真实控件、公式与
输出编写，禁止套话。

运行：python3 scripts/gen_analytics_c_guides.py
- 生成 guides/<slug>-guide.html
- 合并 json/guides.json（tool 用 basename，common.js 按 basename 匹配）
- 向 guides/index.html 的「全部指南」段追加条目
- 相关工具区读取工具页真实 <title> 作链接文字（复用 related-tools-curated.json）
"""
import html
import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GUIDES_DIR = os.path.join(ROOT, 'guides')
SITE = 'https://chenguangwu.github.io'
DATE = '2026-08-31'

GUIDES = [
 {'slug': 'id-card-generator', 'tool': 'tools/it/id-card-generator.html', 'name': '随机身份证号生成器',
  'desc': '随机身份证号生成与解析使用指南：按省份、性别、年龄批量生成符合 GB 11643 校验规则的测试号码。',
  'intro': '按省份、性别和年龄范围批量生成符合 GB 11643 校验码规则的 18 位号码，也能反向解析任意号码的归属地、出生日期与性别。生成结果仅供开发测试，不对应任何真实自然人。',
  'features': ['按 GB 11643 规则生成，末位校验码自动计算，号码本身合法',
               '可指定省份、性别（男/女/随机）与年龄范围（默认 18~65 岁）',
               '批量生成 1 / 5 / 10 / 50 / 100 条，一键复制或清空',
               '反向解析：输入号码查出归属地、出生日期与性别',
               '附身份证号码结构说明（地址码 / 出生日期码 / 顺序码 / 校验码）',
               '纯浏览器本地生成，数据不上传'],
  'scenarios': ['开发与测试：批量填充需要身份证格式的测试数据',
                '表单校验：验证输入框的 18 位长度与校验位逻辑',
                '学习理解：通过解析功能看清号码各段的含义'],
  'steps': ['选择生成数量（1 / 5 / 10 / 50 / 100）',
            '设定性别与年龄范围，选择省份或使用随机省份',
            '点击「生成」得到号码列表',
            '点击「复制」取用，或「清空」后重新生成',
            '需要核对时，把号码填入解析区查看归属地与出生日期'],
  'tips': ['第 17 位顺序码奇数为男、偶数为女',
           '末位校验码按 ISO 7064 MOD 11-2 计算，余数为 10 时记为 X',
           '年龄范围会直接影响生成的出生日期段',
           '解析功能对任意 18 位号码都可用，不限于本页面生成的号码'],
  'faqs': [('生成的号码是真实存在的吗？', '不是。号码符合编码与校验码规则，但不对应任何真实个人，仅供测试使用。'),
           ('为什么有的号码末位是 X？', '校验码按 MOD 11-2 计算，当余数为 10 时按规定记为罗马数字 X，属正常结果。'),
           ('可以拿去注册网站吗？', '不可以。用于真实注册可能违反平台规则乃至法律，请仅作为测试数据。')]},

 {'slug': 'video-speed', 'tool': 'tools/video/video-speed.html', 'name': '视频倍速时长计算器',
  'desc': '视频倍速时长计算使用指南：算倍速观看时间、时间码换算、反推所需倍速。',
  'intro': '输入视频原时长与播放倍速，立刻算出倍速后的观看时长与节省时间；支持时间码与秒互转、按帧率换算帧数，也可用目标时长反推需要的倍速，并附常见倍速对照表。',
  'features': ['按时 / 分 / 秒 / 毫秒输入原时长，设定倍速后得出实际观看时长与节省量',
               '时间码 HH:MM:SS:FF 与秒双向互转，帧率可设（常见 24 / 25 / 30 fps）',
               '反向计算：填入目标时长，反推需要的播放倍速',
               '常见倍速对照表（0.25x~4x），含节省百分比与适合场景',
               '计算历史保存在浏览器本地，可回看复用',
               '结果与时间码一键复制'],
  'scenarios': ['刷课前估算：这门课用 1.5 倍速看完需要多久',
                '剪辑排期：把时间码换算成秒，安排片段与字幕',
                '配音对齐：按目标时长反推该用多少倍速'],
  'steps': ['填入原时长的时 / 分 / 秒 / 毫秒',
            '设定播放速度（可用 0.5x / 1x / 1.25x / 1.5x / 2x 等快捷按钮）',
            '查看倍速后的时长、节省时间与节省百分比',
            '需要时切到时间码区，输入 HH:MM:SS:FF 并设定帧率换算',
            '已知目标时长时，填入「目标时长(秒)」反推所需倍速'],
  'tips': ['倍速后时长 = 原时长 ÷ 倍速',
           '帧率影响时间码精度：国内电视常用 25 fps，影视常用 24 fps',
           '结果会按帧取整，与播放器显示可能有几帧误差',
           '历史记录存于浏览器本地，清除浏览器数据会一并清除'],
  'faqs': [('为什么和播放器显示的时间略有出入？', '播放器常按帧取整或对音频做变速处理，会产生几秒差异，属正常现象。'),
           ('支持很慢或很快的倍速吗？', '支持 0.1x 到 16x 的输入范围，超出范围请分次计算。')]},

 {'slug': 'sample-size-calculator', 'tool': 'tools/science/sample-size-calculator.html', 'name': '样本量计算器',
  'desc': '样本量计算使用指南：按置信水平与误差范围反推需要多少样本，含有限总体修正。',
  'intro': '输入总体大小、置信水平、误差范围和预期比例，计算问卷调查或 A/B 实验所需的最小样本量，自动做有限总体修正，并给出从 z 临界值到向上取整的完整分步推导。',
  'features': ['支持 90% / 95% / 99% / 99.9% 四档置信水平',
               '可选有限总体修正：填入总体大小 N 后自动折算',
               '预期比例 p 可调，未知时取 0.5 即最保守估计',
               '输出 z 临界值、理论样本量 n0 与取整后的推荐样本量',
               '展示完整分步计算过程，便于写进报告或论文',
               '纯前端计算，数据不上传'],
  'scenarios': ['问卷调研：确定要回收多少份问卷才够用',
                'A/B 实验：估算每组最少需要多少流量',
                '学术研究：为论文方法部分提供样本量依据'],
  'steps': ['填写误差范围 E（如 5 表示 ±5%）',
            '选择置信水平（常用 95%）',
            '填写预期比例 p，未知时保持 0.5',
            '若总体有限，填入总体大小 N 启用修正',
            '点击「计算」，查看推荐样本量与分步推导'],
  'tips': ['p = 0.5 时 p(1−p) 最大，样本量最保守，适合未知比例的情形',
           '误差范围减半，所需样本量约变为原来的 4 倍',
           '有限总体修正会显著减少样本量，总体越大修正效果越弱',
           '结果已向上取整，实际执行时建议再预留 10%~20% 的无效样本'],
  'faqs': [('误差范围该填 5 还是 0.05？', '按页面单位填写即可：填 5 表示 ±5%，与 p 的取值口径保持一致。'),
           ('为什么推荐值比理论值大？', '理论值 n0 通常为小数，实际调查必须取整数，故向上取整。')]},

 {'slug': 'lottery-odds-calculator', 'tool': 'tools/finance/lottery-odds-calculator.html', 'name': '彩票中奖概率计算器',
  'desc': '彩票中奖概率计算使用指南：双色球、大乐透、福彩3D、七乐彩各奖级概率与组合数。',
  'intro': '内置双色球、大乐透、福彩 3D、七乐彩的玩法规则，一键算出各奖级的中奖概率与总组合数，也支持自定义总号码数与选取号码数。附概率可视化和通俗类比，直观看懂中奖难度。',
  'features': ['四种常见玩法预设：双色球（6红+1蓝）、大乐透（5前+2后）、福彩3D（3位数）、七乐彩（选7中7）',
               '列出各等奖的中奖概率与对应组合数',
               '自定义模式：填入总号码数 N、选取数 K、匹配数 M 自行计算',
               '概率可视化：用图形对比不同奖级的难度',
               '通俗类比：把极小概率换算成更容易理解的说法',
               '纯浏览器本地计算'],
  'scenarios': ['了解真实中奖难度，避免被"差一个号"的错觉误导',
                '对比不同玩法的一等奖概率高低',
                '学习组合数 C(n, k) 的实际应用'],
  'steps': ['点击选择彩票类型（双色球 / 大乐透 / 福彩3D / 七乐彩）',
            '查看该玩法各奖级的中奖概率与组合数',
            '需要自定义时，切换到「自定义组合」并填入 N、K、M',
            '结合概率可视化与通俗类比理解数量级',
            '可用「匹配指定号码数概率」单独查某一情形'],
  'tips': ['双色球一等奖约 1/17,721,088，大乐透约 1/21,425,712',
           '各奖级概率之和才是"中任意奖"的概率，远大于一等奖概率',
           '自定义模式用的是组合数公式，不考虑顺序',
           '本工具只算概率，不预测号码'],
  'faqs': [('双色球和大乐透哪个更容易中一等奖？', '双色球一等奖组合数约 1772 万，大乐透约 2143 万，双色球概率略高，但两者都极其困难。'),
           ('为什么"中任意奖"的概率比一等奖高很多？', '因为低等级奖项（如中 1~2 个号）的概率远高于一等奖，累加后总和明显上升。')]},

 {'slug': 'factorial-calculator', 'tool': 'tools/science/factorial-calculator.html', 'name': '阶乘计算器',
  'desc': '阶乘计算使用指南：计算 n! 精确值，支持大整数与位数统计。',
  'intro': '输入非负整数 n，计算 n! = n × (n−1) × … × 2 × 1 的精确结果，支持大整数运算并显示结果位数，适合排列组合学习与公式验算。',
  'features': ['计算 n! 的精确整数值，不做浮点近似',
               '支持大整数，结果显示完整位数',
               '超出常规范围时自动切换科学计数法显示',
               '0! 与 1! 按定义返回 1',
               '实时计算，输入即出结果',
               '纯前端运行'],
  'scenarios': ['排列组合题目验算：C(n,k)、P(n,k) 的组成部分',
                '概率论与统计学习中的阶乘推导',
                '工程与算法中估算阶乘量级'],
  'steps': ['在输入框填入非负整数 n',
            '查看 n! 的精确结果与位数',
            '数值极大时查看科学计数法近似值',
            '配合组合数、排列数工具继续计算'],
  'tips': ['0! = 1，这是数学定义而非计算错误',
           'n 越大结果增长极快，20! 已是 19 位数',
           '建议 n ≤ 10000，过大数值计算会明显变慢',
           '阶乘只接受非负整数，负数与小数无定义'],
  'faqs': [('为什么结果这么长？', '阶乘增长极快，例如 100! 有 158 位，属于正常现象。'),
           ('可以算小数的阶乘吗？', '普通阶乘只对非负整数有定义；小数需使用伽马函数，本工具不支持。')]},

 {'slug': 'formula-calculator', 'tool': 'tools/math/formula-calculator.html', 'name': '公式计算器',
  'desc': '公式计算器使用指南：按分类检索公式，填入已知量自动求解未知量并展示步骤。',
  'intro': '覆盖代数、几何、统计等常用公式，支持关键词搜索；选定公式后填入已知变量，自动解出未知量并给出代入过程，适合作业、实验数据与工程估算。',
  'features': ['公式按分类组织（代数 / 几何 / 统计等），可用搜索框快速定位',
               '选定公式后填入已知变量，自动求解未知量',
               '展示代入数值后的推导步骤，便于核对',
               '常见公式附带适用条件与单位说明',
               '支持反复修改输入即时重算',
               '纯前端运行，数据不上传'],
  'scenarios': ['学生作业：代入已知量求二次方程根、几何面积等',
                '实验数据处理：用统计公式反推均值、标准差',
                '工程估算：把现场测量值代入经验公式算结果'],
  'steps': ['在搜索框输入关键词（如"二次方程""面积"）定位公式',
            '点击公式进入计算面板',
            '在已知变量框填入数值，留出待求变量空',
            '点击「计算」得到未知量结果与步骤',
            '需要换数时直接修改输入框即时重算'],
  'tips': ['未知量留空、其余填全，工具才知求解哪个变量',
           '注意单位一致：混合单位会得出错误量级',
           '搜索不到时换个近义词，如"方差"可试"标准差"',
           '结果带步骤，建议对照检查代入是否抄错'],
  'faqs': [('公式搜不到怎么办？', '尝试更通用的关键词或近义词；本工具内置常用公式，非常用公式可先用分类浏览。'),
           ('步骤和手算不一致？', '多半是单位或变量代入位置不同，请按步骤逐项核对已知量。')]},

 {'slug': 'radiation-converter', 'tool': 'tools/life/radiation-converter.html', 'name': '辐射量单位换算器',
  'desc': '辐射量单位换算使用指南：吸收剂量、当量剂量、活度与照射量之间的单位互转。',
  'intro': '在 Gy/rad（吸收剂量）、Sv/rem（当量剂量）、Bq/Ci（活度）、R（照射量）等辐射相关单位间换算，按类别选择后输入数值即得目标单位结果，适合放射、核医学与环境监测场景。',
  'features': ['按类别换算：吸收剂量(Gy↔rad)、当量剂量(Sv↔rem)、活度(Bq↔Ci)、照射量(R)',
               '输入一个单位数值，自动给出对应单位结果',
               '常数已内置（如 1 Gy = 100 rad，1 Sv = 100 rem，1 Ci = 3.7e10 Bq）',
               '结果按常用精度显示',
               '纯前端换算，数据不上传'],
  'scenarios': ['放射科 / 核医学：读片与报告中的剂量单位统一',
                '环境监测：把不同仪器的活度读数换成统一单位',
                '学习备考：理解各辐射量之间的换算关系'],
  'steps': ['选择换算类别（吸收剂量 / 当量剂量 / 活度 / 照射量）',
            '在源单位框输入数值',
            '查看目标单位自动换算结果',
            '需要反向时切换源与目标单位再输入'],
  'tips': ['吸收剂量看"能量沉积"(Gy/rad)，当量剂量看"生物效应"(Sv/rem)，二者不要混用',
           '1 Gy = 100 rad，1 Sv = 100 rem，记住 100 倍关系即可心算',
           '活度 Bq 与 Ci 差约 10^10 量级，大数建议用科学计数法',
           '照射量 R 常用于老式仪器，新标准多用 C/kg'],
  'faqs': [('Gy 和 Sv 有什么区别？', 'Gy 衡量吸收的能量多少，Sv 在其基础上乘组织权重，反映对人体危害，适用场景不同。'),
           ('Ci 和 Bq 哪个更常用？', '国际通用 Bq，国内部分老资料仍用 Ci，1 Ci = 3.7×10^10 Bq。')]},

 {'slug': 'median-calculator', 'tool': 'tools/science/median-calculator.html', 'name': '中位数计算器',
  'desc': '中位数计算使用指南：输入一组数字，自动排序取中间值，不受极端值影响。',
  'intro': '输入用逗号或空格分隔的一组数字，自动排序后取中位数（偶数个时取中间两个数的平均值），不受极端值干扰，适合成绩、薪资、房价等偏态数据的集中趋势分析。',
  'features': ['支持逗号、空格、换行分隔的一批数字',
               '自动排序后定位中间值',
               '偶数个数据时取中间两数平均值',
               '同步显示排序后的数据，便于核对',
               '与均值、四分位数可配合分析',
               '纯前端计算'],
  'scenarios': ['薪资分析：用中位数避免被极高值拉偏',
                '成绩统计：看典型水平而非平均',
                '房价 / 收入：偏态分布下比均值更稳健'],
  'steps': ['在输入框粘贴或输入一组数字（逗号或空格分隔）',
            '点击「计算」得到排序结果与中位数',
            '核对排序序列，确认没有录入错误',
            '配合均值、众数工具做完整描述统计'],
  'tips': ['中位数比均值更抗极端值，偏态数据优先看中位数',
           '数据个数为偶数时，取中间两数平均',
           '空值或文本会被忽略，建议先清洗数据',
           '样本量很小时中位数代表性有限'],
  'faqs': [('中位数和均值该看哪个？', '数据分布对称看均值，偏态或有离群值看中位数更稳健。'),
           ('为什么我输入后没反应？', '多半含非数字字符或分隔不对，检查是否有中文逗号或字母。')]},

 {'slug': 'subtitle-tool', 'tool': 'tools/video/subtitle-tool.html', 'name': '字幕时间轴调整工具',
  'desc': '字幕时间轴调整使用指南：批量平移或缩放 SRT 时间轴，修正音画不同步。',
  'intro': '粘贴或导入 SRT 字幕内容，按毫秒整体平移时间轴，或按倍率缩放以匹配变速后的视频，也可批量调整字幕格式，用于修正字幕与画面不同步。',
  'features': ['整体平移：把所有时间码向后 / 向前移动指定毫秒',
               '按比例缩放：按倍率拉伸或压缩时间轴以匹配变速视频',
               '支持粘贴 SRT 文本或整段导入',
               '逐条时间码实时预览，避免错位',
               '结果可复制或导出',
               '纯前端处理，字幕不上传'],
  'scenarios': ['视频变速后字幕对不上：按比例缩放时间轴',
                '字幕整体偏移：统一平移几秒修正',
                '多语种字幕对齐：复用同一份时间轴'],
  'steps': ['把 SRT 内容粘贴到输入框',
            '选择「平移」并填偏移毫秒，或选「缩放」并填倍率',
            '点击「应用」预览新时间轴',
            '确认无误后复制或导出结果'],
  'tips': ['视频加速到 1.25x，时间轴应除以 1.25（缩放倍率 0.8）',
           '平移用毫秒更精细，如偏移 500ms 填 500',
           '先小批量试一段确认方向再全量处理',
           '缩放会同时改变每条字幕的起止与间隔'],
  'faqs': [('缩放倍率填多少？', '目标倍速的倒数。如视频 1.5x，字幕缩放填 1/1.5≈0.667。'),
           ('平移后首条还差一点？', '可能是源字幕本身起点偏移，再补一个小的平移量即可。')]},

 {'slug': 'canopy-coverage', 'tool': 'tools/agriculture/canopy-coverage.html', 'name': '作物冠层覆盖度估算器',
  'desc': '作物冠层覆盖度估算使用指南：几何法与网格法两种，算出田间冠层覆盖比例。',
  'intro': '提供两种方法：几何法按行距、株距、冠层直径与形状估算单株投影覆盖；网格法按照片中绿色格数占比估算实际覆盖度，适用于农业遥感、田间试验与长势评估。',
  'features': ['几何法：输入行距、株距、平均冠层直径、冠层形状与重叠率',
               '网格法：输入总格数、绿色格数与拍摄面积估算覆盖度',
               '冠层形状支持圆形 / 方形 / 椭圆三种',
               '两种结果可互相印证',
               '输出覆盖率百分比与估算面积',
               '纯前端计算'],
  'scenarios': ['田间试验：评估种植密度是否合理',
                '长势监测：定期拍照用网格法跟踪覆盖变化',
                '遥感校验：用地面实测覆盖度校正卫星反演'],
  'steps': ['选择估算方法（几何法 / 网格法）',
            '几何法：填行距、株距、冠层直径、形状与重叠率',
            '网格法：填总格数、绿色格数与拍摄面积',
            '点击「计算」得到覆盖率与对应面积',
            '两种方法结果相差大时检查输入是否准确'],
  'tips': ['几何法假设冠层规则，密植重叠率高时需填重叠率修正',
           '网格法拍照要正对地面、光照均匀，避免阴影误判',
           '冠层形状选错会高估或低估投影面积',
           '覆盖度是比例，常用来算 LAI 等衍生指标'],
  'faqs': [('几何法和网格法哪个准？', '网格法基于实测照片更贴近实际，几何法适合规则种植的快速估算。'),
           ('重叠率怎么估？', '密植时相邻冠层相交，目测相交面积占比填入，缺省可先填 0 看上限。')]},

 {'slug': 'marketing-ltv-calculator', 'tool': 'tools/marketing/marketing-ltv-calculator.html', 'name': 'LTV 客户终身价值计算器',
  'desc': 'LTV 客户终身价值计算使用指南：简易法与订阅法两种，算客户全生命周期价值与 LTV/CAC。',
  'intro': '提供简易法（客单价 × 年购买频次 × 生命周期 × 毛利率）与订阅法（月收入 × 毛利率 ÷ 月流失率）两种模型，并给出 LTV/CAC 参考与行业范围，帮你看清获客是否划算。',
  'features': ['简易法：客单价、年频次、生命周期、毛利率四要素',
               '订阅法：月收入、毛利率、月流失率三要素',
               '自动给出 LTV/CAC 比值，判断是否健康（通常 > 3）',
               '内置行业 LTV 范围参考表',
               '结果可切换查看明细',
               '纯前端计算'],
  'scenarios': ['评估获客预算：对比 LTV 与 CAC',
                '订阅业务：用流失率估算客户长期价值',
                '经营复盘：看毛利率变化对 LTV 的影响'],
  'steps': ['选择模型（简易 / 订阅）',
            '简易法填客单价、年购买频次、生命周期、毛利率',
            '订阅法填月收入、毛利率、月流失率，以及 CAC',
            '点击「计算」得到 LTV 与 LTV/CAC',
            '对照行业范围判断是否健康'],
  'tips': ['LTV/CAC > 3 通常被认为获客健康，< 1 则在亏钱拉新',
           '月流失率哪怕 5%，客户平均寿命也只有 20 个月',
           '毛利率对 LTV 影响很大，先校准毛利率',
           '订阅法对"月收入"口径要一致（含税费还是不含）'],
  'faqs': [('简易法和订阅法用哪个？', '有稳定月度订阅用订阅法；偶发复购用简易法。'),
           ('LTV/CAC 多少算好？', '一般 3 以上较健康，但要结合回收周期看现金流。')]},

 {'slug': 'uacr', 'tool': 'tools/nephrology/uacr.html', 'name': '尿白蛋白肌酐比(UACR)计算器',
  'desc': '尿白蛋白肌酐比(UACR)计算使用指南：输入尿白蛋白与肌酐，算 ACR 并分级。',
  'intro': '输入随机尿或晨尿的白蛋白浓度与肌酐浓度，计算尿白蛋白肌酐比（UACR，单位 mg/g），并给出正常、微量白蛋白尿、大量白蛋白尿的分级参考，用于早期肾损伤筛查。',
  'features': ['输入尿白蛋白（mg/L 或 mg/dL）与肌酐（mmol/L 或 mg/dL）',
               '自动按单位换算并计算 UACR（mg/g）',
               '输出分级：正常 / 微量白蛋白尿 / 大量白蛋白尿',
               '附各分级的临床意义说明',
               '纯前端计算，数据不上传'],
  'scenarios': ['体检解读：把化验单数值换算成 ACR',
                '慢病随访：糖尿病、高血压患者的肾损伤监测',
                '科普学习：理解微量白蛋白尿的意义'],
  'steps': ['选择白蛋白与肌酐的单位',
            '填入尿白蛋白浓度与肌酐浓度',
            '点击「计算」得到 UACR（mg/g）',
            '查看分级与对应说明'],
  'tips': ['UACR 用随机尿即可，受饮水影响比单次尿蛋白小',
           '单位一定要选对，mg/L 与 mg/dL 差 10 倍',
           '微量白蛋白尿通常 30~300 mg/g，>300 为大量',
           '结果仅供解读参考，确诊需结合临床与多次复查'],
  'faqs': [('ACR 和 24 小时尿蛋白有什么区别？', 'ACR 用随机尿估算，方便筛查；24 小时尿更准但麻烦，二者互补。'),
           ('单位选错会怎样？', '肌酐单位 mg/dL 与 mmol/L 差约 88 倍，选错结果会严重偏差。')]},

 {'slug': 'barcode-pharmacode', 'tool': 'tools/science/barcode-pharmacode.html', 'name': 'Pharmacode 条形码生成器',
  'desc': 'Pharmacode 条形码生成使用指南：输入 1~131070 的整数生成药品二进制码。',
  'intro': '输入 1 到 131070 之间的整数，生成 Pharmacode（药品二进制码）条形码。该码制由宽窄条组合表示数值，用于药品包装的印刷与识别，常用于医药生产线。',
  'features': ['输入 1~131070 的整数生成对应 Pharmacode',
               '实时渲染条形码图形',
               '显示编码对应的二进制条宽序列',
               '可调整条码高度与缩放',
               '结果可导出或复制',
               '纯前端生成'],
  'scenarios': ['药品包装打样：生成规定编号的 Pharmacode',
                '生产线校验：核对印刷码与系统编号一致',
                '学习理解：看清二进制码如何编码数值'],
  'steps': ['在输入框填入 1~131070 之间的整数',
            '查看自动生成的 Pharmacode 条形码',
            '需要时调整条码高度 / 缩放',
            '导出或复制用于打样'],
  'tips': ['Pharmacode 只用宽窄两种条，按二进制累加编码',
           '超出 131070 会无法编码，请分段或核对编号',
           '与 EAN/UPC 不同，Pharmacode 专为医药设计',
           '导出前确认打印分辨率满足条码识别要求'],
  'faqs': [('为什么和超市商品码不一样？', 'Pharmacode 是医药专用码，结构简单、适合高速印刷线，与零售 EAN 不同。'),
           ('编号上限是多少？', '标准 Pharmacode 可表示 1~131070。')]},

 {'slug': 'nato-phonetic', 'tool': 'tools/science/nato-phonetic.html', 'name': 'NATO 音标字母转换器',
  'desc': 'NATO 音标字母转换使用指南：把文本逐字母转成 Alpha、Bravo、Charlie 拼读。',
  'intro': '输入任意文本，逐字母转换为 NATO 音标字母（Alpha、Bravo、Charlie……），避免电话、无线电和客服场景中 B 与 D、M 与 N 等发音混淆，附完整字母表对照。',
  'features': ['输入文本逐字母转为 NATO 音标词',
               '附完整 A~Z 字母表对照',
               '数字与标点也可给出标准读法',
               '结果一键复制',
               '支持反向：音标词转回字母',
               '纯前端转换'],
  'scenarios': ['无线电 / 电话报号：清晰读出账号、车牌、呼号',
                '客服核对：避免字母听错',
                '学习记忆：熟悉标准航空 / 海事拼读'],
  'steps': ['在输入框输入要转换的文本',
            '查看逐字母的 NATO 音标词',
            '点击「复制」取用',
            '需要回读时切到反向模式'],
  'tips': ['易混对：B(Bravo)/D(Delta)、M(Mike)/N(November)、F(Foxtrot)/S(Sierra)',
           '数字也有标准词（如 3 读 Tree、5 读 Fife）',
           '转换忽略大小写，输出统一大写',
           '空格与标点通常保留原样'],
  'faqs': [('为什么用 Alpha 而不是 A？', 'A 在嘈杂环境易与其他音混淆，专用词辨识度更高。'),
           ('中文能转吗？', 'NATO 音标针对英文字母，中文需先转拼音再逐字母转换。')]},

 {'slug': 'physics-calculator', 'tool': 'tools/science/physics-calculator.html', 'name': '物理公式计算器',
  'desc': '物理公式计算使用指南：按力学、热学、电磁等分类，填已知量解未知量。',
  'intro': '覆盖力学、热学、电磁学等分类的物理公式，选定公式后填入已知变量，自动求解未知量并给出代入过程，适合物理作业、实验数据处理和工程估算。',
  'features': ['公式按力学 / 热学 / 电磁等分类组织',
               '选定公式填已知量，自动解未知量',
               '展示代入数值后的推导步骤',
               '常见公式附适用条件与单位',
               '支持即时重算',
               '纯前端运行'],
  'scenarios': ['课后作业：代入已知量求速度、力、功等',
                '实验报告：用公式反推缺失物理量',
                '工程估算：快速验算设计参数'],
  'steps': ['选择物理分类（力学 / 热学 / 电磁等）',
            '点击具体公式进入计算面板',
            '填入已知变量，留空待求量',
            '点击「计算」得到结果与步骤'],
  'tips': ['未知量留空、其余填全，工具才知求解哪个',
           '单位统一再代入，混用会差 10^3 量级',
           '带角度的量注意用度还是弧度',
           '结果带步骤，建议逐项核对代入'],
  'faqs': [('公式分类里找不到？', '可用搜索或换近义词；非常用公式建议先用分类浏览。'),
           ('步骤和教材不一致？', '多半是单位或符号定义不同，按步骤核对变量即可。')]},

 {'slug': 'fengshui-calculator', 'tool': 'tools/fengshui/fengshui-calculator.html', 'name': '风水罗盘(娱乐版)',
  'desc': '风水罗盘(娱乐版)使用指南：输入朝向角度或选方位，看八卦与二十四山对应，仅供娱乐。',
  'intro': '输入朝向角度或选择预设方位（如坐北朝南），查看对应的八卦、二十四山与方位分析；也可按房屋坐向与房型做娱乐性解读。本工具为文化趣味，不构成任何专业建议。',
  'features': ['输入朝向角度（0~360°）或选预设方位',
               '显示对应八卦、二十四山与方位范围',
               '房屋坐向 + 房型娱乐分析',
               '内置方位对照表可查阅',
               '保存历史记录便于对比',
               '纯前端，数据不上传'],
  'scenarios': ['文化兴趣：了解自家朝向对应的八卦说法',
                '装修闲聊：和朋友对照方位趣味解读',
                '学习传统：认识二十四山与罗盘角度'],
  'steps': ['在朝向角度框输入数值或选预设方位',
            '查看八卦 / 二十四山 / 方位分析',
            '切换到房屋坐向，选坐向与房型看娱乐解读',
            '需要对比时查看历史记录'],
  'tips': ['本工具明确标注"娱乐版"，结果请勿用于实际决策',
           '方位角度以正北为 0°，顺时针增加',
           '二十四山是传统罗盘细分，角度每 15° 一山',
           '解读仅供参考，专业选址请咨询相关从业者'],
  'faqs': [('结果能当装修依据吗？', '不能。本工具为娱乐性质，仅作文化趣谈，不涉及专业建议。'),
           ('角度怎么取？', '以正北为 0°、顺时针测量，常见坐北朝南为 180°。')]},

 {'slug': 'arbitration-fee', 'tool': 'tools/legal/arbitration-fee.html', 'name': '仲裁费计算器',
  'desc': '仲裁费计算使用指南：按机构与争议金额，分段算出受理费与处理费。',
  'intro': '选择仲裁机构（一般仲裁 / 贸仲 / 北仲 / 劳动仲裁等）并输入争议金额，按分段费率计算案件受理费与处理费，简易程序与劳动仲裁有特别规定，结果供费用预估参考。',
  'features': ['选择仲裁机构（一般标准 / 贸仲 CIETAC / 北仲 BAC / 劳动仲裁）',
               '输入争议金额，按分段费率累计计算',
               '区分案件受理费与案件处理费',
               '支持勾选「简易程序」适用较低标准',
               '劳动仲裁标注不收费（经费由财政保障）',
               '纯前端计算'],
  'scenarios': ['起诉前预估：算清仲裁要花多少费用',
                '对比途径：仲裁费与诉讼费孰高',
                '合规核对：确认简易程序是否适用'],
  'steps': ['选择对应的仲裁机构',
            '输入争议金额（元）',
            '如适用简易程序请勾选',
            '点击「计算」查看受理费、处理费与合计',
            '劳动仲裁会直接提示不收费'],
  'tips': ['仲裁费通常 = 标的 × 分段费率，金额越大单笔越高',
           '简易程序门槛与费率各机构不同，勾选后自动调整',
           '劳动争议仲裁不收费，对裁决不服起诉仅 10 元/件',
           '结果为预估，最终以机构收费通知为准'],
  'faqs': [('劳动仲裁要钱吗？', '不收费，仲裁经费由财政保障；对裁决不服向法院起诉的，诉讼费 10 元/件。'),
           ('受理费和处理费有什么区别？', '受理费按标的计收，处理费含办案实际开支，二者分开列示。')]},

 {'slug': 'mesh-size-guide', 'tool': 'tools/fishery/mesh-size-guide.html', 'name': '捕捞网目尺寸查询器',
  'desc': '捕捞网目尺寸查询使用指南：选鱼种，按网目查最小可捕规格或反查网目。',
  'intro': '选择鱼种（鲤、草鱼、罗非、鲶、对虾等），两种模式：按网目尺寸查对应的最小可捕体长，或按目标体长反查应选用的网目尺寸，帮助合规捕捞、保护幼体资源。',
  'features': ['内置常见鱼种的最小可捕规格参考',
               '模式一：按网目尺寸(mm)查最小可捕体长(cm)',
               '模式二：按目标体长(cm)反查网目尺寸(mm)',
               '结果显示对应关系与合规提示',
               '纯前端查询'],
  'scenarios': ['合规捕捞：确认网目不小于规定下限',
                '渔具选型：按目标规格选合适网目',
                '科普学习：理解最小可捕规格的意义'],
  'steps': ['选择鱼种',
            '选择查询方式（按网目查规格 / 按规格查网目）',
            '填入网目尺寸或目标体长',
            '点击「计算」查看对应关系'],
  'tips': ['网目过小会误捕幼鱼，多数地区有法定下限',
           '不同鱼种最小可捕规格不同，先选对鱼种',
           '反查结果建议再对照当地法规确认',
           '数值为参考，实际以主管部门规定为准'],
  'faqs': [('为什么要限制网目尺寸？', '避免捕捞幼体，保护种群补充，维持渔业可持续。'),
           ('结果能直接用作执法依据吗？', '不能，仅为工具参考，具体以当地渔业法规为准。')]},

 {'slug': 'heat-stress-index', 'tool': 'tools/livestock/heat-stress-index.html', 'name': '热应激指数(THI)预警器',
  'desc': '热应激指数(THI)预警使用指南：输入温湿度与畜种，算 THI 并分级预警。',
  'intro': '输入温度、相对湿度与动物类型（奶牛、肉牛、猪、蛋鸡、肉鸡、羊），计算温湿指数 THI 并给出热应激等级与影响提示；可选填风速做修正，用于养殖场防暑决策。',
  'features': ['输入温度(℃)、相对湿度(%)与动物类型',
               '计算 THI 并给出热应激等级（正常 / 警惕 / 危险等）',
               '内置不同畜种的 THI 等级参考表',
               '可选填风速(m/s)做修正',
               '显示对应畜种的影响说明',
               '纯前端计算'],
  'scenarios': ['夏季养殖：预判畜禽热应激风险',
                '防暑调度：按等级安排降温与喂料',
                '科普学习：理解温湿指数如何合成'],
  'steps': ['填入温度与相对湿度',
            '选择动物类型',
            '如有风速填选填项',
            '点击「计算」得到 THI 与等级',
            '对照等级表查看影响与建议'],
  'tips': ['THI 越高应激越重，奶牛约 72 以上进入警惕区',
           '高湿会放大高温危害，湿度不可忽略',
           '风速可缓解热应激，填了会更准',
           '等级表因畜种而异，务必选对动物类型'],
  'faqs': [('THI 怎么算？', '常用温湿指数公式由温度与湿度合成，本工具按内置公式给出数值与等级。'),
           ('为什么同一种温度不同动物等级不同？', '不同畜禽耐热能力不同，分级阈值按畜种分别设定。')]},

 {'slug': 'testicular-volume', 'tool': 'tools/reproductive-medicine/testicular-volume.html', 'name': '睾丸体积测量器',
  'desc': '睾丸体积测量使用指南：Prader 睾丸计对比法或椭球公式法，输出左右侧体积。',
  'intro': '支持两种方法：直接选择 Prader 睾丸计比对所得体积，或用长、宽、高按椭球公式（V = 长×宽×高×0.71/1000，单位 mm）计算；分别输出左右侧睾丸体积，成人参考范围约 15~25 mL，结果仅供自查参考。',
  'features': ['方法一：Prader 睾丸计对比，选最接近的体积(1~25 mL)',
               '方法二：椭球公式法，填长/宽/高(mm)自动计算',
               '分别输出左、右侧睾丸体积',
               '标注成人参考范围约 15~25 mL',
               '切换方法即时重算',
               '纯前端，数据不上传'],
  'scenarios': ['生殖健康自查：估算睾丸体积是否在正常范围',
                '随访对比：记录两侧体积变化',
                '科普学习：理解 Prader 法与椭球公式'],
  'steps': ['选择测量方法（Prader 对比 / 椭球公式）',
            'Prader 法：选左、右侧最接近的体积',
            '公式法：填左、右侧的长/宽/高(mm)',
            '点击「计算」得到左右侧体积与参考提示'],
  'tips': ['椭球公式 V = 长×宽×高×0.71/1000，单位用 mm、结果 mL',
           'Prader 法是临床常用对比法，需实际比对模型',
           '成人参考约 15~25 mL，低于此提示就医评估',
           '本工具仅供自查，异常请找专科医生'],
  'faqs': [('两种方法有差异正常吗？', '测量与比对都有误差，轻微差异正常；差异大建议复查或就医。'),
           ('公式里的 0.71 是什么？', '是椭球近似的经验系数（Lambert 公式），把三维尺寸折算成体积。')]},

 {'slug': 'myocardial-bridge', 'tool': 'tools/cardiology/myocardial-bridge.html', 'name': '心肌桥程度评估器',
  'desc': '心肌桥(壁冠状动脉)评估使用指南：填压缩程度与长度深度，看 Nobel 分级与处理策略。',
  'intro': '输入收缩期压缩程度、舒张期残余狭窄、心肌桥长度与深度，并勾选缺血症状、心律失常、运动试验等，按 Nobel 分级系统评估心肌桥程度与临床意义，给出处理策略参考。',
  'features': ['输入收缩期压缩(%)、舒张期残余狭窄(%)、长度(mm)、深度(mm)',
               '勾选缺血症状 / 心律失常 / 运动试验阳性',
               '按 Nobel 分级系统给出压缩程度分级',
               '内置处理策略对照表',
               '输出综合风险提示',
               '纯前端，数据不上传'],
  'scenarios': ['影像报告解读：把 CT/造影描述换算成分级',
                '医患沟通：直观说明心肌桥程度',
                '科普学习：理解表浅型与深在型差异'],
  'steps': ['填入收缩期压缩程度与舒张期残余狭窄',
            '填心肌桥长度与深度',
            '勾选是否有缺血症状、心律失常、运动试验阳性',
            '点击「评估」查看 Nobel 分级与处理策略'],
  'tips': ['收缩期压缩 <50% 多为表浅型、临床意义小',
           '深度与长度影响症状，深在型更需关注',
           '有缺血症状或运动试验阳性应提高警惕',
           '本工具仅供解读参考，确诊与处理请遵医嘱'],
  'faqs': [('心肌桥严重吗？', '多数表浅型无症状、无需处理；深在型或伴缺血才需进一步评估。'),
           ('分级看哪个指标？', '主要看收缩期压缩程度，结合深度、症状综合判断。')]},
]


TPL = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title} - ToolBox</title>
<meta name="description" content="{desc}">
<meta property="og:title" content="{title}">
<meta property="og:type" content="article">
<meta property="og:site_name" content="ToolBox">
<meta property="og:url" content="{canonical}">
<meta property="og:description" content="{desc}">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{desc}">
<meta name="twitter:image" content="https://chenguangwu.github.io/og-image.png">
<meta name="twitter:image:alt" content="ToolBox - 免费在线工具与使用指南">
<meta property="og:image" content="https://chenguangwu.github.io/og-image.png">
<meta name="twitter:card" content="summary_large_image">
<link rel="canonical" href="{canonical}">
<script type="application/ld+json">{article_json}</script>
<script type="application/ld+json">{breadcrumb_json}</script>
<script type="application/ld+json">{faq_json}</script>
<style>
:root{--primary:#FF6B35;--text:#1F2937;--muted:#6B7280;--border:#E5E7EB;--bg:#FFFAF7;}
*{box-sizing:border-box;}
body{margin:0;font-family:"Noto Sans SC","Plus Jakarta Sans",system-ui,sans-serif;color:var(--text);background:var(--bg);line-height:1.75;}
.breadcrumb a{color:var(--primary);text-decoration:none;margin-right:6px;}
.breadcrumb a:hover{text-decoration:underline;}
main{max-width:820px;margin:0 auto;padding:28px 20px 60px;}
h1{font-size:28px;margin:0 0 8px;}
.lead{font-size:16px;color:var(--muted);margin:0 0 22px;}
h2{font-size:20px;margin:28px 0 10px;color:var(--primary);}
.toc{background:#fff;border:1px solid var(--border);border-radius:14px;padding:14px 18px;margin:18px 0;}
.toc ul{margin:0;padding-left:20px;}
.toc a{color:var(--text);text-decoration:none;}
.toc a:hover{color:var(--primary);}
ul,ol{padding-left:22px;}
li{margin:8px 0;}
.related{margin-top:26px;padding:16px;background:#fff;border:1px solid var(--border);border-radius:14px;}
.related h3{margin:0 0 10px;font-size:16px;color:var(--text);}
.tool-chip{display:inline-block;margin:4px 6px 4px 0;padding:6px 12px;border:1px solid var(--border);border-radius:999px;color:var(--primary);text-decoration:none;font-size:14px;}
.tool-chip:hover{background:var(--primary);color:#fff;}
.faq{margin-top:26px;}
.faq dt{font-weight:700;margin-top:14px;}
.faq dd{margin:4px 0 0;color:var(--muted);}
.back{margin-top:30px;padding:16px;background:#fff;border:1px solid var(--border);border-radius:14px;}
.back a{color:var(--primary);font-weight:700;text-decoration:none;}
</style>
<script src="/js/analytics.js" defer></script>
<link rel="stylesheet" href="../css/common.css">
<script src="../js/common.js" defer></script>
<meta name="title-zh" content="{title} - ToolBox">
</head>
<body>
<nav class="breadcrumb"><a href="https://chenguangwu.github.io/">ToolBox</a> / <a href="https://chenguangwu.github.io/guides/index.html">使用指南</a> / <span>{title}</span></nav>
<main>
<h1>{title}</h1>
<p class="lead">{intro}</p>
<div class="toc"><strong>目录</strong><ul><li><a href="#s0">核心功能</a></li><li><a href="#s1">适用场景</a></li><li><a href="#s2">使用步骤</a></li><li><a href="#s3">实用技巧</a></li><li><a href="#s4">常见问题</a></li></ul></div>
<h2 id="s0">核心功能</h2>
<ul>{features}</ul>
<h2 id="s1">适用场景</h2>
<ul>{scenarios}</ul>
<h2 id="s2">使用步骤</h2>
<ol>{steps}</ol>
<h2 id="s3">实用技巧</h2>
<ul>{tips}</ul>
<div class="related"><h3>相关工具</h3>{related_chips}</div>
<div class="faq"><h2 id="s4">常见问题</h2><dl>{faqs}</dl></div>
<div class="back"><a href="https://chenguangwu.github.io/guides/index.html">&larr; 返回「使用指南」中心</a></div>
</main>
</body>
</html>"""


def li(items):
    return ''.join('<li>%s</li>' % html.escape(str(x)) for x in items)


def read_title(rel):
    p = os.path.join(ROOT, rel)
    if not os.path.isfile(p):
        return os.path.basename(rel).replace('-', ' ')
    s = open(p, encoding='utf-8', errors='ignore').read()
    m = re.search(r'<title>([^<]*)</title>', s)
    if not m:
        return os.path.basename(rel)
    t = re.sub(r'\s*[-–]\s*ToolBox.*$', '', m.group(1)).strip()
    return t or os.path.basename(rel)


def chip(href, name):
    return '<a class="tool-chip" href="%s">%s</a>' % (href, html.escape(name))


def main():
    curated_path = os.path.join(ROOT, 'json', 'related-tools-curated.json')
    curated = json.load(open(curated_path, encoding='utf-8')) if os.path.isfile(curated_path) else {}
    os.makedirs(GUIDES_DIR, exist_ok=True)
    guide_map = []
    for g in GUIDES:
        slug = g['slug']
        fn = '%s-guide.html' % slug
        canonical = '%s/guides/%s' % (SITE, fn)
        # 相关工具：本工具自身 + 策划表前 5 个
        rel = curated.get(g['tool'].replace('tools/', '', 1), [])[:5]
        chips = [chip('/%s' % g['tool'], read_title(g['tool']))]
        for r in rel:
            rt = 'tools/%s' % r
            chips.append(chip('/%s' % rt, read_title(rt)))
        related_chips = ''.join(chips)
        faq_json = json.dumps({
            '@context': 'https://schema.org',
            '@type': 'FAQPage',
            'mainEntity': [{'@type': 'Question', 'name': q,
                            'acceptedAnswer': {'@type': 'Answer', 'text': a}}
                           for q, a in g['faqs']]
        }, ensure_ascii=False)
        article_json = json.dumps({
            '@context': 'https://schema.org', '@type': 'Article',
            'headline': g['name'], 'description': g['desc'],
            'author': {'@type': 'Organization', 'name': 'ToolBox'},
            'datePublished': DATE, 'dateModified': DATE,
            'mainEntityOfPage': {'@type': 'WebPage', '@id': canonical}
        }, ensure_ascii=False)
        breadcrumb_json = json.dumps({
            '@context': 'https://schema.org', '@type': 'BreadcrumbList',
            'itemListElement': [
                {'@type': 'ListItem', 'position': 1, 'name': 'ToolBox', 'item': SITE + '/'},
                {'@type': 'ListItem', 'position': 2, 'name': '使用指南', 'item': SITE + '/guides/index.html'},
                {'@type': 'ListItem', 'position': 3, 'name': g['name'], 'item': canonical}
            ]
        }, ensure_ascii=False)
        page = (TPL
            .replace('{title}', html.escape(g['name']))
            .replace('{desc}', html.escape(g['desc']))
            .replace('{canonical}', canonical)
            .replace('{intro}', html.escape(g['intro']))
            .replace('{features}', li(g['features']))
            .replace('{scenarios}', li(g['scenarios']))
            .replace('{steps}', li(g['steps']))
            .replace('{tips}', li(g['tips']))
            .replace('{related_chips}', related_chips)
            .replace('{faqs}', ''.join('<dt>%s</dt><dd>%s</dd>' % (html.escape(q), html.escape(a)) for q, a in g['faqs']))
            .replace('{article_json}', article_json)
            .replace('{breadcrumb_json}', breadcrumb_json)
            .replace('{faq_json}', faq_json))
        open(os.path.join(GUIDES_DIR, fn), 'w', encoding='utf-8').write(page)
        guide_map.append({'tool': os.path.basename(g['tool']),
                          'guide': '../../guides/%s' % fn,
                          'title': g['name'] + '使用指南'})
        print('OK: guides/%s' % fn)

    # 合并 guides.json（按 basename 去重，跳过已注册）
    jf = os.path.join(ROOT, 'json', 'guides.json')
    old = json.load(open(jf, encoding='utf-8')) if os.path.isfile(jf) else []
    existing = {m['tool'] for m in old}
    merged = old + [m for m in guide_map if m['tool'] not in existing]
    json.dump(merged, open(jf, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
    print('guides.json 合并完成，共 %d 条（新增 %d）' % (len(merged), len(guide_map) - len([m for m in guide_map if m['tool'] in existing])))

    # 向 guides/index.html 的「全部指南」段追加条目
    ip = os.path.join(GUIDES_DIR, 'index.html')
    if os.path.isfile(ip):
        s = open(ip, encoding='utf-8').read()
        new_li = ''.join(
            '<li><a href="https://chenguangwu.github.io/guides/%s-guide.html">%s使用指南</a>'
            '<span style="color:var(--muted);font-size:13px;"> — %s</span></li>'
            % (g['slug'], html.escape(g['name']), html.escape(g['desc'])) for g in GUIDES)
        m = re.search(r'全部指南</h2>', s)
        if m:
            already = all(('guides/%s-guide.html' % g['slug']) in s for g in GUIDES)
            if not already:
                after = s[m.end():]
                idx = after.find('</ul>')
                if idx != -1:
                    pos = m.end() + idx
                    s = s[:pos] + new_li + s[pos:]
                    open(ip, 'w', encoding='utf-8').write(s)
                    print('guides/index.html 追加 %d 条到「全部指南」段' % len(GUIDES))
            else:
                print('guides/index.html 已含本批指南，跳过追加')


if __name__ == '__main__':
    main()
