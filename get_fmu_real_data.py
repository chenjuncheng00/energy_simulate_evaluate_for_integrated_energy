import numpy as np
from algorithm_code import *
from model_fmu_input_type import chiller_input_type, air_source_heat_pump_input_type, cold_storage_input_type, \
                                 tower_chilled_input_type
from model_fmu_output_name import chiller_output_name, air_source_heat_pump_output_name, cold_storage_output_name, \
                                  tower_chilled_output_name

def main_get_fmu_real_data(simulate_result, cfg_path_equipment, txt_path):
    """

    Args:
        simulate_result: [object]，FMU模型仿真结果
        cfg_path_equipment: [string]，设备信息参数cfg文件路径
        txt_path: [string]，相对路径

    Returns:

    """
    # 设备类型名称(air_conditioner,air_source_heat_pump等)，相对路径
    chiller_equipment_type_path = ["chiller", txt_path]
    ashp_equipment_type_path = ["air_source_heat_pump", txt_path]
    storage_equipment_type_path = ["energy_storage_equipment", txt_path]
    tower_chilled_equipment_type_path = ["tower_chilled", txt_path]
    # 获取FMU仿真的结果值
    get_chiller_real_data(simulate_result, chiller_equipment_type_path, cfg_path_equipment)
    get_ashp_real_data(simulate_result, ashp_equipment_type_path, cfg_path_equipment)
    get_storage_real_data(simulate_result, storage_equipment_type_path, cfg_path_equipment)
    get_tower_chilled_real_data(simulate_result, tower_chilled_equipment_type_path, cfg_path_equipment)
    get_user_real_data(simulate_result, txt_path, cfg_path_equipment)
    get_environment_real_data(simulate_result, txt_path, cfg_path_equipment)


def get_Teo_set_real_data(txt_path):
    """
    需要先执行main_get_fmu_real_data()，将各个设备的Teo_set值记录，再计算综合值
    Args:
        txt_path: [string]，相对路径

    Returns:

    """
    equipment_type_list = ["chiller", "air_source_heat_pump"]
    # 计算Teo_set
    calculate_Teo_set_synthesize_value(equipment_type_list, txt_path)


