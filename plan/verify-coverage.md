# verify 用例覆盖台账

> 生成日期：2026-11-05（口径修正版）| 口径：工具页 = `tools/<dir>/*.html` **排除各行业 `index.html`**（分类落地页不含 calc 逻辑）；已覆盖 = 该页 slug 出现在 `scripts/` 下任一 `verify_*` 文件的 `slug` 键中（`"slug"` 与 `slug` 两种写法均计）。

## 总览

| 指标 | 数值 |
|---|---|
| 工具页总数（排除 index） | 4705 |
| 至少 1 条用例覆盖 | 4563（97.0%） |
| 零用例页 | 142（3.0%） |
| 存在零用例页的目录 | 36 |

## 零用例页按目录（页数降序）

| 目录 | 零用例页数 | 目录总页数 | slug |
|---|---|---|---|
| `fun` | 39 | 54 | 1a2b-guess, zodiac-match, othello, daily-riddle, tic-tac-toe, space-shooter, breakout, tongue-twister, sequence-puzzle, snake-game, blood-type-personality, generator-laugh, keyboard-heatmap, sequence-memory, color-guess, hangman, coin-flip, pong, riddle-generator, number-puzzle, rock-paper-scissors, gomoku-ai, emoji-memory, bingo-generator, tetris, word-scramble, memory-game, solitaire, sliding-puzzle, gomoku, generator-2, 2048-game, pattern-memory, minesweeper, shape-memory, generator-3, color-memory, random-name-gen, fingerprint-types |
| `it` | 24 | 338 | ksuid-generator, regex, device-info, pdf-signature-checker, ulid-generator, generator-16, gamertag-generator, ecdsa, tiny-url, less-compiler, benchmark-builder, aes-encryptor, uuid-v7-generator, random-port-generator, typing-test, token-generator, nickname-generator, short-link-generator, team-name-generator, html-to-markdown, keycode-info, uuid-v4-generator, camera-recorder, typescript-compiler |
| `edu` | 11 | 44 | color-quiz, capital-quiz, math-quiz, reminder-1, multiplication-table, country-quiz, flashcards, number-memory, typing-game, flag-quiz, countdown-5 |
| `ai` | 6 | 64 | speech-to-text, text-summarization, sentiment-analysis, ai-text-summarizer, image-classification, ocr |
| `psychology` | 6 | 20 | enneagram-test, analysis-2, bigfive-personality-test, bubble-tea-personality-quiz, tester-3, scl90-assessment |
| `audio` | 4 | 8 | audio-speed, audio-recorder, audio-echo, audio-volume |
| `biz` | 4 | 69 | motto-generator, app-name-generator, brand-name-generator, product-name-generator |
| `design` | 4 | 108 | image-rotator, font-pairing, image-color-picker, palette-extractor |
| `health` | 4 | 40 | stretch-generator, dysphagia-food-guide, symptom-checker, rehab-timer |
| `marketing` | 4 | 45 | funnel-calculator, tagline-generator, hashtag-generator, slogan-generator |
| `ophthalmology` | 3 | 31 | ishihara-test, astigmatism-chart, pupil-reflex |
| `science` | 3 | 92 | logic-gate-simulator, periodic-table, calculator |
| `agriculture` | 2 | 64 | countdown-4, countdown-cycle |
| `food` | 2 | 24 | cooking-converter, beer-gravity-estimator |
| `language` | 2 | 17 | ipa-practice, riyuwushiyintulianxi-dianjifayin |
| `life` | 2 | 70 | holiday-calendar, event-countdown |
| `office` | 2 | 6 | pdf-merge, flowchart |
| `usedcar` | 2 | 12 | checker-3, rater-37 |
| `accessibility` | 1 | 5 | accessible-restroom |
| `acupuncture` | 1 | 22 | acupoint-combination |
| `aerospace` | 1 | 37 | weight-balance |
| `astronomy` | 1 | 23 | solar-elevation |
| `eco` | 1 | 39 | noise-superposition |
| `finance` | 1 | 115 | word-search |
| `geology` | 1 | 36 | calc-1 |
| `image` | 1 | 14 | image-converter |
| `legal` | 1 | 48 | calendar |
| `metalwork` | 1 | 39 | detector-55 |
| `music` | 1 | 20 | detector |
| `obstetrics` | 1 | 27 | pcos-rotterdam |
| `optical` | 1 | 40 | driving-lens |
| `reproductive-medicine` | 1 | 25 | assessor-15 |
| `safety` | 1 | 15 | self-test |
| `security` | 1 | 11 | passphrase-generator |
| `wedding` | 1 | 9 | countdown-time |
| `yi` | 1 | 5 | gua-interpretation |

## 说明

- 旧版台账把 `index.html` 计入分母、且 slug 匹配未归一，导致「117 目录整目录零覆盖 1492 页」的结论失真（实际 0 个整目录零覆盖，零用例最集中的目录也只有少量页）。
- `clinical-nursing/**` 由临床线在途，本台账只统计、不在本线改动。
