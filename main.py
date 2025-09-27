import speech_recognition as sr
import os
import webbrowser
import datetime
import random

import pyttsx3
import playsound

from openai import OpenAI

# Initialize OpenAI client
client = OpenAI(api_key="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")  # Replace with your actual GPT-4o API key

# Initialize TTS engine
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('rate', 166)
engine.setProperty('volume', 1.0)
engine.setProperty('voice', voices[1].id)

chat_history = ""

def say(text):
    print(f"Friday: {text}")
    engine.say(text)
    engine.runAndWait()

def chat(query):
    global chat_history
    chat_history += f"Human: {query}\nFriday: "

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are Friday, an intelligent AI assistant."},
                {"role": "user", "content": chat_history}
            ]
        )
        answer = response.choices[0].message.content
        say(answer)
        chat_history += answer + "\n"
        return answer
    except Exception as e:
        say("Sorry, I encountered an error with OpenAI.")
        print(e)
        return "Error"

def ai(prompt):
    try:
        say("Working on your request...")
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ]
        )
        answer = response.choices[0].message.content
        os.makedirs("Openai", exist_ok=True)
        filename = f"Openai/{'_'.join(prompt.split()[:5])}_{random.randint(100,999)}.txt"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(f"Prompt: {prompt}\n\nResponse:\n{answer}")
        say("Response saved.")
    except Exception as e:
        say("Error while getting response from OpenAI.")
        print(e)

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        try:
            audio = r.listen(source, timeout=None, phrase_time_limit=8)
            print("Recognizing...")
            query = r.recognize_google(audio, language="en-in")
            print(f"User said: {query}")
            return query
        except sr.UnknownValueError:
            print("Could not understand.")
            return ""
        except Exception as e:
            print("Error:", e)
            return ""

if __name__ == '__main__':
    say("Hi, I am Friday with GPT-4o. How may I help you?")
    while True:
        query = takeCommand().lower().strip()
        if not query:
            continue

        if "friday quit" in query:
            say("Goodbye sir, shutting down.")
            break

        elif "reset chat" in query:
            chat_history = ""
            say("Chat history cleared.")

        elif "open" in query:
            sites = [
                ["youtube", "https://www.youtube.com"],
                ["wikipedia", "https://www.wikipedia.org"],
                ["google", "https://www.google.com"],
                ["whatsapp", "https://web.whatsapp.com"]
            ]
            for site in sites:
                if site[0] in query:
                    say(f"Opening {site[0]}...")
                    webbrowser.open(site[1])
                    break

        elif "play music" in query:
            musicPath = "Believer(PaglaSongs).mp3"
            say("Playing music.")
            try:
                playsound.playsound(musicPath)
            except Exception as e:
                say("Couldn't play music.")
                print(e)

        elif "the time" in query:
            now = datetime.datetime.now()
            say(f"The time is {now.hour} hours and {now.minute} minutes.")

        elif "set alarm" in query:
            say("You can set the alarm manually, you lazy guy!")

        elif "open terminal" in query:
            try:
                os.system("start cmd")
                say("Opening terminal.")
            except:
                say("Failed to open terminal.")

        elif "friday" in query:
            ai(prompt=query)

        else:
            chat(query)
