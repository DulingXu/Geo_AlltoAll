import os
import re
from datetime import datetime
import subprocess

# use to parse the log file of normal group
def parse_log_file(log_file):
    """
    解析单个日志文件，提取执行时间和 Makespan 结果
    :param log_file: 日志文件的路径
    :return: (文件名, 执行时间（毫秒）, Makespan 结果) 或 None 如果文件格式不正确
    """
    start_time, end_time, makespan = None, None, None

    with open(log_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        

    # 提取文件开始和结束的时间戳
    for line in lines:
        match = re.search(r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{3})', line)
        if match:
            if not start_time:
                start_time = match.group(1)  # 获取开始时间
            end_time = match.group(1)  # 最后一个时间为结束时间

        # 提取 Makespan 结果
        if 'Makespan 结果' in line:
            makespan_match = re.search(r'Makespan 结果: ([\d.]+)', line)
            if makespan_match:
                makespan = makespan_match.group(1)

    # 计算执行时间并转换为毫秒
    if start_time and end_time and makespan:
        start_dt = datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S,%f")
        end_dt = datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S,%f")
        execution_time = (end_dt - start_dt).total_seconds() * 1000  # 保留毫秒级差异
        return os.path.basename(log_file), execution_time, makespan
    else:
        return None

def process_log_files(directories, output_directory):
    """
    处理指定目录中的所有日志文件，并将结果写入到指定的输出目录中
    :param directories: 包含日志文件的目录路径列表
    :param output_directory: 分析结果的输出目录
    """
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    for input_directory in directories:
        # 获取输入目录的最后一层名称
        dir_name = os.path.basename(os.path.normpath(input_directory))
        output_file = os.path.join(output_directory, f"{dir_name}_analyze.log")

        with open(output_file, 'w', encoding='utf-8') as out_file:
            out_file.write("文件名, 执行时间（毫秒）, Makespan 结果\n")

            for log_file in os.listdir(input_directory):
                if log_file.endswith(".log"):  # 只处理 .log 类型文件
                    log_path = os.path.join(input_directory, log_file)
                    result = parse_log_file(log_path)

                    if result:
                        filename, exec_time, makespan = result
                        out_file.write(f"{filename}, {exec_time:.3f}, {makespan}\n")
                    else:
                        print(f"无法解析文件: {log_file}")

        print(f"日志处理完成，结果已保存到: {output_file}")

if __name__ == "__main__":
    # 指定多个输入目录路径
    input_directories = [
        "/Users/duling/Desktop/code/Geo_All2All/output/total_result/conflict/0.1/rule_group_conflict_0.1",
        "/Users/duling/Desktop/code/Geo_All2All/output/total_result/conflict/0.2/rule_group_conflict_0.2",
        "/Users/duling/Desktop/code/Geo_All2All/output/total_result/conflict/0.3/rule_group_conflict_0.3",
        "/Users/duling/Desktop/code/Geo_All2All/output/total_result/conflict/0.4/rule_group_conflict_0.4",
        "/Users/duling/Desktop/code/Geo_All2All/output/total_result/conflict/0.5/rule_group_conflict_0.5",
        # 添加更多目录路径
    ]

    # 指定输出目录路径
    output_directory = "/Users/duling/Desktop/code/Geo_All2All/output/total_result/conflict/key_result"

    process_log_files(input_directories, output_directory)
