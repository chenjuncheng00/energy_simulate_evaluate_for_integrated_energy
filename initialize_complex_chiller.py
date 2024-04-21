import numpy as np
from algorithm_code import *
from model_fmu_input_type import chiller_input_type, cold_storage_input_type, \
                                 simple_load_input_type, environment_input_type
from model_fmu_input_data_default import chiller_input_data_default, cold_storage_input_data_default, \
                                         simple_load_input_data_default, environment_input_data_default

def initialize_complex_chiller(file_fmu_time, file_fmu_state, start_time, stop_time, simulate_initialize,
                               output_interval, time_out, tolerance, txt_path):
    """
    chiller_and_storage_with_simple_load.fmu
    初始化模型：冷水机+蓄冷水罐+简单负荷
    Args:
        file_fmu_time: [string]，储存FMU模型仿真时间(start_time)的文件路径
        file_fmu_state: [string]，储存FMU模型状态的文件路径
        start_time: [int]，仿真开始时间
        stop_time: [int]，仿真终止时间
        simulate_initialize: [int]，初始化仿真时间
        output_interval: [int]，仿真输出时间间隔
        time_out: [int]，仿真超时时间
        tolerance: [float]，FMU模型求解相对误差
        txt_path: [string]，相对路径

    Returns:

    """
    print("正在初始化FMU模型......")
    # 0：user_load；1：simple_load
    load_mode = 1
    # 第1步：初始化设置
    # FMU模型状态：依次为：fmu_initialize, fmu_terminate, stop_time, output_interval, time_out, tolerance
    fmu_state_list = [1, 0, stop_time, output_interval, time_out, tolerance]
    write_txt_data(file_fmu_state, fmu_state_list)
    # 初始化时间
    t1_initialize = start_time + simulate_initialize
    write_txt_data(file_fmu_time, [start_time])

    # 第2步：将管道内的水全部冷却下来
    print("初始化FMU模型：将管道内的水全部冷却下来...")
    # 冷水机模型输入数据
    chiller_turn_Teo = [True, True, True, True, True, True, 7]
    chiller_pump = [50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50]
    chiller_tower = [1, 1, 1, 1, 1, 1]
    chiller_valve = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    chiller_tower_chilled_valve = [0, 0]
    chiller_user_valve = [1, 1]
    chiller_input_data = chiller_turn_Teo + chiller_pump + chiller_tower + chiller_valve + \
                         chiller_tower_chilled_valve + chiller_user_valve
    # 模型输入名称和类型
    input_type_list = [("time", np.float_)] + environment_input_type(load_mode)[0] + chiller_input_type()[0] + \
                      cold_storage_input_type()[0] + simple_load_input_type()
    # 模型输入数据
    input_data_list = [start_time] + environment_input_data_default(load_mode) + chiller_input_data + \
                      cold_storage_input_data_default() + simple_load_input_data_default()
    # FMU仿真
    main_simulate_pause_single(input_data_list, input_type_list, simulate_initialize, txt_path, add_input=False)

    # 第3步：更新初始化设置
    # 修改FMU状态
    fmu_state_list = [0, 0, stop_time, output_interval, time_out, tolerance]
    write_txt_data(file_fmu_state, fmu_state_list)
    # 初始化时间
    simulate_time2 = 1 * 3600
    t2_initialize = t1_initialize + simulate_time2
    write_txt_data(file_fmu_time, [t1_initialize])

    # 第4步：关闭所有设备，恢复初始状态
    print("初始化FMU模型：关闭所有设备，恢复初始状态...")
    # FMU输入名称和数据类型
    input_data_list = [t1_initialize] + environment_input_data_default(load_mode) + chiller_input_data_default() + \
                      cold_storage_input_data_default() + simple_load_input_data_default()
    # FMU仿真
    main_simulate_pause_single(input_data_list, input_type_list, simulate_time2, txt_path, add_input=False)
    # 修改时间
    write_txt_data(file_fmu_time, [t2_initialize])
    print("\n")

    # 第5步：初始化总用时
    init_time_total = simulate_initialize + simulate_time2
    # 返回结果
    return init_time_total