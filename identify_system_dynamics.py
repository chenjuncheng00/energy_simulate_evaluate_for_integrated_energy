import traceback
import pickle
import matplotlib.pyplot as plt
from fmpy import *
from algorithm_win import (algorithm_common_station, write_txt_data, write_log_data, clear_all_txt_data,
                           main_simulate_station_fmu, main_optimization_common_station, main_optimization_water_pump)
from air_conditioner_dynamic import estimate_transfer_function
from run_initialize import run_initialize
from model_fmu_output_name import main_model_output_name
from model_fmu_input_name import main_model_input_name
from model_fmu_input_type import (main_model_input_type, chiller_input_type, cold_storage_input_type,
                                  air_source_heat_pump_input_type, load_input_type)
from model_fmu_input_data_default import main_input_data_default

def main_identify_system_dynamics(path_matlab, fmu_unzipdir, fmu_description, start_time, stop_time, output_interval,
                                  Ts, time_out, tolerance, np_max, fitpercent_target_list, EER_mode, Q_list, txt_path,
                                  cfg_path_equipment, cfg_path_public, identify_mode):
    """

    Args:
        path_matlab: [string]，matlab文件所在的路径
        fmu_unzipdir: [string]，FMU模型解压后的路径
        fmu_description: [object]，获取FMU模型描述
        start_time: [float]，仿真开始时间，单位：秒
        stop_time: [float]，仿真结束时间，单位：秒
        output_interval: [float]，FMU模型输出采样时间，单位：秒
        Ts: [float]，采样时间
        time_out: [float]，仿真超时时间，单位：秒
        tolerance: [float]，FMU模型求解相对误差
        np_max: [int]，传递函数极点最大值
        fitpercent_target_list: [list]，传递函数辨识得分目标，列表
        EER_mode: [int]，EER数据获取模型，0：直接读取FMU数据；1：保持Q不变，自行计算
        Q_list: [list]，模型辨识指定的制冷功率，列表，单位：kW
        txt_path: [string]，相对路径
        cfg_path_equipment:[string]，设备信息参数cfg文件路径
        cfg_path_public:[string]，公用参数cfg文件路径
        identify_mode: [int]，0:仅冷水机；1:冷水机+空气源热泵

    Returns:

    """
    # FMU相关文件路径
    file_fmu_address = txt_path + "/process_data/fmu_address.txt"
    # FMU模型仿真时间：仿真开始的时间(start_time)
    file_fmu_time = txt_path + "/process_data/fmu_time.txt"
    # FMU模型状态：依次为：fmu_initialize, fmu_terminate, stop_time, output_interval, time_out
    file_fmu_state = txt_path + "/process_data/fmu_state.txt"
    # FMU模型输出名称
    file_fmu_input_output_name = txt_path + "/process_data/fmu_input_output_name.pkl"
    # 仿真结果
    file_fmu_result_all = "./model_file/simulate_log/fmu_result_all.log"
    file_fmu_result_last = "./model_file/simulate_log/fmu_result_last.log"
    # 设备的pkl文件路径
    file_pkl_chiller = "./model_file/file_equipment/chiller.pkl"
    file_pkl_ashp = "./model_file/file_equipment/ashp.pkl"
    # file_pkl_stroage = "./model_file/file_equipment/storage.pkl"
    file_pkl_system = "./model_file/file_equipment/system.pkl"
    # 用来拟合传递函数的数据储存路径：EER
    path_Few_EER_tfdata = "./model_file/file_identify/result_system_dynamics/tf_Few_EER.txt"  # 冷冻水流量
    path_Fcw_EER_tfdata = "./model_file/file_identify/result_system_dynamics/tf_Fcw_EER.txt"  # 冷却水流量
    path_Fca_EER_tfdata = "./model_file/file_identify/result_system_dynamics/tf_Fca_EER.txt"  # 冷却塔风量
    path_Teo_EER_tfdata = "./model_file/file_identify/result_system_dynamics/tf_Teo_EER.txt"  # 冷冻水出水温度
    # 用来拟合传递函数的数据储存路径：Tei
    path_Few_Tei_tfdata = "./model_file/file_identify/result_system_dynamics/tf_Few_Tei.txt"  # 冷冻水流量
    path_Fcw_Tei_tfdata = "./model_file/file_identify/result_system_dynamics/tf_Fcw_Tei.txt"  # 冷却水流量
    path_Fca_Tei_tfdata = "./model_file/file_identify/result_system_dynamics/tf_Fca_Tei.txt"  # 冷却塔风量
    path_Teo_Tei_tfdata = "./model_file/file_identify/result_system_dynamics/tf_Teo_Tei.txt"  # 冷冻水出水温度
    # 储存最终结果文本的文件路径
    path_result_EER = "./model_file/file_identify/result_system_dynamics/result_transfer_function_EER.txt"
    path_result_Tei = "./model_file/file_identify/result_system_dynamics/result_transfer_function_Tei.txt"
    # 传递函数数据的.txt文件文件所在的文件夹路径
    path_tf = "./model_file/file_identify/result_system_dynamics"
    # 清空txt文件
    root_path1 = "./model_file/file_identify/result_system_dynamics"
    clear_all_txt_data(root_path1)

    # 冷水机系统动态特性辨识
    if identify_mode == 0:
        identify_chiller_dynamics(fmu_unzipdir, fmu_description, file_fmu_address, file_fmu_time, file_fmu_state,
                                  file_fmu_input_output_name, file_fmu_result_all, file_fmu_result_last,
                                  file_pkl_chiller, file_pkl_system, start_time, stop_time, output_interval, Ts,
                                  time_out, tolerance, path_result_EER, path_result_Tei, path_tf, path_matlab,
                                  path_Few_EER_tfdata, path_Fcw_EER_tfdata, path_Fca_EER_tfdata, path_Teo_EER_tfdata,
                                  path_Few_Tei_tfdata, path_Fcw_Tei_tfdata, path_Fca_Tei_tfdata, path_Teo_Tei_tfdata,
                                  np_max, fitpercent_target_list, Q_list, EER_mode, txt_path, cfg_path_equipment,
                                  cfg_path_public)
    # 冷水机+空气源热泵
    elif identify_mode == 1:
        identify_chiller_ashp_dynamics(fmu_unzipdir, fmu_description, file_fmu_address, file_fmu_time, file_fmu_state,
                                       file_fmu_input_output_name, file_fmu_result_all, file_fmu_result_last,
                                       file_pkl_chiller, file_pkl_ashp, file_pkl_system, start_time, stop_time,
                                       output_interval, Ts, time_out, tolerance, path_result_EER, path_result_Tei,
                                       path_tf, path_matlab, path_Few_EER_tfdata, path_Fcw_EER_tfdata, path_Fca_EER_tfdata,
                                       path_Teo_EER_tfdata, path_Few_Tei_tfdata, path_Fcw_Tei_tfdata, path_Fca_Tei_tfdata,
                                       path_Teo_Tei_tfdata, np_max, fitpercent_target_list, Q_list, EER_mode, txt_path,
                                       cfg_path_equipment, cfg_path_public)


