from .utils import load_compressed, write_text

def deCompress(bitStream, finalCodes):
    s = temp = ''

    for bit in bitStream:
        temp += bit
        letter = finalCodes.get(temp, False)
        if(letter):
            s += letter
            temp = ''

    return s;

def decompress_file(in_path, out_path):
    bitstream, codes = load_compressed(in_path)
    write_text(out_path, deCompress(bitstream, codes))