import torch
from matplotlib import pyplot as plt
import numpy as np
import cv2
import pyttsx3
import threading
import time
import easyocr
from PIL import Image
from geopy.geocoders import Nominatim
import reverse_geocoder as rg
import serial
import pynmea2
import RPi.GPIO as GPIO
import dis_sensor as ds

import voice_recog as vr
import threading
from datetime import datetime
import time


distance = ds.distance_act()


GPIO.setmode(GPIO.BCM)

GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)#Button to GPIO23
GPIO.setup(24, GPIO.IN, pull_up_down=GPIO.PUD_UP)


def get_current_time():
    now = datetime.now()
    hour = now.strftime("%I")
    minutes = now.strftime("%M")
    second = now.strftime("%S")
    return hour, minutes, second

def dis_1():
    threshold = 100
    if distance <= threshold:
        return "Near, to you, "
    else:
        return "Far, to you, "



def locationalarm():
    try:
        port = "/dev/ttyAMA0"
        ser = serial.Serial(port, baudrate=9600, timeout=0.5)
        dataout = pynmea2.NMEAStreamReader()


        newdata = ser.readline().decode('unicode_escape')
        if newdata.startswith('$GPGGA'):
            newmsg = pynmea2.parse(newdata)
            lat = newmsg.latitude
            lng = newmsg.longitude

            geolocator = Nominatim(user_agent="address")
            location = geolocator.reverse(f"{lat},{lng}", timeout=10, exactly_one=True)
            print(location.address)
            vr.run_thread1(location.address)
            

        else:
            print("No GPS signal")
            vr.run_thread1("No Gps Signal")


            time.sleep(1)

                                    

    except:
        pass
               

vr.run_thread1("Hello. To Activate the Text Recognition. Press Button 1. To activate GPS Location. Press Button 2, your system, is now, detecting")
### OBJECT DETECTION FUNCTION
def detection():
    

    path_hubconfig = r'/home/pi/Project Thesiss/yolov5'# path ng yolov5
    path_trained_model = r'/home/pi/Project Thesiss/smart.pt' #Our model
    model = torch.hub.load(path_hubconfig, 'custom', path=path_trained_model, source='local')

    cap = cv2.VideoCapture(0)
#     cap.set(3,640)
#     cap.set(4,480)



    while True:
        try:
            ret, frame = cap.read()

            model.conf = 0.35

        # Make detections 
            results = model(frame)

            labels, cord = results.xyxyn[0][:, -1], results.xyxyn[0][:, :-1]
            
            labels1, cord = results.xyxyn[0][:, -2], results.xyxyn[0][:, :-2]
            
            xmax_value = results.pandas().xyxy[0]['xmax']


            cv2.imshow('YOLO', np.squeeze(results.render()))

            
            n = len(labels)


            for i in range(len(labels)):
                for obj in range(len(labels1)):
                    xmax_value = results.pandas().xyxy[0]['xmax'][i]

                    def right():    
                        if xmax_value.item() >=500:
#                             run_thread3("right")
                            print("right")
                            return "in, the, Right "
                        
                    def left(): 
                        if xmax_value.item() <=300:
#                             run_thread1("middle")
                            print("left")
                            return "in, the, left"
                            
                    def middle(): 
                        if xmax_value.item() >=400 and xmax_value.item() <=500:
