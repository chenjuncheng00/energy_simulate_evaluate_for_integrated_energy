import time, datetime
from algorithm_code.read_write_data import *
from run_chiller import run_chiller
from run_air_source_heat_pump import run_air_source_heat_pump

def run_simulate_evaluate(Q_total):

    # cfg文件路径
    cfg_path_equipment = "./config/equipment_config.cfg"
    cfg_path_public = "./config/public_config.cfg"
    # 设备类型名称(air_conditioner,air_source_heat_pump等)，相对路径
    chiller_equipment_type_path = ["chiller", "../optimal_control_algorithm_for_cooling_season"]
    ashp_equipment_type_path = ["air_source_heat_pump", "../optimal_control_algorithm_for_cooling_season"]
    storage_equipment_type_path = ["energy_storage_equipment", "../optimal_control_algorithm_for_cooling_season"]

    while True:
        print("系统运行...")
        # 执行主程序
        now_minute = datetime.datetime.now().minute
        # 设置的算法启动的分钟，返回的是一个列表
        minute_set = read_cfg_data(cfg_path_public, "算法自动运行的时间", "minute_set", 1)
        # 每小时计算次数
        n_calculate_hour = 0
        for i in range(len(minute_set)):
            if 0 <= minute_set[i] <= 60:
                n_calculate_hour += 1
        if now_minute == minute_set[0] or now_minute == minute_set[1] or now_minute == minute_set[2] or \
                now_minute == minute_set[3] or now_minute == minute_set[4] or now_minute == minute_set[5] \
                or minute_set[6] == 99:
            # 冷水机总负荷：包括蓄冷水罐蓄冷功率
            chiller_Q = 10000
            # 先优化一次冷水机，不进行控制，用于获取阀门开启比例，用于蓄冷水罐和冷却塔直接供冷计算
            ans_chiller = run_chiller(chiller_Q, n_calculate_hour, chiller_equipment_type_path,
                                      cfg_path_equipment, cfg_path_public, True)
            chiller_chilled_value_open = ans_chiller[2]
            chiller_cooling_value_open = ans_chiller[3]
            chiller_tower_value_open = ans_chiller[4]
            # 冷水机优化和控制
            run_chiller(chiller_Q, n_calculate_hour, chiller_equipment_type_path, cfg_path_equipment,
                        cfg_path_public, False)
            # 空气源热泵优化和控制
            air_source_heat_pump_Q = Q_total - chiller_Q
            run_air_source_heat_pump(air_source_heat_pump_Q, n_calculate_hour, ashp_equipment_type_path,
                                     cfg_path_equipment, cfg_path_public, False)
        else:
            print("正在等待程序运行………………，sleep_time2")
            time.sleep(read_cfg_data(cfg_path_public, "算法运行后休眠时间", "sleep_time2", 1))


if __name__ == "__main__":
    run_simulate_evaluate(15000)