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
| 1 | `metrology` | 28 | 836 | 534 | pending |
| 2 | `nuclear` | 28 | 923 | 579 | pending |
| 3 | `robotics` | 28 | 816 | 565 | pending |
| 4 | `chemistry` | 27 | 939 | 654 | pending |
| 5 | `economics` | 27 | 838 | 564 | pending |
| 6 | `food-testing` | 27 | 1873 | 979 | pending |
| 7 | `hematology` | 27 | 2189 | 1253 | pending |
| 8 | `obstetrics` | 27 | 2395 | 1478 | pending |
| 9 | `quantum` | 27 | 839 | 550 | pending |
| 10 | `signal` | 27 | 786 | 541 | pending |
| 11 | `thermodynamics` | 27 | 867 | 576 | pending |
| 12 | `electromagnetism` | 26 | 850 | 588 | pending |
| 13 | `livestock` | 26 | 1993 | 1025 | pending |
| 14 | `reproductive-medicine` | 26 | 2501 | 1254 | pending |
| 15 | `structural` | 26 | 762 | 513 | pending |
| 16 | `banking` | 25 | 728 | 488 | pending |
| 17 | `clinical-lab` | 25 | 1540 | 937 | pending |
| 18 | `clinical-nursing` | 25 | 1906 | 1220 | pending |
| 19 | `construction` | 25 | 1970 | 1231 | pending |
| 20 | `dentistry` | 25 | 1859 | 1120 | pending |
| 21 | `kinematics` | 25 | 809 | 502 | pending |
| 22 | `neurology` | 25 | 2674 | 1537 | pending |
| 23 | `rheumatology` | 25 | 2514 | 1447 | pending |
| 24 | `textile` | 25 | 1994 | 1100 | pending |
| 25 | `cardiology` | 24 | 1917 | 1181 | pending |
| 26 | `food` | 24 | 1772 | 927 | pending |
| 27 | `pediatrics` | 24 | 1865 | 999 | pending |
| 28 | `psychiatry` | 24 | 1565 | 722 | pending |
| 29 | `pulmonology` | 24 | 1832 | 1036 | pending |
| 30 | `urology` | 24 | 2148 | 1138 | pending |
| 31 | `acupuncture` | 23 | 1406 | 656 | pending |
| 32 | `astronomy` | 23 | 1340 | 867 | pending |
| 33 | `dynamics` | 23 | 715 | 464 | pending |
| 34 | `ecommerce` | 23 | 1412 | 661 | pending |
| 35 | `ent` | 23 | 1911 | 1044 | pending |
| 36 | `fluid` | 23 | 670 | 414 | pending |
| 37 | `investment` | 23 | 725 | 507 | pending |
| 38 | `nephrology` | 23 | 1853 | 1034 | pending |
| 39 | `dermatology` | 22 | 2081 | 1077 | pending |
| 40 | `gastroenterology` | 22 | 2114 | 1216 | pending |
| 41 | `rehabilitation` | 22 | 1930 | 1054 | pending |
| 42 | `tcm-chemistry` | 22 | 1690 | 955 | pending |
| 43 | `tcm-pharmacy` | 22 | 1542 | 884 | pending |
| 44 | `beauty` | 21 | 1438 | 852 | pending |
| 45 | `civil` | 21 | 741 | 547 | pending |
| 46 | `electronics` | 21 | 1327 | 723 | pending |
| 47 | `endocrinology` | 21 | 2016 | 1404 | pending |
| 48 | `food-processing` | 21 | 1230 | 518 | pending |
| 49 | `hr` | 21 | 1087 | 564 | pending |
| 50 | `optics` | 21 | 645 | 443 | pending |
| 51 | `property` | 21 | 1344 | 732 | pending |
| 52 | `tcm-diagnosis` | 21 | 2103 | 1170 | pending |
| 53 | `travel` | 21 | 1654 | 918 | pending |
| 54 | `forensic-medicine` | 20 | 2374 | 1597 | pending |
| 55 | `metallurgy` | 20 | 1236 | 646 | pending |
| 56 | `psychology` | 20 | 1057 | 622 | pending |
| 57 | `electrical` | 19 | 810 | 545 | pending |
| 58 | `forestry` | 19 | 1435 | 727 | pending |
| 59 | `language` | 19 | 1123 | 622 | pending |
| 60 | `music` | 19 | 1577 | 893 | pending |
| 61 | `nutrition` | 18 | 980 | 546 | pending |
| 62 | `data` | 17 | 906 | 405 | pending |
| 63 | `advertising` | 16 | 1007 | 520 | pending |
| 64 | `niche` | 16 | 1101 | 690 | pending |
| 65 | `leather` | 15 | 948 | 510 | pending |
| 66 | `logistics` | 15 | 807 | 478 | pending |
| 67 | `safety` | 15 | 838 | 503 | pending |
| 68 | `transport` | 15 | 682 | 495 | pending |
| 69 | `welding` | 15 | 1025 | 546 | pending |
| 70 | `engineering` | 14 | 495 | 324 | pending |
| 71 | `image` | 14 | 882 | 609 | pending |
| 72 | `mechanical` | 14 | 644 | 398 | pending |
| 73 | `medical` | 14 | 936 | 604 | pending |
| 74 | `dyeing` | 13 | 868 | 467 | pending |
| 75 | `gardening` | 12 | 866 | 455 | pending |
| 76 | `mining` | 12 | 768 | 468 | pending |
| 77 | `paper` | 12 | 778 | 399 | pending |
| 78 | `pr` | 12 | 900 | 530 | pending |
| 79 | `chemical` | 11 | 654 | 355 | pending |
| 80 | `elderly` | 11 | 691 | 469 | pending |
| 81 | `fire` | 11 | 774 | 461 | pending |
| 82 | `gas` | 11 | 718 | 380 | pending |
| 83 | `text` | 11 | 467 | 301 | pending |
| 84 | `usedcar` | 11 | 641 | 408 | pending |
| 85 | `hvac` | 10 | 908 | 668 | pending |
| 86 | `pet` | 10 | 657 | 446 | pending |
| 87 | `process` | 10 | 315 | 217 | pending |
| 88 | `security` | 10 | 755 | 532 | pending |
| 89 | `baking` | 9 | 532 | 363 | pending |
| 90 | `misc` | 9 | 609 | 337 | pending |
| 91 | `misc2` | 9 | 616 | 392 | pending |
| 92 | `procurement` | 9 | 563 | 332 | pending |
| 93 | `sales` | 9 | 629 | 362 | pending |
| 94 | `admin` | 8 | 539 | 321 | pending |
| 95 | `cleaning` | 8 | 551 | 382 | pending |
| 96 | `cognition` | 8 | 599 | 422 | pending |
| 97 | `decor` | 8 | 629 | 415 | pending |
| 98 | `library` | 8 | 442 | 247 | pending |
| 99 | `museum` | 8 | 496 | 267 | pending |
| 100 | `quality` | 8 | 507 | 321 | pending |
| 101 | `rental` | 8 | 464 | 281 | pending |
| 102 | `research` | 8 | 527 | 306 | pending |
| 103 | `restaurant` | 8 | 488 | 266 | pending |
| 104 | `telecom` | 8 | 476 | 290 | pending |
| 105 | `audio` | 7 | 512 | 378 | pending |
| 106 | `dance` | 7 | 560 | 377 | pending |
| 107 | `hotel` | 7 | 531 | 329 | pending |
| 108 | `printing` | 7 | 491 | 312 | pending |
| 109 | `woodwork` | 7 | 399 | 292 | pending |
| 110 | `archaeology` | 6 | 360 | 202 | pending |
| 111 | `chinese-cook` | 6 | 471 | 293 | pending |
| 112 | `exhibition` | 6 | 424 | 242 | pending |
| 113 | `film` | 6 | 360 | 236 | pending |
| 114 | `floral` | 6 | 472 | 352 | pending |
| 115 | `funeral` | 6 | 464 | 335 | pending |
| 116 | `home` | 6 | 350 | 211 | pending |
| 117 | `jewelry` | 6 | 430 | 273 | pending |
| 118 | `media` | 6 | 344 | 169 | pending |
| 119 | `office` | 6 | 341 | 264 | pending |
| 120 | `packaging` | 6 | 301 | 171 | pending |
| 121 | `parenting` | 6 | 270 | 164 | pending |
| 122 | `road` | 6 | 460 | 292 | pending |
| 123 | `startup` | 6 | 469 | 309 | pending |
| 124 | `urban` | 6 | 499 | 316 | pending |
| 125 | `video` | 6 | 486 | 311 | pending |
| 126 | `accessibility` | 5 | 347 | 210 | pending |
| 127 | `antiques` | 5 | 345 | 201 | pending |
| 128 | `aquaculture` | 5 | 299 | 189 | pending |
| 129 | `audit` | 5 | 359 | 214 | pending |
| 130 | `bonding` | 5 | 294 | 181 | pending |
| 131 | `bridge` | 5 | 393 | 246 | pending |
| 132 | `ceramics` | 5 | 387 | 247 | pending |
| 133 | `chess` | 5 | 427 | 320 | pending |
| 134 | `chinese` | 5 | 238 | 188 | pending |
| 135 | `edu2` | 5 | 292 | 189 | pending |
| 136 | `fengshui` | 5 | 408 | 300 | pending |
| 137 | `forex` | 5 | 416 | 250 | pending |
| 138 | `futures` | 5 | 411 | 254 | pending |
| 139 | `gardening2` | 5 | 365 | 263 | pending |
| 140 | `glass` | 5 | 364 | 204 | pending |
| 141 | `kids` | 5 | 334 | 198 | pending |
| 142 | `legal2` | 5 | 332 | 200 | pending |
| 143 | `logistics2` | 5 | 319 | 189 | pending |
| 144 | `manufacturing` | 5 | 279 | 154 | pending |
| 145 | `maritime` | 5 | 424 | 282 | pending |
| 146 | `martial` | 5 | 362 | 255 | pending |
| 147 | `medical2` | 5 | 333 | 206 | pending |
| 148 | `pet-training` | 5 | 364 | 263 | pending |
| 149 | `petrochem` | 5 | 355 | 230 | pending |
| 150 | `pets` | 5 | 333 | 229 | pending |
| 151 | `plastic` | 5 | 312 | 175 | pending |
| 152 | `project` | 5 | 403 | 194 | pending |
| 153 | `railway` | 5 | 124 | 80 | pending |
| 154 | `rubber` | 5 | 311 | 174 | pending |
| 155 | `seismology` | 5 | 306 | 195 | pending |
| 156 | `service` | 5 | 306 | 164 | pending |
| 157 | `shipping` | 5 | 311 | 202 | pending |
| 158 | `stage` | 5 | 324 | 186 | pending |
| 159 | `tunnel` | 5 | 373 | 221 | pending |
| 160 | `woodworking` | 5 | 413 | 297 | pending |
| 161 | `yi` | 5 | 370 | 242 | pending |
| 162 | `photo2` | 4 | 236 | 159 | pending |
| 163 | `stats` | 4 | 281 | 198 | pending |

