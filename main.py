from tkinter import *
from tkinter import messagebox
from tkinter.ttk import *
from sample import sample_texts
import random
import time

# Global variables
start_time = 0
time_left = 60
current_text = ""
correct_chars = 0
total_chars = 0
timer_running = False


# Function to start the typing test
def start_test():
    global start_time, time_left, correct_chars, total_chars, timer_running
    start_time = time.time()
    time_left = 60
    correct_chars = 0
    total_chars = 0
    timer_running = True

    text_box.config(state=NORMAL)
    text_box.delete("1.0", END)
    text_box.focus()

    next_sentence()
    update_timer()


# Timer countdown
def update_timer():
    global time_left, timer_running
    if time_left > 0 and timer_running:
        timer_label.config(text=f"Time Left: {time_left}s")
        time_left -= 1
        root.after(1000, update_timer)
    else:
        timer_running = False
        text_box.config(state=DISABLED)
        show_result()


# Load new sentence
def next_sentence():
    global current_text
    current_text = random.choice(sample_texts)
    sentence_label.config(text=current_text)
    text_box.delete("1.0", END)


# Track text in real-time
def on_text_change(event):
    global correct_chars, total_chars

    typed = text_box.get("1.0", END).strip()
    target = current_text[:len(typed)]

    total_chars += 1
    if typed == current_text:
        correct_chars += len(typed)
        next_sentence()


# Show final result in a popup
def show_result():
    time_taken = 60
    wpm = (correct_chars / 5) / (time_taken / 60)
    accuracy = (correct_chars / total_chars) * 100 if total_chars > 0 else 0

    result = Toplevel(root)
    result.title("Typing Results")
    result.geometry("300x150")
    result.resizable(False, False)

    # Center the popup window manually
    result.update_idletasks()
    w = result.winfo_width()
    h = result.winfo_height()
    x = (result.winfo_screenwidth() // 2) - (w // 2)
    y = (result.winfo_screenheight() // 2) - (h // 2)
    result.geometry(f"{w}x{h}+{x}+{y}")

    Label(result, text=f"Your WPM: {int(wpm)}", font=("Helvetica", 12)).pack(pady=10)
    Label(result, text=f"Accuracy: {accuracy:.2f}%", font=("Helvetica", 12)).pack(pady=5)
    Button(result, text="Close", command=result.destroy).pack(pady=10)


# UI Setup
root = Tk()
root.title("TypeRush")
root.geometry("800x500")
root.configure(bg="#f0f4f8")

style = Style()
style.configure("TButton", font=("Helvetica", 12))
style.configure("TLabel", font=("Helvetica", 12))

mainframe = Frame(root, padding=20)
mainframe.pack(expand=True)

title = Label(mainframe, text="TypeRush: Are you a Typing Wizard!", font=("Helvetica", 16, "bold"))
title.pack(pady=10)

sentence_label = Label(mainframe, text="Click Start to Begin!", wraplength=700, justify="center",
                       font=("Helvetica", 12), background="#f0f4f8")
sentence_label.pack(pady=10)

text_box = Text(mainframe, width=80, height=10, font=("Courier", 12), wrap=WORD)
text_box.pack(pady=10)
text_box.bind("<KeyRelease>", on_text_change)
text_box.config(state=DISABLED)

timer_label = Label(mainframe, text="Time Left: 60s", font=("Helvetica", 12, "bold"))
timer_label.pack(pady=10)

start_btn = Button(mainframe, text="Start Test", command=start_test)
start_btn.pack()

root.mainloop()
