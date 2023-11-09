from algorithm_code import *
from system_default_status import air_source_heat_pump_default_status, chiller_default_status, storage_default_status, \
                                  tower_chilled_default_status

def run_initialize(txt_path):
    """

    Args:
        txt_path: [string]，相对路径

    Returns:

    """
    # 从配置文件读取设置的设备参数
    cfg_path_equipment = "./config/equipment_config.cfg"
    # 系统公用二级冷冻水泵数量
    n_chilled_pump_secondary = read_cfg_data(cfg_path_equipment, "二级冷冻水泵", "n_chilled_pump_secondary", 1)
    # 向用户侧供冷阀门和冷却塔直接供冷阀门，默认数量都是2
    n_user_value = 2
    n_tower_chilled_value = 2
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
    initialize_txt_chiller(txt_path, n_chiller, n_chilled_pump_secondary, n_chiller_chilled_pump,
                           n_chiller_cooling_pump, n_chiller_cooling_tower, n_user_value, n_tower_chilled_value)

    # 空气源热泵数量
    n_air_source_heat_pump = read_cfg_data(cfg_path_equipment, "空气源热泵", "n_air_source_heat_pump", 1)
    n_ashp_chilled_pump = read_cfg_data(cfg_path_equipment, "一级冷冻水泵_空气源热泵", "n_chilled_pump", 1)
    initialize_txt_air_source_heat_pump(txt_path, n_air_source_heat_pump, n_chilled_pump_secondary,
                                        n_ashp_chilled_pump, n_user_value)

    # 冷却塔直接供冷设备数量
    n_tower_chilled_pump = read_cfg_data(cfg_path_equipment, "一级冷冻水泵_冷却塔直接供冷", "n_chilled_pump", 1)
    initialize_txt_tower_chilled(txt_path, n_chilled_pump_secondary, n_tower_chilled_pump)

    # 温湿度传感器设备数量
    n_Tdo = read_cfg_data(cfg_path_equipment, "室外环境温湿度传感器", "n_Tdo", 1)
    n_Hro = read_cfg_data(cfg_path_equipment, "室外环境温湿度传感器", "n_Hro", 1)
    initialize_txt_other(txt_path, n_Tdo, 0, n_Hro)
    # 室内数量
    n_Tdi = read_cfg_data(cfg_path_equipment, "用户末端温湿度传感器", "n_Tdi", 1)
    n_Hri = read_cfg_data(cfg_path_equipment, "用户末端温湿度传感器", "n_Hri", 1)
    n_mau = read_cfg_data(cfg_path_equipment, "室内新风机组", "n_mau", 1)
    initialize_txt_user_terminal(txt_path, n_Tdi, n_Hri, n_mau, 0, 0, 0)

    # 蓄冷水罐
    # 蓄冷阀门个数 AND 放冷阀门个数
    n_chilled_value_in_storage = read_cfg_data(cfg_path_equipment, "蓄冷阀门_蓄能装置", "n_chilled_value", 1)
    n_chilled_value_to_user = read_cfg_data(cfg_path_equipment, "放冷阀门_蓄能装置", "n_chilled_value", 1)
    n_storage_chilled_value = n_chilled_value_in_storage + n_chilled_value_to_user
    n_storage_chilled_pump = read_cfg_data(cfg_path_equipment, "一级冷冻水泵_蓄能装置", "n_chilled_pump", 1)
    initialize_txt_energy_storage_equipment(txt_path, n_chilled_pump_secondary, n_storage_chilled_pump,
                                            n_chilled_value_in_storage, n_chilled_value_to_user)
    file_storage_E = txt_path + "/real_value/energy_storage_equipment/Q_plan_E_plan/energy_storage_equipment_E.txt"
    energy_storage_equipment_E0 = read_cfg_data(cfg_path_equipment, "蓄能装置", "energy_storage_equipment_E0", 0)
    write_txt_data(file_storage_E, [energy_storage_equipment_E0])

    # FMU仿真结果
    path_fmu_result = "./model_data/simulate_log/"
    clear_all_txt_data(path_fmu_result)
    # 删除已有的.log文件
    delete_all_file(path_fmu_result, ".log")
    # 冷负荷总需求功率
    file_Q_total = "./model_data/file_Q/fmu_Q_user.txt"
    write_txt_data(file_Q_total, [10000])

    # 系统初始化时，会将冷水机系统全开，但是其他系统全关
    ashp_equipment_type_path = ["air_source_heat_pump", txt_path]
    ashp_real_value_dict = air_source_heat_pump_default_status(n_air_source_heat_pump, n_ashp_chilled_pump)
    read_real_value_DO_station(ashp_real_value_dict, n_user_value, ashp_equipment_type_path, cfg_path_equipment)
    chiller_equipment_type_path = ["chiller", txt_path]
    chiller_real_value_dict = chiller_default_status(n_chiller, n_chiller_chilled_pump, n_chiller_cooling_pump,
                                                     n_chiller_cooling_tower)
    read_real_value_DO_station(chiller_real_value_dict, n_user_value, chiller_equipment_type_path, cfg_path_equipment)
    storage_equipment_type_path = ["energy_storage_equipment", txt_path]
    storage_real_value_dict = storage_default_status(n_storage_chilled_value, n_storage_chilled_pump)
    read_real_value_DO_station(storage_real_value_dict, 0, storage_equipment_type_path, cfg_path_equipment)
    tower_chilled_equipment_type_path = ["tower_chilled", txt_path]
    tower_chilled_real_value_dict = tower_chilled_default_status(n_tower_chilled_pump)
    read_real_value_DO_station(tower_chilled_real_value_dict, 0, tower_chilled_equipment_type_path, cfg_path_equipment)

if __name__ == "__main__":
    txt_path = "../optimal_control_algorithm_for_cooling_season"
    run_initialize(txt_path)