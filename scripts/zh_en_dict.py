# -*- coding: utf-8 -*-
"""
中文工具名/描述 -> 英文 的「语义短语级」翻译引擎（规则版，无外部 API）。
用于 _build.py 在生成 search-index.json / tools.json 时给每个工具注入 en / ed 字段，
使英文模式下首页与行业页卡片显示英文。

设计原则（v2 语义化重构，杜绝机械逐字翻译）：
- **短语级最长匹配**：只认 >=2 字中文短语（函数词 的/和/与/转 例外），
  绝不按单字硬替——「中文几个字 -> 一个自然英文词/词组」（如 贝叶斯后验概率 -> Bayesian Posterior Probability）。
- 类型后缀（计算器/生成器/转换器…）优先英文化；X器 按动作语义推断设备后缀（默认 Device）。
- 保留 ASCII 片段（JSON / Base64 / URL / MD5 …）。
- **安全回退**：翻译结果仍含中文（即整句未翻出）-> 返回干净原文中文，绝不输出中英混杂乱码。
- 覆盖率上限：工具名长尾极散（4275 个不同概念头，多数仅出现 1 次），规则词典无法全覆盖；
  要 100% 自然英文需构建期接 MT（详见 docs/i18n-spec.md §4.1）。
"""

# ===== 类型后缀（仅“X器”类真后缀，最长匹配优先；弱动作词见 DOMAIN 全局替换）=====
TYPE_SUFFIX = [
    ('编解码器', 'Codec'),
    ('编码器', 'Encoder'), ('解码器', 'Decoder'),
    ('转换器', 'Converter'), ('换算器', 'Converter'), ('换器', 'Converter'),
    ('生成器', 'Generator'), ('成器', 'Generator'),
    ('计算器', 'Calculator'), ('算器', 'Calculator'),
    ('估算器', 'Estimator'), ('评估器', 'Evaluator'),
    ('分析器', 'Analyzer'),
    ('校验器', 'Validator'), ('验证器', 'Verifier'),
    ('检测器', 'Detector'), ('测器', 'Detector'),
    ('查询器', 'Finder'), ('选择器', 'Selector'), ('选择器', 'Picker'),
    ('编辑器', 'Editor'), ('解析器', 'Parser'),
    ('模拟器', 'Simulator'), ('对比器', 'Comparator'),
    ('统计器', 'Counter'), ('压缩器', 'Compressor'), ('解压器', 'Decompressor'),
    ('加密器', 'Encryptor'), ('解密器', 'Decryptor'),
    ('检查器', 'Checker'),
    ('记录器', 'Recorder'), ('监视器', 'Monitor'),
    ('播放器', 'Player'), ('控制器', 'Controller'), ('报警器', 'Alarm'),
    ('提取器', 'Extractor'), ('合并器', 'Merger'), ('拆分器', 'Splitter'),
]

