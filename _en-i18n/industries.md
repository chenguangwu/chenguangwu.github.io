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
| 1 | `clinical-nursing` | 25 | 1906 | 1220 | pending |
| 2 | `construction` | 25 | 1970 | 1231 | pending |
| 3 | `dentistry` | 25 | 1859 | 1120 | pending |
| 4 | `kinematics` | 25 | 809 | 502 | pending |
| 5 | `neurology` | 25 | 2674 | 1537 | pending |
| 6 | `rheumatology` | 25 | 2514 | 1447 | pending |
| 7 | `textile` | 25 | 1994 | 1100 | pending |
| 8 | `cardiology` | 24 | 1917 | 1181 | pending |
| 9 | `food` | 24 | 1772 | 927 | pending |
| 10 | `pediatrics` | 24 | 1865 | 999 | pending |
| 11 | `psychiatry` | 24 | 1565 | 722 | pending |
| 12 | `pulmonology` | 24 | 1832 | 1036 | pending |
| 13 | `urology` | 24 | 2148 | 1138 | pending |
| 14 | `acupuncture` | 23 | 1406 | 656 | pending |
| 15 | `astronomy` | 23 | 1340 | 867 | pending |
| 16 | `dynamics` | 23 | 715 | 464 | pending |
| 17 | `ecommerce` | 23 | 1412 | 661 | pending |
| 18 | `ent` | 23 | 1911 | 1044 | pending |
| 19 | `fluid` | 23 | 670 | 414 | pending |
| 20 | `investment` | 23 | 725 | 507 | pending |
| 21 | `nephrology` | 23 | 1853 | 1034 | pending |
| 22 | `dermatology` | 22 | 2081 | 1077 | pending |
| 23 | `gastroenterology` | 22 | 2114 | 1216 | pending |
| 24 | `rehabilitation` | 22 | 1930 | 1054 | pending |
| 25 | `tcm-chemistry` | 22 | 1690 | 955 | pending |
| 26 | `tcm-pharmacy` | 22 | 1542 | 884 | pending |
| 27 | `beauty` | 21 | 1438 | 852 | pending |
| 28 | `civil` | 21 | 741 | 547 | pending |
| 29 | `electronics` | 21 | 1327 | 723 | pending |
| 30 | `endocrinology` | 21 | 2016 | 1404 | pending |
| 31 | `food-processing` | 21 | 1230 | 518 | pending |
| 32 | `hr` | 21 | 1087 | 564 | pending |
| 33 | `optics` | 21 | 645 | 443 | pending |
| 34 | `property` | 21 | 1344 | 732 | pending |
| 35 | `tcm-diagnosis` | 21 | 2103 | 1170 | pending |
| 36 | `travel` | 21 | 1654 | 918 | pending |
| 37 | `forensic-medicine` | 20 | 2374 | 1597 | pending |
| 38 | `metallurgy` | 20 | 1236 | 646 | pending |
| 39 | `psychology` | 20 | 1057 | 622 | pending |
| 40 | `electrical` | 19 | 810 | 545 | pending |
| 41 | `forestry` | 19 | 1435 | 727 | pending |
| 42 | `language` | 19 | 1123 | 622 | pending |
| 43 | `music` | 19 | 1577 | 893 | pending |
| 44 | `nutrition` | 18 | 980 | 546 | pending |
| 45 | `data` | 17 | 906 | 405 | pending |
| 46 | `advertising` | 16 | 1007 | 520 | pending |
| 47 | `niche` | 16 | 1101 | 690 | pending |
| 48 | `leather` | 15 | 948 | 510 | pending |
| 49 | `logistics` | 15 | 807 | 478 | pending |
| 50 | `safety` | 15 | 838 | 503 | pending |
| 51 | `transport` | 15 | 682 | 495 | pending |
| 52 | `welding` | 15 | 1025 | 546 | pending |
| 53 | `engineering` | 14 | 495 | 324 | pending |
| 54 | `image` | 14 | 882 | 609 | pending |
| 55 | `mechanical` | 14 | 644 | 398 | pending |
| 56 | `medical` | 14 | 936 | 604 | pending |
| 57 | `dyeing` | 13 | 868 | 467 | pending |
| 58 | `gardening` | 12 | 866 | 455 | pending |
| 59 | `mining` | 12 | 768 | 468 | pending |
| 60 | `paper` | 12 | 778 | 399 | pending |
| 61 | `pr` | 12 | 900 | 530 | pending |
| 62 | `chemical` | 11 | 654 | 355 | pending |
| 63 | `elderly` | 11 | 691 | 469 | pending |
| 64 | `fire` | 11 | 774 | 461 | pending |
| 65 | `gas` | 11 | 718 | 380 | pending |
| 66 | `text` | 11 | 467 | 301 | pending |
| 67 | `usedcar` | 11 | 641 | 408 | pending |
| 68 | `hvac` | 10 | 908 | 668 | pending |
| 69 | `pet` | 10 | 657 | 446 | pending |
| 70 | `process` | 10 | 315 | 217 | pending |
| 71 | `security` | 10 | 755 | 532 | pending |
| 72 | `baking` | 9 | 532 | 363 | pending |
| 73 | `misc` | 9 | 609 | 337 | pending |
| 74 | `misc2` | 9 | 616 | 392 | pending |
| 75 | `procurement` | 9 | 563 | 332 | pending |
| 76 | `sales` | 9 | 629 | 362 | pending |
| 77 | `admin` | 8 | 539 | 321 | pending |
| 78 | `cleaning` | 8 | 551 | 382 | pending |
| 79 | `cognition` | 8 | 599 | 422 | pending |
| 80 | `decor` | 8 | 629 | 415 | pending |
| 81 | `library` | 8 | 442 | 247 | pending |
| 82 | `museum` | 8 | 496 | 267 | pending |
| 83 | `quality` | 8 | 507 | 321 | pending |
| 84 | `rental` | 8 | 464 | 281 | pending |
| 85 | `research` | 8 | 527 | 306 | pending |
| 86 | `restaurant` | 8 | 488 | 266 | pending |
| 87 | `telecom` | 8 | 476 | 290 | pending |
| 88 | `audio` | 7 | 512 | 378 | pending |
| 89 | `dance` | 7 | 560 | 377 | pending |
| 90 | `hotel` | 7 | 531 | 329 | pending |
| 91 | `printing` | 7 | 491 | 312 | pending |
| 92 | `woodwork` | 7 | 399 | 292 | pending |
| 93 | `archaeology` | 6 | 360 | 202 | pending |
| 94 | `chinese-cook` | 6 | 471 | 293 | pending |
| 95 | `exhibition` | 6 | 424 | 242 | pending |
| 96 | `film` | 6 | 360 | 236 | pending |
| 97 | `floral` | 6 | 472 | 352 | pending |
| 98 | `funeral` | 6 | 464 | 335 | pending |
| 99 | `home` | 6 | 350 | 211 | pending |
| 100 | `jewelry` | 6 | 430 | 273 | pending |
| 101 | `media` | 6 | 344 | 169 | pending |
| 102 | `office` | 6 | 341 | 264 | pending |
| 103 | `packaging` | 6 | 301 | 171 | pending |
| 104 | `parenting` | 6 | 270 | 164 | pending |
| 105 | `road` | 6 | 460 | 292 | pending |
| 106 | `startup` | 6 | 469 | 309 | pending |
| 107 | `urban` | 6 | 499 | 316 | pending |
| 108 | `video` | 6 | 486 | 311 | pending |
| 109 | `accessibility` | 5 | 347 | 210 | pending |
| 110 | `antiques` | 5 | 345 | 201 | pending |
| 111 | `aquaculture` | 5 | 299 | 189 | pending |
| 112 | `audit` | 5 | 359 | 214 | pending |
| 113 | `bonding` | 5 | 294 | 181 | pending |
| 114 | `bridge` | 5 | 393 | 246 | pending |
| 115 | `ceramics` | 5 | 387 | 247 | pending |
| 116 | `chess` | 5 | 427 | 320 | pending |
| 117 | `chinese` | 5 | 238 | 188 | pending |
| 118 | `edu2` | 5 | 292 | 189 | pending |
| 119 | `fengshui` | 5 | 408 | 300 | pending |
| 120 | `forex` | 5 | 416 | 250 | pending |
| 121 | `futures` | 5 | 411 | 254 | pending |
| 122 | `gardening2` | 5 | 365 | 263 | pending |
| 123 | `glass` | 5 | 364 | 204 | pending |
| 124 | `kids` | 5 | 334 | 198 | pending |
| 125 | `legal2` | 5 | 332 | 200 | pending |
| 126 | `logistics2` | 5 | 319 | 189 | pending |
| 127 | `manufacturing` | 5 | 279 | 154 | pending |
| 128 | `maritime` | 5 | 424 | 282 | pending |
| 129 | `martial` | 5 | 362 | 255 | pending |
| 130 | `medical2` | 5 | 333 | 206 | pending |
| 131 | `pet-training` | 5 | 364 | 263 | pending |
| 132 | `petrochem` | 5 | 355 | 230 | pending |
| 133 | `pets` | 5 | 333 | 229 | pending |
| 134 | `plastic` | 5 | 312 | 175 | pending |
| 135 | `project` | 5 | 403 | 194 | pending |
| 136 | `railway` | 5 | 124 | 80 | pending |
| 137 | `rubber` | 5 | 311 | 174 | pending |
| 138 | `seismology` | 5 | 306 | 195 | pending |
| 139 | `service` | 5 | 306 | 164 | pending |
| 140 | `shipping` | 5 | 311 | 202 | pending |
| 141 | `stage` | 5 | 324 | 186 | pending |
| 142 | `tunnel` | 5 | 373 | 221 | pending |
| 143 | `woodworking` | 5 | 413 | 297 | pending |
| 144 | `yi` | 5 | 370 | 242 | pending |
| 145 | `photo2` | 4 | 236 | 159 | pending |
| 146 | `stats` | 4 | 281 | 198 | pending |

