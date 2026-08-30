# -*- coding: utf-8 -*-
"""
生成 /guides/ 下的 20 篇高频工具使用指南 + 指南中心(index.html) + json/guides.json(供工具页自动注入"使用指南"链接)。
纯前端、无依赖。运行：python3 _gen_guides.py
"""
import os, json, html

ROOT = os.path.dirname(os.path.abspath(__file__))
GUIDES_DIR = os.path.join(ROOT, 'guides')
JSON_DIR = os.path.join(ROOT, 'json')
os.makedirs(GUIDES_DIR, exist_ok=True)

SITE = 'https://chenguangwu.github.io'

# 工具元数据：slug(指南文件名前缀) / tool(仓库根相对路径) / 显示名 / 描述
# 每篇指南含：intro(引言) / features(核心功能) / scenarios(适用场景) / steps(使用步骤) / tips(实用技巧) / faqs(常见问题)
GUIDES = [
 {
  'slug':'qrcode','tool':'tools/it/qrcode.html','name':'二维码生成器',
  'desc':'二维码生成器使用指南：文本、网址、WiFi、名片等一键生成可下载的二维码图片。',
  'intro':'二维码（QR Code）已经成为信息流转的通用入口。ToolBox 二维码生成器完全在浏览器本地运行，输入文本、网址、WiFi 信息或联系人名片，即可实时生成高清二维码并下载为 PNG/SVG，全程数据不上传服务器。',
  'features':['支持文本、网址(URL)、WiFi、邮箱、电话、短信、地理位置等多种内容类型','实时预览，输入即生成，无需点击按钮','可选纠错级别(L/M/Q/H)，平衡容错率与密度','支持 PNG 位图与 SVG 矢量两种导出格式','自定义前景/背景颜色与边距，适配品牌场景'],
  'scenarios':['把公众号链接、商品页生成二维码印在海报上','共享 WiFi 时生成二维码，访客扫码自动联网','展会名片：把联系方式生成二维码方便交换','线下物料：菜单、桌牌、宣传单上的跳转入口'],
  'steps':['在输入框选择内容类型（文本/网址/WiFi/名片等）','填写对应内容，页面会实时显示二维码预览','按需调整纠错级别与尺寸：人多、易污损场景选 H 级','点击"下载 PNG"或"下载 SVG"保存到本地','（可选）修改前景色/背景色，确保打印后对比度足够'],
  'tips':['纠错级别越高越耐脏污，但图案越密；户外物料建议 L/H 之间权衡','打印二维码务必保留至少 4 个模块(静区)的空白边距，否则可能扫不出','深色前景 + 浅色背景对比度最高，避免相近色','WiFi 二维码包含密码，注意只在可信环境分享'],
  'faqs':[('二维码扫不出来怎么办？','优先检查静区边距是否足够、对比度是否过低，以及纠错级别是否过低；重新生成并提高纠错级别通常可解决。'),('生成的二维码会被上传吗？','不会。所有生成在浏览器本地完成，内容不会发送到任何服务器。')]
 },
 {
  'slug':'json-formatter','tool':'tools/it/json-formatter.html','name':'JSON 格式化',
  'desc':'JSON 格式化使用指南：压缩/美化 JSON、校验语法、折叠展开，前端调试必备。',
  'intro':'JSON 是前后端通信的事实标准，但原始的压缩 JSON 难以阅读。ToolBox JSON 格式化工具在本地帮你美化缩进、校验语法错误、折叠展开节点，是调试接口返回值的得力助手。',
  'features':['一键美化：压缩 JSON 按层级缩进显示','语法校验：定位缺失的引号、逗号、括号等错误','紧凑模式：把美化后的 JSON 再压缩成单行','树形折叠：大对象可逐层展开/收起','复制结果：格式化后一键复制'],
  'scenarios':['对接接口时查看后端返回的 JSON 结构','排查前端报错：定位 JSON.parse 失败的准确位置','整理配置文件、日志片段','对比两份 JSON 的结构差异'],
  'steps':['把原始 JSON 粘贴到左侧输入框','点击"格式化"，右侧出现带缩进的结果','若提示语法错误，按高亮位置修正后重试','需要折叠时点击行首三角收起子节点','点击"复制"把结果用于代码或文档'],
  'tips':['格式化前先确认内容确实为 JSON，而非 XML 或 YAML','超长单行 JSON 建议先格式化再阅读，错误位置更易定位','生产环境不要把包含密钥的 JSON 粘贴到不可信的在线工具，本地工具更安全'],
  'faqs':[('为什么提示 JSON 语法错误？','常见原因是尾部多了逗号、键名没加双引号、或使用了单引号；按提示位置修正即可。'),('格式化会修改数据吗？','不会，仅调整排版与缩进，数据内容保持不变。')]
 },
 {
  'slug':'base64','tool':'tools/it/base64.html','name':'Base64 编解码',
  'desc':'Base64 编解码使用指南：文本与 Base64 互转，支持文件转 Base64 data URI。',
  'intro':'Base64 把二进制或文本数据编码为可打印字符，常用于在文本协议(如 JSON、CSS、邮件)中内嵌数据。ToolBox Base64 工具在本地完成编码与解码，支持字符串与文件互转。',
  'features':['文本 ↔ Base64 双向转换','文件转 Base64：图片/文件生成 data URI','URL 安全模式：把 + / = 替换为 - _ 去掉填充','一键复制结果','支持大文件分块，避免卡顿'],
  'scenarios':['把小图标转 Base64 内联进 CSS，减少请求','在仅支持文本的接口里传输二进制','邮件正文内嵌附件内容','调试含 Base64 字段的接口数据'],
  'steps':['选择"编码"或"解码"模式','编码：粘贴文本或选择文件；解码：粘贴 Base64 字符串','如需兼容 URL 参数，勾选"URL 安全"','点击转换，结果实时显示','点击复制或下载'],
  'tips':['Base64 会使数据体积增大约 33%，不宜用于大文件长期存储','图片内联 Base64 适合小图标，大图仍建议用独立文件+缓存','解码前确认是标准 Base64，URL 安全编码需先切回标准模式'],
  'faqs':[('Base64 是加密吗？','不是。Base64 只是编码，任何人都能解码，切勿用来"保密"敏感信息。'),('data URI 太长怎么办？','说明原始文件偏大，建议改用独立文件引用而非内联。')]
 },
 {
  'slug':'password-generator','tool':'tools/it/password-generator.html','name':'密码生成器',
  'desc':'密码生成器使用指南：生成高强度随机密码，自定义长度与字符集，保障账号安全。',
  'intro':'弱密码是账号被盗的首要原因。ToolBox 密码生成器在浏览器本地用强随机数生成密码，不联网、不上传，可自定义长度、是否包含大小写/数字/符号。',
  'features':['可调长度（建议 12 位以上）','独立开关：大写、小写、数字、符号','排除易混淆字符(如 0/O/1/l)可选','一键复制，不落地存储','基于浏览器密码学安全随机源'],
  'scenarios':['为新账号生成高强度主密码','为不同网站生成不重复的独立密码','生成 API Key、临时令牌的随机串','团队协作时分配一次性访问口令'],
  'steps':['设定密码长度，重要账号建议 ≥16 位','勾选需要的字符类型，默认全选最安全','（可选）开启"排除易混淆字符"避免抄写出错','点击生成，预览密码','点击复制并立即存入密码管理器'],
  'tips':['每个网站使用不同密码，配合密码管理器最稳妥','不要用生日、地名、连续数字等弱组合','生成后立刻保存，不要在多处明文粘贴','开启双重验证(2FA)比单纯加长密码更有效'],
  'faqs':[('生成的密码安全吗？','使用浏览器原生强随机数源，且在本地生成不联网，安全性高。'),('为什么建议用密码管理器？','人脑难记大量强密码，管理器可加密保管并自动填充。')]
 },
 {
  'slug':'timestamp-converter','tool':'tools/it/timestamp-converter.html','name':'时间戳转换',
  'desc':'时间戳转换使用指南：Unix 时间戳与日期互转，支持秒/毫秒与多时区。',
  'intro':'Unix 时间戳（自 1970-01-01 起的秒/毫秒数）广泛用于日志与接口。ToolBox 时间戳转换在本地帮你在"时间戳 ⇄ 可读日期"之间互转，并支持毫秒识别。',
  'features':['时间戳 → 日期：自动识别秒或毫秒','日期 → 时间戳：生成秒级与毫秒级两种','显示当前时间戳，一键刷新','支持本地时区展示','批量/逐个转换皆可'],
  'scenarios':['排查日志：把接口返回的时间戳还原成具体时间','调试代码：确认时区与单位(秒/毫秒)是否一致','数据库时间字段核对','跨系统时间对齐'],
  'steps':['查看当前时间戳作为参照','在"转日期"框粘贴时间戳，自动判断秒/毫秒并显示日期','在"转时间戳"框选择日期时间，生成对应秒/毫秒值','注意结果所在的时区是否为你预期','复制需要的值用于代码或文档'],
  'tips':['最常见坑：把毫秒当秒用会差 1000 倍，工具会自动识别但请复核','前后端约定好单位，避免前端用秒、后端用毫秒','涉及展示时统一用用户本地时区，存储用 UTC'],
  'faqs':[('秒和毫秒怎么区分？','13 位通常是毫秒，10 位是秒；本工具会尝试自动判断。'),('为什么不同机器显示时间不同？','因为时区设置不同，底层时间戳是一致的。')]
 },
 {
  'slug':'unit-converter','tool':'tools/life/unit-converter.html','name':'单位换算',
  'desc':'单位换算使用指南：长度、重量、体积、温度等常见单位一键换算。',
  'intro':'日常与工程中频繁遇到单位换算。ToolBox 单位换算在本地覆盖长度、面积、重量、体积、温度、速度等常用类别，输入即换算。',
  'features':['多类别：长度/面积/体积/重量/温度/速度/时间等','实时换算，切换单位即时更新','常见单位全覆盖（米、英尺、公斤、磅、℃/℉…）','清晰展示换算系数','支持小数精度调整'],
  'scenarios':['海淘时把英寸/磅换算成厘米/公斤','烹饪按食谱换算杯与毫升','装修面积、体积估算','出行温度(℃/℉)快速对照'],
  'steps':['选择换算类别（如长度）','输入数值并选择源单位','选择目标单位，结果实时出现','如需多组对比，可分批换算并对比系数','复制结果'],
  'tips':['温度换算不是线性比例（℃→℉ 有 +32），工具已内置公式','跨境购物注意"盎司"有常衡/金衡之分，重量用常衡','大数换算注意单位量级，避免漏看 k/m 前缀'],
  'faqs':[('温度换算为什么不能直接乘系数？','因为摄氏与华氏零点不同，存在 +32 偏移，公式已自动处理。'),('换算结果有误差吗？','使用标准换算系数，仅受显示精度影响，无实质误差。')]
 },
 {
  'slug':'mortgage-calculator','tool':'tools/finance/mortgage-calculator.html','name':'房贷计算器',
  'desc':'房贷计算器使用指南：等额本息/等额本金月供、总利息与还款计划测算。',
  'intro':'买房是家庭最大宗支出之一。ToolBox 房贷计算器在本地帮你测算月供、总利息与还款总额，支持等额本息与等额本金两种还款方式对比。',
  'features':['支持等额本息与等额本金两种算法','输入贷款总额、年利率、年限即得月供','输出总利息、还款总额','可对比两种方式的总成本差异','不依赖联网，数据本地计算'],
  'scenarios':['购房前估算月供是否在家庭承受范围内','比较等额本息与等额本金哪个更省利息','评估提前还款的潜在收益','不同首付比例下的月供试算'],
  'steps':['输入贷款本金（如 100 万）','填写年利率（如 3.95%）与贷款年限（如 30 年）','选择还款方式','点击计算，查看月供、总利息、总额','切换另一种方式对比总成本'],
  'tips':['等额本金前期月供高但总利息更少，适合前期还款能力强的人','利率用"年利率"，别误填月利率','实际月供还含物业/税费等，计算器仅算贷款本息','关注 LPR 变动对浮动利率的影响'],
  'faqs':[('等额本息和等额本金怎么选？','想月供稳定选等额本息；想省总利息且前期能多还选等额本金。'),('计算器结果和银行一致吗？','算法一致；差异通常来自利率取值、尾差舍入与附加费用。')]
 },
 {
  'slug':'bmi-calculator','tool':'tools/health/bmi-calculator.html','name':'BMI 计算器',
  'desc':'BMI 计算器使用指南：身高体重测算身体质量指数，判断体重健康区间。',
  'intro':'BMI（身体质量指数）是评估体重是否健康的最常用指标。ToolBox BMI 计算器在本地根据身高体重给出 BMI 值与所属区间（偏瘦/正常/超重/肥胖）。',
  'features':['输入身高(cm)与体重(kg)即得 BMI','自动标注所属健康区间','显示标准体重参考范围','适配成人，计算瞬时完成','纯本地，无需联网'],
  'scenarios':['日常健康监测，了解体重趋势','健身前后对比 BMI 变化','体检报告辅助解读','制定减重/增重目标的起点'],
  'steps':['输入身高（厘米）','输入体重（公斤）','点击计算，得到 BMI 数值','对照区间判断偏瘦/正常/超重/肥胖','结合腰围等指标综合评估'],
  'tips':['BMI 不区分肌肉与脂肪，健身人群（肌肉多）可能偏高但健康','孕妇、未成年人、老年群体需结合专业评估','BMI 正常也建议保持运动与均衡饮食','关注长期趋势而非单次数值'],
  'faqs':[('BMI 正常就一定健康吗？','不一定，它忽略了体脂分布与肌肉量，需结合腰围等指标。'),('为什么健身的人 BMI 偏高？','因为肌肉密度大于脂肪，BMI 把肌肉也当作"重"，属误判。')]
 },
 {
  'slug':'regex-tester','tool':'tools/it/regex-tester.html','name':'正则表达式测试',
  'desc':'正则表达式测试使用指南：在线调试正则，实时高亮匹配、分组与替换。',
  'intro':'正则表达式是文本处理的瑞士军刀，但语法易错。ToolBox 正则测试在本地帮你实时调试表达式，高亮所有匹配、捕获分组，并支持替换预览。',
  'features':['实时匹配高亮，输入即更新','显示每个匹配的捕获分组','支持 g/i/m/s 等常用修饰符','替换模式：预览替换结果','解释常见错误，辅助排错'],
  'scenarios':['从日志/文本中提取邮箱、手机号、URL','表单输入格式校验（如身份证、邮编）','批量重命名、查找替换','清洗数据时按规则筛选行'],
  'steps':['在"正则表达式"框输入模式，如 \\d+','在"测试文本"框粘贴待匹配内容','开启需要的修饰符（如 g 全局、i 忽略大小写）','查看高亮与分组结果，调整表达式','需要替换时切换到替换模式预览'],
  'tips':['先写最小可匹配再逐步加约束，避免一步到位出错','注意 . 默认不匹配换行，多行用 s 修饰符','中文匹配可用 [] 区间或 \\p{...}（依赖引擎）','贪婪/非贪婪(*? +?)的选择常决定匹配长度'],
  'faqs':[('为什么只匹配到第一个？','未开启全局 g 修饰符时默认只返回首个匹配。'),('如何匹配中文？','可用字符区间 [一-鿿] 或具体的 Unicode 属性，视引擎支持而定。')]
 },
 {
  'slug':'color-picker','tool':'tools/design/color-picker.html','name':'颜色选择器',
  'desc':'颜色选择器使用指南：取色、调色与 HEX/RGB/HSL 互转，设计配色必备。',
  'intro':'无论是写 CSS 还是做设计稿，准确的颜色值都至关重要。ToolBox 颜色选择器在本地帮你取色、微调，并实时互转 HEX / RGB / HSL 多种格式。',
  'features':['可视化调色板，拖动即时取色','HEX / RGB / HSL 三种格式实时互转','显示对比文字色（黑/白）建议','支持复制任意格式','可输入颜色值反向定位'],
  'scenarios':['前端开发写 CSS 颜色值','根据品牌色推导相近色','对比前景/背景可读性','从图片吸色后转成代码可用值'],
  'steps':['在调色板拖动选择目标颜色','查看同步生成的 HEX/RGB/HSL','复制需要的格式到代码','输入某个已知色值可反向定位到面板','用对比色提示确认文字可读性'],
  'tips':['同一颜色在不同屏幕有偏差，重要品牌色以代码值为准','保证可访问性：正文与背景对比度建议 ≥4.5:1','HSL 更适合做明暗/饱和度微调','保存调色板时注意命名一致'],
  'faqs':[('HEX 和 RGB 哪个更好？','本质等价，HEX 更紧凑、RGB 更直观，按需选择。'),('怎么保证文字可读？','用工具提供的对比色建议，确保前景背景对比度足够。')]
 },
 {
  'slug':'markdown-to-html','tool':'tools/it/markdown-to-html.html','name':'Markdown 转 HTML',
  'desc':'Markdown 转 HTML 使用指南：把 Markdown 文档实时渲染为 HTML，便于发布。',
  'intro':'Markdown 是写作与文档的主流轻量标记语言。ToolBox Markdown 转 HTML 工具在本地把 .md 文本实时渲染为 HTML 片段，方便粘贴进网页或富文本编辑器。',
  'features':['实时渲染：左边写 Markdown，右边出 HTML','支持标题、列表、表格、代码块、引用等常用语法','输出干净 HTML 片段，可直接使用','一键复制结果','支持导出'],
  'scenarios':['把笔记/文档转成网页可发布的 HTML','撰写 README、博客草稿','在 CMS 中粘贴结构化内容','教学/报告中快速排版'],
  'steps':['在左侧粘贴或输入 Markdown 文本','右侧实时显示渲染后的 HTML','如需 HTML 源码，切换到源码视图并复制','检查表格、代码块等是否如预期','粘贴到目标编辑器时注意清理多余样式'],
  'tips':['复杂表格、脚注等高级语法不同引擎支持不一，渲染后请复核','生成的 HTML 可能带默认标签，建议再加一层 CSS 约束','避免直接渲染不可信内容以防 XSS（本工具本地运行仍需注意下游使用）'],
  'faqs':[('渲染结果能直接上线吗？','可以，但建议套用站点 CSS 以保证样式统一。'),('为什么有些语法没生效？','可能属扩展语法，标准 Markdown 未涵盖，需确认引擎支持。')]
 },
 {
  'slug':'age-calculator','tool':'tools/life/age-calculator.html','name':'年龄计算器',
  'desc':'年龄计算器使用指南：根据出生日期精确计算周岁、天数与下次生日。',
  'intro':'想知道自己精确活了多少天，或距离某个纪念日还有多久？ToolBox 年龄计算器在本地根据出生日期算出精确年龄、总天数与下次生日倒计时。',
  'features':['输入出生日期即得精确周岁','显示累计天数、月数等','计算距离下次生日的天数','支持任意两个日期的差值','瞬时计算，纯本地'],
  'scenarios':['填写表单时确认周岁','计算宝宝出生至今的天数','纪念日、保费、合同期限推算','健康管理中的年龄节点提醒'],
  'steps':['选择出生日期','点击计算，得到周岁与总天数','查看距离下次生日的倒计时','如需两日期差值，使用日期差模式','复制结果'],
  'tips':['周岁按"未满即减一岁"规则，与虚岁不同','涉及合同/保险以条款约定为准','跨时区日期以当地日历日计算'],
  'faqs':[('周岁和虚岁有什么区别？','周岁按生日是否过了算，虚岁出生即算一岁，常大 1-2 岁。'),('年龄计算准吗？','基于公历日期精确计算，结果可靠。')]
 },
 {
  'slug':'compound-interest','tool':'tools/finance/compound-interest.html','name':'复利计算器',
  'desc':'复利计算器使用指南：测算本金按复利增长的未来价值与累计利息。',
  'intro':'复利被称为"世界第八大奇迹"。ToolBox 复利计算器在本地帮你测算一笔本金在定期计息、定投下的未来价值，看清时间与利率的威力。',
  'features':['单笔本金复利未来值计算','支持每月/每年定投（年金）','可调年化利率与计息频次','输出本金、利息、总额明细','图表化展示增长曲线'],
  'scenarios':['规划储蓄与理财目标','比较不同利率/期限下的收益','教育金、养老金长期测算','理解"尽早开始"的复利效应'],
  'steps':['输入初始本金','填写年化收益率与年限','选择是否定投及金额/频率','点击计算，查看未来值与利息','用曲线观察增长加速点'],
  'tips':['时间是复利最大变量，越早开始收益越显著','注意"年化"与"实际到手"的差异，税费会侵蚀收益','高收益常伴高风险，计算器不含波动'],
  'faqs':[('复利和单利差在哪？','单利只对本金计息，复利对"本金+已生利息"再计息，长期差距巨大。'),('定投和单笔哪个好？','定投平摊时点风险，适合工资结余；单笔适合已有本金。')]
 },
 {
  'slug':'color-converter','tool':'tools/it/color-converter.html','name':'颜色转换',
  'desc':'颜色转换使用指南：HEX/RGB/HSL/CMYK 多格式互转，设计开发通用。',
  'intro':'不同场景使用不同颜色模型：网页用 HEX/RGB，印刷用 CMYK。ToolBox 颜色转换在本地实现多格式互转，省去手动换算。',
  'features':['HEX / RGB / HSL / CMYK 多向互转','输入任一格式自动填充其余','实时预览色块','一键复制目标格式','支持带透明度的 RGBA'],
  'scenarios':['网页色转印刷 CMYK 核对','设计稿色值转代码','批量统一团队颜色格式','还原截图里的颜色'],
  'steps':['在任一输入框填入颜色值（如 #3366CC）','其余格式自动同步','点击复制所需格式','如需透明，使用 RGBA 模式','核对预览色块'],
  'tips':['CMYK 是减色模型，转回 RGB 可能有轻微色差，印刷以打样为准','HSL 调明暗比 RGB 更直观','保存品牌色时固定一种格式避免歧义'],
  'faqs':[('CMYK 转 RGB 为什么有色差？','两者色彩空间不同，转换是近似映射。'),('透明度怎么表示？','用 RGBA 的 A 通道(0-1)或 HEX 8 位(#RRGGBBAA)。')]
 },
 {
  'slug':'body-fat-calculator','tool':'tools/health/body-fat-calculator.html','name':'体脂率计算器',
  'desc':'体脂率计算器使用指南：用围度/身高体重估算体脂率，评估身体成分。',
  'intro':'体脂率比体重更能反映身材健康。ToolBox 体脂率计算器在本地用常用公式（如海军法）根据身高、体重、腰围等估算体脂率，并给出健康区间参考。',
  'features':['输入身高、体重、腰围等围度估算体脂','分性别采用不同公式','显示体脂健康区间参考','结果附带解读建议','纯本地计算'],
  'scenarios':['健身减脂期跟踪身体成分变化','体检数据自我解读','制定训练/饮食目标','比 BMI 更细化的健康评估'],
  'steps':['选择性别','输入身高、体重、腰围（部分公式需颈围/臀围）','点击计算，得到估算体脂率','对照健康区间判断','结合运动与饮食改善'],
  'tips':['公式是估算，存在个体误差，宜看趋势而非绝对数','围度测量需固定部位与方法才可比','体脂过低或过高都不健康，关注合理区间'],
  'faqs':[('体脂率和 BMI 哪个准？','体脂率更反映身体成分，BMI 只看体重身高比。'),('为什么男女公式不同？','男女脂肪分布不同，公式需分性别以提高准确度。')]
 },
 {
  'slug':'percentage-calculator','tool':'tools/life/percentage-calculator.html','name':'百分比计算器',
  'desc':'百分比计算器使用指南：百分比增减、占比、折扣与比例快速计算。',
  'intro':'折扣、涨幅、占比……百分比无处不在。ToolBox 百分比计算器在本地帮你快速算增减幅度、某数占另一数的比例、以及打折后的价格。',
  'features':['计算 A 占 B 的百分比','求数值增减百分比','折扣/涨价后价格','按比例分配','瞬时出结果'],
  'scenarios':['购物算折后价与省了多少','业绩同比/环比涨幅','报表中占比分析','小费、税率快速估算'],
  'steps':['选择计算类型（占比/增减/折扣）','填入对应数值','点击计算，得到百分比或结果值','复核口径（基数是谁）','复制结果'],
  'tips':['"增长了 50%"的基数不同结果不同，务必确认基准','折扣 20% 即乘以 0.8，别误减 20 元','同比用上年同期、环比用上一周期，别混用'],
  'faqs':[('20% off 怎么算？','原价 ×(1-0.2)=0.8 倍，即打八折。'),('占比和增长率一样吗？','不一样：占比是部分/整体，增长率是变化量/原值。')]
 },
 {
  'slug':'case-converter','tool':'tools/it/case-converter.html','name':'大小写转换',
  'desc':'大小写转换使用指南：驼峰、下划线、连字符、全大写等命名风格互转。',
  'intro':'变量命名风格五花八门（camelCase、snake_case、kebab-case…）。ToolBox 大小写转换在本地一键互转，程序员与写作者都常用。',
  'features':['支持 camelCase / PascalCase / snake_case / kebab-case / 全大写/全小写','批量转换整段文本','保留单词边界，智能分词','一键复制','处理空格与标点边界'],
  'scenarios':['代码重构时统一变量命名风格','把文案转成标题大小写','生成 URL slug(连字符)','数据库字段与代码变量名对齐'],
  'steps':['粘贴或输入待转换文本','选择目标风格（如 snake_case）','实时得到转换结果','检查分词是否正确（尤其缩写）','复制使用'],
  'tips':['连续大写缩写(如 "HTTP")在 camelCase 中常被误拆，转换后请复核','中文混排时以空格/标点作为分词边界','kebab-case 常用于 URL，snake_case 常用于数据库'],
  'faqs':[('驼峰和帕斯卡有什么区别？','camelCase 首字母小写，PascalCase 首字母大写，常用于不同语言约定。'),('为什么分词错了？','工具按空格/标点/大小写切换分词，异常缩写可能误判。')]
 },
 {
  'slug':'countdown-timer','tool':'tools/life/countdown-timer.html','name':'倒计时',
  'desc':'倒计时使用指南：设定目标时间，实时显示剩余天/时/分/秒。',
  'intro':'重要日子值得期待。ToolBox 倒计时在本地帮你设定任意目标时间，实时显示距离它的剩余天数、小时、分钟与秒。',
  'features':['设定目标日期与时间','实时刷新剩余时间','支持活动、节日、截止日等','界面简洁，无需登录','纯本地运行'],
  'scenarios':['高考、考研、考试倒计时','产品发布、活动开幕倒计时','项目截止日提醒','个人目标（如戒断、挑战）'],
  'steps':['选择或输入目标日期与时间','点击开始，页面显示剩余时间','可最小化做别的事，回来仍计时','到临近时关注秒级变化','分享目标可截图'],
  'tips':['以本地时区计时，跨时区活动注意对齐','重要截止日前设多重提醒，不只依赖网页','关闭页面后计时停止，长期提醒请用日历'],
  'faqs':[('关掉页面倒计时还在吗？','本地计时随页面存在，关闭即停止；长期提醒请用系统日历。'),('时间不准怎么办？','以设备系统时间为准，校准系统时钟即可。')]
 },
 {
  'slug':'date-diff','tool':'tools/misc/date-diff.html','name':'日期差计算',
  'desc':'日期差计算使用指南：计算两个日期之间相隔的天数、月数与工作日的工具。',
  'intro':'"这个项目还有多少天？""两次发薪间隔几周？"ToolBox 日期差计算在本地帮你精确算出两个日期之间的天数、周数，并可选排除周末。',
  'features':['两个日期相隔天数/周数','可选仅算工作日（去除周末）','支持跨年、跨月计算','显示起止信息','瞬时出结果'],
  'scenarios':['项目周期、租期天数核算','薪资/账单周期统计','工期排期与里程碑','合同期限的精确天数'],
  'steps':['选择开始日期与结束日期','点击计算，得到相隔天数','如需工作日，勾选"仅工作日"','查看周数等衍生结果','复制结果到排期表'],
  'tips':['"包含首尾"与否会影响天数，按业务口径选择','工作日模式默认去周末，不含法定节假日','跨时区日期以当地日历日计算'],
  'faqs':[('天数包含开始那天吗？','通常按"结束-开始"的自然日差，是否含端点看具体设置。'),('法定节假日算工作日吗？','本工具工作日模式仅去周末，不含节假日调整。')]
 },
 {
  'slug':'url-encode','tool':'tools/it/url-encode.html','name':'URL 编码',
  'desc':'URL 编码使用指南：URL 编码/解码，处理中文、空格与特殊字符。',
  'intro':'URL 只允许部分安全字符，中文、空格、& 等需编码。ToolBox URL 编码在本地帮你对网址或参数做编码/解码，避免请求出错。',
  'features':['URL 编码与解码双向','处理中文、空格、特殊字符','保留常见安全字符 unchanged','支持整段或参数片段','一键复制'],
  'scenarios':['把中文关键词拼进查询参数','构造含特殊字符的下载链接','调试接口 400/乱码问题','表单 GET 参数预处理'],
  'steps':['选择编码或解码','粘贴待处理文本','点击转换，得到结果','核对编码后是否可被正常解析','复制用于链接或请求'],
  'tips':['空格在 URL 中常编码为 %20 或 +，按场景选择','仅编码参数值，别把整个协议/域名编码了','解码前确认是标准编码，避免双重编码'],
  'faqs':[('为什么中文会变成 %E4%BD%A0？','那是 UTF-8 字节的百分号编码，浏览器/服务器会自动还原。'),('编码后链接打不开？','可能编码了不该编码的部分（如 :// 或 /），只编码参数值即可。')]
 },
 {
  'slug':'md5','tool':'tools/it/md5.html','name':'MD5 计算',
  'desc':'MD5 计算使用指南：本地生成文本/文件的 MD5 摘要，用于校验与去重。',
  'intro':'MD5 是常用的哈希算法，可把任意数据生成固定长度的摘要，常用于完整性校验。ToolBox MD5 工具在本地计算文本或文件的 MD5，不联网、不上传。',
  'features':['文本与文件均支持','生成 32 位十六进制 MD5 摘要','大文件流式计算，避免卡顿','一键复制结果','纯本地，数据不上传'],
  'scenarios':['下载文件后校验完整性（比对官方 MD5）','检测两份文件是否一致','去重与快速指纹','调试接口签名中的摘要'],
  'steps':['粘贴文本或选择文件','点击计算，得到 MD5 值','与官方/对方提供的摘要比对','一致则说明内容未被篡改','复制结果记录'],
  'tips':['MD5 已被证明不安全，切勿用于密码存储或签名防篡改','它适合"完整性校验"而非"安全防护"','大文件校验以官方提供的哈希为准'],
  'faqs':[('MD5 能用来存密码吗？','不能。MD5 已不安全，密码应使用慢哈希(如 bcrypt)。'),('为什么文件 MD5 对不上？','内容有任一字节差异摘要就不同，确认来源一致再比对。')]
 },
]

