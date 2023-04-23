"""
获取与设备有关的各种TXT文件路径
"""

def get_station_equipment_open_feedback_txt_path(equipment_type, txt_path):
    """
    能源站内设备开启控制和控制反馈的txt文件路径

    Args:
        equipment_type:[string]，设备类型
        txt_path:[string]，储存记录的txt文件路径(用于区分是否是上层目录)

    Returns:

    """
    # 各个设备的开启命令、开启状态反馈文件路径
    # 冷冻侧，冷冻侧，冷冻侧，冷冻侧，冷冻侧
    if equipment_type == "chiller" or equipment_type == "water_source_heat_pump" or \
            equipment_type == "air_source_heat_pump" or equipment_type == "lithium_bromide":
        # 如果是chiller、water_source_heat_pump、air_source_heat_pump、lithium_bromide,则有冷冻侧
        file_open_chilled_value = txt_path + "/control_commands/commands_set/" + equipment_type + \
                                  "/equipment_open/chilled_value.txt"
        file_feedback_open_chilled_value = txt_path + "/control_commands/commands_feedback/" + equipment_type + \
                                           "/equipment_open/chilled_value.txt"
        file_open_chilled_pump = txt_path + "/control_commands/commands_set/" + equipment_type + \
                                 "/equipment_open/chilled_pump.txt"
        file_feedback_open_chilled_pump = txt_path + "/control_commands/commands_feedback/" + equipment_type + \
                                          "/equipment_open/chilled_pump.txt"
        file_open_chilled_pump_secondary = txt_path + "/control_commands/commands_set/" + equipment_type + \
                                           "/equipment_open/chilled_pump_secondary.txt"
        file_feedback_open_chilled_pump_secondary = txt_path + "/control_commands/commands_feedback/" + \
                                                    equipment_type + "/equipment_open/chilled_pump_secondary.txt"
        file_open_main_equipment = txt_path + "/control_commands/commands_set/" + equipment_type + \
                                   "/equipment_open/air_conditioner.txt"
        file_feedback_open_main_equipment = txt_path + "/control_commands/commands_feedback/" + equipment_type + \
                                            "/equipment_open/air_conditioner.txt"
    elif equipment_type == "energy_storage_equipment":
        # 如果是蓄能装置，则主设备就是一级冷冻水泵
        file_open_chilled_value = txt_path + "/control_commands/commands_set/" + equipment_type + \
                                  "/equipment_open/chilled_value.txt"
        file_feedback_open_chilled_value = txt_path + "/control_commands/commands_feedback/" + equipment_type + \
                                           "/equipment_open/chilled_value.txt"
        file_open_chilled_pump = None
        file_feedback_open_chilled_pump = None
        file_open_chilled_pump_secondary = txt_path + "/control_commands/commands_set/" + equipment_type + \
                                           "/equipment_open/chilled_pump_secondary.txt"
        file_feedback_open_chilled_pump_secondary = txt_path + "/control_commands/commands_feedback/" + \
                                                    equipment_type + "/equipment_open/chilled_pump_secondary.txt"
        file_open_main_equipment = txt_path + "/control_commands/commands_set/" + equipment_type + \
                                   "/equipment_open/chilled_pump.txt"
        file_feedback_open_main_equipment = txt_path + "/control_commands/commands_feedback/" + equipment_type + \
                                            "/equipment_open/chilled_pump.txt"
    elif equipment_type == "chilled_pump_secondary":
        # 二级冷冻水泵，只有水泵
        file_open_chilled_value = None
        file_feedback_open_chilled_value = None
        file_open_chilled_pump = None
        file_feedback_open_chilled_pump = None
        file_open_chilled_pump_secondary = txt_path + "/control_commands/commands_set/" + equipment_type + \
                                           "/equipment_open/chilled_pump_secondary.txt"
        file_feedback_open_chilled_pump_secondary = txt_path + "/control_commands/commands_feedback/" + \
                                                    equipment_type + "/equipment_open/chilled_pump_secondary.txt"
        file_open_main_equipment = None
        file_feedback_open_main_equipment = None
    elif equipment_type == "internal_combustion_engine":
        # 内燃机，只有设备本身开启
        file_open_chilled_value = None
        file_feedback_open_chilled_value = None
        file_open_chilled_pump = None
        file_feedback_open_chilled_pump = None
        file_open_chilled_pump_secondary = None
        file_feedback_open_chilled_pump_secondary = None
        file_open_main_equipment = txt_path + "/control_commands/commands_set/" + equipment_type + \
                                   "/equipment_open/internal_combustion_engine.txt"
        file_feedback_open_main_equipment = txt_path + "/control_commands/commands_feedback/" + equipment_type + \
                                            "/equipment_open/internal_combustion_engine.txt"
    else:
        file_open_chilled_value = None
        file_feedback_open_chilled_value = None
        file_open_chilled_pump = None
        file_feedback_open_chilled_pump = None
        file_open_chilled_pump_secondary = None
        file_feedback_open_chilled_pump_secondary = None
        file_open_main_equipment = None
        file_feedback_open_main_equipment = None
    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————
    # 冷却侧，冷却侧，冷却侧，冷却侧，冷却侧
    if equipment_type == "chiller" or equipment_type == "lithium_bromide":
        # 如果是chiller、lithium_bromide,则有冷却水泵+冷却塔
        file_open_cooling_value = txt_path + "/control_commands/commands_set/" + equipment_type + \
                                  "/equipment_open/cooling_value.txt"
        file_feedback_open_cooling_value = txt_path + "/control_commands/commands_feedback/" + equipment_type + \
                                           "/equipment_open/cooling_value.txt"
        file_open_cooling_pump = txt_path + "/control_commands/commands_set/" + equipment_type + \
                                 "/equipment_open/cooling_pump.txt"
        file_feedback_open_cooling_pump = txt_path + "/control_commands/commands_feedback/" + equipment_type + \
                                          "/equipment_open/cooling_pump.txt"
        file_open_cooling_tower = txt_path + "/control_commands/commands_set/" + equipment_type + \
                                  "/equipment_open/cooling_tower.txt"
        file_feedback_open_cooling_tower = txt_path + "/control_commands/commands_feedback/" + equipment_type + \
                                           "/equipment_open/cooling_tower.txt"
        file_open_tower_value = txt_path + "/control_commands/commands_set/" + equipment_type + \
                                "/equipment_open/tower_value.txt"
        file_feedback_open_tower_value = txt_path + "/control_commands/commands_feedback/" + equipment_type + \
                                         "/equipment_open/tower_value.txt"
    elif equipment_type == "water_source_heat_pump":
        # 如果是water_source_heat_pump，则冷却侧没有冷却塔
        file_open_cooling_value = txt_path + "/control_commands/commands_set/" + equipment_type + \
                                  "/equipment_open/cooling_value.txt"
        file_feedback_open_cooling_value = txt_path + "/control_commands/commands_feedback/" + equipment_type + \
                                           "/equipment_open/cooling_value.txt"
        file_open_cooling_pump = txt_path + "/control_commands/commands_set/" + equipment_type + \
                                 "/equipment_open/cooling_pump.txt"
        file_feedback_open_cooling_pump = txt_path + "/control_commands/commands_feedback/" + equipment_type + \
                                          "/equipment_open/cooling_pump.txt"
        file_open_cooling_tower = None
        file_feedback_open_cooling_tower = None
        file_open_tower_value = None
        file_feedback_open_tower_value = None
    else:
        # 没有冷却侧
        file_open_cooling_value = None
        file_feedback_open_cooling_value = None
        file_open_cooling_pump = None
        file_feedback_open_cooling_pump = None
        file_open_cooling_tower = None
        file_feedback_open_cooling_tower = None
        file_open_tower_value = None
        file_feedback_open_tower_value = None
    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————
    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————
    # 各个设备的频率设定值、设定状态反馈文件路径
    # 冷冻侧，冷冻侧，冷冻侧，冷冻侧，冷冻侧
    if equipment_type == "chiller" or equipment_type == "water_source_heat_pump" or \
            equipment_type == "air_source_heat_pump" or equipment_type == "lithium_bromide":
        # 具有一级冷冻水泵、二级冷冻水泵
        file_frequency_chilled_pump_secondary = txt_path + "/control_commands/commands_set/" + equipment_type + \
                                                "/equipment_frequency/chilled_pump_secondary.txt"
        file_feedback_frequency_chilled_pump_secondary = txt_path + "/control_commands/commands_feedback/" + \
                                                         equipment_type + "/equipment_frequency/chilled_pump_secondary.txt"
        file_frequency_chilled_pump = txt_path + "/control_commands/commands_set/" + equipment_type + \
                                      "/equipment_frequency/chilled_pump.txt"
        file_feedback_frequency_chilled_pump = txt_path + "/control_commands/commands_feedback/" + equipment_type + \
                                               "/equipment_frequency/chilled_pump.txt"
    elif equipment_type == "chilled_pump_secondary" or equipment_type == "energy_storage_equipment":
        # 二级冷冻水泵，只有水泵；蓄能装置，一级水泵是主设备
        file_frequency_chilled_pump_secondary = txt_path + "/control_commands/commands_set/" + equipment_type + \
                                                "/equipment_frequency/chilled_pump_secondary.txt"
        file_feedback_frequency_chilled_pump_secondary = txt_path + "/control_commands/commands_feedback/" + \
                                                         equipment_type + "/equipment_frequency/chilled_pump_secondary.txt"
        file_frequency_chilled_pump = None
        file_feedback_frequency_chilled_pump = None
    else:
        file_frequency_chilled_pump_secondary = None
        file_feedback_frequency_chilled_pump_secondary = None
        file_frequency_chilled_pump = None
        file_feedback_frequency_chilled_pump = None
    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————
    # 冷却侧，冷却侧，冷却侧，冷却侧，冷却侧
    if equipment_type == "chiller" or equipment_type == "lithium_bromide":
        # 如果是chiller、lithium_bromide,则有冷却水泵+冷却塔
        file_frequency_cooling_pump = txt_path + "/control_commands/commands_set/" + equipment_type + \
                                      "/equipment_frequency/cooling_pump.txt"
        file_feedback_frequency_cooling_pump = txt_path + "/control_commands/commands_feedback/" + equipment_type + \
                                               "/equipment_frequency/cooling_pump.txt"
        file_frequency_cooling_tower = txt_path + "/control_commands/commands_set/" + equipment_type + \
                                       "/equipment_frequency/cooling_tower.txt"
        file_feedback_frequency_cooling_tower = txt_path + "/control_commands/commands_feedback/" + equipment_type + \
                                                "/equipment_frequency/cooling_tower.txt"
    elif equipment_type == "water_source_heat_pump":
        # 如果是water_source_heat_pump，则冷却侧没有冷却塔
        file_frequency_cooling_pump = txt_path + "/control_commands/commands_set/" + equipment_type + \
                                      "/equipment_frequency/cooling_pump.txt"
        file_feedback_frequency_cooling_pump = txt_path + "/control_commands/commands_feedback/" + equipment_type + \
                                               "/equipment_frequency/cooling_pump.txt"
        file_frequency_cooling_tower = None
        file_feedback_frequency_cooling_tower = None
    else:
        # 没有冷却侧
        file_frequency_cooling_pump = None
        file_feedback_frequency_cooling_pump = None
        file_frequency_cooling_tower = None
        file_feedback_frequency_cooling_tower = None
    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————
    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————
    # 主设备本体冷冻水出水温度设定值和反馈的文件路径
    if equipment_type == "chiller" or equipment_type == "water_source_heat_pump" or \
            equipment_type == "air_source_heat_pump" or equipment_type == "lithium_bromide":
        file_set_value_main_equipment = txt_path + "/control_commands/commands_set/" + equipment_type + \
                                        "/equipment_Teo/air_conditioner.txt"
        file_feedback_set_value_main_equipment = txt_path + "/control_commands/commands_feedback/" + equipment_type + \
                                                 "/equipment_Teo/air_conditioner.txt"
    elif equipment_type == "internal_combustion_engine":
        # 内燃机，是设定发电功率P
        file_set_value_main_equipment = txt_path + "/control_commands/commands_set/" + equipment_type + \
                                        "/equipment_P/internal_combustion_engine.txt"
        file_feedback_set_value_main_equipment = txt_path + "/control_commands/commands_feedback/" + equipment_type + \
                                                 "/equipment_P/internal_combustion_engine.txt"
    elif equipment_type == "energy_storage_equipment":
        # 蓄能装置，一级水泵是主设备，是水泵频率
        file_set_value_main_equipment = txt_path + "/control_commands/commands_set/" + equipment_type + \
                                        "/equipment_frequency/chilled_pump.txt"
        file_feedback_set_value_main_equipment = txt_path + "/control_commands/commands_feedback/" + equipment_type + \
                                                 "/equipment_frequency/chilled_pump.txt"
    else:
        file_set_value_main_equipment = None
        file_feedback_set_value_main_equipment = None
    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————
    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————
    # 阀门开度设定值、设定值反馈文件路径
    # 冷冻侧，冷冻侧，冷冻侧，冷冻侧，冷冻侧
    if equipment_type == "chiller" or equipment_type == "water_source_heat_pump" or \
            equipment_type == "air_source_heat_pump" or equipment_type == "lithium_bromide" \
            or equipment_type == "energy_storage_equipment":
        # 冷冻阀门
        file_proportion_chilled_value = txt_path + "/control_commands/commands_set/" + equipment_type + \
                                        "/equipment_proportion/chilled_value.txt"
        file_feedback_proportion_chilled_value = txt_path + "/control_commands/commands_feedback/" + equipment_type + \
                                                 "/equipment_proportion/chilled_value.txt"
    else:
        file_proportion_chilled_value = None
        file_feedback_proportion_chilled_value = None
    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————
    # 冷却侧阀门
    if equipment_type == "chiller" or equipment_type == "lithium_bromide":
        file_proportion_cooling_value = txt_path + "/control_commands/commands_set/" + equipment_type + \
                                        "/equipment_proportion/cooling_value.txt"
        file_feedback_proportion_cooling_value = txt_path + "/control_commands/commands_feedback/" + equipment_type + \
                                                 "/equipment_proportion/cooling_value.txt"
        file_proportion_tower_value = txt_path + "/control_commands/commands_set/" + equipment_type + \
                                      "/equipment_proportion/tower_value.txt"
        file_feedback_proportion_tower_value = txt_path + "/control_commands/commands_feedback/" + equipment_type + \
                                               "/equipment_proportion/tower_value.txt"
    elif equipment_type == "water_source_heat_pump":
        file_proportion_cooling_value = txt_path + "/control_commands/commands_set/" + equipment_type + \
                                        "/equipment_proportion/cooling_value.txt"
        file_feedback_proportion_cooling_value = txt_path + "/control_commands/commands_feedback/" + equipment_type + \
                                                 "/equipment_proportion/cooling_value.txt"
        file_proportion_tower_value = None
        file_feedback_proportion_tower_value = None
    else:
        # 没有冷却侧
        file_proportion_cooling_value = None
        file_feedback_proportion_cooling_value = None
        file_proportion_tower_value = None
        file_feedback_proportion_tower_value = None
    # 返回结果
    return file_open_chilled_value, file_feedback_open_chilled_value, file_open_chilled_pump,\
           file_feedback_open_chilled_pump, file_open_chilled_pump_secondary, \
           file_feedback_open_chilled_pump_secondary, file_open_main_equipment, file_feedback_open_main_equipment,\
           file_open_cooling_value, file_feedback_open_cooling_value, file_open_cooling_pump, \
           file_feedback_open_cooling_pump, file_open_cooling_tower, file_feedback_open_cooling_tower, \
           file_frequency_chilled_pump_secondary, file_feedback_frequency_chilled_pump_secondary, \
           file_frequency_chilled_pump, file_feedback_frequency_chilled_pump, \
           file_frequency_cooling_pump, file_feedback_frequency_cooling_pump, file_frequency_cooling_tower,\
           file_feedback_frequency_cooling_tower, file_set_value_main_equipment,file_feedback_set_value_main_equipment, \
           file_proportion_chilled_value, file_feedback_proportion_chilled_value, file_proportion_cooling_value,\
           file_feedback_proportion_cooling_value, file_open_tower_value, file_feedback_open_tower_value, \
           file_proportion_tower_value, file_feedback_proportion_tower_value


