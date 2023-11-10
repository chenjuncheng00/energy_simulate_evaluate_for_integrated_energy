from gap_metric import *
from model_fmu_dynamics import model_dynamics_complex_chiller, model_dynamics_chiller_ashp

if __name__ == "__main__":
    # model_mode: 0:仅冷水机；1:冷水机+空气源热泵
    model_mode = 1
    y_gpc_list = ["EER", "Tei"]
    path_matlab = "/Users/chenjuncheng/Documents/Machine_Learning_Development/system_identification/gap_metric"
    if model_mode == 0:
        ans_model = model_dynamics_complex_chiller()
    elif model_mode == 1:
        ans_model = model_dynamics_chiller_ashp()
    else:
        ans_model = None
    if "EER" in y_gpc_list and "Tei" in y_gpc_list:
        model_list = ans_model[1]
    elif "EER" in y_gpc_list and "Tei" not in y_gpc_list:
        model_list = ans_model[2]
    elif "EER" not in y_gpc_list and "Tei" in y_gpc_list:
        model_list = ans_model[3]
    else:
        model_list = []
    calculate_gap_metric(path_matlab, model_list)
