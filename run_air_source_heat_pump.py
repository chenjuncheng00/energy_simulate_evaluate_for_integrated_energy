from algorithm_code.custom_model import *
from algorithm_code.read_write_data import *
from algorithm_code.optimization_universal import *
from algorithm_code import *

def run_air_source_heat_pump(Q_total, n_calculate_hour, equipment_type_path, cfg_path_equipment, cfg_path_public,
                             opt_only):
    """

    Args:
        Q_total: [float]，总冷负荷需求量(kW)
        n_calculate_hour:[int]，算法每小时的计算次数
        equipment_type_path:[string]，[list]，设备类型名称(air_conditioner,air_source_heat_pump等)，相对路径
        cfg_path_equipment: [string]，设备信息参数cfg文件路径
        cfg_path_public: [string]，公用参数cfg文件路径
        opt_only: [boolean]，是否仅进行优化计算

    Returns:

    """
    n0_air_source_heat_pump = read_cfg_data(cfg_path_equipment, "空气源热泵", "n_air_source_heat_pump", 1)
    n0_chilled_pump = read_cfg_data(cfg_path_equipment, "冷冻水泵_空气源热泵", "n_chilled_pump", 1)
    # 扬程需求值(建议比实际的最小扬程需求值大一点，留余量)
    H_chilled_pump = read_cfg_data(cfg_path_equipment, "水泵扬程需求", "H_ashp_chilled_pump", 0)
    # 水泵性能系数
    chilled_pump_Fw0_coef = read_cfg_data(cfg_path_equipment, "冷冻水泵_空气源热泵", "chilled_pump_Fw0_coef", 0)
    chilled_pump_H0_coef = read_cfg_data(cfg_path_equipment, "冷冻水泵_空气源热泵", "chilled_pump_H0_coef", 0)
    chilled_pump_P0_coef = read_cfg_data(cfg_path_equipment, "冷冻水泵_空气源热泵", "chilled_pump_P0_coef", 0)
    # 实例化空气源热泵，输出空气源热泵列表
    # 系数依次对应:常数项、负荷率的三次方、负荷率的平方、负荷率的一次方
    air_source_heat_pump_cop_coef = read_cfg_data(cfg_path_equipment, "空气源热泵", "air_source_heat_pump_cop_coef", 0)
    air_source_heat_pump_Q0 = read_cfg_data(cfg_path_equipment, "空气源热泵", "air_source_heat_pump_Q0", 0)
    air_source_heat_pump_alpha = read_cfg_data(cfg_path_equipment, "空气源热泵", "air_source_heat_pump_alpha", 0)
    air_source_heat_pump_beta = read_cfg_data(cfg_path_equipment, "空气源热泵", "air_source_heat_pump_beta", 0)
    air_source_heat_pump_Few0 = read_cfg_data(cfg_path_equipment, "空气源热泵", "air_source_heat_pump_Few0", 0)
    air_source_heat_pump_Rew = read_cfg_data(cfg_path_equipment, "空气源热泵", "air_source_heat_pump_Rew", 0)
    air_source_heat_pump_f_status = read_cfg_data(cfg_path_equipment, "空气源热泵", "air_source_heat_pump_f_status", 2)
    air_source_heat_pump = Electric_Air_Conditioner(air_source_heat_pump_cop_coef, air_source_heat_pump_Q0,
                                                    air_source_heat_pump_alpha, air_source_heat_pump_beta,
                                                    air_source_heat_pump_Few0, air_source_heat_pump_Rew,
                                                    air_source_heat_pump_f_status)
    # 实例化一级冷冻水泵
    chilled_pump_f0 = read_cfg_data(cfg_path_equipment, "冷冻水泵_空气源热泵", "chilled_pump_f0", 0)
    chilled_pump_fmax = read_cfg_data(cfg_path_equipment, "冷冻水泵_空气源热泵", "chilled_pump_fmax", 0)
    chilled_pump_fmin = read_cfg_data(cfg_path_equipment, "冷冻水泵_空气源热泵", "chilled_pump_fmin", 0)
    chilled_pump_Few0 = read_cfg_data(cfg_path_equipment, "冷冻水泵_空气源热泵", "chilled_pump_Few0", 0)
    chilled_pump_H0 = read_cfg_data(cfg_path_equipment, "冷冻水泵_空气源热泵", "chilled_pump_H0", 0)
    chilled_pump_P0 = read_cfg_data(cfg_path_equipment, "冷冻水泵_空气源热泵", "chilled_pump_P0", 0)
    chilled_pump_Rw = read_cfg_data(cfg_path_equipment, "冷冻水泵_空气源热泵", "chilled_pump_Rw", 0)
    chilled_pump_f_status = read_cfg_data(cfg_path_equipment, "冷冻水泵_空气源热泵", "chilled_pump_f_status", 2)
    chilled_pump = Water_Pump(chilled_pump_Fw0_coef, chilled_pump_H0_coef, chilled_pump_P0_coef, chilled_pump_f0,
                              chilled_pump_fmax, chilled_pump_fmin, chilled_pump_Few0, chilled_pump_H0,
                              chilled_pump_P0, chilled_pump_Rw, chilled_pump_f_status)
    # 判断Q_total是否满足要求
    if Q_total < air_source_heat_pump.calculate_Q_min():
        cal_set = False
    elif Q_total > n0_air_source_heat_pump * air_source_heat_pump.calculate_Q_max():
        cal_set = False
    else:
        cal_set = True
    # 仅优化空气源热泵系统的耗电功率
    if opt_only == True and cal_set == True:
        air_source_heat_pump_list = [air_source_heat_pump]
        n_air_source_heat_pump_list = [n0_air_source_heat_pump]
        chilled_pump_list = [chilled_pump]
        n_chilled_pump_list = [n0_chilled_pump]
        ans_opt = optimization_system_universal(Q_total, H_chilled_pump, 0, 0, air_source_heat_pump_list,
                                                chilled_pump_list, [], [], [], n_air_source_heat_pump_list,
                                                n_chilled_pump_list, [], [], [], equipment_type_path, cfg_path_public)
        ans_P_total = ans_opt[0]
        ans_Q_total = ans_opt[1]
    elif opt_only == False and cal_set == True:
        algorithm_air_source_heat_pump(Q_total, H_chilled_pump, 0, air_source_heat_pump, chilled_pump, None,
                                       equipment_type_path, n_calculate_hour, cfg_path_equipment, cfg_path_public)
        ans_P_total = None
        ans_Q_total = None
    else:
        ans_P_total = 0
        ans_Q_total = 0
    # 返回结果
    return ans_P_total, ans_Q_total