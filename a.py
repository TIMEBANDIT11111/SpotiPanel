import sys
import spotipy
import spotipy.util as util
import spotipy.oauth2 as oauth2
import time
import tkinter as tk
from tkinter import *
from PIL import Image, ImageTk
from urllib.request import urlopen
import io
import threading

token = util.prompt_for_user_token('317h99f45vnqujlkyiarzx3mr', 'user-read-currently-playing', '144bc246b721405a8f72b6f92ccead4d', '799c3ada2dba4a958eb152710108c211', 'http://localhost:8888/callback/')
sp = spotipy.Spotify(auth=token)
a=['placeholder.png']




def app():
    global root
    root = tk.Tk()
    root.overrideredirect(True)
    root.config(bg="blue", bd=0, highlightthickness=0)
    root.attributes("-transparentcolor", "blue","-topmost", True)
    canvas = tk.Canvas(root, bg="blue", bd=0, highlightthickness=0,width=root.winfo_screenwidth(),height=root.winfo_screenheight())



    canvas.create_image(root.winfo_screenwidth()/2,root.winfo_screenheight()/2,image=tk_image,anchor="center")
    canvas.pack(expand=True)
    root.mainloop()


class GUI(Frame):
    def __init__(self, master=None):
        threading.Thread(target=self.choose,daemon=True).start()
        self.root = tk.Tk()
        self.root.overrideredirect(True)
        self.root.config(bg="blue", bd=0, highlightthickness=0)
        self.root.attributes("-transparentcolor", "blue","-topmost", True)
        self.canvas = tk.Canvas(self.root, bg="blue", bd=0, highlightthickness=0,width=self.root.winfo_screenwidth(),height=self.root.winfo_screenheight())

        image_bytes = urlopen('https://i.scdn.co/image/ab67616d0000b273894842f6e437f87263785977').read()
        data_stream = io.BytesIO(image_bytes)
        pil_image = Image.open(data_stream)
        first = ImageTk.PhotoImage(pil_image)
        self.image_on_canvas=self.canvas.create_image(self.root.winfo_screenwidth()/2,self.root.winfo_screenheight()/2,image=first,anchor="center")
        self.canvas.pack(expand=True)
        self.root.mainloop()


    def choose(self):
        print('a')
        time.sleep(1)
        print('b')
        # image_bytes = urlopen('https://i.scdn.co/image/ab67616d0000b2739e1cfc756886ac782e363d79').read()
        # data_stream = io.BytesIO(image_bytes)
        # pil_image = Image.open(data_stream)
        # tk_image = ImageTk.PhotoImage(pil_image)
        self.canvas.delete()
        self.image_on_canvas=self.canvas.create_image(self.root.winfo_screenwidth(),self.root.winfo_screenheight(),image=tk.PhotoImage(file='placeholder.png'),anchor="center")
        # self.canvas.itemconfig(self.image_on_canvas, image=tk.PhotoImage(file='logo.png'))

while 1:
    panel=GUI()
    time.sleep(1)
    print(a)
    
    # GUI().choose()
    
    
    # if token:
    #     current_song = sp.currently_playing()

    #     print(current_song['item']['album']['images'][0]['url'])
    #     print(current_song['item']['album']['name'])
    #     print(current_song['item']['album']['artists'][0]['name'])

    # else:
    #     print("Can't get token for", username)



