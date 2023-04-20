from fmpy import extract, read_model_description
from identify_hydraulic_characteristic import main_identify_hydraulic_characteristic
from identify_equipment_characteristic import main_identify_equipment_characteristic

def run_identify_hydraulic_characteristic():
    fmu_path = "./model_data/file_fmu/integrated_air_conditioning_20230420.fmu"
    start_time = (31 + 28 + 31 + 30 + 31) * 24 * 3600
    stop_time = start_time + 2 * 3600
    output_interval = 60
    time_out = 600
    n_cal_f_pump = 3
    cfg_path_equipment = "./config/equipment_config.cfg"
    chiller_chilled_result_txt_path = "./model_data/file_txt/result_hydraulic_characteristic/chiller_chilled.txt"
    chiller_cooling_result_txt_path = "./model_data/file_txt/result_hydraulic_characteristic/chiller_cooling.txt"
    ashp_chilled_result_txt_path = "./model_data/file_txt/result_hydraulic_characteristic/ashp_chilled.txt"
    storage_from_chiller_result_txt_path = "./model_data/file_txt/result_hydraulic_characteristic/storage_from_chiller.txt"
    storage_to_user_result_txt_path = "./model_data/file_txt/result_hydraulic_characteristic/storage_to_user.txt"
    tower_chilled_result_txt_path = "./model_data/file_txt/result_hydraulic_characteristic/tower_chilled.txt"
    # 模型初始化
    fmu_unzipdir = extract(fmu_path)
    fmu_description = read_model_description(fmu_unzipdir)
    # 水力特性辨识
    main_identify_hydraulic_characteristic(fmu_unzipdir, fmu_description, start_time, stop_time, output_interval,
                                           time_out, n_cal_f_pump, cfg_path_equipment, chiller_chilled_result_txt_path,
                                           chiller_cooling_result_txt_path, ashp_chilled_result_txt_path,
                                           storage_from_chiller_result_txt_path, storage_to_user_result_txt_path,
                                           tower_chilled_result_txt_path)


def run_equipment_characteristic():
    fmu_path = "./model_data/file_fmu/system_characteristic_20230417.fmu"
    start_time = 0
    stop_time = start_time + 2 * 3600
    output_interval = 60
    time_out = 600
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
                                           time_out, cfg_path_equipment, chiller_big_cop_result_txt_path,
                                           chiller_small_cop_result_txt_path, ashp_cop_result_txt_path,
                                           cooling_tower_approach_result_txt_path)


if __name__ == "__main__":
    run_identify_hydraulic_characteristic()
    run_equipment_characteristic()