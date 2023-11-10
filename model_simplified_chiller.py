"""
用于测试的simplified_chiller_model.fmu的相关内容
"""
import numpy as np
from control.matlab import *

def model_input_type():
    """
    模型输入的数据类型
    Returns:

    """
    fmu_input_type = [("time", np.float_), ("Two", np.float_), ("Q_set", np.float_), ("chiller_turn1", np.bool_),
                      ("chiller_Teo_set", np.float_), ("chiller_f_chilled_pump1", np.float_),
                      ("chiller_f_cooling_pump1", np.float_), ("chiller_f_cooling_tower1", np.float_)]
    return fmu_input_type


def model_dynamics_simplified_chiller():
    """

    Returns:

    """

    # 传递函数
    s = tf("s")
    # 预测时域Np
    Np = 70
    # 控制时域Nc
    Nc = 15

    # EER模型: Q=700kW
    tf11_7 = (-2.41 * s + 2.451 * 10 ** (-5)) / (s + 0.004431)
    tf12_7 = (-1.247 * 10 ** (-5)) / (s + 0.005522)
    tf13_7 = (-0.001902 * s - 3.093 * 10 ** (-5)) / (s + 0.01621)
    tf14_7 = (-0.00307 * s - 4.51 * 10 ** (-5)) / (s + 0.0155)
    tf7_EER_list = [[tf11_7, tf12_7, tf13_7, tf14_7]]
    # Tei模型: Q=700kW
    tf21_7 = (0.004483) / (s + 0.004485)
    tf22_7 = (-2.772 * 10 ** (-6)) / (s + 0.003637)
    tf23_7 = 0 / 1
    tf24_7 = 0 / 1
    tf7_Tei_list = [[tf21_7, tf22_7, tf23_7, tf24_7]]
    # 模型列表
    tf7_list = [tf7_EER_list[0], tf7_Tei_list[0]]
    # 控制器参数
    r1_1 = 297.74
    r2_1 = 182.07
    r3_1 = 186.17
    r4_1 = 387.49
    r1_list = [r1_1, r2_1, r3_1, r4_1]
    q1_1 = 5719.22
    q2_1 = 8694.95
    q1_list = [q1_1, q2_1]

    # EER模型: Q=1400kW
    tf11_14 = (-1.775 * s + 7.987 * 10 ** (-5)) / (s + 0.004408)
    tf12_14 = (-1.556 * 10 ** (-5)) / (s + 0.004713)
    tf13_14 = (-0.002802 * s - 4.863 * 10 ** (-5)) / (s + 0.01729)
    tf14_14 = (-0.004068 * s - 5.615 * 10 ** (-5)) / (s + 0.01569)
    tf14_EER_list = [[tf11_14, tf12_14, tf13_14, tf14_14]]
    # Tei模型: Q=1400kW
    tf21_14 = (0.004492) / (s + 0.004493)
    tf22_14 = (-6.412 * 10 ** (-6)) / (s + 0.003627)
    tf23_14 = 0 / 1
    tf24_14 = 0 / 1
    tf14_Tei_list = [[tf21_14, tf22_14, tf23_14, tf24_14]]
    # 模型列表
    tf14_list = [tf14_EER_list[0], tf14_Tei_list[0]]
    # 控制器参数
    r1_2 = 1000.0
    r2_2 = 720.42
    r3_2 = 332.77
    r4_2 = 0.01
    r2_list = [r1_2, r2_2, r3_2, r4_2]
    q1_2 = 9198.0
    q2_2 = 8698.01
    q2_list = [q1_2, q2_2]

    # EER模型: Q=1900kW
    tf11_19 = (-1.346 * s + 0.0001693) / (s + 0.004625)
    tf12_19 = (-2.075 * 10 ** (-5)) / (s + 0.00573)
    tf13_19 = (-0.003018 * s - 5.534 * 10 ** (-5)) / (s + 0.01826)
    tf14_19 = (-0.00372 * s - 4.494 * 10 ** (-5)) / (s + 0.01573)
    tf19_EER_list = [[tf11_19, tf12_19, tf13_19, tf14_19]]
    # Tei模型: Q=1900kW
    tf21_19 = (0.004492) / (s + 0.004494)
    tf22_19 = (-9.011 * 10 ** (-6)) / (s + 0.003625)
    tf23_19 = 0 / 1
    tf24_19 = 0 / 1
    tf19_Tei_list = [[tf21_19, tf22_19, tf23_19, tf24_19]]
    # 模型列表
    tf19_list = [tf19_EER_list[0], tf19_Tei_list[0]]
    # 控制器参数
    r1_3 = 1000.0
    r2_3 = 1000.0
    r3_3 = 0.01
    r4_3 = 0.01
    r3_list = [r1_3, r2_3, r3_3, r4_3]
    q1_3 = 10000.0
    q2_3 = 4174.43
    q3_list = [q1_3, q2_3]

    # EER模型: Q=2300kW
    tf11_23 = (-0.9239 * s + 0.000317) / (s + 0.005142)
    tf12_23 = (-0.001944 * s - 1.485 * 10 ** (-5)) / (s + 0.004099)
    tf13_23 = (-0.002924 * s - 5.703 * 10 ** (-5)) / (s + 0.0194)
    tf14_23 = (-0.002697 * s - 2.259 * 10 ** (-5)) / (s + 0.01584)
    tf23_EER_list = [[tf11_23, tf12_23, tf13_23, tf14_23]]
    # Tei模型: Q=2300kW
    tf21_23 = (0.004492) / (s + 0.004493)
    tf22_23 = (-1.109 * 10 ** (-5)) / (s + 0.003624)
    tf23_23 = 0 / 1
    tf24_23 = 0 / 1
    tf23_Tei_list = [[tf21_23, tf22_23, tf23_23, tf24_23]]
    # 模型列表
    tf23_list = [tf23_EER_list[0], tf23_Tei_list[0]]
    # 控制器参数
    r1_4 = 1000.0
    r2_4 = 1000.0
    r3_4 = 0.01
    r4_4 = 0.01
    r4_list = [r1_4, r2_4, r3_4, r4_4]
    q1_4 = 9429.65
    q2_4 = 6255.02
    q4_list = [q1_4, q2_4]

    # EER模型: Q=2500kW
    tf11_25 = (-0.6739 * s + 0.0004626) / (s + 0.005839)
    tf12_25 = (-0.002424 * s - 2.059 * 10 ** (-5)) / (s + 0.005822)
    tf13_25 = (-0.002786 * s - 5.642 * 10 ** (-5)) / (s + 0.02013)
    tf14_25 = (-0.001909 * s - 6.022 * 10 ** (-6)) / (s + 0.01585)
    tf25_EER_list = [[tf11_25, tf12_25, tf13_25, tf14_25]]
    # Tei模型: Q=2500kW
    tf21_25 = (0.004492) / (s + 0.004493)
    tf22_25 = (-1.213 * 10 ** (-5)) / (s + 0.003624)
    tf23_25 = 0 / 1
    tf24_25 = 0 / 1
    tf25_Tei_list = [[tf21_25, tf22_25, tf23_25, tf24_25]]
    # 模型列表
    tf25_list = [tf25_EER_list[0], tf25_Tei_list[0]]
    # 控制器参数
    r1_5 = 434.37
    r2_5 = 0.01
    r3_5 = 0.01
    r4_5 = 277.48
    r5_list = [r1_5, r2_5, r3_5, r4_5]
    q1_5 = 5341.33
    q2_5 = 1636.96
    q5_list = [q1_5, q2_5]

    # EER模型: Q=2700kW
    tf11_27 = (-0.3897 * s + 0.0007994) / (s + 0.007876)
    tf12_27 = (-0.003481 * s - 2.426 * 10 ** (-6)) / (s + 0.0007144)
    tf13_27 = (-0.002589 * s - 5.471 * 10 ** (-5)) / (s + 0.02099)
    tf14_27 = (-0.0009115 * s + 1.451 * 10 ** (-5)) / (s + 0.01588)
    tf27_EER_list = [[tf11_27, tf12_27, tf13_27, tf14_27]]
    # Tei模型: Q=2700kW
    tf21_27 = (0.004492) / (s + 0.004493)
    tf22_27 = (-1.317 * 10 ** (-5)) / (s + 0.003624)
    tf23_27 = 0 / 1
    tf24_27 = 0 / 1
    tf27_Tei_list = [[tf21_27, tf22_27, tf23_27, tf24_27]]
    # 模型列表
    tf27_list = [tf27_EER_list[0], tf27_Tei_list[0]]
    # 控制器参数
    r1_6 = 567.74
    r2_6 = 0.01
    r3_6 = 0.01
    r4_6 = 1000.0
    r6_list = [r1_6, r2_6, r3_6, r4_6]
    q1_6 = 5945.44
    q2_6 = 7829.07
    q6_list = [q1_6, q2_6]

    # EER模型: Q=2900kW
    tf11_29 = ((0.002897 * s + 4.376 * 10 ** (-6)) / (s ** 2 + 0.01348 * s + 3.397 * 10 ** (-5))) * (1 / (60 * s + 1))
    tf12_29 = (-0.004234 * s - 6.098 * 10 ** (-6)) / (s + 0.001901)
    tf13_29 = (-0.002334 * s - 5.161 * 10 ** (-5)) / (s + 0.02193)
    tf14_29 = (4.372 * 10 ** (-5)) / (s + 0.01761)
    tf29_EER_list = [[tf11_29, tf12_29, tf13_29, tf14_29]]
    # Tei模型: Q=2900kW
    tf21_29 = (0.004492) / (s + 0.004493)
    tf22_29 = (-1.421 * 10 ** (-5)) / (s + 0.003623)
    tf23_29 = 0 / 1
    tf24_29 = 0 / 1
    tf29_Tei_list = [[tf21_29, tf22_29, tf23_29, tf24_29]]
    # 模型列表
    tf29_list = [tf29_EER_list[0], tf29_Tei_list[0]]
    # 控制器参数
    r1_7 = 0.01
    r2_7 = 0.01
    r3_7 = 0.01
    r4_7 = 350.69
    r7_list = [r1_7, r2_7, r3_7, r4_7]
    q1_7 = 8233.47
    q2_7 = 669.3
    q7_list = [q1_7, q2_7]

    # 模型列表
    Np_list = [Np, Np, Np, Np, Np, Np, Np]
    Nc_list = [Nc, Nc, Nc, Nc, Nc, Nc, Nc]
    model_EER_list = [tf7_EER_list, tf14_EER_list, tf19_EER_list, tf23_EER_list, tf25_EER_list, tf27_EER_list, tf29_EER_list]
    model_Tei_list = [tf7_Tei_list, tf14_Tei_list, tf19_Tei_list, tf23_Tei_list, tf25_Tei_list, tf27_Tei_list, tf29_Tei_list]
    model_list = [tf7_list, tf14_list, tf19_list, tf23_list, tf25_list, tf27_list, tf29_list]
    r_list = [r1_list, r2_list, r3_list, r4_list, r5_list, r6_list, r7_list]
    q_list = [q1_list, q2_list, q3_list, q4_list, q5_list, q6_list, q7_list]
    q_EER_list = [[q1_list[0]], [q2_list[0]], [q3_list[0]], [q4_list[0]], [q5_list[0]], [q6_list[0]], [q7_list[0]]]
    q_Tei_list = [[q1_list[1]], [q2_list[1]], [q3_list[1]], [q4_list[1]], [q5_list[1]], [q6_list[1]], [q7_list[1]]]
    # 每个模型对应的制冷功率Q的列表
    Q_model_list = [700, 1400, 1900, 2300, 2500, 2700, 2900]
    # 返回结果
    return (Q_model_list, model_list, model_EER_list, model_Tei_list, Np_list, Nc_list, r_list, q_list,
            q_EER_list, q_Tei_list)


