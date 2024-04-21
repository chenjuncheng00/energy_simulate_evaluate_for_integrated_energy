import pickle
from algorithm_code import *

def generate_equipment_model(file_pkl_chiller, file_pkl_ashp, file_pkl_storage, file_pkl_tower_chilled,
                             file_pkl_system, cfg_path_equipment):
    """
    生成用于计算的系统设备模型，并保存
    之后在计算中只需要读取保存的数据即可
    Args:
        file_pkl_chiller: [string]，冷水机系统信息储存路径
        file_pkl_ashp: [string]，空气源热泵系统信息储存路径
        file_pkl_storage: [string]，蓄冷水罐系统信息储存路径
        file_pkl_tower_chilled: [string]，冷却塔直接供冷系统信息储存路径
        file_pkl_system: [string]，公用系统信息储存路径
        cfg_path_equipment: [string]，设备信息参数cfg文件路径

    Returns:

    """
    # 冷水机系统
    # 设备数量
    n_chiller1 = read_cfg_data(cfg_path_equipment, "冷水机1", "n_chiller1", 1)
    n_chiller2 = read_cfg_data(cfg_path_equipment, "冷水机2", "n_chiller2", 1)
    n_chiller_chilled_pump1 = read_cfg_data(cfg_path_equipment, "一级冷冻水泵_冷水机1", "n_chilled_pump1", 1)
    n_chiller_chilled_pump2 = read_cfg_data(cfg_path_equipment, "一级冷冻水泵_冷水机2", "n_chilled_pump2", 1)
    n_chiller_cooling_pump1 = read_cfg_data(cfg_path_equipment, "冷却水泵_冷水机1", "n_cooling_pump1", 1)
    n_chiller_cooling_pump2 = read_cfg_data(cfg_path_equipment, "冷却水泵_冷水机2", "n_cooling_pump2", 1)
    n_chiller_cooling_tower = read_cfg_data(cfg_path_equipment, "冷却塔_冷水机", "n_cooling_tower", 1)
    # 扬程需求值(建议比实际的最小扬程需求值大一点，留余量)
    H_chiller_chilled_pump = read_cfg_data(cfg_path_equipment, "水泵扬程需求", "H_chiller_chilled_pump", 0)
    H_chiller_cooling_pump = read_cfg_data(cfg_path_equipment, "水泵扬程需求", "H_chiller_cooling_pump", 0)
    # 水泵1性能系数
    chiller_cooling_pump1_Fw0_coef = read_cfg_data(cfg_path_equipment, "冷却水泵_冷水机1", "cooling_pump1_Fw0_coef", 0)
    chiller_cooling_pump1_H0_coef = read_cfg_data(cfg_path_equipment, "冷却水泵_冷水机1", "cooling_pump1_H0_coef", 0)
    chiller_cooling_pump1_P0_coef = read_cfg_data(cfg_path_equipment, "冷却水泵_冷水机1", "cooling_pump1_P0_coef", 0)
    chiller_chilled_pump1_Fw0_coef = read_cfg_data(cfg_path_equipment, "一级冷冻水泵_冷水机1", "chilled_pump1_Fw0_coef", 0)
    chiller_chilled_pump1_H0_coef = read_cfg_data(cfg_path_equipment, "一级冷冻水泵_冷水机1", "chilled_pump1_H0_coef", 0)
    chiller_chilled_pump1_P0_coef = read_cfg_data(cfg_path_equipment, "一级冷冻水泵_冷水机1", "chilled_pump1_P0_coef", 0)
    # 水泵2性能系数
    chiller_cooling_pump2_Fw0_coef = read_cfg_data(cfg_path_equipment, "冷却水泵_冷水机2", "cooling_pump2_Fw0_coef", 0)
    chiller_cooling_pump2_H0_coef = read_cfg_data(cfg_path_equipment, "冷却水泵_冷水机2", "cooling_pump2_H0_coef", 0)
    chiller_cooling_pump2_P0_coef = read_cfg_data(cfg_path_equipment, "冷却水泵_冷水机2", "cooling_pump2_P0_coef", 0)
    chiller_chilled_pump2_Fw0_coef = read_cfg_data(cfg_path_equipment, "一级冷冻水泵_冷水机2", "chilled_pump2_Fw0_coef", 0)
    chiller_chilled_pump2_H0_coef = read_cfg_data(cfg_path_equipment, "一级冷冻水泵_冷水机2", "chilled_pump2_H0_coef", 0)
    chiller_chilled_pump2_P0_coef = read_cfg_data(cfg_path_equipment, "一级冷冻水泵_冷水机2", "chilled_pump2_P0_coef", 0)
    # 实例化冷水机
    # 系数依次对应:常数项、负荷率的三次方、负荷率的平方、负荷率的一次方
    chiller1_cop_coef = read_cfg_data(cfg_path_equipment, "冷水机1", "chiller1_cop_coef", 0)
    chiller1_Q0_coef = read_cfg_data(cfg_path_equipment, "冷水机1", "chiller1_Q0_coef", 0)
    chiller1_Q0 = read_cfg_data(cfg_path_equipment, "冷水机1", "chiller1_Q0", 0)
    chiller1_alpha = read_cfg_data(cfg_path_equipment, "冷水机1", "chiller1_alpha", 0)
    chiller1_beta = read_cfg_data(cfg_path_equipment, "冷水机1", "chiller1_beta", 0)
    chiller1_Few0 = read_cfg_data(cfg_path_equipment, "冷水机1", "chiller1_Few0", 0)
    chiller1_Fcw0 = read_cfg_data(cfg_path_equipment, "冷水机1", "chiller1_Fcw0", 0)
    chiller1_Rew = read_cfg_data(cfg_path_equipment, "冷水机1", "chiller1_Rew", 0)
    chiller1_Rcw = read_cfg_data(cfg_path_equipment, "冷水机1", "chiller1_Rcw", 0)
    chiller1_f_status = read_cfg_data(cfg_path_equipment, "冷水机1", "chiller1_f_status", 2)
    chiller1 = Electric_Air_Conditioner(chiller1_cop_coef, chiller1_Q0_coef, chiller1_Q0, chiller1_alpha,
                                        chiller1_beta, chiller1_Few0, chiller1_Rew, chiller1_f_status)
    chiller1.Fcw0 = chiller1_Fcw0
    chiller1.Rcw = chiller1_Rcw
    chiller2_cop_coef = read_cfg_data(cfg_path_equipment, "冷水机2", "chiller2_cop_coef", 0)
    chiller2_Q0_coef = read_cfg_data(cfg_path_equipment, "冷水机2", "chiller2_Q0_coef", 0)
    chiller2_Q0 = read_cfg_data(cfg_path_equipment, "冷水机2", "chiller2_Q0", 0)
    chiller2_alpha = read_cfg_data(cfg_path_equipment, "冷水机2", "chiller2_alpha", 0)
    chiller2_beta = read_cfg_data(cfg_path_equipment, "冷水机2", "chiller2_beta", 0)
    chiller2_Few0 = read_cfg_data(cfg_path_equipment, "冷水机2", "chiller2_Few0", 0)
    chiller2_Fcw0 = read_cfg_data(cfg_path_equipment, "冷水机2", "chiller2_Fcw0", 0)
    chiller2_Rew = read_cfg_data(cfg_path_equipment, "冷水机2", "chiller2_Rew", 0)
    chiller2_Rcw = read_cfg_data(cfg_path_equipment, "冷水机2", "chiller2_Rcw", 0)
    chiller2_f_status = read_cfg_data(cfg_path_equipment, "冷水机2", "chiller2_f_status", 2)
    chiller2 = Electric_Air_Conditioner(chiller2_cop_coef, chiller2_Q0_coef, chiller2_Q0, chiller2_alpha,
                                        chiller2_beta, chiller2_Few0, chiller2_Rew, chiller2_f_status)
    chiller2.Fcw0 = chiller2_Fcw0
    chiller2.Rcw = chiller2_Rcw
    # 实例化冷却塔
    chiller_cooling_tower_approach_coef = read_cfg_data(cfg_path_equipment, "冷却塔_冷水机",
                                                        "cooling_tower_approach_coef", 0)
    # 系数依次对应:常数项、转速比的三次方、转速比的平方、转速比的一次方
    chiller_cooling_tower_f0 = read_cfg_data(cfg_path_equipment, "冷却塔_冷水机", "cooling_tower_f0", 0)
    chiller_cooling_tower_fmax = read_cfg_data(cfg_path_equipment, "冷却塔_冷水机", "cooling_tower_fmax", 0)
    chiller_cooling_tower_fmin = read_cfg_data(cfg_path_equipment, "冷却塔_冷水机", "cooling_tower_fmin", 0)
    chiller_cooling_tower_Fcw0 = read_cfg_data(cfg_path_equipment, "冷却塔_冷水机", "cooling_tower_Fcw0", 0)
    chiller_cooling_tower_P0 = read_cfg_data(cfg_path_equipment, "冷却塔_冷水机", "cooling_tower_P0", 0)
    chiller_cooling_tower_Rcw = read_cfg_data(cfg_path_equipment, "冷却塔_冷水机", "cooling_tower_Rcw", 0)
    chiller_cooling_tower_approach_design = read_cfg_data(cfg_path_equipment, "冷却塔_冷水机",
                                                          "cooling_tower_approach_design", 0)
    chiller_cooling_tower_f_status = read_cfg_data(cfg_path_equipment, "冷却塔_冷水机", "cooling_tower_f_status", 2)
    chiller_cooling_tower = Cooling_Tower(chiller_cooling_tower_approach_coef, chiller_cooling_tower_f0,
                                          chiller_cooling_tower_fmax, chiller_cooling_tower_fmin,
                                          chiller_cooling_tower_Fcw0, chiller_cooling_tower_P0,
                                          chiller_cooling_tower_Rcw, chiller_cooling_tower_approach_design,
                                          chiller_cooling_tower_f_status)
    # 实例化冷却水泵
    chiller_cooling_pump1_f0 = read_cfg_data(cfg_path_equipment, "冷却水泵_冷水机1", "cooling_pump1_f0", 0)
    chiller_cooling_pump1_fmax = read_cfg_data(cfg_path_equipment, "冷却水泵_冷水机1", "cooling_pump1_fmax", 0)
    chiller_cooling_pump1_fmin = read_cfg_data(cfg_path_equipment, "冷却水泵_冷水机1", "cooling_pump1_fmin", 0)
    chiller_cooling_pump1_Fcw0 = read_cfg_data(cfg_path_equipment, "冷却水泵_冷水机1", "cooling_pump1_Fcw0", 0)
    chiller_cooling_pump1_H0 = read_cfg_data(cfg_path_equipment, "冷却水泵_冷水机1", "cooling_pump1_H0", 0)
    chiller_cooling_pump1_P0 = read_cfg_data(cfg_path_equipment, "冷却水泵_冷水机1", "cooling_pump1_P0", 0)
    chiller_cooling_pump1_Rw = read_cfg_data(cfg_path_equipment, "冷却水泵_冷水机1", "cooling_pump1_Rw", 0)
    chiller_cooling_pump1_f_status = read_cfg_data(cfg_path_equipment, "冷却水泵_冷水机1", "cooling_pump1_f_status", 2)
    chiller_cooling_pump1 = Water_Pump(chiller_cooling_pump1_Fw0_coef, chiller_cooling_pump1_H0_coef,
                                       chiller_cooling_pump1_P0_coef, chiller_cooling_pump1_f0,
                                       chiller_cooling_pump1_fmax, chiller_cooling_pump1_fmin,
                                       chiller_cooling_pump1_Fcw0, chiller_cooling_pump1_H0, chiller_cooling_pump1_P0,
                                       chiller_cooling_pump1_Rw, chiller_cooling_pump1_f_status)
    chiller_cooling_pump2_f0 = read_cfg_data(cfg_path_equipment, "冷却水泵_冷水机2", "cooling_pump2_f0", 0)
    chiller_cooling_pump2_fmax = read_cfg_data(cfg_path_equipment, "冷却水泵_冷水机2", "cooling_pump2_fmax", 0)
    chiller_cooling_pump2_fmin = read_cfg_data(cfg_path_equipment, "冷却水泵_冷水机2", "cooling_pump2_fmin", 0)
    chiller_cooling_pump2_Fcw0 = read_cfg_data(cfg_path_equipment, "冷却水泵_冷水机2", "cooling_pump2_Fcw0", 0)
    chiller_cooling_pump2_H0 = read_cfg_data(cfg_path_equipment, "冷却水泵_冷水机2", "cooling_pump2_H0", 0)
    chiller_cooling_pump2_P0 = read_cfg_data(cfg_path_equipment, "冷却水泵_冷水机2", "cooling_pump2_P0", 0)
    chiller_cooling_pump2_Rw = read_cfg_data(cfg_path_equipment, "冷却水泵_冷水机2", "cooling_pump2_Rw", 0)
    chiller_cooling_pump2_f_status = read_cfg_data(cfg_path_equipment, "冷却水泵_冷水机2", "cooling_pump2_f_status", 2)
    chiller_cooling_pump2 = Water_Pump(chiller_cooling_pump2_Fw0_coef, chiller_cooling_pump2_H0_coef,
                                       chiller_cooling_pump2_P0_coef, chiller_cooling_pump2_f0,
                                       chiller_cooling_pump2_fmax, chiller_cooling_pump2_fmin,
                                       chiller_cooling_pump2_Fcw0, chiller_cooling_pump2_H0, chiller_cooling_pump2_P0,
                                       chiller_cooling_pump2_Rw, chiller_cooling_pump2_f_status)
    # 实例化冷冻水泵
    chiller_chilled_pump1_f0 = read_cfg_data(cfg_path_equipment, "一级冷冻水泵_冷水机1", "chilled_pump1_f0", 0)
    chiller_chilled_pump1_fmax = read_cfg_data(cfg_path_equipment, "一级冷冻水泵_冷水机1", "chilled_pump1_fmax", 0)
    chiller_chilled_pump1_fmin = read_cfg_data(cfg_path_equipment, "一级冷冻水泵_冷水机1", "chilled_pump1_fmin", 0)
    chiller_chilled_pump1_Few0 = read_cfg_data(cfg_path_equipment, "一级冷冻水泵_冷水机1", "chilled_pump1_Few0", 0)
    chiller_chilled_pump1_H0 = read_cfg_data(cfg_path_equipment, "一级冷冻水泵_冷水机1", "chilled_pump1_H0", 0)
    chiller_chilled_pump1_P0 = read_cfg_data(cfg_path_equipment, "一级冷冻水泵_冷水机1", "chilled_pump1_P0", 0)
    chiller_chilled_pump1_Rw = read_cfg_data(cfg_path_equipment, "一级冷冻水泵_冷水机1", "chilled_pump1_Rw", 0)
    chiller_chilled_pump1_f_status = read_cfg_data(cfg_path_equipment, "一级冷冻水泵_冷水机1", "chilled_pump1_f_status", 2)
    chiller_chilled_pump1 = Water_Pump(chiller_chilled_pump1_Fw0_coef, chiller_chilled_pump1_H0_coef,
                                       chiller_chilled_pump1_P0_coef, chiller_chilled_pump1_f0,
                                       chiller_chilled_pump1_fmax, chiller_chilled_pump1_fmin,
                                       chiller_chilled_pump1_Few0, chiller_chilled_pump1_H0, chiller_chilled_pump1_P0,
                                       chiller_chilled_pump1_Rw, chiller_chilled_pump1_f_status)
    chiller_chilled_pump2_f0 = read_cfg_data(cfg_path_equipment, "一级冷冻水泵_冷水机2", "chilled_pump2_f0", 0)
    chiller_chilled_pump2_fmax = read_cfg_data(cfg_path_equipment, "一级冷冻水泵_冷水机2", "chilled_pump2_fmax", 0)
    chiller_chilled_pump2_fmin = read_cfg_data(cfg_path_equipment, "一级冷冻水泵_冷水机2", "chilled_pump2_fmin", 0)
    chiller_chilled_pump2_Few0 = read_cfg_data(cfg_path_equipment, "一级冷冻水泵_冷水机2", "chilled_pump2_Few0", 0)
    chiller_chilled_pump2_H0 = read_cfg_data(cfg_path_equipment, "一级冷冻水泵_冷水机2", "chilled_pump2_H0", 0)
    chiller_chilled_pump2_P0 = read_cfg_data(cfg_path_equipment, "一级冷冻水泵_冷水机2", "chilled_pump2_P0", 0)
    chiller_chilled_pump2_Rw = read_cfg_data(cfg_path_equipment, "一级冷冻水泵_冷水机2", "chilled_pump2_Rw", 0)
    chiller_chilled_pump2_f_status = read_cfg_data(cfg_path_equipment, "一级冷冻水泵_冷水机2", "chilled_pump2_f_status", 2)
    chiller_chilled_pump2 = Water_Pump(chiller_chilled_pump2_Fw0_coef, chiller_chilled_pump2_H0_coef,
                                       chiller_chilled_pump2_P0_coef, chiller_chilled_pump2_f0,
                                       chiller_chilled_pump2_fmax, chiller_chilled_pump2_fmin,
                                       chiller_chilled_pump2_Few0, chiller_chilled_pump2_H0, chiller_chilled_pump2_P0,
                                       chiller_chilled_pump2_Rw, chiller_chilled_pump2_f_status)
    chiller_list = [chiller1, chiller2]
    n_chiller_list = [n_chiller1, n_chiller2]
    chiller_chilled_pump_list = [chiller_chilled_pump1, chiller_chilled_pump2]
    n_chiller_chilled_pump_list = [n_chiller_chilled_pump1, n_chiller_chilled_pump2]
    chiller_cooling_pump_list = [chiller_cooling_pump1, chiller_cooling_pump2]
    n_chiller_cooling_pump_list = [n_chiller_cooling_pump1, n_chiller_cooling_pump2]
    chiller_cooling_tower_list = [chiller_cooling_tower]
    n_chiller_cooling_tower_list = [n_chiller_cooling_tower]
    n_chiller_user_valve = 2
    # 保存冷水机模型文件
    chiller_dict = dict()
    chiller_dict["H_chiller_chilled_pump"] = H_chiller_chilled_pump
    chiller_dict["H_chiller_cooling_pump"] = H_chiller_cooling_pump
    chiller_dict["chiller_list"] = chiller_list
    chiller_dict["chiller_chilled_pump_list"] = chiller_chilled_pump_list
    chiller_dict["chiller_cooling_pump_list"] = chiller_cooling_pump_list
    chiller_dict["chiller_cooling_tower_list"] = chiller_cooling_tower_list
    chiller_dict["n_chiller_list"] = n_chiller_list
    chiller_dict["n_chiller_chilled_pump_list"] = n_chiller_chilled_pump_list
    chiller_dict["n_chiller_cooling_pump_list"] = n_chiller_cooling_pump_list
    chiller_dict["n_chiller_cooling_tower_list"] = n_chiller_cooling_tower_list
    chiller_dict["chiller1"] = chiller1
    chiller_dict["chiller2"] = chiller2
    chiller_dict["chiller_chilled_pump1"] = chiller_chilled_pump1
    chiller_dict["chiller_chilled_pump2"] = chiller_chilled_pump2
    chiller_dict["chiller_cooling_pump1"] = chiller_cooling_pump1
    chiller_dict["chiller_cooling_pump2"] = chiller_cooling_pump2
    chiller_dict["chiller_cooling_tower"] = chiller_cooling_tower
    chiller_dict["n_chiller1"] = n_chiller1
    chiller_dict["n_chiller2"] = n_chiller2
    chiller_dict["n_chiller_chilled_pump1"] = n_chiller_chilled_pump1
    chiller_dict["n_chiller_chilled_pump2"] = n_chiller_chilled_pump2
    chiller_dict["n_chiller_cooling_pump1"] = n_chiller_cooling_pump1
    chiller_dict["n_chiller_cooling_pump2"] = n_chiller_cooling_pump2
    chiller_dict["n_chiller_cooling_tower"] = n_chiller_cooling_tower
    chiller_dict["n_chiller_user_valve"] = n_chiller_user_valve
    with open(file_pkl_chiller, "wb") as f:
        pickle.dump(chiller_dict, f)

    # 实例化空气源热泵系统设备模型
    n_air_source_heat_pump = read_cfg_data(cfg_path_equipment, "空气源热泵", "n_air_source_heat_pump", 1)
    n_ashp_chilled_pump = read_cfg_data(cfg_path_equipment, "一级冷冻水泵_空气源热泵", "n_chilled_pump", 1)
    # 扬程需求值(建议比实际的最小扬程需求值大一点，留余量)
    H_ashp_chilled_pump = read_cfg_data(cfg_path_equipment, "水泵扬程需求", "H_ashp_chilled_pump", 0)
    # 水泵性能系数
    ashp_chilled_pump_Fw0_coef = read_cfg_data(cfg_path_equipment, "一级冷冻水泵_空气源热泵", "chilled_pump_Fw0_coef", 0)
    ashp_chilled_pump_H0_coef = read_cfg_data(cfg_path_equipment, "一级冷冻水泵_空气源热泵", "chilled_pump_H0_coef", 0)
    ashp_chilled_pump_P0_coef = read_cfg_data(cfg_path_equipment, "一级冷冻水泵_空气源热泵", "chilled_pump_P0_coef", 0)
    # 实例化空气源热泵，输出空气源热泵列表
    # 系数依次对应:常数项、负荷率的三次方、负荷率的平方、负荷率的一次方
    air_source_heat_pump_cop_coef = read_cfg_data(cfg_path_equipment, "空气源热泵", "air_source_heat_pump_cop_coef", 0)
    air_source_heat_pump_Q0_coef = read_cfg_data(cfg_path_equipment, "空气源热泵", "air_source_heat_pump_Q0_coef", 0)
    air_source_heat_pump_Q0 = read_cfg_data(cfg_path_equipment, "空气源热泵", "air_source_heat_pump_Q0", 0)
    air_source_heat_pump_alpha = read_cfg_data(cfg_path_equipment, "空气源热泵", "air_source_heat_pump_alpha", 0)
    air_source_heat_pump_beta = read_cfg_data(cfg_path_equipment, "空气源热泵", "air_source_heat_pump_beta", 0)
    air_source_heat_pump_Few0 = read_cfg_data(cfg_path_equipment, "空气源热泵", "air_source_heat_pump_Few0", 0)
    air_source_heat_pump_Rew = read_cfg_data(cfg_path_equipment, "空气源热泵", "air_source_heat_pump_Rew", 0)
    air_source_heat_pump_f_status = read_cfg_data(cfg_path_equipment, "空气源热泵", "air_source_heat_pump_f_status", 2)
    air_source_heat_pump = Electric_Air_Conditioner(air_source_heat_pump_cop_coef, air_source_heat_pump_Q0_coef,
                                                    air_source_heat_pump_Q0, air_source_heat_pump_alpha,
                                                    air_source_heat_pump_beta, air_source_heat_pump_Few0,
                                                    air_source_heat_pump_Rew, air_source_heat_pump_f_status)
    # 实例化一级冷冻水泵
    ashp_chilled_pump_f0 = read_cfg_data(cfg_path_equipment, "一级冷冻水泵_空气源热泵", "chilled_pump_f0", 0)
    ashp_chilled_pump_fmax = read_cfg_data(cfg_path_equipment, "一级冷冻水泵_空气源热泵", "chilled_pump_fmax", 0)
    ashp_chilled_pump_fmin = read_cfg_data(cfg_path_equipment, "一级冷冻水泵_空气源热泵", "chilled_pump_fmin", 0)
    ashp_chilled_pump_Few0 = read_cfg_data(cfg_path_equipment, "一级冷冻水泵_空气源热泵", "chilled_pump_Few0", 0)
    ashp_chilled_pump_H0 = read_cfg_data(cfg_path_equipment, "一级冷冻水泵_空气源热泵", "chilled_pump_H0", 0)
    ashp_chilled_pump_P0 = read_cfg_data(cfg_path_equipment, "一级冷冻水泵_空气源热泵", "chilled_pump_P0", 0)
    ashp_chilled_pump_Rw = read_cfg_data(cfg_path_equipment, "一级冷冻水泵_空气源热泵", "chilled_pump_Rw", 0)
    ashp_chilled_pump_f_status = read_cfg_data(cfg_path_equipment, "一级冷冻水泵_空气源热泵",
                                               "chilled_pump_f_status", 2)
    ashp_chilled_pump = Water_Pump(ashp_chilled_pump_Fw0_coef, ashp_chilled_pump_H0_coef, ashp_chilled_pump_P0_coef,
                                   ashp_chilled_pump_f0, ashp_chilled_pump_fmax, ashp_chilled_pump_fmin,
                                   ashp_chilled_pump_Few0, ashp_chilled_pump_H0, ashp_chilled_pump_P0,
                                   ashp_chilled_pump_Rw, ashp_chilled_pump_f_status)
    # 保存空气源热泵模型文件
    ashp_dict = dict()
    ashp_dict["H_ashp_chilled_pump"] = H_ashp_chilled_pump
    ashp_dict["n_air_source_heat_pump"] = n_air_source_heat_pump
    ashp_dict["n_ashp_chilled_pump"] = n_ashp_chilled_pump
    ashp_dict["air_source_heat_pump"] = air_source_heat_pump
    ashp_dict["ashp_chilled_pump"] = ashp_chilled_pump
    with open(file_pkl_ashp, "wb") as f:
        pickle.dump(ashp_dict, f)

    # 实例化蓄冷系统设备模型
    # 每小时计算次数
    n_calculate_hour = 1
    # 扬程需求值(建议比实际的最小扬程需求值大一点，留余量)
    H_chilled_pump_to_user = read_cfg_data(cfg_path_equipment, "水泵扬程需求", "H_storage_chilled_pump_to_user", 0)
    H_chilled_pump_in_storage = read_cfg_data(cfg_path_equipment, "水泵扬程需求", "H_storage_chilled_pump_in_storage", 0)
    # 蓄冷阀门个数 AND 放冷阀门个数
    n_chilled_valve_in_storage = read_cfg_data(cfg_path_equipment, "蓄冷阀门_蓄能装置", "n_chilled_valve", 1)
    n_chilled_valve_to_user = read_cfg_data(cfg_path_equipment, "放冷阀门_蓄能装置", "n_chilled_valve", 1)
    # 水泵性能系数
    chilled_pump_to_user_Fw0_coef = read_cfg_data(cfg_path_equipment, "一级冷冻水泵_蓄能装置",
                                                  "chilled_pump_to_user_Fw0_coef", 0)
    chilled_pump_to_user_H0_coef = read_cfg_data(cfg_path_equipment, "一级冷冻水泵_蓄能装置",
                                                 "chilled_pump_to_user_H0_coef", 0)
    chilled_pump_to_user_P0_coef = read_cfg_data(cfg_path_equipment, "一级冷冻水泵_蓄能装置",
                                                 "chilled_pump_to_user_P0_coef", 0)
    chilled_pump_in_storage_Fw0_coef = read_cfg_data(cfg_path_equipment, "一级冷冻水泵_蓄能装置",
                                                     "chilled_pump_in_storage_Fw0_coef", 0)
    chilled_pump_in_storage_H0_coef = read_cfg_data(cfg_path_equipment, "一级冷冻水泵_蓄能装置",
                                                    "chilled_pump_in_storage_H0_coef", 0)
    chilled_pump_in_storage_P0_coef = read_cfg_data(cfg_path_equipment, "一级冷冻水泵_蓄能装置",
                                                    "chilled_pump_in_storage_P0_coef", 0)
    # 实例化蓄能装置
    energy_storage_equipment_Q0 = read_cfg_data(cfg_path_equipment, "蓄能装置", "energy_storage_equipment_Q0", 0)
    energy_storage_equipment_E0 = read_cfg_data(cfg_path_equipment, "蓄能装置", "energy_storage_equipment_E0", 0)
    energy_storage_equipment_alpha = read_cfg_data(cfg_path_equipment, "蓄能装置", "energy_storage_equipment_alpha", 0)
    energy_storage_equipment_beta = read_cfg_data(cfg_path_equipment, "蓄能装置", "energy_storage_equipment_beta", 0)
    energy_storage_equipment_Few0 = read_cfg_data(cfg_path_equipment, "蓄能装置", "energy_storage_equipment_Few0", 0)
    energy_storage_equipment_SOE_min = read_cfg_data(cfg_path_equipment, "蓄能装置",
                                                     "energy_storage_equipment_SOE_min", 0)
    energy_storage_equipment = Energy_Storage_Equipment(energy_storage_equipment_Q0, energy_storage_equipment_E0,
                                                        energy_storage_equipment_alpha,
                                                        energy_storage_equipment_beta,
                                                        energy_storage_equipment_Few0,
                                                        energy_storage_equipment_SOE_min,
                                                        n_calculate_hour)
    energy_storage_equipment.SOE = 1
    # 实例化冷冻水泵
    storage_chilled_pump_f0 = read_cfg_data(cfg_path_equipment, "一级冷冻水泵_蓄能装置", "chilled_pump_f0", 0)
    storage_chilled_pump_fmax = read_cfg_data(cfg_path_equipment, "一级冷冻水泵_蓄能装置", "chilled_pump_fmax", 0)
    storage_chilled_pump_fmin = read_cfg_data(cfg_path_equipment, "一级冷冻水泵_蓄能装置", "chilled_pump_fmin", 0)
    storage_chilled_pump_Few0 = read_cfg_data(cfg_path_equipment, "一级冷冻水泵_蓄能装置", "chilled_pump_Few0", 0)
    storage_chilled_pump_H0 = read_cfg_data(cfg_path_equipment, "一级冷冻水泵_蓄能装置", "chilled_pump_H0", 0)
    storage_chilled_pump_P0 = read_cfg_data(cfg_path_equipment, "一级冷冻水泵_蓄能装置", "chilled_pump_P0", 0)
    storage_chilled_pump_Rw = read_cfg_data(cfg_path_equipment, "一级冷冻水泵_蓄能装置", "chilled_pump_Rw", 0)
    storage_chilled_pump_f_status = read_cfg_data(cfg_path_equipment, "一级冷冻水泵_蓄能装置",
                                                  "chilled_pump_f_status", 2)
    # 冷冻水泵：向用户侧供冷工况
    chilled_pump_to_user = Water_Pump(chilled_pump_to_user_Fw0_coef, chilled_pump_to_user_H0_coef,
                                      chilled_pump_to_user_P0_coef, storage_chilled_pump_f0,
                                      storage_chilled_pump_fmax,
                                      storage_chilled_pump_fmin, storage_chilled_pump_Few0, storage_chilled_pump_H0,
                                      storage_chilled_pump_P0, storage_chilled_pump_Rw,
                                      storage_chilled_pump_f_status)
    # 冷冻水泵：蓄冷工况
    chilled_pump_in_storage = Water_Pump(chilled_pump_in_storage_Fw0_coef, chilled_pump_in_storage_H0_coef,
                                         chilled_pump_in_storage_P0_coef, storage_chilled_pump_f0,
                                         storage_chilled_pump_fmax, storage_chilled_pump_fmin,
                                         storage_chilled_pump_Few0,
                                         storage_chilled_pump_H0, storage_chilled_pump_P0, storage_chilled_pump_Rw,
                                         storage_chilled_pump_f_status)
    n_storage_chilled_pump = read_cfg_data(cfg_path_equipment, "一级冷冻水泵_蓄能装置", "n_chilled_pump", 1)
    # 保存蓄冷水罐模型文件
    storage_dict = dict()
    storage_dict["H_chilled_pump_to_user"] = H_chilled_pump_to_user
    storage_dict["H_chilled_pump_in_storage"] = H_chilled_pump_in_storage
    storage_dict["energy_storage_equipment"] = energy_storage_equipment
    storage_dict["chilled_pump_to_user"] = chilled_pump_to_user
    storage_dict["chilled_pump_in_storage"] = chilled_pump_in_storage
    storage_dict["n_chilled_valve_in_storage"] = n_chilled_valve_in_storage
    storage_dict["n_chilled_valve_to_user"] = n_chilled_valve_to_user
    storage_dict["n_storage_chilled_pump"] = n_storage_chilled_pump
    with open(file_pkl_storage, "wb") as f:
        pickle.dump(storage_dict, f)

    # 实例化冷却塔直接供冷设备模型
    # 扬程需求值(建议比实际的最小扬程需求值大一点，留余量)
    H_tower_chilled_pump = read_cfg_data(cfg_path_equipment, "水泵扬程需求", "H_tower_chilled_pump", 0)
    # 水泵性能系数
    tower_chilled_pump_Fw0_coef = read_cfg_data(cfg_path_equipment, "一级冷冻水泵_冷却塔直接供冷", "chilled_pump_Fw0_coef", 0)
    tower_chilled_pump_H0_coef = read_cfg_data(cfg_path_equipment, "一级冷冻水泵_冷却塔直接供冷", "chilled_pump_H0_coef", 0)
    tower_chilled_pump_P0_coef = read_cfg_data(cfg_path_equipment, "一级冷冻水泵_冷却塔直接供冷", "chilled_pump_P0_coef", 0)
    # 实例化一级冷冻水泵
    tower_chilled_pump_f0 = read_cfg_data(cfg_path_equipment, "一级冷冻水泵_冷却塔直接供冷", "chilled_pump_f0", 0)
    tower_chilled_pump_fmax = read_cfg_data(cfg_path_equipment, "一级冷冻水泵_冷却塔直接供冷", "chilled_pump_fmax", 0)
    tower_chilled_pump_fmin = read_cfg_data(cfg_path_equipment, "一级冷冻水泵_冷却塔直接供冷", "chilled_pump_fmin", 0)
    tower_chilled_pump_Few0 = read_cfg_data(cfg_path_equipment, "一级冷冻水泵_冷却塔直接供冷", "chilled_pump_Few0", 0)
    tower_chilled_pump_H0 = read_cfg_data(cfg_path_equipment, "一级冷冻水泵_冷却塔直接供冷", "chilled_pump_H0", 0)
    tower_chilled_pump_P0 = read_cfg_data(cfg_path_equipment, "一级冷冻水泵_冷却塔直接供冷", "chilled_pump_P0", 0)
    tower_chilled_pump_Rw = read_cfg_data(cfg_path_equipment, "一级冷冻水泵_冷却塔直接供冷", "chilled_pump_Rw", 0)
    tower_chilled_pump_f_status = read_cfg_data(cfg_path_equipment, "一级冷冻水泵_冷却塔直接供冷",
                                                "chilled_pump_f_status", 2)
    tower_chilled_pump = Water_Pump(tower_chilled_pump_Fw0_coef, tower_chilled_pump_H0_coef, tower_chilled_pump_P0_coef,
                                    tower_chilled_pump_f0, tower_chilled_pump_fmax, tower_chilled_pump_fmin,
                                    tower_chilled_pump_Few0, tower_chilled_pump_H0, tower_chilled_pump_P0,
                                    tower_chilled_pump_Rw, tower_chilled_pump_f_status)
    n_tower_chilled_pump = read_cfg_data(cfg_path_equipment, "一级冷冻水泵_冷却塔直接供冷", "n_chilled_pump", 1)
    n_tower_chilled_valve = 2
    # 保存冷却塔直接供冷模型文件
    tower_chilled_dict = dict()
    tower_chilled_dict["H_tower_chilled_pump"] = H_tower_chilled_pump
    tower_chilled_dict["tower_chilled_pump"] = tower_chilled_pump
    tower_chilled_dict["n_tower_chilled_valve"] = n_tower_chilled_valve
    tower_chilled_dict["n_tower_chilled_pump"] = n_tower_chilled_pump
    with open(file_pkl_tower_chilled, "wb") as f:
        pickle.dump(tower_chilled_dict, f)

    # 储存系统公用参数
    system_dict = dict()
    system_dict["n_calculate_hour"] = n_calculate_hour
    with open(file_pkl_system, "wb") as f:
        pickle.dump(system_dict, f)


if __name__ == "__main__":
    file_pkl_chiller = "./model_data/file_equipment/chiller.pkl"
    file_pkl_ashp = "./model_data/file_equipment/ashp.pkl"
    file_pkl_storage = "./model_data/file_equipment/storage.pkl"
    file_pkl_tower_chilled = "./model_data/file_equipment/tower_chilled.pkl"
    file_pkl_system = "./model_data/file_equipment/system.pkl"
    cfg_path_equipment = "./config/equipment_config.cfg"
    generate_equipment_model(file_pkl_chiller, file_pkl_ashp, file_pkl_storage, file_pkl_tower_chilled,
                             file_pkl_system, cfg_path_equipment)