import pickle
from algorithm_code import *

def generate_system_topology(cfg_path_equipment, file_raw_pickle):
    """

    Args:
        cfg_path_equipment:
        file_raw_pickle:

    Returns:

    """
    # 各个元素和设备数量
    n_user_load = 1
    n_chiller1 = read_cfg_data(cfg_path_equipment, "冷水机1", "n_chiller1", 1)
    n_chiller2 = read_cfg_data(cfg_path_equipment, "冷水机2", "n_chiller2", 1)
    n_chiller1_chilled_pump = read_cfg_data(cfg_path_equipment, "一级冷冻水泵_冷水机1", "n_chilled_pump1", 1)
    n_chiller2_chilled_pump = read_cfg_data(cfg_path_equipment, "一级冷冻水泵_冷水机2", "n_chilled_pump2", 1)
    n_chiller1_cooling_pump = read_cfg_data(cfg_path_equipment, "冷却水泵_冷水机1", "n_cooling_pump1", 1)
    n_chiller2_cooling_pump = read_cfg_data(cfg_path_equipment, "冷却水泵_冷水机2", "n_cooling_pump2", 1)
    n_chiller_cooling_tower = read_cfg_data(cfg_path_equipment, "冷却塔_冷水机", "n_cooling_tower", 1)
    n_air_source_heat_pump = read_cfg_data(cfg_path_equipment, "空气源热泵", "n_air_source_heat_pump", 1)
    n_ashp_chilled_pump = read_cfg_data(cfg_path_equipment, "一级冷冻水泵_空气源热泵", "n_chilled_pump", 1)
    n_air_conditioner = n_chiller1 + n_chiller2 + n_air_source_heat_pump
    n_cooling_source = n_chiller_cooling_tower + 1  # 6台冷却塔+空气
    n_chilled_pump = n_chiller1_chilled_pump + n_chiller2_chilled_pump + n_ashp_chilled_pump
    n_cooling_pump = n_chiller1_cooling_pump + n_chiller2_cooling_pump

    # 设备节点编号，从1开始
    user_load_index_in = 1
    chiller1_chilled_pump_index_out = 1
    chiller2_chilled_pump_index_out = 1
    ashp_chilled_pump_index_out = 1
    chiller1_chilled_pump_index_in = 2
    chiller2_chilled_pump_index_in = 2
    ashp_chilled_pump_index_in = 3
    chiller1_index_chilled = 2
    chiller2_index_chilled = 2
    ashp_index_chilled = 3
    chiller1_index_cooling = 4
    chiller2_index_cooling = 4
    ashp_index_cooling = 5
    chiller1_cooling_pump_index_out = 4
    chiller2_cooling_pump_index_out = 4
    chiller1_cooling_pump_index_in = 6
    chiller2_cooling_pump_index_in = 6
    chiller_cooling_tower_index_out = 6
    ashp_cooling_source_index_out = 5
    # 节点编号列表
    user_load_index_in_list = [user_load_index_in]
    chiller_index_chilled_list = []
    for i in range(n_chiller1):
        chiller_index_chilled_list.append(chiller1_index_chilled)
    for i in range(n_chiller2):
        chiller_index_chilled_list.append(chiller2_index_chilled)
    chiller_index_cooling_list = []
    for i in range(n_chiller1):
        chiller_index_cooling_list.append(chiller1_index_cooling)
    for i in range(n_chiller2):
        chiller_index_cooling_list.append(chiller2_index_cooling)
    chiller_chilled_pump_index_out_list = []
    for i in range(n_chiller1_chilled_pump):
        chiller_chilled_pump_index_out_list.append(chiller1_chilled_pump_index_out)
    for i in range(n_chiller2_chilled_pump):
        chiller_chilled_pump_index_out_list.append(chiller2_chilled_pump_index_out)
    chiller_chilled_pump_index_in_list = []
    for i in range(n_chiller1_chilled_pump):
        chiller_chilled_pump_index_in_list.append(chiller1_chilled_pump_index_in)
    for i in range(n_chiller2_chilled_pump):
        chiller_chilled_pump_index_in_list.append(chiller2_chilled_pump_index_in)
    chiller_cooling_pump_index_out_list = []
    for i in range(n_chiller1_cooling_pump):
        chiller_cooling_pump_index_out_list.append(chiller1_cooling_pump_index_out)
    for i in range(n_chiller2_cooling_pump):
        chiller_cooling_pump_index_out_list.append(chiller2_cooling_pump_index_out)
    chiller_cooling_pump_index_in_list = []
    for i in range(n_chiller1_cooling_pump):
        chiller_cooling_pump_index_in_list.append(chiller1_cooling_pump_index_in)
    for i in range(n_chiller2_cooling_pump):
        chiller_cooling_pump_index_in_list.append(chiller2_cooling_pump_index_in)
    chiller_cooling_tower_index_out_list = []
    for i in range(n_chiller_cooling_tower):
        chiller_cooling_tower_index_out_list.append(chiller_cooling_tower_index_out)
    ashp_index_chilled_list = []
    for i in range(n_air_source_heat_pump):
        ashp_index_chilled_list.append(ashp_index_chilled)
    ashp_index_cooling_list = []
    for i in range(n_air_source_heat_pump):
        ashp_index_cooling_list.append(ashp_index_cooling)
    ashp_chilled_pump_index_out_list = []
    for i in range(n_ashp_chilled_pump):
        ashp_chilled_pump_index_out_list.append(ashp_chilled_pump_index_out)
    ashp_chilled_pump_index_in_list = []
    for i in range(n_ashp_chilled_pump):
        ashp_chilled_pump_index_in_list.append(ashp_chilled_pump_index_in)
    ashp_cooling_source_index_out_list = [ashp_cooling_source_index_out]
    # 设备的自身编号，是一个列表，从101开始
    user_load_index_self_list = [101]
    chiller_index_self_list = [102, 103, 104, 105, 106, 107]
    chiller_chilled_pump_index_self_list = [108, 109, 110, 111, 112, 113]
    chiller_cooling_pump_index_self_list = [114, 115, 116, 116, 117, 119]
    chiller_cooling_tower_index_self_list = [120, 121, 122, 123, 124, 125]
    ashp_index_self_list = [126, 127, 128, 129]
    ashp_chilled_pump_index_self_list = [130, 131, 132, 133]
    ashp_cooling_source_index_self_list = [134]
    # 列表合并
    cooling_source_index_out_list = chiller_cooling_tower_index_out_list + ashp_cooling_source_index_out_list
    cooling_source_index_self_list = chiller_cooling_tower_index_self_list + ashp_cooling_source_index_self_list
    air_conditioner_index_chilled_list = chiller_index_chilled_list + ashp_index_chilled_list
    air_conditioner_index_cooling_list = chiller_index_cooling_list + ashp_index_cooling_list
    air_conditioner_index_self_list = chiller_index_self_list + ashp_index_self_list
    chilled_pump_index_in_list = chiller_chilled_pump_index_in_list + ashp_chilled_pump_index_in_list
    chilled_pump_index_out_list = chiller_chilled_pump_index_out_list + ashp_chilled_pump_index_out_list
    chilled_pump_index_self_list = chiller_chilled_pump_index_self_list + ashp_chilled_pump_index_self_list
    cooling_pump_index_in_list = chiller_cooling_pump_index_in_list
    cooling_pump_index_out_list = chiller_cooling_pump_index_out_list
    cooling_pump_index_self_list = chiller_cooling_pump_index_self_list

    # 生成拓扑结构字典
    index_dict = dict()
    for i in range(n_user_load):
        tmp_name = 'user_load_' + str(i)
        tmp_dict = {'index_in': user_load_index_in_list[i], 'index_self': user_load_index_self_list[i]}
        index_dict[tmp_name] = tmp_dict
    for i in range(n_cooling_source):
        tmp_name = 'cooling_source_' + str(i)
        tmp_dict = {'index_out': cooling_source_index_out_list[i], 'index_self': cooling_source_index_self_list[i]}
        index_dict[tmp_name] = tmp_dict
    for i in range(n_air_conditioner):
        tmp_name = 'air_conditioner_' + str(i)
        tmp_dict = {'index_chilled': air_conditioner_index_chilled_list[i],
                    'index_cooling': air_conditioner_index_cooling_list[i],
                    'index_self': air_conditioner_index_self_list[i]}
        index_dict[tmp_name] = tmp_dict
    for i in range(n_chilled_pump):
        tmp_name = 'chilled_pump_' + str(i)
        tmp_dict = {'index_in': chilled_pump_index_in_list[i],
                    'index_out': chilled_pump_index_out_list[i],
                    'index_self': chilled_pump_index_self_list[i]}
        index_dict[tmp_name] = tmp_dict
    for i in range(n_cooling_pump):
        tmp_name = 'cooling_pump_' + str(i)
        tmp_dict = {'index_in': cooling_pump_index_in_list[i],
                    'index_out': cooling_pump_index_out_list[i],
                    'index_self': cooling_pump_index_self_list[i]}
        index_dict[tmp_name] = tmp_dict
    number_dict = dict()
    number_dict['user_load'] = {'number': n_user_load}
    number_dict['cooling_source'] = {'number': n_cooling_source}
    number_dict['air_conditioner'] = {'number': n_air_conditioner}
    number_dict['chilled_pump'] = {'number': n_chilled_pump}
    number_dict['chilled_pump_secondary'] = {'number': 0}
    number_dict['cooling_pump'] = {'number': n_cooling_pump}
    raw_topology_dict = dict()
    raw_topology_dict['topology_index'] = index_dict
    raw_topology_dict['equipment_number'] = number_dict
    # 储存pickle文件，没有经过辨识的原始编号文件
    with open(file_raw_pickle, "wb") as f_obj:
        pickle.dump(raw_topology_dict, f_obj)


if __name__ == "__main__":
    cfg_path_equipment = './config/equipment_config.cfg'
    file_raw_pickle = "./model_data/raw_topology_index.pickle"
    generate_system_topology(cfg_path_equipment, file_raw_pickle)