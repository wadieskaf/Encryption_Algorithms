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
    for e in range(0, len(new_message), 2):
        if new_message[e] == new_message[e + 1]:
            new_message.insert(e + 1, "X")

    if len(new_message) % 2 != 0:
        new_message.append("X")

    return new_message


def encrypt(text, key):
    key_matrix = build_cipher_matrix(key)
    print(key_matrix)
    message = message_processing(text)
    print(message)
    cipher_text = []
    for e in range(0, len(message), 2):
        i1, j1 = np.where(key_matrix == message[e])
        i2, j2 = np.where(key_matrix == message[e + 1])
        if i1 == i2:
            if j2 == 4:
                j2 = -1
            elif j1 == 4:
                j1 = -1
            cipher_text.append(key_matrix[i1, j1 + 1])
            cipher_text.append(key_matrix[i2, j2 + 1])
        elif j1 == j2:
            if i1 == 4:
                i1 = -1
            elif i2 == 4:
                i2 = -1
            cipher_text.append(key_matrix[i1 + 1, j1])
            cipher_text.append(key_matrix[i2 + 1, j2])
        else:
            cipher_text.append(key_matrix[i1, j2])
            cipher_text.append(key_matrix[i2, j1])
    cipher_text = np.array(cipher_text)
    return cipher_text


def decrypt(message, key):
    key_matrix = build_cipher_matrix(key)
    message = message.upper()
    plain_text = []
    for e in range(0, len(message), 2):
        print(message[e])
        i1, j1 = np.where(key_matrix == str(message[e]))
        i2, j2 = np.where(key_matrix == str(message[e + 1]))
        if i1 == i2:
            if j2 == 0:
                j2 = 5
            elif j1 == 0:
                j1 = 5
            plain_text.append(key_matrix[i1, j1 - 1])
            plain_text.append(key_matrix[i2, j2 - 1])
        elif j1 == j2:
            if i1 == 0:
                i1 = 5
            elif i2 == 0:
                i2 = 5
            plain_text.append(key_matrix[i1 - 1, j1])
            plain_text.append(key_matrix[i2 - 1, j2])
        else:
            plain_text.append(key_matrix[i1, j2])
            plain_text.append(key_matrix[i2, j1])
    plain_text = np.array(plain_text)
    return plain_text

