def GF2(a, b, sign, ploy):
    ans = 0

    if sign == '+' or sign == '-':  # 加减
        ans = a ^ b
        return ans, 0

    elif sign == '*':  # 乘
        while b > 0:
            if b & 1 == 1:
                ans = ans ^ a
            a = a << 1
            if 1 & (a >> 2) == 1:
                a = a ^ ploy
            a = a & 0b11
            b = b >> 1
        return ans, 0

    else:  # 除
        if a == 0:
            return 0, 0
        elif b == 0:
            print("error!")
            return None, None

        rec = len(str(bin(a))[2:]) - len(str(bin(b))[2:])
        while rec >= 0:
            ans = ans ^ (1 << rec)
            a = a ^ (b << rec)
            if a == 0:
                rec = 0 - len(str(bin(b))[2:])
            else:
                rec = len(str(bin(a))[2:]) - len(str(bin(b))[2:])

        return ans, a


def GF_expand_gcd(a, b, ploy):
    if b == 0:
        return 1, 0, a
    else:
        m, r = GF2(a, b, '/', ploy)
        x_tmp, y_tmp, gcd = GF_expand_gcd(b, r, ploy)
        x = y_tmp
        y = x_tmp ^ GF2(y_tmp, m, '*', ploy)[0]
        return x, y, gcd


def ECC_1(x, a, b, p):
    tmp1 = GF2(GF2(x, x, '*', p)[0], x, '*', p)[0]
    tmp2 = GF2(a, GF2(x, x, '*', p)[0], '*', p)[0]
    res = tmp1 ^ tmp2 ^ b % p

    return res


def ECC_2(x, y, a, b, p):
    tmp1 = GF2(y, y, '*', p)[0]
    tmp2 = GF2(x, y, '*', p)[0]
    res = tmp1 ^ tmp2
    return res


if __name__ == "__main__":
    g = 0b01
    a = 0b11
    b = 0b11
    p = 0b111

    # for i in range(1, 4):
    #     res = ECC_1(i, a, b, p)
    #     for j in range(1, 4):
    #         res2 = ECC_2(i, j, a, b, p)
    #         if res == res2:
    #             print(bin(i), ',', bin(j))
    i = 3
    res = ECC_1(i, a, b, p)
    print(res)
    for j in range(1, 4):
        res2 = ECC_2(i, j, a, b, p)
        print(res2, end=' ')

