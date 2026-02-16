from prettytable import PrettyTable
from gtts import gTTS
import speech_recognition as sr
from playsound import playsound
from random import randint
import uuid
import os
import re
from deep_translator import GoogleTranslator
from colorama import init, Fore, Back, Style
init()  # Enables ANSI code support on Windows

imp_sqlqueries="""
-------------------------Basic queries-------------------------
SHOW DATABASES;
SELECT DATABASE();
CREATE DATABASE testdb;
use testdb; 
show tables;
create table students(rollno int primary key, name varchar(20), marks int);

------------------------insert queries--------------------------
insert into students values(107,'test4',75);
INSERT INTO students (rollno, name,marks)VALUES (105, 'test2',85);

------------------------select queries--------------------------
select * from students;
select max(marks) from students;
select name, marks from students where marks=(select max(marks) from students);
select * from students where name like "%a"; -- it represents ending with 
select * from students where name like 'm%' or name like 'u%'; 
select avg(marks) from students where name like 't%';

------------------------delete queries------------------------
delete from students where rollno=105;  #to delete single record
DELETE FROM students WHERE rollno = 108 OR rollno = 107;  #to delete multiple records
DELETE FROM students WHERE rollno IN (108, 107);  #to delete multiple records using IN keyword
DELETE FROM students;  #to delete all records
"""

def todict(keys,rows):
    """Convert fetched rows to dictionary format.the rows should be like [(value,value),(value,vlaue),...]"""
    """
    EXAMPLE USE CASE-------------------:
    
    from vishnu_library import todict,creat_table
    keys=["name","rollno","marks"]
    rows=[("vishnu",117,93),("uday",104,85),("sreemanth",89,83)]
    tabledata=todict(keys,rows)
    tabledata1={
        "name":["vishnu","uday","sreemanth"],
        "rollno":[117,104,89],
        "marks":[93,85,83]
    }
    a=int(input("En"))
    print(creat_table(tabledata))
    print(creat_table(tabledata1))"""
    values=[]
    #print(len(rows))
    for i in range(0,len(keys)):
        value=[]
        for j in range(0,len(rows)):
            value.append(rows[j][i])
        values.append(value)  
    td = dict(zip(keys, values))
    return td     
    
def creat_table(tabledata):
    """
it is a function which generates a ascii table for given dectionary formet text
Sample dictionary and code with its output is, 
tabledata={
   "s.no":[1,2,3,4,5],
}
   "Natural numbers":[1,2,3,4,5],
   "whloe numbers":[0,1,2,3,4],
   "intizer numbers":[-2,-1,0,1,2]
print(creat_table(tabledata))

OUTPUT:----------------------------------------------------

+------+-----------------+---------------+-----------------+
| s.no | Natural numbers | whloe numbers | intizer numbers |
+------+-----------------+---------------+-----------------+
|  1   |        1        |       0       |        -2       |
|  2   |        2        |       1       |        -1       |
|  3   |        3        |       2       |        0        |
|  4   |        4        |       3       |        1        |
|  5   |        5        |       4       |        2        |
+------+-----------------+---------------+-----------------+
"""
    table = PrettyTable()
    for column_headings in tabledata:
        table.add_column(column_headings,tabledata[column_headings])
    return table

def speak(text):
    filename = f"{uuid.uuid4()}.mp3"
    speech = gTTS(text=text, lang='en')
    speech.save(filename)
    playsound(filename)
    os.remove(filename)


def speech():
    # Initialize recognizer
    recognizer = sr.Recognizer()

    # Use microphone as source
    with sr.Microphone() as source:
        print("🎤 Speak something...")

        # Reduce background noise
        recognizer.adjust_for_ambient_noise(source, duration=1)

        # Listen to user speech
        audio = recognizer.listen(source)

        try:
            # Convert speech to text using Google API
            text = recognizer.recognize_google(audio)
            print("You said:", text)
            return text
        except sr.UnknownValueError:
            print("❌ Could not understand audio")
        except sr.RequestError:
            print("⚠️ Could not connect to speech service")

def screen_up():
    print("\n"*100)

def screen_puzz():
    """
it is used to puzz the screen when you are runing the code in cmd by just double clicking on it.
The screen will puzz untill you press enter to exit
"""
    input("press enter to exit...")

def add(num1,num2):
    return num1+num2

def substract(num1,num2):
    return num1-num2

def multiple(num1,num2):
    return num1*num2

def devide(num1,num2):
    return num1/num2

def modulo_dividion(num1,num2):
    return num1%num2

def power(num,expo):
    return pow(num,expo)

oparators={
"+":add,
"-":substract,
"*":multiple,
"/":devide,
"%":modulo_dividion,
"^":power,
            }



