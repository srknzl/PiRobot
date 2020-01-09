import RPi.GPIO as GPIO
import time

in1 = 24
in2 = 23
en = 25
temp1 = 1
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(in1, GPIO.OUT)
GPIO.setup(in2, GPIO.OUT)
GPIO.setup(en, GPIO.OUT)
GPIO.output(in1, GPIO.LOW)
GPIO.output(in2, GPIO.LOW)
p = GPIO.PWM(en, 1000)
p.start(25)
print("\n")
print("Baslangic olarak dusuk hiz ve ileri olarak calisir")
print("r-ileri s-dur f-ileri b-geri l-dusuk m-orta h-hizli e-cikis")
print("\n")

while (1):

    x = input()

    if x == 'r':
        print("ileri")
        if (temp1 == 1):
            GPIO.output(in1, GPIO.HIGH)
            GPIO.output(in2, GPIO.LOW)
            print("forward")
            x = 'z'
        else:
            GPIO.output(in1, GPIO.LOW)
            GPIO.output(in2, GPIO.HIGH)
            print("backward")
            x = 'z'


    elif x == 's':
        print("Dur")
        GPIO.output(in1, GPIO.LOW)
        GPIO.output(in2, GPIO.LOW)
        x = 'z'

    elif x == 'f':
        print("ileri")
        GPIO.output(in1, GPIO.HIGH)
        GPIO.output(in2, GPIO.LOW)
        temp1 = 1
        x = 'z'

    elif x == 'b':
        print("Geri")
        GPIO.output(in1, GPIO.LOW)
        GPIO.output(in2, GPIO.HIGH)
        temp1 = 0
        x = 'z'

    elif x == 'l':
        print("Dusuk")
        p.ChangeDutyCycle(25)
        x = 'z'

    elif x == 'm':
        print("Orta")
        p.ChangeDutyCycle(50)
        x = 'z'

    elif x == 'h':
        print("Yuksek")
        p.ChangeDutyCycle(75)
        x = 'z'


    elif x == 'e':
        GPIO.cleanup()
        break

    else:
        print("<<<  hatali data  >>>")
        print("normal komutlari yaziniz.....")