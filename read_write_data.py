import os, configparser
from equipment_txt_path import get_station_equipment_alarm_status_txt_path, get_station_equipment_fault_status_txt_path,\
                               get_station_equipment_remote_status_txt_path, get_station_equipment_repair_status_txt_path
"""
算法实现所需的基本的读写数据方法
"""

def set_equipment_DI_AI(file_DI_AI, index_list, DI_AI_list, column_index=0, return_status=1):
    """
    向txt文件写入数据：修改某一台设备的(开关状态、故障状态、报警状态、检修状态、就地状态、频率值、温度值、开度值)

    Args:
        file_DI_AI:[string]，储存设备(开关状态、故障状态、报警状态、检修状态、就地状态、频率值、温度值、开度值)的txt文件路径
        index_list:[list]，设备的编号(从0开始)列表
        DI_AI_list: [list][int][float],设备状态列表(1：设备开启，0：设备关闭；
                                                  1：没有故障，0：故障状态；
                                                  1：没有报警，0：没有报警；
                                                  1：没有检修，0：检修状态；
                                                  1：远方状态，0：就地状态;
                                                  实际频率值；实际温度值；实际开度值)
        column_index: [int]，需要读取的列编号
        return_status: 返回的数据类型(0：float，1：int，2：string)

    Returns:
        修改某一台设备的(开关、故障、报警、检修、就地)状态
    """
    if column_index == 0:
        # 读取目前的设备状态
        equipment_status = read_txt_data(file_DI_AI, return_status=return_status)
        # 修改具体某一个设备的状态
        for i in range(len(index_list)):
            index = index_list[i]
            if isinstance(DI_AI_list, list) == True:
                equipment_status[index] = DI_AI_list[i]
            else:
                equipment_status[index] = DI_AI_list
        # 重新写入txt文件
        write_txt_data(file_DI_AI, equipment_status)
    else:
        # 判断是否需要读取设备编号
        result_list = []
        # 读取设备ID
        equipment_ID = read_txt_data(file_DI_AI, return_status=return_status)
        # 读取目前的设备状态
        equipment_status = read_txt_data(file_DI_AI, return_status=return_status, column_index=column_index)
        # 修改具体某一个设备的状态
        for index_tmp in index_list: # index_tmp:设备编号
            i = index_list.index(index_tmp)  # i：设备编号所对应的列表中的序号
            for ID_tmp in equipment_ID: # ID：设备编号
                j = equipment_ID.index(ID_tmp)  # j：设备编号所对应的列表中的序号
                if ID_tmp == index_tmp:
                    if isinstance(DI_AI_list, list) == True:
                        equipment_status[j] = DI_AI_list[i]
                        break
                    else:
                        equipment_status[j] = DI_AI_list
                        break
        # 拼接列表
        for k in range(len(equipment_ID)):
            result_tmp = str(equipment_ID[k]) + "\t" + str(equipment_status[k])
            result_list.append(result_tmp)
        # 重新写入txt文件
        write_txt_data(file_DI_AI, result_list)


def get_equipment_status(file_fault, file_alarm, file_repair, file_remote):
    """
    从txt文件读取数据：设备是否存在故障、报警、检修、就地状态

    Args:
        file_fault:[string]，储存设备故障状态的txt文件位置
        file_alarm:[string]，储存设备报警状态的txt文件位置
        file_repair:[string]，储存设备维修状态的txt文件位置
        file_remote:[string]，储存设备远方状态的txt文件位置

    Returns:
        返回设备是否存在故障、报警、检修、就地状态列表
    """
    # 1：没有故障，0：故障状态
    fault_list = read_txt_data(file_fault, return_status=1)
    # 1：没有报警，0：没有报警
    alarm_list = read_txt_data(file_alarm, return_status=1)
    # 1：没有检修，0：检修状态
    repair_list = read_txt_data(file_repair, return_status=1)
    # 1：远方状态，0：就地状态
    remote_list = read_txt_data(file_remote, return_status=1)
    # 计算设备的综合状态，故障、报警、检修、远方状态中任何一个有问题，都显示有问题，取交集
    # 1：设备一切正常，0：设备存在问题
    equipment_status = []
    for i in range(len(fault_list)):
        tmp = fault_list[i] * alarm_list[i] * repair_list[i] * remote_list[i]
        equipment_status.append(tmp)
    # 返回结果
    return equipment_status


