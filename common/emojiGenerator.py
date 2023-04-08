import random
from common.emojiMap import emoji_map

def generate_random_emoji():
    return random.choice(list(emoji_map.values()))

def get_random_emoji():
    return generate_random_emoji()


