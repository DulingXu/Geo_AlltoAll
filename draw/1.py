import matplotlib.pyplot as plt
import re

# use to draw the execution time and makespan of different algorithms

def read_data_from_log(file_path):
    """
    从给定的日志文件路径读取执行时间和 Makespan 结果
    :param file_path: 日志文件路径
    :return: (文件名列表, 执行时间列表, Makespan 结果列表)
    """
    filenames, exec_times, makespans = [], [], []

    print(f"正在读取文件: {file_path}")  # 调试信息

    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    for line in lines:
        # 提取文件名、执行时间、Makespan 结果
        match = re.match(r'(.+?),\s+([\d.]+),\s+([\d.]+)', line)
        if match:
            filenames.append(match.group(1))
            exec_times.append(float(match.group(2)))
            makespans.append(float(match.group(3)))
        else:
            print(f"无法解析的行: {line.strip()}")  # 调试输出

    print(f"文件解析完毕: {len(exec_times)} 条记录")  # 调试信息
    return filenames, exec_times, makespans

def plot_results(file_paths):
    """
    根据多个文件生成两个子图：执行时间和 Makespan 结果
    :param file_paths: 文件路径列表
    """
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(24, 14))  # 将图的宽度增加为 20，以便点分散

    markers = ['^', 'x', 's', '.', '+','^']  # 定义几种不同的标记符号
    for i, file_path in enumerate(file_paths):
        filenames, exec_times, makespans = read_data_from_log(file_path)

        # 为了图示，使用文件名作为图例
        label = file_path.split('/')[-1]
        marker = markers[i % len(markers)]  # 按顺序选择标记符号

        # 检查解析到的数据
        print(f"绘制文件: {label}, 执行时间数: {len(exec_times)}, Makespan数: {len(makespans)}")

        # 绘制执行时间散点图
        ax1.scatter(range(len(exec_times)), exec_times, label=label, marker=marker)
        ax1.set_title('Computation Time')  # 左图标题改为英文
        ax1.set_xlabel('Data Points')
        ax1.set_ylabel('Execution Time (ms)')  # 改为毫秒单位

        # 绘制 Makespan 结果散点图
        ax2.scatter(range(len(makespans)), makespans, label=label, marker=marker)
        ax2.set_title('Transmission Makespan')  # 右图标题改为英文
        ax2.set_xlabel('Data Points')
        ax2.set_ylabel('Makespan')

    # 添加图例
    ax1.legend()
    ax2.legend()

    # 显示图表
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    # 示例文件路径，添加你实际使用的 .log 文件路径
    # K = 3  Kmeans ，下同
    # K = 2
    # k = 4
    # 随机分组
    # 最短路径，不考虑所有实现的问题，直接走最短路径的值，也是最低bound
    # 
    # file_paths = [
    #     "/Users/duling/Desktop/code/Geo_All2All/output/key_result/kmeans_group_analyze.log",
    #     "/Users/duling/Desktop/code/Geo_All2All/output/key_result/kmeans_2_group_analyze.log",
    #     "/Users/duling/Desktop/code/Geo_All2All/output/key_result/kmeans_4_group_analyze.log",
    #     "/Users/duling/Desktop/code/Geo_All2All/output/key_result/random_group_analyze.log",
    #     "/Users/duling/Desktop/code/Geo_All2All/output/key_result/shortest_group_analyze.log",
    #     "/Users/duling/Desktop/code/Geo_All2All/output/key_result/our_group_analyze.log",   
    #     "/Users/duling/Desktop/code/Geo_All2All/output/key_result/our_group_2_analyze.log",   
    #    #  "/Users/duling/Desktop/code/Geo_All2All/output/key_result/best_group_detection_analyze.log", 
    #    "/Users/duling/Desktop/code/Geo_All2All/output/key_result/dp_group_analyze.log",
    #    "/Users/duling/Desktop/code/Geo_All2All/output/key_result/no_group_just_max_analyze.log",
    
    # ]
    file_paths = [
        #"/Users/duling/Desktop/code/Geo_All2All/output/key_result/kmeans_group_1_latency_analyze.log",
        #"/Users/duling/Desktop/code/Geo_All2All/output/key_result/kmeans_2_group_1_latency_analyze.log",
        "/Users/duling/Desktop/code/Geo_All2All/output/key_result/kmeans_4_group_1_latency_analyze.log",
        # "/Users/duling/Desktop/code/Geo_All2All/output/key_result/random_group_1_latency_analyze.log",
        # "/Users/duling/Desktop/code/Geo_All2All/output/key_result/shortest_group_1_latency_analyze.log",
        # "/Users/duling/Desktop/code/Geo_All2All/output/key_result/shortest_group_1_1_latency_analyze.log",
        #"/Users/duling/Desktop/code/Geo_All2All/output/key_result/our_group_1_latency_analyze.log",   
        "/Users/duling/Desktop/code/Geo_All2All/output/key_result/our_group_2_1_latency_analyze.log",   
       #  "/Users/duling/Desktop/code/Geo_All2All/output/key_result/best_group_detection_analyze.log", 
       #"/Users/duling/Desktop/code/Geo_All2All/output/key_result/dp_group_1_latency_analyze.log",
       # "/Users/duling/Desktop/code/Geo_All2All/output/key_result/no_group_just_max_1_latency_analyze.log",
    
    ]
    # 生成图表
    plot_results(file_paths)