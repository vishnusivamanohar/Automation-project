"""
Automation Library - Jarvis AI Assistant
Works effectively on this PC. Automates tasks via voice/text commands.
"""

# ─────────────────────────── Standard Imports ───────────────────────────────
import sys
import os
import re
import json
import time

# ─────────────────────────── Third-party Imports ────────────────────────────
import pyttsx3
import speech_recognition as sr
import pyautogui
from PIL import ImageGrab, Image
from groq import Groq
from deep_translator import GoogleTranslator
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.tools import tool
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage, ToolMessage
from langgraph.prebuilt import create_react_agent          # FIX: correct import (langchain.agents.create_agent is removed)
from langgraph.checkpoint.memory import InMemorySaver
from google import genai
from google.genai import errors as genai_errors
from datetime import datetime as _datetime                  

# ─────────────────────────── Stdout Encoding ────────────────────────────────
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

# ─────────────────────────── Environment / API Keys ─────────────────────────
load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")   # Change key if tokens are exhausted
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

llm = ChatGroq(model="openai/gpt-oss-120b", api_key=GROQ_API_KEY)  

client = genai.Client(api_key=GEMINI_API_KEY)

# ════════════════════════════════════════════════════════════════════════════
#  UTILITY FUNCTIONS
# ════════════════════════════════════════════════════════════════════════════

def clean_markdown(text: str) -> str:
    """Remove common markdown symbols to produce clean text for speech/display."""
    text = re.sub(r'[*_`>~\-]+', '', text)
    text = re.sub(r'\s*#{1,6}\s*', '\n', text)
    text = re.sub(r'(\n)?\s*[\-\*\•]\s*', r'\n• ', text)
    text = re.sub(r'(\d+[\.)])\s*', r'\n\1 ', text)
    text = re.sub(r'\n\s*\n+', '\n\n', text)
    return text.strip()


def speak(text: str) -> None:
    """Speak the given text string using pyttsx3 TTS.
    """
    clean_text = clean_markdown(text)
    engine = None
    try:
        engine = pyttsx3.init()
        engine.setProperty('rate', 180)
        voices = engine.getProperty('voices')
        if voices:
            engine.setProperty('voice', voices[0].id)
        engine.say(clean_text)
        engine.runAndWait()
    except Exception as e:
        print(f"[speak] TTS error: {e}")
    finally:
        if engine:
            try:
                engine.stop()
            except Exception:
                pass


# ════════════════════════════════════════════════════════════════════════════
#  SPEECH RECOGNITION
# ════════════════════════════════════════════════════════════════════════════

def speech_to_english() -> str | None:
    """Listen for English speech and return the recognised text, or None."""
    recognizer = sr.Recognizer()
    recognizer.energy_threshold = 300
    recognizer.dynamic_energy_threshold = True
    recognizer.pause_threshold = 0.8
    recognizer.non_speaking_duration = 0.5

    with sr.Microphone() as source:
        print("🎙️ Speak in English...")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        print("🎤 Listening...")
        try:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
        except sr.WaitTimeoutError:
            print("⏱️ No speech detected.")
            return None

    try:
        print("🧠 Recognizing...")
        text = recognizer.recognize_google(audio, language="en-IN")
        print(f"🗣️ You said: {text}")
        return text
    except sr.UnknownValueError:
        print("⚠️ Sorry, I couldn't understand the speech.")
        return None
    except sr.RequestError as e:
        print(f"🚫 Speech recognition service error: {e}")
        return None


# ════════════════════════════════════════════════════════════════════════════
#  INFORMATION STRING
# ════════════════════════════════════════════════════════════════════════════

