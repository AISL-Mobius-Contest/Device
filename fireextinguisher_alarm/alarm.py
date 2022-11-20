import RPi.GPIO as GPIO
import requests
import time
import threading

O = 1
C = 261
D = 293
E = 329
F = 349
Ff = 370
G = 391
A = 440
B = 493
Cc = 523

pinPiezo = 3

GPIO.setmode(GPIO.BOARD)
GPIO.setup(pinPiezo, GPIO.OUT)
GPIO.setwarnings(False)

Buzz = GPIO.PWM(pinPiezo, 440)

def buzz_Freq(Piano):
    Buzz.ChangeFrequency(Piano)

pins = (18, 19, 21)

def led(pins, color, t):
    RGBs = (
        (1,1,1),
        (1,0,0),
        (0,1,0),
        (0,0,1),
        (0,1,1),
        (1,0,1),
        (1,1,0)
    )
    GPIO.setmode(GPIO.BOARD)
    
    GPIO.setup(pins[0], GPIO.OUT)
    GPIO.setup(pins[1], GPIO.OUT)
    GPIO.setup(pins[2], GPIO.OUT)
    
    GPIO.output(pins[0], RGBs[color][0])
    GPIO.output(pins[1], RGBs[color][1])
    GPIO.output(pins[2], RGBs[color][2])
    
    time.sleep(t)
    
    GPIO.cleanup(pins)

url = 'XXXX'
payload = {}
headers = {
    'Accept': 'application/json',
    'X-M2M-RI': '12345',
    'X-M2M-Origin': 'SOrigin'
}

if __name__ == '__main__':
    while True:
        response = requests.request('GET', url, headers=headers, data=payload)
        res = response.json()['m2m:cin']['con']['ReqID']
        if res == 0:
            break
        else: time.sleep(1)
    Buzz.start(90)
    
    t1 = threading.Thread(target=led, args=(pins, 1, 10))
    t2 = threading.Thread(target=buzz_Freq, args=(Cc,))
    
    t1.start()
    t2.start()
    
    t1.join()
    t2.join()
    
    GPIO.cleanup()