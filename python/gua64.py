import base64

class Gua64Wrapper:
    base64_chars = [
        'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H',
        'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
        'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X',
        'Y', 'Z', 'a', 'b', 'c', 'd', 'e', 'f',
        'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n',
        'o', 'p', 'q', 'r', 's', 't', 'u', 'v',
        'w', 'x', 'y', 'z', '0', '1', '2', '3',
        '4', '5', '6', '7', '8', '9', '+', '/'
    ]
    gua_begin = 19904

    @classmethod
    def encode(cls, s):
        s = base64.b64encode(s)
        s = s.decode('ascii')

        for i in range(64):
            s = s.replace(cls.base64_chars[i], chr(19904 + i))

        s = s.replace('=', '☯')

        return s
    
    @classmethod
    def decode(cls, s):
        for i in range(64):
            s = s.replace(chr(cls.gua_begin + i), cls.base64_chars[i])
        
        s = s.replace('☯', '=')

        base64_bytes = s.encode('ascii')
        s = base64.b64decode(base64_bytes)

        return s
    

class Gua64Native:

    gua_begin = 19904

    @classmethod
    def encode(cls, b):
        output = []
        padding = 0
        
        # Handle byte length to determine padding
        byte_len = len(b)
        if byte_len % 3 == 1:
            padding = 2  # Zero pad with two "0" bytes to make it 3
            b += b'\x00\x00'
        elif byte_len % 3 == 2:
            padding = 1  # Zero pad with one "0" byte to make it 3
            b += b'\x00'

        # Process 3 bytes at a time
        for i in range(0, len(b), 3):
            # Get 3 bytes
            block = b[i:i + 3]
            code = (block[0] << 16) + (block[1] << 8) + block[2]  # Combine to 24 bits

            # Get 4 indices for the custom base64
            output.append(chr(cls.gua_begin + ((code >> 18) & 0x3F)))  # First 6 bits
            output.append(chr(cls.gua_begin + ((code >> 12) & 0x3F)))  # Second 6 bits
            output.append(chr(cls.gua_begin + ((code >> 6) & 0x3F)))   # Third 6 bits
            output.append(chr(cls.gua_begin + (code & 0x3F)))          # Last 6 bits
            
        # Modify last `padding` characters to '☯' if necessary
        if padding > 0:
            for _ in range(padding):
                output[-1] = '☯'
        
        return ''.join(output)

    @classmethod
    def decode(cls, s):
        output = bytearray()
        padding = 0

        # Replace customized characters back to base64 indices
        for i in range(len(s)):
            if s[i] == '☯':
                padding += 1
            else:
                idx = ord(s[i]) - cls.gua_begin
                output.append(idx)

        out_bytes = bytearray()
        # Process indices to get bytes
        for i in range(0, len(output), 4):
            if i + 3 < len(output):
                # Create 24 bits from 4 base64 indices
                block = (output[i] << 18) + (output[i + 1] << 12) + (output[i + 2] << 6) + output[i + 3] 
                out_bytes.append((block >> 16) & 0xFF)
                out_bytes.append((block >> 8) & 0xFF)
                out_bytes.append(block & 0xFF)

        # Adjust for padding
        if padding > 0:
            out_bytes = out_bytes[:-padding]

        return bytes(out_bytes)
