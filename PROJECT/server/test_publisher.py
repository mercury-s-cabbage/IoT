import time
import paho.mqtt.client as mqtt_client
import random
from uuid import getnode as get_mac
import hashlib

broker="broker.emqx.io"

# make client id
h = hashlib.new('sha256')
mac = get_mac()
h.update(str(mac).encode())
pub_id = h.hexdigest()[:10]
print(f"Listen me at id {pub_id}")

client = mqtt_client.Client(
    mqtt_client.CallbackAPIVersion.VERSION2,
    pub_id
)
print("Connecting to broker", broker)
print(client.connect(broker))

client.loop_start()
print("Publishing")


while True:
    current_time = time.localtime()
    current_second = current_time.tm_sec

    if current_second % 2 == 0:
        print('send')
        client.publish(f"esp8266/commands", "data")

    time.sleep(1)

# client.disconnect()
# client.loop_stop()
