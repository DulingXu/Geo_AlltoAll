import zmq

def normal_node_send_to_aggregation(aggregation_ip):
    context = zmq.Context()

    try:
        # PUSH socket to send message to aggregation node
        push_socket = context.socket(zmq.PUSH)
        push_socket.connect(f"tcp://{aggregation_ip}:5557")  # 连接聚合节点

        # 发送消息到聚合节点
        message = "Message from normal node"
        try:
            push_socket.send_string(message)
            print(f"Sent to aggregation node: {message}")
        except zmq.ZMQError as e:
            print(f"Failed to send message: {e}")

    #确保套接字和上下文 关闭和终止，防泄漏
    finally:
        push_socket.close()
        context.term()

# 示例，假设聚合节点的 IP 是 192.168.0.2
if __name__ == "__main__":
    normal_node_send_to_aggregation("192.168.0.2")