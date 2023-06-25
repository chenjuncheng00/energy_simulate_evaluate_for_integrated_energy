import pickle
import numpy as np
from fmpy import *
from algorithm_code import *
from model_fmu_output_name import chiller_output_name, cold_storage_output_name, simple_load_output_name
from model_fmu_input_type import simple_load_input_type
from initialize_simple_load import initialize_simple_load
from run_initialize import run_initialize

def run_simple_load(txt_path, file_fmu):
    """
    冷水机+蓄冷水罐+简单的用户负荷
    搜算优化算法+GPC控制算法
    Args:
        txt_path: [string]，相对路径
        file_fmu: [string]，FMU模型文件

    Returns:

    """
    # cfg文件路径
    cfg_path_equipment = "./config/equipment_config.cfg"
    cfg_path_public = "./config/public_config.cfg"
    # 设备类型名称(air_conditioner,air_source_heat_pump等)，相对路径
    chiller_equipment_type_path = ["chiller", txt_path]
    # storage_equipment_type_path = ["energy_storage_equipment", txt_path]
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
    # chiller_chilled_pump_list = chiller_dict["chiller_chilled_pump_list"]
    # chiller_cooling_pump_list = chiller_dict["chiller_cooling_pump_list"]
    # chiller_cooling_tower_list = chiller_dict["chiller_cooling_tower_list"]
    # n_chiller_list = chiller_dict["n_chiller_list"]
    # n_chiller_chilled_pump_list = chiller_dict["n_chiller_chilled_pump_list"]
    # n_chiller_cooling_pump_list = chiller_dict["n_chiller_cooling_pump_list"]
    # n_chiller_cooling_tower_list = chiller_dict["n_chiller_cooling_tower_list"]
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
    # file_fmu_input_log = "./model_data/simulate_result/fmu_input_log.txt"
    # file_fmu_input_feedback_log = "./model_data/simulate_result/fmu_input_feedback_log.txt"
    # FMU仿真参数
    start_time = 1 * 24 * 3600
    stop_time = 31 * 24 * 3600 - 3600
    output_interval = 10
    time_out = 600
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
    file_fmu_output_name = txt_path + "/process_data/fmu_output_name.pkl"
    fmu_output_name = chiller_output_name()[0] + cold_storage_output_name()[0] + simple_load_output_name()
    with open(file_fmu_output_name, 'wb') as f:
        pickle.dump(fmu_output_name, f)
    # 冷负荷总需求功率
    file_Q_user = "./model_data/simulate_result/fmu_Q_user.txt"
    file_Q_user_list = "./model_data/fmu_Q_user_list.txt"
    # Q_time_all_list = read_txt_data(file_Q_user_list, column_index=0)
    Q_user_all_list = read_txt_data(file_Q_user_list, column_index=1)
    write_txt_data(file_Q_user, [Q_user_all_list[0]])
    # 每小时计算次数
    n_simulate = int((stop_time - start_time) / (3600 / n_calculate_hour))
    # 仿真结果
    file_fmu_result_all = "./model_data/simulate_result/fmu_result_all.txt"
    file_fmu_result_last = "./model_data/simulate_result/fmu_result_last.txt"
    txt_str = "start_time" + "\t" + "pause_time"
    for i in range(len(fmu_output_name)):
        txt_str += "\t" + fmu_output_name[i]
    write_txt_data(file_fmu_result_all, [txt_str])
    write_txt_data(file_fmu_result_last, [txt_str])
    # FMU模型初始化
    initialize_simple_load(file_fmu_time, file_fmu_state, start_time, stop_time, output_interval, time_out, txt_path)

    for i in range(n_simulate):
        print("一共需要计算" + str(n_simulate) + "次，正在进行第" + str(i + 1) + "次计算；已完成" + str(i) + "次计算；已完成" +
              str(np.round(100 * (i + 1) / n_simulate, 4)) + "%")
        # 读取Q_user
        Q_user = read_txt_data(file_Q_user)[0]

        # 第1步：冷水机优化+控制
        algorithm_chiller_double(Q_user, H_chiller_chilled_pump, 0, H_chiller_cooling_pump, chiller1,
                                 chiller2, chiller_chilled_pump1, chiller_chilled_pump2, None, None,
                                 chiller_cooling_pump1, chiller_cooling_pump2, chiller_cooling_tower, None,
                                 n0_chiller1, n0_chiller2, n0_chiller_chilled_pump1, n0_chiller_chilled_pump2,
                                 0, 0, n0_chiller_cooling_pump1, n0_chiller_cooling_pump2, n0_chiller_cooling_tower,
                                 0, chiller_equipment_type_path, n_calculate_hour, n_chiller_user_value,
                                 cfg_path_equipment, cfg_path_public)

        # 第2步：获取time，并仿真到指定时间
        time_now = read_txt_data(file_fmu_time)[0]
        n_cal_now = int((time_now - start_time) / (3600 * (1 / n_calculate_hour)))
        simulate_time = start_time + (n_cal_now + 1) * 3600 * (1 / n_calculate_hour) - time_now
        input_type_list = simple_load_input_type()
        input_data_list = [Q_user * 1000]
        main_simulate_pause_single(input_data_list, input_type_list, simulate_time, txt_path)

    # 修改FMU状态
    fmu_state_list = [0, 1, stop_time, output_interval, time_out]
    write_txt_data(file_fmu_state, fmu_state_list)
    # 最后仿真一次
    main_simulate_pause_single([], [], 3600, txt_path)


if __name__ == "__main__":
    txt_path = "../optimal_control_algorithm_for_cooling_season"
    file_fmu = "./model_data/file_fmu/chiller_and_storage_with_simple_load_Cvode.fmu"
    run_simple_load(txt_path, file_fmu)
