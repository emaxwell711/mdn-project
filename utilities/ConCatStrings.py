def JoinStrings(bit_strings):
    pieces = bit_strings.split(' ')
    if len(pieces[0]) != 5 or len(pieces[1]) != 4 or len(pieces[2]) != 23:
        raise ValueError('Length of strings must be 5, 4, and 23, respectively')
    else:
        string = ''.join(pieces)
        return string
    
test = '01100 0000 00001100101010101111000'
final = JoinStrings(test)
print(final)
    
