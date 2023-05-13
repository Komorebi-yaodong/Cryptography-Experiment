# -*- coding: utf-8 -*-
from pycallgraph import Config
from pycallgraph import GlobbingFilter
from pycallgraph import PyCallGraph
from pycallgraph.output import GraphvizOutput


# 初始置换
def initial_substitution(s_64, mode):  # 输入64bit，mode选择：1：IP置换；0：逆置换
    # 初始置换IP于IP逆
    IP = [
        58, 50, 42, 34, 26, 18, 10, 2, 60, 52, 44, 36, 28, 20, 12, 4,
        62, 54, 46, 38, 30, 22, 14, 6, 64, 56, 48, 40, 32, 24, 16, 8,
        57, 49, 41, 33, 25, 17, 9, 1, 59, 51, 43, 35, 27, 19, 11, 3,
        61, 53, 45, 37, 29, 21, 13, 5, 63, 55, 47, 39, 31, 23, 15, 7
    ]
    IP_ = [
        40, 8, 48, 16, 56, 24, 64, 32, 39, 7, 47, 15, 55, 23, 63, 31,
        38, 6, 46, 14, 54, 22, 62, 30, 37, 5, 45, 13, 53, 21, 61, 29,
        36, 4, 44, 12, 52, 20, 60, 28, 35, 3, 43, 11, 51, 19, 59, 27,
        34, 2, 42, 10, 50, 18, 58, 26, 33, 1, 41, 9, 49, 17, 57, 25
    ]
    result = 0
    if mode == 1:
        for i in range(64):
            distance = 64 - IP[i]
            flag = 1 & (s_64 >> distance)
            result = result ^ (flag << (63 - i))
    else:
        for i in range(64):
            distance = 64 - IP_[i]
            flag = 1 & (s_64 >> distance)
            result = result ^ (flag << (63 - i))
    return result


# 拓展置换E
def expand_substitution(s_32):  # 输入32bit
    result = 0
    E = [
        32, 1, 2, 3, 4, 5,
        4, 5, 6, 7, 8, 9,
        8, 9, 10, 11, 12, 13,
        12, 13, 14, 15, 16, 17,
        16, 17, 18, 19, 20, 21,
        20, 21, 22, 23, 24, 25,
        24, 25, 26, 27, 28, 29,
        28, 29, 30, 31, 32, 1
    ]
    for i in range(48):
        distance = E[i] - 1
        flag = 1 & (s_32 >> distance)
        result = result ^ (flag << i)
    return result


def sbox(s_6, SBox):  # 输入6bit
    # print(f"s6:{bin(s_6)}")
    raw = ((((s_6 >> 5) & 1) << 1) + (s_6 & 1)) & 0b11
    column = (s_6 >> 1) & 0b01111
    # print(f"raw:{raw},column:{column}")
    result = SBox[raw][column]
    return result


def s_box(s_48):  # 输入48bit
    # print(f"s48:{bin(s_48)}")
    s8 = s_48 & 0b111111
    s7 = (s_48 >> 6) & 0b111111
    s6 = (s_48 >> 12) & 0b111111
    s5 = (s_48 >> 18) & 0b111111
    s4 = (s_48 >> 24) & 0b111111
    s3 = (s_48 >> 30) & 0b111111
    s2 = (s_48 >> 36) & 0b111111
    s1 = (s_48 >> 42) & 0b111111

    SBox1 = [
        [14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7],
        [0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8],
        [4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0],
        [15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13]
    ]
    SBox2 = [
        [15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10],
        [3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5],
        [0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15],
        [13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9]
    ]
    SBox3 = [
        [10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8],
        [13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1],
        [13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7],
        [1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12]
    ]
    SBox4 = [
        [7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15],
        [13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9],
        [10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4],
        [3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14]
    ]
    SBox5 = [
        [2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9],
        [14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6],
        [4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14],
        [11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3]
    ]
    SBox6 = [
        [12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11],
        [10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8],
        [9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6],
        [4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13]
    ]
    SBox7 = [
        [4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1],
        [13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6],
        [1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2],
        [6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12]
    ]
    SBox8 = [
        [13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7],
        [1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2],
        [7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8],
        [2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11]
    ]
    s1 = sbox(s1, SBox1)
    s2 = sbox(s2, SBox2)
    s3 = sbox(s3, SBox3)
    s4 = sbox(s4, SBox4)
    s5 = sbox(s5, SBox5)
    s6 = sbox(s6, SBox6)
    s7 = sbox(s7, SBox7)
    s8 = sbox(s8, SBox8)
    result = 0xffffffff & ((s1 << 28) ^ (s2 << 24) ^ (s3 << 20) ^ (s4 << 16) ^ (s5 << 12) ^ (s6 << 8) ^ (s7 << 4) ^ s8)

    return result


# 置换运算P
def permutation(s_32):  # 32bit输入
    result = 0
    P = [
        16, 7, 20, 21, 29, 12, 28, 17,
        1, 15, 23, 26, 5, 18, 31, 10,
        2, 8, 24, 14, 32, 27, 3, 9,
        19, 13, 30, 6, 22, 11, 4, 25
    ]
    for i in range(32):
        distance = 32 - P[i]
        flag = 1 & (s_32 >> distance)
        result = result ^ (flag << (31 - i))
    return result


