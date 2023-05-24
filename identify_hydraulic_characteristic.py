import time, traceback, numpy as np
from algorithm_code.read_write_data import *
from algorithm_code.other import *
from model_fmu_input_type import main_model_input_type
from model_fmu_input_data_default import environment_input_data_default, chiller_input_data_default, \
                                         air_source_heat_pump_input_data_default, cold_storage_input_data_default, \
                                         tower_chilled_input_data_default, user_load_input_data_default, \
                                         main_input_data_default
from model_fmu_output_name import main_model_output_name

def main_identify_hydraulic_characteristic(fmu_unzipdir, fmu_description, start_time, stop_time, output_interval,
                                           time_out, n_cal_f_pump, cfg_path_equipment, chiller_chilled_result_txt_path,
                                           chiller_cooling_result_txt_path, ashp_chilled_result_txt_path,
                                           storage_from_chiller_result_txt_path, storage_to_user_result_txt_path,
                                           chiller_user_storage_result_txt_path, tower_chilled_result_txt_path,
                                           tower_cooling_chilled_result_txt_path, full_open_result_txt_path, pump_f0_cal):
    """
    模型水力特性辨识
    
    Args:
        fmu_unzipdir: [string]，FMU模型解压后的路径
        fmu_description: [object]，获取FMU模型描述
        start_time: [float]，仿真开始时间，单位：秒
        stop_time: [float]，仿真结束时间，单位：秒
        output_interval: [float]，FMU模型输出采样时间，单位：秒
        time_out: [float]，仿真超时时间，单位：秒
        n_cal_f_pump: [int]，水泵转速计算次数
        cfg_path_equipment: [string]，设备信息参数cfg文件路径
        chiller_chilled_result_txt_path: [string]，冷水机冷冻侧水力特性辨识结果，txt文件路径
        chiller_cooling_result_txt_path: [string]，冷水机冷却侧水力特性辨识结果，txt文件路径
        ashp_chilled_result_txt_path: [string]，空气源热泵冷冻侧水力特性辨识结果，txt文件路径
        storage_from_chiller_result_txt_path: [string]，蓄冷水罐蓄冷水力特性辨识结果，txt文件路径
        storage_to_user_result_txt_path: [string]，蓄冷水罐放冷水力特性辨识结果，txt文件路径
        chiller_user_storage_result_txt_path: [string]，冷水机同时向用户侧供冷+向水罐蓄冷水力特性辨识结果，txt文件路径
        tower_chilled_result_txt_path: [string]，冷却塔直接供冷水力特性辨识结果，txt文件路径
        tower_cooling_chilled_result_txt_path: [string]，冷水机冷却侧+冷却塔直接供冷水力特性辨识结果，txt文件路径
        full_open_result_txt_path: [string]，阀门和水泵全开水力特性辨识结果，txt文件路径
        pump_f0_cal: [boolean]，是否仅计算水泵额定转速的数据

    Returns:

    """
    # 设备装机数量，阀门的数量等于主设备数量
    n_chiller1 = read_cfg_data(cfg_path_equipment, "冷水机1", "n_chiller1", 1)
    n_chiller2 = read_cfg_data(cfg_path_equipment, "冷水机2", "n_chiller2", 1)
    n_chiller_chilled_pump1 = read_cfg_data(cfg_path_equipment, "一级冷冻水泵_冷水机1", "n_chilled_pump1", 1)
    n_chiller_chilled_pump2 = read_cfg_data(cfg_path_equipment, "一级冷冻水泵_冷水机2", "n_chilled_pump2", 1)
    n_chiller_cooling_pump1 = read_cfg_data(cfg_path_equipment, "冷却水泵_冷水机1", "n_cooling_pump1", 1)
    n_chiller_cooling_pump2 = read_cfg_data(cfg_path_equipment, "冷却水泵_冷水机2", "n_cooling_pump2", 1)
    n_chiller_cooling_tower = read_cfg_data(cfg_path_equipment, "冷却塔_冷水机", "n_cooling_tower", 1)
    n_air_source_heat_pump = read_cfg_data(cfg_path_equipment, "空气源热泵", "n_air_source_heat_pump", 1)
    n_ashp_chilled_pump = read_cfg_data(cfg_path_equipment, "一级冷冻水泵_空气源热泵", "n_chilled_pump", 1)
    n_storage_chilled_pump = read_cfg_data(cfg_path_equipment, "一级冷冻水泵_蓄能装置", "n_chilled_pump", 1)
    n_tower_chilled_pump = read_cfg_data(cfg_path_equipment, "一级冷冻水泵_冷却塔直接供冷", "n_chilled_pump", 1)
    # 设备额定水流量
    chiller1_Few0 = read_cfg_data(cfg_path_equipment, "冷水机1", "chiller1_Few0", 0)
    chiller2_Few0 = read_cfg_data(cfg_path_equipment, "冷水机2", "chiller2_Few0", 0)
    chiller1_Fcw0 = read_cfg_data(cfg_path_equipment, "冷水机1", "chiller1_Fcw0", 0)
    chiller2_Fcw0 = read_cfg_data(cfg_path_equipment, "冷水机2", "chiller2_Fcw0", 0)
    chiller1_chilled_pump_Fw0 = read_cfg_data(cfg_path_equipment, "一级冷冻水泵_冷水机1", "chilled_pump1_Few0", 0)
    chiller2_chilled_pump_Fw0 = read_cfg_data(cfg_path_equipment, "一级冷冻水泵_冷水机2", "chilled_pump2_Few0", 0)
    chiller1_cooling_pump_Fw0 = read_cfg_data(cfg_path_equipment, "冷却水泵_冷水机1", "cooling_pump1_Fcw0", 0)
    chiller2_cooling_pump_Fw0 = read_cfg_data(cfg_path_equipment, "冷却水泵_冷水机2", "cooling_pump2_Fcw0", 0)
    chiller_cooling_tower_Fcw0 = read_cfg_data(cfg_path_equipment, "冷却塔_冷水机", "cooling_tower_Fcw0", 0)
    air_source_heat_pump_Few0 = read_cfg_data(cfg_path_equipment, "空气源热泵", "air_source_heat_pump_Few0", 0)
    ashp_chilled_pump_Fw0 = read_cfg_data(cfg_path_equipment, "一级冷冻水泵_空气源热泵", "chilled_pump_Few0", 0)
    storage_chilled_pump_Fw0 = read_cfg_data(cfg_path_equipment, "一级冷冻水泵_蓄能装置", "chilled_pump_Few0", 0)
    tower_chilled_pump_Fw0 = read_cfg_data(cfg_path_equipment, "一级冷冻水泵_冷却塔直接供冷", "chilled_pump_Few0", 0)
    # 水泵额定转速
    chiller1_chilled_pump_f0 = read_cfg_data(cfg_path_equipment, "一级冷冻水泵_冷水机1", "chilled_pump1_f0", 0)
    chiller2_chilled_pump_f0 = read_cfg_data(cfg_path_equipment, "一级冷冻水泵_冷水机2", "chilled_pump2_f0", 0)
    chiller1_cooling_pump_f0 = read_cfg_data(cfg_path_equipment, "冷却水泵_冷水机1", "cooling_pump1_f0", 0)
    chiller2_cooling_pump_f0 = read_cfg_data(cfg_path_equipment, "冷却水泵_冷水机2", "cooling_pump2_f0", 0)
    ashp_chilled_pump_f0 = read_cfg_data(cfg_path_equipment, "一级冷冻水泵_空气源热泵", "chilled_pump_f0", 0)
    storage_chilled_pump_f0 = read_cfg_data(cfg_path_equipment, "一级冷冻水泵_蓄能装置", "chilled_pump_f0", 0)
    tower_chilled_pump_f0 = read_cfg_data(cfg_path_equipment, "一级冷冻水泵_冷却塔直接供冷", "chilled_pump_f0", 0)
    # 水泵最小转速
    chiller1_chilled_pump_fmin = read_cfg_data(cfg_path_equipment, "一级冷冻水泵_冷水机1", "chilled_pump1_fmin", 0)
    chiller2_chilled_pump_fmin = read_cfg_data(cfg_path_equipment, "一级冷冻水泵_冷水机2", "chilled_pump2_fmin", 0)
    chiller1_cooling_pump_fmin = read_cfg_data(cfg_path_equipment, "冷却水泵_冷水机1", "cooling_pump1_fmin", 0)
    chiller2_cooling_pump_fmin = read_cfg_data(cfg_path_equipment, "冷却水泵_冷水机2", "cooling_pump2_fmin", 0)
    ashp_chilled_pump_fmin = read_cfg_data(cfg_path_equipment, "一级冷冻水泵_空气源热泵", "chilled_pump_fmin", 0)
    storage_chilled_pump_fmin = read_cfg_data(cfg_path_equipment, "一级冷冻水泵_蓄能装置", "chilled_pump_fmin", 0)
    tower_chilled_pump_fmin = read_cfg_data(cfg_path_equipment, "一级冷冻水泵_冷却塔直接供冷", "chilled_pump_fmin", 0)

    # 水泵转速测试列表，从大到小
    if n_cal_f_pump > 1:
        chiller1_chilled_pump_f_list = []
        chiller2_chilled_pump_f_list = []
        chiller1_cooling_pump_f_list = []
        chiller2_cooling_pump_f_list = []
        ashp_chilled_pump_f_list = []
        storage_chilled_pump_f_list = []
        tower_chilled_pump_f_list = []
        for i in range(n_cal_f_pump):
            chiller1_chilled_pump_f_list.append(chiller1_chilled_pump_f0 - i * (chiller1_chilled_pump_f0 - chiller1_chilled_pump_fmin) / (n_cal_f_pump - 1))
            chiller2_chilled_pump_f_list.append(chiller2_chilled_pump_f0 - i * (chiller2_chilled_pump_f0 - chiller2_chilled_pump_fmin) / (n_cal_f_pump - 1))
            chiller1_cooling_pump_f_list.append(chiller1_cooling_pump_f0 - i * (chiller1_cooling_pump_f0 - chiller1_cooling_pump_fmin) / (n_cal_f_pump - 1))
            chiller2_cooling_pump_f_list.append(chiller2_cooling_pump_f0 - i * (chiller2_cooling_pump_f0 - chiller2_cooling_pump_fmin) / (n_cal_f_pump - 1))
            ashp_chilled_pump_f_list.append(ashp_chilled_pump_f0 - i * (ashp_chilled_pump_f0 - ashp_chilled_pump_fmin) / (n_cal_f_pump - 1))
            storage_chilled_pump_f_list.append(storage_chilled_pump_f0 - i * (storage_chilled_pump_f0 - storage_chilled_pump_fmin) / (n_cal_f_pump - 1))
            tower_chilled_pump_f_list.append(tower_chilled_pump_f0 - i * (tower_chilled_pump_f0 - tower_chilled_pump_fmin) / (n_cal_f_pump - 1))
    else:
        chiller1_chilled_pump_f_list = [chiller1_chilled_pump_f0]
        chiller2_chilled_pump_f_list = [chiller2_chilled_pump_f0]
        chiller1_cooling_pump_f_list = [chiller1_cooling_pump_f0]
        chiller2_cooling_pump_f_list = [chiller2_cooling_pump_f0]
        ashp_chilled_pump_f_list = [ashp_chilled_pump_f0]
        storage_chilled_pump_f_list = [storage_chilled_pump_f0]
        tower_chilled_pump_f_list = [tower_chilled_pump_f0]

    # 与水力特性辨识无关的模型输入，给定值
    time_data = [start_time]
    chiller_data = [False, False, False, False, False, False, 8]
    chiller_cooling_tower_data = [0, 0, 0, 0, 0, 0]
    air_source_heat_pump_data = [False, False, False, False, 8]
    # 模型输入名称和类型
    model_input_type = main_model_input_type()
    # 模型输出名称
    model_output_name = main_model_output_name()

    # 冷水机模型，冷冻水，水力特性测试
    identify_chiller_chilled_side(n_chiller1, n_chiller2, n_chiller_chilled_pump1, n_chiller_chilled_pump2,
                                  chiller1_Few0, chiller2_Few0, chiller1_chilled_pump_Fw0, chiller2_chilled_pump_Fw0,
                                  chiller1_chilled_pump_f_list, chiller2_chilled_pump_f_list, time_data, chiller_data,
                                  chiller_cooling_tower_data, fmu_unzipdir, fmu_description, start_time, stop_time,
                                  time_out, model_input_type, model_output_name, output_interval,
                                  chiller_chilled_result_txt_path, pump_f0_cal)
    # 冷水机模型，冷却水，水力特性测试
    identify_chiller_cooling_side(n_chiller1, n_chiller2, n_chiller_cooling_pump1, n_chiller_cooling_pump2,
                                  n_chiller_cooling_tower, chiller1_Fcw0, chiller2_Fcw0, chiller_cooling_tower_Fcw0,
                                  chiller1_cooling_pump_Fw0,  chiller2_cooling_pump_Fw0, chiller1_cooling_pump_f_list,
                                  chiller2_cooling_pump_f_list, time_data, chiller_data, chiller_cooling_tower_data,
                                  fmu_unzipdir, fmu_description, start_time, stop_time, time_out, model_input_type,
                                  model_output_name, output_interval, chiller_cooling_result_txt_path, pump_f0_cal)
    # 空气源热泵模型，冷冻水，水力特性测试
    identify_air_source_heat_pump_chilled_side(n_air_source_heat_pump, n_ashp_chilled_pump, air_source_heat_pump_Few0,
                                               ashp_chilled_pump_Fw0, ashp_chilled_pump_f_list, time_data,
                                               air_source_heat_pump_data, fmu_unzipdir, fmu_description, start_time,
                                               stop_time, time_out, model_input_type, model_output_name,
                                               output_interval, ashp_chilled_result_txt_path, pump_f0_cal)
    # 蓄冷水罐模型，蓄冷工况，水力特性测试
    identify_cold_storage_from_chiller(n_chiller1, n_chiller2, n_storage_chilled_pump, chiller1_Few0, chiller2_Few0,
                                       storage_chilled_pump_Fw0, storage_chilled_pump_f_list, time_data, chiller_data,
                                       chiller_cooling_tower_data, fmu_unzipdir, fmu_description, start_time,
                                       stop_time, time_out, model_input_type, model_output_name, output_interval,
                                       storage_from_chiller_result_txt_path, pump_f0_cal)
    # 蓄冷水罐模型，放冷工况，水力特性测试
    identify_cold_storage_to_user(n_storage_chilled_pump, storage_chilled_pump_f_list, time_data, fmu_unzipdir,
                                  fmu_description, start_time, stop_time, time_out, model_input_type,
                                  model_output_name, output_interval, storage_to_user_result_txt_path, pump_f0_cal)
    # 冷水机+蓄冷水罐模型，冷水机同时向用户侧供冷+向水罐蓄冷，水力特性辨识
    identify_chiller_user_storage(n_chiller1, n_chiller2, n_chiller_chilled_pump1, n_chiller_chilled_pump2,
                                  chiller1_Few0, chiller2_Few0, chiller1_chilled_pump_Fw0, chiller2_chilled_pump_Fw0,
                                  chiller1_chilled_pump_f_list, chiller2_chilled_pump_f_list, n_storage_chilled_pump,
                                  storage_chilled_pump_Fw0, storage_chilled_pump_f_list, time_data, chiller_data,
                                  chiller_cooling_tower_data, fmu_unzipdir, fmu_description, start_time, stop_time,
                                  time_out, model_input_type, model_output_name, output_interval,
                                  chiller_user_storage_result_txt_path, pump_f0_cal)
    # 冷却塔直接供冷模型，水力特性测试
    identify_tower_chilled(n_chiller_cooling_tower, n_tower_chilled_pump, chiller_cooling_tower_Fcw0,
                           tower_chilled_pump_Fw0, tower_chilled_pump_f_list, time_data, chiller_data,
                           chiller_cooling_tower_data, fmu_unzipdir, fmu_description, start_time, stop_time,
                           time_out, model_input_type, model_output_name, output_interval,
                           tower_chilled_result_txt_path, pump_f0_cal)
    # 冷水机冷却侧+冷却塔直接供冷模型，水力特性测试
    identify_tower_cooling_chilled(n_chiller1, n_chiller2, n_chiller_cooling_pump1, n_chiller_cooling_pump2,
                                   n_chiller_cooling_tower, chiller1_Fcw0, chiller2_Fcw0, chiller_cooling_tower_Fcw0,
                                   chiller1_cooling_pump_Fw0, chiller2_cooling_pump_Fw0, chiller1_cooling_pump_f_list,
                                   chiller2_cooling_pump_f_list, n_tower_chilled_pump, tower_chilled_pump_Fw0,
                                   tower_chilled_pump_f_list, time_data, chiller_data, chiller_cooling_tower_data,
                                   fmu_unzipdir, fmu_description, start_time, stop_time, time_out, model_input_type,
                                   model_output_name, output_interval, tower_cooling_chilled_result_txt_path,
                                   pump_f0_cal)
    # 阀门和水泵全开，水力特性测试
    identify_full_open(n_chiller1, n_chiller2, n_chiller_chilled_pump1, n_chiller_chilled_pump2,
                       chiller1_chilled_pump_Fw0, chiller2_chilled_pump_Fw0, chiller1_chilled_pump_f0,
                       chiller2_chilled_pump_f0, n_chiller_cooling_pump1, n_chiller_cooling_pump2,
                       chiller1_cooling_pump_Fw0, chiller2_cooling_pump_Fw0, chiller1_cooling_pump_f0,
                       chiller2_cooling_pump_f0, n_ashp_chilled_pump, ashp_chilled_pump_Fw0, ashp_chilled_pump_f0,
                       n_storage_chilled_pump, storage_chilled_pump_Fw0, storage_chilled_pump_f0,
                       n_tower_chilled_pump, tower_chilled_pump_Fw0, tower_chilled_pump_f0, time_data, chiller_data,
                       chiller_cooling_tower_data, air_source_heat_pump_data, fmu_unzipdir, fmu_description,
                       start_time, stop_time, time_out, model_input_type, model_output_name, output_interval,
                       full_open_result_txt_path)


