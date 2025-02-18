import dictionary
from tkinter import Tk, Entry, PhotoImage, Canvas, Toplevel, Label, Text, DISABLED, NORMAL, END
from tkmacosx import Button
import random

#---------------------------------CONSTANTS-----------------------------#

timer = None
timer_started=False
FONT_NAME = "Courier"
TEST_SEC = 60
TITLE="Typing speed test "
COLOR1 = "#FBF5DD"
COLOR2 = "#A6CDC6"
COLOR3 = "#16404D"
COLOR4 = "#DDA853"
COLOR_CORRECT="#008000"
COLOR_INCORRECT="#FF0000"
word_count=0
typed_words=[]
incorrect_words=[]
LISTS_OF_WORDS=random.sample(dictionary.word_list, len(dictionary.word_list))

#---------------------------------COUNTDOWN TIMER-----------------------#

def start_timer():
    global timer_started, word_count, typed_words
    word_count=0
    typed_words=[]
    input_field.config(state=NORMAL)
    input_field.focus()
    input_field.delete(0, END)
    update_displayed_text()
    timer_started=False
    canvas.itemconfig(timer_text, text="01:00")
    button_reset.configure(state="normal")
    button_start.configure(state="disabled")
    
def reset_button():
    global timer, word_count, typed_words
    if timer is not None:
        window.after_cancel(timer)
    canvas.itemconfig(timer_text,text="00:00")
    input_field.delete(0, END)
    input_field.config(state=DISABLED)
    word_count=0
    typed_words=[]
    update_displayed_text()
    button_shuffle.configure(state="normal")
    button_reset.configure(state="disabled")
    button_start.configure(state="normal")

def count_down(count):
    global word_count
    count_minute=int(count/60)
    count_seconds=count % 60
    canvas.itemconfig(timer_text, text=f"{count_minute:02}:{count_seconds:02}") #02 for 0 as the filler, 2 for the number of digits
    if count>0:
        global timer
        timer=window.after(1000, count_down, count-1)
    else:
        check_words()
        show_custom_message(f"Time's up! Your result is {word_count} words per minute\n You made {len(incorrect_words)} mistakes")
        button_start.configure(state="normal")
        reset_button()
        button_reset.configure(state="disabled")

def check_words():
    global word_count
    word_count=sum(1 for word in typed_words if word in LISTS_OF_WORDS)
    return word_count

def shuffle_button():
    global LISTS_OF_WORDS
    LISTS_OF_WORDS=random.sample(dictionary.word_list, len(dictionary.word_list))
    update_displayed_text()
    
#------------------------------ LIVE WORD CHECK---------------------------#

def update_typed_words(event):
    global typed_words, timer_started
    if not timer_started:
        timer_started=True
        count_down(TEST_SEC)
    typed_words=input_field.get().split()
    update_displayed_text()

def update_displayed_text():
    global incorrect_words
    incorrect_words=[]
    text_display.config(state="normal")
    text_display.delete("1.0", "end")  # Clear previous text
    words = LISTS_OF_WORDS  # Get the words to type
    for i, word in enumerate(words):
        if i < len(typed_words):
            if typed_words[i] == word:
                text_display.insert("end", word + " ", "correct")  # Green
            else:
                text_display.insert("end", word + " ", "incorrect")
                if typed_words[i] not in incorrect_words:
                    incorrect_words.append(typed_words[i]) # Red
        else:
            text_display.insert("end", word + " ")
    text_display.config(state="disabled")  # Make read-only
    
#----------------------------- MESSAGE BOX------------------------------- #

