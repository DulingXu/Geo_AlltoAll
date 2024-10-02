from zmq_use.aggregation_node import aggregate
from zmq_use.normal_node import NormalNode

def main():
    aggregate()
    node = NormalNode()
    node.send_message()

if __name__ == "__main__":
    main()