#                             run_thread1("middle")
                            print("middle")
                            return "in, the, middle"
                
                

                    if labels[i] == 0 and labels1[obj] >= 0.60:

                        print ("Apple")
                        
                        vr.run_thread1("Apple Detected")
                        vr.run_thread2(f"Distance: {distance} inch")


                       
                        
                    if labels[i] == 1 and labels1[obj] >= 0.60:

                        print ("Banana")
                        vr.run_thread3("Banana detected, ",f"in, {distance}, inch,",dis_1())

                    if labels[i] == 2 and labels1[obj] >= 0.60:

                        print ("Kiwi")
                        vr.run_thread3("Kiwi detected, ",f"in, {distance}, inch,",dis_1())


                    if labels[i] == 3 and labels1[obj] >= 0.60:

                        print ("Orange")
                        vr.run_thread4("Orange detected, ",f"in, {distance}, inch,",dis_1(),right())
                        vr.run_thread4("Orange detected, ",f"in, {distance}, inch,",dis_1(),middle())
                        vr.run_thread4("Orange detected, ",f"in, {distance}, inch,",dis_1(),left())



                    if labels[i] == 4 and labels1[obj] >= 0.50:

                        print ("Pear")
                        vr.run_thread3("Pear detected, ",f"in, {distance}, inch,",dis_1())


                    if labels[i] == 5 and labels1[obj] >= 0.45:

                        print ("Pedestrian")
                        vr.run_thread3("Pedestrian detected, ",f"in, {distance}, inch,",dis_1())
                        vr.run_thread4("Pedestrian detected, ",f"in, {distance}, inch,",dis_1(),right())
                        vr.run_thread4("Pedestrian detected, ",f"in, {distance}, inch,",dis_1(),middle())
                        vr.run_thread4("Pedestrian detected, ",f"in, {distance}, inch,",dis_1(),left())
                    if labels[i] == 6 and labels1[obj] >= 0.60:

                        print ("Traffic Light Green")
                        vr.run_thread3("Traffic Light Green, ",f"in, {distance}, inch,",dis_1())

                    if labels[i] == 7 and labels1[obj] >= 0.60:

                        print ("Traffic Light Inconclusive")
                        vr.run_thread3("Traffic Light Inconclusive, ",f"in, {distance}, inch,",dis_1())


                    if labels[i] == 8 and labels1[obj] >= 0.60:

                        print ("Traffic Light RED")
                        vr.run_thread3("Traffic Light RED detected, ",f"in, {distance}, inch,",dis_1())



                    if labels[i] == 9 and labels1[obj] >= 0.50:

                        print ("traffic light yellow")
                        vr.run_thread3("Traffic Light Yellow, ",f"in, {distance}, inch,",dis_1())


                    if labels[i] == 10 and labels1[obj] >= 0.45:

                        print ("Book")
                        vr.run_thread4("book detected, ",f"in, {distance}, inch,",dis_1(),right())
                        vr.run_thread4("book detected, ",f"in, {distance}, inch,",dis_1(),middle())
                        vr.run_thread4("book detected, ",f"in, {distance}, inch,",dis_1(),left())
                    if labels[i] == 11 and labels1[obj] >= 0.60:

                        print ("car")
                        vr.run_thread4("car detected,be careful,",f"in, {distance}, inch,",dis_1(),right())
                        vr.run_thread4("car detected, be careful,",f"in, {distance}, inch,",dis_1(),middle())
                        vr.run_thread4("car detected, be careful,",f"in, {distance}, inch,",dis_1(),left())
                    if labels[i] == 12 and labels1[obj] >= 0.60:

                        print ("cat")
                        vr.run_thread3("cat detected, ",f"in, {distance}, inch,",dis_1())


                    if labels[i] == 13 and labels1[obj] >= 0.50:
                        clockhour, minutes, second = get_current_time()

                        print ("clock")
                        vr.run_thread3("Clock detected. The current time is: ", clockhour, minutes)

 


                    if labels[i] == 14 and labels1[obj] >= 0.50:

                        print ("computer")
                        vr.run_thread4("computer detected, ",f"in, {distance}, inch,",dis_1(),right())
                        vr.run_thread4("computer detected, ",f"in, {distance}, inch,",dis_1(),middle())
                        vr.run_thread4("computer detected, ",f"in, {distance}, inch,",dis_1(),left())

                    if labels[i] == 15 and labels1[obj] >= 0.45:

                        print ("cups")
                        vr.run_thread3("cups detected, ",f"in, {distance}, inch,",dis_1())

                    if labels[i] == 16 and labels1[obj] >= 0.60:

                        print ("Dogs")
                        vr.run_thread3("dogs Green, ",f"in, {distance}, inch,",dis_1())

                    if labels[i] == 17 and labels1[obj] >= 0.35:

                        print ("downstair")
                        vr.run_thread4("Downstair detected, ",f"in, {distance}, inch,",dis_1(),right())
                        vr.run_thread4("Downstair detected, ",f"in, {distance}, inch,",dis_1(),middle())
                        vr.run_thread4("Downstair detected, ",f"in, {distance}, inch,",dis_1(),left())

                    if labels[i] == 18 and labels1[obj] >= 0.60:

                        print ("electric fan")
                        vr.run_thread4("electric fan detected, ",f"in, {distance}, inch,",dis_1(),right())
                        vr.run_thread4("electric fan detected, ",f"in, {distance}, inch,",dis_1(),middle())
                        vr.run_thread4("electric fan detected, ",f"in, {distance}, inch,",dis_1(),left())

                    if labels[i] == 19 and labels1[obj] >= 0.50:

                        print ("person")
                        vr.run_thread4("person detected, ",f"in, {distance}, inch,",dis_1(),right())
                        vr.run_thread4("person detected, ",f"in, {distance}, inch,",dis_1(),middle())
                        vr.run_thread4("person detected, ",f"in, {distance}, inch,",dis_1(),left())
                    if labels[i] == 20 and labels1[obj] >= 0.45:

                        print ("phone")
                        vr.run_thread4("Phone detected, ",f"in, {distance}, inch,",dis_1(),right())
                        vr.run_thread4("Phone detected, ",f"in, {distance}, inch,",dis_1(),middle())
                        vr.run_thread4("Phone detected, ",f"in, {distance}, inch,",dis_1(),left())
                    if labels[i] == 21 and labels1[obj] >= 0.45:

                        print ("table")
                        vr.run_thread4("table detected, ",f"in, {distance}, inch,",dis_1(),right())
                        vr.run_thread4("table detected, ",f"in, {distance}, inch,",dis_1(),middle())
                        vr.run_thread4("table detected, ",f"in, {distance}, inch,",dis_1(),left())
                    if labels[i] == 22 and labels1[obj] >= 0.45:

                        print ("text")
                        vr.run_thread4("text detected, ",f"in, {distance}, inch,",dis_1(),right())
                        vr.run_thread4("text detected, ",f"in, {distance}, inch,",dis_1(),middle())
                        vr.run_thread4("text detected, ",f"in, {distance}, inch,",dis_1(),left())
                    if labels[i] == 23 and labels1[obj] >= 0.3:

                        print ("upstair ")
                        vr.run_thread4("Upstair detected, ",f"in, {distance}, inch,",dis_1(),right())
                        vr.run_thread4("upstair detected, ",f"in, {distance}, inch,",dis_1(),middle())
                        vr.run_thread4("upstair detected, ",f"in, {distance}, inch,",dis_1(),left())
                    if labels[i] == 24 and labels1[obj] >= 0.50:

                        print ("water bottle")
                        vr.run_thread4("water bottle detected, ",f"in, {distance}, inch,",dis_1(),right())
                        vr.run_thread4("water bottle detected, ",f"in, {distance}, inch,",dis_1(),middle())
                        vr.run_thread4("water bottle detected, ",f"in, {distance}, inch,",dis_1(),left())
   
                    
                    ###describing the two classify##
                    
                    if 10 in labels and 22 in labels and labels1[obj] >= 0.60:
                        print ("Book and Texts")
                        vr.run_thread1("There are Text, on. a Book")

                    if 14 in labels and 21 in labels and labels1[obj] >= 0.60:
                        print ("Computer and Table")
                        vr.run_thread1("There are computer, on. a table")
                    
                    if 20 in labels and 21 in labels and labels1[obj] >= 0.60:
                        print ("Phone and Table")
                        vr.run_thread1("There are Phone, on. a table")
                        
                    
