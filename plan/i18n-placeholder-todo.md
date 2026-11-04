# 英文态 placeholder / title 中文残留量化

> 只读静态扫描（Python HTMLParser）+ 抽样真机确认；未改页面、未改 `i18n.js`、未跑 `_build.py`、未 push。

## 一、静态扫描结论

- 扫描范围：`tools/*/*.html`（排除各行业 `index.html`）。
- `<input|textarea placeholder>` 含汉字：**12796 处 / 3940 页**，覆盖 **206 个行业目录**。
- `title=` 属性含汉字（悬停提示）：**153 处 / 99 页**。
- 任一属性含汉字：**3947 页**。
- 其中 placeholder 原文能在该页第三层词典 `map` 中找到键的：**1291 处**；找不到的：**11505 处**（后者才是英文态必残留）。
- title 属性：词典命中 **23 处** / 未命中 **130 处**。
- **页面级覆盖**：共有 placeholder 中文的 3940 页中，全部能被词典命中（现有属性分支可译）**353 页**；部分命中 **215 页**；全部未命中（英文态必残留）**3372 页**。
- 工具页显式声明 `data-i18n-ph` 的：**0 页**（无）。
- JS 动态给 `placeholder` 赋中文的页面：**2 页**（静态属性扫不到，属隐藏影响面）。

### 按行业目录

| 目录 | 页面数 | placeholder 处 | 涉及页 | title 处 | 涉及页 | 词典命中 | 词典未命中 | data-i18n-ph 页 | JS 动态中文页 |
|---|---|---|---|---|---|---|---|---|---|
| it | 338 | 499 | 251 | 35 | 4 | 15 | 484 | 0 | 0 |
| finance | 115 | 442 | 110 | 1 | 1 | 171 | 271 | 0 | 0 |
| machinery | 76 | 308 | 75 | 2 | 2 | 0 | 308 | 0 | 0 |
| automotive | 59 | 288 | 57 | 0 | 0 | 10 | 278 | 0 | 0 |
| hydraulic | 55 | 272 | 52 | 0 | 0 | 4 | 268 | 0 | 0 |
| sports | 75 | 259 | 67 | 9 | 9 | 19 | 240 | 0 | 0 |
| agriculture | 64 | 261 | 62 | 0 | 0 | 11 | 250 | 0 | 0 |
| science | 92 | 219 | 73 | 7 | 1 | 3 | 216 | 0 | 0 |
| ai | 64 | 215 | 61 | 0 | 0 | 17 | 198 | 0 | 0 |
| realestate | 54 | 188 | 50 | 14 | 14 | 2 | 186 | 0 | 0 |
| general | 55 | 199 | 52 | 0 | 0 | 0 | 199 | 0 | 0 |
| design | 108 | 180 | 79 | 6 | 3 | 47 | 133 | 0 | 0 |
| construction | 37 | 175 | 37 | 0 | 0 | 2 | 173 | 0 | 0 |
| marketing | 45 | 173 | 37 | 0 | 0 | 17 | 156 | 0 | 0 |
| fishery | 38 | 156 | 38 | 4 | 4 | 7 | 149 | 0 | 0 |
| statistics | 51 | 160 | 39 | 0 | 0 | 0 | 160 | 0 | 0 |
| biz | 69 | 150 | 64 | 0 | 0 | 53 | 97 | 0 | 0 |
| energy | 41 | 143 | 41 | 0 | 0 | 2 | 141 | 0 | 0 |
| fitness | 37 | 138 | 35 | 0 | 0 | 5 | 133 | 0 | 0 |
| life | 70 | 138 | 62 | 0 | 0 | 45 | 93 | 0 | 0 |
| healthcare | 35 | 134 | 35 | 0 | 0 | 32 | 102 | 0 | 0 |
| eco | 39 | 132 | 38 | 0 | 0 | 1 | 131 | 0 | 0 |
| legal | 48 | 128 | 37 | 4 | 4 | 29 | 99 | 0 | 0 |
| metalwork | 39 | 121 | 37 | 6 | 6 | 4 | 117 | 0 | 0 |
| hematology | 26 | 122 | 23 | 0 | 0 | 6 | 116 | 0 | 0 |
| chemistry | 37 | 121 | 37 | 0 | 0 | 0 | 121 | 0 | 0 |
| health | 40 | 121 | 33 | 0 | 0 | 10 | 111 | 0 | 0 |
| materials | 41 | 117 | 41 | 0 | 0 | 0 | 117 | 0 | 0 |
| civil | 24 | 115 | 24 | 0 | 0 | 0 | 115 | 0 | 0 |
| aerospace | 37 | 114 | 37 | 0 | 0 | 1 | 113 | 0 | 0 |
| surveying | 43 | 110 | 39 | 3 | 3 | 2 | 108 | 0 | 0 |
| optical | 40 | 110 | 38 | 0 | 0 | 0 | 110 | 0 | 0 |
| tcm-chemistry | 22 | 110 | 20 | 0 | 0 | 9 | 101 | 0 | 0 |
| food-testing | 26 | 109 | 25 | 0 | 0 | 8 | 101 | 0 | 0 |
| meteorology | 42 | 109 | 42 | 0 | 0 | 1 | 108 | 0 | 0 |
| fire-rescue | 39 | 107 | 34 | 0 | 0 | 1 | 106 | 0 | 0 |
| electrical | 35 | 106 | 31 | 0 | 0 | 2 | 104 | 0 | 0 |
| math | 41 | 105 | 38 | 0 | 0 | 8 | 97 | 0 | 0 |
| textile | 28 | 105 | 23 | 0 | 0 | 0 | 105 | 0 | 0 |
| securities | 35 | 102 | 32 | 0 | 0 | 3 | 99 | 0 | 0 |
| geology | 36 | 95 | 31 | 4 | 4 | 5 | 90 | 0 | 0 |
| photo | 31 | 99 | 31 | 0 | 0 | 5 | 94 | 0 | 0 |
| accounting | 35 | 93 | 34 | 0 | 0 | 1 | 92 | 0 | 0 |
| thermodynamics | 28 | 91 | 28 | 0 | 0 | 0 | 91 | 0 | 0 |
| livestock | 27 | 87 | 21 | 0 | 0 | 1 | 86 | 0 | 0 |
| nephrology | 23 | 87 | 21 | 0 | 0 | 13 | 74 | 0 | 0 |
| edu | 44 | 83 | 32 | 3 | 2 | 32 | 51 | 0 | 0 |
| endocrinology | 22 | 85 | 21 | 0 | 0 | 11 | 74 | 0 | 0 |
| investment | 25 | 82 | 24 | 0 | 0 | 0 | 82 | 0 | 0 |
| tax | 31 | 82 | 31 | 0 | 0 | 0 | 82 | 0 | 0 |
| encode | 31 | 81 | 29 | 0 | 0 | 2 | 79 | 0 | 0 |
| food | 24 | 79 | 23 | 1 | 1 | 24 | 55 | 0 | 0 |
| hvac | 13 | 80 | 13 | 0 | 0 | 5 | 75 | 0 | 0 |
| reproductive-medicine | 25 | 80 | 22 | 0 | 0 | 0 | 80 | 0 | 0 |
| obstetrics | 27 | 79 | 23 | 0 | 0 | 3 | 76 | 0 | 0 |
| welding | 21 | 79 | 21 | 0 | 0 | 1 | 78 | 0 | 0 |
| clinical-lab | 22 | 78 | 19 | 0 | 0 | 34 | 44 | 0 | 0 |
| ophthalmology | 31 | 78 | 20 | 0 | 0 | 9 | 69 | 0 | 0 |
| fluid | 23 | 75 | 23 | 0 | 0 | 0 | 75 | 0 | 0 |
| food-processing | 20 | 73 | 16 | 0 | 0 | 1 | 72 | 0 | 0 |
| metallurgy | 19 | 70 | 18 | 3 | 3 | 15 | 55 | 0 | 0 |
| cosmetic-derm | 33 | 72 | 23 | 0 | 0 | 5 | 67 | 0 | 0 |
| ecommerce | 23 | 61 | 22 | 11 | 11 | 23 | 38 | 0 | 0 |
| insurance | 30 | 72 | 29 | 0 | 0 | 0 | 72 | 0 | 0 |
| robotics | 28 | 72 | 28 | 0 | 0 | 0 | 72 | 0 | 0 |
| geometry | 28 | 69 | 28 | 0 | 0 | 0 | 69 | 0 | 0 |
| economics | 27 | 66 | 27 | 0 | 0 | 0 | 66 | 0 | 0 |
| banking | 25 | 65 | 25 | 0 | 0 | 4 | 61 | 0 | 0 |
| property | 20 | 61 | 18 | 4 | 4 | 8 | 53 | 0 | 0 |
| dynamics | 23 | 62 | 23 | 0 | 0 | 0 | 62 | 0 | 0 |
| hr | 19 | 59 | 17 | 3 | 3 | 2 | 57 | 0 | 0 |
| metrology | 29 | 62 | 26 | 0 | 0 | 0 | 62 | 0 | 0 |
| mechanical | 14 | 61 | 14 | 0 | 0 | 0 | 61 | 0 | 0 |
| electromagnetism | 26 | 60 | 25 | 0 | 0 | 0 | 60 | 0 | 0 |
| logistics | 15 | 60 | 14 | 0 | 0 | 10 | 50 | 0 | 0 |
| advertising | 16 | 59 | 16 | 0 | 0 | 3 | 56 | 0 | 0 |
| structural | 26 | 59 | 26 | 0 | 0 | 0 | 59 | 0 | 0 |
| kinematics | 25 | 58 | 25 | 0 | 0 | 0 | 58 | 0 | 0 |
| pediatrics | 24 | 57 | 24 | 0 | 0 | 8 | 49 | 0 | 0 |
| acoustics | 28 | 56 | 28 | 0 | 0 | 0 | 56 | 0 | 0 |
| electronics | 21 | 56 | 16 | 0 | 0 | 0 | 56 | 0 | 0 |
| cardiology | 23 | 55 | 17 | 0 | 0 | 11 | 44 | 0 | 0 |
| nuclear | 28 | 54 | 28 | 0 | 0 | 0 | 54 | 0 | 0 |
| rehabilitation | 21 | 54 | 12 | 0 | 0 | 49 | 5 | 0 | 0 |
| mining | 12 | 53 | 10 | 0 | 0 | 1 | 52 | 0 | 0 |
| leather | 15 | 51 | 15 | 0 | 0 | 3 | 48 | 0 | 0 |
| startup | 6 | 51 | 4 | 0 | 0 | 33 | 18 | 0 | 0 |
| forestry | 19 | 50 | 17 | 0 | 0 | 1 | 49 | 0 | 0 |
| gastroenterology | 22 | 49 | 16 | 0 | 0 | 4 | 45 | 0 | 0 |
| medical | 14 | 49 | 14 | 0 | 0 | 35 | 14 | 0 | 0 |
| signal | 27 | 49 | 26 | 0 | 0 | 0 | 49 | 0 | 0 |
| transport | 15 | 49 | 15 | 0 | 0 | 4 | 45 | 0 | 0 |
| ent | 23 | 47 | 11 | 0 | 0 | 0 | 47 | 0 | 0 |
| optics | 21 | 47 | 21 | 0 | 0 | 0 | 47 | 0 | 0 |
| urology | 24 | 47 | 18 | 0 | 0 | 2 | 45 | 0 | 0 |
| astronomy | 23 | 44 | 22 | 1 | 1 | 2 | 42 | 0 | 0 |
| dyeing | 13 | 44 | 12 | 0 | 0 | 1 | 43 | 0 | 0 |
| printing | 7 | 43 | 6 | 0 | 0 | 19 | 24 | 0 | 0 |
| process | 14 | 43 | 14 | 0 | 0 | 0 | 43 | 0 | 0 |
| paper | 12 | 38 | 12 | 4 | 4 | 1 | 37 | 0 | 0 |
| gas | 11 | 41 | 10 | 0 | 0 | 0 | 41 | 0 | 0 |
| rheumatology | 25 | 41 | 11 | 0 | 0 | 0 | 41 | 0 | 0 |
| pulmonology | 24 | 40 | 12 | 0 | 0 | 9 | 31 | 0 | 0 |
| quantum | 27 | 40 | 27 | 0 | 0 | 0 | 40 | 0 | 0 |
| usedcar | 12 | 40 | 11 | 0 | 0 | 7 | 33 | 0 | 0 |
| travel | 24 | 39 | 16 | 0 | 0 | 11 | 28 | 0 | 0 |
| decor | 8 | 38 | 7 | 0 | 0 | 0 | 38 | 0 | 0 |
| chemical | 14 | 37 | 10 | 0 | 0 | 5 | 32 | 0 | 0 |
| dentistry | 23 | 37 | 13 | 0 | 0 | 1 | 36 | 0 | 0 |
| procurement | 9 | 35 | 9 | 2 | 2 | 0 | 35 | 0 | 0 |
| tcm-pharmacy | 21 | 36 | 17 | 0 | 0 | 16 | 20 | 0 | 0 |
| tcm-diagnosis | 21 | 35 | 7 | 0 | 0 | 34 | 1 | 0 | 0 |
| fire | 11 | 34 | 9 | 0 | 0 | 1 | 33 | 0 | 0 |
| bridge | 5 | 33 | 5 | 0 | 0 | 9 | 24 | 0 | 0 |
| rental | 8 | 32 | 7 | 0 | 0 | 2 | 30 | 0 | 0 |
| nutrition | 18 | 31 | 13 | 0 | 0 | 2 | 29 | 0 | 0 |
| safety | 15 | 31 | 12 | 0 | 0 | 13 | 18 | 0 | 0 |
| telecom | 9 | 31 | 9 | 0 | 0 | 1 | 30 | 0 | 0 |
| pet | 14 | 30 | 11 | 0 | 0 | 2 | 28 | 0 | 0 |
| quality | 8 | 30 | 8 | 0 | 0 | 2 | 28 | 0 | 0 |
| restaurant | 10 | 30 | 8 | 0 | 0 | 0 | 30 | 0 | 0 |
| sales | 9 | 30 | 8 | 0 | 0 | 3 | 27 | 0 | 1 |
| research | 8 | 29 | 6 | 0 | 0 | 4 | 25 | 0 | 0 |
| urban | 6 | 29 | 6 | 0 | 0 | 0 | 29 | 0 | 0 |
| engineering | 11 | 28 | 8 | 0 | 0 | 0 | 28 | 0 | 0 |
| exhibition | 6 | 28 | 4 | 0 | 0 | 1 | 27 | 0 | 0 |
| forensic-medicine | 19 | 28 | 9 | 0 | 0 | 0 | 28 | 0 | 0 |
| audit | 5 | 27 | 5 | 0 | 0 | 0 | 27 | 0 | 0 |
| clinical-nursing | 26 | 27 | 12 | 0 | 0 | 16 | 11 | 0 | 0 |
| music | 20 | 24 | 11 | 3 | 1 | 9 | 15 | 0 | 0 |
| plastic | 5 | 27 | 5 | 0 | 0 | 1 | 26 | 0 | 0 |
| futures | 5 | 26 | 5 | 0 | 0 | 0 | 26 | 0 | 0 |
| museum | 8 | 26 | 5 | 0 | 0 | 7 | 19 | 0 | 0 |
| road | 6 | 26 | 6 | 0 | 0 | 0 | 26 | 0 | 0 |
| maritime | 5 | 25 | 5 | 0 | 0 | 6 | 19 | 0 | 0 |
| seismology | 5 | 25 | 5 | 0 | 0 | 17 | 8 | 0 | 0 |
| woodwork | 7 | 25 | 7 | 0 | 0 | 1 | 24 | 0 | 0 |
| forex | 5 | 24 | 5 | 0 | 0 | 0 | 24 | 0 | 0 |
| manufacturing | 5 | 24 | 5 | 0 | 0 | 0 | 24 | 0 | 0 |
| video | 7 | 24 | 7 | 0 | 0 | 7 | 17 | 0 | 0 |
| dermatology | 23 | 23 | 4 | 0 | 0 | 1 | 22 | 0 | 0 |
| language | 17 | 23 | 14 | 0 | 0 | 23 | 0 | 0 | 0 |
| logistics2 | 5 | 23 | 5 | 0 | 0 | 11 | 12 | 0 | 0 |
| petrochem | 5 | 23 | 5 | 0 | 0 | 0 | 23 | 0 | 0 |
| film | 6 | 22 | 6 | 0 | 0 | 1 | 21 | 0 | 0 |
| home | 6 | 22 | 5 | 0 | 0 | 3 | 19 | 0 | 0 |
| fun | 54 | 17 | 15 | 4 | 2 | 0 | 17 | 0 | 0 |
| image | 14 | 11 | 5 | 10 | 2 | 6 | 5 | 0 | 0 |
| library | 7 | 21 | 6 | 0 | 0 | 1 | 20 | 0 | 0 |
| shipping | 5 | 21 | 5 | 0 | 0 | 1 | 20 | 0 | 0 |
| aquaculture | 5 | 20 | 5 | 0 | 0 | 3 | 17 | 0 | 0 |
| beauty | 21 | 20 | 8 | 0 | 0 | 3 | 17 | 0 | 0 |
| medical2 | 5 | 20 | 5 | 0 | 0 | 5 | 15 | 0 | 0 |
| tunnel | 5 | 19 | 5 | 0 | 0 | 2 | 17 | 0 | 0 |
| woodworking | 5 | 19 | 5 | 0 | 0 | 0 | 19 | 0 | 0 |
| dance | 7 | 18 | 6 | 0 | 0 | 0 | 18 | 0 | 0 |
| data | 21 | 18 | 15 | 0 | 0 | 2 | 16 | 0 | 1 |
| cleaning | 9 | 17 | 6 | 0 | 0 | 5 | 12 | 0 | 0 |
| media | 6 | 17 | 6 | 0 | 0 | 3 | 14 | 0 | 0 |
| packaging | 6 | 14 | 5 | 3 | 3 | 2 | 12 | 0 | 0 |
| baking | 8 | 16 | 7 | 0 | 0 | 5 | 11 | 0 | 0 |
| floral | 6 | 16 | 5 | 0 | 0 | 0 | 16 | 0 | 0 |
| glass | 5 | 16 | 5 | 0 | 0 | 0 | 16 | 0 | 0 |
| hotel | 7 | 16 | 5 | 0 | 0 | 0 | 16 | 0 | 0 |
| parenting | 6 | 16 | 6 | 0 | 0 | 0 | 16 | 0 | 0 |
| acupuncture | 22 | 15 | 13 | 0 | 0 | 6 | 9 | 0 | 0 |
| funeral | 6 | 15 | 6 | 0 | 0 | 8 | 7 | 0 | 0 |
| archaeology | 6 | 14 | 6 | 0 | 0 | 4 | 10 | 0 | 0 |
| bonding | 5 | 14 | 5 | 0 | 0 | 1 | 13 | 0 | 0 |
| pr | 12 | 14 | 7 | 0 | 0 | 6 | 8 | 0 | 0 |
| stage | 5 | 14 | 5 | 0 | 0 | 1 | 13 | 0 | 0 |
| chess | 5 | 13 | 4 | 0 | 0 | 2 | 11 | 0 | 0 |
| martial | 5 | 13 | 5 | 0 | 0 | 1 | 12 | 0 | 0 |
| rubber | 5 | 13 | 5 | 0 | 0 | 0 | 13 | 0 | 0 |
| security | 11 | 13 | 6 | 0 | 0 | 0 | 13 | 0 | 0 |
| edu2 | 5 | 12 | 4 | 0 | 0 | 9 | 3 | 0 | 0 |
| elderly | 11 | 12 | 5 | 0 | 0 | 7 | 5 | 0 | 0 |
| neurology | 25 | 12 | 3 | 0 | 0 | 0 | 12 | 0 | 0 |
| wedding | 9 | 12 | 5 | 0 | 0 | 0 | 12 | 0 | 0 |
| gardening | 15 | 11 | 11 | 0 | 0 | 7 | 4 | 0 | 0 |
| pet-training | 5 | 11 | 5 | 0 | 0 | 0 | 11 | 0 | 0 |
| jewelry | 6 | 10 | 6 | 0 | 0 | 1 | 9 | 0 | 0 |
| ceramics | 6 | 9 | 4 | 0 | 0 | 1 | 8 | 0 | 0 |
| text | 12 | 9 | 7 | 0 | 0 | 1 | 8 | 0 | 0 |
| admin | 7 | 7 | 4 | 0 | 0 | 3 | 4 | 0 | 0 |
| audio | 8 | 4 | 2 | 3 | 2 | 0 | 4 | 0 | 0 |
| chinese | 5 | 7 | 3 | 0 | 0 | 7 | 0 | 0 | 0 |
| service | 5 | 7 | 3 | 0 | 0 | 1 | 6 | 0 | 0 |
| photo2 | 4 | 6 | 3 | 0 | 0 | 1 | 5 | 0 | 0 |
| railway | 2 | 4 | 2 | 2 | 2 | 0 | 4 | 0 | 0 |
| stats | 4 | 6 | 4 | 0 | 0 | 0 | 6 | 0 | 0 |
| accessibility | 5 | 5 | 4 | 0 | 0 | 3 | 2 | 0 | 0 |
| antiques | 6 | 5 | 5 | 0 | 0 | 5 | 0 | 0 | 0 |
| legal2 | 5 | 5 | 4 | 0 | 0 | 1 | 4 | 0 | 0 |
| office | 6 | 4 | 4 | 1 | 1 | 4 | 0 | 0 | 0 |
| chinese-cook | 6 | 4 | 3 | 0 | 0 | 1 | 3 | 0 | 0 |
| gardening2 | 5 | 4 | 2 | 0 | 0 | 0 | 4 | 0 | 0 |
| kids | 5 | 4 | 2 | 0 | 0 | 1 | 3 | 0 | 0 |
| fengshui | 5 | 3 | 3 | 0 | 0 | 1 | 2 | 0 | 0 |
| project | 5 | 3 | 1 | 0 | 0 | 1 | 2 | 0 | 0 |
| beekeeping | 1 | 2 | 1 | 0 | 0 | 0 | 2 | 0 | 0 |
| express | 1 | 2 | 1 | 0 | 0 | 2 | 0 | 0 | 0 |
| psychology | 20 | 2 | 2 | 0 | 0 | 0 | 2 | 0 | 0 |
| yi | 5 | 2 | 2 | 0 | 0 | 2 | 0 | 0 | 0 |
| cognition | 8 | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 0 |
| daily-goods | 1 | 1 | 1 | 0 | 0 | 0 | 1 | 0 | 0 |
| psychiatry | 24 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| **合计** | **4705** | **12796** | **3940** | **153** | **99** | **1291** | **11505** | **0** | **2** |

