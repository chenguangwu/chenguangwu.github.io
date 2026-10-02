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
| 1 | `transport` | 15 | 682 | 495 | pending |
| 2 | `welding` | 15 | 1025 | 546 | pending |
| 3 | `engineering` | 14 | 495 | 324 | pending |
| 4 | `image` | 14 | 882 | 609 | pending |
| 5 | `mechanical` | 14 | 644 | 398 | pending |
| 6 | `medical` | 14 | 936 | 604 | pending |
| 7 | `dyeing` | 13 | 868 | 467 | pending |
| 8 | `gardening` | 12 | 866 | 455 | pending |
| 9 | `mining` | 12 | 768 | 468 | pending |
| 10 | `paper` | 12 | 778 | 399 | pending |
| 11 | `pr` | 12 | 900 | 530 | pending |
| 12 | `chemical` | 11 | 654 | 355 | pending |
| 13 | `elderly` | 11 | 691 | 469 | pending |
| 14 | `fire` | 11 | 774 | 461 | pending |
| 15 | `gas` | 11 | 718 | 380 | pending |
| 16 | `text` | 11 | 467 | 301 | pending |
| 17 | `usedcar` | 11 | 641 | 408 | pending |
| 18 | `hvac` | 10 | 908 | 668 | pending |
| 19 | `pet` | 10 | 657 | 446 | pending |
| 20 | `process` | 10 | 315 | 217 | pending |
| 21 | `security` | 10 | 755 | 532 | pending |
| 22 | `baking` | 9 | 532 | 363 | pending |
| 23 | `misc` | 9 | 609 | 337 | pending |
| 24 | `misc2` | 9 | 616 | 392 | pending |
| 25 | `procurement` | 9 | 563 | 332 | pending |
| 26 | `sales` | 9 | 629 | 362 | pending |
| 27 | `admin` | 8 | 539 | 321 | pending |
| 28 | `cleaning` | 8 | 551 | 382 | pending |
| 29 | `cognition` | 8 | 599 | 422 | pending |
| 30 | `decor` | 8 | 629 | 415 | pending |
| 31 | `library` | 8 | 442 | 247 | pending |
| 32 | `museum` | 8 | 496 | 267 | pending |
| 33 | `quality` | 8 | 507 | 321 | pending |
| 34 | `rental` | 8 | 464 | 281 | pending |
| 35 | `research` | 8 | 527 | 306 | pending |
| 36 | `restaurant` | 8 | 488 | 266 | pending |
| 37 | `telecom` | 8 | 476 | 290 | pending |
| 38 | `audio` | 7 | 512 | 378 | pending |
| 39 | `dance` | 7 | 560 | 377 | pending |
| 40 | `hotel` | 7 | 531 | 329 | pending |
| 41 | `printing` | 7 | 491 | 312 | pending |
| 42 | `woodwork` | 7 | 399 | 292 | pending |
| 43 | `archaeology` | 6 | 360 | 202 | pending |
| 44 | `chinese-cook` | 6 | 471 | 293 | pending |
| 45 | `exhibition` | 6 | 424 | 242 | pending |
| 46 | `film` | 6 | 360 | 236 | pending |
| 47 | `floral` | 6 | 472 | 352 | pending |
| 48 | `funeral` | 6 | 464 | 335 | pending |
| 49 | `home` | 6 | 350 | 211 | pending |
| 50 | `jewelry` | 6 | 430 | 273 | pending |
| 51 | `media` | 6 | 344 | 169 | pending |
| 52 | `office` | 6 | 341 | 264 | pending |
| 53 | `packaging` | 6 | 301 | 171 | pending |
| 54 | `parenting` | 6 | 270 | 164 | pending |
| 55 | `road` | 6 | 460 | 292 | pending |
| 56 | `startup` | 6 | 469 | 309 | pending |
| 57 | `urban` | 6 | 499 | 316 | pending |
| 58 | `video` | 6 | 486 | 311 | pending |
| 59 | `accessibility` | 5 | 347 | 210 | pending |
| 60 | `antiques` | 5 | 345 | 201 | pending |
| 61 | `aquaculture` | 5 | 299 | 189 | pending |
| 62 | `audit` | 5 | 359 | 214 | pending |
| 63 | `bonding` | 5 | 294 | 181 | pending |
| 64 | `bridge` | 5 | 393 | 246 | pending |
| 65 | `ceramics` | 5 | 387 | 247 | pending |
| 66 | `chess` | 5 | 427 | 320 | pending |
| 67 | `chinese` | 5 | 238 | 188 | pending |
| 68 | `edu2` | 5 | 292 | 189 | pending |
| 69 | `fengshui` | 5 | 408 | 300 | pending |
| 70 | `forex` | 5 | 416 | 250 | pending |
| 71 | `futures` | 5 | 411 | 254 | pending |
| 72 | `gardening2` | 5 | 365 | 263 | pending |
| 73 | `glass` | 5 | 364 | 204 | pending |
| 74 | `kids` | 5 | 334 | 198 | pending |
| 75 | `legal2` | 5 | 332 | 200 | pending |
| 76 | `logistics2` | 5 | 319 | 189 | pending |
| 77 | `manufacturing` | 5 | 279 | 154 | pending |
| 78 | `maritime` | 5 | 424 | 282 | pending |
| 79 | `martial` | 5 | 362 | 255 | pending |
| 80 | `medical2` | 5 | 333 | 206 | pending |
| 81 | `pet-training` | 5 | 364 | 263 | pending |
| 82 | `petrochem` | 5 | 355 | 230 | pending |
| 83 | `pets` | 5 | 333 | 229 | pending |
| 84 | `plastic` | 5 | 312 | 175 | pending |
| 85 | `project` | 5 | 403 | 194 | pending |
| 86 | `railway` | 5 | 124 | 80 | pending |
| 87 | `rubber` | 5 | 311 | 174 | pending |
| 88 | `seismology` | 5 | 306 | 195 | pending |
| 89 | `service` | 5 | 306 | 164 | pending |
| 90 | `shipping` | 5 | 311 | 202 | pending |
| 91 | `stage` | 5 | 324 | 186 | pending |
| 92 | `tunnel` | 5 | 373 | 221 | pending |
| 93 | `woodworking` | 5 | 413 | 297 | pending |
| 94 | `yi` | 5 | 370 | 242 | pending |
| 95 | `photo2` | 4 | 236 | 159 | pending |
| 96 | `stats` | 4 | 281 | 198 | pending |

