import pickle
from fmpy import *
from keras.api.models import load_model
from algorithm_win import (read_cfg_data, read_txt_data, write_txt_data, write_log_data, algorithm_common_station,
                           algorithm_station_dynamics, main_optimization_common_station, main_simulate_station_fmu,
                           get_station_open_status_txt_path, get_sensor_outside_real_value_txt_path,
                           initialize_user_Tei)
from model_fmu_output_name import main_model_output_name
from model_fmu_input_name import main_model_input_name
from model_fmu_input_type import load_input_type
from model_fmu_dynamics import model_dynamics_complex_chiller, model_dynamics_chiller_ashp
from initialize_integrated_system import initialize_integrated_system
from run_initialize import run_initialize
from get_fmu_real_data import main_get_fmu_real_data, get_Teo_set_real_data

def run_dynamics_control(Q_total, txt_path, file_fmu, load_mode):
    """
    测试GPC控制算法
    综合系统：冷水机+空气源热泵+蓄冷水罐+简单负荷
    Args:
        Q_total: [float]，冷负荷，列表，单位：kW
        txt_path: [string]，相对路径
        file_fmu: [string]，FMU模型文件
        load_mode: [int]，0：user_load；1：simple_load

    Returns:

    """
    # cfg文件路径
    cfg_path_equipment = txt_path + "/config/equipment_config.cfg"
    cfg_path_public = txt_path + "/config/public_config.cfg"
    # 设备类型名称(air_conditioner,air_source_heat_pump等)，相对路径
    chiller_system_type_path = ["chiller", txt_path]
    ashp_system_type_path = ["air_source_heat_pump", txt_path]
    # storage_equipment_type_path = ["energy_storage_equipment", txt_path]
    # 重置所有内容
    run_initialize(txt_path)
    # Q_total储存文件
    file_Q_value_chiller = txt_path + "/real_value/energy_station/chiller/Q_value/chilled_main_pipe.txt"
    file_Q_value_ashp = txt_path + "/real_value/energy_station/air_source_heat_pump/Q_value/chilled_main_pipe.txt"

    # 室外温湿度文件路径
    ans_environment_value_txt_path = get_sensor_outside_real_value_txt_path(txt_path)
    file_Tdo_value = ans_environment_value_txt_path[0]
    file_Hro_value = ans_environment_value_txt_path[1]
    # 总冷负荷
    file_Q_total = txt_path + "/process_data/Q_total.txt"
    # 室内温湿度控制目标值
    Tdi_set = read_cfg_data(cfg_path_public, "计算目标设定值", "Tdi_set", 0)
    Hri_set = read_cfg_data(cfg_path_public, "计算目标设定值", "Hri_set", 0)

    # 设备的pkl文件路径
    file_pkl_chiller = "./model_file/file_equipment/chiller.pkl"
    file_pkl_ashp = "./model_file/file_equipment/ashp.pkl"
    # file_pkl_stroage = "./model_file/file_equipment/storage.pkl"
    file_pkl_system = "./model_file/file_equipment/system.pkl"

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
    # chiller1 = chiller_dict["chiller1"]
    # chiller2 = chiller_dict["chiller2"]
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
    # n_chiller_user_valve = chiller_dict["n_chiller_user_valve"]
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
    # n_chilled_valve_in_storage = storage_dict["n_chilled_valve_in_storage"]
    # n_chilled_valve_to_user = storage_dict["n_chilled_valve_to_user"]
    # 读取公共系统信息
    with open(file_pkl_system, "rb") as f_obj:
        system_dict = pickle.load(f_obj)
    n_calculate_hour = system_dict["n_calculate_hour"]
    # 日志文件
    file_fmu_input_log = "./model_file/simulate_log/fmu_input_log.log"
    file_fmu_input_feedback_log = "./model_file/simulate_log/fmu_input_feedback_log.log"

    # 加载user_Tei_model
    path_model = "./model_file/model_user_nn.h5"
    user_model_nn = load_model(path_model)

    # 用于MMGPC控制器的列表
    H_chilled_pump_list = [H_chiller_chilled_pump, H_ashp_chilled_pump]
    H_cooling_pump_list = [H_chiller_cooling_pump, 0]
    chilled_pump_list = [[chiller_chilled_pump1, chiller_chilled_pump2], [ashp_chilled_pump]]
    cooling_pump_list = [[chiller_cooling_pump1, chiller_cooling_pump2], []]
    n_air_conditioner_list = [[n0_chiller1, n0_chiller2], [n0_air_source_heat_pump]]
    n_chilled_pump_list = [[n0_chiller_chilled_pump1, n0_chiller_chilled_pump2], [n0_ashp_chilled_pump]]
    n_cooling_pump_list = [[n0_chiller_cooling_pump1, n0_chiller_cooling_pump2], []]
    n_cooling_tower_list = [[n0_chiller_cooling_tower], []]

    # MMGPC是否绘图
    mmgpc_plot_set = True
    # 是否将MMGPC各个内置模型的计算结果画图
    model_plot_set = False
    # 模型仿真时间
    simulate_initialize = 23 * 3600
    if load_mode == 0:
        simulate_time1 = 2 * 3600
    elif load_mode == 1:
        simulate_time1 = 8 * 3600
    else:
        simulate_time1 = None
    simulate_time2 = 1 * 3600
    # FMU仿真参数
    if load_mode == 0:
        start_time = (31 + 28 + 31 + 30 + 31 + 15) * 24 * 3600
        stop_time = (31 + 28 + 31 + 30 + 31 + 30 + 31 + 31 + 30) * 24 * 3600 - 3600
    else:
        start_time = 0
        stop_time = start_time + simulate_initialize + simulate_time1 + 6 * 48 * 3600 + simulate_time2
    output_interval = 30
    time_out = 600
    tolerance = 0.0001

    # 各系统制冷功率最大值
    chiller_Q0_max = 14500
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
    with open(file_fmu_input_output_name, "wb") as f:
        pickle.dump(fmu_input_output_name, f)  # type: ignore

    # 冷负荷总需求功率
    file_name_Q_list = "./model_file/file_Q/file_name_Q_list.txt"
    if load_mode == 0:
        file_Q_user_list = "./model_file/file_Q/fmu_Q_MixedAir_list.txt"
    else:
        file_Q_user_list = "./model_file/file_Q/fmu_Q_simple_constant.txt"
        tmp_str1 = str(0) + "\t" + str(Q_total)
        tmp_str2 = str(365 * 24 * 3600) + "\t" + str(Q_total)
        write_txt_data(file_Q_user_list, [tmp_str1, tmp_str2])
    write_txt_data(file_name_Q_list, [file_Q_user_list])
    # Q_time_all_list = read_txt_data(file_Q_user_list, column_index=0)
    Q_user_all_list = read_txt_data(file_Q_user_list, column_index=1)
    file_Q_user = "./model_file/file_Q/fmu_Q_user.txt"
    write_txt_data(file_Q_user, [Q_user_all_list[0]])

    # 仿真结果
    file_fmu_result_all = "./model_file/simulate_log/fmu_result_all.log"
    file_fmu_result_last = "./model_file/simulate_log/fmu_result_last.log"
    txt_str = "start_time" + "\t" + "pause_time"
    for i in range(len(fmu_input_output_name)):
        txt_str += "\t" + fmu_input_output_name[i]
    write_log_data(file_fmu_result_all, [txt_str], "data")
    write_log_data(file_fmu_result_last, [txt_str], "data")
    # FMU模型初始化
    initialize_integrated_system(file_fmu_time, file_fmu_state, start_time, stop_time, output_interval, time_out,
                                 tolerance, load_mode, txt_path)
    # 仿真计算
    # 第1步：用向用户侧供冷功率优化一次冷水机计算，不进行控制，用于获取冷冻水泵扬程
    input_log_1 = "第1步：用向用户侧供冷功率优化一次冷水机计算，不进行控制，用于获取冷冻水泵扬程..."
    print(input_log_1)
    # 读取Q_user
    if load_mode == 0:
        Q_user = read_txt_data(file_Q_user)[0]
    elif load_mode == 1:
        Q_user = Q_total
    else:
        Q_user = 0
    chiller_Q_user = min(Q_user, chiller_Q0_max)
    write_txt_data(file_Q_value_chiller, [chiller_Q_user])
    ans_chiller = main_optimization_common_station(H_chiller_chilled_pump, 0, H_chiller_cooling_pump, chiller_list,
                                                     chiller_chilled_pump_list, [], chiller_cooling_pump_list,
                                                     chiller_cooling_tower_list, n_chiller_list, n_chiller_chilled_pump_list,
                                                     [], n_chiller_cooling_pump_list, n_chiller_cooling_tower_list,
                                                     chiller_system_type_path, cfg_path_public, cfg_path_equipment)
    chiller_user_chilled_pump_H = ans_chiller[3]

    # 第2步：用向用户侧供冷供冷，冷水机优化和控制
    input_log_2 = "第2步：用向用户侧供冷供冷，冷水机优化和控制..."
    print(input_log_2)
    write_log_data(file_fmu_input_log, [input_log_2], "info")
    write_log_data(file_fmu_input_feedback_log, [input_log_2], "info")
    write_txt_data(file_Q_value_chiller, [chiller_Q_user])
    algorithm_common_station(H_chiller_chilled_pump, 0, H_chiller_cooling_pump, chiller_list,
                               chiller_chilled_pump_list, [], chiller_cooling_pump_list,
                               chiller_cooling_tower_list, n_chiller_list, n_chiller_chilled_pump_list,
                               [], n_chiller_cooling_pump_list, n_chiller_cooling_tower_list,
                               chiller_system_type_path, n_calculate_hour, cfg_path_equipment, cfg_path_public)

    # 第3步：用向用户侧供冷功率，空气源热泵优化和控制
    input_log_3 = "第3步：用向用户侧供冷功率，空气源热泵优化和控制..."
    print(input_log_3)
    write_log_data(file_fmu_input_log, [input_log_3], "info")
    write_log_data(file_fmu_input_feedback_log, [input_log_3], "info")
    ashp_Q_user = min(Q_user - chiller_Q_user, ashp_Q0_max)
    ashp_chilled_pump_H = 0.67 * chiller_user_chilled_pump_H
    write_txt_data(file_Q_value_ashp, [ashp_Q_user])
    algorithm_common_station(ashp_chilled_pump_H, 0, 0, [air_source_heat_pump], [ashp_chilled_pump],
                               [], [], [], [n0_air_source_heat_pump], [n0_ashp_chilled_pump], [], [], [],
                               ashp_system_type_path, n_calculate_hour, cfg_path_equipment, cfg_path_public)

    # 第4步：持续仿真，使得系统稳定下来
    input_log_4 = "第4步：持续仿真，使得系统稳定下来..."
    print(input_log_4)
    write_log_data(file_fmu_input_log, [input_log_4], "info")
    write_log_data(file_fmu_input_feedback_log, [input_log_4], "info")
    input_type_list = load_input_type(load_mode)
    if load_mode == 0:
        input_data_list = [50, 50]
    elif load_mode == 1:
        input_data_list = [Q_user * 1000]
    else:
        input_data_list = []
    result = main_simulate_station_fmu(input_data_list, input_type_list, simulate_time1, txt_path)

    # 第5步：获取FMU模型的实际数据并写入txt文件
    input_log_5 = "第5步：获取FMU模型的实际数据并写入txt文件..."
    print(input_log_5)
    main_get_fmu_real_data(result, cfg_path_equipment, txt_path)
    get_Teo_set_real_data(txt_path, n_air_conditioner_list)

    # 第6步：MMGPC对EER和Tei进行控制
    input_log_6 = "第6步：MMGPC对EER和Tei进行控制..."
    print(input_log_6)
    write_log_data(file_fmu_input_log, [input_log_6], "info")
    write_log_data(file_fmu_input_feedback_log, [input_log_6], "info")
    Teo0 = result["chiller_Teo_set"][-1]
    chiller_Few0 = result["chiller_Few_total"][-1]
    chiller_Fcw0 = result["chiller_Fcw_total"][-1]
    chiller_Fca0 = result["chiller_Fca_total"][-1]
    ashp_Few0 = result["ashp_Few_total"][-1]
    # 确定动态控制的模型类型，model_mode: 0:仅冷水机；1:冷水机+空气源热泵
    if Q_user > chiller_Q0_max:
        model_mode = 1
    else:
        model_mode = 0
    # MMGPC内置系统动态模型
    if model_mode == 0:
        ans_model = model_dynamics_complex_chiller()
    elif model_mode == 1:
        ans_model = model_dynamics_chiller_ashp()
    else:
        ans_model = None
    Q_model_list = ans_model[0]
    model_list = ans_model[1]
    Np_list = ans_model[4]
    Nc_list = ans_model[5]
    # 将初始化的控制器参数数据保存下来的路径
    if model_mode == 0:
        file_path_init = "./model_file/file_GPC/complex_chiller"
    elif model_mode == 1:
        file_path_init = "./model_file/file_GPC/chiller_ashp"
    else:
        file_path_init = ""
    file_Q_model_list = file_path_init + "/Q_model_list.txt"
    write_txt_data(file_Q_model_list, Q_model_list)
    # 动态控制器初始值
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
    Tei0 = result["user_Tei"][-1]
    yr_0_list = [EER0, Tei0]
    yrk_list = [EER0 + 0.3, Tei0 + 0.5]
    # 获取冷却塔开启数量
    ans_chiller_open_status_txt_path = get_station_open_status_txt_path(chiller_system_type_path[0], txt_path)
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
        equipment_type_list = ["chiller", "air_source_heat_pump"]
    elif model_mode == 0:
        du_limit_list = [1, 0.1 * chiller_Few0, 0.1 * chiller_Fcw0, 50]
        u_limit_list = [[5, 15], [0.5 * chiller_Few0, 1.5 * chiller_Few0], [0.5 * chiller_Fcw0, 1.5 * chiller_Fcw0],
                        [n_open_chiller_cooling_tower * chiller_cooling_tower.fmin,
                         n_open_chiller_cooling_tower * chiller_cooling_tower.fmax]]
        equipment_type_list = ["chiller"]
    else:
        du_limit_list = []
        u_limit_list = []
        equipment_type_list = []

    # 初始化user_Tei_model
    # 更新系统总冷负荷
    Q_total = read_txt_data(file_Q_total)[0]
    # 室外环境温湿度
    Tdo = read_txt_data(file_Tdo_value)[0]
    Hro = read_txt_data(file_Hro_value)[0]
    user_input_data_list = [Teo0, chiller_Few0 + ashp_Few0, Tdi_set, Hri_set, Tdo, Hro, Q_total, Tei0]
    initialize_user_Tei(user_model_nn, user_input_data_list, cfg_path_public)

    # MMGPC
    results = algorithm_station_dynamics(user_model_nn, Np_list, Nc_list, model_list, yrk_list, yr_0_list, u_0_list,
                                         du_limit_list, u_limit_list, file_path_init, 0, H_chilled_pump_list,
                                         H_cooling_pump_list, [], chilled_pump_list, cooling_pump_list,
                                         n_air_conditioner_list, [], n_chilled_pump_list, n_cooling_pump_list,
                                         n_cooling_tower_list, equipment_type_list, txt_path, cfg_path_equipment,
                                         cfg_path_public, mmgpc_plot_set, model_plot_set)

    # 第7步：获取FMU模型的实际数据并写入txt文件
    input_log_7 = "第7步：动态控制，获取FMU模型的实际数据并写入txt文件..."
    for result in results:
        print(input_log_7)
        main_get_fmu_real_data(result, cfg_path_equipment, txt_path)
        get_Teo_set_real_data(txt_path, n_air_conditioner_list)

    # 第8步：终止FMU模型，最后仿真一次
    input_log_8 = "第8步：终止FMU模型，最后仿真一次..."
    print(input_log_8)
    # 修改FMU状态
    fmu_state_list = [0, 1, stop_time, output_interval, time_out, tolerance]
    write_txt_data(file_fmu_state, fmu_state_list)
    # 最后仿真一次
    main_simulate_station_fmu([], [], simulate_time2, txt_path)


if __name__ == "__main__":
    txt_path = "./algorithm_file"
    # simple_load使用的参数
    Q_total = 16000
    # 负荷模型类型选择：0：user_load；1：simple_load
    load_mode = 1
    # 确定FMU模型文件
    if load_mode == 0:
        file_fmu = "./model_file/file_fmu/integrated_air_conditioning_Sdirk34hw.fmu"
    else:
        file_fmu = "./model_file/file_fmu/integrated_air_conditioning_simple_load_Sdirk34hw.fmu"
    run_dynamics_control(Q_total, txt_path, file_fmu, load_mode)
