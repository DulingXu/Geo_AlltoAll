import sys

def read_group_result(file_path):
    """
    从指定的文件路径读取分组结果
    :param file_path: 分组结果文件路径
    :return: 分组结果列表
    """
    try:
        group_result = []
        with open(file_path, 'r') as f:
            for line in f:
                group = list(map(int, line.strip().split()))
                group_result.append(group)
        return group_result
    except Exception as e:
        print(f"读取分组结果时出错: {e}")
        return None

def main(output_path):
    group_result = read_group_result(output_path)
    if group_result:
        print(group_result)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        output_path = sys.argv[1]
    else:
        output_path = "/Users/duling/Desktop/code/Geo_All2All/output/group_result/shortest/shortest_matrix_0.txt"

    main(output_path)