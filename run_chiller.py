from algorithm_code.custom_model import *
from algorithm_code.read_write_data import *
from algorithm_code.optimization_universal import *
from algorithm_code import *

def run_chiller(Q_total, n_calculate_hour, equipment_type_path, cfg_path_equipment, cfg_path_public, opt_only):
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
    # 设备数量
    n0_chiller1 = read_cfg_data(cfg_path_equipment, "冷水机1", "n_chiller1", 1)
    n0_chiller2 = read_cfg_data(cfg_path_equipment, "冷水机2", "n_chiller2", 1)
    n0_chilled_pump1 = read_cfg_data(cfg_path_equipment, "一级冷冻水泵_冷水机1", "n_chilled_pump1", 1)
    n0_chilled_pump2 = read_cfg_data(cfg_path_equipment, "一级冷冻水泵_冷水机2", "n_chilled_pump2", 1)
    n0_cooling_pump1 = read_cfg_data(cfg_path_equipment, "冷却水泵_冷水机1", "n_cooling_pump1", 1)
    n0_cooling_pump2 = read_cfg_data(cfg_path_equipment, "冷却水泵_冷水机2", "n_cooling_pump2", 1)
    n0_cooling_tower = read_cfg_data(cfg_path_equipment, "冷却塔_冷水机", "n_cooling_tower", 1)
    # 扬程需求值(建议比实际的最小扬程需求值大一点，留余量)
    H_chilled_pump = read_cfg_data(cfg_path_equipment, "水泵扬程需求", "H_chiller_chilled_pump", 0)
    H_cooling_pump = read_cfg_data(cfg_path_equipment, "水泵扬程需求", "H_chiller_cooling_pump", 0)
    # 水泵1性能系数
    cooling_pump1_Fw0_coef = read_cfg_data(cfg_path_equipment, "冷却水泵_冷水机1", "cooling_pump1_Fw0_coef", 0)
    cooling_pump1_H0_coef = read_cfg_data(cfg_path_equipment, "冷却水泵_冷水机1", "cooling_pump1_H0_coef", 0)
    cooling_pump1_P0_coef = read_cfg_data(cfg_path_equipment, "冷却水泵_冷水机1", "cooling_pump1_P0_coef", 0)
    chilled_pump1_Fw0_coef = read_cfg_data(cfg_path_equipment, "一级冷冻水泵_冷水机1", "chilled_pump1_Fw0_coef", 0)
    chilled_pump1_H0_coef = read_cfg_data(cfg_path_equipment, "一级冷冻水泵_冷水机1", "chilled_pump1_H0_coef", 0)
    chilled_pump1_P0_coef = read_cfg_data(cfg_path_equipment, "一级冷冻水泵_冷水机1", "chilled_pump1_P0_coef", 0)
    # 水泵2性能系数
    cooling_pump2_Fw0_coef = read_cfg_data(cfg_path_equipment, "冷却水泵_冷水机2", "cooling_pump2_Fw0_coef", 0)
    cooling_pump2_H0_coef = read_cfg_data(cfg_path_equipment, "冷却水泵_冷水机2", "cooling_pump2_H0_coef", 0)
    cooling_pump2_P0_coef = read_cfg_data(cfg_path_equipment, "冷却水泵_冷水机2", "cooling_pump2_P0_coef", 0)
    chilled_pump2_Fw0_coef = read_cfg_data(cfg_path_equipment, "一级冷冻水泵_冷水机2", "chilled_pump2_Fw0_coef", 0)
    chilled_pump2_H0_coef = read_cfg_data(cfg_path_equipment, "一级冷冻水泵_冷水机2", "chilled_pump2_H0_coef", 0)
    chilled_pump2_P0_coef = read_cfg_data(cfg_path_equipment, "一级冷冻水泵_冷水机2", "chilled_pump2_P0_coef", 0)
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
    cooling_tower_approach_coef = read_cfg_data(cfg_path_equipment, "冷却塔_冷水机", "cooling_tower_approach_coef", 0)
    # 系数依次对应:常数项、转速比的三次方、转速比的平方、转速比的一次方
    cooling_tower_f0 = read_cfg_data(cfg_path_equipment, "冷却塔_冷水机", "cooling_tower_f0", 0)
    cooling_tower_fmax = read_cfg_data(cfg_path_equipment, "冷却塔_冷水机", "cooling_tower_fmax", 0)
    cooling_tower_fmin = read_cfg_data(cfg_path_equipment, "冷却塔_冷水机", "cooling_tower_fmin", 0)
    cooling_tower_Fcw0 = read_cfg_data(cfg_path_equipment, "冷却塔_冷水机", "cooling_tower_Fcw0", 0)
    cooling_tower_P0 = read_cfg_data(cfg_path_equipment, "冷却塔_冷水机", "cooling_tower_P0", 0)
    cooling_tower_Rcw = read_cfg_data(cfg_path_equipment, "冷却塔_冷水机", "cooling_tower_Rcw", 0)
    cooling_tower_approach_limit = read_cfg_data(cfg_path_equipment, "冷却塔_冷水机",
                                                 "cooling_tower_approach_limit", 0)
    cooling_tower_f_status = read_cfg_data(cfg_path_equipment, "冷却塔_冷水机", "cooling_tower_f_status", 2)
    cooling_tower = Cooling_Tower(cooling_tower_approach_coef, cooling_tower_f0, cooling_tower_fmax,
                                  cooling_tower_fmin, cooling_tower_Fcw0, cooling_tower_P0, cooling_tower_Rcw,
                                  cooling_tower_approach_limit, cooling_tower_f_status)
    # 实例化冷却水泵
    cooling_pump1_f0 = read_cfg_data(cfg_path_equipment, "冷却水泵_冷水机1", "cooling_pump1_f0", 0)
    cooling_pump1_fmax = read_cfg_data(cfg_path_equipment, "冷却水泵_冷水机1", "cooling_pump1_fmax", 0)
    cooling_pump1_fmin = read_cfg_data(cfg_path_equipment, "冷却水泵_冷水机1", "cooling_pump1_fmin", 0)
    cooling_pump1_Fcw0 = read_cfg_data(cfg_path_equipment, "冷却水泵_冷水机1", "cooling_pump1_Fcw0", 0)
    cooling_pump1_H0 = read_cfg_data(cfg_path_equipment, "冷却水泵_冷水机1", "cooling_pump1_H0", 0)
    cooling_pump1_P0 = read_cfg_data(cfg_path_equipment, "冷却水泵_冷水机1", "cooling_pump1_P0", 0)
    cooling_pump1_Rw = read_cfg_data(cfg_path_equipment, "冷却水泵_冷水机1", "cooling_pump1_Rw", 0)
    cooling_pump1_f_status = read_cfg_data(cfg_path_equipment, "冷却水泵_冷水机1", "cooling_pump1_f_status", 2)
    cooling_pump1 = Water_Pump(cooling_pump1_Fw0_coef, cooling_pump1_H0_coef, cooling_pump1_P0_coef,
                               cooling_pump1_f0, cooling_pump1_fmax, cooling_pump1_fmin, cooling_pump1_Fcw0,
                               cooling_pump1_H0, cooling_pump1_P0, cooling_pump1_Rw, cooling_pump1_f_status)
    cooling_pump2_f0 = read_cfg_data(cfg_path_equipment, "冷却水泵_冷水机2", "cooling_pump2_f0", 0)
    cooling_pump2_fmax = read_cfg_data(cfg_path_equipment, "冷却水泵_冷水机2", "cooling_pump2_fmax", 0)
    cooling_pump2_fmin = read_cfg_data(cfg_path_equipment, "冷却水泵_冷水机2", "cooling_pump2_fmin", 0)
    cooling_pump2_Fcw0 = read_cfg_data(cfg_path_equipment, "冷却水泵_冷水机2", "cooling_pump2_Fcw0", 0)
    cooling_pump2_H0 = read_cfg_data(cfg_path_equipment, "冷却水泵_冷水机2", "cooling_pump2_H0", 0)
    cooling_pump2_P0 = read_cfg_data(cfg_path_equipment, "冷却水泵_冷水机2", "cooling_pump2_P0", 0)
    cooling_pump2_Rw = read_cfg_data(cfg_path_equipment, "冷却水泵_冷水机2", "cooling_pump2_Rw", 0)
    cooling_pump2_f_status = read_cfg_data(cfg_path_equipment, "冷却水泵_冷水机2", "cooling_pump2_f_status", 2)
    cooling_pump2 = Water_Pump(cooling_pump2_Fw0_coef, cooling_pump2_H0_coef, cooling_pump2_P0_coef,
                               cooling_pump2_f0, cooling_pump2_fmax, cooling_pump2_fmin, cooling_pump2_Fcw0,
                               cooling_pump2_H0, cooling_pump2_P0, cooling_pump2_Rw, cooling_pump2_f_status)
    # 实例化冷冻水泵
    chilled_pump1_f0 = read_cfg_data(cfg_path_equipment, "一级冷冻水泵_冷水机1", "chilled_pump1_f0", 0)
    chilled_pump1_fmax = read_cfg_data(cfg_path_equipment, "一级冷冻水泵_冷水机1", "chilled_pump1_fmax", 0)
    chilled_pump1_fmin = read_cfg_data(cfg_path_equipment, "一级冷冻水泵_冷水机1", "chilled_pump1_fmin", 0)
    chilled_pump1_Few0 = read_cfg_data(cfg_path_equipment, "一级冷冻水泵_冷水机1", "chilled_pump1_Few0", 0)
    chilled_pump1_H0 = read_cfg_data(cfg_path_equipment, "一级冷冻水泵_冷水机1", "chilled_pump1_H0", 0)
    chilled_pump1_P0 = read_cfg_data(cfg_path_equipment, "一级冷冻水泵_冷水机1", "chilled_pump1_P0", 0)
    chilled_pump1_Rw = read_cfg_data(cfg_path_equipment, "一级冷冻水泵_冷水机1", "chilled_pump1_Rw", 0)
    chilled_pump1_f_status = read_cfg_data(cfg_path_equipment, "一级冷冻水泵_冷水机1", "chilled_pump1_f_status", 2)
    chilled_pump1 = Water_Pump(chilled_pump1_Fw0_coef, chilled_pump1_H0_coef, chilled_pump1_P0_coef,
                               chilled_pump1_f0, chilled_pump1_fmax, chilled_pump1_fmin, chilled_pump1_Few0,
                               chilled_pump1_H0, chilled_pump1_P0, chilled_pump1_Rw, chilled_pump1_f_status)
    chilled_pump2_f0 = read_cfg_data(cfg_path_equipment, "一级冷冻水泵_冷水机2", "chilled_pump2_f0", 0)
    chilled_pump2_fmax = read_cfg_data(cfg_path_equipment, "一级冷冻水泵_冷水机2", "chilled_pump2_fmax", 0)
    chilled_pump2_fmin = read_cfg_data(cfg_path_equipment, "一级冷冻水泵_冷水机2", "chilled_pump2_fmin", 0)
    chilled_pump2_Few0 = read_cfg_data(cfg_path_equipment, "一级冷冻水泵_冷水机2", "chilled_pump2_Few0", 0)
    chilled_pump2_H0 = read_cfg_data(cfg_path_equipment, "一级冷冻水泵_冷水机2", "chilled_pump2_H0", 0)
    chilled_pump2_P0 = read_cfg_data(cfg_path_equipment, "一级冷冻水泵_冷水机2", "chilled_pump2_P0", 0)
    chilled_pump2_Rw = read_cfg_data(cfg_path_equipment, "一级冷冻水泵_冷水机2", "chilled_pump2_Rw", 0)
    chilled_pump2_f_status = read_cfg_data(cfg_path_equipment, "一级冷冻水泵_冷水机2", "chilled_pump2_f_status", 2)
    chilled_pump2 = Water_Pump(chilled_pump2_Fw0_coef, chilled_pump2_H0_coef, chilled_pump2_P0_coef,
                               chilled_pump2_f0, chilled_pump2_fmax, chilled_pump2_fmin, chilled_pump2_Few0,
                               chilled_pump2_H0, chilled_pump2_P0, chilled_pump2_Rw, chilled_pump2_f_status)
    # 仅优化冷水机系统的耗电功率
    if opt_only == True:
        chiller_list = [chiller1, chiller2]
        n_chiller_list = [n0_chiller1, n0_chiller2]
        chilled_pump_list = [chilled_pump1, chilled_pump2]
        n_chilled_pump_list = [n0_chilled_pump1, n0_chilled_pump2]
        cooling_pump_list = [cooling_pump1, cooling_pump2]
        n_cooling_pump_list = [n0_cooling_pump1, n0_cooling_pump2]
        cooling_tower_list = [cooling_tower]
        n_cooling_tower_list = [n0_cooling_tower]
        ans_opt = optimization_system_universal(Q_total, H_chilled_pump, 0, H_cooling_pump, chiller_list,
                                                chilled_pump_list, [], cooling_pump_list, cooling_tower_list,
                                                n_chiller_list, n_chilled_pump_list, [], n_cooling_pump_list,
                                                n_cooling_tower_list, equipment_type_path, cfg_path_public)
        ans_P_total = ans_opt[0]
        ans_Q_total = ans_opt[1]
        chilled_value_open = ans_opt[2]
        cooling_value_open = ans_opt[3]
        tower_value_open = ans_opt[4]
    elif opt_only == False:
        algorithm_chiller_double(Q_total, H_chilled_pump, 0, H_cooling_pump, chiller1,
                                 chiller2, chilled_pump1, chilled_pump2, None,
                                 None, cooling_pump1, cooling_pump2, cooling_tower,
                                 None, n0_chiller1, n0_chiller2, n0_chilled_pump1, n0_chilled_pump2,
                                 0, 0, n0_cooling_pump1,n0_cooling_pump2, n0_cooling_tower, 0, equipment_type_path,
                                 n_calculate_hour, cfg_path_equipment, cfg_path_public)
        ans_P_total = None
        ans_Q_total = None
        chilled_value_open = None
        cooling_value_open = None
        tower_value_open = None
    else:
        ans_P_total = 0
        ans_Q_total = 0
        chilled_value_open = 0
        cooling_value_open = 0
        tower_value_open = 0
    # 返回结果
    return ans_P_total, ans_Q_total, chilled_value_open, cooling_value_open, tower_value_open