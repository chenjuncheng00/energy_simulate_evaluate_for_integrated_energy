import time, traceback, numpy as np
from read_write_data import read_cfg_data, write_txt_data
from model_fmu_simulate import simulate_sample


def main_identify_equipment_characteristic(fmu_unzipdir, fmu_description, start_time, stop_time, output_interval,
                                           time_out, cfg_path_equipment, chiller_big_cop_result_txt_path,
                                           chiller_small_cop_result_txt_path, ashp_cop_result_txt_path,
                                           cooling_tower_approach_result_txt_path):
    """
    模型设备性能特性辨识

    Args:
        fmu_unzipdir: [string]，FMU模型解压后的路径
        fmu_description: [object]，获取FMU模型描述
        start_time: [float]，仿真开始时间，单位：秒
        stop_time: [float]，仿真结束时间，单位：秒
        output_interval: [float]，FMU模型输出采样时间，单位：秒
        time_out: [float]，仿真超时时间，单位：秒
        cfg_path_equipment: [string]，设备信息参数cfg文件路径
        chiller_big_cop_result_txt_path: [string]，大冷水机COP特性辨识结果，txt文件路径
        chiller_small_cop_result_txt_path: [string]，小冷水机COP特性辨识结果，txt文件路径
        ashp_cop_result_txt_path: [string]，空气源热泵COP特性辨识结果，txt文件路径
        cooling_tower_approach_result_txt_path: [string]，冷却塔逼近度特性辨识结果，txt文件路径

    Returns:

    """
    # 设备额定水流量
    chiller1_Few0 = read_cfg_data(cfg_path_equipment, "冷水机1", "chiller1_Few0", 0)
    chiller2_Few0 = read_cfg_data(cfg_path_equipment, "冷水机2", "chiller2_Few0", 0)
    chiller1_Fcw0 = read_cfg_data(cfg_path_equipment, "冷水机1", "chiller1_Fcw0", 0)
    chiller2_Fcw0 = read_cfg_data(cfg_path_equipment, "冷水机2", "chiller2_Fcw0", 0)
    chiller_cooling_tower_Fcw0 = read_cfg_data(cfg_path_equipment, "冷却塔_冷水机", "cooling_tower_Fcw0", 0)
    air_source_heat_pump_Few0 = read_cfg_data(cfg_path_equipment, "空气源热泵", "air_source_heat_pump_Few0", 0)
    air_source_heat_pump_Fca0 = 92.47 # kg/s
    # 设备额定制冷功率，单位：kW
    chiller1_Q0 = read_cfg_data(cfg_path_equipment, "冷水机1", "chiller1_Q0", 0)
    chiller2_Q0 = read_cfg_data(cfg_path_equipment, "冷水机2", "chiller2_Q0", 0)
    air_source_heat_pump_Q0 = read_cfg_data(cfg_path_equipment, "空气源热泵", "air_source_heat_pump_Q0", 0)

    # 冷冻水出水温度设定值辨识范围，单位转换为：K
    Teo_set_min = 5
    Teo_set_max = 15
    Teo_set_step = 2
    n_cal_Teo = int((Teo_set_max - Teo_set_min) / Teo_set_step)
    Teo_set_list = []
    for i in range(n_cal_Teo + 1):
        Teo_set_list.append(Teo_set_min + i * Teo_set_step + 273.15)
    # 冷却水回水温度辨识范围，单位转换为：K
    Tci_min = 20
    Tci_max = 40
    Tci_step = 4
    n_cal_Tci = int((Tci_max - Tci_min) / Tci_step)
    Tci_list = []
    for i in range(n_cal_Tci + 1):
        Tci_list.append(Tci_min + i * Tci_step + 273.15)
    # 湿球温度辨识范围，单位转换为：K
    Two_min = 10
    Two_max = 40
    Two_step = 3
    n_cal_Two = int((Two_max - Two_min) / Two_step)
    Two_list = []
    for i in range(n_cal_Two + 1):
        Two_list.append(Two_min + i * Two_step + 273.15)
    cooling_tower_Tin_list = Two_list

    # 流量比例上下限和步长
    Fw_min_ratio = 0.2
    Fw_max_ratio = 1.2
    Fw_step = 0.2
    n_Fw_cal = int((Fw_max_ratio - Fw_min_ratio) / Fw_step)
    # 流量辨识范围，单位转换为：kg/s
    chiller1_Few_list = []
    chiller2_Few_list = []
    chiller1_Fcw_list = []
    chiller2_Fcw_list = []
    ashp_Few_list = []
    ashp_Fca_list = []
    cooling_tower_Fcw_list = []
    for i in range(n_Fw_cal + 1):
        tmp_ratio = Fw_min_ratio + i * Fw_step
        chiller1_Few_list.append(chiller1_Few0 * tmp_ratio / 3.6)
        chiller2_Few_list.append(chiller2_Few0 * tmp_ratio / 3.6)
        chiller1_Fcw_list.append(chiller1_Fcw0 * tmp_ratio / 3.6)
        chiller2_Fcw_list.append(chiller2_Fcw0 * tmp_ratio / 3.6)
        ashp_Few_list.append(air_source_heat_pump_Few0 * tmp_ratio / 3.6)
        ashp_Fca_list.append(air_source_heat_pump_Fca0 * tmp_ratio)
        cooling_tower_Fcw_list.append(chiller_cooling_tower_Fcw0 * tmp_ratio / 3.6)

    # 制冷功率辨识范围，单位：kW
    Q_min_ratio = 0.2
    Q_max_ratio = 1
    Q_step = 0.2
    n_Q_cal = int((Q_max_ratio - Q_min_ratio) / Q_step)
    chiller1_Q_list = []
    chiller2_Q_list = []
    ashp_Q_list = []
    for i in range(n_Q_cal + 1):
        tmp_ratio = Q_min_ratio + i * Q_step
        chiller1_Q_list.append(chiller1_Q0 * tmp_ratio)
        chiller2_Q_list.append(chiller2_Q0 * tmp_ratio)
        ashp_Q_list.append(air_source_heat_pump_Q0 * tmp_ratio)

    # 冷却塔风机转速辨识范围
    f_tower_min = 0.2
    f_tower_max = 1
    f_tower_step = 0.2
    n_cal_f_tower = int((f_tower_max - f_tower_min) / f_tower_step)
    f_cooling_tower_list = []
    for i in range(n_cal_f_tower + 1):
        f_cooling_tower_list.append(f_tower_min + i * f_tower_step)

    # FMU模型输入名称和数据类型
    model_input_type = [('time', np.float_), ('Teo_set', np.float_), ('Tei', np.float_), ('chiller_Tci', np.float_),
                        ('turn_chiller_big', np.bool_), ('chiller_big_Few', np.float_), ('chiller_big_Fcw', np.float_),
                        ('turn_chiller_small', np.bool_), ('chiller_small_Few', np.float_), ('chiller_small_Fcw', np.float_),
                        ('turn_ashp', np.bool_), ('ashp_Tci', np.float_), ('ashp_Few', np.float_), ('ashp_Fca', np.float_),
                        ('Two', np.float_), ('f_tower', np.float_), ('tower_Tin', np.float_), ('tower_Fcw', np.float_)]
    model_output_name = ['P_chiller_big', 'Teo_chiller_big', 'Tco_chiller_big',
                         'P_chiller_small', 'Teo_chiller_small', 'Tco_chiller_small',
                         'P_ashp', 'Teo_ashp', 'Tco_ashp', 'tower_Tout', 'RH_air_in', 'RH_air_out']
    # 仿真开始时间
    time_data = [start_time]

    # 大冷水机，COP
    identify_chiller_big_cop(Teo_set_list, Tci_list, chiller1_Few_list, chiller1_Fcw_list, chiller1_Q_list, time_data,
                             fmu_unzipdir, fmu_description, start_time, stop_time, time_out, model_input_type,
                             model_output_name, output_interval, chiller_big_cop_result_txt_path)
    # 小冷水机，COP
    identify_chiller_small_cop(Teo_set_list, Tci_list, chiller2_Few_list, chiller2_Fcw_list, chiller2_Q_list, time_data,
                               fmu_unzipdir, fmu_description, start_time, stop_time, time_out, model_input_type,
                               model_output_name, output_interval, chiller_small_cop_result_txt_path)
    # 空气源热泵，COP
    identify_ashp_cop(Teo_set_list, Tci_list, ashp_Few_list, ashp_Fca_list, ashp_Q_list, time_data, fmu_unzipdir,
                      fmu_description, start_time, stop_time, time_out, model_input_type, model_output_name,
                      output_interval, ashp_cop_result_txt_path)
    # 冷却塔，逼近度
    identify_cooling_tower_approach(Two_list, cooling_tower_Fcw_list, f_cooling_tower_list, cooling_tower_Tin_list,
                                    time_data, fmu_unzipdir, fmu_description, start_time, stop_time, time_out,
                                    model_input_type, model_output_name, output_interval,
                                    cooling_tower_approach_result_txt_path)