def identify_chiller_chilled_side(n_chiller1, n_chiller2, n_chiller_chilled_pump1, n_chiller_chilled_pump2,
                                  chiller1_Few0, chiller2_Few0, chiller1_chilled_pump_Fw0, chiller2_chilled_pump_Fw0,
                                  chiller1_chilled_pump_f_list, chiller2_chilled_pump_f_list, time_data, chiller_data,
                                  chiller_cooling_tower_data, fmu_unzipdir, fmu_description, start_time, stop_time,
                                  time_out, model_input_type, model_output_name, output_interval,
                                  chiller_chilled_result_txt_path, pump_f0_cal):
    """
    冷水机模型，冷冻水，水力特性测试
    Args:
        n_chiller1: [int]，大冷水机装机台数
        n_chiller2: [int]，小冷水机装机台数
        n_chiller_chilled_pump1: [int]，大冷冻水泵装机台数
        n_chiller_chilled_pump2: [int]，小冷冻水泵装机台数
        chiller1_Few0: [float]，大冷水机额定冷冻水流量
        chiller2_Few0: [float]，小冷水机额定冷冻水流量
        chiller1_chilled_pump_Fw0: [float]，大冷冻水泵额定冷冻水流量
        chiller2_chilled_pump_Fw0: [float]，小冷冻水泵额定冷冻水流量
        chiller1_chilled_pump_f_list: [list，float]，大冷冻水泵需要辨识的转速，列表
        chiller2_chilled_pump_f_list: [list，float]，小冷冻水泵需要辨识的转速，列表
        time_data: [list]，模型输入数据，时间
        chiller_data: [list]，模型输入数据，冷水机开关及出水温度温度设定
        chiller_cooling_tower_data: [list]，模型输入数据，冷却塔风机转速比
        fmu_unzipdir: [string]，FMU模型解压后的路径
        fmu_description: [object]，获取FMU模型描述
        start_time: [float]，仿真开始时间，单位：秒
        stop_time: [float]，仿真结束时间，单位：秒
        time_out: [float]，仿真超时时间，单位：秒
        model_input_type: [list]，模型输入名称和数据类型
        model_output_name: [list]，模型输出名称
        output_interval: [float]，FMU模型输出采样时间，单位：秒
        chiller_chilled_result_txt_path: [string]，仿真结果保存txt文件路径
        pump_f0_cal: [boolean]，是否仅计算水泵额定转速的数据

    Returns:

    """
    # 冷水机模型，冷冻水，水力特性测试
    chiller_chilled_result_list = []
    chiller_chilled_result_list.append("冷水机模型，冷冻侧管道，水力特性辨识：")
    chiller_chilled_result_list.append("大冷冻阀门开启数量" + "\t" + "小冷冻阀门开启数量" + "\t" +
                                       "大冷冻水泵开启数量" + "\t" + "小冷冻水泵开启数量" + "\t" +
                                       "大冷冻水泵开启转速" + "\t" + "小冷冻水泵开启转速" + "\t" +
                                       "大冷水机单台水流量" + "\t" + "小冷水机单台水流量" + "\t" +
                                       "大冷冻水泵单台水流量" + "\t" + "小冷冻水泵单台水流量" + "\t" +
                                       "大冷冻水泵单台电功率" + "\t" + "小冷冻水泵单台电功率" + "\t" +
                                       "冷冻水泵扬程")
    # 默认值
    chiller_cooling_pump_data = [0, 0, 0, 0, 0, 0]
    chiller_cooling_value_data = [0, 0, 0, 0, 0, 0]
    chiller_tower_value_data = [0, 0, 0, 0, 0, 0]
    chiller_tower_chilled_value_data = [0, 0]
    chiller_user_value_data = [1, 1]
    for i in range(n_chiller1 + 1):
        for j in range(n_chiller2 + 1):
            for k in range(n_chiller_chilled_pump1 + 1):
                for l in range(n_chiller_chilled_pump2 + 1):
                    if i + j == 0:
                        continue
                    if k + l == 0:
                        continue
                    n_cal_f = 0
                    for m in range(len(chiller1_chilled_pump_f_list)):
                        if n_cal_f > 0 and pump_f0_cal == True:
                            continue
                        pump1_f = chiller1_chilled_pump_f_list[m]
                        pump2_f = chiller2_chilled_pump_f_list[m]
                        chiller_Few0_total = i * chiller1_Few0 + j * chiller2_Few0
                        pump_Fw0_total = k * chiller1_chilled_pump_Fw0 * (pump1_f / chiller1_chilled_pump_f_list[0]) + \
                                         l * chiller2_chilled_pump_Fw0 * (pump2_f / chiller2_chilled_pump_f_list[0])
                        if pump_Fw0_total >= 2 * chiller_Few0_total:
                            continue
                        if pump_Fw0_total <= 0.2 * chiller_Few0_total:
                            continue
                        chiller_chilled_value_data = []
                        chiller_chilled_pump_data = []
                        print("正在进行 冷水机模型 冷冻侧 水力特性辨识：" + "大冷冻阀门开启数量：" + str(i) +
                              "，小冷冻阀门开启数量" + str(j) + "，大冷冻水泵开启数量" + str(k) +
                              "，小冷冻水泵开启数量" + str(l) + "，大冷冻水泵转速" + str(pump1_f) +
                              "，小冷冻水泵转速" + str(pump2_f))
                        # 阀门和水泵输入数值
                        for ii in range(n_chiller1 + 1)[1:]:
                            if ii <= i:
                                chiller_chilled_value_data.append(1)
                            else:
                                chiller_chilled_value_data.append(0)
                        for jj in range(n_chiller2 + 1)[1:]:
                            if jj <= j:
                                chiller_chilled_value_data.append(1)
                            else:
                                chiller_chilled_value_data.append(0)
                        for kk in range(n_chiller_chilled_pump1 + 1)[1:]:
                            if kk <= k:
                                chiller_chilled_pump_data.append(pump1_f)
                            else:
                                chiller_chilled_pump_data.append(0)
                        for ll in range(n_chiller_chilled_pump2 + 1)[1:]:
                            if ll <= l:
                                chiller_chilled_pump_data.append(pump2_f)
                            else:
                                chiller_chilled_pump_data.append(0)
                        # 整个模型输入数值
                        model_input_data = time_data + environment_input_data_default() + chiller_data + \
                                           chiller_chilled_pump_data + chiller_cooling_pump_data + \
                                           chiller_cooling_tower_data + chiller_chilled_value_data + \
                                           chiller_cooling_value_data + chiller_tower_value_data + \
                                           chiller_tower_chilled_value_data + chiller_user_value_data + \
                                           air_source_heat_pump_input_data_default() + \
                                           cold_storage_input_data_default() + tower_chilled_input_data_default() + \
                                           user_load_input_data_default()
                        # FMU仿真
                        try:
                            time1 = time.time()
                            result = simulate_sample(fmu_unzipdir, fmu_description, None, start_time, stop_time,
                                                     model_input_data, model_input_type, model_output_name,
                                                     output_interval, time_out, False, False)
                            # 获取仿真结果
                            # 冷水机组总流量=水泵组总流量
                            Few_total = result['chiller_Few_total'][-1]
                            # 冷水机组流量
                            chiller_Few_big_total = result['chiller_Few_big'][-1]
                            chiller_Few_small_total = result['chiller_Few_small'][-1]
                            # 水泵组流量
                            chilled_pump_Few_small_total = result['chiller_Few_chilled_pump_small'][-1]
                            chilled_pump_Few_big_total = Few_total - chilled_pump_Few_small_total
                            chilled_pump_H = result['chiller_H_chilled_pump'][-1]
                            chilled_pump_P_big_total = result['chiller_P_big_chilled_pump'][-1]
                            chilled_pump_P_small_total = result['chiller_P_small_chilled_pump'][-1]
                            # 单台冷水机的数据
                            if i == 0:
                                chiller_Few_big = 0
                            else:
                                chiller_Few_big = chiller_Few_big_total / i
                            if j == 0:
                                chiller_Few_small = 0
                            else:
                                chiller_Few_small = chiller_Few_small_total / j
                            # 单台水泵的数据
                            if k == 0:
                                chilled_pump_Few_big = 0
                                chilled_pump_P_big = 0
                            else:
                                chilled_pump_Few_big = chilled_pump_Few_big_total / k
                                chilled_pump_P_big = chilled_pump_P_big_total / k
                            if l == 0:
                                chilled_pump_Few_small = 0
                                chilled_pump_P_small = 0
                            else:
                                chilled_pump_Few_small = chilled_pump_Few_small_total / l
                                chilled_pump_P_small = chilled_pump_P_small_total / l
                            # 如果水泵频率不是50Hz，则用相似率换算数据
                            if n_cal_f == 0 and pump1_f < chiller1_chilled_pump_f_list[0] and \
                                    pump2_f < chiller2_chilled_pump_f_list[0]:
                                chilled_pump_Few_big = chilled_pump_Few_big * (chiller1_chilled_pump_f_list[0] / pump1_f)
                                chilled_pump_Few_small = chilled_pump_Few_small * (chiller2_chilled_pump_f_list[0] / pump2_f)
                                chiller_Few_big = chiller_Few_big * (chiller1_chilled_pump_f_list[0] / pump1_f)
                                chiller_Few_small = chiller_Few_small * (chiller2_chilled_pump_f_list[0] / pump2_f)
                                chilled_pump_H = chilled_pump_H * ((chiller1_chilled_pump_f_list[0] / pump1_f) ** 2)
                                chilled_pump_P_big = chilled_pump_P_big * ((chiller1_chilled_pump_f_list[0] / pump1_f) ** 3)
                                chilled_pump_P_small = chilled_pump_P_small * ((chiller2_chilled_pump_f_list[0] / pump2_f) ** 3)
                                pump1_f = chiller1_chilled_pump_f_list[0]
                                pump2_f = chiller2_chilled_pump_f_list[0]
                            # 仿真结果生成txt
                            tmp_txt = str(i) + "\t" + str(j) + "\t" + str(k) + "\t" + str(l) + "\t" + \
                                      str(pump1_f) + "\t" + str(pump2_f) + "\t" + \
                                      str(np.round(chiller_Few_big, 2)) + "\t" + \
                                      str(np.round(chiller_Few_small, 2)) + "\t" + \
                                      str(np.round(chilled_pump_Few_big, 2)) + "\t" + \
                                      str(np.round(chilled_pump_Few_small, 2)) + "\t" + \
                                      str(np.round(chilled_pump_P_big, 2)) + "\t" + \
                                      str(np.round(chilled_pump_P_small, 2)) + "\t" + \
                                      str(np.round(chilled_pump_H, 2))
                            chiller_chilled_result_list.append(tmp_txt)
                            time2 = time.time()
                            time_cost = np.round(time2 - time1, 2)
                            print("本次仿真计算用时(秒)：" + str(time_cost) + "\n")
                            n_cal_f += 1
                        except:
                            print("FMU仿真失败：" + "大冷冻阀门开启数量：" + str(i) + "，小冷冻阀门开启数量" + str(j) +
                                  "，大冷冻水泵开启数量" + str(k) + "，小冷冻水泵开启数量" + str(l))
                            print(traceback.format_exc() + "\n")
                            pass
    # 结果写入txt
    write_txt_data(chiller_chilled_result_txt_path, chiller_chilled_result_list)


def identify_chiller_cooling_side(n_chiller1, n_chiller2, n_chiller_cooling_pump1, n_chiller_cooling_pump2,
                                  n_chiller_cooling_tower, chiller1_Fcw0, chiller2_Fcw0, chiller_cooling_tower_Fcw0,
                                  chiller1_cooling_pump_Fw0,  chiller2_cooling_pump_Fw0, chiller1_cooling_pump_f_list,
                                  chiller2_cooling_pump_f_list, time_data, chiller_data, chiller_cooling_tower_data,
                                  fmu_unzipdir, fmu_description, start_time, stop_time, time_out, model_input_type,
                                  model_output_name, output_interval, chiller_cooling_result_txt_path, pump_f0_cal):
    """
    冷水机模型，冷却水，水力特性测试
    Args:
        n_chiller1: [int]，大冷水机装机台数
        n_chiller2: [int]，小冷水机装机台数
        n_chiller_cooling_pump1: [int]，大冷却水泵装机台数
        n_chiller_cooling_pump2: [int]，小冷却水泵装机台数
        n_chiller_cooling_tower: [int]，冷却塔装机台数
        chiller1_Fcw0: [float]，大冷水机额定冷却水流量
        chiller2_Fcw0: [float]，小冷水机额定冷却水流量
        chiller_cooling_tower_Fcw0: [float]，冷却塔额定冷却水流量
        chiller1_cooling_pump_Fw0: [float]，大冷却水泵额定冷却水流量
        chiller2_cooling_pump_Fw0: [float]，小冷却水泵额定冷却水流量
        chiller1_cooling_pump_f_list: [list，float]，大冷却水泵需要辨识的转速，列表
        chiller2_cooling_pump_f_list: [list，float]，小冷却水泵需要辨识的转速，列表
        time_data: [list]，模型输入数据，时间
        chiller_data: [list]，模型输入数据，冷水机开关及出水温度温度设定
        chiller_cooling_tower_data: [list]，模型输入数据，冷却塔风机转速比
        fmu_unzipdir: [string]，FMU模型解压后的路径
        fmu_description: [object]，获取FMU模型描述
        start_time: [float]，仿真开始时间，单位：秒
        stop_time: [float]，仿真结束时间，单位：秒
        time_out: [float]，仿真超时时间，单位：秒
        model_input_type: [list]，模型输入名称和数据类型
        model_output_name: [list]，模型输出名称
        output_interval: [float]，FMU模型输出采样时间，单位：秒
        chiller_cooling_result_txt_path: [string]，仿真结果保存txt文件路径
        pump_f0_cal: [boolean]，是否仅计算水泵额定转速的数据

    Returns:

    """
    # 冷水机模型，冷却水，水力特性测试
    chiller_cooling_result_list = []
    chiller_cooling_result_list.append("冷水机模型，冷却侧管道，水力特性辨识：")
    chiller_cooling_result_list.append("大冷却阀门开启数量" + "\t" + "小冷却阀门开启数量" + "\t" + "冷却塔阀门开启数量" + "\t" +
                                       "大冷却水泵开启数量" + "\t" + "小冷却水泵开启数量" + "\t" +
                                       "大冷却水泵开启转速" + "\t" + "小冷却水泵开启转速" + "\t" +
                                       "大冷水机单台水流量" + "\t" + "小冷水机单台水流量" + "\t" +
                                       "大冷却水泵单台水流量" + "\t" + "小冷却水泵单台水流量" + "\t" +
                                       "大冷却水泵单台电功率" + "\t" + "小冷却水泵单台电功率" + "\t" + "冷却水泵扬程")
    # 默认值
    chiller_chilled_pump_data = [0, 0, 0, 0, 0, 0]
    chiller_chilled_value_data = [0, 0, 0, 0, 0, 0]
    chiller_tower_chilled_value_data = [0, 0]
    chiller_user_value_data = [0, 0]
    for i in range(n_chiller1 + 1):
        for j in range(n_chiller2 + 1):
            for k in range(n_chiller_cooling_tower + 1):
                for l in range(n_chiller_cooling_pump1 + 1):
                    for m in range(n_chiller_cooling_pump2 + 1):
                        if i + j == 0:
                            continue
                        if k == 0:
                            continue
                        if l + m == 0:
                            continue
                        n_cal_f = 0
                        for n in range(len(chiller1_cooling_pump_f_list)):
                            if n_cal_f > 0 and pump_f0_cal == True:
                                continue
                            pump1_f = chiller1_cooling_pump_f_list[n]
                            pump2_f = chiller2_cooling_pump_f_list[n]
                            chiller_Fcw0_total = i * chiller1_Fcw0 + j * chiller2_Fcw0
                            tower_Fcw0_total = k * chiller_cooling_tower_Fcw0
                            pump_Fw0_total = l * chiller1_cooling_pump_Fw0 * (pump1_f / chiller1_cooling_pump_f_list[0]) + \
                                             m * chiller2_cooling_pump_Fw0 * (pump2_f / chiller2_cooling_pump_f_list[0])
                            if pump_Fw0_total >= 2 * chiller_Fcw0_total:
                                continue
                            if pump_Fw0_total <= 0.2 * chiller_Fcw0_total:
                                continue
                            if pump_Fw0_total >= 2 * tower_Fcw0_total:
                                continue
                            chiller_cooling_value_data = []
                            chiller_tower_value_data = []
                            chiller_cooling_pump_data = []
                            print("正在进行 冷水机模型 冷却侧 水力特性辨识：" + "大冷却阀门开启数量：" + str(i) +
                                  "，小冷却阀门开启数量" + str(j) + "，冷却塔阀门开启数量" + str(k) +
                                  "，大冷却水泵开启数量" + str(l) + "，小冷却水泵开启数量" + str(m) +
                                  "，大冷却水泵转速" + str(pump1_f) + "，小冷却水泵转速" + str(pump2_f))
                            # 阀门和水泵输入数值
                            for ii in range(n_chiller1 + 1)[1:]:
                                if ii <= i:
                                    chiller_cooling_value_data.append(1)
                                else:
                                    chiller_cooling_value_data.append(0)
                            for jj in range(n_chiller2 + 1)[1:]:
                                if jj <= j:
                                    chiller_cooling_value_data.append(1)
                                else:
                                    chiller_cooling_value_data.append(0)
                            for kk in range(n_chiller_cooling_tower + 1)[1:]:
                                if kk <= k:
                                    chiller_tower_value_data.append(1)
                                else:
                                    chiller_tower_value_data.append(0)
                            for ll in range(n_chiller_cooling_pump1 + 1)[1:]:
                                if ll <= l:
                                    chiller_cooling_pump_data.append(pump1_f)
                                else:
                                    chiller_cooling_pump_data.append(0)
                            for mm in range(n_chiller_cooling_pump2 + 1)[1:]:
                                if mm <= m:
                                    chiller_cooling_pump_data.append(pump2_f)
                                else:
                                    chiller_cooling_pump_data.append(0)
                            # 整个模型输入数值
                            model_input_data = time_data + environment_input_data_default() + chiller_data + \
                                               chiller_chilled_pump_data + chiller_cooling_pump_data + \
                                               chiller_cooling_tower_data + chiller_chilled_value_data + \
                                               chiller_cooling_value_data + chiller_tower_value_data + \
                                               chiller_tower_chilled_value_data + chiller_user_value_data + \
                                               air_source_heat_pump_input_data_default() + \
                                               cold_storage_input_data_default() + \
                                               tower_chilled_input_data_default() + user_load_input_data_default()
                            # FMU仿真
                            try:
                                time1 = time.time()
                                result = simulate_sample(fmu_unzipdir, fmu_description, None, start_time, stop_time,
                                                         model_input_data, model_input_type, model_output_name,
                                                         output_interval, time_out, False, False)
                                # 获取仿真结果
                                # 冷水机组总流量=水泵组总流量
                                Fcw_total = result['chiller_Fcw_total'][-1]
                                # 冷水机组流量
                                chiller_Fcw_big_total = result['chiller_Fcw_big'][-1]
                                chiller_Fcw_small_total = result['chiller_Fcw_small'][-1]
                                # 水泵组流量
                                cooling_pump_Fcw_small_total = result['chiller_Fcw_cooling_pump_small'][-1]
                                cooling_pump_Fcw_big_total = Fcw_total - cooling_pump_Fcw_small_total
                                cooling_pump_H = result['chiller_H_cooling_pump'][-1]
                                cooling_pump_P_big_total = result['chiller_P_big_cooling_pump'][-1]
                                cooling_pump_P_small_total = result['chiller_P_small_cooling_pump'][-1]
                                # 单台冷水机的数据
                                if i == 0:
                                    chiller_Fcw_big = 0
                                else:
                                    chiller_Fcw_big = chiller_Fcw_big_total / i
                                if j == 0:
                                    chiller_Fcw_small = 0
                                else:
                                    chiller_Fcw_small = chiller_Fcw_small_total / j
                                # 单台水泵的数据
                                if l == 0:
                                    cooling_pump_Fcw_big = 0
                                    cooling_pump_P_big = 0
                                else:
                                    cooling_pump_Fcw_big = cooling_pump_Fcw_big_total / l
                                    cooling_pump_P_big = cooling_pump_P_big_total / l
                                if m == 0:
                                    cooling_pump_Fcw_small = 0
                                    cooling_pump_P_small = 0
                                else:
                                    cooling_pump_Fcw_small = cooling_pump_Fcw_small_total / m
                                    cooling_pump_P_small = cooling_pump_P_small_total / m
                                # 如果水泵频率不是50Hz，则用相似率换算数据
                                if n_cal_f == 0 and pump1_f < chiller1_cooling_pump_f_list[0] and \
                                        pump2_f < chiller2_cooling_pump_f_list[0]:
                                    cooling_pump_Fcw_big = cooling_pump_Fcw_big * (chiller1_cooling_pump_f_list[0] / pump1_f)
                                    cooling_pump_Fcw_small = cooling_pump_Fcw_small * (chiller2_cooling_pump_f_list[0] / pump2_f)
                                    chiller_Fcw_big = chiller_Fcw_big * (chiller1_cooling_pump_f_list[0] / pump1_f)
                                    chiller_Fcw_small = chiller_Fcw_small * (chiller2_cooling_pump_f_list[0] / pump2_f)
                                    cooling_pump_H = cooling_pump_H * ((chiller1_cooling_pump_f_list[0] / pump1_f) ** 2)
                                    cooling_pump_P_big = cooling_pump_P_big * ((chiller1_cooling_pump_f_list[0] / pump1_f) ** 3)
                                    cooling_pump_P_small = cooling_pump_P_small * ((chiller2_cooling_pump_f_list[0] / pump2_f) ** 3)
                                    pump1_f = chiller1_cooling_pump_f_list[0]
                                    pump2_f = chiller2_cooling_pump_f_list[0]
                                # 仿真结果生成txt
                                tmp_txt = str(i) + "\t" + str(j) + "\t" + str(k) + "\t" + str(l) + "\t" + \
                                          str(m) + "\t" + str(pump1_f) + "\t" + str(pump2_f) + "\t" + \
                                          str(np.round(chiller_Fcw_big, 2)) + "\t" + \
                                          str(np.round(chiller_Fcw_small, 2)) + "\t" + \
                                          str(np.round(cooling_pump_Fcw_big, 2)) + "\t" + \
                                          str(np.round(cooling_pump_Fcw_small, 2)) + "\t" + \
                                          str(np.round(cooling_pump_P_big, 2)) + "\t" + \
                                          str(np.round(cooling_pump_P_small, 2)) + "\t" + \
                                          str(np.round(cooling_pump_H, 2))
                                chiller_cooling_result_list.append(tmp_txt)
                                time2 = time.time()
                                time_cost = np.round(time2 - time1, 2)
                                print("本次仿真计算用时(秒)：" + str(time_cost) + "\n")
                                n_cal_f += 1
                            except:
                                print("FMU仿真失败：" + "大冷却阀门开启数量：" + str(i) + "，小冷却阀门开启数量" + str(j) +
                                      "，冷却塔阀门开启数量" + str(k) + "，大冷却水泵开启数量" + str(l) +
                                      "，小冷却水泵开启数量" + str(m))
                                print(traceback.format_exc() + "\n")
                                pass
    # 结果写入txt
    write_txt_data(chiller_cooling_result_txt_path, chiller_cooling_result_list)