### 样例（前 8 条/目录，placeholder）

- **accounting**
  - `tools/accounting/amortization-intangible.html` : `如 600000`
  - `tools/accounting/amortization-intangible.html` : `如 0`
  - `tools/accounting/amortization-intangible.html` : `如 10`
  - `tools/accounting/analysis-cost-5.html` : `如 12000`
  - `tools/accounting/analysis-cost-5.html` : `如 40`
  - `tools/accounting/analysis-cost-5.html` : `如 20`
  - `tools/accounting/analysis-cost-5.html` : `如 10`
  - `tools/accounting/analysis-cost-5.html` : `如 180000`
- **acoustics**
  - `tools/acoustics/absorption-coeff-sabine.html` : `如 100`
  - `tools/acoustics/absorption-coeff-sabine.html` : `如 130`
  - `tools/acoustics/absorption-coeff-sabine.html` : `如 0.8`
  - `tools/acoustics/acoustic-impedance.html` : `如 1.2`
  - `tools/acoustics/acoustic-impedance.html` : `如 343`
  - `tools/acoustics/beat-frequency.html` : `如 440`
  - `tools/acoustics/beat-frequency.html` : `如 444`
  - `tools/acoustics/combine-two-spl.html` : `如 80`
- **acupuncture**
  - `tools/acupuncture/acupoint-combination.html` : `如 头痛、失眠`
  - `tools/acupuncture/acupoint-injection.html` : `如 2（1–6）`
  - `tools/acupuncture/acupoint-location.html` : `如 24`
  - `tools/acupuncture/acupoint-location.html` : `如 1.5`
  - `tools/acupuncture/acupoint-location.html` : `如 7.5`
  - `tools/acupuncture/bloodletting-therapy.html` : `如 3（1–20）`
  - `tools/acupuncture/cupping-pressure.html` : `如 10`
  - `tools/acupuncture/ear-acupressure.html` : `如 失眠、胃痛`
- **advertising**
  - `tools/advertising/ad-size.html` : `如 1920`
  - `tools/advertising/ad-size.html` : `如 1080`
  - `tools/advertising/analysis-27.html` : `自家,18 竞品A,35 竞品B,28 竞品C,12 竞品D,7`
  - `tools/advertising/analysis-55.html` : `自家,120000,3600,180,12 竞品A,200000,5000,150,20 竞品B,90000,2700,90,8 竞品C,60000,1500,60,5`
  - `tools/advertising/assessor-52.html` : `如 50000`
  - `tools/advertising/assessor-52.html` : `如 15000`
  - `tools/advertising/assessor-52.html` : `如 20000`
  - `tools/advertising/assessor-52.html` : `如 8000`
- **aerospace**
  - `tools/aerospace/aspect-ratio.html` : `如 10`
  - `tools/aerospace/aspect-ratio.html` : `如 20`
  - `tools/aerospace/assessor-capacity.html` : `如 50000`
  - `tools/aerospace/assessor-capacity.html` : `如 12`
  - `tools/aerospace/assessor-capacity.html` : `如 40`
  - `tools/aerospace/assessor-capacity.html` : `如 20`
  - `tools/aerospace/assessor-capacity.html` : `如 2500`
  - `tools/aerospace/bank-angle-load.html` : `如 60`
- **agriculture**
  - `tools/agriculture/agri-calculator.html` : `如 15（0–100）`
  - `tools/agriculture/agri-calculator.html` : `如 15（0–100）`
  - `tools/agriculture/agri-calculator.html` : `如 15（0–100）`
  - `tools/agriculture/agri-calculator.html` : `如 10`
  - `tools/agriculture/agri-calculator.html` : `如 25`
  - `tools/agriculture/agri-calculator.html` : `如 30`
  - `tools/agriculture/agri-calculator.html` : `如 50`
  - `tools/agriculture/agri-calculator.html` : `如 10`
- **ai**
  - `tools/ai/ai-10.html` : `如 224`
  - `tools/ai/ai-10.html` : `如 3`
  - `tools/ai/ai-10.html` : `如 1`
  - `tools/ai/ai-10.html` : `如 1`
  - `tools/ai/ai-10.html` : `如 1`
  - `tools/ai/ai-11.html` : `如 0.2`
  - `tools/ai/ai-11.html` : `如 0.6`
  - `tools/ai/ai-11.html` : `如 95`
- **aquaculture**
  - `tools/aquaculture/area-power.html` : `如 10`
  - `tools/aquaculture/area-power.html` : `如 1.5`
  - `tools/aquaculture/area-power.html` : `如 3`
  - `tools/aquaculture/area-power.html` : `如 3`
  - `tools/aquaculture/area-power.html` : `如 4`
  - `tools/aquaculture/density-7.html` : `如 6`
  - `tools/aquaculture/density-7.html` : `如 20`
  - `tools/aquaculture/density-7.html` : `如 150`
- **archaeology**
  - `tools/archaeology/artifact-measurement.html` : `如 12.0`
  - `tools/archaeology/artifact-measurement.html` : `如 8.0`
  - `tools/archaeology/artifact-measurement.html` : `如 3.0`
  - `tools/archaeology/artifact-measurement.html` : `如 240`
  - `tools/archaeology/artifact-measurement.html` : `如 9.0`
  - `tools/archaeology/artifact-measurement.html` : `如 5.0`
  - `tools/archaeology/dating-method.html` : `搜索方法 / 材料 / 原理...`
  - `tools/archaeology/pottery-typology.html` : `搜索文化 / 陶质 / 纹饰 / 器形...`
- **astronomy**
  - `tools/astronomy/apparent-magnitude-distance.html` : `如 1`
  - `tools/astronomy/apparent-magnitude-distance.html` : `如 1`
  - `tools/astronomy/atmospheric-refraction.html` : `如 30`
  - `tools/astronomy/convert-15.html` : `如 6`
  - `tools/astronomy/convert-18.html` : `如 1013.25`
  - `tools/astronomy/crater-estimator.html` : `如 100`
  - `tools/astronomy/crater-estimator.html` : `如 3000`
  - `tools/astronomy/crater-estimator.html` : `如 20`
- **audit**
  - `tools/audit/audit-sample.html` : `如 95`
  - `tools/audit/audit-sample.html` : `如 5`
  - `tools/audit/audit-sample.html` : `如 1`
  - `tools/audit/audit-sample.html` : `如 5000`
  - `tools/audit/audit-sample.html` : `如 50000`
  - `tools/audit/audit-sample.html` : `如 10000`
  - `tools/audit/audit-sample.html` : `如 150`
  - `tools/audit/audit-sample.html` : `如 95`
- **automotive**
  - `tools/automotive/analysis-diagnosis.html` : `如 P0301`
  - `tools/automotive/analysis-diagnosis.html` : `如 P0420`
  - `tools/automotive/analysis-diagnosis.html` : `如 U0100`
  - `tools/automotive/analysis-diagnosis.html` : `如 C0035`
  - `tools/automotive/analysis-diagnosis.html` : `如 92`
  - `tools/automotive/analysis-diagnosis.html` : `如 18`
  - `tools/automotive/analysis-diagnosis.html` : `如 750`
  - `tools/automotive/analysis-diagnosis.html` : `如 12`
- **baking**
  - `tools/baking/baker-percentage.html` : `如 500`
  - `tools/baking/baker-percentage.html` : `配料名称（如蜂蜜）`
  - `tools/baking/baker-percentage.html` : `百分比`
  - `tools/baking/baker-percentage.html` : `如 800`
  - `tools/baking/convert-28.html` : `如 500`
  - `tools/baking/convert-28.html` : `如 60`
  - `tools/baking/convert-temp.html` : `如 180`
  - `tools/baking/convert-temp.html` : `如 17`
- **banking**
  - `tools/banking/amortization-first-interest.html` : `如 500000`
  - `tools/banking/amortization-first-interest.html` : `如 4.9`
  - `tools/banking/apy-calculator.html` : `如 0.05`
  - `tools/banking/apy-calculator.html` : `如 12`
  - `tools/banking/bond-current-yield.html` : `如 50`
  - `tools/banking/bond-current-yield.html` : `如 980`
  - `tools/banking/break-even-savings.html` : `如 2`
  - `tools/banking/break-even-savings.html` : `如 5`
- **beauty**
  - `tools/beauty/aging-calculator.html` : `如 25（15–80）`
  - `tools/beauty/analysis-cost-profit.html` : `如 300`
  - `tools/beauty/analysis-cost-profit.html` : `如 260`
  - `tools/beauty/analysis-cost-profit.html` : `如 45`
  - `tools/beauty/analysis-cost-profit.html` : `如 22000`
  - `tools/beauty/analysis-cost-profit.html` : `如 26000`
  - `tools/beauty/analysis-detector-diagnosis.html` : `如 50（0–100）`
  - `tools/beauty/analysis-detector-diagnosis.html` : `如 42（0–100）`
- **biz**
  - `tools/biz/analysis-47.html` : `如 7（0–10）`
  - `tools/biz/analysis-47.html` : `如 8（0–10）`
  - `tools/biz/analysis-47.html` : `如 6（0–10）`
  - `tools/biz/analysis-47.html` : `如 5（0–10）`
  - `tools/biz/analysis-47.html` : `如 6（0–10）`
  - `tools/biz/analysis-47.html` : `如 7（0–10）`
  - `tools/biz/analysis-47.html` : `如 6（0–10）`
  - `tools/biz/analysis-47.html` : `如 5（0–10）`
- **bonding**
  - `tools/bonding/analysis-cost-4.html` : `如：环氧胶,3.5,4,0.5,98`
  - `tools/bonding/analysis-resolution.html` : `如 25`
  - `tools/bonding/analysis-resolution.html` : `如 30`
  - `tools/bonding/assessor-cycle-lifespan.html` : `如 600`
  - `tools/bonding/assessor-cycle-lifespan.html` : `如 200`
  - `tools/bonding/assessor-cycle-lifespan.html` : `如 100`
  - `tools/bonding/assessor-cycle-lifespan.html` : `如 2.0`
  - `tools/bonding/assessor-cycle-lifespan.html` : `如 100`
- **bridge**
  - `tools/bridge/deflection-calc.html` : `如 20`
  - `tools/bridge/deflection-calc.html` : `如 32.5`
  - `tools/bridge/deflection-calc.html` : `如 0.15`
  - `tools/bridge/deflection-calc.html` : `如 30`
  - `tools/bridge/deflection-calc.html` : `如 200`
  - `tools/bridge/foundation-calc.html` : `如 1.2`
  - `tools/bridge/foundation-calc.html` : `如 25`
  - `tools/bridge/foundation-calc.html` : `如 1200`
- **cardiology**
  - `tools/cardiology/ambulatory-bp.html` : `如 142`
  - `tools/cardiology/ambulatory-bp.html` : `如 88`
  - `tools/cardiology/ambulatory-bp.html` : `如 150`
  - `tools/cardiology/ambulatory-bp.html` : `如 92`
  - `tools/cardiology/ambulatory-bp.html` : `如 128`
  - `tools/cardiology/ambulatory-bp.html` : `如 78`
  - `tools/cardiology/ambulatory-bp.html` : `如 120`
  - `tools/cardiology/ambulatory-bp.html` : `如 165`
- **ceramics**
  - `tools/ceramics/clay-shrinkage.html` : `如 120`
  - `tools/ceramics/clay-shrinkage.html` : `如 112`
  - `tools/ceramics/clay-shrinkage.html` : `如 100`
  - `tools/ceramics/clay-shrinkage.html` : `如 100`
  - `tools/ceramics/clay-shrinkage.html` : `如 14（0–50）`
  - `tools/ceramics/glaze-ratio.html` : `如 1000`
  - `tools/ceramics/glaze-temp.html` : `输入锥号或温度筛选`
  - `tools/ceramics/glaze-temp.html` : `如 1200`
- **chemical**
  - `tools/chemical/analysis-cost-7.html` : `例如: 800,200,1200,300`
  - `tools/chemical/analysis-cost-7.html` : `如 2500`
  - `tools/chemical/analysis-cost-7.html` : `如 3`
  - `tools/chemical/calc-pipeline-pressure-drop.html` : `如 200`
  - `tools/chemical/calc-pipeline-pressure-drop.html` : `如 100`
  - `tools/chemical/calc-pipeline-pressure-drop.html` : `如 1.5`
  - `tools/chemical/calc-pipeline-pressure-drop.html` : `如 1000`
  - `tools/chemical/calc-pipeline-pressure-drop.html` : `如 0.001`
- **chemistry**
  - `tools/chemistry/acid-base-titration.html` : `如 0.1`
  - `tools/chemistry/acid-base-titration.html` : `如 25`
  - `tools/chemistry/acid-base-titration.html` : `如 1`
  - `tools/chemistry/acid-base-titration.html` : `如 0.1`
  - `tools/chemistry/acid-base-titration.html` : `如 1`
  - `tools/chemistry/arrhenius.html` : `如 1e13`
  - `tools/chemistry/arrhenius.html` : `如 50000`
  - `tools/chemistry/arrhenius.html` : `如 298`
