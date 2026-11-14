/**
 * ToolBox Aztec 二维条码编码库（ISO/IEC 24778 · 纯前端、零依赖）
 * ---------------------------------------------------------------------------
 * 算法移植自 ZXing（https://github.com/zxing/zxing）的 Aztec 编码器，
 * 原作者 Rustam Abdullaev、Frank Yellin，遵循 Apache License 2.0：
 *   http://www.apache.org/licenses/LICENSE-2.0
 * 移植保持与参考实现逐位一致（已用 ZXing 自带单元测试向量回归校验：
 * testEncode1 / testEncode2 的完整矩阵、testHighLevelEncode 的高电平位串、
 * testStuffBits 的位填充、testGenerateModeMessage 的模式消息）。
 *
 * 编码流程（与规范一致）：
 *   1. 高电平编码：UPPER/LOWER/DIGIT/MIXED/PUNCT 五张码表 + 动态规划，
 *      逐字符取最短位串（不合法字符走 BINARY 移位）
 *   2. 位填充：每 wordSize 位为一字，全 1 / 全 0 的字要插入分隔，避免与
 *      填充位混淆
 *   3. Reed-Solomon 纠错：紧凑型 GF(64)、全尺寸 GF(256)，模式消息用 GF(16)
 *   4. 布点：数据位按层螺旋写入四边，中心画同心方靶心，全尺寸再画参考网格
 *
 * 输出：{ size, layers, compact, codeWords, eccPercent, rows }
 *   rows —— size 个长度 size 的字符串，'1' 为深色模块、'0' 为浅色
 */
