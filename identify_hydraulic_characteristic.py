import time
from read_write_data import read_cfg_data, write_txt_data
from model_fmu_simulate import simulate_sample
from model_fmu_input_type import *
from model_fmu_input_data_default import *
from model_fmu_output_name import *

def identify_hydraulic_characteristic(fmu_path, start_time, stop_time, output_interval, cfg_path_equipment,
                                      chiller_chilled_result_txt_path, chiller_cooling_result_txt_path,
                                      ashp_chilled_result_txt_path, storage_from_chiller_result_txt_path,
                                      storage_to_user_result_txt_path, tower_chilled_result_txt_path):
    """
    模型水力特性辨识
    
    Args:
        fmu_path: [string]，FMU文件路径
        start_time: [float]，仿真开始时间，单位：秒
        stop_time: [float]，仿真结束时间，单位：秒
        output_interval: [float]，FMU模型输出采样时间，单位：秒
        cfg_path_equipment: [string]，设备信息参数cfg文件路径
        chiller_chilled_result_txt_path: [string]，冷水机冷冻侧水力特性辨识结果，txt文件路径
        chiller_cooling_result_txt_path: [string]，冷水机冷却侧水力特性辨识结果，txt文件路径
        ashp_chilled_result_txt_path: [string]，空气源热泵冷冻侧水力特性辨识结果，txt文件路径
        storage_from_chiller_result_txt_path: [string]，蓄冷水罐蓄冷水力特性辨识结果，txt文件路径
        storage_to_user_result_txt_path: [string]，蓄冷水罐放冷水力特性辨识结果，txt文件路径
        tower_chilled_result_txt_path: [string]，冷却塔直接供冷水力特性辨识结果，txt文件路径

    Returns:

    """
    # 设备装机数量，阀门的数量等于主设备数量
    n_chiller1 = read_cfg_data(cfg_path_equipment, "冷水机1", "n_chiller1", 1)
    n_chiller2 = read_cfg_data(cfg_path_equipment, "冷水机2", "n_chiller2", 1)
    n_chiller_chilled_pump1 = read_cfg_data(cfg_path_equipment, "冷冻水泵_冷水机1", "n_chilled_pump1", 1)
    n_chiller_chilled_pump2 = read_cfg_data(cfg_path_equipment, "冷冻水泵_冷水机2", "n_chilled_pump2", 1)
    n_chiller_cooling_pump1 = read_cfg_data(cfg_path_equipment, "冷却水泵_冷水机1", "n_cooling_pump1", 1)
    n_chiller_cooling_pump2 = read_cfg_data(cfg_path_equipment, "冷却水泵_冷水机2", "n_cooling_pump2", 1)
    n_chiller_cooling_tower = read_cfg_data(cfg_path_equipment, "冷却塔_冷水机", "n_cooling_tower", 1)
    n_air_source_heat_pump = read_cfg_data(cfg_path_equipment, "空气源热泵", "n_air_source_heat_pump", 1)
    n_ashp_chilled_pump = read_cfg_data(cfg_path_equipment, "冷冻水泵_空气源热泵", "n_chilled_pump", 1)
    n_storage_chilled_pump = read_cfg_data(cfg_path_equipment, "冷冻水泵_蓄能装置", "n_chilled_pump", 1)
    n_tower_chilled_pump = read_cfg_data(cfg_path_equipment, "冷冻水泵_冷却塔直接供冷", "n_chilled_pump", 1)

    # 与水力特性辨识无关的模型输入，给定值
    time_data = [start_time]
    chiller_data = [False, False, False, False, False, False, 8]
    chiller_cooling_tower_data = [0, 0, 0, 0, 0, 0]
    air_source_heat_pump_data = [False, False, False, False, 8]
    # 模型输入名称和类型
    model_input_type = main_model_input_type()
    # 模型输出名称
    model_output_name = main_model_output_name()

    # 冷水机模型，冷却水，水力特性测试
    identify_chiller_chilled_side(n_chiller1, n_chiller2, n_chiller_chilled_pump1, n_chiller_chilled_pump2, time_data,
                                  chiller_data, chiller_cooling_tower_data, fmu_path, start_time, stop_time,
                                  model_input_type, model_output_name, output_interval, chiller_chilled_result_txt_path)
    # 冷水机模型，冷却水，水力特性测试
    identify_chiller_cooling_side(n_chiller1, n_chiller2, n_chiller_cooling_pump1, n_chiller_cooling_pump2,
                                  n_chiller_cooling_tower, time_data, chiller_data, chiller_cooling_tower_data,
                                  fmu_path, start_time, stop_time, model_input_type, model_output_name,
                                  output_interval, chiller_cooling_result_txt_path)
    # 空气源热泵模型，冷冻水，水力特性测试
    identify_air_source_heat_pump_chilled_side(n_air_source_heat_pump, n_ashp_chilled_pump, time_data,
                                               air_source_heat_pump_data, fmu_path, start_time, stop_time,
                                               model_input_type, model_output_name, output_interval,
                                               ashp_chilled_result_txt_path)
    # 蓄冷水罐模型，蓄冷工况，水力特性测试
    identify_cold_storage_from_chiller(n_chiller1, n_chiller2, n_storage_chilled_pump, time_data, chiller_data,
                                       chiller_cooling_tower_data, fmu_path, start_time, stop_time, model_input_type,
                                       model_output_name, output_interval, storage_from_chiller_result_txt_path)
    # 蓄冷水罐模型，放冷工况，水力特性测试
    identify_cold_storage_to_user(n_storage_chilled_pump, time_data, fmu_path, start_time, stop_time, model_input_type,
                                  model_output_name, output_interval, storage_to_user_result_txt_path)
    # 冷却塔直接供冷模型，水力特性测试
    identify_tower_chilled(n_chiller_cooling_tower, n_tower_chilled_pump, time_data, chiller_data,
                           chiller_cooling_tower_data, fmu_path, start_time, stop_time, model_input_type,
                           model_output_name, output_interval, tower_chilled_result_txt_path)


