# -*- coding: utf-8 -*-
def s_table_get(k: str):
    S = [i for i in range(0, 256)]
    length = len(k)
    count = 0
    j = 0
    for i in range(256):
        t = int(k[count % length] + k[(count + 1) % length], 16)
        j = (j + S[i] + t) % 256
        S[i], S[j] = S[j], S[i]
        count += 2

    return S


def rc4(m: str, k: str):
    res = ""
    s_table = s_table_get(k)
    i = 0
    j = 0
    for count in range(0, len(m), 2):
        c = int(m[count] + m[count + 1], 16)
        j = (j + s_table[i]) % 256
        s_table[i], s_table[j] = s_table[j], s_table[i]
        t = (s_table[i] + s_table[j]) % 256
        res = res + ("%02x" % (s_table[t] ^ c))
        i += 1

    return res


if __name__ == "__main__":
    k = '0123456789abcedf'
    m = '0123456789abcedf'
    c = rc4(m, k)
    c_ = rc4(c, k)
    print(c)
    print(c_)
