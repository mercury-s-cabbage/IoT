from xml.etree.ElementTree import tostring
from random import randint
import time
import serial
import numpy as np
import numpy.polynomial.polynomial as poly
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error

def trig(connection, cmd, resp_length):
    str_resp = ''
    connection.flushInput()
    connection.write(cmd.encode())

    if resp_length > 0:
        resp: bytes = connection.read(resp_length)
        str_resp = resp.decode(errors='ignore').strip()
    return str_resp

def is_full(x, signal_range, space):
    if not x:
        return False

    x = sorted(x)
    start, end = signal_range
    if x[0] > start+space or x[-1] < end-space:
        return False

    for i in range(len(x) - 1):
        if x[i + 1] - x[i] - 1 > space:
            return False
    return True

def make_model(x, y):
    best_degree = 1
    best_mse = float('inf')
    best_model = None

    for degree in range(1, 6):
        coefficients = np.polyfit(x, y, degree)
        model = np.poly1d(coefficients)
        mse = mean_squared_error(y, model(x))

        if mse < best_mse:
            best_mse = mse
            best_degree = degree
            best_model = model

    print(f"Best polynomial degree: {best_degree}")

    # График
    x_sorted = np.linspace(min(x), max(x), 100)
    y_pred = best_model(x_sorted)

    plt.scatter(x, y, label='Data')
    plt.plot(x_sorted, y_pred, color='red', label='Best Fit Curve')
    plt.legend()
    plt.show()
    return best_model
def calibration(connection, signal_range):
    x = []
    y = []
    while True:
        data = trig(connection, 't', 8)
        if data:
            d1 = int(data[:4])
            d2 = int(data[4:])
            if (d1>=signal_range[0] and d1<=signal_range[1]):
                if not d1 in y:
                    y.append(d1)
                    x.append(d2)
                    print(f"{y} \n{x}\n\n")


        if is_full(y, signal_range, 2):
            model = make_model(x, y)
            return model


port = 'COM7'
connection = serial.Serial(port, baudrate=9600, timeout=2)
time.sleep(3) # waiting for connection
model = None

while(True):
    command = input()
    if command == "c":
        model = calibration(connection, [20, 40])
    elif command == "p":
        print("Start prediction")
        if (not model):
            print("There is no model")
        else:
            data = trig(connection, 't', 8)
            print(data)
            if data:
                d1 = int(data[:4])
                d2 = int(data[4:])

                d1_pred = model(int(d2))
                print(f"d_real = {d1}, d_pred = {d1_pred}\n")



