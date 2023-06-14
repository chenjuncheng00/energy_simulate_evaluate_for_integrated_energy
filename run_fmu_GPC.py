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
    du_limit_list = [1, 300, 300, 50]
    u_limit_list = [[6, 15], [350, 3500], [450, 4200], [30, 300]]
    # 系统动态模型
    ans_model = model_fmu_dynamics()
    model_list = ans_model[0]
    Np_list = ans_model[3]
    Nc_list = ans_model[4]
    r_list = ans_model[5]
    q_list = ans_model[6]
    index = 0
    smgpc(L, Ts, Np_list[index], Nc_list[index], model_list[index], r_list[index], q_list[index],
          yr_list, yr_0_list, u_0_list, du_limit_list, u_limit_list, True)

