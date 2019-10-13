from builtins import hex

_xormap = {('0', '1'): '1', ('1', '0'): '1', ('1', '1'): '0', ('0', '0'): '0'}

# initial permutation IP
__ip = [57, 49, 41, 33, 25, 17, 9, 1,
        59, 51, 43, 35, 27, 19, 11, 3,
        61, 53, 45, 37, 29, 21, 13, 5,
        63, 55, 47, 39, 31, 23, 15, 7,
        56, 48, 40, 32, 24, 16, 8, 0,
        58, 50, 42, 34, 26, 18, 10, 2,
        60, 52, 44, 36, 28, 20, 12, 4,
        62, 54, 46, 38, 30, 22, 14, 6
        ]

# Expansion table for turning 32 bit blocks into 48 bits
__expansion_table = [
    31, 0, 1, 2, 3, 4,
    3, 4, 5, 6, 7, 8,
    7, 8, 9, 10, 11, 12,
    11, 12, 13, 14, 15, 16,
    15, 16, 17, 18, 19, 20,
    19, 20, 21, 22, 23, 24,
    23, 24, 25, 26, 27, 28,
    27, 28, 29, 30, 31, 0
]

# The (in)famous S-boxes
__sbox = [
    # S1
    [14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7,
     0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8,
     4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0,
     15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13],

    # S2
    [15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10,
     3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5,
     0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15,
     13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9],

    # S3
    [10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8,
     13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1,
     13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7,
     1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12],

    # S4
    [7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15,
     13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9,
     10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4,
     3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14],

    # S5
    [2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9,
     14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6,
     4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14,
     11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3],

    # S6
    [12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11,
     10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8,
     9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6,
     4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13],

    # S7
    [4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1,
     13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6,
     1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2,
     6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12],

    # S8
    [13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7,
     1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2,
     7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8,
     2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11],
]

# 32-bit permutation function P used on the output of the S-boxes
__p = [
    15, 6, 19, 20, 28, 11,
    27, 16, 0, 14, 22, 25,
    4, 17, 30, 9, 1, 7,
    23, 13, 31, 26, 2, 8,
    18, 12, 29, 5, 21, 10,
    3, 24]

hex2bin_map = {
    "0": "0000",
    "1": "0001",
    "2": "0010",
    "3": "0011",
    "4": "0100",
    "5": "0101",
    "6": "0110",
    "7": "0111",
    "8": "1000",
    "9": "1001",
    "A": "1010",
    "B": "1011",
    "C": "1100",
    "D": "1101",
    "E": "1110",
    "F": "1111",
}

__pc1 = [56, 48, 40, 32, 24, 16, 8,
         0, 57, 49, 41, 33, 25, 17,
         9, 1, 58, 50, 42, 34, 26,
         18, 10, 2, 59, 51, 43, 35,
         62, 54, 46, 38, 30, 22, 14,
         6, 61, 53, 45, 37, 29, 21,
         13, 5, 60, 52, 44, 36, 28,
         20, 12, 4, 27, 19, 11, 3
         ]
__pc2 = [
    13, 16, 10, 23, 0, 4,
    2, 27, 14, 5, 20, 9,
    22, 18, 11, 3, 25, 7,
    15, 6, 26, 19, 12, 1,
    40, 51, 30, 36, 46, 54,
    29, 39, 50, 44, 32, 47,
    43, 48, 38, 55, 33, 52,
    45, 41, 49, 35, 28, 31
]

__left_rotations = [
    1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1
]

# final permutation IP^-1
__fp = [
    39, 7, 47, 15, 55, 23, 63, 31,
    38, 6, 46, 14, 54, 22, 62, 30,
    37, 5, 45, 13, 53, 21, 61, 29,
    36, 4, 44, 12, 52, 20, 60, 28,
    35, 3, 43, 11, 51, 19, 59, 27,
    34, 2, 42, 10, 50, 18, 58, 26,
    33, 1, 41, 9, 49, 17, 57, 25,
    32, 0, 40, 8, 48, 16, 56, 24
]


def xor(x, y):
    return ''.join([_xormap[a, b] for a, b in zip(x, y)])


def convert_hex_to_bin(hex_str):
    bin_str = []
    for i in range(0, len(hex_str)):
        bin_str.append(hex2bin_map[hex_str[i].upper()])
    return bin_str


def pre_sbox(bin_m):
    new = []
    for i in range(0, len(bin_m), 6):
        new.append(bin_m[i:i + 6])
    return new


