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
| 1 | `encode` | 30 | 1235 | 722 | pending |
| 2 | `tax` | 29 | 1007 | 707 | pending |
| 3 | `acoustics` | 28 | 832 | 543 | pending |
| 4 | `geometry` | 28 | 915 | 568 | pending |
| 5 | `metrology` | 28 | 836 | 534 | pending |
| 6 | `nuclear` | 28 | 923 | 579 | pending |
| 7 | `robotics` | 28 | 816 | 565 | pending |
| 8 | `chemistry` | 27 | 939 | 654 | pending |
| 9 | `economics` | 27 | 838 | 564 | pending |
| 10 | `food-testing` | 27 | 1873 | 979 | pending |
| 11 | `hematology` | 27 | 2189 | 1253 | pending |
| 12 | `obstetrics` | 27 | 2395 | 1478 | pending |
| 13 | `quantum` | 27 | 839 | 550 | pending |
| 14 | `signal` | 27 | 786 | 541 | pending |
| 15 | `thermodynamics` | 27 | 867 | 576 | pending |
| 16 | `electromagnetism` | 26 | 850 | 588 | pending |
| 17 | `livestock` | 26 | 1993 | 1025 | pending |
| 18 | `reproductive-medicine` | 26 | 2501 | 1254 | pending |
| 19 | `structural` | 26 | 762 | 513 | pending |
| 20 | `banking` | 25 | 728 | 488 | pending |
| 21 | `clinical-lab` | 25 | 1540 | 937 | pending |
| 22 | `clinical-nursing` | 25 | 1906 | 1220 | pending |
| 23 | `construction` | 25 | 1970 | 1231 | pending |
| 24 | `dentistry` | 25 | 1859 | 1120 | pending |
| 25 | `kinematics` | 25 | 809 | 502 | pending |
| 26 | `neurology` | 25 | 2674 | 1537 | pending |
| 27 | `rheumatology` | 25 | 2514 | 1447 | pending |
| 28 | `textile` | 25 | 1994 | 1100 | pending |
| 29 | `cardiology` | 24 | 1917 | 1181 | pending |
| 30 | `food` | 24 | 1772 | 927 | pending |
| 31 | `pediatrics` | 24 | 1865 | 999 | pending |
| 32 | `psychiatry` | 24 | 1565 | 722 | pending |
| 33 | `pulmonology` | 24 | 1832 | 1036 | pending |
| 34 | `urology` | 24 | 2148 | 1138 | pending |
| 35 | `acupuncture` | 23 | 1406 | 656 | pending |
| 36 | `astronomy` | 23 | 1340 | 867 | pending |
| 37 | `dynamics` | 23 | 715 | 464 | pending |
| 38 | `ecommerce` | 23 | 1412 | 661 | pending |
| 39 | `ent` | 23 | 1911 | 1044 | pending |
| 40 | `fluid` | 23 | 670 | 414 | pending |
| 41 | `investment` | 23 | 725 | 507 | pending |
| 42 | `nephrology` | 23 | 1853 | 1034 | pending |
| 43 | `dermatology` | 22 | 2081 | 1077 | pending |
| 44 | `gastroenterology` | 22 | 2114 | 1216 | pending |
| 45 | `rehabilitation` | 22 | 1930 | 1054 | pending |
| 46 | `tcm-chemistry` | 22 | 1690 | 955 | pending |
| 47 | `tcm-pharmacy` | 22 | 1542 | 884 | pending |
| 48 | `beauty` | 21 | 1438 | 852 | pending |
| 49 | `civil` | 21 | 741 | 547 | pending |
| 50 | `electronics` | 21 | 1327 | 723 | pending |
| 51 | `endocrinology` | 21 | 2016 | 1404 | pending |
| 52 | `food-processing` | 21 | 1230 | 518 | pending |
| 53 | `hr` | 21 | 1087 | 564 | pending |
| 54 | `optics` | 21 | 645 | 443 | pending |
| 55 | `property` | 21 | 1344 | 732 | pending |
| 56 | `tcm-diagnosis` | 21 | 2103 | 1170 | pending |
| 57 | `travel` | 21 | 1654 | 918 | pending |
| 58 | `forensic-medicine` | 20 | 2374 | 1597 | pending |
| 59 | `metallurgy` | 20 | 1236 | 646 | pending |
| 60 | `psychology` | 20 | 1057 | 622 | pending |
| 61 | `electrical` | 19 | 810 | 545 | pending |
| 62 | `forestry` | 19 | 1435 | 727 | pending |
| 63 | `language` | 19 | 1123 | 622 | pending |
| 64 | `music` | 19 | 1577 | 893 | pending |
| 65 | `nutrition` | 18 | 980 | 546 | pending |
| 66 | `data` | 17 | 906 | 405 | pending |
| 67 | `advertising` | 16 | 1007 | 520 | pending |
| 68 | `niche` | 16 | 1101 | 690 | pending |
| 69 | `leather` | 15 | 948 | 510 | pending |
| 70 | `logistics` | 15 | 807 | 478 | pending |
| 71 | `safety` | 15 | 838 | 503 | pending |
| 72 | `transport` | 15 | 682 | 495 | pending |
| 73 | `welding` | 15 | 1025 | 546 | pending |
| 74 | `engineering` | 14 | 495 | 324 | pending |
| 75 | `image` | 14 | 882 | 609 | pending |
| 76 | `mechanical` | 14 | 644 | 398 | pending |
| 77 | `medical` | 14 | 936 | 604 | pending |
| 78 | `dyeing` | 13 | 868 | 467 | pending |
| 79 | `gardening` | 12 | 866 | 455 | pending |
| 80 | `mining` | 12 | 768 | 468 | pending |
| 81 | `paper` | 12 | 778 | 399 | pending |
| 82 | `pr` | 12 | 900 | 530 | pending |
| 83 | `chemical` | 11 | 654 | 355 | pending |
| 84 | `elderly` | 11 | 691 | 469 | pending |
| 85 | `fire` | 11 | 774 | 461 | pending |
| 86 | `gas` | 11 | 718 | 380 | pending |
| 87 | `text` | 11 | 467 | 301 | pending |
| 88 | `usedcar` | 11 | 641 | 408 | pending |
| 89 | `hvac` | 10 | 908 | 668 | pending |
| 90 | `pet` | 10 | 657 | 446 | pending |
| 91 | `process` | 10 | 315 | 217 | pending |
| 92 | `security` | 10 | 755 | 532 | pending |
| 93 | `baking` | 9 | 532 | 363 | pending |
| 94 | `misc` | 9 | 609 | 337 | pending |
| 95 | `misc2` | 9 | 616 | 392 | pending |
| 96 | `procurement` | 9 | 563 | 332 | pending |
| 97 | `sales` | 9 | 629 | 362 | pending |
| 98 | `admin` | 8 | 539 | 321 | pending |
| 99 | `cleaning` | 8 | 551 | 382 | pending |
| 100 | `cognition` | 8 | 599 | 422 | pending |
| 101 | `decor` | 8 | 629 | 415 | pending |
| 102 | `library` | 8 | 442 | 247 | pending |
| 103 | `museum` | 8 | 496 | 267 | pending |
| 104 | `quality` | 8 | 507 | 321 | pending |
| 105 | `rental` | 8 | 464 | 281 | pending |
| 106 | `research` | 8 | 527 | 306 | pending |
| 107 | `restaurant` | 8 | 488 | 266 | pending |
| 108 | `telecom` | 8 | 476 | 290 | pending |
| 109 | `audio` | 7 | 512 | 378 | pending |
| 110 | `dance` | 7 | 560 | 377 | pending |
| 111 | `hotel` | 7 | 531 | 329 | pending |
| 112 | `printing` | 7 | 491 | 312 | pending |
| 113 | `woodwork` | 7 | 399 | 292 | pending |
| 114 | `archaeology` | 6 | 360 | 202 | pending |
| 115 | `chinese-cook` | 6 | 471 | 293 | pending |
| 116 | `exhibition` | 6 | 424 | 242 | pending |
| 117 | `film` | 6 | 360 | 236 | pending |
| 118 | `floral` | 6 | 472 | 352 | pending |
| 119 | `funeral` | 6 | 464 | 335 | pending |
| 120 | `home` | 6 | 350 | 211 | pending |
| 121 | `jewelry` | 6 | 430 | 273 | pending |
| 122 | `media` | 6 | 344 | 169 | pending |
| 123 | `office` | 6 | 341 | 264 | pending |
| 124 | `packaging` | 6 | 301 | 171 | pending |
| 125 | `parenting` | 6 | 270 | 164 | pending |
| 126 | `road` | 6 | 460 | 292 | pending |
| 127 | `startup` | 6 | 469 | 309 | pending |
| 128 | `urban` | 6 | 499 | 316 | pending |
| 129 | `video` | 6 | 486 | 311 | pending |
| 130 | `accessibility` | 5 | 347 | 210 | pending |
| 131 | `antiques` | 5 | 345 | 201 | pending |
| 132 | `aquaculture` | 5 | 299 | 189 | pending |
| 133 | `audit` | 5 | 359 | 214 | pending |
| 134 | `bonding` | 5 | 294 | 181 | pending |
| 135 | `bridge` | 5 | 393 | 246 | pending |
| 136 | `ceramics` | 5 | 387 | 247 | pending |
| 137 | `chess` | 5 | 427 | 320 | pending |
| 138 | `chinese` | 5 | 238 | 188 | pending |
| 139 | `edu2` | 5 | 292 | 189 | pending |
| 140 | `fengshui` | 5 | 408 | 300 | pending |
| 141 | `forex` | 5 | 416 | 250 | pending |
| 142 | `futures` | 5 | 411 | 254 | pending |
| 143 | `gardening2` | 5 | 365 | 263 | pending |
| 144 | `glass` | 5 | 364 | 204 | pending |
| 145 | `kids` | 5 | 334 | 198 | pending |
| 146 | `legal2` | 5 | 332 | 200 | pending |
| 147 | `logistics2` | 5 | 319 | 189 | pending |
| 148 | `manufacturing` | 5 | 279 | 154 | pending |
| 149 | `maritime` | 5 | 424 | 282 | pending |
| 150 | `martial` | 5 | 362 | 255 | pending |
| 151 | `medical2` | 5 | 333 | 206 | pending |
| 152 | `pet-training` | 5 | 364 | 263 | pending |
| 153 | `petrochem` | 5 | 355 | 230 | pending |
| 154 | `pets` | 5 | 333 | 229 | pending |
| 155 | `plastic` | 5 | 312 | 175 | pending |
| 156 | `project` | 5 | 403 | 194 | pending |
| 157 | `railway` | 5 | 124 | 80 | pending |
| 158 | `rubber` | 5 | 311 | 174 | pending |
| 159 | `seismology` | 5 | 306 | 195 | pending |
| 160 | `service` | 5 | 306 | 164 | pending |
| 161 | `shipping` | 5 | 311 | 202 | pending |
| 162 | `stage` | 5 | 324 | 186 | pending |
| 163 | `tunnel` | 5 | 373 | 221 | pending |
| 164 | `woodworking` | 5 | 413 | 297 | pending |
| 165 | `yi` | 5 | 370 | 242 | pending |
| 166 | `photo2` | 4 | 236 | 159 | pending |
| 167 | `stats` | 4 | 281 | 198 | pending |