def identify_chiller_chilled_side(n_chiller1, n_chiller2, n_chiller_chilled_pump1, n_chiller_chilled_pump2, time_data,
                                  chiller_data, chiller_cooling_tower_data, fmu_path, start_time, stop_time,
                                  model_input_type, model_output_name, output_interval, chiller_chilled_result_txt_path):
    """
    冷水机模型，冷冻水，水力特性测试
    Args:
        n_chiller1: [int]，大冷水机装机台数
        n_chiller2: [int]，小冷水机装机台数
        n_chiller_chilled_pump1: [int]，大冷冻水泵装机台数
        n_chiller_chilled_pump2: [int]，小冷冻水泵装机台数
        time_data: [list]，模型输入数据，时间
        chiller_data: [list]，模型输入数据，冷水机开关及出水温度温度设定
        chiller_cooling_tower_data: [list]，模型输入数据，冷却塔风机转速比
        fmu_path: [string]，FMU文件路径
        start_time: [float]，仿真开始时间，单位：秒
        stop_time: [float]，仿真结束时间，单位：秒
        model_input_type: [list]，模型输入名称和数据类型
        model_output_name: [list]，模型输出名称
        output_interval: [float]，FMU模型输出采样时间，单位：秒
        chiller_chilled_result_txt_path: [string]，仿真结果保存txt文件路径

    Returns:

    """
    # 冷水机模型，冷冻水，水力特性测试
    chiller_chilled_result_list = []
    chiller_chilled_result_list.append("冷水机模型，冷冻侧管道，水力特性辨识：")
    chiller_chilled_result_list.append("大冷冻阀门开启数量" + "\t" + "小冷冻阀门开启数量" + "\t" +
                                       "大冷冻水泵开启数量" + "\t" + "小冷冻水泵开启数量" + "\t" +
                                       "大冷冻水泵单台水流量" + "\t" + "小冷冻水泵单台水流量" + "\t" +
                                       "大冷冻水泵单台电功率" + "\t" + "小冷冻水泵单台电功率" + "\t" + "冷冻水泵扬程")
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
                    chiller_chilled_value_data = []
                    chiller_chilled_pump_data = []
                    if i + j == 0:
                        continue
                    if k + l == 0:
                        continue
                    print("正在进行 冷水机模型 冷冻侧 水力特性辨识：" + "大冷冻阀门开启数量：" + str(i) +
                          "，小冷冻阀门开启数量" + str(j) + "，大冷冻水泵开启数量" + str(k) +
                          "，小冷冻水泵开启数量" + str(l) + "\n")
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
                            chiller_chilled_pump_data.append(1480)
                        else:
                            chiller_chilled_pump_data.append(0)
                    for ll in range(n_chiller_chilled_pump2 + 1)[1:]:
                        if ll <= l:
                            chiller_chilled_pump_data.append(1480)
                        else:
                            chiller_chilled_pump_data.append(0)
                    # 整个模型输入数值
                    model_input_data = time_data + environment_input_data_default() + chiller_data + \
                                       chiller_chilled_pump_data + chiller_cooling_pump_data + \
                                       chiller_cooling_tower_data + chiller_chilled_value_data + \
                                       chiller_cooling_value_data + chiller_tower_value_data + \
                                       chiller_tower_chilled_value_data + chiller_user_value_data + \
                                       air_source_heat_pump_input_data_default() + cold_storage_input_data_default() + \
                                       tower_chilled_input_data_default() + user_load_input_data_default()
                    # FMU仿真
                    try:
                        time1 = time.time()
                        result = simulate_sample(fmu_path, None, start_time, stop_time, model_input_data,
                                                 model_input_type, model_output_name, output_interval, False, False)
                        # 获取仿真结果
                        chiller_Few_big_total = result['chiller_Few_big'][-1]
                        chiller_Few_small_total = result['chiller_Few_small'][-1]
                        chiller_H_chilled_pump = result['chiller_H_chilled_pump'][-1]
                        chiller_chilled_pump_P_big_total = result['chiller_P_big_chilled_pump'][-1]
                        chiller_chilled_pump_P_small_total = result['chiller_P_small_chilled_pump'][-1]
                        # 单台水泵的数据
                        if k == 0:
                            chiller_Few_big = 0
                            chiller_chilled_pump_P_big = 0
                        else:
                            chiller_Few_big = chiller_Few_big_total / k
                            chiller_chilled_pump_P_big = chiller_chilled_pump_P_big_total / k
                        if l == 0:
                            chiller_Few_small = 0
                            chiller_chilled_pump_P_small = 0
                        else:
                            chiller_Few_small = chiller_Few_small_total / l
                            chiller_chilled_pump_P_small = chiller_chilled_pump_P_small_total / l
                        # 仿真结果生成txt
                        tmp_txt = str(i) + "\t" + str(j) + "\t" + str(k) + "\t" + str(l) + "\t" + \
                                  str(chiller_Few_big) + "\t" + str(chiller_Few_small) + "\t" + \
                                  str(chiller_chilled_pump_P_big) + "\t" + str(chiller_chilled_pump_P_small) + "\t" + \
                                  str(chiller_H_chilled_pump)
                        chiller_chilled_result_list.append(tmp_txt)
                        time2 = time.time()
                        time_cost = np.round(time2 - time1, 2)
                        print("本次仿真计算用时(秒)：" + str(time_cost) + "\n")
                    except:
                        print("FMU仿真失败：" + "大冷冻阀门开启数量：" + str(i) + "，小冷冻阀门开启数量" + str(j) +
                              "，大冷冻水泵开启数量" + str(k) + "，小冷冻水泵开启数量" + str(l) + "\n")
                        pass
    # 结果写入txt
    write_txt_data(chiller_chilled_result_txt_path, chiller_chilled_result_list)


