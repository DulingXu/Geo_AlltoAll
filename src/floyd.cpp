#include <iostream>
#include <vector>
#include <fstream>
#include <sstream>
#include <limits>

// 定义一个大数作为无穷大
const double INF = std::numeric_limits<double>::infinity();

// 读取矩阵并计算节点数量
int determine_matrix_size(const std::string& matrix_path) {
    std::ifstream infile(matrix_path);
    std::string line;
    
    if (std::getline(infile, line)) { // 读取第一行
        std::istringstream iss(line);
        std::vector<double> first_row((std::istream_iterator<double>(iss)), std::istream_iterator<double>());
        return first_row.size();  // 返回第一行的元素数量，即矩阵的维度
    }

    return -1; // 如果文件读取失败，返回 -1
}

// 读取延迟矩阵文件
std::vector<std::vector<double>> load_delay_matrix(const std::string& matrix_path, int num_node) {
    std::vector<std::vector<double>> matrix(num_node, std::vector<double>(num_node, INF));
    std::ifstream infile(matrix_path);
    std::string line;
    int row = 0;
    
    while (std::getline(infile, line) && row < num_node) {
        std::istringstream iss(line);
        for (int col = 0; col < num_node; ++col) {
            iss >> matrix[row][col];
        }
        ++row;
    }
    
    return matrix;
}

// Floyd-Warshall算法
std::vector<std::vector<double>> floyd_warshall(const std::vector<std::vector<double>>& matrix, int num_node) {
    std::vector<std::vector<double>> dist = matrix;

    // 初始化对角线为0
    for (int i = 0; i < num_node; ++i) {
        dist[i][i] = 0;
    }

    // 核心算法：逐步更新最短路径
    for (int k = 0; k < num_node; ++k) {
        for (int i = 0; i < num_node; ++i) {
            for (int j = 0; j < num_node; ++j) {
                if (dist[i][k] != INF && dist[k][j] != INF) {
                    dist[i][j] = std::min(dist[i][j], dist[i][k] + dist[k][j]);
                }
            }
        }
    }

    return dist;
}

// 将矩阵保存到文件中
void save_matrix_to_file(const std::vector<std::vector<double>>& matrix, const std::string& file_path) {
    std::ofstream outfile(file_path);
    int num_node = matrix.size();
    
    for (int i = 0; i < num_node; ++i) {
        for (int j = 0; j < num_node; ++j) {
            if (matrix[i][j] == INF) {
                outfile << "-1 "; // 如果是无穷大，则写入-1
            } else {
                outfile << matrix[i][j] << " ";
            }
        }
        outfile << std::endl;
    }
    outfile.close();
}

int main(int argc, char **argv) {
    if (argc != 3) {
        printf("Usage: %s matrix_path output_path\n", argv[0]);
        return 0;
    }

    // 获取输入和输出文件路径
    std::string matrix_path = argv[1]; // 输入文件路径
    std::string output_path = argv[2]; // 输出文件路径

    // 计算节点数量
    int num_node = determine_matrix_size(matrix_path);
    if (num_node == -1) {
        std::cerr << "Error: Failed to read the delay matrix file." << std::endl;
        return -1;
    }

    // 加载延迟矩阵
    std::vector<std::vector<double>> delay_matrix = load_delay_matrix(matrix_path, num_node);

    // 执行Floyd-Warshall算法
    std::vector<std::vector<double>> shortest_paths = floyd_warshall(delay_matrix, num_node);

    // 将结果保存到文件
    save_matrix_to_file(shortest_paths, output_path);

    std::cout << "Shortest path matrix has been saved to " << output_path << std::endl;

    return 0;
}
