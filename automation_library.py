"""this is a smale automation code. it works effectively in only my pc.it donot think. just do what i tell in code"""
import speech_recognition as sr
from playsound import playsound
import pyautogui
import time
from PIL import ImageGrab
from groq import Groq
import re
import asyncio
import os, time
import edge_tts
from playsound import playsound
import speech_recognition as sr
from deep_translator import GoogleTranslator


def mixed_speech_to_english():
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("🎙️ Speak in Telugu or English...")
        recognizer.adjust_for_ambient_noise(source, duration=0.8)
        audio = recognizer.listen(source, phrase_time_limit=10)

    try:
        print("🧠 Recognizing...")
        # Try Telugu first
        try:
            telugu_text = recognizer.recognize_google(audio, language="te-IN")
            if telugu_text and any('\u0C00' <= ch <= '\u0C7F' for ch in telugu_text):
                translated = GoogleTranslator(source='te', target='en').translate(telugu_text)
                print(f"🗣 Telugu Text: {telugu_text}")
                print(f"🌍 English Translation: {translated}")
                return translated
        except:
            pass  # If Telugu recognition fails, fall back to English

        # Then try English
        english_text = recognizer.recognize_google(audio, language="en-IN")
        print(f"🗣 English Text: {english_text}")
        return english_text

    except sr.UnknownValueError:
        print("⚠️ Could not understand your speech.")
        return None
    except sr.RequestError:
        print("🚫 Network error or Google Speech API unavailable.")
        return None


info="""
This is a program that automate your work.You can just type/speek in normal language it can understand and do that particular work.
you can normally ask any questions or talk with this , it gives you the responce.this is a deepseek api. it supports both telugu and english languages
Here is the list of tasks that this program is capable to do.

 open Chrome and search given text
 open YouTube and search video and play the first vedio in the page
 only open YouTube
 just open ChatGPT
 open ChatGPT and search given text
 open WhatsApp
 send a WhatsApp message to a person of gien name
 send multiple WhatsApp messages to the person of given count
 open camera and takes a picture
 run the file → run filename
 play Chrome Dino game by its own
 put pc in sleep
 shutdown PC
 shows all activities information

note:it will work effectively in my pc only.
"""

API_KEY = "AIP key here"
client = Groq(api_key=API_KEY)


def convert_to_command(user_input):
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        temperature=1.5,   # NO creativitytext
        
        max_tokens=30,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are Jarvis, a STRICT command classifier.\n"
                    "If input clearly matches a rule, return ONLY that command.\n"
                    "If input does NOT match any rule, return: chat_bot <text>\n"
                    "Do NOT explain. Do NOT add extra words."
                )
            },
            {
                "role": "user",
                "content": f"""Rules:
To open Chrome and search text → chrome text
To open YouTube and search video → youtube text
To open YouTube → youtube
To just open ChatGPT → chatgpt
To open ChatGPT and search text → chatgpt text
To open WhatsApp → whatsapp
To send a WhatsApp message → whatsapp name_message
To send multiple WhatsApp messages → whatsapp name_message_count
To open camera for picture → camera
To run the file → run filename
To play Chrome Dino game → chromedyno
To put pc in sleep → sleep
To shutdown PC or turn off pc → off
To show all activities information or to show this program information → info
If input is normal chat or question → chat_bot text

Examples:
Input: open youtube
Output: youtube

Input: open youtube and play a song
Output: youtube play a song

Input: open chatgpt and search what is python
Output: chatgpt what is python

Input: open whatsapp and send hello to rajesh anna 10 times
Output: whatsapp rajesh_hello_10

Input: run  oa
Output: run oa

Output: chat_bot what is python

Input: what is python
Output: chat_bot what is python

Now workout on this Input: {user_input}
"""
            }
        ]
    )

    command = response.choices[0].message.content.strip()
    print("Command:", command)
    return command


def open_chrome(Input):    
    # Step 1: Open Run dialog (Win + R)
    pyautogui.hotkey('win', 'r')
    time.sleep(1)

    # Step 2: Type 'chrome' and press Enter
    pyautogui.typewrite('chrome')
    pyautogui.press('enter')
    time.sleep(2)  # Wait for Chrome to open fully
    
    pyautogui.typewrite(Input)
    pyautogui.press('enter')
    
def camera():    
    pyautogui.hotkey('win')
    time.sleep(1)

    pyautogui.typewrite('camera')
    time.sleep(1)
    pyautogui.press('enter')
    time.sleep(3) 
    pyautogui.press('enter')

def open_youtube(Input):
    open_chrome('youtube.com')
    time.sleep(6)  # Wait for YouTube to load

    if Input:
        # Step 4: Move focus to YouTube search bar
        for _ in range(4):  # Press Tab 4 times
            pyautogui.press('tab')
            time.sleep(0.3)
        # Step 5: Type the search query and press Enter
        pyautogui.typewrite(Input)
        pyautogui.press('enter')
        
        time.sleep(1)
        #to click the first vedio 
        pyautogui.moveTo(450, 330, duration=1)
        pyautogui.click()    

def open_chatgtp(Input):
    open_chrome('chatgpt')
    time.sleep(4)  # Wait for chatgpt to load

    # Step 5: Type the search query and press Enter
    if Input!="":
        pyautogui.typewrite(Input)
        pyautogui.press('enter')

def run_sc(Input):
    pyautogui.hotkey('win', 'r')
    time.sleep(1)

    pyautogui.typewrite('cmd')
    pyautogui.press('enter')
    time.sleep(1) 
    pyautogui.typewrite(Input)
    pyautogui.press('enter')
    pyautogui.typewrite(f'python app.py')
    pyautogui.press('enter')
    time.sleep(1) 
    open_chrome('http://127.0.0.1:5000')

