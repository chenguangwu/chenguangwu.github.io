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
| 1 | `gas` | 11 | 718 | 380 | pending |
| 2 | `text` | 11 | 467 | 301 | pending |
| 3 | `usedcar` | 11 | 641 | 408 | pending |
| 4 | `hvac` | 10 | 908 | 668 | pending |
| 5 | `pet` | 10 | 657 | 446 | pending |
| 6 | `process` | 10 | 315 | 217 | pending |
| 7 | `security` | 10 | 755 | 532 | pending |
| 8 | `baking` | 9 | 532 | 363 | pending |
| 9 | `misc` | 9 | 609 | 337 | pending |
| 10 | `misc2` | 9 | 616 | 392 | pending |
| 11 | `procurement` | 9 | 563 | 332 | pending |
| 12 | `sales` | 9 | 629 | 362 | pending |
| 13 | `admin` | 8 | 539 | 321 | pending |
| 14 | `cleaning` | 8 | 551 | 382 | pending |
| 15 | `cognition` | 8 | 599 | 422 | pending |
| 16 | `decor` | 8 | 629 | 415 | pending |
| 17 | `library` | 8 | 442 | 247 | pending |
| 18 | `museum` | 8 | 496 | 267 | pending |
| 19 | `quality` | 8 | 507 | 321 | pending |
| 20 | `rental` | 8 | 464 | 281 | pending |
| 21 | `research` | 8 | 527 | 306 | pending |
| 22 | `restaurant` | 8 | 488 | 266 | pending |
| 23 | `telecom` | 8 | 476 | 290 | pending |
| 24 | `audio` | 7 | 512 | 378 | pending |
| 25 | `dance` | 7 | 560 | 377 | pending |
| 26 | `hotel` | 7 | 531 | 329 | pending |
| 27 | `printing` | 7 | 491 | 312 | pending |
| 28 | `woodwork` | 7 | 399 | 292 | pending |
| 29 | `archaeology` | 6 | 360 | 202 | pending |
| 30 | `chinese-cook` | 6 | 471 | 293 | pending |
| 31 | `exhibition` | 6 | 424 | 242 | pending |
| 32 | `film` | 6 | 360 | 236 | pending |
| 33 | `floral` | 6 | 472 | 352 | pending |
| 34 | `funeral` | 6 | 464 | 335 | pending |
| 35 | `home` | 6 | 350 | 211 | pending |
| 36 | `jewelry` | 6 | 430 | 273 | pending |
| 37 | `media` | 6 | 344 | 169 | pending |
| 38 | `office` | 6 | 341 | 264 | pending |
| 39 | `packaging` | 6 | 301 | 171 | pending |
| 40 | `parenting` | 6 | 270 | 164 | pending |
| 41 | `road` | 6 | 460 | 292 | pending |
| 42 | `startup` | 6 | 469 | 309 | pending |
| 43 | `urban` | 6 | 499 | 316 | pending |
| 44 | `video` | 6 | 486 | 311 | pending |
| 45 | `accessibility` | 5 | 347 | 210 | pending |
| 46 | `antiques` | 5 | 345 | 201 | pending |
| 47 | `aquaculture` | 5 | 299 | 189 | pending |
| 48 | `audit` | 5 | 359 | 214 | pending |
| 49 | `bonding` | 5 | 294 | 181 | pending |
| 50 | `bridge` | 5 | 393 | 246 | pending |
| 51 | `ceramics` | 5 | 387 | 247 | pending |
| 52 | `chess` | 5 | 427 | 320 | pending |
| 53 | `chinese` | 5 | 238 | 188 | pending |
| 54 | `edu2` | 5 | 292 | 189 | pending |
| 55 | `fengshui` | 5 | 408 | 300 | pending |
| 56 | `forex` | 5 | 416 | 250 | pending |
| 57 | `futures` | 5 | 411 | 254 | pending |
| 58 | `gardening2` | 5 | 365 | 263 | pending |
| 59 | `glass` | 5 | 364 | 204 | pending |
| 60 | `kids` | 5 | 334 | 198 | pending |
| 61 | `legal2` | 5 | 332 | 200 | pending |
| 62 | `logistics2` | 5 | 319 | 189 | pending |
| 63 | `manufacturing` | 5 | 279 | 154 | pending |
| 64 | `maritime` | 5 | 424 | 282 | pending |
| 65 | `martial` | 5 | 362 | 255 | pending |
| 66 | `medical2` | 5 | 333 | 206 | pending |
| 67 | `pet-training` | 5 | 364 | 263 | pending |
| 68 | `petrochem` | 5 | 355 | 230 | pending |
| 69 | `pets` | 5 | 333 | 229 | pending |
| 70 | `plastic` | 5 | 312 | 175 | pending |
| 71 | `project` | 5 | 403 | 194 | pending |
| 72 | `railway` | 5 | 124 | 80 | pending |
| 73 | `rubber` | 5 | 311 | 174 | pending |
| 74 | `seismology` | 5 | 306 | 195 | pending |
| 75 | `service` | 5 | 306 | 164 | pending |
| 76 | `shipping` | 5 | 311 | 202 | pending |
| 77 | `stage` | 5 | 324 | 186 | pending |
| 78 | `tunnel` | 5 | 373 | 221 | pending |
| 79 | `woodworking` | 5 | 413 | 297 | pending |
| 80 | `yi` | 5 | 370 | 242 | pending |
| 81 | `photo2` | 4 | 236 | 159 | pending |
| 82 | `stats` | 4 | 281 | 198 | pending |

