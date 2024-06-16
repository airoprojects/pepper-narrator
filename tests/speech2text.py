import speech_recognition as sr

# Initialize recognizer
r = sr.Recognizer()

# Capture data from microphone
with sr.Microphone() as source:
    print("Say something!")
    audio = r.listen(source)

# Recognize speech using Google Web Speech API
try:
    print("Google Speech Recognition thinks you said:")
    print(r.recognize_google(audio))
except sr.UnknownValueError:
    print("Google Speech Recognition could not understand audio")
except sr.RequestError as e:
    print("Could not request results; {0}".format(e))