TPL = '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}使用指南 - ToolBox</title>
<meta name="description" content="{desc}">
<meta property="og:title" content="{title}使用指南 - ToolBox">
<meta property="og:type" content="article">
<meta property="og:site_name" content="ToolBox">
<meta property="og:url" content="{canonical}">
<link rel="canonical" href="{canonical}">
<script type="application/ld+json">
{{"@context":"https://schema.org","@type":"Article","headline":"{title}使用指南","description":"{desc}","author":{{"@type":"Organization","name":"ToolBox"}}}}
</script>
<style>
:root{{--primary:#FF6B35;--text:#1F2937;--muted:#6B7280;--border:#E5E7EB;--bg:#FFFAF7;}}
*{{box-sizing:border-box;}}
body{{margin:0;font-family:"Noto Sans SC","Plus Jakarta Sans",system-ui,sans-serif;color:var(--text);background:var(--bg);line-height:1.75;}}
header{{padding:18px 20px;border-bottom:1px solid var(--border);background:#fff;}}
.breadcrumb a{{color:var(--primary);text-decoration:none;margin-right:6px;}}
.breadcrumb a:hover{{text-decoration:underline;}}
main{{max-width:780px;margin:0 auto;padding:28px 20px 60px;}}
h1{{font-size:28px;margin:0 0 8px;}}
.lead{{font-size:16px;color:var(--muted);margin:0 0 22px;}}
h2{{font-size:20px;margin:28px 0 10px;color:var(--primary);}}
ul,ol{{padding-left:22px;}}
li{{margin:6px 0;}}
dl{{margin:0;}}
dt{{font-weight:700;margin-top:12px;}}
dd{{margin:4px 0 0;color:var(--muted);}}
.back{{margin-top:30px;padding:16px;background:#fff;border:1px solid var(--border);border-radius:14px;}}
.back a{{color:var(--primary);font-weight:700;text-decoration:none;}}
footer{{text-align:center;color:var(--muted);font-size:13px;padding:24px;border-top:1px solid var(--border);}}
</style>
</head>
<body>
<header><nav class="breadcrumb"><a href="{home}">ToolBox</a> / <a href="{home}#guides">使用指南</a> / <span>{title}</span></nav></header>
<main>
<h1>{title} 使用指南</h1>
<p class="lead">{intro}</p>
<h2>核心功能</h2>
<ul>{features}</ul>
<h2>适用场景</h2>
<ul>{scenarios}</ul>
<h2>使用步骤</h2>
<ol>{steps}</ol>
<h2>实用技巧</h2>
<ul>{tips}</ul>
<h2>常见问题</h2>
<dl>{faqs}</dl>
<p class="back"><a href="{tool_url}">→ 打开「{title}」工具立即使用</a></p>
</main>
<footer>© ToolBox · 5000+ 免费在线工具，纯前端运行，数据不上传</footer>
</body>
</html>'''

def li(items): return ''.join(f'<li>{html.escape(str(x))}</li>' for x in items)
def faq(items): return ''.join(f'<dt>{html.escape(q)}</dt><dd>{html.escape(a)}</dd>' for q,a in items)

def render(g):
    tool_url = SITE + '/' + g['tool']
    canonical = SITE + '/guides/' + g['slug'] + '-guide.html'
    return TPL.format(
        title=g['name'], desc=g['desc'], canonical=canonical,
        home=SITE + '/', tool_url=tool_url,
        intro=g['intro'],
        features=li(g['features']),
        scenarios=li(g['scenarios']),
        steps=li(g['steps']),
        tips=li(g['tips']),
        faqs=faq(g['faqs']),
    )

def render_index(items):
    cards = ''.join(
        f'<li><a href="{SITE}/guides/{g["slug"]}-guide.html">{html.escape(g["name"])}使用指南</a>'
        f'<span style="color:var(--muted);font-size:13px;"> — {html.escape(g["desc"])}</span></li>'
        for g in items
    )
    return f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>工具使用指南中心 - ToolBox</title>
<meta name="description" content="ToolBox 高频工具使用指南：场景、步骤、技巧与常见问题，帮你把每个工具用得更顺手。">
<meta property="og:title" content="工具使用指南中心 - ToolBox">
<meta property="og:type" content="website">
<meta property="og:site_name" content="ToolBox">
<link rel="canonical" href="{SITE}/guides/index.html">
<style>
:root{{--primary:#FF6B35;--text:#1F2937;--muted:#6B7280;--border:#E5E7EB;--bg:#FFFAF7;}}
*{{box-sizing:border-box;}}
body{{margin:0;font-family:"Noto Sans SC","Plus Jakarta Sans",system-ui,sans-serif;color:var(--text);background:var(--bg);line-height:1.8;}}
header{{padding:18px 20px;border-bottom:1px solid var(--border);background:#fff;}}
.breadcrumb a{{color:var(--primary);text-decoration:none;}}
main{{max-width:820px;margin:0 auto;padding:28px 20px 60px;}}
h1{{font-size:28px;}}
ul{{padding-left:22px;}}
li{{margin:12px 0;}}
li a{{color:var(--primary);font-weight:700;text-decoration:none;font-size:16px;}}
footer{{text-align:center;color:var(--muted);font-size:13px;padding:24px;border-top:1px solid var(--border);}}
</style>
</head>
<body>
<header><nav class="breadcrumb"><a href="{SITE}/">ToolBox</a> / <span>使用指南</span></nav></header>
<main>
<h1>工具使用指南中心</h1>
<p style="color:var(--muted);">精选高频工具的实用指南，涵盖核心功能、适用场景、使用步骤、实用技巧与常见问题。</p>
<ul>{cards}</ul>
</main>
<footer>© ToolBox · 5000+ 免费在线工具，纯前端运行，数据不上传</footer>
</body>
</html>'''

def main():
    map_entries = []
    for g in GUIDES:
        out = render(g)
        path = os.path.join(GUIDES_DIR, g['slug'] + '-guide.html')
        with open(path, 'w', encoding='utf-8') as f:
            f.write(out)
        tool_base = os.path.basename(g['tool'])
        map_entries.append({
            'tool': tool_base,
            'guide': '../../guides/' + g['slug'] + '-guide.html',
            'title': g['name'] + '使用指南',
        })
    # 指南中心
    with open(os.path.join(GUIDES_DIR, 'index.html'), 'w', encoding='utf-8') as f:
        f.write(render_index(GUIDES))
    # 工具页自动链接映射
    os.makedirs(JSON_DIR, exist_ok=True)
    with open(os.path.join(JSON_DIR, 'guides.json'), 'w', encoding='utf-8') as f:
        json.dump(map_entries, f, ensure_ascii=False, indent=2)
    print('Generated', len(GUIDES), 'guides + index + guides.json')

if __name__ == '__main__':
    main()
