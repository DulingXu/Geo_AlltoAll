import zmq

context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:5555")

print("Sending request...")
socket.send(b"Hello, server")
message = socket.recv()
print(f"Received reply: {message}")