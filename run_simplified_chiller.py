import copy
import numpy as np
import pickle
import matplotlib.pyplot as plt
from fmpy import *
from GPC_universal import *
from algorithm_code import *
from air_conditioner_dynamic import *
from run_tuning_dynamics_model import tuning_mmgpc, tuning_smgpc
from model_simplified_chiller import (model_input_type, model_dynamics_simplified_chiller,
                                      plant_dynamics_simplified_chiller)

def run_GPC_simplified_chiller():
    """

    Returns:

    """
    # 仿真类型：smgpc、mmgpc
    simulate_mode = "mmgpc"
    # 控制器目标
    y_gpc_list = ["EER", "Tei"]
    # MMGPC的计算模式：bayes、ms、itae
    mmgpc_mode = "bayes"
    # 多模型隶属度函数计算模式，0：梯形隶属度函数；1：三角形隶属度函数
    ms_mode = 0

    # MMGPC内置模型编号
    model_index = 3
    # 用于测试的被控对象模型编号
    plant_index = 20

    # 仿真时长和采样周期，单位：秒
    L = 5 * 3600
    Ts = 1 * 60
    # 仿真次数
    n = int(L / Ts)

    # V: 一个非常小的正实数，保证所有子控制器将来可用
    V = 0.0001
    # 多模型权值系数
    s_EER = 1
    s_Tei = 5000
    # MMGPC设置
    save_data_init = True
    plot_set = True
    model_plot_set = False

    # 输出目标值yr的初始值
    # EER, Tei
    EER0 = 4.5
    Tei0 = 12
    if "EER" in y_gpc_list and "Tei" in y_gpc_list:
        yr_0_list = [EER0, Tei0]
    elif "EER" in y_gpc_list and "Tei" not in y_gpc_list:
        yr_0_list = [EER0]
    elif "EER" not in y_gpc_list and "Tei" in y_gpc_list:
        yr_0_list = [Tei0]
    else:
        yr_0_list = []
    # 控制指令u初始值
    Teo0 = 8
    Few0 = 50
    Fcw0 = 50
    Fca0 = 50
    u_0_list = [Teo0, Few0, Fcw0, Fca0]
    # 输出的目标值yr
    yr_EER_list = []
    yr_Tei_list = []
    for i in range(n + 1):
        if i <= int(n / 5):
            yr_EER_list.append(EER0)
            yr_Tei_list.append(Tei0)
        else:
            yr_EER_list.append(EER0 + 0.1)
            yr_Tei_list.append(Tei0 + 0.2)
    if "EER" in y_gpc_list and "Tei" in y_gpc_list:
        yr_list = [yr_EER_list, yr_Tei_list]
    elif "EER" in y_gpc_list and "Tei" not in y_gpc_list:
        yr_list = [yr_EER_list]
    elif "EER" not in y_gpc_list and "Tei" in y_gpc_list:
        yr_list = [yr_Tei_list]
    else:
        yr_list = []
    # 控制量限制
    du_limit_list = [1, 10, 10, 10]
    u_limit_list = [[5, 15], [30, 50], [30, 50], [15, 50]]

    # MMGPC内置系统动态模型
    ans_model = model_dynamics_simplified_chiller()
    Q_model_list = ans_model[0]
    if "EER" in y_gpc_list and "Tei" in y_gpc_list:
        model_list = ans_model[1]
    elif "EER" in y_gpc_list and "Tei" not in y_gpc_list:
        model_list = ans_model[2]
    elif "EER" not in y_gpc_list and "Tei" in y_gpc_list:
        model_list = ans_model[3]
    else:
        model_list = []
    Np_list = ans_model[4]
    Nc_list = ans_model[5]
    r_list = ans_model[6]
    if "EER" in y_gpc_list and "Tei" in y_gpc_list:
        q_list = ans_model[7]
    elif "EER" in y_gpc_list and "Tei" not in y_gpc_list:
        q_list = ans_model[8]
    elif "EER" not in y_gpc_list and "Tei" in y_gpc_list:
        q_list = ans_model[9]
    else:
        q_list = []

    # 用于测试的plant_model
    ans_plant = plant_dynamics_simplified_chiller()
    Q_plant_list = ans_plant[0]
    if "EER" in y_gpc_list and "Tei" in y_gpc_list:
        plant_list = ans_plant[1]
    elif "EER" in y_gpc_list and "Tei" not in y_gpc_list:
        plant_list = ans_plant[2]
    elif "EER" not in y_gpc_list and "Tei" in y_gpc_list:
        plant_list = ans_plant[3]
    else:
        plant_list = []

    # mmgpc仿真参数设置
    # 将初始化的控制器参数数据保存下来的路径
    file_path_init = "./model_data/GPC_data/simplified_chiller"
    # 多模型权值系数的递推计算收敛系数
    if "EER" in y_gpc_list and "Tei" in y_gpc_list:
        s_list = [s_EER, s_Tei]
    elif "EER" in y_gpc_list and "Tei" not in y_gpc_list:
        s_list = [s_EER]
    elif "EER" not in y_gpc_list and "Tei" in y_gpc_list:
        s_list = [s_Tei]
    else:
        s_list = []
    # 计算隶属度函数
    if mmgpc_mode == "ms" and simulate_mode == "mmgpc":
        ms_list = calculate_membership(Q_plant_list[plant_index], Q_model_list, ms_mode)
    else:
        ms_list = []

    # 控制器仿真
    # smgpc
    if simulate_mode == "smgpc":
        smgpc(L, Ts, Np_list[model_index], Nc_list[model_index], model_list[model_index], r_list[model_index],
              q_list[model_index], yr_list, yr_0_list, u_0_list, du_limit_list, u_limit_list, True)
    elif simulate_mode == "mmgpc":
        mmgpc(L, Ts, Np_list, Nc_list, s_list, V, plant_list[plant_index], model_list, r_list, q_list, yr_list,
              yr_0_list, u_0_list, du_limit_list, u_limit_list, file_path_init, save_data_init, ms_list, mmgpc_mode,
              plot_set, model_plot_set)


