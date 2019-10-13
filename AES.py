import numpy as np

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

s_box = ['63', '7C', '77', '7B', 'F2', '6B', '6F', 'C5', '30', '01', '67', '2B', 'FE', 'D7', 'AB', '76', 'CA', '82',
         'C9', '7D', 'FA', '59', '47', 'F0', 'AD', 'D4', 'A2', 'AF', '9C', 'A4', '72', 'C0', 'B7', 'FD', '93', '26',
         '36', '3F', 'F7', 'CC', '34', 'A5', 'E5', 'F1', '71', 'D8', '31', '15', '04', 'C7', '23', 'C3', '18', '96',
         '05',
         '9A', '07', '12', '80', 'E2', 'EB', '27', 'B2', '75', '09', '83', '2C', '1A', '1B', '6E', '5A', 'A0', '52',
         '3B',
         'D6', 'B3', '29', 'E3', '2F', '84', '53', 'D1', '00', 'ED', '20', 'FC', 'B1', '5B', '6A', 'CB', 'BE', '39',
         '4A', '4C', '58', 'CF', 'D0', 'EF', 'AA', 'FB', '43', '4D', '33', '85', '45', 'F9', '02', '7F', '50', '3C',
         '9F', 'A8', '51', 'A3', '40', '8F', '92', '9D', '38', 'F5', 'BC', 'B6', 'DA', '21', '10', 'FF', 'F3', 'D2',
         'CD', '0C', '13', 'EC', '5F', '97', '44', '17', 'C4', 'A7', '7E', '3D', '64', '5D', '19', '73', '60', '81',
         '4F', 'DC', '22', '2A', '90', '88', '46', 'EE', 'B8', '14', 'DE', '5E', '0B', 'DB', 'E0', '32', '3A', '0A',
         '49',
         '06', '24', '5C', 'C2', 'D3', 'AC', '62', '91', '95', 'E4', '79', 'E7', 'C8', '37', '6D', '8D', 'D5', '4E',
         'A9', '6C', '56', 'F4', 'EA', '65', '7A', 'AE', '08', 'BA', '78', '25', '2E', '1C', 'A6', 'B4', 'C6', 'E8',
         'DD', '74', '1F', '4B', 'BD', '8B', '8A', '70', '3E', 'B5', '66', '48', '03', 'F6', '0E', '61', '35', '57',
         'B9',
         '86', 'C1', '1D', '9E', 'E1', 'F8', '98', '11', '69', 'D9', '8E', '94', '9B', '1E', '87', 'E9', 'CE', '55',
         '28', 'DF', '8C', 'A1', '89', '0D', 'BF', 'E6', '42', '68', '41', '99', '2D', '0F', 'B0', '54', 'BB', '16']
s_box_arr = np.array(s_box).reshape(16, 16)

bin2hex_map = {v: k for k, v in hex2bin_map.items()}

_rcon = {1: '01', 2: '02', 3: '04', 4: '08', 5: '10', 6: '20', 7: '40', 8: '80', 9: '1B', 10: '36'}

_xormap = {('0', '1'): '1', ('1', '0'): '1', ('1', '1'): '0', ('0', '0'): '0'}


def convert_hex_to_bin(hex_str):
    bin_str = []
    for i in range(0, len(hex_str)):
        bin_str.append(hex2bin_map[hex_str[i].upper()])
    return "".join(bin_str)


def convert_bin_to_hex(bin_str):
    hex_str = []
    for i in range(0, len(bin_str), 4):
        hex_str.append(bin2hex_map[bin_str[i:i + 4]])
    return hex_str


def convert_hex_mat_to_int(matrix):
    new = []
    for i in range(len(matrix)):
        new.append(int(matrix[i], 16))
    return new


def convert_int_mat_to_hex(matrix):
    new = []
    for i in range(len(matrix)):
        temp = (hex(matrix[i]))[2:].upper()
        if len(temp) == 2:
            new.append(temp)
        else:
            new.append("0" + temp)
    return new


def process_hex_list(hex_list):
    new_list = []
    for i in range(0, len(hex_list), 2):
        sub_list = hex_list[i:i + 2]
        new_list.append("".join(sub_list))
    return new_list


def xor(x, y):
    return ''.join([_xormap[a, b] for a, b in zip(x, y)])


def rotword(key):
    word = list(key)
    temp = word[0]
    for i in range(0, 3):
        word[i] = word[i + 1]
    word[3] = temp
    return word


