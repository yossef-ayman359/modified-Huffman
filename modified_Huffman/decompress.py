# final_codes {'11'':'a', ...}, bitstream 11100110...

def deCompress(bitStream, finalCodes):
    s = temp = ''

    for bit in bitStream:
        temp += bit
        letter = finalCodes.get(temp, False)
        if(letter):
            s += letter
            temp = ''

    return s;