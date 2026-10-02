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
| 1 | `optics` | 21 | 645 | 443 | pending |
| 2 | `property` | 21 | 1344 | 732 | pending |
| 3 | `tcm-diagnosis` | 21 | 2103 | 1170 | pending |
| 4 | `travel` | 21 | 1654 | 918 | pending |
| 5 | `forensic-medicine` | 20 | 2374 | 1597 | pending |
| 6 | `metallurgy` | 20 | 1236 | 646 | pending |
| 7 | `psychology` | 20 | 1057 | 622 | pending |
| 8 | `electrical` | 19 | 810 | 545 | pending |
| 9 | `forestry` | 19 | 1435 | 727 | pending |
| 10 | `language` | 19 | 1123 | 622 | pending |
| 11 | `music` | 19 | 1577 | 893 | pending |
| 12 | `nutrition` | 18 | 980 | 546 | pending |
| 13 | `data` | 17 | 906 | 405 | pending |
| 14 | `advertising` | 16 | 1007 | 520 | pending |
| 15 | `niche` | 16 | 1101 | 690 | pending |
| 16 | `leather` | 15 | 948 | 510 | pending |
| 17 | `logistics` | 15 | 807 | 478 | pending |
| 18 | `safety` | 15 | 838 | 503 | pending |
| 19 | `transport` | 15 | 682 | 495 | pending |
| 20 | `welding` | 15 | 1025 | 546 | pending |
| 21 | `engineering` | 14 | 495 | 324 | pending |
| 22 | `image` | 14 | 882 | 609 | pending |
| 23 | `mechanical` | 14 | 644 | 398 | pending |
| 24 | `medical` | 14 | 936 | 604 | pending |
| 25 | `dyeing` | 13 | 868 | 467 | pending |
| 26 | `gardening` | 12 | 866 | 455 | pending |
| 27 | `mining` | 12 | 768 | 468 | pending |
| 28 | `paper` | 12 | 778 | 399 | pending |
| 29 | `pr` | 12 | 900 | 530 | pending |
| 30 | `chemical` | 11 | 654 | 355 | pending |
| 31 | `elderly` | 11 | 691 | 469 | pending |
| 32 | `fire` | 11 | 774 | 461 | pending |
| 33 | `gas` | 11 | 718 | 380 | pending |
| 34 | `text` | 11 | 467 | 301 | pending |
| 35 | `usedcar` | 11 | 641 | 408 | pending |
| 36 | `hvac` | 10 | 908 | 668 | pending |
| 37 | `pet` | 10 | 657 | 446 | pending |
| 38 | `process` | 10 | 315 | 217 | pending |
| 39 | `security` | 10 | 755 | 532 | pending |
| 40 | `baking` | 9 | 532 | 363 | pending |
| 41 | `misc` | 9 | 609 | 337 | pending |
| 42 | `misc2` | 9 | 616 | 392 | pending |
| 43 | `procurement` | 9 | 563 | 332 | pending |
| 44 | `sales` | 9 | 629 | 362 | pending |
| 45 | `admin` | 8 | 539 | 321 | pending |
| 46 | `cleaning` | 8 | 551 | 382 | pending |
| 47 | `cognition` | 8 | 599 | 422 | pending |
| 48 | `decor` | 8 | 629 | 415 | pending |
| 49 | `library` | 8 | 442 | 247 | pending |
| 50 | `museum` | 8 | 496 | 267 | pending |
| 51 | `quality` | 8 | 507 | 321 | pending |
| 52 | `rental` | 8 | 464 | 281 | pending |
| 53 | `research` | 8 | 527 | 306 | pending |
| 54 | `restaurant` | 8 | 488 | 266 | pending |
| 55 | `telecom` | 8 | 476 | 290 | pending |
| 56 | `audio` | 7 | 512 | 378 | pending |
| 57 | `dance` | 7 | 560 | 377 | pending |
| 58 | `hotel` | 7 | 531 | 329 | pending |
| 59 | `printing` | 7 | 491 | 312 | pending |
| 60 | `woodwork` | 7 | 399 | 292 | pending |
| 61 | `archaeology` | 6 | 360 | 202 | pending |
| 62 | `chinese-cook` | 6 | 471 | 293 | pending |
| 63 | `exhibition` | 6 | 424 | 242 | pending |
| 64 | `film` | 6 | 360 | 236 | pending |
| 65 | `floral` | 6 | 472 | 352 | pending |
| 66 | `funeral` | 6 | 464 | 335 | pending |
| 67 | `home` | 6 | 350 | 211 | pending |
| 68 | `jewelry` | 6 | 430 | 273 | pending |
| 69 | `media` | 6 | 344 | 169 | pending |
| 70 | `office` | 6 | 341 | 264 | pending |
| 71 | `packaging` | 6 | 301 | 171 | pending |
| 72 | `parenting` | 6 | 270 | 164 | pending |
| 73 | `road` | 6 | 460 | 292 | pending |
| 74 | `startup` | 6 | 469 | 309 | pending |
| 75 | `urban` | 6 | 499 | 316 | pending |
| 76 | `video` | 6 | 486 | 311 | pending |
| 77 | `accessibility` | 5 | 347 | 210 | pending |
| 78 | `antiques` | 5 | 345 | 201 | pending |
| 79 | `aquaculture` | 5 | 299 | 189 | pending |
| 80 | `audit` | 5 | 359 | 214 | pending |
| 81 | `bonding` | 5 | 294 | 181 | pending |
| 82 | `bridge` | 5 | 393 | 246 | pending |
| 83 | `ceramics` | 5 | 387 | 247 | pending |
| 84 | `chess` | 5 | 427 | 320 | pending |
| 85 | `chinese` | 5 | 238 | 188 | pending |
| 86 | `edu2` | 5 | 292 | 189 | pending |
| 87 | `fengshui` | 5 | 408 | 300 | pending |
| 88 | `forex` | 5 | 416 | 250 | pending |
| 89 | `futures` | 5 | 411 | 254 | pending |
| 90 | `gardening2` | 5 | 365 | 263 | pending |
| 91 | `glass` | 5 | 364 | 204 | pending |
| 92 | `kids` | 5 | 334 | 198 | pending |
| 93 | `legal2` | 5 | 332 | 200 | pending |
| 94 | `logistics2` | 5 | 319 | 189 | pending |
| 95 | `manufacturing` | 5 | 279 | 154 | pending |
| 96 | `maritime` | 5 | 424 | 282 | pending |
| 97 | `martial` | 5 | 362 | 255 | pending |
| 98 | `medical2` | 5 | 333 | 206 | pending |
| 99 | `pet-training` | 5 | 364 | 263 | pending |
| 100 | `petrochem` | 5 | 355 | 230 | pending |
| 101 | `pets` | 5 | 333 | 229 | pending |
| 102 | `plastic` | 5 | 312 | 175 | pending |
| 103 | `project` | 5 | 403 | 194 | pending |
| 104 | `railway` | 5 | 124 | 80 | pending |
| 105 | `rubber` | 5 | 311 | 174 | pending |
| 106 | `seismology` | 5 | 306 | 195 | pending |
| 107 | `service` | 5 | 306 | 164 | pending |
| 108 | `shipping` | 5 | 311 | 202 | pending |
| 109 | `stage` | 5 | 324 | 186 | pending |
| 110 | `tunnel` | 5 | 373 | 221 | pending |
| 111 | `woodworking` | 5 | 413 | 297 | pending |
| 112 | `yi` | 5 | 370 | 242 | pending |
| 113 | `photo2` | 4 | 236 | 159 | pending |
| 114 | `stats` | 4 | 281 | 198 | pending |