def get_station_equipment_close_feedback_txt_path(equipment_type, txt_path):
    """
    能源站内设备关闭控制和控制反馈的txt文件路径

    Args:
        equipment_type:[string]，设备类型
        txt_path:[string]，储存记录的txt文件路径(用于区分是否是上层目录)

    Returns:

    """
    # 各个设备的关闭命令、关闭状态反馈文件路径
    # 冷冻侧，冷冻侧，冷冻侧，冷冻侧，冷冻侧
    if equipment_type == "chiller" or equipment_type == "water_source_heat_pump" or \
            equipment_type == "air_source_heat_pump" or equipment_type == "lithium_bromide":
        # 如果是chiller、water_source_heat_pump、air_source_heat_pump、lithium_bromide,则有冷冻侧
        file_close_main_equipment = txt_path + "/control_commands/commands_set/" + equipment_type + \
                                    "/equipment_close/air_conditioner.txt"
        file_feedback_close_main_equipment = txt_path + "/control_commands/commands_feedback/" + equipment_type + \
                                             "/equipment_close/air_conditioner.txt"
        file_close_chilled_pump = txt_path + "/control_commands/commands_set/" + equipment_type + \
                                  "/equipment_close/chilled_pump.txt"
        file_feedback_close_chilled_pump = txt_path + "/control_commands/commands_feedback/" + equipment_type + \
                                           "/equipment_close/chilled_pump.txt"
        file_close_chilled_value = txt_path + "/control_commands/commands_set/" + equipment_type + \
                                   "/equipment_close/chilled_value.txt"
        file_feedback_close_chilled_value = txt_path + "/control_commands/commands_feedback/" + equipment_type + \
                                            "/equipment_close/chilled_value.txt"
        file_close_chilled_pump_secondary = txt_path + "/control_commands/commands_set/" + equipment_type + \
                                            "/equipment_close/chilled_pump_secondary.txt"
        file_feedback_close_chilled_pump_secondary = txt_path + "/control_commands/commands_feedback/" + \
                                                     equipment_type + "/equipment_close/chilled_pump_secondary.txt"
    elif equipment_type == "energy_storage_equipment":
        # 蓄能装置，一级水泵是主设备
        file_close_main_equipment = txt_path + "/control_commands/commands_set/" + equipment_type + \
                                    "/equipment_close/chilled_pump.txt"
        file_feedback_close_main_equipment = txt_path + "/control_commands/commands_feedback/" + equipment_type + \
                                             "/equipment_close/chilled_pump.txt"
        file_close_chilled_pump = None
        file_feedback_close_chilled_pump = None
        file_close_chilled_value = txt_path + "/control_commands/commands_set/" + equipment_type + \
                                   "/equipment_close/chilled_value.txt"
        file_feedback_close_chilled_value = txt_path + "/control_commands/commands_feedback/" + equipment_type + \
                                            "/equipment_close/chilled_value.txt"
        file_close_chilled_pump_secondary = txt_path + "/control_commands/commands_set/" + equipment_type + \
                                            "/equipment_close/chilled_pump_secondary.txt"
        file_feedback_close_chilled_pump_secondary = txt_path + "/control_commands/commands_feedback/" + \
                                                     equipment_type + "/equipment_close/chilled_pump_secondary.txt"
    elif equipment_type == "chilled_pump_secondary":
        # 二级冷冻水泵，只有水泵
        file_close_main_equipment = None
        file_feedback_close_main_equipment = None
        file_close_chilled_pump = None
        file_feedback_close_chilled_pump = None
        file_close_chilled_value = None
        file_feedback_close_chilled_value = None
        file_close_chilled_pump_secondary = txt_path + "/control_commands/commands_set/" + equipment_type + \
                                            "/equipment_close/chilled_pump_secondary.txt"
        file_feedback_close_chilled_pump_secondary = txt_path + "/control_commands/commands_feedback/" + \
                                                     equipment_type + "/equipment_close/chilled_pump_secondary.txt"
    elif equipment_type == "internal_combustion_engine":
        # 内燃机，只有设备本身开启
        file_close_main_equipment = txt_path + "/control_commands/commands_set/" + equipment_type + \
                                    "/equipment_close/internal_combustion_engine.txt"
        file_feedback_close_main_equipment = txt_path + "/control_commands/commands_feedback/" + equipment_type + \
                                             "/equipment_close/internal_combustion_engine.txt"
        file_close_chilled_pump = None
        file_feedback_close_chilled_pump = None
        file_close_chilled_value = None
        file_feedback_close_chilled_value = None
        file_close_chilled_pump_secondary = None
        file_feedback_close_chilled_pump_secondary = None
    else:
        file_close_main_equipment = None
        file_feedback_close_main_equipment = None
        file_close_chilled_pump = None
        file_feedback_close_chilled_pump = None
        file_close_chilled_value = None
        file_feedback_close_chilled_value = None
        file_close_chilled_pump_secondary = None
        file_feedback_close_chilled_pump_secondary = None
    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————
    # 冷却侧，冷却侧，冷却侧，冷却侧，冷却侧
    if equipment_type == "chiller" or equipment_type == "lithium_bromide":
        # 如果是chiller、lithium_bromide,则有冷却水泵+冷却塔
        file_close_cooling_tower = txt_path + "/control_commands/commands_set/" + equipment_type + \
                                   "/equipment_close/cooling_tower.txt"
        file_feedback_close_cooling_tower = txt_path + "/control_commands/commands_feedback/" + equipment_type + \
                                            "/equipment_close/cooling_tower.txt"
        file_close_cooling_pump = txt_path + "/control_commands/commands_set/" + equipment_type + \
                                  "/equipment_close/cooling_pump.txt"
        file_feedback_close_cooling_pump = txt_path + "/control_commands/commands_feedback/" + equipment_type + \
                                           "/equipment_close/cooling_pump.txt"
        file_close_cooling_value = txt_path + "/control_commands/commands_set/" + equipment_type + \
                                   "/equipment_close/cooling_value.txt"
        file_feedback_close_cooling_value = txt_path + "/control_commands/commands_feedback/" + equipment_type + \
                                            "/equipment_close/cooling_value.txt"
        file_close_tower_value = txt_path + "/control_commands/commands_set/" + equipment_type + \
                                 "/equipment_close/tower_value.txt"
        file_feedback_close_tower_value = txt_path + "/control_commands/commands_feedback/" + equipment_type + \
                                          "/equipment_close/tower_value.txt"
    elif equipment_type == "water_source_heat_pump":
        # 如果是water_source_heat_pump，则冷却侧没有冷却塔
        file_close_cooling_tower = None
        file_feedback_close_cooling_tower = None
        file_close_cooling_pump = txt_path + "/control_commands/commands_set/" + equipment_type + \
                                  "/equipment_close/cooling_pump.txt"
        file_feedback_close_cooling_pump = txt_path + "/control_commands/commands_feedback/" + equipment_type + \
                                           "/equipment_close/cooling_pump.txt"
        file_close_cooling_value = txt_path + "/control_commands/commands_set/" + equipment_type + \
                                   "/equipment_close/cooling_value.txt"
        file_feedback_close_cooling_value = txt_path + "/control_commands/commands_feedback/" + equipment_type + \
                                            "/equipment_close/cooling_value.txt"
        file_close_tower_value = None
        file_feedback_close_tower_value = None
    else:
        # 没有冷却侧
        file_close_cooling_tower = None
        file_feedback_close_cooling_tower = None
        file_close_cooling_pump = None
        file_feedback_close_cooling_pump = None
        file_close_cooling_value = None
        file_feedback_close_cooling_value = None
        file_close_tower_value = None
        file_feedback_close_tower_value = None
    # 返回结果
    return file_close_main_equipment, file_feedback_close_main_equipment, file_close_chilled_pump,\
           file_feedback_close_chilled_pump, file_close_chilled_value, file_feedback_close_chilled_value,\
           file_close_chilled_pump_secondary, file_feedback_close_chilled_pump_secondary, file_close_cooling_tower, \
           file_feedback_close_cooling_tower, file_close_cooling_pump, file_feedback_close_cooling_pump, \
           file_close_cooling_value, file_feedback_close_cooling_value, file_close_tower_value, \
           file_feedback_close_tower_value