def identify_chiller_cooling_side(n_chiller1, n_chiller2, n_chiller_cooling_pump1, n_chiller_cooling_pump2,
                                  n_chiller_cooling_tower, time_data, chiller_data, chiller_cooling_tower_data,
                                  fmu_path, start_time, stop_time, model_input_type, model_output_name,
                                  output_interval, chiller_cooling_result_txt_path):
    """
    冷水机模型，冷却水，水力特性测试
    Args:
        n_chiller1: [int]，大冷水机装机台数
        n_chiller2: [int]，小冷水机装机台数
        n_chiller_cooling_pump1: [int]，大冷却水泵装机台数
        n_chiller_cooling_pump2: [int]，小冷却水泵装机台数
        n_chiller_cooling_tower: [int]，冷却塔装机台数
        time_data: [list]，模型输入数据，时间
        chiller_data: [list]，模型输入数据，冷水机开关及出水温度温度设定
        chiller_cooling_tower_data: [list]，模型输入数据，冷却塔风机转速比
        fmu_path: [string]，FMU文件路径
        start_time: [float]，仿真开始时间，单位：秒
        stop_time: [float]，仿真结束时间，单位：秒
        model_input_type: [list]，模型输入名称和数据类型
        model_output_name: [list]，模型输出名称
        output_interval: [float]，FMU模型输出采样时间，单位：秒
        chiller_cooling_result_txt_path: [string]，仿真结果保存txt文件路径

    Returns:

    """
    # 冷水机模型，冷却水，水力特性测试
    chiller_cooling_result_list = []
    chiller_cooling_result_list.append("冷水机模型，冷却侧管道，水力特性辨识：")
    chiller_cooling_result_list.append("大冷却阀门开启数量" + "\t" + "小冷却阀门开启数量" + "\t" + "冷却塔阀门开启数量" + "\t" +
                                       "大冷却水泵开启数量" + "\t" + "小冷却水泵开启数量" + "\t" +
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
                        chiller_cooling_value_data = []
                        chiller_tower_value_data = []
                        chiller_cooling_pump_data = []
                        if i + j == 0:
                            continue
                        if k == 0:
                            continue
                        if l + m == 0:
                            continue
                        print("正在进行 冷水机模型 冷却侧 水力特性辨识：" + "大冷却阀门开启数量：" + str(i) +
                              "，小冷却阀门开启数量" + str(j) + "，冷却塔阀门开启数量" + str(k) +
                              "，大冷却水泵开启数量" + str(l) + "，小冷却水泵开启数量" + str(m) + "\n")
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
                        for kk in range(n_chiller_cooling_tower)[1:]:
                            if kk <= k:
                                chiller_tower_value_data.append(1)
                            else:
                                chiller_tower_value_data.append(0)
                        for ll in range(n_chiller_cooling_pump1 + 1)[1:]:
                            if ll <= l:
                                chiller_cooling_pump_data.append(1480)
                            else:
                                chiller_cooling_pump_data.append(0)
                        for mm in range(n_chiller_cooling_pump2 + 1)[1:]:
                            if mm <= m:
                                chiller_cooling_pump_data.append(1480)
                            else:
                                chiller_cooling_pump_data.append(0)
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
                            result = simulate_sample(fmu_path, None, start_time, stop_time, model_input_data,
                                                     model_input_type, model_output_name, output_interval,
                                                     False, False)
                            # 获取仿真结果
                            chiller_Fcw_big_total = result['chiller_Fcw_big'][-1]
                            chiller_Fcw_small_total = result['chiller_Fcw_small'][-1]
                            chiller_H_cooling_pump = result['chiller_H_cooling_pump'][-1]
                            chiller_cooling_pump_P_big_total = result['chiller_P_big_cooling_pump'][-1]
                            chiller_cooling_pump_P_small_total = result['chiller_P_small_cooling_pump'][-1]
                            # 单台水泵的数据
                            if l == 0:
                                chiller_Fcw_big = 0
                                chiller_cooling_pump_P_big = 0
                            else:
                                chiller_Fcw_big = chiller_Fcw_big_total / l
                                chiller_cooling_pump_P_big = chiller_cooling_pump_P_big_total / l
                            if m == 0:
                                chiller_Fcw_small = 0
                                chiller_cooling_pump_P_small = 0
                            else:
                                chiller_Fcw_small = chiller_Fcw_small_total / m
                                chiller_cooling_pump_P_small = chiller_cooling_pump_P_small_total / m
                            # 仿真结果生成txt
                            tmp_txt = str(i) + "\t" + str(j) + "\t" + str(k) + "\t" + str(l) + "\t" + str(m) + "\t" + \
                                      str(chiller_Fcw_big) + "\t" + str(chiller_Fcw_small) + "\t" + \
                                      str(chiller_cooling_pump_P_big) + "\t" + \
                                      str(chiller_cooling_pump_P_small) + "\t" + str(chiller_H_cooling_pump)
                            chiller_cooling_result_list.append(tmp_txt)
                            time2 = time.time()
                            time_cost = np.round(time2 - time1, 2)
                            print("本次仿真计算用时(秒)：" + str(time_cost) + "\n")
                        except:
                            print("FMU仿真失败：" + "大冷却阀门开启数量：" + str(i) + "，小冷却阀门开启数量" + str(j) +
                                  "，冷却塔阀门开启数量" + str(k) + "，大冷却水泵开启数量" + str(l) +
                                  "，小冷却水泵开启数量" + str(m) + "\n")
                            pass
    # 结果写入txt
    write_txt_data(chiller_cooling_result_txt_path, chiller_cooling_result_list)


def identify_air_source_heat_pump_chilled_side(n_air_source_heat_pump, n_ashp_chilled_pump, time_data,
                                               air_source_heat_pump_data, fmu_path, start_time, stop_time,
                                               model_input_type, model_output_name, output_interval,
                                               ashp_chilled_result_txt_path):
    """
    空气源热泵模型，冷冻水，水力特性测试
    Args:
        n_air_source_heat_pump: [int]，空气源热泵装机台数
        n_ashp_chilled_pump: [int]，冷冻水泵装机台数
        time_data: [list]，模型输入数据，时间
        air_source_heat_pump_data: [list]，模型输入数据，空气源热泵开关及出水温度温度设定
        fmu_path: [string]，FMU文件路径
        start_time: [float]，仿真开始时间，单位：秒
        stop_time: [float]，仿真结束时间，单位：秒
        model_input_type: [list]，模型输入名称和数据类型
        model_output_name: [list]，模型输出名称
        output_interval: [float]，FMU模型输出采样时间，单位：秒
        ashp_chilled_result_txt_path: [string]，仿真结果保存txt文件路径

    Returns:

    """
    # 空气源热泵模型，冷冻水，水力特性测试
    ashp_chilled_result_list = []
    ashp_chilled_result_list.append("空气源热泵模型，冷冻侧管道，水力特性辨识：")
    ashp_chilled_result_list.append("冷冻阀门开启数量" + "\t" + "冷冻水泵开启数量" + "\t" + "冷冻水泵单台水流量" + "\t" +
                                    "冷冻水泵单台电功率" + "\t" + "冷冻水泵扬程")
    for i in range(n_air_source_heat_pump + 1):
        for j in range(n_ashp_chilled_pump + 1):
            ashp_chilled_value_data = []
            ashp_chilled_pump_data = []
            if i == 0 or j == 0:
                continue
            print("正在进行 空气源热泵模型 冷冻侧 水力特性辨识：" + "冷冻阀门开启数量：" + str(i) +
                  "，冷冻水泵开启数量" + str(j) + "\n")
            # 阀门和水泵输入数值
            for ii in range(n_air_source_heat_pump + 1)[1:]:
                if ii <= i:
                    ashp_chilled_value_data.append(1)
                else:
                    ashp_chilled_value_data.append(0)
            for jj in range(n_ashp_chilled_pump + 1)[1:]:
                if jj <= j:
                    ashp_chilled_pump_data.append(1480)
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
                result = simulate_sample(fmu_path, None, start_time, stop_time, model_input_data, model_input_type,
                                         model_output_name, output_interval, False, False)
                # 获取仿真结果
                ashp_Few_total = result['ashp_Few_total'][-1]
                ashp_H_chilled_pump = result['ashp_H_chilled_pump'][-1]
                ashp_chilled_pump_P_total = result['ashp_P_total_chilled_pump'][-1]
                # 单台水泵的数据
                if j == 0:
                    ashp_Few = 0
                    ashp_chilled_pump_P = 0
                else:
                    ashp_Few = ashp_Few_total / j
                    ashp_chilled_pump_P = ashp_chilled_pump_P_total / j
                # 仿真结果生成txt
                tmp_txt = str(i) + "\t" + str(j) + "\t" + str(ashp_Few) + "\t" + \
                          str(ashp_chilled_pump_P) + "\t" + str(ashp_H_chilled_pump)
                ashp_chilled_result_list.append(tmp_txt)
                time2 = time.time()
                time_cost = np.round(time2 - time1, 2)
                print("本次仿真计算用时(秒)：" + str(time_cost) + "\n")
            except:
                print("FMU仿真失败：" + "冷冻阀门开启数量：" + str(i) + "，冷冻水泵开启数量" + str(j) + "\n")
                pass
    # 结果写入txt
    write_txt_data(ashp_chilled_result_txt_path, ashp_chilled_result_list)


def identify_cold_storage_from_chiller(n_chiller1, n_chiller2, n_storage_chilled_pump, time_data, chiller_data,
                                       chiller_cooling_tower_data, fmu_path, start_time, stop_time, model_input_type,
                                       model_output_name, output_interval, storage_from_chiller_result_txt_path):
    """
    蓄冷水罐模型，蓄冷工况，水力特性测试
    Args:
        n_chiller1: [int]，大冷水机装机台数
        n_chiller2: [int]，小冷水机装机台数
        n_storage_chilled_pump: [int]，冷冻水泵装机台数
        time_data: [list]，模型输入数据，时间
        chiller_data: [list]，模型输入数据，冷水机开关及出水温度温度设定
        chiller_cooling_tower_data: [list]，模型输入数据，冷却塔风机转速比
        fmu_path: [string]，FMU文件路径
        start_time: [float]，仿真开始时间，单位：秒
        stop_time: [float]，仿真结束时间，单位：秒
        model_input_type: [list]，模型输入名称和数据类型
        model_output_name: [list]，模型输出名称
        output_interval: [float]，FMU模型输出采样时间，单位：秒
        storage_from_chiller_result_txt_path: [string]，仿真结果保存txt文件路径

    Returns:

    """
    # 蓄冷水罐模型，蓄冷工况，水力特性测试
    storage_from_chiller_result_list = []
    storage_from_chiller_result_list.append("蓄冷水罐模型，蓄冷工况，水力特性辨识：")
    storage_from_chiller_result_list.append("冷水机大冷冻阀门开启数量" + "\t" + "冷水机小冷冻阀门开启数量" + "\t" +
                                            "蓄冷水罐冷冻水泵开启数量" + "\t" + "蓄冷水罐冷冻水泵单台水流量" + "\t" +
                                            "蓄冷水罐冷冻水泵单台电功率" + "\t" + "蓄冷水罐冷冻水泵扬程")
    # 默认值
    chiller_chilled_pump_data = [0, 0, 0, 0, 0, 0]
    chiller_cooling_pump_data = [0, 0, 0, 0, 0, 0]
    chiller_cooling_value_data = [0, 0, 0, 0, 0, 0]
    chiller_tower_value_data = [0, 0, 0, 0, 0, 0]
    chiller_tower_chilled_value_data = [0, 0]
    chiller_user_value_data = [0, 0]
    storage_user_value_data = [0, 0, 0]
    storage_chiller_value_data = [1, 1, 1]
    for i in range(n_chiller1 + 1):
        for j in range(n_chiller2 + 1):
            for k in range(n_storage_chilled_pump + 1):
                chiller_chilled_value_data = []
                storage_chilled_pump_data = []
                if i + j == 0:
                    continue
                if k == 0:
                    continue
                print("正在进行 蓄冷水罐模型 蓄冷工况 水力特性辨识：" + "冷水机大冷冻阀门开启数量：" + str(i) +
                      "，冷水机小冷冻阀门开启数量" + str(j) + "，蓄冷水罐冷冻水泵开启数量" + str(k) + "\n")
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
                        storage_chilled_pump_data.append(1480)
                    else:
                        storage_chilled_pump_data.append(0)
                # 整个模型输入数值
                model_input_data = time_data + environment_input_data_default() + chiller_data + \
                                   chiller_chilled_pump_data + chiller_cooling_pump_data + \
                                   chiller_cooling_tower_data + chiller_chilled_value_data + \
                                   chiller_cooling_value_data + chiller_tower_value_data + \
                                   chiller_tower_chilled_value_data + chiller_user_value_data + \
                                   air_source_heat_pump_input_data_default() + storage_chilled_pump_data + \
                                   storage_user_value_data + storage_chiller_value_data + \
                                   tower_chilled_input_data_default() + user_load_input_data_default()
                # FMU仿真
                try:
                    time1 = time.time()
                    result = simulate_sample(fmu_path, None, start_time, stop_time, model_input_data, model_input_type,
                                             model_output_name, output_interval, False, False)
                    # 获取仿真结果
                    storage_Few_total_from_chiller = result['storage_Few_total_from_chiller'][-1]
                    storage_H_chilled_pump = result['storage_H_chilled_pump'][-1]
                    storage_P_total_chilled_pump = result['storage_P_total_chilled_pump'][-1]
                    # 单台水泵的数据
                    if k == 0:
                        storage_Few_from_chiller = 0
                        storage_chilled_pump_P = 0
                    else:
                        storage_Few_from_chiller = storage_Few_total_from_chiller / k
                        storage_chilled_pump_P = storage_P_total_chilled_pump / k
                    # 仿真结果生成txt
                    tmp_txt = str(i) + "\t" + str(j) + "\t" + str(k) + "\t" + str(storage_Few_from_chiller) + "\t" + \
                              str(storage_chilled_pump_P) + "\t" + str(storage_H_chilled_pump)
                    storage_from_chiller_result_list.append(tmp_txt)
                    time2 = time.time()
                    time_cost = np.round(time2 - time1, 2)
                    print("本次仿真计算用时(秒)：" + str(time_cost) + "\n")
                except:
                    print("FMU仿真失败：" + "冷水机大冷冻阀门开启数量：" + str(i) + "，冷水机小冷冻阀门开启数量" + str(j) +
                          "，蓄冷水罐冷冻水泵开启数量" + str(k) + "\n")
                    pass
    # 结果写入txt
    write_txt_data(storage_from_chiller_result_txt_path, storage_from_chiller_result_list)


def identify_cold_storage_to_user(n_storage_chilled_pump, time_data, fmu_path, start_time, stop_time, model_input_type,
                                  model_output_name, output_interval, storage_to_user_result_txt_path):
    """
    蓄冷水罐模型，放冷工况，水力特性测试
    Args:
        n_storage_chilled_pump: [int]，冷冻水泵装机台数
        time_data: [list]，模型输入数据，时间
        fmu_path: [string]，FMU文件路径
        start_time: [float]，仿真开始时间，单位：秒
        stop_time: [float]，仿真结束时间，单位：秒
        model_input_type: [list]，模型输入名称和数据类型
        model_output_name: [list]，模型输出名称
        output_interval: [float]，FMU模型输出采样时间，单位：秒
        storage_to_user_result_txt_path: [string]，仿真结果保存txt文件路径

    Returns:

    """
    # 蓄冷水罐模型，放冷工况，水力特性测试
    storage_to_user_result_list = []
    storage_to_user_result_list.append("蓄冷水罐模型，放冷工况，水力特性辨识：")
    storage_to_user_result_list.append("蓄冷水罐冷冻水泵开启数量" + "\t" + "蓄冷水罐冷冻水泵单台水流量" + "\t" +
                                       "蓄冷水罐冷冻水泵单台电功率" + "\t" + "蓄冷水罐冷冻水泵扬程")
    storage_user_value_data = [1, 1, 1]
    storage_chiller_value_data = [0, 0, 0]
    for i in range(n_storage_chilled_pump + 1):
        storage_chilled_pump_data = []
        if i == 0:
            continue
        print("正在进行 蓄冷水罐模型 放冷工况 水力特性辨识：" + "，蓄冷水罐冷冻水泵开启数量" + str(i) + "\n")
        for ii in range(n_storage_chilled_pump + 1)[1:]:
            if ii <= i:
                storage_chilled_pump_data.append(1480)
            else:
                storage_chilled_pump_data.append(0)
        # 整个模型输入数值
        model_input_data = time_data + environment_input_data_default() + chiller_input_data_default() + \
                           air_source_heat_pump_input_data_default() + storage_chilled_pump_data + \
                           storage_user_value_data + storage_chiller_value_data + \
                           tower_chilled_input_data_default() + user_load_input_data_default()
        # FMU仿真
        try:
            time1 = time.time()
            result = simulate_sample(fmu_path, None, start_time, stop_time, model_input_data, model_input_type,
                                     model_output_name, output_interval, False, False)
            # 获取仿真结果
            storage_Few_total_to_user = result['storage_Few_total_to_user'][-1]
            storage_H_chilled_pump = result['storage_H_chilled_pump'][-1]
            storage_P_total_chilled_pump = result['storage_P_total_chilled_pump'][-1]
            # 单台水泵的数据
            if i == 0:
                storage_Few_to_user = 0
                storage_chilled_pump_P = 0
            else:
                storage_Few_to_user = storage_Few_total_to_user / i
                storage_chilled_pump_P = storage_P_total_chilled_pump / i
            # 仿真结果生成txt
            tmp_txt = str(i) + "\t" + str(storage_Few_to_user) + "\t" + str(storage_chilled_pump_P) + "\t" + \
                      str(storage_H_chilled_pump)
            storage_to_user_result_list.append(tmp_txt)
            time2 = time.time()
            time_cost = np.round(time2 - time1, 2)
            print("本次仿真计算用时(秒)：" + str(time_cost) + "\n")
        except:
            print("FMU仿真失败：" + "，蓄冷水罐冷冻水泵开启数量" + str(i) + "\n")
            pass
    # 结果写入txt
    write_txt_data(storage_to_user_result_txt_path, storage_to_user_result_list)


def identify_tower_chilled(n_chiller_cooling_tower, n_tower_chilled_pump, time_data, chiller_data,
                           chiller_cooling_tower_data, fmu_path, start_time, stop_time, model_input_type,
                           model_output_name, output_interval, tower_chilled_result_txt_path):
    """
    冷却塔直接供冷模型，水力特性测试
    Args:
        n_chiller_cooling_tower: [int]，冷却塔装机台数
        n_tower_chilled_pump: [int]，冷冻水泵安装台数
        time_data: [list]，模型输入数据，时间
        chiller_data: [list]，模型输入数据，冷水机开关及出水温度温度设定
        chiller_cooling_tower_data: [list]，模型输入数据，冷却塔风机转速比
        fmu_path: [string]，FMU文件路径
        start_time: [float]，仿真开始时间，单位：秒
        stop_time: [float]，仿真结束时间，单位：秒
        model_input_type: [list]，模型输入名称和数据类型
        model_output_name: [list]，模型输出名称
        output_interval: [float]，FMU模型输出采样时间，单位：秒
        tower_chilled_result_txt_path: [string]，仿真结果保存txt文件路径

    Returns:

    """
    # 冷却塔直接供冷模型，水力特性测试
    tower_chilled_result_list = []
    tower_chilled_result_list.append("冷却塔直接供冷模型，水力特性辨识：")
    tower_chilled_result_list.append("冷水机冷却塔阀门开启数量" + "\t" + "冷却塔直接供冷水泵开启数量" + "\t" +
                                     "冷却塔直接供冷水泵单台水流量" + "\t" + "冷却塔直接供冷水泵单台电功率" + "\t" +
                                     "冷却塔直接供冷水泵扬程")
    # 默认值
    chiller_chilled_pump_data = [0, 0, 0, 0, 0, 0]
    chiller_cooling_pump_data = [0, 0, 0, 0, 0, 0]
    chiller_chilled_value_data = [0, 0, 0, 0, 0, 0]
    chiller_cooling_value_data = [0, 0, 0, 0, 0, 0]
    chiller_tower_chilled_value_data = [1, 1]
    chiller_user_value_data = [0, 0]
    for i in range(n_chiller_cooling_tower + 1):
        for j in range(n_tower_chilled_pump + 1):
            chiller_tower_value_data = []
            tower_chilled_pump_data = []
            if i == 0 or j == 0:
                continue
            print("正在进行 冷却塔直接供冷模型 水力特性辨识：" + "，冷水机冷却塔阀门开启数量" + str(i) +
                  "，冷却塔直接供冷水泵开启数量" + str(j) + "\n")
            for ii in range(n_chiller_cooling_tower)[1:]:
                if ii <= i:
                    chiller_tower_value_data.append(1)
                else:
                    chiller_tower_value_data.append(0)
            for jj in range(n_tower_chilled_pump + 1)[1:]:
                if jj <= j:
                    tower_chilled_pump_data.append(1480)
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
                result = simulate_sample(fmu_path, None, start_time, stop_time, model_input_data, model_input_type,
                                         model_output_name, output_interval, False, False)
                # 获取仿真结果
                tower_chilled_Few_total = result['tower_chilled_Few_total'][-1]
                tower_chilled_H_chilled_pump = result['tower_chilled_H_chilled_pump'][-1]
                tower_chilled_P_total_chilled_pump = result['tower_chilled_P_total_chilled_pump'][-1]
                # 单台水泵的数据
                if j == 0:
                    tower_chilled_Few = 0
                    tower_chilled_pump_P = 0
                else:
                    tower_chilled_Few = tower_chilled_Few_total / j
                    tower_chilled_pump_P = tower_chilled_P_total_chilled_pump / j
                # 仿真结果生成txt
                tmp_txt = str(i) + "\t" + str(j) + "\t" + str(tower_chilled_Few) + "\t" + \
                          str(tower_chilled_pump_P) + "\t" + str(tower_chilled_H_chilled_pump)
                tower_chilled_result_list.append(tmp_txt)
                time2 = time.time()
                time_cost = np.round(time2 - time1, 2)
                print("本次仿真计算用时(秒)：" + str(time_cost) + "\n")
            except:
                print("FMU仿真失败：" + "，冷水机冷却塔阀门开启数量" + str(i) + "，冷却塔直接供冷水泵开启数量" + str(j) + "\n")
                pass
    write_txt_data(tower_chilled_result_txt_path, tower_chilled_result_list)