# 轮函数
def F_func(l_32, r_32, k_48):
    # 拓展置换E
    result1 = expand_substitution(r_32)
    # print("拓展置换：", hex(result1))

    # 与密钥异或
    result2 = k_48 ^ result1
    # print("密钥异或：", hex(result2))

    # s_box 压缩置换
    result3 = s_box(result2)
    # print("S盒：", hex(result3))

    # 置换运算P
    result4 = permutation(result3)
    # print("P盒：", hex(result4))

    # 与左半侧异或并换位
    result5 = l_32 ^ result4
    result = (result5 ^ (r_32 << 32)) & 0xffffffffffffffff

    # print("异或并换位：", hex(result))

    return result


# 密钥生成算法

def get_key(k_64):
    key = []
    LS = [
        1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1
    ]
    # 选择置换1（密钥）
    PC1 = [
        57, 49, 41, 33, 25, 17, 9, 1, 58, 50, 42, 34, 26, 18,
        10, 2, 59, 51, 43, 35, 27, 19, 11, 3, 60, 52, 44, 36,
        63, 55, 47, 39, 31, 23, 15, 7, 62, 54, 46, 38, 30, 22,
        14, 6, 61, 53, 45, 37, 29, 21, 13, 5, 28, 20, 12, 4
    ]
    # 选择置换2（密钥）
    PC2 = [
        14, 17, 11, 24, 1, 5, 3, 28, 15, 6, 21, 10,
        23, 19, 12, 4, 26, 8, 16, 7, 27, 20, 13, 2,
        41, 52, 31, 37, 47, 55, 30, 40, 51, 45, 33, 48,
        44, 49, 39, 56, 34, 53, 46, 42, 50, 36, 29, 32
    ]
    #####################################
    # 密钥置换选择1
    k = 0
    for i in range(56):
        distance = 64 - PC1[i]
        flag = 1 & (k_64 >> distance)
        k = (k ^ (flag << (55 - i))) & 0xffffffffffffff
    C = (k >> 28) & 0xfffffff
    D = k & 0xfffffff
    #####################################
    for round in range(16):
        # 循环左移
        ls = LS[round]
        head = C >> (28 - ls)
        C = ((C << ls) ^ head) & 0xfffffff

        head = D >> (28 - ls)
        D = ((D << ls) ^ head) & 0xfffffff
        # print(f"C1:{bin(C1)} , D1:{bin(D1)}")

        # 置换选择2 获得密钥k
        k = 0
        mid_key = ((C << 28) ^ D) & 0xffffffffffffff
        for i in range(48):
            distance = 56 - PC2[i]
            flag = 1 & (mid_key >> distance)
            k = k ^ (flag << (47 - i))
        key.append(k)
    # print("密钥：", hex(k))

    return key


def des(s, k_64, mode):
    # 加密
    if mode == 1:

        key = get_key(k_64)
        for round in range(16):
            # print(hex(s))
            l = (s >> 32) & 0xffffffff
            r = s & 0xffffffff
            s = F_func(l, r, key[round])
        s = ((s << 32) ^ (s >> 32)) & 0xffffffffffffffff

    # 解密
    else:
        key = get_key(k_64)
        for round in range(16):
            l = (s >> 32) & 0xffffffff
            r = s & 0xffffffff
            s = F_func(l, r, key[15 - round])
        s = ((s << 32) ^ (s >> 32)) & 0xffffffffffffffff
    result = s
    return result


def treble_des(s_64, k1, k2):
    s0 = initial_substitution(s_64, 1)
    s1 = des(s0, k1, 1)
    s2 = des(s1, k2, 0)
    s3 = des(s2, k1, 1)
    res = initial_substitution(s3, 0)
    return res


def get_random_ansi_x9_17(iv, key1, key2, DT, n):
    R = []
    V = [iv, ]
    for i in range(n):
        R_new = treble_des((V[-1] ^ treble_des(DT[i], key1, key2)), key1, key2)
        V_new = treble_des((R_new ^ treble_des(DT[i], key1, key2)), key1, key2)
        R.append(R_new)
        V.append(V_new)
    return R


def main():
    DT = []
    iv = int(input().strip(), 16)
    key1 = int(input().strip(), 16)
    key2 = int(input().strip(), 16)
    n = int(input().strip())
    for i in range(n):
        DT_new = int(input().strip(), 16)
        DT.append(DT_new)
    R = get_random_ansi_x9_17(iv, key1, key2, DT, n)
    for ram in R:
        print("0x%016x" % ram)


if __name__ == "__main__":
    ############################################################################
    '''
        生成函数调用图
    '''
    config = Config()
    config.trace_filter = GlobbingFilter(
        include=[
            '*'
        ]
    )
    config.trace_filter = GlobbingFilter(
        exclude=['pycallgraph.*']
    )
    ############################################################################

    graphviz = GraphvizOutput()
    graphviz.output_file = 'ANSI_X9_17伪随机数发生器.png'
    with PyCallGraph(output=graphviz, config=config):
        main()