def get_chiller_real_data(simulate_result, equipment_type_path, cfg_path_equipment):
    """
    读取冷水机模型的实际值，并写入txt文件
    Args:
        simulate_result: [object]，FMU模型仿真结果
        equipment_type_path:[string]，[list]，设备类型名称(air_conditioner,air_source_heat_pump等)，相对路径
        cfg_path_equipment:[string]，设备信息参数cfg文件路径

    Returns:

    """
    # 设备实时值
    real_value_DO_dict = dict()
    real_value_DO_dict["real_value"] = dict()
    # input_name
    chiller_input_name_list = get_fmu_input_name(chiller_input_type()[1])
    Teo_set_input_name_list = get_fmu_input_name(chiller_input_type()[2])
    chilled_pump_input_name_list = get_fmu_input_name(chiller_input_type()[3])
    cooling_pump_input_name_list = get_fmu_input_name(chiller_input_type()[4])
    cooling_tower_input_name_list = get_fmu_input_name(chiller_input_type()[5])
    chilled_value_input_name_list = get_fmu_input_name(chiller_input_type()[6])
    cooling_value_input_name_list = get_fmu_input_name(chiller_input_type()[7])
    tower_value_input_name_list = get_fmu_input_name(chiller_input_type()[8])
    tower_chilled_value_input_name_list = get_fmu_input_name(chiller_input_type()[9])
    user_value_input_name_list = get_fmu_input_name(chiller_input_type()[10])
    # output_name
    chiller_P_output_name_list = chiller_output_name()[13]
    chilled_pump_P_output_name_list = chiller_output_name()[14]
    cooling_pump_P_output_name_list = chiller_output_name()[15]
    cooling_tower_P_output_name_list = chiller_output_name()[16]
    chiller_Few_output_name_list = chiller_output_name()[17]
    chiller_Fcw_output_name_list = chiller_output_name()[18]
    # 开关量，开关量，开关量，开关量，开关量
    # 空调主机
    for i in range(len(chiller_input_name_list)):
        DO_status = dict()
        DO_status["DO"] = dict()
        DO_status["DO"]["报警状态"] = 1
        DO_status["DO"]["故障状态"] = 1
        DO_status["DO"]["远方状态"] = 1
        DO_status["DO"]["维修状态"] = 1
        input_tmp = bool(simulate_result[chiller_input_name_list[i]][-1])
        if input_tmp == True:
            DO_status["DO"]["开关状态"] = 1
        else:
            DO_status["DO"]["开关状态"] = 0
        tmp_name = "冷水机_" + str(i)
        real_value_DO_dict["real_value"][tmp_name] = DO_status
    # 冷冻阀门
    for i in range(len(chiller_input_name_list)):
        DO_status = dict()
        DO_status["DO"] = dict()
        DO_status["DO"]["报警状态"] = 1
        DO_status["DO"]["故障状态"] = 1
        DO_status["DO"]["远方状态"] = 1
        DO_status["DO"]["维修状态"] = 1
        input_tmp = int(simulate_result[chilled_value_input_name_list[i]][-1])
        if input_tmp == 1:
            DO_status["DO"]["开关状态"] = 1
        else:
            DO_status["DO"]["开关状态"] = 0
        tmp_name = "冷冻阀门_" + str(i)
        real_value_DO_dict["real_value"][tmp_name] = DO_status
    # 冷却阀门
    for i in range(len(chiller_input_name_list)):
        DO_status = dict()
        DO_status["DO"] = dict()
        DO_status["DO"]["报警状态"] = 1
        DO_status["DO"]["故障状态"] = 1
        DO_status["DO"]["远方状态"] = 1
        DO_status["DO"]["维修状态"] = 1
        input_tmp = int(simulate_result[cooling_value_input_name_list[i]][-1])
        if input_tmp == 1:
            DO_status["DO"]["开关状态"] = 1
        else:
            DO_status["DO"]["开关状态"] = 0
        tmp_name = "冷却阀门_" + str(i)
        real_value_DO_dict["real_value"][tmp_name] = DO_status
    # 一级冷冻水泵
    for i in range(len(chilled_pump_input_name_list)):
        DO_status = dict()
        DO_status["DO"] = dict()
        DO_status["DO"]["报警状态"] = 1
        DO_status["DO"]["故障状态"] = 1
        DO_status["DO"]["远方状态"] = 1
        DO_status["DO"]["维修状态"] = 1
        input_tmp = float(simulate_result[chilled_pump_input_name_list[i]][-1])
        if input_tmp >= 20:
            DO_status["DO"]["开关状态"] = 1
        else:
            DO_status["DO"]["开关状态"] = 0
        tmp_name = "一级冷冻水泵_" + str(i)
        real_value_DO_dict["real_value"][tmp_name] = DO_status
    # 冷却水泵
    for i in range(len(cooling_pump_input_name_list)):
        DO_status = dict()
        DO_status["DO"] = dict()
        DO_status["DO"]["报警状态"] = 1
        DO_status["DO"]["故障状态"] = 1
        DO_status["DO"]["远方状态"] = 1
        DO_status["DO"]["维修状态"] = 1
        input_tmp = float(simulate_result[cooling_pump_input_name_list[i]][-1])
        if input_tmp >= 20:
            DO_status["DO"]["开关状态"] = 1
        else:
            DO_status["DO"]["开关状态"] = 0
        tmp_name = "冷却水泵_" + str(i)
        real_value_DO_dict["real_value"][tmp_name] = DO_status
    # 冷却塔
    for i in range(len(cooling_tower_input_name_list)):
        DO_status = dict()
        DO_status["DO"] = dict()
        DO_status["DO"]["报警状态"] = 1
        DO_status["DO"]["故障状态"] = 1
        DO_status["DO"]["远方状态"] = 1
        DO_status["DO"]["维修状态"] = 1
        input_tmp = float(simulate_result[cooling_tower_input_name_list[i]][-1])
        if input_tmp >= 0.1:
            DO_status["DO"]["开关状态"] = 1
        else:
            DO_status["DO"]["开关状态"] = 0
        tmp_name = "冷却塔_" + str(i)
        real_value_DO_dict["real_value"][tmp_name] = DO_status
    # 冷却塔阀门
    for i in range(len(cooling_tower_input_name_list)):
        DO_status = dict()
        DO_status["DO"] = dict()
        DO_status["DO"]["报警状态"] = 1
        DO_status["DO"]["故障状态"] = 1
        DO_status["DO"]["远方状态"] = 1
        DO_status["DO"]["维修状态"] = 1
        input_tmp = int(simulate_result[tower_value_input_name_list[i]][-1])
        if input_tmp == 1:
            DO_status["DO"]["开关状态"] = 1
        else:
            DO_status["DO"]["开关状态"] = 0
        tmp_name = "冷却塔阀门_" + str(i)
        real_value_DO_dict["real_value"][tmp_name] = DO_status
    # 向用户侧供冷阀门
    for i in range(len(user_value_input_name_list)):
        DO_status = dict()
        DO_status["DO"] = dict()
        DO_status["DO"]["报警状态"] = 1
        DO_status["DO"]["故障状态"] = 1
        DO_status["DO"]["远方状态"] = 1
        DO_status["DO"]["维修状态"] = 1
        input_tmp = int(simulate_result[user_value_input_name_list[i]][-1])
        if input_tmp == 1:
            DO_status["DO"]["开关状态"] = 1
        else:
            DO_status["DO"]["开关状态"] = 0
        tmp_name = "向用户侧供冷阀门_" + str(i)
        real_value_DO_dict["real_value"][tmp_name] = DO_status
    # 冷却塔直接供冷阀门
    for i in range(len(tower_chilled_value_input_name_list)):
        DO_status = dict()
        DO_status["DO"] = dict()
        DO_status["DO"]["报警状态"] = 1
        DO_status["DO"]["故障状态"] = 1
        DO_status["DO"]["远方状态"] = 1
        DO_status["DO"]["维修状态"] = 1
        input_tmp = int(simulate_result[tower_chilled_value_input_name_list[i]][-1])
        if input_tmp == 1:
            DO_status["DO"]["开关状态"] = 1
        else:
            DO_status["DO"]["开关状态"] = 0
        tmp_name = "冷却塔直接供冷阀门_" + str(i)
        real_value_DO_dict["real_value"][tmp_name] = DO_status
    # 设备实时值
    real_value_AO_dict = dict()
    real_value_AO_dict["real_value"] = dict()
    # 模拟量，模拟量，模拟量，模拟量，模拟量
    Teo_set = np.round(float(simulate_result[Teo_set_input_name_list[0]][-1]), 4)
    chiller_Teo = np.round(float(simulate_result["chiller_Teo"][-1]), 4)
    chiller_Tei = np.round(float(simulate_result["chiller_Tei"][-1]), 4)
    chiller_Tco = np.round(float(simulate_result["chiller_Tco"][-1]), 4)
    chiller_Tci = np.round(float(simulate_result["chiller_Tci"][-1]), 4)
    # 空调主机
    for i in range(len(chiller_input_name_list)):
        input_tmp = bool(simulate_result[chiller_input_name_list[i]][-1])
        chiller_name_tmp = "冷水机_" + str(i)
        chiller_consume_name_tmp = "冷水机_电表_" + str(i)
        chiller_Few_name_tmp = "冷水机_冷冻水流量计_" + str(i)
        chiller_Fcw_name_tmp = "冷水机_冷却水流量计_" + str(i)
        real_value_AO_dict["real_value"][chiller_name_tmp] = dict()
        real_value_AO_dict["real_value"][chiller_consume_name_tmp] = dict()
        real_value_AO_dict["real_value"][chiller_Few_name_tmp] = dict()
        real_value_AO_dict["real_value"][chiller_Fcw_name_tmp] = dict()
        real_value_AO_dict["real_value"][chiller_name_tmp]["AO"] = dict()
        real_value_AO_dict["real_value"][chiller_consume_name_tmp]["AO"] = dict()
        real_value_AO_dict["real_value"][chiller_Few_name_tmp]["AO"] = dict()
        real_value_AO_dict["real_value"][chiller_Fcw_name_tmp]["AO"] = dict()
        chiller_P = np.round(float(simulate_result[chiller_P_output_name_list[i]][-1]) / 1000, 4)
        chiller_Few = np.round(float(simulate_result[chiller_Few_output_name_list[i]][-1]) * 3.6, 4)
        chiller_Fcw = np.round(float(simulate_result[chiller_Fcw_output_name_list[i]][-1]) * 3.6, 4)
        real_value_AO_dict["real_value"][chiller_consume_name_tmp]["AO"]["电功率"] = chiller_P
        real_value_AO_dict["real_value"][chiller_Few_name_tmp]["AO"]["流量"] = chiller_Few
        real_value_AO_dict["real_value"][chiller_Fcw_name_tmp]["AO"]["流量"] = chiller_Fcw
        if input_tmp == True:
            real_value_AO_dict["real_value"][chiller_name_tmp]["AO"]["冷冻水出水温度设定值"] = Teo_set
            real_value_AO_dict["real_value"][chiller_name_tmp]["AO"]["冷冻水出水温度"] = chiller_Teo
            real_value_AO_dict["real_value"][chiller_name_tmp]["AO"]["冷冻水回水温度"] = chiller_Tei
            real_value_AO_dict["real_value"][chiller_name_tmp]["AO"]["冷却水出水温度"] = chiller_Tco
            real_value_AO_dict["real_value"][chiller_name_tmp]["AO"]["冷却水回水温度"] = chiller_Tci
        else:
            real_value_AO_dict["real_value"][chiller_name_tmp]["AO"]["冷冻水出水温度设定值"] = 0
            real_value_AO_dict["real_value"][chiller_name_tmp]["AO"]["冷冻水出水温度"] = 0
            real_value_AO_dict["real_value"][chiller_name_tmp]["AO"]["冷冻水回水温度"] = 0
            real_value_AO_dict["real_value"][chiller_name_tmp]["AO"]["冷却水出水温度"] = 0
            real_value_AO_dict["real_value"][chiller_name_tmp]["AO"]["冷却水回水温度"] = 0
    # 一级冷冻水泵
    for i in range(len(chilled_pump_input_name_list)):
        chilled_pump_frequency = np.round(float(simulate_result[chilled_pump_input_name_list[i]][-1]), 4)
        chilled_pump_P = np.round(float(simulate_result[chilled_pump_P_output_name_list[i]][-1]) / 1000, 4)
        chilled_pump_frequency_name_tmp = "一级冷冻水泵_" + str(i)
        chilled_pump_P_name_tmp = "一级冷冻水泵电表_" + str(i)
        real_value_AO_dict["real_value"][chilled_pump_P_name_tmp] = dict()
        real_value_AO_dict["real_value"][chilled_pump_frequency_name_tmp] = dict()
        real_value_AO_dict["real_value"][chilled_pump_P_name_tmp]["AO"] = dict()
        real_value_AO_dict["real_value"][chilled_pump_frequency_name_tmp]["AO"] = dict()
        real_value_AO_dict["real_value"][chilled_pump_P_name_tmp]["AO"]["电功率"] = chilled_pump_P
        real_value_AO_dict["real_value"][chilled_pump_frequency_name_tmp]["AO"]["频率"] = chilled_pump_frequency
    # 冷却水泵
    for i in range(len(cooling_pump_input_name_list)):
        cooling_pump_frequency = np.round(float(simulate_result[cooling_pump_input_name_list[i]][-1]), 4)
        cooling_pump_P = np.round(float(simulate_result[cooling_pump_P_output_name_list[i]][-1]) / 1000, 4)
        cooling_pump_frequency_name_tmp = "冷却水泵_" + str(i)
        cooling_pump_P_name_tmp = "冷却水泵电表_" + str(i)
        real_value_AO_dict["real_value"][cooling_pump_P_name_tmp] = dict()
        real_value_AO_dict["real_value"][cooling_pump_frequency_name_tmp] = dict()
        real_value_AO_dict["real_value"][cooling_pump_P_name_tmp]["AO"] = dict()
        real_value_AO_dict["real_value"][cooling_pump_frequency_name_tmp]["AO"] = dict()
        real_value_AO_dict["real_value"][cooling_pump_P_name_tmp]["AO"]["电功率"] = cooling_pump_P
        real_value_AO_dict["real_value"][cooling_pump_frequency_name_tmp]["AO"]["频率"] = cooling_pump_frequency
    # 冷却塔
    for i in range(len(cooling_tower_input_name_list)):
        cooling_tower_frequency = np.round(float(simulate_result[cooling_tower_input_name_list[i]][-1]) * 50, 4)
        cooling_tower_P = np.round(float(simulate_result[cooling_tower_P_output_name_list[i]][-1]) / 1000, 4)
        cooling_tower_frequency_name_tmp = "冷却塔_" + str(i)
        cooling_tower_P_name_tmp = "冷却塔电表_" + str(i)
        real_value_AO_dict["real_value"][cooling_tower_P_name_tmp] = dict()
        real_value_AO_dict["real_value"][cooling_tower_frequency_name_tmp] = dict()
        real_value_AO_dict["real_value"][cooling_tower_P_name_tmp]["AO"] = dict()
        real_value_AO_dict["real_value"][cooling_tower_frequency_name_tmp]["AO"] = dict()
        real_value_AO_dict["real_value"][cooling_tower_P_name_tmp]["AO"]["电功率"] = cooling_tower_P
        real_value_AO_dict["real_value"][cooling_tower_frequency_name_tmp]["AO"]["频率"] = cooling_tower_frequency
    # 冷冻阀门
    for i in range(len(chiller_input_name_list)):
        input_tmp = int(simulate_result[chilled_value_input_name_list[i]][-1])
        chilled_value_proportion = input_tmp * 100
        chilled_value_name_tmp = "冷冻阀门_" + str(i)
        real_value_AO_dict["real_value"][chilled_value_name_tmp] = dict()
        real_value_AO_dict["real_value"][chilled_value_name_tmp]["AO"] = dict()
        real_value_AO_dict["real_value"][chilled_value_name_tmp]["AO"]["阀门开度"] = chilled_value_proportion
    # 冷却阀门
    for i in range(len(chiller_input_name_list)):
        input_tmp = int(simulate_result[cooling_value_input_name_list[i]][-1])
        cooling_value_proportion = input_tmp * 100
        cooling_value_name_tmp = "冷却阀门_" + str(i)
        real_value_AO_dict["real_value"][cooling_value_name_tmp] = dict()
        real_value_AO_dict["real_value"][cooling_value_name_tmp]["AO"] = dict()
        real_value_AO_dict["real_value"][cooling_value_name_tmp]["AO"]["阀门开度"] = cooling_value_proportion
    # 冷却塔阀门
    for i in range(len(cooling_tower_input_name_list)):
        input_tmp = int(simulate_result[tower_value_input_name_list[i]][-1])
        tower_value_proportion = input_tmp * 100
        tower_value_name_tmp = "冷却塔阀门_" + str(i)
        real_value_AO_dict["real_value"][tower_value_name_tmp] = dict()
        real_value_AO_dict["real_value"][tower_value_name_tmp]["AO"] = dict()
        real_value_AO_dict["real_value"][tower_value_name_tmp]["AO"]["阀门开度"] = tower_value_proportion
    # 向用户侧供冷阀门
    for i in range(len(user_value_input_name_list)):
        input_tmp = int(simulate_result[user_value_input_name_list[i]][-1])
        user_value_proportion = input_tmp * 100
        user_value_name_tmp = "向用户侧供冷阀门_" + str(i)
        real_value_AO_dict["real_value"][user_value_name_tmp] = dict()
        real_value_AO_dict["real_value"][user_value_name_tmp]["AO"] = dict()
        real_value_AO_dict["real_value"][user_value_name_tmp]["AO"]["阀门开度"] = user_value_proportion
    # 冷却塔直接供冷阀门
    for i in range(len(tower_chilled_value_input_name_list)):
        input_tmp = int(simulate_result[tower_chilled_value_input_name_list[i]][-1])
        tower_chilled_value_proportion = input_tmp * 100
        tower_chilled_value_name_tmp = "冷却塔直接供冷阀门_" + str(i)
        real_value_AO_dict["real_value"][tower_chilled_value_name_tmp] = dict()
        real_value_AO_dict["real_value"][tower_chilled_value_name_tmp]["AO"] = dict()
        real_value_AO_dict["real_value"][tower_chilled_value_name_tmp]["AO"]["阀门开度"] = tower_chilled_value_proportion
    # 总管数据
    real_value_AO_dict["real_value"]["冷冻出水总管温度传感器_0"] = dict()
    real_value_AO_dict["real_value"]["冷冻回水总管温度传感器_0"] = dict()
    real_value_AO_dict["real_value"]["冷却出水总管温度传感器_0"] = dict()
    real_value_AO_dict["real_value"]["冷却回水总管温度传感器_0"] = dict()
    real_value_AO_dict["real_value"]["冷冻水总管流量计_0"] = dict()
    real_value_AO_dict["real_value"]["冷却水总管流量计_0"] = dict()
    real_value_AO_dict["real_value"]["冷冻出水总管温度传感器_0"]["AO"] = dict()
    real_value_AO_dict["real_value"]["冷冻回水总管温度传感器_0"]["AO"] = dict()
    real_value_AO_dict["real_value"]["冷却出水总管温度传感器_0"]["AO"] = dict()
    real_value_AO_dict["real_value"]["冷却回水总管温度传感器_0"]["AO"] = dict()
    real_value_AO_dict["real_value"]["冷冻水总管流量计_0"]["AO"] = dict()
    real_value_AO_dict["real_value"]["冷却水总管流量计_0"]["AO"] = dict()
    real_value_AO_dict["real_value"]["冷冻出水总管温度传感器_0"]["AO"]["温度"] = chiller_Teo
    real_value_AO_dict["real_value"]["冷冻回水总管温度传感器_0"]["AO"]["温度"] = chiller_Tei
    real_value_AO_dict["real_value"]["冷却出水总管温度传感器_0"]["AO"]["温度"] = chiller_Tco
    real_value_AO_dict["real_value"]["冷却回水总管温度传感器_0"]["AO"]["温度"] = chiller_Tci
    chiller_Few_total = np.round(float(simulate_result["chiller_Few_total"][-1]), 4)
    chiller_Fcw_total = np.round(float(simulate_result["chiller_Fcw_total"][-1]), 4)
    real_value_AO_dict["real_value"]["冷冻水总管流量计_0"]["AO"]["流量"] = chiller_Few_total
    real_value_AO_dict["real_value"]["冷却水总管流量计_0"]["AO"]["流量"] = chiller_Fcw_total
    # 写入txt
    read_real_value_DO_station(real_value_DO_dict, equipment_type_path, cfg_path_equipment)
    read_real_value_AO_station(real_value_AO_dict, equipment_type_path, cfg_path_equipment)
    # 返回结果
    return real_value_DO_dict, real_value_AO_dict


