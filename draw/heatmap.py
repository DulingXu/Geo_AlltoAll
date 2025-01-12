import os
import json
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

def load_group_file(file_path):
    """从 JSON 文件加载分组数据"""
    try:
        with open(file_path, 'r') as f:
            group_data = json.load(f)
        return group_data
    except json.JSONDecodeError as e:
        print(f"解析JSON文件 {file_path} 时出错: {e}")
        return []
    except Exception as e:
        print(f"读取文件 {file_path} 时出错: {e}")
        return []

def calculate_path_usage(group_data, N):
    """
    根据分组数据计算路径使用频率矩阵
    :param group_data: 分组情况
    :param N: 总节点数
    :return: 路径使用频率矩阵 (NxN)
    """
    path_usage_frequency = np.zeros((N, N))

    # 遍历每个分组，计算路径使用频率
    for group in group_data:
        if len(group) == 0:
            continue  # 跳过空分组
        
        group_leader = group[0]  # 第一个元素是组长
        group_size = len(group)
        
        # 组内路径计算
        for i in range(group_size):
            src = group[i]
            if src != group_leader:
                # 组员到组长路径次数为 2
                path_usage_frequency[src][group_leader] += 2
                path_usage_frequency[group_leader][src] += 2

            for j in range(i + 1, group_size):
                dst = group[j]
                if src != group_leader and dst != group_leader:
                    # 组员之间路径次数为 1
                    path_usage_frequency[src][dst] += 1
                    path_usage_frequency[dst][src] += 1

    # 组长之间路径次数为 2
    for i in range(len(group_data)):
        leader1 = group_data[i][0]
        for j in range(i + 1, len(group_data)):
            leader2 = group_data[j][0]
            path_usage_frequency[leader1][leader2] += 2
            path_usage_frequency[leader2][leader1] += 2

    return path_usage_frequency

def calculate_node_usage(group_data, N, num_leaders):
    """
    根据分组数据计算节点使用频次
    :param group_data: 分组情况
    :param N: 总节点数
    :param num_leaders: 组长的数量
    :return: 节点使用频次矩阵 (Nx轮次)
    """
    node_usage_frequency = np.zeros(N)

    # 遍历每个分组，计算节点使用次数
    for group in group_data:
        if len(group) == 0:
            continue  # 跳过空分组

        group_leader = group[0]  # 组长
        group_size = len(group)

        # 计算组长的使用次数
        if group_size > 1:
            node_usage_frequency[group_leader] += (num_leaders - 1) * 2 + (group_size - 1) * 2
        else:
            node_usage_frequency[group_leader] += (num_leaders - 1) * 2

        # 计算组员的使用次数
        for i in range(1, group_size):
            member = group[i]
            node_usage_frequency[member] += 2 + (group_size - 2)  # 与组长通信 2 次 + 与其他组员的通信

    return node_usage_frequency

def get_total_nodes(directory_path):
    """根据分组文件统计节点总数"""
    json_files = [f for f in os.listdir(directory_path) if f.endswith('.json')]
    all_nodes = set()

    for json_file in json_files:
        file_path = os.path.join(directory_path, json_file)
        group_data = load_group_file(file_path)
        
        # 将所有节点添加到集合中（去重）
        for group in group_data:
            all_nodes.update(group)
    
    return len(all_nodes)

def process_directory(directory_path):
    """处理目录中的所有 .json 分组文件，计算路径使用频率和节点使用频次"""
    # 统计目录下所有分组文件中的节点总数
    N = get_total_nodes(directory_path)
    print(f"统计到的节点总数为: {N}")

    total_path_usage = np.zeros((N, N))
    json_files = [f for f in os.listdir(directory_path) if f.endswith('.json')]
    
    num_rounds = len(json_files)
    node_usage_matrix = np.zeros((N, num_rounds))  # 节点使用矩阵 (节点数 x 轮次)

    for round_index, json_file in enumerate(json_files):
        file_path = os.path.join(directory_path, json_file)
        print(f"处理文件: {file_path}")
        group_data = load_group_file(file_path)
        
        # 计算路径使用频率
        path_usage_frequency = calculate_path_usage(group_data, N)
        total_path_usage += path_usage_frequency  # 累加路径使用次数
        
        # 计算节点使用频次
        num_leaders = len([group[0] for group in group_data if len(group) > 0])
        node_usage_frequency = calculate_node_usage(group_data, N, num_leaders)
        node_usage_matrix[:, round_index] = node_usage_frequency  # 保存每轮的节点使用频次

    return total_path_usage, node_usage_matrix, num_rounds

