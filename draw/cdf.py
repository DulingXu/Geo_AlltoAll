import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.colors as mcolors
from matplotlib.backends.backend_pdf import PdfPages
import subprocess
import sys

# 定义文件路径列表和方案名称
file_paths = [
    "/Users/duling/Desktop/code/Geo_All2All/output/key_result/kmeans_group_1_latency_analyze.log",
    "/Users/duling/Desktop/code/Geo_All2All/output/key_result/kmeans_2_group_1_latency_analyze.log",
    "/Users/duling/Desktop/code/Geo_All2All/output/key_result/kmeans_4_group_1_latency_analyze.log",
    "/Users/duling/Desktop/code/Geo_All2All/output/key_result/random_group_1_latency_analyze.log", 
    "/Users/duling/Desktop/code/Geo_All2All/output/key_result/shortest_group_1_latency_analyze.log",
    "/Users/duling/Desktop/code/Geo_All2All/output/key_result/dp_group_1_latency_analyze.log",
    "/Users/duling/Desktop/code/Geo_All2All/output/key_result/no_group_just_max_200_1_latency_analyze.log",
]

labels = [
    "KMeans Grouping\n(K=3)",
    "KMeans Grouping\n(K=2)",
    "KMeans Grouping\n(K=4)",
    "Random Grouping",
    "Shortest Grouping\n (low bound) ",
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

# 收集所有方案的 Makespan 数据
all_makespans = []
for path in file_paths:
    all_makespans.append(extract_makespan(path))

# 定义不同的颜色
colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf']

# 创建CDF图
plt.figure(figsize=(10,6))

for i, makespans in enumerate(all_makespans):
    # 计算CDF
    sorted_data = np.sort(makespans)
    yvals = np.arange(len(sorted_data))/float(len(sorted_data)-1)
    
    # 在绘制 CDF 时增加 linewidth 参数
    plt.plot(sorted_data, yvals, label=labels[i], color=colors[i % len(colors)], linewidth=2.5)

# 设置图标题和标签
plt.xlabel('Makespan (ms)', fontsize=20)
plt.ylabel('CDF', fontsize=20)
#plt.title('Cumulative Distribution Function of Makespan', fontsize=16)

# 设置图例
plt.legend(fontsize=18)

# 设置刻度字体大小
plt.xticks(fontsize=18)
plt.yticks(fontsize=18)

# 添加网格
plt.grid(True, linestyle='--', alpha=0.7)

# 调整布局
plt.tight_layout()

# 保存为 PDF 并自动关闭
pdf_filename = 'cdf_result.pdf'
with PdfPages(pdf_filename) as pdf:
    pdf.savefig()
    plt.close()

print(f"PDF saved as {pdf_filename}")

# 自动打开 PDF 文件
if sys.platform.startswith('darwin'):  # macOS
    subprocess.call(('open', pdf_filename))
elif sys.platform.startswith('win'):   # Windows
    os.startfile(pdf_filename)
else:  # Linux
    subprocess.call(('xdg-open', pdf_filename))

# 退出程序
sys.exit()

# Adjust spines for a darker border
plt.gca().spines['top'].set_visible(False)
plt.gca().spines['right'].set_visible(False)
plt.gca().spines['bottom'].set_color('#333333')
plt.gca().spines['left'].set_color('#333333')
