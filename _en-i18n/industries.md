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
| 1 | `kinematics` | 25 | 809 | 502 | pending |
| 2 | `neurology` | 25 | 2674 | 1537 | pending |
| 3 | `rheumatology` | 25 | 2514 | 1447 | pending |
| 4 | `textile` | 25 | 1994 | 1100 | pending |
| 5 | `cardiology` | 24 | 1917 | 1181 | pending |
| 6 | `food` | 24 | 1772 | 927 | pending |
| 7 | `pediatrics` | 24 | 1865 | 999 | pending |
| 8 | `psychiatry` | 24 | 1565 | 722 | pending |
| 9 | `pulmonology` | 24 | 1832 | 1036 | pending |
| 10 | `urology` | 24 | 2148 | 1138 | pending |
| 11 | `acupuncture` | 23 | 1406 | 656 | pending |
| 12 | `astronomy` | 23 | 1340 | 867 | pending |
| 13 | `dynamics` | 23 | 715 | 464 | pending |
| 14 | `ecommerce` | 23 | 1412 | 661 | pending |
| 15 | `ent` | 23 | 1911 | 1044 | pending |
| 16 | `fluid` | 23 | 670 | 414 | pending |
| 17 | `investment` | 23 | 725 | 507 | pending |
| 18 | `nephrology` | 23 | 1853 | 1034 | pending |
| 19 | `dermatology` | 22 | 2081 | 1077 | pending |
| 20 | `gastroenterology` | 22 | 2114 | 1216 | pending |
| 21 | `rehabilitation` | 22 | 1930 | 1054 | pending |
| 22 | `tcm-chemistry` | 22 | 1690 | 955 | pending |
| 23 | `tcm-pharmacy` | 22 | 1542 | 884 | pending |
| 24 | `beauty` | 21 | 1438 | 852 | pending |
| 25 | `civil` | 21 | 741 | 547 | pending |
| 26 | `electronics` | 21 | 1327 | 723 | pending |
| 27 | `endocrinology` | 21 | 2016 | 1404 | pending |
| 28 | `food-processing` | 21 | 1230 | 518 | pending |
| 29 | `hr` | 21 | 1087 | 564 | pending |
| 30 | `optics` | 21 | 645 | 443 | pending |
| 31 | `property` | 21 | 1344 | 732 | pending |
| 32 | `tcm-diagnosis` | 21 | 2103 | 1170 | pending |
| 33 | `travel` | 21 | 1654 | 918 | pending |
| 34 | `forensic-medicine` | 20 | 2374 | 1597 | pending |
| 35 | `metallurgy` | 20 | 1236 | 646 | pending |
| 36 | `psychology` | 20 | 1057 | 622 | pending |
| 37 | `electrical` | 19 | 810 | 545 | pending |
| 38 | `forestry` | 19 | 1435 | 727 | pending |
| 39 | `language` | 19 | 1123 | 622 | pending |
| 40 | `music` | 19 | 1577 | 893 | pending |
| 41 | `nutrition` | 18 | 980 | 546 | pending |
| 42 | `data` | 17 | 906 | 405 | pending |
| 43 | `advertising` | 16 | 1007 | 520 | pending |
| 44 | `niche` | 16 | 1101 | 690 | pending |
| 45 | `leather` | 15 | 948 | 510 | pending |
| 46 | `logistics` | 15 | 807 | 478 | pending |
| 47 | `safety` | 15 | 838 | 503 | pending |
| 48 | `transport` | 15 | 682 | 495 | pending |
| 49 | `welding` | 15 | 1025 | 546 | pending |
| 50 | `engineering` | 14 | 495 | 324 | pending |
| 51 | `image` | 14 | 882 | 609 | pending |
| 52 | `mechanical` | 14 | 644 | 398 | pending |
| 53 | `medical` | 14 | 936 | 604 | pending |
| 54 | `dyeing` | 13 | 868 | 467 | pending |
| 55 | `gardening` | 12 | 866 | 455 | pending |
| 56 | `mining` | 12 | 768 | 468 | pending |
| 57 | `paper` | 12 | 778 | 399 | pending |
| 58 | `pr` | 12 | 900 | 530 | pending |
| 59 | `chemical` | 11 | 654 | 355 | pending |
| 60 | `elderly` | 11 | 691 | 469 | pending |
| 61 | `fire` | 11 | 774 | 461 | pending |
| 62 | `gas` | 11 | 718 | 380 | pending |
| 63 | `text` | 11 | 467 | 301 | pending |
| 64 | `usedcar` | 11 | 641 | 408 | pending |
| 65 | `hvac` | 10 | 908 | 668 | pending |
| 66 | `pet` | 10 | 657 | 446 | pending |
| 67 | `process` | 10 | 315 | 217 | pending |
| 68 | `security` | 10 | 755 | 532 | pending |
| 69 | `baking` | 9 | 532 | 363 | pending |
| 70 | `misc` | 9 | 609 | 337 | pending |
| 71 | `misc2` | 9 | 616 | 392 | pending |
| 72 | `procurement` | 9 | 563 | 332 | pending |
| 73 | `sales` | 9 | 629 | 362 | pending |
| 74 | `admin` | 8 | 539 | 321 | pending |
| 75 | `cleaning` | 8 | 551 | 382 | pending |
| 76 | `cognition` | 8 | 599 | 422 | pending |
| 77 | `decor` | 8 | 629 | 415 | pending |
| 78 | `library` | 8 | 442 | 247 | pending |
| 79 | `museum` | 8 | 496 | 267 | pending |
| 80 | `quality` | 8 | 507 | 321 | pending |
| 81 | `rental` | 8 | 464 | 281 | pending |
| 82 | `research` | 8 | 527 | 306 | pending |
| 83 | `restaurant` | 8 | 488 | 266 | pending |
| 84 | `telecom` | 8 | 476 | 290 | pending |
| 85 | `audio` | 7 | 512 | 378 | pending |
| 86 | `dance` | 7 | 560 | 377 | pending |
| 87 | `hotel` | 7 | 531 | 329 | pending |
| 88 | `printing` | 7 | 491 | 312 | pending |
| 89 | `woodwork` | 7 | 399 | 292 | pending |
| 90 | `archaeology` | 6 | 360 | 202 | pending |
| 91 | `chinese-cook` | 6 | 471 | 293 | pending |
| 92 | `exhibition` | 6 | 424 | 242 | pending |
| 93 | `film` | 6 | 360 | 236 | pending |
| 94 | `floral` | 6 | 472 | 352 | pending |
| 95 | `funeral` | 6 | 464 | 335 | pending |
| 96 | `home` | 6 | 350 | 211 | pending |
| 97 | `jewelry` | 6 | 430 | 273 | pending |
| 98 | `media` | 6 | 344 | 169 | pending |
| 99 | `office` | 6 | 341 | 264 | pending |
| 100 | `packaging` | 6 | 301 | 171 | pending |
| 101 | `parenting` | 6 | 270 | 164 | pending |
| 102 | `road` | 6 | 460 | 292 | pending |
| 103 | `startup` | 6 | 469 | 309 | pending |
| 104 | `urban` | 6 | 499 | 316 | pending |
| 105 | `video` | 6 | 486 | 311 | pending |
| 106 | `accessibility` | 5 | 347 | 210 | pending |
| 107 | `antiques` | 5 | 345 | 201 | pending |
| 108 | `aquaculture` | 5 | 299 | 189 | pending |
| 109 | `audit` | 5 | 359 | 214 | pending |
| 110 | `bonding` | 5 | 294 | 181 | pending |
| 111 | `bridge` | 5 | 393 | 246 | pending |
| 112 | `ceramics` | 5 | 387 | 247 | pending |
| 113 | `chess` | 5 | 427 | 320 | pending |
| 114 | `chinese` | 5 | 238 | 188 | pending |
| 115 | `edu2` | 5 | 292 | 189 | pending |
| 116 | `fengshui` | 5 | 408 | 300 | pending |
| 117 | `forex` | 5 | 416 | 250 | pending |
| 118 | `futures` | 5 | 411 | 254 | pending |
| 119 | `gardening2` | 5 | 365 | 263 | pending |
| 120 | `glass` | 5 | 364 | 204 | pending |
| 121 | `kids` | 5 | 334 | 198 | pending |
| 122 | `legal2` | 5 | 332 | 200 | pending |
| 123 | `logistics2` | 5 | 319 | 189 | pending |
| 124 | `manufacturing` | 5 | 279 | 154 | pending |
| 125 | `maritime` | 5 | 424 | 282 | pending |
| 126 | `martial` | 5 | 362 | 255 | pending |
| 127 | `medical2` | 5 | 333 | 206 | pending |
| 128 | `pet-training` | 5 | 364 | 263 | pending |
| 129 | `petrochem` | 5 | 355 | 230 | pending |
| 130 | `pets` | 5 | 333 | 229 | pending |
| 131 | `plastic` | 5 | 312 | 175 | pending |
| 132 | `project` | 5 | 403 | 194 | pending |
| 133 | `railway` | 5 | 124 | 80 | pending |
| 134 | `rubber` | 5 | 311 | 174 | pending |
| 135 | `seismology` | 5 | 306 | 195 | pending |
| 136 | `service` | 5 | 306 | 164 | pending |
| 137 | `shipping` | 5 | 311 | 202 | pending |
| 138 | `stage` | 5 | 324 | 186 | pending |
| 139 | `tunnel` | 5 | 373 | 221 | pending |
| 140 | `woodworking` | 5 | 413 | 297 | pending |
| 141 | `yi` | 5 | 370 | 242 | pending |
| 142 | `photo2` | 4 | 236 | 159 | pending |
| 143 | `stats` | 4 | 281 | 198 | pending |