def calculator():
    print('''
________________________________________________________________________________________________
           _            _       _             
          | |          | |     | |            
  ___ __ _| | ___ _   _| | __ _| |_ ___  _ __ 
 / __/ _` | |/ __| | | | |/ _` | __/ _ \| '__|
| (_| (_| | | (__| |_| | | (_| | || (_) | |   
 \___\__,_|_|\___|\__,_|_|\__,_|_|_\___/|_|
 


             _____________________
            |  _________________  |
            | | JO           0. | |
            | |_________________| |
            |  ___ ___ ___   ___  |
            | | 7 | 8 | 9 | | + | |
            | |___|___|___| |___| |
            | | 4 | 5 | 6 | | - | |
            | |___|___|___| |___| |
            | | 1 | 2 | 3 | | x | |
            | |___|___|___| |___| |
            | | . | 0 | = | | / | |
            | |___|___|___| |___| |
             _____________________


This code allows you one by one digit calculations.In this calculator the following operators are allowed

+:add,
-:substract,
*:multiple,
/:devide,
%:modulo_dividion,
^:power

First enter digit and then press enter to enter operator continue like this''')
    try:
        result=int(input("digit:"))
        while(True):
            opp=input("oparetor:")
            if opp[0]=="&":
                break
            num2=int(input("digit:"))
            if opp[0] in oparators:
                result=oparators[opp[0]](result,num2)
                print(f"result={result}")
            else:
                print("your's oparetor is not in the list!Try again")
        print(f"Final result={result}")
    except ValueError as ve:
        print("only numarical digits are considered!",ve)
    except IndexError:
        print("Operators should be enter!")

def print_white_black(text):
    print(Back.WHITE + Fore.BLACK  + text +Style.RESET_ALL)
  
def print_brite(text):
    print(Style.BRIGHT + text +Style.RESET_ALL)
    
def print_blue_white(text):
    print(Back.BLUE + Fore.WHITE + Style.BRIGHT + text +Style.RESET_ALL)


"""
#decorators are called as this
#@star
#@doted_line
#@line
# @wraptext
# def welcome(text):
    # print(text)

# welcome("hello vishnu","Lable:","Note:")
"""

def star(func):
    def wrapper(text):
        print("★" * 20)
        func(text)
        print("★" * 20)
    return wrapper

def doted_line(func):
    def wrapper(text):
        print("-" * 20)
        func(text)
        print("-" * 20)
    return wrapper
    
def line(func):
    def wrapper(text):
        print("_" * 20)
        print("")
        func(text)
        print("_" * 20)
    return wrapper   
    
def wraptext(func):
    def wrapper(text,Btext,Atext):
        print(Btext)
        func(text)
        print(Atext)
    return wrapper
    
class toss:                                                                                          #go to 274 to know how to use this class
    def head_or_tails_oneperson():
        uc=input("Enter your choice(head/tails):")
        if randint(1,2) == 1:
            cc="head"
        else :
            cc="tails"
        if cc==uc :
            print("win")
            return "win"
        else:
            print("loss")
            return "loss"
    def head_or_tails_twoperson():
            uc=input("Enter person1 choice(head/tails):")
            if randint(1,2) == 1:
                cc="head"
            else :
                cc="tails"
            if cc==uc :
                print("person1 win")
            else:
                print("person2 win")
    def even_or_odd_withcomputer():
        print("Perform toss for batting/bowling")
        uc = input("Enter your toss (odd/even):")
        utoss = int(input("Enter your number:"))
        ctoss = randint(1, 10)
        value = utoss + ctoss
        if value % 2 == 0:
            result = "even"
        else:
            result = "odd"
        if result == uc:
            print(f"Computer toss is {ctoss}")
            print("You win the toss")
            return "user"
        else:
            print(f"Computer toss is {ctoss}")
            print("You lose the toss")
            return "computer"
            
    
class speech_recognition_tool:
    """this is used to recognize both telugu and english speech and convert it into text.
    If it is telugu it also translate it into english text and then returns it """
    @staticmethod
    def detect_language(text):
        """Detects if the text is Telugu or English"""
        telugu_chars = re.findall(r'[\u0C00-\u0C7F]', text)
        return 'te' if len(telugu_chars) > 0 else 'en'

    @staticmethod
    def mixed_speech_to_english():
        recognizer = sr.Recognizer()

        with sr.Microphone() as source:
            print("🎙️ Speak in Telugu or English...")
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source)

        text = ""
        # Step 1: Try recognizing as Telugu first
        try:
            text = recognizer.recognize_google(audio, language='te-IN')
            lang = 'te'
        except sr.UnknownValueError:
            # Step 2: If Telugu fails, try English
            try:
                text = recognizer.recognize_google(audio, language='en-IN')
                lang = 'en'
            except sr.UnknownValueError:
                print("⚠️ Sorry, could not understand your speech.")
                return
            except sr.RequestError:
                print("🚫 Could not request results — check internet connection.")
                return
        except sr.RequestError:
            print("🚫 Could not request results — check internet connection.")
            return

        # Double-check language using character inspection
        if lang == 'en':
            detected = speech_recognition_tool.detect_language(text)
            if detected == 'te':
                lang = 'te'

        # Translate Telugu to English
        if lang == 'te':
            print(f"🗣 Telugu Text: {text}")
            translated = GoogleTranslator(source='te', target='en').translate(text)
            print(f"🌍 English Translation: {translated}")
        else:
            print(f"🗣 English Text: {text}")
            translated = text

        return translated

        

# NOTE:if a function is inside a class it should be called like this,
# from vishnu_library import toss
# Now call any method for example,
# toss.head_or_tails_oneperson()
# -------------or--------------------
# import vishnu_library
# vishnu_library.toss.head_or_tails_oneperson()