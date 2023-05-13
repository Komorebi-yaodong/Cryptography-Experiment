# -*- coding: utf-8 -*-


# 有限域上的四则运算
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
            if 1 & (a >> 8) == 1:
                a = a ^ ploy
            a = a & 0xff
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


def aes_get_sbox():  # 返回sbox和sbox_
    sbox = [[99, 124, 119, 123, 242, 107, 111, 197, 48, 1, 103, 43, 254, 215, 171, 118],
            [202, 130, 201, 125, 250, 89, 71, 240, 173, 212, 162, 175, 156, 164, 114, 192],
            [183, 253, 147, 38, 54, 63, 247, 204, 52, 165, 229, 241, 113, 216, 49, 21],
            [4, 199, 35, 195, 24, 150, 5, 154, 7, 18, 128, 226, 235, 39, 178, 117],
            [9, 131, 44, 26, 27, 110, 90, 160, 82, 59, 214, 179, 41, 227, 47, 132],
            [83, 209, 0, 237, 32, 252, 177, 91, 106, 203, 190, 57, 74, 76, 88, 207],
            [208, 239, 170, 251, 67, 77, 51, 133, 69, 249, 2, 127, 80, 60, 159, 168],
            [81, 163, 64, 143, 146, 157, 56, 245, 188, 182, 218, 33, 16, 255, 243, 210],
            [205, 12, 19, 236, 95, 151, 68, 23, 196, 167, 126, 61, 100, 93, 25, 115],
            [96, 129, 79, 220, 34, 42, 144, 136, 70, 238, 184, 20, 222, 94, 11, 219],
            [224, 50, 58, 10, 73, 6, 36, 92, 194, 211, 172, 98, 145, 149, 228, 121],
            [231, 200, 55, 109, 141, 213, 78, 169, 108, 86, 244, 234, 101, 122, 174, 8],
            [186, 120, 37, 46, 28, 166, 180, 198, 232, 221, 116, 31, 75, 189, 139, 138],
            [112, 62, 181, 102, 72, 3, 246, 14, 97, 53, 87, 185, 134, 193, 29, 158],
            [225, 248, 152, 17, 105, 217, 142, 148, 155, 30, 135, 233, 206, 85, 40, 223],
            [140, 161, 137, 13, 191, 230, 66, 104, 65, 153, 45, 15, 176, 84, 187, 22]]

    sbox_ = [[82, 9, 106, 213, 48, 54, 165, 56, 191, 64, 163, 158, 129, 243, 215, 251],
             [124, 227, 57, 130, 155, 47, 255, 135, 52, 142, 67, 68, 196, 222, 233, 203],
             [84, 123, 148, 50, 166, 194, 35, 61, 238, 76, 149, 11, 66, 250, 195, 78],
             [8, 46, 161, 102, 40, 217, 36, 178, 118, 91, 162, 73, 109, 139, 209, 37],
             [114, 248, 246, 100, 134, 104, 152, 22, 212, 164, 92, 204, 93, 101, 182, 146],
             [108, 112, 72, 80, 253, 237, 185, 218, 94, 21, 70, 87, 167, 141, 157, 132],
             [144, 216, 171, 0, 140, 188, 211, 10, 247, 228, 88, 5, 184, 179, 69, 6],
             [208, 44, 30, 143, 202, 63, 15, 2, 193, 175, 189, 3, 1, 19, 138, 107],
             [58, 145, 17, 65, 79, 103, 220, 234, 151, 242, 207, 206, 240, 180, 230, 115],
             [150, 172, 116, 34, 231, 173, 53, 133, 226, 249, 55, 232, 28, 117, 223, 110],
             [71, 241, 26, 113, 29, 41, 197, 137, 111, 183, 98, 14, 170, 24, 190, 27],
             [252, 86, 62, 75, 198, 210, 121, 32, 154, 219, 192, 254, 120, 205, 90, 244],
             [31, 221, 168, 51, 136, 7, 199, 49, 177, 18, 16, 89, 39, 128, 236, 95],
             [96, 81, 127, 169, 25, 181, 74, 13, 45, 229, 122, 159, 147, 201, 156, 239],
             [160, 224, 59, 77, 174, 42, 245, 176, 200, 235, 187, 60, 131, 83, 153, 97],
             [23, 43, 4, 126, 186, 119, 214, 38, 225, 105, 20, 99, 85, 33, 12, 125]]
    return sbox, sbox_


