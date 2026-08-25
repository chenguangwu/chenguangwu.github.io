# N1-01 跳转桩治理批次 04

## 执行时间
- 2026-08-20

## 处理类型
- DELETE：删除零入链（无站内 HTML/JS/JSON 引用）且目标真实存在的旧 slug 兼容跳转桩

## 处理前/后跳转桩总数
- 处理前：53
- 处理后：19
- 本批删除：34
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

## 删除明细（34 个）

- tools/chemical/anquan-msds-xielou-xiaofang-yuan.html
- tools/discipline/compare-13.html
- tools/fire/extinguish-classify-extinguisher.html
- tools/food-safety/lookup-13.html
- tools/general/classify-104.html
- tools/outdoor/yewaidaohangfangweijiao-cipianjiao-xiuzheng.html
- tools/pediatrics/fare-yewen-gangwen-hulizhidao.html
- tools/pet/hegui-xuke-fangyi-shuiwu-baozhang.html
- tools/pharmacy/yibao-shuaka-baoxiao-jiesuan-caozuo.html
- tools/pipe/tool-004-110.html
- tools/pr/neirong-yingxiao-gushi-shipin-chuanbo.html
- tools/realestate/tool-013-33.html
- tools/rental/fangyuan-fabu-xiajia-zhuangtai.html
- tools/securities/yidongpingjunxian-ma-jincha-sichatishi.html
- tools/security/ai-zhinengyuhulianduibijisuanqi.html
- tools/seismology/lishi-dizhen-yizhi-shuju-ji.html
- tools/shipping/chishui-shuichi-zaizhongxian-biaoji.html
- tools/sports-event/yiliao-jijiu-zhan-yingji-baozhang.html
- tools/sports/zhuanxiang-pao-tiao-tou-jishufenjie.html
- tools/text/tool-006-3.html
- tools/textile/kangzhou-huifujiao-pingji.html
- tools/transport/jiaochakou-shijusanjiaoxing-qingkong.html
- tools/urban/tool-004-17.html
- tools/urology/tool-011-8.html
- tools/usedcar/tool-012-41.html
- tools/valve/tool-020-110.html
- tools/video/tool-005-105.html
- tools/warehouse/tool-005-107.html
- tools/water/tool-003-52.html
- tools/wedding/tool-005-16.html
- tools/welding/tool-004-74.html
- tools/welding/tool-012-62.html
- tools/woodwork/tool-003-11.html
- tools/yoga/tool-011-78.html

## 保留与阻塞

- 仍有入链的桩保留（KEEP），后续批次可先修正入链使其变零入链，再评估删除。
- 无法确认外部直接收录状态时按 NEXT 规则优先保留，仅删零入链且经 grep 校验无引用的安全项。
