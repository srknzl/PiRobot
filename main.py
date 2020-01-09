import time
from gpiozero import Motor
import bluetooth
# from signal import pause

server_socket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)

port = 1
server_socket.bind(("", port))
server_socket.listen(1)

client_socket, address = server_socket.accept()
print("Accepted connection from ", address)
while 1:
    data = client_socket.recv(1024).decode("utf-8")

    if data == "run":
        leftMotor = Motor(23, 24, 18, pwm=True)  # 23-> pin16, 24->pin18, 18-> pin12
        rightMotor = Motor(27, 22, 19, pwm=True)  # 27-> pin13, 22-> pin15, 19-> pin35

        leftMotor.forward(0.5)
        rightMotor.forward(0.5)
        time.sleep(1)
        leftMotor.backward(1)
        rightMotor.backward(1)
        time.sleep(1)
    else:
        print(data)

