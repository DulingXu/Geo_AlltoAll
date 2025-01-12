import zmq

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5555")

print("Server is listening on port 5555...")
message = socket.recv()
print(f"Received message: {message}")
socket.send(b"Message received")