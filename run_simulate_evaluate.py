import pickle
import numpy as np
from fmpy import *
from model_fmu_output_name import main_model_output_name
from model_fmu_input_type import main_model_input_type
from model_fmu_input_data_default import main_input_data_default
from algorithm_code.optimization_single import *
from algorithm_code.optimization_universal import *
from algorithm_code.algorithm_equipment import *
from algorithm_code.read_write_data import *
from algorithm_code.custom_model import *
from algorithm_code.other import *
from algorithm_code import *
from calculate_energy_storage_value import generate_Q_list, generate_time_name_list

def run_simulate_evaluate():

    # cfg文件路径
    cfg_path_equipment = "./config/equipment_config.cfg"
    cfg_path_public = "./config/public_config.cfg"
    # 设备类型名称(air_conditioner,air_source_heat_pump等)，相对路径
    txt_path = "../optimal_control_algorithm_for_cooling_season"
    chiller_equipment_type_path = ["chiller", txt_path]
    ashp_equipment_type_path = ["air_source_heat_pump", txt_path]
    storage_equipment_type_path = ["energy_storage_equipment", txt_path]
    tower_chilled_equipment_type_path = ["tower_chilled", txt_path]
    # 每小时计算次数
    n_calculate_hour = 1

    # 实例化冷水机系统设备模型
    # 设备数量
    n0_chiller1 = read_cfg_data(cfg_path_equipment, "冷水机1", "n_chiller1", 1)
    n0_chiller2 = read_cfg_data(cfg_path_equipment, "冷水机2", "n_chiller2", 1)
    n0_chiller_chilled_pump1 = read_cfg_data(cfg_path_equipment, "一级冷冻水泵_冷水机1", "n_chilled_pump1", 1)
    n0_chiller_chilled_pump2 = read_cfg_data(cfg_path_equipment, "一级冷冻水泵_冷水机2", "n_chilled_pump2", 1)
    n0_chiller_cooling_pump1 = read_cfg_data(cfg_path_equipment, "冷却水泵_冷水机1", "n_cooling_pump1", 1)
    n0_chiller_cooling_pump2 = read_cfg_data(cfg_path_equipment, "冷却水泵_冷水机2", "n_cooling_pump2", 1)
    n0_chiller_cooling_tower = read_cfg_data(cfg_path_equipment, "冷却塔_冷水机", "n_cooling_tower", 1)
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
    n_chiller_list = [n0_chiller1, n0_chiller2]
    chiller_chilled_pump_list = [chiller_chilled_pump1, chiller_chilled_pump2]
    n_chiller_chilled_pump_list = [n0_chiller_chilled_pump1, n0_chiller_chilled_pump2]
    chiller_cooling_pump_list = [chiller_cooling_pump1, chiller_cooling_pump2]
    n_chiller_cooling_pump_list = [n0_chiller_cooling_pump1, n0_chiller_cooling_pump2]
    chiller_cooling_tower_list = [chiller_cooling_tower]
    n_chiller_cooling_tower_list = [n0_chiller_cooling_tower]
    n_chiller_user_value = 2

    # 实例化空气源热泵系统设备模型
    # n0_air_source_heat_pump = read_cfg_data(cfg_path_equipment, "空气源热泵", "n_air_source_heat_pump", 1)
    # n0_ashp_chilled_pump = read_cfg_data(cfg_path_equipment, "一级冷冻水泵_空气源热泵", "n_chilled_pump", 1)
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
    ashp_chilled_pump_f_status = read_cfg_data(cfg_path_equipment, "一级冷冻水泵_空气源热泵", "chilled_pump_f_status", 2)
    ashp_chilled_pump = Water_Pump(ashp_chilled_pump_Fw0_coef, ashp_chilled_pump_H0_coef, ashp_chilled_pump_P0_coef,
                                   ashp_chilled_pump_f0, ashp_chilled_pump_fmax, ashp_chilled_pump_fmin,
                                   ashp_chilled_pump_Few0, ashp_chilled_pump_H0, ashp_chilled_pump_P0,
                                   ashp_chilled_pump_Rw, ashp_chilled_pump_f_status)

    # 实例化蓄冷水罐系统模型
    # 扬程需求值(建议比实际的最小扬程需求值大一点，留余量)
    H_chilled_pump_to_user = read_cfg_data(cfg_path_equipment, "水泵扬程需求", "H_storage_chilled_pump_to_user", 0)
    H_chilled_pump_in_storage = read_cfg_data(cfg_path_equipment, "水泵扬程需求", "H_storage_chilled_pump_in_storage",
                                              0)
    # 蓄冷阀门个数 AND 放冷阀门个数
    n_chilled_value_in_storage = read_cfg_data(cfg_path_equipment, "蓄冷阀门_蓄能装置", "n_chilled_value", 1)
    n_chilled_value_to_user = read_cfg_data(cfg_path_equipment, "放冷阀门_蓄能装置", "n_chilled_value", 1)
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
    energy_storage_equipment = Energy_Storage_Equipment(energy_storage_equipment_Q0, energy_storage_equipment_E0,
                                                        energy_storage_equipment_alpha, energy_storage_equipment_beta,
                                                        energy_storage_equipment_Few0, n_calculate_hour)
    # 实例化冷冻水泵
    storage_chilled_pump_f0 = read_cfg_data(cfg_path_equipment, "一级冷冻水泵_蓄能装置", "chilled_pump_f0", 0)
    storage_chilled_pump_fmax = read_cfg_data(cfg_path_equipment, "一级冷冻水泵_蓄能装置", "chilled_pump_fmax", 0)
    storage_chilled_pump_fmin = read_cfg_data(cfg_path_equipment, "一级冷冻水泵_蓄能装置", "chilled_pump_fmin", 0)
    storage_chilled_pump_Few0 = read_cfg_data(cfg_path_equipment, "一级冷冻水泵_蓄能装置", "chilled_pump_Few0", 0)
    storage_chilled_pump_H0 = read_cfg_data(cfg_path_equipment, "一级冷冻水泵_蓄能装置", "chilled_pump_H0", 0)
    storage_chilled_pump_P0 = read_cfg_data(cfg_path_equipment, "一级冷冻水泵_蓄能装置", "chilled_pump_P0", 0)
    storage_chilled_pump_Rw = read_cfg_data(cfg_path_equipment, "一级冷冻水泵_蓄能装置", "chilled_pump_Rw", 0)
    storage_chilled_pump_f_status = read_cfg_data(cfg_path_equipment, "一级冷冻水泵_蓄能装置", "chilled_pump_f_status", 2)
    # 冷冻水泵：向用户侧供冷工况
    chilled_pump_to_user = Water_Pump(chilled_pump_to_user_Fw0_coef, chilled_pump_to_user_H0_coef,
                                      chilled_pump_to_user_P0_coef, storage_chilled_pump_f0, storage_chilled_pump_fmax,
                                      storage_chilled_pump_fmin, storage_chilled_pump_Few0, storage_chilled_pump_H0,
                                      storage_chilled_pump_P0, storage_chilled_pump_Rw, storage_chilled_pump_f_status)
    # 冷冻水泵：蓄冷工况
    chilled_pump_in_storage = Water_Pump(chilled_pump_in_storage_Fw0_coef, chilled_pump_in_storage_H0_coef,
                                         chilled_pump_in_storage_P0_coef, storage_chilled_pump_f0,
                                         storage_chilled_pump_fmax, storage_chilled_pump_fmin, storage_chilled_pump_Few0,
                                         storage_chilled_pump_H0, storage_chilled_pump_P0, storage_chilled_pump_Rw,
                                         storage_chilled_pump_f_status)

    # FMU文件
    file_fmu = "./model_data/file_fmu/integrated_air_conditioning_20230522.fmu"
    file_fmu_input_log = "./model_data/simulate_result/fmu_input_log.txt"
    file_fmu_input_feedback_log = "./model_data/simulate_result/fmu_input_feedback_log.txt"
    # FMU仿真参数
    start_time = (31 + 28 + 31 + 30) * 24 * 3600
    stop_time = (31 + 28 + 31 + 30 + 31 + 30 + 31 + 31 + 30 + 31) * 24 * 3600
    output_interval = 10
    time_out = 600
    # 模型初始化和实例化
    fmu_unzipdir = extract(file_fmu)
    fmu_description = read_model_description(fmu_unzipdir)
    fmu_instance = instantiate_fmu(unzipdir=fmu_unzipdir, model_description=fmu_description)
    # 获取内存地址
    file_fmu_address = txt_path + "/process_data/fmu_address.txt"
    unzipdir_address = id(fmu_unzipdir)
    description_address = id(fmu_description)
    instance_address = id(fmu_instance)
    fmu_address_list = [unzipdir_address, description_address, instance_address]
    write_txt_data(file_fmu_address, fmu_address_list)
    # FMU模型仿真时间：仿真开始的时间(start_time)
    file_fmu_time = txt_path + "/process_data/fmu_time.txt"
    write_txt_data(file_fmu_time, [start_time])
    # FMU模型状态：依次为：fmu_initialize, fmu_terminate, stop_time, output_interval, time_out
    file_fmu_state = txt_path + "/process_data/fmu_state.txt"
    fmu_state_list = [1, 0, stop_time, output_interval, time_out]
    write_txt_data(file_fmu_state, fmu_state_list)
    # FMU模型输出名称
    file_fmu_output_name = txt_path + "/process_data/fmu_output_name.pkl"
    fmu_output_name = main_model_output_name()
    with open(file_fmu_output_name, 'wb') as f:
        pickle.dump(fmu_output_name, f)
    # 各系统制冷功率最大值
    chiller_Q0_max = 15600
    ashp_Q0_max = 4092
    Q0_total_in = chiller_Q0_max
    Q0_total_out = chiller_Q0_max + ashp_Q0_max
    # 冷负荷总需求功率
    file_Q_user = "./model_data/simulate_result/fmu_Q_user.txt"
    file_Q_user_list = "./model_data/fmu_Q_user_list.txt"
    Q_time_all_list = read_txt_data(file_Q_user_list, column_index=0)
    Q_user_all_list = read_txt_data(file_Q_user_list, column_index=1)
    write_txt_data(file_Q_user, [Q_user_all_list[0]])
    # 每小时计算次数
    n_simulate = int((stop_time - start_time) / (3600 / n_calculate_hour))
    # 仿真结果
    file_fmu_result_all = "./model_data/simulate_result/fmu_result_all.txt"
    file_fmu_result_last = "./model_data/simulate_result/fmu_result_last.txt"
    txt_str = "start_time" + "\t" + "pause_time"
    for i in range(len(fmu_output_name)):
        txt_str += "\t" + fmu_output_name[i]
    write_txt_data(file_fmu_result_all, [txt_str])
    write_txt_data(file_fmu_result_last, [txt_str])
    # FMU输入名称和数据类型
    input_type_list = main_model_input_type()
    input_data_list = [start_time] + main_input_data_default()
    # 先仿真一次，启动系统
    print("正在初始化FMU模型......")
    hours_init = 1
    main_simulate_pause_single(input_data_list, input_type_list, hours_init * 3600, txt_path, add_input=False)
    # 修改FMU状态
    fmu_state_list = [0, 0, stop_time, output_interval, time_out]
    write_txt_data(file_fmu_state, fmu_state_list)
    # 逐时用电时间段列表，字符串，长度24
    time_name_list = ["谷", "谷", "谷", "谷", "谷", "谷", "谷", "谷", "平", "平", "峰", "峰", "峰", "平", "平", "峰",
                      "峰", "平", "平", "平", "峰", "峰", "峰", "平"]

    for i in range(n_simulate)[hours_init:]:
        print("一共需要计算" + str(n_simulate) + "次，正在进行第" + str(i + 1) + "次计算；已完成" + str(i) + "次计算；已完成" +
              str(np.round(100 * (i + 1) / n_simulate, 4)) + "%")
        # 读取Q_user
        Q_user = read_txt_data(file_Q_user)[0]

        # 第1步：仅进行蓄冷水罐优化计算，获取当前时刻的充放冷功率，不进行控制
        input_log_1 = "第1步：仅进行蓄冷水罐优化计算，获取当前时刻的充放冷功率，不进行控制..."
        print(input_log_1)
        write_txt_data(file_fmu_input_log, [input_log_1, "\n" + "\n"], 1)
        write_txt_data(file_fmu_input_feedback_log, [input_log_1, "\n" + "\n"], 1)
        Q_user_list = generate_Q_list(file_fmu_time, start_time, Q_time_all_list, Q_user_all_list, n_calculate_hour)
        ans_ese = main_optimization_energy_storage_equipment(storage_equipment_type_path, Q_user_list, time_name_list,
                                                             Q0_total_in, Q0_total_out, energy_storage_equipment)
        Q_out_ese = ans_ese[0]
        Q_total = Q_user - Q_out_ese  # 计算Q_total
        print("蓄冷水罐冷负荷功率：" + str(Q_out_ese))

        # 第2步：进行冷水机+蓄冷水罐控制
        if Q_out_ese < 0:
            # 第2-1步：用蓄冷功率优化一次冷水机计算，不进行控制，用于获取阀门开启比例
            input_log_2_1 = "第2-1步：用蓄冷功率优化一次冷水机计算，不进行控制，用于获取阀门开启比例..."
            print(input_log_2_1)
            write_txt_data(file_fmu_input_log, [input_log_2_1, "\n" + "\n"], 1)
            write_txt_data(file_fmu_input_feedback_log, [input_log_2_1, "\n" + "\n"], 1)
            chiller_Q_storage = - Q_out_ese  # 冷水机蓄冷负荷
            ans_chiller1 = optimization_system_universal(chiller_Q_storage, H_chiller_chilled_pump, 0,
                                                         H_chiller_cooling_pump, chiller_list,
                                                         chiller_chilled_pump_list, [], chiller_cooling_pump_list,
                                                         chiller_cooling_tower_list, n_chiller_list,
                                                         n_chiller_chilled_pump_list, [], n_chiller_cooling_pump_list,
                                                         n_chiller_cooling_tower_list, chiller_equipment_type_path,
                                                         cfg_path_public)
            chiller_storage_chilled_value_open = ans_chiller1[0]

            # 第2-2步：用向用户侧供冷功率优化一次冷水机计算，不进行控制，用于获取阀门开启比例
            input_log_2_2 = "第2-2步：用向用户侧供冷功率优化一次冷水机计算，不进行控制，用于获取阀门开启比例..."
            print(input_log_2_2)
            write_txt_data(file_fmu_input_log, [input_log_2_2, "\n" + "\n"], 1)
            write_txt_data(file_fmu_input_feedback_log, [input_log_2_2, "\n" + "\n"], 1)
            chiller_Q_user = min(Q_user, chiller_Q0_max)
            ans_chiller2 = optimization_system_universal(chiller_Q_user, H_chiller_chilled_pump, 0,
                                                         H_chiller_cooling_pump, chiller_list,
                                                         chiller_chilled_pump_list, [], chiller_cooling_pump_list,
                                                         chiller_cooling_tower_list, n_chiller_list,
                                                         n_chiller_chilled_pump_list, [], n_chiller_cooling_pump_list,
                                                         n_chiller_cooling_tower_list, chiller_equipment_type_path,
                                                         cfg_path_public)
            chiller_user_chilled_value_open = ans_chiller2[0]

            # 第2-3步：用向用户侧供冷供冷+蓄冷功率，冷水机优化和控制，但是不进行冷冻水泵控制
            input_log_2_3 = "第2-3步：用向用户侧供冷供冷+蓄冷功率，冷水机优化和控制，但是不进行冷冻水泵控制..."
            print(input_log_2_3)
            write_txt_data(file_fmu_input_log, [input_log_2_3, "\n" + "\n"], 1)
            write_txt_data(file_fmu_input_feedback_log, [input_log_2_3, "\n" + "\n"], 1)
            chiller_Q_total = min(Q_total, chiller_Q0_max)
            algorithm_chiller_double(chiller_Q_total, H_chiller_chilled_pump, 0, H_chiller_cooling_pump, chiller1,
                                     chiller2, chiller_chilled_pump1, chiller_chilled_pump2, None, None,
                                     chiller_cooling_pump1, chiller_cooling_pump2, chiller_cooling_tower, None,
                                     n0_chiller1, n0_chiller2, n0_chiller_chilled_pump1, n0_chiller_chilled_pump2,
                                     0, 0, n0_chiller_cooling_pump1, n0_chiller_cooling_pump2, n0_chiller_cooling_tower,
                                     0, chiller_equipment_type_path, n_calculate_hour, n_chiller_user_value,
                                     cfg_path_equipment, cfg_path_public, chilled_pump_control=False)

            # 第2-4步：用向用户侧供冷功率，冷水机优化和控制，仅进行冷冻水泵控制
            input_log_2_4 = "第2-4步：用向用户侧供冷功率，冷水机优化和控制，仅进行冷冻水泵控制..."
            print(input_log_2_4)
            write_txt_data(file_fmu_input_log, [input_log_2_4, "\n" + "\n"], 1)
            write_txt_data(file_fmu_input_feedback_log, [input_log_2_4, "\n" + "\n"], 1)
            algorithm_chilled_pump(chiller_Q_user, H_chiller_chilled_pump, 0, chiller_user_chilled_value_open,
                                   chiller_chilled_pump_list, [], n_chiller_chilled_pump_list, [],
                                   chiller_equipment_type_path, n_calculate_hour, cfg_path_equipment, cfg_path_public)

            # 第2-5步：蓄冷水罐和水泵优化+控制
            input_log_2_5 = "第2-5步：蓄冷水罐和水泵优化+控制..."
            print(input_log_2_5)
            write_txt_data(file_fmu_input_log, [input_log_2_5, "\n" + "\n"], 1)
            write_txt_data(file_fmu_input_feedback_log, [input_log_2_5, "\n" + "\n"], 1)
            algorithm_energy_storage_equipment(Q_user_list, time_name_list, Q0_total_in, Q0_total_out,
                                               energy_storage_equipment, chilled_pump_to_user, chilled_pump_in_storage,
                                               None, chiller_storage_chilled_value_open, H_chilled_pump_to_user,
                                               H_chilled_pump_in_storage, 0, n_chilled_value_in_storage,
                                               n_chilled_value_to_user, storage_equipment_type_path,
                                               n_calculate_hour, cfg_path_equipment, cfg_path_public)

            # 第2-6步：用向用户侧供冷功率，空气源热泵优化和控制
            input_log_2_6 = "第2-6步：用向用户侧供冷功率，空气源热泵优化和控制..."
            print(input_log_2_6)
            write_txt_data(file_fmu_input_log, [input_log_2_6, "\n" + "\n"], 1)
            write_txt_data(file_fmu_input_feedback_log, [input_log_2_6, "\n" + "\n"], 1)
            ashp_Q_user = min(Q_user - chiller_Q_user, ashp_Q0_max)
            algorithm_air_source_heat_pump(ashp_Q_user, H_ashp_chilled_pump, 0, air_source_heat_pump,
                                           ashp_chilled_pump, None, ashp_equipment_type_path, n_calculate_hour,
                                           0, cfg_path_equipment, cfg_path_public)

        else:
            # 第2-1步：蓄冷水罐和水泵优化+控制，蓄冷工况
            input_log_2_1 = "第2-1步：蓄冷水罐和水泵优化+控制，蓄冷工况..."
            print(input_log_2_1)
            write_txt_data(file_fmu_input_log, [input_log_2_1, "\n" + "\n"], 1)
            write_txt_data(file_fmu_input_feedback_log, [input_log_2_1, "\n" + "\n"], 1)
            algorithm_energy_storage_equipment(Q_user_list, time_name_list, Q0_total_in, Q0_total_out,
                                               energy_storage_equipment, chilled_pump_to_user, chilled_pump_in_storage,
                                               None, None, H_chilled_pump_to_user, H_chilled_pump_in_storage, 0,
                                               n_chilled_value_in_storage, n_chilled_value_to_user,
                                               storage_equipment_type_path, n_calculate_hour, cfg_path_equipment,
                                               cfg_path_public)

            # 第2-2步：用向用户侧供冷供冷，冷水机优化和控制
            input_log_2_2 = "第2-2步：用向用户侧供冷供冷，冷水机优化和控制..."
            print(input_log_2_2)
            write_txt_data(file_fmu_input_log, [input_log_2_2, "\n" + "\n"], 1)
            write_txt_data(file_fmu_input_feedback_log, [input_log_2_2, "\n" + "\n"], 1)
            chiller_Q_user = min(Q_total, chiller_Q0_max)
            algorithm_chiller_double(chiller_Q_user, H_chiller_chilled_pump, 0, H_chiller_cooling_pump, chiller1,
                                     chiller2, chiller_chilled_pump1, chiller_chilled_pump2, None, None,
                                     chiller_cooling_pump1, chiller_cooling_pump2, chiller_cooling_tower, None,
                                     n0_chiller1, n0_chiller2, n0_chiller_chilled_pump1, n0_chiller_chilled_pump2,
                                     0, 0, n0_chiller_cooling_pump1, n0_chiller_cooling_pump2, n0_chiller_cooling_tower,
                                     0, chiller_equipment_type_path, n_calculate_hour, n_chiller_user_value,
                                     cfg_path_equipment, cfg_path_public)

            # 第2-3步：用向用户侧供冷功率，空气源热泵优化和控制
            input_log_2_3 = "第2-3步：用向用户侧供冷功率，空气源热泵优化和控制..."
            print(input_log_2_3)
            write_txt_data(file_fmu_input_log, [input_log_2_3, "\n" + "\n"], 1)
            write_txt_data(file_fmu_input_feedback_log, [input_log_2_3, "\n" + "\n"], 1)
            ashp_Q_user = min(Q_total - chiller_Q_user, ashp_Q0_max)
            algorithm_air_source_heat_pump(ashp_Q_user, H_ashp_chilled_pump, 0, air_source_heat_pump,
                                           ashp_chilled_pump, None, ashp_equipment_type_path, n_calculate_hour,
                                           0, cfg_path_equipment, cfg_path_public)

        # 修改time_list
        time_name_list = generate_time_name_list(time_name_list)
        # 第3步：获取time，并仿真到指定时间
        input_log_3 = "第3步：获取time，并仿真到指定时间..."
        print(input_log_3)
        write_txt_data(file_fmu_input_log, [input_log_3, "\n" + "\n"], 1)
        write_txt_data(file_fmu_input_feedback_log, [input_log_3, "\n" + "\n"], 1)
        time_now = read_txt_data(file_fmu_time)[0]
        n_cal_now = int((time_now - start_time) / (3600 * (1 / n_calculate_hour)))
        simulate_time = start_time + (n_cal_now + 1) * 3600 * (1 / n_calculate_hour) - time_now
        main_simulate_pause_single([], [], simulate_time, txt_path)
        print("\n" + "\n")

    # 修改FMU状态
    fmu_state_list = [0, 1, stop_time, output_interval, time_out]
    write_txt_data(file_fmu_state, fmu_state_list)
    # 最后仿真一次
    main_simulate_pause_single([], [], 3600, txt_path)


if __name__ == "__main__":
    run_simulate_evaluate()