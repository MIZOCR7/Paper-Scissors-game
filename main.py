import random
import os
import PIL
import time 

win_path = "assets/win.gif"
lose_path = 'assets/lose.gif'
draw_path = 'assets/draw.gif'

options = ['rock', 'paper', 'scissor']

win_conditions = {
  'rock':'scissor',
  'scissor':'paper',
  'paper':'rock'
}

def main():
  while True:
    user_input = input("Welcome to our game choose paper, scissor or rock or press 'q' to exit: ").lower()
    if user_input == 'q':
      break
    
    if user_input not in options:
      print('please: choose "paper", "scissor", "rock" \n')
      continue
    
    computer_choice = random.choice(options)
    if user_input == computer_choice:
      print("It is Draw :)")
    elif computer_choice == win_conditions[user_input]:
      print("U win :)")
    else:
      print("U lost") 
  
main()
