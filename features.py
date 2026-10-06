import os
import re
import struct
import subprocess
from playsound import playsound
import webbrowser
import sqlite3  
import eel
import pvporcupine
import pyaudio
import pyautogui


from engine.config import ASSISTANT_NAME
import pywhatkit as kit
import time
from engine.helper import extract_yt_term
con = sqlite3.connect("coco.db")
cursor = con.cursor()
@eel.expose


#PLAYING SOUND WHEN ASSISTANT SPEAKS

def playAssistantSound():
    music_dir = "www\\assets\\audio\\tick-sound-effect-1-336779.mp3"
    playsound(music_dir)


@eel.expose
def openCommand(query):
    query = query.replace("ASSISTANT_NAME", "")  
    query = query.replace("open", "")
    query=query.strip().lower()

    app_name = query.strip() 

    if app_name != "": # type: ignore
        try:
        
            cursor.execute('SELECT path FROM sys_command WHERE name IN (?)', (app_name,)) # type: ignore
            result = cursor.fetchall() # type: ignore

            if len (result) !=0: # type: ignore
                speak("opening " + query) # type: ignore
                os.startfile(result[0][0]) # type: ignore

            elif len (result) ==0:  # type: ignore
                
                cursor.execute('SELECT url FROM web_command WHERE name In (?)', (app_name,)) # type: ignore
                result = cursor.fetchall() # type: ignore

                if len (result) !=0: # type: ignore
                    speak("opening " + query) # type: ignore
                    webbrowser.open(result[0][0]) # type: ignore
                else:
                
                    speak("Opening " + query) # type: ignore
                    try:
                        os.system("start " + query) # type: ignore
                    except  :
                        speak("not found") # type: ignore

        except:
            speak("something went wrong") # type: ignore

@eel.expose
def PlayYoutube(query):
   search_term = extract_yt_term(query)
   speak("Playing " + search_term + " on youtube") # type: ignore
   kit.playonyt(search_term)



def hotword():
    porcupine = None
    paud = None
    audio_stream = None
    try:
        porcupine = pvporcupine.create(keywords=["coco", "alexa"])
        paud = pyaudio.PyAudio()
        audio_stream = paud.open(
            rate=porcupine.sample_rate,
            channels=1,
            format=pyaudio.paInt16,
            input=True,
            frames_per_buffer=porcupine.frame_length
        )
     
        while True:
            keyword = audio_stream.read(porcupine.frame_length)
            keyword = struct.unpack_from("h" * porcupine.frame_length, keyword)

            keyword_index = porcupine.process(keyword)

            if keyword_index >= 0:
                print("hotword detected")
                # win+k
                import pyautogui as autogui
                autogui.keyDown("win")
                autogui.press("k")
                time.sleep(2)
                autogui.keyUp("win")

    except:
        if porcupine is not None:
            porcupine.delete()
        if audio_stream is not None:
            audio_stream.close()
        if paud is not None:
            paud.terminate()
            hotword()
# Find Contacts
def findContact(query):
    
    
    words_to_remove = [ASSISTANT_NAME, 'make', 'a', 'to', 'phone', 'call', 'send', 'message', 'wahtsapp', 'video']
    query = remove_words(query, words_to_remove) # type: ignore

    try:
        query = query.strip().lower()
        cursor.execute("SELECT mobile_no FROM contacts WHERE LOWER(name) LIKE ? OR LOWER(name) LIKE ?", ('%' + query + '%', query + '%'))
        results = cursor.fetchall()
        print(results[0][0])
        mobile_number_str = str(results[0][0])
        if not mobile_number_str.startswith('+91'):
            mobile_number_str = '+91' + mobile_number_str

        return mobile_number_str, query
    except:
        speak('not exist in contacts') # type: ignore
        return 0, 0
    
def whatsApp(mobile_no, message, flag, name):

    if flag == 'message':
        target_tab = 12
        jarvis_message = "message send successfully to "+name

    elif flag == 'call':
        target_tab = 7
        message = ''
        jarvis_message = "calling to "+name

    else:
        target_tab = 6
        message = ''
        jarvis_message = "staring video call with "+name

    # Encode the message for URL
    encoded_message = quote(message) # type: ignore

    # Construct the URL
    whatsapp_url = f"whatsapp://send?phone={mobile_no}&text={encoded_message}"

    # Construct the full command
    full_command = f'start "" "{whatsapp_url}"'

    # Open WhatsApp with the constructed URL using cmd.exe
    subprocess.run(full_command, shell=True) # type: ignore
    time.sleep(5)
    subprocess.run(full_command, shell=True)
    
    pyautogui.hotkey('ctrl', 'f')

    for i in range(1, target_tab):
        pyautogui.hotkey('tab')

    pyautogui.hotkey('enter')
    speak(jarvis_message) # type: ignore
