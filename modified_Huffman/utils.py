import json


def read_text(path):
    with open(path, "r", encoding="utf-8", newline="") as f:
        return f.read()


def write_text(path, text):
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(text)


def bits_to_bytes(bitstream):
    # pad with zeros 3shan length yb2aa a multiple of 8
    padded = bitstream + "0" * (-len(bitstream) % 8)
    # every 8 bits ------->> one byte
    return bytes(int(padded[i:i + 8], 2) for i in range(0, len(padded), 8))


def bytes_to_bits(data, bit_length):
    # every byte ->>>>>>>>>> 8 bits we eetaa3 elba2y
    bits = "".join(format(b, "08b") for b in data)
    return bits[:bit_length]


def save_compressed(path, bitstream, final_codes):
    """final_codes: symbol -> code"""
    header = json.dumps({"codes": final_codes, "bit_length": len(bitstream)})

    with open(path, "wb") as f:
        f.write(header.encode("utf-8") + b"\n")   # line 1: header (text)
        f.write(bits_to_bytes(bitstream))         # rest: real bits (binary)


def load_compressed(path):
    with open(path, "rb") as f:
        header = json.loads(f.readline())         # read line 1
        data = f.read()                           # rest = compressed bytes

    codes = {code: symbol for symbol, code in header["codes"].items()}
    bitstream = bytes_to_bits(data, header["bit_length"])
    return bitstream, codes