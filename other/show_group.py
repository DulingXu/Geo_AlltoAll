import networkx as nx
import matplotlib.pyplot as plt

def plot_grouping(groups, delay_matrix):
    G = nx.Graph()
    
    # 添加节点和组间的连接
    for group in groups:
        aggregator = group[0]  # 聚合节点
        G.add_node(aggregator)  # 确保聚合节点被添加
        for node in group:
            G.add_node(node)  # 确保所有节点被添加
            if node != aggregator:
                G.add_edge(aggregator, node, weight=delay_matrix[aggregator][node])

    # 绘制图
    pos = nx.spring_layout(G)  # 位置布局
    edges = G.edges(data=True)
    
    # 获取延迟权重
    weights = [d['weight'] for (u, v, d) in edges]
    
    # 绘制节点
    nx.draw_networkx_nodes(G, pos, node_color='lightblue', node_size=500)
    
    # 绘制聚合节点
    aggregator_nodes = [group[0] for group in groups]
    nx.draw_networkx_nodes(G, pos, nodelist=aggregator_nodes, node_color='red', node_size=700)
    
    # 绘制边和延迟
    nx.draw_networkx_edges(G, pos, width=[w/10 for w in weights])
    nx.draw_networkx_labels(G, pos, font_size=12)
    
    # 标注边上的延迟
    edge_labels = {(u, v): f'{d["weight"]}' for u, v, d in edges}
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

    plt.title("Node Grouping Visualization")
    plt.show()

# 示例分组和延迟矩阵
groups = [[0, 1], [2, 3], [4]]  # 假设3个组，每个组中的第一个节点是聚合节点
delay_matrix = [
    [0, 10, 20, 30, 40],
    [10, 0, 25, 35, 45],
    [20, 25, 0, 15, 25],
    [30, 35, 15, 0, 20],
    [40, 45, 25, 20, 0]
]

# 调用绘图函数
plot_grouping(groups, delay_matrix)
