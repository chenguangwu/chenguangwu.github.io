# N1-01 跳转桩治理批次 01

## 执行时间
- 2026-08-20

## 处理类型
- DELETE：删除零入链（无任何站内 HTML 链接指向）且目标真实存在的旧 slug 兼容跳转桩

## 处理前/后跳转桩总数
- 处理前：352
- 处理后：252
- 本批删除：100

## 删除判定依据

- 脚本 `scripts/audit_stubs.py` 审计：当前 352 个跳转桩全部 `target_type=ok`（目标真实存在，无 missing/external）。
- 其中 238 个零入链，满足 N1-01 删除条件：目标存在、零入链、同目标已有规范入口（目标工具页/行业页）。
- 跳转桩页本身含 `<meta name="robots" content="noindex,follow">`，不被搜索引擎收录，删除不会造成已收录 URL 的 404。
- 有入链 114 个保留（KEEP）：被站内引用，删之会产生死链，留待后续批次先修正入链再评估。
- 无法确认外部直接收录状态时按 NEXT 规则优先保留，本批仅删零入链安全项。

## 门禁结果（删除后 `_build.py` 重建 + 四门禁）

- `_test_static.py`：0 失败 0 警告，相关工具映射 0 缺失 0 冗余
- `_audit_links.py --check`：0 死链
- `_audit_assets.py --check`：0 资产死链 / 0 lang 缺失 / 0 重复 id
- `node scripts/verify_calc.js`：ALL OK

## 删除明细（100 个）

- tools/accessibility/tool-001-9.html
- tools/accounting/tool-012-72.html
- tools/acupuncture/strength-2.html
- tools/admin/tool-002-57.html
- tools/advertising/recognize-5.html
- tools/aerospace/tool-002-49.html
- tools/agriculture/countdown-6.html
- tools/agriculture/stats-recorder.html
- tools/antiques/tool-003-12.html
- tools/aquaculture/tool-013-19.html
- tools/aquaculture/tool-018-18.html
- tools/archaeology/estimate-area-2.html
- tools/archive/tool-013-45.html
- tools/astronomy/lookup-8.html
- tools/auto-beauty/tool-019-35.html
- tools/automation/tool-011-62.html
- tools/automotive/tool-007-42.html
- tools/baking/temp-time-humidity.html
- tools/ballistics/tool-014-21.html
- tools/beauty/tool-013-72.html
- tools/beekeeping/tool-012-25.html
- tools/beneficiation/tool-003-65.html
- tools/bonding/tool-018-62.html
- tools/brand/tool-016-70.html
- tools/building-material/tool-018-96.html
- tools/cable/voltage-3.html
- tools/cardiology/tool-008-14.html
- tools/casting/tool-003-68.html
- tools/chemical/tool-008-105.html
- tools/chinese-cook/tool-002-12.html
- tools/cleaning/tool-013-55.html
- tools/clinical-lab/tool-019-1.html
- tools/clinical-nursing/stats-recorder-2.html
- tools/cnc/tool-015-61.html
- tools/community/tool-015-96.html
- tools/construction/tool-015-3.html
- tools/consulting/tool-010-64.html
- tools/content/tool-010-39.html
- tools/convenience/price-7.html
- tools/cosmetic-derm/tool-005-38.html
- tools/cosmetics/formula-6.html
- tools/customer-service/ticket.html
- tools/daily-goods/tool-018-104.html
- tools/dailychem/tool-014-116.html
- tools/dance/tool-014-89.html
- tools/data/classify-11.html
- tools/decor/tool-007-41.html
- tools/defense/tool-009-62.html
- tools/dentistry/tool-007-13.html
- tools/dentistry/tool-012-12.html
- tools/dentistry/tool-015-8.html
- tools/dentistry/tool-017-6.html
- tools/dermatology/tool-014-17.html
- tools/discipline/tool-020-45.html
- tools/domestic/ratio-4.html
- tools/dyeing/tool-012-31.html
- tools/dyeing/tool-014-37.html
- tools/dyeing/tool-018-27.html
- tools/eco/eco-2.html
- tools/ecommerce/analysis-65.html
- tools/ecommerce/tool-017-33.html
- tools/elderly/tool-002-75.html
- tools/electrical/voltage-wire-pressure-drop.html
- tools/electronics/tool-006-36.html
- tools/electronics/tool-014-33.html
- tools/embedded/tool-005-51.html
- tools/endocrinology/tool-013-7.html
- tools/energy/estimate-6.html
- tools/energy/lookup-classify.html
- tools/ent/tool-020-8.html
- tools/environment/wastewater-solid-waste-classify.html
- tools/event/tool-019-78.html
- tools/exam/score-calculator.html
- tools/exhibition/tool-001-74.html
- tools/express/tool-012-65.html
- tools/film/tool-003-18.html
- tools/fire-rescue/angle-9.html
- tools/fire-rescue/tool-016-42.html
- tools/fire/tool-014-290.html
- tools/fishery/tool-006-11.html
- tools/fitness/generator-random-motion.html
- tools/fitness/tool-015-25.html
- tools/floral/tool-010-84.html
- tools/food-processing/tool-003-24.html
- tools/food-safety/tool-009-35.html
- tools/food-testing/tool-012-5.html
- tools/forensic-medicine/tool-008-22.html
- tools/forestry/tool-017-16.html
- tools/fresh/price-5.html
- tools/fun/demo-classify-fingerprint.html
- tools/funeral/tool-007-94.html
- tools/furniture/tool-004-103.html
- tools/gardening/compare-pruning.html
- tools/gas/tool-012-33.html
- tools/gastroenterology/tool-016-9.html
- tools/general/classify-107.html
- tools/geology/tool-008-55.html
- tools/geology/tool-019-54.html
- tools/gis/ratio-14.html
- tools/glass/tool-002-17.html

## 保留与阻塞

- 114 个有入链桩保留（KEEP），后续批次可先修正入链使其变零入链，再评估删除。
- 全部删除需等 GSC/外部收录数据确认，当前按保守规则仅删零入链安全项。
