import numpy as np
import pickle
import traceback
import matplotlib.pyplot as plt
from fmpy import *
from air_conditioner_dynamic import *
from algorithm_code.read_write_data import *
from algorithm_code.other import *
from algorithm_code import *
from run_initialize import run_initialize
from model_fmu_input_type import chiller_input_type, cold_storage_input_type, \
                                 simple_load_input_type, environment_input_type
from model_fmu_input_data_default import chiller_input_data_default, cold_storage_input_data_default, \
                                         simple_load_input_data_default, environment_input_data_default
from model_fmu_output_name import chiller_output_name, cold_storage_output_name, simple_load_output_name
from model_fmu_input_name import chiller_input_name, cold_storage_input_name

def main_identify_system_dynamics(fmu_unzipdir, fmu_description, start_time, stop_time, output_interval, Ts,
                                  time_out, np_max, fitpercent_target, chiller_object_list, chiller_Y_mode_list,
                                  chiller_Q_list, chiller_equipment_type_path, cfg_path_equipment, cfg_path_public):
    """

    Args:
        fmu_unzipdir: [string]，FMU模型解压后的路径
        fmu_description: [object]，获取FMU模型描述
        start_time: [float]，仿真开始时间，单位：秒
        stop_time: [float]，仿真结束时间，单位：秒
        output_interval: [float]，FMU模型输出采样时间，单位：秒
        Ts: [float]，采样时间
        time_out: [float]，仿真超时时间，单位：秒
        np_max: [int]，传递函数极点最大值
        fitpercent_target: [float]，传递函数辨识得分目标
        chiller_object_list: [list]，需要被辨识的对象列表：Fcw、Few、Fca、Teo、Tci等
        chiller_Y_mode_list: [list]，模型输出模式：EER/Tei
        chiller_Q_list: [list]，模型辨识指定的制冷功率，列表，单位：kW
        chiller_equipment_type_path: [string]，[list]，设备类型名称，相对路径
        cfg_path_equipment:[string]，设备信息参数cfg文件路径
        cfg_path_public:[string]，公用参数cfg文件路径

    Returns:

    """
    # 相对路径
    txt_path = chiller_equipment_type_path[1]
    # FMU相关文件路径
    file_fmu_address = txt_path + "/process_data/fmu_address.txt"
    # FMU模型仿真时间：仿真开始的时间(start_time)
    file_fmu_time = txt_path + "/process_data/fmu_time.txt"
    # FMU模型状态：依次为：fmu_initialize, fmu_terminate, stop_time, output_interval, time_out
    file_fmu_state = txt_path + "/process_data/fmu_state.txt"
    # FMU模型输出名称
    file_fmu_output_name = txt_path + "/process_data/fmu_output_name.pkl"
    # 仿真结果
    file_fmu_result_all = "./model_data/simulate_result/fmu_result_all.txt"
    file_fmu_result_last = "./model_data/simulate_result/fmu_result_last.txt"
    # 设备的pkl文件路径
    file_pkl_chiller = "./model_data/file_equipment/chiller.pkl"
    file_pkl_stroage = "./model_data/file_equipment/storage.pkl"
    file_pkl_system = "./model_data/file_equipment/system.pkl"
    # 用来拟合传递函数的数据储存路径：EER
    path_Few_EER_tfdata = './model_data/file_txt/result_system_dynamics/tf_Few_EER.txt'  # 冷冻水流量
    path_Fcw_EER_tfdata = './model_data/file_txt/result_system_dynamics/tf_Fcw_EER.txt'  # 冷却水流量
    path_Fca_EER_tfdata = './model_data/file_txt/result_system_dynamics/tf_Fca_EER.txt'  # 冷却塔风量
    path_Teo_EER_tfdata = './model_data/file_txt/result_system_dynamics/tf_Teo_EER.txt'  # 冷冻水出水温度
    # 用来拟合传递函数的数据储存路径：Tei
    path_Few_Tei_tfdata = './model_data/file_txt/result_system_dynamics/tf_Few_Tei.txt'  # 冷冻水流量
    path_Fcw_Tei_tfdata = './model_data/file_txt/result_system_dynamics/tf_Fcw_Tei.txt'  # 冷却水流量
    path_Fca_Tei_tfdata = './model_data/file_txt/result_system_dynamics/tf_Fca_Tei.txt'  # 冷却塔风量
    path_Teo_Tei_tfdata = './model_data/file_txt/result_system_dynamics/tf_Teo_Tei.txt'  # 冷冻水出水温度
    # 储存最终结果文本的文件路径
    path_result_EER = './model_data/file_txt/result_system_dynamics/result_transfer_function_EER.txt'
    path_result_Tei = './model_data/file_txt/result_system_dynamics/result_transfer_function_Tei.txt'
    # 传递函数数据的.txt文件文件所在的文件夹路径
    path_tf = './model_data/file_txt/result_system_dynamics'
    # 冷水机系统动态特性辨识
    identify_chiller_dynamics(fmu_unzipdir, fmu_description, file_fmu_address, file_fmu_time, file_fmu_state,
                              file_fmu_output_name, file_fmu_result_all, file_fmu_result_last, file_pkl_chiller,
                              file_pkl_system, start_time, stop_time, output_interval, Ts, time_out, path_result_EER,
                              path_result_Tei, path_tf, path_Few_EER_tfdata, path_Fcw_EER_tfdata, path_Fca_EER_tfdata,
                              path_Teo_EER_tfdata, path_Few_Tei_tfdata, path_Fcw_Tei_tfdata, path_Fca_Tei_tfdata,
                              path_Teo_Tei_tfdata, np_max, fitpercent_target, chiller_object_list, chiller_Y_mode_list,
                              chiller_Q_list, chiller_equipment_type_path, cfg_path_equipment, cfg_path_public)


