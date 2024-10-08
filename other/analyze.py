import os
import re
from datetime import datetime

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

def process_log_files(input_directory):
    """
    处理指定目录中的所有日志文件，并将结果写入到输入目录中的分析日志文件中
    :param input_directory: 包含日志文件的目录路径
    """
    # 获取输入目录的最后一层名称
    dir_name = os.path.basename(os.path.normpath(input_directory))
    output_file = os.path.join(input_directory, f"{dir_name}_analyze.log")

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
    # 直接指定输入目录路径
    # 需要分析的日志路径
    input_directory = "/Users/duling/Desktop/code/Geo_All2All/output/total_result/dp_group"  
    process_log_files(input_directory)