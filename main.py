from gpiozero import Motor, PWMOutputDevice
from signal import pause
pwm = PWMOutputDevice("GPIO26")
motor = Motor(4, 5)
motor.forward()
pwm.value = 0.5

pause()