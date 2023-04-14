from fmpy import extract, read_model_description
from identify_hydraulic_characteristic import main_identify_hydraulic_characteristic

if __name__ == "__main__":
    fmu_path = "./model_data/file_fmu/integrated_air_conditioning_20230414.fmu"
    start_time = (31 + 28 + 31 + 30 + 31) * 24 * 3600
    stop_time = start_time + 2 * 3600
    output_interval = 60
    time_out = 600
    cfg_path_equipment = "./config/equipment_config.cfg"
    chiller_chilled_result_txt_path = "./model_data/file_txt/chiller_chilled_hydraulic_characteristic_result.txt"
    chiller_cooling_result_txt_path = "./model_data/file_txt/chiller_cooling_hydraulic_characteristic_result.txt"
    ashp_chilled_result_txt_path = "./model_data/file_txt/ashp_chilled_hydraulic_characteristic_result.txt"
    storage_from_chiller_result_txt_path = "./model_data/file_txt/storage_from_chiller_hydraulic_characteristic_result.txt"
    storage_to_user_result_txt_path = "./model_data/file_txt/storage_to_user_hydraulic_characteristic_result.txt"
    tower_chilled_result_txt_path = "./model_data/file_txt/tower_chilled_hydraulic_characteristic_result.txt"
    # 模型初始化
    fmu_unzipdir = extract(fmu_path)
    fmu_description = read_model_description(fmu_unzipdir)
    # 水力特性辨识
    main_identify_hydraulic_characteristic(fmu_unzipdir, fmu_description, start_time, stop_time, output_interval,
                                           time_out, cfg_path_equipment, chiller_chilled_result_txt_path,
                                           chiller_cooling_result_txt_path, ashp_chilled_result_txt_path,
                                           storage_from_chiller_result_txt_path, storage_to_user_result_txt_path,
                                           tower_chilled_result_txt_path)