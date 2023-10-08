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
latest=None
# token='BQCc8Rrx0NPg8TCHIYDAA0B5zerX-YvtQSjxV_qpR_O3-EImk7RNvEr0ynnupJRMDZSJT4uBkkxwsn6JXkgF5VSYG9Y0Xbbe8WZYjDOLM_ycvzqyD4aB5vb2zWFHfrdmK3e3X-RIYRzWkygw_Lxc30N9U8zJFZJL4iTNvgdpbkLrku9Nreqh4DbK7RybTgEFyYXxwiAJ1AkVK5CHtw1Kgw'
sp = spotipy.Spotify(auth=token)
print(token)

def refresh_image(canvas, img, image_path, image_id):
    try:
        minw=min(root.winfo_height(),root.winfo_width())
        if minw<150:
            minw=150
        # print(current_song['item']['album']['images'][0]['url'])
        # print(current_song['item']['album']['name'])
        # print(current_song['item']['album']['artists'][0]['name'])
        current_song = sp.currently_playing()
        response = requests.get(current_song['item']['album']['images'][0]['url'])
        img = ImageTk.PhotoImage(Image.open(BytesIO(response.content)).resize((minw,minw), Image.ANTIALIAS))
        canvas.configure(width=minw,height=minw)
        canvas.itemconfigure(image_id, image=img)
        canvas.after(1000, refresh_image, canvas, img, image_path, image_id)
    except spotipy.SpotifyException as e:
        print(e)
        print('token expired!')
        token = util.prompt_for_user_token('317h99f45vnqujlkyiarzx3mr', 'user-read-currently-playing', '144bc246b721405a8f72b6f92ccead4d', '799c3ada2dba4a958eb152710108c211', 'http://localhost:8888/callback/')
        img = ImageTk.PhotoImage(Image.open('150.png'))
        canvas.configure(width=minw,height=minw)
        canvas.itemconfigure(image_id, image=img)
        canvas.after(1000, refresh_image, canvas, img, image_path, image_id)
    # except Exception as e:
    #     print(e)
    #     img = ImageTk.PhotoImage(Image.open('150.png'))
    #     canvas.configure(width=minw,height=minw)
    #     canvas.itemconfigure(image_id, image=img)
    #     canvas.after(1000, refresh_image, canvas, img, image_path, image_id)




root = tk.Tk()
root.overrideredirect(True)


def move_app(e):
    root.geometry(f'+{e.x_root}+{e.y_root}')

def resize_app_inc(e):
    root.geometry(f'{root.winfo_height()+5}x{root.winfo_height()+5}')

def resize_app_decr(e):
    root.geometry(f'{root.winfo_height()-5}x{root.winfo_height()-5}')


root.config(bg="blue", bd=0, highlightthickness=0)
root.attributes("-transparentcolor", "blue","-topmost", True)
image_path = 'placeholder.png'
canvas = tk.Canvas(root, bg="blue", bd=0, highlightthickness=0,)
img = None  # initially only need a canvas image place-holder
image_id = canvas.create_image(0, 0, image=img,anchor="nw")
canvas.bind("<B1-Motion>",move_app)
canvas.bind("<Double-Button-1>",resize_app_inc)
canvas.bind("<Double-Button-3>",resize_app_decr)
canvas.pack()
refresh_image(canvas, img, image_path, image_id)
root.mainloop()