def judge_equipment_controllable_status(equipment_type_path, equipment_name_list, start_index_list=None,
                                        end_index_list=None):
    """
    判断可以被控制的设备数量最大值、判断设备处于的可控/不可控状态的设备编号列表

    Args:
        equipment_type_path: [string]，[list]，设备类型名称(air_conditioner,air_source_heat_pump等)，相对路径
        equipment_name_list: [list]，各个设备的类型名称，列表
        start_index_list:[list]，不同类型设备在列表中的开始编号(包含)列表，与equipment_name_list一一对应
        end_index_list:[list]，不同类型设备在列表中的结束编号(包含)列表，与equipment_name_list一一对应

    Returns:

    """
    # 设备类型
    equipment_type = equipment_type_path[0]
    # 储存记录的txt文件路径(用于区分是否是上层目录)
    txt_path = equipment_type_path[1]
    # 获取各种txt文件路径
    ans_alarm_status_txt_path = get_station_equipment_alarm_status_txt_path(equipment_type, txt_path)
    file_alarm_main_equipment = ans_alarm_status_txt_path[0]
    file_alarm_chilled_pump = ans_alarm_status_txt_path[1]
    file_alarm_chilled_pump_secondary = ans_alarm_status_txt_path[2]
    file_alarm_cooling_pump = ans_alarm_status_txt_path[3]
    file_alarm_cooling_tower = ans_alarm_status_txt_path[4]
    file_alarm_chilled_value = ans_alarm_status_txt_path[5]
    file_alarm_cooling_value = ans_alarm_status_txt_path[6]
    file_alarm_tower_value = ans_alarm_status_txt_path[7]
    ans_fault_status_txt_path = get_station_equipment_fault_status_txt_path(equipment_type, txt_path)
    file_fault_main_equipment = ans_fault_status_txt_path[0]
    file_fault_chilled_pump = ans_fault_status_txt_path[1]
    file_fault_chilled_pump_secondary = ans_fault_status_txt_path[2]
    file_fault_cooling_pump = ans_fault_status_txt_path[3]
    file_fault_cooling_tower = ans_fault_status_txt_path[4]
    file_fault_chilled_value = ans_fault_status_txt_path[5]
    file_fault_cooling_value = ans_fault_status_txt_path[6]
    file_fault_tower_value = ans_fault_status_txt_path[7]
    ans_remote_status_txt_path = get_station_equipment_remote_status_txt_path(equipment_type, txt_path)
    file_remote_main_equipment = ans_remote_status_txt_path[0]
    file_remote_chilled_pump = ans_remote_status_txt_path[1]
    file_remote_chilled_pump_secondary = ans_remote_status_txt_path[2]
    file_remote_cooling_pump = ans_remote_status_txt_path[3]
    file_remote_cooling_tower = ans_remote_status_txt_path[4]
    file_remote_chilled_value = ans_remote_status_txt_path[5]
    file_remote_cooling_value = ans_remote_status_txt_path[6]
    file_remote_tower_value = ans_remote_status_txt_path[7]
    ans_repair_status_txt_path = get_station_equipment_repair_status_txt_path(equipment_type, txt_path)
    file_repair_main_equipment = ans_repair_status_txt_path[0]
    file_repair_chilled_pump = ans_repair_status_txt_path[1]
    file_repair_chilled_pump_secondary = ans_repair_status_txt_path[2]
    file_repair_cooling_pump = ans_repair_status_txt_path[3]
    file_repair_cooling_tower = ans_repair_status_txt_path[4]
    file_repair_chilled_value = ans_repair_status_txt_path[5]
    file_repair_cooling_value = ans_repair_status_txt_path[6]
    file_repair_tower_value = ans_repair_status_txt_path[7]
    # 列表，储存最终结果
    n_max_list = []
    controllable_index_list = []
    uncontrollable_index_list = []
    # 计算
    for i in range(len(equipment_name_list)):
        equipment_name = equipment_name_list[i]
        # 储存设备的故障、维修、告警、远方状态txt文件路径
        if equipment_name == "air_conditioner" or equipment_name == "internal_combustion_engine" or \
                (equipment_type == "energy_storage_equipment" and equipment_name == "chilled_pump"):
            # 主设备
            file_fault_equipment = file_fault_main_equipment
            file_alarm_equipment = file_alarm_main_equipment
            file_repair_equipment = file_repair_main_equipment
            file_remote_equipment = file_remote_main_equipment
        elif equipment_name == "chilled_pump":
            file_fault_equipment = file_fault_chilled_pump
            file_alarm_equipment = file_alarm_chilled_pump
            file_repair_equipment = file_repair_chilled_pump
            file_remote_equipment = file_remote_chilled_pump
        elif equipment_name == "chilled_pump_secondary":
            file_fault_equipment = file_fault_chilled_pump_secondary
            file_alarm_equipment = file_alarm_chilled_pump_secondary
            file_repair_equipment = file_repair_chilled_pump_secondary
            file_remote_equipment = file_remote_chilled_pump_secondary
        elif equipment_name == "cooling_pump":
            file_fault_equipment = file_fault_cooling_pump
            file_alarm_equipment = file_alarm_cooling_pump
            file_repair_equipment = file_repair_cooling_pump
            file_remote_equipment = file_remote_cooling_pump
        elif equipment_name == "cooling_tower":
            file_fault_equipment = file_fault_cooling_tower
            file_alarm_equipment = file_alarm_cooling_tower
            file_repair_equipment = file_repair_cooling_tower
            file_remote_equipment = file_remote_cooling_tower
        else:
            file_fault_equipment = None
            file_alarm_equipment = None
            file_repair_equipment = None
            file_remote_equipment = None
        # 设备的综合状态
        equipment_status = get_equipment_status(file_fault_equipment, file_alarm_equipment,
                                                file_repair_equipment, file_remote_equipment)
        equipment_status_segment = []
        if start_index_list != None and end_index_list != None:
            n_max_equipment = []
            for j in range(len(start_index_list[i])):
                equipment_status_tmp = equipment_status[start_index_list[i][j]:(end_index_list[i][j] + 1)].copy()
                equipment_status_segment.append(equipment_status_tmp)
                n_max_equipment_tmp = sum(equipment_status_tmp)
                n_max_equipment.append(n_max_equipment_tmp)
        else:
            n_max_equipment = sum(equipment_status)
        # 如果是设备本体，则需要同时考虑冷冻阀门、冷却阀门的状态
        if (equipment_type == "chiller" or equipment_type == "water_source_heat_pump" or
            equipment_type == "lithium_bromide") and equipment_name == "air_conditioner":
            # 冷冻阀门
            chilled_value_status = get_equipment_status(file_fault_chilled_value, file_alarm_chilled_value,
                                                        file_repair_chilled_value, file_remote_chilled_value)
            # 冷却阀门
            cooling_value_status = get_equipment_status(file_fault_cooling_value, file_alarm_cooling_value,
                                                        file_repair_cooling_value, file_remote_cooling_value)
            # 计算阀门综合状态
            value_status = []
            for j in range(len(equipment_status)):
                tmp = chilled_value_status[j] * cooling_value_status[j]
                value_status.append(tmp)
            value_status_segment = []
            if start_index_list != None and end_index_list != None:
                for j in range(len(start_index_list[i])):
                    value_status_tmp = value_status[start_index_list[i][j]:(end_index_list[i][j] + 1)].copy()
                    value_status_segment.append(value_status_tmp)
            # 同时考虑冷冻阀门和冷却阀门
            tmp_controllable_index_list = []
            tmp_uncontrollable_index_list = []
            for j in range(len(equipment_status)):
                if equipment_status[j] == 1 and value_status[j] == 1:
                    tmp_controllable_index_list.append(j)
                else:
                    tmp_uncontrollable_index_list.append(j)
            if start_index_list != None and end_index_list != None:
                n_max = []
                for j in range(len(start_index_list[i])):
                    n_max_segment_tmp = 0
                    for k in range(len(equipment_status_segment[j])):
                        if equipment_status_segment[j][k] == 1 and value_status_segment[j][k] == 1:
                            n_max_segment_tmp += 1
                    n_max.append(n_max_segment_tmp)
            else:
                n_max = 0
                for j in range(len(equipment_status)):
                    if equipment_status[j] == 1 and value_status[j] == 1:
                        n_max += 1
        elif (equipment_type == "air_source_heat_pump" and equipment_name == "air_conditioner") or \
                (equipment_type == "energy_storage_equipment" and equipment_name == "chilled_pump"):
            # 只有冷冻阀门
            chilled_value_status = get_equipment_status(file_fault_chilled_value, file_alarm_chilled_value,
                                                        file_repair_chilled_value, file_remote_chilled_value)
            chilled_value_status_segment = []
            if start_index_list != None and end_index_list != None:
                for j in range(len(start_index_list[i])):
                    chilled_value_status_tmp = chilled_value_status[start_index_list[i][j]:(end_index_list[i][j] + 1)].copy()
                    chilled_value_status_segment.append(chilled_value_status_tmp)
            # 仅同时考虑冷冻阀门
            tmp_controllable_index_list = []
            tmp_uncontrollable_index_list = []
            for j in range(len(equipment_status)):
                if equipment_status[j] == 1 and chilled_value_status[j] == 1:
                    tmp_controllable_index_list.append(j)
                else:
                    tmp_uncontrollable_index_list.append(j)
            if start_index_list != None and end_index_list != None:
                n_max = []
                for j in range(len(start_index_list[i])):
                    n_max_segment_tmp = 0
                    for k in range(len(equipment_status_segment[j])):
                        if equipment_status_segment[j][k] == 1 and chilled_value_status_segment[j][k] == 1:
                            n_max_segment_tmp += 1
                    n_max.append(n_max_segment_tmp)
            else:
                n_max = 0
                for j in range(len(equipment_status)):
                    if equipment_status[j] == 1 and chilled_value_status[j] == 1:
                        n_max += 1
        elif equipment_name == "cooling_tower":
            # 考虑冷却塔阀门
            tower_value_status = get_equipment_status(file_fault_tower_value, file_alarm_tower_value,
                                                      file_repair_tower_value, file_remote_tower_value)
            # 同时考虑冷却塔阀门
            tmp_controllable_index_list = []
            tmp_uncontrollable_index_list = []
            for j in range(len(equipment_status)):
                if equipment_status[j] == 1 and tower_value_status[j] == 1:
                    tmp_controllable_index_list.append(j)
                else:
                    tmp_uncontrollable_index_list.append(j)
            tower_value_status_segment = []
            if start_index_list != None and end_index_list != None:
                for j in range(len(start_index_list[i])):
                    tower_value_status_tmp = tower_value_status[start_index_list[i][j]:(end_index_list[i][j] + 1)].copy()
                    tower_value_status_segment.append(tower_value_status_tmp)
            if start_index_list != None and end_index_list != None:
                n_max = []
                for j in range(len(start_index_list[i])):
                    n_max_segment_tmp = 0
                    for k in range(len(equipment_status_segment[j])):
                        if equipment_status_segment[j][k] == 1 and tower_value_status_segment[j][k] == 1:
                            n_max_segment_tmp += 1
                    n_max.append(n_max_segment_tmp)
            else:
                n_max = 0
                for j in range(len(equipment_status)):
                    if equipment_status[j] == 1 and tower_value_status[j] == 1:
                        n_max += 1
        else:
            n_max = n_max_equipment
            # 不需要考虑阀门
            tmp_controllable_index_list = []
            tmp_uncontrollable_index_list = []
            for j in range(len(equipment_status)):
                if equipment_status[j] == 1:
                    tmp_controllable_index_list.append(j)
                else:
                    tmp_uncontrollable_index_list.append(j)
        # 记录结果
        n_max_list.append(n_max)
        controllable_index_list.append(tmp_controllable_index_list)
        uncontrollable_index_list.append(tmp_uncontrollable_index_list)
    # 返回结果
    return n_max_list, controllable_index_list, uncontrollable_index_list


