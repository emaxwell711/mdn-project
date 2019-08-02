def AlphaBits(bits):
    alpha = 'abcdefghijklmnop'
    if type(bits) !=str:
        raise TypeError('bits must be str')
    if len(bits) != 16:
        raise ValueError('len of bits must be 16')
    if '1' in bits:
        num = bits.index('1')
        letter = alpha[num]
        return letter

        
test1 = '0101011101010101'
test2 = '0000010000100000'
test3 = '0000'

letter = AlphaBits(test2)
print(letter)
        
    
        
        
    
