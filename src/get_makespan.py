import os
import json
import numpy as np
import subprocess

MESSAGE_SIZE_MB = 10  # 假设消息大小为10MB

def load_data(file_path):
    """
    从指定的 JSON 文件路径加载数据（NxN 矩阵或 N 数组）。
    """
    if not os.path.exists(file_path):
        print(f"文件路径不存在: {file_path}")
        return None

    try:
        with open(file_path, 'r') as f:
            data = json.load(f)  # 读取 JSON 数据
        array_data = np.array(data, dtype=float)
        
        # 不再强制要求数据为矩阵，因为可能是数组
        return array_data
    except json.JSONDecodeError as e:
        print(f"解析 JSON 文件时出错: {e}")
        return None
    except Exception as e:
        print(f"加载数据时出错: {e}")
        return None

def print_loaded_data(latency_matrix, bandwidth_array, conflict_matrix, num_messages_array, group_result):
    """
    打印所有加载的输入数据和分组情况，确保它们正确读取。
    """
    print("\n---- 加载的输入数据 ----")
    print("时延矩阵 (latency matrix):")
    print(latency_matrix)
    print("\n带宽数组 (bandwidth array):")
    print(bandwidth_array)
    print("\n冲突率矩阵 (conflict rate matrix):")
    print(conflict_matrix)
    print("\n每个节点的消息个数 (number of messages per node):")
    print(num_messages_array)
    print("\n分组情况 (group result):")
    print(group_result)
    print("--------------------------\n")

def calculate_makespan(latency_matrix, bandwidth_array, conflict_matrix, message_size, num_messages_array, group_result):
    """
    计算 makespan 的占位函数。
    :param latency_matrix: 时延矩阵 (NxN)
    :param bandwidth_array: 带宽数组 (N)  （Mbps）
    :param conflict_matrix: 冲突率矩阵 (NxN) (百分比率)
    :param message_size: 消息大小（MB）
    :param num_messages_array: 每个节点发送的消息个数 (N) 
    :param group_result: 从 get_group.py 得到的分组情况
    :return: 假设的 makespan 值
    """
    num_nodes = len(bandwidth_array)  # 节点数量
    total_data_transferred = sum(num_messages_array) * message_size  # 总数据量
    avg_bandwidth = np.mean(bandwidth_array)  # 平均带宽

    # 在计算中结合 group_result 进行处理
    # 假设 makespan 是总数据量除以平均带宽的结果
    makespan = total_data_transferred / avg_bandwidth
    return makespan

def call_get_group(latency_file):
    """
    调用 get_group.py 并获取分组结果。
    假设 get_group.py 将分组结果输出到文件。
    """
    try:
        output_dir = "/Users/duling/Desktop/code/Geo_All2All/output/group_result/shortest"
        
        # 确保输出目录存在
        os.makedirs(output_dir, exist_ok=True)

        # 调用 get_group.py
        result = subprocess.run(
            ["python3", "get_group.py", latency_file],  # 调用 get_group.py，并传递时延文件
            capture_output=True, text=True, check=True
        )

        # 输出调试信息
        if result.returncode != 0:
            raise RuntimeError(f"get_group.py 执行失败，返回代码: {result.returncode}")

        print(f"get_group.py 标准输出: {result.stdout}")
        print(f"get_group.py 标准错误: {result.stderr}")

        # 读取保存的分组结果文件
        group_file = os.path.join(output_dir, "shortest_matrix_0.txt")
        if not os.path.exists(group_file):
            raise FileNotFoundError(f"未找到分组结果文件: {group_file}")

        group_result = []
        with open(group_file, 'r') as f:
            for line in f:
                group = list(map(int, line.strip().split()))  # 将每行数据转为整数列表
                group_result.append(group)

        return group_result
    
    except subprocess.CalledProcessError as e:
        print(f"调用 get_group.py 时出错: {e}")
        return None
    except FileNotFoundError as e:
        print(f"文件未找到错误: {e}")
        return None
    except Exception as e:
        print(f"读取分组结果时出错: {e}")
        return None

def main():
    # 数据文件夹的根路径
    dataset_dir = "/Users/duling/Desktop/code/Geo_All2All/dataset/reallset/"

    # 定义各参数文件夹的路径
    latency_file = os.path.join(dataset_dir, "latency/1", "matrix_0.json")  # 时延 NxN 矩阵
    bandwidth_file = os.path.join(dataset_dir, "bandwidth", "bandwidth_0.json")  # 带宽 N 数组
    conflict_file = os.path.join(dataset_dir, "conflict_rate", "conflict_0.json")  # 冲突率 NxN 矩阵
    num_messages_file = os.path.join(dataset_dir, "num_message", "num_message_0.json")  # 每个节点的消息个数 N 数组

    # 加载数据
    latency_matrix = load_data(latency_file)
    bandwidth_array = load_data(bandwidth_file)
    conflict_matrix = load_data(conflict_file)
    num_messages_array = load_data(num_messages_file)

    # 检查是否所有数据都已加载
    if latency_matrix is None or bandwidth_array is None or conflict_matrix is None or num_messages_array is None:
        print("加载数据失败，退出程序。")
        return

    # 调用 get_group.py 获取分组情况
    group_result = call_get_group(latency_file)
    if group_result is None:
        print("获取分组结果失败，退出程序。")
        return

    # 打印所有加载的输入数据和分组情况
    print_loaded_data(latency_matrix, bandwidth_array, conflict_matrix, num_messages_array, group_result)