def judge_redundantly_opened_valve(file_open_status_main_equipment, file_open_status_cooling_tower,
                                   file_open_status_chilled_value, file_open_status_cooling_value,
                                   file_open_status_tower_value):
    """
    判断多余开启的阀门编号：主设备没有开，但是阀门开启了；返回编号列表

    Args:
        file_open_status_main_equipment:[string]，储存主设备开关状态的txt文件的路径
        file_open_status_cooling_tower:[string]，储存冷却塔开关状态的txt文件的路径
        file_open_status_chilled_value:[string]，储存冷冻阀门开关状态的txt文件的路径
        file_open_status_cooling_value:[string]，储存冷却阀门开关状态的txt文件的路径
        file_open_status_tower_value:[string]，储存冷却塔阀门开关状态的txt文件的路径

    Returns:

    """
    # 获取设备的开关状态列表
    if file_open_status_main_equipment != None:
        open_status_main_equipment = read_txt_data(file_open_status_main_equipment, return_status=1)
    else:
        open_status_main_equipment = []
    if file_open_status_cooling_tower != None:
        open_status_cooling_tower = read_txt_data(file_open_status_cooling_tower, return_status=1)
    else:
        open_status_cooling_tower = []
    if file_open_status_chilled_value != None:
        open_status_chilled_value = read_txt_data(file_open_status_chilled_value, return_status=1)
    else:
        open_status_chilled_value = []
    if file_open_status_cooling_value != None:
        open_status_cooling_value = read_txt_data(file_open_status_cooling_value, return_status=1)
    else:
        open_status_cooling_value = []
    if file_open_status_tower_value != None:
        open_status_tower_value = read_txt_data(file_open_status_tower_value, return_status=1)
    else:
        open_status_tower_value = []
    # 多余开启的阀门编号列表，也是需要被单独关闭的设备编号列表
    chilled_value_redundantly_list = []
    cooling_value_redundantly_list = []
    tower_value_redundantly_list = []
    for i in range(len(open_status_main_equipment)):
        if open_status_main_equipment[i] == 0 and open_status_chilled_value[i] == 1:
            chilled_value_redundantly_list.append(i)
        if file_open_status_cooling_value != None:
            if open_status_main_equipment[i] == 0 and open_status_cooling_value[i] == 1:
                cooling_value_redundantly_list.append(i)
    for i in range(len(open_status_cooling_tower)):
        if open_status_cooling_tower[i] == 0 and open_status_tower_value[i] == 1:
            tower_value_redundantly_list.append(i)
    # 返回结果
    return chilled_value_redundantly_list, cooling_value_redundantly_list, tower_value_redundantly_list


