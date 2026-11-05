# 第三层英文词典死键扫描（i18n/tools/en）

> 只读扫描，无页面/词典/构建产物改动；未跑 `_build.py`、未 push。

## 结论速览

- 有页面且有词典的工具页：**4819** 页
- 词典键总数：**169688**
- 死键总数：**11737**（占 6.9%）
- 高优先（`dead`，页面文本已改而词典未跟，英文态会显示中文）：**5164**
- 成因分布：`dead`（真漏翻）/ `dynamic`（动态拼接/结果值）/ `fragment`（原文被内联标签拆成多个文本节点）/ `harmless`（emoji 卡片名、纯英文键等无害冗余）

## 汇总（按行业目录分片）

| 目录 | 页数 | 键数 | 死键数 | 高优先 | dynamic | fragment | harmless |
|---|---|---|---|---|---|---|---|
| accessibility | 6 | 112 | 0 | 0 | 0 | 0 | 0 |
| accounting | 36 | 866 | 27 | 27 | 0 | 0 | 0 |
| acoustics | 28 | 586 | 5 | 5 | 0 | 0 | 0 |
| acupuncture | 23 | 649 | 4 | 2 | 2 | 0 | 0 |
| admin | 8 | 225 | 0 | 0 | 0 | 0 | 0 |
| advertising | 17 | 505 | 2 | 2 | 0 | 0 | 0 |
| aerospace | 38 | 977 | 24 | 8 | 14 | 2 | 0 |
| agriculture | 64 | 2590 | 246 | 120 | 99 | 13 | 14 |
| ai | 64 | 1634 | 307 | 305 | 0 | 0 | 2 |
| antiques | 7 | 235 | 2 | 2 | 0 | 0 | 0 |
| aquaculture | 6 | 161 | 12 | 1 | 10 | 1 | 0 |
| archaeology | 7 | 166 | 1 | 1 | 0 | 0 | 0 |
| astronomy | 24 | 885 | 21 | 16 | 4 | 1 | 0 |
| audio | 9 | 254 | 6 | 6 | 0 | 0 | 0 |
| audit | 6 | 117 | 0 | 0 | 0 | 0 | 0 |
| automotive | 59 | 2470 | 44 | 32 | 5 | 7 | 0 |
| baking | 9 | 350 | 2 | 0 | 1 | 1 | 0 |
| banking | 25 | 532 | 9 | 6 | 2 | 1 | 0 |
| beauty | 22 | 825 | 2 | 2 | 0 | 0 | 0 |
| beekeeping | 1 | 55 | 1 | 0 | 1 | 0 | 0 |
| biz | 69 | 2427 | 326 | 227 | 29 | 34 | 36 |
| bonding | 6 | 141 | 0 | 0 | 0 | 0 | 0 |
| bridge | 6 | 141 | 3 | 0 | 3 | 0 | 0 |
| cardiology | 23 | 1274 | 58 | 28 | 25 | 4 | 1 |
| ceramics | 7 | 214 | 1 | 1 | 0 | 0 | 0 |
| chemical | 15 | 489 | 24 | 13 | 8 | 3 | 0 |
| chemistry | 37 | 1002 | 37 | 11 | 21 | 3 | 2 |
| chess | 6 | 264 | 77 | 19 | 53 | 3 | 2 |
| chinese | 5 | 181 | 10 | 5 | 5 | 0 | 0 |
| chinese-cook | 7 | 253 | 0 | 0 | 0 | 0 | 0 |
| civil | 25 | 684 | 19 | 12 | 1 | 4 | 2 |
| cleaning | 10 | 383 | 3 | 2 | 0 | 1 | 0 |
| clinical-lab | 22 | 1069 | 120 | 52 | 55 | 13 | 0 |
| clinical-nursing | 26 | 1302 | 44 | 11 | 28 | 5 | 0 |
| cognition | 9 | 405 | 5 | 0 | 5 | 0 | 0 |
| construction | 37 | 1548 | 42 | 17 | 21 | 2 | 2 |
| cosmetic-derm | 33 | 1528 | 11 | 10 | 0 | 1 | 0 |
| daily-goods | 1 | 36 | 4 | 2 | 2 | 0 | 0 |
| dance | 8 | 329 | 0 | 0 | 0 | 0 | 0 |
| data | 22 | 501 | 10 | 10 | 0 | 0 | 0 |
| decor | 9 | 374 | 5 | 4 | 0 | 1 | 0 |
| dentistry | 23 | 1070 | 14 | 11 | 3 | 0 | 0 |
| dermatology | 24 | 1024 | 15 | 8 | 0 | 7 | 0 |
| design | 108 | 3784 | 605 | 184 | 315 | 103 | 3 |
| dyeing | 14 | 488 | 1 | 0 | 0 | 1 | 0 |
| dynamics | 24 | 518 | 6 | 5 | 0 | 1 | 0 |
| eco | 40 | 1042 | 34 | 25 | 3 | 6 | 0 |
| ecommerce | 24 | 798 | 68 | 40 | 16 | 12 | 0 |
| economics | 27 | 583 | 7 | 6 | 0 | 1 | 0 |
| edu | 44 | 2020 | 63 | 34 | 22 | 6 | 1 |
| edu2 | 5 | 108 | 6 | 3 | 0 | 3 | 0 |
| elderly | 12 | 439 | 0 | 0 | 0 | 0 | 0 |
| electrical | 36 | 1172 | 68 | 8 | 45 | 4 | 11 |
| electromagnetism | 26 | 576 | 0 | 0 | 0 | 0 | 0 |
| electronics | 22 | 756 | 21 | 5 | 14 | 2 | 0 |
| encode | 31 | 731 | 20 | 19 | 0 | 0 | 1 |
| endocrinology | 23 | 1345 | 5 | 4 | 1 | 0 | 0 |
| energy | 42 | 1257 | 58 | 24 | 27 | 5 | 2 |
| engineering | 12 | 267 | 13 | 9 | 3 | 0 | 1 |
| ent | 24 | 945 | 1 | 1 | 0 | 0 | 0 |
| exhibition | 7 | 219 | 0 | 0 | 0 | 0 | 0 |
| express | 1 | 40 | 4 | 4 | 0 | 0 | 0 |
| fengshui | 5 | 153 | 5 | 4 | 1 | 0 | 0 |
| film | 7 | 219 | 0 | 0 | 0 | 0 | 0 |
| finance | 115 | 5149 | 1262 | 638 | 549 | 74 | 1 |
| fire | 12 | 398 | 4 | 4 | 0 | 0 | 0 |
| fire-rescue | 40 | 1704 | 26 | 17 | 6 | 2 | 1 |
| fishery | 39 | 1282 | 83 | 58 | 15 | 10 | 0 |
| fitness | 38 | 1394 | 20 | 15 | 2 | 1 | 2 |
| floral | 7 | 334 | 0 | 0 | 0 | 0 | 0 |
| fluid | 24 | 466 | 12 | 11 | 0 | 1 | 0 |
| food | 24 | 858 | 2 | 2 | 0 | 0 | 0 |
| food-processing | 21 | 570 | 8 | 2 | 1 | 5 | 0 |
| food-testing | 26 | 925 | 6 | 6 | 0 | 0 | 0 |
| forensic-medicine | 20 | 1553 | 1 | 1 | 0 | 0 | 0 |
| forestry | 20 | 768 | 20 | 8 | 9 | 3 | 0 |
| forex | 5 | 207 | 0 | 0 | 0 | 0 | 0 |
| fun | 54 | 1907 | 282 | 171 | 20 | 18 | 73 |
| funeral | 7 | 316 | 0 | 0 | 0 | 0 | 0 |
| futures | 5 | 206 | 0 | 0 | 0 | 0 | 0 |
| gardening | 16 | 542 | 11 | 8 | 0 | 0 | 3 |
| gardening2 | 5 | 96 | 0 | 0 | 0 | 0 | 0 |
| gas | 12 | 410 | 2 | 1 | 1 | 0 | 0 |
| gastroenterology | 23 | 1205 | 60 | 29 | 24 | 7 | 0 |
| general | 55 | 1939 | 127 | 20 | 87 | 20 | 0 |
| geology | 37 | 1214 | 32 | 24 | 8 | 0 | 0 |
| geometry | 28 | 633 | 6 | 3 | 1 | 2 | 0 |
| glass | 5 | 173 | 0 | 0 | 0 | 0 | 0 |
| health | 40 | 2620 | 70 | 37 | 22 | 11 | 0 |
| healthcare | 36 | 1009 | 123 | 58 | 49 | 14 | 2 |
| hematology | 26 | 1168 | 18 | 15 | 3 | 0 | 0 |
| home | 7 | 131 | 0 | 0 | 0 | 0 | 0 |
| hotel | 8 | 287 | 0 | 0 | 0 | 0 | 0 |
| hr | 20 | 667 | 152 | 64 | 69 | 17 | 2 |
| hvac | 14 | 782 | 15 | 3 | 10 | 0 | 2 |
| hydraulic | 55 | 1898 | 71 | 25 | 39 | 7 | 0 |
| image | 15 | 611 | 5 | 1 | 4 | 0 | 0 |
| insurance | 30 | 716 | 25 | 22 | 0 | 3 | 0 |
| investment | 26 | 632 | 13 | 12 | 1 | 0 | 0 |
| it | 338 | 14247 | 3805 | 1050 | 2621 | 116 | 18 |
| jewelry | 7 | 228 | 2 | 2 | 0 | 0 | 0 |
| kids | 5 | 95 | 0 | 0 | 0 | 0 | 0 |
| kinematics | 25 | 509 | 0 | 0 | 0 | 0 | 0 |
| language | 18 | 643 | 54 | 10 | 33 | 11 | 0 |
| leather | 16 | 524 | 23 | 12 | 8 | 3 | 0 |
| legal | 48 | 2124 | 37 | 24 | 6 | 6 | 1 |
| legal2 | 5 | 100 | 0 | 0 | 0 | 0 | 0 |
| library | 8 | 200 | 12 | 1 | 9 | 2 | 0 |
| life | 70 | 2700 | 333 | 254 | 62 | 17 | 0 |
| livestock | 27 | 1023 | 26 | 5 | 15 | 6 | 0 |
| logistics | 16 | 510 | 3 | 3 | 0 | 0 | 0 |
| logistics2 | 5 | 205 | 22 | 4 | 10 | 8 | 0 |
| machinery | 77 | 2755 | 189 | 47 | 127 | 9 | 6 |
| manufacturing | 5 | 128 | 16 | 10 | 6 | 0 | 0 |
| maritime | 5 | 121 | 5 | 4 | 1 | 0 | 0 |
| marketing | 45 | 2073 | 80 | 19 | 59 | 2 | 0 |
| martial | 5 | 93 | 0 | 0 | 0 | 0 | 0 |
| materials | 41 | 1090 | 33 | 15 | 14 | 1 | 3 |
| math | 42 | 1158 | 65 | 23 | 37 | 3 | 2 |
| mechanical | 15 | 369 | 1 | 1 | 0 | 0 | 0 |
| media | 7 | 162 | 0 | 0 | 0 | 0 | 0 |
| medical | 15 | 663 | 30 | 13 | 16 | 1 | 0 |
| medical2 | 5 | 111 | 0 | 0 | 0 | 0 | 0 |
| metallurgy | 20 | 657 | 33 | 13 | 15 | 5 | 0 |
| metalwork | 39 | 1555 | 67 | 40 | 18 | 8 | 1 |
| meteorology | 42 | 1290 | 23 | 18 | 0 | 5 | 0 |
| metrology | 29 | 624 | 13 | 11 | 1 | 1 | 0 |
| mining | 13 | 467 | 7 | 2 | 4 | 1 | 0 |
| misc | 1 | 21 | 9 | 9 | 0 | 0 | 0 |
| misc2 | 1 | 24 | 11 | 11 | 0 | 0 | 0 |
| museum | 9 | 199 | 14 | 6 | 7 | 1 | 0 |
| music | 21 | 920 | 6 | 3 | 2 | 1 | 0 |
| nephrology | 24 | 1038 | 46 | 19 | 23 | 4 | 0 |
| neurology | 25 | 1496 | 47 | 6 | 41 | 0 | 0 |
| niche | 1 | 27 | 17 | 17 | 0 | 0 | 0 |
| nuclear | 28 | 599 | 10 | 10 | 0 | 0 | 0 |
| nutrition | 19 | 531 | 24 | 4 | 8 | 12 | 0 |
| obstetrics | 27 | 1399 | 17 | 15 | 1 | 1 | 0 |
| office | 7 | 142 | 0 | 0 | 0 | 0 | 0 |
| ophthalmology | 31 | 1279 | 19 | 12 | 6 | 1 | 0 |
| optical | 41 | 1577 | 15 | 14 | 0 | 1 | 0 |
| optics | 22 | 494 | 6 | 3 | 3 | 0 | 0 |
| packaging | 7 | 162 | 2 | 0 | 1 | 1 | 0 |
| paper | 13 | 397 | 2 | 0 | 0 | 2 | 0 |
| parenting | 7 | 147 | 0 | 0 | 0 | 0 | 0 |
| pediatrics | 24 | 986 | 57 | 23 | 29 | 3 | 2 |
| pet | 13 | 538 | 26 | 15 | 2 | 3 | 6 |
| pet-training | 5 | 101 | 1 | 0 | 1 | 0 | 0 |
| petrochem | 5 | 107 | 1 | 1 | 0 | 0 | 0 |
| photo | 31 | 704 | 26 | 23 | 0 | 3 | 0 |
| photo2 | 4 | 118 | 6 | 1 | 5 | 0 | 0 |
| plastic | 5 | 151 | 4 | 1 | 2 | 1 | 0 |
| pr | 13 | 518 | 5 | 1 | 2 | 2 | 0 |
| printing | 8 | 313 | 28 | 7 | 15 | 6 | 0 |
| process | 15 | 331 | 11 | 10 | 1 | 0 | 0 |
| procurement | 10 | 301 | 8 | 7 | 1 | 0 | 0 |
| project | 5 | 171 | 10 | 1 | 3 | 6 | 0 |
| property | 21 | 700 | 11 | 11 | 0 | 0 | 0 |
| psychiatry | 24 | 638 | 2 | 2 | 0 | 0 | 0 |
| psychology | 21 | 695 | 0 | 0 | 0 | 0 | 0 |
| pulmonology | 24 | 1040 | 37 | 11 | 25 | 1 | 0 |
| quality | 9 | 284 | 5 | 4 | 0 | 1 | 0 |
| quantum | 27 | 571 | 15 | 5 | 9 | 1 | 0 |
| railway | 2 | 55 | 0 | 0 | 0 | 0 | 0 |
| realestate | 54 | 1968 | 42 | 41 | 1 | 0 | 0 |
| rehabilitation | 22 | 1041 | 6 | 3 | 3 | 0 | 0 |
| rental | 9 | 265 | 1 | 1 | 0 | 0 | 0 |
| reproductive-medicine | 25 | 1176 | 13 | 11 | 0 | 2 | 0 |
| research | 9 | 316 | 29 | 16 | 8 | 5 | 0 |
| restaurant | 11 | 258 | 13 | 9 | 0 | 0 | 4 |
| rheumatology | 25 | 1342 | 10 | 9 | 1 | 0 | 0 |
| road | 7 | 254 | 0 | 0 | 0 | 0 | 0 |
| robotics | 28 | 588 | 25 | 15 | 6 | 4 | 0 |
| rubber | 5 | 142 | 1 | 0 | 0 | 1 | 0 |
| safety | 16 | 509 | 1 | 0 | 0 | 1 | 0 |
| sales | 10 | 314 | 3 | 2 | 0 | 1 | 0 |
| science | 92 | 3451 | 565 | 175 | 349 | 33 | 8 |
| securities | 36 | 975 | 14 | 13 | 0 | 1 | 0 |
| security | 12 | 518 | 4 | 4 | 0 | 0 | 0 |
| seismology | 5 | 200 | 6 | 1 | 5 | 0 | 0 |
| service | 5 | 86 | 0 | 0 | 0 | 0 | 0 |
| shipping | 5 | 178 | 2 | 1 | 1 | 0 | 0 |
| signal | 27 | 582 | 4 | 3 | 0 | 1 | 0 |
| sports | 75 | 2689 | 303 | 267 | 16 | 18 | 2 |
| stage | 5 | 173 | 1 | 0 | 0 | 1 | 0 |
| startup | 7 | 153 | 1 | 1 | 0 | 0 | 0 |
| statistics | 51 | 1130 | 32 | 31 | 0 | 1 | 0 |
| stats | 4 | 110 | 1 | 1 | 0 | 0 | 0 |
| structural | 26 | 530 | 6 | 6 | 0 | 0 | 0 |
| surveying | 43 | 1011 | 19 | 15 | 0 | 4 | 0 |
| tax | 31 | 778 | 23 | 13 | 0 | 10 | 0 |
| tcm-chemistry | 23 | 974 | 7 | 4 | 3 | 0 | 0 |
| tcm-diagnosis | 22 | 1071 | 1 | 1 | 0 | 0 | 0 |
| tcm-pharmacy | 22 | 915 | 0 | 0 | 0 | 0 | 0 |
| telecom | 10 | 286 | 13 | 5 | 8 | 0 | 0 |
| text | 13 | 327 | 14 | 3 | 11 | 0 | 0 |
| textile | 28 | 1129 | 9 | 5 | 4 | 0 | 0 |
| thermodynamics | 28 | 637 | 9 | 9 | 0 | 0 | 0 |
| transport | 16 | 504 | 4 | 0 | 0 | 4 | 0 |
| travel | 25 | 1015 | 9 | 5 | 3 | 1 | 0 |
| tunnel | 5 | 190 | 8 | 6 | 2 | 0 | 0 |
| urban | 7 | 280 | 0 | 0 | 0 | 0 | 0 |
| urology | 24 | 1054 | 29 | 6 | 23 | 0 | 0 |
| usedcar | 13 | 448 | 5 | 1 | 4 | 0 | 0 |
| video | 8 | 331 | 1 | 1 | 0 | 0 | 0 |
| wedding | 9 | 353 | 95 | 21 | 61 | 4 | 9 |
| welding | 22 | 761 | 42 | 13 | 24 | 2 | 3 |
| woodwork | 8 | 211 | 5 | 5 | 0 | 0 | 0 |
| woodworking | 5 | 97 | 0 | 0 | 0 | 0 | 0 |
| yi | 5 | 107 | 0 | 0 | 0 | 0 | 0 |
| **全站合计** | **4819** | **169688** | **11737** | **5164** | **5546** | **796** | **231** |

## 逐条清单（仅高优先 `dead`）

格式：`页面路径 : 死键原文 : 成因`。原文超过 160 字时截断并标注「…(+N字)」，完整键可在对应 `i18n/tools/en/<ind>/<slug>.json` 中按前缀检索。

- `dead`（高优先）：页面里找不到该原文，且不是动态/碎片/无害情形 —— 页面文本已改、词典没跟，英文态对应的新文本仍是中文；
- `dynamic`：键出现在 `<script>` 源串中（拼接模板）或呈数字/结果形态，运行时渲染文本与键不同；
- `fragment`：键只能作为某个文本节点的子串存在，原文被内联标签拆开，运行时精确匹配不到；
- `harmless`：含 emoji 的短卡片名或纯英文键，由其它字典/构建层管理，记录不修。
- 为避免文件失控，`dynamic`/`fragment`/`harmless` 只在各目录末尾列前 5 条样例，完整计数见汇总表。

### accounting（dead 27 / dynamic 0 / fragment 0 / harmless 0）

- `tools/accounting/amortization-intangible.html` : `年摊销 = (原值−残值)/年限` : dead
- `tools/accounting/assessor-risk-11.html` : `Z≥2.99为安全区，1.81-2.99为灰色区，Z<1.81为危险区` : dead
- `tools/accounting/asset-turnover.html` : `资产周转率 = 营收/总资产` : dead
- `tools/accounting/break-even-units.html` : `盈亏平衡量 = FC/(P−VC)` : dead
- `tools/accounting/calc-1.html` : `应纳增值税 = 销项税额 − 进项税额` : dead
- `tools/accounting/calc-2.html` : `预缴所得税 = 利润 × 税率` : dead
- `tools/accounting/contribution-margin.html` : `单位边际贡献 = 单价 − 单位变动成本` : dead
- `tools/accounting/current-ratio.html` : `流动比率 = 流动资产/流动负债` : dead
- `tools/accounting/days-payable-outstanding.html` : `DPO = 应付账款/营业成本 × 365` : dead
- `tools/accounting/days-sales-outstanding.html` : `DSO = 应收账款/营收 × 365` : dead
- `tools/accounting/debt-service-coverage.html` : `DSCR = OCF/债务偿付额` : dead
- `tools/accounting/debt-to-asset.html` : `资产负债率 = 负债总额/资产总额` : dead
- `tools/accounting/depreciation-declining.html` : `年折旧 = 账面净值 × 2/年限` : dead
- `tools/accounting/depreciation-straight.html` : `年折旧 = (原值−残值)/年限` : dead
- `tools/accounting/depreciation-syd.html` : `年折旧 = (原值−残值)×剩余年数/年数总和` : dead
- `tools/accounting/ebit.html` : `EBIT = 营收 − 营业成本 − 费用` : dead
- `tools/accounting/ebitda.html` : `EBITDA = EBIT + 折旧 + 摊销` : dead
- `tools/accounting/gross-margin.html` : `毛利率 = (收入−成本)/收入 × 100%` : dead
- `tools/accounting/gross-profit.html` : `毛利 = 营收 − 营业成本` : dead
- `tools/accounting/interest-coverage.html` : `利息保障倍数 = EBIT/利息费用` : dead
- `tools/accounting/inventory-days.html` : `DIO = 存货/营业成本 × 365` : dead
- `tools/accounting/inventory-turnover.html` : `存货周转率 = 销售成本/平均存货` : dead
- `tools/accounting/net-profit-margin.html` : `净利率 = 净利/收入 × 100%` : dead
- `tools/accounting/quick-ratio.html` : `速动比率 = (流动资产−存货)/流动负债` : dead
- `tools/accounting/roa-calc.html` : `ROA = 净利/总资产 × 100%` : dead
- `tools/accounting/roe-calc.html` : `ROE = 净利/净资产 × 100%` : dead
- `tools/accounting/working-capital.html` : `营运资金 = 流动资产 − 流动负债` : dead

### acoustics（dead 5 / dynamic 0 / fragment 0 / harmless 0）

- `tools/acoustics/critical-distance.html` : `r_c ≈ 0.057·√(Q·V/RT60)（公制近似）。 V=200、RT60=1、Q=1 → r_c≈2 m。` : dead
- `tools/acoustics/doppler-acoustic.html` : `声源趋近（f' = f·v / (v − v_s)）` : dead
- `tools/acoustics/intensity-inverse-square.html` : `声强衰减（I₂ = I₁·(r₁/r₂)²）` : dead
- `tools/acoustics/room-axial-mode.html` : `f_n = n·c/(2L)。 5 m 房间基模 ≈ 34.3 Hz。` : dead
- `tools/acoustics/wavelength-from-freq.html` : `λ = c/f。 1 kHz 在空气中 λ=0.343 m。` : dead

### acupuncture（dead 2 / dynamic 2 / fragment 0 / harmless 0）

- `tools/acupuncture/acupoint-location.html` : `「依据《灵枢·骨度》及全国统编教材骨度分寸折量标准，按患者实测体表长度换算取穴」按输入参数进行专业计算并输出结果。` : dead
- `tools/acupuncture/acupoint-location.html` : `患者肘横纹至腕横纹骨度 12 寸，实测 24cm，则 1 寸=2cm；取内关（腕上 2 寸）即腕横纹上 4cm 处，避免以医者手指代寸造成偏差。反算核对：若从腕横纹量到某处为 5cm，则 5 ÷ 2 = 2.5 寸，可据此判断该点是否在预期的 2 寸附近。` : dead

  其它成因样例（共 2 条，仅列前 5）：
  - `tools/acupuncture/acupoint-location.html` : `反算寸数有什么用？` : dynamic
  - `tools/acupuncture/acupoint-location.html` : `反算即把体表量得的厘米数除以每寸折量，换算成寸数，用于核对已取穴位是否偏移。不同分段的每寸折量并不相同，反算时须使用该段自身的实测长度。` : dynamic

### advertising（dead 2 / dynamic 0 / fragment 0 / harmless 0）

- `tools/advertising/estimate-cycle.html` : `回本周期 = CAC / (ARPU × 毛利率)，建议 < 12 个月` : dead
- `tools/advertising/tester-15.html` : `P 值 < α 时差异显著，建议采用更优方案` : dead

### aerospace（dead 8 / dynamic 14 / fragment 2 / harmless 0）

- `tools/aerospace/breguet-range.html` : `螺旋桨飞机航程公式。` : dead
- `tools/aerospace/delta-v-rocket.html` : `=300 s、初始质量 m₀=500 t、最终质量 m_f=100 t。Δv = 300×9.81×ln(500/100) = 2943×ln(5) = 2943×1.609 ≈ 4733 m/s ≈ 4.73 km/s。单级远不足入轨，需多级接力。` : dead
- `tools/aerospace/delta-v-rocket.html` : `标准重力加速度 9.80665 m/s²，仅作 Isp（秒）转排气速度的` : dead
- `tools/aerospace/flight-time.html` : `实际飞行时长 = (到达当地时刻 − 出发当地时刻) + (到达时区 − 出发时区)` : dead
- `tools/aerospace/flight-time.html` : `时差 = 到达时区 - 出发时区（向东为正，向西为负）` : dead
- `tools/aerospace/payload-fraction.html` : `有效载荷占比 = (m₀−m_f)/m₀ × 100%` : dead
- `tools/aerospace/rocket-delta-v.html` : `排气速度 v_e=2500 m/s、初始质量 m₀=100 t、末质量 m_f=20 t。Δv=2500×ln(100/20)=2500×ln(5)=2500×1.609≈4023 m/s ≈ 4.02 km/s。足以完成多数轨道转移段。` : dead
- `tools/aerospace/thrust-to-weight.html` : `推重比 = T/W` : dead

  其它成因样例（共 16 条，仅列前 5）：
  - `tools/aerospace/climb-rate.html` : `ROC=0（平飞极限）。` : fragment
  - `tools/aerospace/delta-v-rocket.html` : `⚠ 比冲 Isp 必须大于 0。` : dynamic
  - `tools/aerospace/delta-v-rocket.html` : `⚠ 初始质量 m₀ 必须大于 0。` : dynamic
  - `tools/aerospace/delta-v-rocket.html` : `⚠ 最终质量 m_f 必须大于 0（质量为 0 时对数发散）。` : dynamic
  - `tools/aerospace/delta-v-rocket.html` : `⚠ 最终质量 m_f 不能大于初始质量 m₀：推进剂消耗后质量只会减少。` : dynamic

### agriculture（dead 120 / dynamic 99 / fragment 13 / harmless 14）

- `tools/agriculture/agri-calculator.html` : `关于「农业计算器」` : dead
- `tools/agriculture/agri-calculator.html` : `农业计算器是做什么的？` : dead
- `tools/agriculture/agri-calculator.html` : `农业计算器适合哪些场景？` : dead
- `tools/agriculture/agri-calculator.html` : `农药稀释按有效成分还是制剂？` : dead
- `tools/agriculture/agri-calculator.html` : `农药稀释算例` : dead
- `tools/agriculture/agri-calculator.html` : `如何使用农业计算器？` : dead
- `tools/agriculture/agri-calculator.html` : `按目标配方中各养分占纯养分的百分比填写，如 15-15-15 表示 N 15%、P₂O₅ 15%、K₂O 15%；工具再按尿素/过磷酸钙/氯化钾等单质肥的有效含量折算实物用量。` : dead
- `tools/agriculture/agri-calculator.html` : `本页按制剂的「有效成分含量%」折算原药用量，ppm 指百万分之一，1 ppm ≈ 1 mg/L；配药前请以药品标签标注的浓度与安全间隔期为准。` : dead
- `tools/agriculture/agri-calculator.html` : `本页提供 6 个独立小工具：肥料配方折算、种植密度、农药稀释、灌溉用水量、孵化参数、农机油耗。` : dead
- `tools/agriculture/agri-calculator.html` : `目标浓度 1000 ppm、配药液量 30 L、原药有效成分 40% ⇒ 原药用量 = 1000 ppm × 30 L ÷ 40% = 75 g（1 ppm ≈ 1 mg/L，故 1000 ppm = 1 g/L）。配药时请按药品标签复核浓度与安全间隔期。` : dead
- `tools/agriculture/agri-calculator.html` : `种植密度面板按株距×行距折算每亩株数；灌溉面板按「面积×灌水深度×0.667」折算用水量。` : dead
- `tools/agriculture/agri-calculator.html` : `肥料面板按 N-P-K 比例与目标用量折算单质肥；农药面板按有效成分含量折算原药用量与稀释倍数。` : dead
- `tools/agriculture/agri-calculator.html` : `肥料面板的 N-P-K 比例怎么填？` : dead
- `tools/agriculture/agri-calculator.html` : `说明：本页不提供「投入产出/净收益」测算。若需估算净收益，请另行用「产量 × 单价 − 成本」手工计算或使用专门的盈亏平衡工具，避免把本页 6 个计算器误当作收益模型。` : dead
- `tools/agriculture/assessor-1.html` : `如何使用收获损失率（机器/人工）评估？` : dead
- `tools/agriculture/assessor-1.html` : `收获损失率（机器/人工）评估是做什么的？` : dead
- `tools/agriculture/assessor-1.html` : `收获损失率（机器/人工）评估适合哪些场景？` : dead
- `tools/agriculture/calc-12.html` : `如何使用灌溉用水量估算？` : dead
- `tools/agriculture/calc-12.html` : `灌溉用水量估算是做什么的？` : dead
- `tools/agriculture/calc-12.html` : `灌溉用水量估算适合哪些场景？` : dead
- `tools/agriculture/calc-13.html` : `农机油耗估算是做什么的？` : dead
- `tools/agriculture/calc-13.html` : `农机油耗估算适合哪些场景？` : dead
- `tools/agriculture/calc-13.html` : `如何使用农机油耗估算？` : dead
- `tools/agriculture/calc-15.html` : `如何使用播种日期计算器？` : dead
- `tools/agriculture/calc-15.html` : `播种日期计算器是做什么的？` : dead
- `tools/agriculture/calc-15.html` : `播种日期计算器适合哪些场景？` : dead
- `tools/agriculture/calc-2.html` : `关于「种植密度计算器（株距×行距）」` : dead
- `tools/agriculture/calc-2.html` : `如何使用种植密度计算器（株距×行距）？` : dead
- `tools/agriculture/calc-2.html` : `种植密度计算器（株距×行距）是做什么的？` : dead
- `tools/agriculture/calc-2.html` : `种植密度计算器（株距×行距）适合哪些场景？` : dead
- `tools/agriculture/calc-36.html` : `作物需水量（蒸腾蒸发ET）计算是做什么的？` : dead
- `tools/agriculture/calc-36.html` : `作物需水量（蒸腾蒸发ET）计算适合哪些场景？` : dead
- `tools/agriculture/calc-36.html` : `如何使用作物需水量（蒸腾蒸发ET）计算？` : dead
- `tools/agriculture/calc-37.html` : `光照累积量（每日光积分DLI）计算是做什么的？` : dead
- `tools/agriculture/calc-37.html` : `光照累积量（每日光积分DLI）计算适合哪些场景？` : dead
- `tools/agriculture/calc-37.html` : `如何使用光照累积量（每日光积分DLI）计算？` : dead
- `tools/agriculture/calc-38.html` : `如何使用灌溉均匀度（克里斯琴森系数）计算？` : dead
- `tools/agriculture/calc-38.html` : `灌溉均匀度（克里斯琴森系数）计算是做什么的？` : dead
- `tools/agriculture/calc-38.html` : `灌溉均匀度（克里斯琴森系数）计算适合哪些场景？` : dead
- `tools/agriculture/calc-6.html` : `养殖存栏量估算是做什么的？` : dead
- `tools/agriculture/calc-6.html` : `养殖存栏量估算适合哪些场景？` : dead
- `tools/agriculture/calc-6.html` : `如何使用养殖存栏量估算？` : dead
- `tools/agriculture/calc-7.html` : `如何使用水肥一体化滴灌配比调节？` : dead
- `tools/agriculture/calc-7.html` : `水肥一体化滴灌配比调节是做什么的？` : dead
- `tools/agriculture/calc-7.html` : `水肥一体化滴灌配比调节适合哪些场景？` : dead
- `tools/agriculture/calc-8.html` : `土壤pH值调节计算器是做什么的？` : dead
- `tools/agriculture/calc-8.html` : `土壤pH值调节计算器适合哪些场景？` : dead
- `tools/agriculture/calc-8.html` : `如何使用土壤pH值调节计算器？` : dead
- `tools/agriculture/calc-8.html` : `石灰用量(kg) =（目标 pH − 当前 pH）× 缓冲系数 × 面积` : dead
- `tools/agriculture/calc-ventilation-2.html` : `如何使用温室通风量（换气次数）计算？` : dead
- `tools/agriculture/calc-ventilation-2.html` : `温室通风量（换气次数）计算是做什么的？` : dead
- `tools/agriculture/calc-ventilation-2.html` : `温室通风量（换气次数）计算适合哪些场景？` : dead
- `tools/agriculture/calculator-calc-1.html` : `如何使用播种日期计算器（基于无霜期）？` : dead
- `tools/agriculture/calculator-calc-1.html` : `播种日期计算器（基于无霜期）是做什么的？` : dead
- `tools/agriculture/calculator-calc-1.html` : `播种日期计算器（基于无霜期）适合哪些场景？` : dead
- `tools/agriculture/calculator-calc-concentration.html` : `农药稀释浓度计算器是做什么的？` : dead
- `tools/agriculture/calculator-calc-concentration.html` : `农药稀释浓度计算器适合哪些场景？` : dead
- `tools/agriculture/calculator-calc-concentration.html` : `如何使用农药稀释浓度计算器？` : dead
- `tools/agriculture/calculator-calc-density.html` : `如何使用种植密度计算器（株距×行距）？` : dead
- `tools/agriculture/calculator-calc-density.html` : `种植密度计算器（株距×行距）是做什么的？` : dead
- `tools/agriculture/calculator-calc-density.html` : `种植密度计算器（株距×行距）适合哪些场景？` : dead
- `tools/agriculture/calculator-calc-ratio.html` : `如何使用肥料配比计算器（N-P-K比例）？` : dead
- `tools/agriculture/calculator-calc-ratio.html` : `肥料配比计算器（N-P-K比例）是做什么的？` : dead
- `tools/agriculture/calculator-calc-ratio.html` : `肥料配比计算器（N-P-K比例）适合哪些场景？` : dead
- `tools/agriculture/calculator-calc-ratio-1.html` : `如何使用饲料配比计算器（按营养成分）？` : dead
- `tools/agriculture/calculator-calc-ratio-1.html` : `饲料配比计算器（按营养成分）是做什么的？` : dead
- `tools/agriculture/calculator-calc-ratio-1.html` : `饲料配比计算器（按营养成分）适合哪些场景？` : dead
- `tools/agriculture/calculator-calc-soil.html` : `ΔpH = 目标 − 当前。升 pH 用石灰（以 CaCO₃ 当量计），质地系数按砂土 0.3、壤土 0.6、黏土 1.0、有机质土 1.6 取值，并以「耕层深度 ÷ 20 cm」做深度归一。降 pH 用硫磺，在石灰基准式上乘 0.4（纯 S 计）。同时给出石灰的 CaO、Ca(OH)₂ 折算量。ΔpH 绝对值小于 0…(+14字)` : dead
- `tools/agriculture/calculator-calc-soil.html` : `土壤pH值调节计算器（加硫或石灰）是做什么的？` : dead
- `tools/agriculture/calculator-calc-soil.html` : `土壤pH值调节计算器（加硫或石灰）适合哪些场景？` : dead
- `tools/agriculture/calculator-calc-soil.html` : `如何使用土壤pH值调节计算器（加硫或石灰）？` : dead
- `tools/agriculture/calculator-calc-soil.html` : `石灰(CaCO₃)用量 = ΔpH × 质地系数 × 面积 ÷ 100 × (耕层cm ÷ 20)；硫磺用量 = 同式 × 0.4（以纯 S 计）` : dead
- `tools/agriculture/calculator-calc-soil.html` : `石灰以 CaCO₃（碳酸钙）当量估算；若使用生石灰（CaO）或熟石灰 Ca(OH)₂，需按有效成分换算（CaO ≈ 1.78×CaCO₃；Ca(OH)₂ ≈ 1.35×CaCO₃）。` : dead
- `tools/agriculture/calculator-calc-soil.html` : `💡 计算原理：石灰用量 ≈ |目标pH − 当前pH| × 土壤质地系数 × 面积 × 深度系数；硫磺用量约为石灰当量的 1/3～1/2（按纯硫计）。` : dead
- `tools/agriculture/canopy-coverage.html` : `作物冠层覆盖度估算器是做什么的？` : dead
- `tools/agriculture/canopy-coverage.html` : `作物冠层覆盖度估算器适合哪些场景？` : dead
- `tools/agriculture/canopy-coverage.html` : `如何使用作物冠层覆盖度估算器？` : dead
- `tools/agriculture/convert-content-1.html` : `农产品干物质含量与水分换算是做什么的？` : dead
- `tools/agriculture/convert-content-1.html` : `农产品干物质含量与水分换算适合哪些场景？` : dead
- `tools/agriculture/convert-content-1.html` : `千农产品干物质含量` : dead
- `tools/agriculture/convert-content-1.html` : `千水分换算` : dead
- `tools/agriculture/convert-content-1.html` : `如何使用农产品干物质含量与水分换算？` : dead
- `tools/agriculture/convert-content-1.html` : `干物质 = 鲜重 × (1 − 含水率)。本工具按质量守恒在鲜重与干物质、不同含水率间换算，用于粮食与饲草贸易计价；换算基于干物质守恒。` : dead
- `tools/agriculture/convert-content-1.html` : `毫农产品干物质含量` : dead
- `tools/agriculture/convert-content-1.html` : `毫水分换算` : dead
- `tools/agriculture/countdown-4.html` : `如何使用鸡蛋孵化倒计时（21天）？` : dead
- `tools/agriculture/countdown-4.html` : `鸡蛋孵化倒计时（21天）是做什么的？` : dead
- `tools/agriculture/countdown-4.html` : `鸡蛋孵化倒计时（21天）适合哪些场景？` : dead
- `tools/agriculture/countdown-cycle.html` : `如何使用收获倒计时（按作物生长周期）？` : dead
- `tools/agriculture/countdown-cycle.html` : `收获倒计时（按作物生长周期）是做什么的？` : dead
- `tools/agriculture/countdown-cycle.html` : `收获倒计时（按作物生长周期）适合哪些场景？` : dead
- `tools/agriculture/crop-rotation.html` : `作物轮作周期规划表是做什么的？` : dead
- `tools/agriculture/crop-rotation.html` : `作物轮作周期规划表适合哪些场景？` : dead
- `tools/agriculture/crop-rotation.html` : `关于「作物轮作周期规划表」` : dead
- `tools/agriculture/crop-rotation.html` : `如何使用作物轮作周期规划表？` : dead
- `tools/agriculture/crop-water-requirement.html` : `作物需水量计算器是做什么的？` : dead
- `tools/agriculture/crop-water-requirement.html` : `作物需水量计算器适合哪些场景？` : dead
- `tools/agriculture/crop-water-requirement.html` : `如何使用作物需水量计算器？` : dead
- `tools/agriculture/crop-water-requirement.html` : `有效降雨量(mm/天)` : dead
- `tools/agriculture/crop-yield.html` : `作物产量估算器是做什么的？` : dead
- `tools/agriculture/crop-yield.html` : `作物产量估算器适合哪些场景？` : dead
- `tools/agriculture/crop-yield.html` : `如何使用作物产量估算器？` : dead
- `tools/agriculture/crop-yield.html` : `穗数法 亩产(kg) = 亩穗数(万穗) × 穗粒数 × 千粒重(g) ÷ 1 000 000；样方法 亩产 = 样方重量 × 干物质率 × 666.67 ÷ 样方面积；标准亩产 = 亩产 × (100 − 含水量) ÷ (100 − 13)` : dead
- `tools/agriculture/cycle-honey.html` : `下次摇蜜日 = 上次取蜜日 + 流蜜周期(天)；周期按 7~14 天校验` : dead
- `tools/agriculture/cycle-honey.html` : `如何使用采蜜期（摇蜜周期）安排？` : dead
- `tools/agriculture/cycle-honey.html` : `采蜜期（摇蜜周期）安排是做什么的？` : dead
- `tools/agriculture/cycle-honey.html` : `采蜜期（摇蜜周期）安排适合哪些场景？` : dead
- `tools/agriculture/detector-13.html` : `关于「蜂螨（寄生率）检测」` : dead
- `tools/agriculture/detector-13.html` : `如何使用蜂螨（寄生率）检测？` : dead
- `tools/agriculture/detector-13.html` : `蜂螨寄生率(%) = 检出螨数 ÷ 样本蜂数 × 100` : dead
- `tools/agriculture/detector-13.html` : `蜂螨（寄生率）检测是做什么的？` : dead
- `tools/agriculture/detector-13.html` : `蜂螨（寄生率）检测适合哪些场景？` : dead
- `tools/agriculture/detector-nutrition.html` : `关于「花粉（发酵）全营养检测」` : dead
- `tools/agriculture/detector-nutrition.html` : `如何使用花粉（发酵）全营养检测？` : dead
- `tools/agriculture/detector-nutrition.html` : `花粉（发酵）全营养检测是做什么的？` : dead
- `tools/agriculture/detector-nutrition.html` : `花粉（发酵）全营养检测适合哪些场景？` : dead
- `tools/agriculture/estimate-3.html` : `净灌水 = (ETc − Pe) × 面积 / 0.667（m³，Pe 为有效降雨 mm）。` : dead
- `tools/agriculture/machinery-efficiency.html` : `理论生产率 = 幅宽(m) × 速度(km/h) × 0.15 (亩/h)；实际生产率 = 理论 × 时间利用率%；工时 = 总面积 ÷ 实际生产率；成本/亩 = (油耗成本 + 人工成本) ÷ 总面积` : dead
- `tools/agriculture/machinery-efficiency.html` : `经验换算：幅宽 1 m、速度 1 km/h 约合 0.15 亩/h（由 1 km × 1 m = 1000 m² ≈ 1.5 亩、乘 0.001 h 系数得）。理论生产率乘时间利用率得实际生产率，再据总面积求工时；油耗按每小时油耗 × 工时 × 油价、人工按工时 × 人时费合计，折算为单位面积成本，用于多台农机横向比较…(+4字)` : dead
- `tools/agriculture/seed-germination-rate.html` : `100 粒供试，逐日发芽数 14/22/18/12/6/3/1，发芽率 64%。GI = 14/1 + 22/2 + 18/3 + 12/4 + 6/5 + 3/6 + 1/7 = 37.14，平均苗长 12 cm，活力指数 VI = 37.14 × 12 = 445.7。若发芽率仅 80% 则需提高播量（÷0.80）…(+3字)` : dead

  其它成因样例（共 126 条，仅列前 5）：
  - `tools/agriculture/agri-calculator.html` : `📚 深度解析：农业计算器` : harmless
  - `tools/agriculture/agri-calculator.html` : `📚 深度解析：农业生产常用计算` : harmless
  - `tools/agriculture/analysis-21.html` : `输入异常` : dynamic
  - `tools/agriculture/analysis-21.html` : `请输入 0–1 范围内的反射率（NIR、RED），且两者之和不能为 0` : dynamic
  - `tools/agriculture/analysis-21.html` : `请输入每行一组的「NIR,RED」（反射率 0–1）` : dynamic

### ai（dead 305 / dynamic 0 / fragment 0 / harmless 2）

- `tools/ai/ai.html` : `关于「分类准确率评估」` : dead
- `tools/ai/ai.html` : `分类准确率评估是做什么的？` : dead
- `tools/ai/ai.html` : `分类准确率评估适合哪些场景？` : dead
- `tools/ai/ai.html` : `如何使用分类准确率评估？` : dead
- `tools/ai/ai-10.html` : `Design CNN 时需逐层推算特征图尺寸，确保首尾维度匹配、不出现负数。` : dead
- `tools/ai/ai-10.html` : `关于「图像卷积输出尺寸」` : dead
- `tools/ai/ai-10.html` : `图像卷积输出尺寸是做什么的？` : dead
- `tools/ai/ai-10.html` : `图像卷积输出尺寸适合哪些场景？` : dead
- `tools/ai/ai-10.html` : `如何使用图像卷积输出尺寸？` : dead
- `tools/ai/ai-11.html` : `关于「过拟合诊断」` : dead
- `tools/ai/ai-11.html` : `如何使用过拟合诊断？` : dead
- `tools/ai/ai-11.html` : `过拟合诊断是做什么的？` : dead
- `tools/ai/ai-11.html` : `过拟合诊断适合哪些场景？` : dead
- `tools/ai/ai-11.html` : `过拟合：训练表现远好于验证表现` : dead
- `tools/ai/ai-12.html` : `Original 1000 张，施加翻转/旋转/色彩 3 类各 2 档共 8 种组合 → 等效≈1000×8=8000 张。若同一变换重复 3 次，有效增益远低于 3 倍，因样本高度相关。` : dead
- `tools/ai/ai-12.html` : `关于「数据增强有效量」` : dead
- `tools/ai/ai-12.html` : `如何使用数据增强有效量？` : dead
- `tools/ai/ai-12.html` : `数据增强有效量是做什么的？` : dead
- `tools/ai/ai-12.html` : `数据增强有效量适合哪些场景？` : dead
- `tools/ai/ai-12.html` : `有效量 ≈ 原始样本 × [1 + (aug − 1) × 多样性系数]` : dead
- `tools/ai/ai-12.html` : `理论扩充量 = 基数 × 增强倍数；有效等效量 = 基数 × [1 + (倍数 − 1) × 多样性系数]` : dead
- `tools/ai/ai-13.html` : `patience 决定模型在验证指标不改善时继续等待的 epoch 数` : dead
- `tools/ai/ai-13.html` : `关于「早停耐心估算」` : dead
- `tools/ai/ai-13.html` : `如何使用早停耐心估算？` : dead
- `tools/ai/ai-13.html` : `早停耐心估算是做什么的？` : dead
- `tools/ai/ai-13.html` : `早停耐心估算适合哪些场景？` : dead
- `tools/ai/ai-14.html` : `cos(q, d) = (q·d)/(‖q‖·‖d‖)，检索取 top-k 最大者` : dead
- `tools/ai/ai-14.html` : `关于「词嵌入余弦检索」` : dead
- `tools/ai/ai-14.html` : `如何使用词嵌入余弦检索？` : dead
- `tools/ai/ai-14.html` : `词嵌入余弦检索是做什么的？` : dead
- `tools/ai/ai-14.html` : `词嵌入余弦检索适合哪些场景？` : dead
- `tools/ai/ai-15.html` : `关于「贝叶斯后验概率」` : dead
- `tools/ai/ai-15.html` : `如何使用贝叶斯后验概率？` : dead
- `tools/ai/ai-15.html` : `贝叶斯后验概率是做什么的？` : dead
- `tools/ai/ai-15.html` : `贝叶斯后验概率适合哪些场景？` : dead
- `tools/ai/ai-16.html` : `关于「模型融合加权投票」` : dead
- `tools/ai/ai-16.html` : `如何使用模型融合加权投票？` : dead
- `tools/ai/ai-16.html` : `模型融合加权投票是做什么的？` : dead
- `tools/ai/ai-16.html` : `模型融合加权投票适合哪些场景？` : dead
- `tools/ai/ai-17.html` : `上下文占用 = 系统 + 历史 + 当前输入` : dead
- `tools/ai/ai-17.html` : `关于「提示词上下文窗口」` : dead
- `tools/ai/ai-17.html` : `如何使用提示词上下文窗口？` : dead
- `tools/ai/ai-17.html` : `提示词上下文窗口是做什么的？` : dead
- `tools/ai/ai-17.html` : `提示词上下文窗口适合哪些场景？` : dead
- `tools/ai/ai-4.html` : `关于「欧氏距离」` : dead
- `tools/ai/ai-4.html` : `如何使用欧氏距离？` : dead
- `tools/ai/ai-4.html` : `欧氏距离是做什么的？` : dead
- `tools/ai/ai-4.html` : `欧氏距离适合哪些场景？` : dead
- `tools/ai/ai-5.html` : `关于「批量大小迭代次数」` : dead
- `tools/ai/ai-5.html` : `如何使用批量大小迭代次数？` : dead
- `tools/ai/ai-5.html` : `批量大小迭代次数是做什么的？` : dead
- `tools/ai/ai-5.html` : `批量大小迭代次数适合哪些场景？` : dead
- `tools/ai/ai-6.html` : `关于「参数数量估算」` : dead
- `tools/ai/ai-6.html` : `参数数量估算是做什么的？` : dead
- `tools/ai/ai-6.html` : `参数数量估算适合哪些场景？` : dead
- `tools/ai/ai-6.html` : `如何使用参数数量估算？` : dead
- `tools/ai/ai-7.html` : `关于「混淆矩阵指标」` : dead
- `tools/ai/ai-7.html` : `如何使用混淆矩阵指标？` : dead
- `tools/ai/ai-7.html` : `混淆矩阵指标是做什么的？` : dead
- `tools/ai/ai-7.html` : `混淆矩阵指标适合哪些场景？` : dead
- `tools/ai/ai-8.html` : `关于「梯度下降一步」` : dead
- `tools/ai/ai-8.html` : `如何使用梯度下降一步？` : dead
- `tools/ai/ai-8.html` : `梯度下降一步是做什么的？` : dead
- `tools/ai/ai-8.html` : `梯度下降一步适合哪些场景？` : dead
- `tools/ai/ai-9.html` : `信息增益近似是做什么的？` : dead
- `tools/ai/ai-9.html` : `信息增益近似适合哪些场景？` : dead
- `tools/ai/ai-9.html` : `关于「信息增益近似」` : dead
- `tools/ai/ai-9.html` : `如何使用信息增益近似？` : dead
- `tools/ai/ai-code-review.html` : `AI 代码审查是做什么的？` : dead
- `tools/ai/ai-code-review.html` : `AI 代码审查适合哪些场景？` : dead
- `tools/ai/ai-code-review.html` : `如何使用AI 代码审查？` : dead
- `tools/ai/ai-prompt-generator.html` : `AI 提示词生成器是做什么的？` : dead
- `tools/ai/ai-prompt-generator.html` : `AI 提示词生成器适合哪些场景？` : dead
- `tools/ai/ai-prompt-generator.html` : `如何使用AI 提示词生成器？` : dead
- `tools/ai/ai-text-summarizer.html` : `AI 文本摘要是做什么的？` : dead
- `tools/ai/ai-text-summarizer.html` : `AI 文本摘要适合哪些场景？` : dead
- `tools/ai/ai-text-summarizer.html` : `如何使用AI 文本摘要？` : dead
- `tools/ai/attention-flops.html` : `关于「注意力计算量」` : dead
- `tools/ai/attention-flops.html` : `单层注意力 ≈ 2·S²·d(QKᵀ) + 2·S²·d(·V)` : dead
- `tools/ai/attention-flops.html` : `如何使用注意力计算量？` : dead
- `tools/ai/attention-flops.html` : `注意力计算量是做什么的？` : dead
- `tools/ai/attention-flops.html` : `注意力计算量适合哪些场景？` : dead
- `tools/ai/attention-head-dim.html` : `关于「注意力头维度」` : dead
- `tools/ai/attention-head-dim.html` : `如何使用注意力头维度？` : dead
- `tools/ai/attention-head-dim.html` : `每头维度 = d / heads；单层权重参数 ≈ 4d² + 2d·ffn` : dead
- `tools/ai/attention-head-dim.html` : `注意力头维度是做什么的？` : dead
- `tools/ai/attention-head-dim.html` : `注意力头维度适合哪些场景？` : dead
- `tools/ai/auc-rank.html` : `AUC 秩次估算是做什么的？` : dead
- `tools/ai/auc-rank.html` : `AUC 秩次估算适合哪些场景？` : dead
- `tools/ai/auc-rank.html` : `关于「AUC 秩次估算」` : dead
- `tools/ai/auc-rank.html` : `如何使用AUC 秩次估算？` : dead
- `tools/ai/augmentation-multiplier.html` : `Original 5000 张，旋转/翻转/色彩 3 类各 3 档共 9 组合 → 总量≈5000×9=45000 张。若叠加 2 次重复则≈90000，但有效增益低于 18 倍。` : dead
- `tools/ai/augmentation-multiplier.html` : `关于「数据增强倍数」` : dead
- `tools/ai/augmentation-multiplier.html` : `增强后总量 = 原始样本数 × (1 + 系数 × 变换种类数)` : dead
- `tools/ai/augmentation-multiplier.html` : `如何使用数据增强倍数？` : dead
- `tools/ai/augmentation-multiplier.html` : `总量 = 原始 ×(1 + 倍数 × 变换数)` : dead
- `tools/ai/augmentation-multiplier.html` : `按每种变换贡献的增量线性外推总量，系数反映单次变换的等效增益（通常 <1）。这是上界估计：变换间高度相关时实际有效量远小于此，且增强样本不能完全替代真实数据的分布覆盖。` : dead
- `tools/ai/augmentation-multiplier.html` : `数据增强倍数是做什么的？` : dead
- `tools/ai/augmentation-multiplier.html` : `数据增强倍数适合哪些场景？` : dead
- `tools/ai/best-epoch.html` : `关于「最佳轮次选择」` : dead
- `tools/ai/best-epoch.html` : `如何使用最佳轮次选择？` : dead
- `tools/ai/best-epoch.html` : `最佳轮次 = argmin(验证损失)；最小验证损失 = min(l₁…l₅)` : dead
- `tools/ai/best-epoch.html` : `最佳轮次 = loss 最小者` : dead
- `tools/ai/best-epoch.html` : `最佳轮次选择是做什么的？` : dead
- `tools/ai/best-epoch.html` : `最佳轮次选择适合哪些场景？` : dead
- `tools/ai/cohens-kappa.html` : `Cohen Kappa 系数是做什么的？` : dead
- `tools/ai/cohens-kappa.html` : `Cohen Kappa 系数适合哪些场景？` : dead
- `tools/ai/cohens-kappa.html` : `关于「Cohen Kappa 系数」` : dead
- `tools/ai/cohens-kappa.html` : `如何使用Cohen Kappa 系数？` : dead
- `tools/ai/context-window.html` : `上下文窗口占用是做什么的？` : dead
- `tools/ai/context-window.html` : `上下文窗口占用适合哪些场景？` : dead
- `tools/ai/context-window.html` : `关于「上下文窗口占用」` : dead
- `tools/ai/context-window.html` : `占用 = 系统+对话+回复；占用率 = 已用/上限` : dead
- `tools/ai/context-window.html` : `如何使用上下文窗口占用？` : dead
- `tools/ai/cosine-similarity.html` : `余弦相似度是做什么的？` : dead
- `tools/ai/cosine-similarity.html` : `余弦相似度适合哪些场景？` : dead
- `tools/ai/cosine-similarity.html` : `关于「余弦相似度」` : dead
- `tools/ai/cosine-similarity.html` : `如何使用余弦相似度？` : dead
- `tools/ai/cross-entropy.html` : `交叉熵损失是做什么的？` : dead
- `tools/ai/cross-entropy.html` : `交叉熵损失适合哪些场景？` : dead
- `tools/ai/cross-entropy.html` : `关于「交叉熵损失」` : dead
- `tools/ai/cross-entropy.html` : `单样本 L = −[y·ln p + (1 − y)·ln(1 − p)]；批量 L = 单样本 × n` : dead
- `tools/ai/cross-entropy.html` : `如何使用交叉熵损失？` : dead
- `tools/ai/dropout.html` : `Dropout 保留期望是做什么的？` : dead
- `tools/ai/dropout.html` : `Dropout 保留期望适合哪些场景？` : dead
- `tools/ai/dropout.html` : `关于「Dropout 保留期望」` : dead
- `tools/ai/dropout.html` : `如何使用Dropout 保留期望？` : dead
- `tools/ai/dropout.html` : `推理时缩放 1/(1−p)` : dead
- `tools/ai/dropout.html` : `期望输出 = x · (1 − p)` : dead
- `tools/ai/elbow-wcss.html` : `关于「手肘法 WCSS 降幅」` : dead
- `tools/ai/elbow-wcss.html` : `如何使用手肘法 WCSS 降幅？` : dead
- `tools/ai/elbow-wcss.html` : `手肘法 WCSS 降幅是做什么的？` : dead
- `tools/ai/elbow-wcss.html` : `手肘法 WCSS 降幅适合哪些场景？` : dead
- `tools/ai/elbow-wcss.html` : `降幅 = (WCSS(k) − WCSS(k+1))/WCSS(k)` : dead
- `tools/ai/epoch-time.html` : `关于「单轮训练时长」` : dead
- `tools/ai/epoch-time.html` : `单轮训练时长是做什么的？` : dead
- `tools/ai/epoch-time.html` : `单轮训练时长适合哪些场景？` : dead
- `tools/ai/epoch-time.html` : `如何使用单轮训练时长？` : dead
- `tools/ai/epoch-time.html` : `步数 = ⌈epochs×数据/批次⌉；时长 = 步数/吞吐` : dead
- `tools/ai/flops.html` : `关于「模型 flops 估算」` : dead
- `tools/ai/flops.html` : `如何使用模型 flops 估算？` : dead
- `tools/ai/flops.html` : `模型 flops 估算是做什么的？` : dead
- `tools/ai/flops.html` : `模型 flops 估算适合哪些场景？` : dead
- `tools/ai/grad-accumulation.html` : `关于「梯度累积步数」` : dead
- `tools/ai/grad-accumulation.html` : `如何使用梯度累积步数？` : dead
- `tools/ai/grad-accumulation.html` : `梯度累积步数是做什么的？` : dead
- `tools/ai/grad-accumulation.html` : `梯度累积步数适合哪些场景？` : dead
- `tools/ai/grad-accumulation.html` : `累积 = ⌈目标批次 /(单卡批次×GPU数)⌉` : dead
- `tools/ai/grad-accumulation.html` : `累积步数 = ⌈目标批量 / (单卡批量 × 卡数)⌉` : dead
- `tools/ai/image-classification.html` : `关于「图像分类识别」` : dead
- `tools/ai/image-classification.html` : `图像分类识别是做什么的？` : dead
- `tools/ai/image-classification.html` : `图像分类识别适合哪些场景？` : dead
- `tools/ai/image-classification.html` : `如何使用图像分类识别？` : dead
- `tools/ai/inference-throughput.html` : `Elapsed 秒` : dead
- `tools/ai/inference-throughput.html` : `关于「推理吞吐估算」` : dead
- `tools/ai/inference-throughput.html` : `吞吐 = tokens / 秒；单请求吞吐 = tokens / (秒 × 并发批量)` : dead
- `tools/ai/inference-throughput.html` : `吞吐 = tokens / 耗时；人均 = 吞吐 / 并发` : dead
- `tools/ai/inference-throughput.html` : `如何使用推理吞吐估算？` : dead
- `tools/ai/inference-throughput.html` : `推理吞吐估算是做什么的？` : dead
- `tools/ai/inference-throughput.html` : `推理吞吐估算适合哪些场景？` : dead
- `tools/ai/k-means.html` : `Inertia 估算 ≈ n·dim·spread²/k；每簇样本 ≈ ⌈n/k⌉` : dead
- `tools/ai/k-means.html` : `关于「聚类 K-Means 代价」` : dead
- `tools/ai/k-means.html` : `如何使用聚类 K-Means 代价？` : dead
- `tools/ai/k-means.html` : `聚类 K-Means 代价是做什么的？` : dead
- `tools/ai/k-means.html` : `聚类 K-Means 代价适合哪些场景？` : dead
- `tools/ai/l1-l2.html` : `L1 = λ₁·Σ|wᵢ|；L2 = λ₂·Σwᵢ²；总惩罚 = L1 + L2` : dead
- `tools/ai/l1-l2.html` : `L1 L2 正则化惩罚是做什么的？` : dead
- `tools/ai/l1-l2.html` : `L1 L2 正则化惩罚适合哪些场景？` : dead
- `tools/ai/l1-l2.html` : `关于「L1 L2 正则化惩罚」` : dead
- `tools/ai/l1-l2.html` : `如何使用L1 L2 正则化惩罚？` : dead
- `tools/ai/l1-l2-regularization.html` : `L1 范数 = Σ|wᵢ|；L2 范数 = √(Σwᵢ²)` : dead
- `tools/ai/l1-l2-regularization.html` : `L1/L2 正则项是做什么的？` : dead
- `tools/ai/l1-l2-regularization.html` : `L1/L2 正则项适合哪些场景？` : dead
- `tools/ai/l1-l2-regularization.html` : `关于「L1/L2 正则项」` : dead
- `tools/ai/l1-l2-regularization.html` : `如何使用L1/L2 正则项？` : dead
- `tools/ai/lr-decay.html` : `lr(epoch) = lr₀ × γ^epoch（指数衰减，γ<1）` : dead
- `tools/ai/lr-decay.html` : `关于「学习率衰减」` : dead
- `tools/ai/lr-decay.html` : `如何使用学习率衰减？` : dead
- `tools/ai/lr-decay.html` : `学习率衰减是做什么的？` : dead
- `tools/ai/lr-decay.html` : `学习率衰减适合哪些场景？` : dead
- `tools/ai/lr-warmup.html` : `warmup = 总步数 × 比例` : dead
- `tools/ai/lr-warmup.html` : `关于「学习率预热步数」` : dead
- `tools/ai/lr-warmup.html` : `如何使用学习率预热步数？` : dead
- `tools/ai/lr-warmup.html` : `学习率预热步数是做什么的？` : dead
- `tools/ai/lr-warmup.html` : `学习率预热步数适合哪些场景？` : dead
- `tools/ai/lr-warmup.html` : `预热步数 = 总步数 × 比例；预热末 LR = 峰值 LR` : dead
- `tools/ai/min-max.html` : `关于「特征缩放 Min-Max」` : dead
- `tools/ai/min-max.html` : `如何使用特征缩放 Min-Max？` : dead
- `tools/ai/min-max.html` : `特征缩放 Min-Max是做什么的？` : dead
- `tools/ai/min-max.html` : `特征缩放 Min-Max适合哪些场景？` : dead
- `tools/ai/model-accuracy.html` : `关于「模型准确率」` : dead
- `tools/ai/model-accuracy.html` : `准确率 = (TP+TN)/(TP+TN+FP+FN)×100%` : dead
- `tools/ai/model-accuracy.html` : `如何使用模型准确率？` : dead
- `tools/ai/model-accuracy.html` : `模型准确率是做什么的？` : dead
- `tools/ai/model-accuracy.html` : `模型准确率适合哪些场景？` : dead
- `tools/ai/multi-agent-overhead.html` : `关于「多智能体通信开销」` : dead
- `tools/ai/multi-agent-overhead.html` : `多智能体通信开销是做什么的？` : dead
- `tools/ai/multi-agent-overhead.html` : `多智能体通信开销适合哪些场景？` : dead
- `tools/ai/multi-agent-overhead.html` : `如何使用多智能体通信开销？` : dead
- `tools/ai/multi-agent-overhead.html` : `消息 = n·(n−1)·轮次（全连接）` : dead
- `tools/ai/multi-agent-overhead.html` : `消息总数 = n(n − 1) × 轮数；总流量 = 消息总数 × 单条大小` : dead
- `tools/ai/ocr.html` : `OCR 文字识别是做什么的？` : dead
- `tools/ai/ocr.html` : `OCR 文字识别适合哪些场景？` : dead
- `tools/ai/ocr.html` : `关于「OCR 文字识别」` : dead
- `tools/ai/ocr.html` : `如何使用OCR 文字识别？` : dead
- `tools/ai/precision-recall.html` : `关于「精确率与召回率」` : dead
- `tools/ai/precision-recall.html` : `如何使用精确率与召回率？` : dead
- `tools/ai/precision-recall.html` : `精确率与召回率是做什么的？` : dead
- `tools/ai/precision-recall.html` : `精确率与召回率适合哪些场景？` : dead
- `tools/ai/quantization-ratio.html` : `关于「量化压缩比」` : dead
- `tools/ai/quantization-ratio.html` : `压缩比 = 原位数 / 目标位数；模型大小(MB) ≈ 参数量 × 位数 / 8 / 1024²` : dead
- `tools/ai/quantization-ratio.html` : `压缩比 = 原字节/量化字节` : dead
- `tools/ai/quantization-ratio.html` : `如何使用量化压缩比？` : dead
- `tools/ai/quantization-ratio.html` : `量化压缩比是做什么的？` : dead
- `tools/ai/quantization-ratio.html` : `量化压缩比适合哪些场景？` : dead
- `tools/ai/rag.html` : `RAG 召回率是做什么的？` : dead
- `tools/ai/rag.html` : `RAG 召回率适合哪些场景？` : dead
- `tools/ai/rag.html` : `关于「RAG 召回率」` : dead
- `tools/ai/rag.html` : `如何使用RAG 召回率？` : dead
- `tools/ai/relu-leakyrelu.html` : `ReLU 与 LeakyReLU是做什么的？` : dead
- `tools/ai/relu-leakyrelu.html` : `ReLU 与 LeakyReLU适合哪些场景？` : dead
- `tools/ai/relu-leakyrelu.html` : `关于「ReLU 与 LeakyReLU」` : dead
- `tools/ai/relu-leakyrelu.html` : `如何使用ReLU 与 LeakyReLU？` : dead
- `tools/ai/rmse.html` : `关于「均方误差 RMSE」` : dead
- `tools/ai/rmse.html` : `均方误差 RMSE是做什么的？` : dead
- `tools/ai/rmse.html` : `均方误差 RMSE适合哪些场景？` : dead
- `tools/ai/rmse.html` : `如何使用均方误差 RMSE？` : dead
- `tools/ai/roc-auc.html` : `ROC AUC 近似是做什么的？` : dead
- `tools/ai/roc-auc.html` : `ROC AUC 近似适合哪些场景？` : dead
- `tools/ai/roc-auc.html` : `关于「ROC AUC 近似」` : dead
- `tools/ai/roc-auc.html` : `如何使用ROC AUC 近似？` : dead
- `tools/ai/sentiment-analysis.html` : `关于「情感分析」` : dead
- `tools/ai/sentiment-analysis.html` : `如何使用情感分析？` : dead
- `tools/ai/sentiment-analysis.html` : `情感分析是做什么的？` : dead
- `tools/ai/sentiment-analysis.html` : `情感分析适合哪些场景？` : dead
- `tools/ai/sigmoid.html` : `Sigmoid 输出是做什么的？` : dead
- `tools/ai/sigmoid.html` : `Sigmoid 输出适合哪些场景？` : dead
- `tools/ai/sigmoid.html` : `关于「Sigmoid 输出」` : dead
- `tools/ai/sigmoid.html` : `如何使用Sigmoid 输出？` : dead
- `tools/ai/softmax.html` : `Softmax 概率是做什么的？` : dead
- `tools/ai/softmax.html` : `Softmax 概率适合哪些场景？` : dead
- `tools/ai/softmax.html` : `关于「Softmax 概率」` : dead
- `tools/ai/softmax.html` : `如何使用Softmax 概率？` : dead
- `tools/ai/softmax-2.html` : `Pᵢ(T) = e^{zᵢ/T} / Σⱼ e^{zⱼ/T}；分布熵 H = −Σ Pᵢ ln Pᵢ` : dead
- `tools/ai/softmax-2.html` : `关于「温度缩放 Softmax」` : dead
- `tools/ai/softmax-2.html` : `如何使用温度缩放 Softmax？` : dead
- `tools/ai/softmax-2.html` : `温度缩放 Softmax是做什么的？` : dead
- `tools/ai/softmax-2.html` : `温度缩放 Softmax适合哪些场景？` : dead
- `tools/ai/specificity.html` : `关于「特异度计算」` : dead
- `tools/ai/specificity.html` : `如何使用特异度计算？` : dead
- `tools/ai/specificity.html` : `特异度 = TN/(TN+FP)` : dead
- `tools/ai/specificity.html` : `特异度计算是做什么的？` : dead
- `tools/ai/specificity.html` : `特异度计算适合哪些场景？` : dead
- `tools/ai/speech-to-text.html` : `关于「语音转文字」` : dead
- `tools/ai/speech-to-text.html` : `如何使用语音转文字？` : dead
- `tools/ai/speech-to-text.html` : `语音转文字是做什么的？` : dead
- `tools/ai/speech-to-text.html` : `语音转文字适合哪些场景？` : dead
- `tools/ai/steps-per-epoch.html` : `关于「每轮训练步数」` : dead
- `tools/ai/steps-per-epoch.html` : `如何使用每轮训练步数？` : dead
- `tools/ai/steps-per-epoch.html` : `步数 = ⌈数据/批次⌉` : dead
- `tools/ai/steps-per-epoch.html` : `每卡步数 = ⌈样本数 / 批量⌉；每步覆盖样本 = 批量 × 卡数` : dead
- `tools/ai/steps-per-epoch.html` : `每轮训练步数是做什么的？` : dead
- `tools/ai/steps-per-epoch.html` : `每轮训练步数适合哪些场景？` : dead
- `tools/ai/temperature-scaling.html` : `scaled = logit / T；T>1 更平滑，T<1 更尖锐` : dead
- `tools/ai/temperature-scaling.html` : `z′ = z/T（T>1 平滑分布，T<1 锐化分布）` : dead
- `tools/ai/temperature-scaling.html` : `关于「温度缩放 Logits」` : dead
- `tools/ai/temperature-scaling.html` : `如何使用温度缩放 Logits？` : dead
- `tools/ai/temperature-scaling.html` : `温度缩放 Logits是做什么的？` : dead
- `tools/ai/temperature-scaling.html` : `温度缩放 Logits适合哪些场景？` : dead
- `tools/ai/text-summarization.html` : `关于「文本摘要」` : dead
- `tools/ai/text-summarization.html` : `如何使用文本摘要？` : dead
- `tools/ai/text-summarization.html` : `文本摘要是做什么的？` : dead
- `tools/ai/text-summarization.html` : `文本摘要适合哪些场景？` : dead
- `tools/ai/token.html` : `Token 数量估算是做什么的？` : dead
- `tools/ai/token.html` : `Token 数量估算适合哪些场景？` : dead
- `tools/ai/token.html` : `关于「Token 数量估算」` : dead
- `tools/ai/token.html` : `如何使用Token 数量估算？` : dead
- `tools/ai/token-2.html` : `关于「提示词 Token 成本」` : dead
- `tools/ai/token-2.html` : `如何使用提示词 Token 成本？` : dead
- `tools/ai/token-2.html` : `提示词 Token 成本是做什么的？` : dead
- `tools/ai/token-2.html` : `提示词 Token 成本适合哪些场景？` : dead
- `tools/ai/token-2.html` : `费用 = Token 数 × 单价 / 1,000,000` : dead
- `tools/ai/token-usage.html` : `Token 用量估算是做什么的？` : dead
- `tools/ai/token-usage.html` : `Token 用量估算适合哪些场景？` : dead
- `tools/ai/token-usage.html` : `tokens ≈ 中文字数 / 1.5 + 英文词数 / 0.75 + 代码字符数` : dead
- `tools/ai/token-usage.html` : `中文≈字数/1.5，英文≈词数/0.75` : dead
- `tools/ai/token-usage.html` : `关于「Token 用量估算」` : dead
- `tools/ai/token-usage.html` : `如何使用Token 用量估算？` : dead
- `tools/ai/training-flops.html` : `C ≈ 6·N·D（Kaplan 估算）` : dead
- `tools/ai/training-flops.html` : `关于「训练算力需求」` : dead
- `tools/ai/training-flops.html` : `如何使用训练算力需求？` : dead
- `tools/ai/training-flops.html` : `训练算力需求是做什么的？` : dead
- `tools/ai/training-flops.html` : `训练算力需求适合哪些场景？` : dead
- `tools/ai/transformer-params.html` : `Transformer 参数量是做什么的？` : dead
- `tools/ai/transformer-params.html` : `Transformer 参数量适合哪些场景？` : dead
- `tools/ai/transformer-params.html` : `主体参数 ≈ 12·L·d²；嵌入参数 ≈ vocab × d` : dead
- `tools/ai/transformer-params.html` : `关于「Transformer 参数量」` : dead
- `tools/ai/transformer-params.html` : `如何使用Transformer 参数量？` : dead
- `tools/ai/transformer-params.html` : `近似 12·L·d²（含注意力与 FFN）` : dead
- `tools/ai/vram-estimate.html` : `关于「模型显存估算」` : dead
- `tools/ai/vram-estimate.html` : `如何使用模型显存估算？` : dead
- `tools/ai/vram-estimate.html` : `显存 ≈ 参数(十亿)×字节 + 激活开销` : dead
- `tools/ai/vram-estimate.html` : `权重显存 ≈ 参数量 × 每参数字节数；总显存 ≈ 权重 + 激活/1000` : dead
- `tools/ai/vram-estimate.html` : `模型显存估算是做什么的？` : dead
- `tools/ai/vram-estimate.html` : `模型显存估算适合哪些场景？` : dead

  其它成因样例（共 2 条，仅列前 5）：
  - `tools/ai/k-means.html` : `📚 深度解析：聚类 K-Means 代价` : harmless
  - `tools/ai/relu-leakyrelu.html` : `📚 深度解析：ReLU 与 LeakyReLU` : harmless

### antiques（dead 2 / dynamic 0 / fragment 0 / harmless 0）

- `tools/antiques/index.html` : `古董鉴定工具集合收录了 5 个免费在线工具，覆盖古董鉴定场景下的常见计算、换算与查询需求。无论你是相关领域的从业者、学生还是普通用户，都能在这里找到即用即走的实用小工具。所有工具纯前端运行，数据不上传服务器，保护隐私安全。` : dead
- `tools/antiques/rater-1.html` : `MS-70（完美未流通）` : dead

### aquaculture（dead 1 / dynamic 10 / fragment 1 / harmless 0）

- `tools/aquaculture/density-7.html` : `风险指数 = 运输时长 × 温度系数 × 密度系数 × 体重系数；预估存活率 = 100 − 风险指数 × 0.5；建议密度 = 1000 ÷ (时长 × 温度系数 × 体重系数) (kg/m³)` : dead

  其它成因样例（共 11 条，仅列前 5）：
  - `tools/aquaculture/area-power.html` : `理论曝气能耗（kW·h/次）` : dynamic
  - `tools/aquaculture/area-power.html` : `折算功率（kW）` : dynamic
  - `tools/aquaculture/area-power.html` : `台数按单台功率向上取整，增氧机应合理分布于池塘四周与中央。` : dynamic
  - `tools/aquaculture/area-power.html` : `请输入有效参数：面积、水深、溶氧提升量、单台功率需大于 0，曝气时长需在 0–24 小时。` : dynamic
  - `tools/aquaculture/density-7.html` : `按完整模型反解，该密度下预估存活率约 95%。` : dynamic

### archaeology（dead 1 / dynamic 0 / fragment 0 / harmless 0）

- `tools/archaeology/dating-method.html` : `提示：碳-14校正需用树轮校正曲线（如IntCal）；年轻样品（<300年）需注意"现代碳污染"，老样品（>3万年）受本底限制。` : dead

### astronomy（dead 16 / dynamic 4 / fragment 1 / harmless 0）

- `tools/astronomy/atmospheric-refraction.html` : `Bennett 近似在什么范围适用？` : dead
- `tools/astronomy/atmospheric-refraction.html` : `R = 1.02 / tan(h + 10.3/(h+5.11)) 角分（Bennett 近似）。` : dead
- `tools/astronomy/atmospheric-refraction.html` : `代入 Bennett 公式 R=1.02/tan(h+10.3/(h+5.11))（单位角分），h=30° 时括号内≈30.29°，tan≈0.5846，得 R≈1.02/0.5846≈1.74′。天体真实位置实际比观测视位置低约 1.74 角分。` : dead
- `tools/astronomy/atmospheric-refraction.html` : `单位通常为角分（′）或度（°）。地平线附近折射约 34′（≈0.57°），天顶处趋近 0。` : dead
- `tools/astronomy/atmospheric-refraction.html` : `在低高度角观测时，近地面大气使天体视高度被抬升，用 Bennett 近似估算折射量以修正望远镜指向。` : dead
- `tools/astronomy/atmospheric-refraction.html` : `真高度角 (°)` : dead
- `tools/astronomy/atmospheric-refraction.html` : `示例：真高度角 30° 时的大气折射` : dead
- `tools/astronomy/atmospheric-refraction.html` : `视线穿过的大气层路径随高度角降低而急剧变长，折射累积更大；高度角趋近 0° 时折射可达约 34′，接近一个太阳视直径。` : dead
- `tools/astronomy/atmospheric-refraction.html` : `近地面大气使天体视高度抬升（Bennett 近似，单位角分）。` : dead
- `tools/astronomy/convert-15.html` : `千地震震级` : dead
- `tools/astronomy/convert-15.html` : `千能量换算` : dead
- `tools/astronomy/convert-15.html` : `本工具按 Gutenberg-Richter 关系 log₁₀E=4.8+1.5M（E 单位焦耳）在里氏/矩震级与释放能量之间换算，并给出对应的 TNT 当量参考；纯前端本地换算，结果仅供科普估算。` : dead
- `tools/astronomy/convert-15.html` : `毫地震震级` : dead
- `tools/astronomy/convert-15.html` : `毫能量换算` : dead
- `tools/astronomy/convert-18.html` : `气压 P = P₀·(1 − h/44330)^5.255` : dead
- `tools/astronomy/convert-18.html` : `海拔 h = 44330·(1 − (P/P₀)^(1/5.255))` : dead

  其它成因样例（共 5 条，仅列前 5）：
  - `tools/astronomy/atmospheric-refraction.html` : `视高度角需填写 0–90° 的有效数值；留空、负数或超过 90° 不计算。` : dynamic
  - `tools/astronomy/atmospheric-refraction.html` : `修正后真高度角 (度)` : dynamic
  - `tools/astronomy/atmospheric-refraction.html` : `大气折射 R (′)` : dynamic
  - `tools/astronomy/atmospheric-refraction.html` : `折射（角秒）` : dynamic
  - `tools/astronomy/convert-15.html` : `地震震级` : fragment

### audio（dead 6 / dynamic 0 / fragment 0 / harmless 0）

- `tools/audio/audio-recorder.html` : `如何使用音频录制处理器` : dead
- `tools/audio/audio-recorder.html` : `如何使用音频录制处理器？` : dead
- `tools/audio/audio-recorder.html` : `音频录制处理器是做什么的？` : dead
- `tools/audio/audio-recorder.html` : `音频录制处理器适合哪些场景？` : dead
- `tools/audio/audio-recorder.html` : `音频录制处理器，在浏览器本地录制音频、调节音量与速度并可视化波形，纯前端运行、数据不上传，适合语音与素材处理。` : dead
- `tools/audio/index.html` : `音频工具工具集合收录了 7 个免费在线工具，覆盖音频工具场景下的常见计算、换算与查询需求。无论你是相关领域的从业者、学生还是普通用户，都能在这里找到即用即走的实用小工具。所有工具纯前端运行，数据不上传服务器，保护隐私安全。` : dead

### automotive（dead 32 / dynamic 5 / fragment 7 / harmless 0）

- `tools/automotive/brake-pad-life.html` : `位置系数：前轮 1.3（承担约 70% 制动负荷）｜后轮 0.7` : dead
- `tools/automotive/brake-pad-life.html` : `剩余可用厚度 = 当前厚度 − 极限厚度(3mm)` : dead
- `tools/automotive/brake-pad-life.html` : `剩余里程 = 剩余可用厚度 ÷ k × 10000` : dead
- `tools/automotive/brake-pad-life.html` : `基础预测率 = 片型系数 × 环境系数 × 习惯系数 × 位置系数` : dead
- `tools/automotive/brake-pad-life.html` : `实际磨损率 = (新厚度 − 当前厚度) ÷ (已行驶里程 ÷ 10000)  [mm/1000km]` : dead
- `tools/automotive/brake-pad-life.html` : `磨损率 k = max( 实际磨损率, 基础预测率 )` : dead
- `tools/automotive/cycle-belt.html` : `下次更换里程 = 上次更换里程 + 厂建议间隔里程` : dead
- `tools/automotive/cycle-belt.html` : `使用进度 = (当前里程 − 上次更换里程) ÷ 厂建议间隔里程 × 100%` : dead
- `tools/automotive/cycle-belt.html` : `剩余天数 = 剩余里程 ÷ 日均里程` : dead
- `tools/automotive/driver-license-validator.html` : `按常见州/地区规则校验号段长度与校验位，并解析可能的发证年份与发证地区` : dead
- `tools/automotive/fuel-anomaly.html` : `区间油耗 = 本次加油量 ÷ (本次里程 − 上次里程) × 100  [L/100km]` : dead
- `tools/automotive/fuel-anomaly.html` : `区间油费 = 加油量 × 油价` : dead
- `tools/automotive/fuel-anomaly.html` : `异常阈值 = 平均油耗 + 1.5 × σ（超阈即标红异常）` : dead
- `tools/automotive/fuel-anomaly.html` : `标准差 σ = √( Σ(区间油耗 − 平均油耗)² ÷ 期数 )` : dead
- `tools/automotive/fuel-converter.html` : `如何使用油耗换算？` : dead
- `tools/automotive/fuel-converter.html` : `油耗换算是做什么的？` : dead
- `tools/automotive/fuel-converter.html` : `油耗换算适合哪些场景？` : dead
- `tools/automotive/pressure-fuel-oil.html` : `λ 值 = AFR ÷ 理论空燃比(14.7)` : dead
- `tools/automotive/pressure-fuel-oil.html` : `单次喷油量 = 实际流量 × 喷油脉宽 ÷ 60000  [cc]` : dead
- `tools/automotive/pressure-fuel-oil.html` : `喷油占空比 = 喷油脉宽 ÷ 可用脉宽(120000 ÷ 转速) × 100%` : dead
- `tools/automotive/pressure-fuel-oil.html` : `总燃油流量 = 单次喷油量 × (缸数 ÷ 2) × 转速  [cc/min]` : dead
- `tools/automotive/pressure-fuel-oil.html` : `空气流量 = 排量 × (充气效率 ÷ 100) × (转速 ÷ 2) × 空气密度(1.225)` : dead
- `tools/automotive/pressure-fuel-oil.html` : `空燃比 AFR = 空气流量质量 ÷ 燃油流量质量` : dead
- `tools/automotive/pressure-fuel-oil.html` : `说明：喷油量与压差平方根成正比（轨压升高喷油量增加）；汽油理论空燃比 14.7:1，λ=1 为理想混合气，λ>1.1 偏稀、λ<0.9 偏浓。` : dead
- `tools/automotive/tire-wear.html` : `当前花纹深度 = 新胎深度 − 累计磨损` : dead
- `tools/automotive/tire-wear.html` : `每万km磨损量 = 基础磨损率 × 路况系数 × 驾驶系数 × 定位系数  [mm]` : dead
- `tools/automotive/voltage-1.html` : `发电机功率 = 发电机额定电流 × 系统电压` : dead
- `tools/automotive/voltage-1.html` : `含充电总电流 = 用电总电流 + 电池充电电流` : dead
- `tools/automotive/voltage-1.html` : `用电功率 = 用电总电流 × 系统电压` : dead
- `tools/automotive/voltage-1.html` : `用电总电流 = Σ各用电器电流` : dead
- `tools/automotive/voltage-1.html` : `负载率 = 含充电总电流 ÷ 发电机额定电流 × 100%` : dead
- `tools/automotive/voltage-1.html` : `💡 总负载率 = (用电总电流+充电电流) ÷ 发电机额定电流 × 100%；安全负载率应 < 80%` : dead

  其它成因样例（共 12 条，仅列前 5）：
  - `tools/automotive/brake-pad-life.html` : `剩余天数 = 剩余里程 ÷ (年均里程 ÷ 365)` : fragment
  - `tools/automotive/cycle-belt.html` : `剩余里程 = max(0, 下次更换里程 − 当前里程)` : fragment
  - `tools/automotive/cycle-belt.html` : `日均里程 = 年均里程 ÷ 365` : fragment
  - `tools/automotive/fuel-anomaly.html` : `每公里成本 = 区间油费 ÷ 区间里程` : fragment
  - `tools/automotive/fuel-anomaly.html` : `平均油耗 = Σ区间油耗 ÷ 期数` : fragment

### banking（dead 6 / dynamic 2 / fragment 1 / harmless 0）

- `tools/banking/bond-current-yield.html` : `当前收益率 = 年息/价格` : dead
- `tools/banking/bond-current-yield.html` : `当前收益率=年息÷市价，年息=面值×票息率。折价买入（市价<面值）时高于票息率，溢价买入时低于票息率；不含资本利得与期限因素。` : dead
- `tools/banking/debt-to-income.html` : `DTI = 月债/月收 × 100%` : dead
- `tools/banking/debt-to-income.html` : `DTI 一般建议 <43%。` : dead
- `tools/banking/loan-to-value.html` : `LTV = 贷款/抵押物价值 × 100%` : dead
- `tools/banking/tax-equivalent-yield.html` : `TEY = 免税收益/(1−税率)` : dead

  其它成因样例（共 3 条，仅列前 5）：
  - `tools/banking/apy-calculator.html` : `名义年利率 r` : fragment
  - `tools/banking/apy-calculator.html` : `⚠ 年复利次数 n 必须为正整数（如 12 表示每月复利）。` : dynamic
  - `tools/banking/apy-calculator.html` : `⚠ 名义年利率 r 必须大于 −1（即 −100%）；r 按小数口径填写（0.05 = 5%）。` : dynamic

### beauty（dead 2 / dynamic 0 / fragment 0 / harmless 0）

- `tools/beauty/skin-tewl.html` : `按经皮失水率分级：正常 < 10、轻度受损 10–20、重度 > 20 g/(m²·h)。问卷按紧绷、脱屑、刺痛频次映射到区间，高值提示屏障受损，需神经酰胺修护并暂停刷酸。` : dead
- `tools/beauty/skincare-routine.html` : `高浓度原型VC（pH<3.5）+烟酰胺 = 可能转化为烟酸刺激皮肤` : dead

### biz（dead 227 / dynamic 29 / fragment 34 / harmless 36）

- `tools/biz/assessor-risk-8.html` : `Mass（服务标准/检查/改进）` : dead
- `tools/biz/assessor-risk-8.html` : `质量（服务标准/检查/改进）` : dead
- `tools/biz/barcode-generator.html` : `关于「条形码生成器」` : dead
- `tools/biz/checker-8.html` : `四个维度权重合计 100%，流程权重最高是因为服务交付过程最容易被抽查取证。响应时间属逆向指标（越小越好），必须先折算成百分制得分才能与其他比率型指标求平均，否则"越小越好"会被算成"越低越差"。投诉次数超过 5 次后每次扣 3 分，属超额惩罚而非线性扣分，模拟"容忍阈值"管理惯例；满意度得分下限截为 0 避免负分抵消…(+46字)` : dead
- `tools/biz/checker-8.html` : `风险（排查/评估/防控）措施` : dead
- `tools/biz/fancy-text.html` : `如何使用装饰文字？` : dead
- `tools/biz/fancy-text.html` : `装饰文字是做什么的？` : dead
- `tools/biz/fancy-text.html` : `装饰文字适合哪些场景？` : dead
- `tools/biz/fullwidth-halfwidth.html` : `Unicode 只有片假名有半角码位（ｱｲｳ…），平假名（あいう）没有半角形式。勾选假名后：转半角把全角片假名（ア/ガ）转成半角（ｱ/ｶﾞ），转全角把半角片假名合成全角片假名；平假名始终原样保留。` : dead
- `tools/biz/fullwidth-halfwidth.html` : `假名项和「全角转半角」是什么关系？` : dead
- `tools/biz/fullwidth-halfwidth.html` : `假名（仅日文）` : dead
- `tools/biz/fullwidth-halfwidth.html` : `全角半角互转是做什么的？` : dead
- `tools/biz/fullwidth-halfwidth.html` : `全角半角互转适合哪些场景？` : dead
- `tools/biz/fullwidth-halfwidth.html` : `如何使用全角半角互转？` : dead
- `tools/biz/lorem-ipsum-advanced.html` : `/ 高级 Lorem Ipsum 生成器` : dead
- `tools/biz/lorem-ipsum-advanced.html` : `如何使用高级 Lorem Ipsum 生成器？` : dead
- `tools/biz/lorem-ipsum-advanced.html` : `高级 Lorem Ipsum 生成器是做什么的？` : dead
- `tools/biz/lorem-ipsum-advanced.html` : `高级 Lorem Ipsum 生成器适合哪些场景？` : dead
- `tools/biz/markdown.html` : `/ Markdown 实时预览` : dead
- `tools/biz/markdown.html` : `Markdown 实时预览是做什么的？` : dead
- `tools/biz/markdown.html` : `Markdown 实时预览适合哪些场景？` : dead
- `tools/biz/markdown.html` : `如何使用Markdown 实时预览？` : dead
- `tools/biz/meeting-cost-calculator.html` : `会议成本计算器是做什么的？` : dead
- `tools/biz/meeting-cost-calculator.html` : `会议成本计算器适合哪些场景？` : dead
- `tools/biz/meeting-cost-calculator.html` : `如何使用会议成本计算器？` : dead
- `tools/biz/motto-generator.html` : `如何使用座右铭生成器？` : dead
- `tools/biz/motto-generator.html` : `座右铭生成器是做什么的？` : dead
- `tools/biz/motto-generator.html` : `座右铭生成器适合哪些场景？` : dead
- `tools/biz/name-generator.html` : `中文名长度由风格字库决定（多为 1~2 字），页面不提供中文名字数设置；游戏 ID 标签页可设置字符长度。` : dead
- `tools/biz/name-generator.html` : `随机名字生成器适合哪些场景？` : dead
- `tools/biz/presentation-timer.html` : `Current ：第` : dead
- `tools/biz/presentation-timer.html` : `如何使用演讲计时器？` : dead
- `tools/biz/presentation-timer.html` : `演讲计时器是做什么的？` : dead
- `tools/biz/presentation-timer.html` : `演讲计时器适合哪些场景？` : dead
- `tools/biz/product-name-generator.html` : `产品名生成器是做什么的？` : dead
- `tools/biz/product-name-generator.html` : `产品名生成器适合哪些场景？` : dead
- `tools/biz/product-name-generator.html` : `如何使用产品名生成器？` : dead
- `tools/biz/random-script.html` : `如何使用标准话术模板随机抽取器？` : dead
- `tools/biz/random-script.html` : `标准话术模板随机抽取器是做什么的？` : dead
- `tools/biz/random-script.html` : `标准话术模板随机抽取器适合哪些场景？` : dead
- `tools/biz/simplified-traditional.html` : `如何使用简繁转换？` : dead
- `tools/biz/simplified-traditional.html` : `简繁转换是做什么的？` : dead
- `tools/biz/simplified-traditional.html` : `简繁转换适合哪些场景？` : dead
- `tools/biz/small-caps.html` : `如何使用小型大写字母？` : dead
- `tools/biz/small-caps.html` : `小型大写字母是做什么的？` : dead
- `tools/biz/small-caps.html` : `小型大写字母适合哪些场景？` : dead
- `tools/biz/stats-time-response.html` : `20 个工单响应时长均值 26 分钟、中位数 9 分钟、最大值 210 分钟；中位数更能代表常态体验，那几条超长工单应单独排查（如夜间无人值守）。` : dead
- `tools/biz/stats-time-response.html` : `判断整体响应水平。` : dead
- `tools/biz/stats-time-response.html` : `十几条样本的标准差本身波动很大，建议至少积累一个完整周期（如一周）的数据再下结论，并保留原始数据便于事后核对。` : dead
- `tools/biz/stats-time-response.html` : `均值被少数超长工单拉高` : dead
- `tools/biz/stats-time-response.html` : `如何使用客服平均响应时间/解决率统计？` : dead
- `tools/biz/stats-time-response.html` : `客服平均响应时间/解决率统计是做什么的？` : dead
- `tools/biz/stats-time-response.html` : `客服平均响应时间/解决率统计适合哪些场景？` : dead
- `tools/biz/stats-time-response.html` : `对比两个班组或两个月份的响应分布，结合达标率与标准差看服务稳定性。` : dead
- `tools/biz/stats-time-response.html` : `对比两个班组或两个月份的响应时长分布，用极差与` : dead
- `tools/biz/stats-time-response.html` : `平均响应 = Σ 单次时长 / 次数　·　达标率 = (≤ 阈值次数 / 总次数) × 100%` : dead
- `tools/biz/stats-time-response.html` : `必须统一。混贴秒与分钟会让均值和标准差完全失真，建议先换算成同一单位（推荐分钟）再贴入。` : dead
- `tools/biz/stats-time-response.html` : `把一天内所有工单的首次响应时长（分钟）贴入，用均值与` : dead
- `tools/biz/stats-time-response.html` : `把客服首响（或平均响应）时长逐条录入，计算平均响应时间、中位数与达标率，并给出最长/最短响应，用于服务 SLA 达成情况复盘；数据仅在浏览器本地处理，不上传。` : dead
- `tools/biz/stats-time-response.html` : `抽检已解决工单的处理耗时，估算解决率与平均处理时长的匹配关系。` : dead
- `tools/biz/stats-time-response.html` : `改版前后对比` : dead
- `tools/biz/stats-time-response.html` : `改版前标准差 34、改版后 12，均值均由 20 降到 15；波动收窄说明流程改动确实生效，而不只是恰好遇到简单工单。` : dead
- `tools/biz/stats-time-response.html` : `贴入一天内所有工单的首次响应时长（秒），用均值、中位数与 P90 判断整体时效；P90 比均值更能反映长尾体验。` : dead
- `tools/biz/stats-time-response.html` : `页面只做数值统计、不区分指标类型；建议分两批输入（一批响应时长、一批是否解决的 1/0），分别取均值，后者均值即解决率。` : dead
- `tools/biz/strawberry-text.html` : `如何使用草莓文字？` : dead
- `tools/biz/strawberry-text.html` : `草莓文字是做什么的？` : dead
- `tools/biz/strawberry-text.html` : `草莓文字适合哪些场景？` : dead
- `tools/biz/summary-rater-csat.html` : `如何使用客户满意度（CSAT）评分汇总？` : dead
- `tools/biz/summary-rater-csat.html` : `客户满意度（CSAT）评分汇总是做什么的？` : dead
- `tools/biz/summary-rater-csat.html` : `客户满意度（CSAT）评分汇总适合哪些场景？` : dead
- `tools/biz/team-roster-generator.html` : `关于「随机分组」` : dead
- `tools/biz/team-roster-generator.html` : `如何使用随机分组？` : dead
- `tools/biz/team-roster-generator.html` : `随机分组是做什么的？` : dead
- `tools/biz/team-roster-generator.html` : `随机分组适合哪些场景？` : dead
- `tools/biz/text-box-drawing.html` : `如何使用文本框绘制？` : dead
- `tools/biz/text-box-drawing.html` : `文本框绘制是做什么的？` : dead
- `tools/biz/text-box-drawing.html` : `文本框绘制适合哪些场景？` : dead
- `tools/biz/text-case.html` : `如何使用文本大小写转换？` : dead
- `tools/biz/text-case.html` : `文本大小写转换是做什么的？` : dead
- `tools/biz/text-case.html` : `文本大小写转换适合哪些场景？` : dead
- `tools/biz/text-case-advanced.html` : `如何使用高级大小写转换？` : dead
- `tools/biz/text-case-advanced.html` : `高级大小写转换是做什么的？` : dead
- `tools/biz/text-case-advanced.html` : `高级大小写转换适合哪些场景？` : dead
- `tools/biz/text-compare.html` : `如何使用文本并排对比？` : dead
- `tools/biz/text-compare.html` : `文本并排对比是做什么的？` : dead
- `tools/biz/text-compare.html` : `文本并排对比适合哪些场景？` : dead
- `tools/biz/text-dedup.html` : `/ 文本去重工具` : dead
- `tools/biz/text-dedup.html` : `如何使用文本去重工具？` : dead
- `tools/biz/text-dedup.html` : `文本去重工具是做什么的？` : dead
- `tools/biz/text-dedup.html` : `文本去重工具适合哪些场景？` : dead
- `tools/biz/text-extract.html` : `如何使用文本提取？` : dead
- `tools/biz/text-extract.html` : `文本提取是做什么的？` : dead
- `tools/biz/text-extract.html` : `文本提取适合哪些场景？` : dead
- `tools/biz/text-extract-chinese.html` : `如何使用提取中文字符？` : dead
- `tools/biz/text-extract-chinese.html` : `提取中文字符是做什么的？` : dead
- `tools/biz/text-extract-chinese.html` : `提取中文字符适合哪些场景？` : dead
- `tools/biz/text-extract-dates.html` : `如何使用提取日期？` : dead
- `tools/biz/text-extract-dates.html` : `提取日期是做什么的？` : dead
- `tools/biz/text-extract-dates.html` : `提取日期适合哪些场景？` : dead
- `tools/biz/text-extract-emails.html` : `如何使用提取邮箱？` : dead
- `tools/biz/text-extract-emails.html` : `提取邮箱是做什么的？` : dead
- `tools/biz/text-extract-emails.html` : `提取邮箱适合哪些场景？` : dead
- `tools/biz/text-extract-english.html` : `如何使用提取英文字符？` : dead
- `tools/biz/text-extract-english.html` : `提取英文字符是做什么的？` : dead
- `tools/biz/text-extract-english.html` : `提取英文字符适合哪些场景？` : dead
- `tools/biz/text-extract-html-tags.html` : `<div class="container"> ⏎   <h2 id="title">Hello</h2> ⏎   <p class="text" data-zh="从 HTML 片段中抽出所有标签名或指定标签，统计出现次数并去重，便于检查页面结构、清理冗余标签或核对模板标记。">Pull all tag names …(+337字)` : dead
- `tools/biz/text-extract-html-tags.html` : `仅标签名` : dead
- `tools/biz/text-extract-html-tags.html` : `含属性` : dead
- `tools/biz/text-extract-html-tags.html` : `如何使用提取 HTML 标签？` : dead
- `tools/biz/text-extract-html-tags.html` : `抽取特定标签：如筛出全部 <a href>、<img src> 记录，做资源盘点。` : dead
- `tools/biz/text-extract-html-tags.html` : `提取 HTML 标签是做什么的？` : dead
- `tools/biz/text-extract-html-tags.html` : `提取 HTML 标签适合哪些场景？` : dead
- `tools/biz/text-extract-html-tags.html` : `标签名去重` : dead
- `tools/biz/text-extract-html-tags.html` : `粘贴一段 HTML，在“指定标签”填 a，勾选“保留属性”，结果会逐条列出全部 <a ...> 开标签，可据此检查 href 是否有空值或站外链接；关掉“保留属性”则只输出 <a> 形式，便于统计数量。` : dead
- `tools/biz/text-extract-html-tags.html` : `粘贴一段 HTML，工具列出「div×12、a×5、img×3」并导出所有 <a> 的 href 列表，便于检查死链或外链。` : dead
- `tools/biz/text-extract-html-tags.html` : `统计 div 与 a` : dead
- `tools/biz/text-extract-html-tags.html` : `默认统计所有 <...> 形态；如需排除 <script>/<style> 内示例，可开启「仅正文标签」过滤。` : dead
- `tools/biz/text-extract-ips.html` : `如何使用提取 IP 地址？` : dead
- `tools/biz/text-extract-ips.html` : `提取 IP 地址是做什么的？` : dead
- `tools/biz/text-extract-ips.html` : `提取 IP 地址适合哪些场景？` : dead
- `tools/biz/text-extract-urls.html` : `如何使用提取 URL？` : dead
- `tools/biz/text-extract-urls.html` : `提取 URL是做什么的？` : dead
- `tools/biz/text-extract-urls.html` : `提取 URL适合哪些场景？` : dead
- `tools/biz/text-filter-lines.html` : `大小写敏感吗？` : dead
- `tools/biz/text-filter-lines.html` : `如何使用按行过滤？` : dead
- `tools/biz/text-filter-lines.html` : `按行过滤是做什么的？` : dead
- `tools/biz/text-filter-lines.html` : `按行过滤适合哪些场景？` : dead
- `tools/biz/text-indent.html` : `如何使用自动缩进？` : dead
- `tools/biz/text-indent.html` : `自动缩进是做什么的？` : dead
- `tools/biz/text-indent.html` : `自动缩进适合哪些场景？` : dead
- `tools/biz/text-keep-only.html` : `仅保留指定字符是做什么的？` : dead
- `tools/biz/text-keep-only.html` : `仅保留指定字符适合哪些场景？` : dead
- `tools/biz/text-keep-only.html` : `只留含「支付」的行` : dead
- `tools/biz/text-keep-only.html` : `如何使用仅保留指定字符？` : dead
- `tools/biz/text-line-numbers.html` : `如何使用添加行号？` : dead
- `tools/biz/text-line-numbers.html` : `添加行号是做什么的？` : dead
- `tools/biz/text-line-numbers.html` : `添加行号适合哪些场景？` : dead
- `tools/biz/text-merge.html` : `一列清单合并成一行` : dead
- `tools/biz/text-merge.html` : `多段文本合并适合哪些场景？` : dead
- `tools/biz/text-merge.html` : `是合并两列还是多行转一行？` : dead
- `tools/biz/text-merge.html` : `本工具把输入框里的每一行视为一段，按所选分隔符横向拼成一段；不做两列配对合并，也不做 CSV 转义。` : dead
- `tools/biz/text-merge.html` : `空格、逗号、顿号、分号、竖线、换行、分隔线均可，也可自定义；结果作为 CSV 字段且内容含逗号时，建议改用制表符或自定义分隔符。` : dead
- `tools/biz/text-merge.html` : `输入三行「苹果 / 香蕉 / 橙子」，分隔符选顿号并勾选跳过空行，结果为「苹果、香蕉、橙子」；再勾选「添加序号」则得到「1. 苹果、2. 香蕉、3. 橙子」。本工具按行横向拼接，不做两列配对。` : dead
- `tools/biz/text-pad.html` : `如何使用文本填充？` : dead
- `tools/biz/text-pad.html` : `文本填充是做什么的？` : dead
- `tools/biz/text-pad.html` : `文本填充适合哪些场景？` : dead
- `tools/biz/text-prefix-suffix.html` : `生成 SQL/代码列表：把名字列表加「'」与逗号，直接贴进查询。` : dead
- `tools/biz/text-remove-numbers.html` : `在线字符移除工具，可剔除文本中的数字、字母、标点或自定义字符，支持正则与忽略大小写，适合清洗与脱敏，纯前端处理。` : dead
- `tools/biz/text-remove-numbers.html` : `如何使用移除指定字符` : dead
- `tools/biz/text-remove-numbers.html` : `如何使用移除指定字符？` : dead
- `tools/biz/text-remove-numbers.html` : `移除指定字符是做什么的？` : dead
- `tools/biz/text-remove-numbers.html` : `移除指定字符适合哪些场景？` : dead
- `tools/biz/text-repeat.html` : `/ 文本重复工具` : dead
- `tools/biz/text-repeat.html` : `关于「文本重复工具」` : dead
- `tools/biz/text-repeat.html` : `在线文本重复工具，把指定文本或字符重复 N 次，可加序号、零填充，适合生成分隔线、占位串与批量填充，纯前端处理。` : dead
- `tools/biz/text-repeat.html` : `如何使用文本重复` : dead
- `tools/biz/text-repeat.html` : `如何使用文本重复工具？` : dead
- `tools/biz/text-repeat.html` : `文本重复工具是做什么的？` : dead
- `tools/biz/text-repeat.html` : `文本重复工具适合哪些场景？` : dead
- `tools/biz/text-reverse.html` : `/ 文本反转工具` : dead
- `tools/biz/text-reverse.html` : `在线文本反转工具，将文本按字符、单词、行或词序整体倒序，支持保留符号与空格位置、固定种子复现，适合算法演示、回文检查与趣味排版，纯前端处理。` : dead
- `tools/biz/text-reverse.html` : `如何使用文本反转` : dead
- `tools/biz/text-reverse.html` : `如何使用文本反转工具？` : dead
- `tools/biz/text-reverse.html` : `文本反转工具是做什么的？` : dead
- `tools/biz/text-reverse.html` : `文本反转工具适合哪些场景？` : dead
- `tools/biz/text-reverse-lines.html` : `在线行顺序反转工具，把多行文本整体倒序排列，可保留首尾行、跳过空行或同时反转字符，适合日志倒序与栈式回放，纯前端处理。` : dead
- `tools/biz/text-reverse-lines.html` : `如何使用行顺序反转` : dead
- `tools/biz/text-reverse-lines.html` : `如何使用行顺序反转？` : dead
- `tools/biz/text-reverse-lines.html` : `行顺序反转是做什么的？` : dead
- `tools/biz/text-reverse-lines.html` : `行顺序反转适合哪些场景？` : dead
- `tools/biz/text-sort.html` : `/ 文本行排序` : dead
- `tools/biz/text-sort.html` : `在线文本排序工具，把多行文本按字母、长度、拼音或自然顺序排序，支持忽略大小写、去重与去空行，适合名单整理与数据预处理，纯前端处理。` : dead
- `tools/biz/text-sort.html` : `如何使用文本排序` : dead
- `tools/biz/text-sort.html` : `如何使用文本行排序？` : dead
- `tools/biz/text-sort.html` : `文本行排序是做什么的？` : dead
- `tools/biz/text-sort.html` : `文本行排序适合哪些场景？` : dead
- `tools/biz/text-sort-advanced.html` : `在线高级排序工具，支持字典序、中文拼音、长度与自然排序，按列或自定义键排序，可去重与忽略大小写，适合名单、编号与表格数据，纯前端处理。` : dead
- `tools/biz/text-sort-advanced.html` : `如何使用高级排序` : dead
- `tools/biz/text-sort-advanced.html` : `如何使用高级排序？` : dead
- `tools/biz/text-sort-advanced.html` : `高级排序是做什么的？` : dead
- `tools/biz/text-sort-advanced.html` : `高级排序适合哪些场景？` : dead
- `tools/biz/text-split.html` : `/ 文本分割工具` : dead
- `tools/biz/text-split.html` : `关于「文本分割工具」` : dead
- `tools/biz/text-split.html` : `在线文本分割工具，按分隔符、行、段落或固定长度拆分文本，支持正则、去空段与去首尾空格，适合分列、定长切块与批量整理，纯前端处理。` : dead
- `tools/biz/text-split.html` : `如何使用文本分割` : dead
- `tools/biz/text-split.html` : `如何使用文本分割工具？` : dead
- `tools/biz/text-split.html` : `文本分割工具是做什么的？` : dead
- `tools/biz/text-split.html` : `文本分割工具适合哪些场景？` : dead
- `tools/biz/text-stats.html` : `/ 文本统计工具` : dead
- `tools/biz/text-stats.html` : `如何使用文本统计工具？` : dead
- `tools/biz/text-stats.html` : `文本统计工具是做什么的？` : dead
- `tools/biz/text-stats.html` : `文本统计工具适合哪些场景？` : dead
- `tools/biz/text-to-banner.html` : `8 种字符边框：井号填充、星号包围、等号横线、虚线框、双线框、圆角框、爱心边框、菱形边框；再配合左右与上下内边距控制留白。` : dead
- `tools/biz/text-to-banner.html` : `不会。工具按显示列宽计算：中文、全角标点与 emoji 各计 2 列，半角字符计 1 列，因此中英混排的边框能对齐；但终端字体若非等宽，实际显示仍可能轻微偏移。` : dead
- `tools/biz/text-to-banner.html` : `不能。本工具只产出纯文本字符横幅，可复制或下载 .txt；需要图片请用截图或专门的图片横幅工具，页面不再宣称图片导出。` : dead
- `tools/biz/text-to-banner.html` : `中文会错位吗？` : dead
- `tools/biz/text-to-banner.html` : `有哪些样式？` : dead
- `tools/biz/text-to-banner.html` : `本文本工具基于标准字符编码与文本处理规则，纯前端运行，代码不离开浏览器。 工具名称：文字转横幅 - 商业办公领域的在线工具。` : dead
- `tools/biz/text-to-banner.html` : `生成「HI」横幅` : dead
- `tools/biz/text-to-banner.html` : `纯文本交付：结果复制或下载为 .txt，可直接放进代码注释、邮件与文档，不依赖图片。` : dead
- `tools/biz/text-to-banner.html` : `终端/README 标题：把文字包进字符边框，作为脚本输出、日志或 README 顶部的分隔标题。` : dead
- `tools/biz/text-to-banner.html` : `能导出图片吗？` : dead
- `tools/biz/text-to-banner.html` : `趣味排版：用 ASCII 字符画做轻量视觉。` : dead
- `tools/biz/text-to-banner.html` : `输入「HI」、井号填充、左右内边距 2 → 文本列宽 2、内容宽 6，输出「╔════════╗ / ║##HI##║ / ╚════════╝」（实际为 3 行，上下填充为 0）；复制或下载后可直接粘进终端与 README。` : dead
- `tools/biz/text-to-slug.html` : `如何使用文本转 Slug？` : dead
- `tools/biz/text-to-slug.html` : `文本转 Slug是做什么的？` : dead
- `tools/biz/text-to-slug.html` : `文本转 Slug适合哪些场景？` : dead
- `tools/biz/text-trim.html` : `/ 文本修剪工具` : dead
- `tools/biz/text-trim.html` : `如何使用文本修剪工具？` : dead
- `tools/biz/text-trim.html` : `文本修剪工具是做什么的？` : dead
- `tools/biz/text-trim.html` : `文本修剪工具适合哪些场景？` : dead
- `tools/biz/text-wrap.html` : `/ 文本换行与填充` : dead
- `tools/biz/text-wrap.html` : `如何使用文本换行与填充？` : dead
- `tools/biz/text-wrap.html` : `文本换行与填充是做什么的？` : dead
- `tools/biz/text-wrap.html` : `文本换行与填充适合哪些场景？` : dead
- `tools/biz/unicode-normalize.html` : `Unicode 规范化是做什么的？` : dead
- `tools/biz/unicode-normalize.html` : `Unicode 规范化适合哪些场景？` : dead
- `tools/biz/unicode-normalize.html` : `如何使用Unicode 规范化？` : dead
- `tools/biz/unit-price-compare.html` : `/ 单位价格比较器` : dead
- `tools/biz/unit-price-compare.html` : `关于「单位价格比较」` : dead
- `tools/biz/unit-price-compare.html` : `单位价格比较器是做什么的？` : dead
- `tools/biz/unit-price-compare.html` : `单位价格比较器适合哪些场景？` : dead
- `tools/biz/unit-price-compare.html` : `如何使用单位价格比较器？` : dead
- `tools/biz/upside-down-text.html` : `如何使用颠倒文字？` : dead
- `tools/biz/upside-down-text.html` : `颠倒文字是做什么的？` : dead
- `tools/biz/upside-down-text.html` : `颠倒文字适合哪些场景？` : dead
- `tools/biz/zalgo-text.html` : `/ Zalgo 文字生成器` : dead

  其它成因样例（共 99 条，仅列前 5）：
  - `tools/biz/barcode-generator.html` : `/ 条形码生成器` : fragment
  - `tools/biz/fancy-text.html` : `📖 查看「装饰文字使用指南」` : harmless
  - `tools/biz/fancy-text.html` : `📚 深度解析：装饰文字` : fragment
  - `tools/biz/lorem-ipsum-advanced.html` : `📚 深度解析：高级 Lorem Ipsum 生成器` : harmless
  - `tools/biz/markdown-quote.html` : `📚 深度解析：Markdown 引用转换器` : harmless

### cardiology（dead 28 / dynamic 25 / fragment 4 / harmless 1）

- `tools/cardiology/ambulatory-bp.html` : `高血压 (mmHg)` : dead
- `tools/cardiology/aortic-dissection.html` : `DeBakey 分型：I 型起于升主动脉累及主动脉弓及降部，II 型仅限升主动脉，III 型起于弓降部向远段；DeBakey I/II 对应 Stanford A，III 对应 B。` : dead
- `tools/cardiology/aortic-dissection.html` : `急诊分诊与预警：突发撕裂样胸背痛、血压差（双臂收缩压差 >20 mmHg）、脉搏不对称提示夹层，结合 D-二聚体与增强 CT 主动脉成像快速分层，A 型立即启动绿色通道。` : dead
- `tools/cardiology/aortic-dissection.html` : `提示：Stanford分型最常用于临床决策——A型夹层是外科急症，需急诊手术修复；B型无并发症者首选药物治疗(控制心率<60bpm、收缩压100-120mmHg)。复杂B型(破裂/灌注不良/快速增大)需TEVAR(腔内修复)。仅供临床参考。` : dead
- `tools/cardiology/aortic-dissection.html` : `输入（页面默认值）：累及范围选「升主动脉+降主动脉(全程)」，仅勾选「高血压」。工具输出：Stanford A 型（累及升主动脉）、DeBakey I 型、临床类型 急诊。Note: A 型每延误 1 小时死亡风险显著上升，须立即转诊。` : dead
- `tools/cardiology/aortic-dissection.html` : `输入：破口位于升主动脉、累及主动脉弓、伴右臂血压高于左臂 25 mmHg。工具输出：Stanford A 型（DeBakey I 型）、危险度 高危、处理原则 紧急外科手术置换/再行支架、紧急措施 控制收缩压 100–120 mmHg 与心率 <60 次/分。提示：A 型每延误 1 小时死亡风险显著上升，须立即转诊。` : dead
- `tools/cardiology/calc-1.html` : `危险分层：在分级基础上叠加吸烟、血脂、糖尿病、靶器官损害与临床合并症，分为低/中/高/很高危，决定起始治疗时机与目标。` : dead
- `tools/cardiology/calc-3.html` : `TIMI 评分累加（STEMI 30 天死亡风险）：年龄 ≥75、≥65 且 <75、糖尿病/高血压/心绞痛史、收缩压 <100、心率 >100、Killip 分级 ≥2、体重 <67 kg、前壁 ST 段抬高或 LBBB、发病 ≥4h 各计 1 分（0–14 分）。` : dead
- `tools/cardiology/calc-3.html` : `危险分层：分值越高 30 天死亡风险越大（如 ≥4 分属高危），用于再灌注策略与监护强度决策。` : dead
- `tools/cardiology/calc-3.html` : `收缩压 <100 mmHg` : dead
- `tools/cardiology/cardiac-rehab-mets.html` : `输入：活动 中等速度骑行 30 分钟、强度约 6 METs、体重 70 kg。工具输出：能耗约 6×3.5×70×30/1000 ≈ 44.1 kcal、METs·分钟 180、心脏负荷 中等、建议 纳入 II 期康复有氧处方、警戒 心率不超过缺血阈。提示：具体强度由运动平板试验结果定。` : dead
- `tools/cardiology/cardiac-rehab-mets.html` : `运动靶心率 = 静息心率+(最大心率-静息心率)×40–80%` : dead
- `tools/cardiology/echo-report.html` : `LVEF <30% 属重度收缩功能降低（HFrEF 范围）；是否终末期、是否需移植/LVAD 须由心衰专科结合症状、BNP、影像与整体状况评估，本页仅提示，需临床复核。` : dead
- `tools/cardiology/echo-report.html` : `LVEF分级：≥50% 正常；40–49% HFmrEF(中间值)；30–39% HFrEF(降低)；< 30% 重度降低WMSI：≤1.0 正常、≤1.5 轻度、≤2.0 中度、> 2.0 重度心腔：LVIDd ≥ 55mm 左室扩大、左房 ≥ 40mm 扩大、主动脉 ≥ 37mm 增宽、右室 ≥ 30mm 扩大舒张…(+185字)` : dead
- `tools/cardiology/grace-score.html` : `II级 啰音<50%肺野/S3` : dead
- `tools/cardiology/grace-score.html` : `院内死亡分层：≤108 低危、109–140 中危、&gt;140 高危；6个月死亡分层另用一套切点：≤88 低危、89–118 中危、&gt;118 高危` : dead
- `tools/cardiology/hypertension-jnc.html` : `2级高血压 + 无/≤2危险因素；或 1级 + 1–2危险因素` : dead
- `tools/cardiology/hypertension-jnc.html` : `伴随临床情况/糖尿病；或 3级高血压` : dead
- `tools/cardiology/hypertension-jnc.html` : `危险分层（JNC-7）：按分级叠加年龄、吸烟、血脂、糖尿病、靶器官损害与合并临床疾病，分平均/低/中/高/很高危，决定治疗强度。` : dead
- `tools/cardiology/hypertension-jnc.html` : `提示：本工具依据JNC-7标准与中国高血压防治指南综合设计，SBP与DBP分属不同级别时取较高级别。风险分层仅供临床参考，治疗决策需由专业医师综合判断。` : dead
- `tools/cardiology/hypertension-jnc.html` : `血压分级取收缩压(SBP)与舒张压(DBP)较高级别：正常 <120/80、高血压前期 <140/90、1级 <160/100、2级 ≥160或≥100 mmHg。风险分层按 JNC-7：低危(正常/前期且无危险因素)；中危(正常/前期有 1–2 个危险因素，或 1级/2级无危险因素)；高危(正常/前期伴伴随临床情况，…(+54字)` : dead
- `tools/cardiology/hypertension-jnc.html` : `输入：收缩压 152 mmHg、舒张压 94 mmHg、女、62 岁、糖尿病、无吸烟。工具输出：分级 1级高血压、危险分层 中危（1级 + 1 个危险因素，按 JNC-7 表；临床实践常把糖尿病按高危管理）、建议 生活方式干预 + 评估启动药物、目标 <140/90（合并糖尿病常按 <130/80）、监测 家庭自测 +…(+35字)` : dead
- `tools/cardiology/hypertension-jnc.html` : `输入：收缩压 152 mmHg、舒张压 94 mmHg、女、62 岁、糖尿病、无吸烟。工具输出：分级 1级高血压（DBP 94 属 90–99）、危险分层 很高危（1级合并糖尿病）、建议 立即药物治疗 + 生活方式、目标 <130/80 且平稳、监测 家庭自测 + 并发症筛查。提示：诊断以规范测量为准。` : dead
- `tools/cardiology/nyha-classification.html` : `NYHA 心功能分级：I 级 活动不受限；II 级 日常活动轻度受限；III 级 体力活动明显受限；IV 级 休息时即有症状。6分钟步行试验(6MWT)辅助评估运动耐量：>450m 轻度/代偿良好、≥300m 中度受损、≥150m 重度受损、<150m 极重度受损。` : dead
- `tools/cardiology/nyha-classification.html` : `提示：NYHA分级为主观功能评价，受患者配合度与医师判断影响，同一患者不同时间可变化。6MWT客观反映运动耐量，两者结合可更准确评估。NYHA IV级或6MWT<300米者应评估是否需CRT/ICD或心脏移植。仅供临床参考。` : dead
- `tools/cardiology/nyha-classification.html` : `运动耐量极重度下降（<150m），死亡/再住院风险高；是否进入终末期或需移植/LVAD 应由心衰专科结合 NYHA、BNP、影像与整体状况评估，本页仅提示，需临床复核。` : dead
- `tools/cardiology/nyha-classification.html` : `高死亡风险，终末期心衰` : dead
- `tools/cardiology/pericardial-effusion.html` : `IVC增宽无塌陷(>2.1cm，塌陷<50%)` : dead

  其它成因样例（共 30 条，仅列前 5）：
  - `tools/cardiology/ambulatory-bp.html` : `请填写 8 项 ABPM 数值（收缩压/舒张压均须为 1–300 mmHg 的有效值）；空值不判读昼夜节律、晨峰与血压分级。` : dynamic
  - `tools/cardiology/ambulatory-bp.html` : `达到ABPM高血压阈值` : dynamic
  - `tools/cardiology/ambulatory-bp.html` : `未达ABPM高血压阈值` : dynamic
  - `tools/cardiology/calc-3.html` : `<65 岁` : dynamic
  - `tools/cardiology/calc-3.html` : `体重 <67 kg` : fragment

### ceramics（dead 1 / dynamic 0 / fragment 0 / harmless 0）

- `tools/ceramics/index.html` : `陶瓷工艺工具集合收录了 5 个免费在线工具，覆盖陶瓷工艺场景下的常见计算、换算与查询需求。无论你是相关领域的从业者、学生还是普通用户，都能在这里找到即用即走的实用小工具。所有工具纯前端运行，数据不上传服务器，保护隐私安全。` : dead

### chemical（dead 13 / dynamic 8 / fragment 3 / harmless 0）

- `tools/chemical/calc-pipeline-pressure-drop.html` : `ΔP = f · (L/D) · (ρ·v²/2)（达西–魏斯巴赫公式）` : dead
- `tools/chemical/checker-15.html` : `≥90% 优秀，75-89% 良好，60-74% 合格，<60% 不合格` : dead
- `tools/chemical/convert-capacity-tank.html` : `立式圆柱 V = π·(直径/2)²·液位高` : dead
- `tools/chemical/convert-capacity-tank.html` : `长方体 V = 长 × 宽 × 液位高` : dead
- `tools/chemical/convert-density-crude.html` : `千原油API度` : dead
- `tools/chemical/convert-density-crude.html` : `千密度换算` : dead
- `tools/chemical/convert-density-crude.html` : `毫原油API度` : dead
- `tools/chemical/convert-density-crude.html` : `毫密度换算` : dead
- `tools/chemical/miaomu-guige-zhiliang-yanshou-biaozhun.html` : `合格率 = 合格株数÷总数；综合得分 = (合格率+规格符合率)/2` : dead
- `tools/chemical/reaction-yield.html` : `评级：<50% 偏低｜<70% 一般｜<90% 优秀｜≥90% 卓越` : dead
- `tools/chemical/solution-concentration.html` : `58.5 g NaCl（M=58.44 g/mol）溶于 1 L 水 → 1.001 mol/L；按稀释定律 C₁V₁=C₂V₂ 稀释到 0.1 mol/L，V₂=1.001×1÷0.1≈10.01 L，需加水约 9.01 L。跨到质量分数（w%）还需密度与摩尔质量桥接，本页不提供该换算，可用质量分数工具另行计算。` : dead
- `tools/chemical/solution-concentration.html` : `摩尔浓度与稀释演练` : dead
- `tools/chemical/solution-concentration.html` : `输入 w%=10、密度 1.07 g/mL、M=58.44，工具输出约 1.83 mol/L，并给出稀释到 0.1 mol/L 的加水量参考。` : dead

  其它成因样例（共 11 条，仅列前 5）：
  - `tools/chemical/calc-pipeline-pressure-drop.html` : `折合水柱` : fragment
  - `tools/chemical/calc-pipeline-pressure-drop.html` : `折合水柱（ρ=1000）` : dynamic
  - `tools/chemical/calc-pipeline-pressure-drop.html` : `折合液柱（当前 ρ）` : dynamic
  - `tools/chemical/convert-density-crude.html` : `原油API度` : fragment
  - `tools/chemical/convert-density-crude.html` : `API 度需填写大于 -131.5 的数值（否则 SG 不为正）` : dynamic

### chemistry（dead 11 / dynamic 21 / fragment 3 / harmless 2）

- `tools/chemistry/acid-base-titration.html` : `中和所需碱体积（V_b = C_a·V_a·n_a / (C_b·n_b)）` : dead
- `tools/chemistry/boiling-point-elevation.html` : `沸点升高（ΔT_b = K_b · m · i）` : dead
- `tools/chemistry/concentration-20.html` : `C = V_溶质 / V_总` : dead
- `tools/chemistry/kp-kc.html` : `R=8.314。 Δn=0 时 Kp=Kc。` : dead
- `tools/chemistry/kp-kc.html` : `输入 Kc、温度与气体摩尔数变化 Δn，求 Kp（R=8.314，T 为开尔文）。` : dead
- `tools/chemistry/limiting-reagent.html` : `ξ = n_i/ν_i，取较小者对应的物质为限量反应物。 示` : dead
- `tools/chemistry/ph-to-h.html` : `pH < 7 酸性，> 7 碱性。` : dead
- `tools/chemistry/pressure-flow-6.html` : `混合后纯度 = Σ(各气源纯度 × 流量) ÷ 总流量` : dead
- `tools/chemistry/reaction-quotient.html` : `Q = [P]^ν_P / [R]^ν_R（气相用分压）。 QK 逆向。` : dead
- `tools/chemistry/temp-time-concentration.html` : `速率 ∝ Q₁₀^(T/10)（范特霍夫规则，Q₁₀≈2）` : dead
- `tools/chemistry/voltage-current-1.html` : `Q = I×t；沉积质量 = k×Q = k×I×t（法拉第电解定律）` : dead

  其它成因样例（共 26 条，仅列前 5）：
  - `tools/chemistry/concentration-20.html` : `🛠️ 冷却液浓度维护` : harmless
  - `tools/chemistry/concentration-20.html` : `排液置换排液量 (L)` : dynamic
  - `tools/chemistry/concentration-20.html` : `直接补加后总容量 (L)` : dynamic
  - `tools/chemistry/concentration-20.html` : `需补原液 (L)` : dynamic
  - `tools/chemistry/concentration-20.html` : `需补清水 (L)` : dynamic

### chess（dead 19 / dynamic 53 / fragment 3 / harmless 2）

- `tools/chess/gomoku-forbidden.html` : `三三禁手算例（预设「三三示例」）` : dead
- `tools/chess/gomoku-forbidden.html` : `三三禁手：逐方向检测「补一子后可形成两端开放的活四」的活三，两个及以上方向成立即禁手。` : dead
- `tools/chess/gomoku-forbidden.html` : `五连与长连：直接按该落点在四个方向的连续黑子数判断；恰好 5 为胜，≥ 6 为长连禁手。` : dead
- `tools/chess/gomoku-forbidden.html` : `共 15 行、每行 15 位：0=空、1=黑、2=白，行序从上到下；可另起一行写 judge:H8 指定待判点。例如第 8 行（从上数第 8 行）为 000001100000000 时，表示 F8、G8 为黑子。点击「载入局面并分析」后工具会渲染棋盘并直接给出判定。` : dead
- `tools/chess/gomoku-forbidden.html` : `四四禁手：逐方向检测「5 格窗口含 4 黑 1 空、补一子即成恰好五连」的四，两个及以上方向成立即禁手。` : dead
- `tools/chess/gomoku-forbidden.html` : `棋盘上 F8、G8、H6、H7 已有黑子，待判点 H8。落下后横向形成 F8-G8-H8 三连、纵向形成 H6-H7-H8 三连，两条线各补一子都能成为两端开放的活四 ⇒ 横、竖各计 1 个活三，合计 2 个，判定为三三禁手，黑方判负。若其中一条线只能补成冲四（一端被堵），则不计入活三，结论可能变为合法着法。` : dead
- `tools/chess/gomoku-forbidden.html` : `每个方向最多计 1 个，避免同一方向的多个窗口重复计数；该点已有黑子时按「查看该子」分析，不模拟落子。` : dead
- `tools/chess/gomoku-forbidden.html` : `粘贴局面格式` : dead
- `tools/chess/xiangqi-endgame.html` : `不一定。条件是必要前提，还要看先后次序、对方应手与子力是否被牵制；条件成立只说明「有杀的可能」。` : dead
- `tools/chess/xiangqi-endgame.html` : `不会。页面只列成杀条件与要点，不计算或验证任何着法；具体着法请对照棋谱、规则与棋盘实测。` : dead
- `tools/chess/xiangqi-endgame.html` : `先按名称找到对应卡片，把成杀条件逐条对照当前棋盘：哪些已满足、哪些还差一手，再决定是否继续计算。` : dead
- `tools/chess/xiangqi-endgame.html` : `基础杀法卡：给出每类杀法的成杀条件，例如重炮要求「双炮同线且前炮能借后炮作架」。` : dead
- `tools/chess/xiangqi-endgame.html` : `怎么用于实战复盘？` : dead
- `tools/chess/xiangqi-endgame.html` : `本页会给出具体着法吗？` : dead
- `tools/chess/xiangqi-endgame.html` : `满足成杀条件就一定能杀吗？` : dead
- `tools/chess/xiangqi-endgame.html` : `第一张卡「重炮」：成杀条件 = 双炮在同一线路叠放、前炮能借后炮为炮架将军、黑将无路可走；要点 = 先控将门再落炮，避免后炮被吃或炮架被拆；注意 = 本卡只讲条件，不给具体着法。复盘时按这三条逐项核对，再回到棋盘实测。` : dead
- `tools/chess/xiangqi-endgame.html` : `组合杀法卡：说明马炮、车炮配合的先后次序与成立前提，例如马后炮要先控斜线退路、再落炮。` : dead
- `tools/chess/xiangqi-endgame.html` : `经典残局卡：七星聚会、野马操田、千里独行等名局的攻防要点，只列条件与思路，不着录着法。` : dead
- `tools/chess/xiangqi-endgame.html` : `重炮成杀条件速查` : dead

  其它成因样例（共 58 条，仅列前 5）：
  - `tools/chess/bridge-scoring.html` : `请检查输入：定约级别需为 1–7 的整数，完成墩数需为 0–13 的整数。` : dynamic
  - `tools/chess/elo-rating.html` : `预期得分率分析（含和棋）` : dynamic
  - `tools/chess/elo-rating.html` : `你方预期得分率` : dynamic
  - `tools/chess/elo-rating.html` : `对手预期得分率` : dynamic
  - `tools/chess/elo-rating.html` : `Elo 的 Ea 是「胜=1、和=0.5、负=0」的期望得分，并非纯胜率；两项之和恒为 100%。` : dynamic

### chinese（dead 5 / dynamic 5 / fragment 0 / harmless 0）

- `tools/chinese/stroke-order-viewer.html` : `Static stroke order of 永 (Eight Principles of Yong)` : dead
- `tools/chinese/stroke-order-viewer.html` : `小朋友学写字，照着静态笔顺列表逐笔临摹「永」「学」「想」等已收录字，建立正确的起笔、行笔、收笔顺序，避免倒笔。` : dead
- `tools/chinese/stroke-order-viewer.html` : `成年人练书法或硬笔字，核对易错字笔顺（如「我」第五笔为斜钩、「想」先写木字旁再写目和心），纠正长期错误习惯。` : dead
- `tools/chinese/stroke-order-viewer.html` : `演示「永」字八法笔顺` : dead
- `tools/chinese/stroke-order-viewer.html` : `输入「永」（5 画）：按列表依次显示 点→横折钩→横撇→撇→捺，对应「永字八法」基本笔画；再输入「学」（8 画）可对照 点、点、撇、点、横钩……；本工具为静态列表，不播放动画。` : dead

  其它成因样例（共 5 条，仅列前 5）：
  - `tools/chinese/stroke-order-viewer.html` : `请输入一个汉字` : dynamic
  - `tools/chinese/stroke-order-viewer.html` : `字：` : dynamic
  - `tools/chinese/stroke-order-viewer.html` : `总笔画：` : dynamic
  - `tools/chinese/stroke-order-viewer.html` : `未收录笔顺，可先按拼音/部首分解辅助书写。` : dynamic
  - `tools/chinese/stroke-order-viewer.html` : `提示：本工具输出静态笔顺文字列表；真实笔顺依字形字体可能存在差异，结果供学习参考。` : dynamic

### civil（dead 12 / dynamic 1 / fragment 4 / harmless 2）

- `tools/civil/active-earth-rankine.html` : `请输入有效的土体参数：γ、H > 0，φ 在 0–45° 之间，c ≥ 0。` : dead
- `tools/civil/calc-strength-ratio.html` : `Bolomey：W/C = (α·f_c × γ_c)/(f_c + α·γ_c × γ_w)；体积比由 W/C 与砂率推导` : dead
- `tools/civil/concrete-wb-ratio.html` : `σ 按 JGJ 55 取值：≤C20 取 4.0 MPa，C25–C35 取 5.0 MPa，>C35 取 6.0 MPa；上表按 f_b=42.5 MPa、α_a=0.53、α_b=0.20 反算，实际以试配为准。耐久性另有最大水胶比限值（一类 0.60、二a 0.55、二b 0.50、三a 0.45、三b 0.40…(+11字)` : dead
- `tools/civil/concrete-wb-ratio.html` : `鲍罗米公式（水胶比）：W/B = α_a × 胶凝材料实际强度 f_b ÷ (配制强度 f_cu,0 + α_a × α_b × f_b)，联动输出胶水比 = 1 ÷ W/B。校验：f_cu、f_b、α_a 任一 ≤0 提示「请输入有效参数」。判据：无固定分级，W/B 保留 3 位小数、胶水比保留 2 位小数，两者互为…(+101字)` : dead
- `tools/civil/dijichengzailijisuan.html` : `承载力 = f(土性, 深度, 宽度)` : dead
- `tools/civil/dijichengzailijisuan.html` : `请输入有效参数：c≥0，φ 在 0–45° 之间，γ、B、K>0，Df≥0` : dead
- `tools/civil/index.html` : `土木工程工具集合收录了 21 个免费在线工具，覆盖土木工程场景下的常见计算、换算与查询需求。无论你是相关领域的从业者、学生还是普通用户，都能在这里找到即用即走的实用小工具。所有工具纯前端运行，数据不上传服务器，保护隐私安全。` : dead
- `tools/civil/masonry-bearing.html` : `砌体墙抗压承载力 N = φ × f × A，其中 f 为砌体抗压强度设计值(MPa)、A 为墙体截面面积(mm²)、φ 为承载力影响系数（由高厚比 β = H₀ ÷ h 与偏心距确定，β 越大 φ 越小）；f 由块体与砂浆强度等级查表确定（MU10 砖配 M5 砂浆约 1.5 MPa）；须满足 N 不低于荷载设计值。` : dead
- `tools/civil/pile-capacity.html` : `请输入有效的桩参数：d、L > 0，q_s、q_p ≥ 0，K ≥ 1。` : dead
- `tools/civil/rebar-anchorage.html` : `d=20mm、C30（ft=1.43）、HRB400（fy=360）、带肋 α=0.14：la=α·(fy/ft)·d=0.14×(360/1.43)×20≈705mm；抗震 laE=ζaE·la（一二级 ζaE=1.15）≈811mm。` : dead
- `tools/civil/rebar-anchorage.html` : `l_ab = α·ζ_a·(f_y/f_t)·d，α=0.14（带肋钢筋外形系数）` : dead
- `tools/civil/two-way-slab.html` : `两向弯矩均按短跨 l_x² 折算：M_x = α_x·q·l_x²，M_y = α_y·q·l_x² 系数按 l_y/l_x 查表线性插值；l_y/l_x ≥ 2 时按单向板设计（系数取 2.0 行封顶）` : dead

  其它成因样例（共 7 条，仅列前 5）：
  - `tools/civil/beam-udl.html` : `σ = M/W，W = bh²/6 为截面模量` : fragment
  - `tools/civil/beam-udl.html` : `请输入有效的梁参数。` : dynamic
  - `tools/civil/calc-2.html` : `D = 系数 × d，` : fragment
  - `tools/civil/calc-strength-ratio.html` : `🧮 混凝土配合比计算（通用）` : harmless
  - `tools/civil/masonry-bearing.html` : `🧮 砌体墙抗压承载力计算（土木）` : harmless

### cleaning（dead 2 / dynamic 0 / fragment 1 / harmless 0）

- `tools/cleaning/area-hours.html` : `：约 8-12 分钟/㎡，含地面、桌面、卫生间基础清洁` : dead
- `tools/cleaning/checker-9.html` : `≥90% 流程完善，75-89% 基本完善，60-74% 待改进，<60% 需重建` : dead

  其它成因样例（共 1 条，仅列前 5）：
  - `tools/cleaning/checker-10.html` : `综合考核分 = 各区域平均分之和 ÷ 区域数 × 20` : fragment

### clinical-lab（dead 52 / dynamic 55 / fragment 13 / harmless 0）

- `tools/clinical-lab/biochemistry-ratio.html` : `• AST/ALT (De Ritis)：<1 提示急性病毒性肝炎；>1 提示酒精性肝病、慢性肝病或肝硬化` : dead
- `tools/clinical-lab/biochemistry-ratio.html` : `• BUN/Cr (mmol/L÷μmol/L)：需×1000换算，比值>20(换算后)提示肾前性氮质血症；<10提示肾性或低蛋白饮食` : dead
- `tools/clinical-lab/cardiac-marker-curve.html` : `「输入连续检测的cTnI/cTnT值与时间，绘制动态曲线并分析变化趋势」按输入参数进行专业计算并输出结果。` : dead
- `tools/clinical-lab/cardiac-marker-curve.html` : `参考上限(99百分位)` : dead
- `tools/clinical-lab/cardiac-marker-curve.html` : `参考：本页按 Rhea 法估算` : dead
- `tools/clinical-lab/cardiac-marker-curve.html` : `心肌标志物动态判读（时序展示与辅助判读，非剂量公式）：cTnI/cTnT 发病 3–6h 升高、10–24h 达峰、持续 7–14 天；CK-MB 3–8h 升高、12–24h 达峰、48–72h 恢复（宜判再梗死）；MYO 1–2h 升高、6–8h 达峰、24h 恢复。以 99th 百分位参考上限(URL) 为 cu…(+48字)` : dead
- `tools/clinical-lab/coagulation-inr.html` : `= 对照PT / (对照PT + 0.6×(患者PT - 对照PT)) × 100%，<40%提示严重肝损害` : dead
- `tools/clinical-lab/convert-glucose-1.html` : `eAG(mmol/L) = eAG(mg/dL) ÷ 18（mg/dL → mmol/L 的固定换算除数 18）。校验：无独立校验，mmol/L 值随 mg/dL 结果联动换算。判据：判读分级（<140 正常 / 140–199 糖尿病前期 / ≥200 糖尿病范围）按 mg/dL 口径给出，mmol/L 供国际单位读…(+4字)` : dead
- `tools/clinical-lab/convert-glucose-1.html` : `即时显示` : dead
- `tools/clinical-lab/convert-glucose-1.html` : `双向换算` : dead
- `tools/clinical-lab/convert-glucose-1.html` : `平均血糖 eAG(mg/dL) = 28.7 × HbA1c(%) − 46.7（ADAG 换算式）；与控制目标差距 = eAG − 154（对应 HbA1c 7.0% 目标）。校验：无强校验，HbA1c 缺省按 0。判据：eAG <140 正常糖耐量（年度复查）、140–199 糖尿病前期（OGTT 复查，每 3–6…(+48字)` : dead
- `tools/clinical-lab/convert-glucose-1.html` : `血糖 mg/dL↔mmol/L 换算工具。用于跨系统与报告统一；纯换算。` : dead
- `tools/clinical-lab/convert-glucose-1.html` : `诊断切点对照` : dead
- `tools/clinical-lab/convert-glucose-1.html` : `采用 ADAG 研究公式，由 HbA1c 估算平均血糖；仅供健康管理参考，不能替代指尖/静脉血糖监测。` : dead
- `tools/clinical-lab/flow-cytometry-ratio.html` : `HbA1c 换算器` : dead
- `tools/clinical-lab/flow-cytometry-ratio.html` : `• CD4/CD8↓：常见于AIDS(CD4<200为艾滋病期)、肿瘤化疗后、免疫抑制` : dead
- `tools/clinical-lab/flow-cytometry-ratio.html` : `• CD4<500：HIV感染者免疫抑制；<200：机会性感染风险高，需预防性用药` : dead
- `tools/clinical-lab/flow-cytometry-ratio.html` : `在 HbA1c 与平均血糖之间换算，辅助糖尿病随访与检验报告对照。` : dead
- `tools/clinical-lab/flow-cytometry-ratio.html` : `常规免疫评估` : dead
- `tools/clinical-lab/flow-cytometry-ratio.html` : `流式细胞术 CD4/CD8 比值与淋巴细胞亚群计算器。输入各亚群百分比或绝对计数，计算 CD4/CD8 比值并对照参考范围，辅助免疫状态评估；结果仅供复核，不替代专科诊断。` : dead
- `tools/clinical-lab/parasite-egg-id.html` : `命中：卵壳` : dead
- `tools/clinical-lab/parasite-egg-id.html` : `命中：卵盖` : dead
- `tools/clinical-lab/parasite-egg-id.html` : `命中：名称` : dead
- `tools/clinical-lab/parasite-egg-id.html` : `命中：大小` : dead
- `tools/clinical-lab/parasite-egg-id.html` : `命中：形状` : dead
- `tools/clinical-lab/parasite-egg-id.html` : `命中：说明` : dead
- `tools/clinical-lab/parasite-egg-id.html` : `图谱复习` : dead
- `tools/clinical-lab/parasite-egg-id.html` : `如：蛔虫、钩虫、血吸虫` : dead
- `tools/clinical-lab/parasite-egg-id.html` : `常见肠道寄生虫虫卵形态学特征查询，辅助镜检识别` : dead
- `tools/clinical-lab/parasite-egg-id.html` : `搜索虫卵名称` : dead
- `tools/clinical-lab/pcr-ct-interpretation.html` : `• Ct 38-40：弱阳性/灰区，需重复确认` : dead
- `tools/clinical-lab/pcr-ct-interpretation.html` : `• Ct<29：强阳性，模板浓度高` : dead
- `tools/clinical-lab/pcr-ct-interpretation.html` : `• Ct>40 或无Ct：阴性` : dead
- `tools/clinical-lab/semen-analysis.html` : `= 精液量 × 浓度 × (PR+NP)%，是评估男性生育力的重要综合指标。TMSC>20×10⁶提示生育力良好，<5×10⁶提示生育力受损。需禁欲2-7天后检测，异常需复查2-3次确诊。` : dead
- `tools/clinical-lab/semen-analysis.html` : `按 WHO 参考下限对精液量、浓度、活力、形态逐项对照，辅助男科报告初读；结果仅供参考。` : dead
- `tools/clinical-lab/tumor-marker-doubling.html` : `核心计算公式（按输入变量）：dt × Math.log(2) ÷ Math.log(ratio)；dt × Math.log(2) ÷ Math.log(v1÷v2)；|(t2-t1)|÷(1000×60×60×24)` : dead
- `tools/clinical-lab/urinalysis-interpretation.html` : `尿液 pH 偏碱` : dead
- `tools/clinical-lab/urinalysis-interpretation.html` : `尿液 pH 偏酸` : dead
- `tools/clinical-lab/urine-sediment-atlas.html` : `共 15 项 · 按类别与关键词过滤` : dead
- `tools/clinical-lab/urine-sediment-atlas.html` : `如：管型、结晶、红细胞` : dead
- `tools/clinical-lab/urine-sediment-atlas.html` : `对尿沉渣有形成分（红细胞/白细胞/管型/结晶）的形态与提示做图谱式对照，辅助镜检复习。` : dead
- `tools/clinical-lab/urine-sediment-atlas.html` : `查询尿沉渣中管型、结晶、细胞等有形成分的形态与临床意义` : dead
- `tools/clinical-lab/vaginal-discharge-grading.html` : `Nugent/AV 评分` : dead
- `tools/clinical-lab/vaginal-discharge-grading.html` : `乳酸杆菌 ++++、无球菌、上皮 ++++、WBC 0–5/HP → Ⅰ度；若乳酸杆菌减少、球菌增多且 WBC 增多 → Ⅲ–Ⅳ度。Nugent 评分（0–10 分）需按油镜视野另行计数，本页不计算。` : dead
- `tools/clinical-lab/vaginal-discharge-grading.html` : `分级计算` : dead
- `tools/clinical-lab/vaginal-discharge-grading.html` : `按 Nugent 或 AV 评分对阴道分泌物做分级计算，辅助报告理解；诊断与用药由妇科医师决定。` : dead
- `tools/clinical-lab/vaginal-discharge-grading.html` : `教学演示评分` : dead
- `tools/clinical-lab/vaginal-discharge-grading.html` : `清洁度分级示例` : dead
- `tools/clinical-lab/vaginal-discharge-grading.html` : `白带常规按乳酸杆菌/球菌/上皮/白细胞组合判读清洁度（Ⅰ–Ⅳ）；Nugent 0–10 分需另做评分，本页不提供。` : dead
- `tools/clinical-lab/vaginal-discharge-grading.html` : `阴道分泌物分级工具。按 Nugent/AV 评分计算分级，辅助报告理解；诊断与用药由妇科医师决定。` : dead
- `tools/clinical-lab/vaginal-discharge-grading.html` : `阴道清洁度按乳酸杆菌/球菌/上皮细胞/白细胞组合判 Ⅰ–Ⅳ 度：Ⅰ度(乳酸杆菌+++、无球菌、上皮+++、WBC 0–5)正常；Ⅱ度(乳酸杆菌/上皮较多、WBC少)正常；Ⅲ度(乳酸杆菌减少、球菌增多、上皮减少、WBC 15–30)炎症；Ⅳ度(乳酸杆菌/上皮消失、大量球菌+脓细胞)严重炎症兜底计分 = 乳酸杆菌 − 球菌…(+78字)` : dead
- `tools/clinical-lab/vaginal-discharge-grading.html` : `需氧菌性阴道炎(AV)需另按 AV 评分评估，本页不计算。` : dead

  其它成因样例（共 68 条，仅列前 5）：
  - `tools/clinical-lab/autoantibody-interpretation.html` : `硬化症-肌炎重叠综合征(SSc-肌炎)` : dynamic
  - `tools/clinical-lab/autoantibody-interpretation.html` : `副肿瘤神经综合征相关(抗Ma-2)` : dynamic
  - `tools/clinical-lab/autoantibody-interpretation.html` : `抗Ma-2（需筛查潜在肿瘤）` : dynamic
  - `tools/clinical-lab/blood-gas-analysis.html` : `I型呼吸衰竭` : dynamic
  - `tools/clinical-lab/blood-gas-analysis.html` : `II型呼吸衰竭` : dynamic

### clinical-nursing（dead 11 / dynamic 28 / fragment 5 / harmless 0）

- `tools/clinical-nursing/cvc-maintenance.html` : `单管腔冲管量 = 导管容积 + 追加量（约 2 mL）；封管量 = 导管容积 × 1.2；总冲管量 = 单管腔冲管量 × 管腔数；肝素封管单位数 = 总封管量(mL) × 封管液浓度(U/mL，常用 10 或 100 U/mL)；采用正压脉冲式冲管并边推边夹管。` : dead
- `tools/clinical-nursing/cvc-maintenance.html` : `注意：严格无菌操作，冲管遇阻力不可强行推注，应检查导管是否打折或血栓。肝素使用需评估患者凝血功能。` : dead
- `tools/clinical-nursing/cvc-maintenance.html` : `透析导管：1000-5000 U/mL 肝素液` : dead
- `tools/clinical-nursing/gastric-tube-depth.html` : `公式：置入深度 = 身高 × 0.2 + 鼻尖至剑突测量值` : dead
- `tools/clinical-nursing/gastric-tube-depth.html` : `置入深度 = 身高 × 0.2 + 鼻尖至剑突测量值` : dead
- `tools/clinical-nursing/gastric-tube-depth.html` : `身高公式：身高×0.2 + 鼻尖至剑突距离` : dead
- `tools/clinical-nursing/generator-pressure.html` : `复核一次六期描述生成` : dead
- `tools/clinical-nursing/suction-pressure.html` : `婴幼儿安全范围` : dead
- `tools/clinical-nursing/suction-pressure.html` : `当前压力 150 mmHg（≈20.0 kPa）过高（超过安全上限 120 mmHg），有黏膜损伤风险！` : dead
- `tools/clinical-nursing/suction-pressure.html` : `成人中心负压 80–120 mmHg（约 10.6–16.0 kPa），儿童 80–100，婴儿 60–80，新生儿 40–60。` : dead
- `tools/clinical-nursing/suction-pressure.html` : `新生儿安全范围` : dead

  其它成因样例（共 33 条，仅列前 5）：
  - `tools/clinical-nursing/bag-valve-mask.html` : `CPR成人通气频率：10次/分（每6秒1次，高级气道建立后）` : dynamic
  - `tools/clinical-nursing/bag-valve-mask.html` : `CPR儿童通气频率：20-30次/分（每2-3秒1次）` : dynamic
  - `tools/clinical-nursing/bag-valve-mask.html` : `CPR婴儿通气频率：20-30次/分（每2-3秒1次）` : dynamic
  - `tools/clinical-nursing/bag-valve-mask.html` : `婴儿急救通气：20-30次/分（每2-3秒1次）` : dynamic
  - `tools/clinical-nursing/bag-valve-mask.html` : `儿童急救通气：12-20次/分（每3-5秒1次）` : dynamic

### construction（dead 17 / dynamic 21 / fragment 2 / harmless 2）

- `tools/construction/ac-size-guide.html` : `市场俗称 1 匹≈2500W 制冷量（部分厂商按 2324W 标称；小 1 匹约 2200W、大 1 匹约 2600W）。选购以『制冷量 W』为准更准，匹数只是通俗说法。` : dead
- `tools/construction/ac-size-guide.html` : `新房装修或单间添置空调，先按面积与层高估算制冷量（普通住宅约 200–220 W/㎡），再折算匹数（1 匹≈2500 W 制冷量），避免小马拉大车导致制冷不足。` : dead
- `tools/construction/ac-size-guide.html` : `面积 20㎡ × 层高 2.8m × 指标 220W/㎡ ≈ 基础制冷量 4400W ⏎ 1 匹≈2500W → 约需 1.8 匹 ⏎ 普通朝向无西晒：选 2 匹挂机留余量` : dead
- `tools/construction/calc-204.html` : `承载面积法：间距 s = √(容许荷载 / 侧压力)；根数 n = 理论布置数` : dead
- `tools/construction/calc-204.html` : `模板支撑布置：理论间距 s = √(单根支撑容许荷载 Pa ÷ 混凝土侧压力 q)；纵向根数 nL = 向上取整(模板长度 L ÷ s)、竖向根数 nH = 向上取整(模板高度 H ÷ s)，总根数 = nL × nH；实际纵距 = L ÷ nL、实际竖距 = H ÷ nH；单根实际荷载 = q × 实际纵距 × 实际…(+124字)` : dead
- `tools/construction/calc-204.html` : `💡 支撑间距 s=√(P_allow/q)；按间距布设支撑，单根承载面积 s×s，根数=⌈L/s⌉×⌈H/s⌉。` : dead
- `tools/construction/calc-205.html` : `用钢量 = Σ(杆件长度 × 钢管线密度) + 扣件/连接件` : dead
- `tools/construction/calc-206.html` : `立杆稳定性 K = N / (φ·A·f)（按 JGJ130 轴压稳定）` : dead
- `tools/construction/calc-94.html` : `调差系数 = Σ(报告期价ᵢ / 基期价ᵢ × 权重ᵢ)` : dead
- `tools/construction/cement-mortar-ratio.html` : `Cement (kg) = 每方水泥用量 × 砂浆体积；砂(kg) = 水泥 × 砂灰比；水(kg) = 水泥 × 0.45；袋数 = ⌈水泥 ÷ 每袋重量⌉` : dead
- `tools/construction/cement-mortar-ratio.html` : `请输入有效的砂浆方量（>0）与每袋水泥重量（>0，kg）；空值不再按 50kg 兜底。` : dead
- `tools/construction/cement-mortar-ratio.html` : `质量比 水泥:砂 ≈ 1:4.8 ⏎ 每方约：水泥 280kg，砂 1344kg，水约 300kg（依砂含水）` : dead
- `tools/construction/estimate-39.html` : `不可预见费(5%)` : dead
- `tools/construction/estimate-39.html` : `总投资 = Σ(面积 × 分项单价) × (1 + 不可预见费率)` : dead
- `tools/construction/gongchengzaojiazhishujisuan.html` : `Iᵢ = P₁ᵢ/P₀ᵢ × 100；综合指数 = Σ(Iᵢ×wᵢ)/Σwᵢ` : dead
- `tools/construction/gongchengzaojiazhishujisuan.html` : `指数>100表示造价上涨，<100表示下降` : dead
- `tools/construction/window-shading.html` : `计算遮阳系数` : dead

  其它成因样例（共 25 条，仅列前 5）：
  - `tools/construction/analysis-43.html` : `120000.00 元` : dynamic
  - `tools/construction/calc-196.html` : `保温后外径 (mm)` : dynamic
  - `tools/construction/calc-196.html` : `年散热损失 (kWh/m)` : dynamic
  - `tools/construction/calc-196.html` : `散热损失 q (W/m)` : dynamic
  - `tools/construction/calc-196.html` : `裸管散热损失 (W/m)` : dynamic

### cosmetic-derm（dead 10 / dynamic 0 / fragment 1 / harmless 0）

- `tools/cosmetic-derm/area-12.html` : `严重程度按红斑面积占比分级；血管直径按 μm 分型` : dead
- `tools/cosmetic-derm/area-12.html` : `面积占比分级：<5% 轻度（毛细血管扩张 I 级）、5–15% 中度（II 级）、15–30% 重度（III 级）、≥30% 极重度（IV 级）；占比上限截断至 100%。血管直径分型：<0.2 μm 细血管（毛细血管扩张）、<1 μm 中等血管（小静脉扩张）、≥1 μm 粗血管（静脉扩张）。用于面部毛细血管扩张（红血…(+14字)` : dead
- `tools/cosmetic-derm/concentration.html` : `pKa 常数：AHA（甘醇酸）3.83、BHA（水杨酸）2.97、TCA 0.66。pH 越低游离酸比例越高、剥脱力越强；pH 提示：<2.0 刺激性大、<3.0 剥脱力强、<3.5 适中、≥3.5 温和。剥脱深度判定：AHA 按浓度与 pH 组合分极浅表（≤20% 且 pH≥3.5）／浅表／中度／深度；BHA 按 ≤…(+74字)` : dead
- `tools/cosmetic-derm/concentration.html` : `游离酸比例 = 10^(pH − pKa) / (1 + 10^(pH − pKa))；游离酸浓度 = 输入浓度 × 游离酸比例` : dead
- `tools/cosmetic-derm/concentration.html` : `💡 剥脱深度由酸种类、浓度、pH 共同决定。pH 越低、浓度越高，剥脱越深。游离酸量 = 浓度 × 10^(pH-pKa) /(1+10^(pH-pKa))。` : dead
- `tools/cosmetic-derm/length-spacing.html` : `针长以 mm 计，实际穿透深度按皮肤弹性回缩取 0.8 折减。单点通道面积 = π × (直径 μm/10000 ÷ 2)² cm²。作用层次判定：<0.3 mm 角质层、<0.5 mm 表皮层、<1.0 mm 真皮乳头层、<1.5 mm 真皮网状层、≥1.5 mm 深层真皮/皮下。用于微针针长与间距组合的层次覆盖评估…(+1字)` : dead
- `tools/cosmetic-derm/microneedle.html` : `有效深度 = 针长 × 0.75（皮肤回缩折减）；单孔半径 r = 直径 μm ÷ 2 ÷ 1000（mm）；总孔体积 = 密度 × 面积 × 单孔体积 × 遍数（mm³ ≈ μL）。分子量因子：<1 kDa 0.95、<10 kDa 0.85、<100 kDa 0.65、<500 kDa 0.45、否则 0.30。单…(+64字)` : dead
- `tools/cosmetic-derm/sebumeter.html` : `温度每升高 1 ℃ 皮脂分泌约增 10%，故按标准 25 ℃ 作反向校正。混合型判定：|T区 − U区| > 60 μg/cm² 即为混合型，并按 T/U 区分别定性。肤质分级：<70 干性、<120 中性、<180 偏油、≥180 油性。用于皮脂仪（Sebumeter）多部位读数换算与肤质判定。` : dead
- `tools/cosmetic-derm/temp-time-4.html` : `收缩率分段：<45 ℃ 为 0；45–55 ℃ 为 (T − 45)/10 × 10；55–60 ℃ 为 10 + (T − 55)/5 × 10；60–70 ℃ 为 20 + (T − 60)/10 × 25；70–75 ℃ 为 45 + (T − 70)/5 × 5；≥75 ℃ 封顶 50%。效果分级：<45 无效…(+53字)` : dead
- `tools/cosmetic-derm/thread-lift.html` : `线材系数：平滑线 0、PDO 0.5、双向锯齿 0.6、PLA 0.7、PCLA 0.8、单向锯齿 0.85、360° 锯齿 1.0。角度偏差 = |输入角度 − 区域最佳角度|；区域最佳进针/提拉角：中面部 50/45°、下面部 40/35°、下颌线 55/50°、颈部 35/30°、眉部 20/15°。松弛度修正：…(+82字)` : dead

  其它成因样例（共 1 条，仅列前 5）：
  - `tools/cosmetic-derm/calc-51.html` : `SPF = 1/(1-UVB阻隔率)` : fragment

### daily-goods（dead 2 / dynamic 2 / fragment 0 / harmless 0）

- `tools/daily-goods/shoe-size.html` : `cm=26.0，中国码 CN=26.0；欧盟码 EU=round((26×1.5+2)×2)/2=41；美码男 US=round((26×1.5-22)×2)/2=17；英码 UK=US-1=16；女码 US=17+1.5=18.5。若脚长 250mm：EU=39.5、US男=15.5、UK=14.5。Nike 等偏窄…(+9字)` : dead
- `tools/daily-goods/shoe-size.html` : `≈ 脚长cm × 3 ÷ 2 − 22（如 25.5cm → 7.25 ≈ 7.5）` : dead

  其它成因样例（共 2 条，仅列前 5）：
  - `tools/daily-goods/shoe-size.html` : `≈ 男码 + 1.5` : dynamic
  - `tools/daily-goods/shoe-size.html` : `≈ 美码 − 1` : dynamic

### data（dead 10 / dynamic 0 / fragment 0 / harmless 0）

- `tools/data/csv-json.html` : `CSV/JSON 互转是做什么的？` : dead
- `tools/data/csv-json.html` : `CSV/JSON 互转适合哪些场景？` : dead
- `tools/data/csv-json.html` : `如何使用CSV/JSON 互转？` : dead
- `tools/data/csv-to-markdown.html` : `CSV ↔ Markdown 表格是做什么的？` : dead
- `tools/data/csv-to-markdown.html` : `CSV ↔ Markdown 表格适合哪些场景？` : dead
- `tools/data/csv-to-markdown.html` : `如何使用CSV ↔ Markdown 表格？` : dead
- `tools/data/index.html` : `数据分析工具集合收录了 17 个免费在线工具，覆盖数据分析场景下的常见计算、换算与查询需求。无论你是相关领域的从业者、学生还是普通用户，都能在这里找到即用即走的实用小工具。所有工具纯前端运行，数据不上传服务器，保护隐私安全。` : dead
- `tools/data/yaml-json.html` : `YAML/JSON 互转是做什么的？` : dead
- `tools/data/yaml-json.html` : `YAML/JSON 互转适合哪些场景？` : dead
- `tools/data/yaml-json.html` : `如何使用YAML/JSON 互转？` : dead

### decor（dead 4 / dynamic 0 / fragment 1 / harmless 0）

- `tools/decor/detector-18.html` : `新房入住前自测：录入甲醛、TVOC 实测值，与 GB/T 18883 限值（甲醛 0.10、TVOC 0.60 mg/m³ 等）逐项比对，输出「达标/超标」与超标倍数。` : dead
- `tools/decor/detector-18.html` : `甲醛限值≤0.10mg/m³，TVOC≤0.60mg/m³，苯≤0.11mg/m³，氨≤0.20mg/m³，氡≤300Bq/m³` : dead
- `tools/decor/detector-18.html` : `示例：密闭 12h 后实测甲醛 0.14 mg/m³、TVOC 0.45 mg/m³。 ⏎ • 甲醛限值 0.10，超标 0.14÷0.10−1 = 40% ⏎ • TVOC 限值 0.60，0.45 达标 ⏎ • 结论：甲醛超标，建议加强通风并延迟入住` : dead
- `tools/decor/paint-color-mix.html` : `色浆比例 = 色浆质量 ÷ 乳胶漆质量 × 100%` : dead

  其它成因样例（共 1 条，仅列前 5）：
  - `tools/decor/curtain-fabric.html` : `每幅用料长 = 成品高 + 上下缝边 + 对花损耗` : fragment

### dentistry（dead 11 / dynamic 3 / fragment 0 / harmless 0）

- `tools/dentistry/assessor-5.html` : `氧化锆透光率 = 分光测量` : dead
- `tools/dentistry/bite-contact.html` : `咬合平衡 = 接触点分析` : dead
- `tools/dentistry/calc-1.html` : `DMFT = 龋数 + 失数 + 补数` : dead
- `tools/dentistry/caries-risk.html` : `Cariogram 龋病风险 = 加权评分` : dead
- `tools/dentistry/gingival-index.html` : `牙龈指数 GI = 分级评分` : dead
- `tools/dentistry/implant-dimensions.html` : `种植体选择 = f(骨量, 美学)` : dead
- `tools/dentistry/oral-ulcer.html` : `口腔溃疡分期 = 病程分级` : dead
- `tools/dentistry/orthodontic-force.html` : `正畸力 = 牙移动需求` : dead
- `tools/dentistry/salivary-flow.html` : `唾液流率 = 测量评估` : dead
- `tools/dentistry/sialography.html` : `腺体造影 = 导管形态判读` : dead
- `tools/dentistry/tongue-oral-health.html` : `舌诊关联 = 特征匹配` : dead

  其它成因样例（共 3 条，仅列前 5）：
  - `tools/dentistry/periodontal-pocket.html` : `轻度附着丧失（CAL 2–3 mm），建议基础治疗与定期维护` : dynamic
  - `tools/dentistry/periodontal-pocket.html` : `中度附着丧失（CAL 4–5 mm），需系统牙周治疗` : dynamic
  - `tools/dentistry/periodontal-pocket.html` : `重度附着丧失（CAL ≥6 mm），需综合治疗，可能需手术干预` : dynamic

### dermatology（dead 8 / dynamic 0 / fragment 7 / harmless 0）

- `tools/dermatology/actinic-keratosis.html` : `低（<1%/年）` : dead
- `tools/dermatology/easi-eczema.html` : `四区评估：逐区录入受累面积（0–6 级，其中 2 级为 10–29%）与四项严重度（各 0–3），成人按头颈 0.1、上肢 0.2、躯干 0.3、下肢 0.4 加权（儿童 <8 岁改用 0.2/0.3/0.2/0.3），汇总 EASI。` : dead
- `tools/dermatology/easi-eczema.html` : `成人权重：头颈0.1/上肢0.2/躯干0.3/下肢0.4；儿童权重：头颈0.2/上肢0.2/躯干0.3/下肢0.3` : dead
- `tools/dermatology/gags-acne.html` : `GAGS = Σ(各部位最重皮损评分 × 局部因子)。Doshi 1997 原版为 6 个部位：前额、双颊各 2，鼻、下颌各 1，胸部与上背合并计 1 个部位（取较重者）=3。皮损评分：0无、1粉刺、2丘疹、3脓疱、4结节。满分 4×(2+2+2+1+1+3)=44。` : dead
- `tools/dermatology/gags-acne.html` : `GAGS = Σ(各部位最重皮损评分 × 局部因子)。局部因子：前额/双颊/胸部/上背=2，鼻/下颌=1。皮损评分：0无、1粉刺、2丘疹、3脓疱、4结节。满分48。` : dead
- `tools/dermatology/leprosy-grading.html` : `视力<6/60/兔眼/角膜溃疡` : dead
- `tools/dermatology/leprosy-grading.html` : `视力<6/60、兔眼（眼睑闭合不全）、虹膜睫状体炎、角膜溃疡` : dead
- `tools/dermatology/leprosy-grading.html` : `麻风病可防可治不可怕。早期诊断和及时MDT治疗是防止残疾的关键。2级残疾（G2D）是衡量麻风防治效果的重要指标，WHO目标是G2D在新发患者中比例<1%。如出现以下"麻风可疑症状"请转诊：1. 皮肤出现浅色/红色斑块且感觉丧失；2. 手足麻木伴肌肉无力；3. 面部出现浸润性结节或斑块；4. 周围神经粗大伴触痛。` : dead

  其它成因样例（共 7 条，仅列前 5）：
  - `tools/dermatology/easi-eczema.html` : `EASI 严重度分级` : fragment
  - `tools/dermatology/gags-acne.html` : `GAGS = Σ(各部位最重皮损评分 × 局部因子)` : fragment
  - `tools/dermatology/gags-acne.html` : `胸部` : fragment
  - `tools/dermatology/gags-acne.html` : `上背` : fragment
  - `tools/dermatology/gags-acne.html` : `胸部/上背` : fragment

### design（dead 184 / dynamic 315 / fragment 103 / harmless 3）

- `tools/design/analysis-64.html` : `使用体验（贡献 +3.8）、功能完整度（贡献 +2.5）。` : dead
- `tools/design/analysis-64.html` : `同一组得分换用不同权重会得出不同结论：当前「均衡」权重下 价格竞争力 占 20%，若企业实际更看重体验，可切换「重体验」再看结论是否翻转 —— 结论翻转说明该维度是决策敏感项，需先对齐权重口径。` : dead
- `tools/design/analysis-64.html` : `品牌信任（贡献 -4.5）、价格竞争力（贡献 -2.0） —— 高权重上的劣势对总分拖累最大，建议先投入这两项。` : dead
- `tools/design/analysis-64.html` : `在「均衡」权重下，总分差 +0.5（0.7%），判定为 双方胶着。` : dead
- `tools/design/analysis-64.html` : `总分差（0.7%）` : dead
- `tools/design/aztec-code.html` : `按 Aztec 码编码规则生成：文本经高等级纠错编码与位填充后排布为方阵，并带中央定位图案（简化版采用固定模式）；纯前端生成，用于票据与物流信息的移动端识读。` : dead
- `tools/design/base64-to-image.html` : `输入去首尾空白后，若不以 data: 开头则自动补上 data:image/png;base64, 前缀；交由 Image 加载校验，加载成功则插入图片并把该 data URL 记为结果地址，加载失败提示无效的 Base64 数据并清空结果` : dead
- `tools/design/bpm-tapper.html` : `BPM = 60 / 平均点击间隔(秒)` : dead
- `tools/design/breakpoint-queries.html` : `@media (min-width: <断点>) { /* 移动优先样式 */ }` : dead
- `tools/design/checker-5.html` : `内置平声 198 字、仄声 2086 字常用字库，无需联网查韵书` : dead
- `tools/design/checker-5.html` : `第1句` : dead
- `tools/design/checker-5.html` : `第2句` : dead
- `tools/design/checker-5.html` : `第3句` : dead
- `tools/design/checker-5.html` : `第4句` : dead
- `tools/design/checker-5.html` : `逐字判定平仄：把每句按字拆开，命中内置平声字库（198 字）标「平」、命中仄声字库（2086 字）标「仄」、两库均未收录标「？」，再按句分行输出逐字平仄串，便于对照格律谱自查。多音字与古入声字仅作参考，最终以权威韵书为准。` : dead
- `tools/design/color-picker.html` : `使用 #4151E1` : dead
- `tools/design/color-picker.html` : `使用 #41A1E1` : dead
- `tools/design/color-picker.html` : `使用 #41E1D1` : dead
- `tools/design/color-picker.html` : `使用 #8141E1` : dead
- `tools/design/color-picker.html` : `使用 #D141E1` : dead
- `tools/design/color-shade-generator.html` : `#6366f1 基色` : dead
- `tools/design/css-grid-generator.html` : `grid-template-columns: repeat(n, 1fr | <固定宽度> | auto)；gap: <行间距> <列间距>` : dead
- `tools/design/cvd-safe-palette.html` : `⚠ 相邻两色最小对比 2.90:1（#BF124E ↔ #FF9A11），低于非文字元素 AA（≥3:1），相邻摆放时需加分隔或标签。` : dead
- `tools/design/cvd-safe-palette.html` : `明度（L*）序列：58 → 21 → 91 → 41 → 73 → 31　相邻最小间隔` : dead
- `tools/design/data-matrix.html` : `生成数据矩阵风格的装饰图案（示意用途，不可扫码），可调整尺寸与配色。` : dead
- `tools/design/detector-29.html` : `AAA级要求（正常文字）` : dead
- `tools/design/detector-29.html` : `AA级要求（正常文字）` : dead
- `tools/design/detector-29.html` : `• A级要求未全部满足：优先修复A级不合规项（共10项），这是无障碍最低要求` : dead
- `tools/design/detector-29.html` : `参考标准：W3C WCAG 2.1, WAI-ARIA 1.1, Section 508 | 清单通过：0/14` : dead
- `tools/design/detector-29.html` : `正常文字（<18pt / <24px）` : dead
- `tools/design/detector-29.html` : `满足AAA级最高要求（7.0:1），所有文字均可被清晰识别。` : dead
- `tools/design/farnsworth-d15-test.html` : `槽位 10` : dead
- `tools/design/farnsworth-d15-test.html` : `槽位 11` : dead
- `tools/design/farnsworth-d15-test.html` : `槽位 12` : dead
- `tools/design/farnsworth-d15-test.html` : `槽位 13` : dead
- `tools/design/farnsworth-d15-test.html` : `槽位 14` : dead
- `tools/design/farnsworth-d15-test.html` : `槽位 2` : dead
- `tools/design/farnsworth-d15-test.html` : `槽位 3` : dead
- `tools/design/farnsworth-d15-test.html` : `槽位 4` : dead
- `tools/design/farnsworth-d15-test.html` : `槽位 5` : dead
- `tools/design/farnsworth-d15-test.html` : `槽位 6` : dead
- `tools/design/farnsworth-d15-test.html` : `槽位 7` : dead
- `tools/design/farnsworth-d15-test.html` : `槽位 8` : dead
- `tools/design/farnsworth-d15-test.html` : `槽位 9` : dead
- `tools/design/farnsworth-d15-test.html` : `第 10 个色帽，可拖动或用左右方向键移动` : dead
- `tools/design/farnsworth-d15-test.html` : `第 11 个色帽，可拖动或用左右方向键移动` : dead
- `tools/design/farnsworth-d15-test.html` : `第 12 个色帽，可拖动或用左右方向键移动` : dead
- `tools/design/farnsworth-d15-test.html` : `第 13 个色帽，可拖动或用左右方向键移动` : dead
- `tools/design/farnsworth-d15-test.html` : `第 14 个色帽，可拖动或用左右方向键移动` : dead
- `tools/design/farnsworth-d15-test.html` : `第 2 个色帽，可拖动或用左右方向键移动` : dead
- `tools/design/farnsworth-d15-test.html` : `第 3 个色帽，可拖动或用左右方向键移动` : dead
- `tools/design/farnsworth-d15-test.html` : `第 4 个色帽，可拖动或用左右方向键移动` : dead
- `tools/design/farnsworth-d15-test.html` : `第 5 个色帽，可拖动或用左右方向键移动` : dead
- `tools/design/farnsworth-d15-test.html` : `第 6 个色帽，可拖动或用左右方向键移动` : dead
- `tools/design/farnsworth-d15-test.html` : `第 7 个色帽，可拖动或用左右方向键移动` : dead
- `tools/design/farnsworth-d15-test.html` : `第 8 个色帽，可拖动或用左右方向键移动` : dead
- `tools/design/farnsworth-d15-test.html` : `第 9 个色帽，可拖动或用左右方向键移动` : dead
- `tools/design/focal-length-equivalent.html` : `APS-C (佳能)等效` : dead
- `tools/design/generator-33.html` : `【人物设定卡】 ⏎ 姓名/代号： ⏎ 身份与立场： ⏎ 核心目标（想要什么）： ⏎ 最大阻碍（谁/什么在挡）： ⏎ 性格缺陷或心结： ⏎ 与主角的关系： ⏎ 一句话人设： ⏎  ⏎ 【章节卡】 ⏎ 第 N 章｜所属幕： ⏎ 本章目标（推动什么）： ⏎ 冲突升级点： ⏎ 结尾钩子： ⏎ 预计字数：` : dead
- `tools/design/generator-33.html` : `每章平均 2500 字，高于最少 2000 字，配额可行；按日均 3000 字约 100 天完稿。` : dead
- `tools/design/generator-33.html` : `第 1 章` : dead
- `tools/design/generator-33.html` : `第 117 章` : dead
- `tools/design/generator-33.html` : `第 118 章` : dead
- `tools/design/generator-33.html` : `第 119 章` : dead
- `tools/design/generator-33.html` : `第 120 章` : dead
- `tools/design/generator-33.html` : `第 2 章` : dead
- `tools/design/generator-33.html` : `第 3 章` : dead
- `tools/design/generator-33.html` : `第 4 章` : dead
- `tools/design/generator-33.html` : `第 5 章` : dead
- `tools/design/generator-33.html` : `第 61 章` : dead
- `tools/design/generator-34.html` : `按「字高(mm) ≈ 观看距离(m) ÷ 5」估算：若最后一排距幕布 X 米，正文最小字号约需 20 pt × X ÷ 1.4（本页参数下约 113 pt 可覆盖 8 m）。` : dead
- `tools/design/generator-34.html` : `每要点可用时间偏紧（8~15 秒），建议页内要点不超过 4 条，并把细节放入备注页。` : dead
- `tools/design/generator-34.html` : `第 1 页` : dead
- `tools/design/generator-34.html` : `第 10 页` : dead
- `tools/design/generator-34.html` : `第 15 页` : dead
- `tools/design/generator-34.html` : `第 16 页` : dead
- `tools/design/generator-34.html` : `第 17 页` : dead
- `tools/design/generator-34.html` : `第 18 页` : dead
- `tools/design/generator-34.html` : `第 2 页` : dead
- `tools/design/generator-34.html` : `第 3 页` : dead
- `tools/design/generator-34.html` : `第 4 页` : dead
- `tools/design/generator-38.html` : `【角色】你是资深产品/设计领域专家。 ⏎ 【任务】对「健身 App 的「完成训练」页面」执行生成。 ⏎ 【输出格式】按分条列表输出 3 条，条与条之间不要重复语义。 ⏎ 【约束】不超过 12 字；避免使用感叹号；面向 25-35 岁上班族。 ⏎ 【自检】输出前逐条核对：① 条数是否等于 3；② 是否满足上述全部约束；③…(+51字)` : dead
- `tools/design/generator-38.html` : `对「健身 App 的「完成训练」页面」执行【生成】` : dead
- `tools/design/generator-38.html` : `对象：健身 App 的「完成训练」页面` : dead
- `tools/design/generator-6.html` : `内阴影怎么来的？` : dead
- `tools/design/generator-6.html` : `每层有约 20% 概率自动带上 inset 关键字，结果中会直接写出，复制后即可使用。想手动调偏移与颜色请用专门的阴影调节工具。` : dead
- `tools/design/generator-6.html` : `生成 3 组随机阴影` : dead
- `tools/design/gradient.html` : `以及相邻色标对比度提示（此处约 1.90:1，仅适合装饰，不宜作为正文文字底色）。` : dead
- `tools/design/gradient.html` : `会。工具按 WCAG 相对亮度公式计算相邻色标的对比度，并标注「正文级（≥4.5:1）/ 大字或图形级（≥3:1）/ 仅装饰（<3:1）」。注意这是色标之间的对比度，不是文字与背景的对比度，正文配色仍需另行核算。` : dead
- `tools/design/gradient.html` : `会提示对比度不足吗？` : dead
- `tools/design/gradient.html` : `按位置升序拼为 linear-gradient(135deg, #FF6B35 0%, #7C3AED 100%)。` : dead
- `tools/design/gradient.html` : `浏览器实时预览、可复制的 ` : dead
- `tools/design/gradient.html` : `结果以浏览器实时渲染为准，纯前端本地处理、数据不上传；生成的样式仅作快速产出参考，正式项目请以设计系统与浏览器实测为准。` : dead
- `tools/design/identicon-generator.html` : `哈希 = FNV-1a / MD5(输入串) → 取位生成左右对称网格与色相` : dead
- `tools/design/image-dpi-converter.html` : `1920 × 1080 像素 @ 300 DPI = 162.56 × 91.44 mm` : dead
- `tools/design/image-dpi-converter.html` : `对角线 (mm)` : dead
- `tools/design/image-dpi-converter.html` : `高度 (mm)` : dead
- `tools/design/iso-noise-reference.html` : `ISO 6,400 · 较重` : dead
- `tools/design/material-color.html` : `主色 #009688` : dead
- `tools/design/material-color.html` : `主色 #00BCD4` : dead
- `tools/design/material-color.html` : `主色 #03A9F4` : dead
- `tools/design/material-color.html` : `主色 #2196F3` : dead
- `tools/design/material-color.html` : `主色 #3F51B5` : dead
- `tools/design/material-color.html` : `主色 #4CAF50` : dead
- `tools/design/material-color.html` : `主色 #607D8B` : dead
- `tools/design/material-color.html` : `主色 #673AB7` : dead
- `tools/design/material-color.html` : `主色 #795548` : dead
- `tools/design/material-color.html` : `主色 #8BC34A` : dead
- `tools/design/material-color.html` : `主色 #9C27B0` : dead
- `tools/design/material-color.html` : `主色 #9E9E9E` : dead
- `tools/design/material-color.html` : `主色 #CDDC39` : dead
- `tools/design/material-color.html` : `主色 #E91E63` : dead
- `tools/design/material-color.html` : `主色 #F44336` : dead
- `tools/design/material-color.html` : `主色 #FF5722` : dead
- `tools/design/material-color.html` : `主色 #FF9800` : dead
- `tools/design/material-color.html` : `主色 #FFC107` : dead
- `tools/design/material-color.html` : `主色 #FFEB3B` : dead
- `tools/design/mesh-gradient.html` : `PNG 与浏览器预览完全一致吗？` : dead
- `tools/design/mesh-gradient.html` : `mesh 和线性渐变有什么区别？` : dead
- `tools/design/mesh-gradient.html` : `三色 mesh 与对比度` : dead
- `tools/design/mesh-gradient.html` : `三色（#667eea / #764ba2 / #f093fb）在默认位置生成 3 层 radial-gradient；叠加文字设为 #000000 时，与最暗色 #764ba2 的对比度为 3.30:1，仅达到「AA 大文本」，正文需放大或改用 #ffffff（最低 6.37:1，达到 AA）。` : dead
- `tools/design/mesh-gradient.html` : `不会。颜色、位置与导出全部在浏览器本地完成，不上传服务器、不写入远端存储。` : dead
- `tools/design/mesh-gradient.html` : `不完全一致。PNG 由 Canvas 按 farthest-corner 半径近似绘制，色团位置与配色一致，但边缘过渡与 CSS 渲染可能有细微差别；需要像素级一致时请截图或使用 CSS。` : dead
- `tools/design/mesh-gradient.html` : `会。页面按 WCAG 公式计算叠加文字与每个色标的对比度，报告最差的一处并给出等级；低于 4.5:1 会标红，提示换色或加大字号。` : dead
- `tools/design/mesh-gradient.html` : `线性渐变沿单一方向过渡，mesh 用多个径向色团叠加、方向各异，过渡更自然，常用于海报与大背景。本页输出的是标准 CSS 多层 radial-gradient，可直接粘贴到项目样式。` : dead
- `tools/design/music-scale-reference.html` : `同调内取 1、3、5 级音叠加即三和弦；不同级数决定和弦性质。本页只列音阶与调号，不直接计算和弦。` : dead
- `tools/design/music-scale-reference.html` : `音阶调号参考。设计创意工具，可视化操作，一键生成 CSS 代码。` : dead
- `tools/design/pixel-art-generator.html` : `不会。绘图状态只存在当前页面内存中，刷新即重置；导出通过浏览器本地下载，数据不上传。` : dead
- `tools/design/pixel-art-generator.html` : `不支持。本工具是手工网格绘制，不读取本地图片，也不做色彩量化；需要照片像素化请先用图像软件处理。` : dead
- `tools/design/pixel-art-generator.html` : `固定 6 色（红、橙、绿、蓝、紫、黑），另可切到擦除模式清除格子；不支持任意色值输入。` : dead
- `tools/design/pixel-art-generator.html` : `导出 CSS 像素块（box-shadow 方案），直接放进网页做装饰元素。` : dead
- `tools/design/pixel-art-generator.html` : `导出明细 CSV` : dead
- `tools/design/pixel-art-generator.html` : `手绘 8×8 / 16×16 像素头像、图标或游戏素材。` : dead
- `tools/design/pixel-art-generator.html` : `把网格作品导出为字符画，贴进文档、README 或聊天窗口。` : dead
- `tools/design/pixel-art-generator.html` : `支持导入图片自动像素化吗？` : dead
- `tools/design/pixel-art-generator.html` : `网格尺寸 8、颜色选橙色（#F59E0B），页面载入预置笑脸：共 48 个有色格、16 个空格。字符画为 8 行、每行 8 个符号（■ 有色、· 空白）；CSS 导出生成含 48 条 box-shadow 的 .pixel-art 规则，可直接嵌入页面。` : dead
- `tools/design/pixel-art-generator.html` : `网格尺寸改为 16 后画布清空，点击格子逐格上色；切换「擦除」模式可清除误点格。绘制完成后用「导出字符画 .txt」或「导出 CSS 像素块」保存，字符画预览与导出内容一致。` : dead
- `tools/design/pixel-art-generator.html` : `自绘 16×16 图标` : dead
- `tools/design/pixel-art-generator.html` : `调色板有几种颜色？` : dead
- `tools/design/px-to-rem.html` : `rem 相对于根元素（）的 font-size；修改根字号即可整体缩放页面，便于响应式与无障碍。` : dead
- `tools/design/rem-to-px.html` : `px = rem × root（root 为当前根元素 font-size）` : dead
- `tools/design/shadow-generator.html` : `文字阴影模式支持文本阴影效果` : dead
- `tools/design/shutter-speed-calculator.html` : `- 体育、动作、奔跑儿童` : dead
- `tools/design/shutter-speed-calculator.html` : `- 凝固高速运动（飞鸟、赛车）` : dead
- `tools/design/shutter-speed-calculator.html` : `- 安全手持下限、摆拍` : dead
- `tools/design/shutter-speed-calculator.html` : `- 建议三脚架、追焦` : dead
- `tools/design/shutter-speed-calculator.html` : `- 弱光环境、车流光轨` : dead
- `tools/design/shutter-speed-calculator.html` : `- 瀑布拉丝、夜景长曝光` : dead
- `tools/design/shutter-speed-calculator.html` : `- 行走的人、日常抓拍` : dead
- `tools/design/shutter-speed-calculator.html` : `- 需屏息、轻微动态模糊` : dead
- `tools/design/shutter-speed-calculator.html` : `- 风景、静止人物、日常` : dead
- `tools/design/shutter-speed-calculator.html` : `安全快门 t ≤ 1 / (f × k)（k 为裁切系数；经验法则为焦距倒数）` : dead
- `tools/design/spectrum-visualizer.html` : `用正弦叠加公式生成频谱柱形动画（合成数据，不接入麦克风或音频文件）。` : dead
- `tools/design/spectrum-visualizer.html` : `音乐播放器的频谱样式参考。` : dead
- `tools/design/svg-to-png.html` : `默认保留透明通道，只有选择白色背景时才铺白底。` : dead
- `tools/design/svg-to-png.html` : `默认导出透明背景；把「背景」切到白色即可得到白底 PNG。` : dead
- `tools/design/tailwind-colors.html` : `主色 #06B6D4` : dead
- `tools/design/tailwind-colors.html` : `主色 #0EA5E9` : dead
- `tools/design/tailwind-colors.html` : `主色 #10B981` : dead
- `tools/design/tailwind-colors.html` : `主色 #14B8A6` : dead
- `tools/design/tailwind-colors.html` : `主色 #22C55E` : dead
- `tools/design/tailwind-colors.html` : `主色 #3B82F6` : dead
- `tools/design/tailwind-colors.html` : `主色 #6366F1` : dead
- `tools/design/tailwind-colors.html` : `主色 #64748B` : dead
- `tools/design/tailwind-colors.html` : `主色 #6B7280` : dead
- `tools/design/tailwind-colors.html` : `主色 #71717A` : dead
- `tools/design/tailwind-colors.html` : `主色 #737373` : dead
- `tools/design/tailwind-colors.html` : `主色 #78716C` : dead
- `tools/design/tailwind-colors.html` : `主色 #84CC16` : dead
- `tools/design/tailwind-colors.html` : `主色 #8B5CF6` : dead
- `tools/design/tailwind-colors.html` : `主色 #A855F7` : dead
- `tools/design/tailwind-colors.html` : `主色 #D946EF` : dead
- `tools/design/tailwind-colors.html` : `主色 #EAB308` : dead
- `tools/design/tailwind-colors.html` : `主色 #EC4899` : dead
- `tools/design/tailwind-colors.html` : `主色 #EF4444` : dead
- `tools/design/tailwind-colors.html` : `主色 #F43F5E` : dead
- `tools/design/tailwind-colors.html` : `主色 #F59E0B` : dead
- `tools/design/tailwind-colors.html` : `主色 #F97316` : dead
- `tools/design/tester-assessor.html` : `SUS得分（等级D）` : dead
- `tools/design/tester-assessor.html` : `• SUS得分低于平均（50<68）：系统整体可用性需大幅改进，重点解决一致性和复杂性问题` : dead
- `tools/design/tester-assessor.html` : `• 任务完成率偏低（80%）：优化关键任务流程，减少步骤，提供明确引导` : dead
- `tools/design/tester-assessor.html` : `• 完成时间超出预期（1.3x）：精简操作步骤，优化高频路径，提供快捷方式` : dead
- `tools/design/tester-assessor.html` : `参考标准：ISO 9241-11, SUS (Brooke, 1996), Nielsen可用性准则 | 测试用户：5人` : dead
- `tools/design/waveform-visualizer.html` : `按公式生成时域波形预览，不读取或上传音频文件。` : dead

  其它成因样例（共 421 条，仅列前 5）：
  - `tools/design/analysis-64.html` : `可用性（测试/评估/改进）流程` : fragment
  - `tools/design/analysis-64.html` : `无障碍（设计/标准/检测）指南` : fragment
  - `tools/design/analysis-64.html` : `我方加权总分（换算百分制）` : dynamic
  - `tools/design/analysis-64.html` : `竞品加权总分（换算百分制）` : dynamic
  - `tools/design/analysis-64.html` : `双方胶着` : fragment

### dynamics（dead 5 / dynamic 0 / fragment 1 / harmless 0）

- `tools/dynamics/coefficient-restitution.html` : `e=1 完全弹性，e=0 完全非弹性。 5,0→2,3 → e=0.2。` : dead
- `tools/dynamics/hooke-force.html` : `F = k·x（大小，方向反向形变）。 k=200,x=0.1 → 20 N。` : dead
- `tools/dynamics/inclined-plane-accel.html` : `a = g(sinθ − μcosθ)。 θ 过小且 μ 大则不下溜。` : dead
- `tools/dynamics/static-friction-max.html` : `max = μ_s·N。 静摩擦系数通常 > 动摩擦。` : dead
- `tools/dynamics/terminal-velocity.html` : `mg = ½ρv²C_dA 时达到终端速度。 示例 → 约 43.2 m/s。` : dead

  其它成因样例（共 1 条，仅列前 5）：
  - `tools/dynamics/torque-force.html` : `τ=rF 最大。` : fragment

### eco（dead 25 / dynamic 3 / fragment 6 / harmless 0）

- `tools/eco/afforestation-cost.html` : `投资 = 株数 × 单株成本；年吸收 = 株数 × 18.3` : dead
- `tools/eco/aqi.html` : `AQI 等级：优/良/轻度/中度/重度/严重污染` : dead
- `tools/eco/battery-storage.html` : `E = 容量(Ah) × 电压(V) / 1000 × 放电深度` : dead
- `tools/eco/carbon-forest.html` : `树木数 = 年排放 / 单株吸收；林地 = 树木数 / 密度` : dead
- `tools/eco/carbon-offset.html` : `交通 = 私家车×0.192 + 公交×0.089 + 短途航班×0.255 + 长途航班×0.195（kg/km，按公里数）；能源 = 用电×0.583（kg/kWh） + 天然气×2.04（kg/m³）；饮食按年值（素食 100 / 基本素食 150 / 少量肉 250 / 平均 330 / 高肉 500 kg）除…(+171字)` : dead
- `tools/eco/eco-10.html` : `减排 = 发电量 × 排放因子` : dead
- `tools/eco/eco-10.html` : `年发电量 = 装机 × 满发小时` : dead
- `tools/eco/eco-14.html` : `单位面积能耗 = 年用电量 / 建筑面积` : dead
- `tools/eco/eco-15.html` : `电单耗 = 日总电耗 / 日处理量` : dead
- `tools/eco/eco-16.html` : `年发电量 = 装机 × 容量因子 × 8760 小时` : dead
- `tools/eco/eco-4.html` : `总量 = 人口 × 人均量 × 天数` : dead
- `tools/eco/eco-5.html` : `节水率 = (原用水量 − 节水后) / 原用水量 × 100%` : dead
- `tools/eco/eco-6.html` : `绿化覆盖率 = 绿地面积 / 总面积 × 100%` : dead
- `tools/eco/eco-8.html` : `年碳汇 = 面积 × 密度 × 单株固碳量` : dead
- `tools/eco/env-impact-score.html` : `综合 = (能耗 + 水耗 + 废弃物 + 排放) / 4` : dead
- `tools/eco/fuel-carbon.html` : `CO₂ = 燃油量 × 排放因子（汽油约 2.31）` : dead
- `tools/eco/index.html` : `生态环保工具集合收录了 38 个免费在线工具，覆盖生态环保场景下的常见计算、换算与查询需求。无论你是相关领域的从业者、学生还是普通用户，都能在这里找到即用即走的实用小工具。所有工具纯前端运行，数据不上传服务器，保护隐私安全。` : dead
- `tools/eco/landfill-methane.html` : `CH₄ = 有机物 × 可降解比 × MCF × 体积比 × 16/12` : dead
- `tools/eco/lifespan-8.html` : `回收环境收益 = (原生能耗 − 再生能耗) × 回收质量` : dead
- `tools/eco/methane-equivalent.html` : `CO₂e = CH₄ × GWP₁₀₀（甲烷≈28）` : dead
- `tools/eco/recycle-rate.html` : `回收率 = 回收量 / 总量 × 100%` : dead
- `tools/eco/solar-output.html` : `E = 面积 × 效率 × 日均辐照 × 天数` : dead
- `tools/eco/waste-calculator.html` : `基础量 = 人数 × 1.2 kg/人/天 × (1 + 地区修正)（城区 0、郊区 −0.1、农村 −0.2）；食品残渣 = 人数 × (烹饪系数 + 剩菜系数) × 30（烹饪：餐餐做 2.5 / 经常 1.5 / 偶尔 0.8 / 几乎不做 0.3；剩菜：无 0 / 偶尔 0.3 / 较多 0.7，单位 kg/人…(+146字)` : dead
- `tools/eco/water-footprint.html` : `牛肉≈15415 L/kg，棉衬衫≈2700 L/件，咖啡≈140 L/杯` : dead
- `tools/eco/water-saving.html` : `节约 = 人均 × 人数 × 天数 × 节水比例` : dead

  其它成因样例（共 9 条，仅列前 5）：
  - `tools/eco/carbon-offset.html` : `垃圾减量计算` : fragment
  - `tools/eco/convert-air-aqi.html` : `垃圾减量计算` : fragment
  - `tools/eco/convert-air-aqi.html` : `碳足迹抵消` : fragment
  - `tools/eco/lifespan-8.html` : `回收质量 (kg)` : dynamic
  - `tools/eco/lifespan-8.html` : `等效减排里程 (km)` : dynamic

### ecommerce（dead 40 / dynamic 16 / fragment 12 / harmless 0）

- `tools/ecommerce/analysis-70.html` : `不能。工具只做环比计算、阈值标记和「改善 / 需关注」的机械判定，不含归因拆解、漏斗分析或改进建议生成。结论可作为复盘会的输入，具体原因仍需人工排查。` : dead
- `tools/ecommerce/analysis-70.html` : `竞品（监测/分析/应对）研究` : dead
- `tools/ecommerce/analysis-conversion-funnel.html` : `整体转化率 = Π 各层相邻转化率 = 末层 ÷ 首层 × 100%` : dead
- `tools/ecommerce/analysis-cost-8.html` : `保本销量 = 固定成本 ÷ (单价 − 单位变动成本)；单位边际贡献 = 单价 − 单位变动成本` : dead
- `tools/ecommerce/analysis-cost-8.html` : `单价（元）` : dead
- `tools/ecommerce/analysis-cost-8.html` : `按采购/佣金/物流/推广分项核算毛利` : dead
- `tools/ecommerce/analysis-cost-8.html` : `本量利（CVP）测算：输入固定成本、单位变动成本与单价，计算单位边际贡献、保本销量与保本销售额，辅助定价与成本控制。` : dead
- `tools/ecommerce/calc-79.html` : `增长率 = (本期−同期)/同期 × 100%` : dead
- `tools/ecommerce/conversion-4.html` : `转化率 = 成交/观看` : dead
- `tools/ecommerce/discount.html` : `实付 = 标价 × (1−折扣率)` : dead
- `tools/ecommerce/erp-dingdan-caigou-duijie.html` : `ERP 对接 = 数据映射` : dead
- `tools/ecommerce/estimate-ranking.html` : `优化排查：调高评分或转化看分变化，定位短板因子。` : dead
- `tools/ecommerce/estimate-ranking.html` : `先归一化到同尺度再加权，否则量纲大的因子主导结果。结果仅供电商运营测算、选品与决策参考，不构成财务或税务意见，也不替代各平台最新规则与正式对账，以平台官方规则与账实为准。` : dead
- `tools/ecommerce/estimate-ranking.html` : `关键词搜索量` : dead
- `tools/ecommerce/estimate-ranking.html` : `平台算法不公开，本工具按经验权重估算趋势，仅供优化方向参考。结果仅供电商运营测算、选品与决策参考，不构成财务或税务意见，也不替代各平台最新规则与正式对账，以平台官方规则与账实为准。` : dead
- `tools/ecommerce/estimate-ranking.html` : `得分估算：录入各因子与权重，算综合排名分。` : dead
- `tools/ecommerce/estimate-ranking.html` : `按搜索量与权重得分估算综合排序分与首页门槛差距。` : dead
- `tools/ecommerce/estimate-ranking.html` : `按点击率、转化率、销量、评分与评价数五个因子归一化加权，估算搜索排名竞争力与预估点击、订单、GMV。` : dead
- `tools/ecommerce/estimate-ranking.html` : `排名 = 权重×因子` : dead
- `tools/ecommerce/estimate-ranking.html` : `搜索排名得分估算` : dead
- `tools/ecommerce/estimate-ranking.html` : `教学演示：演示归一化后加权求和。` : dead
- `tools/ecommerce/estimate-ranking.html` : `本工具按销量、评分、点击与转化等权重因子估算搜索排名得分与相对位次，辅助搜索优化。` : dead
- `tools/ecommerce/estimate-ranking.html` : `权重得分` : dead
- `tools/ecommerce/estimate-ranking.html` : `标题与主图优化前后对比` : dead
- `tools/ecommerce/estimate-ranking.html` : `示例：销量权 0.4 得 80、评分 0.3 得 70、转化 0.3 得 60，综合=0.4×80+0.3×70+0.3×60=71。` : dead
- `tools/ecommerce/estimate-ranking.html` : `类目内相对位次判断` : dead
- `tools/ecommerce/estimate-ranking.html` : `评分/转化短板定位` : dead
- `tools/ecommerce/estimate-ranking.html` : `💡 综合排序分 = 搜索量 × 权重得分 ÷ 100；首页门槛取搜索量的 90%；差距 = 门槛 − 排序分。` : dead
- `tools/ecommerce/index.html` : `输入销量、评价与点击等权重因子，估算商品在搜索结果中的相对排名与权重得分，用于电商 SEO 与曝光优化参考。` : dead
- `tools/ecommerce/inventory-1.html` : `补货点 = 日均销×提前期 + 安全库存` : dead
- `tools/ecommerce/kedan-jiandanjia-liandailv.html` : `客单价 = 销售额/订单数` : dead
- `tools/ecommerce/pingjia-chaping-tuihuo-lv.html` : `退货率 = 退货/成交` : dead
- `tools/ecommerce/report.html` : `关键指标异常标红` : dead
- `tools/ecommerce/report.html` : `同环比与占比呈现` : dead
- `tools/ecommerce/report.html` : `多维度经营指标卡可视化` : dead
- `tools/ecommerce/report.html` : `核心指标快照汇总` : dead
- `tools/ecommerce/report.html` : `经营日报/周报看板搭建` : dead
- `tools/ecommerce/response-2.html` : `客服响应 = 时效统计` : dead
- `tools/ecommerce/wuliu-fahuo-cangchu-gongyinglian-zhenghe.html` : `物流整合 = 路径优化` : dead
- `tools/ecommerce/wuliu-lanshou-qianshou-shixiao.html` : `物流时效 = 揽收→签收时长` : dead

  其它成因样例（共 28 条，仅列前 5）：
  - `tools/ecommerce/analysis-70.html` : `⚠️ 退款率应在 0–100% 之间，已按边界值处理，请核对原始数据。` : dynamic
  - `tools/ecommerce/analysis-70.html` : `增长依赖客单价而非单量` : dynamic
  - `tools/ecommerce/analysis-conversion-funnel.html` : `相邻转化率 = 本层人数 ÷ 上层人数 × 100%` : fragment
  - `tools/ecommerce/analysis-cost-8.html` : `控制/优化/效益` : fragment
  - `tools/ecommerce/analysis-cost-8.html` : `单位变动成本（元）` : dynamic

### economics（dead 6 / dynamic 0 / fragment 1 / harmless 0）

- `tools/economics/elasticity-demand.html` : `E_d ≈ −1.22（富有弹性）。 绝对值>1 为富有弹性。` : dead
- `tools/economics/gdp-growth-rate.html` : `本期 GDP_t (亿元)` : dead
- `tools/economics/nominal-to-real.html` : `实际 = 名义/(1+π)` : dead
- `tools/economics/present-value.html` : `现值的计算：PV = FV ÷（1 + r)^t；贴现额 = FV − PV；贴现因子 =（1 + r)^t；隐含年化收益率 =（FV ÷ PV)^(1/t) − 1；用于投资与票据的现值折算及收益率反推。` : dead
- `tools/economics/unemployment-rate.html` : `u = 失业人数 / 劳动力` : dead
- `tools/economics/velocity-of-money.html` : `MV = PY（交易方程）。 P=1,Y=2000,M=500 → 4。` : dead

  其它成因样例（共 1 条，仅列前 5）：
  - `tools/economics/real-gdp.html` : `GDP = 名义 GDP / (1 + 平减指数` : fragment

### edu（dead 34 / dynamic 22 / fragment 6 / harmless 1）

- `tools/edu/calc-4.html` : `剩余考核平均分 = (目标成绩 − 当前成绩) / 剩余权重 × 100` : dead
- `tools/edu/capital-quiz.html` : `限时挑战：可选每题 10/15/20 秒倒计时，超时按答错处理。` : dead
- `tools/edu/chinese-zodiac.html` : `输入年份仍按公历直接换算，并提示「春节日期表仅覆盖 1980–2040 年」；结果可能因年初出生差一年，需以万年历核对。` : dead
- `tools/edu/convert-area-volume.html` : `千重量` : dead
- `tools/edu/convert-area-volume.html` : `千长度` : dead
- `tools/edu/convert-area-volume.html` : `毫重量` : dead
- `tools/edu/convert-area-volume.html` : `毫长度` : dead
- `tools/edu/country-quiz.html` : `即时反馈：答后给答案。` : dead
- `tools/edu/country-quiz.html` : `有答案？` : dead
- `tools/edu/country-quiz.html` : `本工具为纯前端在线工具，数据在浏览器本地处理、不上传服务器，依据对应领域标准与规范进行计算或处理，结果仅供参考。 工具名称：国家测验 - 教育学习领域的在线工具。` : dead
- `tools/edu/country-quiz.html` : `每题展示标准答案与正确率。` : dead
- `tools/edu/country-quiz.html` : `看国旗选国家，共 10 题并即时判分。` : dead
- `tools/edu/country-quiz.html` : `示例：出题「日本首都是？」应答「东京」。` : dead
- `tools/edu/country-quiz.html` : `覆盖常见国家基础地理常识。` : dead
- `tools/edu/country-quiz.html` : `错题库：强化易错项。` : dead
- `tools/edu/country-quiz.html` : `随机抽题：国家知识问答。` : dead
- `tools/edu/country-quiz.html` : `📚 深度解析：随机抽取国家相关题目（首都/国旗/位置）进行测验与判分，辅助地理识记。` : dead
- `tools/edu/generator-4.html` : `摘要按句子权重抽取：句子得分 = Σ 该句实词词频（可除以词总数归一）+ 位置加权（首段 ×1.5、含标题词 ×1.2）− 长度惩罚；按得分降序取前 k 句（k 由摘要长度或句数设定），再按原文顺序重排输出；压缩率 = 摘要字数 ÷ 原文字数 × 100%。` : dead
- `tools/edu/grade-weight-calculator.html` : `加权总分 = Σ(成绩ᵢ × 权重ᵢ / 100)` : dead
- `tools/edu/grade-weight-calculator.html` : `最终加权平均分 = 加权总分 / (总权重 / 100)` : dead
- `tools/edu/math-quiz.html` : `完成 20 道数学题，挑战满分` : dead
- `tools/edu/math-quiz.html` : `完成 30 道数学题，挑战满分` : dead
- `tools/edu/pinyin-converter.html` : `Matched whole-word first (e.g. 银行, 音乐, 头发, 好了); unseen words fall back to each character default reading, and unusual contexts still need manual correction.` : dead
- `tools/edu/pinyin-converter.html` : `Polyphones are matched whole-word first, e.g. 银行 → yín háng, 音乐 → yīn yuè, 头发 → tóu fà, 好了 → hǎo le` : dead
- `tools/edu/pinyin-typing-practice.html` : `💡 开启中文输入法后，按照上方文字输入即可` : dead
- `tools/edu/typing-game.html` : `排行：本地最高分。` : dead
- `tools/edu/typing-game.html` : `速度统计：WPM 与正确率。` : dead
- `tools/edu/word-memory.html` : `不认识词优先复现。` : dead
- `tools/edu/word-memory.html` : `内置基础词表，本地处理。` : dead
- `tools/edu/word-memory.html` : `建议在学习后 1天、3天、7天、15天、30天 各复习一次` : dead
- `tools/edu/word-memory.html` : `循环：错词反复练。` : dead
- `tools/edu/word-memory.html` : `标记：认识/不认识分流。` : dead
- `tools/edu/word-memory.html` : `翻卡识记：正面词反面音义。` : dead
- `tools/edu/word-memory.html` : `📚 深度解析：内置英语单词卡（音标+释义）进行翻卡与自测，支持认识/不认识标记循环复习。` : dead

  其它成因样例（共 29 条，仅列前 5）：
  - `tools/edu/calc-4.html` : `剩余权重 = 100 − 当前权重` : fragment
  - `tools/edu/convert-area-volume.html` : `摄氏度 ℃` : dynamic
  - `tools/edu/convert-area-volume.html` : `华氏度 ℉` : dynamic
  - `tools/edu/convert-area-volume.html` : `开尔文 K` : dynamic
  - `tools/edu/country-quiz.html` : `看图识国旗的国家测验` : fragment

### edu2（dead 3 / dynamic 0 / fragment 3 / harmless 0）

- `tools/edu2/exam-analysis.html` : `分数段分布：90–100%｜80–89%｜70–79%｜60–69%｜<60%（按满分比例）` : dead
- `tools/edu2/exam-analysis.html` : `排名按分数降序；等级：≥优秀线 优秀｜≥满分75% 良好｜≥及格线 及格｜其余不及格` : dead
- `tools/edu2/exam-analysis.html` : `整体水平：均分 ≥优秀线 优秀｜≥及格线 良好｜否则不及格` : dead

  其它成因样例（共 3 条，仅列前 5）：
  - `tools/edu2/schedule-conflict.html` : `无冲突排课率` : fragment
  - `tools/edu2/schedule-conflict.html` : `可视化课表` : fragment
  - `tools/edu2/schedule-conflict.html` : `节次` : fragment

### electrical（dead 8 / dynamic 45 / fragment 4 / harmless 11）

- `tools/electrical/detector-173.html` : `电气检查：电缆截面≥30mm²，接线端子压接牢固，接地电阻≤4Ω` : dead
- `tools/electrical/detector-173.html` : `额定功率：15 kW | 工作电压：380 V` : dead
- `tools/electrical/dianhuaxuedunhuakongzhi.html` : `依据 Pourbaix 图：电位 E 与 pH 判定免蚀/活化/钝化/过钝化` : dead
- `tools/electrical/index.html` : `电气工程工具集合收录了 17 个免费在线工具，覆盖电气工程场景下的常见计算、换算与查询需求。无论你是相关领域的从业者、学生还是普通用户，都能在这里找到即用即走的实用小工具。所有工具纯前端运行，数据不上传服务器，保护隐私安全。` : dead
- `tools/electrical/power-7.html` : `算法：需用功率 Pj = 总功率×同时系数；计算电流 Ij = Pj×1000/(U×cosφ)；断路器取 ≥ Ij×1.25 的标准规格（16,20,25,32,40,50,63,80,100,125,160,200,250A）；导线取载流量 ≥ Ij×1.25 的最小规格（1.5/16、2.5/25、4/32、6/…(+80字)` : dead
- `tools/electrical/power-7.html` : `💡 需用功率 Pj=P×Kd；计算电流 Ij=Pj×1000/(U×cosφ)；断路器 In≥Ij×1.25；导线截面按载流量匹配。` : dead
- `tools/electrical/transformer-sizing.html` : `P=600×0.85=510kW；S选=510/(0.8×1.2)≈531kVA，按标准容量选 630kVA。` : dead
- `tools/electrical/transformer-sizing.html` : `负载 S=600kVA cosφ=0.85 同时 0.8 预留 1.2` : dead

  其它成因样例（共 60 条，仅列前 5）：
  - `tools/electrical/battery-bank.html` : `串联/并联数量必须为正整数（≥1）` : dynamic
  - `tools/electrical/battery-bank.html` : `放电深度 DoD 与效率 η 须在 1–100% 之间（0% DoD 无可用能量、效率不能超过 100%）` : dynamic
  - `tools/electrical/breaker-sizing.html` : `超出表内最大档` : dynamic
  - `tools/electrical/breaker-sizing.html` : `推荐额定电流` : fragment
  - `tools/electrical/calc-2.html` : `🧮 三相功率计算` : harmless

### electronics（dead 5 / dynamic 14 / fragment 2 / harmless 0）

- `tools/electronics/calc-63.html` : `A=I/(k·ΔT^b)；按 IPC-2221 外层系数 k=0.048 算得约 1.4mm，散热好可缩到 1.0mm。` : dead
- `tools/electronics/calc-63.html` : `电源走线：5A 铜厚 1oz 温升 10℃，外层最小约 2.8mm。` : dead
- `tools/electronics/crystal-divider.html` : `晶振分频与 PLL 倍频计算<br>整数分频：输出频率 = 晶振频率 / N（N≥1，须为正整数）；周期 T = 1/f<br>PLL：VCO 频率 = 晶振 / 预分频 × 倍频系数 M（预分频、输出分频、M 均为正整数）；输出 = VCO / 输出分频<br>目标频率匹配：理论分频比 = 晶振/目标；比率≥1 取整…(+70字)` : dead
- `tools/electronics/crystal-divider.html` : `核心计算公式（按输入变量）：Math.round(tgt÷xr)；Math.round(ratio)` : dead
- `tools/electronics/frequency-13.html` : `VSWR<2为可接受范围` : dead

  其它成因样例（共 16 条，仅列前 5）：
  - `tools/electronics/capacitor-calculator.html` : `充电电阻 R (Ω)` : dynamic
  - `tools/electronics/capacitor-calculator.html` : `充电至 99.3% (5τ)` : dynamic
  - `tools/electronics/capacitor-calculator.html` : `平均充电功率（0→5τ）` : dynamic
  - `tools/electronics/crystal-divider.html` : `分频系数需为正整数（≥1）` : dynamic
  - `tools/electronics/crystal-divider.html` : `前/后分频系数需为正整数（≥1）` : dynamic

### encode（dead 19 / dynamic 0 / fragment 0 / harmless 1）

- `tools/encode/ascii-readability.html` : `ASCII 占比 = (总数 − 非ASCII) / 总数` : dead
- `tools/encode/base58.html` : `Base58 每个字符约携带 log₂58 ≈ 5.86 比特信息` : dead
- `tools/encode/base64-length.html` : `字符数 = ⌈n/3⌉ × 4，末尾按余 1 补 2、余 2 补 1 个 =` : dead
- `tools/encode/base64-size.html` : `Base64 每 3 字节编码为 4 字符，增长约 33%` : dead
- `tools/encode/compression-ratio.html` : `压缩率 = (1 − 压缩后/原始) × 100%` : dead
- `tools/encode/convert-4.html` : `千ASCII` : dead
- `tools/encode/convert-4.html` : `千Unicode` : dead
- `tools/encode/convert-4.html` : `毫ASCII` : dead
- `tools/encode/convert-4.html` : `毫Unicode` : dead
- `tools/encode/crc.html` : `CRC-n 产生 n 位校验值` : dead
- `tools/encode/crc.html` : `Hex 长度 = ⌈n/4⌉` : dead
- `tools/encode/crc-error-rate.html` : `CRC 对随机错误的漏检概率 ≈ 2⁻ʳ` : dead
- `tools/encode/encode-2.html` : `汉明距离 = 两个等长串对应位不同的数量` : dead
- `tools/encode/encode-4.html` : `每个符号含点/划及间隔，实际时长约为点划数 × 1.5 个单位` : dead
- `tools/encode/encode-5.html` : `QR 码版本 1-40，容量随版本和纠错等级变化` : dead
- `tools/encode/encoding-redundancy.html` : `冗余 = (平均码长 − 熵) / 平均码长` : dead
- `tools/encode/huffman-avg-length.html` : `平均码长 = Σ(fᵢ / Σf) · lᵢ` : dead
- `tools/encode/huffman-avg-length.html` : `理论下界为信息熵 H` : dead
- `tools/encode/image-to-base64.html` : `支持 PNG / JPG / WebP / GIF，建议 < 5MB` : dead

  其它成因样例（共 1 条，仅列前 5）：
  - `tools/encode/convert-4.html` : `🔤 ASCII/Unicode/字符编码转换` : harmless

### endocrinology（dead 4 / dynamic 1 / fragment 0 / harmless 0）

- `tools/endocrinology/cycle-hormone.html` : `：卵泡期 <1.5 ng/mL，黄体期 3.3-25.6 ng/mL，黄体中期 >3 提示有排卵` : dead
- `tools/endocrinology/insulin-adjustment.html` : `当前血糖 14.0 mmol/L，目标 7.0，采用 1800 法则且每日总量 36 U 推出 ISF=(1800/36)=50 mmol/L/U：校正剂量=(14−7)/50=0.14 U，即约 1.4 U。提示：校正剂量应设安全上限并结合近期低血糖史。` : dead
- `tools/endocrinology/pcos-diagnosis.html` : `总睾酮 (ng/dL)` : dead
- `tools/endocrinology/short-stature-prediction.html` : `情况1：骨龄 ≈ 实际年龄（差值 ≤ 1岁） ⏎   预测身高 = 当前身高 × B/P系数 ⏎   （B为该骨龄对应骨龄身高百分位中位数，P为终身高系数） ⏎  ⏎ 情况2：骨龄 > 实际年龄（早熟型） ⏎   预测身高偏矮（生长空间缩小） ⏎  ⏎ 情况3：骨龄 < 实际年龄（延迟型，GHD常见） ⏎   预测身高…(+10字)` : dead

  其它成因样例（共 1 条，仅列前 5）：
  - `tools/endocrinology/cycle-hormone.html` : `导出明细 CSV` : dynamic

### energy（dead 24 / dynamic 27 / fragment 5 / harmless 2）

- `tools/energy/air-purifier-area.html` : `适用面积 ≈ CADR × 0.1 (m²)` : dead
- `tools/energy/assessor-water-quality.html` : `TDS 评级：按阈值分段判定水质` : dead
- `tools/energy/assessor-water-quality.html` : `TDS过低(<30mg/L)几乎不含矿物质，长期饮用需补充` : dead
- `tools/energy/battery-life.html` : `续航 = 容量(Wh) / 功耗(W)` : dead
- `tools/energy/calculator-calc-4.html` : `分贝叠加 L = 10·log₁₀(Σ10^(L_i/10))` : dead
- `tools/energy/calculator-calc-power-usage.html` : `阶梯电费 = Σ 各档电量 × 档位电价` : dead
- `tools/energy/convert-emission.html` : `CO₂当量 = 质量 × GWP` : dead
- `tools/energy/daily-irradiation.html` : `日辐照量 = 峰值 × 等效日照时数` : dead
- `tools/energy/energy-cost.html` : `电费 = P × t × 电价` : dead
- `tools/energy/energy-efficiency.html` : `能效 = 输出 / 输入` : dead
- `tools/energy/energy-payback.html` : `回收期 = 投资 / 年节约额` : dead
- `tools/energy/estimate-area.html` : `发电量 = 面积 × 辐照 × 效率 × 小时` : dead
- `tools/energy/estimate-time-current.html` : `充电时间 = 容量 / 电流` : dead
- `tools/energy/fridge-power-estimator.html` : `日耗电 ≈ 额定功率 × 24 × 负载系数` : dead
- `tools/energy/fuel-heat-value.html` : `热量 = 质量 × 低位热值` : dead
- `tools/energy/heat-pump-cop.html` : `制冷量与输入功率均须大于 0。` : dead
- `tools/energy/heat-pump-cop.html` : `制热量与输入功率均须大于 0。` : dead
- `tools/energy/index.html` : `能源电力工具集合收录了 39 个免费在线工具，覆盖能源电力场景下的常见计算、换算与查询需求。无论你是相关领域的从业者、学生还是普通用户，都能在这里找到即用即走的实用小工具。所有工具纯前端运行，数据不上传服务器，保护隐私安全。` : dead
- `tools/energy/lcoe.html` : `LCOE = 生命周期成本 / 总发电量` : dead
- `tools/energy/power-consumption.html` : `用电 = P × t` : dead
- `tools/energy/solar-calculator.html` : `发电 = 面积 × 辐照 × 效率` : dead
- `tools/energy/standby-power-calculator.html` : `待机功耗 = Σ(P_i × t_i)` : dead
- `tools/energy/thermal-efficiency.html` : `η = 输出 / 输入` : dead
- `tools/energy/wind-power-estimator.html` : `；本次采用 Cp=` : dead

  其它成因样例（共 34 条，仅列前 5）：
  - `tools/energy/carbon-footprint.html` : `碳足迹 = Σ(活动量 × 排放因子)` : fragment
  - `tools/energy/carnot-efficiency.html` : `低温 T_c 须 ≥0 且小于高温 T_h（单位 K）；请确认未误填摄氏温度或高低颠倒。` : dynamic
  - `tools/energy/daily-irradiation.html` : `24h 理论上限 (kWh/m²)` : dynamic
  - `tools/energy/daily-irradiation.html` : `请输入有效的峰值辐照度（>0，W/m²）与等效日照时数（≥0，h）。` : dynamic
  - `tools/energy/electrical-power.html` : `⚠ 请输入有效参数：电压与电流均须大于 0。` : dynamic

### engineering（dead 9 / dynamic 3 / fragment 0 / harmless 1）

- `tools/engineering/heat-transfer.html` : `请输入有效参数：发射率 ε 须在 0–1 之间，面积 A > 0，绝对温度 T₁、T₂ > 0 K。` : dead
- `tools/engineering/index.html` : `圆轴扭转剪应力计算` : dead
- `tools/engineering/index.html` : `圆轴扭转剪应力计算器。输入扭矩、轴半径与极惯性矩，按 τ = T·r/J 求圆轴最大扭转剪应力，用于传动轴强度校核与直径选型。` : dead
- `tools/engineering/index.html` : `工程计算工具集合收录了 14 个免费在线工具，覆盖工程计算场景下的常见计算、换算与查询需求。无论你是相关领域的从业者、学生还是普通用户，都能在这里找到即用即走的实用小工具。所有工具纯前端运行，数据不上传服务器，保护隐私安全。` : dead
- `tools/engineering/index.html` : `螺栓预紧力计算` : dead
- `tools/engineering/index.html` : `螺栓预紧力计算器。输入螺栓规格、摩擦系数与目标夹紧力等参数，计算所需预紧力矩与预紧力，适用于法兰、连接件装配的螺栓拧紧工艺设计。` : dead
- `tools/engineering/index.html` : `角焊缝强度计算` : dead
- `tools/engineering/index.html` : `角焊缝强度计算器。输入焊脚尺寸、焊缝长度与钢材许用应力，按角焊缝有效截面积求承载剪力与强度，用于钢结构焊接节点设计与验算。` : dead
- `tools/engineering/thermal-expansion.html` : `热膨胀伸长：ΔL = α · L₀ · ΔT；α 线膨胀系数、L₀ 原长、ΔT 温差。` : dead

  其它成因样例（共 4 条，仅列前 5）：
  - `tools/engineering/heat-transfer.html` : `请输入有效参数：导热系数 k、面积 A、厚度 L 均须 > 0，温度须为有效数值。` : dynamic
  - `tools/engineering/heat-transfer.html` : `请输入有效参数：对流换热系数 h、面积 A 均须 > 0，表面/流体温度须为有效数值。` : dynamic
  - `tools/engineering/heat-transfer.html` : `请输入有效参数：k、A、L、h₁、h₂ 均须 > 0，温度须为有效数值。` : dynamic
  - `tools/engineering/material-calculator.html` : `🧮 材料截面计算` : harmless

### ent（dead 1 / dynamic 0 / fragment 0 / harmless 0）

- `tools/ent/tympanometry.html` : `B型鼓室图伴ECV异常增大提示鼓膜穿孔；C型鼓室图峰压-100~-200daPa为C1型（轻度负压），<-200daPa为C2型（重度负压）。声导抗是中耳功能筛查的重要工具，结合纯音测听可鉴别传导性与感音神经性聋。` : dead

### express（dead 4 / dynamic 0 / fragment 0 / harmless 0）

- `tools/express/insurance-fee.html` : `不一定。理赔上限为 min(声明价值, 单票保价上限)，超出上限的部分不予赔付；此外常有免赔额或比例免赔，且需证明物品实际价值（发票或凭证）。保价费是风险转移成本，并非越高越好，按物品真实价值声明即可。` : dead
- `tools/express/insurance-fee.html` : `以「顺丰速运、声明价值 1 万元、保价上限 2 万元」为例` : dead
- `tools/express/insurance-fee.html` : `保价费 = 声明价值 × 费率，并按快递公司规则取上下限：费率通常 0.5% 至 1%（如顺丰约 0.5%、EMS 约 1%），最低收费 1 元起、单票最高保额多为 2 万至 10 万元；实际费用 = min(max(声明价值 × 费率, 最低收费), 最高封顶)，超出保额部分的损失不予赔付。` : dead
- `tools/express/insurance-fee.html` : `保价费=声明价值×0.5%=50 元（最低 1 元）；理赔上限=min(10000, 20000)=10000 元，未超上限可足额承保。若选中国邮政 EMS（费率 1%）则保价费=100 元。声明价值 3 万元时，理赔上限仍为 2 万元、超出 1 万元不赔，保价费按 3 万元×费率收取。` : dead

### fengshui（dead 4 / dynamic 1 / fragment 0 / harmless 0）

- `tools/fengshui/birthday-analysis.html` : `Good Day Selector - pick an activity and start date to see auspicious days from the Jian-Chu (十二建除) almanac. Cultural reference only.` : dead
- `tools/fengshui/fengshui-calculator.html` : `Good Day Selector - pick an activity and start date to see auspicious days from the Jian-Chu (十二建除) almanac. Cultural reference only.` : dead
- `tools/fengshui/fengshui-guide.html` : `Good Day Selector - pick an activity and start date to see auspicious days from the Jian-Chu (十二建除) almanac. Cultural reference only.` : dead
- `tools/fengshui/zodiac-lookup.html` : `Good Day Selector - pick an activity and start date to see auspicious days from the Jian-Chu (十二建除) almanac. Cultural reference only.` : dead

  其它成因样例（共 1 条，仅列前 5）：
  - `tools/fengshui/zodiac-lookup.html` : `✅ 六合 / 三合贵人` : dynamic

### finance（dead 638 / dynamic 549 / fragment 74 / harmless 1）

- `tools/finance/amount-in-words.html` : `按中文大写金额规则：数字分组（万/亿）+ 单位（元/角/分）+ 零位特殊处理` : dead
- `tools/finance/analysis-5.html` : `(流动资产 500000.00 − 存货 180000.00 − 预付费用 20000.00) ÷ 流动负债 300000.00` : dead
- `tools/finance/analysis-5.html` : `元，所有者权益 = 资产 1200000.00 − 负债 700000.00 =` : dead
- `tools/finance/analysis-5.html` : `勾稽校验：权益乘数 = 1 ÷ (1 − 资产负债率) = 1 ÷ (1 − 0.5833) = 2.40` : dead
- `tools/finance/analysis-5.html` : `流动资产 500000.00 ÷ 流动负债 300000.00` : dead
- `tools/finance/analysis-5.html` : `现金 80000.00 ÷ 流动负债 300000.00` : dead
- `tools/finance/analysis-5.html` : `营运资金 = 流动资产 500000.00 − 流动负债 300000.00 =` : dead
- `tools/finance/analysis-5.html` : `负债总额 700000.00 ÷ 所有者权益 500000.00` : dead
- `tools/finance/analysis-5.html` : `负债总额 700000.00 ÷ 资产总额 1200000.00` : dead
- `tools/finance/analysis-5.html` : `资产总额 1200000.00 ÷ 所有者权益 500000.00` : dead
- `tools/finance/analysis-risk.html` : `EBIT = 贡献边际 400000.00 − 固定成本 200000.00 =` : dead
- `tools/finance/analysis-risk.html` : `元；EPS = 112500.00 ÷ 100000 =` : dead
- `tools/finance/analysis-risk.html` : `净利润 = (200000.00 − 50000.00) × (1 − 25.00%) =` : dead
- `tools/finance/analysis-risk.html` : `利息保障倍数 4.00，经营利润对利息的覆盖较为充足。` : dead
- `tools/finance/analysis-risk.html` : `利息保障倍数 = 200000.00 ÷ 50000.00 =` : dead
- `tools/finance/analysis-risk.html` : `贡献边际 = 1000000.00 − 600000.00 =` : dead
- `tools/finance/analysis-risk.html` : `：EBIT 每变动 1%，EPS 变动约 1.33%` : dead
- `tools/finance/analysis-risk.html` : `：营业收入每变动 1%，EBIT 变动约 2.00%` : dead
- `tools/finance/analysis-risk.html` : `：营业收入每变动 1%，EPS 变动约 2.67%` : dead
- `tools/finance/assessor-manager.html` : `信用评分 = Σ(各指标分档得分 × 权重)；授信额度按评分档位核定` : dead
- `tools/finance/bond-yield-calculator.html` : `* YTM为年化收益率，假设利息按YTM再投资` : dead
- `tools/finance/break-even-calculator.html` : `变动成本总额：240,000.00 元` : dead
- `tools/finance/break-even-calculator.html` : `固定成本总额：100,000.00 元` : dead
- `tools/finance/break-even-calculator.html` : `总成本：340,000.00 元` : dead
- `tools/finance/break-even-calculator.html` : `所得税（25%）：15,000.00 元` : dead
- `tools/finance/break-even-calculator.html` : `（销量每增1%，利润增2.67%）` : dead
- `tools/finance/cagr.html` : `CAGR ≈ 10.41%。 几何平均而非算术平均。` : dead
- `tools/finance/calc-4.html` : `第 10 期` : dead
- `tools/finance/calc-4.html` : `第 11 期` : dead
- `tools/finance/calc-4.html` : `第 12 期` : dead
- `tools/finance/calc-4.html` : `第 360 期` : dead
- `tools/finance/calc-4.html` : `第 6 期` : dead
- `tools/finance/calc-4.html` : `第 7 期` : dead
- `tools/finance/calc-4.html` : `第 8 期` : dead
- `tools/finance/calc-4.html` : `第 9 期` : dead
- `tools/finance/cnpj-validator.html` : `CNPJ 两位校验位按 mod-11：权重循环 2..9，Σ(权重 × 数字) mod 11，余数 < 2 取 0，否则取 11 − 余数` : dead
- `tools/finance/credit-card-grace-period.html` : `下下期 25 日` : dead
- `tools/finance/credit-card-grace-period.html` : `大额消费安排在账单日次日最划算；取现与分期无免息期。若将 ¥10,000.00 延后 44 天还款并按 2% 年化理财，可多赚约 ¥24.11（需确保还款日按时还清，否则利息远超收益）。` : dead
- `tools/finance/credit-card-grace-period.html` : `最长免息期资金收益（2%年化）` : dead
- `tools/finance/credit-card-interest.html` : `⚠️ 最低还款利息成本很高，年化利率约 18.25%` : dead
- `tools/finance/credit-card-interest.html` : `信用卡常见日利率约万分之五（0.05%），名义年化 ≈ 0.05%×365 = 18.25%，按月结算的有效年化 ≈ 19.56%。未全额还款则从消费日起` : dead
- `tools/finance/credit-card-interest.html` : `信用卡循环利息 ≈ 消费金额 × 日利率(0.05%) × 计息天数；按月计收复利。` : dead
- `tools/finance/credit-card-interest.html` : `日息万五叠加「未全额即失去免息、从入账日计息」的规则，名义年化约 18%，按月复利的有效年化约 19.56%，远高于普通贷款，故信用卡宜全额按时还。` : dead
- `tools/finance/credit-card-interest.html` : `最低还款年化利率约 18.25%，远高于普通贷款，仅适合短期周转。` : dead
- `tools/finance/credit-card-interest.html` : `滞纳金` : dead
- `tools/finance/credit-card-interest.html` : `滞纳金总额` : dead
- `tools/finance/credit-card-interest.html` : `错过还款日会产生滞纳金并影响征信，建议设置自动还款。` : dead
- `tools/finance/currency-converter.html` : `目标金额 = 原金额 × 汇率(目标币/原币)` : dead
- `tools/finance/currency-symbol.html` : `170+ 种货币符号、代码、国家/地区快速查询` : dead
- `tools/finance/currency-symbol.html` : `AED · 阿联酋迪拉姆` : dead
- `tools/finance/currency-symbol.html` : `AFN · 阿富汗尼` : dead
- `tools/finance/currency-symbol.html` : `AMD · 亚美尼亚德拉姆` : dead
- `tools/finance/currency-symbol.html` : `ANG · 荷属安的列斯盾` : dead
- `tools/finance/currency-symbol.html` : `AOA · 安哥拉宽扎` : dead
- `tools/finance/currency-symbol.html` : `ARS · 阿根廷比索` : dead
- `tools/finance/currency-symbol.html` : `AUD · 澳元` : dead
- `tools/finance/currency-symbol.html` : `AUD · 澳大利亚元` : dead
- `tools/finance/currency-symbol.html` : `AWG · 阿鲁巴弗罗林` : dead
- `tools/finance/currency-symbol.html` : `AZN · 阿塞拜疆马纳特` : dead
- `tools/finance/currency-symbol.html` : `BBD · 巴巴多斯元` : dead
- `tools/finance/currency-symbol.html` : `BDT · 孟加拉国塔卡` : dead
- `tools/finance/currency-symbol.html` : `BGN · 保加利亚列弗` : dead
- `tools/finance/currency-symbol.html` : `BHD · 巴林第纳尔` : dead
- `tools/finance/currency-symbol.html` : `BIF · 布隆迪法郎` : dead
- `tools/finance/currency-symbol.html` : `BND · 文莱元` : dead
- `tools/finance/currency-symbol.html` : `BOB · 玻利维亚诺` : dead
- `tools/finance/currency-symbol.html` : `BRL · 巴西雷亚尔` : dead
- `tools/finance/currency-symbol.html` : `BSD · 巴哈马元` : dead
- `tools/finance/currency-symbol.html` : `BTN · 不丹努扎姆` : dead
- `tools/finance/currency-symbol.html` : `BWP · 博茨瓦纳普拉` : dead
- `tools/finance/currency-symbol.html` : `BZD · 伯利兹元` : dead
- `tools/finance/currency-symbol.html` : `CAD · 加元` : dead
- `tools/finance/currency-symbol.html` : `CDF · 刚果法郎` : dead
- `tools/finance/currency-symbol.html` : `CHF · 瑞士法郎` : dead
- `tools/finance/currency-symbol.html` : `CLF · 智利发展单位` : dead
- `tools/finance/currency-symbol.html` : `CLP · 智利比索` : dead
- `tools/finance/currency-symbol.html` : `CNH · 离岸人民币` : dead
- `tools/finance/currency-symbol.html` : `CNY · 人民币` : dead
- `tools/finance/currency-symbol.html` : `COP · 哥伦比亚比索` : dead
- `tools/finance/currency-symbol.html` : `CRC · 哥斯达黎加科朗` : dead
- `tools/finance/currency-symbol.html` : `CUP · 古巴比索` : dead
- `tools/finance/currency-symbol.html` : `CZK · 捷克克朗` : dead
- `tools/finance/currency-symbol.html` : `DJF · 吉布提法郎` : dead
- `tools/finance/currency-symbol.html` : `DKK · 丹麦克朗` : dead
- `tools/finance/currency-symbol.html` : `DOP · 多米尼加比索` : dead
- `tools/finance/currency-symbol.html` : `DZD · 阿尔及利亚第纳尔` : dead
- `tools/finance/currency-symbol.html` : `EGP · 埃及镑` : dead
- `tools/finance/currency-symbol.html` : `ERN · 厄立特里亚纳克法` : dead
- `tools/finance/currency-symbol.html` : `ETB · 埃塞俄比亚比尔` : dead
- `tools/finance/currency-symbol.html` : `ETH · 以太坊` : dead
- `tools/finance/currency-symbol.html` : `EUR · 欧元` : dead
- `tools/finance/currency-symbol.html` : `FJD · 斐济元` : dead
- `tools/finance/currency-symbol.html` : `FKP · 福克兰群岛镑` : dead
- `tools/finance/currency-symbol.html` : `GBP · 英镑` : dead
- `tools/finance/currency-symbol.html` : `GBX · 便士` : dead
- `tools/finance/currency-symbol.html` : `GEL · 格鲁吉亚拉里` : dead
- `tools/finance/currency-symbol.html` : `GGP · 根西岛镑` : dead
- `tools/finance/currency-symbol.html` : `GHS · 加纳塞地` : dead
- `tools/finance/currency-symbol.html` : `GIP · 直布罗陀镑` : dead
- `tools/finance/currency-symbol.html` : `GMD · 冈比亚达拉西` : dead
- `tools/finance/currency-symbol.html` : `GTQ · 危地马拉格查尔` : dead
- `tools/finance/currency-symbol.html` : `GYD · 圭亚那元` : dead
- `tools/finance/currency-symbol.html` : `HKD · 港币` : dead
- `tools/finance/currency-symbol.html` : `HNL · 洪都拉斯伦皮拉` : dead
- `tools/finance/currency-symbol.html` : `HRK · 克罗地亚库纳` : dead
- `tools/finance/currency-symbol.html` : `HTG · 海地古德` : dead
- `tools/finance/currency-symbol.html` : `HUF · 匈牙利福林` : dead
- `tools/finance/currency-symbol.html` : `IDR · 印尼盾` : dead
- `tools/finance/currency-symbol.html` : `ILS · 以色列新谢克尔` : dead
- `tools/finance/currency-symbol.html` : `IMP · 马恩岛镑` : dead
- `tools/finance/currency-symbol.html` : `INR · 印度卢比` : dead
- `tools/finance/currency-symbol.html` : `IQD · 伊拉克第纳尔` : dead
- `tools/finance/currency-symbol.html` : `ISK · 冰岛克朗` : dead
- `tools/finance/currency-symbol.html` : `JEP · 泽西岛镑` : dead
- `tools/finance/currency-symbol.html` : `JMD · 牙买加元` : dead
- `tools/finance/currency-symbol.html` : `JOD · 约旦第纳尔` : dead
- `tools/finance/currency-symbol.html` : `JPY · 日元` : dead
- `tools/finance/currency-symbol.html` : `KES · 肯尼亚先令` : dead
- `tools/finance/currency-symbol.html` : `KGS · 吉尔吉斯斯坦索姆` : dead
- `tools/finance/currency-symbol.html` : `KHR · 柬埔寨瑞尔` : dead
- `tools/finance/currency-symbol.html` : `KID · 基里巴斯元` : dead
- `tools/finance/currency-symbol.html` : `KMF · 科摩罗法郎` : dead
- `tools/finance/currency-symbol.html` : `KPW · 朝鲜圆` : dead
- `tools/finance/currency-symbol.html` : `KRW · 韩元` : dead
- `tools/finance/currency-symbol.html` : `KWD · 科威特第纳尔` : dead
- `tools/finance/currency-symbol.html` : `KZT · 哈萨克斯坦坚戈` : dead
- `tools/finance/currency-symbol.html` : `LAK · 老挝基普` : dead
- `tools/finance/currency-symbol.html` : `LBP · 黎巴嫩镑` : dead
- `tools/finance/currency-symbol.html` : `LKR · 斯里兰卡卢比` : dead
- `tools/finance/currency-symbol.html` : `LRD · 利比里亚元` : dead
- `tools/finance/currency-symbol.html` : `LSL · 莱索托洛蒂` : dead
- `tools/finance/currency-symbol.html` : `LYD · 利比亚第纳尔` : dead
- `tools/finance/currency-symbol.html` : `MAD · 摩洛哥迪拉姆` : dead
- `tools/finance/currency-symbol.html` : `MGA · 马达加斯加阿里亚里` : dead
- `tools/finance/currency-symbol.html` : `MMK · 缅甸缅元` : dead
- `tools/finance/currency-symbol.html` : `MNT · 蒙古图格里克` : dead
- `tools/finance/currency-symbol.html` : `MOP · 澳门元` : dead
- `tools/finance/currency-symbol.html` : `MUR · 毛里求斯卢比` : dead
- `tools/finance/currency-symbol.html` : `MVR · 马尔代夫拉菲亚` : dead
- `tools/finance/currency-symbol.html` : `MXN · 墨西哥比索` : dead
- `tools/finance/currency-symbol.html` : `MYR · 马来西亚林吉特` : dead
- `tools/finance/currency-symbol.html` : `MZN · 莫桑比克梅蒂卡尔` : dead
- `tools/finance/currency-symbol.html` : `NAD · 纳米比亚元` : dead
- `tools/finance/currency-symbol.html` : `NGN · 尼日利亚奈拉` : dead
- `tools/finance/currency-symbol.html` : `NIO · 尼加拉瓜科多巴` : dead
- `tools/finance/currency-symbol.html` : `NOK · 挪威克朗` : dead
- `tools/finance/currency-symbol.html` : `NPR · 尼泊尔卢比` : dead
- `tools/finance/currency-symbol.html` : `NZD · 新西兰元` : dead
- `tools/finance/currency-symbol.html` : `OMR · 阿曼里亚尔` : dead
- `tools/finance/currency-symbol.html` : `PAB · 巴拿马巴波亚` : dead
- `tools/finance/currency-symbol.html` : `PEN · 秘鲁索尔` : dead
- `tools/finance/currency-symbol.html` : `PGK · 巴布亚新几内亚基那` : dead
- `tools/finance/currency-symbol.html` : `PHP · 菲律宾比索` : dead
- `tools/finance/currency-symbol.html` : `PKR · 巴基斯坦卢比` : dead
- `tools/finance/currency-symbol.html` : `PLN · 波兰兹罗提` : dead
- `tools/finance/currency-symbol.html` : `PYG · 巴拉圭瓜拉尼` : dead
- `tools/finance/currency-symbol.html` : `QAR · 卡塔尔里亚尔` : dead
- `tools/finance/currency-symbol.html` : `RON · 罗马尼亚列伊` : dead
- `tools/finance/currency-symbol.html` : `RUB · 俄罗斯卢布` : dead
- `tools/finance/currency-symbol.html` : `RWF · 卢旺达法郎` : dead
- `tools/finance/currency-symbol.html` : `SAR · 沙特里亚尔` : dead
- `tools/finance/currency-symbol.html` : `SBD · 所罗门群岛元` : dead
- `tools/finance/currency-symbol.html` : `SCR · 塞舌尔卢比` : dead
- `tools/finance/currency-symbol.html` : `SDG · 苏丹镑` : dead
- `tools/finance/currency-symbol.html` : `SEK · 瑞典克朗` : dead
- `tools/finance/currency-symbol.html` : `SGD · 新加坡元` : dead
- `tools/finance/currency-symbol.html` : `SHP · 圣赫勒拿镑` : dead
- `tools/finance/currency-symbol.html` : `SLL · 塞拉利昂利昂` : dead
- `tools/finance/currency-symbol.html` : `SOS · 索马里先令` : dead
- `tools/finance/currency-symbol.html` : `SRD · 苏里南元` : dead
- `tools/finance/currency-symbol.html` : `SSP · 南苏丹镑` : dead
- `tools/finance/currency-symbol.html` : `SVC · 萨尔瓦多科朗` : dead
- `tools/finance/currency-symbol.html` : `SYP · 叙利亚镑` : dead
- `tools/finance/currency-symbol.html` : `SZL · 斯威士兰里兰吉尼` : dead
- `tools/finance/currency-symbol.html` : `THB · 泰铢` : dead
- `tools/finance/currency-symbol.html` : `TJS · 塔吉克斯坦索莫尼` : dead
- `tools/finance/currency-symbol.html` : `TMT · 土库曼斯坦马纳特` : dead
- `tools/finance/currency-symbol.html` : `TND · 突尼斯第纳尔` : dead
- `tools/finance/currency-symbol.html` : `TOP · 汤加潘加` : dead
- `tools/finance/currency-symbol.html` : `TRY · 土耳其里拉` : dead
- `tools/finance/currency-symbol.html` : `TTD · 特立尼达和多巴哥元` : dead
- `tools/finance/currency-symbol.html` : `TVD · 图瓦卢元` : dead
- `tools/finance/currency-symbol.html` : `TWD · 新台币` : dead
- `tools/finance/currency-symbol.html` : `TZS · 坦桑尼亚先令` : dead
- `tools/finance/currency-symbol.html` : `UGX · 乌干达先令` : dead
- `tools/finance/currency-symbol.html` : `USD · 美元` : dead
- `tools/finance/currency-symbol.html` : `UYU · 乌拉圭比索` : dead
- `tools/finance/currency-symbol.html` : `UZS · 乌兹别克斯坦苏姆` : dead
- `tools/finance/currency-symbol.html` : `VEF · 委内瑞拉玻利瓦尔` : dead
- `tools/finance/currency-symbol.html` : `VND · 越南盾` : dead
- `tools/finance/currency-symbol.html` : `VUV · 瓦努阿图瓦图` : dead
- `tools/finance/currency-symbol.html` : `WST · 萨摩亚塔拉` : dead
- `tools/finance/currency-symbol.html` : `XAF · 中非法郎` : dead
- `tools/finance/currency-symbol.html` : `XBT · 比特币` : dead
- `tools/finance/currency-symbol.html` : `XCD · 东加勒比元` : dead
- `tools/finance/currency-symbol.html` : `XOF · 西非法郎` : dead
- `tools/finance/currency-symbol.html` : `XPF · 太平洋法郎` : dead
- `tools/finance/currency-symbol.html` : `YER · 也门里亚尔` : dead
- `tools/finance/currency-symbol.html` : `ZAR · 南非兰特` : dead
- `tools/finance/currency-symbol.html` : `共找到 153 种货币` : dead
- `tools/finance/dca-calculator.html` : `年（共120期），预期年化` : dead
- `tools/finance/dca-calculator.html` : `（高于定投 44.63%）` : dead
- `tools/finance/dca-calculator.html` : `💡 对比：若一次性投入 ¥120,000，期末资产约` : dead
- `tools/finance/discount-calculator.html` : `节省 ¥ 20.00（20.0% OFF）` : dead
- `tools/finance/esn-validator.html` : `格式 ^[0-9A-Fa-f]{8}$（8 位十六进制）` : dead
- `tools/finance/futures-pnl-calculator.html` : `IF 点` : dead
- `tools/finance/generator-report-1.html` : `#1 模拟报表（单位：万元）` : dead
- `tools/finance/generator-report-1.html` : `#2 模拟报表（单位：万元）` : dead
- `tools/finance/generator-report-1.html` : `#3 模拟报表（单位：万元）` : dead
- `tools/finance/generator-report-1.html` : `#4 模拟报表（单位：万元）` : dead
- `tools/finance/generator-report-1.html` : `#5 模拟报表（单位：万元）` : dead
- `tools/finance/generator-report-1.html` : `利润表：营业收入 279.98，营业成本 146.56，净利润 133.42` : dead
- `tools/finance/generator-report-1.html` : `利润表：营业收入 435.85，营业成本 246.31，净利润 189.54` : dead
- `tools/finance/generator-report-1.html` : `利润表：营业收入 522.36，营业成本 268.92，净利润 253.44` : dead
- `tools/finance/generator-report-1.html` : `利润表：营业收入 535.60，营业成本 373.93，净利润 161.67` : dead
- `tools/finance/generator-report-1.html` : `利润表：营业收入 593.90，营业成本 396.08，净利润 197.82` : dead
- `tools/finance/generator-report-1.html` : `现金流量表：经营 121.92，投资 -39.92，筹资 -20.17` : dead
- `tools/finance/generator-report-1.html` : `现金流量表：经营 141.46，投资 -59.02，筹资 -20.27` : dead
- `tools/finance/generator-report-1.html` : `现金流量表：经营 161.37，投资 -45.17，筹资 -44.20` : dead
- `tools/finance/generator-report-1.html` : `现金流量表：经营 165.11，投资 -41.19，筹资 -43.44` : dead
- `tools/finance/generator-report-1.html` : `现金流量表：经营 217.14，投资 -95.91，筹资 -52.44` : dead
- `tools/finance/generator-report-1.html` : `资产负债表：资产 1058.20，负债 378.16，所有者权益 680.04` : dead
- `tools/finance/generator-report-1.html` : `资产负债表：资产 437.65，负债 194.27，所有者权益 243.38` : dead
- `tools/finance/generator-report-1.html` : `资产负债表：资产 627.27，负债 435.96，所有者权益 191.31` : dead
- `tools/finance/generator-report-1.html` : `资产负债表：资产 755.58，负债 507.51，所有者权益 248.07` : dead
- `tools/finance/generator-report-1.html` : `资产负债表：资产 845.60，负债 575.79，所有者权益 269.81` : dead
- `tools/finance/gold-price-calculator.html` : `金额 = 克重 × 纯度 × 单价；单位换算：1 盎司 ≈ 31.1035 克` : dead
- `tools/finance/housing-fund-loan.html` : `⚠️ 贷款利率按首套公积金贷款利率3.1%估算（2024年参考）。` : dead
- `tools/finance/housing-fund-loan.html` : `公积金贷款 = f(余额, 缴存)` : dead
- `tools/finance/housing-fund-loan.html` : `如：2000` : dead
- `tools/finance/housing-fund-loan.html` : `如：5` : dead
- `tools/finance/housing-fund-loan.html` : `月缴存额（元）` : dead
- `tools/finance/housing-fund-loan.html` : `首套公积金贷款利率约 3.1%，据此估算月供与总利息。` : dead
- `tools/finance/inflation-calculator.html` : `第11年` : dead
- `tools/finance/inflation-calculator.html` : `第12年` : dead
- `tools/finance/inflation-calculator.html` : `第13年` : dead
- `tools/finance/inflation-calculator.html` : `第14年` : dead
- `tools/finance/inflation-calculator.html` : `第15年` : dead
- `tools/finance/inflation-calculator.html` : `第16年` : dead
- `tools/finance/inflation-calculator.html` : `第17年` : dead
- `tools/finance/inflation-calculator.html` : `第18年` : dead
- `tools/finance/inflation-calculator.html` : `第19年` : dead
- `tools/finance/inflation-calculator.html` : `第20年` : dead
- `tools/finance/investment-calculator.html` : `年化收益率 CAGR = (期末价值 / 总投入)^(1 / 年数) − 1` : dead
- `tools/finance/investment-calculator.html` : `累计回报率 = (期末价值 − 总投入) / 总投入` : dead
- `tools/finance/invoice-generator.html` : `不含税金额 = 价税合计 / (1 + 税率)；税额 = 不含税金额 × 税率` : dead
- `tools/finance/irr-calculator.html` : `• IRR < 折现率：项目不可行，不建议投资` : dead
- `tools/finance/irr-calculator.html` : `• NPV < 0：投资收益低于预期，不可行` : dead
- `tools/finance/isbn-validator.html` : `ISBN 验证与转换。ISBN-10（mod-11）：前 9 位分别乘以权重 10,9,8,…,2，求和后加校验位，总和能被 11 整除则通过。校验位为 10 时用 X 表示。 ⏎       ISBN-13（mod-10）：12 位数字交替乘以 1 和 3，求和后` : dead
- `tools/finance/lease-payment-calculator.html` : `· 期末还款` : dead
- `tools/finance/lease-payment-calculator.html` : `导出明细 CSV` : dead
- `tools/finance/lease-payment-calculator.html` : `期（3.0年）` : dead
- `tools/finance/lease-payment-calculator.html` : `每月还款：¥3,042.19` : dead
- `tools/finance/lease-payment-calculator.html` : `每期租金 = V·i·(1+i)ⁿ / ((1+i)ⁿ − 1)（V 租赁物价值，i 期利率，n 期数）` : dead
- `tools/finance/loan-amortization.html` : `第100期` : dead
- `tools/finance/loan-amortization.html` : `第101期` : dead
- `tools/finance/loan-amortization.html` : `第102期` : dead
- `tools/finance/loan-amortization.html` : `第103期` : dead
- `tools/finance/loan-amortization.html` : `第104期` : dead
- `tools/finance/loan-amortization.html` : `第105期` : dead
- `tools/finance/loan-amortization.html` : `第106期` : dead
- `tools/finance/loan-amortization.html` : `第107期` : dead
- `tools/finance/loan-amortization.html` : `第108期` : dead
- `tools/finance/loan-amortization.html` : `第109期` : dead
- `tools/finance/loan-amortization.html` : `第110期` : dead
- `tools/finance/loan-amortization.html` : `第111期` : dead
- `tools/finance/loan-amortization.html` : `第112期` : dead
- `tools/finance/loan-amortization.html` : `第113期` : dead
- `tools/finance/loan-amortization.html` : `第114期` : dead
- `tools/finance/loan-amortization.html` : `第115期` : dead
- `tools/finance/loan-amortization.html` : `第116期` : dead
- `tools/finance/loan-amortization.html` : `第117期` : dead
- `tools/finance/loan-amortization.html` : `第118期` : dead
- `tools/finance/loan-amortization.html` : `第119期` : dead
- `tools/finance/loan-amortization.html` : `第120期` : dead
- `tools/finance/loan-amortization.html` : `第121期` : dead
- `tools/finance/loan-amortization.html` : `第122期` : dead
- `tools/finance/loan-amortization.html` : `第123期` : dead
- `tools/finance/loan-amortization.html` : `第124期` : dead
- `tools/finance/loan-amortization.html` : `第125期` : dead
- `tools/finance/loan-amortization.html` : `第126期` : dead
- `tools/finance/loan-amortization.html` : `第127期` : dead
- `tools/finance/loan-amortization.html` : `第128期` : dead
- `tools/finance/loan-amortization.html` : `第129期` : dead
- `tools/finance/loan-amortization.html` : `第130期` : dead
- `tools/finance/loan-amortization.html` : `第131期` : dead
- `tools/finance/loan-amortization.html` : `第132期` : dead
- `tools/finance/loan-amortization.html` : `第133期` : dead
- `tools/finance/loan-amortization.html` : `第134期` : dead
- `tools/finance/loan-amortization.html` : `第135期` : dead
- `tools/finance/loan-amortization.html` : `第136期` : dead
- `tools/finance/loan-amortization.html` : `第137期` : dead
- `tools/finance/loan-amortization.html` : `第138期` : dead
- `tools/finance/loan-amortization.html` : `第139期` : dead
- `tools/finance/loan-amortization.html` : `第140期` : dead
- `tools/finance/loan-amortization.html` : `第141期` : dead
- `tools/finance/loan-amortization.html` : `第142期` : dead
- `tools/finance/loan-amortization.html` : `第143期` : dead
- `tools/finance/loan-amortization.html` : `第144期` : dead
- `tools/finance/loan-amortization.html` : `第145期` : dead
- `tools/finance/loan-amortization.html` : `第146期` : dead
- `tools/finance/loan-amortization.html` : `第147期` : dead
- `tools/finance/loan-amortization.html` : `第148期` : dead
- `tools/finance/loan-amortization.html` : `第149期` : dead
- `tools/finance/loan-amortization.html` : `第150期` : dead
- `tools/finance/loan-amortization.html` : `第151期` : dead
- `tools/finance/loan-amortization.html` : `第152期` : dead
- `tools/finance/loan-amortization.html` : `第153期` : dead
- `tools/finance/loan-amortization.html` : `第154期` : dead
- `tools/finance/loan-amortization.html` : `第155期` : dead
- `tools/finance/loan-amortization.html` : `第156期` : dead
- `tools/finance/loan-amortization.html` : `第157期` : dead
- `tools/finance/loan-amortization.html` : `第158期` : dead
- `tools/finance/loan-amortization.html` : `第159期` : dead
- `tools/finance/loan-amortization.html` : `第160期` : dead
- `tools/finance/loan-amortization.html` : `第161期` : dead
- `tools/finance/loan-amortization.html` : `第162期` : dead
- `tools/finance/loan-amortization.html` : `第163期` : dead
- `tools/finance/loan-amortization.html` : `第164期` : dead
- `tools/finance/loan-amortization.html` : `第165期` : dead
- `tools/finance/loan-amortization.html` : `第166期` : dead
- `tools/finance/loan-amortization.html` : `第167期` : dead
- `tools/finance/loan-amortization.html` : `第168期` : dead
- `tools/finance/loan-amortization.html` : `第169期` : dead
- `tools/finance/loan-amortization.html` : `第170期` : dead
- `tools/finance/loan-amortization.html` : `第171期` : dead
- `tools/finance/loan-amortization.html` : `第172期` : dead
- `tools/finance/loan-amortization.html` : `第173期` : dead
- `tools/finance/loan-amortization.html` : `第174期` : dead
- `tools/finance/loan-amortization.html` : `第175期` : dead
- `tools/finance/loan-amortization.html` : `第176期` : dead
- `tools/finance/loan-amortization.html` : `第177期` : dead
- `tools/finance/loan-amortization.html` : `第178期` : dead
- `tools/finance/loan-amortization.html` : `第179期` : dead
- `tools/finance/loan-amortization.html` : `第180期` : dead
- `tools/finance/loan-amortization.html` : `第181期` : dead
- `tools/finance/loan-amortization.html` : `第182期` : dead
- `tools/finance/loan-amortization.html` : `第183期` : dead
- `tools/finance/loan-amortization.html` : `第184期` : dead
- `tools/finance/loan-amortization.html` : `第185期` : dead
- `tools/finance/loan-amortization.html` : `第186期` : dead
- `tools/finance/loan-amortization.html` : `第187期` : dead
- `tools/finance/loan-amortization.html` : `第188期` : dead
- `tools/finance/loan-amortization.html` : `第189期` : dead
- `tools/finance/loan-amortization.html` : `第190期` : dead
- `tools/finance/loan-amortization.html` : `第191期` : dead
- `tools/finance/loan-amortization.html` : `第192期` : dead
- `tools/finance/loan-amortization.html` : `第193期` : dead
- `tools/finance/loan-amortization.html` : `第194期` : dead
- `tools/finance/loan-amortization.html` : `第195期` : dead
- `tools/finance/loan-amortization.html` : `第196期` : dead
- `tools/finance/loan-amortization.html` : `第197期` : dead
- `tools/finance/loan-amortization.html` : `第198期` : dead
- `tools/finance/loan-amortization.html` : `第199期` : dead
- `tools/finance/loan-amortization.html` : `第200期` : dead
- `tools/finance/loan-amortization.html` : `第201期` : dead
- `tools/finance/loan-amortization.html` : `第202期` : dead
- `tools/finance/loan-amortization.html` : `第203期` : dead
- `tools/finance/loan-amortization.html` : `第204期` : dead
- `tools/finance/loan-amortization.html` : `第205期` : dead
- `tools/finance/loan-amortization.html` : `第206期` : dead
- `tools/finance/loan-amortization.html` : `第207期` : dead
- `tools/finance/loan-amortization.html` : `第208期` : dead
- `tools/finance/loan-amortization.html` : `第209期` : dead
- `tools/finance/loan-amortization.html` : `第210期` : dead
- `tools/finance/loan-amortization.html` : `第211期` : dead
- `tools/finance/loan-amortization.html` : `第212期` : dead
- `tools/finance/loan-amortization.html` : `第213期` : dead
- `tools/finance/loan-amortization.html` : `第214期` : dead
- `tools/finance/loan-amortization.html` : `第215期` : dead
- `tools/finance/loan-amortization.html` : `第216期` : dead
- `tools/finance/loan-amortization.html` : `第217期` : dead
- `tools/finance/loan-amortization.html` : `第218期` : dead
- `tools/finance/loan-amortization.html` : `第219期` : dead
- `tools/finance/loan-amortization.html` : `第220期` : dead
- `tools/finance/loan-amortization.html` : `第221期` : dead
- `tools/finance/loan-amortization.html` : `第222期` : dead
- `tools/finance/loan-amortization.html` : `第223期` : dead
- `tools/finance/loan-amortization.html` : `第224期` : dead
- `tools/finance/loan-amortization.html` : `第225期` : dead
- `tools/finance/loan-amortization.html` : `第226期` : dead
- `tools/finance/loan-amortization.html` : `第227期` : dead
- `tools/finance/loan-amortization.html` : `第228期` : dead
- `tools/finance/loan-amortization.html` : `第229期` : dead
- `tools/finance/loan-amortization.html` : `第230期` : dead
- `tools/finance/loan-amortization.html` : `第231期` : dead
- `tools/finance/loan-amortization.html` : `第232期` : dead
- `tools/finance/loan-amortization.html` : `第233期` : dead
- `tools/finance/loan-amortization.html` : `第234期` : dead
- `tools/finance/loan-amortization.html` : `第235期` : dead
- `tools/finance/loan-amortization.html` : `第236期` : dead
- `tools/finance/loan-amortization.html` : `第237期` : dead
- `tools/finance/loan-amortization.html` : `第238期` : dead
- `tools/finance/loan-amortization.html` : `第239期` : dead
- `tools/finance/loan-amortization.html` : `第240期` : dead
- `tools/finance/loan-amortization.html` : `第241期` : dead
- `tools/finance/loan-amortization.html` : `第242期` : dead
- `tools/finance/loan-amortization.html` : `第243期` : dead
- `tools/finance/loan-amortization.html` : `第244期` : dead
- `tools/finance/loan-amortization.html` : `第245期` : dead
- `tools/finance/loan-amortization.html` : `第246期` : dead
- `tools/finance/loan-amortization.html` : `第247期` : dead
- `tools/finance/loan-amortization.html` : `第248期` : dead
- `tools/finance/loan-amortization.html` : `第249期` : dead
- `tools/finance/loan-amortization.html` : `第250期` : dead
- `tools/finance/loan-amortization.html` : `第251期` : dead
- `tools/finance/loan-amortization.html` : `第252期` : dead
- `tools/finance/loan-amortization.html` : `第253期` : dead
- `tools/finance/loan-amortization.html` : `第254期` : dead
- `tools/finance/loan-amortization.html` : `第255期` : dead
- `tools/finance/loan-amortization.html` : `第256期` : dead
- `tools/finance/loan-amortization.html` : `第257期` : dead
- `tools/finance/loan-amortization.html` : `第258期` : dead
- `tools/finance/loan-amortization.html` : `第259期` : dead
- `tools/finance/loan-amortization.html` : `第260期` : dead
- `tools/finance/loan-amortization.html` : `第261期` : dead
- `tools/finance/loan-amortization.html` : `第262期` : dead
- `tools/finance/loan-amortization.html` : `第263期` : dead
- `tools/finance/loan-amortization.html` : `第264期` : dead
- `tools/finance/loan-amortization.html` : `第265期` : dead
- `tools/finance/loan-amortization.html` : `第266期` : dead
- `tools/finance/loan-amortization.html` : `第267期` : dead
- `tools/finance/loan-amortization.html` : `第268期` : dead
- `tools/finance/loan-amortization.html` : `第269期` : dead
- `tools/finance/loan-amortization.html` : `第270期` : dead
- `tools/finance/loan-amortization.html` : `第271期` : dead
- `tools/finance/loan-amortization.html` : `第272期` : dead
- `tools/finance/loan-amortization.html` : `第273期` : dead
- `tools/finance/loan-amortization.html` : `第274期` : dead
- `tools/finance/loan-amortization.html` : `第275期` : dead
- `tools/finance/loan-amortization.html` : `第276期` : dead
- `tools/finance/loan-amortization.html` : `第277期` : dead
- `tools/finance/loan-amortization.html` : `第278期` : dead
- `tools/finance/loan-amortization.html` : `第279期` : dead
- `tools/finance/loan-amortization.html` : `第280期` : dead
- `tools/finance/loan-amortization.html` : `第281期` : dead
- `tools/finance/loan-amortization.html` : `第282期` : dead
- `tools/finance/loan-amortization.html` : `第283期` : dead
- `tools/finance/loan-amortization.html` : `第284期` : dead
- `tools/finance/loan-amortization.html` : `第285期` : dead
- `tools/finance/loan-amortization.html` : `第286期` : dead
- `tools/finance/loan-amortization.html` : `第287期` : dead
- `tools/finance/loan-amortization.html` : `第288期` : dead
- `tools/finance/loan-amortization.html` : `第289期` : dead
- `tools/finance/loan-amortization.html` : `第290期` : dead
- `tools/finance/loan-amortization.html` : `第291期` : dead
- `tools/finance/loan-amortization.html` : `第292期` : dead
- `tools/finance/loan-amortization.html` : `第293期` : dead
- `tools/finance/loan-amortization.html` : `第294期` : dead
- `tools/finance/loan-amortization.html` : `第295期` : dead
- `tools/finance/loan-amortization.html` : `第296期` : dead
- `tools/finance/loan-amortization.html` : `第297期` : dead
- `tools/finance/loan-amortization.html` : `第298期` : dead
- `tools/finance/loan-amortization.html` : `第299期` : dead
- `tools/finance/loan-amortization.html` : `第300期` : dead
- `tools/finance/loan-amortization.html` : `第301期` : dead
- `tools/finance/loan-amortization.html` : `第302期` : dead
- `tools/finance/loan-amortization.html` : `第303期` : dead
- `tools/finance/loan-amortization.html` : `第304期` : dead
- `tools/finance/loan-amortization.html` : `第305期` : dead
- `tools/finance/loan-amortization.html` : `第306期` : dead
- `tools/finance/loan-amortization.html` : `第307期` : dead
- `tools/finance/loan-amortization.html` : `第308期` : dead
- `tools/finance/loan-amortization.html` : `第309期` : dead
- `tools/finance/loan-amortization.html` : `第310期` : dead
- `tools/finance/loan-amortization.html` : `第311期` : dead
- `tools/finance/loan-amortization.html` : `第312期` : dead
- `tools/finance/loan-amortization.html` : `第313期` : dead
- `tools/finance/loan-amortization.html` : `第314期` : dead
- `tools/finance/loan-amortization.html` : `第315期` : dead
- `tools/finance/loan-amortization.html` : `第316期` : dead
- `tools/finance/loan-amortization.html` : `第317期` : dead
- `tools/finance/loan-amortization.html` : `第318期` : dead
- `tools/finance/loan-amortization.html` : `第319期` : dead
- `tools/finance/loan-amortization.html` : `第320期` : dead
- `tools/finance/loan-amortization.html` : `第321期` : dead
- `tools/finance/loan-amortization.html` : `第322期` : dead
- `tools/finance/loan-amortization.html` : `第323期` : dead
- `tools/finance/loan-amortization.html` : `第324期` : dead
- `tools/finance/loan-amortization.html` : `第325期` : dead
- `tools/finance/loan-amortization.html` : `第326期` : dead
- `tools/finance/loan-amortization.html` : `第327期` : dead
- `tools/finance/loan-amortization.html` : `第328期` : dead
- `tools/finance/loan-amortization.html` : `第329期` : dead
- `tools/finance/loan-amortization.html` : `第330期` : dead
- `tools/finance/loan-amortization.html` : `第331期` : dead
- `tools/finance/loan-amortization.html` : `第332期` : dead
- `tools/finance/loan-amortization.html` : `第333期` : dead
- `tools/finance/loan-amortization.html` : `第334期` : dead
- `tools/finance/loan-amortization.html` : `第335期` : dead
- `tools/finance/loan-amortization.html` : `第336期` : dead
- `tools/finance/loan-amortization.html` : `第337期` : dead
- `tools/finance/loan-amortization.html` : `第338期` : dead
- `tools/finance/loan-amortization.html` : `第339期` : dead
- `tools/finance/loan-amortization.html` : `第340期` : dead
- `tools/finance/loan-amortization.html` : `第341期` : dead
- `tools/finance/loan-amortization.html` : `第342期` : dead
- `tools/finance/loan-amortization.html` : `第343期` : dead
- `tools/finance/loan-amortization.html` : `第344期` : dead
- `tools/finance/loan-amortization.html` : `第345期` : dead
- `tools/finance/loan-amortization.html` : `第346期` : dead
- `tools/finance/loan-amortization.html` : `第347期` : dead
- `tools/finance/loan-amortization.html` : `第348期` : dead
- `tools/finance/loan-amortization.html` : `第349期` : dead
- `tools/finance/loan-amortization.html` : `第350期` : dead
- `tools/finance/loan-amortization.html` : `第351期` : dead
- `tools/finance/loan-amortization.html` : `第352期` : dead
- `tools/finance/loan-amortization.html` : `第353期` : dead
- `tools/finance/loan-amortization.html` : `第354期` : dead
- `tools/finance/loan-amortization.html` : `第355期` : dead
- `tools/finance/loan-amortization.html` : `第356期` : dead
- `tools/finance/loan-amortization.html` : `第357期` : dead
- `tools/finance/loan-amortization.html` : `第358期` : dead
- `tools/finance/loan-amortization.html` : `第359期` : dead
- `tools/finance/loan-amortization.html` : `第360期` : dead
- `tools/finance/loan-amortization.html` : `第56期` : dead
- `tools/finance/loan-amortization.html` : `第57期` : dead
- `tools/finance/loan-amortization.html` : `第58期` : dead
- `tools/finance/loan-amortization.html` : `第59期` : dead
- `tools/finance/loan-amortization.html` : `第60期` : dead
- `tools/finance/loan-amortization.html` : `第61期` : dead
- `tools/finance/loan-amortization.html` : `第62期` : dead
- `tools/finance/loan-amortization.html` : `第63期` : dead
- `tools/finance/loan-amortization.html` : `第64期` : dead
- `tools/finance/loan-amortization.html` : `第65期` : dead
- `tools/finance/loan-amortization.html` : `第66期` : dead
- `tools/finance/loan-amortization.html` : `第67期` : dead
- `tools/finance/loan-amortization.html` : `第68期` : dead
- `tools/finance/loan-amortization.html` : `第69期` : dead
- `tools/finance/loan-amortization.html` : `第70期` : dead
- `tools/finance/loan-amortization.html` : `第71期` : dead
- `tools/finance/loan-amortization.html` : `第72期` : dead
- `tools/finance/loan-amortization.html` : `第73期` : dead
- `tools/finance/loan-amortization.html` : `第74期` : dead
- `tools/finance/loan-amortization.html` : `第75期` : dead
- `tools/finance/loan-amortization.html` : `第76期` : dead
- `tools/finance/loan-amortization.html` : `第77期` : dead
- `tools/finance/loan-amortization.html` : `第78期` : dead
- `tools/finance/loan-amortization.html` : `第79期` : dead
- `tools/finance/loan-amortization.html` : `第80期` : dead
- `tools/finance/loan-amortization.html` : `第81期` : dead
- `tools/finance/loan-amortization.html` : `第82期` : dead
- `tools/finance/loan-amortization.html` : `第83期` : dead
- `tools/finance/loan-amortization.html` : `第84期` : dead
- `tools/finance/loan-amortization.html` : `第85期` : dead
- `tools/finance/loan-amortization.html` : `第86期` : dead
- `tools/finance/loan-amortization.html` : `第87期` : dead
- `tools/finance/loan-amortization.html` : `第88期` : dead
- `tools/finance/loan-amortization.html` : `第89期` : dead
- `tools/finance/loan-amortization.html` : `第90期` : dead
- `tools/finance/loan-amortization.html` : `第91期` : dead
- `tools/finance/loan-amortization.html` : `第92期` : dead
- `tools/finance/loan-amortization.html` : `第93期` : dead
- `tools/finance/loan-amortization.html` : `第94期` : dead
- `tools/finance/loan-amortization.html` : `第95期` : dead
- `tools/finance/loan-amortization.html` : `第96期` : dead
- `tools/finance/loan-amortization.html` : `第97期` : dead
- `tools/finance/loan-amortization.html` : `第98期` : dead
- `tools/finance/loan-amortization.html` : `第99期` : dead
- `tools/finance/loan-comparison.html` : `A 方案` : dead
- `tools/finance/mortgage-calculator.html` : `贷款金额（万元）` : dead
- `tools/finance/mortgage-prepayment.html` : `原方案（不提前还，以输入的每月还款为基准）` : dead
- `tools/finance/msisdn-validator.html` : `格式 ^\+?[1-9]\d{6,14}$（含国家码，总长 7~15 位）` : dead
- `tools/finance/mutual-fund-calculator.html` : `年化收益率（IRR）：` : dead
- `tools/finance/mutual-fund-calculator.html` : `期末总资产：¥165,902.94` : dead
- `tools/finance/npv-calculator.html` : `IRR < 折现率：` : dead
- `tools/finance/npv-calculator.html` : `NPV > 0：项目可行；NPV < 0：项目不可行` : dead
- `tools/finance/npv-calculator.html` : `PI > 1：可行；PI < 1：不可行` : dead
- `tools/finance/number-to-words-chinese.html` : `按中文读数规则：万/亿分组，逐级读“数字 + 单位”，并对零位做特殊处理` : dead
- `tools/finance/option-profit-calculator.html` : `总盈亏：+¥496.00` : dead
- `tools/finance/option-profit-calculator.html` : `看涨期权买方` : dead
- `tools/finance/password-generator-advanced.html` : `一般建议 12 位以上并混合大小写、数字与符号；高价值账户建议 16 位以上或使用口令短语。` : dead
- `tools/finance/password-generator-advanced.html` : `生成便于记忆的口令短语（passphrase）` : dead
- `tools/finance/password-generator-advanced.html` : `高级密码生成器。自定义长度、字符集与排除规则生成高强度密码，支持口令短语模式，纯前端生成不存储，适合账号安全与密钥管理。` : dead
- `tools/finance/payroll-calculator.html` : `住房公积金比例不能为负数。` : dead
- `tools/finance/payroll-calculator.html` : `养老保险比例不能为负数。` : dead
- `tools/finance/payroll-calculator.html` : `医疗保险比例不能为负数。` : dead
- `tools/finance/payroll-calculator.html` : `失业保险比例不能为负数。` : dead
- `tools/finance/payroll-calculator.html` : `年税后总收入：¥135,270.00` : dead
- `tools/finance/payroll-calculator.html` : `第10月` : dead
- `tools/finance/payroll-calculator.html` : `第11月` : dead
- `tools/finance/payroll-calculator.html` : `第12月` : dead
- `tools/finance/payroll-calculator.html` : `第1月` : dead
- `tools/finance/payroll-calculator.html` : `第2月` : dead
- `tools/finance/payroll-calculator.html` : `第3月` : dead
- `tools/finance/payroll-calculator.html` : `第4月` : dead
- `tools/finance/payroll-calculator.html` : `第5月` : dead
- `tools/finance/payroll-calculator.html` : `第6月` : dead
- `tools/finance/payroll-calculator.html` : `第7月` : dead
- `tools/finance/payroll-calculator.html` : `第8月` : dead
- `tools/finance/payroll-calculator.html` : `第9月` : dead
- `tools/finance/points-redemption-value.html` : `每万分价值 = 商品现金价值 / 兑换所需积分 × 10000` : dead
- `tools/finance/profit-margin-calculator.html` : `EBITDA 17.00万` : dead
- `tools/finance/profit-margin-calculator.html` : `⚠ 所得税税率须在 0%–100% 之间（不含 100%）。` : dead
- `tools/finance/profit-margin-calculator.html` : `⚠ 目标净利率过高：扣除所得税与 25% 假设期间费用率后售价无解，请降低目标净利率。` : dead
- `tools/finance/profit-margin-calculator.html` : `⚠ 目标利润率须在 0%–100% 之间（不含 100%）。` : dead
- `tools/finance/profit-margin-calculator.html` : `⚠ 目标营业利润率须小于 75%（扣除 25% 假设期间费用率后仍须为正）。` : dead
- `tools/finance/profit-margin-calculator.html` : `元（EBITDA利润率 17.00%）` : dead
- `tools/finance/profit-margin-calculator.html` : `元（净利率 6.75%）` : dead
- `tools/finance/profit-margin-calculator.html` : `元（营业利润率 11.00%）` : dead
- `tools/finance/profit-margin-calculator.html` : `净利润 6.75万` : dead
- `tools/finance/profit-margin-calculator.html` : `利润总额：9.00万 元` : dead
- `tools/finance/profit-margin-calculator.html` : `所得税（25%）：2.25万 元` : dead
- `tools/finance/profit-margin-calculator.html` : `折旧摊销：6.00万 元（占收入 6.00%）` : dead
- `tools/finance/profit-margin-calculator.html` : `毛利润 40.00万` : dead
- `tools/finance/profit-margin-calculator.html` : `研发费用：5.00万 元（占收入 5.00%）` : dead
- `tools/finance/profit-margin-calculator.html` : `管理费用：10.00万 元（占收入 10.00%）` : dead
- `tools/finance/profit-margin-calculator.html` : `营业利润 11.00万` : dead
- `tools/finance/profit-margin-calculator.html` : `财务费用：2.00万 元（占收入 2.00%）` : dead
- `tools/finance/profit-margin-calculator.html` : `销售费用：8.00万 元（占收入 8.00%）` : dead
- `tools/finance/provident-fund.html` : `个人缴存（12%）：` : dead
- `tools/finance/provident-fund.html` : `元　（受当地最高额度 50 万元封顶）` : dead
- `tools/finance/provident-fund.html` : `元（余额 × 20）` : dead
- `tools/finance/provident-fund.html` : `单位缴存（12%）：` : dead
- `tools/finance/provident-fund.html` : `按 50 万元 30 年、利率 3.1% 测算（等额本息）：` : dead
- `tools/finance/provident-fund.html` : `累计缴存 60 月，账户余额（估算）：` : dead
- `tools/finance/report-1.html` : `元；少数股东损益 = 150,000.00 × 20% =` : dead
- `tools/finance/report-1.html` : `合并价差 = 长期股权投资 800,000.00 − 母公司享有 560,000.00 =` : dead
- `tools/finance/report-1.html` : `合并价差（商誉）` : dead
- `tools/finance/report-1.html` : `子公司净资产 = 实收资本 500,000.00 + 未分配利润 200,000.00 + 评估增值 0.00 =` : dead
- `tools/finance/report-1.html` : `少数股东权益 = 700,000.00 × 20% =` : dead
- `tools/finance/report-1.html` : `少数股东权益（20%）` : dead
- `tools/finance/report-1.html` : `归属于母公司股东的净利润 = 150,000.00 × 80% =` : dead
- `tools/finance/report-1.html` : `母公司享有份额 = 700,000.00 × 80% =` : dead
- `tools/finance/report-1.html` : `母公司享有份额（80%）` : dead
- `tools/finance/report-1.html` : `长期股权投资高于母公司享有的净资产份额，差额 240,000.00 元确认为` : dead
- `tools/finance/sort-code-validator-validator.html` : `格式 ^\d{2}-?\d{2}-?\d{2}$（6 位数字，可含连字符）` : dead
- `tools/finance/text-reverse-words.html` : `将句子按空白切分为单词后整体逆序输出，可选保留标点位置` : dead
- `tools/finance/tfn-validator.html` : `9 位（8 位前补 0）按权重 1、4、3、7、5、8、6、9、10 加权，总和须被 11 整除。` : dead
- `tools/finance/uan-validator.html` : `格式 ^\d{12}$（12 位数字）` : dead
- `tools/finance/word-search.html` : `可以。输入自定义单词后会随机排布进网格，支持设定网格大小与方向。` : dead
- `tools/finance/word-search.html` : `可以。页面提供可打印视图，适合课堂或线下活动使用。` : dead
- `tools/finance/word-search.html` : `在字母矩阵中隐藏并寻找目标单词，支持自定义词表与网格大小，适合词汇记忆与休闲游戏，纯前端生成可打印或在线玩。` : dead
- `tools/finance/word-search.html` : `打印或在线进行词汇记忆练习` : dead
- `tools/finance/word-search.html` : `找词游戏是一款金融财务领域的在线工具。在字母矩阵中隐藏并寻找目标单词，支持自定义词表与网格大小，适合词汇记忆与休闲游戏，纯前端生成可打印或在线玩。` : dead
- `tools/finance/word-search.html` : `自定义词表与网格大小生成题目` : dead
- `tools/finance/word-search.html` : `输入词表（如 apple, book, cat），页面把单词按横竖斜方向随机排入字母矩阵，支持打印。` : dead
- `tools/finance/zip-code-validator.html` : `格式 ^\d{5}(-\d{4})?$；前 3 位可映射至州/地区分区` : dead

  其它成因样例（共 624 条，仅列前 5）：
  - `tools/finance/amount-in-words.html` : `金额超出支持范围（最多 16 位整数）` : dynamic
  - `tools/finance/analysis-44.html` : `80000.00 元` : dynamic
  - `tools/finance/analysis-5.html` : `1.5~2.5 常见 / > 3 高杠杆` : dynamic
  - `tools/finance/analysis-5.html` : `40%~60% 适中 / > 70% 警戒 / < 30% 偏低` : dynamic
  - `tools/finance/analysis-5.html` : `< 1 稳健 / 1~2 一般 / > 2 高杠杆` : dynamic

### fire（dead 4 / dynamic 0 / fragment 0 / harmless 0）

- `tools/fire/analysis-cost-price-8.html` : `毛利 = 售价 - 单位成本；毛利率 = 毛利 / 售价` : dead
- `tools/fire/evacuation-time.html` : `t = N/(b·D·f) + 行走时间` : dead
- `tools/fire/extinguisher-calc.html` : `灭火器最大保护距离/配置基准（GB 50140）` : dead
- `tools/fire/hydrant-pressure.html` : `栓口动压 = 几何高差 + 沿程 + 局部` : dead

### fire-rescue（dead 17 / dynamic 6 / fragment 2 / harmless 1）

- `tools/fire-rescue/calc-4.html` : `GB 50140-2005 §6.1 规定一个计算单元内配置的灭火器数量不得少于 2 具，且每个设置点不宜多于 5 具；这样一具失效、压力不足或被火势封锁时仍有备用，同时避免单点堆放过密。` : dead
- `tools/fire-rescue/calc-4.html` : `为什么每个计算单元最少要配 2 具？` : dead
- `tools/fire-rescue/calc-4.html` : `按默认参数（A 类火灾、轻危险级、保护面积 300 m²）：U=100 m²/A，Q=K·S/U=3A；按 4kg ABC 干粉单具 2A 折算，⌈3/2⌉=2 具（且每计算单元不少于 2 具），按每处 2 具布置约需 1 个设置点。每个设置点不宜多于 5 具，且任一点到最近设置点的步行距离应满足表 5.2.1（A 类…(+21字)` : dead
- `tools/fire-rescue/detector-20.html` : `≥90% 合格，75-89% 基本合格，60-74% 需整改，<60% 不合格` : dead
- `tools/fire-rescue/fire-extinguisher-selection.html` : `GB 50140-2005 §6.1 规定一个计算单元内配置的灭火器数量不得少于 2 具、每个设置点不宜多于 5 具；这样一处失效、压力不足或被火势封锁时仍有备用，同时避免单点堆放过密。` : dead
- `tools/fire-rescue/fire-extinguisher-selection.html` : `按默认参数（A 类火灾、中危险级、保护面积 100 m²）：推荐 ABC 干粉 4 kg（通用性强、适用 A 类固体火灾）为主，水基/泡沫型为辅；配置数量 2 具（Q=⌈100 ÷ 75⌉=2A，按单具 2A 折算 1 具、且每个计算单元不少于 2 具），最低灭火级别 2A（GB 50140-2005 表 6.2.1：…(+47字)` : dead
- `tools/fire-rescue/fire-resistance-rating.html` : `高层仓库（>24m）耐火等级不应低于二级；高架仓库应为一级（GB 50016-2014 第 3.2.5 条）。` : dead
- `tools/fire-rescue/fire-resistance-rating.html` : `高层厂房（>24m）耐火等级不应低于二级（GB 50016-2014 第 3.2.2 条）。` : dead
- `tools/fire-rescue/high-rise-fire.html` : `GB 50084 相关水力计算` : dead
- `tools/fire-rescue/high-rise-fire.html` : `GB/T 26770 登高平台消防车等整车标准` : dead
- `tools/fire-rescue/high-rise-fire.html` : `作业高度 ≈ 云梯额定长度 × 0.8 − 建筑高度修正` : dead
- `tools/fire-rescue/hydrant-flow.html` : `室内消火栓充实水柱要求：高层建筑、厂房、库房及室内净高超过 8m 的民用建筑 ≥13 m，其他建筑 ≥10 m。18.7 m 已满足高层要求；但若要达到单栓 5 L/s 基准，需提高栓口压力或缩短水带长度。` : dead
- `tools/fire-rescue/smoke-management.html` : `47.3 m³/s，排烟量 170368 m³/h（已含 1.2 安全系数）；烟层底部 5.0 m ≥ 清晰高度 3.0 m，烟层控制满足要求。设计建议排烟口 12 个、单口 14197 m³/h；当前若不足应增至 12 个。` : dead
- `tools/fire-rescue/smoke-management.html` : `请输入有效的热释放速率（>0）、烟层底部高度（>0）、清晰高度（>0）；火焰高度限制须 ≥0（0 表示不设限）。` : dead
- `tools/fire-rescue/sprinkler-design.html` : `中危险级 I 级 6 L/min·m²、II 级 8（作用面积 160 m²）` : dead
- `tools/fire-rescue/sprinkler-design.html` : `按默认参数（中危Ⅰ级、标准作用面积 160 m²、标准喷水强度 6 L/(min·m²)）：作用面积内约 13 个喷头（间距约 3.6 m），单喷头流量 80 L/min；系统设计流量 = 1040 L/min = 17.3 L/s，实际喷水强度 6.5 L/(min·m²) ≥ 标准 6，满足设计要求。建议消防水池储…(+32字)` : dead
- `tools/fire-rescue/sprinkler-design.html` : `来自 GB 50084 按火灾危险等级的规定：中危Ⅰ级为 6、中危Ⅱ级为 8、严重危险级更高；设计喷水强度不得低于对应等级下限，否则无法有效控制火情。GB 55036-2022 实施后，与通用规范不一致的强制性条文以其为准。` : dead

  其它成因样例（共 9 条，仅列前 5）：
  - `tools/fire-rescue/calc-4.html` : `GB 50140-2005 表 6.2.1` : dynamic
  - `tools/fire-rescue/fire-resistance-rating.html` : `可燃` : fragment
  - `tools/fire-rescue/fire-resistance-rating.html` : `多层厂房耐火等级不应低于三级（GB 50016-2014 第 3.2.3 条；甲、乙类厂房应为二级）。` : dynamic
  - `tools/fire-rescue/fire-resistance-rating.html` : `仓库耐火等级不应低于二级（本页未区分储存物品类别，按偏严取值；单层乙、丙类及多层丁、戊类仓库可为三级，见 GB 50016-2014 第 3.2.5 条）。` : dynamic
  - `tools/fire-rescue/high-rise-fire.html` : `GB 50084-2019` : harmless

### fishery（dead 58 / dynamic 15 / fragment 10 / harmless 0）

- `tools/fishery/aerator-duration.html` : `增氧机时长 = 溶氧缺口/(功率×效率)` : dead
- `tools/fishery/aerator-duration.html` : `水体体积=面积×666.67×水深(m³)；增氧机增氧速率(mg/L·h)=功率×SAE×1000÷体积；净增氧=增氧速率-耗氧率；所需时长=(目标溶氧-当前溶氧)÷净增氧。叶轮式增氧机 SAE 一般 1.2-2.0。曝气无法超过饱和溶氧，本页按暖水（约 30℃）饱和 7.6 mg/L 取 7.5 mg/L 为保守上限…(+1字)` : dead
- `tools/fishery/aerator-duration.html` : `请检查输入：面积、水深、目标溶氧、功率、增氧效率须 >0；当前溶氧、耗氧率须 ≥0。` : dead
- `tools/fishery/assessor-risk-4.html` : `溶氧<3mg/L时鱼类浮头，<1mg/L可致泛塘死亡` : dead
- `tools/fishery/assessor-risk-4.html` : `鱼病风险 = f(水温, 密度, 水质)` : dead
- `tools/fishery/breeding-cycle.html` : `以草鱼为例（默认参数）：总周期约 138 天（从放苗到上市，放苗期已计入，不再额外加 14 天），日增长率约 2.50%；其中放苗期 14 天、培育期约 31 天（规格至约 152 g）、养成期约 68 天（至约 813 g）、收获期约 25 天（至上市规格约 1500 g）；若放苗日 2026-09-08，则预计上市…(+36字)` : dead
- `tools/fishery/breeding-cycle.html` : `养殖周期 = 培育+养成+收获` : dead
- `tools/fishery/calc-power.html` : `水体积 V (m³)` : dead
- `tools/fishery/cycle-6.html` : `清淤周期 = f(淤积速率)` : dead
- `tools/fishery/density-1.html` : `密度 = 尾数 / 面积` : dead
- `tools/fishery/dissolved-oxygen.html` : `溶氧预测 = f(温度, 气压)` : dead
- `tools/fishery/drug-withdrawal-fish.html` : `不可以。内置值只是常见说明书的示例，不同药品与地区可能采用更高的度日口径（如恩诺沙星 500 度日）；页面结果仅供估算，上市前必须以药品说明书、当地法规和残留检测为准。` : dead
- `tools/fishery/drug-withdrawal-fish.html` : `休药期 = 基准×(温度校正)` : dead
- `tools/fishery/drug-withdrawal-fish.html` : `内置的标准休药期可以直接用吗？` : dead
- `tools/fishery/drug-withdrawal-fish.html` : `实际水温必须高于温度下限，否则工具直接拒绝计算并提示参数不合理；现实中低于下限时代谢极慢，不可套用公式，应大幅延长休药期并送样检测残留。` : dead
- `tools/fishery/drug-withdrawal-fish.html` : `请检查输入：标准休药期须 >0；温度下限须 ≥0 且低于参考水温；实际水温须高于温度下限且不超过 40℃。` : dead
- `tools/fishery/drug-withdrawal-fish.html` : `默认参数（标准休药期 14 天 @ 参考温度 15℃、温度下限 5℃、实际水温 22℃）：度日需求 K = 14×(15−5) = 140 ℃·天；有效温度 = 22−5 = 17℃；校正休药期 = 140 / 17 ≈ 8.2 天，按安全口径向上取整为 9 天，约为标准的 0.59 倍，水温较高可缩短；但若当地执行更…(+75字)` : dead
- `tools/fishery/feed-calculator.html` : `请检查输入：鱼体总重量须 >0，水温 0–40℃，养殖天数须 >0，饲料单价须 ≥0。` : dead
- `tools/fishery/feed-calculator.html` : `饲料量 = 体重×投喂率` : dead
- `tools/fishery/feed-protein-fat.html` : `蛋白脂肪配比 = 营养需求` : dead
- `tools/fishery/feed-rate-calculator.html` : `投喂率 = 体重×率%` : dead
- `tools/fishery/feed-rate-calculator.html` : `请检查输入：存塘量、均重须 >0，水温须在 0–40℃，且不能留空或为负。` : dead
- `tools/fishery/feeding-rate.html` : `投喂率 = 体重×日率` : dead
- `tools/fishery/feeding-rate.html` : `请检查输入：水温须在 0–40℃ 之间，总重量须 >0。` : dead
- `tools/fishery/fish-disease-risk.html` : `鱼病风险 = 综合评分` : dead
- `tools/fishery/fish-growth-curve.html` : `生长曲线 = 特定生长率拟合` : dead
- `tools/fishery/fish-weight.html` : `鱼体重 = a·体长^b` : dead
- `tools/fishery/fry-transport-survival.html` : `纯氧系数 0.5、空气 1.0、无增氧 2.0，系数越小越安全（风险率越低）；提高增氧能显著延长安全运输时长。` : dead
- `tools/fishery/fry-transport-survival.html` : `请检查输入：密度与时长须 >0，目标成活率须在 50–99%（不含 100%），水温须在模型适用区间 5–30℃。` : dead
- `tools/fishery/fry-transport-survival.html` : `运输成活率 = f(密度, 温度, 时间)` : dead
- `tools/fishery/fry-transport-survival.html` : `风险率=0.02×(密度/100)×(时长/6)×exp((水温-15)/12)×增氧系数；成活率=100×exp(-风险率)。纯氧系数0.5，空气1.0，无增氧2.0。建议密度按目标成活率反推。` : dead
- `tools/fishery/harvest-size-price.html` : `规格价格 = 均重×单价` : dead
- `tools/fishery/mesh-size-guide.html` : `网目尺寸 = 最小可捕规格` : dead
- `tools/fishery/oxygen-machine.html` : `增氧机配置 = 需氧量/单机功率` : dead
- `tools/fishery/oxygen-machine.html` : `请检查输入：水体体积须 >0；鱼载量须 ≥0；水温须在 0–40℃ 之间。` : dead
- `tools/fishery/parasite-lifecycle.html` : `寄生虫周期 = 温度依赖模拟` : dead
- `tools/fishery/plankton-biomass.html` : `浮游生物量 = 计数×体积` : dead
- `tools/fishery/pond-capacity.html` : `承鱼量 = f(面积, 溶氧, 换水)` : dead
- `tools/fishery/pond-desilting.html` : `当前淤泥 8 cm、允许上限 20 cm、沉积速率 3 cm/年、保留 5 cm 肥泥层：剩余 12 cm，约 4.0 年后需清淤；届时需清除 15 cm，清淤量约 500 m³，费用约 7500 元。若当前已 22 cm 超限，则立即清淤，需清除 17 cm，清淤量约 567 m³、费用约 8500 元。` : dead
- `tools/fishery/pond-desilting.html` : `清淤周期 = 淤积/清除速率` : dead
- `tools/fishery/pond-desilting.html` : `请检查输入：面积与沉积速率须 >0；允许厚度、当前厚度、单价、保留肥泥层厚度须 ≥0；保留厚度须小于允许厚度。` : dead
- `tools/fishery/profit-calculator.html` : `利润 = 收入 − 成本` : dead
- `tools/fishery/ratio-hormone.html` : `最简比 = a/g : b/g（g 为最大公约数）` : dead
- `tools/fishery/salinity-calculator.html` : `四项均需填写有效数值：现有水量须 >0，三个盐度须 ≥0。未测盐度请勿留空（淡水请明确输入 0）` : dead
- `tools/fishery/salinity-calculator.html` : `盐度 = 盐质量/水体积` : dead
- `tools/fishery/seafood-cold-storage.html` : `冷藏温度 = 保质期对应` : dead
- `tools/fishery/spawning-hormone.html` : `催产剂量 = 体重×系数` : dead
- `tools/fishery/stocking-density.html` : `两者任一成为瓶颈都会限制产量，取小值保证不突破任一约束，是保守安全的设计。注意：功率为 0（如粗养水库）时功率约束不启用，只按水体承载估算，页面会把来源标为「水体承载（未配增氧）」。` : dead
- `tools/fishery/stocking-density.html` : `放养密度 = 优化承载` : dead
- `tools/fishery/stocking-density.html` : `默认参数：功率载鱼量 = (4/5)×450 = 360 kg/亩；水体载鱼量 = 3×(5×1.2×666.67)/5 = 2400 kg/亩；取较小值 360 kg/亩；放养密度 = 360/(15/100)/0.75 ≈ 32000 尾/亩，总放苗量 ≈ 160000 尾，预计产量 1800 kg；增氧 0.8 …(+10字)` : dead
- `tools/fishery/wastewater-cod.html` : `COD 估算 = 投饵×排放系数` : dead
- `tools/fishery/water-exchange-rate.html` : `换水率 = 流量/池体积` : dead
- `tools/fishery/water-exchange-rate.html` : `请检查输入：池体积需 >0，日换水量/产生率/进水浓度需 ≥0，目标浓度需 >0。` : dead
- `tools/fishery/water-oxygen.html` : `先按水温定位温度区间、按盐度定位盐度区间，做双线性插值得到该条件下的理论饱和溶氧；饱和度 = 实测 ÷ 饱和 × 100%。分级：<2 危险(浮头)，<4 偏低(开增氧机)，≤8 正常，>8 过饱和(防气泡病)。` : dead
- `tools/fishery/water-quality-threshold.html` : `氨氮/亚盐安全阈值 = 查表` : dead
- `tools/fishery/water-quality-threshold.html` : `水温 26℃、pH 8 时 NH₄⁺ pKa≈9.219，非离子氨占比约 5.70%；实测 TAN 0.8 mg/L → 有毒 NH₃ 0.0456 mg/L（超过 0.02 mg/L 安全限，约 228%，判超标）；Cl⁻ 20 mg/L 时亚硝酸盐安全限 = min(0.1, 20×0.0132)=0.1 mg/L…(+40字)` : dead
- `tools/fishery/winter-heating.html` : `加热功率 = V·ρ·c·ΔT/t` : dead
- `tools/fishery/winter-heating.html` : `请检查输入：面积需 >0，风速与余量需 ≥0（余量 ≤100%）。` : dead

  其它成因样例（共 25 条，仅列前 5）：
  - `tools/fishery/aerator-duration.html` : `目标溶氧 ` : fragment
  - `tools/fishery/aerator-duration.html` : ` 超过曝气可达的饱和上限（本页按暖水 7.5 mg/L 保守估算）。曝气只能接近饱和值，无法超过；需换水、降温或使用化学增氧。若要按具体水温核算饱和值，请先查该水温下的溶解氧饱和表。` : dynamic
  - `tools/fishery/calc-power.html` : `平均加热功率 P = Q÷t` : dynamic
  - `tools/fishery/calc-power.html` : `所需热量 Q` : fragment
  - `tools/fishery/calc-power.html` : `建议配置功率（1.2×）` : dynamic

### fitness（dead 15 / dynamic 2 / fragment 1 / harmless 2）

- `tools/fitness/analysis-retention.html` : `Mass（评估/优化/提升）机制` : dead
- `tools/fitness/assessor-64.html` : `师资力量 = 认证系数×0.6 + min(从业年限/10, 1)×4（上限 10）；课程内容 = 三项评分均值；教学环境 = 室温×0.3 + 湿度×0.2 + 班级人数×0.25 + 人均面积×0.25（达标记 10、不达标记 5–6）；学员效果 = (满意度×0.3 + 留存×0.3 + 续费×0.2 + 进度×…(+73字)` : dead
- `tools/fitness/assessor-64.html` : `数据分析（会员/课程/留存）` : dead
- `tools/fitness/calc-3.html` : `男 体脂% = 86.010×log₁₀(腰围−颈围) − 70.041×log₁₀(身高) + 36.76；女 体脂% = 163.205×log₁₀(腰围+臀围−颈围) − 97.684×log₁₀(身高) − 78.387` : dead
- `tools/fitness/calc-3.html` : `男性：身高 175 cm、颈围 38 cm、腰围 85 cm。 ⏎ waist−neck=47；log10(47)=1.6721，log10(175)=2.2430。 ⏎ bf=86.010×1.6721−70.041×2.2430+36.76=143.81−157.08+36.76=23.49%。 ⏎ 按男性分级：<…(+152字)` : dead
- `tools/fitness/estimate-2.html` : `基于代谢当量（MET）法：MET = 1 约等于静息代谢（3.5 ml O₂/kg/min）。MET 越高强度越大（<3 低强度、<6 中等、<9 高强度，≥9 极高强度）。米饭当量按每碗约 230 kcal 折算，便于直观理解消耗量。` : dead
- `tools/fitness/index.html` : `健身运动工具集合收录了 34 个免费在线工具，覆盖健身运动场景下的常见计算、换算与查询需求。无论你是相关领域的从业者、学生还是普通用户，都能在这里找到即用即走的实用小工具。所有工具纯前端运行，数据不上传服务器，保护隐私安全。` : dead
- `tools/fitness/pace-calculator.html` : `Distance +时间→配速` : dead
- `tools/fitness/pace-calculator.html` : `Distance +配速→时间` : dead
- `tools/fitness/pace-calculator.html` : `Input: 距离 5 km、完赛时间 30:00。 ⏎ 平均配速 = 30:00 ÷ 5 = 6:00 /km。 ⏎ 延展：若维持 6:00/km，10 km 需 60:00、半马 21.1 km 需约 2:06:36、全马 42.2 km 需约 4:13:12。 ⏎ 结论：想 5 km 跑进 25 分，需把配速提到…(+26字)` : dead
- `tools/fitness/pace-calculator.html` : `Velocity(km/h) = 3600 ÷ 每公里秒数（英制按 1 英里 = 1.60934 km 换算）` : dead
- `tools/fitness/rater-time.html` : `推荐时长 = 60 s（压痛 0–2）/ 90 s（3–5）/ 120 s（6–7）/ 60 s（≥8）；判定：实际 < 0.6×推荐 偏短，0.6–1.5×推荐 适中，> 1.5×推荐 偏长` : dead
- `tools/fitness/step-stride.html` : `如何使用步幅与速度换算？` : dead
- `tools/fitness/step-stride.html` : `步幅与速度换算是做什么的？` : dead
- `tools/fitness/step-stride.html` : `步幅与速度换算适合哪些场景？` : dead

  其它成因样例（共 5 条，仅列前 5）：
  - `tools/fitness/calc-3.html` : `腰围必须大于颈围，当前围度差 ≤ 0，无法计算体脂率，请核对测量部位。` : dynamic
  - `tools/fitness/calc-3.html` : `腰围 + 臀围必须大于颈围，当前围度差 ≤ 0，无法计算体脂率，请核对测量部位。` : dynamic
  - `tools/fitness/calc-heart-rate.html` : `目标心率 = (最大心率 − 静息心率) × 强度% + 静息心率` : fragment
  - `tools/fitness/step-stride.html` : `📖 查看「步幅与速度换算使用指南」` : harmless
  - `tools/fitness/step-stride.html` : `📚 深度解析：步幅与速度换算` : harmless

### fluid（dead 11 / dynamic 0 / fragment 1 / harmless 0）

- `tools/fluid/buoyancy-force.html` : `F_b = ρ_f g V。 浮力等于排开液重。` : dead
- `tools/fluid/capillary-pressure.html` : `ΔP = 4γ/D（完全润湿圆管）。 水,D=1mm → 288 Pa。` : dead
- `tools/fluid/capillary-rise.html` : `h = 2γcosθ/(ρgr)。 水在细玻管中明显上升。` : dead
- `tools/fluid/cavitation-number.html` : `σ 越小越易空化（σ<1 危险）。` : dead
- `tools/fluid/froude-number.html` : `Fr>1 为急流，Fr<1 为缓流。` : dead
- `tools/fluid/hydrostatic-pressure.html` : `P = ρgh。 10 m 水柱 ≈ 98 kPa。` : dead
- `tools/fluid/kinematic-viscosity.html` : `ν = μ/ρ。 水 20°C → 1.0×10⁻⁶ m²/s。` : dead
- `tools/fluid/manning-velocity.html` : `v = (1/n)R^(2/3)S^(1/2)。 混凝土渠 n≈0.013。` : dead
- `tools/fluid/orifice-discharge.html` : `Q = C_d A√(2ΔP/ρ)。 重力出流时 ΔP=ρgh。` : dead
- `tools/fluid/poiseuille-flow.html` : `Q = πΔP r⁴/(8μL)。 流量对半径极敏感（四次方）。` : dead
- `tools/fluid/stokes-settling.html` : `v = 2r²(ρ_p−ρ_f)g/(9μ)。 适用低雷诺数小球。` : dead

  其它成因样例（共 1 条，仅列前 5）：
  - `tools/fluid/cavitation-number.html` : `v=10 → 约 1.98。` : fragment

### food（dead 2 / dynamic 0 / fragment 0 / harmless 0）

- `tools/food/analysis-menu.html` : `单品毛利率 = (售价 − 成本) ÷ 售价 × 100%` : dead
- `tools/food/analysis-menu.html` : `综合毛利率 = Σ(售价×销量 − 成本×销量) ÷ Σ(售价×销量) × 100%` : dead

### food-processing（dead 2 / dynamic 1 / fragment 5 / harmless 0）

- `tools/food-processing/freeze-thaw-loss.html` : `解冻失水率(%) = (冷冻前重 − 解冻后重) ÷ 冷冻前重 × 100%` : dead
- `tools/food-processing/sterilization-f-value.html` : `杀菌F值（D值/Z值）计算器。美食烹饪工具，帮助精确掌握食材配比与营养。` : dead

  其它成因样例（共 6 条，仅列前 5）：
  - `tools/food-processing/dough-absorption.html` : `面团最终水分含量 = 面团总水分 ÷ 面团总重 × 100%` : fragment
  - `tools/food-processing/emulsion-stability.html` : `ESI = 乳液层高度 ÷ 总高度 × 100%` : fragment
  - `tools/food-processing/fermentation-brix.html` : `酒精生成 = 糖消耗 × 0.511 × 发酵效率` : fragment
  - `tools/food-processing/oil-absorption-rate.html` : `吸油率 = 吸油量 ÷ 油炸前重量 × 100%` : fragment
  - `tools/food-processing/sterilization-f-value.html` : `当前参考温度不是 121.1℃，该 F 值只是此温度下的等效时间，不能与 F₀≥3 基准直接比较` : dynamic

### food-testing（dead 6 / dynamic 0 / fragment 0 / harmless 0）

- `tools/food-testing/detector-3.html` : `抑制率 ≥50% 为阳性（不合格），需用色谱法确证；35%-50% 为可疑需复测；<35% 为阴性（合格）` : dead
- `tools/food-testing/detector-3.html` : `提示：ΔA 为反应前后吸光度变化值，通常由分光光度计/农残速测仪自动读取。若 ΔA0 < 0.3，说明酶活性不足需重新配制。` : dead
- `tools/food-testing/heavy-metal-migration.html` : `= (浓度 × 模拟液体积) / 食品模拟液体积 × 1000` : dead
- `tools/food-testing/heavy-metal-migration.html` : `以材料浓度 conc(mg/kg) 估算：迁移量(mg/dm²) = conc×模拟液体积 / 接触面积；迁移量(mg/kg) = conc×模拟液体积 / 食品量 ×1000。` : dead
- `tools/food-testing/heavy-metal-migration.html` : `材料中铅 0.05 mg/kg、模拟液 100 mL、面积 2 dm²、食品量 1000 mL、SML 0.01 mg/kg：迁移 0.05×100/2=2.5 mg/dm²，0.05×100/1000×1000=5.0 mg/kg，远超 SML 0.01 → 不合格。` : dead
- `tools/food-testing/heavy-metal-migration.html` : `核心计算公式（按输入变量）：(conc×volume)÷foodVol×1000；area÷foodVol×1000` : dead

### forensic-medicine（dead 1 / dynamic 0 / fragment 0 / harmless 0）

- `tools/forensic-medicine/dna-str-typing.html` : `PI > 1 支持亲权关系，PI < 1 不支持亲权关系。` : dead

### forestry（dead 8 / dynamic 9 / fragment 3 / harmless 0）

- `tools/forestry/carbon-sequestration.html` : `⚠ 输入无效：地上生物量与根茎比须为正数，请修正后重新计算。` : dead
- `tools/forestry/carbon-sequestration.html` : `⚠ 输入无效：年均生长量须为正数，请修正后重新计算。` : dead
- `tools/forestry/carbon-sequestration.html` : `⚠ 输入无效：蓄积量与林龄须为正数，请修正后重新计算。` : dead
- `tools/forestry/carbon-sequestration.html` : `⚠ 输入无效：面积与碳价须为正数，请修正后重新计算。` : dead
- `tools/forestry/carbon-sequestration.html` : `杉木（ρ=0.307,BEF=1.53,CF=0.52）蓄积 V=120 m³/ha、面积 10 ha、林龄 20 年、碳价 60 元/t：B=56.4、C=29.3 t/ha、CO₂=107.5 t/ha；总 CO₂≈1075 t、年均≈53.7 t、价值≈6.45 万元。` : dead
- `tools/forestry/carbon-sequestration.html` : `森林碳汇计算<br>生物量(t/ha) = 材积 × 木材密度 × BEF（生物量扩展因子）；或 现存量 × (1 + 根茎比0.25)<br>面积估算法：年生物量增量 = 年均生长量 MAI × 木材密度 × BEF（按 1 年计）<br>碳储量 = 生物量 × 含碳率；CO₂ 当量 = 碳储量 × 3.667（44…(+88字)` : dead
- `tools/forestry/carbon-sequestration.html` : `蓄积量扩展法：生物量 B=V×ρ×BEF（ρ 木材密度、BEF 生物量扩展因子），碳储量 C=B×CF（含碳率约 0.5），CO₂=C×3.667；总 CO₂=CO₂/ha×面积，年均=总 CO₂/林龄，价值=总 CO₂×碳价。` : dead
- `tools/forestry/pest-1.html` : `等级标准：轻微 <5%，轻度 5~10%，中度 10~20%，重度 20~40%，严重 >40%` : dead

  其它成因样例（共 12 条，仅列前 5）：
  - `tools/forestry/calc-57.html` : `郁闭度 = 被树冠覆盖点数 ÷ 样点总数` : fragment
  - `tools/forestry/carbon-sequestration.html` : `单位面积年固CO₂(t/ha·年)` : dynamic
  - `tools/forestry/carbon-sequestration.html` : `年固CO₂总量(t/年)` : dynamic
  - `tools/forestry/carbon-sequestration.html` : `总固碳量 = 单公顷CO₂ × 面积；年固碳量 = 总固碳量 / 林龄` : fragment
  - `tools/forestry/carbon-sequestration.html` : `年均生长量(m³/ha·年)` : dynamic

### fun（dead 171 / dynamic 20 / fragment 18 / harmless 73）

- `tools/fun/1a2b-guess.html` : `1A2B 猜数字是做什么的？` : dead
- `tools/fun/1a2b-guess.html` : `1A2B 猜数字适合哪些场景？` : dead
- `tools/fun/1a2b-guess.html` : `关于「1A2B 猜数字」` : dead
- `tools/fun/1a2b-guess.html` : `如何使用1A2B 猜数字？` : dead
- `tools/fun/2048-game.html` : `2048 游戏是做什么的？` : dead
- `tools/fun/2048-game.html` : `2048 游戏适合哪些场景？` : dead
- `tools/fun/2048-game.html` : `如何使用2048 游戏？` : dead
- `tools/fun/anagram-game.html` : `720 种排列里绝大多数是乱序非词，只有通过词表校验的才列出，故有效词通常十几个到几十个。` : dead
- `tools/fun/anagram-game.html` : `如何使用字谜游戏？` : dead
- `tools/fun/anagram-game.html` : `字母组 LISTEN 可重排出 SILENT、TINSEL、ENLIST、INLETS、LISTEN 等；若取 5 字母子集可得 LINES、TILES、SLIME、EMITS、ISLET 等。6 个不同字母的全排列为 6!=720 种，其中有效英文单词占比很小，工具仅输出词典命中的那些。` : dead
- `tools/fun/anagram-game.html` : `字母重排组合数 = 字母数 n 的阶乘 ÷（各重复字母出现次数阶乘之积）；从字母集合中枚举长度不低于 3 的子集并做全排列，与词典比对去重得到所有可拼单词；按长度降序或字典序输出，得分常按单词长度或稀有度计算。` : dead
- `tools/fun/anagram-game.html` : `字谜游戏是做什么的？` : dead
- `tools/fun/anagram-game.html` : `字谜游戏适合哪些场景？` : dead
- `tools/fun/anagram-game.html` : `输入或随机给一组字母（如 6 个），工具按字典穷举所有「字母不重复使用」且长度 ≥3 的子序列组合，逐一查词表命中即列出；结果可按键长降序或字母序排列。` : dead
- `tools/fun/bingo-generator.html` : `关于「活动随机号码生成器」` : dead
- `tools/fun/bingo-generator.html` : `如何使用活动随机号码生成器？` : dead
- `tools/fun/bingo-generator.html` : `活动随机号码生成器是做什么的？` : dead
- `tools/fun/bingo-generator.html` : `活动随机号码生成器适合哪些场景？` : dead
- `tools/fun/blink-counter.html` : `如何使用眨眼次数统计？` : dead
- `tools/fun/blink-counter.html` : `眨眼次数统计是做什么的？` : dead
- `tools/fun/blink-counter.html` : `眨眼次数统计适合哪些场景？` : dead
- `tools/fun/blood-type-personality.html` : `如何使用血型性格分析？` : dead
- `tools/fun/blood-type-personality.html` : `血型性格分析是做什么的？` : dead
- `tools/fun/blood-type-personality.html` : `血型性格分析适合哪些场景？` : dead
- `tools/fun/breakout.html` : `如何使用打砖块？` : dead
- `tools/fun/breakout.html` : `打砖块是做什么的？` : dead
- `tools/fun/breakout.html` : `打砖块适合哪些场景？` : dead
- `tools/fun/chess-fen-viewer.html` : `国际象棋 FEN 查看器是做什么的？` : dead
- `tools/fun/chess-fen-viewer.html` : `国际象棋 FEN 查看器适合哪些场景？` : dead
- `tools/fun/chess-fen-viewer.html` : `如何使用国际象棋 FEN 查看器？` : dead
- `tools/fun/click-speed.html` : `如何使用点击速度测试？` : dead
- `tools/fun/click-speed.html` : `点击速度测试是做什么的？` : dead
- `tools/fun/click-speed.html` : `点击速度测试适合哪些场景？` : dead
- `tools/fun/coin-toss-streak.html` : `如何使用抛硬币连胜统计？` : dead
- `tools/fun/coin-toss-streak.html` : `抛硬币连胜统计是做什么的？` : dead
- `tools/fun/coin-toss-streak.html` : `抛硬币连胜统计适合哪些场景？` : dead
- `tools/fun/color-memory.html` : `如何使用颜色记忆？` : dead
- `tools/fun/color-memory.html` : `颜色记忆是做什么的？` : dead
- `tools/fun/color-memory.html` : `颜色记忆适合哪些场景？` : dead
- `tools/fun/cps-test.html` : `CPS 测试是做什么的？` : dead
- `tools/fun/cps-test.html` : `CPS 测试适合哪些场景？` : dead
- `tools/fun/cps-test.html` : `如何使用CPS 测试？` : dead
- `tools/fun/daily-riddle.html` : `关于「每日谜题挑战」` : dead
- `tools/fun/daily-riddle.html` : `如何使用每日谜题挑战？` : dead
- `tools/fun/daily-riddle.html` : `每日谜题挑战是做什么的？` : dead
- `tools/fun/daily-riddle.html` : `每日谜题挑战适合哪些场景？` : dead
- `tools/fun/emoji-memory.html` : `Emoji 记忆游戏是做什么的？` : dead
- `tools/fun/emoji-memory.html` : `Emoji 记忆游戏适合哪些场景？` : dead
- `tools/fun/emoji-memory.html` : `如何使用Emoji 记忆游戏？` : dead
- `tools/fun/fingerprint-types.html` : `如何使用指纹纹路分类演示？` : dead
- `tools/fun/fingerprint-types.html` : `指纹纹路分类演示是做什么的？` : dead
- `tools/fun/fingerprint-types.html` : `指纹纹路分类演示适合哪些场景？` : dead
- `tools/fun/fingerprint-types.html` : `相同指纹概率` : dead
- `tools/fun/generator-2.html` : `如何使用数独生成器 / 求解器？` : dead
- `tools/fun/generator-2.html` : `数独生成器 / 求解器是做什么的？` : dead
- `tools/fun/generator-2.html` : `数独生成器 / 求解器适合哪些场景？` : dead
- `tools/fun/generator-3.html` : `如何使用迷宫生成器（自动生成并求解）？` : dead
- `tools/fun/generator-3.html` : `迷宫生成器（自动生成并求解）是做什么的？` : dead
- `tools/fun/generator-3.html` : `迷宫生成器（自动生成并求解）适合哪些场景？` : dead
- `tools/fun/generator-laugh.html` : `如何使用笑声音效生成器（合成）？` : dead
- `tools/fun/generator-laugh.html` : `笑声音效生成器（合成）是做什么的？` : dead
- `tools/fun/generator-laugh.html` : `笑声音效生成器（合成）适合哪些场景？` : dead
- `tools/fun/gomoku.html` : `五子棋是做什么的？` : dead
- `tools/fun/gomoku.html` : `五子棋适合哪些场景？` : dead
- `tools/fun/gomoku.html` : `关于「五子棋」` : dead
- `tools/fun/gomoku.html` : `如何使用五子棋？` : dead
- `tools/fun/gomoku-ai.html` : `五子棋人机对战是做什么的？` : dead
- `tools/fun/gomoku-ai.html` : `五子棋人机对战适合哪些场景？` : dead
- `tools/fun/gomoku-ai.html` : `关于「五子棋人机对战」` : dead
- `tools/fun/gomoku-ai.html` : `如何使用五子棋人机对战？` : dead
- `tools/fun/hangman.html` : `如何使用猜单词游戏？` : dead
- `tools/fun/hangman.html` : `猜单词游戏是做什么的？` : dead
- `tools/fun/hangman.html` : `猜单词游戏适合哪些场景？` : dead
- `tools/fun/meditation-timer.html` : `关于「冥想计时器」` : dead
- `tools/fun/meditation-timer.html` : `冥想计时器是做什么的？` : dead
- `tools/fun/meditation-timer.html` : `冥想计时器适合哪些场景？` : dead
- `tools/fun/meditation-timer.html` : `如何使用冥想计时器？` : dead
- `tools/fun/memory-game.html` : `如何使用记忆翻牌游戏？` : dead
- `tools/fun/memory-game.html` : `记忆翻牌游戏是做什么的？` : dead
- `tools/fun/memory-game.html` : `记忆翻牌游戏适合哪些场景？` : dead
- `tools/fun/minesweeper.html` : `如何使用扫雷游戏？` : dead
- `tools/fun/minesweeper.html` : `扫雷游戏是做什么的？` : dead
- `tools/fun/minesweeper.html` : `扫雷游戏适合哪些场景？` : dead
- `tools/fun/number-guess.html` : `/ 猜数字（1-100）` : dead
- `tools/fun/number-guess.html` : `关于「猜数字（1-100）」` : dead
- `tools/fun/number-guess.html` : `如何使用猜数字（1-100）？` : dead
- `tools/fun/number-guess.html` : `猜数字（1-100）是做什么的？` : dead
- `tools/fun/number-guess.html` : `猜数字（1-100）适合哪些场景？` : dead
- `tools/fun/othello.html` : `如何使用黑白棋？` : dead
- `tools/fun/othello.html` : `黑白棋是做什么的？` : dead
- `tools/fun/othello.html` : `黑白棋适合哪些场景？` : dead
- `tools/fun/pong.html` : `乒乓对战是做什么的？` : dead
- `tools/fun/pong.html` : `乒乓对战适合哪些场景？` : dead
- `tools/fun/pong.html` : `如何使用乒乓对战？` : dead
- `tools/fun/raffle-picker.html` : `50 人名单抽 3 名：单次第一名概率 = 1/50 = 2.0%；任意 1 人被抽中的概率 = 3/50 = 6.0%（因为每人有 3 次被选中的机会）。若把某人名字重复写 3 行，总行数变为 52，其概率会高于 3/52，因此不能简单按行数倍算。` : dead
- `tools/fun/raffle-picker.html` : `raffle 偏名单 + 滚动动画的正式抽取；random-picker 是轻量选项级抽取。` : dead
- `tools/fun/raffle-picker.html` : `不放回抽取：抽中的名字即从名单移除，同一人不会被重复抽中。` : dead
- `tools/fun/raffle-picker.html` : `前端伪随机，单次抽取公开可验；名单内每行等概率，同名重复按多行计，不做隐藏加权。` : dead
- `tools/fun/raffle-picker.html` : `如何使用活动随机抽取器？` : dead
- `tools/fun/raffle-picker.html` : `概率口径：单次第一名是 1/N；抽 n 人（不放回）时，任意 1 人被抽中的概率是 n/N，不是 1/N。` : dead
- `tools/fun/raffle-picker.html` : `每行一个名字导入名单，设置抽中数量；名单内每行等概率，抽中即移出（不放回），因此不会重复中签。前端随机、可公开滚动动画增强可信度。` : dead
- `tools/fun/raffle-picker.html` : `活动随机抽取器是做什么的？` : dead
- `tools/fun/raffle-picker.html` : `活动随机抽取器适合哪些场景？` : dead
- `tools/fun/random-name-gen.html` : `关于「随机姓名生成器」` : dead
- `tools/fun/random-name-gen.html` : `如何使用随机姓名生成器？` : dead
- `tools/fun/random-name-gen.html` : `随机姓名生成器是做什么的？` : dead
- `tools/fun/random-name-gen.html` : `随机姓名生成器适合哪些场景？` : dead
- `tools/fun/random-picker.html` : `如何使用随机选择器？` : dead
- `tools/fun/random-picker.html` : `本工具是轻量「选项级」抽取；raffle 支持名单文件与滚动动画，适合正式活动。` : dead
- `tools/fun/random-picker.html` : `选项 [火锅, 炒菜, 日料, 外卖] 抽 1 → 如「日料」；抽 3 不放回 → 3 个不同项（剩 1 项）。每个选项等概率 1/N。` : dead
- `tools/fun/random-picker.html` : `随机选择器是做什么的？` : dead
- `tools/fun/random-picker.html` : `随机选择器适合哪些场景？` : dead
- `tools/fun/reaction-tester.html` : `反应测试是做什么的？` : dead
- `tools/fun/reaction-tester.html` : `反应测试适合哪些场景？` : dead
- `tools/fun/reaction-tester.html` : `如何使用反应测试？` : dead
- `tools/fun/riddle-generator.html` : `关于「谜语生成器」` : dead
- `tools/fun/riddle-generator.html` : `如何使用谜语生成器？` : dead
- `tools/fun/riddle-generator.html` : `谜语生成器是做什么的？` : dead
- `tools/fun/riddle-generator.html` : `谜语生成器适合哪些场景？` : dead
- `tools/fun/rock-paper-scissors.html` : `如何使用石头剪刀布？` : dead
- `tools/fun/rock-paper-scissors.html` : `石头剪刀布是做什么的？` : dead
- `tools/fun/rock-paper-scissors.html` : `石头剪刀布适合哪些场景？` : dead
- `tools/fun/sequence-memory.html` : `如何使用序列记忆？` : dead
- `tools/fun/sequence-memory.html` : `序列记忆是做什么的？` : dead
- `tools/fun/sequence-memory.html` : `序列记忆适合哪些场景？` : dead
- `tools/fun/sequence-puzzle.html` : `不止。还有质数、斐波那契、阶乘、图形旋转/对称等，题库会覆盖多种。` : dead
- `tools/fun/sequence-puzzle.html` : `如何使用序列谜题？` : dead
- `tools/fun/sequence-puzzle.html` : `序列谜题是做什么的？` : dead
- `tools/fun/sequence-puzzle.html` : `序列谜题适合哪些场景？` : dead
- `tools/fun/sequence-puzzle.html` : `观察相邻项关系：等差（差恒定）、等比（比恒定）、斐波那契（每项=前两项和）、平方/立方、质数、阶乘与交替序列；答题后会给出对应的规律解析。本工具只出数字题，不含图形序列。` : dead
- `tools/fun/sequence-puzzle.html` : `观察相邻项关系：等差（差恒定）、等比（比恒定）、斐波那契（每项=前两项和）、平方/质数等；图形题看旋转/数量变化。附解析。` : dead
- `tools/fun/sequence-puzzle.html` : `规律覆盖：等差、等比、斐波那契、质数、图形旋转等。` : dead
- `tools/fun/sequence-puzzle.html` : `逻辑训练：给数字/图形序列，推断下一项。` : dead
- `tools/fun/shape-memory.html` : `如何使用形状记忆？` : dead
- `tools/fun/shape-memory.html` : `形状记忆是做什么的？` : dead
- `tools/fun/shape-memory.html` : `形状记忆适合哪些场景？` : dead
- `tools/fun/sliding-puzzle.html` : `关于「滑动拼图」` : dead
- `tools/fun/sliding-puzzle.html` : `如何使用滑动拼图？` : dead
- `tools/fun/sliding-puzzle.html` : `滑动拼图是做什么的？` : dead
- `tools/fun/sliding-puzzle.html` : `滑动拼图适合哪些场景？` : dead
- `tools/fun/snake-game.html` : `如何使用贪吃蛇？` : dead
- `tools/fun/snake-game.html` : `贪吃蛇是做什么的？` : dead
- `tools/fun/snake-game.html` : `贪吃蛇适合哪些场景？` : dead
- `tools/fun/solitaire.html` : `如何使用纸牌接龙？` : dead
- `tools/fun/solitaire.html` : `纸牌接龙是做什么的？` : dead
- `tools/fun/solitaire.html` : `纸牌接龙适合哪些场景？` : dead
- `tools/fun/space-shooter.html` : `太空射击是做什么的？` : dead
- `tools/fun/space-shooter.html` : `太空射击适合哪些场景？` : dead
- `tools/fun/space-shooter.html` : `如何使用太空射击？` : dead
- `tools/fun/stats-3.html` : `如何使用手掌大小与身高相关性（统计）？` : dead
- `tools/fun/stats-3.html` : `手掌大小与身高相关性（统计）是做什么的？` : dead
- `tools/fun/stats-3.html` : `手掌大小与身高相关性（统计）适合哪些场景？` : dead
- `tools/fun/tetris.html` : `俄罗斯方块是做什么的？` : dead
- `tools/fun/tetris.html` : `俄罗斯方块适合哪些场景？` : dead
- `tools/fun/tetris.html` : `关于「俄罗斯方块」` : dead
- `tools/fun/tetris.html` : `如何使用俄罗斯方块？` : dead
- `tools/fun/tic-tac-toe.html` : `井字棋是做什么的？` : dead
- `tools/fun/tic-tac-toe.html` : `井字棋适合哪些场景？` : dead
- `tools/fun/tic-tac-toe.html` : `如何使用井字棋？` : dead
- `tools/fun/tongue-twister.html` : `如何使用绕口令？` : dead
- `tools/fun/tongue-twister.html` : `绕口令是做什么的？` : dead
- `tools/fun/tongue-twister.html` : `绕口令适合哪些场景？` : dead
- `tools/fun/typing-rhythm.html` : `如何使用打字节奏感测试？` : dead
- `tools/fun/typing-rhythm.html` : `打字节奏感测试是做什么的？` : dead
- `tools/fun/typing-rhythm.html` : `打字节奏感测试适合哪些场景？` : dead
- `tools/fun/whack-a-mole.html` : `如何使用打地鼠？` : dead
- `tools/fun/whack-a-mole.html` : `打地鼠是做什么的？` : dead
- `tools/fun/whack-a-mole.html` : `打地鼠适合哪些场景？` : dead
- `tools/fun/zodiac-match.html` : `如何使用星座配对指数？` : dead
- `tools/fun/zodiac-match.html` : `星座配对指数是做什么的？` : dead
- `tools/fun/zodiac-match.html` : `星座配对指数适合哪些场景？` : dead

  其它成因样例（共 111 条，仅列前 5）：
  - `tools/fun/1a2b-guess.html` : `📖 查看「1A2B 猜数字使用指南」` : harmless
  - `tools/fun/1a2b-guess.html` : `📚 深度解析：1A2B 猜数字` : fragment
  - `tools/fun/2048-game.html` : `📖 查看「2048 游戏使用指南」` : harmless
  - `tools/fun/2048-game.html` : `📚 深度解析：2048 游戏` : harmless
  - `tools/fun/anagram-game.html` : `📖 查看「字谜游戏使用指南」` : harmless

### gardening（dead 8 / dynamic 0 / fragment 0 / harmless 3）

- `tools/gardening/balcony-sunlight.html` : `不能。基准表是经验值，楼层只按低/中/高做 ±1 小时修正，未考虑楼间距、窗外树木、雨棚与城市纬度差异；结果用于选花方向判断，精确光照请用照度计实测。` : dead
- `tools/gardening/balcony-sunlight.html` : `全日照≥6h、半日照 4-6h、散射光 2-4h、耐阴<2h` : dead
- `tools/gardening/balcony-sunlight.html` : `北半球朝北的阳台冬季几乎全天处于建筑阴影，只有散射光，模型按 0 小时直射计；若楼栋间距大或有侧向反射，可再上调 0.5-1 小时。` : dead
- `tools/gardening/balcony-sunlight.html` : `北向冬季为什么是 0 小时？` : dead
- `tools/gardening/balcony-sunlight.html` : `南向 6 楼、夏季：估算每日直射约 8h → 适合月季、茉莉、番茄等喜阳植物；同条件冬季约 4h，需改养长寿花、多肉等短日照花卉；北向则只能养蕨类、玉簪等耐阴植物。西向低层夏季：基准 6h − 低层遮挡 1h = 5h，归入半日照。` : dead
- `tools/gardening/balcony-sunlight.html` : `按朝向（南/东/西/北）、楼层（低层易受遮挡、高层更通透）与季节查经验基准表，再加楼层修正：南向中层夏季约 8h、冬季约 4h；北向以散射光为主，直射不足 2h。` : dead
- `tools/gardening/balcony-sunlight.html` : `结果能精确到小时吗？` : dead
- `tools/gardening/index.html` : `园艺种植工具集合收录了 12 个免费在线工具，覆盖园艺种植场景下的常见计算、换算与查询需求。无论你是相关领域的从业者、学生还是普通用户，都能在这里找到即用即走的实用小工具。所有工具纯前端运行，数据不上传服务器，保护隐私安全。` : dead

  其它成因样例（共 3 条，仅列前 5）：
  - `tools/gardening/pruning-calendar.html` : `🌷 园艺修剪时间提示` : harmless
  - `tools/gardening/reminder-cycle-succulent.html` : `🌷 多肉浇水周期提醒（按品种）` : harmless
  - `tools/gardening/watering-schedule.html` : `✨ 浇水计划生成` : harmless

### gas（dead 1 / dynamic 1 / fragment 0 / harmless 0）

- `tools/gas/pressure-7.html` : `💡 达西公式 ΔP=λ·(L/D)·(ρv²/2)；λ 用 Haaland 公式；低压管道总压降宜<5%。` : dead

  其它成因样例（共 1 条，仅列前 5）：
  - `tools/gas/current-2.html` : `过保护（<-1.2V）可能导致涂层阴极剥离` : dynamic

### gastroenterology（dead 29 / dynamic 24 / fragment 7 / harmless 0）

- `tools/gastroenterology/bilirubin-ratio.html` : `直接胆红素比值 = DBIL ÷ TBIL × 100%；间接胆红素 = TBIL − DBIL。校验：TBIL、DBIL 均必填（缺项不出结论），DBIL 大于 TBIL 时显式报错并停止计算（不做静默封顶）。判据：TBIL、DBIL 均在参考上限内判正常；TBIL 正常而 DBIL 超上限判孤立性直接胆红素升高；比…(+81字)` : dead
- `tools/gastroenterology/bilirubin-ratio.html` : `算法：间接胆红素 IBIL = TBIL − DBIL；直接胆红素比值 = DBIL/TBIL×100%（DBIL>TBIL 时按 TBIL 封顶）。判定：TBIL≤参考值(默认21μmol/L)为正常；比值<20% 提示间接胆红素升高为主（溶血/Gilbert）；20%~35% 混合性（倾向溶血）；35%~60% 肝…(+88字)` : dead
- `tools/gastroenterology/cdai.html` : `例：女性、稀便 14 次、腹痛 10 分、全身状况 7 分、并发症 1 项、无止泻药、无包块、Hct 35%、体重 −5% → (37−35)=2 → CDAI = 28+50+49+20+0+0+12−5 = 154，轻度活动。若男性、稀便 20 次、腹痛 30 分、全身 10 分、并发症 2 项、用止泻药、包块 5…(+84字)` : dead
- `tools/gastroenterology/cdai.html` : `克罗恩病活动指数 CDAI = 临床变量（腹泻次数、腹痛、全身状况、并发症、止泻药、腹部包块、红细胞压积、体重）加权求和；小于150 缓解、150–220 轻度、220–450 中度、大于450 重度。` : dead
- `tools/gastroenterology/cdai.html` : `女（标准37%）` : dead
- `tools/gastroenterology/cdai.html` : `男:42-Hct, 女:37-Hct` : dead
- `tools/gastroenterology/cdai.html` : `男（标准42%）` : dead
- `tools/gastroenterology/cdai.html` : `算法：CDAI = 稀便次数×2 + 腹痛(0~10)×5 + 全身状况(0~10)×7 + 并发症×20 + 止泻药(>0记1)×30 + 腹部包块(0/2/5)×10 + (标准Hct−实测Hct)×6 + 体重偏差%×1；男标准 Hct 42、女 37。分级：<150 缓解、150~219 轻度、220~450 …(+11字)` : dead
- `tools/gastroenterology/cdai.html` : `红细胞压积 Hct (男%, 女%)` : dead
- `tools/gastroenterology/child-pugh.html` : `算法：总胆红素 >51→3、34~51→2、<34 μmol/L→1 分；白蛋白 <28→3、28~35→2、>35 g/L→1 分；凝血项取 PT 延长与 INR 二者较高分（PT>6s→3、≥4s→2、<4s→1；INR>2.3→3、≥1.7→2、<1.7→1）；腹水（无/少/中重）1~3 分；肝性脑病（无/I-I…(+44字)` : dead
- `tools/gastroenterology/ercp-success.html` : `⚠️ 需临床复核：本页为教学用简化估算。Cotton 等（ASGE 工作组，Gastrointest Endosc 2011）原表为 1–4 级；本页合并为 3 档，分值权重与成功率区间由本页设定，不是指南原文数值，不能替代内镜医师的术前评估。` : dead
- `tools/gastroenterology/ercp-success.html` : `「基于操作难度相关因素，评估ERCP取石和支架置入的成功概率」按输入参数进行专业计算并输出结果。` : dead
- `tools/gastroenterology/ercp-success.html` : `例：胆总管中段结石 12mm、2~3 枚、无手术史 → +2+1+1 = 难度 4，2 级（预估成功 80~90%），常规 EST+网篮取石。若肝内胆管结石 20mm、≥4 枚、Roux-en-Y 术后、有憩室 → +3+2+3+3+1 = 难度 12，3 级（60~80%），建议高容量中心或 EUS-BD/SpyGl…(+40字)` : dead
- `tools/gastroenterology/ercp-success.html` : `基于操作难度相关因素，评估ERCP取石和支架置入的成功概率` : dead
- `tools/gastroenterology/ercp-success.html` : `成功率受术者经验、设备条件和患者解剖因素综合影响。` : dead
- `tools/gastroenterology/ercp-success.html` : `提示：ERCP 是胆胰疾病的重要诊治手段，但属高难度操作。Cotton 等（2009）与 ASGE 不良事件综述常引用总体并发症约 5–10%（术后胰腺炎、出血、穿孔、胆管炎），随病例复杂度升高。高难度病例建议转诊至经验中心或考虑 EUS-BD 等替代方案。本页为教学估算，需临床复核。` : dead
- `tools/gastroenterology/ercp-success.html` : `提示：ERCP是胆胰疾病的重要诊治手段，但属高难度操作，并发症发生率约5-10%（胰腺炎、出血、穿孔、感染）。高难度病例建议转诊至经验中心或考虑EUS-BD等替代方案。仅供临床参考。` : dead
- `tools/gastroenterology/ercp-success.html` : `胆总管直径 (mm)` : dead
- `tools/gastroenterology/glasgow-pancreatitis.html` : `Glasgow 急性胰腺炎评分 = 9 项指标各达标计 1 分之和：年龄 &gt; 55 岁；WBC &gt; 15×10⁹/L；血糖 &gt; 10 mmol/L；LDH &gt; 600 U/L；AST &gt; 200 U/L；血钙 &lt; 2.0 mmol/L；白蛋白 &lt; 32 g/L；尿素 &gt; …(+126字)` : dead
- `tools/gastroenterology/hepatic-encephalopathy.html` : `算法：意识状态、行为变化、认知/智力、扑翼样震颤各取 0~IV 级（0 正常、I 轻度、II 嗜睡/行为异常、III 昏睡、IV 昏迷），取四项最高级别作为 HE 分级。0 级为轻微型(MHE)，I 级启动乳果糖，II 级住院，III 级 ICU 监护，IV 级气管插管保护气道。` : dead
- `tools/gastroenterology/hepatic-encephalopathy.html` : `肝性脑病分级 0 至 IV：取意识、行为、认知、扑翼样震颤各项中最高级别；依次为 0 级（MHE）、Ⅰ 级、Ⅱ 级、Ⅲ 级、Ⅳ 级（昏迷）。` : dead
- `tools/gastroenterology/hepatic-encephalopathy.html` : `轻微型肝性脑病实验室/影像正常，但心理与神经生理测试异常，影响生活质量与驾驶安全。建议乳果糖口服（目标 2~3 次软便/日）并定期评估，多数可门诊管理。` : dead
- `tools/gastroenterology/hp-dob.html` : `DOB = (服药后²³CO₂/²³CO₂比值 - 服药前) × 1000` : dead
- `tools/gastroenterology/hp-dob.html` : `¹³C-UBT：DOB = (服药后²³CO₂/²³CO₂比值 - 服药前) × 1000，单位‰。不同厂家试剂的阳性阈值可能略有差异（2.0-6.0‰）。` : dead
- `tools/gastroenterology/hp-resistance.html` : `例：青霉素过敏、铋剂可用、克拉霉素敏感 → 铋剂四联（PPI+铋剂+四环素 500mg qid+甲硝唑 0.4g tid）14 天。若初次治疗、克拉霉素耐药、甲硝唑敏感、无铋剂 → 避开克拉霉素，选伴同疗法（PPI+阿莫西林+甲硝唑+...）或大剂量二联（艾司奥美拉唑 40mg qid+阿莫西林 1g tid）14 天…(+1字)` : dead
- `tools/gastroenterology/hp-resistance.html` : `未检测药物按可能敏感处理，失败风险较高，条件允许时建议补做药敏。` : dead
- `tools/gastroenterology/hp-resistance.html` : `算法：青霉素过敏且有铋剂 → 铋剂四联（PPI+铋剂+四环素+甲硝唑，或克拉霉素+甲硝唑替代）；初次治疗克拉霉素耐药 → 避开克拉霉素的铋剂四联/大剂量二联；甲硝唑耐药可由铋剂四联克服；既往失败 1 次且左氧氟沙星敏感 → 含左氧四联；失败 ≥2 次 → 含四环素/呋喃唑酮方案或药敏指导。疗程均 14 天。` : dead
- `tools/gastroenterology/mayo-score.html` : `算法：排便次数(正常/+/1~2/+/3~4/+/≥5 计 0~3)、便血(无/少许/明显/以血为主 0~3)、内镜(正常/轻度/中度/重度 0~3)、医师评估(正常/轻/中/重 0~3) 四项求和得 Mayo 总分 0~12；部分 Mayo = 排便+便血+医师评估。≤2 缓解、3~5 轻度、6~10 中度、>10 …(+3字)` : dead
- `tools/gastroenterology/saag-ascites.html` : `算法：SAAG = 血清白蛋白 − 腹水白蛋白（g/L）。≥11 g/L 提示门脉高压性腹水（肝硬化约 80%、布-加、右心衰、门脉血栓、暴发性肝衰）；<11 g/L 提示非门脉高压性（腹膜转移癌、结核性腹膜炎、肾病综合征、胰源、胆源）。门脉高压且腹水总蛋白 <25 多肝硬化、≥25 需排查心源/布加。采样要求血清与腹…(+14字)` : dead

  其它成因样例（共 31 条，仅列前 5）：
  - `tools/gastroenterology/bilirubin-ratio.html` : `直接胆红素比值 = DBIL / TBIL × 100%` : fragment
  - `tools/gastroenterology/child-pugh.html` : `Child-Pugh 分级 = 胆红素 + 白蛋白 + 凝血酶原时间/INR + 腹水 + 肝性脑病（各 1 至 3 分）之和；5–6 分 A 级、7–9 B 级、10–15 C 级。` : fragment
  - `tools/gastroenterology/colonoscopy-polyp.html` : `请输入有效的息肉直径（1–200 mm）；留空不判读，也不按 0 计为微小息肉。` : dynamic
  - `tools/gastroenterology/colonoscopy-polyp.html` : `留空不判读` : dynamic
  - `tools/gastroenterology/colonoscopy-polyp.html` : `可疑癌变（需病理确认）` : dynamic

### general（dead 20 / dynamic 87 / fragment 20 / harmless 0）

- `tools/general/calc-13.html` : `Δ天 = 日期₂ − 日期₁` : dead
- `tools/general/calc-14.html` : `年龄 = 今天 − 出生日期` : dead
- `tools/general/color-temp-2.html` : `Φ = E × A ÷ 0.6 ÷ 0.8；N = Φ ÷ Φ₁（向上取整）` : dead
- `tools/general/convert-22.html` : `换算值 = 数值 × 10^k` : dead
- `tools/general/detector-118.html` : `体系认证(ISO 9001)` : dead
- `tools/general/estimate-36.html` : `193nm 光源、NA=1.35 时，理论分辨率约` : dead
- `tools/general/frequency-15.html` : `超声加工参数（频率 f、振幅 A、工具直径 D、静压力 F）按材料匹配` : dead
- `tools/general/gravity.html` : `重心 x = Σ(Wᵢ·xᵢ) / ΣWᵢ；力矩 Mᵢ = Wᵢ·xᵢ` : dead
- `tools/general/lifespan-10.html` : `金属回收率>90%，塑料约60%，复合材料<30%` : dead
- `tools/general/lifespan-5.html` : `湿度>70%时微生物活跃，<40%时生物降解基本停止` : dead
- `tools/general/lifespan-corrosion.html` : `剩余寿命 = (初始壁厚 − 已用量 − 腐蚀裕量) / 腐蚀速率` : dead
- `tools/general/lifespan-wear-2.html` : `剩余寿命 ≈ (允许磨损量 ÷ 磨损率 ÷ 日运行时间) − 已运行时间` : dead
- `tools/general/nianjieqiangdujisuan.html` : `τ = F / A；许用载荷 F = τ·A / n` : dead
- `tools/general/pressure-5.html` : `可切厚度 ∝ (水压)^0.5 × 磨料流量` : dead
- `tools/general/ratio-fuel-oil.html` : `混合密度 = Σ(比例 × 密度)；混合热值 = Σ(比例 × 热值)` : dead
- `tools/general/tester-40.html` : `| 预计工期：1~3天` : dead
- `tools/general/tester-40.html` : `维修后测试清单（5项）：` : dead
- `tools/general/tester-40.html` : `设备：电气设备 | 故障：电气故障` : dead
- `tools/general/turnover-2.html` : `可维持天数 = 当前库存 ÷ 日均消耗；周转次数 = 周期需求量 ÷ 日均消耗` : dead
- `tools/general/wear-4.html` : `磨损率 ∝ P×v×μ/HV（Archard 近似）` : dead

  其它成因样例（共 107 条，仅列前 5）：
  - `tools/general/air-1.html` : `AQI 空气质量指数` : dynamic
  - `tools/general/calc-14.html` : `25 岁 0 个月 0 天` : dynamic
  - `tools/general/calc-203.html` : `孔极限 (mm)` : dynamic
  - `tools/general/calc-203.html` : `轴极限 (mm)` : dynamic
  - `tools/general/calc-power-spacing.html` : `污水（检查井/跌水）布置` : fragment

### geology（dead 24 / dynamic 8 / fragment 0 / harmless 0）

- `tools/geology/calc-1.html` : `RQD = Σ(长度 ≥ 阈值 的完整岩芯段) / 钻孔总长度 × 100%` : dead
- `tools/geology/calc-87.html` : `Ac > 1 判为正异常、< 1 为负异常；强度 ≥ 2 为强异常，≥ 1.5 中异常，≥ 1 弱异常，否则落于背景范围。` : dead
- `tools/geology/dip-strike.html` : `走向/倾角 = 测量换算` : dead
- `tools/geology/diqiuhuaxueyichangjieshi.html` : `地球化学异常解释 = 背景+衬值` : dead
- `tools/geology/diqiuwuliyingyong.html` : `地球物理应用 = 反演解释` : dead
- `tools/geology/dizhibianlujilubiao.html` : `编录参数 = 分层计算` : dead
- `tools/geology/dizhiwurandiaochapinggu.html` : `Cn 为实测浓度、Bn 为背景值、Sn 为评价标准值；Igeo < 0 无污染，0–1 无至中度，1–2 中度，2–3 中至强，≥ 3 强污染（Müller 地累积指数分级）。` : dead
- `tools/geology/estimate-grade-reserve.html` : `品位储量 = 品位 × 体积 × 体重` : dead
- `tools/geology/estimate-reserve-1.html` : `断面法 V = Σ(A_i×L_i)` : dead
- `tools/geology/hazard.html` : `地质灾害风险 = f(坡度, 岩性, 降雨)` : dead
- `tools/geology/huanjingdizhipingjia.html` : `环境地质评价 = 综合分级` : dead
- `tools/geology/index.html` : `地质勘探工具集合收录了 37 个免费在线工具，覆盖地质勘探场景下的常见计算、换算与查询需求。无论你是相关领域的从业者、学生还是普通用户，都能在这里找到即用即走的实用小工具。所有工具纯前端运行，数据不上传服务器，保护隐私安全。` : dead
- `tools/geology/index.html` : `基于太沙基公式计算条形基础地基极限承载力与特征值(安全系数取2)，用于建筑基础设计与地基承载力验算。` : dead
- `tools/geology/richter-scale.html` : `M_L = log10(A) + 距离修正` : dead
- `tools/geology/sanweidizhijianmocanshu.html` : `三维建模参数 = 网格/插值` : dead
- `tools/geology/sanweidizhijianmocanshu.html` : `例：钻孔视厚 h=5m、θ=25°、L=300m、S=200m、D=2.7 t/m³ → t=5×cos25°=4.532m、A=60000 m²、V=60000×4.532=271892 m³（27.19 万m³）、Ah=54378 m²、铅垂厚=2.113m、Q=271892×2.7=734109 t。` : dead
- `tools/geology/sanweidizhijianmocanshu.html` : `公式：真厚度 t = 视厚度 h × cos(倾角θ)；真面积 A = 走向长 L × 倾向延 S；体积 V = A × t；水平投影面积 Ah = L×S×cosθ；铅垂厚度 = h×sinθ；矿石量 Q = V × 体重 D。倾角 θ 取 0–89°（本地计算，单位 m、t/m³）。` : dead
- `tools/geology/shuiwendizhishentoushiyan.html` : `渗透系数 k = Q/(A·i)` : dead
- `tools/geology/soil-sample.html` : `采样设计 = 网度布置` : dead
- `tools/geology/tester-16.html` : `吸水率反映岩石孔隙率，一般 Wa<1% 为致密岩石` : dead
- `tools/geology/tester-16.html` : `岩石力学参数 = 强度/变形计算` : dead
- `tools/geology/tester-16.html` : `软化系数 K = σcw / σcd，K<0.75 为软化岩石` : dead
- `tools/geology/tester-16.html` : `软化系数 K<0.75 为软化岩石（遇水强度显著降低），工程中需特别注意` : dead
- `tools/geology/wutanyichangjieyi.html` : `推测埋深 ≈ 异常半宽 W / 1.31（Peters 半宽法）` : dead

  其它成因样例（共 8 条，仅列前 5）：
  - `tools/geology/analysis-33.html` : `⚠ 数据无效：` : dynamic
  - `tools/geology/analysis-33.html` : ` 行无法解析，已接受 ` : dynamic
  - `tools/geology/analysis-33.html` : ` 行、拒绝 ` : dynamic
  - `tools/geology/analysis-33.html` : ` 行。请修正后重新计算。` : dynamic
  - `tools/geology/analysis-33.html` : `存在无效行时不输出批次合格结论。` : dynamic

### geometry（dead 3 / dynamic 1 / fragment 2 / harmless 0）

- `tools/geometry/midpoint-2d.html` : `中点 = 两端坐标算术平均。 1,2 与 5,8 → (3,5)。` : dead
- `tools/geometry/polygon-interior-angle.html` : `内角 = (n−2)·180°/n` : dead
- `tools/geometry/trapezoid-area.html` : `A = (a+b)·h/2。 3/5 底、高 4 的梯形面积 16。` : dead

  其它成因样例（共 3 条，仅列前 5）：
  - `tools/geometry/arc-length.html` : `L = r·θ，θ 为弧度` : fragment
  - `tools/geometry/sector-area.html` : `A = r²·θ / 2，θ 为弧度` : fragment
  - `tools/geometry/triangle-heron.html` : `当前三边无法构成三角形，暂无示意图。` : dynamic

### health（dead 37 / dynamic 22 / fragment 11 / harmless 0）

- `tools/health/alcohol-units.html` : `Input: 2 瓶啤酒、酒精度 5%、每瓶 330 ml、体重 65 kg。 ⏎ 计算：酒精体积 = 2×330×5% = 33 ml，纯酒精质量 = 33×0.8 = 26.4 g（约 26.0 g）；按 1 标准杯≈14 g 计约 1.9 标准杯；65 kg 体重下完全代谢约需 3.9 小时。 ⏎ 结论：该次饮酒…(+50字)` : dead
- `tools/health/alcohol-units.html` : `Note:个体差异大，受体重、性别、耐受度、饮酒速度等多种因素影响` : dead
- `tools/health/blood-pressure-classifier.html` : `Input: 收缩压 120 mmHg、舒张压 80 mmHg、年龄 40。 ⏎ 计算：脉压 = 120 − 80 = 40 mmHg；平均动脉压 MAP ≈ 舒张压 + 1/3×脉压 = 80 + 13.3 = 93.3（约 93）mmHg；收缩/舒张比 = 120/80 = 1.50。 ⏎ 结论：120/80 属正…(+29字)` : dead
- `tools/health/blood-pressure-classifier.html` : `Note:当收缩压和舒张压分属不同级别时，以较高的分级为准` : dead
- `tools/health/body-fat-calculator.html` : `* 皮褶厚度法需要专业皮褶卡尺，3点法或7点法` : dead
- `tools/health/body-fat-calculator.html` : `Input: 身高 170 cm、体重 65 kg、腰围 80 cm、颈围 38 cm、臀围 95 cm（女性）。 ⏎ 海军法（女）：BFP = 163.205×log₁₀(腰+臀−颈) − 97.684×(log₁₀身高) − 78.387。 ⏎ 结果：体脂率 13.7%、脂肪重量 8.9 kg、瘦体重(LBM) 5…(+71字)` : dead
- `tools/health/body-fat-calculator.html` : `男性可选` : dead
- `tools/health/body-fat-calculator.html` : `肩胛下皮褶 (mm)` : dead
- `tools/health/body-surface-area.html` : `Input: 身高 170 cm、体重 65 kg。 ⏎ Mosteller = √((身高×体重)/3600) = √((170×65)/3600) = √(11050/3600) = √3.069 ≈ 1.752 m²。 ⏎ Du Bois ≈ 1.75 m²、Haycock ≈ 1.75 m²，三公式差异约 ±0…(+60字)` : dead
- `tools/health/caffeine-limit.html` : `Input: 体重 65 kg、人群=健康成人（6 mg/kg）、单杯饮品 95 mg。 ⏎ 每日安全上限 = 65 × 6 = 390 mg；约相当于 390 ÷ 95 ≈ 4.1 杯美式（每杯约 95 mg）。 ⏎ 中度(3mg/kg)=195 mg、高风险(6mg/kg 已含)=390 mg。 ⏎ 半衰期模型：饮…(+93字)` : dead
- `tools/health/calc-1.html` : `Input: 体重 65 kg、运动 30 分钟、基础系数 30 ml/kg。 ⏎ 计算：基础需求 = 65 × 30 = 1950 ml；运动补充约 250 ml（按 30 分钟中高强度估算）；合计 ≈ 2200 ml/天。 ⏎ 按常见 250 ml/杯折算约 8.8 杯。 ⏎ 结论：该成人每日建议饮水约 2200 …(+40字)` : dead
- `tools/health/calc-2.html` : `Input: 睡眠总时长 7 小时（其他细分按默认）。 ⏎ 评分：睡眠时长 20 分 + 入睡 10 分 + 夜醒 10 分 + 深度 15 分 + 日间 15 分 = 70 分，评级「良好」。 ⏎ 结论：7 小时睡眠且各维度正常时得分约 70，属健康区间；若时长<6h 或夜醒频繁，分数将明显下滑并提示风险。` : dead
- `tools/health/calc-3.html` : `Input: 手机 3 h、电脑 6 h、电视 1 h、平板 0.5 h。 ⏎ 计算：总屏幕 = 3 + 6 + 1 + 0.5 = 10.5 h/天；其中娱乐屏幕按常见占比约 4.5 h。 ⏎ 对照：该人群娱乐屏幕建议 ≤ 2 h/天、上限 ≤ 8 h/天。 ⏎ 结论：总屏幕 10.5 h 明显超标，娱乐 4.5 h…(+28字)` : dead
- `tools/health/calc-3.html` : `Mobile （小时/天）` : dead
- `tools/health/calc-3.html` : `Rating:≤ 推荐值「控制良好」，≤ 上限「略偏高」，> 上限「明显超标」（按人群分档）` : dead
- `tools/health/calc-3.html` : `Tablet /其他（小时/天）` : dead
- `tools/health/calorie-needs.html` : `Input: 男性、30 岁、170 cm、65 kg、活动系数 1.5（中等）、目标维持、均衡饮食（蛋白25%/碳水50%/脂肪25%）。 ⏎ BMR（Mifflin-St Jeor）= 10×65 + 6.25×170 − 5×30 + 5 = 1568 kcal。 ⏎ TDEE = 1568 × 1.5 = 23…(+238字)` : dead
- `tools/health/child-bmi-calculator.html` : `Input: 年龄 10 岁、身高 140 cm、体重 35 kg。 ⏎ BMI = 35 ÷ (1.40²) = 35 ÷ 1.96 = 17.86。 ⏎ 对照 10 岁同性别儿童参考曲线：P5 ≈ 16.5、P85 ≈ 21.5、P95 ≈ 25.0。 ⏎ 结论：实测 BMI 17.86 落在 P5–P85（正常范…(+43字)` : dead
- `tools/health/child-height-predictor.html` : `Input: 父亲 175 cm、母亲 162 cm。 ⏎ 中亲身高 = (175 + 162) ÷ 2 = 168.5 cm。 ⏎ 男孩预测 = 168.5 + 6.5 = 175.0 cm；女孩预测 = 168.5 − 6.5 = 162.0 cm。 ⏎ 遗传范围约 ±1 个` : dead
- `tools/health/child-height-predictor.html` : `Pass X光片评估骨龄，结合当前身高预测成年身高，是最准确的方法，需到医院进行。` : dead
- `tools/health/child-medication-dose.html` : `Clark Formula:剂量 = 体重(kg) × 成人剂量 ÷ 70` : dead
- `tools/health/child-medication-dose.html` : `Input: 年龄 3 岁、体重 15 kg，某药成人剂量 400 mg/次、浓度 20 mg/ml。 ⏎ Clark 公式 = 体重×成人剂量÷70 = 15×400÷70 ≈ 85.7 mg/次。 ⏎ Young 公式（≤12岁）= 年龄×成人剂量÷(年龄+12) = 3×400÷15 = 80 mg/次。 ⏎ 体…(+116字)` : dead
- `tools/health/child-medication-dose.html` : `Young Formula:剂量 = 年龄 × 成人剂量 ÷ (年龄 + 12)；标准范围 = mg/kg 单位剂量 × 体重` : dead
- `tools/health/cholesterol-ratio.html` : `Input: 总胆固醇 200、HDL 50、LDL 130、TG 150 mg/dL。 ⏎ LDL/HDL = 130 ÷ 50 = 2.60；TG/HDL = 150 ÷ 50 = 3.00；非 HDL-C = 总−HDL = 200 − 50 = 150 mg/dL。 ⏎ 评估：LDL/HDL 2.60（理想 <…(+118字)` : dead
- `tools/health/cholesterol-ratio.html` : `Note:单位换算 1 mmol/L = 38.67 mg/dL (TC/LDL/HDL)；1 mmol/L = 88.5 mg/dL (TG)` : dead
- `tools/health/convert-content.html` : `单支摄入 (mg)` : dead
- `tools/health/convert-content.html` : `年摄入 (mg)` : dead
- `tools/health/convert-content.html` : `日摄入 (mg)` : dead
- `tools/health/convert-content.html` : `每日焦油摄入估算（日 20 支 × K=1.5）` : dead
- `tools/health/dumbbell-weight-calculator.html` : `Input: 目标总重量 60 kg、杠铃杆重 20 kg。 ⏎ 每侧需配重 = (60 − 20) ÷ 2 = 20 kg。 ⏎ 若配重片规格含 20 kg 单片，则每侧 1 片共 2 片，合计 40 kg 配重 + 杆 20 kg = 60 kg，误差 0。 ⏎ 结论：目标 60 kg 用 20 kg 杆 + 每侧…(+24字)` : dead
- `tools/health/gfr-calculator.html` : `Input: 年龄 50 岁、血肌酐 1.0 mg/dL、体重 65 kg、身高 170 cm（女性）。 ⏎ CKD-EPI 公式得 eGFR ≈ 92 mL/min/1.73m²；MDRD 公式得 ≈ 84 mL/min/1.73m²。 ⏎ 分级：两者均 ≥90 属 G1 期（肾功能正常或亢进）。 ⏎ 结论：该化验提…(+50字)` : dead
- `tools/health/gfr-calculator.html` : `eGFR = 142 × min(SCr/κ, 1)^α × max(SCr/κ, 1)^(-1.200) ⏎      × 0.9938^年龄 × 性别系数 × 种族系数 ⏎  ⏎ 其中： ⏎   男性 κ=0.9, α=-0.302；女性 κ=0.7, α=-0.241 ⏎   性别系数：女性=1.012，男性=1…(+23字)` : dead
- `tools/health/ibw-calculator.html` : `Input: 身高 170 cm、实际体重 70 kg（男性）。 ⏎ Devine 公式 IBW = 50 + 0.9×(170−152.4) = 50 + 15.84 ≈ 66 kg；Robinson ≈ 66.7 kg、Miller ≈ 66 kg、Hamwi ≈ 66.7 kg。 ⏎ 结论：该男性理想体重约 66…(+21字)` : dead
- `tools/health/milk-tea-calories.html` : `Input: 中杯 500 ml、奶茶基底(+30)、全脂牛奶(+80)、全糖(100%)、加珍珠(+80)。 ⏎ 基底热量 = 30 + 80 = 110 kcal；糖热 = 500÷100 × (100%÷100) × 10 = 50 kcal；小料 = 80 kcal。 ⏎ 合计 = 110 + 50 + 80 …(+91字)` : dead
- `tools/health/one-rep-max.html` : `Input: 某动作完成 80 kg × 5 次。 ⏎ Epley = 80×(1+5/30) = 93.3 kg；Brzycki = 80×36/(37−5) = 90 kg；Lombardi = 80×5^0.1 = 94 kg；Mayhew ≈ 95.2 kg；O'Conner = 80×(1+5/40) = 9…(+62字)` : dead
- `tools/health/ovulation-calculator.html` : `Input: 月经周期 28 天、经期 5 天（以末次月经第 1 天为基准）。 ⏎ 排卵日 ≈ 周期第 (28−14) = 14 天；易孕窗 = 排卵前 5 天至排卵后 1 天 ≈ 第 9–15 天；下次月经 ≈ 第 28 天。 ⏎ 月经期 ≈ 第 1–5 天。 ⏎ 结论：该 28 天周期者易孕窗约第 9–15 天，计…(+36字)` : dead
- `tools/health/wound-healing-time.html` : `小（< 3cm）` : dead

  其它成因样例（共 33 条，仅列前 5）：
  - `tools/health/body-fat-calculator.html` : `导出明细 CSV` : dynamic
  - `tools/health/calorie-needs.html` : `导出明细 CSV` : dynamic
  - `tools/health/child-bmi-calculator.html` : `导出明细 CSV` : dynamic
  - `tools/health/convert-content.html` : `单支焦油 (mg)` : dynamic
  - `tools/health/convert-content.html` : `日尼古丁 (mg)` : dynamic

### healthcare（dead 58 / dynamic 49 / fragment 14 / harmless 2）

- `tools/healthcare/analysis-report-cost.html` : `Mass（管理/体系/检查）机制` : dead
- `tools/healthcare/antipyretic-dose.html` : `体积 = 体重 × 剂量(mg/kg) / 浓度` : dead
- `tools/healthcare/antipyretic-dose.html` : `对乙酰氨基酚每日上限约 60 mg/kg，请遵说明书。` : dead
- `tools/healthcare/blood-pressure-grade.html` : `例1（130/85）：脉压 45mmHg → 正常高值（非高血压）。例2（160/100）：脉压 60mmHg → 2 级高血压，建议就医。例3（150/85）：脉压 65mmHg → 单纯收缩期高血压。` : dead
- `tools/healthcare/bmi-2.html` : `Z ≈ (BMI − 参考均值) / 标准差` : dead
- `tools/healthcare/bmi-2.html` : `参考均值随年龄性别变化` : dead
- `tools/healthcare/bmr-calculator.html` : `Mifflin-St Jeor：男 10W+6.25H−5A+5，女 −161` : dead
- `tools/healthcare/bsa-calculator.html` : `DuBois 对普通成人较好；肥胖或儿童需专用公式（如 Haycock），极端体型下误差增大。` : dead
- `tools/healthcare/bsa-calculator.html` : `例1（65kg / 170cm）：BSA = 0.007184 × 65^0.425 × 170^0.725 = 1.754 m²。例2（80kg / 185cm）：BSA = 0.007184 × 80^0.425 × 185^0.725 = 2.036 m²。` : dead
- `tools/healthcare/bsa-calculator.html` : `算法（DuBois）：BSA = 0.007184 × 体重(kg)^0.425 × 身高(cm)^0.725，单位 m²。要求体重、身高>0。` : dead
- `tools/healthcare/chads-vasc.html` : `C/H/A/D 各 1 分；S（既往卒中/血栓）2 分；V/年龄65-74/女性各 1 分` : dead
- `tools/healthcare/checker-manager.html` : `财务（成本/利润/报表）分析` : dead
- `tools/healthcare/due-date-calc.html` : `EDD = LMP + 280 天（40 周）；当前孕周 = 距LMP天数/7` : dead
- `tools/healthcare/egfr.html` : `CKD-EPI 公式（简化版）` : dead
- `tools/healthcare/egfr.html` : `如 1` : dead
- `tools/healthcare/egfr-calculator.html` : `MDRD 175 简化式：175·Scr⁻¹·¹⁵⁴·年龄⁻⁰·²⁰³·(女×0.742)` : dead
- `tools/healthcare/egfr-calculator.html` : `用 MDRD 175 简化公式估算 eGFR，并输出 CKD 分期。` : dead
- `tools/healthcare/fat-loss-deficit.html` : `1 kg 脂肪 ≈ 7700 kcal；日缺口 = 总缺口 / 天数` : dead
- `tools/healthcare/gfr-cockcroft.html` : `为什么本工具数字异常大？` : dead
- `tools/healthcare/gfr-cockcroft.html` : `工具实现漏了标准公式的 /72 除数，导致结果约为真实值的 72 倍；请以标准 Cockcroft-Gault 公式（含 /72）为准，或改用本站 eGFR 工具。` : dead
- `tools/healthcare/gfr-cockcroft.html` : `算法（标准 Cockcroft-Gault）：CrCl = (140−年龄)×体重(kg) ÷ (72×SCr_mg/dL) × (女×0.85)，单位 mL/min；体标化 CrCl×1.73/BSA。本工具页面实现漏除以 72，其显示值约为标准的 72 倍（如默认约 6961 mL/min，明显失真），下方给出标准…(+2字)` : dead
- `tools/healthcare/gfr-cockcroft.html` : `算法（标准 Cockcroft-Gault）：CrCl = (140−年龄)×体重(kg) ÷ (72×SCr_mg/dL) × (女×0.85)，单位 mL/min；体表面积归一值 = CrCl×1.73÷BSA，BSA 按输入身高用 DuBois 式（0.007184×体重^0.425×身高^0.725）计算，不再…(+7字)` : dead
- `tools/healthcare/healthcare.html` : `儿童剂量 = 成人剂量 × (儿童体重 / 成人体重)` : dead
- `tools/healthcare/healthcare.html` : `儿童剂量按体重换算（按体重比例 + 成人剂量倍数封顶，本页代码口径）：按体重剂量 = 成人剂量 × (儿童体重 ÷ 参考成人体重)（mg）；受限剂量 = min(按体重剂量, 成人剂量 × 最大倍数限制)（mg，最大倍数须 ≥1，小于 1 时拒绝计算以防剂量被压缩至 0）；剂量比例 = 儿童体重 ÷ 成人体重 × 10…(+77字)` : dead
- `tools/healthcare/healthcare-2.html` : `滴速(滴/分) = 液体总量 × 滴系数 / 时间(分)` : dead
- `tools/healthcare/healthcare-3.html` : `血钠变化 ≈ (输注液钠 − 当前血钠) / (总体水 + 1)` : dead
- `tools/healthcare/healthcare-4.html` : `NYHA I-IV 级按症状和活动受限程度划分` : dead
- `tools/healthcare/healthcare-5.html` : `蛋白质需求 = 体重 × 0.8 g/kg × 活动系数 × 目标系数` : dead
- `tools/healthcare/ideal-weight.html` : `Devine：男 50 + 2.3×超出英寸，女 45.5 + 2.3×超出英寸；Hamwi：男 48 + 2.7×超出英寸，女 45.5 + 2.2×超出英寸；Miller：男 56.2 + 1.41×超出英寸，女 53.1 + 1.41×超出英寸；Robinson：男 52 + 1.9×超出英寸，女 49 + 1.…(+56字)` : dead
- `tools/healthcare/ideal-weight.html` : `in = 175 ÷ 2.54 = 68.90，超出 8.90 英寸 ⇒ Devine = 50 + 2.3×8.90 = 70.5 kg；Hamwi = 48 + 2.7×8.90 = 72.0 kg；Miller = 56.2 + 1.41×8.90 = 68.7 kg；Robinson = 52 + 1.9×8.…(+27字)` : dead
- `tools/healthcare/ideal-weight.html` : `临床给药与通气最常用 Devine；Hamwi 多用于营养评估，Miller 与 Robinson 是后来的修正版。同一身高四式差 2–4 kg 属正常，关键是同一场景内保持一致，别混用。` : dead
- `tools/healthcare/ideal-weight.html` : `为什么身高低于 152 cm 不给结果？` : dead
- `tools/healthcare/ideal-weight.html` : `四个公式该用哪个？` : dead
- `tools/healthcare/ideal-weight.html` : `四套公式都以 5 英尺为基准做线性外推，低于基准时结果会明显偏低甚至为负，不能反映真实生理值，应改用儿科或专用公式。` : dead
- `tools/healthcare/ideal-weight.html` : `四套公式（均以 5 英尺 = 60 英寸为基准，超出部分按系数递增，单位 kg）` : dead
- `tools/healthcare/ideal-weight.html` : `算例（175 cm、男）` : dead
- `tools/healthcare/index.html` : `使用 CKD-EPI 简化公式，输入血肌酐、年龄与性别，估算肾小球滤过率 eGFR，评估肾功能并提示异常（如 eGFR<60 持续三月提示慢性肾病需就医）。` : dead
- `tools/healthcare/map.html` : `MAP ≈ 舒张压 + (收缩压 − 舒张压) / 3` : dead
- `tools/healthcare/nrs2002.html` : `BMI <20.5（0-3 分）` : dead
- `tools/healthcare/nrs2002.html` : `⚠ 请为每项输入 0–1 的整数分值，不能留空或超出范围` : dead
- `tools/healthcare/nrs2002.html` : `⚠ 请为每项输入 0–3 的整数分值，不能留空或超出范围` : dead
- `tools/healthcare/nrs2002.html` : `、体重下降、摄食减少三项取最高分（0–3）；总分 = 营养受损+疾病严重程度+年龄(≥70 加 1)，总分 0–7；总分≥3 存在营养风险。` : dead
- `tools/healthcare/nrs2002.html` : `例1（营养三项 1/1/1 取最高 1、疾病 2、年龄 1）：总分 4 分，存在营养风险。例2（营养三项均 3、疾病 0、年龄 0）：营养受损 3 分、总分 3 分，仍达风险阈值。` : dead
- `tools/healthcare/nrs2002.html` : `算法（NRS2002）：营养受损评分 = max(BMI 项, 体重下降项, 进食量项)（取最高项，0–3 分）；总分 = 营养受损 + 疾病严重程度 + 年龄(≥70 加 1)；总分 ≥3 存在营养风险。` : dead
- `tools/healthcare/parkland.html` : `Parkland 的前 8h 半量是独立时段目标，不是把 24h 总量平均分摊：t≤8h 按「半量 × t/8」累计，8h 时正好达到总量 1/2；t>8h 才进入后 16h 的「半量 × (t−8)/16」累计，24h 达到总量。按 24h 均摊会在 8h 只给到 1/3（如 70kg、30% 为 2800mL 而非…(+19字)` : dead
- `tools/healthcare/parkland.html` : `一半在前 8h，一半在后 16h` : dead
- `tools/healthcare/parkland.html` : `例1（70kg、TBSA 30%）：24h=4×70×30=8400mL，前 8h=4200mL，后 16h=4200mL；若受伤已 8 小时，当前应输=8400×8/24=2800mL。例2（60kg、40%）：24h=9600mL。` : dead
- `tools/healthcare/parkland.html` : `已输注 8 小时，为什么累计应是总量的一半，而不是三分之一？` : dead
- `tools/healthcare/parkland.html` : `算法（Parkland）：24h 总量 = 4 × 体重(kg) × 烧伤面积 TBSA(%) mL；前 8h 输半量，后 16h 输另半量；某时刻应输 = 总量 × 已过去小时/24。要求体重、面积>0。` : dead
- `tools/healthcare/qtc.html` : `例1（QT 400ms、HR 75、男）：RR=0.8，Bazett=400/√0.8=447.2ms，Fridericia=400/∛0.8=430.9ms，超男上限 440 需关注。例2（QT 360、HR 60、女）：Bazett=360ms，正常（女上限 450）。` : dead
- `tools/healthcare/qtc.html` : `正常上限（女）：` : dead
- `tools/healthcare/qtc.html` : `正常上限（男）：` : dead
- `tools/healthcare/qtc.html` : `算法：QTc Bazett = QT / √(RR)，RR=60/心率(秒)；QTc Fridericia = QT / ∛(RR)；正常上限男 440ms、女 450ms，≥500ms 高风险。要求 QT、心率>0。` : dead
- `tools/healthcare/resp-rate.html` : `仅直观反映距对应年龄参考范围中值的程度（成人范围中值为 16）；真正判断看绝对值与伴随症状（发绀、胸陷、嗜睡），本工具不替代医生。` : dead
- `tools/healthcare/resp-rate.html` : `成人正常静息呼吸 12–20 次/分` : dead
- `tools/healthcare/water-intake.html` : `饮水 ≈ 体重(kg) × 35 mL × 活动 × 气候系数` : dead
- `tools/healthcare/weight-dosage.html` : `日剂量 = 体重 × mg/kg；单次 = 日剂量 / 次数` : dead
- `tools/healthcare/wells.html` : `总分 = 各项得分之和 ≤4 低度可能，>4 高度可能` : dead

  其它成因样例（共 65 条，仅列前 5）：
  - `tools/healthcare/antipyretic-dose.html` : `⚠ 3 月龄以下婴儿发热应及时就医，不建议自行使用退热药；请由医生评估后再决定。` : dynamic
  - `tools/healthcare/antipyretic-dose.html` : `⚠ 6 月龄及以下婴儿用药需医师评估，请遵医嘱。` : dynamic
  - `tools/healthcare/blood-pressure-grade.html` : `脉压 = 收缩压 − 舒张压` : fragment
  - `tools/healthcare/blood-pressure-grade.html` : `脉压：` : dynamic
  - `tools/healthcare/blood-pressure-grade.html` : `分级：` : dynamic

### hematology（dead 15 / dynamic 3 / fragment 0 / harmless 0）

- `tools/hematology/dic-scoring.html` : `ISTH 显性 DIC 评分：血小板 <50(+2)、50–100(+1)；D-二聚体 >10(+3)、5–10(+2)、>1(+1)；PT 延长 >6s(+2)、3–6s(+1)；纤维蛋白原 <1.0(+1)。前提：必须存在可诱发 DIC 的基础疾病；总分 ≥5 显性 DIC、3–4 非显性、<3 不支持。` : dead
- `tools/hematology/dic-scoring.html` : `例（血小板=45、D-二聚体=8.5、PT 延长=6s、纤维蛋白原=1.2）：血小板<50(+2)、D-二聚体 5–10(+2)、PT 3–6s(+1)、纤维蛋白原≥1.0(+0) → 总分=5 分 → 达显性 DIC 阈值，需立即治疗基础疾病并替代/抗凝。` : dead
- `tools/hematology/hemophilia-treatment.html` : `提示：实际剂量需根据回收率个体化调整，回收率<66%提示存在抑制物。预防治疗推荐FVIII 25-40 IU/kg 每周3次，FIX 40-100 IU/kg 每周2次（延半衰期产品可减频）。仅供学习参考。` : dead
- `tools/hematology/hlh-diagnosis.html` : `HGB <90 g/L (婴儿<100)` : dead
- `tools/hematology/hlh-diagnosis.html` : `TG≥3.0 mmol/L 或 Fib<1.5 g/L` : dead
- `tools/hematology/iron-overload.html` : `提示：血清铁蛋白受炎症影响，急性期可能假性升高。MRI T2*是评估心脏和肝脏铁过载的金标准。祛铁目标：铁蛋白<1000 μg/L（地贫），<500-1000 μg/L（MDS）。仅供学习参考。` : dead
- `tools/hematology/m-protein.html` : `(Anemia)：血红蛋白 <100 g/L 或低于正常下限20g/L` : dead
- `tools/hematology/m-protein.html` : `(Renal)：肌酐清除率 <40 mL/min 或血肌酐 >177 μmol/L` : dead
- `tools/hematology/mm-staging.html` : `白蛋白 ≥35 g/L 且 β2-MG <3.5 mg/L` : dead
- `tools/hematology/mpn-scoring.html` : `DIPSS适用于随访中评估，HGB<100计2分（其余变量各1分）。DIPSS-plus在DIPSS基础上增加血小板<100、输血依赖、不良核型各1分。仅供临床参考。` : dead
- `tools/hematology/mpn-scoring.html` : `IPSS变量：年龄>65(1分)、HGB<100(1分)、WBC>25(1分)、外周血原始细胞>1%(1分)、全身症状(1分)` : dead
- `tools/hematology/rater-6.html` : `评分 <5 分提示非显性 DIC，建议 24-48 小时后复查` : dead
- `tools/hematology/rater-risk-1.html` : `血小板 <30×10⁹/L 伴出血需紧急处理` : dead
- `tools/hematology/transfusion-dose.html` : `HGB<70g/L 或 <80g/L(有症状)` : dead
- `tools/hematology/transfusion-dose.html` : `PLT<20 或 <50(出血/手术)` : dead

  其它成因样例（共 3 条，仅列前 5）：
  - `tools/hematology/dic-scoring.html` : `请完整填写血小板、D-二聚体、PT 延长与纤维蛋白原四项数值` : dynamic
  - `tools/hematology/dic-scoring.html` : `数值不能为负，请检查输入` : dynamic
  - `tools/hematology/rater-5.html` : `< 60岁（0分）` : dynamic

### hr（dead 64 / dynamic 69 / fragment 17 / harmless 2）

- `tools/hr/analysis-29.html` : `期初 220 人、期末 200 人（平均在职 210 人）、期间离职 18 人、单人替换成本 24000 元、胜任周期 2 个月、人均月产出 30000 元 → 离职率 = 18/210 = 8.57%；替换成本 432000 元，产能爬坡损失 = 18×2×30000×0.5 = 540000 元；离职总成本 972…(+40字)` : dead
- `tools/hr/analysis-29.html` : `离职率 = 离职人数 ÷ 平均在职人数 × 100%（平均在职人数 =（期初 + 期末）÷ 2）；替换成本 = 离职人数 × 单人替换成本；产能爬坡损失 = 离职人数 × 胜任周期 × 人均月产出 × 50%；离职总成本 = 替换成本 + 产能爬坡损失。` : dead
- `tools/hr/annual-leave-prorate.html` : `档位 5 天；在职天数 = 365−74+1 = 292（含入职与截止当日）；折算 = 292/365×5 = 4.00 → 取 0.5 天档 4 天。` : dead
- `tools/hr/assessor-training-hr.html` : `培训评估 = 需求/效果加权` : dead
- `tools/hr/assessor-training-hr.html` : `本页用柯氏前两层（反应/学习）打分合成培训效果分；行为层与结果层需训后 1–3 个月跟踪，另做` : dead
- `tools/hr/assessor-training-hr.html` : `满意度 9.0 → L1 = 90；知识测试通过率 92% → L2 = 92；能力均分 6.0 → 8.0，提升率 = 2.0/6.0 = 33.3% → L3 = min(100, 66.7) = 66.7；综合 =（90 + 92 + 66.7）÷ 3 = 82.9，评级「优秀」。` : dead
- `tools/hr/assessor-training-hr.html` : `算例` : dead
- `tools/hr/attendance-stats.html` : `、休息日加班可转调休，与 comp-time/overtime 工具口径一致。` : dead
- `tools/hr/attendance-stats.html` : `出勤率 = 实际出勤天数 ÷ 应出勤天数 × 100%，实际出勤 = max(应出勤 − 旷工 − 请假, 0)（负值截 0，加班不参与计算）；应扣 = 迟到次数×迟到单价 + 早退次数×早退单价 + 旷工天数×旷工单价；加班费 = 加班小时 × 加班单价；全勤奖：无迟到/早退/旷工/请假才发放。校验：应出勤天数缺省按…(+99字)` : dead
- `tools/hr/attendance-stats.html` : `出勤率 = 实际出勤天数 ÷ 应出勤天数 × 100%；扣款 = 迟到×迟到单价 + 早退×早退单价 + 旷工×旷工单价。数据仅本地计算，不上传。` : dead
- `tools/hr/attendance-stats.html` : `应出 22 实出 20` : dead
- `tools/hr/attendance-stats.html` : `延时加班走` : dead
- `tools/hr/attendance-stats.html` : `异常考勤（连续迟到）标记供主管跟进。` : dead
- `tools/hr/attendance-stats.html` : `按全勤规则核算全勤奖，并按加班单价核算加班费。` : dead
- `tools/hr/attendance-stats.html` : `某员工连续 5 天迟到，工具标红并提示谈话。` : dead
- `tools/hr/attendance-stats.html` : `核算全勤奖与加班调休余额。` : dead
- `tools/hr/attendance-stats.html` : `缺勤 2 天、加班 8 小时；全勤奖因缺勤取消，加班 8h 进入调休池。` : dead
- `tools/hr/attendance-stats.html` : `考勤统计 = 出勤/缺勤/加班` : dead
- `tools/hr/attendance-stats.html` : `迟到/早退统计，批量计算出勤率与应扣薪资` : dead
- `tools/hr/attendance-stats.html` : `迟到趋势` : dead
- `tools/hr/bandwidth-1.html` : `不是。工具按均匀分布近似，取中位 × (1 ∓ 幅度%/2)；真实市场分位需以薪酬调研数据为准。` : dead
- `tools/hr/bandwidth-1.html` : `幅度是参数输入（相对中位值向两侧展开的百分比）；带宽比 = 上限 ÷ 下限，是结果指标。例如中位 8000、±30% 时带宽比为 1.857，而不是 30%。` : dead
- `tools/hr/calc-81.html` : `两档岗位内推核算` : dead
- `tools/hr/calc-81.html` : `同上但稀缺岗系数改为 2.0：稀缺岗小计 500×2.0×2=2000 元，激励总额升至 6000 元，单位录用成本 600.00 元，ROI 降至 1233.33%（(80000−6000)÷6000）。系数提高会抬升激励总额、降低相对 ROI，用于判断加码是否值得。` : dead
- `tools/hr/calc-81.html` : `基数 500 元，普通岗系数 1.0、8 人，稀缺岗系数 1.5、2 人。普通岗小计 500×1.0×8=4000 元，稀缺岗小计 500×1.5×2=1500 元，激励总额 5500 元。推荐 40 人、录用 10 人 → 转化率 25%，单位录用成本 5500÷10=550.00 元；外部渠道人均 8000 元时总…(+36字)` : dead
- `tools/hr/calc-81.html` : `提高稀缺岗系数` : dead
- `tools/hr/calc-81.html` : `普遍设转正或满 3-6 月护航期，防短留即奖；本工具按一次性计发口径测算，过保口径请把「人数」改为实际过保人数后重算，不做自动滚动统计。` : dead
- `tools/hr/hris-zizhuyuaiduibijisuanqi.html` : `A 功能 9 成本 6、B 功能 7 成本 8、C 功能 8 成本 7，按权重合成 → B 总分最高，工具推荐采购中端 SaaS。` : dead
- `tools/hr/hris-zizhuyuaiduibijisuanqi.html` : `AI 能力现在重要吗？` : dead
- `tools/hr/hris-zizhuyuaiduibijisuanqi.html` : `TCO 对比` : dead
- `tools/hr/hris-zizhuyuaiduibijisuanqi.html` : `三方案加权` : dead
- `tools/hr/hris-zizhuyuaiduibijisuanqi.html` : `关于「数字化（HRIS/自助/AI）设想」` : dead
- `tools/hr/hris-zizhuyuaiduibijisuanqi.html` : `向决策层输出雷达式对比结论。` : dead
- `tools/hr/hris-zizhuyuaiduibijisuanqi.html` : `对比自研与采购 SaaS 的总拥有成本（TCO）。` : dead
- `tools/hr/hris-zizhuyuaiduibijisuanqi.html` : `按企业阶段：成长期重成本与速度、规范期重合规与扩展，权重随之调整。` : dead
- `tools/hr/hris-zizhuyuaiduibijisuanqi.html` : `数字化（HRIS/自助/AI）设想。免费在线工具，纯前端处理，数据不上传，保护隐私安全。` : dead
- `tools/hr/hris-zizhuyuaiduibijisuanqi.html` : `权重怎么设？` : dead
- `tools/hr/hris-zizhuyuaiduibijisuanqi.html` : `自研三年 120 万 vs SaaS 年费 30 万，工具折现后给出拐点。` : dead
- `tools/hr/hris-zizhuyuaiduibijisuanqi.html` : `若已有大量重复录入与问答，AI 自助可降 30%+ 事务量，建议给足权重。` : dead
- `tools/hr/hris-zizhuyuaiduibijisuanqi.html` : `这个工具能算 TCO 或投资回报吗？` : dead
- `tools/hr/hris-zizhuyuaiduibijisuanqi.html` : `选型时按功能、实施、成本、扩展、AI 五大维度加权打分。` : dead
- `tools/hr/hris-zizhuyuaiduibijisuanqi.html` : `👥 HRIS、自助与AI对比计算器` : dead
- `tools/hr/hris-zizhuyuaiduibijisuanqi.html` : `📚 深度解析：HRIS、员工自助与 AI 能力对比评分` : dead
- `tools/hr/index.html` : `HRIS/自助/AI 对比计算器。输入 HRIS、员工自助与 AI 方案的各项参数，对比数字化人力管理的成本与效率，用于 HR 数字化选型参考。` : dead
- `tools/hr/index.html` : `批量导入员工每日打卡记录，统计迟到、早退、缺勤与请假天数，计算个人与团队出勤率，并按既定扣款规则核算应扣薪资，生成可导出考勤报表，减轻 HR 月末核算负担。` : dead
- `tools/hr/index.html` : `招聘（渠道/预算/漏斗）统计工具。输入各渠道花费、简历与录用数据，按财务规则测算招聘漏斗与单聘成本，用于招聘预算与渠道绩效分析（结果仅供参考）。` : dead
- `tools/hr/index.html` : `数字化（HRIS/自助/AI）设想` : dead
- `tools/hr/index.html` : `补休调休计算器是一款免费的在线人力资源工具，加班攒了多少补休？按《劳动法》倍数：工作日加班 1.5 倍、休息日 2 倍（可补休）、法定节假日 3 倍。输入加班时长自动换算补休天数。纯前端运行、数据不…` : dead
- `tools/hr/overtime-pay-calc.html` : `本工具直接输入基本时薪；若只有月薪，先按「月薪 ÷ 21.75 ÷ 8」折算（例：月薪 8000 → 45.98 元/小时）。基数应为劳动合同约定的正常工作时间工资（通常为基本工资/岗位工资），不含加班费、津贴补贴，且不低于当地最低工资。` : dead
- `tools/hr/performance-ranking.html` : `归一化得分 = min(100, 本人得分 ÷ 团队最高分 × 100)；相对差距 = (最高 − 本人) ÷ 最高 × 100%` : dead
- `tools/hr/performance-ranking.html` : `绩效归一化把不同量纲、不同团队得分映射到 0–100 的同一尺度：归一化得分=本人÷最高×100，相对差距=(最高−本人)÷最高，便于跨组横向排名。` : dead
- `tools/hr/performance-score.html` : `绩效 = 指标加权` : dead
- `tools/hr/recruitment-funnel.html` : `招聘转化 = 各阶段/上一阶段` : dead
- `tools/hr/social-insurance.html` : `社保 = 基数 × 缴费比例` : dead
- `tools/hr/stats-funnel-recruit.html` : `三渠道 CPO 对比` : dead
- `tools/hr/stats-funnel-recruit.html` : `内推花 1 万、200 简历、8 offer、7 入职 → CPO 1250、单入职成本 1428.57；招聘网站花 3 万、4 offer、3 入职 → CPO 7500、单入职成本 10000；猎头花 6 万、6 offer、5 入职 → CPO 10000、单入职成本 12000。合计 10 万、入职 15 人 …(+56字)` : dead
- `tools/hr/stats-funnel-recruit.html` : `削减网站 30% 预算转内推，预计同等花费多 3 个 offer。` : dead
- `tools/hr/stats-funnel-recruit.html` : `发放 Offer 人数` : dead
- `tools/hr/stats-funnel-recruit.html` : `实际入职人数` : dead
- `tools/hr/stats-funnel-recruit.html` : `猎头花 6 万得 6 offer → CPO 1 万；内推花 1 万得 8 offer → CPO 1250；招聘网站花 3 万得 4 offer → CPO 7500，内推性价比最高。` : dead
- `tools/hr/stats-funnel-recruit.html` : `简历 / 投递人数` : dead
- `tools/hr/stats-funnel-recruit.html` : `输入招聘漏斗各环节人数（简历 → 面试 → Offer → 入职），自动计算各阶段转化率与整体转化率，定位流失最严重的环节。计算在浏览器本地完成。` : dead
- `tools/hr/stats-funnel-recruit.html` : `进入面试人数` : dead
- `tools/hr/tracking-hours.html` : `培训学时 = 累计 − 缺口` : dead

  其它成因样例（共 88 条，仅列前 5）：
  - `tools/hr/analysis-29.html` : `请输入期初与期末在职人数` : dynamic
  - `tools/hr/analysis-29.html` : `离职人数与成本参数不能为负数` : dynamic
  - `tools/hr/annual-leave-calc.html` : `满1年不满10年：5天；满10年不满20年：10天；满20年：15天` : dynamic
  - `tools/hr/annual-leave-calc.html` : `请填写连续工龄与本年工作月数后再计算。` : dynamic
  - `tools/hr/annual-leave-calc.html` : `工龄需为 ≥0 的有效数字，工作月数须为 0–12 的整数（按整月折算）。` : dynamic

### hvac（dead 3 / dynamic 10 / fragment 0 / harmless 2）

- `tools/hvac/dehumidifier.html` : `进风含湿量 d1≈16.9 g/kg，处理到 15℃/90%RH 出风 d2≈9.5 g/kg；小时除湿 W = 120×1.2×(16.9−9.5)/1000 ≈ 1.06 kg/h，日约 25 L。` : dead
- `tools/hvac/index.html` : `暖通空调工具集合收录了 10 个免费在线工具，覆盖暖通空调场景下的常见计算、换算与查询需求。无论你是相关领域的从业者、学生还是普通用户，都能在这里找到即用即走的实用小工具。所有工具纯前端运行，数据不上传服务器，保护隐私安全。` : dead
- `tools/hvac/kongtiaolengfuhejisuan.html` : `冷负荷 ≈ 围护传热 + 人员显热 + 设备散热 + 新风负荷（经验估算法）` : dead

  其它成因样例（共 12 条，仅列前 5）：
  - `tools/hvac/cooling-tower.html` : `❄️ 冷却塔散热与补水量计算器` : harmless
  - `tools/hvac/kongtiaolengfuhejisuan.html` : `🧮 空调冷负荷计算` : harmless
  - `tools/hvac/kongtiaolengfuhejisuan.html` : `人员负荷 (W)` : dynamic
  - `tools/hvac/kongtiaolengfuhejisuan.html` : `围护结构负荷 (W)` : dynamic
  - `tools/hvac/kongtiaolengfuhejisuan.html` : `总冷负荷 (kW)` : dynamic

### hydraulic（dead 25 / dynamic 39 / fragment 7 / harmless 0）

- `tools/hydraulic/area-capacity.html` : `库容 = ∫面积 dH` : dead
- `tools/hydraulic/bernoulli-velocity.html` : `P + ½ρv² + ρgh = 常数` : dead
- `tools/hydraulic/calc-1.html` : `管道压降 = 沿程+局部损失` : dead
- `tools/hydraulic/calc-2.html` : `水泵扬程 H = 几何扬程 + 损失` : dead
- `tools/hydraulic/calc-26.html` : `明渠均匀流 v = (1/n)R^(2/3)S^(1/2)` : dead
- `tools/hydraulic/calc-54.html` : `水闸启闭力 = 总水压力 + 摩擦` : dead
- `tools/hydraulic/calc-power-2.html` : `换热功率 Q = k·A·ΔT` : dead
- `tools/hydraulic/calc-pressure.html` : `💡 压力流采用 Hazen-Williams Formula:hf = 10.67·L·Q^1.852 / (C^1.852·D^4.87)；重力流采用 Manning Formula:Q = (1/n)·(D/4)^(2/3)·S^(1/2)·(πD²/4)。雷诺数 Re = V·D/ν。` : dead
- `tools/hydraulic/calc-pressure-capacity.html` : `等温过程适用于补油保压（动作时间>1min），绝热适用于快速动作（<1min）` : dead
- `tools/hydraulic/calc-pressure-capacity.html` : `蓄能器容量 = 容积×压力系数` : dead
- `tools/hydraulic/calc-protection.html` : `水锤 Δp = ρ·a·Δv` : dead
- `tools/hydraulic/calc-speed-itinerary.html` : `液压缸推力 F = p·A` : dead
- `tools/hydraulic/density-4.html` : `填筑密度 = 干密度控制` : dead
- `tools/hydraulic/flow.html` : `m=0.49、b=20、H=3 → Q=0.49×20×√(2×9.81)×3^1.5≈225 m³/s，与下游安全下泄比对。` : dead
- `tools/hydraulic/flow.html` : `溢洪道泄流 Q = m·b·√(2g)·H^(3/2)` : dead
- `tools/hydraulic/flow-1.html` : `生态下泄流量 = 多年均值×系数` : dead
- `tools/hydraulic/flow-pipeline.html` : `引水管径 D = √(4Q/(πv))` : dead
- `tools/hydraulic/gear-1.html` : `压力分级：低压<2.5MPa 齿轮泵，中压2.5~8MPa 叶片泵，中高压8~16MPa 柱塞泵，高压>16MPa 柱塞泵` : dead
- `tools/hydraulic/gear-1.html` : `液压泵排量 = 流量/转速` : dead
- `tools/hydraulic/power-3.html` : `泵站效率 η = 输出/输入` : dead
- `tools/hydraulic/power-torque.html` : `液压马达 T = p·V/(2π)` : dead
- `tools/hydraulic/pressure-flow-1.html` : `液压阀流量 Q = C_d·A·√(2Δp/ρ)` : dead
- `tools/hydraulic/speed-pressure.html` : `液压回路 v = Q/A` : dead
- `tools/hydraulic/spillway-calc.html` : `m=0.49、b=20、H=3 → Q=0.49×20×√(2×9.81)×3^1.5≈225 m³/s，与设计洪量比对。` : dead
- `tools/hydraulic/yeyayouxiangsheji.html` : `油箱容积 = 泵流量×系数` : dead

  其它成因样例（共 46 条，仅列前 5）：
  - `tools/hydraulic/calc-flow-1.html` : `气动维护（排水/加油/检修）周期` : fragment
  - `tools/hydraulic/calc-speed.html` : `气动维护（排水/加油/检修）周期` : fragment
  - `tools/hydraulic/daohongxi-shuitousunshi-maishen.html` : `沿程水头损失 hf=λ(L/D)·v²/(2g)` : dynamic
  - `tools/hydraulic/daohongxi-shuitousunshi-maishen.html` : `局部水头损失 hj=Σζ·v²/(2g)` : dynamic
  - `tools/hydraulic/daohongxi-shuitousunshi-maishen.html` : `总水头损失 hf＋hj` : dynamic

### image（dead 1 / dynamic 4 / fragment 0 / harmless 0）

- `tools/image/image-resize.html` : `JPEG/WebP 格式不支持透明背景，输出时会以白色填充` : dead

  其它成因样例（共 4 条，仅列前 5）：
  - `tools/image/image-compress.html` : `导出明细 CSV` : dynamic
  - `tools/image/image-converter.html` : `已铺白底` : dynamic
  - `tools/image/image-converter.html` : `已保留透明` : dynamic
  - `tools/image/nine-grid-cutter.html` : `上传图片后显示切割参数。` : dynamic

### insurance（dead 22 / dynamic 0 / fragment 3 / harmless 0）

- `tools/insurance/average-severity.html` : `平均赔付额 = 总赔款/索赔件数` : dead
- `tools/insurance/calc-1.html` : `豁免保费现值 = Σ 未缴保费_t/(1+i)^t` : dead
- `tools/insurance/claim-frequency.html` : `理赔频率 = 理赔次数/风险暴露` : dead
- `tools/insurance/claim-reserve.html` : `准备金 = 终极赔款 − 已付赔款` : dead
- `tools/insurance/combined-ratio.html` : `综合成本率 < 100% 表示承保盈利。` : dead
- `tools/insurance/combined-ratio.html` : `综合成本率 = (赔款+费用)/保费 × 100%` : dead
- `tools/insurance/endowment-premium.html` : `两全保费 = 身故现值 + 满期现值` : dead
- `tools/insurance/expense-ratio.html` : `费用率 = 营运费用/保费` : dead
- `tools/insurance/gross-premium-loading.html` : `毛保费 = 纯保费 × (1+附加费率)` : dead
- `tools/insurance/ibnr-estimate.html` : `IBNR = 终极赔款 × (1−已付比例)` : dead
- `tools/insurance/ibnr-reserve.html` : `IBNR = 已发生赔款 − 已报告赔款` : dead
- `tools/insurance/level-premium-life.html` : `年保费 = 趸缴保费/äₙ` : dead
- `tools/insurance/life-cover-need.html` : `寿险保额 = 年收入缺口 × 折现年金因子` : dead
- `tools/insurance/loss-ratio.html` : `赔付率 = 已决赔款/保费` : dead
- `tools/insurance/mortality-prob.html` : `死亡率 qₓ = 1−pₓ` : dead
- `tools/insurance/net-single-premium.html` : `NSP = Σ 给付_t/(1+i)^t` : dead
- `tools/insurance/premium-calc.html` : `保费 = 保额 × 费率` : dead
- `tools/insurance/premium-elasticity.html` : `弹性 = (Δ需求/需求)/(Δ保费/保费)` : dead
- `tools/insurance/premium-elasticity.html` : `弹性<1 为缺乏弹性（刚需）。` : dead
- `tools/insurance/pure-premium-rate.html` : `纯费率 = 期望损失/暴露单位` : dead
- `tools/insurance/uw-margin.html` : `承保利润 = 保费 × (1−综合成本率)` : dead
- `tools/insurance/uw-margin.html` : `综合成本率<100% 才承保盈利。` : dead

  其它成因样例（共 3 条，仅列前 5）：
  - `tools/insurance/annuity-nsp.html` : `净单保费 = 年给付 × äₙ` : fragment
  - `tools/insurance/mortality-table.html` : `x岁死亡人数 = lx × qx` : fragment
  - `tools/insurance/uw-profit.html` : `承保利润 = 保费 − 赔款 − 费用` : fragment

### investment（dead 12 / dynamic 1 / fragment 0 / harmless 0）

- `tools/investment/discounted-payback.html` : `折现回收期 = 累计折现现金流回正年限` : dead
- `tools/investment/eps-calc.html` : `EPS = (净利−优先股)/流通股数` : dead
- `tools/investment/index.html` : `投资理财工具集合收录了 24 个免费在线工具，覆盖投资理财场景下的常见计算、换算与查询需求。无论你是相关领域的从业者、学生还是普通用户，都能在这里找到即用即走的实用小工具。所有工具纯前端运行，数据不上传服务器，保护隐私安全。` : dead
- `tools/investment/lifespan-12.html` : `回报期<3年为优秀，3~5年为良好，>5年需评估` : dead
- `tools/investment/lifespan-12.html` : `节能收益 = 功率 × 日运行时间 × 年天数 × 节能率 × 电价 × 寿命` : dead
- `tools/investment/payback-period.html` : `回收期 = 累计现金流由负转正年限` : dead
- `tools/investment/profitability-index.html` : `PI = 现值 / 初始投资` : dead
- `tools/investment/real-rate-return.html` : `实际 = (1+名义)/(1+通胀) − 1` : dead
- `tools/investment/retention-ratio.html` : `留存率 = 1 − 股利支付率` : dead
- `tools/investment/roi-calc.html` : `ROI = (收益 − 成本)/成本` : dead
- `tools/investment/sustainable-growth.html` : `g = ROE × 留存率` : dead
- `tools/investment/yield-spread.html` : `利差 = 债券收益率 − 基准收益率` : dead

  其它成因样例（共 1 条，仅列前 5）：
  - `tools/investment/lifespan-12.html` : `全寿命节电量 (kWh)` : dynamic

### it（dead 1050 / dynamic 2621 / fragment 116 / harmless 18）

- `tools/it/ascii-tree-generator.html` : `关于「ASCII 目录树生成器」` : dead
- `tools/it/barcode-ean.html` : `输入数字串（如 '123456789'）→ 渲染 EAN 条码图形；请按规范长度与校验位填写。` : dead
- `tools/it/barcode-msi.html` : `MSI（Modified Plessey）是脉冲调制型条码，每位数字用 8 个单元表示：0 编码为「窄空宽条」，1 编码为「宽条窄空」，其余数字按二进制位展开为 8 个宽窄交替的单元。它只含数字、无字母，密度中等，主要用在零售货架标签与仓库库位标识。MSI 本身不校验，实践中常追加 Mod 10（即 Luhn 算法）、…(+32字)` : dead
- `tools/it/barcode-msi.html` : `校验：Mod 10（Luhn）/ Mod 11 / Mod 1010 可选` : dead
- `tools/it/barcode-msi.html` : `每位数字 = 8 个单元（0→窄空宽条，1→宽条窄空，其余按二进制展开）` : dead
- `tools/it/charset-detector.html` : `不能。粘贴框里拿到的是已经解码后的字符串，原始字节与 BOM 已不可见，因此本页不做 GBK/Big5 猜测。若需按 GBK 读取文件，请在导入 CSV/文本时直接指定正确编码。` : dead
- `tools/it/charset-detector.html` : `为什么有时无法修复？` : dead
- `tools/it/charset-detector.html` : `判断一段文本是否已经发生不可逆的解码失败（出现 U+FFFD 替换符）。` : dead
- `tools/it/charset-detector.html` : `双重编码还原要求整串字符都能折算回 cp1252 字节，且按 UTF-8 严格解码合法。含 U+FFFD、超出 cp1252 的字符（如已正确显示的中文）或非法续字节时解码会失败，此时工具不会强行替换，而是原样输出并提示不可还原。` : dead
- `tools/it/charset-detector.html` : `复制来的引号、省略号显示成「â€™」「â€¦」时，按字节还原为「’」「…」。` : dead
- `tools/it/charset-detector.html` : `粘贴「Ã©」→ 折算字节 C3 A9 → 按 UTF-8 解码得「é」；粘贴「â€™」→ 折算字节 E2 80 99 → 得「’」。若文本里已经是「�」（U+FFFD），说明原始字节在解码时已被丢弃，无法从文本还原。` : dead
- `tools/it/charset-detector.html` : `网页或接口返回的中文变成「Ã¤Â¸Â­Ã¦Â–Â‡」这类西文乱码时，还原真实文本。` : dead
- `tools/it/charset-detector.html` : `能识别 GBK、Big5 或 BOM 吗？` : dead
- `tools/it/charset-detector.html` : `还原双重编码乱码` : dead
- `tools/it/confidence-interval.html` : `CI = x̄ ± t α/2,n-1  × (s / √n)  (t 分布)` : dead
- `tools/it/confidence-interval.html` : `当 σ 未知且 n<30 时,使用 t 分布(自由度 df=n-1)。` : dead
- `tools/it/confidence-interval.html` : `自动(n≥30 用 z,n<30 用 t)` : dead
- `tools/it/cpp-cheatsheet.html` : `auto x = 1;       -- int ⏎ auto& r = v[0];    -- 引用 ⏎ const auto& cr = v[0]; ⏎ decltype(x) y = 2;` : dead
- `tools/it/cpp-cheatsheet.html` : `int add(int a, int b = 0) { return a + b; } ⏎ int add(int a) { return a + 1; }  -- 重载 ⏎ add(1, 2); add(1);` : dead
- `tools/it/cpp-cheatsheet.html` : `int x = 1; ⏎ int* p = &x; ⏎ *p = 2; ⏎ int* arr = new int[10]; ⏎ delete[] arr;  -- 必须释放` : dead
- `tools/it/cpp-cheatsheet.html` : `namespace app { ⏎   void run() {} ⏎ } ⏎ app::run(); ⏎ using namespace std;  -- 不推荐头文件中使用 ⏎ using std::string;` : dead
- `tools/it/cpp-cheatsheet.html` : `std::array<int, 3> a;  -- 固定数组 ⏎ std::deque<int> dq;       -- 双端队列 ⏎ std::list<int> l;         -- 链表 ⏎ std::stack<int> s;        -- 栈 ⏎ std::queue<int> q;      …(+38字)` : dead
- `tools/it/cpp-cheatsheet.html` : `std::vector<int> v = {1,2,3}; ⏎ for (int x : v) std::cout << x; ⏎ for (const auto& x : v) {}  -- 只读引用` : dead
- `tools/it/cpp-cheatsheet.html` : `template<typename T> ⏎ T add(T a, T b) { return a + b; } ⏎ add<int>(1, 2); ⏎ add(1.5, 2.5);  -- 推断 ⏎  ⏎ template<typename T> ⏎ class Stack { std::vector<T> v; }…(+1字)` : dead
- `tools/it/cpp-cheatsheet.html` : `共 24 项` : dead
- `tools/it/cron.html` : `每周执行` : dead
- `tools/it/cron.html` : `每天 每10分钟执行` : dead
- `tools/it/cron.html` : `每天 每15分钟执行` : dead
- `tools/it/cron.html` : `每天 每30分钟执行` : dead
- `tools/it/cron.html` : `每天 每5分钟执行` : dead
- `tools/it/cron.html` : `每天 每分钟执行` : dead
- `tools/it/cron.html` : `每天 每小时第15分执行` : dead
- `tools/it/cron.html` : `每天执行` : dead
- `tools/it/cron.html` : `每小时执行` : dead
- `tools/it/cron.html` : `每月执行` : dead
- `tools/it/crontab-generator.html` : `⚠️ 分钟 字段超出范围或格式无效（允许 0-59；支持 *、*/n、a-b、a,b）` : dead
- `tools/it/crontab-generator.html` : `⚠️ 小时 字段超出范围或格式无效（允许 0-23；支持 *、*/n、a-b、a,b）` : dead
- `tools/it/crontab-generator.html` : `⚠️ 日期 字段超出范围或格式无效（允许 1-31；支持 *、*/n、a-b、a,b）` : dead
- `tools/it/crontab-generator.html` : `⚠️ 星期 字段超出范围或格式无效（允许 0-7；支持 *、*/n、a-b、a,b）` : dead
- `tools/it/crontab-generator.html` : `⚠️ 月份 字段超出范围或格式无效（允许 1-12；支持 *、*/n、a-b、a,b）` : dead
- `tools/it/css-properties.html` : `共 133 个属性` : dead
- `tools/it/csv-to-html-table.html` : `粘贴 CSV 数据，自动解析（支持引号转义与换行），生成可直接使用的 HTML <table> 代码，右侧实时预览渲染效果。` : dead
- `tools/it/cuid-generator.html` : `c + base36(时间戳) + 计数器 + 指纹 + 随机数` : dead
- `tools/it/device-info.html` : `+8 (东8区)` : dead
- `tools/it/device-info.html` : `<span class="status-badge ok">在线</span>` : dead
- `tools/it/docker-cheatsheet.html` : `docker ps ⏎ docker ps -a ⏎ docker ps -q  -- 仅 ID` : dead
- `tools/it/docker-cheatsheet.html` : `docker rm web ⏎ docker rm -f $(docker ps -aq)  -- 删所有` : dead
- `tools/it/docker-cheatsheet.html` : `docker stop web ⏎ docker stop $(docker ps -q)  -- 停所有` : dead
- `tools/it/docker-cheatsheet.html` : `exec 形式 ["cmd","arg"]` : dead
- `tools/it/docker-cheatsheet.html` : `共 59 项` : dead
- `tools/it/emacs-cheatsheet.html` : `;; init.el 示例 ⏎ (setq make-backup-files nil) ⏎ (global-linum-mode 1) ⏎ (setq tab-width 4)` : dead
- `tools/it/emacs-cheatsheet.html` : `C-SPC  -- 设标记 ⏎ 移动光标选区 ⏎ M-w  -- 复制选区 ⏎ C-w  -- 剪切选区` : dead
- `tools/it/emacs-cheatsheet.html` : `C-a  行首 ⏎ C-e  行末` : dead
- `tools/it/emacs-cheatsheet.html` : `C-f  前进 ⏎ C-b  后退` : dead
- `tools/it/emacs-cheatsheet.html` : `C-k  -- 删除光标到行末 ⏎ 连续按删除多行` : dead
- `tools/it/emacs-cheatsheet.html` : `C-l  光标行居中 ⏎ C-u 0 C-l  行到顶部 ⏎ C-u - C-l  行到底部` : dead
- `tools/it/emacs-cheatsheet.html` : `C-n  下一行 ⏎ C-p  上一行` : dead
- `tools/it/emacs-cheatsheet.html` : `C-s word  向下搜 ⏎ C-r word  向上搜 ⏎ 多次 C-s 下一个` : dead
- `tools/it/emacs-cheatsheet.html` : `C-v  下一页 ⏎ M-v  上一页` : dead
- `tools/it/emacs-cheatsheet.html` : `C-w  剪切选区 ⏎ M-w  复制选区 ⏎ C-y  粘贴` : dead
- `tools/it/emacs-cheatsheet.html` : `C-x 0  关闭当前窗口 ⏎ C-x 1  只保留当前 ⏎ C-x 2  水平分割 ⏎ C-x 3  垂直分割` : dead
- `tools/it/emacs-cheatsheet.html` : `C-x 5 2  新 frame ⏎ C-x 5 0  关闭 frame` : dead
- `tools/it/emacs-cheatsheet.html` : `C-x b  -- 切换缓冲 ⏎ C-x b *scratch*  -- 切到 scratch` : dead
- `tools/it/emacs-cheatsheet.html` : `C-x u  -- 撤销 ⏎ C-/  -- 撤销 ⏎ C-g C-/  -- 重做` : dead
- `tools/it/emacs-cheatsheet.html` : `C-y  -- 粘贴 ⏎ M-y  -- 替换为更早的剪贴内容` : dead
- `tools/it/emacs-cheatsheet.html` : `M-% foo RET bar ⏎ y 替换 ⏎ n 跳过 ⏎ ! 全部替换` : dead
- `tools/it/emacs-cheatsheet.html` : `M-<  文件首 ⏎ M->  文件末` : dead
- `tools/it/emacs-cheatsheet.html` : `M-a  句首 ⏎ M-e  句末` : dead
- `tools/it/emacs-cheatsheet.html` : `M-d  删下个单词 ⏎ M-Backspace  删上个单词` : dead
- `tools/it/emacs-cheatsheet.html` : `M-f  下个单词 ⏎ M-b  上个单词` : dead
- `tools/it/emacs-cheatsheet.html` : `M-x 指令名  -- 执行指令 ⏎ M-x compile  -- 编译 ⏎ M-x shell  -- 打开 shell` : dead
- `tools/it/emacs-cheatsheet.html` : `emacs file.txt ⏎ emacs -nw file.txt  -- 终端模式 ⏎ emacsclient -t file.txt  -- 连接守护进程` : dead
- `tools/it/emoji-cheatsheet.html` : `一指 (index)` : dead
- `tools/it/emoji-cheatsheet.html` : `三明治 (sandwich)` : dead
- `tools/it/emoji-cheatsheet.html` : `不屑 (unamused)` : dead
- `tools/it/emoji-cheatsheet.html` : `不爽 (angry)` : dead
- `tools/it/emoji-cheatsheet.html` : `东京塔 (tower)` : dead
- `tools/it/emoji-cheatsheet.html` : `举手 (raise hands)` : dead
- `tools/it/emoji-cheatsheet.html` : `举手 (stop)` : dead
- `tools/it/emoji-cheatsheet.html` : `举重 (weight)` : dead
- `tools/it/emoji-cheatsheet.html` : `乒乓球 (ping pong)` : dead
- `tools/it/emoji-cheatsheet.html` : `乘 (multiply)` : dead
- `tools/it/emoji-cheatsheet.html` : `书呆子 (nerd)` : dead
- `tools/it/emoji-cheatsheet.html` : `云 (cloud)` : dead
- `tools/it/emoji-cheatsheet.html` : `云太阳 (cloud sun)` : dead
- `tools/it/emoji-cheatsheet.html` : `五指 (fingers)` : dead
- `tools/it/emoji-cheatsheet.html` : `交替 (alternation)` : dead
- `tools/it/emoji-cheatsheet.html` : `亲吻 (kissing)` : dead
- `tools/it/emoji-cheatsheet.html` : `仓鼠 (hamster)` : dead
- `tools/it/emoji-cheatsheet.html` : `企鹅 (penguin)` : dead
- `tools/it/emoji-cheatsheet.html` : `伞 (umbrella)` : dead
- `tools/it/emoji-cheatsheet.html` : `传真 (fax)` : dead
- `tools/it/emoji-cheatsheet.html` : `伪装 (disguise)` : dead
- `tools/it/emoji-cheatsheet.html` : `体育场 (stadium)` : dead
- `tools/it/emoji-cheatsheet.html` : `便利店 (store)` : dead
- `tools/it/emoji-cheatsheet.html` : `便当 (bento)` : dead
- `tools/it/emoji-cheatsheet.html` : `保龄球 (bowling)` : dead
- `tools/it/emoji-cheatsheet.html` : `信用卡 (card)` : dead
- `tools/it/emoji-cheatsheet.html` : `倒脸 (upside down)` : dead
- `tools/it/emoji-cheatsheet.html` : `停止 (stop)` : dead
- `tools/it/emoji-cheatsheet.html` : `傻眼 (zany)` : dead
- `tools/it/emoji-cheatsheet.html` : `光盘 (disc)` : dead
- `tools/it/emoji-cheatsheet.html` : `克尔白 (kaaba)` : dead
- `tools/it/emoji-cheatsheet.html` : `兑换 (exchange)` : dead
- `tools/it/emoji-cheatsheet.html` : `兔子 (rabbit)` : dead
- `tools/it/emoji-cheatsheet.html` : `八角 (eight pointed)` : dead
- `tools/it/emoji-cheatsheet.html` : `八角星 (eight star)` : dead
- `tools/it/emoji-cheatsheet.html` : `公交车 (bus)` : dead
- `tools/it/emoji-cheatsheet.html` : `公交车前 (bus)` : dead
- `tools/it/emoji-cheatsheet.html` : `六芒星 (six pointed)` : dead
- `tools/it/emoji-cheatsheet.html` : `共 551 个 emoji` : dead
- `tools/it/emoji-cheatsheet.html` : `关机 (phone off)` : dead
- `tools/it/emoji-cheatsheet.html` : `写字 (write)` : dead
- `tools/it/emoji-cheatsheet.html` : `冥想 (meditation)` : dead
- `tools/it/emoji-cheatsheet.html` : `冰壶 (curling)` : dead
- `tools/it/emoji-cheatsheet.html` : `冰淇淋 (ice cream)` : dead
- `tools/it/emoji-cheatsheet.html` : `冰球 (hockey)` : dead
- `tools/it/emoji-cheatsheet.html` : `冲浪 (surf)` : dead
- `tools/it/emoji-cheatsheet.html` : `冷脸 (cold)` : dead
- `tools/it/emoji-cheatsheet.html` : `减 (minus)` : dead
- `tools/it/emoji-cheatsheet.html` : `出租车 (taxi)` : dead
- `tools/it/emoji-cheatsheet.html` : `出租车前 (taxi)` : dead
- `tools/it/emoji-cheatsheet.html` : `击剑 (fencing)` : dead
- `tools/it/emoji-cheatsheet.html` : `划船 (row)` : dead
- `tools/it/emoji-cheatsheet.html` : `割 (discount)` : dead
- `tools/it/emoji-cheatsheet.html` : `办公楼 (office)` : dead
- `tools/it/emoji-cheatsheet.html` : `加 (plus)` : dead
- `tools/it/emoji-cheatsheet.html` : `加油 (fuel)` : dead
- `tools/it/emoji-cheatsheet.html` : `勾 (check mark)` : dead
- `tools/it/emoji-cheatsheet.html` : `勾选 (check)` : dead
- `tools/it/emoji-cheatsheet.html` : `勾选框 (checkbox)` : dead
- `tools/it/emoji-cheatsheet.html` : `医院 (hospital)` : dead
- `tools/it/emoji-cheatsheet.html` : `十字架 (cross)` : dead
- `tools/it/emoji-cheatsheet.html` : `半挂车 (lorry)` : dead
- `tools/it/emoji-cheatsheet.html` : `华夫饼 (waffle)` : dead
- `tools/it/emoji-cheatsheet.html` : `单板滑雪 (snowboard)` : dead
- `tools/it/emoji-cheatsheet.html` : `单片眼镜 (monocle)` : dead
- `tools/it/emoji-cheatsheet.html` : `单眼吐舌 (wink tongue)` : dead
- `tools/it/emoji-cheatsheet.html` : `单轨列车 (monorail)` : dead
- `tools/it/emoji-cheatsheet.html` : `卡车 (truck)` : dead
- `tools/it/emoji-cheatsheet.html` : `卫星天线 (satellite)` : dead
- `tools/it/emoji-cheatsheet.html` : `印度庙 (temple)` : dead
- `tools/it/emoji-cheatsheet.html` : `卷饼 (burrito)` : dead
- `tools/it/emoji-cheatsheet.html` : `原子 (atom)` : dead
- `tools/it/emoji-cheatsheet.html` : `叉 (cross mark)` : dead
- `tools/it/emoji-cheatsheet.html` : `叉 (cross)` : dead
- `tools/it/emoji-cheatsheet.html` : `叉框 (cross mark box)` : dead
- `tools/it/emoji-cheatsheet.html` : `双叹 (bang bang)` : dead
- `tools/it/emoji-cheatsheet.html` : `双子 (gemini)` : dead
- `tools/it/emoji-cheatsheet.html` : `双峰驼 (camel2)` : dead
- `tools/it/emoji-cheatsheet.html` : `双心 (two hearts)` : dead
- `tools/it/emoji-cheatsheet.html` : `双鱼 (pisces)` : dead
- `tools/it/emoji-cheatsheet.html` : `反派 (villain)` : dead
- `tools/it/emoji-cheatsheet.html` : `变心 (growing)` : dead
- `tools/it/emoji-cheatsheet.html` : `口罩 (mask)` : dead
- `tools/it/emoji-cheatsheet.html` : `古典建筑 (classical)` : dead
- `tools/it/emoji-cheatsheet.html` : `台式机 (desktop)` : dead
- `tools/it/emoji-cheatsheet.html` : `台球 (pool)` : dead
- `tools/it/emoji-cheatsheet.html` : `右拳 (right fist)` : dead
- `tools/it/emoji-cheatsheet.html` : `叹问 (interrobang)` : dead
- `tools/it/emoji-cheatsheet.html` : `合十 (pray)` : dead
- `tools/it/emoji-cheatsheet.html` : `名牌 (badge)` : dead
- `tools/it/emoji-cheatsheet.html` : `吐舌 (tongue)` : dead
- `tools/it/emoji-cheatsheet.html` : `吐舌眨眼 (tongue wink)` : dead
- `tools/it/emoji-cheatsheet.html` : `吓到尖叫 (scream)` : dead
- `tools/it/emoji-cheatsheet.html` : `吸管杯 (cup)` : dead
- `tools/it/emoji-cheatsheet.html` : `呕吐 (vomit)` : dead
- `tools/it/emoji-cheatsheet.html` : `和平 (peace)` : dead
- `tools/it/emoji-cheatsheet.html` : `咖啡 (coffee)` : dead
- `tools/it/emoji-cheatsheet.html` : `咖喱饭 (curry)` : dead
- `tools/it/emoji-cheatsheet.html` : `哈密瓜 (melon)` : dead
- `tools/it/emoji-cheatsheet.html` : `哭 (cry)` : dead
- `tools/it/emoji-cheatsheet.html` : `啤酒 (beer)` : dead
- `tools/it/emoji-cheatsheet.html` : `喷泉 (fountain)` : dead
- `tools/it/emoji-cheatsheet.html` : `困 (sleepy)` : dead
- `tools/it/emoji-cheatsheet.html` : `圆圈 (circle)` : dead
- `tools/it/emoji-cheatsheet.html` : `土豆 (potato)` : dead
- `tools/it/emoji-cheatsheet.html` : `地图 (map)` : dead
- `tools/it/emoji-cheatsheet.html` : `垒球 (softball)` : dead
- `tools/it/emoji-cheatsheet.html` : `培根 (bacon)` : dead
- `tools/it/emoji-cheatsheet.html` : `墨镜 (cool)` : dead
- `tools/it/emoji-cheatsheet.html` : `处女 (virgo)` : dead
- `tools/it/emoji-cheatsheet.html` : `大卫星 (star of david)` : dead
- `tools/it/emoji-cheatsheet.html` : `大哭 (sob)` : dead
- `tools/it/emoji-cheatsheet.html` : `大猩猩 (gorilla)` : dead
- `tools/it/emoji-cheatsheet.html` : `大笑 (smiley)` : dead
- `tools/it/emoji-cheatsheet.html` : `大蒜 (garlic)` : dead
- `tools/it/emoji-cheatsheet.html` : `大象 (elephant)` : dead
- `tools/it/emoji-cheatsheet.html` : `天使 (innocent)` : dead
- `tools/it/emoji-cheatsheet.html` : `天秤 (libra)` : dead
- `tools/it/emoji-cheatsheet.html` : `天蝎 (scorpio)` : dead
- `tools/it/emoji-cheatsheet.html` : `太阳 (sun)` : dead
- `tools/it/emoji-cheatsheet.html` : `太阳云 (sun cloud)` : dead
- `tools/it/emoji-cheatsheet.html` : `失望 (disappointed)` : dead
- `tools/it/emoji-cheatsheet.html` : `夹子 (clamp)` : dead
- `tools/it/emoji-cheatsheet.html` : `奥姆 (om)` : dead
- `tools/it/emoji-cheatsheet.html` : `奶茶 (milk tea)` : dead
- `tools/it/emoji-cheatsheet.html` : `奶酪 (cheese)` : dead
- `tools/it/emoji-cheatsheet.html` : `好崇拜 (star struck)` : dead
- `tools/it/emoji-cheatsheet.html` : `威士忌 (whisky)` : dead
- `tools/it/emoji-cheatsheet.html` : `婚礼 (wedding)` : dead
- `tools/it/emoji-cheatsheet.html` : `学校 (school)` : dead
- `tools/it/emoji-cheatsheet.html` : `学霸 (nerd)` : dead
- `tools/it/emoji-cheatsheet.html` : `安心 (relieved)` : dead
- `tools/it/emoji-cheatsheet.html` : `定时器 (timer)` : dead
- `tools/it/emoji-cheatsheet.html` : `客轮 (ferry)` : dead
- `tools/it/emoji-cheatsheet.html` : `害怕 (fearful)` : dead
- `tools/it/emoji-cheatsheet.html` : `害羞 (blush)` : dead
- `tools/it/emoji-cheatsheet.html` : `富士山 (fuji)` : dead
- `tools/it/emoji-cheatsheet.html` : `对拳 (fist bump)` : dead
- `tools/it/emoji-cheatsheet.html` : `寻呼机 (pager)` : dead
- `tools/it/emoji-cheatsheet.html` : `寿司 (sushi)` : dead
- `tools/it/emoji-cheatsheet.html` : `射手 (sagittarius)` : dead
- `tools/it/emoji-cheatsheet.html` : `小型飞机 (small plane)` : dead
- `tools/it/emoji-cheatsheet.html` : `尴尬 (grimace)` : dead
- `tools/it/emoji-cheatsheet.html` : `山 (mountain)` : dead
- `tools/it/emoji-cheatsheet.html` : `山地缆车 (mountain)` : dead
- `tools/it/emoji-cheatsheet.html` : `山地车 (mountain bike)` : dead
- `tools/it/emoji-cheatsheet.html` : `山地铁路 (railway)` : dead
- `tools/it/emoji-cheatsheet.html` : `工厂 (factory)` : dead
- `tools/it/emoji-cheatsheet.html` : `左拳 (left fist)` : dead
- `tools/it/emoji-cheatsheet.html` : `巧克力 (chocolate)` : dead
- `tools/it/emoji-cheatsheet.html` : `巨蟹 (cancer)` : dead
- `tools/it/emoji-cheatsheet.html` : `帆船 (sailboat)` : dead
- `tools/it/emoji-cheatsheet.html` : `帐篷 (tent)` : dead
- `tools/it/emoji-cheatsheet.html` : `带花园的房子 (garden)` : dead
- `tools/it/emoji-cheatsheet.html` : `庆祝 (party)` : dead
- `tools/it/emoji-cheatsheet.html` : `废弃房子 (abandoned)` : dead
- `tools/it/emoji-cheatsheet.html` : `座机 (phone)` : dead
- `tools/it/emoji-cheatsheet.html` : `座钟 (clock)` : dead
- `tools/it/emoji-cheatsheet.html` : `开心 (smile)` : dead
- `tools/it/emoji-cheatsheet.html` : `弓箭 (bow)` : dead
- `tools/it/emoji-cheatsheet.html` : `张开手 (hand)` : dead
- `tools/it/emoji-cheatsheet.html` : `录像带 (vhs)` : dead
- `tools/it/emoji-cheatsheet.html` : `录音棚 (studio)` : dead
- `tools/it/emoji-cheatsheet.html` : `彗星 (comet)` : dead
- `tools/it/emoji-cheatsheet.html` : `彩虹 (rainbow)` : dead
- `tools/it/emoji-cheatsheet.html` : `得意 (smirk)` : dead
- `tools/it/emoji-cheatsheet.html` : `微笑 (slight smile)` : dead
- `tools/it/emoji-cheatsheet.html` : `心叹 (heart exclamation)` : dead
- `tools/it/emoji-cheatsheet.html` : `心形 (heart)` : dead
- `tools/it/emoji-cheatsheet.html` : `心碎 (broken heart)` : dead
- `tools/it/emoji-cheatsheet.html` : `心跳 (beating)` : dead
- `tools/it/emoji-cheatsheet.html` : `快艇 (speedboat)` : dead
- `tools/it/emoji-cheatsheet.html` : `怒 (anger)` : dead
- `tools/it/emoji-cheatsheet.html` : `恳求 (pleading)` : dead
- `tools/it/emoji-cheatsheet.html` : `恶心 (nauseated)` : dead
- `tools/it/emoji-cheatsheet.html` : `悬挂式列车 (suspension)` : dead
- `tools/it/emoji-cheatsheet.html` : `情人酒店 (love hotel)` : dead
- `tools/it/emoji-cheatsheet.html` : `意面 (spaghetti)` : dead
- `tools/it/emoji-cheatsheet.html` : `感叹 (exclamation)` : dead
- `tools/it/emoji-cheatsheet.html` : `愤怒 (angry)` : dead
- `tools/it/emoji-cheatsheet.html` : `房子 (house)` : dead
- `tools/it/emoji-cheatsheet.html` : `房屋群 (houses)` : dead
- `tools/it/emoji-cheatsheet.html` : `手机 (phone)` : dead
- `tools/it/emoji-cheatsheet.html` : `手机响 (phone)` : dead
- `tools/it/emoji-cheatsheet.html` : `手球 (handball)` : dead
- `tools/it/emoji-cheatsheet.html` : `手电筒 (flashlight)` : dead
- `tools/it/emoji-cheatsheet.html` : `手背 (raised back)` : dead
- `tools/it/emoji-cheatsheet.html` : `手表 (watch)` : dead
- `tools/it/emoji-cheatsheet.html` : `打印机 (printer)` : dead
- `tools/it/emoji-cheatsheet.html` : `打电话 (call)` : dead
- `tools/it/emoji-cheatsheet.html` : `投影仪 (projector)` : dead
- `tools/it/emoji-cheatsheet.html` : `披萨 (pizza)` : dead
- `tools/it/emoji-cheatsheet.html` : `拖拉机 (tractor)` : dead
- `tools/it/emoji-cheatsheet.html` : `拳击 (boxing)` : dead
- `tools/it/emoji-cheatsheet.html` : `拳头 (fist)` : dead
- `tools/it/emoji-cheatsheet.html` : `指上 (point up)` : dead
- `tools/it/emoji-cheatsheet.html` : `指下 (point down)` : dead
- `tools/it/emoji-cheatsheet.html` : `指南针 (compass)` : dead
- `tools/it/emoji-cheatsheet.html` : `指右 (point right)` : dead
- `tools/it/emoji-cheatsheet.html` : `指左 (point left)` : dead
- `tools/it/emoji-cheatsheet.html` : `挑眉 (raised eyebrow)` : dead
- `tools/it/emoji-cheatsheet.html` : `挥手 (wave)` : dead
- `tools/it/emoji-cheatsheet.html` : `排球 (volleyball)` : dead
- `tools/it/emoji-cheatsheet.html` : `插头 (plug)` : dead
- `tools/it/emoji-cheatsheet.html` : `握手 (handshake)` : dead
- `tools/it/emoji-cheatsheet.html` : `握拳 (fist)` : dead
- `tools/it/emoji-cheatsheet.html` : `摄像机 (video)` : dead
- `tools/it/emoji-cheatsheet.html` : `摇杆 (joystick)` : dead
- `tools/it/emoji-cheatsheet.html` : `摇滚 (rock)` : dead
- `tools/it/emoji-cheatsheet.html` : `摔跤 (wrestle)` : dead
- `tools/it/emoji-cheatsheet.html` : `摩天轮 (ferris)` : dead
- `tools/it/emoji-cheatsheet.html` : `摩托 (scooter)` : dead
- `tools/it/emoji-cheatsheet.html` : `摩托车 (motorcycle)` : dead
- `tools/it/emoji-cheatsheet.html` : `摩羯 (capricorn)` : dead
- `tools/it/emoji-cheatsheet.html` : `攀岩 (climb)` : dead
- `tools/it/emoji-cheatsheet.html` : `收音机 (radio)` : dead
- `tools/it/emoji-cheatsheet.html` : `救护车 (ambulance)` : dead
- `tools/it/emoji-cheatsheet.html` : `教堂 (church)` : dead
- `tools/it/emoji-cheatsheet.html` : `斑马 (zebra)` : dead
- `tools/it/emoji-cheatsheet.html` : `斜眼笑 (laughing)` : dead
- `tools/it/emoji-cheatsheet.html` : `施工 (construction)` : dead
- `tools/it/emoji-cheatsheet.html` : `旋转心 (revolving)` : dead
- `tools/it/emoji-cheatsheet.html` : `旋转木马 (carousel)` : dead
- `tools/it/emoji-cheatsheet.html` : `旋钮 (knob)` : dead
- `tools/it/emoji-cheatsheet.html` : `无 (free)` : dead
- `tools/it/emoji-cheatsheet.html` : `无穷 (infinity)` : dead
- `tools/it/emoji-cheatsheet.html` : `日元 (yen)` : dead
- `tools/it/emoji-cheatsheet.html` : `日文可 (accept)` : dead
- `tools/it/emoji-cheatsheet.html` : `日本城堡 (castle)` : dead
- `tools/it/emoji-cheatsheet.html` : `日本邮局 (post)` : dead
- `tools/it/emoji-cheatsheet.html` : `星 (star)` : dead
- `tools/it/emoji-cheatsheet.html` : `星月 (star and crescent)` : dead
- `tools/it/emoji-cheatsheet.html` : `晕 (dizzy)` : dead
- `tools/it/emoji-cheatsheet.html` : `曲棍球 (field hockey)` : dead
- `tools/it/emoji-cheatsheet.html` : `有 (not free)` : dead
- `tools/it/emoji-cheatsheet.html` : `有轨电车 (tram)` : dead
- `tools/it/emoji-cheatsheet.html` : `未成年禁 (minor)` : dead
- `tools/it/emoji-cheatsheet.html` : `松口气 (sigh)` : dead
- `tools/it/emoji-cheatsheet.html` : `松饼 (pancake)` : dead
- `tools/it/emoji-cheatsheet.html` : `板球 (cricket)` : dead
- `tools/it/emoji-cheatsheet.html` : `柠檬 (lemon)` : dead
- `tools/it/emoji-cheatsheet.html` : `桃子 (peach)` : dead
- `tools/it/emoji-cheatsheet.html` : `梨 (pear)` : dead
- `tools/it/emoji-cheatsheet.html` : `棒球 (baseball)` : dead
- `tools/it/emoji-cheatsheet.html` : `棕心 (brown heart)` : dead
- `tools/it/emoji-cheatsheet.html` : `椒盐卷饼 (pretzel)` : dead
- `tools/it/emoji-cheatsheet.html` : `椰子 (coconut)` : dead
- `tools/it/emoji-cheatsheet.html` : `横向红绿灯 (traffic)` : dead
- `tools/it/emoji-cheatsheet.html` : `樱桃 (cherries)` : dead
- `tools/it/emoji-cheatsheet.html` : `橄榄球 (football)` : dead
- `tools/it/emoji-cheatsheet.html` : `橘子 (orange)` : dead
- `tools/it/emoji-cheatsheet.html` : `橙心 (orange heart)` : dead
- `tools/it/emoji-cheatsheet.html` : `欧元 (euro)` : dead
- `tools/it/emoji-cheatsheet.html` : `欧洲城堡 (castle)` : dead
- `tools/it/emoji-cheatsheet.html` : `武术 (martial arts)` : dead
- `tools/it/emoji-cheatsheet.html` : `水滴 (droplet)` : dead
- `tools/it/emoji-cheatsheet.html` : `水球 (water polo)` : dead
- `tools/it/emoji-cheatsheet.html` : `水瓶 (aquarius)` : dead
- `tools/it/emoji-cheatsheet.html` : `汉堡 (burger)` : dead
- `tools/it/emoji-cheatsheet.html` : `汗 (sweat)` : dead
- `tools/it/emoji-cheatsheet.html` : `汽车 (car)` : dead
- `tools/it/emoji-cheatsheet.html` : `汽车前 (car)` : dead
- `tools/it/emoji-cheatsheet.html` : `沉思 (pensive)` : dead
- `tools/it/emoji-cheatsheet.html` : `沙漏完 (hourglass)` : dead
- `tools/it/emoji-cheatsheet.html` : `沙漏流 (hourglass)` : dead
- `tools/it/emoji-cheatsheet.html` : `沙漠 (desert)` : dead
- `tools/it/emoji-cheatsheet.html` : `河豚 (blowfish)` : dead
- `tools/it/emoji-cheatsheet.html` : `河马 (hippo)` : dead
- `tools/it/emoji-cheatsheet.html` : `油桶 (oil)` : dead
- `tools/it/emoji-cheatsheet.html` : `油灯 (lamp)` : dead
- `tools/it/emoji-cheatsheet.html` : `法棍 (baguette)` : dead
- `tools/it/emoji-cheatsheet.html` : `法轮 (wheel)` : dead
- `tools/it/emoji-cheatsheet.html` : `洋葱 (onion)` : dead
- `tools/it/emoji-cheatsheet.html` : `派对 (party)` : dead
- `tools/it/emoji-cheatsheet.html` : `流口水 (drool)` : dead
- `tools/it/emoji-cheatsheet.html` : `海滩 (beach)` : dead
- `tools/it/emoji-cheatsheet.html` : `海豚 (dolphin)` : dead
- `tools/it/emoji-cheatsheet.html` : `消防车 (fire engine)` : dead
- `tools/it/emoji-cheatsheet.html` : `清真寺 (mosque)` : dead
- `tools/it/emoji-cheatsheet.html` : `渡轮 (ferry)` : dead
- `tools/it/emoji-cheatsheet.html` : `温度计 (thermometer)` : dead
- `tools/it/emoji-cheatsheet.html` : `温泉 (hotspring)` : dead
- `tools/it/emoji-cheatsheet.html` : `游泳 (swim)` : dead
- `tools/it/emoji-cheatsheet.html` : `游艇 (yacht)` : dead
- `tools/it/emoji-cheatsheet.html` : `滑冰 (skate)` : dead
- `tools/it/emoji-cheatsheet.html` : `滑板车 (scooter)` : dead
- `tools/it/emoji-cheatsheet.html` : `滑雪 (ski)` : dead
- `tools/it/emoji-cheatsheet.html` : `滑雪者 (skier)` : dead
- `tools/it/emoji-cheatsheet.html` : `火 (fire)` : dead
- `tools/it/emoji-cheatsheet.html` : `火山 (volcano)` : dead
- `tools/it/emoji-cheatsheet.html` : `火心 (heart fire)` : dead
- `tools/it/emoji-cheatsheet.html` : `火箭 (rocket)` : dead
- `tools/it/emoji-cheatsheet.html` : `火车 (train)` : dead
- `tools/it/emoji-cheatsheet.html` : `火车站 (station)` : dead
- `tools/it/emoji-cheatsheet.html` : `灭火器 (extinguisher)` : dead
- `tools/it/emoji-cheatsheet.html` : `灯泡 (bulb)` : dead
- `tools/it/emoji-cheatsheet.html` : `烤红薯 (sweet potato)` : dead
- `tools/it/emoji-cheatsheet.html` : `热带鱼 (fish)` : dead
- `tools/it/emoji-cheatsheet.html` : `热狗 (hotdog)` : dead
- `tools/it/emoji-cheatsheet.html` : `热脸 (hot)` : dead
- `tools/it/emoji-cheatsheet.html` : `焦虑 (anxious)` : dead
- `tools/it/emoji-cheatsheet.html` : `煎蛋 (egg)` : dead
- `tools/it/emoji-cheatsheet.html` : `熊 (bear)` : dead
- `tools/it/emoji-cheatsheet.html` : `熊猫 (panda)` : dead
- `tools/it/emoji-cheatsheet.html` : `爆炸 (boom)` : dead
- `tools/it/emoji-cheatsheet.html` : `爆炸头 (mind blown)` : dead
- `tools/it/emoji-cheatsheet.html` : `爆粗口 (swear)` : dead
- `tools/it/emoji-cheatsheet.html` : `爱你 (love you)` : dead
- `tools/it/emoji-cheatsheet.html` : `爱心眼 (smiling hearts)` : dead
- `tools/it/emoji-cheatsheet.html` : `牛 (cow)` : dead
- `tools/it/emoji-cheatsheet.html` : `牛仔 (cowboy)` : dead
- `tools/it/emoji-cheatsheet.html` : `牛奶 (milk)` : dead
- `tools/it/emoji-cheatsheet.html` : `牛排 (steak)` : dead
- `tools/it/emoji-cheatsheet.html` : `牛油果 (avocado)` : dead
- `tools/it/emoji-cheatsheet.html` : `牛角包 (croissant)` : dead
- `tools/it/emoji-cheatsheet.html` : `犀牛 (rhino)` : dead
- `tools/it/emoji-cheatsheet.html` : `犹太教堂 (synagogue)` : dead
- `tools/it/emoji-cheatsheet.html` : `狐狸 (fox)` : dead
- `tools/it/emoji-cheatsheet.html` : `狗 (dog)` : dead
- `tools/it/emoji-cheatsheet.html` : `独角兽 (unicorn)` : dead
- `tools/it/emoji-cheatsheet.html` : `狮子 (leo)` : dead
- `tools/it/emoji-cheatsheet.html` : `狮子 (lion)` : dead
- `tools/it/emoji-cheatsheet.html` : `狼 (wolf)` : dead
- `tools/it/emoji-cheatsheet.html` : `猕猴桃 (kiwi)` : dead
- `tools/it/emoji-cheatsheet.html` : `猪 (pig)` : dead
- `tools/it/emoji-cheatsheet.html` : `猫 (cat)` : dead
- `tools/it/emoji-cheatsheet.html` : `猫头鹰 (owl)` : dead
- `tools/it/emoji-cheatsheet.html` : `猴子 (monkey)` : dead
- `tools/it/emoji-cheatsheet.html` : `玉米 (corn)` : dead
- `tools/it/emoji-cheatsheet.html` : `玉米卷 (taco)` : dead
- `tools/it/emoji-cheatsheet.html` : `球门 (goal)` : dead
- `tools/it/emoji-cheatsheet.html` : `瓢虫 (ladybug)` : dead
- `tools/it/emoji-cheatsheet.html` : `甜甜圈 (donut)` : dead
- `tools/it/emoji-cheatsheet.html` : `生化 (biohazard)` : dead
- `tools/it/emoji-cheatsheet.html` : `生日蛋糕 (birthday)` : dead
- `tools/it/emoji-cheatsheet.html` : `申 (apply)` : dead
- `tools/it/emoji-cheatsheet.html` : `电影机 (movie)` : dead
- `tools/it/emoji-cheatsheet.html` : `电池 (battery)` : dead
- `tools/it/emoji-cheatsheet.html` : `电脑 (computer)` : dead
- `tools/it/emoji-cheatsheet.html` : `电视 (tv)` : dead
- `tools/it/emoji-cheatsheet.html` : `电话 (phone)` : dead
- `tools/it/emoji-cheatsheet.html` : `电车 (tram)` : dead
- `tools/it/emoji-cheatsheet.html` : `电车 (trolley)` : dead
- `tools/it/emoji-cheatsheet.html` : `番茄 (tomato)` : dead
- `tools/it/emoji-cheatsheet.html` : `白叹 (white exclamation)` : dead
- `tools/it/emoji-cheatsheet.html` : `白心 (white heart)` : dead
- `tools/it/emoji-cheatsheet.html` : `白羊 (aries)` : dead
- `tools/it/emoji-cheatsheet.html` : `白问 (white question)` : dead
- `tools/it/emoji-cheatsheet.html` : `百货公司 (mall)` : dead
- `tools/it/emoji-cheatsheet.html` : `直升机 (helicopter)` : dead
- `tools/it/emoji-cheatsheet.html` : `相机 (camera)` : dead
- `tools/it/emoji-cheatsheet.html` : `眨眼 (wink)` : dead
- `tools/it/emoji-cheatsheet.html` : `睁眼亲 (kissing smiling)` : dead
- `tools/it/emoji-cheatsheet.html` : `睡觉 (sleep)` : dead
- `tools/it/emoji-cheatsheet.html` : `碰杯 (beers)` : dead
- `tools/it/emoji-cheatsheet.html` : `碰杯 (clink)` : dead
- `tools/it/emoji-cheatsheet.html` : `礼心 (ribbon)` : dead
- `tools/it/emoji-cheatsheet.html` : `祈愿 (fingers crossed)` : dead
- `tools/it/emoji-cheatsheet.html` : `禁手机 (no phone)` : dead
- `tools/it/emoji-cheatsheet.html` : `禁止 (forbidden)` : dead
- `tools/it/emoji-cheatsheet.html` : `禁止 (no entry)` : dead
- `tools/it/emoji-cheatsheet.html` : `禁止乱扔 (no litter)` : dead
- `tools/it/emoji-cheatsheet.html` : `禁止行人 (no pedestrian)` : dead
- `tools/it/emoji-cheatsheet.html` : `禁烟 (no smoking)` : dead
- `tools/it/emoji-cheatsheet.html` : `禁自行车 (no bike)` : dead
- `tools/it/emoji-cheatsheet.html` : `禁饮水 (non potable)` : dead
- `tools/it/emoji-cheatsheet.html` : `秒表 (stopwatch)` : dead
- `tools/it/emoji-cheatsheet.html` : `章鱼 (octopus)` : dead
- `tools/it/emoji-cheatsheet.html` : `笑哭 (rofl)` : dead
- `tools/it/emoji-cheatsheet.html` : `笑哭了 (joy)` : dead
- `tools/it/emoji-cheatsheet.html` : `笑脸 (grinning)` : dead
- `tools/it/emoji-cheatsheet.html` : `等号 (equal)` : dead
- `tools/it/emoji-cheatsheet.html` : `箭心 (arrow)` : dead
- `tools/it/emoji-cheatsheet.html` : `篮球 (basketball)` : dead
- `tools/it/emoji-cheatsheet.html` : `米饭 (rice)` : dead
- `tools/it/emoji-cheatsheet.html` : `紫心 (purple heart)` : dead
- `tools/it/emoji-cheatsheet.html` : `红心 (heart)` : dead
- `tools/it/emoji-cheatsheet.html` : `红毛猩猩 (orangutan)` : dead
- `tools/it/emoji-cheatsheet.html` : `红绿灯 (traffic)` : dead
- `tools/it/emoji-cheatsheet.html` : `红苹果 (apple)` : dead
- `tools/it/emoji-cheatsheet.html` : `红酒 (wine)` : dead
- `tools/it/emoji-cheatsheet.html` : `绷带 (bandage)` : dead
- `tools/it/emoji-cheatsheet.html` : `绷带心 (heart bandage)` : dead
- `tools/it/emoji-cheatsheet.html` : `绿心 (green heart)` : dead
- `tools/it/emoji-cheatsheet.html` : `缆车 (aerial)` : dead
- `tools/it/emoji-cheatsheet.html` : `网球 (tennis)` : dead
- `tools/it/emoji-cheatsheet.html` : `美元 (dollar)` : dead
- `tools/it/emoji-cheatsheet.html` : `美元符 (dollar)` : dead
- `tools/it/emoji-cheatsheet.html` : `羽毛球 (badminton)` : dead
- `tools/it/emoji-cheatsheet.html` : `翻白眼 (roll eyes)` : dead
- `tools/it/emoji-cheatsheet.html` : `翻筋斗 (cartwheel)` : dead
- `tools/it/emoji-cheatsheet.html` : `老虎 (tiger)` : dead
- `tools/it/emoji-cheatsheet.html` : `老虎机 (slot)` : dead
- `tools/it/emoji-cheatsheet.html` : `老鼠 (mouse)` : dead
- `tools/it/emoji-cheatsheet.html` : `考拉 (koala)` : dead
- `tools/it/emoji-cheatsheet.html` : `肉骨 (meat)` : dead
- `tools/it/emoji-cheatsheet.html` : `肌肉 (muscle)` : dead
- `tools/it/emoji-cheatsheet.html` : `胜利 (victory)` : dead
- `tools/it/emoji-cheatsheet.html` : `胡萝卜 (carrot)` : dead
- `tools/it/emoji-cheatsheet.html` : `胶片 (film)` : dead
- `tools/it/emoji-cheatsheet.html` : `自由女神 (statue)` : dead
- `tools/it/emoji-cheatsheet.html` : `自行车 (bike)` : dead
- `tools/it/emoji-cheatsheet.html` : `芒果 (mango)` : dead
- `tools/it/emoji-cheatsheet.html` : `花痴 (heart eyes)` : dead
- `tools/it/emoji-cheatsheet.html` : `苦笑 (sweat smile)` : dead
- `tools/it/emoji-cheatsheet.html` : `英式橄榄 (rugby)` : dead
- `tools/it/emoji-cheatsheet.html` : `英镑 (pound)` : dead
- `tools/it/emoji-cheatsheet.html` : `茄子 (eggplant)` : dead
- `tools/it/emoji-cheatsheet.html` : `茶 (tea)` : dead
- `tools/it/emoji-cheatsheet.html` : `草莓 (strawberry)` : dead
- `tools/it/emoji-cheatsheet.html` : `荒岛 (island)` : dead
- `tools/it/emoji-cheatsheet.html` : `菠萝 (pineapple)` : dead
- `tools/it/emoji-cheatsheet.html` : `营 (business)` : dead
- `tools/it/emoji-cheatsheet.html` : `葡萄 (grapes)` : dead
- `tools/it/emoji-cheatsheet.html` : `蒸汽火车 (locomotive)` : dead
- `tools/it/emoji-cheatsheet.html` : `蓝心 (blue heart)` : dead
- `tools/it/emoji-cheatsheet.html` : `薯条 (fries)` : dead
- `tools/it/emoji-cheatsheet.html` : `虎 (tiger)` : dead
- `tools/it/emoji-cheatsheet.html` : `虫子 (bug)` : dead
- `tools/it/emoji-cheatsheet.html` : `虾 (shrimp)` : dead
- `tools/it/emoji-cheatsheet.html` : `蚂蚁 (ant)` : dead
- `tools/it/emoji-cheatsheet.html` : `蛋糕 (cake)` : dead
- `tools/it/emoji-cheatsheet.html` : `蜗牛 (snail)` : dead
- `tools/it/emoji-cheatsheet.html` : `蜘蛛 (spider)` : dead
- `tools/it/emoji-cheatsheet.html` : `蜜蜂 (bee)` : dead
- `tools/it/emoji-cheatsheet.html` : `蜡烛 (candle)` : dead
- `tools/it/emoji-cheatsheet.html` : `蝙蝠 (bat)` : dead
- `tools/it/emoji-cheatsheet.html` : `蝴蝶 (butterfly)` : dead
- `tools/it/emoji-cheatsheet.html` : `螃蟹 (crab)` : dead
- `tools/it/emoji-cheatsheet.html` : `蟋蟀 (cricket)` : dead
- `tools/it/emoji-cheatsheet.html` : `袋鼠 (kangaroo)` : dead
- `tools/it/emoji-cheatsheet.html` : `西兰花 (broccoli)` : dead
- `tools/it/emoji-cheatsheet.html` : `西瓜 (watermelon)` : dead
- `tools/it/emoji-cheatsheet.html` : `警灯 (light)` : dead
- `tools/it/emoji-cheatsheet.html` : `警车 (police)` : dead
- `tools/it/emoji-cheatsheet.html` : `警车前 (police)` : dead
- `tools/it/emoji-cheatsheet.html` : `说谎 (liar)` : dead
- `tools/it/emoji-cheatsheet.html` : `调音台 (level)` : dead
- `tools/it/emoji-cheatsheet.html` : `豹 (leopard)` : dead
- `tools/it/emoji-cheatsheet.html` : `赛车 (race car)` : dead
- `tools/it/emoji-cheatsheet.html` : `赛马 (horse)` : dead
- `tools/it/emoji-cheatsheet.html` : `赞 (thumbs up)` : dead
- `tools/it/emoji-cheatsheet.html` : `起飞 (takeoff)` : dead
- `tools/it/emoji-cheatsheet.html` : `足球 (soccer)` : dead
- `tools/it/emoji-cheatsheet.html` : `跑步 (running)` : dead
- `tools/it/emoji-cheatsheet.html` : `踩 (thumbs down)` : dead
- `tools/it/emoji-cheatsheet.html` : `车厢 (car)` : dead
- `tools/it/emoji-cheatsheet.html` : `轨迹球 (trackball)` : dead
- `tools/it/emoji-cheatsheet.html` : `轮船 (ship)` : dead
- `tools/it/emoji-cheatsheet.html` : `软盘 (floppy)` : dead
- `tools/it/emoji-cheatsheet.html` : `轻轨 (light rail)` : dead
- `tools/it/emoji-cheatsheet.html` : `辐射 (radioactive)` : dead
- `tools/it/emoji-cheatsheet.html` : `辣椒 (pepper)` : dead
- `tools/it/emoji-cheatsheet.html` : `过山车 (coaster)` : dead
- `tools/it/emoji-cheatsheet.html` : `运球 (ball)` : dead
- `tools/it/emoji-cheatsheet.html` : `迷妹 (star)` : dead
- `tools/it/emoji-cheatsheet.html` : `邮局 (post)` : dead
- `tools/it/emoji-cheatsheet.html` : `酒店 (hotel)` : dead
- `tools/it/emoji-cheatsheet.html` : `酷 (cool)` : dead
- `tools/it/emoji-cheatsheet.html` : `野猪 (boar)` : dead
- `tools/it/emoji-cheatsheet.html` : `金牛 (taurus)` : dead
- `tools/it/emoji-cheatsheet.html` : `钓鱼 (fishing)` : dead
- `tools/it/emoji-cheatsheet.html` : `钱袋 (bag)` : dead
- `tools/it/emoji-cheatsheet.html` : `钱飞 (money)` : dead
- `tools/it/emoji-cheatsheet.html` : `钻石 (gem)` : dead
- `tools/it/emoji-cheatsheet.html` : `银行 (bank)` : dead
- `tools/it/emoji-cheatsheet.html` : `锚 (anchor)` : dead
- `tools/it/emoji-cheatsheet.html` : `键盘 (keyboard)` : dead
- `tools/it/emoji-cheatsheet.html` : `长曲棍球 (lacrosse)` : dead
- `tools/it/emoji-cheatsheet.html` : `长颈鹿 (giraffe)` : dead
- `tools/it/emoji-cheatsheet.html` : `闪 (sparkles)` : dead
- `tools/it/emoji-cheatsheet.html` : `闪光 (sparkle)` : dead
- `tools/it/emoji-cheatsheet.html` : `闪光相机 (flash)` : dead
- `tools/it/emoji-cheatsheet.html` : `闪心 (sparkling)` : dead
- `tools/it/emoji-cheatsheet.html` : `闪星 (glowing star)` : dead
- `tools/it/emoji-cheatsheet.html` : `闪烁 (sparkle)` : dead
- `tools/it/emoji-cheatsheet.html` : `闪电 (zap)` : dead
- `tools/it/emoji-cheatsheet.html` : `闪电雨 (lightning)` : dead
- `tools/it/emoji-cheatsheet.html` : `闭眼亲 (kissing closed)` : dead
- `tools/it/emoji-cheatsheet.html` : `问号 (question)` : dead
- `tools/it/emoji-cheatsheet.html` : `闹钟 (alarm)` : dead
- `tools/it/emoji-cheatsheet.html` : `降落 (landing)` : dead
- `tools/it/emoji-cheatsheet.html` : `降落伞 (parachute)` : dead
- `tools/it/emoji-cheatsheet.html` : `除 (divide)` : dead
- `tools/it/emoji-cheatsheet.html` : `雕像 (statue)` : dead
- `tools/it/emoji-cheatsheet.html` : `雨 (rain)` : dead
- `tools/it/emoji-cheatsheet.html` : `雨伞 (umbrella rain)` : dead
- `tools/it/emoji-cheatsheet.html` : `雨太阳 (rain sun)` : dead
- `tools/it/emoji-cheatsheet.html` : `雪 (snow)` : dead
- `tools/it/emoji-cheatsheet.html` : `雪山 (snow mountain)` : dead
- `tools/it/emoji-cheatsheet.html` : `雪橇 (sled)` : dead
- `tools/it/emoji-cheatsheet.html` : `雪花 (snowflake)` : dead
- `tools/it/emoji-cheatsheet.html` : `雷雨 (storm)` : dead
- `tools/it/emoji-cheatsheet.html` : `震动 (vibration)` : dead
- `tools/it/emoji-cheatsheet.html` : `露营 (camp)` : dead
- `tools/it/emoji-cheatsheet.html` : `露齿笑 (grin)` : dead
- `tools/it/emoji-cheatsheet.html` : `青椒 (bell pepper)` : dead
- `tools/it/emoji-cheatsheet.html` : `青苹果 (green apple)` : dead
- `tools/it/emoji-cheatsheet.html` : `青菜 (greens)` : dead
- `tools/it/emoji-cheatsheet.html` : `青蛙 (frog)` : dead
- `tools/it/emoji-cheatsheet.html` : `面包 (bread)` : dead
- `tools/it/emoji-cheatsheet.html` : `面包车 (van)` : dead
- `tools/it/emoji-cheatsheet.html` : `面条 (noodle)` : dead
- `tools/it/emoji-cheatsheet.html` : `风 (wind)` : dead
- `tools/it/emoji-cheatsheet.html` : `飞吻 (kiss)` : dead
- `tools/it/emoji-cheatsheet.html` : `飞机 (airplane)` : dead
- `tools/it/emoji-cheatsheet.html` : `飞盘 (frisbee)` : dead
- `tools/it/emoji-cheatsheet.html` : `飞镖 (dart)` : dead
- `tools/it/emoji-cheatsheet.html` : `饭团 (rice ball)` : dead
- `tools/it/emoji-cheatsheet.html` : `饼干 (cookie)` : dead
- `tools/it/emoji-cheatsheet.html` : `馋 (yum)` : dead
- `tools/it/emoji-cheatsheet.html` : `香蕉 (banana)` : dead
- `tools/it/emoji-cheatsheet.html` : `马 (horse)` : dead
- `tools/it/emoji-cheatsheet.html` : `骆驼 (camel)` : dead
- `tools/it/emoji-cheatsheet.html` : `骑车 (bike)` : dead
- `tools/it/emoji-cheatsheet.html` : `骰子 (dice)` : dead
- `tools/it/emoji-cheatsheet.html` : `高尔夫 (golf)` : dead
- `tools/it/emoji-cheatsheet.html` : `高尔夫球手 (golfer)` : dead
- `tools/it/emoji-cheatsheet.html` : `高速列车 (bullet)` : dead
- `tools/it/emoji-cheatsheet.html` : `高铁 (train)` : dead
- `tools/it/emoji-cheatsheet.html` : `鱼 (fish)` : dead
- `tools/it/emoji-cheatsheet.html` : `鱿鱼 (squid)` : dead
- `tools/it/emoji-cheatsheet.html` : `鲨鱼 (shark)` : dead
- `tools/it/emoji-cheatsheet.html` : `鲸鱼 (whale)` : dead
- `tools/it/emoji-cheatsheet.html` : `鲸鱼2 (whale2)` : dead
- `tools/it/emoji-cheatsheet.html` : `鳄鱼 (crocodile)` : dead
- `tools/it/emoji-cheatsheet.html` : `鸟 (bird)` : dead
- `tools/it/emoji-cheatsheet.html` : `鸟居 (torii)` : dead
- `tools/it/emoji-cheatsheet.html` : `鸡 (chicken)` : dead
- `tools/it/emoji-cheatsheet.html` : `鸡尾酒 (cocktail)` : dead
- `tools/it/emoji-cheatsheet.html` : `鸡腿 (chicken)` : dead
- `tools/it/emoji-cheatsheet.html` : `鸡蛋 (egg)` : dead
- `tools/it/emoji-cheatsheet.html` : `鸭子 (duck)` : dead
- `tools/it/emoji-cheatsheet.html` : `鹰 (eagle)` : dead
- `tools/it/emoji-cheatsheet.html` : `黄心 (yellow heart)` : dead
- `tools/it/emoji-cheatsheet.html` : `黄瓜 (cucumber)` : dead
- `tools/it/emoji-cheatsheet.html` : `黑心 (black heart)` : dead
- `tools/it/emoji-cheatsheet.html` : `鼓掌 (clap)` : dead
- `tools/it/emoji-cheatsheet.html` : `鼠标 (mouse)` : dead
- `tools/it/emoji-cheatsheet.html` : `龙虾 (lobster)` : dead
- `tools/it/emoji-meaning.html` : `共 444 个 Emoji` : dead
- `tools/it/emoji-meaning.html` : `🇨🇳 旗帜` : dead
- `tools/it/git-commands.html` : `# 丢弃单个文件 ⏎  git checkout -- file.txt ⏎  ⏎ # 丢弃所有修改 ⏎  git checkout -- .` : dead
- `tools/it/git-commands.html` : `# 从其他分支取单个提交 ⏎  git cherry-pick abc1234 ⏎  ⏎ # 取多个提交 ⏎  git cherry-pick abc1234 def5678` : dead
- `tools/it/git-commands.html` : `# 修改提交信息 ⏎  git commit --amend -m "新的消息" ⏎  ⏎ # 追加文件到上次提交 ⏎  git add new-file.txt ⏎  git commit --amend --no-edit ⏎  ⏎ # 修改作者 ⏎  git commit --amend --author="张三…(+18字)` : dead
- `tools/it/git-commands.html` : `# 克隆仓库 ⏎  git clone https://github.com/user/repo.git ⏎  ⏎ # 克隆指定分支 ⏎  git clone -b main https://github.com/user/repo.git ⏎  ⏎ # 浅克隆（最近1次提交） ⏎  git clone --depth…(+35字)` : dead
- `tools/it/git-commands.html` : `# 切换分支 ⏎  git checkout main ⏎  ⏎ # 创建并切换分支 ⏎  git checkout -b feature ⏎  ⏎ # 强制创建分支 ⏎  git checkout -B feature origin/feature ⏎  ⏎ # 切换到上一个分支 ⏎  git checkout -` : dead
- `tools/it/git-commands.html` : `# 切换分支 ⏎  git switch main ⏎  ⏎ # 创建并切换 ⏎  git switch -c feature ⏎  ⏎ # 切换到远程分支 ⏎  git switch origin/feature` : dead
- `tools/it/git-commands.html` : `# 列出所有暂存 ⏎  git stash list` : dead
- `tools/it/git-commands.html` : `# 列出本地分支 ⏎  git branch ⏎  ⏎ # 列出所有分支（含远程） ⏎  git branch -a ⏎  ⏎ # 创建分支 ⏎  git branch feature ⏎  ⏎ # 删除分支 ⏎  git branch -d feature ⏎  ⏎ # 强制删除 ⏎  git branch -D f…(+88字)` : dead
- `tools/it/git-commands.html` : `# 列出标签 ⏎  git tag ⏎  git tag -l 'v1.*' ⏎  ⏎ # 创建轻量标签 ⏎  git tag v1.0.0 ⏎  ⏎ # 创建附注标签 ⏎  git tag -a v1.0.0 -m "发布 1.0.0" ⏎  ⏎ # 在指定提交打标签 ⏎  git tag -a v1.0.0 abc…(+136字)` : dead
- `tools/it/git-commands.html` : `# 列出远程 ⏎  git remote -v ⏎  ⏎ # 添加远程 ⏎  git remote add origin https://github.com/user/repo.git ⏎  ⏎ # 修改远程 URL ⏎  git remote set-url origin git@github.com:user/r…(+97字)` : dead
- `tools/it/git-commands.html` : `# 创建附注标签 ⏎  git tag -a v1.0.0 -m "Release 1.0.0" ⏎  ⏎ # 在指定提交创建 ⏎  git tag -a v1.0.0 abc1234 -m "Release 1.0.0"` : dead
- `tools/it/git-commands.html` : `# 初始化 Git Flow ⏎  git flow init` : dead
- `tools/it/git-commands.html` : `# 删除文件 ⏎  git rm file.txt ⏎  ⏎ # 从暂存区移除但保留本地 ⏎  git rm --cached file.txt ⏎  ⏎ # 递归删除目录 ⏎  git rm -r dist/` : dead
- `tools/it/git-commands.html` : `# 删除远程分支 ⏎  git push origin --delete feature` : dead
- `tools/it/git-commands.html` : `# 单行历史 ⏎  git log --oneline ⏎  ⏎ # 图形化所有分支 ⏎  git log --oneline --graph --all ⏎  ⏎ # 查看指定文件历史 ⏎  git log --oneline -- file.txt` : dead
- `tools/it/git-commands.html` : `# 变基到 main ⏎  git rebase main ⏎  ⏎ # 交互式变基（压缩/重排提交） ⏎  git rebase -i HEAD~3 ⏎  ⏎ # 变基到指定提交 ⏎  git rebase --onto main feature ⏎  ⏎ # 中止变基 ⏎  git rebase --abort ⏎…(+38字)` : dead
- `tools/it/git-commands.html` : `# 合并 feature 到当前分支 ⏎  git merge feature ⏎  ⏎ # 不使用快进（保留分支历史） ⏎  git merge --no-ff feature ⏎  ⏎ # Squash 合并（压缩为一次提交） ⏎  git merge --squash feature ⏎  git commit …(+48字)` : dead
- `tools/it/git-commands.html` : `# 合并保留分支历史 ⏎  git merge --no-ff feature ⏎  ⏎ # 配置默认不快进 ⏎  git config --global merge.ff false` : dead
- `tools/it/git-commands.html` : `# 在当前目录初始化 ⏎  git init ⏎  ⏎ # 指定初始分支名 ⏎  git init --initial-branch=main ⏎  ⏎ # 创建裸仓库（用于服务器） ⏎  git init --bare` : dead
- `tools/it/git-commands.html` : `# 在所有子模块拉取 ⏎  git submodule foreach git pull` : dead
- `tools/it/git-commands.html` : `# 垃圾回收 ⏎  git gc ⏎  ⏎ # 深度清理 ⏎  git gc --aggressive --prune=now` : dead
- `tools/it/git-commands.html` : `# 应用单个提交 ⏎  git cherry-pick abc1234 ⏎  ⏎ # 应用多个提交 ⏎  git cherry-pick abc1234 def5678 ⏎  ⏎ # 应用但不自动提交 ⏎  git cherry-pick --no-commit abc1234` : dead
- `tools/it/git-commands.html` : `# 开始二分 ⏎  git bisect start ⏎  ⏎ # 标记坏提交 ⏎  git bisect bad HEAD ⏎  ⏎ # 标记好提交 ⏎  git bisect good v1.0.0 ⏎  ⏎ # 自动测试 ⏎  git bisect run npm test ⏎  ⏎ # 结束二分 ⏎  git …(+12字)` : dead
- `tools/it/git-commands.html` : `# 开始发布 ⏎  git flow release start 1.0.0 ⏎  ⏎ # 完成发布 ⏎  git flow release finish 1.0.0` : dead
- `tools/it/git-commands.html` : `# 开始新功能 ⏎  git flow feature start my-feature ⏎  ⏎ # 完成功能 ⏎  git flow feature finish my-feature ⏎  ⏎ # 发布功能分支 ⏎  git flow feature publish my-feature ⏎  ⏎ # 切换到功能…(+42字)` : dead
- `tools/it/git-commands.html` : `# 开始热修复 ⏎  git flow hotfix start hotfix-1.0.1 ⏎  ⏎ # 完成热修复 ⏎  git flow hotfix finish hotfix-1.0.1` : dead
- `tools/it/git-commands.html` : `# 归档为 zip ⏎  git archive --format=zip --output=repo.zip HEAD ⏎  ⏎ # 归档为 tar.gz ⏎  git archive --format=tar.gz --output=repo.tar.gz HEAD` : dead
- `tools/it/git-commands.html` : `# 恢复最近的暂存 ⏎  git stash pop ⏎  ⏎ # 恢复指定暂存 ⏎  git stash pop stash@{2}` : dead
- `tools/it/git-commands.html` : `# 拉取并变基 ⏎  git pull --rebase origin main ⏎  ⏎ # 设置默认拉取为变基 ⏎  git config --global pull.rebase true` : dead
- `tools/it/git-commands.html` : `# 拉取并合并 ⏎  git pull origin main ⏎  ⏎ # 拉取并变基 ⏎  git pull --rebase origin main` : dead
- `tools/it/git-commands.html` : `# 拉取所有远程 ⏎  git fetch --all ⏎  ⏎ # 拉取指定远程 ⏎  git fetch origin ⏎  ⏎ # 拉取指定分支 ⏎  git fetch origin main` : dead
- `tools/it/git-commands.html` : `# 按作者统计提交数 ⏎  git shortlog -sn` : dead
- `tools/it/git-commands.html` : `# 推送当前分支 ⏎  git push ⏎  ⏎ # 推送并设置上游 ⏎  git push -u origin feature ⏎  ⏎ # 强制推送（危险！） ⏎  git push -f ⏎  git push --force-with-lease ⏎  ⏎ # 推送标签 ⏎  git push --tags …(+31字)` : dead
- `tools/it/git-commands.html` : `# 描述最近的标签 ⏎  git describe ⏎  ⏎ # 使用轻量标签 ⏎  git describe --tags` : dead
- `tools/it/git-commands.html` : `# 提交并写消息 ⏎  git commit -m "feat: 添加登录功能" ⏎  ⏎ # 跳过 add 直接提交已跟踪文件 ⏎  git commit -am "fix: 修复 bug" ⏎  ⏎ # 修改上一次提交（追加修改） ⏎  git add new-file.txt ⏎  git commit --am…(+59字)` : dead
- `tools/it/git-commands.html` : `# 撤销工作区修改 ⏎  git restore file.txt ⏎  ⏎ # 取消暂存（保留修改） ⏎  git restore --staged file.txt ⏎  ⏎ # 从指定提交恢复 ⏎  git restore --source=HEAD~1 file.txt` : dead
- `tools/it/git-commands.html` : `# 撤销最新提交 ⏎  git revert HEAD ⏎  ⏎ # 撤销指定提交 ⏎  git revert abc1234 ⏎  ⏎ # 撤销但不自动提交 ⏎  git revert --no-commit abc1234` : dead
- `tools/it/git-commands.html` : `# 暂存当前修改 ⏎  git stash ⏎  git stash save "work in progress" ⏎  ⏎ # 查看暂存列表 ⏎  git stash list ⏎  ⏎ # 恢复最近的暂存（并删除） ⏎  git stash pop ⏎  ⏎ # 恢复但不删除 ⏎  git stash apply…(+83字)` : dead
- `tools/it/git-commands.html` : `# 查看历史 ⏎  git log ⏎  ⏎ # 单行显示 ⏎  git log --oneline ⏎  ⏎ # 图形化显示分支 ⏎  git log --oneline --graph --all ⏎  ⏎ # 查看指定作者的提交 ⏎  git log --author="张三" ⏎  ⏎ # 查看最近 10 条 …(+98字)` : dead
- `tools/it/git-commands.html` : `# 查看工作区与暂存区差异 ⏎  git diff ⏎  ⏎ # 查看暂存区与最新提交差异 ⏎  git diff --staged ⏎  git diff --cached ⏎  ⏎ # 比较两个提交 ⏎  git diff abc1234 def5678 ⏎  ⏎ # 比较分支 ⏎  git diff main f…(+43字)` : dead
- `tools/it/git-commands.html` : `# 查看帮助 ⏎  git help ⏎  git help commit ⏎  git help push` : dead
- `tools/it/git-commands.html` : `# 查看引用日志 ⏎  git reflog ⏎  ⏎ # 恢复到 5 步前 ⏎  git reset --hard HEAD@{5}` : dead
- `tools/it/git-commands.html` : `# 查看引用日志 ⏎  git reflog ⏎  ⏎ # 查看所有引用 ⏎  git reflog --all ⏎  ⏎ # 找回丢失的提交 ⏎  git reset --hard HEAD@{5}` : dead
- `tools/it/git-commands.html` : `# 查看文件每行的修改者 ⏎  git blame file.txt ⏎  ⏎ # 查看指定行范围 ⏎  git blame -L 10,20 file.txt` : dead
- `tools/it/git-commands.html` : `# 查看最新提交 ⏎  git show ⏎  ⏎ # 查看指定提交 ⏎  git show abc1234 ⏎  ⏎ # 查看某文件的某次提交 ⏎  git show abc1234:file.txt` : dead
- `tools/it/git-commands.html` : `# 查看详细状态 ⏎  git status ⏎  ⏎ # 简短输出 ⏎  git status -s` : dead
- `tools/it/git-commands.html` : `# 检查 ⏎  git fsck` : dead
- `tools/it/git-commands.html` : `# 添加子模块 ⏎  git submodule add https://github.com/user/lib.git libs/lib ⏎  ⏎ # 初始化子模块 ⏎  git submodule init ⏎  git submodule update ⏎  ⏎ # 一次性初始化和更新 ⏎  git submod…(+94字)` : dead
- `tools/it/git-commands.html` : `# 添加工作树 ⏎  git worktree add ../repo-feature feature ⏎  ⏎ # 列出工作树 ⏎  git worktree list ⏎  ⏎ # 删除工作树 ⏎  git worktree remove ../repo-feature` : dead
- `tools/it/git-commands.html` : `# 添加所有变更 ⏎  git add . ⏎  git add -A ⏎  ⏎ # 添加修改和删除（不含新文件） ⏎  git add -u ⏎  ⏎ # 添加指定文件 ⏎  git add file1.txt file2.txt ⏎  ⏎ # 交互式添加 ⏎  git add -p` : dead
- `tools/it/git-commands.html` : `# 编辑最近 3 次提交 ⏎  git rebase -i HEAD~3 ⏎ # 在编辑器中可： ⏎ # pick   - 保留 ⏎ # reword - 修改信息 ⏎ # squash - 合并到上一条 ⏎ # drop   - 删除 ⏎ # edit   - 暂停修改` : dead
- `tools/it/git-commands.html` : `# 设置全局用户名 ⏎  git config --global user.name "张三" ⏎  ⏎ # 设置全局邮箱 ⏎  git config --global user.email "zs@example.com" ⏎  ⏎ # 设置默认编辑器 ⏎  git config --global core.edit…(+41字)` : dead
- `tools/it/git-commands.html` : `# 设置别名 ⏎  git config --global alias.co checkout ⏎  git config --global alias.br branch ⏎  git config --global alias.ci commit ⏎  git config --global alias.st st…(+31字)` : dead
- `tools/it/git-commands.html` : `# 设置默认分支为 main ⏎  git config --global init.defaultBranch main` : dead
- `tools/it/git-commands.html` : `# 软重置（保留修改） ⏎  git reset --soft HEAD~1 ⏎  ⏎ # 默认重置（取消暂存，保留修改） ⏎  git reset HEAD~1 ⏎  ⏎ # 硬重置（丢弃修改，危险！） ⏎  git reset --hard HEAD~1 ⏎  ⏎ # 重置到指定提交 ⏎  git reset --…(+12字)` : dead
- `tools/it/git-commands.html` : `# 重命名文件 ⏎  git mv old.txt new.txt ⏎  ⏎ # 移动文件到目录 ⏎  git mv file.txt src/` : dead
- `tools/it/git-commands.html` : `# 预览将删除的文件 ⏎  git clean -n ⏎  ⏎ # 删除未跟踪文件 ⏎  git clean -f ⏎  ⏎ # 删除未跟踪目录 ⏎  git clean -fd ⏎  ⏎ # 删除所有未跟踪（含忽略） ⏎  git clean -fdx` : dead
- `tools/it/git-commands.html` : `共 58 个命令` : dead
- `tools/it/go-cheatsheet.html` : `f, _ := os.Open("f") ⏎ defer f.Close() ⏎  ⏎ // LIFO 顺序 ⏎ defer fmt.Println("1") ⏎ defer fmt.Println("2")  -- 先输出` : dead
- `tools/it/go-cheatsheet.html` : `for i := 0; i < 5; i++ { fmt.Println(i) } ⏎ for _, v := range slice { fmt.Println(v) } ⏎ for cond { /* while */ } ⏎ for { /* 死循环 */ break }` : dead
- `tools/it/go-cheatsheet.html` : `func print(v any) { fmt.Println(v) } ⏎ var i any = 1 ⏎ v, ok := i.(int)  -- 类型断言 ⏎ switch v := i.(type) { ⏎   case int: ... ⏎ }` : dead
- `tools/it/go-cheatsheet.html` : `switch day { ⏎ case "Sat", "Sun": fmt.Println("weekend") ⏎ default: fmt.Println("workday") ⏎ } ⏎  ⏎ switch {  -- 无表达式 ⏎   case x < 0: ... ⏎ }` : dead
- `tools/it/go-escape.html` : `支持字符串与 rune 转义，含 \a \b \f \n \r \t \v \\ \' \" \xXX \uXXXX \UXXXXXXXX。` : dead
- `tools/it/hash-multi.html` : `,具备确定性、雪崩效应(改 1 bit 约半数输出变)、单向不可逆。` : dead
- `tools/it/hash-multi.html` : `哈希函数把任意长度输入映射为` : dead
- `tools/it/hash-multi.html` : `定长摘要` : dead
- `tools/it/html-entities.html` : `" - 双引号` : dead
- `tools/it/html-entities.html` : `& - 与号` : dead
- `tools/it/html-entities.html` : `&baht; - 泰铢` : dead
- `tools/it/html-entities.html` : `&dong; - 盾` : dead
- `tools/it/html-entities.html` : `&hrivn; - 格里夫纳` : dead
- `tools/it/html-entities.html` : `&lira; - 里拉` : dead
- `tools/it/html-entities.html` : `&peso; - 比索` : dead
- `tools/it/html-entities.html` : `&ruble; - 卢布` : dead
- `tools/it/html-entities.html` : `&rupee; - 卢比` : dead
- `tools/it/html-entities.html` : `&wron; - 韩元` : dead
- `tools/it/html-entities.html` : `' - 单引号` : dead
- `tools/it/html-entities.html` : `+ - 加号` : dead
- `tools/it/html-entities.html` : `¡ - 倒感叹号` : dead
- `tools/it/html-entities.html` : `¢ - 美分` : dead
- `tools/it/html-entities.html` : `¦ - 断竖线` : dead
- `tools/it/html-entities.html` : `§ - 章节符` : dead
- `tools/it/html-entities.html` : `¨ - 分音符` : dead
- `tools/it/html-entities.html` : `© - 版权` : dead
- `tools/it/html-entities.html` : `ª - 阴性序数` : dead
- `tools/it/html-entities.html` : `« - 左双尖引号` : dead
- `tools/it/html-entities.html` : `¬ - 非` : dead
- `tools/it/html-entities.html` : `® - 注册商标` : dead
- `tools/it/html-entities.html` : `¯ - 长音符号` : dead
- `tools/it/html-entities.html` : `° - 度` : dead
- `tools/it/html-entities.html` : `± - 正负号` : dead
- `tools/it/html-entities.html` : `² - 上标 2` : dead
- `tools/it/html-entities.html` : `³ - 上标 3` : dead
- `tools/it/html-entities.html` : `´ - 锐音符` : dead
- `tools/it/html-entities.html` : `µ - 微` : dead
- `tools/it/html-entities.html` : `¶ - 段落符` : dead
- `tools/it/html-entities.html` : `· - 中点` : dead
- `tools/it/html-entities.html` : `¸ - 下尾符` : dead
- `tools/it/html-entities.html` : `¹ - 上标 1` : dead
- `tools/it/html-entities.html` : `º - 阳性序数` : dead
- `tools/it/html-entities.html` : `» - 右双尖引号` : dead
- `tools/it/html-entities.html` : `¼ - 四分之一` : dead
- `tools/it/html-entities.html` : `½ - 二分之一` : dead
- `tools/it/html-entities.html` : `¾ - 四分之三` : dead
- `tools/it/html-entities.html` : `¿ - 倒问号` : dead
- `tools/it/html-entities.html` : `À - A 抑音符` : dead
- `tools/it/html-entities.html` : `Á - A 锐音符` : dead
- `tools/it/html-entities.html` : `Â - A 扬抑符` : dead
- `tools/it/html-entities.html` : `Ã - A 鼻化符` : dead
- `tools/it/html-entities.html` : `Ä - A 分音符` : dead
- `tools/it/html-entities.html` : `Å - A 上圆圈` : dead
- `tools/it/html-entities.html` : `Æ - AE 连字` : dead
- `tools/it/html-entities.html` : `Ç - C 下尾符` : dead
- `tools/it/html-entities.html` : `È - E 抑音符` : dead
- `tools/it/html-entities.html` : `É - E 锐音符` : dead
- `tools/it/html-entities.html` : `Ê - E 扬抑符` : dead
- `tools/it/html-entities.html` : `Ë - E 分音符` : dead
- `tools/it/html-entities.html` : `Ì - I 抑音符` : dead
- `tools/it/html-entities.html` : `Í - I 锐音符` : dead
- `tools/it/html-entities.html` : `Î - I 扬抑符` : dead
- `tools/it/html-entities.html` : `Ï - I 分音符` : dead
- `tools/it/html-entities.html` : `Ñ - N 鼻化符` : dead
- `tools/it/html-entities.html` : `Ò - O 抑音符` : dead
- `tools/it/html-entities.html` : `Ó - O 锐音符` : dead
- `tools/it/html-entities.html` : `Ô - O 扬抑符` : dead
- `tools/it/html-entities.html` : `Õ - O 鼻化符` : dead
- `tools/it/html-entities.html` : `Ö - O 分音符` : dead
- `tools/it/html-entities.html` : `× - 乘号` : dead
- `tools/it/html-entities.html` : `Ø - O 斜线` : dead
- `tools/it/html-entities.html` : `Ù - U 抑音符` : dead
- `tools/it/html-entities.html` : `Ú - U 锐音符` : dead
- `tools/it/html-entities.html` : `Û - U 扬抑符` : dead
- `tools/it/html-entities.html` : `Ü - U 分音符` : dead
- `tools/it/html-entities.html` : `Ý - Y 锐音符` : dead
- `tools/it/html-entities.html` : `à - a 抑音符` : dead
- `tools/it/html-entities.html` : `á - a 锐音符` : dead
- `tools/it/html-entities.html` : `â - a 扬抑符` : dead
- `tools/it/html-entities.html` : `ã - a 鼻化符` : dead
- `tools/it/html-entities.html` : `ä - a 分音符` : dead
- `tools/it/html-entities.html` : `å - a 上圆圈` : dead
- `tools/it/html-entities.html` : `æ - ae 连字` : dead
- `tools/it/html-entities.html` : `ç - c 下尾符` : dead
- `tools/it/html-entities.html` : `è - e 抑音符` : dead
- `tools/it/html-entities.html` : `é - e 锐音符` : dead
- `tools/it/html-entities.html` : `ê - e 扬抑符` : dead
- `tools/it/html-entities.html` : `ë - e 分音符` : dead
- `tools/it/html-entities.html` : `ì - i 抑音符` : dead
- `tools/it/html-entities.html` : `í - i 锐音符` : dead
- `tools/it/html-entities.html` : `î - i 扬抑符` : dead
- `tools/it/html-entities.html` : `ï - i 分音符` : dead
- `tools/it/html-entities.html` : `ñ - n 鼻化符` : dead
- `tools/it/html-entities.html` : `ò - o 抑音符` : dead
- `tools/it/html-entities.html` : `ó - o 锐音符` : dead
- `tools/it/html-entities.html` : `ô - o 扬抑符` : dead
- `tools/it/html-entities.html` : `õ - o 鼻化符` : dead
- `tools/it/html-entities.html` : `ö - o 分音符` : dead
- `tools/it/html-entities.html` : `÷ - 除号` : dead
- `tools/it/html-entities.html` : `ø - o 斜线` : dead
- `tools/it/html-entities.html` : `ù - u 抑音符` : dead
- `tools/it/html-entities.html` : `ú - u 锐音符` : dead
- `tools/it/html-entities.html` : `û - u 扬抑符` : dead
- `tools/it/html-entities.html` : `ü - u 分音符` : dead
- `tools/it/html-entities.html` : `ý - y 锐音符` : dead
- `tools/it/html-entities.html` : `ÿ - y 分音符` : dead
- `tools/it/html-entities.html` : `π - 圆周率` : dead
- `tools/it/html-entities.html` : `– - 短破折号` : dead
- `tools/it/html-entities.html` : `— - 长破折号` : dead
- `tools/it/html-entities.html` : `‘ - 左单引号` : dead
- `tools/it/html-entities.html` : `’ - 右单引号` : dead
- `tools/it/html-entities.html` : `“ - 左双引号` : dead
- `tools/it/html-entities.html` : `” - 右双引号` : dead
- `tools/it/html-entities.html` : `• - 黑色圆点` : dead
- `tools/it/html-entities.html` : `… - 省略号` : dead
- `tools/it/html-entities.html` : `‰ - 千分号` : dead
- `tools/it/html-entities.html` : `′ - 撇` : dead
- `tools/it/html-entities.html` : `″ - 双撇` : dead
- `tools/it/html-entities.html` : `‹ - 单左尖引号` : dead
- `tools/it/html-entities.html` : `› - 单右尖引号` : dead
- `tools/it/html-entities.html` : `™ - 商标` : dead
- `tools/it/html-entities.html` : `⅓ - 三分之一` : dead
- `tools/it/html-entities.html` : `← - 左箭头` : dead
- `tools/it/html-entities.html` : `↑ - 上箭头` : dead
- `tools/it/html-entities.html` : `→ - 右箭头` : dead
- `tools/it/html-entities.html` : `↓ - 下箭头` : dead
- `tools/it/html-entities.html` : `↔ - 左右箭头` : dead
- `tools/it/html-entities.html` : `↕ - 上下箭头` : dead
- `tools/it/html-entities.html` : `↖ - 左上箭头` : dead
- `tools/it/html-entities.html` : `↗ - 右上箭头` : dead
- `tools/it/html-entities.html` : `↘ - 右下箭头` : dead
- `tools/it/html-entities.html` : `↙ - 左下箭头` : dead
- `tools/it/html-entities.html` : `↵ - 回车箭头` : dead
- `tools/it/html-entities.html` : `⇐ - 双线左箭头` : dead
- `tools/it/html-entities.html` : `⇑ - 双线上箭头` : dead
- `tools/it/html-entities.html` : `⇒ - 双线右箭头` : dead
- `tools/it/html-entities.html` : `⇓ - 双线下箭头` : dead
- `tools/it/html-entities.html` : `⇔ - 双线左右箭头` : dead
- `tools/it/html-entities.html` : `∀ - 任意` : dead
- `tools/it/html-entities.html` : `∂ - 偏导数` : dead
- `tools/it/html-entities.html` : `∃ - 存在` : dead
- `tools/it/html-entities.html` : `∅ - 空集` : dead
- `tools/it/html-entities.html` : `∇ - 梯度` : dead
- `tools/it/html-entities.html` : `∈ - 属于` : dead
- `tools/it/html-entities.html` : `∉ - 不属于` : dead
- `tools/it/html-entities.html` : `∏ - 求积` : dead
- `tools/it/html-entities.html` : `∑ - 求和` : dead
- `tools/it/html-entities.html` : `√ - 平方根` : dead
- `tools/it/html-entities.html` : `∞ - 无穷` : dead
- `tools/it/html-entities.html` : `∠ - 角` : dead
- `tools/it/html-entities.html` : `∥ - 平行` : dead
- `tools/it/html-entities.html` : `∩ - 交集` : dead
- `tools/it/html-entities.html` : `∪ - 并集` : dead
- `tools/it/html-entities.html` : `∫ - 积分` : dead
- `tools/it/html-entities.html` : `≠ - 不等于` : dead
- `tools/it/html-entities.html` : `≡ - 恒等于` : dead
- `tools/it/html-entities.html` : `⊂ - 真子集` : dead
- `tools/it/html-entities.html` : `⊃ - 真超集` : dead
- `tools/it/html-entities.html` : `⊆ - 子集` : dead
- `tools/it/html-entities.html` : `⊇ - 超集` : dead
- `tools/it/html-entities.html` : `⊥ - 垂直` : dead
- `tools/it/html-entities.html` : `⋄ - 白色菱形` : dead
- `tools/it/html-entities.html` : `⋄ - 黑色菱形` : dead
- `tools/it/html-entities.html` : `□ - 小黑色方块` : dead
- `tools/it/html-entities.html` : `□ - 白色方块` : dead
- `tools/it/html-entities.html` : `▪ - 黑色方块` : dead
- `tools/it/html-entities.html` : `▴ - 黑色三角` : dead
- `tools/it/html-entities.html` : `▵ - 白色三角` : dead
- `tools/it/html-entities.html` : `▾ - 黑色倒三角` : dead
- `tools/it/html-entities.html` : `▿ - 白色倒三角` : dead
- `tools/it/html-entities.html` : `○ - 小白色方块` : dead
- `tools/it/html-entities.html` : `共 181 个实体` : dead
- `tools/it/html-escape.html` : `HTML命名 · 转义 · 09/30 00:44` : dead
- `tools/it/html-minifier.html` : `<div class="card"> ⏎   <h2>月度报表</h2> ⏎   <p>共 128 条记录，新增 12 条。</p> ⏎   <ul> ⏎     <li>项目 1</li> ⏎     <li>项目 2</li> ⏎   </ul> ⏎ </div>` : dead
- `tools/it/html-tags.html` : `<address> ⏎   作者：张三<br> ⏎   邮箱：a@b.com ⏎ </address>` : dead
- `tools/it/html-tags.html` : `<article> ⏎   <h2>文章标题</h2> ⏎   <p>文章内容</p> ⏎ </article>` : dead
- `tools/it/html-tags.html` : `<aside> ⏎   <h3>相关链接</h3> ⏎   <ul>...</ul> ⏎ </aside>` : dead
- `tools/it/html-tags.html` : `<blockquote cite="https://example.com"> ⏎   这是引用内容。 ⏎ </blockquote>` : dead
- `tools/it/html-tags.html` : `<body> ⏎   <h2>欢迎</h2> ⏎   <p>正文内容</p> ⏎ </body>` : dead
- `tools/it/html-tags.html` : `<datalist id="cities"> ⏎   <option value="北京"> ⏎ </datalist>` : dead
- `tools/it/html-tags.html` : `<details> ⏎   <summary>点击展开</summary> ⏎   <p>详细内容</p> ⏎ </details>` : dead
- `tools/it/html-tags.html` : `<dialog open> ⏎   <p>对话框内容</p> ⏎ </dialog>` : dead
- `tools/it/html-tags.html` : `<dl> ⏎   <dt>HTML</dt> ⏎   <dd>超文本标记语言</dd> ⏎ </dl>` : dead
- `tools/it/html-tags.html` : `<fieldset> ⏎   <legend>用户信息</legend> ⏎   <input type="text"> ⏎ </fieldset>` : dead
- `tools/it/html-tags.html` : `<figure> ⏎   <img alt=""  src="https://placehold.co/300x200"> ⏎   <figcaption>图片说明</figcaption> ⏎ </figure>` : dead
- `tools/it/html-tags.html` : `<footer> ⏎   <p>版权 © 2024</p> ⏎ </footer>` : dead
- `tools/it/html-tags.html` : `<head>\n  <meta charset="UTF-8">\n  &lt;title&gt;标题&lt;/title&gt;\n</head>` : dead
- `tools/it/html-tags.html` : `<header> ⏎   <h2>网站标题</h2> ⏎   <nav>...</nav> ⏎ </header>` : dead
- `tools/it/html-tags.html` : `<label for="user">用户名</label> ⏎ <input id="user" type="text">` : dead
- `tools/it/html-tags.html` : `<main> ⏎   <h2>主标题</h2> ⏎ </main>` : dead
- `tools/it/html-tags.html` : `<menu> ⏎   <li>菜单项</li> ⏎ </menu>` : dead
- `tools/it/html-tags.html` : `<nav> ⏎   <a href="https://example.com/">首页</a> ⏎   <a href="https://example.com/about">关于</a> ⏎ </nav>` : dead
- `tools/it/html-tags.html` : `<noscript> ⏎   <p>请启用 JavaScript</p> ⏎ </noscript>` : dead
- `tools/it/html-tags.html` : `<ol> ⏎   <li>第一项</li> ⏎   <li>第二项</li> ⏎ </ol>` : dead
- `tools/it/html-tags.html` : `<optgroup label="亚洲"> ⏎   <option>中国</option> ⏎ </optgroup>` : dead
- `tools/it/html-tags.html` : `<pre> ⏎   保留空格 ⏎   和换行 ⏎ </pre>` : dead
- `tools/it/html-tags.html` : `<script src="app.js"></script> ⏎ <script> ⏎   console.log("内联"); ⏎ </script>` : dead
- `tools/it/html-tags.html` : `<section> ⏎   <h2>章节标题</h2> ⏎   <p>内容</p> ⏎ </section>` : dead
- `tools/it/html-tags.html` : `<select name="city"> ⏎   <option value="bj">北京</option> ⏎ </select>` : dead
- `tools/it/html-tags.html` : `<table> ⏎   <tr><td>单元格</td></tr> ⏎ </table>` : dead
- `tools/it/html-tags.html` : `<tbody> ⏎   <tr><td>内容</td></tr> ⏎ </tbody>` : dead
- `tools/it/html-tags.html` : `<template id="t"> ⏎   <div>模板</div> ⏎ </template>` : dead
- `tools/it/html-tags.html` : `<tfoot> ⏎   <tr><td>合计</td></tr> ⏎ </tfoot>` : dead
- `tools/it/html-tags.html` : `<thead> ⏎   <tr><th>标题</th></tr> ⏎ </thead>` : dead
- `tools/it/html-tags.html` : `<tr> ⏎   <td>单元格</td> ⏎ </tr>` : dead
- `tools/it/html-tags.html` : `<ul> ⏎   <li>项目1</li> ⏎   <li>项目2</li> ⏎ </ul>` : dead
- `tools/it/html-tags.html` : `共 121 个标签` : dead
- `tools/it/http-cookies.html` : `共 26 项` : dead
- `tools/it/http-headers.html` : `共 91 项` : dead
- `tools/it/http-response-headers.html` : `共 65 项` : dead
- `tools/it/js-formatter.html` : `⚠ 含 import/export 模块语法，浏览器脚本编译器无法校验，仅做括号配对检查` : dead
- `tools/it/js-minify.html` : `// 计算总价 ⏎ function total(items) { ⏎   /* 遍历累加 */ ⏎   var s = 0; ⏎   for (var i = 0; i < items.length; i++) { ⏎     s += items[i]; ⏎   } ⏎   return s; ⏎ }` : dead
- `tools/it/json-diff.html` : `"city": "上海",` : dead
- `tools/it/json-diff.html` : `"city": "北京",` : dead
- `tools/it/json-formatter.html` : `点击复制值` : dead
- `tools/it/json-formatter.html` : `点击复制对象` : dead
- `tools/it/json-formatter.html` : `点击复制数组` : dead
- `tools/it/json-formatter.html` : `点击复制键` : dead
- `tools/it/json-path.html` : `$.store.book[?(@.price<10)] 过滤` : dead
- `tools/it/kubernetes-cheatsheet.html` : `kubectl label pod web-xxx env=prod ⏎ kubectl label pod web-xxx env-  -- 删除标签` : dead
- `tools/it/latex.html` : `共 183 条（点击命令复制）` : dead
- `tools/it/linux-cheatsheet.html` : `export PATH=$PATH:$HOME/.local/bin ⏎ # 写入 ~/.bashrc 永久生效` : dead
- `tools/it/linux-cheatsheet.html` : `history ⏎  !!  -- 上一条 ⏎  !42  -- 第 42 条` : dead
- `tools/it/linux-cheatsheet.html` : `sleep 100 & ⏎ echo $!  -- 进程 PID` : dead
- `tools/it/linux-cheatsheet.html` : `共 114 项` : dead
- `tools/it/matrix-transpose.html` : `矩阵 A (2×3)` : dead
- `tools/it/md5.html` : `MD5加密工具` : dead
- `tools/it/md5.html` : `免费在线MD5加密工具，生成字符串的MD5哈希值，支持批量生成，MD5碰撞检测参考。纯前端本地处理。。专为开发者打造的在线工具，纯前端运行，代码不离开浏览器。` : dead
- `tools/it/md5.html` : `关于「MD5加密工具」` : dead
- `tools/it/md5.html` : `勾选「每行分别哈希」后，输入框按换行拆分成行，每行单独计算 MD5。例如两行 a、b → 0cc175b9c0f1b6a831c399e269772661 与 92eb5ffee6ae2fec3ad71c777531578f，结果表同时列出原文与摘要，便于逐条核对。` : dead
- `tools/it/md5.html` : `逐行批量哈希` : dead
- `tools/it/mongodb-cheatsheet.html` : `db.users.find({name: {$regex: "^张", $options: "i"}})` : dead
- `tools/it/mongodb-cheatsheet.html` : `共 53 项` : dead
- `tools/it/nginx-cheatsheet.html` : `access_log /var/log/nginx/access.log main; ⏎ error_log /var/log/nginx/error.log warn; ⏎ access_log off;  -- 关闭` : dead
- `tools/it/nginx-cheatsheet.html` : `nginx -s reload ⏎ nginx -s stop ⏎ nginx -s reopen  -- 重开日志` : dead
- `tools/it/nginx-cheatsheet.html` : `共 34 项` : dead
- `tools/it/nginx-config-generator.html` : `新站点上线前生成配置：填域名、端口与后端地址得到可用的 server 块，再按需要补 HTTPS 与安全头。` : dead
- `tools/it/nginx-config-generator.html` : `至少三件事：一是 HTTPS（证书路径、HTTP/2，以及 80 端口跳转）；二是安全头（HSTS、X-Content-Type-Options，CSP 视情况）；三是上传大小与超时（client_max_body_size、proxy_read_timeout），默认值常不适合实际业务。上线前务必 nginx -t …(+3字)` : dead
- `tools/it/nickname-generator.html` : `组合 = 形容词词库 × 名词词库 × 可选数字后缀` : dead
- `tools/it/phone-parser.html` : `常见原因：号码缺少国家码（无法判断归属）、包含了分隔符与分机号，或是虚拟运营商与新号段尚未收录。中国手机号是 11 位、以 1 开头，若输入的是固话需带区号。解析失败时应保留原始输入并提示用户补充国家码，而不是直接丢弃。` : dead
- `tools/it/phone-parser.html` : `显示：中国 11 位手机按 3-4-4 分组，其余按 4 位一组从右分组。` : dead
- `tools/it/phone-parser.html` : `校验：只校验长度范围；号段/前缀是否真实存在需另用权威号码库。` : dead
- `tools/it/phone-parser.html` : `清洗：剔除非数字字符（空格、连字符、括号） ⏎ 国家码：优先用输入中的“+”前缀识别；否则用所选地区；若纯数字开头已含所选国家码且余下长度合理，则自动剥离 ⏎ 国内首位 0：英国/日本/印度/中国台湾/澳大利亚等按规则去掉（trunk prefix） ⏎ E.164 = + 国家码 + 国内号码，总长 ≤15 位 ⏎ …(+32字)` : dead
- `tools/it/phone-parser.html` : `清洗：剔除非数字字符（空格、连字符、括号）国家码：优先用输入中的“+”前缀识别；否则用所选地区；若纯数字开头已含所选国家码且余下长度合理，则自动剥离国内首位 0：英国/日本/印度/中国台湾/澳大利亚等按规则去掉（trunk prefix）E.164 = + 国家码 + 国内号码，总长 ≤15 位校验：仅校验国内号码长度…(+20字)` : dead
- `tools/it/phone-parser.html` : `结果拆分展示国家码、区号与用户号，便于国际呼叫、存储与校验；建议始终带国家区号以确保跨区可用。` : dead
- `tools/it/phone-parser.html` : `若原号码已含国家码，请选择对应国家再粘贴纯数字。` : dead
- `tools/it/phone-parser.html` : `解析电话号码并按要求格式化。` : dead
- `tools/it/phone-parser.html` : `解析范围：识别并剥离国家码、去掉国内首位 0；不解析区号归属地，也不判断运营商。` : dead
- `tools/it/phone-parser.html` : `：国内号码常按 3-4-4 分组，国际格式按国家分组规则展示。` : dead
- `tools/it/phone-parser.html` : `：识别国家码、区号与本地号码，再按目标格式重新分组排版。` : dead
- `tools/it/phone-parser.html` : `：需依据各国号段规则判断长度与前缀是否合法。` : dead
- `tools/it/php-cheatsheet.html` : `$s = "hello"; ⏎ strlen($s);  -- 字节 ⏎ mb_strlen($s);  -- 字符 ⏎ $s . "!"; ⏎ sprintf("Hi %s", $name); ⏎ str_replace("a", "b", $s); ⏎ explode(",", "a,b"); ⏎ implode(…(+16字)` : dead
- `tools/it/php-cheatsheet.html` : `$s = json_encode($data);  -- 数组/对象 ⏎ $obj = json_decode($s);  -- 对象 ⏎ $arr = json_decode($s, true);  -- 关联数组` : dead
- `tools/it/php-cheatsheet.html` : `<?php ⏎ echo "hi"; ⏎ ?> ⏎ <?= $var ?>  -- 等同 echo` : dead
- `tools/it/php-cheatsheet.html` : `function add(int $a, int $b = 0): int { ⏎   return $a + $b; ⏎ } ⏎ function inc(&$x) { $x++; } ⏎ $fn = fn($x) => $x * 2;  -- 箭头函数` : dead
- `tools/it/php-cheatsheet.html` : `共 23 项` : dead
- `tools/it/postgresql-cheatsheet.html` : `-- 会话 A ⏎ LISTEN user_events; ⏎ -- 会话 B ⏎ NOTIFY user_events, '{"id":1}';` : dead
- `tools/it/postgresql-cheatsheet.html` : `VACUUM ANALYZE users; ⏎ VACUUM FULL;  -- 锁表，回收空间` : dead
- `tools/it/python-cheatsheet.html` : `class Dog: ⏎     species = "Canis"  -- 类属性 ⏎     def __init__(self, name): ⏎         self.name = name ⏎     def bark(self): return f"{self.name}!" ⏎  ⏎ d = Dog(…(+17字)` : dead
- `tools/it/python-cheatsheet.html` : `import os ⏎ from datetime import datetime, timedelta ⏎ import numpy as np ⏎ from . import helper  -- 相对导入` : dead
- `tools/it/python-cheatsheet.html` : `name = "Alice" ⏎ f"Hello {name}" ⏎ f"{1+1=}"  -- "1+1=2" ⏎ f"{3.14159:.2f}"  -- "3.14" ⏎ f"{'center':^10}"  -- 居中` : dead
- `tools/it/python-cheatsheet.html` : `raise ValueError("invalid") ⏎ raise  -- 重抛` : dead
- `tools/it/python-cheatsheet.html` : `s = {1, 2, 3} ⏎ s.add(4) ⏎ 1 in s  -- True ⏎ s & {2,3,4}  -- 交 ⏎ s | {5}  -- 并` : dead
- `tools/it/python-cheatsheet.html` : `t = (1, "a") ⏎ a, b = t  -- 解包` : dead
- `tools/it/python-cheatsheet.html` : `x = 1 ⏎ name: str = "Alice" ⏎ x, y = 1, 2  -- 多重赋值 ⏎ x, *rest = [1,2,3]  -- rest=[2,3]` : dead
- `tools/it/python-cheatsheet.html` : `xs = [1,2,3] ⏎ xs.append(4)  -- [1,2,3,4] ⏎ xs.pop()  -- 4 ⏎ xs[0] = 9 ⏎ xs[1:3]  -- 切片 ⏎ [x*2 for x in xs if x > 1]  -- 推导式` : dead
- `tools/it/qr-decoder.html` : `查询提示:` : dead
- `tools/it/random.html` : `结果: <strong id="singleResult"></strong>` : dead
- `tools/it/redis-cheatsheet.html` : `PING  -- 返回 PONG ⏎ PING hello  -- 返回 hello` : dead
- `tools/it/redis-cheatsheet.html` : `WATCH counter ⏎ MULTI ⏎ INCR counter ⏎ EXEC  -- 若 counter 被改则 nil` : dead
- `tools/it/redis-cheatsheet.html` : `共 83 项` : dead
- `tools/it/regex-cheatsheet.html` : `/(<\w+>).*<\/\1>/ 匹配 <b>x</b>` : dead
- `tools/it/regex-cheatsheet.html` : `/(?<!\$)\d+/ 匹配非"$"后的数字` : dead
- `tools/it/regex-cheatsheet.html` : `/(?<=\$)\d+/ 匹配 "$100" 中的 100` : dead
- `tools/it/regex-cheatsheet.html` : `/(?<year>\d{4})-(?<month>\d{2})/ ⏎ 替换：${year}` : dead
- `tools/it/regex-cheatsheet.html` : `/(ab)+/ 匹配 abab ⏎ 替换：$1 表示第 1 组` : dead
- `tools/it/regex-cheatsheet.html` : `/\Bcat/ 匹配 category 中的 cat` : dead
- `tools/it/regex-cheatsheet.html` : `/\bcat\b/ 匹配 cat 不匹配 category` : dead
- `tools/it/regex-cheatsheet.html` : `/\d+(?!元)/ 匹配非"元"前的数字` : dead
- `tools/it/regex-cheatsheet.html` : `/\d+(?=元)/ 匹配 "100元" 中的 100` : dead
- `tools/it/regex-cheatsheet.html` : `/\d+/ 匹配 123 ⏎ /\D+/ 匹配 abc` : dead
- `tools/it/regex-cheatsheet.html` : `/\d+/g 匹配所有` : dead
- `tools/it/regex-cheatsheet.html` : `/\d{2,4}/ 匹配 2-4 位` : dead
- `tools/it/regex-cheatsheet.html` : `/\d{2,}/ 匹配至少 2 位` : dead
- `tools/it/regex-cheatsheet.html` : `/\d{4}/ 匹配 4 位数字` : dead
- `tools/it/regex-cheatsheet.html` : `/\n/ 匹配换行` : dead
- `tools/it/regex-cheatsheet.html` : `/\p{Letter}/u  字母 ⏎ /\p{Number}/u  数字 ⏎ /\p{Script=Han}/u  汉字` : dead
- `tools/it/regex-cheatsheet.html` : `/\s+/ 匹配空格\t制表` : dead
- `tools/it/regex-cheatsheet.html` : `/\u4e2d/ 匹配 中` : dead
- `tools/it/regex-cheatsheet.html` : `/\w+/ 匹配 hello_123` : dead
- `tools/it/regex-cheatsheet.html` : `/\x41/ 匹配 A` : dead
- `tools/it/regex-cheatsheet.html` : `/^\uD83D/u ⏎ /^\p{L}+/u 匹配所有字母` : dead
- `tools/it/regex-cheatsheet.html` : `/a*/ 匹配 "" "a" "aaa"` : dead
- `tools/it/regex-cheatsheet.html` : `/a+/ 匹配 "a" "aaa"，不匹配 ""` : dead
- `tools/it/regex-cheatsheet.html` : `[[:alpha:]]  字母 ⏎ [[:digit:]]  数字 ⏎ [[:space:]]  空白` : dead
- `tools/it/regex-cheatsheet.html` : `含 \t\n\r\f\v` : dead
- `tools/it/robots-txt-generator.html` : `选择 User-agent、Allow、Disallow 与 Sitemap，快速生成 <code>robots.txt</code>。` : dead
- `tools/it/sql-cheatsheet.html` : `BEGIN; ⏎ UPDATE accounts SET balance = balance - 100 WHERE id = 1; ⏎ UPDATE accounts SET balance = balance + 100 WHERE id = 2; ⏎ COMMIT;  -- 或 ROLLBACK` : dead
- `tools/it/sqlite-cheatsheet.html` : `共 46 项` : dead
- `tools/it/team-name-generator.html` : `组合 = 风格词库（形容词 × 名词）× 可选后缀` : dead
- `tools/it/text-similarity.html` : `|  文本A长度: 14  |  文本B长度: 15` : dead
- `tools/it/text-similarity.html` : `|  文本A长度: 14  |  文本B长度: 15` : dead
- `tools/it/text-similarity.html` : `插入 1 次` : dead
- `tools/it/text-similarity.html` : `文本长度不等（A: 14, B: 15），汉明距离仅适用于等长字符串。` : dead
- `tools/it/text-similarity.html` : `替换 4 次` : dead
- `tools/it/text-to-hex.html` : `\\x 前缀` : dead
- `tools/it/time-format-converter.html` : `同一时刻在不同时区显示的"墙钟时间"不同。请确认所选时区与你的日志来源一致，否则转换出的日期会差几小时。` : dead
- `tools/it/time-format-converter.html` : `输入 Unix 秒级时间戳 '1690000000' → 输出 '2023-07-22 08:53:20 UTC'（按所选时区换算）。 ⏎ 反向：输入 '2023-07-22 08:53:20' + 时区 UTC → 输出 '1690000000'。` : dead
- `tools/it/timestamp-converter.html` : `✅ 识别为微秒时间戳（16 位）→ 已同步填充秒、毫秒与日期时间` : dead
- `tools/it/timestamp-converter.html` : `✅ 识别为毫秒时间戳（12 位）→ 已同步填充秒、毫秒与日期时间` : dead
- `tools/it/timestamp-converter.html` : `东京 (GMT+9)` : dead
- `tools/it/timestamp-converter.html` : `伦敦 (GMT+0)` : dead
- `tools/it/timestamp-converter.html` : `北京 (GMT+8)` : dead
- `tools/it/timestamp-converter.html` : `夏威夷 (GMT-10)` : dead
- `tools/it/timestamp-converter.html` : `巴黎 (GMT+1)` : dead
- `tools/it/timestamp-converter.html` : `悉尼 (GMT+11)` : dead
- `tools/it/timestamp-converter.html` : `洛杉矶 (GMT-8)` : dead
- `tools/it/timestamp-converter.html` : `纽约 (GMT-5)` : dead
- `tools/it/tmux-cheatsheet.html` : `# 先按 C-b 再按后续键 ⏎ # 例：C-b c 新建窗口` : dead
- `tools/it/tmux-cheatsheet.html` : `C-b "  -- 上下分割` : dead
- `tools/it/tmux-cheatsheet.html` : `C-b (  上个 ⏎ C-b )  下个` : dead
- `tools/it/tmux-cheatsheet.html` : `C-b :set mouse on  -- 开启鼠标 ⏎ C-b :source ~/.tmux.conf  -- 重载配置` : dead
- `tools/it/tmux-cheatsheet.html` : `C-b [  -- 进入复制模式 ⏎   空格 开始选择 ⏎   Enter 复制 ⏎   q 退出` : dead
- `tools/it/tmux-cheatsheet.html` : `C-b n  下个 ⏎ C-b p  上个` : dead
- `tools/it/tmux-cheatsheet.html` : `C-b q  -- 显示编号 ⏎ C-b q 2  -- 跳到 2 号` : dead
- `tools/it/tmux-cheatsheet.html` : `C-b t  -- 大时钟 ⏎ 任意键退出` : dead
- `tools/it/tmux-cheatsheet.html` : `setw -g mode-keys vi ⏎ # 复制模式下：hjkl 移动, v 选择, y 复制` : dead
- `tools/it/tmux-cheatsheet.html` : `tmux  -- 匿名会话 ⏎ tmux new -s work  -- 名为 work ⏎ tmux new -s work -d  -- 后台` : dead
- `tools/it/tmux-cheatsheet.html` : `tmux kill-session -t old ⏎ tmux kill-session -a  -- 关闭除当前外所有` : dead
- `tools/it/triangle-calculator.html` : `判断类型：任一内角≈90° 为直角，三者都<90° 为锐角，否则为钝角（浮点误差用 1e-6 容差）。` : dead
- `tools/it/typescript-cheatsheet.html` : `class C { ⏎   private x = 1;  -- 仅本类 ⏎   protected y = 2;  -- 子类 ⏎   #z = 3;  -- 真私有 ⏎ }` : dead
- `tools/it/typescript-cheatsheet.html` : `const cfg = { port: 80 } satisfies Config; ⏎ -- 保留字面量类型，又校验` : dead
- `tools/it/typescript-cheatsheet.html` : `enum Color { Red, Green, Blue } ⏎ let c: Color = Color.Red; ⏎  ⏎ const enum Dir { Up, Down }  -- 内联` : dead
- `tools/it/typescript-cheatsheet.html` : `function id<T>(x: T): T { return x; } ⏎ const r = id<number>(5); ⏎ const r2 = id("a");  -- 推断` : dead
- `tools/it/typescript-cheatsheet.html` : `interface User { ⏎   id: number; ⏎   name: string; ⏎   greet?(): void;  -- 可选方法 ⏎ }` : dead
- `tools/it/typescript-cheatsheet.html` : `let el = document.querySelector("#x"); ⏎ el!.value;  -- 断言非空` : dead
- `tools/it/typescript-cheatsheet.html` : `let x: string | number = 1; ⏎ let y: "a" | "b" | "c" = "a";  -- 字面量联合` : dead
- `tools/it/typescript-cheatsheet.html` : `共 43 项` : dead
- `tools/it/url-qr.html` : `M（约 15%）最常用；打印尺寸小或物料易磨损时选 Q/H，代价是同样内容需要更高版本、模块更密。L 容量最大但容错最弱，适合屏幕展示。` : dead
- `tools/it/url-qr.html` : `'https://ex.com/a'（16 字节，纠错 M）→ 最小版本 V2（25×25 模块），矩阵可直接扫码。` : dead
- `tools/it/url-qr.html` : `是。链接越长字节数越大，版本与模块数随之上升，小尺寸打印时更难扫。可在保持最终落地页不变的前提下使用短链。` : dead
- `tools/it/url-qr.html` : `生成的是真二维码还是示意图？` : dead
- `tools/it/url-qr.html` : `真二维码。矩阵由本地 ISO/IEC 18004 编码器计算，包含 Reed-Solomon 纠错码字、格式信息与掩码；页面不联网、不上传网址，可直接用手机相机实扫验证。` : dead
- `tools/it/url-qr.html` : `纠错等级选哪个？` : dead
- `tools/it/vim-cheatsheet.html` : `"ayy  -- 复制行到寄存器 a ⏎ "ap  -- 粘贴寄存器 a ⏎ "+y  -- 复制到系统剪贴板 ⏎ "+p  -- 从系统剪贴板粘贴` : dead
- `tools/it/vim-cheatsheet.html` : `*  向下搜光标词 ⏎ #  向上搜光标词` : dead
- `tools/it/vim-cheatsheet.html` : `/function ⏎ n  下一个匹配 ⏎ N  上一个匹配` : dead
- `tools/it/vim-cheatsheet.html` : `:!ls ⏎ :!make test ⏎ :%!jq .  -- 格式化整个文件` : dead
- `tools/it/vim-cheatsheet.html` : `:e other.txt ⏎ :e!  -- 放弃修改重载` : dead
- `tools/it/vim-cheatsheet.html` : `:r other.txt  -- 插入文件内容 ⏎ :r! date  -- 插入命令输出` : dead
- `tools/it/vim-cheatsheet.html` : `:s/old/new/g  当前行全部 ⏎ :%s/old/new/g  全文件 ⏎ :%s/old/new/gc  全文件确认 ⏎ :5,10s/old/new/g  5-10 行` : dead
- `tools/it/vim-cheatsheet.html` : `:set number  -- 显示行号 ⏎ :set nonumber ⏎ :set tabstop=4 ⏎ :set expandtab ⏎ :set autoindent ⏎ :set hlsearch  -- 高亮搜索 ⏎ :set ignorecase  -- 忽略大小写 ⏎ :set paste  -- 粘…(+3字)` : dead
- `tools/it/vim-cheatsheet.html` : `:split  水平分割 ⏎ :vsplit  垂直分割 ⏎ Ctrl+w w  切换窗口 ⏎ :q  关闭当前窗口` : dead
- `tools/it/vim-cheatsheet.html` : `:tabnew ⏎ :tabnext  下个标签 ⏎ :tabprev  上个标签 ⏎ gt  下个标签 ⏎ gT  上个标签` : dead
- `tools/it/vim-cheatsheet.html` : `:w ⏎ :q ⏎ :wq ⏎ :q!  -- 不保存退出 ⏎ :x  -- 保存退出 ⏎ ZZ  -- 等价 :x ⏎ ZQ  -- 等价 :q!` : dead
- `tools/it/vim-cheatsheet.html` : `:w  保存 ⏎ :q  退出 ⏎ :wq 保存退出 ⏎ :q! 强制退出` : dead
- `tools/it/vim-cheatsheet.html` : `>G  缩进到文件末 ⏎ >>  缩进当前行 ⏎ <V  块选后取消缩进` : dead
- `tools/it/vim-cheatsheet.html` : `Ctrl+f  下一页 ⏎ Ctrl+b  上一页` : dead
- `tools/it/vim-cheatsheet.html` : `Ctrl+o  跳回上个位置 ⏎ Ctrl+i  跳到下个位置` : dead
- `tools/it/vim-cheatsheet.html` : `Ctrl+u  上半屏 ⏎ Ctrl+d  下半屏` : dead
- `tools/it/vim-cheatsheet.html` : `cw  改单词 ⏎ c$  改到行末 ⏎ cc  改整行` : dead
- `tools/it/vim-cheatsheet.html` : `dw  删到下个单词 ⏎ de  删到单词末尾 ⏎ d$  删到行末 ⏎ dd  删行 ⏎ dG  删到文件末` : dead
- `tools/it/vim-cheatsheet.html` : `gg  文件首 ⏎ G  文件末 ⏎ 100G  跳到 100 行` : dead
- `tools/it/vim-cheatsheet.html` : `h 左 ⏎ j 下 ⏎ k 上 ⏎ l 右` : dead
- `tools/it/vim-cheatsheet.html` : `i  光标前插入 ⏎ a  光标后插入 ⏎ I  行首插入 ⏎ A  行末插入 ⏎ o  下方新行 ⏎ O  上方新行` : dead
- `tools/it/vim-cheatsheet.html` : `ma  设置标记 a ⏎ 'a  跳到标记 a ⏎ 'a  跳到标记行首` : dead
- `tools/it/vim-cheatsheet.html` : `p  光标后粘贴 ⏎ P  光标前粘贴` : dead
- `tools/it/vim-cheatsheet.html` : `u  撤销 ⏎ Ctrl+r  重做` : dead
- `tools/it/vim-cheatsheet.html` : `v  字符选择 ⏎ V  行选择 ⏎ Ctrl+v  块选择` : dead
- `tools/it/vim-cheatsheet.html` : `vim file.txt ⏎ vim +100 file.txt  -- 跳到 100 行 ⏎ vim -R file.txt  -- 只读` : dead
- `tools/it/vim-cheatsheet.html` : `w  下个单词开头 ⏎ b  上个单词开头 ⏎ e  下个单词末尾` : dead
- `tools/it/vim-cheatsheet.html` : `x  删字符 ⏎ dd  删整行 ⏎ yy  复制整行 ⏎ 3dd  删 3 行 ⏎ 3yy  复制 3 行` : dead
- `tools/it/vim-cheatsheet.html` : `yw  复制单词 ⏎ y$  复制到行末 ⏎ yG  复制到文件末` : dead
- `tools/it/vim-cheatsheet.html` : `{  上个段落 ⏎ }  下个段落` : dead
- `tools/it/whitespace.html` : `因为行首空格（缩进）也属于空白字符：若选择了「合并连续空格为单个」或「去除每行首尾空白」，代码缩进与列表层级都会被去掉。处理代码或带结构文本时应关闭「去除每行首尾空白」、只压缩行内重复空格；建议先小段试处理，确认效果再全量应用。` : dead
- `tools/it/whitespace.html` : `清理示例` : dead
- `tools/it/whitespace.html` : `输入 "  a   b \n\n  c  "，勾选「去除行首尾空白」「删除空行」「合并连续空格为单个」后 → "a b\nc"；若再勾选「压成一行」则 → "a b c"。只勾选选项时页面结果区会同步给出字符数与空行数变化。` : dead
- `tools/it/xml-to-yaml.html` : `<note> ⏎   <to>Tony</to> ⏎   <from>Anna</from> ⏎   <heading>Reminder</heading> ⏎   <body>Don't forget me!<!-- TOOLBOX-DEEP-DIVE --> ⏎ <style> ⏎ .deep-dive{max-w…(+1836字)` : dead

  其它成因样例（共 2755 条，仅列前 5）：
  - `tools/it/ascii-art.html` : `Block 方块` : dynamic
  - `tools/it/ascii-art.html` : `Box 实心` : dynamic
  - `tools/it/bacon-cipher.html` : `0/1 编码` : dynamic
  - `tools/it/barcode-ean.html` : `请输入 12 或 13 位数字（EAN-13）` : dynamic
  - `tools/it/barcode-ean.html` : `输入含非数字字符，请只填写数字` : dynamic

### jewelry（dead 2 / dynamic 0 / fragment 0 / harmless 0）

- `tools/jewelry/gem-hardness.html` : `硬度≥7适合日常佩戴(耐刮擦)；硬度6-7需小心使用；硬度<6仅适合耳环、吊坠等不易碰撞的饰品，避免与硬物接触。` : dead
- `tools/jewelry/gem-hardness.html` : `较软 (<6)` : dead

### language（dead 10 / dynamic 33 / fragment 11 / harmless 0）

- `tools/language/calc-1.html` : `词汇量估算 = f(测试正确率, 词表)` : dead
- `tools/language/calc-2.html` : `阅读速度 = 字数 / 时间` : dead
- `tools/language/grammar-checker.html` : `密度 = 问题数 ÷ 句数。低于 0.5 通常可接受，0.5~1.5 建议逐句修订，高于 1.5 说明基础错误密集，建议先整体润色再逐条改。` : dead
- `tools/language/grammar-checker.html` : `按规则与统计模型双重检测：常见问题含中英文标点混用、句子成分缺失、主谓不一致、搭配不当、同一词在 20 字内重复出现；每处问题给出位置偏移与修改建议，问题密度 = 问题数 ÷ 总句数；改写建议按最小编辑距离优选；密度低于 0.5 属良好、0.5 至 1.5 建议局部修订、超过 1.5 需整体润色。` : dead
- `tools/language/grammar-checker.html` : `英文：常见拼写（teh、recieve、definately 等）、第三人称单数缺 -s、a/an 误用、your welcome、重复词；中文：中英标点混用、叠字、状语“的”应为“地”、动词补语“的”应为“得”、“在/再”混用。规则命中会给出来源片段与修改建议，不自动改写原文。` : dead
- `tools/language/grammar-checker.html` : `覆盖的检查类型` : dead
- `tools/language/grammar-checker.html` : `规则按词面模式匹配，对非常规但正确的句式（如倒装、专有名词、文学表达）可能误判；每条提示都注明命中的片段，请结合上下文判断。` : dead
- `tools/language/grammar-checker.html` : `规则检查只能抓规则表覆盖的明显硬错；语义、逻辑、搭配不当和长难句结构问题会漏检，规则也可能对非常规但正确的句式产生提示。重要文本仍需人工复核。` : dead
- `tools/language/grammar-checker.html` : `问题密度怎么用？` : dead
- `tools/language/stats-2.html` : `汉字数 + 英文单词数 + 数字字符数 + 标点数 + 空白符 = 总字符数` : dead

  其它成因样例（共 44 条，仅列前 5）：
  - `tools/language/calc-1.html` : `认识单词数：` : dynamic
  - `tools/language/calc-1.html` : `估算词汇量：` : dynamic
  - `tools/language/calc-1.html` : `估算区间（95%）：` : dynamic
  - `tools/language/calc-1.html` : `水平参考：` : dynamic
  - `tools/language/calc-1.html` : `区间按 20 个抽样词的二项标准误估算，结果为粗略参考。` : dynamic

### leather（dead 12 / dynamic 8 / fragment 3 / harmless 0）

- `tools/leather/area-20.html` : `💡 厚度分级：≥3.5mm 头层厚皮 / 1.2~3.5mm 头层 / 0.8~1.2mm 薄头层 / <0.8mm 二层；面积分级：≥25 大皮 / 15~25 中皮 / 8~15 小皮 / <8 碎皮` : dead
- `tools/leather/xueyunhoudukongzhi.html` : `不是。评分只按刀痕间距分档，反映参数组合的粗细程度；实际厚度精度还受刀片锋利度、皮张含水与张力影响，须用测厚仪多点实测抽检。` : dead
- `tools/leather/xueyunhoudukongzhi.html` : `为什么要求来料厚度大于目标厚度？` : dead
- `tools/leather/xueyunhoudukongzhi.html` : `刀片锋利度与刀距同样影响削匀质量` : dead
- `tools/leather/xueyunhoudukongzhi.html` : `刀痕间距 = 1000 × 进给速度 ÷ 转速（mm/rev）；切除量 = 来料厚度 − 目标厚度；评分按间距分档（≤0.5、≤1、≤2、≤4、>4 分别记 100、85、70、50、30）。例如进给 8 m/min、转速 4000 rpm → 间距 2.00 mm/rev → 70 分（一般）；转速提到 8000 r…(+31字)` : dead
- `tools/leather/xueyunhoudukongzhi.html` : `削匀只去除余量，来料必须留有余量才能达到目标厚度；相等或更薄时没有可切除材料，参数再优也无法成活。` : dead
- `tools/leather/xueyunhoudukongzhi.html` : `实际偏差须用测厚仪多点测量` : dead
- `tools/leather/xueyunhoudukongzhi.html` : `来料 2.0 mm、目标 1.2 mm、转速 4000 rpm、进给 8 m/min：切除量 0.80 mm，间距 1000×8÷4000 = 2.00 mm/rev，评分 70（一般）；同参数若转速降至 1200 rpm，间距 6.67 mm/rev，评分 30（不合格），建议提高转速或降低进给。注意评分只反映参数粗…(+11字)` : dead
- `tools/leather/xueyunhoudukongzhi.html` : `评分是实测均匀度吗？` : dead
- `tools/leather/xueyunhoudukongzhi.html` : `进给越快、转速不变时刀痕间距越大，单位长度内切削次数减少，易出现波纹与厚度不均；降低进给或提高转速可减小间距、改善表面平整度。` : dead
- `tools/leather/xueyunhoudukongzhi.html` : `高转速、低进给有利于均匀度` : dead
- `tools/leather/xueyunhoudukongzhi.html` : `💡 均匀度评分 = min(100, 转速÷进给速度×10)；厚度偏差 ≈ (100−评分)×0.05 mm` : dead

  其它成因样例（共 11 条，仅列前 5）：
  - `tools/leather/calc-dosage-4.html` : `硫化钠浓度须在 0–20% 之间（常温溶解度上限）` : dynamic
  - `tools/leather/calc-dosage-4.html` : `液比不得为负` : dynamic
  - `tools/leather/calc-dosage-4.html` : `皮重须大于 0` : fragment
  - `tools/leather/xueyunhoudukongzhi.html` : `刀痕间距 (mm/rev)` : fragment
  - `tools/leather/xueyunhoudukongzhi.html` : `切除量 (mm)` : fragment

### legal（dead 24 / dynamic 6 / fragment 6 / harmless 1）

- `tools/legal/arbitration-fee.html` : `仲裁费 = 标的×费率（分段）` : dead
- `tools/legal/calc-16.html` : `诉讼时效届满日 = 起算日 + 期间` : dead
- `tools/legal/estimate-salary.html` : `劳动争议赔偿 = 工资×年限×系数` : dead
- `tools/legal/food-safety.html` : `退一赔十 = 价款 × 10（或损失×3）` : dead
- `tools/legal/inheritance-share.html` : `继承份额 = 法定比例分配` : dead
- `tools/legal/ipr-damages.html` : `侵权赔偿 = 损失/获利/许可费` : dead
- `tools/legal/labor-compensation.html` : `经济补偿 = N × 月薪（封顶）` : dead
- `tools/legal/labor-compensation-n1.html` : `N+1 补偿 = (N+1) × 月薪` : dead
- `tools/legal/late-payment-interest.html` : `逾期利息 = 本金 × 日利率 × 天数` : dead
- `tools/legal/legal-age.html` : `法定年龄 = 当前 − 出生日期` : dead
- `tools/legal/legal-calculator.html` : `法律计算 = 通用公式` : dead
- `tools/legal/legal-reference.html` : `法律查询 = 条文匹配` : dead
- `tools/legal/loan-statute-limitations.html` : `借款时效 = 起算 + 3年` : dead
- `tools/legal/marriage-property-agreement.html` : `婚姻财产 = 共同/个人划分` : dead
- `tools/legal/notarization-fee.html` : `公证费 = 标的×费率` : dead
- `tools/legal/overtime-pay.html` : `加班费 = 基数 × 150%/200%/300%` : dead
- `tools/legal/patent-fee-calculator.html` : `专利费 = 年费×年度` : dead
- `tools/legal/patent-term-calculator.html` : `专利有效期 = 申请日 + 20年` : dead
- `tools/legal/personal-injury.html` : `人身损害 = 医疗费+误工+残疾` : dead
- `tools/legal/rent-deposit.html` : `租房押金 = 月租 × 倍数` : dead
- `tools/legal/severance-pay.html` : `违法解除 2N = 2N × 月薪` : dead
- `tools/legal/social-security-base.html` : `社保基数 = 工资（上下限）` : dead
- `tools/legal/stamp-duty-legal.html` : `印花税 = 金额 × 税率` : dead
- `tools/legal/statute-limitations.html` : `诉讼时效 = 起算 + 期间` : dead

  其它成因样例（共 13 条，仅列前 5）：
  - `tools/legal/calc-96.html` : `违约金 = 合同总额 × 违约金比例%` : fragment
  - `tools/legal/inheritance-share.html` : `配偶` : fragment
  - `tools/legal/inheritance-share.html` : `子女` : fragment
  - `tools/legal/jicheng-yizhu-gongzheng-yichan-fenpei.html` : `⚖️ 继承（遗嘱/公证/遗产）分配` : harmless
  - `tools/legal/lawyer-fee-reference.html` : `费用构成：` : dynamic

### library（dead 1 / dynamic 9 / fragment 2 / harmless 0）

- `tools/library/generator-label.html` : `档案盒脊背标签打印格式生成。免费在线工具，纯前端处理，数据不上传，保护隐私安全。` : dead

  其它成因样例（共 11 条，仅列前 5）：
  - `tools/library/generator-label.html` : `机构` : fragment
  - `tools/library/generator-label.html` : `标签行数` : dynamic
  - `tools/library/generator-label.html` : `字号` : fragment
  - `tools/library/generator-label.html` : `请至少填写一项标签内容。` : dynamic
  - `tools/library/generator-label.html` : `本次生成` : dynamic

### life（dead 254 / dynamic 62 / fragment 17 / harmless 0）

- `tools/life/age-calculator.html` : `周岁 = 今年 − 出生年（月/日/时/分/秒逐级借位修正）` : dead
- `tools/life/age-calculator.html` : `如何使用精确年龄计算器？` : dead
- `tools/life/age-calculator.html` : `精确年龄计算器是做什么的？` : dead
- `tools/life/age-calculator.html` : `精确年龄计算器适合哪些场景？` : dead
- `tools/life/age-in-days.html` : `如何使用年龄天数计算？` : dead
- `tools/life/age-in-days.html` : `年龄天数计算是做什么的？` : dead
- `tools/life/age-in-days.html` : `年龄天数计算适合哪些场景？` : dead
- `tools/life/analysis-23.html` : `如何使用景观（风水/视线）分析？` : dead
- `tools/life/analysis-23.html` : `景观（风水/视线）分析是做什么的？` : dead
- `tools/life/analysis-23.html` : `景观（风水/视线）分析适合哪些场景？` : dead
- `tools/life/analysis-74.html` : `如何使用竞争（分析/应对/差异化）？` : dead
- `tools/life/analysis-74.html` : `竞争（分析/应对/差异化）是做什么的？` : dead
- `tools/life/analysis-74.html` : `竞争（分析/应对/差异化）适合哪些场景？` : dead
- `tools/life/analysis-80.html` : `如何使用损耗（控制/分析/改善）体系？` : dead
- `tools/life/analysis-80.html` : `损耗（控制/分析/改善）体系是做什么的？` : dead
- `tools/life/analysis-80.html` : `损耗（控制/分析/改善）体系适合哪些场景？` : dead
- `tools/life/analysis-cost-10.html` : `如何使用成本（控制/分析/优化）体系？` : dead
- `tools/life/analysis-cost-10.html` : `成本（控制/分析/优化）体系是做什么的？` : dead
- `tools/life/analysis-cost-10.html` : `成本（控制/分析/优化）体系适合哪些场景？` : dead
- `tools/life/analysis-cost-9.html` : `不会自动识别科目。可在每行第三列手动标注「固定」或「变动」（也接受 F/V），工具据此拆分；不标则计入“未分类”，只做总量与占比统计。` : dead
- `tools/life/analysis-cost-9.html` : `原料 42（变动）、人工 31（固定）、物流 15（变动）、能耗 9（固定）：合计 97，固定 40（41.24%）、变动 57（58.76%）。若产量 1000、单价 0.12，则单位成本 0.0970、单位变动成本 0.0570、边际贡献 0.0630，盈亏平衡产量 = 40 ÷ 0.0630 ≈ 634.9，当前…(+57字)` : dead
- `tools/life/analysis-cost-9.html` : `可按部门或产品线分次贴入分别统计，再横向比较占比；同一次统计内保持科目口径一致。` : dead
- `tools/life/analysis-cost-9.html` : `固定/变动拆解与盈亏平衡` : dead
- `tools/life/analysis-cost-9.html` : `在第三列标注「固定/变动」，拆出固定成本与变动成本，算出单位成本与盈亏平衡产量。` : dead
- `tools/life/analysis-cost-9.html` : `如何使用成本（控制/优化/分析）体系？` : dead
- `tools/life/analysis-cost-9.html` : `成本（控制/优化/分析）体系是做什么的？` : dead
- `tools/life/analysis-cost-9.html` : `成本（控制/优化/分析）体系适合哪些场景？` : dead
- `tools/life/analysis-cost-9.html` : `把各项成本金额贴入，看合计、均值与占比最大的成本项。` : dead
- `tools/life/analysis-cost-9.html` : `盈亏平衡产量为什么显示“—”？` : dead
- `tools/life/analysis-cost-9.html` : `需要同时填写产量与单价，且单价必须高于单位变动成本；否则边际贡献 ≤ 0，任何产量都无法覆盖固定成本，页面会给出提示。` : dead
- `tools/life/angle-converter.html` : `如何使用角度换算？` : dead
- `tools/life/angle-converter.html` : `角度换算是做什么的？` : dead
- `tools/life/angle-converter.html` : `角度换算适合哪些场景？` : dead
- `tools/life/area-converter.html` : `如何使用面积换算？` : dead
- `tools/life/area-converter.html` : `面积换算是做什么的？` : dead
- `tools/life/area-converter.html` : `面积换算适合哪些场景？` : dead
- `tools/life/assessor-target.html` : `A 铺：人流 8000、竞争 2 家、人口 3 万、租金 120 元/m²、可见性 8 分 → 综合约 82 分（优秀）；B 铺：人流 3000、竞争 5 家、人口 1 万、租金 200 元/m²、可见性 5 分 → 约 48 分（一般）；在资源有限时优先洽谈 A 铺。` : dead
- `tools/life/assessor-target.html` : `按人流量、竞争密度、常住人口、租金、可见性五维加权评分输出综合分与选址等级（A/B/C）；模型量化选址要素，结果为网点布局决策参考，最终盈利还看选品与运营。` : dead
- `tools/life/assessor-target.html` : `无冲突排课率` : dead
- `tools/life/assessor-target.html` : `某铺租金 260 元/m²（得分较低），但人流、人口与可见性均接近满分，综合仍达 70 分；说明高租金可由强客流部分抵消，不应只凭租金一项否决。` : dead
- `tools/life/assessor-target.html` : `页面内置经验权重：人流 30%、竞争 20%、人口 20%、租金 15%、可见性 15%；业态不同时可据此判断偏重，是否调整以自身经营经验为准。` : dead
- `tools/life/base-convert.html` : `如何使用进制转换器？` : dead
- `tools/life/base-convert.html` : `进制转换器是做什么的？` : dead
- `tools/life/base-convert.html` : `进制转换器适合哪些场景？` : dead
- `tools/life/bill-splitter.html` : `AA制账单分摊是做什么的？` : dead
- `tools/life/bill-splitter.html` : `AA制账单分摊适合哪些场景？` : dead
- `tools/life/bill-splitter.html` : `如何使用AA制账单分摊？` : dead
- `tools/life/birthday-paradox.html` : `如何使用生日悖论计算器？` : dead
- `tools/life/birthday-paradox.html` : `生日悖论计算器是做什么的？` : dead
- `tools/life/birthday-paradox.html` : `生日悖论计算器适合哪些场景？` : dead
- `tools/life/bra-size-converter.html` : `如何使用罩杯尺寸换算？` : dead
- `tools/life/bra-size-converter.html` : `罩杯尺寸换算是做什么的？` : dead
- `tools/life/bra-size-converter.html` : `罩杯尺寸换算适合哪些场景？` : dead
- `tools/life/chinese-number.html` : `中文数字转换是做什么的？` : dead
- `tools/life/chinese-number.html` : `中文数字转换适合哪些场景？` : dead
- `tools/life/chinese-number.html` : `如何使用中文数字转换？` : dead
- `tools/life/chinese-number.html` : `简体/大写支持「点」逐位小数，负数前置「负」` : dead
- `tools/life/chinese-number.html` : `金额：阿拉伯数字 → 人民币大写，金额末尾加"元整"` : dead
- `tools/life/clothing-size-converter.html` : `如何使用服装尺码换算？` : dead
- `tools/life/clothing-size-converter.html` : `服装尺码换算是做什么的？` : dead
- `tools/life/clothing-size-converter.html` : `服装尺码换算适合哪些场景？` : dead
- `tools/life/color-name-finder.html` : `如何使用颜色名称查询？` : dead
- `tools/life/color-name-finder.html` : `颜色名称查询是做什么的？` : dead
- `tools/life/color-name-finder.html` : `颜色名称查询适合哪些场景？` : dead
- `tools/life/concentration-converter.html` : `如何使用浓度换算？` : dead
- `tools/life/concentration-converter.html` : `浓度换算是做什么的？` : dead
- `tools/life/concentration-converter.html` : `浓度换算适合哪些场景？` : dead
- `tools/life/countdown.html` : `倒计时器（设置日期）是做什么的？` : dead
- `tools/life/countdown.html` : `倒计时器（设置日期）适合哪些场景？` : dead
- `tools/life/countdown.html` : `如何使用倒计时器（设置日期）？` : dead
- `tools/life/countdown-1.html` : `如何使用计时器（正计时/倒计时）？` : dead
- `tools/life/countdown-1.html` : `计时器（正计时/倒计时）是做什么的？` : dead
- `tools/life/countdown-1.html` : `计时器（正计时/倒计时）适合哪些场景？` : dead
- `tools/life/countdown-2.html` : `如何使用纪念日倒计时（多组）？` : dead
- `tools/life/countdown-2.html` : `纪念日倒计时（多组）是做什么的？` : dead
- `tools/life/countdown-2.html` : `纪念日倒计时（多组）适合哪些场景？` : dead
- `tools/life/countdown-timer.html` : `多功能倒计时器是做什么的？` : dead
- `tools/life/countdown-timer.html` : `多功能倒计时器适合哪些场景？` : dead
- `tools/life/countdown-timer.html` : `如何使用多功能倒计时器？` : dead
- `tools/life/cycle-4.html` : `如何使用清洁用品消耗量与补货周期？` : dead
- `tools/life/cycle-4.html` : `清洁用品消耗量与补货周期是做什么的？` : dead
- `tools/life/cycle-4.html` : `清洁用品消耗量与补货周期适合哪些场景？` : dead
- `tools/life/cycle-pruning-lawn.html` : `如何使用草坪（修剪/养护）周期？` : dead
- `tools/life/cycle-pruning-lawn.html` : `景观（风水/视线）分析` : dead
- `tools/life/cycle-pruning-lawn.html` : `草坪（修剪/养护）周期是做什么的？` : dead
- `tools/life/cycle-pruning-lawn.html` : `草坪（修剪/养护）周期适合哪些场景？` : dead
- `tools/life/daily-calorie-needs.html` : `体脂率改用 Deurenberg 公式（男 1.20×BMI + 0.23×年龄 − 16.2；女 1.20×BMI + 0.23×年龄 − 5.4），限 2%–60%` : dead
- `tools/life/daily-calorie-needs.html` : `卡路里计算器是做什么的？` : dead
- `tools/life/daily-calorie-needs.html` : `卡路里计算器适合哪些场景？` : dead
- `tools/life/daily-calorie-needs.html` : `如何使用卡路里计算器？` : dead
- `tools/life/daily-calorie-needs.html` : `默认 Mifflin-St Jeor 公式，另可选 Harris-Benedict（男 66.5+13.75W+5.003H−6.755A）与 Katch-McArdle（370+21.6×去脂体重，体脂率用 Deurenberg Formula:男 1.20×BMI+0.23×年龄−16.2、女 1.20×BMI+0…(+60字)` : dead
- `tools/life/daily-calorie-needs.html` : `默认 Mifflin-St Jeor 公式，另可选 Harris-Benedict（男 66.5+13.75W+5.003H−6.755A）与 Katch-McArdle（370+21.6×去脂体重，先用 BMI 估算体脂率）。每日目标摄入 = TDEE + 目标差额（减脂/维持/增肌），数值为估算参考。` : dead
- `tools/life/data-rate-converter.html` : `如何使用数据速率换算？` : dead
- `tools/life/data-rate-converter.html` : `数据速率换算是做什么的？` : dead
- `tools/life/data-rate-converter.html` : `数据速率换算适合哪些场景？` : dead
- `tools/life/data-unit-converter.html` : `如何使用数据存储单位换算？` : dead
- `tools/life/data-unit-converter.html` : `数据存储单位换算是做什么的？` : dead
- `tools/life/data-unit-converter.html` : `数据存储单位换算适合哪些场景？` : dead
- `tools/life/date-add-subtract.html` : `如何使用日期加减？` : dead
- `tools/life/date-add-subtract.html` : `日/时/分/秒按时间戳精确加减` : dead
- `tools/life/date-add-subtract.html` : `日期加减是做什么的？` : dead
- `tools/life/date-add-subtract.html` : `日期加减适合哪些场景？` : dead
- `tools/life/date-add-subtract.html` : `目标日期 = 基准日期 + 年、月、日、时、分、秒增量（负数表示减）；先加年月并处理月末溢出（如 1 月 31 日加 1 月取 2 月末），再累加天数自动跨月跨年，最后按秒数补时分秒；闰年 2 月为 29 天须在跨月时校正。` : dead
- `tools/life/date-diff.html` : `如何使用日期差计算？` : dead
- `tools/life/date-diff.html` : `日期差计算是做什么的？` : dead
- `tools/life/date-diff.html` : `日期差计算适合哪些场景？` : dead
- `tools/life/date-difference-calculator.html` : `如何使用日期差计算器？` : dead
- `tools/life/date-difference-calculator.html` : `日期差计算器是做什么的？` : dead
- `tools/life/date-difference-calculator.html` : `日期差计算器适合哪些场景？` : dead
- `tools/life/density-converter.html` : `关于「密度换算器」` : dead
- `tools/life/detector-checker-strength.html` : `如何使用强密码检测器（检查强度）？` : dead
- `tools/life/detector-checker-strength.html` : `密码强度评分 = 长度分（不足 8 位 0 分、8 至 11 位 10 分、12 至 15 位 20 分、16 位及以上 30 分）+ 字符集分（大写 15 分、小写 15 分、数字 15 分、符号 25 分）− 惩罚项（连续或重复字符、弱口令字典命中）；总分 0 至 100 对应很弱至很强五级。` : dead
- `tools/life/detector-checker-strength.html` : `强密码检测器（检查强度）是做什么的？` : dead
- `tools/life/detector-checker-strength.html` : `强密码检测器（检查强度）适合哪些场景？` : dead
- `tools/life/drinking-water-plan.html` : `关于「喝水提醒计划计算器」` : dead
- `tools/life/drinking-water-plan.html` : `喝水提醒计划计算器是做什么的？` : dead
- `tools/life/drinking-water-plan.html` : `喝水提醒计划计算器适合哪些场景？` : dead
- `tools/life/drinking-water-plan.html` : `如何使用喝水提醒计划计算器？` : dead
- `tools/life/drinking-water-plan.html` : `饮水目标 = 体重×30ml + 运动增量 + 高温增量 + 特殊增量` : dead
- `tools/life/energy-converter.html` : `如何使用能量换算？` : dead
- `tools/life/energy-converter.html` : `能量换算是做什么的？` : dead
- `tools/life/energy-converter.html` : `能量换算适合哪些场景？` : dead
- `tools/life/event-countdown.html` : `如何使用节日倒计时？` : dead
- `tools/life/event-countdown.html` : `节日倒计时是做什么的？` : dead
- `tools/life/event-countdown.html` : `节日倒计时适合哪些场景？` : dead
- `tools/life/flow-rate-converter.html` : `如何使用流量换算？` : dead
- `tools/life/flow-rate-converter.html` : `流量换算是做什么的？` : dead
- `tools/life/flow-rate-converter.html` : `流量换算适合哪些场景？` : dead
- `tools/life/frequency-converter.html` : `如何使用频率换算？` : dead
- `tools/life/frequency-converter.html` : `频率换算是做什么的？` : dead
- `tools/life/frequency-converter.html` : `频率换算适合哪些场景？` : dead
- `tools/life/generator-price.html` : `合同（服务/价格/条款）生成是做什么的？` : dead
- `tools/life/generator-price.html` : `合同（服务/价格/条款）生成适合哪些场景？` : dead
- `tools/life/generator-price.html` : `如何使用合同（服务/价格/条款）生成？` : dead
- `tools/life/generator-random-1.html` : `如何使用随机数生成器（范围任意）？` : dead
- `tools/life/generator-random-1.html` : `随机数生成器（范围任意）是做什么的？` : dead
- `tools/life/generator-random-1.html` : `随机数生成器（范围任意）适合哪些场景？` : dead
- `tools/life/generator-strength.html` : `如何使用密码生成器（带强度检测）？` : dead
- `tools/life/generator-strength.html` : `字符种类统计小写/大写/数字/符号四类中出现的种数。并设上限修正：长度 <8 位分数封顶 30、<6 位封顶 15、仅含一类字符封顶 25。按总分分档：<30 弱、<55 中、<80 强、其余很强。字符池由勾选项决定，可进一步排除相似字符 0O1lI 与歧义字符。` : dead
- `tools/life/generator-strength.html` : `密码生成器（带强度检测）是做什么的？` : dead
- `tools/life/generator-strength.html` : `密码生成器（带强度检测）适合哪些场景？` : dead
- `tools/life/holiday-calendar.html` : `关于「节假日日历」` : dead
- `tools/life/holiday-calendar.html` : `如何使用节假日日历？` : dead
- `tools/life/holiday-calendar.html` : `节假日日历是做什么的？` : dead
- `tools/life/holiday-calendar.html` : `节假日日历适合哪些场景？` : dead
- `tools/life/leap-year-checker.html` : `如何使用闰年检查器？` : dead
- `tools/life/leap-year-checker.html` : `闰年检查器是做什么的？` : dead
- `tools/life/leap-year-checker.html` : `闰年检查器适合哪些场景？` : dead
- `tools/life/length-converter.html` : `关于「长度换算器」` : dead
- `tools/life/length-converter.html` : `目标单位：` : dead
- `tools/life/magnet-converter.html` : `关于「磁场强度换算器」` : dead
- `tools/life/music-practice-timer.html` : `如何使用音乐练习计时器？` : dead
- `tools/life/music-practice-timer.html` : `音乐练习计时器是做什么的？` : dead
- `tools/life/music-practice-timer.html` : `音乐练习计时器适合哪些场景？` : dead
- `tools/life/number-to-chinese.html` : `→ 一十` : dead
- `tools/life/number-to-chinese.html` : `如何使用数字转中文？` : dead
- `tools/life/number-to-chinese.html` : `数字转中文是做什么的？` : dead
- `tools/life/number-to-chinese.html` : `数字转中文适合哪些场景？` : dead
- `tools/life/parking-fee.html` : `停车费 = 计费时长 × 每小时费率，计费时长 = 停放时长 − 免费时长（不足 1 小时按 1 小时计或按分钟折算）；每日封顶时按自然日分组取较小值（当日费用与封顶价）后累加；跨日停放逐日分别计费再求和。` : dead
- `tools/life/parking-fee.html` : `停车费计算器是做什么的？` : dead
- `tools/life/parking-fee.html` : `停车费计算器适合哪些场景？` : dead
- `tools/life/parking-fee.html` : `免费时长（小时）` : dead
- `tools/life/parking-fee.html` : `关于「停车费计算器」` : dead
- `tools/life/parking-fee.html` : `如何使用停车费计算器？` : dead
- `tools/life/percentage-calculator.html` : `如何使用百分比计算器？` : dead
- `tools/life/percentage-calculator.html` : `百分比计算器是做什么的？` : dead
- `tools/life/percentage-calculator.html` : `百分比计算器适合哪些场景？` : dead
- `tools/life/phone-lookup.html` : `归一化去空格 / 连字符 / 括号 / 点；带 + 时按国家码库 3→1 位前缀匹配；不带 + 时：^1[3-9]\d{9}$ 推断中国大陆手机（第 4 位映射运营商），^0\d{10,11}$ 判固话（010 / 02x 取 2 位区号，其余按 3–4 位区号匹配号段表，绝不把号码首位并入区号）` : dead
- `tools/life/power-converter.html` : `关于「功率换算器」` : dead
- `tools/life/power-converter.html` : `功率换算器是做什么的？` : dead
- `tools/life/power-converter.html` : `功率换算器适合哪些场景？` : dead
- `tools/life/power-converter.html` : `如何使用功率换算器？` : dead
- `tools/life/pressure-converter.html` : `关于「压力换算器」` : dead
- `tools/life/pressure-converter.html` : `压力换算器是做什么的？` : dead
- `tools/life/pressure-converter.html` : `压力换算器适合哪些场景？` : dead
- `tools/life/pressure-converter.html` : `如何使用压力换算器？` : dead
- `tools/life/radiation-converter.html` : `关于「辐射剂量换算器」` : dead
- `tools/life/recommender-8.html` : `保险（责任/意外/雇主）推荐是做什么的？` : dead
- `tools/life/recommender-8.html` : `保险（责任/意外/雇主）推荐适合哪些场景？` : dead
- `tools/life/recommender-8.html` : `如何使用保险（责任/意外/雇主）推荐？` : dead
- `tools/life/reminder-cycle.html` : `如何使用家电深度清洁周期提醒？` : dead
- `tools/life/reminder-cycle.html` : `家电深度清洁周期提醒是做什么的？` : dead
- `tools/life/reminder-cycle.html` : `家电深度清洁周期提醒适合哪些场景？` : dead
- `tools/life/report-profit.html` : `如何使用财务（利润/现金流/报表）核算？` : dead
- `tools/life/report-profit.html` : `财务（利润/现金流/报表）核算是做什么的？` : dead
- `tools/life/report-profit.html` : `财务（利润/现金流/报表）核算适合哪些场景？` : dead
- `tools/life/ring-size-converter.html` : ` mm（直径 ` : dead
- `tools/life/ring-size-converter.html` : `中国港码：` : dead
- `tools/life/ring-size-converter.html` : `关于「戒指尺寸换算器」` : dead
- `tools/life/ring-size-converter.html` : `周长(mm)：` : dead
- `tools/life/ring-size-converter.html` : `如何使用戒指尺寸换算器？` : dead
- `tools/life/ring-size-converter.html` : `意码：` : dead
- `tools/life/ring-size-converter.html` : `戒指尺寸换算器是做什么的？` : dead
- `tools/life/ring-size-converter.html` : `戒指尺寸换算器适合哪些场景？` : dead
- `tools/life/ring-size-converter.html` : `欧码：` : dead
- `tools/life/ring-size-converter.html` : `直径(mm)：` : dead
- `tools/life/ring-size-converter.html` : `美码：` : dead
- `tools/life/ring-size-converter.html` : `英码：` : dead
- `tools/life/roman-numeral.html` : `如何使用罗马数字转换？` : dead
- `tools/life/roman-numeral.html` : `罗马数字转换是做什么的？` : dead
- `tools/life/roman-numeral.html` : `罗马数字转换适合哪些场景？` : dead
- `tools/life/shoe-size-converter.html` : `中国码 CN = 脚长 mm / 10 （如 250mm → 25）` : dead
- `tools/life/shoe-size-converter.html` : `关于「鞋码换算器」` : dead
- `tools/life/shoe-size-converter.html` : `如何使用鞋码换算器？` : dead
- `tools/life/shoe-size-converter.html` : `欧盟码 EU ≈ 1.5 × (脚长 cm + 2)（如 25cm → 41）` : dead
- `tools/life/shoe-size-converter.html` : `注：各品牌存在 0.5-1 码差异，建议以品牌对照表为准` : dead
- `tools/life/shoe-size-converter.html` : `美码女 US ≈ 0.847 × 脚长 cm - 18.4` : dead
- `tools/life/shoe-size-converter.html` : `美码男 US ≈ 0.847 × 脚长 cm - 17.6（约 7-12 常见）` : dead
- `tools/life/shoe-size-converter.html` : `英码 UK ≈ 美码男 - 1` : dead
- `tools/life/shoe-size-converter.html` : `鞋码按脚长换算：中国码 CN = 脚长(mm) ÷ 10（250 mm 对应 CN 250 即 40 码）；欧洲码 EU ≈ 脚长(cm) × 1.5 + 2；美国码与英国码在欧码基础上按性别减约 33 至 34（EU 40 约合 US 男 7 号、女 8.5 号）；建议以脚跟至最长脚趾的实测长度选码并预留 5 至 1…(+5字)` : dead
- `tools/life/shoe-size-converter.html` : `鞋码换算器是做什么的？` : dead
- `tools/life/shoe-size-converter.html` : `鞋码换算器适合哪些场景？` : dead
- `tools/life/speed-converter.html` : `关于「速度换算器」` : dead
- `tools/life/speed-converter.html` : `如何使用速度换算器？` : dead
- `tools/life/speed-converter.html` : `速度换算器是做什么的？` : dead
- `tools/life/speed-converter.html` : `速度换算器适合哪些场景？` : dead
- `tools/life/stats-13.html` : `如何使用预售（发布/接龙/统计）工具？` : dead
- `tools/life/stats-13.html` : `库存与发车预备` : dead
- `tools/life/stats-13.html` : `报名付款聚合` : dead
- `tools/life/stats-13.html` : `时段峰值识别` : dead
- `tools/life/stats-13.html` : `聚合报名、付款与时段分布，输出转化漏斗与参与结构，辅助活动节奏与备货。` : dead
- `tools/life/stats-13.html` : `转化流失定位` : dead
- `tools/life/stats-13.html` : `转化漏斗分层` : dead
- `tools/life/stats-13.html` : `预售报名统计` : dead
- `tools/life/stats-13.html` : `预售（发布/接龙/统计）工具是做什么的？` : dead
- `tools/life/stats-13.html` : `预售（发布/接龙/统计）工具适合哪些场景？` : dead
- `tools/life/temperature-converter.html` : `如何使用温度转换器？` : dead
- `tools/life/temperature-converter.html` : `温度转换器是做什么的？` : dead
- `tools/life/temperature-converter.html` : `温度转换器适合哪些场景？` : dead
- `tools/life/time-converter.html` : `关于「时间换算器」` : dead
- `tools/life/time-converter.html` : `如何使用时间换算器？` : dead
- `tools/life/time-converter.html` : `时间换算器是做什么的？` : dead
- `tools/life/time-converter.html` : `时间换算器适合哪些场景？` : dead
- `tools/life/unit-converter.html` : `结果 = 数值 × 源单位因子 ÷ 目标单位因子（温度走专用换算）` : dead
- `tools/life/volume-converter.html` : `关于「体积换算器」` : dead
- `tools/life/weight-converter.html` : `关于「重量换算器」` : dead
- `tools/life/weight-converter.html` : `如何使用重量换算器？` : dead
- `tools/life/weight-converter.html` : `重量换算器是做什么的？` : dead
- `tools/life/weight-converter.html` : `重量换算器适合哪些场景？` : dead
- `tools/life/workday-calculator.html` : `含起始日，不含结束日（如周一到周五 = 5 个工作日）` : dead
- `tools/life/workday-calculator.html` : `如何使用工作日计算器？` : dead
- `tools/life/workday-calculator.html` : `工作日数 = 区间总天数 − 周末天数 − 自定义节假日天数（按选项决定是否排除周六、周日）；总天数 =（结束日期 − 开始日期）÷ 86400000 + 1（含首尾两天）；逐日遍历统计可识别调休与自定义假日，用于工期与考勤估算。` : dead
- `tools/life/workday-calculator.html` : `工作日计算器是做什么的？` : dead
- `tools/life/workday-calculator.html` : `工作日计算器适合哪些场景？` : dead
- `tools/life/workday-calculator.html` : `自定义节假日：列出法定调休日（如国庆、春节假期）` : dead
- `tools/life/workday-calculator.html` : `自定义额外节假日（每行一个日期，格式 YYYY-MM-DD）` : dead
- `tools/life/workday-calculator.html` : `若需要调休上班（周末补班），请取消对应周末的勾选` : dead
- `tools/life/world-clock.html` : `世界时钟是做什么的？` : dead
- `tools/life/world-clock.html` : `世界时钟适合哪些场景？` : dead
- `tools/life/world-clock.html` : `如何使用世界时钟？` : dead
- `tools/life/zodiac-calculator.html` : `Note:本工具按公历年份估算，1-2 月初出生者可能需按农历调整` : dead
- `tools/life/zodiac-calculator.html` : `如何使用生肖星座计算？` : dead
- `tools/life/zodiac-calculator.html` : `生肖星座计算是做什么的？` : dead
- `tools/life/zodiac-calculator.html` : `生肖星座计算适合哪些场景？` : dead

  其它成因样例（共 79 条，仅列前 5）：
  - `tools/life/age-in-days.html` : `请输入有效日期（YYYY-MM-DD）` : dynamic
  - `tools/life/age-in-days.html` : `距离下一个生日：` : dynamic
  - `tools/life/age-in-days.html` : `天` : fragment
  - `tools/life/age-in-days.html` : `（今天）` : dynamic
  - `tools/life/age-in-days.html` : `出生日期不能晚于今天` : dynamic

### livestock（dead 5 / dynamic 15 / fragment 6 / harmless 0）

- `tools/livestock/ammonia-ventilation.html` : `c2 由 15 降至 10 ppm：Q 增到约 110 次/分。` : dead
- `tools/livestock/ammonia-ventilation.html` : `舍容 1800 m³（50×12×3），η=0.6：Q=V·ln(c1/c2)/(t·η)=1800×ln(40/15)/0.6≈2943 m³/s，换气约 98 次/分。` : dead
- `tools/livestock/analysis-18.html` : `料蛋比 = 耗料总量 ÷ 产蛋总重` : dead
- `tools/livestock/mycotoxin-limit.html` : `本工具仔猪料 ZEA 限量按 250 μg/kg 计，实测 150 为限量的 60%，判合格；若按更严格的地方/企业标准（如 100 μg/kg）则应判超标，实际判定请以现行 GB 13078 与当地法规为准。` : dead
- `tools/livestock/stats-7.html` : `需助产率 = (轻度助产 + 难产) ÷ 产犊总数 × 100%` : dead

  其它成因样例（共 21 条，仅列前 5）：
  - `tools/livestock/ammonia-ventilation.html` : `维持通风量(m³/h)` : dynamic
  - `tools/livestock/ammonia-ventilation.html` : `维持通风量(产氨)` : dynamic
  - `tools/livestock/analysis-18.html` : `产蛋率 = 产蛋总数 ÷ (存栏鸡数 × 统计天数) × 100%` : fragment
  - `tools/livestock/calving-interval.html` : `请输入有效的上次产犊日期` : dynamic
  - `tools/livestock/calving-interval.html` : `请输入有效的配种日期` : dynamic

### logistics（dead 3 / dynamic 0 / fragment 0 / harmless 0）

- `tools/logistics/checker-4.html` : `≥90% 流程完善，75-89% 基本完善，60-74% 待改进，<60% 需重建` : dead
- `tools/logistics/load-calculator.html` : `利用率 <70% 提示调整包装尺寸；输入箱尺寸格式 L×W×H` : dead
- `tools/logistics/load-calculator.html` : `限制因素 = 体积实际箱数 < 重量限制箱数 时取体积，否则重量` : dead

### logistics2（dead 4 / dynamic 10 / fragment 8 / harmless 0）

- `tools/logistics2/loading-utilization.html` : `为什么枚举 6 种摆放取向？` : dead
- `tools/logistics2/loading-utilization.html` : `最大可装件数（体积侧）：对 6 种正交摆放取向（长宽高三边全排列）分别计算 floor(车厢长÷第一边)×floor(车厢宽÷第二边)×floor(车厢高÷第三边)，取六者最大值作为体积上限。` : dead
- `tools/logistics2/loading-utilization.html` : `输入：车厢 6.8×2.3×2.4 m（容积 37.536 m³）、载重 5000 kg；纸箱 0.6×0.4×0.5 m（单件 0.12 m³）、单件 15 kg；计划 500 件。六种取向：(0.6,0.4,0.5)→11×5×4=220 件、(0.6,0.5,0.4)→11×4×5=220 件、(0.4,0.6,…(+330字)` : dead
- `tools/logistics2/loading-utilization.html` : `长方体正交摆放有 6 种三边分配方式，全部枚举后取最大值，避免只试 3 种时低估可装件数（例如把较长边放到车厢长度方向反而能多装）。若货物不允许倒置（如带向上标识的箱体），可手工剔除把原高边转到竖直方向的取向。` : dead

  其它成因样例（共 18 条，仅列前 5）：
  - `tools/logistics2/storage-allocation.html` : `合计` : fragment
  - `tools/logistics2/storage-allocation.html` : `A 类` : fragment
  - `tools/logistics2/storage-allocation.html` : `B 类` : fragment
  - `tools/logistics2/storage-allocation.html` : `C 类` : fragment
  - `tools/logistics2/storage-allocation.html` : `合计校验：` : dynamic

### machinery（dead 47 / dynamic 127 / fragment 9 / harmless 6）

- `tools/machinery/area-dosage-1.html` : `涂装用量 = 面积 × 膜厚 × 密度` : dead
- `tools/machinery/banjinzhewanzhankai.html` : `展开长度 = 中性层 + 折弯补偿` : dead
- `tools/machinery/banjinzhewanzhankai.html` : `当 R/t < 0.5 时可能产生裂纹，应增大内圆角半径` : dead
- `tools/machinery/banjinzhewanzhankai.html` : `翼缘长度 A、B 为从外边到切点的距离，留 0 可仅计算弯角参数` : dead
- `tools/machinery/bearing.html` : `轴承补油/换油周期依据 dn 值（d×n）与润滑方式估算` : dead
- `tools/machinery/calc-64.html` : `装配间隙/过盈 = 公差配合` : dead
- `tools/machinery/calc-89.html` : `离合器转矩 T = μ·F·R·Z` : dead
- `tools/machinery/calc-gear.html` : `标准齿轮 d = m·z` : dead
- `tools/machinery/calc-gear-1.html` : `齿轮模数 m = d/z` : dead
- `tools/machinery/calc-gear-3.html` : `齿轮参数 = 标准模数系列` : dead
- `tools/machinery/calc-lifespan-belt.html` : `皮带寿命 = f(张力, 转速)` : dead
- `tools/machinery/calc-strength.html` : `轴强度 σ = M/W` : dead
- `tools/machinery/drive-2.html` : `蜗杆效率 η = tanλ/tan(λ+ρ)` : dead
- `tools/machinery/energy-2.html` : `制动能耗 = ½J(ω₁² − ω₂²)` : dead
- `tools/machinery/estimate-gravity.html` : `重心 = Σ(m_i·x_i)/Σm_i` : dead
- `tools/machinery/fengjixuanxingjisuan.html` : `风量 Q (m³/h)、全压 p (Pa) 定工况；选型匹配性能曲线` : dead
- `tools/machinery/gear.html` : `齿轮设计 = 强度/几何计算` : dead
- `tools/machinery/gongyebengxuanxing.html` : `安装校核：高扬程注意汽蚀余量 NPSH` : dead
- `tools/machinery/gongyebengxuanxing.html` : `污染` : dead
- `tools/machinery/gongyebengxuanxing.html` : `汽蚀余量评估与转速推荐` : dead
- `tools/machinery/index.html` : `机械制造工具集合收录了 35 个免费在线工具，覆盖机械制造场景下的常见计算、换算与查询需求。无论你是相关领域的从业者、学生还是普通用户，都能在这里找到即用即走的实用小工具。所有工具纯前端运行，数据不上传服务器，保护隐私安全。` : dead
- `tools/machinery/jingmishebeixuanxing.html` : `依据定位精度、负载、行程、移动速度选直线导轨(HGR)与滚珠丝杠` : dead
- `tools/machinery/lifespan-20.html` : `L₁₀ = (C/P)^p（ISO 281），并计精度因子与润滑因子` : dead
- `tools/machinery/lifespan-bearing.html` : `轴承寿命 L10 = (C/P)^p` : dead
- `tools/machinery/lifespan-bearing-1.html` : `轴承额定动载 C = f(寿命, 转速)` : dead
- `tools/machinery/power-16.html` : `依据传递功率 P、主动轮转速 n₁ 与传动比 i 选带型与带轮直径` : dead
- `tools/machinery/power-voltage.html` : `P = F · v / η；推荐标准电机功率等级与极数` : dead
- `tools/machinery/pressure-4.html` : `花键挤压 σ = F/(d·l·z)` : dead
- `tools/machinery/pressure-flow-4.html` : `比功率 = 轴功率 ÷ 排气量；能效对照 GB 19153` : dead
- `tools/machinery/pressure-flow-5.html` : `Cv = Q × √(ρ/ΔP) × 换算系数；口径按 Cv 选标准通径` : dead
- `tools/machinery/runhuaxitongsheji.html` : `润滑油量 = f(功率, 转速)` : dead
- `tools/machinery/shusongdaixuanxingjisuan.html` : `带宽 ≈ Q ÷ (ρ × 带速 × 填充系数)，向上取整至标准规格` : dead
- `tools/machinery/strength-15.html` : `链条拉力 = 功率/速度` : dead
- `tools/machinery/strength-6.html` : `键强度 = 挤压/剪切校核` : dead
- `tools/machinery/strength-7.html` : `铆接剪切 τ = F/(n·πd²/4)` : dead
- `tools/machinery/stretch.html` : `弹簧刚度 k = G·d⁴/(8D³n)` : dead
- `tools/machinery/tanhuangsheji.html` : `弹簧设计 k = G·d⁴/(8D³n)` : dead
- `tools/machinery/temp-hardness.html` : `热处理硬度 = f(温度, 冷却)` : dead
- `tools/machinery/thread-4.html` : `H = 0.866×P（理论）；H₁ ≈ 0.5413×P（实际牙高）` : dead
- `tools/machinery/thread-recognize.html` : `60° 公制三角螺纹理论牙型，中径 = 大径 − 2×(H/2 在轴向投影)，几何推导得此式（H 为理论牙高）。` : dead
- `tools/machinery/thread-recognize.html` : `中径为何用 0.75H·cos(α/2)？` : dead
- `tools/machinery/thread-recognize.html` : `外径≈10、螺距 1.5、牙型角 60°：H=p/(2·tan30°)=1.5/1.1547≈1.299 mm；d2=10−0.75×1.299×cos30°=10−0.843≈9.157 mm；d1=10−1.0825×1.5≈8.376 mm。匹配标准 M10×1.5。` : dead
- `tools/machinery/thread-recognize.html` : `螺纹识别 = 参数查表` : dead
- `tools/machinery/tolerance.html` : `配合公差 = 孔轴偏差` : dead
- `tools/machinery/tolerance-1.html` : `几何公差 = 标注查表` : dead
- `tools/machinery/torque.html` : `T = K × F × d（扭矩系数法）；F = 预紧比例 × σs × As` : dead
- `tools/machinery/xiao-dingwei-lianjie-chicun.html` : `销钉直径 d = √(4F ÷ (π·τ))；F 为传递力，τ 为许用剪应力` : dead

  其它成因样例（共 142 条，仅列前 5）：
  - `tools/machinery/analysis-lifespan.html` : `MTBF = 总运行时间 ÷ 故障次数` : fragment
  - `tools/machinery/analysis-lifespan.html` : `可靠度 R(t) = e^(−t ÷ MTBF)` : fragment
  - `tools/machinery/banjinzhewanzhankai.html` : `请输入有效参数（板厚须大于 0，角度须在 0°–180° 之间且不含端点，K 因子 0~1）` : dynamic
  - `tools/machinery/banjinzhewanzhankai.html` : `折弯角 0~180°（不含端点，180° 时 tan(θ/2) 发散）` : fragment
  - `tools/machinery/banjinzhewanzhankai.html` : `⚠ 翼缘 A/B 小于外截退量 OSSB，几何上无法按该公式展开，展开总长暂不显示；请核对测量口径（应为外边到虚拟尖角交叉点）。` : dynamic

### manufacturing（dead 10 / dynamic 6 / fragment 0 / harmless 0）

- `tools/manufacturing/capacity-planning.html` : `产能富余,可减少 台设备或增加订单` : dead
- `tools/manufacturing/capacity-planning.html` : `请输入有效参数：设备数与每日班次须为正整数，单台班产能>0，需求>0，每月工作日为 1–31 的整数。` : dead
- `tools/manufacturing/defect-rate.html` : `CPK 粗算 = (σ − 3) × 2 ÷ 3` : dead
- `tools/manufacturing/defect-rate.html` : `DPMO 指每百万次机会中的缺陷数，西格玛水平由 DPMO 查表换算：约 66807→3σ、6210→3.5σ、233→4σ、3.4→5σ、0.002→6σ。数值越高过程越稳定，行业通常目标 ≥4σ（约 DPMO≤6210）。` : dead
- `tools/manufacturing/defect-rate.html` : `某装配线投入 50000 件、检出不良 250 件、共 2 道工序。不良率 = 250÷50000 = 0.5%；单工序直通率 = 1−0.5% = 99.5%；滚动直通率 RTY = 0.995² ≈ 99.00%；PPM = 0.5%×10⁶ = 5000；DPMO = 5000÷2 = 2500；查表得西格玛水平…(+51字)` : dead
- `tools/manufacturing/defect-rate.html` : `核心计算公式（按输入变量）：max(0, (sigma - 3) × 2 ÷ 3)；(d ÷ t) × 1000000 ÷ p；(d ÷ t) × 1000000` : dead
- `tools/manufacturing/defect-rate.html` : `西格玛水平 = DPMO 反查标准表（含 1.5σ 漂移，3.4→6σ、233→5σ、6210→4σ、66807→3σ）<br>短期等效 CPK = 西格玛水平 ÷ 3<br>等级：<3σ 行业平均｜3~4σ 良好｜4~5σ 优秀｜≥5σ 卓越<br>输入校验：投入>0、不良数 ≤ 投入数` : dead
- `tools/manufacturing/defect-rate.html` : `西格玛水平 = DPMO 反查正态分位（含 1.5σ 漂移）` : dead
- `tools/manufacturing/production-efficiency.html` : `核心计算公式（按输入变量）：(1 - min(performance,1)) × 100；min(O ÷ idealCount, 1.5)；(runTime × 60) ÷ CT` : dead
- `tools/manufacturing/quality-control.html` : `样本数 n<30，长期能力估计参考性有限` : dead

  其它成因样例（共 6 条，仅列前 5）：
  - `tools/manufacturing/capacity-planning.html` : `完成订单所需设备` : dynamic
  - `tools/manufacturing/capacity-planning.html` : `总设备日需求` : dynamic
  - `tools/manufacturing/capacity-planning.html` : `本工序产能缺口` : dynamic
  - `tools/manufacturing/defect-rate.html` : `⚠ 输入无效：投入数量与工序数须为正整数，不良数量须为 0 到投入数量之间的整数。` : dynamic
  - `tools/manufacturing/quality-control.html` : `长期标准差须大于 0（留空则不计算 PPK）` : dynamic

### maritime（dead 4 / dynamic 1 / fragment 0 / harmless 0）

- `tools/maritime/stowage-factor.html` : `请检查输入：积载因数、船舶舱容与载重吨需为 >0 的数值，总货量需为 ≥0 的数值。` : dead
- `tools/maritime/stowage-factor.html` : `请检查输入：货物体积与货物重量均需为 >0 的数值。` : dead
- `tools/maritime/stowage-factor.html` : `货物分类：SF <0.6 重货（载重受限）｜<1.3 中等｜<2.0 轻货（舱容受限）｜≥2.0 极轻` : dead
- `tools/maritime/tide-window.html` : `Mean = (高潮潮高+低潮潮高)÷2；振幅 = (高潮潮高−低潮潮高)÷2` : dead

  其它成因样例（共 1 条，仅列前 5）：
  - `tools/maritime/tide-window.html` : `⚠ 输入无效：潮高、水深、吃水与 UKC 不得为负，通航所需时间须大于 0。` : dynamic

### marketing（dead 19 / dynamic 59 / fragment 2 / harmless 0）

- `tools/marketing/ad-roi.html` : `广告 ROI 模拟：CPC 模式 点击数=预算÷CPC、展示=点击÷CTR；CPM 模式 展示=预算÷CPM×1000、点击=展示×CTR。收入=点击×CVR×客单价，毛利=收入×(1−成本率)−固定成本，ROI=毛利÷预算。调整出价 / CTR / CVR 即可比较不同投放方案盈亏。` : dead
- `tools/marketing/ad-roi.html` : `盈亏平衡 ROAS = 1 ÷ 毛利率。毛利率 40% 时只要 ROAS≥1.67 就不亏，低于则必亏。` : dead
- `tools/marketing/ad-roi.html` : `若利润为负，公式给出：转化率需提升到 预算/(客单价×点击量)，或客单价提升到 预算/(点击量×转化率)。例如点击 5000、客单价 300、预算 10000 → 转化率需达 10000/(300×5000)=0.67% 才保本。` : dead
- `tools/marketing/calc-price-elasticity.html` : `价格 +10%、销量仅 −3% → E=−0.3 缺乏弹性，总收入由 100000 升到 113300 元，适合小幅提价。` : dead
- `tools/marketing/calc-price-elasticity.html` : `弧弹性（中点法）：需求变化率=(q2−q1)/[(q1+q2)/2]，价格变化率=(p2−p1)/[(p1+p2)/2]，Ed=需求变化率÷价格变化率（带符号）。|Ed|>1 富有弹性、<1 缺乏弹性；收入变化率=(p2×q2−p1×q1)/(p1×q1)，用于判断调价方向。` : dead
- `tools/marketing/marketing-coupon-discount.html` : `最终价格 = (原价 × 折扣率 - 优惠券) × 数量` : dead
- `tools/marketing/marketing-coupon-discount.html` : `注意：需先判断是否满足优惠券使用条件。` : dead
- `tools/marketing/marketing-coupon-discount.html` : `注意：需先判断是否满足优惠券使用条件；<strong>门槛按折前总额（原价×数量）判断，不按折后金额</strong>，且本页只支持「先折扣、后减券」一张券，多券叠加需按活动规则另算。` : dead
- `tools/marketing/marketing-coupon-discount.html` : `注意：需先判断是否满足优惠券使用条件；门槛按折前总额（原价×数量）判断，不按折后金额，且本页只支持「先折扣、后减券」一张券，多券叠加需按活动规则另算。` : dead
- `tools/marketing/marketing-free-shipping-threshold.html` : `免邮门槛评估：距免邮差额 = max(0, 门槛 − 购物车)；加购至免邮的净收益 =（门槛 − 购物车）× 平均毛利率 − 运费，正值提示加购划算。` : dead
- `tools/marketing/marketing-price-elasticity.html` : `价格 +10%、销量仅 −3% → E=−0.3，原收入 100000、新收入 113300，刚需品适合提价。` : dead
- `tools/marketing/marketing-roas-calculator.html` : `「广告费后利润率」= (广告收入 − 广告花费)/广告收入，只扣广告费、未扣货品成本，不是毛利率也不是净利率；真正的盈亏平衡判断要用输入的商品毛利率。` : dead
- `tools/marketing/marketing-roas-calculator.html` : `不等于毛利率/净利率` : dead
- `tools/marketing/marketing-roas-calculator.html` : `广告费后利润=10000、占收入 50%（未扣货品成本，` : dead
- `tools/marketing/marketing-roas-calculator.html` : `盈亏平衡ROAS（毛利为负，无平衡点）` : dead
- `tools/marketing/marketing-roas-calculator.html` : `（毛利率为扣货品成本口径，如 40% ⇒ 2.50x）。` : dead
- `tools/marketing/marketing-roas-calculator.html` : `）；盈亏平衡 ROAS = 1/` : dead
- `tools/marketing/marketing-roi.html` : `净利润` : dead
- `tools/marketing/price-elasticity.html` : `中点法弧弹性 Ed=(ΔQ/均价Q)÷(ΔP/均价P)。|Ed|>1 富有弹性（降价增收入）、<1 缺乏弹性（涨价增收入）、≈1 单位弹性。结果带符号，负号表示价格上升需求下降，符合常规需求规律。` : dead

  其它成因样例（共 61 条，仅列前 5）：
  - `tools/marketing/ad-roi.html` : `当前货品成本率 ≥ 100%（毛利率 ≤ 0），任何转化率或客单价都无法覆盖货品成本，请先下调货品成本率。` : dynamic
  - `tools/marketing/ad-roi.html` : `货品成本率 ≥ 100%，广告投多少都覆盖不了货品成本` : dynamic
  - `tools/marketing/marketing-ad-budget-allocator.html` : `总预算、分配比例与 ROAS 均须为非负数` : dynamic
  - `tools/marketing/marketing-ad-budget-allocator.html` : `⚠ 输入比例合计 ` : dynamic
  - `tools/marketing/marketing-ad-budget-allocator.html` : `%，与 100% 相差 ` : dynamic

### materials（dead 15 / dynamic 14 / fragment 1 / harmless 3）

- `tools/materials/analysis-cost-profit-2.html` : `Mass（检测/标准/追溯）体系` : dead
- `tools/materials/bulk-modulus-e-nu.html` : `K = E/[3(1−2ν)]。 钢 → 约 166.7 GPa。` : dead
- `tools/materials/detector-40.html` : `Mass（色差/强度/标准）检测` : dead
- `tools/materials/detector-strength-color-diff.html` : `Mass（标准/检测/环保）认证` : dead
- `tools/materials/fourier-conduction.html` : `q = k·A·ΔT/L。 钢 k=50，示例 → 1000 W。` : dead
- `tools/materials/hardness-14.html` : `HRC→HV 查标准换算表（如 HRC30≈HV303）` : dead
- `tools/materials/huanbaonaimopinggu.html` : `B - 良好` : dead
- `tools/materials/huanbaonaimopinggu.html` : `C - 中等` : dead
- `tools/materials/lifespan-25.html` : `Coffin-Manson 公式适用于低周疲劳（Nf < 10⁵）` : dead
- `tools/materials/lifespan-6.html` : `ISO 12944 环境等级：C1(<1.3)、C2(1.3-25)、C3(25-50)、C4(50-80)、C5(80-200) μm/年` : dead
- `tools/materials/naimoxingpinggujisuan.html` : `磨损系数 k ≈ a·μ²（摩擦越大磨损越剧烈的经验简化式）` : dead
- `tools/materials/rule-of-mixtures.html` : `纵向模量（E_c = V_f·E_f + V_m·E_m）` : dead
- `tools/materials/specific-heat-capacity.html` : `C = m·c。 水 m=2kg,c=4200 → 8400 J/K。` : dead
- `tools/materials/thermal-diffusivity.html` : `α = k/(ρ·c)。 钢 ≈ 1.4×10⁻⁵ m²/s。` : dead
- `tools/materials/thermal-resistance.html` : `R_th = L/(k·A)。 示例 → 0.1 K/W。` : dead

  其它成因样例（共 18 条，仅列前 5）：
  - `tools/materials/detector-hardness-lifespan.html` : `8 莫氏` : fragment
  - `tools/materials/huanbaonaimopinggu.html` : `· 综合等级：` : dynamic
  - `tools/materials/lifespan-25.html` : `热应力估算 (MPa)` : dynamic
  - `tools/materials/lifespan-26.html` : `🛠️ 高温蠕变寿命` : harmless
  - `tools/materials/lifespan-26.html` : `绝对温度 (K)` : dynamic

### math（dead 23 / dynamic 37 / fragment 3 / harmless 2）

- `tools/math/calc-2.html` : `比例 a:b = a/b` : dead
- `tools/math/calc-4.html` : `圆面积 A = πr², 周长 C = 2πr` : dead
- `tools/math/calculus-tools.html` : `导数/积分 = 微积运算` : dead
- `tools/math/combination-repetition.html` : `可重复组合 C(n+k−1, k)` : dead
- `tools/math/equation-solver.html` : `一次方程直接求解；二次方程先算判别式 Δ = b² − 4ac，Δ > 0 得两个实根、Δ = 0 得重根、Δ < 0 输出一对共轭复根；三次方程以牛顿法配合区间扫描求全部实根。` : dead
- `tools/math/function-plotter.html` : `输入以 x 为变量的表达式，可用 sin, cos, tan, exp, log, sqrt, abs, pow, PI, E 等。` : dead
- `tools/math/geometric-series-sum.html` : `|r|<1 时数列收敛。` : dead
- `tools/math/geometry-calculator.html` : `面积/体积 = 几何公式` : dead
- `tools/math/index.html` : `数学计算工具集合收录了 36 个免费在线工具，覆盖数学计算场景下的常见计算、换算与查询需求。无论你是相关领域的从业者、学生还是普通用户，都能在这里找到即用即走的实用小工具。所有工具纯前端运行，数据不上传服务器，保护隐私安全。` : dead
- `tools/math/liangshuzhihe-chengjizuida-zuixiao-shuxueti.html` : `一、和定积最大：a + b = 20` : dead
- `tools/math/liangshuzhihe-chengjizuida-zuixiao-shuxueti.html` : `三、代入验算：a = 12，b = 8` : dead
- `tools/math/liangshuzhihe-chengjizuida-zuixiao-shuxueti.html` : `二、积定和最小：a × b = 36` : dead
- `tools/math/liangshuzhihe-chengjizuida-zuixiao-shuxueti.html` : `五、因数对枚举表（a × b = 36）` : dead
- `tools/math/liangshuzhihe-chengjizuida-zuixiao-shuxueti.html` : `取等条件：a = b = 10，此时积取最大值 100。该和下两数恰好都能取整数，正整数解同样取到等号点。` : dead
- `tools/math/liangshuzhihe-chengjizuida-zuixiao-shuxueti.html` : `取等条件：a = b = √P = 6，此时和取最小值 12。√P 为整数，正整数解同样取到等号点。` : dead
- `tools/math/liangshuzhihe-chengjizuida-zuixiao-shuxueti.html` : `四、正整数拆分枚举表（a + b = 20）` : dead
- `tools/math/liangshuzhihe-chengjizuida-zuixiao-shuxueti.html` : `差值 0` : dead
- `tools/math/liangshuzhihe-chengjizuida-zuixiao-shuxueti.html` : `待验算 a×b（a=12，b=8）` : dead
- `tools/math/liangshuzhihe-chengjizuida-zuixiao-shuxueti.html` : `最大积（a+b=20，正整数解）` : dead
- `tools/math/liangshuzhihe-chengjizuida-zuixiao-shuxueti.html` : `最小和（a×b=36，正整数解）` : dead
- `tools/math/liangshuzhihe-chengjizuida-zuixiao-shuxueti.html` : `距最大积 4` : dead
- `tools/math/percent-change.html` : `Δ% = (新−旧)/旧 × 100%` : dead
- `tools/math/quadratic-discriminant.html` : `Δ>0 两实根，Δ=0 重根，Δ<0 复根。` : dead

  其它成因样例（共 42 条，仅列前 5）：
  - `tools/math/circular-permutation.html` : `环形排列数 = (n−1)!` : fragment
  - `tools/math/factorial-calc.html` : `n 必须是非负整数（不支持小数、负数或空值）。` : dynamic
  - `tools/math/fibonacci-n.html` : `n 必须是非负整数（不支持小数、负数或空值）。` : dynamic
  - `tools/math/fibonacci-n.html` : `为保证计算性能，n 上限为 1000（已不再静默截断）。` : dynamic
  - `tools/math/function-plotter.html` : `🧮 数学图形绘制` : harmless

### mechanical（dead 1 / dynamic 0 / fragment 0 / harmless 0）

- `tools/mechanical/torque-power.html` : `P = T·ω/1000 应回等于输入功率` : dead

### medical（dead 13 / dynamic 16 / fragment 1 / harmless 0）

- `tools/medical/assessor-risk-3.html` : `尿酸结石在酸性尿(pH<5.5)中易形成，碱化至pH 6.5-7.0可预防` : dead
- `tools/medical/calc-34.html` : `BMI = 体重(kg) ÷ 身高(m)²：<18.5 偏瘦｜18.5–24 正常｜24–28 超重｜≥28 肥胖` : dead
- `tools/medical/calc-34.html` : `RER（静息能量需求）按 25 kcal/kg 估算，参考区间 25–30 kcal/kg，与 BMR 不是同一指标；肥胖者按理想体重、重症需叠加应激系数。` : dead
- `tools/medical/calc-34.html` : `按 Mifflin-St Jeor 公式估算静息能量消耗（RER/BMR），再乘活动系数得每日总消耗（` : dead
- `tools/medical/calc-34.html` : `男性 65 kg / 170 cm / 30 岁、久坐（1.2）：BMR = 650 + 1062.5 − 150 + 5 = 1567.5 ≈ 1568 kcal/日；TDEE = 1567.5 × 1.2 ≈ 1881 kcal；减脂目标 ≈ 1505 kcal；增肌目标 ≈ 2281 kcal；BMI = 65 …(+142字)` : dead
- `tools/medical/calculator-calc-2.html` : `婴儿（<1 岁）与老年（≥65 岁）提示专科核定` : dead
- `tools/medical/clinical-tools.html` : `13–15 分：轻度意识障碍，密切观察、定期复评` : dead
- `tools/medical/convert-glucose.html` : `空腹血糖 5.6 mmol/L → 5.6 × 18.0159 ≈ 100.9 mg/dL，属正常范围（3.9-6.1 mmol/L / 70-110 mg/dL）。随机血糖 11.1 mmol/L → × 18.0159 ≈ 200.0 mg/dL，达到糖尿病诊断的随机阈值。反向：血糖仪显示 100.9 mg/dL …(+228字)` : dead
- `tools/medical/convert-time-infusion.html` : `滴速(滴/分) = 液体量(mL) × 滴系数(滴/mL) ÷ 时间(分)` : dead
- `tools/medical/dosage-calculator.html` : `体重法：单次剂量 = 体重(kg) × 每公斤剂量(mg/kg)，日剂量 = 单次剂量 × 每日次数。体表面积法：BSA(m²) = √(身高(cm) × 体重(kg) ÷ 3600)（Mosteller 公式），单次剂量 = BSA × 每平方米剂量(mg/m²)，日剂量 = 单次 × 次数。两套基准必须按药物说明书…(+74字)` : dead
- `tools/medical/dosage-calculator.html` : `每公斤/每平方米剂量` : dead
- `tools/medical/stats-4.html` : `平均时长 x̄ = Σ时长 ÷ 例数` : dead
- `tools/medical/stats-4.html` : `时长上限 P95 ≈ x̄ + 1.645 × 标准差` : dead

  其它成因样例（共 17 条，仅列前 5）：
  - `tools/medical/calc-34.html` : `⚠️ 当前减脂缺口超过建议的 300–500 kcal/日上限，建议上调摄入或提高活动量。` : dynamic
  - `tools/medical/calculator-calc-2.html` : `有效最大日剂量（取较小值）` : dynamic
  - `tools/medical/clinical-tools.html` : `90 天死亡率约 1.9%，定期随访。` : dynamic
  - `tools/medical/clinical-tools.html` : `90 天死亡率约 6.0%，每 3–6 个月复查并评估移植指征。` : dynamic
  - `tools/medical/clinical-tools.html` : `90 天死亡率约 19.6%，建议启动肝移植评估。` : dynamic

### metallurgy（dead 13 / dynamic 15 / fragment 5 / harmless 0）

- `tools/metallurgy/convert-hardness.html` : `千布氏` : dead
- `tools/metallurgy/convert-hardness.html` : `千洛氏` : dead
- `tools/metallurgy/convert-hardness.html` : `毫布氏` : dead
- `tools/metallurgy/convert-hardness.html` : `毫洛氏` : dead
- `tools/metallurgy/hardness-conversion.html` : `硬度换算（ASTM E140 / GB/T 33362 近似）：以线性插值在标准对照表上换算布氏 HB、洛氏 HRC/HRB、维氏 HV；同一材料不同标尺硬度对应同一抗拉强度区间，如 HRC 20 约对应 HB 238、HV 247，HRC 40 约对应 HB 371、HV 392。` : dead
- `tools/metallurgy/stats-10.html` : `成材率 = 合格成品材量 ÷ 合格坯（锭）量 × 100%` : dead
- `tools/metallurgy/stats-10.html` : `收得率 = 合格坯（锭）量 ÷ 入炉金属料 × 100%` : dead
- `tools/metallurgy/steel-profile-weight.html` : `圆管壁厚需满足 0 < t < a/2。` : dead
- `tools/metallurgy/steel-profile-weight.html` : `圆钢/圆管` : dead
- `tools/metallurgy/steel-profile-weight.html` : `壁厚/边厚 t（mm，管/角钢用）` : dead
- `tools/metallurgy/steel-profile-weight.html` : `按碳钢密度 7.85 g/cm³ 推导的经验系数（圆钢 0.00617、方钢/扁钢/角钢 0.00785）： 圆钢 a²×0.00617 = 20²×0.00617 = 2.468 kg/m，总重 2.468×6 ≈ 14.81 kg； 方钢 a²×0.00785 = 3.14 kg/m，总重 18.84 kg； 扁钢…(+212字)` : dead
- `tools/metallurgy/steel-profile-weight.html` : `槽钢需满足 0 < t < b，且次尺寸 b 大于 0。` : dead
- `tools/metallurgy/steel-profile-weight.html` : `角钢边厚需满足 0 < t < a。` : dead

  其它成因样例（共 20 条，仅列前 5）：
  - `tools/metallurgy/alloy-ratio.html` : `预计终态(%)` : dynamic
  - `tools/metallurgy/alloy-ratio.html` : `各元素目标含量合计超出原料可带入能力，无法同时达到，请降低目标或提高合金含量/回收率。` : dynamic
  - `tools/metallurgy/convert-hardness.html` : `布氏` : fragment
  - `tools/metallurgy/convert-hardness.html` : `洛氏` : fragment
  - `tools/metallurgy/energy-1.html` : `折标煤 =（节电量 × 0.1229 ＋ 节气量 × 1.33）÷ 1000（tce）；减排 CO₂ ≈ 折标煤 × 2.66（t）；折能 = 折标煤 × 29.307（GJ）` : fragment

### metalwork（dead 40 / dynamic 18 / fragment 8 / harmless 1）

- `tools/metalwork/analysis-39.html` : `热处理控温记录` : dead
- `tools/metalwork/analysis-39.html` : `热处理（自动化/控温/记录）` : dead
- `tools/metalwork/analysis-39.html` : `热处理（自动化/控温/记录） - 面向热处理车间的控温记录工具` : dead
- `tools/metalwork/analysis-cost-price-5.html` : `Mean = 各期价格之和 ÷ 期数；样本标准差按 n−1 口径计算，变异系数 CV = 标准差 ÷ 均值 ×100%，用来衡量价格波动幅度。` : dead
- `tools/metalwork/analysis-cost-price-5.html` : `Range = 最高价 − 最低价；首末涨跌幅 =（末期价 − 首期价）÷ 首期价 ×100%。` : dead
- `tools/metalwork/analysis-cost-price-5.html` : `安装（敷设/连接/测试）服务` : dead
- `tools/metalwork/analysis-cost-price-5.html` : `安装（敷设/连接/测试）服务 - 电缆安装敷设后的绝缘电阻、导通电阻` : dead
- `tools/metalwork/calc-feed.html` : `铣削进给 f = v_c/(π·d·n)` : dead
- `tools/metalwork/calc-gear-2.html` : `由端面模数 mt、齿数 z 决定齿距与啮合尺寸。` : dead
- `tools/metalwork/calc-gear-2.html` : `端面模数 mt = 分度圆直径÷齿数，是齿轮尺寸与强度的核心参数，必须成对啮合相同，单位 mm；斜齿的法向模数 mn = mt×cosβ。` : dead
- `tools/metalwork/calc-gear-2.html` : `齿轮加工 = 滚齿/插齿参数` : dead
- `tools/metalwork/calc-pressure-mold.html` : `Perimeter L=100mm、料厚 t=2mm、抗剪强度 τ=350MPa：理论冲裁力 F = L×t×τ = 100×2×350 = 70000 N = 70 kN；设计力 Fd = 70×1.3 = 91 kN（含安全系数）。` : dead
- `tools/metalwork/calc-pressure-mold.html` : `冲压力 F = L·t·τ` : dead
- `tools/metalwork/calc-stretch.html` : `拉伸率 = (L−L₀)/L₀ × 100%` : dead
- `tools/metalwork/detector-21.html` : `无损检测 = 方法选择` : dead
- `tools/metalwork/detector-24.html` : `缺陷（气孔/缩松/夹渣）分析` : dead
- `tools/metalwork/detector-55.html` : `≥90% 优秀，75-89% 良好，60-74% 合格，<60% 不合格` : dead
- `tools/metalwork/detector-hardness.html` : `Qualified （一般用途）` : dead
- `tools/metalwork/detector-hardness.html` : `盐雾试验结果评估` : dead
- `tools/metalwork/detector-hardness.html` : `盐雾（试验/等级/标准）评估` : dead
- `tools/metalwork/detector-hardness.html` : `盐雾（试验/等级/标准）评估 - 盐雾试验结果评估工具` : dead
- `tools/metalwork/forging-ratio.html` : `锻造比 = A₀/A` : dead
- `tools/metalwork/laxue-ladao-chisheng-lali-sheji.html` : `按单位切削力 250 N/mm²、切削宽度 10 mm、同时工作齿数 3 计算切屑总面积对应的拉削力，再按 1.3 倍安全系数与刀杆许用拉应力 600 MPa 反推刀杆最小截面。` : dead
- `tools/metalwork/lifespan-1.html` : `电池寿命 = 容量/负载` : dead
- `tools/metalwork/pinpaijiazhipinggujisuan.html` : `本页用经验参数法：品牌利润×行业乘数×年限系数×份额系数；乘数与行业、品牌强度相关，仅作快速比较与参考，不等同 ISO 10668 的合规品牌评估。` : dead
- `tools/metalwork/pinpaijiazhipinggujisuan.html` : `用经验倍率快速估算制造/金工品牌的参考价值（非合规评估）。` : dead
- `tools/metalwork/pressure-casting.html` : `铸造方法 = 选型` : dead
- `tools/metalwork/resistance-2.html` : `Mass/成本/保护气体对比` : dead
- `tools/metalwork/resistance-2.html` : `焊接方法 = 选型` : dead
- `tools/metalwork/resistance-2.html` : `输入材料厚度、接头形式与材料类型，推荐适合的焊接方法（仅做方法选型，不计算电流、电压等工艺参数）。` : dead
- `tools/metalwork/sheet-bend.html` : `钣金折弯展开 = 中性层法` : dead
- `tools/metalwork/speed-itinerary.html` : `刨削速度 = 行程/时间` : dead
- `tools/metalwork/surface-finish.html` : `Surface roughness = Ra 对照` : dead
- `tools/metalwork/surface-finish.html` : `表面粗糙度 = Ra 对照` : dead
- `tools/metalwork/temp-forging.html` : `锻造温度 = 材料相图区间` : dead
- `tools/metalwork/tester-19.html` : `价格（铜价/行情/成本）分析` : dead
- `tools/metalwork/thread.html` : `螺纹加工 = 方案选择` : dead
- `tools/metalwork/welding-heat.html` : `热输入 Q = η·U·I/v` : dead
- `tools/metalwork/welding-heat.html` : `请输入有效参数：电流、电压、焊速 > 0，热效率 η 在 0–1 之间` : dead
- `tools/metalwork/zulinfeilvjisuan.html` : `租赁费率 = 原值×费率/周期` : dead

  其它成因样例（共 27 条，仅列前 5）：
  - `tools/metalwork/cable-tray-sizing.html` : `单根截面积 A₁ = π·D²/4；电缆总截面积 A = A₁·N；所需桥架面积 A_need = A / 填充率；推荐规格取满足「宽×高 ≥ A_need」的最小规格；实际填充率 = A /(宽×高)×100%` : fragment
  - `tools/metalwork/cable-tray-sizing.html` : `需定制/双排` : dynamic
  - `tools/metalwork/cable-tray-sizing.html` : `所需面积已超过常规最大规格 600×200（120000 mm²），请改用定制桥架或双排并联，并按实际规格重新校核填充率。` : dynamic
  - `tools/metalwork/calc-gear-2.html` : `端面齿距 pt (mm)` : dynamic
  - `tools/metalwork/calc-gear-2.html` : `法向模数 mn (mm)` : dynamic

### meteorology（dead 18 / dynamic 0 / fragment 5 / harmless 0）

- `tools/meteorology/air-aqi.html` : `AQI = 逐污染物分段线性插值` : dead
- `tools/meteorology/apparent-temperature.html` : `AT = 体感温度（温湿风综合）` : dead
- `tools/meteorology/assessor-29.html` : `干旱评估用两类指标：降水距平百分率 Pa=(当前降水量−同期均值)÷同期均值×100%，按 Pa 阈值分级（≥−15% 无旱、−30% 轻旱、−50% 中旱、−70% 重旱、<−70% 特旱）；标准化降水指数 SPI=(当前−均值)÷标准差，按 SPI 阈值（≥−0.5 无旱、−1.0 轻旱、−1.5 中旱、−2.0 …(+27字)` : dead
- `tools/meteorology/beaufort-scale.html` : `风速 v ↔ 蒲福风级 n` : dead
- `tools/meteorology/calc-55.html` : `月相照明率 = (1+cos φ)/2` : dead
- `tools/meteorology/calc-84.html` : `日照辐射量 = 辐照度 × 时长` : dead
- `tools/meteorology/cloud-identify.html` : `云按云底高度分四族：高云（>5km）、中云（2.5—5km）、低云（<2.5km）、直展云（垂直发展旺盛）。` : dead
- `tools/meteorology/dew-point.html` : `露点 Td = Magnus 公式反解` : dead
- `tools/meteorology/heat-index.html` : `HI = 体感指数（温湿综合）` : dead
- `tools/meteorology/humidity-1.html` : `露点舒适度 = f(温度, 露点)` : dead
- `tools/meteorology/jiaotongqixianganquantishi.html` : `道路气象安全按三项分级综合研判：能见度 vis（<50m 特级、<200m 红、<500m 橙、<1000m 黄、其余良好）、路面温度 rt（<−3℃ 红、<0℃ 橙、<2℃ 黄）、侧风 v（≥24m/s 红，逐级下降）。任一要素达红/橙级即给出对应管制建议（限速、防滑、封闭），保障行车安全。` : dead
- `tools/meteorology/lvyouqixiangzhishu.html` : `旅游气象指数按温度(T)、湿度(RH)、风速(V)、紫外线(UV)四项舒适度加权：温度分=100−|T−22|×3.5、湿度分=100−|RH−55|×0.9、风速分=100−|V−3|×6、紫外线分=100−UV×9（均截断 0–100）；综合 idx=0.35×T分+0.20×RH分+0.20×V分+0.25×UV…(+50字)` : dead
- `tools/meteorology/nongyeqixiangjianyi.html` : `农业气象建议基于作物积温：生育进度=累积 GDD÷该作物所需 GDD 上限×100，划分播种-出苗/苗期-分蘖/拔节-抽穗/灌浆-结铃/成熟等生育期；播种适宜性按气温 T 与作物播种温区[sowT]、最适温区[optT]判定；降水量 P<10mm 提示灌溉缺水，依生育期与降水给出收割与防涝建议。` : dead
- `tools/meteorology/precipitation-rate.html` : `采用中国气象局常用分级：小雨<2.5、中雨<8、大雨<16、暴雨<50、大暴雨<100。` : dead
- `tools/meteorology/qiyaxitongyidonglujing.html` : `💡 高压（P>1020）多晴好天气，低压（P<1000）多阴雨；3小时变压 ΔP>1.5 表示系统快速接近，<-1.5 表示低压加深、天气转坏。` : dead
- `tools/meteorology/strength-3.html` : `雷达回波强度：反射率因子 Z=10^(dBZ/10)，降水率 R=(Z/200)^(1/1.6) mm/h；冰雹概率由 dBZ 与回波顶高 h 联合估计；液态水含量 VIL=3.44×10⁻⁶·Z^(4/7)·h（kg/m²）；按 dBZ 阈值（<30 弱对流、<50 强对流、≥55 冰雹可能、≥60 强冰雹）判定对流…(+18字)` : dead
- `tools/meteorology/wet-bulb-temperature.html` : `湿球温度 T_w（迭代近似）` : dead
- `tools/meteorology/wind-direction.html` : `风向方位 = 角度 → 16 方位` : dead

  其它成因样例（共 5 条，仅列前 5）：
  - `tools/meteorology/analysis-31.html` : `距平 = 观测值 − 常年平均值` : fragment
  - `tools/meteorology/analysis-31.html` : `标准化距平 σ = 距平 ÷ 历史标准差` : fragment
  - `tools/meteorology/analysis-tide.html` : `潮型系数 F = (H_K1 + H_O1) ÷ (H_M2 + H_S2)` : fragment
  - `tools/meteorology/speed-11.html` : `Z = 200·R^1.6，故 R = (Z/200)^(1/1.6)` : fragment
  - `tools/meteorology/taifengdingqiang.html` : `节 = 0.5144 m/s。气压越低，最大风速越强。` : fragment

### metrology（dead 11 / dynamic 1 / fragment 1 / harmless 0）

- `tools/metrology/bias-absolute.html` : `偏倚 = x − x_ref` : dead
- `tools/metrology/bias-percent.html` : `偏倚% = (x − x_ref)/x_ref × 100%` : dead
- `tools/metrology/expanded-uncertainty.html` : `k=2 约 95% 置信。 报告形式：测得值 ±U。` : dead
- `tools/metrology/flatness-deviation.html` : `平面度 = 最高点 − 最低点` : dead
- `tools/metrology/gauge-repeatability.html` : `重复性 = R̄/d₂` : dead
- `tools/metrology/gauge-reproducibility.html` : `再现性 = R̄/d₂*` : dead
- `tools/metrology/grr-percent.html` : `%GRR<10% 测量系统可接受。` : dead
- `tools/metrology/grr-study.html` : `%GRR<10% 良好。` : dead
- `tools/metrology/least-count-error.html` : `极限误差 = ±(分度值/2)` : dead
- `tools/metrology/precision-tolerance-ratio.html` : `PTR<0.1 通常分辨率足够。` : dead
- `tools/metrology/roundness-deviation.html` : `圆度 = R_max − R_min` : dead

  其它成因样例（共 2 条，仅列前 5）：
  - `tools/metrology/detector-139.html` : `12 个月` : fragment
  - `tools/metrology/detector-139.html` : `3 个月` : dynamic

### mining（dead 2 / dynamic 4 / fragment 1 / harmless 0）

- `tools/mining/convert-grade-ore.html` : `矿石价值(元) = 金属总量 × 金属价格(元/g)` : dead
- `tools/mining/excavation-volume.html` : `长方体 V=L·W·D；梯形截面 V=(上底宽+下底宽)/2×深×长（含边坡时上底=下底+2·深·边坡）；圆柱 V=πR²H，圆台 V=πH/3·(R₁²+R₁R₂+R₂²)；虚方=实方×松散系数 swell；成本=实方×单价。` : dead

  其它成因样例（共 5 条，仅列前 5）：
  - `tools/mining/convert-grade-ore.html` : `金属总量(g) = 品位(g/t) × 矿石量(t)` : fragment
  - `tools/mining/convert-grade-ore.html` : `品位需填写 ≥0 的数值（g/t）` : dynamic
  - `tools/mining/convert-grade-ore.html` : `矿石量需填写 ≥0 的数值（t）` : dynamic
  - `tools/mining/convert-grade-ore.html` : `金属价格需填写 ≥0 的数值（元/g）` : dynamic
  - `tools/mining/excavation-volume.html` : `上口宽不能小于底宽，请核对输入` : dynamic

### misc（dead 9 / dynamic 0 / fragment 0 / harmless 0）

- `tools/misc/index.html` : `使用 Canvas 绘制常见函数图像：一次函数、二次函数、三角函数、指数函数、对数函数，支持自定义参数与坐标范围。` : dead
- `tools/misc/index.html` : `内置 30+ 常用物理学常数，含数值、单位、符号与说明，支持搜索与分类筛选。数据基于 CODATA 2018 推荐值。` : dead
- `tools/misc/index.html` : `在 SI 单位前缀（nano / micro / milli / kilo / Mega / Giga / Tera 等）之间换算数值。` : dead
- `tools/misc/index.html` : `支持复数的加、减、乘、除运算及与极坐标（模、幅角）的相互转换，并在复平面上直观绘制点的位置，适用于工程数学与电路相量分析的教学演示。` : dead
- `tools/misc/index.html` : `标准小数与科学记数法（a×10ⁿ）双向互转，支持工程记数法与 E 记数法。` : dead
- `tools/misc/index.html` : `生成奇数阶幻方使各行列对角线和相等，可调阶数并校验，用于数学游戏与教学演示，纯前端生成棋盘可复制。` : dead
- `tools/misc/index.html` : `用 4 个数字和 +、−、×、÷、括号 组成表达式，使结果等于 24。每个数字必须且只能用一次。` : dead
- `tools/misc/index.html` : `输入逻辑表达式，自动识别变量并生成完整真值表。支持与或非、异或、蕴含、等价等运算。` : dead
- `tools/misc/index.html` : `选择分布类型（正态、泊松、二项），输入均值/方差或成功概率与试验次数等参数，计算对应概率密度函数与累积分布概率。用于概率统计教学、质量分析与风险建模。` : dead

### misc2（dead 11 / dynamic 0 / fragment 0 / harmless 0）

- `tools/misc2/index.html` : `二手车残值计算` : dead
- `tools/misc2/index.html` : `列出各品牌与国家的鞋码对照（欧、美、英、厘米），输入已知码查对应尺码，方便网购选号，纯前端查表。` : dead
- `tools/misc2/index.html` : `基于十二平均律生成各音名的标准频率对照表，默认基准A4=440Hz并支持自定义基准音高，供乐器校音、合唱定调与声学教学快速查阅参考。` : dead
- `tools/misc2/index.html` : `屏幕尺寸计算器由分辨率宽高与对角线英寸求 PPI 像素密度，并换算实际显示尺寸，适合选购显示器、手机与投影设备的清晰度评估。` : dead
- `tools/misc2/index.html` : `快递保价费计算器按声明价值与快递公司费率估算保价费用，支持多家快递对比，适合寄件前成本预估与贵重物品保护决策。` : dead
- `tools/misc2/index.html` : `查阅 18–30 寸主流行李箱的长宽高与容量规格，并对照各航空公司随身行李与托运行李的尺寸重量限制。用于出行前选择符合航司规定的箱包，避免登机受阻。` : dead
- `tools/misc2/index.html` : `生活杂项工具集合收录了 9 个免费在线工具，覆盖生活杂项场景下的常见计算、换算与查询需求。无论你是相关领域的从业者、学生还是普通用户，都能在这里找到即用即走的实用小工具。所有工具纯前端运行，数据不上传服务器，保护隐私安全。` : dead
- `tools/misc2/index.html` : `输入境外购物金额、目的地国家税率与实时汇率，估算可退税款金额与退税后的实际花费。用于出境旅游购物前预估退税收益、比较不同目的地划算程度。` : dead
- `tools/misc2/index.html` : `输入新车购置价与已使用年限，按前5年分别折旧 15%、12%、10%、8%、6%、之后每年约 5% 的曲线估算二手车剩余价值。用于家用车快速估值、置换参考与残值预测。` : dead
- `tools/misc2/index.html` : `输入香烟标注的焦油/尼古丁含量与每日吸烟支数，估算每日焦油与尼古丁摄入总量及相对暴露风险。用于烟民了解吸烟负荷，结果仅供健康意识参考。` : dead
- `tools/misc2/index.html` : `选择或输入钱币品相等级（谢尔登分级 Sheldon 1–70），查看对应磨损程度说明、评分要点与收藏保值建议。用于钱币收藏者快速对照品相、评估钱币价值。` : dead

### museum（dead 6 / dynamic 7 / fragment 1 / harmless 0）

- `tools/museum/era-comparator.html` : `历史朝代对比。历史人文工具，帮助查询与了解历史文化知识。` : dead
- `tools/museum/historical-calendar.html` : `历史日历是一款历史人文领域的在线工具。历史人文工具，帮助查询与了解历史文化知识。` : dead
- `tools/museum/index.html` : `历史日历是一款免费的在线文博展陈工具，历史日历是一款历史人文领域的在线工具。历史人文工具，帮助查询与了解历史文化知识。纯前端运行、数据不上传、无需注册，打开浏览器即可使用。` : dead
- `tools/museum/index.html` : `历史时间轴是一款免费的在线文博展陈工具，历史时间轴是一款历史人文领域的在线工具。历史人文工具，帮助查询与了解历史文化知识。纯前端运行、数据不上传、无需注册，打开浏览器即可使用。` : dead
- `tools/museum/index.html` : `历史朝代对比是一款免费的在线文博展陈工具，历史朝代对比。历史人文工具，帮助查询与了解历史文化知识。纯前端运行、数据不上传、无需注册，打开浏览器即可使用。` : dead
- `tools/museum/timeline-viewer.html` : `历史时间轴是一款历史人文领域的在线工具。历史人文工具，帮助查询与了解历史文化知识。` : dead

  其它成因样例（共 8 条，仅列前 5）：
  - `tools/museum/lighting-lux.html` : `达标 ✓` : dynamic
  - `tools/museum/lighting-lux.html` : `平均照度超标 ✕` : dynamic
  - `tools/museum/lighting-lux.html` : `中心照度过曝 ✕` : dynamic
  - `tools/museum/visitor-route.html` : `检测到负距离，已按绝对值纳入计算。` : dynamic
  - `tools/museum/visitor-route.html` : `必看节点` : fragment

### music（dead 3 / dynamic 2 / fragment 1 / harmless 0）

- `tools/music/index.html` : `音乐艺术工具集合收录了 19 个免费在线工具，覆盖音乐艺术场景下的常见计算、换算与查询需求。无论你是相关领域的从业者、学生还是普通用户，都能在这里找到即用即走的实用小工具。所有工具纯前端运行，数据不上传服务器，保护隐私安全。` : dead
- `tools/music/random-training-rhythm.html` : `鼓手/器乐练习者用空格或点击跟节拍器敲击，练稳定律动；随机节奏型用于读谱与节奏型参考` : dead
- `tools/music/web-tuner.html` : `MIDI = 69 + 12·log2(f / A4参考频率)；A4 参考 440 Hz 时，440 Hz → MIDI 69 → A4，音分 = (69−69)×100 = 0（准）。446 Hz → MIDI≈69.246 → +24.6 cents（偏高）；参考改为 442 Hz 时 442 Hz 同样对应 A4…(+7字)` : dead

  其它成因样例（共 3 条，仅列前 5）：
  - `tools/music/random-training-rhythm.html` : `节奏准确率 = 命中节拍数 ÷ 总节拍数 × 100%；单次偏差 = 实际点击时刻 − 标准节拍时刻（正为拖后、负为提前），平均偏差 = Σ 偏差 ÷ 次数；稳定度可用偏差标准差衡量，标准差低于 30 ms 为稳定；节拍间隔 = 60000 ÷ BPM 毫秒（如 120 BPM 为 500 ms）。` : fragment
  - `tools/music/random-training-rhythm.html` : `已停止` : dynamic
  - `tools/music/random-training-rhythm.html` : `跟拍中… 共 ` : dynamic

### nephrology（dead 19 / dynamic 23 / fragment 4 / harmless 0）

- `tools/nephrology/aki-kdigo.html` : `AKI诊断：48h Scr↑≥26.5 μmol/L 或 7天↑≥1.5×基线 或 尿量<0.5 mL/kg/h。分期：1期 1.5–1.9×；2期 2.0–2.9×；3期 ≥3× 或 ≥353.6 μmol/L 或 尿量<0.3 mL/kg/h×≥24h；取肌酐/尿量较重者` : dead
- `tools/nephrology/ca-p-product.html` : `换算：钙磷乘积 mmol²/L² × 12.45 = mg²/dL²。目标值<55 mg²/dL²（4.4 mmol²/L²）。` : dead
- `tools/nephrology/ckd-staging.html` : `G3a+A2→高风险，建议 2 次/年随访并转诊肾内科。` : dead
- `tools/nephrology/ckd-staging.html` : `G4(15–29)+A3→很高风险，≥3 次/年随访，积极管理并发症并准备肾脏替代。` : dead
- `tools/nephrology/creatinine-clearance.html` : `Ccr 50-80 为轻度损害，25-50 为中度损害，10-25 为重度损害，<10 为终末期肾病。` : dead
- `tools/nephrology/creatinine-clearance.html` : `提示：收集24h尿液前3天需低蛋白饮食（<40g/d），禁食肉食，避免剧烈运动，以保证肌酐排泄稳定。Ccr反映肾小球滤过功能，但肾小管也分泌少量肌酐，故Ccr略高于真实GFR。本工具仅供学习参考。` : dead
- `tools/nephrology/creatinine-clearance.html` : `本页按 Ccr 分段：≥80 正常范围、50–79 轻度下降、25–49 中度下降、10–24 重度下降、<10 极重度下降。该分段仅为 Ccr 的功能描述，不等同于 KDIGO 2012 的 CKD G1–G5 分期（后者基于 eGFR）；「终末期肾病」为临床诊断，本页不下此结论。` : dead
- `tools/nephrology/edema-grading.html` : `水肿分级（按凹陷深度）：1+ 不超过2mm 轻度、2+ 2–4mm 中度、3+ 4–6mm 重度、4+ 不低于6mm 极重度；结合部位与是否对称评估病因。` : dead
- `tools/nephrology/manager-1.html` : `CKD诊断需满足：eGFR<60持续>3个月，或肾脏损伤标志（白蛋白尿等）持续>3个月` : dead
- `tools/nephrology/manager-1.html` : `：ACR <30 mg/g（正常至微量增加）` : dead
- `tools/nephrology/manager-1.html` : `：eGFR <15（肾衰竭）` : dead
- `tools/nephrology/proteinuria-24h.html` : `24 小时尿蛋白分级：小于0.15g 正常、0.15–0.5 轻度、0.5–3.5 中度、不低于3.5g 为肾病综合征范围蛋白尿。` : dead
- `tools/nephrology/proteinuria-24h.html` : `24h 尿蛋白 ≥3.5 g，属肾病综合征范围蛋白尿；但肾病综合征的诊断还需血清白蛋白 <30 g/L 与水肿，本页不能据此单独确诊。需评估血清白蛋白、血脂、肾功能，排查继发因素（糖尿病、系统性红斑狼疮、肿瘤等），建议肾内科评估是否肾活检。` : dead
- `tools/nephrology/proteinuria-24h.html` : `≥3.5g/24h 属肾病范围；是否诊断肾病综合征还需低白蛋白(<30g/L)与水肿，并由肾内科评估是否需病理检查。` : dead
- `tools/nephrology/proteinuria-24h.html` : `□ 查血清白蛋白是否 <30 g/L（肾病综合征必需条件之一）` : dead
- `tools/nephrology/renal-anemia-epo.html` : `HGB <100（个体化）` : dead
- `tools/nephrology/renal-tubular-acidosis.html` : `低钾(常<3.5)` : dead
- `tools/nephrology/renal-tubular-acidosis.html` : `提示：RTA核心特征为正常阴离子间隙型代谢性酸中毒(AG正常)。I型尿pH始终>5.5，II型酸中毒严重时尿pH可<5.5，IV型以高钾血症为特征。碳酸氢盐试验(FE-HCO₃⁻)有助于确诊。本工具仅供学习参考。` : dead
- `tools/nephrology/urine-electrolyte.html` : `<20肾外丢失，>20肾性丢失` : dead

  其它成因样例（共 27 条，仅列前 5）：
  - `tools/nephrology/ckd-staging.html` : `请填写有效的 eGFR 与 UACR 数值（UACR 不能留空）` : dynamic
  - `tools/nephrology/creatinine-clearance.html` : `内生肌酐清除率 Ccr(mL/min) = [尿肌酐(μmol/L) × 尿量(mL/min)] ÷ 血肌酐(μmol/L)；并用体表面积校正 Ccr × 1.73 ÷ BSA。` : fragment
  - `tools/nephrology/creatinine-clearance.html` : `Ccr ≥80（正常范围）` : dynamic
  - `tools/nephrology/creatinine-clearance.html` : `Ccr 50–79（轻度下降）` : dynamic
  - `tools/nephrology/creatinine-clearance.html` : `Ccr 25–49（中度下降）` : dynamic

### neurology（dead 6 / dynamic 41 / fragment 0 / harmless 0）

- `tools/neurology/alsfrs-r.html` : `球部 12+臂 12+躯干 4+腿 8+呼吸 12=48 分（满分，功能正常）。` : dead
- `tools/neurology/nihss.html` : `0 无神经功能缺损（不代表排除卒中）、1~4 轻、5~15 中、16~20 中重、≥21 重；上限 42。` : dead
- `tools/neurology/nihss.html` : `合计 18 分：中重度（16~20），需紧急评估取栓/溶栓并加强监护。` : dead
- `tools/neurology/nihss.html` : `总分 ≥16 分提示可能存在大血管闭塞` : dead
- `tools/neurology/rater-22.html` : `SARA 小脑共济失调量表总分 = 8 项检查（步态/站姿/坐姿/言语/指鼻/跟膝胫/轮替/跟-胫滑动）之和，满分 40；≤3 轻度、≤8 轻中度、≤15 中度、≤30 重度、>30 极重度。` : dead
- `tools/neurology/rater-22.html` : `SARA包含步态、站立、坐位、言语、追视、鼻指测试和交替轮替运动8项检查，总分0-40分，广泛用于遗传性共济失调的诊断分期、疗效评估和疾病进展监测。` : dead

  其它成因样例（共 41 条，仅列前 5）：
  - `tools/neurology/qmg.html` : `13.颈屈` : dynamic
  - `tools/neurology/rater-22.html` : `1.步态（0–8分）` : dynamic
  - `tools/neurology/rater-22.html` : `2.站立（0–6分）` : dynamic
  - `tools/neurology/rater-22.html` : `3.坐位（0–4分）` : dynamic
  - `tools/neurology/rater-22.html` : `4.言语障碍（0–6分）` : dynamic

### niche（dead 17 / dynamic 0 / fragment 0 / harmless 0）

- `tools/niche/index.html` : `在不同采样率（如 44.1k、48k）间换算，输入声道数与位深计算音频文件大小，并按奈奎斯特定理给出最高可记录频率。用于录音、混音格式选型。` : dead
- `tools/niche/index.html` : `在常见视频帧率（24/25/30/60fps）间换算并估算时长变化，用于剪辑与格式转换参考，纯前端换算不转码。` : dead
- `tools/niche/index.html` : `垂直工具工具集合收录了 16 个免费在线工具，覆盖垂直工具场景下的常见计算、换算与查询需求。无论你是相关领域的从业者、学生还是普通用户，都能在这里找到即用即走的实用小工具。所有工具纯前端运行，数据不上传服务器，保护隐私安全。` : dead
- `tools/niche/index.html` : `基于曝光三角（光圈、快门、ISO）计算曝光值 EV，并提供多组等效曝光组合，方便摄影师在保持曝光量不变下自由调整参数。` : dead
- `tools/niche/index.html` : `按低光、中光、高光三级对常见水草分类，输入鱼缸光照条件即可筛选适合养殖的品种并标注养护要点。用于水族造景选草，避免光照不足或藻类爆发。` : dead
- `tools/niche/index.html` : `按多肉品种管理浇水周期，内置常见科属浇水频率数据库，自动根据季节调整（夏休眠/冬减量），按紧急度排序生成浇水队列。` : dead
- `tools/niche/index.html` : `蜡烛燃烧时间估算工具按蜡烛重量与蜡材类型估算可持续燃烧时长，并给出首燃与烛芯修剪建议，适合香薰与应急照明规划。` : dead
- `tools/niche/index.html` : `输入猫或狗的实足年龄，按物种换算为对应的人类年龄阶段，帮助主人理解宠物的生命阶段与保健重点。用于宠物健康管理科普与兽医沟通。` : dead
- `tools/niche/index.html` : `输入蜂箱数量、花源面积与蜜源类型（油菜、椴树、荔枝等），估算年度可采蜜量并比较不同蜜源产量差异。用于养蜂场产能规划与收益预估。` : dead
- `tools/niche/index.html` : `输入视频时长与目标帧率（24/25/30/60 fps 等），换算总帧数并计算不同帧率间的关系，评估慢放/抽帧效果。用于视频剪辑、动画与帧率匹配。` : dead
- `tools/niche/index.html` : `输入鱼缸长×宽×高（或已有水量），计算实际装水体积与有效水量，并按每厘米鱼长需约 1 升水推荐可养鱼数量与过滤/加热设备配置。用于新手养鱼规划。` : dead
- `tools/niche/index.html` : `选择多肉品种与季节，推荐浇水频率并支持记录每次浇水时间、到期自动提醒，避免烂根或过度干旱。用于多肉爱好者规律养护。` : dead
- `tools/niche/index.html` : `选择植物类型（月季、果树、灌木等）与季节，推荐最佳修剪时间窗口与操作要点，帮助花园维持株型美观与开花结果。用于家庭园艺日程规划。` : dead
- `tools/niche/index.html` : `选择草种（如早熟禾、结缕草等 8 种）与季节，推荐最佳修剪留茬高度并给出不同季节的修剪频率与策略。用于庭院草坪养护，保持草皮健康浓密。` : dead
- `tools/niche/index.html` : `选择陶土类型（低温陶土、高温陶土、瓷土等），查看推荐的烧制温度区间、升温/保温/降温曲线与各阶段关键参数。用于陶艺工作者规划窑炉烧制方案。` : dead
- `tools/niche/index.html` : `陶艺烧制温度曲线推荐工具依据泥料与器型推荐升温、保温与冷却曲线，辅助电窑或气窑的烧成方案制定，适合陶艺创作。` : dead
- `tools/niche/index.html` : `音频采样率转换工具在 kHz 单位间换算采样频率，支持播放与录制参数的格式统一，适合音频处理、降采样与设备兼容。` : dead

### nuclear（dead 10 / dynamic 0 / fragment 0 / harmless 0）

- `tools/nuclear/activity-decay.html` : `A = A₀e^(−λt)。 活度衰减与核数同步。` : dead
- `tools/nuclear/age-from-activity.html` : `t = (1/λ)·ln(N₀/N)。 C-14 减半 → 约 5730 年。` : dead
- `tools/nuclear/carbon-dating-age.html` : `t = T½/ln2 · ln(N₀/N)。 剩 50% 即一个半衰期。` : dead
- `tools/nuclear/decay-fraction.html` : `已衰变份额 = 1 − e^(−λt)` : dead
- `tools/nuclear/mass-defect.html` : `Δm = Zm_p + Nm_n − M。 铁-56：Z=26,N=30。` : dead
- `tools/nuclear/q-value.html` : `Q>0 放能，Q<0 吸能。` : dead
- `tools/nuclear/radioactive-decay.html` : `N = N₀e^(−λt)。 一半衰期后剩约 50%。` : dead
- `tools/nuclear/reaction-rate.html` : `R = ΦσN。 示例 → 1×10⁵ /s。` : dead
- `tools/nuclear/specific-activity.html` : `a = λN_A/M。 碳-14 比活度较低。` : dead
- `tools/nuclear/specific-activity.html` : `碳-14 比活度较低。` : dead

### nutrition（dead 4 / dynamic 8 / fragment 12 / harmless 0）

- `tools/nutrition/generator-nutrition-label.html` : `复制结果` : dead
- `tools/nutrition/generator-nutrition-label.html` : `按 GB 28050 预包装食品营养标签通则：能量 8400 kJ、蛋白质 60g、脂肪 60g、碳水 300g、膳食纤维 25g、钠 2000mg。` : dead
- `tools/nutrition/generator-nutrition-label.html` : `某食品每 100g：蛋白质 10g、脂肪 20g、碳水 55g、膳食纤维 2g、钠 300mg。能量 = 10×17 + 20×37 + 55×17 + 2×8 = 1861 kJ（444.9 kcal）。NRV%：蛋白质 16.7%、脂肪 33.3%、碳水 18.3%、膳食纤维 8.0%、钠 15.0%、能量 22.…(+24字)` : dead
- `tools/nutrition/generator-nutrition-label.html` : `营养（表标签）一键生成。免费在线工具，纯前端处理，数据不上传，保护隐私安全。` : dead

  其它成因样例（共 20 条，仅列前 5）：
  - `tools/nutrition/generator-glucose-load.html` : `碳水` : fragment
  - `tools/nutrition/generator-glucose-load.html` : `每份` : dynamic
  - `tools/nutrition/generator-nutrition-label.html` : `表标签` : fragment
  - `tools/nutrition/generator-nutrition-label.html` : `请至少填写一项营养素含量（g/100g）。` : dynamic
  - `tools/nutrition/generator-nutrition-label.html` : `每 100 g` : fragment

### obstetrics（dead 15 / dynamic 1 / fragment 1 / harmless 0）

- `tools/obstetrics/afi-normal.html` : `羊水指数按四象限深度求和；AFI 5–24 cm 为正常，<5 cm 羊水过少，>24 cm 羊水过多；SDP 2–8 cm 正常。` : dead
- `tools/obstetrics/biyun-pearlzhishu-shibailv.html` : `指数 = （意外妊娠数 × 12 × 100` : dead
- `tools/obstetrics/cycle-8.html` : `：排卵前 <7mm 可能影响着床；>14mm 需警惕内膜病变` : dead
- `tools/obstetrics/down-screening.html` : `母血胎儿DNA，对21/18/13三体检出率>99%，假阳性<1%` : dead
- `tools/obstetrics/ectopic-hcg.html` : `hCG阳性+超声未见宫内孕囊(需排除hCG<2000的"鉴别区")` : dead
- `tools/obstetrics/ectopic-hcg.html` : `升高 < 53%` : dead
- `tools/obstetrics/ectopic-hcg.html` : `正常宮内孕婚 48h hCG 增幅≥ 66%（<1500）/≥ 53%（1500–3000）/≥ 30%（>3000）；≤ 正常下限需警惕异位孕婚。` : dead
- `tools/obstetrics/ectopic-hcg.html` : `注：hCG越高倍增越慢。初始hCG<1500时48h应升高≥66%为宫内妊娠；升高<53%高度怀疑异位妊娠或流产。` : dead
- `tools/obstetrics/fetal-movement-count.html` : `12 小时肾动数 = (早 + 中 + 晚 各段计数) × 4；≥ 30 正常，20–29 临界，< 20 偏少` : dead
- `tools/obstetrics/labor-curve.html` : `宫口扩张<1cm/h×4h为活跃期延长` : dead
- `tools/obstetrics/ovarian-reserve.html` : `AMH 分级：<0.5 极低、<1.0 低、<3.5 正常、<6.0 偏高、≥ 6.0 极高；FSH < 10 正常；AFC ≥ 8 正常` : dead
- `tools/obstetrics/postpartum-hemorrhage.html` : `失血量 ≥ 500 mL 为产后出血；SI < 0.9 正常、0.9–1.1 轻度、1.1–1.5 中度、> 1.5 重度伤克。` : dead
- `tools/obstetrics/preeclampsia-prediction.html` : `血管生成比值 = sFlt-1 / PlGF；< 38 排除（1周 NPV 99.3%），38–85(早发)/110(晚发) 灰色区，≥ 阈值 确诊` : dead
- `tools/obstetrics/yangshuizhishu-afi-zhengchangfanwei.html` : `AFI < 5 cm 羊水过少、5–8 cm 临界、8–25 cm 正常、> 25 cm 羊水过多；MVP < 2 过少、2–8 正常、> 8 过多。` : dead
- `tools/obstetrics/yangshuizhishu-afi-zhengchangfanwei.html` : `AFI = 四象限羊水池深度之和；MVP = 最大垂直羊水池深度` : dead

  其它成因样例（共 2 条，仅列前 5）：
  - `tools/obstetrics/calc-50.html` : `出血量 = 血容量 × (Hct前 − Hct后) / Hct前` : fragment
  - `tools/obstetrics/rater-26.html` : `<3次/天 (1分)` : dynamic

### ophthalmology（dead 12 / dynamic 6 / fragment 1 / harmless 0）

- `tools/ophthalmology/convert-42.html` : `20 英尺（20/xx）与 6 米（6/xx）记法如何统一？` : dead
- `tools/ophthalmology/convert-42.html` : `两套分子只是检查距离不同：6/6 ≡ 20/20、6/12 ≡ 20/40。统一先转小数（分子/分母），再转 logMAR 或五分记录法，结果一致。` : dead
- `tools/ophthalmology/corneal-endothelium.html` : `CD ≥ 2500 正常、1500–2500 临界、< 1500 低密度；CV < 0.30 正常、0.30–0.40 临界、> 0.40 异常；六角形比例 ≥ 55% 正常、50%–55% 临界。` : dead
- `tools/ophthalmology/iol-power.html` : `SRK II：P = A′ − 0.9K − 2.5L（A′ 随眼轴分段校正）；SRK/T：P = 1336/(AL − ELP) − 1336/(1336/K − ELP)，ELP = pACD + H，pACD = 0.62467A − 68.747，R = 337.5/K，H = R − √(R² − (Cw/2…(+100字)` : dead
- `tools/ophthalmology/iop-correction.html` : `CCT 偏离均值越远、各经验系数差异越大；均值可减低单一公式偏差，但校正值仍不能替代直接眼压测量。` : dead
- `tools/ophthalmology/iop-correction.html` : `Ehlers=18+(520−550)×0.071=15.87；Doughty=18+(542−550)×0.02=17.84；Feltgen=18+(550−550)×0.03=18；三式均值≈17.2 mmHg（比值法=17.02，仅参考）。` : dead
- `tools/ophthalmology/iop-correction.html` : `三公式差异大说明什么？` : dead
- `tools/ophthalmology/iop-correction.html` : `同时给 Ehlers/Doughty/Feltgen 三种已发表公式并取均值；比值法仅作换算参考，不纳入均值。` : dead
- `tools/ophthalmology/iop-correction.html` : `眼压角膜厚度多公式校正：Ehlers = IOP +（520 − CCT）× 0.071；Doughty = IOP +（542 − CCT）× 0.020；Feltgen = IOP +（550 − CCT）× 0.030；比值法 = IOP × 520 ÷ CCT。取 Ehlers/Doughty/Feltgen …(+49字)` : dead
- `tools/ophthalmology/iop-correction.html` : `眼压角膜厚度多公式校正：Ehlers = IOP +（520 − CCT）× 0.071；Doughty = IOP +（542 − CCT）× 0.020；Feltgen = IOP +（550 − CCT）× 0.030；比值法 = IOP × 520 ÷ CCT；取四式均值与最值，CCT 小于500μm 读数偏低…(+2字)` : dead
- `tools/ophthalmology/osdi-scale.html` : `OSDI = (各题得分之和 × 100) / (已答题数 × 4)` : dead
- `tools/ophthalmology/visual-acuity-converter.html` : `每行 5 个字母、每字母 0.02 log 单位：logMAR = 1.10 &minus; 0.02 &times; 正确字母数；0–70 字母，20/20 = 55、20/10 = 70、&lt;20/200 计 0` : dead

  其它成因样例（共 7 条，仅列前 5）：
  - `tools/ophthalmology/convert-42.html` : `请输入有效数值：小数视力 0.01–2.0、logMAR −0.3–2.0、Snellen 分母 2–400（20/xx）；空值或越界不换算。` : dynamic
  - `tools/ophthalmology/iol-power.html` : `SRK II：P = A′ − 0.9K − 2.5L（A′ 随眼轴分段校正）；SRK/T：P = 1336/(AL − ELP) − 1336/(1336/K − ELP)，ELP = pACD + H，pACD = 0.62467A − 68.747，R = 337.5/K，H = R − √(R² − (Cw/2…(+3字)` : fragment
  - `tools/ophthalmology/iol-power.html` : `请输入有效参数：眼轴 15–36 mm、角膜曲率 30–60 D、A 常数 100–130；空值或越界不做计算。` : dynamic
  - `tools/ophthalmology/iop-correction.html` : `请输入有效眼压（1–80 mmHg）与角膜中央厚度（300–800 μm）；空值或越界不做校正。` : dynamic
  - `tools/ophthalmology/iop-correction.html` : `校正后眼压(三公式估算均值)：` : dynamic

### optical（dead 14 / dynamic 0 / fragment 1 / harmless 0）

- `tools/optical/checker-stress.html` : `光学元件双折射：精密级<10nm/cm，普通级<50nm/cm` : dead
- `tools/optical/checker-stress.html` : `钢化玻璃残余应力：表面压应力应>90MPa，中心张应力<45MPa` : dead
- `tools/optical/convergence-near-point.html` : `集合近点过远(>10cm)提示集合不足，常见于阅读疲劳、复视；过近(<3cm)可能集合过强。需结合聚散功能综合评估。` : dead
- `tools/optical/driving-lens.html` : `夜间驾驶严禁使用深色太阳镜（VLT<75%），会严重影响视野和反应速度。` : dead
- `tools/optical/gaussian-beam-waist.html` : `w₀ = 4λf/(πD) 计算束腰半径` : dead
- `tools/optical/lens-maker.html` : `符号约定：凸面 R>0、凹面 R<0（光线从左入射）。` : dead
- `tools/optical/lens-power-diopter.html` : `屈光度单位 D = m⁻¹；凸透镜 P>0（远视/老花），凹透镜 P<0（近视）。` : dead
- `tools/optical/mirror-imaging.html` : `凹面镜 f>0、凸面镜 f<0（此处曲率半径符号决定）。` : dead
- `tools/optical/peripheral-defocus.html` : `RPD>0 为近视性离焦，RPD<0 为远视性离焦；结合镜片类型评估近视防控效能。` : dead
- `tools/optical/peripheral-defocus.html` : `相对周边离焦 RPD = 周边屈光度 − 中央屈光度（D）` : dead
- `tools/optical/pupil-height.html` : `瞳高占 B 值比例 = 瞳高(mm) / 镜框 B 值(mm) × 100%` : dead
- `tools/optical/snell-refraction.html` : `n₁·sinθ₁ = n₂·sinθ₂ 计算折射角` : dead
- `tools/optical/thin-lens-imaging.html` : `1/f = 1/u + 1/v（实物距 u>0，凸透镜 f>0）。 像距 v>0 为实像（屏可接收），v` : dead
- `tools/optical/thin-lens-imaging.html` : `像距 v>0 为实像（屏可接收），v<0 为虚像；放大率 m<0 表示倒立。` : dead

  其它成因样例（共 1 条，仅列前 5）：
  - `tools/optical/frame-pupillary.html` : `单眼移心量 = (A + DBL) / 2 − PD / 2` : fragment

### optics（dead 3 / dynamic 3 / fragment 0 / harmless 0）

- `tools/optics/magnification-optics.html` : `|M|>1 放大、<1 缩小。` : dead
- `tools/optics/mirror-equation.html` : `凹镜 f>0、凸镜 f<0。` : dead
- `tools/optics/single-slit-diffraction.html` : `sinθ = mλ。 第一暗纹 m=1。` : dead

  其它成因样例（共 3 条，仅列前 5）：
  - `tools/optics/single-slit-diffraction.html` : `⚠ 缝宽 a 必须大于 0。` : dynamic
  - `tools/optics/single-slit-diffraction.html` : `⚠ 波长 λ 必须大于 0（λ=0 不会形成衍射条纹）。` : dynamic
  - `tools/optics/single-slit-diffraction.html` : `⚠ 暗纹级次 m 必须为非零整数（±1、±2、±3…）；0 级是中央亮纹，不是暗纹。` : dynamic

### pediatrics（dead 23 / dynamic 29 / fragment 3 / harmless 2）

- `tools/pediatrics/assessor-spo2.html` : `SpO2 <90%（任何部位）：CCHD筛查阳性，需紧急评估` : dead
- `tools/pediatrics/assessor-spo2.html` : `早产儿（<37周）` : dead
- `tools/pediatrics/diarrhea-dehydration.html` : `Plan C：静脉补液 100 mL/kg，3–6 小时；<12 月：30 mL/kg 1 小时内 + 70 mL/kg 5 小时；≥12 月：30 mL/kg 30 分钟内 + 70 mL/kg 2.5 小时` : dead
- `tools/pediatrics/diarrhea-dehydration.html` : `核心计算公式（按输入变量）：weight×deficit×1000；freq×10×weight÷10` : dead
- `tools/pediatrics/mchat-autism.html` : `提示：M-CHAT-R适用于16-30月龄儿童。关键题项(2,5,12)：若任何关键题未通过，即使总分<3也需随访。关键题：5(对呼名反应)、2(对兴趣指物)、12(模仿)。筛查阳性≠确诊ASD，需经ADOS/ADI-R等诊断评估确认。ASD核心症状：社交沟通障碍、刻板重复行为、兴趣狭窄。18月和24月是推荐筛查时间点…(+11字)` : dead
- `tools/pediatrics/neonatal-jaundice.html` : `48 小时 TSB 10 mg/dL、胎龄 38 周：位于 p40–p75 之间（中低危险区）；低危足月儿 48–72h 光疗阈值 18 mg/dL，10<18 暂不需光疗，密切监测随访。` : dead
- `tools/pediatrics/neonatal-jaundice.html` : `48 小时 TSB 14 mg/dL、胎龄 38 周：Bhutani ≥95 百分位（P95≈12），属高危险区；本页 AAP 2004 低危光疗阈值 18，14<18 暂不需光疗，但需密切随访并按 AAP 2022 阈值复核。` : dead
- `tools/pediatrics/neonatal-jaundice.html` : `48h 同值 14：中危（≥38 周伴危险因素或 35–37 周无危险因素）阈值 15，未达；高危（35–37 周伴危险因素）阈值 13，已超过需光疗；<35 周应按 2022 AAP 早产儿曲线复核。` : dead
- `tools/pediatrics/neonatal-jaundice.html` : `光疗/换血阈值为 AAP 2004 小时胆红素曲线近似值（AAP 2022 已取代 2004，临床以 2022 版为准），需临床复核；胎龄 <35 周应按 2022 AAP/NICHD 早产儿曲线单独评估。` : dead
- `tools/pediatrics/neonatal-jaundice.html` : `光疗阈值(mg/dL)` : dead
- `tools/pediatrics/neonatal-jaundice.html` : `同值若 35–37 周且无危险因素（本页中危 48–72 h 阈值 15），14<15 暂不达光疗；若伴危险因素（高危阈值 13），14≥13 需光疗；<35 周应按 2022 AAP 早产儿曲线复核。` : dead
- `tools/pediatrics/neonatal-jaundice.html` : `如 14` : dead
- `tools/pediatrics/neonatal-jaundice.html` : `换血阈值(mg/dL)` : dead
- `tools/pediatrics/neonatal-jaundice.html` : `表中为≥38 周、无神经毒性风险因素足月儿的 AAP 2004 小时胆红素曲线近似阈值（与本工具计算口径一致）。AAP 2022（Kemper et al., Pediatrics 2022;150(3):e2022060643）已取代 AAP 2004，临床应以 2022 版小时胆红素阈值图为准。35–37 周或存在…(+54字)` : dead
- `tools/pediatrics/neonatal-jaundice.html` : `表中为≥38 周、无神经毒性风险因素足月儿的阈值（与本工具计算口径一致）。35–37 周或存在溶血/G6PD/败血症等风险因素时按中危下调约 2 mg/dL，<35 周按高危下调约 4–5 mg/dL。` : dead
- `tools/pediatrics/pediatric-anemia.html` : `1 岁属 6–23 月档，Hb 阈值 105；Hb 90 为中度贫血（70–99）；铁蛋白<12、MCV<70→缺铁性，铁剂 4mg/kg×10kg=40mg/日。` : dead
- `tools/pediatrics/pediatric-anemia.html` : `提示：缺铁性贫血(IDA)是最常见的儿童贫血类型。铁缺乏分三期：1.铁减少期(SF<12μg/L,Hb正常)；2.缺铁性红细胞生成(SF<12,MCV<正常,Hb正常)；3.缺铁性贫血(SF<12,MCV低,Hb低)。补铁首选口服二价铁(元素铁3-6mg/kg/日)，餐间服用+维C促吸收。治疗4周复查Hb，纠正后继续补…(+45字)` : dead
- `tools/pediatrics/pediatric-anemia.html` : `提示：铁缺乏分三期：1.铁减少期(SF<12μg/L,Hb正常)；2.缺铁性红细胞生成(SF<12,MCV<正常,Hb正常)；3.缺铁性贫血(SF<12,MCV低,Hb低)。补铁首选口服二价铁(元素铁3-6mg/kg/日)，餐间服用+维C促吸收。治疗4周复查Hb，纠正后继续补铁2-3月补足储存铁。早产儿2周龄起预防性补…(+23字)` : dead
- `tools/pediatrics/pediatric-asthma.html` : `提示：C-ACT适用于4-11岁儿童(7道题由儿童自答+家长答)，ACT适用于≥12岁。评估近4周情况。哮喘长期管理目标：达到并维持控制，预防急性发作，维持正常肺功能。ICS(吸入糖皮质激素)是长期控制首选。急性发作PEF<60%预计值需就医。本工具仅供临床参考，不替代专业医疗评估。` : dead
- `tools/pediatrics/pediatric-pneumonia.html` : `提示：呼吸增快是诊断肺炎最敏感的体征。胸凹陷(下胸壁内陷)提示重症。低氧血症(SpO2<90%)需氧疗。新生儿肺炎表现不典型(口吐白沫/呼吸暂停)。重度肺炎需排查并发症(脓胸/脓气胸/ARDS)。本工具仅供临床参考。` : dead
- `tools/pediatrics/rater-27.html` : `Z < -3：严重低于标准；Z < -2：中度低于标准；Z > 2：高于标准；Z > 3：严重高于标准` : dead
- `tools/pediatrics/xinshengerhuangdan-xiaoshidanhongsu-quxian.html` : `Bhutani ≥95 百分位（48h P95≈12）；低风险 AAP 2022 简化光疗阈值 13.5 mg/dL → 14≥13.5，需光疗。` : dead
- `tools/pediatrics/xinshengerhuangdan-xiaoshidanhongsu-quxian.html` : `胎龄<38 周或高危，48h 光疗阈值降至≈11 mg/dL，列线图整体左移。` : dead

  其它成因样例（共 34 条，仅列前 5）：
  - `tools/pediatrics/dehydration-assessment.html` : `请输入有效体重（0.5–100 kg）；空值或越界不做判读。` : dynamic
  - `tools/pediatrics/dehydration-assessment.html` : `按需口服补液，继续喂养；无需静脉补液。` : dynamic
  - `tools/pediatrics/diarrhea-dehydration.html` : `请输入有效年龄（0–60 月）、体重（0.5–100 kg）、腹泻次数（1–30 次/日）与病程（0–30 天）；空值或越界不做判读。` : dynamic
  - `tools/pediatrics/diarrhea-dehydration.html` : `补液方案（WHO 2005 Plan A/B/C）` : dynamic
  - `tools/pediatrics/diarrhea-dehydration.html` : `Plan A：每次稀便后补充 ORS，<2 岁 50–100 mL/次、≥2 岁 100–200 mL/次` : dynamic

### pet（dead 15 / dynamic 2 / fragment 3 / harmless 6）

- `tools/pet/checker-16.html` : `合规等级：≥90分优秀，75-89良好，60-74一般，<60不合格` : dead
- `tools/pet/index.html` : `宠物养护工具集合收录了 9 个免费在线工具，覆盖宠物养护场景下的常见计算、换算与查询需求。无论你是相关领域的从业者、学生还是普通用户，都能在这里找到即用即走的实用小工具。所有工具纯前端运行，数据不上传服务器，保护隐私安全。` : dead
- `tools/pet/index.html` : `宠物喂食量计算` : dead
- `tools/pet/index.html` : `宠物喂食量计算是一款免费的在线宠物养护工具，宠物喂食量计算是一款免费的在线宠物养护工具，输入参数即可实时得出结果；纯前端运行、数据不上传、无需注册，打开浏览器即可使用。纯前端运行、数据不上传、无需注…` : dead
- `tools/pet/pet-age-converter.html` : `犬种体型/猫龄类型` : dead
- `tools/pet/pet-age-converter.html` : `犬龄换算人类年龄：前 2 年每年折约 12 至 15 岁（1 岁约 15 岁、2 岁约 24 岁），其后按体型每年加 4 至 7 岁（小型犬 4、中型 5、大型 6、超大型 7）；猫龄前 2 年分别折 15 岁与 9 岁，其后每年加 4 岁；人类等效年龄超过 7 岁为成年后期、超过 10 岁为老年期，应加强关节、口腔与…(+7字)` : dead
- `tools/pet/pet-age-converter.html` : `狗狗猫咪年龄转换为人类等效年龄（仅近似参考）。` : dead
- `tools/pet/pet-feeding-calc.html` : `/ 宠物喂食量计算` : dead
- `tools/pet/pet-feeding-calc.html` : `中等活动` : dead
- `tools/pet/pet-feeding-calc.html` : `增重/增肌` : dead
- `tools/pet/pet-feeding-calc.html` : `按体重、年龄与活动度估算日均热量需求与日喂粮量（g）。` : dead
- `tools/pet/pet-feeding-calc.html` : `活动等级` : dead
- `tools/pet/pet-feeding-calc.html` : `静息能量需求 RER(kcal/天) = 70 × 体重(kg) 的 0.75 次方；每日能量需求 DER = RER × 系数（幼年 2.5 至 3.0、绝育成年 1.6、未绝育成年 1.8、老年 1.2 至 1.4、减重期 0.8 至 1.0、增重期 1.2 至 1.8）；每日喂食量(g) = DER ÷ 每克饲料…(+47字)` : dead
- `tools/pet/pet-feeding-calc.html` : `非常活跃` : dead
- `tools/pet/pet-feeding-calc.html` : `食物热量（kcal/100g）` : dead

  其它成因样例（共 11 条，仅列前 5）：
  - `tools/pet/aquarium-light.html` : `🎯 水草光照需求分类` : harmless
  - `tools/pet/pet-age-converter.html` : `🐾 宠物年龄换算` : harmless
  - `tools/pet/pet-age-converter.html` : `/ 宠物年龄换算` : fragment
  - `tools/pet/pet-age-converter.html` : `📖 查看「pet-age-converter 使用指南」` : harmless
  - `tools/pet/pet-age.html` : `🐾 宠物年龄换算` : harmless

### petrochem（dead 1 / dynamic 0 / fragment 0 / harmless 0）

- `tools/petrochem/pipe-pressure.html` : `过渡流：流量 100 m³/h、管径 200 mm、管长 500 m、密度 900、黏度 50 mPa·s、粗糙度 0.1 mm。流速=0.884 m/s；Re=ρvD/μ=900×0.884×0.2/0.05≈3183(湍流区)；Swamee-Jain f≈0.0442；总压降=0.0442×(500/0.2)×(9…(+166字)` : dead

### photo（dead 23 / dynamic 0 / fragment 3 / harmless 0）

- `tools/photo/bracketing-plan.html` : `张数 = 范围/步进 + 1；覆盖 [基准−范围/2, 基准+范围/2]` : dead
- `tools/photo/card-capacity.html` : `张数 = 容量(GB)×1000 / 单张大小(MB)` : dead
- `tools/photo/convert-focal.html` : `千视场角换算` : dead
- `tools/photo/convert-focal.html` : `千镜头焦距` : dead
- `tools/photo/convert-focal.html` : `毫视场角换算` : dead
- `tools/photo/convert-focal.html` : `毫镜头焦距` : dead
- `tools/photo/depth-of-field.html` : `H = f²/(N·c) + f；近/远 = H·S/(H±(S−f))` : dead
- `tools/photo/dpi.html` : `DPI = 像素数 / 英寸长度` : dead
- `tools/photo/dpi.html` : `英寸 = 厘米 / 2.54` : dead
- `tools/photo/dynamic-range.html` : `DR = log₂(最亮/最暗)` : dead
- `tools/photo/flash-gn.html` : `光圈 = GN / 距离（ISO100）` : dead
- `tools/photo/golden-hour.html` : `日长 = 2·acos(−tanφ·tanδ)/15 小时` : dead
- `tools/photo/macro-magnification.html` : `放大率 m = f/(S−f)` : dead
- `tools/photo/nd-filter.html` : `新快门 = 基准 × 2^档数` : dead
- `tools/photo/photo-10.html` : `张数 = 2 × ceil(总范围 / 步长) + 1` : dead
- `tools/photo/photo-3.html` : `ISO 加倍，距离 ×√2` : dead
- `tools/photo/photo-5.html` : `对焦 H 时，景深从 H/2 到无穷远` : dead
- `tools/photo/photo-6.html` : `视角 = 2 · arctan(传感器边长 / (2 · 焦距))` : dead
- `tools/photo/photo-7.html` : `放大倍率 = 成像大小 / 实际大小` : dead
- `tools/photo/photo-8.html` : `压缩后 ≈ 未压缩 / 压缩比` : dead
- `tools/photo/photo-8.html` : `未压缩大小 = 像素数 × 位深 / 8` : dead
- `tools/photo/raw-size.html` : `大小 = 像素 × 位深 / 8` : dead
- `tools/photo/safe-shutter.html` : `安全快门 ≈ 1/(焦距 × 裁剪系数)` : dead

  其它成因样例（共 3 条，仅列前 5）：
  - `tools/photo/convert-focal.html` : `镜头焦距` : fragment
  - `tools/photo/convert-focal.html` : `视场角换算` : fragment
  - `tools/photo/equivalent-focal.html` : `等效焦距 = 实际焦距 × 裁剪系数` : fragment

### photo2（dead 1 / dynamic 5 / fragment 0 / harmless 0）

- `tools/photo2/exposure-triangle.html` : `EV（曝光值）Formula:` : dead

  其它成因样例（共 5 条，仅列前 5）：
  - `tools/photo2/exposure-triangle.html` : `调整档位` : dynamic
  - `tools/photo2/exposure-triangle.html` : `ISO（固定）` : dynamic
  - `tools/photo2/exposure-triangle.html` : `偏差` : dynamic
  - `tools/photo2/exposure-triangle.html` : `等量曝光：固定 ISO，光圈按 2^(s/2)、快门按 2^s 同时调整，保持 N²/t 不变，总进光量不变` : dynamic
  - `tools/photo2/exposure-triangle.html` : `请选择有效的光圈、快门与 ISO（ISO 不能为空）。` : dynamic

### plastic（dead 1 / dynamic 2 / fragment 1 / harmless 0）

- `tools/plastic/extrusion-rate.html` : `螺杆直径 10 mm、螺槽深 1 mm、螺距 5 mm、转速 10 rpm、密度 0.92、效率 90%。流道截面积 = π/4×(10²−(10−2)²) = π/4×36 ≈ 28.27 mm²；每转排量 28.27×5 ≈ 141.4 mm³；每分钟 1414 mm³、每秒 23.6 mm³；质量产量 = 23.…(+64字)` : dead

  其它成因样例（共 3 条，仅列前 5）：
  - `tools/plastic/extrusion-rate.html` : `请输入有效参数：所有参数需大于 0，输送效率需在 0–100% 之间` : dynamic
  - `tools/plastic/extrusion-rate.html` : `请输入有效参数：螺槽深度过大，请检查` : dynamic
  - `tools/plastic/injection-cycle.html` : `注塑成型周期 = 注射 + 保压 + 冷却 + 开模 + 顶出 + 关模` : fragment

### pr（dead 1 / dynamic 2 / fragment 2 / harmless 0）

- `tools/pr/assessor-59.html` : `关键信息渗透率 = 包含核心传播信息的报道/总报道` : dead

  其它成因样例（共 4 条，仅列前 5）：
  - `tools/pr/analysis-density-1.html` : `总词数 = 中文字符数 + 英文单词数` : fragment
  - `tools/pr/analysis-density-1.html` : `关键词密度 = 关键词出现次数 ÷ 总词数 × 100%` : fragment
  - `tools/pr/assessor-59.html` : `2-正面<40%` : dynamic
  - `tools/pr/assessor-59.html` : `1-<20%覆盖` : dynamic

### printing（dead 7 / dynamic 15 / fragment 6 / harmless 0）

- `tools/printing/analysis-7.html` : `平均亮度 L̄ = Σ Li ÷ n` : dead
- `tools/printing/convert-gsm.html` : `千厚度换算` : dead
- `tools/printing/convert-gsm.html` : `千纸张克重` : dead
- `tools/printing/convert-gsm.html` : `毫厚度换算` : dead
- `tools/printing/convert-gsm.html` : `毫纸张克重` : dead
- `tools/printing/estimate-ink.html` : `损耗墨量(5%)` : dead
- `tools/printing/sheet-calc.html` : `全张用纸量 = 印张 × 册数 × (1 + 加放率)` : dead

  其它成因样例（共 21 条，仅列前 5）：
  - `tools/printing/analysis-7.html` : `照度均匀度 U₁ = 最小亮度 ÷ 平均亮度` : fragment
  - `tools/printing/box-area.html` : `表面积 = 2×(L×W + L×H + W×H)` : fragment
  - `tools/printing/convert-gsm.html` : `纸张克重` : fragment
  - `tools/printing/convert-gsm.html` : `厚度换算` : fragment
  - `tools/printing/convert-gsm.html` : `定量 GSM 需填写大于 0 的数值（g/m²）` : dynamic

### process（dead 10 / dynamic 1 / fragment 0 / harmless 0）

- `tools/process/cp-index.html` : `σ=0.01 → Cp=1.667。 Cp≥1.33 通常视为合格。` : dead
- `tools/process/cpk-index.html` : `Cpk=Cp。 Cpk≥1.33 为过程能力充足。` : dead
- `tools/process/defect-probability.html` : `z=5 → 概率约 2.87e-7。 对称时总缺陷为两侧之和。` : dead
- `tools/process/dpmo-calc.html` : `20000×1e6 = 6200 DPMO。 机会数指可缺陷的特征数。` : dead
- `tools/process/first-pass-yield.html` : `FPY = 良品数 / 投入数` : dead
- `tools/process/measurement-uncertainty.html` : `√0.38≈0.616。 分量应相互独立。` : dead
- `tools/process/rolled-throughput-yield.html` : `98%×97%×99% ≈ 94.11%。 工序越多 RTY 越低。` : dead
- `tools/process/tolerance-rss.html` : `√0.0725≈0.269。 RSS 比最差情况宽松。` : dead
- `tools/process/tolerance-worst-case.html` : `0.2 = 0.45。 最差情况偏保守。` : dead
- `tools/process/xbar-control-limits.html` : `σ=2、n=5 → 界限 ±2.683。 σ/√n 为均值标准误。` : dead

  其它成因样例（共 1 条，仅列前 5）：
  - `tools/process/cpk-index.html` : `⚠ 输入无效：过程标准差 σ 须大于 0，且上规格限 USL 须大于下规格限 LSL。` : dynamic

### procurement（dead 7 / dynamic 1 / fragment 0 / harmless 0）

- `tools/procurement/assessor-26.html` : `供应商准入分 = 指标加权` : dead
- `tools/procurement/assessor-26.html` : `分级标准：≥85分战略供应商，70-84优选，60-69合格，<60淘汰` : dead
- `tools/procurement/rater-price.html` : `供应商评分 = 综合加权` : dead
- `tools/procurement/stats-on-time-1.html` : `准时 255 批、合格 270 批、准时且合格 240 批。准时率=255/300=85.00%，良品率=270/300=90.00%，联合合格率=240/300=80.00%，准时不良率=(255−240)/300=5.00%，未达标率=(300−240)/300=20.00%。` : dead
- `tools/procurement/stats-on-time-1.html` : `输入当月交货总批次、准时批次、合格批次与「准时且合格」批次（取交集），自动计算准时率、良品率、联合合格率、准时但不良率与未达标率，用于供应商绩效考评。` : dead
- `tools/procurement/supplier-score.html` : `综合评分 = 质量×交期×价格×服务` : dead
- `tools/procurement/zhaobiao-gongkai-yaoqing-jingzheng-fangshi.html` : `金额≥400 且 公开→公开招标；金额≥400 且 限定→邀请招标；金额<400→竞争性谈判` : dead

  其它成因样例（共 1 条，仅列前 5）：
  - `tools/procurement/zhaobiao-gongkai-yaoqing-jingzheng-fangshi.html` : `💡 金额≥400 且公开→公开招标；限定→邀请招标；<400→竞争性谈判。` : dynamic

### project（dead 1 / dynamic 3 / fragment 6 / harmless 0）

- `tools/project/analysis-28.html` : `关注度 = 权力 × 利益；按「高/低权 × 高/低利」落入四象限` : dead

  其它成因样例（共 9 条，仅列前 5）：
  - `tools/project/assessor-risk-9.html` : `1-极低（<10%）` : dynamic
  - `tools/project/checker-training-hr-1.html` : `HSE 关键项存在 0 分项，触发一票否决规则：不得评为优秀或合格，本次评级降为不合格；请立即整改关键项后重新评估。` : dynamic
  - `tools/project/checker-training-hr-1.html` : `不达标关键项` : dynamic
  - `tools/project/checker-training-hr-1.html` : `安全培训档案` : fragment
  - `tools/project/checker-training-hr-1.html` : `特种作业持证` : fragment

### property（dead 11 / dynamic 0 / fragment 0 / harmless 0）

- `tools/property/calc-shared-property-fee.html` : `物业费 = 面积 × 单价` : dead
- `tools/property/checker-7.html` : `综合得分≥85分为优秀，70-84分为良好，55-69分为合格，<55分为不合格` : dead
- `tools/property/cleaning-allocation.html` : `保洁分配 = 区域/频次覆盖` : dead
- `tools/property/elevator-energy.html` : `电梯能耗 = 次数 × 单次能耗` : dead
- `tools/property/energy.html` : `运费 = 重量 × 运费率（元/kg）；吨均运费 = 运费率 × 1000` : dead
- `tools/property/fee-allocation.html` : `物业费分摊 = 面积比例` : dead
- `tools/property/irrigation-schedule.html` : `浇灌排程 = 需水量/流量` : dead
- `tools/property/rater-performance.html` : `绩效考核 = 指标加权评分` : dead
- `tools/property/rater-performance.html` : `💡 加权得分 = Σ(各维度得分 × 权重) / Σ权重。考核等级：A级(≥90)优秀 / B级(80-89)良好 / C级(70-79)合格 / D级(60-69)待改进 / E级(<60)不合格。维度得分参考：满意度调查均分、设施完好率、工单响应时间达标率、实际收费率、安全检查通过率、环境巡查合格率。` : dead
- `tools/property/stats-manager.html` : `临停位周转率 = 当日临停车次 ÷ 临停车位` : dead
- `tools/property/stats-manager.html` : `预计月收入 = 临停车次 × 时长 × 单价 × 30 + 包月车位 × 月租` : dead

### psychiatry（dead 2 / dynamic 0 / fragment 0 / harmless 0）

- `tools/psychiatry/eat26-eating.html` : `EAT-26总分 = Σ26个条目（含反向计分条目按REVERSE/NORMAL加权）；<20低风险、≥20提示进食障碍风险，需专业评估。` : dead
- `tools/psychiatry/rater-24.html` : `心理韧性总分 = Σ各条目（0-4），满分 = 题数×4；得分率 = 总分÷满分×100%；≥80高韧性、65-79中高、50-64中等、<50待提升。` : dead

### pulmonology（dead 11 / dynamic 25 / fragment 1 / harmless 0）

- `tools/pulmonology/lung-rads.html` : `实性结节 6mm→2 类，12 月低剂量 CT 随访。` : dead
- `tools/pulmonology/lung-rads.html` : `部分实性>10mm` : dead
- `tools/pulmonology/lung-rads.html` : `部分实性成分>10mm→4A/4B 类，建议 3 月复查或 PET-CT/活检。` : dead
- `tools/pulmonology/pneumothorax.html` : `气胸肺压缩比 ≈ 三处肋间测量平均距离 × 10（上限 100%）；压缩 小于20% 且无症状可观察并吸高浓度氧，继发性或张力性气胸需胸腔闭式引流或紧急排气。` : dead
- `tools/pulmonology/pulmonary-function.html` : `本工具 cutoff 可设(默认 0.7)，老年建议按 LLN。` : dead
- `tools/pulmonology/rater-13.html` : `三分类法：<2分低风险，2-6分中风险，>6分高风险` : dead
- `tools/pulmonology/respiratory-failure.html` : `氧合指数 P/F = PaO₂ / FiO₂` : dead
- `tools/pulmonology/tb-resistance.html` : `MDR/RR + 耐氟喹诺酮 + 耐至少一种二线注射剂` : dead
- `tools/pulmonology/tb-resistance.html` : `MDR/RR + 耐氟喹诺酮 或 二线注射剂` : dead
- `tools/pulmonology/tb-resistance.html` : `提示：涂片阳性提示传染性强，需呼吸道隔离。GeneXpert利福平耐药需经表型药敏确认。BPaL/BPaLM方案(贝达喹啉+普托马尼+利奈唑胺±莫西沙星)适用于≥6岁、无氟喹诺酮及注射剂耐药的MDR/RR-TB。仅供临床参考。` : dead
- `tools/pulmonology/tb-resistance.html` : `结核耐药分型：无利福平及异烟肼耐药为药物敏感结核 DS-TB（2HRZE/4HR）；耐利福平为 RR-TB、同时耐异烟肼为耐多药 MDR-TB、再加氟喹诺酮及二线注射剂耐药为广泛耐药 XDR-TB，据耐药谱选方案。` : dead

  其它成因样例（共 26 条，仅列前 5）：
  - `tools/pulmonology/niv-settings.html` : `压力支持 PS = IPAP − EPAP` : dynamic
  - `tools/pulmonology/pneumothorax.html` : `依据立位后前位胸片测量胸膜间距，采用 Rhea 法估算气胸肺压缩百分比` : dynamic
  - `tools/pulmonology/pneumothorax.html` : `请填写 A/B/C 三处胸膜间距（≥0 的有效数字）；空值或负值不会被当作 0 给出压缩比例。` : dynamic
  - `tools/pulmonology/pneumothorax.html` : `三处胸膜间距均为 0，无法估计气胸压缩比例；请核对测量值。` : dynamic
  - `tools/pulmonology/pneumothorax.html` : `创伤性气胸需先按 ATLS 评估合并伤，排查开放性/张力性气胸与血气胸；多数需胸腔闭式引流，由急诊/创伤团队复核。` : dynamic

### quality（dead 4 / dynamic 0 / fragment 1 / harmless 0）

- `tools/quality/convert-qualified-defect.html` : `千PPM换算` : dead
- `tools/quality/convert-qualified-defect.html` : `千不合格品率` : dead
- `tools/quality/convert-qualified-defect.html` : `毫PPM换算` : dead
- `tools/quality/convert-qualified-defect.html` : `毫不合格品率` : dead

  其它成因样例（共 1 条，仅列前 5）：
  - `tools/quality/convert-qualified-defect.html` : `不合格品率` : fragment

### quantum（dead 5 / dynamic 9 / fragment 1 / harmless 0）

- `tools/quantum/cyclotron-frequency.html` : `ω = qB/m（与速度无关）。 用于回旋加速器设计。` : dead
- `tools/quantum/pair-production-threshold.html` : `光子产生正负电子对所需最小能量。` : dead
- `tools/quantum/pair-production-threshold.html` : `需 ≥ 两电子静能之和。` : dead
- `tools/quantum/photoelectric-effect.html` : `K_max = hf − φ。 f 需 > φ/h 才逸出。` : dead
- `tools/quantum/rydberg-wavelength.html` : `R≈1.097e7 m⁻¹。 n:3→2 为巴耳末 α 线 ≈ 656 nm。` : dead

  其它成因样例（共 10 条，仅列前 5）：
  - `tools/quantum/infinite-well-energy.html` : `⚠ 量子数 n 必须为正整数（1、2、3…），不能为 0、负数或小数。` : dynamic
  - `tools/quantum/infinite-well-energy.html` : `⚠ 粒子质量 m 必须大于 0。` : dynamic
  - `tools/quantum/infinite-well-energy.html` : `⚠ 阱宽 L 必须大于 0。` : dynamic
  - `tools/quantum/pair-production-threshold.html` : `⚠ 靶核质量数 A 须为 ≥0 的整数（0 表示不计反冲）。` : dynamic
  - `tools/quantum/pair-production-threshold.html` : `当前粒子对` : dynamic

### realestate（dead 41 / dynamic 1 / fragment 0 / harmless 0）

- `tools/realestate/analysis-24.html` : `未来价值 = 当前总价 × (1 + 年涨跌幅%)^持有年数` : dead
- `tools/realestate/assessor-23.html` : `成新率 = 1 − 已用年限/经济寿命` : dead
- `tools/realestate/assessor-38.html` : `按揭月供 = 等额本息公式` : dead
- `tools/realestate/assessor-39.html` : `计税评估值 = 计税依据 × 税率` : dead
- `tools/realestate/assessor-40.html` : `保险重置价值 = 重建成本` : dead
- `tools/realestate/assessor-42.html` : `征收补偿 = 区片价 × 面积` : dead
- `tools/realestate/assessor-43.html` : `企业价值 = 资产 − 负债（或收益法）` : dead
- `tools/realestate/assessor-44.html` : `无形资产评估 = 收益/市场/成本法` : dead
- `tools/realestate/assessor-45.html` : `涉税评估值` : dead
- `tools/realestate/assessor-return.html` : `V = NOI / 资本化率 R` : dead
- `tools/realestate/assessor-second-hand.html` : `评估值 = 可比实例价 × 修正系数` : dead
- `tools/realestate/calc-1.html` : `月供 = P·i·(1+i)^n/((1+i)^n−1)` : dead
- `tools/realestate/calc-2.html` : `租金回报率 = 年租金/总价 × 100%` : dead
- `tools/realestate/calc-70.html` : `楼面价 = 土地总价/总建筑面积` : dead
- `tools/realestate/calc-93.html` : `比较法：评估值 = 案例价 × Π修正` : dead
- `tools/realestate/calc-assessor.html` : `拆迁补偿 = 重置价 × 成新率 + 区位` : dead
- `tools/realestate/calc-cost.html` : `资本机会成本 = 替代投资收益` : dead
- `tools/realestate/calc-return.html` : `REITs 收益 = 分红/价格` : dead
- `tools/realestate/chiyou-qijianyunying-feiyong.html` : `持有费用 = 税费+维护+管理` : dead
- `tools/realestate/convert-area-shared.html` : `公摊面积 = 套内面积 × 公摊系数` : dead
- `tools/realestate/convert-area-shared.html` : `建筑面积 = 套内 + 公摊；得房率 = 套内 / 建筑面积 × 100%` : dead
- `tools/realestate/cost-depreciation.html` : `年折旧 = (重置−残值)/使用年限` : dead
- `tools/realestate/cost-depreciation-1.html` : `成本法：价值 = 重置成本 − 折旧 + 地价` : dead
- `tools/realestate/depreciation-2.html` : `房屋折旧 = (1−成新率)×重置成本` : dead
- `tools/realestate/down-payment.html` : `首付 = 总价 × 首付比例` : dead
- `tools/realestate/estimate-37.html` : `空置损失 = 潜在租金 × 空置率` : dead
- `tools/realestate/fangdichan-xintuo-jijinguzhi.html` : `REITs 估值 = 资产净值/份额` : dead
- `tools/realestate/fund-loan.html` : `公积金额度 = f(账户余额, 缴存)` : dead
- `tools/realestate/fund-loan-1.html` : `可贷额度 = 余额×倍数 或 缴存法` : dead
- `tools/realestate/layout-score.html` : `户型评分 = 综合指标加权` : dead
- `tools/realestate/market-valuation.html` : `市场比较法：评估值 = 可比价×修正` : dead
- `tools/realestate/paimai-baoliujia-qipaijia-sheding.html` : `起拍价 = 保留价×折扣` : dead
- `tools/realestate/price-discount-1.html` : `实售价 = 标价×(1−折扣率)` : dead
- `tools/realestate/rater-usable-layout.html` : `得房率 = 套内/建筑面积 × 100%` : dead
- `tools/realestate/rent-1.html` : `潜在毛收入 = 租金×面积×入住率` : dead
- `tools/realestate/return-1.html` : `净收益 = 经营收入 − 运营费用` : dead
- `tools/realestate/return-2.html` : `收益法：V = NOI / 资本化率` : dead
- `tools/realestate/shichang-bijiaofa-anlixiuzheng.html` : `案例修正 = 可比价×因素修正` : dead
- `tools/realestate/tudi-jizhundijia-luxianjia-xishuxiuzheng.html` : `路线价 = 基准价×深度×宽深修正` : dead
- `tools/realestate/xianjinliuyuce.html` : `现金流 = 经营现金流 − 资本支出` : dead
- `tools/realestate/yanglao-dichan-touzi-tuichu-jihui.html` : `投资回报 = 收益/投入` : dead

  其它成因样例（共 1 条，仅列前 5）：
  - `tools/realestate/calc-93.html` : `💡 评估单价 = 案例单价 × 综合修正系数；修正额 = 案例单价 ×（系数 − 1）；系数 < 1 为向下修正。` : dynamic

### rehabilitation（dead 3 / dynamic 3 / fragment 0 / harmless 0）

- `tools/rehabilitation/asia-impairment-scale.html` : `损伤平面以下>半数关键肌肌力<3级` : dead
- `tools/rehabilitation/fim-scale.html` : `自己完成<25%，完全依赖他人` : dead
- `tools/rehabilitation/wheelchair-posture.html` : `核心计算公式（按输入变量）：ischialPressure ÷ 133.322；force ÷ (2 × 5)；hipW + 2` : dead

  其它成因样例（共 3 条，仅列前 5）：
  - `tools/rehabilitation/tester-rater.html` : `1-<10秒` : dynamic
  - `tools/rehabilitation/tester-rater.html` : `1-<3秒` : dynamic
  - `tools/rehabilitation/tester-rater.html` : `4-每侧<3秒` : dynamic

### rental（dead 1 / dynamic 0 / fragment 0 / harmless 0）

- `tools/rental/reminder-4.html` : `绿色=剩余>90天，黄色=30-90天，橙色=7-30天，红色=<7天` : dead

### reproductive-medicine（dead 11 / dynamic 0 / fragment 2 / harmless 0）

- `tools/reproductive-medicine/detector-9.html` : `判定标准：精液量 < 1.5ml 且 retroPct ≥ 50% 且 urTotal > 5×10⁶ → 显著逆行射精` : dead
- `tools/reproductive-medicine/detector-9.html` : `尿液总精子 urTotal = urVol × urConc` : dead
- `tools/reproductive-medicine/detector-9.html` : `精液总精子 ejTotal = ejVol × ejConc` : dead
- `tools/reproductive-medicine/detector-9.html` : `逆行射精诊断要点：精液量极少（常<1ml）+ 射精后尿液中发现大量精子` : dead
- `tools/reproductive-medicine/ivf-statistics.html` : `优质胚胎率 = 优质胚胎数 / 受精数 × 100%` : dead
- `tools/reproductive-medicine/ivf-statistics.html` : `卵裂率 = 卵裂数 / 受精数 × 100%` : dead
- `tools/reproductive-medicine/ivf-statistics.html` : `受精率 = 受精数 / 获卵数 × 100%` : dead
- `tools/reproductive-medicine/ivf-statistics.html` : `正常受精率 = 受精数 / MII卵数 × 100%` : dead
- `tools/reproductive-medicine/ivf-statistics.html` : `着床率 = 孕囊数 / 移植数 × 100%` : dead
- `tools/reproductive-medicine/sperm-morphology.html` : `正常形态(%) = 正常形态数 / 计数总数 × 100` : dead
- `tools/reproductive-medicine/testicular-volume.html` : `体积(mL) = 长 × 宽 × 高 × 0.71 ÷ 1000（单位 mm）` : dead

  其它成因样例（共 2 条，仅列前 5）：
  - `tools/reproductive-medicine/epididymal-aspiration.html` : `获取精子总量(×10⁶) = 浓度(×10⁶/mL) × 体积(mL)` : fragment
  - `tools/reproductive-medicine/sperm-cryopreservation.html` : `复苏率 = 复苏后精子数 / 冻前精子数 ×100` : fragment

### research（dead 16 / dynamic 8 / fragment 5 / harmless 0）

- `tools/research/analysis-49.html` : `KMO 和 Bartlett 分别看什么？` : dead
- `tools/research/analysis-49.html` : `KMO 衡量条目间的共同方差是否足够，越接近 1 越适合做因子分析（常用 0.70 以上为可接受）；Bartlett 检验相关矩阵是否为单位阵，p<0.05 表示条目间存在相关、具备做因子分析的前提。两者都要看，KMO 低而 Bartlett 显著仍不宜直接做因子分析。` : dead
- `tools/research/analysis-49.html` : `α = k ÷ (k − 1) × (1 − Σ 条目方差 ÷ 总分方差)` : dead
- `tools/research/analysis-49.html` : `不会。本页只做可因子性检验与条目诊断，不运行主成分/主轴因子提取，也不输出载荷矩阵。需要因子结构和旋转结果时，请把数据导入统计软件（如 R、SPSS、JASP）继续分析。` : dead
- `tools/research/analysis-49.html` : `仍用上述 6×5 矩阵：相关矩阵行列式 |R| = 0.0001504，KMO = 0.553（按 Kaiser 1974 分档为「较差」）。Bartlett χ² = −[6 − 1 − (2×5+5) ÷ 6] × ln(0.0001504) = 22.006，df = 5×4 ÷ 2 = 10，p = 0.015…(+104字)` : dead
- `tools/research/analysis-49.html` : `准备做探索性因子分析前，先用 KMO 与 Bartlett 检验判断这批数据是否“值得”做因子分析。` : dead
- `tools/research/analysis-49.html` : `同一矩阵中，条目 1~5 的校正后条目-总分相关分别为 0.925、0.748、0.644、0.822、0.958；删除后的 α 分别为 0.8917、0.9268、0.9395、0.9083、0.8792。条目 3 的相关最低、删除后 α 最高（0.9395 > 0.9273），是优先复核的删题候选；条目 5 删除后…(+34字)` : dead
- `tools/research/analysis-49.html` : `同一组数据的 KMO 与 Bartlett` : dead
- `tools/research/analysis-49.html` : `总分方差按全部被试的合计得分计算` : dead
- `tools/research/analysis-49.html` : `把量表数据矩阵录入（每行一名被试、每列一个条目），计算克隆巴赫 α 系数，评估量表内部一致性信度。通常 α 达到 0.70 以上认为可靠，0.60 到 0.70 勉强可用，低于 0.60 需要修订条目。所有数据仅在浏览器本地处理，不上传。` : dead
- `tools/research/analysis-49.html` : `把量表数据矩阵录入（每行一名被试、每列一个条目），计算克隆巴赫 α 系数，评估量表内部一致性信度。通常 α 达到 0.70 以上认为可靠，0.60~0.70 勉强可用，低于 0.60 需修订条目。数据仅在浏览器本地处理，不会上传。` : dead
- `tools/research/analysis-49.html` : `本页会帮我提取因子吗？` : dead
- `tools/research/analysis-49.html` : `条目分析怎么用来删题` : dead
- `tools/research/analysis-49.html` : `量表（信度/效度/因子）分析。免费在线工具，纯前端处理，数据不上传，保护隐私安全。` : dead
- `tools/research/analysis-52.html` : `加权评分 = Σ(提及次数 × 评分) ÷ Σ提及次数` : dead
- `tools/research/analysis-54.html` : `近 5 条均含主题且未出现新主题，主题趋于饱和，可考虑停止抽样。` : dead

  其它成因样例（共 13 条，仅列前 5）：
  - `tools/research/analysis-49.html` : `结构效度（可因子性检验）` : dynamic
  - `tools/research/analysis-49.html` : `KMO 取样适切性：` : dynamic
  - `tools/research/analysis-49.html` : `Bartlett 球形检验：χ²=` : dynamic
  - `tools/research/analysis-49.html` : `条目分析（校正后条目-总分相关 / 删除该条目后的 α）` : dynamic
  - `tools/research/analysis-49.html` : `条目` : fragment

### restaurant（dead 9 / dynamic 0 / fragment 0 / harmless 4）

- `tools/restaurant/bbq-portion.html` : `关于「烧烤食材分量计算器」` : dead
- `tools/restaurant/bbq-portion.html` : `如何使用烧烤食材分量计算器？` : dead
- `tools/restaurant/bbq-portion.html` : `烧烤食材分量计算器是做什么的？` : dead
- `tools/restaurant/bbq-portion.html` : `烧烤食材分量计算器适合哪些场景？` : dead
- `tools/restaurant/hotpot-portion.html` : `关于「火锅食材分量计算器」` : dead
- `tools/restaurant/hotpot-portion.html` : `如何使用火锅食材分量计算器？` : dead
- `tools/restaurant/hotpot-portion.html` : `火锅食材分量计算器是做什么的？` : dead
- `tools/restaurant/hotpot-portion.html` : `火锅食材分量计算器适合哪些场景？` : dead
- `tools/restaurant/index.html` : `餐饮经营工具集合收录了 8 个免费在线工具，覆盖餐饮经营场景下的常见计算、换算与查询需求。无论你是相关领域的从业者、学生还是普通用户，都能在这里找到即用即走的实用小工具。所有工具纯前端运行，数据不上传服务器，保护隐私安全。` : dead

  其它成因样例（共 4 条，仅列前 5）：
  - `tools/restaurant/bbq-portion.html` : `📖 查看「烧烤食材分量计算器使用指南」` : harmless
  - `tools/restaurant/bbq-portion.html` : `📚 深度解析：烧烤食材分量计算器` : harmless
  - `tools/restaurant/hotpot-portion.html` : `📖 查看「火锅食材分量计算器使用指南」` : harmless
  - `tools/restaurant/hotpot-portion.html` : `📚 深度解析：火锅食材分量计算器` : harmless

### rheumatology（dead 9 / dynamic 1 / fragment 0 / harmless 0）

- `tools/rheumatology/basdai.html` : `CRP = 0.12×腰背痛 + 0.06×晨僵持续时间 + 0.07×患者总体 + 0.11×CRP(√)` : dead
- `tools/rheumatology/basdai.html` : `提示：BASDAI≥4是ASAS/EULAR推荐启动抗TNF生物制剂治疗的主要标准之一。BASDAI主观性较强，建议结合ASDAS(含CRP/ESR的客观指标)综合评估。ASDAS-CRP = 0.12×腰背痛 + 0.06×晨僵持续时间 + 0.07×患者总体 + 0.11×CRP(√)。仅供临床参考。` : dead
- `tools/rheumatology/essdai.html` : `高 — 肾小球肾炎/eGFR<30` : dead
- `tools/rheumatology/gout-uric-acid.html` : `提示：急性发作期不启动ULT，已用药者不停药。ULT启动初期(3-6月)需联合秋水仙碱(0.5mg 1-2次/日)预防发作。血尿酸不可降得过低(<180μmol/L)，可能与神经退行性疾病相关。每2-4周监测尿酸，达标后每6月复查。仅供临床参考。` : dead
- `tools/rheumatology/igg4-level.html` : `嗜酸性粒细胞 (×10⁹/L, 正常 <0.5)` : dead
- `tools/rheumatology/igg4-level.html` : `总IgE (IU/mL, 正常 <100)` : dead
- `tools/rheumatology/igg4-level.html` : `：IgG4+/IgG+比值>40%且>10个/HPF(+10分)；比值>40%但<10/HPF(+5分)` : dead
- `tools/rheumatology/lupus-anticoagulant.html` : `妊娠并发症：①≥10周不明原因死胎；②≥34周因子痫前期/胎盘功能不全早产；③连续3次<10周不明原因自然流产` : dead
- `tools/rheumatology/womac.html` : `标准化总分 = (原始分/96)×100` : dead

  其它成因样例（共 1 条，仅列前 5）：
  - `tools/rheumatology/gout-uric-acid.html` : `5期 (GFR <15/透析)` : dynamic

### robotics（dead 15 / dynamic 6 / fragment 4 / harmless 0）

- `tools/robotics/battery-runtime.html` : `t = 容量(Wh) / 功耗(W)` : dead
- `tools/robotics/cable-tension-pulley.html` : `单侧绳张力 T = mg/2` : dead
- `tools/robotics/encoder-angle-resolution.html` : `四倍频后分辨率 = 360°/(4·CPR)。` : dead
- `tools/robotics/encoder-angle-resolution.html` : `输入每转脉冲数 CPR（四倍频后），求最小角度分辨率。` : dead
- `tools/robotics/encoder-angle-resolution.html` : `输入编码器每转单相脉冲数 PPR，工具按 θ_min=360°/(4·PPR)（正交四倍频）计算最小可分辨角度，说明高 PPR 提升定位精度，用于选型与运动控制分辨率评估。` : dead
- `tools/robotics/forward-kinematics-2r.html` : `θ₁=30°、θ₂=45°、L=1 → 约 (1.297, 1.207)。` : dead
- `tools/robotics/gravity-comp-torque.html` : `5kg、臂长 0.3m、水平` : dead
- `tools/robotics/gravity-comp-torque.html` : `τ = m·g·L·cosθ（水平时最大）。` : dead
- `tools/robotics/gravity-comp-torque.html` : `τ=m·g·L·cosθ=5×9.81×0.3×1=14.7 N·m（θ=0 水平最大）。` : dead
- `tools/robotics/gravity-comp-torque.html` : `水平臂重力平衡。` : dead
- `tools/robotics/gravity-comp-torque.html` : `臂与水平夹角；水平 θ=0 时重力矩最大。` : dead
- `tools/robotics/gravity-comp-torque.html` : `角度 θ (°)` : dead
- `tools/robotics/servo-pwm-angle.html` : `角度 = (脉宽−最小)/(最大−最小)×180°` : dead
- `tools/robotics/stepper-step-angle.html` : `步距角 = 360°/(步数/圈)` : dead
- `tools/robotics/wheel-odometry.html` : `ds=(1.0+1.2)/2=1.1m，dθ=(1.2−1.0)/0.4=0.5rad；前进 1.1m 并右转 0.5rad。` : dead

  其它成因样例（共 10 条，仅列前 5）：
  - `tools/robotics/encoder-angle-resolution.html` : `每转脉冲 PPR` : fragment
  - `tools/robotics/encoder-angle-resolution.html` : `⚠ 每转脉冲 PPR 必须为正整数（≥1），不能为 0、负数或小数。` : dynamic
  - `tools/robotics/inverse-kinematics-2r.html` : `θ₁ 肘下 (°)` : dynamic
  - `tools/robotics/inverse-kinematics-2r.html` : `θ₂ (°)` : dynamic
  - `tools/robotics/inverse-kinematics-2r.html` : `θ₂ 肘上 (°)` : dynamic

### sales（dead 2 / dynamic 0 / fragment 1 / harmless 0）

- `tools/sales/moving-average.html` : `SMA(3)：第3期 (100+120+110)/3 = 110；第4期 (120+110+130)/3 = 120；第5期 (110+130+140)/3 = 126.67。 ⏎ 下一期预测 = 最近窗口均值 = (110+130+140)/3 = 126.67。 ⏎ WMA(3) 权重 1/2/3，第5期 = (1…(+92字)` : dead
- `tools/sales/moving-average.html` : `核心计算公式（按输入变量）：2÷(n+1)；n×(n+1)÷2；n-1` : dead

  其它成因样例（共 1 条，仅列前 5）：
  - `tools/sales/target-breakdown.html` : `个人目标 = 总目标 × (个人权重 ÷ 权重总和)` : fragment

### science（dead 175 / dynamic 349 / fragment 33 / harmless 8）

- `tools/science/astronomy-toolkit.html` : `天文观测 = 坐标/历算/视差` : dead
- `tools/science/calc-1.html` : `h = v₀t + ½gt²　落地速度 v = v₀ + gt` : dead
- `tools/science/calc-2.html` : `理想气体 PV = nRT` : dead
- `tools/science/calc-cycle.html` : `分子量 = Σ(原子量×个数)` : dead
- `tools/science/calc-distance.html` : `地理距离 = Haversine 公式` : dead
- `tools/science/correlation-calculator.html` : `Pearson 相关系数 r ∈ [−1, 1]：衡量两个变量的线性相关程度与方向，并给 R² = r²（解释方差比例）；n<3 或任一方差为 0 时无法定义。` : dead
- `tools/science/cycle.html` : `氖 (Neon)` : dead
- `tools/science/cycle.html` : `氙 (Xenon)` : dead
- `tools/science/cycle.html` : `氟 (Fluorine)` : dead
- `tools/science/cycle.html` : `氡 (Radon)` : dead
- `tools/science/cycle.html` : `氢 (Hydrogen)` : dead
- `tools/science/cycle.html` : `氦 (Helium)` : dead
- `tools/science/cycle.html` : `氧 (Oxygen)` : dead
- `tools/science/cycle.html` : `氩 (Argon)` : dead
- `tools/science/cycle.html` : `氪 (Krypton)` : dead
- `tools/science/cycle.html` : `氮 (Nitrogen)` : dead
- `tools/science/cycle.html` : `氯 (Chlorine)` : dead
- `tools/science/cycle.html` : `汞 (Mercury)` : dead
- `tools/science/cycle.html` : `溴 (Bromine)` : dead
- `tools/science/cycle.html` : `砷 (Arsenic)` : dead
- `tools/science/cycle.html` : `砹 (Astatine)` : dead
- `tools/science/cycle.html` : `硅 (Silicon)` : dead
- `tools/science/cycle.html` : `硒 (Selenium)` : dead
- `tools/science/cycle.html` : `硫 (Sulfur)` : dead
- `tools/science/cycle.html` : `硼 (Boron)` : dead
- `tools/science/cycle.html` : `碘 (Iodine)` : dead
- `tools/science/cycle.html` : `碲 (Tellurium)` : dead
- `tools/science/cycle.html` : `碳 (Carbon)` : dead
- `tools/science/cycle.html` : `磷 (Phosphorus)` : dead
- `tools/science/cycle.html` : `金 (Gold)` : dead
- `tools/science/cycle.html` : `鉨 (Nihonium)` : dead
- `tools/science/cycle.html` : `鎶 (Copernicium)` : dead
- `tools/science/cycle.html` : `钆 (Gadolinium)` : dead
- `tools/science/cycle.html` : `钇 (Yttrium)` : dead
- `tools/science/cycle.html` : `钋 (Polonium)` : dead
- `tools/science/cycle.html` : `钌 (Ruthenium)` : dead
- `tools/science/cycle.html` : `钍 (Thorium)` : dead
- `tools/science/cycle.html` : `钐 (Samarium)` : dead
- `tools/science/cycle.html` : `钒 (Vanadium)` : dead
- `tools/science/cycle.html` : `钔 (Mendelevium)` : dead
- `tools/science/cycle.html` : `钕 (Neodymium)` : dead
- `tools/science/cycle.html` : `钙 (Calcium)` : dead
- `tools/science/cycle.html` : `钚 (Plutonium)` : dead
- `tools/science/cycle.html` : `钛 (Titanium)` : dead
- `tools/science/cycle.html` : `钠 (Sodium)` : dead
- `tools/science/cycle.html` : `钡 (Barium)` : dead
- `tools/science/cycle.html` : `钨 (Tungsten)` : dead
- `tools/science/cycle.html` : `钪 (Scandium)` : dead
- `tools/science/cycle.html` : `钫 (Francium)` : dead
- `tools/science/cycle.html` : `钬 (Holmium)` : dead
- `tools/science/cycle.html` : `钯 (Palladium)` : dead
- `tools/science/cycle.html` : `钴 (Cobalt)` : dead
- `tools/science/cycle.html` : `钷 (Promethium)` : dead
- `tools/science/cycle.html` : `钼 (Molybdenum)` : dead
- `tools/science/cycle.html` : `钽 (Tantalum)` : dead
- `tools/science/cycle.html` : `钾 (Potassium)` : dead
- `tools/science/cycle.html` : `铀 (Uranium)` : dead
- `tools/science/cycle.html` : `铁 (Iron)` : dead
- `tools/science/cycle.html` : `铂 (Platinum)` : dead
- `tools/science/cycle.html` : `铅 (Lead)` : dead
- `tools/science/cycle.html` : `铈 (Cerium)` : dead
- `tools/science/cycle.html` : `铊 (Thallium)` : dead
- `tools/science/cycle.html` : `铋 (Bismuth)` : dead
- `tools/science/cycle.html` : `铌 (Niobium)` : dead
- `tools/science/cycle.html` : `铍 (Beryllium)` : dead
- `tools/science/cycle.html` : `铑 (Rhodium)` : dead
- `tools/science/cycle.html` : `铒 (Erbium)` : dead
- `tools/science/cycle.html` : `铕 (Europium)` : dead
- `tools/science/cycle.html` : `铜 (Copper)` : dead
- `tools/science/cycle.html` : `铝 (Aluminium)` : dead
- `tools/science/cycle.html` : `铟 (Indium)` : dead
- `tools/science/cycle.html` : `铥 (Thulium)` : dead
- `tools/science/cycle.html` : `铪 (Hafnium)` : dead
- `tools/science/cycle.html` : `铬 (Chromium)` : dead
- `tools/science/cycle.html` : `铯 (Cesium)` : dead
- `tools/science/cycle.html` : `铱 (Iridium)` : dead
- `tools/science/cycle.html` : `银 (Silver)` : dead
- `tools/science/cycle.html` : `铷 (Rubidium)` : dead
- `tools/science/cycle.html` : `铹 (Lawrencium)` : dead
- `tools/science/cycle.html` : `铼 (Rhenium)` : dead
- `tools/science/cycle.html` : `铽 (Terbium)` : dead
- `tools/science/cycle.html` : `锂 (Lithium)` : dead
- `tools/science/cycle.html` : `锆 (Zirconium)` : dead
- `tools/science/cycle.html` : `锇 (Osmium)` : dead
- `tools/science/cycle.html` : `锌 (Zinc)` : dead
- `tools/science/cycle.html` : `锎 (Californium)` : dead
- `tools/science/cycle.html` : `锑 (Antimony)` : dead
- `tools/science/cycle.html` : `锔 (Curium)` : dead
- `tools/science/cycle.html` : `锕 (Actinium)` : dead
- `tools/science/cycle.html` : `锗 (Germanium)` : dead
- `tools/science/cycle.html` : `锘 (Nobelium)` : dead
- `tools/science/cycle.html` : `锝 (Technetium)` : dead
- `tools/science/cycle.html` : `锡 (Tin)` : dead
- `tools/science/cycle.html` : `锫 (Berkelium)` : dead
- `tools/science/cycle.html` : `锰 (Manganese)` : dead
- `tools/science/cycle.html` : `锶 (Strontium)` : dead
- `tools/science/cycle.html` : `锿 (Einsteinium)` : dead
- `tools/science/cycle.html` : `镁 (Magnesium)` : dead
- `tools/science/cycle.html` : `镄 (Fermium)` : dead
- `tools/science/cycle.html` : `镅 (Americium)` : dead
- `tools/science/cycle.html` : `镆 (Moscovium)` : dead
- `tools/science/cycle.html` : `镉 (Cadmium)` : dead
- `tools/science/cycle.html` : `镍 (Nickel)` : dead
- `tools/science/cycle.html` : `镎 (Neptunium)` : dead
- `tools/science/cycle.html` : `镓 (Gallium)` : dead
- `tools/science/cycle.html` : `镝 (Dysprosium)` : dead
- `tools/science/cycle.html` : `镤 (Protactinium)` : dead
- `tools/science/cycle.html` : `镥 (Lutetium)` : dead
- `tools/science/cycle.html` : `镧 (Lanthanum)` : dead
- `tools/science/cycle.html` : `镨 (Praseodymium)` : dead
- `tools/science/cycle.html` : `镭 (Radium)` : dead
- `tools/science/cycle.html` : `镱 (Ytterbium)` : dead
- `tools/science/cycle.html` : `鿔 (Meitnerium)` : dead
- `tools/science/cycle.html` : `鿫 (Oganesson)` : dead
- `tools/science/cycle.html` : `鿬 (Tennessine)` : dead
- `tools/science/equation-balancer.html` : `H (氢)` : dead
- `tools/science/equation-balancer.html` : `O (氧)` : dead
- `tools/science/equation-balancer.html` : `Σ vᵢ·E(反应物) = Σ vᵢ·E(生成物)，每种元素守恒` : dead
- `tools/science/fibonacci.html` : `F(1) 到 F(20)` : dead
- `tools/science/geo-distance-calculator.html` : `(东南偏南 (SSE))` : dead
- `tools/science/gravitational-potential.html` : `E=mgh 求重力势能 - ToolBox` : dead
- `tools/science/logic-gate-simulator.html` : `AND（与门）：两输入全1输出1` : dead
- `tools/science/meteor-crater-estimator.html` : `102.30 km（有感震动、轻微损坏）` : dead
- `tools/science/meteor-crater-estimator.html` : `45.01 km（玻璃破碎、轻质建筑损坏）` : dead
- `tools/science/meteor-crater-estimator.html` : `TNT当量 (百万吨 (Mt))` : dead
- `tools/science/meteor-crater-estimator.html` : `沉积岩 (2700 kg/m³)` : dead
- `tools/science/molar-mass-calculator.html` : `括号内原子数乘括号外系数。` : dead
- `tools/science/molar-mass-calculator.html` : `括号怎么算？` : dead
- `tools/science/molar-mass-calculator.html` : `摩尔质量 = Σ(原子量×个数)` : dead
- `tools/science/nth-root-calculator.html` : `计算 ⁿ√x = x^(1/n)` : dead
- `tools/science/pendulum-period.html` : `适用条件：小角度（θ<5°~10°）；与摆球质量无关。` : dead
- `tools/science/ph-calculator.html` : `pH = pKa + log([盐]/[酸]) = pKa + log(cb/ca)` : dead
- `tools/science/polar-day-night.html` : `0（极夜）（1月1日，太阳赤纬 -23.0°）` : dead
- `tools/science/polar-day-night.html` : `24.0 小时（5月21日，太阳赤纬 20.1°）` : dead
- `tools/science/polar-day-night.html` : `太阳全天不升，持续 64 天` : dead
- `tools/science/polar-day-night.html` : `太阳全天不落，持续 64 天` : dead
- `tools/science/polar-day-night.html` : `当 δ < 0 时（冬至附近），北极夜南极昼` : dead
- `tools/science/polar-day-night.html` : `极昼极夜 = f(纬度, 节气)` : dead
- `tools/science/polar-day-night.html` : `白夜＝午夜太阳高度 > −6°（民用曙暮光，整夜不黑）；极昼期间同时计入白夜天数。` : dead
- `tools/science/prime-number.html` : `n 为素数 ⇔ n>1 且不存在 p ∈ [2, √n] 使 p | n` : dead
- `tools/science/quadratic-equation.html` : `二次方程求根公式，判别式 Δ = b²−4ac：Δ>0 两实根、Δ=0 重根、Δ<0 一对共轭复根；a=0 时退化为一次方程。` : dead
- `tools/science/range-calculator.html` : `Range = 最大值 − 最小值` : dead
- `tools/science/rc-time-constant.html` : `t(到 α%) = −τ×ln(1−α)（充电）　·　10%→90% 上升时间 ≈ 2.2τ` : dead
- `tools/science/resistor-color-code.html` : `<span class="color-chip" style="background:#000000"></span>黑` : dead
- `tools/science/resistor-color-code.html` : `<span class="color-chip" style="background:#1E88E5"></span>蓝` : dead
- `tools/science/resistor-color-code.html` : `<span class="color-chip" style="background:#43A047"></span>绿` : dead
- `tools/science/resistor-color-code.html` : `<span class="color-chip" style="background:#8B4513"></span>棕` : dead
- `tools/science/resistor-color-code.html` : `<span class="color-chip" style="background:#8E24AA"></span>紫` : dead
- `tools/science/resistor-color-code.html` : `<span class="color-chip" style="background:#9E9E9E"></span>灰` : dead
- `tools/science/resistor-color-code.html` : `<span class="color-chip" style="background:#C0C0C0"></span>银` : dead
- `tools/science/resistor-color-code.html` : `<span class="color-chip" style="background:#E53935"></span>红` : dead
- `tools/science/resistor-color-code.html` : `<span class="color-chip" style="background:#FAFAFA"></span>白` : dead
- `tools/science/resistor-color-code.html` : `<span class="color-chip" style="background:#FB8C00"></span>橙` : dead
- `tools/science/resistor-color-code.html` : `<span class="color-chip" style="background:#FDD835"></span>黄` : dead
- `tools/science/resistor-color-code.html` : `<span class="color-chip" style="background:#FFD700"></span>金` : dead
- `tools/science/science-pressure-converter.html` : `MPa · 兆帕` : dead
- `tools/science/science-pressure-converter.html` : `PSI · 磅/平方英寸` : dead
- `tools/science/science-pressure-converter.html` : `Pa · 帕斯卡` : dead
- `tools/science/science-pressure-converter.html` : `Torr · 托` : dead
- `tools/science/science-pressure-converter.html` : `atm · 标准大气压` : dead
- `tools/science/science-pressure-converter.html` : `bar · 巴` : dead
- `tools/science/science-pressure-converter.html` : `inHg · 英寸汞柱` : dead
- `tools/science/science-pressure-converter.html` : `kPa · 千帕` : dead
- `tools/science/science-pressure-converter.html` : `kgf/cm² · 千克力/厘米²` : dead
- `tools/science/science-pressure-converter.html` : `mbar · 毫巴` : dead
- `tools/science/science-pressure-converter.html` : `mmHg · 毫米汞柱` : dead
- `tools/science/science-pressure-converter.html` : `mmH₂O · 毫米水柱` : dead
- `tools/science/si-unit-converter.html` : `⏱️ 时间` : dead
- `tools/science/significant-figures.html` : `结果位数 ≤ 参与运算中有效数字最少者（乘除）/ 小数位最少者（加减）` : dead
- `tools/science/star-magnitude-compare.html` : `星等1 (-1.46) 的天体更亮，亮度是星等2的 3.84 倍` : dead
- `tools/science/star-magnitude-compare.html` : `星等1 (天狼星)` : dead
- `tools/science/star-magnitude-compare.html` : `星等1 对应恒星：天狼星` : dead
- `tools/science/tide-height-estimator.html` : `当前月相（月龄 19.0 天）` : dead
- `tools/science/tide-height-estimator.html` : `潮汐高度 = 天文+气象分潮` : dead
- `tools/science/trigonometry-calculator.html` : `sinθ = 对边/斜边　cosθ = 邻边/斜边　tanθ = 对边/邻边` : dead

  其它成因样例（共 390 条，仅列前 5）：
  - `tools/science/astronomy-toolkit.html` : `10.9天` : dynamic
  - `tools/science/astronomy-toolkit.html` : `亏凸月` : fragment
  - `tools/science/battery-life-calculator.html` : `0 秒` : dynamic
  - `tools/science/battery-life-calculator.html` : `12小时 45分钟` : dynamic
  - `tools/science/battery-life-calculator.html` : `19小时 8分钟` : dynamic

### securities（dead 13 / dynamic 0 / fragment 1 / harmless 0）

- `tools/securities/capm-beta.html` : `β = 协方差 / 市场方差。 样本需等长。` : dead
- `tools/securities/current-yield.html` : `CY = 年息/现价` : dead
- `tools/securities/ddm-price.html` : `P = D₁ / (r − g)。 仅适用于 r > g 且增长稳定的股票。` : dead
- `tools/securities/earnings-yield.html` : `盈利收益率 = EPS/P × 100%` : dead
- `tools/securities/fcf-yield.html` : `FCF收益率 = FCF/股价 × 100%` : dead
- `tools/securities/margin-requirement.html` : `保证金比例 = 权益/持仓市值 × 100%` : dead
- `tools/securities/market-cap.html` : `市值 = 股价×总股本` : dead
- `tools/securities/max-drawdown.html` : `MDD = (峰值−谷值)/峰值 × 100%` : dead
- `tools/securities/option-breakeven-call.html` : `看涨盈亏平衡 = K + 权利金` : dead
- `tools/securities/option-breakeven-put.html` : `看跌盈亏平衡 = K − P` : dead
- `tools/securities/peg-ratio.html` : `PEG<1 常被视为低估。` : dead
- `tools/securities/price-to-book.html` : `P/B = 股价/每股账面价值` : dead
- `tools/securities/price-to-book.html` : `P/B<1 可能被低估（需结合资产质量）。` : dead

  其它成因样例（共 1 条，仅列前 5）：
  - `tools/securities/market-cap.html` : `市值` : fragment

### security（dead 4 / dynamic 0 / fragment 0 / harmless 0）

- `tools/security/index.html` : `网络安全工具集合收录了 12 个免费在线工具，覆盖网络安全场景下的常见计算、换算与查询需求。无论你是相关领域的从业者、学生还是普通用户，都能在这里找到即用即走的实用小工具。所有工具纯前端运行，数据不上传服务器，保护隐私安全。` : dead
- `tools/security/index.html` : `自定义长度、字符集与排除规则生成高强度密码，支持口令短语模式，纯前端生成不存储，适合账号安全与密钥管理。` : dead
- `tools/security/index.html` : `金融级密码在线生成器，可设长度、字符集与排除易混淆字符，生成高强度随机密码，数据本地生成不上传，纯前端。` : dead
- `tools/security/passphrase-generator.html` : `熵 ≈ n · log₂(W)（bit）` : dead

### seismology（dead 1 / dynamic 5 / fragment 0 / harmless 0）

- `tools/seismology/assessor-31.html` : `等级：≥0.7 毁灭性｜≥0.5 特大｜≥0.3 严重｜≥0.1 中等｜<0.1 轻微` : dead

  其它成因样例（共 5 条，仅列前 5）：
  - `tools/seismology/assessor-31.html` : `综合指数 ≥0.7 毁灭性、≥0.5 特大、≥0.3 严重、≥0.1 中等、其余为轻微；对应启动 I 级（毁灭性/特大）或 II~IV 级应急响应。阈值按固定五级划分，工具内不支持自定义；地方标准不同时以当地预案为准。` : dynamic
  - `tools/seismology/assessor-31.html` : `请输入大于 0 的建筑总数（栋）` : dynamic
  - `tools/seismology/assessor-31.html` : `各项破坏数量不得为负数` : dynamic
  - `tools/seismology/assessor-31.html` : `需安置人口比例(粗估)` : dynamic
  - `tools/seismology/assessor-31.html` : `按倒塌率×5 + 严重破坏占比×2 粗略估算，仅供参考` : dynamic

### shipping（dead 1 / dynamic 1 / fragment 0 / harmless 0）

- `tools/shipping/convert-time-speed.html` : `航程 = 航速 × 航行时间` : dead

  其它成因样例（共 1 条，仅列前 5）：
  - `tools/shipping/convert-speed-1.html` : `请输入有效的数值。` : dynamic

### signal（dead 3 / dynamic 0 / fragment 1 / harmless 0）

- `tools/signal/damping-ratio.html` : `ζ = c/(2√(km))；ζ1 过阻尼。 示例 ζ=0.1（欠阻尼振荡）。` : dead
- `tools/signal/damping-ratio.html` : `ζ = c/(2√(km))；ζ<1 振荡，ζ=1 临界，ζ>1 过阻尼。` : dead
- `tools/signal/peak-time-2nd.html` : `峰值时间（t_p = π / (ω_n√(1−ζ²))）` : dead

  其它成因样例（共 1 条，仅列前 5）：
  - `tools/signal/cascade-gain-db.html` : `20=27 dB → 线性≈501。` : fragment

### sports（dead 267 / dynamic 16 / fragment 18 / harmless 2）

- `tools/sports/altitude-acclimatization.html` : `如何使用登山海拔适应时间表？` : dead
- `tools/sports/altitude-acclimatization.html` : `登山海拔适应时间表是做什么的？` : dead
- `tools/sports/altitude-acclimatization.html` : `登山海拔适应时间表适合哪些场景？` : dead
- `tools/sports/analysis-19.html` : `如何使用战术（攻防）视频分析？` : dead
- `tools/sports/analysis-19.html` : `战术（攻防）视频分析是做什么的？` : dead
- `tools/sports/analysis-19.html` : `战术（攻防）视频分析适合哪些场景？` : dead
- `tools/sports/analysis-spacing.html` : `如何使用攀岩挂片间距与受力分析？` : dead
- `tools/sports/analysis-spacing.html` : `攀岩挂片间距与受力分析是做什么的？` : dead
- `tools/sports/analysis-spacing.html` : `攀岩挂片间距与受力分析适合哪些场景？` : dead
- `tools/sports/assessor-csat.html` : `CSAT = 满意人数 ÷ (满意 + 一般 + 不满意) × 100%` : dead
- `tools/sports/assessor-csat.html` : `NPS = 推荐者占比 − 贬损者占比` : dead
- `tools/sports/assessor-csat.html` : `到场率 = 实际到场人数 ÷ 总参与人数 × 100%` : dead
- `tools/sports/assessor-csat.html` : `如何使用评估（满意度/效果/报告）方法？` : dead
- `tools/sports/assessor-csat.html` : `成绩（统计/公布/证书）系统` : dead
- `tools/sports/assessor-csat.html` : `评估（满意度/效果/报告）方法是做什么的？` : dead
- `tools/sports/assessor-csat.html` : `评估（满意度/效果/报告）方法适合哪些场景？` : dead
- `tools/sports/assessor-hardness.html` : `踢腿高度与柔韧度转换关系` : dead
- `tools/sports/assessor-risk-2.html` : `如何使用运动损伤风险评估（问卷）？` : dead
- `tools/sports/assessor-risk-2.html` : `运动损伤风险评估（问卷）是做什么的？` : dead
- `tools/sports/assessor-risk-2.html` : `运动损伤风险评估（问卷）适合哪些场景？` : dead
- `tools/sports/calc-61.html` : `关于「能量消耗便携计算」` : dead
- `tools/sports/calc-61.html` : `如何使用能量消耗便携计算？` : dead
- `tools/sports/calc-61.html` : `能量消耗 = MET × 体重 × 时间` : dead
- `tools/sports/calc-61.html` : `能量消耗便携计算是做什么的？` : dead
- `tools/sports/calc-61.html` : `能量消耗便携计算适合哪些场景？` : dead
- `tools/sports/calc-62.html` : `关于「棒球打击率/自责分计算」` : dead
- `tools/sports/calc-62.html` : `如何使用棒球打击率/自责分计算？` : dead
- `tools/sports/calc-62.html` : `打击率 = 安打/打数；ERA = 自责分×9/局` : dead
- `tools/sports/calc-62.html` : `棒球打击率/自责分计算是做什么的？` : dead
- `tools/sports/calc-62.html` : `棒球打击率/自责分计算适合哪些场景？` : dead
- `tools/sports/calc-angle-slope.html` : `关于「滑雪坡度角度计算（百分比度）」` : dead
- `tools/sports/calc-angle-slope.html` : `如何使用滑雪坡度角度计算（百分比度）？` : dead
- `tools/sports/calc-angle-slope.html` : `滑雪坡度角度计算（百分比度）是做什么的？` : dead
- `tools/sports/calc-angle-slope.html` : `滑雪坡度角度计算（百分比度）适合哪些场景？` : dead
- `tools/sports/calc-angle-slope.html` : `百分比坡度 = tanθ × 100%` : dead
- `tools/sports/calc-heart-rate-1.html` : `关于「心率储备计算（HRR）」` : dead
- `tools/sports/calc-heart-rate-1.html` : `如何使用心率储备计算（HRR）？` : dead
- `tools/sports/calc-heart-rate-1.html` : `心率储备计算（HRR）是做什么的？` : dead
- `tools/sports/calc-heart-rate-1.html` : `心率储备计算（HRR）适合哪些场景？` : dead
- `tools/sports/calc-length-cutting.html` : `关于「肌肉效贴布裁剪长度计算」` : dead
- `tools/sports/calc-length-cutting.html` : `如何使用肌肉效贴布裁剪长度计算？` : dead
- `tools/sports/calc-length-cutting.html` : `肌效贴裁剪长度 = 按需分摊` : dead
- `tools/sports/calc-length-cutting.html` : `肌肉效贴布裁剪长度计算是做什么的？` : dead
- `tools/sports/calc-length-cutting.html` : `肌肉效贴布裁剪长度计算适合哪些场景？` : dead
- `tools/sports/calc-time.html` : `NDL 免减压时间 = f(深度, 潜水时长)` : dead
- `tools/sports/calc-time.html` : `关于「潜水免减压时间计算」` : dead
- `tools/sports/calc-time.html` : `如何使用潜水免减压时间计算？` : dead
- `tools/sports/calc-time.html` : `潜水免减压时间计算是做什么的？` : dead
- `tools/sports/calc-time.html` : `潜水免减压时间计算适合哪些场景？` : dead
- `tools/sports/calculator-calc-9.html` : `关于「骑行齿比计算器」` : dead
- `tools/sports/calculator-calc-9.html` : `如何使用骑行齿比计算器？` : dead
- `tools/sports/calculator-calc-9.html` : `骑行齿比计算器是做什么的？` : dead
- `tools/sports/calculator-calc-9.html` : `骑行齿比计算器适合哪些场景？` : dead
- `tools/sports/calculator-calc-9.html` : `齿比 = 牙盘齿数 / 飞轮齿数` : dead
- `tools/sports/calculator-calc-time.html` : `关于「马拉松配速计算器」` : dead
- `tools/sports/calculator-calc-time.html` : `如何使用马拉松配速计算器？` : dead
- `tools/sports/calculator-calc-time.html` : `配速 = 时间 / 距离` : dead
- `tools/sports/calculator-calc-time.html` : `马拉松配速计算器是做什么的？` : dead
- `tools/sports/calculator-calc-time.html` : `马拉松配速计算器适合哪些场景？` : dead
- `tools/sports/climbing-grade-converter.html` : `如何使用攀岩难度等级转换？` : dead
- `tools/sports/climbing-grade-converter.html` : `攀岩难度等级转换是做什么的？` : dead
- `tools/sports/climbing-grade-converter.html` : `攀岩难度等级转换适合哪些场景？` : dead
- `tools/sports/climbing-grade-converter.html` : `攀岩难度等级转换，支持 V级抱石、YDS、法式、英式等主流系统` : dead
- `tools/sports/convert-29.html` : `抗击打部位硬度（指测）评估` : dead
- `tools/sports/convert-29.html` : `柔韧指数 = 踢腿高度 / 身高 × 100%` : dead
- `tools/sports/convert-47.html` : `力量（1RM/最大力量）换算是做什么的？` : dead
- `tools/sports/convert-47.html` : `力量（1RM/最大力量）换算适合哪些场景？` : dead
- `tools/sports/convert-47.html` : `如何使用力量（1RM/最大力量）换算？` : dead
- `tools/sports/convert-time.html` : `如何使用铁人三项转换时间（游泳/骑车/跑步）？` : dead
- `tools/sports/convert-time.html` : `铁人三项转换时间（游泳/骑车/跑步）是做什么的？` : dead
- `tools/sports/convert-time.html` : `铁人三项转换时间（游泳/骑车/跑步）适合哪些场景？` : dead
- `tools/sports/detector-14.html` : `如何使用无氧阈（拐点）检测？` : dead
- `tools/sports/detector-14.html` : `无氧阈 = 乳酸拐点对应强度` : dead
- `tools/sports/detector-14.html` : `无氧阈（拐点）检测是做什么的？` : dead
- `tools/sports/detector-14.html` : `无氧阈（拐点）检测适合哪些场景？` : dead
- `tools/sports/dianjiezhi-diushi-buchong.html` : `如何使用电解质（丢失）补充？` : dead
- `tools/sports/dianjiezhi-diushi-buchong.html` : `电解质（丢失）补充是做什么的？` : dead
- `tools/sports/dianjiezhi-diushi-buchong.html` : `电解质（丢失）补充适合哪些场景？` : dead
- `tools/sports/estimate-22.html` : `如何使用运动补水策略估算？` : dead
- `tools/sports/estimate-22.html` : `运动补水 = 体重损失 × 系数` : dead
- `tools/sports/estimate-22.html` : `运动补水策略估算是做什么的？` : dead
- `tools/sports/estimate-22.html` : `运动补水策略估算适合哪些场景？` : dead
- `tools/sports/estimate-35.html` : `关于「出汗率估算」` : dead
- `tools/sports/estimate-35.html` : `出汗率 = (运动前−后体重)/时间` : dead
- `tools/sports/estimate-35.html` : `出汗率估算是做什么的？` : dead
- `tools/sports/estimate-35.html` : `出汗率估算适合哪些场景？` : dead
- `tools/sports/estimate-35.html` : `如何使用出汗率估算？` : dead
- `tools/sports/estimate-tester.html` : `VO2max = 15.3×距离(英里)/时间 + 3.5` : dead
- `tools/sports/estimate-tester.html` : `如何使用最大摄氧量（VO2max）估算（跑步测试）？` : dead
- `tools/sports/estimate-tester.html` : `最大摄氧量（VO2max）估算（跑步测试）是做什么的？` : dead
- `tools/sports/estimate-tester.html` : `最大摄氧量（VO2max）估算（跑步测试）适合哪些场景？` : dead
- `tools/sports/generator-random-3.html` : `如何使用瑜伽体式随机生成（内置常见体式）？` : dead
- `tools/sports/generator-random-3.html` : `瑜伽体式随机生成（内置常见体式）是做什么的？` : dead
- `tools/sports/generator-random-3.html` : `瑜伽体式随机生成（内置常见体式）适合哪些场景？` : dead
- `tools/sports/heart-rate-1.html` : `关于「最大心率个体化计算」` : dead
- `tools/sports/heart-rate-1.html` : `如何使用最大心率个体化计算？` : dead
- `tools/sports/heart-rate-1.html` : `最大心率 = 220 − 年龄` : dead
- `tools/sports/heart-rate-1.html` : `最大心率个体化计算是做什么的？` : dead
- `tools/sports/heart-rate-1.html` : `最大心率个体化计算适合哪些场景？` : dead
- `tools/sports/heart-rate-2.html` : `如何使用心率变异性分析？` : dead
- `tools/sports/heart-rate-2.html` : `心率变异性分析是做什么的？` : dead
- `tools/sports/heart-rate-2.html` : `心率变异性分析适合哪些场景？` : dead
- `tools/sports/heart-rate-3.html` : `HRR 恢复 = (运动心率−恢复心率)/运动心率` : dead
- `tools/sports/heart-rate-3.html` : `如何使用心率恢复指数？` : dead
- `tools/sports/heart-rate-3.html` : `心率恢复指数是做什么的？` : dead
- `tools/sports/heart-rate-3.html` : `心率恢复指数适合哪些场景？` : dead
- `tools/sports/jianzhong-tuoshui-buye-kongzhi.html` : `减重（脱水/补液）控制是做什么的？` : dead
- `tools/sports/jianzhong-tuoshui-buye-kongzhi.html` : `减重（脱水/补液）控制适合哪些场景？` : dead
- `tools/sports/jianzhong-tuoshui-buye-kongzhi.html` : `如何使用减重（脱水/补液）控制？` : dead
- `tools/sports/jixianwei-kuai-man-leixingtuice.html` : `力耐比 = 立定跳远 ÷ 耐力跑用时；比值越高越偏快肌（爆发型）` : dead
- `tools/sports/juzhongzongchengji-sinclair-xishu.html` : `举重总成绩/体重系数计算是做什么的？` : dead
- `tools/sports/juzhongzongchengji-sinclair-xishu.html` : `举重总成绩/体重系数计算适合哪些场景？` : dead
- `tools/sports/juzhongzongchengji-sinclair-xishu.html` : `关于「举重总成绩/体重系数计算」` : dead
- `tools/sports/juzhongzongchengji-sinclair-xishu.html` : `如何使用举重总成绩/体重系数计算？` : dead
- `tools/sports/juzhongzongchengji-sinclair-xishu.html` : `总成绩 = 抓举+挺举；Sinclair 系数修正` : dead
- `tools/sports/lanqiumingzhonglv-lanbanxiaolv.html` : `关于「篮球命中率/篮板效率」` : dead
- `tools/sports/lanqiumingzhonglv-lanbanxiaolv.html` : `命中率 = 命中/出手；篮板效率 = 篮板/分钟` : dead
- `tools/sports/lanqiumingzhonglv-lanbanxiaolv.html` : `如何使用篮球命中率/篮板效率？` : dead
- `tools/sports/lanqiumingzhonglv-lanbanxiaolv.html` : `篮球命中率/篮板效率是做什么的？` : dead
- `tools/sports/lanqiumingzhonglv-lanbanxiaolv.html` : `篮球命中率/篮板效率适合哪些场景？` : dead
- `tools/sports/lingmin-zhefanpao-chengji.html` : `如何使用灵敏（折返跑）成绩？` : dead
- `tools/sports/lingmin-zhefanpao-chengji.html` : `灵敏（折返跑）成绩是做什么的？` : dead
- `tools/sports/lingmin-zhefanpao-chengji.html` : `灵敏（折返跑）成绩适合哪些场景？` : dead
- `tools/sports/pilaohuifuqushi.html` : `如何使用疲劳恢复趋势？` : dead
- `tools/sports/pilaohuifuqushi.html` : `疲劳恢复趋势是做什么的？` : dead
- `tools/sports/pilaohuifuqushi.html` : `疲劳恢复趋势适合哪些场景？` : dead
- `tools/sports/pingheng-biyandanjiao-shichang.html` : `如何使用平衡（闭眼单脚）时长？` : dead
- `tools/sports/pingheng-biyandanjiao-shichang.html` : `平衡（闭眼单脚）时长是做什么的？` : dead
- `tools/sports/pingheng-biyandanjiao-shichang.html` : `平衡（闭眼单脚）时长适合哪些场景？` : dead
- `tools/sports/pingpangqiu-xiangchi-faqiu-defen.html` : `11 分制得分统计。` : dead
- `tools/sports/pingpangqiu-xiangchi-faqiu-defen.html` : `乒乓球得分由相持与发球等环节构成：总分=相持+发球，平均=总分÷2，差距=|相持−发球|。据此分析得分结构，优化技战术侧重与训练安排。` : dead
- `tools/sports/pingpangqiu-xiangchi-faqiu-defen.html` : `乒乓球（相持/发球）得分是做什么的？` : dead
- `tools/sports/pingpangqiu-xiangchi-faqiu-defen.html` : `乒乓球（相持/发球）得分适合哪些场景？` : dead
- `tools/sports/pingpangqiu-xiangchi-faqiu-defen.html` : `如何使用乒乓球（相持/发球）得分？` : dead
- `tools/sports/pingpangqiu-xiangchi-faqiu-defen.html` : `对抗训练统计发球直接得分率与相持回合胜率，定位发球抢攻与相持短板。` : dead
- `tools/sports/pingpangqiu-xiangchi-faqiu-defen.html` : `总分 = 相持得分 + 发球得分；平均分 = 总分 ÷ 2` : dead
- `tools/sports/pingpangqiu-xiangchi-faqiu-defen.html` : `按相持与发球得分计算乒乓球单局总分与平均得分，用于技术结构分析。` : dead
- `tools/sports/pingpangqiu-xiangchi-faqiu-defen.html` : `💡 总分 = 相持 + 发球；平均分 = 总分 ÷ 2。` : dead
- `tools/sports/rater-34.html` : `如何使用排球（一传到位/扣球）评分？` : dead
- `tools/sports/rater-34.html` : `排球（一传到位/扣球）评分是做什么的？` : dead
- `tools/sports/rater-34.html` : `排球（一传到位/扣球）评分适合哪些场景？` : dead
- `tools/sports/rater-36.html` : `如何使用马术（步态/跳跃）评分？` : dead
- `tools/sports/rater-36.html` : `马术（步态/跳跃）评分是做什么的？` : dead
- `tools/sports/rater-36.html` : `马术（步态/跳跃）评分适合哪些场景？` : dead
- `tools/sports/rater-motion.html` : `Coefficient of variation(CV)是衡量动作稳定性的核心统计指标` : dead
- `tools/sports/rater-motion.html` : `Coefficient of variation(CV)自动计算` : dead
- `tools/sports/ratio-18.html` : `脂肪氧化比例 = f(运动强度)` : dead
- `tools/sports/rehab-motion.html` : `关于「损伤（预防/康复）动作」` : dead
- `tools/sports/rehab-motion.html` : `如何使用损伤（预防/康复）动作？` : dead
- `tools/sports/rehab-motion.html` : `如靠墙静蹲（膝康复）、臀桥（髋稳定）；按阶段递增负荷。` : dead
- `tools/sports/rehab-motion.html` : `康复与预防训练动作库。` : dead
- `tools/sports/rehab-motion.html` : `康复动作负荷以体重与重复次数估算：总负荷(kg)=体重×次数，单组建议时长≈次数×3秒，渐进增量≈总负荷×10%（每周）。循序增加负荷可促进组织适应，避免过度训练导致再损伤。` : dead
- `tools/sports/rehab-motion.html` : `康复动作越多越好？` : dead
- `tools/sports/rehab-motion.html` : `总负荷 = 体重 × 次数；单组时长 ≈ 次数 × 3s；周增量 ≈ 总负荷 × 10%` : dead
- `tools/sports/rehab-motion.html` : `按体重与动作重复次数估算康复动作总负荷、单组时长与渐进增量，指导安全进阶。` : dead
- `tools/sports/rehab-motion.html` : `损伤（预防/康复）动作。体育竞技工具，帮助计算与分析运动数据。` : dead
- `tools/sports/rehab-motion.html` : `损伤（预防/康复）动作是做什么的？` : dead
- `tools/sports/rehab-motion.html` : `损伤（预防/康复）动作适合哪些场景？` : dead
- `tools/sports/rehab-motion.html` : `疼了还练？` : dead
- `tools/sports/rehab-motion.html` : `膝伤康复按阶段选动作库，从激活到负重渐进防过早回归致再伤。` : dead
- `tools/sports/rehab-motion.html` : `重复次数 (次)` : dead
- `tools/sports/rehab-motion.html` : `重质量与阶段匹配，过量或跳阶反而延时愈合并增加再伤风险。` : dead
- `tools/sports/rehab-motion.html` : `锐痛停，酸胀可接受，遵医嘱。` : dead
- `tools/sports/rehab-motion.html` : `💡 总负荷 = 体重 × 次数；单组 ≈ 次数 × 3s；周增量 ≈ 总负荷 × 10%。` : dead
- `tools/sports/rouren-qianqu-cequ-jinbu.html` : `如何使用柔韧（前屈/侧屈）进步？` : dead
- `tools/sports/rouren-qianqu-cequ-jinbu.html` : `柔韧进步 = 后测 − 前测；相对提升 = 进步 ÷ 前测 × 100%` : dead
- `tools/sports/rouren-qianqu-cequ-jinbu.html` : `柔韧（前屈/侧屈）进步是做什么的？` : dead
- `tools/sports/rouren-qianqu-cequ-jinbu.html` : `柔韧（前屈/侧屈）进步适合哪些场景？` : dead
- `tools/sports/shejiansanbubanjing.html` : `如何使用射箭散布半径？` : dead
- `tools/sports/shejiansanbubanjing.html` : `射箭散布半径是做什么的？` : dead
- `tools/sports/shejiansanbubanjing.html` : `射箭散布半径适合哪些场景？` : dead
- `tools/sports/shejiansanbubanjing.html` : `散布半径 = √(Σd²/n)` : dead
- `tools/sports/sheyangdonglixuebanshi.html` : `VO2 半时 = ln2/动力学常数` : dead
- `tools/sports/shuimianhuifuzhiliang.html` : `如何使用睡眠恢复质量？` : dead
- `tools/sports/shuimianhuifuzhiliang.html` : `睡眠恢复 = f(时长, 深睡)` : dead
- `tools/sports/shuimianhuifuzhiliang.html` : `睡眠恢复质量是做什么的？` : dead
- `tools/sports/shuimianhuifuzhiliang.html` : `睡眠恢复质量适合哪些场景？` : dead
- `tools/sports/simulator-18.html` : `伯努利试验模拟是做什么的？` : dead
- `tools/sports/simulator-18.html` : `伯努利试验模拟适合哪些场景？` : dead
- `tools/sports/simulator-18.html` : `如何使用伯努利试验模拟？` : dead
- `tools/sports/sleeping-bag-rating.html` : `如何使用睡袋温标对照？` : dead
- `tools/sports/sleeping-bag-rating.html` : `睡袋温标对照是做什么的？` : dead
- `tools/sports/sleeping-bag-rating.html` : `睡袋温标对照适合哪些场景？` : dead
- `tools/sports/speed-5.html` : `如何使用速度加速度分解？` : dead
- `tools/sports/speed-5.html` : `速度 = 距离/时间；加速度 = Δv/Δt` : dead
- `tools/sports/speed-5.html` : `速度加速度分解是做什么的？` : dead
- `tools/sports/speed-5.html` : `速度加速度分解适合哪些场景？` : dead
- `tools/sports/speed-6.html` : `击剑弓步速度 = 距离/时间` : dead
- `tools/sports/speed-6.html` : `击剑弓步速度分析是做什么的？` : dead
- `tools/sports/speed-6.html` : `击剑弓步速度分析适合哪些场景？` : dead
- `tools/sports/speed-6.html` : `如何使用击剑弓步速度分析？` : dead
- `tools/sports/sports-calculator.html` : `体育计算器是做什么的？` : dead
- `tools/sports/sports-calculator.html` : `体育计算器适合哪些场景？` : dead
- `tools/sports/sports-calculator.html` : `如何使用体育计算器？` : dead
- `tools/sports/sports-reference.html` : `体育户外参考工具是做什么的？` : dead
- `tools/sports/sports-reference.html` : `体育户外参考工具适合哪些场景？` : dead
- `tools/sports/sports-reference.html` : `如何使用体育户外参考工具？` : dead
- `tools/sports/sports-schedule.html` : `关于「每周运动计划表」` : dead
- `tools/sports/sports-stats.html` : `如何使用运动数据统计？` : dead
- `tools/sports/sports-stats.html` : `运动数据统计是做什么的？` : dead
- `tools/sports/sports-stats.html` : `运动数据统计适合哪些场景？` : dead
- `tools/sports/stats-11.html` : `如何使用成绩（统计/公布/证书）系统？` : dead
- `tools/sports/stats-11.html` : `成绩（统计/公布/证书）系统是做什么的？` : dead
- `tools/sports/stats-11.html` : `成绩（统计/公布/证书）系统适合哪些场景？` : dead
- `tools/sports/stats-11.html` : `评估（满意度/效果/报告）方法` : dead
- `tools/sports/stats-8.html` : `如何使用足球（控球率/传球成功）统计？` : dead
- `tools/sports/stats-8.html` : `足球（控球率/传球成功）统计是做什么的？` : dead
- `tools/sports/stats-8.html` : `足球（控球率/传球成功）统计适合哪些场景？` : dead
- `tools/sports/strength-5.html` : `如何使用训练周计划强度分布？` : dead
- `tools/sports/strength-5.html` : `训练周计划强度分布是做什么的？` : dead
- `tools/sports/strength-5.html` : `训练周计划强度分布适合哪些场景？` : dead
- `tools/sports/swimming-stroke-efficiency.html` : `如何使用游泳划水效率计算？` : dead
- `tools/sports/swimming-stroke-efficiency.html` : `游泳划水效率计算是做什么的？` : dead
- `tools/sports/swimming-stroke-efficiency.html` : `游泳划水效率计算适合哪些场景？` : dead
- `tools/sports/taiquandao-hengti-xiapi-defen.html` : `总分 = 横踢得分 + 下劈得分；平均分 = 总分 ÷ 2` : dead
- `tools/sports/tester-1.html` : `俯卧撑/引体向上极限测试（推算1RM）是做什么的？` : dead
- `tools/sports/tester-1.html` : `俯卧撑/引体向上极限测试（推算1RM）适合哪些场景？` : dead
- `tools/sports/tester-1.html` : `如何使用俯卧撑/引体向上极限测试（推算1RM）？` : dead
- `tools/sports/tester-7.html` : `如何使用耐力（AT/VO2max）测试？` : dead
- `tools/sports/tester-7.html` : `耐力（AT/VO2max）测试是做什么的？` : dead
- `tools/sports/tester-7.html` : `耐力（AT/VO2max）测试适合哪些场景？` : dead
- `tools/sports/tester-8.html` : `如何使用最大（累积氧亏）测试？` : dead
- `tools/sports/tester-8.html` : `最大（累积氧亏）测试是做什么的？` : dead
- `tools/sports/tester-8.html` : `最大（累积氧亏）测试适合哪些场景？` : dead
- `tools/sports/time-31.html` : `如何使用摔跤比赛时间分配？` : dead
- `tools/sports/time-31.html` : `摔跤比赛时间分配是做什么的？` : dead
- `tools/sports/time-31.html` : `摔跤比赛时间分配适合哪些场景？` : dead
- `tools/sports/tongqibizhifenxi.html` : `如何使用通气比值分析？` : dead
- `tools/sports/tongqibizhifenxi.html` : `通气比值分析是做什么的？` : dead
- `tools/sports/tongqibizhifenxi.html` : `通气比值分析适合哪些场景？` : dead
- `tools/sports/training-planner.html` : `4–6 周按反馈微调。` : dead
- `tools/sports/training-planner.html` : `一般基于储备心率或乳酸阈划分，再按周期目标分配各区间周占比。` : dead
- `tools/sports/training-planner.html` : `个性化训练计划按目标、水平与可用时间生成：以容量(次数×组数×重量)为基线，每周渐进增量控制在 10% 以内，动作、组次与进阶节奏自动编排。` : dead
- `tools/sports/training-planner.html` : `减脂：每周 4 次有氧+2 次力量+1 柔韧；增肌：分化训练 5 次。` : dead
- `tools/sports/training-planner.html` : `单周排期：按部位与每周天数生成 3–6 天分化安排；多周周期化、减量周与本页无关，需另行规划。` : dead
- `tools/sports/training-planner.html` : `基于你的目标和水平生成专属训练计划` : dead
- `tools/sports/training-planner.html` : `备赛期按周量与强度分布自动生成周期化计划，保证渐进超负荷且有减量周。` : dead
- `tools/sports/training-planner.html` : `如何使用训练计划生成？` : dead
- `tools/sports/training-planner.html` : `按目标/水平排计划。` : dead
- `tools/sports/training-planner.html` : `本工具只给动作与组次，不计算重量百分比或心率区间。重量应按个人 1RM 的百分比或 RPE（自觉用力程度）自行设定，并在 4–6 周后按反馈调整。` : dead
- `tools/sports/training-planner.html` : `渐进负荷：周增量 ≤ 10%；容量 = 次数×组数×重量` : dead
- `tools/sports/training-planner.html` : `计划里的强度区间怎么定？` : dead
- `tools/sports/training-planner.html` : `计划里的重量和强度区间怎么定？` : dead
- `tools/sports/training-planner.html` : `训练计划生成是做什么的？` : dead
- `tools/sports/training-planner.html` : `训练计划生成适合哪些场景？` : dead
- `tools/sports/triathlon-transition.html` : `如何使用铁人三项转换时间计算？` : dead
- `tools/sports/triathlon-transition.html` : `铁人三项转换时间计算是做什么的？` : dead
- `tools/sports/triathlon-transition.html` : `铁人三项转换时间计算适合哪些场景？` : dead
- `tools/sports/wangqiudefenlvfenxi.html` : `ACE率 = ACE / 发球总数；破发点挽救率 = 挽救 / 面临破发点` : dead
- `tools/sports/wangqiudefenlvfenxi.html` : `如何使用网球得分率分析？` : dead
- `tools/sports/wangqiudefenlvfenxi.html` : `网球得分率分析是做什么的？` : dead
- `tools/sports/wangqiudefenlvfenxi.html` : `网球得分率分析适合哪些场景？` : dead
- `tools/sports/xuerusuanyuzhiceding.html` : `LT = 血乳酸较基线升高 1.0mmol/L 时的心率` : dead
- `tools/sports/yangmaiboxiaolv.html` : `如何使用氧脉搏效率？` : dead
- `tools/sports/yangmaiboxiaolv.html` : `氧脉搏效率是做什么的？` : dead
- `tools/sports/yangmaiboxiaolv.html` : `氧脉搏效率适合哪些场景？` : dead
- `tools/sports/yoga-pose-generator.html` : `如何使用瑜伽体式随机生成？` : dead
- `tools/sports/yoga-pose-generator.html` : `瑜伽体式随机生成是做什么的？` : dead
- `tools/sports/yoga-pose-generator.html` : `瑜伽体式随机生成适合哪些场景？` : dead
- `tools/sports/youyonghuashuixiaolv-swolf.html` : `SWOLF = 单趟时间(秒) + 划水次数；DPS = 池长 / 划次` : dead
- `tools/sports/youyonghuashuixiaolv-swolf.html` : `关于「游泳划水效率」` : dead
- `tools/sports/youyonghuashuixiaolv-swolf.html` : `如何使用游泳划水效率？` : dead
- `tools/sports/youyonghuashuixiaolv-swolf.html` : `游泳划水效率是做什么的？` : dead
- `tools/sports/youyonghuashuixiaolv-swolf.html` : `游泳划水效率适合哪些场景？` : dead
- `tools/sports/yumaoqiushaqiuxiaolv.html` : `如何使用羽毛球杀球效率？` : dead
- `tools/sports/yumaoqiushaqiuxiaolv.html` : `羽毛球杀球效率是做什么的？` : dead
- `tools/sports/yumaoqiushaqiuxiaolv.html` : `羽毛球杀球效率适合哪些场景？` : dead

  其它成因样例（共 36 条，仅列前 5）：
  - `tools/sports/analysis-20.html` : `样本标准差 SD = √[ Σ(xᵢ − x̄)² ÷ (n − 1) ]` : fragment
  - `tools/sports/analysis-20.html` : `变异系数 CV = SD ÷ 平均环值 × 100%` : fragment
  - `tools/sports/assessor-csat.html` : `综合效果分 = (组织执行 + 场馆设施 + 宣传推广 + 安全保障) ÷ 4` : fragment
  - `tools/sports/calc-heart-rate-1.html` : `HRR = 最大心率 − 静息心率` : fragment
  - `tools/sports/estimate-tester.html` : `1.5英里跑公式：VO2max=483/时间(秒)+3.5` : dynamic

### startup（dead 1 / dynamic 0 / fragment 0 / harmless 0）

- `tools/startup/burn-rate.html` : `预警分级：跑道 <6 月 高危｜<9 月 加速｜<12 月 提示｜其他 充裕` : dead

### statistics（dead 31 / dynamic 0 / fragment 1 / harmless 0）

- `tools/statistics/binomial-pmf.html` : `X=k)=C(n,k)p^k(1−p)^(n−k)。 10 投 3 中、p=0.5 → 0.1172。` : dead
- `tools/statistics/chi-square-test.html` : `χ² = Σ(O−E)²/E。 df = 类别数 − 1。` : dead
- `tools/statistics/confidence-proportion.html` : `结果可视化` : dead
- `tools/statistics/correlation-r-squared.html` : `结果可视化` : dead
- `tools/statistics/f-test-variance.html` : `结果可视化` : dead
- `tools/statistics/geometric-mean.html` : `结果可视化` : dead
- `tools/statistics/harmonic-mean.html` : `结果可视化` : dead
- `tools/statistics/independent-t-test.html` : `结果可视化` : dead
- `tools/statistics/mean-absolute-deviation.html` : `结果可视化` : dead
- `tools/statistics/odds-ratio.html` : `结果可视化` : dead
- `tools/statistics/p.html` : `双尾 p = 2 · (1 − Φ(|Z|))` : dead
- `tools/statistics/paired-t-test.html` : `结果可视化` : dead
- `tools/statistics/percentile-rank.html` : `PR = (Below+0.5·Equal)/N×100。 描述相对位置。` : dead
- `tools/statistics/percentile-rank.html` : `结果可视化` : dead
- `tools/statistics/poisson-pmf.html` : `结果可视化` : dead
- `tools/statistics/probability-complement.html` : `结果可视化` : dead
- `tools/statistics/relative-risk.html` : `结果可视化` : dead
- `tools/statistics/sample-size-mean.html` : `结果可视化` : dead
- `tools/statistics/sample-size-proportion.html` : `p=0.5 时样本量最大。 95% 置信取 z=1.96。` : dead
- `tools/statistics/sample-variance.html` : `s² = Σ(xᵢ−x̄)²/(n−1)。 分母为 n−1（无偏）。` : dead
- `tools/statistics/standard-error.html` : `结果可视化` : dead
- `tools/statistics/standard-error-proportion.html` : `结果可视化` : dead
- `tools/statistics/statistics-10.html` : `CV = (标准差 / |均值|) × 100%` : dead
- `tools/statistics/statistics-11.html` : `加权平均 = Σ(xᵢ · wᵢ) / Σwᵢ` : dead
- `tools/statistics/statistics-11.html` : `加权平均 x̄_w = (v₁w₁ + v₂w₂ + v₃w₃) / (w₁ + w₂ + w₃)` : dead
- `tools/statistics/statistics-4.html` : `CI = x̄ ± z · s / √n；z 由置信水平按逆正态近似反解（双侧）` : dead
- `tools/statistics/t.html` : `t = (x̄ − μ₀) / (s / √n)；自由度 df = n − 1` : dead
- `tools/statistics/t-score.html` : `结果可视化` : dead
- `tools/statistics/variance-list.html` : `结果可视化` : dead
- `tools/statistics/z.html` : `Z = (x − μ) / σ；百分位 = Φ(Z) × 100%；距均值 = |Z| 个标准差` : dead
- `tools/statistics/z.html` : `百分位 Φ(Z) 由正态分布累积函数近似` : dead

  其它成因样例（共 1 条，仅列前 5）：
  - `tools/statistics/f-test-variance.html` : `p = 2·min(右尾,左尾)。` : fragment

### stats（dead 1 / dynamic 0 / fragment 0 / harmless 0）

- `tools/stats/regression-analysis.html` : `Slope b 的 95% 置信区间 [1.9324, 2.0409] 不含 0，说明自变量与因变量存在显著线性关系；若区间跨越 0 则关系不显著。` : dead

### structural（dead 6 / dynamic 0 / fragment 0 / harmless 0）

- `tools/structural/angle-of-twist.html` : `θ = TL/(GJ)。 示例 → 约 0.0102 rad。` : dead
- `tools/structural/deflection-cantilever-point.html` : `δ = FL³/(3EI)（自由端）。 示例 → 约 0.272 mm。` : dead
- `tools/structural/deflection-cantilever-udl.html` : `δ = wL⁴/(8EI)（自由端）。 示例 → 约 2.04 mm。` : dead
- `tools/structural/hoop-stress.html` : `薄壁假设 t/r < 0.1。` : dead
- `tools/structural/longitudinal-stress.html` : `σ_l = σ_h/2。 同上例 → 50 MPa。` : dead
- `tools/structural/ss-point-deflection.html` : `δ = PL³/(48EI)（跨中集中力）。 示例约 8.33 mm。` : dead

### surveying（dead 15 / dynamic 0 / fragment 4 / harmless 0）

- `tools/surveying/area-calc.html` : `A = 长 × 宽（矩形）或 ½|Σ(x(i)·y(i+1)−x(i+1)·y(i))|` : dead
- `tools/surveying/calc-1.html` : `平差改正数 v_i = −f_h/n（闭合差均摊）` : dead
- `tools/surveying/calc-angle-2.html` : `十进制 = 度 + 分/60 + 秒/3600` : dead
- `tools/surveying/convert-33.html` : `平距 D = S·cos α，高差 h = S·sin α（α 为竖直角）` : dead
- `tools/surveying/convert-46.html` : `千坐标` : dead
- `tools/surveying/convert-46.html` : `千度分秒转换` : dead
- `tools/surveying/convert-46.html` : `毫坐标` : dead
- `tools/surveying/convert-46.html` : `毫度分秒转换` : dead
- `tools/surveying/coordinate-convert.html` : `坐标转换：仿射或七参数` : dead
- `tools/surveying/cut-fill-volume.html` : `V = (A₁+A₂)/2 · L（相邻断面）` : dead
- `tools/surveying/elevation-diff.html` : `闭合差 f_h = Σh − (H_终−H_起)` : dead
- `tools/surveying/grade-angle.html` : `坡度 i = tanα × 100%` : dead
- `tools/surveying/horizontal-from-slope.html` : `平距 = 斜距·cos(垂直角)` : dead
- `tools/surveying/scale-converter.html` : `图上长 = 实地长 / 比例尺分母` : dead
- `tools/surveying/vertical-curve-elev.html` : `抛物线竖曲线 y = ax²+bx+c` : dead

  其它成因样例（共 4 条，仅列前 5）：
  - `tools/surveying/convert-46.html` : `坐标` : fragment
  - `tools/surveying/convert-46.html` : `度分秒转换` : fragment
  - `tools/surveying/leveling-calc.html` : `H(i) = H(i−1) + 后视 − 前视` : fragment
  - `tools/surveying/slope-percent.html` : `= 高差 / 平距` : fragment

### tax（dead 13 / dynamic 0 / fragment 10 / harmless 0）

- `tools/tax/ad-valorem-duty.html` : `从价税 = 计税价×税率` : dead
- `tools/tax/average-tax-rate.html` : `平均税率 = 总税/总收入` : dead
- `tools/tax/capital-gains-effective.html` : `应缴税 = 收益×优惠税率` : dead
- `tools/tax/excise-tax.html` : `从价消费税 = 计税价×数量×税率。 10×100×20% → 200 元。` : dead
- `tools/tax/foreign-tax-credit.html` : `可抵扣 = min(境外已纳, 抵免限额)` : dead
- `tools/tax/marginal-tax-rate.html` : `MTR = Δ税额/Δ收入。 收入增 5 万、税额增 1.5 万 → 30%。` : dead
- `tools/tax/progressive-income-tax.html` : `3000=6000。 可改档位模拟个税/企税。` : dead
- `tools/tax/reverse-charge.html` : `代扣代缴 = 代扣金额×征收率` : dead
- `tools/tax/social-security-tax.html` : `社保费 = 基数×费率` : dead
- `tools/tax/specific-duty.html` : `从量税 = 数量×单位税额` : dead
- `tools/tax/tax-credit.html` : `实缴 = max(应纳税额−抵免, 0)` : dead
- `tools/tax/tax-to-gdp.html` : `宏观税负 = 税收/GDP × 100%` : dead
- `tools/tax/vat-output.html` : `销项税额 = 销售额×税率` : dead

  其它成因样例（共 10 条，仅列前 5）：
  - `tools/tax/corporate-income-tax.html` : `= 应纳税所得额` : fragment
  - `tools/tax/customs-duty.html` : `= 完税价格` : fragment
  - `tools/tax/effective-tax-rate.html` : `= 总税额` : fragment
  - `tools/tax/interest-income-tax.html` : `= 利息` : fragment
  - `tools/tax/property-tax.html` : `= 计税余值` : fragment

### tcm-chemistry（dead 4 / dynamic 3 / fragment 0 / harmless 0）

- `tools/tcm-chemistry/metabolite-prediction.html` : `口服与静脉两条给药路径的首过差异提示：口服强调肠道菌群与肠壁/肝首过，静脉强调肝脏 CYP 代谢。` : dead
- `tools/tcm-chemistry/metabolite-prediction.html` : `按化合物类别速查常见 I 相（氧化/水解/还原）与 II 相（结合）反应，不依赖网络数据库。` : dead
- `tools/tcm-chemistry/metabolite-prediction.html` : `用分子量做代谢产物的质量差估算（脱糖基 −162、羟基化 +16、葡萄糖醛酸化 +176 等），用于对照 LC-MS 的 m/z 差值。` : dead
- `tools/tcm-chemistry/metabolite-prediction.html` : `选中具体化合物时给出该化合物的常见文献代谢要点；未选中时仅展示类别模板。` : dead

  其它成因样例（共 3 条，仅列前 5）：
  - `tools/tcm-chemistry/metabolite-prediction.html` : `脱糖基(-C₆H₁₀O₅)` : dynamic
  - `tools/tcm-chemistry/metabolite-prediction.html` : `* 上表按官能团加合/丢失的固定质量差估算（脱糖基 −162、羟基化 +16、去甲基 −14、葡萄糖醛酸化 +176、硫酸化 +80、脱水 −18），不是该化合物实测分子量；数值 ≤ 0 时以「—」显示。` : dynamic
  - `tools/tcm-chemistry/solubility-guide.html` : `导出明细 CSV` : dynamic

### tcm-diagnosis（dead 1 / dynamic 0 / fragment 0 / harmless 0）

- `tools/tcm-diagnosis/constitution-test.html` : `⚠️ 体质判定标准：转化分≥60分为"是"，40-59分为"倾向是"，<40分为"否"。可同时具备多种体质倾向（兼夹体质）。本工具仅供健康参考，不能替代医师诊断。` : dead

### telecom（dead 5 / dynamic 8 / fragment 0 / harmless 0）

- `tools/telecom/ap-coverage.html` : `Pt = 20 dBm、Gt = 3 dBi、Gr = 2 dBi、接收灵敏度 −75 dBm、频率 2400 MHz、附加损耗 0 dB、衰落余量 10 dB、环境"室内办公(多墙)"附加 8 dB → 总损耗 18 dB。MAPL = 20 + 3 + 2 − (−75) − 18 = 82.00 dB；d = 1…(+152字)` : dead
- `tools/telecom/bandwidth-calculator.html` : `MB/s (兆字节/秒)` : dead
- `tools/telecom/convert-24.html` : `信噪比 SNR (dB)` : dead
- `tools/telecom/convert-24.html` : `其中 SNR 为信噪比（dB），erfc 为互补误差函数。` : dead
- `tools/telecom/quick-calc-time-bandwidth.html` : `带宽与时间换算：时间 =（文件大小 × 8）÷ 带宽；带宽 =（文件大小 × 8）÷ 时间；1 MB = 8 Mbit，故 100 Mbps 下 1 GB 约 80 秒；常见文件（照片约 5 MB、歌曲约 10 MB、电影约 4 GB）可对照速估。` : dead

  其它成因样例（共 8 条，仅列前 5）：
  - `tools/telecom/bandwidth-calculator.html` : `传输效率需在 1–100% 之间` : dynamic
  - `tools/telecom/convert-24.html` : `请输入有效 SNR（dB，可为负数）` : dynamic
  - `tools/telecom/distance-power-frequency.html` : `5,800 MHz 理想视距最大传输距离约` : dynamic
  - `tools/telecom/estimate-9.html` : `接收功率（自动单位）` : dynamic
  - `tools/telecom/path-loss.html` : `接收功率（自动单位）` : dynamic

### text（dead 3 / dynamic 11 / fragment 0 / harmless 0）

- `tools/text/index.html` : `将文字左右镜像反转生成可复制的字符或预览图，用于趣味签名、艺术字与水印，纯前端即时转换支持一键复制结果。` : dead
- `tools/text/index.html` : `文本处理工具集合收录了 13 个免费在线工具，覆盖文本处理场景下的常见计算、换算与查询需求。无论你是相关领域的从业者、学生还是普通用户，都能在这里找到即用即走的实用小工具。所有工具纯前端运行，数据不上传服务器，保护隐私安全。` : dead
- `tools/text/index.html` : `金融文本自动换行工具，按指定宽度对段落折行，适合报表备注与文档排版对齐，纯前端即时处理。` : dead

  其它成因样例（共 11 条，仅列前 5）：
  - `tools/text/analysis-density.html` : `请输入文本` : dynamic
  - `tools/text/analysis-density.html` : `请输入至少一个关键词` : dynamic
  - `tools/text/analysis-density.html` : `不适用（无汉字/英文单词）` : dynamic
  - `tools/text/analysis-density.html` : `密度 = 关键词出现次数 ÷ 合计词数 × 100%；英文关键词按整词计数，中文关键词按子串计数；建议区间 1%–5%，过高可能被判定堆砌。` : dynamic
  - `tools/text/reading-time-estimator.html` : `请输入大于 0 的阅读速度（中文按字/分、英文按词/分）。` : dynamic

### textile（dead 5 / dynamic 4 / fragment 0 / harmless 0）

- `tools/textile/fabric-3.html` : `依据 GB 色牢度 1~5 级（4 级为良好）等质量指标综合评估` : dead
- `tools/textile/fuliao-lalian-niukou-guige.html` : `拉链长度 = 开口 + 2×余量；纽扣数量 = ceil(开口/间距)+1` : dead
- `tools/textile/kangjingdianbanshuaiqi.html` : `半衰期 < 2s 为优良抗静电，< 10s 为合格` : dead
- `tools/textile/kangjingdianbanshuaiqi.html` : `要求 Vt < V₀，且两者均大于 0` : dead
- `tools/textile/shrinkage.html` : `缩水率  = (原尺寸 - 水洗后尺寸) / 原尺寸 × 100%` : dead

  其它成因样例（共 4 条，仅列前 5）：
  - `tools/textile/fabric-1.html` : `每匹总重 (kg)` : dynamic
  - `tools/textile/fabric-1.html` : `每米重量 (g/m)` : dynamic
  - `tools/textile/fabric-1.html` : `纬纱用量 (kg)` : dynamic
  - `tools/textile/fabric-1.html` : `经纱用量 (kg)` : dynamic

### thermodynamics（dead 9 / dynamic 0 / fragment 0 / harmless 0）

- `tools/thermodynamics/biot-number.html` : `Bi = hL/k。Bi 金属小件常满足 Bi` : dead
- `tools/thermodynamics/biot-number.html` : `Bi = hL/k。Bi<0.1 时可用集总参数法。` : dead
- `tools/thermodynamics/biot-number.html` : `金属小件常满足 Bi<<1。` : dead
- `tools/thermodynamics/boyles-law.html` : `等温压强-体积（P₁V₁ = P₂V₂）` : dead
- `tools/thermodynamics/charles-law.html` : `等压体积-温度（V₂ = V₁·T₂ / T₁）` : dead
- `tools/thermodynamics/gay-lussac-law.html` : `等容压强-温度（P₂ = P₁·T₂ / T₁）` : dead
- `tools/thermodynamics/newton-cooling.html` : `k 0.05→0.02：30s 后 T≈82.1 ℃。` : dead
- `tools/thermodynamics/polytropic-work.html` : `W=(P₂V₂−P₁V₁)/(1−n)（SI 单位）。 n=1 时退化为等温，需另用 ln 式。` : dead
- `tools/thermodynamics/thermal-resistance-series.html` : `R=R1+R2，U=1/R_total。 保温层+砖墙示例可得低 U 值。` : dead

### travel（dead 5 / dynamic 3 / fragment 1 / harmless 0）

- `tools/travel/index.html` : `旅行出行工具集合收录了 21 个免费在线工具，覆盖旅行出行场景下的常见计算、换算与查询需求。无论你是相关领域的从业者、学生还是普通用户，都能在这里找到即用即走的实用小工具。所有工具纯前端运行，数据不上传服务器，保护隐私安全。` : dead
- `tools/travel/road-trip-gas-cost.html` : `选 EV 预设用电耗折算，或自定义把「油耗」填度电耗、油价填电价。` : dead
- `tools/travel/zhangpengfangfengxishu.html` : `如何使用帐篷防风系数？` : dead
- `tools/travel/zhangpengfangfengxishu.html` : `帐篷防风系数是做什么的？` : dead
- `tools/travel/zhangpengfangfengxishu.html` : `帐篷防风系数适合哪些场景？` : dead

  其它成因样例（共 4 条，仅列前 5）：
  - `tools/travel/road-trip-gas-cost.html` : `百公里电耗 (kWh/100km)` : dynamic
  - `tools/travel/road-trip-gas-cost.html` : `电价 (元/kWh)` : dynamic
  - `tools/travel/road-trip-gas-cost.html` : `所需电量` : dynamic
  - `tools/travel/road-trip-gas-cost.html` : `电费` : fragment

### tunnel（dead 6 / dynamic 2 / fragment 0 / harmless 0）

- `tools/tunnel/support-design.html` : `喷射混凝土厚度 t 按围岩级别取 5~25cm；` : dead
- `tools/tunnel/support-design.html` : `锚杆长度 L 按塌落拱高度估算（一般为跨度的 1/3~1/4，且不小于 2m）；` : dead
- `tools/tunnel/support-design.html` : `锚杆间距 S 通常取 0.8~1.5m，且 S ≤ L/2；` : dead
- `tools/tunnel/ventilation-calc.html` : `工具按 v×3600÷100 估算每小时换气次数，即默认以 100 m 长的洞段为基准（风速乘以一小时走过的距离，再除以 100 m 段长）。若实际通风区段长度不同，应自行按 v×3600÷实际段长 换算，否则换气次数会被系统性放大或缩小。` : dead
- `tools/tunnel/ventilation-calc.html` : `按 CO 稀释（CO 模式）：CO 排放总量=单车排放量 q×小时交通量 N×隧道长度 L；需风量 Q=q×N×L÷δ（δ 为 CO 容许浓度，直接以 ppm 数值代入）；再反算所需控制风速 v=Q÷3600÷A，以及换气次数 n=v×3600÷L。` : dead
- `tools/tunnel/ventilation-calc.html` : `换气次数里的 100 是什么意思？` : dead

  其它成因样例（共 2 条，仅列前 5）：
  - `tools/tunnel/ventilation-calc.html` : `请输入有效的断面积 A 与控制风速 v（均需大于 0）。` : dynamic
  - `tools/tunnel/ventilation-calc.html` : `请输入有效参数：隧道长度、交通量、CO 排放量与容许浓度、断面积均需大于 0。` : dynamic

### urology（dead 6 / dynamic 23 / fragment 0 / harmless 0）

- `tools/urology/assessor-pressure.html` : `严重降低 (<10)` : dead
- `tools/urology/hydronephrosis.html` : `重度肾积水(SFU 4级 / APD>20mm / 皮质<5mm)提示肾功能受损，需尽早解除梗阻（支架/造瘘/手术）并行肾显像评估分肾功能。` : dead
- `tools/urology/iief5-score.html` : `国际勃起功能问卷简表（IIEF-5）总分 5–25，5 题各 1–5 分相加：` : dead
- `tools/urology/iief5-score.html` : `评分基于过去6个月性生活情况。若近期无性生活（Q2–Q5 选"0"），评分参考价值有限。 ⏎       ED 病因包括心理性、血管性、神经性、内分泌性及药物性，建议结合睾酮、血糖、血脂等检查综合评估。` : dead
- `tools/urology/ipss-score.html` : `IPSS 国际前列腺症状评分 = 求和 7 个问题（每项 0 至 5，满分 35）再加生活质量 QOL（0 至 6）；总分 不超过7 轻度、8 至 19 中度、不低于20 重度。` : dead
- `tools/urology/ipss-score.html` : `排尿不尽、2h 内再排、间断、尿急、尿线变细、费力、夜尿；每项 0-5，7 项合计满分 35（不含 QoL）；QoL 0-6 单独记录。` : dead

  其它成因样例（共 23 条，仅列前 5）：
  - `tools/urology/assessor-pressure.html` : `有（低压<20cmH2O）` : dynamic
  - `tools/urology/iief5-score.html` : `1. 对获得和维持勃起有多大信心？（1–5 分）` : dynamic
  - `tools/urology/iief5-score.html` : `2. 受到性刺激后，阴茎坚挺进入阴道的次数？（0–5 分）` : dynamic
  - `tools/urology/iief5-score.html` : `3. 性交时，阴茎进入阴道后维持勃起的次数？（0–5 分）` : dynamic
  - `tools/urology/iief5-score.html` : `4. 性交时，维持勃起到性交完毕的困难程度？（0–5 分）` : dynamic

### usedcar（dead 1 / dynamic 4 / fragment 0 / harmless 0）

- `tools/usedcar/index.html` : `二手车工具集合收录了 11 个免费在线工具，覆盖二手车场景下的常见计算、换算与查询需求。无论你是相关领域的从业者、学生还是普通用户，都能在这里找到即用即走的实用小工具。所有工具纯前端运行，数据不上传服务器，保护隐私安全。` : dead

  其它成因样例（共 4 条，仅列前 5）：
  - `tools/usedcar/car-residual.html` : `新车购置价需为有效的非负数值` : dynamic
  - `tools/usedcar/car-residual.html` : `已使用年限需在 0–30 年之间` : dynamic
  - `tools/usedcar/car-residual.html` : `折旧年限需在 1–30 年之间` : dynamic
  - `tools/usedcar/car-residual.html` : `残值率需在 0–100 之间` : dynamic

### video（dead 1 / dynamic 0 / fragment 0 / harmless 0）

- `tools/video/index.html` : `视频处理工具集合收录了 6 个免费在线工具，覆盖视频处理场景下的常见计算、换算与查询需求。无论你是相关领域的从业者、学生还是普通用户，都能在这里找到即用即走的实用小工具。所有工具纯前端运行，数据不上传服务器，保护隐私安全。` : dead

### wedding（dead 21 / dynamic 61 / fragment 4 / harmless 9）

- `tools/wedding/countdown-timeline.html` : `交换戒指、宣誓环节（约10分钟）` : dead
- `tools/wedding/countdown-timeline.html` : `伴娘堵门游戏环节（约30分钟）` : dead
- `tools/wedding/countdown-timeline.html` : `双方父母致辞感谢来宾（约15分钟）` : dead
- `tools/wedding/countdown-timeline.html` : `向女方父母敬茶、改口（约30分钟）` : dead
- `tools/wedding/countdown-timeline.html` : `天 8小时 2分钟` : dead
- `tools/wedding/countdown-timeline.html` : `婚车队伍前往婚礼场地（约30分钟）` : dead
- `tools/wedding/countdown-timeline.html` : `宾客入席，婚宴正式开始（约180分钟）` : dead
- `tools/wedding/countdown-timeline.html` : `摄影摄像团队到达，拍摄准备花絮（约30分钟）` : dead
- `tools/wedding/countdown-timeline.html` : `新人逐桌敬酒（约60分钟）` : dead
- `tools/wedding/countdown-timeline.html` : `新娘化妆、发型设计开始（约120分钟）` : dead
- `tools/wedding/countdown-timeline.html` : `新娘抛捧花环节（约10分钟）` : dead
- `tools/wedding/countdown-timeline.html` : `新郎带队出发接亲（约60分钟）` : dead
- `tools/wedding/countdown-timeline.html` : `欢送宾客，婚礼圆满结束（约30分钟）` : dead
- `tools/wedding/countdown-timeline.html` : `正式婚礼仪式开始（约40分钟）` : dead
- `tools/wedding/wedding-banquet.html` : `关于「婚宴桌数估算器」` : dead
- `tools/wedding/wedding-banquet.html` : `如何使用婚宴桌数估算器？` : dead
- `tools/wedding/wedding-banquet.html` : `婚宴桌数估算器是做什么的？` : dead
- `tools/wedding/wedding-banquet.html` : `婚宴桌数估算器适合哪些场景？` : dead
- `tools/wedding/wedding-budget-planner.html` : `已花费 0.0% | 已分配 100.0%` : dead
- `tools/wedding/wedding-budget-planner.html` : `最大支出项：婚宴酒席（¥35,000）` : dead
- `tools/wedding/wedding-car-route.html` : `（行驶26分 + 停留1时20分 + 缓冲15分）` : dead

  其它成因样例（共 74 条，仅列前 5）：
  - `tools/wedding/countdown-timeline.html` : `剩余天数` : fragment
  - `tools/wedding/countdown-timeline.html` : `剩余小时` : dynamic
  - `tools/wedding/countdown-timeline.html` : `总倒计时` : dynamic
  - `tools/wedding/countdown-timeline.html` : `当前阶段：` : dynamic
  - `tools/wedding/countdown-timeline.html` : `中期筹备阶段` : dynamic

### welding（dead 13 / dynamic 24 / fragment 2 / harmless 3）

- `tools/welding/calc-1.html` : `手工电弧焊电流经验式：I = k × d（k 为经验系数，一般取 30 至 50，d 为焊条直径 mm）；焊接线能量 E = 60 × U × I ÷ v，U 为电弧电压（V）、I 为电流（A）、v 为焊接速度（mm/min）；据焊条直径与材质推荐电流区间。` : dead
- `tools/welding/calc-weld.html` : `焊缝强度 = 焊脚×长度×强度` : dead
- `tools/welding/hanjiegongyicanshu.html` : `焊接电流/电压依据材料厚度与焊接方法（经验区间）` : dead
- `tools/welding/hanjiezidonghuapinggu.html` : `💡 机器人焊接时间约为人工 40%；投资回收期 <3 年为推荐，<2 年为强烈推荐。` : dead
- `tools/welding/index.html` : `焊接工程工具集合收录了 15 个免费在线工具，覆盖焊接工程场景下的常见计算、换算与查询需求。无论你是相关领域的从业者、学生还是普通用户，都能在这里找到即用即走的实用小工具。所有工具纯前端运行，数据不上传服务器，保护隐私安全。` : dead
- `tools/welding/temp-time-6.html` : `核心计算公式（按输入变量）：cV+mnV÷6+(crV+moV)÷5；100+(ce-0.5)×500；150+(ce-0.6)×500` : dead
- `tools/welding/temp-time-6.html` : `💡 CEV<0.4 焊接性优良一般无需预热；0.4~0.6 需预热；>0.6 焊接性差需较高预热温度。` : dead
- `tools/welding/weld-strength.html` : `A_e = 0.7·h_f·l_w（角焊缝有效截面）` : dead
- `tools/welding/weld-strength.html` : `l_w 应扣除起灭弧缺陷（通常减 2h_f）` : dead
- `tools/welding/weld-strength.html` : `角焊缝危险截面为 45° 喉部，喉厚=0.707a，有效面积=0.707a·L。` : dead
- `tools/welding/weld-strength.html` : `角焊缝承受 F=50 kN，焊脚 a=6 mm，两侧总长 L=200 mm。τ=50000/(0.707×6×200)=58.9 MPa，E43 焊条 [τ]=120–140 MPa，安全。` : dead
- `tools/welding/weld-strength.html` : `角焊缝有效截面积 A_e = 0.7 · h_f · l_w，焊缝应力 τ = F ÷ A_e；F 作用力、h_f 焊脚尺寸、l_w 焊缝计算长度。` : dead
- `tools/welding/weld-strength.html` : `请输入有效参数：F ≥ 0，h_f、l_w、f_fw 均须 > 0。` : dead

  其它成因样例（共 29 条，仅列前 5）：
  - `tools/welding/detector-water-pressure-1.html` : `1.6 倍` : fragment
  - `tools/welding/flow-ratio.html` : `⚠ 喷嘴直径与总流量须大于 0。` : dynamic
  - `tools/welding/flow-ratio.html` : `⚠ Ar、CO₂ 比例须为非负，且两者之和须大于 0。` : dynamic
  - `tools/welding/flow-ratio.html` : `按推荐流量区间判定（TIG 8~15、MIG/MAG 15~20 L/min），流量过低保护不足，过高易产生紊流卷入空气。` : dynamic
  - `tools/welding/hanjiegongyicanshu.html` : `🛠️ 焊接工艺参数` : harmless

### woodwork（dead 5 / dynamic 0 / fragment 0 / harmless 0）

- `tools/woodwork/analysis-cost-price.html` : `Mass（等级/含水率/标准）检测` : dead
- `tools/woodwork/convert-30.html` : `线干缩率 ≈ (初始含水率 − 终了含水率) × 收缩系数` : dead
- `tools/woodwork/desk-dimensions.html` : `Mass（标准/检测/认证）保障` : dead
- `tools/woodwork/detector-32.html` : `稳定性系数 = 抗倾覆力矩/倾覆力矩` : dead
- `tools/woodwork/detector-37.html` : `价格（行情/波动/成本）分析` : dead

## 词典存在但无对应页面的 slug（非死键，单独列出）

- admin/register-depreciation (json=register-depreciation.json)
- design/color-contrast-check (json=color-contrast-check.json)
- fun/word-search (json=word-search.json)
- general/vcard-qr (json=vcard-qr.json)
- network/dns-record-info (json=dns-record-info.json)
- pets/feeding-amount (json=feeding-amount.json)
- pets/grooming-guide (json=grooming-guide.json)
- pets/kennel-space (json=kennel-space.json)
- pets/pet-age-convert (json=pet-age-convert.json)
- pets/vaccine-reminder (json=vaccine-reminder.json)
- security/password-generator-advanced (json=password-generator-advanced.json)
- security/password (json=password.json)

## 口径说明

1. **词典来源**：`i18n/tools/en/<ind>/<slug>.json` 的 `map`，键为简体原文（共 214 个行业目录、4819 对「有页面且有词典」的 slug）。
2. **页面语料**：同名 `tools/<ind>/<slug>.html` 经 HTMLParser 解析，排除 `<script>/<style>/<noscript>` 内容，收集：
   - 可见文本节点（`textContent.trim()` 口径，NBSP/全角空格归一、连续空白折叠）；
   - `placeholder/title/aria-label/alt` 属性值（运行时 `applyEnDict` (c) 分支会翻译）；
   - `data-zh` 属性值（运行时 (a) 分支以它为键）。
3. **判定**：
   - 键与上述任一值归一后**完全相等** → 存活；
   - 以 `：`/`:` 结尾的键，若为某文本节点串首 → 存活（`replaceColonLabelsAll`/`longestPrefixKey` 口径）；
   - 键只是某文本节点的**子串**（原文被内联标签拆分）→ `fragment`；
   - 键出现在 `<script>` 源串但不在渲染文本，或呈数字/结果形态 → `dynamic`；
   - 纯英文键、含 emoji 的短卡片名 → `harmless`；
   - 其余 → `dead`（高优先）。
4. **局限**：静态解析不执行 JS，运行时由 JS 注入且不与脚本源串同形的文本可能被误判为 `dead`；`harmless` 为启发式；不覆盖 `_common.json` 与行业层 `<ind>-body.json`/`<ind>-phrases.json`。建议各线在修复前用 `?lang=en-US` 真机抽查确认。
5. **修复口径提示**：`dead` 先核对页面当前文本（FAQ/深度解析/公式说明是否整体重写），把新原文补进词典并删除旧键；`dynamic` 应把键改为不含变量部分的固定前缀；`fragment` 需按运行时 DOM 空白约定拆键或改造页面结构。

## 附：`slug-en.json` 游离键清理（第一批，2026-11-05）

- 基线：`slug-en` 5515 键 ↔ `json/industry-*.json` 4705 个工具页键，游离 **810**。
- 逐键核实（不按名字猜）：
  - **599** 键在 `tools/<ind>/<slug>.html` 下**无对应页面**（已删除 / 迁移改名后残留）；
  - **211** 键对应 `tools/<ind>/index.html` 分类落地页（页面存在，但 `js/tool-i18n.js:normalizeRelatedKey` 对 `index` 明确 `return null`，这些键永远查不到）；
  - **0** 个 `TOOLBOX-REDIRECT` 存根页（无迁移壳键）。
- 处置：全部删除，`slug-en.json` 5515 → **4705**，与行业工具页一一对应（缺失 0 / 冗余 0）。
- 门禁：`_test_static.py` 清理后 **0 失败 / 0 告警**；英文态真机探针抽检 9 页全部 `残留 0`，另用真机复核 4 页标题/关联卡片名均为英文。
- 保留：无（810 个键全部满足可删判据）。

## 附：第三层词典死键清理（第一批，2026-11-05）

### 试点目录与总量

| 目录 | 键总数 | 存活 | 判定死键（已删） | 保留待核 | 改动文件 |
|---|---|---|---|---|---|
| `ai` | 1634 | 1327 | 270 | 37 | 62 |
| `health` | 2620 | 2547 | 7 | 66 | 5 |
| `finance` | 5150 | 3878 | 33 | 1239 | 13 |
| `design` | 3821 | 3214 | 28 | 579 | 12 |
| `life` | 2731 | 2391 | 209 | 131 | 65 |
| **合计** | **15956** | **13357** | **547** | **2052** | **157** |

### 删前三级核实（缺一不可）

1. **页面源码不存在**：key 归一化（NBSP/全角空格归一、连续空白折叠）后在该页原始 HTML 中不存在；只要在源码任意位置（含 `<script>`、注释、JSON-LD）出现即保留，归入「源码存在」待核。
2. **共享层未复用**：逐 key 比对 `js/tool-i18n-en.js` 的 `GEN_UI_MAP`（960 键）/`BODY_PHRASE_MAP`（10079 键）、`i18n/tools/en/_common.json`、`_prefix.json`、`<ind>-phrases.json`（`<ind>-body.json` 的顶层键是 slug，不是原文，不计）。命中即保留。
3. **运行时探针复核**：用 jsdom 真实执行页面内联脚本 + 真实 `js/i18n.js`/`js/tool-i18n.js`，把第三层 `map` 包成 `Proxy` 记录每次 `pickEn()` 读取，并补样本、点主流程按钮后再收集。**从未被读取的 key 才允许删除**。本批因此把 **148 个**静态判定为 dead、但运行时会读取的 key 全部保留（如 `finance/analysis-5` 的「流动资产 … ÷ 流动负债 …」实时算例、`design/analysis-64` 的「总分差（0.7%）」动态结论、`health/convert-content` 的「日摄入 (mg)」结果标签）。
4. **动态形态保守保留**（避免「修改输入后才会出现的运行时文本」误删）：含数字、以 `：`/`:` 结尾、`第 N 期`/`槽位 N`、长度 ≤8 且不含 FAQ 标记的短标签，一律保留待核，不计入删除。共 **892** 个。

### 删后验证

- 中文残留基线/复测（`node scripts/_en_i18n_probe.mjs --check <industry>`，全量行业页）：

| 目录 | 检查页数 | 基线有残留页 | 删后有残留页 | 残留增加的页 |
|---|---|---|---|---|
| `ai` | 64 | 50 | 50 | 0 |
| `health` | 40 | 31 | 31 | 0 |
| `design` | 108 | 63 | 63 | 0 |
| `finance` | 115 | 44 | 44 | 0 |
| `life` | 70 | 14 | 14 | 0 |

- 逐页比对基线快照，**397 页残留数全部一致，0 页增加**（无新增中文残留）。
- 只改 `i18n/tools/en/{ai,health,finance,design,life}/**` 的 `map`，未跑 `_build.py`、未 push；157 个改动文件 JSON 全部可正常解析，格式按原文件逐个探测（indent=1/2 + 文件末尾换行状态），`git diff` 仅 546 行删除 + 2 行尾逗号调整。
- 另有 2 个文件（`life/ring-size-converter`、`life/bra-size-converter`）原始 JSON 含重复键，无法无损重写，整文件跳过，7 个候选键转入下一批复核。
- 保留待核的 2052 个键：源码内仍存在（1001）、碎片节点（1）、共享层复用（3）、动态/数字/短标签形态（892）、运行时探针命中（148）、重复键文件跳过（7）。后续批次需先补运行时用例或页面改动后再判定，不得仅凭静态扫描删除。

## 附：第三层词典死键清理（第二批，2026-11-05）

### 试点分组与实际键数

| 组 | 目录 | 键总数 | 存活 | 已删 | 保留待核 | 改动文件 |
|---|---|---|---|---|---|---|
| 临床+全科 | `clinical-lab` `clinical-nursing` `medical` `medical2` `psychiatry` | 3782 | 3564 | 19 | 199 | 13 |
| 妇产+儿科+口腔 | `obstetrics` `pediatrics` `dentistry` | 3463 | 3368 | 15 | 80 | 14 |
| 商业/电商 | `biz` `ecommerce` | 3263 | 2838 | 276 | 149 | 74 |
| 教育 | `edu` `edu2` `language` | 2771 | 2636 | 37 | 98 | 12 |
| 土木/结构 | `construction` `civil` `structural` | 2774 | 2691 | 14 | 69 | 10 |
| **合计** | **16 个目录** | **16053** | **15097** | **361** | **595** | **123** |

> `it` 因另一条线有 27 个未提交的第三层词典改动，本批不碰；以同量级的上述 16 个目录替代。

### 核实与结果

- 静态初筛候选 367 个；运行时 Proxy 探针命中 2 个，已保留（`ecommerce/inventory-1` 的动态结果标签等）。
- 动态/数字/短标签形态保留 174 个；源码内仍存在 398 个；碎片节点 6 个；行业层复用 11 个；重复键文件整文件跳过 4 个（`clinical-lab/vaginal-discharge-grading` 的 `白带常规判读` 两处值不同，未无损重写）。
- 最终删除 **361** 个键，123 个文件；`git diff` 仅删除行 + 6 行尾逗号调整，无格式重排。
- 删前/删后探针（124 个受影响页逐页）：基线 96 页有残留，删后 93 页有残留，**0 页增加、12 页减少**。减少页与并发提交（`e9f2c90329` 随机工具改造、`881ca2198d` 量表页重建）同步发生，非删除导致；本批自身对每页残留只减不增。

### 同期独立修复：重复键

`life/ring-size-converter`、`life/bra-size-converter` 的 `map` 各含 2 个重复键：`请输入数据计算`、`港码 = 周长 − 40（…）`；两处值完全相同，去重保留首处、语义不变。已单独提交，`--check life` 70 页残留与基线逐页一致。

## 第三批：`data` + `electrical`（2026-11-05）

> 白名单：仅 `i18n/tools/en/data/**`、`i18n/tools/en/electrical/**`；未跑 `_build.py`、未 push。

### 口径与核实

- **弃用纯静态判死**：源码缺失 ≠ 运行时不用（动态文本可由 JS 拼出）。本批对每个静态候选做**运行时标记法复核**——临时把候选键值改为 `@@MKn@@` 加载 `?lang=en-US`，读 `document.body.textContent` + `input/textarea` 的 `placeholder/value` + `title/aria-label/alt` + `data-zh/data-i18n` 属性；**标记未出现才判死**。
- 候选 37 条（data 19 / electrical 18），其中 **3 条被运行时读取，保留**：`data/xml-html-css-geshihua-yiyou-kebuchong` 的 `如 2（1–8）`、`data/yaml-json` 的 `| 保留换行，> 折叠换行`、`electrical/generator-23` 的 1 条。
- 本批未触碰 `i18n/tools/data-body.json` / `electrical-body.json`（无必要改动）。

### 结果

| 目录 | 词典页 | 键总数（改前） | 删死键 | 补/修半译键 | 键总数（改后） | 探针残留 | 真机剩余（动态） |
|---|---|---|---|---|---|---|---|
| `data` | 22 | 501 | 17 | 17 | 501 | **0 页** | 4 页 / 7 条 |
| `electrical` | 36 | 1172 | 17 | 237 | 1392 | **0 页** | 32 页 / 50 条 |
| 合计 | 58 | 1673 | **34** | **254** | 1893 | **0** | 36 页 / 57 条 |

### 删死键明细（34 条）

| 页面 | 条数 | 内容 |
|---|---|---|
| `data/csv-json` | 3 | 3 条旧 FAQ（页面已删正文，仅余 `<h3>❓ 常见问题（FAQ）</h3>`） |
| `data/csv-to-markdown` | 3 | 同上 |
| `data/generator-35` | 3 | 旧「组距/边界」说明段（已改写为新口径） |
| `data/index` | 5 | 1 条旧介绍 + 4 条旧 FAQ（已改写为「分类下的工具需要下载或注册吗？」等新文案） |
| `data/yaml-json` | 3 | 3 条旧 FAQ |
| `electrical/calc-2` | 1 | `🧮 三相功率计算`（卡片名已改） |
| `electrical/detector-resistance-1` `-aging` `detector-resistance` | 3 | `⚡ 检测…服务`（3 页各 1 条） |
| `electrical/dianhuaxuedunhuakongzhi` | 2 | 旧标题 + 旧公式说明 |
| `electrical/generator-23` | 4 | 旧 intro / deep-dive / 运算符说明 / 占位串 |
| `electrical/index` | 4 | 4 条旧 FAQ（已改写） |
| `electrical/power-factor-compensation` | 1 | `🔌 功率因数补偿` |
| `electrical/voltage-divider` | 1 | `🔌 分压电路计算` |
| `electrical/voltage` | 1 | `🛠️ 电子束焊接参数`（错配卡片名） |

### 半译修复（254 条，键一律照抄运行时 `textContent.trim()`）

- `electrical` 以**公式说明行**（`formula-eq`）+ `placeholder` + 结果区标签（如 `总电压 (V)`、`视在功率 S（kVA）`）为主；`data` 以直方图/统计标签与 `placeholder` 为主。
- **动态数字型不硬拗**：含随输入变化的数值串（如 `总能量 10240 Wh`、`步骤1…`、`0时…` 除外——后者是 24 个固定轴标签，已程序化补键 `0时→0h`）一律不建键，计入「真机剩余」。
- 特例 `electrical/transformer-sizing`：标准容量枚举 `30、50、63…` 是**固定串**，整串成键（译为半角逗号列表），兼顾 IT 线新加的「数字间全角分隔符保留」规则。

### 改前 → 改后（实际渲染）

| 页面 | 改前 | 改后 |
|---|---|---|
| `tools/data/generator-35.html` | `📊 统计摘要` / `如 12,15,16,18,20` | `📊 Summary Statistics` / `e.g. 12,15,16,18,20` |
| `tools/electrical/voltage-divider.html` | `输入电压 Vin (V)` / `R1 (Ω, 上)` | `Input voltage Vin (V)` / `R1 (Ω, top)` |
| `tools/electrical/wire-resistance.html` | `导体电阻 R = 电阻率 ρ × 长度 L ÷ 截面积 A。校验：…` | `Conductor resistance R = resistivity ρ × length L ÷ cross-section A. Validation: …` |

### 剩余（真机 `?lang=en-US`，均为随输入变化的动态值，需页面/运行时改动，不在本批白名单）

| 目录 | 页 | 条 | 样例 |
|---|---|---|---|
| `data` | 4 | 7 | `颜色越深值越大 · 7行 × 24列`、`标签数：10 个`、`Max nesting depth：3 层` |
| `electrical` | 32 | 50 | `总能量 10240 Wh，续航 14.75 小时`、`＝ 51.20 V`、`步骤1` 序列 |

> 另有 5 条键（`electrical/detector-175` 的 `Estimated shaft power:约`、`temp-26` 的 `🛡️ Flameproof type:` / `📦 Recommended device:`、`dianhuaxuedunhuakongzhi` 的 `Potential below passivation threshold，金属持续溶解` 等）在**直接 `?lang=en-US` 首屏**仍显示中文——根因是页面脚本在翻译之后重写同一节点（本批只补了键，切换语言路径已可用；首屏需页面侧或 `tool-i18n.js` 处理，另行立项）。

### 待构建

| 目录 | 文件数 | 说明 |
|---|---|---|
| `i18n/tools/en/data/` | 7 | `csv-json`、`csv-to-markdown`、`data-visualizer`、`generator-35`、`index`、`xml-html-css-geshihua-yiyou-kebuchong`、`yaml-json` |
| `i18n/tools/en/electrical/` | 34 | 见本节「删死键明细」，含 `calc-1`、`calc-2`、`calc-power-voltage`、`current-divider`、`detector-173/175/aging/protection-2/resistance*`、`dianhuaxuedunhuakongzhi`、`generator-23`、`home-load-estimate`、`index`、`led-resistor`、`lizishujianshejisuan`、`load-curve`、`power-7`、`power-factor-compensation`、`power-voltage-1`、`rc-filter`、`rlc-resonance`、`speed-9`、`temp-26`、`transformer-sizing`、`voltage-8/9`、`voltage-divider`、`voltage-drop`、`voltage`、`wire-gauge-selector`、`wire-resistance` |
| `js/tool-i18n.js` | 1 | 共享层（数据上下文标点保护 + 动态补译积压重放），已单独提交 `b1effabac1` |
| **合计** | **42** | 均须 `_build.py` 刷新 SW 版本戳后生效 |

## 今日新增经验（2026-11-05）

### 一、半译键必须先 `--keysrc` 还原源文键

`--check` 输出的是**运行时改写后的残留串**，其中「标签：」片段可能已被全局层（`BODY_PHRASE_MAP` / `replaceColonLabelsAll`）先替换成英文；直接照抄该串建键，键在 `applyEnDict` 执行时已不存在，永远打不中。

- 实例：`usedcar/rater-37` 的 `Rating:≥85 优秀…` 源文实为 `评级：≥85 优秀…`；`usedcar/tester-12` 的 `Charge voltage：…` 源文为 `充电电压：…`；`usedcar/wear` 的 `Deviation <0 时…` 源文为 `偏差 <0 时…`；`finance/points-redemption-value` 的 `（Reference:现金抵扣…` 源文为 `（参考：现金抵扣…`。
- 做法：先跑 `node scripts/_en_i18n_probe.mjs --keysrc <ind>/<slug>`，把输出里 `≠ EN … / ZH: …` 的 ZH 串作为 `map` 键。
- 同类历史坑：`🟢 状态良好：剩余里程充足`、`generic` 占位。

### 二、复查期新出现的正文要按当前 DOM 补译，被他人持有的页标记「待重译」

批量收口期间页面可能被其他线改写（新增深度解析段、FAQ 等），复查时会冒出 `--check` 首轮从未出现的条目。此时按**当前 DOM**补译即可；若该页仍在被别的线改造（如 `tools/finance/salary-after-tax.html` 正被假工具重写线处理），**不要硬译**，登记「待重译」，等对方提交后再补键，避免白译与键漂移。
