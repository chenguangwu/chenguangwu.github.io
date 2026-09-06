# -*- coding: utf-8 -*-
"""清理 banking 分类旧套话：20 个 formula-desc 升级为详实计算原理；fisher-real-rate 旧 opt-faq/适用场景替换。"""
import os, re, json

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOOLS_DIR = os.path.join(ROOT, "tools", "banking")
CONTENT = os.path.join(ROOT, "i18n", "tools", "content_deepdive.json")

# 各文件 formula-desc 真实化文案（含公式/参数/边界说明）
FD = {
    "amortization-first-interest": "首月利息=贷款总额×月利率，月利率=年利率÷12。等额本息首期剩余本金即全额，故首月利息最高，之后随本金摊还逐月递减。",
    "apy-calculator": "APY=(1+r/n)^n−1，r 为名义年利率、n 为每年复利次数；反映不同复利频率下的真实年化收益，频率越高 APY 越大，上限为连续复利 e^r−1。",
    "bond-current-yield": "当前收益率=年息÷市价，年息=面值×票息率。折价买入（市价<面值）时高于票息率，溢价买入时低于票息率；不含资本利得与期限因素。",
    "break-even-savings": "设存款占比 X，净息=X·r_d−(1−X)·r_l，令其为零得 X=r_l÷(r_d+r_l)。该点左侧存款更划算、右侧还贷更划算，未计入流动性、风险与税负。",
    "compound-interest": "A=P(1+r/n)^(nt)，P 本金、r 名义年利率、n 年复利次数、t 年数。复利频率越高终值越大，连续复利 A=P·e^(rt) 为理论上限。",
    "credit-card-interest-monthly": "月利息=欠款余额×日利率×计息天数。多数银行未全额还款即从每笔消费记账日起按日计息、免息期失效，折合年化约日利率×365（如 0.05%×365≈18.25%）。",
    "daily-interest": "利息=本金×日利率×实际天数，日利率=年利率÷计基（国内常用 360 或实际 365）。「算头不算尾」使取款当日不计息，跨日资金须核对计息天数。",
    "debt-to-income": "DTI=月债务支出÷月收入，常见警戒线 43%~50%，越低偿债压力越小。仅含房贷、车贷、信用卡最低还款等债务性支出，不含日常消费。",
    "effective-annual-rate": "EAR=(1+r/n)^n−1，r 名义年利率、n 复利次数，是贷款的真实年化成本。比较信贷产品应以 EAR 而非合同 APR 为准，高频复利会显著抬高成本。",
    "fisher-real-rate": "精确费雪 (1+名义)=(1+实际)(1+通胀)，故实际=(1+名义)÷(1+通胀)−1。近似式「名义−通胀」仅适用于低利率低通胀，高通胀时交叉项不可忽略须用精确式。",
    "future-value-annuity-due": "FV=PMT×[(1+r)^n−1]÷r×(1+r)，期初年金每笔付款多赚一期利息，终值=同参数期末年金×(1+r)。适用于房租、保费等期初支付流。",
    "growing-annuity-pv": "PV=C÷(r−g)×[1−((1+g)/(1+r))^n]，C 首期现金流、r 贴现率、g 增长率、n 期数。须满足 r>g 否则现值发散、公式失效。",
    "loan-tenure": "n=ln(PMT÷(PMT−P·r))÷ln(1+r)，P 本金、r 每期利率、PMT 月供。若月供≤月息（PMT≤P·r）则分母非正、无解，本金越欠越多，须提高月供。",
    "loan-to-value": "LTV=贷款额÷抵押物评估值。分母通常取评估值与成交价的较低者以防「高评高贷」，LTV 越低杠杆越安全，房价下跌时抗负资产能力越强。",
    "loan-total-interest": "总利息=月供×期数−本金。等额本息前期利息占比高、本金摊还慢，缩短期限或提高月供可显著压降总利息；等额本金总息更少但前期月供高。",
    "net-worth": "净资产=总资产−总负债，含房产、存款、投资与房贷、信用贷等。自住房计入资产但流动性差，分析偿债力时常单列「可投资净资产」。",
    "nominal-from-effective": "名义 r=n×((1+EAR)^(1/n)−1)，由真实年化 EAR 反推挂牌名义年利率，用于统一不同复利频率产品的利率口径；n 为每年复利次数。",
    "perpetuity-pv": "PV=C÷r，C 每期现金流、r 贴现率，适用于永久国债、优先股等无限期现金流。现实中多含赎回或违约条款，严格永续仅存在于模型。",
    "present-value-annuity-due": "PV=PMT×[1−(1+r)^(−n)]÷r×(1+r)，期初年金每笔提前一期发生、折现期少一期，现值高于同参数期末年金（如房贷月供）。",
    "tax-equivalent-yield": "TEY=免税收益率÷(1−边际税率)。只有应税品种收益率高于 TEY 时才更划算，须代入自身边际税率比较；资本利得税未纳入。",
}

PAT_FD = re.compile(r'<p class="formula-desc"[^>]*>.*?</p>', re.S)
PAT_OPTFAQ = re.compile(r'<section class="opt-faq">.*?</section>', re.S)
PAT_SCEN = re.compile(r'<h2>适用场景</h2><p>.*?</p>', re.S)


def main():
    data = json.load(open(CONTENT, encoding="utf-8"))
    still_cliche = 0
    fd_changed = 0
    opt_changed = 0
    for fn in sorted(os.listdir(TOOLS_DIR)):
        if not fn.endswith(".html") or fn == "index.html":
            continue
        base = fn[:-5]
        key = "banking/" + base
        p = os.path.join(TOOLS_DIR, fn)
        s = open(p, encoding="utf-8").read()
        s2 = s
        if base in FD:
            new_fd = '<p class="formula-desc">%s</p>' % FD[base]
            if PAT_FD.search(s2):
                s2 = PAT_FD.sub(new_fd, s2, count=1)
                fd_changed += 1
            else:
                print("  FD not found in", base)
        # fisher-real-rate 旧 opt-faq + 适用场景
        if base == "fisher-real-rate":
            e = data.get(key, {})
            faqs = e.get("faqs", [])
            if faqs and PAT_OPTFAQ.search(s2):
                dl = "<section class=\"opt-faq\"><h2>常见问题</h2><dl class=\"faq-list\">"
                for f in faqs:
                    dl += "<dt>%s</dt><dd>%s</dd>" % (f["q"], f["a"])
                dl += "</dl></section>"
                s2 = PAT_OPTFAQ.sub(dl, s2, count=1)
                opt_changed += 1
            scen = e.get("scenarios", [])
            if scen and PAT_SCEN.search(s2):
                new_scen = "<h2>适用场景</h2><p>%s</p>" % scen[0]
                s2 = PAT_SCEN.sub(new_scen, s2, count=1)
        # cliche re-check
        if any(w in s2 for w in ["在对应的输入框或选项中填写", "工具名称：", "本计算器基于标准数学运算", "本工程计算", "工作与生活中的相关计算与查询", "本速查内容依据权威标准", "高频复用模板", "可先用该工具生成一版标准结果"]):
            still_cliche += 1
            print("  still_cliche:", base)
        if s2 != s:
            open(p, "w", encoding="utf-8").write(s2)
    print("banking FD upgraded:", fd_changed, "| opt-faq cleaned:", opt_changed, "| still_cliche:", still_cliche)


if __name__ == "__main__":
    main()
