# -*- coding: utf-8 -*-
import random


def lcg(seed, a, b, m, length):
    x = [seed]
    res = 0
    for i in range(length):
        print((x[-1] & 1), end=' ')
        res = (res << 1) ^ (x[-1] & 1)
        x_new = (a * x[-1] + b) % m
        x.append(x_new)

    print()
    # print(x)
    return res


def lcg_bit(seed, a, b, m, length):
    x = [seed]
    res = 0
    bit = []
    for i in range(length):
        bit.append((x[-1] & 1))
        res = (res << 1) ^ (x[-1] & 1)
        x_new = (a * x[-1] + b) % m
        x.append(x_new)

    # print()
    # print(x)
    return bit


def t_lcg(a, b, m):
    table = []
    for i in range(5000):
        tmp = random.randint(1, m)
        bit = lcg_bit(tmp, a, b, m, 100)
        table.append(bit)

    # 均匀性
    res = []
    for i in range(100):
        flag = 0
        for j in range(5000):
            if table[j][i] == 1:
                flag += 1
        flag = flag / 5000.0
        res.append(flag)
    big_res = 0.0
    for i in res:
        big_res += i

    big_res = big_res / 100

    print("整体占比：", big_res)
    print("每位占比：")
    for i in res:
        print(i, end=' ')
    print()


if __name__ == "__main__":
    a = lcg(2, 6, 0, 13, 12)
    b = lcg(2, 7, 0, 13, 12)

    # print("第一项：")
    # t_lcg(6, 0, 13)
    # print("第二项：")
    # t_lcg(7, 0, 13)
