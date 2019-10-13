import numpy as np
import math as m

order = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7, "i": 8, "j": 9, "k": 10, "l": 11, "m": 12,
         "n": 13, "o": 14, "p": 15, "q": 16, "r": 17, "s": 18, "t": 19, "u": 20, "v": 21, "w": 22, "x": 23, "y": 24,
         "z": 25}
inv_order = {0: 'a', 1: 'b', 2: 'c', 3: 'd', 4: 'e', 5: 'f', 6: 'g', 7: 'h', 8: 'i', 9: 'j', 10: 'k', 11: 'l', 12: 'm',
             13: 'n', 14: 'o', 15: 'p', 16: 'q', 17: 'r', 18: 's', 19: 't', 20: 'u', 21: 'v', 22: 'w', 23: 'x', 24: 'y',
             25: 'z'}


def modulo_multiplicative_inverse(A, N):
    for i in range(0, N):

        if (A * i) % N == 1:
            return i
    return -1


def convert_to_numbers_matrix(char_matrix):
    numbers_matrix = np.empty_like(char_matrix, dtype=int)
    for index, f in np.ndenumerate(char_matrix):
        f = order[f]
        numbers_matrix[index[0], index[1]] = f
    return numbers_matrix


def convert_to_char_matrix(numbers_matrix):
    char_matrix = np.empty_like(numbers_matrix, dtype=str)
    for index, f in np.ndenumerate(numbers_matrix):
        f = inv_order[f]
        char_matrix[index[0], index[1]] = f
    return char_matrix


def text_processing(text, key_matrix):
    text_list = []
    for c in text:
        if c != " ":
            x = c
            text_list.append(x)
    print(key_matrix)
    print(text_list)
    a, b = key_matrix.shape
    print(a, " ", b)
    rows = int(m.ceil(len(text_list) / a))
    print(rows)
    text_matrix = np.array(text_list, dtype=str)
    text_matrix.resize(rows, a)
    text_matrix[np.where(text_matrix == "")] = 'x'
    print(text_matrix)
    return text_matrix


def encrypt(text, key_matrix):
    text_matrix = text_processing(text, key_matrix)
    text_matrix_numbers = convert_to_numbers_matrix(text_matrix)
    cipher_text_numbers_matrix = np.matmul(text_matrix_numbers, key_matrix) % 26
    cipher_text_matrix = convert_to_char_matrix(cipher_text_numbers_matrix)
    return cipher_text_matrix


def decrypt(text, key_matrix):
    text_matrix = text_processing(text, key_matrix)
    text_matrix_numbers = convert_to_numbers_matrix(text_matrix)
    plain_text_numbers_matrix = np.matmul(text_matrix_numbers, np.linalg.inv(key_matrix)) % 26
    print(plain_text_numbers_matrix)
    plain_text_matrix = convert_to_char_matrix(plain_text_numbers_matrix)
    return plain_text_matrix


def find_key_inverse(key_matrix):
    key_inverse = np.empty_like(key_matrix, dtype=int)
    a, b = np.shape(key_matrix)
    if a == b == 2:
        key_inverse[0, 0] = key_matrix[1, 1]
        key_inverse[1, 1] = key_matrix[0, 0]
        key_inverse[0, 1] = -1 * key_matrix[0, 1]
        key_inverse[1, 0] = -1 * key_matrix[1, 0]
        return key_inverse
    else:
        det = np.linalg.det(key_matrix)
        inv_det = modulo_multiplicative_inverse(det, 26)


key_matrix = np.array(([7, 8],
                       [11, 11]), dtype=int)

mat = np.array(([5, 7, 10],
               [13, 17, 17],
               [0, 5, 4]), dtype = int)

mat2 = np.matrix(mat)

print(mat2.getI())