/* PDF 结构工具：检测表单/书签/链接，重映射内部链接，复制书签树（纯前端，pdf-lib） */
(function (global) {
  'use strict';
  function lib() { return global.PDFLib; }
  function isRef(v) { try { return v instanceof lib().PDFRef; } catch (e) { return false; } }
  function isDict(v) { try { return v instanceof lib().PDFDict; } catch (e) { return false; } }
  function isArray(v) { try { return v instanceof lib().PDFArray; } catch (e) { return false; } }
  function refKey(v) { return isRef(v) ? v.toString() : ''; }
  function name(s) { return lib().PDFName.of(s); }
  function lookupDict(doc, key) { var v = doc.catalog.lookup(name(key)); return isDict(v) ? v : null; }

  function countOutlineChildren(firstRef, ctx) {
    var n = 0, ref = firstRef, guard = 0;
    while (ref && guard++ < 20000) {
      var d = ctx.lookup(ref);
      if (!isDict(d)) break;
      n++;
      n += countOutlineChildren(d.get(name('First')), ctx);
      ref = d.get(name('Next'));
    }
    return n;
  }

  function detect(doc) {
    var out = { forms: 0, outlines: 0, links: 0, internalLinks: 0 };
    try {
      var acro = lookupDict(doc, 'AcroForm');
      if (acro) {
        var fields = acro.get(name('Fields'));
        if (isArray(fields)) out.forms = fields.size();
      }
    } catch (e) { /* 忽略畸形表单 */ }
    try {
      var outlines = lookupDict(doc, 'Outlines');
      if (outlines) out.outlines = countOutlineChildren(outlines.get(name('First')), doc.context);
    } catch (e2) { /* 忽略畸形书签 */ }
    try {
      doc.getPages().forEach(function (page) {
        var annots = page.node.lookup(name('Annots'));
        if (!isArray(annots)) return;
        for (var i = 0; i < annots.size(); i++) {
          var a = annots.lookup(i);
          if (!isDict(a)) continue;
          var sub = a.get(name('Subtype'));
          if (!sub || sub.toString() !== '/Link') continue;
          out.links++;
          var act = a.get(name('A'));
          if (isDict(act) && actionKind(act) === 'internal') out.internalLinks++;
          var dest = a.get(name('Dest'));
          if (dest && destKind(dest) === 'internal') out.internalLinks++;
        }
      });
    } catch (e3) { /* 忽略畸形注释 */ }
    return out;
  }

  function actionKind(action) {
    var s = action.get(name('S'));
    if (!s) return 'other';
    var v = s.toString();
    if (v === '/GoTo') return 'internal';
    if (v === '/URI' || v === '/Launch') return 'external';
    return 'other';
  }

  function destKind(dest) {
    if (isRef(dest)) return 'internal';
    if (isArray(dest)) {
      if (dest.size() === 0) return 'other';
      return isRef(dest.get(0)) ? 'internal' : 'other';
    }
    return 'other';
  }

  function mappedPage(ref, pageMap) {
    var k = refKey(ref);
    if (!k) return null;
    return pageMap.get(k) || null;
  }

  function cloneDestArray(dest, pageMap, ctx) {
    var oldRef = dest.get(0);
    var newRef = mappedPage(oldRef, pageMap);
    if (!newRef) return null;
    var arr = lib().PDFArray.withContext(ctx);
    arr.push(newRef);
    for (var i = 1; i < dest.size(); i++) arr.push(dest.get(i));
    return arr;
  }

  // 修正单个注释的内部跳转；返回 fixed / dropped / unsupported。
  function remapAnnotation(annot, pageMap, ctx) {
    var res = { fixed: 0, dropped: 0, unsupported: 0 };
    var dest = annot.get(name('Dest'));
    if (dest) {
      if (destKind(dest) === 'internal') {
        if (isRef(dest)) {
          var nd = mappedPage(dest, pageMap);
          if (nd) { annot.set(name('Dest'), nd); res.fixed++; }
          else { annot.delete(name('Dest')); res.dropped++; }
        } else {
          var na = cloneDestArray(dest, pageMap, ctx);
          if (na) { annot.set(name('Dest'), na); res.fixed++; }
          else { annot.delete(name('Dest')); res.dropped++; }
        }
      } else { annot.delete(name('Dest')); res.unsupported++; }
    }
    var act = annot.get(name('A'));
    if (isDict(act) && actionKind(act) === 'internal') {
      var d = act.get(name('D'));
      if (destKind(d) === 'internal') {
        if (isRef(d)) {
          var nd2 = mappedPage(d, pageMap);
          if (nd2) { act.set(name('D'), nd2); res.fixed++; }
          else { annot.delete(name('A')); res.dropped++; }
        } else {
          var na2 = cloneDestArray(d, pageMap, ctx);
          if (na2) { act.set(name('D'), na2); res.fixed++; }
          else { annot.delete(name('A')); res.dropped++; }
        }
      } else {
        // 命名目标/页码等无法可靠映射：移除动作，避免指向源文件旧对象。
        annot.delete(name('A'));
        res.unsupported++;
      }
    }
    return res;
  }

  function pageIndexFromDest(srcDoc, dest) {
    if (isRef(dest)) {
      return srcDoc.getPages().findIndex(function (p) { return p.ref.toString() === dest.toString(); });
    }
    if (isArray(dest) && dest.size()) {
      var r = dest.get(0);
      if (isRef(r)) return srcDoc.getPages().findIndex(function (p) { return p.ref.toString() === r.toString(); });
    }
    return -1;
  }

  function newDestArray(srcDest, newPageRef, ctx) {
    var arr = lib().PDFArray.withContext(ctx);
    arr.push(newPageRef);
    if (isArray(srcDest)) {
      for (var i = 1; i < srcDest.size(); i++) arr.push(srcDest.get(i));
    } else {
      arr.push(name('Fit'));
    }
    return arr;
  }

  // 以源页注释为基准重建输出页链接：pdf-lib copyPages 会把链接目标改成输出文档里的错误对象，
  // 不能依赖复制后的 /D；必须回到源注释解析“目标页序号”，再写入正确输出页引用。
  function relinkPages(srcDoc, outDoc, pairs) {
    var out = { fixed: 0, dropped: 0, unsupported: 0, pages: 0 };
    var srcToOut = new Map();
    pairs.forEach(function (pair) { srcToOut.set(pair[0], pair[1]); });
    pairs.forEach(function (pair) {
      var si = pair[0], oi = pair[1];
      var sp = srcDoc.getPage(si), op = outDoc.getPage(oi);
      var sAn = sp.node.lookup(name('Annots'));
      var oAn = op.node.lookup(name('Annots'));
      if (!isArray(sAn) || !isArray(oAn)) return;
      var touched = false;
      var n = Math.min(sAn.size(), oAn.size());
      for (var i = 0; i < n; i++) {
        var sa = sAn.lookup(i), oa = oAn.lookup(i);
        if (!isDict(sa) || !isDict(oa)) continue;
        var sSub = sa.get(name('Subtype'));
        if (!sSub || sSub.toString() !== '/Link') continue;
        var dest = sa.get(name('Dest'));
        if (dest) {
          if (destKind(dest) === 'internal') {
            var di = pageIndexFromDest(srcDoc, dest);
            if (di >= 0 && srcToOut.has(di)) {
              oa.set(name('Dest'), newDestArray(dest, outDoc.getPage(srcToOut.get(di)).ref, outDoc.context));
              out.fixed++; touched = true;
            } else {
              oa.delete(name('Dest')); out.dropped++; touched = true;
            }
          } else { oa.delete(name('Dest')); out.unsupported++; touched = true; }
        }
        var act = sa.get(name('A'));
        if (isDict(act) && actionKind(act) === 'internal') {
          var dd = act.get(name('D'));
          if (destKind(dd) === 'internal') {
            var ti = pageIndexFromDest(srcDoc, dd);
            if (ti >= 0 && srcToOut.has(ti)) {
              var na = lib().PDFDict.withContext(outDoc.context);
              na.set(name('S'), name('GoTo'));
              na.set(name('D'), newDestArray(dd, outDoc.getPage(srcToOut.get(ti)).ref, outDoc.context));
              oa.set(name('A'), na); out.fixed++; touched = true;
            } else {
              oa.delete(name('A')); out.dropped++; touched = true;
            }
          } else {
            oa.delete(name('A')); out.unsupported++; touched = true;
          }
        }
      }
      if (touched) out.pages++;
    });
    return out;
  }

  function remapLinks(doc, pageMap) {
    var out = { fixed: 0, dropped: 0, unsupported: 0, pages: 0 };
    doc.getPages().forEach(function (page) {
      var annots = page.node.lookup(name('Annots'));
      if (!isArray(annots)) return;
      var touched = false;
      for (var i = 0; i < annots.size(); i++) {
        var a = annots.lookup(i);
        if (!isDict(a)) continue;
        var sub = a.get(name('Subtype'));
        if (!sub || sub.toString() !== '/Link') continue;
        var r = remapAnnotation(a, pageMap, doc.context);
        if (r.fixed || r.dropped || r.unsupported) touched = true;
        out.fixed += r.fixed; out.dropped += r.dropped; out.unsupported += r.unsupported;
      }
      if (touched) out.pages++;
    });
    return out;
  }

  function readChildren(firstRef, ctx, depth) {
    var nodes = [], ref = firstRef, guard = 0;
    while (ref && guard++ < 20000) {
      var d = ctx.lookup(ref);
      if (!isDict(d)) break;
      var node = readNode(d, ctx, depth + 1);
      if (node) nodes.push(node);
      ref = d.get(name('Next'));
    }
    return nodes;
  }

  function readNode(d, ctx, depth) {
    if (depth > 64) return null;
    var title = d.get(name('Title'));
    var dest = d.get(name('Dest'));
    var act = d.get(name('A'));
    var kind = 'none', target = null;
    if (dest) {
      if (destKind(dest) === 'internal') {
        kind = 'page';
        target = isRef(dest) ? dest : dest.get(0);
      } else { kind = 'unsupported'; }
    } else if (isDict(act)) {
      var ak = actionKind(act);
      if (ak === 'internal') {
        var dd = act.get(name('D'));
        if (destKind(dd) === 'internal') {
          kind = 'page';
          target = isRef(dd) ? dd : dd.get(0);
        } else { kind = 'unsupported'; }
      } else if (ak === 'external') {
        kind = 'external';
      }
    }
    var countVal = d.get(name('Count'));
    var countSign = 1;
    try { if (countVal && countVal.asNumber && countVal.asNumber() < 0) countSign = -1; } catch (e) {}
    return {
      title: title,
      color: d.get(name('C')),
      flags: d.get(name('F')),
      dest: dest,
      action: act,
      kind: kind,
      target: target,
      countSign: countSign,
      children: readChildren(d.get(name('First')), ctx, depth)
    };
  }

  // 过滤：目标页不在输出文档中的书签删除；其子书签提升到父级，避免整棵子树丢失。
  function filterNodes(nodes, pageMap, stats) {
    var out = [];
    nodes.forEach(function (n) {
      var kids = filterNodes(n.children, pageMap, stats);
      var keep = true;
      if (n.kind === 'page') {
        keep = !!mappedPage(n.target, pageMap);
        if (!keep) stats.dropped++;
      } else if (n.kind === 'unsupported') {
        keep = false;
        stats.dropped++;
      }
      if (keep) {
        out.push({ title: n.title, color: n.color, flags: n.flags, kind: n.kind, dest: n.dest, action: n.action, target: n.target, countSign: n.countSign, children: kids });
      } else {
        kids.forEach(function (k) { out.push(k); });
      }
    });
    return out;
  }

  function writeDest(item, node, pageMap, ctx) {
    if (node.kind === 'page') {
      var nr = mappedPage(node.target, pageMap);
      if (!nr) return false;
      if (isRef(node.dest)) {
        item.set(name('Dest'), nr);
      } else if (isArray(node.dest)) {
        item.set(name('Dest'), cloneDestArray(node.dest, pageMap, ctx));
      } else if (isDict(node.action)) {
        var a = lib().PDFDict.withContext(ctx);
        a.set(name('S'), name('GoTo'));
        var d = node.action.get(name('D'));
        a.set(name('D'), isRef(d) ? nr : cloneDestArray(d, pageMap, ctx));
        item.set(name('A'), a);
      }
      return true;
    }
    if (node.kind === 'external' && isDict(node.action)) {
      var ea = lib().PDFDict.withContext(ctx);
      var s = node.action.get(name('S'));
      if (s) ea.set(name('S'), s);
      var uri = node.action.get(name('URI'));
      if (uri) ea.set(name('URI'), uri);
      item.set(name('A'), ea);
    }
    return true;
  }

  function buildSequence(nodes, parentRef, startPrev, ctx, pageMap) {
    var first = null, last = null, count = 0;
    var prev = startPrev || null;
    nodes.forEach(function (node) {
      var item = lib().PDFDict.withContext(ctx);
      if (node.title) item.set(name('Title'), node.title);
      if (node.color) item.set(name('C'), node.color);
      if (node.flags) item.set(name('F'), node.flags);
      item.set(name('Parent'), parentRef);
      if (prev) item.set(name('Prev'), prev);
      var ref = ctx.register(item);
      if (prev) {
        var pd = ctx.lookup(prev);
        if (isDict(pd)) pd.set(name('Next'), ref);
      }
      if (!first) first = ref;
      var kids = buildSequence(node.children, ref, null, ctx, pageMap);
      if (kids.first) {
        item.set(name('First'), kids.first);
        item.set(name('Last'), kids.last);
      }
      var total = 1 + kids.count;
      if (kids.count > 0) item.set(name('Count'), lib().PDFNumber.of(node.countSign < 0 ? -total : total));
      writeDest(item, node, pageMap, ctx);
      count += total;
      last = ref;
      prev = ref;
    });
    return { first: first, last: last, count: count };
  }

  function appendOutlines(srcDoc, outDoc, pageMap) {
    var srcRoot = lookupDict(srcDoc, 'Outlines');
    var stats = { items: 0, dropped: 0 };
    if (!srcRoot) return stats;
    var nodes = readChildren(srcRoot.get(name('First')), srcDoc.context, 0);
    var filtered = filterNodes(nodes, pageMap, stats);
    if (!filtered.length) return stats;

    var outRoot = lookupDict(outDoc, 'Outlines');
    var rootRef;
    if (!outRoot) {
      outRoot = lib().PDFDict.withContext(outDoc.context);
      outRoot.set(name('Type'), name('Outlines'));
      rootRef = outDoc.context.register(outRoot);
      outDoc.catalog.set(name('Outlines'), rootRef);
    } else {
      rootRef = outDoc.catalog.get(name('Outlines'));
    }
    var prevLast = outRoot.get(name('Last')) || null;
    var built = buildSequence(filtered, rootRef, prevLast, outDoc.context, pageMap);
    if (built.first) {
      if (!outRoot.get(name('First'))) outRoot.set(name('First'), built.first);
      outRoot.set(name('Last'), built.last);
      var oldCount = 0;
      try { var c = outRoot.get(name('Count')); if (c && c.asNumber) oldCount = c.asNumber(); } catch (e) {}
      outRoot.set(name('Count'), lib().PDFNumber.of(oldCount + built.count));
    }
    stats.items += built.count;
    return stats;
  }

  global.PDFStructure = {
    detect: detect,
    remapLinks: remapLinks,
    relinkPages: relinkPages,
    appendOutlines: appendOutlines
  };
})(typeof window !== 'undefined' ? window : globalThis);