def identify_chiller_big_cop(Teo_set_list, Tci_list, chiller1_Few_list, chiller1_Fcw_list, chiller1_Q_list, time_data,
                             fmu_unzipdir, fmu_description, start_time, stop_time, time_out,  model_input_type,
                             model_output_name, output_interval,  chiller_big_cop_result_txt_path):
    """
    大冷水机COP特性辨识

    Args:
        Teo_set_list: [list]，冷冻水出水温度设定值辨识列表
        Tci_list: [list]，冷却水回水温度辨识列表
        chiller1_Few_list: [list]，冷冻水流量辨识列表
        chiller1_Fcw_list: [list]，冷却水流量辨识列表
        chiller1_Q_list: [list]，制冷功率辨识列表
        time_data: [list]，模型输入数据，时间
        fmu_unzipdir: [string]，FMU模型解压后的路径
        fmu_description: [object]，获取FMU模型描述
        start_time: [float]，仿真开始时间，单位：秒
        stop_time: [float]，仿真结束时间，单位：秒
        time_out: [float]，仿真超时时间，单位：秒
        model_input_type: [list]，模型输入名称和数据类型
        model_output_name: [list]，模型输出名称
        output_interval: [float]，FMU模型输出采样时间，单位：秒
        chiller_big_cop_result_txt_path: [string]，仿真结果保存txt文件路径

    Returns:

    """
    # 大冷水机模型，COP特性辨识
    chiller_big_cop_result_list = []
    chiller_big_cop_result_list.append("大冷水机模型，COP特性辨识：")
    chiller_big_cop_result_list.append("冷冻水出水温度设定值" + "\t" + "冷冻水出水温度实际值" + "\t" +
                                       "冷冻水回水温度实际值" + "\t" + "冷却水回水温度实际值" + "\t" +
                                       "冷冻水流量实际值" + "\t" + "冷却水流量实际值" + "\t" +
                                       "制冷功率目标值" + "\t" + "制冷功率实际值" + "\t" + "冷冻水温差实际值" + "\t" +
                                       "冷却水温差实际值" + "\t" + "冷水机耗电功率" + "\t" + "冷水机COP")
    # input_data不变的默认值
    chiller_small_data = [False, 0, 0]
    ashp_data = [False, 20 + 273.15, 0, 0]
    tower_data = [25 + 273.15, 0, 20 + 273.15, 0]
    for i in range(len(Teo_set_list)):
        for j in range(len(Tci_list)):
            for k in range(len(chiller1_Few_list)):
                for l in range(len(chiller1_Fcw_list)):
                    for m in range(len(chiller1_Q_list)):
                        Teo_set = Teo_set_list[i] # K
                        Tci = Tci_list[j] # K
                        Few = chiller1_Few_list[k] # kg/s
                        Fcw = chiller1_Fcw_list[l] # kg/s
                        Q_target = chiller1_Q_list[m] # kW
                        Tei = Q_target / 4.16 / Few + Teo_set
                        tmp_Tco = 1.2 * Q_target / 4.16 / Fcw + Tci # 预估的Tco
                        if Tei - Teo_set > 15 or Tei - Teo_set < 1:
                            continue
                        if tmp_Tco - Tci > 15 or tmp_Tco - Tci < 1:
                            continue
                        model_input_data = time_data + [Teo_set, Tei, Tci] + [True, Few, Fcw] + \
                                           chiller_small_data + ashp_data + tower_data
                        print("正在进行 大冷水机模型 COP特性辨识：" + "冷冻水出水温度设定值：" + str(Teo_set - 273.15) +
                              "，冷却水回水温度实际值" + str(Tci - 273.15) + "，冷冻水流量" + str(np.round(Few * 3.6, 2)) +
                              "，冷却水流量" + str(np.round(Fcw * 3.6, 2)) + "，制冷功率目标值" + str(np.round(Q_target, 2)) +
                              "，冷冻水回水温度实际值" + str(np.round(Tei - 273.15, 2)))
                        # FMU仿真
                        try:
                            time1 = time.time()
                            result = simulate_sample(fmu_unzipdir, fmu_description, None, start_time, stop_time,
                                                     model_input_data, model_input_type, model_output_name,
                                                     output_interval, time_out, False, False)
                            # 获取仿真结果
                            P_chiller = result['P_chiller_big'][-1] # W
                            Teo_real = result['Teo_chiller_big'][-1] # K
                            Tco = result['Tco_chiller_big'][-1] # K
                            # 重新计算制冷功率，kW
                            Q_real = Few * (Tei - Teo_real) * 4.18
                            # 计算温差
                            Ted = Tei - Teo_real
                            Tcd = Tco - Tci
                            # 计算COP
                            if P_chiller > 0:
                                COP = Q_real / (P_chiller / 1000)
                            else:
                                COP = 0
                            # 仿真结果生成txt
                            if COP > 1 and COP < 30 and abs(Teo_real - Teo_set) < 0.5:
                                tmp_txt = str(Teo_set - 273.15) + "\t" + str(np.round(Teo_real - 273.15, 2)) + "\t" + \
                                          str(np.round(Tei - 273.15, 2)) + "\t" + str(Tci - 273.15) + "\t" + \
                                          str(np.round(Few * 3.6, 2)) + "\t" + str(np.round(Fcw * 3.6, 2)) + "\t" + \
                                          str(np.round(Q_target, 2)) + "\t" + str(np.round(Q_real, 2)) + "\t" + \
                                          str(np.round(Ted, 2)) + "\t" + str(np.round(Tcd, 2)) + "\t" + \
                                          str(np.round(P_chiller / 1000, 2)) + "\t" + str(np.round(COP, 2))
                                chiller_big_cop_result_list.append(tmp_txt)
                            else:
                                print("本次仿真的COP结果为：" + str(np.round(COP, 2)) +
                                      "；冷冻水出水温度目标值和实际值差值为：" + str(np.round(abs(Teo_real - Teo_set), 2)) +
                                      "；数据异常，不记录本次仿真结果！")
                            time2 = time.time()
                            time_cost = np.round(time2 - time1, 2)
                            print("本次仿真计算用时(秒)：" + str(time_cost) + "\n")
                        except:
                            print("FMU仿真失败：" + "冷冻水出水温度设定值：" + str(Teo_set - 273.15) +
                                  "，冷却水回水温度实际值" + str(Tci - 273.15) + "，冷冻水流量" + str(np.round(Few * 3.6, 2)) +
                                  "，冷却水流量" + str(np.round(Fcw * 3.6, 2)) + "，制冷功率目标值" + str(np.round(Q_target, 2)))
                            print(traceback.format_exc() + "\n")
                            pass
    # 结果写入txt
    write_txt_data(chiller_big_cop_result_txt_path, chiller_big_cop_result_list)