def run(Input):
    if Input=="oa":
        run_sc('cd Desktop\T.vishnu.s.m\projects\projects using flask\online_attendance_flask')
        
    elif Input=="tm":
        run_sc(r'cd Desktop\T.vishnu.s.m\projects\projects using flask\task_manager_project')
        
    elif Input=="rps":
        run_sc(r'cd Desktop\T.vishnu.s.m\projects\projects using flask\rps_game_files')
        
    else:
        pyautogui.hotkey('win', 'r')
        time.sleep(1)

        pyautogui.typewrite('cmd')
        pyautogui.press('enter')
        time.sleep(1) 
        pyautogui.typewrite('cd Desktop\T.vishnu.s.m\programs')
        pyautogui.press('enter')
        pyautogui.typewrite(f'python {Input}.py')
        pyautogui.press('enter')
        
    
def whatsapp(Input):
    open_chrome('https://web.whatsapp.com/.com')
    time.sleep(9) 
    if Input:
        data=Input.split("_")
        name=data[0]
        message=data[1]
        if len(data)==3 :
            n=int(data[2])
        else:
            n=1

        pyautogui.moveTo(280, 180, duration=1)
        pyautogui.click()
        pyautogui.typewrite(name)
        time.sleep(1)
        pyautogui.press('enter')
        for _ in range(n):
            pyautogui.typewrite(f'{message}')
            pyautogui.press('enter')


def obstacle_detected():
    img = ImageGrab.grab(bbox=(x1, y1, x2, y2))  # Capture the rectangular area
    colors = img.getcolors(img.size[0] * img.size[1])  # Get all colors in the area
    for count, color in colors:
        if color == obstacle:
            return True
    return False
    
# Obstacle color
obstacle = (83, 83, 83)
# Define the rectangular area where obstacles appear (adjust coordinates for your game)
# For Chrome Dino: just in front of the dinosaur
x1, y1 = 460 , 293  # Top-left corner
x2, y2 = 560, 316  # Bottom-right corner

def play_game():
    open_chrome('https://chromedino.com')
    time.sleep(3)
    pyautogui.press('space')
    while True:
        if obstacle_detected():
            pyautogui.press('space')
            #time.sleep(0.2)
            #pyautogui.press('down')
        time.sleep(0.01)

def shut_down():
    pyautogui.hotkey('win', 'x')
    pyautogui.press('u')
    pyautogui.press('u')
    
def sleep():
    pyautogui.hotkey('win', 'x')
    pyautogui.press('u')
    pyautogui.press('s')
    
async def speak(text):
    #print(text)
    output_file = f"temp_{int(time.time())}.mp3"
    tts = edge_tts.Communicate(text, "en-IN-AaravNeural")
    await tts.save(output_file)
    playsound(output_file)
    os.remove(output_file)
    

def clean_markdown(text):
    # Remove markdown symbols like **, __, `, >, etc., but keep structure
    text = re.sub(r'[*_`>~\-]+', '', text)

    # Replace markdown headings (###, ##, #) with line breaks
    text = re.sub(r'\s*#{1,6}\s*', '\n', text)

    # Add line breaks before bullet points (•, -, or numbers with .)
    text = re.sub(r'(\n)?\s*[\-\*\•]\s*', r'\n• ', text)

    # Ensure numbered points like 1. or 2) start on new lines
    text = re.sub(r'(\d+[\.\)])\s*', r'\n\1 ', text)

    # Replace multiple newlines with a single blank line for spacing
    text = re.sub(r'\n\s*\n+', '\n\n', text)

    # Keep double newlines between paragraphs
    return text.strip()

    

conversation_history = [
    {
        "role": "system",
        "content": (
            "You are a helpful and concise AI assistant. "
            "Your name is jarvis. Always reply clearly without using markdown symbols "
            "like ** or ###.\n"
            "Example format:\n"
            "1. Start with the Basics\n"
            "Learn common greetings: Hello, Hi, Good morning, How are you?\n"
            "Simple phrases: My name is…, I am from…, Thank you, Please, Sorry."
        )
    }
]

def chat(user_input):
    global conversation_history

    # Add user message
    conversation_history.append({
        "role": "user",
        "content": user_input
    })

    # Keep last 10 messages
    if len(conversation_history) > 10:
        conversation_history = conversation_history[-10:]

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        temperature=0.3,
        max_tokens=500,
        messages=conversation_history
    )

    reply = response.choices[0].message.content.strip()
    print("response:", reply)
    #asyncio.run(speak(clean_markdown(reply)))

    # Add assistant reply to history
    conversation_history.append({
        "role": "assistant",
        "content": reply
    })

    return reply
   
        
def main(text):         
    command=convert_to_command(text)
    #print(f"command:{command}")
    activities = command.split(" ",1)
    m_cmd=activities[0].lower()
    match m_cmd.strip():
        case 'chat_bot':
            chat(activities[1])
        case 'youtube':
            if len(activities)==2:
                open_youtube(activities[1])
            else:
                open_youtube("")
        case 'chatgpt':
            if len(activities)==2:
                open_chatgtp(activities[1])
            else:
                open_chatgtp("")
        case 'chrome':
            open_chrome(activities[1])
        case 'run':
            run(activities[1].lower())
        case 'whatsapp':
            if len(activities)==2:
                whatsapp(activities[1])
            else:
                whatsapp("")
        case 'chromedyno':
            play_game()
        case 'camera':
            camera()
        case 'off':
            shut_down()
        case 'sleep':
            sleep()
        case 'info':
            print(info)
        
        
 

   

  
