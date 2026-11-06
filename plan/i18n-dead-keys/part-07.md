## 逐条清单（仅高优先 `dead`）

- `tools/it/regex-cheatsheet.html` : `/a+/ 匹配 "a" "aaa"，不匹配 ""` : dead
- `tools/it/regex-cheatsheet.html` : `[[:alpha:]]  字母 ⏎ [[:digit:]]  数字 ⏎ [[:space:]]  空白` : dead
- `tools/it/regex-cheatsheet.html` : `含 \t\n\r\f\v` : dead
- `tools/it/robots-txt-generator.html` : `选择 User-agent、Allow、Disallow 与 Sitemap，快速生成 <code>robots.txt</code>。` : dead
- `tools/it/sql-cheatsheet.html` : `BEGIN; ⏎ UPDATE accounts SET balance = balance - 100 WHERE id = 1; ⏎ UPDATE accounts SET balance = balance + 100 WHERE id = 2; ⏎ COMMIT;  -- 或 ROLLBACK` : dead
- `tools/it/sqlite-cheatsheet.html` : `共 46 项` : dead
- `tools/it/team-name-generator.html` : `组合 = 风格词库（形容词 × 名词）× 可选后缀` : dead
- `tools/it/text-similarity.html` : `|  文本A长度: 14  |  文本B长度: 15` : dead
- `tools/it/text-similarity.html` : `|  文本A长度: 14  |  文本B长度: 15` : dead
- `tools/it/text-similarity.html` : `插入 1 次` : dead
- `tools/it/text-similarity.html` : `文本长度不等（A: 14, B: 15），汉明距离仅适用于等长字符串。` : dead
- `tools/it/text-similarity.html` : `替换 4 次` : dead
- `tools/it/text-to-hex.html` : `\\x 前缀` : dead
- `tools/it/time-format-converter.html` : `同一时刻在不同时区显示的"墙钟时间"不同。请确认所选时区与你的日志来源一致，否则转换出的日期会差几小时。` : dead
- `tools/it/time-format-converter.html` : `输入 Unix 秒级时间戳 '1690000000' → 输出 '2023-07-22 08:53:20 UTC'（按所选时区换算）。 ⏎ 反向：输入 '2023-07-22 08:53:20' + 时区 UTC → 输出 '1690000000'。` : dead
- `tools/it/timestamp-converter.html` : `✅ 识别为微秒时间戳（16 位）→ 已同步填充秒、毫秒与日期时间` : dead
- `tools/it/timestamp-converter.html` : `✅ 识别为毫秒时间戳（12 位）→ 已同步填充秒、毫秒与日期时间` : dead
- `tools/it/timestamp-converter.html` : `东京 (GMT+9)` : dead
- `tools/it/timestamp-converter.html` : `伦敦 (GMT+0)` : dead
- `tools/it/timestamp-converter.html` : `北京 (GMT+8)` : dead
- `tools/it/timestamp-converter.html` : `夏威夷 (GMT-10)` : dead
- `tools/it/timestamp-converter.html` : `巴黎 (GMT+1)` : dead
- `tools/it/timestamp-converter.html` : `悉尼 (GMT+11)` : dead
- `tools/it/timestamp-converter.html` : `洛杉矶 (GMT-8)` : dead
- `tools/it/timestamp-converter.html` : `纽约 (GMT-5)` : dead
- `tools/it/tmux-cheatsheet.html` : `# 先按 C-b 再按后续键 ⏎ # 例：C-b c 新建窗口` : dead
- `tools/it/tmux-cheatsheet.html` : `C-b "  -- 上下分割` : dead
- `tools/it/tmux-cheatsheet.html` : `C-b (  上个 ⏎ C-b )  下个` : dead
- `tools/it/tmux-cheatsheet.html` : `C-b :set mouse on  -- 开启鼠标 ⏎ C-b :source ~/.tmux.conf  -- 重载配置` : dead
- `tools/it/tmux-cheatsheet.html` : `C-b [  -- 进入复制模式 ⏎   空格 开始选择 ⏎   Enter 复制 ⏎   q 退出` : dead
- `tools/it/tmux-cheatsheet.html` : `C-b n  下个 ⏎ C-b p  上个` : dead
- `tools/it/tmux-cheatsheet.html` : `C-b q  -- 显示编号 ⏎ C-b q 2  -- 跳到 2 号` : dead
- `tools/it/tmux-cheatsheet.html` : `C-b t  -- 大时钟 ⏎ 任意键退出` : dead
- `tools/it/tmux-cheatsheet.html` : `setw -g mode-keys vi ⏎ # 复制模式下：hjkl 移动, v 选择, y 复制` : dead
- `tools/it/tmux-cheatsheet.html` : `tmux  -- 匿名会话 ⏎ tmux new -s work  -- 名为 work ⏎ tmux new -s work -d  -- 后台` : dead
- `tools/it/tmux-cheatsheet.html` : `tmux kill-session -t old ⏎ tmux kill-session -a  -- 关闭除当前外所有` : dead
- `tools/it/triangle-calculator.html` : `判断类型：任一内角≈90° 为直角，三者都<90° 为锐角，否则为钝角（浮点误差用 1e-6 容差）。` : dead
- `tools/it/typescript-cheatsheet.html` : `class C { ⏎   private x = 1;  -- 仅本类 ⏎   protected y = 2;  -- 子类 ⏎   #z = 3;  -- 真私有 ⏎ }` : dead
- `tools/it/typescript-cheatsheet.html` : `const cfg = { port: 80 } satisfies Config; ⏎ -- 保留字面量类型，又校验` : dead
- `tools/it/typescript-cheatsheet.html` : `enum Color { Red, Green, Blue } ⏎ let c: Color = Color.Red; ⏎  ⏎ const enum Dir { Up, Down }  -- 内联` : dead
- `tools/it/typescript-cheatsheet.html` : `function id<T>(x: T): T { return x; } ⏎ const r = id<number>(5); ⏎ const r2 = id("a");  -- 推断` : dead
- `tools/it/typescript-cheatsheet.html` : `interface User { ⏎   id: number; ⏎   name: string; ⏎   greet?(): void;  -- 可选方法 ⏎ }` : dead
- `tools/it/typescript-cheatsheet.html` : `let el = document.querySelector("#x"); ⏎ el!.value;  -- 断言非空` : dead
- `tools/it/typescript-cheatsheet.html` : `let x: string | number = 1; ⏎ let y: "a" | "b" | "c" = "a";  -- 字面量联合` : dead
- `tools/it/typescript-cheatsheet.html` : `共 43 项` : dead
- `tools/it/url-qr.html` : `M（约 15%）最常用；打印尺寸小或物料易磨损时选 Q/H，代价是同样内容需要更高版本、模块更密。L 容量最大但容错最弱，适合屏幕展示。` : dead
- `tools/it/url-qr.html` : `'https://ex.com/a'（16 字节，纠错 M）→ 最小版本 V2（25×25 模块），矩阵可直接扫码。` : dead
- `tools/it/url-qr.html` : `是。链接越长字节数越大，版本与模块数随之上升，小尺寸打印时更难扫。可在保持最终落地页不变的前提下使用短链。` : dead
- `tools/it/url-qr.html` : `生成的是真二维码还是示意图？` : dead
- `tools/it/url-qr.html` : `真二维码。矩阵由本地 ISO/IEC 18004 编码器计算，包含 Reed-Solomon 纠错码字、格式信息与掩码；页面不联网、不上传网址，可直接用手机相机实扫验证。` : dead
- `tools/it/url-qr.html` : `纠错等级选哪个？` : dead
- `tools/it/vim-cheatsheet.html` : `"ayy  -- 复制行到寄存器 a ⏎ "ap  -- 粘贴寄存器 a ⏎ "+y  -- 复制到系统剪贴板 ⏎ "+p  -- 从系统剪贴板粘贴` : dead
- `tools/it/vim-cheatsheet.html` : `*  向下搜光标词 ⏎ #  向上搜光标词` : dead
- `tools/it/vim-cheatsheet.html` : `/function ⏎ n  下一个匹配 ⏎ N  上一个匹配` : dead
- `tools/it/vim-cheatsheet.html` : `:!ls ⏎ :!make test ⏎ :%!jq .  -- 格式化整个文件` : dead
- `tools/it/vim-cheatsheet.html` : `:e other.txt ⏎ :e!  -- 放弃修改重载` : dead
- `tools/it/vim-cheatsheet.html` : `:r other.txt  -- 插入文件内容 ⏎ :r! date  -- 插入命令输出` : dead
- `tools/it/vim-cheatsheet.html` : `:s/old/new/g  当前行全部 ⏎ :%s/old/new/g  全文件 ⏎ :%s/old/new/gc  全文件确认 ⏎ :5,10s/old/new/g  5-10 行` : dead
- `tools/it/vim-cheatsheet.html` : `:set number  -- 显示行号 ⏎ :set nonumber ⏎ :set tabstop=4 ⏎ :set expandtab ⏎ :set autoindent ⏎ :set hlsearch  -- 高亮搜索 ⏎ :set ignorecase  -- 忽略大小写 ⏎ :set paste  -- 粘…(+3字)` : dead
- `tools/it/vim-cheatsheet.html` : `:split  水平分割 ⏎ :vsplit  垂直分割 ⏎ Ctrl+w w  切换窗口 ⏎ :q  关闭当前窗口` : dead
- `tools/it/vim-cheatsheet.html` : `:tabnew ⏎ :tabnext  下个标签 ⏎ :tabprev  上个标签 ⏎ gt  下个标签 ⏎ gT  上个标签` : dead
- `tools/it/vim-cheatsheet.html` : `:w ⏎ :q ⏎ :wq ⏎ :q!  -- 不保存退出 ⏎ :x  -- 保存退出 ⏎ ZZ  -- 等价 :x ⏎ ZQ  -- 等价 :q!` : dead
- `tools/it/vim-cheatsheet.html` : `:w  保存 ⏎ :q  退出 ⏎ :wq 保存退出 ⏎ :q! 强制退出` : dead
- `tools/it/vim-cheatsheet.html` : `>G  缩进到文件末 ⏎ >>  缩进当前行 ⏎ <V  块选后取消缩进` : dead
- `tools/it/vim-cheatsheet.html` : `Ctrl+f  下一页 ⏎ Ctrl+b  上一页` : dead
- `tools/it/vim-cheatsheet.html` : `Ctrl+o  跳回上个位置 ⏎ Ctrl+i  跳到下个位置` : dead
- `tools/it/vim-cheatsheet.html` : `Ctrl+u  上半屏 ⏎ Ctrl+d  下半屏` : dead
- `tools/it/vim-cheatsheet.html` : `cw  改单词 ⏎ c$  改到行末 ⏎ cc  改整行` : dead
- `tools/it/vim-cheatsheet.html` : `dw  删到下个单词 ⏎ de  删到单词末尾 ⏎ d$  删到行末 ⏎ dd  删行 ⏎ dG  删到文件末` : dead
- `tools/it/vim-cheatsheet.html` : `gg  文件首 ⏎ G  文件末 ⏎ 100G  跳到 100 行` : dead
- `tools/it/vim-cheatsheet.html` : `h 左 ⏎ j 下 ⏎ k 上 ⏎ l 右` : dead
- `tools/it/vim-cheatsheet.html` : `i  光标前插入 ⏎ a  光标后插入 ⏎ I  行首插入 ⏎ A  行末插入 ⏎ o  下方新行 ⏎ O  上方新行` : dead
- `tools/it/vim-cheatsheet.html` : `ma  设置标记 a ⏎ 'a  跳到标记 a ⏎ 'a  跳到标记行首` : dead
- `tools/it/vim-cheatsheet.html` : `p  光标后粘贴 ⏎ P  光标前粘贴` : dead
- `tools/it/vim-cheatsheet.html` : `u  撤销 ⏎ Ctrl+r  重做` : dead
- `tools/it/vim-cheatsheet.html` : `v  字符选择 ⏎ V  行选择 ⏎ Ctrl+v  块选择` : dead
- `tools/it/vim-cheatsheet.html` : `vim file.txt ⏎ vim +100 file.txt  -- 跳到 100 行 ⏎ vim -R file.txt  -- 只读` : dead
- `tools/it/vim-cheatsheet.html` : `w  下个单词开头 ⏎ b  上个单词开头 ⏎ e  下个单词末尾` : dead
- `tools/it/vim-cheatsheet.html` : `x  删字符 ⏎ dd  删整行 ⏎ yy  复制整行 ⏎ 3dd  删 3 行 ⏎ 3yy  复制 3 行` : dead
- `tools/it/vim-cheatsheet.html` : `yw  复制单词 ⏎ y$  复制到行末 ⏎ yG  复制到文件末` : dead
- `tools/it/vim-cheatsheet.html` : `{  上个段落 ⏎ }  下个段落` : dead
- `tools/it/whitespace.html` : `因为行首空格（缩进）也属于空白字符：若选择了「合并连续空格为单个」或「去除每行首尾空白」，代码缩进与列表层级都会被去掉。处理代码或带结构文本时应关闭「去除每行首尾空白」、只压缩行内重复空格；建议先小段试处理，确认效果再全量应用。` : dead
- `tools/it/whitespace.html` : `清理示例` : dead
- `tools/it/whitespace.html` : `输入 "  a   b \n\n  c  "，勾选「去除行首尾空白」「删除空行」「合并连续空格为单个」后 → "a b\nc"；若再勾选「压成一行」则 → "a b c"。只勾选选项时页面结果区会同步给出字符数与空行数变化。` : dead
- `tools/it/xml-to-yaml.html` : `<note> ⏎   <to>Tony</to> ⏎   <from>Anna</from> ⏎   <heading>Reminder</heading> ⏎   <body>Don't forget me!<!-- TOOLBOX-DEEP-DIVE --> ⏎ <style> ⏎ .deep-dive{max-w…(+1836字)` : dead

  其它成因样例（共 2755 条，仅列前 5）：
  - `tools/it/ascii-art.html` : `Block 方块` : dynamic
  - `tools/it/ascii-art.html` : `Box 实心` : dynamic
  - `tools/it/bacon-cipher.html` : `0/1 编码` : dynamic
  - `tools/it/barcode-ean.html` : `请输入 12 或 13 位数字（EAN-13）` : dynamic
  - `tools/it/barcode-ean.html` : `输入含非数字字符，请只填写数字` : dynamic