def rcon(word, i):
    r = xor(convert_hex_to_bin(word[0:2]), convert_hex_to_bin(_rcon[i // 4]))
    return "".join(convert_bin_to_hex(r)) + word[2:]


def subwbyte(word):
    x = s_box_arr[int(word[0], 16), int(word[1], 16)]
    return x


def subword(word):
    new_word = []
    for i in range(0, len(word), 2):
        new_word.append(subwbyte(word[i:i + 2]))
    return "".join(new_word)


def matrix_subbyte(initial):
    matrix = np.array(initial)
    for i in range(0, 4):
        a = subword("".join(matrix[i, :]))
        matrix[i, :] = process_hex_list(a)
    return matrix


def multiple_rotword(x, n):
    res = list(x)
    for i in range(0, n):
        res = rotword(res)
    return res


def shift_rows(initial):
    matrix = np.array(initial)
    for i in range(0, 4):
        x = multiple_rotword(matrix[i, :], i)
        matrix[i, :] = x
    return matrix


def keys_generation(key):
    # print(key)
    keys = np.empty((44, 4), dtype=object)
    for i in range(0, 4):
        keys[i, :] = list(key[i, :])
    for j in range(4, 44):
        # print("j = ", j)
        if j % 4 == 0:
            # print("key = ", keys[j - 1, :])
            rot_w = rotword(keys[j - 1, :])
            # print("rotw = ", rot_w)
            sub_w = subword("".join(rot_w))
            # print('sub_w = ', sub_w)
            hex_t = rcon(sub_w, j)
            t = convert_hex_to_bin(hex_t)
            b1 = convert_hex_to_bin("".join(keys[j - 4, :]))
            w = xor(t, b1)
            w_arr = np.array(process_hex_list(convert_bin_to_hex(w)))
            # print('r_r_key = ', w_arr)
            keys[j, :] = w_arr
        else:
            # print("key1 = ", keys[j - 1, :])
            # print("key2 = ", keys[j - 4, :])
            b1 = convert_hex_to_bin("".join(keys[j - 1, :]))
            b2 = convert_hex_to_bin("".join(keys[j - 4, :]))
            # print("b1 = ", b1)
            # print("b2 = ", b2)
            w = xor(b1, b2)
            # print(w)
            w_arr = np.array(process_hex_list(convert_bin_to_hex(w)))
            # print('warr', j, ' = ', w_arr)
            # print('r_key = ', w_arr)
            keys[j, :] = w_arr
    # convert words to key matrix
    keys_list = []
    for y in range(0, 44, 4):
        k = np.empty((4, 4), dtype=object)
        for x in range(0, 4):
            k[:, x] = np.transpose(keys[x + y, :])
        # print("k = ", k)
        keys_list.append(k)
    return keys_list


def add_round_key(key, text_matrix):
    result = np.empty((4, 4), dtype=object)
    for i in range(0, 4):
        a = "".join(np.transpose(text_matrix[:, i]))
        b = "".join(np.transpose(key[:, i]))
        r = xor(convert_hex_to_bin(a), convert_hex_to_bin(b))
        r = convert_bin_to_hex(r)
        m_r = np.array(process_hex_list(r))
        result[:, i] = np.transpose(m_r)
    return result


def galoisMult(a, b):
    p = 0
    hiBitSet = 0
    for i in range(8):
        if b & 1 == 1:
            p ^= a
        hiBitSet = a & 0x80
        a <<= 1
        if hiBitSet == 0x80:
            a ^= 0x1b
        b >>= 1
    return p % 256


def mixColumn(column):
    temp = column.copy()
    column[0] = galoisMult(temp[0], 2) ^ galoisMult(temp[3], 1) ^ \
                galoisMult(temp[2], 1) ^ galoisMult(temp[1], 3)
    column[1] = galoisMult(temp[1], 2) ^ galoisMult(temp[0], 1) ^ \
                galoisMult(temp[3], 1) ^ galoisMult(temp[2], 3)
    column[2] = galoisMult(temp[2], 2) ^ galoisMult(temp[1], 1) ^ \
                galoisMult(temp[0], 1) ^ galoisMult(temp[3], 3)
    column[3] = galoisMult(temp[3], 2) ^ galoisMult(temp[2], 1) ^ \
                galoisMult(temp[1], 1) ^ galoisMult(temp[0], 3)


def mix_columns(matrix):
    result = np.empty((4, 4), dtype=object)
    # print(result)
    for i in range(0, 4):
        temp = np.transpose(matrix[:, i])
        t = convert_hex_mat_to_int(temp)
        mixColumn(t)
        m_t = np.array(t).transpose()
        m_t = convert_int_mat_to_hex(m_t)
        # print("m_t = ", m_t)
        result[:, i] = m_t
    return result


def encrypt(text, key):
    keys_list = keys_generation(key)
    mat = add_round_key(keys_list[0], text)
    print("text = ", text)
    print("key = ", keys_list[0])

    for i in range(1, 11):
        print("round")
        print("mat = ", mat)
        s = matrix_subbyte(mat)
        print("sub_bvte = " , s)

        sh = shift_rows(s)
        print("shift_rows = ",sh)
        if i != 10:
            m = mix_columns(sh)
            print("mix_columns = ",m)
        else:
            m = sh.copy()
        mat = add_round_key(keys_list[i], m)
        print("key = ", keys_list[i])

    return mat


key = np.array((['54', '68', '61', '74'],
                ['73', '20', '6D', '79'],
                ['20', '4B', '75', '6E'],
                ['67', '20', '46', '75']), dtype=str)

test = np.array((['63', 'EB', '9F', 'A0'],
                 ['2F', '93', '92', 'C0'],
                 ['AF', 'C7', 'AB', '30'],
                 ['A2', '20', 'CB', '2B']), dtype=str)

text = np.array((['54', '4F', '4E', '20'],
                 ['77', '6E', '69', '54'],
                 ['6F', '65', '6E', '77'],
                 ['20', '20', '65', '6F']), dtype=str)

text_t = np.transpose(text)
# print(key[0,:])
# print(keys_generation(key))
# print(rcon('B75A9D85',4))
# print(matrix_subbyte(key))
# print(shift_rows(key))
# print(mix_columns(test))
print(encrypt(text, key))
