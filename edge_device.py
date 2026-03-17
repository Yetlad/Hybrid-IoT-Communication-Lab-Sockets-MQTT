import socket
import paho.mqtt.client as mqtt

HOST = "192.168.56.1"
PORT = 5000

broker = "broker.emqx.io"
topic = "savonia/iot/temperature"

mqtt_client = mqtt.Client()
mqtt_client.connect(broker,1883)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

print("Edge device waiting for sensor...")

conn, addr = server.accept()

print("Sensor connected:", addr)

while True:

    data = conn.recv(1024)

    if not data:
        break

    value = data.decode()

    print("Edge received:", value)

    mqtt_client.publish(topic,value)

    print("Forwarded to MQTT:", value)