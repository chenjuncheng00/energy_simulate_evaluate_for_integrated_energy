import numpy as np

def main_model_input_type():
    """
    整个模型的输入，名称和数据类型

    Returns:

    """
    # 仿真时间
    time_input = [('time', np.float_)]
    # 环境参数模型
    environment_input = environment_input_type()[0]
    # 冷水机模型
    chiller_input = chiller_input_type()[0]
    # 空气源热泵模型
    air_source_heat_pump_input = air_source_heat_pump_input_type()[0]
    # 蓄冷水罐模型
    storage_input = cold_storage_input_type()[0]
    # 冷却塔直接供冷模型
    tower_chilled_input = tower_chilled_input_type()
    # 用户负荷模型
    user_input = user_load_input_type()
    # 模型总输入
    model_input = time_input + environment_input + chiller_input + air_source_heat_pump_input + storage_input + \
                  tower_chilled_input + user_input
    # 返回结果
    return model_input


def chiller_input_type():
    """
    冷水机模型输入，名称和数据类型

    Returns:

    """
    # 空调主机，开关，True或False
    main_equipment_turn = [('turn_chiller1', np.bool_), ('turn_chiller2', np.bool_), ('turn_chiller3', np.bool_),
                           ('turn_chiller4', np.bool_), ('turn_chiller5', np.bool_), ('turn_chiller6', np.bool_)]
    main_equipment_Teo_set = [('chiller_Teo_set', np.float_)]
    # 冷冻水泵，转速，0到1480
    chilled_pump = [('chiller_f_chilled_pump1', np.float_), ('chiller_f_chilled_pump2', np.float_),
                    ('chiller_f_chilled_pump3', np.float_), ('chiller_f_chilled_pump4', np.float_),
                    ('chiller_f_chilled_pump5', np.float_), ('chiller_f_chilled_pump6', np.float_)]
    # 冷却水泵，转速，0到1480
    cooling_pump = [('chiller_f_cooling_pump1', np.float_), ('chiller_f_cooling_pump2', np.float_),
                    ('chiller_f_cooling_pump3', np.float_), ('chiller_f_cooling_pump4', np.float_),
                    ('chiller_f_cooling_pump5', np.float_), ('chiller_f_cooling_pump6', np.float_)]
    # 冷却塔风机，转速比，0到1
    cooling_tower = [('chiller_f_cooling_tower1', np.float_), ('chiller_f_cooling_tower2', np.float_),
                     ('chiller_f_cooling_tower3', np.float_), ('chiller_f_cooling_tower4', np.float_),
                     ('chiller_f_cooling_tower5', np.float_), ('chiller_f_cooling_tower6', np.float_)]
    # 冷冻阀门，开度比，0到1
    chilled_value = [('chiller_turn_chilled_value1', np.float_), ('chiller_turn_chilled_value2', np.float_),
                     ('chiller_turn_chilled_value3', np.float_), ('chiller_turn_chilled_value4', np.float_),
                     ('chiller_turn_chilled_value5', np.float_), ('chiller_turn_chilled_value6', np.float_)]
    # 冷却阀门，开度比，0到1
    cooling_value = [('chiller_turn_cooling_value1', np.float_), ('chiller_turn_cooling_value2', np.float_),
                     ('chiller_turn_cooling_value3', np.float_), ('chiller_turn_cooling_value4', np.float_),
                     ('chiller_turn_cooling_value5', np.float_), ('chiller_turn_cooling_value6', np.float_)]
    # 冷却塔阀门，开度比，0到1
    tower_value = [('chiller_turn_tower_value1', np.float_), ('chiller_turn_tower_value2', np.float_),
                   ('chiller_turn_tower_value3', np.float_), ('chiller_turn_tower_value4', np.float_),
                   ('chiller_turn_tower_value5', np.float_), ('chiller_turn_tower_value6', np.float_)]
    # 冷却塔直接供冷阀门，开度比，0到1
    tower_chilled_value = [('chiller_turn_tower_chilled_value1', np.float_),
                           ('chiller_turn_tower_chilled_value2', np.float_)]
    # 向用户侧供冷阀门，开度比，0到1
    user_value = [('chiller_turn_user_value1', np.float_), ('chiller_turn_user_value2', np.float_)]
    # 总输入
    chiller_input = main_equipment_turn + main_equipment_Teo_set + chilled_pump + cooling_pump + cooling_tower + \
                    chilled_value + cooling_value + tower_value + tower_chilled_value + user_value
    # 返回结构
    return chiller_input, main_equipment_turn, main_equipment_Teo_set, chilled_pump, cooling_pump, cooling_tower, \
           chilled_value, cooling_value, tower_value, tower_chilled_value, user_value