def run_simplified_chiller(Q_total_list, Q_index, txt_path, file_fmu, run_mode):
    """
    简化的冷水机模型，用于测试系统动态特性和GPC算法
    Args:
        Q_total_list: [list]，冷负荷，列表，单位：kW
        Q_index: [int]，用于仿真的负荷编号
        txt_path: [string]，相对路径
        file_fmu: [string]，FMU模型文件
        run_mode: [string]，运行模式：simulate、identify

    Returns:

    """
    # 模型输入
    fmu_input_type = model_input_type()
    # 模型输出
    fmu_output_name = ["Q_total", "P_total", "Teo", "Tei", "Tco", "Tci", "Few", "Fcw"]
    fmu_input_name = get_fmu_input_name(fmu_input_type)
    fmu_input_output_name = fmu_input_name + fmu_output_name

    # # FMU模型仿真时间：仿真开始的时间(start_time)
    # file_fmu_time = txt_path + "/process_data/fmu_time.txt"
    # # FMU模型状态：依次为：fmu_initialize, fmu_terminate, stop_time, output_interval, time_out
    # file_fmu_state = txt_path + "/process_data/fmu_state.txt"
    # FMU模型输出名称
    file_fmu_input_output_name = txt_path + "/process_data/fmu_input_output_name.pkl"
    with open(file_fmu_input_output_name, "wb") as f:
        pickle.dump(fmu_input_output_name, f)
    # 仿真结果
    file_fmu_result_all = "./model_data/simulate_log/fmu_result_all.log"
    file_fmu_result_last = "./model_data/simulate_log/fmu_result_last.log"
    txt_str = "start_time" + "\t" + "pause_time"
    for i in range(len(fmu_input_output_name)):
        txt_str += "\t" + fmu_input_output_name[i]
    write_log_data(file_fmu_result_all, [txt_str], "data")
    write_log_data(file_fmu_result_last, [txt_str], "data")

    # 系统动态特性辨识
    if run_mode == "identify":
        identify_dynamics_simplified_chiller(Q_total_list, txt_path, file_fmu)
    elif run_mode == "simulate":
        simulate_dynamics_control(Q_total_list[Q_index], txt_path, file_fmu)