def identify_chiller_small_cop(Teo_set_list, Tci_list, chiller2_Few_list, chiller2_Fcw_list, chiller2_Q_list, time_data,
                               fmu_unzipdir, fmu_description, start_time, stop_time, time_out,  model_input_type,
                               model_output_name, output_interval,  chiller_small_cop_result_txt_path):
    """
    小冷水机COP特性辨识

    Args:
        Teo_set_list: [list]，冷冻水出水温度设定值辨识列表
        Tci_list: [list]，冷却水回水温度辨识列表
        chiller2_Few_list: [list]，冷冻水流量辨识列表
        chiller2_Fcw_list: [list]，冷却水流量辨识列表
        chiller2_Q_list: [list]，制冷功率辨识列表
        time_data: [list]，模型输入数据，时间
        fmu_unzipdir: [string]，FMU模型解压后的路径
        fmu_description: [object]，获取FMU模型描述
        start_time: [float]，仿真开始时间，单位：秒
        stop_time: [float]，仿真结束时间，单位：秒
        time_out: [float]，仿真超时时间，单位：秒
        model_input_type: [list]，模型输入名称和数据类型
        model_output_name: [list]，模型输出名称
        output_interval: [float]，FMU模型输出采样时间，单位：秒
        chiller_small_cop_result_txt_path: [string]，仿真结果保存txt文件路径

    Returns:

    """
    # 小冷水机模型，COP特性辨识
    chiller_small_cop_result_list = []
    chiller_small_cop_result_list.append("小冷水机模型，COP特性辨识：")
    chiller_small_cop_result_list.append("冷冻水出水温度设定值" + "\t" + "冷冻水出水温度实际值" + "\t" +
                                         "冷冻水回水温度实际值" + "\t" + "冷却水回水温度实际值" + "\t" +
                                         "冷冻水流量实际值" + "\t" + "冷却水流量实际值" + "\t" +
                                         "制冷功率目标值" + "\t" + "制冷功率实际值" + "\t" + "冷冻水温差实际值" + "\t" +
                                         "冷却水温差实际值" + "\t" + "冷水机耗电功率" + "\t" + "冷水机COP")
    # input_data不变的默认值
    chiller_big_data = [False, 0, 0]
    ashp_data = [False, 20 + 273.15, 0, 0]
    tower_data = [25 + 273.15, 0, 20 + 273.15, 0]
    for i in range(len(Teo_set_list)):
        for j in range(len(Tci_list)):
            for k in range(len(chiller2_Few_list)):
                for l in range(len(chiller2_Fcw_list)):
                    for m in range(len(chiller2_Q_list)):
                        Teo_set = Teo_set_list[i] # K
                        Tci = Tci_list[j] # K
                        Few = chiller2_Few_list[k] # kg/s
                        Fcw = chiller2_Fcw_list[l] # kg/s
                        Q_target = chiller2_Q_list[m] # kW
                        Tei = Q_target / 4.16 / Few + Teo_set
                        tmp_Tco = 1.2 * Q_target / 4.16 / Fcw + Tci  # 预估的Tco
                        if Tei - Teo_set > 15 or Tei - Teo_set < 1:
                            continue
                        if tmp_Tco - Tci > 15 or tmp_Tco - Tci < 1:
                            continue
                        model_input_data = time_data + [Teo_set, Tei, Tci] + chiller_big_data + \
                                           [True, Few, Fcw] + ashp_data + tower_data
                        print("正在进行 小冷水机模型 COP特性辨识：" + "冷冻水出水温度设定值：" + str(Teo_set - 273.15) +
                              "，冷却水回水温度实际值" + str(Tci - 273.15) + "，冷冻水流量" + str(np.round(Few * 3.6, 2)) +
                              "，冷却水流量" + str(np.round(Fcw * 3.6, 2)) + "，制冷功率目标值" + str(np.round(Q_target, 2)) +
                              "，冷冻水回水温度实际值" + str(np.round(Tei - 273.15, 2)))
                        # FMU仿真
                        try:
                            time1 = time.time()
                            result = simulate_sample(fmu_unzipdir, fmu_description, None, start_time, stop_time,
                                                     model_input_data, model_input_type, model_output_name,
                                                     output_interval, time_out, False, False)
                            # 获取仿真结果
                            P_chiller = result['P_chiller_small'][-1]  # W
                            Teo_real = result['Teo_chiller_small'][-1]  # K
                            Tco = result['Tco_chiller_small'][-1]  # K
                            # 重新计算制冷功率，kW
                            Q_real = Few * (Tei - Teo_real) * 4.18
                            # 计算温差
                            Ted = Tei - Teo_real
                            Tcd = Tco - Tci
                            # 计算COP
                            if P_chiller > 0:
                                COP = Q_real / (P_chiller / 1000)
                            else:
                                COP = 0
                            # 仿真结果生成txt
                            if COP > 1 and COP < 30 and abs(Teo_real - Teo_set) < 0.5:
                                tmp_txt = str(Teo_set - 273.15) + "\t" + str(np.round(Teo_real - 273.15, 2)) + "\t" + \
                                          str(np.round(Tei - 273.15, 2)) + "\t" + str(Tci - 273.15) + "\t" + \
                                          str(np.round(Few * 3.6, 2)) + "\t" + str(np.round(Fcw * 3.6, 2)) + "\t" + \
                                          str(np.round(Q_target, 2)) + "\t" + str(np.round(Q_real, 2)) + "\t" + \
                                          str(np.round(Ted, 2)) + "\t" + str(np.round(Tcd, 2)) + "\t" + \
                                          str(np.round(P_chiller / 1000, 2)) + "\t" + str(np.round(COP, 2))
                                chiller_small_cop_result_list.append(tmp_txt)
                            else:
                                print("本次仿真的COP结果为：" + str(np.round(COP, 2)) +
                                      "；冷冻水出水温度目标值和实际值差值为：" + str(np.round(abs(Teo_real - Teo_set), 2)) +
                                      "；数据异常，不记录本次仿真结果！")
                            time2 = time.time()
                            time_cost = np.round(time2 - time1, 2)
                            print("本次仿真计算用时(秒)：" + str(time_cost) + "\n")
                        except:
                            print("FMU仿真失败：" + "冷冻水出水温度设定值：" + str(Teo_set - 273.15) +
                                  "，冷却水回水温度实际值" + str(Tci - 273.15) + "，冷冻水流量" + str(np.round(Few * 3.6, 2)) +
                                  "，冷却水流量" + str(np.round(Fcw * 3.6, 2)) + "，制冷功率目标值" + str(np.round(Q_target, 2)))
                            print(traceback.format_exc() + "\n")
                            pass
    # 结果写入txt
    write_txt_data(chiller_small_cop_result_txt_path, chiller_small_cop_result_list)


