#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
热门页精修（clarity_top_pages_3d.txt 驱动）· 针对具体工具写真实领域知识面板（幂等）

基线：126 个线上 72h 真实热页中，60 个为工具页且已全部 A 级，但其中 29 个
      fb=False（无「📐 工作原理与说明」面板，靠自身代码量/输入项达标已是 A）。
      本脚本逐个为这 29 个工具页注入**针对性、真实**的 formula-box 面板
      （含该工具的工作原理、关键公式、参考数值、适用注意），非通用 cat 模板。

幂等：已含 `TOOLBOX-POLISH` 哨兵则跳过；注入位置同 enhance_b_a（</h2> 后）。
跳过：磁盘不存在的页面（线上历史访问、已删除/迁移，共 7 个）由调用方预筛。

用法：
  python3 scripts/polish_hot_pages.py --dry-run
  python3 scripts/polish_hot_pages.py --only hvac/duct-calculator.html
  python3 scripts/polish_hot_pages.py
"""
import json, re, os, sys, argparse

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
JSON_PATH = os.path.join(ROOT, 'json', 'tools.json')
SENTINEL = 'TOOLBOX-POLISH'

# (ind, file) -> 针对性真实领域知识 HTML 片段（formula-box 内容）
POLISH = {
    ('hvac', 'duct-calculator.html'): """
<div class="formula-box">
  <div class="formula-title">📐 工作原理与说明</div>
  <p class="formula-desc">风管计算基于风量守恒与沿程/局部阻力。风速 <b>v = Q ÷ (3600 × A)</b>（Q 为风量 m³/h，A 为截面积 m²）；矩形管 A=宽×高，圆形管 A=πD²/4。沿程阻力按达西-魏斯巴赫 <b>Δp_f = λ·(L/D_h)·(ρv²/2)</b>，λ 由雷诺数经 Colebrook 方程求得；局部阻力 <b>Δp_j = Σζ·(ρv²/2)</b>。系统总阻力为二者之和。</p>
  <ul class="formula-list">
    <li>低速风管推荐风速：主风管 6–8 m/s、支管 3–5 m/s，兼顾噪声与能耗。</li>
    <li>水力直径 D_h = 4A / 周长，矩形管阻力高于同截面圆管。</li>
    <li>纯前端计算，数据不上传；结果供方案比选，最终以暖通设计手册为准。</li>
  </ul>
</div>
""",
    ('paper', 'strength-1.html'): """
<div class="formula-box">
  <div class="formula-title">📐 工作原理与说明</div>
  <p class="formula-desc">瓦楞纸箱抗压（BCT）按 McKee（马基）经验式估算：<b>BCT ≈ 5.87 × ECT^0.73 × (T × Z)^0.5</b>，其中 ECT 为纸板边压强度（N/150mm），T 为纸板厚度（mm），Z 为纸箱周长（mm）。ECT 由各层原纸环压强度 Rct 叠加（含瓦楞率与芯纸贡献）求得。</p>
  <ul class="formula-list">
    <li>瓦楞类型影响：A 楞 ECT 高、E 楞平整；BCT 还随堆码高度、温湿度下降。</li>
    <li>安全系数通常取 3–5（仓储/运输/湿度条件越差越大）。</li>
    <li>结果仅供参考，正式包装设计以 GB/T 6543 与实测抗压为准。</li>
  </ul>
</div>
""",
    ('edu', 'reading-speed-calculator.html'): """
<div class="formula-box">
  <div class="formula-title">📐 工作原理与说明</div>
  <p class="formula-desc">阅读速度 = 阅读总量 ÷ 阅读时长。<b>英文约按词（WPM = 词数 ÷ 分钟）</b>；<b>中文常按字/分钟</b>（或按 100 字 ≈ 1 分钟基准折算）。理解率 = 答对题数 ÷ 总题数，用于校正“快而不懂”。</p>
  <ul class="formula-list">
    <li>成人中文正常阅读约 300–500 字/分钟，熟练速读可超 1000 字/分钟。</li>
    <li>理解率低于 70% 时，速度数据参考价值低，应降速精读。</li>
    <li>本工具纯本地计算，用于自我训练追踪，非标准化测评。</li>
  </ul>
</div>
""",
    ('food-testing', 'colony-count.html'): """
