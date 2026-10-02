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
| 1 | `gastroenterology` | 22 | 2114 | 1216 | pending |
| 2 | `rehabilitation` | 22 | 1930 | 1054 | pending |
| 3 | `tcm-chemistry` | 22 | 1690 | 955 | pending |
| 4 | `tcm-pharmacy` | 22 | 1542 | 884 | pending |
| 5 | `beauty` | 21 | 1438 | 852 | pending |
| 6 | `civil` | 21 | 741 | 547 | pending |
| 7 | `electronics` | 21 | 1327 | 723 | pending |
| 8 | `endocrinology` | 21 | 2016 | 1404 | pending |
| 9 | `food-processing` | 21 | 1230 | 518 | pending |
| 10 | `hr` | 21 | 1087 | 564 | pending |
| 11 | `optics` | 21 | 645 | 443 | pending |
| 12 | `property` | 21 | 1344 | 732 | pending |
| 13 | `tcm-diagnosis` | 21 | 2103 | 1170 | pending |
| 14 | `travel` | 21 | 1654 | 918 | pending |
| 15 | `forensic-medicine` | 20 | 2374 | 1597 | pending |
| 16 | `metallurgy` | 20 | 1236 | 646 | pending |
| 17 | `psychology` | 20 | 1057 | 622 | pending |
| 18 | `electrical` | 19 | 810 | 545 | pending |
| 19 | `forestry` | 19 | 1435 | 727 | pending |
| 20 | `language` | 19 | 1123 | 622 | pending |
| 21 | `music` | 19 | 1577 | 893 | pending |
| 22 | `nutrition` | 18 | 980 | 546 | pending |
| 23 | `data` | 17 | 906 | 405 | pending |
| 24 | `advertising` | 16 | 1007 | 520 | pending |
| 25 | `niche` | 16 | 1101 | 690 | pending |
| 26 | `leather` | 15 | 948 | 510 | pending |
| 27 | `logistics` | 15 | 807 | 478 | pending |
| 28 | `safety` | 15 | 838 | 503 | pending |
| 29 | `transport` | 15 | 682 | 495 | pending |
| 30 | `welding` | 15 | 1025 | 546 | pending |
| 31 | `engineering` | 14 | 495 | 324 | pending |
| 32 | `image` | 14 | 882 | 609 | pending |
| 33 | `mechanical` | 14 | 644 | 398 | pending |
| 34 | `medical` | 14 | 936 | 604 | pending |
| 35 | `dyeing` | 13 | 868 | 467 | pending |
| 36 | `gardening` | 12 | 866 | 455 | pending |
| 37 | `mining` | 12 | 768 | 468 | pending |
| 38 | `paper` | 12 | 778 | 399 | pending |
| 39 | `pr` | 12 | 900 | 530 | pending |
| 40 | `chemical` | 11 | 654 | 355 | pending |
| 41 | `elderly` | 11 | 691 | 469 | pending |
| 42 | `fire` | 11 | 774 | 461 | pending |
| 43 | `gas` | 11 | 718 | 380 | pending |
| 44 | `text` | 11 | 467 | 301 | pending |
| 45 | `usedcar` | 11 | 641 | 408 | pending |
| 46 | `hvac` | 10 | 908 | 668 | pending |
| 47 | `pet` | 10 | 657 | 446 | pending |
| 48 | `process` | 10 | 315 | 217 | pending |
| 49 | `security` | 10 | 755 | 532 | pending |
| 50 | `baking` | 9 | 532 | 363 | pending |
| 51 | `misc` | 9 | 609 | 337 | pending |
| 52 | `misc2` | 9 | 616 | 392 | pending |
| 53 | `procurement` | 9 | 563 | 332 | pending |
| 54 | `sales` | 9 | 629 | 362 | pending |
| 55 | `admin` | 8 | 539 | 321 | pending |
| 56 | `cleaning` | 8 | 551 | 382 | pending |
| 57 | `cognition` | 8 | 599 | 422 | pending |
| 58 | `decor` | 8 | 629 | 415 | pending |
| 59 | `library` | 8 | 442 | 247 | pending |
| 60 | `museum` | 8 | 496 | 267 | pending |
| 61 | `quality` | 8 | 507 | 321 | pending |
| 62 | `rental` | 8 | 464 | 281 | pending |
| 63 | `research` | 8 | 527 | 306 | pending |
| 64 | `restaurant` | 8 | 488 | 266 | pending |
| 65 | `telecom` | 8 | 476 | 290 | pending |
| 66 | `audio` | 7 | 512 | 378 | pending |
| 67 | `dance` | 7 | 560 | 377 | pending |
| 68 | `hotel` | 7 | 531 | 329 | pending |
| 69 | `printing` | 7 | 491 | 312 | pending |
| 70 | `woodwork` | 7 | 399 | 292 | pending |
| 71 | `archaeology` | 6 | 360 | 202 | pending |
| 72 | `chinese-cook` | 6 | 471 | 293 | pending |
| 73 | `exhibition` | 6 | 424 | 242 | pending |
| 74 | `film` | 6 | 360 | 236 | pending |
| 75 | `floral` | 6 | 472 | 352 | pending |
| 76 | `funeral` | 6 | 464 | 335 | pending |
| 77 | `home` | 6 | 350 | 211 | pending |
| 78 | `jewelry` | 6 | 430 | 273 | pending |
| 79 | `media` | 6 | 344 | 169 | pending |
| 80 | `office` | 6 | 341 | 264 | pending |
| 81 | `packaging` | 6 | 301 | 171 | pending |
| 82 | `parenting` | 6 | 270 | 164 | pending |
| 83 | `road` | 6 | 460 | 292 | pending |
| 84 | `startup` | 6 | 469 | 309 | pending |
| 85 | `urban` | 6 | 499 | 316 | pending |
| 86 | `video` | 6 | 486 | 311 | pending |
| 87 | `accessibility` | 5 | 347 | 210 | pending |
| 88 | `antiques` | 5 | 345 | 201 | pending |
| 89 | `aquaculture` | 5 | 299 | 189 | pending |
| 90 | `audit` | 5 | 359 | 214 | pending |
| 91 | `bonding` | 5 | 294 | 181 | pending |
| 92 | `bridge` | 5 | 393 | 246 | pending |
| 93 | `ceramics` | 5 | 387 | 247 | pending |
| 94 | `chess` | 5 | 427 | 320 | pending |
| 95 | `chinese` | 5 | 238 | 188 | pending |
| 96 | `edu2` | 5 | 292 | 189 | pending |
| 97 | `fengshui` | 5 | 408 | 300 | pending |
| 98 | `forex` | 5 | 416 | 250 | pending |
| 99 | `futures` | 5 | 411 | 254 | pending |
| 100 | `gardening2` | 5 | 365 | 263 | pending |
| 101 | `glass` | 5 | 364 | 204 | pending |
| 102 | `kids` | 5 | 334 | 198 | pending |
| 103 | `legal2` | 5 | 332 | 200 | pending |
| 104 | `logistics2` | 5 | 319 | 189 | pending |
| 105 | `manufacturing` | 5 | 279 | 154 | pending |
| 106 | `maritime` | 5 | 424 | 282 | pending |
| 107 | `martial` | 5 | 362 | 255 | pending |
| 108 | `medical2` | 5 | 333 | 206 | pending |
| 109 | `pet-training` | 5 | 364 | 263 | pending |
| 110 | `petrochem` | 5 | 355 | 230 | pending |
| 111 | `pets` | 5 | 333 | 229 | pending |
| 112 | `plastic` | 5 | 312 | 175 | pending |
| 113 | `project` | 5 | 403 | 194 | pending |
| 114 | `railway` | 5 | 124 | 80 | pending |
| 115 | `rubber` | 5 | 311 | 174 | pending |
| 116 | `seismology` | 5 | 306 | 195 | pending |
| 117 | `service` | 5 | 306 | 164 | pending |
| 118 | `shipping` | 5 | 311 | 202 | pending |
| 119 | `stage` | 5 | 324 | 186 | pending |
| 120 | `tunnel` | 5 | 373 | 221 | pending |
| 121 | `woodworking` | 5 | 413 | 297 | pending |
| 122 | `yi` | 5 | 370 | 242 | pending |
| 123 | `photo2` | 4 | 236 | 159 | pending |
| 124 | `stats` | 4 | 281 | 198 | pending |

