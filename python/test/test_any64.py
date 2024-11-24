# pylint: disable=wrong-import-position
import sys
import pytest
import string
import random

sys.path.append('..')

from any64 import CustomBase64Native  # pylint: disable=import-error

# Any English letters, digits, 汉字, emoji, and special characters can be used as the character pool.
# English letters (uppercase and lowercase)
english_letters = (
    string.ascii_uppercase +  # A-Z
    string.ascii_lowercase  # a-z
)

# Digits (0-9)
digits = string.digits  # 0-9

# Chinese characters (汉字)
# This will include common Chinese characters. You may adjust the range as needed.
chinese_characters = ''.join(
    chr(i) for i in range(0x4E00, 0x9FFF))  # CJK Unified Ideographs

# Emojis
emoji_characters = ''.join(
    chr(i) for i in range(0x1F600, 0x1F64F))  # Emoticons (basic emojis range)
emoji_characters += ''.join(
    chr(i)
    for i in range(0x1F300, 0x1F5FF))  # Miscellaneous Symbols and Pictographs

# Combine all the parts into CHAR_POOL
CHAR_POOL = english_letters + digits + chinese_characters + emoji_characters

# random.sample(CHAR_POOL, len(CHAR_POOL))
CHAR_MAP_LST = [random.sample(CHAR_POOL, 64) for _ in range(10)]

PADDING_CHAR_LST = ['=', '!', ' ']

TEXT_LST = [
    b"",
    b"Hello, world!",
    b"This is a longer test string.",
    b"1234567890",
    b"~!@#$%^&*()_+=-`",
    b"This string contains some unusual characters: \x00\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0A\x0B\x0C\x0D\x0E\x0F",
    bytes([random.randint(0, 255) for _ in range(100)])  # Random bytes
]


class TestCustomBase64Native:

    @pytest.mark.parametrize("char_map, padding_char, text",
                             [(char_map, padding_char, text)
                              for char_map in CHAR_MAP_LST
                              for padding_char in PADDING_CHAR_LST
                              for text in TEXT_LST])
    def test_consitency(self, char_map, padding_char, text):
        try:
            cb64 = CustomBase64Native(char_map, padding_char)
            encoded = cb64.encode(text)
            decoded = cb64.decode(encoded)
            assert text == decoded
        except Exception as e:
            pytest.fail(
                f"Test failed with char_map={char_map}, padding_char={padding_char}, text={text}. Exception: {e}"
            )