### jewelry（dead 2 / dynamic 0 / fragment 0 / harmless 0）

- `tools/jewelry/gem-hardness.html` : `硬度≥7适合日常佩戴(耐刮擦)；硬度6-7需小心使用；硬度<6仅适合耳环、吊坠等不易碰撞的饰品，避免与硬物接触。` : dead
- `tools/jewelry/gem-hardness.html` : `较软 (<6)` : dead

### language（dead 10 / dynamic 33 / fragment 11 / harmless 0）

- `tools/language/calc-1.html` : `词汇量估算 = f(测试正确率, 词表)` : dead
- `tools/language/calc-2.html` : `阅读速度 = 字数 / 时间` : dead
- `tools/language/grammar-checker.html` : `密度 = 问题数 ÷ 句数。低于 0.5 通常可接受，0.5~1.5 建议逐句修订，高于 1.5 说明基础错误密集，建议先整体润色再逐条改。` : dead
- `tools/language/grammar-checker.html` : `按规则与统计模型双重检测：常见问题含中英文标点混用、句子成分缺失、主谓不一致、搭配不当、同一词在 20 字内重复出现；每处问题给出位置偏移与修改建议，问题密度 = 问题数 ÷ 总句数；改写建议按最小编辑距离优选；密度低于 0.5 属良好、0.5 至 1.5 建议局部修订、超过 1.5 需整体润色。` : dead
- `tools/language/grammar-checker.html` : `英文：常见拼写（teh、recieve、definately 等）、第三人称单数缺 -s、a/an 误用、your welcome、重复词；中文：中英标点混用、叠字、状语“的”应为“地”、动词补语“的”应为“得”、“在/再”混用。规则命中会给出来源片段与修改建议，不自动改写原文。` : dead
- `tools/language/grammar-checker.html` : `覆盖的检查类型` : dead
- `tools/language/grammar-checker.html` : `规则按词面模式匹配，对非常规但正确的句式（如倒装、专有名词、文学表达）可能误判；每条提示都注明命中的片段，请结合上下文判断。` : dead
- `tools/language/grammar-checker.html` : `规则检查只能抓规则表覆盖的明显硬错；语义、逻辑、搭配不当和长难句结构问题会漏检，规则也可能对非常规但正确的句式产生提示。重要文本仍需人工复核。` : dead
- `tools/language/grammar-checker.html` : `问题密度怎么用？` : dead
- `tools/language/stats-2.html` : `汉字数 + 英文单词数 + 数字字符数 + 标点数 + 空白符 = 总字符数` : dead

  其它成因样例（共 44 条，仅列前 5）：
  - `tools/language/calc-1.html` : `认识单词数：` : dynamic
  - `tools/language/calc-1.html` : `估算词汇量：` : dynamic
  - `tools/language/calc-1.html` : `估算区间（95%）：` : dynamic
  - `tools/language/calc-1.html` : `水平参考：` : dynamic
  - `tools/language/calc-1.html` : `区间按 20 个抽样词的二项标准误估算，结果为粗略参考。` : dynamic

### leather（dead 12 / dynamic 8 / fragment 3 / harmless 0）

- `tools/leather/area-20.html` : `💡 厚度分级：≥3.5mm 头层厚皮 / 1.2~3.5mm 头层 / 0.8~1.2mm 薄头层 / <0.8mm 二层；面积分级：≥25 大皮 / 15~25 中皮 / 8~15 小皮 / <8 碎皮` : dead
- `tools/leather/xueyunhoudukongzhi.html` : `不是。评分只按刀痕间距分档，反映参数组合的粗细程度；实际厚度精度还受刀片锋利度、皮张含水与张力影响，须用测厚仪多点实测抽检。` : dead
- `tools/leather/xueyunhoudukongzhi.html` : `为什么要求来料厚度大于目标厚度？` : dead
- `tools/leather/xueyunhoudukongzhi.html` : `刀片锋利度与刀距同样影响削匀质量` : dead
- `tools/leather/xueyunhoudukongzhi.html` : `刀痕间距 = 1000 × 进给速度 ÷ 转速（mm/rev）；切除量 = 来料厚度 − 目标厚度；评分按间距分档（≤0.5、≤1、≤2、≤4、>4 分别记 100、85、70、50、30）。例如进给 8 m/min、转速 4000 rpm → 间距 2.00 mm/rev → 70 分（一般）；转速提到 8000 r…(+31字)` : dead
- `tools/leather/xueyunhoudukongzhi.html` : `削匀只去除余量，来料必须留有余量才能达到目标厚度；相等或更薄时没有可切除材料，参数再优也无法成活。` : dead
- `tools/leather/xueyunhoudukongzhi.html` : `实际偏差须用测厚仪多点测量` : dead
- `tools/leather/xueyunhoudukongzhi.html` : `来料 2.0 mm、目标 1.2 mm、转速 4000 rpm、进给 8 m/min：切除量 0.80 mm，间距 1000×8÷4000 = 2.00 mm/rev，评分 70（一般）；同参数若转速降至 1200 rpm，间距 6.67 mm/rev，评分 30（不合格），建议提高转速或降低进给。注意评分只反映参数粗…(+11字)` : dead
- `tools/leather/xueyunhoudukongzhi.html` : `评分是实测均匀度吗？` : dead
- `tools/leather/xueyunhoudukongzhi.html` : `进给越快、转速不变时刀痕间距越大，单位长度内切削次数减少，易出现波纹与厚度不均；降低进给或提高转速可减小间距、改善表面平整度。` : dead
- `tools/leather/xueyunhoudukongzhi.html` : `高转速、低进给有利于均匀度` : dead
- `tools/leather/xueyunhoudukongzhi.html` : `💡 均匀度评分 = min(100, 转速÷进给速度×10)；厚度偏差 ≈ (100−评分)×0.05 mm` : dead

  其它成因样例（共 11 条，仅列前 5）：
  - `tools/leather/calc-dosage-4.html` : `硫化钠浓度须在 0–20% 之间（常温溶解度上限）` : dynamic
  - `tools/leather/calc-dosage-4.html` : `液比不得为负` : dynamic
  - `tools/leather/calc-dosage-4.html` : `皮重须大于 0` : fragment
  - `tools/leather/xueyunhoudukongzhi.html` : `刀痕间距 (mm/rev)` : fragment
  - `tools/leather/xueyunhoudukongzhi.html` : `切除量 (mm)` : fragment

### legal（dead 24 / dynamic 6 / fragment 6 / harmless 1）

- `tools/legal/arbitration-fee.html` : `仲裁费 = 标的×费率（分段）` : dead
- `tools/legal/calc-16.html` : `诉讼时效届满日 = 起算日 + 期间` : dead
- `tools/legal/estimate-salary.html` : `劳动争议赔偿 = 工资×年限×系数` : dead
- `tools/legal/food-safety.html` : `退一赔十 = 价款 × 10（或损失×3）` : dead
- `tools/legal/inheritance-share.html` : `继承份额 = 法定比例分配` : dead
- `tools/legal/ipr-damages.html` : `侵权赔偿 = 损失/获利/许可费` : dead
- `tools/legal/labor-compensation.html` : `经济补偿 = N × 月薪（封顶）` : dead
- `tools/legal/labor-compensation-n1.html` : `N+1 补偿 = (N+1) × 月薪` : dead
- `tools/legal/late-payment-interest.html` : `逾期利息 = 本金 × 日利率 × 天数` : dead
- `tools/legal/legal-age.html` : `法定年龄 = 当前 − 出生日期` : dead
- `tools/legal/legal-calculator.html` : `法律计算 = 通用公式` : dead
- `tools/legal/legal-reference.html` : `法律查询 = 条文匹配` : dead
- `tools/legal/loan-statute-limitations.html` : `借款时效 = 起算 + 3年` : dead
- `tools/legal/marriage-property-agreement.html` : `婚姻财产 = 共同/个人划分` : dead
- `tools/legal/notarization-fee.html` : `公证费 = 标的×费率` : dead
- `tools/legal/overtime-pay.html` : `加班费 = 基数 × 150%/200%/300%` : dead
- `tools/legal/patent-fee-calculator.html` : `专利费 = 年费×年度` : dead
- `tools/legal/patent-term-calculator.html` : `专利有效期 = 申请日 + 20年` : dead
- `tools/legal/personal-injury.html` : `人身损害 = 医疗费+误工+残疾` : dead
- `tools/legal/rent-deposit.html` : `租房押金 = 月租 × 倍数` : dead
- `tools/legal/severance-pay.html` : `违法解除 2N = 2N × 月薪` : dead
- `tools/legal/social-security-base.html` : `社保基数 = 工资（上下限）` : dead
- `tools/legal/stamp-duty-legal.html` : `印花税 = 金额 × 税率` : dead
- `tools/legal/statute-limitations.html` : `诉讼时效 = 起算 + 期间` : dead

  其它成因样例（共 13 条，仅列前 5）：
  - `tools/legal/calc-96.html` : `违约金 = 合同总额 × 违约金比例%` : fragment
  - `tools/legal/inheritance-share.html` : `配偶` : fragment
  - `tools/legal/inheritance-share.html` : `子女` : fragment
  - `tools/legal/jicheng-yizhu-gongzheng-yichan-fenpei.html` : `⚖️ 继承（遗嘱/公证/遗产）分配` : harmless
  - `tools/legal/lawyer-fee-reference.html` : `费用构成：` : dynamic

