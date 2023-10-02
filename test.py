from PIL import Image, ImageTk
import tkinter as tk
import os
import shutil
import threading
import time
import sys
import spotipy
import spotipy.util as util
import spotipy.oauth2 as oauth2
from urllib.request import urlopen
import io
import requests
from io import BytesIO


token = util.prompt_for_user_token('317h99f45vnqujlkyiarzx3mr', 'user-read-currently-playing', '144bc246b721405a8f72b6f92ccead4d', '799c3ada2dba4a958eb152710108c211', 'http://localhost:8888/callback/')
sp = spotipy.Spotify(auth=token)
latest=None

def refresh_image(canvas, img, image_path, image_id):
    global latest,root
    if token:
        minw=min(root.winfo_height(),root.winfo_width())
        if minw<150:
            minw=150
        current_song = sp.currently_playing()
        print(current_song['item']['album']['images'][0]['url'])
        print(current_song['item']['album']['name'])
        print(current_song['item']['album']['artists'][0]['name'])
        response = requests.get(current_song['item']['album']['images'][0]['url'])
        img1 = Image.open(BytesIO(response.content)).resize((minw,minw), Image.ANTIALIAS)
        img = ImageTk.PhotoImage(img1)
        canvas.configure(width=minw*2,height=minw*2)
        canvas.itemconfigure(image_id, image=img)
        root.geometry(f'{minw}x{minw}')

        canvas.after(2000, refresh_image, canvas, img, image_path, image_id)

root = tk.Tk()
root.overrideredirect(True)


def move_app(e):
    root.geometry(f'+{e.x_root}+{e.y_root}')

root.config(bg="blue", bd=0, highlightthickness=0)
root.attributes("-transparentcolor", "blue","-topmost", True)
image_path = 'placeholder.png'

canvas = tk.Canvas(root, bg="blue", bd=0, highlightthickness=0,)
img = None  # initially only need a canvas image place-holder
image_id = canvas.create_image(0, 0, image=img,anchor="nw")
canvas.bind("<B1-Motion>",move_app)
canvas.pack()

refresh_image(canvas, img, image_path, image_id)
root.mainloop()