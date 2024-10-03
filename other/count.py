import os

def count_json_files(directory_path):
    # 统计 .json 文件的个数
    json_count = 0

    # 遍历目录下的所有文件
    for filename in os.listdir(directory_path):
        # 检查文件是否以 .json 结尾
        if filename.endswith(".json"):
            json_count += 1

    return json_count

# 替换 'abc' 为实际的文件路径
directory_path = '/Users/duling/Desktop/code/Geo_All2All/dataset/reallset/latency/1'

# 获取 .json 文件的数量
json_file_count = count_json_files(directory_path)

# 输出结果
print(f"There are {json_file_count} .json files in the directory: {directory_path}")