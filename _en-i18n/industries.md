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
| 1 | `fishery` | 38 | 2623 | 1239 | pending |
| 2 | `aerospace` | 37 | 1506 | 929 | pending |
| 3 | `geology` | 37 | 2415 | 1213 | pending |
| 4 | `machinery` | 37 | 2185 | 1310 | pending |
| 5 | `fitness` | 36 | 2186 | 1243 | pending |
| 6 | `math` | 36 | 1339 | 860 | pending |
| 7 | `accounting` | 35 | 1222 | 792 | pending |
| 8 | `healthcare` | 35 | 1317 | 843 | pending |
| 9 | `securities` | 35 | 1319 | 914 | pending |
| 10 | `cosmetic-derm` | 33 | 2832 | 1632 | pending |
| 11 | `insurance` | 33 | 1092 | 727 | pending |
| 12 | `ophthalmology` | 32 | 2371 | 1278 | pending |
| 13 | `photo` | 32 | 1459 | 744 | pending |
| 14 | `materials` | 31 | 1143 | 742 | pending |
| 15 | `encode` | 30 | 1235 | 722 | pending |
| 16 | `tax` | 29 | 1007 | 707 | pending |
| 17 | `acoustics` | 28 | 832 | 543 | pending |
| 18 | `geometry` | 28 | 915 | 568 | pending |
| 19 | `metrology` | 28 | 836 | 534 | pending |
| 20 | `nuclear` | 28 | 923 | 579 | pending |
| 21 | `robotics` | 28 | 816 | 565 | pending |
| 22 | `chemistry` | 27 | 939 | 654 | pending |
| 23 | `economics` | 27 | 838 | 564 | pending |
| 24 | `food-testing` | 27 | 1873 | 979 | pending |
| 25 | `hematology` | 27 | 2189 | 1253 | pending |
| 26 | `obstetrics` | 27 | 2395 | 1478 | pending |
| 27 | `quantum` | 27 | 839 | 550 | pending |
| 28 | `signal` | 27 | 786 | 541 | pending |
| 29 | `thermodynamics` | 27 | 867 | 576 | pending |
| 30 | `electromagnetism` | 26 | 850 | 588 | pending |
| 31 | `livestock` | 26 | 1993 | 1025 | pending |
| 32 | `reproductive-medicine` | 26 | 2501 | 1254 | pending |
| 33 | `structural` | 26 | 762 | 513 | pending |
| 34 | `banking` | 25 | 728 | 488 | pending |
| 35 | `clinical-lab` | 25 | 1540 | 937 | pending |
| 36 | `clinical-nursing` | 25 | 1906 | 1220 | pending |
| 37 | `construction` | 25 | 1970 | 1231 | pending |
| 38 | `dentistry` | 25 | 1859 | 1120 | pending |
| 39 | `kinematics` | 25 | 809 | 502 | pending |
| 40 | `neurology` | 25 | 2674 | 1537 | pending |
| 41 | `rheumatology` | 25 | 2514 | 1447 | pending |
| 42 | `textile` | 25 | 1994 | 1100 | pending |
| 43 | `cardiology` | 24 | 1917 | 1181 | pending |
| 44 | `food` | 24 | 1772 | 927 | pending |
| 45 | `pediatrics` | 24 | 1865 | 999 | pending |
| 46 | `psychiatry` | 24 | 1565 | 722 | pending |
| 47 | `pulmonology` | 24 | 1832 | 1036 | pending |
| 48 | `urology` | 24 | 2148 | 1138 | pending |
| 49 | `acupuncture` | 23 | 1406 | 656 | pending |
| 50 | `astronomy` | 23 | 1340 | 867 | pending |
| 51 | `dynamics` | 23 | 715 | 464 | pending |
| 52 | `ecommerce` | 23 | 1412 | 661 | pending |
| 53 | `ent` | 23 | 1911 | 1044 | pending |
| 54 | `fluid` | 23 | 670 | 414 | pending |
| 55 | `investment` | 23 | 725 | 507 | pending |
| 56 | `nephrology` | 23 | 1853 | 1034 | pending |
| 57 | `dermatology` | 22 | 2081 | 1077 | pending |
| 58 | `gastroenterology` | 22 | 2114 | 1216 | pending |
| 59 | `rehabilitation` | 22 | 1930 | 1054 | pending |
| 60 | `tcm-chemistry` | 22 | 1690 | 955 | pending |
| 61 | `tcm-pharmacy` | 22 | 1542 | 884 | pending |
| 62 | `beauty` | 21 | 1438 | 852 | pending |
| 63 | `civil` | 21 | 741 | 547 | pending |
| 64 | `electronics` | 21 | 1327 | 723 | pending |
| 65 | `endocrinology` | 21 | 2016 | 1404 | pending |
| 66 | `food-processing` | 21 | 1230 | 518 | pending |
| 67 | `hr` | 21 | 1087 | 564 | pending |
| 68 | `optics` | 21 | 645 | 443 | pending |
| 69 | `property` | 21 | 1344 | 732 | pending |
| 70 | `tcm-diagnosis` | 21 | 2103 | 1170 | pending |
| 71 | `travel` | 21 | 1654 | 918 | pending |
| 72 | `forensic-medicine` | 20 | 2374 | 1597 | pending |
| 73 | `metallurgy` | 20 | 1236 | 646 | pending |
| 74 | `psychology` | 20 | 1057 | 622 | pending |
| 75 | `electrical` | 19 | 810 | 545 | pending |
| 76 | `forestry` | 19 | 1435 | 727 | pending |
| 77 | `language` | 19 | 1123 | 622 | pending |
| 78 | `music` | 19 | 1577 | 893 | pending |
| 79 | `nutrition` | 18 | 980 | 546 | pending |
| 80 | `data` | 17 | 906 | 405 | pending |
| 81 | `advertising` | 16 | 1007 | 520 | pending |
| 82 | `niche` | 16 | 1101 | 690 | pending |
| 83 | `leather` | 15 | 948 | 510 | pending |
| 84 | `logistics` | 15 | 807 | 478 | pending |
| 85 | `safety` | 15 | 838 | 503 | pending |
| 86 | `transport` | 15 | 682 | 495 | pending |
| 87 | `welding` | 15 | 1025 | 546 | pending |
| 88 | `engineering` | 14 | 495 | 324 | pending |
| 89 | `image` | 14 | 882 | 609 | pending |
| 90 | `mechanical` | 14 | 644 | 398 | pending |
| 91 | `medical` | 14 | 936 | 604 | pending |
| 92 | `dyeing` | 13 | 868 | 467 | pending |
| 93 | `gardening` | 12 | 866 | 455 | pending |
| 94 | `mining` | 12 | 768 | 468 | pending |
| 95 | `paper` | 12 | 778 | 399 | pending |
| 96 | `pr` | 12 | 900 | 530 | pending |
| 97 | `chemical` | 11 | 654 | 355 | pending |
| 98 | `elderly` | 11 | 691 | 469 | pending |
| 99 | `fire` | 11 | 774 | 461 | pending |
| 100 | `gas` | 11 | 718 | 380 | pending |
| 101 | `text` | 11 | 467 | 301 | pending |
| 102 | `usedcar` | 11 | 641 | 408 | pending |
| 103 | `hvac` | 10 | 908 | 668 | pending |
| 104 | `pet` | 10 | 657 | 446 | pending |
| 105 | `process` | 10 | 315 | 217 | pending |
| 106 | `security` | 10 | 755 | 532 | pending |
| 107 | `baking` | 9 | 532 | 363 | pending |
| 108 | `misc` | 9 | 609 | 337 | pending |
| 109 | `misc2` | 9 | 616 | 392 | pending |
| 110 | `procurement` | 9 | 563 | 332 | pending |
| 111 | `sales` | 9 | 629 | 362 | pending |
| 112 | `admin` | 8 | 539 | 321 | pending |
| 113 | `cleaning` | 8 | 551 | 382 | pending |
| 114 | `cognition` | 8 | 599 | 422 | pending |
| 115 | `decor` | 8 | 629 | 415 | pending |
| 116 | `library` | 8 | 442 | 247 | pending |
| 117 | `museum` | 8 | 496 | 267 | pending |
| 118 | `quality` | 8 | 507 | 321 | pending |
| 119 | `rental` | 8 | 464 | 281 | pending |
| 120 | `research` | 8 | 527 | 306 | pending |
| 121 | `restaurant` | 8 | 488 | 266 | pending |
| 122 | `telecom` | 8 | 476 | 290 | pending |
| 123 | `audio` | 7 | 512 | 378 | pending |
| 124 | `dance` | 7 | 560 | 377 | pending |
| 125 | `hotel` | 7 | 531 | 329 | pending |
| 126 | `printing` | 7 | 491 | 312 | pending |
| 127 | `woodwork` | 7 | 399 | 292 | pending |
| 128 | `archaeology` | 6 | 360 | 202 | pending |
| 129 | `chinese-cook` | 6 | 471 | 293 | pending |
| 130 | `exhibition` | 6 | 424 | 242 | pending |
| 131 | `film` | 6 | 360 | 236 | pending |
| 132 | `floral` | 6 | 472 | 352 | pending |
| 133 | `funeral` | 6 | 464 | 335 | pending |
| 134 | `home` | 6 | 350 | 211 | pending |
| 135 | `jewelry` | 6 | 430 | 273 | pending |
| 136 | `media` | 6 | 344 | 169 | pending |
| 137 | `office` | 6 | 341 | 264 | pending |
| 138 | `packaging` | 6 | 301 | 171 | pending |
| 139 | `parenting` | 6 | 270 | 164 | pending |
| 140 | `road` | 6 | 460 | 292 | pending |
| 141 | `startup` | 6 | 469 | 309 | pending |
| 142 | `urban` | 6 | 499 | 316 | pending |
| 143 | `video` | 6 | 486 | 311 | pending |
| 144 | `accessibility` | 5 | 347 | 210 | pending |
| 145 | `antiques` | 5 | 345 | 201 | pending |
| 146 | `aquaculture` | 5 | 299 | 189 | pending |
| 147 | `audit` | 5 | 359 | 214 | pending |
| 148 | `bonding` | 5 | 294 | 181 | pending |
| 149 | `bridge` | 5 | 393 | 246 | pending |
| 150 | `ceramics` | 5 | 387 | 247 | pending |
| 151 | `chess` | 5 | 427 | 320 | pending |
| 152 | `chinese` | 5 | 238 | 188 | pending |
| 153 | `edu2` | 5 | 292 | 189 | pending |
| 154 | `fengshui` | 5 | 408 | 300 | pending |
| 155 | `forex` | 5 | 416 | 250 | pending |
| 156 | `futures` | 5 | 411 | 254 | pending |
| 157 | `gardening2` | 5 | 365 | 263 | pending |
| 158 | `glass` | 5 | 364 | 204 | pending |
| 159 | `kids` | 5 | 334 | 198 | pending |
| 160 | `legal2` | 5 | 332 | 200 | pending |
| 161 | `logistics2` | 5 | 319 | 189 | pending |
| 162 | `manufacturing` | 5 | 279 | 154 | pending |
| 163 | `maritime` | 5 | 424 | 282 | pending |
| 164 | `martial` | 5 | 362 | 255 | pending |
| 165 | `medical2` | 5 | 333 | 206 | pending |
| 166 | `pet-training` | 5 | 364 | 263 | pending |
| 167 | `petrochem` | 5 | 355 | 230 | pending |
| 168 | `pets` | 5 | 333 | 229 | pending |
| 169 | `plastic` | 5 | 312 | 175 | pending |
| 170 | `project` | 5 | 403 | 194 | pending |
| 171 | `railway` | 5 | 124 | 80 | pending |
| 172 | `rubber` | 5 | 311 | 174 | pending |
| 173 | `seismology` | 5 | 306 | 195 | pending |
| 174 | `service` | 5 | 306 | 164 | pending |
| 175 | `shipping` | 5 | 311 | 202 | pending |
| 176 | `stage` | 5 | 324 | 186 | pending |
| 177 | `tunnel` | 5 | 373 | 221 | pending |
| 178 | `woodworking` | 5 | 413 | 297 | pending |
| 179 | `yi` | 5 | 370 | 242 | pending |
| 180 | `photo2` | 4 | 236 | 159 | pending |
| 181 | `stats` | 4 | 281 | 198 | pending |

