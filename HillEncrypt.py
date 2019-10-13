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

