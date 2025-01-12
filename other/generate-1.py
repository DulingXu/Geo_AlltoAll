import os
import json

def create_files(directory, base_filename, content, start, stop, step):
    """生成文件，文件名数字递增，以 step 为步长，内容相同"""
    if not os.path.exists(directory):
        os.makedirs(directory)
    
    for i in range(start, stop + 1, step):
        file_path = os.path.join(directory, f"{base_filename}_{i}.json")
        with open(file_path, 'w') as f:
            json.dump(content, f, indent=4)
        print(f"文件已生成: {file_path}")

if __name__ == "__main__":
    # 目标目录
    directory = "/Users/duling/Desktop/code/Geo_All2All/output/group_result/no_group_source"
    
    # 文件名基础
    base_filename = "no_group"
    
    # 文件内容 (从 no_group.json 中复制)
    content = [
        [0],
        [1],
        [2],
        [3],
        [4],
        [5],
        [6]
    ]
    
    # 生成 333 个文件，从 100 到 33300，每次跳跃 100
    create_files(directory, base_filename, content, start=100, stop=33300, step=100)