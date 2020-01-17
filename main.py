import bluetooth
import time
from threading import Thread
from gpiozero import Motor, Button, PWMLED, Buzzer
from signal import pause
from bluetooth import *
import subprocess
import enum
import math


def ledsWhenTurnRight():
    rightGreen.blink(0.3, 0.3)
    rightRed.blink(0.3, 0.3)
    leftGreen.off()
    leftRed.off()


def ledsWhenTurnLeft():
    leftGreen.blink(0.3, 0.3)
    leftRed.blink(0.3, 0.3)
    rightGreen.off()
    rightRed.off()


def ledsWhenStop():
    leftRed.on()
    rightRed.on()
    leftGreen.off()
    rightGreen.off()


def ledsWhenNotConnected():
    leftRed.blink()
    rightRed.blink()
    leftGreen.off()
    rightGreen.off()


def turnOffLeds():
    leftRed.off()
    rightRed.off()
    leftGreen.off()
    rightGreen.off()


"""
def stopSomeTimeLater():
    time.sleep(STOPTIME)
    leftMotor.stop()
    rightMotor.stop()
    ledsWhenStop()
"""


def turnOffBuzzer():
    buzzer.off()


def beep():
    buzzer.beep(0.3, 0.3)


def connect():
    PORT = 1
    server_socket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)

    server_socket.bind(("", PORT))
    server_socket.listen(1)
    uuid = "94f39d29-7d6d-437d-973b-fba39e49d4ee"
    print("Starting a rfcomm server with uuid 94f39d29-7d6d-437d-973b-fba39e49d4ee..")

    advertise_service(server_socket, "raspberrypi",
                      service_id=uuid,
                      service_classes=[uuid, SERIAL_PORT_CLASS],
                      profiles=[SERIAL_PORT_PROFILE])

    acceptResult = server_socket.accept()
    cs = acceptResult[0]
    address = acceptResult[1]
    turnOffLeds()
    print("Accepted connection from ", address)
    listener = Thread(target=listenForMessages, args=(cs,), daemon=True)
    listener.start()


def discoveryEnabler():
    while True:
        time.sleep(10)
        discoverable_result = subprocess.check_output(
            " echo 'show B8:27:EB:49:FB:3B' | bluetoothctl | grep Discoverable: ", shell=True).decode("utf-8")
        pairable_result = subprocess.check_output(" echo 'show B8:27:EB:49:FB:3B' | bluetoothctl | grep Pairable: ",
                                                  shell=True).decode("utf-8")

        if 'no' in discoverable_result or 'no' in pairable_result:
            subprocess.call(  # pair without pin ref: https://stackoverflow.com/a/34751404/9483495
                "echo  'discoverable on' | bluetoothctl && echo  'pairable on' | bluetoothctl", shell=True)


