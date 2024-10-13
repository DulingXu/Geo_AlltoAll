import os
import pandas as pd
import matplotlib.pyplot as plt
import re
from collections import defaultdict

def read_data_from_log(file_path):
    """
    从给定的日志文件路径读取 Makespan 结果
    :param file_path: 日志文件路径
    :return: (文件名列表, Makespan 结果列表)
    """
    filenames, makespans = [], []

    print(f"正在读取文件: {file_path}")  # 调试信息

    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    for line in lines[1:]:  # 跳过第一行（列名）
        # 提取文件名和 Makespan 结果
        match = re.match(r'(.+?),\s+([\d.]+),\s+([\d.]+)', line)
        if match:
            filenames.append(match.group(1))
            makespans.append(float(match.group(3)))  # 只提取 Makespan 结果
        else:
            print(f"无法解析的行: {line.strip()}")  # 调试输出

    print(f"文件解析完毕: {len(makespans)} 条记录")  # 调试信息
    return filenames, makespans

def plot_makespan_boxplots(makespan_data, output_directory):
    """
    根据分类的 Makespan 数据生成箱线图并保存
    :param makespan_data: 字典，键为数字，值为文件路径列表
    :param output_directory: 输出目录
    """
    for key, file_paths in makespan_data.items():
        all_makespans = []  # 用于存储所有 Makespan 数据

        for file_path in file_paths:
            _, makespans = read_data_from_log(file_path)
            all_makespans.append(makespans)

        plt.figure(figsize=(14, 8))  # 设置图形大小

        # 绘制箱线图
        box = plt.boxplot(all_makespans, labels=[os.path.basename(fp) for fp in file_paths], patch_artist=True)

        # 设置颜色
        colors = ['#FF9999', '#66B3FF', '#99FF99', '#FFCC99', '#FFD700']  # 自定义颜色
        for patch, color in zip(box['boxes'], colors):
            patch.set_facecolor(color)

        plt.title(f'Makespan Boxplot for {key}')  # 图标题
        plt.xlabel('Algorithms')
        plt.ylabel('Makespan')
        plt.grid(True, linestyle='--', alpha=0.7)
        plt.xticks(rotation=15)  # 旋转横坐标标注
        plt.tight_layout()

        # 保存图表
        output_file = os.path.join(output_directory, f'makespan_boxplot_{key}.png')
        plt.savefig(output_file)
        plt.close()
        print(f"图表已保存: {output_file}")

def analyze_and_plot(directory, output_directory):
    """分析并绘制所有方案的 Makespan 结果"""
    makespan_data = defaultdict(list)

    # Debugging: Print the input directory
    print(f"Input directory: {directory}")

    # 遍历目录及其子目录，查找所有 .log 文件
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith("_analyze.log"):  # 只处理以 _analyze.log 结尾的文件
                file_path = os.path.join(root, file)
                print(f"找到日志文件: {file_path}")  # 调试信息

                # 从文件路径中提取数字（例如 0.1）
                match = re.search(r'_(\d+\.\d+)_', file_path)
                if match:
                    key = match.group(1)  # 提取数字
                    makespan_data[key].append(file_path)  # 将文件路径添加到对应的数字分类中

    # 生成图表
    plot_makespan_boxplots(makespan_data, output_directory)

# Example usage
if __name__ == "__main__":
    input_directory = "/Users/duling/Desktop/code/Geo_All2All/output/total_result/conflict/key_result"  # Replace with your data directory
    output_directory = "/Users/duling/Desktop/code/Geo_All2All/draw"  # Replace with your output directory
    analyze_and_plot(input_directory, output_directory)
