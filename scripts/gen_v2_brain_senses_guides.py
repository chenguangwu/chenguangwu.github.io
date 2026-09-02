# -*- coding: utf-8 -*-
"""V2 脑科学/感官配套使用指南：为 19 个认知/心理/感官工具补写真实使用指南。

选取依据：PLAN-V2-BRAIN-SENSES.md 的 G05 要求为新建 26 工具撰写使用指南，
此前仅完成工具与 i18n 同步，指南页遗留。本脚本补齐这 19 个工具（其余已在别批完成）。
内容全部基于各工具页真实控件、测试原理与输出编写，禁止套话。

运行：python3 scripts/gen_v2_brain_senses_guides.py
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
DATE = '2026-09-02'

GUIDES = [
 {'slug': 'corsi-block-test', 'tool': 'tools/cognition/corsi-block-test.html', 'name': 'Corsi 木块敲击测试',
  'desc': 'Corsi 木块敲击测试使用指南：测量视觉空间工作记忆广度，按递增序列复述点击方块。',
  'intro': '在屏幕上依次点亮一组方块，你按相同顺序点击复述；序列长度逐轮增加，直到无法正确复述，所得最大长度即为你的视觉空间工作记忆广度（Corsi 广度）。适合评估注意力、脑损伤康复与日常记忆训练。',
  'features': ['顺向广度：按原顺序复述点亮的方块序列',
               '逆向广度（可选）：按相反顺序复述，难度更高',
               '序列长度自适应递增，精准定位记忆上限',
               '实时反馈对错与当前最长序列',
               '可设置起始长度与最大长度',
               '纯浏览器本地运行，数据不上传'],
  'scenarios': ['认知评估：快速了解视觉空间工作记忆水平',
                '康复随访：脑损伤或卒中后的记忆训练',
                '日常训练：用递增难度锻炼短期记忆'],
  'steps': ['点击开始，记住第一组点亮的方块顺序',
            '按顺序点击方块复述该序列',
            '答对则下一轮序列加长，答错则结束',
            '查看你的最大正确序列长度（Corsi 广度）',
            '需要挑战时开启逆向模式重新测'],
  'tips': ['顺向广度正常成人约 5~6 个，逆向约 4~5 个',
           '分心环境会明显下降，建议在安静处测',
           '单次结果有波动，可取多次平均',
           '逆向广度更能反映中央执行功能'],
  'faqs': [('Corsi 广度和数字广度有什么区别？', 'Corsi 测视觉空间记忆（位置序列），数字广度测语音/言语记忆（数字序列），两者评估不同通路。'),
           ('结果偏低要紧吗？', '单次偏低未必异常，受疲劳与注意力影响；若持续明显偏低建议就医评估。')]},

 {'slug': 'digit-span-test', 'tool': 'tools/cognition/digit-span-test.html', 'name': '数字广度记忆测验',
  'desc': '数字广度记忆测验使用指南：顺背与倒背数字序列，评估语音工作记忆广度。',
  'intro': '逐位朗读一组数字，你在听完后按顺序复述（顺背），或更难地按相反顺序复述（倒背）。序列逐渐变长，直到无法正确复述，所得最大长度即数字广度，是经典的工作记忆与注意力测评。',
  'features': ['顺背：按原顺序复述数字序列',
               '倒背：按相反顺序复述，难度更高',
               '序列长度自适应递增',
               '可设定起始长度与每轮位数',
               '实时反馈与最长序列统计',
               '纯前端运行，数据不上传'],
  'scenarios': ['学业与招聘：作为注意力与工作记忆的快速筛查',
                '康复评估：脑损伤后记忆功能随访',
                '自我训练：每天练几组提升短期记忆'],
  'steps': ['点击开始，记住报出的数字序列',
            '顺背模式按原序点击或输入，倒背模式按反序',
            '答对序列加长，答错结束',
            '查看顺背与倒背的最大长度',
            '想进阶就练倒背模式'],
  'tips': ['成人顺背广度通常 7±2 位，倒背约 5~6 位',
           '倒背更依赖中央执行功能，难度明显更高',
           '避免边看边记，纯靠记忆更准',
           '疲劳会显著降低成绩，分多次测'],
  'faqs': [('顺背和倒背哪个更难？', '倒背更难，需要在脑内反转顺序，对中央执行功能要求更高。'),
           ('倒背成绩差代表什么？', '可能反映工作记忆的执行控制较弱，但不能单凭一次结果下结论。')]},

 {'slug': 'human-benchmark', 'tool': 'tools/cognition/human-benchmark.html', 'name': 'Human Benchmark 认知基准测评',
  'desc': 'Human Benchmark 认知基准测评使用指南：反应时、记忆力、准确性等多项目挑战你的认知表现。',
  'intro': '集成反应时、数字记忆、听觉记忆、视觉记忆、语言记忆、打字速度、瞄准精度等一系列小测验，给出可对比的基准分数，帮你了解自己的反应与记忆水平，也能反复练习看进步。',
  'features': ['反应时测试：测看到信号到点击的延迟',
               '数字/听觉/视觉/语言记忆多项记忆挑战',
               '打字速度与瞄准精度测试',
               '即时分数与历史最佳对比',
               '可选多轮取平均',
               '纯浏览器本地运行'],
  'scenarios': ['自我认知：量化反应速度与记忆广度',
                '训练反馈：反复练习追踪进步',
                '趣味挑战：和朋友比拼基准分'],
  'steps': ['选择要挑战的项目（如反应时）',
            '按提示完成每一轮（点击/记忆/输入）',
            '查看本次分数与历史最佳',
            '可切换到其他项目继续测',
            '多轮后看平均成绩'],
  'tips': ['反应时受设备与状态影响，用鼠标比触屏更稳',
           '记忆类项目靠练习可显著提升',
           '单次波动大，看趋势而非单点',
           '保证专注，分心会拉低所有分数'],
  'faqs': [('为什么我的反应时比别人慢？', '受年龄、设备延迟、专注度影响，几百毫秒内都属正常波动。'),
           ('这些分数有临床意义吗？', '仅作趣味与自我参考，不能替代专业认知评估。')]},

 {'slug': 'nback-training', 'tool': 'tools/cognition/nback-training.html', 'name': 'N-Back 工作记忆训练',
  'desc': 'N-Back 工作记忆训练使用指南：判断当前刺激是否与 N 步前的相同，锻炼中央执行功能。',
  'intro': '屏幕上连续出现字母、位置或图形，你需要判断当前这一个是否与前面第 N 个相同。N 越大越难（1-back 最简单，3-back 已很有挑战）。这是认知训练研究中最常用的范式，可提升工作记忆与注意力。',
  'features': ['可调 N 值（1-back 到 3-back 及以上）',
               '刺激类型可选字母 / 位置 / 双 N-back',
               '逐 trial 实时反馈对错',
               '得分、正确率与连续正确统计',
               '难度随 N 自适应或手动设定',
               '纯前端运行，数据不上传'],
  'scenarios': ['认知训练：系统提升工作记忆容量',
                '研究参与：复现经典 N-back 范式',
                '专注力练习：每天几组保持状态'],
  'steps': ['选择 N 值（新手从 1-back 起）与刺激类型',
            '记住前面第 N 个刺激是什么',
            '当前刺激出现时判断是否匹配',
            '答对继续，答错看反馈后继续',
            '逐步把 N 调到 2、3 提升难度'],
  'tips': ['2-back 已接近多数人的舒适上限',
           '双 N-back（同时看字母和位置）难度陡增',
           '先把 1-back 练到几乎全对再升 N',
           '保持节奏，过快易错、过慢记不清'],
  'faqs': [('N-back 训练真的有效吗？', '研究显示对训练任务本身提升明显，迁移到日常其他任务存在争议，但作为脑力锻炼有普遍价值。'),
           ('N 越大越好吗？', '不是，超过自己能力太多只会挫败；在能做对七八成的难度最利于提升。')]},

 {'slug': 'schulte-table', 'tool': 'tools/cognition/schulte-table.html', 'name': '舒尔特方格注意力训练',
  'desc': '舒尔特方格注意力训练使用指南：按 1~25 顺序快速点格，测注意力与视觉搜索速度。',
  'intro': '在 5×5（可调整）随机排列数字的方格中，按顺序尽快点击 1 到 25。完成时间越短，说明视觉搜索与注意力集中度越好。常用于注意力测评与训练，也适合作为专注力热身。',
  'features': ['标准 5×5 方格，支持 4×4 / 6×6 等尺寸',
               '数字随机生成，每局不同',
               '实时计时与完成用时',
               '记录历史最佳成绩',
               '可选倒序或字母模式',
               '纯前端运行'],
  'scenarios': ['注意力测评：用完成时间量化专注度',
                '训练热身：学习或工作前激活专注',
                '儿童专注力练习：有趣而不枯燥'],
  'steps': ['选择方格尺寸（默认 5×5）点击开始',
            '按 1→2→3…顺序尽快点击数字',
            '完成后查看用时与历史最佳',
            '想更难就加大方格或切换倒序',
            '每天几局追踪进步'],
  'tips': ['用余光扫全局比逐格找更快',
           '视线跳动少、节奏稳成绩更好',
           '分心会显著拖慢，保持安静环境',
           '完成时间受方格大小影响，同尺寸才可比'],
  'faqs': [('完成时间多少算正常？', '5×5 成人多在 30~60 秒，受训练与状态影响很大，看自身进步更有意义。'),
           ('为什么比朋友慢很多？', '视觉搜索策略与专注度差异所致，多练会明显提升。')]},

 {'slug': 'stroop-test', 'tool': 'tools/cognition/stroop-test.html', 'name': 'Stroop 斯特鲁普效应测试',
  'desc': 'Stroop 斯特鲁普效应测试使用指南：说出/选出字义而非字色的颜色，测选择性注意与干扰抑制。',
  'intro': '屏幕上出现用某种颜色写的颜色词（如红字写「蓝」），你需要忽略字义、按墨色作答。这种字义与颜色的冲突会产生著名的 Stroop 效应，用来评估选择性注意与认知干扰抑制能力。',
  'features': ['经典 Stroop：按墨色选或说颜色，忽略字义',
               '可限时计分或自由模式',
               '实时正确率与平均反应时',
               '多种试次随机呈现避免练习效应',
               '结果可对比常模',
               '纯前端运行'],
  'scenarios': ['认知测评：了解干扰抑制能力',
                '注意力训练：练习抵抗自动反应',
                '科普演示：直观感受 Stroop 效应'],
  'steps': ['点击开始，看清每个词的墨色',
            '忽略词本身的意思，只按颜色作答',
            '限时内尽量快且准',
            '完成后看正确率与反应时',
            '可多轮取平均'],
  'tips': ['越想快越容易念出字义，慢半拍更准',
           '中性词作对照能分离出纯干扰量',
           '反应时受语言熟练度影响',
           '保持节奏，慌乱会错更多'],
  'faqs': [('为什么字义总抢在颜色前面？', '阅读是高度自动化的习惯，抑制它会占用额外认知资源，这就是 Stroop 效应的来源。'),
           ('成绩差说明什么？', '单次结果受状态影响，仅作参考；明显持续困难可关注注意力管理。')]},

 {'slug': 'time-perception', 'tool': 'tools/cognition/time-perception.html', 'name': '时间感知与节奏精度测试',
  'desc': '时间感知与节奏精度测试使用指南：估算与复现时间区间、跟打节拍，评估内在时间感。',
  'intro': '通过估算一段时长、等比复现间隔、跟打稳定节拍等任务，评估你对时间的感知与保持节奏的精度。内在时间感与小脑、基底节相关，常用于节奏训练、运动与音乐练习前的自评。',
  'features': ['时长估算：判断呈现的秒数',
               '间隔复现：等比重现刚才的间隔',
               '节拍跟打：保持稳定节奏输出',
               '误差与标准差实时统计',
               '多种时长与节奏档位',
               '纯前端运行'],
  'scenarios': ['音乐/舞蹈：评估并训练节奏稳定性',
                '运动训练：提升动作时间感',
                '科普自评：了解自己的时间感知偏差'],
  'steps': ['选择任务（估算 / 复现 / 节拍）',
            '按提示感知或产出时间',
            '系统比对你的输出与标准',
            '查看误差与波动',
            '多轮后看稳定性变化'],
  'tips': ['短时长（小于1秒）更易高估，长时长更易低估',
           '有外部节拍器参考会显著变准',
           '疲劳与分心会放大波动',
           '音乐训练者通常节拍更稳定'],
  'faqs': [('为什么我总估不准时间？', '内在时钟会随注意与唤醒水平漂移，短时长尤其容易偏差，属正常现象。'),
           ('节奏不稳能练好吗？', '可以，靠节拍器跟打与刻意练习能明显改善稳定性。')]},

 {'slug': 'pure-tone-audiometry', 'tool': 'tools/ent/pure-tone-audiometry.html', 'name': '纯音听力筛查 · 听力图',
  'desc': '纯音听力筛查使用指南：在各频率找到能听到的最轻声音，生成个人听力图。',
  'intro': '在安静环境戴上耳机，系统在各频率（如 250Hz~8kHz）播放由弱到强的纯音，你听到就按键；记录各频率的听阈并连成听力图，快速了解自己的听力曲线。本筛查不能替代专业测听。',
  'features': ['多频率纯音（250/500/1k/2k/4k/8k Hz 等）',
               '阈值的升/降法自动定位',
               '生成可保存的听力图曲线',
               '左右耳分别测试',
               '结果分级提示（正常/轻度等）',
               '纯前端播放，数据不上传'],
  'scenarios': ['自我筛查：留意是否某频率听不清',
                '护耳参考：长期噪声暴露后复测',
                '科普了解：直观看到听力曲线'],
  'steps': ['戴上耳机，调好舒适音量，环境尽量安静',
            '逐频率点击播放，听到就按听到了',
            '系统确定该频率听阈后进入下一频率',
            '左右耳分别完成后查看听力图',
            '对比既往结果看变化趋势'],
  'tips': ['务必用耳机且在安静处测，外放会严重失真',
           '感冒鼻塞时中耳受压，结果会偏差',
           '高频（4k/8k）下降常见于噪损，属预警',
           '本结果仅作参考，耳闷或突聋请就医'],
  'faqs': [('筛查正常就代表听力没问题吗？', '仅覆盖纯音听阈，不排除听辨、耳鸣等其他问题，异常感受仍应就医。'),
           ('为什么高频先下降？', '长期噪声与年龄相关听力损失多从高频开始，故 4k~8k 最敏感。')]},

 {'slug': 'temporal-resolution-hearing', 'tool': 'tools/ent/temporal-resolution-hearing.html', 'name': '听觉时间分辨率测试',
  'desc': '听觉时间分辨率测试使用指南：辨别快速变化的声音与间隙，评估听觉时间加工能力。',
  'intro': '通过间隙检测（两段声音之间能否听出停顿）、时程分辨等任务，评估听觉系统对时间细节的分辨能力。时间分辨率下降会影响嘈杂环境的言语理解，常用于听力与康复自评。',
  'features': ['间隙检测：判断两段音之间是否有停顿',
               '时程/调制分辨等多种任务',
               '间隙宽度自适应由宽到窄',
               '左右耳可分别测',
               '结果以最小可辨间隙呈现',
               '纯前端播放'],
  'scenarios': ['助听器/康复随访：看时间加工是否改善',
                '嘈杂环境听不清的自查',
                '科普了解听觉时间感'],
  'steps': ['戴耳机在安静处开始',
            '听成对声音，判断是否有间隙或不同',
            '由易到难，系统收缩到你的阈值',
            '左右耳分别完成后看最小可辨间隙',
            '对比前后变化'],
  'tips': ['用耳机且安静环境，外放会漏掉细节',
           '年龄与噪损都会让时间分辨率下降',
           '与纯音听力联合看更全面',
           '结果异常或伴听不清请就医'],
  'faqs': [('时间分辨率和纯音听力是一回事吗？', '不是，纯音看多轻能听见，时间分辨看多快的变化能分清，后者更影响言语清晰度。'),
           ('为什么吵地方我听得见却听不清？', '常因时间分辨率与频率分辨下降，能听到声音却抓不住快速变化的语音细节。')]},

 {'slug': '1a2b-guess', 'tool': 'tools/fun/1a2b-guess.html', 'name': '1A2B 猜数字（Bulls & Cows）',
  'desc': '1A2B 猜数字使用指南：用 A/B 线索推理出隐藏数字序列，锻炼逻辑推理。',
  'intro': '系统生成一个不重复的数字序列，你每猜一次，会得到 A（数字与位置都对）和 B（数字对但位置错）的提示，据此逐步缩小范围、推理出正确答案。这是经典的逻辑推理小游戏。',
  'features': ['可设位数（常见 4 位）与是否允许重复',
               '每次猜测返回 A/B 提示',
               '历史记录与线索一目了然',
               '可开启计时与最少步数挑战',
               '提供提示模式降低难度',
               '纯前端运行'],
  'scenarios': ['逻辑训练：锻炼演绎推理',
                '休闲娱乐：和朋友比谁步数少',
                '破冰热身：激活思维'],
  'steps': ['选择位数与规则后开始',
            '输入一组猜测数字',
            '根据 A/B 提示排除不可能的组合',
            '逐步收敛，直到全 A',
            '查看用了几步与耗时'],
  'tips': ['先广撒网找数字，再定位顺序',
           'B 多说明数字对、调位置；A 多说明顺序对',
           '记好每轮线索避免矛盾',
           '新手从 3 位或无重复开始'],
  'faqs': [('A 和 B 到底什么意思？', 'A=数字和位置都对，B=数字对但位置错；目标是尽快达到全 A。'),
           ('有没有必胜策略？', '没有捷径，但系统的排除法能稳定用较少步数解出。')]},

 {'slug': 'daily-riddle', 'tool': 'tools/fun/daily-riddle.html', 'name': '每日谜题挑战',
  'desc': '每日谜题挑战使用指南：每天一道脑筋急转弯与逻辑谜题，附提示与答案。',
  'intro': '每天更新一道谜题（脑筋急转弯、逻辑、数学或文字类），提供逐层提示与最终答案，既放松又练脑。适合茶余饭后动动脑筋。',
  'features': ['每日一题，日期固定可回看',
               '多层级提示逐步降低难度',
               '答案与解析一键查看',
               '支持收藏与分享',
               '题库持续扩充',
               '纯前端运行'],
  'scenarios': ['日常娱乐：碎片时间动脑',
                '亲子互动：一起猜谜',
                '思维热身：工作前激活'],
  'steps': ['打开当日谜题阅读题目',
            '卡住时点提示看线索',
            '想好后对答案与解析',
            '喜欢可收藏或分享给朋友',
            '明天再来挑战新题'],
  'tips': ['先自己想再点提示，锻炼更明显',
           '很多谜题靠换个角度而非硬算',
           '解析往往点破思维定势',
           '和孩子玩可多给提示'],
  'faqs': [('谜题每天几点更新？', '按日期轮换，同一天内容一致，隔日换新题。'),
           ('答案有争议怎么办？', '部分脑筋急转弯本就开放，解析给出一种合理解读即可。')]},

 {'slug': 'amsler-grid-test', 'tool': 'tools/ophthalmology/amsler-grid-test.html', 'name': 'Amsler 阿姆斯勒方格表',
  'desc': 'Amsler 方格表使用指南：自测黄斑区功能，留意直线是否扭曲或区域变暗。',
  'intro': '注视方格中心圆点，用单眼观察网格线是否平直、有无扭曲、空缺或变暗。Amsler 表是筛查黄斑变性等黄斑病变的简易自测工具，异常变化应及时就医。',
  'features': ['标准方格网格，中心固定注视点',
               '支持单眼/双眼切换',
               '可标记你看到的扭曲或缺损区域',
               '提供使用示意与记录',
               '适配手机与桌面',
               '纯前端展示'],
  'scenarios': ['黄斑自检：定期留意视物变形',
                '慢病随访：糖尿病/高龄人群居家监测',
                '科普了解黄斑功能'],
  'steps': ['戴日常眼镜，距离约 30cm',
            '遮一只眼，盯住中心圆点',
            '用余光看整片网格是否平直',
            '发现扭曲或暗区就在图上标出',
            '换另一只眼重复，定期对比'],
  'tips': ['务必单眼测，双眼会互相补偿掩盖问题',
           '固定距离与光线，结果才可比',
           '线条一变形就记录并就医，别等加重',
           '不能替代眼底检查，仅作预警'],
  'faqs': [('网格看起来弯就是生病吗？', '可能是黄斑问题的信号，尤其新近出现或单眼，建议尽快眼科就诊。'),
           ('多久自测一次合适？', '高风险人群（糖尿病、高龄、家族史）可每周一次，作趋势监测。')]},

 {'slug': 'astigmatism-chart', 'tool': 'tools/ophthalmology/astigmatism-chart.html', 'name': '散光放射线自测表',
  'desc': '散光放射线自测表使用指南：看放射线哪方向更清晰，初步判断散光轴向与程度。',
  'intro': '表上由中心向四周放射的线条若看起来清晰度不一（某些方向明显更黑更实），可能提示散光。本表仅作初步自测参考，配镜仍需专业验光。',
  'features': ['标准放射线（太阳放射）图样',
               '可切换不同密度与颜色背景',
               '单眼/双眼切换',
               '示意说明与注意项',
               '适配多端屏幕',
               '纯前端展示'],
  'scenarios': ['散光初筛：留意线条清晰度差异',
                '配镜前自查：了解是否可能散光',
                '科普了解散光成因'],
  'steps': ['戴日常眼镜，距离约 30~40cm',
            '遮一只眼，看放射线是否均匀',
            '某方向明显更清晰或更实即记录',
            '换眼重复',
            '综合判断是否需要验光'],
  'tips': ['线条明显不均才具提示意义，轻微差异常见',
           '屏幕亮度均匀、距离固定更准',
           '结果受屏幕与视疲劳影响',
           '确诊散光请做专业验光'],
  'faqs': [('线条一边清一边糊就是散光？', '高度提示散光可能，但需验光确认轴位与度数。'),
           ('散光一定要配镜吗？', '低度且无症状可观察，影响视力或疲劳则需矫正。')]},

 {'slug': 'eye-chart-toolkit', 'tool': 'tools/ophthalmology/eye-chart-toolkit.html', 'name': '专业视力表工具箱',
  'desc': '视力表工具箱使用指南：多种 Snellen/logMAR 视力表与距离工具，快速自查视力。',
  'intro': '集成标准视力表（如 E 字表、字母表、logMAR 表）与测距参考，按正确视距查看能认到的最小一行，估算裸眼或矫正视力。自测结果仅供参考，配镜与诊断请就医。',
  'features': ['多种视力表（E 字 / 字母 / logMAR）',
               '可调视距与换算',
               '单眼/双眼切换',
               '记录各次视力值',
               '距离与视标大小说明',
               '纯前端展示'],
  'scenarios': ['视力自查：定期看是否下降',
                '护眼提醒：发现模糊及时就医',
                '科普了解视力记录方式'],
  'steps': ['选表与设定视距（如 5 米）',
            '遮一只眼，从大往小认到最后能看清的行',
            '记录该行视力值',
            '换眼重复',
            '前后对比趋势'],
  'tips': ['标准视距与照明很重要，家里可用米尺量',
           '眯眼会虚高结果，别偷瞄',
           '屏幕像素密度影响小字号清晰度',
           '视力下降明显请眼科就诊'],
  'faqs': [('5.0 和 1.0 视力是什么关系？', '是中国标准对数（5 分制）与小数记录的两种写法，约略对应同一视力。'),
           ('在家测的准吗？', '只能看趋势，因距离、屏幕、光线难标准化，正式以验光为准。')]},

 {'slug': 'vision-screening-21', 'tool': 'tools/ophthalmology/vision-screening-21.html', 'name': '21 题自适应视力筛查',
  'desc': '21 题自适应视力筛查使用指南：通过自适应问卷估算双眼大致屈光需求。',
  'intro': '以 21 道自适应问题（用眼习惯、视物距离、模糊场景等）逐步收敛，给出你双眼大致的屈光倾向（如近视/远视/散光风险）参考。属筛查性质，不替代医学验光。',
  'features': ['自适应提问，答完约 21 题',
               '覆盖远近用眼与症状维度',
               '实时收敛给出倾向参考',
               '左右眼分别评估',
               '结果可保存对比',
               '纯前端运行'],
  'scenarios': ['屈光风险自查：提示是否需要验光',
                '青少年监测：留意近视化趋势',
                '科普了解屈光概念'],
  'steps': ['如实回答用眼与视物相关问题',
            '系统按回答自适应追问',
            '完成后查看双眼倾向参考',
            '对照建议决定是否验光',
            '定期重测看变化'],
  'tips': ['如实作答才有效，别按理想答',
           '结果受主观描述影响，作趋势参考',
           '青少年频繁眯眼或凑近应尽早验光',
           '最终以专业验光单为准'],
  'faqs': [('21 题能测出我多少度吗？', '不能给出精确度数，只提示屈光风险与方向，配镜需验光。'),
           ('小孩能用吗？', '可作家长观察辅助，但最终以儿童眼科检查为准。')]},

 {'slug': 'attachment-style-test', 'tool': 'tools/psychology/attachment-style-test.html', 'name': '成人依恋类型测试（ECR）',
  'desc': '成人依恋类型测试使用指南：用 ECR 量表评估你在亲密关系中的焦虑与回避维度。',
  'intro': '基于经验性亲密关系量表（ECR），通过一系列关于亲密与依赖的陈述，评估你的焦虑（担心被弃）与回避（不适亲密）两个维度，从而定位依恋风格（安全、焦虑、回避、恐惧型）。结果仅供自我了解。',
  'features': ['标准 ECR 维度：焦虑 × 回避',
               '多题项李克特自评',
               '自动算出两维度分数',
               '映射四种依恋风格',
               '结果可保存与复测',
               '纯前端运行'],
  'scenarios': ['自我探索：理解亲密关系模式',
                '伴侣沟通：用共同语言谈需求',
                '科普学习：了解依恋理论'],
  'steps': ['按第一直觉对每句陈述打分',
            '完成后看焦虑/回避双轴得分',
            '对照四象限定位你的风格',
            '结合例子理解含义',
            '可与伴侣分享讨论'],
  'tips': ['按真实感受而非应该怎样答',
           '分数是连续维度，非贴死标签',
           '风格会随关系与经历变化',
           '用于理解而非评判自己或对方'],
  'faqs': [('依恋类型能改变吗？', '维度分数相对稳定但可随经历与关系改善而变化，安全型可通过觉察提升。'),
           ('恐惧型是什么？', '高焦虑加高回避，既渴望亲密又害怕受伤，常表现为推拉。')]},

 {'slug': 'bubble-tea-personality-quiz', 'tool': 'tools/psychology/bubble-tea-personality-quiz.html', 'name': '你是哪款珍珠奶茶',
  'desc': '珍珠奶茶人格测试使用指南：趣味问答匹配你的奶茶人格，轻松破冰。',
  'intro': '用一组轻松有趣的选择题，把你映射到某款珍珠奶茶人格（如经典珍珠、芋泥啵啵、芝士奶盖等），纯属娱乐互动，适合社交破冰与心情调节。',
  'features': ['趣味多选题，几分钟出结果',
               '多种奶茶人格映射',
               '结果附性格小解读',
               '可分享给朋友比一比',
               '随机彩蛋与重测',
               '纯前端运行'],
  'scenarios': ['社交破冰：聚会暖场小游戏',
                '休闲解压：随手测着玩',
                '内容互动：社群话题素材'],
  'steps': ['按直觉选每个情境的答案',
            '完成后看你的奶茶人格与解读',
            '觉得不准就重测换组合',
            '分享给朋友一起玩',
            '收藏喜欢的结果'],
  'tips': ['纯娱乐，结果别太当真',
           '不同选项组合会指向不同人格',
           '适合轻松氛围，别较真',
           '可多人同测比差异'],
  'faqs': [('结果准吗？', '是趣味映射，不具心理测量学意义，图个乐。'),
           ('能自定义奶茶人格吗？', '目前为固定映射，娱乐向，欢迎当梗图玩。')]},

 {'slug': 'enneagram-test', 'tool': 'tools/psychology/enneagram-test.html', 'name': '九型人格测试',
  'desc': '九型人格测试使用指南：定位你的核心类型与动机，理解行为底层。',
  'intro': '通过一系列关于动机、恐惧与欲望的陈述，帮你定位九型人格（1~9 型）中的核心类型及侧翼，理解自己行为背后的驱动力。结果用于自我成长参考。',
  'features': ['覆盖九型及侧翼/三元组',
               '多题项自评计分',
               '给出主导型与可能侧翼',
               '类型释义与成长建议',
               '结果可保存复测',
               '纯前端运行'],
  'scenarios': ['自我认知：看清核心动机',
                '团队/关系：理解差异与摩擦源',
                '个人成长：针对性突破卡点'],
  'steps': ['凭第一直觉对陈述打分',
            '系统汇总各型得分',
            '看最高分类型及其释义',
            '结合侧翼理解更立体',
            '与他人交流印证'],
  'tips': ['按最像我而非我想成为答',
           '九型看动机而非行为表象',
           '高分型可能有 2~3 个接近，看整体',
           '用于成长而非贴标签评判'],
  'faqs': [('九型和 MBTI 有什么区别？', '九型聚焦核心动机与恐惧，MBTI 偏认知偏好，角度不同可互补。'),
           ('为什么我好几型都高？', '很多人有相邻侧翼，核心型看最高且最贴合内心的那一个。')]},

 {'slug': 'holland-career-test', 'tool': 'tools/psychology/holland-career-test.html', 'name': '霍兰德职业兴趣测试（RIASEC）',
  'desc': '霍兰德职业兴趣测试使用指南：用 RIASEC 六型定位你的兴趣代码与职业方向。',
  'intro': '基于霍兰德 RIASEC 模型（现实型、研究型、艺术型、社会型、企业型、常规型），通过兴趣活动自评，得出你的三位兴趣代码，并给出与之匹配的职业方向参考，适合选专业与职业规划。',
  'features': ['RIASEC 六型兴趣自评',
               '算出前三兴趣代码（如 SEC）',
               '匹配职业方向建议',
               '类型释义与组合解读',
               '结果可保存对比',
               '纯前端运行'],
  'scenarios': ['选专业/职业：用兴趣代码缩小范围',
                '职业规划：看清适配方向',
                '生涯教育：自我探索工具'],
  'steps': ['对六类活动按喜好打分',
            '系统排序得出你的兴趣代码',
            '查看前三代码对应职业',
            '结合能力与现实做决策',
            '可与咨询师讨论'],
  'tips': ['凭真实兴趣而非热门答',
           '前三代码组合比单型更有信息量',
           '兴趣不等于能力，决策还要看特长',
           '代码会随经历微调，定期复测'],
  'faqs': [('RIASEC 六型是什么？', '现实/研究/艺术/社会/企业/常规六种兴趣取向，组合成你的职业兴趣画像。'),
           ('结果能直接定职业吗？', '给出方向参考，最终结合能力、价值观与机会综合判断。')]},
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

    jf = os.path.join(ROOT, 'json', 'guides.json')
    old = json.load(open(jf, encoding='utf-8')) if os.path.isfile(jf) else []
    existing = {m['tool'] for m in old}
    merged = old + [m for m in guide_map if m['tool'] not in existing]
    json.dump(merged, open(jf, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
    print('guides.json 合并完成，共 %d 条（新增 %d）' % (len(merged), len(guide_map) - len([m for m in guide_map if m['tool'] in existing])))

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
