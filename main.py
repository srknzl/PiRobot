from gpiozero import Motor
from signal import pause

motor = Motor(4, 5, 1, pwm=True)
motor.forward(0.5)

pause()