def show_custom_message(message):
    top = Toplevel(window)
    top.title("Finished")
    top.geometry("500x350")
    window_width = window.winfo_width()
    window_height = window.winfo_height()
    # screen_width = window.winfo_screenwidth()
    # screen_height = window.winfo_screenheight()
    position_top = (window_height // 2) - (250 // 2)  # Vertical position
    position_left = (window_width // 2) - (500 // 2)  # Horizontal position
    
    top.geometry(f"500x250+{position_left}+{position_top}")
    top.config(bg=COLOR3)
    message_label = Label(top,
                          text=message,
                          font=(FONT_NAME, 16),
                          padx=10,
                          pady=10,
                          bg=COLOR3,
                          fg=COLOR4)
    message_label.pack(expand=True)

    button_close = Button(top,
                          text="Close",
                          command=top.destroy,
                          font=(FONT_NAME, 16, "bold"),
                          bg=COLOR4,
                          fg=COLOR3,
                          borderless=1,
                          activebackground=COLOR2,
                          activeforeground=COLOR3,
                          highlightbackground=COLOR4,
                          relief="flat",
                          focuscolor=COLOR2)
    button_close.pack(pady=20)
    top.grab_set()

# ---------------------------- UI SETUP --------------------------------- #

window=Tk()
window.title(TITLE)
window.minsize(700,700)
window.config(padx=150,pady=10, bg=COLOR1)

title_label=Label(text="Check the speed of your typing",
                  font=(FONT_NAME, 30),
                  fg=COLOR3, bg=COLOR1)
title_label.grid(column=1,row=0)

canvas=Canvas(width=200, height=200, bg=COLOR1, highlightthickness=0)
image=PhotoImage(file="typewriter.png")
canvas.create_image(100, 100, image=image)
canvas.create_rectangle(50, 115, 150, 145, fill="#333333", outline="#333333")
timer_text=canvas.create_text(100,130, text="01:00", fill="white",font=(FONT_NAME, 25, "bold"))
canvas.grid(column=1,row=1)

button_start=Button(text="Start",
                    font=(FONT_NAME, 20),
                    width=150,
                    height=30,
                    background=COLOR4,
                    foreground=COLOR3,
                    borderless=1,
                    activebackground=COLOR3,
                    activeforeground=COLOR4,
                    highlightbackground=COLOR1,
                    relief="flat",
                    focuscolor=COLOR2,
                    state="normal",
                    command=start_timer)
button_start.grid(column=0, row=2)

button_reset=Button(text="Reset",
                    font=(FONT_NAME, 20),
                    width=150,
                    height=30,
                    background=COLOR4,
                    foreground=COLOR3,
                    borderless=1,
                    activebackground=COLOR3,
                    activeforeground=COLOR4,
                    highlightbackground=COLOR1,
                    relief="flat",
                    focuscolor=COLOR2,
                    state="disabled",
                    command=reset_button)
button_reset.grid(column=2, row=2)

text_display = Text(window, width=70,
                    height=8,
                    font=(FONT_NAME, 16),
                    bg=COLOR2,
                    wrap="word")
text_display.grid(column=0,
                  row=3,
                  columnspan=3,
                  pady=20)
text_display.config(state="disabled")  # Read-only
text_display.tag_configure("correct", foreground=COLOR_CORRECT)  # Green for correct words
text_display.tag_configure("incorrect", foreground=COLOR_INCORRECT)  # Red for incorrect words

input_field = Entry(width=70,
                    highlightthickness=1,
                    font=(FONT_NAME, 16),
                    state=DISABLED)
input_field.grid(column=0, row=4, columnspan=3, pady=20)
input_field.bind("<KeyRelease>", update_typed_words)

button_shuffle=Button(text="Shuffle words",
                      font=(FONT_NAME, 30),
                      width=250,
                      height=40,
                      background=COLOR4,
                      foreground=COLOR3,
                      borderless=1,
                      activebackground=COLOR3,
                      activeforeground=COLOR4,
                      highlightbackground=COLOR1,
                      relief="flat",
                      focuscolor=COLOR2,
                      state="disabled",
                      command=shuffle_button)
button_shuffle.grid(column=1, row=5, pady=20)

update_displayed_text()
window.mainloop()