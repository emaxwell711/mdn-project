import random
from random import choice

def generate_random_flags(field_length):
    print(''.join(random.choice("01") for i in range(field_length))


### AS ANOTHER OPTION ###

def generate_random_flags(field_length):
        random_flags = [] 
        for i in range(field_length):
            rand = str(random.randint(0,1))
            random_flags.append(rand)
            print(''.join(random_flags))


