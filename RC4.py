n = 8


def generate_s_t(key):
    t = []
    keylen = len(key)
    s = list(range(n))
    for i in range(0, n):
        t.append(key[i % keylen])
    return s, t


def swap(s, i, j):
    s[i], s[j] = s[j], s[i]
    return


def initial_permutation(s, t):
    j = 0
    for i in range(0, n):
        j = (j + s[i] + t[i]) % n
        swap(s, i, j)
    return s


def encrypt(p, key):
    cipher = []
    s, t = generate_s_t(key)
    s = initial_permutation(s, t)
    i, j = 0, 0
    for a in range(0, len(p)):
        i = (i + 1) % n
        j = (j + s[i]) % n
        swap(s, i, j)
        t = (s[i] + s[j]) % n
        k = s[t]
        c = p[a] ^ k
        cipher.append(c)
    return cipher


def decrypt(c, key):
    plain = []
    s, t = generate_s_t(key)
    s = initial_permutation(s, t)
    i, j = 0, 0
    for a in range(0, len(c)):
        i = (i + 1) % n
        j = (j + s[i]) % n
        swap(s, i, j)
        t = (s[i] + s[j]) % n
        k = s[t]
        x = c[a] ^ k
        plain.append(x)
    return plain


print(encrypt([1, 2, 2, 2], [1, 2, 3, 6]))
print(decrypt([4, 3, 2, 3], [1, 2, 3, 6]))
