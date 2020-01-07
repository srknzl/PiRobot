from bluedot import BlueDot
from gpiozero import LED
from time import sleep
bd = BlueDot()

led = LED(17)

while True:
    led.on()
    sleep(1)
    led.off()
    sleep(1)

