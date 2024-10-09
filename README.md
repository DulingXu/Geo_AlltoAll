# ALL-to-ALL

# Attention
This project is a modified version of [pyzmq](https://github.com/zeromq/pyzmq), which is licensed under the MIT License. Modifications include [……] to support my research .

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
5 4 4 2 0 8
6 5 6 4 8 0
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

// 增加时延文件 写一个多轮的时延计算


```shell
├── README.md
├── dataset
│   ├── delay_matrix.txt
│   ├── group_id.txt
│   ├── new_delay_matrix.txt
│   ├── operator_set.txt
│   └── reallset
├── draw
│   ├── 1.py
│   └── box.py
├── include
│   ├── io.hpp
│   ├── json
│   ├── nlohmann
│   └── type.hpp
├── makefile
├── other
│   ├── analyze.py
│   ├── analyze2.py
│   ├── count.py
│   ├── generate.py
│   └── test.py
├── output
│   ├── get_best_group_logs
│   ├── get_best_makespan_logs
│   ├── group_result
│   ├── key_result
│   ├── logs
│   ├── makespan_result
│   ├── new_delay_matrix
│   ├── shortest_path
│   ├── tmp
│   ├── total_result
│   └── us
├── requirements.txt
├── single_all_to_all.dSYM
│   └── Contents
├── src
│   ├── __pycache__
│   ├── best_group_detecttion.py
│   ├── dp_group.py
│   ├── get_group.py
│   ├── get_makespan.py
│   ├── get_makespan_best_group.py
│   ├── kmeans_2_group.py
│   ├── kmeans_4_group.py
│   ├── kmeans_group.py
│   ├── our_group.py
│   ├── our_group_2.py
│   ├── random_group.py
│   ├── run.sh
│   ├── run_best.sh
│   ├── run_get_makespan_#.sh
│   ├── shortest_group.py
│   ├── shortest_group_1.py
│   ├── single
│   └── test.py
├── tests
├── zmq
│   └── pyzmq-26.2.0
└── zmq_use
    ├── __init__.py
    ├── agrregation_node.py
    └── normal_node.py
```