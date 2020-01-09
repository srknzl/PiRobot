import time
from gpiozero import Motor
from signal import pause

leftMotor = Motor(23, 24, 18, pwm=True)  # 23-> pin16, 24->pin18, 18-> pin12
rightMotor = Motor(27, 22, 19, pwm=True)  # 27-> pin13, 22-> pin15, 19-> pin35

while True:
    leftMotor.forward(0.5)
    rightMotor.forward(0.5)
    time.sleep(1)
    leftMotor.backward(1)
    rightMotor.backward(1)
    time.sleep(1)
pause()
