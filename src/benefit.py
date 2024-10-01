import re

# 从日志文件中读取数据并转换为字典
def load_log_data(log_file_path, remove_prefix=None):
    data = {}
    with open(log_file_path, 'r') as f:
        for line in f:
            match = re.match(r'([\w_]+\.json):\s*(\d+\.?\d*)', line)
            if match:
                filename = match.group(1)
                if remove_prefix and filename.startswith(remove_prefix):
                    filename = filename[len(remove_prefix):]  # 去掉前缀
                value = float(match.group(2))
                data[filename] = value
    return data

# 计算文件 A 中的数据比文件 B 中的数据大的占比
def compare_logs(log_a, log_b):
    larger_count = 0
    total_count = 0

    # 遍历文件 A 和 B 中共有的文件
    for filename in log_a:
        if filename in log_b:
            total_count += 1
            if log_a[filename] > log_b[filename]:
                larger_count += 1

    if total_count > 0:
        percentage_larger = (larger_count / total_count) * 100
        print(f"Total files compared: {total_count}")
        print(f"Files where log A has a larger value than log B: {larger_count}")
        print(f"Percentage of files where log A is larger than log B: {percentage_larger:.2f}%")
    else:
        print("No common files to compare.")

# 文件路径
log_a_path = '/Users/duling/Desktop/code/Geo_All2All/output/log/normal.log'  # 日志 原始最大值 文件路径
log_b_path = '/Users/duling/Desktop/code/Geo_All2All/output/new_latency_optimal/0_overall_max_shortest_paths.log'  # 日志 剪枝后的最短路径日志文件路径

# 加载日志数据，去掉 'new_' 前缀以便文件名匹配
log_a_data = load_log_data(log_a_path)
log_b_data = load_log_data(log_b_path, remove_prefix="new_")

# 反向比较日志 A 和 B
compare_logs(log_a_data, log_b_data)