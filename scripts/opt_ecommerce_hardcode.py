# -*- coding: utf-8 -*-
"""清理 ecommerce 工具页硬编码套话：
A 类 formula-desc：14 页通用占位/错配 → 真实领域描述（5 页财务/数学领域变体语义相符保留）；
C 类 tool-intro-body 块内 6 类通用套话：19 页（cycle-15/groupon-filler 块内已真实或缺失，跳过）。
B 类 opt 套话「工作与生活中的相关计算与查询」0 命中。
"""
import re, sys, os

DRY = '--dry' in sys.argv
BASE = 'tools/ecommerce'

# ---- A 类 formula-desc 替换（仅需清理的 14 页）----
A_REPL = {
 'calc-79': '本工具按本期与基期数值计算同比/环比增长率，自动处理基期为零与跨期对比，输出百分比与变动绝对值。',
 'calc-commission-2': '本工具按成交金额与佣金比例（含阶梯与封顶）计算平台佣金、服务费与到账金额，支持多档费率试算。',
 'conversion-4': '本工具按直播观看人数、互动与成交订单计算观看转化率、千次观看成交(GPM)与流量变现效率。',
 'erp-dingdan-caigou-duijie': '本工具按订单量、采购提前期与安全库存计算再订货点与补货建议，并生成订单-采购字段映射，辅助 ERP 协同。',
 'kedan-jiandanjia-liandailv': '本工具按销售额、订单数与件数计算客单价、件单价与连带率，辅助门店连带销售分析。',
 'wuliu-fahuo-cangchu-gongyinglian-zhenghe': '本工具按发货量、仓储周转与履约时效计算物流整合成本与时效，辅助供应链协同与仓网优化。',
 'pingjia-chaping-tuihuo-lv': '本工具按评价数、差评数与退货数计算好评率、差评率与退货率，辅助服务与品控监控。',
 'estimate-ranking': '本工具按销量、评分、点击与转化等权重因子估算搜索排名得分与相对位次，辅助搜索优化。',
 'wuliu-lanshou-qianshou-shixiao': '本工具按揽收、运输与签收时间计算物流时效与超时率，辅助承运商考核与时效监控。',
 'response-2': '本工具按咨询量、首次响应时长与解决率计算客服平均响应时间、首响与解决率指标。',
 'discount': '本工具按折扣率、满减门槛与优惠券叠加规则计算到手价与优惠力度，支持多方案对比。',
 'inventory-1': '本工具按日均销量、补货提前期与安全库存计算再订货点与预警，输出补货数量建议。',
 'kaidian-yunyingyuguizeduibijisuanqi': '本工具按平台开店保证金、佣金率、年费与流量规则对比多平台开店与运营成本，输出对比结论。',
 'analysis-25': '本工具汇总多平台同款商品到手价、历史价与折扣力度，自动计算价差与监控预警，辅助选品与调价决策。 工具名称：竞品（比价/监控）分析。',
}

# ---- C 类 tool-intro-body 清理（19 页）----
JUNK_TAIL = '免费在线工具，纯前端处理，数据不上传，保护隐私安全。'
KEEP_FEATS = ['纯前端处理，数据不上传服务器', '支持复制和下载结果', '实时显示结果，所见即所得']