def simulate_dynamics_control(Q_total, txt_path, file_fmu):
    """

    Args:
        Q_total:
        txt_path:
        file_fmu:

    Returns:

    """
    # 控制器目标
    y_gpc_list = ["EER", "Tei"]
    # MMGPC的计算模式，bayes、ms、itae
    mmgpc_mode = "ms"
    # 多模型隶属度函数计算模式，0：梯形隶属度函数；1：三角形隶属度函数
    ms_mode = 0
    # 是否将MMGPC各个内置模型的计算结果画图
    model_plot_set = False

    # FMU仿真参数
    start_time = 0
    time_out = 600
    tolerance = 0.00001
    # 采样时间
    Ts = 1 * 60
    # 初始化FMU仿真时间
    simulate_time0 = 4 * 3600
    simulate_time1 = 4 * 3600
    # GPC仿真时间
    L = 4 * 3600
    # 仿真终止时间
    stop_time = simulate_time0 + simulate_time1 + L

    # V: 一个非常小的正实数，保证所有子控制器将来可用
    V = 0.0001
    # 多模型权值系数的递推计算收敛系数
    s_EER = 1
    s_Tei = 5000
    # 控制量限制
    du_limit_list = [1, 10, 10, 10]
    u_limit_list = [[5, 15], [30, 50], [30, 50], [15, 50]]

    # 将初始化的控制器参数数据保存下来的路径
    file_path_init = "./model_data/GPC_data/simplified_chiller"
    # FMU模型状态：依次为：fmu_initialize, fmu_terminate, stop_time, output_interval, time_out
    file_fmu_state = txt_path + "/process_data/fmu_state.txt"
    # FMU模型仿真时间：仿真开始的时间(start_time)
    file_fmu_time = txt_path + "/process_data/fmu_time.txt"
    # 模型初始化和实例化
    fmu_unzipdir = extract(file_fmu)
    fmu_description = read_model_description(fmu_unzipdir)
    fmu_instance = instantiate_fmu(unzipdir=fmu_unzipdir, model_description=fmu_description)
    # 获取内存地址
    file_fmu_address = txt_path + "/process_data/fmu_address.txt"
    unzipdir_address = id(fmu_unzipdir)
    description_address = id(fmu_description)
    instance_address = id(fmu_instance)
    fmu_address_list = [unzipdir_address, description_address, instance_address]
    write_txt_data(file_fmu_address, fmu_address_list)

    # 模型初始化
    input_data_initialize = [start_time, 27.1, 0, True, 8, 50, 50, 50]
    initialize_simplified_chiller(file_fmu_time, file_fmu_state, input_data_initialize, start_time, stop_time,
                                   simulate_time0, Ts, time_out, tolerance, txt_path)
    # 计算U0和y0
    input_data_list = [Q_total * 1000]
    input_type_list = [("Q_set", np.float_)]
    result = main_simulate_pause_single(input_data_list, input_type_list, simulate_time1, txt_path)
    Teo0 = list(result["chiller_Teo_set"])[-1]
    Few0 = list(result["chiller_f_chilled_pump1"])[-1]
    Fcw0 = list(result["chiller_f_cooling_pump1"])[-1]
    Fca0 = list(result["chiller_f_cooling_tower1"])[-1]
    u_0_list = [Teo0, Few0, Fcw0, Fca0]
    Tei0 = list(result["Tei"])[-1]
    Q0 = list(result["Q_total"])[-1]
    P0 = list(result["P_total"])[-1]
    EER0 = Q0 / P0
    if "EER" in y_gpc_list and "Tei" in y_gpc_list:
        yr_0_list = [EER0, Tei0]
        yrk_list = [EER0 + 0.1, Tei0 + 0.2]
    elif "EER" in y_gpc_list and "Tei" not in y_gpc_list:
        yr_0_list = [EER0]
        yrk_list = [EER0 + 0.3]
    elif "EER" not in y_gpc_list and "Tei" in y_gpc_list:
        yr_0_list = [Tei0]
        yrk_list = [Tei0 + 0.5]
    else:
        yr_0_list = []
        yrk_list = []
    yr0_correction_list = copy.deepcopy(yrk_list)

    ans_model = model_dynamics_simplified_chiller()
    # MMGPC内置模型的制冷功率列表
    Q_model_list = ans_model[0]
    if "EER" in y_gpc_list and "Tei" in y_gpc_list:
        model_list = ans_model[1]
    elif "EER" in y_gpc_list and "Tei" not in y_gpc_list:
        model_list = ans_model[2]
    elif "EER" not in y_gpc_list and "Tei" in y_gpc_list:
        model_list = ans_model[3]
    else:
        model_list = []
    Np_list = ans_model[4]
    Nc_list = ans_model[5]

    # 多模型权值系数的递推计算收敛系数
    if "EER" in y_gpc_list and "Tei" in y_gpc_list:
        s_list = [s_EER, s_Tei]
    elif "EER" in y_gpc_list and "Tei" not in y_gpc_list:
        s_list = [s_EER]
    elif "EER" not in y_gpc_list and "Tei" in y_gpc_list:
        s_list = [s_Tei]
    else:
        s_list = []

    # 求模型的数量
    n_model = len(model_list)
    # 确定模型的输入输出数量
    n_output = len(model_list[0])
    n_input = len(model_list[0][0])

    # 反馈校正
    kc_list = [0.4, 0.2]  # 比例增益系数
    n_smooth_list = [40, 10]  # 数据滑动平均连续采样的数据个数
    init_correction = feedback_correction_initialize(n_output, yr0_correction_list)
    e_correction_list = init_correction[0]
    dyr_correction_list = init_correction[1]
    yr_correction_list = init_correction[2]

    # ms方法需要ms_list参数
    # 计算隶属度函数
    if mmgpc_mode == "ms":
        ms_list = calculate_membership(Q_total, Q_model_list, ms_mode)
    else:
        ms_list = []

    # 初始化各个模型的控制器参数，列表
    F1_list = []
    F2_list = []
    G_list = []
    R_list = []
    Q_list = []
    B_list = []
    C_list = []
    len_A_list = []
    len_B_list = []
    len_B_max_list = []
    duk_model_list = []
    yrk_model_Np_list = []
    # 逐个模型初始化GPC控制器，从已经保存在文件里的控制器参数文件读取数据
    for i in range(n_model):
        file_name_init = file_path_init + "/model_" + str(i + 1) + ".npz"
        GPC_data = np.load(file_name_init, allow_pickle=True)
        # 获取GPC初始化的结果
        F1_list.append(GPC_data["F1"])
        F2_list.append(GPC_data["F2"])
        G_list.append(GPC_data["G"])
        R_list.append(GPC_data["R"])
        Q_list.append(GPC_data["Q"])
        B_list.append(GPC_data["B_list"])
        C_list.append(GPC_data["C_list"])
        len_A_list.append(GPC_data["len_A_list"])
        len_B_list.append(GPC_data["len_B_list"])
        len_B_max_list.append(GPC_data["len_B_max_list"])
        duk_model_list.append(GPC_data["duk_list"])
        yrk_model_Np_list.append(GPC_data["yrk_Np_list"])

    # 实际被控对象，控制指令的实际值u的列表
    u_list = []
    for i in range(n_input):
        tmp = []
        u_list.append(tmp)
    # 实际被控对象，控制指令的实际值的变化量Δu列表
    du_list = []
    for i in range(n_input):
        tmp = []
        du_list.append(tmp)
    # 实际被控对象，输出值y的实际值列表
    y_list = []
    for i in range(n_output):
        tmp = []
        y_list.append(tmp)
    # 被控对象目标值列表
    yr_list = []
    for i in range(n_output):
        tmp = []
        yr_list.append(tmp)

    # 各个内置模型，输出值y的实际值列表
    y_model_list = []
    for i in range(n_model):
        tmp_model = []
        y_model_list.append(tmp_model)
        for j in range(n_output):
            tmp_output = []
            y_model_list[i].append(tmp_output)
    # 各个内置模型，控制指令的实际值u的列表
    u_model_list = []
    for i in range(n_model):
        tmp_model = []
        u_model_list.append(tmp_model)
        for j in range(n_input):
            tmp_input = []
            u_model_list[i].append(tmp_input)
    # 各个内置模型，控制指令的实际值的变化量Δu列表
    du_model_list = []
    for i in range(n_model):
        tmp_model = []
        du_model_list.append(tmp_model)
        for j in range(n_input):
            tmp_input = []
            du_model_list[i].append(tmp_input)

    # 控制器参数初始值
    uk_list = u_0_list
    duk_list = [0, 0, 0, 0]
    yk_list = yr_0_list
    # 初始化：k时刻的输出值，用于滚动替换
    yk_model_list = []
    for i in range(n_model):
        yk_init_list = []
        for j in range(n_output):
            yk_tmp = np.ones((len_A_list[i][j][j], 1)) * yr_0_list[j]
            yk_init_list.append(yk_tmp)
        yk_model_list.append(yk_init_list)
    # 初始化：k时刻的控制指令u，用于滚动替换
    uk_model_list = []
    for i in range(n_model):
        uk_init_list = []
        for j in range(n_input):
            uk_tmp = np.ones((len_B_max_list[i][j], 1)) * u_0_list[j]
            uk_init_list.append(uk_tmp)
        uk_model_list.append(uk_init_list)

    # bayes方法需要ek_list，pk_list，wk_list参数
    # 各个内置模型的输出值与被控对象的实际输出的误差比值
    erk_list = []
    for i in range(n_model):
        tmp_model = []
        erk_list.append(tmp_model)
        for j in range(n_output):
            tmp_output = 0
            erk_list[i].append(tmp_output)
    # 各个内置模型与实际被控对象的匹配程度条件概率
    pk_list = []
    for i in range(n_model):
        tmp = 1 / n_model  # 初始值为1 / n_model
        pk_list.append(tmp)
    # 多模型策略下，各个内置模型控制指令实际值u/变化量Δu的权值
    wk_list = []
    for i in range(n_model):
        tmp_model = 0
        wk_list.append(tmp_model)

    # itae方法需要ek_list、Jk_list
    # 各个内置模型的输出值与被控对象的实际输出的误差绝对值
    ek_list = []
    for i in range(n_model):
        tmp_model = []
        ek_list.append(tmp_model)
        for j in range(n_output):
            tmp_output = 0
            ek_list[i].append(tmp_output)
    Jk_list = []
    for i in range(n_model):
        tmp_model = []
        Jk_list.append(tmp_model)
        for j in range(n_output):
            tmp_output = 0
            Jk_list[i].append(tmp_output)

    # 仿真时间列表
    time_list = []
    # 仿真次数
    n = int(L / Ts)
    for k in range(n):
        # 数据加入总列表
        for l in range(n_input):
            u_list[l].append(uk_list[l])
            du_list[l].append(duk_list[l])
        for l in range(n_output):
            y_list[l].append(yk_list[l])
            yr_list[l].append(yr0_correction_list[l])
            yr_correction_list[l].append(yrk_list[l])
        time_list.append(Ts * (k + 1))

        # mmgpc的yrk_list实际上是k+1时刻的EER和Tei目标值
        # 计算k时刻MMGPC的结果
        if mmgpc_mode == "bayes":
            mmgpc_bayes(F1_list, F2_list, G_list, R_list, Q_list, B_list, C_list, len_A_list, len_B_list, len_B_max_list,
                        y_model_list, du_model_list, u_model_list, yrk_model_Np_list, yk_model_list, duk_model_list,
                        uk_model_list, Np_list, Nc_list, s_list, V, model_list, yrk_list, yk_list, uk_list, duk_list,
                        du_limit_list, u_limit_list, pk_list, wk_list, True)
        elif mmgpc_mode == "ms":
            mmgpc_ms(F1_list, F2_list, G_list, R_list, Q_list, B_list, C_list, len_A_list, len_B_list, len_B_max_list,
                     y_model_list, du_model_list, u_model_list, yrk_model_Np_list, yk_model_list, duk_model_list,
                     uk_model_list, Np_list, Nc_list, model_list, yrk_list, yk_list, uk_list, duk_list, du_limit_list,
                     u_limit_list, ms_list)
        elif mmgpc_mode == "itae":
            # time_k = time_list[-1]
            time_k = k
            mmgpc_itae(F1_list, F2_list, G_list, R_list, Q_list, B_list, C_list, len_A_list, len_B_list, len_B_max_list,
                       y_model_list, du_model_list, u_model_list, yrk_model_Np_list, yk_model_list, duk_model_list,
                       uk_model_list, Np_list, Nc_list, model_list, yrk_list, yk_list, uk_list, duk_list, du_limit_list,
                       u_limit_list, Jk_list, time_k, True)

        # 将MMGPC的控制量输入到实际被控对象
        # mmgpc的uk_list实际上是k时刻的Teo、Few、Fcw、Fca计算实际值
        Teo = uk_list[0]
        Few = uk_list[1]
        Fcw = uk_list[2]
        Fca = uk_list[3]
        # 写入控制命令
        input_type_list = [("chiller_Teo_set", np.float_), ("chiller_f_chilled_pump1", np.float_),
                           ("chiller_f_cooling_pump1", np.float_), ("chiller_f_cooling_tower1", np.float_)]
        input_data_list = [Teo, Few, Fcw, Fca]

        result = main_simulate_pause_single(input_data_list, input_type_list, Ts, txt_path)
        # 获取输出的yk
        Tei = list(result["Tei"])[-1]
        Q = list(result["Q_total"])[-1]
        P = list(result["P_total"])[-1]
        EER = Q / P
        if "EER" in y_gpc_list and "Tei" in y_gpc_list:
            yk_list = [EER, Tei]
        elif "EER" in y_gpc_list and "Tei" not in y_gpc_list:
            yk_list = [EER]
        elif "EER" not in y_gpc_list and "Tei" in y_gpc_list:
            yk_list = [Tei]
        else:
            yk_list = []
        # GPC控制器反馈校正
        feedback_correction_kc(n_output, n_smooth_list, kc_list, yr0_correction_list, yr_correction_list, yrk_list,
                               yk_list, e_correction_list, dyr_correction_list)

    # GPC计算结果画图
    # plt画线颜色列表
    color_list = ["black", "brown", "green", "blue", "purple", "sienna", "yellowgreen", "slategray",
                  "hotpink", "yellow", "peachpuff", "palegreen", "goldenrod", "turquoise", "plum",
                  "gray", "fuchsia", "tomato", "goldenrod", "cyan", "slateblue", "orchid", "seagreen"]
    # 输出值y和输出目标值yr画图
    n = min(min(len(y_list[0]), len(yr_list[0])), len(time_list))
    for i in range(n_output):
        plt.figure(i + 1).set_size_inches(24, 8)
        plt.title("y_" + str(i + 1) + " and " + "yr_" + str(i + 1))
        plt.xlabel("t(s)")
        plt.ylabel("y_" + str(i + 1))
        plt.plot(time_list[:n], y_list[i][:n], color="skyblue", label="y", linewidth=3)
        plt.plot(time_list[:n], yr_list[i][:n], color="red", label="yr", linewidth=3)
        if model_plot_set == True:
            plt.plot(time_list[:n], yr_correction_list[i][:n], color="blueviolet", label="yr_correction",
                     linewidth=3, linestyle="dashed")
            for j in range(n_model):
                plt.plot(time_list[:n], y_model_list[j][i][:n], color=color_list[j],
                         label="y_model_" + str(j + 1), linewidth=3, linestyle="dotted")
        plt.legend()
    # 控制量u画图
    for i in range(n_input):
        plt.figure(i + 1 + n_output).set_size_inches(24, 8)
        plt.title("u_" + str(i + 1))
        plt.xlabel("t(s)")
        plt.ylabel("u_" + str(i + 1))
        plt.plot(time_list[:n], u_list[i][:n], color="skyblue", label="u", linewidth=3)
        if model_plot_set == True:
            for j in range(n_model):
                plt.plot(time_list[:n], u_model_list[j][i][:n], color=color_list[j],
                         label="u_model_" + str(j + 1), linewidth=3, linestyle="dotted")
        plt.legend()
    # 控制量变化率du画图
    for i in range(n_input):
        plt.figure(i + 1 + n_output + n_input).set_size_inches(24, 8)
        plt.title("du_" + str(i + 1))
        plt.xlabel("t(s)")
        plt.ylabel("du_" + str(i + 1))
        plt.plot(time_list[:n], du_list[i][:n], color="skyblue", label="du", linewidth=3)
        if model_plot_set == True:
            for j in range(n_model):
                plt.plot(time_list[:n], du_model_list[j][i][:n], color=color_list[j],
                         label="du_model_" + str(j + 1), linewidth=3, linestyle="dotted")
        plt.legend()
    # 显示画图结果
    plt.show()


