# 编码/通信/安全/数据 · tools/{encode,telecom,security,data}（合计 ~100 页）

## 已知问题
### E1. encode 系结果仅文本
- ✅ 已落地（2026-10-26 · 落点 it/char-encoder 多格式字符编码器）：加「🔬 字节视图」卡（#byteViewBox：字符 ↔ 码点 ↔ UTF-8 字节 hex/binary 逐字符对照表，空格␣/换行⏎/制表⇥符号化、截前 64 字符、TBKit EN 守卫双语；空输入清空零渲染）。verify 强用例（Hi中 → U+4E2D e4 b8 ad 11100100…）；EN probe 全英文（输入回显除外）。verify it 763/763、判别器 0 逃生、门禁 218/218。

### E2. telecom 换算页口径混杂
- ✅ 已落地（2026-10-26）：bandwidth-calculator KB 选项 0.001→1/1024（byte 系统一 1024，GB/TB 原本已 1024）+ 「bit 系 1000 / byte 系 1024」口径标注（data-zh 双语）；quick-calc-time-bandwidth formula-eq 80 秒（1000 进制）与案例 91 秒（1024 进制）矛盾消除标注。verify 强用例（2048 KB=2.00 MB，clicks 直调）；verify telecom 11/11、判别器 0、门禁 218/218。

### E3. security 模拟器类内容单薄
- ✅ 已落地（2026-10-26 · data-erase-simulator）：加「📚 标准依据」徽标（#standardBadge 随选中算法切换：零填充→NIST 800-88 Clear 级 / 随机→Clear/Purge 过渡 / DoD→NIST 已不推荐说明 / Gutmann→1996 论文局限+建议加密擦除），对比表与 CSV 导出加「标准依据」列，页脚 NIST 800-88 Rev.1 三级别说明（data-zh 双语 + GEN_UI_MAP 映射）。⚠ 同批修两条弱锚：老用例锚「24」是 byteGrid 随机字节概率性回显（撞值即逃生）→ 收紧为 startSim 同步渲染的确定性步骤锚；新用例锚须带「标准依据」badge 专属前缀（compareTable 全算法列会把引据文本带进默认态）。verify security 11/11、判别器 0 逃生、门禁 218/218。
- ✅ 已落地（2026-10-26 · smoke-alarm-test / virtual-safe）：smoke-alarm 加 #alarmStdBadge 随报警器位置切换引据（GB 20517-2009 产品标准 + GB 50016 设置场所 + NFPA 72 每月测试，8 位置各配专属安装/选型文案，select onchange + 预设按钮联动，TBKit helper 双语）；verify +2 强位置锚（厨房附近「距烹饪区至少 3 米」/地下室「烟气易积聚」——badge 通用引据渲染不依赖输入，不可作 expect）。virtual-safe 加静态 NIST 800-63B/OWASP 标准徽标（data-zh，无 id 不进 blob 零用例影响）+ updateStrength 追加 NIST 长度建议动态行（masterPwd addEventListener input 在 stub 可触发）；verify +1 强锚。verify security 14/14、判别器 0、门禁 218/218。

## 功能缺陷
- ✅ 自定义多项式已落地（2026-10-26）：`it/crc-calculator` 加「自定义 CRC 模型」块（checkbox 默认关 ⇒ 零渲染；width 8–64/poly·init·xorout hex/refin·refout 勾选，复用 crcGeneric 在 8 标准算法后追加一行）；__gv 防御 harness stub 对静态 input .value 不解析 attribute 的坑。verify 自洽用例（CRC-8 参数+abc → 0x5f 与内置一致）；GEN_UI_MAP 补 7 条 label。verify it 764/764、判别器 0 逃生、门禁 218/218。（既往疑点已定性 2026-10-26：blob 中「undefined 0xundefined」×2 卡是 harness 兜底步骤无参直调 `renderResult()` 的伪影，真实浏览器无此调用路径，页面 8 张标准卡计算全对，无需改动。）

## 优化点
- S1 首屏即答案：编码类页默认给「Hello World」示例的完整编码链。
  - ✅ 试点落地（2026-10-26 · it/url-encode）：textarea 默认样例 `https://toolbox.example.com/search?q=你好 世界` + `__url_encodeFirstRender()` boot 静默首渲染（encodeURIComponent、output 空才写、不写历史不弹 toast）。同批修 1 条 B 类快照用例漂移（blob 段序变化 → 隔离 fullBlob 实测重写，判别力保持）。verify it 766/766、判别器 0、门禁 218/218。⚠ 首屏渲染串不依赖注入（A===B 盲区）→ 不配 expect，以既有用例零漂移为闭环标准。
  - 🔴 待续：同类空输入页 html-entities-encode / html-entity-encoder / url-encoder-advanced / uuencode（qr-decoder 需传图不算）；每页同批核对「默认态不含」反向锚。

## 受影响范围
- tools/encode/、tools/telecom/、tools/security/、tools/data/（合计 ~100 页）

## 进度
- 🟢 批次 2026-10-26：E1 字节视图（char-encoder）+ E2 进制统一（bandwidth-calculator/quick-calc）+ E3 引据徽标（data-erase-simulator）+ crc 自定义多项式均已落地。
- 🔴 待开发：S1 编码链默认示例。
