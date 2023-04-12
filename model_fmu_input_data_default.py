"""
FMU模型输入数值的默认值：
1、用户侧水泵默认开启，其它设备都默认关闭；
2、数据顺序与model_fmu_input_type中一致
"""

def main_input_data_default():
    """
    整个模型的输入，数值

    Returns:

    """
    model_input = environment_input_data_default() + chiller_input_data_default() + \
                  air_source_heat_pump_input_data_default() + cold_storage_input_data_default() + \
                  tower_chilled_input_data_default() + user_load_input_data_default()
    return model_input


def chiller_input_data_default():
    """
    冷水机模型输入，数值

    Returns:

    """
    # 空调主机
    main_equipment = [False, False, False, False, False, False, 8]
    # 冷冻水泵
    chilled_pump = [0, 0, 0, 0, 0, 0]
    # 冷却水泵
    cooling_pump = [0, 0, 0, 0, 0, 0]
    # 冷却塔风机
    cooling_tower = [0, 0, 0, 0, 0, 0]
    # 冷冻阀门
    chilled_value = [0, 0, 0, 0, 0, 0]
    # 冷却阀门
    cooling_value = [0, 0, 0, 0, 0, 0]
    # 冷却塔阀门
    tower_value = [0, 0, 0, 0, 0, 0]
    # 冷却塔直接供冷阀门
    tower_chilled_value = [0, 0]
    # 向用户侧供冷阀门
    user_value = [0, 0]
    # 总输入
    chiller_input = main_equipment + chilled_pump + cooling_pump + cooling_tower + \
                    chilled_value + cooling_value + tower_value + tower_chilled_value + user_value
    # 返回结构
    return chiller_input


def air_source_heat_pump_input_data_default():
    """
    空气源热泵模型输入，数值

    Returns:

    """
    # 空调主机
    main_equipment = [False, False, False, False, 8]
    # 冷冻水泵
    chilled_pump = [0, 0, 0, 0]
    # 冷冻阀门
    chilled_value = [0, 0, 0, 0]
    # 总输入
    air_source_heat_pump_input = main_equipment + chilled_pump + chilled_value
    # 返回结构
    return air_source_heat_pump_input


def cold_storage_input_data_default():
    """
    蓄冷水罐模型输入，数值

    Returns:

    """
    # 冷冻水泵
    chilled_pump = [0, 0, 0, 0]
    # 向用户侧供冷阀门
    user_value = [0, 0, 0]
    # 从冷水机蓄冷阀门
    chiller_value = [0, 0, 0]
    # 总输入
    storage_input = chilled_pump + user_value + chiller_value
    # 返回结果
    return storage_input


def tower_chilled_input_data_default():
    """
    冷却塔直接供冷模型输入，数值

    Returns:

    """
    # 冷冻水泵
    chilled_pump = [0, 0, 0, 0]
    # 返回结果
    return chilled_pump


def user_load_input_data_default():
    """
    用户末端负荷模型输入，数值

    Returns:

    """
    # 冷冻水泵
    chilled_pump = [1480, 1480]
    # 返回结果
    return chilled_pump


def environment_input_data_default():
    """
    环境温湿度输入，名称和数据类型

    Returns:

    """
    Tdo = [30]
    Two = [25]
    environment_input = Tdo + Two
    # 返回结果
    return environment_input