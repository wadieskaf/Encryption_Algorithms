import numpy as np
import math as m

conv = {0: "A", 1: "D", 2: "F", 3: "G", 4: "V", 5: "X"}

inv_conv = {"A": 0, "D": 1, "F": 2, "G": 3, "V": 4, "X": 5}

order = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7, "i": 8, "j": 9, "k": 10, "l": 11, "m": 12,
         "n": 13, "o": 14, "p": 15, "q": 16, "r": 17, "s": 18, "t": 19, "u": 20, "v": 21, "w": 22, "x": 23, "y": 24,
         "z": 25}


def build_key_matrix(key_word):
    list1 = []
    for e in key_word.lower():
        if e not in list1:
            list1.append(e)
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789".lower()

    for e in alphabet:
        if e not in list1:
            list1.append(e)

    mat = np.array(list1).reshape((6, 6))
    return mat


def convert_to_numbers(key_word):
    key_numbers = []
    for i in range(0, len(key_word)):
        x = order[key_word[i]]
        key_numbers.append(x)
    key_numbers_arr = np.array(key_numbers)
    temp = sorted(key_numbers)
    for j in range(0, len(key_numbers)):
        key_numbers_arr[np.where(key_numbers_arr == temp[0])[0][0]] = j
        temp.pop(0)

    return key_numbers_arr


def text_processing(text, key_word):
    key_len = len(key_word)
    print("keylen =", key_len)
    text = list(text)
    for e in text:
        if e == " ":
            text.remove(e)
    x = np.array(text)
    print(x)
    x.resize((int(m.ceil(len(text) / key_len)), key_len))
    print("tempx =", x)
    x[np.where(x == "")] = 'a'
    return x.transpose()


def reorder(text, key_word):
    text_matrix = text_processing(text, key_word)
    print("textmat =", text_matrix)
    cipher_text = np.empty((len(key_word), int(m.ceil(len(text) / len(key_word)))), dtype=str)
    print("temp ctext=", cipher_text)
    key_numbers = convert_to_numbers(key_word)
    print("keyn = ", key_numbers)
    for j, i in enumerate(key_numbers):
        print("i=", key_numbers[i], " j=", key_numbers[j])
        cipher_text[i, :] = text_matrix[j, :]
    return cipher_text


def inv_reorder(text, key_word):
    key_numbers = convert_to_numbers(key_word)
    text_matrix = np.array(list(text)).reshape((len(key_numbers), -1))
    reordered_text_matrix = np.empty_like(text_matrix)
    for j, i in enumerate(key_numbers):
        reordered_text_matrix[j, :] = text_matrix[i, :]
    reordered_text_matrix = reordered_text_matrix.transpose()
    return reordered_text_matrix.flatten()


def encrypt(key_word1, key_word2, text):
    temp_text = []
    if key_word2 == "":
        key_mat = build_key_matrix("")
    else:
        key_mat = build_key_matrix(key_word1)
    print(key_mat)
    for c in text:
        i, j = np.where(key_mat == c)
        x = conv[int(i)]
        y = conv[int(j)]
        temp_text.append(x)
        temp_text.append(y)
    if key_word1 != "" and key_word2 == "":
        cipher_text = reorder(temp_text, key_word1)
    elif key_word1 != "" and key_word2 != "":
        cipher_text = reorder(temp_text, key_word2)
    else:
        cipher_text = np.array(temp_text)
    print("final c text=", cipher_text)
    return cipher_text.flatten()


def decrypt(key_word1, key_word2, text):
    plain_text = []
    if key_word2 == "":
        key_mat = build_key_matrix("")
    else:
        key_mat = build_key_matrix(key_word1)
    if key_word1 != "" and key_word2 == "":
        cipher_text = inv_reorder(text, key_word1)
    elif key_word1 != "" and key_word2 != "":
        cipher_text = inv_reorder(text, key_word2)
    else:
        cipher_text = np.array(text)

    for i in range(0, len(cipher_text), 2):
        x = cipher_text[i]
        y = cipher_text[i + 1]
        a = inv_conv[x]
        b = inv_conv[y]
        plain_text.append(key_mat[a, b])

    return np.array(plain_text)

print(encrypt("orange", "rinad", "computer"))

#print(decrypt("orange", "rinad", "AGXAFFAADFDAAVAADGGD"))
