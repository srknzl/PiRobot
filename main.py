import time
from gpiozero import Motor, Button, DigitalInputDevice
import bluetooth
from bluetooth import BluetoothSocket

# from signal import pause

def countWheel(device):
    global speedSensorCounter
    speedSensorCounter += 1


PORT = 1
server_socket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)

server_socket.bind(("", PORT))
server_socket.listen(1)

acceptResult = server_socket.accept()
client_socket = acceptResult[0]  # type: BluetoothSocket
address = acceptResult[1]
print("Accepted connection from ", address)

leftMotor = Motor(23, 24, 18, pwm=True)  # 23-> pin16, 24->pin18, 18-> pin12
rightMotor = Motor(27, 22, 19, pwm=True)  # 27-> pin13, 22-> pin15, 19-> pin35

speedSensorCounter = 0
speedSensor = DigitalInputDevice(4, pull_up=False)

#speedSensor = Button(4)
#speedSensor.when_activated = countWheel

while True:
    data = client_socket.recv(1024).decode("utf-8")
    data = data.rstrip('\r\n')

    splittedData = data.split("|")
    message = splittedData[0]
    if message == "left":
        leftMotor.forward(0.3)
        rightMotor.forward(0.7)
        # todo Add left led code
    elif message == "right":
        leftMotor.forward(0.7)
        rightMotor.forward(0.3)
        # todo Add right led code
    elif message == "left90":
        pass  # todo Add 90 degree left turn code
    elif message == "right90":
        pass  # todo Add 90 degree left turn code
    elif message == "speed":
        if len(splittedData) != 2:
            client_socket.send("Wrong usage of speed command" + str(splittedData))
            print("Wrong usage of speed command", splittedData)
            continue
        leftMotor.value = float(splittedData[1])
        rightMotor.value = float(splittedData[1])
    elif message == "stop":
        leftMotor.value = 0
        rightMotor.value = 0
        # todo Add stop led code
    elif message == "forward":
        leftMotor.forward(leftMotor.value)
        rightMotor.forward(rightMotor.value)
    elif message == "backward":
        leftMotor.backward(leftMotor.value)
        rightMotor.backward(rightMotor.value)
    elif message == "wheel":
        client_socket.send("Wheel:" + str(speedSensorCounter))
        print("Wheel: ", speedSensorCounter)
    # print(data)
    print(speedSensor.value)
