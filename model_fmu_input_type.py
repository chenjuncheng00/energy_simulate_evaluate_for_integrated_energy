import numpy as np

def main_model_input_type(load_mode=0):
    """
    整个模型的输入，名称和数据类型
    Args:
        load_mode: [int]，0：user_load；1：simple_load

    Returns:

    """
    # 仿真时间
    time_input = [("time", np.float_)]
    # 环境参数模型
    environment_input = environment_input_type(load_mode)[0]
    # 冷水机模型
    chiller_input = chiller_input_type()[0]
    # 空气源热泵模型
    air_source_heat_pump_input = air_source_heat_pump_input_type()[0]
    # 蓄冷水罐模型
    storage_input = cold_storage_input_type()[0]
    # 冷却塔直接供冷模型
    tower_chilled_input = tower_chilled_input_type()
    # 用户负荷模型
    load_input = load_input_type(load_mode)
    # 模型总输入
    model_input = time_input + environment_input + chiller_input + air_source_heat_pump_input + storage_input + \
                  tower_chilled_input + load_input
    # 返回结果
    return model_input


def environment_input_type(load_mode):
    """
    环境温湿度输入，名称和数据类型
    Args:
        load_mode: [int]，0：user_load；1：simple_load

    Returns:

    """
    Tdo = [("Tdo", np.float_)]
    Two = [("Two", np.float_)]
    if load_mode == 0:
        environment_input = Tdo + Two
    else:
        # simple_load没有天气数据
        environment_input = []
    # 返回结果
    return environment_input, Tdo, Two


def chiller_input_type():
    """
    冷水机模型输入，名称和数据类型

    Returns:

    """
    # 空调主机，开关，True或False
    main_equipment_turn = [("chiller_turn1", np.bool_), ("chiller_turn2", np.bool_), ("chiller_turn3", np.bool_),
                           ("chiller_turn4", np.bool_), ("chiller_turn5", np.bool_), ("chiller_turn6", np.bool_)]
    main_equipment_Teo_set = [("chiller_Teo_set", np.float_)]
    # 冷冻水泵，转速，0到50
    chilled_pump = [("chiller_f_chilled_pump1", np.float_), ("chiller_f_chilled_pump2", np.float_),
                    ("chiller_f_chilled_pump3", np.float_), ("chiller_f_chilled_pump4", np.float_),
                    ("chiller_f_chilled_pump5", np.float_), ("chiller_f_chilled_pump6", np.float_)]
    # 冷却水泵，转速，0到50
    cooling_pump = [("chiller_f_cooling_pump1", np.float_), ("chiller_f_cooling_pump2", np.float_),
                    ("chiller_f_cooling_pump3", np.float_), ("chiller_f_cooling_pump4", np.float_),
                    ("chiller_f_cooling_pump5", np.float_), ("chiller_f_cooling_pump6", np.float_)]
    # 冷却塔风机，转速比，0到1
    cooling_tower = [("chiller_f_cooling_tower1", np.float_), ("chiller_f_cooling_tower2", np.float_),
                     ("chiller_f_cooling_tower3", np.float_), ("chiller_f_cooling_tower4", np.float_),
                     ("chiller_f_cooling_tower5", np.float_), ("chiller_f_cooling_tower6", np.float_)]
    # 冷冻阀门，开度比，0到1
    chilled_valve = [("chiller_turn_chilled_valve1", np.float_), ("chiller_turn_chilled_valve2", np.float_),
                     ("chiller_turn_chilled_valve3", np.float_), ("chiller_turn_chilled_valve4", np.float_),
                     ("chiller_turn_chilled_valve5", np.float_), ("chiller_turn_chilled_valve6", np.float_)]
    # 冷却阀门，开度比，0到1
    cooling_valve = [("chiller_turn_cooling_valve1", np.float_), ("chiller_turn_cooling_valve2", np.float_),
                     ("chiller_turn_cooling_valve3", np.float_), ("chiller_turn_cooling_valve4", np.float_),
                     ("chiller_turn_cooling_valve5", np.float_), ("chiller_turn_cooling_valve6", np.float_)]
    # 冷却塔阀门，开度比，0到1
    tower_valve = [("chiller_turn_tower_valve1", np.float_), ("chiller_turn_tower_valve2", np.float_),
                   ("chiller_turn_tower_valve3", np.float_), ("chiller_turn_tower_valve4", np.float_),
                   ("chiller_turn_tower_valve5", np.float_), ("chiller_turn_tower_valve6", np.float_)]
    # 冷却塔直接供冷阀门，开度比，0到1
    tower_chilled_valve = [("chiller_turn_tower_chilled_valve1", np.float_),
                           ("chiller_turn_tower_chilled_valve2", np.float_)]
    # 向用户侧供冷阀门，开度比，0到1
    user_valve = [("chiller_turn_user_valve1", np.float_), ("chiller_turn_user_valve2", np.float_)]
    # 总输入
    chiller_input = main_equipment_turn + main_equipment_Teo_set + chilled_pump + cooling_pump + cooling_tower + \
                    chilled_valve + cooling_valve + tower_valve + tower_chilled_valve + user_valve
    # 返回结构
    return chiller_input, main_equipment_turn, main_equipment_Teo_set, chilled_pump, cooling_pump, cooling_tower, \
           chilled_valve, cooling_valve, tower_valve, tower_chilled_valve, user_valve