def get_ashp_real_data(simulate_result, equipment_type_path, cfg_path_equipment):
    """
    读取空气源热泵模型的实际值，并写入txt文件
    Args:
        simulate_result: [object]，FMU模型仿真结果
        equipment_type_path:[string]，[list]，设备类型名称(air_conditioner,air_source_heat_pump等)，相对路径
        cfg_path_equipment:[string]，设备信息参数cfg文件路径

    Returns:

    """
    # 设备实时值
    real_value_DO_dict = dict()
    real_value_DO_dict["real_value"] = dict()
    # input_name
    ashp_input_name_list = get_fmu_input_name(air_source_heat_pump_input_type()[1])
    Teo_set_input_name_list = get_fmu_input_name(air_source_heat_pump_input_type()[2])
    chilled_pump_input_name_list = get_fmu_input_name(air_source_heat_pump_input_type()[3])
    chilled_value_input_name_list = get_fmu_input_name(air_source_heat_pump_input_type()[4])
    # output_name
    ashp_P_output_name_list = air_source_heat_pump_output_name()[8]
    chilled_pump_P_output_name_list = air_source_heat_pump_output_name()[9]
    ashp_Few_output_name_list = air_source_heat_pump_output_name()[10]
    # 开关量，开关量，开关量，开关量，开关量
    # 空调主机
    for i in range(len(ashp_input_name_list)):
        DO_status = dict()
        DO_status["DO"] = dict()
        DO_status["DO"]["报警状态"] = 1
        DO_status["DO"]["故障状态"] = 1
        DO_status["DO"]["远方状态"] = 1
        DO_status["DO"]["维修状态"] = 1
        input_tmp = bool(simulate_result[ashp_input_name_list[i]][-1])
        if input_tmp == True:
            DO_status["DO"]["开关状态"] = 1
        else:
            DO_status["DO"]["开关状态"] = 0
        tmp_name = "空气源热泵_" + str(i)
        real_value_DO_dict["real_value"][tmp_name] = DO_status
    # 冷冻阀门
    for i in range(len(ashp_input_name_list)):
        DO_status = dict()
        DO_status["DO"] = dict()
        DO_status["DO"]["报警状态"] = 1
        DO_status["DO"]["故障状态"] = 1
        DO_status["DO"]["远方状态"] = 1
        DO_status["DO"]["维修状态"] = 1
        input_tmp = int(simulate_result[chilled_value_input_name_list[i]][-1])
        if input_tmp == 1:
            DO_status["DO"]["开关状态"] = 1
        else:
            DO_status["DO"]["开关状态"] = 0
        tmp_name = "冷冻阀门_" + str(i)
        real_value_DO_dict["real_value"][tmp_name] = DO_status
    # 一级冷冻水泵
    for i in range(len(chilled_pump_input_name_list)):
        DO_status = dict()
        DO_status["DO"] = dict()
        DO_status["DO"]["报警状态"] = 1
        DO_status["DO"]["故障状态"] = 1
        DO_status["DO"]["远方状态"] = 1
        DO_status["DO"]["维修状态"] = 1
        input_tmp = float(simulate_result[chilled_pump_input_name_list[i]][-1])
        if input_tmp >= 20:
            DO_status["DO"]["开关状态"] = 1
        else:
            DO_status["DO"]["开关状态"] = 0
        tmp_name = "一级冷冻水泵_" + str(i)
        real_value_DO_dict["real_value"][tmp_name] = DO_status
    # 设备实时值
    real_value_AO_dict = dict()
    real_value_AO_dict["real_value"] = dict()
    # 模拟量，模拟量，模拟量，模拟量，模拟量
    Teo_set = np.round(float(simulate_result[Teo_set_input_name_list[0]][-1]), 4)
    ashp_Teo = np.round(float(simulate_result["ashp_Teo"][-1]), 4)
    ashp_Tei = np.round(float(simulate_result["ashp_Tei"][-1]), 4)
    # 空调主机
    for i in range(len(ashp_input_name_list)):
        input_tmp = bool(simulate_result[ashp_input_name_list[i]][-1])
        ashp_name_tmp = "空气源热泵_" + str(i)
        ashp_consume_name_tmp = "空气源热泵_电表_" + str(i)
        ashp_Few_name_tmp = "空气源热泵_冷冻水流量计_" + str(i)
        real_value_AO_dict["real_value"][ashp_name_tmp] = dict()
        real_value_AO_dict["real_value"][ashp_consume_name_tmp] = dict()
        real_value_AO_dict["real_value"][ashp_Few_name_tmp] = dict()
        real_value_AO_dict["real_value"][ashp_name_tmp]["AO"] = dict()
        real_value_AO_dict["real_value"][ashp_consume_name_tmp]["AO"] = dict()
        real_value_AO_dict["real_value"][ashp_Few_name_tmp]["AO"] = dict()
        ashp_P = np.round(float(simulate_result[ashp_P_output_name_list[i]][-1]) / 1000, 4)
        ashp_Few = np.round(float(simulate_result[ashp_Few_output_name_list[i]][-1]) * 3.6, 4)
        real_value_AO_dict["real_value"][ashp_consume_name_tmp]["AO"]["电功率"] = ashp_P
        real_value_AO_dict["real_value"][ashp_Few_name_tmp]["AO"]["流量"] = ashp_Few
        if input_tmp == True:
            real_value_AO_dict["real_value"][ashp_name_tmp]["AO"]["冷冻水出水温度设定值"] = Teo_set
            real_value_AO_dict["real_value"][ashp_name_tmp]["AO"]["冷冻水出水温度"] = ashp_Teo
            real_value_AO_dict["real_value"][ashp_name_tmp]["AO"]["冷冻水回水温度"] = ashp_Tei
        else:
            real_value_AO_dict["real_value"][ashp_name_tmp]["AO"]["冷冻水出水温度设定值"] = 0
            real_value_AO_dict["real_value"][ashp_name_tmp]["AO"]["冷冻水出水温度"] = 0
            real_value_AO_dict["real_value"][ashp_name_tmp]["AO"]["冷冻水回水温度"] = 0
    # 一级冷冻水泵
    for i in range(len(chilled_pump_input_name_list)):
        chilled_pump_frequency = np.round(float(simulate_result[chilled_pump_input_name_list[i]][-1]), 4)
        chilled_pump_P = np.round(float(simulate_result[chilled_pump_P_output_name_list[i]][-1]) / 1000, 4)
        chilled_pump_frequency_name_tmp = "一级冷冻水泵_" + str(i)
        chilled_pump_P_name_tmp = "一级冷冻水泵电表_" + str(i)
        real_value_AO_dict["real_value"][chilled_pump_P_name_tmp] = dict()
        real_value_AO_dict["real_value"][chilled_pump_frequency_name_tmp] = dict()
        real_value_AO_dict["real_value"][chilled_pump_P_name_tmp]["AO"] = dict()
        real_value_AO_dict["real_value"][chilled_pump_frequency_name_tmp]["AO"] = dict()
        real_value_AO_dict["real_value"][chilled_pump_P_name_tmp]["AO"]["电功率"] = chilled_pump_P
        real_value_AO_dict["real_value"][chilled_pump_frequency_name_tmp]["AO"]["频率"] = chilled_pump_frequency
    # 冷冻阀门
    for i in range(len(ashp_input_name_list)):
        input_tmp = int(simulate_result[chilled_value_input_name_list[i]][-1])
        chilled_value_proportion = input_tmp * 100
        chilled_value_name_tmp = "冷冻阀门_" + str(i)
        real_value_AO_dict["real_value"][chilled_value_name_tmp] = dict()
        real_value_AO_dict["real_value"][chilled_value_name_tmp]["AO"] = dict()
        real_value_AO_dict["real_value"][chilled_value_name_tmp]["AO"]["阀门开度"] = chilled_value_proportion
    # 总管数据
    real_value_AO_dict["real_value"]["冷冻出水总管温度传感器_0"] = dict()
    real_value_AO_dict["real_value"]["冷冻回水总管温度传感器_0"] = dict()
    real_value_AO_dict["real_value"]["冷冻水总管流量计_0"] = dict()
    real_value_AO_dict["real_value"]["冷冻出水总管温度传感器_0"]["AO"] = dict()
    real_value_AO_dict["real_value"]["冷冻回水总管温度传感器_0"]["AO"] = dict()
    real_value_AO_dict["real_value"]["冷冻水总管流量计_0"]["AO"] = dict()
    real_value_AO_dict["real_value"]["冷冻出水总管温度传感器_0"]["AO"]["温度"] = ashp_Teo
    real_value_AO_dict["real_value"]["冷冻回水总管温度传感器_0"]["AO"]["温度"] = ashp_Tei
    ashp_Few_total = np.round(float(simulate_result["ashp_Few_total"][-1]), 4)
    real_value_AO_dict["real_value"]["冷冻水总管流量计_0"]["AO"]["流量"] = ashp_Few_total
    # 写入txt
    read_real_value_DO_station(real_value_DO_dict, equipment_type_path, cfg_path_equipment)
    read_real_value_AO_station(real_value_AO_dict, equipment_type_path, cfg_path_equipment)
    # 返回结果
    return real_value_DO_dict, real_value_AO_dict


