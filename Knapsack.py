def modulo_multiplicative_inverse(A, N):
    for i in range(0, N):

        if (A * i) % N == 1:
            return i
    return -1


def find_public_key(b, r, n):
    a = []
    for i in b:
        a.append((i * r) % n)
    return a


def knapsack_sum(text, a):
    s = 0
    for i in range(0, len(a)):
        s = s + text[i] * a[i]
    return s


def inv_knapsack_sum(s, b):
    res = []
    for i in range(len(b) - 1, -1, -1):
        if s >= b[i]:
            res.append(1)
            s = s - b[i]
        else:
            res.append(0)
    res.reverse()
    return res


def encrypt(text, b, r, n):
    a = find_public_key(b, r, n)
    res = []
    for i in range(0, len(text), len(a)):
        s = knapsack_sum(text[i:i + len(a)], a)
        res.append(s)
    return res


def decrypt(text, b, r, n):
    inv_r = modulo_multiplicative_inverse(r, n)
    s = []
    for i in range(0, len(text)):
        x = text[i] * inv_r % n
        s.append(x)
    res = []
    for j in s:
        y = inv_knapsack_sum(j, b)
        res = res + y
    return res


x = list([0, 1, 1, 0, 0, 0, 1, 1, 0, 1, 0, 1, 1, 0, 1, 1, 1, 0])
print(encrypt(x, [2, 3, 6, 13, 27, 52], 31, 105))
print(decrypt([174, 280, 333], [2, 3, 6, 13, 27, 52], 31, 105))