# ===== 领域/修饰词 -> 英文（覆盖高频 + 常见领域）=====
DOMAIN = {
    # 技术
    'JSON': 'JSON', 'Base64': 'Base64', 'URL': 'URL', 'URI': 'URI', 'SQL': 'SQL',
    'MD5': 'MD5', 'SHA': 'SHA', 'UUID': 'UUID', 'XML': 'XML', 'HTML': 'HTML',
    'CSS': 'CSS', 'YAML': 'YAML', 'Regex': 'Regex', '正则': 'Regex',
    '二维码': 'QR Code', '条形码': 'Barcode', '哈希': 'Hash', '时间戳': 'Timestamp',
    '密码': 'Password', '随机': 'Random', '颜色': 'Color', '取色': 'Color Picker',
    '调色': 'Color Palette', '字体': 'Font', '字符': 'Character', '文本': 'Text',
    '字符串': 'String', '域名': 'Domain', '网址': 'URL', '邮件': 'Email', '邮箱': 'Email',
    '端口': 'Port', '密钥': 'Key', '签名': 'Signature', '证书': 'Certificate',
    '图片': 'Image', '图像': 'Image', '音频': 'Audio', '视频': 'Video',
    '字幕': 'Subtitle', '表情': 'Emoji', '图标': 'Icon', '标志': 'Logo', 'Logo': 'Logo',
    '代码': 'Code', '脚本': 'Script', '程序': 'Program', '算法': 'Algorithm',
    '网络': 'Network', 'IP': 'IP', 'TCP': 'TCP', 'HTTP': 'HTTP', 'API': 'API',
    '数据库': 'Database', '缓存': 'Cache', 'Cookie': 'Cookie', 'Token': 'Token',
    '文件': 'File', '压缩': 'Compress', '格式': 'Format', '格式化': 'Formatter',
    '进制': 'Base', '字节': 'Byte', '编码': 'Encoding', '解码': 'Decoding',
    # 数学
    '分数': 'Fraction', '小数': 'Decimal', '整数': 'Integer', '百分比': 'Percentage',
    '比例': 'Ratio', '指数': 'Exponent', '对数': 'Logarithm', '矩阵': 'Matrix',
    '向量': 'Vector', '方程': 'Equation', '积分': 'Integral', '微分': 'Derivative',
    '概率': 'Probability', '统计': 'Statistics', '平均值': 'Average', '中位数': 'Median',
    '标准差': 'Standard Deviation', '方差': 'Variance', '素数': 'Prime', '质数': 'Prime',
    '阶乘': 'Factorial', '进制转换': 'Base Converter', '角度': 'Angle', '弧度': 'Radian',
    # 物理
    '长度': 'Length', '重量': 'Weight', '面积': 'Area', '体积': 'Volume',
    '温度': 'Temperature', '速度': 'Speed', '距离': 'Distance', '密度': 'Density',
    '压力': 'Pressure', '力': 'Force', '功率': 'Power', '能量': 'Energy',
    '频率': 'Frequency', '波长': 'Wavelength', '电阻': 'Resistance', '电容': 'Capacitance',
    '电压': 'Voltage', '电流': 'Current', '磁场': 'Magnetic Field', '光照': 'Illumination',
    # 时间/日期
    '时间': 'Time', '日期': 'Date', '星期': 'Weekday', '月份': 'Month', '年份': 'Year',
    '纪元': 'Epoch', '时区': 'Time Zone', '倒计时': 'Countdown', '计时': 'Timer',
    '闹钟': 'Alarm', '日程': 'Schedule', '农历': 'Lunar Calendar', '节气': 'Solar Term',
    # 单位/度量
    '单位': 'Unit', '尺寸': 'Size', '容量': 'Capacity', '剂量': 'Dose',
    '浓度': 'Concentration', '汇率': 'Exchange Rate', '利率': 'Interest Rate',
    # 金融/商业
    '金额': 'Amount', '货币': 'Currency', '利息': 'Interest', '贷款': 'Loan',
    '房贷': 'Mortgage', '复利': 'Compound Interest', '税率': 'Tax Rate', '发票': 'Invoice',
    '工资': 'Salary', '薪资': 'Payroll', '奖金': 'Bonus', '利润': 'Profit', '成本': 'Cost',
    '收益': 'Earnings', '收益': 'Return', '投资': 'Investment', '股票': 'Stock',
    '基金': 'Fund', '保险': 'Insurance', '税务': 'Tax', '记账': 'Bookkeeping',
    '预算': 'Budget', '折扣': 'Discount', '小费': 'Tip', '分期': 'Installment',
    '汇率换算': 'Currency Converter', '理财': 'Finance', '公积金': 'Housing Fund',
    # 健康/生活
    '健康': 'Health', '体脂': 'Body Fat', '卡路里': 'Calorie', '营养': 'Nutrition',
    'BMI': 'BMI', '体重': 'Weight', '身高': 'Height', '血型': 'Blood Type',
    '孕期': 'Pregnancy', '预产期': 'Due Date', '婴儿': 'Baby', '睡眠': 'Sleep',
    '饮食': 'Diet', '食谱': 'Recipe', '菜谱': 'Recipe', '烹饪': 'Cooking',
    '装修': 'Renovation', '家居': 'Home', '家具': 'Furniture', '园艺': 'Garden',
    '宠物': 'Pet', '植物': 'Plant', '花卉': 'Flower', '浇水': 'Watering',
    # 教育/文字
    '字数': 'Word Count', '字数统计': 'Word Counter', '大小写': 'Case', '拼音': 'Pinyin',
    '汉字': 'Chinese Character', '成语': 'Idiom', '诗词': 'Poetry', '文言文': 'Classical Chinese',
    '翻译': 'Translate', '字典': 'Dictionary', '词典': 'Dictionary', '语法': 'Grammar',
    '单词': 'Word', '笔记': 'Notes', '错题': 'Mistakes', '考试': 'Exam', '成绩': 'Score',
    '论文': 'Thesis', '引用': 'Citation', '文献': 'Reference', '查重': 'Plagiarism Check',
    # 图像/设计
    '图像': 'Image', '图片': 'Image', '照片': 'Photo', '头像': 'Avatar',
    '壁纸': 'Wallpaper', '海报': 'Poster', 'Logo': 'Logo', '图标': 'Icon',
    '配色': 'Color Scheme', '调色板': 'Palette', '渐变': 'Gradient', '圆角': 'Rounded Corner',
    '阴影': 'Shadow', '模糊': 'Blur', '滤镜': 'Filter', '水印': 'Watermark',
    '裁剪': 'Crop', '缩放': 'Resize', '抠图': 'Cutout', '拼图': 'Collage',
    # 娱乐/游戏
    '游戏': 'Game', '骰子': 'Dice', '扑克': 'Poker', '彩票': 'Lottery', '抽奖': 'Draw',
    '积分': 'Score', '段位': 'Rank', '攻略': 'Guide', '装备': 'Equipment',
    '角色': 'Character', '地图': 'Map', '建筑': 'Building', '红石': 'Redstone',
    '开奖': 'Draw Result', '接龙': 'Chain', '种子': 'Seed', '我的世界': 'Minecraft',
    # 通用动作/属性（名词化，无“器”的工具名也英文化）
    '免费': 'Free', '在线': 'Online', '工具': '', '神器': '', '助手': 'Assistant',
    '生成': 'Generator', '制作': 'Maker', '创建': 'Creator', '设计': 'Design',
    '计算': 'Calculator', '转换': 'Converter', '换算': 'Converter', '编码': 'Encoder', '解码': 'Decoder',
    '估算': 'Estimator', '评估': 'Evaluator', '分析': 'Analyzer', '检测': 'Detector',
    '查询': 'Lookup', '搜索': 'Search', '对比': 'Comparator', '分类': 'Classifier',
    '分级': 'Grader', '评分': 'Score', '预测': 'Predictor', '模拟': 'Simulator',
    '测试': 'Tester', '校验': 'Validator', '验证': 'Verifier', '速查': 'Quick Reference',
    '参考': 'Reference', '对照': 'Reference', '标准': 'Standard', '安全': 'Security',
    '风险': 'Risk', '质量': 'Quality', '效率': 'Efficiency', '性能': 'Performance',
    '强度': 'Strength', '寿命': 'Lifespan', '周期': 'Cycle', '选型': 'Selection',
    '配置': 'Config', '参数': 'Parameter', '曲线': 'Curve', '数据': 'Data',
    '流量': 'Flow', '运动': 'Motion', '距离': 'Distance', '尺寸': 'Size',
    '比例': 'Ratio', '配比': 'Ratio',
    '浓度': 'Concentration', '选型': 'Selection', '仓储': 'Storage', '物流': 'Logistics',
    '运输': 'Transport', '采购': 'Procurement', '生产': 'Production', '制造': 'Manufacturing',
    '表达式': 'Expression', '去重': 'Deduplicate', '编解码': 'Encode/Decode',
    '转': ' to ', '转义': 'Escape', '字数统计': 'Word Counter',
    '所得税': 'Income Tax', '个人': 'Personal', '宝宝': 'Baby',
    '倒计时器': 'Countdown Timer', '番茄钟': 'Pomodoro Timer',
    '计时器': 'Timer', '记录器': 'Recorder', '监视器': 'Monitor', '播放器': 'Player',
    '控制器': 'Controller', '报警器': 'Alarm', '提取器': 'Extractor', '合并器': 'Merger',
    '拆分器': 'Splitter', '计时': 'Timer', '取名': 'Name Generator',
    # 行业/场景
    '农业': 'Agriculture', '种植': 'Planting', '养殖': 'Farming', '畜牧': 'Livestock',
    '建筑': 'Construction', '地产': 'Real Estate', '装修': 'Renovation',
    '法律': 'Legal', '合同': 'Contract', '条款': 'Clause', '专利': 'Patent',
    '商标': 'Trademark', '版权': 'Copyright', '合规': 'Compliance',
    '营销': 'Marketing', '推广': 'Promotion', '文案': 'Copywriting', '海报': 'Poster',
    '旅行': 'Travel', '机票': 'Flight', '酒店': 'Hotel', '签证': 'Visa', '路线': 'Route',
    '科学': 'Science', '化学': 'Chemistry', '物理': 'Physics', '生物': 'Biology',
    '天文': 'Astronomy', '地理': 'Geography', '历史': 'History', '文化': 'Culture',
    '音乐': 'Music', '乐谱': 'Sheet Music', '和弦': 'Chord', '节拍': 'Beat',
    '写作': 'Writing', '小说': 'Novel', '剧本': 'Script', '标题': 'Title', '摘要': 'Summary',
    '美食': 'Food', '饮料': 'Drink', '咖啡': 'Coffee', '茶': 'Tea', '酒': 'Wine',
    '美妆': 'Beauty', '护肤': 'Skincare', '发型': 'Hair Style', '穿搭': 'Outfit',
    '育儿': 'Parenting', '教育': 'Education', '学习': 'Learning', '读书': 'Reading',
    '职场': 'Career', '简历': 'Resume', '面试': 'Interview', '会议': 'Meeting',
    # 文本/长尾高频动作与修饰（提升覆盖率）
    '提取': 'Extract', '过滤': 'Filter', '排序': 'Sort', '替换': 'Replace',
    '添加': 'Add', '删除': 'Remove', '换行': 'Line Break', '缩进': 'Indent',
    '镜像': 'Mirror', '颠倒': 'Reverse', '合成': 'Synthesis', '提醒': 'Reminder',
    '前缀': 'Prefix', '后缀': 'Suffix', '号码': 'Number', '行号': 'Line Number',
    '关键词': 'Keyword', '上标': 'Superscript', '下标': 'Subscript',
    '待办事项': 'Todo List', '摩斯电码': 'Morse Code', '语音合成': 'Text to Speech',
    '装饰': 'Decorative', '疫苗': 'Vaccine', '驱虫': 'Deworming', '幸运': 'Lucky',
    '草莓': 'Strawberry', '文字': 'Text', '信息熵': 'Entropy', '香农': 'Shannon',
    '哈夫曼': 'Huffman', '平均码长': 'Average Code Length', '时长': 'Duration',
    '增强版': 'Enhanced', '批量': 'Batch', '高级': 'Advanced', '今日': 'Today',
    '数字': 'Number', '大小': 'Size', '两端对齐': 'Justify', '自动': 'Auto',
    '小型大写字母': 'Small Caps', '商业办公': 'Business', '金融财务': 'Finance',
    '健康医疗': 'Health', '领域': 'Field',     '开发': 'Dev',
    '身体质量指数': 'Body Mass Index', '身体': 'Body',
    # 剩余长尾高频词（推高覆盖率）
    '推荐': 'Recommend', '指南': 'Guide', '支持': 'Support', '工作': 'Work',
    '万年历': 'Perpetual Calendar', '世界时钟': 'World Clock', '闰年': 'Leap Year',
    '日历': 'Calendar', '时钟': 'Clock', '增益': 'Gain', '梯度': 'Gradient',
    '下降': 'Descent', '过拟合': 'Overfitting', '损失': 'Loss', '交叉熵': 'Cross Entropy',
    '智能体': 'Agent', '通信': 'Communication', '开销': 'Overhead', '模型': 'Model',
    '融合': 'Fusion', '投票': 'Voting', '查看器': 'Viewer', '上下文': 'Context',
    '窗口': 'Window', '提示词': 'Prompt', '词嵌入': 'Word Embedding', '余弦': 'Cosine',
    '检索': 'Retrieval', '埃特巴什码': 'Atbash Cipher', '住宿': 'Accommodation',
    '发布会': 'Press Conference', '流程表': 'Checklist', '宾客': 'Guest',
    '座位图': 'Seating Chart', '话术': 'Script', '模板': 'Template', '镜架': 'Glasses',
    '餐饮': 'Dining', '保洁': 'Cleaning', '排班': 'Schedule', '日语': 'Japanese',
    '五十音图': 'Hiragana', '练习': 'Practice', '草坪': 'Lawn', '修剪': 'Mowing',
    '高度': 'Height', '穴位': 'Acupoint', '配伍': 'Compatibility', '老年人': 'Elderly',
    '蛋白质': 'Protein', '维生素': 'Vitamin', '胎压': 'Tire Pressure',
    '膳食纤维': 'Dietary Fiber', '达标': 'Target', '交通': 'Traffic', '拥堵': 'Congestion',
    '碳排': 'Carbon Emission', '水足迹': 'Water Footprint', '生态': 'Eco',
    '环保': 'Environmental', '替代': 'Alternative', '类型': 'Type', '预订': 'Booking',
    '评价': 'Review', '材质': 'Material', '风格': 'Style', '适配': 'Fit',
    '特色': 'Feature', '分布': 'Distribution', '方案': 'Plan', '培养': 'Training',
    '人士': 'Person', '产品': 'Product', '设备信息': 'Device Info',
    # ===== v2 扩充：数据挖掘出的高频未覆盖通用词（推高干净英文覆盖率，绝不引入中文）=====
    '使用': 'Use', '输入': 'Input', '输出': 'Output', '的': '', '数学': 'Math',
    '品类': 'Category', '表': 'Table', '研究': 'Research', '基于': 'Based',
    '依据': 'Based on', '根据': 'Based on', '服务': 'Service', '管理': 'Management',
    '人工智能': 'AI', '处理': 'Process', '娱乐': 'Entertainment', '创意': 'Creative',
    '检查': 'Check', '值': 'Value', '摄影': 'Photography', '金融': 'Finance',
    '命令': 'Command', '体系': 'System', '控制': 'Control', '土木': 'Civil',
    '优化': 'Optimization', '流程': 'Process', '机械': 'Mechanical', '趣味': 'Fun',
    '年龄': 'Age', '出行': 'Travel', '工程': 'Engineering', '方法': 'Method',
    '内置': 'Built-in', '报表': 'Report', '财务': 'Finance', '码': 'Code',
    '米': 'Meter', '报告': 'Report', '检验': 'Inspection', '严重度': 'Severity',
    '堆放': 'Stacking', '演练': 'Drill', '汽车': 'Car', '机制': 'Mechanism',
    '费用': 'Fee', '维修': 'Maintenance', '品种': 'Variety', '策略': 'Strategy',
    '儿童': 'Children', '硬度': 'Hardness', '样本量': 'Sample Size', '体育竞技': 'Sports',
    '效果': 'Effect', '改进': 'Improvement', '流速': 'Flow Rate', '焊接': 'Welding',
    '诊断': 'Diagnosis', '防护': 'Protection', '价格': 'Price', '与': 'and',
    '率': 'Rate', '日常': 'Daily', '生活': 'Life',
    # ===== AI 翻译批量补（数据挖掘高频未覆盖通用词，干净英文，无中文）=====
    '系统': 'System', '设备': 'Device', '材料': 'Material', '目标': 'Target',
    '调节': 'Adjust', '活动': 'Activity', '标签': 'Label', '组合': 'Combination',
    '监测': 'Monitor', '常数': 'Constant', '存储': 'Storage', '空气': 'Air',
    '法则': 'Law', '采用': 'Use', '综合': 'Comprehensive', '计划': 'Plan',
    '养护': 'Maintenance', '皮肤': 'Skin', '回报': 'Return', '净': 'Net',
    '信用卡': 'Credit Card', '互': 'Mutual', '记录': 'Record', '数量': 'Quantity',
    '更换': 'Replace', '创作': 'Create', '问卷': 'Questionnaire', '坐标': 'Coordinate',
    '焦耳': 'Joule', '坡度': 'Slope', '风速': 'Wind Speed', '广告': 'Ad',
    '等级': 'Level', '渔业': 'Fishery', '水产': 'Aquaculture', '均': 'Average',
    '样本': 'Sample', '电气': 'Electrical', '语言': 'Language', '竞争': 'Competition',
    '激光': 'Laser', '小时': 'Hour', '竞品': 'Competitor', '需求': 'Demand',
    '折旧': 'Depreciation', '指标': 'Metric', '理想': 'Ideal', '记忆': 'Memory',
    '防潮': 'Moisture-proof', '美化': 'Beautify', '通用': 'General', '系数': 'Coefficient',
    '通过': 'Via', '印度': 'India', '秒': 'Second', '培训': 'Training',
    '三项': 'Three-phase', '加密': 'Encrypt', '解密': 'Decrypt', '热': 'Thermal',
    '初': 'Initial', '逗号分隔': 'Comma-separated', '中华': 'China', '医疗专业': 'Medical',
    '医疗保健': 'Healthcare', '分型': 'Classification', '过程能': 'Process Capability',
    '肾小球滤过': 'Glomerular Filtration', '数': 'Number', '量': 'Amount', '比': 'Ratio',
    '法': 'Method', '度': 'Degree', '和': 'and', '日': 'Day', '二': 'Two', '分': 'Minute',
    '米': 'Meter', '选择': 'Selection', '计算': 'Calculate', '生成': 'Generate',
    '转换': 'Convert', '处理': 'Process', '分析': 'Analysis', '设计': 'Design',
    '管理': 'Management', '控制': 'Control', '查询': 'Query', '测试': 'Test',
    '验证': 'Verify', '检测': 'Detect', '预测': 'Predict', '模拟': 'Simulate',
    '评估': 'Evaluate', '估算': 'Estimate', '创建': 'Create', '制作': 'Make',
    '编辑': 'Edit', '解析': 'Parse', '提取': 'Extract', '合并': 'Merge',
    '拆分': 'Split', '压缩': 'Compress', '加密': 'Encrypt', '解密': 'Decrypt',
    '编码': 'Encode', '解码': 'Decode', '格式化': 'Format', '转换': 'Convert',
    '换算': 'Convert', '校验': 'Check', '对比': 'Compare', '分类': 'Classify',
    '统计': 'Statistics', '排序': 'Sort', '过滤': 'Filter', '替换': 'Replace',
    '添加': 'Add', '删除': 'Remove', '检查': 'Check', '查看': 'View',
    '导出': 'Export', '导入': 'Import', '生成器': 'Generator', '计算器': 'Calculator',
    '转换器': 'Converter', '编辑器': 'Editor', '解析器': 'Parser', '校验器': 'Validator',
    '检测器': 'Detector', '选择器': 'Selector', '分析器': 'Analyzer',
    '提取器': 'Extractor', '合并器': 'Merger', '拆分器': 'Splitter', '压缩器': 'Compressor',
    '记录器': 'Recorder',     '播放器': 'Player', '控制器': 'Controller',
}