# 各页：简介前缀（保留）+ 真实功能特点（替换"操作简单，一键完成"）+ 4 真实使用场景
C_REPL = {
 'analysis-25': dict(prefix='竞品（比价/监控）分析。',
   feat='录入多平台同款到手价自动算价差与监控预警',
   scenes=['多平台选品比价与最低价判断', '重点 SKU 历史价与伪降价监控', '活动调价前后价差复盘', '竞品价格带分布速览']),
 'analysis-conversion-funnel': dict(prefix='转化（漏斗/流失）分析。',
   feat='录入各漏斗层人数自动算转化率与流失',
   scenes=['曝光→点击→加购→支付瓶颈定位', '大促活动漏斗复盘', '行业基准对比找弱层', '落地页改版前后转化对比']),
 'analysis-cost-8': dict(prefix='成本（控制/优化/效益）分析。',
   feat='按采购/佣金/物流/推广分项核算毛利',
   scenes=['单品与店铺毛利率核算', '低毛利品识别与优化', '费用结构占比分析', '促销前后利润测算']),
 'calc-79': dict(prefix='增长率（同比/环比）计算。',
   feat='录入本期与基期自动算同比/环比',
   scenes=['经营月报同比增长核算', '环比短期走势跟踪', '基期为 0 的异常处理', '多指标趋势对比']),
 'calc-commission-2': dict(prefix='佣金（平台/服务费）计算。',
   feat='按费率与封顶算佣金与到账',
   scenes=['成交结算佣金试算', '阶梯费率跳档对比', '大额订单佣金封顶测算', '多平台佣金成本比较']),
 'conversion-4': dict(prefix='直播（观看/成交）转化。',
   feat='按观看与成交算转化率与 GPM',
   scenes=['直播间观看转化率评估', '千次观看成交(GPM)对比', '主播/场次变现效率排名', '互动与转化关系观察']),
 'discount': dict(prefix='促销（折扣/满减/优惠券）设计。',
   feat='按折扣/满减/券叠加算到手价',
   scenes=['满减与折扣方案到手价对比', '优惠券叠加顺序测算', '活动优惠力度统一比较', '利润与促销力度平衡']),
 'erp-dingdan-caigou-duijie': dict(prefix='ERP（订单/采购）对接。',
   feat='算再订货点并生成字段映射',
   scenes=['再订货点与补货预警', '平台订单与 ERP 物料映射', '采购提前期安全库存设定', '断货风险排查']),
 'estimate-ranking': dict(prefix='排名（搜索/权重）估算。',
   feat='按权重因子估算搜索排名分',
   scenes=['搜索排名得分估算', '评分/转化短板定位', '标题与主图优化前后对比', '类目内相对位次判断']),
 'inventory-1': dict(prefix='库存（预警/补货）自动。',
   feat='按日均销量与提前期算再订货点',
   scenes=['库存预警与再订货点', '目标周转补货量测算', '安全库存设定', '断货与资金占用权衡']),
 'kaidian-yunyingyuguizeduibijisuanqi': dict(prefix='平台（开店/运营/规则）熟悉。',
   feat='对比多平台开店与运营成本',
   scenes=['多平台首年入驻成本对比', '佣金率对利润影响测算', '保证金与年费占用比较', '品类适配平台选择']),
 'kedan-jiandanjia-liandailv': dict(prefix='客单（件单价/连带率）。',
   feat='按销售额与件数算客单连带',
   scenes=['客单价与件单价核算', '连带率分析与提升', '门店连带销售诊断', '搭配推荐效果评估']),
 'pingjia-chaping-tuihuo-lv': dict(prefix='评价（差评/退货）率。',
   feat='算好评/差评/退货率并预警',
   scenes=['差评率阈值监控', '高退货品类定位', '体验与品控归因', '评价结构健康度看板']),
 'report': dict(prefix='BI（报表/可视化）仪表。',
   feat='多维度经营指标卡可视化',
   scenes=['经营日报/周报看板搭建', '关键指标异常标红', '同环比与占比呈现', '核心指标快照汇总']),
 'response-2': dict(prefix='客服（咨询/投诉）响应。',
   feat='算平均/首响时长与解决率',
   scenes=['客服响应时长考核', '首响 P50/P90 分布', '解决率与服务质监', '高峰期排班参考']),
 'stats-flow-conversion': dict(prefix='流量（UV/PV/转化）统计。',
   feat='按 UV/PV 算深度与转化率',
   scenes=['流量质量与跳出率分析', 'UV 转化率评估', '内容吸引深度诊断', '落地页承接优化']),
 'stats-profit': dict(prefix='利润率（单品/店铺）统计。',
   feat='按全费用核算毛利与净利',
   scenes=['单品与店铺盈利核算', '多 SKU 利润排序', '引流款与利润款组合', '退款对利润影响测算']),
 'wuliu-fahuo-cangchu-gongyinglian-zhenghe': dict(prefix='物流（发货/仓储/供应链）整合。',
   feat='算物流整合成本与履约时效',
   scenes=['单仓与分仓履约成本比', '仓网覆盖优化', '库存周转效率评估', '供应链协同时效监控']),
 'wuliu-lanshou-qianshou-shixiao': dict(prefix='物流（揽收/签收）时效。',
   feat='算物流时效与超时率',
   scenes=['履约时长与超时率考核', '多承运商准时率对比', '分环节慢点定位', '承运商服务质量评估']),
}

