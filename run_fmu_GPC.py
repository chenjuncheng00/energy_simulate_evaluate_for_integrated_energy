from GPC_universal import *
from model_fmu_dynamics import model_fmu_dynamics, plant_fmu_dynamics

if __name__ == "__main__":
    # 仿真类型：smgpc、mmgpc
    simulate_mode = 'mmgpc'
    # 控制器目标
    y_gpc_list = ['EER', 'Tei']

    # MMGPC内置模型编号
    model_index = 2
    # 用于测试的被控对象模型编号
    plant_index = 2

    # 仿真时长和采样周期，单位：秒
    L = 20 * 3600
    Ts = 10 * 60
    # 仿真次数
    n = int(L / Ts)

    # MMGPC的计算模式，bayes、ms、itae
    mmgpc_mode = "itae"
    # 多模型隶属度函数计算模式，0：梯形隶属度函数；1：三角形隶属度函数
    ms_mode = 0
    # V: 一个非常小的正实数，保证所有子控制器将来可用
    V = 0.0001
    # 多模型权值系数
    s_EER = 1
    s_Tei = 10
    # MMGPC设置
    save_data_init = False
    plot_set = True
    model_plot_set = False

    # 输出目标值yr的初始值
    # EER, Tei
    EER0 = 4.5
    Tei0 = 14
    if 'EER' in y_gpc_list and 'Tei' in y_gpc_list:
        yr_0_list = [EER0, Tei0]
    elif 'EER' in y_gpc_list and 'Tei' not in y_gpc_list:
        yr_0_list = [EER0]
    elif 'EER' not in y_gpc_list and 'Tei' in y_gpc_list:
        yr_0_list = [EER0]
    else:
        yr_0_list = []
    # 控制指令u初始值
    # Teo, Few, Fcw, Fca
    Teo0 = 8
    Few0 = 1435
    Fcw0 = 1675
    Fca0 = 200
    u_0_list = [Teo0, Few0, Fcw0, Fca0]
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
    if 'EER' in y_gpc_list and 'Tei' in y_gpc_list:
        yr_list = [yr_EER_list, yr_Tei_list]
    elif 'EER' in y_gpc_list and 'Tei' not in y_gpc_list:
        yr_list = [yr_EER_list]
    elif 'EER' not in y_gpc_list and 'Tei' in y_gpc_list:
        yr_list = [yr_Tei_list]
    else:
        yr_list = []
    # 控制量限制
    du_limit_list = [1, 50, 50, 50]
    u_limit_list = [[6, 15], [350, 3500], [450, 4200], [30, 300]]

    # MMGPC内置系统动态模型
    ans_model = model_fmu_dynamics()
    Q_model_list = ans_model[0]
    if 'EER' in y_gpc_list and 'Tei' in y_gpc_list:
        model_list = ans_model[1]
    elif 'EER' in y_gpc_list and 'Tei' not in y_gpc_list:
        model_list = ans_model[2]
    elif 'EER' not in y_gpc_list and 'Tei' in y_gpc_list:
        model_list = ans_model[3]
    else:
        model_list = []
    Np_list = ans_model[4]
    Nc_list = ans_model[5]
    if 'EER' in y_gpc_list and 'Tei' in y_gpc_list:
        r_list = ans_model[6]
        q_list = ans_model[7]
    elif 'EER' in y_gpc_list and 'Tei' not in y_gpc_list:
        r_list = ans_model[8]
        q_list = ans_model[9]
    elif 'EER' not in y_gpc_list and 'Tei' in y_gpc_list:
        r_list = ans_model[10]
        q_list = ans_model[11]
    else:
        r_list = []
        q_list = []
    # 用于测试的plant_model
    ans_plant = plant_fmu_dynamics()
    Q_plant_list = ans_plant[0]
    if 'EER' in y_gpc_list and 'Tei' in y_gpc_list:
        plant_list = ans_plant[1]
    elif 'EER' in y_gpc_list and 'Tei' not in y_gpc_list:
        plant_list = ans_plant[2]
    elif 'EER' not in y_gpc_list and 'Tei' in y_gpc_list:
        plant_list = ans_plant[3]
    else:
        plant_list = []

    # mmgpc仿真参数设置
    # 将初始化的控制器参数数据保存下来的路径
    file_path_init = './model_data/GPC_data'
    # 多模型权值系数的递推计算收敛系数
    if 'EER' in y_gpc_list and 'Tei' in y_gpc_list:
        s_list = [s_EER, s_Tei]
    elif 'EER' in y_gpc_list and 'Tei' not in y_gpc_list:
        s_list = [s_EER]
    elif 'EER' not in y_gpc_list and 'Tei' in y_gpc_list:
        s_list = [s_Tei]
    else:
        s_list = []
    # 计算隶属度函数
    if mmgpc_mode == "ms" and simulate_mode == 'mmgpc':
        ms_list = calculate_membership(Q_plant_list[plant_index], Q_model_list, ms_mode)
    else:
        ms_list = []

    # 控制器仿真
    # smgpc
    if simulate_mode == 'smgpc':
        smgpc(L, Ts, Np_list[model_index], Nc_list[model_index], model_list[model_index], r_list[model_index],
              q_list[model_index], yr_list, yr_0_list, u_0_list, du_limit_list, u_limit_list, True)
    elif simulate_mode == 'mmgpc':
        mmgpc(L, Ts, Np_list, Nc_list, s_list, V, plant_list[plant_index], model_list, r_list, q_list, yr_list,
              yr_0_list, u_0_list, du_limit_list, u_limit_list, file_path_init, save_data_init, ms_list, mmgpc_mode,
              plot_set, model_plot_set)

