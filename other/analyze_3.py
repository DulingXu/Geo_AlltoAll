import os
import time
import re

def get_last_line(file_path):
    """获取文件的最后一行"""
    with open(file_path, 'r') as file:
        lines = file.readlines()
        return lines[-1].strip()

def extract_last_number(line):
    # Use a regular expression to find the makespan value in the line
    match = re.search(r"makespan 的值: ([\d.]+)", line)
    if match:
        return float(match.group(1))
    else:
        print(f"Warning: Could not find makespan value in line: '{line}'")
        return None

def analyze_directory(directory_path):
    """分析目录中的文件并生成日志"""
    print(f"开始分析目录: {directory_path}")
    log_entries = []
    file_paths = [os.path.join(directory_path, f) for f in os.listdir(directory_path) if f.endswith('.log')]
    file_paths.sort(key=os.path.getmtime)  # 按文件修改时间排序

    previous_time = None

    for file_path in file_paths:
        print(f"正在处理文件: {file_path}")
        file_name = os.path.basename(file_path)
        last_line = get_last_line(file_path)
        makespan_result = extract_last_number(last_line)

        current_time = os.path.getmtime(file_path)
        if previous_time is not None:
            execution_time = (current_time - previous_time) * 1000  # 转换为毫秒
        else:
            execution_time = 0.0  # 第一个文件没有前一个文件来计算时间差

        log_entries.append(f"{file_name}, {execution_time:.3f}, {makespan_result}")
        previous_time = current_time

    # 生成日志文件
    log_file_name = os.path.basename(directory_path) + "_analyze.log"
    log_file_path = os.path.join(directory_path, log_file_name)
    with open(log_file_path, 'w') as log_file:
        log_file.write("文件名, 执行时间（毫秒）, Makespan 结果\n")
        for entry in log_entries:
            log_file.write(entry + "\n")

    print(f"分析完成，日志已存储到: {log_file_path}")

if __name__ == "__main__":
    directory_path = "/Users/duling/Desktop/code/Geo_All2All/output/total_result/no_group_just_max_200_1_latency"
    analyze_directory(directory_path)

