from automation_library import *


while True :
    
    try:   
        choice=int(input("\n Choose to type or speek(0/9):"))
        if choice == 9:
            text= mixed_speech_to_english()
        elif choice == 0:
            text=input("Enter it:")
        else:
            break
        if text==None:
            text=input("Enter it:")
        main(text)
    except ValueError:
        print("Enter valed choice") 