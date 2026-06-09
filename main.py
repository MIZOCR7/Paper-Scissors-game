import random
from tkinter import *
import tkinter as tk
from PIL import Image, ImageTk, ImageSequence 


win_path = "assets/win.gif"
lose_path = 'assets/lose.gif'
draw_path = 'assets/draw.gif'

options = ['rock', 'scissor', 'paper']

win_conditions = {
  'scissor':'paper',
  'paper': 'rock',
  'rock': 'scissor',
}

player_score = 0
computer_score = 0
draws = 0
choice_emoji = {'rock': '✊', 'paper': '✋', 'scissor': '✌️'}

def play_sound(sound_type):
  import winsound
  if sound_type == 'win':
    winsound.Beep(1000, 300)
  elif sound_type == 'lose':
    winsound.Beep(400, 300)
  elif sound_type == 'draw':
    winsound.Beep(600, 200)

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
  label.animation_id = None
  
  def animate(frame_index=0):
    if label.winfo_exists():
      label.config(image=frames[frame_index])
      label.animation_id = root.after(delay, animate, (frame_index + 1) % len(frames))
  
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


result_label = None
result_gif = None
score_label = None
computer_choice_label = None

def update_score():
  global score_label
  if score_label:
    score_label.destroy()
  score_label = tk.Label(root, text=f"You: {player_score} | Draw: {draws} | Computer: {computer_score}", 
                         font=("Arial", 12, 'bold'), fg='white', bg='#333')
  score_label.place(relx=0.5, y=10, anchor='n')

def start_game():
  global result_label, result_gif
  for widget in root.winfo_children():
      if hasattr(widget, 'animation_id') and widget.animation_id:
        root.after_cancel(widget.animation_id)
      widget.destroy()
  
  player_img = 'assets/player.jpg'
  create_img(root, player_img, 25, 25, 0.5)
  player_name = tk.Label(root, text="Player", font=('Arial', 12))
  player_name.pack()
  player_name.place(x=90, y=225)
  
  update_score()
  
  player_name.config(text="👤 Player", font=('Arial', 14, 'bold'), fg='#333')
  
  computer_img = 'assets/computer.jpg'
  create_img(root, computer_img, 565, 25, 0.192)
  computer_name = tk.Label(root, text='🤖 Computer', font=('Arial', 14, 'bold'), fg='#333')
  computer_name.pack()
  computer_name.place(x=620,y=225)
  
  scissor_btn = tk.Button(root,
                          text="✌️ SCISSOR",
                          activebackground='#FF6B6B',
                          activeforeground='white',
                          width=15,
                          height=3,
                          bg='#FF8787',
                          fg='white',
                          font=('Arial', 14, 'bold'),
                          relief='raised',
                          bd=3,
                          command=lambda: play("scissor"))
  scissor_btn.pack()
  scissor_btn.place(x=100,y=500)
  
  paper_btn = tk.Button(root,
                          text="✋ PAPER",
                          activebackground='#4ECDC4',
                          activeforeground='white',
                          width=15,
                          height=3,
                          bg='#45B7AA',
                          fg='white',
                          font=('Arial', 14, 'bold'),
                          relief='raised',
                          bd=3,
                          command=lambda: play("paper"))
  paper_btn.pack()
  paper_btn.place(x=300,y=500)
  
  rock_btn = tk.Button(root,
                          text="✊ ROCK",
                          activebackground='#FFB84D',
                          activeforeground='white',
                          width=15,
                          height=3,
                          bg='#FFD93D',
                          fg='#333',
                          font=('Arial', 14, 'bold'),
                          relief='raised',
                          bd=3,
                          command=lambda: play("rock"))
  rock_btn.pack()
  rock_btn.place(x=500,y=500) 
  
  def play(player_choice):
    global player_score, computer_score, draws, computer_choice_label
    computer_choice = random.choice(options)
    if player_choice == computer_choice:
      result = '🤝 It\'s a Draw!'
      gif = draw_path
      draws += 1
      play_sound('draw')
    elif computer_choice in win_conditions[player_choice]:
      result = "🎉 You Win! 🎉"
      gif = win_path
      player_score += 1
      play_sound('win')
    else:
      result = "😢 You Lose!"
      gif = lose_path
      computer_score += 1
      play_sound('lose')
    
    if computer_choice_label:
      computer_choice_label.destroy()
    computer_choice_label = tk.Label(root, text=f"Computer chose: {choice_emoji[computer_choice]}", font=("Arial", 16, 'bold'), fg='#333', bg='#F0F0F0')
    computer_choice_label.place(relx=0.5, y=300, anchor='center')
    
    show_result(result, gif)
    update_score()
  
  def show_result(text, gif_path):
    global result_label, result_gif
    
    if result_label:
      result_label.destroy()
    if result_gif:
      result_gif.destroy()
      
    result_label = Label(root, text=text, font=("Arial", 20, 'bold'))
    result_label.config(fg='#333', bg='#F0F0F0')
    result_label.place(x=230, y=350)
    
    result_gif = create_gif(root, gif_path, 480, 350, 0.3)


root = Tk()
root.geometry("800x600")
root.title("🎮 Rock Paper Scissors Game 🎮")
root.resizable(False, False)
root.config(bg='#F0F0F0')


hello_message = Label(root, text="Welcome to my game: ", font=("Arial", 20, 'bold'))
hello_message.config(fg='#FF6B6B', bg='#F0F0F0', text="🎮 Welcome to Rock Paper Scissors 🎮")
hello_message.pack()
hello_message.place(x=130, y=170)

hello_gif = "assets/hi.gif"
create_gif(root, hello_gif, 280, 230, 0.5)
welcome_btn = tk.Button(
  root,
  text="Let's Play!",
  font=("Arial", 14, 'bold'),
  width=20,
  height=3,
  cursor='hand2',
  bg='#45B7AA',
  fg='white',
  activebackground='#4ECDC4',
  activeforeground='white',
  relief='raised',
  bd=3,
  command=start_game)
welcome_btn.pack()
 
welcome_btn.place(x=275,y=380)

root.mainloop()