def identify_air_source_heat_pump_chilled_side(n_air_source_heat_pump, n_ashp_chilled_pump, air_source_heat_pump_Few0,
                                               ashp_chilled_pump_Fw0, ashp_chilled_pump_f_list, time_data,
                                               air_source_heat_pump_data, fmu_unzipdir, fmu_description, start_time,
                                               stop_time, time_out, model_input_type, model_output_name,
                                               output_interval, ashp_chilled_result_txt_path, pump_f0_cal):
    """
    空气源热泵模型，冷冻水，水力特性测试
    Args:
        n_air_source_heat_pump: [int]，空气源热泵装机台数
        n_ashp_chilled_pump: [int]，冷冻水泵装机台数
        air_source_heat_pump_Few0: [float]，空气源热泵额定冷冻水流量
        ashp_chilled_pump_Fw0: [float]，冷冻水泵额定冷冻水流量
        ashp_chilled_pump_f_list: [list，float]，冷冻水泵需要辨识的转速，列表
        time_data: [list]，模型输入数据，时间
        air_source_heat_pump_data: [list]，模型输入数据，空气源热泵开关及出水温度温度设定
        fmu_unzipdir: [string]，FMU模型解压后的路径
        fmu_description: [object]，获取FMU模型描述
        start_time: [float]，仿真开始时间，单位：秒
        stop_time: [float]，仿真结束时间，单位：秒
        time_out: [float]，仿真超时时间，单位：秒
        model_input_type: [list]，模型输入名称和数据类型
        model_output_name: [list]，模型输出名称
        output_interval: [float]，FMU模型输出采样时间，单位：秒
        ashp_chilled_result_txt_path: [string]，仿真结果保存txt文件路径
        pump_f0_cal: [boolean]，是否仅计算水泵额定转速的数据

    Returns:

    """
    # 空气源热泵模型，冷冻水，水力特性测试
    ashp_chilled_result_list = []
    ashp_chilled_result_list.append("空气源热泵模型，冷冻侧管道，水力特性辨识：")
    ashp_chilled_result_list.append("冷冻阀门开启数量" + "\t" + "冷冻水泵开启数量" + "\t" + "冷冻水泵转速" + "\t" 
                                    "冷冻水泵单台水流量" + "\t" + "冷冻水泵单台电功率" + "\t" + "冷冻水泵扬程")
    for i in range(n_air_source_heat_pump + 1):
        for j in range(n_ashp_chilled_pump + 1):
            if i == 0 or j == 0:
                continue
            n_cal_f = 0
            for k in range(len(ashp_chilled_pump_f_list)):
                if n_cal_f > 0 and pump_f0_cal == True:
                    continue
                pump_f = ashp_chilled_pump_f_list[k]
                ashp_Few0_total = i * air_source_heat_pump_Few0
                pump_Fw0_total = j * ashp_chilled_pump_Fw0 * (pump_f / ashp_chilled_pump_f_list[0])
                if pump_Fw0_total >= 2 * ashp_Few0_total:
                    continue
                if pump_Fw0_total <= 0.2 * ashp_Few0_total:
                    continue
                ashp_chilled_value_data = []
                ashp_chilled_pump_data = []
                print("正在进行 空气源热泵模型 冷冻侧 水力特性辨识：" + "冷冻阀门开启数量：" + str(i) +
                      "，冷冻水泵开启数量" + str(j) + "，冷冻水泵转速" + str(pump_f))
                # 阀门和水泵输入数值
                for ii in range(n_air_source_heat_pump + 1)[1:]:
                    if ii <= i:
                        ashp_chilled_value_data.append(1)
                    else:
                        ashp_chilled_value_data.append(0)
                for jj in range(n_ashp_chilled_pump + 1)[1:]:
                    if jj <= j:
                        ashp_chilled_pump_data.append(pump_f)
                    else:
                        ashp_chilled_pump_data.append(0)
                # 整个模型输入数值
                model_input_data = time_data + environment_input_data_default() + chiller_input_data_default() + \
                                   air_source_heat_pump_data + ashp_chilled_pump_data + ashp_chilled_value_data + \
                                   cold_storage_input_data_default() + tower_chilled_input_data_default() + \
                                   user_load_input_data_default()
                # FMU仿真
                try:
                    time1 = time.time()
                    result = simulate_sample(fmu_unzipdir, fmu_description, None, start_time, stop_time,
                                             model_input_data, model_input_type, model_output_name, output_interval,
                                             time_out, False, False)
                    # 获取仿真结果
                    Few_total = result['ashp_Few_total'][-1]  # 空调机组总流量=水泵组总流量
                    chilled_pump_H = result['ashp_H_chilled_pump'][-1]
                    chilled_pump_P_total = result['ashp_P_total_chilled_pump'][-1]
                    # 单台水泵的数据
                    if j == 0:
                        chilled_pump_Few = 0
                        chilled_pump_P = 0
                    else:
                        chilled_pump_Few = Few_total / j
                        chilled_pump_P = chilled_pump_P_total / j
                    # 如果水泵频率不是50Hz，则用相似率换算数据
                    if n_cal_f == 0 and pump_f < ashp_chilled_pump_f_list[0]:
                        chilled_pump_Few = chilled_pump_Few * (ashp_chilled_pump_f_list[0] / pump_f)
                        chilled_pump_H = chilled_pump_H * ((ashp_chilled_pump_f_list[0] / pump_f) ** 2)
                        chilled_pump_P = chilled_pump_P * ((ashp_chilled_pump_f_list[0] / pump_f) ** 3)
                        pump_f = ashp_chilled_pump_f_list[0]
                    # 仿真结果生成txt
                    tmp_txt = str(i) + "\t" + str(j) + "\t" + str(pump_f) + "\t" + \
                              str(np.round(chilled_pump_Few, 2)) + "\t" + \
                              str(np.round(chilled_pump_P, 2)) + "\t" + str(np.round(chilled_pump_H, 2))
                    ashp_chilled_result_list.append(tmp_txt)
                    time2 = time.time()
                    time_cost = np.round(time2 - time1, 2)
                    print("本次仿真计算用时(秒)：" + str(time_cost) + "\n")
                    n_cal_f += 1
                except:
                    print("FMU仿真失败：" + "冷冻阀门开启数量：" + str(i) + "，冷冻水泵开启数量" + str(j))
                    print(traceback.format_exc() + "\n")
                    pass
    # 结果写入txt
    write_txt_data(ashp_chilled_result_txt_path, ashp_chilled_result_list)


def identify_cold_storage_from_chiller(n_chiller1, n_chiller2, n_storage_chilled_pump, chiller1_Few0, chiller2_Few0,
                                       storage_chilled_pump_Fw0, storage_chilled_pump_f_list, time_data, chiller_data,
                                       chiller_cooling_tower_data, fmu_unzipdir, fmu_description, start_time,
                                       stop_time, time_out, model_input_type, model_output_name, output_interval,
                                       storage_from_chiller_result_txt_path, pump_f0_cal):
    """
    蓄冷水罐模型，蓄冷工况，水力特性测试
    Args:
        n_chiller1: [int]，大冷水机装机台数
        n_chiller2: [int]，小冷水机装机台数
        n_storage_chilled_pump: [int]，冷冻水泵装机台数
        chiller1_Few0: [float]，大冷水机额定冷冻水流量
        chiller2_Few0: [float]，小冷水机额定冷冻水流量
        storage_chilled_pump_Fw0: [float]，冷冻水泵额定冷冻水流量
        storage_chilled_pump_f_list: [list，float]，冷冻水泵需要辨识的转速，列表
        time_data: [list]，模型输入数据，时间
        chiller_data: [list]，模型输入数据，冷水机开关及出水温度温度设定
        chiller_cooling_tower_data: [list]，模型输入数据，冷却塔风机转速比
        fmu_unzipdir: [string]，FMU模型解压后的路径
        fmu_description: [object]，获取FMU模型描述
        start_time: [float]，仿真开始时间，单位：秒
        stop_time: [float]，仿真结束时间，单位：秒
        time_out: [float]，仿真超时时间，单位：秒
        model_input_type: [list]，模型输入名称和数据类型
        model_output_name: [list]，模型输出名称
        output_interval: [float]，FMU模型输出采样时间，单位：秒
        storage_from_chiller_result_txt_path: [string]，仿真结果保存txt文件路径
        pump_f0_cal: [boolean]，是否仅计算水泵额定转速的数据

    Returns:

    """
    # 蓄冷水罐模型，蓄冷工况，水力特性测试
    storage_from_chiller_result_list = []
    storage_from_chiller_result_list.append("蓄冷水罐模型，蓄冷工况，水力特性辨识：")
    storage_from_chiller_result_list.append("冷水机大冷冻阀门开启数量" + "\t" + "冷水机小冷冻阀门开启数量" + "\t" +
                                            "蓄冷水罐冷冻水泵开启数量" + "\t" + "蓄冷水罐冷冻水泵转速" + "\t" +
                                            "大冷水机单台水流量" + "\t" + "小冷水机单台水流量" + "\t" +
                                            "蓄冷水罐冷冻水泵单台水流量" + "\t" + "蓄冷水罐冷冻水泵单台电功率" + "\t" +
                                            "蓄冷水罐冷冻水泵扬程")
    # 默认值
    chiller_chilled_pump_data = [0, 0, 0, 0, 0, 0]
    chiller_cooling_pump_data = [0, 0, 0, 0, 0, 0]
    chiller_cooling_value_data = [0, 0, 0, 0, 0, 0]
    chiller_tower_value_data = [0, 0, 0, 0, 0, 0]
    chiller_tower_chilled_value_data = [0, 0]
    chiller_user_value_data = [0, 0]
    # 阀门列表：先是蓄冷阀门，然后是放冷阀门
    storage_chiller_value_data = [1, 1, 1]
    storage_user_value_data = [0, 0, 0]
    for i in range(n_chiller1 + 1):
        for j in range(n_chiller2 + 1):
            for k in range(n_storage_chilled_pump + 1):
                if i + j == 0:
                    continue
                if k == 0:
                    continue
                n_cal_f = 0
                for l in range(len(storage_chilled_pump_f_list)):
                    if n_cal_f > 0 and pump_f0_cal == True:
                        continue
                    pump_f = storage_chilled_pump_f_list[l]
                    chiller_Few0_total = i * chiller1_Few0 + j * chiller2_Few0
                    pump_Fw0_total = k * storage_chilled_pump_Fw0 * (pump_f / storage_chilled_pump_f_list[0])
                    if pump_Fw0_total >= 2 * chiller_Few0_total:
                        continue
                    if pump_Fw0_total <= 0.2 * chiller_Few0_total:
                        continue
                    chiller_chilled_value_data = []
                    storage_chilled_pump_data = []
                    print("正在进行 蓄冷水罐模型 蓄冷工况 水力特性辨识：" + "冷水机大冷冻阀门开启数量：" + str(i) +
                          "，冷水机小冷冻阀门开启数量" + str(j) + "，蓄冷水罐冷冻水泵开启数量" + str(k) +
                          "，蓄冷水罐冷冻水泵转速" + str(pump_f))
                    # 阀门和水泵输入数值
                    for ii in range(n_chiller1 + 1)[1:]:
                        if ii <= i:
                            chiller_chilled_value_data.append(1)
                        else:
                            chiller_chilled_value_data.append(0)
                    for jj in range(n_chiller2 + 1)[1:]:
                        if jj <= j:
                            chiller_chilled_value_data.append(1)
                        else:
                            chiller_chilled_value_data.append(0)
                    for kk in range(n_storage_chilled_pump + 1)[1:]:
                        if kk <= k:
                            storage_chilled_pump_data.append(pump_f)
                        else:
                            storage_chilled_pump_data.append(0)
                    # 整个模型输入数值
                    model_input_data = time_data + environment_input_data_default() + chiller_data + \
                                       chiller_chilled_pump_data + chiller_cooling_pump_data + \
                                       chiller_cooling_tower_data + chiller_chilled_value_data + \
                                       chiller_cooling_value_data + chiller_tower_value_data + \
                                       chiller_tower_chilled_value_data + chiller_user_value_data + \
                                       air_source_heat_pump_input_data_default() + storage_chilled_pump_data + \
                                       storage_chiller_value_data + storage_user_value_data + \
                                       tower_chilled_input_data_default() + user_load_input_data_default()
                    # FMU仿真
                    try:
                        time1 = time.time()
                        result = simulate_sample(fmu_unzipdir, fmu_description, None, start_time, stop_time,
                                                 model_input_data, model_input_type, model_output_name,
                                                 output_interval, time_out, False, False)
                        # 获取仿真结果
                        # 冷水机组流量
                        chiller_Few_big_total = result['chiller_Few_big'][-1]
                        chiller_Few_small_total = result['chiller_Few_small'][-1]
                        # 蓄冷水泵数据
                        Few_total_from_chiller = result['storage_Few_total_from_chiller'][-1]
                        chilled_pump_H = result['storage_H_chilled_pump'][-1]
                        chilled_pump_P_total = result['storage_P_total_chilled_pump'][-1]
                        # 单台冷水机的数据
                        if i == 0:
                            chiller_Few_big = 0
                        else:
                            chiller_Few_big = chiller_Few_big_total / i
                        if j == 0:
                            chiller_Few_small = 0
                        else:
                            chiller_Few_small = chiller_Few_small_total / j
                        # 单台水泵的数据
                        if k == 0:
                            chilled_pump_Few = 0
                            chilled_pump_P = 0
                        else:
                            chilled_pump_Few = Few_total_from_chiller / k
                            chilled_pump_P = chilled_pump_P_total / k
                        # 如果水泵频率不是50Hz，则用相似率换算数据
                        if n_cal_f == 0 and pump_f < storage_chilled_pump_f_list[0]:
                            chiller_Few_big = chiller_Few_big * (storage_chilled_pump_f_list[0] / pump_f)
                            chiller_Few_small = chiller_Few_small * (storage_chilled_pump_f_list[0] / pump_f)
                            chilled_pump_Few = chilled_pump_Few * (storage_chilled_pump_f_list[0] / pump_f)
                            chilled_pump_H = chilled_pump_H * ((storage_chilled_pump_f_list[0] / pump_f) ** 2)
                            chilled_pump_P = chilled_pump_P * ((storage_chilled_pump_f_list[0] / pump_f) ** 3)
                            pump_f = storage_chilled_pump_f_list[0]
                        # 仿真结果生成txt
                        tmp_txt = str(i) + "\t" + str(j) + "\t" + str(k) + "\t" + str(pump_f) + "\t" + \
                                  str(np.round(chiller_Few_big, 2)) + "\t" + \
                                  str(np.round(chiller_Few_small, 2)) + "\t" + \
                                  str(np.round(chilled_pump_Few, 2)) + "\t" + \
                                  str(np.round(chilled_pump_P, 2)) + "\t" + \
                                  str(np.round(chilled_pump_H, 2))
                        storage_from_chiller_result_list.append(tmp_txt)
                        time2 = time.time()
                        time_cost = np.round(time2 - time1, 2)
                        print("本次仿真计算用时(秒)：" + str(time_cost) + "\n")
                        n_cal_f += 1
                    except:
                        print("FMU仿真失败：" + "冷水机大冷冻阀门开启数量：" + str(i) + "，冷水机小冷冻阀门开启数量" + str(j) +
                              "，蓄冷水罐冷冻水泵开启数量" + str(k))
                        print(traceback.format_exc() + "\n")
                        pass
    # 结果写入txt
    write_txt_data(storage_from_chiller_result_txt_path, storage_from_chiller_result_list)


