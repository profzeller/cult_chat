#!python3

from pytchat import LiveChat
from pathlib import Path
from playsound import playsound
import re
import sys


def create_list():
    # Ask for who they want to follow
    print("Please enter a list of people you want to follow separated by commas, no spaces:")
    print("For example: MrHits,Nightbot")
    print("This is case sensitive!")

    my_input = input("> ")

    global myList
    myList = my_input.split(",")
    return


def print_list():
    global myList
    print("\nYou have the following people in your list:")
    for person in myList:
        print(person)
    print()
    return


def verify_list():
    print("Would you like to verify your list of people? (y/n)")
    while True:
        my_ans = input("> ")
        if my_ans.lower() == 'y' or my_ans.lower() == 'n':
            break
        else:
            print('Please enter (y) or (n)!')

    if my_ans.lower() == 'y':
        print_list()
        print("Would you like to change your list? (y/n)")
        while True:
            change = input("> ")
            if change.lower() == 'y' or change.lower() == 'n':
                break
            else:
                print('Please enter (y) or (n)!')
        if change.lower() == 'y':
            create_list()
            return True
        else:
            print("Starting chat monitor...\n\n")
            return False
    else:
        print("Starting chat monitor...\n\n")
        return False


def geturl():
    global live_chat
    global mo
    # Get video URL and split off the video ID
    while True:
        print("Please enter the YouTube Live Stream URL, then press Enter: ")
        video_url = input()
        try:
            url = re.compile(r'^((?:https?:)?\/\/)?((?:www|m)\.)?((?:youtube\.com|youtu.be))(\/(?:[\w\-]+\?v=|embed\/|v\/)?)([\w\-]+)(\S+)?$')
            mo = url.search(video_url)
            live_chat = LiveChat(mo.group(5))
            break
        except:
            print("Invalid YouTube URL! Please try again!\n")
            continue


def pad_to_center(l: list, w: int) -> str:
    """Manual centering"""
    padding = ' '*(w//2)
    parts = [padding[0: (w-len(p))//2+1]+p for p in l]
    return '\n'.join(parts)


def print_welcome():
    logo = r"""
                                   (            
  *   )    )           (           )\ )  *   )  
` )  /( ( /(    (      )\      (  (()/(` )  /(  
 ( )(_)))\())  ))\   (((_)     )\  /(_))( )(_)) 
(_(_())((_)\  /((_)  )\___  _ ((_)(_)) (_(_())  
|_   _|| |(_)(_))   ((/ __|| | | || |  |_   _|  
  | |  | ' \ / -_)   | (__ | |_| || |__  | |    
  |_|  |_||_|\___|    \___| \___/ |____| |_|    

"""
    print(pad_to_center(logo.splitlines(), 80))
    print("########################".center(80))
    print("Sup Chad, let's go baby!".center(80))
    print("########################".center(80))
    print("\n\n\n")


alarm_filename = 'alarm.mp3'
# Alarm file
alarm = Path(alarm_filename)

myList = []
  
# Welcome
print_welcome()

geturl()
    

while myList == []:
    create_list()

verified = True
while verified:
    verified = verify_list()

while live_chat.is_alive():
    try:
        chat_data = live_chat.get()
        for c in chat_data.items:
            if c.author.name in myList:
                if alarm.exists():
                    playsound(alarm_filename)
                print(f"{c.datetime} [{c.author.name}] - {c.message}")
                chat_data.tick()
    except KeyboardInterrupt:
        live_chat.terminate()
        break

if not live_chat.is_alive():
    print("URL is not currently a live stream")
    print("Would you like to start on the recorded stream? (y/n)")
    while True:
        playback = input("> ")
        if playback.lower() == 'y' or playback.lower() == 'n':
            break
        else:
            print('Please enter (y) or (n)!')
    if playback == 'y':
        live_chat = LiveChat(mo.group(5), seektime=1)
        while live_chat:
            try:
                chat_data = live_chat.get()
                for c in chat_data.items:
                    if c.author.name in myList:
                        if alarm.exists():
                            playsound(alarm_filename)
                        print("{} [{}] - {}".format(c.datetime,
                                                    c.author.name,
                                                    c.message))
                        chat_data.tick()
            except KeyboardInterrupt:
                live_chat.terminate()
                sys.exit()
    else:
        print("Program will now exit...")
        sys.exit()