def listenForMessages(cs):
    global speed, currentOperation
    client_socket = cs  # type: BluetoothSocket
    while True:
        try:
            data = client_socket.recv(1024).decode("utf-8")
        except BluetoothError:
            connecter = Thread(target=connect, args=(), daemon=True)
            connecter.start()
            # stop and connect again
            ledsWhenNotConnected()
            leftMotor.value = 0
            rightMotor.value = 0
            return
        data = data.rstrip('\r\n')
        splittedData = data.split(" ")
        message = splittedData[0]
        if message == "left":
            leftMotor.backward(speed)
            rightMotor.forward(speed)
            # stopper = Thread(target=stopSomeTimeLater, args=(), daemon=True)
            # stopper.start()
            ledsWhenTurnLeft()
            turnOffBuzzer()
            currentOperation = Operation.left
        elif message == "right":
            leftMotor.forward(speed)
            rightMotor.backward(speed)
            # stopper = Thread(target=stopSomeTimeLater, args=(), daemon=True)
            # stopper.start()
            ledsWhenTurnRight()
            turnOffBuzzer()
            currentOperation = Operation.right
        elif message == "joystick":
            if not str.isdigit(angle) or not str.isdigit(movement):
                print("Wrong usage of joystick command")
                continue

            angle = int(splittedData[1])
            movement = int(splittedData[2])

            scaleFactor = (1.0 * movement) / 100
            left = 0
            right = 0
            if angle == 0:
                left = 1
                right = 0
            elif angle == 90:
                left = 1
                right = 1
            elif angle == 180:
                left = 0
                right = 1
            elif angle == 270:
                left = -1
                right = -1
            elif 0 < angle < 90:
                left = 1
                right = (angle * 1.0) / 90
            elif 90 < angle < 180:
                left = 2 - (angle * 1.0) / 90
                right = 1
            elif 180 < angle < 270:
                left = 2 - (1.0 * angle) / 90
                right = 5 - (1.0 * angle) / 45
            elif angle > 270:
                left = -1 + (2.0 * (angle - 270)) / 90
                right = -1 + (1.0 * (angle - 270)) / 90

            assert 1 >= left * scaleFactor >= -1, "left: " + str(left) + ", scaleFactor: " + str(scaleFactor) + ", mult: " + str(left * scaleFactor)
            assert 1 >= right * scaleFactor >= -1, "right: " + str(right) + ", scaleFactor: " + str(scaleFactor) + ", mult: " + str(right * scaleFactor)

            leftMotor.value = left * scaleFactor
            rightMotor.value = right * scaleFactor

        elif message == "speed":
            if len(splittedData) != 2:
                client_socket.send("Wrong usage of speed command" + str(splittedData))
                print("Wrong usage of speed command", splittedData)
                continue
            speed = float(splittedData[1])
            if currentOperation == Operation.backward:
                leftMotor.backward(speed)
                rightMotor.backward(speed)
            elif currentOperation == Operation.forward:
                leftMotor.forward(speed)
                rightMotor.forward(speed)
            elif currentOperation == Operation.left:
                leftMotor.backward(speed)
                rightMotor.forward(speed)
            elif currentOperation == Operation.right:
                leftMotor.forward(speed)
                rightMotor.backward(speed)

        elif message == "stop":
            leftMotor.value = 0
            rightMotor.value = 0
            ledsWhenStop()
            turnOffBuzzer()
            currentOperation = Operation.stop
        elif message == "forward":
            leftMotor.forward(speed)
            rightMotor.forward(speed)
            turnOffLeds()
            turnOffBuzzer()
            currentOperation = Operation.forward
        elif message == "backward":
            leftMotor.backward(speed)
            rightMotor.backward(speed)
            turnOffLeds()
            beep()
            currentOperation = Operation.backward
        # print(data)


class Operation(enum.Enum):
    forward = 1
    backward = 2
    left = 3
    right = 4
    stop = 5
    joystick_control = 6


currentOperation = Operation.stop
speed = 0.5
# STOPTIME = 0.43 # Konya :D
discoveryEnabler = Thread(target=discoveryEnabler, args=(), daemon=True)
discoveryEnabler.start()
print(subprocess.check_output(
    "echo  'power on' | bluetoothctl && echo  'discoverable on' | bluetoothctl && echo  'pairable on' | "
    "bluetoothctl  && echo 'agent NoInputNoOutput' | bluetoothctl &&  echo 'default-agent ' | "
    "bluetoothctl && echo  'show B8:27:EB:49:FB:3B' | bluetoothctl ", shell=True).decode(
    "utf-8"))
leftRed = PWMLED(15)
leftGreen = PWMLED(14)
rightRed = PWMLED(2)
rightGreen = PWMLED(10)
ledsWhenNotConnected()

connect()

leftMotor = Motor(23, 24, 18, pwm=True)  # In1 23-> pin16, In2 24->pin18, 18-> pin12
rightMotor = Motor(27, 22, 19, pwm=True)  # 27-> pin13, 22-> pin15, 19-> pin35

buzzer = Buzzer(25)

pause()
