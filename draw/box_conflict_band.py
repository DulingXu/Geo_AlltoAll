import os
import pandas as pd
import matplotlib.pyplot as plt

# 输入和输出目录
input_directory = "/Users/duling/Desktop/code/Geo_All2All/output-1/key-analyze-result"  # 输入路径
output_directory = "/Users/duling/Desktop/code/Geo_All2All/draw"  # 输出路径

# 准备字典存储每个文件的 Makespan 数据
makespan_data_dict = {}

# 遍历输入目录中的所有日志文件
for filename in os.listdir(input_directory):
    if filename.endswith(".log"):  # 仅处理 .log 文件
        file_path = os.path.join(input_directory, filename)
        makespan_data = []
        with open(file_path, 'r') as f:
            for line in f:
                parts = line.strip().split(',')
                if len(parts) == 3:
                    try:
                        makespan = float(parts[2].strip())  # 提取 Makespan 数值
                        makespan_data.append(makespan)
                    except ValueError:
                        continue  # 跳过转换失败的行
        # 如果文件中有数据，存储到字典中
        if makespan_data:
            makespan_data_dict[filename] = makespan_data

# 创建箱线图
plt.figure(figsize=(12, 8))

# 为每个文件生成一个箱子
plt.boxplot(makespan_data_dict.values(), patch_artist=True, labels=makespan_data_dict.keys())

# 图像设置
plt.title('Makespan Analysis by Log File', fontsize=14)
plt.ylabel('Makespan (ms)', fontsize=12)
plt.xticks(rotation=45, ha="right")  # 旋转 x 轴标签以避免重叠
plt.grid(True)

# 保存图像到输出目录
output_plot_path = os.path.join(output_directory, "makespan_boxplot_by_logfile.pdf")
plt.tight_layout()  # 调整布局避免标签重叠
plt.savefig(output_plot_path)

# 打印保存的图片路径
print(f"箱线图已保存到: {output_plot_path}")