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

## 评级账测算（2026-11-04，只做测算、未删任何代码）

> **结论先行**：剔除通用模板死代码后，81 页**仍全部为 A，0 页掉级，缺口 0 字**。但这不代表「死代码白占体积」：它占 `own_len` 的**中位 54.6%**，且这 81 页的真实可见正文**中位仅 950 汉字、无一页达到 1500 汉字** —— 这批 A 级是靠**脚本字节量**达标，不是靠正文丰实。

### 口径（与 `_build.py::classify_quality` 一致，逐页精确扣除）

- `own_len` = 非共享内联 `<script>` 字节 + 非共享 `<script type="module">` 字节 + 外置 `/js/tools/*.js` 文件字节；共享块按 md5 去重（`build_shared_script_index()`）。
- 剔除方式：按上表登记行号区间 `a–b`，用 `'\n'.join(lines[:a-1] + lines[b:])` 删除整段（含行尾），**逐页按真实行号扣除，非估算**。
- 判定：A = `(rich and own_len>=800) or own_len>=6000 or (own_len>=3000 and inputs>=3)`。本批 `inputs` 分布为 2 的 73 页、3 的 2 页、4 的 1 页、5 的 2 页、6/8/10 各 1 页。
- **单位提醒**：`own_len` 是**字节**，不是汉字；下文「缺口字数」按 A 门槛 `6000` 的同一字节口径计算。

### 汇总

| 指标 | 现状（含死模板） | 剔除后 |
|---|---:|---:|
| 页数 | 81 | 81 |
| 评级 A | 81 | 81 |
| **掉出 A** | — | **0** |
| `own_len` 最小 | 27,553 | 9,695 |
| `own_len` 中位 | 33,122 | 15,049 |
| `own_len` 最大 | 34,582 | 16,513 |
| `own_len` 均值 | 31,461.9 | 13,474.8 |
| `own_len` 合计 | 2,548,414 | 1,091,459 |
| 距 6000 阈值最近余量 | — | 3,695（`tools/surveying/area-24.html`） |
| 死模板字节合计 | 1,456,874（页均 17,986） | — |
| 死模板占页面体积 | 34.8%–41.6%（中位 37.6%） | — |
| 死模板占 `own_len` | 中位 54.6% | — |

> 注：`own_len` 合计下降 `1,456,955` 字节，与删除段字节合计 `1,456,874` 相差 81 字节（每页 1 字节，来自删除段与脚本区块的换行边界），非估算误差。

### 可见正文规模（剔除死模板 + 去共享脚本 + 去 `<script>`/`<style>` 后）

| 指标 | 最小 | 中位 | 最大 | 均值 |
|---|---:|---:|---:|---:|
| 汉字数 | 614 | 950 | 1,325 | 959.7 |
| 非空格字符数 | 1,293 | 1,665 | 2,231 | 1,707.4 |

- 汉字数分布：`<1000` **50 页**（61.7%）、`1000–1499` **31 页**（38.3%）、`≥1500` **0 页**。
- 这意味着「补真实内容」不是小工程：若以 3000 汉字为正文目标，需补 **165,261 汉字**（页均 2,040）；以 6000 汉字为目标需补 **408,261 汉字**（页均 5,040）。

### 逐页清单（81 页）