def get_storage_real_data(simulate_result, equipment_type_path, cfg_path_equipment):
    """
    读取蓄冷水罐模型的实际值，并写入txt文件
    Args:
        simulate_result: [object]，FMU模型仿真结果
        equipment_type_path:[string]，[list]，设备类型名称(air_conditioner,air_source_heat_pump等)，相对路径
        cfg_path_equipment:[string]，设备信息参数cfg文件路径

    Returns:

    """
    # 设备实时值
    real_value_DO_dict = dict()
    real_value_DO_dict["real_value"] = dict()
    # input_name
    chilled_pump_input_name_list = get_fmu_input_name(cold_storage_input_type()[1])
    chilled_value_in_storage_input_name_list = get_fmu_input_name(cold_storage_input_type()[2])
    chilled_value_to_user_input_name_list = get_fmu_input_name(cold_storage_input_type()[3])
    chilled_value_input_name_list = chilled_value_in_storage_input_name_list + chilled_value_to_user_input_name_list
    # output_name
    chilled_pump_P_output_name_list = cold_storage_output_name()[6]
    # 开关量，开关量，开关量，开关量，开关量
    # 冷冻阀门
    for i in range(len(chilled_value_input_name_list)):
        DO_status = dict()
        DO_status["DO"] = dict()
        DO_status["DO"]["报警状态"] = 1
        DO_status["DO"]["故障状态"] = 1
        DO_status["DO"]["远方状态"] = 1
        DO_status["DO"]["维修状态"] = 1
        input_tmp = int(simulate_result[chilled_value_input_name_list[i]][-1])
        if input_tmp == 1:
            DO_status["DO"]["开关状态"] = 1
        else:
            DO_status["DO"]["开关状态"] = 0
        tmp_name = "冷冻阀门_" + str(i)
        real_value_DO_dict["real_value"][tmp_name] = DO_status
    # 一级冷冻水泵
    for i in range(len(chilled_pump_input_name_list)):
        DO_status = dict()
        DO_status["DO"] = dict()
        DO_status["DO"]["报警状态"] = 1
        DO_status["DO"]["故障状态"] = 1
        DO_status["DO"]["远方状态"] = 1
        DO_status["DO"]["维修状态"] = 1
        input_tmp = float(simulate_result[chilled_pump_input_name_list[i]][-1])
        if input_tmp >= 20:
            DO_status["DO"]["开关状态"] = 1
        else:
            DO_status["DO"]["开关状态"] = 0
        tmp_name = "一级冷冻水泵_" + str(i)
        real_value_DO_dict["real_value"][tmp_name] = DO_status
    # 设备实时值
    real_value_AO_dict = dict()
    real_value_AO_dict["real_value"] = dict()
    # 模拟量，模拟量，模拟量，模拟量，模拟量
    # 一级冷冻水泵
    for i in range(len(chilled_pump_input_name_list)):
        chilled_pump_frequency = np.round(float(simulate_result[chilled_pump_input_name_list[i]][-1]), 4)
        chilled_pump_P = np.round(float(simulate_result[chilled_pump_P_output_name_list[i]][-1]) / 1000, 4)
        chilled_pump_frequency_name_tmp = "一级冷冻水泵_" + str(i)
        chilled_pump_P_name_tmp = "一级冷冻水泵电表_" + str(i)
        real_value_AO_dict["real_value"][chilled_pump_P_name_tmp] = dict()
        real_value_AO_dict["real_value"][chilled_pump_frequency_name_tmp] = dict()
        real_value_AO_dict["real_value"][chilled_pump_P_name_tmp]["AO"] = dict()
        real_value_AO_dict["real_value"][chilled_pump_frequency_name_tmp]["AO"] = dict()
        real_value_AO_dict["real_value"][chilled_pump_P_name_tmp]["AO"]["电功率"] = chilled_pump_P
        real_value_AO_dict["real_value"][chilled_pump_frequency_name_tmp]["AO"]["频率"] = chilled_pump_frequency
    # 冷冻阀门
    for i in range(len(chilled_value_input_name_list)):
        input_tmp = int(simulate_result[chilled_value_input_name_list[i]][-1])
        chilled_value_proportion = input_tmp * 100
        chilled_value_name_tmp = "冷冻阀门_" + str(i)
        real_value_AO_dict["real_value"][chilled_value_name_tmp] = dict()
        real_value_AO_dict["real_value"][chilled_value_name_tmp]["AO"] = dict()
        real_value_AO_dict["real_value"][chilled_value_name_tmp]["AO"]["阀门开度"] = chilled_value_proportion
    # 总管数据
    real_value_AO_dict["real_value"]["冷冻出水总管温度传感器_0"] = dict()
    real_value_AO_dict["real_value"]["冷冻回水总管温度传感器_0"] = dict()
    real_value_AO_dict["real_value"]["冷冻水总管流量计_0"] = dict()
    real_value_AO_dict["real_value"]["冷冻出水总管温度传感器_0"]["AO"] = dict()
    real_value_AO_dict["real_value"]["冷冻回水总管温度传感器_0"]["AO"] = dict()
    real_value_AO_dict["real_value"]["冷冻水总管流量计_0"]["AO"] = dict()
    storage_Teo_from_chiller = np.round(float(simulate_result["chiller_Teo"][-1]), 4)
    storage_Tei_from_chiller = np.round(float(simulate_result["storage_Tei_from_chiller"][-1]), 4)
    storage_Teo_to_user = np.round(float(simulate_result["storage_Teo_to_user"][-1]), 4)
    storage_Tei_to_user = np.round(float(simulate_result["storage_Tei_to_user"][-1]), 4)
    storage_Few_total_from_chiller = np.round(float(simulate_result["storage_Few_total_from_chiller"][-1]), 4)
    storage_Few_total_to_user = np.round(float(simulate_result["storage_Few_total_to_user"][-1]), 4)
    if storage_Few_total_from_chiller > storage_Few_total_to_user:
        real_value_AO_dict["real_value"]["冷冻出水总管温度传感器_0"]["AO"]["温度"] = storage_Teo_from_chiller
        real_value_AO_dict["real_value"]["冷冻回水总管温度传感器_0"]["AO"]["温度"] = storage_Tei_from_chiller
        real_value_AO_dict["real_value"]["冷冻水总管流量计_0"]["AO"]["流量"] = storage_Few_total_from_chiller
    else:
        real_value_AO_dict["real_value"]["冷冻出水总管温度传感器_0"]["AO"]["温度"] = storage_Teo_to_user
        real_value_AO_dict["real_value"]["冷冻回水总管温度传感器_0"]["AO"]["温度"] = storage_Tei_to_user
        real_value_AO_dict["real_value"]["冷冻水总管流量计_0"]["AO"]["流量"] = storage_Few_total_to_user
    # 写入txt
    read_real_value_DO_station(real_value_DO_dict, equipment_type_path, cfg_path_equipment)
    read_real_value_AO_station(real_value_AO_dict, equipment_type_path, cfg_path_equipment)
    # 返回结果
    return real_value_DO_dict, real_value_AO_dict


