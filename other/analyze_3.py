import os
import re

# use to analyze the log file of no group just max latency transfer
def get_last_line(file_path):
    """获取文件的最后一行"""
    with open(file_path, 'r') as file:
        lines = file.readlines()
        return lines[-1].strip()

def extract_last_number(line):
    """从行中提取 makespan 的值"""
    match = re.search(r"makespan 的值: ([\d.]+)", line)
    if match:
        return float(match.group(1))
    else:
        print(f"Warning: Could not find makespan value in line: '{line}'")
        return None

def analyze_directory(directory_path, output_directory):
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
            execution_time = 0.0  
            # the first file has no previous file to calculate the time difference

        log_entries.append(f"{file_name}, {execution_time:.3f}, {makespan_result}")
        previous_time = current_time

    # 生成日志文件以存储结果
    log_file_name = os.path.basename(directory_path) + "_analyze.log"
    log_file_path = os.path.join(output_directory, log_file_name)
    with open(log_file_path, 'w') as log_file:
        log_file.write("文件名, 执行时间（毫秒）, Makespan 结果\n")
        for entry in log_entries:
            log_file.write(entry + "\n")

    print(f"分析完成，日志已存储到: {log_file_path}")

if __name__ == "__main__":
    # 指定多个输入目录路径
    input_directories = [
        "/Users/duling/Desktop/code/Geo_All2All/output/total_result/conflict/0.1/no_group_conflict_0.1",
        "/Users/duling/Desktop/code/Geo_All2All/output/total_result/conflict/0.2/no_group_conflict_0.2",
        "/Users/duling/Desktop/code/Geo_All2All/output/total_result/conflict/0.3/no_group_conflict_0.3",
        "/Users/duling/Desktop/code/Geo_All2All/output/total_result/conflict/0.4/no_group_conflict_0.4",
        "/Users/duling/Desktop/code/Geo_All2All/output/total_result/conflict/0.5/no_group_conflict_0.5",
        # "/Users/duling/Desktop/code/Geo_All2All/output/total_result/conflict/0.1/no_group",
        # to add more directory paths
    ]

    # specify the output directory path
    output_directory = "/Users/duling/Desktop/code/Geo_All2All/output/total_result/conflict/key_result"

    # 确保输出目录存在
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    # 处理每个输入目录
    for directory in input_directories:
        analyze_directory(directory, output_directory)