# ===== AI 语义短语层（整段短语 -> 自然英文；中文几个字对应一个英文词，绝不按字硬替）=====
# 仅收录 >=2 字短语；函数词 的/和/与/转 在 SAFE_SINGLE 例外。
SEMANTIC = {
    # —— ML / AI / 统计 ——
    '贝叶斯': 'Bayesian', '后验概率': 'Posterior Probability', '先验概率': 'Prior Probability',
    '先验': 'Prior', '欧氏距离': 'Euclidean Distance', '混淆矩阵': 'Confusion Matrix',
    '聚类': 'Clustering', '聚类分析': 'Cluster Analysis', '梯度下降': 'Gradient Descent',
    '正则化': 'Regularization', '特征缩放': 'Feature Scaling', '数据增强': 'Data Augmentation',
    '召回率': 'Recall', '分类准确率': 'Classification Accuracy', '准确率': 'Accuracy',
    '精确率': 'Precision', '均方误差': 'Mean Squared Error', '信息增益': 'Information Gain',
    '过拟合': 'Overfitting', '早停': 'Early Stopping', '早停耐心': 'Early Stopping Patience',
    '批量大小': 'Batch Size', '迭代次数': 'Iteration Count', '多智能体': 'Multi-Agent',
    '卷积': 'Convolution', '卷积输出': 'Convolution Output', '模型融合': 'Model Ensemble',
    '加权投票': 'Weighted Voting', '交叉熵损失': 'Cross Entropy Loss', '词嵌入': 'Word Embedding',
    '检索增强': 'Retrieval-Augmented', '假阳性': 'False Positive', '假阴性': 'False Negative',
    '代价函数': 'Cost Function', '线性回归': 'Linear Regression', '逻辑回归': 'Logistic Regression',
    '决策树': 'Decision Tree', '随机森林': 'Random Forest', '神经网络': 'Neural Network',
    '损失函数': 'Loss Function', '激活函数': 'Activation Function', '注意力': 'Attention',
    '嵌入': 'Embedding', '微调': 'Fine-tuning', '训练': 'Training', '推理': 'Inference',
    '数据集': 'Dataset', '标注': 'Annotation', '梯度': 'Gradient', '下降': 'Descent',
    '特征': 'Feature', '缩放': 'Scaling', '增强': 'Augmentation', '召回': 'Recall',
    '代价': 'Cost', '回归': 'Regression', '线性': 'Linear', '逻辑': 'Logistic',
    '激活': 'Activation', '融合': 'Ensemble',
    # —— 密码学 / 编码 ——
    '凯撒密码': 'Caesar Cipher', '仿射密码': 'Affine Cipher', '培根密码': 'Bacon Cipher',
    '栅栏密码': 'Rail Fence Cipher', '维吉尼亚密码': 'Vigenère Cipher',
    '波利比奥斯方阵': 'Polybius Square', '普莱费尔密码': 'Playfair Cipher',
    '流加密': 'Stream Cipher', '分组加密': 'Block Cipher', '密钥派生': 'Key Derivation',
    '碰撞概率': 'Collision Probability', '检错能力': 'Error Detection Capability',
    '校验位宽': 'Checksum Width', '汉明码': 'Hamming Code', '汉明距离': 'Hamming Distance',
    '编码冗余度': 'Coding Redundancy', '助记词': 'Mnemonic', '方阵': 'Square',
    '北约音标字母': 'NATO Phonetic Alphabet', '数字缩写': 'Numeronym',
    '凯撒': 'Caesar', '仿射': 'Affine', '培根': 'Bacon', '栅栏': 'Rail Fence',
    '维吉尼亚': 'Vigenère', '波利比奥斯': 'Polybius', '普莱费尔': 'Playfair',
    '冗余': 'Redundancy', '派生': 'Derivation', '碰撞': 'Collision', '检错': 'Error Detection',
    '校验位': 'Checksum Bits', '汉明': 'Hamming',
    # —— 数据 / 文本 / 开发工具 ——
    '数据透视表': 'Pivot Table', '数据清洗': 'Data Cleaning', '数据可视化': 'Data Visualization',
    '文本反转': 'Text Reversal', '全角半角': 'Full-width/Half-width', '代码注释': 'Code Comment',
    '单词顺序': 'Word Order', '文字转横幅': 'Text to Banner', '横幅': 'Banner',
    '占位图': 'Placeholder Image', '语法高亮': 'Syntax Highlighting', '嵌套检查': 'Nesting Check',
    '路径提取': 'Path Extraction', '字符串混淆': 'String Obfuscation', '简化器': 'Minifier',
    '简化': 'Minify', '缩写': 'Abbreviation', '按键码': 'Key Code', '键码': 'Key Code',
    '摄像头录制': 'Camera Recording', '数学表达式': 'Math Expression', '位运算': 'Bitwise',
    '子网': 'Subnet', '权限': 'Permission', '基准测试': 'Benchmark', '抽象语法树': 'AST',
    '可读性': 'Readability', '目录树': 'Directory Tree', '正则可视化': 'Regex Visualization',
    '可视化': 'Visualization', '清洗': 'Cleaning', '反转': 'Reverse', '反转工具': 'Reverser',
    '全角': 'Full-width', '半角': 'Half-width', '注释': 'Comment', '占位': 'Placeholder',
    '高亮': 'Highlight', '嵌套': 'Nesting', '路径': 'Path', '规范化': 'Normalization',
    '混淆器': 'Obfuscator', '求值': 'Evaluate', '摄像': 'Camera', '录制': 'Recording',
    '抽象': 'Abstract', '语法树': 'Syntax Tree',
    # —— 医疗 / 护理 / 生活 ——
    '冰袋冷敷': 'Ice Pack Cold Compress', '安全防护用品': 'PPE', '更换周期': 'Replacement Interval',
    '临床护理': 'Clinical Care', '园艺月历': 'Gardening Calendar', '待办事项列表': 'Todo List',
    '按行去重': 'Line Deduplication', '按行过滤': 'Line Filter', '提取IP地址': 'Extract IP Address',
    '提取中文字符': 'Extract Chinese Characters', '提取电话号码': 'Extract Phone Number',
    '提取英文字符': 'Extract English Characters', '文本分割': 'Text Split', '文本填充': 'Text Fill',
    '文本合并': 'Text Merge', '种植密度': 'Planting Density', '播种日期': 'Sowing Date',
    '退休年龄': 'Retirement Age', '经济补偿': 'Economic Compensation', '退税': 'Tax Refund',
    '年金现值': 'Annuity Present Value', '停车费用': 'Parking Fee', '境外购物': 'Overseas Shopping',
    '相对湿度': 'Relative Humidity', '体感温度': 'Apparent Temperature', '动能': 'Kinetic Energy',
    '重力势能': 'Gravitational Potential Energy', '库仑力': 'Coulomb Force', '雷诺数': 'Reynolds Number',
    '运动黏度': 'Kinematic Viscosity', '单摆周期': 'Pendulum Period', '望远镜放大率': 'Telescope Magnification',
    '极差': 'Range', '复数': 'Complex', '日期差': 'Date Difference', '演讲': 'Speech',
    '呼吸': 'Breathing', '冰袋': 'Ice Pack', '冷敷': 'Cold Compress', '安全防护': 'Safety Protection',
    '用品': 'Supplies', '更换': 'Replacement', '临床': 'Clinical', '护理': 'Care',
    '月历': 'Calendar', '待办': 'Todo', '按行': 'Line-by-line', '字符': 'Character',
    '分割': 'Split', '填充': 'Fill', '合并': 'Merge', '种植': 'Planting', '密度': 'Density',
    '播种': 'Sowing', '退休': 'Retirement', '购物': 'Shopping', '相对': 'Relative',
    '体感': 'Apparent', '重力': 'Gravitational', '势能': 'Potential Energy', '库仑': 'Coulomb',
    '雷诺': 'Reynolds', '黏度': 'Viscosity', '单摆': 'Pendulum', '望远镜': 'Telescope',
    '放大率': 'Magnification',
    # —— 通用动作/名词（语义化，非单字）——
    '计算': 'Calculate', '生成': 'Generate', '转换': 'Convert', '处理': 'Process',
    '分析': 'Analysis', '设计': 'Design', '管理': 'Management', '控制': 'Control',
    '查询': 'Query', '测试': 'Test', '验证': 'Verify', '检测': 'Detect', '预测': 'Predict',
    '模拟': 'Simulate', '评估': 'Evaluate', '估算': 'Estimate', '创建': 'Create',
    '制作': 'Make', '编辑': 'Edit', '解析': 'Parse', '提取': 'Extract', '合并': 'Merge',
    '拆分': 'Split', '压缩': 'Compress', '加密': 'Encrypt', '解密': 'Decrypt',
    '编码': 'Encode', '解码': 'Decode', '格式化': 'Format', '换算': 'Convert',
    '校验': 'Check', '对比': 'Compare', '分类': 'Classify', '统计': 'Statistics',
    '排序': 'Sort', '过滤': 'Filter', '替换': 'Replace', '添加': 'Add', '删除': 'Remove',
    '检查': 'Check', '查看': 'View', '导出': 'Export', '导入': 'Import',
}
DOMAIN.update(SEMANTIC)