(function (global) {
  'use strict';

  /* ===================== 高电平编码码表 ===================== */
  var MODE_UPPER = 0, MODE_LOWER = 1, MODE_DIGIT = 2, MODE_MIXED = 3, MODE_PUNCT = 4;

  // LATCH_TABLE[from][to]：高 16 位为位数，低 16 位为要写入的位串
  var LATCH_TABLE = [
    [0,
      (5 << 16) + 28,               // UPPER -> LOWER
      (5 << 16) + 30,               // UPPER -> DIGIT
      (5 << 16) + 29,               // UPPER -> MIXED
      (10 << 16) + (29 << 5) + 30], // UPPER -> MIXED -> PUNCT
    [(9 << 16) + (30 << 4) + 14,    // LOWER -> DIGIT -> UPPER
      0,
      (5 << 16) + 30,               // LOWER -> DIGIT
      (5 << 16) + 29,               // LOWER -> MIXED
      (10 << 16) + (29 << 5) + 30],
    [(4 << 16) + 14,                // DIGIT -> UPPER
      (9 << 16) + (14 << 5) + 28,   // DIGIT -> UPPER -> LOWER
      0,
      (9 << 16) + (14 << 5) + 29,   // DIGIT -> UPPER -> MIXED
      (14 << 16) + (14 << 10) + (29 << 5) + 30],
    [(5 << 16) + 29,                // MIXED -> UPPER
      (5 << 16) + 28,               // MIXED -> LOWER
      (10 << 16) + (29 << 5) + 30,  // MIXED -> UPPER -> DIGIT
      0,
      (5 << 16) + 30],              // MIXED -> PUNCT
    [(5 << 16) + 31,                // PUNCT -> UPPER
      (10 << 16) + (31 << 5) + 28,  // PUNCT -> UPPER -> LOWER
      (10 << 16) + (31 << 5) + 30,  // PUNCT -> UPPER -> DIGIT
      (10 << 16) + (31 << 5) + 29,  // PUNCT -> UPPER -> MIXED
      0]
  ];

  function blankTable() {
    var t = [], i;
    for (i = 0; i < 256; i++) t.push(0);
    return t;
  }

  // CHAR_MAP[mode][charCode] = 该模式下的码值；0 表示该模式无此字符
  var CHAR_MAP = [blankTable(), blankTable(), blankTable(), blankTable(), blankTable()];

  (function () {
    var c, i;
    CHAR_MAP[MODE_UPPER][32] = 1;
    for (c = 65; c <= 90; c++) CHAR_MAP[MODE_UPPER][c] = c - 65 + 2;
    CHAR_MAP[MODE_LOWER][32] = 1;
    for (c = 97; c <= 122; c++) CHAR_MAP[MODE_LOWER][c] = c - 97 + 2;
    CHAR_MAP[MODE_DIGIT][32] = 1;
    for (c = 48; c <= 57; c++) CHAR_MAP[MODE_DIGIT][c] = c - 48 + 2;
    CHAR_MAP[MODE_DIGIT][44] = 12;  // ','
    CHAR_MAP[MODE_DIGIT][46] = 13;  // '.'
    // MIXED：控制字符 + 几个符号
    var mixed = [0, 32, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13,
      27, 28, 29, 30, 31, 64, 92, 94, 95, 96, 124, 126, 127];
    for (i = 0; i < mixed.length; i++) CHAR_MAP[MODE_MIXED][mixed[i]] = i;
    // PUNCT：0=FLG(n)、1=CR、2=CR LF、3=". "、4=", "、5=": "，其余见 ISO/IEC 24778
    var punct = [0, 13, 0, 0, 0, 0, 33, 39, 35, 36, 37, 38, 39, 40, 41, 42,
      43, 44, 45, 46, 47, 58, 59, 60, 61, 62, 63, 91, 93, 123, 125];
    for (i = 0; i < punct.length; i++) {
      if (punct[i] > 0) CHAR_MAP[MODE_PUNCT][punct[i]] = i;
    }
  })();

  // SHIFT_TABLE[from][to]：单字符临时移位码；-1 表示不存在该移位
  var SHIFT_TABLE = (function () {
    var t = [], i;
    for (i = 0; i < 6; i++) t.push([-1, -1, -1, -1, -1, -1]);
    t[MODE_UPPER][MODE_PUNCT] = 0;
    t[MODE_LOWER][MODE_PUNCT] = 0;
    t[MODE_LOWER][MODE_UPPER] = 28;
    t[MODE_MIXED][MODE_PUNCT] = 0;
    t[MODE_DIGIT][MODE_PUNCT] = 0;
    t[MODE_DIGIT][MODE_UPPER] = 15;
    return t;
  })();

  /* ===================== 位串容器 ===================== */
  function Bits() {
    this.arr = [];
  }
  Bits.prototype.append = function (value, n) {
    for (var i = n - 1; i >= 0; i--) this.arr.push((value >>> i) & 1);
  };
  Bits.prototype.get = function (i) {
    return this.arr[i] === 1;
  };
  Bits.prototype.size = function () {
    return this.arr.length;
  };
  Bits.prototype.toBinary = function () {
    return this.arr.join('');
  };

  /* ===================== 令牌（输出位串的不可变链） ===================== */
  var TOKEN_EMPTY = { prevToken: null, kind: 0, value: 0, bits: 0 };

  function tokenAdd(tok, value, bits) {
    return { prevToken: tok, kind: 0, value: value, bits: bits };
  }
  function tokenAddBinaryShift(tok, start, count) {
    return { prevToken: tok, kind: 1, start: start, count: count };
  }
  function tokenAppendTo(tok, out, bytes) {
    if (tok.kind === 0) {
      out.append(tok.value, tok.bits);
      return;
    }
    var n = tok.count, i;
    for (i = 0; i < n; i++) {
      if (i === 0 || (i === 31 && n <= 62)) {
        out.append(31, 5); // BINARY_SHIFT
        if (n > 62) out.append(n - 31, 16);
        else if (i === 0) out.append(Math.min(n, 31), 5);
        else out.append(n - 31, 5);
      }
      out.append(bytes[tok.start + i], 8);
    }
  }

  /* ===================== 编码状态机 ===================== */
  function binaryShiftCost(n) {
    if (n > 62) return 21; // 带扩展长度的 B/S
    if (n > 31) return 20; // 两段 B/S
    if (n > 0) return 10;  // 一段 B/S
    return 0;
  }

  function mkState(token, mode, binaryBytes, bitCount) {
    return {
      token: token, mode: mode, binaryBytes: binaryBytes,
      bitCount: bitCount, binaryCost: binaryShiftCost(binaryBytes)
    };
  }

  var INITIAL_STATE = mkState(TOKEN_EMPTY, MODE_UPPER, 0, 0);

  function latchAndAppend(st, mode, value) {
    var bitCount = st.bitCount, tok = st.token;
    if (mode !== st.mode) {
      var latch = LATCH_TABLE[st.mode][mode];
      tok = tokenAdd(tok, latch & 0xFFFF, latch >> 16);
      bitCount += latch >> 16;
    }
    var nb = mode === MODE_DIGIT ? 4 : 5;
    tok = tokenAdd(tok, value, nb);
    return mkState(tok, mode, 0, bitCount + nb);
  }

  function shiftAndAppend(st, mode, value) {
    var nb = st.mode === MODE_DIGIT ? 4 : 5;
    var tok = tokenAdd(st.token, SHIFT_TABLE[st.mode][mode], nb);
    tok = tokenAdd(tok, value, 5);
    return mkState(tok, st.mode, 0, st.bitCount + nb + 5);
  }

  function addBinaryShiftChar(st, index) {
    var tok = st.token, mode = st.mode, bitCount = st.bitCount;
    if (st.mode === MODE_PUNCT || st.mode === MODE_DIGIT) {
      var latch = LATCH_TABLE[mode][MODE_UPPER];
      tok = tokenAdd(tok, latch & 0xFFFF, latch >> 16);
      bitCount += latch >> 16;
      mode = MODE_UPPER;
    }
    var delta = (st.binaryBytes === 0 || st.binaryBytes === 31) ? 18
      : (st.binaryBytes === 62 ? 9 : 8);
    var res = mkState(tok, mode, st.binaryBytes + 1, bitCount + delta);
    if (res.binaryBytes === 2047 + 31) res = endBinaryShift(res, index + 1);
    return res;
  }

  function endBinaryShift(st, index) {
    if (st.binaryBytes === 0) return st;
    var tok = tokenAddBinaryShift(st.token, index - st.binaryBytes, st.binaryBytes);
    return mkState(tok, st.mode, 0, st.bitCount);
  }

  function isBetterOrEqualTo(a, b) {
    var n = a.bitCount + (LATCH_TABLE[a.mode][b.mode] >> 16);
    if (a.binaryBytes < b.binaryBytes) n += b.binaryCost - a.binaryCost;
    else if (a.binaryBytes > b.binaryBytes && b.binaryBytes > 0) n += 10;
    return n <= b.bitCount;
  }

  function stateToBits(st, bytes) {
    var list = [], tok = endBinaryShift(st, bytes.length).token;
    while (tok) {
      list.push(tok);
      tok = tok.prevToken;
    }
    var out = new Bits(), i;
    for (i = list.length - 1; i >= 0; i--) tokenAppendTo(list[i], out, bytes);
    return out;
  }

  // 字符集标记 FLG(n)：非默认字符集（如 UTF-8 的 ECI 26）需要先发这个
  function appendFLGn(st, eci) {
    var res = shiftAndAppend(st, MODE_PUNCT, 0); // 0 = FLG(n)
    var tok = res.token, bitsAdded = 3;
    if (eci < 0) {
      tok = tokenAdd(tok, 0, 3); // FNC1
    } else {
      var digits = String(eci);
      tok = tokenAdd(tok, digits.length, 3);
      for (var i = 0; i < digits.length; i++) {
        tok = tokenAdd(tok, digits.charCodeAt(i) - 48 + 2, 4);
      }
      bitsAdded += digits.length * 4;
    }
    return mkState(tok, st.mode, 0, st.bitCount + bitsAdded);
  }

  function simplifyStates(states) {
    var result = [], i, k;
    for (k = 0; k < states.length; k++) {
      var newState = states[k], add = true;
      for (i = 0; i < result.length; i++) {
        if (isBetterOrEqualTo(result[i], newState)) { add = false; break; }
        if (isBetterOrEqualTo(newState, result[i])) { result.splice(i, 1); i--; }
      }
      if (add) result.unshift(newState);
    }
    return result;
  }

  function updateStateForChar(st, index, bytes, result) {
    var ch = bytes[index] & 0xFF;
    var charInCurrentTable = CHAR_MAP[st.mode][ch] > 0;
    var stateNoBinary = null, mode;
    for (mode = 0; mode <= MODE_PUNCT; mode++) {
      var charInMode = CHAR_MAP[mode][ch];
      if (charInMode > 0) {
        if (stateNoBinary === null) stateNoBinary = endBinaryShift(st, index);
        if (!charInCurrentTable || mode === st.mode || mode === MODE_DIGIT) {
          result.push(latchAndAppend(stateNoBinary, mode, charInMode));
        }
        if (!charInCurrentTable && SHIFT_TABLE[st.mode][mode] >= 0) {
          result.push(shiftAndAppend(stateNoBinary, mode, charInMode));
        }
      }
    }
    if (st.binaryBytes > 0 || CHAR_MAP[st.mode][ch] === 0) {
      result.push(addBinaryShiftChar(st, index));
    }
  }

  function updateStateForPair(st, index, pairCode, result) {
    var stateNoBinary = endBinaryShift(st, index);
    result.push(latchAndAppend(stateNoBinary, MODE_PUNCT, pairCode));
    if (st.mode !== MODE_PUNCT) {
      result.push(shiftAndAppend(stateNoBinary, MODE_PUNCT, pairCode));
    }
    if (pairCode === 3 || pairCode === 4) {
      // 两个字符都在 DIGIT 表里时，直接连续写两位数更省位
      result.push(latchAndAppend(
        latchAndAppend(stateNoBinary, MODE_DIGIT, 16 - pairCode), MODE_DIGIT, 1));
    }
    if (st.binaryBytes > 0) {
      result.push(addBinaryShiftChar(addBinaryShiftChar(st, index), index + 1));
    }
  }

  function highLevelEncode(bytes, eci) {
    var states = [eci === null || eci === undefined ? INITIAL_STATE : appendFLGn(INITIAL_STATE, eci)];
    var index, i;
    for (index = 0; index < bytes.length; index++) {
      var pairCode = 0, next = index + 1 < bytes.length ? bytes[index + 1] : 0;
      if (bytes[index] === 13) pairCode = next === 10 ? 2 : 0;       // CR LF
      else if (bytes[index] === 46) pairCode = next === 32 ? 3 : 0;  // ". "
      else if (bytes[index] === 44) pairCode = next === 32 ? 4 : 0;  // ", "
      else if (bytes[index] === 58) pairCode = next === 32 ? 5 : 0;  // ": "
      if (pairCode > 0) {
        var list = [];
        for (i = 0; i < states.length; i++) updateStateForPair(states[i], index, pairCode, list);
        states = simplifyStates(list);
        index++;
      } else {
        var list2 = [];
        for (i = 0; i < states.length; i++) updateStateForChar(states[i], index, bytes, list2);
        states = simplifyStates(list2);
      }
    }
    var min = states[0];
    for (i = 1; i < states.length; i++) {
      if (states[i].bitCount < min.bitCount) min = states[i];
    }
    return stateToBits(min, bytes);
  }

  /* ===================== 伽罗华域与 Reed-Solomon ===================== */
  // primitive 为不可约多项式的位表示，generatorBase 为生成多项式起始幂（Aztec 取 1）
  function GF(primitive, size, generatorBase) {
    this.size = size;
    this.generatorBase = generatorBase;
    this.expTable = [];
    this.logTable = [];
    var x = 1, i;
    for (i = 0; i < size; i++) {
      this.expTable.push(x);
      x *= 2;
      if (x >= size) {
        x ^= primitive;
        x &= size - 1;
      }
    }
    for (i = 0; i < size - 1; i++) this.logTable[this.expTable[i]] = i;
  }
  GF.prototype.exp = function (n) {
    return this.expTable[n % (this.size - 1)];
  };
  GF.prototype.mul = function (a, b) {
    if (a === 0 || b === 0) return 0;
    return this.expTable[(this.logTable[a] + this.logTable[b]) % (this.size - 1)];
  };

  var GF_AZTEC_PARAM = new GF(0x13, 16, 1);      // x^4 + x + 1
  var GF_AZTEC_DATA_6 = new GF(0x43, 64, 1);     // x^6 + x + 1
  var GF_AZTEC_DATA_8 = new GF(0x12D, 256, 1);   // x^8 + x^5 + x^3 + x^2 + 1
  var GF_AZTEC_DATA_10 = new GF(0x409, 1024, 1); // x^10 + x^3 + 1
  var GF_AZTEC_DATA_12 = new GF(0x1069, 4096, 1); // x^12 + x^6 + x^5 + x^3 + 1

  function getField(wordSize) {
    switch (wordSize) {
      case 4: return GF_AZTEC_PARAM;
      case 6: return GF_AZTEC_DATA_6;
      case 8: return GF_AZTEC_DATA_8;
      case 10: return GF_AZTEC_DATA_10;
      case 12: return GF_AZTEC_DATA_12;
      default: throw new Error('不支持的码字长度: ' + wordSize);
    }
  }

  // 生成多项式 g(x) = ∏(x + a^(i+generatorBase))，返回按幂次升序的系数
  function generatorPolyAsc(field, degree) {
    var poly = [1], d, i;
    for (d = 0; d < degree; d++) {
      var f = field.exp(d + field.generatorBase);
      var next = [];
      for (i = 0; i <= poly.length; i++) next.push(0);
      for (i = 0; i < poly.length; i++) {
        next[i + 1] ^= poly[i];
        next[i] ^= field.mul(poly[i], f);
      }
      poly = next;
    }
    return poly;
  }

  // 多项式长除法取余，data 为按幂次降序的系数
  function rsRemainder(data, ecCount, field) {
    var genAsc = generatorPolyAsc(field, ecCount);
    var gen = genAsc.slice().reverse(); // 降序，gen[0] 恒为 1
    var buf = data.slice(), i, j;
    for (i = 0; i < ecCount; i++) buf.push(0);
    for (i = 0; i < data.length; i++) {
      var coef = buf[i];
      if (coef !== 0) {
        for (j = 0; j < gen.length; j++) buf[i + j] ^= field.mul(gen[j], coef);
      }
    }
    return buf.slice(data.length, data.length + ecCount);
  }

  /* ===================== 符号尺寸与布点 ===================== */
  var WORD_SIZE = [4, 6, 6, 8, 8, 8, 8, 8, 8,
    10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10,
    12, 12, 12, 12, 12, 12, 12, 12, 12, 12];

  var MAX_LAYERS = 32, MAX_LAYERS_COMPACT = 4;

  function totalBitsInLayer(layers, compact) {
    return ((compact ? 88 : 112) + 16 * layers) * layers;
  }

  function bitsToWords(stuffedBits, wordSize, totalWords) {
    var message = [], i, j;
    for (i = 0; i < totalWords; i++) message.push(0);
    var n = Math.floor(stuffedBits.size() / wordSize);
    for (i = 0; i < n; i++) {
      var value = 0;
      for (j = 0; j < wordSize; j++) {
        if (stuffedBits.get(i * wordSize + j)) value |= 1 << (wordSize - j - 1);
      }
      message[i] = value;
    }
    return message;
  }

  // 位填充：全 1 / 全 0 的字会与填充位混淆，需插入分隔位（参考实现同款处理）
  function stuffBits(bits, wordSize) {
    var out = new Bits();
    var n = bits.size(), mask = (1 << wordSize) - 2, i, j;
    for (i = 0; i < n; i += wordSize) {
      var word = 0;
      for (j = 0; j < wordSize; j++) {
        if (i + j >= n || bits.get(i + j)) word |= 1 << (wordSize - 1 - j);
      }
      if ((word & mask) === mask) {
        out.append(word & mask, wordSize);
        i--;
      } else if ((word & mask) === 0) {
        out.append(word | 1, wordSize);
        i--;
      } else {
        out.append(word, wordSize);
      }
    }
    return out;
  }

  function generateCheckWords(bitArray, totalBits, wordSize) {
    var messageSizeInWords = bitArray.size() / wordSize;
    var totalWords = Math.floor(totalBits / wordSize);
    var words = bitsToWords(bitArray, wordSize, totalWords);
    var ecWords = totalWords - messageSizeInWords;
    if (ecWords <= 0) throw new Error('纠错码字数量非法');
    var rem = rsRemainder(words.slice(0, messageSizeInWords), ecWords, getField(wordSize));
    for (var i = 0; i < ecWords; i++) words[messageSizeInWords + i] = rem[i];
    var startPad = totalBits % wordSize;
    var out = new Bits();
    out.append(0, startPad);
    for (var k = 0; k < totalWords; k++) out.append(words[k], wordSize);
    return out;
  }

  function generateModeMessage(compact, layers, messageSizeInWords) {
    var b = new Bits();
    if (compact) {
      b.append(layers - 1, 2);
      b.append(messageSizeInWords - 1, 6);
      return generateCheckWords(b, 28, 4);
    }
    b.append(layers - 1, 5);
    b.append(messageSizeInWords - 1, 11);
    return generateCheckWords(b, 40, 4);
  }

  function BitMatrix(size) {
    this.size = size;
    this.rows = [];
    for (var y = 0; y < size; y++) {
      var row = [];
      for (var x = 0; x < size; x++) row.push(false);
      this.rows.push(row);
    }
  }
  BitMatrix.prototype.set = function (x, y) {
    if (x >= 0 && y >= 0 && x < this.size && y < this.size) this.rows[y][x] = true;
  };
  BitMatrix.prototype.get = function (x, y) {
    return this.rows[y][x];
  };

  function drawBullsEye(matrix, center, size) {
    var i, j;
    for (i = 0; i < size; i += 2) {
      for (j = center - i; j <= center + i; j++) {
        matrix.set(j, center - i);
        matrix.set(j, center + i);
        matrix.set(center - i, j);
        matrix.set(center + i, j);
      }
    }
    matrix.set(center - size, center - size);
    matrix.set(center - size + 1, center - size);
    matrix.set(center - size, center - size + 1);
    matrix.set(center + size, center - size);
    matrix.set(center + size, center - size + 1);
    matrix.set(center + size, center + size - 1);
  }

  function drawModeMessage(matrix, compact, matrixSize, modeMessage) {
    var center = Math.floor(matrixSize / 2), i, offset;
    if (compact) {
      for (i = 0; i < 7; i++) {
        offset = center - 3 + i;
        if (modeMessage.get(i)) matrix.set(offset, center - 5);
        if (modeMessage.get(i + 7)) matrix.set(center + 5, offset);
        if (modeMessage.get(20 - i)) matrix.set(offset, center + 5);
        if (modeMessage.get(27 - i)) matrix.set(center - 5, offset);
      }
    } else {
      for (i = 0; i < 10; i++) {
        offset = center - 5 + i + Math.floor(i / 5);
        if (modeMessage.get(i)) matrix.set(offset, center - 7);
        if (modeMessage.get(i + 10)) matrix.set(center + 7, offset);
        if (modeMessage.get(29 - i)) matrix.set(offset, center + 7);
        if (modeMessage.get(39 - i)) matrix.set(center - 7, offset);
      }
    }
  }

  /* ===================== 主编码流程 ===================== */
  function encodeBytes(bytes, minECCPercent, userLayers, eci) {
    var bits = highLevelEncode(bytes, eci);

    var eccBits = Math.floor(bits.size() * minECCPercent / 100) + 11;
    var totalSizeBits = bits.size() + eccBits;
    var compact, layers, totalBits, wordSize = 0, stuffedBits = null, i;

    if (userLayers) {
      compact = userLayers < 0;
      layers = Math.abs(userLayers);
      if (layers > (compact ? MAX_LAYERS_COMPACT : MAX_LAYERS)) {
        throw new Error('层数超出范围: ' + userLayers);
      }
      totalBits = totalBitsInLayer(layers, compact);
      wordSize = WORD_SIZE[layers];
      var usableLayers = totalBits - (totalBits % wordSize);
      stuffedBits = stuffBits(bits, wordSize);
      if (stuffedBits.size() + eccBits > usableLayers) {
        throw new Error('数据超出指定层的容量');
      }
      if (compact && stuffedBits.size() > wordSize * 64) {
        throw new Error('紧凑型最多 64 个数据码字');
      }
    } else {
      for (i = 0; ; i++) {
        if (i > MAX_LAYERS) throw new Error('数据过长，超出 Aztec 最大容量');
        compact = i <= 3;
        layers = compact ? i + 1 : i;
        totalBits = totalBitsInLayer(layers, compact);
        if (totalSizeBits > totalBits) continue;
        if (stuffedBits === null || wordSize !== WORD_SIZE[layers]) {
          wordSize = WORD_SIZE[layers];
          stuffedBits = stuffBits(bits, wordSize);
        }
        var usable = totalBits - (totalBits % wordSize);
        if (compact && stuffedBits.size() > wordSize * 64) continue;
        if (stuffedBits.size() + eccBits <= usable) break;
      }
    }

    var messageBits = generateCheckWords(stuffedBits, totalBits, wordSize);
    var messageSizeInWords = stuffedBits.size() / wordSize;
    var modeMessage = generateModeMessage(compact, layers, messageSizeInWords);

    var baseMatrixSize = (compact ? 11 : 14) + layers * 4;
    var alignmentMap = [], matrixSize, k;
    if (compact) {
      matrixSize = baseMatrixSize;
      for (k = 0; k < baseMatrixSize; k++) alignmentMap.push(k);
    } else {
      matrixSize = baseMatrixSize + 1 +
        2 * Math.floor((Math.floor(baseMatrixSize / 2) - 1) / 15);
      var origCenter = Math.floor(baseMatrixSize / 2);
      var center = Math.floor(matrixSize / 2);
      for (k = 0; k < baseMatrixSize; k++) alignmentMap.push(0);
      for (k = 0; k < origCenter; k++) {
        var newOffset = k + Math.floor(k / 15);
        alignmentMap[origCenter - k - 1] = center - newOffset - 1;
        alignmentMap[origCenter + k] = center + newOffset + 1;
      }
    }

    var matrix = new BitMatrix(matrixSize);

    // 数据位：按层从外圈向内螺旋写入四条边
    var rowOffset = 0;
    for (var li = 0; li < layers; li++) {
      var rowSize = (layers - li) * 4 + (compact ? 9 : 12);
      for (var j = 0; j < rowSize; j++) {
        var columnOffset = j * 2;
        for (var kk = 0; kk < 2; kk++) {
          if (messageBits.get(rowOffset + columnOffset + kk)) {
            matrix.set(alignmentMap[li * 2 + kk], alignmentMap[li * 2 + j]);
          }
          if (messageBits.get(rowOffset + rowSize * 2 + columnOffset + kk)) {
            matrix.set(alignmentMap[li * 2 + j], alignmentMap[baseMatrixSize - 1 - li * 2 - kk]);
          }
          if (messageBits.get(rowOffset + rowSize * 4 + columnOffset + kk)) {
            matrix.set(alignmentMap[baseMatrixSize - 1 - li * 2 - kk],
              alignmentMap[baseMatrixSize - 1 - li * 2 - j]);
          }
          if (messageBits.get(rowOffset + rowSize * 6 + columnOffset + kk)) {
            matrix.set(alignmentMap[baseMatrixSize - 1 - li * 2 - j], alignmentMap[li * 2 + kk]);
          }
        }
      }
      rowOffset += rowSize * 8;
    }

    drawModeMessage(matrix, compact, matrixSize, modeMessage);

    if (compact) {
      drawBullsEye(matrix, Math.floor(matrixSize / 2), 5);
    } else {
      drawBullsEye(matrix, Math.floor(matrixSize / 2), 7);
      // 全尺寸符号带参考网格：每隔 16 个模块一条
      for (var a = 0, b = 0; a < Math.floor(baseMatrixSize / 2); a += 15, b += 16) {
        for (var h = Math.floor(matrixSize / 2) & 1; h < matrixSize; h += 2) {
          matrix.set(Math.floor(matrixSize / 2) - b, h);
          matrix.set(Math.floor(matrixSize / 2) + b, h);
          matrix.set(h, Math.floor(matrixSize / 2) - b);
          matrix.set(h, Math.floor(matrixSize / 2) + b);
        }
      }
    }

    var rows = [], y, x;
    for (y = 0; y < matrixSize; y++) {
      var line = [];
      for (x = 0; x < matrixSize; x++) line.push(matrix.get(x, y) ? '1' : '0');
      rows.push(line.join(''));
    }
    return {
      size: matrixSize,
      layers: layers,
      compact: compact,
      codeWords: messageSizeInWords,
      eccPercent: minECCPercent,
      bytes: bytes.length,
      eci: eci,
      rows: rows
    };
  }

  /* ===================== 文本 → 字节 ===================== */
  function isPureAscii(s) {
    for (var i = 0; i < s.length; i++) {
      if (s.charCodeAt(i) > 0x7F) return false;
    }
    return true;
  }

  function asciiBytes(s) {
    var out = [];
    for (var i = 0; i < s.length; i++) out.push(s.charCodeAt(i) & 0xFF);
    return out;
  }

  function utf8Bytes(s) {
    var out = [], i, c;
    for (i = 0; i < s.length; i++) {
      c = s.charCodeAt(i);
      if (c >= 0xD800 && c <= 0xDBFF && i + 1 < s.length) {
        var c2 = s.charCodeAt(i + 1);
        if (c2 >= 0xDC00 && c2 <= 0xDFFF) {
          c = 0x10000 + ((c - 0xD800) << 10) + (c2 - 0xDC00);
          i++;
        }
      }
      if (c < 0x80) {
        out.push(c);
      } else if (c < 0x800) {
        out.push(0xC0 | (c >> 6), 0x80 | (c & 0x3F));
      } else if (c < 0x10000) {
        out.push(0xE0 | (c >> 12), 0x80 | ((c >> 6) & 0x3F), 0x80 | (c & 0x3F));
      } else if (c < 0x200000) {
        out.push(0xF0 | (c >> 18), 0x80 | ((c >> 12) & 0x3F),
          0x80 | ((c >> 6) & 0x3F), 0x80 | (c & 0x3F));
      }
    }
    return out;
  }

  var Aztec = {
    /**
     * 生成 Aztec 符号
     * @param {string} text 文本
     * @param {Object} [opts] { eccPercent: 23|33|50, layers: 0 自动 | ±1..32 }
     * @returns {Object|null} { size, layers, compact, codeWords, eccPercent, rows }
     */
    encode: function (text, opts) {
      var o = opts || {};
      var s = String(text === null || text === undefined ? '' : text);
      if (!s) return null;
      var ecc = Number(o.eccPercent);
      if (!isFinite(ecc) || ecc < 5 || ecc > 95) ecc = 33;
      ecc = Math.round(ecc);
      var layers = Number(o.layers) || 0;
      var bytes, eci = null;
      if (isPureAscii(s)) {
        bytes = asciiBytes(s);
      } else {
        // 非 ASCII 一律 UTF-8 字节 + ECI 26 标记，避免解码端猜错字符集
        bytes = utf8Bytes(s);
        eci = 26;
      }
      return encodeBytes(bytes, ecc, layers, eci);
    },

    // 以下为验证用内部接口（与 ZXing 单元测试向量逐位比对）
    _highLevelBits: function (bytes, eci) {
      return highLevelEncode(bytes, eci === undefined ? null : eci).toBinary();
    },
    _stuffBits: function (bitString, wordSize) {
      var b = new Bits();
      for (var i = 0; i < bitString.length; i++) b.arr.push(bitString.charAt(i) === '1' ? 1 : 0);
      return stuffBits(b, wordSize).toBinary();
    },
    _modeMessage: function (compact, layers, words) {
      return generateModeMessage(compact, layers, words).toBinary();
    },
    _wordSizeTable: WORD_SIZE,
    _asciiBytes: asciiBytes,
    _utf8Bytes: utf8Bytes
  };

  global.Aztec = Aztec;
  if (typeof module !== 'undefined' && module.exports) module.exports = Aztec;
})(typeof window !== 'undefined' ? window : globalThis);
