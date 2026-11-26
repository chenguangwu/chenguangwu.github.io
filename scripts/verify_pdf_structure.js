#!/usr/bin/env node
'use strict';
/*
 * PDF 结构保持回归：书签树、内部页内跳转、外部 URL、表单展平。
 * 直接加载 vendor/pdf-lib 与 js/tools/pdf-structure.js（无浏览器依赖）。
 */
const assert = require('assert');
const fs = require('fs');
const path = require('path');
const vm = require('vm');
const PDFLib = require('../vendor/pdf-lib/1.17.1/pdf-lib.min.js');
const { PDFDocument, PDFName, PDFArray, PDFDict, PDFString, PDFNumber } = PDFLib;

const ctx = { PDFLib, console };
vm.createContext(ctx);
vm.runInContext(fs.readFileSync(path.join(__dirname, '..', 'js/tools/pdf-structure.js'), 'utf8'), ctx);
const PDFStructure = ctx.PDFStructure;

function addLink(doc, page, opts) {
  const c = doc.context;
  const annot = PDFDict.withContext(c);
  annot.set(PDFName.of('Type'), PDFName.of('Annot'));
  annot.set(PDFName.of('Subtype'), PDFName.of('Link'));
  const rect = PDFArray.withContext(c);
  [40, 40, 120, 80].forEach(function (n) { rect.push(PDFNumber.of(n)); });
  annot.set(PDFName.of('Rect'), rect);
  if (opts.uri) {
    const action = PDFDict.withContext(c);
    action.set(PDFName.of('S'), PDFName.of('URI'));
    action.set(PDFName.of('URI'), PDFString.of(opts.uri));
    annot.set(PDFName.of('A'), action);
  } else {
    const action = PDFDict.withContext(c);
    action.set(PDFName.of('S'), PDFName.of('GoTo'));
    const dest = PDFArray.withContext(c);
    dest.push(opts.target.ref);
    dest.push(PDFName.of('Fit'));
    action.set(PDFName.of('D'), dest);
    annot.set(PDFName.of('A'), action);
  }
  let annots = page.node.lookup(PDFName.of('Annots'));
  if (!annots) {
    annots = PDFArray.withContext(c);
    page.node.set(PDFName.of('Annots'), annots);
  }
  annots.push(c.register(annot));
}

function addOutlineTree(doc, items) {
  const c = doc.context;
  const root = PDFDict.withContext(c);
  root.set(PDFName.of('Type'), PDFName.of('Outlines'));
  const rootRef = c.register(root);

  function build(list, parent) {
    let prev = null, first = null, last = null, count = 0;
    list.forEach(function (item) {
      const node = PDFDict.withContext(c);
      node.set(PDFName.of('Title'), PDFString.of(item.title));
      node.set(PDFName.of('Parent'), parent);
      if (item.target) {
        const dest = PDFArray.withContext(c);
        dest.push(item.target.ref);
        dest.push(PDFName.of('Fit'));
        node.set(PDFName.of('Dest'), dest);
      }
      if (prev) prev.set(PDFName.of('Next'), c.register(node));
      const ref = c.register(node);
      if (!first) first = ref;
      let childCount = 0;
      if (item.children && item.children.length) {
        const kids = build(item.children, ref);
        node.set(PDFName.of('First'), kids.first);
        node.set(PDFName.of('Last'), kids.last);
        node.set(PDFName.of('Count'), PDFNumber.of(kids.count));
        childCount = kids.count;
      }
      count += 1 + childCount;
      last = ref;
      prev = node;
    });
    return { first: first, last: last, count: count };
  }

  const built = build(items, rootRef);
  root.set(PDFName.of('First'), built.first);
  root.set(PDFName.of('Last'), built.last);
  root.set(PDFName.of('Count'), PDFNumber.of(built.count));
  doc.catalog.set(PDFName.of('Outlines'), rootRef);
}

