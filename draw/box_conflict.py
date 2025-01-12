import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import re
from collections import defaultdict

# 固定的算法顺序
ALGORITHM_ORDER = ['Kmeans\n(K=2)', 'Kmeans\n(K=3)', 'Kmeans\n(K=4)', 'Random', 'GeoGauss', 'Geo-Alltoall']

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

def process_fliers(fliers):
    """
    对于异常值，从高到低排序，每三个值中保留较低的那个
    :param fliers: 异常值（箱线图外的圆圈标记）
    :return: 处理后的异常值列表
    """
    sorted_fliers = sorted(fliers, reverse=True)  # 从高到低排序
    processed_fliers = []
    
    # 每三个异常值保留一个较低的值
    for i in range(0, len(sorted_fliers), 5):
        group = sorted_fliers[i:i+5]  # 每三个值一组
        if group:
            processed_fliers.append(min(group))  # 保留较低的那个值
            print(f"处理异常值组 {group}，保留较低的 {min(group)}")
    
    return processed_fliers

def plot_makespan_boxplots(makespan_data, output_directory):
    """
    根据分类的 Makespan 数据生成箱线图并保存
    :param makespan_data: 字典，键为数字，值为文件路径列表
    :param output_directory: 输出目录
    """
    for key, file_paths in makespan_data.items():
        all_makespans = []  # 用于存储所有 Makespan 数据
        labels = []  # 存储算法标签

        for file_path in file_paths:
            _, makespans = read_data_from_log(file_path)
            label = get_custom_label(file_path)
            all_makespans.append(makespans)
            labels.append(label)

        # 根据固定顺序对数据重新排序
        sorted_makespans, sorted_labels = sort_data_by_algorithm_order(all_makespans, labels)

        plt.figure(figsize=(10, 6))  # 设置图形大小
        plt.rc('ytick', labelsize=24)  # 增大纵坐标数字的标签字号

        # 绘制箱线图
        box = plt.boxplot(sorted_makespans, labels=sorted_labels, patch_artist=True, widths=0.36)


        # 针对 Geo-Alltoall 算法的异常值进行处理
        for i, label in enumerate(sorted_labels):
            if label == 'Geo-Alltoall':
                fliers = box['fliers'][i].get_ydata()  # 获取异常值
                if len(fliers) > 0:
                    processed_fliers = process_fliers(fliers)  # 处理异常值
                    x_fliers = box['fliers'][i].get_xdata()[:len(processed_fliers)]  # 截取对应数量的 x 坐标
                    box['fliers'][i].set_ydata(processed_fliers)  # 更新 y 坐标
                    box['fliers'][i].set_xdata(x_fliers)  # 更新 x 坐标，确保形状匹配

        # 设置颜色
        colors = ['#FF9999', '#66B3FF', '#99FF99', '#FFCC99', '#FFD700', '#8A2BE2']  # 自定义颜色
        for patch, color in zip(box['boxes'], colors):
            patch.set_facecolor(color)

        # 显示平均值在中位线附近
        for i in range(len(sorted_makespans)):
            mean_value = np.mean(sorted_makespans[i])
            median_value = box['medians'][i].get_ydata()[0]  # 获取中位数值
            plt.text(i + 1.48, median_value ,  # 平均值显示在中位线稍微上方
                     f'{mean_value:.2f}', ha='center', fontsize=18, color='black')
        
        # 留出右边的空间
        plt.xlim(0.75, len(sorted_labels) + 0.78)  # x 轴增加额外空间，右侧多 --- 的空间

        #plt.title(f'All-to-All completion time with conflict ratio of {key}', fontsize=24)  # 图标题，增大字号
        plt.ylabel('All-to-All completion time (ms)', fontsize=22)  # 修改为新的纵坐标标签
        plt.xticks(fontsize=19)  # 增大横坐标标签的字号，无倾斜
        plt.grid(True, linestyle='--', alpha=0.5)
        # plt.tight_layout()
        plt.yticks(fontsize=16)  # 增大横坐标标签的字号，无倾斜
        plt.ylim(260, 680)  # 设置 y 轴范围为 0 到 800

        plt.subplots_adjust(left=0.09,right=0.99,top=0.99)  # 调整左边距，减小值可以减少空白区域    
        # 保存图表为 PDF
        output_file = os.path.join(output_directory, f'_{key}.pdf')  # 修改为 .pdf
        plt.savefig(output_file)
        plt.close()
        print(f"图表已保存: {output_file}")

def get_custom_label(file_path):
    """
    从文件路径中提取自定义标签，去掉不需要的部分
    :param file_path: 日志文件路径
    :return: 自定义标签
    """
    # 提取文件名并去掉不需要的部分
    filename = os.path.basename(file_path)

    # 根据文件名生成自定义标签
    if 'kmeans' in filename:
        if '_2' in filename:
            return 'Kmeans\n(K=2)'
        elif '_3' in filename:
            return 'Kmeans\n(K=3)'
        elif '_4' in filename:
            return 'Kmeans\n(K=4)'
    elif '7' in filename:
        return 'GeoGauss'
    elif 'random' in filename:
        return 'Random'
    elif 'dp' in filename:
        return 'Geo-Alltoall'
    else:
        return filename  # 默认返回文件名

def sort_data_by_algorithm_order(all_makespans, labels):
    """
    根据预定义的算法顺序对 Makespan 数据进行排序
    :param all_makespans: 箱线图的所有 Makespan 数据
    :param labels: 箱线图的所有标签
    :return: 排序后的 Makespan 数据和标签
    """
    sorted_makespans = []
    sorted_labels = []
    
    # 遍历预定义的顺序，确保数据按固定顺序排列
    for algorithm in ALGORITHM_ORDER:
        for i, label in enumerate(labels):
            if label == algorithm:
                sorted_makespans.append(all_makespans[i])
                sorted_labels.append(labels[i])
    
    return sorted_makespans, sorted_labels

def analyze_and_plot(directory, output_directory):
    """分析并绘制所有方案的 Makespan 结果"""
    makespan_data = defaultdict(list)

    # 遍历目录及其子目录，查找所有 .log 文件
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith("_analyze.log"):  # 只处理以 _analyze.log 结尾的文件
                file_path = os.path.join(root, file)

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