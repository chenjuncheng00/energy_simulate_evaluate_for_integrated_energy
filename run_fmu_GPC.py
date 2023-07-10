from GPC_universal import *
from model_fmu_dynamics import model_fmu_dynamics, plant_fmu_dynamics

if __name__ == "__main__":
    L = 20 * 3600
    Ts = 10 * 60
    # 仿真次数
    n = int(L / Ts)
    # 输出目标值yr的初始值
    # EER, Tei
    EER0 = 4.5
    Tei0 = 14
    yr_0_list = [EER0, Tei0]
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
            yr_EER_list.append(EER0 + 0.4)
            yr_Tei_list.append(Tei0 + 0.5)
    yr_list = [yr_EER_list, yr_Tei_list]
    # 控制量限制
    du_limit_list = [1, 50, 50, 50]
    u_limit_list = [[6, 15], [350, 3500], [450, 4200], [30, 300]]

    # MMGPC内置系统动态模型
    ans_model = model_fmu_dynamics()
    model_list = ans_model[0]
    Np_list = ans_model[3]
    Nc_list = ans_model[4]
    r_list = ans_model[5]
    q_list = ans_model[6]
    Q_model_list = ans_model[7]
    # 用于测试的plant_model
    ans_plant = plant_fmu_dynamics()
    plant_list = ans_plant[0]
    Q_plant_list = ans_plant[3]

    # # smgpc
    # model_index = 4
    # smgpc(L, Ts, Np_list[model_index], Nc_list[model_index], model_list[model_index], r_list[model_index],
    #       q_list[model_index], yr_list, yr_0_list, u_0_list, du_limit_list, u_limit_list, True)

    # mmgpc
    plant_index = 7
    s_list = [1, 1000]
    mmgpc_mode = "switch"
    # V: 一个非常小的正实数，保证所有子控制器将来可用
    V = 0.0001
    # 计算隶属度函数
    Q_switch = (Q_model_list[1] - Q_model_list[0]) / 4
    ms_list = calculate_membership(Q_plant_list[plant_index], Q_switch, Q_model_list)
    # 将初始化的控制器参数数据保存下来的路径
    file_path_init = './model_data/GPC_data'
    save_data_init = False
    plot_set = True
    model_plot_set = False
    mmgpc(L, Ts, Np_list, Nc_list, s_list, V, plant_list[plant_index], model_list, r_list, q_list, yr_list, yr_0_list,
          u_0_list, du_limit_list, u_limit_list, file_path_init, save_data_init, ms_list, mmgpc_mode, plot_set,
          model_plot_set)

