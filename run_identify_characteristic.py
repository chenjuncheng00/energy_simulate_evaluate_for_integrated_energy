from identify_hydraulic_characteristic import identify_hydraulic_characteristic

if __name__ == "__main__":
    fmu_path = "./model_data/file_fmu/integrated_air_conditioning_20230411.fmu"
    start_time = (31 + 28 + 31 + 30 + 31) * 24 * 3600
    stop_time = start_time + 2 * 3600
    output_interval = 60
    cfg_path_equipment = "./config/equipment_config.cfg"
    chiller_chilled_result_txt_path = "./model_data/file_txt/chiller_chilled_hydraulic_characteristic_result.txt"
    chiller_cooling_result_txt_path = "./model_data/file_txt/chiller_cooling_hydraulic_characteristic_result.txt"
    ashp_chilled_result_txt_path = "./model_data/file_txt/ashp_chilled_hydraulic_characteristic_result.txt"
    storage_from_chiller_result_txt_path = "./model_data/file_txt/storage_from_chiller_hydraulic_characteristic_result.txt"
    storage_to_user_result_txt_path = "./model_data/file_txt/storage_to_user_hydraulic_characteristic_result.txt"
    tower_chilled_result_txt_path = "./model_data/file_txt/tower_chilled_hydraulic_characteristic_result.txt"
    identify_hydraulic_characteristic(fmu_path, start_time, stop_time, output_interval, cfg_path_equipment,
                                      chiller_chilled_result_txt_path, chiller_cooling_result_txt_path,
                                      ashp_chilled_result_txt_path, storage_from_chiller_result_txt_path,
                                      storage_to_user_result_txt_path, tower_chilled_result_txt_path)