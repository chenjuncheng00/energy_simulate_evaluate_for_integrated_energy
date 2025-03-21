import time
import numpy as np
from algorithm_win import write_txt_data, clear_all_txt_data, single_model_gpc_tuning, multi_model_gpc_tuning
from model_fmu_dynamics import model_dynamics_complex_chiller, model_dynamics_chiller_ashp

def tuning_smgpc(path_result_smgpc, model_info, L, Ts, yr_list, yr_0_list, u_0_list, du_limit_list, u_limit_list,
                 y_gpc_list, fit_target):
    """

    Args:
        path_result_smgpc: [string]，储存最终结果文本的文件路径
        model_info: [list]，模型信息
        L: [int]，仿真时间，单位：秒
        Ts: [int]，采样周期，单位：秒
        yr_list: [list]，输出目标值，列表
        yr_0_list: [list]，输出目标初始值，列表
        u_0_list: [list]，控制量的初始值，列表
        du_limit_list: [list]，控制量变化率的限制范围，列表
        u_limit_list: [list]，控制量的限制范围，列表
        y_gpc_list: [list]，控制器输出目标的名称列表
        fit_target: [int]，设置优化目标：0：综合考虑每次求解的y和yr的误差以及du的情况；1：仅考虑y的终值和yr的误差

    Returns:

    """
    # 系统动态模型
    if "EER" in y_gpc_list and "Tei" in y_gpc_list:
        model_list = model_info[1]
    elif "EER" in y_gpc_list and "Tei" not in y_gpc_list:
        model_list = model_info[2]
    elif "EER" not in y_gpc_list and "Tei" in y_gpc_list:
        model_list = model_info[3]
    else:
        model_list = []
    Np_list = model_info[4]
    Nc_list = model_info[5]
    # 寻优y权重
    k1 = 1
    # 寻优du权重
    k2 = 1 - k1
    # 输入输出数量
    n_input = len(model_list[0][0])
    n_output = len(model_list[0])
    # 寻优参数的上下限
    r_min = 0.01
    r_max = 1000
    r_min_list = []
    r_max_list = []
    for i in range(n_input):
        r_min_list.append(r_min)
        r_max_list.append(r_max)
    q_min = 10
    q_max = 10000
    q_min_list = []
    q_max_list = []
    for i in range(n_output):
        q_min_list.append(q_min)
        q_max_list.append(q_max)
    # 开始参数整定
    for i in range(len(model_list)):
        tf_list = model_list[i]
        Np = Np_list[i]
        Nc = Nc_list[i]
        time_start = time.time()
        txt_tuning = single_model_gpc_tuning(L, Ts, Np, Nc, tf_list, yr_list, yr_0_list, u_0_list, du_limit_list,
                                             u_limit_list, k1, k2, r_min_list, r_max_list, q_min_list, q_max_list,
                                             i + 1, fit_target)
        txt_list = [txt_tuning]
        time_end = time.time()
        time_cost = np.round(time_end - time_start, 2)
        print("计算用时(秒)：" + str(time_cost))
        # 结果写入txt
        write_txt_data(path_result_smgpc, txt_list, write_model=1)