def identify_cold_storage_to_user(n_storage_chilled_pump, storage_chilled_pump_f_list, time_data, fmu_unzipdir,
                                  fmu_description, start_time, stop_time, time_out, model_input_type,
                                  model_output_name, output_interval, storage_to_user_result_txt_path, pump_f0_cal):
    """
    蓄冷水罐模型，放冷工况，水力特性测试
    Args:
        n_storage_chilled_pump: [int]，冷冻水泵装机台数
        storage_chilled_pump_f_list: [list，float]，冷冻水泵需要辨识的转速，列表
        time_data: [list]，模型输入数据，时间
        fmu_unzipdir: [string]，FMU模型解压后的路径
        fmu_description: [object]，获取FMU模型描述
        start_time: [float]，仿真开始时间，单位：秒
        stop_time: [float]，仿真结束时间，单位：秒
        time_out: [float]，仿真超时时间，单位：秒
        model_input_type: [list]，模型输入名称和数据类型
        model_output_name: [list]，模型输出名称
        output_interval: [float]，FMU模型输出采样时间，单位：秒
        storage_to_user_result_txt_path: [string]，仿真结果保存txt文件路径
        pump_f0_cal: [boolean]，是否仅计算水泵额定转速的数据

    Returns:

    """
    # 蓄冷水罐模型，放冷工况，水力特性测试
    storage_to_user_result_list = []
    storage_to_user_result_list.append("蓄冷水罐模型，放冷工况，水力特性辨识：")
    storage_to_user_result_list.append("蓄冷水罐冷冻水泵开启数量" + "\t" + "蓄冷水罐冷冻水泵转速" + "\t" +
                                       "蓄冷水罐冷冻水泵单台水流量" + "\t" + "蓄冷水罐冷冻水泵单台电功率" + "\t" +
                                       "蓄冷水罐冷冻水泵扬程")
    # 阀门列表：先是蓄冷阀门，然后是放冷阀门
    storage_chiller_value_data = [0, 0, 0]
    storage_user_value_data = [1, 1, 1]
    for i in range(n_storage_chilled_pump + 1):
        if i == 0:
            continue
        n_cal_f = 0
        for j in range(len(storage_chilled_pump_f_list)):
            if n_cal_f > 0 and pump_f0_cal == True:
                continue
            storage_chilled_pump_data = []
            pump_f = storage_chilled_pump_f_list[j]
            print("正在进行 蓄冷水罐模型 放冷工况 水力特性辨识：" + "，蓄冷水罐冷冻水泵开启数量" + str(i) +
                  "，蓄冷水罐冷冻水泵转速" + str(pump_f))
            # 阀门和水泵输入数值
            for ii in range(n_storage_chilled_pump + 1)[1:]:
                if ii <= i:
                    storage_chilled_pump_data.append(pump_f)
                else:
                    storage_chilled_pump_data.append(0)
            # 整个模型输入数值
            model_input_data = time_data + environment_input_data_default() + chiller_input_data_default() + \
                               air_source_heat_pump_input_data_default() + storage_chilled_pump_data + \
                               storage_chiller_value_data + storage_user_value_data + \
                               tower_chilled_input_data_default() + user_load_input_data_default()
            # FMU仿真
            try:
                time1 = time.time()
                result = simulate_sample(fmu_unzipdir, fmu_description, None, start_time, stop_time, model_input_data,
                                         model_input_type, model_output_name, output_interval, time_out, False, False)
                # 获取仿真结果
                Few_total_to_user = result['storage_Few_total_to_user'][-1]
                chilled_pump_H = result['storage_H_chilled_pump'][-1]
                chilled_pump_P_total = result['storage_P_total_chilled_pump'][-1]
                # 单台水泵的数据
                if i == 0:
                    chilled_pump_Few = 0
                    chilled_pump_P = 0
                else:
                    chilled_pump_Few = Few_total_to_user / i
                    chilled_pump_P = chilled_pump_P_total / i
                # 如果水泵频率不是50Hz，则用相似率换算数据
                if n_cal_f == 0 and pump_f < storage_chilled_pump_f_list[0]:
                    chilled_pump_Few = chilled_pump_Few * (storage_chilled_pump_f_list[0] / pump_f)
                    chilled_pump_H = chilled_pump_H * ((storage_chilled_pump_f_list[0] / pump_f) ** 2)
                    chilled_pump_P = chilled_pump_P * ((storage_chilled_pump_f_list[0] / pump_f) ** 3)
                    pump_f = storage_chilled_pump_f_list[0]
                # 仿真结果生成txt
                tmp_txt = str(i) + "\t" + str(pump_f) + "\t" + str(np.round(chilled_pump_Few, 2)) + "\t" + \
                          str(np.round(chilled_pump_P, 2)) + "\t" + str(np.round(chilled_pump_H, 2))
                storage_to_user_result_list.append(tmp_txt)
                time2 = time.time()
                time_cost = np.round(time2 - time1, 2)
                print("本次仿真计算用时(秒)：" + str(time_cost) + "\n")
                n_cal_f += 1
            except:
                print("FMU仿真失败：" + "，蓄冷水罐冷冻水泵开启数量" + str(i))
                print(traceback.format_exc() + "\n")
                pass
    # 结果写入txt
    write_txt_data(storage_to_user_result_txt_path, storage_to_user_result_list)


def identify_chiller_user_storage(n_chiller1, n_chiller2, n_chiller_chilled_pump1, n_chiller_chilled_pump2,
                                  chiller1_Few0, chiller2_Few0, chiller1_chilled_pump_Fw0, chiller2_chilled_pump_Fw0,
                                  chiller1_chilled_pump_f_list, chiller2_chilled_pump_f_list, n_storage_chilled_pump,
                                  storage_chilled_pump_Fw0, storage_chilled_pump_f_list, time_data, chiller_data,
                                  chiller_cooling_tower_data, fmu_unzipdir, fmu_description, start_time, stop_time,
                                  time_out, model_input_type, model_output_name, output_interval,
                                  chiller_user_storage_result_txt_path, pump_f0_cal):
    """
    冷水机同时向用户侧供冷+向水罐蓄冷，水力特性测试
    Args:
        n_chiller1: [int]，大冷水机装机台数
        n_chiller2: [int]，小冷水机装机台数
        n_chiller_chilled_pump1: [int]，大冷冻水泵装机台数
        n_chiller_chilled_pump2: [int]，小冷冻水泵装机台数
        chiller1_Few0: [float]，大冷水机额定冷冻水流量
        chiller2_Few0: [float]，小冷水机额定冷冻水流量
        chiller1_chilled_pump_Fw0: [float]，大冷冻水泵额定冷冻水流量
        chiller2_chilled_pump_Fw0: [float]，小冷冻水泵额定冷冻水流量
        chiller1_chilled_pump_f_list: [list，float]，大冷冻水泵需要辨识的转速，列表
        chiller2_chilled_pump_f_list: [list，float]，小冷冻水泵需要辨识的转速，列表
        n_storage_chilled_pump: [int]，冷冻水泵装机台数
        storage_chilled_pump_Fw0: [float]，冷冻水泵额定冷冻水流量
        storage_chilled_pump_f_list: [list，float]，冷冻水泵需要辨识的转速，列表
        time_data: [list]，模型输入数据，时间
        chiller_data: [list]，模型输入数据，冷水机开关及出水温度温度设定
        chiller_cooling_tower_data: [list]，模型输入数据，冷却塔风机转速比
        fmu_unzipdir: [string]，FMU模型解压后的路径
        fmu_description: [object]，获取FMU模型描述
        start_time: [float]，仿真开始时间，单位：秒
        stop_time: [float]，仿真结束时间，单位：秒
        time_out: [float]，仿真超时时间，单位：秒
        model_input_type: [list]，模型输入名称和数据类型
        model_output_name: [list]，模型输出名称
        output_interval: [float]，FMU模型输出采样时间，单位：秒
        chiller_user_storage_result_txt_path: [string]，仿真结果保存txt文件路径
        pump_f0_cal: [boolean]，是否仅计算水泵额定转速的数据

    Returns:

    """
    chiller_user_storage_result_list = []
    chiller_user_storage_result_list.append("冷水机+蓄冷水罐模型，冷水机同时向用户侧供冷+向水罐蓄冷，水力特性辨识：")
    chiller_user_storage_result_list.append("冷水机大冷冻阀门开启数量" + "\t" + "冷水机小冷冻阀门开启数量" + "\t" +
                                            "冷水机大冷冻水泵开启数量" + "\t" + "冷水机小冷冻水泵开启数量" + "\t" +
                                            "冷水机大冷冻水泵开启转速" + "\t" + "冷水机小冷冻水泵开启转速" + "\t" +
                                            "大冷水机单台水流量" + "\t" + "小冷水机单台水流量" + "\t" +
                                            "冷水机大冷冻水泵单台水流量" + "\t" + "冷水机小冷冻水泵单台水流量" + "\t" +
                                            "冷水机大冷冻水泵单台电功率" + "\t" + "冷水机小冷冻水泵单台电功率" + "\t" +
                                            "冷水机冷冻水泵扬程" + "\t" + "蓄冷水罐冷冻水泵开启数量" + "\t" +
                                            "蓄冷水罐冷冻水泵转速" + "\t" + "蓄冷水罐冷冻水泵单台水流量" + "\t" +
                                            "蓄冷水罐冷冻水泵单台电功率" + "\t" + "蓄冷水罐冷冻水泵扬程")
    # 默认值
    chiller_cooling_pump_data = [0, 0, 0, 0, 0, 0]
    chiller_cooling_value_data = [0, 0, 0, 0, 0, 0]
    chiller_tower_value_data = [0, 0, 0, 0, 0, 0]
    chiller_tower_chilled_value_data = [0, 0]
    chiller_user_value_data = [1, 1]
    storage_chiller_value_data = [1, 1, 1]
    storage_user_value_data = [0, 0, 0]
    for i in range(n_chiller1 + 1):
        for j in range(n_chiller2 + 1):
            for k in range(n_chiller_chilled_pump1 + 1):
                for l in range(n_chiller_chilled_pump2 + 1):
                    for m in range(n_storage_chilled_pump + 1):
                        if i + j == 0:
                            continue
                        if k + l == 0:
                            continue
                        if m == 0:
                            continue
                        n_cal_f = 0
                        for n in range(len(chiller1_chilled_pump_f_list)):
                            if n_cal_f > 0 and pump_f0_cal == True:
                                continue
                            chiller_Few0_total = i * chiller1_Few0 + j * chiller2_Few0
                            chiller_pump1_f = chiller1_chilled_pump_f_list[n]
                            chiller_pump2_f = chiller2_chilled_pump_f_list[n]
                            chiller_pump_Fw0_total = k * chiller1_chilled_pump_Fw0 * \
                                                     (chiller_pump1_f / chiller1_chilled_pump_f_list[0]) + \
                                                     l * chiller2_chilled_pump_Fw0 * \
                                                     (chiller_pump2_f / chiller2_chilled_pump_f_list[0])
                            storage_pump_f = storage_chilled_pump_f_list[n]
                            storage_pump_Fw0_total = m * storage_chilled_pump_Fw0 * \
                                                     (storage_pump_f / storage_chilled_pump_f_list[0])
                            pump_Fw0_total = chiller_pump_Fw0_total + storage_pump_Fw0_total
                            if pump_Fw0_total >= 2 * chiller_Few0_total:
                                continue
                            if pump_Fw0_total <= 0.2 * chiller_Few0_total:
                                continue
                            chiller_chilled_value_data = []
                            chiller_chilled_pump_data = []
                            storage_chilled_pump_data = []
                            print("正在进行 冷水机同时向用户侧供冷+向水罐蓄冷 水力特性辨识：" +
                                  "；冷水机大冷冻阀门开启数量：" + str(i) + "，冷水机小冷冻阀门开启数量" + str(j) +
                                  "，冷水机大冷冻水泵开启数量" + str(k) + "，冷水机小冷冻水泵开启数量" + str(l) +
                                  "，冷水机大冷冻水泵转速" + str(chiller_pump1_f) +
                                  "，冷水机小冷冻水泵转速" + str(chiller_pump2_f) +
                                  "，蓄冷水罐冷冻水泵开启数量" + str(m) + "，蓄冷水罐冷冻水泵转速" + str(storage_pump_f))
                            # 阀门和水泵输入数值
                            for ii in range(n_chiller1 + 1)[1:]:
                                if ii <= i:
                                    chiller_chilled_value_data.append(1)
                                else:
                                    chiller_chilled_value_data.append(0)
                            for jj in range(n_chiller2 + 1)[1:]:
                                if jj <= j:
                                    chiller_chilled_value_data.append(1)
                                else:
                                    chiller_chilled_value_data.append(0)
                            for kk in range(n_chiller_chilled_pump1 + 1)[1:]:
                                if kk <= k:
                                    chiller_chilled_pump_data.append(chiller_pump1_f)
                                else:
                                    chiller_chilled_pump_data.append(0)
                            for ll in range(n_chiller_chilled_pump2 + 1)[1:]:
                                if ll <= l:
                                    chiller_chilled_pump_data.append(chiller_pump2_f)
                                else:
                                    chiller_chilled_pump_data.append(0)
                            for mm in range(n_storage_chilled_pump + 1)[1:]:
                                if mm <= m:
                                    storage_chilled_pump_data.append(storage_pump_f)
                                else:
                                    storage_chilled_pump_data.append(0)
                            # 整个模型输入数值
                            model_input_data = time_data + environment_input_data_default() + chiller_data + \
                                               chiller_chilled_pump_data + chiller_cooling_pump_data + \
                                               chiller_cooling_tower_data + chiller_chilled_value_data + \
                                               chiller_cooling_value_data + chiller_tower_value_data + \
                                               chiller_tower_chilled_value_data + chiller_user_value_data + \
                                               air_source_heat_pump_input_data_default() + storage_chilled_pump_data + \
                                               storage_chiller_value_data + storage_user_value_data + \
                                               tower_chilled_input_data_default() + user_load_input_data_default()
                            # FMU仿真
                            try:
                                time1 = time.time()
                                result = simulate_sample(fmu_unzipdir, fmu_description, None, start_time, stop_time,
                                                         model_input_data, model_input_type, model_output_name,
                                                         output_interval, time_out, False, False)
                                # 获取仿真结果
                                # 冷水机组总流量=水泵组总流量
                                Few_total = result['chiller_Few_total'][-1]
                                # 冷水机组流量
                                chiller_Few_big_total = result['chiller_Few_big'][-1]
                                chiller_Few_small_total = result['chiller_Few_small'][-1]
                                # 水泵组流量
                                storage_Few_total_from_chiller = result['storage_Few_total_from_chiller'][-1]
                                storage_chilled_pump_H = result['storage_H_chilled_pump'][-1]
                                storage_chilled_pump_P_total = result['storage_P_total_chilled_pump'][-1]
                                chiller_chilled_pump_Few_small_total = result['chiller_Few_chilled_pump_small'][-1]
                                chiller_chilled_pump_Few_big_total = Few_total - storage_Few_total_from_chiller - \
                                                                     chiller_chilled_pump_Few_small_total
                                chiller_chilled_pump_H = result['chiller_H_chilled_pump'][-1]
                                chiller_chilled_pump_P_big_total = result['chiller_P_big_chilled_pump'][-1]
                                chiller_chilled_pump_P_small_total = result['chiller_P_small_chilled_pump'][-1]
                                # 单台冷水机的数据
                                if i == 0:
                                    chiller_Few_big = 0
                                else:
                                    chiller_Few_big = chiller_Few_big_total / i
                                if j == 0:
                                    chiller_Few_small = 0
                                else:
                                    chiller_Few_small = chiller_Few_small_total / j
                                # 冷水机单台水泵的数据
                                if k == 0:
                                    chiller_chilled_pump_Few_big = 0
                                    chiller_chilled_pump_P_big = 0
                                else:
                                    chiller_chilled_pump_Few_big = chiller_chilled_pump_Few_big_total / k
                                    chiller_chilled_pump_P_big = chiller_chilled_pump_P_big_total / k
                                if l == 0:
                                    chiller_chilled_pump_Few_small = 0
                                    chiller_chilled_pump_P_small = 0
                                else:
                                    chiller_chilled_pump_Few_small = chiller_chilled_pump_Few_small_total / l
                                    chiller_chilled_pump_P_small = chiller_chilled_pump_P_small_total / l
                                # 如果水泵频率不是50Hz，则用相似率换算数据
                                if n_cal_f == 0 and chiller_pump1_f < chiller1_chilled_pump_f_list[0] and \
                                        chiller_pump2_f < chiller2_chilled_pump_f_list[0]:
                                    chiller_chilled_pump_Few_big = chiller_chilled_pump_Few_big * (chiller1_chilled_pump_f_list[0] / chiller_pump1_f)
                                    chiller_chilled_pump_Few_small = chiller_chilled_pump_Few_small * (chiller2_chilled_pump_f_list[0] / chiller_pump2_f)
                                    chiller_Few_big = chiller_Few_big * (chiller1_chilled_pump_f_list[0] / chiller_pump1_f)
                                    chiller_Few_small = chiller_Few_small * (chiller2_chilled_pump_f_list[0] / chiller_pump2_f)
                                    chiller_chilled_pump_H = chiller_chilled_pump_H * ((chiller1_chilled_pump_f_list[0] / chiller_pump1_f) ** 2)
                                    chiller_chilled_pump_P_big = chiller_chilled_pump_P_big * ((chiller1_chilled_pump_f_list[0] / chiller_pump1_f) ** 3)
                                    chiller_chilled_pump_P_small = chiller_chilled_pump_P_small * ((chiller2_chilled_pump_f_list[0] / chiller_pump2_f) ** 3)
                                    chiller_pump1_f = chiller1_chilled_pump_f_list[0]
                                    chiller_pump2_f = chiller2_chilled_pump_f_list[0]
                                # 蓄冷单台水泵的数据
                                if m == 0:
                                    storage_chilled_pump_Few = 0
                                    storage_chilled_pump_P = 0
                                else:
                                    storage_chilled_pump_Few = storage_Few_total_from_chiller / m
                                    storage_chilled_pump_P = storage_chilled_pump_P_total / m
                                # 如果水泵频率不是50Hz，则用相似率换算数据
                                if n_cal_f == 0 and storage_pump_f < storage_chilled_pump_f_list[0]:
                                    storage_chilled_pump_Few = storage_chilled_pump_Few * (storage_chilled_pump_f_list[0] / storage_pump_f)
                                    storage_chilled_pump_H = storage_chilled_pump_H * ((storage_chilled_pump_f_list[0] / storage_pump_f) ** 2)
                                    storage_chilled_pump_P = storage_chilled_pump_P * ((storage_chilled_pump_f_list[0] / storage_pump_f) ** 3)
                                    storage_pump_f = storage_chilled_pump_f_list[0]
                                # 仿真结果生成txt
                                tmp_txt = str(i) + "\t" + str(j) + "\t" + str(k) + "\t" + str(l) + "\t" + \
                                          str(chiller_pump1_f) + "\t" + str(chiller_pump2_f) + "\t" + \
                                          str(np.round(chiller_Few_big, 2)) + "\t" + \
                                          str(np.round(chiller_Few_small, 2)) + "\t" + \
                                          str(np.round(chiller_chilled_pump_Few_big, 2)) + "\t" + \
                                          str(np.round(chiller_chilled_pump_Few_small, 2)) + "\t" + \
                                          str(np.round(chiller_chilled_pump_P_big, 2)) + "\t" + \
                                          str(np.round(chiller_chilled_pump_P_small, 2)) + "\t" + \
                                          str(np.round(chiller_chilled_pump_H, 2)) + "\t" + str(m) + "\t" + \
                                          str(storage_pump_f) + "\t" + \
                                          str(np.round(storage_chilled_pump_Few, 2)) + "\t" + \
                                          str(np.round(storage_chilled_pump_P, 2)) + "\t" + \
                                          str(np.round(storage_chilled_pump_H, 2))
                                chiller_user_storage_result_list.append(tmp_txt)
                                time2 = time.time()
                                time_cost = np.round(time2 - time1, 2)
                                print("本次仿真计算用时(秒)：" + str(time_cost) + "\n")
                                n_cal_f += 1
                            except:
                                print("FMU仿真失败：" + "冷水机大冷冻阀门开启数量：" + str(i) +
                                      "，冷水机小冷冻阀门开启数量" + str(j) + "，冷水机大冷冻水泵开启数量" + str(k) +
                                      "，冷水机小冷冻水泵开启数量" + str(l) + "，蓄冷水罐冷冻水泵开启数量" + str(m))
                                print(traceback.format_exc() + "\n")
                                pass
    # 结果写入txt
    write_txt_data(chiller_user_storage_result_txt_path, chiller_user_storage_result_list)