def get_station_equipment_real_value_txt_path(equipment_type, txt_path):
    """
    能源站内设备当前实际值txt文件路径

    Args:
        equipment_type:[string]，设备类型
        txt_path:[string]，储存记录的txt文件路径(用于区分是否是上层目录)

    Returns:

    """
    # 各种设备被控制的模拟量实际值路径、耗电功率实际值路径、耗天然气量实际值路径
    # 主设备当前Teo、发电功率(仅内燃机)、耗电功率、耗天然气功率(仅内燃机)
    if equipment_type == "chiller" or equipment_type == "water_source_heat_pump" or \
            equipment_type == "air_source_heat_pump" or equipment_type == "lithium_bromide":
        file_out_value_main_equipment = txt_path + "/real_value/" + equipment_type + "/Teo_value/air_conditioner.txt"
        file_consume_value_main_equipment = txt_path + "/real_value/" + equipment_type + "/P_value/air_conditioner.txt"
    elif equipment_type == "internal_combustion_engine":
        # 内燃机，是发电功率P
        file_out_value_main_equipment = txt_path + "/real_value/" + equipment_type + \
                                        "/P_value/internal_combustion_engine.txt"
        file_consume_value_main_equipment = txt_path + "/real_value/" + equipment_type + \
                                            "/NG_value/internal_combustion_engine.txt"
    elif equipment_type == "energy_storage_equipment":
        # 蓄能装置，一级水泵是主设备
        file_out_value_main_equipment = txt_path + "/real_value/" + equipment_type + "/frequency_value/chilled_pump.txt"
        file_consume_value_main_equipment = txt_path + "/real_value/" + equipment_type + "/P_value/chilled_pump.txt"
    else:
        file_out_value_main_equipment = None
        file_consume_value_main_equipment = None
    if equipment_type == "energy_storage_equipment":
        # 当前时刻蓄能装置剩余的蓄能量，单位kWh
        file_energy_storage_equipment_E = txt_path + "/real_value/" + equipment_type + \
                                          "/Q_plan_E_plan/energy_storage_equipment_E.txt"
        # 储存逐时用能计划，24小时逐时的Q，单位KW
        file_energy_storage_equipment_Q_plan = txt_path + "/real_value/" + equipment_type + \
                                               "/Q_plan_E_plan/energy_storage_equipment_Q_plan.txt"
        # 储存逐时用能计划，24小时逐时的，单位KWh
        file_energy_storage_equipment_E_plan = txt_path + "/real_value/" + equipment_type + \
                                               "/Q_plan_E_plan/energy_storage_equipment_E_plan.txt"
    else:
        file_energy_storage_equipment_E = None
        file_energy_storage_equipment_Q_plan = None
        file_energy_storage_equipment_E_plan = None
    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————
    # 冷冻侧水泵
    if equipment_type == "chiller" or equipment_type == "water_source_heat_pump" or \
            equipment_type == "air_source_heat_pump" or equipment_type == "lithium_bromide":
        file_frequency_value_chilled_pump = txt_path + "/real_value/" + equipment_type + \
                                            "/frequency_value/chilled_pump.txt"
        file_frequency_value_chilled_pump_secondary = txt_path + "/real_value/" + equipment_type + \
                                                      "/frequency_value/chilled_pump_secondary.txt"
        file_P_value_chilled_pump = txt_path + "/real_value/" + equipment_type + "/P_value/chilled_pump.txt"
        file_P_value_chilled_pump_secondary = txt_path + "/real_value/" + equipment_type + \
                                              "/P_value/chilled_pump_secondary.txt"
    elif equipment_type == "chilled_pump_secondary" or equipment_type == "energy_storage_equipment":
        # 二级冷冻水泵，只有水泵;蓄能装置，一级水泵是主设备
        file_frequency_value_chilled_pump = None
        file_frequency_value_chilled_pump_secondary = txt_path + "/real_value/" + equipment_type + \
                                                      "/frequency_value/chilled_pump_secondary.txt"
        file_P_value_chilled_pump = None
        file_P_value_chilled_pump_secondary = txt_path + "/real_value/" + equipment_type + \
                                              "/P_value/chilled_pump_secondary.txt"
    else:
        file_frequency_value_chilled_pump = None
        file_frequency_value_chilled_pump_secondary = None
        file_P_value_chilled_pump = None
        file_P_value_chilled_pump_secondary = None
    # 冷冻阀门
    if equipment_type == "chiller" or equipment_type == "water_source_heat_pump" or \
            equipment_type == "air_source_heat_pump" or equipment_type == "lithium_bromide" \
            or equipment_type == "energy_storage_equipment":
        file_proportion_value_chilled_value = txt_path + "/real_value/" + equipment_type + \
                                              "/proportion_value/chilled_value.txt"
    else:
        file_proportion_value_chilled_value = None
    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————
    # 冷却侧阀门、水泵、冷却塔
    if equipment_type == "chiller" or equipment_type == "lithium_bromide":
        file_frequency_value_cooling_pump = txt_path + "/real_value/" + equipment_type + \
                                            "/frequency_value/cooling_pump.txt"
        file_frequency_value_cooling_tower = txt_path + "/real_value/" + equipment_type + \
                                             "/frequency_value/cooling_tower.txt"
        file_proportion_value_cooling_value = txt_path + "/real_value/" + equipment_type + \
                                              "/proportion_value/cooling_value.txt"
        file_proportion_value_tower_value = txt_path + "/real_value/" + equipment_type + \
                                            "/proportion_value/tower_value.txt"
        file_P_value_cooling_pump = txt_path + "/real_value/" + equipment_type + "/P_value/cooling_pump.txt"
        file_P_value_cooling_tower = txt_path + "/real_value/" + equipment_type + "/P_value/cooling_tower.txt"
    elif equipment_type == "water_source_heat_pump":
        # 如果是water_source_heat_pump，则冷却侧没有冷却塔
        file_frequency_value_cooling_pump = txt_path + "/real_value/" + equipment_type + \
                                            "/frequency_value/cooling_pump.txt"
        file_frequency_value_cooling_tower = None
        file_proportion_value_cooling_value = txt_path + "/real_value/" + equipment_type + \
                                              "/proportion_value/cooling_value.txt"
        file_proportion_value_tower_value = None
        file_P_value_cooling_pump = txt_path + "/real_value/" + equipment_type + "/P_value/cooling_pump.txt"
        file_P_value_cooling_tower = None
    else:
        # 没有冷却侧
        file_frequency_value_cooling_pump = None
        file_frequency_value_cooling_tower = None
        file_proportion_value_cooling_value = None
        file_proportion_value_tower_value = None
        file_P_value_cooling_pump = None
        file_P_value_cooling_tower = None
    # 返回结果
    return file_out_value_main_equipment, file_frequency_value_chilled_pump, \
           file_frequency_value_chilled_pump_secondary, file_proportion_value_chilled_value, \
           file_frequency_value_cooling_pump, file_frequency_value_cooling_tower, file_proportion_value_cooling_value, \
           file_proportion_value_tower_value, file_consume_value_main_equipment, file_P_value_chilled_pump, \
           file_P_value_chilled_pump_secondary, file_P_value_cooling_pump, file_P_value_cooling_tower, \
           file_energy_storage_equipment_E, file_energy_storage_equipment_Q_plan, file_energy_storage_equipment_E_plan