| # | 页面 | 现状 `own_len` | 剔除后 `own_len` | 是否掉出 A | 缺口字数 | 可见正文汉字 |
|---:|---|---:|---:|:---:|---:|---:|
| 1 | `tools/ecommerce/calc-79.html` | 33,122 | 15,057 | 否 | 0 | 1,097 |
| 2 | `tools/ecommerce/calc-commission-2.html` | 29,055 | 11,197 | 否 | 0 | 1,065 |
| 3 | `tools/ecommerce/conversion-4.html` | 33,275 | 15,208 | 否 | 0 | 1,080 |
| 4 | `tools/ecommerce/discount.html` | 33,897 | 16,039 | 否 | 0 | 1,274 |
| 5 | `tools/ecommerce/erp-dingdan-caigou-duijie.html` | 33,763 | 15,697 | 否 | 0 | 1,052 |
| 6 | `tools/ecommerce/inventory-1.html` | 33,253 | 15,179 | 否 | 0 | 1,093 |
| 7 | `tools/ecommerce/kaidian-yunyingyuguizeduibijisuanqi.html` | 34,140 | 16,065 | 否 | 0 | 1,102 |
| 8 | `tools/ecommerce/kedan-jiandanjia-liandailv.html` | 34,582 | 16,513 | 否 | 0 | 1,098 |
| 9 | `tools/ecommerce/pingjia-chaping-tuihuo-lv.html` | 33,769 | 15,702 | 否 | 0 | 1,083 |
| 10 | `tools/ecommerce/response-2.html` | 33,223 | 15,153 | 否 | 0 | 1,111 |
| 11 | `tools/ecommerce/wuliu-fahuo-cangchu-gongyinglian-zhenghe.html` | 34,401 | 16,329 | 否 | 0 | 1,122 |
| 12 | `tools/ecommerce/wuliu-lanshou-qianshou-shixiao.html` | 33,966 | 15,899 | 否 | 0 | 1,103 |
| 13 | `tools/geology/duanceng-xingzhi-weiyi-huodongxing-panding.html` | 29,855 | 11,997 | 否 | 0 | 1,046 |
| 14 | `tools/geology/kengtan-chuanmai-yanmai-quyang-fangshi.html` | 29,656 | 11,798 | 否 | 0 | 950 |
| 15 | `tools/geology/sample-1.html` | 28,488 | 10,630 | 否 | 0 | 934 |
| 16 | `tools/geology/spacing-4.html` | 28,551 | 10,693 | 否 | 0 | 1,017 |
| 17 | `tools/hr/bandwidth-1.html` | 34,166 | 16,089 | 否 | 0 | 1,066 |
| 18 | `tools/hr/calc-81.html` | 34,389 | 16,318 | 否 | 0 | 947 |
| 19 | `tools/hr/eap-xinli-zixun-weiji-ziyuan.html` | 29,192 | 11,334 | 否 | 0 | 825 |
| 20 | `tools/hr/hris-zizhuyuaiduibijisuanqi.html` | 34,062 | 15,973 | 否 | 0 | 896 |
| 21 | `tools/hr/performance-ranking.html` | 30,696 | 11,502 | 否 | 0 | 1,323 |
| 22 | `tools/legal/calc-96.html` | 27,777 | 9,919 | 否 | 0 | 1,325 |
| 23 | `tools/legal/calculator-calc-6.html` | 27,842 | 9,984 | 否 | 0 | 1,194 |
| 24 | `tools/legal/feisu-ipo-simu-binggou-yewu.html` | 29,095 | 11,237 | 否 | 0 | 1,234 |
| 25 | `tools/legal/jicheng-yizhu-gongzheng-yichan-fenpei.html` | 27,966 | 10,108 | 否 | 0 | 1,220 |
| 26 | `tools/machinery/xiao-dingwei-lianjie-chicun.html` | 29,272 | 11,414 | 否 | 0 | 796 |
| 27 | `tools/machinery/zhineng-wurenyugaoxiaoduibijisuanqi.html` | 34,091 | 16,008 | 否 | 0 | 802 |
| 28 | `tools/machinery/zhujian-bamoxiedu-sheji.html` | 33,919 | 15,842 | 否 | 0 | 983 |
| 29 | `tools/metallurgy/calc-temp-1.html` | 33,229 | 15,150 | 否 | 0 | 837 |
| 30 | `tools/metallurgy/energy-1.html` | 29,239 | 11,381 | 否 | 0 | 834 |
| 31 | `tools/metallurgy/power-6.html` | 33,075 | 14,998 | 否 | 0 | 1,216 |
| 32 | `tools/metalwork/carbon-8.html` | 28,722 | 10,864 | 否 | 0 | 1,105 |
| 33 | `tools/metalwork/diandonggongju-xifen.html` | 33,601 | 15,526 | 否 | 0 | 782 |
| 34 | `tools/metalwork/laxue-ladao-chisheng-lali-sheji.html` | 34,054 | 15,976 | 否 | 0 | 1,160 |
| 35 | `tools/metalwork/tangxue-tangdao-tanggan-jingdu-kongzhi.html` | 29,767 | 11,909 | 否 | 0 | 824 |
| 36 | `tools/metalwork/wushua-zhinengyuqingliangduibijisuanqi.html` | 34,228 | 16,145 | 否 | 0 | 870 |
| 37 | `tools/metalwork/yuanlingongju-xifen.html` | 33,571 | 15,494 | 否 | 0 | 825 |
| 38 | `tools/metalwork/zhineng-duogongnengyunaiyongduibijisuanqi.html` | 34,330 | 16,247 | 否 | 0 | 1,232 |
| 39 | `tools/packaging/shousuomo-shousuolv-refeng-canshu.html` | 34,036 | 15,957 | 否 | 0 | 846 |
| 40 | `tools/packaging/strength-11.html` | 33,274 | 15,191 | 否 | 0 | 798 |
| 41 | `tools/packaging/strength-12.html` | 33,215 | 15,140 | 否 | 0 | 837 |
| 42 | `tools/paper/carbon-5.html` | 33,178 | 15,103 | 否 | 0 | 962 |
| 43 | `tools/paper/naipo-dingpo-zhishu.html` | 33,549 | 15,470 | 否 | 0 | 818 |
| 44 | `tools/paper/strength-10.html` | 33,209 | 15,134 | 否 | 0 | 903 |
| 45 | `tools/paper/strength-9.html` | 33,183 | 15,105 | 否 | 0 | 906 |
| 46 | `tools/procurement/wuliu-yunshufangshi-yunfei-bidui.html` | 29,345 | 11,487 | 否 | 0 | 924 |
| 47 | `tools/procurement/zhaobiao-gongkai-yaoqing-jingzheng-fangshi.html` | 29,644 | 11,786 | 否 | 0 | 972 |
| 48 | `tools/property/cost-profit.html` | 33,278 | 15,207 | 否 | 0 | 815 |
| 49 | `tools/property/energy.html` | 28,291 | 10,433 | 否 | 0 | 851 |
| 50 | `tools/property/response-1.html` | 28,578 | 10,720 | 否 | 0 | 803 |
| 51 | `tools/property/response-4.html` | 28,543 | 10,685 | 否 | 0 | 812 |
| 52 | `tools/railway/diaoche-zuoye-xiaolv-youhua.html` | 33,854 | 15,775 | 否 | 0 | 907 |
| 53 | `tools/railway/power-5.html` | 33,127 | 15,049 | 否 | 0 | 877 |
| 54 | `tools/realestate/calc-93.html` | 28,461 | 10,603 | 否 | 0 | 1,000 |
| 55 | `tools/realestate/calc-cost.html` | 33,215 | 15,137 | 否 | 0 | 954 |
| 56 | `tools/realestate/chiyou-qijianyunying-feiyong.html` | 33,940 | 15,864 | 否 | 0 | 944 |
| 57 | `tools/realestate/cost-depreciation-1.html` | 33,731 | 15,658 | 否 | 0 | 1,011 |
| 58 | `tools/realestate/cost-depreciation.html` | 33,555 | 15,482 | 否 | 0 | 962 |
| 59 | `tools/realestate/depreciation-2.html` | 28,731 | 10,873 | 否 | 0 | 918 |
| 60 | `tools/realestate/fangdichan-xintuo-jijinguzhi.html` | 34,007 | 15,933 | 否 | 0 | 962 |
| 61 | `tools/realestate/fund-loan-1.html` | 28,695 | 10,837 | 否 | 0 | 998 |
| 62 | `tools/realestate/paimai-baoliujia-qipaijia-sheding.html` | 29,541 | 11,683 | 否 | 0 | 994 |
| 63 | `tools/realestate/price-discount-1.html` | 33,494 | 15,424 | 否 | 0 | 940 |
| 64 | `tools/realestate/pv.html` | 28,329 | 10,471 | 否 | 0 | 900 |
| 65 | `tools/realestate/rent-1.html` | 28,460 | 10,602 | 否 | 0 | 925 |
| 66 | `tools/realestate/return-1.html` | 33,202 | 15,129 | 否 | 0 | 1,009 |
| 67 | `tools/realestate/yanglao-dichan-touzi-tuichu-jihui.html` | 34,165 | 16,089 | 否 | 0 | 992 |
| 68 | `tools/sports/baofali-zongtiao-lidingtiaoyuan.html` | 29,349 | 11,491 | 否 | 0 | 1,062 |
| 69 | `tools/sports/dianjiezhi-diushi-buchong.html` | 29,124 | 11,266 | 否 | 0 | 681 |
| 70 | `tools/sports/hongxibao-xieyang-shiyingxing.html` | 29,368 | 11,510 | 否 | 0 | 1,065 |
| 71 | `tools/sports/jianzhong-tuoshui-buye-kongzhi.html` | 29,243 | 11,385 | 否 | 0 | 686 |
| 72 | `tools/sports/jixianwei-kuai-man-leixingtuice.html` | 29,351 | 11,493 | 否 | 0 | 1,201 |
| 73 | `tools/sports/lingmin-zhefanpao-chengji.html` | 33,792 | 15,718 | 否 | 0 | 655 |
| 74 | `tools/sports/pingheng-biyandanjiao-shichang.html` | 29,332 | 11,474 | 否 | 0 | 709 |
| 75 | `tools/sports/pingpangqiu-xiangchi-faqiu-defen.html` | 30,528 | 12,670 | 否 | 0 | 905 |
| 76 | `tools/sports/rehab-motion.html` | 29,716 | 11,858 | 否 | 0 | 854 |
| 77 | `tools/sports/rouren-qianqu-cequ-jinbu.html` | 28,994 | 11,136 | 否 | 0 | 771 |
| 78 | `tools/sports/taiquandao-hengti-xiapi-defen.html` | 29,144 | 11,286 | 否 | 0 | 1,130 |
| 79 | `tools/surveying/area-24.html` | 27,553 | 9,695 | 否 | 0 | 620 |
| 80 | `tools/surveying/area-25.html` | 31,959 | 13,882 | 否 | 0 | 723 |
| 81 | `tools/surveying/calc-86.html` | 27,852 | 9,994 | 否 | 0 | 614 |

