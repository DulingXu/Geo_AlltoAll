import numpy as np
import os

def floyd_warshall(matrix):
    N = len(matrix)
    dist = np.array(matrix)
    next_node = np.full((N, N), -1)

    for i in range(N):
        for j in range(N):
            if i != j and matrix[i][j] != np.inf:
                next_node[i][j] = j

    for k in range(N):
        for i in range(N):
            for j in range(N):
                if dist[i][k] + dist[k][j] < dist[i][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]
                    next_node[i][j] = next_node[i][k]

    return dist, next_node

def print_paths(matrix, dist, next_node):
    N = len(matrix)
    for i in range(N):
        for j in range(N):
            if i != j and next_node[i][j] != j:
                path = [i]
                intermediate = i
                while intermediate != j:
                    intermediate = next_node[intermediate][j]
                    path.append(intermediate)
                path_str = " --> ".join(map(str, path))
                print(f"节点 {i} 到 节点 {j} 的路径: {path_str}, 共 {len(path) - 1} 跳")

def group_nodes(dist, next_node):
    N = len(dist)
    groups = []
    grouped = [False] * N

    dependency_count = {i: 0 for i in range(N)}

    for i in range(N):
        for j in range(N):
            if i != j and next_node[i][j] != j:
                intermediate = next_node[i][j]
                dependency_count[intermediate] += 1

    for i in range(N):
        if grouped[i]:
            continue

        dependencies = []
        for j in range(N):
            if i != j and next_node[i][j] != j:
                dependencies.append((next_node[i][j], dist[i][j]))

        if dependencies:
            dependencies.sort(key=lambda x: (-dependency_count[x[0]], x[1]))
            aggregation_node = dependencies[0][0]

            if not grouped[aggregation_node]:
                groups.append([aggregation_node])
                grouped[aggregation_node] = True

            for group in groups:
                if group[0] == aggregation_node:
                    group.append(i)
                    grouped[i] = True
                    break
        else:
            groups.append([i])
            grouped[i] = True

    seen_nodes = set()
    for group in groups:
        group[:] = [node for node in group if node not in seen_nodes]
        seen_nodes.update(group)

    return groups

def get_shortest_groups(matrix, output_path):
    dist, next_node = floyd_warshall(matrix)
    print("最短路径矩阵:")
    print(dist)
    print_paths(matrix, dist, next_node)

    groups = group_nodes(dist, next_node)
    print(f"分组结果: {groups}")

    # 保存分组结果到指定路径
    try:
        with open(output_path, 'w') as f:
            for group in groups:
                group_str = " ".join(map(str, group))
                f.write(f"{group_str}\n")
        print(f"分组结果已保存到: {output_path}")
    except Exception as e:
        print(f"保存分组结果时出错: {e}")

def main(latency_matrix, output_path):
    get_shortest_groups(latency_matrix, output_path)

if __name__ == "__main__":
    # 示例路径和文件（根据你的情况调整）
    latency_matrix = [[0, 1, 2], [1, 0, 2], [2, 2, 0]]
    output_path = "/Users/duling/Desktop/code/Geo_All2All/output/group_result/shortestt"

    main(latency_matrix, output_path)