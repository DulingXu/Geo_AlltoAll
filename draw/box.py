import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# 定义文件路径列表和方案名称
file_paths = [
    # "/Users/duling/Desktop/code/Geo_All2All/output/key_result/random_group_analyze.log",
    # "/Users/duling/Desktop/code/Geo_All2All/output/key_result/kmeans_group_analyze.log",
    # "/Users/duling/Desktop/code/Geo_All2All/output/key_result/kmeans_2_group_analyze.log",
    # "/Users/duling/Desktop/code/Geo_All2All/output/key_result/kmeans_4_group_analyze.log",
    # "/Users/duling/Desktop/code/Geo_All2All/output/key_result/shortest_group_analyze.log",
    # "/Users/duling/Desktop/code/Geo_All2All/output/key_result/dp_group_analyze.log"
    
    "/Users/duling/Desktop/code/Geo_All2All/output/key_result/kmeans_group_1_latency_analyze.log",
    "/Users/duling/Desktop/code/Geo_All2All/output/key_result/kmeans_2_group_1_latency_analyze.log",
    "/Users/duling/Desktop/code/Geo_All2All/output/key_result/kmeans_4_group_1_latency_analyze.log",
    "/Users/duling/Desktop/code/Geo_All2All/output/key_result/random_group_1_latency_analyze.log", 
    "/Users/duling/Desktop/code/Geo_All2All/output/key_result/shortest_group_1_latency_analyze.log",
    # "/Users/duling/Desktop/code/Geo_All2All/output/key_result/shortest_group_1_1_latency_analyze.log",
    # "/Users/duling/Desktop/code/Geo_All2All/output/key_result/our_group_1_latency_analyze.log",   
    # "/Users/duling/Desktop/code/Geo_All2All/output/key_result/our_group_2_1_latency_analyze.log",   
    # "/Users/duling/Desktop/code/Geo_All2All/output/key_result/best_group_detection_analyze.log", 
    "/Users/duling/Desktop/code/Geo_All2All/output/key_result/dp_group_1_latency_analyze.log",
    "/Users/duling/Desktop/code/Geo_All2All/output/key_result/no_group_just_max_200_1_latency_analyze.log",
]

labels = [
    "KMeans Grouping\n(K=3)",
    "KMeans Grouping\n(K=2)",
    "KMeans Grouping\n(K=4)",
    "Random Grouping",
    "Shortest Grouping\n (low bound) ",
    # "Shortest Grouping_1",
    # "our_group_2",
    "Node Grouping\n (our's) ",
    "No Grouping",
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

def reduce_outliers(data, threshold=0.1):
    """Reduce outliers by merging close values, keeping the larger one."""
    if not data:
        return data
    data = sorted(data)
    reduced_data = [data[0]]
    for value in data[1:]:
        if value - reduced_data[-1] > threshold:
            reduced_data.append(value)
        else:
            reduced_data[-1] = max(reduced_data[-1], value)
    return reduced_data

# 收集所有方案的 Makespan 数据并处理异常值
all_makespans = []
for path in file_paths:
    makespans = extract_makespan(path)
    # Reduce outliers for each dataset
    makespans = reduce_outliers(makespans)
    all_makespans.append(makespans)

# 确保长度匹配
if len(labels) != len(all_makespans):
    raise ValueError("标签数量必须与 all_makespans 中的数据集数量一致。")

# 定义颜色
colors = ['lightblue', 'lightgreen', 'lightcoral', 'lightyellow', 'lightpink', 'lightgray']

# 创建正方形比例的图
plt.figure(figsize=(16, 8))  
box = plt.boxplot(
    all_makespans, 
    patch_artist=True, 
    tick_labels=labels, 
    widths=0.24,
    flierprops=dict(marker='o', color='red', markersize=5)  # 设置异常值的样式
)

# 设定不同的颜色和加粗框线
for patch, color in zip(box['boxes'], colors):
    patch.set_facecolor(color)
    patch.set_linewidth(2)  # Set the linewidth to make the box edges thicker

# 计算每个方案的平均值并在箱线图上标注，向右偏移0.2个柱子的宽度，向上偏移1
for i, makespans in enumerate(all_makespans, start=1):
    mean_val = np.mean(makespans)  # 计算均值
    plt.text(i+0.36, mean_val, f'{mean_val:.2f}', horizontalalignment='center', verticalalignment='center', fontsize=16, color='black')

# 设置图标题和标签
plt.ylabel('Makespan (ms)', fontsize=20)

# 设置刻度字体大小
plt.xticks(rotation=16, fontsize=18)
plt.yticks(fontsize=18)

# 去掉右边和上边的框线
ax = plt.gca()  # 获取当前的Axes对象
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)

# 调整布局
plt.tight_layout()

# 保存图表为PDF文件
plt.savefig('box_result_square_with_means_shifted.pdf')

# 显示图表
plt.show()