import re

_ZH_RUN = re.compile(r'[一-鿿]+')

def _has_chinese(s):
    """结果是否仍含中文（即规则翻译未覆盖，属乱码风险）。"""
    return bool(_ZH_RUN.search(s or ''))

# 安全单字例外：仅函数词允许单字翻译（避免「按字替换」的机械翻译）
SAFE_SINGLE = {'的', '和', '与', '转'}

# 短语级最长匹配表：只取 >=2 字短语 + 安全单字，彻底禁用单字硬替
PHRASES = sorted(
    ((k, v) for k, v in DOMAIN.items() if len(k) >= 2 or k in SAFE_SINGLE),
    key=lambda kv: -len(kv[0]),
)

# X器 通用后缀推断：X 为「器」前中文主体，按动作语义选后缀，默认 Device
ACTION_SUFFIX = {
    '计算': 'Calculator', '测算': 'Calculator', '估算': 'Estimator', '概算': 'Estimator',
    '测量': 'Meter', '测': 'Meter', '计量': 'Meter', '量测': 'Meter',
    '评估': 'Evaluator', '评价': 'Evaluator', '评分': 'Scorer', '评级': 'Grader',
    '分级': 'Grader', '分类': 'Classifier', '分型': 'Classifier', '判别': 'Classifier',
    '分析': 'Analyzer', '检测': 'Detector', '探测': 'Detector', '探测': 'Probe',
    '生成': 'Generator', '换算': 'Converter', '转换': 'Converter', '变换': 'Converter',
    '编译': 'Compiler', '测试': 'Tester', '模拟': 'Simulator', '仿真': 'Simulator',
    '编辑': 'Editor', '查询': 'Finder', '检索': 'Finder', '搜索': 'Searcher',
    '选择': 'Selector', '记录': 'Recorder', '播放': 'Player', '控制': 'Controller',
    '提取': 'Extractor', '合并': 'Merger', '拆分': 'Splitter', '分割': 'Splitter',
    '压缩': 'Compressor', '解压': 'Decompressor', '加密': 'Encryptor', '解密': 'Decryptor',
    '校验': 'Validator', '验证': 'Verifier', '监测': 'Monitor', '监视': 'Monitor',
    '调节': 'Regulator', '诊断': 'Diagnoser', '筛查': 'Screener', '鉴别': 'Identifier',
    '识别': 'Identifier', '灭火': 'Extinguisher', '问卷': 'Questionnaire', '扫描': 'Scanner',
    '混淆': 'Obfuscator', '计数': 'Counter', '比较': 'Comparator',
    # 工程/电子高频 X器
    '分流': 'Splitter', '分压': 'Divider', '继电': 'Relay', '传感': 'Sensor',
    '滤波': 'Filter', '放大': 'Amplifier', '衰减': 'Attenuator', '变压': 'Transformer',
    '整流': 'Rectifier', '逆变': 'Inverter', '伺服': 'Servo', '执行': 'Actuator',
    '驱动': 'Driver', '变送': 'Transmitter', '调理': 'Conditioner', '隔离': 'Isolator',
    '耦合': 'Coupler', '调制': 'Modulator', '解调': 'Demodulator', '振荡': 'Oscillator',
    '发生': 'Generator', '稳压': 'Regulator', '限幅': 'Limiter', '混频': 'Mixer',
    '倍频': 'Multiplier', '分频': 'Divider', '锁相': 'PLL', '收发': 'Transceiver',
    '适配': 'Adapter', '分配': 'Distributor', '收集': 'Collector', '喷射': 'Injector',
    '吸收': 'Absorber', '燃烧': 'Burner', '加热': 'Heater', '冷却': 'Cooler',
    '冷凝': 'Condenser', '蒸发': 'Evaporator', '干燥': 'Dryer', '洗涤': 'Scrubber',
    '搅拌': 'Mixer', '粉碎': 'Crusher', '切割': 'Cutter', '钻孔': 'Drill',
    '打磨': 'Polisher', '焊接': 'Welder', '喷涂': 'Sprayer', '限位': 'Limiter',
    '定位': 'Positioner', '抓取': 'Gripper', '搬运': 'Mover', '翻转': 'Inverter',
    '转向': 'Steering', '制动': 'Brake', '牵引': 'Traction', '悬挂': 'Suspension',
}

