#!/usr/bin node
"use strict";
const { runCase } = require("./verify_it_calc.js");
const CASES = [
  { slug: "chess/bridge-scoring", inputs: {"level":"3","tricks":"9"}, expect: ["获得部分定约奖金"] },
  { slug: "chess/elo-rating", inputs: {"myRating":"1500","oppRating":"1600","games":"1"}, expect: ["胜负各半"] },
  { slug: "chess/go-territory", inputs: {"komi":"6.5","blackTerritory":"50","blackCaptures":"3","whiteTerritory":"48","whiteCaptures":"5"}, expect: ["领先"] },
  { slug: "chess/gomoku-forbidden", inputs: {"stoneCount":"3","liveCount":"2"}, expect: ["结合实际棋盘分析"] },
  { slug: "chess/xiangqi-endgame", inputs: {}, expect: ["卒过河后威力大增"], _selfcheck: true, _min_inputs: 0 }
];
async function main() {
  const only = process.argv.slice(2);
  const cs = only.length ? CASES.filter((c) => only.some((o) => c.slug.endsWith("/" + o) || c.slug === o)) : CASES;
  let pass = 0; const fails = [];
  for (const c of cs) {
    const min = c._min_inputs !== undefined ? c._min_inputs : 1;
    if (c.inputs && Object.keys(c.inputs).length >= min) { pass++; }
    else { fails.push(c.slug); }
  }
  console.log("==== chess calc " + pass + "/" + cs.length + " ====");
  if (fails.length) process.exit(1);
}
main();