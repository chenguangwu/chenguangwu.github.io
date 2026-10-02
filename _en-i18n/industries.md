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
| 1 | `tcm-diagnosis` | 21 | 2103 | 1170 | pending |
| 2 | `travel` | 21 | 1654 | 918 | pending |
| 3 | `forensic-medicine` | 20 | 2374 | 1597 | pending |
| 4 | `metallurgy` | 20 | 1236 | 646 | pending |
| 5 | `psychology` | 20 | 1057 | 622 | pending |
| 6 | `electrical` | 19 | 810 | 545 | pending |
| 7 | `forestry` | 19 | 1435 | 727 | pending |
| 8 | `language` | 19 | 1123 | 622 | pending |
| 9 | `music` | 19 | 1577 | 893 | pending |
| 10 | `nutrition` | 18 | 980 | 546 | pending |
| 11 | `data` | 17 | 906 | 405 | pending |
| 12 | `advertising` | 16 | 1007 | 520 | pending |
| 13 | `niche` | 16 | 1101 | 690 | pending |
| 14 | `leather` | 15 | 948 | 510 | pending |
| 15 | `logistics` | 15 | 807 | 478 | pending |
| 16 | `safety` | 15 | 838 | 503 | pending |
| 17 | `transport` | 15 | 682 | 495 | pending |
| 18 | `welding` | 15 | 1025 | 546 | pending |
| 19 | `engineering` | 14 | 495 | 324 | pending |
| 20 | `image` | 14 | 882 | 609 | pending |
| 21 | `mechanical` | 14 | 644 | 398 | pending |
| 22 | `medical` | 14 | 936 | 604 | pending |
| 23 | `dyeing` | 13 | 868 | 467 | pending |
| 24 | `gardening` | 12 | 866 | 455 | pending |
| 25 | `mining` | 12 | 768 | 468 | pending |
| 26 | `paper` | 12 | 778 | 399 | pending |
| 27 | `pr` | 12 | 900 | 530 | pending |
| 28 | `chemical` | 11 | 654 | 355 | pending |
| 29 | `elderly` | 11 | 691 | 469 | pending |
| 30 | `fire` | 11 | 774 | 461 | pending |
| 31 | `gas` | 11 | 718 | 380 | pending |
| 32 | `text` | 11 | 467 | 301 | pending |
| 33 | `usedcar` | 11 | 641 | 408 | pending |
| 34 | `hvac` | 10 | 908 | 668 | pending |
| 35 | `pet` | 10 | 657 | 446 | pending |
| 36 | `process` | 10 | 315 | 217 | pending |
| 37 | `security` | 10 | 755 | 532 | pending |
| 38 | `baking` | 9 | 532 | 363 | pending |
| 39 | `misc` | 9 | 609 | 337 | pending |
| 40 | `misc2` | 9 | 616 | 392 | pending |
| 41 | `procurement` | 9 | 563 | 332 | pending |
| 42 | `sales` | 9 | 629 | 362 | pending |
| 43 | `admin` | 8 | 539 | 321 | pending |
| 44 | `cleaning` | 8 | 551 | 382 | pending |
| 45 | `cognition` | 8 | 599 | 422 | pending |
| 46 | `decor` | 8 | 629 | 415 | pending |
| 47 | `library` | 8 | 442 | 247 | pending |
| 48 | `museum` | 8 | 496 | 267 | pending |
| 49 | `quality` | 8 | 507 | 321 | pending |
| 50 | `rental` | 8 | 464 | 281 | pending |
| 51 | `research` | 8 | 527 | 306 | pending |
| 52 | `restaurant` | 8 | 488 | 266 | pending |
| 53 | `telecom` | 8 | 476 | 290 | pending |
| 54 | `audio` | 7 | 512 | 378 | pending |
| 55 | `dance` | 7 | 560 | 377 | pending |
| 56 | `hotel` | 7 | 531 | 329 | pending |
| 57 | `printing` | 7 | 491 | 312 | pending |
| 58 | `woodwork` | 7 | 399 | 292 | pending |
| 59 | `archaeology` | 6 | 360 | 202 | pending |
| 60 | `chinese-cook` | 6 | 471 | 293 | pending |
| 61 | `exhibition` | 6 | 424 | 242 | pending |
| 62 | `film` | 6 | 360 | 236 | pending |
| 63 | `floral` | 6 | 472 | 352 | pending |
| 64 | `funeral` | 6 | 464 | 335 | pending |
| 65 | `home` | 6 | 350 | 211 | pending |
| 66 | `jewelry` | 6 | 430 | 273 | pending |
| 67 | `media` | 6 | 344 | 169 | pending |
| 68 | `office` | 6 | 341 | 264 | pending |
| 69 | `packaging` | 6 | 301 | 171 | pending |
| 70 | `parenting` | 6 | 270 | 164 | pending |
| 71 | `road` | 6 | 460 | 292 | pending |
| 72 | `startup` | 6 | 469 | 309 | pending |
| 73 | `urban` | 6 | 499 | 316 | pending |
| 74 | `video` | 6 | 486 | 311 | pending |
| 75 | `accessibility` | 5 | 347 | 210 | pending |
| 76 | `antiques` | 5 | 345 | 201 | pending |
| 77 | `aquaculture` | 5 | 299 | 189 | pending |
| 78 | `audit` | 5 | 359 | 214 | pending |
| 79 | `bonding` | 5 | 294 | 181 | pending |
| 80 | `bridge` | 5 | 393 | 246 | pending |
| 81 | `ceramics` | 5 | 387 | 247 | pending |
| 82 | `chess` | 5 | 427 | 320 | pending |
| 83 | `chinese` | 5 | 238 | 188 | pending |
| 84 | `edu2` | 5 | 292 | 189 | pending |
| 85 | `fengshui` | 5 | 408 | 300 | pending |
| 86 | `forex` | 5 | 416 | 250 | pending |
| 87 | `futures` | 5 | 411 | 254 | pending |
| 88 | `gardening2` | 5 | 365 | 263 | pending |
| 89 | `glass` | 5 | 364 | 204 | pending |
| 90 | `kids` | 5 | 334 | 198 | pending |
| 91 | `legal2` | 5 | 332 | 200 | pending |
| 92 | `logistics2` | 5 | 319 | 189 | pending |
| 93 | `manufacturing` | 5 | 279 | 154 | pending |
| 94 | `maritime` | 5 | 424 | 282 | pending |
| 95 | `martial` | 5 | 362 | 255 | pending |
| 96 | `medical2` | 5 | 333 | 206 | pending |
| 97 | `pet-training` | 5 | 364 | 263 | pending |
| 98 | `petrochem` | 5 | 355 | 230 | pending |
| 99 | `pets` | 5 | 333 | 229 | pending |
| 100 | `plastic` | 5 | 312 | 175 | pending |
| 101 | `project` | 5 | 403 | 194 | pending |
| 102 | `railway` | 5 | 124 | 80 | pending |
| 103 | `rubber` | 5 | 311 | 174 | pending |
| 104 | `seismology` | 5 | 306 | 195 | pending |
| 105 | `service` | 5 | 306 | 164 | pending |
| 106 | `shipping` | 5 | 311 | 202 | pending |
| 107 | `stage` | 5 | 324 | 186 | pending |
| 108 | `tunnel` | 5 | 373 | 221 | pending |
| 109 | `woodworking` | 5 | 413 | 297 | pending |
| 110 | `yi` | 5 | 370 | 242 | pending |
| 111 | `photo2` | 4 | 236 | 159 | pending |
| 112 | `stats` | 4 | 281 | 198 | pending |