### 两方案成本对比

#### 方案 A：删死模板 + 补真实内容到 A
- **按现行 `own_len` 门槛：需补 0 页、0 字**（剔除后 81/81 仍 A，最小值 9,695 仍高出阈值 3,695 字节）。
- **按「正文也达标」的新标准（超出 `classify_quality` 现行口径）**：81 页全部需要补写；补到 3000 汉字需 **165,261 汉字**（页均 2,040），补到 6000 汉字需 **408,261 汉字**（页均 5,040）。约等于重写 81 页正文，属独立大工程。
- 额外工程成本：删 1.46 MB 后必须重跑 `python3 _build.py`（`json/tools.json` 体积/评级字段、SW 版本戳）+ `scripts/run_gates.py`，并逐页复核 `own_len` 与 verify 用例。

#### 方案 B：删死模板 + 接受降级
- **实际降级 0 页**：A→B 0 页、A→C 0 页，掉级页数 **0**。
- **全站 A 级占比影响**：现状 `json/tools.json` 4705/4705 = 100%；删除后仍 4705/4705 = 100%，**影响 0.00 个百分点**。
- 收益：81 页合计减少 **1,456,874 字节**（页均 17,986 字节，占页面体积 34.8%–41.6%、中位 37.6%），首屏解析与传输成本确定下降；无评级风险。
- 代价：构建 + 门禁 + 逐页 verify 复跑；`it/` 类无此批页面，不涉及跨分类共享脚本。

