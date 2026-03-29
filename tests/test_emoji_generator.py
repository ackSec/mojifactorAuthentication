from common.emojiMap import emoji_map
from common.emojiGenerator import generate_random_emoji


def test_generate_random_emoji_returns_valid_emoji():
    emoji = generate_random_emoji()
    assert emoji in emoji_map.values()


def test_generate_random_emoji_returns_string():
    emoji = generate_random_emoji()
    assert isinstance(emoji, str)


def test_emoji_map_has_expected_emotions():
    expected = {'HAPPY', 'SAD', 'ANGRY', 'CONFUSED', 'DISGUSTED', 'SURPRISED', 'CALM', 'FEAR'}
    assert set(emoji_map.keys()) == expected


def test_emoji_map_values_are_unique():
    values = list(emoji_map.values())
    assert len(values) == len(set(values))