### library（dead 1 / dynamic 9 / fragment 2 / harmless 0）

- `tools/library/generator-label.html` : `档案盒脊背标签打印格式生成。免费在线工具，纯前端处理，数据不上传，保护隐私安全。` : dead

  其它成因样例（共 11 条，仅列前 5）：
  - `tools/library/generator-label.html` : `机构` : fragment
  - `tools/library/generator-label.html` : `标签行数` : dynamic
  - `tools/library/generator-label.html` : `字号` : fragment
  - `tools/library/generator-label.html` : `请至少填写一项标签内容。` : dynamic
  - `tools/library/generator-label.html` : `本次生成` : dynamic

### life（dead 254 / dynamic 62 / fragment 17 / harmless 0）

- `tools/life/age-calculator.html` : `周岁 = 今年 − 出生年（月/日/时/分/秒逐级借位修正）` : dead
- `tools/life/age-calculator.html` : `如何使用精确年龄计算器？` : dead
- `tools/life/age-calculator.html` : `精确年龄计算器是做什么的？` : dead
- `tools/life/age-calculator.html` : `精确年龄计算器适合哪些场景？` : dead
- `tools/life/age-in-days.html` : `如何使用年龄天数计算？` : dead
- `tools/life/age-in-days.html` : `年龄天数计算是做什么的？` : dead
- `tools/life/age-in-days.html` : `年龄天数计算适合哪些场景？` : dead
- `tools/life/analysis-23.html` : `如何使用景观（风水/视线）分析？` : dead
- `tools/life/analysis-23.html` : `景观（风水/视线）分析是做什么的？` : dead
- `tools/life/analysis-23.html` : `景观（风水/视线）分析适合哪些场景？` : dead
- `tools/life/analysis-74.html` : `如何使用竞争（分析/应对/差异化）？` : dead
- `tools/life/analysis-74.html` : `竞争（分析/应对/差异化）是做什么的？` : dead
- `tools/life/analysis-74.html` : `竞争（分析/应对/差异化）适合哪些场景？` : dead
- `tools/life/analysis-80.html` : `如何使用损耗（控制/分析/改善）体系？` : dead
- `tools/life/analysis-80.html` : `损耗（控制/分析/改善）体系是做什么的？` : dead
- `tools/life/analysis-80.html` : `损耗（控制/分析/改善）体系适合哪些场景？` : dead
- `tools/life/analysis-cost-10.html` : `如何使用成本（控制/分析/优化）体系？` : dead
- `tools/life/analysis-cost-10.html` : `成本（控制/分析/优化）体系是做什么的？` : dead
- `tools/life/analysis-cost-10.html` : `成本（控制/分析/优化）体系适合哪些场景？` : dead
- `tools/life/analysis-cost-9.html` : `不会自动识别科目。可在每行第三列手动标注「固定」或「变动」（也接受 F/V），工具据此拆分；不标则计入“未分类”，只做总量与占比统计。` : dead
- `tools/life/analysis-cost-9.html` : `原料 42（变动）、人工 31（固定）、物流 15（变动）、能耗 9（固定）：合计 97，固定 40（41.24%）、变动 57（58.76%）。若产量 1000、单价 0.12，则单位成本 0.0970、单位变动成本 0.0570、边际贡献 0.0630，盈亏平衡产量 = 40 ÷ 0.0630 ≈ 634.9，当前…(+57字)` : dead
- `tools/life/analysis-cost-9.html` : `可按部门或产品线分次贴入分别统计，再横向比较占比；同一次统计内保持科目口径一致。` : dead
- `tools/life/analysis-cost-9.html` : `固定/变动拆解与盈亏平衡` : dead
- `tools/life/analysis-cost-9.html` : `在第三列标注「固定/变动」，拆出固定成本与变动成本，算出单位成本与盈亏平衡产量。` : dead
- `tools/life/analysis-cost-9.html` : `如何使用成本（控制/优化/分析）体系？` : dead
- `tools/life/analysis-cost-9.html` : `成本（控制/优化/分析）体系是做什么的？` : dead
- `tools/life/analysis-cost-9.html` : `成本（控制/优化/分析）体系适合哪些场景？` : dead
- `tools/life/analysis-cost-9.html` : `把各项成本金额贴入，看合计、均值与占比最大的成本项。` : dead
- `tools/life/analysis-cost-9.html` : `盈亏平衡产量为什么显示“—”？` : dead
- `tools/life/analysis-cost-9.html` : `需要同时填写产量与单价，且单价必须高于单位变动成本；否则边际贡献 ≤ 0，任何产量都无法覆盖固定成本，页面会给出提示。` : dead
- `tools/life/angle-converter.html` : `如何使用角度换算？` : dead
- `tools/life/angle-converter.html` : `角度换算是做什么的？` : dead
- `tools/life/angle-converter.html` : `角度换算适合哪些场景？` : dead
- `tools/life/area-converter.html` : `如何使用面积换算？` : dead
- `tools/life/area-converter.html` : `面积换算是做什么的？` : dead
- `tools/life/area-converter.html` : `面积换算适合哪些场景？` : dead
- `tools/life/assessor-target.html` : `A 铺：人流 8000、竞争 2 家、人口 3 万、租金 120 元/m²、可见性 8 分 → 综合约 82 分（优秀）；B 铺：人流 3000、竞争 5 家、人口 1 万、租金 200 元/m²、可见性 5 分 → 约 48 分（一般）；在资源有限时优先洽谈 A 铺。` : dead
- `tools/life/assessor-target.html` : `按人流量、竞争密度、常住人口、租金、可见性五维加权评分输出综合分与选址等级（A/B/C）；模型量化选址要素，结果为网点布局决策参考，最终盈利还看选品与运营。` : dead
- `tools/life/assessor-target.html` : `无冲突排课率` : dead
- `tools/life/assessor-target.html` : `某铺租金 260 元/m²（得分较低），但人流、人口与可见性均接近满分，综合仍达 70 分；说明高租金可由强客流部分抵消，不应只凭租金一项否决。` : dead
- `tools/life/assessor-target.html` : `页面内置经验权重：人流 30%、竞争 20%、人口 20%、租金 15%、可见性 15%；业态不同时可据此判断偏重，是否调整以自身经营经验为准。` : dead
- `tools/life/base-convert.html` : `如何使用进制转换器？` : dead
- `tools/life/base-convert.html` : `进制转换器是做什么的？` : dead
- `tools/life/base-convert.html` : `进制转换器适合哪些场景？` : dead
- `tools/life/bill-splitter.html` : `AA制账单分摊是做什么的？` : dead
- `tools/life/bill-splitter.html` : `AA制账单分摊适合哪些场景？` : dead
- `tools/life/bill-splitter.html` : `如何使用AA制账单分摊？` : dead
- `tools/life/birthday-paradox.html` : `如何使用生日悖论计算器？` : dead
- `tools/life/birthday-paradox.html` : `生日悖论计算器是做什么的？` : dead
- `tools/life/birthday-paradox.html` : `生日悖论计算器适合哪些场景？` : dead
- `tools/life/bra-size-converter.html` : `如何使用罩杯尺寸换算？` : dead
- `tools/life/bra-size-converter.html` : `罩杯尺寸换算是做什么的？` : dead
- `tools/life/bra-size-converter.html` : `罩杯尺寸换算适合哪些场景？` : dead
- `tools/life/chinese-number.html` : `中文数字转换是做什么的？` : dead
- `tools/life/chinese-number.html` : `中文数字转换适合哪些场景？` : dead
- `tools/life/chinese-number.html` : `如何使用中文数字转换？` : dead
- `tools/life/chinese-number.html` : `简体/大写支持「点」逐位小数，负数前置「负」` : dead
- `tools/life/chinese-number.html` : `金额：阿拉伯数字 → 人民币大写，金额末尾加"元整"` : dead
- `tools/life/clothing-size-converter.html` : `如何使用服装尺码换算？` : dead
- `tools/life/clothing-size-converter.html` : `服装尺码换算是做什么的？` : dead
- `tools/life/clothing-size-converter.html` : `服装尺码换算适合哪些场景？` : dead
- `tools/life/color-name-finder.html` : `如何使用颜色名称查询？` : dead
- `tools/life/color-name-finder.html` : `颜色名称查询是做什么的？` : dead
- `tools/life/color-name-finder.html` : `颜色名称查询适合哪些场景？` : dead
- `tools/life/concentration-converter.html` : `如何使用浓度换算？` : dead
- `tools/life/concentration-converter.html` : `浓度换算是做什么的？` : dead
- `tools/life/concentration-converter.html` : `浓度换算适合哪些场景？` : dead
- `tools/life/countdown.html` : `倒计时器（设置日期）是做什么的？` : dead
- `tools/life/countdown.html` : `倒计时器（设置日期）适合哪些场景？` : dead
- `tools/life/countdown.html` : `如何使用倒计时器（设置日期）？` : dead
- `tools/life/countdown-1.html` : `如何使用计时器（正计时/倒计时）？` : dead
- `tools/life/countdown-1.html` : `计时器（正计时/倒计时）是做什么的？` : dead
- `tools/life/countdown-1.html` : `计时器（正计时/倒计时）适合哪些场景？` : dead
- `tools/life/countdown-2.html` : `如何使用纪念日倒计时（多组）？` : dead
- `tools/life/countdown-2.html` : `纪念日倒计时（多组）是做什么的？` : dead
- `tools/life/countdown-2.html` : `纪念日倒计时（多组）适合哪些场景？` : dead
- `tools/life/countdown-timer.html` : `多功能倒计时器是做什么的？` : dead
- `tools/life/countdown-timer.html` : `多功能倒计时器适合哪些场景？` : dead
- `tools/life/countdown-timer.html` : `如何使用多功能倒计时器？` : dead
- `tools/life/cycle-4.html` : `如何使用清洁用品消耗量与补货周期？` : dead
- `tools/life/cycle-4.html` : `清洁用品消耗量与补货周期是做什么的？` : dead
- `tools/life/cycle-4.html` : `清洁用品消耗量与补货周期适合哪些场景？` : dead
- `tools/life/cycle-pruning-lawn.html` : `如何使用草坪（修剪/养护）周期？` : dead
- `tools/life/cycle-pruning-lawn.html` : `景观（风水/视线）分析` : dead
- `tools/life/cycle-pruning-lawn.html` : `草坪（修剪/养护）周期是做什么的？` : dead
- `tools/life/cycle-pruning-lawn.html` : `草坪（修剪/养护）周期适合哪些场景？` : dead
- `tools/life/daily-calorie-needs.html` : `体脂率改用 Deurenberg 公式（男 1.20×BMI + 0.23×年龄 − 16.2；女 1.20×BMI + 0.23×年龄 − 5.4），限 2%–60%` : dead
- `tools/life/daily-calorie-needs.html` : `卡路里计算器是做什么的？` : dead
- `tools/life/daily-calorie-needs.html` : `卡路里计算器适合哪些场景？` : dead
- `tools/life/daily-calorie-needs.html` : `如何使用卡路里计算器？` : dead
- `tools/life/daily-calorie-needs.html` : `默认 Mifflin-St Jeor 公式，另可选 Harris-Benedict（男 66.5+13.75W+5.003H−6.755A）与 Katch-McArdle（370+21.6×去脂体重，体脂率用 Deurenberg Formula:男 1.20×BMI+0.23×年龄−16.2、女 1.20×BMI+0…(+60字)` : dead
- `tools/life/daily-calorie-needs.html` : `默认 Mifflin-St Jeor 公式，另可选 Harris-Benedict（男 66.5+13.75W+5.003H−6.755A）与 Katch-McArdle（370+21.6×去脂体重，先用 BMI 估算体脂率）。每日目标摄入 = TDEE + 目标差额（减脂/维持/增肌），数值为估算参考。` : dead
- `tools/life/data-rate-converter.html` : `如何使用数据速率换算？` : dead
- `tools/life/data-rate-converter.html` : `数据速率换算是做什么的？` : dead
- `tools/life/data-rate-converter.html` : `数据速率换算适合哪些场景？` : dead
- `tools/life/data-unit-converter.html` : `如何使用数据存储单位换算？` : dead
- `tools/life/data-unit-converter.html` : `数据存储单位换算是做什么的？` : dead
- `tools/life/data-unit-converter.html` : `数据存储单位换算适合哪些场景？` : dead
- `tools/life/date-add-subtract.html` : `如何使用日期加减？` : dead
- `tools/life/date-add-subtract.html` : `日/时/分/秒按时间戳精确加减` : dead
- `tools/life/date-add-subtract.html` : `日期加减是做什么的？` : dead
- `tools/life/date-add-subtract.html` : `日期加减适合哪些场景？` : dead
- `tools/life/date-add-subtract.html` : `目标日期 = 基准日期 + 年、月、日、时、分、秒增量（负数表示减）；先加年月并处理月末溢出（如 1 月 31 日加 1 月取 2 月末），再累加天数自动跨月跨年，最后按秒数补时分秒；闰年 2 月为 29 天须在跨月时校正。` : dead
- `tools/life/date-diff.html` : `如何使用日期差计算？` : dead
- `tools/life/date-diff.html` : `日期差计算是做什么的？` : dead
- `tools/life/date-diff.html` : `日期差计算适合哪些场景？` : dead
- `tools/life/date-difference-calculator.html` : `如何使用日期差计算器？` : dead
- `tools/life/date-difference-calculator.html` : `日期差计算器是做什么的？` : dead
- `tools/life/date-difference-calculator.html` : `日期差计算器适合哪些场景？` : dead
- `tools/life/density-converter.html` : `关于「密度换算器」` : dead
- `tools/life/detector-checker-strength.html` : `如何使用强密码检测器（检查强度）？` : dead
- `tools/life/detector-checker-strength.html` : `密码强度评分 = 长度分（不足 8 位 0 分、8 至 11 位 10 分、12 至 15 位 20 分、16 位及以上 30 分）+ 字符集分（大写 15 分、小写 15 分、数字 15 分、符号 25 分）− 惩罚项（连续或重复字符、弱口令字典命中）；总分 0 至 100 对应很弱至很强五级。` : dead
- `tools/life/detector-checker-strength.html` : `强密码检测器（检查强度）是做什么的？` : dead
- `tools/life/detector-checker-strength.html` : `强密码检测器（检查强度）适合哪些场景？` : dead
- `tools/life/drinking-water-plan.html` : `关于「喝水提醒计划计算器」` : dead
- `tools/life/drinking-water-plan.html` : `喝水提醒计划计算器是做什么的？` : dead
- `tools/life/drinking-water-plan.html` : `喝水提醒计划计算器适合哪些场景？` : dead
- `tools/life/drinking-water-plan.html` : `如何使用喝水提醒计划计算器？` : dead
- `tools/life/drinking-water-plan.html` : `饮水目标 = 体重×30ml + 运动增量 + 高温增量 + 特殊增量` : dead
- `tools/life/energy-converter.html` : `如何使用能量换算？` : dead
- `tools/life/energy-converter.html` : `能量换算是做什么的？` : dead
- `tools/life/energy-converter.html` : `能量换算适合哪些场景？` : dead
- `tools/life/event-countdown.html` : `如何使用节日倒计时？` : dead
- `tools/life/event-countdown.html` : `节日倒计时是做什么的？` : dead
- `tools/life/event-countdown.html` : `节日倒计时适合哪些场景？` : dead
- `tools/life/flow-rate-converter.html` : `如何使用流量换算？` : dead
- `tools/life/flow-rate-converter.html` : `流量换算是做什么的？` : dead
- `tools/life/flow-rate-converter.html` : `流量换算适合哪些场景？` : dead
- `tools/life/frequency-converter.html` : `如何使用频率换算？` : dead
- `tools/life/frequency-converter.html` : `频率换算是做什么的？` : dead
- `tools/life/frequency-converter.html` : `频率换算适合哪些场景？` : dead
- `tools/life/generator-price.html` : `合同（服务/价格/条款）生成是做什么的？` : dead
- `tools/life/generator-price.html` : `合同（服务/价格/条款）生成适合哪些场景？` : dead
- `tools/life/generator-price.html` : `如何使用合同（服务/价格/条款）生成？` : dead
- `tools/life/generator-random-1.html` : `如何使用随机数生成器（范围任意）？` : dead
- `tools/life/generator-random-1.html` : `随机数生成器（范围任意）是做什么的？` : dead
- `tools/life/generator-random-1.html` : `随机数生成器（范围任意）适合哪些场景？` : dead
- `tools/life/generator-strength.html` : `如何使用密码生成器（带强度检测）？` : dead
- `tools/life/generator-strength.html` : `字符种类统计小写/大写/数字/符号四类中出现的种数。并设上限修正：长度 <8 位分数封顶 30、<6 位封顶 15、仅含一类字符封顶 25。按总分分档：<30 弱、<55 中、<80 强、其余很强。字符池由勾选项决定，可进一步排除相似字符 0O1lI 与歧义字符。` : dead
- `tools/life/generator-strength.html` : `密码生成器（带强度检测）是做什么的？` : dead
- `tools/life/generator-strength.html` : `密码生成器（带强度检测）适合哪些场景？` : dead
- `tools/life/holiday-calendar.html` : `关于「节假日日历」` : dead
- `tools/life/holiday-calendar.html` : `如何使用节假日日历？` : dead
- `tools/life/holiday-calendar.html` : `节假日日历是做什么的？` : dead
- `tools/life/holiday-calendar.html` : `节假日日历适合哪些场景？` : dead
- `tools/life/leap-year-checker.html` : `如何使用闰年检查器？` : dead
- `tools/life/leap-year-checker.html` : `闰年检查器是做什么的？` : dead
- `tools/life/leap-year-checker.html` : `闰年检查器适合哪些场景？` : dead
- `tools/life/length-converter.html` : `关于「长度换算器」` : dead
- `tools/life/length-converter.html` : `目标单位：` : dead
- `tools/life/magnet-converter.html` : `关于「磁场强度换算器」` : dead
- `tools/life/music-practice-timer.html` : `如何使用音乐练习计时器？` : dead
- `tools/life/music-practice-timer.html` : `音乐练习计时器是做什么的？` : dead
- `tools/life/music-practice-timer.html` : `音乐练习计时器适合哪些场景？` : dead
- `tools/life/number-to-chinese.html` : `→ 一十` : dead
- `tools/life/number-to-chinese.html` : `如何使用数字转中文？` : dead
- `tools/life/number-to-chinese.html` : `数字转中文是做什么的？` : dead
- `tools/life/number-to-chinese.html` : `数字转中文适合哪些场景？` : dead
- `tools/life/parking-fee.html` : `停车费 = 计费时长 × 每小时费率，计费时长 = 停放时长 − 免费时长（不足 1 小时按 1 小时计或按分钟折算）；每日封顶时按自然日分组取较小值（当日费用与封顶价）后累加；跨日停放逐日分别计费再求和。` : dead
- `tools/life/parking-fee.html` : `停车费计算器是做什么的？` : dead
- `tools/life/parking-fee.html` : `停车费计算器适合哪些场景？` : dead
- `tools/life/parking-fee.html` : `免费时长（小时）` : dead
- `tools/life/parking-fee.html` : `关于「停车费计算器」` : dead
- `tools/life/parking-fee.html` : `如何使用停车费计算器？` : dead
- `tools/life/percentage-calculator.html` : `如何使用百分比计算器？` : dead
- `tools/life/percentage-calculator.html` : `百分比计算器是做什么的？` : dead
- `tools/life/percentage-calculator.html` : `百分比计算器适合哪些场景？` : dead
- `tools/life/phone-lookup.html` : `归一化去空格 / 连字符 / 括号 / 点；带 + 时按国家码库 3→1 位前缀匹配；不带 + 时：^1[3-9]\d{9}$ 推断中国大陆手机（第 4 位映射运营商），^0\d{10,11}$ 判固话（010 / 02x 取 2 位区号，其余按 3–4 位区号匹配号段表，绝不把号码首位并入区号）` : dead
- `tools/life/power-converter.html` : `关于「功率换算器」` : dead
- `tools/life/power-converter.html` : `功率换算器是做什么的？` : dead
- `tools/life/power-converter.html` : `功率换算器适合哪些场景？` : dead
- `tools/life/power-converter.html` : `如何使用功率换算器？` : dead
- `tools/life/pressure-converter.html` : `关于「压力换算器」` : dead
- `tools/life/pressure-converter.html` : `压力换算器是做什么的？` : dead
- `tools/life/pressure-converter.html` : `压力换算器适合哪些场景？` : dead
- `tools/life/pressure-converter.html` : `如何使用压力换算器？` : dead
- `tools/life/radiation-converter.html` : `关于「辐射剂量换算器」` : dead
- `tools/life/recommender-8.html` : `保险（责任/意外/雇主）推荐是做什么的？` : dead
- `tools/life/recommender-8.html` : `保险（责任/意外/雇主）推荐适合哪些场景？` : dead
- `tools/life/recommender-8.html` : `如何使用保险（责任/意外/雇主）推荐？` : dead
- `tools/life/reminder-cycle.html` : `如何使用家电深度清洁周期提醒？` : dead
- `tools/life/reminder-cycle.html` : `家电深度清洁周期提醒是做什么的？` : dead
- `tools/life/reminder-cycle.html` : `家电深度清洁周期提醒适合哪些场景？` : dead
- `tools/life/report-profit.html` : `如何使用财务（利润/现金流/报表）核算？` : dead
- `tools/life/report-profit.html` : `财务（利润/现金流/报表）核算是做什么的？` : dead
- `tools/life/report-profit.html` : `财务（利润/现金流/报表）核算适合哪些场景？` : dead
- `tools/life/ring-size-converter.html` : ` mm（直径 ` : dead
- `tools/life/ring-size-converter.html` : `中国港码：` : dead
- `tools/life/ring-size-converter.html` : `关于「戒指尺寸换算器」` : dead
- `tools/life/ring-size-converter.html` : `周长(mm)：` : dead
- `tools/life/ring-size-converter.html` : `如何使用戒指尺寸换算器？` : dead
- `tools/life/ring-size-converter.html` : `意码：` : dead
- `tools/life/ring-size-converter.html` : `戒指尺寸换算器是做什么的？` : dead
- `tools/life/ring-size-converter.html` : `戒指尺寸换算器适合哪些场景？` : dead
- `tools/life/ring-size-converter.html` : `欧码：` : dead
- `tools/life/ring-size-converter.html` : `直径(mm)：` : dead
- `tools/life/ring-size-converter.html` : `美码：` : dead
- `tools/life/ring-size-converter.html` : `英码：` : dead
- `tools/life/roman-numeral.html` : `如何使用罗马数字转换？` : dead
- `tools/life/roman-numeral.html` : `罗马数字转换是做什么的？` : dead
- `tools/life/roman-numeral.html` : `罗马数字转换适合哪些场景？` : dead
- `tools/life/shoe-size-converter.html` : `中国码 CN = 脚长 mm / 10 （如 250mm → 25）` : dead
- `tools/life/shoe-size-converter.html` : `关于「鞋码换算器」` : dead
- `tools/life/shoe-size-converter.html` : `如何使用鞋码换算器？` : dead
- `tools/life/shoe-size-converter.html` : `欧盟码 EU ≈ 1.5 × (脚长 cm + 2)（如 25cm → 41）` : dead
- `tools/life/shoe-size-converter.html` : `注：各品牌存在 0.5-1 码差异，建议以品牌对照表为准` : dead
- `tools/life/shoe-size-converter.html` : `美码女 US ≈ 0.847 × 脚长 cm - 18.4` : dead
- `tools/life/shoe-size-converter.html` : `美码男 US ≈ 0.847 × 脚长 cm - 17.6（约 7-12 常见）` : dead
- `tools/life/shoe-size-converter.html` : `英码 UK ≈ 美码男 - 1` : dead
- `tools/life/shoe-size-converter.html` : `鞋码按脚长换算：中国码 CN = 脚长(mm) ÷ 10（250 mm 对应 CN 250 即 40 码）；欧洲码 EU ≈ 脚长(cm) × 1.5 + 2；美国码与英国码在欧码基础上按性别减约 33 至 34（EU 40 约合 US 男 7 号、女 8.5 号）；建议以脚跟至最长脚趾的实测长度选码并预留 5 至 1…(+5字)` : dead
- `tools/life/shoe-size-converter.html` : `鞋码换算器是做什么的？` : dead
- `tools/life/shoe-size-converter.html` : `鞋码换算器适合哪些场景？` : dead
- `tools/life/speed-converter.html` : `关于「速度换算器」` : dead
- `tools/life/speed-converter.html` : `如何使用速度换算器？` : dead
- `tools/life/speed-converter.html` : `速度换算器是做什么的？` : dead
- `tools/life/speed-converter.html` : `速度换算器适合哪些场景？` : dead
- `tools/life/stats-13.html` : `如何使用预售（发布/接龙/统计）工具？` : dead
- `tools/life/stats-13.html` : `库存与发车预备` : dead
- `tools/life/stats-13.html` : `报名付款聚合` : dead
- `tools/life/stats-13.html` : `时段峰值识别` : dead
- `tools/life/stats-13.html` : `聚合报名、付款与时段分布，输出转化漏斗与参与结构，辅助活动节奏与备货。` : dead
- `tools/life/stats-13.html` : `转化流失定位` : dead
- `tools/life/stats-13.html` : `转化漏斗分层` : dead
- `tools/life/stats-13.html` : `预售报名统计` : dead
- `tools/life/stats-13.html` : `预售（发布/接龙/统计）工具是做什么的？` : dead
- `tools/life/stats-13.html` : `预售（发布/接龙/统计）工具适合哪些场景？` : dead
- `tools/life/temperature-converter.html` : `如何使用温度转换器？` : dead
- `tools/life/temperature-converter.html` : `温度转换器是做什么的？` : dead
- `tools/life/temperature-converter.html` : `温度转换器适合哪些场景？` : dead
- `tools/life/time-converter.html` : `关于「时间换算器」` : dead
- `tools/life/time-converter.html` : `如何使用时间换算器？` : dead
- `tools/life/time-converter.html` : `时间换算器是做什么的？` : dead
- `tools/life/time-converter.html` : `时间换算器适合哪些场景？` : dead
- `tools/life/unit-converter.html` : `结果 = 数值 × 源单位因子 ÷ 目标单位因子（温度走专用换算）` : dead
- `tools/life/volume-converter.html` : `关于「体积换算器」` : dead
- `tools/life/weight-converter.html` : `关于「重量换算器」` : dead
- `tools/life/weight-converter.html` : `如何使用重量换算器？` : dead
- `tools/life/weight-converter.html` : `重量换算器是做什么的？` : dead
- `tools/life/weight-converter.html` : `重量换算器适合哪些场景？` : dead
- `tools/life/workday-calculator.html` : `含起始日，不含结束日（如周一到周五 = 5 个工作日）` : dead
- `tools/life/workday-calculator.html` : `如何使用工作日计算器？` : dead
- `tools/life/workday-calculator.html` : `工作日数 = 区间总天数 − 周末天数 − 自定义节假日天数（按选项决定是否排除周六、周日）；总天数 =（结束日期 − 开始日期）÷ 86400000 + 1（含首尾两天）；逐日遍历统计可识别调休与自定义假日，用于工期与考勤估算。` : dead
- `tools/life/workday-calculator.html` : `工作日计算器是做什么的？` : dead
- `tools/life/workday-calculator.html` : `工作日计算器适合哪些场景？` : dead
- `tools/life/workday-calculator.html` : `自定义节假日：列出法定调休日（如国庆、春节假期）` : dead
- `tools/life/workday-calculator.html` : `自定义额外节假日（每行一个日期，格式 YYYY-MM-DD）` : dead
- `tools/life/workday-calculator.html` : `若需要调休上班（周末补班），请取消对应周末的勾选` : dead
- `tools/life/world-clock.html` : `世界时钟是做什么的？` : dead
- `tools/life/world-clock.html` : `世界时钟适合哪些场景？` : dead
- `tools/life/world-clock.html` : `如何使用世界时钟？` : dead
- `tools/life/zodiac-calculator.html` : `Note:本工具按公历年份估算，1-2 月初出生者可能需按农历调整` : dead
- `tools/life/zodiac-calculator.html` : `如何使用生肖星座计算？` : dead
- `tools/life/zodiac-calculator.html` : `生肖星座计算是做什么的？` : dead
- `tools/life/zodiac-calculator.html` : `生肖星座计算适合哪些场景？` : dead

  其它成因样例（共 79 条，仅列前 5）：
  - `tools/life/age-in-days.html` : `请输入有效日期（YYYY-MM-DD）` : dynamic
  - `tools/life/age-in-days.html` : `距离下一个生日：` : dynamic
  - `tools/life/age-in-days.html` : `天` : fragment
  - `tools/life/age-in-days.html` : `（今天）` : dynamic
  - `tools/life/age-in-days.html` : `出生日期不能晚于今天` : dynamic