- **chess**
  - `tools/chess/bridge-scoring.html` : `如 3（1–7）`
  - `tools/chess/bridge-scoring.html` : `如 9（0–13）`
  - `tools/chess/elo-rating.html` : `如 1500（100–3500）`
  - `tools/chess/elo-rating.html` : `如 1600（100–3500）`
  - `tools/chess/elo-rating.html` : `如 1（1–100）`
  - `tools/chess/go-territory.html` : `如 6.5（0–13）`
  - `tools/chess/go-territory.html` : `如 50`
  - `tools/chess/go-territory.html` : `如 3`
- **civil**
  - `tools/civil/active-earth-rankine.html` : `如 18`
  - `tools/civil/active-earth-rankine.html` : `如 5`
  - `tools/civil/active-earth-rankine.html` : `如 30（0–45）`
  - `tools/civil/active-earth-rankine.html` : `如 0`
  - `tools/civil/beam-udl.html` : `如 6`
  - `tools/civil/beam-udl.html` : `如 20`
  - `tools/civil/beam-udl.html` : `如 30`
  - `tools/civil/beam-udl.html` : `如 200`
- **cleaning**
  - `tools/cleaning/area-hours.html` : `如 100`
  - `tools/cleaning/area-hours.html` : `如 2（1–20）`
  - `tools/cleaning/cycle-20.html` : `如 客厅大地毯`
  - `tools/cleaning/cycle-20.html` : `如 8`
  - `tools/cleaning/cycle-20.html` : `如 处理了咖啡渍，吸尘3遍`
  - `tools/cleaning/detector-corrosion.html` : `如 97`
  - `tools/cleaning/detector-corrosion.html` : `如 0.005`
  - `tools/cleaning/detector-corrosion.html` : `如 3`
- **clinical-lab**
  - `tools/clinical-lab/biochemistry-ratio.html` : `如 40`
  - `tools/clinical-lab/biochemistry-ratio.html` : `如 30`
  - `tools/clinical-lab/biochemistry-ratio.html` : `如 100`
  - `tools/clinical-lab/biochemistry-ratio.html` : `如 30`
  - `tools/clinical-lab/biochemistry-ratio.html` : `如 5.0`
  - `tools/clinical-lab/biochemistry-ratio.html` : `如 80`
  - `tools/clinical-lab/biochemistry-ratio.html` : `如 300`
  - `tools/clinical-lab/biochemistry-ratio.html` : `如 40`
- **clinical-nursing**
  - `tools/clinical-nursing/assessor-pressure-risk.html` : `如 3（卧床/约束时长）`
  - `tools/clinical-nursing/assessor-pressure-risk.html` : `如 22（14–40）`
  - `tools/clinical-nursing/assessor-pressure-risk.html` : `如 55（18–100）`
  - `tools/clinical-nursing/convert-flow-concentration.html` : `如 2`
  - `tools/clinical-nursing/cvc-maintenance.html` : `如 1.5（导管标称容积）`
  - `tools/clinical-nursing/cvc-maintenance.html` : `如 2（额外冲管量）`
  - `tools/clinical-nursing/cycle-7.html` : `如：01床 张某`
  - `tools/clinical-nursing/cycle-7.html` : `如：已活动肢体，更换约束部位...`
- **construction**
  - `tools/construction/ac-size-guide.html` : `如 20`
  - `tools/construction/ac-size-guide.html` : `如 2.8（2–6）`
  - `tools/construction/ac-size-guide.html` : `如 1（0–10）`
  - `tools/construction/analysis-43.html` : `如 120000`
  - `tools/construction/analysis-43.html` : `如 80`
  - `tools/construction/analysis-43.html` : `如 600`
  - `tools/construction/analysis-43.html` : `如 250`
  - `tools/construction/area-calculator.html` : `如 5`
- **cosmetic-derm**
  - `tools/cosmetic-derm/area-12.html` : `如 10（0–100）`
  - `tools/cosmetic-derm/area-12.html` : `如 0.2（0.01–5）`
  - `tools/cosmetic-derm/assessor-67.html` : `如 5`
  - `tools/cosmetic-derm/assessor-67.html` : `如 2`
  - `tools/cosmetic-derm/assessor-67.html` : `如 0.5`
  - `tools/cosmetic-derm/assessor-67.html` : `如 0.1`
  - `tools/cosmetic-derm/assessor-67.html` : `如 100`
  - `tools/cosmetic-derm/calc-51.html` : `如 96（0–99.9）`
- **dance**
  - `tools/dance/bpm-rhythm.html` : `如 120（40–240）`
  - `tools/dance/bpm-rhythm.html` : `如 4（2–12）`
  - `tools/dance/bpm-rhythm.html` : `如 1（0.25–8）`
  - `tools/dance/bpm-rhythm.html` : `如 60`
  - `tools/dance/choreography-timeline.html` : `如 120（40–240）`
  - `tools/dance/choreography-timeline.html` : `如 6（2–16）`
  - `tools/dance/choreography-timeline.html` : `如 4（1–16）`
  - `tools/dance/choreography-timeline.html` : `如 0`
- **data**
  - `tools/data/csv-json.html` : `CSV 或 JSON 内容...`
  - `tools/data/csv-to-markdown.html` : `粘贴 CSV 或 Markdown 表格...`
  - `tools/data/csv-to-markdown.html` : `转换结果...`
  - `tools/data/data-cleaner.html` : `每行一条数据`
  - `tools/data/data-cleaner.html` : `如 0`
  - `tools/data/data-cleaner.html` : `清洗后的数据`
  - `tools/data/data-visualizer.html` : `如 8（3–20）`
  - `tools/data/generator-14.html` : `如 5（1–50）`
- **decor**
  - `tools/decor/ceiling-panel-quantity.html` : `如 4.2`
  - `tools/decor/ceiling-panel-quantity.html` : `如 3.6`
  - `tools/decor/ceiling-panel-quantity.html` : `如 600`
  - `tools/decor/ceiling-panel-quantity.html` : `如 600`
  - `tools/decor/ceiling-panel-quantity.html` : `如 5`
  - `tools/decor/curtain-fabric.html` : `如 2.5`
  - `tools/decor/curtain-fabric.html` : `如 2.6`
  - `tools/decor/curtain-fabric.html` : `如 0.05`
- **dentistry**
  - `tools/dentistry/alveolar-bone-loss.html` : `如 8`
  - `tools/dentistry/alveolar-bone-loss.html` : `如 14`
  - `tools/dentistry/assessor-5.html` : `如 0.5（0.2–1.5）`
  - `tools/dentistry/bite-contact.html` : `如 25`
  - `tools/dentistry/bite-contact.html` : `如 25`
  - `tools/dentistry/bite-contact.html` : `如 30`
  - `tools/dentistry/bite-contact.html` : `如 20`
  - `tools/dentistry/bruxism-force.html` : `如 15`
- **dermatology**
  - `tools/dermatology/calc-1.html` : `如 30（0–120）`
  - `tools/dermatology/calc-1.html` : `例如 60`
  - `tools/dermatology/calc-1.html` : `如 9`
  - `tools/dermatology/calc-1.html` : `如 9`
  - `tools/dermatology/calc-1.html` : `如 9`
  - `tools/dermatology/calc-1.html` : `如 18`
  - `tools/dermatology/calc-1.html` : `如 18`
  - `tools/dermatology/calc-1.html` : `如 18`
- **design**
  - `tools/design/analysis-64.html` : `如 7（0–100）`
  - `tools/design/analysis-64.html` : `如 8（0–100）`
  - `tools/design/analysis-64.html` : `如 8（0–100）`
  - `tools/design/analysis-64.html` : `如 7（0–100）`
  - `tools/design/analysis-64.html` : `如 9（0–100）`
  - `tools/design/analysis-64.html` : `如 7.5（0–100）`
  - `tools/design/analysis-64.html` : `如 6（0–100）`
  - `tools/design/analysis-64.html` : `如 9（0–100）`
- **dyeing**
  - `tools/dyeing/assessor-color-diff.html` : `如 50`
  - `tools/dyeing/assessor-color-diff.html` : `如 20`
  - `tools/dyeing/assessor-color-diff.html` : `如 10`
  - `tools/dyeing/assessor-color-diff.html` : `如 51`
  - `tools/dyeing/assessor-color-diff.html` : `如 21.5`
  - `tools/dyeing/assessor-color-diff.html` : `如 9`
  - `tools/dyeing/assessor-color-diff.html` : `如 2`
  - `tools/dyeing/assessor-color-diff.html` : `如 1`
- **dynamics**
  - `tools/dynamics/angular-momentum-conservation.html` : `如 2`
  - `tools/dynamics/angular-momentum-conservation.html` : `如 10`
  - `tools/dynamics/angular-momentum-conservation.html` : `如 1`
  - `tools/dynamics/angular-momentum.html` : `如 0.5`
  - `tools/dynamics/angular-momentum.html` : `如 10`
  - `tools/dynamics/banked-curve.html` : `如 50`
  - `tools/dynamics/banked-curve.html` : `如 30`
  - `tools/dynamics/banked-curve.html` : `如 9.81`
- **eco**
  - `tools/eco/afforestation-cost.html` : `如 1000`
  - `tools/eco/afforestation-cost.html` : `如 30`
  - `tools/eco/afforestation-cost.html` : `如 20`
  - `tools/eco/aqi-converter.html` : `如 75`
  - `tools/eco/aqi.html` : `如 85`
  - `tools/eco/aqi.html` : `如 30`
  - `tools/eco/aqi.html` : `如 2`
  - `tools/eco/battery-storage.html` : `如 100`
- **ecommerce**
  - `tools/ecommerce/analysis-25.html` : `A商品,89,99`
  - `tools/ecommerce/analysis-70.html` : `第1期,120000,3400,3.5,28 第2期,138000,3900,3.1,26 第3期,152000,4200,2.8,25`
  - `tools/ecommerce/analysis-71.html` : `竞品A,199,5200,4.8,2 竞品B,229,3100,4.6,3 竞品C,179,8800,4.9,1`
  - `tools/ecommerce/analysis-conversion-funnel.html` : `例如: 曝光,10000`
  - `tools/ecommerce/analysis-cost-8.html` : `如 60000`
  - `tools/ecommerce/analysis-cost-8.html` : `如 30`
  - `tools/ecommerce/analysis-cost-8.html` : `如 50`
  - `tools/ecommerce/analysis-cost-8.html` : `如 5000`
- **economics**
  - `tools/economics/average-propensity-consume.html` : `如 800`
  - `tools/economics/average-propensity-consume.html` : `如 1000`
  - `tools/economics/balance-of-trade.html` : `如 200`
  - `tools/economics/balance-of-trade.html` : `如 180`
  - `tools/economics/cobb-douglas.html` : `如 1`
  - `tools/economics/cobb-douglas.html` : `如 200`
  - `tools/economics/cobb-douglas.html` : `如 0.3`
  - `tools/economics/cobb-douglas.html` : `如 100`
- **edu**
  - `tools/edu/assessor-27.html` : `如 6（1–10）`
  - `tools/edu/assessor-27.html` : `如 5（1–10）`
  - `tools/edu/assessor-27.html` : `如 7（1–10）`
  - `tools/edu/assessor-27.html` : `如 4（1–10）`
  - `tools/edu/assessor-27.html` : `如 7（1–10）`
  - `tools/edu/assessor-27.html` : `如 8（1–10）`
  - `tools/edu/calc-2.html` : `如 85`
  - `tools/edu/calc-2.html` : `如 75`
- **edu2**
  - `tools/edu2/exam-analysis.html` : `如 100`
  - `tools/edu2/exam-analysis.html` : `如 60（0–100）`
  - `tools/edu2/exam-analysis.html` : `如 85（0–100）`
  - `tools/edu2/exam-analysis.html` : `姓名,分数 例如： 张三,92 李四,85 王五,78 或直接输入分数： 92 85 78`
  - `tools/edu2/schedule-conflict.html` : `课程名,教师,教室,星期,起始节,结束节 例如： 高等数学,张老师,A101,1,1,2 线性代数,张老师,B202,1,1,2 英语,李老师,A101,1,3,4`
  - `tools/edu2/study-progress.html` : `如 4`
  - `tools/edu2/study-progress.html` : `科目,已完成,总数,每任务小时 例如： 数学,45,80,1.5 英语,30,60,1 专业课,20,100,2`
  - `tools/edu2/wrong-book.html` : `如：数学`
- **elderly**
  - `tools/elderly/aid-height.html` : `如 165（120–210）`
  - `tools/elderly/aid-height.html` : `如 2（0–10）`
  - `tools/elderly/assessor-35.html` : `如 75`
  - `tools/elderly/bp-trend.html` : `如 130`
  - `tools/elderly/bp-trend.html` : `如 85`
  - `tools/elderly/bp-trend.html` : `如 72`
  - `tools/elderly/bp-trend.html` : `如 6.1`
  - `tools/elderly/medication-schedule.html` : `如 3（1–30）`
- **electrical**
  - `tools/electrical/battery-bank.html` : `如 3.2`
  - `tools/electrical/battery-bank.html` : `如 100`
  - `tools/electrical/battery-bank.html` : `如 16`
  - `tools/electrical/battery-bank.html` : `如 2`
  - `tools/electrical/battery-bank.html` : `如 500`
  - `tools/electrical/battery-bank.html` : `如 80（1–100）`
  - `tools/electrical/battery-bank.html` : `如 90（1–100）`
  - `tools/electrical/breaker-sizing.html` : `如 10`
- **electromagnetism**
  - `tools/electromagnetism/b-field-wire.html` : `如 10`
  - `tools/electromagnetism/b-field-wire.html` : `如 0.01`
  - `tools/electromagnetism/capacitance-parallel-plate.html` : `如 1`
  - `tools/electromagnetism/capacitance-parallel-plate.html` : `如 0.01`
  - `tools/electromagnetism/capacitance-parallel-plate.html` : `如 1e-3`
  - `tools/electromagnetism/capacitive-reactance.html` : `如 60`
  - `tools/electromagnetism/capacitive-reactance.html` : `如 1`
  - `tools/electromagnetism/capacitors-parallel.html` : `如 10`
- **electronics**
  - `tools/electronics/analysis-22.html` : `如 3.7`
  - `tools/electronics/analysis-22.html` : `如 25`
  - `tools/electronics/analysis-22.html` : `如 0.05`
  - `tools/electronics/analysis-22.html` : `如 5（0–100）`
  - `tools/electronics/analysis-22.html` : `如 2000`
  - `tools/electronics/bandwidth.html` : `如 10`
  - `tools/electronics/bandwidth.html` : `如 100000`
  - `tools/electronics/calc-63.html` : `如 2`
- **encode**
  - `tools/encode/ascii-readability.html` : `如 100`
  - `tools/encode/ascii-readability.html` : `如 8`
  - `tools/encode/ascii-readability.html` : `如 2`
  - `tools/encode/base32.html` : `如 100`
  - `tools/encode/base32.html` : `如 1`
  - `tools/encode/base32.html` : `如 0`
  - `tools/encode/base58.html` : `如 25`
  - `tools/encode/base58.html` : `如 4`
- **endocrinology**
  - `tools/endocrinology/aldosterone-renin.html` : `如 22`
  - `tools/endocrinology/aldosterone-renin.html` : `如 0.6`
  - `tools/endocrinology/aldosterone-renin.html` : `如 3.2`
  - `tools/endocrinology/aldosterone-renin.html` : `如 155`
  - `tools/endocrinology/calcium-pth-axis.html` : `如 2.85`
  - `tools/endocrinology/calcium-pth-axis.html` : `如 40`
  - `tools/endocrinology/calcium-pth-axis.html` : `如 85`
  - `tools/endocrinology/calcium-pth-axis.html` : `如 0.78`
- **energy**
  - `tools/energy/air-purifier-area.html` : `如 400`
  - `tools/energy/air-purifier-area.html` : `如 0.10（0.05–0.15）`
  - `tools/energy/assessor-water-quality.html` : `如 150`
  - `tools/energy/assessor-water-quality.html` : `如 20`
  - `tools/energy/battery-capacity-wh.html` : `如 50`
  - `tools/energy/battery-capacity-wh.html` : `如 12`
  - `tools/energy/battery-capacity-wh.html` : `如 100`
  - `tools/energy/battery-life.html` : `如 4000`
- **engineering**
  - `tools/engineering/axial-stress.html` : `如 50`
  - `tools/engineering/axial-stress.html` : `如 500`
  - `tools/engineering/axial-stress.html` : `如 200`
  - `tools/engineering/axial-stress.html` : `如 2`
  - `tools/engineering/beam-calculator.html` : `如 5`
  - `tools/engineering/beam-calculator.html` : `如 10`
  - `tools/engineering/beam-calculator.html` : `如 200`
  - `tools/engineering/beam-calculator.html` : `如 500`
- **ent**
  - `tools/ent/ahi-severity.html` : `如 30`
  - `tools/ent/ahi-severity.html` : `如 50`
  - `tools/ent/ahi-severity.html` : `如 6`
  - `tools/ent/ahi-severity.html` : `如 82（0–100）`
  - `tools/ent/ahi-severity.html` : `如 60`
  - `tools/ent/ahi-severity.html` : `如 40`
  - `tools/ent/allergy-skin-test.html` : `如 8`
  - `tools/ent/allergy-skin-test.html` : `如 20`
- **exhibition**
  - `tools/exhibition/analysis-61.html` : `如 2000`
  - `tools/exhibition/analysis-61.html` : `展位费,120000,120000`
  - `tools/exhibition/analysis-pnl.html` : `如 400`
  - `tools/exhibition/analysis-pnl.html` : `如 12（0–100）`
  - `tools/exhibition/analysis-pnl.html` : `如 8500`
  - `tools/exhibition/analysis-pnl.html` : `如 60（0–100）`
  - `tools/exhibition/analysis-pnl.html` : `如 30000`
  - `tools/exhibition/analysis-pnl.html` : `如 8000`