info = """
╔══════════════════════════════════════════════════════════╗
║           🤖  JARVIS — What I Can Do For You            ║
╚══════════════════════════════════════════════════════════╝

1. 🗣️  VOICE & SPEECH
   • Listen to your spoken English commands via microphone
   • Speak responses aloud using text-to-speech

2. 🌐  OPEN WEBSITES & APPS
   • Open Chrome, Notepad, Calculator, VS Code, Paint, Spotify, VLC,
     Word, Excel, PowerPoint, Task Manager, Settings, Camera, and more
   • Open any website (e.g. "open monkey type website")

3. 🚀  LAUNCH YOUR PROJECTS
   • Hand Detection (3 variants), Face Detection (3 variants)
   • Mouse Control via Hand Gestures
   • Telegram Bot, Royal Spice RAG Chatbot, AI Quiz App
   • Online Attendance Flask App, Task Manager App
   • RPS Game (HTML), My Resume

4. 💬  WHATSAPP MESSAGING
   • Send messages to any contact on WhatsApp Web
   • Send the same message multiple times (bulk messaging)

5. ⌨️  KEYBOARD & MOUSE CONTROL
   • Type text into any active window
   • Press any key (Enter, Escape, Arrow keys, F1-F12, etc.)
   • Execute hotkeys (Ctrl+C, Alt+Tab, Win+D, etc.)
   • Left click, right click, or double click anywhere on screen

6. 🔆  BRIGHTNESS CONTROL
   • Increase / decrease brightness by 20%
   • Set brightness to an exact level (0–100)

7. 👁️  SCREEN VISION (Gemini AI)
   • Find any UI element on screen by description and get its coordinates
   • Describe / explain what is currently on the screen
   • Extract all visible text from the screen
   • Answer visual questions about the screen

8. 🕒  DATE & TIME
   • Tell you the current date and time

9. 💬  GENERAL AI CHAT
   • Answer any general question directly (no tool needed)
   • Remembers the last 5 messages for conversation context

10. ℹ️  HELP
    • Ask "what can you do?" to see this list anytime

Note: Works most effectively on this specific Windows PC.
"""


# ════════════════════════════════════════════════════════════════════════════
#  TOOL FUNCTIONS
# ════════════════════════════════════════════════════════════════════════════