# 计算 makespan
def calculate_makespan(latency_matrix, bandwidth_array, conflict_matrix, message_size, num_messages_array, group_result):
    """
    计算 makespan 的逻辑。
    :param latency_matrix: 时延矩阵 (NxN)
    :param bandwidth_array: 带宽数组 (N)
    :param conflict_matrix: 冲突率矩阵 (NxN)
    :param message_size: 消息大小（MB）
    :param num_messages_array: 每个节点发送的消息个数 (N)
    :param group_result: 分组情况
    :return: 最终完成时间 (makespan)
    """
    N = len(latency_matrix)  # 节点数量
    makespan_matrix = np.zeros((N, N))  # 初始化完成时间矩阵
    
    # 计算 单条路径 makespan
    def calculate_single_path_time(src, dst, group_result):
        """
        计算单条路径的完成时间。
        :param src: 源节点
        :param dst: 目标节点
        :param group_result: 分组结果
        :return: 该路径的完成时间
        """
        src_group = None
        dst_group = None
        for group in group_result:
            if src in group:
                src_group = group
            if dst in group:
                dst_group = group
        
        if src_group is None or dst_group is None:
            raise ValueError(f"源节点或目标节点未找到分组: src={src}, dst={dst}")
        
        src_leader = src_group[0]  # 源节点的组长
        dst_leader = dst_group[0]  # 目标节点的组长

        # 1. 计算源节点 -> 源组组长的时间
        if src != src_leader:
            src_to_leader_time = (num_messages_array[src] * message_size) / bandwidth_array[src]  # 组员到组长的发送时间
            src_to_leader_latency = latency_matrix[src][src_leader]  # 组员到组长的时延
        else:
            src_to_leader_time = 0  # 组长自身不需要发送到自己
            src_to_leader_latency = 0

        # 2. 计算源组组长 -> 目标组组长的时间
        leader_to_leader_latency = latency_matrix[src_leader][dst_leader]  # 组长到目标组组长的时延
        leader_send_time = (num_messages_array[src_leader] * message_size) / bandwidth_array[src_leader]  # 组长发送时间

        # 3. 计算目标组组长 -> 目标节点的时间
        if dst != dst_leader:
            leader_to_dst_latency = latency_matrix[dst_leader][dst]  # 组长到目标组员的时延
            dst_receive_time = (num_messages_array[dst] * message_size) / bandwidth_array[dst]  # 组员接收时间
        else:
            leader_to_dst_latency = 0
            dst_receive_time = 0

        # 4. 计算聚合时间：在源组组长上聚合消息
        # 消息量可能因为冲突率减少
        total_aggregated_data = (num_messages_array[src] + num_messages_array[src_leader]) * (1 - conflict_matrix[src][src_leader])
        
        # 计算聚合后的消息发送时间
        aggregation_time = total_aggregated_data / bandwidth_array[src_leader]

        # 最终路径完成时间 = 组内发送时间 + 聚合时间 + 组间发送时间 + 目标组的转发时间
        localmakespan = max(src_to_leader_time + src_to_leader_latency, aggregation_time + \
                   leader_to_leader_latency + leader_send_time) + leader_to_dst_latency + dst_receive_time
        print(f"makespan [{src}][{dst}] 结果: {localmakespan}")
        return localmakespan
        
    # 遍历所有路径，计算每条路径的完成时间
    for i in range(N):
        for j in range(N):
            if i != j:
                makespan_matrix[i][j] = calculate_single_path_time(i, j, group_result)
    
    # 最终完成时间取所有路径中的最大值
    final_makespan = np.max(makespan_matrix)
    return final_makespan

    # # 计算 makespan
    # 用于调试，仅导入数据，不计算
    # makespan = calculate_makespan(latency_matrix, bandwidth_array, conflict_matrix, MESSAGE_SIZE_MB, num_messages_array, group_result)

    # 输出结果
    print(f"Makespan 结果: {makespan}")

def main():
    try:
        # 数据文件夹的根路径
        dataset_dir = "/Users/duling/Desktop/code/Geo_All2All/dataset/reallset/"

        # 定义各参数文件夹的路径
        latency_file = os.path.join(dataset_dir, "latency/1", "matrix_0.json")
        bandwidth_file = os.path.join(dataset_dir, "bandwidth", "bandwidth_0.json")
        conflict_file = os.path.join(dataset_dir, "conflict_rate", "conflict_0.json")
        num_messages_file = os.path.join(dataset_dir, "num_message", "num_message_0.json")

        # 加载数据
        latency_matrix = load_data(latency_file)
        bandwidth_array = load_data(bandwidth_file)
        conflict_matrix = load_data(conflict_file)
        num_messages_array = load_data(num_messages_file)

        # 检查是否所有数据都已加载
        if latency_matrix is None or bandwidth_array is None or conflict_matrix is None or num_messages_array is None:
            print("加载数据失败，退出程序。")
            return

        # 调用 get_group.py 获取分组情况
        group_result = call_get_group(latency_file)
        if group_result is None:
            print("获取分组结果失败，退出程序。")
            return

        # 打印所有加载的输入数据和分组情况
        print_loaded_data(latency_matrix, bandwidth_array, conflict_matrix, num_messages_array, group_result)

        # 计算 makespan
        makespan = calculate_makespan(latency_matrix, bandwidth_array, conflict_matrix, MESSAGE_SIZE_MB, num_messages_array, group_result)

        # 输出结果
        print(f"Makespan 结果: {makespan}")

    except Exception as e:
        print(f"程序执行过程中出错: {e}")
        return

if __name__ == "__main__":
    main()
