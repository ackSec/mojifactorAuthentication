import tkinter as tk
import authenticateFace as af
import common.emojiGenerator as eg
from modules.frameCapture import runner
from urllib.request import urlopen


def get_insult():
    url = "https://evilinsult.com/generate_insult.php"
    try:
        response = urlopen(url)
        return response.read().decode()
    except Exception as e:
        return "An error occurred while fetching insult: " + str(e)


def run_authenticate():
    af.runner()
    generate_emoji_button.config(state="normal")


def run_generate_emoji():
    global random_emoji
    random_emoji = eg.generate_random_emoji()
    emoji_label.config(text=f"Please make this face to authenticate yourself: {random_emoji}")
    detect_emotion_button.config(state="normal")


def run_detect_emotion():
    detected_emotion = runner()
    if eg.emoji_map[detected_emotion] == random_emoji:
        status_label.config(text="Fully authenticated - Thank you!")
    else:
        insult = get_insult()
        status_label.config(text=insult)

# Create the main window
window = tk.Tk()
window.title("Mojifactor Authentication")
window.geometry("500x300")
window.resizable(False, False)

# Create the widgets
authenticate_button = tk.Button(window, text="Authenticate", command=run_authenticate)
generate_emoji_button = tk.Button(window, text="Generate Emoji", command=run_generate_emoji, state="disabled")
detect_emotion_button = tk.Button(window, text="Detect Emotion", command=run_detect_emotion, state="disabled")

emoji_label = tk.Label(window, text="")
status_label = tk.Label(window, text="")

# Add the widgets to the window
authenticate_button.pack(pady=10)
generate_emoji_button.pack(pady=10)
detect_emotion_button.pack(pady=10)
emoji_label.pack(pady=10)
status_label.pack(pady=10)

# Run the window
window.mainloop()