def get_station_equipment_open_status_txt_path(equipment_type, txt_path):
    """
    能源站内设备开启状态txt文件路径

    Args:
        equipment_type:[string]，设备类型
        txt_path:[string]，储存记录的txt文件路径(用于区分是否是上层目录)

    Returns:

    """
    # 储存设备运行状态的文件路径
    # 冷冻侧，冷冻侧，冷冻侧，冷冻侧，冷冻侧
    if equipment_type == "chiller" or equipment_type == "water_source_heat_pump" or \
            equipment_type == "air_source_heat_pump" or equipment_type == "lithium_bromide":
        file_main_equipment_open_status = txt_path + "/equipment_status/" + equipment_type + \
                                          "/open_status/air_conditioner.txt"
        file_chilled_pump_open_status = txt_path + "/equipment_status/" + equipment_type + \
                                        "/open_status/chilled_pump.txt"
        file_chilled_pump_secondary_open_status = txt_path + "/equipment_status/" + equipment_type + \
                                                  "/open_status/chilled_pump_secondary.txt"
        file_chilled_value_open_status = txt_path + "/equipment_status/" + equipment_type + \
                                         "/open_status/chilled_value.txt"
    elif equipment_type == "energy_storage_equipment":
        # 蓄能装置，一级水泵是主设备
        file_main_equipment_open_status = txt_path + "/equipment_status/" + equipment_type + \
                                          "/open_status/chilled_pump.txt"
        file_chilled_pump_open_status = None
        file_chilled_pump_secondary_open_status = txt_path + "/equipment_status/" + equipment_type + \
                                                  "/open_status/chilled_pump_secondary.txt"
        file_chilled_value_open_status = txt_path + "/equipment_status/" + equipment_type + \
                                         "/open_status/chilled_value.txt"
    elif equipment_type == "chilled_pump_secondary":
        # 二级冷冻水泵，只有水泵
        file_main_equipment_open_status = None
        file_chilled_pump_open_status = None
        file_chilled_pump_secondary_open_status = txt_path + "/equipment_status/" + equipment_type + \
                                                  "/open_status/chilled_pump_secondary.txt"
        file_chilled_value_open_status = None
    elif equipment_type == "internal_combustion_engine":
        file_main_equipment_open_status = txt_path + "/equipment_status/" + equipment_type + \
                                          "/open_status/internal_combustion_engine.txt"
        file_chilled_pump_open_status = None
        file_chilled_pump_secondary_open_status = None
        file_chilled_value_open_status = None
    else:
        file_main_equipment_open_status = None
        file_chilled_pump_open_status = None
        file_chilled_pump_secondary_open_status = None
        file_chilled_value_open_status = None
    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————
    # 冷却侧，冷却侧，冷却侧，冷却侧，冷却侧
    if equipment_type == "chiller" or equipment_type == "lithium_bromide":
        # 如果是chiller、lithium_bromide,则有冷却水泵+冷却塔
        file_cooling_pump_open_status = txt_path + "/equipment_status/" + equipment_type + \
                                        "/open_status/cooling_pump.txt"
        file_cooling_tower_open_status = txt_path + "/equipment_status/" + equipment_type + \
                                         "/open_status/cooling_tower.txt"
        file_cooling_value_open_status = txt_path + "/equipment_status/" + equipment_type + \
                                         "/open_status/cooling_value.txt"
        file_tower_value_open_status = txt_path + "/equipment_status/" + equipment_type + \
                                       "/open_status/tower_value.txt"
    elif equipment_type == "water_source_heat_pump":
        # 如果是water_source_heat_pump，则冷却侧没有冷却塔
        file_cooling_pump_open_status = txt_path + "/equipment_status/" + equipment_type + \
                                        "/open_status/cooling_pump.txt"
        file_cooling_tower_open_status = None
        file_cooling_value_open_status = txt_path + "/equipment_status/" + equipment_type + \
                                         "/open_status/cooling_value.txt"
        file_tower_value_open_status = None
    else:
        # 没有冷却侧
        file_cooling_pump_open_status = None
        file_cooling_tower_open_status = None
        file_cooling_value_open_status = None
        file_tower_value_open_status = None
    # 返回结果
    return file_main_equipment_open_status, file_chilled_pump_open_status, file_chilled_pump_secondary_open_status, \
           file_cooling_pump_open_status, file_cooling_tower_open_status, file_chilled_value_open_status, \
           file_cooling_value_open_status, file_tower_value_open_status


