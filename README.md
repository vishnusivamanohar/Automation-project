# 🤖 Jarvis — Voice & Vision AI Desktop Automation Assistant

> A modular, intelligent desktop assistant for Windows that executes tasks through natural language voice or text commands. Powered by **LangGraph ReAct agents**, **Groq LLM (`openai/gpt-oss-120b`)**, **Google Gemini 2.5 Flash Vision**, and **PyAutoGUI**.

---

## 📑 Table of Contents

- [Overview](#-overview)
- [Architecture & Workflow](#-architecture--workflow)
- [Key Features](#-key-features)
- [Requirements & Prerequisites](#-requirements--prerequisites)
- [Installation & Setup](#-installation--setup)
- [Configuration (.env)](#-configuration-env)
- [Usage](#-usage)
- [Registered Agent Tools](#-registered-agent-tools)
- [Project Structure](#-project-structure)
- [Important Notes & Troubleshooting](#-important-notes--troubleshooting)
- [Author](#-author)

---

## 🌟 Overview

Jarvis acts as an autonomous co-pilot on Windows. You can interact with it via voice or text. When an instruction requires operating the system, launching apps, interacting with WhatsApp, adjusting screen brightness, or analyzing visible UI elements on screen, Jarvis uses tool-calling via a ReAct agent loop. For normal questions, it responds conversationally with audio speech feedback.

---

## 🏗️ Architecture & Workflow

```text
[ User Voice / Text Input ]
            │
            ▼
┌───────────────────────────┐
│ SpeechRecognition / Input │ (Google Speech-to-Text engine, en-IN)
└───────────┬───────────────┘
            │
            ▼
┌───────────────────────────┐
│   LangGraph ReAct Agent   │ (Powered by ChatGroq: openai/gpt-oss-120b)
└───────────┬───────────────┘
            │
     ┌──────┴──────────────────────────────────┐
     ▼                                         ▼
[ General Conversational Reply ]    [ Actionable Tool Triggered ]
     │                                         │
     │                                         ├──► System Apps & Projects Launcher
     │                                         ├──► WhatsApp Web Automated Messaging
     │                                         ├──► Gemini 2.5 Flash Screen Vision
     │                                         ├──► Keyboard & Mouse Emulation
     │                                         └──► WMI Brightness Control
     │                                         │
     └───────────────────┬─────────────────────┘
                         │
                         ▼
┌──────────────────────────────────────────────┐
│        pyttsx3 Text-To-Speech (TTS)          │ (Voice response spoken aloud)
└──────────────────────────────────────────────┘
```

---

## 🚀 Key Features

### 1. 🎙️ Natural Voice Interaction
- Listens to English speech through your microphone with automatic ambient noise compensation (`sr.adjust_for_ambient_noise`).
- Speaks responses aloud with `pyttsx3` text-to-speech engine.
- Filters out markdown formatting so speech output sounds natural.

### 2. 🖥️ Smart App & Project Launcher (`run_program`)
- **System Apps:** Opens Google Chrome, Notepad, Calculator, VS Code, Task Manager, Paint, Word, Excel, PowerPoint, Spotify, VLC, Settings, Camera, etc.
- **Custom Projects:** Launches local ML and Web projects (e.g., Hand Gesture Recognition, Face Recognition, Telegram Bot, Flask Apps) and automatically activates the local virtual environment (`venv\Scripts\activate`) before running.

### 3. 💬 Automated WhatsApp Messaging (`whatsapp`)
- Opens WhatsApp Web via Chrome.
- Searches for the specified contact name, clicks on the chat, pastes the message, and sends it.
- Supports batch/multiple message repeats (e.g. sending reminders $N$ times).

### 4. 👁️ Screen Understanding & Vision AI (Gemini 2.5 Flash)
- **UI Element Detection (`find_elements_onScreen`):** Takes a screen capture, passes it to Gemini Vision with bounding box prompting (`[ymin, xmin, ymax, xmax]`), normalizes coordinates from 0–1000 scale to exact screen pixels, and pinpoints UI items to click.
- **Visual Q&A (`explain_screen`):** Answers questions about the current screen layout, explains visible windows, or extracts and transcribes visible text.

### 5. ⌨️ Keyboard & Mouse Automation (`pyautogui`)
- **Key Presses & Combinations (`press_buttons`):** Handles single keys (Enter, Esc, Tab, Volume keys) and multi-key combos (`ctrl+c`, `win+r`, `alt+tab`).
- **Typing (`type_text`):** Types text strings into the currently focused window with realistic keystroke intervals.
- **Mouse Clicks (`click`):** Performs single left click, right click, or double click at target screen coordinates.

### 6. 🔆 Display Brightness Control (`change_brightness`)
- Controls laptop screen brightness using Windows WMI PowerShell commands:
  - Relative increase: `action="up"` (+20%)
  - Relative decrease: `action="down"` (-20%)
  - Direct setting: `action="set", level=60` (clamped between 0 and 100)

### 7. 🧠 Contextual Memory
- Retains a rolling history of the last 5 conversation exchanges to answer follow-up queries coherently.

---

## 📋 Requirements & Prerequisites

### 💻 System Requirements
- **Operating System:** Windows 10 or Windows 11 (required for PowerShell WMI brightness controls and Windows hotkeys).
- **Python Version:** Python 3.10, 3.11, or 3.12.
- **Hardware:** Working microphone and speakers/headphones.
- **Browser:** Google Chrome (logged in to WhatsApp Web if using WhatsApp automation).

### 🔑 Required API Keys
1. **Groq Cloud API Key:** Used for high-speed agent tool-calling with `openai/gpt-oss-120b`. Obtain free/paid keys at [console.groq.com](https://console.groq.com/).
2. **Google Gemini API Key:** Used for multimodal screen analysis and UI element localization (`gemini-2.5-flash`). Obtain at [aistudio.google.com](https://aistudio.google.com/).

### 📦 Python Dependencies
All required libraries are listed in [`requirements.txt`](file:///c:/Users/HP/Desktop/T.vishnu.s.m/projects/ML%20projects/requirements.txt):
- `pyttsx3`
- `SpeechRecognition`
- `pyaudio` (Microphone stream input)
- `pyautogui` & `pyperclip` (System input automation & clipboard management)
- `pillow` (Screen capture handling)
- `groq` & `langchain-groq` (Groq API bindings)
- `langchain-core` & `langgraph` (ReAct agent runtime and tool bindings)
- `google-genai` (Official Google GenAI SDK for Gemini Vision)
- `python-dotenv` (Environment variable management)
- `deep-translator` (Text translation support)

---

## 🛠️ Installation & Setup

### Step 1: Clone or Navigate to the Repository
```powershell
cd "c:\Users\HP\Desktop\T.vishnu.s.m\projects\ML projects"
```

### Step 2: Create and Activate a Virtual Environment
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```
*(If execution of scripts is restricted in PowerShell, run `Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned`)*

### Step 3: Install Required Packages
```powershell
pip install -r requirements.txt
```

> [!NOTE]
> **Windows PyAudio Installation:** If `pip install pyaudio` fails due to missing C++ build tools, install it via pipwin or pre-compiled wheel:
> ```powershell
> pip install pipwin
> pipwin install pyaudio
> ```

---

## ⚙️ Configuration (.env)

Create a `.env` file in the project root directory (you can use [`.env.example`](file:///c:/Users/HP/Desktop/T.vishnu.s.m/projects/ML%20projects/.env.example) as a template):

```env
GROQ_API_KEY=gsk_your_groq_api_key_here
GEMINI_API_KEY=AIzaSy_your_gemini_api_key_here
```

---

## 🎯 Usage

### 1. Launching Jarvis (Voice Mode)
Run the main script:
```powershell
python automation.py
```
- Jarvis greets you according to the time of day (Morning, Afternoon, Evening, Night).
- It opens the microphone and prompts `"🎙️ Speak in English..."`.
- Speak your command. Jarvis processes it, executes the action, and speaks back.

### 2. Switching to Text Mode
If you do not wish to use voice or are in a noisy environment:
1. Open [`automation.py`](file:///c:/Users/HP/Desktop/T.vishnu.s.m/projects/ML%20projects/automation.py#L22).
2. Uncomment line 22 (`text = input("user:")`) and comment line 23 (`text = speech_to_english()`).
3. Run `python automation.py` and type your instructions directly.

### 3. Example Commands to Try

| Goal | Example Spoken / Typed Command |
|---|---|
| **App Launching** | *"Open Google Chrome"* / *"Open Task Manager"* / *"Open VS Code"* |
| **Project Launching** | *"Run hand detection project"* / *"Launch attendance app"* |
| **WhatsApp Message** | *"Send 'I will be there in 10 minutes' to John on WhatsApp"* |
| **Screen Analysis** | *"What is currently open on my screen?"* / *"Read the text in the active email"* |
| **UI Interaction** | *"Find the search bar on screen"* / *"Click the blue Submit button"* |
| **Hardware Control** | *"Increase brightness"* / *"Set brightness to 80"* |
| **Keyboard Actions** | *"Press Ctrl+T to open a new tab"* / *"Type Hello World and hit enter"* |
| **Time & Info** | *"What time is it?"* / *"Show available activities"* |

---

## 🧰 Registered Agent Tools

| Tool Function | Description |
|---|---|
| `run_program(program_name)` | Matches request against system shortcuts and registered project scripts. |
| `send_whatsapp_message(name, message, count)` | Automates Chrome WhatsApp Web UI navigation and message dispatching. |
| `explain_screen(query)` | Captures screenshot and asks Gemini 2.5 Flash for visual comprehension or OCR. |
| `find_elements_onScreen(object_to_find)` | Returns screen coordinates `(x, y)` of any UI widget identified by Gemini Vision. |
| `click(x, y, button)` | Executes `left`, `right`, or `double` mouse click at specified coordinates. |
| `press_buttons(buttons, presses)` | Executes hotkeys (e.g. `ctrl+c`) or single key presses with configurable repeats. |
| `type_text(text)` | Types text into the active cursor position via PyAutoGUI. |
| `control_brightness(action, level)` | Adjusts display brightness using PowerShell WMI monitor methods. |
| `get_datetime()` | Returns current formatted date and time string. |
| `show_available_activities()` | Displays the internal `info` reference string listing available tasks. |
| `speak(text)` | Triggers offline text-to-speech output. |

---

## 📂 Project Structure

```text
ML projects/
├── .env                         # API keys (Groq, Gemini) - [Do not commit]
├── .env.example                 # Example environment template
├── .gitignore                   # Git ignore file for secrets, venv, pycache
├── requirements.txt             # Project Python dependencies
├── README.md                    # Project documentation
├── automation.py                # Main application entry point (Greeting & Loop)
├── automation_library.py        # Core tool implementations, ReAct agent & TTS/STT
├── screen.png                   # Scratch frame saved during screen vision calls
├── venv/                        # Python virtual environment
├── hand ditection/              # MediaPipe Hand detection sub-projects
├── face_recogization/           # OpenCV Face recognition sub-projects
└── llm engineering course/      # RAG & LLM chatbot projects
```

---

## ⚠️ Important Notes & Troubleshooting

- **WhatsApp Web Session:** You must already be logged into WhatsApp Web in Chrome on your PC.
- **Brightness Control:** WMI brightness methods (`WmiMonitorBrightnessMethods`) operate on integrated laptop screens. They may not adjust external HDMI/DisplayPort desktop monitors (which use DDC/CI hardware controls).
- **Screen Coordinate Resolution:** Gemini Vision detects normalized coordinates (0–1000). Ensure Windows display scaling (DPI) matches normal PyAutoGUI resolution if clicking targets slightly miss.
- **Failsafe:** PyAutoGUI has a built-in emergency stop: slamming your mouse cursor into any screen corner aborts ongoing automation actions.

---

## 👨‍💻 Author

**T. Vishnu S. M.**  
*Machine Learning & Automation Projects*
