import os
import json

# 用于去除重复的时延文件

# 读取json文件并返回矩阵数据
def load_matrix_from_json(file_path):
    with open(file_path, 'r') as f:
        return json.load(f)

# 比较两个矩阵是否相同
def are_matrices_equal(matrix1, matrix2):
    return matrix1 == matrix2  # 使用Python的列表比较方法来比较两个矩阵

# 删除路径下重复的json文件
def remove_duplicate_json_files(directory):
    # 存储矩阵和文件路径的字典
    matrix_map = {}

    # 遍历文件夹中的所有json文件
    for filename in os.listdir(directory):
        if filename.endswith('.json'):
            file_path = os.path.join(directory, filename)

            # 读取json文件中的矩阵
            try:
                matrix = load_matrix_from_json(file_path)
            except json.JSONDecodeError:
                print(f"Error reading {file_path}. Skipping file.")
                continue

            # 查找是否已经存在相同的矩阵
            duplicate_found = False
            for existing_matrix, existing_file_path in matrix_map.items():
                if are_matrices_equal(matrix, existing_matrix):
                    # 如果找到相同的矩阵，删除编号较大的文件
                    existing_file_number = int(os.path.splitext(os.path.basename(existing_file_path))[0])
                    current_file_number = int(os.path.splitext(os.path.basename(file_path))[0])

                    if current_file_number > existing_file_number:
                        print(f"Removing duplicate file: {file_path}")
                        os.remove(file_path)
                    else:
                        print(f"Removing duplicate file: {existing_file_path}")
                        os.remove(existing_file_path)
                        # 更新为编号较小的文件
                        matrix_map[matrix] = file_path

                    duplicate_found = True
                    break

            if not duplicate_found:
                # 如果没有找到相同的矩阵，加入到字典中
                matrix_map[tuple(map(tuple, matrix))] = file_path

# 调用函数时，给定要处理的文件夹路径
directory = '/Users/duling/Desktop/code/Geo_All2All/dataset/reallset/latency/1'  
remove_duplicate_json_files(directory)