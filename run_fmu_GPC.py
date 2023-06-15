from GPC_universal import *
from model_fmu_dynamics import *

if __name__ == "__main__":
    L = 10 * 3600
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
    # 系统动态模型
    ans_model = model_fmu_dynamics()
    model_list = ans_model[1]
    Np_list = ans_model[3]
    Nc_list = ans_model[4]
    r_list = ans_model[5]
    q_list = ans_model[6]
    index = 1
    # smgpc
    smgpc(L, Ts, Np_list[index], Nc_list[index], model_list[index], r_list[index], q_list[index],
          yr_list, yr_0_list, u_0_list, du_limit_list, u_limit_list, True)
    # # mmgpc
    # # s_list: 多模型权值系数的递推计算收敛系数，列表
    # s_list = [1000]
    # # V: 一个非常小的正实数，保证所有子控制器将来可用
    # V = 0.0001
    # # 将初始化的控制器参数数据保存下来的路径
    # file_path_init = './model_data/GPC_data'
    # plant_list = model_list[index]
    # save_data_init = True
    # plot_set = True
    # model_plot_set = True
    # mmgpc(L, Ts, Np_list, Nc_list, s_list, V, plant_list, model_list, r_list, q_list, yr_list, yr_0_list,
    #       u_0_list, du_limit_list, u_limit_list, file_path_init, save_data_init, plot_set, model_plot_set)

