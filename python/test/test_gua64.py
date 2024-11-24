import sys

sys.path.append('..')

import pytest
from gua64 import Gua64Native  # Assuming your Gua64Native class is in gua64.py


def test_encode_decode_empty():
    assert Gua64Native.decode(Gua64Native.encode(b'')) == b''


def test_encode_decode_single_byte():
    assert Gua64Native.decode(Gua64Native.encode(b'A')) == b'A'


def test_encode_decode_multiple_bytes():
    test_data = [
        b'Hello, world!',
        b'This is a longer string to test the encoding and decoding.',
        b'\x00\x01\x02\x03\x04\x05\x06\x07\x08\x09',  # Test with null bytes
        b'\xff\xfe\xfd\xfc\xfb\xfa\xf9\xf8\xf7\xf6'  # Test with high-value bytes
    ]
    for data in test_data:
        assert Gua64Native.decode(Gua64Native.encode(data)) == data


def test_encode_decode_padding():
    assert Gua64Native.decode(Gua64Native.encode(b'He')) == b'He'
    assert Gua64Native.decode(Gua64Native.encode(b'H')) == b'H'


def test_decode_invalid_input():
    with pytest.raises(TypeError):
        Gua64Native.decode(123)  # Invalid input type
    with pytest.raises(ValueError):
        Gua64Native.decode(
            "Invalid character outside range")  # Character outside range
    with pytest.raises(ValueError):
        Gua64Native.decode("This is an invalid length string")  # wrong length


def test_encode_invalid_input():
    with pytest.raises(TypeError):
        Gua64Native.encode(123)  # Invalid input type


@pytest.mark.parametrize("length", range(0, 30, 3))  #Test multiples of 3
def test_encode_decode_multiples_of_three(length):
    test_str = b'a' * length
    assert Gua64Native.decode(Gua64Native.encode(test_str)) == test_str


@pytest.mark.parametrize("length", range(1, 30,
                                         3))  #Test one less than multiple of 3
def test_encode_decode_one_less(length):
    test_str = b'a' * length
    assert Gua64Native.decode(Gua64Native.encode(test_str)) == test_str


@pytest.mark.parametrize("length", range(2, 30,
                                         3))  #Test two less than multiple of 3
def test_encode_decode_two_less(length):
    test_str = b'a' * length
    assert Gua64Native.decode(Gua64Native.encode(test_str)) == test_str
