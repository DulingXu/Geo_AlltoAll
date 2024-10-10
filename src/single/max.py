import os
import json

# 读取json文件并返回矩阵中的最大值
def find_max_in_json(file_path):
    with open(file_path, 'r') as f:
        matrix = json.load(f)
    
    # 初始化最大值为负无穷大
    max_value = float('-inf')
    for row in matrix:
        for value in row:
            if value != "n":  # 忽略 "n" 表示的不可达值
                max_value = max(max_value, float(value))
    
    return max_value

# 打印并保存到日志
def log_and_print(log_file, message):
    print(message)  # 打印到终端
    with open(log_file, 'a') as log:
        log.write(message + '\n')  # 追加写入日志文件

# 批量处理指定文件夹下的所有 .json 文件
def process_all_json_files_in_directory(input_directory, output_log_file):
    # 清空日志文件
    with open(output_log_file, 'w') as log:
        log.write("Max values in each .json file:\n")

    # 遍历输入目录下的所有 .json 文件
    for filename in os.listdir(input_directory):
        if filename.endswith(".json"):
            input_file_path = os.path.join(input_directory, filename)
            max_value = find_max_in_json(input_file_path)
            result = f"{filename}: {max_value}"
            
            # 输出每个文件中的最大值到日志
            log_and_print(output_log_file, result)

# 调用函数时，给定输入文件夹路径和输出文件路径
input_directory = '/Users/duling/Desktop/code/Geo_All2All/dataset/reallset/latency/1'  # 输入路径
output_log_file = '/Users/duling/Desktop/code/Geo_All2All/output/key_result/no_group_just_max_analyze.log'  # 输出文件路径

process_all_json_files_in_directory(input_directory, output_log_file)