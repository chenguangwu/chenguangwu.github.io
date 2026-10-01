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
| 1 | `accounting` | 35 | 1222 | 792 | pending |
| 2 | `healthcare` | 35 | 1317 | 843 | pending |
| 3 | `securities` | 35 | 1319 | 914 | pending |
| 4 | `cosmetic-derm` | 33 | 2832 | 1632 | pending |
| 5 | `insurance` | 33 | 1092 | 727 | pending |
| 6 | `ophthalmology` | 32 | 2371 | 1278 | pending |
| 7 | `photo` | 32 | 1459 | 744 | pending |
| 8 | `materials` | 31 | 1143 | 742 | pending |
| 9 | `encode` | 30 | 1235 | 722 | pending |
| 10 | `tax` | 29 | 1007 | 707 | pending |
| 11 | `acoustics` | 28 | 832 | 543 | pending |
| 12 | `geometry` | 28 | 915 | 568 | pending |
| 13 | `metrology` | 28 | 836 | 534 | pending |
| 14 | `nuclear` | 28 | 923 | 579 | pending |
| 15 | `robotics` | 28 | 816 | 565 | pending |
| 16 | `chemistry` | 27 | 939 | 654 | pending |
| 17 | `economics` | 27 | 838 | 564 | pending |
| 18 | `food-testing` | 27 | 1873 | 979 | pending |
| 19 | `hematology` | 27 | 2189 | 1253 | pending |
| 20 | `obstetrics` | 27 | 2395 | 1478 | pending |
| 21 | `quantum` | 27 | 839 | 550 | pending |
| 22 | `signal` | 27 | 786 | 541 | pending |
| 23 | `thermodynamics` | 27 | 867 | 576 | pending |
| 24 | `electromagnetism` | 26 | 850 | 588 | pending |
| 25 | `livestock` | 26 | 1993 | 1025 | pending |
| 26 | `reproductive-medicine` | 26 | 2501 | 1254 | pending |
| 27 | `structural` | 26 | 762 | 513 | pending |
| 28 | `banking` | 25 | 728 | 488 | pending |
| 29 | `clinical-lab` | 25 | 1540 | 937 | pending |
| 30 | `clinical-nursing` | 25 | 1906 | 1220 | pending |
| 31 | `construction` | 25 | 1970 | 1231 | pending |
| 32 | `dentistry` | 25 | 1859 | 1120 | pending |
| 33 | `kinematics` | 25 | 809 | 502 | pending |
| 34 | `neurology` | 25 | 2674 | 1537 | pending |
| 35 | `rheumatology` | 25 | 2514 | 1447 | pending |
| 36 | `textile` | 25 | 1994 | 1100 | pending |
| 37 | `cardiology` | 24 | 1917 | 1181 | pending |
| 38 | `food` | 24 | 1772 | 927 | pending |
| 39 | `pediatrics` | 24 | 1865 | 999 | pending |
| 40 | `psychiatry` | 24 | 1565 | 722 | pending |
| 41 | `pulmonology` | 24 | 1832 | 1036 | pending |
| 42 | `urology` | 24 | 2148 | 1138 | pending |
| 43 | `acupuncture` | 23 | 1406 | 656 | pending |
| 44 | `astronomy` | 23 | 1340 | 867 | pending |
| 45 | `dynamics` | 23 | 715 | 464 | pending |
| 46 | `ecommerce` | 23 | 1412 | 661 | pending |
| 47 | `ent` | 23 | 1911 | 1044 | pending |
| 48 | `fluid` | 23 | 670 | 414 | pending |
| 49 | `investment` | 23 | 725 | 507 | pending |
| 50 | `nephrology` | 23 | 1853 | 1034 | pending |
| 51 | `dermatology` | 22 | 2081 | 1077 | pending |
| 52 | `gastroenterology` | 22 | 2114 | 1216 | pending |
| 53 | `rehabilitation` | 22 | 1930 | 1054 | pending |
| 54 | `tcm-chemistry` | 22 | 1690 | 955 | pending |
| 55 | `tcm-pharmacy` | 22 | 1542 | 884 | pending |
| 56 | `beauty` | 21 | 1438 | 852 | pending |
| 57 | `civil` | 21 | 741 | 547 | pending |
| 58 | `electronics` | 21 | 1327 | 723 | pending |
| 59 | `endocrinology` | 21 | 2016 | 1404 | pending |
| 60 | `food-processing` | 21 | 1230 | 518 | pending |
| 61 | `hr` | 21 | 1087 | 564 | pending |
| 62 | `optics` | 21 | 645 | 443 | pending |
| 63 | `property` | 21 | 1344 | 732 | pending |
| 64 | `tcm-diagnosis` | 21 | 2103 | 1170 | pending |
| 65 | `travel` | 21 | 1654 | 918 | pending |
| 66 | `forensic-medicine` | 20 | 2374 | 1597 | pending |
| 67 | `metallurgy` | 20 | 1236 | 646 | pending |
| 68 | `psychology` | 20 | 1057 | 622 | pending |
| 69 | `electrical` | 19 | 810 | 545 | pending |
| 70 | `forestry` | 19 | 1435 | 727 | pending |
| 71 | `language` | 19 | 1123 | 622 | pending |
| 72 | `music` | 19 | 1577 | 893 | pending |
| 73 | `nutrition` | 18 | 980 | 546 | pending |
| 74 | `data` | 17 | 906 | 405 | pending |
| 75 | `advertising` | 16 | 1007 | 520 | pending |
| 76 | `niche` | 16 | 1101 | 690 | pending |
| 77 | `leather` | 15 | 948 | 510 | pending |
| 78 | `logistics` | 15 | 807 | 478 | pending |
| 79 | `safety` | 15 | 838 | 503 | pending |
| 80 | `transport` | 15 | 682 | 495 | pending |
| 81 | `welding` | 15 | 1025 | 546 | pending |
| 82 | `engineering` | 14 | 495 | 324 | pending |
| 83 | `image` | 14 | 882 | 609 | pending |
| 84 | `mechanical` | 14 | 644 | 398 | pending |
| 85 | `medical` | 14 | 936 | 604 | pending |
| 86 | `dyeing` | 13 | 868 | 467 | pending |
| 87 | `gardening` | 12 | 866 | 455 | pending |
| 88 | `mining` | 12 | 768 | 468 | pending |
| 89 | `paper` | 12 | 778 | 399 | pending |
| 90 | `pr` | 12 | 900 | 530 | pending |
| 91 | `chemical` | 11 | 654 | 355 | pending |
| 92 | `elderly` | 11 | 691 | 469 | pending |
| 93 | `fire` | 11 | 774 | 461 | pending |
| 94 | `gas` | 11 | 718 | 380 | pending |
| 95 | `text` | 11 | 467 | 301 | pending |
| 96 | `usedcar` | 11 | 641 | 408 | pending |
| 97 | `hvac` | 10 | 908 | 668 | pending |
| 98 | `pet` | 10 | 657 | 446 | pending |
| 99 | `process` | 10 | 315 | 217 | pending |
| 100 | `security` | 10 | 755 | 532 | pending |
| 101 | `baking` | 9 | 532 | 363 | pending |
| 102 | `misc` | 9 | 609 | 337 | pending |
| 103 | `misc2` | 9 | 616 | 392 | pending |
| 104 | `procurement` | 9 | 563 | 332 | pending |
| 105 | `sales` | 9 | 629 | 362 | pending |
| 106 | `admin` | 8 | 539 | 321 | pending |
| 107 | `cleaning` | 8 | 551 | 382 | pending |
| 108 | `cognition` | 8 | 599 | 422 | pending |
| 109 | `decor` | 8 | 629 | 415 | pending |
| 110 | `library` | 8 | 442 | 247 | pending |
| 111 | `museum` | 8 | 496 | 267 | pending |
| 112 | `quality` | 8 | 507 | 321 | pending |
| 113 | `rental` | 8 | 464 | 281 | pending |
| 114 | `research` | 8 | 527 | 306 | pending |
| 115 | `restaurant` | 8 | 488 | 266 | pending |
| 116 | `telecom` | 8 | 476 | 290 | pending |
| 117 | `audio` | 7 | 512 | 378 | pending |
| 118 | `dance` | 7 | 560 | 377 | pending |
| 119 | `hotel` | 7 | 531 | 329 | pending |
| 120 | `printing` | 7 | 491 | 312 | pending |
| 121 | `woodwork` | 7 | 399 | 292 | pending |
| 122 | `archaeology` | 6 | 360 | 202 | pending |
| 123 | `chinese-cook` | 6 | 471 | 293 | pending |
| 124 | `exhibition` | 6 | 424 | 242 | pending |
| 125 | `film` | 6 | 360 | 236 | pending |
| 126 | `floral` | 6 | 472 | 352 | pending |
| 127 | `funeral` | 6 | 464 | 335 | pending |
| 128 | `home` | 6 | 350 | 211 | pending |
| 129 | `jewelry` | 6 | 430 | 273 | pending |
| 130 | `media` | 6 | 344 | 169 | pending |
| 131 | `office` | 6 | 341 | 264 | pending |
| 132 | `packaging` | 6 | 301 | 171 | pending |
| 133 | `parenting` | 6 | 270 | 164 | pending |
| 134 | `road` | 6 | 460 | 292 | pending |
| 135 | `startup` | 6 | 469 | 309 | pending |
| 136 | `urban` | 6 | 499 | 316 | pending |
| 137 | `video` | 6 | 486 | 311 | pending |
| 138 | `accessibility` | 5 | 347 | 210 | pending |
| 139 | `antiques` | 5 | 345 | 201 | pending |
| 140 | `aquaculture` | 5 | 299 | 189 | pending |
| 141 | `audit` | 5 | 359 | 214 | pending |
| 142 | `bonding` | 5 | 294 | 181 | pending |
| 143 | `bridge` | 5 | 393 | 246 | pending |
| 144 | `ceramics` | 5 | 387 | 247 | pending |
| 145 | `chess` | 5 | 427 | 320 | pending |
| 146 | `chinese` | 5 | 238 | 188 | pending |
| 147 | `edu2` | 5 | 292 | 189 | pending |
| 148 | `fengshui` | 5 | 408 | 300 | pending |
| 149 | `forex` | 5 | 416 | 250 | pending |
| 150 | `futures` | 5 | 411 | 254 | pending |
| 151 | `gardening2` | 5 | 365 | 263 | pending |
| 152 | `glass` | 5 | 364 | 204 | pending |
| 153 | `kids` | 5 | 334 | 198 | pending |
| 154 | `legal2` | 5 | 332 | 200 | pending |
| 155 | `logistics2` | 5 | 319 | 189 | pending |
| 156 | `manufacturing` | 5 | 279 | 154 | pending |
| 157 | `maritime` | 5 | 424 | 282 | pending |
| 158 | `martial` | 5 | 362 | 255 | pending |
| 159 | `medical2` | 5 | 333 | 206 | pending |
| 160 | `pet-training` | 5 | 364 | 263 | pending |
| 161 | `petrochem` | 5 | 355 | 230 | pending |
| 162 | `pets` | 5 | 333 | 229 | pending |
| 163 | `plastic` | 5 | 312 | 175 | pending |
| 164 | `project` | 5 | 403 | 194 | pending |
| 165 | `railway` | 5 | 124 | 80 | pending |
| 166 | `rubber` | 5 | 311 | 174 | pending |
| 167 | `seismology` | 5 | 306 | 195 | pending |
| 168 | `service` | 5 | 306 | 164 | pending |
| 169 | `shipping` | 5 | 311 | 202 | pending |
| 170 | `stage` | 5 | 324 | 186 | pending |
| 171 | `tunnel` | 5 | 373 | 221 | pending |
| 172 | `woodworking` | 5 | 413 | 297 | pending |
| 173 | `yi` | 5 | 370 | 242 | pending |
| 174 | `photo2` | 4 | 236 | 159 | pending |
| 175 | `stats` | 4 | 281 | 198 | pending |

