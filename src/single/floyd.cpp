#include <iostream>
#include <vector>
#include <fstream>
#include <sstream>
#include <limits>
#include <string>
#include <stdexcept>
#include <algorithm>

// 定义一个大数作为无穷大
const double INF = std::numeric_limits<double>::infinity();

// 打印矩阵（用于调试）
void print_matrix(const std::vector<std::vector<double>>& matrix) {
    for (const auto& row : matrix) {
        for (const auto& value : row) {
            if (value == INF) {
                std::cout << "-1 ";
            } else {
                std::cout << value << " ";
            }
        }
        std::cout << std::endl;
    }
}

// 读取 JSON 文件并解析为矩阵
std::vector<std::vector<double>> load_delay_matrix(const std::string& matrix_path) {
    std::ifstream infile(matrix_path);
    std::vector<std::vector<double>> matrix;
    std::string line;

    if (!infile.is_open()) {
        std::cerr << "Error opening file: " << matrix_path << std::endl;
        return matrix;
    }

    while (std::getline(infile, line)) {
        // 跳过包含 [ 和 ] 的行
        if (line.find('[') != std::string::npos || line.find(']') != std::string::npos) {
            continue;
        }

        std::vector<double> matrix_row;
        std::stringstream ss(line);
        std::string value;

        // 处理当前行中的每个值
        while (std::getline(ss, value, ',')) {  // 用逗号分隔
            // 移除引号
            value.erase(std::remove(value.begin(), value.end(), '\"'), value.end());

            try {
                if (!value.empty()) {
                    matrix_row.push_back(std::stod(value));  // 将字符串转换为 double
                }
            } catch (const std::invalid_argument& e) {
                std::cerr << "Conversion error: " << e.what() << " for value: " << value << std::endl;
            }
        }

        if (!matrix_row.empty()) {
            matrix.push_back(matrix_row);
        }
    }

    std::cout << "Matrix loaded from file:" << std::endl;
    print_matrix(matrix); // 调试：打印读取的矩阵
    std::cout << "Matrix size: " << matrix.size() << "x" << (matrix.empty() ? 0 : matrix[0].size()) << std::endl;

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
    std::ofstream outfile(file_path, std::ios::app); // 以追加方式打开文件
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

int main() {
    const std::string matrix_path = "/Users/duling/Desktop/code/Geo_All2All/dataset/reallset/latency/1/matrix_0.json";
    const std::string output_path = "/Users/duling/Desktop/code/Geo_All2All/output/result.txt"; // 输出路径

    // 读取延迟矩阵
    std::vector<std::vector<double>> delay_matrix = load_delay_matrix(matrix_path);

    if (delay_matrix.empty()) {
        std::cerr << "Error: Loaded matrix is empty." << std::endl;
        return -1;
    }

    // 执行Floyd-Warshall算法
    std::vector<std::vector<double>> shortest_paths = floyd_warshall(delay_matrix, delay_matrix.size());

    // 将结果保存到文件
    save_matrix_to_file(shortest_paths, output_path);

    std::cout << "Shortest path matrix has been saved to " << output_path << std::endl;

    return 0;
}