def identify_chiller_dynamics(fmu_unzipdir, fmu_description, file_fmu_address, file_fmu_time, file_fmu_state,
                              file_fmu_output_name, file_fmu_result_all, file_fmu_result_last, file_pkl_chiller,
                              file_pkl_system, start_time, stop_time, output_interval, Ts, time_out, path_result_EER,
                              path_result_Tei, path_tf, path_Few_EER_tfdata, path_Fcw_EER_tfdata, path_Fca_EER_tfdata,
                              path_Teo_EER_tfdata, path_Few_Tei_tfdata, path_Fcw_Tei_tfdata, path_Fca_Tei_tfdata,
                              path_Teo_Tei_tfdata, np_max, fitpercent_target, object_list, Y_mode_list, Q_list,
                              chiller_equipment_type_path, cfg_path_equipment, cfg_path_public):
    """

    Args:
        fmu_unzipdir: [string]，FMU模型解压后的路径
        fmu_description: [object]，获取FMU模型描述
        file_fmu_address: [string]，储存FMU模型对象内存地址文件路径
        file_fmu_time: [string]，储存FMU模型仿真时间(start_time)的文件路径
        file_fmu_state: [string]，储存FMU模型状态的文件路径
        file_fmu_output_name: [string]，储存FMU模型输出名称的文件路径
        file_fmu_result_all: [string]，储存FMU模型所有仿真结果的文件路径
        file_fmu_result_last: [string]，储存FMU模型每次仿真最后时刻结果的文件路径
        file_pkl_chiller: [string]，冷水机系统信息储存路径
        file_pkl_system: [string]，公用系统信息储存路径
        start_time: [float]，仿真开始时间，单位：秒
        stop_time: [float]，仿真结束时间，单位：秒
        output_interval: [float]，FMU模型输出采样时间，单位：秒
        Ts: [float]，采样时间
        time_out: [float]，仿真超时时间，单位：秒
        path_result_EER: [string]，储存最终结果文本的文件路径
        path_result_Tei: [string]，储存最终结果文本的文件路径
        path_tf: [string]，需要读取的.txt文件文件所在的文件夹路径
        path_Few_EER_tfdata: [string]，冷冻水流量阶跃响应传递函数建模数据
        path_Fcw_EER_tfdata: [string]，冷却水流量阶跃响应传递函数建模数据
        path_Fca_EER_tfdata: [string]，冷却塔风量阶跃响应传递函数建模数据
        path_Teo_EER_tfdata: [string]，冷冻水出水温度阶跃响应传递函数建模数据
        path_Few_Tei_tfdata: [string]，冷冻水流量阶跃响应传递函数建模数据
        path_Fcw_Tei_tfdata: [string]，冷却水流量阶跃响应传递函数建模数据
        path_Fca_Tei_tfdata: [string]，冷却塔风量阶跃响应传递函数建模数据
        path_Teo_Tei_tfdata: [string]，冷冻水出水温度阶跃响应传递函数建模数据
        np_max: [int]，传递函数极点最大值
        fitpercent_target: [float]，传递函数辨识得分目标
        object_list: [list]，需要被辨识的对象列表：Fcw、Few、Fca、Teo、Tci等
        Y_mode_list: [list]，模型输出模式：EER/Tei
        Q_list: [list]，模型辨识指定的制冷功率，列表，单位：kW
        chiller_equipment_type_path: [string]，[list]，设备类型名称，相对路径
        cfg_path_equipment:[string]，设备信息参数cfg文件路径
        cfg_path_public:[string]，公用参数cfg文件路径

    Returns:

    """
    # 设备类型
    equipment_type = chiller_equipment_type_path[0]
    # 相对路径
    txt_path = chiller_equipment_type_path[1]
    # FMU模型输出名称
    fmu_output_name = chiller_output_name()[0] + cold_storage_output_name()[0] + simple_load_output_name() + \
                      chiller_input_name()[0] + cold_storage_input_name()[0]
    # 读取冷水机设备信息
    with open(file_pkl_chiller, "rb") as f_obj:
        chiller_dict = pickle.load(f_obj)
    H_chiller_chilled_pump = chiller_dict["H_chiller_chilled_pump"]
    H_chiller_cooling_pump = chiller_dict["H_chiller_cooling_pump"]
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
    n_chiller_user_value = chiller_dict["n_chiller_user_value"]
    # 读取公共系统信息
    with open(file_pkl_system, "rb") as f_obj:
        system_dict = pickle.load(f_obj)
    n_calculate_hour = system_dict["n_calculate_hour"]

    # 清空txt文件
    root_path1 = "./model_data/file_txt/result_system_dynamics"
    clear_all_txt_data(root_path1)
    # 遍历所有制冷功率
    for i in range(len(Q_list)):
        # 获取制冷功率，单位：kW
        Q_input = Q_list[i]
        # 遍历所有需要辨识的项目类型
        for j in range(len(object_list)):
            tf_obj = object_list[j]
            # 第1步:初始化FMU模型
            print("制冷功率(kW)：" + str(round(Q_input, 2)) + "，辨识输入：" + tf_obj + "，正在初始化FMU模型!")
            # 重置所有内容
            run_initialize(txt_path)
            # 生成FMU输出名称文件
            with open(file_fmu_output_name, 'wb') as f:
                pickle.dump(fmu_output_name, f)
            # 仿真结果
            txt_str = "start_time" + "\t" + "pause_time"
            for i in range(len(fmu_output_name)):
                txt_str += "\t" + fmu_output_name[i]
            write_txt_data(file_fmu_result_all, [txt_str])
            write_txt_data(file_fmu_result_last, [txt_str])
            # 模型初始化和实例化
            fmu_instance = instantiate_fmu(unzipdir=fmu_unzipdir, model_description=fmu_description)
            # 获取内存地址
            unzipdir_address = id(fmu_unzipdir)
            description_address = id(fmu_description)
            instance_address = id(fmu_instance)
            fmu_address_list = [unzipdir_address, description_address, instance_address]
            write_txt_data(file_fmu_address, fmu_address_list)
            # FMU模型状态：依次为：fmu_initialize, fmu_terminate, stop_time, output_interval, time_out
            fmu_state_list = [1, 0, stop_time, output_interval, time_out]
            write_txt_data(file_fmu_state, fmu_state_list)
            # 写入start_time
            write_txt_data(file_fmu_time, [start_time])
            # 模型输入名称和类型
            input_type_list = [('time', np.float_)] + environment_input_type()[0] + chiller_input_type()[0] + \
                              cold_storage_input_type()[0] + simple_load_input_type()
            # 模型输入数据
            input_data_list = [start_time] + environment_input_data_default() + chiller_input_data_default() + \
                              cold_storage_input_data_default() + simple_load_input_data_default()
            initialize_time = 3600
            # FMU仿真
            main_simulate_pause_single(input_data_list, input_type_list, initialize_time, txt_path, add_input=False)
            # 第2步：更新初始化设置
            # 修改FMU状态
            fmu_state_list = [0, 0, stop_time, output_interval, time_out]
            write_txt_data(file_fmu_state, fmu_state_list)
            # 第3步：优化冷水机系统并进行控制命令下发
            print("制冷功率(kW)：" + str(round(Q_input, 2)) + "，辨识输入：" + tf_obj + "，正在优化冷水机系统并进行控制命令下发!")
            algorithm_chiller_double(Q_input, H_chiller_chilled_pump, 0, H_chiller_cooling_pump, chiller1,
                                     chiller2, chiller_chilled_pump1, chiller_chilled_pump2, None, None,
                                     chiller_cooling_pump1, chiller_cooling_pump2, chiller_cooling_tower, None,
                                     n0_chiller1, n0_chiller2, n0_chiller_chilled_pump1, n0_chiller_chilled_pump2,
                                     0, 0, n0_chiller_cooling_pump1, n0_chiller_cooling_pump2, n0_chiller_cooling_tower,
                                     0, chiller_equipment_type_path, n_calculate_hour, n_chiller_user_value,
                                     cfg_path_equipment, cfg_path_public)
            # 第4步：系统仿真15小时，确保系统稳定，并获取数据
            print("制冷功率(kW)：" + str(round(Q_input, 2)) + "，辨识输入：" + tf_obj + "，正在持续仿真，确保系统稳定!")
            # 修改采样时间
            fmu_state_list = [0, 0, stop_time, Ts, time_out]
            write_txt_data(file_fmu_state, fmu_state_list)
            simulate_time = 15 * 3600
            # 模型输入名称和类型
            input_type_list = simple_load_input_type()
            # 模型输入数据
            input_data_list = [Q_input * 1000]
            result = main_simulate_pause_single(input_data_list, input_type_list, simulate_time, txt_path)
            # 获取系统稳定后的数据，用于系统辨识初始值
            chiller_f_chilled_pump_list = [list(result["chiller_f_chilled_pump1"]),
                                           list(result["chiller_f_chilled_pump2"]),
                                           list(result["chiller_f_chilled_pump3"]),
                                           list(result["chiller_f_chilled_pump4"]),
                                           list(result["chiller_f_chilled_pump5"]),
                                           list(result["chiller_f_chilled_pump6"])]
            chiller_f_cooling_pump_list = [list(result["chiller_f_cooling_pump1"]),
                                           list(result["chiller_f_cooling_pump2"]),
                                           list(result["chiller_f_cooling_pump3"]),
                                           list(result["chiller_f_cooling_pump4"]),
                                           list(result["chiller_f_cooling_pump5"]),
                                           list(result["chiller_f_cooling_pump6"])]
            chiller_f_cooling_tower_list = [list(result["chiller_f_cooling_tower1"]),
                                            list(result["chiller_f_cooling_tower2"]),
                                            list(result["chiller_f_cooling_tower3"]),
                                            list(result["chiller_f_cooling_tower4"]),
                                            list(result["chiller_f_cooling_tower5"]),
                                            list(result["chiller_f_cooling_tower6"])]
            chiller_Teo0 = list(result["chiller_Teo"])
            chiller_Few0 = list(result["chiller_Few_total"])
            chiller_Fcw0 = list(result["chiller_Fcw_total"])
            chiller_EER0 = list(result["chiller_EER"])
            chiller_Tei0 = list(result["chiller_Tei"])
            chiller_Fca0 = calculate_sum_value_list(chiller_f_cooling_tower_list)
            chiller_Q0 = list(result["chiller_Q_total"])
            chiller_P0 = list(result["chiller_P_total_main_equipment"])
            chilled_pump_P0 = list(result["chiller_P_total_chilled_pump"])
            cooling_pump_P0 = list(result["chiller_P_total_cooling_pump"])
            cooling_tower_P0 = list(result["chiller_P_total_cooling_tower"])
            # 第5步：生成系统阶跃响应实验的输入数据
            print("制冷功率(kW)：" + str(round(Q_input, 2)) + "，辨识输入：" + tf_obj + "，正在生成系统阶跃响应实验的输入数据！")
            # 确定step_value
            if tf_obj == "Teo":
                step_value = 2
                input_type_list = chiller_input_type()[2]
                input_data_list = [chiller_Teo0[-1] + step_value]
            elif tf_obj == "Few":
                value_list = chiller_f_chilled_pump_list
                input_data_list, input_type_list = get_simulate_step_value(equipment_type, tf_obj, value_list)
            elif tf_obj == "Fcw":
                value_list = chiller_f_cooling_pump_list
                input_data_list, input_type_list = get_simulate_step_value(equipment_type, tf_obj, value_list)
            elif tf_obj == "Fca":
                value_list = chiller_f_cooling_tower_list
                input_data_list, input_type_list = get_simulate_step_value(equipment_type, tf_obj, value_list)
            else:
                input_data_list = None
                input_type_list = None
            # 第6步：系统阶跃响应实验
            print("制冷功率(kW)：" + str(round(Q_input, 2)) + "，辨识输入：" + tf_obj + "，正在进行系统阶跃响应实验！")
            simulate_time = 4 * 3600
            result = main_simulate_pause_single(input_data_list, input_type_list, simulate_time, txt_path)
            chiller_f_cooling_tower_list = [list(result["chiller_f_cooling_tower1"]),
                                            list(result["chiller_f_cooling_tower2"]),
                                            list(result["chiller_f_cooling_tower3"]),
                                            list(result["chiller_f_cooling_tower4"]),
                                            list(result["chiller_f_cooling_tower5"]),
                                            list(result["chiller_f_cooling_tower6"])]
            chiller_Teo1 = list(result["chiller_Teo"])
            chiller_Few1 = list(result["chiller_Few_total"])
            chiller_Fcw1 = list(result["chiller_Fcw_total"])
            chiller_Fca1 = calculate_sum_value_list(chiller_f_cooling_tower_list)
            chiller_EER1 = list(result["chiller_EER"])
            chiller_Tei1 = list(result["chiller_Tei"])
            chiller_Q1 = list(result["chiller_Q_total"])
            chiller_P1 = list(result["chiller_P_total_main_equipment"])
            chilled_pump_P1 = list(result["chiller_P_total_chilled_pump"])
            cooling_pump_P1 = list(result["chiller_P_total_cooling_pump"])
            cooling_tower_P1 = list(result["chiller_P_total_cooling_tower"])
            # 读取仿真的数据，并截取需要的部分
            chiller_Teo_list = chiller_Teo0 + chiller_Teo1
            chiller_Few_list = chiller_Few0 + chiller_Few1
            chiller_Fcw_list = chiller_Fcw0 + chiller_Fcw1
            chiller_Fca_list = chiller_Fca0 + chiller_Fca1
            chiller_EER_list = chiller_EER0 + chiller_EER1
            chiller_Tei_list = chiller_Tei0 + chiller_Tei1
            chiller_Q_list = chiller_Q0 + chiller_Q1
            chiller_P_list = chiller_P0 + chiller_P1
            chilled_pump_P_list = chilled_pump_P0 + chilled_pump_P1
            cooling_pump_P_list = cooling_pump_P0 + cooling_pump_P1
            cooling_tower_P_list = cooling_tower_P0 + cooling_tower_P1
            P_total_list = []
            # Q、P、EER绘图
            for o in range(len(chiller_Q_list)):
                P_total = chiller_P_list[o] + chilled_pump_P_list[o] + cooling_pump_P_list[o] + cooling_tower_P_list[o]
                P_total_list.append(P_total)
            plt.figure(1)
            plt.title("X = " + tf_obj + "，chiller_Q")
            plt.xlabel("t(s)")
            plt.ylabel("chiller_Q")
            plt.plot(chiller_Q_list, color='blue', label='chiller_Q')
            plt.figure(2)
            plt.title("X = " + tf_obj + "，P_total")
            plt.xlabel("t(s)")
            plt.ylabel("P_total")
            plt.plot(P_total_list, color='blue', label='P_total')
            plt.figure(3)
            plt.title("X = " + tf_obj + "，EER")
            plt.xlabel("t(s)")
            plt.ylabel("EER")
            plt.plot(chiller_EER_list, color='blue', label='EER')
            plt.legend()
            plt.show()
            # 第7步：确定传递函数辨识的输入X和输出Y
            # 只保留最后6个小时的数据，并换算到0初始值条件下
            # 模型输入X
            if tf_obj == "Teo":
                start_index = int(len(chiller_Teo_list) - 6 * 3600 / Ts)
                X_list = chiller_Teo_list[start_index:]
                for n in range(len(X_list)):
                    X_list[n] = X_list[n] - chiller_Teo0[-1]
            elif tf_obj == "Few":
                start_index = int(len(chiller_Few_list) - 6 * 3600 / Ts)
                X_list = chiller_Few_list[start_index:]
                for n in range(len(X_list)):
                    X_list[n] = X_list[n] - chiller_Few0[-1]
            elif tf_obj == "Fcw":
                start_index = int(len(chiller_Fcw_list) - 6 * 3600 / Ts)
                X_list = chiller_Fcw_list[start_index:]
                for n in range(len(X_list)):
                    X_list[n] = X_list[n] - chiller_Fcw0[-1]
            elif tf_obj == "Fca":
                start_index = int(len(chiller_Fca_list) - 6 * 3600 / Ts)
                X_list = chiller_Fca_list[start_index:]
                for n in range(len(X_list)):
                    X_list[n] = X_list[n] - chiller_Fca0[-1]
            else:
                X_list = None
            # 模型输出Y
            for k in range(len(Y_mode_list)):
                Y_mode = Y_mode_list[k]
                if Y_mode == "EER":
                    start_index = int(len(chiller_EER_list) - 6 * 3600 / Ts)
                    Y_list = chiller_EER_list[start_index:]
                    for n in range(len(Y_list)):
                        Y_list[n] = Y_list[n] - chiller_EER0[-1]
                elif Y_mode == "Tei":
                    start_index = int(len(chiller_Tei_list) - 6 * 3600 / Ts)
                    Y_list = chiller_Tei_list[start_index:]
                    for n in range(len(Y_list)):
                        Y_list[n] = Y_list[n] - chiller_Tei0[-1]
                else:
                    Y_list = None
                # 拼接数据，写入txt
                tf_txt_list = []
                for l in range(len(X_list)):
                    tmp = str(X_list[l]) + "\t" + str(Y_list[l])
                    tf_txt_list.append(tmp)
                if tf_obj == "Teo" and Y_mode == "EER":
                    write_txt_data(path_Teo_EER_tfdata, tf_txt_list)
                elif tf_obj == "Few" and Y_mode == "EER":
                    write_txt_data(path_Few_EER_tfdata, tf_txt_list)
                elif tf_obj == "Fcw" and Y_mode == "EER":
                    write_txt_data(path_Fcw_EER_tfdata, tf_txt_list)
                elif tf_obj == "Fca" and Y_mode == "EER":
                    write_txt_data(path_Fca_EER_tfdata, tf_txt_list)
                elif tf_obj == "Teo" and Y_mode == "Tei":
                    write_txt_data(path_Teo_Tei_tfdata, tf_txt_list)
                elif tf_obj == "Few" and Y_mode == "Tei":
                    write_txt_data(path_Few_Tei_tfdata, tf_txt_list)
                elif tf_obj == "Fcw" and Y_mode == "Tei":
                    write_txt_data(path_Fcw_Tei_tfdata, tf_txt_list)
                elif tf_obj == "Fca" and Y_mode == "Tei":
                    write_txt_data(path_Fca_Tei_tfdata, tf_txt_list)
            # 第8步：终止FMU模型
            print("制冷功率(kW)：" + str(round(Q_input, 2)) + "，辨识输入：" + tf_obj + "，正在终止FMU模型！")
            # 修改FMU状态
            fmu_state_list = [0, 1, stop_time, output_interval, time_out]
            write_txt_data(file_fmu_state, fmu_state_list)
            # 最后仿真一次
            main_simulate_pause_single([], [], 3600, txt_path)

        # 第9步：辨识传递函数
        print("制冷功率(kW)：" + str(round(Q_input, 2)) + "，所有的传递函数辨识数据生成完成！")
        for m in range(len(Y_mode_list)):
            Y_mode = Y_mode_list[m]
            print("制冷功率(kW)：" + str(round(Q_input, 2)) + "，辨识输出：" + Y_mode + "，正在进行传递函数辨识!")
            info_txt = "Q=" + str(round(Q_input, 2)) + "kW, "
            try:
                # 传递函数系统辨识
                ans_tf = estimate_transfer_function(path_tf, Ts, object_list, np_max, fitpercent_target, i + 1,
                                                    Y_mode, False)
                tf_txt = "# " + Y_mode + "模型: " + info_txt + "\n"
                tf_txt += ans_tf
                tf_txt_list = [tf_txt]
            except:
                print_txt = "正在进行辨识的模型类型为：" + Y_mode + "；传递函数辨识出现异常，工况点序号为：" + \
                            str(i + 1) + ", " + info_txt
                tf_txt_list = []
                print(print_txt)
                print(traceback.format_exc())
                pass
            # 将结果写入txt文件
            if Y_mode == "EER":
                path_result = path_result_EER
            elif Y_mode == "Tei":
                path_result = path_result_Tei
            else:
                path_result = None
            write_txt_data(path_result, tf_txt_list, write_model=1)


