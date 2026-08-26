#!/usr/bin/env python3
# 升级 clarity 热门页中 24 个"通用 cat 面板"为"针对具体工具的真实面板"
# 幂等:已含 TOOLBOX-POLISH 哨兵则跳过;用 re.sub 整体替换第一个 formula-box 块。
import os, re, sys

ROOT = '/Users/cgw/project/cgw/chenguangwu.github.io'

RAW = {
('urology', 'stone-composition.html'): r'''<h3>📐 工作原理与说明</h3>
<p>本工具依据<strong>红外光谱(IR)定性法</strong>对尿路结石成分进行鉴别。不同成分在红外波段有特征吸收峰,据此判定结石类型,进而指导复发预防与碎石策略。</p>
<ul>
<li><strong>草酸钙</strong>(一水 COM / 二水 COD):最常见,约占 70–80%;特征峰 ~1320 / 780 / 616 cm⁻¹;质地硬、难碎。</li>
<li><strong>磷酸钙</strong>(碳酸磷灰石):~1050 / 950 / 605 cm⁻¹;与碱性尿、甲状旁腺功能相关。</li>
<li><strong>尿酸(UA)</strong>:~1700 / 1400 / 780 cm⁻¹;与高尿酸、酸性尿相关,<strong>可碱化尿液溶解</strong>。</li>
<li><strong>感染石 / 鸟粪石</strong>(六水磷酸铵镁):~1050 / 880 cm⁻¹;需手术取石 + 抗感染。</li>
<li><strong>胱氨酸</strong>:~2100 / 2050 cm⁻¹(二硫键);遗传性疾病,需碱化 + 硫普罗宁。</li>
</ul>
<p>⚠️ 仅作成分科普参考,结石确诊、成分分析与治疗请以北医/三甲医院的检验与医嘱为准。</p>''',

('rheumatology', 'essdai.html'): r'''<h3>📐 工作原理与说明</h3>
<p><strong>ESSDAI</strong>(EULAR Sjögren's Syndrome Disease Activity Index,2010)用于评估原发性干燥综合征的系统活动度。它把病变分为 12 个域:</p>
<ul>
<li>全身、淋巴结、腺体、关节、皮肤、肺、肾、肌肉、外周神经、中枢神经、血液、生物标志物。</li>
<li>每个域按严重度赋 0–2(部分域 0–3)分,评分越高活动度越强。</li>
</ul>
<p><strong>总分 = 各域得分之和</strong>(范围 0–约 123)。判读:0 = 无活动;≥5 = 中–高活动,通常需免疫抑制治疗;≥14 = 高活动。仅作临床评估参考,诊断与用药须由风湿免疫科医师决定。</p>''',

('environment', 'convert-air-aqi.html'): r'''<h3>📐 工作原理与说明</h3>
<p>中国环境空气质量指数 <strong>AQI</strong>(依据 HJ 633-2012)将污染分为六级:优(0–50)、良(51–100)、轻度污染(101–150)、中度污染(151–200)、重度(201–300)、严重(>300)。</p>
<p>AQI 由各污染物<strong>分指数 IAQI 取最大值</strong>得到;IAQI 由浓度在分级断点间线性插值:</p>
<p><code>IAQI = (IAQI_Hi − IAQI_Lo) / (BP_Hi − BP_Lo) × (C − BP_Lo) + IAQI_Lo</code></p>
<p>参与计算的污染物:PM₂.₅、PM₁₀、SO₂、NO₂、CO、O₃。⚠️ 仅供健康与出行参考,以生态环境部门官方发布数据为准。</p>''',

('fishery', 'salinity-calculator.html'): r'''<h3>📐 工作原理与说明</h3>
<p><strong>盐度 S</strong>(实用盐标 PSU)表示每千克水体中溶解盐的克数。盐度计多以电导率 EC 推算:<code>S ≈ a + b·EC</code>。</p>
<ul>
<li>淡水与海水分界约 0.5 PSU;大洋平均约 35 PSU。</li>
<li>比重近似关系:<code>sg ≈ 1 + S/1000</code>(如 35 PSU ≈ 1.035)。</li>
<li>淡水鱼宜 &lt;0.5 PSU;广盐性(罗非鱼、鲑)可适应;海水养殖常维持 25–35 PSU。</li>
</ul>
<p>盐度变化直接影响溶氧、渗透压与存活,换水/补水时需监控。</p>''',

('it', 'invite-code-generator.html'): r'''<h3>📐 工作原理与说明</h3>
<p>邀请码在本工具完全于浏览器本地生成,核心要点:</p>
<ul>
<li>使用 <strong>Web Crypto <code>getRandomValues</code></strong> 生成密码学安全随机数(非 <code>Math.random</code>,不可预测)。</li>
<li>采用 Base32 / Base36 编码,并<strong>剔除易混字符</strong>(0/O、1/I、l),降低人工录入错误。</li>
<li>可附加<strong>校验位</strong>(Luhn 变体或 CRC)以拦截错填;批量生成自动去重保证唯一。</li>
</ul>
<p>⚠️ 全程纯前端,邀请码不上传服务器;请妥善保管,避免泄露被冒用。</p>''',

('hydraulic', 'water-level.html'): r'''<h3>📐 工作原理与说明</h3>
<p>依据<strong>伯努利方程</strong>,流线上任一点总水头 H 由三项组成:</p>
<p><code>H = z + p/(ρg) + v²/(2g)</code></p>
<ul>
<li>z:位置水头(相对基准面的高度);</li>
<li>p/(ρg):压力水头(相当于测压管中液柱高度);</li>
<li>v²/(2g):流速水头。</li>
</ul>
<p>静水压强 <code>p = ρgh</code>(ρ≈1000 kg/m³,g≈9.81 m/s²)。水头差即水流驱动力,广泛用于渠道、管道、闸门液位与扬程计算。计算时请统一单位(米、Pa)。</p>''',

('it', 'git-cheatsheet.html'): r'''<h3>📐 工作原理与说明</h3>
<p>Git 是<strong>分布式版本控制系统</strong>,代码在四个区域间流动:</p>
<ul>
<li>工作区(Working Tree)→ 暂存区(index, <code>git add</code>)→ 本地仓库(<code>git commit</code>)→ 远程仓库(<code>git push</code>)。</li>
<li>常用:init / clone / status / diff / branch / switch / merge / rebase / cherry-pick / stash / log。</li>
</ul>
<p><strong>merge</strong> 保留分支分叉历史;<strong>rebase</strong> 将提交"重放"成线性历史(已推送到公共分支的提交勿随意 rebase)。<code>.gitignore</code> 控制哪些文件不被跟踪。</p>''',

('printing', 'ink-coverage.html'): r'''<h3>📐 工作原理与说明</h3>
<p>单张油墨消耗量近似:</p>
<p><code>墨量 ≈ 印面面积 × 实地覆盖率 × 上墨量(g/m²)</code></p>
<ul>
<li>上墨量随网点/实地而异,常见 0.5–3 g/m²;满版实地最费墨。</li>
<li>总耗墨 = 单张墨量 × 印数 × (1 + 损耗率)。</li>
<li>CMYK 四色分色,各色独立计量后汇总。</li>
</ul>
<p>结果用于油墨采购与印刷成本核算;实际受纸张、网点扩大影响会有偏差。</p>''',

('stage', 'dimmer-curve.html'): r'''<h3>📐 工作原理与说明</h3>
<p>调光曲线描述<strong>输出亮度 vs 输入信号</strong>(0–100% 或 DMX512 的 0–255)的映射关系。常见类型:</p>
<ul>
<li><strong>Linear</strong>(线性):输出与输入成正比。</li>
<li><strong>Square Law</strong>(平方律):模拟白炽灯——人眼亮度近似与功率平方根相关,低区更细腻、更自然。</li>
<li><strong>S-Curve</strong>:两端缓和、中段陡峭,适合强调中间调过渡。</li>
<li><strong>Log / Inverse</strong>:反向曲线,用于特殊观感。</li>
</ul>
<p>选错曲线会造成渐变"跳变"或暗部死黑,应按灯具特性与现场需求选择。</p>''',

('health', 'ibw-calculator.html'): r'''<h3>📐 工作原理与说明</h3>
<p><strong>理想体重 IBW</strong>常用 Devine(1974)公式(单位 kg):</p>
<p><code>男 IBW = 50 + 2.3 × (身高cm − 152.4) / 2.54</code></p>
<p><code>女 IBW = 45.5 + 2.3 × (身高cm − 152.4) / 2.54</code></p>
<ul>
<li>变体 Hamwi / Robinson 系数略有差异。</li>
<li>IBW 多用于部分药物剂量(如肌松药)、营养支持与透析评估的<strong>基准</strong>,并非"健康体重目标"。</li>
</ul>
<p>个体肌肉量、骨架差异大,IBW 仅为统计参考。</p>''',

('it', 'json-to-csv.html'): r'''<h3>📐 工作原理与说明</h3>
<p>将 JSON 对象数组展平为二维表格的逻辑:</p>
<ul>
<li>递归下钻嵌套对象/数组,键名以"·"或"."合并为列名(如 <code>user.name</code>)。</li>
<li>每个数组元素输出一行;值转为字符串(布尔、数字、日期原样)。</li>
<li><code>null</code> / 缺失字段留空;数组经索引展开。</li>
</ul>
<p>导出建议带 <strong>UTF-8 BOM</strong>,以便 Excel 正确识别中文不乱码。全程纯前端解析,数据不上传。</p>''',

('advertising', 'assessor-54.html'): r'''<h3>📐 工作原理与说明</h3>
<p>户外广告媒体价值从四个维度评估:</p>
<ul>
<li><strong>触达人数</strong> = 日均客流 × 有效可见率 × 投放周期天数。</li>
<li><strong>频次</strong>:平均每人暴露次数;媒体总曝光 = 触达 × 频次。</li>
<li><strong>千人成本 CPM</strong> = 费用 / 曝光 × 1000;<strong>GRP</strong> ≈ 触达率 × 频次。</li>
<li><strong>可见性</strong>(viewability,IAB 参考):≥50% 广告面积可见且 ≥1 秒计为有效曝光。</li>
</ul>
<p>结果供媒介策划与比价参考,实际效果以第三方投放监测数据为准。</p>''',

('science', 'heat-transfer-calculator.html'): r'''<h3>📐 工作原理与说明</h3>
<p>热量传递有三种基本方式:</p>
<ul>
<li><strong>传导</strong>(傅里叶定律):<code>Q = k·A·ΔT / L</code>(k 导热系数)。</li>
<li><strong>对流</strong>(牛顿冷却):<code>Q = h·A·ΔT</code>(h 表面传热系数)。</li>
<li><strong>辐射</strong>(斯特藩-玻尔兹曼):<code>Q = ε·σ·A·(T₁⁴ − T₂⁴)</code>(σ=5.67×10⁻⁸ W/m²K⁴,ε 发射率)。</li>
</ul>
<p>复合传热用总传热系数 U:<code>Q = U·A·ΔT</code>。温度请使用绝对温标(K),面积 A、温差 ΔT 单位需统一。</p>''',

('finance', 'iccid-validator.html'): r'''<h3>📐 工作原理与说明</h3>
<p><strong>ICCID</strong> 是 SIM 卡的唯一标识,长度 19–20 位,结构为:前 3 位 MCC(国家码)+ 2 位 MNC(运营商)+ 账户标识 + 末位校验位。</p>
<p>校验位采用 <strong>Luhn 算法</strong>:从右数第 2 位起,奇数位乘 2(若 &gt;9 则减 9),与偶数位数字求和,总和模 10 为 0 即合法。</p>
<p>⚠️ 仅校验号码格式合法性,不验证卡片是否真实激活或归属。</p>''',

('it', 'bip39-generator.html'): r'''<h3>📐 工作原理与说明</h3>
<p><strong>BIP39</strong> 助记词生成流程:</p>
<ul>
<li>取熵(128–256 bit)→ 计算 SHA-256,取前 <code>ENT/32</code> 位作为校验和。</li>
<li>熵 + 校验和拼接,按每 <strong>11 bit</strong> 一组 → 查 2048 词英语词表。</li>
<li>得 12 / 15 / 18 / 21 / 24 个单词;可加 passphrase(BIP39 第 2 因子)增强。</li>
<li>最终 seed 经 <strong>PBKDF2</strong>(2048 次)派生主密钥。</li>
</ul>
<p>⚠️ 助记词即资产控制权,务必离线抄写保管,任何泄露 = 资产丢失;本工具纯前端生成。</p>''',

('finance', 'cpf-validator.html'): r'''<h3>📐 工作原理与说明</h3>
<p>巴西 <strong>CPF</strong> 共 11 位,前 9 位为基,第 10、11 位为校验位,采用模 11 算法:</p>
<ul>
<li>第 10 位:前 9 位分别乘 10→2 求和,取模 11;余 0 或 1 则第 10 位 = 0,否则 = 11 − 余。</li>
<li>第 11 位:前 10 位乘 11→2 求第 11 位,规则同上。</li>
<li>全相同数字(如 111.111.111-11)直接判无效。</li>
</ul>
<p>⚠️ 仅校验号码格式,不验证 CPF 是否真实存在或有效。</p>''',

('fun', 'generator-3.html'): r'''<h3>📐 工作原理与说明</h3>
<p>迷宫生成常用三类算法,特征各异:</p>
<ul>
<li><strong>递归回溯(DFS)</strong>:生成"主干 + 死胡同",通常<strong>唯一解</strong>,路径长。</li>
<li><strong>Prim / Kruskal</strong>(随机权重):生成多岔路、更开放,解不唯一。</li>
<li><strong>递归分割</strong>:生成对称房间式结构。</li>
</ul>
<p>自动求解采用 BFS 或 A* 求最短路径;网格越大,路径越复杂。纯娱乐,生成结果无版权。</p>''',

('fun', 'generator-laugh.html'): r'''<h3>📐 工作原理与说明</h3>
<p>笑声由 <strong>Web Audio API</strong> 在浏览器内实时合成,不涉及任何第三方音频素材:</p>
<ul>
<li>基频振荡器(sawtooth / square)模拟声带"哈"的顿挫。</li>
<li><strong>ADSR 包络</strong>控制每个"哈"的起音/衰减/释放,形成节奏。</li>
<li><strong>LFO 颤音</strong> + 共振峰(formant)滤波逼近人声元音音色。</li>
</ul>
<p>参数随机微调产生多样的"哈哈哈"。合成音频可自由下载使用,无版权风险。</p>''',

('ai', 'ai-prompt-generator.html'): r'''<h3>📐 工作原理与说明</h3>
<p>高质量提示词(Prompt)通常包含五要素,本工具按模板拼接并填空:</p>
<ul>
<li><strong>角色(Role)</strong> + <strong>任务(Task)</strong> + <strong>上下文(Context)</strong> + <strong>格式(Format)</strong> + <strong>约束(Constraints)</strong>。</li>
<li>可附加 few-shot 示例、chain-of-thought(逐步推理)引导。</li>
</ul>
<p>token 估算:中文约 1 字 ≈ 1.5 token、英文约 1 词 ≈ 1.3 token(仅作量级参考)。有效提示应<strong>明确、单一、给示例与边界</strong>。</p>''',

('fun', 'lottery-quick-pick.html'): r'''<h3>📐 工作原理与说明</h3>
<p>本工具使用 <strong>Web Crypto</strong> 生成密码学安全随机数,在各彩种号码池内不重复抽取:</p>
<ul>
<li>双色球:红球 1–33 选 6 + 蓝球 1–16 选 1。</li>
<li>大乐透:前区 1–35 选 5 + 后区 1–12 选 2。</li>
</ul>
<p>⚠️ 开奖为极低概率随机事件(双色球头奖 ≈ 1/17,721,536),本工具<strong>无任何预测能力</strong>,纯娱乐,请理性购彩。</p>''',

('it', 'qrcode.html'): r'''<h3>📐 工作原理与说明</h3>
<p>QR 码由定位与编码两类图案组成:</p>
<ul>
<li><strong>定位图案</strong>:三个角上的 Finder(回字)、Alignment、Timing,用于扫码定位与校正。</li>
<li><strong>编码模式</strong>:数字 / 字母数字 / 字节(UTF-8)/ 汉字,自动选最短以省空间。</li>
<li><strong>纠错等级</strong> L / M / Q / H 可恢复约 7% / 15% / 25% / 30% 的损毁。</li>
<li><strong>版本</strong> 1–40 对应模块 21×21 → 177×177;含 Reed-Solomon 纠错与掩码优化。</li>
</ul>
<p>纯前端生成,扫码即可读取,无需联网。</p>''',

('general', 'convert-22.html'): r'''<h3>📐 工作原理与说明</h3>
<p>本工具处理 <strong>SI 词头</strong>与 10 的幂的换算。常用词头:</p>
<ul>
<li>atto 10⁻¹⁸、femto 10⁻¹⁵、pico 10⁻¹²、nano 10⁻⁹、micro(µ)10⁻⁶、milli 10⁻³、centi 10⁻²。</li>
<li>kilo 10³、mega 10⁶、giga 10⁹、tera 10¹² … yotta 10²⁴。</li>
</ul>
<p>换算:<code>x_dst = x_src × 10^(e_src − e_dst)</code>。注意<strong>二进制词头</strong> Ki=2¹⁰、Mi=2²⁰、Gi=2³⁰ 用于数据存储,不等于十进制的 10³/10⁶/10⁹。</p>''',

('general', 'detector-159.html'): r'''<h3>📐 工作原理与说明</h3>
<p>本工具对机械部件做三项力学性能检测与合格判定:</p>
<ul>
<li><strong>刚度</strong>:k = F / δ(载荷 / 变形量,胡克定律),反映抗变形能力。</li>
<li><strong>额定载荷</strong>:依据标准(如 GB/T 1448 玻璃钢弯曲、GB/T 307 滚动轴承)判定许用值。</li>
<li><strong>疲劳寿命</strong>:用 S-N 曲线 + <strong>Miner 线性累积损伤</strong>准则,∑ n_i/N_i ≤ 1 视为安全。</li>
</ul>
<p>⚠️ 仅作工程估算与自检参考,正式判定与出报告须由具备资质的第三方检测机构完成。</p>''',

('it', 'hash-multi.html'): r'''<h3>📐 工作原理与说明</h3>
<p>哈希函数把任意长度输入映射为<strong>定长摘要</strong>,具备确定性、雪崩效应(改 1 bit 约半数输出变)、单向不可逆。</p>
<ul>
<li>支持 MD5(128b)/ SHA-1(160b)/ SHA-256 / SHA-512 / SHA-3,经 Web Crypto <code>SubtleCrypto.digest</code> 计算。</li>
<li>用途:文件完整性校验、去重、内容指纹。</li>
</ul>
<p>⚠️ <strong>安全提示</strong>:MD5、SHA-1 已被证明可碰撞,勿用于数字签名或口令存储;口令应使用 bcrypt / Argon2 等慢哈希。本工具纯前端,数据不上传。</p>''',
}