def identify_ashp_cop(Teo_set_list, Tci_list, ashp_Few_list, ashp_Fca_list, ashp_Q_list, time_data, fmu_unzipdir,
                      fmu_description, start_time, stop_time, time_out,  model_input_type, model_output_name,
                      output_interval,  ashp_cop_result_txt_path):
    """
    空气源热泵COP特性辨识

    Args:
        Teo_set_list: [list]，冷冻水出水温度设定值辨识列表
        Tci_list: [list]，冷却水回水温度辨识列表
        ashp_Few_list: [list]，冷冻水流量辨识列表
        ashp_Fca_list: [list]，空气流量辨识列表
        ashp_Q_list: [list]，制冷功率辨识列表
        time_data: [list]，模型输入数据，时间
        fmu_unzipdir: [string]，FMU模型解压后的路径
        fmu_description: [object]，获取FMU模型描述
        start_time: [float]，仿真开始时间，单位：秒
        stop_time: [float]，仿真结束时间，单位：秒
        time_out: [float]，仿真超时时间，单位：秒
        model_input_type: [list]，模型输入名称和数据类型
        model_output_name: [list]，模型输出名称
        output_interval: [float]，FMU模型输出采样时间，单位：秒
        ashp_cop_result_txt_path: [string]，仿真结果保存txt文件路径

    Returns:

    """
    # 空气源热泵模型，COP特性辨识
    ashp_cop_result_list = []
    ashp_cop_result_list.append("空气源热泵模型，COP特性辨识：")
    ashp_cop_result_list.append("冷冻水出水温度设定值" + "\t" + "冷冻水出水温度实际值" + "\t" +
                                "冷冻水回水温度实际值" + "\t" + "空气入口温度实际值" + "\t" +
                                "冷冻水流量实际值" + "\t" + "空气流量实际值" + "\t" + "制冷功率目标值" + "\t" +
                                "制冷功率实际值" + "\t" + "冷冻水温差实际值" + "\t" + "空气温差实际值" + "\t" +
                                "空气源热泵耗电功率" + "\t" + "空气源热泵COP")
    # input_data不变的默认值
    chiller_big_data = [20 + 273.15, False, 0, 0]
    chiller_small_data = [False, 0, 0]
    tower_data = [25 + 273.15, 0, 20 + 273.15, 0]
    for i in range(len(Teo_set_list)):
        for j in range(len(Tci_list)):
            for k in range(len(ashp_Few_list)):
                for l in range(len(ashp_Fca_list)):
                    for m in range(len(ashp_Q_list)):
                        Teo_set = Teo_set_list[i] # K
                        Tci = Tci_list[j] # K
                        Few = ashp_Few_list[k] # kg/s
                        Fca = ashp_Fca_list[l] # kg/s
                        Q_target = ashp_Q_list[m] # kW
                        Tei = Q_target / 4.16 / Few + Teo_set
                        tmp_Tco = 1.2 * Q_target / 4.16 / Fca + Tci  # 预估的Tco
                        if Tei - Teo_set > 15 or Tei - Teo_set < 1:
                            continue
                        if tmp_Tco - Tci > 15 or tmp_Tco - Tci < 1:
                            continue
                        model_input_data = time_data + [Teo_set, Tei] + chiller_big_data + chiller_small_data + \
                                           [True, Tci, Few, Fca] + tower_data
                        print("正在进行 空气源热泵模型 COP特性辨识：" + "冷冻水出水温度设定值：" + str(Teo_set - 273.15) +
                              "，冷却水回水温度实际值" + str(Tci - 273.15) + "，冷冻水流量" + str(np.round(Few * 3.6, 2)) +
                              "，空气流量" + str(np.round(Fca * 3.6, 2)) + "，制冷功率目标值" + str(np.round(Q_target, 2)) +
                              "，冷冻水回水温度实际值" + str(np.round(Tei - 273.15, 2)))
                        # FMU仿真
                        try:
                            time1 = time.time()
                            result = simulate_sample(fmu_unzipdir, fmu_description, None, start_time, stop_time,
                                                     model_input_data, model_input_type, model_output_name,
                                                     output_interval, time_out, False, False)
                            # 获取仿真结果
                            P_ashp = result['P_ashp'][-1]  # W
                            Teo_real = result['Teo_ashp'][-1]  # K
                            Tco = result['Tco_ashp'][-1]  # K
                            # 重新计算制冷功率，kW
                            Q_real = Few * (Tei - Teo_real) * 4.18
                            # 计算温差
                            Ted = Tei - Teo_real
                            Tcd = Tco - Tci
                            # 计算COP
                            if P_ashp > 0:
                                COP = Q_real / (P_ashp / 1000)
                            else:
                                COP = 0
                            # 仿真结果生成txt
                            if COP > 1 and COP < 30 and abs(Teo_real - Teo_set) < 0.5:
                                tmp_txt = str(Teo_set - 273.15) + "\t" + str(np.round(Teo_real - 273.15, 2)) + "\t" + \
                                          str(np.round(Tei - 273.15, 2)) + "\t" + str(Tci - 273.15) + "\t" + \
                                          str(np.round(Few * 3.6, 2)) + "\t" + str(np.round(Fca * 3.6, 2)) + "\t" + \
                                          str(np.round(Q_target, 2)) + "\t" + str(np.round(Q_real, 2)) + "\t" + \
                                          str(np.round(Ted, 2)) + "\t" + str(np.round(Tcd, 2)) + "\t" + \
                                          str(np.round(P_ashp / 1000, 2)) + "\t" + str(np.round(COP, 2))
                                ashp_cop_result_list.append(tmp_txt)
                            else:
                                print("本次仿真的COP结果为：" + str(np.round(COP, 2)) +
                                      "；冷冻水出水温度目标值和实际值差值为：" + str(np.round(abs(Teo_real - Teo_set), 2)) +
                                      "；数据异常，不记录本次仿真结果！")
                            time2 = time.time()
                            time_cost = np.round(time2 - time1, 2)
                            print("本次仿真计算用时(秒)：" + str(time_cost) + "\n")
                        except:
                            print("FMU仿真失败：" + "冷冻水出水温度设定值：" + str(Teo_set - 273.15) +
                                  "，空气入口温度实际值" + str(Tci - 273.15) + "，冷冻水流量" + str(np.round(Few * 3.6, 2)) +
                                  "，空气流量" + str(np.round(Fca * 3.6, 2)) + "，制冷功率目标值" + str(np.round(Q_target, 2)))
                            print(traceback.format_exc() + "\n")
                            pass
    # 结果写入txt
    write_txt_data(ashp_cop_result_txt_path, ashp_cop_result_list)


