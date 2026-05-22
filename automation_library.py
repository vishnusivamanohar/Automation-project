"""this is a smale automation code. it works effectively in only my pc.it donot think. just do what i tell in code"""
import pyttsx3
import speech_recognition as sr
import pyautogui
import time
from PIL import ImageGrab
from groq import Groq
import re
import json
import os
from deep_translator import GoogleTranslator
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.tools import tool
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

load_dotenv()


def clean_markdown(text: str) -> str:
    """Removes common markdown formatting symbols to make text clean for speech and display."""
    text = re.sub(r'[*_`>~\-]+', '', text)
    text = re.sub(r'\s*#{1,6}\s*', '\n', text)
    text = re.sub(r'(\n)?\s*[\-\*\•]\s*', r'\n• ', text)
    text = re.sub(r'(\d+[\.\)])\s*', r'\n\1 ', text)
    text = re.sub(r'\n\s*\n+', '\n\n', text)
    return text.strip()


def speak(text: str):
    """Speaks the text using pyttsx3 Text-to-Speech engine."""
    clean_text = clean_markdown(text)
    engine = pyttsx3.init()
    engine.setProperty('rate', 180)
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[0].id)
    engine.say(clean_text)
    engine.runAndWait()


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
 change or mute system volume
 change or set screen brightness
 open the calculator
 take a screenshot and save it to the desktop

