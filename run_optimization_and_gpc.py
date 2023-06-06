import pickle
import numpy as np
from fmpy import *
from model_fmu_output_name import main_model_output_name
from algorithm_code.optimization_single import *
from algorithm_code.optimization_universal import *
from algorithm_code.algorithm_equipment import *
from algorithm_code.read_write_data import *
from algorithm_code.other import *
from algorithm_code import *
from calculate_energy_storage_value import generate_Q_list, generate_time_name_list

def run_optimization_and_gpc():
    """
    冷水机+蓄冷水罐+简单的用户负荷
    搜算优化算法+GPC控制算法
    Returns:

    """
    # cfg文件路径
    cfg_path_equipment = "./config/equipment_config.cfg"
    cfg_path_public = "./config/public_config.cfg"
    # 设备类型名称(air_conditioner,air_source_heat_pump等)，相对路径
    txt_path = "../optimal_control_algorithm_for_cooling_season"
    chiller_equipment_type_path = ["chiller", txt_path]
    storage_equipment_type_path = ["energy_storage_equipment", txt_path]
    # 设备的pkl文件路径
    file_pkl_chiller = "./model_data/file_equipment/chiller.pkl"
    file_pkl_stroage = "./model_data/file_equipment/storage.pkl"
    file_pkl_system = "./model_data/file_equipment/system.pkl"

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
    chiller1 = chiller_dict["chiller1"]
    chiller2 = chiller_dict["chiller2"]
    chiller_chilled_pump1 = chiller_dict["chiller_chilled_pump1"]
    chiller_chilled_pump2 = chiller_dict["chiller_chilled_pump2"]
    chiller_cooling_pump1 = chiller_dict["chiller_cooling_pump1"]
    chiller_cooling_pump2 = chiller_dict["chiller_cooling_pump2"]
    chiller_cooling_tower = chiller_dict["chiller_cooling_tower"]
    n0_chiller1 = chiller_dict["n_chiller1"]
    n0_chiller2 = chiller_dict["n_chiller2"]
    n0_chiller_chilled_pump1 = chiller_dict["n_chiller_chilled_pump1"]
    n0_chiller_chilled_pump2 = chiller_dict["n_chiller_chilled_pump2"]
    n0_chiller_cooling_pump1 = chiller_dict["n_chiller_cooling_pump1"]
    n0_chiller_cooling_pump2 = chiller_dict["n_chiller_cooling_pump2"]
    n0_chiller_cooling_tower = chiller_dict["n_chiller_cooling_tower"]
    n_chiller_user_value = chiller_dict["n_chiller_user_value"]
    # 读取蓄冷水罐设备信息
    with open(file_pkl_stroage, "rb") as f_obj:
        storage_dict = pickle.load(f_obj)
    energy_storage_equipment = storage_dict["energy_storage_equipment"]
    chilled_pump_to_user = storage_dict["chilled_pump_to_user"]
    chilled_pump_in_storage = storage_dict["chilled_pump_in_storage"]
    n_chilled_value_in_storage = storage_dict["n_chilled_value_in_storage"]
    n_chilled_value_to_user = storage_dict["n_chilled_value_to_user"]
    # 读取公共系统信息
    with open(file_pkl_system, "rb") as f_obj:
        system_dict = pickle.load(f_obj)
    n_calculate_hour = system_dict["n_calculate_hour"]

    # FMU文件
    file_fmu = "./model_data/file_fmu/chiller_and_storage_with_simple_load_20230602.fmu"
    file_fmu_input_log = "./model_data/simulate_result/fmu_input_log.txt"
    file_fmu_input_feedback_log = "./model_data/simulate_result/fmu_input_feedback_log.txt"
    # FMU仿真参数
    start_time = 0
    stop_time = 31 * 24 * 3600
    output_interval = 10
    time_out = 600


