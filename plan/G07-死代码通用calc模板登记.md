# G07 · 死代码通用 `calc()` 模板登记（81 页）

## 背景

- 2026-11-04 全站重复定义扫描发现：81 页同时存在「通用模板 `calc()`」与「业务版 `calc()`」。通用模板在前、业务版在后，业务版生效，通用模板为死代码。
- 通用模板函数体约 17.8–19.2 KB，占页面体积约 36–40%，是 `own_len` 评级的重要来源。**删除会改变评级，本批暂不删除**，待集成线评估后再统一处置。
- 运行风险：无。本清单仅登记体积/维护债务；删除前必须重跑 `python3 _build.py` + `scripts/run_gates.py`，并复核 `own_len` 评级。

## 判定口径

- 通用模板特征：函数体内含 `分级|分型|分度|分层|风险|比例|比率|占比|百分比` 分支链与 `.test(title)`。
- 生效者：同页后定义的业务版 `calc()`（或其后包装器调用的业务实现）。
- 已抽查确认：81 页通用模板均在前、业务版在后，无「通用模板覆盖业务」案例；全站「最后一个 calc 是通用模板」= 0 页。

## 清单

| # | 页面 | 行号范围 | 函数体字节 | 页面字节 |
|---:|---|---:|---:|---:|
| 1 | `tools/ecommerce/calc-79.html` | 304–583 | 18049 | 48356 |
| 2 | `tools/ecommerce/calc-commission-2.html` | 198–476 | 17842 | 44206 |
| 3 | `tools/ecommerce/conversion-4.html` | 304–583 | 18051 | 48510 |
| 4 | `tools/ecommerce/discount.html` | 211–489 | 17842 | 50591 |
| 5 | `tools/ecommerce/erp-dingdan-caigou-duijie.html` | 304–583 | 18050 | 49117 |
| 6 | `tools/ecommerce/inventory-1.html` | 304–583 | 18058 | 48338 |
| 7 | `tools/ecommerce/kaidian-yunyingyuguizeduibijisuanqi.html` | 304–583 | 18059 | 49762 |
| 8 | `tools/ecommerce/kedan-jiandanjia-liandailv.html` | 304–583 | 18053 | 49958 |
| 9 | `tools/ecommerce/pingjia-chaping-tuihuo-lv.html` | 304–583 | 18051 | 49070 |
| 10 | `tools/ecommerce/response-2.html` | 304–583 | 18054 | 48325 |
| 11 | `tools/ecommerce/wuliu-fahuo-cangchu-gongyinglian-zhenghe.html` | 304–583 | 18056 | 50026 |
| 12 | `tools/ecommerce/wuliu-lanshou-qianshou-shixiao.html` | 304–583 | 18051 | 49356 |
| 13 | `tools/geology/duanceng-xingzhi-weiyi-huodongxing-panding.html` | 172–450 | 17842 | 45952 |
| 14 | `tools/geology/kengtan-chuanmai-yanmai-quyang-fangshi.html` | 201–479 | 17842 | 45782 |
| 15 | `tools/geology/sample-1.html` | 201–479 | 17842 | 44120 |
| 16 | `tools/geology/spacing-4.html` | 201–479 | 17842 | 44157 |
| 17 | `tools/hr/bandwidth-1.html` | 304–583 | 18061 | 50176 |
| 18 | `tools/hr/calc-81.html` | 314–593 | 18055 | 50555 |
| 19 | `tools/hr/eap-xinli-zixun-weiji-ziyuan.html` | 198–476 | 17842 | 44442 |
| 20 | `tools/hr/hris-zizhuyuaiduibijisuanqi.html` | 304–583 | 18073 | 49587 |
| 21 | `tools/hr/performance-ranking.html` | 213–508 | 19178 | 48021 |
| 22 | `tools/legal/calc-96.html` | 204–482 | 17842 | 45509 |
| 23 | `tools/legal/calculator-calc-6.html` | 204–482 | 17842 | 45540 |
| 24 | `tools/legal/feisu-ipo-simu-binggou-yewu.html` | 206–484 | 17842 | 46633 |
| 25 | `tools/legal/jicheng-yizhu-gongzheng-yichan-fenpei.html` | 204–482 | 17842 | 45837 |
| 26 | `tools/machinery/xiao-dingwei-lianjie-chicun.html` | 201–479 | 17842 | 45097 |
| 27 | `tools/machinery/zhineng-wurenyugaoxiaoduibijisuanqi.html` | 307–586 | 18067 | 49905 |
| 28 | `tools/machinery/zhujian-bamoxiedu-sheji.html` | 306–585 | 18061 | 49481 |
| 29 | `tools/metallurgy/calc-temp-1.html` | 300–579 | 18063 | 48414 |
| 30 | `tools/metallurgy/energy-1.html` | 198–476 | 17842 | 44969 |
| 31 | `tools/metallurgy/power-6.html` | 303–582 | 18061 | 49638 |
| 32 | `tools/metalwork/carbon-8.html` | 203–481 | 17842 | 45069 |
| 33 | `tools/metalwork/diandonggongju-xifen.html` | 309–588 | 18059 | 49382 |
| 34 | `tools/metalwork/laxue-ladao-chisheng-lali-sheji.html` | 308–587 | 18062 | 50350 |
| 35 | `tools/metalwork/tangxue-tangdao-tanggan-jingdu-kongzhi.html` | 203–481 | 17842 | 45908 |
| 36 | `tools/metalwork/wushua-zhinengyuqingliangduibijisuanqi.html` | 309–588 | 18067 | 50477 |
| 37 | `tools/metalwork/yuanlingongju-xifen.html` | 309–588 | 18061 | 49260 |
| 38 | `tools/metalwork/zhineng-duogongnengyunaiyongduibijisuanqi.html` | 312–591 | 18067 | 52030 |
| 39 | `tools/packaging/shousuomo-shousuolv-refeng-canshu.html` | 300–579 | 18063 | 49177 |
| 40 | `tools/packaging/strength-11.html` | 300–579 | 18067 | 48141 |
| 41 | `tools/packaging/strength-12.html` | 300–579 | 18059 | 48082 |
| 42 | `tools/paper/carbon-5.html` | 304–583 | 18059 | 48355 |
| 43 | `tools/paper/naipo-dingpo-zhishu.html` | 304–583 | 18063 | 48766 |
| 44 | `tools/paper/strength-10.html` | 304–583 | 18059 | 48375 |
| 45 | `tools/paper/strength-9.html` | 304–583 | 18062 | 48263 |
| 46 | `tools/procurement/wuliu-yunshufangshi-yunfei-bidui.html` | 198–476 | 17842 | 44538 |
| 47 | `tools/procurement/zhaobiao-gongkai-yaoqing-jingzheng-fangshi.html` | 198–476 | 17842 | 44992 |
| 48 | `tools/property/cost-profit.html` | 304–583 | 18055 | 48633 |
| 49 | `tools/property/energy.html` | 198–476 | 17842 | 43361 |
| 50 | `tools/property/response-1.html` | 198–476 | 17842 | 43494 |
| 51 | `tools/property/response-4.html` | 198–476 | 17842 | 43580 |
| 52 | `tools/railway/diaoche-zuoye-xiaolv-youhua.html` | 310–589 | 18063 | 48919 |
| 53 | `tools/railway/power-5.html` | 310–589 | 18062 | 47951 |
| 54 | `tools/realestate/calc-93.html` | 172–450 | 17842 | 44729 |
| 55 | `tools/realestate/calc-cost.html` | 307–586 | 18062 | 48811 |
| 56 | `tools/realestate/chiyou-qijianyunying-feiyong.html` | 307–586 | 18060 | 49947 |
| 57 | `tools/realestate/cost-depreciation-1.html` | 278–557 | 18057 | 50004 |
| 58 | `tools/realestate/cost-depreciation.html` | 278–557 | 18057 | 49717 |
| 59 | `tools/realestate/depreciation-2.html` | 201–479 | 17842 | 44461 |
| 60 | `tools/realestate/fangdichan-xintuo-jijinguzhi.html` | 307–586 | 18058 | 49970 |
| 61 | `tools/realestate/fund-loan-1.html` | 172–450 | 17842 | 44903 |
| 62 | `tools/realestate/paimai-baoliujia-qipaijia-sheding.html` | 201–479 | 17842 | 45668 |
| 63 | `tools/realestate/price-discount-1.html` | 307–586 | 18054 | 49171 |
| 64 | `tools/realestate/pv.html` | 172–450 | 17842 | 44292 |
| 65 | `tools/realestate/rent-1.html` | 172–450 | 17842 | 44504 |
| 66 | `tools/realestate/return-1.html` | 278–557 | 18057 | 49285 |
| 67 | `tools/realestate/yanglao-dichan-touzi-tuichu-jihui.html` | 307–586 | 18060 | 50240 |
| 68 | `tools/sports/baofali-zongtiao-lidingtiaoyuan.html` | 208–486 | 17842 | 46443 |
| 69 | `tools/sports/dianjiezhi-diushi-buchong.html` | 205–483 | 17842 | 44477 |
| 70 | `tools/sports/hongxibao-xieyang-shiyingxing.html` | 208–486 | 17842 | 46406 |
| 71 | `tools/sports/jianzhong-tuoshui-buye-kongzhi.html` | 205–483 | 17842 | 44650 |
| 72 | `tools/sports/jixianwei-kuai-man-leixingtuice.html` | 208–486 | 17842 | 46534 |
| 73 | `tools/sports/lingmin-zhefanpao-chengji.html` | 311–590 | 18058 | 48988 |
| 74 | `tools/sports/pingheng-biyandanjiao-shichang.html` | 205–483 | 17842 | 44738 |
| 75 | `tools/sports/pingpangqiu-xiangchi-faqiu-defen.html` | 212–490 | 17842 | 46675 |
| 76 | `tools/sports/rehab-motion.html` | 211–489 | 17842 | 45453 |
| 77 | `tools/sports/rouren-qianqu-cequ-jinbu.html` | 205–483 | 17842 | 44387 |
| 78 | `tools/sports/taiquandao-hengti-xiapi-defen.html` | 208–486 | 17842 | 46170 |
| 79 | `tools/surveying/area-24.html` | 214–492 | 17842 | 42968 |
| 80 | `tools/surveying/area-25.html` | 317–596 | 18061 | 47439 |
| 81 | `tools/surveying/calc-86.html` | 214–492 | 17842 | 43546 |

## 复扫命令

```bash
python3 - <<'PY'
# 重新提取：通用模板 calc() 行号范围与函数体字节
# 判定特征见上；同时确认同页存在更晚的业务版 calc()
PY
```


## 维护记录

- 2026-11-04：首次登记 81 页；只登记、不删除。
