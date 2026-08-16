import speech_recognition as sr
import webbrowser
import pyttsx3
import requests
import musiclibrary
import ollama
from dotenv import load_dotenv
from cryptography.fernet import Fernet
import os
import json, time

load_dotenv()

recognizer = sr.Recognizer()
newsapi = os.getenv('NEWS_API_KEY')
HISTORY_FILE = "history.json"
EXPIRY_SECONDS = 86400
key = os.getenv("FERNET_KEY")
cipher = Fernet(key)


def speak(text):
    """
    Initializes a fresh instance of pyttsx3 every time to prevent
    the engine loop from silently breaking or hanging.
    """
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()
    del engine  # Destroy the instance to free audio drivers

def aiProcess(command):
    """
    Sends the user's voice command to the locally running llama3.1
    model via Ollama and returns the generated response.
    """
    try:
        response = ollama.chat(
            model = "llama3.1",
            messages=[
                {
                    'role':'system',
                    'content':'You are a well-behaved and polite virtual assistant named Friday. '
                               'Give short, direct, and to-the-point answers. '
                               'Use simple, easy, and clearly understandable Indian English words. '
                               'Answers should be 2-3 lines long.'
                },
                {
                    'role':'user',
                    'content':command 
                }
            ]
        )
        return response['message']['content']
    except Exception as e:
        return f"Sorry, I encountered an error connecting to Ollama: {str(e)}"

def processCommand(c):
    if "open google" in c.lower():
        webbrowser.open("https://google.com")
    elif "open youtube" in c.lower():
        webbrowser.open("https://youtube.com")
    elif "open github" in c.lower():
        webbrowser.open("https://github.com")
    elif "open linkedin" in c.lower():
        webbrowser.open("https://linkedin.com")
    elif c.lower().startswith("play"):
        song = c.lower().replace("play ", "", 1)   # remove the word "play"
        link = musiclibrary.music[song]
        webbrowser.open(link)


   
    elif "news" in c.lower():
        speak("Fetching latest Indian headlines in English.")
        url = f"https://newsdata.io/api/1/latest?apikey={newsapi}&language=en&country=in"
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
                    headline = headline.replace(" - ", " from ").replace(" — ", " from ")
                    print(f"Friday says: {headline}")
                    speak(headline)
        else:
            print(f"API Error Code: {r.status_code}")
            speak("Sorry, I am facing an API connection issue.")
    elif "history" in c.lower():
        show_history()
    else:
        # ai integration
        output = aiProcess(c)
        speak(output)
        save_history(c)

def save_history(command):
    entry = {"event": f"Command heard: {command}", "timestamp": time.time()}
    entry_json = json.dumps(entry).encode()
    encrypted = cipher.encrypt(entry_json).decode()
    with open(HISTORY_FILE, "a") as f:
        f.write(json.dumps({"ciphertext": encrypted}) + "\n")


def cleanup_history():
    if not os.path.exists(HISTORY_FILE):
        return

    fresh_entries = []
    now = time.time()

    with open(HISTORY_FILE, "r") as f:
        for line in f:
            if not line.strip():
                continue
            try:
                line_data = json.loads(line.strip())
                encrypted_str = line_data["ciphertext"]
                
                decrypted = cipher.decrypt(encrypted_str.encode())
                entry = json.loads(decrypted.decode())
                
                if now - entry["timestamp"] <= EXPIRY_SECONDS:
                    fresh_entries.append(entry)
            except Exception as e:
                print(f"Cleanup skip debug line: {e}")
                continue

    with open(HISTORY_FILE, "w") as f:
        for entry in fresh_entries:
            encrypted = cipher.encrypt(json.dumps(entry).encode()).decode()
            f.write(json.dumps({"ciphertext": encrypted}) + "\n")


def show_history():
    cleanup_history()
    if not os.path.exists(HISTORY_FILE):
        speak("No history found.")
        return
    
    events = []
    with open(HISTORY_FILE, "r") as f:
        for line in f:
            if not line.strip():
                continue
            try:
                line_data = json.loads(line.strip())
                encrypted_str = line_data["ciphertext"]
                
                decrypted = cipher.decrypt(encrypted_str.encode())
                entry = json.loads(decrypted.decode())
                print(entry)
                events.append(entry["event"])
            except Exception as e:
                print(f"Show history skip debug line: {e}")
                continue
    
    if events:
        speak("Here are your recent commands: " + ", ".join(events))
    else:
        speak("No structural history logs found.")




if __name__ == "__main__":
    speak("Initializing Friday.....")
    
    # Calibrate background noise once at startup
    with sr.Microphone() as source:
        print("Adjusting for ambient noise... Please wait.")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        
    while True: 
        print("\nListening for wake word 'Friday'...")
        
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
        if "friday" in word.lower():
            speak("Ya")
            print("Friday Active... Speak your command.")
            
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