- **film**
  - `tools/film/aspect-ratio.html` : `如 1920`
  - `tools/film/aspect-ratio.html` : `如 1080`
  - `tools/film/aspect-ratio.html` : `如 1920`
  - `tools/film/aspect-ratio.html` : `如 1080`
  - `tools/film/color-grading.html` : `搜索LUT名称…`
  - `tools/film/convert-time-1.html` : `如 0`
  - `tools/film/convert-time-1.html` : `如 0`
  - `tools/film/convert-time-1.html` : `如 10`
- **finance**
  - `tools/finance/aadhaar-validator.html` : `如：234123412346`
  - `tools/finance/aba-validator.html` : `如：021000021`
  - `tools/finance/abn-validator.html` : `如：51 824 753 556`
  - `tools/finance/amount-in-words.html` : `如 1234.56`
  - `tools/finance/analysis-44.html` : `如 1000000`
  - `tools/finance/analysis-44.html` : `如 1080000`
  - `tools/finance/analysis-44.html` : `例如: 主体工程,500000,530000`
  - `tools/finance/analysis-5.html` : `如 500000`
- **fire-rescue**
  - `tools/fire-rescue/calc-3.html` : `探测+反应时间`
  - `tools/fire-rescue/calc-pressure-1.html` : `如 20`
  - `tools/fire-rescue/calc-pressure-1.html` : `如 6.5`
  - `tools/fire-rescue/calc-time-response.html` : `如 50`
  - `tools/fire-rescue/calc-time-response.html` : `如 300`
  - `tools/fire-rescue/calc-time-response.html` : `如 2.0`
  - `tools/fire-rescue/calc-time-response.html` : `如 20`
  - `tools/fire-rescue/calc-time-response.html` : `如 68`
- **fire**
  - `tools/fire/analysis-cost-price-8.html` : `如 120`
  - `tools/fire/analysis-cost-price-8.html` : `如 75`
  - `tools/fire/analysis-cost-price-8.html` : `例如: 105,110,125,130`
  - `tools/fire/calc-water-pressure-hydrant.html` : `如 0.55`
  - `tools/fire/calc-water-pressure-hydrant.html` : `如 12`
  - `tools/fire/calc-water-pressure-hydrant.html` : `如 0.35`
  - `tools/fire/calc-water-pressure-hydrant.html` : `如 0.08`
  - `tools/fire/detector-178.html` : `如 1`
- **fishery**
  - `tools/fishery/aerator-duration.html` : `如 5`
  - `tools/fishery/aerator-duration.html` : `如 1.2`
  - `tools/fishery/aerator-duration.html` : `如 3.0`
  - `tools/fishery/aerator-duration.html` : `如 5.0`
  - `tools/fishery/aerator-duration.html` : `如 3`
  - `tools/fishery/aerator-duration.html` : `如 1.5`
  - `tools/fishery/aerator-duration.html` : `如 0.3`
  - `tools/fishery/assessor-risk-4.html` : `如 25`
- **fitness**
  - `tools/fitness/analysis-retention.html` : `如 1000`
  - `tools/fitness/analysis-retention.html` : `如 620`
  - `tools/fitness/analysis-retention.html` : `如 6`
  - `tools/fitness/angle-motion.html` : `如 90（0–180）`
  - `tools/fitness/angle-motion.html` : `如 35`
  - `tools/fitness/angle-motion.html` : `如 10`
  - `tools/fitness/assessor-18.html` : `如 60`
  - `tools/fitness/assessor-18.html` : `如 40`
- **floral**
  - `tools/floral/golden-ratio.html` : `如 15`
  - `tools/floral/golden-ratio.html` : `如 12`
  - `tools/floral/preservative.html` : `如 500`
  - `tools/floral/price.html` : `如 5000`
  - `tools/floral/price.html` : `如 150`
  - `tools/floral/price.html` : `如 300`
  - `tools/floral/price.html` : `如 80`
  - `tools/floral/price.html` : `如 200`
- **fluid**
  - `tools/fluid/bernoulli-pressure.html` : `如 101325`
  - `tools/fluid/bernoulli-pressure.html` : `如 1`
  - `tools/fluid/bernoulli-pressure.html` : `如 3`
  - `tools/fluid/bernoulli-pressure.html` : `如 1000`
  - `tools/fluid/buoyancy-force.html` : `如 1000`
  - `tools/fluid/buoyancy-force.html` : `如 0.05`
  - `tools/fluid/buoyancy-force.html` : `如 9.8`
  - `tools/fluid/capillary-pressure.html` : `如 0.072`
- **food-processing**
  - `tools/food-processing/additive-limit-lookup.html` : `如：防腐剂、苯甲酸、饮料、抗氧化`
  - `tools/food-processing/dough-absorption.html` : `如 1000`
  - `tools/food-processing/dough-absorption.html` : `如 13.5（0–100）`
  - `tools/food-processing/dough-absorption.html` : `如 620`
  - `tools/food-processing/dough-absorption.html` : `如 0`
  - `tools/food-processing/dough-absorption.html` : `如 20`
  - `tools/food-processing/dough-absorption.html` : `如 2（0–100）`
  - `tools/food-processing/emulsion-stability.html` : `如 50`
- **food-testing**
  - `tools/food-testing/acid-peroxide-titration.html` : `如 2.50`
  - `tools/food-testing/acid-peroxide-titration.html` : `如 0.1000`
  - `tools/food-testing/acid-peroxide-titration.html` : `如 3.00`
  - `tools/food-testing/acid-peroxide-titration.html` : `如 3`
  - `tools/food-testing/acid-peroxide-titration.html` : `如 12.50`
  - `tools/food-testing/acid-peroxide-titration.html` : `如 0.20`
  - `tools/food-testing/acid-peroxide-titration.html` : `如 0.0020`
  - `tools/food-testing/acid-peroxide-titration.html` : `如 2.00`
- **food**
  - `tools/food/analysis-cost-6.html` : `如 58`
  - `tools/food/analysis-cost-6.html` : `如 15`
  - `tools/food/analysis-cost-6.html` : `如 5`
  - `tools/food/analysis-cost-6.html` : `如 2`
  - `tools/food/analysis-cost-6.html` : `如 4`
  - `tools/food/analysis-cost-6.html` : `如 55（0–100）`
  - `tools/food/analysis-menu.html` : `宫保鸡丁,12,32,180`
  - `tools/food/beer-gravity-estimator.html` : `如 20`
- **forensic-medicine**
  - `tools/forensic-medicine/abuse-pattern.html` : `如 3（0–120）`
  - `tools/forensic-medicine/bloodstain-pattern.html` : `如 10`
  - `tools/forensic-medicine/bloodstain-pattern.html` : `如 6`
  - `tools/forensic-medicine/bloodstain-pattern.html` : `如 0`
  - `tools/forensic-medicine/bloodstain-pattern.html` : `如 50`
  - `tools/forensic-medicine/bloodstain-pattern.html` : `如 45`
  - `tools/forensic-medicine/bloodstain-pattern.html` : `如 80`
  - `tools/forensic-medicine/bloodstain-pattern.html` : `如 50`
- **forestry**
  - `tools/forestry/area-18.html` : `如 1`
  - `tools/forestry/calc-57.html` : `如 100`
  - `tools/forestry/calc-57.html` : `如 65`
  - `tools/forestry/concentration-5.html` : `如 1800`
  - `tools/forestry/density-5.html` : `如 600`
  - `tools/forestry/density-5.html` : `如 80`
  - `tools/forestry/density-5.html` : `如 16`
  - `tools/forestry/density-6.html` : `如 2`
- **forex**
  - `tools/forex/cross-rate.html` : `如 1.0850`
  - `tools/forex/cross-rate.html` : `如 0.00665`
  - `tools/forex/cross-rate.html` : `如 1000`
  - `tools/forex/leverage-calc.html` : `如 1`
  - `tools/forex/leverage-calc.html` : `如 1`
  - `tools/forex/leverage-calc.html` : `如 10000`
  - `tools/forex/leverage-calc.html` : `如 50（0–100）`
  - `tools/forex/lot-size.html` : `如 10000`
- **fun**
  - `tools/fun/1a2b-guess.html` : `依次输入数字`
  - `tools/fun/anagram-game.html` : `输入一个单词`
  - `tools/fun/daily-riddle.html` : `在此输入你的答案，回车提交`
  - `tools/fun/generator-2.html` : `如 5（1–50）`
  - `tools/fun/generator-24.html` : `如 5（1–50）`
  - `tools/fun/generator-3.html` : `如 5（1–50）`
  - `tools/fun/generator-laugh.html` : `如 5（1–50）`
  - `tools/fun/keyboard-heatmap.html` : `点击此处开始打字，按键分布会实时显示在下方键盘热力图上…`
- **funeral**
  - `tools/funeral/ceremony-timeline.html` : `时间`
  - `tools/funeral/ceremony-timeline.html` : `环节名称`
  - `tools/funeral/ceremony-timeline.html` : `时长(分钟)`
  - `tools/funeral/ceremony-timeline.html` : `说明（选填）`
  - `tools/funeral/funeral-budget-planner.html` : `项目名称（如：骨灰盒）`
  - `tools/funeral/funeral-budget-planner.html` : `金额（元）`
  - `tools/funeral/grave-design.html` : `如 0.8`
  - `tools/funeral/grave-design.html` : `如 1.0`
- **futures**
  - `tools/futures/futures-pricing.html` : `如 5000`
  - `tools/futures/futures-pricing.html` : `如 4`
  - `tools/futures/futures-pricing.html` : `如 0.25`
  - `tools/futures/futures-pricing.html` : `如 1`
  - `tools/futures/futures-pricing.html` : `如 0.5`
  - `tools/futures/futures-pricing.html` : `如 5075`
  - `tools/futures/hedge-ratio.html` : `如 3`
  - `tools/futures/hedge-ratio.html` : `如 3.5`
- **gardening**
  - `tools/gardening/compost-calculator.html` : `配方名称（如：标准菜叶堆肥）`
  - `tools/gardening/garden-layout.html` : `如 20`
  - `tools/gardening/garden-tools.html` : `工具名/用途关键词...`
  - `tools/gardening/pest-identifier.html` : `如：黄叶、蚜虫、白粉病、月季...`
  - `tools/gardening/plant-calendar.html` : `🔍 搜索蔬菜名称...`
  - `tools/gardening/plant-care.html` : `如：绿萝、月季、多肉...`
  - `tools/gardening/pruning-calendar.html` : `输入植物名称，如：月季、桂花`
  - `tools/gardening/recommender.html` : `如 5（1–50）`
- **gas**
  - `tools/gas/calc-68.html` : `如 100`
  - `tools/gas/calc-68.html` : `如 60`
  - `tools/gas/concentration-7.html` : `如 1000`
  - `tools/gas/concentration-7.html` : `如 20`
  - `tools/gas/concentration-7.html` : `如 100`
  - `tools/gas/concentration-8.html` : `如 1.0`
  - `tools/gas/current-2.html` : `如 50`
  - `tools/gas/current-2.html` : `如 100`
- **gastroenterology**
  - `tools/gastroenterology/bilirubin-ratio.html` : `如 85`
  - `tools/gastroenterology/bilirubin-ratio.html` : `如 55`
  - `tools/gastroenterology/calc-1.html` : `例如 35`
  - `tools/gastroenterology/calc-1.html` : `例如 32`
  - `tools/gastroenterology/calc-1.html` : `例如 1.5`
  - `tools/gastroenterology/cdai.html` : `如 14`
  - `tools/gastroenterology/cdai.html` : `如 10`
  - `tools/gastroenterology/cdai.html` : `如 7`
- **general**
  - `tools/general/air-1.html` : `如 35`
  - `tools/general/air-1.html` : `如 60`
  - `tools/general/air-1.html` : `如 20`
  - `tools/general/air-1.html` : `如 40`
  - `tools/general/air-1.html` : `如 1.0`
  - `tools/general/air-1.html` : `如 80`
  - `tools/general/assessor-20.html` : `如 5`
  - `tools/general/assessor-20.html` : `如 15`
- **geology**
  - `tools/geology/analysis-32.html` : `西翼,270,30`
  - `tools/geology/analysis-33.html` : `如 5`
  - `tools/geology/analysis-cost-2.html` : `如 6`
  - `tools/geology/analysis-cost-2.html` : `如 1800`
  - `tools/geology/analysis-cost-2.html` : `如 150`
  - `tools/geology/analysis-cost-2.html` : `如 45`
  - `tools/geology/analysis-cost-2.html` : `如 2600`
  - `tools/geology/analysis-cost-2.html` : `如 60000`
- **geometry**
  - `tools/geometry/angle-between-vectors.html` : `如 1`
  - `tools/geometry/angle-between-vectors.html` : `如 0`
  - `tools/geometry/angle-between-vectors.html` : `如 0`
  - `tools/geometry/angle-between-vectors.html` : `如 1`
  - `tools/geometry/arc-length.html` : `如 10`
  - `tools/geometry/arc-length.html` : `如 90`
  - `tools/geometry/chord-length.html` : `如 10`
  - `tools/geometry/chord-length.html` : `如 90`
- **glass**
  - `tools/glass/annealing-curve.html` : `如 6`
  - `tools/glass/annealing-curve.html` : `如 50（20–300）`
  - `tools/glass/cutting-score.html` : `如 1830`
  - `tools/glass/cutting-score.html` : `如 1220`
  - `tools/glass/cutting-score.html` : `如 5`
  - `tools/glass/cutting-score.html` : `如 400`
  - `tools/glass/cutting-score.html` : `如 300`
  - `tools/glass/cutting-score.html` : `如 3`
- **health**
  - `tools/health/alcohol-units.html` : `如 2`
  - `tools/health/alcohol-units.html` : `如 5`
  - `tools/health/alcohol-units.html` : `如 330`
  - `tools/health/alcohol-units.html` : `如 65`
  - `tools/health/alcohol-units.html` : `如 0`
  - `tools/health/blood-pressure-classifier.html` : `如 120`
  - `tools/health/blood-pressure-classifier.html` : `如 80`
  - `tools/health/blood-pressure-classifier.html` : `如 40`
- **healthcare**
  - `tools/healthcare/analysis-report-cost.html` : `内科,1200000,980000`
  - `tools/healthcare/antipyretic-dose.html` : `如 15`
  - `tools/healthcare/antipyretic-dose.html` : `如 4（0–18；2 月龄填 0.17）`
  - `tools/healthcare/antipyretic-dose.html` : `如 15`
  - `tools/healthcare/antipyretic-dose.html` : `如 32`
  - `tools/healthcare/apgar.html` : `如 2`
  - `tools/healthcare/apgar.html` : `如 2`
  - `tools/healthcare/apgar.html` : `如 2`
- **hematology**
  - `tools/hematology/anemia-classification.html` : `如 85`
  - `tools/hematology/anemia-classification.html` : `如 3.5`
  - `tools/hematology/anemia-classification.html` : `如 27`
  - `tools/hematology/anemia-classification.html` : `如 75`
  - `tools/hematology/anemia-classification.html` : `如 24`
  - `tools/hematology/anemia-classification.html` : `如 300`
  - `tools/hematology/anemia-differential.html` : `如 72`
  - `tools/hematology/anemia-differential.html` : `如 1.2`
- **home**
  - `tools/home/furniture-layout.html` : `如 5（1–20）`
  - `tools/home/furniture-layout.html` : `如 4（1–20）`
  - `tools/home/lighting-calculator.html` : `如 5`
  - `tools/home/lighting-calculator.html` : `如 4`
  - `tools/home/lighting-calculator.html` : `如 2.8`
  - `tools/home/lighting-calculator.html` : `如 800`
  - `tools/home/lighting-calculator.html` : `如 0.6（0.1–1）`
  - `tools/home/lighting-calculator.html` : `如 0.8（0.1–1）`
- **hotel**
  - `tools/hotel/currency-exchange.html` : `如 0.138`
  - `tools/hotel/currency-exchange.html` : `如 0`
  - `tools/hotel/currency-exchange.html` : `如 10000`
  - `tools/hotel/itinerary-planner.html` : `如 5`
  - `tools/hotel/itinerary-planner.html` : `如 8（1–16）`
  - `tools/hotel/itinerary-planner.html` : `如 6（1–30）`
  - `tools/hotel/itinerary-planner.html` : `如 3`
  - `tools/hotel/luggage-weight.html` : `如 7（1–60）`
- **hr**
  - `tools/hr/analysis-29.html` : `如 130`
  - `tools/hr/analysis-29.html` : `如 120`
  - `tools/hr/analysis-29.html` : `如 15`
  - `tools/hr/analysis-29.html` : `如 18000`
  - `tools/hr/analysis-29.html` : `如 3`
  - `tools/hr/analysis-29.html` : `如 25000`
  - `tools/hr/annual-leave-calc.html` : `如 1`
  - `tools/hr/annual-leave-calc.html` : `如 12（0–12）`
- **hvac**
  - `tools/hvac/air-filter.html` : `如 2000`
  - `tools/hvac/air-filter.html` : `如 592`
  - `tools/hvac/air-filter.html` : `如 592`
  - `tools/hvac/air-filter.html` : `留空则按宽×高计算`
  - `tools/hvac/chiller-efficiency.html` : `如 500`
  - `tools/hvac/chiller-efficiency.html` : `如 142.17`
  - `tools/hvac/chiller-efficiency.html` : `如 90`
  - `tools/hvac/chiller-efficiency.html` : `如 12`
