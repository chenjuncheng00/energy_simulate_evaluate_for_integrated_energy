from fmpy import extract, read_model_description
from identify_hydraulic_characteristic import main_identify_hydraulic_characteristic
from identify_equipment_characteristic import main_identify_equipment_characteristic
from identify_system_dynamics import main_identify_system_dynamics
from identify_user_characteristic import identify_user_characteristic

def run_identify_hydraulic_characteristic(fmu_path, load_mode):
    """

    Args:
        fmu_path: [string]，FMU文件路径
        load_mode: [int]，0：user_load；1：simple_load

    Returns:

    """
    start_time = (31 + 28 + 31 + 30 + 31) * 24 * 3600
    stop_time = start_time + 2 * 3600
    output_interval = 60
    time_out = 600
    tolerance = 0.0001
    n_cal_f_pump = 5
    pump_f0_cal = True
    cfg_path_equipment = "./algorithm_file/config/equipment_config.cfg"
    chiller_chilled_result_txt_path = "./model_file/file_identify/result_hydraulic_characteristic/chiller_chilled.txt"
    chiller_cooling_result_txt_path = "./model_file/file_identify/result_hydraulic_characteristic/chiller_cooling.txt"
    ashp_chilled_result_txt_path = "./model_file/file_identify/result_hydraulic_characteristic/ashp_chilled.txt"
    storage_from_chiller_result_txt_path = "./model_file/file_identify/result_hydraulic_characteristic/storage_from_chiller.txt"
    storage_to_user_result_txt_path = "./model_file/file_identify/result_hydraulic_characteristic/storage_to_user.txt"
    chiller_user_storage_result_txt_path = "./model_file/file_identify/result_hydraulic_characteristic/chiller_user_storage.txt"
    full_open_result_txt_path = "./model_file/file_identify/result_hydraulic_characteristic/full_open.txt"
    # 模型初始化
    fmu_unzipdir = extract(fmu_path)
    fmu_description = read_model_description(fmu_unzipdir)
    # 水力特性辨识
    main_identify_hydraulic_characteristic(fmu_unzipdir, fmu_description, load_mode, start_time, stop_time,
                                           output_interval, time_out, tolerance, n_cal_f_pump, cfg_path_equipment,
                                           chiller_chilled_result_txt_path, chiller_cooling_result_txt_path,
                                           ashp_chilled_result_txt_path, storage_from_chiller_result_txt_path,
                                           storage_to_user_result_txt_path, chiller_user_storage_result_txt_path,
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
    tolerance = 0.0001
    cfg_path_equipment = "./algorithm_file/config/equipment_config.cfg"
    chiller_big_cop_result_txt_path = "./model_file/file_identify/result_equipment_characteristic/chiller_big_cop.txt"
    chiller_small_cop_result_txt_path = "./model_file/file_identify/result_equipment_characteristic/chiller_small_cop.txt"
    ashp_cop_result_txt_path = "./model_file/file_identify/result_equipment_characteristic/ashp_cop.txt"
    cooling_tower_approach_result_txt_path = "./model_file/file_identify/result_equipment_characteristic/cooling_tower_approach.txt"
    # 模型初始化
    fmu_unzipdir = extract(fmu_path)
    fmu_description = read_model_description(fmu_unzipdir)
    # 设备特性辨识
    main_identify_equipment_characteristic(fmu_unzipdir, fmu_description, start_time, stop_time, output_interval,
                                           time_out, tolerance, cfg_path_equipment, chiller_big_cop_result_txt_path,
                                           chiller_small_cop_result_txt_path, ashp_cop_result_txt_path,
                                           cooling_tower_approach_result_txt_path)


def run_identify_system_dynamics(fmu_path, path_matlab, txt_path, identify_mode):
    """

    Args:
        fmu_path: [string]，FMU文件路径
        path_matlab: [string]，matlab文件所在的路径
        txt_path: [string]，相对路径
        identify_mode: [int]，0:仅冷水机；1:冷水机+空气源热泵

    Returns:

    """
    # 模型初始化
    fmu_unzipdir = extract(fmu_path)
    fmu_description = read_model_description(fmu_unzipdir)
    start_time = 0
    stop_time = start_time + 96 * 3600
    output_interval = 30
    Ts = 10 * 60  # 采样时间
    time_out = 600
    tolerance = 0.0001
    cfg_path_equipment = "./algorithm_file/config/equipment_config.cfg"
    cfg_path_public = "./algorithm_file/config/public_config.cfg"
    # EER数据获取模型，0：直接读取FMU数据；1：保持Q不变，自行计算
    EER_mode = 0
    # 辨识的冷负荷列表，单位：kW
    if identify_mode == 0:
        Q_list = [14000, 13500, 13000, 12500, 12000, 11500, 11000, 10500, 10000, 9500, 9000, 8500, 8000,
                  7500, 7000, 6500, 6000, 5500, 5000, 4500, 4000, 3500, 3000, 2500, 2000]
    elif identify_mode == 1:
        Q_list = [14600, 15200, 15800, 16400, 17000, 17600]
        # Q_list = [16400]
    else:
        Q_list = []
    # 传递函数极点的最大数
    np_max = 3
    # 系统辨识得分的目标
    fitpercent_target_list = [95, 90, 85, 80, 75, 70, 65, 60, 55, 50]
    main_identify_system_dynamics(path_matlab, fmu_unzipdir, fmu_description, start_time, stop_time, output_interval,
                                  Ts, time_out, tolerance, np_max, fitpercent_target_list, EER_mode, Q_list, txt_path,
                                  cfg_path_equipment, cfg_path_public, identify_mode)


def run_identify_user_characteristic(fmu_path):
    """

    Args:
        fmu_path: [string]，FMU文件路径

    Returns:

    """
    fmu_unzipdir = extract(fmu_path)
    fmu_description = read_model_description(fmu_unzipdir)
    start_time = (31 + 28 + 31 + 30 + 31) * 24 * 3600
    stop_time = (31 + 28 + 31 + 30 + 31 + 30 + 31 + 31 + 30) * 24 * 3600
    output_interval = 10 * 60  # 与系统动态特性模型的采样周期Ts保持一致
    time_out = 600
    tolerance = 0.0001
    Teo_min = 5
    Teo_max = 10
    Tdi_target = 26
    identify_user_characteristic(fmu_unzipdir, fmu_description, start_time, stop_time, output_interval, time_out,
                                 tolerance, Teo_min, Teo_max, Tdi_target)


if __name__ == "__main__":
    # # 水力特性模型辨识
    # load_mode = 0
    # fmu_path = "./model_file/file_fmu/integrated_air_conditioning_Sdirk34hw.fmu"
    # run_identify_hydraulic_characteristic(fmu_path, load_mode)
    # # 设备性能模型辨识
    # fmu_path = "./model_file/file_fmu/equipment_characteristic_Cvode.fmu"
    # run_equipment_characteristic(fmu_path)
    # # 系统动态特性辨识
    # identify_mode = 1  # 0:仅冷水机；1:冷水机+空气源热泵
    # path_matlab = "/Users/chenjuncheng/Documents/Machine_Learning_Development/system_identification/air_conditioner_dynamic"
    # fmu_path = "./model_file/file_fmu/integrated_air_conditioning_simple_load_Sdirk34hw.fmu"
    # txt_path = "./algorithm_file"
    # run_identify_system_dynamics(fmu_path, path_matlab, txt_path, identify_mode)
    # 用户侧特性辨识
    fmu_path = "./model_file/file_fmu/user_characteristic_Cvode.fmu"
    run_identify_user_characteristic(fmu_path)