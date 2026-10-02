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
| 1 | `psychiatry` | 24 | 1565 | 722 | pending |
| 2 | `pulmonology` | 24 | 1832 | 1036 | pending |
| 3 | `urology` | 24 | 2148 | 1138 | pending |
| 4 | `acupuncture` | 23 | 1406 | 656 | pending |
| 5 | `astronomy` | 23 | 1340 | 867 | pending |
| 6 | `dynamics` | 23 | 715 | 464 | pending |
| 7 | `ecommerce` | 23 | 1412 | 661 | pending |
| 8 | `ent` | 23 | 1911 | 1044 | pending |
| 9 | `fluid` | 23 | 670 | 414 | pending |
| 10 | `investment` | 23 | 725 | 507 | pending |
| 11 | `nephrology` | 23 | 1853 | 1034 | pending |
| 12 | `dermatology` | 22 | 2081 | 1077 | pending |
| 13 | `gastroenterology` | 22 | 2114 | 1216 | pending |
| 14 | `rehabilitation` | 22 | 1930 | 1054 | pending |
| 15 | `tcm-chemistry` | 22 | 1690 | 955 | pending |
| 16 | `tcm-pharmacy` | 22 | 1542 | 884 | pending |
| 17 | `beauty` | 21 | 1438 | 852 | pending |
| 18 | `civil` | 21 | 741 | 547 | pending |
| 19 | `electronics` | 21 | 1327 | 723 | pending |
| 20 | `endocrinology` | 21 | 2016 | 1404 | pending |
| 21 | `food-processing` | 21 | 1230 | 518 | pending |
| 22 | `hr` | 21 | 1087 | 564 | pending |
| 23 | `optics` | 21 | 645 | 443 | pending |
| 24 | `property` | 21 | 1344 | 732 | pending |
| 25 | `tcm-diagnosis` | 21 | 2103 | 1170 | pending |
| 26 | `travel` | 21 | 1654 | 918 | pending |
| 27 | `forensic-medicine` | 20 | 2374 | 1597 | pending |
| 28 | `metallurgy` | 20 | 1236 | 646 | pending |
| 29 | `psychology` | 20 | 1057 | 622 | pending |
| 30 | `electrical` | 19 | 810 | 545 | pending |
| 31 | `forestry` | 19 | 1435 | 727 | pending |
| 32 | `language` | 19 | 1123 | 622 | pending |
| 33 | `music` | 19 | 1577 | 893 | pending |
| 34 | `nutrition` | 18 | 980 | 546 | pending |
| 35 | `data` | 17 | 906 | 405 | pending |
| 36 | `advertising` | 16 | 1007 | 520 | pending |
| 37 | `niche` | 16 | 1101 | 690 | pending |
| 38 | `leather` | 15 | 948 | 510 | pending |
| 39 | `logistics` | 15 | 807 | 478 | pending |
| 40 | `safety` | 15 | 838 | 503 | pending |
| 41 | `transport` | 15 | 682 | 495 | pending |
| 42 | `welding` | 15 | 1025 | 546 | pending |
| 43 | `engineering` | 14 | 495 | 324 | pending |
| 44 | `image` | 14 | 882 | 609 | pending |
| 45 | `mechanical` | 14 | 644 | 398 | pending |
| 46 | `medical` | 14 | 936 | 604 | pending |
| 47 | `dyeing` | 13 | 868 | 467 | pending |
| 48 | `gardening` | 12 | 866 | 455 | pending |
| 49 | `mining` | 12 | 768 | 468 | pending |
| 50 | `paper` | 12 | 778 | 399 | pending |
| 51 | `pr` | 12 | 900 | 530 | pending |
| 52 | `chemical` | 11 | 654 | 355 | pending |
| 53 | `elderly` | 11 | 691 | 469 | pending |
| 54 | `fire` | 11 | 774 | 461 | pending |
| 55 | `gas` | 11 | 718 | 380 | pending |
| 56 | `text` | 11 | 467 | 301 | pending |
| 57 | `usedcar` | 11 | 641 | 408 | pending |
| 58 | `hvac` | 10 | 908 | 668 | pending |
| 59 | `pet` | 10 | 657 | 446 | pending |
| 60 | `process` | 10 | 315 | 217 | pending |
| 61 | `security` | 10 | 755 | 532 | pending |
| 62 | `baking` | 9 | 532 | 363 | pending |
| 63 | `misc` | 9 | 609 | 337 | pending |
| 64 | `misc2` | 9 | 616 | 392 | pending |
| 65 | `procurement` | 9 | 563 | 332 | pending |
| 66 | `sales` | 9 | 629 | 362 | pending |
| 67 | `admin` | 8 | 539 | 321 | pending |
| 68 | `cleaning` | 8 | 551 | 382 | pending |
| 69 | `cognition` | 8 | 599 | 422 | pending |
| 70 | `decor` | 8 | 629 | 415 | pending |
| 71 | `library` | 8 | 442 | 247 | pending |
| 72 | `museum` | 8 | 496 | 267 | pending |
| 73 | `quality` | 8 | 507 | 321 | pending |
| 74 | `rental` | 8 | 464 | 281 | pending |
| 75 | `research` | 8 | 527 | 306 | pending |
| 76 | `restaurant` | 8 | 488 | 266 | pending |
| 77 | `telecom` | 8 | 476 | 290 | pending |
| 78 | `audio` | 7 | 512 | 378 | pending |
| 79 | `dance` | 7 | 560 | 377 | pending |
| 80 | `hotel` | 7 | 531 | 329 | pending |
| 81 | `printing` | 7 | 491 | 312 | pending |
| 82 | `woodwork` | 7 | 399 | 292 | pending |
| 83 | `archaeology` | 6 | 360 | 202 | pending |
| 84 | `chinese-cook` | 6 | 471 | 293 | pending |
| 85 | `exhibition` | 6 | 424 | 242 | pending |
| 86 | `film` | 6 | 360 | 236 | pending |
| 87 | `floral` | 6 | 472 | 352 | pending |
| 88 | `funeral` | 6 | 464 | 335 | pending |
| 89 | `home` | 6 | 350 | 211 | pending |
| 90 | `jewelry` | 6 | 430 | 273 | pending |
| 91 | `media` | 6 | 344 | 169 | pending |
| 92 | `office` | 6 | 341 | 264 | pending |
| 93 | `packaging` | 6 | 301 | 171 | pending |
| 94 | `parenting` | 6 | 270 | 164 | pending |
| 95 | `road` | 6 | 460 | 292 | pending |
| 96 | `startup` | 6 | 469 | 309 | pending |
| 97 | `urban` | 6 | 499 | 316 | pending |
| 98 | `video` | 6 | 486 | 311 | pending |
| 99 | `accessibility` | 5 | 347 | 210 | pending |
| 100 | `antiques` | 5 | 345 | 201 | pending |
| 101 | `aquaculture` | 5 | 299 | 189 | pending |
| 102 | `audit` | 5 | 359 | 214 | pending |
| 103 | `bonding` | 5 | 294 | 181 | pending |
| 104 | `bridge` | 5 | 393 | 246 | pending |
| 105 | `ceramics` | 5 | 387 | 247 | pending |
| 106 | `chess` | 5 | 427 | 320 | pending |
| 107 | `chinese` | 5 | 238 | 188 | pending |
| 108 | `edu2` | 5 | 292 | 189 | pending |
| 109 | `fengshui` | 5 | 408 | 300 | pending |
| 110 | `forex` | 5 | 416 | 250 | pending |
| 111 | `futures` | 5 | 411 | 254 | pending |
| 112 | `gardening2` | 5 | 365 | 263 | pending |
| 113 | `glass` | 5 | 364 | 204 | pending |
| 114 | `kids` | 5 | 334 | 198 | pending |
| 115 | `legal2` | 5 | 332 | 200 | pending |
| 116 | `logistics2` | 5 | 319 | 189 | pending |
| 117 | `manufacturing` | 5 | 279 | 154 | pending |
| 118 | `maritime` | 5 | 424 | 282 | pending |
| 119 | `martial` | 5 | 362 | 255 | pending |
| 120 | `medical2` | 5 | 333 | 206 | pending |
| 121 | `pet-training` | 5 | 364 | 263 | pending |
| 122 | `petrochem` | 5 | 355 | 230 | pending |
| 123 | `pets` | 5 | 333 | 229 | pending |
| 124 | `plastic` | 5 | 312 | 175 | pending |
| 125 | `project` | 5 | 403 | 194 | pending |
| 126 | `railway` | 5 | 124 | 80 | pending |
| 127 | `rubber` | 5 | 311 | 174 | pending |
| 128 | `seismology` | 5 | 306 | 195 | pending |
| 129 | `service` | 5 | 306 | 164 | pending |
| 130 | `shipping` | 5 | 311 | 202 | pending |
| 131 | `stage` | 5 | 324 | 186 | pending |
| 132 | `tunnel` | 5 | 373 | 221 | pending |
| 133 | `woodworking` | 5 | 413 | 297 | pending |
| 134 | `yi` | 5 | 370 | 242 | pending |
| 135 | `photo2` | 4 | 236 | 159 | pending |
| 136 | `stats` | 4 | 281 | 198 | pending |

