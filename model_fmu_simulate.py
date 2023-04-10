import numpy as np
import matplotlib.pyplot as plt
from fmpy import *
from fmpy.util import write_csv

def simulate_sample(fmu_path, csv_path, start_time, stop_time, input_data_list, input_type_list, output_name_list,
                    output_interval, plot_set, write_csv_set):
    """
    FMU模型仿真，从开始直接仿真到结束，中间不进行额外处理

    Args:
        fmu_path: [string]，FMU文件路径
        csv_path: [string]，CSV文件路径
        start_time: [float]，仿真开始时间，单位：秒
        stop_time: [float]，仿真结束时间，单位：秒
        input_data_list: [double/boolean，list]，FMU模型输入数值，列表
        input_type_list: [string，list]，FMU模型输入变量名和数据类型，列表
        output_name_list: [string，list]，FMU模型输出变量名，列表
        output_interval: [float]，FMU模型输出采样时间，单位：秒
        plot_set: [boolean]，是否绘图
        write_csv_set: [boolean]，是否将仿真结果写入CSV文件

    Returns:

    """
    # 模型输入
    fmu_input = np.array(input_data_list, dtype=input_type_list)
    # 仿真
    result = simulate_fmu(filename=fmu_path, start_time=start_time, stop_time=stop_time, input=fmu_input,
                          output=output_name_list, output_interval=output_interval)
    # 写入CSV文件
    if write_csv_set == True:
        write_csv(csv_path, result)
    # 仿真结果绘图
    if plot_set == True:
        for i in range(len(output_name_list)):
            output_data = result[output_name_list[i]]
            plt.figure(i+1)
            plt.title(output_name_list[i])
            plt.xlabel('time')
            plt.ylabel(output_name_list[i])
            plt.plot(output_data, color='skyblue', label=output_name_list[i])
            plt.legend()
        plt.show()
    # 返回结果
    return result


def simulate_pause(fmu_path, start_time_list, pause_time_list, stop_time, input_data_list, input_type_list,
                   output_name_list, output_interval, plot_set):
    """
    FMU模型仿真，可以自定义进行模型仿真的启动、暂停和终止

    Args:
        fmu_path: [string]，FMU文件路径
        start_time_list: [float，list]，仿真开始时间，列表，单位：秒
        pause_time_list: [float，list]，仿真暂停时间，列表，单位：秒
        stop_time: [float]，仿真结束时间，单位：秒
        input_data_list: [double/boolean，list]，FMU模型输入数值，列表
        input_type_list: [string，list]，FMU模型输入变量名和数据类型，列表
        output_name_list: [string，list]，FMU模型输出变量名，列表
        output_interval: [float]，FMU模型输出采样时间，单位：秒
        plot_set: [boolean]，是否绘图

    Returns:

    """
    # 模型初始化
    unzipdir = extract(fmu_path)
    model_description = read_model_description(unzipdir)
    fmu_instance = instantiate_fmu(unzipdir=unzipdir, model_description=model_description)
    # 列表，储存仿真结果
    result_list = []
    for i in range(len(output_name_list)):
        result_list.append([])
    # 仿真次数
    n_simulate = len(start_time_list)
    for i in range(n_simulate):
        # 暂停判定
        pause_time = pause_time_list[i]
        def pause_simulation(time, recorder):
            nonlocal pause_time
            if time >= pause_time:
                pause_time = time
                return False
            return True
        # 模型输入
        fmu_input = np.array(input_data_list[i], dtype=input_type_list)
        # 模型仿真
        if i == 0:
            # 第一次仿真，需要初始化，不需要终止
            tmp_sim = simulate_fmu(filename=unzipdir, model_description=model_description, fmu_instance=fmu_instance,
                                   start_time=start_time_list[i], stop_time=stop_time, input=fmu_input,
                                   output_interval=output_interval, output=output_name_list,
                                   step_finished=pause_simulation, initialize=True, terminate=False)
        elif 0 < i < n_simulate - 1:
            # 需要中间暂停，不需要初始化，不需要终止
            tmp_sim = simulate_fmu(filename=unzipdir, model_description=model_description, fmu_instance=fmu_instance,
                                   start_time=start_time_list[i], stop_time=stop_time, input=fmu_input,
                                   output_interval=output_interval, output=output_name_list,
                                   step_finished=pause_simulation, initialize=False, terminate=False)
        else:
            # 结束仿真，不需要初始化，需要终止
            tmp_sim = simulate_fmu(filename=unzipdir, model_description=model_description, fmu_instance=fmu_instance,
                                   start_time=start_time_list[i], stop_time=stop_time, input=fmu_input,
                                   output_interval=output_interval, output=output_name_list,
                                   step_finished=pause_simulation, initialize=False, terminate=True)
        # 记录每次仿真的结果
        for j in range(len(output_name_list)):
            output_data = tmp_sim[output_name_list[j]][-1]
            result_list[j].append(output_data)
    # 仿真结果绘图
    if plot_set == True:
        for i in range(len(output_name_list)):
            output_data = result_list[i]
            plt.figure(i + 1)
            plt.title(output_name_list[i])
            plt.xlabel('time')
            plt.ylabel(output_name_list[i])
            plt.plot(output_data, color='skyblue', label=output_name_list[i])
            plt.legend()
        plt.show()