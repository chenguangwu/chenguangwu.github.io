# 物理/光学/量子 · tools/{physics 类目录,astronomy,optics,quantum,kinematics,dynamics,thermodynamics,acoustics,fluid}（~250 页）

## 受影响范围
- tools/optics/（40）、tools/quantum/（28）、tools/astronomy/、tools/kinematics/、tools/dynamics/、tools/thermodynamics/、tools/acoustics/（56）、tools/fluid/、tools/optical/（40）（~250 页）

## 进度
- 🔴 待开发

## 2026-11-03 续查（并行批 I）

### PQ-10 电子质量常数与引据标称版本不一致（低，待验证）
- 描述：多个量子页使用 `ME=9.10938356e-31`（CODATA 2014），而引据表标称 CODATA 2018（2018 值为 9.1093837015e-31），属引据一致性问题；因显示位数有限，当前输出看不出差异。
- 证据：`tools/quantum/compton-shift.html:210`、`tools/quantum/infinite-well-energy.html:272`、`tools/quantum/pair-production-threshold.html:212`（均 `ME=9.10938356e-31`）；`tools/quantum/compton-shift.html:156` 引据行写「CODATA 2018」。node 复算：λ_C = 2.426310 pm（2014 与 2018 在 6 位小数处相同，相对差异 1.55e-6 %）；阈值 1.0220 MeV（4 位小数相同）。
- 影响：`tools/quantum/compton-shift.html`、`infinite-well-energy.html`、`pair-production-threshold.html`，当前显示值不受影响，但引据与实现版本不符，后续提高精度或换位数时会暴露。
- 方案：统一把电子质量换成 CODATA 2018 值并在引据表注明取值年份；或把引据表改标 CODATA 2014，二者取其一，避免「标称 2018、实算 2014」。

### 留存优化
- 2026-11-06 复核：无限深势阱和单缝衍射已引入共用校验，不应再把旧结构描述为全部 8 页的现状。
- 原 `infinite-well-energy` 和 `single-slit-diffraction` 零值预设已替换；建议继续复核其他页面。
- `__tbInputGuard` 的 `__D` 由「真浏览器逐项置零探测」生成，本批已见过度收录（`young-fringe` 把分子当分母）与完全为空（`brewster-angle`）两种失真；建议改为人工按公式分母维护并加注释。
- 常量与引据：本批 4 个量子页重复声明同一组常量（H/C/ME/EV/A0/RY/B_WIEN），其中 A0、RY、B_WIEN 多数页未使用；可收敛为共享常量表，同时统一到 CODATA 2018。

### 续查覆盖
- 本批实查 8 页：`tools/optics/malus-law.html`、`brewster-angle.html`、`young-fringe.html`、`single-slit-diffraction.html`、`tools/quantum/compton-shift.html`、`infinite-well-energy.html`、`zeeman-splitting.html`、`pair-production-threshold.html`。
- 前批已覆盖（本批未重复）：`tools/optics/snells-law.html`、`prism-deviation.html`、`tools/quantum/rydberg-wavelength.html`、`photoelectric-effect.html`。
- 方法：仅静态阅读源码 + node 内存复算（输入→输出逐条记录如上）；**未**开浏览器、未做英文态/繁体态、未做移动端、未跑 `_build.py`/`run_gates.py` 或任何门禁，也未验证线上表现。
- 未覆盖：`tools/optics` 余 15 页、`tools/quantum` 余 21 页、`tools/optical`(41)、`tools/astronomy`(24) 及 `tools/kinematics|dynamics|thermodynamics|acoustics|fluid`，留待后续批次。

## X 批 · 物理/光学（2026-11-04）

- 2026-11-06 复核 PQ-11～22：除 PQ-14 的空值主区和旧表问题已修、仍有图表问题外，其余问题对应源码分支仍在；PQ-19 已修正原记录对超光速相速度的物理表述。此次为源码复核，未做浏览器验证。
- 2026-11-17 第 1022 批真机销账：PQ-11（多普勒 vo/vs 负值）、PQ-12（球面镜 f<0 凸面镜）、PQ-15（磁通量反解漏 cosθ）已修并 verify+判别器确认。
- 2026-11-17 第 1023 批真机销账：PQ-20（球面镜 f=0 分母守卫，`__D` 加 f）已修并 verify+判别器确认；其余 PQ 条目仍待处理。

### PQ-14 重力势能空值错误态仍会重画伪图（中，确认源码缺陷）
- 2026-11-06 复核：`tools/science/gravitational-potential.html:215-240,254-260` 主区已有必填守卫，错误时清空表格和图表，明细遇空值返回；原「主区 0、旧表保留」描述已不成立。
- 但 `:331-348,366` 的外层包装器在主区返回后仍调用图表函数；`__gvptSweep()` 经 `num()` 把空值按 0 计算，因此清空高度后仍会重画零势能及零高度曲线。仅源码推导，未做浏览器验证。
- 「高度复算」仍为同一输入推回，且 m·g=0 时分母兜底为 1，不能作为独立指标。方案：图表与主区共用输入校验，空值停止绘制；复算项标明校验性质或删除。

### PQ-16 折射定律入射角未限幅，100°/负角被当合法（中，确认）
- 描述：θ₁ 不经任何范围校验就投入 `sin`，大于 90° 或负值按三角函数周期继续计算，输出看似正常的折射角。
- 证据：`tools/science/physics-calculator.html:449-457`（`:451` 直接 `Math.sin(theta1.v*π/180)`，`:457` 反解 θ₁ 亦无校验）。node 复算：n₁=1、n₂=1.5、θ₁=100° → θ₂=41.036°；θ₁=−30° → θ₂=−19.471°。
- 影响：`tools/science/physics-calculator.html`，物理上不存在的入射角被接受，折射角与临界角判断随之失真。
- 方案：限定 0°≤θ₁≤90°（含 90° 边界），越界明确提示；θ₂ 同理限定 0–90°。

