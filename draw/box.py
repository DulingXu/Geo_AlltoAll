import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# 定义文件路径列表和方案名称
file_paths = [
    "/Users/duling/Desktop/code/Geo_All2All/output/key_result/random_group_analyze.log",
    "/Users/duling/Desktop/code/Geo_All2All/output/key_result/kmeans_group_analyze.log",
    "/Users/duling/Desktop/code/Geo_All2All/output/key_result/kmeans_2_group_analyze.log",
    "/Users/duling/Desktop/code/Geo_All2All/output/key_result/kmeans_4_group_analyze.log",
    "/Users/duling/Desktop/code/Geo_All2All/output/key_result/shortest_group_analyze.log",
    "/Users/duling/Desktop/code/Geo_All2All/output/key_result/dp_group_analyze.log"
]

labels = [
    "Random Grouping",
    "KMeans Grouping",
    "KMeans 2 Grouping",
    "KMeans 4 Grouping",
    "Shortest Grouping",
    "Node Grouping"
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

# 定义颜色
colors = ['lightblue', 'lightgreen', 'lightcoral', 'lightyellow', 'lightpink', 'lightgray']

# 创建正方形比例的图
plt.figure(figsize=(9, 8))  # 设置为正方形比例
box = plt.boxplot(all_makespans, patch_artist=True, labels=labels, widths=0.2)

# 设定不同的颜色
for patch, color in zip(box['boxes'], colors):
    patch.set_facecolor(color)

# 计算每个方案的平均值并在箱线图上标注，向右偏移0.2个柱子的宽度，向上偏移1
for i, makespans in enumerate(all_makespans, start=1):
    mean_val = np.mean(makespans)  # 计算均值
    plt.text(i +0.4, mean_val, f'{mean_val:.2f}', horizontalalignment='center', verticalalignment='center', fontsize=12, color='black')

# 设置图标题和标签
plt.ylabel('Makespan (ms)', fontsize=14)

# 设置刻度字体大小
plt.xticks(rotation=12, fontsize=12)
plt.yticks(fontsize=12)

# 调整布局
plt.tight_layout()

# 保存图表为PDF文件
plt.savefig('box_result_square_with_means_shifted.pdf')

# 显示图表
plt.show()