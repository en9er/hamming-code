import random

from hamming import *


word = "hello world"
msgs = hamming_encode(word)

for msg in msgs:
    bit_ind = random.randint(0, CHUNK_LEN - 1)
    msg = replace_bit(msg, bit_ind)
    hamming_decode(msg)

