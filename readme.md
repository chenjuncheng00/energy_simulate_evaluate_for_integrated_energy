# 综合能源仿真评估程序说明文档
## 1. 功能介绍
- 基于Modelica搭建综合能源系统机理模型；
- 将Modelica机理模型导出为FMU；
- 使用FMU进行系统参数辨识，得到算法所需的模型；
- 稳态模型：空调主机COP模型、冷却塔逼近度模型、水泵管道阻力特性模型；
- 动态模型：系统EER效率动态模型、冷冻水回水温度动态模型；
- 使用优化控制算法对FMU进行控制仿真；
- 优化控制算法包括: 稳态搜索算法和动态控制算法；
- 动态控制算法为广义预测控制算法；
- 验证和评估算法的优化控制效果；
## 2. 代码说明
- 本程序可以在Windows系统运行
- 系统要求: Windows 10 OR 11 64位
- Python版本要求: 3.12
## 3. 综合能源系统介绍
### 3.1 包括的设备类型
- 电空调: 冷水机、空气源热泵；
- 水泵: 一级冷冻水泵、二级冷冻水泵、冷却水泵；
- 设备级阀门: 冷冻阀门、冷却阀门、冷却塔阀门；
- 系统级阀门: 向用户侧供冷阀门；
- 蓄冷装置: 水蓄冷；
- 冷却塔；
- 换热器(用于自然冷却模式时代替电空调参与计算)；
### 3.2 可实现的控制命令类型
- 电空调: 开启、关闭、冷冻水出水温度设定值；
- 水泵: 开启、关闭、频率设定值；
- 冷却塔: 开启、关闭、频率设定值；
- 阀门: 开启、关闭；
## 4. 其它说明
- 本代码对应的研究成果有专门的PPT说明，如有兴趣可与我联系；


# Documentation for the Integrated Energy Simulation and Evaluation Program
## 1. Function Introduction
- Building an integrated energy system model based on Modelica;
- Exporting the Modelica model to an FMU;
- Using the FMU for parameter identification to obtain the algorithm-required model;
- Steady-state models: COP model for the air conditioning unit, approximation degree model for the cooling tower, resistance characteristic model for the water pump;
- Dynamic models: EER efficiency dynamic model for the system, return water temperature dynamic model for the chilled water;
- Control simulation using optimization control algorithms on the FMU;
- Optimization control algorithms include: steady-state search algorithm and dynamic control algorithm;
- The dynamic control algorithm is the universal predictive control algorithm;
- Verifying and evaluating the optimization control effect of the algorithm;
## 2. Code Explanation
- This program can run on Windows system
- System requirements: Windows 10 OR 11 64-bit
- Python version: 3.12
## 3. Introduction to Integrated Energy Systems
### 3.1 Types of Equipment Included
- Electric air conditioners: water chillers, air source heat pumps;
- Water pumps: primary chilled water pumps, secondary chilled water pumps, cooling water pumps;
- Equipment-level valves: chilled water valves, cooling water valves, cooling tower valves;
- System-level valves: valves supplying cold to users;
- Thermal energy storage devices: water thermal energy storage;
- Cooling towers;
- Heat exchangers (used to replace electric air conditioners in natural cooling mode for calculation);
3.2 Types of Achievable Control Commands
- Electric Air Conditioner: Start/Stop, Setpoint for Chilled Water Outlet Temperature;
- Water Pump: Start/Stop, Setpoint for Frequency;
- Cooling Tower: Start/Stop, Setpoint for Frequency;
- Valves: Open/Close;
## 4. Other Information
- There is a specific PPT to explain the research results corresponding to this code, and you can contact me if you are interested;