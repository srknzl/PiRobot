import time
from gpiozero import Motor
from signal import pause
motor = Motor(23, 24, 18, pwm=True) #23-> pin16, 24->pin18, 18-> pin12

while True:
        motor.forward(0.5)
        time.sleep(1)
        motor.backward(1)
        time.sleep(1)
pause()

