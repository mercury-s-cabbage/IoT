import paho.mqtt.client as mqtt_client
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
    data_to_send = input("Введите данные для отправки (или 'exit' для выхода): ")
    if data_to_send.lower() == 'exit':
        print("Выход из программы.")
        break
    # Отправляем данные в топик "123"
    client.publish("1254926558", data_to_send)
    print(f"Отправлено: {data_to_send}")

# client.disconnect()
# client.loop_stop()
