from tkinter import *
import time
from pytchat import LiveChat
from threading import Thread
import re
import sys


def receive():
    """Handles receiving of chat messages."""
    while live_chat.is_alive():
        try:
            chat_data = live_chat.get()
            for c in chat_data.items:
                msg = f"{c.datetime} [{c.author.name}] - {c.message}\n"
                msg_list.insert(END, msg)
                msg_list.see(END)
                chat_data.tick()
        except KeyboardInterrupt:
            live_chat.terminate()
            break


def on_close():
    """Handles when window is closed."""
    sys.exit()


def send(event=None):  # event is passed by binders.
    """Handles sending of messages."""
    global live_chat
    video_url = my_msg.get()
    try:
        url = re.compile(
            r'^((?:https?:)?\/\/)?((?:www|m)\.)?((?:youtube\.com|youtu.be))(\/(?:[\w\-]+\?v=|embed\/|v\/)?)([\w\-]+)(\S+)?$')
        mo = url.search(video_url)
        live_chat = LiveChat(mo.group(5))
        receive_thread = Thread(target=receive)
        receive_thread.start()
    except:
        msg = "Invalid YouTube URL! Please try again!\n"
        msg_list.insert(END, msg)
        msg_list.see(END)


window = Tk()

window.title("The Cult Chat Filter")
window.geometry('{}x{}'.format(640, 600))


logo_frame = Frame(window, width=630, height=200, pady=10)
url_frame = Frame(window, width=630, height=100, pady=3)
messages_frame = Frame(window, bg='white', width=630, height=300, pady=3)

logo = r"""
           )                   (            
  *   ) ( /(         (         )\ )  *   )  
` )  /( )\())(       )\     ( (()/(` )  /(  
 ( )(_)|(_)\ )\    (((_)    )\ /(_))( )(_)) 
(_(_()) _((_|(_)   )\___ _ ((_|_)) (_(_())  
|_   _|| || | __| ((/ __| | | | |  |_   _|  
  | |  | __ | _|   | (__| |_| | |__  | |    
  |_|  |_||_|___|   \___|\___/|____| |_|    
                                            
"""
w = Label(logo_frame, text=logo, font=("Courier", 8), justify=LEFT)
w.pack()
logo_frame.pack()


my_msg = StringVar()  # For the messages to be sent.
my_msg.set("")
url_label = Label(url_frame, text="Please enter the YouTube Live Stream URL, then click Send:", justify=LEFT)
url_label.pack()
entry_field = Entry(url_frame, textvariable=my_msg, width=75, justify=LEFT)
entry_field.bind("<Return>", send)
entry_field.pack()
send_button = Button(url_frame, text="Send", command=send, justify=LEFT)
send_button.pack()
url_frame.pack()

scrollbar = Scrollbar(messages_frame)  # To navigate through past messages.
# Following will contain the messages.
msg_list = Text(messages_frame, height=50, width=300, yscrollcommand=scrollbar.set, wrap=WORD)
msg_list.insert(END, "Waiting for URL...\n")
scrollbar.pack(side=RIGHT, fill=Y)
msg_list.pack(side=LEFT, fill=BOTH)
msg_list.pack()
messages_frame.pack()

window.protocol("WM_DELETE_WINDOW", on_close)


window.mainloop()  # Starts GUI execution.