def key_to_56_bit(key):
    new_key = []
    bin_key_list = convert_hex_to_bin(key)
    bin_key = "".join(bin_key_list)
    # print(bin_key)
    for i in range(0, len(__pc1)):
        new_key.append(bin_key[__pc1[i]])
    # print("56bitkey= ", new_key)
    # new_key = hex(int("".join(new_key), 2))
    return new_key


def key_to_48_bit(key_list):
    new_key = []
    bin_key = "".join(key_list)
    for i in range(0, len(__pc2)):
        new_key.append(bin_key[__pc2[i]])
    return new_key


def shift_left(bin_value, shift_value):
    new_bin = list(bin_value)
    last = len(bin_value) - 1
    for i in range(0, shift_value):
        temp = new_bin[0]
        for j in range(1, len(new_bin)):
            new_bin[j - 1] = new_bin[j]
        new_bin[last] = temp
    return new_bin


def keys_generation(key):
    hex_keys_list = []
    key_56_bit = key_to_56_bit(key)
    # print(key_56_bit)
    key_left = key_56_bit[0:28]
    key_right = key_56_bit[28:]
    for i in range(0, 16):
        s_left = shift_left(key_left, __left_rotations[i])
        s_right = shift_left(key_right, __left_rotations[i])
        s_bin_key = s_left + s_right
        key_48_bit = key_to_48_bit(s_bin_key)
        hex_key = hex(int("".join(key_48_bit), 2))
        hex_keys_list.append(hex_key)
        key_left = s_left
        key_right = s_right

    return hex_keys_list


def expand(text):
    expanded_text = []
    for i in range(0, len(__expansion_table)):
        expanded_text.append(text[__expansion_table[i]])
    return expanded_text


def s_box(row, col, round_number):
    res = []
    value_order = row * 16 + col
    value = __sbox[round_number][value_order]
    res.append((value & 8) >> 3)
    res.append((value & 4) >> 2)
    res.append((value & 2) >> 1)
    res.append((value & 1))
    res = "".join(map(str, res))
    return res


def fix(binary_num):
    if len(binary_num) < 44:
        new_num = str(binary_num)
        for i in range(0, 44 - len(binary_num)):
            new_num = '0' + new_num
        return new_num


def des_function(key, text):
    expanded_text = expand(text)
    print("extext = ", "".join(expanded_text))
    print("lenkey = ", len("".join(convert_hex_to_bin(key[2:]))))
    print("binkey = ", "".join(convert_hex_to_bin(key[2:])))
    # bin_m = convert_dec_to_bin(str(m))
    bin_m = xor("".join(expanded_text), "".join(convert_hex_to_bin(key[2:])))
    temp = []
    round_number = 0
    bin_m = pre_sbox("".join(bin_m))

    for i in range(0, len(bin_m)):
        row = bin_m[i][0] + bin_m[i][5]
        col = bin_m[i][1:  5]
        row = "".join(row)
        col = "".join(col)
        value = s_box(int(row, 2), int(col, 2), round_number)
        temp.append(value)
        round_number = round_number + 1
    # permutation
    out_put = []
    temp = "".join(temp)
    for j in range(0, len(__p)):
        out_put.append(temp[__p[j]])
    out_put = "".join(out_put)

    return out_put


def encrypt(key, text):
    # initial permutation
    keys = keys_generation(key)
    p_text = []
    for i in range(0, len(__ip)):
        p_text.append(text[__ip[i]])
    print("ptext= ", p_text)
    l_text = p_text[:32]
    r_text = p_text[32:]
    r_text = "".join(r_text)
    l_text = "".join(l_text)
    print("rtext= ", r_text)
    for j in range(0, 16):
        print("round =", j)
        print("l_text = ", l_text)
        print("r_text = ", r_text)
        temp = r_text
        out = des_function(keys[j], r_text)
        print("out= ", out)
        print("l_text= ", l_text)
        xor_result_bin = xor("".join(out), "".join(l_text))
        l_text = temp
        r_text = xor_result_bin
    print("final l_text = ", l_text)
    print("fina r_text = ", r_text)
    mixed = r_text + l_text
    print("mixed = ", mixed)
    out_put = []
    # final permutation IP^-1
    for a in range(0, len(__fp)):
        out_put.append(mixed[__fp[a]])
    return "".join(out_put)


# print(keys_generation("133457799BBCDFF1"))
print("cipher_text = ",encrypt("133457799BBCDFF1", "0000000100100011010001010110011110001001101010111100110111101111"))
# print(pre_sbox("011000010001011110111010100001100110010100100111"))
