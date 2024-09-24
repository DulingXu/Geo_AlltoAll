#pragma once
#include <iostream>
#include <vector>
#include <cassert>
#include <cstdint>
#include <fstream>
#include <istream>
#include <ostream>
#include <algorithm>

class delay_matrix {
public:
    delay_matrix(int _num_node) : num_node(_num_node), matrix(_num_node * _num_node, 0.0) {}

    double get_delay_ij(int i, int j) const {
        assert(i >= 0 && i < num_node && j >= 0 && j < num_node);
        return matrix[i * num_node + j];
    }

    void load(const std::string& path) {
        std::ifstream infile(path);
        if (!infile) {
            throw std::runtime_error("Unable to open file: " + path);
        }
        double tmp;
        while (infile >> tmp) {
            matrix.push_back(tmp);
        }
    }

private:
    int num_node;
    std::vector<double> matrix;
};

class group_id {
public:
    group_id() : num_group(0) {}

    int get_num_group() const {
        return num_group;
    }

    int get_group_centerid(int gid) const {
        assert(gid >= 0 && gid < num_group);
        return centerid[gid];
    }

    // std::vector<int>& get_group_member(int _group_id) const {
    //     assert(_group_id >= 0 && _group_id < num_group);
    //     return group_member[_group_id];
    // }
    
    const std::vector<int>& get_group_member(int _group_id) const {
        assert(_group_id >= 0 && _group_id < num_group);
        return group_member[_group_id];
    }

    void load(const std::string& path) {
        std::ifstream infile(path);
        if (!infile) {
            throw std::runtime_error("Unable to open file: " + path);
        }
        infile >> num_group;
        group_member.resize(num_group);
        centerid.resize(num_group);
        int _group_total_member;
        for (int i = 0; i < num_group; i++) {
            infile >> _group_total_member;
            group_member_number.emplace_back(_group_total_member);
            int _group_id_number;
            for (int j = 0; j < _group_total_member; j++) {
                infile >> _group_id_number;
                group_member[i].emplace_back(_group_id_number);
            }
            int _centerid;
            infile >> _centerid;
            centerid[i] = _centerid;
        }
    }

    std::vector<int> get_all_center_ids() const {
        return centerid;
    }

private:
    int num_group;
    std::vector<int> group_member_number;
    std::vector<int> centerid;
    std::vector<std::vector<int>> group_member;
};

enum operator_type { WRITE, READ, UPDATE, DELETE };

// Template classes for operator and operator_set can be uncommented and implemented as needed.
/**
 * @class operator
 * @brief Template class to represent an operator.
 */
// template <class KeyT, class ValueT>
// class operator {
// public:
//     operator(operator_type _flag, KeyT _key, ValueT _value) : flag(_flag), key(_key), value(_value) {}
//     operator_type get_flag() { return flag; }
//     KeyT get_key() { return key; }
//     ValueT get_value() { return value; }
// private:
//     operator_type flag;
//     KeyT key;
//     ValueT value;
// };

/**
 * @class operator_set
 * @brief Template class to represent a set of operators.
 */
// template <class KeyT, class ValueT>
// class operator_set {
// public:
//     operator_set(uint64_t _total_number) : total_number(_total_number) { set.resize(total_number); }
//     void push_back(operator<KeyT, ValueT>& op) { set.emplace_back(op); }
// private:
//     std::vector<operator<KeyT, ValueT>> set;
//     uint64_t total_number;
// };
