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
| 1 | `optical` | 40 | 2602 | 1543 | pending |
| 2 | `energy` | 39 | 1967 | 1127 | pending |
| 3 | `fire-rescue` | 39 | 2605 | 1614 | pending |
| 4 | `eco` | 38 | 1860 | 983 | pending |
| 5 | `fishery` | 38 | 2623 | 1239 | pending |
| 6 | `aerospace` | 37 | 1506 | 929 | pending |
| 7 | `geology` | 37 | 2415 | 1213 | pending |
| 8 | `machinery` | 37 | 2185 | 1310 | pending |
| 9 | `fitness` | 36 | 2186 | 1243 | pending |
| 10 | `math` | 36 | 1339 | 860 | pending |
| 11 | `accounting` | 35 | 1222 | 792 | pending |
| 12 | `healthcare` | 35 | 1317 | 843 | pending |
| 13 | `securities` | 35 | 1319 | 914 | pending |
| 14 | `cosmetic-derm` | 33 | 2832 | 1632 | pending |
| 15 | `insurance` | 33 | 1092 | 727 | pending |
| 16 | `ophthalmology` | 32 | 2371 | 1278 | pending |
| 17 | `photo` | 32 | 1459 | 744 | pending |
| 18 | `materials` | 31 | 1143 | 742 | pending |
| 19 | `encode` | 30 | 1235 | 722 | pending |
| 20 | `tax` | 29 | 1007 | 707 | pending |
| 21 | `acoustics` | 28 | 832 | 543 | pending |
| 22 | `geometry` | 28 | 915 | 568 | pending |
| 23 | `metrology` | 28 | 836 | 534 | pending |
| 24 | `nuclear` | 28 | 923 | 579 | pending |
| 25 | `robotics` | 28 | 816 | 565 | pending |
| 26 | `chemistry` | 27 | 939 | 654 | pending |
| 27 | `economics` | 27 | 838 | 564 | pending |
| 28 | `food-testing` | 27 | 1873 | 979 | pending |
| 29 | `hematology` | 27 | 2189 | 1253 | pending |
| 30 | `obstetrics` | 27 | 2395 | 1478 | pending |
| 31 | `quantum` | 27 | 839 | 550 | pending |
| 32 | `signal` | 27 | 786 | 541 | pending |
| 33 | `thermodynamics` | 27 | 867 | 576 | pending |
| 34 | `electromagnetism` | 26 | 850 | 588 | pending |
| 35 | `livestock` | 26 | 1993 | 1025 | pending |
| 36 | `reproductive-medicine` | 26 | 2501 | 1254 | pending |
| 37 | `structural` | 26 | 762 | 513 | pending |
| 38 | `banking` | 25 | 728 | 488 | pending |
| 39 | `clinical-lab` | 25 | 1540 | 937 | pending |
| 40 | `clinical-nursing` | 25 | 1906 | 1220 | pending |
| 41 | `construction` | 25 | 1970 | 1231 | pending |
| 42 | `dentistry` | 25 | 1859 | 1120 | pending |
| 43 | `kinematics` | 25 | 809 | 502 | pending |
| 44 | `neurology` | 25 | 2674 | 1537 | pending |
| 45 | `rheumatology` | 25 | 2514 | 1447 | pending |
| 46 | `textile` | 25 | 1994 | 1100 | pending |
| 47 | `cardiology` | 24 | 1917 | 1181 | pending |
| 48 | `food` | 24 | 1772 | 927 | pending |
| 49 | `pediatrics` | 24 | 1865 | 999 | pending |
| 50 | `psychiatry` | 24 | 1565 | 722 | pending |
| 51 | `pulmonology` | 24 | 1832 | 1036 | pending |
| 52 | `urology` | 24 | 2148 | 1138 | pending |
| 53 | `acupuncture` | 23 | 1406 | 656 | pending |
| 54 | `astronomy` | 23 | 1340 | 867 | pending |
| 55 | `dynamics` | 23 | 715 | 464 | pending |
| 56 | `ecommerce` | 23 | 1412 | 661 | pending |
| 57 | `ent` | 23 | 1911 | 1044 | pending |
| 58 | `fluid` | 23 | 670 | 414 | pending |
| 59 | `investment` | 23 | 725 | 507 | pending |
| 60 | `nephrology` | 23 | 1853 | 1034 | pending |
| 61 | `dermatology` | 22 | 2081 | 1077 | pending |
| 62 | `gastroenterology` | 22 | 2114 | 1216 | pending |
| 63 | `rehabilitation` | 22 | 1930 | 1054 | pending |
| 64 | `tcm-chemistry` | 22 | 1690 | 955 | pending |
| 65 | `tcm-pharmacy` | 22 | 1542 | 884 | pending |
| 66 | `beauty` | 21 | 1438 | 852 | pending |
| 67 | `civil` | 21 | 741 | 547 | pending |
| 68 | `electronics` | 21 | 1327 | 723 | pending |
| 69 | `endocrinology` | 21 | 2016 | 1404 | pending |
| 70 | `food-processing` | 21 | 1230 | 518 | pending |
| 71 | `hr` | 21 | 1087 | 564 | pending |
| 72 | `optics` | 21 | 645 | 443 | pending |
| 73 | `property` | 21 | 1344 | 732 | pending |
| 74 | `tcm-diagnosis` | 21 | 2103 | 1170 | pending |
| 75 | `travel` | 21 | 1654 | 918 | pending |
| 76 | `forensic-medicine` | 20 | 2374 | 1597 | pending |
| 77 | `metallurgy` | 20 | 1236 | 646 | pending |
| 78 | `psychology` | 20 | 1057 | 622 | pending |
| 79 | `electrical` | 19 | 810 | 545 | pending |
| 80 | `forestry` | 19 | 1435 | 727 | pending |
| 81 | `language` | 19 | 1123 | 622 | pending |
| 82 | `music` | 19 | 1577 | 893 | pending |
| 83 | `nutrition` | 18 | 980 | 546 | pending |
| 84 | `data` | 17 | 906 | 405 | pending |
| 85 | `advertising` | 16 | 1007 | 520 | pending |
| 86 | `niche` | 16 | 1101 | 690 | pending |
| 87 | `leather` | 15 | 948 | 510 | pending |
| 88 | `logistics` | 15 | 807 | 478 | pending |
| 89 | `safety` | 15 | 838 | 503 | pending |
| 90 | `transport` | 15 | 682 | 495 | pending |
| 91 | `welding` | 15 | 1025 | 546 | pending |
| 92 | `engineering` | 14 | 495 | 324 | pending |
| 93 | `image` | 14 | 882 | 609 | pending |
| 94 | `mechanical` | 14 | 644 | 398 | pending |
| 95 | `medical` | 14 | 936 | 604 | pending |
| 96 | `dyeing` | 13 | 868 | 467 | pending |
| 97 | `gardening` | 12 | 866 | 455 | pending |
| 98 | `mining` | 12 | 768 | 468 | pending |
| 99 | `paper` | 12 | 778 | 399 | pending |
| 100 | `pr` | 12 | 900 | 530 | pending |
| 101 | `chemical` | 11 | 654 | 355 | pending |
| 102 | `elderly` | 11 | 691 | 469 | pending |
| 103 | `fire` | 11 | 774 | 461 | pending |
| 104 | `gas` | 11 | 718 | 380 | pending |
| 105 | `text` | 11 | 467 | 301 | pending |
| 106 | `usedcar` | 11 | 641 | 408 | pending |
| 107 | `hvac` | 10 | 908 | 668 | pending |
| 108 | `pet` | 10 | 657 | 446 | pending |
| 109 | `process` | 10 | 315 | 217 | pending |
| 110 | `security` | 10 | 755 | 532 | pending |
| 111 | `baking` | 9 | 532 | 363 | pending |
| 112 | `misc` | 9 | 609 | 337 | pending |
| 113 | `misc2` | 9 | 616 | 392 | pending |
| 114 | `procurement` | 9 | 563 | 332 | pending |
| 115 | `sales` | 9 | 629 | 362 | pending |
| 116 | `admin` | 8 | 539 | 321 | pending |
| 117 | `cleaning` | 8 | 551 | 382 | pending |
| 118 | `cognition` | 8 | 599 | 422 | pending |
| 119 | `decor` | 8 | 629 | 415 | pending |
| 120 | `library` | 8 | 442 | 247 | pending |
| 121 | `museum` | 8 | 496 | 267 | pending |
| 122 | `quality` | 8 | 507 | 321 | pending |
| 123 | `rental` | 8 | 464 | 281 | pending |
| 124 | `research` | 8 | 527 | 306 | pending |
| 125 | `restaurant` | 8 | 488 | 266 | pending |
| 126 | `telecom` | 8 | 476 | 290 | pending |
| 127 | `audio` | 7 | 512 | 378 | pending |
| 128 | `dance` | 7 | 560 | 377 | pending |
| 129 | `hotel` | 7 | 531 | 329 | pending |
| 130 | `printing` | 7 | 491 | 312 | pending |
| 131 | `woodwork` | 7 | 399 | 292 | pending |
| 132 | `archaeology` | 6 | 360 | 202 | pending |
| 133 | `chinese-cook` | 6 | 471 | 293 | pending |
| 134 | `exhibition` | 6 | 424 | 242 | pending |
| 135 | `film` | 6 | 360 | 236 | pending |
| 136 | `floral` | 6 | 472 | 352 | pending |
| 137 | `funeral` | 6 | 464 | 335 | pending |
| 138 | `home` | 6 | 350 | 211 | pending |
| 139 | `jewelry` | 6 | 430 | 273 | pending |
| 140 | `media` | 6 | 344 | 169 | pending |
| 141 | `office` | 6 | 341 | 264 | pending |
| 142 | `packaging` | 6 | 301 | 171 | pending |
| 143 | `parenting` | 6 | 270 | 164 | pending |
| 144 | `road` | 6 | 460 | 292 | pending |
| 145 | `startup` | 6 | 469 | 309 | pending |
| 146 | `urban` | 6 | 499 | 316 | pending |
| 147 | `video` | 6 | 486 | 311 | pending |
| 148 | `accessibility` | 5 | 347 | 210 | pending |
| 149 | `antiques` | 5 | 345 | 201 | pending |
| 150 | `aquaculture` | 5 | 299 | 189 | pending |
| 151 | `audit` | 5 | 359 | 214 | pending |
| 152 | `bonding` | 5 | 294 | 181 | pending |
| 153 | `bridge` | 5 | 393 | 246 | pending |
| 154 | `ceramics` | 5 | 387 | 247 | pending |
| 155 | `chess` | 5 | 427 | 320 | pending |
| 156 | `chinese` | 5 | 238 | 188 | pending |
| 157 | `edu2` | 5 | 292 | 189 | pending |
| 158 | `fengshui` | 5 | 408 | 300 | pending |
| 159 | `forex` | 5 | 416 | 250 | pending |
| 160 | `futures` | 5 | 411 | 254 | pending |
| 161 | `gardening2` | 5 | 365 | 263 | pending |
| 162 | `glass` | 5 | 364 | 204 | pending |
| 163 | `kids` | 5 | 334 | 198 | pending |
| 164 | `legal2` | 5 | 332 | 200 | pending |
| 165 | `logistics2` | 5 | 319 | 189 | pending |
| 166 | `manufacturing` | 5 | 279 | 154 | pending |
| 167 | `maritime` | 5 | 424 | 282 | pending |
| 168 | `martial` | 5 | 362 | 255 | pending |
| 169 | `medical2` | 5 | 333 | 206 | pending |
| 170 | `pet-training` | 5 | 364 | 263 | pending |
| 171 | `petrochem` | 5 | 355 | 230 | pending |
| 172 | `pets` | 5 | 333 | 229 | pending |
| 173 | `plastic` | 5 | 312 | 175 | pending |
| 174 | `project` | 5 | 403 | 194 | pending |
| 175 | `railway` | 5 | 124 | 80 | pending |
| 176 | `rubber` | 5 | 311 | 174 | pending |
| 177 | `seismology` | 5 | 306 | 195 | pending |
| 178 | `service` | 5 | 306 | 164 | pending |
| 179 | `shipping` | 5 | 311 | 202 | pending |
| 180 | `stage` | 5 | 324 | 186 | pending |
| 181 | `tunnel` | 5 | 373 | 221 | pending |
| 182 | `woodworking` | 5 | 413 | 297 | pending |
| 183 | `yi` | 5 | 370 | 242 | pending |
| 184 | `photo2` | 4 | 236 | 159 | pending |
| 185 | `stats` | 4 | 281 | 198 | pending |

