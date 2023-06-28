import pyttsx3
import threading
engine = pyttsx3.init()
alarm_sound = pyttsx3.init()
voices = alarm_sound.getProperty('voices')
alarm_sound.setProperty('voice', 'english+f2')
alarm_sound.setProperty('rate', 140)



### VOICE RECONGITION FUNCTION


def speak_text1(text):
    try:
        alarm_sound = pyttsx3.init()
        alarm_sound.say(text)
        alarm_sound.runAndWait()
    except:
        pass
    
def speak_text2(text1, text2):
    try:
        alarm_sound = pyttsx3.init()
        alarm_sound.say(text1 + text2)
        alarm_sound.runAndWait()
    except:
        pass
def speak_text3(text1, text2, text3):
    try:
        alarm_sound = pyttsx3.init()
        alarm_sound.say(text1 + text2 + text3)
        alarm_sound.runAndWait()
    except:
        pass
def speak_text4(text1, text2, text3, text4):
    try:
        alarm_sound = pyttsx3.init()
        alarm_sound.say(text1 + text2 + text3 +text4)
        alarm_sound.runAndWait()
    except:
        pass   
def run_thread1(text):
    try:
        
        thread = threading.Thread(target=speak_text1, args=(text,))
        thread.start()
    except:
        pass
    

def run_thread2(text1, text2):
    try:
            
        thread = threading.Thread(target=speak_text2, args=(text1, text2))
        thread.start()
    except:
        pass
def run_thread3(text1, text2, text3):
    try:
            
        thread = threading.Thread(target=speak_text3, args=(text1, text2, text3))
        thread.start()
    except:
        pass
        pass
def run_thread4(text1, text2, text3, text4):
    try:
            
        thread = threading.Thread(target=speak_text4, args=(text1, text2, text3, text4))
        thread.start()
    except:
        pass
    
    
if __name__ == "__main__":
    text = "hello this is my voice"
    run_thread4("text","tex1","tex2","text4")
    
