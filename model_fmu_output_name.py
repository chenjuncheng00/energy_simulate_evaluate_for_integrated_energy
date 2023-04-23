
def main_model_output_name():
    """
    整个模型的输出，名称

    Returns:

    """
    # 环境参数
    environment_output = environment_output_name()[0]
    # 冷水机模型
    chiller_output = chiller_output_name()[0]
    # 空气源热泵模型
    air_source_heat_pump_output = air_source_heat_pump_output_name()[0]
    # 蓄冷水罐模型
    storage_output = cold_storage_output_name()[0]
    # 冷却塔直接供冷模型
    tower_chilled_output = tower_chilled_output_name()[0]
    # 用户侧模型
    user_output = user_load_output_name()[0]
    # 总输出
    model_output = environment_output + chiller_output + air_source_heat_pump_output + storage_output + \
                   tower_chilled_output + user_output
    # 返回结果
    return model_output


def chiller_output_name():
    """
    冷水机模型输出，名称

    Returns:

    """
    # 制冷功率，单位：kW
    Q = ['chiller_Q_total', 'chiller_Q_big', 'chiller_Q_small']
    # 冷却侧散热功率，单位：kW
    Qct = ['chiller_Qct_total', 'chiller_Qct_big', 'chiller_Qct_small']
    # 耗电功率，单位：kW
    P = ['chiller_P_total_main_equipment', 'chiller_P_big_main_equipment', 'chiller_P_small_main_equipment',
         'chiller_P_total_chilled_pump', 'chiller_P_big_chilled_pump', 'chiller_P_small_chilled_pump',
         'chiller_P_total_cooling_pump', 'chiller_P_big_cooling_pump', 'chiller_P_small_cooling_pump',
         'chiller_P_total_cooling_tower']
    # 冷冻水流量，单位：t/h
    Few = ['chiller_Few_total', 'chiller_Few_big', 'chiller_Few_small', 'chiller_Few_chilled_pump_small']
    # 冷却水流量，单位：t/h
    Fcw = ['chiller_Fcw_total', 'chiller_Fcw_big', 'chiller_Fcw_small', 'chiller_Fcw_cooling_pump_small']
    # 冷冻水温度，单位：℃
    Te = ['chiller_Ted_all', 'chiller_Ted_big', 'chiller_Ted_small',
          'chiller_Tei_all', 'chiller_Tei_big', 'chiller_Tei_small',
          'chiller_Teo_all', 'chiller_Teo_big', 'chiller_Teo_small']
    # 冷却水温度，单位：℃
    Tc = ['chiller_Tcd_all', 'chiller_Tcd_big', 'chiller_Tcd_small',
          'chiller_Tci_all', 'chiller_Tci_big', 'chiller_Tci_small',
          'chiller_Tco_all', 'chiller_Tco_big', 'chiller_Tco_small']
    # 冷却塔逼近度，单位：℃
    T_approach = ['chiller_T_approach_cooling_tower']
    # 水泵扬程，单位：m
    H_pump = ['chiller_H_chilled_pump', 'chiller_H_cooling_pump', 'chiller_H_cooling_tower']
    # COP
    COP = ['chiller_COP', 'chiller_COP_big', 'chiller_COP_small']
    # EER
    EER = ['chiller_EER']
    # 总输出
    chiller_output = Q + Qct + P + Few + Fcw + Te + Tc + T_approach + H_pump + COP + EER
    # 返回结果
    return chiller_output, Q, Qct, P, Few, Fcw, Te, Tc, T_approach, H_pump, COP, EER


def air_source_heat_pump_output_name():
    """
    空气源热泵模型输出，名称

    Returns:

    """
    # 制冷功率，单位：kW
    Q = ['ashp_Q_total']
    # 耗电功率，单位：kW
    P = ['ashp_P_total_main_equipment', 'ashp_P_total_chilled_pump']
    # 冷冻水流量，单位：t/h
    Few = ['ashp_Few_total']
    # 冷冻水温度，单位：℃
    Te = ['ashp_Ted', 'ashp_Tei', 'ashp_Teo']
    # 水泵扬程，单位：m
    H_pump = ['ashp_H_chilled_pump']
    # COP
    COP = ['ashp_COP']
    # EER
    EER = ['ashp_EER']
    # 总输出
    air_source_heat_pump_output = Q + P + Few + Te + H_pump + COP + EER
    # 返回结果
    return air_source_heat_pump_output, Q, P, Few, Te, H_pump, COP, EER


def cold_storage_output_name():
    """
    蓄冷水罐模型输出，名称

    Returns:

    """
    # 蓄冷功率，单位：kW
    Q = ['storage_Q_total_from_chiller']
    # 耗电功率，单位：kW
    P = ['storage_P_total_chilled_pump']
    # 冷冻水流量，单位：t/h
    Few = ['storage_Few_total_from_chiller', 'storage_Few_total_to_user']
    # 冷冻水温度，单位：℃
    Te = ['storage_Ted_from_chiller', 'storage_Ted_to_user', 'storage_Tei_from_chiller',
          'storage_Tei_to_user', 'storage_Teo_to_user']
    # 水泵扬程，单位：m
    H_pump = ['storage_H_chilled_pump']
    # 总输出
    storage_output = Q + P + Few + Te + H_pump
    # 返回结果
    return storage_output, Q, P, Few, Te, H_pump


def tower_chilled_output_name():
    """
    冷却塔直接供冷模型输出，名称

    Returns:

    """
    # 耗电功率，单位：kW
    P = ['tower_chilled_P_total_chilled_pump']
    # 冷冻水流量，单位：t/h
    Few = ['tower_chilled_Few_total']
    # 水泵扬程，单位：m
    H_pump = ['tower_chilled_H_chilled_pump']
    # 总输出
    tower_chilled_output = P + Few + H_pump
    # 返回结果
    return tower_chilled_output, P, Few, H_pump


def user_load_output_name():
    """
    用户末端负荷模型输出，名称

    Returns:

    """
    # 室内干球温度，单位：℃
    room_T = ['user_Tdi_room1', 'user_Tdi_room2', 'user_Tdi_room3', 'user_Tdi_room4']
    # 室内相对湿度，单位：1
    room_H = ['user_Hri_room1', 'user_Hri_room2', 'user_Hri_room3', 'user_Hri_room4']
    # 制冷功率，单位：kW
    Q = ['user_Q_total', 'user_Q_chiller', 'user_Q_ashp', 'user_Q_storage', 'user_Q_tower_chilled']
    # 耗电功率，单位：kW
    P = ['user_P_total_chilled_pump']
    # 冷冻水流量，单位：t/h
    Few = ['user_Few_total']
    # 水泵扬程，单位：m
    H_pump = ['user_H_chilled_pump']
    # 冷冻水温度，单位：℃
    Te = ['user_Ted', 'user_Tei', 'user_Teo']
    # 总输出
    user_output = room_T + room_H + Q + P + Few + Te + H_pump
    # 返回结果
    return user_output, room_T, room_H, Q, P, Few, Te, H_pump


def environment_output_name():
    """
    环境温湿度输出，名称

    Returns:

    """
    # 室外干球温度，单位：K
    Tdo = ['weather_data.TDryBul']
    # 室外湿球温度，单位：K
    Two = ['weather_data.TWetBul']
    # 室外相对湿度，单位：1
    Hro = ['weather_data.relHum']
    # 总输出
    environment_output = Tdo + Two + Hro
    # 返回结果
    return environment_output, Tdo, Two, Hro