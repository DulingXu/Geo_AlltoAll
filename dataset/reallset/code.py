import os
import json
import shutil

def max_jumps(distance):
    n = len(distance)
    memo = [[-1] * n for _ in range(n)]

    def dfs(i, j):
        if memo[i][j] != -1:
            return memo[i][j]

        max_jump = 0
        for k in range(n):
            if k != i and k != j:
                if distance[i][k] + distance[k][j] < distance[i][j]:
                    max_jump = max(max_jump, 1 + dfs(k, j))

        memo[i][j] = max_jump
        return max_jump               # 返回最大跳数矩阵
    
    for i in range(n):
        for j in range(n):
            if i != j:
                dfs(i, j)

    return max(max(row) for row in memo)  # 返回跳数矩阵的最大值
      

def classify_json_files(input_folder, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    max_value_dict = {}

    for filename in os.listdir(input_folder):
        if filename.endswith('.json'):
            file_path = os.path.join(input_folder, filename)

            with open(file_path, 'r') as f:
                data = json.load(f)

            # 转换 JSON 数据到距离矩阵
            distance = [[float(value) for value in row] for row in data]
            max_value = max_jumps(distance)

            # 创建新的文件夹用于保存相同最大值的文件
            max_folder = os.path.join(output_folder, str(max_value))
            if not os.path.exists(max_folder):
                os.makedirs(max_folder)

            # 移动文件到相应的文件夹
            shutil.move(file_path, os.path.join(max_folder, filename))

if __name__ == "__main__":
    input_folder = "D:\\Matrix-1"  # 输入文件夹路径
    output_folder = "D:\\result"    # 输出文件夹路径
    classify_json_files(input_folder, output_folder)