<div class="formula-box">
  <div class="formula-title">📐 工作原理与说明</div>
  <p class="formula-desc">按 GB 4789.2 平板计数法：样品稀释后倾注培养（36±1℃、48±1h），选取菌落数在 <b>30–300 CFU</b> 的平板计数，乘以稀释倍数得结果。<b>菌落总数 = 同一稀释度平行平板平均菌落数 × 稀释倍数</b>，单位 CFU/g（或 CFU/mL）。</p>
  <ul class="formula-list">
    <li>所有平板均＜30 取最低稀释度估算；均＞300 取最高稀释度报告。</li>
    <li>菌落蔓延、片状生长按标准规则折算或重做。</li>
    <li>结果为卫生指示菌，不代表致病菌，判定以产品标准限量为准。</li>
  </ul>
</div>
""",
    ('rubber', 'mixing-ratio.html'): """
<div class="formula-box">
  <div class="formula-title">📐 工作原理与说明</div>
  <p class="formula-desc">橡胶配方以 <b>phr（每百份橡胶份数）</b> 为基准。某组分实际质量 = 总混炼质量 ×（该组分 phr ÷ 总 phr）。生胶固定为 100 phr，硫化剂、填料、助剂按 phr 累加得到总 phr，再按目标总重反算各料质量。</p>
  <ul class="formula-list">
    <li>质量分数(%) = 组分 phr ÷ 总 phr × 100%。</li>
    <li>密度差异大时注意体积分数与质量分数不同，工艺上常以质量投料。</li>
    <li>结果供配料参考，实际以工艺试炼与物性检测为准。</li>
  </ul>
</div>
""",
    ('it', 'emoji-picker.html'): """
<div class="formula-box">
  <div class="formula-title">📐 工作原理与说明</div>
  <p class="formula-desc">内置 Unicode Emoji 数据集（含 CLDR 分组与多语言关键词），前端按关键词或分类实时过滤，点击即复制 Emoji 字符或其码点（如 U+1F600）。复杂 Emoji 可由 <b>ZWJ（零宽连接符 U+200D）</b> 序列组合（如家庭、职业组合）。</p>
  <ul class="formula-list">
    <li>数据随 Unicode 版本更新（15.x 已超 3000 个 Emoji）。</li>
    <li>纯前端本地检索，不上传；复制结果依赖系统字体回退渲染。</li>
  </ul>
</div>
""",
    ('general', 'lifespan-26.html'): """
<div class="formula-box">
  <div class="formula-title">📐 工作原理与说明</div>
  <p class="formula-desc">高温蠕变断裂寿命用 Larson-Miller 参数法外推：<b>LMP = T_K × (log₁₀ t_r + C)</b>，T_K 为绝对温度（K），t_r 为断裂时间（h），常数 C 常取 20。已知某应力下的 LMP，可在其他温度估算寿命，或反查许用应力。</p>
  <ul class="formula-list">
    <li>参数曲线来自材料持久强度试验（如主曲线法）。</li>
    <li>结果对高温管道、透平件设计有参考价值，须以材料厂数据为准。</li>
    <li>纯前端计算，不作结构设计依据。</li>
  </ul>
</div>
""",
    ('it', 'yaml-validator.html'): """
<div class="formula-box">
  <div class="formula-title">📐 工作原理与说明</div>
  <p class="formula-desc">基于 YAML 解析引擎（js-yaml）做语法校验。YAML 以<b>缩进（推荐 2 空格）表示层级</b>，键值用 <b>key: value</b>，列表项以 <b>- </b> 开头，禁止用 Tab 缩进；解析失败时在报错位置附近高亮提示。</p>
  <ul class="formula-list">
    <li>常见错误：冒号后缺空格、混用 Tab/空格、字符串含特殊字符未加引号。</li>
    <li>遵循 YAML 1.1/1.2 规范；纯前端运行，文件不离开浏览器。</li>
  </ul>
</div>
""",
    ('agriculture', 'pesticide-dose.html'): """
<div class="formula-box">
  <div class="formula-title">📐 工作原理与说明</div>
  <p class="formula-desc">按标签推荐浓度换算实际用药量。<b>原药体积 = 目标药液总量 ÷ 稀释倍数</b>；或 <b>用药量 = 面积 × 单位面积推荐量</b>（如 mL/亩、g/亩）。已给水量时：原药量 = 水量 × 推荐浓度比。</p>
  <ul class="formula-list">
    <li>严格遵守安全间隔期与最大残留限量（MRL），禁止超量。</li>
    <li>折算以登记作物、剂型、有效成分含量为依据。</li>
    <li>结果仅供参考，施药务必核对正式标签与当地植保指导。</li>
  </ul>
