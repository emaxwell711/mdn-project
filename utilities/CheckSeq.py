def CheckOnes(bits1, bits2):
    if '1' not in bits1:
        raise ValueError('bits1 does not contain a 1')
    if '1' not in bits2:
        raise ValueError('bits2 does not contain a 1')
    for i in range(len(bits1)):
        if bits1[i] == bits2[i] and bits1[i] == 1 and bits2[i] == 1:
            return i

        
        