def identify_chiller_dynamics(fmu_unzipdir, fmu_description, file_fmu_address, file_fmu_time, file_fmu_state,
                              file_fmu_input_output_name, file_fmu_result_all, file_fmu_result_last, file_pkl_chiller,
                              file_pkl_system, start_time, stop_time, output_interval, Ts, time_out, tolerance,
                              path_result_EER, path_result_Tei, path_tf, path_matlab, path_Few_EER_tfdata,
                              path_Fcw_EER_tfdata, path_Fca_EER_tfdata, path_Teo_EER_tfdata, path_Few_Tei_tfdata,
                              path_Fcw_Tei_tfdata, path_Fca_Tei_tfdata, path_Teo_Tei_tfdata, np_max,
                              fitpercent_target_list, Q_list, EER_mode, txt_path, cfg_path_equipment, cfg_path_public):
    """
    仅冷水机系统动态特性辨识
    Args:
        fmu_unzipdir: [string]，FMU模型解压后的路径
        fmu_description: [object]，获取FMU模型描述
        file_fmu_address: [string]，储存FMU模型对象内存地址文件路径
        file_fmu_time: [string]，储存FMU模型仿真时间(start_time)的文件路径
        file_fmu_state: [string]，储存FMU模型状态的文件路径
        file_fmu_input_output_name: [string]，储存FMU模型输入输出名称的文件路径
        file_fmu_result_all: [string]，储存FMU模型所有仿真结果的文件路径
        file_fmu_result_last: [string]，储存FMU模型每次仿真最后时刻结果的文件路径
        file_pkl_chiller: [string]，冷水机系统信息储存路径
        file_pkl_system: [string]，公用系统信息储存路径
        start_time: [float]，仿真开始时间，单位：秒
        stop_time: [float]，仿真结束时间，单位：秒
        output_interval: [float]，FMU模型输出采样时间，单位：秒
        Ts: [float]，采样时间
        time_out: [float]，仿真超时时间，单位：秒
        tolerance: [float]，FMU模型求解相对误差
        path_result_EER: [string]，储存最终结果文本的文件路径
        path_result_Tei: [string]，储存最终结果文本的文件路径
        path_tf: [string]，需要读取的.txt文件文件所在的文件夹路径
        path_matlab: [string]，matlab文件所在的路径
        path_Few_EER_tfdata: [string]，冷冻水流量阶跃响应传递函数建模数据
        path_Fcw_EER_tfdata: [string]，冷却水流量阶跃响应传递函数建模数据
        path_Fca_EER_tfdata: [string]，冷却塔风量阶跃响应传递函数建模数据
        path_Teo_EER_tfdata: [string]，冷冻水出水温度阶跃响应传递函数建模数据
        path_Few_Tei_tfdata: [string]，冷冻水流量阶跃响应传递函数建模数据
        path_Fcw_Tei_tfdata: [string]，冷却水流量阶跃响应传递函数建模数据
        path_Fca_Tei_tfdata: [string]，冷却塔风量阶跃响应传递函数建模数据
        path_Teo_Tei_tfdata: [string]，冷冻水出水温度阶跃响应传递函数建模数据
        np_max: [int]，传递函数极点最大值
        fitpercent_target_list: [list]，传递函数辨识得分目标，列表
        Q_list: [list]，模型辨识指定的制冷功率，列表，单位：kW
        EER_mode: [int]，EER数据获取模型，0：直接读取FMU数据；1：保持Q不变，自行计算
        txt_path: [string]，相对路径
        cfg_path_equipment:[string]，设备信息参数cfg文件路径
        cfg_path_public:[string]，公用参数cfg文件路径

    Returns:

    """
    # Q_total储存文件
    file_Q_value_chiller = txt_path + "/real_value/energy_station/chiller/Q_value/chilled_main_pipe.txt"
    # 需要被辨识的对象列表：Fcw、Few、Fca、Teo、Tci等
    object_list = ["Teo", "Few", "Fcw", "Fca"]
    n_object_list = [1, 1, 1, 1]
    # 模型输出模式：EER/Tei
    Y_mode_list = ["EER", "Tei"]
    # 设备类型名称，相对路径，设备名称类型一定要是列表
    chiller_system_type = "chiller"
    chiller_system_type_path = [chiller_system_type, txt_path]
    # FMU模型输出名称，包括所有输入输出名称
    load_mode = 1  # 0：user_load；1：simple_load
    fmu_output_name = main_model_output_name(load_mode)
    fmu_input_name = main_model_input_name(load_mode)
    fmu_input_output_name = fmu_output_name + fmu_input_name
    # 读取冷水机设备信息
    with open(file_pkl_chiller, "rb") as f_obj:
        chiller_dict = pickle.load(f_obj)
    H_chiller_chilled_pump = chiller_dict["H_chiller_chilled_pump"]
    H_chiller_cooling_pump = chiller_dict["H_chiller_cooling_pump"]
    chiller_list = chiller_dict["chiller_list"]
    chiller_chilled_pump_list = chiller_dict["chiller_chilled_pump_list"]
    chiller_cooling_pump_list = chiller_dict["chiller_cooling_pump_list"]
    chiller_cooling_tower_list = chiller_dict["chiller_cooling_tower_list"]
    n_chiller_list = chiller_dict["n_chiller_list"]
    n_chiller_chilled_pump_list = chiller_dict["n_chiller_chilled_pump_list"]
    n_chiller_cooling_pump_list = chiller_dict["n_chiller_cooling_pump_list"]
    n_chiller_cooling_tower_list = chiller_dict["n_chiller_cooling_tower_list"]
    chiller1 = chiller_dict["chiller1"]
    chiller2 = chiller_dict["chiller2"]
    chiller_chilled_pump1 = chiller_dict["chiller_chilled_pump1"]
    chiller_chilled_pump2 = chiller_dict["chiller_chilled_pump2"]
    chiller_cooling_pump1 = chiller_dict["chiller_cooling_pump1"]
    chiller_cooling_pump2 = chiller_dict["chiller_cooling_pump2"]
    chiller_cooling_tower = chiller_dict["chiller_cooling_tower"]
    n0_chiller1 = chiller_dict["n_chiller1"]
    n0_chiller2 = chiller_dict["n_chiller2"]
    n0_chiller_chilled_pump1 = chiller_dict["n_chiller_chilled_pump1"]
    n0_chiller_chilled_pump2 = chiller_dict["n_chiller_chilled_pump2"]
    n0_chiller_cooling_pump1 = chiller_dict["n_chiller_cooling_pump1"]
    n0_chiller_cooling_pump2 = chiller_dict["n_chiller_cooling_pump2"]
    n0_chiller_cooling_tower = chiller_dict["n_chiller_cooling_tower"]
    n_chiller_user_valve = chiller_dict["n_chiller_user_valve"]
    # 读取公共系统信息
    with open(file_pkl_system, "rb") as f_obj:
        system_dict = pickle.load(f_obj)
    n_calculate_hour = system_dict["n_calculate_hour"]

    # 仿真各个阶段的时间，单位：秒
    simulate_time0 = 2 * 3600  # 初始化FMU
    simulate_time1 = 24 * 3600  # 系统稳定
    simulate_time2 = 12 * 3600  # 阶跃响应实验
    simulate_time3 = 2 * 3600  # 终止FMU
    # 最后要保存的
    n_data_save1 = 4 * 3600 / Ts
    n_data_save2 = simulate_time2 / Ts
    # plot的图编号
    index_figure = 1
    # 遍历所有制冷功率
    for i in range(len(Q_list)):
        # 获取制冷功率，单位：kW
        Q_input = Q_list[i]
        try:
            # 遍历所有需要辨识的项目类型
            for j in range(len(object_list)):
                tf_obj = object_list[j]
                # 第1步:初始化FMU模型
                print("制冷功率(kW)：" + str(round(Q_input, 2)) + "，辨识输入：" + tf_obj + "，正在初始化FMU模型!")
                # 重置所有内容
                run_initialize(txt_path)
                # 生成FMU输出名称文件
                with open(file_fmu_input_output_name, "wb") as f:
                    pickle.dump(fmu_input_output_name, f)  # type: ignore
                # 仿真结果
                txt_str = "start_time" + "\t" + "pause_time"
                for k in range(len(fmu_input_output_name)):
                    txt_str += "\t" + fmu_input_output_name[k]
                write_log_data(file_fmu_result_all, [txt_str], "data")
                write_log_data(file_fmu_result_last, [txt_str], "data")
                # 模型初始化和实例化
                fmu_instance = instantiate_fmu(unzipdir=fmu_unzipdir, model_description=fmu_description)
                # 获取内存地址
                unzipdir_address = id(fmu_unzipdir)
                description_address = id(fmu_description)
                instance_address = id(fmu_instance)
                fmu_address_list = [unzipdir_address, description_address, instance_address]
                write_txt_data(file_fmu_address, fmu_address_list)
                # FMU模型状态：依次为：fmu_initialize, fmu_terminate, stop_time, output_interval, time_out
                fmu_state_list = [1, 0, stop_time, output_interval, time_out, tolerance]
                write_txt_data(file_fmu_state, fmu_state_list)
                # 写入start_time
                write_txt_data(file_fmu_time, [start_time])
                # 模型输入名称和类型
                input_type_list = main_model_input_type(load_mode)
                # 模型输入数据
                input_data_list = [start_time] + main_input_data_default(load_mode)
                # FMU仿真
                main_simulate_station_fmu(input_data_list, input_type_list, simulate_time0, txt_path, add_input=False)
                # 第2步：更新初始化设置
                # 修改FMU状态
                fmu_state_list = [0, 0, stop_time, output_interval, time_out, tolerance]
                write_txt_data(file_fmu_state, fmu_state_list)
                # 第3步：优化一次冷水机计算，不进行控制，用于获取阀门开启比例
                print("制冷功率(kW)：" + str(round(Q_input, 2)) + "，辨识输入：" + tf_obj +
                      "，正在优化冷水机系统，但是不进行控制命令下发，用于获取阀门开启比例！")
                write_txt_data(file_Q_value_chiller, [Q_input])
                ans_chiller = main_optimization_common_station(H_chiller_chilled_pump, 0, H_chiller_cooling_pump,
                                                               chiller_list, chiller_chilled_pump_list, [],
                                                               chiller_cooling_pump_list, chiller_cooling_tower_list,
                                                               n_chiller_list, n_chiller_chilled_pump_list, [],
                                                               n_chiller_cooling_pump_list, n_chiller_cooling_tower_list,
                                                               chiller_system_type_path, cfg_path_public, cfg_path_equipment)
                chilled_valve_open = ans_chiller[0]
                cooling_valve_open = ans_chiller[1]
                tower_valve_open = ans_chiller[2]
                # 第4步：优化冷水机系统并进行控制命令下发
                print("制冷功率(kW)：" + str(round(Q_input, 2)) + "，辨识输入：" + tf_obj +
                      "，正在优化冷水机系统并进行控制命令下发!")
                write_txt_data(file_Q_value_chiller, [Q_input])
                algorithm_common_station(H_chiller_chilled_pump, 0, H_chiller_cooling_pump, [chiller1, chiller2],
                                         [chiller_chilled_pump1, chiller_chilled_pump2], [],
                                         [chiller_cooling_pump1, chiller_cooling_pump2], [chiller_cooling_tower],
                                         [n0_chiller1, n0_chiller2], [n0_chiller_chilled_pump1, n0_chiller_chilled_pump2],
                                         [], [n0_chiller_cooling_pump1, n0_chiller_cooling_pump2],
                                         [n0_chiller_cooling_tower], chiller_system_type_path, n_calculate_hour,
                                         cfg_path_equipment, cfg_path_public)
                # 第5步：系统仿真24小时，确保系统稳定，并获取数据
                print("制冷功率(kW)：" + str(round(Q_input, 2)) + "，辨识输入：" + tf_obj + "，正在持续仿真，确保系统稳定!")
                # 修改采样时间
                fmu_state_list = [0, 0, stop_time, Ts, time_out, tolerance]
                write_txt_data(file_fmu_state, fmu_state_list)
                # 模型输入名称和类型
                input_type_list = load_input_type(load_mode)
                # 模型输入数据
                input_data_list = [Q_input * 1000]
                result = main_simulate_station_fmu(input_data_list, input_type_list, simulate_time1, txt_path)
                # 获取系统稳定后的数据，用于系统辨识初始值
                chiller_f_cooling_tower_list = [list(result["chiller_f_cooling_tower1"]),
                                                list(result["chiller_f_cooling_tower2"]),
                                                list(result["chiller_f_cooling_tower3"]),
                                                list(result["chiller_f_cooling_tower4"]),
                                                list(result["chiller_f_cooling_tower5"]),
                                                list(result["chiller_f_cooling_tower6"])]
                chiller_Teo0 = list(result["chiller_Teo_set"])
                chiller_Few0 = list(result["chiller_Few_total"])
                chiller_Fcw0 = list(result["chiller_Fcw_total"])
                chiller_Tei0 = list(result["chiller_Tei"])
                chiller_Fca0 = calculate_sum_tower_f_list(chiller_f_cooling_tower_list)
                chiller_P0 = list(result["chiller_P_total_main_equipment"])
                chiller_chilled_pump_P0 = list(result["chiller_P_total_chilled_pump"])
                chiller_cooling_pump_P0 = list(result["chiller_P_total_cooling_pump"])
                chiller_cooling_tower_P0 = list(result["chiller_P_total_cooling_tower"])
                if EER_mode == 0:
                    chiller_EER0 = list(result["chiller_EER"])
                elif EER_mode == 1:
                    chiller_EER0 = []
                    for k in range(len(chiller_P0)):
                        P_tmp = chiller_P0[k] + chiller_chilled_pump_P0[k] + chiller_cooling_pump_P0[k] + \
                                chiller_cooling_tower_P0[k]
                        EER_tmp = Q_input / P_tmp
                        chiller_EER0.append(EER_tmp)
                else:
                    chiller_EER0 = None
                # 第6步：生成系统阶跃响应实验的输入数据
                print("制冷功率(kW)：" + str(round(Q_input, 2)) + "，辨识输入：" + tf_obj +
                      "，正在生成系统阶跃响应实验的输入数据！")
                # 确定step_value
                if tf_obj == "Teo":
                    step_value = 2
                    input_type_list = chiller_input_type()[2]
                    input_data_list = [chiller_Teo0[-1] + step_value]
                elif tf_obj == "Few":
                    Few_total = 1.2 * chiller_Few0[-1]
                    ans_Fw_step = calculate_Fw_step_value(chiller_system_type, tf_obj, Few_total,
                                                          chiller_chilled_pump_list, n_chiller_chilled_pump_list,
                                                          chilled_valve_open, cooling_valve_open, tower_valve_open, 0)
                    input_data_list = ans_Fw_step[0]
                    input_type_list = ans_Fw_step[1]
                elif tf_obj == "Fcw":
                    Fcw_total = 1.2 * chiller_Fcw0[-1]
                    ans_Fw_step = calculate_Fw_step_value(chiller_system_type, tf_obj, Fcw_total,
                                                          chiller_cooling_pump_list, n_chiller_cooling_pump_list,
                                                          chilled_valve_open, cooling_valve_open, tower_valve_open, 0)
                    input_data_list = ans_Fw_step[0]
                    input_type_list = ans_Fw_step[1]
                elif tf_obj == "Fca":
                    input_data_list, input_type_list = calculate_Fca_step_value(chiller_f_cooling_tower_list)
                else:
                    input_data_list = None
                    input_type_list = None
                # 第7步：系统阶跃响应实验
                print("制冷功率(kW)：" + str(round(Q_input, 2)) + "，辨识输入：" + tf_obj + "，正在进行系统阶跃响应实验！")
                result = main_simulate_station_fmu(input_data_list, input_type_list, simulate_time2, txt_path)
                chiller_f_cooling_tower_list = [list(result["chiller_f_cooling_tower1"])[1:],
                                                list(result["chiller_f_cooling_tower2"])[1:],
                                                list(result["chiller_f_cooling_tower3"])[1:],
                                                list(result["chiller_f_cooling_tower4"])[1:],
                                                list(result["chiller_f_cooling_tower5"])[1:],
                                                list(result["chiller_f_cooling_tower6"])[1:]]
                chiller_Teo1 = list(result["chiller_Teo_set"])[1:]
                chiller_Few1 = list(result["chiller_Few_total"])[1:]
                chiller_Fcw1 = list(result["chiller_Fcw_total"])[1:]
                chiller_Fca1 = calculate_sum_tower_f_list(chiller_f_cooling_tower_list)
                chiller_Tei1 = list(result["chiller_Tei"])[1:]
                chiller_P1 = list(result["chiller_P_total_main_equipment"])[1:]
                chiller_chilled_pump_P1 = list(result["chiller_P_total_chilled_pump"])[1:]
                chiller_cooling_pump_P1 = list(result["chiller_P_total_cooling_pump"])[1:]
                chiller_cooling_tower_P1 = list(result["chiller_P_total_cooling_tower"])[1:]
                if EER_mode == 0:
                    chiller_EER1 = list(result["chiller_EER"])[1:]
                elif EER_mode == 1:
                    chiller_EER1 = []
                    for k in range(len(chiller_P1)):
                        P_tmp = chiller_P1[k] + chiller_chilled_pump_P1[k] + chiller_cooling_pump_P1[k] + \
                                chiller_cooling_tower_P1[k]
                        EER_tmp = Q_input / P_tmp
                        chiller_EER1.append(EER_tmp)
                else:
                    chiller_EER1 = None
                # 读取仿真的数据，并截取需要的部分
                chiller_Teo_list = chiller_Teo0 + chiller_Teo1
                chiller_Few_list = chiller_Few0 + chiller_Few1
                chiller_Fcw_list = chiller_Fcw0 + chiller_Fcw1
                chiller_Fca_list = chiller_Fca0 + chiller_Fca1
                chiller_EER_list = chiller_EER0 + chiller_EER1
                chiller_Tei_list = chiller_Tei0 + chiller_Tei1
                # 第8步：确定传递函数辨识的输入X和输出Y
                # 只保留最后6个小时的数据，并换算到0初始值条件下
                # 模型输入X
                if tf_obj == "Teo":
                    start_index0 = int(len(chiller_Teo0) - n_data_save1)
                    X0_list = chiller_Teo0[start_index0:]
                    X0 = sum(X0_list) / len(X0_list)
                    start_index1 = int(len(chiller_Teo_list) - (n_data_save1 + n_data_save2))
                    X_list = chiller_Teo_list[start_index1:]
                    for k in range(len(X_list)):
                        X_list[k] -= X0
                elif tf_obj == "Few":
                    start_index0 = int(len(chiller_Few0) - n_data_save1)
                    X0_list = chiller_Few0[start_index0:]
                    X0 = sum(X0_list) / len(X0_list)
                    start_index1 = int(len(chiller_Few_list) - (n_data_save1 + n_data_save2))
                    X_list = chiller_Few_list[start_index1:]
                    for k in range(len(X_list)):
                        X_list[k] -= X0
                elif tf_obj == "Fcw":
                    start_index0 = int(len(chiller_Fcw0) - n_data_save1)
                    X0_list = chiller_Fcw0[start_index0:]
                    X0 = sum(X0_list) / len(X0_list)
                    start_index1 = int(len(chiller_Fcw_list) - (n_data_save1 + n_data_save2))
                    X_list = chiller_Fcw_list[start_index1:]
                    for k in range(len(X_list)):
                        X_list[k] -= X0
                elif tf_obj == "Fca":
                    start_index0 = int(len(chiller_Fca0) - n_data_save1)
                    X0_list = chiller_Fca0[start_index0:]
                    X0 = sum(X0_list) / len(X0_list)
                    start_index1 = int(len(chiller_Fca_list) - (n_data_save1 + n_data_save2))
                    X_list = chiller_Fca_list[start_index1:]
                    for k in range(len(X_list)):
                        X_list[k] -= X0
                else:
                    X_list = None
                # 绘图
                plt.figure(index_figure)
                plt.title("Q_input(kW):" + str(Q_input) + "; " + tf_obj)
                plt.plot(X_list)
                index_figure += 1
                # 模型输出Y
                for k in range(len(Y_mode_list)):
                    Y_mode = Y_mode_list[k]
                    if Y_mode == "EER":
                        start_index0 = int(len(chiller_EER0) - n_data_save1)
                        Y0_list = chiller_EER0[start_index0:]
                        Y0 = sum(Y0_list) / len(Y0_list)
                        start_index1 = int(len(chiller_EER_list) - (n_data_save1 + n_data_save2))
                        Y_list = chiller_EER_list[start_index1:]
                        for l in range(len(Y_list)):
                            Y_list[l] -= Y0
                        # 绘图
                        plt.figure(index_figure)
                        plt.title("Q_input(kW):" + str(Q_input) + "; " + "EER: " + tf_obj)
                        plt.plot(Y_list)
                        index_figure += 1
                    elif Y_mode == "Tei":
                        start_index0 = int(len(chiller_Tei0) - n_data_save1)
                        Y0_list = chiller_Tei0[start_index0:]
                        Y0 = sum(Y0_list) / len(Y0_list)
                        start_index1 = int(len(chiller_Tei_list) - (n_data_save1 + n_data_save2))
                        Y_list = chiller_Tei_list[start_index1:]
                        # 如果是Fcw或者Fca，则Y_list全部改成0
                        for l in range(len(Y_list)):
                            if tf_obj == "Fcw" or tf_obj == "Fca":
                                Y_list[l] = 0
                            else:
                                Y_list[l] -= Y0
                        # 绘图
                        plt.figure(index_figure)
                        plt.title("Q_input(kW):" + str(Q_input) + "; " + "Tei: " + tf_obj)
                        plt.plot(Y_list)
                        index_figure += 1
                    else:
                        Y_list = None
                    # 拼接数据，写入txt
                    tf_data_txt_list = []
                    for l in range(len(X_list)):
                        tmp = str(X_list[l]) + "\t" + str(Y_list[l])
                        tf_data_txt_list.append(tmp)
                    if tf_obj == "Teo" and Y_mode == "EER":
                        write_txt_data(path_Teo_EER_tfdata, tf_data_txt_list)
                    elif tf_obj == "Few" and Y_mode == "EER":
                        write_txt_data(path_Few_EER_tfdata, tf_data_txt_list)
                    elif tf_obj == "Fcw" and Y_mode == "EER":
                        write_txt_data(path_Fcw_EER_tfdata, tf_data_txt_list)
                    elif tf_obj == "Fca" and Y_mode == "EER":
                        write_txt_data(path_Fca_EER_tfdata, tf_data_txt_list)
                    elif tf_obj == "Teo" and Y_mode == "Tei":
                        write_txt_data(path_Teo_Tei_tfdata, tf_data_txt_list)
                    elif tf_obj == "Few" and Y_mode == "Tei":
                        write_txt_data(path_Few_Tei_tfdata, tf_data_txt_list)
                    elif tf_obj == "Fcw" and Y_mode == "Tei":
                        write_txt_data(path_Fcw_Tei_tfdata, tf_data_txt_list)
                    elif tf_obj == "Fca" and Y_mode == "Tei":
                        write_txt_data(path_Fca_Tei_tfdata, tf_data_txt_list)
                # 绘图
                plt.show()
                # 第9步：终止FMU模型
                print("制冷功率(kW)：" + str(round(Q_input, 2)) + "，辨识输入：" + tf_obj + "，正在终止FMU模型！")
                # 修改FMU状态
                fmu_state_list = [0, 1, stop_time, output_interval, time_out, tolerance]
                write_txt_data(file_fmu_state, fmu_state_list)
                # 最后仿真一次
                main_simulate_station_fmu([], [], simulate_time3, txt_path)

            # 第10步：辨识传递函数
            print("制冷功率(kW)：" + str(round(Q_input, 2)) + "，所有的传递函数辨识数据生成完成！")
            for j in range(len(Y_mode_list)):
                Y_mode = Y_mode_list[j]
                print("制冷功率(kW)：" + str(round(Q_input, 2)) + "，辨识输出：" + Y_mode + "，正在进行传递函数辨识!")
                info_txt = "Q=" + str(round(Q_input, 2)) + "kW"
                # 传递函数系统辨识
                ans_tf = estimate_transfer_function(path_tf, path_matlab, Ts, object_list, n_object_list, np_max,
                                                    fitpercent_target_list, i + 1, Y_mode, True)
                tf_txt = "# " + Y_mode + "模型: " + info_txt + "\n"
                tf_txt += ans_tf
                tf_txt_list = [tf_txt]
                # 将结果写入txt文件
                if Y_mode == "EER":
                    path_result = path_result_EER
                elif Y_mode == "Tei":
                    path_result = path_result_Tei
                else:
                    path_result = None
                # 记录结果
                write_txt_data(path_result, tf_txt_list, write_model=1)
                # 结束循环
                print_txt = "传递函数辨识完成, 辨识的模型类型为：" + Y_mode + "；工况点序号为：" + \
                            str(i + 1) + ", " + info_txt + "\n"
                print(print_txt)
        except:
            print("动态特性辨识失败！制冷功率(kW)：" + str(round(Q_input, 2)) + "，跳过计算....")
            print(traceback.format_exc())
            pass


