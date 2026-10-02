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
| 1 | `clinical-lab` | 25 | 1540 | 937 | pending |
| 2 | `clinical-nursing` | 25 | 1906 | 1220 | pending |
| 3 | `construction` | 25 | 1970 | 1231 | pending |
| 4 | `dentistry` | 25 | 1859 | 1120 | pending |
| 5 | `kinematics` | 25 | 809 | 502 | pending |
| 6 | `neurology` | 25 | 2674 | 1537 | pending |
| 7 | `rheumatology` | 25 | 2514 | 1447 | pending |
| 8 | `textile` | 25 | 1994 | 1100 | pending |
| 9 | `cardiology` | 24 | 1917 | 1181 | pending |
| 10 | `food` | 24 | 1772 | 927 | pending |
| 11 | `pediatrics` | 24 | 1865 | 999 | pending |
| 12 | `psychiatry` | 24 | 1565 | 722 | pending |
| 13 | `pulmonology` | 24 | 1832 | 1036 | pending |
| 14 | `urology` | 24 | 2148 | 1138 | pending |
| 15 | `acupuncture` | 23 | 1406 | 656 | pending |
| 16 | `astronomy` | 23 | 1340 | 867 | pending |
| 17 | `dynamics` | 23 | 715 | 464 | pending |
| 18 | `ecommerce` | 23 | 1412 | 661 | pending |
| 19 | `ent` | 23 | 1911 | 1044 | pending |
| 20 | `fluid` | 23 | 670 | 414 | pending |
| 21 | `investment` | 23 | 725 | 507 | pending |
| 22 | `nephrology` | 23 | 1853 | 1034 | pending |
| 23 | `dermatology` | 22 | 2081 | 1077 | pending |
| 24 | `gastroenterology` | 22 | 2114 | 1216 | pending |
| 25 | `rehabilitation` | 22 | 1930 | 1054 | pending |
| 26 | `tcm-chemistry` | 22 | 1690 | 955 | pending |
| 27 | `tcm-pharmacy` | 22 | 1542 | 884 | pending |
| 28 | `beauty` | 21 | 1438 | 852 | pending |
| 29 | `civil` | 21 | 741 | 547 | pending |
| 30 | `electronics` | 21 | 1327 | 723 | pending |
| 31 | `endocrinology` | 21 | 2016 | 1404 | pending |
| 32 | `food-processing` | 21 | 1230 | 518 | pending |
| 33 | `hr` | 21 | 1087 | 564 | pending |
| 34 | `optics` | 21 | 645 | 443 | pending |
| 35 | `property` | 21 | 1344 | 732 | pending |
| 36 | `tcm-diagnosis` | 21 | 2103 | 1170 | pending |
| 37 | `travel` | 21 | 1654 | 918 | pending |
| 38 | `forensic-medicine` | 20 | 2374 | 1597 | pending |
| 39 | `metallurgy` | 20 | 1236 | 646 | pending |
| 40 | `psychology` | 20 | 1057 | 622 | pending |
| 41 | `electrical` | 19 | 810 | 545 | pending |
| 42 | `forestry` | 19 | 1435 | 727 | pending |
| 43 | `language` | 19 | 1123 | 622 | pending |
| 44 | `music` | 19 | 1577 | 893 | pending |
| 45 | `nutrition` | 18 | 980 | 546 | pending |
| 46 | `data` | 17 | 906 | 405 | pending |
| 47 | `advertising` | 16 | 1007 | 520 | pending |
| 48 | `niche` | 16 | 1101 | 690 | pending |
| 49 | `leather` | 15 | 948 | 510 | pending |
| 50 | `logistics` | 15 | 807 | 478 | pending |
| 51 | `safety` | 15 | 838 | 503 | pending |
| 52 | `transport` | 15 | 682 | 495 | pending |
| 53 | `welding` | 15 | 1025 | 546 | pending |
| 54 | `engineering` | 14 | 495 | 324 | pending |
| 55 | `image` | 14 | 882 | 609 | pending |
| 56 | `mechanical` | 14 | 644 | 398 | pending |
| 57 | `medical` | 14 | 936 | 604 | pending |
| 58 | `dyeing` | 13 | 868 | 467 | pending |
| 59 | `gardening` | 12 | 866 | 455 | pending |
| 60 | `mining` | 12 | 768 | 468 | pending |
| 61 | `paper` | 12 | 778 | 399 | pending |
| 62 | `pr` | 12 | 900 | 530 | pending |
| 63 | `chemical` | 11 | 654 | 355 | pending |
| 64 | `elderly` | 11 | 691 | 469 | pending |
| 65 | `fire` | 11 | 774 | 461 | pending |
| 66 | `gas` | 11 | 718 | 380 | pending |
| 67 | `text` | 11 | 467 | 301 | pending |
| 68 | `usedcar` | 11 | 641 | 408 | pending |
| 69 | `hvac` | 10 | 908 | 668 | pending |
| 70 | `pet` | 10 | 657 | 446 | pending |
| 71 | `process` | 10 | 315 | 217 | pending |
| 72 | `security` | 10 | 755 | 532 | pending |
| 73 | `baking` | 9 | 532 | 363 | pending |
| 74 | `misc` | 9 | 609 | 337 | pending |
| 75 | `misc2` | 9 | 616 | 392 | pending |
| 76 | `procurement` | 9 | 563 | 332 | pending |
| 77 | `sales` | 9 | 629 | 362 | pending |
| 78 | `admin` | 8 | 539 | 321 | pending |
| 79 | `cleaning` | 8 | 551 | 382 | pending |
| 80 | `cognition` | 8 | 599 | 422 | pending |
| 81 | `decor` | 8 | 629 | 415 | pending |
| 82 | `library` | 8 | 442 | 247 | pending |
| 83 | `museum` | 8 | 496 | 267 | pending |
| 84 | `quality` | 8 | 507 | 321 | pending |
| 85 | `rental` | 8 | 464 | 281 | pending |
| 86 | `research` | 8 | 527 | 306 | pending |
| 87 | `restaurant` | 8 | 488 | 266 | pending |
| 88 | `telecom` | 8 | 476 | 290 | pending |
| 89 | `audio` | 7 | 512 | 378 | pending |
| 90 | `dance` | 7 | 560 | 377 | pending |
| 91 | `hotel` | 7 | 531 | 329 | pending |
| 92 | `printing` | 7 | 491 | 312 | pending |
| 93 | `woodwork` | 7 | 399 | 292 | pending |
| 94 | `archaeology` | 6 | 360 | 202 | pending |
| 95 | `chinese-cook` | 6 | 471 | 293 | pending |
| 96 | `exhibition` | 6 | 424 | 242 | pending |
| 97 | `film` | 6 | 360 | 236 | pending |
| 98 | `floral` | 6 | 472 | 352 | pending |
| 99 | `funeral` | 6 | 464 | 335 | pending |
| 100 | `home` | 6 | 350 | 211 | pending |
| 101 | `jewelry` | 6 | 430 | 273 | pending |
| 102 | `media` | 6 | 344 | 169 | pending |
| 103 | `office` | 6 | 341 | 264 | pending |
| 104 | `packaging` | 6 | 301 | 171 | pending |
| 105 | `parenting` | 6 | 270 | 164 | pending |
| 106 | `road` | 6 | 460 | 292 | pending |
| 107 | `startup` | 6 | 469 | 309 | pending |
| 108 | `urban` | 6 | 499 | 316 | pending |
| 109 | `video` | 6 | 486 | 311 | pending |
| 110 | `accessibility` | 5 | 347 | 210 | pending |
| 111 | `antiques` | 5 | 345 | 201 | pending |
| 112 | `aquaculture` | 5 | 299 | 189 | pending |
| 113 | `audit` | 5 | 359 | 214 | pending |
| 114 | `bonding` | 5 | 294 | 181 | pending |
| 115 | `bridge` | 5 | 393 | 246 | pending |
| 116 | `ceramics` | 5 | 387 | 247 | pending |
| 117 | `chess` | 5 | 427 | 320 | pending |
| 118 | `chinese` | 5 | 238 | 188 | pending |
| 119 | `edu2` | 5 | 292 | 189 | pending |
| 120 | `fengshui` | 5 | 408 | 300 | pending |
| 121 | `forex` | 5 | 416 | 250 | pending |
| 122 | `futures` | 5 | 411 | 254 | pending |
| 123 | `gardening2` | 5 | 365 | 263 | pending |
| 124 | `glass` | 5 | 364 | 204 | pending |
| 125 | `kids` | 5 | 334 | 198 | pending |
| 126 | `legal2` | 5 | 332 | 200 | pending |
| 127 | `logistics2` | 5 | 319 | 189 | pending |
| 128 | `manufacturing` | 5 | 279 | 154 | pending |
| 129 | `maritime` | 5 | 424 | 282 | pending |
| 130 | `martial` | 5 | 362 | 255 | pending |
| 131 | `medical2` | 5 | 333 | 206 | pending |
| 132 | `pet-training` | 5 | 364 | 263 | pending |
| 133 | `petrochem` | 5 | 355 | 230 | pending |
| 134 | `pets` | 5 | 333 | 229 | pending |
| 135 | `plastic` | 5 | 312 | 175 | pending |
| 136 | `project` | 5 | 403 | 194 | pending |
| 137 | `railway` | 5 | 124 | 80 | pending |
| 138 | `rubber` | 5 | 311 | 174 | pending |
| 139 | `seismology` | 5 | 306 | 195 | pending |
| 140 | `service` | 5 | 306 | 164 | pending |
| 141 | `shipping` | 5 | 311 | 202 | pending |
| 142 | `stage` | 5 | 324 | 186 | pending |
| 143 | `tunnel` | 5 | 373 | 221 | pending |
| 144 | `woodworking` | 5 | 413 | 297 | pending |
| 145 | `yi` | 5 | 370 | 242 | pending |
| 146 | `photo2` | 4 | 236 | 159 | pending |
| 147 | `stats` | 4 | 281 | 198 | pending |

