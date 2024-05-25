#pragma once
#include <iostream>
#include <vector>
#include <assert.h>
#include <cstdint>
#include <fstream>
#include <istream>
#include <ostream>

class delay_martix{
    public:
    delay_martix(int _num_node) : num_node(_num_node){
        // martix.resize(num_node*(num_node-1)/2);
    }
    // delay_martix(int _num_node, std::vector<double> &data){
    //     martix.resize(num_node*num_node);
    //     std::copy(data.begin(), data.end(), martix.begin());
    // }
    double get_delay_ij(int i, int j){ 
        assert(i < num_node && j < num_node);
        return martix[i*num_node+j];
    }
    void set_delay_ij(int i, int j, double value){
        assert(i < num_node && j < num_node);
        martix[i*num_node+j] = value;
    }
    void load(std::string path){
        std::ifstream infile(path);
        double tmp;
        while(infile >> tmp){
            martix.push_back(tmp);
        }
    }
    
    private:
    int num_node;
    std::vector<double> martix;
};

class group_id{
    public:
    group_id(){
        // group.resize(num_node);
    }
    // double get_group_id(int i){
    //     assert(i >= num_node);
    //     return group[i];
    // }
    int get_num_group(){
        return num_group;
    }
    // void set_group_id(int i, int value){
    //     assert(i >= num_node);
    //     group[i] = value;
    // }
    int get_group_centerid(int gid){
        return centerid[gid];
    }
    void load(std::string path){
        std::ifstream infile(path);
        infile >> num_group;
        group_member.resize(num_group);
        centerid.resize(num_group);
        int _group_total_member;
        for(int i = 0; i < num_group; i++){
            infile >> _group_total_member;
            group_member_number.emplace_back(_group_total_member);
            int _group_id_number;
            for(int j = 0; j < _group_total_member; j++){
                infile >> _group_id_number;
                group_member[i].emplace_back(_group_id_number);
            }
            int _centerid;
            infile >> _centerid;
            centerid[i] = _centerid;
        }
    }
    /*
    * example: group id: 1, return [1, 2, 3, 4, 5], where[1,2,3,4,5] belongs to group 1
    */
    std::vector<int>& get_group_member(int _group_id){
        //return member of target group_id
        return group_member[_group_id];
    }
    
    private:
    int num_node;
    int num_group;
    std::vector<int> group_member_number;
    // std::vector<int> group;
    std::vector<int> centerid;
    std::vector<std::vector<int>> group_member;
};

enum operator_type {WRITE, READ, UPDATE, DELETE};


/*
* a update 1  :  flag=update, key=a, value=1 key: mempry address, value: int, float
*/
// template <class KeyT, class ValueT>
// class operator{
//     public:
//     operator(operator_type _flag, KeyT _key, Value value_) : flag(_flag), key(_key), value(_value);
//     operator_type get_flag(){ return flag };
//     KeyT get_key(){ return key; }
//     ValueT get_value(){ return value; }
//     private:
//     operator_type flag;
//     KeyT key;
//     ValueT value;
// };

// template <class KeyT, class ValueT>
// class operator_set{
//     public:
//     operator_set(){}
//     operator_set(uint64_t _total_number) : total_number(_total_number){ set.resize(total_number); }
//     void push_back(operator<KeyT, ValueT> &op){
//         set.emplace_back(op);
//     }
//     private:
//     std::vector<operator<KeyT, ValueT>> set;
//     uint64_t total_number;
// }




