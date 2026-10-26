# 摄影/视频 · tools/{photo,video}（~80 页）

## 已知问题
### P3. 自洽不立案：card-capacity GB×1000 与 photo-8 的 1024 进制跨页不一致——建议统一标注进制（列入本文件为唯一遗留）。
- ✅ 已标注（2026-10-26）：两页互加「进制口径说明」（p data-zh 双语，card-capacity 十进制卡厂口径 / photo-8 二进制 MiB 口径，7.4% 差异 + 跨页同口径折算提示）；各保留本行业正确口径不改数值。verify photo 64/64、判别器 0 逃生、门禁 218/218。

## 功能缺陷
- ✅ 景深系「超焦距街拍预设」（S2，2026-10-26）：hyperfocal 加 3 预设（28mm f/8 / 35mm f/5.6 / 35mm f/8）；depth-of-field 加 3 个「对焦在超焦距」预设（24mm f/8 @2.5m / 28mm f/8 @3.4m / 35mm f/5.6 @7.5m，均 s≥H ⇒ 远限 ∞ 演示）；labelEn 双语。顺带修两页 #result EN 存量泄漏（超焦距/近限/远限/∞ 全 __T + location fallback）。verify photo 64→69、判别器 0 逃生、EN 双页 OK_EN。
- ✅ 视频码率「平台推荐码率表」（2026-10-26）：video-compressor 平台预设 tab 追加「分辨率档位推荐码率表」（YouTube SDR 官方值 2160p 35-45/1440p 16/1080p 8/720p 5/480p 2.5 Mbps + 高帧率档；B站 4K 20/1080p 6/720p 3；抖音 4K 10-20/1080p 5/720p 2.5，标注以平台投稿入口为准）；新增 20 条 BODY_PHRASE_MAP 映射（含存量『抖音/快手』『约 N Mbps』泄漏修复）。Playwright HTTP 真机 EN 态 tabPlatform CJK=[]、zh 回归 OK；门禁 218/218。

## 优化点
- S3 分步：曝光三角页加 EV 补偿链路推导。
- S4 分享卡：黄金时刻/星历结果卡。

## 受影响范围
- tools/photo/（64）、tools/video/

## 进度
- 🟡 续批中（S2 街拍预设已落地；剩余：平台码率表 / S3 曝光三角 / S4 分享卡）
