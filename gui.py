import tkinter as tk
from tkinter import messagebox
import authenticateFace as af
import common.emojiGenerator as eg
from common.emojiMap import emoji_map
from common.insult import get_insult
from modules.frameCapture import runner


random_emoji = None


def run_authenticate():
    try:
        result = af.runner()
    except RuntimeError as e:
        authenticate_status_label.config(text=str(e))
        return

    if result:
        authenticate_status_label.config(text=f"Welcome, {result}!")
        generate_emoji_button.config(state="normal")
    else:
        authenticate_status_label.config(text="Face not recognized. Please try again.")


def run_generate_emoji():
    global random_emoji
    random_emoji = eg.generate_random_emoji()
    emoji_label.config(text=f"Please make this face to authenticate yourself: {random_emoji}")
    detect_emotion_button.config(state="normal")


def update_countdown_label(countdown):
    if countdown > 0:
        status_label.config(text=f"Time remaining: {countdown}s")
        window.after(1000, update_countdown_label, countdown - 1)
    else:
        run_detect_emotion_after_countdown()


def run_detect_emotion():
    countdown_duration = 5
    update_countdown_label(countdown_duration)


def run_detect_emotion_after_countdown():
    try:
        detected_emotion = runner()
    except RuntimeError as e:
        messagebox.showerror("Error", str(e))
        return

    if detected_emotion is None:
        messagebox.showerror("Error", "No face detected, please try again")
        return

    corresponding_emoji = emoji_map.get(detected_emotion, "❓")
    detected_emotion_label.config(text=f"Detected emotion: {detected_emotion} ({corresponding_emoji})")

    if corresponding_emoji == random_emoji:
        status_label.config(text="Fully authenticated - Thank you!")
    else:
        status_label.config(text=get_insult())


# Create the main window
window = tk.Tk()
window.title("Mojifactor Authentication")
window.geometry("500x400")
window.resizable(False, False)

window.eval('tk::PlaceWindow %s center' % window.winfo_pathname(window.winfo_id()))

window.tk_setPalette(
    background='#2c2c2c', foreground='white',
    activeBackground='#0078d7', activeForeground='white'
)

# Create the frames
authenticate_frame = tk.Frame(window)
generate_emoji_frame = tk.Frame(window)
detect_emotion_frame = tk.Frame(window)

# Create the widgets
authenticate_button = tk.Button(
    authenticate_frame, text="Authenticate", command=run_authenticate,
    height=2, width=15, font=("Helvetica", 14), bd=0, highlightthickness=0
)
authenticate_status_label = tk.Label(authenticate_frame, text="", font=("Helvetica", 12))

generate_emoji_button = tk.Button(
    generate_emoji_frame, text="Generate Emoji", command=run_generate_emoji,
    height=2, width=15, font=("Helvetica", 14), bd=0, highlightthickness=0, state="disabled"
)
emoji_label = tk.Label(generate_emoji_frame, text="", font=("Helvetica", 12))

detect_emotion_button = tk.Button(
    detect_emotion_frame, text="Detect Emotion", command=run_detect_emotion,
    height=2, width=15, font=("Helvetica", 14), bd=0, highlightthickness=0, state="disabled"
)
detected_emotion_label = tk.Label(detect_emotion_frame, text="", font=("Helvetica", 12))
status_label = tk.Label(detect_emotion_frame, text="", font=("Helvetica", 12))

# Pack widgets into frames
authenticate_button.pack()
authenticate_status_label.pack()
generate_emoji_button.pack()
emoji_label.pack()
detect_emotion_button.pack()
detected_emotion_label.pack()
status_label.pack()

# Pack frames into window
authenticate_frame.pack(pady=5)
generate_emoji_frame.pack(pady=5)
detect_emotion_frame.pack(pady=5)

window.mainloop()
