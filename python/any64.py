class CustomBase64Native:
    def __init__(self, char_map, padding_char='='):
        self.char_map = char_map
        self.padding_char = padding_char
        self.reverse_map = {char: i
                            for i, char in enumerate(char_map)
                            }  # Create reverse map for efficiency

    def encode(self, b):
        output = []
        padding = 0

        byte_len = len(b)
        if byte_len % 3 == 1:
            padding = 2
            b += b'\x00\x00'
        elif byte_len % 3 == 2:
            padding = 1
            b += b'\x00'

        for i in range(0, len(b), 3):
            block = b[i:i + 3]
            code = (block[0] << 16) + (block[1] << 8) + block[2]

            output.append(self.char_map[(code >> 18) & 0x3F])
            output.append(self.char_map[(code >> 12) & 0x3F])
            output.append(self.char_map[(code >> 6) & 0x3F])
            output.append(self.char_map[code & 0x3F])

        if padding > 0:
            output[-padding:] = [self.padding_char] * padding

        # print(output)
        return ''.join(output)

    def decode(self, s):

        if not isinstance(s, str):
            raise TypeError("Input must be a string")

        output = []

        #Efficiently handle invalid characters
        for char in s:
            if char == self.padding_char:
                output.append(None)  #Represents padding
            elif char in self.reverse_map:
                output.append(self.reverse_map[char])
            else:
                raise ValueError(
                    f"Invalid character '{char}' encountered during decoding.")

        if len(output) % 4 != 0:
            raise ValueError("Invalid Gua64 string length")

        out_bytes = bytearray()
        for i in range(0, len(output), 4):
            if any(x is None for x in output[i:i + 4]):
                #Handle padding
                block = sum(x << (18 - 6 * j)
                            for j, x in enumerate(output[i:i + 4])
                            if x is not None)
                num_bytes = 3 - output[i:i + 4].count(None)
                for j in range(num_bytes):
                    out_bytes.append((block >> (16 - 8 * j)) & 0xFF)
            else:
                block = (output[i] << 18) + (output[i + 1] << 12) + (
                    output[i + 2] << 6) + output[i + 3]
                out_bytes.append((block >> 16) & 0xFF)
                out_bytes.append((block >> 8) & 0xFF)
                out_bytes.append(block & 0xFF)

        return bytes(out_bytes)


# Example usage
if __name__ == "__main__":
    custom_map = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
    padding_character = '='

    base64_instance = CustomBase64Native(custom_map, padding_character)

    original_data = b"Hello, World! This is a longer string to test more thoroughly."
    encoded_data = base64_instance.encode(original_data)
    print("Encoded:", encoded_data)

    decoded_data = base64_instance.decode(encoded_data)
    print("Decoded:", decoded_data)

    assert original_data == decoded_data
    print("Test Passed!")