def identify_dynamics_simplified_chiller(Q_total_list, txt_path, file_fmu):
    """

    Args:
        Q_total_list: [list]，模型辨识指定的制冷功率，列表，单位：kW
        txt_path: [string]，相对路径
        file_fmu: [string]，FMU模型文件

    Returns:

    """
    # FMU仿真参数
    start_time = 0
    stop_time = 24 * 3600
    time_out = 600
    tolerance = 0.00001
    # 采样时间
    Ts = 1 * 60

    # 模型初始化和实例化
    fmu_unzipdir = extract(file_fmu)
    fmu_description = read_model_description(fmu_unzipdir)
    # 获取内存地址
    file_fmu_address = txt_path + "/process_data/fmu_address.txt"
    unzipdir_address = id(fmu_unzipdir)
    description_address = id(fmu_description)
    # FMU模型状态：依次为：fmu_initialize, fmu_terminate, stop_time, output_interval, time_out
    file_fmu_state = txt_path + "/process_data/fmu_state.txt"
    # FMU模型仿真时间：仿真开始的时间(start_time)
    file_fmu_time = txt_path + "/process_data/fmu_time.txt"

    # 需要被辨识的对象列表：Fcw、Few、Fca、Teo、Tci等
    object_list = ["Teo", "Few", "Fcw", "Fca"]
    n_object_list = [1, 1, 1, 1]
    # 模型输出模式：EER/Tei
    Y_mode_list = ["EER", "Tei"]
    # 传递函数极点的最大数
    np_max = 3
    # 系统辨识得分的目标
    fitpercent_target_list = [95, 90, 85, 80]
    # matlab程序地址
    path_matlab = "/Users/chenjuncheng/Documents/Machine_Learning_Development/system_identification/air_conditioner_dynamic"

    # 用来拟合传递函数的数据储存路径：EER
    path_Few_EER_tfdata = "./model_data/file_identify/result_system_dynamics/tf_Few_EER.txt"  # 冷冻水流量
    path_Fcw_EER_tfdata = "./model_data/file_identify/result_system_dynamics/tf_Fcw_EER.txt"  # 冷却水流量
    path_Fca_EER_tfdata = "./model_data/file_identify/result_system_dynamics/tf_Fca_EER.txt"  # 冷却塔风量
    path_Teo_EER_tfdata = "./model_data/file_identify/result_system_dynamics/tf_Teo_EER.txt"  # 冷冻水出水温度
    # 用来拟合传递函数的数据储存路径：Tei
    path_Few_Tei_tfdata = "./model_data/file_identify/result_system_dynamics/tf_Few_Tei.txt"  # 冷冻水流量
    path_Fcw_Tei_tfdata = "./model_data/file_identify/result_system_dynamics/tf_Fcw_Tei.txt"  # 冷却水流量
    path_Fca_Tei_tfdata = "./model_data/file_identify/result_system_dynamics/tf_Fca_Tei.txt"  # 冷却塔风量
    path_Teo_Tei_tfdata = "./model_data/file_identify/result_system_dynamics/tf_Teo_Tei.txt"  # 冷冻水出水温度
    # 储存最终结果文本的文件路径
    path_result_EER = "./model_data/file_identify/result_system_dynamics/result_transfer_function_EER.txt"
    path_result_Tei = "./model_data/file_identify/result_system_dynamics/result_transfer_function_Tei.txt"
    # 传递函数数据的.txt文件文件所在的文件夹路径
    path_tf = "./model_data/file_identify/result_system_dynamics"
    # 清空txt文件
    root_path1 = "./model_data/file_identify/result_system_dynamics"
    clear_all_txt_data(root_path1)

    # 仿真各个阶段的时间，单位：秒
    simulate_time0 = 2 * 3600  # 初始化FMU
    simulate_time1 = 6 * 3600  # 系统稳定
    simulate_time2 = 6 * 3600  # 阶跃响应实验
    simulate_time3 = 2 * 3600  # 终止FMU
    # 最后要保存的
    n_data_save1 = 3 * 3600 / Ts
    n_data_save2 = simulate_time2 / Ts
    # plot的图编号
    index_figure = 1
    # 遍历所有制冷功率
    for i in range(len(Q_total_list)):
        # 获取制冷功率，单位：kW
        Q_input = Q_total_list[i]
        # 遍历所有需要辨识的项目类型
        for j in range(len(object_list)):
            tf_obj = object_list[j]
            # 第1步:初始化FMU模型
            print("制冷功率(kW)：" + str(round(Q_input, 2)) + "，辨识输入：" + tf_obj + "，正在初始化FMU模型!")
            # 初始化FMU模型
            fmu_instance = instantiate_fmu(unzipdir=fmu_unzipdir, model_description=fmu_description)
            instance_address = id(fmu_instance)
            fmu_address_list = [unzipdir_address, description_address, instance_address]
            write_txt_data(file_fmu_address, fmu_address_list)
            input_data_initialize = [start_time, 27.1, 0, True, 8, 50, 50, 50]
            initialize_simplified_chiller(file_fmu_time, file_fmu_state, input_data_initialize, start_time,
                                           stop_time, simulate_time0, Ts, time_out, tolerance, txt_path)

            # 第2步:给定冷负荷，并使得系统稳定
            input_data_list = [Q_input * 1000]
            input_type_list = [("Q_set", np.float_)]
            result = main_simulate_pause_single(input_data_list, input_type_list, simulate_time1, txt_path)
            Teo0 = list(result["chiller_Teo_set"])
            Few0 = list(result["Few"])
            Fcw0 = list(result["Fcw"])
            Fca0 = list(result["chiller_f_cooling_tower1"])
            Tei0 = list(result["Tei"])
            Q0 = list(result["Q_total"])
            P0 = list(result["P_total"])
            EER0 = []
            for k in range(len(Q0)):
                EER0.append(Q0[k] / P0[k])
            # 第3步:系统阶跃响应试验
            if tf_obj == "Teo":
                input_data_list = [9]
                input_type_list = [("chiller_Teo_set", np.float_)]
            elif tf_obj == "Few":
                input_data_list = [40]
                input_type_list = [("chiller_f_chilled_pump1", np.float_)]
            elif tf_obj == "Fcw":
                input_data_list = [40]
                input_type_list = [("chiller_f_cooling_pump1", np.float_)]
            elif tf_obj == "Fca":
                input_data_list = [40]
                input_type_list = [("chiller_f_cooling_tower1", np.float_)]
            else:
                input_data_list = []
                input_type_list = []
            result = main_simulate_pause_single(input_data_list, input_type_list, simulate_time2, txt_path)
            Teo1 = list(result["chiller_Teo_set"])
            Few1 = list(result["Few"])
            Fcw1 = list(result["Fcw"])
            Fca1 = list(result["chiller_f_cooling_tower1"])
            Tei1 = list(result["Tei"])
            Q1 = list(result["Q_total"])
            P1 = list(result["P_total"])
            EER1 = []
            for k in range(len(Q1)):
                EER1.append(Q1[k] / P1[k])
            # 第4步：确定传递函数辨识的输入X和输出Y
            Teo_list = Teo0 + Teo1
            Few_list = Few0 + Few1
            Fcw_list = Fcw0 + Fcw1
            Fca_list = Fca0 + Fca1
            EER_list = EER0 + EER1
            Tei_list = Tei0 + Tei1
            if tf_obj == "Teo":
                start_index0 = int(len(Teo0) - n_data_save1)
                X0_list = Teo0[start_index0:]
                X0 = sum(X0_list) / len(X0_list)
                start_index1 = int(len(Teo_list) - (n_data_save1 + n_data_save2))
                X_list = Teo_list[start_index1:]
                for k in range(len(X_list)):
                    X_list[k] -= X0
            elif tf_obj == "Few":
                start_index0 = int(len(Few0) - n_data_save1)
                X0_list = Few0[start_index0:]
                X0 = sum(X0_list) / len(X0_list)
                start_index1 = int(len(Few_list) - (n_data_save1 + n_data_save2))
                X_list = Few_list[start_index1:]
                for k in range(len(X_list)):
                    X_list[k] -= X0
            elif tf_obj == "Fcw":
                start_index0 = int(len(Fcw0) - n_data_save1)
                X0_list = Fcw0[start_index0:]
                X0 = sum(X0_list) / len(X0_list)
                start_index1 = int(len(Fcw_list) - (n_data_save1 + n_data_save2))
                X_list = Fcw_list[start_index1:]
                for k in range(len(X_list)):
                    X_list[k] -= X0
            elif tf_obj == "Fca":
                start_index0 = int(len(Fca0) - n_data_save1)
                X0_list = Fca0[start_index0:]
                X0 = sum(X0_list) / len(X0_list)
                start_index1 = int(len(Fca_list) - (n_data_save1 + n_data_save2))
                X_list = Fca_list[start_index1:]
                for k in range(len(X_list)):
                    X_list[k] -= X0
            else:
                X_list = None
                start_index1 = None
            # 绘图
            plt.figure(index_figure).set_size_inches(24, 8)
            plt.title("Q_input(kW):" + str(Q_input) + "; " + tf_obj)
            plt.plot(X_list, linewidth=3)
            index_figure += 1
            # 模型输出Y
            for k in range(len(Y_mode_list)):
                Y_mode = Y_mode_list[k]
                if Y_mode == "EER":
                    start_index0 = int(len(EER0) - n_data_save1)
                    Y0_list = EER0[start_index0:]
                    Y0 = sum(Y0_list) / len(Y0_list)
                    start_index1 = int(len(EER_list) - (n_data_save1 + n_data_save2))
                    Y_list = EER_list[start_index1:]
                    for l in range(len(Y_list)):
                        Y_list[l] -= Y0
                    # 绘图
                    plt.figure(index_figure).set_size_inches(24, 8)
                    plt.title("Q_input(kW):" + str(Q_input) + "; " + "EER: " + tf_obj)
                    plt.plot(Y_list, linewidth=3)
                    index_figure += 1
                elif Y_mode == "Tei":
                    start_index0 = int(len(Tei0) - n_data_save1)
                    Y0_list = Tei0[start_index0:]
                    Y0 = sum(Y0_list) / len(Y0_list)
                    start_index1 = int(len(Tei_list) - (n_data_save1 + n_data_save2))
                    Y_list = Tei_list[start_index1:]
                    # 如果是Fcw或者Fca，则Y_list全部改成0
                    for l in range(len(Y_list)):
                        if tf_obj == "Fcw" or tf_obj == "Fca":
                            Y_list[l] = 0
                        else:
                            Y_list[l] -= Y0
                    # 绘图
                    plt.figure(index_figure).set_size_inches(24, 8)
                    plt.title("Q_input(kW):" + str(Q_input) + "; " + "Tei: " + tf_obj)
                    plt.plot(Y_list, linewidth=3)
                    index_figure += 1
                else:
                    Y_list = None
                # 拼接数据，写入txt
                tf_data_txt_list = []
                for l in range(len(X_list)):
                    tmp = str(X_list[l]) + "\t" + str(Y_list[l])
                    tf_data_txt_list.append(tmp)
                if tf_obj == "Teo" and Y_mode == "EER":
                    write_txt_data(path_Teo_EER_tfdata, tf_data_txt_list)
                elif tf_obj == "Few" and Y_mode == "EER":
                    write_txt_data(path_Few_EER_tfdata, tf_data_txt_list)
                elif tf_obj == "Fcw" and Y_mode == "EER":
                    write_txt_data(path_Fcw_EER_tfdata, tf_data_txt_list)
                elif tf_obj == "Fca" and Y_mode == "EER":
                    write_txt_data(path_Fca_EER_tfdata, tf_data_txt_list)
                elif tf_obj == "Teo" and Y_mode == "Tei":
                    write_txt_data(path_Teo_Tei_tfdata, tf_data_txt_list)
                elif tf_obj == "Few" and Y_mode == "Tei":
                    write_txt_data(path_Few_Tei_tfdata, tf_data_txt_list)
                elif tf_obj == "Fcw" and Y_mode == "Tei":
                    write_txt_data(path_Fcw_Tei_tfdata, tf_data_txt_list)
                elif tf_obj == "Fca" and Y_mode == "Tei":
                    write_txt_data(path_Fca_Tei_tfdata, tf_data_txt_list)
            # 绘图
            plt.show()
            # 第5步：终止FMU模型
            print("制冷功率(kW)：" + str(round(Q_input, 2)) + "，辨识输入：" + tf_obj + "，正在终止FMU模型！")
            # 修改FMU状态
            fmu_state_list = [0, 1, stop_time, Ts, time_out, tolerance]
            write_txt_data(file_fmu_state, fmu_state_list)
            # 最后仿真一次
            main_simulate_pause_single([], [], simulate_time3, txt_path)

        # 第6步：辨识传递函数
        print("制冷功率(kW)：" + str(round(Q_input, 2)) + "，所有的传递函数辨识数据生成完成！")
        for j in range(len(Y_mode_list)):
            Y_mode = Y_mode_list[j]
            print("制冷功率(kW)：" + str(round(Q_input, 2)) + "，辨识输出：" + Y_mode + "，正在进行传递函数辨识!")
            info_txt = ("Q=" + str(round(Q_input, 2)) + "kW")
            # 传递函数系统辨识
            ans_tf = estimate_transfer_function(path_tf, path_matlab, Ts, object_list, n_object_list, np_max,
                                                fitpercent_target_list, i + 1, Y_mode, True)
            tf_txt = "# " + Y_mode + "模型: " + info_txt + "\n"
            tf_txt += ans_tf
            tf_txt_list = [tf_txt]
            # 将结果写入txt文件
            if Y_mode == "EER":
                path_result = path_result_EER
            elif Y_mode == "Tei":
                path_result = path_result_Tei
            else:
                path_result = None
            # 记录结果
            write_txt_data(path_result, tf_txt_list, write_model=1)
            # 结束循环
            print_txt = "传递函数辨识完成, 辨识的模型类型为：" + Y_mode + "；工况点序号为：" + \
                        str(i + 1) + ", " + info_txt + "\n"
            print(print_txt)


