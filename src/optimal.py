import os
import json
import numpy as np
from datetime import datetime

# Floyd-Warshall算法计算最短路径
def floyd_warshall_with_path(matrix):
    num_nodes = len(matrix)
    dist = np.full((num_nodes, num_nodes), np.inf)  # 初始化距离为无穷大
    next_node = [[None for _ in range(num_nodes)] for _ in range(num_nodes)]  # 记录路径
    
    # 初始化距离矩阵和路径矩阵
    for i in range(num_nodes):
        for j in range(num_nodes):
            if matrix[i][j] != "n":  # 忽略标记为'n'的边（不可达边）
                dist[i][j] = float(matrix[i][j])
                next_node[i][j] = j
    
    # 执行 Floyd-Warshall 算法
    for k in range(num_nodes):
        for i in range(num_nodes):
            for j in range(num_nodes):
                if dist[i][k] != np.inf and dist[k][j] != np.inf:  # 跳过不可达路径
                    if dist[i][k] + dist[k][j] < dist[i][j]:
                        dist[i][j] = dist[i][k] + dist[k][j]
                        next_node[i][j] = next_node[i][k]
    
    return dist, next_node

# 通过路径追溯计算经过哪些节点
def construct_path(next_node, i, j):
    if next_node[i][j] is None:
        return []  # 不可达，返回空列表
    path = [i]
    while i != j:
        i = next_node[i][j]
        path.append(i)
    return path

# 打印并保存日志
def log_and_print(log_file, message):
    print(message)
    with open(log_file, 'a') as log:
        log.write(message + '\n')

# 主要函数，读取文件，运行Floyd-Warshall算法并保存结果
def process_delay_matrix(input_file_path, log_file):
    # 读取输入的矩阵
    with open(input_file_path, 'r') as f:
        matrix = json.load(f)
    
    # Floyd-Warshall算法计算最短路径和路径信息
    dist, next_node = floyd_warshall_with_path(matrix)
    
    num_nodes = len(matrix)
    max_shortest_path = 0  # 记录最大最短路径的值
    
    # 记录所有最短路径以及经过的节点
    log_and_print(log_file, "Shortest paths:")
    for i in range(num_nodes):
        for j in range(num_nodes):
            if i != j:
                path = construct_path(next_node, i, j)
                if path:  # 如果存在路径
                    # 计算路径时延总和
                    path_str = "-->".join(map(str, path))
                    total_delay = sum(float(matrix[path[k]][path[k + 1]]) for k in range(len(path) - 1))
                    log_and_print(log_file, f"{i}-->{j}: {path_str} = {total_delay}")
                    # 更新最大最短路径
                    max_shortest_path = max(max_shortest_path, total_delay)
                else:
                    log_and_print(log_file, f"{i}-->{j}: No path")  # 不可达的情况

    # 输出整体最大时延（取最短路径中的最大值）
    log_and_print(log_file, f"\nOverall maximum shortest path delay: {max_shortest_path}")
    
    # 返回最大最短路径
    return max_shortest_path

# 批量处理指定文件夹下的所有 .json 文件，并生成总日志
def process_all_json_files_in_directory(input_directory, output_directory, overall_log_file_path):
    with open(overall_log_file_path, 'w') as overall_log:
        overall_log.write("Overall Maximum Shortest Path Delays:\n")

    # 遍历输入目录下的所有 .json 文件
    for filename in os.listdir(input_directory):
        if filename.endswith(".json"):
            input_file_path = os.path.join(input_directory, filename)
            log_file_path = os.path.join(output_directory, f"{os.path.splitext(filename)[0]}.log")
            
            # 清空并创建日志文件
            with open(log_file_path, 'w') as log_file:
                log_file.write(f"Processing file: {filename}\n")
            
            # 处理每个文件并生成对应的日志
            max_shortest_path = process_delay_matrix(input_file_path, log_file_path)
            
            # 将文件名和对应的最大最短路径记录到总日志
            with open(overall_log_file_path, 'a') as overall_log:
                overall_log.write(f"{filename}: {max_shortest_path}\n")

# 调用函数时，给定输入文件夹路径和日志输出目录
input_directory = '/Users/duling/Desktop/code/Geo_All2All/output/new_delay_matrix'  # 输入文件夹路径
output_directory = '/Users/duling/Desktop/code/Geo_All2All/output/new_latency_optimal'  # 输出日志路径
overall_log_file_path = '/Users/duling/Desktop/code/Geo_All2All/output/new_latency_optimal/0_overall_max_shortest_paths.log'  # 总日志文件路径

process_all_json_files_in_directory(input_directory, output_directory, overall_log_file_path)