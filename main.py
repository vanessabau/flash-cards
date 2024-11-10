from tkinter import *
import pandas
import random

BACKGROUND_COLOR = "#B1DDC6"
current_card = {}
to_learn = {}
try:
    data = pandas.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    original_data = pandas.read_csv("data/french_words.csv")
    to_learn= original_data.to_dict(orient="records")
else:
    to_learn=data.to_dict(orient="records")


# ---------------------------- FUNCTIONS ------------------------------- #
def next_card():
    global current_card, flip_timer
    window.after_cancel(flip_timer)
    current_card = random.choice(to_learn)
    canvas.itemconfig(card_title, text="French", fill="black")
    canvas.itemconfig(card_word, text=current_card["French"], fill="black")
    canvas.itemconfig(card_background, image=card_front_img)
    flip_timer = window.after(3000, func=flip_card)

def flip_card():
    canvas.itemconfig(card_title, text="English", fill="white")
    canvas.itemconfig(card_word, text=current_card["English"], fill="white")
    canvas.itemconfig(card_background, image=card_back_img)

def is_known():
    to_learn.remove(current_card)
    data = pandas.DataFrame(to_learn)
    data.to_csv("data/words_to_learn.csv", index=False)
    next_card()

# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Flashy")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

flip_timer = window.after(3000, func=flip_card)
canvas = Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)

# ---------------------------- CARD SETUP ------------------------------- #
card_front_img = PhotoImage(file="images/card_front.png")
card_back_img = PhotoImage(file="images/card_back.png")

card_background = canvas.create_image(400, 263, image=card_front_img)
canvas.grid(column=0, row=0, columnspan=2)

# ---------------------------- WORDS ------------------------------- #
card_title = english_word = canvas.create_text(400, 150, text="English", font=("Ariel", 40, "italic"))

card_word = french_word = canvas.create_text(400, 263, text="Anglais", font=("Ariel", 60, "bold"))

# ---------------------------- BUTTONS ------------------------------- #
no_button_img = PhotoImage(file="images/wrong.png")
no_button = Button(image=no_button_img, highlightthickness=0, command=next_card)
no_button.grid(column=0, row=2)

yes_button_img = PhotoImage(file="images/right.png")
yes_button = Button(image=yes_button_img, highlightthickness=0, command=is_known)
yes_button.grid(column=1, row=2)

next_card()

window.mainloop()
