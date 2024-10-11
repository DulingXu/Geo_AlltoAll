import json
import os
from datetime import datetime

# 读取JSON文件
input_file = '/Users/duling/Desktop/code/Geo_All2All/dataset/reallset/1_latency/latency_matrices_cleaned.json'
output_dir = '/Users/duling/Desktop/code/Geo_All2All/dataset/reallset/1_latency'

# 确保输出目录存在
os.makedirs(output_dir, exist_ok=True)

# 检查文件是否存在
if not os.path.exists(input_file):
    print(f"Error: The file {input_file} does not exist.")
else:
    # 读取JSON数据
    with open(input_file, 'r') as f:
        data = json.load(f)

    # 初始化文件名计数器
    file_counter = 100

    # 遍历每个时间点的矩阵
    for entry in data['data']:
        # 创建文件名
        filename = f"matrix_{file_counter}.json"
        filepath = os.path.join(output_dir, filename)
        
        # 将矩阵写入文件
        with open(filepath, 'w') as f:
            # Convert each number to a string to match the format
            json.dump([[str(value) for value in row] for row in entry['matrix']], f, indent=4)

        # 增加计数器
        file_counter += 100

    print(f"已提取 {len(data['data'])} 个矩阵并保存到 {output_dir} 目录")

    print("Current working directory:", os.getcwd())
