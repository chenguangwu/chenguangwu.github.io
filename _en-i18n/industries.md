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
| 1 | `dermatology` | 22 | 2081 | 1077 | pending |
| 2 | `gastroenterology` | 22 | 2114 | 1216 | pending |
| 3 | `rehabilitation` | 22 | 1930 | 1054 | pending |
| 4 | `tcm-chemistry` | 22 | 1690 | 955 | pending |
| 5 | `tcm-pharmacy` | 22 | 1542 | 884 | pending |
| 6 | `beauty` | 21 | 1438 | 852 | pending |
| 7 | `civil` | 21 | 741 | 547 | pending |
| 8 | `electronics` | 21 | 1327 | 723 | pending |
| 9 | `endocrinology` | 21 | 2016 | 1404 | pending |
| 10 | `food-processing` | 21 | 1230 | 518 | pending |
| 11 | `hr` | 21 | 1087 | 564 | pending |
| 12 | `optics` | 21 | 645 | 443 | pending |
| 13 | `property` | 21 | 1344 | 732 | pending |
| 14 | `tcm-diagnosis` | 21 | 2103 | 1170 | pending |
| 15 | `travel` | 21 | 1654 | 918 | pending |
| 16 | `forensic-medicine` | 20 | 2374 | 1597 | pending |
| 17 | `metallurgy` | 20 | 1236 | 646 | pending |
| 18 | `psychology` | 20 | 1057 | 622 | pending |
| 19 | `electrical` | 19 | 810 | 545 | pending |
| 20 | `forestry` | 19 | 1435 | 727 | pending |
| 21 | `language` | 19 | 1123 | 622 | pending |
| 22 | `music` | 19 | 1577 | 893 | pending |
| 23 | `nutrition` | 18 | 980 | 546 | pending |
| 24 | `data` | 17 | 906 | 405 | pending |
| 25 | `advertising` | 16 | 1007 | 520 | pending |
| 26 | `niche` | 16 | 1101 | 690 | pending |
| 27 | `leather` | 15 | 948 | 510 | pending |
| 28 | `logistics` | 15 | 807 | 478 | pending |
| 29 | `safety` | 15 | 838 | 503 | pending |
| 30 | `transport` | 15 | 682 | 495 | pending |
| 31 | `welding` | 15 | 1025 | 546 | pending |
| 32 | `engineering` | 14 | 495 | 324 | pending |
| 33 | `image` | 14 | 882 | 609 | pending |
| 34 | `mechanical` | 14 | 644 | 398 | pending |
| 35 | `medical` | 14 | 936 | 604 | pending |
| 36 | `dyeing` | 13 | 868 | 467 | pending |
| 37 | `gardening` | 12 | 866 | 455 | pending |
| 38 | `mining` | 12 | 768 | 468 | pending |
| 39 | `paper` | 12 | 778 | 399 | pending |
| 40 | `pr` | 12 | 900 | 530 | pending |
| 41 | `chemical` | 11 | 654 | 355 | pending |
| 42 | `elderly` | 11 | 691 | 469 | pending |
| 43 | `fire` | 11 | 774 | 461 | pending |
| 44 | `gas` | 11 | 718 | 380 | pending |
| 45 | `text` | 11 | 467 | 301 | pending |
| 46 | `usedcar` | 11 | 641 | 408 | pending |
| 47 | `hvac` | 10 | 908 | 668 | pending |
| 48 | `pet` | 10 | 657 | 446 | pending |
| 49 | `process` | 10 | 315 | 217 | pending |
| 50 | `security` | 10 | 755 | 532 | pending |
| 51 | `baking` | 9 | 532 | 363 | pending |
| 52 | `misc` | 9 | 609 | 337 | pending |
| 53 | `misc2` | 9 | 616 | 392 | pending |
| 54 | `procurement` | 9 | 563 | 332 | pending |
| 55 | `sales` | 9 | 629 | 362 | pending |
| 56 | `admin` | 8 | 539 | 321 | pending |
| 57 | `cleaning` | 8 | 551 | 382 | pending |
| 58 | `cognition` | 8 | 599 | 422 | pending |
| 59 | `decor` | 8 | 629 | 415 | pending |
| 60 | `library` | 8 | 442 | 247 | pending |
| 61 | `museum` | 8 | 496 | 267 | pending |
| 62 | `quality` | 8 | 507 | 321 | pending |
| 63 | `rental` | 8 | 464 | 281 | pending |
| 64 | `research` | 8 | 527 | 306 | pending |
| 65 | `restaurant` | 8 | 488 | 266 | pending |
| 66 | `telecom` | 8 | 476 | 290 | pending |
| 67 | `audio` | 7 | 512 | 378 | pending |
| 68 | `dance` | 7 | 560 | 377 | pending |
| 69 | `hotel` | 7 | 531 | 329 | pending |
| 70 | `printing` | 7 | 491 | 312 | pending |
| 71 | `woodwork` | 7 | 399 | 292 | pending |
| 72 | `archaeology` | 6 | 360 | 202 | pending |
| 73 | `chinese-cook` | 6 | 471 | 293 | pending |
| 74 | `exhibition` | 6 | 424 | 242 | pending |
| 75 | `film` | 6 | 360 | 236 | pending |
| 76 | `floral` | 6 | 472 | 352 | pending |
| 77 | `funeral` | 6 | 464 | 335 | pending |
| 78 | `home` | 6 | 350 | 211 | pending |
| 79 | `jewelry` | 6 | 430 | 273 | pending |
| 80 | `media` | 6 | 344 | 169 | pending |
| 81 | `office` | 6 | 341 | 264 | pending |
| 82 | `packaging` | 6 | 301 | 171 | pending |
| 83 | `parenting` | 6 | 270 | 164 | pending |
| 84 | `road` | 6 | 460 | 292 | pending |
| 85 | `startup` | 6 | 469 | 309 | pending |
| 86 | `urban` | 6 | 499 | 316 | pending |
| 87 | `video` | 6 | 486 | 311 | pending |
| 88 | `accessibility` | 5 | 347 | 210 | pending |
| 89 | `antiques` | 5 | 345 | 201 | pending |
| 90 | `aquaculture` | 5 | 299 | 189 | pending |
| 91 | `audit` | 5 | 359 | 214 | pending |
| 92 | `bonding` | 5 | 294 | 181 | pending |
| 93 | `bridge` | 5 | 393 | 246 | pending |
| 94 | `ceramics` | 5 | 387 | 247 | pending |
| 95 | `chess` | 5 | 427 | 320 | pending |
| 96 | `chinese` | 5 | 238 | 188 | pending |
| 97 | `edu2` | 5 | 292 | 189 | pending |
| 98 | `fengshui` | 5 | 408 | 300 | pending |
| 99 | `forex` | 5 | 416 | 250 | pending |
| 100 | `futures` | 5 | 411 | 254 | pending |
| 101 | `gardening2` | 5 | 365 | 263 | pending |
| 102 | `glass` | 5 | 364 | 204 | pending |
| 103 | `kids` | 5 | 334 | 198 | pending |
| 104 | `legal2` | 5 | 332 | 200 | pending |
| 105 | `logistics2` | 5 | 319 | 189 | pending |
| 106 | `manufacturing` | 5 | 279 | 154 | pending |
| 107 | `maritime` | 5 | 424 | 282 | pending |
| 108 | `martial` | 5 | 362 | 255 | pending |
| 109 | `medical2` | 5 | 333 | 206 | pending |
| 110 | `pet-training` | 5 | 364 | 263 | pending |
| 111 | `petrochem` | 5 | 355 | 230 | pending |
| 112 | `pets` | 5 | 333 | 229 | pending |
| 113 | `plastic` | 5 | 312 | 175 | pending |
| 114 | `project` | 5 | 403 | 194 | pending |
| 115 | `railway` | 5 | 124 | 80 | pending |
| 116 | `rubber` | 5 | 311 | 174 | pending |
| 117 | `seismology` | 5 | 306 | 195 | pending |
| 118 | `service` | 5 | 306 | 164 | pending |
| 119 | `shipping` | 5 | 311 | 202 | pending |
| 120 | `stage` | 5 | 324 | 186 | pending |
| 121 | `tunnel` | 5 | 373 | 221 | pending |
| 122 | `woodworking` | 5 | 413 | 297 | pending |
| 123 | `yi` | 5 | 370 | 242 | pending |
| 124 | `photo2` | 4 | 236 | 159 | pending |
| 125 | `stats` | 4 | 281 | 198 | pending |

