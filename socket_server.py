import socket

HOST = "192.168.56.1"
PORT = 5000

PORT = 5000

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen(1)

print("Waiting for sensor connection on port 5000...")

conn, addr = server.accept()
print("Connected:", addr)

while True:
    data = conn.recv(1024)
    if not data:
        break
    print("Sensor data:", data.decode())

conn.close()
server.close()
