import re
from collections import defaultdict

# 解析日志文件，统计中间节点的使用频率和剪枝边的频率
def analyze_log(log_file):
    intermediate_node_count = defaultdict(int)  # 用于记录中间节点出现的频率
    cut_edge_count = defaultdict(int)  # 用于记录剪枝边出现的频率
    total_paths_with_intermediate = 0  # 总的路径数（包含中间节点）
    total_cut_edges = 0  # 总的剪枝边数
    
    with open(log_file, 'r') as f:
        lines = f.readlines()
    
    for line in lines:
        # 解析 shortest path 的信息，找到中间节点
        path_match = re.match(r'(\d+)-->(\d+):\s+([\d\-\>]+)', line)
        if path_match:
            path = path_match.group(3).split("-->")
            if len(path) > 2:
                total_paths_with_intermediate += 1  # 有中间节点的路径
                # 中间节点存在
                intermediate_nodes = path[1:-1]
                for node in intermediate_nodes:
                    intermediate_node_count[int(node)] += 1

        # 解析剪枝边的信息
        cut_edge_match = re.match(r'cut:(\d+)-->(\d+)', line)
        if cut_edge_match:
            total_cut_edges += 1  # 记录剪枝边的总数
            node1 = int(cut_edge_match.group(1))
            node2 = int(cut_edge_match.group(2))
            cut_edge_count[(node1, node2)] += 1
    
    return intermediate_node_count, cut_edge_count, total_paths_with_intermediate, total_cut_edges

# 统计最高频率的中间节点和剪枝边，输出为百分比
def summarize_statistics(intermediate_node_count, cut_edge_count, total_paths_with_intermediate, total_cut_edges):
    print("Most frequently used intermediate nodes (in percentage):")
    if total_paths_with_intermediate > 0:
        sorted_nodes = sorted(intermediate_node_count.items(), key=lambda x: x[1], reverse=True)
        for node, count in sorted_nodes:
            percentage = (count / total_paths_with_intermediate) * 100
            print(f"Node {node}: {percentage:.2f}% ({count}/{total_paths_with_intermediate})")
    else:
        print("No paths with intermediate nodes found.")
    
    print("\nMost frequently cut edges (in percentage):")
    if total_cut_edges > 0:
        sorted_edges = sorted(cut_edge_count.items(), key=lambda x: x[1], reverse=True)
        for edge, count in sorted_edges:
            percentage = (count / total_cut_edges) * 100
            print(f"Edge {edge[0]}-->{edge[1]}: {percentage:.2f}% ({count}/{total_cut_edges})")
    else:
        print("No cut edges found.")

# 主函数，读取日志并进行分析
def main(log_file):
    intermediate_node_count, cut_edge_count, total_paths_with_intermediate, total_cut_edges = analyze_log(log_file)
    summarize_statistics(intermediate_node_count, cut_edge_count, total_paths_with_intermediate, total_cut_edges)

# 替换为实际日志文件的路径
log_file = '/Users/duling/Desktop/code/Geo_All2All/output/new_delay_matrix/new_delay.log'

# 调用主函数
main(log_file)