import RPi.GPIO as GPIO
import time
import voice_recog as vr

TRIG=21
ECHO=20
maxTime = 0.04
def distance_act():
    GPIO.setmode(GPIO.BCM)


    GPIO.setup(TRIG,GPIO.OUT)
    GPIO.setup(ECHO,GPIO.IN)
    GPIO.output(TRIG,False)

   

    GPIO.output(TRIG,True)

   

    GPIO.output(TRIG,False)

    pulse_start = time.time()
    timeout = pulse_start + maxTime
    while GPIO.input(ECHO) == 0 and pulse_start < timeout:
        pulse_start = time.time()
    pulse_end = time.time()
    timeout = pulse_end + maxTime
    while GPIO.input(ECHO) == 1 and pulse_end < timeout:
        pulse_end = time.time()

    pulse_duration = pulse_end - pulse_start
    distance = pulse_duration * 17000/2.54 #inch
    distance = round(distance, 2)
    # 
    dis = int(distance)
    GPIO.cleanup()
    return distance

def dis_1():
    threshold = 12
    if distance <= threshold:
        return "Near you,"
    else:
        return "Far you,"
    
if __name__ == "__main__":
    distance = distance_act()
    print(distance)
    distance1 = dis_1()
    vr.run_thread2("hello",distance1)
    
    

