import speech_recognition as sr
import webbrowser
import pyttsx3
import requests
import musiclibrary

recognizer = sr.Recognizer()
newsapi = "pub_ab1b518f74cb4d5fb8d38a2711c4412f"


def speak(text):
    """
    Initializes a fresh instance of pyttsx3 every time to prevent
    the engine loop from silently breaking or hanging.
    """
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()
    del engine  # Destroy the instance to free audio drivers

def processCommand(c):
    if "open google" in c.lower():
        webbrowser.open("https://google.com")
    elif "open youtube" in c.lower():
        webbrowser.open("https://www.youtube.com/")
    elif "open github" in c.lower():
        webbrowser.open("https://github.com")
    elif "open linkedin" in c.lower():
        webbrowser.open("https://linkedin.com")
    elif c.lower().startswith("play"):
        song = c.lower().split(" ")[1]
        link = musiclibrary.music[song]
        webbrowser.open(link)
   
    elif "news" in c.lower():
        speak("Fetching latest Indian headlines in English.")
        # FIX 1: Filtered URL by language and country
        url = f"https://newsdata.io/api/1/latest?apikey=pub_ab1b518f74cb4d5fb8d38a2711c4412f&language=en&country=in"
        r = requests.get(url)
        
        if r.status_code == 200:
            data = r.json()
            articles = data.get('results', [])
            
            if not articles:
                speak("No English news articles found for this region.")
                return

            for article in articles[:3]:
                headline = article.get('title')
                if headline:
                    # FIX 2: Remove confusing special symbols like em-dashes
                    headline = headline.replace(" - ", " from ").replace(" — ", " from ")
                    
                    print(f"Jarvis says: {headline}")
                    speak(headline)
        else:
            print(f"API Error Code: {r.status_code}")
            speak("Sorry, I am facing an API connection issue.")
    else:
        #ai integration




if __name__ == "__main__":
    speak("Initializing Jarvis.....")
    
    # Calibrate background noise once at startup
    with sr.Microphone() as source:
        print("Adjusting for ambient noise... Please wait.")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        
    while True: 
        print("\nListening for wake word 'Jarvis'...")
        
        # STEP 1: Open mic ONLY to listen for the wake word
        with sr.Microphone() as source:
            try:
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=3)
                word = recognizer.recognize_google(audio)
                print(f"Heard: {word}")
            except (sr.WaitTimeoutError, sr.UnknownValueError):
                continue
            except sr.RequestError as e:
                print(f"API Error: {e}")
                continue

        # Mic is CLOSED here. Safe for pyttsx3 to speak.
        if "jarvis" in word.lower():
            speak("Ya")
            print("Jarvis Active... Speak your command.")
            
            # STEP 2: Reopen mic ONLY to listen for the command
            with sr.Microphone() as source:
                try:
                    audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
                    command = recognizer.recognize_google(audio)
                    print(f"Command heard: {command}")
                except (sr.UnknownValueError, sr.WaitTimeoutError):
                    print("Could not understand the command.")
                    continue

            # Mic is CLOSED here. Safe to run processCommand / speak again.
            processCommand(command)
