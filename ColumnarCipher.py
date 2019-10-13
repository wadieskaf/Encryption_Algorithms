import numpy as np

order = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7, "i": 8, "j": 9, "k": 10, "l": 11, "m": 12,
         "n": 13, "o": 14, "p": 15, "q": 16, "r": 17, "s": 18, "t": 19, "u": 20, "v": 21, "w": 22, "x": 23, "y": 24,
         "z": 25}


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


def encrypt(key_word, text):
    text_matrix = np.array(text_processing(text, key_word))
    print(text_matrix)
    cipher_text = np.array(text_matrix)
    key_numbers = convert_to_numbers(key_word)
    print(key_numbers)

    for j, i in enumerate(key_numbers):
        print("i=", i, " j=", j)
        cipher_text[:, j] = text_matrix[:, i]
    return cipher_text


def decrypt(key_word, text):
    text = text.lower()
    cipher_text_matrix = np.array(list(text)).reshape(len(key_word), -1)
    cipher_text_matrix = cipher_text_matrix.transpose()
    plain_text = np.empty_like(cipher_text_matrix)
    key_numbers = convert_to_numbers(key_word)
    for j, i in enumerate(key_numbers):
        print("i=", i, " j=", j)
        plain_text[:, i] = cipher_text_matrix[:, j]
    return "".join(plain_text.flatten())


def text_processing(text, key_word):
    key_numbers = convert_to_numbers(key_word)
    key_len = len(key_numbers)
    text = list(text)
    for e in text:
        if e == " ":
            text.remove(e)
    x = np.array(text)
    print(x)
    x.resize(len(text) // key_len + 1, key_len)
    x[np.where(x == "")] = 'x'
    return x


'''x = encrypt("trivia", "we are discovered")
x = x.transpose()
x = x.flatten()
print(x)'''

#print(decrypt("trivia","EVXROXESEDEXACDWIR"))

print(convert_to_numbers("trivia"))