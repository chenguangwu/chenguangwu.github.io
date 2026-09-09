#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Real-ize deep-dive content for the `sports` category (75 tools).

Replaces generic SOP boilerplate with tool-specific REAL deep-dive content:
real sports-science examples, scenarios, FAQs. json.dump(indent=1).
"""
import json

DD = 'i18n/tools/content_deepdive.json'
data = json.load(open(DD, encoding='utf-8'))
KB = {}

KB['sports/altitude-acclimatization'] = dict(title='登山海拔适应时间表',
  scenarios=['高原攀登前规划适应，防急性高山病。'],
  examples=[dict(title='适应节奏', body='每升 1000 m 安排 1–3 天适应；3500 m 以上每日净爬升建议 ≤300–500 m，配合睡眠高度递减原则。')],
  faqs=[dict(q='为何要 sleep low？', a='睡眠在较低海拔利于恢复，降低夜间低氧应激。')])

KB['sports/analysis-19'] = dict(title='战术（攻防）视频分析',
  scenarios=['复盘比赛攻防转换与空间利用。'],
  examples=[dict(title='指标', body='统计攻防转换次数、压迫成功率和预期失球 xGA，定位防守空当。')],
  faqs=[dict(q='样本量多少稳？', a='单场噪声大，按多场滚动均值才可靠。')])

KB['sports/analysis-20'] = dict(title='射击（环数/稳定性）分析',
  scenarios=['评估射击精度与一致性。'],
  examples=[dict(title='稳定度', body='10 发环数 10,9,10,9,8,10,9,10,9,10 → 均值 9.4、标准差 0.7，SD 越小越稳。')],
  faqs=[dict(q='环数还是分组？', a='分组（密集度）比总环更能反映稳定性。')])

KB['sports/assessor-risk-2'] = dict(title='运动损伤风险评估（问卷）',
  scenarios=['赛前用问卷筛高危人群。'],
  examples=[dict(title='评分', body='既往伤史 2 分 + 训练量突增 1 分 + 肌力不平衡 1 分 ≥4 分 → 高危，需加强预防。')],
  faqs=[dict(q='问卷能替代体检？', a='不能，仅初筛，阳性需专业评估。')])

KB['sports/baofali-zongtiao-lidingtiaoyuan'] = dict(title='爆发力（纵跳/立定跳远）',
  scenarios=['用纵跳高度估下肢爆发力。'],
  examples=[dict(title='估算', body='纵跳 40 cm → 起跳速度 v=√(2gh)=√(2·9.8·0.4)≈2.8 m/s；立定跳远 2.4 m 属良好水平。')],
  faqs=[dict(q='纵跳怎么测？', a='Paired 贴标或计时垫测腾空时间反推高度。')])

KB['sports/calc-61'] = dict(title='能量消耗便携计算',
  scenarios=['按项目估热量消耗。'],
  examples=[dict(title='跑步', body='约 1 kcal/kg/km；70 kg 跑 5 km ≈350 kcal（匀速、平路近似）。')],
  faqs=[dict(q='配速影响大？', a='越快单位时间耗能高，但单位距离近似恒定。')])

KB['sports/calc-62'] = dict(title='棒球打击率 / 自责分计算',
  scenarios=['棒球打击率与投手 ERA。'],
  examples=[dict(title='计算', body='安打 30 / 打数 100 → 打击率 AVG=0.300；ERA=自责分×9/局数，3 自责÷7局×9≈3.86。')],
  faqs=[dict(q='AVG 多少算强？', a='MLB 均值约 .250，.300 以上出众。')])

KB['sports/calc-angle-slope'] = dict(title='百分比坡度计算器（运动）',
  scenarios=['跑步/骑行坡度换算。'],
  examples=[dict(title='换算', body='坡度角 5° → 百分比坡度=tan5°×100≈8.75%；10% 坡对应约 5.7°。')],
  faqs=[dict(q='百分比坡含义？', a='每水平 100 上升高度，如 8% 即百米升 8 米。')])

KB['sports/calc-heart-rate-1'] = dict(title='心率储备计算（HRR）',
  scenarios=['按心率储备定训练区间。'],
  examples=[dict(title='计算', body='静息 60、最大 190 → HRR=130；60% 强度区=静息+0.6×130=138 bpm。')],
  faqs=[dict(q='HRR 与最大心率法？', a='HRR 法（Karvonen）更个体化，考虑了静息。')])

KB['sports/calc-length-cutting'] = dict(title='肌肉效贴布裁剪长度计算',
  scenarios=['按贴扎部位估长度。'],
  examples=[dict(title='估算', body='肩部 Y 形贴扎约需 3–4 条各 15–20 cm，总长约 50–60 cm（视体型）。')],
  faqs=[dict(q='张力怎么选？', a='减压 10–15% 张力，助力 25–50%。')])

KB['sports/calc-time'] = dict(title='潜水免减压时间计算（NDL）',
  scenarios=['按深度查免减压极限防减压病。'],
  examples=[dict(title='查表', body='18 m 免减压极限约 56 min，30 m 约 20 min（常用休闲潜水表，单次无停留）。')],
  faqs=[dict(q='重复潜水怎么算？', a='需计入残余氮气，查重复潜水时间表缩短 NDL。')])

KB['sports/calculator-calc-9'] = dict(title='骑行齿比计算器',
  scenarios=['齿比与踏频算速度。'],
  examples=[dict(title='计算', body='前 53 / 后 11 → 齿比 4.82；轮周长 2.1 m、踏频 90 → 速度≈4.82×2.1×90×60≈54.7 km/h。')],
  faqs=[dict(q='齿比大好还是小好？', a='大齿比高速但费力，爬坡用小齿比。')])

KB['sports/calculator-calc-time'] = dict(title='马拉松配速计算器',
  scenarios=['由目标完赛时间算每公里配速。'],
  examples=[dict(title='计算', body='目标 3:30:00、距离 42.195 km → 配速=210min/42.195≈4:58/km。')],
  faqs=[dict(q='负分割策略？', a='后半程略快于前半，利于匀速完赛。')])

KB['sports/climbing-grade-converter'] = dict(title='攀岩难度等级转换',
  scenarios=['V 级（抱石）与 YDS 对照。'],
  examples=[dict(title='对照', body='V5 ≈ YDS 5.11d；V10 ≈ 5.14a（不同体系近似对应）。')],
  faqs=[dict(q='体系差异？', a='V 为抱石、YDS 为先锋，且法/澳标不同。')])

KB['sports/convert-13'] = dict(title='攀岩难度等级转换（V级 ↔ YDS）',
  scenarios=['与 climbing-grade-converter 同义互转。'],
  examples=[dict(title='对照', body='V7 ≈ 5.13a；具体以权威对照表为准。')],
  faqs=[dict(q='为何两套？', a='抱石与时间攀采用不同历史体系。')])

KB['sports/convert-47'] = dict(title='力量（1RM/最大力量）换算',
  scenarios=['由多次重复推单次最大（1RM）。'],
  examples=[dict(title='Epley', body='100 kg 做 5 次 → 1RM=100×(1+5/30)=116.7 kg（Epley 公式）。')],
  faqs=[dict(q='Epley 与 Brzycki？', a='两式近似，次数越少估算越准。')])

KB['sports/convert-time'] = dict(title='铁人三项转换时间（游泳/骑车/跑步）',
  scenarios=['核算 T1/T2 转换耗时。'],
  examples=[dict(title='核算', body='T1（泳→骑）目标 ≤90 s，T2（骑→跑）≤60 s；慢转换可丢名次。')],
  faqs=[dict(q='转换怎么练？', a='专项模拟换项，减少多余动作。')])

KB['sports/detector-14'] = dict(title='无氧阈（拐点）检测',
  scenarios=['由血乳酸拐点定耐力训练强度。'],
  examples=[dict(title='定位', body='渐增负荷中血乳酸由 2 升到 4 mmol/L 的拐点即无氧阈，对应约 85–90% 最大心率。')],
  faqs=[dict(q='无氧阈越高越好？', a='是，代表可维持高强度更久。')])

KB['sports/dianjiezhi-diushi-buchong'] = dict(title='电解质（丢失）补充',
  scenarios=['长时间运动补钠防抽筋/低钠。'],
  examples=[dict(title='补充', body='每小时出汗 1 L 约失钠 500–700 mg；耐力赛中按此补含钠饮品。')],
  faqs=[dict(q='只喝水够吗？', a='大量纯水稀释血钠，需补电解质。')])

KB['sports/diving-no-decompression'] = dict(title='潜水免减压时间计算',
  scenarios=['与 calc-time 同，按深度算 NDL。'],
  examples=[dict(title='查表', body='12 m 约 120 min NDL；随深度减小而缩短。')],
  faqs=[dict(q='安全停留？', a='建议 5 m 做 3 分钟安全停留。')])

KB['sports/estimate-22'] = dict(title='运动补水策略估算',
  scenarios=['按体重丢失定补水量。'],
  examples=[dict(title='估算', body='跑后轻 1 kg（≈失水 1 L）→ 补 1.2–1.5 L 含电解质液（少量多次）。')],
  faqs=[dict(q='脱水多少影响表现？', a='体重降 2% 即明显下滑，>3% 危险。')])

KB['sports/estimate-35'] = dict(title='出汗率估算',
  scenarios=['称重法算出汗量指导补液。'],
  examples=[dict(title='估算', body='运动前 70.0 kg、后 68.8 kg、饮 0.5 L → 出汗≈1.7 L/小时。')],
  faqs=[dict(q='晨重更准？', a='是，固定条件下排空后称重误差小。')])

KB['sports/estimate-tester'] = dict(title='最大摄氧量（VO2max）估算（跑步测试）',
  scenarios=['12 分钟跑（Cooper）估 VO2max。'],
  examples=[dict(title='Cooper', body='12 分钟跑 2.4 km → VO2max=22.35×2.4−11.29≈42.6 mL/kg/min（良好水平）。')],
  faqs=[dict(q='单位含义？', a='每公斤体重每分钟耗氧毫升数，越高有氧能力越强。')])

KB['sports/generator-random-3'] = dict(title='瑜伽体式随机生成（内置常见体式）',
  scenarios=['编排练习随机体式序列。'],
  examples=[dict(title='生成', body='随机序列如 山式→下犬式→战士二→婴儿式（仅演示，非医疗建议）。')],
  faqs=[dict(q='新手能用？', a='需量力，避免勉强高难体式。')])

KB['sports/heart-rate-1'] = dict(title='最大心率个体化计算',
  scenarios=['由年龄估最大心率定强度。'],
  examples=[dict(title='计算', body='最大心率≈220−年龄；30 岁 → 190 bpm（公式近似，个体有差）。')],
  faqs=[dict(q='公式准吗？', a='群体均值，个体差异 ±10–15。')])

KB['sports/heart-rate-2'] = dict(title='心率变异性分析 (HRV)',
  scenarios=['HRV 反映恢复与自主神经平衡。'],
  examples=[dict(title='指标', body='常用 RMSSD（相邻 R-R 间期差均方根），静息越高通常恢复越好。')],
  faqs=[dict(q='HRV 低说明？', a='可能疲劳/压力，宜降负荷。')])

KB['sports/heart-rate-3'] = dict(title='心率恢复指数 (HRR)',
  scenarios=['运动后心率回落速度。'],
  examples=[dict(title='计算', body='运动末 170 bpm，停 1 分钟降至 140 → HRR=30 bpm（≥20 多为良好）。')],
  faqs=[dict(q='HRR 低？', a='提示心肺适能或恢复不足。')])

KB['sports/hongxibao-xieyang-shiyingxing'] = dict(title='红细胞（携氧）适应性',
  scenarios=['高原/训练后红细胞与 Hb 变化。'],
  examples=[dict(title='变化', body='高原适应数周血红蛋白可升 5–10%，提升携氧；需监测铁储备。')],
  faqs=[dict(q='EPO 作用？', a='低氧促 EPO 分泌刺激红细胞生成。')])

KB['sports/jianzhong-tuoshui-buye-kongzhi'] = dict(title='减重（脱水/补液）控制',
  scenarios=['按级别称重控体重。'],
  examples=[dict(title='控制', body='赛前脱水建议 ≤体重 2%，赛后 2 小时内补回 1.2–1.5 L/ kg 丢失。')],
  faqs=[dict(q='急剧减重危害？', a='影响力量与认知，严禁极端脱水。')])

KB['sports/jixianwei-kuai-man-leixingtuice'] = dict(title='肌纤维（快/慢）类型推测',
  scenarios=['由短冲/耐力表现推测纤维偏向。'],
  examples=[dict(title='推测', body='30 m 冲刺快、耐力弱 → 偏快肌（II 型）；反之偏慢肌（I 型）。')],
  faqs=[dict(q='可训练改变？', a='比例相对固定，可改变其表达与代谢。')])

KB['sports/juzhongzongchengji-sinclair-xishu'] = dict(title='举重总成绩 / Sinclair 系数',
  scenarios=['跨级别比较用 Sinclair 系数。'],
  examples=[dict(title='计算', body='抓举 100 kg + 挺举 130 kg = 总成绩 230 kg；再乘该体重级 Sinclair 系数得标准值用于跨级排名。')],
  faqs=[dict(q='Sinclair 作用？', a='消除体重优势，使不同级别可横向比。')])

KB['sports/lanqiumingzhonglv-lanbanxiaolv'] = dict(title='篮球命中率 / 篮板效率',
  scenarios=['FG%、篮板率统计。'],
  examples=[dict(title='计算', body='投篮 20 中 10 → FG%=50%；篮板率=该队篮板/(总篮板)。')],
  faqs=[dict(q='有效命中率？', a='eFG% 给三分额外权重更准。')])

KB['sports/lingmin-zhefanpao-chengji'] = dict(title='灵敏（折返跑）成绩',
  scenarios=['Illinois/折返跑测灵敏。'],
  examples=[dict(title='成绩', body='Illinois 灵敏测试 <15 s 为较好；时间越短越灵敏。')],
  faqs=[dict(q='受什么影响？', a='启动、变向、协调与下肢力量。')])

KB['sports/pingheng-biyandanjiao-shichang'] = dict(title='平衡（闭眼单脚）时长',
  scenarios=['闭眼单脚站测平衡。'],
  examples=[dict(title='成绩', body='闭眼单脚站立 ≥30 s 为平衡良好；老年人 <10 s 提示跌倒风险。')],
  faqs=[dict(q='睁眼差异？', a='睁眼借视觉，闭眼更依赖前庭与本体感觉。')])

KB['sports/pingpangqiu-xiangchi-faqiu-defen'] = dict(title='乒乓球（相持/发球）得分',
  scenarios=['11 分制得分统计。'],
  examples=[dict(title='统计', body='发球得分率=发球直接得分/发球总数；相持得分率=相持赢球/相持总数。')],
  faqs=[dict(q='11 分制？', a='先到 11 且领先 2 分胜。')])

KB['sports/rater-34'] = dict(title='排球（一传到位/扣球）评分',
  scenarios=['一传到位率、扣球成功率。'],
  examples=[dict(title='评分', body='一传 20 次到位 15 → 到位率 75%；扣球 30 扣中 12 → 成功率 40%。')],
  faqs=[dict(q='一传为何关键？', a='到位率决定战术组织质量。')])

KB['sports/rater-35'] = dict(title='柔道（投技/寝技）评分',
  scenarios=['一本/技有等评分。'],
  examples=[dict(title='评分', body='一本（10 分）即胜；技有（7 分）、有效（5 分）累计；寝技压制 10 s 计一本。')],
  faqs=[dict(q='一本条件？', a='大幅摔投或压制 20 s（原 25 s）判一本。')])

KB['sports/rater-36'] = dict(title='马术（步态/跳跃）评分',
  scenarios=['动作规范与障碍扣分。'],
  examples=[dict(title='评分', body='盛装舞步按动作给 0–10 分；障碍碰杆每次罚 4 分。')],
  faqs=[dict(q='罚分来源？', a='超时、拒跳、碰杆均罚分。')])

KB['sports/rater-motion'] = dict(title='技术（动作）稳定性评分',
  scenarios=['动作变异系数 CV 评稳定。'],
  examples=[dict(title='评分', body='10 次动作时长 SD/均值=CV；CV<5% 为稳定，>15% 需修正。')],
  faqs=[dict(q='CV 越小越好？', a='是，代表一致性高。')])

KB['sports/ratio-18'] = dict(title='脂肪氧化供能比例',
  scenarios=['中低强度脂肪供能占比高。'],
  examples=[dict(title='比例', body='约 50–65% 最大摄氧强度脂肪供能比最高；更高强度转糖供能为主。')],
  faqs=[dict(q='减脂区间？', a='中低强度 + 时长更利脂肪氧化，但总耗更重要。')])

KB['sports/rehab-motion'] = dict(title='损伤（预防/康复）动作',
  scenarios=['康复与预防训练动作库。'],
  examples=[dict(title='动作', body='如靠墙静蹲（膝康复）、臀桥（髋稳定）；按阶段递增负荷。')],
  faqs=[dict(q='疼了还练？', a='锐痛停，酸胀可接受，遵医嘱。')])

KB['sports/rouren-qianqu-cequ-jinbu'] = dict(title='柔韧（前屈/侧屈）进步',
  scenarios=['坐位体前屈记录进步。'],
  examples=[dict(title='记录', body='初始 −2 cm、8 周后 +8 cm → 进步 10 cm（坐位体前屈）。')],
  faqs=[dict(q='每天拉更有效？', a='规律温和拉伸+热身更佳，避免弹振拉伤。')])

KB['sports/shejiansanbubanjing'] = dict(title='射箭散布半径',
  scenarios=['分组密集度评估。'],
  examples=[dict(title='计算', body='6 箭着点均距靶心 4 cm → 散布半径约 4 cm，越小越准。')],
  faqs=[dict(q='环数还是散布？', a='比赛看环数，训练看散布定稳定性。')])

KB['sports/sheyangdonglixuebanshi'] = dict(title='摄氧动力学半时',
  scenarios=['运动开始摄氧升至稳态的半时。'],
  examples=[dict(title='半时', body='中等强度摄氧半时约 30 s；快肌多者更快但氧亏大。')],
  faqs=[dict(q='氧亏含义？', a='摄氧滞后于需求的亏欠，由无氧供能补。')])

KB['sports/shuimianhuifuzhiliang'] = dict(title='睡眠恢复质量',
  scenarios=['睡眠时长+深睡估恢复。'],
  examples=[dict(title='评分', body='7–9 h 睡眠、深睡占比 ≥15–20% 恢复较好；<6 h 需警惕过度训练。')],
  faqs=[dict(q='午睡有用？', a='20–30 min 短暂午睡可补，过久影响夜眠。')])

KB['sports/simulator-18'] = dict(title='高原（低氧）适应模拟',
  scenarios=['模拟低氧训练刺激。'],
  examples=[dict(title='模拟', body='间歇低氧（IHT）设 FiO₂≈15% 模拟约 2500 m，刺激红细胞生成。')],
  faqs=[dict(q='替代实地高原？', a='部分，但实地更综合。')])

KB['sports/sleeping-bag-rating'] = dict(title='睡袋温标对照',
  scenarios=['按舒适/极限温标选睡袋。'],
  examples=[dict(title='对照', body='舒适温标 0°C、极限 −5°C 的睡袋，0°C 舒适睡眠、−5°C 为生存下限。')],
  faqs=[dict(q='极限温标能睡？', a='仅保命，舒适温标才体感好。')])

KB['sports/speed-5'] = dict(title='速度加速度分解',
  scenarios=['矢量分解算合速度。'],
  examples=[dict(title='计算', body='vx=3、vy=4 m/s → 合速度=√(9+16)=5 m/s，方向 atan(4/3)≈53°。')],
  faqs=[dict(q='加速度分解同理？', a='是，各分量独立叠加。')])

KB['sports/speed-6'] = dict(title='击剑弓步速度分析',
  scenarios=['弓步伸膝速度。'],
  examples=[dict(title='分析', body='弓步 1.2 m 用 0.3 s → 平均速度 4 m/s，启动越快先得分。')],
  faqs=[dict(q='反应时关键？', a='是，先动且命中才有效。')])

KB['sports/sports-calculator'] = dict(title='体育计算器',
  scenarios=['综合运动指标速算。'],
  examples=[dict(title='计算', body='BMI=体重/身高²；70kg/1.75²≈22.9（正常）。')],
  faqs=[dict(q='BMI 局限？', a='不区分肌肉脂肪，运动员可偏高。')])

KB['sports/sports-reference'] = dict(title='体育户外参考工具',
  scenarios=['查装备/环境参数。'],
  examples=[dict(title='查', body='风速分级、体感温度等户外参考值。')],
  faqs=[dict(q='体感温度？', a='风+湿使体感低于实际气温。')])

KB['sports/sports-schedule'] = dict(title='每周运动计划表',
  scenarios=['安排频率与恢复。'],
  examples=[dict(title='安排', body='每周 3–5 次、力量+有氧+柔韧组合，留 1–2 天完全恢复。')],
  faqs=[dict(q='天天练？', a='不宜，肌肉在恢复中增长。')])

KB['sports/sports-stats'] = dict(title='运动数据统计',
  scenarios=['汇总训练负荷与表现。'],
  examples=[dict(title='统计', body='周跑量 40 km、平均配速 5:10、静息心率降 3 bpm → 有氧提升。')],
  faqs=[dict(q='过度训练信号？', a='静息心率升、成绩降、睡眠差。')])

KB['sports/stats-8'] = dict(title='足球（控球率/传球成功）统计',
  scenarios=['控球率与传球成功率。'],
  examples=[dict(title='计算', body='控球 54 min/90 → 60%；传球 500 成功 420 → 成功率 84%。')],
  faqs=[dict(q='控球率高必胜？', a='不一定，关键在转化效率。')])

KB['sports/strength-5'] = dict(title='训练周计划强度分布 (80/20)',
  scenarios=['极化训练：多数低强度+少数高强度。'],
  examples=[dict(title='安排', body='周训练 80% 低强度（轻松跑）、20% 高强度间歇，提升有氧基底。')],
  faqs=[dict(q='业余也适用？', a='适用，但可放宽至 70/30。')])

KB['sports/swimming-stroke-efficiency'] = dict(title='游泳划水效率计算',
  scenarios=['划距 DPS 评效率。'],
  examples=[dict(title='计算', body='25 m 用 20 划 → DPS=1.25 m/划；划数越少效率越高。')],
  faqs=[dict(q='SWOLF？', a='划数+每 25 m 秒数，越小越高效。')])

KB['sports/taiquandao-hengti-xiapi-defen'] = dict(title='跆拳道（横踢/下劈）得分',
  scenarios=['电子护具得分规则。'],
  examples=[dict(title='得分', body='有效横踢 2 分、下劈 3 分（青少年/成人），旋转技加 1 分。')],
  faqs=[dict(q='几分胜？', a='三局累计高分胜，黄金分制决胜。')])

KB['sports/tent-wind-rating'] = dict(title='户外帐篷防风系数',
  scenarios=['按抗风等级选帐篷。'],
  examples=[dict(title='对照', body='3 季帐抗 5–6 级风，4 季/高山帐可抗 8 级以上；注意地钉与风绳。')],
  faqs=[dict(q='风绳作用？', a='分散受力、显著降低被吹翻概率。')])

KB['sports/tester-1'] = dict(title='俯卧撑/引体向上极限测试（推算1RM）',
  scenarios=['由多次重复推 1RM。'],
  examples=[dict(title='Epley', body='做 15 个俯卧撑（末次力竭）→ 估 1RM≈体重×(1+15/30)；引体同理按附加负重。')],
  faqs=[dict(q='徒手怎么算？', a='以自体重为负荷代入次数公式估算。')])

KB['sports/tester-7'] = dict(title='耐力（AT/VO2max）测试',
  scenarios=['渐增负荷测无氧阈与最大摄氧。'],
  examples=[dict(title='测', body='跑台递增速率，达血乳酸 4 mmol/L 即 AT 强度；峰值估 VO2max。')],
  faqs=[dict(q='多久测一次？', a='周期中测 1–2 次跟踪进展即可。')])

KB['sports/tester-8'] = dict(title='最大（累积氧亏）测试',
  scenarios=['高强度累积氧亏估无氧能力。'],
  examples=[dict(title='测', body='超极量运动至力竭，累计摄氧亏越大无氧产能越强。')],
  faqs=[dict(q='危险吗？', a='极量测试需监护，心肺疾患者禁。')])

KB['sports/time-30'] = dict(title='游泳划水效率 (SWOLF)',
  scenarios=['SWOLF=划数+每 25 m 秒数。'],
  examples=[dict(title='计算', body='25 m 游 20 s、15 划 → SWOLF=35；越小越高效。')],
  faqs=[dict(q='自由泳基准？', a='好选手单趟 SWOLF 约 30–40。')])

KB['sports/time-31'] = dict(title='摔跤比赛时间分配',
  scenarios=['按局时长分配体力。'],
  examples=[dict(title='分配', body='三局各 2 min，局间 30 s；首局试探、末局冲刺。')],
  faqs=[dict(q='分值？', a='不同级别 2–5 分动作，跪撑与地面得分。')])

KB['sports/tongqibizhifenxi'] = dict(title='通气比值分析',
  scenarios=['VE/VO2 通气当量。'],
  examples=[dict(title='分析', body='通气当量=VE/VO2；升高拐点提示代谢性酸中毒（无氧阈附近）。')],
  faqs=[dict(q='VE 是什么？', a='每分通气量。')])

KB['sports/training-load'] = dict(title='超量恢复负荷安排',
  scenarios=['训练-疲劳-恢复的负荷周期。'],
  examples=[dict(title='安排', body='大负荷周后接减载周（量降 40–60%），促成超量恢复。')],
  faqs=[dict(q='一直加量？', a='会过度训练，须周期化。')])

KB['sports/training-planner'] = dict(title='个性化训练计划',
  scenarios=['按目标/水平排计划。'],
  examples=[dict(title='排', body='减脂：每周 4 次有氧+2 次力量+1 柔韧；增肌：分化训练 5 次。')],
  faqs=[dict(q='计划多久调？', a='4–6 周按反馈微调。')])

KB['sports/triathlon-transition'] = dict(title='铁人三项转换时间计算',
  scenarios=['与 convert-time 同，核算 T1/T2。'],
  examples=[dict(title='核算', body='T1+T2 合计控在 2–3 min 内为优秀转换。')],
  faqs=[dict(q='转换练什么？', a='熟练穿脱装备、动线最短。')])

KB['sports/wangqiudefenlvfenxi'] = dict(title='网球得分率分析',
  scenarios=['一发/二发得分率。'],
  examples=[dict(title='计算', body='一发 60 个赢 42 → 一发得分率 70%；二发 30 赢 15 → 50%。')],
  faqs=[dict(q='破发点关键？', a='是，破发直接左右胜负。')])

KB['sports/xuerusuanyuzhiceding'] = dict(title='血乳酸阈值测定',
  scenarios=['血乳酸 4 mmol/L 定强度。'],
  examples=[dict(title='测定', body='渐增负荷采血，乳酸由 1 升到 4 mmol/L 对应强度即乳酸阈（约 85–90% HRmax）。')],
  faqs=[dict(q='乳酸阈=无氧阈？', a='近似，概念略有差异。')])

KB['sports/yangmaiboxiaolv'] = dict(title='氧脉搏效率',
  scenarios=['VO2/HR 评每搏氧效。'],
  examples=[dict(title='计算', body='VO2=2.5 L/min、HR=150 → 氧脉搏=2500/150≈16.7 mL/beat；静息约 5。')],
  faqs=[dict(q='越大越好？', a='是，代表每次心跳摄氧效率。')])

KB['sports/yoga-pose-generator'] = dict(title='瑜伽体式随机生成',
  scenarios=['与 generator-random-3 同，随机体式序列。'],
  examples=[dict(title='生成', body='序列如 猫牛式→战士一→三角式→挺尸式。')],
  faqs=[dict(q='体式 contraindication？', a='伤病者避开对应体式。')])

KB['sports/youyonghuashuixiaolv-swolf'] = dict(title='游泳划水效率（SWOLF）',
  scenarios=['与 time-30 同，SWOLF 效率。'],
  examples=[dict(title='计算', body='50 m 游 40 s、30 划 → SWOLF 按每 25 m 计约 35。')],
  faqs=[dict(q='怎么降 SWOLF？', a='改进划手与节奏、减少打腿耗能。')])

KB['sports/yumaoqiushaqiuxiaolv'] = dict(title='羽毛球杀球效率',
  scenarios=['杀球速度与落点。'],
  examples=[dict(title='效率', body='杀球 80 m/s 且压线得分率高 → 效率高；落点越贴网前越难接。')],
  faqs=[dict(q='杀球速度上限？', a='专业男单可达 400+ km/h。')])

KB['sports/zhangpengfangfengxishu'] = dict(title='帐篷防风系数',
  scenarios=['与 tent-wind-rating 同，防风等级。'],
  examples=[dict(title='对照', body='抗风 8 级（≈17–20 m/s）的高山帐需强地钉与风绳。')],
  faqs=[dict(q='迎风摆放？', a='帐尾迎风减少受风面。')])

KB['sports/pilaohuifuqushi'] = dict(title='疲劳恢复趋势',
  scenarios=['按静息心率/睡眠质量/主观疲劳跟踪恢复。'],
  examples=[dict(title='跟踪', body='连续 3 天静息心率升 5 bpm + 睡眠降 → 疲劳累积，宜减载；回落至基线即恢复。')],
  faqs=[dict(q='单一指标够？', a='不够，宜多指标综合判断避免过度训练。')])

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
