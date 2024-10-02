import zmq

def normal_node_send_to_aggregation(aggregation_ip):
    context = zmq.Context()
    
    # PUSH socket to send message to aggregation node
    push_socket = context.socket(zmq.PUSH)
    push_socket.connect(f"tcp://{aggregation_ip}:5557")  # 连接聚合节点

    # 发送消息到聚合节点
    message = "Message from normal node"
    push_socket.send_string(message)
    print(f"Sent to aggregation node: {message}")

# 示例，假设聚合节点的 IP 是 192.168.0.2
normal_node_send_to_aggregation("192.168.0.2")