def identify_chiller_ashp_dynamics(fmu_unzipdir, fmu_description, file_fmu_address, file_fmu_time, file_fmu_state,
                                   file_fmu_input_output_name, file_fmu_result_all, file_fmu_result_last,
                                   file_pkl_chiller, file_pkl_ashp, file_pkl_system, start_time, stop_time,
                                   output_interval, Ts, time_out, tolerance, path_result_EER, path_result_Tei, path_tf,
                                   path_matlab, path_Few_EER_tfdata, path_Fcw_EER_tfdata, path_Fca_EER_tfdata,
                                   path_Teo_EER_tfdata, path_Few_Tei_tfdata, path_Fcw_Tei_tfdata, path_Fca_Tei_tfdata,
                                   path_Teo_Tei_tfdata, np_max, fitpercent_target_list, Q_list, EER_mode, txt_path,
                                   cfg_path_equipment, cfg_path_public):
    """
    冷水机+空气源热泵耦合系统动态特性辨识
    Args:
        fmu_unzipdir: [string]，FMU模型解压后的路径
        fmu_description: [object]，获取FMU模型描述
        file_fmu_address: [string]，储存FMU模型对象内存地址文件路径
        file_fmu_time: [string]，储存FMU模型仿真时间(start_time)的文件路径
        file_fmu_state: [string]，储存FMU模型状态的文件路径
        file_fmu_input_output_name: [string]，储存FMU模型输入输出名称的文件路径
        file_fmu_result_all: [string]，储存FMU模型所有仿真结果的文件路径
        file_fmu_result_last: [string]，储存FMU模型每次仿真最后时刻结果的文件路径
        file_pkl_chiller: [string]，冷水机系统信息储存路径
        file_pkl_ashp: [string]，空气源热泵系统信息储存路径
        file_pkl_system: [string]，公用系统信息储存路径
        start_time: [float]，仿真开始时间，单位：秒
        stop_time: [float]，仿真结束时间，单位：秒
        output_interval: [float]，FMU模型输出采样时间，单位：秒
        Ts: [float]，采样时间
        time_out: [float]，仿真超时时间，单位：秒
        tolerance: [float]，FMU模型求解相对误差
        path_result_EER: [string]，储存最终结果文本的文件路径
        path_result_Tei: [string]，储存最终结果文本的文件路径
        path_tf: [string]，需要读取的.txt文件文件所在的文件夹路径
        path_matlab: [string]，matlab文件所在的路径
        path_Few_EER_tfdata: [string]，冷冻水流量阶跃响应传递函数建模数据
        path_Fcw_EER_tfdata: [string]，冷却水流量阶跃响应传递函数建模数据
        path_Fca_EER_tfdata: [string]，冷却塔风量阶跃响应传递函数建模数据
        path_Teo_EER_tfdata: [string]，冷冻水出水温度阶跃响应传递函数建模数据
        path_Few_Tei_tfdata: [string]，冷冻水流量阶跃响应传递函数建模数据
        path_Fcw_Tei_tfdata: [string]，冷却水流量阶跃响应传递函数建模数据
        path_Fca_Tei_tfdata: [string]，冷却塔风量阶跃响应传递函数建模数据
        path_Teo_Tei_tfdata: [string]，冷冻水出水温度阶跃响应传递函数建模数据
        np_max: [int]，传递函数极点最大值
        fitpercent_target_list: [list]，传递函数辨识得分目标，列表
        Q_list: [list]，模型辨识指定的制冷功率，列表，单位：kW
        EER_mode: [int]，EER数据获取模型，0：直接读取FMU数据；1：保持Q不变，自行计算
        txt_path: [string]，相对路径
        cfg_path_equipment:[string]，设备信息参数cfg文件路径
        cfg_path_public:[string]，公用参数cfg文件路径

    Returns:

    """
    # Q_total储存文件
    file_Q_value_chiller = txt_path + "/real_value/energy_station/chiller/Q_value/chilled_main_pipe.txt"
    file_Q_value_ashp = txt_path + "/real_value/energy_station/air_source_heat_pump/Q_value/chilled_main_pipe.txt"
    # 需要被辨识的对象列表：Fcw、Few、Fca、Teo、Tci等
    object_list = ["Teo", "chiller_Few", "Fcw", "Fca", "ashp_Few"]
    estf_object_list = ["Teo", "Few", "Fcw", "Fca"]
    n_object_list = [1, 2, 1, 1]
    # 模型输出模式：EER/Tei
    Y_mode_list = ["EER", "Tei"]
    # 设备类型
    chiller_system_type = "chiller"
    ashp_system_type = "air_source_heat_pump"
    # 设备类型和相对路径
    chiller_system_type_path = [chiller_system_type, txt_path]
    ashp_system_type_path = [ashp_system_type, txt_path]
    # FMU模型输出名称，包括所有输入输出名称
    load_mode = 1  # 0：user_load；1：simple_load
    fmu_output_name = main_model_output_name(load_mode)
    fmu_input_name = main_model_input_name(load_mode)
    fmu_input_output_name = fmu_output_name + fmu_input_name
    # 读取冷水机设备信息
    with open(file_pkl_chiller, "rb") as f_obj:
        chiller_dict = pickle.load(f_obj)
    H_chiller_chilled_pump = chiller_dict["H_chiller_chilled_pump"]
    H_chiller_cooling_pump = chiller_dict["H_chiller_cooling_pump"]
    chiller_list = chiller_dict["chiller_list"]
    chiller_chilled_pump_list = chiller_dict["chiller_chilled_pump_list"]
    chiller_cooling_pump_list = chiller_dict["chiller_cooling_pump_list"]
    chiller_cooling_tower_list = chiller_dict["chiller_cooling_tower_list"]
    n_chiller_list = chiller_dict["n_chiller_list"]
    n_chiller_chilled_pump_list = chiller_dict["n_chiller_chilled_pump_list"]
    n_chiller_cooling_pump_list = chiller_dict["n_chiller_cooling_pump_list"]
    n_chiller_cooling_tower_list = chiller_dict["n_chiller_cooling_tower_list"]
    chiller1 = chiller_dict["chiller1"]
    chiller2 = chiller_dict["chiller2"]
    chiller_chilled_pump1 = chiller_dict["chiller_chilled_pump1"]
    chiller_chilled_pump2 = chiller_dict["chiller_chilled_pump2"]
    chiller_cooling_pump1 = chiller_dict["chiller_cooling_pump1"]
    chiller_cooling_pump2 = chiller_dict["chiller_cooling_pump2"]
    chiller_cooling_tower = chiller_dict["chiller_cooling_tower"]
    n0_chiller1 = chiller_dict["n_chiller1"]
    n0_chiller2 = chiller_dict["n_chiller2"]
    n0_chiller_chilled_pump1 = chiller_dict["n_chiller_chilled_pump1"]
    n0_chiller_chilled_pump2 = chiller_dict["n_chiller_chilled_pump2"]
    n0_chiller_cooling_pump1 = chiller_dict["n_chiller_cooling_pump1"]
    n0_chiller_cooling_pump2 = chiller_dict["n_chiller_cooling_pump2"]
    n0_chiller_cooling_tower = chiller_dict["n_chiller_cooling_tower"]
    n_chiller_user_valve = chiller_dict["n_chiller_user_valve"]
    # 读取空气源热泵设备信息
    with open(file_pkl_ashp, "rb") as f_obj:
        ashp_dict = pickle.load(f_obj)
    # H_ashp_chilled_pump = ashp_dict["H_ashp_chilled_pump"]
    n0_air_source_heat_pump = ashp_dict["n_air_source_heat_pump"]
    n0_ashp_chilled_pump = ashp_dict["n_ashp_chilled_pump"]
    air_source_heat_pump = ashp_dict["air_source_heat_pump"]
    ashp_chilled_pump = ashp_dict["ashp_chilled_pump"]
    # 读取公共系统信息
    with open(file_pkl_system, "rb") as f_obj:
        system_dict = pickle.load(f_obj)
    n_calculate_hour = system_dict["n_calculate_hour"]
    # 各系统制冷功率最大值
    chiller_Q0_max = 14000
    ashp_Q0_max = 3600
    # Q0_total_in = chiller_Q0_max
    # Q0_total_out = chiller_Q0_max + ashp_Q0_max
    # 仿真各个阶段的时间，单位：秒
    simulate_time0 = 2 * 3600  # 初始化FMU
    simulate_time1 = 24 * 3600  # 系统稳定
    simulate_time2 = 12 * 3600  # 阶跃响应实验
    simulate_time3 = 2 * 3600  # 终止FMU
    # 最后要保存的
    n_data_save1 = 4 * 3600 / Ts
    n_data_save2 = simulate_time2 / Ts
    # plot的图编号
    index_figure = 1
    # 遍历所有制冷功率
    for i in range(len(Q_list)):
        # 获取制冷功率，单位：kW
        Q_input = Q_list[i]
        # Few有两种，需要拼接
        x_Few_list = []
        y_Few_EER_list = []
        y_Few_Tei_list = []
        try:
            # 遍历所有需要辨识的项目类型
            for j in range(len(object_list)):
                tf_obj = object_list[j]
                # 第1步:初始化FMU模型
                print("制冷功率(kW)：" + str(round(Q_input, 2)) + "，辨识输入：" + tf_obj + "，正在初始化FMU模型!")
                # 重置所有内容
                run_initialize(txt_path)
                # 生成FMU输出名称文件
                with open(file_fmu_input_output_name, "wb") as f:
                    pickle.dump(fmu_input_output_name, f)  # type: ignore
                # 仿真结果
                txt_str = "start_time" + "\t" + "pause_time"
                for k in range(len(fmu_input_output_name)):
                    txt_str += "\t" + fmu_input_output_name[k]
                write_log_data(file_fmu_result_all, [txt_str], "data")
                write_log_data(file_fmu_result_last, [txt_str], "data")
                # 模型初始化和实例化
                fmu_instance = instantiate_fmu(unzipdir=fmu_unzipdir, model_description=fmu_description)
                # 获取内存地址
                unzipdir_address = id(fmu_unzipdir)
                description_address = id(fmu_description)
                instance_address = id(fmu_instance)
                fmu_address_list = [unzipdir_address, description_address, instance_address]
                write_txt_data(file_fmu_address, fmu_address_list)
                # FMU模型状态：依次为：fmu_initialize, fmu_terminate, stop_time, output_interval, time_out
                fmu_state_list = [1, 0, stop_time, output_interval, time_out, tolerance]
                write_txt_data(file_fmu_state, fmu_state_list)
                # 写入start_time
                write_txt_data(file_fmu_time, [start_time])
                # 模型输入名称和类型
                input_type_list = main_model_input_type(load_mode)
                # 模型输入数据
                input_data_list = [start_time] + main_input_data_default(load_mode)
                # FMU仿真
                main_simulate_station_fmu(input_data_list, input_type_list, simulate_time0, txt_path, add_input=False)
                # 第2步：更新初始化设置
                # 修改FMU状态
                fmu_state_list = [0, 0, stop_time, output_interval, time_out, tolerance]
                write_txt_data(file_fmu_state, fmu_state_list)
                # 第3步：稳态搜索，冷水机和空气源热泵初始运行策略
                # 第3-1步：用供冷功率优化一次冷水机计算，不进行控制，用于获取阀门开启比例和冷冻水泵扬程...
                print("制冷功率(kW)：" + str(round(Q_input, 2)) + "，辨识输入：" + tf_obj +
                      "，正在优化冷水机系统，但是不进行控制命令下发，用于获取阀门开启比例和冷冻水泵扬程！")
                chiller_Q_total = min(Q_input, chiller_Q0_max)
                write_txt_data(file_Q_value_chiller, [chiller_Q_total])
                ans_chiller = main_optimization_common_station(H_chiller_chilled_pump, 0, H_chiller_cooling_pump,
                                                               chiller_list, chiller_chilled_pump_list, [],
                                                               chiller_cooling_pump_list, chiller_cooling_tower_list,
                                                               n_chiller_list, n_chiller_chilled_pump_list, [],
                                                               n_chiller_cooling_pump_list, n_chiller_cooling_tower_list,
                                                               chiller_system_type_path, cfg_path_public, cfg_path_equipment)
                chiller_chilled_valve_open = ans_chiller[0]
                chiller_cooling_valve_open = ans_chiller[1]
                chiller_tower_valve_open = ans_chiller[2]
                chiller_chilled_pump_H = ans_chiller[4]
                # 第3-2步：优化一次空气源热泵，不进行控制，用于获取阀门开启比例...
                print("制冷功率(kW)：" + str(round(Q_input, 2)) + "，辨识输入：" + tf_obj +
                      "，正在优化空气源热泵系统，但是不进行控制命令下发，用于获取阀门开启比例！")
                ashp_Q_total = min(Q_input - chiller_Q_total, ashp_Q0_max)
                H_ashp_chilled_pump = 0.67 * chiller_chilled_pump_H
                write_txt_data(file_Q_value_ashp, [ashp_Q_total])
                ans_ashp = main_optimization_common_station(H_ashp_chilled_pump, 0, 0, [air_source_heat_pump],
                                                            [ashp_chilled_pump], [], [], [], [n0_air_source_heat_pump],
                                                            [n0_ashp_chilled_pump], [], [], [], ashp_system_type_path,
                                                            cfg_path_public, cfg_path_equipment)
                ashp_chilled_valve_open = ans_ashp[0]
                # 第3-3步：冷水机优化和控制...
                print("制冷功率(kW)：" + str(round(Q_input, 2)) + "，辨识输入：" + tf_obj +
                      "，正在优化冷水机系统并进行控制命令下发!")
                write_txt_data(file_Q_value_chiller, [chiller_Q_total])
                algorithm_common_station(H_chiller_chilled_pump, 0, H_chiller_cooling_pump, [chiller1, chiller2],
                                         [chiller_chilled_pump1, chiller_chilled_pump2], [],
                                         [chiller_cooling_pump1, chiller_cooling_pump2], [chiller_cooling_tower],
                                         [n0_chiller1, n0_chiller2], [n0_chiller_chilled_pump1, n0_chiller_chilled_pump2],
                                         [], [n0_chiller_cooling_pump1, n0_chiller_cooling_pump2],
                                         [n0_chiller_cooling_tower], chiller_system_type_path, n_calculate_hour,
                                         cfg_path_equipment, cfg_path_public)
                # 第3-4步：空气源热泵优化和控制...
                print("制冷功率(kW)：" + str(round(Q_input, 2)) + "，辨识输入：" + tf_obj +
                      "，正在优化空气源热泵系统并进行控制命令下发!")
                write_txt_data(file_Q_value_ashp, [ashp_Q_total])
                algorithm_common_station(H_ashp_chilled_pump, 0, 0, [air_source_heat_pump], [ashp_chilled_pump],
                                         [], [], [], [n0_air_source_heat_pump], [n0_ashp_chilled_pump], [],
                                         [], [], ashp_system_type_path, n_calculate_hour, cfg_path_equipment,
                                         cfg_path_public)
                # 第4步：系统仿真24小时，确保系统稳定，并获取数据
                print("制冷功率(kW)：" + str(round(Q_input, 2)) + "，辨识输入：" + tf_obj + "，正在持续仿真，确保系统稳定!")
                # 修改采样时间
                fmu_state_list = [0, 0, stop_time, Ts, time_out, tolerance]
                write_txt_data(file_fmu_state, fmu_state_list)
                # 模型输入名称和类型
                input_type_list = load_input_type(load_mode)
                # 模型输入数据
                input_data_list = [Q_input * 1000]
                result = main_simulate_station_fmu(input_data_list, input_type_list, simulate_time1, txt_path)
                # 获取系统稳定后的数据，用于系统辨识初始值
                chiller_f_cooling_tower_list = [list(result["chiller_f_cooling_tower1"]),
                                                list(result["chiller_f_cooling_tower2"]),
                                                list(result["chiller_f_cooling_tower3"]),
                                                list(result["chiller_f_cooling_tower4"]),
                                                list(result["chiller_f_cooling_tower5"]),
                                                list(result["chiller_f_cooling_tower6"])]
                # user_Q0 = list(result["user_Q_total"])
                user_Tei0 = list(result["user_Tei"])
                # user_Few0 = list(result["user_Few_total"])
                Teo0_set = list(result["chiller_Teo_set"])  # ashp_Teo_set数值相同
                chiller_Q0 = list(result["chiller_Q_total"])
                chiller_Few0 = list(result["chiller_Few_total"])
                chiller_Fcw0 = list(result["chiller_Fcw_total"])
                chiller_Fca0 = calculate_sum_tower_f_list(chiller_f_cooling_tower_list)
                chiller_P0 = list(result["chiller_P_total_main_equipment"])
                chiller_chilled_pump_P0 = list(result["chiller_P_total_chilled_pump"])
                chiller_cooling_pump_P0 = list(result["chiller_P_total_cooling_pump"])
                chiller_cooling_tower_P0 = list(result["chiller_P_total_cooling_tower"])
                ashp_Q0 = list(result["ashp_Q_total"])
                ashp_Few0 = list(result["ashp_Few_total"])
                ashp_P0 = list(result["ashp_P_total_main_equipment"])
                ashp_chilled_pump_P0 = list(result["ashp_P_total_chilled_pump"])
                Q0_total = []
                P0_total = []
                EER0 = []
                for k in range(len(chiller_P0)):
                    Q_tmp = chiller_Q0[k] + ashp_Q0[k]
                    Q0_total.append(Q_tmp)
                    P_tmp = (chiller_P0[k] + chiller_chilled_pump_P0[k] + chiller_cooling_pump_P0[k] +
                             chiller_cooling_tower_P0[k] + ashp_P0[k] + ashp_chilled_pump_P0[k])
                    P0_total.append(P_tmp)
                    if EER_mode == 0:
                        EER_tmp = Q_tmp / P_tmp
                    elif EER_mode == 1:
                        EER_tmp = Q_input / P_tmp
                    else:
                        EER_tmp = None
                    EER0.append(EER_tmp)
                # 第5步：生成系统阶跃响应实验的输入数据
                print("制冷功率(kW)：" + str(round(Q_input, 2)) + "，辨识输入：" + tf_obj +
                      "，正在生成系统阶跃响应实验的输入数据！")
                # 确定step_value
                if tf_obj == "Teo":
                    # 冷水机+空气源热泵
                    step_value = 2
                    input_type_list = chiller_input_type()[2] + air_source_heat_pump_input_type()[2]
                    input_data_list = [Teo0_set[-1] + step_value, Teo0_set[-1] + step_value]
                elif tf_obj == "chiller_Few":
                    chiller_Few_total = 1.2 * chiller_Few0[-1]
                    ans_chiller_Fw_step = calculate_Fw_step_value(chiller_system_type, "Few", chiller_Few_total,
                                                                  chiller_chilled_pump_list, n_chiller_chilled_pump_list,
                                                                  chiller_chilled_valve_open, chiller_cooling_valve_open,
                                                                  chiller_tower_valve_open, 0)
                    input_data_list = ans_chiller_Fw_step[0]
                    input_type_list = ans_chiller_Fw_step[1]
                elif tf_obj == "ashp_Few":
                    ashp_Few_total = 1.2 * ashp_Few0[-1]
                    ans_ashp_Fw_step = calculate_Fw_step_value(ashp_system_type, "Few", ashp_Few_total,
                                                               [ashp_chilled_pump], [n0_ashp_chilled_pump],
                                                               ashp_chilled_valve_open, 0, 0, 0)
                    input_data_list = ans_ashp_Fw_step[0]
                    input_type_list = ans_ashp_Fw_step[1]
                elif tf_obj == "Fcw":
                    Fcw_total = 1.3 * chiller_Fcw0[-1]
                    ans_Fw_step = calculate_Fw_step_value(chiller_system_type, tf_obj, Fcw_total,
                                                          chiller_cooling_pump_list, n_chiller_cooling_pump_list,
                                                          chiller_chilled_valve_open, chiller_cooling_valve_open,
                                                          chiller_tower_valve_open, 0)
                    input_data_list = ans_Fw_step[0]
                    input_type_list = ans_Fw_step[1]
                elif tf_obj == "Fca":
                    input_data_list, input_type_list = calculate_Fca_step_value(chiller_f_cooling_tower_list)
                else:
                    input_data_list = None
                    input_type_list = None
                # 第6步：系统阶跃响应实验
                print("制冷功率(kW)：" + str(round(Q_input, 2)) + "，辨识输入：" + tf_obj + "，正在进行系统阶跃响应实验！")
                result = main_simulate_station_fmu(input_data_list, input_type_list, simulate_time2, txt_path)
                chiller_f_cooling_tower_list = [list(result["chiller_f_cooling_tower1"])[1:],
                                                list(result["chiller_f_cooling_tower2"])[1:],
                                                list(result["chiller_f_cooling_tower3"])[1:],
                                                list(result["chiller_f_cooling_tower4"])[1:],
                                                list(result["chiller_f_cooling_tower5"])[1:],
                                                list(result["chiller_f_cooling_tower6"])[1:]]
                # user_Q1 = list(result["user_Q_total"])[1:]
                user_Tei1 = list(result["user_Tei"])[1:]
                # user_Few1 = list(result["user_Few_total"])[1:]
                Teo1_set = list(result["chiller_Teo_set"])[1:]  # ashp_Teo_set数值相同
                chiller_Q1 = list(result["chiller_Q_total"])[1:]
                chiller_Few1 = list(result["chiller_Few_total"])[1:]
                chiller_Fcw1 = list(result["chiller_Fcw_total"])[1:]
                chiller_Fca1 = calculate_sum_tower_f_list(chiller_f_cooling_tower_list)
                chiller_P1 = list(result["chiller_P_total_main_equipment"])[1:]
                chiller_chilled_pump_P1 = list(result["chiller_P_total_chilled_pump"])[1:]
                chiller_cooling_pump_P1 = list(result["chiller_P_total_cooling_pump"])[1:]
                chiller_cooling_tower_P1 = list(result["chiller_P_total_cooling_tower"])[1:]
                ashp_Q1 = list(result["ashp_Q_total"])[1:]
                ashp_Few1 = list(result["ashp_Few_total"])[1:]
                ashp_P1 = list(result["ashp_P_total_main_equipment"])[1:]
                ashp_chilled_pump_P1 = list(result["ashp_P_total_chilled_pump"])[1:]
                Q1_total = []
                P1_total = []
                EER1 = []
                for k in range(len(chiller_P1)):
                    Q_tmp = chiller_Q1[k] + ashp_Q1[k]
                    Q1_total.append(Q_tmp)
                    P_tmp = (chiller_P1[k] + chiller_chilled_pump_P1[k] + chiller_cooling_pump_P1[k] +
                             chiller_cooling_tower_P1[k] + ashp_P1[k] + ashp_chilled_pump_P1[k])
                    P1_total.append(P_tmp)
                    if EER_mode == 0:
                        EER_tmp = Q_tmp / P_tmp
                    elif EER_mode == 1:
                        EER_tmp = Q_input / P_tmp
                    else:
                        EER_tmp = None
                    EER1.append(EER_tmp)
                # 读取仿真的数据，并截取需要的部分
                # Q_total_list = Q0_total + Q1_total
                # P_total_list = P0_total + P1_total
                Teo_set_list = Teo0_set + Teo1_set
                # user_Few_list = user_Few0 + user_Few1
                chiller_Few_list = chiller_Few0 + chiller_Few1
                chiller_Fcw_list = chiller_Fcw0 + chiller_Fcw1
                chiller_Fca_list = chiller_Fca0 + chiller_Fca1
                ashp_Few_list = ashp_Few0 + ashp_Few1
                EER_list = EER0 + EER1
                user_Tei_list = user_Tei0 + user_Tei1
                # 第7步：确定传递函数辨识的输入X和输出Y
                # 只保留最后6个小时的数据，并换算到0初始值条件下
                # 模型输入X
                if tf_obj == "Teo":
                    start_index0 = int(len(Teo0_set) - n_data_save1)
                    X0_list = Teo0_set[start_index0:]
                    X0 = sum(X0_list) / len(X0_list)
                    start_index1 = int(len(Teo_set_list) - (n_data_save1 + n_data_save2))
                    X_list = Teo_set_list[start_index1:]
                    for k in range(len(X_list)):
                        X_list[k] -= X0
                elif tf_obj == "chiller_Few":
                    start_index0 = int(len(chiller_Few0) - n_data_save1)
                    X0_list = chiller_Few0[start_index0:]
                    X0 = sum(X0_list) / len(X0_list)
                    start_index1 = int(len(chiller_Few_list) - (n_data_save1 + n_data_save2))
                    X_list = chiller_Few_list[start_index1:]
                    for k in range(len(X_list)):
                        X_list[k] -= X0
                    x_Few_list.append(X_list)
                elif tf_obj == "ashp_Few":
                    start_index0 = int(len(ashp_Few0) - n_data_save1)
                    X0_list = ashp_Few0[start_index0:]
                    X0 = sum(X0_list) / len(X0_list)
                    start_index1 = int(len(ashp_Few_list) - (n_data_save1 + n_data_save2))
                    X_list = ashp_Few_list[start_index1:]
                    for k in range(len(X_list)):
                        X_list[k] -= X0
                    x_Few_list.append(X_list)
                elif tf_obj == "Fcw":
                    start_index0 = int(len(chiller_Fcw0) - n_data_save1)
                    X0_list = chiller_Fcw0[start_index0:]
                    X0 = sum(X0_list) / len(X0_list)
                    start_index1 = int(len(chiller_Fcw_list) - (n_data_save1 + n_data_save2))
                    X_list = chiller_Fcw_list[start_index1:]
                    for k in range(len(X_list)):
                        X_list[k] -= X0
                elif tf_obj == "Fca":
                    start_index0 = int(len(chiller_Fca0) - n_data_save1)
                    X0_list = chiller_Fca0[start_index0:]
                    X0 = sum(X0_list) / len(X0_list)
                    start_index1 = int(len(chiller_Fca_list) - (n_data_save1 + n_data_save2))
                    X_list = chiller_Fca_list[start_index1:]
                    for k in range(len(X_list)):
                        X_list[k] -= X0
                else:
                    X_list = None
                # 绘图，X
                index_figure += 1
                plt.figure(index_figure)
                plt.title("Q_input(kW):" + str(Q_input) + "; " + tf_obj)
                plt.plot(X_list)
                index_figure += 1
                # 模型输出Y
                for k in range(len(Y_mode_list)):
                    Y_mode = Y_mode_list[k]
                    if Y_mode == "EER":
                        start_index0 = int(len(EER0) - n_data_save1)
                        Y0_list = EER0[start_index0:]
                        Y0 = sum(Y0_list) / len(Y0_list)
                        start_index1 = int(len(EER_list) - (n_data_save1 + n_data_save2))
                        Y_list = EER_list[start_index1:]
                        for l in range(len(Y_list)):
                            Y_list[l] -= Y0
                        if tf_obj == "chiller_Few":
                            y_Few_EER_list.append(Y_list)
                        elif tf_obj == "ashp_Few":
                            y_Few_EER_list.append(Y_list)
                        # 绘图
                        plt.figure(index_figure)
                        plt.title("Q_input(kW):" + str(Q_input) + "; " + "EER: " + tf_obj)
                        plt.plot(Y_list)
                        index_figure += 1
                    elif Y_mode == "Tei":
                        start_index0 = int(len(user_Tei0) - n_data_save1)
                        Y0_list = user_Tei0[start_index0:]
                        Y0 = sum(Y0_list) / len(Y0_list)
                        start_index1 = int(len(user_Tei_list) - (n_data_save1 + n_data_save2))
                        Y_list = user_Tei_list[start_index1:]
                        # 如果是Fcw或者Fca，则Y_list全部改成0
                        for l in range(len(Y_list)):
                            if tf_obj == "Fcw" or tf_obj == "Fca":
                                Y_list[l] = 0
                            else:
                                Y_list[l] -= Y0
                        if tf_obj == "chiller_Few":
                            y_Few_Tei_list.append(Y_list)
                        elif tf_obj == "ashp_Few":
                            y_Few_Tei_list.append(Y_list)
                        # 绘图
                        plt.figure(index_figure)
                        plt.title("Q_input(kW):" + str(Q_input) + "; " + "Tei: " + tf_obj)
                        plt.plot(Y_list)
                        index_figure += 1
                    else:
                        Y_list = None
                    # 拼接数据，写入txt
                    if tf_obj == "chiller_Few" or tf_obj == "ashp_Few":
                        if Y_mode == "EER" and len(x_Few_list) == 2 and len(y_Few_EER_list) == 2:
                            tf_data_txt_list = []
                            for l in range(len(X_list)):
                                tmp = (str(x_Few_list[0][l]) + "\t" + str(y_Few_EER_list[0][l]) + "\t" +
                                       str(x_Few_list[1][l]) + "\t" + str(y_Few_EER_list[1][l]))
                                tf_data_txt_list.append(tmp)
                            write_txt_data(path_Few_EER_tfdata, tf_data_txt_list)
                        elif Y_mode == "Tei" and len(x_Few_list) == 2 and len(y_Few_Tei_list) == 2:
                            tf_data_txt_list = []
                            for l in range(len(X_list)):
                                tmp = (str(x_Few_list[0][l]) + "\t" + str(y_Few_Tei_list[0][l]) + "\t" +
                                       str(x_Few_list[1][l]) + "\t" + str(y_Few_Tei_list[1][l]))
                                tf_data_txt_list.append(tmp)
                            write_txt_data(path_Few_Tei_tfdata, tf_data_txt_list)
                    else:
                        tf_data_txt_list = []
                        for l in range(len(X_list)):
                            tmp = str(X_list[l]) + "\t" + str(Y_list[l])
                            tf_data_txt_list.append(tmp)
                        if tf_obj == "Teo" and Y_mode == "EER":
                            write_txt_data(path_Teo_EER_tfdata, tf_data_txt_list)
                        elif tf_obj == "Fcw" and Y_mode == "EER":
                            write_txt_data(path_Fcw_EER_tfdata, tf_data_txt_list)
                        elif tf_obj == "Fca" and Y_mode == "EER":
                            write_txt_data(path_Fca_EER_tfdata, tf_data_txt_list)
                        elif tf_obj == "Teo" and Y_mode == "Tei":
                            write_txt_data(path_Teo_Tei_tfdata, tf_data_txt_list)
                        elif tf_obj == "Fcw" and Y_mode == "Tei":
                            write_txt_data(path_Fcw_Tei_tfdata, tf_data_txt_list)
                        elif tf_obj == "Fca" and Y_mode == "Tei":
                            write_txt_data(path_Fca_Tei_tfdata, tf_data_txt_list)
                # 绘图
                plt.show()
                # 第9步：终止FMU模型
                print("制冷功率(kW)：" + str(round(Q_input, 2)) + "，辨识输入：" + tf_obj + "，正在终止FMU模型！")
                # 修改FMU状态
                fmu_state_list = [0, 1, stop_time, output_interval, time_out, tolerance]
                write_txt_data(file_fmu_state, fmu_state_list)
                # 最后仿真一次
                main_simulate_station_fmu([], [], simulate_time3, txt_path)

            # 第10步：辨识传递函数
            print("制冷功率(kW)：" + str(round(Q_input, 2)) + "，所有的传递函数辨识数据生成完成！")
            for j in range(len(Y_mode_list)):
                Y_mode = Y_mode_list[j]
                print("制冷功率(kW)：" + str(round(Q_input, 2)) + "，辨识输入：" + Y_mode + "，正在进行传递函数辨识!")
                info_txt = "Q=" + str(round(Q_input, 2)) + "kW"
                # 传递函数系统辨识
                ans_tf = estimate_transfer_function(path_tf, path_matlab, Ts, estf_object_list, n_object_list,
                                                    np_max, fitpercent_target_list, i + 1, Y_mode, True)
                tf_txt = "# " + Y_mode + "模型: " + info_txt + "\n"
                tf_txt += ans_tf
                tf_txt_list = [tf_txt]
                # 将结果写入txt文件
                if Y_mode == "EER":
                    path_result = path_result_EER
                elif Y_mode == "Tei":
                    path_result = path_result_Tei
                else:
                    path_result = None
                # 记录结果
                write_txt_data(path_result, tf_txt_list, write_model=1)
                # 结束循环
                print_txt = "传递函数辨识完成, 辨识的模型类型为：" + Y_mode + "；工况点序号为：" + \
                            str(i + 1) + ", " + info_txt + "\n"
                print(print_txt)
        except:
            print("动态特性辨识失败！制冷功率(kW)：" + str(round(Q_input, 2)) + "，跳过计算....")
            print(traceback.format_exc())
            pass