### livestock（dead 5 / dynamic 15 / fragment 6 / harmless 0）

- `tools/livestock/ammonia-ventilation.html` : `c2 由 15 降至 10 ppm：Q 增到约 110 次/分。` : dead
- `tools/livestock/ammonia-ventilation.html` : `舍容 1800 m³（50×12×3），η=0.6：Q=V·ln(c1/c2)/(t·η)=1800×ln(40/15)/0.6≈2943 m³/s，换气约 98 次/分。` : dead
- `tools/livestock/analysis-18.html` : `料蛋比 = 耗料总量 ÷ 产蛋总重` : dead
- `tools/livestock/mycotoxin-limit.html` : `本工具仔猪料 ZEA 限量按 250 μg/kg 计，实测 150 为限量的 60%，判合格；若按更严格的地方/企业标准（如 100 μg/kg）则应判超标，实际判定请以现行 GB 13078 与当地法规为准。` : dead
- `tools/livestock/stats-7.html` : `需助产率 = (轻度助产 + 难产) ÷ 产犊总数 × 100%` : dead

  其它成因样例（共 21 条，仅列前 5）：
  - `tools/livestock/ammonia-ventilation.html` : `维持通风量(m³/h)` : dynamic
  - `tools/livestock/ammonia-ventilation.html` : `维持通风量(产氨)` : dynamic
  - `tools/livestock/analysis-18.html` : `产蛋率 = 产蛋总数 ÷ (存栏鸡数 × 统计天数) × 100%` : fragment
  - `tools/livestock/calving-interval.html` : `请输入有效的上次产犊日期` : dynamic
  - `tools/livestock/calving-interval.html` : `请输入有效的配种日期` : dynamic

