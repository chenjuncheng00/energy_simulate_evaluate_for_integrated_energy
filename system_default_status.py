
def air_source_heat_pump_default_status(n_air_source_heat_pump, n_ashp_chilled_pump):
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
    for i in range(n_ashp_chilled_pump):
        tmp_name = "一级冷冻水泵_" + str(i)
        real_value_dict["real_value"][tmp_name] = DO_status
    for i in range(n_air_source_heat_pump):
        tmp_name = "空气源热泵_" + str(i)
        real_value_dict["real_value"][tmp_name] = DO_status
    for i in range(n_air_source_heat_pump):
        tmp_name = "冷冻阀门_" + str(i)
        real_value_dict["real_value"][tmp_name] = DO_status
    # 返回结果
    return real_value_dict