def tuning_mmgpc(path_result_mmgpc, model_info, file_path_init, L, Ts, yr_list, yr_0_list, u_0_list, du_limit_list,
                 u_limit_list, y_gpc_list, fit_target):
    """

    Args:
        path_result_mmgpc: [string]，储存最终结果文本的文件路径
        model_info: [list]，模型信息
        file_path_init: [string]，将初始化的控制器参数数据保存下来的路径
        L: [int]，仿真时间，单位：秒
        Ts: [int]，采样周期，单位：秒
        yr_list: [list]，输出目标值，列表
        yr_0_list: [list]，输出目标初始值，列表
        u_0_list: [list]，控制量的初始值，列表
        du_limit_list: [list]，控制量变化率的限制范围，列表
        u_limit_list: [list]，控制量的限制范围，列表
        y_gpc_list: [list]，控制器输出目标的名称列表
        fit_target: [int]，设置优化目标：0：综合考虑每次求解的y和yr的误差以及du的情况；1：仅考虑y的终值和yr的误差

    Returns:

    """
    # 系统动态模型
    if "EER" in y_gpc_list and "Tei" in y_gpc_list:
        model_list = model_info[1]
    elif "EER" in y_gpc_list and "Tei" not in y_gpc_list:
        model_list = model_info[2]
    elif "EER" not in y_gpc_list and "Tei" in y_gpc_list:
        model_list = model_info[3]
    else:
        model_list = []
    Np_list = model_info[4]
    Nc_list = model_info[5]
    if "EER" in y_gpc_list and "Tei" in y_gpc_list:
        r_list = model_info[6]
        q_list = model_info[7]
    elif "EER" in y_gpc_list and "Tei" not in y_gpc_list:
        r_list = model_info[8]
        q_list = model_info[9]
    elif "EER" not in y_gpc_list and "Tei" in y_gpc_list:
        r_list = model_info[10]
        q_list = model_info[11]
    else:
        r_list = []
        q_list = []
    # V: 一个非常小的正实数，保证所有子控制器将来可用
    V = 0.0001
    # 寻优y权重
    k1 = 0.9
    # 寻优du权重
    k2 = 1 - k1
    # 输入输出数量
    n_output = len(model_list[0])
    # 待寻优参数的上下限
    S_min = 1
    S_max = 100000
    S_min_list = []
    S_max_list = []
    for i in range(n_output):
        S_min_list.append(S_min)
        S_max_list.append(S_max)
    # 开始参数整定
    for i in range(len(model_list)):
        plant_list = model_list[i]
        time_start = time.time()
        txt_tuning = multi_model_gpc_tuning(L, Ts, Np_list, Nc_list, V, plant_list, model_list, r_list, q_list,
                                            yr_list, yr_0_list, u_0_list, du_limit_list, u_limit_list, k1, k2,
                                            S_min_list, S_max_list, fit_target, file_path_init, i + 1)[1]
        txt_list = [txt_tuning]
        time_end = time.time()
        time_cost = np.round(time_end - time_start, 2)
        print("计算用时(秒)：" + str(time_cost))
        # 结果写入txt
        write_txt_data(path_result_mmgpc, txt_list, write_model=1)


if __name__ == "__main__":
    # model_mode: 0:仅冷水机；1:冷水机+空气源热泵
    model_mode = 1
    # 系统模型
    if model_mode == 0:
        model_info = model_dynamics_complex_chiller()
    elif model_mode == 1:
        model_info = model_dynamics_chiller_ashp()
    else:
        model_info = None
    # 控制器目标
    y_gpc_list = ["EER", "Tei"]
    # 仿真时长和采样周期，单位：秒
    L = 24 * 3600
    Ts = 10 * 60
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
    Few0 = 1435
    Fcw0 = 1675
    Fca0 = 200
    u_0_list = [Teo0, Few0, Fcw0, Fca0]
    # 输出的目标值yr
    yr_EER_list = []
    yr_Tei_list = []
    for i in range(n + 1):
        if i <= 10:
            yr_EER_list.append(EER0)
            yr_Tei_list.append(Tei0)
        else:
            yr_EER_list.append(EER0 + 0.4)
            yr_Tei_list.append(Tei0 + 0.5)
    if "EER" in y_gpc_list and "Tei" in y_gpc_list:
        yr_list = [yr_EER_list, yr_Tei_list]
    elif "EER" in y_gpc_list and "Tei" not in y_gpc_list:
        yr_list = [yr_EER_list]
    elif "EER" not in y_gpc_list and "Tei" in y_gpc_list:
        yr_list = [yr_Tei_list]
    else:
        yr_list = []
    # 控制量限制
    du_limit_list = [1, 300, 300, 100]
    u_limit_list = [[6, 15], [350, 3500], [450, 4200], [30, 300]]
    # 设置优化目标
    fit_target = 2
    # 储存结果的文件路径
    path_result_root = "./model_file/file_identify/result_system_dynamics"
    path_result_smgpc = path_result_root + "/result_tuning_smgpc.txt"
    path_result_mmgpc = path_result_root + "/result_tuning_mmgpc.txt"
    # 情况txt内容
    clear_all_txt_data(path_result_root)
    # 将初始化的控制器参数数据保存下来的路径
    if model_mode == 0:
        file_path_init = "./model_file/file_GPC/complex_chiller"
    elif model_mode == 1:
        file_path_init = "./model_file/file_GPC/chiller_ashp"
    else:
        file_path_init = ""
    # smgpc整定
    tuning_smgpc(path_result_smgpc, model_info, L, Ts, yr_list, yr_0_list, u_0_list, du_limit_list, u_limit_list,
                 y_gpc_list, fit_target)
    # mmgpc整定
    tuning_mmgpc(path_result_mmgpc, model_info, file_path_init, L, Ts, yr_list, yr_0_list, u_0_list, du_limit_list,
                 u_limit_list, y_gpc_list, fit_target)