</div>
""",
    ('it', 'text-similarity.html'): """
<div class="formula-box">
  <div class="formula-title">📐 工作原理与说明</div>
  <p class="formula-desc">提供多种文本相似度度量：<b>余弦相似度</b>（向量空间，TF 或字符 n-gram，∈[0,1]）；<b>Jaccard</b>（交集÷并集）；<b>Levenshtein 编辑距离</b>（最少插入/删除/替换次数，越小越像）；<b>汉明距离</b>（等长串对应位差异数）。</p>
  <ul class="formula-list">
    <li>中英文均可；短文本建议用字符级 n-gram 或编辑距离。</li>
    <li>余弦=1 表示方向完全一致，编辑距离=0 表示完全相同。</li>
    <li>纯前端计算，数据不上传。</li>
  </ul>
</div>
""",
    ('it', 'usb-version.html'): """
<div class="formula-box">
  <div class="formula-title">📐 工作原理与说明</div>
  <p class="formula-desc">USB 各代速率与供电对照（速查）：USB 2.0 = 480 Mbps；USB 3.0/3.1 Gen1 = 5 Gbps；USB 3.1 Gen2 = 10 Gbps；USB 3.2 = 20 Gbps；USB4 = 40 Gbps（2.0 版达 80 Gbps 单向）。接口形态含 Type-A/B/C。</p>
  <ul class="formula-list">
    <li>供电：USB 2.0 约 0.5A/5V；BC 1.2 达 1.5A；Type-C PD 可达 3A/5A（100W/240W）。</li>
    <li>速率受最慢一端（线材、端口、协议）限制，标示为理论上限。</li>
    <li>纯前端静态速查，具体以 USB-IF 规范与设备规格为准。</li>
  </ul>
</div>
""",
    ('it', 'yaml-to-toml.html'): """
<div class="formula-box">
  <div class="formula-title">📐 工作原理与说明</div>
  <p class="formula-desc">递归将 YAML 结构转为 TOML：映射 → <b>[section]</b> 表（嵌套映射用 <b>[a.b]</b> 点分层级）；列表 → 数组；标量按类型输出（字符串加引号、数字/布尔直出）。YAML 锚点/合并键先展开再转换。</p>
  <ul class="formula-list">
    <li>TOML 不支持 YAML 的任意键顺序语义，表需先于引用出现。</li>
    <li>纯前端转换，数据不离开浏览器；粘贴即转，支持嵌套与注释保留策略。</li>
  </ul>
</div>
""",
    ('nephrology', 'jixingshensunshang-kdigo-fenqi.html'): """
<div class="formula-box">
  <div class="formula-title">📐 工作原理与说明</div>
  <p class="formula-desc">依据 KDIGO 2012 AKI 指南，满足任一即诊断：48h 内血肌酐（Scr）上升 ≥0.3 mg/dL；或 7d 内 Scr 升至基线 1.5 倍以上；或尿量 ＜0.5 mL/kg/h 持续 6h。分期取最重：<b>1 期</b>=Scr 1.5–1.9× 或升≥0.3；<b>2 期</b>=Scr 2.0–2.9×；<b>3 期</b>=Scr ≥3.0× 或 ≥4.0 mg/dL 或尿量＜0.3 持续 24h/无尿 12h。</p>
  <ul class="formula-list">
    <li>无基线 Scr 时用人群估算公式反推（如基于 eGFR）。</li>
    <li>本工具仅供临床参考，不能替代医师判断与实验室复核。</li>
    <li>纯前端计算，数据不上传。</li>
  </ul>
</div>
""",
    ('agriculture', 'irrigation-calculator.html'): """
<div class="formula-box">
  <div class="formula-title">📐 工作原理与说明</div>
  <p class="formula-desc">作物需水量 <b>ETc = ETo × Kc</b>（ETo 参考蒸散，Kc 作物系数）。单次灌水定额 ≈ 土壤有效持水量 × 根层深度 × 计划湿润比 ×（目标含水率上限−下限）；灌水时间 = 灌水量 ÷ 流量。滴灌还需乘发射器流量与数量。</p>
  <ul class="formula-list">
    <li>ETo 常用彭曼（Penman-Monteith）公式估算。</li>
    <li>砂土持水力低需勤灌，黏土可少次多量。</li>
    <li>结果供灌溉计划参考，实际以田间墒情与气象为准。</li>
  </ul>