def get_station_equipment_alarm_status_txt_path(equipment_type, txt_path):
    """
    能源站内设备告警状态txt文件路径

    Args:
        equipment_type:[string]，设备类型
        txt_path:[string]，储存记录的txt文件路径(用于区分是否是上层目录)

    Returns:

    """
    # 储存设备运行状态的文件路径
    # 冷冻侧，冷冻侧，冷冻侧，冷冻侧，冷冻侧
    if equipment_type == "chiller" or equipment_type == "water_source_heat_pump" or \
            equipment_type == "air_source_heat_pump" or equipment_type == "lithium_bromide":
        file_main_equipment_alarm_status = txt_path + "/equipment_status/" + equipment_type + \
                                          "/alarm_status/air_conditioner.txt"
        file_chilled_pump_alarm_status = txt_path + "/equipment_status/" + equipment_type + \
                                        "/alarm_status/chilled_pump.txt"
        file_chilled_pump_secondary_alarm_status = txt_path + "/equipment_status/" + equipment_type + \
                                                  "/alarm_status/chilled_pump_secondary.txt"
        file_chilled_value_alarm_status = txt_path + "/equipment_status/" + equipment_type + \
                                         "/alarm_status/chilled_value.txt"
    elif equipment_type == "energy_storage_equipment":
        # 蓄能装置，一级水泵是主设备
        file_main_equipment_alarm_status = txt_path + "/equipment_status/" + equipment_type + \
                                          "/alarm_status/chilled_pump.txt"
        file_chilled_pump_alarm_status = None
        file_chilled_pump_secondary_alarm_status = txt_path + "/equipment_status/" + equipment_type + \
                                                  "/alarm_status/chilled_pump_secondary.txt"
        file_chilled_value_alarm_status = txt_path + "/equipment_status/" + equipment_type + \
                                         "/alarm_status/chilled_value.txt"
    elif equipment_type == "chilled_pump_secondary":
        # 二级冷冻水泵，只有水泵
        file_main_equipment_alarm_status = None
        file_chilled_pump_alarm_status = None
        file_chilled_pump_secondary_alarm_status = txt_path + "/equipment_status/" + equipment_type + \
                                                  "/alarm_status/chilled_pump_secondary.txt"
        file_chilled_value_alarm_status = None
    elif equipment_type == "internal_combustion_engine":
        file_main_equipment_alarm_status = txt_path + "/equipment_status/" + equipment_type + \
                                          "/alarm_status/internal_combustion_engine.txt"
        file_chilled_pump_alarm_status = None
        file_chilled_pump_secondary_alarm_status = None
        file_chilled_value_alarm_status = None
    else:
        file_main_equipment_alarm_status = None
        file_chilled_pump_alarm_status = None
        file_chilled_pump_secondary_alarm_status = None
        file_chilled_value_alarm_status = None
    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————
    # 冷却侧，冷却侧，冷却侧，冷却侧，冷却侧
    if equipment_type == "chiller" or equipment_type == "lithium_bromide":
        # 如果是chiller、lithium_bromide,则有冷却水泵+冷却塔
        file_cooling_pump_alarm_status = txt_path + "/equipment_status/" + equipment_type + \
                                        "/alarm_status/cooling_pump.txt"
        file_cooling_tower_alarm_status = txt_path + "/equipment_status/" + equipment_type + \
                                         "/alarm_status/cooling_tower.txt"
        file_cooling_value_alarm_status = txt_path + "/equipment_status/" + equipment_type + \
                                         "/alarm_status/cooling_value.txt"
        file_tower_value_alarm_status = txt_path + "/equipment_status/" + equipment_type + \
                                       "/alarm_status/tower_value.txt"
    elif equipment_type == "water_source_heat_pump":
        # 如果是water_source_heat_pump，则冷却侧没有冷却塔
        file_cooling_pump_alarm_status = txt_path + "/equipment_status/" + equipment_type + \
                                        "/alarm_status/cooling_pump.txt"
        file_cooling_tower_alarm_status = None
        file_cooling_value_alarm_status = txt_path + "/equipment_status/" + equipment_type + \
                                         "/alarm_status/cooling_value.txt"
        file_tower_value_alarm_status = None
    else:
        # 没有冷却侧
        file_cooling_pump_alarm_status = None
        file_cooling_tower_alarm_status = None
        file_cooling_value_alarm_status = None
        file_tower_value_alarm_status = None
    # 返回结果
    return file_main_equipment_alarm_status, file_chilled_pump_alarm_status, file_chilled_pump_secondary_alarm_status, \
           file_cooling_pump_alarm_status, file_cooling_tower_alarm_status, file_chilled_value_alarm_status, \
           file_cooling_value_alarm_status, file_tower_value_alarm_status


