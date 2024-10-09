import os
import pandas as pd
import matplotlib.pyplot as plt

# 定义文件路径列表和方案名称
file_paths = [
    "/Users/duling/Desktop/code/Geo_All2All/output/key_result/kmeans_group_analyze.log",
    "/Users/duling/Desktop/code/Geo_All2All/output/key_result/kmeans_2_group_analyze.log",
    "/Users/duling/Desktop/code/Geo_All2All/output/key_result/kmeans_4_group_analyze.log",
    "/Users/duling/Desktop/code/Geo_All2All/output/key_result/random_group_analyze.log",
    "/Users/duling/Desktop/code/Geo_All2All/output/key_result/shortest_group_analyze.log",
    "/Users/duling/Desktop/code/Geo_All2All/output/key_result/our_group_analyze.log",   
    "/Users/duling/Desktop/code/Geo_All2All/output/key_result/our_group_2_analyze.log",   
    "/Users/duling/Desktop/code/Geo_All2All/output/key_result/dp_group_analyze.log"
]

labels = [
    "KMeans Group",
    "KMeans 2 Group",
    "KMeans 4 Group",
    "Random Group",
    "Shortest Group",
    "Our Group",
    "Our Group 2",
    "DP Group"
]

# 从文件中提取最后的 Makespan 值
def extract_makespan(file_path):
    makespans = []
    with open(file_path, 'r') as file:
        for line in file:
            try:
                # 提取行中最后一个数字（Makespan）
                makespan = float(line.strip().split(",")[-1])
                makespans.append(makespan)
            except ValueError:
                continue  # 如果解析失败，跳过此行
    return makespans

# 收集所有方案的 Makespan 数据
all_makespans = []
for path in file_paths:
    all_makespans.append(extract_makespan(path))

# 创建箱线图
plt.figure(figsize=(10, 6))
plt.boxplot(all_makespans, labels=labels)

# 设置图标题和标签
plt.title('Comparison of Makespan Across Different Grouping Schemes')
plt.xlabel('Grouping Schemes')
plt.ylabel('Makespan (ms)')

# 显示图表
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()