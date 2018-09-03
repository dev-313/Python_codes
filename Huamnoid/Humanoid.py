import sys
import json
import time
import os.path
from subprocess import call
import speech_recognition as sr
from gtts import gTTS

try:
    import apiai

except ImportError:
    sys.path.append(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir)
    )
    import apiai


CLIENT_ACCESS_TOKEN = 'ee827bba7142436b9d4c3be52187bbe2'


def audio_to_text():
    recognize_obj = sr.Recognizer()

    with sr.Microphone() as source:                                                                       
        audio = recognize_obj.listen(source)   

    try:
        return (recognize_obj.recognize_google(audio))

    except Exception as e:
        return ("Could not understand audio")



def AI_response():
    ai = apiai.ApiAI(CLIENT_ACCESS_TOKEN)

    print ("Please Wait...")

    request = ai.text_request()

    request.lang = 'de'  # optional, default value equal 'en'

    request.session_id = "<SESSION ID, UNIQUE FOR EACH USER>"
    
    request.query = audio_to_text()

    print ("Processing Statement...")

    response = request.getresponse()

    return (response.read())


def AIresponse_to_audio():
    response = AI_response()
    response_dict = json.loads(response)
    response_text = response_dict["result"]["fulfillment"]["speech"]
    time.sleep(5)
    print (response_text)
    #call(['espeak -g7 -s150 -ven+f3 "'+response_text+'"'],shell=True)
    #return "DONE"
    language = 'en'

    myobj = gTTS(text=response_text, lang=language, slow=False)
 

    myobj.save("welcome.mp3")
 

    os.system("mpg321 welcome.mp3")



if __name__ == '__main__':

    while True:
          input_state = input("press s to speak: ")
          input_state = input_state.lower()
          if input_state == 's':
              print('Listening...')
              print(AIresponse_to_audio())
              print("Stopped Listening...")
          else:
              print ("Idle...")
              time.sleep(1)