def calculate_Fw_step_value(system_type, tf_obj, Fw_total, pump_list, n_pump_list, chilled_valve_open,
                            cooling_valve_open, tower_valve_open, H_pump):
    """
    水泵，阶跃响应测试输入数据生成
    Args:
        system_type: [string]，设备类型名称
        tf_obj: [string]，需要被辨识的对象
        Fw_total: [float]，水流量总需求，t/h
        pump_list: [list]，水泵模型，列表
        n_pump_list: [list]，水泵装机数量，列表
        chilled_valve_open: [float]，冷冻阀门开启比例
        cooling_valve_open: [float]，冷却阀门开启比例
        tower_valve_open: [float]，冷却塔阀门开启比例
        H_pump: [float]，水泵目标扬程，m

    Returns:

    """
    # 阀门开启比例赋值
    if tf_obj == "Few":
        for pump in pump_list:
            pump.value_open = [chilled_valve_open, 1]
    elif tf_obj == "Fcw":
        for pump in pump_list:
            pump.value_open = [cooling_valve_open, tower_valve_open]
    # 确定input_type
    if system_type == "chiller":
        if tf_obj == "Few":
            input_type_list = chiller_input_type()[3]
        elif tf_obj == "Fcw":
            input_type_list = chiller_input_type()[4]
        else:
            input_type_list = None
    elif system_type == "air_source_heat_pump":
        if tf_obj == "Few":
            input_type_list = air_source_heat_pump_input_type()[3]
        else:
            input_type_list = None
    elif system_type == "energy_storage_equipment":
        if tf_obj == "Few":
            input_type_list = cold_storage_input_type()[1]
        else:
            input_type_list = None
    else:
        input_type_list = None
    # 确定input_data
    if system_type == "chiller":
        ans = main_optimization_water_pump(pump_list, n_pump_list, [0, 0], Fw_total,[0, 0], H_pump, 0)
        best_n1 = ans[2][0]
        best_n2 = ans[2][1]
        best_f1 = ans[3][0]
        best_f2 = ans[3][1]
        best_H1 = ans[4][0]
        best_H2 = ans[4][1]
        best_H = max(best_H1, best_H2)
        input_data_list = []
        for i in range(n_pump_list[0]):
            if i < best_n1:
                input_data_list.append(best_f1)
            else:
                input_data_list.append(0)
        for i in range(n_pump_list[1]):
            if i < best_n2:
                input_data_list.append(best_f2)
            else:
                input_data_list.append(0)
    elif system_type == "energy_storage_equipment" or system_type == "air_source_heat_pump":
        ans = main_optimization_water_pump(pump_list, n_pump_list, [0], Fw_total, [0], H_pump, 0)
        best_n = ans[2][0]
        best_f = ans[3][0]
        best_H = ans[4][0]
        input_data_list = []
        for i in range(n_pump_list[0]):
            if i < best_n:
                input_data_list.append(best_f)
            else:
                input_data_list.append(0)
    else:
        input_data_list = None
        best_H = None
    # 返回结果
    return input_data_list, input_type_list, best_H


