import zmq
import threading

# 组内通信，普通节点 --> 聚合节点
# 接收来自普通节点的消息
def aggregation_node_receive_from_normal():
    context = zmq.Context()

    # PULL socket to receive messages from normal nodes
    pull_socket = context.socket(zmq.PULL)
    pull_socket.bind("tcp://*:5557")  # 绑定到端口接收普通节点的消息

    while True:
        message = pull_socket.recv_string()
        print(f"Aggregation node received from normal node: {message}")
        # 可以进一步处理消息，或者将其转发给其他聚合节点

# 发布消息给其他聚合节点
def aggregation_node_send_to_other_aggregation():
    context = zmq.Context()

    # PUB socket to publish message to other aggregation nodes
    pub_socket = context.socket(zmq.PUB)
    pub_socket.bind("tcp://*:5558")  # 绑定端口用于发布消息

    while True:
        # 示例，定期发送消息到其他聚合节点
        message = "Message from this aggregation node"
        pub_socket.send_string(message)
        print(f"Published to other aggregation nodes: {message}")

# 组间通信，聚合节点间通信
# 接收来自其他聚合节点的消息
def aggregation_node_receive_from_other_aggregation():
    context = zmq.Context()

    # SUB socket to subscribe to other aggregation nodes' messages
    sub_socket = context.socket(zmq.SUB)
    sub_socket.connect("tcp://<other_aggregation_ip>:5558")  # 连接其他聚合节点
    sub_socket.setsockopt_string(zmq.SUBSCRIBE, "")  # 订阅所有消息

    while True:
        message = sub_socket.recv_string()
        print(f"Received from other aggregation node: {message}")

# 使用多线程并行处理不同任务
if __name__ == "__main__":
    # 启动接收普通节点消息的线程
    recv_thread = threading.Thread(target=aggregation_node_receive_from_normal)
    recv_thread.start()

    # 启动发送消息给其他聚合节点的线程
    send_thread = threading.Thread(target=aggregation_node_send_to_other_aggregation)
    send_thread.start()

    # 启动接收来自其他聚合节点消息的线程
    recv_other_thread = threading.Thread(target=aggregation_node_receive_from_other_aggregation)
    recv_other_thread.start()

    # 等待线程结束
    recv_thread.join()
    send_thread.join()
    recv_other_thread.join()