### logistics（dead 3 / dynamic 0 / fragment 0 / harmless 0）

- `tools/logistics/checker-4.html` : `≥90% 流程完善，75-89% 基本完善，60-74% 待改进，<60% 需重建` : dead
- `tools/logistics/load-calculator.html` : `利用率 <70% 提示调整包装尺寸；输入箱尺寸格式 L×W×H` : dead
- `tools/logistics/load-calculator.html` : `限制因素 = 体积实际箱数 < 重量限制箱数 时取体积，否则重量` : dead

### logistics2（dead 4 / dynamic 10 / fragment 8 / harmless 0）

- `tools/logistics2/loading-utilization.html` : `为什么枚举 6 种摆放取向？` : dead
- `tools/logistics2/loading-utilization.html` : `最大可装件数（体积侧）：对 6 种正交摆放取向（长宽高三边全排列）分别计算 floor(车厢长÷第一边)×floor(车厢宽÷第二边)×floor(车厢高÷第三边)，取六者最大值作为体积上限。` : dead
- `tools/logistics2/loading-utilization.html` : `输入：车厢 6.8×2.3×2.4 m（容积 37.536 m³）、载重 5000 kg；纸箱 0.6×0.4×0.5 m（单件 0.12 m³）、单件 15 kg；计划 500 件。六种取向：(0.6,0.4,0.5)→11×5×4=220 件、(0.6,0.5,0.4)→11×4×5=220 件、(0.4,0.6,…(+330字)` : dead
- `tools/logistics2/loading-utilization.html` : `长方体正交摆放有 6 种三边分配方式，全部枚举后取最大值，避免只试 3 种时低估可装件数（例如把较长边放到车厢长度方向反而能多装）。若货物不允许倒置（如带向上标识的箱体），可手工剔除把原高边转到竖直方向的取向。` : dead

  其它成因样例（共 18 条，仅列前 5）：
  - `tools/logistics2/storage-allocation.html` : `合计` : fragment
  - `tools/logistics2/storage-allocation.html` : `A 类` : fragment
  - `tools/logistics2/storage-allocation.html` : `B 类` : fragment
  - `tools/logistics2/storage-allocation.html` : `C 类` : fragment
  - `tools/logistics2/storage-allocation.html` : `合计校验：` : dynamic

### machinery（dead 47 / dynamic 127 / fragment 9 / harmless 6）

