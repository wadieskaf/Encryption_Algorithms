import numpy as np


def build_cipher_matrix(key):
    list1 = []
    for e in key.upper():
        if e not in list1:
            list1.append(e)
    alphabet = "ABCDEFGHIKLMNOPQRSTUVWXYZ"

    for e in alphabet:
        if e not in list1:
            list1.append(e)

    mat = np.array(list1).reshape((5, 5))
    return mat


def message_processing(original_message):
    original_message = original_message.upper()
    new_message = []
    for e in original_message:
        new_message.append(e)
    for e in new_message:
        if e == " ":
            new_message.remove(e)
    if len(new_message) % 2 != 0:
        new_message.append("X")

    return new_message


def encrypt(text, key1, key2):
    key_matrix1 = build_cipher_matrix(key1)
    key_matrix2 = build_cipher_matrix(key2)
    message = message_processing(text)
    cipher_text = []
    for e in range(0, len(message), 2):
        i1, j1 = np.where(key_matrix1 == message[e])
        i2, j2 = np.where(key_matrix2 == message[e + 1])
        if i1 == i2:
            if j1 == 4:
                j1 = -1
            if j2 == 4:
                j2 = -1
            cipher_text.append(key_matrix1[i1, j1 + 1])
            cipher_text.append((key_matrix2[i2, j2 + 1]))
        else:
            cipher_text.append(key_matrix2[i1, j2])
            cipher_text.append(key_matrix1[i2, j1])
    cipher_text = np.array(cipher_text)
    return cipher_text


''' def decrypt(message, key1, key2):
    key_matrix1 = build_cipher_matrix(key1)
    key_matrix2 = build_cipher_matrix(key2)
    message = message.upper()
    plain_text = []
    for e in range(0, len(message), 2):
        i1, j1 = np.where(key_matrix1 == message[e])
        i2, j2 = np.where(key_matrix2 == message[e + 1])
        if i1 == i2:
            if j1 == 0:
                j1 = 5
            if j2 == 0:
                j2 = 5
            plain_text.append(key_matrix1[i1, j1 - 1])
            plain_text.append((key_matrix2[i2, j2 - 1]))
        else:
            i1, j1 = np.where(key_matrix2 == message[e])
            i2, j2 = np.where(key_matrix1 == message[e + 1])
            plain_text.append(key_matrix1[i1, j2])
            plain_text.append(key_matrix2[i2, j1])
    plain_text = np.array(plain_text)
    return plain_text
'''


