/**
 * ToolBox 一维条码编码库（纯前端、零依赖）
 * ---------------------------------------------------------------------------
 * 编码表依据：
 *   Code 128  —— ISO/IEC 15417:2007（Start A/B/C、107 个符号 + 13 模块 Stop，
 *                校验位为加权模 103：sum = start + Σ value_i × i）
 *   EAN-13    —— GS1 General Specifications（L/G/R 三组编码，首位决定左侧
 *                L/G 组合；校验位为加权模 10，奇数位 ×1、偶数位 ×3）
 *   UPC-A     —— GS1 General Specifications（左侧 L、右侧 R；奇数位 ×3、偶数位 ×1）
 *   Code 39   —— ISO/IEC 16388（5 bar + 4 space 共 9 元素，其中 3 个宽元素；
 *                bar 用 two-out-of-five 权重 1/2/4/7/0，space 位置决定分组）
 *   Pharmacode—— 单轨药码（二进制去掉最高位后自低位起交替 bar/space，1=宽 0=窄）
 *
 * 输出统一为「模块位串」：字符 '1' 表示黑条（一个模块宽），'0' 表示空白。
 * 该表示与具体绘制方式（canvas / SVG）解耦，便于下载多种格式。
 */
(function (global) {
  'use strict';

  /* ======================= Code 128 ======================= */
  // 索引 0~102 为数据符号，103/104/105 为 Start A/B/C，106 为 Stop（13 模块）
  var CODE128 = [
    '11011001100', '11001101100', '11001100110', '10010011000', '10010001100',
    '10001001100', '10011001000', '10011000100', '10001100100', '11001001000',
    '11001000100', '11000100100', '10110011100', '10011011100', '10011001110',
    '10111001100', '10011101100', '10011100110', '11001110010', '11001011100',
    '11001001110', '11011100100', '11001110100', '11101101110', '11101001100',
    '11100101100', '11100100110', '11101100100', '11100110100', '11100110010',
    '11011011000', '11011000110', '11000110110', '10100011000', '10001011000',
    '10001000110', '10110001000', '10001101000', '10001100010', '11010001000',
    '11000101000', '11000100010', '10110111000', '10110001110', '10001101110',
    '10111011000', '10111000110', '10001110110', '11101110110', '11010001110',
    '11000101110', '11011101000', '11011100010', '11011101110', '11101011000',
    '11101000110', '11100010110', '11101101000', '11101100010', '11100011010',
    '11101111010', '11001000010', '11110001010', '10100110000', '10100001100',
    '10010110000', '10010000110', '10000101100', '10000100110', '10110010000',
    '10110000100', '10011010000', '10011000010', '10000110100', '10000110010',
    '11000010010', '11001010000', '11110111010', '11000010100', '10001111010',
    '10100111100', '10010111100', '10010011110', '10111100100', '10011110100',
    '10011110010', '11110100100', '11110010100', '11110010010', '11011011110',
    '11011110110', '11110110110', '10101111000', '10100011110', '10001011110',
    '10111101000', '10111100010', '11110101000', '11110100010', '10111011110',
    '10111101110', '11101011110', '11110101110', '11010000100', '11010010000',
    '11010011100', '1100011101011'
  ];
  var C128_START_A = 103, C128_START_B = 104, C128_START_C = 105, C128_STOP = 106;

  function inRange(text, lo, hi) {
    for (var i = 0; i < text.length; i++) {
      var c = text.charCodeAt(i);
      if (c < lo || c > hi) return false;
    }
    return true;
  }

  /**
   * Code 128 编码。子集选择策略（不做动态规划，取确定性规则）：
   *   纯数字且长度为偶数 → Code C（每两位一个符号，最紧凑）
   *   全部可打印 ASCII（32~127）→ Code B
   *   其余落在 ASCII 0~95 内 → Code A
   */
  function code128Encode(text) {
    if (!text) return { ok: false, error: '请输入条码内容' };
    var start, values = [], i;
    if (/^[0-9]+$/.test(text) && text.length % 2 === 0 && text.length >= 2) {
      start = C128_START_C;
      for (i = 0; i < text.length; i += 2) values.push(parseInt(text.substr(i, 2), 10));
    } else if (inRange(text, 32, 127)) {
      start = C128_START_B;
      for (i = 0; i < text.length; i++) values.push(text.charCodeAt(i) - 32);
    } else if (inRange(text, 0, 95)) {
      start = C128_START_A;
      for (i = 0; i < text.length; i++) {
        var cc = text.charCodeAt(i);
        values.push(cc < 32 ? cc + 64 : cc - 32);
      }
    } else {
      return { ok: false, error: 'Code 128 仅支持 ASCII 0~127，请改用 Code 39 或缩短内容' };
    }
    var sum = start;
    for (i = 0; i < values.length; i++) sum += values[i] * (i + 1);
    var checksum = sum % 103;
    var bits = CODE128[start];
    for (i = 0; i < values.length; i++) bits += CODE128[values[i]];
    bits += CODE128[checksum] + CODE128[C128_STOP];
    var subset = start === C128_START_C ? 'C' : (start === C128_START_B ? 'B' : 'A');
    return {
      ok: true, bits: bits, text: text,
      detail: {
        subset: subset,
        symbolCount: values.length,
        checksum: checksum,
        checksumRaw: sum,
        widthModules: bits.length,
        quiet: 10
      }
    };
  }

  /* ======================= EAN-13 / UPC-A ======================= */
  var EAN_L = ['0001101', '0011001', '0010011', '0111101', '0100011',
               '0110001', '0101111', '0111011', '0110111', '0001011'];
  var EAN_G = ['0100111', '0110011', '0011011', '0100001', '0011101',
               '0111001', '0000101', '0010001', '0001001', '0010111'];
  var EAN_R = ['1110010', '1100110', '1101100', '1000010', '1011100',
               '1001110', '1010000', '1000100', '1001000', '1110100'];
  // 首位数字 → 左侧 6 位的 L/G 组合
  var EAN13_PARITY = ['LLLLLL', 'LLGLGG', 'LLGGLG', 'LLGGGL', 'LGLLGG',
                      'LGGLLG', 'LGGGLL', 'LGLGLG', 'LGLGGL', 'LGGLGL'];

  function ean13Check(d12) {
    var s = 0;
    for (var i = 0; i < 12; i++) s += (+d12.charAt(i)) * (i % 2 === 0 ? 1 : 3);
    return (10 - (s % 10)) % 10;
  }

  function ean13Encode(digits) {
    digits = String(digits || '').replace(/\D/g, '');
    if (digits.length === 12) {
      digits += ean13Check(digits);
    } else if (digits.length === 13) {
      var expect = ean13Check(digits.slice(0, 12));
      if (+digits.charAt(12) !== expect) {
        return { ok: false, error: '第 13 位校验位应为 ' + expect + '，当前为 ' + digits.charAt(12) };
      }
    } else {
      return { ok: false, error: 'EAN-13 需要 12 位数字（自动补校验位）或完整 13 位' };
    }
    var parity = EAN13_PARITY[+digits.charAt(0)];
    var bits = '101', i;
    for (i = 1; i <= 6; i++) {
      var d = +digits.charAt(i);
      bits += parity.charAt(i - 1) === 'L' ? EAN_L[d] : EAN_G[d];
    }
    bits += '01010';
    for (i = 7; i <= 12; i++) bits += EAN_R[+digits.charAt(i)];
    bits += '101';
    return {
      ok: true, bits: bits, text: digits,
      detail: {
        parity: parity,
        checksum: +digits.charAt(12),
        checksumRaw: '左侧奇偶组合 ' + parity,
        widthModules: bits.length,
        quiet: 11
      }
    };
  }

  function upcaCheck(d11) {
    var s = 0;
    for (var i = 0; i < 11; i++) s += (+d11.charAt(i)) * (i % 2 === 0 ? 3 : 1);
    return (10 - (s % 10)) % 10;
  }

  function upcaEncode(digits) {
    digits = String(digits || '').replace(/\D/g, '');
    if (digits.length === 11) {
      digits += upcaCheck(digits);
    } else if (digits.length === 12) {
      var expect = upcaCheck(digits.slice(0, 11));
      if (+digits.charAt(11) !== expect) {
        return { ok: false, error: '第 12 位校验位应为 ' + expect + '，当前为 ' + digits.charAt(11) };
      }
    } else {
      return { ok: false, error: 'UPC-A 需要 11 位数字（自动补校验位）或完整 12 位' };
    }
    var bits = '101', i;
    for (i = 0; i < 6; i++) bits += EAN_L[+digits.charAt(i)];
    bits += '01010';
    for (i = 6; i < 12; i++) bits += EAN_R[+digits.charAt(i)];
    bits += '101';
    return {
      ok: true, bits: bits, text: digits,
      detail: {
        checksum: +digits.charAt(11),
        checksumRaw: '左侧 L / 右侧 R 编码',
        widthModules: bits.length,
        quiet: 9
      }
    };
  }

  /* ======================= Code 39 ======================= */
  // bar 权重：位置 1~5 依次为 1 / 2 / 4 / 7 / 0（Σ=11 时数字组记为 0、字母组记为 10）
  var C39_WEIGHT = [1, 2, 4, 7, 0];
  var C39_SPACE_GROUP = { '30': 0, '0': 1, '10': 2, '20': 3 };

  function c39BuildTable() {
    var table = {};
    var i, ch;
    // 数字 0~9：bar 值即数字本身（0 由 Σ=11 表示），space 落在 +0 组（位置 2）
    for (i = 0; i <= 9; i++) {
      table[String(i)] = { bv: i === 0 ? 10 : i, sp: C39_SPACE_GROUP['0'] };
    }
    // 字母 A~Z：连续 4 组，每组 10 个（值 = bar 值 + 组基数 − 1）
    var groups = [
      { from: 10, sp: C39_SPACE_GROUP['10'] },
      { from: 20, sp: C39_SPACE_GROUP['20'] },
      { from: 30, sp: C39_SPACE_GROUP['30'] }
    ];
    for (var g = 0; g < groups.length; g++) {
      for (i = 0; i < 10; i++) {
        var val = groups[g].from + i;
        if (val > 35) break;                      // A~Z 共 26 个字母
        ch = String.fromCharCode(65 + val - 10);
        table[ch] = { bv: i + 1, sp: groups[g].sp };
      }
    }
    // +30 组的剩余位：- (36) . (37) 空格 (38) * (39)
    table['-'] = { bv: 7, sp: C39_SPACE_GROUP['30'] };
    table['.'] = { bv: 8, sp: C39_SPACE_GROUP['30'] };
    table[' '] = { bv: 9, sp: C39_SPACE_GROUP['30'] };
    table['*'] = { bv: 10, sp: C39_SPACE_GROUP['30'] };   // 起止符
    return table;
  }
  var C39_TABLE = c39BuildTable();
  var C39_SUPPORTED = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ-. ';

  function c39Bars(bv) {
    var target = bv === 10 ? 11 : bv;            // Σ=11 的图案即 NNWWN（位置 3、4）
    for (var a = 0; a < 5; a++) {
      for (var b = a + 1; b < 5; b++) {
        if (C39_WEIGHT[a] + C39_WEIGHT[b] === target) {
          var arr = ['N', 'N', 'N', 'N', 'N'];
          arr[a] = 'W'; arr[b] = 'W';
          return arr;
        }
      }
    }
    return null;
  }

  /**
   * 生成单个 Code 39 字符的模块位串。
   * 9 个元素按 bar,space,bar,space,bar,space,bar,space,bar 排列，
   * bar 用 '1' 表示（宽 = 多模块），space 用 '0' 表示。
   */
  function code39Char(ch, barN, barW, spN, spW) {
    var spec = C39_TABLE[ch];
    if (!spec) return null;
    var bars = c39Bars(spec.bv);
    var spaces = ['N', 'N', 'N', 'N'];
    spaces[spec.sp] = 'W';
    var out = '';
    for (var i = 0; i < 5; i++) {
      out += bars[i] === 'W' ? barW : barN;
      if (i < 4) out += spaces[i] === 'W' ? spW : spN;
    }
    return out;
  }

  /** Code 39：支持 0~9 A~Z - . 空格；宽窄比默认 2:1（ISO/IEC 16388 允许 2:1~3:1） */
  function code39Encode(text, ratio) {
    if (!text) return { ok: false, error: '请输入条码内容' };
    var use3 = ratio === 3;
    var barN = '1', barW = use3 ? '111' : '11';
    var spN = '0', spW = use3 ? '000' : '00';
    var gap = spN;                       // 字符间隔为 1 个窄空白
    var star = code39Char('*', barN, barW, spN, spW);
    var upper = String(text).toUpperCase();
    var body = '';
    for (var i = 0; i < upper.length; i++) {
      var piece = code39Char(upper.charAt(i), barN, barW, spN, spW);
      if (!piece) {
        return { ok: false, error: 'Code 39 不支持的字符「' + text.charAt(i) + '」，支持 0-9 A-Z 空格 - .（不含 $ / + %）' };
      }
      body += (i ? gap : '') + piece;
    }
    var bits = star + gap + body + gap + star;
    return {
      ok: true, bits: bits, text: upper,
      detail: {
        checksum: null,
        checksumRaw: '无校验位（自校验码制）',
        ratio: use3 ? '3:1' : '2:1',
        widthModules: bits.length,
        quiet: 10
      }
    };
  }

  /* ======================= Pharmacode ======================= */
  function pharmacodeEncode(num) {
    num = parseInt(num, 10);
    if (isNaN(num) || num < 3 || num > 131070) {
      return { ok: false, error: 'Pharmacode 取值范围为 3 ~ 131070（1 与 2 无法构成有效码）' };
    }
    // 规则（Laetus Pharmacode，Wikipedia/Pharmacode）：自右向左，第 i 条（i 从 0 起）
    // 窄条计 2^i、宽条计 2×2^i，全部相加即得数值。等价实现：令 V = num + 1，写成二进制后
    // 去掉最高位，剩余位自左向右逐个映射为条形，0 → 窄条、1 → 宽条。
    // 边界自检：3 → '100' 去掉最高位为 '00' → 两个窄条（1+2=3，与「最小码为 2 条」一致）；
    // 131070 → 16 个宽条（Σ 2×2^i, i=0..15 = 131070，与上限一致）。
    var bin = (num + 1).toString(2).slice(1);
    var bits = '', widths = [];
    for (var i = 0; i < bin.length; i++) {
      var w = bin.charAt(i) === '1' ? 2 : 1;      // 1 → 宽条（2 模块），0 → 窄条（1 模块）
      widths.push(w);
      if (i) bits += '0';                          // 条间固定 1 个模块空白
      bits += w === 2 ? '11' : '1';
    }
    return {
      ok: true, bits: bits, text: String(num),
      detail: {
        binary: num.toString(2),
        barCount: widths.length,
        barWidths: widths.join('-'),
        checksum: null,
        checksumRaw: '无校验位；' + widths.length + ' 条窄宽序列 ' + widths.join('-') + '（窄=1、宽=2）',
        widthModules: bits.length,
        quiet: 10
      }
    };
  }

  /* ======================= 统一入口 ======================= */
  function encode(type, text) {
    switch (type) {
      case 'code128': return code128Encode(text);
      case 'ean13': return ean13Encode(text);
      case 'upca': return upcaEncode(text);
      case 'code39': return code39Encode(text);
      case 'pharmacode': return pharmacodeEncode(text);
      default: return { ok: false, error: '未知码制：' + type };
    }
  }

  /* ======================= 绘制 ======================= */
  function normalizeOptions(o) {
    o = o || {};
    return {
      scale: Math.max(1, Math.min(10, parseFloat(o.scale) || 2)),
      height: Math.max(20, Math.min(400, parseFloat(o.height) || 80)),
      fg: o.fg || '#000000',
      bg: o.bg || '#ffffff',
      showText: o.showText !== false,
      text: o.text || '',
      quiet: o.quiet == null ? 10 : o.quiet,
      fontSize: o.fontSize || 14
    };
  }

  function quietModules(o, bits) {
    return /^[01]+$/.test(bits) ? o.quiet : 0;
  }

  function renderCanvas(bits, options) {
    var o = normalizeOptions(options);
    var q = o.quiet;
    var textH = o.showText ? o.fontSize + 10 : 0;
    var width = bits.length * o.scale + q * 2;
    var height = o.height + textH;
    var canvas = document.createElement('canvas');
    var dpr = window.devicePixelRatio || 1;
    canvas.width = Math.round(width * dpr);
    canvas.height = Math.round(height * dpr);
    canvas.style.width = width + 'px';
    canvas.style.height = height + 'px';
    var ctx = canvas.getContext('2d');
    ctx.scale(dpr, dpr);
    ctx.fillStyle = o.bg;
    ctx.fillRect(0, 0, width, height);
    ctx.fillStyle = o.fg;
    for (var i = 0; i < bits.length; i++) {
      if (bits.charAt(i) === '1') ctx.fillRect(q + i * o.scale, 0, o.scale, o.height);
    }
    if (o.showText) {
      ctx.fillStyle = o.fg;
      ctx.font = o.fontSize + 'px ui-monospace, SFMono-Regular, Menlo, monospace';
      ctx.textAlign = 'center';
      ctx.textBaseline = 'top';
      ctx.fillText(o.text, width / 2, o.height + 5);
    }
    return canvas;
  }

  function renderSVG(bits, options) {
    var o = normalizeOptions(options);
    var q = o.quiet;
    var textH = o.showText ? o.fontSize + 10 : 0;
    var width = bits.length * o.scale + q * 2;
    var height = o.height + textH;
    var parts = [];
    parts.push('<svg xmlns="http://www.w3.org/2000/svg" width="' + width + '" height="' + height +
      '" viewBox="0 0 ' + width + ' ' + height + '" role="img" aria-label="' +
      String(o.text).replace(/[&<>"]/g, function (c) {
        return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c];
      }) + '">');
    parts.push('<rect width="' + width + '" height="' + height + '" fill="' + o.bg + '"/>');
    // 把连续黑条合并成一个矩形，减小 SVG 体积
    var run = 0;
    for (var i = 0; i <= bits.length; i++) {
      if (i < bits.length && bits.charAt(i) === '1') { run++; continue; }
      if (run > 0) {
        parts.push('<rect x="' + (q + (i - run) * o.scale) + '" y="0" width="' +
          (run * o.scale) + '" height="' + o.height + '" fill="' + o.fg + '"/>');
        run = 0;
      }
    }
    if (o.showText) {
      parts.push('<text x="' + (width / 2) + '" y="' + (o.height + 5 + o.fontSize) +
        '" text-anchor="middle" font-family="ui-monospace, SFMono-Regular, Menlo, monospace" font-size="' +
        o.fontSize + '" fill="' + o.fg + '">' +
        String(o.text).replace(/[&<>]/g, function (c) {
          return { '&': '&amp;', '<': '&lt;', '>': '&gt;' }[c];
        }) + '</text>');
    }
    parts.push('</svg>');
    return parts.join('');
  }

  global.ToolBoxBarcode = {
    encode: encode,
    code128: code128Encode,
    ean13: ean13Encode,
    upca: upcaEncode,
    code39: code39Encode,
    pharmacode: pharmacodeEncode,
    renderCanvas: renderCanvas,
    renderSVG: renderSVG,
    CODE128_TABLE: CODE128,
    CODE39_SUPPORTED: C39_SUPPORTED,
    TYPES: [
      { id: 'code128', name: 'Code128', hint: '可变长字母数字，物流与内部编号首选' },
      { id: 'ean13', name: 'EAN-13', hint: '13 位零售商品码，末位为校验位' },
      { id: 'upca', name: 'UPC-A', hint: '12 位北美商品码（EAN-13 的子集）' },
      { id: 'code39', name: 'Code39', hint: '大写字母数字与 - . 空格，无需校验位' }
    ]
  };
})(typeof window !== 'undefined' ? window : this);
