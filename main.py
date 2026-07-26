import os
import random
from tkinter import *
import tkinter as tk
from PIL import Image, ImageTk, ImageSequence

win_path = "assets/win.gif"
lose_path = 'assets/lose.gif'
draw_path = 'assets/draw.gif'

options = ['rock', 'scissor', 'paper']

win_conditions = {
    'scissor': 'paper',
    'paper': 'rock',
    'rock': 'scissor',
}

choice_pngs = {
    'rock': 'assets/rock.jpg',
    'paper': 'assets/paper.jpg',
    'scissor': 'assets/scissor.jpg'
}

choice_emojis = {
    'scissor': '✌️',
    'paper': '✋',
    'rock': '✊'
}

player_score = 0
computer_score = 0
draws = 0

result_label = None
result_gif = None
score_label = None
computer_choice_label = None
computer_choice_img_label = None
timer_label = None
buttons = []
emoji_labels = []
is_animating = False
loaded_png_images = {}


def play_sound(sound_type):
    try:
        import winsound
        if sound_type == 'win':
            winsound.Beep(1000, 300)
        elif sound_type == 'lose':
            winsound.Beep(400, 300)
        elif sound_type == 'draw':
            winsound.Beep(600, 200)
    except ImportError:
        pass


def load_choice_images():
    global loaded_png_images
    for key, path in choice_pngs.items():
        if os.path.exists(path):
            img = Image.open(path).convert("RGBA")
            img = img.resize((80, 80), Image.Resampling.LANCZOS)
            loaded_png_images[key] = ImageTk.PhotoImage(img)
        else:
            loaded_png_images[key] = None


def create_gif(root, gif_path, x, y, scale):
    if not os.path.exists(gif_path):
        return None
    gif = Image.open(gif_path)
    frames = []

    for frame in ImageSequence.Iterator(gif):
        frame = frame.copy().convert("RGBA")
        if scale != 1:
            width = int(frame.width * scale)
            height = int(frame.height * scale)
            frame = frame.resize((width, height), Image.Resampling.LANCZOS)
        frames.append(ImageTk.PhotoImage(frame))

    label = Label(root, bg='#F0F0F0')
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
    if not os.path.exists(path):
        return None
    image = Image.open(path)
    if scale != 1:
        width = int(image.width * scale)
        height = int(image.height * scale)
        image = image.resize((width, height), Image.Resampling.LANCZOS)
    photo = ImageTk.PhotoImage(image)

    label = Label(root, image=photo, bg='#F0F0F0')
    label.image = photo
    label.place(x=x, y=y)
    return label


def update_score():
    global score_label
    if score_label and score_label.winfo_exists():
        score_label.destroy()
    score_label = tk.Label(
        root,
        text=f"You: {player_score} | Draw: {draws} | Computer: {computer_score}",
        font=("Arial", 12, 'bold'),
        fg='white',
        bg='#333',
        padx=15,
        pady=5
    )
    score_label.place(relx=0.5, y=10, anchor='n')


def set_buttons_state(state):
    for btn in buttons:
        if btn.winfo_exists():
            btn.config(state=state)


