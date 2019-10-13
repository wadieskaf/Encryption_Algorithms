order = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7, "i": 8, "j": 9, "k": 10, "l": 11, "m": 12,
         "n": 13, "o": 14, "p": 15, "q": 16, "r": 17, "s": 18, "t": 19, "u": 20, "v": 21, "w": 22, "x": 23, "y": 24,
         "z": 25}
inv_order = {0: 'a', 1: 'b', 2: 'c', 3: 'd', 4: 'e', 5: 'f', 6: 'g', 7: 'h', 8: 'i', 9: 'j', 10: 'k', 11: 'l', 12: 'm',
             13: 'n', 14: 'o', 15: 'p', 16: 'q', 17: 'r', 18: 's', 19: 't', 20: 'u', 21: 'v', 22: 'w', 23: 'x', 24: 'y',
             25: 'z'}
n = 26


def modulo_multiplicative_inverse(A, N):
    for i in range(0, N):

        if (A * i) % N == 1:
            return i
    return -1


def encrypt(text, key1, key2):
    text = text.lower()
    cipher_text = []
    for i in text:
        x = (order[i] * key1 + key2) % n
        x = inv_order[x]
        cipher_text.append(x)
    return cipher_text


def decrypt(text, key1, key2):
    text = text.lower()
    plain_text = []
    inv_key1 = modulo_multiplicative_inverse(key1, n)
    inv_key2 = -1 * key2
    for i in text:
        x = ((order[i] + inv_key2) * inv_key1) % n
        x = inv_order[x]
        plain_text.append(x)
    return plain_text


print(decrypt("ihhwvc", 5, 8))