def build(inner):
    return '<div class="formula-box" data-polish="TOOLBOX-POLISH">\n' + inner + '\n</div>'

POLISH = {k: build(v) for k, v in RAW.items()}

def apply(ind, f):
    p = os.path.join(ROOT, 'tools', ind, f)
    if not os.path.exists(p):
        return 'MISSING'
    s = open(p, encoding='utf-8', errors='ignore').read()
    if 'TOOLBOX-POLISH' in s:
        return 'SKIP(polished)'
    new = POLISH.get((ind, f))
    if not new:
        return 'NO-CONTENT'
    if 'formula-box' in s:
        ns = re.sub(r'<div class="formula-box"[^>]*>.*?</div>', new, s, count=1, flags=re.S)
        if ns == s:
            return 'REPLACE-FAIL'
        open(p, 'w', encoding='utf-8').write(ns)
        return 'REPLACED'
    ns = re.sub(r'(</h2>)', r'\1\n' + new, s, count=1)
    open(p, 'w', encoding='utf-8').write(ns)
    return 'INSERTED'

def main():
    dry = '--dry-run' in sys.argv
    keys = list(POLISH.keys())
    print('待升级页面:', len(keys))
    cnt = {'REPLACED': 0, 'INSERTED': 0, 'SKIP(polished)': 0, 'MISSING': 0, 'NO-CONTENT': 0, 'REPLACE-FAIL': 0}
    for ind, f in keys:
        if dry:
            print('DRY', ind, f)
            continue
        r = apply(ind, f)
        cnt[r] = cnt.get(r, 0) + 1
        print(r, ind, f)
    print('=== 汇总:', cnt, '===')

if __name__ == '__main__':
    main()
