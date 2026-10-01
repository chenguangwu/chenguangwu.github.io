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
| 1 | `cosmetic-derm` | 33 | 2832 | 1632 | pending |
| 2 | `insurance` | 33 | 1092 | 727 | pending |
| 3 | `ophthalmology` | 32 | 2371 | 1278 | pending |
| 4 | `photo` | 32 | 1459 | 744 | pending |
| 5 | `materials` | 31 | 1143 | 742 | pending |
| 6 | `encode` | 30 | 1235 | 722 | pending |
| 7 | `tax` | 29 | 1007 | 707 | pending |
| 8 | `acoustics` | 28 | 832 | 543 | pending |
| 9 | `geometry` | 28 | 915 | 568 | pending |
| 10 | `metrology` | 28 | 836 | 534 | pending |
| 11 | `nuclear` | 28 | 923 | 579 | pending |
| 12 | `robotics` | 28 | 816 | 565 | pending |
| 13 | `chemistry` | 27 | 939 | 654 | pending |
| 14 | `economics` | 27 | 838 | 564 | pending |
| 15 | `food-testing` | 27 | 1873 | 979 | pending |
| 16 | `hematology` | 27 | 2189 | 1253 | pending |
| 17 | `obstetrics` | 27 | 2395 | 1478 | pending |
| 18 | `quantum` | 27 | 839 | 550 | pending |
| 19 | `signal` | 27 | 786 | 541 | pending |
| 20 | `thermodynamics` | 27 | 867 | 576 | pending |
| 21 | `electromagnetism` | 26 | 850 | 588 | pending |
| 22 | `livestock` | 26 | 1993 | 1025 | pending |
| 23 | `reproductive-medicine` | 26 | 2501 | 1254 | pending |
| 24 | `structural` | 26 | 762 | 513 | pending |
| 25 | `banking` | 25 | 728 | 488 | pending |
| 26 | `clinical-lab` | 25 | 1540 | 937 | pending |
| 27 | `clinical-nursing` | 25 | 1906 | 1220 | pending |
| 28 | `construction` | 25 | 1970 | 1231 | pending |
| 29 | `dentistry` | 25 | 1859 | 1120 | pending |
| 30 | `kinematics` | 25 | 809 | 502 | pending |
| 31 | `neurology` | 25 | 2674 | 1537 | pending |
| 32 | `rheumatology` | 25 | 2514 | 1447 | pending |
| 33 | `textile` | 25 | 1994 | 1100 | pending |
| 34 | `cardiology` | 24 | 1917 | 1181 | pending |
| 35 | `food` | 24 | 1772 | 927 | pending |
| 36 | `pediatrics` | 24 | 1865 | 999 | pending |
| 37 | `psychiatry` | 24 | 1565 | 722 | pending |
| 38 | `pulmonology` | 24 | 1832 | 1036 | pending |
| 39 | `urology` | 24 | 2148 | 1138 | pending |
| 40 | `acupuncture` | 23 | 1406 | 656 | pending |
| 41 | `astronomy` | 23 | 1340 | 867 | pending |
| 42 | `dynamics` | 23 | 715 | 464 | pending |
| 43 | `ecommerce` | 23 | 1412 | 661 | pending |
| 44 | `ent` | 23 | 1911 | 1044 | pending |
| 45 | `fluid` | 23 | 670 | 414 | pending |
| 46 | `investment` | 23 | 725 | 507 | pending |
| 47 | `nephrology` | 23 | 1853 | 1034 | pending |
| 48 | `dermatology` | 22 | 2081 | 1077 | pending |
| 49 | `gastroenterology` | 22 | 2114 | 1216 | pending |
| 50 | `rehabilitation` | 22 | 1930 | 1054 | pending |
| 51 | `tcm-chemistry` | 22 | 1690 | 955 | pending |
| 52 | `tcm-pharmacy` | 22 | 1542 | 884 | pending |
| 53 | `beauty` | 21 | 1438 | 852 | pending |
| 54 | `civil` | 21 | 741 | 547 | pending |
| 55 | `electronics` | 21 | 1327 | 723 | pending |
| 56 | `endocrinology` | 21 | 2016 | 1404 | pending |
| 57 | `food-processing` | 21 | 1230 | 518 | pending |
| 58 | `hr` | 21 | 1087 | 564 | pending |
| 59 | `optics` | 21 | 645 | 443 | pending |
| 60 | `property` | 21 | 1344 | 732 | pending |
| 61 | `tcm-diagnosis` | 21 | 2103 | 1170 | pending |
| 62 | `travel` | 21 | 1654 | 918 | pending |
| 63 | `forensic-medicine` | 20 | 2374 | 1597 | pending |
| 64 | `metallurgy` | 20 | 1236 | 646 | pending |
| 65 | `psychology` | 20 | 1057 | 622 | pending |
| 66 | `electrical` | 19 | 810 | 545 | pending |
| 67 | `forestry` | 19 | 1435 | 727 | pending |
| 68 | `language` | 19 | 1123 | 622 | pending |
| 69 | `music` | 19 | 1577 | 893 | pending |
| 70 | `nutrition` | 18 | 980 | 546 | pending |
| 71 | `data` | 17 | 906 | 405 | pending |
| 72 | `advertising` | 16 | 1007 | 520 | pending |
| 73 | `niche` | 16 | 1101 | 690 | pending |
| 74 | `leather` | 15 | 948 | 510 | pending |
| 75 | `logistics` | 15 | 807 | 478 | pending |
| 76 | `safety` | 15 | 838 | 503 | pending |
| 77 | `transport` | 15 | 682 | 495 | pending |
| 78 | `welding` | 15 | 1025 | 546 | pending |
| 79 | `engineering` | 14 | 495 | 324 | pending |
| 80 | `image` | 14 | 882 | 609 | pending |
| 81 | `mechanical` | 14 | 644 | 398 | pending |
| 82 | `medical` | 14 | 936 | 604 | pending |
| 83 | `dyeing` | 13 | 868 | 467 | pending |
| 84 | `gardening` | 12 | 866 | 455 | pending |
| 85 | `mining` | 12 | 768 | 468 | pending |
| 86 | `paper` | 12 | 778 | 399 | pending |
| 87 | `pr` | 12 | 900 | 530 | pending |
| 88 | `chemical` | 11 | 654 | 355 | pending |
| 89 | `elderly` | 11 | 691 | 469 | pending |
| 90 | `fire` | 11 | 774 | 461 | pending |
| 91 | `gas` | 11 | 718 | 380 | pending |
| 92 | `text` | 11 | 467 | 301 | pending |
| 93 | `usedcar` | 11 | 641 | 408 | pending |
| 94 | `hvac` | 10 | 908 | 668 | pending |
| 95 | `pet` | 10 | 657 | 446 | pending |
| 96 | `process` | 10 | 315 | 217 | pending |
| 97 | `security` | 10 | 755 | 532 | pending |
| 98 | `baking` | 9 | 532 | 363 | pending |
| 99 | `misc` | 9 | 609 | 337 | pending |
| 100 | `misc2` | 9 | 616 | 392 | pending |
| 101 | `procurement` | 9 | 563 | 332 | pending |
| 102 | `sales` | 9 | 629 | 362 | pending |
| 103 | `admin` | 8 | 539 | 321 | pending |
| 104 | `cleaning` | 8 | 551 | 382 | pending |
| 105 | `cognition` | 8 | 599 | 422 | pending |
| 106 | `decor` | 8 | 629 | 415 | pending |
| 107 | `library` | 8 | 442 | 247 | pending |
| 108 | `museum` | 8 | 496 | 267 | pending |
| 109 | `quality` | 8 | 507 | 321 | pending |
| 110 | `rental` | 8 | 464 | 281 | pending |
| 111 | `research` | 8 | 527 | 306 | pending |
| 112 | `restaurant` | 8 | 488 | 266 | pending |
| 113 | `telecom` | 8 | 476 | 290 | pending |
| 114 | `audio` | 7 | 512 | 378 | pending |
| 115 | `dance` | 7 | 560 | 377 | pending |
| 116 | `hotel` | 7 | 531 | 329 | pending |
| 117 | `printing` | 7 | 491 | 312 | pending |
| 118 | `woodwork` | 7 | 399 | 292 | pending |
| 119 | `archaeology` | 6 | 360 | 202 | pending |
| 120 | `chinese-cook` | 6 | 471 | 293 | pending |
| 121 | `exhibition` | 6 | 424 | 242 | pending |
| 122 | `film` | 6 | 360 | 236 | pending |
| 123 | `floral` | 6 | 472 | 352 | pending |
| 124 | `funeral` | 6 | 464 | 335 | pending |
| 125 | `home` | 6 | 350 | 211 | pending |
| 126 | `jewelry` | 6 | 430 | 273 | pending |
| 127 | `media` | 6 | 344 | 169 | pending |
| 128 | `office` | 6 | 341 | 264 | pending |
| 129 | `packaging` | 6 | 301 | 171 | pending |
| 130 | `parenting` | 6 | 270 | 164 | pending |
| 131 | `road` | 6 | 460 | 292 | pending |
| 132 | `startup` | 6 | 469 | 309 | pending |
| 133 | `urban` | 6 | 499 | 316 | pending |
| 134 | `video` | 6 | 486 | 311 | pending |
| 135 | `accessibility` | 5 | 347 | 210 | pending |
| 136 | `antiques` | 5 | 345 | 201 | pending |
| 137 | `aquaculture` | 5 | 299 | 189 | pending |
| 138 | `audit` | 5 | 359 | 214 | pending |
| 139 | `bonding` | 5 | 294 | 181 | pending |
| 140 | `bridge` | 5 | 393 | 246 | pending |
| 141 | `ceramics` | 5 | 387 | 247 | pending |
| 142 | `chess` | 5 | 427 | 320 | pending |
| 143 | `chinese` | 5 | 238 | 188 | pending |
| 144 | `edu2` | 5 | 292 | 189 | pending |
| 145 | `fengshui` | 5 | 408 | 300 | pending |
| 146 | `forex` | 5 | 416 | 250 | pending |
| 147 | `futures` | 5 | 411 | 254 | pending |
| 148 | `gardening2` | 5 | 365 | 263 | pending |
| 149 | `glass` | 5 | 364 | 204 | pending |
| 150 | `kids` | 5 | 334 | 198 | pending |
| 151 | `legal2` | 5 | 332 | 200 | pending |
| 152 | `logistics2` | 5 | 319 | 189 | pending |
| 153 | `manufacturing` | 5 | 279 | 154 | pending |
| 154 | `maritime` | 5 | 424 | 282 | pending |
| 155 | `martial` | 5 | 362 | 255 | pending |
| 156 | `medical2` | 5 | 333 | 206 | pending |
| 157 | `pet-training` | 5 | 364 | 263 | pending |
| 158 | `petrochem` | 5 | 355 | 230 | pending |
| 159 | `pets` | 5 | 333 | 229 | pending |
| 160 | `plastic` | 5 | 312 | 175 | pending |
| 161 | `project` | 5 | 403 | 194 | pending |
| 162 | `railway` | 5 | 124 | 80 | pending |
| 163 | `rubber` | 5 | 311 | 174 | pending |
| 164 | `seismology` | 5 | 306 | 195 | pending |
| 165 | `service` | 5 | 306 | 164 | pending |
| 166 | `shipping` | 5 | 311 | 202 | pending |
| 167 | `stage` | 5 | 324 | 186 | pending |
| 168 | `tunnel` | 5 | 373 | 221 | pending |
| 169 | `woodworking` | 5 | 413 | 297 | pending |
| 170 | `yi` | 5 | 370 | 242 | pending |
| 171 | `photo2` | 4 | 236 | 159 | pending |
| 172 | `stats` | 4 | 281 | 198 | pending |