def clear_all_txt_data(root_path):
    """
    向txt文件写入数据：清空指定路径下的所有txt文件

    Args:
        root_path:[string]，开始遍历的根目录路径

    Returns:

    """
    path_dir = os.listdir(root_path)
    for dir in path_dir:
        # 所有的文件路径
        txt_file = []
        # 将文件名加入到当前文件路径后面
        new_dir = os.path.join(root_path, dir)
        # 如果是文件
        if os.path.isfile(new_dir):
            # 如果文件是".txt"后缀的
            if os.path.splitext(new_dir)[1] == ".txt":
                txt_file.append(new_dir)
        # 如果是路径
        elif os.path.isdir(new_dir):
            # 递归
            clear_all_txt_data(new_dir)
        # 清空路径下的所有txt文件
        if len(txt_file) > 0:
            for eachfile in txt_file:
                # 文件设置为写入状态
                f_w = open(eachfile, "w")
                # 清空TXT文件全部内容
                f_w.truncate(0)


def write_initialize_txt_data(root_path, txt_data_list, file_name_txt):
    """
    向txt文件写入数据：根据设备的装机数量，初始化设备的"equipment_status"、"operation_hours"、"real_value"

    Args:
        root_path:[string]，开始遍历的根目录路径
        txt_data_list:[list]，需要写入的参数列表
        file_name_txt:[string]，txt文件名

    Returns:

    """
    path_dir = os.listdir(root_path)
    for dir in path_dir:
        # 所有的文件路径和文件名
        txt_file_path = []
        txt_file_name = []
        # 将文件名加入到当前文件路径后面
        new_dir = os.path.join(root_path, dir)
        # 如果是文件
        if os.path.isfile(new_dir):
            # 如果文件是".txt"后缀的
            if os.path.splitext(new_dir)[1] == ".txt":
                # 文件路径加入列表
                txt_file_path.append(new_dir)
                # 获取txt文件名
                txt_file_name.append(new_dir.strip().split("/")[-1])
        # 如果是路径
        elif os.path.isdir(new_dir):
            # 递归
            write_initialize_txt_data(new_dir, txt_data_list, file_name_txt)
        # 写入数据
        if len(txt_file_path) > 0:
            for i in range(len(txt_file_path)):
                file_path_tmp = txt_file_path[i]
                file_name_tmp = txt_file_name[i]
                if file_name_tmp == file_name_txt:
                    write_txt_data(file_path_tmp, txt_data_list)