def get_station_equipment_fault_status_txt_path(equipment_type, txt_path):
    """
    能源站内设备故障状态txt文件路径

    Args:
        equipment_type:[string]，设备类型
        txt_path:[string]，储存记录的txt文件路径(用于区分是否是上层目录)

    Returns:

    """
    # 储存设备运行状态的文件路径
    # 冷冻侧，冷冻侧，冷冻侧，冷冻侧，冷冻侧
    if equipment_type == "chiller" or equipment_type == "water_source_heat_pump" or \
            equipment_type == "air_source_heat_pump" or equipment_type == "lithium_bromide":
        file_main_equipment_fault_status = txt_path + "/equipment_status/" + equipment_type + \
                                          "/fault_status/air_conditioner.txt"
        file_chilled_pump_fault_status = txt_path + "/equipment_status/" + equipment_type + \
                                        "/fault_status/chilled_pump.txt"
        file_chilled_pump_secondary_fault_status = txt_path + "/equipment_status/" + equipment_type + \
                                                  "/fault_status/chilled_pump_secondary.txt"
        file_chilled_value_fault_status = txt_path + "/equipment_status/" + equipment_type + \
                                         "/fault_status/chilled_value.txt"
    elif equipment_type == "energy_storage_equipment":
        # 蓄能装置，一级水泵是主设备
        file_main_equipment_fault_status = txt_path + "/equipment_status/" + equipment_type + \
                                          "/fault_status/chilled_pump.txt"
        file_chilled_pump_fault_status = None
        file_chilled_pump_secondary_fault_status = txt_path + "/equipment_status/" + equipment_type + \
                                                  "/fault_status/chilled_pump_secondary.txt"
        file_chilled_value_fault_status = txt_path + "/equipment_status/" + equipment_type + \
                                         "/fault_status/chilled_value.txt"
    elif equipment_type == "chilled_pump_secondary":
        # 二级冷冻水泵，只有水泵
        file_main_equipment_fault_status = None
        file_chilled_pump_fault_status = None
        file_chilled_pump_secondary_fault_status = txt_path + "/equipment_status/" + equipment_type + \
                                                  "/fault_status/chilled_pump_secondary.txt"
        file_chilled_value_fault_status = None
    elif equipment_type == "internal_combustion_engine":
        file_main_equipment_fault_status = txt_path + "/equipment_status/" + equipment_type + \
                                          "/fault_status/internal_combustion_engine.txt"
        file_chilled_pump_fault_status = None
        file_chilled_pump_secondary_fault_status = None
        file_chilled_value_fault_status = None
    else:
        file_main_equipment_fault_status = None
        file_chilled_pump_fault_status = None
        file_chilled_pump_secondary_fault_status = None
        file_chilled_value_fault_status = None
    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————
    # 冷却侧，冷却侧，冷却侧，冷却侧，冷却侧
    if equipment_type == "chiller" or equipment_type == "lithium_bromide":
        # 如果是chiller、lithium_bromide,则有冷却水泵+冷却塔
        file_cooling_pump_fault_status = txt_path + "/equipment_status/" + equipment_type + \
                                        "/fault_status/cooling_pump.txt"
        file_cooling_tower_fault_status = txt_path + "/equipment_status/" + equipment_type + \
                                         "/fault_status/cooling_tower.txt"
        file_cooling_value_fault_status = txt_path + "/equipment_status/" + equipment_type + \
                                         "/fault_status/cooling_value.txt"
        file_tower_value_fault_status = txt_path + "/equipment_status/" + equipment_type + \
                                       "/fault_status/tower_value.txt"
    elif equipment_type == "water_source_heat_pump":
        # 如果是water_source_heat_pump，则冷却侧没有冷却塔
        file_cooling_pump_fault_status = txt_path + "/equipment_status/" + equipment_type + \
                                        "/fault_status/cooling_pump.txt"
        file_cooling_tower_fault_status = None
        file_cooling_value_fault_status = txt_path + "/equipment_status/" + equipment_type + \
                                         "/fault_status/cooling_value.txt"
        file_tower_value_fault_status = None
    else:
        # 没有冷却侧
        file_cooling_pump_fault_status = None
        file_cooling_tower_fault_status = None
        file_cooling_value_fault_status = None
        file_tower_value_fault_status = None
    # 返回结果
    return file_main_equipment_fault_status, file_chilled_pump_fault_status, file_chilled_pump_secondary_fault_status, \
           file_cooling_pump_fault_status, file_cooling_tower_fault_status, file_chilled_value_fault_status, \
           file_cooling_value_fault_status, file_tower_value_fault_status