#                     if 3 in labels and 5 in labels and labels1[obj] >= 0.50:
#                         print ("Phone and Text")
#                         vr.run_thread1("There are Text, on. a Phone")
                        
                

                    


        except:
             continue
    #     if n >= 1:
    #         print ("detect object")
    #     else:
    #         print (" multiple object")

        k = cv2.waitKey(1)


###QUIT BUTTONS
#         if k == ord('1'):
        if GPIO.input(23) == GPIO.LOW or k == ord('1'): #button GPIO 23

            cap.release()
            cv2.destroyAllWindows()
            time.sleep(2)
            vr.run_thread1("Activating Text Recognition")

          #  camera = cv2.VideoCapture('http://192.168.1.39:8080/video')
#             width = 480
#             height = 272
            width = 480
            height = 272
            camera = cv2.VideoCapture(0)
#             camera.set(3,640)
#             camera.set(4,480)
            while True:
                _,image=camera.read()
                image = cv2.resize(image, (width, height))
                ##
        

                cv2.imshow('text detection', image)
#                 if cv2.waitKey(1)& 0xFF ==ord("1"):
                if cv2.waitKey(1)& GPIO.input(23) == GPIO.LOW or cv2.waitKey(1)& 0xFF ==ord("1"):

                    time.sleep(1.5)
                    
                    vr.run_thread1("Captured! Please wait for a while. it processing the text. To Activate Text recognition. Press button 1. To activate Gps Location. Press Button 2.")

                    cv2.imwrite(r'/home/pi/Downloads/shot.jpg',image)
                    break
            camera.release()
            cv2.destroyAllWindows()
            tesseract()
            detection()
            
            
            break
        if GPIO.input(24) == GPIO.LOW or k ==ord('2'):

#         if k ==ord('2'):
            vr.run_thread1("Searching GPS")

            time.sleep(3)
            cap.release()
            cv2.destroyAllWindows()

            locationalarm()
            time.sleep(2)
            detection()
        if k == ord('q'):
            cap.release()
            cv2.destroyAllWindows()
            

#             button3()
            
            break

    cap.release()
    cv2.destroyAllWindows()
    
    
#without bounding box

    

#text recognition

def tesseract():
    try:
        reader = easyocr.Reader(['en'])
        IMAGE_PATH = r'/home/pi/Downloads/shot.jpg'
        result = reader.readtext(IMAGE_PATH)
        
        if not result: # If no text is detected
            vr.run_thread1("No text detected")
            return
        
        top_left = tuple(result[0][0][0])
        bottom_right = tuple(result[0][0][2])
        text = result[0][1]
        font = cv2.FONT_HERSHEY_SIMPLEX
        img = cv2.imread(IMAGE_PATH)
        spacer = 100
        for detections in result: 
            
            top_left = tuple(detections[0][0])
            bottom_right = tuple(detections[0][2])
            text = detections[1]
            img = cv2.rectangle(img,top_left,bottom_right,(0,255,0),3)
            img = cv2.putText(img,text,(20,spacer), font, 1,(255,255,0),2,cv2.LINE_AA)
            spacer+=30
            print(text)
            alarm_sound = pyttsx3.init()
            alarm_sound.say(text)
            alarm_sound.runAndWait()
            cv2.imwrite(r'/home/pi/Downloads/result.jpg',img)

    except:
        print("Error occurred while processing image.")        
  
            

   


detection()



