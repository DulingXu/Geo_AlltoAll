import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# 定义文件路径列表和方案名称
file_paths = [
    "/Users/duling/Desktop/code/Geo_All2All/output/key_result/kmeans_2_group_1_latency_analyze.log",
    "/Users/duling/Desktop/code/Geo_All2All/output/key_result/kmeans_group_1_latency_analyze.log",
    "/Users/duling/Desktop/code/Geo_All2All/output/key_result/kmeans_4_group_1_latency_analyze.log",
    "/Users/duling/Desktop/code/Geo_All2All/output/key_result/random_group_1_latency_analyze.log", 
    "/Users/duling/Desktop/code/Geo_All2All/output/key_result/no_group_just_max_200_1_latency_analyze.log",
    "/Users/duling/Desktop/code/Geo_All2All/output/key_result/dp_group_1_latency_analyze.log",
]

labels = [
    "Kmeans \n(K=2)",
    "Kmeans \n(K=3)",
    "Kmeans \n(K=4)",
    "Random",
    "GeoGauss",
    "Geo-Alltoall ",

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

# 定义颜色，与 @box_conflict.py 保持一致
colors = ['#FF9999', '#66B3FF', '#99FF99', '#FFCC99', '#FFD700', '#8A2BE2']  # 自定义颜色

# 调整图幅大小，确保和 @box_conflict.py 保持一致
plt.figure(figsize=(10, 6))

# 绘制箱线图，确保箱子宽度一致
box = plt.boxplot(
    all_makespans, 
    patch_artist=True, 
    widths=0.34,  # 设置一致的箱子宽度
    flierprops=dict(marker='o', color='black', markersize=5)  # 设置异常值样式
)

# 设定不同的颜色和加粗框线
for patch, color in zip(box['boxes'], colors):
    patch.set_facecolor(color)
    patch.set_linewidth(2)  # 设置框线宽度

# 计算每个方案的平均值并在箱线图上标注
for i, makespans in enumerate(all_makespans, start=1):
    mean_val = np.mean(makespans)  # 计算均值
    plt.text(i+0.46, mean_val, f'{mean_val:.2f}', horizontalalignment='center', verticalalignment='center', fontsize=16, color='black')

# 设置图标题和标签
plt.ylabel('All-to-All Completion Time (ms)', fontsize=22)
#plt.title('All-to-All Completion Time (Conflict-Free)', fontsize=28)

# 设置刻度字体大小，不倾斜
plt.xticks(range(1, len(labels) + 1), labels, fontsize=19)
plt.yticks(fontsize=18)

# 设置Y轴范围
plt.ylim(260, 680)  # 设置Y轴的最大值为800

# 去掉右边和上边的框线
ax = plt.gca()
ax.spines['right'].set_visible(True)
ax.spines['top'].set_visible(True)

# 增加网格线
plt.grid(True, linestyle='--', alpha=0.6)
plt.grid(True, linestyle='--', alpha=0.6, which='major', axis='y')  # Move the grid line of the mean value up

# 留出右边的空间
plt.xlim(0.75, len(labels) + 0.78)  # x 轴增加额外空间，右侧多 --- 的空间
plt.subplots_adjust(left=0.1,right=0.99,top=0.99)  # 调整左边距，减小值可以减少空白区域    
# 调整布局

# 保存图表为PDF文件
plt.savefig('box_without_conflict.pdf')

# 显示图表
plt.show()