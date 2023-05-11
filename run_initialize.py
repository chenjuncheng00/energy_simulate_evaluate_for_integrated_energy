from algorithm_code.read_write_data import *
from system_default_status import air_source_heat_pump_default_status

if __name__ == "__main__":
    txt_path = "../optimal_control_algorithm_for_cooling_season"
    # 从配置文件读取设置的设备参数
    cfg_path_equipment = "./config/equipment_config.cfg"
    # 冷水机设备数量
    n_chiller1 = read_cfg_data(cfg_path_equipment, "冷水机1", "n_chiller1", 1)
    n_chiller2 = read_cfg_data(cfg_path_equipment, "冷水机2", "n_chiller2", 1)
    n_chiller_chilled_pump1 = read_cfg_data(cfg_path_equipment, "一级冷冻水泵_冷水机1", "n_chilled_pump1", 1)
    n_chiller_chilled_pump2 = read_cfg_data(cfg_path_equipment, "一级冷冻水泵_冷水机2", "n_chilled_pump2", 1)
    n_chiller_cooling_pump1 = read_cfg_data(cfg_path_equipment, "冷却水泵_冷水机1", "n_cooling_pump1", 1)
    n_chiller_cooling_pump2 = read_cfg_data(cfg_path_equipment, "冷却水泵_冷水机2", "n_cooling_pump2", 1)
    n_chiller_cooling_tower = read_cfg_data(cfg_path_equipment, "冷却塔_冷水机", "n_cooling_tower", 1)
    n_chiller = n_chiller1 + n_chiller2
    n_chiller_chilled_pump = n_chiller_chilled_pump1 + n_chiller_chilled_pump2
    n_chiller_cooling_pump = n_chiller_cooling_pump1 + n_chiller_cooling_pump2
    initialize_txt_chiller(txt_path, n_chiller, 0, n_chiller_chilled_pump, n_chiller_cooling_pump,
                           n_chiller_cooling_tower)
    # 空气源热泵数量
    n_air_source_heat_pump = read_cfg_data(cfg_path_equipment, "空气源热泵", "n_air_source_heat_pump", 1)
    n_ashp_chilled_pump = read_cfg_data(cfg_path_equipment, "一级冷冻水泵_空气源热泵", "n_chilled_pump", 1)
    initialize_txt_air_source_heat_pump(txt_path, n_air_source_heat_pump, 0, n_ashp_chilled_pump)
    # 温湿度传感器设备数量
    n_Tdo = read_cfg_data(cfg_path_equipment, "室外环境温湿度传感器", "n_Tdo", 1)
    n_Hro = read_cfg_data(cfg_path_equipment, "室外环境温湿度传感器", "n_Hro", 1)
    initialize_txt_other(txt_path, n_Tdo, 0, n_Hro)
    # 室内数量
    n_Tdi = read_cfg_data(cfg_path_equipment, "用户末端温湿度传感器", "n_Tdi", 1)
    n_Hri = read_cfg_data(cfg_path_equipment, "用户末端温湿度传感器", "n_Hri", 1)
    n_mau = read_cfg_data(cfg_path_equipment, "室内新风机组", "n_mau", 1)
    initialize_txt_user_terminal(txt_path, n_Tdi, n_Hri, n_mau, 0, 0, 0)
    # FMU仿真结果
    path_fmu_result = "./model_data/simulate_result"
    clear_all_txt_data(path_fmu_result)
    # 冷负荷总需求功率
    file_Q_total = "./model_data/simulate_result/fmu_Q_total.txt"
    write_txt_data(file_Q_total, [10000])

    # 系统初始化时，会降冷水机系统全开，但是其他系统全关
    ashp_equipment_type_path = ["air_source_heat_pump", txt_path]
    ashp_real_value_dict = air_source_heat_pump_default_status(n_air_source_heat_pump, n_ashp_chilled_pump)
    read_real_value_DO_station(ashp_real_value_dict, ashp_equipment_type_path, cfg_path_equipment)