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

