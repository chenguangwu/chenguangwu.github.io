#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""robotics 分类 deep-dive 真实化：用真实机器人运动/动力学算例替换占位/弱泛化内容。"""
import json, re, os

F = 'i18n/tools/content_deepdive.json'
BAD_RE = re.compile(
    r'统一复核|降低上手门槛|可追溯流程|边界样本建议单独标注|减少重复确认成本|'
    r'标准化，再批量|可复核输出|沿用模板逐项核对|形成标准复核清单|统一口径|快速复核|'
    r'高频复用模板|在.{1,20}(业务|场景)里，优先把.{1,40}标准化后再执行|复用模板示例|'
    r'保留复用模板|先按业务口径补充必要字段|运行工具并记录输出|对比另一组边界输入|'
    r'先用一组可复现输入|同一输入样本测试默认和边界情况|选择两组不同来源样本并同步口径定义'
)

KB = {
'robotics/accel-distance': {
  'title': '匀减速制动距离',
  'scenarios': [
    '移动机器人安全停车距离。',
    '给定末速与减速度的位移。',
    '避障急停设计。'],
  'examples': [
    {'title': '2m/s 减速度 1m/s² 到停', 'body': 'd=v²/(2a)=4/2=2m；以 2m/s 匀减速到停需 2m 制动距离。'},
    {'title': '减速度加倍', 'body': 'a=2 时 d=4/4=1m，减速度越大停距越短。'}],
  'faqs': [
    {'q': '公式前提？', 'a': '匀减速且末速为 0；初速 v、减速度 a 恒定。'},
    {'q': '反应时间算吗？', 'a': '本式仅制动段，总停距须另加反应延迟位移 v·t_react。'}]},

'robotics/battery-runtime': {
  'title': '电池续航时间',
  'scenarios': [
    '移动机器人续航估算。',
    '容量-电压-功率换算。',
    '任务规划电源匹配。'],
  'examples': [
    {'title': '12V 2Ah 供 24W', 'body': 't=Ah·V/P=2×12/24=1h；电池能量 24Wh 供 24W 负载可用 1 小时。'},
    {'title': '负载降到 12W', 'body': 't=24/12=2h，功耗减半续航翻倍。'}],
  'faqs': [
    {'q': 'Wh 与 Ah 关系？', 'a': '能量 Wh=Ah×V；续航=Wh/P。'},
    {'q': '实际会打折吗？', 'a': '会；放电倍率、温度、老化使可用容量低于标称。'}]},

'robotics/belt-linear-speed': {
  'title': '带轮线速度',
  'scenarios': [
    '传送带/同步带速度。',
    '轮径与转速换算。',
    '末端进给速度。'],
  'examples': [
    {'title': '直径 60mm、300rpm', 'body': 'v=π·D·n/60=π×0.06×300/60=0.942 m/s。'},
    {'title': '直径加倍', 'body': 'D=0.12 → v=1.885 m/s，线速与直径成正比。'}],
  'faqs': [
    {'q': '单位', 'a': 'D 取米、n 取 rpm，结果 m/s；也可直接 v=πDn（n 为 rps）。'},
    {'q': '打滑影响？', 'a': '同步带近似不打滑；平带需乘滑差系数。'}]},

'robotics/cable-tension-pulley': {
  'title': '滑轮绳张力',
  'scenarios': [
    '定滑轮两侧张力。',
    '悬挂载荷缆绳受力。',
    '配重系统张力。'],
  'examples': [
    {'title': '100N 载荷过定滑轮', 'body': '理想定滑轮无摩擦，两侧张力均 T=F/2=50N（两侧共承 100N）。'},
    {'title': '含摩擦', 'body': '实际有摩擦时两侧不等，须按效率修正。'}],
  'faqs': [
    {'q': '为何各 50N？', 'a': '静力平衡下两侧张力相等且和为 100N，故各 50N。'},
    {'q': '动滑轮呢？', 'a': '动滑轮可省力一半，张力=载荷/2 承担。'}]},

'robotics/centripetal-speed-limit': {
  'title': '转弯限速',
  'scenarios': [
    '差速机器人转弯最大速。',
    '给定向心加速度上限。',
    '防侧翻/打滑速度。'],
  'examples': [
    {'title': '半径 1m、a_max=2m/s²', 'body': 'v=√(a_max·R)=√(2×1)=1.41 m/s，超过则向心加速度超限。'},
    {'title': '半径减半', 'body': 'R=0.5 → v=1.0 m/s，限速随半径平方根下降。'}],
  'faqs': [
    {'q': 'a_max 取多少？', 'a': '依打滑（μg）或侧翻阈值定，常取 1–3 m/s²。'},
    {'q': '与角速度？', 'a': 'v=ωR，亦可写为 ω_max=√(a_max/R)。'}]},

'robotics/dc-motor-back-emf': {
  'title': '直流电机反电动势',
  'scenarios': [
    '电机转速反推电压。',
    '反电动势常数应用。',
    '空载转速估算。'],
  'examples': [
    {'title': '常数 0.05、转速 100rad/s', 'body': 'E=k_e·ω=0.05×100=5V；转速越高反电动势越大，限制电流。'},
    {'title': '转速 200', 'body': 'E=10V，反电动势接近供电电压时电流趋小。'}],
  'faqs': [
    {'q': '反电动势作用？', 'a': '与供电反向，E 升高使电枢电流 I=(U−E)/R 下降，自然限速。'},
    {'q': 'k_e 单位？', 'a': 'V·s/rad（或 V/rpm 需换算），由电机设计决定。'}]},

'robotics/diff-drive-velocity': {
  'title': '差速驱动线/角速度',
  'scenarios': [
    '两轮差速底盘运动学。',
    '左右轮速求位姿变化率。',
    '里程计基础。'],
  'examples': [
    {'title': '左 0.5、右 1.0 m/s、轮距 0.4m', 'body': 'v=(vl+vr)/2=0.75 m/s，ω=(vr−vl)/L=0.5/0.4=1.25 rad/s。'},
    {'title': '等速直行', 'body': 'vl=vr → ω=0，纯平移；反向则原地旋转。'}],
  'faqs': [
    {'q': '轮距 L？', 'a': '两驱动轮间距离；ω=(vr−vl)/L。'},
    {'q': '与里程计关系？', 'a': '位移 ds=(vl+vr)/2·dt、转 dθ=(vr−vl)/L·dt。'}]},

'robotics/encoder-angle-resolution': {
  'title': '编码器角度分辨率',
  'scenarios': [
    '正交编码角度细分。',
    'CPR 与分辨率换算。',
    '位置控制精度评估。'],
  'examples': [
    {'title': '1000 CPR', 'body': 'θ=360/(4×CPR)=360/4000=0.09°；正交 4 倍频后每转 4000 计数。'},
    {'title': '4000 CPR', 'body': 'θ=360/16000=0.0225°，分辨率随 CPR 升高。'}],
  'faqs': [
    {'q': '为何除以 4？', 'a': 'A/B 两相正交各边沿计数，共 4 倍频。'},
    {'q': '与步距角区别？', 'a': '编码器是反馈分辨率，步进是开环步距，二者不同。'}]},

'robotics/end-effector-reach': {
  'title': '机械臂可达工作空间',
  'scenarios': [
    '二连杆可达半径范围。',
    '目标点可达性初判。',
    '工作空间规划。'],
  'examples': [
    {'title': '臂长 1m 与 0.8m', 'body': 'r_min=|1−0.8|=0.2m，r_max=1+0.8=1.8m；末端可达距基座 0.2–1.8m 圆环内。'},
    {'title': '等长 1m', 'body': 'r_min=0（可折叠到基座）、r_max=2m。'}],
  'faqs': [
    {'q': '仅半径够吗？', 'a': '平面二连杆为圆环；含关节限位或三维则为更复杂空间。'},
    {'q': '奇异点？', 'a': '完全伸展(r_max)或折叠(r_min)附近雅可比退化，需避开。'}]},

'robotics/forward-kinematics-2r': {
  'title': '二连杆正运动学',
  'scenarios': [
    '已知关节角求末端坐标。',
    '平面 2R 机械臂。',
    '轨迹点位计算。'],
  'examples': [
    {'title': 'θ1=30°、θ2=45°、臂各 1m', 'body': 'x=cos30+cos75=0.866+0.259=1.125m；y=sin30+sin75=0.5+0.966=1.466m。'},
    {'title': '全伸展', 'body': 'θ1=θ2=0 → 末端 (2,0)，恰为 r_max。'}],
  'faqs': [
    {'q': 'θ2 是相对角？', 'a': '是第二连杆相对第一连杆的夹角，绝对角=θ1+θ2。'},
    {'q': '有唯一解吗？', 'a': '正运动学单值；逆运动学可能多解或不可达。'}]},

'robotics/gear-ratio-speed': {
  'title': '齿轮减速输出转速',
  'scenarios': [
    '减速箱输出转速/线速。',
    '传动比换算。',
    '轮式底盘末级速度。'],
  'examples': [
    {'title': '输入 300rpm、比 30、轮径 0.1m', 'body': 'n_out=300/30=10rpm；v=10×2π×0.1/60=0.105 m/s。'},
    {'title': '减速比 60', 'body': 'n_out=5rpm，线速减半=0.052 m/s，更慢更大力。'}],
  'faqs': [
    {'q': '转速与比关系？', 'a': 'n_out=n_in/i，i>1 减速；同时扭矩按比放大。'},
    {'q': '效率影响速度？', 'a': '理论无滑差，效率主要影响输出力矩而非转速。'}]},

'robotics/gear-ratio-torque': {
  'title': '齿轮传动输出扭矩',
  'scenarios': [
    '减速增扭计算。',
    '含效率的扭矩传递。',
    '关节驱动选型。'],
  'examples': [
    {'title': '输入 1N·m、比 10、效率 0.9', 'body': 'T_out=1×10×0.9=9 N·m；减速 10 倍增扭并计 10% 损耗。'},
    {'title': '效率 1.0', 'body': 'T_out=10 N·m，理想无损耗。'}],
  'faqs': [
    {'q': '扭矩为何增？', 'a': '减速换扭矩，T_out=T_in×i×η。'},
    {'q': '功守恒？', 'a': '忽略损耗时功率守恒：T_in·ω_in=T_out·ω_out。'}]},

'robotics/gravity-comp-torque': {
  'title': '重力补偿力矩',
  'scenarios': [
    '水平臂重力平衡。',
    '关节力矩预估。',
    '平衡弹簧/配重设计。'],
  'examples': [
    {'title': '5kg、臂长 0.3m、水平', 'body': 'τ=m·g·L·cosθ=5×9.81×0.3×1=14.7 N·m（θ=0 水平最大）。'},
    {'title': '臂上举 90°', 'body': 'cos90=0 → 重力矩为 0，无需补偿。'}],
  'faqs': [
    {'q': 'th 是什么角？', 'a': '臂与水平夹角；水平 θ=0 时重力矩最大。'},
    {'q': '多连杆？', 'a': '各连杆重力矩求和，质心法向距离累加。'}]},

'robotics/gripper-force': {
  'title': '夹爪夹持力',
  'scenarios': [
    '关节力矩换夹持力。',
    '夹持可靠性评估。',
    '力控夹爪设定。'],
  'examples': [
    {'title': '力矩 5N·m、力臂 5cm', 'body': 'F=2τ/L=2×5/0.05=200N；双侧夹持共提供 200N 法向力。'},
    {'title': '力臂加倍', 'body': 'L=0.1 → F=100N，力臂越长夹持力越小。'}],
  'faqs': [
    {'q': '为何 2τ？', 'a': '对称双边夹爪各由力矩产生法向力，合力为 2τ/L。'},
    {'q': '与夹紧不滑？', 'a': '需 F·μ≥工件重/外扰，μ 为摩擦系数。'}]},

'robotics/inverse-kinematics-2r': {
  'title': '二连杆逆运动学',
  'scenarios': [
    '已知末端求关节角。',
    '平面内点可达性。',
    '轨迹逆解。'],
  'examples': [
    {'title': '目标 (1.3,1.2)、臂各 1m', 'body': 'r²=1.3²+1.2²=3.13；cosθ2=(3.13−2)/(2×1×1)=0.565 → θ2≈55.6°，可解且在工作空间内。'},
    {'title': '超出 r_max', 'body': 'r>2m 则无解，目标不可达需重规划。'}],
  'faqs': [
    {'q': 'cosθ2>1？', 'a': '说明目标超出可达半径，逆解不存在。'},
    {'q': '几个解？', 'a': '平面内二连杆通常肘上/肘下两解，按约束选。'}]},

'robotics/joint-angular-velocity': {
  'title': '关节角速度',
  'scenarios': [
    '末端线速换关节角速。',
    '单转动关节运动。',
    '速度规划。'],
  'examples': [
    {'title': '线速 0.5m/s、臂长 0.3m', 'body': 'ω=v/L=0.5/0.3=1.67 rad/s。'},
    {'title': '臂长 0.6m', 'body': 'ω=0.83 rad/s，同线速下长臂角速减半。'}],
  'faqs': [
    {'q': '适用场景？', 'a': '单转动关节、末端沿切向线速 v 时。'},
    {'q': '与角加速度？', 'a': 'a_t=L·α，切向加速度同理。'}]},

'robotics/lead-screw-speed': {
  'title': '丝杠进给速度',
  'scenarios': [
    '直线模组分速。',
    '导程与转速换算。',
    'Z 轴进给规划。'],
  'examples': [
    {'title': '导程 5mm、300rpm', 'body': 'v=n·p/60=300×0.005/60=0.025 m/s=25 mm/s。'},
    {'title': '导程 10mm', 'body': 'v=50 mm/s，导程越大同转速进给越快。'}],
  'faqs': [
    {'q': '导程 p？', 'a': '丝杠每转前进距离（m）；v=n·p/60（n 为 rpm）。'},
    {'q': '精度与导程？', 'a': '大导程快但每步分辨率低，需权衡。'}]},

'robotics/lifting-torque': {
  'title': '提升力矩',
  'scenarios': [
    '卷扬/绞盘提升负载。',
    '鼓轮半径换力矩。',
    '提升电机选型。'],
  'examples': [
    {'title': '2kg、鼓半径 0.5m', 'body': 'τ=m·g·r=2×9.8×0.5=9.8 N·m。'},
    {'title': '半径减半', 'body': 'r=0.25 → τ=4.9 N·m，小半径省力。'}],
  'faqs': [
    {'q': '与重力补偿区别？', 'a': '本式为绕鼓轮提升力矩，重力补偿是绕臂关节水平保持。'},
    {'q': '加速提升？', 'a': '须另加 m·a·r 的加速力矩。'}]},

'robotics/linear-accel-force': {
  'title': '直线运动驱动力',
  'scenarios': [
    '加速所需推力。',
    '牛顿第二定律应用。',
    '电机推力选型。'],
  'examples': [
    {'title': '10kg 以 2m/s² 加速', 'body': 'F=m·a=10×2=20N。'},
    {'title': '含摩擦', 'body': '总推力=20N+摩擦阻力，须覆盖地面/传动损耗。'}],
  'faqs': [
    {'q': '匀速时力？', 'a': '理想无摩擦匀速只需克服阻力，F≈0（仅抗摩擦）。'},
    {'q': '斜坡？', 'a': '须加 m·g·sinα 分量。'}]},

'robotics/motor-power': {
  'title': '电机机械功率',
  'scenarios': [
    '力矩×角速求功率。',
    '电机/驱动器选型。',
    '能耗估算。'],
  'examples': [
    {'title': '力矩 2N·m、角速 10rad/s', 'body': 'P=τ·ω=2×10=20W。'},
    {'title': '角速 20', 'body': 'P=40W，功率与角速成正比。'}],
  'faqs': [
    {'q': '单位', 'a': 'τ 用 N·m、ω 用 rad/s，得 W。'},
    {'q': '电气功率？', 'a': '机械功率除以效率得输入电功率。'}]},

'robotics/motor-torque-current': {
  'title': '电机转矩-电流',
  'scenarios': [
    '电流估算输出力矩。',
    '转矩常数应用。',
    '电流环设定。'],
  'examples': [
    {'title': '常数 0.05N·m/A、电流 10A', 'body': 'T=k_t·I=0.05×10=0.5 N·m。'},
    {'title': '电流 20A', 'body': 'T=1.0 N·m，力矩与电流成正比。'}],
  'faqs': [
    {'q': 'k_t 与反电动势常数？', 'a': '理想电机 k_t=k_e（单位一致时），均正比于磁通。'},
    {'q': '堵转？', 'a': '堵转电流最大、力矩最大但易过热，需限流。'}]},

'robotics/pid-controller': {
  'title': 'PID 控制器输出',
  'scenarios': [
    '闭环控制输出计算。',
    'P/I/D 三项合成。',
    '参数整定验证。'],
  'examples': [
    {'title': 'kp1 ki0.1 kd0.05，e=2 ei=1 ep=0.5 dt=0.1', 'body': 'u=1×2+0.1×1+0.05×(2−0.5)/0.1=2+0.1+0.75=2.85。'},
    {'title': '仅 P 控制', 'body': 'ki=kd=0 → u=2，稳态有静差；加 I 消除、D 抑制超调。'}],
  'faqs': [
    {'q': 'ei 是什么？', 'a': '误差积分累积；ep 为上一拍误差，用于 D 项差分 (e−ep)/dt。'},
    {'q': '积分饱和？', 'a': '大误差长期积分易饱和，需抗积分饱和限幅。'}]},

'robotics/rotational-inertia-torque': {
  'title': '转动惯量所需力矩',
  'scenarios': [
    '转动加速力矩。',
    '关节惯量评估。',
    '加减速规划。'],
  'examples': [
    {'title': '惯量 0.5kg·m²、角加速度 4rad/s²', 'body': 'τ=I·α=0.5×4=2 N·m。'},
    {'title': '惯量加倍', 'body': 'I=1 → τ=4 N·m，同角加速需更大力矩。'}],
  'faqs': [
    {'q': '与线性类比？', 'a': 'τ=Iα 对应 F=ma，I 为转动惯量、α 为角加速度。'},
    {'q': '含重力？', 'a': '本式仅加速项；水平臂还需叠加重力矩。'}]},

'robotics/servo-pwm-angle': {
  'title': '舵机 PWM 转角',
  'scenarios': [
    '舵机脉宽映射角度。',
    '50Hz 舵机控制。',
    '关节角度设定。'],
  'examples': [
    {'title': '脉宽 1500μs、范围 500–2500', 'body': 'θ=(1500−500)/(2500−500)×180=1000/2000×180=90°（中位）。'},
    {'title': '脉宽 2000μs', 'body': 'θ=(2000−500)/2000×180=135°，随脉宽线性增大。'}],
  'faqs': [
    {'q': '标准脉宽？', 'a': '常见 500μs=0°、1500μs=90°、2500μs=180°（50Hz）。'},
    {'q': '不同范围？', 'a': '更换 pmin/pmax 即可适配 180°/270° 等舵机。'}]},

'robotics/stepper-step-angle': {
  'title': '步进电机步距角',
  'scenarios': [
    '每步转动角度。',
    '步数/转换算。',
    '开环定位精度。'],
  'examples': [
    {'title': '200 步/转', 'body': 'θ=360/200=1.8°；每转 200 整步，细分可进一步减小。'},
    {'title': '400 步/转', 'body': 'θ=0.9°，步距减半精度更高。'}],
  'faqs': [
    {'q': '细分做什么？', 'a': '驱动器将整步细分（如 1/16）得更小等效步距但力矩略降。'},
    {'q': '丢步？', 'a': '开环无反馈，过载/高速会丢步，需留余量或加编码。'}]},

'robotics/stereo-depth': {
  'title': '双目立体深度',
  'scenarios': [
    '视差求物体深度。',
    '基线/焦距配置。',
    '深度相机原理。'],
  'examples': [
    {'title': '焦距 500px、基线 0.1m、视差 25px', 'body': 'Z=f·B/d=500×0.1/25=2.0m。'},
    {'title': '视差减半', 'body': 'd=12.5 → Z=4m，视差越小越远（深度与视差成反比）。'}],
  'faqs': [
    {'q': '单位？', 'a': 'f、d 同取像素，B 取米，则 Z 为米。'},
    {'q': '近处误差大？', 'a': '是；深度对视差变化敏感，近处更不稳。'}]},

'robotics/trajectory-time-linear': {
  'title': '直线轨迹时间',
  'scenarios': [
    '恒定速度到达时间。',
    '任务节拍估算。',
    '路径规划时长。'],
  'examples': [
    {'title': '移动 1m、速度 0.2m/s', 'body': 't=d/v=1/0.2=5s。'},
    {'title': '提速到 0.5', 'body': 't=2s，速度越高耗时越短。'}],
  'faqs': [
    {'q': '加减速呢？', 'a': '本式为匀速段；含加减速需分段积分。'},
    {'q': '与 S 曲线？', 'a': '工业常用 S 型加减速以减冲击，本式为简化匀速模型。'}]},

'robotics/wheel-odometry': {
  'title': '轮式里程计',
  'scenarios': [
    '左右轮位移推位姿变化。',
    '差速底盘航位推算。',
    '定位漂移评估。'],
  'examples': [
    {'title': '左 1.0、右 1.2m、轮距 0.4m', 'body': 'ds=(1.0+1.2)/2=1.1m，dθ=(1.2−1.0)/0.4=0.5rad；前进 1.1m 并右转 0.5rad。'},
    {'title': '等位移直行', 'body': 'dθ=0，纯平移 ds=dl=dr。'}],
  'faqs': [
    {'q': '轮距 L？', 'a': '两轮间距；dθ=(dr−dl)/L。'},
    {'q': '漂移来源？', 'a': '轮径误差、打滑使积分漂移，需融合 IMU/视觉校正。'}]},
}

def main():
    data = json.load(open(F, encoding='utf-8'))
    for slug, info in KB.items():
        blob = json.dumps(info, ensure_ascii=False)
        if BAD_RE.search(blob):
            raise SystemExit(f'BAD placeholder in KB {slug}: {BAD_RE.search(blob).group()}')
    changed = 0
    for slug, info in KB.items():
        if slug not in data:
            data[slug] = info
            changed += 1
            continue
        if data[slug] != info:
            data[slug] = info
            changed += 1
    json.dump(data, open(F, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    open(F, 'a').write('\n')
    print(f'KB entries: {len(KB)} changed: {changed}')

if __name__ == '__main__':
    main()
