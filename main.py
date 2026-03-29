import authenticateFace as af
import common.emojiGenerator as eg
from common.emojiMap import emoji_map
from common.insult import get_insult
from modules.frameCapture import runner

# Factor 1: Authenticate the user by face recognition
recognized = af.runner()
if recognized is None:
    print("Face not recognized. Authentication failed.")
    exit(1)

print(f"Welcome, {recognized}!")

# Factor 2: Emoji challenge
random_emoji = eg.generate_random_emoji()
print(f"Please make this face to authenticate yourself: {random_emoji}")

detected_emotion = runner()

if detected_emotion is not None and emoji_map.get(detected_emotion) == random_emoji:
    print("Fully authenticated - Thank you!")
else:
    print(get_insult())
