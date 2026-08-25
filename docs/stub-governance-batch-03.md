# N1-01 跳转桩治理批次 03

## 执行时间
- 2026-08-20

## 处理类型
- DELETE：删除零入链（无站内 HTML/JS/JSON 引用）且目标真实存在的旧 slug 兼容跳转桩

## 处理前/后跳转桩总数
- 处理前：153
- 处理后：53
- 本批删除：100
- 本批恢复(KEEP)：1（发现被页面引用，按 NEXT 规则保留）

## 删除判定依据

- `scripts/audit_stubs.py` 审计：桩全部 `target_type=ok`（目标真实存在）。
- 候选 = 零入链（`incoming_count` 无站内 `<a>`/`<script>` 链接）且目标存在。
- 删除前额外用全工作区 grep 校验每个候选是否被任何文件引用（兜底 `incoming_count` 漏算非 `<a>` 入链），有引用者转 KEEP 不删。
- 桩页含 `<meta name="robots" content="noindex,follow">`，不被收录，删除无已收录 URL 404 风险。

## 门禁结果（删除后 `_build.py` 重建 + 四门禁，含恢复项复验）

- `_test_static.py`：0 失败 0 警告，相关工具映射 0 缺失 0 冗余
- `_audit_links.py --check`：0 死链
- `_audit_assets.py --check`：0 资产死链 / 0 lang 缺失 / 0 重复 id
- `node scripts/verify_calc.js`：ALL OK

## 恢复明细（KEEP，被发现仍有入链）

- tools/it/qrcode-generator.html

## 删除明细（100 个）

- tools/accessibility/mangwendianzi-pinyin-yingwen-zhuanyiqi.html
- tools/antiques/compare-5.html
- tools/archive/classify-12.html
- tools/astronomy/compare-1.html
- tools/automotive/lengque-sanre-fengliang-sheji.html
- tools/cable/classify-26.html
- tools/chemical/classify-24.html
- tools/chinese-cook/compare-ingredient.html
- tools/cleaning/classify-14.html
- tools/clinical-lab/compare-7.html
- tools/dentistry/classify-2.html
- tools/discipline/lookup-15.html
- tools/domestic/classify-15.html
- tools/dyeing/compare-6.html
- tools/fire/manager-classify-protection-3.html
- tools/food-safety/lookup-dosage.html
- tools/food-testing/dachangjunqun-mpnfa-jiansuobiao.html
- tools/general/classify-105.html
- tools/healthcare/fagui-guanggaofa-shipinanquan-shencha.html
- tools/hydraulic/daba-wendingxing-kanghua-kangqingfu.html
- tools/insurance/siwanglv-shengmingbiao-yubaofeigoucheng.html
- tools/labor-protection/cailiao-gongnengyuzhinengduibijisuanqi.html
- tools/language/yingyucigen-cizhuijiyika-jiaohukapian.html
- tools/leather/yinhua-yahua-shendu.html
- tools/metallurgy/shifa-jinchu-jinghua-dianji-gongyi.html
- tools/meteorology/rengong-yingxiang-zengyu-fangbao-zuoye.html
- tools/mining/weikuang-ku-ba-jiance-sheji.html
- tools/nephrology/niaodianjiezhi-na-jia-lv-paixie.html
- tools/ophthalmology/rengongjingti-iol-dushu-srk-t.html
- tools/optical/pianguangjing-zhouwei-jiaozheng.html
- tools/outdoor/tool-004-22.html
- tools/packaging/tool-013-29.html
- tools/paint/formula-color-diff.html
- tools/paper/tool-012-32.html
- tools/parenting/sleep-tracker.html
- tools/pediatrics/tool-001-25.html
- tools/pediatrics/tool-005-37.html
- tools/pet/tool-004-10.html
- tools/pet/tool-018-90.html
- tools/pharma/tool-013-96.html
- tools/pharmacy/tool-007-89.html
- tools/photography/tool-011-79.html
- tools/pipe/tool-020-109.html
- tools/pneumatic/tool-001-54.html
- tools/port/tool-020-35.html
- tools/pr/sentiment-analysis.html
- tools/pr/tool-012-76.html
- tools/procurement/tool-002-56.html
- tools/procurement/tool-008-48.html
- tools/procurement/turnover-inventory.html
- tools/project/tool-015-46.html
- tools/property/tool-005-56.html
- tools/psychiatry/tool-011-18.html
- tools/psychology/tool-006-10.html
- tools/pulmonology/tool-019-6.html
- tools/railway/route-1.html
- tools/railway/tool-014-45.html
- tools/realestate/tool-014-72.html
- tools/rehabilitation/tool-009-7.html
- tools/rental/tool-011-40.html
- tools/reproductive-medicine/power-injection.html
- tools/research/analysis-48.html
- tools/rheumatology/tool-003-33.html
- tools/road/estimate-19.html
- tools/rubber/strength-stretch.html
- tools/sales/tool-005-12.html
- tools/securities/tool-001-13.html
- tools/security-guard/tool-001-63.html
- tools/security/tool-019-104.html
- tools/seismology/tool-014-61.html
- tools/shipping/tool-004-54.html
- tools/sports-event/tool-007-71.html
- tools/sports/tool-005-47.html
- tools/sports/tool-011-27.html
- tools/sports/tool-011-29.html
- tools/statistics/statistics-15.html
- tools/statistics/statistics-2.html
- tools/statistics/statistics-3.html
- tools/statistics/statistics-6.html
- tools/statistics/statistics-8.html
- tools/statistics/statistics-9.html
- tools/steel/analysis-91.html
- tools/supplychain/tool-010-42.html
- tools/surface/tool-010-54.html
- tools/surveying/map-scale.html
- tools/surveying/tool-012-54.html
- tools/tcm-chemistry/tool-002-29.html
- tools/tcm-diagnosis/tool-007-11.html
- tools/tcm-pharmacy/tool-008-8.html
- tools/telecom/subnet.html
- tools/text/tool-004-1.html
- tools/text/tool-012-3.html
- tools/textile/tool-007-33.html
- tools/textile/tool-010-28.html
- tools/textile/tool-014-36.html
- tools/timber/wastewater-3.html
- tools/transport/tool-017-14.html
- tools/travel/packing-checklist.html
- tools/uiux/tool-003-91.html
- tools/unitedfront/tool-007-56.html

## 保留与阻塞

- 仍有入链的桩保留（KEEP），后续批次可先修正入链使其变零入链，再评估删除。
- 无法确认外部直接收录状态时按 NEXT 规则优先保留，仅删零入链且经 grep 校验无引用的安全项。
