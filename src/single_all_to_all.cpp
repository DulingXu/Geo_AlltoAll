#include <iostream>
#include <vector>
#include <fstream>
#include <limits>

using namespace std;

void printPath(const vector<vector<int>>& next, int i, int j) {
    if (next[i][j] == -1) {
        cout << "No path";
        return;
    }
    cout << i;
    while (i != j) {
        i = next[i][j];
        cout << " -> " << i;
    }
}

int main() {
    ifstream infile("../dataset/delay_matrix.txt");
    if (!infile) {
        cerr << "Error opening file!" << endl;
        return 1; // 退出程序
    }

    ofstream outfile("../dataset/new_delay_matrix.txt");
    if (!outfile) {
        cerr << "Error opening output file!" << endl;
        return 1; // 退出程序
    }

    while (true) {
        int N;
        infile >> N;
        if (infile.eof()) break; // 检查文件末尾

        vector<vector<int>> dist(N, vector<int>(N, numeric_limits<int>::max()));
        vector<vector<int>> next(N, vector<int>(N, -1));

        // 读取延迟矩阵
        for (int i = 0; i < N; i++) {
            for (int j = 0; j < N; j++) {
                infile >> dist[i][j];
                if (dist[i][j] < numeric_limits<int>::max() && i != j) {
                    next[i][j] = j;  // 设置下一节点
                }
            }
        }

        // Floyd-Warshall 算法
        for (int k = 0; k < N; k++) {
            for (int i = 0; i < N; i++) {
                for (int j = 0; j < N; j++) {
                    if (dist[i][k] != numeric_limits<int>::max() && dist[k][j] != numeric_limits<int>::max()) {
                        if (dist[i][j] > dist[i][k] + dist[k][j]) {
                            dist[i][j] = dist[i][k] + dist[k][j];
                            next[i][j] = next[i][k];  // 更新下一节点
                        }
                    }
                }
            }
        }

        // 剪枝：找出未使用的边并生成新的时延矩阵
        vector<vector<string>> new_dist(N, vector<string>(N, "null"));
        vector<vector<bool>> used(N, vector<bool>(N, false));

        // 标记使用过的边
        for (int i = 0; i < N; i++) {
            for (int j = 0; j < N; j++) {
                if (i != j && dist[i][j] < numeric_limits<int>::max()) {
                    int current = i;
                    while (current != j) {
                        used[current][next[current][j]] = true;
                        current = next[current][j];
                    }
                    used[i][j] = true; // 直接标记当前边
                }
            }
        }

        // 更新新的时延矩阵，未使用的边设置为 null，并输出被剪掉的边
        for (int i = 0; i < N; i++) {
            for (int j = 0; j < N; j++) {
                if (i == j) {
                    new_dist[i][j] = "0";  // 自己到自己的距离为0
                } else if (used[i][j]) {
                    new_dist[i][j] = to_string(dist[i][j]);  // 记录最短路径的时延
                } else {
                    // 输出被剪掉的边的原始值
                    cout << "Node " << i << " ---> " << j << ", delay = " << dist[i][j] << " is cut." << endl;
                    new_dist[i][j] = "null";  // 将未使用的边设置为 null
                }
            }
        }

        // 写入新的延迟矩阵到文件
        outfile << N << endl; // 输出新的组的节点数量
        for (const auto& row : new_dist) {
            for (const auto& val : row) {
                outfile << val << " ";
            }
            outfile << endl;
        }
    }

    cout << "New delay matrices written to new_delay_matrix.txt" << endl;

    infile.close();
    outfile.close();
    return 0;
}