def save_heatmap(data, output_dir, output_filename, x_label, y_label, cbar_label, xtick_labels, cmap, normalize=False):
    """保存热力图并归一化"""
    plt.figure(figsize=(10, 8))  # 增大图的尺寸

    if normalize:
        # 归一化，将数据范围调整到0-100
        data = (data / np.max(data)) * 100

    heatmap = sns.heatmap(
        data, 
        annot=False,  
        fmt=".0f", 
        cmap=cmap,  
        linewidths=.8, 
        cbar_kws={"label": cbar_label},
        vmin=0, vmax=100  # 设置归一化后的范围 0 到 100
    )

    # 增大横纵坐标数字的字体大小
    plt.xticks(fontsize=20)
    plt.yticks(fontsize=20)

    heatmap.set_xticks(np.arange(len(xtick_labels)))
    heatmap.set_xticklabels(xtick_labels)

    plt.xlabel(x_label, fontsize=28)
    plt.ylabel(y_label, fontsize=28)

    # 调整 colorbar 标签的字体大小
    colorbar = heatmap.collections[0].colorbar
    colorbar.ax.tick_params(labelsize=20)  
    colorbar.set_label(cbar_label, size=24)  

    output_path = os.path.join(output_dir, output_filename)
    plt.subplots_adjust(left=0.12, right=0.92, bottom=0.14, top=0.92)    
    plt.savefig(output_path)
    plt.close()
    print(f"热力图已保存到: {output_path}")

def main():
    # 处理指定的路径
    directory_path = "/Users/duling/Desktop/code/Geo_All2All/output/group_result/dp_group_1_latency"
    
    # 处理目录下的所有分组文件，计算路径使用频率和节点使用频次
    total_path_usage, node_usage_matrix, num_rounds = process_directory(directory_path)

    # 输出路径使用次数总体相加的结果
    print("路径使用次数汇总 (每条路径的总次数):")
    N = total_path_usage.shape[0]  # 获取节点总数
    total_usage = 0  # 初始化总使用次数

    for i in range(N):
        for j in range(i + 1, N):  # 只考虑 (i, j) 的上三角
            path_usage = total_path_usage[i, j]
            print(f"路径 ({i} -> {j}) 使用次数: {path_usage}")
            total_usage += path_usage  # 累加路径使用次数

    # 输出所有路径的总使用次数
    print(f"所有路径的总使用次数: {total_usage}")

    # 获取最后一个目录名称作为热力图文件名的一部分
    last_directory_name = os.path.basename(os.path.normpath(directory_path))

    # 保存路径使用频率热力图 (使用默认的Blues colormap)，并归一化为 0-100
    output_filename = f"0-{last_directory_name}-heatmap.pdf"
    save_heatmap(total_path_usage, directory_path, output_filename, "Node Number", "Node Number", "Normalized Usage Frequency (%)", range(total_path_usage.shape[0]), cmap="Blues", normalize=True)

    # 保存节点使用频次热力图 (使用更深颜色的colormap，如'YlOrRd')
    output_filename_node = f"1-{last_directory_name}-heatmap.pdf"
    save_heatmap(node_usage_matrix, directory_path, output_filename_node, "Rounds", "Node Number", "Node Usage Frequency", xtick_labels=range(0, num_rounds, 10000), cmap="YlOrRd")  # Show every 100th label
    
    plt.xticks([])  # 隐藏 x 轴刻度标签

if __name__ == "__main__":
    main()
