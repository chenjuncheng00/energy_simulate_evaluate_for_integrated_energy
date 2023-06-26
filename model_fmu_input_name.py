from model_fmu_input_type import chiller_input_type, air_source_heat_pump_input_type, cold_storage_input_type, \
                                 tower_chilled_input_type, user_load_input_type, simple_load_input_type, \
                                 environment_input_type

def main_model_input_name(load_mode=0):
    """
    整个模型的输入，名称
    Args:
        load_mode: [int]，0：user_load；1：simple_load

    Returns:

    """
    # 冷水机模型
    chiller_input = get_fmu_input_name(chiller_input_type()[0])
    # 空气源热泵模型
    air_source_heat_pump_input = get_fmu_input_name(air_source_heat_pump_input_type()[0])
    # 蓄冷水罐模型
    storage_input = get_fmu_input_name(cold_storage_input_type()[0])
    # 冷却塔直接供冷模型
    tower_chilled_input = get_fmu_input_name(tower_chilled_input_type())
    # 用户末端
    if load_mode == 0:
        user_input = get_fmu_input_name(user_load_input_type())
    else:
        user_input = get_fmu_input_name(simple_load_input_type())
    # 环境参数
    environment_input = get_fmu_input_name(environment_input_type()[0])
    # 模型总输入
    model_input = chiller_input + air_source_heat_pump_input + storage_input + \
                  tower_chilled_input + user_input + environment_input
    # 返回结果
    return model_input


def get_fmu_input_name(input_type_list):
    """
    根据input_type_list，得到input_name_list
    Args:
        input_type_list: [list]，模型的输入类型和名称

    Returns:

    """
    input_name_list = []
    for i in range(len(input_type_list)):
        tmp_input_list = list(input_type_list[i])
        for j in range(len(tmp_input_list)):
            tmp_name = tmp_input_list[j]
            if isinstance(tmp_name, str):
                input_name_list.append(tmp_name)
    # 返回结果
    return input_name_list