def get_tower_chilled_real_data(simulate_result, equipment_type_path, cfg_path_equipment):
    """
    读取蓄冷水罐模型的实际值，并写入txt文件
    Args:
        simulate_result: [object]，FMU模型仿真结果
        equipment_type_path:[string]，[list]，设备类型名称(air_conditioner,air_source_heat_pump等)，相对路径
        cfg_path_equipment:[string]，设备信息参数cfg文件路径

    Returns:

    """
    # 设备实时值
    real_value_DO_dict = dict()
    real_value_DO_dict["real_value"] = dict()
    # input_name
    chilled_pump_input_name_list = get_fmu_input_name(tower_chilled_input_type())
    # output_name
    chilled_pump_P_output_name_list = tower_chilled_output_name()[4]
    # 开关量，开关量，开关量，开关量，开关量
    # 一级冷冻水泵
    for i in range(len(chilled_pump_input_name_list)):
        DO_status = dict()
        DO_status["DO"] = dict()
        DO_status["DO"]["报警状态"] = 1
        DO_status["DO"]["故障状态"] = 1
        DO_status["DO"]["远方状态"] = 1
        DO_status["DO"]["维修状态"] = 1
        input_tmp = float(simulate_result[chilled_pump_input_name_list[i]][-1])
        if input_tmp >= 20:
            DO_status["DO"]["开关状态"] = 1
        else:
            DO_status["DO"]["开关状态"] = 0
        tmp_name = "一级冷冻水泵_" + str(i)
        real_value_DO_dict["real_value"][tmp_name] = DO_status
    # 设备实时值
    real_value_AO_dict = dict()
    real_value_AO_dict["real_value"] = dict()
    # 模拟量，模拟量，模拟量，模拟量，模拟量
    # 一级冷冻水泵
    for i in range(len(chilled_pump_input_name_list)):
        chilled_pump_frequency = np.round(float(simulate_result[chilled_pump_input_name_list[i]][-1]), 4)
        chilled_pump_P = np.round(float(simulate_result[chilled_pump_P_output_name_list[i]][-1]) / 1000, 4)
        chilled_pump_frequency_name_tmp = "一级冷冻水泵_" + str(i)
        chilled_pump_P_name_tmp = "一级冷冻水泵电表_" + str(i)
        real_value_AO_dict["real_value"][chilled_pump_P_name_tmp] = dict()
        real_value_AO_dict["real_value"][chilled_pump_frequency_name_tmp] = dict()
        real_value_AO_dict["real_value"][chilled_pump_P_name_tmp]["AO"] = dict()
        real_value_AO_dict["real_value"][chilled_pump_frequency_name_tmp]["AO"] = dict()
        real_value_AO_dict["real_value"][chilled_pump_P_name_tmp]["AO"]["电功率"] = chilled_pump_P
        real_value_AO_dict["real_value"][chilled_pump_frequency_name_tmp]["AO"]["频率"] = chilled_pump_frequency
    # 冷冻水总管
    real_value_AO_dict["real_value"]["冷冻出水总管温度传感器_0"] = dict()
    real_value_AO_dict["real_value"]["冷冻回水总管温度传感器_0"] = dict()
    real_value_AO_dict["real_value"]["冷冻水总管流量计_0"] = dict()
    real_value_AO_dict["real_value"]["冷冻出水总管温度传感器_0"]["AO"] = dict()
    real_value_AO_dict["real_value"]["冷冻回水总管温度传感器_0"]["AO"] = dict()
    real_value_AO_dict["real_value"]["冷冻水总管流量计_0"]["AO"] = dict()
    tower_chilled_Teo_tmp = np.round(float(simulate_result["chiller_Tci"][-1]), 4)
    tower_chilled_Tei_tmp = np.round(float(simulate_result["chiller_Tco"][-1]), 4)
    tower_chilled_Few_tmp = np.round(float(simulate_result["tower_chilled_Few_total"][-1]), 4)
    real_value_AO_dict["real_value"]["冷冻出水总管温度传感器_0"]["AO"]["温度"] = tower_chilled_Teo_tmp
    real_value_AO_dict["real_value"]["冷冻回水总管温度传感器_0"]["AO"]["温度"] = tower_chilled_Tei_tmp
    real_value_AO_dict["real_value"]["冷冻水总管流量计_0"]["AO"]["流量"] = tower_chilled_Few_tmp
    # 写入txt
    read_real_value_DO_station(real_value_DO_dict, equipment_type_path, cfg_path_equipment)
    read_real_value_AO_station(real_value_AO_dict, equipment_type_path, cfg_path_equipment)
    # 返回结果
    return real_value_DO_dict, real_value_AO_dict