def identify_tower_chilled(n_chiller_cooling_tower, n_tower_chilled_pump, chiller_cooling_tower_Fcw0,
                           tower_chilled_pump_Fw0, tower_chilled_pump_f_list, time_data, chiller_data,
                           chiller_cooling_tower_data, fmu_unzipdir, fmu_description, start_time, stop_time,
                           time_out, model_input_type, model_output_name, output_interval,
                           tower_chilled_result_txt_path, pump_f0_cal):
    """
    冷却塔直接供冷模型，水力特性测试
    Args:
        n_chiller_cooling_tower: [int]，冷却塔装机台数
        n_tower_chilled_pump: [int]，冷冻水泵安装台数
        chiller_cooling_tower_Fcw0: [float]，冷却塔额定冷却水流量
        tower_chilled_pump_Fw0: [float]，冷冻水泵额定冷冻水流量
        tower_chilled_pump_f_list: [list，float]，冷冻水泵需要辨识的转速，列表
        time_data: [list]，模型输入数据，时间
        chiller_data: [list]，模型输入数据，冷水机开关及出水温度温度设定
        chiller_cooling_tower_data: [list]，模型输入数据，冷却塔风机转速比
        fmu_unzipdir: [string]，FMU模型解压后的路径
        fmu_description: [object]，获取FMU模型描述
        start_time: [float]，仿真开始时间，单位：秒
        stop_time: [float]，仿真结束时间，单位：秒
        time_out: [float]，仿真超时时间，单位：秒
        model_input_type: [list]，模型输入名称和数据类型
        model_output_name: [list]，模型输出名称
        output_interval: [float]，FMU模型输出采样时间，单位：秒
        tower_chilled_result_txt_path: [string]，仿真结果保存txt文件路径
        pump_f0_cal: [boolean]，是否仅计算水泵额定转速的数据

    Returns:

    """
    # 冷却塔直接供冷模型，水力特性测试
    tower_chilled_result_list = []
    tower_chilled_result_list.append("冷却塔直接供冷模型，水力特性辨识：")
    tower_chilled_result_list.append("冷水机冷却塔阀门开启数量" + "\t" + "冷却塔直接供冷水泵开启数量" + "\t" +
                                     "冷却塔直接供冷水泵转速" + "\t" + "冷却塔直接供冷水泵单台水流量" + "\t" +
                                     "冷却塔直接供冷水泵单台电功率" + "\t" + "冷却塔直接供冷水泵扬程")
    # 默认值
    chiller_chilled_pump_data = [0, 0, 0, 0, 0, 0]
    chiller_cooling_pump_data = [0, 0, 0, 0, 0, 0]
    chiller_chilled_value_data = [0, 0, 0, 0, 0, 0]
    chiller_cooling_value_data = [0, 0, 0, 0, 0, 0]
    chiller_tower_chilled_value_data = [1, 1]
    chiller_user_value_data = [0, 0]
    for i in range(n_chiller_cooling_tower + 1):
        for j in range(n_tower_chilled_pump + 1):
            if i == 0 or j == 0:
                continue
            n_cal_f = 0
            for k in range(len(tower_chilled_pump_f_list)):
                if n_cal_f > 0 and pump_f0_cal == True:
                    continue
                pump_f = tower_chilled_pump_f_list[k]
                tower_Fcw0_total = i * chiller_cooling_tower_Fcw0
                pump_Fw0_total = j * tower_chilled_pump_Fw0 * (pump_f / tower_chilled_pump_f_list[0])
                if pump_Fw0_total >= 2 * tower_Fcw0_total:
                    continue
                chiller_tower_value_data = []
                tower_chilled_pump_data = []
                print("正在进行 冷却塔直接供冷模型 水力特性辨识：" + "，冷水机冷却塔阀门开启数量" + str(i) +
                      "，冷却塔直接供冷水泵开启数量" + str(j) + "，冷却塔直接供冷水泵转速" + str(pump_f))
                # 阀门和水泵输入数值
                for ii in range(n_chiller_cooling_tower + 1)[1:]:
                    if ii <= i:
                        chiller_tower_value_data.append(1)
                    else:
                        chiller_tower_value_data.append(0)
                for jj in range(n_tower_chilled_pump + 1)[1:]:
                    if jj <= j:
                        tower_chilled_pump_data.append(pump_f)
                    else:
                        tower_chilled_pump_data.append(0)
                # 整个模型输入数值
                model_input_data = time_data + environment_input_data_default() + chiller_data + \
                                   chiller_chilled_pump_data + chiller_cooling_pump_data + \
                                   chiller_cooling_tower_data + chiller_chilled_value_data + \
                                   chiller_cooling_value_data + chiller_tower_value_data + \
                                   chiller_tower_chilled_value_data + chiller_user_value_data + \
                                   air_source_heat_pump_input_data_default() + cold_storage_input_data_default() + \
                                   tower_chilled_pump_data + user_load_input_data_default()
                # FMU仿真
                try:
                    time1 = time.time()
                    result = simulate_sample(fmu_unzipdir, fmu_description, None, start_time, stop_time,
                                             model_input_data, model_input_type, model_output_name, output_interval,
                                             time_out, False, False)
                    # 获取仿真结果
                    Few_total = result['tower_chilled_Few_total'][-1]
                    chilled_pump_H = result['tower_chilled_H_chilled_pump'][-1]
                    chilled_pump_P_total = result['tower_chilled_P_total_chilled_pump'][-1]
                    # 单台水泵的数据
                    if j == 0:
                        chilled_pump_Few = 0
                        chilled_pump_P = 0
                    else:
                        chilled_pump_Few = Few_total / j
                        chilled_pump_P = chilled_pump_P_total / j
                    # 如果水泵频率不是50Hz，则用相似率换算数据
                    if n_cal_f == 0 and pump_f < tower_chilled_pump_f_list[0]:
                        chilled_pump_Few = chilled_pump_Few * (tower_chilled_pump_f_list[0] / pump_f)
                        chilled_pump_H = chilled_pump_H * ((tower_chilled_pump_f_list[0] / pump_f) ** 2)
                        chilled_pump_P = chilled_pump_P * ((tower_chilled_pump_f_list[0] / pump_f) ** 3)
                        pump_f = tower_chilled_pump_f_list[0]
                    # 仿真结果生成txt
                    tmp_txt = str(i) + "\t" + str(j) + "\t" + str(pump_f) + "\t" + \
                              str(np.round(chilled_pump_Few, 2)) + "\t" + \
                              str(np.round(chilled_pump_P, 2)) + "\t" + str(np.round(chilled_pump_H, 2))
                    tower_chilled_result_list.append(tmp_txt)
                    time2 = time.time()
                    time_cost = np.round(time2 - time1, 2)
                    print("本次仿真计算用时(秒)：" + str(time_cost) + "\n")
                    n_cal_f += 1
                except:
                    print("FMU仿真失败：" + "，冷水机冷却塔阀门开启数量" + str(i) +
                          "，冷却塔直接供冷水泵开启数量" + str(j))
                    print(traceback.format_exc() + "\n")
                    pass
    write_txt_data(tower_chilled_result_txt_path, tower_chilled_result_list)


def identify_tower_cooling_chilled(n_chiller1, n_chiller2, n_chiller_cooling_pump1, n_chiller_cooling_pump2,
                                   n_chiller_cooling_tower, chiller1_Fcw0, chiller2_Fcw0, chiller_cooling_tower_Fcw0,
                                   chiller1_cooling_pump_Fw0,  chiller2_cooling_pump_Fw0, chiller1_cooling_pump_f_list,
                                   chiller2_cooling_pump_f_list, n_tower_chilled_pump, tower_chilled_pump_Fw0,
                                   tower_chilled_pump_f_list, time_data, chiller_data, chiller_cooling_tower_data,
                                   fmu_unzipdir, fmu_description, start_time, stop_time, time_out, model_input_type,
                                   model_output_name, output_interval, tower_cooling_chilled_result_txt_path,
                                   pump_f0_cal):
    """
    冷水机冷却侧+冷却塔直接供冷模型，水力特性测试
    Args:
        n_chiller1: [int]，大冷水机装机台数
        n_chiller2: [int]，小冷水机装机台数
        n_chiller_cooling_pump1: [int]，大冷却水泵装机台数
        n_chiller_cooling_pump2: [int]，小冷却水泵装机台数
        n_chiller_cooling_tower: [int]，冷却塔装机台数
        chiller1_Fcw0: [float]，大冷水机额定冷却水流量
        chiller2_Fcw0: [float]，小冷水机额定冷却水流量
        chiller_cooling_tower_Fcw0: [float]，冷却塔额定冷却水流量
        chiller1_cooling_pump_Fw0: [float]，大冷却水泵额定冷却水流量
        chiller2_cooling_pump_Fw0: [float]，小冷却水泵额定冷却水流量
        chiller1_cooling_pump_f_list: [list，float]，大冷却水泵需要辨识的转速，列表
        chiller2_cooling_pump_f_list: [list，float]，小冷却水泵需要辨识的转速，列表
        n_tower_chilled_pump: [int]，冷冻水泵安装台数
        tower_chilled_pump_Fw0: [float]，冷冻水泵额定冷冻水流量
        tower_chilled_pump_f_list: [list，float]，冷冻水泵需要辨识的转速，列表
        time_data: [list]，模型输入数据，时间
        chiller_data: [list]，模型输入数据，冷水机开关及出水温度温度设定
        chiller_cooling_tower_data: [list]，模型输入数据，冷却塔风机转速比
        fmu_unzipdir: [string]，FMU模型解压后的路径
        fmu_description: [object]，获取FMU模型描述
        start_time: [float]，仿真开始时间，单位：秒
        stop_time: [float]，仿真结束时间，单位：秒
        time_out: [float]，仿真超时时间，单位：秒
        model_input_type: [list]，模型输入名称和数据类型
        model_output_name: [list]，模型输出名称
        output_interval: [float]，FMU模型输出采样时间，单位：秒
        tower_cooling_chilled_result_txt_path: [string]，仿真结果保存txt文件路径
        pump_f0_cal: [boolean]，是否仅计算水泵额定转速的数据

    Returns:

    """
    # 冷水机冷却侧+冷却塔直接供冷模型，水力特性测试
    tower_cooling_chilled_result_list = []
    tower_cooling_chilled_result_list.append("冷水机冷却侧+冷却塔直接供冷模型，水力特性测试：")
    tower_cooling_chilled_result_list.append("冷水机大冷却阀门开启数量" + "\t" + "冷水机小冷却阀门开启数量" + "\t" +
                                             "冷水机冷却塔阀门开启数量" + "\t" + "冷水机大冷却水泵开启数量" + "\t" +
                                             "冷水机小冷却水泵开启数量" + "\t" + "冷水机大冷却水泵开启转速" + "\t" +
                                             "冷水机小冷却水泵开启转速" + "\t" + "大冷水机单台水流量" + "\t" +
                                             "小冷水机单台水流量" + "\t" + "冷水机大冷却水泵单台水流量" + "\t" +
                                             "冷水机小冷却水泵单台水流量" + "\t" + "冷水机大冷却水泵单台电功率" + "\t" +
                                             "冷水机小冷却水泵单台电功率" + "\t" + "冷水机冷却水泵扬程" + "\t" +
                                             "冷却塔直接供冷水泵开启数量" + "\t" + "冷却塔直接供冷水泵转速" + "\t" +
                                             "冷却塔直接供冷水泵单台水流量" + "\t" + "冷却塔直接供冷水泵单台电功率" + "\t" +
                                             "冷却塔直接供冷水泵扬程")
    # 默认值
    chiller_chilled_pump_data = [0, 0, 0, 0, 0, 0]
    chiller_chilled_value_data = [0, 0, 0, 0, 0, 0]
    chiller_tower_chilled_value_data = [1, 1]
    chiller_user_value_data = [0, 0]
    for i in range(n_chiller1 + 1):
        for j in range(n_chiller2 + 1):
            for k in range(n_chiller_cooling_tower + 1):
                for l in range(n_chiller_cooling_pump1 + 1):
                    for m in range(n_chiller_cooling_pump2 + 1):
                        for n in range(n_tower_chilled_pump + 1):
                            if i + j == 0:
                                continue
                            if k == 0:
                                continue
                            if l + m == 0:
                                continue
                            if n == 0:
                                continue
                            n_cal_f = 0
                            for o in range(len(chiller1_cooling_pump_f_list)):
                                if n_cal_f > 0 and pump_f0_cal == True:
                                    continue
                                chiller_pump1_f = chiller1_cooling_pump_f_list[o]
                                chiller_pump2_f = chiller2_cooling_pump_f_list[o]
                                chiller_Fcw0_total = i * chiller1_Fcw0 + j * chiller2_Fcw0
                                tower_Fcw0_total = k * chiller_cooling_tower_Fcw0
                                chiller_pump_Fw0_total = l * chiller1_cooling_pump_Fw0 * \
                                                         (chiller_pump1_f / chiller1_cooling_pump_f_list[0]) + \
                                                         m * chiller2_cooling_pump_Fw0 * \
                                                         (chiller_pump2_f / chiller2_cooling_pump_f_list[0])
                                tower_chilled_pump_f = tower_chilled_pump_f_list[o]
                                tower_chilled_pump_Fw0_total = n * tower_chilled_pump_Fw0 * \
                                                               (tower_chilled_pump_f / tower_chilled_pump_f_list[0])
                                if chiller_pump_Fw0_total >= 2 * chiller_Fcw0_total:
                                    continue
                                if chiller_pump_Fw0_total <= 0.2 * chiller_Fcw0_total:
                                    continue
                                if chiller_pump_Fw0_total + tower_chilled_pump_Fw0_total >= 2 * tower_Fcw0_total:
                                    continue
                                chiller_cooling_value_data = []
                                chiller_tower_value_data = []
                                chiller_cooling_pump_data = []
                                tower_chilled_pump_data = []
                                print("正在进行 冷水机冷却侧+冷却塔直接供冷 水力特性辨识：" + "冷水机大冷却阀门开启数量：" +
                                      str(i) + "，冷水机小冷却阀门开启数量" + str(j) + "，冷水机冷却塔阀门开启数量" +
                                      str(k) + "，冷水机大冷却水泵开启数量" + str(l) + "，冷水机小冷却水泵开启数量" +
                                      str(m) + "，冷水机大冷却水泵转速" + str(chiller_pump1_f) + "，冷水机小冷却水泵转速" +
                                      str(chiller_pump2_f) + "，冷却塔直接供冷水泵开启数量" + str(n) +
                                      "，冷却塔直接供冷水泵转速" + str(tower_chilled_pump_f))
                                # 冷水机阀门和水泵输入数值
                                for ii in range(n_chiller1 + 1)[1:]:
                                    if ii <= i:
                                        chiller_cooling_value_data.append(1)
                                    else:
                                        chiller_cooling_value_data.append(0)
                                for jj in range(n_chiller2 + 1)[1:]:
                                    if jj <= j:
                                        chiller_cooling_value_data.append(1)
                                    else:
                                        chiller_cooling_value_data.append(0)
                                for kk in range(n_chiller_cooling_tower + 1)[1:]:
                                    if kk <= k:
                                        chiller_tower_value_data.append(1)
                                    else:
                                        chiller_tower_value_data.append(0)
                                for ll in range(n_chiller_cooling_pump1 + 1)[1:]:
                                    if ll <= l:
                                        chiller_cooling_pump_data.append(chiller_pump1_f)
                                    else:
                                        chiller_cooling_pump_data.append(0)
                                for mm in range(n_chiller_cooling_pump2 + 1)[1:]:
                                    if mm <= m:
                                        chiller_cooling_pump_data.append(chiller_pump2_f)
                                    else:
                                        chiller_cooling_pump_data.append(0)
                                # 冷却塔直接供冷水泵输入数值
                                for nn in range(n_tower_chilled_pump + 1)[1:]:
                                    if nn <= n:
                                        tower_chilled_pump_data.append(tower_chilled_pump_f)
                                    else:
                                        tower_chilled_pump_data.append(0)
                                # 整个模型输入数值
                                model_input_data = time_data + environment_input_data_default() + chiller_data + \
                                                   chiller_chilled_pump_data + chiller_cooling_pump_data + \
                                                   chiller_cooling_tower_data + chiller_chilled_value_data + \
                                                   chiller_cooling_value_data + chiller_tower_value_data + \
                                                   chiller_tower_chilled_value_data + chiller_user_value_data + \
                                                   air_source_heat_pump_input_data_default() + \
                                                   cold_storage_input_data_default() + tower_chilled_pump_data + \
                                                   user_load_input_data_default()
                                # FMU仿真
                                try:
                                    time1 = time.time()
                                    result = simulate_sample(fmu_unzipdir, fmu_description, None, start_time, stop_time,
                                                             model_input_data, model_input_type, model_output_name,
                                                             output_interval, time_out, False, False)
                                    # 获取仿真结果
                                    # 冷水机组总流量=水泵组总流量
                                    chiller_Fcw_total = result['chiller_Fcw_total'][-1]
                                    # 冷水机组流量
                                    chiller_Fcw_big_total = result['chiller_Fcw_big'][-1]
                                    chiller_Fcw_small_total = result['chiller_Fcw_small'][-1]
                                    # 水泵组流量
                                    cooling_pump_Fcw_small_total = result['chiller_Fcw_cooling_pump_small'][-1]
                                    cooling_pump_Fcw_big_total = chiller_Fcw_total - cooling_pump_Fcw_small_total
                                    cooling_pump_H = result['chiller_H_cooling_pump'][-1]
                                    cooling_pump_P_big_total = result['chiller_P_big_cooling_pump'][-1]
                                    cooling_pump_P_small_total = result['chiller_P_small_cooling_pump'][-1]
                                    # 冷却塔直接供冷
                                    tower_chilled_Few_total = result['tower_chilled_Few_total'][-1]
                                    tower_chilled_pump_H = result['tower_chilled_H_chilled_pump'][-1]
                                    tower_chilled_pump_P_total = result['tower_chilled_P_total_chilled_pump'][-1]
                                    # 单台冷水机的数据
                                    if i == 0:
                                        chiller_Fcw_big = 0
                                    else:
                                        chiller_Fcw_big = chiller_Fcw_big_total / i
                                    if j == 0:
                                        chiller_Fcw_small = 0
                                    else:
                                        chiller_Fcw_small = chiller_Fcw_small_total / j
                                    # 冷水机单台水泵的数据
                                    if l == 0:
                                        cooling_pump_Fcw_big = 0
                                        cooling_pump_P_big = 0
                                    else:
                                        cooling_pump_Fcw_big = cooling_pump_Fcw_big_total / l
                                        cooling_pump_P_big = cooling_pump_P_big_total / l
                                    if m == 0:
                                        cooling_pump_Fcw_small = 0
                                        cooling_pump_P_small = 0
                                    else:
                                        cooling_pump_Fcw_small = cooling_pump_Fcw_small_total / m
                                        cooling_pump_P_small = cooling_pump_P_small_total / m
                                    # 如果水泵频率不是50Hz，则用相似率换算数据
                                    if n_cal_f == 0 and chiller_pump1_f < chiller1_cooling_pump_f_list[0] and \
                                            chiller_pump2_f < chiller2_cooling_pump_f_list[0]:
                                        cooling_pump_Fcw_big = cooling_pump_Fcw_big * (chiller1_cooling_pump_f_list[0] / chiller_pump1_f)
                                        cooling_pump_Fcw_small = cooling_pump_Fcw_small * (chiller2_cooling_pump_f_list[0] / chiller_pump2_f)
                                        chiller_Fcw_big = chiller_Fcw_big * (chiller1_cooling_pump_f_list[0] / chiller_pump1_f)
                                        chiller_Fcw_small = chiller_Fcw_small * (chiller2_cooling_pump_f_list[0] / chiller_pump2_f)
                                        cooling_pump_H = cooling_pump_H * ((chiller1_cooling_pump_f_list[0] / chiller_pump1_f) ** 2)
                                        cooling_pump_P_big = cooling_pump_P_big * ((chiller1_cooling_pump_f_list[0] / chiller_pump1_f) ** 3)
                                        cooling_pump_P_small = cooling_pump_P_small * ((chiller2_cooling_pump_f_list[0] / chiller_pump2_f) ** 3)
                                        chiller_pump1_f = chiller1_cooling_pump_f_list[0]
                                        chiller_pump2_f = chiller2_cooling_pump_f_list[0]
                                    # 冷却塔直接供冷单台水泵的数据
                                    if n == 0:
                                        tower_chilled_pump_Few = 0
                                        tower_chilled_pump_P = 0
                                    else:
                                        tower_chilled_pump_Few = tower_chilled_Few_total / n
                                        tower_chilled_pump_P = tower_chilled_pump_P_total / n
                                    # 如果水泵频率不是50Hz，则用相似率换算数据
                                    if n_cal_f == 0 and tower_chilled_pump_f < tower_chilled_pump_f_list[0]:
                                        tower_chilled_pump_Few = tower_chilled_pump_Few * (tower_chilled_pump_f_list[0] / tower_chilled_pump_f)
                                        tower_chilled_pump_H = tower_chilled_pump_H * ((tower_chilled_pump_f_list[0] / tower_chilled_pump_f) ** 2)
                                        tower_chilled_pump_P = tower_chilled_pump_P * ((tower_chilled_pump_f_list[0] / tower_chilled_pump_f) ** 3)
                                        tower_chilled_pump_f = tower_chilled_pump_f_list[0]
                                    # 仿真结果生成txt
                                    tmp_txt = str(i) + "\t" + str(j) + "\t" + str(k) + "\t" + str(l) + "\t" + \
                                              str(m) + "\t" + str(chiller_pump1_f) + "\t" + str(chiller_pump2_f) + "\t" + \
                                              str(np.round(chiller_Fcw_big, 2)) + "\t" + \
                                              str(np.round(chiller_Fcw_small, 2)) + "\t" + \
                                              str(np.round(cooling_pump_Fcw_big, 2)) + "\t" + \
                                              str(np.round(cooling_pump_Fcw_small, 2)) + "\t" + \
                                              str(np.round(cooling_pump_P_big, 2)) + "\t" + \
                                              str(np.round(cooling_pump_P_small, 2)) + "\t" + \
                                              str(np.round(cooling_pump_H, 2)) + "\t" + str(n)+ "\t" + \
                                              str(tower_chilled_pump_f) + "\t" + \
                                              str(np.round(tower_chilled_pump_Few, 2)) + "\t" + \
                                              str(np.round(tower_chilled_pump_P, 2)) + "\t" + \
                                              str(np.round(tower_chilled_pump_H, 2))
                                    tower_cooling_chilled_result_list.append(tmp_txt)
                                    time2 = time.time()
                                    time_cost = np.round(time2 - time1, 2)
                                    print("本次仿真计算用时(秒)：" + str(time_cost) + "\n")
                                    n_cal_f += 1
                                except:
                                    print("FMU仿真失败：" + "大冷却阀门开启数量：" + str(i) + "，小冷却阀门开启数量" + str(j) +
                                          "，冷却塔阀门开启数量" + str(k) + "，大冷却水泵开启数量" + str(l) +
                                          "，小冷却水泵开启数量" + str(m) + "，冷却塔直接供冷水泵开启数量" + str(n))
                                    print(traceback.format_exc() + "\n")
                                    pass
    # 结果写入txt
    write_txt_data(tower_cooling_chilled_result_txt_path, tower_cooling_chilled_result_list)


