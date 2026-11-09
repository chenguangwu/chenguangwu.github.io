# 复核失败重做批次 · 申请再次复核

## IT-N555 Unicode 查名伪造韩文音节及未分配 CJK 名称

**失败点（原复核记录）**
- 页面：`tools/it/unicode-lookup.html`
- 复现：`lookupName(0xAC00)` 显示 `HANGUL SYLLABLE-AC00`，标准名是 `HANGUL SYLLABLE GA`；`lookupName(0x3FFFF)` 显示 `CJK UNIFIED IDEOGRAPH-3FFFF`，该码位未分配。

**根因**
- `lookupName` 对表外码点：`code>=0xAC00&&code<=0xD7A3` 时直接返回拼接串 `HANGUL SYLLABLE-`+hex，未依 Unicode 音节组合规则（SBase+LIndex+VIndex+TIndex）推导真实音节名；CJK 区间判据写成 `(code>=0x3400&&code<=0x9FFF)||(code>=0x20000&&code<=0x3FFFF)`，区间过宽——`0x3FFFF` 落在该宽区间但属未分配码位，被错误套用 `CJK UNIFIED IDEOGRAPH-` 命名。

**修复位点**
- `tools/it/unicode-lookup.html` `lookupName()`：CJK 判据改为 `isCjkAssigned(code)`，仅覆盖真实已分配子区间（Ext A / 主块 / Ext B~G，其中扩展平面止于 `0x3134F`）；`code>=0xAC00&&code<=0xD7A3` 时改调新增 `hangulSyllableName(code)`，按 19 个初声 / 21 个中声 / 27 个终声（TIndex 0 省略）组合成 `HANGUL SYLLABLE <L><V><T>`。

**验证证据**
- `env -u NODE_OPTIONS node scripts/verify_it_calc.js unicode-lookup` 全绿（含新增用例）。
- 新增回归用例：`search=U+AC00` → `render()` → expect `HANGUL SYLLABLE GA`（修复前 `HANGUL SYLLABLE-AC00` 必红）；`search=U+3FFFF` → `render()` → expect `名称未收录`（修复前 `CJK UNIFIED IDEOGRAPH-3FFFF` 必红）。独立复算：U+AC00 的 SIndex=0 ⇒ L0=G、V0=A、T0=空 ⇒ `HANGUL SYLLABLE GA`，与 UnicodeData 一致。

**判别力实测**
- 单文件判别器 `node scripts/discriminate_check.js verify_it_calc.js`：1330 用例已检、正确变红 1330、逃生项 0。两用例分别锚合成音节名与未收录标记，输入为 `U+AC00`/`U+3FFFF` 码点串、输出为规则推导结果 ⇒ 非回显；默认列表不含该码位，强判别、零逃生。
