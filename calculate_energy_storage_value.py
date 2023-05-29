from algorithm_code.read_write_data import *

def generate_Q_list(file_fmu_time, start_time, Q_time_list, Q_user_list, n_calculate_hour):
    """
    获取从当前时刻，向后24个计算间隔的负荷数据列表
    Args:
        file_fmu_time:
        start_time:
        Q_time_list:
        Q_user_list:
        n_calculate_hour:

    Returns:

    """
    # 获取time
    time_now = read_txt_data(file_fmu_time)[0]
    # Q_time_list的时间间隔是1800秒
    if int((time_now - start_time) / 1800) - (time_now - start_time) / 1800 < 0:
        time_now = int((time_now - start_time) / 1800) * 1800 + 1800 + start_time
    else:
        time_now = int((time_now - start_time) / 1800) * 1800 + start_time
    index_now = Q_time_list.index(time_now)
    time_step = 3600 / n_calculate_hour
    index_step = int(time_step / 1800)
    result_Q_list = []
    for i in range(24):
        Q_tmp = Q_user_list[index_now + i * index_step]
        result_Q_list.append(Q_tmp)
    return result_Q_list


def generate_time_name_list(time_name_list):
    """
    将传入的长度24的时间名称列表根据时间平移滚动，形成新的列表
    Args:
        time_name_list:

    Returns:

    """
    time_name_23 = time_name_list[23]
    for i in range(23):
        time_name_list[-i + 23] = time_name_list[-i + 22]
    time_name_list[0] = time_name_23
    return time_name_list