def air_source_heat_pump_input_type():
    """
    空气源热泵模型输入，名称和数据类型

    Returns:

    """
    # 空调主机，开关，True或False
    main_equipment_turn = [("ashp_turn1", np.bool_), ("ashp_turn2", np.bool_),
                           ("ashp_turn3", np.bool_), ("ashp_turn4", np.bool_)]
    main_equipment_Teo_set = [("ashp_Teo_set", np.float_)]
    # 冷冻水泵，转速，0到50
    chilled_pump = [("ashp_f_chilled_pump1", np.float_), ("ashp_f_chilled_pump2", np.float_),
                    ("ashp_f_chilled_pump3", np.float_), ("ashp_f_chilled_pump4", np.float_)]
    # 冷冻阀门，开度比，0到1
    chilled_valve = [("ashp_turn_chilled_valve1", np.float_), ("ashp_turn_chilled_valve2", np.float_),
                     ("ashp_turn_chilled_valve3", np.float_), ("ashp_turn_chilled_valve4", np.float_)]
    # 总输入
    air_source_heat_pump_input = main_equipment_turn + main_equipment_Teo_set + chilled_pump + chilled_valve
    # 返回结构
    return air_source_heat_pump_input, main_equipment_turn, main_equipment_Teo_set, chilled_pump, chilled_valve


def cold_storage_input_type():
    """
    蓄冷水罐模型输入，名称和数据类型

    Returns:

    """
    # 冷冻水泵，转速，0到50
    chilled_pump = [("storage_f_chilled_pump1", np.float_), ("storage_f_chilled_pump2", np.float_),
                    ("storage_f_chilled_pump3", np.float_), ("storage_f_chilled_pump4", np.float_)]
    # 阀门列表：先是蓄冷阀门，然后是放冷阀门
    # 从冷水机蓄冷阀门，开度比，0到1
    chiller_valve = [("storage_turn_chilled_valve1", np.float_), ("storage_turn_chilled_valve2", np.float_),
                     ("storage_turn_chilled_valve3", np.float_)]
    # 向用户侧供冷阀门，开度比，0到1
    user_valve = [("storage_turn_chilled_valve4", np.float_), ("storage_turn_chilled_valve5", np.float_),
                  ("storage_turn_chilled_valve6", np.float_)]
    # 总输入
    storage_input = chilled_pump + chiller_valve + user_valve
    # 返回结果
    return storage_input, chilled_pump, chiller_valve, user_valve


def tower_chilled_input_type():
    """
    冷却塔直接供冷模型输入，名称和数据类型

    Returns:

    """
    # 冷冻水泵，转速，0到50
    chilled_pump = [("tower_chilled_f_chilled_pump1", np.float_), ("tower_chilled_f_chilled_pump2", np.float_),
                    ("tower_chilled_f_chilled_pump3", np.float_), ("tower_chilled_f_chilled_pump4", np.float_)]
    # 返回结果
    return chilled_pump


def load_input_type(load_mode):
    """

    Args:
        load_mode: [int]，0：user_load；1：simple_load

    Returns:

    """
    if load_mode == 0:
        load_input = user_load_input_type()
    else:
        load_input = simple_load_input_type()
    # 返回结果
    return load_input


def user_load_input_type():
    """
    用户末端负荷模型输入，名称和数据类型

    Returns:

    """
    # 冷冻水泵，转速，0到50
    chilled_pump = [("user_f_chilled_pump1", np.float_), ("user_f_chilled_pump2", np.float_)]
    # 返回结果
    return chilled_pump


def simple_load_input_type():
    """
    简单的负荷模型输入，名称和数据类型
    Returns:

    """
    # 负荷值(冷负荷：正值；热负荷：负值)，单位：W
    Q_input = [("Q_input", np.float_)]
    # 返回结果
    return Q_input