note:it will work effectively in my pc only.
"""

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
llm = ChatGroq(model="llama-3.3-70b-versatile", api_key=GROQ_API_KEY) 

def open_chrome(search_query: str = "") -> str:
    """Opens Google Chrome. If search_query is provided, types it in Google Chrome and presses enter."""
    # Step 1: Open Run dialog (Win + R)
    pyautogui.hotkey('win', 'r')
    time.sleep(1)

    # Step 2: Type 'chrome' and press Enter
    pyautogui.typewrite('chrome')
    pyautogui.press('enter')
    time.sleep(2)  # Wait for Chrome to open fully
    
    pyautogui.typewrite(search_query)
    pyautogui.press('enter')
    return "Chrome opened"
    
def open_app(app_name: str) -> str:
    """Opens a specific app or program (e.g. calculator, camera, visual studio, vs code) on the computer."""
    pyautogui.hotkey('win')
    time.sleep(1)
    pyautogui.typewrite(app_name)
    time.sleep(1)
    pyautogui.press('enter')
    time.sleep(2)
    return f"Opened {app_name}"

def open_youtube(search_query: str = "") -> str:
    """Opens YouTube in Google Chrome. If search_query is provided, searches for it and plays the first video in the results."""
    open_chrome(search_query='youtube.com')
    time.sleep(6)  # Wait for YouTube to load

    if search_query:
        # Step 4: Move focus to YouTube search bar
        for _ in range(4):  # Press Tab 4 times
            pyautogui.press('tab')
            time.sleep(0.3)
        # Step 5: Type the search query and press Enter
        pyautogui.typewrite(search_query)
        pyautogui.press('enter')
        
        time.sleep(1)
        #to click the first video 
        pyautogui.moveTo(450, 330, duration=1)
        pyautogui.click()    
    return "YouTube opened"

def open_chatgpt(search_query: str = "") -> str:
    """Opens ChatGPT in Google Chrome. If search_query is provided, types the query and sends it."""
    open_chrome(search_query='chatgpt')
    time.sleep(4)  # Wait for chatgpt to load

    # Step 5: Type the search query and press Enter
    if search_query != "":
        pyautogui.typewrite(search_query)
        pyautogui.press('enter')
    return "ChatGPT opened"


def run(program_name: str) -> str:
    """Runs a specific project or python file."""

    paths = {
        "hand_detection.py":r'python "C:\Users\HP\Desktop\T.vishnu.s.m\projects\ML projects\hand ditection\hand_detection.py"',
        "hand_detection2.py":r'python "C:\Users\HP\Desktop\T.vishnu.s.m\projects\ML projects\hand ditection\hand_detection2.py"',
        "hand_detection3.py":r'python "C:\Users\HP\Desktop\T.vishnu.s.m\projects\ML projects\hand ditection\hand_detection3.py"',
        "face_detection1.py":r'python "C:\Users\HP\Desktop\T.vishnu.s.m\projects\ML projects\face_recogization\p1.py"',
        "face_detection2.py":r'python "C:\Users\HP\Desktop\T.vishnu.s.m\projects\ML projects\face_recogization\p2.py"',
        "face_detection3.py":r'python "C:\Users\HP\Desktop\T.vishnu.s.m\projects\ML projects\face_recogization\p3.py"',
        "mouse control using hand detection":r'python "C:\Users\HP\Desktop\T.vishnu.s.m\projects\ML projects\hand ditection\main.py"',
        "rag project app.py":r'python "C:\Users\HP\Desktop\T.vishnu.s.m\projects\ML projects\llm engineering course projects\rag projects\app.py"',
        "rag project.py":r'python "C:\Users\HP\Desktop\T.vishnu.s.m\projects\ML projects\llm engineering course projects\rag projects\rag project.py"',
        "AI Quize app.py":r'python "C:\Users\HP\Desktop\T.vishnu.s.m\projects\projects using flask\AI Quize\app.py"',
        "online_attendance_flask app.py":r'python "C:\Users\HP\Desktop\T.vishnu.s.m\projects\projects using flask\online_attendance_flask\app.py"',
        "rps_game.html":r'start "" "C:\Users\HP\Desktop\T.vishnu.s.m\projects\projects using flask\rps_game_files\rps_game.html"',
        "task_manager app.py":r'python "C:\Users\HP\Desktop\T.vishnu.s.m\projects\projects using flask\task manager\app.py"',
        "task_manager_singlefile.html":r'start "" "C:\Users\HP\Desktop\T.vishnu.s.m\projects\projects using flask\task manager\task_manager_singlefile.html"',
        "task manager1 app.py":r'python "C:\Users\HP\Desktop\T.vishnu.s.m\projects\projects using flask\task_manager_project\app.py"',
        "my resume":r'start "" "C:\Users\HP\Desktop\T.vishnu.s.m\My_Resume.docx"'
    }

    prompt = f"""
    you are a helpfull assistent to find matching or similar key of user input from the list of keys provided below.
    Note if exact key is not found then return similar key

    keys:{list(paths.keys())}

    user input:"{program_name}"

    example:
    user input:"online attentance"
    matching key:"online_attendance_flask app.py"

    example 2:
    user input:"activate mouse controls"
    matching key:"mouse control using hand detection"

    your responce should be only key as a string nothing else
    """

    chat_response = llm.invoke(prompt)

    response = chat_response.content.strip().replace('"', '').replace("'", "")

    print("Matched Key :", response)

    matched_key = None

    for k in paths.keys():
        if k.lower() == response.lower():
            matched_key = k
            break

    if not matched_key:
        print(f"Could not match LLM response '{response}' to any path.")
        return f"Could not match program name: {program_name}"

    adders = paths[matched_key]

    # -----------------------------
    # Extract actual python file path
    # -----------------------------
    if adders.startswith("python"):

        file_path = adders.replace('python "', '').replace('"', '')

        # Get project folder
        folder_path = os.path.dirname(file_path)

        # ML projects root
        ml_root = r"C:\Users\HP\Desktop\T.vishnu.s.m\projects\ML projects"

        pyautogui.hotkey('win', 'r')
        time.sleep(0.5)

        pyautogui.typewrite('cmd')
        pyautogui.press('enter')

        time.sleep(1)

        # --------------------------------
        # If file belongs to ML projects
        # --------------------------------
        if "ML projects" in file_path:

            pyautogui.typewrite(f'cd /d "{ml_root}"')
            pyautogui.press('enter')

            time.sleep(0.5)

            # Activate venv
            pyautogui.typewrite(r'venv\Scripts\activate')
            pyautogui.press('enter')

            time.sleep(1)

        # Move to actual project folder
        pyautogui.typewrite(f'cd /d "{folder_path}"')
        pyautogui.press('enter')

        time.sleep(0.5)

        # Run file
        pyautogui.typewrite(f'python "{os.path.basename(file_path)}"')
        pyautogui.press('enter')

    else:
        # For HTML / DOCX
        pyautogui.hotkey('win', 'r')
        time.sleep(0.5)
        pyautogui.typewrite('cmd')
        pyautogui.press('enter')
        time.sleep(1)
        pyautogui.typewrite(adders)
        pyautogui.press('enter')
        
    return f"Started program: {program_name}"

def whatsapp(name: str, message: str, count: int = 1) -> str:
    """Sends a WhatsApp message containing `message` to the contact `name`. Optionally sends `count` times."""
    open_chrome(search_query='https://web.whatsapp.com/.com')
    time.sleep(9) 
    pyautogui.moveTo(280, 180, duration=1)
    pyautogui.click()
    pyautogui.typewrite(name)
    time.sleep(1)
    pyautogui.press('enter')
    for _ in range(count):
        pyautogui.typewrite(f'{message}')
        pyautogui.press('enter')
    return f"WhatsApp message sent to {name}"

def shut_down() -> str:
    """Shuts down the computer/PC."""
    pyautogui.hotkey('win', 'x')
    pyautogui.press('u')
    pyautogui.press('u')
    return "PC shutdown initiated"
    
def sleep() -> str:
    """Puts the computer/PC into sleep mode."""
    pyautogui.hotkey('win', 'x')
    pyautogui.press('u')
    pyautogui.press('s')
    return "PC sleep initiated"
    
def change_volume(action: str) -> str:
    """Controls the system volume. action must be one of 'up' (increase volume), 'down' (decrease volume), or 'mute' (mute/unmute)."""
    if action == "up":
        pyautogui.press('volumeup', presses=5) 
    elif action == "down":
        pyautogui.press('volumedown', presses=5)
    elif action == "mute":
        pyautogui.press('volumemute')
    return f"Volume adjusted: {action}"

def change_brightness(action: str, level: int = None) -> str:
    """Controls screen brightness. action must be 'up' (increase brightness), 'down' (decrease brightness), or 'set' (set brightness to specific level). If action is 'set', level (0-100) must be provided."""
    if action == "up":
        os.system('powershell -Command "(Get-WmiObject -Namespace root/wmi -Class WmiMonitorBrightnessMethods).WmiSetBrightness(1, [math]::min(100, (Get-WmiObject -Namespace root/wmi -Class WmiMonitorBrightness).CurrentBrightness + 20))"')
    elif action == "down":
        os.system('powershell -Command "(Get-WmiObject -Namespace root/wmi -Class WmiMonitorBrightnessMethods).WmiSetBrightness(1, [math]::max(0, (Get-WmiObject -Namespace root/wmi -Class WmiMonitorBrightness).CurrentBrightness - 20))"')
    elif action == "set" and level is not None:
        os.system(f'powershell -Command "(Get-WmiObject -Namespace root/wmi -Class WmiMonitorBrightnessMethods).WmiSetBrightness(1, {level})"')
    return f"Brightness adjusted: {action}"

def take_screenshot() -> str:
    """Takes a screenshot of the screen and saves it to the desktop."""
    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
    filename = f"screenshot_{int(time.time())}.png"
    filepath = os.path.join(desktop_path, filename)
    img = ImageGrab.grab()
    img.save(filepath)
    speak("Screenshot taken and saved to desktop")
    print(f"Screenshot saved carefully at {filepath}")
    return "Screenshot captured"

def show_available_activities() -> str:
    """Shows all activities, features, and tasks information that this program is capable of doing."""
    print(info)
    return info

tools = [
    tool(open_chrome),
    tool(open_app),
    tool(open_youtube),
    tool(open_chatgpt),
    tool("run_program")(run),  #just to give custom name for the tool insted of using same function name as tool name
    tool("send_whatsapp_message")(whatsapp),
    tool("shut_down_pc")(shut_down),
    tool("put_pc_to_sleep")(sleep),
    tool("control_volume")(change_volume),
    tool("control_brightness")(change_brightness),
    tool("capture_screenshot")(take_screenshot),
    tool(show_available_activities),
]

conversation_history = [
    SystemMessage(
        content=(
            "You are Jarvis, a helpful and concise AI assistant. "
            "Always reply clearly without using markdown symbols like ** or ###. "
            "You have access to a set of tools to control the PC. If the user's request "
            "requires a tool, call that tool. If the user is just chatting or asking a general "
            "question, respond directly."
        )
    )
]

def main(text):
    global conversation_history
    conversation_history.append(HumanMessage(content=text))

    # Keep system message and last 10 messages of the conversation
    if len(conversation_history) > 11:
        conversation_history = [conversation_history[0]] + conversation_history[-10:]

    try:
        # Bind tools to the model
        llm_with_tools = llm.bind_tools(tools)
        response = llm_with_tools.invoke(conversation_history)
        
        # Add assistant response to history
        conversation_history.append(response)

        # Print/speak the text response if there is one
        if response.content:
            reply = response.content.strip()
            print("response:", reply)
            if len(reply) <= 100:
                speak(reply)

        # If model called tools, execute them
        if response.tool_calls:
            for tool_call in response.tool_calls:
                name = tool_call["name"]
                args = tool_call["args"]
                print(f"Executing tool {name} with arguments {args}")
                
                # Find the tool in our list and run it
                tool_to_run = next((t for t in tools if t.name == name), None)
                if tool_to_run:
                    try:
                        tool_result = tool_to_run.invoke(args)
                        print(f"Tool result: {tool_result}")
                    except Exception as e:
                        print(f"Error running tool {name}: {e}")
                else:
                    print(f"Tool {name} not found.")
    except Exception as e:
        print(f"An error occurred during LLM invocation: {e}")
        