def get_station_equipment_remote_status_txt_path(equipment_type, txt_path):
    """
    能源站内设备远方状态txt文件路径

    Args:
        equipment_type:[string]，设备类型
        txt_path:[string]，储存记录的txt文件路径(用于区分是否是上层目录)

    Returns:

    """
    # 储存设备运行状态的文件路径
    # 冷冻侧，冷冻侧，冷冻侧，冷冻侧，冷冻侧
    if equipment_type == "chiller" or equipment_type == "water_source_heat_pump" or \
            equipment_type == "air_source_heat_pump" or equipment_type == "lithium_bromide":
        file_main_equipment_remote_status = txt_path + "/equipment_status/" + equipment_type + \
                                          "/remote_status/air_conditioner.txt"
        file_chilled_pump_remote_status = txt_path + "/equipment_status/" + equipment_type + \
                                        "/remote_status/chilled_pump.txt"
        file_chilled_pump_secondary_remote_status = txt_path + "/equipment_status/" + equipment_type + \
                                                  "/remote_status/chilled_pump_secondary.txt"
        file_chilled_value_remote_status = txt_path + "/equipment_status/" + equipment_type + \
                                         "/remote_status/chilled_value.txt"
    elif equipment_type == "energy_storage_equipment":
        # 蓄能装置，一级水泵是主设备
        file_main_equipment_remote_status = txt_path + "/equipment_status/" + equipment_type + \
                                          "/remote_status/chilled_pump.txt"
        file_chilled_pump_remote_status = None
        file_chilled_pump_secondary_remote_status = txt_path + "/equipment_status/" + equipment_type + \
                                                  "/remote_status/chilled_pump_secondary.txt"
        file_chilled_value_remote_status = txt_path + "/equipment_status/" + equipment_type + \
                                         "/remote_status/chilled_value.txt"
    elif equipment_type == "chilled_pump_secondary":
        # 二级冷冻水泵，只有水泵
        file_main_equipment_remote_status = None
        file_chilled_pump_remote_status = None
        file_chilled_pump_secondary_remote_status = txt_path + "/equipment_status/" + equipment_type + \
                                                  "/remote_status/chilled_pump_secondary.txt"
        file_chilled_value_remote_status = None
    elif equipment_type == "internal_combustion_engine":
        file_main_equipment_remote_status = txt_path + "/equipment_status/" + equipment_type + \
                                          "/remote_status/internal_combustion_engine.txt"
        file_chilled_pump_remote_status = None
        file_chilled_pump_secondary_remote_status = None
        file_chilled_value_remote_status = None
    else:
        file_main_equipment_remote_status = None
        file_chilled_pump_remote_status = None
        file_chilled_pump_secondary_remote_status = None
        file_chilled_value_remote_status = None
    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————
    # 冷却侧，冷却侧，冷却侧，冷却侧，冷却侧
    if equipment_type == "chiller" or equipment_type == "lithium_bromide":
        # 如果是chiller、lithium_bromide,则有冷却水泵+冷却塔
        file_cooling_pump_remote_status = txt_path + "/equipment_status/" + equipment_type + \
                                        "/remote_status/cooling_pump.txt"
        file_cooling_tower_remote_status = txt_path + "/equipment_status/" + equipment_type + \
                                         "/remote_status/cooling_tower.txt"
        file_cooling_value_remote_status = txt_path + "/equipment_status/" + equipment_type + \
                                         "/remote_status/cooling_value.txt"
        file_tower_value_remote_status = txt_path + "/equipment_status/" + equipment_type + \
                                       "/remote_status/tower_value.txt"
    elif equipment_type == "water_source_heat_pump":
        # 如果是water_source_heat_pump，则冷却侧没有冷却塔
        file_cooling_pump_remote_status = txt_path + "/equipment_status/" + equipment_type + \
                                        "/remote_status/cooling_pump.txt"
        file_cooling_tower_remote_status = None
        file_cooling_value_remote_status = txt_path + "/equipment_status/" + equipment_type + \
                                         "/remote_status/cooling_value.txt"
        file_tower_value_remote_status = None
    else:
        # 没有冷却侧
        file_cooling_pump_remote_status = None
        file_cooling_tower_remote_status = None
        file_cooling_value_remote_status = None
        file_tower_value_remote_status = None
    # 返回结果
    return file_main_equipment_remote_status, file_chilled_pump_remote_status, file_chilled_pump_secondary_remote_status, \
           file_cooling_pump_remote_status, file_cooling_tower_remote_status, file_chilled_value_remote_status, \
           file_cooling_value_remote_status, file_tower_value_remote_status


def get_station_equipment_repair_status_txt_path(equipment_type, txt_path):
    """
    能源站内设备维修状态txt文件路径

    Args:
        equipment_type:[string]，设备类型
        txt_path:[string]，储存记录的txt文件路径(用于区分是否是上层目录)

    Returns:

    """
    # 储存设备运行状态的文件路径
    # 冷冻侧，冷冻侧，冷冻侧，冷冻侧，冷冻侧
    if equipment_type == "chiller" or equipment_type == "water_source_heat_pump" or \
            equipment_type == "air_source_heat_pump" or equipment_type == "lithium_bromide":
        file_main_equipment_repair_status = txt_path + "/equipment_status/" + equipment_type + \
                                          "/repair_status/air_conditioner.txt"
        file_chilled_pump_repair_status = txt_path + "/equipment_status/" + equipment_type + \
                                        "/repair_status/chilled_pump.txt"
        file_chilled_pump_secondary_repair_status = txt_path + "/equipment_status/" + equipment_type + \
                                                  "/repair_status/chilled_pump_secondary.txt"
        file_chilled_value_repair_status = txt_path + "/equipment_status/" + equipment_type + \
                                         "/repair_status/chilled_value.txt"
    elif equipment_type == "energy_storage_equipment":
        # 蓄能装置，一级水泵是主设备
        file_main_equipment_repair_status = txt_path + "/equipment_status/" + equipment_type + \
                                          "/repair_status/chilled_pump.txt"
        file_chilled_pump_repair_status = None
        file_chilled_pump_secondary_repair_status = txt_path + "/equipment_status/" + equipment_type + \
                                                  "/repair_status/chilled_pump_secondary.txt"
        file_chilled_value_repair_status = txt_path + "/equipment_status/" + equipment_type + \
                                         "/repair_status/chilled_value.txt"
    elif equipment_type == "chilled_pump_secondary":
        # 二级冷冻水泵，只有水泵
        file_main_equipment_repair_status = None
        file_chilled_pump_repair_status = None
        file_chilled_pump_secondary_repair_status = txt_path + "/equipment_status/" + equipment_type + \
                                                  "/repair_status/chilled_pump_secondary.txt"
        file_chilled_value_repair_status = None
    elif equipment_type == "internal_combustion_engine":
        file_main_equipment_repair_status = txt_path + "/equipment_status/" + equipment_type + \
                                          "/repair_status/internal_combustion_engine.txt"
        file_chilled_pump_repair_status = None
        file_chilled_pump_secondary_repair_status = None
        file_chilled_value_repair_status = None
    else:
        file_main_equipment_repair_status = None
        file_chilled_pump_repair_status = None
        file_chilled_pump_secondary_repair_status = None
        file_chilled_value_repair_status = None
    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————
    # 冷却侧，冷却侧，冷却侧，冷却侧，冷却侧
    if equipment_type == "chiller" or equipment_type == "lithium_bromide":
        # 如果是chiller、lithium_bromide,则有冷却水泵+冷却塔
        file_cooling_pump_repair_status = txt_path + "/equipment_status/" + equipment_type + \
                                        "/repair_status/cooling_pump.txt"
        file_cooling_tower_repair_status = txt_path + "/equipment_status/" + equipment_type + \
                                         "/repair_status/cooling_tower.txt"
        file_cooling_value_repair_status = txt_path + "/equipment_status/" + equipment_type + \
                                         "/repair_status/cooling_value.txt"
        file_tower_value_repair_status = txt_path + "/equipment_status/" + equipment_type + \
                                       "/repair_status/tower_value.txt"
    elif equipment_type == "water_source_heat_pump":
        # 如果是water_source_heat_pump，则冷却侧没有冷却塔
        file_cooling_pump_repair_status = txt_path + "/equipment_status/" + equipment_type + \
                                        "/repair_status/cooling_pump.txt"
        file_cooling_tower_repair_status = None
        file_cooling_value_repair_status = txt_path + "/equipment_status/" + equipment_type + \
                                         "/repair_status/cooling_value.txt"
        file_tower_value_repair_status = None
    else:
        # 没有冷却侧
        file_cooling_pump_repair_status = None
        file_cooling_tower_repair_status = None
        file_cooling_value_repair_status = None
        file_tower_value_repair_status = None
    # 返回结果
    return file_main_equipment_repair_status, file_chilled_pump_repair_status, file_chilled_pump_secondary_repair_status, \
           file_cooling_pump_repair_status, file_cooling_tower_repair_status, file_chilled_value_repair_status, \
           file_cooling_value_repair_status, file_tower_value_repair_status