def run_program(program_name: str) -> str:
    """Run a specific program, project, or Python file by name.
    Also opens system apps like Chrome, Notepad, Calculator, File Explorer, VS Code, etc.
    """

    # ── System / common apps (opened directly via os.startfile or start command) ──
    system_apps = {
        "chrome":           "chrome",
        "google chrome":    "chrome",
        "notepad":          "notepad",
        "calculator":       "calc",
        "file explorer":    "explorer",
        "explorer":         "explorer",
        "vs code":          "code",
        "vscode":           "code",
        "visual studio code": "code",
        "task manager":     "taskmgr",
        "paint":            "mspaint",
        "word":             "winword",
        "excel":            "excel",
        "powerpoint":       "powerpnt",
        "vlc":              "vlc",
        "spotify":          "spotify",
        "control panel":    "control",
        "settings":         "ms-settings:",
        "camera":           "microsoft.windows.camera:",
    }

    # Check if user is asking for a system app first (simple keyword match)
    lower_input = program_name.strip().lower()
    for key, cmd in system_apps.items():
        if key in lower_input:
            print(f"Opening system app: {cmd}")
            if cmd.endswith(":"):
                # Protocol URI (e.g. ms-settings:)
                os.system(f'start {cmd}')
            else:
                os.system(f'start {cmd}')
            return f"Opened {key}"

    # ── Project paths ──────────────────────────────────────────────────────────
    paths = {
        "hand_detection.py":                   r'python "C:\Users\HP\Desktop\T.vishnu.s.m\projects\ML projects\hand ditection\hand_detection.py"',
        "hand_detection2.py":                  r'python "C:\Users\HP\Desktop\T.vishnu.s.m\projects\ML projects\hand ditection\hand_detection2.py"',
        "hand_detection3.py":                  r'python "C:\Users\HP\Desktop\T.vishnu.s.m\projects\ML projects\hand ditection\hand_detection3.py"',
        "face_detection1.py":                  r'python "C:\Users\HP\Desktop\T.vishnu.s.m\projects\ML projects\face_recogization\p1.py"',
        "face_detection2.py":                  r'python "C:\Users\HP\Desktop\T.vishnu.s.m\projects\ML projects\face_recogization\p2.py"',
        "face_detection3.py":                  r'python "C:\Users\HP\Desktop\T.vishnu.s.m\projects\ML projects\face_recogization\p3.py"',
        "telegrambot1.py":                     r'python "C:\Users\HP\Desktop\T.vishnu.s.m\projects\ML projects\telegrambot1.py"',
        "mouse control using hand detection":  r'python "C:\Users\HP\Desktop\T.vishnu.s.m\projects\ML projects\hand ditection\main.py"',
        "rolyal spice restaurent chatbot rag project app.py": r'python "C:\Users\HP\Desktop\T.vishnu.s.m\projects\ML projects\llm engineering course projects\royal spice restorent chatbot project\app.py"',
        "AI Quize app.py":                     r'python "C:\Users\HP\Desktop\T.vishnu.s.m\projects\projects using flask\AI Quize\app.py"',
        "online_attendance_flask app.py":      r'python "C:\Users\HP\Desktop\T.vishnu.s.m\projects\projects using flask\online_attendance_flask\app.py"',
        "rps_game.html":                       r'start "" "C:\Users\HP\Desktop\T.vishnu.s.m\projects\projects using flask\rps_game_files\rps_game.html"',
        "task_manager app.py":                 r'python "C:\Users\HP\Desktop\T.vishnu.s.m\projects\projects using flask\task manager\app.py"',
        "task_manager_singlefile.html":        r'start "" "C:\Users\HP\Desktop\T.vishnu.s.m\projects\projects using flask\task manager\task_manager_singlefile.html"',
        "task manager1 app.py":                r'python "C:\Users\HP\Desktop\T.vishnu.s.m\projects\projects using flask\task_manager_project\app.py"',
        "my resume":                           r'start "" "C:\Users\HP\Desktop\T.vishnu.s.m\My_Resume.docx"',
    }

    prompt = f"""
You are a helpful assistant. Find the best matching key for the user input from
the list of keys provided below. Return ONLY the matching key string — nothing else.
If an exact match is not found, return the most similar key.
If the user input does not match any key even loosely, return exactly: NO_MATCH

Keys: {list(paths.keys())}

User input: "{program_name}"

Examples:
  Input "online attendance"  → Key "online_attendance_flask app.py"
  Input "activate mouse controls" → Key "mouse control using hand detection"
  Input "open chrome" → NO_MATCH  (chrome is a system app, not in this list)
"""

    chat_response = llm.invoke(prompt)
    response = chat_response.content.strip().strip('"').strip("'")
    print("Matched Key:", response)

    # If LLM says no match, don't guess a wrong project
    if response.upper() == "NO_MATCH":
        return f"Could not find a project named '{program_name}'. If it's a system app, try saying 'open chrome' or 'open notepad'."

    # Case-insensitive match
    matched_key = next(
        (k for k in paths if k.lower() == response.lower()),
        None
    )

    if not matched_key:
        print(f"Could not match LLM response '{response}' to any path.")
        return f"Could not match program name: {program_name}"

    adders = paths[matched_key]
    ml_root = r"C:\Users\HP\Desktop\T.vishnu.s.m\projects\ML projects"

    if adders.startswith("python"):
        # Extract file path from command string
        file_path = adders[len('python "'):-1]   # strip leading `python "` and trailing `"`
        folder_path = os.path.dirname(file_path)

        # Open a new CMD window and run the script
        # FIX: use pyautogui.write() (supports unicode) instead of typewrite() where possible
        pyautogui.hotkey('win', 'r')
        time.sleep(0.5)
        pyautogui.write('cmd', interval=0.05)
        pyautogui.press('enter')
        time.sleep(1)

        if "ML projects" in file_path:
            pyautogui.write(f'cd /d "{ml_root}"', interval=0.02)
            pyautogui.press('enter')
            time.sleep(0.5)
            pyautogui.write(r'venv\Scripts\activate', interval=0.02)
            pyautogui.press('enter')
            time.sleep(1)

        pyautogui.write(f'cd /d "{folder_path}"', interval=0.02)
        pyautogui.press('enter')
        time.sleep(0.5)
        pyautogui.write(f'python "{os.path.basename(file_path)}"', interval=0.02)
        pyautogui.press('enter')

    else:
        # HTML / DOCX: open directly
        pyautogui.hotkey('win', 'r')
        time.sleep(0.5)
        pyautogui.write('cmd', interval=0.05)
        pyautogui.press('enter')
        time.sleep(1)
        pyautogui.write(adders, interval=0.02)
        pyautogui.press('enter')

    return f"Started program: {program_name}"