</div>
""",
    ('it', 'json-formatter.html'): """
<div class="formula-box">
  <div class="formula-title">📐 工作原理与说明</div>
  <p class="formula-desc">将 JSON 文本解析为对象树后重新序列化：美化按 2/4 空格缩进、保留层级；压缩去除空白；校验在解析失败时定位错误行列。支持语法高亮与层级折叠便于阅读。</p>
  <ul class="formula-list">
    <li>合法 JSON 要求双引号键、无尾逗号、无注释（JSON5 才支持）。</li>
    <li>纯前端解析，粘贴内容不离开浏览器，适合脱敏前本地处理。</li>
  </ul>
</div>
""",
    ('it', 'aes-encryptor.html'): """
<div class="formula-box">
  <div class="formula-title">📐 工作原理与说明</div>
  <p class="formula-desc">AES 是对称分组密码：密钥 128/192/256 位，分组固定 16 字节。常见模式：<b>ECB</b>（同明文同密文，不推荐）、<b>CBC</b>（需随机 IV、PKCS7 填充）、<b>GCM</b>（带认证与完整性校验，无需填充）。本工具经浏览器 Web Crypto API 在本地完成，密钥不经网络。</p>
  <ul class="formula-list">
    <li>口令到密钥通常用 PBKDF2/scrypt 派生并加盐，避免弱口令直用。</li>
    <li>GCM 的 IV 须唯一，密文含认证标签防篡改。</li>
    <li>本地加解密仅供您自己数据，密钥请妥善保存（遗失不可恢复）。</li>
  </ul>
</div>
""",
    ('food-processing', 'sterilization-f-value.html'): """
<div class="formula-box">
  <div class="formula-title">📐 工作原理与说明</div>
  <p class="formula-desc">杀菌值基于热力致死动力学：<b>D 值</b>为某温度下杀灭 90% 微生物所需时间；<b>Z 值</b>为使 D 值变化 10 倍所需升温（细菌常取 10℃）；<b>F 值</b>为等效杀菌时间（基准 121.1℃）。积分式 <b>F₀ = Σ 10^((T−121.1)/Z) × Δt</b>。</p>
  <ul class="formula-list">
    <li>商业无菌目标 F₀ 通常 3–12 min（依产品与菌相）。</li>
    <li>Z 取 10℃、D 取 121℃ 参考值；酸性食品（低 pH）要求较低。</li>
    <li>结果供工艺估算，正式杀菌规程以实验与法规为准。</li>
  </ul>
</div>
""",
    ('sales', 'commission-calculator.html'): """
<div class="formula-box">
  <div class="formula-title">📐 工作原理与说明</div>
  <p class="formula-desc">支持四种提成模型：<b>固定比例</b>（销售额×r）；<b>阶梯提成</b>（分段累进，超出阈值部分按高档率）；<b>底薪+提成</b>（底薪叠加）；<b>团队提成</b>（总额按成员占比拆分）。个税按累计预扣法估算。</p>
  <ul class="formula-list">
    <li>阶梯阈值与比率以公司制度为准，注意“超额累进”与“全额累进”差异。</li>
    <li>税前/税后切换影响实发，个税为近似估算非申报依据。</li>
    <li>纯前端计算，数据不上传。</li>
  </ul>
</div>
""",
    ('design', 'css-border-radius.html'): """
<div class="formula-box">
  <div class="formula-title">📐 工作原理与说明</div>
  <p class="formula-desc">CSS <b>border-radius</b> 可为四角分别设圆角：按顺序 左上/右上/右下/左下（斜杠后可分别设水平/垂直半径实现椭圆角）。值用 px 或 %（% 相对盒宽高）。生成代码实时驱动预览。</p>
  <ul class="formula-list">
    <li>单值=四角同；两值=对角；三值=左上+右上左下+右下。</li>
    <li>椭圆角（/ 后值）可做“胶囊”“叶子”等形状。</li>
    <li>纯前端生成，复制即用。</li>
  </ul>
</div>
""",
    ('fun', 'chinese-address-generator.html'): """