def initialize_simplified_chiller(file_fmu_time, file_fmu_state, input_data_initialize, start_time, stop_time,
                                   time_initialize, output_interval, time_out, tolerance, txt_path):
    """

    Args:
        file_fmu_time: [string]，储存FMU模型仿真时间(start_time)的文件路径
        file_fmu_state: [string]，储存FMU模型状态的文件路径
        input_data_initialize: [list]，FMU的初始化输入值
        start_time: [int]，仿真开始时间
        stop_time: [int]，仿真终止时间
        time_initialize: [int]，系统初始化时间，单位：秒
        output_interval: [int]，仿真输出时间间隔
        time_out: [int]，仿真超时时间
        tolerance: [float]，FMU模型求解相对误差
        txt_path: [string]，相对路径

    Returns:

    """

    # 模型默认输入
    fmu_input_type = model_input_type()
    # FMU模型初始化
    # FMU模型状态：依次为：fmu_initialize, fmu_terminate, stop_time, output_interval, time_out, tolerance
    fmu_state_list = [1, 0, stop_time, output_interval, time_out, tolerance]
    write_txt_data(file_fmu_state, fmu_state_list)
    write_txt_data(file_fmu_time, [start_time])
    # FMU仿真
    result = main_simulate_pause_single(input_data_initialize, fmu_input_type, time_initialize, txt_path,
                                        add_input=False)
    # 修改FMU状态
    fmu_state_list = [0, 0, stop_time, output_interval, time_out, tolerance]
    write_txt_data(file_fmu_state, fmu_state_list)
    write_txt_data(file_fmu_time, [start_time + time_initialize])
    # 返回结果
    return result


