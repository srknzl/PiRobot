from gpiozero import Motor
from signal import pause

motor = Motor(4, 5, 26, pwm=True)
motor.forward(0.5)

print(motor.value)

pause()