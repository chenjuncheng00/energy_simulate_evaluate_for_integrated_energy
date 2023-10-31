import pickle
import numpy as np
from fmpy import *
from algorithm_code import *
from model_fmu_output_name import main_model_output_name
from model_fmu_input_name import main_model_input_name
from model_fmu_input_type import load_input_type
from model_fmu_dynamics import model_dynamics_complex_chiller, model_dynamics_chiller_ashp
from initialize_integrated_system import initialize_integrated_system
from run_initialize import run_initialize
from get_fmu_real_data import (get_chiller_input_real_data, get_ashp_input_real_data, get_storage_input_real_data,
                               get_tower_chilled_input_real_data)

def run_dynamics_control(Q_total_list, txt_path, file_fmu, model_mode):
    """
    测试GPC控制算法
    综合系统：冷水机+空气源热泵+蓄冷水罐+冷却塔直接供冷+简单负荷
    Args:
        Q_total_list: [list]，冷负荷，列表，单位：kW
        txt_path: [string]，相对路径
        file_fmu: [string]，FMU模型文件
        model_mode: [int]，0:仅冷水机；1:冷水机+空气源热泵

    Returns:

    """
    # cfg文件路径
    cfg_path_equipment = "./config/equipment_config.cfg"
    cfg_path_public = "./config/public_config.cfg"
    # 设备类型名称(air_conditioner,air_source_heat_pump等)，相对路径
    chiller_equipment_type_path = ["chiller", txt_path]
    ashp_equipment_type_path = ["air_source_heat_pump", txt_path]
    storage_equipment_type_path = ["energy_storage_equipment", txt_path]
    tower_chilled_equipment_type_path = ["tower_chilled", txt_path]
    # 重置所有内容
    run_initialize(txt_path)

    # 设备的pkl文件路径
    file_pkl_chiller = "./model_data/file_equipment/chiller.pkl"
    file_pkl_ashp = "./model_data/file_equipment/ashp.pkl"
    # file_pkl_stroage = "./model_data/file_equipment/storage.pkl"
    file_pkl_system = "./model_data/file_equipment/system.pkl"

    # 读取冷水机设备信息
    with open(file_pkl_chiller, "rb") as f_obj:
        chiller_dict = pickle.load(f_obj)
    H_chiller_chilled_pump = chiller_dict["H_chiller_chilled_pump"]
    H_chiller_cooling_pump = chiller_dict["H_chiller_cooling_pump"]
    chiller_list = chiller_dict["chiller_list"]
    chiller_chilled_pump_list = chiller_dict["chiller_chilled_pump_list"]
    chiller_cooling_pump_list = chiller_dict["chiller_cooling_pump_list"]
    chiller_cooling_tower_list = chiller_dict["chiller_cooling_tower_list"]
    n_chiller_list = chiller_dict["n_chiller_list"]
    n_chiller_chilled_pump_list = chiller_dict["n_chiller_chilled_pump_list"]
    n_chiller_cooling_pump_list = chiller_dict["n_chiller_cooling_pump_list"]
    n_chiller_cooling_tower_list = chiller_dict["n_chiller_cooling_tower_list"]
    chiller1 = chiller_dict["chiller1"]
    chiller2 = chiller_dict["chiller2"]
    chiller_chilled_pump1 = chiller_dict["chiller_chilled_pump1"]
    chiller_chilled_pump2 = chiller_dict["chiller_chilled_pump2"]
    chiller_cooling_pump1 = chiller_dict["chiller_cooling_pump1"]
    chiller_cooling_pump2 = chiller_dict["chiller_cooling_pump2"]
    chiller_cooling_tower = chiller_dict["chiller_cooling_tower"]
    n0_chiller1 = chiller_dict["n_chiller1"]
    n0_chiller2 = chiller_dict["n_chiller2"]
    n0_chiller_chilled_pump1 = chiller_dict["n_chiller_chilled_pump1"]
    n0_chiller_chilled_pump2 = chiller_dict["n_chiller_chilled_pump2"]
    n0_chiller_cooling_pump1 = chiller_dict["n_chiller_cooling_pump1"]
    n0_chiller_cooling_pump2 = chiller_dict["n_chiller_cooling_pump2"]
    n0_chiller_cooling_tower = chiller_dict["n_chiller_cooling_tower"]
    n_chiller_user_value = chiller_dict["n_chiller_user_value"]
    # 读取空气源热泵设备信息
    with open(file_pkl_ashp, "rb") as f_obj:
        ashp_dict = pickle.load(f_obj)
    H_ashp_chilled_pump = ashp_dict["H_ashp_chilled_pump"]
    n0_air_source_heat_pump = ashp_dict["n_air_source_heat_pump"]
    n0_ashp_chilled_pump = ashp_dict["n_ashp_chilled_pump"]
    air_source_heat_pump = ashp_dict["air_source_heat_pump"]
    ashp_chilled_pump = ashp_dict["ashp_chilled_pump"]
    # # 读取蓄冷水罐设备信息
    # with open(file_pkl_stroage, "rb") as f_obj:
    #     storage_dict = pickle.load(f_obj)
    # energy_storage_equipment = storage_dict["energy_storage_equipment"]
    # chilled_pump_to_user = storage_dict["chilled_pump_to_user"]
    # chilled_pump_in_storage = storage_dict["chilled_pump_in_storage"]
    # n_chilled_value_in_storage = storage_dict["n_chilled_value_in_storage"]
    # n_chilled_value_to_user = storage_dict["n_chilled_value_to_user"]
    # 读取公共系统信息
    with open(file_pkl_system, "rb") as f_obj:
        system_dict = pickle.load(f_obj)
    n_calculate_hour = system_dict["n_calculate_hour"]
    # 日志文件
    file_fmu_input_log = "./model_data/simulate_result/fmu_input_log.txt"
    file_fmu_input_feedback_log = "./model_data/simulate_result/fmu_input_feedback_log.txt"

    # 用于MMGPC控制器的列表
    H_chilled_pump_list = [H_chiller_chilled_pump, H_ashp_chilled_pump]
    H_cooling_pump_list = [H_chiller_cooling_pump, 0]
    chilled_pump_list = [[chiller_chilled_pump1, chiller_chilled_pump2], [ashp_chilled_pump]]
    cooling_pump_list = [[chiller_cooling_pump1, chiller_cooling_pump2], []]
    n_air_conditioner_list = [[n0_chiller1, n0_chiller2], [n0_air_source_heat_pump]]
    n_chilled_pump_list = [[n0_chiller_chilled_pump1, n0_chiller_chilled_pump2], [n0_ashp_chilled_pump]]
    n_cooling_pump_list = [[n0_chiller_cooling_pump1, n0_chiller_cooling_pump2], []]
    n_cooling_tower_list = [[n0_chiller_cooling_tower], []]
    equipment_type_list = ["chiller", "air_source_heat_pump"]

    # 控制器目标
    y_gpc_list = ['EER', 'Tei']
    # MMGPC的计算模式，bayes、ms、itae
    mmgpc_mode = "ms"
    # 多模型隶属度函数计算模式，0：梯形隶属度函数；1：三角形隶属度函数
    ms_mode = 0
    # 多模型权值系数的递推计算收敛系数
    if 'EER' in y_gpc_list and 'Tei' in y_gpc_list:
        s_list = [1, 100]
    elif 'EER' in y_gpc_list and 'Tei' not in y_gpc_list:
        s_list = [1]
    elif 'EER' not in y_gpc_list and 'Tei' in y_gpc_list:
        s_list = [100]
    else:
        s_list = []
    # V: 一个非常小的正实数，保证所有子控制器将来可用
    V = 0.0001
    # MMGPC是否绘图
    mmgpc_plot_set = True
    # 是否将MMGPC各个内置模型的计算结果画图
    model_plot_set = False
    # MMGPC控制时长
    L = 24 * 3600
    Ts = 10 * 60

    # MMGPC内置系统动态模型
    if model_mode == 0:
        ans_model = model_dynamics_complex_chiller()
    elif model_mode == 1:
        ans_model = model_dynamics_chiller_ashp()
    else:
        ans_model = None
    Q_model_list = ans_model[0]
    if 'EER' in y_gpc_list and 'Tei' in y_gpc_list:
        model_list = ans_model[1]
    elif 'EER' in y_gpc_list and 'Tei' not in y_gpc_list:
        model_list = ans_model[2]
    elif 'EER' not in y_gpc_list and 'Tei' in y_gpc_list:
        model_list = ans_model[3]
    else:
        model_list = []
    Np_list = ans_model[4]
    Nc_list = ans_model[5]
    # 将初始化的控制器参数数据保存下来的路径
    if model_mode == 0:
        file_path_init = 'model_data/GPC_data/complex_chiller'
    elif model_mode == 1:
        file_path_init = 'model_data/GPC_data/chiller_ashp'
    else:
        file_path_init = ''
    file_Q_model_list = file_path_init + "/Q_model_list.txt"
    write_txt_data(file_Q_model_list, Q_model_list)

    # 0：user_load；1：simple_load
    load_mode = 1
    # 日志文件
    # file_fmu_input_log = "./model_data/simulate_result/fmu_input_log.txt"
    # file_fmu_input_feedback_log = "./model_data/simulate_result/fmu_input_feedback_log.txt"
    # 计算总次数
    n_simulate = len(Q_total_list)
    # 模型仿真时间
    simulate_initialize = 23 * 3600
    simulate_time1 = 8 * 3600
    simulate_time2 = 1 * 3600
    # FMU仿真参数
    start_time = 0
    stop_time = start_time + simulate_initialize + (simulate_time1 + 6 * L) * n_simulate + simulate_time2
    output_interval = 30
    time_out = 600
    tolerance = 0.0001
    # 各系统制冷功率最大值
    chiller_Q0_max = 14000
    ashp_Q0_max = 3600
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
    # FMU模型仿真时间：仿真开始的时间(start_time)
    file_fmu_time = txt_path + "/process_data/fmu_time.txt"
    # FMU模型状态：依次为：fmu_initialize, fmu_terminate, stop_time, output_interval, time_out
    file_fmu_state = txt_path + "/process_data/fmu_state.txt"
    # FMU模型输出名称
    file_fmu_input_output_name = txt_path + "/process_data/fmu_input_output_name.pkl"
    fmu_output_name = main_model_output_name(load_mode)
    fmu_input_name = main_model_input_name(load_mode)
    fmu_input_output_name = fmu_output_name + fmu_input_name
    with open(file_fmu_input_output_name, 'wb') as f:
        pickle.dump(fmu_input_output_name, f)
    # 冷负荷总需求功率
    file_Q_user = "./model_data/simulate_result/fmu_Q_user.txt"
    file_Q_user_list = "./model_data/fmu_Q_user_list.txt"
    # Q_time_all_list = read_txt_data(file_Q_user_list, column_index=0)
    Q_user_all_list = read_txt_data(file_Q_user_list, column_index=1)
    write_txt_data(file_Q_user, [Q_user_all_list[0]])
    # 仿真结果
    file_fmu_result_all = "./model_data/simulate_result/fmu_result_all.txt"
    file_fmu_result_last = "./model_data/simulate_result/fmu_result_last.txt"
    txt_str = "start_time" + "\t" + "pause_time"
    for i in range(len(fmu_input_output_name)):
        txt_str += "\t" + fmu_input_output_name[i]
    write_txt_data(file_fmu_result_all, [txt_str])
    write_txt_data(file_fmu_result_last, [txt_str])
    # FMU模型初始化
    initialize_integrated_system(file_fmu_time, file_fmu_state, start_time, stop_time, output_interval, time_out,
                                 tolerance, load_mode, txt_path)
    # 仿真计算
    for i in range(n_simulate):
        print("一共需要计算" + str(n_simulate) + "次，正在进行第" + str(i + 1) + "次计算；已完成" + str(i) + "次计算；已完成" +
              str(np.round(100 * i / n_simulate, 4)) + "%")
        # 读取Q_user
        Q_total = Q_total_list[i]
        Q_user = Q_total

        # 第1步：用向用户侧供冷功率优化一次冷水机计算，不进行控制，用于获取冷冻水泵扬程
        input_log_1 = "第1步：用向用户侧供冷功率优化一次冷水机计算，不进行控制，用于获取冷冻水泵扬程..."
        print(input_log_1)
        chiller_Q_user = min(Q_user, chiller_Q0_max)
        ans_chiller = optimization_system_universal(chiller_Q_user, H_chiller_chilled_pump, 0,
                                                    H_chiller_cooling_pump, chiller_list, chiller_chilled_pump_list,
                                                    [], chiller_cooling_pump_list, chiller_cooling_tower_list,
                                                    n_chiller_list, n_chiller_chilled_pump_list, [],
                                                    n_chiller_cooling_pump_list, n_chiller_cooling_tower_list,
                                                    chiller_equipment_type_path, cfg_path_public)
        chiller_user_chilled_pump_H = ans_chiller[4]

        # 第2步：用向用户侧供冷供冷，冷水机优化和控制
        input_log_2 = "第2步：用向用户侧供冷供冷，冷水机优化和控制..."
        print(input_log_2)
        write_txt_data(file_fmu_input_log, [input_log_2, "\n"], 1)
        write_txt_data(file_fmu_input_feedback_log, [input_log_2, "\n"], 1)
        algorithm_chiller_double(chiller_Q_user, H_chiller_chilled_pump, 0, H_chiller_cooling_pump, chiller1,
                                 chiller2, chiller_chilled_pump1, chiller_chilled_pump2, None, None,
                                 chiller_cooling_pump1, chiller_cooling_pump2, chiller_cooling_tower, None,
                                 n0_chiller1, n0_chiller2, n0_chiller_chilled_pump1, n0_chiller_chilled_pump2,
                                 0, 0, n0_chiller_cooling_pump1, n0_chiller_cooling_pump2, n0_chiller_cooling_tower,
                                 0, chiller_equipment_type_path, n_calculate_hour, n_chiller_user_value,
                                 cfg_path_equipment, cfg_path_public)

        # 第3步：用向用户侧供冷功率，空气源热泵优化和控制
        input_log_3 = "第3步：用向用户侧供冷功率，空气源热泵优化和控制..."
        print(input_log_3)
        write_txt_data(file_fmu_input_log, [input_log_3, "\n"], 1)
        write_txt_data(file_fmu_input_feedback_log, [input_log_3, "\n"], 1)
        ashp_Q_user = min(Q_total - chiller_Q_user, ashp_Q0_max)
        ashp_chilled_pump_H = 0.67 * chiller_user_chilled_pump_H
        algorithm_air_source_heat_pump(ashp_Q_user, ashp_chilled_pump_H, 0, air_source_heat_pump, ashp_chilled_pump,
                                       None, ashp_equipment_type_path, n_calculate_hour, 0, cfg_path_equipment,
                                       cfg_path_public)

        # 第4步：持续仿真，使得系统稳定下来
        input_log_4 = "第4步：持续仿真，使得系统稳定下来..."
        print(input_log_4)
        write_txt_data(file_fmu_input_log, [input_log_4, "\n"], 1)
        write_txt_data(file_fmu_input_feedback_log, [input_log_4, "\n"], 1)
        input_type_list = load_input_type(load_mode)
        input_data_list = [Q_user * 1000]
        result = main_simulate_pause_single(input_data_list, input_type_list, simulate_time1, txt_path)

        # 第5步：获取FMU模型的实际数据并写入txt文件
        input_log_5 = "第5步：获取FMU模型的实际数据并写入txt文件..."
        print(input_log_5)
        get_chiller_input_real_data(result, chiller_equipment_type_path, cfg_path_equipment)
        get_ashp_input_real_data(result, ashp_equipment_type_path, cfg_path_equipment)
        get_storage_input_real_data(result, storage_equipment_type_path, cfg_path_equipment)
        get_tower_chilled_input_real_data(result, tower_chilled_equipment_type_path, cfg_path_equipment)

        # 第6步：MMGPC对EER和Tei进行控制
        input_log_6 = "第6步：MMGPC对EER和Tei进行控制..."
        print(input_log_6)
        write_txt_data(file_fmu_input_log, [input_log_6, "\n"], 1)
        write_txt_data(file_fmu_input_feedback_log, [input_log_6, "\n"], 1)
        Teo0 = result['chiller_Teo_set'][-1]
        chiller_Few0 = result['chiller_Few_total'][-1]
        chiller_Fcw0 = result['chiller_Fcw_total'][-1]
        chiller_Fca0 = result['chiller_Fca_total'][-1]
        ashp_Few0 = result['ashp_Few_total'][-1]
        if model_mode == 1:
            u_0_list = [Teo0, chiller_Few0, chiller_Fcw0, chiller_Fca0, ashp_Few0]
        elif model_mode == 0:
            u_0_list = [Teo0, chiller_Few0, chiller_Fcw0, chiller_Fca0]
        else:
            u_0_list = []
        P0_tmp = (result["chiller_P_total_main_equipment"][-1] + result["chiller_P_total_chilled_pump"][-1] +
                  result["chiller_P_total_cooling_pump"][-1] + result["chiller_P_total_cooling_tower"][-1] +
                  result["ashp_P_total_main_equipment"][-1] + result["ashp_P_total_chilled_pump"][-1])
        Q0_tmp = result["chiller_Q_total"][-1] + result["ashp_Q_total"][-1]
        EER0 = Q0_tmp / P0_tmp
        Tei0 = result['user_Tei'][-1]
        if 'EER' in y_gpc_list and 'Tei' in y_gpc_list:
            yr_0_list = [EER0, Tei0]
            yrk_list = [EER0 + 0.3, Tei0 + 0.5]
        elif 'EER' in y_gpc_list and 'Tei' not in y_gpc_list:
            yr_0_list = [EER0]
            yrk_list = [EER0 + 0.3]
        elif 'EER' not in y_gpc_list and 'Tei' in y_gpc_list:
            yr_0_list = [Tei0]
            yrk_list = [Tei0 + 0.5]
        else:
            yr_0_list = []
            yrk_list = []
        # 获取冷却塔开启数量
        ans_chiller_open_status_txt_path = get_station_equipment_open_status_txt_path(chiller_equipment_type_path[0],
                                                                                      txt_path)
        file_chiller_cooling_tower_open_status = ans_chiller_open_status_txt_path[4]
        chiller_cooling_tower_open_status_list = read_txt_data(file_chiller_cooling_tower_open_status, return_status=1)
        n_open_chiller_cooling_tower = int(sum(chiller_cooling_tower_open_status_list))
        # 控制量限制
        if model_mode == 1:
            du_limit_list = [1, 0.1 * chiller_Few0, 0.1 * chiller_Fcw0, 50, 0.1 * ashp_Few0]
            u_limit_list = [[5, 15], [0.5 * chiller_Few0, 1.5 * chiller_Few0], [0.5 * chiller_Fcw0, 1.5 * chiller_Fcw0],
                            [n_open_chiller_cooling_tower * chiller_cooling_tower.fmin,
                             n_open_chiller_cooling_tower * chiller_cooling_tower.fmax],
                            [0.5 * ashp_Few0, 1.5 * ashp_Few0]]
        elif model_mode == 0:
            du_limit_list = [1, 0.1 * chiller_Few0, 0.1 * chiller_Fcw0, 50]
            u_limit_list = [[5, 15], [0.5 * chiller_Few0, 1.5 * chiller_Few0], [0.5 * chiller_Fcw0, 1.5 * chiller_Fcw0],
                            [n_open_chiller_cooling_tower * chiller_cooling_tower.fmin,
                             n_open_chiller_cooling_tower * chiller_cooling_tower.fmax]]
        else:
            du_limit_list = []
            u_limit_list = []

        # MMGPC
        algorithm_dynamics(Q_user, Np_list, Nc_list, model_list, s_list, V, mmgpc_mode, ms_mode, yrk_list, yr_0_list,
                           u_0_list, du_limit_list, u_limit_list, L, Ts, file_path_init, 0, H_chilled_pump_list,
                           H_cooling_pump_list, [], chilled_pump_list, cooling_pump_list, n_air_conditioner_list,
                           [], n_chilled_pump_list, n_cooling_pump_list, n_cooling_tower_list, equipment_type_list,
                           txt_path, cfg_path_equipment, cfg_path_public, mmgpc_plot_set, model_plot_set)

    # 第5步：终止FMU模型，最后仿真一次
    input_log_5 = "第5步：终止FMU模型，最后仿真一次..."
    print(input_log_5)
    # 修改FMU状态
    fmu_state_list = [0, 1, stop_time, output_interval, time_out, tolerance]
    write_txt_data(file_fmu_state, fmu_state_list)
    # 最后仿真一次
    main_simulate_pause_single([], [], simulate_time2, txt_path)


if __name__ == "__main__":
    model_mode = 1  # model_mode: 0:仅冷水机；1:冷水机+空气源热泵
    txt_path = "../optimal_control_algorithm_for_cooling_season"
    file_fmu = "./model_data/file_fmu/integrated_air_conditioning_simple_load_Cvode.fmu"
    Q_total_list = [16500]
    run_dynamics_control(Q_total_list, txt_path, file_fmu, model_mode)