- `tools/machinery/area-dosage-1.html` : `涂装用量 = 面积 × 膜厚 × 密度` : dead
- `tools/machinery/banjinzhewanzhankai.html` : `展开长度 = 中性层 + 折弯补偿` : dead
- `tools/machinery/banjinzhewanzhankai.html` : `当 R/t < 0.5 时可能产生裂纹，应增大内圆角半径` : dead
- `tools/machinery/banjinzhewanzhankai.html` : `翼缘长度 A、B 为从外边到切点的距离，留 0 可仅计算弯角参数` : dead
- `tools/machinery/bearing.html` : `轴承补油/换油周期依据 dn 值（d×n）与润滑方式估算` : dead
- `tools/machinery/calc-64.html` : `装配间隙/过盈 = 公差配合` : dead
- `tools/machinery/calc-89.html` : `离合器转矩 T = μ·F·R·Z` : dead
- `tools/machinery/calc-gear.html` : `标准齿轮 d = m·z` : dead
- `tools/machinery/calc-gear-1.html` : `齿轮模数 m = d/z` : dead
- `tools/machinery/calc-gear-3.html` : `齿轮参数 = 标准模数系列` : dead
- `tools/machinery/calc-lifespan-belt.html` : `皮带寿命 = f(张力, 转速)` : dead
- `tools/machinery/calc-strength.html` : `轴强度 σ = M/W` : dead
- `tools/machinery/drive-2.html` : `蜗杆效率 η = tanλ/tan(λ+ρ)` : dead
- `tools/machinery/energy-2.html` : `制动能耗 = ½J(ω₁² − ω₂²)` : dead
- `tools/machinery/estimate-gravity.html` : `重心 = Σ(m_i·x_i)/Σm_i` : dead
- `tools/machinery/fengjixuanxingjisuan.html` : `风量 Q (m³/h)、全压 p (Pa) 定工况；选型匹配性能曲线` : dead
- `tools/machinery/gear.html` : `齿轮设计 = 强度/几何计算` : dead
- `tools/machinery/gongyebengxuanxing.html` : `安装校核：高扬程注意汽蚀余量 NPSH` : dead
- `tools/machinery/gongyebengxuanxing.html` : `污染` : dead
- `tools/machinery/gongyebengxuanxing.html` : `汽蚀余量评估与转速推荐` : dead
- `tools/machinery/index.html` : `机械制造工具集合收录了 35 个免费在线工具，覆盖机械制造场景下的常见计算、换算与查询需求。无论你是相关领域的从业者、学生还是普通用户，都能在这里找到即用即走的实用小工具。所有工具纯前端运行，数据不上传服务器，保护隐私安全。` : dead
- `tools/machinery/jingmishebeixuanxing.html` : `依据定位精度、负载、行程、移动速度选直线导轨(HGR)与滚珠丝杠` : dead
- `tools/machinery/lifespan-20.html` : `L₁₀ = (C/P)^p（ISO 281），并计精度因子与润滑因子` : dead
- `tools/machinery/lifespan-bearing.html` : `轴承寿命 L10 = (C/P)^p` : dead
- `tools/machinery/lifespan-bearing-1.html` : `轴承额定动载 C = f(寿命, 转速)` : dead
- `tools/machinery/power-16.html` : `依据传递功率 P、主动轮转速 n₁ 与传动比 i 选带型与带轮直径` : dead
- `tools/machinery/power-voltage.html` : `P = F · v / η；推荐标准电机功率等级与极数` : dead
- `tools/machinery/pressure-4.html` : `花键挤压 σ = F/(d·l·z)` : dead
- `tools/machinery/pressure-flow-4.html` : `比功率 = 轴功率 ÷ 排气量；能效对照 GB 19153` : dead
- `tools/machinery/pressure-flow-5.html` : `Cv = Q × √(ρ/ΔP) × 换算系数；口径按 Cv 选标准通径` : dead
- `tools/machinery/runhuaxitongsheji.html` : `润滑油量 = f(功率, 转速)` : dead
- `tools/machinery/shusongdaixuanxingjisuan.html` : `带宽 ≈ Q ÷ (ρ × 带速 × 填充系数)，向上取整至标准规格` : dead
- `tools/machinery/strength-15.html` : `链条拉力 = 功率/速度` : dead
- `tools/machinery/strength-6.html` : `键强度 = 挤压/剪切校核` : dead
- `tools/machinery/strength-7.html` : `铆接剪切 τ = F/(n·πd²/4)` : dead
- `tools/machinery/stretch.html` : `弹簧刚度 k = G·d⁴/(8D³n)` : dead
- `tools/machinery/tanhuangsheji.html` : `弹簧设计 k = G·d⁴/(8D³n)` : dead
- `tools/machinery/temp-hardness.html` : `热处理硬度 = f(温度, 冷却)` : dead
- `tools/machinery/thread-4.html` : `H = 0.866×P（理论）；H₁ ≈ 0.5413×P（实际牙高）` : dead
- `tools/machinery/thread-recognize.html` : `60° 公制三角螺纹理论牙型，中径 = 大径 − 2×(H/2 在轴向投影)，几何推导得此式（H 为理论牙高）。` : dead
- `tools/machinery/thread-recognize.html` : `中径为何用 0.75H·cos(α/2)？` : dead
- `tools/machinery/thread-recognize.html` : `外径≈10、螺距 1.5、牙型角 60°：H=p/(2·tan30°)=1.5/1.1547≈1.299 mm；d2=10−0.75×1.299×cos30°=10−0.843≈9.157 mm；d1=10−1.0825×1.5≈8.376 mm。匹配标准 M10×1.5。` : dead
- `tools/machinery/thread-recognize.html` : `螺纹识别 = 参数查表` : dead
- `tools/machinery/tolerance.html` : `配合公差 = 孔轴偏差` : dead
- `tools/machinery/tolerance-1.html` : `几何公差 = 标注查表` : dead
- `tools/machinery/torque.html` : `T = K × F × d（扭矩系数法）；F = 预紧比例 × σs × As` : dead
- `tools/machinery/xiao-dingwei-lianjie-chicun.html` : `销钉直径 d = √(4F ÷ (π·τ))；F 为传递力，τ 为许用剪应力` : dead

  其它成因样例（共 142 条，仅列前 5）：
  - `tools/machinery/analysis-lifespan.html` : `MTBF = 总运行时间 ÷ 故障次数` : fragment
  - `tools/machinery/analysis-lifespan.html` : `可靠度 R(t) = e^(−t ÷ MTBF)` : fragment
  - `tools/machinery/banjinzhewanzhankai.html` : `请输入有效参数（板厚须大于 0，角度须在 0°–180° 之间且不含端点，K 因子 0~1）` : dynamic
  - `tools/machinery/banjinzhewanzhankai.html` : `折弯角 0~180°（不含端点，180° 时 tan(θ/2) 发散）` : fragment
  - `tools/machinery/banjinzhewanzhankai.html` : `⚠ 翼缘 A/B 小于外截退量 OSSB，几何上无法按该公式展开，展开总长暂不显示；请核对测量口径（应为外边到虚拟尖角交叉点）。` : dynamic

### manufacturing（dead 10 / dynamic 6 / fragment 0 / harmless 0）

- `tools/manufacturing/capacity-planning.html` : `产能富余,可减少 台设备或增加订单` : dead
- `tools/manufacturing/capacity-planning.html` : `请输入有效参数：设备数与每日班次须为正整数，单台班产能>0，需求>0，每月工作日为 1–31 的整数。` : dead
- `tools/manufacturing/defect-rate.html` : `CPK 粗算 = (σ − 3) × 2 ÷ 3` : dead
- `tools/manufacturing/defect-rate.html` : `DPMO 指每百万次机会中的缺陷数，西格玛水平由 DPMO 查表换算：约 66807→3σ、6210→3.5σ、233→4σ、3.4→5σ、0.002→6σ。数值越高过程越稳定，行业通常目标 ≥4σ（约 DPMO≤6210）。` : dead
- `tools/manufacturing/defect-rate.html` : `某装配线投入 50000 件、检出不良 250 件、共 2 道工序。不良率 = 250÷50000 = 0.5%；单工序直通率 = 1−0.5% = 99.5%；滚动直通率 RTY = 0.995² ≈ 99.00%；PPM = 0.5%×10⁶ = 5000；DPMO = 5000÷2 = 2500；查表得西格玛水平…(+51字)` : dead
- `tools/manufacturing/defect-rate.html` : `核心计算公式（按输入变量）：max(0, (sigma - 3) × 2 ÷ 3)；(d ÷ t) × 1000000 ÷ p；(d ÷ t) × 1000000` : dead
- `tools/manufacturing/defect-rate.html` : `西格玛水平 = DPMO 反查标准表（含 1.5σ 漂移，3.4→6σ、233→5σ、6210→4σ、66807→3σ）<br>短期等效 CPK = 西格玛水平 ÷ 3<br>等级：<3σ 行业平均｜3~4σ 良好｜4~5σ 优秀｜≥5σ 卓越<br>输入校验：投入>0、不良数 ≤ 投入数` : dead
- `tools/manufacturing/defect-rate.html` : `西格玛水平 = DPMO 反查正态分位（含 1.5σ 漂移）` : dead
- `tools/manufacturing/production-efficiency.html` : `核心计算公式（按输入变量）：(1 - min(performance,1)) × 100；min(O ÷ idealCount, 1.5)；(runTime × 60) ÷ CT` : dead
- `tools/manufacturing/quality-control.html` : `样本数 n<30，长期能力估计参考性有限` : dead

  其它成因样例（共 6 条，仅列前 5）：
  - `tools/manufacturing/capacity-planning.html` : `完成订单所需设备` : dynamic
  - `tools/manufacturing/capacity-planning.html` : `总设备日需求` : dynamic
  - `tools/manufacturing/capacity-planning.html` : `本工序产能缺口` : dynamic
  - `tools/manufacturing/defect-rate.html` : `⚠ 输入无效：投入数量与工序数须为正整数，不良数量须为 0 到投入数量之间的整数。` : dynamic
  - `tools/manufacturing/quality-control.html` : `长期标准差须大于 0（留空则不计算 PPK）` : dynamic

### maritime（dead 4 / dynamic 1 / fragment 0 / harmless 0）

- `tools/maritime/stowage-factor.html` : `请检查输入：积载因数、船舶舱容与载重吨需为 >0 的数值，总货量需为 ≥0 的数值。` : dead
- `tools/maritime/stowage-factor.html` : `请检查输入：货物体积与货物重量均需为 >0 的数值。` : dead
- `tools/maritime/stowage-factor.html` : `货物分类：SF <0.6 重货（载重受限）｜<1.3 中等｜<2.0 轻货（舱容受限）｜≥2.0 极轻` : dead
- `tools/maritime/tide-window.html` : `Mean = (高潮潮高+低潮潮高)÷2；振幅 = (高潮潮高−低潮潮高)÷2` : dead

  其它成因样例（共 1 条，仅列前 5）：
  - `tools/maritime/tide-window.html` : `⚠ 输入无效：潮高、水深、吃水与 UKC 不得为负，通航所需时间须大于 0。` : dynamic

### marketing（dead 19 / dynamic 59 / fragment 2 / harmless 0）

