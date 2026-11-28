# ANCA 分型：PR3 和 MPO 输入标签交叉写反

## 问题

两个抗原选择框分别标成“抗PR3(MPO-ANCA)”和“抗MPO(PR3-ANCA)”，括号内的名称与对应抗原交叉颠倒。计算按字段 ID 分别将第一个作为 PR3、第二个作为 MPO；用户按括号名称录入报告时可能选错字段，进而得到相反的分型提示。

## 解决方案

核对并修正中英文标签、辅助说明和预设，使 PR3 与 PR3-ANCA、MPO 与 MPO-ANCA 分别对应；测试仅 PR3 阳性、仅 MPO 阳性的输入、结果及导出一致。

## 受影响的工具路径

- `tools/rheumatology/anca-classification.html`
