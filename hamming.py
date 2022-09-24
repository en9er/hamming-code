# TODO: implement choose of decode/encode block sizes
CHUNK_LEN = 16
CONTROL_BIT_COUNT = 5

# TODO: generate masks through the code
CB_MASKS = [
    0b101010101010101010101,
    0b001100110011001100110,
    0b110000111100001111000,
    0b000000111111110000000,
    0b111111000000000000000
]


def str_to_bin_chunks(string: str):
    bits = bytearray(string.encode('ascii'))
    return list([list(bits[x:x+2]) for x in range(0, len(bits), 2)])


def bin_chunk_to_str(chunk):
    right_part = chunk & 0b0000000011111111
    left_part = chunk & ((pow(2, chunk.bit_length()) - 1) & 0b1111111100000000)
    return chr(left_part >> 8) + (chr(right_part) if right_part else "")


# Function to check if x is power of 2
def is_power_of_two(num):
    return num and (not (num & (num - 1)))


def insert_control_bits(num):
    res = 0
    mask = pow(2, num.bit_length())
    pos = CHUNK_LEN + CONTROL_BIT_COUNT
    while pos:
        if not is_power_of_two(pos):
            r = (num & mask)
            res = res | r
            mask >>= 1
        else:
            res <<= 1
        pos -= 1
    return res


def parity(num: int):
    return bin(num).count("1") % 2


def calculate_control_bits(chunk: int):
    cb_pos = 0
    while cb_pos < CONTROL_BIT_COUNT:
        set = parity(chunk & CB_MASKS[cb_pos])
        if set:
            chunk = chunk | pow(2, pow(2, cb_pos) - 1)
        cb_pos += 1
    return chunk


def hamming_encode(msg: str):
    bits = str_to_bin_chunks(msg)
    print(bits)
    full_bits_list = []
    for i in range(len(bits)):
        merge_num = (0b0000000000000000 | (0b0000000011111111 & bits[i][0])) << 8
        if len(bits[i]) > 1:
            merge_num = merge_num | (0b0000000011111111 & bits[i][1])
        full_bits = insert_control_bits(merge_num)
        full_bits_list.append(calculate_control_bits(full_bits))
    return full_bits_list


def replace_bit(chunk, ind):
    chunk = chunk ^ (1 << ind)
    return chunk


def reset_control_bits(msg):
    bits = CONTROL_BIT_COUNT
    while bits:
        msg = msg & (pow(2, pow(2, bits - 1) - 1) ^ 0b111111111111111111111)
        bits -= 1
    return msg


def get_control_bits_diff(rec, calc):
    bits = CONTROL_BIT_COUNT
    res = 0
    while bits:
        curr_bit_mask = pow(2, pow(2, bits - 1) - 1)
        rec_bit = rec & curr_bit_mask
        calc_bit = calc & curr_bit_mask
        if rec_bit != calc_bit:
            res += pow(2, bits - 1)
        bits -= 1
    return res


def remove_control_bits(num):
    res = 0
    pos = num.bit_length()
    mask = pow(2, pos - 1)
    while pos:
        if not is_power_of_two(pos):
            res = res | (num & mask)
        else:
            res >>= 1
        mask >>= 1
        pos -= 1
    return res


def hamming_decode(msg):
    res_msg = reset_control_bits(msg)
    calculated_msg = calculate_control_bits(res_msg)
    err_pos = get_control_bits_diff(msg, calculated_msg)
    if err_pos != 0:
        calculated_msg = replace_bit(calculated_msg, err_pos - 1)
    clear_msg = remove_control_bits(calculated_msg)
    print(bin_chunk_to_str(clear_msg))
