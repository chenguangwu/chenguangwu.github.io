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
| 1 | `geometry` | 28 | 915 | 568 | pending |
| 2 | `metrology` | 28 | 836 | 534 | pending |
| 3 | `nuclear` | 28 | 923 | 579 | pending |
| 4 | `robotics` | 28 | 816 | 565 | pending |
| 5 | `chemistry` | 27 | 939 | 654 | pending |
| 6 | `economics` | 27 | 838 | 564 | pending |
| 7 | `food-testing` | 27 | 1873 | 979 | pending |
| 8 | `hematology` | 27 | 2189 | 1253 | pending |
| 9 | `obstetrics` | 27 | 2395 | 1478 | pending |
| 10 | `quantum` | 27 | 839 | 550 | pending |
| 11 | `signal` | 27 | 786 | 541 | pending |
| 12 | `thermodynamics` | 27 | 867 | 576 | pending |
| 13 | `electromagnetism` | 26 | 850 | 588 | pending |
| 14 | `livestock` | 26 | 1993 | 1025 | pending |
| 15 | `reproductive-medicine` | 26 | 2501 | 1254 | pending |
| 16 | `structural` | 26 | 762 | 513 | pending |
| 17 | `banking` | 25 | 728 | 488 | pending |
| 18 | `clinical-lab` | 25 | 1540 | 937 | pending |
| 19 | `clinical-nursing` | 25 | 1906 | 1220 | pending |
| 20 | `construction` | 25 | 1970 | 1231 | pending |
| 21 | `dentistry` | 25 | 1859 | 1120 | pending |
| 22 | `kinematics` | 25 | 809 | 502 | pending |
| 23 | `neurology` | 25 | 2674 | 1537 | pending |
| 24 | `rheumatology` | 25 | 2514 | 1447 | pending |
| 25 | `textile` | 25 | 1994 | 1100 | pending |
| 26 | `cardiology` | 24 | 1917 | 1181 | pending |
| 27 | `food` | 24 | 1772 | 927 | pending |
| 28 | `pediatrics` | 24 | 1865 | 999 | pending |
| 29 | `psychiatry` | 24 | 1565 | 722 | pending |
| 30 | `pulmonology` | 24 | 1832 | 1036 | pending |
| 31 | `urology` | 24 | 2148 | 1138 | pending |
| 32 | `acupuncture` | 23 | 1406 | 656 | pending |
| 33 | `astronomy` | 23 | 1340 | 867 | pending |
| 34 | `dynamics` | 23 | 715 | 464 | pending |
| 35 | `ecommerce` | 23 | 1412 | 661 | pending |
| 36 | `ent` | 23 | 1911 | 1044 | pending |
| 37 | `fluid` | 23 | 670 | 414 | pending |
| 38 | `investment` | 23 | 725 | 507 | pending |
| 39 | `nephrology` | 23 | 1853 | 1034 | pending |
| 40 | `dermatology` | 22 | 2081 | 1077 | pending |
| 41 | `gastroenterology` | 22 | 2114 | 1216 | pending |
| 42 | `rehabilitation` | 22 | 1930 | 1054 | pending |
| 43 | `tcm-chemistry` | 22 | 1690 | 955 | pending |
| 44 | `tcm-pharmacy` | 22 | 1542 | 884 | pending |
| 45 | `beauty` | 21 | 1438 | 852 | pending |
| 46 | `civil` | 21 | 741 | 547 | pending |
| 47 | `electronics` | 21 | 1327 | 723 | pending |
| 48 | `endocrinology` | 21 | 2016 | 1404 | pending |
| 49 | `food-processing` | 21 | 1230 | 518 | pending |
| 50 | `hr` | 21 | 1087 | 564 | pending |
| 51 | `optics` | 21 | 645 | 443 | pending |
| 52 | `property` | 21 | 1344 | 732 | pending |
| 53 | `tcm-diagnosis` | 21 | 2103 | 1170 | pending |
| 54 | `travel` | 21 | 1654 | 918 | pending |
| 55 | `forensic-medicine` | 20 | 2374 | 1597 | pending |
| 56 | `metallurgy` | 20 | 1236 | 646 | pending |
| 57 | `psychology` | 20 | 1057 | 622 | pending |
| 58 | `electrical` | 19 | 810 | 545 | pending |
| 59 | `forestry` | 19 | 1435 | 727 | pending |
| 60 | `language` | 19 | 1123 | 622 | pending |
| 61 | `music` | 19 | 1577 | 893 | pending |
| 62 | `nutrition` | 18 | 980 | 546 | pending |
| 63 | `data` | 17 | 906 | 405 | pending |
| 64 | `advertising` | 16 | 1007 | 520 | pending |
| 65 | `niche` | 16 | 1101 | 690 | pending |
| 66 | `leather` | 15 | 948 | 510 | pending |
| 67 | `logistics` | 15 | 807 | 478 | pending |
| 68 | `safety` | 15 | 838 | 503 | pending |
| 69 | `transport` | 15 | 682 | 495 | pending |
| 70 | `welding` | 15 | 1025 | 546 | pending |
| 71 | `engineering` | 14 | 495 | 324 | pending |
| 72 | `image` | 14 | 882 | 609 | pending |
| 73 | `mechanical` | 14 | 644 | 398 | pending |
| 74 | `medical` | 14 | 936 | 604 | pending |
| 75 | `dyeing` | 13 | 868 | 467 | pending |
| 76 | `gardening` | 12 | 866 | 455 | pending |
| 77 | `mining` | 12 | 768 | 468 | pending |
| 78 | `paper` | 12 | 778 | 399 | pending |
| 79 | `pr` | 12 | 900 | 530 | pending |
| 80 | `chemical` | 11 | 654 | 355 | pending |
| 81 | `elderly` | 11 | 691 | 469 | pending |
| 82 | `fire` | 11 | 774 | 461 | pending |
| 83 | `gas` | 11 | 718 | 380 | pending |
| 84 | `text` | 11 | 467 | 301 | pending |
| 85 | `usedcar` | 11 | 641 | 408 | pending |
| 86 | `hvac` | 10 | 908 | 668 | pending |
| 87 | `pet` | 10 | 657 | 446 | pending |
| 88 | `process` | 10 | 315 | 217 | pending |
| 89 | `security` | 10 | 755 | 532 | pending |
| 90 | `baking` | 9 | 532 | 363 | pending |
| 91 | `misc` | 9 | 609 | 337 | pending |
| 92 | `misc2` | 9 | 616 | 392 | pending |
| 93 | `procurement` | 9 | 563 | 332 | pending |
| 94 | `sales` | 9 | 629 | 362 | pending |
| 95 | `admin` | 8 | 539 | 321 | pending |
| 96 | `cleaning` | 8 | 551 | 382 | pending |
| 97 | `cognition` | 8 | 599 | 422 | pending |
| 98 | `decor` | 8 | 629 | 415 | pending |
| 99 | `library` | 8 | 442 | 247 | pending |
| 100 | `museum` | 8 | 496 | 267 | pending |
| 101 | `quality` | 8 | 507 | 321 | pending |
| 102 | `rental` | 8 | 464 | 281 | pending |
| 103 | `research` | 8 | 527 | 306 | pending |
| 104 | `restaurant` | 8 | 488 | 266 | pending |
| 105 | `telecom` | 8 | 476 | 290 | pending |
| 106 | `audio` | 7 | 512 | 378 | pending |
| 107 | `dance` | 7 | 560 | 377 | pending |
| 108 | `hotel` | 7 | 531 | 329 | pending |
| 109 | `printing` | 7 | 491 | 312 | pending |
| 110 | `woodwork` | 7 | 399 | 292 | pending |
| 111 | `archaeology` | 6 | 360 | 202 | pending |
| 112 | `chinese-cook` | 6 | 471 | 293 | pending |
| 113 | `exhibition` | 6 | 424 | 242 | pending |
| 114 | `film` | 6 | 360 | 236 | pending |
| 115 | `floral` | 6 | 472 | 352 | pending |
| 116 | `funeral` | 6 | 464 | 335 | pending |
| 117 | `home` | 6 | 350 | 211 | pending |
| 118 | `jewelry` | 6 | 430 | 273 | pending |
| 119 | `media` | 6 | 344 | 169 | pending |
| 120 | `office` | 6 | 341 | 264 | pending |
| 121 | `packaging` | 6 | 301 | 171 | pending |
| 122 | `parenting` | 6 | 270 | 164 | pending |
| 123 | `road` | 6 | 460 | 292 | pending |
| 124 | `startup` | 6 | 469 | 309 | pending |
| 125 | `urban` | 6 | 499 | 316 | pending |
| 126 | `video` | 6 | 486 | 311 | pending |
| 127 | `accessibility` | 5 | 347 | 210 | pending |
| 128 | `antiques` | 5 | 345 | 201 | pending |
| 129 | `aquaculture` | 5 | 299 | 189 | pending |
| 130 | `audit` | 5 | 359 | 214 | pending |
| 131 | `bonding` | 5 | 294 | 181 | pending |
| 132 | `bridge` | 5 | 393 | 246 | pending |
| 133 | `ceramics` | 5 | 387 | 247 | pending |
| 134 | `chess` | 5 | 427 | 320 | pending |
| 135 | `chinese` | 5 | 238 | 188 | pending |
| 136 | `edu2` | 5 | 292 | 189 | pending |
| 137 | `fengshui` | 5 | 408 | 300 | pending |
| 138 | `forex` | 5 | 416 | 250 | pending |
| 139 | `futures` | 5 | 411 | 254 | pending |
| 140 | `gardening2` | 5 | 365 | 263 | pending |
| 141 | `glass` | 5 | 364 | 204 | pending |
| 142 | `kids` | 5 | 334 | 198 | pending |
| 143 | `legal2` | 5 | 332 | 200 | pending |
| 144 | `logistics2` | 5 | 319 | 189 | pending |
| 145 | `manufacturing` | 5 | 279 | 154 | pending |
| 146 | `maritime` | 5 | 424 | 282 | pending |
| 147 | `martial` | 5 | 362 | 255 | pending |
| 148 | `medical2` | 5 | 333 | 206 | pending |
| 149 | `pet-training` | 5 | 364 | 263 | pending |
| 150 | `petrochem` | 5 | 355 | 230 | pending |
| 151 | `pets` | 5 | 333 | 229 | pending |
| 152 | `plastic` | 5 | 312 | 175 | pending |
| 153 | `project` | 5 | 403 | 194 | pending |
| 154 | `railway` | 5 | 124 | 80 | pending |
| 155 | `rubber` | 5 | 311 | 174 | pending |
| 156 | `seismology` | 5 | 306 | 195 | pending |
| 157 | `service` | 5 | 306 | 164 | pending |
| 158 | `shipping` | 5 | 311 | 202 | pending |
| 159 | `stage` | 5 | 324 | 186 | pending |
| 160 | `tunnel` | 5 | 373 | 221 | pending |
| 161 | `woodworking` | 5 | 413 | 297 | pending |
| 162 | `yi` | 5 | 370 | 242 | pending |
| 163 | `photo2` | 4 | 236 | 159 | pending |
| 164 | `stats` | 4 | 281 | 198 | pending |

