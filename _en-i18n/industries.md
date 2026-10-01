# 待处理行业清单（EN 内容英文化专项）

> 唯一权威进度源。**每完成一个行业即删除该行**，行数归零即全站完成。
> 初始状态：全部 208 个行业待处理（含工具页的行业，`tools/*/` 共 209 个目录中 208 个有工具页）。
> 排序：按工具页数降序（规模大、影响面大者优先）；同规模按字母序。
> 维护规则：只由 `scripts/_en_i18n_probe.mjs --promote <industry>` 删除行；禁止手工调序。

## 基线（2026-09-28 实测）

| 指标 | 数值 |
|---|---|
| 待处理行业 | 208 |
| 工具页 | 4779 |
| 可见中文文本节点 | 293874 |
| 行业内唯一文本（含跨行业重复） | 166398 |

## 清单

| # | industry | 工具页 | 中文节点 | 唯一文本 | 状态 |
|---:|---|---:|---:|---:|---|
| 1 | `fitness` | 36 | 2186 | 1243 | pending |
| 2 | `math` | 36 | 1339 | 860 | pending |
| 3 | `accounting` | 35 | 1222 | 792 | pending |
| 4 | `healthcare` | 35 | 1317 | 843 | pending |
| 5 | `securities` | 35 | 1319 | 914 | pending |
| 6 | `cosmetic-derm` | 33 | 2832 | 1632 | pending |
| 7 | `insurance` | 33 | 1092 | 727 | pending |
| 8 | `ophthalmology` | 32 | 2371 | 1278 | pending |
| 9 | `photo` | 32 | 1459 | 744 | pending |
| 10 | `materials` | 31 | 1143 | 742 | pending |
| 11 | `encode` | 30 | 1235 | 722 | pending |
| 12 | `tax` | 29 | 1007 | 707 | pending |
| 13 | `acoustics` | 28 | 832 | 543 | pending |
| 14 | `geometry` | 28 | 915 | 568 | pending |
| 15 | `metrology` | 28 | 836 | 534 | pending |
| 16 | `nuclear` | 28 | 923 | 579 | pending |
| 17 | `robotics` | 28 | 816 | 565 | pending |
| 18 | `chemistry` | 27 | 939 | 654 | pending |
| 19 | `economics` | 27 | 838 | 564 | pending |
| 20 | `food-testing` | 27 | 1873 | 979 | pending |
| 21 | `hematology` | 27 | 2189 | 1253 | pending |
| 22 | `obstetrics` | 27 | 2395 | 1478 | pending |
| 23 | `quantum` | 27 | 839 | 550 | pending |
| 24 | `signal` | 27 | 786 | 541 | pending |
| 25 | `thermodynamics` | 27 | 867 | 576 | pending |
| 26 | `electromagnetism` | 26 | 850 | 588 | pending |
| 27 | `livestock` | 26 | 1993 | 1025 | pending |
| 28 | `reproductive-medicine` | 26 | 2501 | 1254 | pending |
| 29 | `structural` | 26 | 762 | 513 | pending |
| 30 | `banking` | 25 | 728 | 488 | pending |
| 31 | `clinical-lab` | 25 | 1540 | 937 | pending |
| 32 | `clinical-nursing` | 25 | 1906 | 1220 | pending |
| 33 | `construction` | 25 | 1970 | 1231 | pending |
| 34 | `dentistry` | 25 | 1859 | 1120 | pending |
| 35 | `kinematics` | 25 | 809 | 502 | pending |
| 36 | `neurology` | 25 | 2674 | 1537 | pending |
| 37 | `rheumatology` | 25 | 2514 | 1447 | pending |
| 38 | `textile` | 25 | 1994 | 1100 | pending |
| 39 | `cardiology` | 24 | 1917 | 1181 | pending |
| 40 | `food` | 24 | 1772 | 927 | pending |
| 41 | `pediatrics` | 24 | 1865 | 999 | pending |
| 42 | `psychiatry` | 24 | 1565 | 722 | pending |
| 43 | `pulmonology` | 24 | 1832 | 1036 | pending |
| 44 | `urology` | 24 | 2148 | 1138 | pending |
| 45 | `acupuncture` | 23 | 1406 | 656 | pending |
| 46 | `astronomy` | 23 | 1340 | 867 | pending |
| 47 | `dynamics` | 23 | 715 | 464 | pending |
| 48 | `ecommerce` | 23 | 1412 | 661 | pending |
| 49 | `ent` | 23 | 1911 | 1044 | pending |
| 50 | `fluid` | 23 | 670 | 414 | pending |
| 51 | `investment` | 23 | 725 | 507 | pending |
| 52 | `nephrology` | 23 | 1853 | 1034 | pending |
| 53 | `dermatology` | 22 | 2081 | 1077 | pending |
| 54 | `gastroenterology` | 22 | 2114 | 1216 | pending |
| 55 | `rehabilitation` | 22 | 1930 | 1054 | pending |
| 56 | `tcm-chemistry` | 22 | 1690 | 955 | pending |
| 57 | `tcm-pharmacy` | 22 | 1542 | 884 | pending |
| 58 | `beauty` | 21 | 1438 | 852 | pending |
| 59 | `civil` | 21 | 741 | 547 | pending |
| 60 | `electronics` | 21 | 1327 | 723 | pending |
| 61 | `endocrinology` | 21 | 2016 | 1404 | pending |
| 62 | `food-processing` | 21 | 1230 | 518 | pending |
| 63 | `hr` | 21 | 1087 | 564 | pending |
| 64 | `optics` | 21 | 645 | 443 | pending |
| 65 | `property` | 21 | 1344 | 732 | pending |
| 66 | `tcm-diagnosis` | 21 | 2103 | 1170 | pending |
| 67 | `travel` | 21 | 1654 | 918 | pending |
| 68 | `forensic-medicine` | 20 | 2374 | 1597 | pending |
| 69 | `metallurgy` | 20 | 1236 | 646 | pending |
| 70 | `psychology` | 20 | 1057 | 622 | pending |
| 71 | `electrical` | 19 | 810 | 545 | pending |
| 72 | `forestry` | 19 | 1435 | 727 | pending |
| 73 | `language` | 19 | 1123 | 622 | pending |
| 74 | `music` | 19 | 1577 | 893 | pending |
| 75 | `nutrition` | 18 | 980 | 546 | pending |
| 76 | `data` | 17 | 906 | 405 | pending |
| 77 | `advertising` | 16 | 1007 | 520 | pending |
| 78 | `niche` | 16 | 1101 | 690 | pending |
| 79 | `leather` | 15 | 948 | 510 | pending |
| 80 | `logistics` | 15 | 807 | 478 | pending |
| 81 | `safety` | 15 | 838 | 503 | pending |
| 82 | `transport` | 15 | 682 | 495 | pending |
| 83 | `welding` | 15 | 1025 | 546 | pending |
| 84 | `engineering` | 14 | 495 | 324 | pending |
| 85 | `image` | 14 | 882 | 609 | pending |
| 86 | `mechanical` | 14 | 644 | 398 | pending |
| 87 | `medical` | 14 | 936 | 604 | pending |
| 88 | `dyeing` | 13 | 868 | 467 | pending |
| 89 | `gardening` | 12 | 866 | 455 | pending |
| 90 | `mining` | 12 | 768 | 468 | pending |
| 91 | `paper` | 12 | 778 | 399 | pending |
| 92 | `pr` | 12 | 900 | 530 | pending |
| 93 | `chemical` | 11 | 654 | 355 | pending |
| 94 | `elderly` | 11 | 691 | 469 | pending |
| 95 | `fire` | 11 | 774 | 461 | pending |
| 96 | `gas` | 11 | 718 | 380 | pending |
| 97 | `text` | 11 | 467 | 301 | pending |
| 98 | `usedcar` | 11 | 641 | 408 | pending |
| 99 | `hvac` | 10 | 908 | 668 | pending |
| 100 | `pet` | 10 | 657 | 446 | pending |
| 101 | `process` | 10 | 315 | 217 | pending |
| 102 | `security` | 10 | 755 | 532 | pending |
| 103 | `baking` | 9 | 532 | 363 | pending |
| 104 | `misc` | 9 | 609 | 337 | pending |
| 105 | `misc2` | 9 | 616 | 392 | pending |
| 106 | `procurement` | 9 | 563 | 332 | pending |
| 107 | `sales` | 9 | 629 | 362 | pending |
| 108 | `admin` | 8 | 539 | 321 | pending |
| 109 | `cleaning` | 8 | 551 | 382 | pending |
| 110 | `cognition` | 8 | 599 | 422 | pending |
| 111 | `decor` | 8 | 629 | 415 | pending |
| 112 | `library` | 8 | 442 | 247 | pending |
| 113 | `museum` | 8 | 496 | 267 | pending |
| 114 | `quality` | 8 | 507 | 321 | pending |
| 115 | `rental` | 8 | 464 | 281 | pending |
| 116 | `research` | 8 | 527 | 306 | pending |
| 117 | `restaurant` | 8 | 488 | 266 | pending |
| 118 | `telecom` | 8 | 476 | 290 | pending |
| 119 | `audio` | 7 | 512 | 378 | pending |
| 120 | `dance` | 7 | 560 | 377 | pending |
| 121 | `hotel` | 7 | 531 | 329 | pending |
| 122 | `printing` | 7 | 491 | 312 | pending |
| 123 | `woodwork` | 7 | 399 | 292 | pending |
| 124 | `archaeology` | 6 | 360 | 202 | pending |
| 125 | `chinese-cook` | 6 | 471 | 293 | pending |
| 126 | `exhibition` | 6 | 424 | 242 | pending |
| 127 | `film` | 6 | 360 | 236 | pending |
| 128 | `floral` | 6 | 472 | 352 | pending |
| 129 | `funeral` | 6 | 464 | 335 | pending |
| 130 | `home` | 6 | 350 | 211 | pending |
| 131 | `jewelry` | 6 | 430 | 273 | pending |
| 132 | `media` | 6 | 344 | 169 | pending |
| 133 | `office` | 6 | 341 | 264 | pending |
| 134 | `packaging` | 6 | 301 | 171 | pending |
| 135 | `parenting` | 6 | 270 | 164 | pending |
| 136 | `road` | 6 | 460 | 292 | pending |
| 137 | `startup` | 6 | 469 | 309 | pending |
| 138 | `urban` | 6 | 499 | 316 | pending |
| 139 | `video` | 6 | 486 | 311 | pending |
| 140 | `accessibility` | 5 | 347 | 210 | pending |
| 141 | `antiques` | 5 | 345 | 201 | pending |
| 142 | `aquaculture` | 5 | 299 | 189 | pending |
| 143 | `audit` | 5 | 359 | 214 | pending |
| 144 | `bonding` | 5 | 294 | 181 | pending |
| 145 | `bridge` | 5 | 393 | 246 | pending |
| 146 | `ceramics` | 5 | 387 | 247 | pending |
| 147 | `chess` | 5 | 427 | 320 | pending |
| 148 | `chinese` | 5 | 238 | 188 | pending |
| 149 | `edu2` | 5 | 292 | 189 | pending |
| 150 | `fengshui` | 5 | 408 | 300 | pending |
| 151 | `forex` | 5 | 416 | 250 | pending |
| 152 | `futures` | 5 | 411 | 254 | pending |
| 153 | `gardening2` | 5 | 365 | 263 | pending |
| 154 | `glass` | 5 | 364 | 204 | pending |
| 155 | `kids` | 5 | 334 | 198 | pending |
| 156 | `legal2` | 5 | 332 | 200 | pending |
| 157 | `logistics2` | 5 | 319 | 189 | pending |
| 158 | `manufacturing` | 5 | 279 | 154 | pending |
| 159 | `maritime` | 5 | 424 | 282 | pending |
| 160 | `martial` | 5 | 362 | 255 | pending |
| 161 | `medical2` | 5 | 333 | 206 | pending |
| 162 | `pet-training` | 5 | 364 | 263 | pending |
| 163 | `petrochem` | 5 | 355 | 230 | pending |
| 164 | `pets` | 5 | 333 | 229 | pending |
| 165 | `plastic` | 5 | 312 | 175 | pending |
| 166 | `project` | 5 | 403 | 194 | pending |
| 167 | `railway` | 5 | 124 | 80 | pending |
| 168 | `rubber` | 5 | 311 | 174 | pending |
| 169 | `seismology` | 5 | 306 | 195 | pending |
| 170 | `service` | 5 | 306 | 164 | pending |
| 171 | `shipping` | 5 | 311 | 202 | pending |
| 172 | `stage` | 5 | 324 | 186 | pending |
| 173 | `tunnel` | 5 | 373 | 221 | pending |
| 174 | `woodworking` | 5 | 413 | 297 | pending |
| 175 | `yi` | 5 | 370 | 242 | pending |
| 176 | `photo2` | 4 | 236 | 159 | pending |
| 177 | `stats` | 4 | 281 | 198 | pending |

