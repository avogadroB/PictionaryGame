# -*- coding: utf-8 -*-
"""
Created on Tue Feb  6 21:26:35 2024

@author: ahsib
"""

"""
PSDL-1 miniproject: 2-Player Pictionary Game

Team members:
    Isha Bhagat-UCE2022428
    Sukhada Bhagwat-UCE2022429
    Rishita Chourey-UCE2022444

"""
import tkinter as tk
from tkinter import Toplevel
import random
import time
# Create a function to display the welcome message and instructions
def display_instructions():
    # Create a pop-up window for instructions
    instructions_popup = Toplevel(root)
    instructions_popup.title("Welcome to Pictionary")
    instructions_popup.configure(bg="yellow")
    # Adjust the window size
    instructions_popup.geometry("1000x550")
    
    # Define the welcome text and game instructions
    welcome_text = "Welcome to Pictionary\n\nGame Instructions:\n\n" \
                  "• This is a 2 player game to be played on a single screen.\n" \
                  "• For the first 5 seconds after starting the game, a word prompt will be displayed on the screen for Player 1 to draw.\n" \
                  "  - Player 1 has 15 seconds to draw the word after which the screen will freeze.\n" \
                  "• After these 15 seconds, Player 2 will be given 3 chances to guess and type the word.\n" \
                  "• This game will be played in 2 rounds of 3 drawings each.\n" \
                  "  - In the first round, word prompts will be given to Player 1 for 3 times, and Player 2 will have to guess. Vice versa for Round 2.\n" \
                  "• Point Scheme:\n" \
                  "  - If the other player is able to guess correctly:\n" \
                  "    - Player who drew: 10 points awarded\n" \
                  "    - Player who guesses: 5 points awarded\n" \
                  "• At the end of both rounds, the player with the highest points will win!"
    

    welcome_label = tk.Label(instructions_popup, text=welcome_text, font=("Arial", 12))
    welcome_label.pack(padx=20, pady=20)
    
    ok_button = tk.Button(instructions_popup, text="OK", command=lambda: on_ok_pressed(instructions_popup), font=("Arial", 16))  # Adjust the button font size
    ok_button.pack(side=tk.BOTTOM, padx=20, pady=20)

def on_ok_pressed(instructions_popup):
    instructions_popup.destroy()
    
def start_paint(event):
    global is_drawing, x, y
    if is_drawing:
        x, y = event.x, event.y
        canvas.create_oval(x, y, event.x, event.y, fill=pen_color, width=pen_width)

def paint(event):
    global is_drawing, x, y
    if is_drawing:
        x1, y1, x2, y2 = x, y, event.x, event.y
        canvas.create_line(x1, y1, x2, y2, fill=pen_color, width=pen_width)
        x, y = x2, y2

def stop_paint(event):
    global x, y
    x, y = None, None

def clear_canvas():
    canvas.delete("all")

def change_pen_color(color):
    global pen_color
    pen_color = color

def start_countdown():
    countdown()
    global is_drawing
    is_drawing = True

def countdown():
    global countdown_seconds
    if countdown_seconds > 0:
        countdown_seconds -= 1
        timer_label.config(text="Time Left: \n{} seconds".format(countdown_seconds))
        root.after(1000, countdown)
    else:
        check_button.config(state="normal") #enable the check button
        global is_drawing
        is_drawing = False
        show_times_up_message()

def show_times_up_message():
    timer_label.config(text="Time's up!", font=("Arial", 24))
    timer_label.place(relx=0.5, rely=0.5, anchor=tk.LEFT)
    update_scoreboard()
        
def display_random_word_popup(word):
    popup = Toplevel(root)
    popup.title("Random Word")
    label = tk.Label(popup, text=word, font=("Arial", 24))
    label.pack(padx=20, pady=20)
    root.after(5000, popup.destroy)  # Close the popup after 5 seconds

def show_success_popup():
    success_popup = Toplevel(root)
    success_popup.title("Success!")
    
    global score_player1, score_player2
    if (round_number <= 3):
        # Player 1 is drawing in rounds 1, 2, 3, and Player 2 guessed correctly
        score_player1 += 10
        score_player2 += 5
    else:
        # Player 2 is drawing in rounds 4, 5, 6, and Player 1 guessed correctly
        score_player1 += 5
        score_player2 += 10
    
    update_scoreboard()
    
    success_label = tk.Label(success_popup, text="Congratulations!\nYou guessed the word correctly!", font=("Arial", 16), fg="green")
    success_label.pack(padx=20, pady=20)
    root.after(1000, success_popup.destroy)
    if round_number < total_rounds:
        next_round()
    else:
        end_game()

