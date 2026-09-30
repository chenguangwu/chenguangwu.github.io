#!/usr/bin/env python3
# 由 report7 的非冒号候选短标签批译：多字词汇+单位规则，只收译文零中文的干净项，作为前缀键并入 _prefix.json
import json, re, os
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
report=json.load(open('/tmp/en_audit/report7.json'))
uniq=set()
for p,v in report.items():
    for x in v.get('strings',[]):
        if '：' not in x: uniq.add(x)

# 只处理：纯中文/少量标点、无句子标点、长度>=2
cand=[s for s in uniq if len(s)>=2 and '。' not in s and '！' not in s and '？' not in s
      and re.match(r'^[一-鿿，、（）()·\s]{2,14}$', s)]

# 多字词汇（CJK->EN），最长优先；仅用于整词替换
V={
'还款总额':'Total repayment','总利息':'Total interest','总回报率':'Total return','净收益':'Net profit',
'年利息收入':'Annual interest income','税后所得':'After-tax income','总收益':'Total return',
'每年利息':'Annual interest','累计回报率':'Cumulative return','科学记数法':'Scientific notation',
'额定扬程':'Rated head','额定压力':'Rated pressure','中文读法':'Chinese reading','原模型月供参考':'Original model payment ref',
'可用范围':'Available range','胜率':'Win rate','额定流量':'Rated flow','输入值':'Input value',
'当前价格':'Current price','初始投入':'Initial investment','月供':'Monthly payment','月供最少':'Min monthly payment',
'概率密度':'Probability density','资产负债率':'Asset-liability ratio','工程记数法':'Engineering notation',
'搭配解读':'Matching interpretation','建议仓位金额':'Suggested position amount','历史均值':'Historical mean',
'推荐设备类型':'Recommended device type','常规表示':'Conventional notation','到期收益率':'Yield to maturity',
'期末价值':'End-of-period value','搭配色':'Secondary color','采购进度':'Procurement progress',
'质量保障综合评分':'QA composite score','建议校准周期':'Recommended calibration interval','甲醛释放量':'Formaldehyde emission',
'距上次校准':'Time since calibration','合规':'Compliance','材料类型':'Material type','中文大写':'Chinese capital numerals',
'信用等级':'Credit rating','约分':'Fraction reduction','整改建议':'Rectification suggestion','饱和度差':'Saturation difference',
'累计盈亏':'Cumulative P/L','建议方案':'Suggested solution','估算覆盖面积':'Estimated coverage area',
'累积概率':'Cumulative probability','催收策略':'Collection strategy','标准小数':'Standard decimal',
'实际税率':'Effective tax rate','凯利分数':'Kelly fraction','建议电机功率':'Suggested motor power',
'贷款本金':'Loan principal','购买力缩水':'Purchasing power loss','需更换部件清单':'Parts replacement list',
'下期预测用量':'Next-period forecast','年化收益率':'Annualized return','服务环节':'Service stage',
'苯系物含量':'BTEX content','英文单词':'English word','速算扣除数':'Quick deduction','推荐传感器类型':'Recommended sensor type',
'保留 4 位有效数字':'Keep 4 sig figs','未折现净现金流':'Undiscounted net cash flow','归一化后权重':'Normalized weights',
'应纳税所得额':'Taxable income','评估标准':'Evaluation criteria','信用评分':'Credit score','通分':'Common denominator',
'文本总长度':'Total text length','相加':'Sum','当期收益率':'Current yield','评级':'Rating','综合评分':'Composite score',
'使用年限':'Service life','环保等级':'Eco grade','保养计划':'Maintenance plan','成本绩效指数':'Cost performance index',
'保养后测试':'Post-maintenance test','公式':'Formula','互补色':'Complementary color','修复输出':'Repair output',
'应用场景':'Application scenario','检测到':'Detected','建议仓位比例':'Suggested position ratio','基本单位值':'Base unit value',
'小数':'Decimal','分档计算明细':'Tiered breakdown','工程总费用':'Total project cost','明度差':'Lightness difference',
'搭配建议':'Matching suggestion','电机功率':'Motor power','环境要求':'Environmental requirement','估算轴功率':'Estimated shaft power',
'对比完成':'Comparison complete','标准分':'Standard score','磨损量':'Wear amount','首月还款':'First month payment',
'预计总寿命':'Estimated total life','落地速度':'Impact velocity','含义':'Meaning','字符数':'Character count',
'原始大小':'Original size','净现值':'Net present value','品相等级':'Grade level','推荐设备':'Recommended device',
'效率要求':'Efficiency requirement','压缩形式':'Compression form','本利和':'Principal & interest','盈利指数':'Profitability index',
'抗风等级':'Wind resistance rating','基本单位':'Base unit','年化回报率':'Annualized return','三个内角':'Three interior angles',
'应用场景':'Application scenario','推荐机型':'Recommended model','主色':'Primary color','搭配色':'Secondary color',
'搭配建议':'Matching suggestion','搭配解读':'Matching interpretation','色相差角':'Hue angle diff','色相关系':'Hue relation',
'和谐度评分':'Harmony score','中差色':'Medium-contrast color','互补色':'Complementary color','明暗梯度':'Light-dark gradient',
'色温描述':'Color temperature desc','白平衡设置':'White balance setting','对比度':'Contrast ratio','对比度比值':'Contrast ratio',
'等级':'Level','通过':'Pass','优秀':'Excellent','正常文字':'normal text','大号文字':'large text','相对亮度':'relative luminance',
'评估结果':'Evaluation result','评估':'Evaluation','结论':'Conclusion','建议':'Suggestion','参考':'Reference','明细':'Details',
'总数':'Total','结果':'Result','统计':'Statistics','预览':'Preview','原始':'Original','处理后':'Processed',
'字符':'characters','字符数':'Character count','行':'lines','行数':'lines','字':'characters','词':'words',
'字节':'bytes','千字节':'KB','兆字节':'MB','吉字节':'GB','太字节':'TB','拍字节':'PB',
'二进制千字节':'KiB','二进制兆字节':'MiB','二进制吉字节':'GiB','二进制太字节':'TiB','二进制拍字节':'PiB',
'像素':'px','位':'bits','秒':'s','分钟':'min','小时':'h','天':'days','年':'yr','月':'mo','周':'weeks',
'倍':'×','条':'items','个':'pcs','次':'times','组':'groups','页':'pages','种':'types','字体':'font',
'模块':'modules','尧米':'Ym','二维码':'QR code','条形码':'barcode','数字':'number','方案':'scheme',
'圆点':'dot','条纹':'stripe','网格':'grid','棋盘':'checkerboard','实心':'solid','虚线':'dashed','双线':'double',
'圆形':'circle','方形':'square','星形':'star','菱形':'diamond','正方形':'square','三角形':'triangle','椭圆':'ellipse',
'日落':'Sunset','森林':'Forest','海洋':'Ocean','赛博朋克':'Cyberpunk','莫兰迪':'Morandi','温暖':'Warm','深沉':'Deep',
'自然':'Natural','商务':'Business','活力':'Vibrant','粉彩':'Pastel','大地':'Earth','薰衣草':'Lavender','珊瑚':'Coral',
'日光':'Daylight','闪光灯':'Flash','标准白光':'standard white light','示例文字':'Sample text',
# 金融/工程长尾
'本金':'Principal','利息':'Interest','利率':'Rate','收益率':'Return','残值':'Residual value','贬值率':'Impairment rate',
'折旧':'Depreciation','折扣':'Discount','税额':'Tax amount','税费':'Tax & fees','手续费':'Fee','均价':'Avg price',
'单价':'Unit price','总价':'Total price','金额':'Amount','价值':'Value','利润':'Profit','成本':'Cost','造价':'Cost',
'投资':'Investment','回报':'Return','回收':'Recovery','节能':'Energy saving','寿命':'Life','精度':'Precision',
'强度':'Strength','载荷':'Load','转速':'Rotation speed','温度':'Temperature','压力':'Pressure','流量':'Flow',
'电压':'Voltage','功率':'Power','效率':'Efficiency','质量':'Quality','等级':'Grade','范围':'Range','因子':'Factor',
'系数':'Coefficient','合格':'Qualified','评估':'Evaluation','检查':'Inspection','维修':'Maintenance','建议':'Suggestion',
'推荐':'Recommended','配置':'Config','设计':'Design','检测':'Detection','磨损':'Wear','润滑':'Lubrication',
'防护':'Protection','防爆':'Explosion-proof','防锈':'Anti-rust','防雷':'Lightning protection','阻燃':'Flame retardant',
'密封':'Sealing','稳定':'Stable','经济':'Economic','环境':'Environmental','环保':'Eco','空气':'Air','水质':'Water quality',
'污染':'Pollution','细菌':'Bacteria','微生物':'Microbial','腐蚀':'Corrosion','老化':'Aging','疲劳':'Fatigue',
'耐热':'Heat resistant','耐温':'Temp resistant','耐磨':'Wear resistant','耐腐蚀':'Corrosion resistant','绝缘':'Insulation',
'电动':'Electric','机械':'Mechanical','材料':'Material','面料':'Fabric','金属':'Metal','合金':'Alloy','玻璃':'Glass',
'陶瓷':'Ceramic','塑料':'Plastic','通用':'General','专用':'Dedicated','标准':'Standard','常用':'Common','可选':'Optional',
'主要':'Main','次要':'Secondary','初始':'Initial','实际':'Actual','理论':'Theoretical','预计':'Estimated',
'最大':'Max','最小':'Min','平均':'Average','累计':'Cumulative','剩余':'Remaining','可用':'Available','总':'Total',
'净':'Net','毛':'Gross','原':'Original','新':'New','旧':'Old','高':'High','低':'Low','中':'Medium','良好':'Good',
'适中':'Moderate','正常':'Normal','超标':'Exceeds limit','充裕':'Ample','轻微':'Slight','明显':'Obvious','合理':'Reasonable',
'代码':'Code','字符画':'ASCII art','字体':'Font','字号':'Font size','分辨率':'Resolution','码率':'Bitrate',
'续航':'Battery life','焦距':'Focal length','光圈':'Aperture','镜头':'Lens','机身':'Body','画幅':'Format','屏幕':'Screen',
'显示':'Display','网络':'Network','地址':'Address','子网':'Subnet','路由':'Routing','接口':'Interface','协议':'Protocol',
'内存':'Memory','存储':'Storage','文件':'File','数据':'Data','数据库':'Database','查询':'Query','缓存':'Cache',
'加密':'Encryption','哈希':'Hash','密钥':'Key','签名':'Signature','证书':'Certificate','权限':'Permission',
'星期':'Weekday','日历':'Calendar','日期':'Date','时区':'Timezone','本地':'Local','经度':'Longitude','纬度':'Latitude',
'距离':'Distance','速度':'Speed','时间':'Time','重量':'Weight','长度':'Length','宽度':'Width','高度':'Height',
'厚度':'Thickness','面积':'Area','体积':'Volume','周长':'Perimeter','直径':'Diameter','半径':'Radius','角度':'Angle',
'密度':'Density','浓度':'Concentration','比例':'Ratio','数量':'Quantity','尺寸':'Size','规格':'Spec','型号':'Model',
'品牌':'Brand','版本':'Version','特性':'Feature','参数':'Parameter','指标':'Metric','性能':'Performance',
'合格率':'Qualification rate','评分':'Score','判定':'Determination','结果':'Result','结论':'Conclusion',
'清单':'Checklist','明细':'Details','汇总':'Summary','分类':'Category','类型':'Type','说明':'Description','提示':'Hint',
'错误':'Error','成功':'Success','失败':'Failed','通过':'Pass','警告':'Warning','注意':'Note','开始':'Start','结束':'End',
'选项':'Option','设置':'Settings','模式':'Mode','状态':'Status','进度':'Progress','历史':'History','当前':'Current',
'全局':'Global','局部':'Local','静态':'Static','动态':'Dynamic','私有':'Private','公有':'Public','常量':'Constant',
'变量':'Variable','函数':'Function','方法':'Method','类':'Class','接口':'Interface','命名空间':'Namespace','表达式':'Expression',
'括号':'Parentheses','引号':'Quotes','空格':'Space','换行':'Line break','缩进':'Indentation','注释':'Comment',
'编译':'Compile','运行':'Run','调试':'Debug','测试':'Test','部署':'Deploy','构建':'Build','提交':'Commit',
'主机':'Host','节点':'Node','服务':'Service','容器':'Container','镜像':'Image','集群':'Cluster','负载':'Load',
'磁盘':'Disk','分区':'Partition','挂载':'Mount','备份':'Backup','恢复':'Restore','同步':'Sync','异步':'Async',
'线程':'Thread','进程':'Process','内存':'Memory','垃圾':'Garbage','回收':'Collection','锁':'Lock','事务':'Transaction',
}
# 单位后缀括号： （元） (元) -> (yuan) 等
UNIT_PAREN=re.compile(r'（(?:元|万元|亿|年|月|天|小时|分钟|秒|公里|米|吨|公里|平方米|立方|%)）|\((?:yuan|yr|mo|days|h|min|s|km|m|t)\)')
def xlate(s):
    if s.strip() in V: return V[s.strip()]
    keys=sorted(V.keys(), key=len, reverse=True)
    out=s
    for k in keys:
        if k and k in out:
            out=out.replace(k, V[k])
    # 括号单位
    out=out.replace('（元）','(yuan)').replace('（万元）','(10k yuan)').replace('（年）','(yr)').replace('（月）','(mo)').replace('（天）','(days)')
    out=out.replace('（小时）','(h)').replace('（分钟）','(min)').replace('（秒）','(s)').replace('（公里）','(km)').replace('（米）','(m)').replace('（吨）','(t)')
    out=re.sub(r'\s+',' ',out).strip()
    return out

prefix=json.load(open(os.path.join(ROOT,'i18n/tools/en/_prefix.json')))
added=0; skip=0
for s in cand:
    tr=xlate(s)
    if re.search(r'[一-鿿]', tr):
        skip+=1; continue
    if s in prefix: continue
    prefix[s]=tr; added+=1
json.dump(prefix, open(os.path.join(ROOT,'i18n/tools/en/_prefix.json'),'w'), ensure_ascii=False, indent=1)
print('candidates', len(cand), 'added', added, 'skipped(residual CJK)', skip, 'total', len(prefix))
