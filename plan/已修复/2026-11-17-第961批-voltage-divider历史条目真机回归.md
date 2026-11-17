# 第 961 批 · voltage-divider 旧 SMS-36/37 真机回归确认

## 来源
`plan/categories/09-自然科学/science-math-statistics.md:23` 的 voltage-divider-calculator「旧 SMS-36～37 待运行回归」。

## 真机回归证据
`scripts/_verify_voltage_divider_961.mjs`（puppeteer-core + 本地 HTTP + 外链 CDN 拦截），5/5 PASS：
- 切「求 R1」页签：目标电压 15V（≥Vin 12V）→ resVout 清空为「—」；目标 0 → 「—」；目标留空 → 「—」（旧 SMS-36/37 升压与空值兜底已修，经 `clearResults` 拦截）。
- 切回「求 Vout」：Vin=12/R1=R2=10000 → Vout=6.000 V（正常）。
- 残余确认：清空 Vin → resVout 仍显示「0.000 V」（`:379-381` 的 `||0` 兜底仍在），非「—」。

## plan 处置
第 23 行由「待运行回归」改为「已修并经真机确认 + 残余（清空 Vin 得 0 V）待改必填校验」。quadratic-equation 的 SMS-136 未做本批真机验证，保持原「待运行回归」不动。

## 门禁
- verify_science_calc.js 240/240；判别器单文件 240/240、逃生 0；脚本语法 OK；git diff --check 干净。
- 本批只 scripts/ 专项脚本 + plan 文档，不进构建产物，不触发部署。

## 状态
本地 commit；距上次 push 时间窗未到，攒批中。
