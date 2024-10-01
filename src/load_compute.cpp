#include <iostream>
#include <vector>
#include <fstream>
#include <sstream>
#include <limits>
#include <filesystem>
#include <string>

const double INF = std::numeric_limits<double>::infinity();

// 读取延迟矩阵文件（手动解析）
std::vector<std::vector<double>> load_delay_matrix(const std::string& matrix_path) {
    std::ifstream infile(matrix_path);
    std::vector<std::vector<double>> matrix;

    std::string line;
    while (std::getline(infile, line)) {
        if (line.empty()) continue;  // 跳过空行

        std::vector<double> matrix_row;
        std::stringstream ss(line);
        std::string value;
        
        while (std::getline(ss, value, ',')) { // 按逗号分隔
            matrix_row.push_back(std::stod(value)); // 转换为 double
        }
        matrix.push_back(matrix_row);
    }
    
    return matrix;
}

// 其他代码保持不变...

int main() {
    const std::string directory_path = "/Users/duling/Desktop/code/Geo_All2All/dataset/realset/latency";
    std::vector<std::string> json_files;

    // 遍历目录中的所有.json文件
    for (const auto& entry : std::filesystem::directory_iterator(directory_path)) {
        if (entry.path().extension() == ".json") {
            json_files.push_back(entry.path().string());
        }
    }

    // 处理每个文件
    for (const std::string& json_file : json_files) {
        // 读取延迟矩阵
        std::vector<std::vector<double>> delay_matrix = load_delay_matrix(json_file);

        // 输出文件路径
        std::string output_file = directory_path + "/output_" + std::filesystem::path(json_file).filename().string();

        // 保存加载的矩阵到临时文件，以供floyd.cpp使用
        std::ofstream temp_file("temp_matrix.txt");
        for (const auto& row : delay_matrix) {
            for (const auto& value : row) {
                temp_file << value << " ";
            }
            temp_file << std::endl;
        }
        temp_file.close();

        // 调用计算最短路径
        compute_shortest_paths("temp_matrix.txt", output_file);

        std::cout << "Shortest path matrix for " << json_file << " has been saved to " << output_file << std::endl;
    }

    return 0;
}
