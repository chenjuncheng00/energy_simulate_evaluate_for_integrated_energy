from control.matlab import *

def model_fmu_dynamics():
    """
    系统动态特性模型:GPC控制器内置的模型
    Returns:

    """
    # 传递函数
    s = tf("s")
    # 预测时域Np
    Np = 700
    # 控制时域Nc
    Nc = 150

    # EER模型: Q=9000kW
    tf11_1 = (-0.8614 * s ** 5 - 0.0008275 * s ** 4 - 2.564 * 10 ** (-6) * s ** 3 - 6.129 * 10 ** (-10) * s ** 2 -
              1.288 * 10 ** (-12) * s + 9.093 * 10 ** (-18)) / \
             (s ** 5 + 0.001345 * s ** 4 + 2.351 * 10 ** (-6) * s ** 3 + 1.701 * 10 ** (-9) * s ** 2 +
              8.882 * 10 ** (-13) * s + 1.954 * 10 ** (-16))
    tf12_1 = (0.002179 * s ** 4 + 8.444 * 10 ** (-6) * s ** 3 + 1.085 * 10 ** (-8) * s ** 2 +
              3.083 * 10 ** (-11) * s - 8.39 * 10 ** (-16)) / \
             (s ** 4 + 0.00331 * s ** 3 + 7.376 * 10 ** (-6) * s ** 2 + 9.551 * 10 ** (-9) * s + 4.197 * 10 ** (-12))
    tf13_1 = (-0.0002421 * s - 6.382 * 10 ** (-5)) / (s + 0.3085)
    tf14_1 = (0.0006234 * s + 1.651 * 10 ** (-6)) / (s + 0.001419)
    # Tei模型: Q=9000kW
    # tf21_1 = (0.0009304) / (s + 0.001014) * exp(-7200 * s)
    # tf22_1 = (-3.022 * 10 ** (-6)) / (s + 0.001188) * exp(-2400 * s)
    tf21_1 = (0.0009304) / (s + 0.001014) * (1 / (7200 * s + 1))
    tf22_1 = (-3.022 * 10 ** (-6)) / (s + 0.001188) * (1 / (2400 * s + 1))
    tf23_1 = 0 / 1
    tf24_1 = 0 / 1
    # 9000kW模型列表
    tf1_EER_list = [[tf11_1, tf12_1, tf13_1, tf14_1]]
    tf1_Tei_list = [[tf21_1, tf22_1, tf23_1, tf24_1]]
    tf1_list = [tf1_EER_list[0], tf1_Tei_list[0]]
    # 9000kW权值列表
    r1_1 = 98.21
    r2_1 = 0.01
    r3_1 = 56.54
    r4_1 = 0.01
    r1_list = [r1_1, r2_1, r3_1, r4_1]
    q1_1 = 1000.0
    q2_1 = 365.9
    q1_list = [q1_1, q2_1]

    # EER模型: Q=11000kW
    tf11_2 = (-1.063 * s ** 4 - 0.001699 * s ** 3 - 1.036 * 10 ** (-6) * s ** 2 - 1.522 * 10 ** (-9) * s +
              2.031 * 10 ** (-15)) / (s ** 4 + 0.001202 * s ** 3 + 1.56 * 10 ** (-6) * s ** 2 +
                                      8.24 * 10 ** (-10) * s + 2.166 * 10 ** (-13))
    tf12_2 = (0.0008663 * s ** 3 + 9.915 * 10 ** (-7) * s ** 2 + 4.135 * 10 ** (-9) * s - 7.302 * 10 ** (-13)) / \
             (s ** 3 + 0.002169 * s ** 2 + 3.046 * 10 ** (-6) * s + 1.556 * 10 ** (-9))
    tf13_2 = (-0.0005302 * s - 1.057 * 10 ** (-6)) / (s + 0.002065)
    tf14_2 = (0.0008379 * s + 2.064 * 10 ** (-6)) / (s + 0.001558)
    # Tei模型: Q=11000kW
    # tf21_2 = (0.2072 * s + 0.001043) / (s + 0.001048) * exp(-6000 * s)
    # tf22_2 = (-0.0007851 * s - 3.137 * 10 ** (-6)) / (s + 0.00133) * exp(-2400 * s)
    tf21_2 = (0.2072 * s + 0.001043) / (s + 0.001048) * (1 / (6000 * s + 1))
    tf22_2 = (-0.0007851 * s - 3.137 * 10 ** (-6)) / (s + 0.00133) * (1 / (2400 * s + 1))
    tf23_2 = 0 / 1
    tf24_2 = 0 / 1
    # 11000kW模型列表
    tf2_EER_list = [[tf11_2, tf12_2, tf13_2, tf14_2]]
    tf2_Tei_list = [[tf21_2, tf22_2, tf23_2, tf24_2]]
    tf2_list = [tf2_EER_list[0], tf2_Tei_list[0]]
    # 11000kW权值列表
    r1_2 = 42.38
    r2_2 = 0.01
    r3_2 = 40.5
    r4_2 = 100.0
    r2_list = [r1_2, r2_2, r3_2, r4_2]
    q1_2 = 645.27
    q2_2 = 389.58
    q2_list = [q1_2, q2_2]

    # EER模型: Q=13000kW
    tf11_3 = (-0.78 * s ** 5 - 0.001237 * s ** 4 - 5.377 * 10 ** (-6) * s ** 3 - 1.888 * 10 ** (-9) * s ** 2 -
              5.882 * 10 ** (-12) * s + 9.041 * 10 ** (-17)) / \
             (s ** 5 + 0.001989 * s ** 4 + 4.952 * 10 ** (-6) * s ** 3 + 5.201 * 10 ** (-9) * s ** 2 +
              3.871 * 10 ** (-12) * s + 1.192 * 10 ** (-15))
    tf12_3 = (-0.001201 * s ** 4 - 2.751 * 10 ** (-6) * s ** 3 - 1.129 * 10 ** (-8) * s ** 2 -
              1.311 * 10 ** (-11) * s - 3.63 * 10 ** (-15)) / \
             (s ** 4 + 0.0025 * s ** 3 + 8.684 * 10 ** (-6) * s ** 2 + 9.754 * 10 ** (-9) * s + 5.811 * 10 ** (-12))
    tf13_3 = (-0.000626 * s - 1.266 * 10 ** (-6)) / (s + 0.001963)
    tf14_3 = (0.0006605 * s + 2.613 * 10 ** (-6)) / (s + 0.002313)
    # Tei模型: Q=13000kW
    # tf21_3 = (0.00114) / (s + 0.001145) * exp(-4800 * s)
    # tf22_3 = (-0.0004101 * s - 3.141 * 10 ** (-6)) / (s + 0.001641) * exp(-1800 * s)
    tf21_3 = (0.00114) / (s + 0.001145) * (1 / (4800 * s + 1))
    tf22_3 = (-0.0004101 * s - 3.141 * 10 ** (-6)) / (s + 0.001641) * (1 / (1800 * s + 1))
    tf23_3 = 0 / 1
    tf24_3 = 0 / 1
    # 13000kW模型列表
    tf3_EER_list = [[tf11_3, tf12_3, tf13_3, tf14_3]]
    tf3_Tei_list = [[tf21_3, tf22_3, tf23_3, tf24_3]]
    tf3_list = [tf3_EER_list[0], tf3_Tei_list[0]]
    # 13000kW权值列表
    r1_3 = 327.89
    r2_3 = 916.76
    r3_3 = 1000.0
    r4_3 = 0.01
    r3_list = [r1_3, r2_3, r3_3, r4_3]
    q1_3 = 6575.59
    q2_3 = 10000.0
    q3_list = [q1_3, q2_3]

    # 模型列表
    Np_list = [Np, Np, Np]
    Nc_list = [Nc, Nc, Nc]
    model_EER_list = [tf1_EER_list, tf2_EER_list, tf3_EER_list]
    model_Tei_list = [tf1_Tei_list, tf2_Tei_list, tf3_Tei_list]
    model_list = [tf1_list, tf2_list, tf3_list]
    r_list = [r1_list, r2_list, r3_list]
    q_list = [q1_list, q2_list, q3_list]
    # 每个模型对应的制冷功率Q的列表
    Q_model_list = [9000, 11000, 13000]

    # # EER模型: Q=13000kW
    # tf11_1 = (-0.9588 * s ** 3 - 0.000365 * s ** 2 - 1.534 * 10 ** (-6) * s + 3.493 * 10 ** (-11)) / \
    #          (s ** 3 + 0.0009529 * s ** 2 + 1.034 * 10 ** (-6) * s + 3.263 * 10 ** (-10))
    # tf12_1 = (-0.001176 * s ** 3 + 0.0001242 * s ** 2 + 1.089 * 10 ** (-7) * s - 4.437 * 10 ** (-11)) / \
    #          (s ** 3 + 0.009892 * s ** 2 + 5.183 * 10 ** (-5) * s + 6.968 * 10 ** (-8))
    # tf13_1 = (-0.0006549 * s - 1.063 * 10 ** (-6)) / (s + 0.001583)
    # tf14_1 = (0.0006289*s+2.518*10**(-6))/(s+0.002324)
    # # Tei模型: Q=13000kW
    # # tf21_1 = (0.4132 * s + 0.2477) / (s + 0.2488) * exp(-4800 * s)
    # # tf22_1 = (-0.002007 * s ** 2 - 5.994 * 10 ** (-7) * s - 9.205 * 10 ** (-10)) / \
    # #          (s ** 2 + 0.0003393 * s + 4.912 * 10 ** (-7)) * exp(-1800 * s)
    # tf21_1 = ((0.4132 * s + 0.2477) / (s + 0.2488)) * (1 / (4800 * s + 1))
    # tf22_1 = ((-0.002007 * s ** 2 - 5.994 * 10 ** (-7) * s - 9.205 * 10 ** (-10)) /
    #           (s ** 2 + 0.0003393 * s + 4.912 * 10 ** (-7))) * (1 / (1800 * s + 1))
    # tf23_1 = 0 / 1
    # tf24_1 = 0 / 1
    # # 13000kW模型列表
    # tf1_EER_list = [[tf11_1, tf12_1, tf13_1, tf14_1]]
    # tf1_Tei_list = [[tf21_1, tf22_1, tf23_1, tf24_1]]
    # tf1_list = [tf1_EER_list[0], tf1_Tei_list[0]]
    # # 13000kW权值列表
    # r1_1 = 327.89
    # r2_1 = 916.76
    # r3_1 = 1000.0
    # r4_1 = 0.01
    # r1_list = [r1_1, r2_1, r3_1, r4_1]
    # q1_1 = 6575.59
    # q2_1 = 10000.0
    # q1_list = [q1_1, q2_1]
    #
    # # EER模型: Q=11000kW
    # tf11_2 = (-0.937 * s ** 2 - 0.000606 * s - 2.874 * 10 ** (-8)) / (s ** 2 + 0.0002834 * s + 1.526 * 10 ** (-7))
    # # tf12_2 = (-0.0006065 * s - 3.366 * 10 ** (-7)) / (s + 0.0006914) * exp(-2400 * s)
    # tf12_2 = ((-0.0006065 * s - 3.366 * 10 ** (-7)) / (s + 0.0006914)) * (1 / (2400 * s + 1))
    # tf13_2 = (-0.0005296 * s - 1.07 * 10 ** (-6)) / (s + 0.002097)
    # tf14_2 = (0.0008114 * s + 1.852 * 10 ** (-6)) / (s + 0.001418)
    # # Tei模型: Q=11000kW
    # # tf21_2 = (0.9507 * s + 0.01279) / (s + 0.01285) * exp(-6000 * s)
    # # tf22_2 = (-0.002393 * s - 7.264 * 10 ** (-7)) / (s + 0.0003096) * exp(-2400 * s)
    # tf21_2 = ((0.9507 * s + 0.01279) / (s + 0.01285)) * (1 / (6000 * s + 1))
    # tf22_2 = ((-0.002393 * s - 7.264 * 10 ** (-7)) / (s + 0.0003096)) * (1 / (2400 * s + 1))
    # tf23_2 = 0 / 1
    # tf24_2 = 0 / 1
    # # 11000kW模型列表
    # tf2_EER_list = [[tf11_2, tf12_2, tf13_2, tf14_2]]
    # tf2_Tei_list = [[tf21_2, tf22_2, tf23_2, tf24_2]]
    # tf2_list = [tf2_EER_list[0], tf2_Tei_list[0]]
    # # 11000kW权值列表
    # r1_2 = 42.38
    # r2_2 = 0.01
    # r3_2 = 40.5
    # r4_2 = 100.0
    # r2_list = [r1_2, r2_2, r3_2, r4_2]
    # q1_2 = 645.27
    # q2_2 = 389.58
    # q2_list = [q1_2, q2_2]
    #
    # # EER模型: Q=9000kW
    # tf11_3 = (-1.015 * s ** 2 - 0.000329 * s - 6.155 * 10 ** (-8)) / \
    #          (s ** 2 + 8.71 * 10 ** (-5) * s + 1.322 * 10 ** (-7))
    # tf12_3 = (0.002177 * s ** 3 + 1.902 * 10 ** (-6) * s ** 2 + 1.196 * 10 ** (-8) * s - 3.923 * 10 ** (-13)) / \
    #          (s ** 3 + 0.001535 * s ** 2 + 3.553 * 10 ** (-6) * s + 2.462 * 10 ** (-9))
    # tf13_3 = (-0.0002741 * s - 0.0001954) / (s + 0.8243)
    # tf14_3 = (0.0006958 * s + 1.817 * 10 ** (-6)) / (s + 0.001414)
    # # Tei模型: Q=9000kW
    # # tf21_3 = (0.713 * s + 0.009071) / (s + 0.009125) * exp(-6600 * s)
    # # tf22_3 = (-0.002064 * s ** 3 - 2.594 * 10 ** (-6) * s ** 2 - 6.333 * 10 ** (-9) * s - 1.496 * 10 ** (-12)) / \
    # #          (s ** 3 + 0.0007392 * s ** 2 + 2.759 * 10 ** (-6) * s + 5.558 * 10 ** (-10)) * exp(-2400 * s)
    # tf21_3 = ((0.713 * s + 0.009071) / (s + 0.009125)) * (1 / (6600 * s + 1))
    # tf22_3 = ((-0.002064 * s ** 3 - 2.594 * 10 ** (-6) * s ** 2 - 6.333 * 10 ** (-9) * s - 1.496 * 10 ** (-12)) /
    #           (s ** 3 + 0.0007392 * s ** 2 + 2.759 * 10 ** (-6) * s + 5.558 * 10 ** (-10))) * (1 / (2400 * s + 1))
    # tf23_3 = 0 / 1
    # tf24_3 = 0 / 1
    # # 9000kW模型列表
    # tf3_EER_list = [[tf11_3, tf12_3, tf13_3, tf14_3]]
    # tf3_Tei_list = [[tf21_3, tf22_3, tf23_3, tf24_3]]
    # tf3_list = [tf3_EER_list[0], tf3_Tei_list[0]]
    # # 9000kW权值列表
    # r1_3 = 98.21
    # r2_3 = 0.01
    # r3_3 = 56.54
    # r4_3 = 0.01
    # r3_list = [r1_3, r2_3, r3_3, r4_3]
    # q1_3 = 1000.0
    # q2_3 = 365.9
    # q3_list = [q1_3, q2_3]
    #
    # # EER模型: Q=7500kW
    # tf11_4 = (-0.903 * s ** 3 + 0.0002535 * s ** 2 - 6.69 * 10 ** (-7) * s + 6.655 * 10 ** (-11)) / \
    #          (s ** 3 + 1.697 * 10 ** (-5) * s ** 2 + 5.569 * 10 ** (-7) * s + 8.981 * 10 ** (-21))
    # tf12_4 = (0.002968 * s ** 3 + 2.118 * 10 ** (-6) * s ** 2 + 1.545 * 10 ** (-8) * s - 2.033 * 10 ** (-13)) / \
    #          (s ** 3 + 0.001769 * s ** 2 + 3.319 * 10 ** (-6) * s + 1.94 * 10 ** (-9))
    # tf13_4 = (-0.0005676 * s - 1.122 * 10 ** (-7)) / (s + 0.0001852)
    # tf14_4 = (0.0003312 * s + 1.894 * 10 ** (-6)) / (s + 0.001875)
    # # Tei模型: Q=7500kW
    # # tf21_4 = (0.949 * s + 0.006319) / (s + 0.006362) * exp(-7800 * s)
    # # tf22_4 = (-0.002566 * s - 1.993 * 10 ** (-6)) / (s + 0.0007493) * exp(-3000 * s)
    # tf21_4 = ((0.949 * s + 0.006319) / (s + 0.006362)) * (1 / (7800 * s + 1))
    # tf22_4 = ((-0.002566 * s - 1.993 * 10 ** (-6)) / (s + 0.0007493)) * (1 / (3000 * s + 1))
    # tf23_4 = 0 / 1
    # tf24_4 = 0 / 1
    # # 7500kW模型列表
    # tf4_EER_list = [[tf11_4, tf12_4, tf13_4, tf14_4]]
    # tf4_Tei_list = [[tf21_4, tf22_4, tf23_4, tf24_4]]
    # tf4_list = [tf4_EER_list[0], tf4_Tei_list[0]]
    # # 7500kW权值列表
    # r1_4 = 0.01
    # r2_4 = 0.01
    # r3_4 = 134.04
    # r4_4 = 0.01
    # r4_list = [r1_4, r2_4, r3_4, r4_4]
    # q1_4 = 2824.57
    # q2_4 = 1500.37
    # q4_list = [q1_4, q2_4]
    #
    # # EER模型: Q=5500kW
    # tf11_5 = (-1.23 * s ** 3 + 2.084 * 10 ** (-6) * s ** 2 - 1.703 * 10 ** (-7) * s + 5.995 * 10 ** (-12)) / \
    #          (s ** 3 + 7.012 * 10 ** (-5) * s ** 2 + 1.058 * 10 ** (-7) * s + 3.609 * 10 ** (-12))
    # tf12_5 = (0.003622 * s ** 2 + 2.466 * 10 ** (-6) * s + 5.594 * 10 ** (-12)) / \
    #          (s ** 2 + 0.000569 * s + 1.437 * 10 ** (-7))
    # tf13_5 = (-0.0001931 * s ** 2 - 9.802 * 10 ** (-8) * s - 1.502 * 10 ** (-11)) / \
    #          (s ** 2 + 0.0004137 * s + 6.702 * 10 ** (-8))
    # # tf14_5 = (0.0008269 * s ** 2 + 9.15 * 10 ** (-7) * s + 3.612 * 10 ** (-10)) / \
    # #          (s ** 2 + 0.000573 * s + 2.577 * 10 ** (-7)) * exp(-600 * s)
    # tf14_5 = (0.0008269 * s ** 2 + 9.15 * 10 ** (-7) * s + 3.612 * 10 ** (-10)) / \
    #          (s ** 2 + 0.000573 * s + 2.577 * 10 ** (-7)) * (1 / (600 * s + 1))
    # # Tei模型: Q=5500kW
    # # tf21_5 = (0.1267 * s ** 2 + 7.265 * 10 ** (-5) * s + 8.598 * 10 ** (-8)) / \
    # #          (s ** 2 + 0.0002301 * s + 8.299 * 10 ** (-8)) * exp(-10200 * s)
    # # tf22_5 = (-1.05 * 10 ** (-6)) / (s + 0.0003412) * exp(-2400 * s)
    # tf21_5 = (0.1267 * s ** 2 + 7.265 * 10 ** (-5) * s + 8.598 * 10 ** (-8)) / \
    #          (s ** 2 + 0.0002301 * s + 8.299 * 10 ** (-8)) * (1 / (10200 * s + 1))
    # tf22_5 = (-1.05 * 10 ** (-6)) / (s + 0.0003412) * (1 / (2400 * s + 1))
    # tf23_5 = 0 / 1
    # tf24_5 = 0 / 1
    # # 5500kW模型列表
    # tf5_EER_list = [[tf11_5, tf12_5, tf13_5, tf14_5]]
    # tf5_Tei_list = [[tf21_5, tf22_5, tf23_5, tf24_5]]
    # tf5_list = [tf5_EER_list[0], tf5_Tei_list[0]]
    # # 5500kW权值列表
    # r1_5 = 2808.68
    # r2_5 = 7943.68
    # r3_5 = 6720.84
    # r4_5 = 0.01
    # r5_list = [r1_5, r2_5, r3_5, r4_5]
    # q1_5 = 78365.77
    # q2_5 = 38308.36
    # q5_list = [q1_5, q2_5]
    #
    # # EER模型: Q=3500kW
    # tf11_6 = (-1.6 * s ** 4 - 0.0002104 * s ** 3 - 2.906 * 10 ** (-7) * s ** 2 - 3.945 * 10 ** (-11) * s -
    #            1.873 * 10 ** (-15)) / (s ** 4 + 0.0001265 * s ** 3 + 1.979 * 10 ** (-7) * s ** 2 +
    #                                    1.377 * 10 ** (-11) * s + 4.147 * 10 ** (-15))
    # tf12_6 = (0.004434 * s ** 3 + 2.071 * 10 ** (-6) * s ** 2 + 2.563 * 10 ** (-9) * s - 1.956 * 10 ** (-14)) / \
    #          (s ** 3 + 0.0006496 * s ** 2 + 4.462 * 10 ** (-7) * s + 6.968 * 10 ** (-11))
    # tf13_6 = (-1.384 * 10 ** (-9) * s ** 2 - 1.431 * 10 ** (-13) * s - 2.94 * 10 ** (-16)) / \
    #          (s ** 4 + 0.0003016 * s ** 3 + 5.005 * 10 ** (-7) * s ** 2 + 1.273 * 10 ** (-10) * s + 3.311 * 10 ** (-14))
    # tf14_6 = (-0.0001868 * s ** 3 + 1.066 * 10 ** (-6) * s ** 2 + 6.35 * 10 ** (-10) * s + 4.696 * 10 ** (-14)) / \
    #          (s ** 3 + 0.002905 * s ** 2 + 9.086 * 10 ** (-7) * s + 7.981 * 10 ** (-11))
    # # Tei模型: Q=3500kW
    # # tf21_6 = (0.1105 * s ** 2 + 6.491 * 10 ** (-5) * s + 7.813 * 10 ** (-8)) / \
    # #           (s ** 2 + 0.000231 * s + 8.307 * 10 ** (-8)) * exp(-10200 * s)
    # # tf22_6 = (-0.0001915 * s - 9.69 * 10 ** (-7)) / (s + 0.0002967) * exp(-4800 * s)
    # tf21_6 = (0.1105 * s ** 2 + 6.491 * 10 ** (-5) * s + 7.813 * 10 ** (-8)) / \
    #           (s ** 2 + 0.000231 * s + 8.307 * 10 ** (-8)) * (1 / (10200 * s + 1))
    # tf22_6 = (-0.0001915 * s - 9.69 * 10 ** (-7)) / (s + 0.0002967) * (1 / (4800 * s + 1))
    # tf23_6 = 0 / 1
    # tf24_6 = 0 / 1
    # # 3500kW模型列表
    # tf6_EER_list = [[tf11_6, tf12_6, tf13_6, tf14_6]]
    # tf6_Tei_list = [[tf21_6, tf22_6, tf23_6, tf24_6]]
    # tf6_list = [tf6_EER_list[0], tf6_Tei_list[0]]
    # # 3500kW权值列表
    # r1_6 = 0.1
    # r2_6 = 0.1
    # r3_6 = 0.1
    # r4_6 = 0.01
    # r6_list = [r1_6, r2_6, r3_6, r4_6]
    # q1_6 = 57.87
    # q2_6 = 10000.0
    # q6_list = [q1_6, q2_6]

    # # 模型列表
    # Np_list = [Np, Np, Np, Np, Np, Np]
    # Nc_list = [Nc, Nc, Nc, Nc, Nc, Nc]
    # model_EER_list = [tf1_EER_list, tf2_EER_list, tf3_EER_list, tf4_EER_list, tf5_EER_list, tf6_EER_list]
    # model_Tei_list = [tf1_Tei_list, tf2_Tei_list, tf3_Tei_list, tf4_Tei_list, tf5_Tei_list, tf6_Tei_list]
    # model_list = [tf1_list, tf2_list, tf3_list, tf4_list, tf5_list, tf6_list]
    # r_list = [r1_list, r2_list, r3_list, r4_list, r5_list, r6_list]
    # q_list = [q1_list, q2_list, q3_list, q4_list, q5_list, q6_list]
    # # 模型列表全部反转，需要按照制冷负荷从小到大排序
    # model_EER_list = list(reversed(model_EER_list))
    # model_Tei_list = list(reversed(model_Tei_list))
    # model_list = list(reversed(model_list))
    # r_list = list(reversed(r_list))
    # q_list = list(reversed(q_list))
    # 每个模型对应的制冷功率Q的列表
    # Q_model_list = [3500, 5500, 7500, 9000, 11000, 13000]

    # 返回结果
    return model_list, model_EER_list, model_Tei_list, Np_list, Nc_list, r_list, q_list, Q_model_list