def write_txt_data(file_txt_data, txt_data_list, write_model=0):
    """
    向txt文件写入数据

    Args:
        file_txt_data:[string]，文件路径
        txt_data_list:[list]，需要写入的参数列表
        write_model: [int]，0：清空原有内容，重新写入新内容；1：不清空原有内容，在原有内容后追加新内容；

    Returns:

    """
    if write_model == 0:
        # 文件设置为写入状态
        f_w = open(file_txt_data, "w")
        # 清空TXT文件全部内容
        f_w.truncate(0)
    elif write_model == 1:
        # 文件设置为追加状态
        f_w = open(file_txt_data, "a")
    else:
        f_w = None
    # 写入内容
    for i in range(len(txt_data_list)):
        write = str(txt_data_list[i]) + "\n"
        f_w.writelines(write)
    f_w.close()  # 关闭文件


def read_txt_data(file_txt_data, return_status=0, column_index=0):
    """
    从txt文件读取数据

    Args:
        file_txt_data: [string]，文件路径
        return_status: [int]，返回的数据类型(0：float，1：int，2：string)
        column_index: [int]，需要读取的列编号
    Returns:

    """
    # 设置文件为读取状态
    file_r = open(file_txt_data, "r")
    txt_data = []
    # 数据只有一列
    for line in file_r.readlines():
        temp = line.strip().split("\t")
        # 转为float数据
        if return_status == 0:
            txt_data.append(float(temp[column_index]))
        elif return_status == 1:
            txt_data.append(int(float(temp[column_index])))
        elif return_status == 2:
            txt_data.append(temp[column_index])
    file_r.close()  # 关闭文件
    # 返回一个列表
    ans = txt_data
    # 返回结果
    return ans