def calculate_Fca_step_value(value_list):
    """
    冷却塔，阶跃响应测试输入数据生成
    Args:
        value_list: [list]，数值列表

    Returns:

    """
    # 确定input_type
    input_type_list = chiller_input_type()[5]
    # 所有的value都乘以50进行换算
    new_value_list = []
    for i in range(len(value_list)):
        tmp_list = []
        for j in range(len(value_list[i])):
            if value_list[i][j] <= 1:
                tmp_list.append(50 * value_list[i][j])
            else:
                tmp_list.append(value_list[i][j])
        new_value_list.append(tmp_list)
    # 只取value_list最后的值
    value_last_list = []
    for i in range(len(new_value_list)):
        value_last_list.append(new_value_list[i][-1])
    value_max = max(value_last_list)
    # 确定step_value
    if value_max >= 45:
        step_value = -10
    elif 40 <= value_max < 45:
        step_value = -7
    elif 35 <= value_max < 40:
        step_value = 7
    else:
        step_value = 10
    n_open = 0
    input_data_list = []
    for i in range(len(value_last_list)):
        value = value_last_list[i]
        if value <= 5:
            input_data_list.append(0)
        else:
            n_open += 1
            # 输入的值要是0-1的小数，所以要除以50
            input_data_list.append((value + step_value) / 50)
    # 返回结果
    return input_data_list, input_type_list


def calculate_sum_tower_f_list(value_list):
    """
    将冷却塔转速数据乘以50，并加和
    Args:
        value_list: [list]，数值列表

    Returns:

    """
    # 所有的value都乘以50进行换算
    new_value_list = []
    for i in range(len(value_list)):
        tmp_list = []
        for j in range(len(value_list[i])):
            if value_list[i][j] <= 1:
                tmp_list.append(50 * value_list[i][j])
            else:
                tmp_list.append(value_list[i][j])
        new_value_list.append(tmp_list)
    # value_list中的每一个值想加
    sum_value_list = []
    for i in range(len(new_value_list[0])):
        sum_tmp = 0
        for j in range(len(new_value_list)):
            sum_tmp += new_value_list[j][i]
        sum_value_list.append(sum_tmp)
    # 返回结果
    return sum_value_list