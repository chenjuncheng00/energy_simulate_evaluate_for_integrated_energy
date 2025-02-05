"""
FMU模型输入数值的默认值：
1、用户侧水泵默认开启，其它设备都默认关闭；
2、数据顺序与model_fmu_input_type中一致
"""

def main_input_data_default(load_mode=0):
    """
    整个模型的输入，数值
    Args:
        load_mode: [int]，0：user_load；1：simple_load

    Returns:

    """
    model_input = environment_input_data_default(load_mode) + chiller_input_data_default() + \
                  air_source_heat_pump_input_data_default() + cold_storage_input_data_default() + \
                  load_input_data_default(load_mode)
    return model_input


def environment_input_data_default(load_mode):
    """
    环境温湿度输入，名称和数据类型
    Args:
        load_mode: [int]，0：user_load；1：simple_load

    Returns:

    """
    Tdo = [35]
    Two = [27]
    if load_mode == 0:
        environment_input = Tdo + Two
    else:
        # simple_load没有天气数据
        environment_input = []
    # 返回结果
    return environment_input


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
    chilled_valve = [0, 0, 0, 0, 0, 0]
    # 冷却阀门
    cooling_valve = [0, 0, 0, 0, 0, 0]
    # 冷却塔阀门
    tower_valve = [0, 0, 0, 0, 0, 0]
    # 向用户侧供冷阀门
    user_valve = [0, 0]
    # 总输入
    chiller_input = main_equipment + chilled_pump + cooling_pump + cooling_tower + \
                    chilled_valve + cooling_valve + tower_valve + user_valve
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
    chilled_valve = [0, 0, 0, 0]
    # 总输入
    air_source_heat_pump_input = main_equipment + chilled_pump + chilled_valve
    # 返回结构
    return air_source_heat_pump_input


def cold_storage_input_data_default():
    """
    蓄冷水罐模型输入，数值

    Returns:

    """
    # 冷冻水泵
    chilled_pump = [0, 0, 0, 0]
    # 阀门列表：先是蓄冷阀门，然后是放冷阀门
    # 从冷水机蓄冷阀门
    chiller_valve = [0, 0, 0]
    # 向用户侧供冷阀门
    user_valve = [0, 0, 0]
    # 总输入
    storage_input = chilled_pump + chiller_valve + user_valve
    # 返回结果
    return storage_input


def load_input_data_default(load_mode):
    """

    Args:
        load_mode: [int]，0：user_load；1：simple_load

    Returns:

    """
    if load_mode == 0:
        load_input_data = user_load_input_data_default()
    else:
        load_input_data = simple_load_input_data_default()
    # 返回结果
    return load_input_data


def user_load_input_data_default():
    """
    用户末端负荷模型输入，数值

    Returns:

    """
    # 冷冻水泵
    chilled_pump = [50, 50]
    # 返回结果
    return chilled_pump

def simple_load_input_data_default():
    """
    简单的负荷模型输入，数值
    Returns:

    """
    # 负荷值(冷负荷：正值；热负荷：负值)，单位：W
    Q_input = [0]
    # 返回结果
    return Q_input