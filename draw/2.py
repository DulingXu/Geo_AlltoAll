import os
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
    "/Users/duling/Desktop/code/Geo_All2All/output/key_result/dp_group_analyze.log",
    "/Users/duling/Desktop/code/Geo_All2All/output/key_result/no_group_just_max_analyze.log"
]

labels = [
    "KMeans Grouping",
    "KMeans 2 Grouping",
    "KMeans 4 Grouping",
    "Random Grouping",
    "Shortest Grouping",
    "Our Group",
    "Our Group 2",
    "DP Group",
    "No Group Just Max"
]

# 从文件中提取每行最后的数字
def extract_last_number(file_path):
    numbers = []
    with open(file_path, 'r') as file:
        for line in file:
            try:
                # 提取行中最后一个数字
                number = float(line.strip().split(",")[-1])
                numbers.append(number)
            except ValueError:
                continue  # 如果解析失败，跳过此行
    return numbers

# 收集每个文件的最后一个数字
all_data = []
for path in file_paths:
    all_data.append(extract_last_number(path))

# 绘制散点图
plt.figure(figsize=(10, 8))

# 为每个方案绘制散点图
for i, data in enumerate(all_data):
    x_values = [i+1] * len(data)  # 用于散点图的x值，每个方案对应一个x轴位置
    plt.scatter(x_values, data, label=labels[i])

# 设置x轴标签和y轴标签
plt.xticks(range(1, len(labels) + 1), labels, rotation=45, ha='right')
plt.xlabel("Grouping Schemes", fontsize=12)
plt.ylabel("Values", fontsize=12)

# 显示图例
plt.legend(loc="upper left", bbox_to_anchor=(1, 1), fontsize=10)

# 调整布局
plt.tight_layout()

# 保存图表为PDF文件
plt.savefig('scatter_result.pdf')

# 显示图表
plt.show()