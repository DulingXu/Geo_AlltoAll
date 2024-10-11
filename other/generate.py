import os
import json
import numpy as np

# 生成文件供测试
# 文件目录
# latency_dir = "/Users/duling/Desktop/code/Geo_All2All/dataset/reallset/latency/1"
# conflict_dir = "/Users/duling/Desktop/code/Geo_All2All/dataset/reallset/conflict_rate"
# bandwidth_dir = "/Users/duling/Desktop/code/Geo_All2All/dataset/reallset/bandwidth"
num_messages_dir = "/Users/duling/Desktop/code/Geo_All2All/dataset/reallset/num_message_200"

# 确保目标目录存在
# os.makedirs(conflict_dir, exist_ok=True)
# os.makedirs(bandwidth_dir, exist_ok=True)
os.makedirs(num_messages_dir, exist_ok=True)

# Define latency_dir before using it
latency_dir = "/Users/duling/Desktop/code/Geo_All2All/dataset/reallset/1_latency"  # Update this path to the correct directory

# 读取 latency 目录中的文件
latency_files = [f for f in os.listdir(latency_dir) if f.startswith("matrix_") and f.endswith(".json")]

# # 1. 生成冲突矩阵文件（全 0 矩阵）
# for latency_file in latency_files:
#     num = latency_file.split('_')[1].split('.')[0]  # 提取数字
#     conflict_matrix = np.zeros((7, 7))  # 假设 7x7 矩阵
#     conflict_file = os.path.join(conflict_dir, f"conflict_{num}.json")

#     with open(conflict_file, 'w') as f:
#         json.dump(conflict_matrix.tolist(), f)
#     print(f"生成冲突矩阵文件: {conflict_file}")

# # 2. 生成带宽文件（内容全为 100 的数组）
# bandwidth_array = [100] * 7
# for latency_file in latency_files:
#     num = latency_file.split('_')[1].split('.')[0]  # 提取数字
#     bandwidth_file = os.path.join(bandwidth_dir, f"bandwidth_{num}.json")

#     with open(bandwidth_file, 'w') as f:
#         json.dump(bandwidth_array, f)
#     print(f"生成带宽文件: {bandwidth_file}")

# 3. ��成 num_message 文件（内容全为 100 的数组）
num_messages_array = [200] * 7
for latency_file in latency_files:
    num = latency_file.split('_')[1].split('.')[0]  # 提取数字
    num_message_file = os.path.join(num_messages_dir, f"num_message_{num}.json")

    with open(num_message_file, 'w') as f:
        json.dump(num_messages_array, f)
    print(f"生成 num_message 文件: {num_message_file}")