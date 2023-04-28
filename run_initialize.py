from algorithm_code.read_write_data import *

if __name__ == "__main__":
    txt_path = "../optimal_control_algorithm_for_cooling_season"
    # 从配置文件读取设置的设备参数
    cfg_path_equipment = "./config/equipment_config.cfg"
    # 冷水机设备数量
    n_chiller1 = read_cfg_data(cfg_path_equipment, "冷水机1", "n_chiller1", 1)
    n_chiller2 = read_cfg_data(cfg_path_equipment, "冷水机2", "n_chiller2", 1)
    n_chilled_pump1 = read_cfg_data(cfg_path_equipment, "冷冻水泵_冷水机1", "n_chilled_pump1", 1)
    n_chilled_pump2 = read_cfg_data(cfg_path_equipment, "冷冻水泵_冷水机2", "n_chilled_pump2", 1)
    n_cooling_pump1 = read_cfg_data(cfg_path_equipment, "冷却水泵_冷水机1", "n_cooling_pump1", 1)
    n_cooling_pump2 = read_cfg_data(cfg_path_equipment, "冷却水泵_冷水机2", "n_cooling_pump2", 1)
    n_cooling_tower = read_cfg_data(cfg_path_equipment, "冷却塔_冷水机", "n_cooling_tower", 1)
    n_chiller = n_chiller1 + n_chiller2
    n_chilled_pump = n_chilled_pump1 + n_chilled_pump2
    n_cooling_pump = n_cooling_pump1 + n_cooling_pump2
    initialize_txt_chiller(txt_path, n_chiller, 0, n_chilled_pump, n_cooling_pump, n_cooling_tower)

    # 温湿度传感器设备数量
    n_Tdo = read_cfg_data(cfg_path_equipment, "室外环境温湿度传感器", "n_Tdo", 1)
    n_Hro = read_cfg_data(cfg_path_equipment, "室外环境温湿度传感器", "n_Hro", 1)
    initialize_txt_other(txt_path, n_Tdo, 0, n_Hro)