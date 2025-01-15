import numpy as np
from algorithm_win import simulate_sample, write_txt_data

def identify_user_characteristic(fmu_unzipdir, fmu_description, start_time, stop_time, output_interval, time_out,
                                 tolerance, Teo_min, Teo_max, Tdi_target):
    """
    辨识用户末端特性模型
    Args:
        fmu_unzipdir: [string]，FMU模型解压后的路径
        fmu_description: [object]，获取FMU模型描述
        start_time: [float]，仿真开始时间，单位：秒
        stop_time: [float]，仿真结束时间，单位：秒
        output_interval: [float]，FMU模型输出采样时间，单位：秒
        time_out: [float]，仿真超时时间，单位：秒
        tolerance: [float]，FMU模型求解相对误差
        Teo_min: [float]，冷冻水出水温度最小值
        Teo_max: [float]，冷冻水出水温度最大值
        Tdi_target: [float]，室内干球温度目标值

    Returns:

    """
    # 储存结果的开始编号，第一天的数据不储存
    start_index = int(24 * 3600 / output_interval)
    # 储存最终结果的文件路径
    path_result_txt = "./model_data/file_identify/result_user_characteristic/result_user_characteristic.txt"
    txt_str = ("冷冻水出水温度" + "\t" + "冷冻水流量" + "\t" + "室内干球温度" + "\t" + "室内相对湿度" + "\t" +
               "室外干球温度" + "\t" + "室外相对湿度" + "\t" + "制冷负荷" + "\t" + "冷冻水回水温度")
    result_list = [txt_str]
    # FMU输入输出
    input_type_list = [("time", np.float64), ("Teo", np.float64), ("Tdi_target", np.float64)]
    output_name_list = ["Teo", "user.Few", "Tdi", "Hri", "user.weather_data.TDryBul", "user.weather_data.relHum",
                        "Q", "Tei"]
    # 冷冻水出水温度
    Teo_list = []
    for i in range(Teo_max - Teo_min + 1):
        Teo_list.append(Teo_min + i)
    # 初始化FMU模型，使得系统稳定
    for i in range(len(Teo_list)):
        Teo = Teo_list[i]
        print("用户末端模型特性辨识，正在进行辨识的冷冻水出水温度为：" + str(Teo))
        input_data_list = [start_time, Teo, Tdi_target]
        result = simulate_sample(fmu_unzipdir, fmu_description, None, start_time, stop_time, input_data_list,
                                 input_type_list, output_name_list, output_interval, {}, time_out, tolerance,
                                 False, False)
        Few_list = list(result["user.Few"])[start_index:]
        Tdi_list = list(result["Tdi"])[start_index:]
        Hri_list = list(result["Hri"])[start_index:]
        Tdo_list = list(result["user.weather_data.TDryBul"])[start_index:]
        Hro_list = list(result["user.weather_data.relHum"])[start_index:]
        Q_list = list(result["Q"])[start_index:]
        Tei_list = list(result["Tei"])[start_index:]
        # Few和Q要乘以4，实际模型有4个房间，但是做特性辨识时只有1个
        for j in range(len(Q_list)):
            txt_tmp = (str(Teo) + "\t" + str(round(4 * Few_list[j], 2)) + "\t" + str(round(Tdi_list[j], 2)) + "\t" +
                       str(round(100 * Hri_list[j], 2)) + "\t" + str(round(Tdo_list[j] - 273.15, 2)) + "\t" +
                       str(round(100 * Hro_list[j], 2)) + "\t" + str(round(4 * Q_list[j], 2)) + "\t" +
                       str(round(Tei_list[j], 2)))
            result_list.append(txt_tmp)
    # 结果写入txt文件
    write_txt_data(path_result_txt, result_list)