def start_game():
    global result_label, result_gif, computer_choice_label, computer_choice_img_label, timer_label, buttons, emoji_labels, is_animating
    
    is_animating = False

    for widget in root.winfo_children():
        if hasattr(widget, 'animation_id') and widget.animation_id:
            root.after_cancel(widget.animation_id)
        widget.destroy()

    buttons = []
    emoji_labels = []

    create_img(root, 'assets/player.jpg', 25, 25, 0.5)
    player_name = tk.Label(root, text="👤 Player", font=('Arial', 14, 'bold'), fg='#333', bg='#F0F0F0')
    player_name.place(x=90, y=225)

    create_img(root, 'assets/computer.jpg', 565, 25, 0.192)
    computer_name = tk.Label(root, text='🤖 Computer', font=('Arial', 14, 'bold'), fg='#333', bg='#F0F0F0')
    computer_name.place(x=620, y=225)

    update_score()

    computer_choice_label = tk.Label(root, text="", font=("Arial", 14, 'bold'), fg='#333', bg='#F0F0F0')
    computer_choice_label.place(relx=0.5, y=250, anchor='center')

    computer_choice_img_label = tk.Label(root, bg='#F0F0F0')
    computer_choice_img_label.place(relx=0.5, y=295, anchor='center')

    timer_label = tk.Label(root, text="", font=("Arial", 15, 'bold'), fg='#E63946', bg='#F0F0F0')
    timer_label.place(relx=0.5, y=345, anchor='center')

    scis_emoji = tk.Label(root, text="✌️", font=('Arial', 22), bg='#F0F0F0')
    scis_emoji.place(x=165, y=465)

    pap_emoji = tk.Label(root, text="✋", font=('Arial', 22), bg='#F0F0F0')
    pap_emoji.place(x=380, y=465)

    rk_emoji = tk.Label(root, text="✊", font=('Arial', 22), bg='#F0F0F0')
    rk_emoji.place(x=595, y=465)

    scissor_btn = tk.Button(
        root, text="SCISSOR", activebackground='#FF6B6B', activeforeground='white',
        width=13, height=2, bg='#FF8787', fg='white', font=('Arial', 13, 'bold'),
        relief='raised', bd=3, cursor='hand2', command=lambda: start_countdown("scissor")
    )
    scissor_btn.place(x=100, y=510)

    paper_btn = tk.Button(
        root, text="PAPER", activebackground='#4ECDC4', activeforeground='white',
        width=13, height=2, bg='#45B7AA', fg='white', font=('Arial', 13, 'bold'),
        relief='raised', bd=3, cursor='hand2', command=lambda: start_countdown("paper")
    )
    paper_btn.place(x=315, y=510)

    rock_btn = tk.Button(
        root, text="ROCK", activebackground='#FFB84D', activeforeground='white',
        width=13, height=2, bg='#FFD93D', fg='#333', font=('Arial', 13, 'bold'),
        relief='raised', bd=3, cursor='hand2', command=lambda: start_countdown("rock")
    )
    rock_btn.place(x=530, y=510)

    buttons = [scissor_btn, paper_btn, rock_btn]


def start_countdown(player_choice):
    global is_animating, result_label, result_gif
    if is_animating:
        return

    is_animating = True
    set_buttons_state(tk.DISABLED)

    if result_label and result_label.winfo_exists():
        result_label.destroy()
    if result_gif and result_gif.winfo_exists():
        result_gif.destroy()

    run_countdown(player_choice, total_ms=5000, elapsed_ms=0)


def run_countdown(player_choice, total_ms, elapsed_ms):
    global is_animating

    remaining_sec = max(1, (total_ms - elapsed_ms + 999) // 1000)
    
    random_option = random.choice(options)
    shuffled_img = loaded_png_images.get(random_option)

    computer_choice_label.config(text="Computer choosing...")
    if shuffled_img:
        computer_choice_img_label.config(image=shuffled_img)
        computer_choice_img_label.image = shuffled_img

    timer_label.config(text=f"⏳ Deciding in: {remaining_sec}s")

    if elapsed_ms < total_ms:
        root.after(150, run_countdown, player_choice, total_ms, elapsed_ms + 150)
    else:
        timer_label.config(text="")
        is_animating = False
        set_buttons_state(tk.NORMAL)
        evaluate_game(player_choice)


def evaluate_game(player_choice):
    global player_score, computer_score, draws

    computer_choice = random.choice(options)
    
    final_img = loaded_png_images.get(computer_choice)
    computer_choice_label.config(text=f"Computer chose: {computer_choice.upper()}")
    if final_img:
        computer_choice_img_label.config(image=final_img)
        computer_choice_img_label.image = final_img

    if player_choice == computer_choice:
        result = "🤝 It's a Draw!"
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

    show_result(result, gif)
    update_score()


def show_result(text, gif_path):
    global result_label, result_gif

    if result_label and result_label.winfo_exists():
        result_label.destroy()
    if result_gif and result_gif.winfo_exists():
        result_gif.destroy()

    result_label = Label(root, text=text, font=("Arial", 18, 'bold'), fg='#333', bg='#F0F0F0')
    result_label.place(relx=0.38, y=385, anchor='center')

    result_gif = create_gif(root, gif_path, 460, 345, 0.22)


root = Tk()
root.geometry("800x600")
root.title("🎮 Rock Paper Scissors Game 🎮")
root.resizable(False, False)
root.config(bg='#F0F0F0')

load_choice_images()

hello_message = Label(root, text="🎮 Welcome to Rock Paper Scissors 🎮", font=("Arial", 20, 'bold'), fg='#FF6B6B', bg='#F0F0F0')
hello_message.place(x=130, y=170)

create_gif(root, "assets/hi.gif", 280, 230, 0.5)

welcome_btn = tk.Button(
    root,
    text="Let's Play!",
    font=("Arial", 14, 'bold'),
    width=20,
    height=2,
    cursor='hand2',
    bg='#45B7AA',
    fg='white',
    activebackground='#4ECDC4',
    activeforeground='white',
    relief='raised',
    bd=3,
    command=start_game
)
welcome_btn.place(x=275, y=420)

root.mainloop()
