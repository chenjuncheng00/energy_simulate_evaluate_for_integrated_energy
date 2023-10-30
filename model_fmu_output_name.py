
def main_model_output_name(load_mode=0):
    """
    整个模型的输出，名称
    Args:
        load_mode: [int]，0：user_load；1：simple_load

    Returns:

    """
    # 环境参数
    environment_output = environment_output_name(load_mode)[0]
    # 冷水机模型
    chiller_output = chiller_output_name()[0]
    # 空气源热泵模型
    air_source_heat_pump_output = air_source_heat_pump_output_name()[0]
    # 蓄冷水罐模型
    storage_output = cold_storage_output_name()[0]
    # 冷却塔直接供冷模型
    tower_chilled_output = tower_chilled_output_name()[0]
    # 用户侧模型
    load_output = load_output_name(load_mode)
    # 总输出
    model_output = environment_output + chiller_output + air_source_heat_pump_output + storage_output + \
                   tower_chilled_output + load_output
    # 返回结果
    return model_output


def environment_output_name(load_mode):
    """
    环境温湿度输出，名称
    Args:
        load_mode: [int]，0：user_load；1：simple_load

    Returns:

    """
    # 室外干球温度，单位：K
    Tdo = ['weather_data.TDryBul']
    # 室外湿球温度，单位：K
    Two = ['weather_data.TWetBul']
    # 室外相对湿度，单位：1
    Hro = ['weather_data.relHum']
    # 总输出
    if load_mode == 0:
        environment_output = Tdo + Two + Hro
    else:
        # simple_load没有天气数据
        environment_output = []
    # 返回结果
    return environment_output, Tdo, Two, Hro


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
    # 冷却塔风机频率，单位：Hz
    Fca = ['chiller_Fca_total', 'chiller_Fca_big', 'chiller_Fca_small']
    # 冷冻水温度，单位：℃
    Te = ['chiller_Ted', 'chiller_Ted_big', 'chiller_Ted_small',
          'chiller_Tei', 'chiller_Tei_big', 'chiller_Tei_small',
          'chiller_Teo', 'chiller_Teo_big', 'chiller_Teo_small']
    # 冷却水温度，单位：℃
    Tc = ['chiller_Tcd', 'chiller_Tcd_big', 'chiller_Tcd_small',
          'chiller_Tci', 'chiller_Tci_big', 'chiller_Tci_small',
          'chiller_Tco', 'chiller_Tco_big', 'chiller_Tco_small']
    # 冷却塔逼近度，单位：℃
    T_approach = ['chiller_T_approach_cooling_tower']
    # 水泵扬程，单位：m
    H_pump = ['chiller_H_chilled_pump', 'chiller_H_cooling_pump', 'chiller_H_cooling_tower']
    # COP
    COP = ['chiller_COP', 'chiller_COP_big', 'chiller_COP_small']
    # EER
    EER = ['chiller_EER']
    # 单台设备的电功率，单位：W
    chiller_P = ['chillers_model.chiller_big1.P', 'chillers_model.chiller_big2.P', 'chillers_model.chiller_big3.P',
                 'chillers_model.chiller_big4.P', 'chillers_model.chiller_small1.P', 'chillers_model.chiller_small2.P']
    chilled_pump_P = ['chillers_model.chilled_pump_big1.P', 'chillers_model.chilled_pump_big2.P',
                      'chillers_model.chilled_pump_big3.P', 'chillers_model.chilled_pump_big4.P',
                      'chillers_model.chilled_pump_small1.P', 'chillers_model.chilled_pump_small2.P']
    cooling_pump_P = ['chillers_model.cooling_pump_big1.P', 'chillers_model.cooling_pump_big2.P',
                      'chillers_model.cooling_pump_big3.P', 'chillers_model.cooling_pump_big4.P',
                      'chillers_model.cooling_pump_small1.P', 'chillers_model.cooling_pump_small2.P']
    cooling_tower_P = ['chillers_model.cooling_tower1.PFan', 'chillers_model.cooling_tower2.PFan',
                       'chillers_model.cooling_tower3.PFan', 'chillers_model.cooling_tower4.PFan',
                       'chillers_model.cooling_tower5.PFan', 'chillers_model.cooling_tower6.PFan']
    # 单台冷水机冷冻水流量，单位：kg/s
    chiller_Few = ['chillers_model.chiller_big1.m2_flow', 'chillers_model.chiller_big2.m2_flow',
                   'chillers_model.chiller_big3.m2_flow', 'chillers_model.chiller_big4.m2_flow',
                   'chillers_model.chiller_small1.m2_flow', 'chillers_model.chiller_small2.m2_flow']
    # 单台冷水机冷却水流量，单位：kg/s
    chiller_Fcw = ['chillers_model.chiller_big1.m1_flow', 'chillers_model.chiller_big2.m1_flow',
                   'chillers_model.chiller_big3.m1_flow', 'chillers_model.chiller_big4.m1_flow',
                   'chillers_model.chiller_small1.m1_flow', 'chillers_model.chiller_small2.m1_flow']
    # 总输出
    chiller_output = Q + Qct + P + Few + Fcw + Fca + Te + Tc + T_approach + H_pump + COP + EER + \
                     chiller_P + chilled_pump_P + cooling_pump_P + cooling_tower_P + chiller_Few + chiller_Fcw
    # 返回结果
    return chiller_output, Q, Qct, P, Few, Fcw, Fca, Te, Tc, T_approach, H_pump, COP, EER, chiller_P, \
           chilled_pump_P, cooling_pump_P, cooling_tower_P, chiller_Few, chiller_Fcw


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
    # 单台设备的电功率，单位：W
    ashp_P = ['air_source_heat_pumps_model.ashp1.P', 'air_source_heat_pumps_model.ashp2.P',
              'air_source_heat_pumps_model.ashp3.P', 'air_source_heat_pumps_model.ashp4.P']
    chilled_pump_P = ['air_source_heat_pumps_model.chilled_pump1.P', 'air_source_heat_pumps_model.chilled_pump2.P',
                      'air_source_heat_pumps_model.chilled_pump3.P', 'air_source_heat_pumps_model.chilled_pump4.P']
    # 单台空气源热泵冷冻水流量，单位：kg/s
    ashp_Few = ['air_source_heat_pumps_model.ashp1.m2_flow', 'air_source_heat_pumps_model.ashp2.m2_flow',
                'air_source_heat_pumps_model.ashp3.m2_flow', 'air_source_heat_pumps_model.ashp4.m2_flow']
    # 总输出
    air_source_heat_pump_output = Q + P + Few + Te + H_pump + COP + EER + ashp_P + chilled_pump_P + ashp_Few
    # 返回结果
    return air_source_heat_pump_output, Q, P, Few, Te, H_pump, COP, EER, ashp_P, chilled_pump_P, ashp_Few


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
    # 单台设备的电功率，单位：W
    storage_pump_P = ['cold_storage_model.storage_pump1.P', 'cold_storage_model.storage_pump2.P',
                      'cold_storage_model.storage_pump3.P', 'cold_storage_model.storage_pump4.P']
    # 总输出
    storage_output = Q + P + Few + Te + H_pump + storage_pump_P
    # 返回结果
    return storage_output, Q, P, Few, Te, H_pump, storage_pump_P


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
    # 单台设备的电功率，单位：W
    chilled_pump_P = ['tower_chilled_model.tower_chilled_pump1.P', 'tower_chilled_model.tower_chilled_pump2.P',
                      'tower_chilled_model.tower_chilled_pump3.P', 'tower_chilled_model.tower_chilled_pump4.P']
    # 总输出
    tower_chilled_output = P + Few + H_pump + chilled_pump_P
    # 返回结果
    return tower_chilled_output, P, Few, H_pump, chilled_pump_P


def load_output_name(load_mode):
    """

    Args:
        load_mode: [int]，0：user_load；1：simple_load

    Returns:

    """
    if load_mode == 0:
        load_output = user_load_output_name()[0]
    else:
        load_output = simple_load_output_name()[0]
    # 返回结果
    return load_output


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


def simple_load_output_name():
    """
    简单的负荷模型输出，名称
    Returns:

    """
    # 制冷功率，单位：kW
    Q = ['user_Q_total', 'user_Q_chiller', 'user_Q_ashp', 'user_Q_storage', 'user_Q_tower_chilled']
    # 冷冻水流量，单位：t/h
    Few = ['user_Few_total']
    # 冷冻水温度，单位：℃
    Te = ['user_Ted', 'user_Tei', 'user_Teo']
    # 总输出
    user_output = Q + Few + Te
    # 返回结果
    return user_output, Q, Few, Te