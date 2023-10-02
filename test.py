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

def refresh_image(canvas, img, image_path, image_id):
    print('b')
    if token:
        current_song = sp.currently_playing()
        print(current_song['item']['album']['images'][0]['url'])
        print(current_song['item']['album']['name'])
        print(current_song['item']['album']['artists'][0]['name'])


    # image_bytes = urlopen(current_song['item']['album']['images'][0]['url']).read()
    # data_stream = io.BytesIO(image_bytes)
    # pil_image = Image.open(data_stream).resize((400,400), Image.ANTIALIAS)
    # tk_image = ImageTk.PhotoImage(pil_image)


    # image_bytes = urlopen('https://i.scdn.co/image/ab67616d0000b273894842f6e437f87263785977').read()
    # data_stream = io.BytesIO(image_bytes)
    # pil_image = Image.open(data_stream)
    # first = ImageTk.PhotoImage(pil_image)
    # test=ImageTk.PhotoImage(file='1.png')



    response = requests.get(current_song['item']['album']['images'][0]['url'])
    img1 = Image.open(BytesIO(response.content)).resize((400,400), Image.ANTIALIAS)

    # pil_img = Image.open('1.png').resize((400,400), Image.ANTIALIAS)
    img = ImageTk.PhotoImage(img1)


    canvas.itemconfigure(image_id, image=img)

    canvas.after(2000, refresh_image, canvas, img, image_path, image_id)  

root = tk.Tk()
# root.overrideredirect(True)
root.config(bg="blue", bd=0, highlightthickness=0)
root.attributes("-transparentcolor", "blue","-topmost", True)
image_path = 'placeholder.png'

canvas = tk.Canvas(root, bg="blue", bd=0, highlightthickness=0, height=400, width=400)
img = None  # initially only need a canvas image place-holder
image_id = canvas.create_image(200, 200, image=img)
canvas.pack()

refresh_image(canvas, img, image_path, image_id)
root.mainloop()