def check_guess():
    global flag
    guessed_word = guess_entry.get().strip()  # Get the user's guess and remove leading/trailing spaces
    if guessed_word.lower() == random_word.lower():
        show_success_popup()  # Display the success popup
    else:
        flag=flag+1
        success_label.config(text=("Try again"), fg="red", font=("Arial", 16))
    guess_entry.delete(0, tk.END)  # Clear the guess entry
    if(flag>3):
        if round_number < total_rounds:
            next_round()
            flag=0
        else:
            end_game()
        

def update_scoreboard():
    global score_player1, score_player2
    score_label.config(text=f"Player 1: {score_player1} points | Player 2: {score_player2} points")

def next_round():
    check_button.config(state="disabled")
    global round_number, random_word, countdown_seconds
    round_number += 1
    random_word = random.choice(words)
    display_random_word_popup(random_word)
    countdown_seconds = 15
    timer_label.config(text="Time Left: {} seconds".format(countdown_seconds))
    success_label.config(text="")
    clear_canvas()
    root.after(5000, start_countdown)
    update_round_number()  # Update the round number label

# Function to update the round number label
def update_round_number():
    round_label.config(text=f"Round: {round_number} of {total_rounds}")

# Function to update the round number label
def update_round_number():
    round_number_var.set(f"Round: {round_number} of {total_rounds}")
    
def end_game():
    # Close the main game window
    root.destroy()

    # Create a new window for displaying scores and declare the winner
    scores_window = tk.Tk()
    scores_window.title("Final Scores")
    scores_window.geometry("400x300")
    scores_window.configure(bg="green")

    # Display the final scores
    final_scores_label = tk.Label(scores_window, text="Game Over!\nFinal Scores:", font=("Arial", 20), bg="green", fg="white")
    final_scores_label.pack(pady=20)

    player1_score_label = tk.Label(scores_window, text=f"Player 1: {score_player1} points", font=("Arial", 16), bg="green", fg="white")
    player1_score_label.pack()

    player2_score_label = tk.Label(scores_window, text=f"Player 2: {score_player2} points", font=("Arial", 16), bg="green", fg="white")
    player2_score_label.pack()

    # Determine and display the winner
    if score_player1 > score_player2:
        winner_label = tk.Label(scores_window, text="Player 1 is the winner!", font=("Arial", 18), bg="green", fg="white")
    elif score_player2 > score_player1:
        winner_label = tk.Label(scores_window, text="Player 2 is the winner!", font=("Arial", 18), bg="green", fg="white")
    else:
        winner_label = tk.Label(scores_window, text="It's a tie!", font=("Arial", 18), bg="green", fg="white")

    winner_label.pack()

    scores_window.mainloop()

# Global variables for keeping track of the score
score_player1 = 0
score_player2 = 0
round_number = 1
total_rounds = 6

# Global variables for countdowns
countdown_seconds = 15

# Define a variable to store the random word
random_word = ""

root = tk.Tk()
root.title("Pictionary Game")
#root.wm_iconbitmap('C:/Users/DELL/Downloads/87_85240.ico')
root.geometry("1200x600")

canvas = tk.Canvas(root, bg="black", width=600, height=600,cursor='pencil')
canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

Instruction = tk.Button(root, text="Instructions", command=display_instructions, font=("Arial",20),bg='darkblue',fg='white')
Instruction.pack(side=tk.TOP, padx=10, pady=10)

pen_color = "white"
pen_width = 4

# Create a label to display the round number
# Create a StringVar to hold the round number
round_number_var = tk.StringVar()
round_number_var.set(f"Round: {round_number} of {total_rounds}")

# Create a label to display the round number
round_label = tk.Label(root, textvariable=round_number_var, font=("Arial", 16))
round_label.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)

is_drawing = True  # Flag to enable/disable drawing
x, y = None, None

canvas.bind("<Button-1>", start_paint)
canvas.bind("<B1-Motion>", paint)
canvas.bind("<ButtonRelease-1>", stop_paint)

countdown_seconds = 15  # Set your desired countdown time
timer_label = tk.Label(root, text="Time Left: {} seconds".format(countdown_seconds), font=("Arial", 16))
timer_label.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)

