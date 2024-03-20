import openai
import pyttsx3
import speech_recognition as sr
import pyaudio

openai.api_key = "add here you key"
model_engine = "gpt-3.5-turbo"

# initialize text-to-speech engine
engine = pyttsx3.init()

# set the voice property to a different voice
voices = engine.getProperty('voices')
engine.setProperty('voice',voices[1].id)

# create a object 
r = sr.Recognizer()
r.energy_threshold = 5000

isTrue = True

engine.say("How can I help you?")
engine.runAndWait()

while isTrue:

    # listen for user input
    with sr.Microphone() as source:
        print("Speak: ")
        audio = r.listen(source)

    try:
        userInput = r.recognize_google(audio)
        print("You said: ", userInput)

    except sr.UnknownValueError:
        print("Speech recognition could not understand audio.")
        continue
    
    except sr.RequestError as e:
        print("Could not request results from google speech recognition service ; {0}".format(e))
        continue

    # userInput = input("Ask : ")
    if userInput == 'get lost':
        isTrue = False

    response = openai.ChatCompletion.create(
        model = 'gpt-3.5-turbo',
        messages = [
            {'role':'system','content':'You are a helpful assistant.'},
            {'role':'user', 'content':userInput},
        ])
    message = response.choices[0]['message']
    print('{}:{}'.format(message['role'],message['content']))

    # speak the response
    engine.say(message['content'])
    engine.runAndWait()