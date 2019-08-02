def SplitBits(bits):
    if len(bits) == 32:
        five = bits[:5]
        four = bits[5:9]
        rest = bits[9:]
        return five , four , rest
    else:
        raise ValueError('length of bits must be 32 characters')

sample = '01010101010010101010101011010101'

five , four , rest = SplitBits(sample)
print(five , four, rest)