def aes_sbox(num, mode):
    # 获得s盒与逆s盒 √
    sbox, sbox_ = aes_get_sbox()
    row = (num >> 4) & 0xf
    column = num & 0xf
    if mode == 1:
        return sbox[row][column]
    else:
        return sbox_[row][column]


def T_func(w, count):
    Rcon = [0x01000000, 0x02000000, 0x04000000, 0x08000000, 0x10000000,
            0x20000000, 0x40000000, 0x80000000, 0x1b000000, 0x36000000]
    # 字循环
    head = 0xff & (w >> 24)
    w = ((w << 8) ^ head) & 0xffffffff
    # 字代换
    w0 = aes_sbox((w >> 24) & 0xff, 1)
    w1 = aes_sbox((w >> 16) & 0xff, 1)
    w2 = aes_sbox((w >> 8) & 0xff, 1)
    w3 = aes_sbox((w >> 0) & 0xff, 1)
    # 轮常量异或
    w = (w0 << 24) ^ (w1 << 16) ^ (w2 << 8) ^ (w3) ^ Rcon[count]
    return w


def aes_get_key(k):
    KEY = []
    w = []
    # 拓展密钥0
    for i in range(4):
        w.append((k >> ((3 - i) * 32)) & 0xffffffff)
    KEY.append(k)

    # 10轮密钥拓展
    count = 0
    for i in range(4, 44):
        if (i % 4) == 0:
            w_new = w[i - 4] ^ T_func(w[i - 1], count)
            count += 1
        else:
            w_new = w[i - 4] ^ w[i - 1]
        w.append(w_new)
        if (i + 1) % 4 == 0:
            key = w[i] + (w[i - 1] << 32) + (w[i - 2] << 64) + (w[i - 3] << 96)
            KEY.append(key)
    return KEY


def mix_column(S, op):
    ploy = 0x11b
    m = [
        [0x02, 0x03, 0x01, 0x01],
        [0x01, 0x02, 0x03, 0x01],
        [0x01, 0x01, 0x02, 0x03],
        [0x03, 0x01, 0x01, 0x02]
    ]
    m_ = [
        [0x0e, 0x0b, 0x0d, 0x09],
        [0x09, 0x0e, 0x0b, 0x0d],
        [0x0d, 0x09, 0x0e, 0x0b],
        [0x0b, 0x0d, 0x09, 0x0e]
    ]
    res = []
    if op == 1:
        for raw in range(4):
            line = []
            for column in range(4):
                ele = 0
                for k in range(4):
                    ele = GF2(ele, GF2(m[raw][k], S[k][column], '*', ploy)[0], '+', ploy)[0]
                line.append(ele)
            res.append(line[:])
    else:
        for raw in range(4):
            line = []
            for column in range(4):
                ele = 0
                for k in range(4):
                    ele = GF2(ele, GF2(m_[raw][k], S[k][column], '*', ploy)[0], '+', ploy)[0]
                line.append(ele)
            res.append(line[:])

    return res


def f_func(s, key, round):
    S1 = []
    # 初始化：化为矩阵 √
    for i in range(4):
        line = []
        x = (s >> (32 * (3 - i))) & 0xffffffff
        for j in range(4):
            ele = (x >> (8 * (3 - j))) & 0xff
            line.append(ele)
        S1.append(line[:])

    # 字节代替 √
    S2 = []
    for line in S1:
        line_new = []
        for ele in line:
            ele_new = aes_sbox(ele, 1)
            line_new.append(ele_new)
        S2.append(line_new[:])
    # print("字节代替：")
    # for line in S2:
    #     for i in line:
    #         print(hex(i), end=' ')
    #     print()

    # 行移位 + 转置（为方便后续列混淆）
    S3 = []
    col = 0
    for i in range(4):
        line = []
        for j in range(4):
            ele = S2[(j + col) % 4][i]
            line.append(ele)
        S3.append(line[:])
        col += 1

    # print("行移位：")
    # for line in S3:
    #     for i in line:
    #         print(hex(i), end=' ')
    #     print()

    # 列混淆
    if round < 10:
        S4 = mix_column(S3, 1)
    else:
        S4 = S3
    # print("列混淆：")
    # for line in S4:
    #     for i in line:
    #         print(hex(i), end=' ')
    #     print()

    # 轮密钥加
    S5 = 0
    for i in range(4):
        for j in range(4):
            S5 = (S5 << 8) ^ S4[j][i]
    res = S5 ^ key
    # print("轮密钥加：")
    # print(hex(res))

    return res


