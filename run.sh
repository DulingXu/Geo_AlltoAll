#只运行compute
#!/bin/bash

# 参数检查
if [ $# -ne 2 ]; then
    echo "Usage: $0 num_node group_path"
    exit 1
fi

NUM_NODE=$1
GROUP_PATH=$2
MATRIX_PATH="dataset/delay_matrix.txt"

# 编译项目
make clean
make

# 运行 compute_group_total_delay 可执行文件
echo "Running compute_group_total_delay..."
./compute_group_total_delay $NUM_NODE $MATRIX_PATH $GROUP_PATH




# #!/bin/bash

# # 参数检查
# if [ $# -ne 2 ]; then
#     echo "Usage: $0 num_node group_path"
#     exit 1
# fi

# NUM_NODE=$1
# GROUP_PATH=$2
# MATRIX_PATH="dataset/delay_matrix.txt"

# # 编译项目
# make clean
# make

# # 运行 compute_group_total_delay 可执行文件
# echo "Running compute_group_total_delay..."
# ./compute_group_total_delay $NUM_NODE $MATRIX_PATH $GROUP_PATH

# # 运行 single_all_to_all 可执行文件
# echo "Running single_all_to_all..."
# ./single_all_to_all $NUM_NODE $MATRIX_PATH $GROUP_PATH




# # exec=./single_all_to_all
# # $exec 6 ./dataset/delay_matrix.txt ./dataset/group_id.txt

# # 编译
# clang++ -std=c++11 -g -I./include src/single_all_to_all.cpp -o single_all_to_all

# # 检查编译是否成功
# if [ $? -ne 0 ]; then
#     echo "编译失败"
#     exit 1
# fi

# # 运行
# exec=./single_all_to_all
# $exec 6 ./dataset/delay_matrix.txt ./dataset/group_id.txt

# # 检查运行是否成功
# if [ $? -ne 0 ]; then
#     echo "运行失败"
#     exit 1
# fi

# echo "运行成功"