def whatsapp(name: str, message: str, count: int = 1) -> str:
    """Send a WhatsApp message to a contact by name. Optionally send `count` times."""
    # FIX: URL was malformed ("https://web.whatsapp.com/.com") — corrected
    pyautogui.hotkey('win', 'r')
    time.sleep(0.5)
    pyautogui.write('chrome https://web.whatsapp.com', interval=0.02)
    pyautogui.press('enter')
    time.sleep(9)
    pyautogui.moveTo(280, 180, duration=1)
    pyautogui.click()
    pyautogui.write(name, interval=0.05)
    time.sleep(1)
    pyautogui.press('enter')
    time.sleep(1)
    for _ in range(count):
        # FIX: typewrite() doesn't support unicode/spaces reliably;
        #      use pyperclip + hotkey for reliable message pasting
        import pyperclip
        pyperclip.copy(message)
        pyautogui.hotkey('ctrl', 'v')
        pyautogui.press('enter')
        time.sleep(0.3)
    return f"WhatsApp message sent to {name}"


def change_brightness(action: str, level: int = None) -> str:
    """Control screen brightness.

    Args:
        action: 'up' (increase by 20), 'down' (decrease by 20), or 'set' (exact level).
        level:  0–100, required only when action is 'set'.
    """
    if action == "up":
        os.system(
            'powershell -Command "(Get-WmiObject -Namespace root/wmi -Class WmiMonitorBrightnessMethods)'
            '.WmiSetBrightness(1, [math]::min(100, '
            '(Get-WmiObject -Namespace root/wmi -Class WmiMonitorBrightness).CurrentBrightness + 20))"'
        )
    elif action == "down":
        os.system(
            'powershell -Command "(Get-WmiObject -Namespace root/wmi -Class WmiMonitorBrightnessMethods)'
            '.WmiSetBrightness(1, [math]::max(0, '
            '(Get-WmiObject -Namespace root/wmi -Class WmiMonitorBrightness).CurrentBrightness - 20))"'
        )
    elif action == "set" and level is not None:
        # FIX: clamp level to 0–100 to avoid invalid WMI calls
        level = max(0, min(100, int(level)))
        os.system(
            f'powershell -Command "(Get-WmiObject -Namespace root/wmi -Class WmiMonitorBrightnessMethods)'
            f'.WmiSetBrightness(1, {level})"'
        )
    else:
        return f"Invalid brightness action '{action}'. Use 'up', 'down', or 'set'."
    return f"Brightness adjusted: {action}"



def show_available_activities() -> str:
    """Show all activities, features, and tasks this program can perform."""
    print(info)
    return info


def type_text(text: str) -> str:
    """Type the given text into the currently active window."""
    # FIX: use pyautogui.write() which handles more characters than typewrite()
    pyautogui.write(text, interval=0.02)
    return "Text written successfully"