def identify_full_open(n_chiller1, n_chiller2, n_chiller_chilled_pump1, n_chiller_chilled_pump2,
                       chiller1_chilled_pump_Fw0, chiller2_chilled_pump_Fw0, chiller1_chilled_pump_f0,
                       chiller2_chilled_pump_f0, n_chiller_cooling_pump1, n_chiller_cooling_pump2,
                       chiller1_cooling_pump_Fw0, chiller2_cooling_pump_Fw0, chiller1_cooling_pump_f0,
                       chiller2_cooling_pump_f0, n_ashp_chilled_pump, ashp_chilled_pump_Fw0, ashp_chilled_pump_f0,
                       n_storage_chilled_pump, storage_chilled_pump_Fw0, storage_chilled_pump_f0,
                       n_tower_chilled_pump, tower_chilled_pump_Fw0, tower_chilled_pump_f0, time_data, chiller_data,
                       chiller_cooling_tower_data, air_source_heat_pump_data, fmu_unzipdir, fmu_description,
                       start_time,  stop_time, time_out, model_input_type, model_output_name, output_interval,
                       full_open_result_txt_path):
    """
    阀门和水泵全部开启情况下，额定点水力特性测试
    Args:
        n_chiller1: [int]，大冷水机装机台数
        n_chiller2: [int]，小冷水机装机台数
        n_chiller_chilled_pump1: [int]，大冷冻水泵装机台数
        n_chiller_chilled_pump2: [int]，小冷冻水泵装机台数
        chiller1_chilled_pump_Fw0: [float]，大冷冻水泵额定冷冻水流量
        chiller2_chilled_pump_Fw0: [float]，小冷冻水泵额定冷冻水流量
        chiller1_chilled_pump_f0: [float]，水泵额定转速
        chiller2_chilled_pump_f0: [float]，水泵额定转速
        n_chiller_cooling_pump1: [int]，大冷却水泵装机台数
        n_chiller_cooling_pump2: [int]，小冷却水泵装机台数
        chiller1_cooling_pump_Fw0: [float]，大冷却水泵额定冷却水流量
        chiller2_cooling_pump_Fw0: [float]，小冷却水泵额定冷却水流量
        chiller1_cooling_pump_f0: [float]，水泵额定转速
        chiller2_cooling_pump_f0: [float]，水泵额定转速
        n_ashp_chilled_pump: [int]，冷冻水泵装机台数
        ashp_chilled_pump_Fw0: [float]，冷冻水泵额定冷冻水流量
        ashp_chilled_pump_f0: [float]，水泵额定转速
        n_storage_chilled_pump: [int]，冷冻水泵装机台数
        storage_chilled_pump_Fw0: [float]，冷冻水泵额定冷冻水流量
        storage_chilled_pump_f0: [float]，水泵额定转速
        n_tower_chilled_pump: [int]，冷冻水泵装机台数
        tower_chilled_pump_Fw0: [float]，冷冻水泵额定冷冻水流量
        tower_chilled_pump_f0: [float]，水泵额定转速
        time_data: [list]，模型输入数据，时间
        chiller_data: [list]，模型输入数据，冷水机开关及出水温度温度设定
        chiller_cooling_tower_data: [list]，模型输入数据，冷却塔风机转速比
        air_source_heat_pump_data: [list]，模型输入数据，空气源热泵开关及出水温度温度设定
        fmu_unzipdir: [string]，FMU模型解压后的路径
        fmu_description: [object]，获取FMU模型描述
        start_time: [float]，仿真开始时间，单位：秒
        stop_time: [float]，仿真结束时间，单位：秒
        time_out: [float]，仿真超时时间，单位：秒
        model_input_type: [list]，模型输入名称和数据类型
        model_output_name: [list]，模型输出名称
        output_interval: [float]，FMU模型输出采样时间，单位：秒
        full_open_result_txt_path: [string]，仿真结果保存txt文件路径

    Returns:

    """
    full_open_result_list = []

    # 冷水机模型，向用户侧供冷，阀门和水泵全开
    full_open_result_list.append("冷水机模型，向用户侧供冷，阀门和水泵全开，水力特性辨识：")
    full_open_result_list.append("实际总流量" + "\t" + "额定总流量" + "\t" + "总流量比例" + "\t" +
                                 "大冷水机实际总流量" + "\t" + "小冷水机实际总流量" + "\t" + "冷水机实际流量分配比例" + "\t" +
                                 "大冷冻水泵实际总流量" + "\t" + "大冷冻水泵额定总流量" + "\t" + "大冷冻水泵流量比例" + "\t" +
                                 "小冷冻水泵实际总流量" + "\t" + "小冷冻水泵额定总流量" + "\t" + "小冷冻水泵流量比例" + "\t" +
                                 "大冷冻水泵实际总电功率" + "\t" + "小冷冻水泵实际总电功率" + "\t" + "冷冻水泵实际扬程")
    chiller_chilled_pump1_Fw0_total = n_chiller_chilled_pump1 * chiller1_chilled_pump_Fw0
    chiller_chilled_pump2_Fw0_total = n_chiller_chilled_pump2 * chiller2_chilled_pump_Fw0
    chiller_chilled_pump_Fw0_total = chiller_chilled_pump1_Fw0_total + chiller_chilled_pump2_Fw0_total
    chiller_chilled_pump_data = [chiller1_chilled_pump_f0, chiller1_chilled_pump_f0, chiller1_chilled_pump_f0,
                                 chiller1_chilled_pump_f0, chiller2_chilled_pump_f0, chiller2_chilled_pump_f0]
    chiller_cooling_pump_data = [0, 0, 0, 0, 0, 0]
    chiller_chilled_value_data = [1, 1, 1, 1, 1, 1]
    chiller_cooling_value_data = [0, 0, 0, 0, 0, 0]
    chiller_tower_value_data = [0, 0, 0, 0, 0, 0]
    chiller_tower_chilled_value_data = [0, 0]
    chiller_user_value_data = [1, 1]
    model_input_data = time_data + environment_input_data_default() + chiller_data + \
                       chiller_chilled_pump_data + chiller_cooling_pump_data + \
                       chiller_cooling_tower_data + chiller_chilled_value_data + \
                       chiller_cooling_value_data + chiller_tower_value_data + \
                       chiller_tower_chilled_value_data + chiller_user_value_data + \
                       air_source_heat_pump_input_data_default() + \
                       cold_storage_input_data_default() + tower_chilled_input_data_default() + \
                       user_load_input_data_default()
    try:
        time1 = time.time()
        print("正在进行：冷水机模型，向用户侧供冷，阀门和水泵全开，水力特性辨识！")
        result = simulate_sample(fmu_unzipdir, fmu_description, None, start_time, stop_time,
                                 model_input_data, model_input_type, model_output_name,
                                 output_interval, time_out, False, False)
        # 获取仿真结果
        # 冷水机组总流量=水泵组总流量
        Few_total = result['chiller_Few_total'][-1]
        # 冷水机组流量
        chiller_Few_big_total = result['chiller_Few_big'][-1]
        chiller_Few_small_total = result['chiller_Few_small'][-1]
        chiller_Few_big = chiller_Few_big_total / n_chiller1
        chiller_Few_small = chiller_Few_small_total / n_chiller2
        # 水泵组流量
        chilled_pump_Few_small_total = result['chiller_Few_chilled_pump_small'][-1]
        chilled_pump_Few_big_total = Few_total - chilled_pump_Few_small_total
        chilled_pump_H = result['chiller_H_chilled_pump'][-1]
        chilled_pump_P_big_total = result['chiller_P_big_chilled_pump'][-1]
        chilled_pump_P_small_total = result['chiller_P_small_chilled_pump'][-1]
        # 仿真结果生成txt
        tmp_txt = str(np.round(Few_total, 2)) + "\t" + \
                  str(np.round(chiller_chilled_pump_Fw0_total, 2)) + "\t" + \
                  str(np.round(Few_total / chiller_chilled_pump_Fw0_total, 4)) + "\t" + \
                  str(np.round(chiller_Few_big_total, 2)) + "\t" + str(np.round(chiller_Few_small_total, 2)) + "\t" + \
                  str(np.round(chiller_Few_big / chiller_Few_small, 4)) + "\t" + \
                  str(np.round(chilled_pump_Few_big_total, 2)) + "\t" + \
                  str(np.round(chiller_chilled_pump1_Fw0_total, 2)) + "\t" + \
                  str(np.round(chilled_pump_Few_big_total / chiller_chilled_pump1_Fw0_total, 4)) + "\t" + \
                  str(np.round(chilled_pump_Few_small_total, 2)) + "\t" + \
                  str(np.round(chiller_chilled_pump2_Fw0_total, 2)) + "\t" + \
                  str(np.round(chilled_pump_Few_small_total / chiller_chilled_pump2_Fw0_total, 4)) + "\t" + \
                  str(np.round(chilled_pump_P_big_total, 2)) + "\t" + \
                  str(np.round(chilled_pump_P_small_total, 2)) + "\t" + str(np.round(chilled_pump_H, 2)) + "\n"
        full_open_result_list.append(tmp_txt)
        time2 = time.time()
        time_cost = np.round(time2 - time1, 2)
        print("本次仿真计算用时(秒)：" + str(time_cost) + "\n")
    except:
        print("FMU仿真失败：冷水机模型，向用户侧供冷，阀门和水泵全开，水力特性辨识！")
        print(traceback.format_exc() + "\n")

    # 冷水机模型，冷却水系统，阀门和水泵全开
    full_open_result_list.append("冷水机模型，冷却水系统，阀门和水泵全开，水力特性辨识：")
    full_open_result_list.append("实际总流量" + "\t" + "额定总流量" + "\t" + "实际流量比例" + "\t" +
                                 "大冷水机实际总流量" + "\t" + "小冷水机实际总流量" + "\t" + "冷水机实际流量分配比例" + "\t" +
                                 "大冷却水泵实际总流量" + "\t" + "大冷却水泵额定总流量" + "\t" + "大冷却水泵流量比例" + "\t" +
                                 "小冷却水泵实际总流量" + "\t" + "小冷却水泵额定总流量" + "\t" + "小冷却水泵流量比例" + "\t" +
                                 "大冷却水泵实际总电功率" + "\t" + "小冷却水泵实际总电功率" + "\t" + "冷却水泵实际扬程")
    chiller_cooling_pump1_Fw0_total = n_chiller_cooling_pump1 * chiller1_cooling_pump_Fw0
    chiller_cooling_pump2_Fw0_total = n_chiller_cooling_pump2 * chiller2_cooling_pump_Fw0
    chiller_cooling_pump_Fw0_total = chiller_cooling_pump1_Fw0_total + chiller_cooling_pump2_Fw0_total
    chiller_chilled_pump_data = [0, 0, 0, 0, 0, 0]
    chiller_cooling_pump_data = [chiller1_cooling_pump_f0, chiller1_cooling_pump_f0, chiller1_cooling_pump_f0,
                                 chiller1_cooling_pump_f0, chiller2_cooling_pump_f0, chiller2_cooling_pump_f0]
    chiller_chilled_value_data = [0, 0, 0, 0, 0, 0]
    chiller_cooling_value_data = [1, 1, 1, 1, 1, 1]
    chiller_tower_value_data = [1, 1, 1, 1, 1, 1]
    chiller_tower_chilled_value_data = [0, 0]
    chiller_user_value_data = [0, 0]
    model_input_data = time_data + environment_input_data_default() + chiller_data + \
                       chiller_chilled_pump_data + chiller_cooling_pump_data + \
                       chiller_cooling_tower_data + chiller_chilled_value_data + \
                       chiller_cooling_value_data + chiller_tower_value_data + \
                       chiller_tower_chilled_value_data + chiller_user_value_data + \
                       air_source_heat_pump_input_data_default() + \
                       cold_storage_input_data_default() + tower_chilled_input_data_default() + \
                       user_load_input_data_default()
    try:
        time1 = time.time()
        print("正在进行：冷水机模型，冷却水系统，阀门和水泵全开，水力特性辨识！")
        result = simulate_sample(fmu_unzipdir, fmu_description, None, start_time, stop_time,
                                 model_input_data, model_input_type, model_output_name,
                                 output_interval, time_out, False, False)
        # 获取仿真结果
        # 冷水机组总流量=水泵组总流量
        Fcw_total = result['chiller_Fcw_total'][-1]
        # 冷水机组流量
        chiller_Fcw_big_total = result['chiller_Fcw_big'][-1]
        chiller_Fcw_small_total = result['chiller_Fcw_small'][-1]
        chiller_Fcw_big = chiller_Fcw_big_total / n_chiller1
        chiller_Fcw_small = chiller_Fcw_small_total / n_chiller2
        # 水泵组流量
        cooling_pump_Fcw_small_total = result['chiller_Fcw_cooling_pump_small'][-1]
        cooling_pump_Fcw_big_total = Fcw_total - cooling_pump_Fcw_small_total
        cooling_pump_H = result['chiller_H_cooling_pump'][-1]
        cooling_pump_P_big_total = result['chiller_P_big_cooling_pump'][-1]
        cooling_pump_P_small_total = result['chiller_P_small_cooling_pump'][-1]
        # 仿真结果生成txt
        tmp_txt = str(np.round(Fcw_total, 2)) + "\t" + \
                  str(np.round(chiller_cooling_pump_Fw0_total, 2)) + "\t" + \
                  str(np.round(Fcw_total / chiller_cooling_pump_Fw0_total, 4)) + "\t" + \
                  str(np.round(chiller_Fcw_big_total, 2)) + "\t" + str(np.round(chiller_Fcw_small_total, 2)) + "\t" + \
                  str(np.round(chiller_Fcw_big / chiller_Fcw_small, 4)) + "\t" + \
                  str(np.round(cooling_pump_Fcw_big_total, 2)) + "\t" + \
                  str(np.round(chiller_cooling_pump1_Fw0_total, 2)) + "\t" + \
                  str(np.round(cooling_pump_Fcw_big_total / chiller_cooling_pump1_Fw0_total, 4)) + "\t" + \
                  str(np.round(cooling_pump_Fcw_small_total, 2)) + "\t" + \
                  str(np.round(chiller_cooling_pump2_Fw0_total, 2)) + "\t" + \
                  str(np.round(cooling_pump_Fcw_small_total / chiller_cooling_pump2_Fw0_total, 4)) + "\t" + \
                  str(np.round(cooling_pump_P_big_total, 2)) + "\t" + \
                  str(np.round(cooling_pump_P_small_total, 2)) + "\t" + \
                  str(np.round(cooling_pump_H, 2)) + "\n"
        full_open_result_list.append(tmp_txt)
        time2 = time.time()
        time_cost = np.round(time2 - time1, 2)
        print("本次仿真计算用时(秒)：" + str(time_cost) + "\n")
    except:
        print("FMU仿真失败：冷水机模型，冷却水系统，阀门和水泵全开，水力特性辨识！")
        print(traceback.format_exc() + "\n")

    # 空气源热泵模型，向用户侧供冷，阀门和水泵全开
    full_open_result_list.append("空气源热泵模型，向用户侧供冷，阀门和水泵全开，水力特性辨识：")
    full_open_result_list.append("冷冻水泵实际总流量" + "\t" + "冷冻水泵额定总流量" + "\t" + "冷冻水泵流量比例" + "\t" +
                                 "冷冻水泵实际总电功率" + "\t" + "冷冻水泵实际扬程")
    ashp_chilled_pump_Fw0_total = n_ashp_chilled_pump * ashp_chilled_pump_Fw0
    ashp_chilled_pump_data = [ashp_chilled_pump_f0, ashp_chilled_pump_f0, ashp_chilled_pump_f0, ashp_chilled_pump_f0]
    ashp_chilled_value_data = [1, 1, 1, 1]
    model_input_data = time_data + environment_input_data_default() + chiller_input_data_default() + \
                       air_source_heat_pump_data + ashp_chilled_pump_data + ashp_chilled_value_data + \
                       cold_storage_input_data_default() + tower_chilled_input_data_default() + \
                       user_load_input_data_default()
    try:
        time1 = time.time()
        print("正在进行：空气源热泵模型，向用户侧供冷，阀门和水泵全开，水力特性辨识！")
        result = simulate_sample(fmu_unzipdir, fmu_description, None, start_time, stop_time,
                                 model_input_data, model_input_type, model_output_name, output_interval,
                                 time_out, False, False)
        Few_total = result['ashp_Few_total'][-1]
        chilled_pump_H = result['ashp_H_chilled_pump'][-1]
        chilled_pump_P_total = result['ashp_P_total_chilled_pump'][-1]
        # 仿真结果生成txt
        tmp_txt = str(np.round(Few_total, 2)) + "\t" + str(np.round(ashp_chilled_pump_Fw0_total, 2)) + "\t" + \
                  str(np.round(Few_total / ashp_chilled_pump_Fw0_total, 4)) + "\t" + \
                  str(np.round(chilled_pump_P_total, 2)) + "\t" + str(np.round(chilled_pump_H, 2)) + "\n"
        full_open_result_list.append(tmp_txt)
        time2 = time.time()
        time_cost = np.round(time2 - time1, 2)
        print("本次仿真计算用时(秒)：" + str(time_cost) + "\n")
    except:
        print("FMU仿真失败：空气源热泵模型，向用户侧供冷，阀门和水泵全开，水力特性辨识！")
        print(traceback.format_exc() + "\n")

    # 蓄冷水罐模型，蓄冷工况，阀门和水泵全开
    full_open_result_list.append("蓄冷水罐模型，蓄冷工况，阀门和水泵全开，水力特性辨识：")
    full_open_result_list.append("冷冻水泵实际总流量" + "\t" + "冷冻水泵额定总流量" + "\t" + "冷冻水泵流量比例" + "\t" +
                                 "大冷水机实际总流量" + "\t" + "小冷水机实际总流量" + "\t" + "冷水机实际流量分配比例" + "\t" +
                                 "冷冻水泵实际总电功率" + "\t" + "冷冻水泵实际扬程")
    storage_chilled_pump_Fw0_total = n_storage_chilled_pump * storage_chilled_pump_Fw0
    chiller_chilled_pump_data = [0, 0, 0, 0, 0, 0]
    chiller_cooling_pump_data = [0, 0, 0, 0, 0, 0]
    chiller_chilled_value_data = [1, 1, 1, 1, 1, 1]
    chiller_cooling_value_data = [0, 0, 0, 0, 0, 0]
    chiller_tower_value_data = [0, 0, 0, 0, 0, 0]
    chiller_tower_chilled_value_data = [0, 0]
    chiller_user_value_data = [0, 0]
    storage_chilled_pump_data = [storage_chilled_pump_f0, storage_chilled_pump_f0,
                                 storage_chilled_pump_f0, storage_chilled_pump_f0]
    storage_user_value_data = [0, 0, 0]
    storage_chiller_value_data = [1, 1, 1]
    model_input_data = time_data + environment_input_data_default() + chiller_data + \
                       chiller_chilled_pump_data + chiller_cooling_pump_data + \
                       chiller_cooling_tower_data + chiller_chilled_value_data + \
                       chiller_cooling_value_data + chiller_tower_value_data + \
                       chiller_tower_chilled_value_data + chiller_user_value_data + \
                       air_source_heat_pump_input_data_default() + storage_chilled_pump_data + \
                       storage_user_value_data + storage_chiller_value_data + \
                       tower_chilled_input_data_default() + user_load_input_data_default()
    try:
        time1 = time.time()
        print("正在进行：蓄冷水罐模型，蓄冷工况，阀门和水泵全开，水力特性辨识！")
        result = simulate_sample(fmu_unzipdir, fmu_description, None, start_time, stop_time,
                                 model_input_data, model_input_type, model_output_name,
                                 output_interval, time_out, False, False)
        # 获取仿真结果
        # 冷水机组流量
        chiller_Few_big_total = result['chiller_Few_big'][-1]
        chiller_Few_small_total = result['chiller_Few_small'][-1]
        chiller_Few_big = chiller_Few_big_total / n_chiller1
        chiller_Few_small = chiller_Few_small_total / n_chiller2
        # 水泵组流量
        Few_total_from_chiller = result['storage_Few_total_from_chiller'][-1]
        chilled_pump_H = result['storage_H_chilled_pump'][-1]
        chilled_pump_P_total = result['storage_P_total_chilled_pump'][-1]
        # 仿真结果生成txt
        tmp_txt = str(np.round(Few_total_from_chiller, 2)) + "\t" + \
                  str(np.round(storage_chilled_pump_Fw0_total, 2)) + "\t" + \
                  str(np.round(Few_total_from_chiller / storage_chilled_pump_Fw0_total, 4)) + "\t" + \
                  str(np.round(chiller_Few_big_total, 2)) + "\t" + str(np.round(chiller_Few_small_total, 2)) + "\t" + \
                  str(np.round(chiller_Few_big / chiller_Few_small, 4)) + "\t" + \
                  str(np.round(chilled_pump_P_total, 2)) + "\t" + str(np.round(chilled_pump_H, 2)) + "\n"
        full_open_result_list.append(tmp_txt)
        time2 = time.time()
        time_cost = np.round(time2 - time1, 2)
        print("本次仿真计算用时(秒)：" + str(time_cost) + "\n")
    except:
        print("FMU仿真失败：蓄冷水罐模型，蓄冷工况，阀门和水泵全开，水力特性辨识！")
        print(traceback.format_exc() + "\n")

    # 蓄冷水罐模型，向用户侧供冷工况，阀门和水泵全开
    full_open_result_list.append("蓄冷水罐模型，向用户侧供冷工况，阀门和水泵全开，水力特性辨识：")
    full_open_result_list.append("冷冻水泵实际总流量" + "\t" + "冷冻水泵额定总流量" + "\t" + "冷冻水泵流量比例" + "\t" +
                                 "冷冻水泵实际总电功率" + "\t" + "冷冻水泵实际扬程")
    storage_chilled_pump_Fw0_total = n_storage_chilled_pump * storage_chilled_pump_Fw0
    storage_chilled_pump_data = [storage_chilled_pump_f0, storage_chilled_pump_f0,
                                 storage_chilled_pump_f0, storage_chilled_pump_f0]
    storage_user_value_data = [1, 1, 1]
    storage_chiller_value_data = [0, 0, 0]
    model_input_data = time_data + environment_input_data_default() + chiller_input_data_default() + \
                       air_source_heat_pump_input_data_default() + storage_chilled_pump_data + \
                       storage_user_value_data + storage_chiller_value_data + \
                       tower_chilled_input_data_default() + user_load_input_data_default()
    try:
        time1 = time.time()
        print("正在进行：蓄冷水罐模型，向用户侧供冷工况，阀门和水泵全开，水力特性辨识！")
        result = simulate_sample(fmu_unzipdir, fmu_description, None, start_time, stop_time, model_input_data,
                                 model_input_type, model_output_name, output_interval, time_out, False, False)
        # 获取仿真结果
        Few_total_to_user = result['storage_Few_total_to_user'][-1]
        chilled_pump_H = result['storage_H_chilled_pump'][-1]
        chilled_pump_P_total = result['storage_P_total_chilled_pump'][-1]
        # 仿真结果生成txt
        tmp_txt = str(np.round(Few_total_to_user, 2)) + "\t" + \
                  str(np.round(storage_chilled_pump_Fw0_total, 2)) + "\t" + \
                  str(np.round(Few_total_to_user / storage_chilled_pump_Fw0_total, 4)) + "\t" + \
                  str(np.round(chilled_pump_P_total, 2)) + "\t" + str(np.round(chilled_pump_H, 2)) + "\n"
        full_open_result_list.append(tmp_txt)
        time2 = time.time()
        time_cost = np.round(time2 - time1, 2)
        print("本次仿真计算用时(秒)：" + str(time_cost) + "\n")
    except:
        print("FMU仿真失败：蓄冷水罐模型，向用户侧供冷工况，阀门和水泵全开，水力特性辨识！")
        print(traceback.format_exc() + "\n")

    # 冷却塔直接供冷模型，向用户侧供冷，阀门和水泵全开
    full_open_result_list.append("冷却塔直接供冷模型，向用户侧供冷，阀门和水泵全开，水力特性辨识：")
    full_open_result_list.append("冷冻水泵实际总流量" + "\t" + "冷冻水泵额定总流量" + "\t" + "冷冻水泵流量比例" + "\t" +
                                 "冷冻水泵实际总电功率" + "\t" + "冷冻水泵实际扬程")
    tower_chilled_pump_Fw0_total = n_tower_chilled_pump * tower_chilled_pump_Fw0
    chiller_chilled_pump_data = [0, 0, 0, 0, 0, 0]
    chiller_cooling_pump_data = [0, 0, 0, 0, 0, 0]
    chiller_chilled_value_data = [0, 0, 0, 0, 0, 0]
    chiller_cooling_value_data = [0, 0, 0, 0, 0, 0]
    chiller_tower_value_data = [1, 1, 1, 1, 1, 1]
    chiller_tower_chilled_value_data = [1, 1]
    chiller_user_value_data = [0, 0]
    tower_chilled_pump_data = [tower_chilled_pump_f0, tower_chilled_pump_f0, tower_chilled_pump_f0, tower_chilled_pump_f0]
    model_input_data = time_data + environment_input_data_default() + chiller_data + \
                       chiller_chilled_pump_data + chiller_cooling_pump_data + \
                       chiller_cooling_tower_data + chiller_chilled_value_data + \
                       chiller_cooling_value_data + chiller_tower_value_data + \
                       chiller_tower_chilled_value_data + chiller_user_value_data + \
                       air_source_heat_pump_input_data_default() + cold_storage_input_data_default() + \
                       tower_chilled_pump_data + user_load_input_data_default()
    try:
        time1 = time.time()
        print("正在进行：冷却塔直接供冷模型，向用户侧供冷，阀门和水泵全开，水力特性辨识！")
        result = simulate_sample(fmu_unzipdir, fmu_description, None, start_time, stop_time,
                                 model_input_data, model_input_type, model_output_name, output_interval,
                                 time_out, False, False)
        # 获取仿真结果
        Few_total = result['tower_chilled_Few_total'][-1]
        chilled_pump_H = result['tower_chilled_H_chilled_pump'][-1]
        chilled_pump_P_total = result['tower_chilled_P_total_chilled_pump'][-1]
        # 仿真结果生成txt
        tmp_txt = str(np.round(Few_total, 2)) + "\t" + str(np.round(tower_chilled_pump_Fw0_total, 2)) + "\t" + \
                  str(np.round(Few_total / tower_chilled_pump_Fw0_total, 4)) + "\t" + \
                  str(np.round(chilled_pump_P_total, 2)) + "\t" + str(np.round(chilled_pump_H, 2)) + "\n"
        full_open_result_list.append(tmp_txt)
        time2 = time.time()
        time_cost = np.round(time2 - time1, 2)
        print("本次仿真计算用时(秒)：" + str(time_cost) + "\n")
    except:
        print("FMU仿真失败：冷却塔直接供冷模型，向用户侧供冷，阀门和水泵全开，水力特性辨识！")
        print(traceback.format_exc() + "\n")

    # 用户负荷模型，循环泵，阀门和水泵全开
    full_open_result_list.append("用户负荷模型，循环泵，阀门和水泵全开，水力特性辨识：")
    full_open_result_list.append("冷冻水泵实际总流量" + "\t" + "冷冻水泵额定总流量" + "\t" + "冷冻水泵流量比例" + "\t" +
                                 "冷冻水泵实际总电功率" + "\t" + "冷冻水泵实际扬程")
    user_chilled_pump_Fw0_total = chiller_chilled_pump_Fw0_total + ashp_chilled_pump_Fw0_total + \
                                  storage_chilled_pump_Fw0_total
    model_input_data = time_data + main_input_data_default()
    try:
        time1 = time.time()
        print("正在进行：用户负荷模型，循环泵，阀门和水泵全开，水力特性辨识！")
        result = simulate_sample(fmu_unzipdir, fmu_description, None, start_time, stop_time,
                                 model_input_data, model_input_type, model_output_name, output_interval,
                                 time_out, False, False)
        # 获取仿真结果
        Few_total = result['user_Few_total'][-1]
        chilled_pump_H = result['user_H_chilled_pump'][-1]
        chilled_pump_P_total = result['user_P_total_chilled_pump'][-1]
        # 仿真结果生成txt
        tmp_txt = str(np.round(Few_total, 2)) + "\t" + str(np.round(user_chilled_pump_Fw0_total, 2)) + "\t" + \
                  str(np.round(Few_total / user_chilled_pump_Fw0_total, 4)) + "\t" + \
                  str(np.round(chilled_pump_P_total, 2)) + "\t" + str(np.round(chilled_pump_H, 2)) + "\n"
        full_open_result_list.append(tmp_txt)
        time2 = time.time()
        time_cost = np.round(time2 - time1, 2)
        print("本次仿真计算用时(秒)：" + str(time_cost) + "\n")
    except:
        print("FMU仿真失败：用户负荷模型，循环泵，阀门和水泵全开，水力特性辨识！")
        print(traceback.format_exc() + "\n")

    # 冷水机+空气源热泵+蓄冷水罐，向用户侧供冷，阀门和水泵全开
    full_open_result_list.append("冷水机+空气源热泵+蓄冷水罐，向用户侧供冷，阀门和水泵全开，水力特性辨识：")
    full_open_result_list.append("系统实际总流量" + "\t" + "系统额定总流量" + "\t" + "系统流量比例" + "\t" +
                                 "大冷水机实际总流量" + "\t" + "小冷水机实际总流量" + "\t" + "冷水机实际流量分配比例" + "\t" +
                                 "冷水机冷冻水泵实际总流量" + "\t" + "冷水机冷冻水泵额定总流量" + "\t" + "冷水机冷冻水泵流量比例" + "\t" +
                                 "冷水机大冷冻水泵实际总流量" + "\t" + "冷水机大冷冻水泵额定总流量" + "\t" + "冷水机大冷冻水泵流量比例" + "\t" +
                                 "冷水机小冷冻水泵实际总流量" + "\t" + "冷水机小冷冻水泵额定总流量" + "\t" + "冷水机小冷冻水泵流量比例" + "\t" +
                                 "冷水机大冷冻水泵实际总电功率" + "\t" + "冷水机小冷冻水泵实际总电功率" + "\t" + "冷水机冷冻水泵实际扬程" + "\t" +
                                 "空气源热泵冷冻水泵实际总流量" + "\t" + "空气源热泵冷冻水泵额定总流量" + "\t" + "空气源热泵冷冻水泵流量比例" + "\t" +
                                 "空气源热泵冷冻水泵实际总电功率" + "\t" + "空气源热泵冷冻水泵实际扬程" + "\t" +
                                 "蓄冷水罐冷冻水泵实际总流量" + "\t" + "蓄冷水罐冷冻水泵额定总流量" + "\t" + "蓄冷水罐冷冻水泵流量比例" + "\t" +
                                 "蓄冷水罐冷冻水泵实际总电功率" + "\t" + "蓄冷水罐冷冻水泵实际扬程")
    Few0_total = chiller_chilled_pump_Fw0_total + ashp_chilled_pump_Fw0_total + storage_chilled_pump_Fw0_total
    chiller_chilled_pump_data = [chiller1_chilled_pump_f0, chiller1_chilled_pump_f0, chiller1_chilled_pump_f0,
                                 chiller1_chilled_pump_f0, chiller2_chilled_pump_f0, chiller2_chilled_pump_f0]
    chiller_cooling_pump_data = [0, 0, 0, 0, 0, 0]
    chiller_chilled_value_data = [1, 1, 1, 1, 1, 1]
    chiller_cooling_value_data = [0, 0, 0, 0, 0, 0]
    chiller_tower_value_data = [0, 0, 0, 0, 0, 0]
    chiller_tower_chilled_value_data = [0, 0]
    chiller_user_value_data = [1, 1]
    ashp_chilled_pump_data = [ashp_chilled_pump_f0, ashp_chilled_pump_f0, ashp_chilled_pump_f0, ashp_chilled_pump_f0]
    ashp_chilled_value_data = [1, 1, 1, 1]
    storage_chilled_pump_data = [storage_chilled_pump_f0, storage_chilled_pump_f0,
                                 storage_chilled_pump_f0, storage_chilled_pump_f0]
    storage_user_value_data = [1, 1, 1]
    storage_chiller_value_data = [0, 0, 0]
    model_input_data = time_data + environment_input_data_default() + chiller_data + \
                       chiller_chilled_pump_data + chiller_cooling_pump_data + \
                       chiller_cooling_tower_data + chiller_chilled_value_data + \
                       chiller_cooling_value_data + chiller_tower_value_data + \
                       chiller_tower_chilled_value_data + chiller_user_value_data + \
                       air_source_heat_pump_data + ashp_chilled_pump_data + ashp_chilled_value_data + \
                       storage_chilled_pump_data + storage_user_value_data + storage_chiller_value_data + \
                       tower_chilled_input_data_default() + user_load_input_data_default()
    try:
        time1 = time.time()
        print("正在进行：冷水机+空气源热泵+蓄冷水罐，向用户侧供冷，阀门和水泵全开，水力特性辨识！")
        result = simulate_sample(fmu_unzipdir, fmu_description, None, start_time, stop_time,
                                 model_input_data, model_input_type, model_output_name,
                                 output_interval, time_out, False, False)
        # 获取仿真结果
        # 冷水机总流量=冷水机冷冻水泵总流量
        chiller_Few_total = result['chiller_Few_total'][-1]
        # 冷水机组流量
        chiller_Few_big_total = result['chiller_Few_big'][-1]
        chiller_Few_small_total = result['chiller_Few_small'][-1]
        # 冷水机冷冻水泵组流量
        chiller_chilled_pump_Few_small_total = result['chiller_Few_chilled_pump_small'][-1]
        chiller_chilled_pump_Few_big_total = chiller_Few_total - chiller_chilled_pump_Few_small_total
        chiller_chilled_pump_H = result['chiller_H_chilled_pump'][-1]
        chiller_chilled_pump_P_big_total = result['chiller_P_big_chilled_pump'][-1]
        chiller_chilled_pump_P_small_total = result['chiller_P_small_chilled_pump'][-1]
        # 空气源热泵数据
        ashp_Few_total = result['ashp_Few_total'][-1]
        ashp_chilled_pump_H = result['ashp_H_chilled_pump'][-1]
        ashp_chilled_pump_P_total = result['ashp_P_total_chilled_pump'][-1]
        # 蓄冷水罐数据
        storage_Few_total_to_user = result['storage_Few_total_to_user'][-1]
        storage_chilled_pump_H = result['storage_H_chilled_pump'][-1]
        storage_chilled_pump_P_total = result['storage_P_total_chilled_pump'][-1]
        # 总流量
        Few_total = chiller_Few_total + ashp_Few_total + storage_Few_total_to_user
        # 仿真结果生成txt
        tmp_txt = str(np.round(Few_total, 2)) + "\t" + str(np.round(Few0_total, 2)) + "\t" + \
                  str(np.round(Few_total / Few0_total, 4)) + "\t" + \
                  str(np.round(chiller_Few_big_total, 2)) + "\t" + str(np.round(chiller_Few_small_total, 2)) + "\t" + \
                  str(np.round(chiller_Few_big_total / chiller_Few_small_total, 4)) + "\t" + \
                  str(np.round(chiller_Few_total, 2)) + "\t" + \
                  str(np.round(chiller_chilled_pump_Fw0_total, 2)) + "\t" + \
                  str(np.round(chiller_Few_total / chiller_chilled_pump_Fw0_total, 4)) + "\t" + \
                  str(np.round(chiller_chilled_pump_Few_big_total, 2)) + "\t" + \
                  str(np.round(chiller_chilled_pump1_Fw0_total, 2)) + "\t" + \
                  str(np.round(chiller_chilled_pump_Few_big_total / chiller_chilled_pump1_Fw0_total, 4)) + "\t" + \
                  str(np.round(chiller_chilled_pump_Few_small_total, 2)) + "\t" + \
                  str(np.round(chiller_chilled_pump2_Fw0_total, 2)) + "\t" + \
                  str(np.round(chiller_chilled_pump_Few_small_total / chiller_chilled_pump2_Fw0_total, 4)) + "\t" + \
                  str(np.round(chiller_chilled_pump_P_big_total, 2)) + "\t" + \
                  str(np.round(chiller_chilled_pump_P_small_total, 2)) + "\t" + \
                  str(np.round(chiller_chilled_pump_H, 2)) + "\t" + \
                  str(np.round(ashp_Few_total, 2)) + "\t" + str(np.round(ashp_chilled_pump_Fw0_total, 2)) + "\t" + \
                  str(np.round(ashp_Few_total / ashp_chilled_pump_Fw0_total, 4)) + "\t" + \
                  str(np.round(ashp_chilled_pump_P_total, 2)) + "\t" + str(np.round(ashp_chilled_pump_H, 2)) + "\t" + \
                  str(np.round(storage_Few_total_to_user, 2)) + "\t" + \
                  str(np.round(storage_chilled_pump_Fw0_total, 2)) + "\t" + \
                  str(np.round(storage_Few_total_to_user / storage_chilled_pump_Fw0_total, 4)) + "\t" + \
                  str(np.round(storage_chilled_pump_P_total, 2)) + "\t" + \
                  str(np.round(storage_chilled_pump_H, 2)) + "\n"
        full_open_result_list.append(tmp_txt)
        time2 = time.time()
        time_cost = np.round(time2 - time1, 2)
        print("本次仿真计算用时(秒)：" + str(time_cost) + "\n")
    except:
        print("FMU仿真失败：冷水机+空气源热泵+蓄冷水罐，向用户侧供冷，阀门和水泵全开，水力特性辨识！")
        print(traceback.format_exc() + "\n")

    # 冷水机+空气源热泵，向用户侧供冷，阀门和水泵全开
    full_open_result_list.append("冷水机+空气源热泵，向用户侧供冷，阀门和水泵全开，水力特性辨识：")
    full_open_result_list.append("系统实际总流量" + "\t" + "系统额定总流量" + "\t" + "系统流量比例" + "\t" +
                                 "大冷水机实际总流量" + "\t" + "小冷水机实际总流量" + "\t" + "冷水机实际流量分配比例" + "\t" +
                                 "冷水机冷冻水泵实际总流量" + "\t" + "冷水机冷冻水泵额定总流量" + "\t" + "冷水机冷冻水泵流量比例" + "\t" +
                                 "冷水机大冷冻水泵实际总流量" + "\t" + "冷水机大冷冻水泵额定总流量" + "\t" + "冷水机大冷冻水泵流量比例" + "\t" +
                                 "冷水机小冷冻水泵实际总流量" + "\t" + "冷水机小冷冻水泵额定总流量" + "\t" + "冷水机小冷冻水泵流量比例" + "\t" +
                                 "冷水机大冷冻水泵实际总电功率" + "\t" + "冷水机小冷冻水泵实际总电功率" + "\t" + "冷水机冷冻水泵实际扬程" + "\t" +
                                 "空气源热泵冷冻水泵实际总流量" + "\t" + "空气源热泵冷冻水泵额定总流量" + "\t" + "空气源热泵冷冻水泵流量比例" + "\t" +
                                 "空气源热泵冷冻水泵实际总电功率" + "\t" + "空气源热泵冷冻水泵实际扬程")
    Few0_total = chiller_chilled_pump_Fw0_total + ashp_chilled_pump_Fw0_total
    chiller_chilled_pump_data = [chiller1_chilled_pump_f0, chiller1_chilled_pump_f0, chiller1_chilled_pump_f0,
                                 chiller1_chilled_pump_f0, chiller2_chilled_pump_f0, chiller2_chilled_pump_f0]
    chiller_cooling_pump_data = [0, 0, 0, 0, 0, 0]
    chiller_chilled_value_data = [1, 1, 1, 1, 1, 1]
    chiller_cooling_value_data = [0, 0, 0, 0, 0, 0]
    chiller_tower_value_data = [0, 0, 0, 0, 0, 0]
    chiller_tower_chilled_value_data = [0, 0]
    chiller_user_value_data = [1, 1]
    ashp_chilled_pump_data = [ashp_chilled_pump_f0, ashp_chilled_pump_f0, ashp_chilled_pump_f0, ashp_chilled_pump_f0]
    ashp_chilled_value_data = [1, 1, 1, 1]
    model_input_data = time_data + environment_input_data_default() + chiller_data + \
                       chiller_chilled_pump_data + chiller_cooling_pump_data + \
                       chiller_cooling_tower_data + chiller_chilled_value_data + \
                       chiller_cooling_value_data + chiller_tower_value_data + \
                       chiller_tower_chilled_value_data + chiller_user_value_data + \
                       air_source_heat_pump_data + ashp_chilled_pump_data + ashp_chilled_value_data + \
                       cold_storage_input_data_default() + tower_chilled_input_data_default() + \
                       user_load_input_data_default()
    try:
        time1 = time.time()
        print("正在进行：冷水机+空气源热泵，向用户侧供冷，阀门和水泵全开，水力特性辨识！")
        result = simulate_sample(fmu_unzipdir, fmu_description, None, start_time, stop_time,
                                 model_input_data, model_input_type, model_output_name,
                                 output_interval, time_out, False, False)
        # 获取仿真结果
        # 冷水机总流量=冷水机冷冻水泵总流量
        chiller_Few_total = result['chiller_Few_total'][-1]
        # 冷水机组流量
        chiller_Few_big_total = result['chiller_Few_big'][-1]
        chiller_Few_small_total = result['chiller_Few_small'][-1]
        # 冷水机冷冻水泵组流量
        chiller_chilled_pump_Few_small_total = result['chiller_Few_chilled_pump_small'][-1]
        chiller_chilled_pump_Few_big_total = chiller_Few_total - chiller_chilled_pump_Few_small_total
        chiller_chilled_pump_H = result['chiller_H_chilled_pump'][-1]
        chiller_chilled_pump_P_big_total = result['chiller_P_big_chilled_pump'][-1]
        chiller_chilled_pump_P_small_total = result['chiller_P_small_chilled_pump'][-1]
        # 空气源热泵数据
        ashp_Few_total = result['ashp_Few_total'][-1]
        ashp_chilled_pump_H = result['ashp_H_chilled_pump'][-1]
        ashp_chilled_pump_P_total = result['ashp_P_total_chilled_pump'][-1]
        # 总流量
        Few_total = chiller_Few_total + ashp_Few_total
        # 仿真结果生成txt
        tmp_txt = str(np.round(Few_total, 2)) + "\t" + str(np.round(Few0_total, 2)) + "\t" + \
                  str(np.round(Few_total / Few0_total, 4)) + "\t" + \
                  str(np.round(chiller_Few_big_total, 2)) + "\t" + str(np.round(chiller_Few_small_total, 2)) + "\t" + \
                  str(np.round(chiller_Few_big_total / chiller_Few_small_total, 4)) + "\t" + \
                  str(np.round(chiller_Few_total, 2)) + "\t" + \
                  str(np.round(chiller_chilled_pump_Fw0_total, 2)) + "\t" + \
                  str(np.round(chiller_Few_total / chiller_chilled_pump_Fw0_total, 4)) + "\t" + \
                  str(np.round(chiller_chilled_pump_Few_big_total, 2)) + "\t" + \
                  str(np.round(chiller_chilled_pump1_Fw0_total, 2)) + "\t" + \
                  str(np.round(chiller_chilled_pump_Few_big_total / chiller_chilled_pump1_Fw0_total, 4)) + "\t" + \
                  str(np.round(chiller_chilled_pump_Few_small_total, 2)) + "\t" + \
                  str(np.round(chiller_chilled_pump2_Fw0_total, 2)) + "\t" + \
                  str(np.round(chiller_chilled_pump_Few_small_total / chiller_chilled_pump2_Fw0_total, 4)) + "\t" + \
                  str(np.round(chiller_chilled_pump_P_big_total, 2)) + "\t" + \
                  str(np.round(chiller_chilled_pump_P_small_total, 2)) + "\t" + \
                  str(np.round(chiller_chilled_pump_H, 2)) + "\t" + \
                  str(np.round(ashp_Few_total, 2)) + "\t" + str(np.round(ashp_chilled_pump_Fw0_total, 2)) + "\t" + \
                  str(np.round(ashp_Few_total / ashp_chilled_pump_Fw0_total, 4)) + "\t" + \
                  str(np.round(ashp_chilled_pump_P_total, 2)) + "\t" + \
                  str(np.round(ashp_chilled_pump_H, 2)) + "\t" + "\n"
        full_open_result_list.append(tmp_txt)
        time2 = time.time()
        time_cost = np.round(time2 - time1, 2)
        print("本次仿真计算用时(秒)：" + str(time_cost) + "\n")
    except:
        print("FMU仿真失败：冷水机+空气源热泵，向用户侧供冷，阀门和水泵全开，水力特性辨识！")
        print(traceback.format_exc() + "\n")

    # 冷水机+蓄冷水罐，向用户侧供冷，阀门和水泵全开
    full_open_result_list.append("冷水机+蓄冷水罐，向用户侧供冷，阀门和水泵全开，水力特性辨识：")
    full_open_result_list.append("系统实际总流量" + "\t" + "系统额定总流量" + "\t" + "系统流量比例" + "\t" +
                                 "大冷水机实际总流量" + "\t" + "小冷水机实际总流量" + "\t" + "冷水机实际流量分配比例" + "\t" +
                                 "冷水机冷冻水泵实际总流量" + "\t" + "冷水机冷冻水泵额定总流量" + "\t" + "冷水机冷冻水泵流量比例" + "\t" +
                                 "冷水机大冷冻水泵实际总流量" + "\t" + "冷水机大冷冻水泵额定总流量" + "\t" + "冷水机大冷冻水泵流量比例" + "\t" +
                                 "冷水机小冷冻水泵实际总流量" + "\t" + "冷水机小冷冻水泵额定总流量" + "\t" + "冷水机小冷冻水泵流量比例" + "\t" +
                                 "冷水机大冷冻水泵实际总电功率" + "\t" + "冷水机小冷冻水泵实际总电功率" + "\t" + "冷水机冷冻水泵实际扬程" + "\t" +
                                 "蓄冷水罐冷冻水泵实际总流量" + "\t" + "蓄冷水罐冷冻水泵额定总流量" + "\t" + "蓄冷水罐冷冻水泵流量比例" + "\t" +
                                 "蓄冷水罐冷冻水泵实际总电功率" + "\t" + "蓄冷水罐冷冻水泵实际扬程")
    Few0_total = chiller_chilled_pump_Fw0_total + storage_chilled_pump_Fw0_total
    chiller_chilled_pump_data = [chiller1_chilled_pump_f0, chiller1_chilled_pump_f0, chiller1_chilled_pump_f0,
                                 chiller1_chilled_pump_f0, chiller2_chilled_pump_f0, chiller2_chilled_pump_f0]
    chiller_cooling_pump_data = [0, 0, 0, 0, 0, 0]
    chiller_chilled_value_data = [1, 1, 1, 1, 1, 1]
    chiller_cooling_value_data = [0, 0, 0, 0, 0, 0]
    chiller_tower_value_data = [0, 0, 0, 0, 0, 0]
    chiller_tower_chilled_value_data = [0, 0]
    chiller_user_value_data = [1, 1]
    storage_chilled_pump_data = [storage_chilled_pump_f0, storage_chilled_pump_f0,
                                 storage_chilled_pump_f0, storage_chilled_pump_f0]
    storage_user_value_data = [1, 1, 1]
    storage_chiller_value_data = [0, 0, 0]
    model_input_data = time_data + environment_input_data_default() + chiller_data + \
                       chiller_chilled_pump_data + chiller_cooling_pump_data + \
                       chiller_cooling_tower_data + chiller_chilled_value_data + \
                       chiller_cooling_value_data + chiller_tower_value_data + \
                       chiller_tower_chilled_value_data + chiller_user_value_data + \
                       air_source_heat_pump_input_data_default() + \
                       storage_chilled_pump_data + storage_user_value_data + storage_chiller_value_data + \
                       tower_chilled_input_data_default() + user_load_input_data_default()
    try:
        time1 = time.time()
        print("正在进行：冷水机+蓄冷水罐，向用户侧供冷，阀门和水泵全开，水力特性辨识！")
        result = simulate_sample(fmu_unzipdir, fmu_description, None, start_time, stop_time,
                                 model_input_data, model_input_type, model_output_name,
                                 output_interval, time_out, False, False)
        # 获取仿真结果
        # 冷水机总流量=冷水机冷冻水泵总流量
        chiller_Few_total = result['chiller_Few_total'][-1]
        # 冷水机组流量
        chiller_Few_big_total = result['chiller_Few_big'][-1]
        chiller_Few_small_total = result['chiller_Few_small'][-1]
        # 冷水机冷冻水泵组流量
        chiller_chilled_pump_Few_small_total = result['chiller_Few_chilled_pump_small'][-1]
        chiller_chilled_pump_Few_big_total = chiller_Few_total - chiller_chilled_pump_Few_small_total
        chiller_chilled_pump_H = result['chiller_H_chilled_pump'][-1]
        chiller_chilled_pump_P_big_total = result['chiller_P_big_chilled_pump'][-1]
        chiller_chilled_pump_P_small_total = result['chiller_P_small_chilled_pump'][-1]
        # 蓄冷水罐数据
        storage_Few_total_to_user = result['storage_Few_total_to_user'][-1]
        storage_chilled_pump_H = result['storage_H_chilled_pump'][-1]
        storage_chilled_pump_P_total = result['storage_P_total_chilled_pump'][-1]
        # 总流量
        Few_total = chiller_Few_total + storage_Few_total_to_user
        # 仿真结果生成txt
        tmp_txt = str(np.round(Few_total, 2)) + "\t" + str(np.round(Few0_total, 2)) + "\t" + \
                  str(np.round(Few_total / Few0_total, 4)) + "\t" + \
                  str(np.round(chiller_Few_big_total, 2)) + "\t" + str(np.round(chiller_Few_small_total, 2)) + "\t" + \
                  str(np.round(chiller_Few_big_total / chiller_Few_small_total, 4)) + "\t" + \
                  str(np.round(chiller_Few_total, 2)) + "\t" + \
                  str(np.round(chiller_chilled_pump_Fw0_total, 2)) + "\t" + \
                  str(np.round(chiller_Few_total / chiller_chilled_pump_Fw0_total, 4)) + "\t" + \
                  str(np.round(chiller_chilled_pump_Few_big_total, 2)) + "\t" + \
                  str(np.round(chiller_chilled_pump1_Fw0_total, 2)) + "\t" + \
                  str(np.round(chiller_chilled_pump_Few_big_total / chiller_chilled_pump1_Fw0_total, 4)) + "\t" + \
                  str(np.round(chiller_chilled_pump_Few_small_total, 2)) + "\t" + \
                  str(np.round(chiller_chilled_pump2_Fw0_total, 2)) + "\t" + \
                  str(np.round(chiller_chilled_pump_Few_small_total / chiller_chilled_pump2_Fw0_total, 4)) + "\t" + \
                  str(np.round(chiller_chilled_pump_P_big_total, 2)) + "\t" + \
                  str(np.round(chiller_chilled_pump_P_small_total, 2)) + "\t" + \
                  str(np.round(chiller_chilled_pump_H, 2)) + "\t" + \
                  str(np.round(storage_Few_total_to_user, 2)) + "\t" + \
                  str(np.round(storage_chilled_pump_Fw0_total, 2)) + "\t" + \
                  str(np.round(storage_Few_total_to_user / storage_chilled_pump_Fw0_total, 4)) + "\t" + \
                  str(np.round(storage_chilled_pump_P_total, 2)) + "\t" + \
                  str(np.round(storage_chilled_pump_H, 2)) + "\n"
        full_open_result_list.append(tmp_txt)
        time2 = time.time()
        time_cost = np.round(time2 - time1, 2)
        print("本次仿真计算用时(秒)：" + str(time_cost) + "\n")
    except:
        print("FMU仿真失败：冷水机+蓄冷水罐，向用户侧供冷，阀门和水泵全开，水力特性辨识！")
        print(traceback.format_exc() + "\n")

    # 空气源热泵+蓄冷水罐，向用户侧供冷，阀门和水泵全开
    full_open_result_list.append("空气源热泵+蓄冷水罐，向用户侧供冷，阀门和水泵全开，水力特性辨识：")
    full_open_result_list.append("系统实际总流量" + "\t" + "系统额定总流量" + "\t" + "系统流量比例" + "\t" +
                                 "空气源热泵冷冻水泵实际总流量" + "\t" + "空气源热泵冷冻水泵额定总流量" + "\t" + "空气源热泵冷冻水泵流量比例" + "\t" +
                                 "空气源热泵冷冻水泵实际总电功率" + "\t" + "空气源热泵冷冻水泵实际扬程" + "\t" +
                                 "蓄冷水罐冷冻水泵实际总流量" + "\t" + "蓄冷水罐冷冻水泵额定总流量" + "\t" + "蓄冷水罐冷冻水泵流量比例" + "\t" +
                                 "蓄冷水罐冷冻水泵实际总电功率" + "\t" + "蓄冷水罐冷冻水泵实际扬程")
    Few0_total = ashp_chilled_pump_Fw0_total + storage_chilled_pump_Fw0_total
    ashp_chilled_pump_data = [ashp_chilled_pump_f0, ashp_chilled_pump_f0, ashp_chilled_pump_f0, ashp_chilled_pump_f0]
    ashp_chilled_value_data = [1, 1, 1, 1]
    storage_chilled_pump_data = [storage_chilled_pump_f0, storage_chilled_pump_f0,
                                 storage_chilled_pump_f0, storage_chilled_pump_f0]
    storage_user_value_data = [1, 1, 1]
    storage_chiller_value_data = [0, 0, 0]
    model_input_data = time_data + environment_input_data_default() + chiller_input_data_default() + \
                       air_source_heat_pump_data + ashp_chilled_pump_data + ashp_chilled_value_data + \
                       storage_chilled_pump_data + storage_user_value_data + storage_chiller_value_data + \
                       tower_chilled_input_data_default() + user_load_input_data_default()
    try:
        time1 = time.time()
        print("正在进行：空气源热泵+蓄冷水罐，向用户侧供冷，阀门和水泵全开，水力特性辨识！")
        result = simulate_sample(fmu_unzipdir, fmu_description, None, start_time, stop_time,
                                 model_input_data, model_input_type, model_output_name,
                                 output_interval, time_out, False, False)
        # 获取仿真结果
        # 空气源热泵数据
        ashp_Few_total = result['ashp_Few_total'][-1]
        ashp_chilled_pump_H = result['ashp_H_chilled_pump'][-1]
        ashp_chilled_pump_P_total = result['ashp_P_total_chilled_pump'][-1]
        # 蓄冷水罐数据
        storage_Few_total_to_user = result['storage_Few_total_to_user'][-1]
        storage_chilled_pump_H = result['storage_H_chilled_pump'][-1]
        storage_chilled_pump_P_total = result['storage_P_total_chilled_pump'][-1]
        # 总流量
        Few_total = ashp_Few_total + storage_Few_total_to_user
        # 仿真结果生成txt
        tmp_txt = str(np.round(Few_total, 2)) + "\t" + str(np.round(Few0_total, 2)) + "\t" + \
                  str(np.round(Few_total / Few0_total, 4)) + "\t" + \
                  str(np.round(ashp_Few_total, 2)) + "\t" + str(np.round(ashp_chilled_pump_Fw0_total, 2)) + "\t" + \
                  str(np.round(ashp_Few_total / ashp_chilled_pump_Fw0_total, 4)) + "\t" + \
                  str(np.round(ashp_chilled_pump_P_total, 2)) + "\t" + str(np.round(ashp_chilled_pump_H, 2)) + "\t" + \
                  str(np.round(storage_Few_total_to_user, 2)) + "\t" + \
                  str(np.round(storage_chilled_pump_Fw0_total, 2)) + "\t" + \
                  str(np.round(storage_Few_total_to_user / storage_chilled_pump_Fw0_total, 4)) + "\t" + \
                  str(np.round(storage_chilled_pump_P_total, 2)) + "\t" + \
                  str(np.round(storage_chilled_pump_H, 2)) + "\n"
        full_open_result_list.append(tmp_txt)
        time2 = time.time()
        time_cost = np.round(time2 - time1, 2)
        print("本次仿真计算用时(秒)：" + str(time_cost) + "\n")
    except:
        print("FMU仿真失败：空气源热泵+蓄冷水罐，向用户侧供冷，阀门和水泵全开，水力特性辨识！")
        print(traceback.format_exc() + "\n")

    # 结果写入txt
    write_txt_data(full_open_result_txt_path, full_open_result_list)