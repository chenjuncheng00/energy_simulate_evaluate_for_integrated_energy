import pickle
import numpy as np
from fmpy import *
from algorithm_code.read_write_data import *
from algorithm_code.other import *
from run_chiller import run_chiller
from run_air_source_heat_pump import run_air_source_heat_pump
from model_fmu_output_name import main_model_output_name
from model_fmu_input_type import main_model_input_type
from model_fmu_input_data_default import main_input_data_default

def run_simulate_evaluate():

    # cfg文件路径
    cfg_path_equipment = "./config/equipment_config.cfg"
    cfg_path_public = "./config/public_config.cfg"
    # 设备类型名称(air_conditioner,air_source_heat_pump等)，相对路径
    txt_path = "../optimal_control_algorithm_for_cooling_season"
    chiller_equipment_type_path = ["chiller", txt_path]
    ashp_equipment_type_path = ["air_source_heat_pump", txt_path]
    storage_equipment_type_path = ["energy_storage_equipment", txt_path]

    # FMU文件
    file_fmu = "./model_data/file_fmu/integrated_air_conditioning_20230512.fmu"
    # FMU仿真参数
    start_time = (31 + 28 + 31 + 30 + 31 + 30) * 24 * 2600
    stop_time = (31 + 28 + 31 + 30 + 31 + 30 + 31 + 31) * 24 * 2600
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
    write_txt_data(file_fmu_time, [start_time])
    # FMU模型状态：依次为：fmu_initialize, fmu_terminate, stop_time, output_interval, time_out
    file_fmu_state = txt_path + "/process_data/fmu_state.txt"
    fmu_state_list = [1, 0, stop_time, output_interval, time_out]
    write_txt_data(file_fmu_state, fmu_state_list)
    # FMU模型输出名称
    file_fmu_output_name = txt_path + "/process_data/fmu_output_name.pkl"
    fmu_output_name = main_model_output_name()
    with open(file_fmu_output_name, 'wb') as f:
        pickle.dump(fmu_output_name, f)
    # 各系统制冷功率最大值
    chiller_Q0_max = 15600
    ashp_Q0_max = 4092
    # 冷负荷总需求功率
    file_Q_total = "./model_data/simulate_result/fmu_Q_total.txt"
    # 每小时计算次数
    n_calculate_hour = 1
    n_simulate = int((stop_time - start_time) / 3600 / n_calculate_hour)
    # 仿真结果
    file_fmu_result_all = "./model_data/simulate_result/fmu_result_all.txt"
    file_fmu_result_last = "./model_data/simulate_result/fmu_result_last.txt"
    txt_str = "start_time" + "\t" + "pause_time"
    for i in range(len(fmu_output_name)):
        txt_str += "\t" + fmu_output_name[i]
    write_txt_data(file_fmu_result_all, [txt_str])
    write_txt_data(file_fmu_result_last, [txt_str])
    # FMU输入名称和数据类型
    input_type_list = main_model_input_type()
    input_data_list = [start_time] + main_input_data_default()
    # 先仿真一次，启动系统
    print("正在初始化FMU模型......")
    hours_init = 1
    main_simulate_pause_single(input_data_list, input_type_list, hours_init * 3600, txt_path, add_input=False)
    # 修改FMU状态
    fmu_state_list = [0, 0, stop_time, output_interval, time_out]
    write_txt_data(file_fmu_state, fmu_state_list)

    # 运行
    for i in range(n_simulate)[hours_init:]:
        print("一共需要计算" + str(n_simulate) + "次，正在进行第" + str(i + 1) + "次计算；已完成" + str(i) + "次计算；已完成" +
              str(np.round(100 * (i + 1) / n_simulate, 4)) + "%")
        # 读取Q_total
        Q_total = read_txt_data(file_Q_total)[0]
        # 冷水机总负荷：包括蓄冷水罐蓄冷功率
        chiller_Q = min(Q_total, chiller_Q0_max)
        # # 先优化一次冷水机，不进行控制，用于获取阀门开启比例，用于蓄冷水罐和冷却塔直接供冷计算
        # ans_chiller = run_chiller(chiller_Q, n_calculate_hour, chiller_equipment_type_path,
        #                           cfg_path_equipment, cfg_path_public, True)
        # chiller_chilled_value_open = ans_chiller[2]
        # chiller_cooling_value_open = ans_chiller[3]
        # chiller_tower_value_open = ans_chiller[4]
        # 冷水机优化和控制
        run_chiller(chiller_Q, n_calculate_hour, chiller_equipment_type_path, cfg_path_equipment,
                    cfg_path_public, False)
        # 空气源热泵优化和控制
        air_source_heat_pump_Q = min(Q_total - chiller_Q, ashp_Q0_max)
        run_air_source_heat_pump(air_source_heat_pump_Q, n_calculate_hour, ashp_equipment_type_path,
                                 cfg_path_equipment, cfg_path_public, False)
        # 获取time，并仿真到指定时间
        time_now = read_txt_data(file_fmu_time)[0]
        simulate_time = start_time + (i + 1) * 3600 * (1 / n_calculate_hour) - time_now
        main_simulate_pause_single([], [], simulate_time, txt_path)

    # 修改FMU状态
    fmu_state_list = [0, 1, stop_time, output_interval, time_out]
    write_txt_data(file_fmu_state, fmu_state_list)
    # 最后仿真一次
    main_simulate_pause_single([], [], 3600, txt_path)


if __name__ == "__main__":
    run_simulate_evaluate()