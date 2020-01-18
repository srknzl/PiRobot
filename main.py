import bluetooth
import time
from threading import Thread
from gpiozero import Motor, PWMLED, Buzzer, DistanceSensor, LightSensor
from signal import pause
from bluetooth import *
import subprocess
import enum


def stopFunction():
    global currentOperation
    ledsWhenStop()
    leftMotor.stop()
    rightMotor.stop()
    currentOperation = Operation.stop
    turnOffBuzzer()


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


def reportDistance():
    while True:
        print("Distance in meters: ", distanceSensor.distance)
        time.sleep(0.2)



def reportLight():
    while True:
        print("Right light: ", rightLDR.value)
        print("Left light: ", leftLDR.value)
        time.sleep(1)
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
        subprocess.call("echo  'discoverable on' | bluetoothctl && echo  'pairable on' | "
                "bluetoothctl  && echo 'agent on' | bluetoothctl &&  echo 'default-agent ' | "
                "bluetoothctl", shell=True)


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
            if not str.isdigit(splittedData[1]) or not str.isdigit(splittedData[2]):
                print("Wrong usage of joystick command")
                continue

            angle = int(splittedData[1])
            movement = int(splittedData[2])

            scaleFactor = (1.0 * movement) / 100
            left = 0
            right = 0

            if scaleFactor < 0.4:
                left = 0
                right = 0
                if currentOperation != Operation.stop:
                    ledsWhenStop()
                currentOperation = Operation.stop
            elif 20 >= angle >= 0 or angle > 340:  # Turn around
                left = 1
                right = -1
                if currentOperation != Operation.right:
                    ledsWhenTurnRight()
                currentOperation = Operation.right
            elif 70 >= angle >= 20:  # Turn right
                left = 1
                right = 0.25
                if currentOperation != Operation.right:
                    ledsWhenTurnRight()
                currentOperation = Operation.right
            elif 110 >= angle > 70:  # Go forward
                left = 1
                right = 1
                turnOffLeds()
                currentOperation = Operation.forward
            elif 160 >= angle > 110:  # Turn left
                left = 0.25
                right = 1
                if currentOperation != Operation.left:
                    ledsWhenTurnLeft()
                currentOperation = Operation.left
            elif 200 >= angle > 160:  # Turn around
                left = -1
                right = 1
                if currentOperation != Operation.left:
                    ledsWhenTurnLeft()
                currentOperation = Operation.left
            elif 250 >= angle > 200:  # Turn back left
                left = -0.25
                right = -1
                if currentOperation != Operation.left:
                    ledsWhenTurnLeft()
                currentOperation = Operation.left
            elif 290 >= angle > 250:  # Go back
                left = -1
                right = -1
                turnOffLeds()
                currentOperation = Operation.backward
            elif 340 >= angle > 290:  # Turn back right
                left = -1
                right = -0.25
                if currentOperation != Operation.right:
                    ledsWhenTurnRight()
                currentOperation = Operation.right

            if not 1 >= left * scaleFactor >= -1:
                print("Something is not right with this motor value")
                continue
            if not 1 >= right * scaleFactor >= -1:
                print("Something is not right with this motor value")
                continue
            print("left:", left * scaleFactor)
            print("right:", right * scaleFactor)

            leftMotor.value = left * scaleFactor
            rightMotor.value = right * scaleFactor
            """
            if angle == 0:
                left = 1
                right = -1
            elif angle == 90:
                left = 1
                right = 1
            elif angle == 180:
                left = -1
                right = 1
            elif angle == 270:
                left = -1
                right = -1
            elif 0 < angle < 90:
                left = 1
                right = -1 + 2 * (angle * 1.0) / 90
            elif 90 < angle < 180:
                left = 1 - ((angle - 90) * 2.0) / 90
                right = 1
            elif 180 < angle < 270:
                left = -1
                right = 1 - ((angle - 180) * 2.0) / 90
            elif angle > 270:
                left = -1 + ((angle - 270) * 2.0) / 90
                right = -1

            if not 1 >= left * scaleFactor >= -1:
                print("Something is not right with this motor value")
                continue
            if not 1 >= right * scaleFactor >= -1:
                print("Something is not right with this motor value")
                continue
            print("left:", left * scaleFactor)
            print("right:", right * scaleFactor)

            if abs(left * scaleFactor) < 0.4 and abs(right * scaleFactor) < 0.4:
                leftMotor.value = 0
                rightMotor.value = 0
            elif abs(left * scaleFactor) < 0.4:
                if left < 0:
                    leftMotor.value = -1 * max(0.4, abs(right * scaleFactor)/2)
                else:
                    leftMotor.value = max(0.4, abs(right * scaleFactor)/2)
                rightMotor.value = right * scaleFactor
            elif abs(right * scaleFactor) < 0.4:
                if right < 0:
                    rightMotor.value = -1 * max(0.4, abs(left * scaleFactor)/2)
                else:
                    rightMotor.value = max(0.4, abs(left * scaleFactor)/2)
                leftMotor.value = left * scaleFactor
            else:
                leftMotor.value = left * scaleFactor
                rightMotor.value = right * scaleFactor
            """
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
# STOPTIME = 0.43


leftRed = PWMLED(15)
leftGreen = PWMLED(14)
rightRed = PWMLED(2)
rightGreen = PWMLED(10)

subprocess.call("echo 'discoverable on' | bluetoothctl && echo  'pairable on' | "
                "bluetoothctl  && echo 'agent on' | bluetoothctl &&  echo 'default-agent ' | "
                "bluetoothctl", shell=True)

discoveryEnabler = Thread(target=discoveryEnabler, args=(), daemon=True)
discoveryEnabler.start()

ledsWhenNotConnected()

connect()



leftLDR = LightSensor(5, threshold=0.9)
rightLDR = LightSensor(6, threshold=0.9)


"""
lightReporter = Thread(target=reportLight, args=(), daemon=True)
lightReporter.start()

distanceReporter = Thread(target=reportDistance, args=(), daemon=True)
distanceReporter.start()
"""

leftLDR.when_light = stopFunction
rightLDR.when_light = stopFunction

distance = 0 # in cms
distanceSensor = DistanceSensor(20, 21, threshold_distance=0.3)
distanceSensor.when_in_range = stopFunction

leftMotor = Motor(23, 24, 18, pwm=True)  # In1 23-> pin16, In2 24->pin18, 18-> pin12
rightMotor = Motor(27, 22, 19, pwm=True)  # 27-> pin13, 22-> pin15, 19-> pin35

buzzer = Buzzer(25)

pause()
