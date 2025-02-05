from algorithm_win import calculate_membership, smgpc, mmgpc
from model_fmu_dynamics import model_dynamics_complex_chiller, model_dynamics_chiller_ashp

if __name__ == "__main__":
    # model_mode: 0:仅冷水机；1:冷水机+空气源热泵
    model_mode = 0
    # 仿真类型：smgpc、mmgpc
    simulate_mode = "mmgpc"
    # 控制器目标
    y_gpc_list = ["EER", "Tei"]
    # MMGPC的计算模式，bayes、ms、itae
    mmgpc_mode = "bayes"
    # 多模型隶属度函数计算模式，0：梯形隶属度函数；1：三角形隶属度函数
    ms_mode = 0

    # MMGPC内置模型编号
    model_index = 0
    # 用于测试的被控对象模型编号
    plant_index = 4

    # 仿真时长和采样周期，单位：秒
    L = 24 * 3600
    Ts = 10 * 60
    # 仿真次数
    n = int(L / Ts)

    # V: 一个非常小的正实数，保证所有子控制器将来可用
    V = 0.0001
    # 多模型权值系数
    s_EER = 1
    s_Tei = 10000
    # MMGPC设置
    save_data_init = True
    plot_set = True
    model_plot_set = False

    # 输出目标值yr的初始值
    # EER, Tei
    EER0 = 4.5
    Tei0 = 14
    if "EER" in y_gpc_list and "Tei" in y_gpc_list:
        yr_0_list = [EER0, Tei0]
    elif "EER" in y_gpc_list and "Tei" not in y_gpc_list:
        yr_0_list = [EER0]
    elif "EER" not in y_gpc_list and "Tei" in y_gpc_list:
        yr_0_list = [EER0]
    else:
        yr_0_list = []
    # 控制指令u初始值
    # Teo, Few, Fcw, Fca
    Teo0 = 8
    Few10 = 1435
    Fcw0 = 1675
    Fca0 = 200
    Few20 = 400
    if model_mode == 0:
        u_0_list = [Teo0, Few10, Fcw0, Fca0]
    elif model_mode == 1:
        u_0_list = [Teo0, Few10, Fcw0, Fca0, Few20]
    else:
        u_0_list = []
    # 输出的目标值yr
    yr_EER_list = []
    yr_Tei_list = []
    for i in range(n + 1):
        if i <= 10:
            yr_EER_list.append(EER0)
            yr_Tei_list.append(Tei0)
        else:
            yr_EER_list.append(EER0 + 0.2)
            yr_Tei_list.append(Tei0 + 0.5)
    if "EER" in y_gpc_list and "Tei" in y_gpc_list:
        yr_list = [yr_EER_list, yr_Tei_list]
    elif "EER" in y_gpc_list and "Tei" not in y_gpc_list:
        yr_list = [yr_EER_list]
    elif "EER" not in y_gpc_list and "Tei" in y_gpc_list:
        yr_list = [yr_Tei_list]
    else:
        yr_list = []
    # 控制量限制
    if model_mode == 0:
        du_limit_list = [1, 50, 50, 50]
        u_limit_list = [[6, 15], [350, 3500], [450, 4200], [30, 300]]
    elif model_mode == 1:
        du_limit_list = [1, 50, 50, 50, 50]
        u_limit_list = [[6, 15], [350, 3500], [450, 4200], [30, 300], [100, 800]]
    else:
        du_limit_list = []
        u_limit_list = []
    # MMGPC内置系统动态模型
    if model_mode == 0:
        ans_model = model_dynamics_complex_chiller()
    elif model_mode == 1:
        ans_model = model_dynamics_chiller_ashp()
    else:
        ans_model = None
    Q_model_list = ans_model[0]
    if "EER" in y_gpc_list and "Tei" in y_gpc_list:
        model_list = ans_model[1]
    elif "EER" in y_gpc_list and "Tei" not in y_gpc_list:
        model_list = ans_model[2]
    elif "EER" not in y_gpc_list and "Tei" in y_gpc_list:
        model_list = ans_model[3]
    else:
        model_list = []
    Np_list = ans_model[4]
    Nc_list = ans_model[5]
    r_list = ans_model[6]
    if "EER" in y_gpc_list and "Tei" in y_gpc_list:
        q_list = ans_model[7]
    elif "EER" in y_gpc_list and "Tei" not in y_gpc_list:
        q_list = ans_model[8]
    elif "EER" not in y_gpc_list and "Tei" in y_gpc_list:
        q_list = ans_model[9]
    else:
        q_list = []

    # mmgpc仿真参数设置
    # 将初始化的控制器参数数据保存下来的路径
    if model_mode == 0:
        file_path_init = "./model_file/file_GPC/complex_chiller"
    elif model_mode == 1:
        file_path_init = "./model_file/file_GPC/chiller_ashp"
    else:
        file_path_init = ""
    # 多模型权值系数的递推计算收敛系数
    if "EER" in y_gpc_list and "Tei" in y_gpc_list:
        s_list = [s_EER, s_Tei]
    elif "EER" in y_gpc_list and "Tei" not in y_gpc_list:
        s_list = [s_EER]
    elif "EER" not in y_gpc_list and "Tei" in y_gpc_list:
        s_list = [s_Tei]
    else:
        s_list = []
    # 计算隶属度函数
    if mmgpc_mode == "ms" and simulate_mode == "mmgpc":
        ms_list = calculate_membership(Q_model_list[plant_index], Q_model_list, ms_mode)
    else:
        ms_list = []

    # 控制器仿真
    # smgpc
    if simulate_mode == "smgpc":
        smgpc(L, Ts, Np_list[model_index], Nc_list[model_index], model_list[model_index], r_list[model_index],
              q_list[model_index], yr_list, yr_0_list, u_0_list, du_limit_list, u_limit_list, True)
    elif simulate_mode == "mmgpc":
        mmgpc(L, Ts, Np_list, Nc_list, s_list, V, model_list[plant_index], model_list, r_list, q_list, yr_list,
              yr_0_list, u_0_list, du_limit_list, u_limit_list, file_path_init, save_data_init, ms_list, mmgpc_mode,
              plot_set, model_plot_set)