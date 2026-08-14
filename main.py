import speech_recognition as sr
import webbrowser
import pyttsx3

recognizer = sr.Recognizer()
engine = pyttsx3.init()

def speak(text):
    engine.say(text)
    engine.runAndWait()
    
if __name__ == "__main__":
    speak("Initializing Simmba.....")
    while True: 

        # Listen for the wake word Simmba
        #obtain audio from microphone
        # obtain audio from the microphone
        # obtain audio from the microphone
        r = sr.Recognizer()
        with sr.Microphone() as source:
            print("Listening ....")
            audio = r.listen(source, timeout = 2, phrase_time_limit=1)
        
        # recognize speech using google
        print("Recognizing...")
        try:
            command = r.recognize_google(audio)
            print(command)    
            
        except sr.UnknownValueError:
            print("Simmba could not understand audio")
        except sr.RequestError as e:
            print("Simmba error; {0}".format(e))