# 设备/类型后缀词集合（用于避免双后缀，如 Score Scorer）
DEV_WORDS = set()
for _, v in TYPE_SUFFIX:
    DEV_WORDS.add(v)
for _, v in ACTION_SUFFIX.items():
    DEV_WORDS.add(v)
DEV_WORDS.update({
    'Calculator', 'Generator', 'Converter', 'Encoder', 'Decoder', 'Validator',
    'Verifier', 'Detector', 'Finder', 'Picker', 'Editor', 'Parser', 'Analyzer',
    'Simulator', 'Comparator', 'Counter', 'Compressor', 'Encryptor', 'Decryptor',
    'Checker', 'Recorder', 'Monitor', 'Player', 'Controller', 'Alarm', 'Extractor',
    'Merger', 'Splitter', 'Device', 'Meter', 'Estimator', 'Evaluator', 'Scorer',
    'Grader', 'Classifier', 'Screener', 'Identifier', 'Probe', 'Compiler', 'Tester',
    'Searcher', 'Regulator', 'Diagnoser', 'Obfuscator', 'Scanner', 'Relay', 'Sensor',
    'Amplifier', 'Attenuator', 'Transformer', 'Rectifier', 'Inverter', 'Servo',
    'Actuator', 'Driver', 'Transmitter', 'Conditioner', 'Isolator', 'Coupler',
    'Modulator', 'Demodulator', 'Oscillator', 'PLL', 'Transceiver', 'Adapter',
    'Distributor', 'Collector', 'Injector', 'Absorber', 'Burner', 'Heater', 'Cooler',
    'Condenser', 'Evaporator', 'Dryer', 'Scrubber', 'Mixer', 'Crusher', 'Cutter',
    'Drill', 'Polisher', 'Welder', 'Sprayer', 'Limiter', 'Positioner', 'Gripper',
    'Mover', 'Steering', 'Brake', 'Traction', 'Suspension', 'Questionnaire',
    'Extinguisher',
})