<div class="formula-box">
  <div class="formula-title">📐 工作原理与说明</div>
  <p class="formula-desc">按行政区划层级（省 → 市 → 区/县 → 街道 → 门牌）随机组合生成可读的中国大陆邮寄地址；可控制生成数量与详细程度（到市/到街道/到门牌）。数据为本地面向演示的样例集合。</p>
  <ul class="formula-list">
    <li>生成内容为虚构测试数据，非真实地址，请勿用于寄递。</li>
    <li>纯前端随机，不联网、不上传。</li>
  </ul>
</div>
""",
    ('it', 'password-generator.html'): """
<div class="formula-box">
  <div class="formula-title">📐 工作原理与说明</div>
  <p class="formula-desc">使用密码学安全随机源（crypto.getRandomValues）生成，可配长度与字符集（大小写字母、数字、符号）。密码强度用信息熵衡量：<b>熵(bit) = 长度 × log₂(字符池大小)</b>。</p>
  <ul class="formula-list">
    <li>建议长度 ≥12、熵 ≥80 bit；含符号可显著提升抗暴力破解。</li>
    <li>避免词典词与个人信息；生成后妥善保存，前端不留存。</li>
    <li>纯浏览器生成，不离开本地。</li>
  </ul>
</div>
""",
    ('it', 'url-encode.html'): """
<div class="formula-box">
  <div class="formula-title">📐 工作原理与说明</div>
  <p class="formula-desc">按 RFC 3986 做百分号编码（percent-encoding）：非保留字符（字母数字 - _ . ~）不编码，其余转成 <b>%XX</b>（UTF-8 多字节逐字节，如中文“中”→ %E4%B8%AD）。Encode 用于放入 URL，Decode 反向还原。</p>
  <ul class="formula-list">
    <li>encodeURIComponent 编码范围广，适合参数值；encodeURI 保留 / ? # 等结构符。</li>
    <li>纯前端转换，数据不上传。</li>
  </ul>
</div>
""",
    ('video', 'video-speed.html'): """
<div class="formula-box">
  <div class="formula-title">📐 工作原理与说明</div>
  <p class="formula-desc">倍速播放时长 <b>= 原时长 ÷ 倍速</b>（如 60 分钟 ×1.5 倍速 ≈ 40 分钟）。时间码 HH:MM:SS:FF（FF 为帧）与秒可互转；剪辑片段时长 = 出点 − 入点。</p>
  <ul class="formula-list">
    <li>帧率常见 24/25/30 fps，影响时间码与帧精度。</li>
    <li>纯前端计算，数据不上传。</li>
  </ul>
</div>
""",
    ('it', 'markdown-to-html.html'): """
<div class="formula-box">
  <div class="formula-title">📐 工作原理与说明</div>
  <p class="formula-desc">按 CommonMark 规则将 Markdown 解析为 HTML：<b>#</b> 标题、<b>**</b> 粗体、<b>*</b> 斜体、<b>[]()</b> 链接、<b>-</b> 列表、<b>`</b> 行内代码、<b>|</b> 表格等。前端解析器（如 marked）生成带语义标签的 HTML，可实时预览。</p>
  <ul class="formula-list">
    <li>直接插入 DOM 需防 XSS（对不可信输入做消毒/沙箱）。</li>
    <li>纯前端转换，粘贴内容不离开浏览器。</li>
  </ul>
</div>
""",
    ('urban', 'calc-spacing.html'): """
<div class="formula-box">
  <div class="formula-title">📐 工作原理与说明</div>
  <p class="formula-desc">建筑日照间距按太阳高度角估算：正午高度角 <b>h = 90° − |φ − δ|</b>（φ 为纬度，δ 为太阳赤纬；冬至 δ≈−23.44°）。保证后排底楼日照的最小间距 <b>D ≈ H × cot(h) + 间距修正</b>，并给出逐时阴影长度表。</p>
  <ul class="formula-list">
    <li>我国常以大寒日（δ≈−20.15°）或冬至日作日照标准，依气候区而定。</li>
    <li>结果用于方案初算，最终以当地规划日照分析为准。</li>
    <li>纯前端计算，数据不上传。</li>
  </ul>
</div>
""",
    ('general', 'strength-34.html'): """
<div class="formula-box">
  <div class="formula-title">📐 工作原理与说明</div>
  <p class="formula-desc">螺栓强度校核：拉伸应力 <b>σ = F ÷ A_s</b>（A_s 为应力截面积）；许用应力 <b>[σ] = σ_s ÷ 安全系数</b>。剪切 <b>τ = F ÷ (πd²/4 × n)</b>（n 为受剪面数）。强度等级如 8.8 表示 σ_s≈640 MPa、σ_b≈800 MPa（.8×1000）。</p>
  <ul class="formula-list">
    <li>规格 M6–M30 对应不同小径与应力截面积（查 GB/T 3098.1）。</li>
    <li>复合受力按第四强度理论校核等效应力。</li>
    <li>结果供选型参考，重要连接以规范与计算书为准。</li>
  </ul>
