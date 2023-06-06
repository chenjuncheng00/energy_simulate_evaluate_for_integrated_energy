
def main_input_name():
    """
    整个模型的输入，名称

    Returns:

    """
    # 冷水机模型
    chiller_input = chiller_input_name()[0]
    # 空气源热泵模型
    air_source_heat_pump_input = air_source_heat_pump_input_name()[0]
    # 蓄冷水罐模型
    storage_input = cold_storage_input_name()[0]
    # 冷却塔直接供冷模型
    tower_chilled_input = tower_chilled_input_name()
    # 用户末端
    user_input = user_load_input_name()
    # 模型总输入
    model_input = chiller_input + air_source_heat_pump_input + storage_input + \
                  tower_chilled_input + user_input
    # 返回结果
    return model_input

def chiller_input_name():
    """
    冷水机模型输入，名称

    Returns:

    """
    # 空调主机冷冻水温度设定值
    main_equipment_Teo_set = ['chiller_Teo_set']
    # 冷冻水泵，转速，0到50
    chilled_pump = ['chiller_f_chilled_pump1', 'chiller_f_chilled_pump2', 'chiller_f_chilled_pump3',
                    'chiller_f_chilled_pump4', 'chiller_f_chilled_pump5', 'chiller_f_chilled_pump6']
    # 冷却水泵，转速，0到50
    cooling_pump = ['chiller_f_cooling_pump1', 'chiller_f_cooling_pump2', 'chiller_f_cooling_pump3',
                    'chiller_f_cooling_pump4', 'chiller_f_cooling_pump5', 'chiller_f_cooling_pump6']
    # 冷却塔风机频率
    cooling_tower = ['chiller_f_cooling_tower1', 'chiller_f_cooling_tower2', 'chiller_f_cooling_tower3',
                     'chiller_f_cooling_tower4', 'chiller_f_cooling_tower5', 'chiller_f_cooling_tower6']
    # 总输入
    chiller_input = main_equipment_Teo_set + chilled_pump + cooling_pump + cooling_tower
    # 返回结构
    return chiller_input, main_equipment_Teo_set, chilled_pump, cooling_pump, cooling_tower,


def air_source_heat_pump_input_name():
    """
    空气源热泵模型输入，名称

    Returns:

    """
    # 空调主机冷冻水温度设定值
    main_equipment_Teo_set = ['ashp_Teo_set']
    # 冷冻水泵，转速，0到50
    chilled_pump = ['ashp_f_chilled_pump1', 'ashp_f_chilled_pump2', 'ashp_f_chilled_pump3', 'ashp_f_chilled_pump4']
    # 总输入
    air_source_heat_pump_input = main_equipment_Teo_set + chilled_pump
    # 返回结构
    return air_source_heat_pump_input, main_equipment_Teo_set, chilled_pump


def cold_storage_input_name():
    """
    蓄冷水罐模型输入，名称

    Returns:

    """
    # 冷冻水泵，转速，0到50
    chilled_pump = ['storage_f_chilled_pump1', 'storage_f_chilled_pump2',
                    'storage_f_chilled_pump3', 'storage_f_chilled_pump4']
    # 总输入
    storage_input = chilled_pump
    # 返回结果
    return storage_input, chilled_pump


def tower_chilled_input_name():
    """
    冷却塔直接供冷模型输入，名称

    Returns:

    """
    # 冷冻水泵，转速，0到50
    chilled_pump = ['tower_chilled_f_chilled_pump1', 'tower_chilled_f_chilled_pump2',
                    'tower_chilled_f_chilled_pump3', 'tower_chilled_f_chilled_pump4']
    # 返回结果
    return chilled_pump


def user_load_input_name():
    """
    用户末端负荷模型输入，名称

    Returns:

    """
    # 冷冻水泵，转速，0到50
    chilled_pump = ['user_f_chilled_pump1', 'user_f_chilled_pump2']
    # 返回结果
    return chilled_pump