def plant_fmu_dynamics():
    """
    系统动态特性模型:被控对象当前情况下实际的传递函数模型
    用于测试MMGPC控制器
    Returns:

    """
    # 传递函数
    s = tf("s")

    # EER模型: Q=14000kW
    tf11_1 = (-0.336 * s ** 2 - 0.0003015 * s + 7.644 * 10 ** (-8)) / (s ** 2 + 0.0005004 * s + 2.112 * 10 ** (-7))
    tf12_1 = (-0.004286 * s ** 4 - 6.653 * 10 ** (-6) * s ** 3 - 4.144 * 10 ** (-9) * s ** 2 -
              2.939 * 10 ** (-12) * s + 1.049 * 10 ** (-16)) / \
             (s ** 4 + 0.0009806 * s ** 3 + 1.486 * 10 ** (-6) * s ** 2 + 6.397 * 10 ** (-10) * s + 8.373 * 10 ** (-14))
    tf13_1 = (-0.0004264 * s ** 5 - 3.099 * 10 ** (-7) * s ** 4 - 5.265 * 10 ** (-10) * s ** 3 -
              2.23 * 10 ** (-13) * s ** 2 - 4.668 * 10 ** (-17) * s - 1.026 * 10 ** (-21)) / \
             (s ** 5 + 0.0005971 * s ** 4 + 1.286 * 10 ** (-6) * s ** 3 + 4.192 * 10 ** (-10) * s ** 2 +
              1.615 * 10 ** (-13) * s + 4.1 * 10 ** (-28))
    tf14_1 = (2.943 * 10 ** (-16)) / (s ** 4 + 0.0008364 * s ** 3 + 4.693 * 10 ** (-7) * s ** 2 +
                                      9.107 * 10 ** (-11) * s + 1.475 * 10 ** (-14))
    # Tei模型: Q=14000kW
    tf21_1 = (2.507 * 10 ** (-16)) / (s ** 5 + 0.003466 * s ** 4 + 4.006 * 10 ** (-6) * s ** 3 +
                                      3.539 * 10 ** (-9) * s ** 2 + 1.501 * 10 ** (-12) * s + 2.798 * 10 ** (-16))
    tf22_1 = (0.001282 * s ** 3 - 2.135 * 10 ** (-7) * s ** 2 - 1.138 * 10 ** (-10) * s - 2.453 * 10 ** (-13)) / \
             (s ** 3 + 0.0004499 * s ** 2 + 9.322 * 10 ** (-7) * s + 4.903 * 10 ** (-11))
    tf23_1 = 0 / 1
    tf24_1 = 0 / 1
    # 14000kW模型列表
    tf1_EER_list = [[tf11_1, tf12_1, tf13_1, tf14_1]]
    tf1_Tei_list = [[tf21_1, tf22_1, tf23_1, tf24_1]]
    tf1_list = [tf1_EER_list[0], tf1_Tei_list[0]]

    # EER模型: Q=13500kW
    tf11_2 = (-0.9401 * s ** 3 - 0.001267 * s ** 2 - 1.044 * 10 ** (-6) * s + 4.624 * 10 ** (-11)) / \
             (s ** 3 + 0.001317 * s ** 2 + 8.187 * 10 ** (-7) * s + 2.306 * 10 ** (-10))
    tf12_2 = (-0.001646 * s ** 3 - 8.011 * 10 ** (-6) * s ** 2 - 2.789 * 10 ** (-9) * s - 1.64 * 10 ** (-14)) / \
             (s ** 3 + 0.003995 * s ** 2 + 3.16 * 10 ** (-6) * s + 2.571 * 10 ** (-10))
    tf13_2 = (-0.0003723 * s ** 3 - 3.404 * 10 ** (-8) * s ** 2 - 5.307 * 10 ** (-11) * s - 4.164 * 10 ** (-15)) / \
             (s ** 3 + 0.0001103 * s ** 2 + 1.31 * 10 ** (-7) * s + 1.117 * 10 ** (-11))
    # tf14_2 = (0.003898 * s + 1.485 * 10 ** (-5)) / (s + 0.001431) * exp(-1800 * s)
    tf14_2 = (0.003898 * s + 1.485 * 10 ** (-5)) / (s + 0.001431) * (1 / (1800 * s + 1))
    # Tei模型: Q=13500kW
    tf21_2 = (0.1775 * s ** 3 + 0.0002064 * s ** 2 - 9.543 * 10 ** (-8) * s + 2.038 * 10 ** (-10)) / \
             (s ** 3 + 0.001195 * s ** 2 + 6.846 * 10 ** (-7) * s + 1.494 * 10 ** (-10))
    tf22_2 = (-4.966 * 10 ** (-10) * s - 3.044 * 10 ** (-14)) / \
             (s ** 3 + 0.0009959 * s ** 2 + 3.211 * 10 ** (-7) * s + 1.862 * 10 ** (-11))
    tf23_2 = 0 / 1
    tf24_2 = 0 / 1
    # 13500kW模型列表
    tf2_EER_list = [[tf11_2, tf12_2, tf13_2, tf14_2]]
    tf2_Tei_list = [[tf21_2, tf22_2, tf23_2, tf24_2]]
    tf2_list = [tf2_EER_list[0], tf2_Tei_list[0]]

    # EER模型: Q=12500kW
    # tf11_3 = (-0.2361 * s ** 4 - 0.001279 * s ** 3 + 3.22 * 10 ** (-7) * s ** 2 + 1.541 * 10 ** (-10) * s +
    #           1.456 * 10 ** (-13)) / (s ** 4 + 0.003858 * s ** 3 + 3.092 * 10 ** (-6) * s ** 2 +
    #                                   1.446 * 10 ** (-9) * s + 3.564 * 10 ** (-13)) * exp(-4200 * s)
    tf11_3 = (-0.2361 * s ** 4 - 0.001279 * s ** 3 + 3.22 * 10 ** (-7) * s ** 2 + 1.541 * 10 ** (-10) * s +
              1.456 * 10 ** (-13)) / (s ** 4 + 0.003858 * s ** 3 + 3.092 * 10 ** (-6) * s ** 2 +
                                      1.446 * 10 ** (-9) * s + 3.564 * 10 ** (-13)) * (1 / (4200 * s + 1))
    tf12_3 = (-2.131 * 10 ** (-13) * s + 5.585 * 10 ** (-18)) / \
             (s ** 4 + 0.000621 * s ** 3 + 6.264 * 10 ** (-7) * s ** 2 + 7.814 * 10 ** (-11) * s + 1.5 * 10 ** (-15))
    tf13_3 = (-0.00393 * s ** 5 - 4.618 * 10 ** (-6) * s ** 4 - 1.412 * 10 ** (-8) * s ** 3 -
              8.998 * 10 ** (-12) * s ** 2 - 9.23 * 10 ** (-15) * s + 1.082 * 10 ** (-18)) / \
             (s ** 5 + 0.00119 * s ** 4 + 3.876 * 10 ** (-6) * s ** 3 + 2.474 * 10 ** (-9) * s ** 2 +
              2.9 * 10 ** (-12) * s + 5.021 * 10 ** (-16))
    tf14_3 = (7.066 * 10 ** (-10) * s ** 2 + 2.392 * 10 ** (-13) * s + 1.282 * 10 ** (-16)) / \
             (s ** 4 + 0.0004998 * s ** 3 + 2.31 * 10 ** (-7) * s ** 2 + 3.564 * 10 ** (-11) * s + 4.729 * 10 ** (-15))
    # Tei模型: Q=12500kW
    tf21_3 = (0.3239 * s ** 4 + 0.0001525 * s ** 3 + 9.674 * 10 ** (-7) * s ** 2 - 2.41 * 10 ** (-10) * s +
              1.547 * 10 ** (-13)) / (s ** 4 + 0.001208 * s ** 3 + 1.695 * 10 ** (-6) * s ** 2 +
                                      7.955 * 10 ** (-10) * s + 1.894 * 10 ** (-13))
    tf22_3 = (0.00381 * s ** 4 + 2.012 * 10 ** (-5) * s ** 3 + 1.265 * 10 ** (-8) * s ** 2 + 1.904 * 10 ** (-11) * s +
              4.537 * 10 ** (-15)) / (s ** 4 + 0.004844 * s ** 3 + 3.166 * 10 ** (-6) * s ** 2 +
                                      3.896 * 10 ** (-9) * s + 1.899 * 10 ** (-12))
    tf23_3 = 0 / 1
    tf24_3 = 0 / 1
    # 12500kW模型列表
    tf3_EER_list = [[tf11_3, tf12_3, tf13_3, tf14_3]]
    tf3_Tei_list = [[tf21_3, tf22_3, tf23_3, tf24_3]]
    tf3_list = [tf3_EER_list[0], tf3_Tei_list[0]]

    # EER模型: Q=12000kW
    tf11_4 = (-0.5214 * s ** 4 - 0.0006338 * s ** 3 - 3.742 * 10 ** (-7) * s ** 2 - 5.651 * 10 ** (-10) * s +
              9.898 * 10 ** (-14)) / (s ** 4 + 0.001048 * s ** 3 + 1.289 * 10 ** (-6) * s ** 2 +
                                      5.144 * 10 ** (-10) * s + 1.536 * 10 ** (-13))
    # tf12_4 = (3.074 * 10 ** (-10)) / (s ** 2 + 5.467 * 10 ** (-6) * s + 1.283 * 10 ** (-7)) * exp(-600 * s)
    tf12_4 = (3.074 * 10 ** (-10)) / (s ** 2 + 5.467 * 10 ** (-6) * s + 1.283 * 10 ** (-7)) * (1 / (600 * s + 1))
    tf13_4 = (-0.0001789 * s ** 4 - 4.168 * 10 ** (-7) * s ** 3 - 1.862 * 10 ** (-10) * s ** 2 -
              2.34 * 10 ** (-13) * s - 5.22 * 10 ** (-17)) / \
             (s ** 4 + 0.001027 * s ** 3 + 1.304 * 10 ** (-6) * s ** 2 + 5.543 * 10 ** (-10) * s + 1.923 * 10 ** (-13))
    # tf14_4 = (5.143 * 10 ** (-15) * s + 3.402 * 10 ** (-18)) / \
    #          (s ** 4 + 0.0003711 * s ** 3 + 1.486 * 10 ** (-7) * s ** 2 + 2.109 * 10 ** (-11) * s +
    #           3.337 * 10 ** (-15)) * exp(-600 * s)
    tf14_4 = (5.143 * 10 ** (-15) * s + 3.402 * 10 ** (-18)) / \
             (s ** 4 + 0.0003711 * s ** 3 + 1.486 * 10 ** (-7) * s ** 2 + 2.109 * 10 ** (-11) * s +
              3.337 * 10 ** (-15)) * (1 / (600 * s + 1))
    # Tei模型: Q=12000kW
    tf21_4 = (0.6136 * s ** 4 + 0.000452 * s ** 3 + 8.138 * 10 ** (-7) * s ** 2 + 1.122 * 10 ** (-11) * s +
              1.821 * 10 ** (-13)) / (s ** 4 + 0.0008454 * s ** 3 + 9.817 * 10 ** (-7) * s ** 2 +
                                      3.488 * 10 ** (-10) * s + 1.063 * 10 ** (-13))
    tf22_4 = (0.002951 * s ** 3 + 1.613 * 10 ** (-5) * s ** 2 + 7.492 * 10 ** (-9) * s + 1.765 * 10 ** (-12)) / \
             (s ** 3 + 0.005575 * s ** 2 + 2.327 * 10 ** (-6) * s + 1.257 * 10 ** (-9))
    tf23_4 = 0 / 1
    tf24_4 = 0 / 1
    # 12000kW模型列表
    tf4_EER_list = [[tf11_4, tf12_4, tf13_4, tf14_4]]
    tf4_Tei_list = [[tf21_4, tf22_4, tf23_4, tf24_4]]
    tf4_list = [tf4_EER_list[0], tf4_Tei_list[0]]

    # EER模型: Q=11500kW
    tf11_5 = (-1.075 * s ** 4 - 0.001424 * s ** 3 - 9.792 * 10 ** (-7) * s ** 2 - 8.657 * 10 ** (-10) * s +
              8.697 * 10 ** (-15)) / (s ** 4 + 0.001267 * s ** 3 + 1.148 * 10 ** (-6) * s ** 2 +
                                      5.407 * 10 ** (-10) * s + 1.406 * 10 ** (-13))
    tf12_5 = (0.0003248 * s ** 4 + 2.9 * 10 ** (-7) * s ** 3 + 1.039 * 10 ** (-11) * s ** 2 - 3.949 * 10 ** (-14) * s -
              1.145 * 10 ** (-17)) / (s ** 4 + 0.0005998 * s ** 3 + 6.248 * 10 ** (-7) * s ** 2 +
                                      1.05 * 10 ** (-10) * s + 3.125 * 10 ** (-14))
    tf13_5 = (-0.0005676 * s ** 5 - 4.252 * 10 ** (-7) * s ** 4 - 1.66 * 10 ** (-9) * s ** 3 -
              2.756 * 10 ** (-13) * s ** 2 - 4.023 * 10 ** (-16) * s + 1.461 * 10 ** (-21)) / \
             (s ** 5 + 0.0009969 * s ** 4 + 2.395 * 10 ** (-6) * s ** 3 + 8.491 * 10 ** (-10) * s ** 2 +
              5.155 * 10 ** (-13) * s + 1.106 * 10 ** (-17))
    tf14_5 = (1.263 * 10 ** (-10) * s + 1.399 * 10 ** (-13)) / (s ** 3 + 0.001578 * s ** 2 + 8.487 * 10 ** (-7) * s +
                                                                1.579 * 10 ** (-10))
    # Tei模型: Q=11500kW
    # tf21_5 = (0.0002182 * s + 4.239 * 10 ** (-7)) / (s ** 2 + 0.0006569 * s + 3.825 * 10 ** (-7)) * exp(-4800 * s)
    # tf22_5 = (-0.0002628 * s - 1.598 * 10 ** (-6)) / (s + 0.0007522) * exp(-2400 * s)
    tf21_5 = (0.0002182 * s + 4.239 * 10 ** (-7)) / (s ** 2 + 0.0006569 * s + 3.825 * 10 ** (-7)) * (1 / (4800 * s + 1))
    tf22_5 = (-0.0002628 * s - 1.598 * 10 ** (-6)) / (s + 0.0007522) * (1 / (2400 * s + 1))
    tf23_5 = 0 / 1
    tf24_5 = 0 / 1
    # 11500kW模型列表
    tf5_EER_list = [[tf11_5, tf12_5, tf13_5, tf14_5]]
    tf5_Tei_list = [[tf21_5, tf22_5, tf23_5, tf24_5]]
    tf5_list = [tf5_EER_list[0], tf5_Tei_list[0]]

    # EER模型: Q=10500kW
    tf11_6 = (-1.109 * s ** 4 - 0.001638 * s ** 3 - 1.078 * 10 ** (-6) * s ** 2 - 1.008 * 10 ** (-9) * s -
              1.256 * 10 ** (-15)) / (s ** 4 + 0.00135 * s ** 3 + 1.255 * 10 ** (-6) * s ** 2 +
                                      5.884 * 10 ** (-10) * s + 1.538 * 10 ** (-13))
    tf12_6 = (0.00147 * s ** 4 + 1.572 * 10 ** (-6) * s ** 3 + 3.504 * 10 ** (-9) * s ** 2 - 5.462 * 10 ** (-14) * s +
              5.259 * 10 ** (-19)) / (s ** 4 + 0.001538 * s ** 3 + 2.006 * 10 ** (-6) * s ** 2 +
                                      8.405 * 10 ** (-10) * s + 7.992 * 10 ** (-14))
    tf13_6 = (-0.0003407 * s ** 3 - 5.44 * 10 ** (-7) * s ** 2 + 1.737 * 10 ** (-11) * s - 3.131 * 10 ** (-14)) / \
             (s ** 3 + 0.001238 * s ** 2 + 6.782 * 10 ** (-8) * s + 8.398 * 10 ** (-11))
    # tf14_6 = (0.0004561 * s ** 2 + 5.327 * 10 ** (-7) * s + 3.856 * 10 ** (-11)) / \
    #          (s ** 2 + 0.0005306 * s + 7.473 * 10 ** (-8)) * exp(-600 * s)
    tf14_6 = (0.0004561 * s ** 2 + 5.327 * 10 ** (-7) * s + 3.856 * 10 ** (-11)) / \
             (s ** 2 + 0.0005306 * s + 7.473 * 10 ** (-8)) * (1 / (600 * s + 1))
    # Tei模型: Q=10500kW
    # tf21_6 = (0.1103 * s ** 3 + 0.0006908 * s ** 2 + 3.508 * 10 ** (-7) * s + 9.92 * 10 ** (-10)) / \
    #          (s ** 3 + 0.002458 * s ** 2 + 1.64 * 10 ** (-6) * s + 9.511 * 10 ** (-10)) * exp(-4800 * s)
    # tf22_6 = (0.0005909 * s - 1.099 * 10 ** (-6)) / (s + 0.0005635) * exp(-1800 * s)
    tf21_6 = (0.1103 * s ** 3 + 0.0006908 * s ** 2 + 3.508 * 10 ** (-7) * s + 9.92 * 10 ** (-10)) / \
             (s ** 3 + 0.002458 * s ** 2 + 1.64 * 10 ** (-6) * s + 9.511 * 10 ** (-10)) * (1 / (4800 * s + 1))
    tf22_6 = (0.0005909 * s - 1.099 * 10 ** (-6)) / (s + 0.0005635) * (1 / (1800 * s + 1))
    tf23_6 = 0 / 1
    tf24_6 = 0 / 1
    # 10500kW模型列表
    tf6_EER_list = [[tf11_6, tf12_6, tf13_6, tf14_6]]
    tf6_Tei_list = [[tf21_6, tf22_6, tf23_6, tf24_6]]
    tf6_list = [tf6_EER_list[0], tf6_Tei_list[0]]

    # EER模型: Q=10000kW
    tf11_7 = (-1.109 * s ** 4 - 0.001615 * s ** 3 - 1.064 * 10 ** (-6) * s ** 2 - 9.637 * 10 ** (-10) * s -
              3.612 * 10 ** (-15)) / (s ** 4 + 0.001342 * s ** 3 + 1.219 * 10 ** (-6) * s ** 2 +
                                      5.776 * 10 ** (-10) * s + 1.429 * 10 ** (-13))
    tf12_7 = (0.00173 * s ** 2 + 8.88 * 10 ** (-7) * s - 6.432 * 10 ** (-11)) / \
             (s ** 2 + 0.00054 * s + 2.115 * 10 ** (-7))
    tf13_7 = (1.118 * 10 ** (-10) * s ** 2 - 2.746 * 10 ** (-14) * s + 4.873 * 10 ** (-18)) / \
             (s ** 4 + 0.0003946 * s ** 3 + 4.163 * 10 ** (-7) * s ** 2 + 1.143 * 10 ** (-10) * s + 1.745 * 10 ** (-14))
    # tf14_7 = (-6.137 * 10 ** (-13) * s ** 2 + 2.331 * 10 ** (-16) * s - 1.284 * 10 ** (-20)) / \
    #          (s ** 5 + 0.003643 * s ** 4 + 1.748 * 10 ** (-6) * s ** 3 + 1.499 * 10 ** (-9) * s ** 2 +
    #           3.805 * 10 ** (-13) * s + 3.441 * 10 ** (-17)) * exp(-600 * s)
    tf14_7 = (-6.137 * 10 ** (-13) * s ** 2 + 2.331 * 10 ** (-16) * s - 1.284 * 10 ** (-20)) / \
             (s ** 5 + 0.003643 * s ** 4 + 1.748 * 10 ** (-6) * s ** 3 + 1.499 * 10 ** (-9) * s ** 2 +
              3.805 * 10 ** (-13) * s + 3.441 * 10 ** (-17)) * (1 / (600 * s + 1))
    # Tei模型: Q=10000kW
    # tf21_7 = (0.000129 * s + 3.788 * 10 ** (-7)) / (s ** 2 + 0.0007667 * s + 3.869 * 10 ** (-7)) * exp(-4800 * s)
    # tf22_7 = (-0.0002916 * s - 1.19 * 10 ** (-6)) / (s + 0.0004781) * exp(-1800 * s)
    tf21_7 = (0.000129 * s + 3.788 * 10 ** (-7)) / (s ** 2 + 0.0007667 * s + 3.869 * 10 ** (-7)) * (1 / (4800 * s + 1))
    tf22_7 = (-0.0002916 * s - 1.19 * 10 ** (-6)) / (s + 0.0004781) * (1 / (1800 * s + 1))
    tf23_7 = 0 / 1
    tf24_7 = 0 / 1
    # 10000kW模型列表
    tf7_EER_list = [[tf11_7, tf12_7, tf13_7, tf14_7]]
    tf7_Tei_list = [[tf21_7, tf22_7, tf23_7, tf24_7]]
    tf7_list = [tf7_EER_list[0], tf7_Tei_list[0]]

    # EER模型: Q=9500kW
    tf11_8 = (-1.124 * s ** 4 - 0.001494 * s ** 3 - 9.762 * 10 ** (-7) * s ** 2 - 8.705 * 10 ** (-10) * s -
               4.415 * 10 ** (-15)) / (s ** 4 + 0.001208 * s ** 3 + 1.119 * 10 ** (-6) * s ** 2 +
                                       5.043 * 10 ** (-10) * s + 1.218 * 10 ** (-13))
    tf12_8 = (0.001618 * s ** 4 + 8.529 * 10 ** (-7) * s ** 3 + 6.447 * 10 ** (-10) * s ** 2 +
               7.154 * 10 ** (-15) * s - 5.39 * 10 ** (-18)) / \
              (s ** 4 + 0.0006857 * s ** 3 + 5.734 * 10 ** (-7) * s ** 2 + 1.328 * 10 ** (-10) * s + 2.449 * 10 ** (-14))
    tf13_8 = (-0.000503 * s ** 5 - 5.702 * 10 ** (-7) * s ** 4 - 2.276 * 10 ** (-9) * s ** 3 -
               1.058 * 10 ** (-12) * s ** 2 - 1.356 * 10 ** (-15) * s - 3.546 * 10 ** (-19)) / \
              (s ** 5 + 0.001567 * s ** 4 + 3.83 * 10 ** (-6) * s ** 3 + 3.076 * 10 ** (-9) * s ** 2 +
               2.122 * 10 ** (-12) * s + 7.948 * 10 ** (-16))
    tf14_8 = (0.0123 * s ** 2 + 7.97 * 10 ** (-6) * s + 3.144 * 10 ** (-9)) / \
              (s ** 2 + 0.0003326 * s + 1.169 * 10 ** (-7))
    # Tei模型: Q=9500kW
    # tf21_8 = (0.0006472 * s ** 2 + 1.667 * 10 ** (-7) * s + 1.025 * 10 ** (-9)) / \
    #           (s ** 3 + 0.002134 * s ** 2 + 1.851 * 10 ** (-6) * s + 1.062 * 10 ** (-9)) * exp(-5400 * s)
    # tf22_8 = (-0.000228 * s ** 2 - 6.89 * 10 ** (-7) * s - 1.363 * 10 ** (-10)) / \
    #           (s ** 2 + 0.0004326 * s + 7.177 * 10 ** (-8)) * exp(-1800 * s)
    tf21_8 = (0.0006472 * s ** 2 + 1.667 * 10 ** (-7) * s + 1.025 * 10 ** (-9)) / \
             (s ** 3 + 0.002134 * s ** 2 + 1.851 * 10 ** (-6) * s + 1.062 * 10 ** (-9)) * (1 / (5400 * s + 1))
    tf22_8 = (-0.000228 * s ** 2 - 6.89 * 10 ** (-7) * s - 1.363 * 10 ** (-10)) / \
             (s ** 2 + 0.0004326 * s + 7.177 * 10 ** (-8)) * (1 / (1800 * s + 1))
    tf23_8 = 0 / 1
    tf24_8 = 0 / 1
    # 9500kW模型列表
    tf8_EER_list = [[tf11_8, tf12_8, tf13_8, tf14_8]]
    tf8_Tei_list = [[tf21_8, tf22_8, tf23_8, tf24_8]]
    tf8_list = [tf8_EER_list[0], tf8_Tei_list[0]]

    # EER模型: Q=6000kW
    tf11_9 = (-1.266 * s ** 4 - 0.0006481 * s ** 3 - 1.971 * 10 ** (-7) * s ** 2 - 7.817 * 10 ** (-11) * s +
               1.862 * 10 ** (-15)) / (s ** 4 + 0.0005583 * s ** 3 + 1.751 * 10 ** (-7) * s ** 2 +
                                       5.504 * 10 ** (-11) * s + 1.765 * 10 ** (-15))
    tf12_9 = (0.002659 * s ** 4 + 1.297 * 10 ** (-6) * s ** 3 + 1.111 * 10 ** (-9) * s ** 2 +
               2.873 * 10 ** (-13) * s - 1.46 * 10 ** (-18)) / \
              (s ** 4 + 0.0005088 * s ** 3 + 4.554 * 10 ** (-7) * s ** 2 + 1.266 * 10 ** (-10) * s + 2.121 * 10 ** (-14))
    tf13_9 = (-0.0002873 * s ** 4 - 1.499 * 10 ** (-7) * s ** 3 - 2.048 * 10 ** (-10) * s ** 2 -
               4.434 * 10 ** (-14) * s - 1.044 * 10 ** (-17)) / \
              (s ** 4 + 0.0005627 * s ** 3 + 6.638 * 10 ** (-7) * s ** 2 + 1.374 * 10 ** (-10) * s + 3.657 * 10 ** (-14))
    # tf14_9 = (0.0006828 * s ** 2 + 5.722 * 10 ** (-7) * s + 3.417 * 10 ** (-10)) / \
    #           (s ** 2 + 0.0004758 * s + 3.049 * 10 ** (-7)) * exp(-600 * s)
    tf14_9 = (0.0006828 * s ** 2 + 5.722 * 10 ** (-7) * s + 3.417 * 10 ** (-10)) / \
             (s ** 2 + 0.0004758 * s + 3.049 * 10 ** (-7)) * (1 / (600 * s + 1))
    # Tei模型: Q=6000kW
    # tf21_9 = (9.817 * 10 ** (-5) * s + 3.113 * 10 ** (-8)) / \
    #           (s ** 2 + 0.0002513 * s + 3.634 * 10 ** (-8)) * exp(-10200 * s)
    # tf22_9 = (-1.461 * 10 ** (-9)) / (s ** 2 + 0.00163 * s + 3.857 * 10 ** (-7)) * exp(-1800 * s)
    tf21_9 = (9.817 * 10 ** (-5) * s + 3.113 * 10 ** (-8)) / \
             (s ** 2 + 0.0002513 * s + 3.634 * 10 ** (-8)) * (1 / (10200 * s + 1))
    tf22_9 = (-1.461 * 10 ** (-9)) / (s ** 2 + 0.00163 * s + 3.857 * 10 ** (-7)) * (1 / (1800 * s + 1))
    tf23_9 = 0 / 1
    tf24_9 = 0 / 1
    # 6000kW模型列表
    tf9_EER_list = [[tf11_9, tf12_9, tf13_9, tf14_9]]
    tf9_Tei_list = [[tf21_9, tf22_9, tf23_9, tf24_9]]
    tf9_list = [tf9_EER_list[0], tf9_Tei_list[0]]

    # EER模型: Q=5000kW
    tf11_10 = (-1.242 * s ** 5 + 0.0001053 * s ** 4 - 1.365 * 10 ** (-6) * s ** 3 + 9.864 * 10 ** (-11) * s ** 2 -
              1.5 * 10 ** (-13) * s + 5.543 * 10 ** (-18)) / \
              (s ** 5 + 5.475 * 10 ** (-5) * s ** 4 + 1.036 * 10 ** (-6) * s ** 3 + 2.711 * 10 ** (-11) * s ** 2 +
              9.236 * 10 ** (-14) * s + 2.139 * 10 ** (-18))
    tf12_10 = (0.004082 * s ** 4 + 8.927 * 10 ** (-7) * s ** 3 + 3.405 * 10 ** (-9) * s ** 2 -
              2.148 * 10 ** (-13) * s + 4.067 * 10 ** (-18)) / \
              (s ** 4 + 0.0005428 * s ** 3 + 7.822 * 10 ** (-7) * s ** 2 + 1.234 * 10 ** (-10) * s + 6.248 * 10 ** (-15))
    tf13_10 = (-0.0002755 * s ** 5 - 1.446 * 10 ** (-7) * s ** 4 - 2.768 * 10 ** (-10) * s ** 3 -
              6.129 * 10 ** (-14) * s ** 2 - 2.485 * 10 ** (-17) * s - 1.268 * 10 ** (-21)) / \
              (s ** 5 + 0.0005695 * s ** 4 + 1.069 * 10 ** (-6) * s ** 3 + 2.04 * 10 ** (-10) * s ** 2 +
              1.101 * 10 ** (-13) * s + 2.84 * 10 ** (-18))
    tf14_10 = (-0.0004273 * s ** 4 + 3.027 * 10 ** (-7) * s ** 3 + 3.594 * 10 ** (-10) * s ** 2 +
              6.384 * 10 ** (-13) * s - 7.042 * 10 ** (-18)) / \
              (s ** 4 + 0.004333 * s ** 3 + 3.076 * 10 ** (-6) * s ** 2 + 1.692 * 10 ** (-9) * s + 5.108 * 10 ** (-18))
    # Tei模型: Q=5000kW
    # tf21_10 = (0.1322 * s ** 2 + 6.752 * 10 ** (-5) * s + 8.733 * 10 ** (-8)) / \
    #           (s ** 2 + 0.0001986 * s + 8.652 * 10 ** (-8)) * exp(-10200 * s)
    # tf22_10 = (-1.576 * 10 ** (-6)) / (s + 0.0003493) * exp(-4200 * s)
    tf21_10 = (0.1322 * s ** 2 + 6.752 * 10 ** (-5) * s + 8.733 * 10 ** (-8)) / \
             (s ** 2 + 0.0001986 * s + 8.652 * 10 ** (-8)) * (1 / (10200 * s + 1))
    tf22_10 = (-1.576 * 10 ** (-6)) / (s + 0.0003493) * (1 / (4200 * s + 1))
    tf23_10 = 0 / 1
    tf24_10 = 0 / 1
    # 5000kW模型列表
    tf10_EER_list = [[tf11_10, tf12_10, tf13_10, tf14_10]]
    tf10_Tei_list = [[tf21_10, tf22_10, tf23_10, tf24_10]]
    tf10_list = [tf10_EER_list[0], tf10_Tei_list[0]]

    # 模型列表
    plant_EER_list = [tf1_EER_list, tf2_EER_list, tf3_EER_list, tf4_EER_list, tf5_EER_list,
                      tf6_EER_list, tf7_EER_list, tf8_EER_list, tf9_EER_list, tf10_EER_list]
    plant_Tei_list = [tf1_Tei_list, tf2_Tei_list, tf3_Tei_list, tf4_Tei_list, tf5_Tei_list,
                      tf6_Tei_list, tf7_Tei_list, tf8_Tei_list, tf9_Tei_list, tf10_Tei_list]
    plant_list = [tf1_list, tf2_list, tf3_list, tf4_list, tf5_list, tf6_list, tf7_list, tf8_list, tf9_list, tf10_list]
    # 每个模型对应的制冷功率Q的列表
    Q_plant_list = [14000, 13500, 12500, 12000, 11500, 10500, 10000, 9500, 6000, 5000]

    # 返回结果
    return plant_list, plant_EER_list, plant_Tei_list, Q_plant_list