def get_simulate_step_value(equipment_type, tf_obj, value_list):
    """
    水泵和冷却塔，阶跃响应测试输入数据生成
    Args:
        equipment_type: [string]，设备类型
        tf_obj: [string]，辨识的对象类型
        value_list: [list]，数值列表

    Returns:

    """
    # 只取value_list最后的值
    value_last_list = []
    for i in range(len(value_list)):
        value_last_list.append(value_list[i][-1])
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
    input_data_list = []
    for i in range(len(value_last_list)):
        value = value_last_list[i]
        if value <= 1:
            input_data_list.append(0)
        else:
            input_data_list.append(value + step_value)
    # 确定input_type
    if equipment_type == "chiller":
        if tf_obj == "Few":
            input_type_list = chiller_input_type()[3]
        elif tf_obj == "Fcw":
            input_type_list = chiller_input_type()[4]
        elif tf_obj == "Fca":
            input_type_list = chiller_input_type()[5]
        else:
            input_type_list = None
    elif equipment_type == "energy_storage_equipment":
        if tf_obj == "Few":
            input_type_list = cold_storage_input_type()[1]
        else:
            input_type_list = None
    else:
        input_type_list = None
    # 返回结果
    return input_data_list, input_type_list


def calculate_sum_value_list(value_list):
    """

    Args:
        value_list: [list]，数值列表

    Returns:

    """
    # value_list中的每一个值想加
    sum_value_list = []
    for i in range(len(value_list[0])):
        sum_tmp = 0
        for j in range(len(value_list)):
            sum_tmp += value_list[j][i]
        sum_value_list.append(sum_tmp)
    # 返回结果
    return sum_value_list