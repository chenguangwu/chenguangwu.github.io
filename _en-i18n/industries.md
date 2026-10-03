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
| 1 | `baking` | 9 | 532 | 363 | pending |
| 2 | `misc` | 9 | 609 | 337 | pending |
| 3 | `misc2` | 9 | 616 | 392 | pending |
| 4 | `procurement` | 9 | 563 | 332 | pending |
| 5 | `sales` | 9 | 629 | 362 | pending |
| 6 | `admin` | 8 | 539 | 321 | pending |
| 7 | `cleaning` | 8 | 551 | 382 | pending |
| 8 | `cognition` | 8 | 599 | 422 | pending |
| 9 | `decor` | 8 | 629 | 415 | pending |
| 10 | `library` | 8 | 442 | 247 | pending |
| 11 | `museum` | 8 | 496 | 267 | pending |
| 12 | `quality` | 8 | 507 | 321 | pending |
| 13 | `rental` | 8 | 464 | 281 | pending |
| 14 | `research` | 8 | 527 | 306 | pending |
| 15 | `restaurant` | 8 | 488 | 266 | pending |
| 16 | `telecom` | 8 | 476 | 290 | pending |
| 17 | `audio` | 7 | 512 | 378 | pending |
| 18 | `dance` | 7 | 560 | 377 | pending |
| 19 | `hotel` | 7 | 531 | 329 | pending |
| 20 | `printing` | 7 | 491 | 312 | pending |
| 21 | `woodwork` | 7 | 399 | 292 | pending |
| 22 | `archaeology` | 6 | 360 | 202 | pending |
| 23 | `chinese-cook` | 6 | 471 | 293 | pending |
| 24 | `exhibition` | 6 | 424 | 242 | pending |
| 25 | `film` | 6 | 360 | 236 | pending |
| 26 | `floral` | 6 | 472 | 352 | pending |
| 27 | `funeral` | 6 | 464 | 335 | pending |
| 28 | `home` | 6 | 350 | 211 | pending |
| 29 | `jewelry` | 6 | 430 | 273 | pending |
| 30 | `media` | 6 | 344 | 169 | pending |
| 31 | `office` | 6 | 341 | 264 | pending |
| 32 | `packaging` | 6 | 301 | 171 | pending |
| 33 | `parenting` | 6 | 270 | 164 | pending |
| 34 | `road` | 6 | 460 | 292 | pending |
| 35 | `startup` | 6 | 469 | 309 | pending |
| 36 | `urban` | 6 | 499 | 316 | pending |
| 37 | `video` | 6 | 486 | 311 | pending |
| 38 | `accessibility` | 5 | 347 | 210 | pending |
| 39 | `antiques` | 5 | 345 | 201 | pending |
| 40 | `aquaculture` | 5 | 299 | 189 | pending |
| 41 | `audit` | 5 | 359 | 214 | pending |
| 42 | `bonding` | 5 | 294 | 181 | pending |
| 43 | `bridge` | 5 | 393 | 246 | pending |
| 44 | `ceramics` | 5 | 387 | 247 | pending |
| 45 | `chess` | 5 | 427 | 320 | pending |
| 46 | `chinese` | 5 | 238 | 188 | pending |
| 47 | `edu2` | 5 | 292 | 189 | pending |
| 48 | `fengshui` | 5 | 408 | 300 | pending |
| 49 | `forex` | 5 | 416 | 250 | pending |
| 50 | `futures` | 5 | 411 | 254 | pending |
| 51 | `gardening2` | 5 | 365 | 263 | pending |
| 52 | `glass` | 5 | 364 | 204 | pending |
| 53 | `kids` | 5 | 334 | 198 | pending |
| 54 | `legal2` | 5 | 332 | 200 | pending |
| 55 | `logistics2` | 5 | 319 | 189 | pending |
| 56 | `manufacturing` | 5 | 279 | 154 | pending |
| 57 | `maritime` | 5 | 424 | 282 | pending |
| 58 | `martial` | 5 | 362 | 255 | pending |
| 59 | `medical2` | 5 | 333 | 206 | pending |
| 60 | `pet-training` | 5 | 364 | 263 | pending |
| 61 | `petrochem` | 5 | 355 | 230 | pending |
| 62 | `pets` | 5 | 333 | 229 | pending |
| 63 | `plastic` | 5 | 312 | 175 | pending |
| 64 | `project` | 5 | 403 | 194 | pending |
| 65 | `railway` | 5 | 124 | 80 | pending |
| 66 | `rubber` | 5 | 311 | 174 | pending |
| 67 | `seismology` | 5 | 306 | 195 | pending |
| 68 | `service` | 5 | 306 | 164 | pending |
| 69 | `shipping` | 5 | 311 | 202 | pending |
| 70 | `stage` | 5 | 324 | 186 | pending |
| 71 | `tunnel` | 5 | 373 | 221 | pending |
| 72 | `woodworking` | 5 | 413 | 297 | pending |
| 73 | `yi` | 5 | 370 | 242 | pending |
| 74 | `photo2` | 4 | 236 | 159 | pending |
| 75 | `stats` | 4 | 281 | 198 | pending |