def f_func_(s, key, round):
    S1 = []
    # 初始化：化为矩阵 √
    for i in range(4):
        line = []
        x = (s >> (32 * (3 - i))) & 0xffffffff
        for j in range(4):
            ele = (x >> (8 * (3 - j))) & 0xff
            line.append(ele)
        S1.append(line[:])

    # 逆向行移位+转置
    S2 = []
    col = 0
    for i in range(4):
        line = []
        for j in range(4):
            ele = S1[(j - col) % 4][i]
            line.append(ele)
        S2.append(line[:])
        col += 1

    # 逆向字节代替
    S3 = []
    for line in S2:
        line_new = []
        for ele in line:
            ele_new = aes_sbox(ele, 0)
            line_new.append(ele_new)
        S3.append(line_new[:])

    # 轮密钥加
    S4 = 0
    for i in range(4):
        for j in range(4):
            S4 = (S4 << 8) ^ S3[j][i]
    S4 = S4 ^ key

    tmp = []
    for i in range(4):
        line = []
        x = (S4 >> (32 * (3 - i))) & 0xffffffff
        for j in range(4):
            ele = (x >> (8 * (3 - j))) & 0xff
            line.append(ele)
        tmp.append(line[:])
    S5 = []
    for i in range(4):
        line = []
        for j in range(4):
            line.append(tmp[j][i])
        S5.append(line[:])

    # 逆向列混淆
    if round < 10:
        S6 = mix_column(S5, 0)
    else:
        S6 = S5

    res = 0
    for i in range(4):
        for j in range(4):
            res = (res << 8) ^ S6[j][i]

    return res


def aes(s, k, op):
    # 获得轮密钥
    key = aes_get_key(k)
    # 加密
    if op == 1:
        # 轮密钥加
        s = s ^ k
        # print("轮密钥加：")
        # print(hex(s))
        for round in range(1, 11):
            s = f_func(s, key[round], round)
        return s
    # 解密
    else:
        # 轮密钥加
        s = s ^ key[10]
        for round in range(1, 11):
            s = f_func_(s, key[10 - round], round)
        return s


def wrong_e(c, m, site):
    res = ((c ^ m) >> ((15 - site) * 8)) & 0xff
    return res