def tuning_dynamics_simplified_chiller(tuning_set):
    """

    Args:
        tuning_set: [string]，smgpc，mmgpc

    Returns:

    """
    # 传递函数
    model_info = model_dynamics_simplified_chiller()
    # 控制器目标
    y_gpc_list = ["EER", "Tei"]
    # 仿真时长和采样周期，单位：秒
    L = 8 * 3600
    Ts = 1 * 60
    # 仿真次数
    n = int(L / Ts)
    # 输出目标值yr的初始值
    # EER, Tei
    EER0 = 4.5
    Tei0 = 14
    if "EER" in y_gpc_list and "Tei" in y_gpc_list:
        yr_0_list = [EER0, Tei0]
    elif "EER" in y_gpc_list and "Tei" not in y_gpc_list:
        yr_0_list = [EER0]
    elif "EER" not in y_gpc_list and "Tei" in y_gpc_list:
        yr_0_list = [EER0]
    else:
        yr_0_list = []
    # 控制指令u初始值
    # Teo, Few, Fcw, Fca
    Teo0 = 8
    Few0 = 50
    Fcw0 = 50
    Fca0 = 50
    u_0_list = [Teo0, Few0, Fcw0, Fca0]
    # 输出的目标值yr
    yr_EER_list = []
    yr_Tei_list = []
    for i in range(n + 1):
        if i <= 10:
            yr_EER_list.append(EER0)
            yr_Tei_list.append(Tei0)
        else:
            yr_EER_list.append(EER0 + 0.1)
            yr_Tei_list.append(Tei0 + 0.2)
    if "EER" in y_gpc_list and "Tei" in y_gpc_list:
        yr_list = [yr_EER_list, yr_Tei_list]
    elif "EER" in y_gpc_list and "Tei" not in y_gpc_list:
        yr_list = [yr_EER_list]
    elif "EER" not in y_gpc_list and "Tei" in y_gpc_list:
        yr_list = [yr_Tei_list]
    else:
        yr_list = []
    # 控制量限制
    du_limit_list = [1, 10, 10, 10]
    u_limit_list = [[5, 15], [30, 50], [30, 50], [15, 50]]
    # 设置优化目标
    fit_target = 2
    # 储存结果的文件路径
    path_result_root = "./model_data/file_identify/result_system_dynamics"
    path_result_smgpc = path_result_root + "/result_tuning_smgpc.txt"
    path_result_mmgpc = path_result_root + "/result_tuning_mmgpc.txt"
    # 情况txt内容
    clear_all_txt_data(path_result_root)
    # 将初始化的控制器参数数据保存下来的路径
    file_path_init = "./model_data/GPC_data/simplified_chiller"
    # smgpc整定
    if tuning_set == "smgpc":
        tuning_smgpc(path_result_smgpc, model_info, L, Ts, yr_list, yr_0_list, u_0_list, du_limit_list, u_limit_list,
                     y_gpc_list, fit_target)
    # mmgpc整定
    if tuning_set == "mmgpc":
        tuning_mmgpc(path_result_mmgpc, model_info, file_path_init, L, Ts, yr_list, yr_0_list, u_0_list, du_limit_list,
                     u_limit_list, y_gpc_list, fit_target)


