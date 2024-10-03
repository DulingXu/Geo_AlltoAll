import os
import json
import numpy as np

# 根据最短路径，剪枝未使用的边，输出路径日志，形成剪枝后的新矩阵数据
# Floyd-Warshall算法计算最短路径
def floyd_warshall_with_path(matrix):
    num_nodes = len(matrix)
    dist = np.full((num_nodes, num_nodes), np.inf)  # 初始化距离为无穷大
    next_node = [[None for _ in range(num_nodes)] for _ in range(num_nodes)]  # 记录路径
    
    # 初始化距离矩阵和路径矩阵
    for i in range(num_nodes):
        for j in range(num_nodes):
            if i == j:
                dist[i][j] = 0
            elif matrix[i][j] != '0.0':
                dist[i][j] = float(matrix[i][j])
                next_node[i][j] = j
    
    # 执行 Floyd-Warshall 算法
    for k in range(num_nodes):
        for i in range(num_nodes):
            for j in range(num_nodes):
                if dist[i][k] + dist[k][j] < dist[i][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]
                    next_node[i][j] = next_node[i][k]
    
    return dist, next_node

# 通过路径追溯计算经过哪些节点
def construct_path(next_node, i, j):
    if next_node[i][j] is None:
        return []
    path = [i]
    while i != j:
        i = next_node[i][j]
        path.append(i)
    return path

# 找到并记录未使用的边
def find_unused_edges(matrix, used_edges):
    num_nodes = len(matrix)
    unused_edges = []
    for i in range(num_nodes):
        for j in range(num_nodes):
            if i != j and (i, j) not in used_edges and matrix[i][j] != '0.0':
                unused_edges.append((i, j))
    return unused_edges

# 打印并保存日志
def log_and_print(log_file, message):
    print(message)
    with open(log_file, 'a') as log:
        log.write(message + '\n')

# 主要函数，读取文件，运行Floyd-Warshall算法并保存结果
def process_delay_matrix(input_file_path, output_directory, log_file):
    # 读取输入的矩阵
    with open(input_file_path, 'r') as f:
        matrix = json.load(f)
    
    # Floyd-Warshall算法计算最短路径和路径信息
    dist, next_node = floyd_warshall_with_path(matrix)
    
    num_nodes = len(matrix)
    used_edges = set()
    shortest_paths = {}
    
    # 记录所有最短路径以及经过的节点
    log_and_print(log_file, f"Shortest paths for {input_file_path}:")
    for i in range(num_nodes):
        for j in range(num_nodes):
            if i != j:
                path = construct_path(next_node, i, j)
                if len(path) > 2:
                    shortest_paths[f"{i}-->{j}"] = "-->".join(map(str, path))
                elif len(path) == 2:
                    shortest_paths[f"{i}-->{j}"] = None
                
                # 记录所有使用过的边
                for k in range(len(path) - 1):
                    used_edges.add((path[k], path[k + 1]))
    
    # 输出路径结果
    for path, nodes in shortest_paths.items():
        if nodes:
            log_and_print(log_file, f"{path}: {nodes}")
        else:
            log_and_print(log_file, f"{path}")
    
    # 找到未使用的边
    unused_edges = find_unused_edges(matrix, used_edges)
    
    # 输出未使用的边
    log_and_print(log_file, "\nUnused edges (剪枝的边):")
    for edge in unused_edges:
        log_and_print(log_file, f"cut:{edge[0]}-->{edge[1]}")
    
    # 创建新矩阵，标记未使用的边为 'n'
    new_matrix = [row[:] for row in matrix]
    for edge in unused_edges:
        new_matrix[edge[0]][edge[1]] = "n"
    
    # 生成新文件名
    input_filename = os.path.basename(input_file_path)
    new_filename = f"new_{input_filename}"
    new_file_path = os.path.join(output_directory, new_filename)
    
    # 将新矩阵写入文件
    with open(new_file_path, 'w') as f:
        json.dump(new_matrix, f, indent=4)
    
    log_and_print(log_file, f"\nNew matrix with unused edges marked as 'n' saved to: {new_file_path}\n")

# 新增函数，用于批量处理文件夹下的所有 .json 文件
def process_all_json_files_in_directory(input_directory, output_directory):
    log_file = os.path.join(output_directory, 'new_delay.log')
    # 清空日志文件
    open(log_file, 'w').close()
    
    # 遍历输入目录下的所有 .json 文件
    for filename in os.listdir(input_directory):
        if filename.endswith(".json"):
            input_file_path = os.path.join(input_directory, filename)
            process_delay_matrix(input_file_path, output_directory, log_file)



# 调用函数时，给定输入文件路径和输出目录
input_directory = '/Users/duling/Desktop/code/Geo_All2All/dataset/reallset/latency/1'  
output_directory = '/Users/duling/Desktop/code/Geo_All2All/output/new_delay' 

process_all_json_files_in_directory(input_directory, output_directory)