### PQ-17 光电效应低于阈值仍显示负的「最大初动能」（中，确认）
- 描述：`Eₖₘₐₓ = hf − W₀` 不做阈值判断，hf<W₀ 时把负值照常标成最大初动能。
- 证据：`tools/science/physics-calculator.html:496-500`（`:498` 直接 `hval*f.v-W0.v`）。node 复算：f=1e14 Hz、W₀=2 eV（3.204e-19 J）→ −2.542e-19 J，页面仍显示为「最大初动能」。
- 影响：`tools/science/physics-calculator.html`，低于阈频时给出负动能，概念误导（与前一页 photoelectric-effect 同类缺陷）。
- 方案：hf<W₀ 时显示「无光电子逸出，最大初动能不适用」，若展示 hf−W₀ 须另命名并注明为有符号能量差。

### PQ-18 薄透镜在 d_o=f 时输出「—/-—」与 Infinity 明细（中，确认）
- 描述：守卫只拦截 f=0、d_o=0，未处理 d_o=f；此时像距发散，主区字符串被 `/Infinity/` 替换成「—-」，明细/CSV 保留原始 `Infinity`，SVG 坐标被钳到边界但仍按无穷放大率绘制。
- 证据：`tools/optics/thin-lens-equation.html:239`（`__D` 仅判等于 0）、`:284`（`di=1/(1/f-1/do)`）、`:302`（`calcRay` 同式）、`:319-320`（`xI=xL+di*scale` 后钳位）。node 复算：f=0.1、d_o=0.1 → d_i=Infinity、m=−Infinity，`toFixed(4)` 得到字符串 `Infinity`。
- 影响：`tools/optics/thin-lens-equation.html`，物距等于焦距（成像于无穷远，物理上合法）时出现「像距 —、放大率 -—、像性质 实像」的分裂显示，光路图失真。
- 方案：|d_o−f| 小于阈值时判「成像在无穷远」，清空像距/放大率/光路图并提示；明细与 CSV 走同一状态分支。

### PQ-19 折射率页允许介质光速超过真空光速，n<1 与 3×10¹⁷ 联动值（中，确认）
- 描述：只拦截 v=0，不校验 v≤c；v>c 时 n<1、v 为负时 n 为负，「速度差与光速之比倒数」又用 `max(c−v,1e-9)` 兜底，输出天文数字。
- 证据：`tools/optics/refractive-index-speed.html:268`（`__D` 只含 v）、`:301-306`（n=c/v 与 `c/Math.max(c-v,1e-9)`）、`:386`（FAQ 自己承认 n<1 说明输入有误）。node 复算：v=4e8、c=3e8 → n=0.7500、末项 3e17。
- 2026-11-06 复核：上述代码仍在；负速度、非正真空光速及 `Math.max` 强行兜底会产生错误结果。介质中相速度在特殊色散条件下可超过真空光速，不能笼统以狭义相对论排除 n<1；需明确本页是否限定普通透明介质的相速度模型。
- 方案：要求正且有限的速度，明确适用模型和 c 的物理含义；针对 c−v=0 或负值不要用正数兜底伪造结果，可删除该联动量或改为明确有物理意义的 n−1。仅源码复核，未做浏览器验证。

### PQ-21 多普勒在 v_s=v 时主区「—」、明细/CSV 为 Infinity（中，确认）
- 描述：分母 `v−vs` 为 0 时没有任何守卫（`__D` 为空对象），主区字符串被替换成「—」，明细表与导出却保留字符串 `Infinity`，Δf 同样失效。
- 证据：`tools/science/doppler-effect.html:242`（`var __D={}`）、`:287-290`（fp 与 Δf）、`:311-313`（明细同式）。node 复算：f=1000、v=343、vo=0、vs=343 → fp=Infinity。
- 影响：`tools/science/doppler-effect.html`，波源速度达到波速时页面既无物理解释，又出现主区与明细互相矛盾的输出。
- 方案：vs≥v 时提示「波源速度不能达到或超过波速」并停算；明细/导出与主区共用同一校验结果。

### 覆盖
- 本批实查 8 页：`tools/science/physics-calculator.html`、`gravitational-potential.html`、`spring-oscillation-period.html`、`doppler-effect.html`、`tools/quantum/photon-energy.html`、`tools/optics/thin-lens-equation.html`、`mirror-equation.html`、`refractive-index-speed.html`。
- 页面名替换说明：`tools/physics/` 目录不存在，8 页实际分布在 `tools/science`（4）、`tools/quantum`（1）、`tools/optics`（3）；清单中的 `lens-equation`、`ray-optics`、`refraction-angle` 在仓库中无同名页，按「同目录顺延未审计页」分别取 `thin-lens-equation`、`mirror-equation`、`refractive-index-speed`（`snells-law` 已在前批覆盖，故未重复）。
- `spring-oscillation-period.html` 本批未发现符合入账口径的缺陷（仅 `__D` 把分子 m 误标为「分母」的文案问题，属低危，未计入编号）。
- 方法：仅静态读源码 + node 内存复算（关键输入→输出已逐条记录）；**未**开浏览器、未做英文态/繁体态与移动端、未跑 `_build.py`/`run_gates.py` 或任何门禁，也未验证线上表现。