async function makeSource() {
  const doc = await PDFDocument.create();
  const p1 = doc.addPage([300, 300]);
  const p2 = doc.addPage([300, 300]);
  const p3 = doc.addPage([300, 300]);
  addLink(doc, p1, { target: p2 });
  addLink(doc, p1, { target: p3 });
  addLink(doc, p1, { uri: 'https://example.com/pdf' });
  addOutlineTree(doc, [
    { title: 'Chapter 1', target: p1, children: [
      { title: 'Sub 1.1', target: p2 },
      { title: 'Sub 1.2', target: p3 }
    ] },
    { title: 'Chapter 2', target: p2 }
  ]);
  const form = doc.getForm();
  [
    ['name1', 'Alice', 200],
    ['name2', 'Bob', 170],
    ['note1', 'Hello PDF', 140]
  ].forEach(function (item) {
    const field = form.createTextField(item[0]);
    field.setText(item[1]);
    field.addToPage(p1, { x: 40, y: item[2], width: 150, height: 24 });
    field.setText(item[1]);
  });
  return doc;
}

function outlineTitles(doc) {
  const result = [];
  const root = doc.catalog.lookup(PDFName.of('Outlines'));
  function walk(dict, depth) {
    if (!dict) return;
    let ref = dict.get(PDFName.of('First'));
    let guard = 0;
    while (ref && guard++ < 2000) {
      const node = doc.context.lookup(ref);
      if (!node || !node.get(PDFName.of('Title'))) break;
      result.push('  '.repeat(depth) + node.get(PDFName.of('Title')).decodeText());
      walk(node, depth + 1);
      ref = node.get(PDFName.of('Next'));
    }
  }
  walk(root, 0);
  return result;
}

function pageLinks(doc, pageIndex) {
  const page = doc.getPage(pageIndex);
  const annots = page.node.lookup(PDFName.of('Annots'));
  const links = [];
  if (!annots) return links;
  for (let i = 0; i < annots.size(); i++) {
    const annot = doc.context.lookup(annots.get(i));
    if (!annot) continue;
    const action = annot.get(PDFName.of('A'));
    if (action) {
      const s = action.get(PDFName.of('S'));
      const kind = s ? s.toString() : '';
      if (kind === '/GoTo') {
        const dest = action.get(PDFName.of('D'));
        links.push({ kind: 'goto', ref: dest ? dest.get(0).toString() : null });
      } else if (kind === '/URI') {
        const uri = action.get(PDFName.of('URI'));
        links.push({ kind: 'uri', uri: uri ? uri.decodeText() : null });
      }
    }
  }
  return links;
}

