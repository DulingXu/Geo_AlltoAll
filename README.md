# ALL-to-ALL

## Get started

This is the benchmark repo for all to all test.

To use this repo, `make` and `bash run.sh`.


## Input format

``shell
$exec <num_node> <matrix_path> <group_path>
``

* delay_matrix, eg. for a 6*6 matrix

```shell
0 1 3 4 5 6
1 0 2 3 4 5
3 2 0 3 4 6
4 3 3 0 2 3
5 4 4 2 0 9
6 5 6 4 9 0
```

* group_id, eg, for a 6 node group

```shell
2 // number of total group
3 // total number of group 1
0 
1
2
2 // center id
3 // total number of group 1
3
4
5
4 // center id
```

// 修改时延加和逻辑 算出单论时延长度

// 修改节点分组逻辑 显示表示

// 增加时延文件 写一个多伦的时延计算 并且输出简单图像


'''shell
project/
├── include/       # 头文件目录，存放项目的头文件 (.hpp, .h)
│   ├── type.hpp
│   ├── io.hpp
├── src/           # 源代码目录，存放项目的源代码文件 (.cpp, .c)
│   └── single_all_to_all.cpp
├── dataset/       # 数据集目录，存放输入数据文件
│   ├── delay_matrix.txt
│   ├── group_id.txt
├── build/         # 编译输出目录，存放编译生成的文件（可选）
├── run.sh         # 执行脚本文件
└── Makefile       # 构建脚本或项目配置文件