def _translate_token(tok):
    """翻译一段连续中文（短语级最长匹配；支持 X器 通用后缀推断；绝不按字硬替）。"""
    if tok in DOMAIN and (len(tok) >= 2 or tok in SAFE_SINGLE):
        return DOMAIN[tok]
    dev = ''
    t = tok
    if t.endswith('器'):
        t = t[:-1]
        dev = 'Device'
        for k, v in ACTION_SUFFIX.items():
            if t.endswith(k):
                dev = v
                break
    result = t
    for zh, en in PHRASES:
        if zh and zh in result:
            result = result.replace(zh, ' ' + en + ' ')
    result = result.strip()
    if dev:
        if _has_chinese(result):
            return result + ' 器'   # 含中文 -> 上层安全回退（绝不输出乱码）
        last = result.split()[-1] if result.split() else ''
        if last in DEV_WORDS:
            dev = ''               # 避免双后缀（如 Score Scorer）
        return (result + ' ' + dev).strip() if dev else result
    return result

def translate_text(text):
    """翻译工具名或描述：保留 ASCII 片段，中文逐词替换，类型后缀英文化。"""
    if not text:
        return ''
    out = text
    # 类型后缀：按长度降序遍历，最长匹配优先（避免“析器”误匹配“解析器”）
    for zh, en in sorted(TYPE_SUFFIX, key=lambda kv: -len(kv[0])):
        if zh and out.endswith(zh):
            out = out[: -len(zh)] + en
            break
    parts = re.split(r'([A-Za-z0-9_.\-]+)', out)
    res = []
    for p in parts:
        if not p:
            continue
        if re.match(r'^[A-Za-z0-9_.\-]+$', p):
            res.append(p)
        elif _ZH_RUN.search(p):
            res.append(_translate_token(p).strip())
        else:
            res.append(p)
    s = ' '.join(x for x in res if x).strip()
    s = re.sub(r'\s+', ' ', s)
    s = s.strip()
    # 安全回退：规则翻译未覆盖全部中文 -> 返回干净原文，绝不输出中英混杂乱码
    if _has_chinese(s):
        return (text or '').strip()
    return s