def plant_dynamics_simplified_chiller():
    """
    模型采样周期：60秒

    Returns:

    """
    # 传递函数
    s = tf("s")

    # EER模型: Q=100kW
    tf12_1 = (-0.000836 * s - 1.911 * 10 ** (-6)) / (s + 0.003335)
    tf13_1 = (-0.0004183 * s - 6.532 * 10 ** (-6)) / (s + 0.01559)
    tf14_1 = (-0.0007005 * s - 1.06 * 10 ** (-5)) / (s + 0.01537)
    tf1_EER_list = [[tf12_1, tf13_1, tf14_1]]
    # Tei模型: Q=100kW
    tf21_1 = (0.004489) / (s + 0.00449)
    tf22_1 = (3.492 * 10 ** (-7)) / (s + 0.003496)
    tf23_1 = 0 / 1
    tf24_1 = 0 / 1
    tf1_Tei_list = [[tf21_1, tf22_1, tf23_1, tf24_1]]
    # 模型列表
    tf1_list = [tf1_EER_list[0], tf1_Tei_list[0]]

    # EER模型: Q=200kW
    tf11_2 = ((-1.152 * s ** 3 + 0.001593 * s ** 2 - 4.698 * 10 ** (-5) * s + 3.05 * 10 ** (-10)) /
              (s ** 3 + 0.003869 * s ** 2 + 5.447 * 10 ** (-5) * s + 1.29 * 10 ** (-7)))
    tf12_2 = (-0.0008652 * s - 3.068 * 10 ** (-6)) / (s + 0.003182)
    tf13_2 = (-0.0007503 * s - 1.179 * 10 ** (-5)) / (s + 0.01568)
    tf14_2 = (-0.001254 * s - 1.887 * 10 ** (-5)) / (s + 0.01539)
    tf2_EER_list = [[tf11_2, tf12_2, tf13_2, tf14_2]]
    # Tei模型: Q=200kW
    tf21_2 = (0.004488) / (s + 0.004489)
    tf22_2 = (-1.716 * 10 ** (-7)) / (s + 0.003918)
    tf23_2 = 0 / 1
    tf24_2 = 0 / 1
    tf2_Tei_list = [[tf21_2, tf22_2, tf23_2, tf24_2]]
    # 模型列表
    tf2_list = [tf2_EER_list[0], tf2_Tei_list[0]]

    # EER模型: Q=300kW
    tf11_3 = (-1.754 * s ** 3 + 8.598 * 10 ** (-5) * s ** 2 - 0.0001576 * s + 9.288 * 10 ** (-10)) / (
                s ** 3 + 0.006251 * s ** 2 + 0.0001097 * s + 3.292 * 10 ** (-7))
    tf12_3 = (-0.0008775 * s - 4.09 * 10 ** (-6)) / (s + 0.003171)
    tf13_3 = (-0.001033 * s - 1.612 * 10 ** (-5)) / (s + 0.01556)
    tf14_3 = (-0.001718 * s - 2.568 * 10 ** (-5)) / (s + 0.01536)
    tf3_EER_list = [[tf11_3, tf12_3, tf13_3, tf14_3]]
    # Tei模型: Q=300kW
    tf21_3 = (0.004492) / (s + 0.004493)
    tf22_3 = (-6.895 * 10 ** (-7)) / (s + 0.003678)
    tf23_3 = 0 / 1
    tf24_3 = 0 / 1
    tf3_Tei_list = [[tf21_3, tf22_3, tf23_3, tf24_3]]
    # 模型列表
    tf3_list = [tf3_EER_list[0], tf3_Tei_list[0]]

    # EER模型: Q=400kW
    tf11_4 = ((-2.106 * s ** 3 - 0.003003 * s ** 2 - 0.0003945 * s + 2.551 * 10 ** (-9)) /
              (s ** 3 + 0.009094 * s ** 2 + 0.0002191 * s + 7.426 * 10 ** (-7)))
    tf12_4 = (-0.0008794 * s - 4.992 * 10 ** (-6)) / (s + 0.003177)
    tf13_4 = (-0.001283 * s - 2.091 * 10 ** (-5)) / (s + 0.01625)
    tf14_4 = (-0.002122 * s - 3.126 * 10 ** (-5)) / (s + 0.01523)
    tf4_EER_list = [[tf11_4, tf12_4, tf13_4, tf14_4]]
    # Tei模型: Q=400kW
    tf21_4 = (0.00449) / (s + 0.004491)
    tf22_4 = (-1.209 * 10 ** (-6)) / (s + 0.003651)
    tf23_4 = 0 / 1
    tf24_4 = 0 / 1
    tf4_Tei_list = [[tf21_4, tf22_4, tf23_4, tf24_4]]
    # 模型列表
    tf4_list = [tf4_EER_list[0], tf4_Tei_list[0]]

    # EER模型: Q=500kW
    tf11_5 = ((-2.302 * s ** 3 - 0.01303 * s ** 2 - 0.0009047 * s + 6.7 * 10 ** (-9)) /
              (s ** 3 + 0.01464 * s ** 2 + 0.0004544 * s + 1.652 * 10 ** (-6)))
    tf12_5 = (-0.0008754 * s - 5.8 * 10 ** (-6)) / (s + 0.003182)
    tf13_5 = (-0.001509 * s - 2.417 * 10 ** (-5)) / (s + 0.01598)
    tf14_5 = (-0.002478 * s - 3.663 * 10 ** (-5)) / (s + 0.01539)
    tf5_EER_list = [[tf11_5, tf12_5, tf13_5, tf14_5]]
    # Tei模型: Q=500kW
    tf21_5 = (0.004487) / (s + 0.004489)
    tf22_5 = (-1.728 * 10 ** (-6)) / (s + 0.00364)
    tf23_5 = 0 / 1
    tf24_5 = 0 / 1
    tf5_Tei_list = [[tf21_5, tf22_5, tf23_5, tf24_5]]
    # 模型列表
    tf5_list = [tf5_EER_list[0], tf5_Tei_list[0]]

    # EER模型: Q=600kW
    tf11_6 = ((-2.419 * s ** 3 - 0.02929 * s ** 2 - 0.003103 * s + 2.714 * 10 ** (-8)) /
              (s ** 3 + 0.02661 * s ** 2 + 0.001428 * s + 5.651 * 10 ** (-6)))
    tf12_6 = (-1.24 * 10 ** (-5)) / (s + 0.006054)
    tf13_6 = (-0.001714 * s - 2.765 * 10 ** (-5)) / (s + 0.01609)
    tf14_6 = (-0.002792 * s - 4.112 * 10 ** (-5)) / (s + 0.01542)
    tf6_EER_list = [[tf11_6, tf12_6, tf13_6, tf14_6]]
    # Tei模型: Q=600kW
    tf21_6=(0.004489)/(s+0.004491)
    tf22_6=(-2.252*10**(-6))/(s+0.003641)
    tf23_6=(0)/(1)
    tf24_6=(0)/(1)
    tf6_Tei_list = [[tf21_6, tf22_6, tf23_6, tf24_6]]
    # 模型列表
    tf6_list = [tf6_EER_list[0], tf6_Tei_list[0]]

    # EER模型: Q=700kW
    tf11_7 = (-2.41 * s + 2.451 * 10 ** (-5)) / (s + 0.004431)
    tf12_7 = (-1.247 * 10 ** (-5)) / (s + 0.005522)
    tf13_7 = (-0.001902 * s - 3.093 * 10 ** (-5)) / (s + 0.01621)
    tf14_7 = (-0.00307 * s - 4.51 * 10 ** (-5)) / (s + 0.0155)
    tf7_EER_list = [[tf11_7, tf12_7, tf13_7, tf14_7]]
    # Tei模型: Q=700kW
    tf21_7 = (0.004483) / (s + 0.004485)
    tf22_7 = (-2.772 * 10 ** (-6)) / (s + 0.003637)
    tf23_7 = 0 / 1
    tf24_7 = 0 / 1
    tf7_Tei_list = [[tf21_7, tf22_7, tf23_7, tf24_7]]
    # 模型列表
    tf7_list = [tf7_EER_list[0], tf7_Tei_list[0]]

    # EER模型: Q=800kW
    tf11_8 = (-2.338 * s + 2.977 * 10 ** (-5)) / (s + 0.004488)
    tf12_8 = (-1.271 * 10 ** (-5)) / (s + 0.005185)
    tf13_8 = (-0.002074 * s - 3.365 * 10 ** (-5)) / (s + 0.01618)
    tf14_8 = (-0.003312 * s - 4.884 * 10 ** (-5)) / (s + 0.01567)
    tf8_EER_list = [[tf11_8, tf12_8, tf13_8, tf14_8]]
    # Tei模型: Q=800kW
    tf21_8 = (0.004491) / (s + 0.004492)
    tf22_8 = (-3.292 * 10 ** (-6)) / (s + 0.003635)
    tf23_8 = 0 / 1
    tf24_8 = 0 / 1
    tf8_Tei_list = [[tf21_8, tf22_8, tf23_8, tf24_8]]
    # 模型列表
    tf8_list = [tf8_EER_list[0], tf8_Tei_list[0]]

    # EER模型: Q=900kW
    tf11_9 = (-2.205 * s + 3.553 * 10 ** (-5)) / (s + 0.004413)
    tf12_9 = (-1.305 * 10 ** (-5)) / (s + 0.004965)
    tf13_9 = (-0.00223 * s - 3.697 * 10 ** (-5)) / (s + 0.01652)
    tf14_9 = (-0.003522 * s - 5.079 * 10 ** (-5)) / (s + 0.01545)
    tf9_EER_list = [[tf11_9, tf12_9, tf13_9, tf14_9]]
    # Tei模型: Q=900kW
    tf21_9 = (0.004491) / (s + 0.004493)
    tf22_9 = (-3.813 * 10 ** (-6)) / (s + 0.003633)
    tf23_9 = 0 / 1
    tf24_9 = 0 / 1
    tf9_Tei_list = [[tf21_9, tf22_9, tf23_9, tf24_9]]
    # 模型列表
    tf9_list = [tf9_EER_list[0], tf9_Tei_list[0]]

    # EER模型: Q=1000kW
    tf11_10 = (-2.107 * s + 4.222 * 10 ** (-5)) / (s + 0.004389)
    tf12_10 = (-1.345 * 10 ** (-5)) / (s + 0.004818)
    tf13_10 = (-0.002373 * s - 3.96 * 10 ** (-5)) / (s + 0.01663)
    tf14_10 = (-0.003698 * s - 5.298 * 10 ** (-5)) / (s + 0.01549)
    tf10_EER_list = [[tf11_10, tf12_10, tf13_10, tf14_10]]
    # Tei模型: Q=1000kW
    tf21_10 = (0.004491) / (s + 0.004493)
    tf22_10 = (-4.332 * 10 ** (-6)) / (s + 0.003631)
    tf23_10 = 0 / 1
    tf24_10 = 0 / 1
    tf10_Tei_list = [[tf21_10, tf22_10, tf23_10, tf24_10]]
    # 模型列表
    tf10_list = [tf10_EER_list[0], tf10_Tei_list[0]]

    # EER模型: Q=1100kW
    tf11_11 = (-2.017 * s + 4.976 * 10 ** (-5)) / (s + 0.004378)
    tf12_11 = (-1.39 * 10 ** (-5)) / (s + 0.004729)
    tf13_11 = (-0.002501 * s - 4.233 * 10 ** (-5)) / (s + 0.01687)
    tf14_11 = (-0.003841 * s - 5.458 * 10 ** (-5)) / (s + 0.01552)
    tf11_EER_list = [[tf11_11, tf12_11, tf13_11, tf14_11]]
    # Tei模型: Q=1100kW
    tf21_11 = (0.004492) / (s + 0.004493)
    tf22_11 = (-4.852 * 10 ** (-6)) / (s + 0.00363)
    tf23_11 = 0 / 1
    tf24_11 = 0 / 1
    tf11_Tei_list = [[tf21_11, tf22_11, tf23_11, tf24_11]]
    # 模型列表
    tf11_list = [tf11_EER_list[0], tf11_Tei_list[0]]

    # EER模型: Q=1200kW
    tf11_12 = (-1.934 * s + 5.844 * 10 ** (-5)) / (s + 0.004379)
    tf12_12 = (-1.44 * 10 ** (-5)) / (s + 0.004684)
    tf13_12 = (-0.002615 * s - 4.438 * 10 ** (-5)) / (s + 0.01691)
    tf14_12 = (-0.003951 * s - 5.575 * 10 ** (-5)) / (s + 0.01559)
    tf12_EER_list = [[tf11_12, tf12_12, tf13_12, tf14_12]]
    # Tei模型: Q=1200kW
    tf21_12 = (0.004492) / (s + 0.004493)
    tf22_12 = (-5.372 * 10 ** (-6)) / (s + 0.003628)
    tf23_12 = 0 / 1
    tf24_12 = 0 / 1
    tf12_Tei_list = [[tf21_12, tf22_12, tf23_12, tf24_12]]
    # 模型列表
    tf12_list = [tf12_EER_list[0], tf12_Tei_list[0]]

    # EER模型: Q=1300kW
    tf11_13 = (-1.854 * s + 6.837 * 10 ** (-5)) / (s + 0.00439)
    tf12_13 = (-1.495 * 10 ** (-5)) / (s + 0.00468)
    tf13_13 = (-0.002715 * s - 4.708 * 10 ** (-5)) / (s + 0.01727)
    tf14_13 = (-0.004027 * s - 5.584 * 10 ** (-5)) / (s + 0.01553)
    tf13_EER_list = [[tf11_13, tf12_13, tf13_13, tf14_13]]
    # Tei模型: Q=1300kW
    tf21_13 = (0.004492) / (s + 0.004493)
    tf22_13 = (-5.892 * 10 ** (-6)) / (s + 0.003628)
    tf23_13 = 0 / 1
    tf24_13 = 0 / 1
    tf13_Tei_list = [[tf21_13, tf22_13, tf23_13, tf24_13]]
    # 模型列表
    tf13_list = [tf13_EER_list[0], tf13_Tei_list[0]]

    # EER模型: Q=1400kW
    tf11_14 = (-1.775 * s + 7.987 * 10 ** (-5)) / (s + 0.004408)
    tf12_14 = (-1.556 * 10 ** (-5)) / (s + 0.004713)
    tf13_14 = (-0.002802 * s - 4.863 * 10 ** (-5)) / (s + 0.01729)
    tf14_14 = (-0.004068 * s - 5.615 * 10 ** (-5)) / (s + 0.01569)
    tf14_EER_list = [[tf11_14, tf12_14, tf13_14, tf14_14]]
    # Tei模型: Q=1400kW
    tf21_14 = (0.004492) / (s + 0.004493)
    tf22_14 = (-6.412 * 10 ** (-6)) / (s + 0.003627)
    tf23_14 = 0 / 1
    tf24_14 = 0 / 1
    tf14_Tei_list = [[tf21_14, tf22_14, tf23_14, tf24_14]]
    # 模型列表
    tf14_list = [tf14_EER_list[0], tf14_Tei_list[0]]

    # EER模型: Q=1500kW
    tf11_15 = (-1.694 * s + 9.303 * 10 ** (-5)) / (s + 0.004434)
    tf12_15 = (-1.625 * 10 ** (-5)) / (s + 0.004789)
    tf13_15 = (-0.002874 * s - 4.887 * 10 ** (-5)) / (s + 0.01694)
    tf14_15 = (-0.004074 * s - 5.523 * 10 ** (-5)) / (s + 0.01569)
    tf15_EER_list = [[tf11_15, tf12_15, tf13_15, tf14_15]]
    # Tei模型: Q=1500kW
    tf21_15 = (0.004492) / (s + 0.004493)
    tf22_15 = (-6.931 * 10 ** (-6)) / (s + 0.003626)
    tf23_15 = 0 / 1
    tf24_15 = 0 / 1
    tf15_Tei_list = [[tf21_15, tf22_15, tf23_15, tf24_15]]
    # 模型列表
    tf15_list = [tf15_EER_list[0], tf15_Tei_list[0]]

    # EER模型: Q=1600kW
    tf11_16 = (-1.612 * s + 0.0001082) / (s + 0.004467)
    tf12_16 = (-1.705 * 10 ** (-5)) / (s + 0.004912)
    tf13_16 = (-0.002932 * s - 5.135 * 10 ** (-5)) / (s + 0.01744)
    tf14_16 = (-0.004042 * s - 5.3 * 10 ** (-5)) / (s + 0.0155)
    tf16_EER_list = [[tf11_16, tf12_16, tf13_16, tf14_16]]
    # Tei模型: Q=1600kW
    tf21_16 = (0.004492) / (s + 0.004493)
    tf22_16 = (-7.45 * 10 ** (-6)) / (s + 0.003625)
    tf23_16 = 0 / 1
    tf24_16 = 0 / 1
    tf16_Tei_list = [[tf21_16, tf22_16, tf23_16, tf24_16]]
    # 模型列表
    tf16_list = [tf16_EER_list[0], tf16_Tei_list[0]]

    # EER模型: Q=1700kW
    tf11_17 = (-1.527 * s + 0.0001257) / (s + 0.004508)
    tf12_17 = (-1.801 * 10 ** (-5)) / (s + 0.005095)
    tf13_17 = (-0.002975 * s - 5.278 * 10 ** (-5)) / (s + 0.01767)
    tf14_17 = (-0.003975 * s - 5.157 * 10 ** (-5)) / (s + 0.01574)
    tf17_EER_list = [[tf11_17, tf12_17, tf13_17, tf14_17]]
    # Tei模型: Q=1700kW
    tf21_17 = (0.004492) / (s + 0.004493)
    tf22_17 = (-7.971 * 10 ** (-6)) / (s + 0.003625)
    tf23_17 = 0 / 1
    tf24_17 = 0 / 1
    tf17_Tei_list = [[tf21_17, tf22_17, tf23_17, tf24_17]]
    # 模型列表
    tf17_list = [tf17_EER_list[0], tf17_Tei_list[0]]

    # EER模型: Q=1800kW
    tf11_18 = (-1.439 * s + 0.0001459) / (s + 0.00456)
    tf12_18 = (-1.921 * 10 ** (-5)) / (s + 0.005357)
    tf13_18 = (-0.003004 * s - 5.395 * 10 ** (-5)) / (s + 0.01788)
    tf14_18 = (-0.003868 * s - 4.847 * 10 ** (-5)) / (s + 0.01569)
    tf18_EER_list = [[tf11_18, tf12_18, tf13_18, tf14_18]]
    # Tei模型: Q=1800kW
    tf21_18 = (0.004492) / (s + 0.004493)
    tf22_18 = (-8.491 * 10 ** (-6)) / (s + 0.003625)
    tf23_18 = 0 / 1
    tf24_18 = 0 / 1
    tf18_Tei_list = [[tf21_18, tf22_18, tf23_18, tf24_18]]
    # 模型列表
    tf18_list = [tf18_EER_list[0], tf18_Tei_list[0]]

    # EER模型: Q=1900kW
    tf11_19 = (-1.346 * s + 0.0001693) / (s + 0.004625)
    tf12_19 = (-2.075 * 10 ** (-5)) / (s + 0.00573)
    tf13_19 = (-0.003018 * s - 5.534 * 10 ** (-5)) / (s + 0.01826)
    tf14_19 = (-0.00372 * s - 4.494 * 10 ** (-5)) / (s + 0.01573)
    tf19_EER_list = [[tf11_19, tf12_19, tf13_19, tf14_19]]
    # Tei模型: Q=1900kW
    tf21_19 = (0.004492) / (s + 0.004494)
    tf22_19 = (-9.011 * 10 ** (-6)) / (s + 0.003625)
    tf23_19 = 0 / 1
    tf24_19 = 0 / 1
    tf19_Tei_list = [[tf21_19, tf22_19, tf23_19, tf24_19]]
    # 模型列表
    tf19_list = [tf19_EER_list[0], tf19_Tei_list[0]]

    # EER模型: Q=2000kW
    tf11_20 = (-1.249 * s + 0.000197) / (s + 0.004706)
    tf12_20 = (-2.284 * 10 ** (-5)) / (s + 0.006272)
    tf13_20 = (-0.003017 * s - 5.61 * 10 ** (-5)) / (s + 0.01851)
    tf14_20 = (-0.003531 * s - 4.063 * 10 ** (-5)) / (s + 0.01578)
    tf20_EER_list = [[tf11_20, tf12_20, tf13_20, tf14_20]]
    # Tei模型: Q=2000kW
    tf21_20 = (0.004491) / (s + 0.004493)
    tf22_20 = (-9.531 * 10 ** (-6)) / (s + 0.003624)
    tf23_20 = 0 / 1
    tf24_20 = 0 / 1
    tf20_Tei_list = [[tf21_20, tf22_20, tf23_20, tf24_20]]
    # 模型列表
    tf20_list = [tf20_EER_list[0], tf20_Tei_list[0]]

    # EER模型: Q=2100kW
    tf11_21 = (-1.146 * s + 0.0002296) / (s + 0.004811)
    tf12_21 = (-2.583 * 10 ** (-5)) / (s + 0.007083)
    tf13_21 = (-0.003001 * s - 5.665 * 10 ** (-5)) / (s + 0.01878)
    tf14_21 = (-0.003294 * s - 3.535 * 10 ** (-5)) / (s + 0.01575)
    tf21_EER_list = [[tf11_21, tf12_21, tf13_21, tf14_21]]
    # Tei模型: Q=2100kW
    tf21_21 = (0.004492) / (s + 0.004493)
    tf22_21 = (-1.005 * 10 ** (-5)) / (s + 0.003624)
    tf23_21 = 0 / 1
    tf24_21 = 0 / 1
    tf21_Tei_list = [[tf21_21, tf22_21, tf23_21, tf24_21]]
    # 模型列表
    tf21_list = [tf21_EER_list[0], tf21_Tei_list[0]]

    # EER模型: Q=2200kW
    tf11_22 = (-1.038 * s + 0.0002687) / (s + 0.004951)
    tf12_22 = (-0.001743 * s - 1.395 * 10 ** (-5)) / (s + 0.003826)
    tf13_22 = (-0.00297 * s - 5.697 * 10 ** (-5)) / (s + 0.01908)
    tf14_22 = (-0.003016 * s - 2.932 * 10 ** (-5)) / (s + 0.01575)
    tf22_EER_list = [[tf11_22, tf12_22, tf13_22, tf14_22]]
    # Tei模型: Q=2200kW
    tf21_22 = (0.004492) / (s + 0.004493)
    tf22_22 = (-1.057 * 10 ** (-5)) / (s + 0.003624)
    tf23_22 = 0 / 1
    tf24_22 = 0 / 1
    tf22_Tei_list = [[tf21_22, tf22_22, tf23_22, tf24_22]]
    # 模型列表
    tf22_list = [tf22_EER_list[0], tf22_Tei_list[0]]

    # EER模型: Q=2300kW
    tf11_23 = (-0.9239 * s + 0.000317) / (s + 0.005142)
    tf12_23 = (-0.001944 * s - 1.485 * 10 ** (-5)) / (s + 0.004099)
    tf13_23 = (-0.002924 * s - 5.703 * 10 ** (-5)) / (s + 0.0194)
    tf14_23 = (-0.002697 * s - 2.259 * 10 ** (-5)) / (s + 0.01584)
    tf23_EER_list = [[tf11_23, tf12_23, tf13_23, tf14_23]]
    # Tei模型: Q=2300kW
    tf21_23 = (0.004492) / (s + 0.004493)
    tf22_23 = (-1.109 * 10 ** (-5)) / (s + 0.003624)
    tf23_23 = 0 / 1
    tf24_23 = 0 / 1
    tf23_Tei_list = [[tf21_23, tf22_23, tf23_23, tf24_23]]
    # 模型列表
    tf23_list = [tf23_EER_list[0], tf23_Tei_list[0]]

    # EER模型: Q=2400kW
    tf11_24 = (-0.8026 * s + 0.0003788) / (s + 0.005417)
    tf12_24 = (-0.002171 * s - 1.654 * 10 ** (-5)) / (s + 0.004612)
    tf13_24 = (-0.002862 * s - 5.686 * 10 ** (-5)) / (s + 0.01975)
    tf14_24 = (-0.002329 * s - 1.476 * 10 ** (-5)) / (s + 0.01584)
    tf24_EER_list = [[tf11_24, tf12_24, tf13_24, tf14_24]]
    # Tei模型: Q=2400kW
    tf21_24 = (0.004492) / (s + 0.004493)
    tf22_24 = (-1.161 * 10 ** (-5)) / (s + 0.003623)
    tf23_24 = 0 / 1
    tf24_24 = 0 / 1
    tf24_Tei_list = [[tf21_24, tf22_24, tf23_24, tf24_24]]
    # 模型列表
    tf24_list = [tf24_EER_list[0], tf24_Tei_list[0]]

    # EER模型: Q=2500kW
    tf11_25 = (-0.6739 * s + 0.0004626) / (s + 0.005839)
    tf12_25 = (-0.002424 * s - 2.059 * 10 ** (-5)) / (s + 0.005822)
    tf13_25 = (-0.002786 * s - 5.642 * 10 ** (-5)) / (s + 0.02013)
    tf14_25 = (-0.001909 * s - 6.022 * 10 ** (-6)) / (s + 0.01585)
    tf25_EER_list = [[tf11_25, tf12_25, tf13_25, tf14_25]]
    # Tei模型: Q=2500kW
    tf21_25 = (0.004492) / (s + 0.004493)
    tf22_25 = (-1.213 * 10 ** (-5)) / (s + 0.003624)
    tf23_25 = 0 / 1
    tf24_25 = 0 / 1
    tf25_Tei_list = [[tf21_25, tf22_25, tf23_25, tf24_25]]
    # 模型列表
    tf25_list = [tf25_EER_list[0], tf25_Tei_list[0]]

    # EER模型: Q=2600kW
    tf11_26 = (-0.5369 * s + 0.0005871) / (s + 0.006547)
    tf12_26 = (-0.00271 * s - 3.402 * 10 ** (-5)) / (s + 0.009789)
    tf13_26 = (-0.002695 * s - 5.571 * 10 ** (-5)) / (s + 0.02054)
    tf14_26 = (-0.001437 * s + 3.719 * 10 ** (-6)) / (s + 0.01587)
    tf26_EER_list = [[tf11_26, tf12_26, tf13_26, tf14_26]]
    # Tei模型: Q=2600kW
    tf21_26 = (0.004492) / (s + 0.004493)
    tf22_26 = (-1.265 * 10 ** (-5)) / (s + 0.003624)
    tf23_26 = 0 / 1
    tf24_26 = 0 / 1
    tf26_Tei_list = [[tf21_26, tf22_26, tf23_26, tf24_26]]
    # 模型列表
    tf26_list = [tf26_EER_list[0], tf26_Tei_list[0]]

    # EER模型: Q=2700kW
    tf11_27 = (-0.3897 * s + 0.0007994) / (s + 0.007876)
    tf12_27 = (-0.003481 * s - 2.426 * 10 ** (-6)) / (s + 0.0007144)
    tf13_27 = (-0.002589 * s - 5.471 * 10 ** (-5)) / (s + 0.02099)
    tf14_27 = (-0.0009115 * s + 1.451 * 10 ** (-5)) / (s + 0.01588)
    tf27_EER_list = [[tf11_27, tf12_27, tf13_27, tf14_27]]
    # Tei模型: Q=2700kW
    tf21_27 = (0.004492) / (s + 0.004493)
    tf22_27 = (-1.317 * 10 ** (-5)) / (s + 0.003624)
    tf23_27 = 0 / 1
    tf24_27 = 0 / 1
    tf27_Tei_list = [[tf21_27, tf22_27, tf23_27, tf24_27]]
    # 模型列表
    tf27_list = [tf27_EER_list[0], tf27_Tei_list[0]]

    # EER模型: Q=2800kW
    tf11_28 = (-0.2144 * s ** 2 + 0.0004128 * s + 4.149 * 10 ** (-6)) / (s ** 2 + 0.009657 * s + 3.629 * 10 ** (-5))
    tf12_28 = (-0.00379 * s - 4.975 * 10 ** (-6)) / (s + 0.001504)
    tf13_28 = (-0.002468 * s - 5.338 * 10 ** (-5)) / (s + 0.02147)
    tf14_28 = (2.292 * 10 ** (-5)) / (s + 0.01379)
    tf28_EER_list = [[tf11_28, tf12_28, tf13_28, tf14_28]]
    # Tei模型: Q=2800kW
    tf21_28 = (0.004492) / (s + 0.004493)
    tf22_28 = (-1.369 * 10 ** (-5)) / (s + 0.003623)
    tf23_28 = 0 / 1
    tf24_28 = 0 / 1
    tf28_Tei_list = [[tf21_28, tf22_28, tf23_28, tf24_28]]
    # 模型列表
    tf28_list = [tf28_EER_list[0], tf28_Tei_list[0]]

    # EER模型: Q=2900kW
    tf11_29 = ((0.002897 * s + 4.376 * 10 ** (-6)) / (s ** 2 + 0.01348 * s + 3.397 * 10 ** (-5))) * (1 / (60 * s + 1))
    tf12_29 = (-0.004234 * s - 6.098 * 10 ** (-6)) / (s + 0.001901)
    tf13_29 = (-0.002334 * s - 5.161 * 10 ** (-5)) / (s + 0.02193)
    tf14_29 = (4.372 * 10 ** (-5)) / (s + 0.01761)
    tf29_EER_list = [[tf11_29, tf12_29, tf13_29, tf14_29]]
    # Tei模型: Q=2900kW
    tf21_29 = (0.004492) / (s + 0.004493)
    tf22_29 = (-1.421 * 10 ** (-5)) / (s + 0.003623)
    tf23_29 = 0 / 1
    tf24_29 = 0 / 1
    tf29_Tei_list = [[tf21_29, tf22_29, tf23_29, tf24_29]]
    # 模型列表
    tf29_list = [tf29_EER_list[0], tf29_Tei_list[0]]

    # EER模型: Q=3000kW
    tf11_30 = (0.145 * s ** 2 + 0.002552 * s + 2.885 * 10 ** (-6)) / (s ** 2 + 0.007714 * s + 1.985 * 10 ** (-5))
    tf12_30 = (-0.004768 * s - 6.588 * 10 ** (-6)) / (s + 0.002126)
    tf13_30 = (-0.002188 * s - 4.96 * 10 ** (-5)) / (s + 0.02247)
    tf14_30 = (7.02 * 10 ** (-5)) / (s + 0.02077)
    tf30_EER_list = [[tf11_30, tf12_30, tf13_30, tf14_30]]

    # Tei模型: Q=3000kW
    tf21_30 = (0.004492) / (s + 0.004493)
    tf22_30 = (-1.474 * 10 ** (-5)) / (s + 0.003624)
    tf23_30 = 0 / 1
    tf24_30 = 0 / 1
    tf30_Tei_list = [[tf21_30, tf22_30, tf23_30, tf24_30]]
    # 模型列表
    tf30_list = [tf30_EER_list[0], tf30_Tei_list[0]]

    # EER模型: Q=3100kW
    tf11_31 = (0.3469 * s ** 2 + 0.003333 * s + 2.843 * 10 ** (-6)) / (s ** 2 + 0.007344 * s + 1.735 * 10 ** (-5))
    tf12_31 = (-0.005389 * s - 6.76 * 10 ** (-6)) / (s + 0.002268)
    tf13_31 = (-0.00203 * s - 4.74 * 10 ** (-5)) / (s + 0.02313)
    tf14_31 = (0.0001018) / (s + 0.02334)
    tf31_EER_list = [[tf11_31, tf12_31, tf13_31, tf14_31]]
    # Tei模型: Q=3100kW
    tf21_31 = (0.004492) / (s + 0.004493)
    tf22_31 = (-1.526 * 10 ** (-5)) / (s + 0.003624)
    tf23_31 = 0 / 1
    tf24_31 = 0 / 1
    tf31_Tei_list = [[tf21_31, tf22_31, tf23_31, tf24_31]]
    # 模型列表
    tf31_list = [tf31_EER_list[0], tf31_Tei_list[0]]

    # EER模型: Q=3300kW
    tf11_33 = (0.01938) / (s + 0.4787)
    tf12_33 = ((-0.0004275 * s ** 2 - 3.737 * 10 ** (-5) * s - 8.986 * 10 ** (-9)) /
               (s ** 2 + 0.04701 * s + 1.161 * 10 ** (-5)))
    tf13_33 = (-0.0007765 * s - 4.59 * 10 ** (-7)) / (s + 0.0006033)
    tf14_33 = ((0.001267 * s ** 3 + 5.122 * 10 ** (-5) * s ** 2 + 2.04 * 10 ** (-8) * s + 1.474 * 10 ** (-12)) /
               (s ** 3 + 0.0188 * s ** 2 + 8.741 * 10 ** (-6) * s + 9.347 * 10 ** (-10)))
    tf33_EER_list = [[tf11_33, tf12_33, tf13_33, tf14_33]]
    # Tei模型: Q=3300kW
    tf21_33 = (10.38) / (s + 9.79)
    tf22_33 = ((-5.455 * 10 ** (-9) * s ** 2 - 6.212 * 10 ** (-12) * s - 1.145 * 10 ** (-15)) /
               (s ** 3 + 0.001209 * s ** 2 + 2.844 * 10 ** (-7) * s + 8.81 * 10 ** (-12)))
    tf23_33 = 0 / 1
    tf24_33 = 0 / 1
    tf33_Tei_list = [[tf21_33, tf22_33, tf23_33, tf24_33]]
    # 模型列表
    tf33_list = [tf33_EER_list[0], tf33_Tei_list[0]]

    # EER模型: Q=3400kW
    tf11_34 = (0.002995) / (s + 0.07827)
    tf12_34 = (-0.0004417 * s - 3.898 * 10 ** (-5)) / (s + 0.04809)
    tf13_34 = (-0.0007991 * s - 5.159 * 10 ** (-7)) / (s + 0.0006553)
    tf14_34 = ((0.00125 * s ** 3 + 5.563 * 10 ** (-5) * s ** 2 + 2.996 * 10 ** (-8) * s + 1.83 * 10 ** (-12)) /
               (s ** 3 + 0.02131 * s ** 2 + 1.25 * 10 ** (-5) * s + 1.235 * 10 ** (-9)))
    tf34_EER_list = [[tf11_34, tf12_34, tf13_34, tf14_34]]
    # Tei模型: Q=3400kW
    tf21_34 = (10.36) / (s + 9.771)
    tf22_34 = ((-0.0009465 * s ** 3 - 7.647 * 10 ** (-5) * s ** 2 - 3.234 * 10 ** (-8) * s - 1.217 * 10 ** (-11)) /
               (s ** 3 + 0.08153 * s ** 2 + 1.763 * 10 ** (-5) * s + 1.339 * 10 ** (-8)))
    tf23_34 = 0 / 1
    tf24_34 = 0 / 1
    tf34_Tei_list = [[tf21_34, tf22_34, tf23_34, tf24_34]]
    # 模型列表
    tf34_list = [tf34_EER_list[0], tf34_Tei_list[0]]

    # 模型列表
    model_EER_list = [tf1_EER_list, tf2_EER_list, tf3_EER_list, tf4_EER_list, tf5_EER_list, tf6_EER_list, tf7_EER_list,
                      tf8_EER_list, tf9_EER_list, tf10_EER_list, tf11_EER_list, tf12_EER_list, tf13_EER_list,
                      tf14_EER_list, tf15_EER_list, tf16_EER_list, tf17_EER_list, tf18_EER_list, tf19_EER_list,
                      tf20_EER_list, tf21_EER_list, tf22_EER_list, tf23_EER_list, tf24_EER_list, tf25_EER_list,
                      tf26_EER_list, tf27_EER_list, tf28_EER_list, tf29_EER_list, tf30_EER_list, tf31_EER_list,
                      tf33_EER_list, tf34_EER_list]
    model_Tei_list = [tf1_Tei_list, tf2_Tei_list, tf3_Tei_list, tf4_Tei_list, tf5_Tei_list, tf6_Tei_list, tf7_Tei_list,
                      tf8_Tei_list, tf9_Tei_list, tf10_Tei_list, tf11_Tei_list, tf12_Tei_list, tf13_Tei_list,
                      tf14_Tei_list, tf15_Tei_list, tf16_Tei_list, tf17_Tei_list, tf18_Tei_list, tf19_Tei_list,
                      tf20_Tei_list, tf21_Tei_list, tf22_Tei_list, tf23_Tei_list, tf24_Tei_list, tf25_Tei_list,
                      tf26_Tei_list, tf27_Tei_list, tf28_Tei_list, tf29_Tei_list, tf30_Tei_list, tf31_Tei_list,
                      tf33_Tei_list, tf34_Tei_list]
    model_list = [tf1_list, tf2_list, tf3_list, tf4_list, tf5_list, tf6_list, tf7_list, tf8_list, tf9_list, tf10_list,
                  tf11_list, tf12_list, tf13_list, tf14_list, tf15_list, tf16_list, tf17_list, tf18_list, tf19_list,
                  tf20_list, tf21_list, tf22_list, tf23_list, tf24_list, tf25_list, tf26_list, tf27_list, tf28_list,
                  tf29_list, tf30_list, tf31_list, tf33_list, tf34_list]
    # 每个模型对应的制冷功率Q的列表
    Q_model_list = [100, 200, 300, 400, 500, 600, 700, 800, 900, 1000, 1100, 1200, 1300, 1400, 1500, 1600, 1700, 1800,
                    1900, 2000, 2100, 2200, 2300, 2400, 2500, 2600, 2700, 2800, 2900, 3000, 3100, 3300, 3400]
    # 返回结果
    return Q_model_list, model_list, model_EER_list, model_Tei_list