import time
import bluetooth
from threading import Thread
from gpiozero import Motor, Button, DigitalInputDevice
from signal import pause
from bluetooth import *

def countWheel():
    global speedSensorCounter
    speedSensorCounter += 1
    print(speedSensorCounter)


def listenForMessages(cs):
    client_socket = cs  # type: BluetoothSocket
    while True:
        data = client_socket.recv(1024).decode("utf-8")

        data = data.rstrip('\r\n')

        splittedData = data.split(" ")
        message = splittedData[0]
        if message == "l":
            leftMotor.forward(0.2)
            rightMotor.forward(0.8)
            # todo Add left led code
        elif message == "r":
            leftMotor.forward(0.8)
            rightMotor.forward(0.2)
            # todo Add right led code
        elif message == "left90":
            pass  # todo Add 90 degree left turn code
        elif message == "right90":
            pass  # todo Add 90 degree left turn code
        elif message == "sp":
            if len(splittedData) != 2:
                client_socket.send("Wrong usage of speed command" + str(splittedData))
                print("Wrong usage of speed command", splittedData)
                continue
            if leftMotor.value < 0:
                leftMotor.value = -1*float(splittedData[1])
            else: 
                leftMotor.value = float(splittedData[1])

            if rightMotor.value < 0:
                rightMotor.value = -1*float(splittedData[1])
            else: 
                rightMotor.value = float(splittedData[1])
        elif message == "s":
            leftMotor.value = 0
            rightMotor.value = 0
            # todo Add stop led code
        elif message == "f":
            leftMotor.forward(0.5)
            rightMotor.forward(0.5)
        elif message == "b":
            leftMotor.backward(-0.5)
            rightMotor.backward(-0.5)
        elif message == "wheel":
            client_socket.send("Wheel:" + str(speedSensorCounter))
            print("Wheel: ", speedSensorCounter)
        # print(data)


PORT = 1
server_socket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)

server_socket.bind(("", PORT))
server_socket.listen(1)

uuid = "94f39d29-7d6d-437d-973b-fba39e49d4ee"

advertise_service( server_socket, "raspberrypi",
                   service_id = uuid,
                   service_classes = [ uuid, SERIAL_PORT_CLASS ],
                   profiles = [ SERIAL_PORT_PROFILE ])

acceptResult = server_socket.accept()
cs = acceptResult[0]
address = acceptResult[1]
print("Accepted connection from ", address)

leftMotor = Motor(23, 24, 18, pwm=True)  # In1 23-> pin16, In2 24->pin18, 18-> pin12
rightMotor = Motor(27, 22, 19, pwm=True)  # 27-> pin13, 22-> pin15, 19-> pin35

listener = Thread(target=listenForMessages, args=(cs,), daemon=True)
listener.start()

speedSensorCounter = 0
speedSensor = Button(17)
speedSensor.when_pressed = countWheel

pause()