(async function () {
  let passed = 0;
  function ok(name) { passed++; console.log('ok ' + name); }

  const src = await makeSource();
  const detected = PDFStructure.detect(src);
  assert.deepStrictEqual(JSON.parse(JSON.stringify(detected)), { forms: 3, outlines: 4, links: 3, internalLinks: 2 });
  ok('detect forms/outlines/links');

  const merged = await PDFDocument.create();
  src.getForm().flatten();
  const copied = await merged.copyPages(src, src.getPageIndices());
  const pairs = [];
  copied.forEach(function (page, i) {
    merged.addPage(page);
    pairs.push([i, merged.getPageCount() - 1]);
  });
  const mergeLinks = PDFStructure.relinkPages(src, merged, pairs);
  assert.deepStrictEqual(JSON.parse(JSON.stringify(mergeLinks)), { fixed: 2, dropped: 0, unsupported: 0, pages: 1 });
  const pageMap = new Map();
  src.getPages().forEach(function (page, i) { pageMap.set(page.ref.toString(), copied[i].ref); });
  const mergeOutlines = PDFStructure.appendOutlines(src, merged, pageMap);
  assert.deepStrictEqual(JSON.parse(JSON.stringify(mergeOutlines)), { items: 4, dropped: 0 });
  assert.deepStrictEqual(outlineTitles(merged), [
    'Chapter 1', '  Sub 1.1', '  Sub 1.2', 'Chapter 2'
  ]);
  assert.deepStrictEqual(pageLinks(merged, 0).filter(function (l) { return l.kind === 'goto'; }).map(function (l) { return l.ref; }),
    [merged.getPage(1).ref.toString(), merged.getPage(2).ref.toString()]);
  assert.strictEqual(pageLinks(merged, 0).filter(function (l) { return l.kind === 'uri'; })[0].uri, 'https://example.com/pdf');
  assert.strictEqual(PDFStructure.detect(merged).forms, 0);
  ok('merge keeps nested outlines and rewrites internal links');

  const splitDoc = await makeSource();
  splitDoc.getForm().flatten();
  const split = await PDFDocument.create();
  const selected = [0, 2];
  const splitCopied = await split.copyPages(splitDoc, selected);
  const splitPairs = [];
  splitCopied.forEach(function (page, i) {
    split.addPage(page);
    splitPairs.push([selected[i], split.getPageCount() - 1]);
  });
  const splitLinks = PDFStructure.relinkPages(splitDoc, split, splitPairs);
  assert.deepStrictEqual(JSON.parse(JSON.stringify(splitLinks)), { fixed: 1, dropped: 1, unsupported: 0, pages: 1 });
  const splitMap = new Map();
  splitPairs.forEach(function (pair) {
    splitMap.set(splitDoc.getPage(pair[0]).ref.toString(), split.getPage(pair[1]).ref);
  });
  const splitOutlines = PDFStructure.appendOutlines(splitDoc, split, splitMap);
  assert.deepStrictEqual(JSON.parse(JSON.stringify(splitOutlines)), { items: 2, dropped: 2 });
  assert.deepStrictEqual(outlineTitles(split), ['Chapter 1', '  Sub 1.2']);
  assert.strictEqual(PDFStructure.detect(split).internalLinks, 1);
  assert.strictEqual(pageLinks(split, 0).filter(function (l) { return l.kind === 'uri'; })[0].uri, 'https://example.com/pdf');
  ok('split drops out-of-range targets, promotes child, keeps external URI');

  const reordered = await PDFDocument.create();
  const bDoc = await PDFDocument.create();
  const bPage = bDoc.addPage([300, 300]);
  addOutlineTree(bDoc, [{ title: 'Part B', target: bPage }]);
  const bCopied = await reordered.copyPages(bDoc, bDoc.getPageIndices());
  const bPairs = [];
  bCopied.forEach(function (page, i) { reordered.addPage(page); bPairs.push([i, reordered.getPageCount() - 1]); });
  PDFStructure.relinkPages(bDoc, reordered, bPairs);
  PDFStructure.appendOutlines(bDoc, reordered, new Map([[bPage.ref.toString(), bCopied[0].ref]]));
  const aCopied = await reordered.copyPages(src, src.getPageIndices());
  const aPairs = [];
  aCopied.forEach(function (page, i) { reordered.addPage(page); aPairs.push([i, reordered.getPageCount() - 1]); });
  PDFStructure.relinkPages(src, reordered, aPairs);
  const aMap = new Map();
  src.getPages().forEach(function (page, i) { aMap.set(page.ref.toString(), aCopied[i].ref); });
  PDFStructure.appendOutlines(src, reordered, aMap);
  assert.deepStrictEqual(outlineTitles(reordered), ['Part B', 'Chapter 1', '  Sub 1.1', '  Sub 1.2', 'Chapter 2']);
  assert.deepStrictEqual(pageLinks(reordered, 1).filter(function (l) { return l.kind === 'goto'; }).map(function (l) { return l.ref; }),
    [reordered.getPage(2).ref.toString(), reordered.getPage(3).ref.toString()]);
  ok('merge file reorder keeps link targets and outline order');

  const dup = await PDFDocument.create();
  const dupCopied = await dup.copyPages(src, [0, 0, 2]);
  const dupPairs = [];
  dupCopied.forEach(function (page, i) { dup.addPage(page); dupPairs.push([[0, 0, 2][i], dup.getPageCount() - 1]); });
  PDFStructure.relinkPages(src, dup, dupPairs);
  assert.strictEqual(dup.getPageCount(), 3);
  const dupMap = new Map();
  dupPairs.forEach(function (pair) { dupMap.set(src.getPage(pair[0]).ref.toString(), dup.getPage(pair[1]).ref); });
  PDFStructure.appendOutlines(src, dup, dupMap);
  assert.deepStrictEqual(outlineTitles(dup), ['Chapter 1', '  Sub 1.2']);
  ok('duplicate source pages keep output valid');

  console.log('PDF structure: ' + passed + '/5 passed');
})().catch(function (err) {
  console.error(err && err.stack || err);
  process.exit(1);
});
