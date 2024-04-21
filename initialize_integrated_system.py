from algorithm_code import *
from model_fmu_input_type import main_model_input_type
from model_fmu_input_data_default import air_source_heat_pump_input_data_default, load_input_data_default, \
                                         tower_chilled_input_data_default, environment_input_data_default, \
                                         cold_storage_input_data_default, main_input_data_default

def initialize_integrated_system(file_fmu_time, file_fmu_state, start_time, stop_time, output_interval,
                                 time_out, tolerance, load_mode, txt_path):
    """
    integrated_air_conditioning.fmu"
    integrated_air_conditioning_simple_load.fmu"
    初始化完整模型：冷水机+空气源热泵+蓄冷水罐+冷却塔直接供冷+负荷(简单负荷 OR 复杂负荷)
    Args:
        file_fmu_time: [string]，储存FMU模型仿真时间(start_time)的文件路径
        file_fmu_state: [string]，储存FMU模型状态的文件路径
        start_time: [int]，仿真开始时间
        stop_time: [int]，仿真终止时间
        output_interval: [int]，仿真输出时间间隔
        time_out: [int]，仿真超时时间
        tolerance: [float]，FMU模型求解相对误差
        load_mode: [int]，0：user_load；1：simple_load
        txt_path: [string]，相对路径

    Returns:

    """
    print("正在初始化FMU模型......")
    # 第1步：初始化设置
    # FMU模型状态：依次为：fmu_initialize, fmu_terminate, stop_time, output_interval, time_out, tolerance
    fmu_state_list = [1, 0, stop_time, output_interval, time_out, tolerance]
    write_txt_data(file_fmu_state, fmu_state_list)
    # 初始化时间
    simulate_time1 = 24 * 3600
    t1_initialize = start_time + simulate_time1
    write_txt_data(file_fmu_time, [start_time])

    # 第2步：将蓄冷水罐充满
    print("初始化FMU模型：将蓄冷水罐充满...")
    # 冷水机模型输入数据
    chiller_turn_Teo = [True, True, True, True, True, True, 6]
    chiller_pump = [0, 0, 0, 0, 0, 0, 50, 50, 50, 50, 50, 50]
    chiller_tower = [1, 1, 1, 1, 1, 1]
    chiller_valve = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    chiller_tower_chilled_valve = [0, 0]
    chiller_user_valve = [0, 0]
    chiller_input_data = chiller_turn_Teo + chiller_pump + chiller_tower + chiller_valve + \
                         chiller_tower_chilled_valve + chiller_user_valve
    # 蓄冷水罐模型输入数据
    storage_pump = [50, 50, 50, 50]
    storage_chiller_valve = [1, 1, 1]
    storage_user_valve = [0, 0, 0]
    storage_input_data = storage_pump + storage_chiller_valve + storage_user_valve
    # FMU输入名称和数据类型
    input_type_list = main_model_input_type(load_mode)
    input_data_list = [start_time] + environment_input_data_default(load_mode) + chiller_input_data + \
                      air_source_heat_pump_input_data_default() + storage_input_data + \
                      tower_chilled_input_data_default() + load_input_data_default(load_mode)
    # FMU仿真
    main_simulate_pause_single(input_data_list, input_type_list, simulate_time1, txt_path, add_input=False)

    # 第3步：更新初始化设置
    # 修改FMU状态
    fmu_state_list = [0, 0, stop_time, output_interval, time_out, tolerance]
    write_txt_data(file_fmu_state, fmu_state_list)
    # 修改时间
    simulate_time2 = 23 * 3600
    t2_initialize = t1_initialize + simulate_time2
    write_txt_data(file_fmu_time, [t1_initialize])

    # 第4步：将管道内的水全部冷却下来
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
    # 空气源热泵模型输入数据
    ashp_turn_Teo = [True, True, True, True, 7]
    ashp_pump = [50, 50, 50, 50]
    ashp_valve = [1, 1, 1, 1]
    ashp_input_data = ashp_turn_Teo + ashp_pump + ashp_valve
    # FMU输入名称和数据类型
    input_type_list = main_model_input_type(load_mode)
    input_data_list = [t1_initialize] + environment_input_data_default(load_mode) + chiller_input_data + \
                      ashp_input_data + cold_storage_input_data_default() + \
                      tower_chilled_input_data_default() + load_input_data_default(load_mode)
    # FMU仿真
    main_simulate_pause_single(input_data_list, input_type_list, simulate_time2, txt_path, add_input=False)

    # 第5步：更新初始化设置
    # 修改时间
    simulate_time3 = 1 * 3600
    t3_initialize = t2_initialize + simulate_time3
    write_txt_data(file_fmu_time, [t2_initialize])

    # 第6步：关闭所有设备，恢复初始状态
    print("初始化FMU模型：关闭所有设备，恢复初始状态...")
    # FMU输入名称和数据类型
    input_type_list = main_model_input_type(load_mode)
    input_data_list = [t2_initialize] + main_input_data_default(load_mode)
    # FMU仿真
    main_simulate_pause_single(input_data_list, input_type_list, simulate_time3, txt_path, add_input=False)
    # 修改时间
    write_txt_data(file_fmu_time, [t3_initialize])
    print("\n")

    # 第6步：初始化总用时
    init_time_total = simulate_time1 + simulate_time2 + simulate_time3
    # 返回结果
    return init_time_total