if __name__ == "__main__":
    # 运行 OR 系统辨识
    txt_path = "../optimal_control_algorithm_for_integrated_energy"
    file_fmu = "./model_data/file_fmu/simplified_chiller_model_Cvode.fmu"
    run_mode = "simulate"
    # Q_total_list = [100, 200, 300, 400, 500, 600, 700, 800, 900, 1000, 1100, 1200, 1300, 1400, 1500, 1600, 1700, 1800,
    #                 1900, 2000, 2100, 2200, 2300, 2400, 2500, 2600, 2700, 2800, 2900, 3000, 3100, 3200, 3300, 3400]
    # Q_total_list = [700, 1400, 1900, 2300, 2500, 2700, 2900]
    Q_total_list = [1700]
    Q_index = 0
    run_simplified_chiller(Q_total_list, Q_index, txt_path, file_fmu, run_mode)
    # # GPC控制器运行
    # run_GPC_simplified_chiller()
    # # 控制器整定
    # tuning_set = "smgpc"
    # tuning_dynamics_simplified_chiller(tuning_set)
    # # 模型间隙度计算
    # from gap_metric import *
    # path_matlab = "/Users/chenjuncheng/Documents/Machine_Learning_Development/system_identification/gap_metric"
    # model_list = model_dynamics_simplified_chiller()[1]
    # # model_list = plant_dynamics_simplified_chiller()[1]
    # calculate_gap_metric(path_matlab, model_list)