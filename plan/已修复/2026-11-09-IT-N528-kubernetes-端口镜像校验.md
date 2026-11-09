# 复核失败重做批次 · 申请再次复核

## IT-N528 Kubernetes 生成器端口和镜像参数仍可生成错误 YAML

**失败点（原复核记录）**
- 页面：`tools/it/kubernetes-yaml-generator.html`
- 复现：端口输入 `80.9` 被静默向下取整输出 `80`，违反 1–65535 整数约束；镜像输入 `#invalid` 被直接写为 `image: #invalid`，YAML 将其视为注释、值为 null；`{}` 也会成为映射而非镜像字符串。

**根因**
- `calcTool()` 端口用 `Math.floor(num('port'))` 静默取整，非整数（如 `80.9`）不报错直接写 `containerPort`；镜像仅校验空白/引号/`: `，未拦截以 `#` 开头（YAML 注释）及 YAML 关键字/空结构（`{}`、`[]`、`null`、`true` 等），导致生成的 YAML 语义错误。

**修复位点**
- `tools/it/kubernetes-yaml-generator.html` `calcTool()`：先取 `portRaw=num('port')`，在既有范围校验前新增 `else if(!Number.isInteger(portRaw))` 整数校验；镜像校验链在既有空白校验前新增：① `/^#/.test(image)` 拒绝注释开头；② `/^(null|true|false|yes|no|on|off|~|\{\}|\[\])$/i.test(image)` 拒绝 YAML 关键字与空结构。

**验证证据**
- `env -u NODE_OPTIONS node scripts/verify_it_calc.js kubernetes-yaml-generator` 全绿（含新增 3 用例）。
- 新增回归用例：`port=80.9` → expect `⚠ 端口须为整数（1~65535，80.9 不被允许）`；`image=#invalid` → expect `⚠ 镜像名不能以 # 开头（YAML 会当作注释）`；`image={}` → expect `⚠ 镜像名不能是 YAML 关键字或空结构`。三者在修复前均原样拼进 YAML（无报错）必红。

**判别力实测**
- 单文件判别器 `node scripts/discriminate_check.js verify_it_calc.js`：1330 用例已检、正确变红 1330、逃生项 0。三用例锚各自独立错误提示串，输入为 `80.9`/`#invalid`/`{}`、输出为校验告警 ⇒ 非回显；合法默认 `nginx:latest`/`80` 不触发这些提示，强判别、零逃生。
