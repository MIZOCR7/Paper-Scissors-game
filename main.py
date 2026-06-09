import random
from tkinter import *
import tkinter as tk
from PIL import Image, ImageTk, ImageSequence 


win_path = "assets/win.gif"
lose_path = 'assets/lose.gif'
draw_path = 'assets/draw.gif'


def create_gif(root, gif_path, x, y, scale):
  gif = Image.open(gif_path)
  
  frames = []
  
  for frame in ImageSequence.Iterator(gif):
    frame = frame.copy().convert("RGBA")
    
    if scale != 1:
      width = int(frame.width * scale)
      height = int(frame.height * scale)
      frame = frame.resize((width,height), Image.Resampling.LANCZOS)
    frames.append(ImageTk.PhotoImage(frame))
  
  
  label = Label(root)
  label.place(x=x, y=y)
  
  delay = gif.info.get('duration', 100)
  
  def animate(frame_index=0):
    label.config(image=frames[frame_index])
    root.after(delay, animate, (frame_index + 1) % len(frames))
  
  animate()
  
  label.frames = frames
  
  return label

def create_img(root, path, x, y, scale):
  image = Image.open(path)
  
  if scale != 1:
    width = int(image.width * scale)
    height = int(image.height * scale)
    image = image.resize((width,height), Image.Resampling.LANCZOS)
  photo = ImageTk.PhotoImage(image)
  
  label = Label(root, image=photo)
  label.image = photo
  label.place(x=x, y=y)
  return label


def start_game():
  for widget in root.winfo_children():
      widget.destroy()
  
  player_img = 'assets/player.jpg'
  create_img(root, player_img, 25, 25, 0.5)
  player_name = tk.Label(root, text="Player")
  player_name.pack()
  player_name.place(x=90, y=225)
  
  computer_img = 'assets/computer.jpg'
  create_img(root, computer_img, 565, 25, 0.192)
  computer_name = tk.Label(root, text='Computer')
  computer_name.pack()
  computer_name.place(x=635,y=225)
  
  
   


root = Tk()
root.geometry("800x600")


hello_message = Label(root, text="Welcome to my game: ", font=("Arial", 20, 'bold'))
hello_message.pack()
hello_message.place(x=160, y=250)

hello_gif = "assets/hi.gif"
create_gif(root, hello_gif, 500, 180, 0.5)
welcome_btn = tk.Button(
  root,
  text="Let's go",
  font=("Arial", 12),
  width=20,
  height=3,
  cursor='hand2',
  command=start_game)
welcome_btn.pack()
welcome_btn.place(x=350,y=350)
 

root.mainloop()


