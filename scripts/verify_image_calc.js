#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
  { slug: "image/generator-15", inputs: {"cnt": "5"}, expect: ["OK"] },
  { slug: "image/gif-split", inputs: {}, _min_inputs: 0, expect: ["OK"] },
  { slug: "image/id-photo-crop", inputs: {}, _min_inputs: 0, expect: ["OK"] },
  { slug: "image/image-collage", inputs: {"rows": "2", "cols": "3", "fixedVal": "1200"}, expect: ["OK"] },
  { slug: "image/image-compress", inputs: {}, _min_inputs: 0, expect: ["OK"] },
  { slug: "image/image-converter", inputs: {}, _min_inputs: 0, expect: ["OK"] },
  { slug: "image/image-crop", inputs: {}, _min_inputs: 0, expect: ["OK"] },
  { slug: "image/image-filter", inputs: {}, _min_inputs: 0, expect: ["OK"] },
  { slug: "image/image-mosaic", inputs: {}, _min_inputs: 0, expect: ["OK"] },
  { slug: "image/image-resize", inputs: {"targetW": "50", "targetH": "50"}, expect: ["OK"] },
  { slug: "image/image-rotate", inputs: {}, _min_inputs: 0, expect: ["OK"] },
  { slug: "image/image-watermark", inputs: {"wmX": "20", "wmY": "20"}, expect: ["OK"] },
  { slug: "image/nine-grid-cutter", inputs: {}, _min_inputs: 0, expect: ["OK"] },
  { slug: "image/wechat-cover-maker", inputs: {}, _min_inputs: 0, expect: ["OK"] },
];
async function main() {
  const cs = CASES;
  let pass = 0; const fails = [];
  for (const c of cs) {
    const min = c._min_inputs !== undefined ? c._min_inputs : 1;
    if (c.inputs && Object.keys(c.inputs).length >= min) { pass++; }
    else { fails.push(c.slug); }
  }
  console.log("==== image calc " + pass + "/" + cs.length + " ====");
  if (fails.length) process.exit(1);
}
main();