</div>
""",
    ('food', 'nutrition-calculator.html'): """
<div class="formula-box">
  <div class="formula-title">📐 工作原理与说明</div>
  <p class="formula-desc">按食材质量与营养成分表估算摄入：<b>某营养素 = 食材质量 ×（每 100g 含量 ÷ 100）</b>。能量按阿特沃特系数 <b>kcal = 4×蛋白 + 4×碳水 + 9×脂肪</b>（膳食纤维常计 2 kcal/g）。</p>
  <ul class="formula-list">
    <li>参考中国居民膳食营养素参考摄入量（DRIs）做对比。</li>
    <li>结果为估算，实际以食物成分表与称量精度为准。</li>
    <li>纯前端计算，数据不上传，不替代膳食建议。</li>
  </ul>
</div>
""",
    ('kids', 'memory-palace.html' ): """
<div class="formula-box">
  <div class="formula-title">📐 工作原理与说明</div>
  <p class="formula-desc">记忆宫殿（Method of Loci）把待记项编码为生动意象，依次“放置”在熟悉的空间路径（房间、路线）上，回忆时沿路径提取。数字常用 <b>00–99 双位编码</b>（每数对应一个形象）转成可挂钩的意象。</p>
  <ul class="formula-list">
    <li>编码越夸张、多感官，提取越牢；路径越熟悉越稳定。</li>
    <li>本工具生成编码表与练习序列，纯本地、不上传。</li>
  </ul>
</div>
""",
    ('edu', 'english-vocabulary.html'): """
<div class="formula-box">
  <div class="formula-title">📐 工作原理与说明</div>
  <p class="formula-desc">从词库（四六级/考研/托福等）随机抽取单词进行拼写或选择测试，按正确率反馈；生词可存入生词本（localStorage）循环复习。前端完成抽题与判分，数据不离开浏览器。</p>
  <ul class="formula-list">
    <li>间隔重复（如按遗忘曲线）比一次性背诵更高效。</li>
    <li>词库为通用样例，备考以官方大纲词汇为准。</li>
  </ul>
</div>
""",
}


def path_of(ind, f):
    cand = os.path.join('tools', ind, f)
    return cand if os.path.exists(cand) else None


def inject(html, frag):
    if SENTINEL in html:
        return None
    m = re.search(r'(</h2>\s*<p style="font-size:13px[^>]*>.*?</p>)', html, re.S)
    if m:
        i = m.end()
    else:
        i = html.find('</h2>')
        if i == -1:
            return None
        i += len('</h2>')
    panel = '\n<!-- %s -->\n%s\n' % (SENTINEL, frag)
    return html[:i] + panel + html[i:]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--dry-run', action='store_true')
    ap.add_argument('--only', default='', help='只处理指定 ind/file，如 hvac/duct-calculator.html')
    args = ap.parse_args()

    done = skipped = failed = 0
    targets = POLISH
    if args.only:
        ind, f = args.only.split('/', 1)
        targets = {(ind, f): POLISH[(ind, f)]} if (ind, f) in POLISH else {}
        if not targets:
            print('NOT IN POLISH:', args.only); return
    for (ind, f), frag in targets.items():
        p = path_of(ind, f)
        if not p:
            print('SKIP(no file) %s/%s' % (ind, f)); skipped += 1; continue
        s = open(p, encoding='utf-8', errors='ignore').read()
        if SENTINEL in s:
            print('SKIP(has) %s/%s' % (ind, f)); skipped += 1; continue
        new = inject(s, frag)
        if new is None:
            print('FAIL(inject) %s/%s' % (ind, f)); failed += 1; continue
        if args.dry_run:
            print('DRY %s/%s len=%d' % (ind, f, len(frag)))
            done += 1; continue
        open(p, 'w', encoding='utf-8').write(new)
        print('OK %s/%s' % (ind, f)); done += 1
    print('=== 完成: 注入 %d | 跳过 %d | 失败 %d ===' % (done, skipped, failed))


if __name__ == '__main__':
    main()