def get_environment_real_data(simulate_result, equipment_type_path, cfg_path_equipment):
    """
    读取室外温湿度的实际值，并写入txt文件
    Args:
        simulate_result: [object]，FMU模型仿真结果
        equipment_type_path:[string]，[list]，设备类型名称(air_conditioner,air_source_heat_pump等)，相对路径
        cfg_path_equipment:[string]，设备信息参数cfg文件路径

    Returns:

    """
    # 设备数量
    n_Tdo = read_cfg_data(cfg_path_equipment, "室外环境温湿度传感器", "n_Tdo", 1)
    n_Hro = read_cfg_data(cfg_path_equipment, "室外环境温湿度传感器", "n_Hro", 1)
    # 设备实时值
    real_value_AO_dict = dict()
    real_value_AO_dict["real_value"] = dict()
    real_value_DO_dict = dict()
    real_value_DO_dict["real_value"] = dict()
    # 可能没有天气数据
    try:
        Tdo = round(list(simulate_result["weather_data.TDryBul"])[-1] - 273.15, 4)
        Hro = round(list(simulate_result["weather_data.relHum"])[-1] * 100, 4)
    except:
        Tdo = 35
        Hro = 55
    # 生成字典
    for i in range(n_Tdo):
        Tdo_name_tmp = "室外温度传感器_" + str(i)
        real_value_AO_dict["real_value"][Tdo_name_tmp] = dict()
        real_value_AO_dict["real_value"][Tdo_name_tmp]["AO"] = dict()
        real_value_DO_dict["real_value"][Tdo_name_tmp] = dict()
        real_value_DO_dict["real_value"][Tdo_name_tmp]["DO"] = dict()
        real_value_AO_dict["real_value"][Tdo_name_tmp]["AO"]["温度"] = Tdo
        real_value_DO_dict["real_value"][Tdo_name_tmp]["DO"]["状态"] = 1
    for i in range(n_Hro):
        Hro_name_tmp = "室外湿度传感器_" + str(i)
        real_value_AO_dict["real_value"][Hro_name_tmp] = dict()
        real_value_AO_dict["real_value"][Hro_name_tmp]["AO"] = dict()
        real_value_DO_dict["real_value"][Hro_name_tmp] = dict()
        real_value_DO_dict["real_value"][Hro_name_tmp]["DO"] = dict()
        real_value_AO_dict["real_value"][Hro_name_tmp]["AO"]["湿度"] = Hro
        real_value_DO_dict["real_value"][Hro_name_tmp]["DO"]["状态"] = 1
    # 写入txt
    read_real_value_DO_environment(real_value_DO_dict, equipment_type_path, cfg_path_equipment)
    read_real_value_AO_environment(real_value_AO_dict, equipment_type_path, cfg_path_equipment)
    # 返回结果
    return real_value_DO_dict, real_value_AO_dict