- **hydraulic**
  - `tools/hydraulic/analysis-frequency.html` : `例如: 1200,1500,1800,2100,1400`
  - `tools/hydraulic/analysis-frequency.html` : `如 100`
  - `tools/hydraulic/area-capacity.html` : `水位(m) 面积(m²) 100 0 105 1200 110 3500 115 7200 120 12500`
  - `tools/hydraulic/area-capacity.html` : `如 112`
  - `tools/hydraulic/assessor-22.html` : `如 0.12`
  - `tools/hydraulic/assessor-22.html` : `如 0.20`
  - `tools/hydraulic/assessor-22.html` : `如 50`
  - `tools/hydraulic/assessor-22.html` : `如 30`
- **image**
  - `tools/image/generator-15.html` : `如 5（1–50）`
  - `tools/image/image-collage.html` : `如 2（1–20）`
  - `tools/image/image-collage.html` : `如 3（1–20）`
  - `tools/image/image-collage.html` : `如 1200（100–8000）`
  - `tools/image/image-resize.html` : `宽度`
  - `tools/image/image-resize.html` : `高度`
  - `tools/image/image-watermark.html` : `输入水印文字`
  - `tools/image/image-watermark.html` : `如 20`
- **insurance**
  - `tools/insurance/annuity-certain-pv.html` : `如 12000`
  - `tools/insurance/annuity-certain-pv.html` : `如 0.03`
  - `tools/insurance/annuity-certain-pv.html` : `如 15`
  - `tools/insurance/annuity-nsp.html` : `如 1000`
  - `tools/insurance/annuity-nsp.html` : `如 15`
  - `tools/insurance/annuity-present.html` : `如 10000`
  - `tools/insurance/annuity-present.html` : `如 5（0–100）`
  - `tools/insurance/annuity-present.html` : `如 20`
- **investment**
  - `tools/investment/annuity-fv-inv.html` : `如 1000`
  - `tools/investment/annuity-fv-inv.html` : `如 0.05`
  - `tools/investment/annuity-fv-inv.html` : `如 10`
  - `tools/investment/annuity-pv-inv.html` : `如 1000`
  - `tools/investment/annuity-pv-inv.html` : `如 0.05`
  - `tools/investment/annuity-pv-inv.html` : `如 10`
  - `tools/investment/bond-price.html` : `如 1000`
  - `tools/investment/bond-price.html` : `如 5`
- **it**
  - `tools/it/a1z26-cipher.html` : `输入要编码的文本或要解码的数字串...`
  - `tools/it/a1z26-cipher.html` : `结果将显示在这里...`
  - `tools/it/adfgvx-cipher.html` : `可填 0-9A-Z 共 36 个字符的置换`
  - `tools/it/adfgvx-cipher.html` : `字母密钥`
  - `tools/it/adfgvx-cipher.html` : `输入要加密的明文或要解密的密文...`
  - `tools/it/adfgvx-cipher.html` : `结果将显示在这里...`
  - `tools/it/aes-encryptor.html` : `加密密码/密钥`
  - `tools/it/aes-encryptor.html` : `留空自动生成，加密时随机生成`
- **jewelry**
  - `tools/jewelry/convert-31.html` : `如 1`
  - `tools/jewelry/diamond-carat.html` : `如 6.5`
  - `tools/jewelry/diamond-carat.html` : `如 0`
  - `tools/jewelry/diamond-carat.html` : `如 3.9`
  - `tools/jewelry/gem-hardness.html` : `如：钻石、红宝石...`
  - `tools/jewelry/gold-purity.html` : `如 10`
  - `tools/jewelry/gold-purity.html` : `如 750（0–1000）`
  - `tools/jewelry/pearl-grading.html` : `如 9（2–25）`
- **kinematics**
  - `tools/kinematics/angular-accel.html` : `如 10`
  - `tools/kinematics/angular-accel.html` : `如 2`
  - `tools/kinematics/angular-displacement.html` : `如 2`
  - `tools/kinematics/angular-displacement.html` : `如 1`
  - `tools/kinematics/angular-displacement.html` : `如 3`
  - `tools/kinematics/angular-final-velocity.html` : `如 2`
  - `tools/kinematics/angular-final-velocity.html` : `如 1`
  - `tools/kinematics/angular-final-velocity.html` : `如 3`
- **language**
  - `tools/language/calc-1.html` : `如 60（0–100）`
  - `tools/language/calc-2.html` : `如 800`
  - `tools/language/calc-2.html` : `如 80（0–100）`
  - `tools/language/calc-2.html` : `如 3`
  - `tools/language/calc-2.html` : `如 30（0–59）`
  - `tools/language/french-verb-conjugator.html` : `输入动词原形，如 parler, finir, avoir...`
  - `tools/language/generator-19.html` : `如：Application Programming Interface / 人工智能`
  - `tools/language/german-gender-quiz.html` : `输入德语名词，如 Haus, Blume, Kind...`
- **leather**
  - `tools/leather/area-20.html` : `如 2.5`
  - `tools/leather/area-20.html` : `如 18`
  - `tools/leather/assessor-21.html` : `如 2.0`
  - `tools/leather/assessor-21.html` : `如 1.6`
  - `tools/leather/assessor-21.html` : `如 8（1–10）`
  - `tools/leather/assessor-21.html` : `如 4（1–5）`
  - `tools/leather/calc-dosage-4.html` : `如 100`
  - `tools/leather/calc-dosage-4.html` : `如 2.0`
- **legal**
  - `tools/legal/arbitration-fee.html` : `如 500000`
  - `tools/legal/calc-96.html` : `如 50000`
  - `tools/legal/calc-96.html` : `如 10`
  - `tools/legal/calc-interest.html` : `如 100000`
  - `tools/legal/calc-interest.html` : `如 12`
  - `tools/legal/calc-interest.html` : `如 12`
  - `tools/legal/calc-interest.html` : `如 3.1`
  - `tools/legal/calculator-calc-6.html` : `如 100000`
- **library**
  - `tools/library/archive-label.html` : `如 1`
  - `tools/library/archive-label.html` : `如 5（1–200）`
  - `tools/library/archive-label.html` : `如 50`
  - `tools/library/citation-format.html` : `如 1`
  - `tools/library/clc-classifier.html` : `输入主题词搜索分类`
  - `tools/library/overdue-fine.html` : `如 30`
  - `tools/library/overdue-fine.html` : `如 0.5`
  - `tools/library/overdue-fine.html` : `如 1`
- **life**
  - `tools/life/age-calculator.html` : `如 1995（1900–2100）`
  - `tools/life/age-calculator.html` : `如 1（1–12）`
  - `tools/life/age-calculator.html` : `如 1（1–31）`
  - `tools/life/age-calculator.html` : `如 0（0–23）`
  - `tools/life/age-calculator.html` : `如 0（0–59）`
  - `tools/life/age-calculator.html` : `如 0（0–59）`
  - `tools/life/analysis-23.html` : `A栋,30,36`
  - `tools/life/analysis-23.html` : `如 1.2`
- **livestock**
  - `tools/livestock/ammonia-ventilation.html` : `如 25`
  - `tools/livestock/ammonia-ventilation.html` : `如 15`
  - `tools/livestock/ammonia-ventilation.html` : `如 30`
  - `tools/livestock/ammonia-ventilation.html` : `如 10`
  - `tools/livestock/ammonia-ventilation.html` : `如 3`
  - `tools/livestock/ammonia-ventilation.html` : `如 0`
  - `tools/livestock/analysis-18.html` : `如 10000`
  - `tools/livestock/analysis-18.html` : `如 7`
- **logistics**
  - `tools/logistics/analysis-75.html` : `如：生鲜,1000,60,25`
  - `tools/logistics/analysis-76.html` : `顺达,2,12,0.8,320 云运,3,9,1.5,180 安捷,1,18,0.3,90`
  - `tools/logistics/analysis-cycle-1.html` : `如：A-001,100,97`
  - `tools/logistics/analysis-report.html` : `经营,销售回款,500000`
  - `tools/logistics/assessor-carbon.html` : `如 10`
  - `tools/logistics/assessor-carbon.html` : `如 500`
  - `tools/logistics/assessor-carbon.html` : `如 120`
  - `tools/logistics/assessor-carbon.html` : `如 30`
- **logistics2**
  - `tools/logistics2/inventory-aging.html` : `如 90`
  - `tools/logistics2/inventory-aging.html` : `如 180`
  - `tools/logistics2/inventory-aging.html` : `名称,库存量,出库量,库龄天,单价 例如： 矿泉水,5000,12000,30,2.5 纸巾,2000,3000,45,5 旧款锅具,800,50,220,80`
  - `tools/logistics2/loading-utilization.html` : `如 6.8`
  - `tools/logistics2/loading-utilization.html` : `如 2.3`
  - `tools/logistics2/loading-utilization.html` : `如 2.4`
  - `tools/logistics2/loading-utilization.html` : `如 5000`
  - `tools/logistics2/loading-utilization.html` : `如 0.6`
- **machinery**
  - `tools/machinery/analysis-casting.html` : `如 1000`
  - `tools/machinery/analysis-casting.html` : `如 400`
  - `tools/machinery/analysis-casting.html` : `如 7.2`
  - `tools/machinery/analysis-casting.html` : `如 2.0`
  - `tools/machinery/analysis-lifespan.html` : `如 8760`
  - `tools/machinery/analysis-lifespan.html` : `如 22`
  - `tools/machinery/analysis-lifespan.html` : `如 66`
  - `tools/machinery/analysis-lifespan.html` : `如 500`
- **manufacturing**
  - `tools/manufacturing/capacity-planning.html` : `如 5`
  - `tools/manufacturing/capacity-planning.html` : `如 200`
  - `tools/manufacturing/capacity-planning.html` : `如 20000`
  - `tools/manufacturing/capacity-planning.html` : `如 22（1–31）`
  - `tools/manufacturing/defect-rate.html` : `如 10000`
  - `tools/manufacturing/defect-rate.html` : `如 50`
  - `tools/manufacturing/defect-rate.html` : `如 5`
  - `tools/manufacturing/inventory-calculator.html` : `如 12000`
- **maritime**
  - `tools/maritime/anchorage-capacity.html` : `如 200`
  - `tools/maritime/anchorage-capacity.html` : `如 20`
  - `tools/maritime/anchorage-capacity.html` : `如 5`
  - `tools/maritime/anchorage-capacity.html` : `如 50`
  - `tools/maritime/anchorage-capacity.html` : `如 5`
  - `tools/maritime/compass-correction.html` : `如 -5`
  - `tools/maritime/compass-correction.html` : `如 3`
  - `tools/maritime/compass-correction.html` : `如 045（0–360）`
- **marketing**
  - `tools/marketing/ad-roi.html` : `如 10000`
  - `tools/marketing/ad-roi.html` : `如 2`
  - `tools/marketing/ad-roi.html` : `如 30`
  - `tools/marketing/ad-roi.html` : `如 3`
  - `tools/marketing/ad-roi.html` : `如 5`
  - `tools/marketing/ad-roi.html` : `如 200`
  - `tools/marketing/ad-roi.html` : `如 50（0–100）`
  - `tools/marketing/ad-roi.html` : `如 0`
- **martial**
  - `tools/martial/breathing-rhythm.html` : `如 12（4–40）`
  - `tools/martial/kick-height.html` : `如 170（120–220）`
  - `tools/martial/kick-height.html` : `如 0（0–120）`
  - `tools/martial/kick-height.html` : `如 150（0–250）`
  - `tools/martial/routine-timer.html` : `如 80（10–600）`
  - `tools/martial/routine-timer.html` : `如 2（0–30）`
  - `tools/martial/routine-timer.html` : `或点「开始」计时`
  - `tools/martial/stance-center.html` : `如 80（20–200）`
- **materials**
  - `tools/materials/analysis-cost-profit-2.html` : `如 100`
  - `tools/materials/analysis-cost-profit-2.html` : `如 300`
  - `tools/materials/analysis-cost-profit-2.html` : `如 60`
  - `tools/materials/analysis-cost-profit-2.html` : `如 10000`
  - `tools/materials/analysis-cost-profit-2.html` : `如 20`
  - `tools/materials/brinell-hardness.html` : `如 3000`
  - `tools/materials/brinell-hardness.html` : `如 10`
  - `tools/materials/brinell-hardness.html` : `如 4.2`
- **math**
  - `tools/math/arithmetic-series-sum.html` : `如 10`
  - `tools/math/arithmetic-series-sum.html` : `如 1`
  - `tools/math/arithmetic-series-sum.html` : `如 10`
  - `tools/math/calc-1.html` : `如 200`
  - `tools/math/calc-1.html` : `如 15`
  - `tools/math/calc-1.html` : `如 30`
  - `tools/math/calc-1.html` : `如 200`
  - `tools/math/calc-1.html` : `如 45`
- **mechanical**
  - `tools/mechanical/beam-point-load.html` : `如 4`
  - `tools/mechanical/beam-point-load.html` : `如 10`
  - `tools/mechanical/beam-point-load.html` : `如 30`
  - `tools/mechanical/beam-point-load.html` : `如 5000`
  - `tools/mechanical/beam-point-load.html` : `如 150`
  - `tools/mechanical/beam-point-load.html` : `如 300`
  - `tools/mechanical/bearing-life.html` : `如 50`
  - `tools/mechanical/bearing-life.html` : `如 8`
- **media**
  - `tools/media/analysis-26.html` : `这家店服务很好，物流也快，很满意 收到货有划痕，体验失望想退货 性价比不错，推荐购买`
  - `tools/media/analysis-funnel.html` : `例如: 1000,600,300,150,80`
  - `tools/media/assessor-25.html` : `如 10000`
  - `tools/media/assessor-25.html` : `如 2500`
  - `tools/media/assessor-25.html` : `如 1200`
  - `tools/media/assessor-25.html` : `如 350`
  - `tools/media/assessor-25.html` : `如 45`
  - `tools/media/assessor-25.html` : `如 1500`
- **medical**
  - `tools/medical/assessor-risk-3.html` : `如 6.0（4.5–8.0）`
  - `tools/medical/assessor-risk-3.html` : `如 1500`
  - `tools/medical/assessor-risk-3.html` : `如 1.2`
  - `tools/medical/assessor-risk-3.html` : `如 3000`
  - `tools/medical/assessor-risk-3.html` : `如 150`
  - `tools/medical/calc-34.html` : `如 65`
  - `tools/medical/calc-34.html` : `如 170`
  - `tools/medical/calc-34.html` : `如 30`
- **medical2**
  - `tools/medical2/bed-occupancy.html` : `如 500`
  - `tools/medical2/bed-occupancy.html` : `如 480`
  - `tools/medical2/bed-occupancy.html` : `如 30`
  - `tools/medical2/bed-occupancy.html` : `如 13000`
  - `tools/medical2/bed-occupancy.html` : `如 900`
  - `tools/medical2/drug-expiry.html` : `如 180`
  - `tools/medical2/drug-expiry.html` : `如 30`
  - `tools/medical2/drug-expiry.html` : `如：阿莫西林胶囊`
- **metallurgy**
  - `tools/metallurgy/alloy-ratio.html` : `如 5`
  - `tools/metallurgy/alloy-ratio.html` : `如 0（0–100）`
  - `tools/metallurgy/analysis-34.html` : `例如: 0.48,0.51,0.49,0.50,0.52`
  - `tools/metallurgy/analysis-34.html` : `如 0.50`
  - `tools/metallurgy/analysis-34.html` : `如 0.50`
  - `tools/metallurgy/analysis-34.html` : `如 0.20`
  - `tools/metallurgy/analysis-34.html` : `如 0.69`
  - `tools/metallurgy/analysis-34.html` : `如 5`
- **metalwork**
  - `tools/metalwork/analysis-35.html` : `如 6`
  - `tools/metalwork/analysis-35.html` : `飞边,8,2`
  - `tools/metalwork/analysis-36.html` : `如 200`
  - `tools/metalwork/analysis-36.html` : `气孔,45,2`
  - `tools/metalwork/analysis-39.html` : `如 100`
  - `tools/metalwork/analysis-39.html` : `如 20`
  - `tools/metalwork/analysis-simulator.html` : `如 200`
  - `tools/metalwork/analysis-simulator.html` : `如 100`
- **meteorology**
  - `tools/meteorology/absolute-humidity.html` : `如 25`
  - `tools/meteorology/absolute-humidity.html` : `如 60（0–100）`
  - `tools/meteorology/air-aqi.html` : `如 75`
  - `tools/meteorology/air-aqi.html` : `如 120`
  - `tools/meteorology/air-aqi.html` : `如 20`
  - `tools/meteorology/air-aqi.html` : `如 30`
  - `tools/meteorology/air-aqi.html` : `如 1.2`
  - `tools/meteorology/air-aqi.html` : `如 100`
- **metrology**
  - `tools/metrology/bias-absolute.html` : `如 10.2`
  - `tools/metrology/bias-absolute.html` : `如 10`
  - `tools/metrology/bias-percent.html` : `如 10.2`
  - `tools/metrology/bias-percent.html` : `如 10`
  - `tools/metrology/calibration-uncertainty.html` : `如 0.03`
  - `tools/metrology/calibration-uncertainty.html` : `如 0.02`
  - `tools/metrology/detector-139.html` : `如 3`
  - `tools/metrology/detector-139.html` : `如 12`
- **mining**
  - `tools/mining/analysis-cost-3.html` : `如 5000`
  - `tools/mining/analysis-cost-3.html` : `如 2000000`
  - `tools/mining/analysis-cost-3.html` : `如 1.8`
  - `tools/mining/analysis-cost-3.html` : `如 10000`
  - `tools/mining/analysis-cost-3.html` : `如 55000`
  - `tools/mining/calc-1.html` : `如 0.45`
  - `tools/mining/calc-1.html` : `如 0.4`
  - `tools/mining/calc-1.html` : `如 3.0`
