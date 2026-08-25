# ToolBox 工具开发 Workflow 编排说明

> 关联：`PLAN-TOOLS.md`（工具候选池）· `ROADMAP.md` §P3-1（新工具批量开发）
> 文件：`scripts/tool-dev.workflow.js`（script body）

---

## 一、编排拓扑

    候选批次 (batches)
        |
        v
    [phase 1: verify]  每批一个「轻量」agent 校验重复
        |               输出 keep/duplicate（结构化 JSON）
        v
    [phase 2: develop] 每个工具一个 agent 串行开发
        |               使用同一模型（由主调用层配置）
        v
    主 agent 收尾：python3 _build.py → 四道门禁 → commit

**流式无屏障**：两阶段用 `pipeline` 串联，同一批次走完 verify 即可进入 develop，无需等全部批次校验完——省时。

---

## 二、阶段说明（按默认 agent 运行）

> ✅ 当前策略：默认只走 `verify` 与 `develop` 两阶段。
> 阶段模型不在脚本内绑定，使用你当前会话实际可用模型（由主调用层统一控制）。

| Phase | 工作类型 | 模型 | 理由 |
|---|---|---|---|
| verify | 重复校验（grep + 对照） | 当前会话模型 | 轻量机械劳动，快且省 |
| develop | 工具开发（按清单逐项实现） | 当前会话模型 | 统一单模型串行，降低并发波动 |

> 当前版本不再依赖 `meta.json` 外部模型配置；如需切模型，可直接在主模型调用层统一控制（本项目默认以你指定模型执行）。

---

## 三、运行方式

### 1. 传 args（推荐，精确控制批次）

以 workflow 工具运行，`script` 用 `scripts/tool-dev.workflow.js` 的内容，`args` 传：

    {
      "batches": [
        { "id": "batch1-common", "tools": [ { "slug": "...", "name": "...", "industry": "...", "cat": "...", "icon": "...", "bg": "#...", "desc": "...", "spec": "..." } ] }
      ]
    }

### 2. 不传 args（回退默认）

script 内嵌 `DEFAULT_BATCHES`：批次1（4 个通用刚需）+ 批次2（8 个图像/内容/金融），共 12 个候选——均为对话校验剔除重复后的清单。

### 3. 收尾（workflow 结束后，由主 agent 串行执行）

    python3 _build.py
    python3 scripts/check_clarity_refs.py   # 可选：若 _build 未运行，手动快速验收所有页面 Clarity 引用
    python3 _test_static.py
    python3 _audit_links.py --check
    python3 _audit_assets.py --check

四道全绿后 `git add -A && git commit -m "feat(tools): 批次N - xxx"`（索引提交仅提醒用户手动跑 `_submit_indexnow.py`）。

---

## 四、扩展：把 ROADMAP 其他任务也纳入编排

| ROADMAP 任务 | 如何复用本编排 |
|---|---|
| P0-2 C 级工具升级/清理 | 改 `devPrompt` 为「升级指定工具」prompt，batch 传 C 级工具清单 |
| P0-3 B 级补公式升 A | 同上，batch 传 `find_b_formulas.py` 输出的 B 级清单 |
| P2-2 指南扩容 | 改 `devPrompt` 为指南生成 prompt，输出到 guides/ |
| P3-1 后续批次 | 仅换 `args.batches` 为 PLAN-TOOLS 批次3-6 清单 |

核心骨架（verify→develop）为默认流程。若需补充严格人工复核，可在单独步骤外部执行专用审查，不再默认内嵌。

---

## 五、已剔除的重复候选（对话校验结论）

首批规划 10 个通用工具中，4 个经验证与现有 5254 工具重复，已从 `DEFAULT_BATCHES` 剔除：

| 候选 | 重复对象 |
|---|---|
| URL 解码器 | `it/url-encode.html`（URL编码解码工具，已含解码） |
| 税后工资计算器 | `finance/payroll-calculator.html`（工资税后计算器） |
| 中文姓名生成器 | `data/random-5.html` / `biz/name-generator.html` |
| 阅读时长估算 | `edu/reading-speed-calculator.html`（阅读速度计算器） |

> 这也说明：即便双路精查，仍会有遗漏——所以编排里保留了 `verify` 阶段作为**运行时兜底校验**，而非依赖一次性人工核对。
