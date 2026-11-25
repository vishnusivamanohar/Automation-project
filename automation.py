from automation_library import speak,speech_to_english,main
from datetime import datetime

def get_greeting():
    hour = datetime.now().hour
    w=""
    if 5 <= hour < 12:
        w="morning"
    elif 12 <= hour < 17:
        w="afternoon"
    elif 17 <= hour < 21:
        w="evening"
    else:
        w="night"
    return f"Hi good {w}, how can I help you."

wish = get_greeting()
print(wish)
speak(wish)
while True:
    try:   
        #text = input("user:")
        text = speech_to_english()
        if text:
            main(text)
        else: 
            print("Listening again...\n")
    except KeyboardInterrupt:
        print("\nStopping automation...")
        break
    except Exception as e:
        print(f"An error occurred: {e}")