
def air_source_heat_pump_default_status(n_air_source_heat_pump, n_ashp_chilled_pump):
    """
    空气源热泵默认开关状态
    Args:
        n_air_source_heat_pump: [int]，空气源热泵装机数量
        n_ashp_chilled_pump: [int]，一级冷冻水泵装机数量

    Returns:

    """
    # 系统级阀门(向用户侧供冷阀门、冷却塔直接供冷阀门)，数量默认是2
    n_system_valve = 2
    # 设备实时值
    real_value_dict = dict()
    real_value_dict["real_value"] = dict()
    # DO状态
    DO_status = dict()
    DO_status["DO"] = dict()
    DO_status["DO"]["开关状态"] = 0
    DO_status["DO"]["报警状态"] = 1
    DO_status["DO"]["故障状态"] = 1
    DO_status["DO"]["远方状态"] = 1
    DO_status["DO"]["维修状态"] = 1
    # 各个设备
    for i in range(n_air_source_heat_pump):
        tmp_name = "空气源热泵_" + str(i)
        real_value_dict["real_value"][tmp_name] = DO_status
    for i in range(n_air_source_heat_pump):
        tmp_name = "冷冻阀门_" + str(i)
        real_value_dict["real_value"][tmp_name] = DO_status
    for i in range(n_ashp_chilled_pump):
        tmp_name = "一级冷冻水泵_" + str(i)
        real_value_dict["real_value"][tmp_name] = DO_status
    for i in range(n_system_valve):
        tmp_name = "向用户侧供冷阀门_" + str(i)
        real_value_dict["real_value"][tmp_name] = DO_status
    # 返回结果
    return real_value_dict


def chiller_default_status(n_chiller, n_chiller_chilled_pump, n_chiller_cooling_pump, n_chiller_cooling_tower):
    """

    Args:
        n_chiller: [int]，冷水机装机总数量
        n_chiller_chilled_pump: [int]，一级冷冻水泵装机总数量
        n_chiller_cooling_pump: [int]，冷却水泵装机总数量
        n_chiller_cooling_tower: [int]，冷却塔装机总数量

    Returns:

    """
    # 系统级阀门(向用户侧供冷阀门、冷却塔直接供冷阀门)，数量默认是2
    n_system_valve = 2
    # 设备实时值
    real_value_dict = dict()
    real_value_dict["real_value"] = dict()
    # DO状态
    DO_status = dict()
    DO_status["DO"] = dict()
    DO_status["DO"]["开关状态"] = 0
    DO_status["DO"]["报警状态"] = 1
    DO_status["DO"]["故障状态"] = 1
    DO_status["DO"]["远方状态"] = 1
    DO_status["DO"]["维修状态"] = 1
    # 各个设备
    for i in range(n_chiller):
        tmp_name = "冷水机_" + str(i)
        real_value_dict["real_value"][tmp_name] = DO_status
    for i in range(n_chiller):
        tmp_name = "冷冻阀门_" + str(i)
        real_value_dict["real_value"][tmp_name] = DO_status
    for i in range(n_chiller):
        tmp_name = "冷却阀门_" + str(i)
        real_value_dict["real_value"][tmp_name] = DO_status
    for i in range(n_chiller_chilled_pump):
        tmp_name = "一级冷冻水泵_" + str(i)
        real_value_dict["real_value"][tmp_name] = DO_status
    for i in range(n_chiller_cooling_pump):
        tmp_name = "冷却水泵_" + str(i)
        real_value_dict["real_value"][tmp_name] = DO_status
    for i in range(n_chiller_cooling_tower):
        tmp_name = "冷却塔_" + str(i)
        real_value_dict["real_value"][tmp_name] = DO_status
    for i in range(n_chiller_cooling_tower):
        tmp_name = "冷却塔阀门_" + str(i)
        real_value_dict["real_value"][tmp_name] = DO_status
    for i in range(n_system_valve):
        tmp_name = "向用户侧供冷阀门_" + str(i)
        real_value_dict["real_value"][tmp_name] = DO_status
    for i in range(n_system_valve):
        tmp_name = "冷却塔直接供冷阀门_" + str(i)
        real_value_dict["real_value"][tmp_name] = DO_status
    # 返回结果
    return real_value_dict


def storage_default_status(n_chilled_valve, n_storage_chilled_pump):
    """

    Args:
        n_chilled_valve: [int]，冷冻阀门数量
        n_storage_chilled_pump: [int]，冷冻水泵数量

    Returns:

    """
    # 设备实时值
    real_value_dict = dict()
    real_value_dict["real_value"] = dict()
    # DO状态
    DO_status = dict()
    DO_status["DO"] = dict()
    DO_status["DO"]["开关状态"] = 0
    DO_status["DO"]["报警状态"] = 1
    DO_status["DO"]["故障状态"] = 1
    DO_status["DO"]["远方状态"] = 1
    DO_status["DO"]["维修状态"] = 1
    # 各个设备
    for i in range(n_chilled_valve):
        tmp_name = "冷冻阀门_" + str(i)
        real_value_dict["real_value"][tmp_name] = DO_status
    for i in range(n_storage_chilled_pump):
        tmp_name = "一级冷冻水泵_" + str(i)
        real_value_dict["real_value"][tmp_name] = DO_status
    # 返回结果
    return real_value_dict


def tower_chilled_default_status(n_tower_chilled_pump):
    """

    Args:
        n_tower_chilled_pump: [int]，冷冻水泵数量

    Returns:

    """
    # 设备实时值
    real_value_dict = dict()
    real_value_dict["real_value"] = dict()
    # DO状态
    DO_status = dict()
    DO_status["DO"] = dict()
    DO_status["DO"]["开关状态"] = 0
    DO_status["DO"]["报警状态"] = 1
    DO_status["DO"]["故障状态"] = 1
    DO_status["DO"]["远方状态"] = 1
    DO_status["DO"]["维修状态"] = 1
    # 各个设备
    for i in range(n_tower_chilled_pump):
        tmp_name = "一级冷冻水泵_" + str(i)
        real_value_dict["real_value"][tmp_name] = DO_status
    # 返回结果
    return real_value_dict