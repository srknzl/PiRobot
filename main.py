import bluetooth
import time
from threading import Thread
from gpiozero import Motor, Button, PWMLED, Buzzer
from signal import pause
from bluetooth import *
import subprocess


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


def stopSomeTimeLater():
    time.sleep(STOPTIME)
    leftMotor.stop()
    rightMotor.stop()
    ledsWhenStop()


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
            #leftMotor.forward(0.2)
            #rightMotor.forward(0.8)
            leftMotor.backward(0.7)
            rightMotor.forward(0.7)
            stopper = Thread(target=stopSomeTimeLater, args=(), daemon=True)
            stopper.start()
            ledsWhenTurnLeft()
            turnOffBuzzer()
        elif message == "right":
            #leftMotor.forward(0.8)
            #rightMotor.forward(0.2)
            leftMotor.forward(0.7)
            rightMotor.backward(0.7)
            stopper = Thread(target=stopSomeTimeLater, args=(), daemon=True)
            stopper.start()
            ledsWhenTurnRight()
            turnOffBuzzer()
        elif message == "left90":
            pass  # todo Add 90 degree left turn code
        elif message == "right90":
            pass  # todo Add 90 degree left turn code
        elif message == "speed":
            if len(splittedData) != 2:
                client_socket.send("Wrong usage of speed command" + str(splittedData))
                print("Wrong usage of speed command", splittedData)
                continue
            if leftMotor.value < 0:
                leftMotor.value = -1 * float(splittedData[1])
            else:
                leftMotor.value = float(splittedData[1])

            if rightMotor.value < 0:
                rightMotor.value = -1 * float(splittedData[1])
            else:
                rightMotor.value = float(splittedData[1])
        elif message == "stop":
            leftMotor.value = 0
            rightMotor.value = 0
            ledsWhenStop()
            turnOffBuzzer()
        elif message == "forward":
            leftMotor.forward(0.5)
            rightMotor.forward(0.5)
            turnOffLeds()
            turnOffBuzzer()
        elif message == "backward":
            leftMotor.backward(0.5)
            rightMotor.backward(0.5)
            turnOffLeds()
            beep()
        # print(data)


STOPTIME = 0.72
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