- `tools/marketing/ad-roi.html` : `广告 ROI 模拟：CPC 模式 点击数=预算÷CPC、展示=点击÷CTR；CPM 模式 展示=预算÷CPM×1000、点击=展示×CTR。收入=点击×CVR×客单价，毛利=收入×(1−成本率)−固定成本，ROI=毛利÷预算。调整出价 / CTR / CVR 即可比较不同投放方案盈亏。` : dead
- `tools/marketing/ad-roi.html` : `盈亏平衡 ROAS = 1 ÷ 毛利率。毛利率 40% 时只要 ROAS≥1.67 就不亏，低于则必亏。` : dead
- `tools/marketing/ad-roi.html` : `若利润为负，公式给出：转化率需提升到 预算/(客单价×点击量)，或客单价提升到 预算/(点击量×转化率)。例如点击 5000、客单价 300、预算 10000 → 转化率需达 10000/(300×5000)=0.67% 才保本。` : dead
- `tools/marketing/calc-price-elasticity.html` : `价格 +10%、销量仅 −3% → E=−0.3 缺乏弹性，总收入由 100000 升到 113300 元，适合小幅提价。` : dead
- `tools/marketing/calc-price-elasticity.html` : `弧弹性（中点法）：需求变化率=(q2−q1)/[(q1+q2)/2]，价格变化率=(p2−p1)/[(p1+p2)/2]，Ed=需求变化率÷价格变化率（带符号）。|Ed|>1 富有弹性、<1 缺乏弹性；收入变化率=(p2×q2−p1×q1)/(p1×q1)，用于判断调价方向。` : dead
- `tools/marketing/marketing-coupon-discount.html` : `最终价格 = (原价 × 折扣率 - 优惠券) × 数量` : dead
- `tools/marketing/marketing-coupon-discount.html` : `注意：需先判断是否满足优惠券使用条件。` : dead
- `tools/marketing/marketing-coupon-discount.html` : `注意：需先判断是否满足优惠券使用条件；<strong>门槛按折前总额（原价×数量）判断，不按折后金额</strong>，且本页只支持「先折扣、后减券」一张券，多券叠加需按活动规则另算。` : dead
- `tools/marketing/marketing-coupon-discount.html` : `注意：需先判断是否满足优惠券使用条件；门槛按折前总额（原价×数量）判断，不按折后金额，且本页只支持「先折扣、后减券」一张券，多券叠加需按活动规则另算。` : dead
- `tools/marketing/marketing-free-shipping-threshold.html` : `免邮门槛评估：距免邮差额 = max(0, 门槛 − 购物车)；加购至免邮的净收益 =（门槛 − 购物车）× 平均毛利率 − 运费，正值提示加购划算。` : dead
- `tools/marketing/marketing-price-elasticity.html` : `价格 +10%、销量仅 −3% → E=−0.3，原收入 100000、新收入 113300，刚需品适合提价。` : dead
- `tools/marketing/marketing-roas-calculator.html` : `「广告费后利润率」= (广告收入 − 广告花费)/广告收入，只扣广告费、未扣货品成本，不是毛利率也不是净利率；真正的盈亏平衡判断要用输入的商品毛利率。` : dead
- `tools/marketing/marketing-roas-calculator.html` : `不等于毛利率/净利率` : dead
- `tools/marketing/marketing-roas-calculator.html` : `广告费后利润=10000、占收入 50%（未扣货品成本，` : dead
- `tools/marketing/marketing-roas-calculator.html` : `盈亏平衡ROAS（毛利为负，无平衡点）` : dead
- `tools/marketing/marketing-roas-calculator.html` : `（毛利率为扣货品成本口径，如 40% ⇒ 2.50x）。` : dead
- `tools/marketing/marketing-roas-calculator.html` : `）；盈亏平衡 ROAS = 1/` : dead
- `tools/marketing/marketing-roi.html` : `净利润` : dead
- `tools/marketing/price-elasticity.html` : `中点法弧弹性 Ed=(ΔQ/均价Q)÷(ΔP/均价P)。|Ed|>1 富有弹性（降价增收入）、<1 缺乏弹性（涨价增收入）、≈1 单位弹性。结果带符号，负号表示价格上升需求下降，符合常规需求规律。` : dead

  其它成因样例（共 61 条，仅列前 5）：
  - `tools/marketing/ad-roi.html` : `当前货品成本率 ≥ 100%（毛利率 ≤ 0），任何转化率或客单价都无法覆盖货品成本，请先下调货品成本率。` : dynamic
  - `tools/marketing/ad-roi.html` : `货品成本率 ≥ 100%，广告投多少都覆盖不了货品成本` : dynamic
  - `tools/marketing/marketing-ad-budget-allocator.html` : `总预算、分配比例与 ROAS 均须为非负数` : dynamic
  - `tools/marketing/marketing-ad-budget-allocator.html` : `⚠ 输入比例合计 ` : dynamic
  - `tools/marketing/marketing-ad-budget-allocator.html` : `%，与 100% 相差 ` : dynamic

### materials（dead 15 / dynamic 14 / fragment 1 / harmless 3）

- `tools/materials/analysis-cost-profit-2.html` : `Mass（检测/标准/追溯）体系` : dead
- `tools/materials/bulk-modulus-e-nu.html` : `K = E/[3(1−2ν)]。 钢 → 约 166.7 GPa。` : dead
- `tools/materials/detector-40.html` : `Mass（色差/强度/标准）检测` : dead
- `tools/materials/detector-strength-color-diff.html` : `Mass（标准/检测/环保）认证` : dead
- `tools/materials/fourier-conduction.html` : `q = k·A·ΔT/L。 钢 k=50，示例 → 1000 W。` : dead
- `tools/materials/hardness-14.html` : `HRC→HV 查标准换算表（如 HRC30≈HV303）` : dead
- `tools/materials/huanbaonaimopinggu.html` : `B - 良好` : dead
- `tools/materials/huanbaonaimopinggu.html` : `C - 中等` : dead
- `tools/materials/lifespan-25.html` : `Coffin-Manson 公式适用于低周疲劳（Nf < 10⁵）` : dead
- `tools/materials/lifespan-6.html` : `ISO 12944 环境等级：C1(<1.3)、C2(1.3-25)、C3(25-50)、C4(50-80)、C5(80-200) μm/年` : dead
- `tools/materials/naimoxingpinggujisuan.html` : `磨损系数 k ≈ a·μ²（摩擦越大磨损越剧烈的经验简化式）` : dead
- `tools/materials/rule-of-mixtures.html` : `纵向模量（E_c = V_f·E_f + V_m·E_m）` : dead
- `tools/materials/specific-heat-capacity.html` : `C = m·c。 水 m=2kg,c=4200 → 8400 J/K。` : dead
- `tools/materials/thermal-diffusivity.html` : `α = k/(ρ·c)。 钢 ≈ 1.4×10⁻⁵ m²/s。` : dead
- `tools/materials/thermal-resistance.html` : `R_th = L/(k·A)。 示例 → 0.1 K/W。` : dead

  其它成因样例（共 18 条，仅列前 5）：
  - `tools/materials/detector-hardness-lifespan.html` : `8 莫氏` : fragment
  - `tools/materials/huanbaonaimopinggu.html` : `· 综合等级：` : dynamic
  - `tools/materials/lifespan-25.html` : `热应力估算 (MPa)` : dynamic
  - `tools/materials/lifespan-26.html` : `🛠️ 高温蠕变寿命` : harmless
  - `tools/materials/lifespan-26.html` : `绝对温度 (K)` : dynamic

### math（dead 23 / dynamic 37 / fragment 3 / harmless 2）

- `tools/math/calc-2.html` : `比例 a:b = a/b` : dead
- `tools/math/calc-4.html` : `圆面积 A = πr², 周长 C = 2πr` : dead
- `tools/math/calculus-tools.html` : `导数/积分 = 微积运算` : dead
- `tools/math/combination-repetition.html` : `可重复组合 C(n+k−1, k)` : dead
- `tools/math/equation-solver.html` : `一次方程直接求解；二次方程先算判别式 Δ = b² − 4ac，Δ > 0 得两个实根、Δ = 0 得重根、Δ < 0 输出一对共轭复根；三次方程以牛顿法配合区间扫描求全部实根。` : dead
- `tools/math/function-plotter.html` : `输入以 x 为变量的表达式，可用 sin, cos, tan, exp, log, sqrt, abs, pow, PI, E 等。` : dead
- `tools/math/geometric-series-sum.html` : `|r|<1 时数列收敛。` : dead
- `tools/math/geometry-calculator.html` : `面积/体积 = 几何公式` : dead
- `tools/math/index.html` : `数学计算工具集合收录了 36 个免费在线工具，覆盖数学计算场景下的常见计算、换算与查询需求。无论你是相关领域的从业者、学生还是普通用户，都能在这里找到即用即走的实用小工具。所有工具纯前端运行，数据不上传服务器，保护隐私安全。` : dead
- `tools/math/liangshuzhihe-chengjizuida-zuixiao-shuxueti.html` : `一、和定积最大：a + b = 20` : dead
- `tools/math/liangshuzhihe-chengjizuida-zuixiao-shuxueti.html` : `三、代入验算：a = 12，b = 8` : dead
- `tools/math/liangshuzhihe-chengjizuida-zuixiao-shuxueti.html` : `二、积定和最小：a × b = 36` : dead
- `tools/math/liangshuzhihe-chengjizuida-zuixiao-shuxueti.html` : `五、因数对枚举表（a × b = 36）` : dead
- `tools/math/liangshuzhihe-chengjizuida-zuixiao-shuxueti.html` : `取等条件：a = b = 10，此时积取最大值 100。该和下两数恰好都能取整数，正整数解同样取到等号点。` : dead
- `tools/math/liangshuzhihe-chengjizuida-zuixiao-shuxueti.html` : `取等条件：a = b = √P = 6，此时和取最小值 12。√P 为整数，正整数解同样取到等号点。` : dead
- `tools/math/liangshuzhihe-chengjizuida-zuixiao-shuxueti.html` : `四、正整数拆分枚举表（a + b = 20）` : dead
- `tools/math/liangshuzhihe-chengjizuida-zuixiao-shuxueti.html` : `差值 0` : dead
- `tools/math/liangshuzhihe-chengjizuida-zuixiao-shuxueti.html` : `待验算 a×b（a=12，b=8）` : dead
- `tools/math/liangshuzhihe-chengjizuida-zuixiao-shuxueti.html` : `最大积（a+b=20，正整数解）` : dead
- `tools/math/liangshuzhihe-chengjizuida-zuixiao-shuxueti.html` : `最小和（a×b=36，正整数解）` : dead
- `tools/math/liangshuzhihe-chengjizuida-zuixiao-shuxueti.html` : `距最大积 4` : dead
- `tools/math/percent-change.html` : `Δ% = (新−旧)/旧 × 100%` : dead
- `tools/math/quadratic-discriminant.html` : `Δ>0 两实根，Δ=0 重根，Δ<0 复根。` : dead

  其它成因样例（共 42 条，仅列前 5）：
  - `tools/math/circular-permutation.html` : `环形排列数 = (n−1)!` : fragment
  - `tools/math/factorial-calc.html` : `n 必须是非负整数（不支持小数、负数或空值）。` : dynamic
  - `tools/math/fibonacci-n.html` : `n 必须是非负整数（不支持小数、负数或空值）。` : dynamic
  - `tools/math/fibonacci-n.html` : `为保证计算性能，n 上限为 1000（已不再静默截断）。` : dynamic
  - `tools/math/function-plotter.html` : `🧮 数学图形绘制` : harmless

### mechanical（dead 1 / dynamic 0 / fragment 0 / harmless 0）

- `tools/mechanical/torque-power.html` : `P = T·ω/1000 应回等于输入功率` : dead

### medical（dead 13 / dynamic 16 / fragment 1 / harmless 0）