def press_buttons(
    buttons: str,
    presses: int = 1,
) -> str:
    """Execute keyboard actions: hotkeys or single/repeated key presses to perform any task.

    Args:
    pyautogui.write(text, interval=0.02)
        buttons: Key name (e.g. 'enter', 'volumeup') or hotkey combo (e.g. 'ctrl+c').
        action:  'hotkey', 'press', or 'auto' (default — auto-detected).
        presses: Number of times to repeat (default 1).
    """
    interval = 0.05   # FIX: was 0.0 — tiny interval prevents missed keystrokes
    action: str = "auto"
    mode = action.strip().lower()
    raw_input = buttons.strip()
    lower_input = raw_input.lower()

    if mode == "auto":
        mode = "hotkey" if ("+" in raw_input and len(raw_input) > 1) else "press"

    if mode == "hotkey":
        keys = [k.strip().lower() for k in raw_input.split("+") if k.strip()]
        for _ in range(presses):
            pyautogui.hotkey(*keys, interval=interval)
        return f"Executed hotkey '{'+'.join(keys)}' ({presses}x)"

    elif mode == "press":
        pyautogui.press(lower_input, presses=presses, interval=interval)
        return f"Pressed key '{lower_input}' ({presses}x)"

    else:
        return f"Invalid action '{action}'. Use 'hotkey' or 'press'."


def get_datetime() -> str:
    """Return the current date and time as a formatted string."""
    # FIX: function was named 'datetime', shadowing the datetime module import
    return _datetime.now().strftime("%A, %B %d, %Y %H:%M:%S")


def find_elements_onScreen(object_to_find: str) -> str:
    """used to see the screen .it takes a screenshot and find a UI element (button, search bar, etc.) on screen.
    Returns coordinates (x,y) of that element/object."""

    screenshot = pyautogui.screenshot()
    screenshot.save("screen.png")

    image = Image.open("screen.png")
    image_width, image_height = image.size

    prompt = f"""
Look at this screenshot.
Find the: {object_to_find}

Return ONLY valid JSON in this exact format:

{{
    "box_2d": [ymin, xmin, ymax, xmax]
}}

IMPORTANT:
- Coordinates MUST be normalised from 0 to 1000.
- Format is [ymin, xmin, ymax, xmax].
- Do not return actual pixel coordinates.
- Do not use markdown.
- Do not explain anything.
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=[image, prompt]
    )

    print("Gemini:", response.text)

    raw = response.text.strip()
    raw = re.sub(r"```json|```", "", raw).strip()

    data = json.loads(raw)
    ymin, xmin, ymax, xmax = data["box_2d"]

    # Convert normalised (0–1000) → actual pixels
    x1 = int(xmin / 1000 * image_width)
    y1 = int(ymin / 1000 * image_height)
    x2 = int(xmax / 1000 * image_width)
    y2 = int(ymax / 1000 * image_height)

    # Centre of bounding box
    cx = (x1 + x2) // 2
    cy = (y1 + y2) // 2

    print(f"Bounding box: ({x1}, {y1}) → ({x2}, {y2})")
    print(f"Clicking centre: ({cx}, {cy})")
    #click(cx,cy,"left")

    # FIX: was `click(s, y)` — 's' is undefined (NameError). Fixed to click(cx, cy)
    return f"{(cx,cy)}"


def explain_screen(query: str) -> str:
    """Analyse the current screen and answer any visual query about it.eg: what is on the screen.
    Args:
        query: A natural-language question or instruction about the screen eg:extract the text from the screen.
    Returns:
        A plain-text explanation / answer produced by Gemini Vision.
    """
    # ── 1. Capture the screen ────────────────────────────────────────────────
    screenshot = pyautogui.screenshot()
    screenshot.save("screen.png")
    image = Image.open("screen.png")

    # ── 2. Build a smart, context-aware prompt ───────────────────────────────
    prompt = f"""You are a highly capable screen-reading assistant.
You have been given a screenshot of a computer screen.
Your job is to carefully analyse the screenshot and answer the user's query as accurately and helpfully as possible.

USER QUERY: {query}

