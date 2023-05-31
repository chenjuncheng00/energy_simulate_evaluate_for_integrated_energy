from model_fmu_input_type import main_model_input_type
from model_fmu_input_data_default import air_source_heat_pump_input_data_default, user_load_input_data_default, \
                                         tower_chilled_input_data_default, environment_input_data_default, \
                                         main_input_data_default
from algorithm_code.other import *
from algorithm_code.read_write_data import *

def fmu_simulate_initialize(file_fmu_time, file_fmu_state, start_time, stop_time, output_interval, time_out, txt_path):
    """

    Args:
        file_fmu_time: [string]，储存FMU模型仿真时间(start_time)的文件路径
        file_fmu_state: [string]，储存FMU模型状态的文件路径
        start_time: [int]，仿真开始时间
        stop_time: [int]，仿真终止时间
        output_interval: [int]，仿真输出时间间隔
        time_out: [int]，仿真超时时间
        txt_path: [string]，相对路径

    Returns:

    """
    print("正在初始化FMU模型......")
    # 第1步：初始化设置
    # FMU模型状态：依次为：fmu_initialize, fmu_terminate, stop_time, output_interval, time_out
    fmu_state_list = [1, 0, stop_time, output_interval, time_out]
    write_txt_data(file_fmu_state, fmu_state_list)
    # 初始化时间
    t0_initialize = 10281600
    t1_initialize = start_time - 3600
    simulate_time = t1_initialize - t0_initialize
    write_txt_data(file_fmu_time, [t0_initialize])

    # 第2步：将蓄冷水罐充满
    print("初始化FMU模型：将蓄冷水罐充满...")
    # 冷水机模型输入数据
    chiller_data = [True, True, True, True, False, False, 6]
    chiller_pump = [0, 0, 0, 0, 0, 0, 50, 50, 50, 50, 50, 50]
    chiller_tower = [1, 1, 1, 1, 0, 0]
    chiller_value = [1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 0, 0]
    chiller_tower_chilled_value = [0, 0]
    chiller_user_value = [0, 0]
    chiller_input_data = chiller_data + chiller_pump + chiller_tower + chiller_value + \
                         chiller_tower_chilled_value + chiller_user_value
    # 蓄冷水罐模型输入数据
    storage_pump = [50, 50, 50, 50]
    storage_chiller_value = [1, 1, 1]
    storage_user_value = [0, 0, 0]
    storage_input_data = storage_pump + storage_chiller_value + storage_user_value
    # FMU输入名称和数据类型
    input_type_list = main_model_input_type()
    input_data_list = [t0_initialize] + environment_input_data_default() + chiller_input_data + \
                      air_source_heat_pump_input_data_default() + storage_input_data + \
                      tower_chilled_input_data_default() + user_load_input_data_default()
    # FMU仿真
    main_simulate_pause_single(input_data_list, input_type_list, simulate_time, txt_path, add_input=False)

    # 第3步：更新初始化设置
    # 修改FMU状态
    fmu_state_list = [0, 0, stop_time, output_interval, time_out]
    write_txt_data(file_fmu_state, fmu_state_list)
    # 初始化时间
    simulate_time = start_time - t1_initialize
    write_txt_data(file_fmu_time, [t1_initialize])

    # 第4步：关闭所有设备，恢复初始状态
    print("初始化FMU模型：关闭所有设备，恢复初始状态...")
    # FMU输入名称和数据类型
    input_type_list = main_model_input_type()
    input_data_list = [t1_initialize] + main_input_data_default()
    # FMU仿真
    main_simulate_pause_single(input_data_list, input_type_list, simulate_time, txt_path, add_input=False)