- **museum**
  - `tools/museum/audio-guide-timer.html` : `如 30`
  - `tools/museum/audio-guide-timer.html` : `如 90`
  - `tools/museum/audio-guide-timer.html` : `如 30`
  - `tools/museum/audio-guide-timer.html` : `如 60`
  - `tools/museum/audio-guide-timer.html` : `如 90`
  - `tools/museum/audio-guide-timer.html` : `如 90`
  - `tools/museum/exhibit-spacing.html` : `如 80`
  - `tools/museum/exhibit-spacing.html` : `如 100`
- **music**
  - `tools/music/audio-converter.html` : `采样率Hz`
  - `tools/music/audio-converter.html` : `位深`
  - `tools/music/audio-converter.html` : `声道`
  - `tools/music/audio-converter.html` : `时长秒`
  - `tools/music/beat-subdivision.html` : `如 120（1–999）`
  - `tools/music/beat-subdivision.html` : `如 100（1–999）`
  - `tools/music/beat-subdivision.html` : `如 140（1–999）`
  - `tools/music/bpm-converter.html` : `如 120（40–300）`
- **nephrology**
  - `tools/nephrology/aki-kdigo.html` : `如 80`
  - `tools/nephrology/aki-kdigo.html` : `如 180`
  - `tools/nephrology/aki-kdigo.html` : `如 0.3`
  - `tools/nephrology/aki-kdigo.html` : `如 8`
  - `tools/nephrology/aki-kdigo.html` : `如 24`
  - `tools/nephrology/ca-p-product.html` : `如 2.2`
  - `tools/nephrology/ca-p-product.html` : `如 1.8`
  - `tools/nephrology/ca-p-product.html` : `如 35`
- **neurology**
  - `tools/neurology/midas.html` : `如 0`
  - `tools/neurology/midas.html` : `如 0`
  - `tools/neurology/midas.html` : `如 0`
  - `tools/neurology/midas.html` : `如 0`
  - `tools/neurology/midas.html` : `如 0`
  - `tools/neurology/midas.html` : `如 0`
  - `tools/neurology/midas.html` : `如 0（0–10）`
  - `tools/neurology/psqi.html` : `如 7（0–24）`
- **nuclear**
  - `tools/nuclear/absorbed-dose.html` : `如 0.05`
  - `tools/nuclear/absorbed-dose.html` : `如 1`
  - `tools/nuclear/activity-decay.html` : `如 100`
  - `tools/nuclear/activity-decay.html` : `如 0.001`
  - `tools/nuclear/activity-decay.html` : `如 1000`
  - `tools/nuclear/activity-from-halflife.html` : `如 1.808e11`
  - `tools/nuclear/activity-from-halflife.html` : `如 1e20`
  - `tools/nuclear/activity.html` : `如 1e-9`
- **nutrition**
  - `tools/nutrition/assessor-17.html` : `如 60`
  - `tools/nutrition/assessor-17.html` : `如 500`
  - `tools/nutrition/assessor-17.html` : `如 200`
  - `tools/nutrition/calc-1.html` : `如 30（1–120）`
  - `tools/nutrition/calc-1.html` : `如 65（1–300）`
  - `tools/nutrition/calc-1.html` : `如 170（50–250）`
  - `tools/nutrition/calc-2.html` : `如 100`
  - `tools/nutrition/calc-2.html` : `如 0`
- **obstetrics**
  - `tools/obstetrics/afi-normal.html` : `如 4.5`
  - `tools/obstetrics/afi-normal.html` : `如 5.0`
  - `tools/obstetrics/afi-normal.html` : `如 3.8`
  - `tools/obstetrics/afi-normal.html` : `如 4.2`
  - `tools/obstetrics/afi-normal.html` : `如 4.0`
  - `tools/obstetrics/biyun-pearlzhishu-shibailv.html` : `如 100`
  - `tools/obstetrics/biyun-pearlzhishu-shibailv.html` : `如 1200`
  - `tools/obstetrics/biyun-pearlzhishu-shibailv.html` : `如 6`
- **ophthalmology**
  - `tools/ophthalmology/amblyopia-stereopsis.html` : `如 80`
  - `tools/ophthalmology/amblyopia-stereopsis.html` : `如 0.5 或 20/40`
  - `tools/ophthalmology/amblyopia-stereopsis.html` : `如 0.3 或 20/60`
  - `tools/ophthalmology/amblyopia-stereopsis.html` : `如 5`
  - `tools/ophthalmology/amsler-grid-test.html` : `如：上方线条变弯`
  - `tools/ophthalmology/astigmatism-chart.html` : `如：3点–4点方向最糊`
  - `tools/ophthalmology/axial-length.html` : `如 23.50`
  - `tools/ophthalmology/axial-length.html` : `如 1532`
- **optical**
  - `tools/optical/aca-ratio.html` : `如 -6`
  - `tools/optical/aca-ratio.html` : `如 -2`
  - `tools/optical/aca-ratio.html` : `如 -2.00`
  - `tools/optical/aca-ratio.html` : `如 62`
  - `tools/optical/aca-ratio.html` : `如 -2`
  - `tools/optical/aca-ratio.html` : `如 -6`
  - `tools/optical/aca-ratio.html` : `如 40`
  - `tools/optical/accommodation-amplitude.html` : `如 30`
- **optics**
  - `tools/optics/angular-magnification.html` : `如 250`
  - `tools/optics/angular-magnification.html` : `如 25`
  - `tools/optics/brewster-angle.html` : `如 1.0`
  - `tools/optics/brewster-angle.html` : `如 1.5`
  - `tools/optics/combined-lens-focal.html` : `如 0.1`
  - `tools/optics/combined-lens-focal.html` : `如 0.2`
  - `tools/optics/doppler-optical.html` : `如 5e14`
  - `tools/optics/doppler-optical.html` : `如 300000`
- **packaging**
  - `tools/packaging/calc-2.html` : `用于计算动载荷`
  - `tools/packaging/calc-2.html` : `用于计算动载荷`
  - `tools/packaging/calc-66.html` : `如 400`
  - `tools/packaging/calc-66.html` : `如 300`
  - `tools/packaging/calc-66.html` : `如 250`
  - `tools/packaging/calc-66.html` : `如 2.5`
  - `tools/packaging/calc-66.html` : `如 3`
  - `tools/packaging/calc-66.html` : `如 12`
- **paper**
  - `tools/paper/basis-weight.html` : `如 80`
  - `tools/paper/basis-weight.html` : `如 70`
  - `tools/paper/calc-concentration-1.html` : `如 500`
  - `tools/paper/calc-concentration-1.html` : `如 20`
  - `tools/paper/calc-concentration-1.html` : `如 480`
  - `tools/paper/calc-concentration-1.html` : `如 3`
  - `tools/paper/carbon-5.html` : `如 800`
  - `tools/paper/carbon-5.html` : `如 15`
- **parenting**
  - `tools/parenting/diaper-usage.html` : `如 6`
  - `tools/parenting/diaper-usage.html` : `如 1.2`
  - `tools/parenting/diaper-usage.html` : `如 30`
  - `tools/parenting/feeding-amount-baby.html` : `如 4`
  - `tools/parenting/feeding-amount-baby.html` : `如 6.8`
  - `tools/parenting/feeding-amount-baby.html` : `如 6`
  - `tools/parenting/feeding-schedule.html` : `如 3（0–36）`
  - `tools/parenting/feeding-schedule.html` : `如 6（2–20）`
- **pediatrics**
  - `tools/pediatrics/assessor-13.html` : `如 24`
  - `tools/pediatrics/assessor-13.html` : `如 12`
  - `tools/pediatrics/assessor-13.html` : `如已知病前体重`
  - `tools/pediatrics/assessor-13.html` : `如 2`
  - `tools/pediatrics/assessor-spo2.html` : `如 2`
  - `tools/pediatrics/assessor-spo2.html` : `如 98（0–100）`
  - `tools/pediatrics/assessor-spo2.html` : `如 97（0–100）`
  - `tools/pediatrics/chd-assessment.html` : `如 2`
- **pet-training**
  - `tools/pet-training/clicker-timing.html` : `如 800（200–3000）`
  - `tools/pet-training/command-repetition.html` : `如 5`
  - `tools/pet-training/command-repetition.html` : `如 24`
  - `tools/pet-training/command-repetition.html` : `如 6`
  - `tools/pet-training/elimination-predict.html` : `如 3`
  - `tools/pet-training/elimination-predict.html` : `如 15`
  - `tools/pet-training/leash-length.html` : `如 1.5（0.3–10）`
  - `tools/pet-training/leash-length.html` : `如 15`
- **pet**
  - `tools/pet/analysis-cost-profit-1.html` : `如 320`
  - `tools/pet/analysis-cost-profit-1.html` : `如 280`
  - `tools/pet/analysis-cost-profit-1.html` : `如 110`
  - `tools/pet/analysis-cost-profit-1.html` : `如 12000`
  - `tools/pet/analysis-cost-profit-1.html` : `如 22000`
  - `tools/pet/analysis-cost-profit-1.html` : `如 3000`
  - `tools/pet/analysis-cost-profit-1.html` : `如 8000`
  - `tools/pet/aquarium-light.html` : `输入水草名称`
- **petrochem**
  - `tools/petrochem/api-gravity.html` : `如 35`
  - `tools/petrochem/api-gravity.html` : `如 0.85`
  - `tools/petrochem/catalyst-calc.html` : `如 5000`
  - `tools/petrochem/catalyst-calc.html` : `如 2`
  - `tools/petrochem/catalyst-calc.html` : `如 850`
  - `tools/petrochem/catalyst-calc.html` : `如 700`
  - `tools/petrochem/catalyst-calc.html` : `如 5000`
  - `tools/petrochem/catalyst-calc.html` : `如 30`
- **photo**
  - `tools/photo/bracketing-plan.html` : `如 3`
  - `tools/photo/bracketing-plan.html` : `如 1`
  - `tools/photo/bracketing-plan.html` : `如 0`
  - `tools/photo/calc-exposure-aperture.html` : `如 2.8、4、8`
  - `tools/photo/calc-exposure-aperture.html` : `如 1/125、0.008、2`
  - `tools/photo/calc-exposure-aperture.html` : `如 100`
  - `tools/photo/calc-exposure-aperture.html` : `如 15`
  - `tools/photo/calc-exposure-aperture.html` : `留空=求光圈`
- **plastic**
  - `tools/plastic/blow-molding.html` : `如 80`
  - `tools/plastic/blow-molding.html` : `如 25`
  - `tools/plastic/blow-molding.html` : `如 4`
  - `tools/plastic/blow-molding.html` : `如 3.2`
  - `tools/plastic/blow-molding.html` : `如 25`
  - `tools/plastic/blow-molding.html` : `如 1.2`
  - `tools/plastic/blow-molding.html` : `如 80`
  - `tools/plastic/extrusion-rate.html` : `如 65`
- **pr**
  - `tools/pr/analysis-6.html` : `粘贴需要判断情感倾向的文本`
  - `tools/pr/analysis-assessor.html` : `冠名权益,800000,300000`
  - `tools/pr/analysis-density-1.html` : `粘贴新闻稿正文`
  - `tools/pr/assessor-58.html` : `如 10（0–10000）`
  - `tools/pr/assessor-58.html` : `如 5（0–1000）`
  - `tools/pr/assessor-58.html` : `如 100（0–100000）`
  - `tools/pr/assessor-59.html` : `如 50（0–100000）`
  - `tools/pr/assessor-59.html` : `如 10（0–10000）`
- **printing**
  - `tools/printing/box-area.html` : `如 200`
  - `tools/printing/box-area.html` : `如 150`
  - `tools/printing/box-area.html` : `如 80`
  - `tools/printing/box-area.html` : `如 15`
  - `tools/printing/box-area.html` : `如 3`
  - `tools/printing/carton-design.html` : `如 120`
  - `tools/printing/carton-design.html` : `如 80`
  - `tools/printing/carton-design.html` : `如 60`
- **process**
  - `tools/process/cp-index.html` : `如 10.05`
  - `tools/process/cp-index.html` : `如 9.95`
  - `tools/process/cp-index.html` : `如 0.01`
  - `tools/process/cpk-index.html` : `如 10.05`
  - `tools/process/cpk-index.html` : `如 9.95`
  - `tools/process/cpk-index.html` : `如 10.0`
  - `tools/process/cpk-index.html` : `如 0.01`
  - `tools/process/cpk-with-shift.html` : `如 10.05`
- **procurement**
  - `tools/procurement/analysis-cost.html` : `如 500`
  - `tools/procurement/analysis-cost.html` : `如 100`
  - `tools/procurement/analysis-cost.html` : `如 85`
  - `tools/procurement/analysis-cost.html` : `如 6`
  - `tools/procurement/analysis-cost.html` : `如 10000`
  - `tools/procurement/assessor-26.html` : `如 500`
  - `tools/procurement/assessor-26.html` : `如 5`
  - `tools/procurement/assessor-26.html` : `如 2000`
- **property**
  - `tools/property/analysis-40.html` : `例如: 毛利率,20,28,high 费用率,15,10,low`
  - `tools/property/assessor-manager-1.html` : `如：XX物业服务有限公司`
  - `tools/property/assessor-manager-1.html` : `如 50`
  - `tools/property/assessor-manager-1.html` : `如 12`
  - `tools/property/calc-shared-property-fee.html` : `如 100`
  - `tools/property/calc-shared-property-fee.html` : `如 20（0–100）`
  - `tools/property/calc-shared-property-fee.html` : `如 2.5`
  - `tools/property/calc-shared-property-fee.html` : `如 0.5`
- **pulmonology**
  - `tools/pulmonology/anti-tb-dosing.html` : `如 55`
  - `tools/pulmonology/anti-tb-dosing.html` : `如 45`
  - `tools/pulmonology/calc-48.html` : `如 80`
  - `tools/pulmonology/calc-48.html` : `如 40（21–100）`
  - `tools/pulmonology/calc-48.html` : `用于计算 OI 氧合指数`
  - `tools/pulmonology/calc-48.html` : `用于评估通气`
  - `tools/pulmonology/feigongneng-fev1-fvc-fenji.html` : `如 2.1`
  - `tools/pulmonology/feigongneng-fev1-fvc-fenji.html` : `如 3.5`
- **quality**
  - `tools/quality/calc-cpk.html` : `如 10.5`
  - `tools/quality/calc-cpk.html` : `如 9.5`
  - `tools/quality/calc-cpk.html` : `如 10.0`
  - `tools/quality/calc-cpk.html` : `如 0.1`
  - `tools/quality/calc-cpk.html` : `如 10.5`
  - `tools/quality/calc-cpk.html` : `如 9.5`
  - `tools/quality/control-chart.html` : `如 5`
  - `tools/quality/control-chart.html` : `如 0.2`
- **quantum**
  - `tools/quantum/angular-momentum-quant.html` : `如 3`
  - `tools/quantum/band-gap-photon.html` : `如 1.12`
  - `tools/quantum/bohr-orbit-radius.html` : `如 1`
  - `tools/quantum/boltzmann-population.html` : `如 1`
  - `tools/quantum/boltzmann-population.html` : `如 300`
  - `tools/quantum/compton-shift.html` : `如 90`
  - `tools/quantum/compton-wavelength.html` : `如 9.109e-31`
  - `tools/quantum/cyclotron-frequency.html` : `如 1.602e-19`
- **realestate**
  - `tools/realestate/analysis-24.html` : `如 500`
  - `tools/realestate/analysis-24.html` : `如 3`
  - `tools/realestate/analysis-24.html` : `如 5`
  - `tools/realestate/analysis-41.html` : `如 900`
  - `tools/realestate/analysis-41.html` : `如 700`
  - `tools/realestate/analysis-41.html` : `如 6000`
  - `tools/realestate/analysis-41.html` : `如 19000`
  - `tools/realestate/analysis-41.html` : `如 20500`
- **rehabilitation**
  - `tools/rehabilitation/assistive-device-fitting.html` : `如 170`
  - `tools/rehabilitation/assistive-device-fitting.html` : `如 65`
  - `tools/rehabilitation/assistive-device-fitting.html` : `如 85`
  - `tools/rehabilitation/assistive-device-fitting.html` : `如 40`
  - `tools/rehabilitation/assistive-device-fitting.html` : `如 45`
  - `tools/rehabilitation/assistive-device-fitting.html` : `如 35`
  - `tools/rehabilitation/assistive-device-fitting.html` : `如 50`
  - `tools/rehabilitation/assistive-device-fitting.html` : `如 65`
- **rental**
  - `tools/rental/assessor-24.html` : `如 12000`
  - `tools/rental/assessor-24.html` : `如 4000`
  - `tools/rental/assessor-24.html` : `如 5`
  - `tools/rental/assessor-24.html` : `如 700`
  - `tools/rental/assessor-24.html` : `如 28`
  - `tools/rental/calc-commission-1.html` : `如 200`
  - `tools/rental/calc-commission-1.html` : `如 2`
  - `tools/rental/calc-commission-1.html` : `如 0`
- **reproductive-medicine**
  - `tools/reproductive-medicine/anti-sperm-antibody.html` : `如 10`
  - `tools/reproductive-medicine/baifenbijisuanqi.html` : `如 100`
  - `tools/reproductive-medicine/baifenbijisuanqi.html` : `如 20`
  - `tools/reproductive-medicine/calc-volume-concentration.html` : `如 40（0–1000）`
  - `tools/reproductive-medicine/calc-volume-concentration.html` : `如 3.0（0.1–20）`
  - `tools/reproductive-medicine/detector-9.html` : `如 0.5`
  - `tools/reproductive-medicine/detector-9.html` : `如 0`
  - `tools/reproductive-medicine/detector-9.html` : `如 20`
- **research**
  - `tools/research/analysis-50.html` : `A公司,520`
  - `tools/research/analysis-52.html` : `例如: 价格敏感,12,4`
  - `tools/research/analysis-54.html` : `例如: 访谈1,价格敏感,服务不足`
  - `tools/research/assessor-50.html` : `如 50000`
  - `tools/research/assessor-50.html` : `如 100000`
  - `tools/research/assessor-50.html` : `如 3.5`
  - `tools/research/assessor-50.html` : `如 2.5`
  - `tools/research/assessor-50.html` : `如 45`
