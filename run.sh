# exec=./single_all_to_all
# $exec 6 ./dataset/delay_matrix.txt ./dataset/group_id.txt

# 编译
clang++ -std=c++11 -g -I./include src/single_all_to_all.cpp -o single_all_to_all

# 检查编译是否成功
if [ $? -ne 0 ]; then
    echo "编译失败"
    exit 1
fi

# 运行
exec=./single_all_to_all
$exec 6 ./dataset/delay_matrix.txt ./dataset/group_id.txt

# 检查运行是否成功
if [ $? -ne 0 ]; then
    echo "运行失败"
    exit 1
fi

echo "运行成功"
