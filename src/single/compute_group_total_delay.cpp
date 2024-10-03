#include "../include/type.hpp" // 包含定义 delay_matrix 和 group_id 的头文件
#include <vector>
#include <algorithm> // For std::max
#include <iostream>  // For std::cout


// 计算同一组内的组内最大时延
double compute_max_intra_group_delay(const delay_matrix& dm, const group_id& group, int group_id) {
    int center_id = group.get_group_centerid(group_id);

    // 计算send_delay
    double max_send_delay = 0;
    const std::vector<int>& group_members = group.get_group_member(group_id);
    for (int member_id : group_members) {
        if (member_id == center_id) continue;
        double delay = dm.get_delay_ij(member_id, center_id);
        max_send_delay = std::max(max_send_delay, delay);
    }
    return max_send_delay;
}

// 计算第i组传输时延的总时延
double compute_group_total_delay(const delay_matrix& dm, const group_id& group, int group_id) {
    int center_id = group.get_group_centerid(group_id);

    // 计算组内最大时延
    double send_delay = compute_max_intra_group_delay(dm, group, group_id);

    // 计算inter_center_delay
    double inter_center_delay = 0;
    std::vector<int> all_center_ids = group.get_all_center_ids();
    for (int other_center_id : all_center_ids) {
        if (other_center_id == center_id) continue;
        double delay = dm.get_delay_ij(center_id, other_center_id);
        inter_center_delay = std::max(inter_center_delay, delay);
    }

    // 计算receive_delay
    double receive_delay = 0;
    for (int i = 0; i < group.get_num_group(); ++i) {
        if (i == group_id) continue;
        double max_group_delay = compute_max_intra_group_delay(dm, group, i);
        receive_delay = std::max(receive_delay, max_group_delay);
    }

    // 计算总时延
    double total_delay = send_delay + inter_center_delay + receive_delay;

    // 打印total_delay结果
    std::cout << "Group " << group_id + 1 << " total delay: " << total_delay << std::endl;

    return total_delay;
}

int main(int argc, char **argv) {
    if (argc != 4) {
        printf("Usage: %s num_node matrix_path group_path\n", argv[0]);
        return 0;
    }

    // Load data
    int num_node = atoi(argv[1]); // 将命令行参数转换为整数，表示节点的数量
    delay_matrix dm(num_node); // 创建 delay_matrix 对象
    std::string matrix_path = argv[2]; // 获取存储延迟矩阵的文件路径
    dm.load(matrix_path); // 从文件加载延迟矩阵数据

    group_id group; // 创建 group_id 对象
    std::string group_path = argv[3]; // 获取存储组数据的文件路径
    group.load(group_path); // 从文件加载组数据

    // Compute the physical delay within each group
    int num_group = group.get_num_group(); // 获取组的数量
    std::vector<double> phy_group_delay(num_group); // 创建一个向量存储每个组的物理延迟

    for (int i = 0; i < num_group; ++i) { // 遍历每个组
        phy_group_delay[i] = compute_group_total_delay(dm, group, i);
    }
    // printf("here");
    // 输出每个组的物理延迟
    for (int i = 0; i < num_group; i++) {
        printf("Group %d physical delay: %.4lf\n", i + 1, phy_group_delay[i]);
    }

    return 0;
}
