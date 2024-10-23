import pyttsx3
import speech_recognition as sr
import webbrowser
import smtplib
import datetime
import requests
import pyjokes
import pywhatkit
import os

# Initialize text-to-speech engine
engine = pyttsx3.init()
engine.setProperty('voice', pyttsx3.init().getProperty('voices')[0].id)

def speak(text):
    """Convert text to speech."""
    engine.say(text)
    engine.runAndWait()

def listen():
    """Listen for a command and return it as text."""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)
    try:
        print("Recognizing...")
        query = recognizer.recognize_google(audio, language='en-in')
        print(f"User said: {query}")
    except sr.UnknownValueError:
        speak("Sorry, I did not understand.")
        return None
    except sr.RequestError:
        speak("Sorry, my speech service is down.")
        return None
    return query.lower()

def get_text_input():
    """Get text input from the user."""
    return input("Please type your command: ").lower()

def search_google(query):
    """Search Google with the given query."""
    webbrowser.open(f"https://www.google.com/search?q={query}")

def get_time():
    """Get the current time and return it as a string."""
    return datetime.datetime.now().strftime("%H:%M:%S")

def send_email(to, subject, body):
    """Send an email with the specified subject and body."""
    from_email = "youremail@gmail.com"
    password = "your-password"
    
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(from_email, password)
        message = f"Subject: {subject}\n\n{body}"
        server.sendmail(from_email, to, message)
        server.quit()
        speak("Email has been sent!")
    except Exception as e:
        print(e)
        speak("Sorry, I could not send the email.")

def get_input_mode():
    """Ask the user if they prefer speaking or typing."""
    speak("Would you like to speak or type your command?")
    mode = input("Enter 'speak' to use voice commands or 'type' to type your commands: ").lower()
    return mode

def main():
    speak("I am your assistant. How can I help you today?")
    
    input_mode = get_input_mode()  # Get input mode (speak or type)
    
    while True:
        query = None  # Initialize query before assigning it

        if input_mode == 'speak':
            query = listen()  # Use voice commands
        elif input_mode == 'type':
            query = get_text_input()  # Use text input
        else:
            speak("Invalid input mode.")
            input_mode = get_input_mode()  # Ask again
            continue  # Continue loop to avoid referencing uninitialized 'query'

        if query is None:
            continue

        if 'search' in query:
            search_query = query.replace("search", "")
            search_google(search_query)
            speak(f"Searching Google for {search_query}")

        elif 'time' in query:
            current_time = get_time()
            speak(f"The current time is {current_time}")

        elif 'open' in query:
            website = query.replace("open", "").strip().lower()
            if 'notepad' in website:
                os.startfile('notepad.exe')  # Open Notepad from the device
                speak("Opening Notepad")
            else:
                webbrowser.open(f"https://{website}.com")
                speak(f"Opening {website}")

        elif 'play' in query:
            song = query.replace("play", "").strip()
            speak(f"Playing {song} on YouTube")
            pywhatkit.playonyt(song)  # Play song or video on YouTube

        elif 'email' in query:
            speak("Who should I send the email to?")
            to = listen() if input_mode == 'speak' else get_text_input()
            if to:
                speak("What is the subject of the email?")
                subject = listen() if input_mode == 'speak' else get_text_input()
                if subject:
                    speak("What is the body of the email?")
                    body = listen() if input_mode == 'speak' else get_text_input()
                    if body:
                        send_email(to, subject, body)

        elif 'joke' in query:
            joke = pyjokes.get_joke()
            speak(joke)

        # Shutdown, Restart, and Lock system features
        elif 'shutdown' in query:
            speak("Shutting down the system")
            os.system("shutdown /s /t 1")  # Shutdown command for Windows

        elif 'restart' in query:
            speak("Restarting the system")
            os.system("shutdown /r /t 1")  # Restart command for Windows

        elif 'lock' in query:
            speak("Locking the system")
            os.system("rundll32.exe user32.dll,LockWorkStation")  # Lock system for Windows

        elif 'exit' in query:
            speak("Goodbye! Hope you have a wonderful day!")
            break

if __name__ == "__main__":
    main()