def identify_cooling_tower_approach(Two_list, cooling_tower_Fcw_list, f_cooling_tower_list, cooling_tower_Tin_list,
                                    time_data, fmu_unzipdir, fmu_description, start_time, stop_time, time_out,
                                    model_input_type, model_output_name, output_interval,
                                    cooling_tower_approach_result_txt_path):
    """
    冷却塔逼近度辨识

    Args:
        Two_list: [list]，室外环境湿球温度辨识列表
        cooling_tower_Fcw_list: [list]，冷却塔冷却水流量辨识列表
        f_cooling_tower_list: [list]，冷却塔风机转速比辨识列表
        cooling_tower_Tin_list: [list]，冷却塔入口水温度辨识列表
        time_data: [list]，模型输入数据，时间
        fmu_unzipdir: [string]，FMU模型解压后的路径
        fmu_description: [object]，获取FMU模型描述
        start_time: [float]，仿真开始时间，单位：秒
        stop_time: [float]，仿真结束时间，单位：秒
        time_out: [float]，仿真超时时间，单位：秒
        model_input_type: [list]，模型输入名称和数据类型
        model_output_name: [list]，模型输出名称
        output_interval: [float]，FMU模型输出采样时间，单位：秒
        cooling_tower_approach_result_txt_path: [string]，仿真结果保存txt文件路径

    Returns:

    """
    # 空气源热泵模型，COP特性辨识
    cooling_tower_approach_result_list = []
    cooling_tower_approach_result_list.append("冷却塔模型，出水温度逼近度特性辨识：")
    cooling_tower_approach_result_list.append("室外湿球温度实际值" + "\t" + "冷却水流量实际值" + "\t" +
                                              "冷却塔风机转速比实际值" + "\t" + "冷却塔入口水温度实际值" + "\t" +
                                              "冷却塔出口水温度实际值" + "\t" + "冷却塔温差实际值" + "\t" + "冷却塔逼近度实际值")
    # input_data不变的默认值
    chiller_T_data = [7 + 273.15, 20 + 273.15, 20 + 273.15]
    chiller_big_data = [False, 0, 0]
    chiller_small_data = [False, 0, 0]
    ashp_data = [False, 20 + 273.15, 0, 0]
    for i in range(len(Two_list)):
        for j in range(len(cooling_tower_Fcw_list)):
            for k in range(len(f_cooling_tower_list)):
                for l in range(len(cooling_tower_Tin_list)):
                    Two = Two_list[i]
                    Fcw = cooling_tower_Fcw_list[j]
                    f = f_cooling_tower_list[k]
                    Tin = cooling_tower_Tin_list[l]
                    if Tin - Two <= 1:
                        continue
                    model_input_data = time_data + chiller_T_data + chiller_big_data + chiller_small_data + \
                                       ashp_data + [Two, f, Tin, Fcw]
                    print("正在进行 冷却塔模型 出水温度逼近度特性辨识：" + "室外湿球温度实际值：" + str(Two - 273.15) +
                          "，冷却水流量实际值" + str(np.round(Fcw * 3.6, 2)) + "，冷却塔风机转速比实际值" +
                          str(np.round(f, 2)) + "，冷却塔入口温度实际值" + str(Tin - 273.15))
                    # FMU仿真
                    try:
                        time1 = time.time()
                        result = simulate_sample(fmu_unzipdir, fmu_description, None, start_time, stop_time,
                                                 model_input_data, model_input_type, model_output_name,
                                                 output_interval, time_out, False, False)
                        # 获取仿真结果
                        tower_Tout = result['tower_Tout'][-1]
                        Tcd = Tin - tower_Tout
                        approach = tower_Tout - Two
                        # 仿真结果生成txt
                        if Tcd > 0.1 and approach > 0.1:
                            tmp_txt = str(Two - 273.15) + "\t" + str(np.round(Fcw * 3.6, 2)) + "\t" + \
                                      str(np.round(f, 2)) + "\t" + str(np.round(Tin - 273.15, 2)) + "\t" + \
                                      str(np.round(tower_Tout - 273.15, 2)) + "\t" + \
                                      str(np.round(Tcd, 2)) + "\t" + str(np.round(approach, 2))
                            cooling_tower_approach_result_list.append(tmp_txt)
                        else:
                            print("本次仿真的逼近度结果为：" + str(np.round(approach, 2)) +
                                  "；冷却水进出口温差为：" + str(np.round(abs(Tcd), 2)) +
                                  "；数据异常，不记录本次仿真结果！")
                        time2 = time.time()
                        time_cost = np.round(time2 - time1, 2)
                        print("本次仿真计算用时(秒)：" + str(time_cost) + "\n")
                    except:
                        print("FMU仿真失败：" + "室外湿球温度实际值：" + str(Two - 273.15) +
                              "，冷却水流量实际值" + str(np.round(Fcw * 3.6, 2)) + "，冷却塔风机转速比实际值" +
                              str(np.round(f, 2)) + "，冷却塔入口温度实际值" + str(Tin - 273.15))
                        print(traceback.format_exc() + "\n")
                        pass
    # 结果写入txt
    write_txt_data(cooling_tower_approach_result_txt_path, cooling_tower_approach_result_list)