- **restaurant**
  - `tools/restaurant/bbq-portion.html` : `如 6`
  - `tools/restaurant/delivery-time.html` : `如 3.5`
  - `tools/restaurant/delivery-time.html` : `如 20`
  - `tools/restaurant/delivery-time.html` : `如 15`
  - `tools/restaurant/delivery-time.html` : `如 5`
  - `tools/restaurant/delivery-time.html` : `如 3`
  - `tools/restaurant/dish-cost-card.html` : `如 1`
  - `tools/restaurant/dish-cost-card.html` : `如 38`
- **rheumatology**
  - `tools/rheumatology/anti-ccp.html` : `如 120`
  - `tools/rheumatology/anti-ccp.html` : `如 45`
  - `tools/rheumatology/anti-ccp.html` : `如 12`
  - `tools/rheumatology/anti-ccp.html` : `如 28`
  - `tools/rheumatology/complement-level.html` : `如 0.5`
  - `tools/rheumatology/complement-level.html` : `如 0.08`
  - `tools/rheumatology/complement-level.html` : `如 15`
  - `tools/rheumatology/das28.html` : `如 20`
- **road**
  - `tools/road/convert-angle-slope.html` : `如 10`
  - `tools/road/curve-calc.html` : `如 6（0–10）`
  - `tools/road/curve-calc.html` : `如 0.15（0.05–0.2）`
  - `tools/road/curve-calc.html` : `如 60（1–180）`
  - `tools/road/curve-calc.html` : `如 7.5`
  - `tools/road/curve-calc.html` : `如 125（50–330）`
  - `tools/road/grade-calc.html` : `如 100`
  - `tools/road/grade-calc.html` : `如 108`
- **robotics**
  - `tools/robotics/accel-distance.html` : `如 2`
  - `tools/robotics/accel-distance.html` : `如 1`
  - `tools/robotics/battery-runtime.html` : `如 2`
  - `tools/robotics/battery-runtime.html` : `如 12`
  - `tools/robotics/battery-runtime.html` : `如 24`
  - `tools/robotics/belt-linear-speed.html` : `如 0.06`
  - `tools/robotics/belt-linear-speed.html` : `如 300`
  - `tools/robotics/cable-tension-pulley.html` : `如 100`
- **rubber**
  - `tools/rubber/abrasion-test.html` : `如 0.15`
  - `tools/rubber/cure-time.html` : `如 150`
  - `tools/rubber/cure-time.html` : `如 20`
  - `tools/rubber/cure-time.html` : `如 90`
  - `tools/rubber/cure-time.html` : `如 160`
  - `tools/rubber/hardness-calc.html` : `如 50（0–100）`
  - `tools/rubber/hardness-calc.html` : `如 50（0–100）`
  - `tools/rubber/mixing-ratio.html` : `如 100`
- **safety**
  - `tools/safety/accident-stats.html` : `如 500000`
  - `tools/safety/accident-stats.html` : `如 0`
  - `tools/safety/accident-stats.html` : `如 1`
  - `tools/safety/accident-stats.html` : `如 4`
  - `tools/safety/accident-stats.html` : `如 3`
  - `tools/safety/accident-stats.html` : `如 45`
  - `tools/safety/analysis-3.html` : `例如: 192.168.1.10 login_fail 203.0.113.7 ssh_fail`
  - `tools/safety/analysis-3.html` : `如 3`
- **sales**
  - `tools/sales/commission-calc.html` : `如 250000`
  - `tools/sales/commission-calc.html` : `如 0`
  - `tools/sales/commission-calc.html` : `如 5000`
  - `tools/sales/commission-calculator.html` : `如 100000`
  - `tools/sales/commission-calculator.html` : `如 5（0–100）`
  - `tools/sales/commission-calculator.html` : `如 5000`
  - `tools/sales/commission-calculator.html` : `如 20000`
  - `tools/sales/commission-calculator.html` : `如 8（0–100）`
- **science**
  - `tools/science/astro-geo-calculator.html` : `如 39.9042（-90–90）`
  - `tools/science/astro-geo-calculator.html` : `如 116.4074（-180–180）`
  - `tools/science/astro-geo-calculator.html` : `如 5.0（0–10）`
  - `tools/science/astro-geo-calculator.html` : `如 1.7`
  - `tools/science/astro-geo-calculator.html` : `如 5`
  - `tools/science/astro-geo-calculator.html` : `如 25`
  - `tools/science/astro-geo-calculator.html` : `如 20`
  - `tools/science/astro-geo-calculator.html` : `如 0`
- **securities**
  - `tools/securities/annualized-vol.html` : `如 0.01`
  - `tools/securities/annualized-volatility.html` : `如 0.015`
  - `tools/securities/annualized-volatility.html` : `如 252`
  - `tools/securities/beta-calc.html` : `如：2.5,-1.2,3.1,0.8,...`
  - `tools/securities/beta-calc.html` : `如：1.5,-0.8,2.1,0.5,3.0,-1.5,0.8,1.9,-0.3,2.5,0.6,-1.0,2.0,0.2,2.6`
  - `tools/securities/beta-calc.html` : `如 3`
  - `tools/securities/beta-calc.html` : `如 10`
  - `tools/securities/beta-covariance.html` : `如 0.002`
- **security**
  - `tools/security/anti-fraud-cards.html` : `输入关键词搜索...`
  - `tools/security/data-erase-simulator.html` : `如 16（4–64）`
  - `tools/security/detector-45.html` : `如 15`
  - `tools/security/detector-45.html` : `如 1.2`
  - `tools/security/detector-45.html` : `如 5`
  - `tools/security/detector-45.html` : `如 8（1–10）`
  - `tools/security/emergency-contacts.html` : `如：妈妈、社区医生、物业`
  - `tools/security/emergency-contacts.html` : `输入电话号码`
- **seismology**
  - `tools/seismology/analysis-stress.html` : `节面A,30,60,-90`
  - `tools/seismology/assessor-30.html` : `如 200`
  - `tools/seismology/assessor-30.html` : `如 20`
  - `tools/seismology/assessor-30.html` : `如 0.3（0–1）`
  - `tools/seismology/assessor-31.html` : `如 100`
  - `tools/seismology/assessor-31.html` : `如 30`
  - `tools/seismology/assessor-31.html` : `如 15`
  - `tools/seismology/assessor-31.html` : `如 8`
- **shipping**
  - `tools/shipping/calc-76.html` : `如 180`
  - `tools/shipping/calc-76.html` : `如 28`
  - `tools/shipping/calc-76.html` : `如 9.5`
  - `tools/shipping/calc-76.html` : `如 9.7`
  - `tools/shipping/calc-76.html` : `如 9.9`
  - `tools/shipping/calc-76.html` : `如 0.72（0–1）`
  - `tools/shipping/calc-76.html` : `如 1.025`
  - `tools/shipping/calc-76.html` : `自动`
- **signal**
  - `tools/signal/bandwidth-q.html` : `如 1000`
  - `tools/signal/bandwidth-q.html` : `如 10`
  - `tools/signal/bit-rate-nyquist.html` : `如 3000`
  - `tools/signal/bit-rate-nyquist.html` : `如 4`
  - `tools/signal/carrier-freq.html` : `如 1010`
  - `tools/signal/carrier-freq.html` : `如 990`
  - `tools/signal/cascade-gain-db.html` : `如 10`
  - `tools/signal/cascade-gain-db.html` : `如 -3`
- **sports**
  - `tools/sports/altitude-acclimatization.html` : `如 0（0–8000）`
  - `tools/sports/altitude-acclimatization.html` : `如 5000（0–8848）`
  - `tools/sports/analysis-19.html` : `1,进攻,成功`
  - `tools/sports/analysis-20.html` : `例如: 10,9,10,9,8`
  - `tools/sports/analysis-spacing.html` : `如 2.0`
  - `tools/sports/analysis-spacing.html` : `如 60（0–170）`
  - `tools/sports/analysis-spacing.html` : `如 12`
  - `tools/sports/analysis-spacing.html` : `如 25`
- **stage**
  - `tools/stage/beam-angle.html` : `如 25（0–360）`
  - `tools/stage/beam-angle.html` : `如 10`
  - `tools/stage/beam-angle.html` : `如 50000`
  - `tools/stage/dimmer-curve.html` : `如 128（0–255）`
  - `tools/stage/light-position.html` : `如 6`
  - `tools/stage/light-position.html` : `如 5`
  - `tools/stage/light-position.html` : `如 45（0–90）`
  - `tools/stage/light-position.html` : `如 6`
- **startup**
  - `tools/startup/burn-rate.html` : `如 3000000`
  - `tools/startup/burn-rate.html` : `如 50000`
  - `tools/startup/burn-rate.html` : `如 200000`
  - `tools/startup/burn-rate.html` : `如 30000`
  - `tools/startup/burn-rate.html` : `如 50000`
  - `tools/startup/burn-rate.html` : `如 20000`
  - `tools/startup/calc-1.html` : `如 3000`
  - `tools/startup/calc-1.html` : `如 20000`
- **statistics**
  - `tools/statistics/binomial-cdf.html` : `如 5`
  - `tools/statistics/binomial-cdf.html` : `如 0.5`
  - `tools/statistics/binomial-cdf.html` : `如 2`
  - `tools/statistics/binomial-pmf.html` : `如 10`
  - `tools/statistics/binomial-pmf.html` : `如 3`
  - `tools/statistics/binomial-pmf.html` : `如 0.5`
  - `tools/statistics/coefficient-of-variation.html` : `如 5`
  - `tools/statistics/coefficient-of-variation.html` : `如 2`
- **structural**
  - `tools/structural/allowable-stress.html` : `如 250`
  - `tools/structural/allowable-stress.html` : `如 1.5`
  - `tools/structural/angle-of-twist.html` : `如 500`
  - `tools/structural/angle-of-twist.html` : `如 1`
  - `tools/structural/angle-of-twist.html` : `如 80e9`
  - `tools/structural/angle-of-twist.html` : `如 0.05`
  - `tools/structural/axial-strain.html` : `如 0.002`
  - `tools/structural/axial-strain.html` : `如 2`
- **surveying**
  - `tools/surveying/analysis-17.html` : `如 30`
  - `tools/surveying/analysis-17.html` : `如 100`
  - `tools/surveying/analysis-cycle.html` : `如：第1期,2.1`
  - `tools/surveying/analysis-cycle.html` : `如 10`
  - `tools/surveying/analysis-cycle.html` : `如 2`
  - `tools/surveying/area-24.html` : `如 120`
  - `tools/surveying/area-24.html` : `如 80`
  - `tools/surveying/area-25.html` : `如 100`
- **tax**
  - `tools/tax/ad-valorem-duty.html` : `如 1000`
  - `tools/tax/ad-valorem-duty.html` : `如 0.1`
  - `tools/tax/average-tax-rate.html` : `如 30000`
  - `tools/tax/average-tax-rate.html` : `如 100000`
  - `tools/tax/break-even-taxable.html` : `如 750000`
  - `tools/tax/break-even-taxable.html` : `如 0`
  - `tools/tax/break-even-taxable.html` : `如 25`
  - `tools/tax/calc-8.html` : `如 36000`
- **tcm-chemistry**
  - `tools/tcm-chemistry/calc-44.html` : `如 4`
  - `tools/tcm-chemistry/calc-44.html` : `如 100`
  - `tools/tcm-chemistry/calc-44.html` : `如 25`
  - `tools/tcm-chemistry/calc-44.html` : `如 99`
  - `tools/tcm-chemistry/capsule-filling.html` : `如 30`
  - `tools/tcm-chemistry/capsule-filling.html` : `如 80`
  - `tools/tcm-chemistry/capsule-filling.html` : `如 0.5`
  - `tools/tcm-chemistry/capsule-filling.html` : `如 0.7`
- **tcm-diagnosis**
  - `tools/tcm-diagnosis/disease-tracking.html` : `症状名称（如：头痛）`
  - `tools/tcm-diagnosis/formula-matching.html` : `搜索方剂名、证型、症状（如：风寒、气虚、逍遥散）`
  - `tools/tcm-diagnosis/generator-29.html` : `如 5（1–50）`
  - `tools/tcm-diagnosis/meridian-differentiation.html` : `如：头痛、肩、腰、膝、胁…`
  - `tools/tcm-diagnosis/pulse-diagnosis.html` : `输入脉象名称，如浮、沉、迟、数…`
  - `tools/tcm-diagnosis/tcm-medical-record.html` : `患者姓名`
  - `tools/tcm-diagnosis/tcm-medical-record.html` : `岁`
  - `tools/tcm-diagnosis/tcm-medical-record.html` : `职业`
- **tcm-pharmacy**
  - `tools/tcm-pharmacy/calc-time-concentration.html` : `如 100`
  - `tools/tcm-pharmacy/calc-time-concentration.html` : `如 1000`
  - `tools/tcm-pharmacy/calc-time-concentration.html` : `如 50`
  - `tools/tcm-pharmacy/calc-time-concentration.html` : `如 0.1`
  - `tools/tcm-pharmacy/decoction-time.html` : `例如：石膏，先煎，知母，薄荷，后下，甘草，粳米`
  - `tools/tcm-pharmacy/decoction-time.html` : `如 5（1–50）`
  - `tools/tcm-pharmacy/decoction-time.html` : `如 10（1–100）`
  - `tools/tcm-pharmacy/formula-song.html` : `如：麻黄汤、四物汤...`
- **telecom**
  - `tools/telecom/ap-coverage.html` : `如 20`
  - `tools/telecom/ap-coverage.html` : `如 3`
  - `tools/telecom/ap-coverage.html` : `如 2412`
  - `tools/telecom/ap-coverage.html` : `如 -82`
  - `tools/telecom/ap-coverage.html` : `如 2`
  - `tools/telecom/ap-coverage.html` : `如 10`
  - `tools/telecom/ap-coverage.html` : `如 8`
  - `tools/telecom/bandwidth-calculator.html` : `如 100`
- **text**
  - `tools/text/analysis-density.html` : `粘贴文章正文、网页文案等`
  - `tools/text/calc-1.html` : `原始文本...`
  - `tools/text/calc-1.html` : `修改后的文本...`
  - `tools/text/lorem-ipsum-generator.html` : `如 3`
  - `tools/text/reading-time-estimator.html` : `如 300`
  - `tools/text/reading-time-estimator.html` : `如 200`
  - `tools/text/sensitive-word-filter.html` : `粘贴文本`
  - `tools/text/stats-1.html` : `粘贴或输入文本，支持中英文混排与换行…`
- **textile**
  - `tools/textile/calc-gsm.html` : `如 5.2`
  - `tools/textile/calc-gsm.html` : `如 20`
  - `tools/textile/calc-gsm.html` : `如 20`
  - `tools/textile/calc-gsm.html` : `如 150`
  - `tools/textile/calc-gsm.html` : `如 200`
  - `tools/textile/calc-gsm.html` : `如 150`
  - `tools/textile/calc-gsm.html` : `如 40`
  - `tools/textile/calc-gsm.html` : `如 40`
- **thermodynamics**
  - `tools/thermodynamics/adiabatic-tv.html` : `如 300`
  - `tools/thermodynamics/adiabatic-tv.html` : `如 1`
  - `tools/thermodynamics/adiabatic-tv.html` : `如 2`
  - `tools/thermodynamics/adiabatic-tv.html` : `如 1.4`
  - `tools/thermodynamics/biot-number.html` : `如 50`
  - `tools/thermodynamics/biot-number.html` : `如 0.05`
  - `tools/thermodynamics/biot-number.html` : `如 400`
  - `tools/thermodynamics/boyles-law.html` : `如 100`
- **transport**
  - `tools/transport/calc-4.html` : `输入关键词，如 闯红灯、超速、酒驾`
  - `tools/transport/calc-53.html` : `如：120,80,50,40,60,180,450,780,820,700,650,720,760,690,640,720,820,950,1050,880,620,400,260,160`
  - `tools/transport/calc-53.html` : `如 320`
  - `tools/transport/calc-53.html` : `如 380`
  - `tools/transport/calc-53.html` : `如 410`
  - `tools/transport/calc-53.html` : `如 350`
  - `tools/transport/calculator-calc-3.html` : `如 0`
  - `tools/transport/calculator-calc-3.html` : `如 30（0–59）`
- **travel**
  - `tools/travel/currency-cheat-sheet.html` : `如 7.20`
  - `tools/travel/currency-cheat-sheet.html` : `输入货币名称或代码...`
  - `tools/travel/estimate-15.html` : `如 500`
  - `tools/travel/estimate-15.html` : `如 10（0–100）`
  - `tools/travel/estimate-15.html` : `如 3（0–100）`
  - `tools/travel/estimate-15.html` : `如 7.8`
  - `tools/travel/estimate-15.html` : `如 0`
  - `tools/travel/international-tip-calculator.html` : `如 100`
- **tunnel**
  - `tools/tunnel/advance-rate.html` : `如 3`
  - `tools/tunnel/advance-rate.html` : `如 0.9（0.5–1）`
  - `tools/tunnel/advance-rate.html` : `如 3`
  - `tools/tunnel/advance-rate.html` : `如 1`
  - `tools/tunnel/advance-rate.html` : `如 0.5`
  - `tools/tunnel/advance-rate.html` : `如 3`
  - `tools/tunnel/advance-rate.html` : `如 2`
  - `tools/tunnel/advance-rate.html` : `如 3（1–6）`
- **urban**
  - `tools/urban/building-height.html` : `如 30`
  - `tools/urban/building-height.html` : `如 3（2.4–6）`
  - `tools/urban/building-height.html` : `如 50`
  - `tools/urban/building-height.html` : `如 3000`
  - `tools/urban/building-height.html` : `如 0`
  - `tools/urban/building-height.html` : `如 60`
  - `tools/urban/building-height.html` : `如 3（2.4–6）`
  - `tools/urban/building-height.html` : `如 0.6（0–3）`
