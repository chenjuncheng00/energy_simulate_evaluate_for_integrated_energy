from algorithm_code.custom_model import *
from algorithm_code.read_write_data import *
from algorithm_code import *

def run_energy_storage_equipment(Q_total_list, time_list, Q0_total_in, Q0_total_out, chilled_value_open,
                                 n_calculate_hour, equipment_type_path, cfg_path_equipment, cfg_path_public):
    """

    Args:
        Q_total_list: [list]，逐时冷负荷需求功率，单位kW，长度24
        time_list: [list,string]，逐时用电时间段列表，字符串，长度24
        Q0_total_in: [double]，可以用来蓄冷的空调设备装机总功率，单位kW
        Q0_total_out: [double]，可以用来供冷的空调设备装机总功率，单位kW
        chilled_value_open: [double]，冷冻水泵，主机冷冻阀门开启比例
        n_calculate_hour: [int]，算法每小时的计算次数
        equipment_type_path: [string]，[list]，设备类型名称(air_conditioner,air_source_heat_pump等)，相对路径
        cfg_path_equipment: [string]，设备信息参数cfg文件路径
        cfg_path_public: [string]，公用参数cfg文件路径

    Returns:

    """
    # 扬程需求值(建议比实际的最小扬程需求值大一点，留余量)
    H_chilled_pump_to_user = read_cfg_data(cfg_path_equipment, "水泵扬程需求", "H_storage_chilled_pump_to_user", 0)
    H_chilled_pump_in_storage = read_cfg_data(cfg_path_equipment, "水泵扬程需求", "H_storage_chilled_pump_in_storage", 0)
    # 蓄冷阀门个数 AND 放冷阀门个数
    n_chilled_value_in_storage = read_cfg_data(cfg_path_equipment, "蓄冷阀门_蓄能装置", "n_chilled_value", 1)
    n_chilled_value_to_user = read_cfg_data(cfg_path_equipment, "放冷阀门_蓄能装置", "n_chilled_value", 1)
    # 水泵性能系数
    chilled_pump_to_user_Fw0_coef = read_cfg_data(cfg_path_equipment, "一级冷冻水泵_蓄能装置", "chilled_pump_to_user_Fw0_coef", 0)
    chilled_pump_to_user_H0_coef = read_cfg_data(cfg_path_equipment, "一级冷冻水泵_蓄能装置", "chilled_pump_to_user_H0_coef", 0)
    chilled_pump_to_user_P0_coef = read_cfg_data(cfg_path_equipment, "一级冷冻水泵_蓄能装置", "chilled_pump_to_user_P0_coef", 0)
    chilled_pump_in_storage_Fw0_coef = read_cfg_data(cfg_path_equipment, "一级冷冻水泵_蓄能装置", "chilled_pump_in_storage_Fw0_coef", 0)
    chilled_pump_in_storage_H0_coef = read_cfg_data(cfg_path_equipment, "一级冷冻水泵_蓄能装置", "chilled_pump_in_storage_H0_coef", 0)
    chilled_pump_in_storage_P0_coef = read_cfg_data(cfg_path_equipment, "一级冷冻水泵_蓄能装置", "chilled_pump_in_storage_P0_coef", 0)
    # 实例化蓄能装置
    energy_storage_equipment_Q0 = read_cfg_data(cfg_path_equipment, "蓄能装置", "energy_storage_equipment_Q0", 0)
    energy_storage_equipment_E0 = read_cfg_data(cfg_path_equipment, "蓄能装置", "energy_storage_equipment_E0", 0)
    energy_storage_equipment_alpha = read_cfg_data(cfg_path_equipment, "蓄能装置", "energy_storage_equipment_alpha", 0)
    energy_storage_equipment_beta = read_cfg_data(cfg_path_equipment, "蓄能装置", "energy_storage_equipment_beta", 0)
    energy_storage_equipment_Few0 = read_cfg_data(cfg_path_equipment, "蓄能装置", "energy_storage_equipment_Few0", 0)
    energy_storage_equipment = Energy_Storage_Equipment(energy_storage_equipment_Q0, energy_storage_equipment_E0,
                                                        energy_storage_equipment_alpha, energy_storage_equipment_beta,
                                                        energy_storage_equipment_Few0, n_calculate_hour)
    # 实例化冷冻水泵
    chilled_pump_f0 = read_cfg_data(cfg_path_equipment, "一级冷冻水泵_蓄能装置", "chilled_pump_f0", 0)
    chilled_pump_fmax = read_cfg_data(cfg_path_equipment, "一级冷冻水泵_蓄能装置", "chilled_pump_fmax", 0)
    chilled_pump_fmin = read_cfg_data(cfg_path_equipment, "一级冷冻水泵_蓄能装置", "chilled_pump_fmin", 0)
    chilled_pump_Few0 = read_cfg_data(cfg_path_equipment, "一级冷冻水泵_蓄能装置", "chilled_pump_Few0", 0)
    chilled_pump_H0 = read_cfg_data(cfg_path_equipment, "一级冷冻水泵_蓄能装置", "chilled_pump_H0", 0)
    chilled_pump_P0 = read_cfg_data(cfg_path_equipment, "一级冷冻水泵_蓄能装置", "chilled_pump_P0", 0)
    chilled_pump_Rw = read_cfg_data(cfg_path_equipment, "一级冷冻水泵_蓄能装置", "chilled_pump_Rw", 0)
    chilled_pump_f_status = read_cfg_data(cfg_path_equipment, "一级冷冻水泵_蓄能装置", "chilled_pump_f_status", 2)
    # 冷冻水泵：向用户侧供冷工况
    chilled_pump_to_user = Water_Pump(chilled_pump_to_user_Fw0_coef, chilled_pump_to_user_H0_coef,
                                      chilled_pump_to_user_P0_coef, chilled_pump_f0, chilled_pump_fmax,
                                      chilled_pump_fmin, chilled_pump_Few0, chilled_pump_H0, chilled_pump_P0,
                                      chilled_pump_Rw, chilled_pump_f_status)
    # 冷冻水泵：蓄冷工况
    chilled_pump_in_storage = Water_Pump(chilled_pump_in_storage_Fw0_coef, chilled_pump_in_storage_H0_coef,
                                         chilled_pump_in_storage_P0_coef, chilled_pump_f0, chilled_pump_fmax,
                                         chilled_pump_fmin, chilled_pump_Few0, chilled_pump_H0, chilled_pump_P0,
                                         chilled_pump_Rw, chilled_pump_f_status)
    # 计算
    algorithm_energy_storage_equipment(Q_total_list, time_list, Q0_total_in, Q0_total_out, energy_storage_equipment,
                                       chilled_pump_to_user, chilled_pump_in_storage, None, chilled_value_open,
                                       H_chilled_pump_to_user, H_chilled_pump_in_storage, 0,
                                       n_chilled_value_in_storage, n_chilled_value_to_user, equipment_type_path,
                                       n_calculate_hour, cfg_path_equipment, cfg_path_public)