### 建议

1. **优先方案 B**：收益确定（体积降 1.46 MB）、评级零变化，且能消除「死代码占 `own_len` 中位 54.6%」这一度量噪音，让 `own_len` 更接近真实自研量。
2. **单独正视内容债**：这批页 A 级靠脚本字节达标，可见正文中位 950 汉字。若产品目标是「A 级 = 内容丰实」，应另立批次按正文口径补内容（方案 A 的正文部分），**不要与删死模板混做**，否则无法归因体积收益与内容收益。
3. 无论 A/B，删除批次都必须：改完 **重跑 `_build.py`** → `run_gates.py` 全过 → 抽样 3–6 页真机点击验证（确保生效的是业务版 `calc()`，无 `Maximum call stack size exceeded`）。

### 复现命令

```bash
python3 - <<'PY'
import sys, os, re, json, hashlib, importlib.util
sys.path.insert(0, '.')
spec = importlib.util.spec_from_file_location('b', '_build.py')
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
shared = m.build_shared_script_index()

def own_len(content):
    o = 0
    for b in re.findall(r'<script>(.*?)</script>', content, re.S):
        if hashlib.md5(b.encode()).hexdigest() not in shared: o += len(b)
    for b in re.findall(r'<script type="module">(.*?)</script>', content, re.S):
        if hashlib.md5(b.encode()).hexdigest() not in shared: o += len(b)
    for src in re.findall(r'<script src="(/js/tools/[^"]+\.js)"', content):
        p = os.path.join(m.ROOT, src.lstrip('/'))
        try: o += len(open(p, encoding='utf-8').read())
        except OSError: pass
    return o

md = open('plan/G07-死代码通用calc模板登记.md', encoding='utf-8').read()
rows = re.findall(r'\| \d+ \| `(tools/[^`]+)` \| (\d+)–(\d+) \| \d+ \| \d+ \|', md)
for path, a, b in rows:
    lines = open(path, encoding='utf-8').read().split('\n')
    a, b = int(a), int(b)
    cut = '\n'.join(lines[:a-1] + lines[b:])
    print(path, own_len(open(path, encoding='utf-8').read()), own_len(cut))
PY
```

### 维护记录

- 2026-11-04：首次登记 81 页；只登记、不删除。
- 2026-11-04：追加评级账测算（现状 vs 剔除后 `own_len`、掉级/缺口、可见正文规模、方案 A/B 成本）；**未删任何代码**。
