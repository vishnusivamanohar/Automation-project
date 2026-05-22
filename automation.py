from automation_library import *
while True:
    try:   
        text = input("user:")
        # text = mixed_speech_to_english()
        if text:
            main(text)
        else:
            print("Listening again...\n")
    except KeyboardInterrupt:
        print("\nStopping automation...")
        break
    except Exception as e:
        print(f"An error occurred: {e}")