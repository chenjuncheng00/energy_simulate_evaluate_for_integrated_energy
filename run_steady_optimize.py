import pickle
import numpy as np
from fmpy import *
from algorithm_win import (read_cfg_data, read_txt_data, write_txt_data, write_log_data, main_simulate_pause_single,
                           algorithm_common_universal, algorithm_chilled_pump, algorithm_energy_storage_equipment,
                           algorithm_Teo_set_user, main_optimization_common_universal, main_optimization_energy_storage_equipment)
from model_fmu_output_name import main_model_output_name
from model_fmu_input_name import main_model_input_name
from model_fmu_input_type import load_input_type
from calculate_energy_storage_value import generate_Q_list, generate_time_name_list
from initialize_integrated_system import initialize_integrated_system
from run_initialize import run_initialize
from get_fmu_real_data import main_get_fmu_real_data

def run_run_steady_optimize(txt_path, file_fmu, load_mode):
    """
    测试稳态点优化搜索算法
    综合系统：冷水机+空气源热泵+蓄冷水罐+负荷(简单负荷 OR 复杂负荷)
    Args:
        txt_path: [string]，相对路径
        file_fmu: [string]，FMU模型文件
        load_mode: [int]，0：user_load；1：simple_load

    Returns:

    """
    # 设备类型名称(air_conditioner,air_source_heat_pump等)，相对路径
    chiller_system_type_path = ["chiller", txt_path]
    ashp_system_type_path = ["air_source_heat_pump", txt_path]
    storage_system_type_path = ["energy_storage_equipment", txt_path]
    # 重置所有内容
    run_initialize(txt_path)

    # Q_total储存文件
    file_Q_value_chiller = txt_path + "/real_value/energy_station/chiller/Q_value/chilled_main_pipe.txt"
    file_Q_value_ashp = txt_path + "/real_value/energy_station/air_source_heat_pump/Q_value/chilled_main_pipe.txt"

    # cfg文件路径
    cfg_path_equipment = txt_path + "/config/equipment_config.cfg"
    cfg_path_public = txt_path + "/config/public_config.cfg"
    # 设备的pkl文件路径
    file_pkl_chiller = "./model_file/file_equipment/chiller.pkl"
    file_pkl_ashp = "./model_file/file_equipment/ashp.pkl"
    file_pkl_stroage = "./model_file/file_equipment/storage.pkl"
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
    # chiller_chilled_pump1 = chiller_dict["chiller_chilled_pump1"]
    # chiller_chilled_pump2 = chiller_dict["chiller_chilled_pump2"]
    # chiller_cooling_pump1 = chiller_dict["chiller_cooling_pump1"]
    # chiller_cooling_pump2 = chiller_dict["chiller_cooling_pump2"]
    # chiller_cooling_tower = chiller_dict["chiller_cooling_tower"]
    # n0_chiller1 = chiller_dict["n_chiller1"]
    # n0_chiller2 = chiller_dict["n_chiller2"]
    # n0_chiller_chilled_pump1 = chiller_dict["n_chiller_chilled_pump1"]
    # n0_chiller_chilled_pump2 = chiller_dict["n_chiller_chilled_pump2"]
    # n0_chiller_cooling_pump1 = chiller_dict["n_chiller_cooling_pump1"]
    # n0_chiller_cooling_pump2 = chiller_dict["n_chiller_cooling_pump2"]
    # n0_chiller_cooling_tower = chiller_dict["n_chiller_cooling_tower"]
    # n_chiller_user_valve = chiller_dict["n_chiller_user_valve"]
    # 读取空气源热泵设备信息
    with open(file_pkl_ashp, "rb") as f_obj:
        ashp_dict = pickle.load(f_obj)
    # H_ashp_chilled_pump = ashp_dict["H_ashp_chilled_pump"]
    n0_air_source_heat_pump = ashp_dict["n_air_source_heat_pump"]
    n0_ashp_chilled_pump = ashp_dict["n_ashp_chilled_pump"]
    air_source_heat_pump = ashp_dict["air_source_heat_pump"]
    ashp_chilled_pump = ashp_dict["ashp_chilled_pump"]
    # 读取蓄冷水罐设备信息
    with open(file_pkl_stroage, "rb") as f_obj:
        storage_dict = pickle.load(f_obj)
    energy_storage_equipment = storage_dict["energy_storage_equipment"]
    chilled_pump_to_user = storage_dict["chilled_pump_to_user"]
    chilled_pump_in_storage = storage_dict["chilled_pump_in_storage"]
    n_storage_chilled_pump = storage_dict["n_storage_chilled_pump"]
    # 读取公共系统信息
    with open(file_pkl_system, "rb") as f_obj:
        system_dict = pickle.load(f_obj)
    n_calculate_hour = system_dict["n_calculate_hour"]

    # 日志文件
    file_fmu_input_log = "./model_file/simulate_log/fmu_input_log.log"
    file_fmu_input_feedback_log = "./model_file/simulate_log/fmu_input_feedback_log.log"
    # FMU仿真参数
    if load_mode == 0:
        start_time = (31 + 28 + 31 + 30 + 31 + 30) * 24 * 3600
        stop_time = (31 + 28 + 31 + 30 + 31 + 30 + 31 + 31 + 30) * 24 * 3600 - 3600
    else:
        start_time = 0
        stop_time = 141 * 24 * 3600 - 3600
    output_interval = 30
    time_out = 600
    tolerance = 0.01
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
    # FMU模型输出名称，包括所有的输入和输出名称
    file_fmu_input_output_name = txt_path + "/process_data/fmu_input_output_name.pkl"
    fmu_output_name = main_model_output_name(load_mode)
    fmu_input_name = main_model_input_name(load_mode)
    fmu_input_output_name = fmu_output_name + fmu_input_name
    with open(file_fmu_input_output_name, "wb") as f:
        pickle.dump(fmu_input_output_name, f)  # type: ignore
    # 各系统制冷功率最大值
    chiller_Q0_max = 14000
    ashp_Q0_max = 3600
    Q0_total_in = chiller_Q0_max
    Q0_total_out = chiller_Q0_max + ashp_Q0_max
    # 冷负荷总需求功率
    file_name_Q_list = "./model_file/file_Q/file_name_Q_list.txt"
    if load_mode == 0:
        file_Q_user_list = "./model_file/file_Q/fmu_Q_MixedAir_list.txt"
    else:
        file_Q_user_list = "./model_file/file_Q/fmu_Q_simple_list.txt"
    write_txt_data(file_name_Q_list, [file_Q_user_list])
    Q_time_all_list = read_txt_data(file_Q_user_list, column_index=0)
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
    init_time_total = initialize_integrated_system(file_fmu_time, file_fmu_state, start_time, stop_time,
                                                   output_interval, time_out, tolerance, load_mode, txt_path)
    # 逐时用电时间段列表，字符串，长度24
    time_name_list = ["谷", "谷", "谷", "谷", "谷", "谷", "谷", "谷", "平", "平", "峰", "峰", "峰", "平", "平", "峰",
                      "峰", "平", "平", "平", "峰", "峰", "峰", "平"]
    # 冷冻水额定温差
    Ted_set = read_cfg_data(cfg_path_public, "计算目标设定值", "Ted_set", 0)
    # 计算总次数
    n_simulate = int((stop_time - start_time - init_time_total) / (3600 / n_calculate_hour))

    for i in range(n_simulate):
        print("一共需要计算" + str(n_simulate) + "次，正在进行第" + str(i + 1) + "次计算；已完成" + str(i) + "次计算；已完成" +
              str(np.round(100 * i / n_simulate, 4)) + "%")
        # 读取Q_user
        Q_user = read_txt_data(file_Q_user)[0]

        # 第1步：仅进行蓄冷水罐优化计算，获取当前时刻的充放冷功率，不进行控制
        input_log_1 = "第1步：仅进行蓄冷水罐优化计算，获取当前时刻的充放冷功率，不进行控制..."
        print(input_log_1)
        Q_user_list = generate_Q_list(file_fmu_time, start_time, Q_time_all_list, Q_user_all_list, n_calculate_hour)
        ans_ese = main_optimization_energy_storage_equipment(storage_system_type_path, Q_user_list, time_name_list,
                                                             Q0_total_in, Q0_total_out, energy_storage_equipment, 0)
        Q_out_ese = ans_ese[0]
        Q_total = Q_user - Q_out_ese  # 计算Q_total
        print("蓄冷水罐冷负荷功率：" + str(Q_out_ese))

        # 第2步：进行冷水机+蓄冷水罐控制
        if Q_out_ese < 0:
            # 第2-1步：用蓄冷功率优化一次冷水机计算，不进行控制，用于获取阀门开启比例
            input_log_2_1 = "第2-1步：用蓄冷功率优化一次冷水机计算，不进行控制，用于获取阀门开启比例..."
            print(input_log_2_1)
            chiller_Q_storage = - Q_out_ese  # 冷水机蓄冷负荷
            write_txt_data(file_Q_value_chiller, [chiller_Q_storage])
            ans_chiller1 = main_optimization_common_universal(H_chiller_chilled_pump, 0, H_chiller_cooling_pump,
                                                              chiller_list, chiller_chilled_pump_list, [],
                                                              chiller_cooling_pump_list, chiller_cooling_tower_list,
                                                              n_chiller_list, n_chiller_chilled_pump_list, [],
                                                              n_chiller_cooling_pump_list, n_chiller_cooling_tower_list,
                                                              chiller_system_type_path, cfg_path_public, cfg_path_equipment)
            chiller_storage_chilled_valve_open = ans_chiller1[0]

            # 第2-2步：用向用户侧供冷功率优化一次冷水机计算，不进行控制，用于获取阀门开启比例和冷冻水泵扬程
            input_log_2_2 = "第2-2步：用向用户侧供冷功率优化一次冷水机计算，不进行控制，用于获取阀门开启比例和冷冻水泵扬程..."
            print(input_log_2_2)
            chiller_Q_user = min(Q_user, chiller_Q0_max)
            write_txt_data(file_Q_value_chiller, [chiller_Q_user])
            ans_chiller2 = main_optimization_common_universal(H_chiller_chilled_pump, 0, H_chiller_cooling_pump,
                                                              chiller_list, chiller_chilled_pump_list, [],
                                                              chiller_cooling_pump_list, chiller_cooling_tower_list,
                                                              n_chiller_list, n_chiller_chilled_pump_list, [],
                                                              n_chiller_cooling_pump_list, n_chiller_cooling_tower_list,
                                                              chiller_system_type_path, cfg_path_public, cfg_path_equipment)
            chiller_user_chilled_valve_open = ans_chiller2[0]
            chiller_user_chilled_pump_H = ans_chiller2[4]

            # 第2-3步：用向用户侧供冷供冷+蓄冷功率，冷水机优化和控制，但是不进行冷冻水泵控制
            input_log_2_3 = "第2-3步：用向用户侧供冷供冷+蓄冷功率，冷水机优化和控制，但是不进行冷冻水泵控制..."
            print(input_log_2_3)
            write_log_data(file_fmu_input_log, [input_log_2_3], "info")
            write_log_data(file_fmu_input_feedback_log, [input_log_2_3], "info")
            chiller_Q_total = min(Q_total, chiller_Q0_max)
            write_txt_data(file_Q_value_chiller, [chiller_Q_total])
            algorithm_common_universal(H_chiller_chilled_pump, 0, H_chiller_cooling_pump, chiller_list,
                                       chiller_chilled_pump_list, [], chiller_cooling_pump_list,
                                       chiller_cooling_tower_list, n_chiller_list, n_chiller_chilled_pump_list,
                                       [], n_chiller_cooling_pump_list, n_chiller_cooling_tower_list,
                                       chiller_system_type_path, n_calculate_hour, cfg_path_equipment,
                                       cfg_path_public, chilled_pump_control=False)
            # 第2-4步：用向用户侧供冷功率，冷水机优化和控制，仅进行冷冻水泵控制
            input_log_2_4 = "第2-4步：用向用户侧供冷功率，冷水机优化和控制，仅进行冷冻水泵控制..."
            print(input_log_2_4)
            write_log_data(file_fmu_input_log, [input_log_2_4], "info")
            write_log_data(file_fmu_input_feedback_log, [input_log_2_4], "info")
            chiller_Few_user = chiller_Q_user * 3.6 / 4.18 / Ted_set
            algorithm_chilled_pump([chiller_Few_user], [], H_chiller_chilled_pump, 0, chiller_user_chilled_valve_open,
                                   chiller_chilled_pump_list, [], n_chiller_chilled_pump_list, [],
                                   chiller_system_type_path, n_calculate_hour, cfg_path_equipment, cfg_path_public)

            # 第2-5步：蓄冷水罐和水泵优化+控制，蓄冷工况
            input_log_2_5 = "第2-5步：蓄冷水罐和水泵优化+控制，蓄冷工况..."
            print(input_log_2_5)
            write_log_data(file_fmu_input_log, [input_log_2_5], "info")
            write_log_data(file_fmu_input_feedback_log, [input_log_2_5], "info")
            H_chilled_pump_to_user = 0.65 * chiller_user_chilled_pump_H
            H_chilled_pump_in_storage = 0.65 * chiller_user_chilled_pump_H
            algorithm_energy_storage_equipment(Q_user_list, time_name_list, Q0_total_in, Q0_total_out,
                                               energy_storage_equipment, [chilled_pump_to_user],
                                               [chilled_pump_in_storage], [], chiller_storage_chilled_valve_open,
                                               H_chilled_pump_to_user, H_chilled_pump_in_storage, 0,
                                               [n_storage_chilled_pump], [], storage_system_type_path,
                                               n_calculate_hour, cfg_path_equipment, cfg_path_public)
            # 第2-6步：用向用户侧供冷功率，空气源热泵优化和控制
            input_log_2_6 = "第2-6步：用向用户侧供冷功率，空气源热泵优化和控制..."
            print(input_log_2_6)
            write_log_data(file_fmu_input_log, [input_log_2_6], "info")
            write_log_data(file_fmu_input_feedback_log, [input_log_2_6], "info")
            ashp_Q_user = min(Q_user - chiller_Q_user, ashp_Q0_max)
            H_ashp_chilled_pump = 0.65 * chiller_user_chilled_pump_H
            write_txt_data(file_Q_value_ashp, [ashp_Q_user])
            algorithm_common_universal(H_ashp_chilled_pump, 0, 0, [air_source_heat_pump], [ashp_chilled_pump],
                                       [], [], [], [n0_air_source_heat_pump], [n0_ashp_chilled_pump], [], [], [],
                                       ashp_system_type_path, n_calculate_hour, cfg_path_equipment, cfg_path_public)

        elif Q_out_ese > 0:
            # 第2-1步：用向用户侧供冷功率优化一次冷水机计算，不进行控制，用于获取冷冻水泵扬程
            input_log_2_1 = "第2-1步：用向用户侧供冷功率优化一次冷水机计算，不进行控制，用于获取冷冻水泵扬程..."
            print(input_log_2_1)
            chiller_Q_user = min(Q_user, chiller_Q0_max)
            write_txt_data(file_Q_value_chiller, [chiller_Q_user])
            ans_chiller2 = main_optimization_common_universal(H_chiller_chilled_pump, 0, H_chiller_cooling_pump,
                                                              chiller_list, chiller_chilled_pump_list, [],
                                                              chiller_cooling_pump_list, chiller_cooling_tower_list,
                                                              n_chiller_list, n_chiller_chilled_pump_list, [],
                                                              n_chiller_cooling_pump_list, n_chiller_cooling_tower_list,
                                                              chiller_system_type_path, cfg_path_public, cfg_path_equipment)
            chiller_user_chilled_pump_H = ans_chiller2[4]

            # 第2-2步：蓄冷水罐和水泵优化+控制，供冷工况
            input_log_2_2 = "第2-2步：蓄冷水罐和水泵优化+控制，供冷工况..."
            print(input_log_2_2)
            write_log_data(file_fmu_input_log, [input_log_2_2], "info")
            write_log_data(file_fmu_input_feedback_log, [input_log_2_2], "info")
            H_chilled_pump_to_user = 0.75 * chiller_user_chilled_pump_H
            H_chilled_pump_in_storage = 0.65 * chiller_user_chilled_pump_H
            algorithm_energy_storage_equipment(Q_user_list, time_name_list, Q0_total_in, Q0_total_out,
                                               energy_storage_equipment, [chilled_pump_to_user],
                                               [chilled_pump_in_storage], [], 1, H_chilled_pump_to_user,
                                               H_chilled_pump_in_storage, 0, [n_storage_chilled_pump], [],
                                               storage_system_type_path, n_calculate_hour, cfg_path_equipment,
                                               cfg_path_public)

            # 第2-3步：用向用户侧供冷供冷，冷水机优化和控制
            input_log_2_3 = "第2-3步：用向用户侧供冷供冷，冷水机优化和控制..."
            print(input_log_2_3)
            write_log_data(file_fmu_input_log, [input_log_2_3], "info")
            write_log_data(file_fmu_input_feedback_log, [input_log_2_3], "info")
            write_txt_data(file_Q_value_chiller, [chiller_Q_user])
            algorithm_common_universal(H_chiller_chilled_pump, 0, H_chiller_cooling_pump, chiller_list,
                                       chiller_chilled_pump_list, [], chiller_cooling_pump_list,
                                       chiller_cooling_tower_list, n_chiller_list, n_chiller_chilled_pump_list,
                                       [], n_chiller_cooling_pump_list, n_chiller_cooling_tower_list,
                                       chiller_system_type_path, n_calculate_hour, cfg_path_equipment, cfg_path_public)

            # 第2-4步：用向用户侧供冷功率，空气源热泵优化和控制
            input_log_2_4 = "第2-4步：用向用户侧供冷功率，空气源热泵优化和控制..."
            print(input_log_2_4)
            write_log_data(file_fmu_input_log, [input_log_2_4], "info")
            write_log_data(file_fmu_input_feedback_log, [input_log_2_4], "info")
            ashp_Q_user = min(Q_total - chiller_Q_user, ashp_Q0_max)
            H_ashp_chilled_pump = 0.65 * chiller_user_chilled_pump_H
            write_txt_data(file_Q_value_ashp, [ashp_Q_user])
            algorithm_common_universal(H_ashp_chilled_pump, 0, 0, [air_source_heat_pump], [ashp_chilled_pump],
                                       [], [], [], [n0_air_source_heat_pump], [n0_ashp_chilled_pump], [], [], [],
                                       ashp_system_type_path, n_calculate_hour, cfg_path_equipment, cfg_path_public)
        else:
            # 第2-1步：Q_out_ese=0，蓄冷水罐控制，目的是关闭蓄冷水罐及其系统
            input_log_2_1 = "第2-1步：Q_out_ese=0，蓄冷水罐控制，目的是关闭蓄冷水罐及其系统..."
            print(input_log_2_1)
            write_log_data(file_fmu_input_log, [input_log_2_1], "info")
            write_log_data(file_fmu_input_feedback_log, [input_log_2_1], "info")
            algorithm_energy_storage_equipment(Q_user_list, time_name_list, Q0_total_in, Q0_total_out,
                                               energy_storage_equipment, [chilled_pump_to_user],
                                               [chilled_pump_in_storage], [], 1, 0, 0, 0, [n_storage_chilled_pump],
                                               [], storage_system_type_path, n_calculate_hour, cfg_path_equipment,
                                               cfg_path_public)

            # 第2-2步：用向用户侧供冷功率优化一次冷水机计算，不进行控制，用于获取冷冻水泵扬程
            input_log_2_2 = "第2-2步：用向用户侧供冷功率优化一次冷水机计算，不进行控制，用于获取冷冻水泵扬程..."
            print(input_log_2_2)
            chiller_Q_user = min(Q_user, chiller_Q0_max)
            write_txt_data(file_Q_value_chiller, [chiller_Q_user])
            ans_chiller2 = main_optimization_common_universal(H_chiller_chilled_pump, 0, H_chiller_cooling_pump,
                                                              chiller_list, chiller_chilled_pump_list, [],
                                                              chiller_cooling_pump_list, chiller_cooling_tower_list,
                                                              n_chiller_list, n_chiller_chilled_pump_list, [],
                                                              n_chiller_cooling_pump_list, n_chiller_cooling_tower_list,
                                                              chiller_system_type_path, cfg_path_public, cfg_path_equipment)
            chiller_user_chilled_pump_H = ans_chiller2[4]

            # 第2-3步：用向用户侧供冷供冷，冷水机优化和控制
            input_log_2_3 = "第2-3步：用向用户侧供冷供冷，冷水机优化和控制..."
            print(input_log_2_3)
            write_log_data(file_fmu_input_log, [input_log_2_3], "info")
            write_log_data(file_fmu_input_feedback_log, [input_log_2_3], "info")
            write_txt_data(file_Q_value_chiller, [chiller_Q_user])
            algorithm_common_universal(H_chiller_chilled_pump, 0, H_chiller_cooling_pump, chiller_list,
                                       chiller_chilled_pump_list, [], chiller_cooling_pump_list,
                                       chiller_cooling_tower_list, n_chiller_list, n_chiller_chilled_pump_list,
                                       [], n_chiller_cooling_pump_list, n_chiller_cooling_tower_list,
                                       chiller_system_type_path, n_calculate_hour, cfg_path_equipment, cfg_path_public)

            # 第2-4步：用向用户侧供冷功率，空气源热泵优化和控制
            input_log_2_4 = "第2-4步：用向用户侧供冷功率，空气源热泵优化和控制..."
            print(input_log_2_4)
            write_log_data(file_fmu_input_log, [input_log_2_4], "info")
            write_log_data(file_fmu_input_feedback_log, [input_log_2_4], "info")
            ashp_Q_user = min(Q_total - chiller_Q_user, ashp_Q0_max)
            H_ashp_chilled_pump = 0.65 * chiller_user_chilled_pump_H
            write_txt_data(file_Q_value_ashp, [ashp_Q_user])
            algorithm_common_universal(H_ashp_chilled_pump, 0, 0, [air_source_heat_pump], [ashp_chilled_pump],
                                       [], [], [], [n0_air_source_heat_pump], [n0_ashp_chilled_pump], [], [], [],
                                       ashp_system_type_path, n_calculate_hour, cfg_path_equipment, cfg_path_public)

        # 修改time_list
        time_name_list = generate_time_name_list(time_name_list)
        # 第3步：获取time，并仿真到指定时间
        input_log_3 = "第3步：获取time，并仿真到指定时间..."
        print(input_log_3)
        write_log_data(file_fmu_input_log, [input_log_3], "info")
        write_log_data(file_fmu_input_feedback_log, [input_log_3], "info")
        time_now = read_txt_data(file_fmu_time)[0]
        n_cal_now = int((time_now - start_time) / (3600 * (1 / n_calculate_hour)))
        simulate_time = start_time + (n_cal_now + 1) * 3600 * (1 / n_calculate_hour) - time_now
        if load_mode == 0:
            input_type_list = []
            input_data_list = []
        else:
            input_type_list = load_input_type(load_mode)
            input_data_list = [Q_user * 1000]
        result = main_simulate_pause_single(input_data_list, input_type_list, simulate_time, txt_path)

        # 第4步：获取FMU模型的实际数据并写入txt文件
        input_log_4 = "第4步：获取FMU模型的实际数据并写入txt文件..."
        print(input_log_4)
        main_get_fmu_real_data(result, cfg_path_equipment, txt_path)

        # 第5步：根据用户末端室内的温湿度，修正Teo
        if load_mode == 0:
            input_log_5 = "第5步：根据用户末端室内的温湿度，修正Teo..."
            print(input_log_5)
            write_log_data(file_fmu_input_log, [input_log_5], "info")
            write_log_data(file_fmu_input_feedback_log, [input_log_5], "info")
            algorithm_Teo_set_user(chiller_system_type_path, n_calculate_hour, chiller_list, n_chiller_list, [0])
            algorithm_Teo_set_user(ashp_system_type_path, n_calculate_hour, [air_source_heat_pump], n0_air_source_heat_pump, [0])
        else:
            input_log_5 = "第5步：修正Teo，PASS..."
            print(input_log_5)

    # 第6步：终止FMU模型，最后仿真一次
    input_log_6 = "第6步：终止FMU模型，最后仿真一次..."
    print(input_log_6)
    # 修改FMU状态
    fmu_state_list = [0, 1, stop_time, output_interval, time_out, tolerance]
    write_txt_data(file_fmu_state, fmu_state_list)
    # 最后仿真一次
    main_simulate_pause_single([], [], 3600, txt_path)


if __name__ == "__main__":
    # 相对路径
    txt_path = "./algorithm_file"
    # 负荷模型类型选择：0：user_load；1：simple_load
    load_mode = 0
    # 确定FMU模型文件
    if load_mode == 0:
        file_fmu = "./model_file/file_fmu/integrated_air_conditioning_Sdirk34hw.fmu"
    else:
        file_fmu = "./model_file/file_fmu/integrated_air_conditioning_simple_load_Sdirk34hw.fmu"
    # 执行程序
    run_run_steady_optimize(txt_path, file_fmu, load_mode)