- **urology**
  - `tools/urology/assessor-pressure.html` : `如 50（0–200）`
  - `tools/urology/assessor-pressure.html` : `如 10（0–50）`
  - `tools/urology/bladder-capacity.html` : `如 280`
  - `tools/urology/bladder-capacity.html` : `如 30`
  - `tools/urology/bladder-capacity.html` : `如 45`
  - `tools/urology/calc-volume.html` : `如 4.5`
  - `tools/urology/calc-volume.html` : `如 3.5`
  - `tools/urology/calc-volume.html` : `如 4.0`
- **usedcar**
  - `tools/usedcar/calc-73.html` : `如 20`
  - `tools/usedcar/calc-73.html` : `如 3`
  - `tools/usedcar/calc-73.html` : `如 5`
  - `tools/usedcar/calc-73.html` : `如 1.5`
  - `tools/usedcar/car-purchase-cost.html` : `如 150000`
  - `tools/usedcar/car-purchase-cost.html` : `如 10`
  - `tools/usedcar/car-purchase-cost.html` : `如 8000`
  - `tools/usedcar/car-purchase-cost.html` : `如 800`
- **video**
  - `tools/video/analysis-69.html` : `如 8000`
  - `tools/video/analysis-69.html` : `如 5（0–100）`
  - `tools/video/analysis-69.html` : `如 40（0–100）`
  - `tools/video/analysis-69.html` : `例如: 5000,7000,6000`
  - `tools/video/subtitle-tool.html` : `粘贴 SRT 字幕内容... 1 00:00:01,000 --> 00:00:04,000 Hello World`
  - `tools/video/subtitle-tool.html` : `如 0`
  - `tools/video/subtitle-tool.html` : `如 1`
  - `tools/video/video-compressor.html` : `如 10`
- **wedding**
  - `tools/wedding/detector-33.html` : `如 8（1–10）`
  - `tools/wedding/detector-33.html` : `如 9（1–10）`
  - `tools/wedding/detector-33.html` : `如 7（1–10）`
  - `tools/wedding/detector-33.html` : `如 8（1–10）`
  - `tools/wedding/detector-33.html` : `如 95`
  - `tools/wedding/seating-chart.html` : `如 10（4–20）`
  - `tools/wedding/seating-chart.html` : `如 8（4–20）`
  - `tools/wedding/seating-chart.html` : `如：张三`
- **welding**
  - `tools/welding/analysis-37.html` : `气孔,45`
  - `tools/welding/analysis-38.html` : `如 180`
  - `tools/welding/analysis-38.html` : `如 24`
  - `tools/welding/analysis-38.html` : `如 4`
  - `tools/welding/analysis-38.html` : `如 20`
  - `tools/welding/analysis-38.html` : `如 0.8（0.1–1）`
  - `tools/welding/calc-1.html` : `如 3.2`
  - `tools/welding/calc-1.html` : `如 8`
- **woodwork**
  - `tools/woodwork/analysis-cost-price.html` : `例如: 3200,3300,3100,3400,3500`
  - `tools/woodwork/analysis-cost-price.html` : `如 3000`
  - `tools/woodwork/analysis-cost-price.html` : `如 15`
  - `tools/woodwork/angle-1.html` : `如 30（0–89）`
  - `tools/woodwork/angle-1.html` : `如 18`
  - `tools/woodwork/angle-1.html` : `如 45（0–90）`
  - `tools/woodwork/calculator-calc-15.html` : `如 18`
  - `tools/woodwork/calculator-calc-15.html` : `如 60`
- **woodworking**
  - `tools/woodworking/angle-cut.html` : `如 90（1–180）`
  - `tools/woodworking/angle-cut.html` : `如 2（2–12）`
  - `tools/woodworking/angle-cut.html` : `如 45（0–89）`
  - `tools/woodworking/angle-cut.html` : `如 0（0–89）`
  - `tools/woodworking/angle-cut.html` : `如 50`
  - `tools/woodworking/angle-cut.html` : `如 20`
  - `tools/woodworking/angle-cut.html` : `如 200`
  - `tools/woodworking/board-feet.html` : `如 1（0.25–12）`
- **admin**
  - `tools/admin/analysis-30.html` : `办公用品,20000,23500`
  - `tools/admin/supplies-forecast.html` : `如 3`
  - `tools/admin/supplies-forecast.html` : `如 1.2`
  - `tools/admin/travel-subsidy.html` : `如 100`
  - `tools/admin/travel-subsidy.html` : `如 80`
  - `tools/admin/version-control.html` : `如 1.2.3`
  - `tools/admin/version-control.html` : `本次修订内容说明...`
- **chinese**
  - `tools/chinese/chinese-character.html` : `输入或粘贴一个汉字`
  - `tools/chinese/chinese-culture.html` : `搜索诗名、作者或内容...`
  - `tools/chinese/chinese-culture.html` : `请输入四字成语...`
  - `tools/chinese/chinese-culture.html` : `输入汉字或词语查询笔画数...`
  - `tools/chinese/chinese-culture.html` : `搜索认知偏差...`
  - `tools/chinese/chinese-culture.html` : `搜索名言...`
  - `tools/chinese/chinese-radical-lookup.html` : `例如：你`
- **service**
  - `tools/service/complaint-analysis.html` : `每行输入一条投诉内容 如：配送太慢，等了三天才到`
  - `tools/service/csat-score.html` : `如 45`
  - `tools/service/csat-score.html` : `如 30`
  - `tools/service/csat-score.html` : `如 12`
  - `tools/service/csat-score.html` : `如 8`
  - `tools/service/csat-score.html` : `如 5`
  - `tools/service/response-time.html` : `如 30`
- **photo2**
  - `tools/photo2/focal-length.html` : `如 50`
  - `tools/photo2/video-storage.html` : `如 20`
  - `tools/photo2/video-storage.html` : `如 1`
  - `tools/photo2/video-storage.html` : `如 0（0–59）`
  - `tools/photo2/video-storage.html` : `如 128`
  - `tools/photo2/white-balance.html` : `如 5500（1000–40000）`
- **stats**
  - `tools/stats/data-distribution.html` : `如 0（0–50）`
  - `tools/stats/regression-analysis.html` : `如 11`
  - `tools/stats/sample-size.html` : `如 5`
  - `tools/stats/sample-size.html` : `如 0.5（0–1）`
  - `tools/stats/sample-size.html` : `如 0`
  - `tools/stats/statistical-tests.html` : `如 20`
- **accessibility**
  - `tools/accessibility/braille-translator.html` : `如 ni hao / hello / 123`
  - `tools/accessibility/ramp-slope.html` : `如 40（1–300）`
  - `tools/accessibility/ramp-slope.html` : `如 12（2–50）`
  - `tools/accessibility/sign-language.html` : `如：你好、谢谢、妈妈`
  - `tools/accessibility/voice-synthesis.html` : `请输入文字…`
- **antiques**
  - `tools/antiques/bronze-identification.html` : `如：鼎、饕餮纹、铭文...`
  - `tools/antiques/calligraphy-style.html` : `如：王羲之、颜真卿、隶书...`
  - `tools/antiques/furniture-style.html` : `如：黄花梨、圈椅、雕刻...`
  - `tools/antiques/porcelain-date.html` : `如：青花、釉里红、款识...`
  - `tools/antiques/seal-identification.html` : `如：玉印、瓦钮、朱文、赵孟頫...`
- **legal2**
  - `tools/legal2/compensation-n1.html` : `如 10000`
  - `tools/legal2/compensation-n1.html` : `如 30000`
  - `tools/legal2/contract-dates.html` : `如 30`
  - `tools/legal2/keyword-extract.html` : `粘贴法律文书内容，如判决书、合同、起诉状等... 示例： 原告张三与被告李四买卖合同纠纷一案，本院于2024年3月15日立案。原告诉称，2023年10月1日双方签订《购销合同》，约定被告向原告购买货物`
  - `tools/legal2/statute-deadline.html` : `如 3`
- **audio**
  - `tools/audio/analysis-1.html` : `如 44100`
  - `tools/audio/analysis-1.html` : `如 4096`
  - `tools/audio/analysis-1.html` : `如 200`
  - `tools/audio/audio-sample-rate.html` : `如 60`
- **chinese-cook**
  - `tools/chinese-cook/estimate-16.html` : `如 100`
  - `tools/chinese-cook/estimate-16.html` : `如 20`
  - `tools/chinese-cook/ingredient-substitute.html` : `如：蚝油、料酒、八角...`
  - `tools/chinese-cook/sauce-ratio.html` : `如 2`
- **gardening2**
  - `tools/gardening2/fertilizer-ppm.html` : `如 200`
  - `tools/gardening2/fertilizer-ppm.html` : `如 1`
  - `tools/gardening2/fertilizer-ppm.html` : `如 20（0–100）`
  - `tools/gardening2/watering-frequency.html` : `如 15`
- **kids**
  - `tools/kids/focus-timer.html` : `如 15（5–45）`
  - `tools/kids/focus-timer.html` : `如 5（1–20）`
  - `tools/kids/focus-timer.html` : `如 4（1–12）`
  - `tools/kids/memory-palace.html` : `如：电话号码、圆周率、单词表`
- **office**
  - `tools/office/excel-formula-reference.html` : `搜索：VLOOKUP / IF / SUMIFS`
  - `tools/office/flowchart.html` : `在此输入 Mermaid 代码，例如： flowchart TD A[开始] --> B[结束]`
  - `tools/office/mindmap.html` : `# 主题 ## 分支一 - 子节点 ## 分支二`
  - `tools/office/pdf-split.html` : `例如：1-3, 5, 7-10`
- **railway**
  - `tools/railway/diaoche-zuoye-xiaolv-youhua.html` : `如 300`
  - `tools/railway/diaoche-zuoye-xiaolv-youhua.html` : `如 30`
  - `tools/railway/power-5.html` : `如 200`
  - `tools/railway/power-5.html` : `如 60`
- **fengshui**
  - `tools/fengshui/fengshui-calculator.html` : `如 0（0–360）`
  - `tools/fengshui/fengshui-guide.html` : `如:玄关、明堂、财位...`
  - `tools/fengshui/zodiac-lookup.html` : `如 1990（1900–2100）`
- **project**
  - `tools/project/manager-cost.html` : `如：官网改版项目`
  - `tools/project/manager-cost.html` : `如 100000`
  - `tools/project/manager-cost.html` : `如 90`
- **beekeeping**
  - `tools/beekeeping/honey-estimator.html` : `如 10（1–1000）`
  - `tools/beekeeping/honey-estimator.html` : `如 50（1–10000）`
- **express**
  - `tools/express/insurance-fee.html` : `如 5000`
  - `tools/express/insurance-fee.html` : `如 20000`
- **psychology**
  - `tools/psychology/generator-20.html` : `如 5（1–50）`
  - `tools/psychology/random-12.html` : `如 5（1–50）`
- **yi**
  - `tools/yi/64-gua.html` : `卦名/卦象/卦辞...`
  - `tools/yi/yi-divination.html` : `心中默念您要问的问题...`
- **cognition**
  - `tools/cognition/digit-span-test.html` : `在此输入答案`
- **daily-goods**
  - `tools/daily-goods/shoe-size.html` : `如 255（200–320）`

### JS 动态写中文 placeholder 的页面

- data/csv-json : 输入 CSV 内容...
- sales/commission-calculator : 无穷大(最后一档)

### 已知样例（农业线报告）

- `tools/agriculture/pesticide-dose.html`：`#activePct` placeholder `如 40`、`#targetPpm` placeholder `如 500`，两处均不在该页词典 `map` 中；真机 `?lang=en-US` 已复现（见第五节）。

## 二、机制现状（关键更正）

任务前提「全站没有 data-i18n-ph 这类属性级翻译机制」**不成立**，实际存在两套属性翻译路径：

1. **`js/i18n.js` 已有 `data-i18n-ph` / `data-i18n-title` / `data-i18n-aria` / `data-i18n-alt` 机制**（[i18n.js](file:///Users/cgw/project/cgw/chenguangwu.github.io/js/i18n.js#L735-L770)）：`apply()` 对声明了 `data-i18n-ph="key"` 的元素执行 `el.setAttribute('placeholder', t(key, fallback))`，并在 `snapshotFallback()` 把原文快照到 `data-i18n-ph-fb` 以便切回中文。目前全站仅 `common.js` 的搜索框使用（`search.placeholder`），**工具页 0 页声明**。
2. **`js/tool-i18n.js` 的第三层词典已有属性分支**（[tool-i18n.js](file:///Users/cgw/project/cgw/chenguangwu.github.io/js/tool-i18n.js#L881-L911)）：英文态 `applyEnDict()` 会扫描 `placeholder/title/aria-label/alt`，用 per-tool 字典 `i18n/tools/en/<ind>/<slug>.json` 的 `map` 精确匹配替换，并支持「标签：」前缀片段。**但它与文本键共用同一个 `map` 命名空间，且仅当词典恰好收录该 placeholder 原文时才生效**。

因此真正缺口不是「没有机制」，而是：
- 工具页没有声明 `data-i18n-ph`，通用 `i18n.js` 字典也没有对应键；
- 第三层词典的属性翻译是「碰巧命中」，词典未收录的 placeholder 不会翻译；
- 所有基于元素文本的检查（含 `_en_i18n_probe.mjs`）天然看不到属性值；属性分支在 `tool-i18n.js` 里存在，但探针没有单独核对 `el.placeholder`。

## 三、是否已有页面手工处理

- 工具页声明 `data-i18n-ph`：**0 页**。
- JS 里按语言条件改写 `placeholder` 的页面：**2 页**（若为写死中文则不是语言分支，需逐页复核）。
- 未发现工具页自建 `data-i18n-ph` 声明或按 `?lang=` 改写 placeholder 的通用封装；`tool-i18n.js` 的属性分支是唯一站点级处理，属「有人知道（代码里写了注释）但未形成数据侧机制」。

## 四、最小机制建议（只记录，不改代码）

**方案 A（推荐，改动最小）：复用 `data-i18n-ph`，不新增属性名**
1. 在工具页模板/构建期给 `input[placeholder]`、`textarea[placeholder]` 自动补 `data-i18n-ph="ph:<归一化中文>"`，`title` 补 `data-i18n-title="title:<归一化中文>"`。
2. 在 `js/i18n.js` 的 `I18N_DICT`（或行业层字典）增加 **独立属性键空间**：`ph:<中文原文>` / `title:<中文原文>`，避免与文本键冲突（现有 `map` 是文本键，同一个中文串可能同时用于标题和 placeholder，语义不同）。
3. `apply()` 的 `t(key, fallback)` 已支持 fallback；英文态未收录时保留中文并输出一条可统计的缺失信号，避免「静默残留」。
4. `_en_i18n_probe.mjs` 增加属性探针：直接读 `el.placeholder` / `el.title`，含汉字即报错（不复用可见文本的 `getClientRects()` 口径）。

**方案 B（不改页面模板）：扩展现有第三层词典**
- 在 `tool-i18n.js` 属性分支前，先用 `data-i18n-ph` 键查通用字典，再回退 per-tool `map`；构建期校验「页面所有含中文的 placeholder 必须出现在 `map` 或 `ph:` 键空间」。
- 风险：`map` 文本键与属性键同串不同义时会互相覆盖；必须先引入命名空间再加校验。

**影响面与风险**
- 静态影响面：12796 处 placeholder / 153 处 title，涉及 3947 页；其中 11505 处 placeholder、130 处 title 当前无词典键。
- 方案 A 需改构建模板 + `i18n.js` + 探针，属共享文件改动，必须全量 `_build.py` + `run_gates.py`；`data-i18n-ph-fb` 快照机制已存在，切回中文可逆。
- 若直接给现有 `map` 批量补 placeholder 键，会与文本键混用，存在同串不同义覆盖风险；因此建议独立 `ph:`/`title:` 键空间。
- `placeholder` 与 `value` 不同：只改属性、不碰表单值，工具计算逻辑无影响；但 `common.js` 的 `inputmode` 推断会读取 `inp.placeholder`，英文态替换后可能影响数字键盘推断，需回归。

## 五、抽样真机（2026-11-04，Chrome headless + `?lang=en-US`）

本地 `python3 -m http.server 8137` 起服务，puppeteer-core 打开 5 页，延迟 1.2 s 后直接读 `el.placeholder`（不套 `getClientRects()` 可见性过滤）：

| 页面 | 输入框总数 | placeholder 仍含中文 | 典型残留 | 结论 |
|---|---|---|---|---|
| `tools/agriculture/pesticide-dose.html` | 7 | **2** | `如 40` / `如 500` | 与农业线报告一致 |
| `tools/finance/profit-margin-calculator.html` | 26 | 0 | — | 词典命中，现有属性分支已译 |
| `tools/tcm-diagnosis/tcm-medical-record.html` | 29 | 0 | — | 词典命中，现有属性分支已译 |
| `tools/construction/construction-calculator.html` | 23 | **13** | `如 2.8` / `如 1210` / `如 5（0–50）` | 部分命中，未命中项残留 |
| `tools/it/matrix-transpose.html` | 9 | **1** | `如 2` | 3 个中文 placeholder 中 2 个命中，剩余 1 个残留 |

真机口径：

```js
[...document.querySelectorAll('input[placeholder],textarea[placeholder]')]
  .filter(el => /[\u4e00-\u9fff]/.test(el.placeholder))
  .map(el => ({ id: el.id, placeholder: el.placeholder }))
```

**真机结论**：残留不是「机制不存在」，而是「词典未收录 + 页面未声明」双重缺口；`finance`/`tcm` 两页 0 残留证明 `tool-i18n.js` 属性分支确实生效。
