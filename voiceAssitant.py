import os
import speech_recognition as sr
import openai
from gtts import gTTS
import pyttsx3

# Set OpenAI API key
openai.api_key = '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'  # Replace with your actual OpenAI API key
def generate_response(prompt):
    # Set the messages for chat-based completion
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": f"Generate an answer for the following statement:\n{prompt}"}
    ]

    # Call the OpenAI API to generate the response
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-16k",
        messages=messages,
        max_tokens=256,
        temperature=0.5,
    )

    # Extract the generated response from the API response
    generated_text = response['choices'][0]['message']['content'].strip()

    return generated_text

def take_voice_command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 3
        audio = r.listen(source)
    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")
        return query.lower()
    except Exception as e:
        print(f"Error: {str(e)}")
        print("Say that again, please...")
        return "None"

def text_to_speech(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def voice_assistant():
    flag=0
    while True:
        query = take_voice_command()
        
        if 'goodbye' in query and flag == 1:
            text="It was nice to meet you , goodbye have great Day"
            print(text)
            text_to_speech(text)
            break

        elif 'hello' in query or flag == 1:
            flag = 1 
            response = generate_response(query)
            print(f"System response: {response}\n")

            # Convert the response to voice and play it
            text_to_speech(response)
            
        

if __name__ == "__main__":
    voice_assistant()