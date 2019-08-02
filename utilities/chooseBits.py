import random
def ChooseBits(bits):
    if bits.find('1') != -1:
        seq = bits[1:]
        new =  '1' + seq.replace('1' , '0')
        new1 = list(new)
        random.shuffle(new1)
        finalseq = ''.join(new1)
        return finalseq
    else:
        raise ValueError('bits must contain a 1')
        
seq1 = '0101010000000'
seq2 = '00000'
seq3 = '011111111'

seq = ChooseBits(seq1)
print(seq)