# Random words
words = [
    "Dog", "Beach", "Pizza", "Robot", "Moon", "Guitar", "Cupcake", "Bicycle", "Tornado", "Unicorn", "Snowman", "Rainbow", "Pirate", "Vampire", "Dragon", "Butterfly", "Clown", "Camera", "Elephant", "Clock", "Surfing", "Telephone", "Spider", "Ice Cream", "Sunflower", "Scissors", "Castle", "Toothbrush", "Kangaroo", "Magnet", "Fireworks", "Helicopter", "Pizza", "Hamburger", "Eiffel Tower", "Football", "Lighthouse", "Telescope", "Pizza", "Anchor", "Cake", "Turtle", "Banana", "Cactus", "Pineapple", "Robot", "Umbrella", "Starfish", "Airplane", "Laptop", "Snowflake", "Moon", "Koala", "Octopus", "Lemon", "Penguin", "Car", "House", "Rocket", "Sun"
]


# Display a random word in a pop-up window for 5 seconds at the beginning
random_word = random.choice(words)
display_random_word_popup(random_word)
root.after(5000, start_countdown)

success_label = tk.Label(root, text="", font=("Arial", 16))
success_label.pack(side=tk.RIGHT, padx=10, pady=10)

# Create colored buttons for basic pen colors
color_buttons_frame = tk.Frame(root)
color_buttons_frame.pack(side=tk.TOP, padx=10, pady=10)

color_button_red = tk.Button(color_buttons_frame, bg="red", width=5, height=2, command=lambda:change_pen_color("red"))
color_button_yellow = tk.Button(color_buttons_frame, bg="yellow", width=5, height=2, command=lambda:change_pen_color("yellow"))
color_button_blue = tk.Button(color_buttons_frame, bg="blue", width=5, height=2, command=lambda:change_pen_color("blue"))
color_button_green = tk.Button(color_buttons_frame, bg="green", width=5, height=2, command=lambda:change_pen_color("green"))
color_button_orange = tk.Button(color_buttons_frame, bg="orange", width=5, height=2, command=lambda:change_pen_color("orange"))
color_button_brown = tk.Button(color_buttons_frame, bg="brown", width=5, height=2, command=lambda:change_pen_color("brown"))
color_button_black = tk.Button(color_buttons_frame, bg="black", width=5, height=2, command=lambda:change_pen_color("black"))
color_button_white = tk.Button(color_buttons_frame, bg="white", width=5, height=2, command=lambda:change_pen_color("white"))
color_button_purple = tk.Button(color_buttons_frame, bg="purple", width=5, height=2, command=lambda:change_pen_color("purple"))

color_button_red.grid(row=0, column=0, padx=5, pady=5)
color_button_yellow.grid(row=0, column=1, padx=5, pady=5)
color_button_blue.grid(row=0, column=2, padx=5, pady=5)
color_button_green.grid(row=1, column=0, padx=5, pady=5)
color_button_orange.grid(row=1, column=1, padx=5, pady=5)
color_button_brown.grid(row=1, column=2, padx=5, pady=5)
color_button_black.grid(row=2, column=0, padx=5, pady=5)
color_button_white.grid(row=2, column=1, padx=5, pady=5)
color_button_purple.grid(row=2, column=2, padx=5, pady=5)

# Add a scoreboard
score_label = tk.Label(root, text="Player 1: 0 points | Player 2: 0 points", font=("Arial", 16))
score_label.pack(side=tk.TOP, padx=10, pady=10)

guess_frame = tk.Frame(root)
guess_frame.pack(side=tk.RIGHT, padx=10, pady=10)

guess_label = tk.Label(guess_frame, text="Guess the Word:", font=("Arial", 16))
guess_label.pack(side=tk.TOP, padx=10, pady=10)
guess_entry = tk.Entry(guess_frame, font=("Arial", 16))
guess_entry.pack(side=tk.TOP, padx=10, pady=10)

check_button = tk.Button(guess_frame, text="Check Guess", font=("Arial", 16), command=check_guess)
flag=0
check_button.pack(side=tk.TOP, padx=10, pady=10)
check_button.config(state="disabled")

menu = tk.Menu(root)
root.config(menu=menu)

file_menu = tk.Menu(menu)
menu.add_cascade(label="Canvas Options", menu=file_menu)
file_menu.add_command(label="Clear Canvas", command=clear_canvas)
file_menu.add_command(label="Exit", command=root.quit)

root.mainloop()