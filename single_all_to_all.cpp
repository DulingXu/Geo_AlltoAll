#include <iostream>
#include <type.hpp>
#include <io.hpp>
#include <cstdlib>


//parameter
/*
@num_of_node number of node
@dalay_martix: martix[N*N] 
@group_id: N group_id[N]
@operator: N write_read_set
*/

int main(int argc, char **argv){
    if(argc != 4){
        printf("Usage: %s num_node martix_path group_path\n", argv[0]);
        return 0;
    }
    //load data
    int num_node = atoi(argv[1]);
    delay_martix dm(num_node);
    std::string martix_path = argv[2];
    dm.load(martix_path);
    group_id group;
    std::string group_path = argv[3];
    std::cout << group_path << std::endl;
    group.load(group_path);
    // std::string set_path = argv[4];
    // std::vector<operator_set<int, double>> ops(num_node);
    // ops.load(set_path);

    //compute the physical delay within each group
    int num_group = group.get_num_group();

    std::vector<double> phy_group_delay(num_group);
    for(int i = 0; i < group.get_num_group(); ++i){ // for each group
        int center_id = group.get_group_centerid(i); 
        std::vector<int> group_member = group.get_group_member(i);
        double max_delay = 0;
        for(int i = 0; i < group_member.size(); ++i){
            if(group_member[i] == center_id) continue;
            // get the maximum delay from each group member to center
           max_delay = std::max(max_delay, dm.get_delay_ij(group_member[i], center_id));
        }
        phy_group_delay[i] = max_delay;
    }
    
    for(int i = 0; i < num_group; i++){
        printf("Group %d physical delay: %.4lf\n", i, phy_group_delay[i]);
    }
    return 0;
}