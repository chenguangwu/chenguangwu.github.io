// 排列/组合“实际方案”共享工具（纯函数，无 DOM 依赖）
(function (global) {
  function parseElements(text) {
    return String(text == null ? '' : text)
      .split(/[\n\r,，、;；\t]+/)
      .map(function (s) { return s.trim(); })
      .filter(function (s) { return s.length > 0; });
  }

  function countsOf(tokens) {
    var map = Object.create(null);
    var order = [];
    tokens.forEach(function (t) {
      if (map[t] == null) { map[t] = 0; order.push(t); }
      map[t] += 1;
    });
    return { keys: order, counts: order.map(function (k) { return map[k]; }) };
  }

  // 去重模式：相同文本只保留一个；按位置模式：重复文本追加 #2/#3 便于区分。
  function tokenNames(tokens, dedupe) {
    if (dedupe) {
      var seen = Object.create(null);
      return tokens.filter(function (t) {
        if (seen[t]) return false;
        seen[t] = 1;
        return true;
      });
    }
    // 位置模式：每项都带独立序号前缀，任何用户文本都无法与另一项标识冲突。
    return tokens.map(function (t, i) {
      return '[' + (i + 1) + '] ' + t;
    });
  }

  function uniqueCombinationCount(tokens, r) {
    var c = countsOf(tokens);
    var memo = Object.create(null);
    function f(i, left) {
      if (left === 0) return 1n;
      if (i >= c.keys.length) return 0n;
      var key = i + '|' + left;
      if (memo[key] != null) return memo[key];
      var total = 0n;
      var max = Math.min(c.counts[i], left);
      for (var take = 0; take <= max; take++) total += f(i + 1, left - take);
      memo[key] = total;
      return total;
    }
    return r < 0 || r > tokens.length ? 0n : f(0, r);
  }

  function uniquePermutationCount(tokens, r) {
    if (r < 0 || r > tokens.length) return 0n;
    var c = countsOf(tokens);
    var memo = Object.create(null);
    function g(counts, left) {
      if (left === 0) return 1n;
      var key = counts.join(',') + '|' + left;
      if (memo[key] != null) return memo[key];
      var total = 0n;
      for (var i = 0; i < counts.length; i++) {
        if (!counts[i]) continue;
        counts[i]--;
        total += g(counts, left - 1);
        counts[i]++;
      }
      memo[key] = total;
      return total;
    }
    return g(c.counts, r);
  }

  // 组合：按位置模式按索引选；去重模式按元素类型选（每种类型取 0..count）。
  function combinationSchemes(tokens, r, dedupe) {
    var out = [];
    if (r < 0 || r > tokens.length) return out;
    if (!dedupe) {
      var names = tokenNames(tokens, false);
      var n = tokens.length;
      (function dfs(start, picked) {
        if (picked.length === r) { out.push(picked.slice()); return; }
        for (var i = start; i <= n - (r - picked.length); i++) {
          picked.push(names[i]);
          dfs(i + 1, picked);
          picked.pop();
        }
      })(0, []);
      return out;
    }
    var c = countsOf(tokens);
    (function dfs(i, left, picked) {
      if (left === 0) { out.push(picked.slice()); return; }
      if (i >= c.keys.length) return;
      var max = Math.min(c.counts[i], left);
      for (var take = 0; take <= max; take++) {
        for (var k = 0; k < take; k++) picked.push(c.keys[i]);
        dfs(i + 1, left - take, picked);
        for (var k2 = 0; k2 < take; k2++) picked.pop();
      }
    })(0, r, []);
    return out;
  }

  // 排列：按位置模式按索引 DFS；去重模式按剩余类型 DFS，天然只产出不重复序列。
  function permutationSchemes(tokens, r, dedupe) {
    var out = [];
    if (r < 0 || r > tokens.length) return out;
    if (!dedupe) {
      var names = tokenNames(tokens, false);
      var used = new Array(tokens.length).fill(false);
      (function dfs(picked) {
        if (picked.length === r) { out.push(picked.slice()); return; }
        for (var i = 0; i < names.length; i++) {
          if (used[i]) continue;
          used[i] = true;
          picked.push(names[i]);
          dfs(picked);
          picked.pop();
          used[i] = false;
        }
      })([]);
      return out;
    }
    var c = countsOf(tokens);
    (function dfs(picked) {
      if (picked.length === r) { out.push(picked.slice()); return; }
      for (var i = 0; i < c.keys.length; i++) {
        if (!c.counts[i]) continue;
        c.counts[i]--;
        picked.push(c.keys[i]);
        dfs(picked);
        picked.pop();
        c.counts[i]++;
      }
    })([]);
    return out;
  }

  global.TBCombinatorics = {
    parseElements: parseElements,
    tokenNames: tokenNames,
    uniqueCombinationCount: uniqueCombinationCount,
    uniquePermutationCount: uniquePermutationCount,
    combinationSchemes: combinationSchemes,
    permutationSchemes: permutationSchemes
  };
})(typeof window !== 'undefined' ? window : globalThis);
