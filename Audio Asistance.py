import os
import threading
import time
import streamlit as st
import speech_recognition as sr
import openai
from pydub import AudioSegment
from pydub.playback import play
from gtts import gTTS

# Set OpenAI API key
openai.api_key = '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'
ffmpeg_path = r'C:\gaurav\python\ffmpeg-6.1.1.tar.xz'
os.environ['PATH'] += os.pathsep + ffmpeg_path

# Initialize Streamlit UI
st.title("Tecnoprism - Voice Assistant")
st.text("Welcome to Atech. How may I assist you? Say 'Hello' to start, and 'Goodbye' to end the conversation.")
lang = 'en'
gender = 'female'

def generate_response(prompt):
    # Set the messages for chat-based completion
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": f"Generate answer for following statement:\n{prompt}"}
    ]

    # Call the OpenAI API to generate the summary
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # Use the chat-based language model
        messages=messages,
        max_tokens=150,  # Adjust the max_tokens parameter based on your desired summary length
        temperature=0.7,  # Adjust the temperature parameter for creativity
    )

    # Extract the generated summary from the API response
    summary = response['choices'][0]['message']['content'].strip()

    return summary

def take_command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        st.write("Listening...")
        r.pause_threshold = 3
        audio = r.listen(source)
    try:
        st.write("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        st.write(f"User said: {query}\n")
        return query.lower()
    except Exception as e:
        st.error(f"Error: {str(e)}")
        st.write("Say that again please...")
        return "None"

class TextToAudioConverter:
    def __init__(self, lang='en', gender='female'):
        self.lang = lang
        self.gender = gender

    def get_voice(self):
        voices = {
            'en': {
                'female': 'en'
            },
            # Add more languages and gender options as needed
        }
        lang_code = voices.get(self.lang, {}).get(self.gender, 'en')
        return lang_code

    def generate_audio_from_text(self, text, audio_output_path):
        if text:
            lang_code = self.get_voice()
            engine = gTTS(text=text, lang=lang_code, slow=False)
            engine.save(audio_output_path)

    def play_audio(self, audio_path):
        audio = AudioSegment.from_mp3(audio_path)
        play(audio)

    def delete_audio_file(self, audio_path):
        os.remove(audio_path)

    def combine_text_with_audio(self, text):
        audio_output_path = "output_audio.mp3"
        self.generate_audio_from_text(text, audio_output_path)
        self.play_audio(audio_output_path)
        # Delete the audio file after playback is completed
        self.delete_audio_file(audio_output_path)

def display(response):
    converter = TextToAudioConverter(lang, gender)
    converter.combine_text_with_audio(response)

a = False
while True:
    query = take_command()
    if 'hello' in query:
        a = True
        response = generate_response(query)
        st.write(f"System response: {response}\n")
        display(response)
    while a:
        query = take_command()
        if "thank you" in query or "goodbye" in query:
            display('Have a good day. Thank you for chatting with me.')
            a = False
            break
        else:
            response = generate_response(query)
            st.write(f"System response: {response}\n")
            display(response)
