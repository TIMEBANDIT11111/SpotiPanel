from PIL import Image, ImageTk
import tkinter as tk
import spotipy
import spotipy.util as util
import requests
from io import BytesIO



Client_id='144bc246b721405a8f72b6f92ccead4d'
Client_secret='799c3ada2dba4a958eb152710108c211'


token = util.prompt_for_user_token('', 'user-read-currently-playing', Client_id, Client_secret, 'http://localhost:8888/callback/')
latest=None
sp = spotipy.Spotify(auth=token)
print(token)

def refresh_image(canvas, img, image_path, image_id,text_id):
    global sp,latest
    try:
        minw=min(root.winfo_height(),root.winfo_width())
        if minw<150:
            minw=150
        current_song = sp.currently_playing()
        # print(current_song)
        # print(current_song['item']['album']['images'][0]['url'])     -> album image
        # print(current_song['item']['album']['name'])      -> album name
        # print(current_song['item']['album']['artists'][0]['name'])    -> artist name
        # print(current_song['item']['name'])     -> song name
        response = requests.get(current_song['item']['album']['images'][0]['url'])
        img = ImageTk.PhotoImage(Image.open(BytesIO(response.content)).resize((minw,minw), Image.Resampling.LANCZOS))
        canvas.configure(width=minw,height=minw)
        canvas.itemconfigure(image_id, image=img)
        canvas.itemconfigure(text_id,text=current_song['item']['name'])
        canvas.moveto(text_id,minw//2,minw//2)
        canvas.after(1000, refresh_image, canvas, img, image_path, image_id,text_id)
    except spotipy.SpotifyException as e:
        print(e)
        print('token changing!')
        token = util.prompt_for_user_token('', 'user-read-currently-playing', Client_id, Client_secret, 'http://localhost:8888/callback/')
        sp = spotipy.Spotify(auth=token)
        img = ImageTk.PhotoImage(Image.open('150.png'))
        canvas.configure(width=minw,height=minw)
        canvas.itemconfigure(image_id, image=img)
        canvas.after(1000, refresh_image, canvas, img, image_path, image_id,text_id)
    except Exception as e:
        print(e)
        img = ImageTk.PhotoImage(Image.open('150.png'))
        canvas.configure(width=minw,height=minw)
        canvas.itemconfigure(image_id, image=img)
        canvas.after(1000, refresh_image, canvas, img, image_path, image_id,text_id)
    except KeyboardInterrupt:
        pass

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
text_id = canvas.create_text(75,75,text='SpotiPanel',anchor='center',fill='cyan')
canvas.bind("<B1-Motion>",move_app)
canvas.bind("<Double-Button-1>",resize_app_inc)
canvas.bind("<Double-Button-3>",resize_app_decr)
canvas.pack()
refresh_image(canvas, img, image_path, image_id,text_id)
root.mainloop()