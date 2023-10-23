import pickle
import numpy as np
from fmpy import *
from algorithm_code import *
from model_fmu_output_name import chiller_output_name, cold_storage_output_name, simple_load_output_name
from model_fmu_input_type import chiller_input_type, cold_storage_input_type, simple_load_input_type, \
                                 environment_input_type
from model_fmu_dynamics import model_fmu_dynamics
from initialize_simple_system import initialize_simple_system
from run_initialize import run_initialize
from get_fmu_real_data import get_chiller_input_real_data, get_storage_input_real_data

def run_simple_system(Q_total_list, txt_path, file_fmu):
    """
    冷水机+蓄冷水罐+简单的用户负荷
    搜算优化算法+GPC控制算法
    Args:
        Q_total_list: [list]，冷负荷，列表，单位：kW
        txt_path: [string]，相对路径
        file_fmu: [string]，FMU模型文件

    Returns:

    """
    # cfg文件路径
    cfg_path_equipment = "./config/equipment_config.cfg"
    cfg_path_public = "./config/public_config.cfg"
    # 设备类型名称(air_conditioner,air_source_heat_pump等)，相对路径
    chiller_equipment_type_path = ["chiller", txt_path]
    storage_equipment_type_path = ["energy_storage_equipment", txt_path]
    # 重置所有内容
    run_initialize(txt_path)

    # 设备的pkl文件路径
    file_pkl_chiller = "./model_data/file_equipment/chiller.pkl"
    # file_pkl_stroage = "./model_data/file_equipment/storage.pkl"
    file_pkl_system = "./model_data/file_equipment/system.pkl"

    # 读取冷水机设备信息
    with open(file_pkl_chiller, "rb") as f_obj:
        chiller_dict = pickle.load(f_obj)
    H_chiller_chilled_pump = chiller_dict["H_chiller_chilled_pump"]
    H_chiller_cooling_pump = chiller_dict["H_chiller_cooling_pump"]
    # chiller_list = chiller_dict["chiller_list"]
    chiller_chilled_pump_list = chiller_dict["chiller_chilled_pump_list"]
    chiller_cooling_pump_list = chiller_dict["chiller_cooling_pump_list"]
    # chiller_cooling_tower_list = chiller_dict["chiller_cooling_tower_list"]
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
    # 将初始化的控制器参数数据保存下来的路径
    file_path_init = './model_data/GPC_data/simple_system'
    # MMGPC是否绘图
    mmgpc_plot_set = True
    # 是否将MMGPC各个内置模型的计算结果画图
    model_plot_set = False
    # MMGPC控制时长
    L = 24 * 3600
    Ts = 10 * 60

    # MMGPC内置系统动态模型
    ans_model = model_fmu_dynamics()
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

    file_Q_model_list = file_path_init + "/Q_model_list.txt"
    write_txt_data(file_Q_model_list, Q_model_list)

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
    stop_time = start_time + simulate_initialize + (simulate_time1 + 3 * L) * n_simulate + simulate_time2
    output_interval = 30
    time_out = 600
    tolerance = 0.0001
    # 各系统制冷功率最大值
    chiller_Q0_max = 14000
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
    fmu_output_name = chiller_output_name()[0] + cold_storage_output_name()[0] + simple_load_output_name()
    chiller_input_name = get_fmu_input_name(chiller_input_type()[0])
    cold_storage_input_name = get_fmu_input_name(cold_storage_input_type()[0])
    simple_load_input_name = get_fmu_input_name(simple_load_input_type())
    environment_input_name = get_fmu_input_name(environment_input_type()[0])
    fmu_input_name = chiller_input_name + cold_storage_input_name + simple_load_input_name + environment_input_name
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
    initialize_simple_system(file_fmu_time, file_fmu_state, start_time, stop_time, simulate_initialize,
                             output_interval, time_out, tolerance, txt_path)
    # 仿真计算
    for i in range(n_simulate):
        print("一共需要计算" + str(n_simulate) + "次，正在进行第" + str(i + 1) + "次计算；已完成" + str(i) + "次计算；已完成" +
              str(np.round(100 * i / n_simulate, 4)) + "%")
        # 读取Q_user
        Q_user = Q_total_list[i]

        # 第1步：冷水机优化+控制
        input_log_1 = "第1步：冷水机优化+控制..."
        print(input_log_1)
        write_txt_data(file_fmu_input_log, [input_log_1, "\n"], 1)
        write_txt_data(file_fmu_input_feedback_log, [input_log_1, "\n"], 1)
        chiller_Q_total = min(Q_user, chiller_Q0_max)
        algorithm_chiller_double(chiller_Q_total, H_chiller_chilled_pump, 0, H_chiller_cooling_pump, chiller1,
                                 chiller2, chiller_chilled_pump1, chiller_chilled_pump2, None, None,
                                 chiller_cooling_pump1, chiller_cooling_pump2, chiller_cooling_tower, None,
                                 n0_chiller1, n0_chiller2, n0_chiller_chilled_pump1, n0_chiller_chilled_pump2,
                                 0, 0, n0_chiller_cooling_pump1, n0_chiller_cooling_pump2, n0_chiller_cooling_tower,
                                 0, chiller_equipment_type_path, n_calculate_hour, n_chiller_user_value,
                                 cfg_path_equipment, cfg_path_public)

        # 第2步：持续仿真，使得系统稳定下来
        input_log_2 = "第2步：持续仿真，使得系统稳定下来..."
        print(input_log_2)
        write_txt_data(file_fmu_input_log, [input_log_2, "\n"], 1)
        write_txt_data(file_fmu_input_feedback_log, [input_log_2, "\n"], 1)
        input_type_list = simple_load_input_type()
        input_data_list = [Q_user * 1000]
        result = main_simulate_pause_single(input_data_list, input_type_list, simulate_time1, txt_path)

        # 第3步：获取FMU模型的实际数据并写入txt文件
        input_log_3 = "第3步：获取FMU模型的实际数据并写入txt文件..."
        print(input_log_3)
        print("\n")
        get_chiller_input_real_data(result, chiller_equipment_type_path, cfg_path_equipment)
        get_storage_input_real_data(result, storage_equipment_type_path, cfg_path_equipment)

        # 第4步：MMGPC对EER和Tei进行控制
        input_log_4 = "第4步：MMGPC对EER和Tei进行控制..."
        print(input_log_4)
        print("\n")
        write_txt_data(file_fmu_input_log, [input_log_4, "\n"], 1)
        write_txt_data(file_fmu_input_feedback_log, [input_log_4, "\n"], 1)
        Teo0 = result['chiller_Teo_set'][-1]
        Few0 = result['chiller_Few_total'][-1]
        Fcw0 = result['chiller_Fcw_total'][-1]
        Fca0 = result['chiller_Fca_total'][-1]
        u_0_list = [Teo0, Few0, Fcw0, Fca0]
        EER0 = result['chiller_EER'][-1]
        Tei0 = result['chiller_Tei'][-1]
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
        du_limit_list = [1, 0.1 * Few0, 0.1 * Fcw0, 50]
        u_limit_list = [[5, 15], [0.5 * Few0, 1.5 * Few0], [0.5 * Fcw0, 1.5 * Fcw0],
                        [n_open_chiller_cooling_tower * chiller_cooling_tower.fmin,
                         n_open_chiller_cooling_tower * chiller_cooling_tower.fmax]]
        # MMGPC
        algorithm_dynamics(Q_user, Np_list, Nc_list, model_list, s_list, V, mmgpc_mode, ms_mode, yrk_list, yr_0_list,
                           u_0_list, du_limit_list, u_limit_list, L, Ts, file_path_init, H_chiller_chilled_pump,
                           0, H_chiller_cooling_pump, chiller_chilled_pump_list, [], chiller_cooling_pump_list,
                           n_chiller_list, n_chiller_chilled_pump_list, [], n_chiller_cooling_pump_list,
                           n_chiller_cooling_tower_list, chiller_equipment_type_path, cfg_path_equipment,
                           cfg_path_public, mmgpc_plot_set, model_plot_set)

    # 第5步：终止FMU模型，最后仿真一次
    input_log_5 = "第5步：终止FMU模型，最后仿真一次..."
    print(input_log_5)
    # 修改FMU状态
    fmu_state_list = [0, 1, stop_time, output_interval, time_out, tolerance]
    write_txt_data(file_fmu_state, fmu_state_list)
    # 最后仿真一次
    main_simulate_pause_single([], [], simulate_time2, txt_path)


if __name__ == "__main__":
    txt_path = "../optimal_control_algorithm_for_cooling_season"
    file_fmu = "./model_data/file_fmu/chiller_and_storage_with_simple_load_Cvode.fmu"
    Q_total_list = [11000]
    run_simple_system(Q_total_list, txt_path, file_fmu)