def read_cfg_data(file_config, section, key, return_status):
    """
    从cfg文件读取配置数据

    Args:
        file_config:[string]，cfg文件路径
        section:[string]，读取的大类名称
        key:[string]，读取的关键字名称
        return_status: [int]，返回的数据类型(0：float，1：int，2：bool，3：string)

    Returns:

    """
    cfg = configparser.ConfigParser()
    cfg.read(file_config, encoding="utf-8")
    # 读取的结果用"，"区分，变成列表
    cfg_value = cfg.get(section, key).split(",")
    # 判断读取的结果长度
    if len(cfg_value) == 1:
        if return_status == 0:
            ans_cfg = float(cfg_value[0])
        elif return_status == 1:
            ans_cfg = int(float(cfg_value[0]))
        elif return_status == 2:
            ans_cfg = bool(cfg_value[0])
        elif return_status == 3:
            ans_cfg = cfg_value[0]
        else:
            ans_cfg = None
    else:
        # 如果长度不是1，则返回一个列表
        ans_cfg = []
        for i in range(len(cfg_value)):
            if return_status == 0:
                ans_cfg.append(float(cfg_value[i]))
            elif return_status == 1:
                ans_cfg.append(int(float(cfg_value[i])))
            elif return_status == 2:
                ans_cfg = bool(cfg_value[i])
            elif return_status == 3:
                ans_cfg.append(cfg_value[i])
    # 返回结果
    return ans_cfg