def fix_a(n):
    p = os.path.join(BASE, n + '.html')
    s = open(p, encoding='utf-8').read()
    new = s
    # 通用占位（无 工具名称 后缀）
    for old in ('<p class="formula-desc">输入两个参数，自动计算常用结果</p>',
                '<p class="formula-desc">输入各项参数，自动计算对比结果。</p>'):
        if old in new:
            new = new.replace(old, '<p class="formula-desc">%s</p>' % A_REPL[n])
    # analysis-25 工程错配（含 工具名称 后缀）
    if n == 'analysis-25':
        old = '<p class="formula-desc">本工程计算基于标准物理与材料公式，输入为标准工程单位，结果仅供参考。 工具名称：竞品（比价/监控）分析。</p>'
        if old in new:
            new = new.replace(old, '<p class="formula-desc">%s</p>' % A_REPL[n])
    return s, new

def fix_c(n):
    p = os.path.join(BASE, n + '.html')
    s = open(p, encoding='utf-8').read()
    r = C_REPL[n]
    new = s
    # 1) 简介尾随语：<前缀>JUNK_TAIL → <前缀>
    pat_intro = re.compile(r'(<h4><span class="h4-icon">📝</span>工具简介</h4>\s*<p>' + re.escape(r['prefix']) + r')' + re.escape(JUNK_TAIL))
    new = pat_intro.sub(lambda m: m.group(1), new)
    # 2) 功能特点：替换套话 li 为真实功能
    new = new.replace('<li>操作简单，一键完成</li>', '<li>%s</li>' % r['feat'])
    # 3) 使用场景：整段替换 4 项通用为真实场景
    new = re.sub(r'(<h4><span class="h4-icon">🎯</span>使用场景</h4>\s*<ul class="intro-scenes">).*?(</ul>)',
                 lambda m: m.group(1) + ''.join('<li>%s</li>' % x for x in r['scenes']) + m.group(2),
                 new, flags=re.S)
    return s, new

def main():
    print('=== ecommerce A/C 类检测/清理 ===')
    # A 类保留（语义相符）报告
    keep = ['analysis-conversion-funnel','stats-profit','analysis-cost-8','report','stats-flow-conversion']
    print('(A) 保留(财务/数学领域变体语义相符):', keep)
    for n in A_REPL:
        before, after = fix_a(n)
        left = ('<p class="formula-desc">输入两个参数，自动计算常用结果</p>' in after
                or '<p class="formula-desc">输入各项参数，自动计算对比结果。</p>' in after
                or ('analysis-25'==n and '本工程计算基于标准物理与材料公式' in after))
        print('(A)[%s] 占位残留:%s' % (n, left))
    # C 类
    for n in C_REPL:
        before, after = fix_c(n)
        tail = JUNK_TAIL in after
        feat = '操作简单，一键完成' in after
        scenes = '日常办公与学习' in after
        print('(C)[%s] 尾随语残留:%s 套话li残留:%s 通用场景残留:%s' % (n, tail, feat, scenes))
    if not DRY:
        for n in A_REPL:
            _, after = fix_a(n); open(os.path.join(BASE, n+'.html'), 'w', encoding='utf-8').write(after)
        for n in C_REPL:
            _, after = fix_c(n); open(os.path.join(BASE, n+'.html'), 'w', encoding='utf-8').write(after)
        print('已写入')
    print('完成' if not DRY else 'DRY完成')

if __name__ == '__main__':
    main()