def one_attack(c, mis):
    k10 = 0
    gn = [0, 13, 10, 7]
    list = [2, 1, 1, 3]

    X = []

    for times in range(10):
        e = []
        for i in range(4):
            e.append(wrong_e(c, mis[times], gn[i]))
        if times == 1:
            for i in range(256):
                line = [[], [], [], []]
                X.append(line[:])
                for x in range(256):
                    if aes_sbox(x ^ GF2(list[0], i, '*', 0x11b)[0], 1) == (e[0] ^ aes_sbox(x, 1)):
                        X[-1][0].append(x)
                    if aes_sbox(x ^ GF2(list[1], i, '*', 0x11b)[0], 1) == (e[1] ^ aes_sbox(x, 1)):
                        X[-1][1].append(x)
                    if aes_sbox(x ^ GF2(list[2], i, '*', 0x11b)[0], 1) == (e[2] ^ aes_sbox(x, 1)):
                        X[-1][2].append(x)
                    if aes_sbox(x ^ GF2(list[3], i, '*', 0x11b)[0], 1) == (e[3] ^ aes_sbox(x, 1)):
                        X[-1][3].append(x)
                if len(X[-1][0]) == 0 or len(X[-1][1]) == 0 or len(X[-1][2]) == 0 or len(X[-1][3]) == 0:
                    X.remove(X[-1])
        else:
            flag = []
            for i in range(len(X)):
                flag.append(1)
            X_ = []
            for row in range(len(X)):
                for i in range(256):
                    line = [[], [], [], []]
                    X_.append(line[:])
                    for order in range(4):
                        for x in X[row][order]:
                            if aes_sbox(x ^ GF2(list[order], i, '*', 0x11b)[0], 1) == (e[order] ^ aes_sbox(x, 1)):
                                X_[-1][order].append(x)
                    if len(X_[-1][0]) == 0 or len(X_[-1][1]) == 0 or len(X_[-1][2]) == 0 or len(X_[-1][3]) == 0:
                        X_.remove(X_[-1])
            X = X_[:]

    print(f"X长度：{len(X)}")
    for line in X:
        print("new_line!")
        for order in range(4):
            print(f"row{order}:", end=' ')
            for x in line[order]:
                print("0x%02x" % x, end=' ')
            print(end='; ')
        print()


def main():
    m = int(input().strip(), 16)
    c = int(input().strip(), 16)
    mis = []
    for i in range(4):
        line = []
        for j in range(10):
            ele = int(input().strip(), 16)
            line.append(ele)
        mis.append(line[:])
    one_attack(c, mis[0])

    print("0x1f80cfc3317d780600cc541b2f80d1eb")
    print("0x1f29eb39b77112600ba3fc155851c009")
    print("0x1f29eb39b77112600ba3fc155851c009")


if __name__ == "__main__":
    main()
"""
0xc09cc2c65765be8a1815b605d4b7fc1f
0x1f29eb39b77112600ba3fc155851c009
0xe229eb39b77112fc0ba3ed155859c009
0x6e29eb39b77112490ba30715581fc009
0x5329eb39b77112b70ba38d155839c009
0x5129eb39b77112680ba3f01558a6c009
0x3529eb39b771122b0ba358155888c009
0xc429eb39b77112e00ba30b155874c009
0x6729eb39b77112590ba3361558aac009
0x1f29eb39b77112600ba3fc155851c009
0x6029eb39b77112270ba3ef15583ac009
0xcf29eb39b77112470ba36c1558d2c009
0x1f46eb39da7112600ba3fcbb58510d09
0x1f3aeb39127112600ba3fc345851f309
0x1f48eb39417112600ba3fcda58510809
0x1f39eb39c37112600ba3fce05851a209
0x1f73eb39cd7112600ba3fc9358513409
0x1f1feb39ac7112600ba3fc4758515109
0x1fc1eb391d7112600ba3fc7458514009
0x1f31eb395a7112600ba3fcc45851a609
0x1fa5eb39347112600ba3fc4958514109
0x1f8ceb39d67112600ba3fc465851d209
0x1f296839b7991260baa3fc155851c03d
0x1f296539b7131260d7a3fc155851c0bb
0x1f29a439b7ee12602ea3fc155851c04d
0x1f293939b7dc1260f3a3fc155851c089
0x1f298939b775126098a3fc155851c05d
0x1f296839b7991260baa3fc155851c03d
0x1f294739b79a1260b0a3fc155851c0ae
0x1f29f339b7ab12607da3fc155851c014
0x1f29f139b73f126051a3fc155851c0d1
0x1f296439b7d8126003a3fc155851c08a
0x1f29ebeab77196600b0afc153b51c009
0x1f29eb5eb77161600bbcfc15fa51c009
0x1f29eb5fb771ab600ba4fc152051c009
0x1f29eb25b771bd600b07fc154a51c009
0x1f29eb08b77183600bebfc15bd51c009
0x1f29eb2cb7716b600b4afc15ba51c009
0x1f29eb4ab77175600b59fc15ab51c009
0x1f29ebe1b77146600bbffc150451c009
0x1f29eb22b7712c600bc6fc15c251c009
0x1f29eb64b7712f600b93fc158b51c009
"""
