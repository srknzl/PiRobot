import time
from threading import Thread
from gpiozero import Motor, Button, DigitalInputDevice
from bluetooth import *
from bluetooth import BluetoothSocket
from signal import pause


def countWheel():
    global speedSensorCounter
    speedSensorCounter += 1
    print(speedSensorCounter)


def listenForMessages(cs):
    client_socket = cs  # type: BluetoothSocket
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


PORT = 1
server_socket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)

server_socket.bind(("", PORT))
server_socket.listen(1)

uuid = "94f39d29-7d6d-437d-973b-fba39e49d4ee"

advertise_service( server_sock, "raspberrypi",
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