GUIDELINES:
- If the query asks "what is on the screen" or "describe the screen": give a clear, structured overview — mention the active application, main content area, visible UI elements (buttons, menus, toolbars, sidebars), any open windows, and the general layout.
- If the query asks about specific objects or elements (e.g. "is there a search bar?"): state clearly whether the object is present, where it is located on the screen, and any relevant details about it.
- If the query asks to extract or read text: transcribe ALL visible text faithfully, preserving logical groupings (headings, paragraphs, labels, button text, etc.).
- If the query asks about colours, layout, or design: describe those visual properties precisely.
- If the query asks to extract text, (e.g. text in the email): extract that particular text and send it only.
- Always be concise but complete. Do not omit important details.
- Do NOT use markdown symbols like ** or ###. Write in clean, plain text.
- Do NOT say "I see an image of a screen" — just answer the query directly.
"""

    # ── 3. Call Gemini Vision ────────────────────────────────────────────────
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=[image, prompt]
    )

    result = response.text.strip()
    print("Screen Explanation:", result)
    return result


def click(x: int, y: int, button: str = "left") -> str:
    """Click at the given (x, y) screen coordinates.

    Args:
        x, y:   Screen coordinates.
        button: 'left' (default), 'right', or 'double'.
    """
    action = button.strip().lower()

    if action == "double":
        pyautogui.doubleClick(x, y,duration=0.2)
    elif action in ("left", "right"):
        pyautogui.click(x, y, button=action,duration=0.2)
    else:
        return f"Invalid button '{button}'. Use 'left', 'right', or 'double'."

    return f"Performed {action} click at ({x}, {y})"


# ════════════════════════════════════════════════════════════════════════════
#  TOOL REGISTRY & AGENT
# ════════════════════════════════════════════════════════════════════════════

tools = [
    tool(type_text),
    tool(press_buttons),
    tool("get_datetime")(get_datetime),   # FIX: renamed from 'datetime' to avoid module name clash
    tool(find_elements_onScreen),
    tool(explain_screen),
    tool(run_program),
    tool("send_whatsapp_message")(whatsapp),
    tool("control_brightness")(change_brightness),
    tool(show_available_activities),
    tool(click),
    tool(speak),
]

# FIX: langchain's create_agent() was removed; use langgraph's create_react_agent()
#      which is the correct modern API for tool-calling agents.
agent = create_react_agent(
    model=llm,
    tools=tools,
    prompt=(
        "You are Jarvis, a helpful and concise AI assistant. "
        "Always reply clearly without using markdown symbols like ** or ###. "
        "You have access to tools including keyboard/mouse controls to operate this Windows 10 PC. "
        "If the user's request requires a tool, call it. If the user is chatting or asking a general "
        "question, respond directly without calling tools. "
        "If no specific tool exists but the task can be done via keyboard operations (e.g., Win+R and type chrome/app name to open a specific app), do so."
    ),
)

# ════════════════════════════════════════════════════════════════════════════
#  CONVERSATION LOOP
# ════════════════════════════════════════════════════════════════════════════

conversation_history: list[dict] = []   # Keeps last 5 exchanges


def main(text: str) -> None:
    """Process a user message through the Jarvis agent and speak the response."""
    global conversation_history
    from langchain_core.messages import AIMessage, ToolMessage

    if not text or not text.strip():
        return

    try:
        conversation_history.append({"role": "user", "content": text})

        # Keep only last 5 messages (rolling window)
        if len(conversation_history) > 5:
            conversation_history = conversation_history[-5:]

        response = agent.invoke({"messages": conversation_history})
        messages  = response["messages"]

        # ── Print every tool call + result ────────────────────────────────────
        print("\n" + "─" * 50)
        tool_count = 0
        for msg in messages:
            if isinstance(msg, AIMessage) and msg.tool_calls:
                for tc in msg.tool_calls:
                    tool_count += 1
                    print(f"🔧 Tool Called : {tc['name']}")
                    print(f"   Arguments  : {tc['args']}")
            elif isinstance(msg, ToolMessage):
                print(f"   ↳ Result    : {msg.content}")
        if tool_count == 0:
            print("ℹ️  No tools called (direct answer)")
        else:
            print(f"✅ {tool_count} tool(s) called")
        print("─" * 50)
        # ─────────────────────────────────────────────────────────────────────

        reply = messages[-1].content

        if reply:
            reply = reply.strip()
            conversation_history.append({"role": "assistant", "content": reply})
            print("Response:", reply)
            # Only speak if reply is concise enough
            if len(reply) <= 300:
                speak(reply)

    except Exception as e:
        print(f"An error occurred: {e}")