def air_source_heat_pump_input_type():
    """
    空气源热泵模型输入，名称和数据类型

    Returns:

    """
    # 空调主机，开关，True或False
    main_equipment_turn = [('turn_ashp1', np.bool_), ('turn_ashp2', np.bool_),
                           ('turn_ashp3', np.bool_), ('turn_ashp4', np.bool_)]
    main_equipment_Teo_set = [('ashp_Teo_set', np.float_)]
    # 冷冻水泵，转速，0到1480
    chilled_pump = [('ashp_f_chilled_pump1', np.float_), ('ashp_f_chilled_pump2', np.float_),
                    ('ashp_f_chilled_pump3', np.float_), ('ashp_f_chilled_pump4', np.float_)]
    # 冷冻阀门，开度比，0到1
    chilled_value = [('ashp_turn_chilled_value1', np.float_), ('ashp_turn_chilled_value2', np.float_),
                     ('ashp_turn_chilled_value3', np.float_), ('ashp_turn_chilled_value4', np.float_)]
    # 总输入
    air_source_heat_pump_input = main_equipment_turn + main_equipment_Teo_set + chilled_pump + chilled_value
    # 返回结构
    return air_source_heat_pump_input, main_equipment_turn, main_equipment_Teo_set, chilled_pump, chilled_value


def cold_storage_input_type():
    """
    蓄冷水罐模型输入，名称和数据类型

    Returns:

    """
    # 冷冻水泵，转速，0到1480
    chilled_pump = [('storage_f_chilled_pump1', np.float_), ('storage_f_chilled_pump2', np.float_),
                    ('storage_f_chilled_pump3', np.float_), ('storage_f_chilled_pump4', np.float_)]
    # 向用户侧供冷阀门，开度比，0到1
    user_value = [('storage_turn_user_value1', np.float_), ('storage_turn_user_value2', np.float_),
                  ('storage_turn_user_value3', np.float_)]
    # 从冷水机蓄冷阀门，开度比，0到1
    chiller_value = [('storage_turn_chiller_value1', np.float_), ('storage_turn_chiller_value2', np.float_),
                     ('storage_turn_chiller_value3', np.float_)]
    # 总输入
    storage_input = chilled_pump + user_value + chiller_value
    # 返回结果
    return storage_input, chilled_pump, user_value, chiller_value


def tower_chilled_input_type():
    """
    冷却塔直接供冷模型输入，名称和数据类型

    Returns:

    """
    # 冷冻水泵，转速，0到1480
    chilled_pump = [('tower_chilled_f_pump1', np.float_), ('tower_chilled_f_pump2', np.float_),
                    ('tower_chilled_f_pump3', np.float_), ('tower_chilled_f_pump4', np.float_)]
    # 返回结果
    return chilled_pump


def user_load_input_type():
    """
    用户末端负荷模型输入，名称和数据类型

    Returns:

    """
    # 冷冻水泵，转速，0到1480
    chilled_pump = [('user_f_chilled_pump1', np.float_), ('user_f_chilled_pump2', np.float_)]
    # 返回结果
    return chilled_pump


def environment_input_type():
    """
    环境温湿度输入，名称和数据类型

    Returns:

    """
    Tdo = [('Tdo', np.float_)]
    Two = [('Two', np.float_)]
    environment_input = Tdo + Two
    # 返回结果
    return environment_input, Tdo, Two