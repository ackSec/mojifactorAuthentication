# This displays random emojis to use for the authentication process
# Does NOT play well with main.py, not sure why. Think it conflicts with opencv
#

import tkinter as tk
import random
from common.emojiMap import emoji_map

class EmojiWindow:
    def __init__(self):
        # Create a new window
        self.root = tk.Tk()
        self.root.title("Random Emoji")
        
        # Create a label to display the emoji
        self.label = tk.Label(self.root, text="", font=("Arial", 100))
        self.label.pack()
        
        # Start the loop to display a new emoji every 3 seconds
        self.display_new_emoji()
        
        # Bind the 'q' key to close the window
        self.root.bind('q', self.close_window)
        
        # Start the main loop
        self.root.mainloop()
        
    def display_new_emoji(self):
        # Get four random emojis from the EMOJI_MAP
        emojis = random.sample(list(emoji_map.values()), 4)

        # Set the label text to the four selected emojis, separated by spaces
        self.label.config(text=" ".join(emojis))

        # Call the display_new_emoji() function again in 3 seconds
        self.root.after(3000, self.display_new_emoji)
        
    def close_window(self, event):
        # Close the window when the 'q' key is pressed
        self.root.destroy()

def show_random_emoji():
    EmojiWindow()

if __name__ == "__main__":
    show_random_emoji()
