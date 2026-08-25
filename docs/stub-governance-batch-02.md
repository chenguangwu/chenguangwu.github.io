# N1-01 跳转桩治理批次 02

## 执行时间
- 2026-08-20

## 处理类型
- DELETE：删除零入链（无站内 HTML/JS/JSON 引用）且目标真实存在的旧 slug 兼容跳转桩

## 处理前/后跳转桩总数
- 处理前：252
- 处理后：153
- 本批删除：99
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

## 删除明细（99 个）

- tools/accessibility/quick-ref-1.html
- tools/accounting/lookup-20.html
- tools/acupuncture/compare-9.html
- tools/antiques/tongxiuyanseyuniandai-yanghuachengdu.html
- tools/archive/generator-classify.html
- tools/astronomy/jizhou-jiyeriqipanduan-weidushuru.html
- tools/automotive/quick-ref-3.html
- tools/beauty/compare-perm-curling.html
- tools/building-material/classify-19.html
- tools/cable/manager-classify-protection.html
- tools/cardiology/classify-4.html
- tools/chemical/manager-classify-1.html
- tools/chinese-cook/youwenyupengrenfangshi-hua-chao-zha-duiyingzhina.html
- tools/cleaning/classify-31.html
- tools/clinical-lab/niaochenzhajingjian-guanxing-jiejing-tupu.html
- tools/clinical-nursing/compare-rater.html
- tools/community/hegui-shipin-anquan-shuiwu-baozhang.html
- tools/construction/loutitabuchicunsheji-zonggao-bugao.html
- tools/content/lookup-register-1.html
- tools/cosmetics/classify-35.html
- tools/customer-service/analysis-classify.html
- tools/daily-goods/sheji-gongnengyuzhinengduibijisuanqi.html
- tools/defense/lookup-recognize.html
- tools/dentistry/yaohejiechu-t-scan-pinghengdian.html
- tools/discipline/xinxihua-pingtai-shuju-zhineng-shexiang.html
- tools/domestic/classify-16.html
- tools/dyeing/kangziwaixian-upf-pingji.html
- tools/elderly/lookup-18.html
- tools/electrical/classify-117.html
- tools/energy/calc-voltage-capacity.html
- tools/ent/classify-3.html
- tools/environment/calculator-calc-carbon-1.html
- tools/express/lookup-17.html
- tools/film/guanjianzhenhuanruhuanchu-beisaier-quxian.html
- tools/fire/zhineng-wuxianyulianwangduibijisuanqi.html
- tools/fitness/titai-gupenqian-houqing-shaicha.html
- tools/food-processing/lookup-10.html
- tools/food-safety/stats-classify.html
- tools/food-testing/lookup-11.html
- tools/forestry/gushu-nianling-guce.html
- tools/funeral/classify.html
- tools/gardening/calculator-calc-12.html
- tools/gas/fangsan-anquan-fakongjing.html
- tools/general/classify-106.html
- tools/hardware/tool-009-93.html
- tools/healthcare/bmi.html
- tools/healthcare/tool-019-111.html
- tools/heattreat/tool-020-59.html
- tools/hematology/tool-015-7.html
- tools/hotel/tool-018-73.html
- tools/hr/tool-018-46.html
- tools/hr/training-hr.html
- tools/hydraulic/tool-002-39.html
- tools/hydraulic/tool-014-23.html
- tools/insurance/expense-ratio-ins.html
- tools/insurance/loss-ratio-ins.html
- tools/insurance/tool-001-12.html
- tools/interior/tool-018-81.html
- tools/jewelry/density.html
- tools/knowledge/tool-001-45.html
- tools/labor-protection/tool-019-105.html
- tools/landscape/tool-015-36.html
- tools/language/tool-005-9.html
- tools/language/tool-006-8.html
- tools/language/tool-009-5.html
- tools/leather/tool-008-37.html
- tools/leather/tool-017-23.html
- tools/literature/reading-tracker.html
- tools/livestock/time-28.html
- tools/livestream/tool-008-96.html
- tools/logistics/tool-018-39.html
- tools/machinery/elasticity-1.html
- tools/machinery/tool-014-298.html
- tools/machinery/tool-018-56.html
- tools/marketing/calc-confidence.html
- tools/martial-arts/time-gravity.html
- tools/media/tool-019-81.html
- tools/metallurgy/tool-002-65.html
- tools/metalwork/tool-014-117.html
- tools/metalwork/tool-015-57.html
- tools/metalwork/tool-021.html
- tools/metalwork/tool-035.html
- tools/metalwork/tool-042.html
- tools/meteorology/tool-004-68.html
- tools/meteorology/tool-006-56.html
- tools/meteorology/tool-007-57.html
- tools/meteorology/tool-011-24.html
- tools/mining/tool-011-59.html
- tools/mold/tool-010-53.html
- tools/municipal/tool-017-26.html
- tools/nephrology/tool-003-32.html
- tools/nephrology/tool-012-17.html
- tools/network/tool-005-7.html
- tools/neurology/tool-007-20.html
- tools/niche/time-pruning.html
- tools/nutrition/ratio-15.html
- tools/obstetrics/diagnosis-6.html
- tools/ophthalmology/tool-007-14.html
- tools/optical/tool-011-13.html

## 保留与阻塞

- 仍有入链的桩保留（KEEP），后续批次可先修正入链使其变零入链，再评估删除。
- 无法确认外部直接收录状态时按 NEXT 规则优先保留，仅删零入链且经 grep 校验无引用的安全项。
