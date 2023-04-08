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

# Authenticate the user
af.runner()

# Generate a random emoji
random_emoji = eg.generate_random_emoji()
print(f"Please make this face to authenticate yourself: {random_emoji}")

# Detect the user's emotion
detected_emotion = runner()

# Check if the generated emoji matches the detected emotion
if eg.emoji_map[detected_emotion] == random_emoji:
    print("Fully authenticated - Thank you!")
else:
    insult = get_insult()
    print(insult)