def translate_name(name):
    """工具名翻译：去掉 - 副标题/括号说明，主名翻译后拼回。

    营销模板后缀（含“免费/在线工具/领域”等）直接丢弃，不翻译。
    安全回退：只要结果仍含中文，一律返回干净原文中文，绝不输出乱码。
    """
    if not name:
        return ''
    main = name
    suffix = ''
    if ' - ' in name:
        main, suffix = name.split(' - ', 1)
    elif '（' in name:
        idx = name.index('（')
        main, suffix = name[:idx], name[idx:]
    en = translate_text(main)
    if not en or _has_chinese(en):
        return name
    if suffix:
        # 营销模板后缀（免费XX工具 / XX领域的在线工具）丢弃
        if re.search(r'免费|在线工具|领域', suffix):
            return en.strip()
        suf = translate_text(suffix)
        if not suf or _has_chinese(suf):
            # 副标题含未翻译中文：保留已干净的英文主名，丢弃副标题（不整条回退乱码）
            return en.strip()
        return (en + ' - ' + suf).strip()
    return en.strip()

if __name__ == '__main__':
    tests = [
        'JSON 格式化', 'Base64 编解码', '二维码生成', '密码生成器',
        'Markdown 转 HTML', '时间戳转换', '单位换算', 'BMI 计算器',
        '颜色选择器', '正则表达式测试', 'UUID 生成', '字数统计',
        '文本去重', '汇率换算', '倒计时器', '番茄钟', 'IP 计算器',
        '哈希计算', 'HTML 转义', '颜色转换', '.properties 解析器',
        '房贷计算器', '个人所得税计算器', '卡路里计算器', '宝宝取名',
        '成语接龙', '菜谱生成器', '我的世界种子生成器', '彩票开奖查询',
    ]
    for t in tests:
        print('%-22s -> %s' % (t, translate_name(t)))
