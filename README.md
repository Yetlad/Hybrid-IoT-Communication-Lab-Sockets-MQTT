
#  IoT Communication Pipeline

## Lab Series: From Sockets to MQTT

---

##  Objective

This lab series demonstrates how to build a simple **IoT communication pipeline** using:

* Socket Programming
* MQTT Messaging

The system simulates:

* A **Sensor Node**
* An **Edge Device**
* A **Cloud / Server Application**

The goal is to understand how data flows across different communication layers in IoT systems.

---

##  System Architecture

```
Laptop 1 (Sensor Node)
        ↓ Socket
Laptop 2 (Edge Device)
        ↓ MQTT
MQTT Broker
        ↓
Laptop 1 (Cloud Subscriber)
```

---

##  Data Flow

```
Sensor → Edge Device → Cloud
```

* Sensor sends data using **Sockets**
* Edge device forwards data using **MQTT**
* Cloud receives and displays data

---

#  Lab 1 — Sensor to Edge (Socket Programming)

##  Objective

Implement direct communication between two devices using Python sockets.

---

##  Laptop 2 — Socket Server (Edge Device)

**File:** `socket_server.py`

```python
import socket

HOST = "192.168.56.1"
PORT = 5000

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

print("Waiting for sensor connection...")

conn, addr = server.accept()
print("Connected:", addr)

while True:
    data = conn.recv(1024)
    if not data:
        break
    print("Sensor data:", data.decode())
```

---

## Laptop 1 — Sensor Client

**File:** `socket_sensor.py`

```python
import socket
import random
import time

SERVER_IP = "192.168.56.1"  # Replace with Laptop 2 IP
PORT = 5000

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((SERVER_IP, PORT))

while True:
    temperature = round(random.uniform(20,35),2)
    message = f"{temperature}"
    client.send(message.encode())
    print("Sensor value sent:", temperature)
    time.sleep(5)
```

---

##  Expected Output

**Sensor (Laptop 1):**

```
Sensor value sent: 23.4
Sensor value sent: 24.1
```

**Edge Device (Laptop 2):**

```
Sensor data: 23.4
Sensor data: 24.1
```

---

#  Lab 2 — Edge to Cloud (MQTT)

##  Objective

Forward sensor data using MQTT protocol.

We use a public broker:
 **EMQX Broker** (`broker.emqx.io`)

---

##  Laptop 2 — MQTT Publisher

**File:** `mqtt_publisher.py`

```python
import paho.mqtt.client as mqtt
import random
import time

broker = "broker.emqx.io"
topic = "savonia/iot/temperature"

client = mqtt.Client()
client.connect(broker,1883)

while True:
    temperature = round(random.uniform(20,35),2)
    client.publish(topic,temperature)
    print("Published to MQTT:",temperature)
    time.sleep(5)
```

---

##  Laptop 1 — MQTT Subscriber (Cloud)

**File:** `mqtt_subscriber.py`

```python
import paho.mqtt.client as mqtt

broker = "broker.emqx.io"
topic = "savonia/iot/temperature"

def on_message(client,userdata,msg):
    value = msg.payload.decode()
    print("Cloud received:",value)

client = mqtt.Client()
client.connect(broker,1883)

client.subscribe(topic)
client.on_message = on_message

client.loop_forever()
```

---

##  Expected Output

```
Cloud received: 24.1
Cloud received: 23.7
```

---

#  Lab 3 — Full IoT Pipeline (Integration)

##  Objective

Combine socket and MQTT systems into a complete IoT pipeline.

---

##  Architecture

```
Laptop 1 (Sensor)
      ↓ Socket
Laptop 2 (Edge Device)
      ↓ MQTT
Laptop 1 (Cloud Subscriber)
```

---

##  Edge Device (Socket + MQTT)

**File:** `edge_device.py`

```python
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
```

---

##  Final Output

**Cloud Subscriber (Laptop 1):**

```
Cloud received: 23.5
Cloud received: 24.2
```

#  Conclusion

This lab demonstrates how IoT systems combine multiple communication technologies. Socket programming enables reliable 
local communication between devices, while MQTT allows efficient cloud integration. The edge device plays a critical role 
by bridging these two layers, enabling scalable and real-time data transmission. This architecture reflects real-world 
IoT systems where sensors communicate locally and data is processed and forwarded to the cloud for monitoring and analysis.

---

