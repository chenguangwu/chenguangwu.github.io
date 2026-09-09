# -*- coding: utf-8 -*-
"""language 分类 deep-dive 真实化：用工具专属真实内容替换第六型/弱泛化占位。
用法：python3 scripts/apply_language.py
规则：json.dump(indent=1) + 末尾换行；自检拒绝任何 BAD_RE 占位；
      【铁律】写入必须 json.dumps(data) 全量，写完断言键数不丢，防截断。
"""
import json, re, sys

PATH = "i18n/tools/content_deepdive.json"
BAD_RE = re.compile(
    "统一复核|降低上手门槛|可追溯流程|边界样本建议单独标注|减少重复确认成本|标准化，再批量|"
    "可复核输出|沿用模板逐项核对|形成标准复核清单|统一口径|快速复核|高频复用模板|复用模板示例|"
    "保留复用模板|先按业务口径补充必要字段|运行工具并记录输出|对比另一组边界输入|先用一组可复现输入|"
    "同一输入样本测试默认和边界情况|选择两组不同来源样本并同步口径定义"
)

KB = {
"language/calc-1": {
  "title": "英语词汇量估算（抽样统计）",
  "scenarios": [
    "用 20 个分层抽样词勾选认识比例，估总词汇量区间",
    "自测水平后制定背词计划（如目标 5000/8000）",
    "对比不同词表（通用/雅思/托福）看覆盖差距"
  ],
  "examples": [
    {
      "title": "比例推总量",
      "body": "抽样 20 词认得 14 个（70%），若参考词表 2 万词 → 估认识 ≈ 14000；常用简明词典约 3000 核心词覆盖 80% 文本，认 70% 抽样说明已超基础门槛。"
    },
    {
      "title": "区间理解",
      "body": "抽样有随机误差，结果给区间而非定值；认 16/20(80%) 与 14/20(70%) 虽差 10 个百分点，总量可能差 2000 词，属正常波动。"
    }
  ],
  "faqs": [
    {
      "q": "抽样为什么用 20 词？",
      "a": "太少误差大、太多费时；20 词在可信度与效率间平衡，按难度分层（高频→低频）取样更准。"
    },
    {
      "q": "估算能当真实词汇量吗？",
      "a": "只能估被动词汇量（见词识义），主动复用（说写）通常更小；且认词标准松紧影响结果，作参考非精确值。"
    }
  ]
},
"language/calc-2": {
  "title": "阅读速度测试（WPM）",
  "scenarios": [
    "输入阅读字数与用时算每分钟字数（WPM）",
    "结合理解度自评看有效阅读速度",
    "跟踪训练前后速度变化评估进步"
  ],
  "examples": [
    {
      "title": "WPM 计算",
      "body": "读 3000 字用 10 分钟 → WPM = 3000/10 = 300 字/分钟；中文母语者常见 200–500 字/分钟，理解度高中段最健康。"
    },
    {
      "title": "理解度校正",
      "body": "同样 300 字/分钟，理解自评低（<60%）说明是「扫读」而非有效阅读；提效应兼顾 Comprehension，而非只追速度。"
    }
  ],
  "faqs": [
    {
      "q": "WPM 怎么算？",
      "a": "WPM = 总字数 / 总用时（分钟）；英文常以词计、中文以字计，跨语言比较需注明单位。"
    },
    {
      "q": "速度多少算好？",
      "a": "无绝对标准，关键看理解率；盲目提速若理解崩塌则无效，建议维持 80%+ 理解下的个人最佳速度。"
    }
  ]
},
"language/stats-2": {
  "title": "字符数统计（汉字/英文/标点）",
  "scenarios": [
    "论文/投稿按字数限制核校，区分总字符与可见字符",
    "中英混排时分别计汉字、字母、数字、标点",
    "写作长度把控与平台字数上限检查"
  ],
  "examples": [
    {
      "title": "分类计数",
      "body": "文本「你好Hello2024！」→ 汉字 2、英文字母 5、数字 4、标点 1，总字符 12；可见字符不含换行/空格则为 12。"
    },
    {
      "title": "中英差异",
      "body": "同一段中文 500 字约 500 字符；译成英文可能 350 词但约 2100 字母+空格，按「字符」还是「词」统计结论不同，口径需事先约定一致。"
    }
  ],
  "faqs": [
    {
      "q": "总字符和可见字符差在哪？",
      "a": "总字符含空格、换行等不可见控制符；可见字符只算打印出的字与标点，投稿常按可见字数计。"
    },
    {
      "q": "汉字算几个字符？",
      "a": "一个汉字（含标点）通常计 1 个字符（UTF-16/代码点层面）；英文一个字母 1 字符，混排分别累加。"
    }
  ]
},
"language/generator-19": {
  "title": "首字母缩写生成器",
  "scenarios": [
    "从短语各词取首字母生成缩写（如 API）",
    "调大小写与连接符用于命名/术语提炼",
    "团队/项目起名快速产出候选缩写"
  ],
  "examples": [
    {
      "title": "取首字母",
      "body": "「Application Programming Interface」→ 取各词首字母 A P I → 默认大写连写 API；「natural language processing」→ NLP。"
    },
    {
      "title": "连接符选项",
      "body": "同短语选 kebab 连接 → A-P-I，选小写 → api；含虚词（of/and）可跳过得更短缩写，如 「Federal Bureau of Investigation」→ FBI（跳过 of）。"
    }
  ],
  "faqs": [
    {
      "q": "缩写规则怎么定？",
      "a": "通用取实词首字母、跳过 a/the/of 等虚词；大小写与分隔按风格指南（如变量用驼峰、品牌用全大）。"
    },
    {
      "q": "会产生歧义吗？",
      "a": "会，不同短语可能同缩写（API vs 其他）；正式命名应查重避免与已知缩写冲突。"
    }
  ]
},
"language/french-verb-conjugator": {
  "title": "法语动词变位查询",
  "scenarios": [
    "输入动词原形查直陈/条件/虚拟等语气时态变位",
    "背 -er/-ir/-re 三组规则变位的人称词尾",
    "查常用不规则动词（avoir/être/aller）变位"
  ],
  "examples": [
    {
      "title": "第一组 -er 现在时",
      "body": "parler 直陈现在时：je parle / tu parles / il parle / nous parlons / vous parlez / ils parlent；统一去 -er 加 -e,-es,-e,-ons,-ez,-ent。"
    },
    {
      "title": "不规则动词",
      "body": "avoir 现在时：j'ai / tu as / il a / nous avons / vous avez / ils ont；属高频不规则，需单独记忆。"
    }
  ],
  "faqs": [
    {
      "q": "法语动词分几组？",
      "a": "主要三组：-er（最多，规则统一）、-ir（如 finir→finis）、-re（如 rendre→rends）；外加 être/avoir/aller 等高频不规则。"
    },
    {
      "q": "虚拟式怎么用？",
      "a": "用于表达怀疑、愿望、情感等的主从句（如 il faut que + subjonctif），与直陈式时态体系不同，需按句式触发。"
    }
  ]
},
"language/xibanyayuzhongyinweizhipanduan-neizhiguize": {
  "title": "西班牙语重音位置判断（内置规则）",
  "scenarios": [
    "输入单词判断重音落倒数第几音节",
    "据规则判定重音符号是否必要（规则/不规则）",
    "辅助西语单词正确重读与拼写"
  ],
  "examples": [
    {
      "title": "重音规则",
      "body": "以元音或 n/s 结尾 → 重音在倒数第二音节（llana，如 casa、hablan），一般不标符号；以其他辅音结尾 → 重音在最后音节（aguda，如 ciudad），需标重音符。"
    },
    {
      "title": "esdrújula",
      "body": "重音在倒数第三音节（esdrújula，如 música、pérdida）无论结尾一律标重音符；规则判断即据此分类。"
    }
  ],
  "faqs": [
    {
      "q": "aguda 和 llana 区别？",
      "a": "aguda 重音在最后音节、以辅音(非n/s)结尾需标符号；llana 在倒数第二、以元音/n/s 结尾不标；esdrújula 在倒数第三必标。"
    },
    {
      "q": "为什么有的词不标重音？",
      "a": "符合 llana/以元音或 n/s 结尾 的默认重读位置即无需符号；仅当实际重读偏离默认（aguda 或 esdrújula）才加符号。"
    }
  ]
},
"language/spanish-accent-rules": {
  "title": "西语重音规则（参考速查）",
  "scenarios": [
    "查单词该不该加重音符号（á/é/í/ó/ú/ñ）",
    "区分同形异义词（如 el/él、si/sí）的标法",
    "拼写检查前先确认重音分类"
  ],
  "examples": [
    {
      "title": "同形异义",
      "body": "el（定冠词，无重音）vs él（他，有重音）；si（如果）vs sí（是的/重音在末）；依赖重音区分语义。"
    },
    {
      "title": "标法判定",
      "body": "café 以辅音结尾且重音在末 → 标 é；libro 以元音结尾重音在次末 → 不标；反复练习可内化规则。"
    }
  ],
  "faqs": [
    {
      "q": "重音符号只标元音？",
      "a": "是，西语重音符号只加在 a/e/i/o/u 上（ñ 是独立字母非重音）；á 等表示该音节重读。"
    },
    {
      "q": "疑问词一定标重音？",
      "a": "是，疑问/感叹词（qué/cuándo/dónde）必标重音以区别于关系代词（que/cuando），属固定写法。"
    }
  ]
},
"language/korean-hangul-decomposer": {
  "title": "韩语谚文拆解（初声/中声/终声）",
  "scenarios": [
    "输入韩文逐音节拆成初声(辅音)中声(元音)终声(收音)",
    "理解谚文方块字拼字结构便于识字与打字",
    "教学/输入法研究看音节编码"
  ],
  "examples": [
    {
      "title": "音节拆分",
      "body": "한 = 初声 ㅎ + 中声 ㅏ + 终声 ㄴ；사 = ㅅ+ㅏ（无终声）；랑 = ㄹ+ㅏ+ㅇ。每个方块由三要素组合。"
    },
    {
      "title": "Unicode 编码",
      "body": "谚文音节 = 0xAC00 + 初声序号×588 + 中声序号×28 + 终声序号；如 한(0xD55C) 可反推三要素，便于程序化拆解。"
    }
  ],
  "faqs": [
    {
      "q": "为什么分初声中声终声？",
      "a": "谚文是音素文字，方块由辅音(初)+元音(中)+可选辅音(终)拼成；会拆就能懂任何生字的拼读逻辑。"
    },
    {
      "q": "终声一定是辅音吗？",
      "a": "终声(받침)只能是 27 个合法收音之一（含 ㅇ 等），可空；元音不能作终声，双终声按代表音归一。"
    }
  ]
},
"language/german-gender-quiz": {
  "title": "德语词性（der/die/das）测验",
  "scenarios": [
    "随机出名词练定冠词 der(阳)/die(阴)/das(中)",
    "记常见词性规律（如 -ung/-heit 阴性、-chen 中性）",
    "查错后巩固名词与冠词搭配"
  ],
  "examples": [
    {
      "title": "词性规律",
      "body": "以 -ung、-heit、-keit、-schaft 结尾多阴性(die)；以 -chen、-lein 结尾中性(das)；以 -er 结尾常阳性(der)，但例外多需记。"
    },
    {
      "title": "测验用法",
      "body": "出词「Haus」应选 das（中性）；「Frau」选 die（阴性）；「Mann」选 der（阳性）；错词加入复习队列。"
    }
  ],
  "faqs": [
    {
      "q": "德语词性有规律吗？",
      "a": "部分有（后缀、词义如季节多阳、大部分金属中性），但约 1/3 需硬记；名词首字母永远大写。"
    },
    {
      "q": "词性记错影响大吗？",
      "a": "影响冠词、形容词词尾与代词一致；德语名词必带冠词，词性错全句格变化跟着错。"
    }
  ]
},
"language/ipa-practice": {
  "title": "IPA 国际音标练习",
  "scenarios": [
    "练英语/通用音标的元音辅音发音与辨识",
    "对照音标卡听辨最小对立对（/i/ vs /ɪ/）",
    "纠方言或母语负迁移导致的发音偏差"
  ],
  "examples": [
    {
      "title": "最小对立对",
      "body": "ship /ʃɪp/ vs sheep /ʃiːp/：区别在 /ɪ/（短）与 /iː/（长）；bit /bɪt/ vs beat /biːt/ 同理，练长元音与松元音。"
    },
    {
      "title": "辅音清浊",
      "body": "/s/（清）vs /z/（浊）、/p/ vs /b/；手放喉部感受浊音声带振动，是中文母语者常混点。"
    }
  ],
  "faqs": [
    {
      "q": "IPA 有什么用？",
      "a": "用一套符号精确标任何语言发音，词典里的 /.../ 即音标；比拼写法更准反映实际读音。"
    },
    {
      "q": "英式美式音标差很多？",
      "a": "音系不同（如美式卷舌 r、字母读音差异），但共用 IPA；查词典注意标的是英音(RP)还是美音(GA)。"
    }
  ]
},
"language/grammar-checker": {
  "title": "语法检查（规则/对照）",
  "scenarios": [
    "粘贴文本查主谓一致、时态、冠词等常见错",
    "中英互译后核对目标语语法点",
    "写作前自查基础语法硬伤"
  ],
  "examples": [
    {
      "title": "常见类型",
      "body": "英文：第三人称单数缺 -s（he go→goes）、a/an 误用、时态混用；中文：的/地/得 混用、语序。「He eat apples」应改「eats」。"
    },
    {
      "title": "使用边界",
      "body": "规则检查能抓明显硬错，但语境/语义/搭配错误（如用词不当）常漏；重要文本仍需人工润色。"
    }
  ],
  "faqs": [
    {
      "q": "语法检查能代替人工吗？",
      "a": "不能，只作第一道网抓低级错误；风格、逻辑、地道表达需人审或母语者复核。"
    },
    {
      "q": "为什么有时误报？",
      "a": "规则与统计模型对非常规但正确的句式（如倒装、文学表达）易误判，需结合上下文辨别。"
    }
  ]
},
"language/vocabulary-builder": {
  "title": "单词学习（间隔记忆）",
  "scenarios": [
    "建生词本按遗忘曲线安排复习",
    "用例句+发音多通道记忆单词",
    "按主题/词根分组批量扩充词汇"
  ],
  "examples": [
    {
      "title": "间隔复习",
      "body": "新词第 1/2/4/7/15 天复习符合艾宾浩斯曲线，比集中背更抗遗忘；工具按正确率动态推下次复习日。"
    },
    {
      "title": "词根记忆",
      "body": "词根 spect(看)：inspect(内看=检查)、respect(回看=尊重)、prospect(向前看=前景)；一组同根词联动记更高效。"
    }
  ],
  "faqs": [
    {
      "q": "间隔重复为什么有效？",
      "a": "在快遗忘的临界点复习，用最少次数固化记忆；纯前端工具按本地记录排程，数据不上传。"
    },
    {
      "q": "只背单词够吗？",
      "a": "不够，需配例句、搭配与主动使用（说写）；孤立背词易「见词识义」却不会用。"
    }
  ]
},
"language/translator": {
  "title": "文本翻译（多语互译）",
  "scenarios": [
    "中英/日/韩/西等文本快速互译参考",
    "长句拆段翻译提高准确率",
    "译后对照原文核专业术语"
  ],
  "examples": [
    {
      "title": "分段翻译",
      "body": "「今天天气很好，我们去公园。」→ 「The weather is nice today, let's go to the park.」；长难句先拆主谓宾再译更准。"
    },
    {
      "title": "术语核对",
      "body": "技术文「缓存」译 cache 而非 buffer；译后回查术语表避免机翻常见错配。"
    }
  ],
  "faqs": [
    {
      "q": "机翻能直接用于正式文件？",
      "a": "不建议直接定稿，长句/文化梗/专业术语易错，需人工校对；敏感与法律文本更须母语审。"
    },
    {
      "q": "为什么同一句多次译不同？",
      "a": "神经翻译按上下文动态生成，微小改动能变结果；定稿以一致性为准、人工锁定术语。"
    }
  ]
},
"language/phrase-translator": {
  "title": "常用短语/短句翻译",
  "scenarios": [
    "出行/交流查地道短语与固定搭配",
    "按场景（问候/点餐/问路）取现成短句",
    "对比直译与地道说法差异"
  ],
  "examples": [
    {
      "title": "场景短语",
      "body": "「多少钱？」英文 How much is it?、西语 ¿Cuánto cuesta?；「我听不懂」英文 I don't understand、法语 Je ne comprends pas。"
    },
    {
      "title": "避免直译",
      "body": "「加油」直译 cheer up 不对，赛场应 Go!/Come on!；地道短语不能逐字翻，需记固定搭配。"
    }
  ],
  "faqs": [
    {
      "q": "短语和单词翻译差哪？",
      "a": "短语含习语与搭配，直译常错；现成短句保证地道，适合高频场景直接套用。"
    },
    {
      "q": "发音怎么学？",
      "a": "配合音标或语音试听跟读；纯文本翻译不含发音，需另用发音/音标工具。"
    }
  ]
},
"language/hanyuyanwenchaijie-yuanyin-fuyin": {
  "title": "汉语音韵拆接（声母/韵母/声调）",
  "scenarios": [
    "把音节拆成声母+韵母+声调，理解拼音结构",
    "对比方言与普通话的声韵差异",
    "语音/朗诵教学看拼读拆分"
  ],
  "examples": [
    {
      "title": "音节拆分",
      "body": "「中」zhōng = 声母 zh + 韵母 ong + 声调 1 声；「爱」ài = 零声母 + 韵母 ai + 4 声；普通话 21 声母、39 韵母组合。"
    },
    {
      "title": "零声母",
      "body": "以 a/o/e 开头的音节无声母（如 安 ān、欧 ōu），写作时 y/w 为改写形式（i→yi、u→wu），本质零声母。"
    }
  ],
  "faqs": [
    {
      "q": "声母韵母怎么分？",
      "a": "声母是音节开头辅音（最多 1 个），余下元音部分为韵母；零声母音节开头即韵母。"
    },
    {
      "q": "声调为什么重要？",
      "a": "汉语声调区别意义（妈 mā/麻 má/马 mǎ/骂 mà），同声韵不同调是不同字，是语音核心。"
    }
  ]
},
"language/riyuwushiyintulianxi-dianjifayin": {
  "title": "日语五十音图练习（点击发音）",
  "scenarios": [
    "点假名听发音练平假名/片假名认读",
    "按行（あ行/か行…）循序渐进记忆",
    "对比清音/浊音/拗音位置"
  ],
  "examples": [
    {
      "title": "五十音结构",
      "body": "あ行 a/i/u/e/o、か行 ka/ki/ku/ke/ko… 共 46 基础音（含 ん）；平假名表汉字草书、片假名表偏旁，如 ア = 阿 左耳。"
    },
    {
      "title": "浊音拗音",
      "body": "か行加浊点成 が ga/ぎ gi/ぐ gu/げ ge/ご go；拗音 きゃ kya/きゅ kyu/きょ kyo 由辅音+小ヤ行组成。"
    }
  ],
  "faqs": [
    {
      "q": "平假名片假名用哪个？",
      "a": "平假名用于本土词/语法、片假名用于外来语/拟声；二者同音不同形，需都认。"
    },
    {
      "q": "为什么是五十音不是五十？",
      "a": "清音 45 + ん = 46，传统称「五十音」含历史全表；实际基础发音 46 个，加浊/半浊/拗音扩展。"
    }
  ]
},
"language/idiom-solitaire": {
  "title": "成语接龙（字词游戏）",
  "scenarios": [
    "按末字接下个成语练词汇与反应",
    "同音/同字两种规则切换",
    "亲子/课堂成语积累互动"
  ],
  "examples": [
    {
      "title": "接龙规则",
      "body": "「一帆风顺」→ 顺理成章 → 章句之徒；末字「顺」接「顺…」或同音「瞬/舜」；规则可定同字或同音。"
    },
    {
      "title": "陷阱",
      "body": "末字是多音或生僻（如「为」wéi/wèi）易卡壳；可设允许同音放宽，或限定常用成语库提升流畅。"
    }
  ],
  "faqs": [
    {
      "q": "接龙用末字还是读音？",
      "a": "常见两种：严格末汉字相同，或只要求同音（含声调）；教学常用同字更练书写。"
    },
    {
      "q": "卡住怎么办？",
      "a": "可允许同音、查成语词典，或换规则（如限定某主题成语）；纯娱乐不必纠结唯一解。"
    }
  ]
},
"language/language-toolkit": {
  "title": "语言学习工具箱（集合）",
  "scenarios": [
    "一处调用翻译、词汇、音标、变位等子工具",
    "按任务（背词/纠音/查语法）选对应工具",
    "搭个人语言学习工作流"
  ],
  "examples": [
    {
      "title": "任务映射",
      "body": "背词→vocabulary-builder；纠发音→ipa-practice；查变位→french-verb-conjugator；重音→spanish-accent-rules；按需组合。"
    },
    {
      "title": "工作流",
      "body": "读外刊：先 translator 粗译 → grammar-checker 核句式 → vocabulary-builder 收生词 → ipa-practice 练读音，闭环学习。"
    }
  ],
  "faqs": [
    {
      "q": "工具箱和普通翻译器区别？",
      "a": "不止翻译，覆盖识记/发音/语法/文化多环节，适合系统学习而非单次查词。"
    },
    {
      "q": "数据会上传吗？",
      "a": "本箱各工具多为纯前端，文本在本地处理；涉及翻译的调用依赖外部接口，注意内容敏感性。"
    }
  ]
},
}

