import os
import json

# 读取json文件并返回矩阵中的最大值
def find_max_in_json(file_path):
    with open(file_path, 'r') as f:
        matrix = json.load(f)
    
    # 将 "n" 作为不可达的表示，忽略掉这些值
    max_value = float('-inf')  # 初始化为负无穷大
    for row in matrix:
        for value in row:
            if value != "n":
                max_value = max(max_value, float(value))
    
    return max_value

# 打印并保存到日志
def log_and_print(log_file, message):
    print(message)  # 打印到终端
    with open(log_file, 'a') as log:
        log.write(message + '\n')  # 追加写入日志文件

# 批量处理指定文件夹下的所有 .json 文件
def process_all_json_files_in_directory(input_directory, log_file):
    # 清空并创建日志文件
    with open(log_file, 'w') as log:
        log.write("Max values in each .json file:\n")

    # 遍历输入目录下的所有 .json 文件
    for filename in os.listdir(input_directory):
        if filename.endswith(".json"):
            input_file_path = os.path.join(input_directory, filename)
            max_value = find_max_in_json(input_file_path)
            result = f"{filename}:{max_value}"
            
            # 输出结果并写入日志
            log_and_print(log_file, result)

# 调用函数时，给定输入文件夹路径和日志文件路径
# 原来的未处理路径
input_directory = '/Users/duling/Desktop/code/Geo_All2All/dataset/reallset/latency/1'  
log_file = '/Users/duling/Desktop/code/Geo_All2All/output/log/normal.log'  

process_all_json_files_in_directory(input_directory, log_file)