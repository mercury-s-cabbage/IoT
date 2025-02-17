from xml.etree.ElementTree import tostring
from random import randint
import time
import serial

port = 'COM7'
connection = serial.Serial(port, baudrate=9600, timeout=2)

def trig(connection, cmd, resp_length):
    str_resp = ''
    connection.flushInput()
    connection.write(cmd.encode())

    if resp_length > 0:
        resp: bytes = connection.read(resp_length)
        str_resp = resp.decode(errors='ignore').strip()
        print(f"raw: {resp}, decoded: {str_resp}")
    return str_resp

while True:
    data = trig(connection, 't', 8)
    if data:
        print(data)

    time.sleep(1)