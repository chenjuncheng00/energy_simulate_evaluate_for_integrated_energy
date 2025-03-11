import pickle
from algorithm_win import write_txt_data, algorithm_common_station

def run_compare(txt_path, Q_total):
    """

    Args:
        txt_path:
        Q_total:

    Returns:

    """
    # 设备类型名称(air_conditioner,air_source_heat_pump等)，相对路径
    chiller_system_type_path = ["chiller", txt_path]
    # Q_total储存文件
    file_Q_value_chiller = txt_path + "/real_value/energy_station/chiller/Q_value/chilled_main_pipe.txt"

    # cfg文件路径
    cfg_path_equipment = txt_path + "/config/equipment_config.cfg"
    cfg_path_public = txt_path + "/config/public_config.cfg"
    # 设备的pkl文件路径
    file_pkl_chiller = "./model_file/file_equipment/chiller.pkl"
    file_pkl_system = "./model_file/file_equipment/system.pkl"

    # 读取冷水机设备信息
    with open(file_pkl_chiller, "rb") as f_obj:
        chiller_dict = pickle.load(f_obj)
    H_chiller_chilled_pump = chiller_dict["H_chiller_chilled_pump"]
    H_chiller_cooling_pump = chiller_dict["H_chiller_cooling_pump"]
    chiller_list = chiller_dict["chiller_list"]
    chiller_chilled_pump_list = chiller_dict["chiller_chilled_pump_list"]
    chiller_cooling_pump_list = chiller_dict["chiller_cooling_pump_list"]
    chiller_cooling_tower_list = chiller_dict["chiller_cooling_tower_list"]
    n_chiller_list = chiller_dict["n_chiller_list"]
    n_chiller_chilled_pump_list = chiller_dict["n_chiller_chilled_pump_list"]
    n_chiller_cooling_pump_list = chiller_dict["n_chiller_cooling_pump_list"]
    n_chiller_cooling_tower_list = chiller_dict["n_chiller_cooling_tower_list"]
    # n_chiller_user_valve = chiller_dict["n_chiller_user_valve"]
    # 读取公共系统信息
    with open(file_pkl_system, "rb") as f_obj:
        system_dict = pickle.load(f_obj)
    n_calculate_hour = system_dict["n_calculate_hour"]

    write_txt_data(file_Q_value_chiller, [Q_total])
    algorithm_common_station(H_chiller_chilled_pump, 0, H_chiller_cooling_pump, chiller_list,
                             chiller_chilled_pump_list, [], chiller_cooling_pump_list,
                             chiller_cooling_tower_list, n_chiller_list, n_chiller_chilled_pump_list,
                             [], n_chiller_cooling_pump_list, n_chiller_cooling_tower_list,
                             chiller_system_type_path, n_calculate_hour, cfg_path_equipment, cfg_path_public)

if __name__ == "__main__":
    txt_path = "./algorithm_file"
    Q_total = 5495
    for i in range(10):
        run_compare(txt_path, Q_total)