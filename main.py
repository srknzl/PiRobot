from gpiozero import Motor

motor = Motor(4, 5, 1, pwm=True)
motor.forward(0.5)