def get_user_real_data(simulate_result, equipment_type_path, cfg_path_equipment):
    """
    读取室内温湿度的实际值，并写入txt文件
    Args:
        simulate_result: [object]，FMU模型仿真结果
        equipment_type_path:[string]，[list]，设备类型名称(air_conditioner,air_source_heat_pump等)，相对路径
        cfg_path_equipment:[string]，设备信息参数cfg文件路径

    Returns:

    """
    # 设备数量
    n_Tdi = read_cfg_data(cfg_path_equipment, "用户末端温湿度传感器", "n_Tdi", 1)
    n_Hri = read_cfg_data(cfg_path_equipment, "用户末端温湿度传感器", "n_Hri", 1)
    n_Te = read_cfg_data(cfg_path_equipment, "用户末端温湿度传感器", "n_Te", 1)
    n_mau = read_cfg_data(cfg_path_equipment, "室内新风机组", "n_mau", 1)
    # 设备实时值
    real_value_AO_dict = dict()
    real_value_AO_dict["real_value"] = dict()
    real_value_DO_dict = dict()
    real_value_DO_dict["real_value"] = dict()
    # 可能没有用户末端房间模型
    try:
        Tdi_list = []
        for i in range(n_Tdi):
            name_tmp = "user_Tdi_room" + str(i + 1)
            Tdi_tmp = round(list(simulate_result[name_tmp])[-1], 4)
            Tdi_list.append(Tdi_tmp)
        Hri_list = []
        for i in range(n_Hri):
            name_tmp = "user_Hri_room" + str(i + 1)
            Hri_tmp = round(list(simulate_result[name_tmp])[-1] * 100, 4)
            Hri_list.append(Hri_tmp)
    except:
        Tdi_list = []
        for i in range(n_Tdi):
            Tdi_list.append(26)
        Hri_list = []
        for i in range(n_Hri):
            Hri_list.append(60)
    # 生成字典
    # Teo、Tei
    for i in range(n_Te):
        Teo_name_tmp = "末端冷冻水出水温度传感器_" + str(i)
        real_value_AO_dict["real_value"][Teo_name_tmp] = dict()
        real_value_AO_dict["real_value"][Teo_name_tmp]["AO"] = dict()
        real_value_DO_dict["real_value"][Teo_name_tmp] = dict()
        real_value_DO_dict["real_value"][Teo_name_tmp]["DO"] = dict()
        Teo_tmp = round(list(simulate_result["user_Teo"])[-1], 4)
        real_value_AO_dict["real_value"][Teo_name_tmp]["AO"]["温度"] = Teo_tmp
        real_value_DO_dict["real_value"][Teo_name_tmp]["DO"]["状态"] = 1
        Tei_name_tmp = "末端冷冻水回水温度传感器_" + str(i)
        real_value_AO_dict["real_value"][Tei_name_tmp] = dict()
        real_value_AO_dict["real_value"][Tei_name_tmp]["AO"] = dict()
        real_value_DO_dict["real_value"][Tei_name_tmp] = dict()
        real_value_DO_dict["real_value"][Tei_name_tmp]["DO"] = dict()
        Tei_tmp = round(list(simulate_result["user_Tei"])[-1], 4)
        real_value_AO_dict["real_value"][Tei_name_tmp]["AO"]["温度"] = Tei_tmp
        real_value_DO_dict["real_value"][Tei_name_tmp]["DO"]["状态"] = 1
    # Tdi、Hri
    for i in range(n_Tdi):
        Tdi_name_tmp = "室内温度传感器_" + str(i)
        real_value_AO_dict["real_value"][Tdi_name_tmp] = dict()
        real_value_AO_dict["real_value"][Tdi_name_tmp]["AO"] = dict()
        real_value_DO_dict["real_value"][Tdi_name_tmp] = dict()
        real_value_DO_dict["real_value"][Tdi_name_tmp]["DO"] = dict()
        real_value_AO_dict["real_value"][Tdi_name_tmp]["AO"]["温度"] = Tdi_list[i]
        real_value_DO_dict["real_value"][Tdi_name_tmp]["DO"]["状态"] = 1
    for i in range(n_Hri):
        Hri_name_tmp = "室内湿度传感器_" + str(i)
        real_value_AO_dict["real_value"][Hri_name_tmp] = dict()
        real_value_AO_dict["real_value"][Hri_name_tmp]["AO"] = dict()
        real_value_DO_dict["real_value"][Hri_name_tmp] = dict()
        real_value_DO_dict["real_value"][Hri_name_tmp]["DO"] = dict()
        real_value_AO_dict["real_value"][Hri_name_tmp]["AO"]["湿度"] = Hri_list[i]
        real_value_DO_dict["real_value"][Hri_name_tmp]["DO"]["状态"] = 1
    # mau
    for i in range(n_mau):
        mau_name_tmp = "室内新风机组_" + str(i)
        real_value_AO_dict["real_value"][mau_name_tmp] = dict()
        real_value_AO_dict["real_value"][mau_name_tmp]["AO"] = dict()
        real_value_DO_dict["real_value"][mau_name_tmp] = dict()
        real_value_DO_dict["real_value"][mau_name_tmp]["DO"] = dict()
        real_value_AO_dict["real_value"][mau_name_tmp]["AO"]["新风流量"] = 580
        real_value_AO_dict["real_value"][mau_name_tmp]["AO"]["冷冻水流量"] = 1220
        real_value_AO_dict["real_value"][mau_name_tmp]["AO"]["冷冻水出水温度"] = 7
        real_value_DO_dict["real_value"][mau_name_tmp]["DO"]["状态"] = 1
    # 写入txt
    read_real_value_DO_user(real_value_DO_dict, equipment_type_path, cfg_path_equipment)
    read_real_value_AO_user(real_value_AO_dict, equipment_type_path, cfg_path_equipment)
    # 返回结果
    return real_value_DO_dict, real_value_AO_dict