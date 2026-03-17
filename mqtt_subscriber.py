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