- `tools/medical/assessor-risk-3.html` : `尿酸结石在酸性尿(pH<5.5)中易形成，碱化至pH 6.5-7.0可预防` : dead
- `tools/medical/calc-34.html` : `BMI = 体重(kg) ÷ 身高(m)²：<18.5 偏瘦｜18.5–24 正常｜24–28 超重｜≥28 肥胖` : dead
- `tools/medical/calc-34.html` : `RER（静息能量需求）按 25 kcal/kg 估算，参考区间 25–30 kcal/kg，与 BMR 不是同一指标；肥胖者按理想体重、重症需叠加应激系数。` : dead
- `tools/medical/calc-34.html` : `按 Mifflin-St Jeor 公式估算静息能量消耗（RER/BMR），再乘活动系数得每日总消耗（` : dead
- `tools/medical/calc-34.html` : `男性 65 kg / 170 cm / 30 岁、久坐（1.2）：BMR = 650 + 1062.5 − 150 + 5 = 1567.5 ≈ 1568 kcal/日；TDEE = 1567.5 × 1.2 ≈ 1881 kcal；减脂目标 ≈ 1505 kcal；增肌目标 ≈ 2281 kcal；BMI = 65 …(+142字)` : dead
- `tools/medical/calculator-calc-2.html` : `婴儿（<1 岁）与老年（≥65 岁）提示专科核定` : dead
- `tools/medical/clinical-tools.html` : `13–15 分：轻度意识障碍，密切观察、定期复评` : dead
- `tools/medical/convert-glucose.html` : `空腹血糖 5.6 mmol/L → 5.6 × 18.0159 ≈ 100.9 mg/dL，属正常范围（3.9-6.1 mmol/L / 70-110 mg/dL）。随机血糖 11.1 mmol/L → × 18.0159 ≈ 200.0 mg/dL，达到糖尿病诊断的随机阈值。反向：血糖仪显示 100.9 mg/dL …(+228字)` : dead
- `tools/medical/convert-time-infusion.html` : `滴速(滴/分) = 液体量(mL) × 滴系数(滴/mL) ÷ 时间(分)` : dead
- `tools/medical/dosage-calculator.html` : `体重法：单次剂量 = 体重(kg) × 每公斤剂量(mg/kg)，日剂量 = 单次剂量 × 每日次数。体表面积法：BSA(m²) = √(身高(cm) × 体重(kg) ÷ 3600)（Mosteller 公式），单次剂量 = BSA × 每平方米剂量(mg/m²)，日剂量 = 单次 × 次数。两套基准必须按药物说明书…(+74字)` : dead
- `tools/medical/dosage-calculator.html` : `每公斤/每平方米剂量` : dead
- `tools/medical/stats-4.html` : `平均时长 x̄ = Σ时长 ÷ 例数` : dead
- `tools/medical/stats-4.html` : `时长上限 P95 ≈ x̄ + 1.645 × 标准差` : dead

  其它成因样例（共 17 条，仅列前 5）：
  - `tools/medical/calc-34.html` : `⚠️ 当前减脂缺口超过建议的 300–500 kcal/日上限，建议上调摄入或提高活动量。` : dynamic
  - `tools/medical/calculator-calc-2.html` : `有效最大日剂量（取较小值）` : dynamic
  - `tools/medical/clinical-tools.html` : `90 天死亡率约 1.9%，定期随访。` : dynamic
  - `tools/medical/clinical-tools.html` : `90 天死亡率约 6.0%，每 3–6 个月复查并评估移植指征。` : dynamic
  - `tools/medical/clinical-tools.html` : `90 天死亡率约 19.6%，建议启动肝移植评估。` : dynamic

### metallurgy（dead 13 / dynamic 15 / fragment 5 / harmless 0）

- `tools/metallurgy/convert-hardness.html` : `千布氏` : dead
- `tools/metallurgy/convert-hardness.html` : `千洛氏` : dead
- `tools/metallurgy/convert-hardness.html` : `毫布氏` : dead
- `tools/metallurgy/convert-hardness.html` : `毫洛氏` : dead
- `tools/metallurgy/hardness-conversion.html` : `硬度换算（ASTM E140 / GB/T 33362 近似）：以线性插值在标准对照表上换算布氏 HB、洛氏 HRC/HRB、维氏 HV；同一材料不同标尺硬度对应同一抗拉强度区间，如 HRC 20 约对应 HB 238、HV 247，HRC 40 约对应 HB 371、HV 392。` : dead
- `tools/metallurgy/stats-10.html` : `成材率 = 合格成品材量 ÷ 合格坯（锭）量 × 100%` : dead
- `tools/metallurgy/stats-10.html` : `收得率 = 合格坯（锭）量 ÷ 入炉金属料 × 100%` : dead
- `tools/metallurgy/steel-profile-weight.html` : `圆管壁厚需满足 0 < t < a/2。` : dead
- `tools/metallurgy/steel-profile-weight.html` : `圆钢/圆管` : dead
- `tools/metallurgy/steel-profile-weight.html` : `壁厚/边厚 t（mm，管/角钢用）` : dead
- `tools/metallurgy/steel-profile-weight.html` : `按碳钢密度 7.85 g/cm³ 推导的经验系数（圆钢 0.00617、方钢/扁钢/角钢 0.00785）： 圆钢 a²×0.00617 = 20²×0.00617 = 2.468 kg/m，总重 2.468×6 ≈ 14.81 kg； 方钢 a²×0.00785 = 3.14 kg/m，总重 18.84 kg； 扁钢…(+212字)` : dead
- `tools/metallurgy/steel-profile-weight.html` : `槽钢需满足 0 < t < b，且次尺寸 b 大于 0。` : dead
- `tools/metallurgy/steel-profile-weight.html` : `角钢边厚需满足 0 < t < a。` : dead

  其它成因样例（共 20 条，仅列前 5）：
  - `tools/metallurgy/alloy-ratio.html` : `预计终态(%)` : dynamic
  - `tools/metallurgy/alloy-ratio.html` : `各元素目标含量合计超出原料可带入能力，无法同时达到，请降低目标或提高合金含量/回收率。` : dynamic
  - `tools/metallurgy/convert-hardness.html` : `布氏` : fragment
  - `tools/metallurgy/convert-hardness.html` : `洛氏` : fragment
  - `tools/metallurgy/energy-1.html` : `折标煤 =（节电量 × 0.1229 ＋ 节气量 × 1.33）÷ 1000（tce）；减排 CO₂ ≈ 折标煤 × 2.66（t）；折能 = 折标煤 × 29.307（GJ）` : fragment

### metalwork（dead 40 / dynamic 18 / fragment 8 / harmless 1）

- `tools/metalwork/analysis-39.html` : `热处理控温记录` : dead
- `tools/metalwork/analysis-39.html` : `热处理（自动化/控温/记录）` : dead
- `tools/metalwork/analysis-39.html` : `热处理（自动化/控温/记录） - 面向热处理车间的控温记录工具` : dead
- `tools/metalwork/analysis-cost-price-5.html` : `Mean = 各期价格之和 ÷ 期数；样本标准差按 n−1 口径计算，变异系数 CV = 标准差 ÷ 均值 ×100%，用来衡量价格波动幅度。` : dead
- `tools/metalwork/analysis-cost-price-5.html` : `Range = 最高价 − 最低价；首末涨跌幅 =（末期价 − 首期价）÷ 首期价 ×100%。` : dead
- `tools/metalwork/analysis-cost-price-5.html` : `安装（敷设/连接/测试）服务` : dead
- `tools/metalwork/analysis-cost-price-5.html` : `安装（敷设/连接/测试）服务 - 电缆安装敷设后的绝缘电阻、导通电阻` : dead
- `tools/metalwork/calc-feed.html` : `铣削进给 f = v_c/(π·d·n)` : dead
- `tools/metalwork/calc-gear-2.html` : `由端面模数 mt、齿数 z 决定齿距与啮合尺寸。` : dead
- `tools/metalwork/calc-gear-2.html` : `端面模数 mt = 分度圆直径÷齿数，是齿轮尺寸与强度的核心参数，必须成对啮合相同，单位 mm；斜齿的法向模数 mn = mt×cosβ。` : dead
- `tools/metalwork/calc-gear-2.html` : `齿轮加工 = 滚齿/插齿参数` : dead
- `tools/metalwork/calc-pressure-mold.html` : `Perimeter L=100mm、料厚 t=2mm、抗剪强度 τ=350MPa：理论冲裁力 F = L×t×τ = 100×2×350 = 70000 N = 70 kN；设计力 Fd = 70×1.3 = 91 kN（含安全系数）。` : dead
- `tools/metalwork/calc-pressure-mold.html` : `冲压力 F = L·t·τ` : dead
- `tools/metalwork/calc-stretch.html` : `拉伸率 = (L−L₀)/L₀ × 100%` : dead
- `tools/metalwork/detector-21.html` : `无损检测 = 方法选择` : dead
- `tools/metalwork/detector-24.html` : `缺陷（气孔/缩松/夹渣）分析` : dead
- `tools/metalwork/detector-55.html` : `≥90% 优秀，75-89% 良好，60-74% 合格，<60% 不合格` : dead
- `tools/metalwork/detector-hardness.html` : `Qualified （一般用途）` : dead
- `tools/metalwork/detector-hardness.html` : `盐雾试验结果评估` : dead
- `tools/metalwork/detector-hardness.html` : `盐雾（试验/等级/标准）评估` : dead
- `tools/metalwork/detector-hardness.html` : `盐雾（试验/等级/标准）评估 - 盐雾试验结果评估工具` : dead
- `tools/metalwork/forging-ratio.html` : `锻造比 = A₀/A` : dead
- `tools/metalwork/laxue-ladao-chisheng-lali-sheji.html` : `按单位切削力 250 N/mm²、切削宽度 10 mm、同时工作齿数 3 计算切屑总面积对应的拉削力，再按 1.3 倍安全系数与刀杆许用拉应力 600 MPa 反推刀杆最小截面。` : dead
- `tools/metalwork/lifespan-1.html` : `电池寿命 = 容量/负载` : dead
- `tools/metalwork/pinpaijiazhipinggujisuan.html` : `本页用经验参数法：品牌利润×行业乘数×年限系数×份额系数；乘数与行业、品牌强度相关，仅作快速比较与参考，不等同 ISO 10668 的合规品牌评估。` : dead
- `tools/metalwork/pinpaijiazhipinggujisuan.html` : `用经验倍率快速估算制造/金工品牌的参考价值（非合规评估）。` : dead
- `tools/metalwork/pressure-casting.html` : `铸造方法 = 选型` : dead
- `tools/metalwork/resistance-2.html` : `Mass/成本/保护气体对比` : dead
- `tools/metalwork/resistance-2.html` : `焊接方法 = 选型` : dead
- `tools/metalwork/resistance-2.html` : `输入材料厚度、接头形式与材料类型，推荐适合的焊接方法（仅做方法选型，不计算电流、电压等工艺参数）。` : dead
- `tools/metalwork/sheet-bend.html` : `钣金折弯展开 = 中性层法` : dead
- `tools/metalwork/speed-itinerary.html` : `刨削速度 = 行程/时间` : dead
- `tools/metalwork/surface-finish.html` : `Surface roughness = Ra 对照` : dead
- `tools/metalwork/surface-finish.html` : `表面粗糙度 = Ra 对照` : dead
- `tools/metalwork/temp-forging.html` : `锻造温度 = 材料相图区间` : dead
- `tools/metalwork/tester-19.html` : `价格（铜价/行情/成本）分析` : dead
- `tools/metalwork/thread.html` : `螺纹加工 = 方案选择` : dead
- `tools/metalwork/welding-heat.html` : `热输入 Q = η·U·I/v` : dead
- `tools/metalwork/welding-heat.html` : `请输入有效参数：电流、电压、焊速 > 0，热效率 η 在 0–1 之间` : dead
- `tools/metalwork/zulinfeilvjisuan.html` : `租赁费率 = 原值×费率/周期` : dead

  其它成因样例（共 27 条，仅列前 5）：
  - `tools/metalwork/cable-tray-sizing.html` : `单根截面积 A₁ = π·D²/4；电缆总截面积 A = A₁·N；所需桥架面积 A_need = A / 填充率；推荐规格取满足「宽×高 ≥ A_need」的最小规格；实际填充率 = A /(宽×高)×100%` : fragment
  - `tools/metalwork/cable-tray-sizing.html` : `需定制/双排` : dynamic
  - `tools/metalwork/cable-tray-sizing.html` : `所需面积已超过常规最大规格 600×200（120000 mm²），请改用定制桥架或双排并联，并按实际规格重新校核填充率。` : dynamic
  - `tools/metalwork/calc-gear-2.html` : `端面齿距 pt (mm)` : dynamic
  - `tools/metalwork/calc-gear-2.html` : `法向模数 mn (mm)` : dynamic

