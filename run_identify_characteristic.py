from fmpy import extract, read_model_description
from identify_hydraulic_characteristic import main_identify_hydraulic_characteristic
from identify_equipment_characteristic import main_identify_equipment_characteristic
from identify_system_dynamics import main_identify_system_dynamics

def run_identify_hydraulic_characteristic(fmu_path):
    """

    Args:
        fmu_path: [string]，FMU文件路径

    Returns:

    """
    start_time = (31 + 28 + 31 + 30 + 31) * 24 * 3600
    stop_time = start_time + 2 * 3600
    output_interval = 60
    time_out = 600
    tolerance = 0.01
    n_cal_f_pump = 5
    pump_f0_cal = True
    cfg_path_equipment = "./config/equipment_config.cfg"
    chiller_chilled_result_txt_path = "./model_data/file_txt/result_hydraulic_characteristic/chiller_chilled.txt"
    chiller_cooling_result_txt_path = "./model_data/file_txt/result_hydraulic_characteristic/chiller_cooling.txt"
    ashp_chilled_result_txt_path = "./model_data/file_txt/result_hydraulic_characteristic/ashp_chilled.txt"
    storage_from_chiller_result_txt_path = "./model_data/file_txt/result_hydraulic_characteristic/storage_from_chiller.txt"
    storage_to_user_result_txt_path = "./model_data/file_txt/result_hydraulic_characteristic/storage_to_user.txt"
    chiller_user_storage_result_txt_path = "./model_data/file_txt/result_hydraulic_characteristic/chiller_user_storage.txt"
    tower_chilled_result_txt_path = "./model_data/file_txt/result_hydraulic_characteristic/tower_chilled.txt"
    tower_cooling_chilled_result_txt_path = "./model_data/file_txt/result_hydraulic_characteristic/tower_cooling_chilled.txt"
    full_open_result_txt_path = "./model_data/file_txt/result_hydraulic_characteristic/full_open.txt"
    # 模型初始化
    fmu_unzipdir = extract(fmu_path)
    fmu_description = read_model_description(fmu_unzipdir)
    # 水力特性辨识
    main_identify_hydraulic_characteristic(fmu_unzipdir, fmu_description, start_time, stop_time, output_interval,
                                           time_out, tolerance, n_cal_f_pump, cfg_path_equipment,
                                           chiller_chilled_result_txt_path, chiller_cooling_result_txt_path,
                                           ashp_chilled_result_txt_path, storage_from_chiller_result_txt_path,
                                           storage_to_user_result_txt_path, chiller_user_storage_result_txt_path,
                                           tower_chilled_result_txt_path, tower_cooling_chilled_result_txt_path,
                                           full_open_result_txt_path, pump_f0_cal)


def run_equipment_characteristic(fmu_path):
    """

    Args:
        fmu_path: [string]，FMU文件路径

    Returns:

    """
    start_time = 0
    stop_time = start_time + 2 * 3600
    output_interval = 60
    time_out = 600
    tolerance = 0.01
    cfg_path_equipment = "./config/equipment_config.cfg"
    chiller_big_cop_result_txt_path = "./model_data/file_txt/result_equipment_characteristic/chiller_big_cop.txt"
    chiller_small_cop_result_txt_path = "./model_data/file_txt/result_equipment_characteristic/chiller_small_cop.txt"
    ashp_cop_result_txt_path = "./model_data/file_txt/result_equipment_characteristic/ashp_cop.txt"
    cooling_tower_approach_result_txt_path = "./model_data/file_txt/result_equipment_characteristic/cooling_tower_approach.txt"
    # 模型初始化
    fmu_unzipdir = extract(fmu_path)
    fmu_description = read_model_description(fmu_unzipdir)
    # 设备特性辨识
    main_identify_equipment_characteristic(fmu_unzipdir, fmu_description, start_time, stop_time, output_interval,
                                           time_out, tolerance, cfg_path_equipment, chiller_big_cop_result_txt_path,
                                           chiller_small_cop_result_txt_path, ashp_cop_result_txt_path,
                                           cooling_tower_approach_result_txt_path)


def run_identify_system_dynamics(fmu_path, path_matlab, txt_path):
    """

    Args:
        fmu_path: [string]，FMU文件路径
        path_matlab: [string]，matlab文件所在的路径
        txt_path: [string]，相对路径

    Returns:

    """
    # 模型初始化
    fmu_unzipdir = extract(fmu_path)
    fmu_description = read_model_description(fmu_unzipdir)
    start_time = 0
    stop_time = start_time + 30 * 3600
    output_interval = 30
    Ts = 10 * 60  # 采样时间
    time_out = 600
    tolerance = 0.01
    chiller_equipment_type_path = ["chiller", txt_path]
    cfg_path_equipment = "./config/equipment_config.cfg"
    cfg_path_public = "./config/public_config.cfg"
    # EER数据获取模型，0：直接读取FMU数据；1：保持Q不变，自行计算
    EER_mode = 0
    # 需要被辨识的对象列表：Fcw、Few、Fca、Teo、Tci等
    chiller_object_list = ["Teo", "Few", "Fcw", "Fca"]
    # 模型输出模式：EER/Tei
    chiller_Y_mode_list = ["EER", "Tei"]
    # 辨识的冷负荷列表，单位：kW
    chiller_Q_list = [13000, 11000, 9000, 7000, 5000, 3000]
    # 传递函数极点的最大数
    np_max = 5
    # 系统辨识得分的目标
    fitpercent_target_list = [95, 90, 85, 80, 75, 70]
    main_identify_system_dynamics(path_matlab, fmu_unzipdir, fmu_description, start_time, stop_time, output_interval,
                                  Ts, time_out, tolerance, np_max, fitpercent_target_list, chiller_object_list,
                                  chiller_Y_mode_list, chiller_Q_list, EER_mode, chiller_equipment_type_path,
                                  cfg_path_equipment, cfg_path_public)


if __name__ == "__main__":
    # # 水力特性模型辨识
    # fmu_path = "./model_data/file_fmu/integrated_air_conditioning_Sdirk34hw.fmu"
    # run_identify_hydraulic_characteristic(fmu_path)
    # # 设备性能模型辨识
    # fmu_path = "./model_data/file_fmu/system_characteristic_Sdirk34hw.fmu"
    # run_equipment_characteristic(fmu_path)
    # 系统动态特性辨识
    path_matlab = "/Users/chenjuncheng/Documents/Machine_Learning_Development/system_identification/air_conditioner_dynamic"
    fmu_path = "./model_data/file_fmu/chiller_and_storage_with_simple_load_Sdirk34hw.fmu"
    txt_path = "../optimal_control_algorithm_for_cooling_season"
    run_identify_system_dynamics(fmu_path, path_matlab, txt_path)