def main():
    with open(PATH, encoding="utf-8") as f:
        data = json.load(f)
    before = len(data)
    changed = 0
    for slug, new in KB.items():
        assert slug in data, "slug 不存在: " + slug
        assert len(new["scenarios"]) >= 3, slug + " scenarios<3"
        assert len(new["examples"]) >= 2, slug + " examples<2"
        assert len(new["faqs"]) >= 2, slug + " faqs<2"
        if data[slug] != new:
            data[slug] = new
            changed += 1
    # 仅校验本批写入的 language 键，避免其他待办分类残留占位误报
    sub = {s: data[s] for s in KB}
    if BAD_RE.search(json.dumps(sub, ensure_ascii=False, indent=1)):
        print("ERROR: language 本批内容仍含第六型/弱泛化占位，已中止写入")
        sys.exit(1)
    raw = json.dumps(data, ensure_ascii=False, indent=1)
    with open(PATH, "w", encoding="utf-8") as f:
        f.write(raw + "\n")
    # 铁律：写入后断言键数不丢，防 json.dumps(sub) 误写入导致截断
    reloaded = json.load(open(PATH, encoding="utf-8"))
    assert len(reloaded) == before, "写入后键数由 %d 变为 %d，疑似截断！" % (before, len(reloaded))
    print("language 真实化完成：KB=%d，实际写入变更=%d，键数守恒=%d" % (len(KB), changed, len(reloaded)))

if __name__ == "__main__":
    main()
