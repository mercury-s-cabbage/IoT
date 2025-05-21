import paho.mqtt.client as mqtt_client

broker = "broker.emqx.io"
topic = "esp8266/commands"


def on_connect(client, userdata, flags, rc, properties=None):
    if rc == 0:
        print("Connected to MQTT Broker!")
        client.subscribe(topic)
        print(f"Subscribed to topic: {topic}")
    else:
        print(f"Failed to connect, return code {rc}")

def on_message(client, userdata, msg):
    global current_data
    current_data = msg.payload.decode() # TODO: Сохранять историю данных в БД
    print(f"MQTT received: {current_data}")

def mqtt_loop():
    client_id = "subscriber_client"
    client = mqtt_client.Client(client_id=client_id, callback_api_version=mqtt_client.CallbackAPIVersion.VERSION2)
    client.on_connect = on_connect
    client.on_message = on_message
    print(f"Connecting to broker {broker}...")
    client.connect(broker)
    client.loop_forever()