def get_station_equipment_operation_hours_txt_path(equipment_type, txt_path):
    """
    能源站内设备累计运行小时数txt文件路径

    Args:
        equipment_type:[string]，设备类型
        txt_path:[string]，储存记录的txt文件路径(用于区分是否是上层目录)

    Returns:

    """
    # 储存设备运行小时数的文件路径
    # 冷冻侧，冷冻侧，冷冻侧，冷冻侧，冷冻侧
    if equipment_type == "chiller" or equipment_type == "water_source_heat_pump" or \
            equipment_type == "air_source_heat_pump" or equipment_type == "lithium_bromide":
        file_main_equipment_operation_hours = txt_path + "/operation_hours/" + equipment_type + "/air_conditioner.txt"
        file_chilled_pump_operation_hours = txt_path + "/operation_hours/" + equipment_type + "/chilled_pump.txt"
        file_chilled_pump_secondary_operation_hours = txt_path + "/operation_hours/" + equipment_type + \
                                                      "/chilled_pump_secondary.txt"
        file_chilled_value_operation_hours = txt_path + "/operation_hours/" + equipment_type + "/chilled_value.txt"
    elif equipment_type == "energy_storage_equipment":
        # 蓄能装置，一级水泵是主设备
        file_main_equipment_operation_hours = txt_path + "/operation_hours/" + equipment_type + "/chilled_pump.txt"
        file_chilled_pump_operation_hours = None
        file_chilled_pump_secondary_operation_hours = txt_path + "/operation_hours/" + equipment_type + \
                                                      "/chilled_pump_secondary.txt"
        file_chilled_value_operation_hours = txt_path + "/operation_hours/" + equipment_type + "/chilled_value.txt"
    elif equipment_type == "chilled_pump_secondary":
        # 二级冷冻水泵，只有水泵
        file_main_equipment_operation_hours = None
        file_chilled_pump_operation_hours = None
        file_chilled_pump_secondary_operation_hours = txt_path + "/operation_hours/" + equipment_type + \
                                                      "/chilled_pump_secondary.txt"
        file_chilled_value_operation_hours = None
    elif equipment_type == "internal_combustion_engine":
        file_main_equipment_operation_hours = txt_path + "/operation_hours/" + equipment_type + \
                                              "/internal_combustion_engine.txt"
        file_chilled_pump_operation_hours = None
        file_chilled_pump_secondary_operation_hours = None
        file_chilled_value_operation_hours = None
    else:
        file_main_equipment_operation_hours = None
        file_chilled_pump_operation_hours = None
        file_chilled_pump_secondary_operation_hours = None
        file_chilled_value_operation_hours = None
    # ——————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————
    # 冷却侧，冷却侧，冷却侧，冷却侧，冷却侧
    if equipment_type == "chiller" or equipment_type == "lithium_bromide":
        # 如果是chiller、lithium_bromide,则有冷却水泵+冷却塔
        file_cooling_pump_operation_hours = txt_path + "/operation_hours/" + equipment_type + "/cooling_pump.txt"
        file_cooling_tower_operation_hours = txt_path + "/operation_hours/" + equipment_type + "/cooling_tower.txt"
        file_cooling_value_operation_hours = txt_path + "/operation_hours/" + equipment_type + "/cooling_value.txt"
        file_tower_value_operation_hours = txt_path + "/operation_hours/" + equipment_type + "/tower_value.txt"
    elif equipment_type == "water_source_heat_pump":
        # 如果是water_source_heat_pump，则冷却侧没有冷却塔
        file_cooling_pump_operation_hours = txt_path + "/operation_hours/" + equipment_type + "/cooling_pump.txt"
        file_cooling_tower_operation_hours = None
        file_cooling_value_operation_hours = txt_path + "/operation_hours/" + equipment_type + "/cooling_value.txt"
        file_tower_value_operation_hours = None
    else:
        # 没有冷却侧
        file_cooling_pump_operation_hours = None
        file_cooling_tower_operation_hours = None
        file_cooling_value_operation_hours = None
        file_tower_value_operation_hours = None
    # 返回结果
    return file_main_equipment_operation_hours, file_chilled_pump_operation_hours,\
           file_chilled_pump_secondary_operation_hours, file_cooling_pump_operation_hours, \
           file_cooling_tower_operation_hours, file_chilled_value_operation_hours, \
           file_cooling_value_operation_hours, file_tower_value_operation_hours


def get_user_equipment_real_value_txt_path(txt_path):
    """
    获取用户末端设备和室内末端测点设备的实际值txt文件路径

    Args:
        txt_path:[string]，储存记录的txt文件路径(用于区分是否是上层目录)

    Returns:

    """
    # 用户室内温湿度测点
    file_Tdi_value = txt_path + "/real_value/user_terminal/measure_point/Tdi.txt"
    file_Hri_value = txt_path + "/real_value/user_terminal/measure_point/Hri.txt"
    # 用户末端：新风、风机盘管、辐射、全空气处理箱
    file_fcu_Fea = txt_path + "/real_value/user_terminal/fan_control_unit/Fea.txt"
    file_fcu_Few = txt_path + "/real_value/user_terminal/fan_control_unit/Few.txt"
    file_fcu_Q = txt_path + "/real_value/user_terminal/fan_control_unit/Q.txt"
    file_fcu_Ted = txt_path + "/real_value/user_terminal/fan_control_unit/Ted.txt"
    file_fcu_Teo = txt_path + "/real_value/user_terminal/fan_control_unit/Teo.txt"
    file_mau_Few = txt_path + "/real_value/user_terminal/make_up_air_unit/Few.txt"
    file_mau_Fna = txt_path + "/real_value/user_terminal/make_up_air_unit/Fna.txt"
    file_mau_Q = txt_path + "/real_value/user_terminal/make_up_air_unit/Q.txt"
    file_mau_Ted = txt_path + "/real_value/user_terminal/make_up_air_unit/Ted.txt"
    file_mau_Teo = txt_path + "/real_value/user_terminal/make_up_air_unit/Teo.txt"
    file_rau_Few = txt_path + "/real_value/user_terminal/radiation_air_unit/Few.txt"
    file_rau_Q = txt_path + "/real_value/user_terminal/radiation_air_unit/Q.txt"
    file_rau_Ted = txt_path + "/real_value/user_terminal/radiation_air_unit/Ted.txt"
    file_rau_Teo = txt_path + "/real_value/user_terminal/radiation_air_unit/Teo.txt"
    # 返回结果
    return file_Tdi_value, file_Hri_value, file_fcu_Fea, file_fcu_Few, file_fcu_Q, file_fcu_Ted, file_fcu_Teo, \
           file_mau_Few, file_mau_Fna, file_mau_Q, file_mau_Ted, file_mau_Teo, file_rau_Few, file_rau_Q, \
           file_rau_Ted, file_rau_Teo


def get_user_equipment_status_txt_path(txt_path):
    """
    获取用户末端设备和室内末端测点设备的状态txt文件路径

    Args:
        txt_path:[string]，储存记录的txt文件路径(用于区分是否是上层目录)

    Returns:

    """
    # 用户室内温湿度测点
    file_Tdi_status = txt_path + "/equipment_status/user_terminal/Tdi.txt"
    file_Hri_status = txt_path + "/equipment_status/user_terminal/Hri.txt"
    # 用户末端：新风、风机盘管、全空气处理箱、辐射
    file_mau_status = txt_path + "/equipment_status/user_terminal/make_up_air_unit.txt"
    file_fcu_status = txt_path + "/equipment_status/user_terminal/fan_control_unit.txt"
    file_ahu_status = txt_path + "/equipment_status/user_terminal/air_handling_unit.txt"
    file_rau_status = txt_path + "/equipment_status/user_terminal/radiation_air_unit.txt"
    # 返回结果
    return file_Tdi_status, file_Hri_status, file_mau_status, file_fcu_status, file_ahu_status, file_rau_status


def get_environment_equipment_real_value_txt_path(txt_path):
    """
    获取环境参数测点的实际值txt文件路径

    Args:
        txt_path: [string]，储存记录的txt文件路径(用于区分是否是上层目录)

    Returns:

    """
    file_Tdo_value = txt_path + "/real_value/environment/Tdo.txt"
    file_Hro_value = txt_path + "/real_value/environment/Hro.txt"
    file_Tsw_value = txt_path + "/real_value/environment/Tsw.txt"
    # 返回结果
    return file_Tdo_value, file_Hro_value, file_Tsw_value


def get_environment_equipment_status_txt_path(txt_path):
    """
    获取环境参数测点的状态txt文件路径

    Args:
        txt_path: [string]，储存记录的txt文件路径(用于区分是否是上层目录)

    Returns:

    """
    file_Tdo_status = txt_path + "/equipment_status/environment/Tdo.txt"
    file_Hro_status = txt_path + "/equipment_status/environment/Hro.txt"
    file_Tsw_status = txt_path + "/equipment_status/environment/Tsw.txt"
    # 返回结果
    return file_Tdo_status, file_Hro_status, file_Tsw_status