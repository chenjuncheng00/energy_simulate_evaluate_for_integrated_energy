import numpy as np
from run_chiller import run_chiller
from run_air_source_heat_pump import run_air_source_heat_pump

def run_simulate_evaluate(Q_total):

    print("系统运行...")
    # cfg文件路径
    cfg_path_equipment = "./config/equipment_config.cfg"
    cfg_path_public = "./config/public_config.cfg"
    # 设备类型名称(air_conditioner,air_source_heat_pump等)，相对路径
    chiller_equipment_type_path = ["chiller", "../optimal_control_algorithm_for_cooling_season"]
    ashp_equipment_type_path = ["air_source_heat_pump", "../optimal_control_algorithm_for_cooling_season"]

    # 将Q_total拆分，分别用于冷水机和空气源热泵
    n_optimization = 11
    Q_step = Q_total / (n_optimization - 1)
    chiller_Q_list = []
    air_source_heat_pump_Q_list = []
    for i in range(n_optimization):
        air_source_heat_pump_Q = Q_step * i
        chiller_Q = Q_total - air_source_heat_pump_Q
        air_source_heat_pump_Q_list.append(air_source_heat_pump_Q)
        chiller_Q_list.append(chiller_Q)

    # 优化计算
    P_total_list = []
    Q_total_list = []
    n_calculate_hour = 1
    opt_only = True
    for i in range(n_optimization):
        ans_chiller = run_chiller(chiller_Q_list[i], n_calculate_hour, chiller_equipment_type_path, cfg_path_equipment,
                                  cfg_path_public, opt_only)
        tmp_chiller_P = ans_chiller[0]
        tmp_chiller_Q = ans_chiller[1]
        ans_ashp = run_air_source_heat_pump(air_source_heat_pump_Q_list[i], n_calculate_hour, ashp_equipment_type_path,
                                            cfg_path_equipment, cfg_path_public, opt_only)
        tmp_ashp_P = ans_ashp[0]
        tmp_ashp_Q = ans_ashp[1]
        if tmp_chiller_Q + tmp_ashp_Q >= chiller_Q_list[i] + air_source_heat_pump_Q_list[i]:
            P_total_list.append(tmp_chiller_P + tmp_ashp_P)
            Q_total_list.append(tmp_chiller_Q + tmp_ashp_Q)
        else:
            P_total_list.append(np.inf)
            Q_total_list.append(0)
    # 找出电功率最小值
    min_P_total = min(P_total_list)
    index_min = P_total_list.index(min_P_total)
    best_chiller_Q = chiller_Q_list[index_min]
    best_ashp_Q = air_source_heat_pump_Q_list[index_min]
    print(best_chiller_Q)
    print(best_ashp_Q)

if __name__ == "__main__":
    run_simulate_evaluate(15000)