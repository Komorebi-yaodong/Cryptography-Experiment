# -*- coding: utf-8 -*-

'''
sm4_128_encode(m, mk) :加密函数（128位）
sm4_128_decode(m, mk) :解密函数（128位）
sm4_128_rk(mk) :轮密钥（list类型）
'''


def int2bin(x):  # 要求正整数

    x_list = []
    while x != 0:
        c = x & 1
        x_list.append(c)
        x = x >> 1
    length = len(x_list)
    for i in range(length, 32):
        x_list.append(0)
    x_list.reverse()

    return x_list


# 数字转二进制列表

# 列表转字符串
def list2s(x_list):
    y = ""
    for i in x_list:
        y += str(i)
    return y


# 列表转字符串

# 循环左移（输出整数）
def left_roll(x, pace):
    y = ((x << pace) | (x >> (32 - pace))) & 0xFFFFFFFF
    return y


# 加密算法的循环左移异或

def l_func_e(x):
    x1 = left_roll(x, 2)
    x2 = left_roll(x, 10)
    x3 = left_roll(x, 18)
    x4 = left_roll(x, 24)

    y = x1 ^ x2 ^ x3 ^ x4

    return y


# 加密算法的循环左移异或

# 密钥拓展的循环左移异或

def l_func_pk(x):
    x1 = left_roll(x, 13)
    x2 = left_roll(x, 23)

    y = x1 ^ x2

    return y


# 密钥拓展的循环左移异或

# τ函数
def tao_func(x0, x1, x2, x3):
    y0 = sbox(x0)
    y1 = sbox(x1)
    y2 = sbox(x2)
    y3 = sbox(x3)
    return [y0, y1, y2, y3]


# τ函数

# S盒函数
def sbox(a):  # 输入2位的数字( 0 ~ (2**32-1) )
    BOX = [0xD6, 0x90, 0xE9, 0xFE, 0xCC, 0xE1, 0x3D, 0xB7, 0x16, 0xB6, 0x14, 0xC2, 0x28, 0xFB, 0x2C, 0x05, 0x2B,
           0x67, 0x9A, 0x76, 0x2A, 0xBE, 0x04, 0xC3, 0xAA, 0x44, 0x13, 0x26, 0x49, 0x86, 0x06, 0x99, 0x9C, 0x42,
           0x50, 0xF4, 0x91, 0xEF, 0x98, 0x7A, 0x33, 0x54, 0x0B, 0x43, 0xED, 0xCF, 0xAC, 0x62, 0xE4, 0xB3, 0x1C,
           0xA9, 0xC9, 0x08, 0xE8, 0x95, 0x80, 0xDF, 0x94, 0xFA, 0x75, 0x8F, 0x3F, 0xA6, 0x47, 0x07, 0xA7, 0xFC,
           0xF3, 0x73, 0x17, 0xBA, 0x83, 0x59, 0x3C, 0x19, 0xE6, 0x85, 0x4F, 0xA8, 0x68, 0x6B, 0x81, 0xB2, 0x71,
           0x64, 0xDA, 0x8B, 0xF8, 0xEB, 0x0F, 0x4B, 0x70, 0x56, 0x9D, 0x35, 0x1E, 0x24, 0x0E, 0x5E, 0x63, 0x58,
           0xD1, 0xA2, 0x25, 0x22, 0x7C, 0x3B, 0x01, 0x21, 0x78, 0x87, 0xD4, 0x00, 0x46, 0x57, 0x9F, 0xD3, 0x27,
           0x52, 0x4C, 0x36, 0x02, 0xE7, 0xA0, 0xC4, 0xC8, 0x9E, 0xEA, 0xBF, 0x8A, 0xD2, 0x40, 0xC7, 0x38, 0xB5,
           0xA3, 0xF7, 0xF2, 0xCE, 0xF9, 0x61, 0x15, 0xA1, 0xE0, 0xAE, 0x5D, 0xA4, 0x9B, 0x34, 0x1A, 0x55, 0xAD,
           0x93, 0x32, 0x30, 0xF5, 0x8C, 0xB1, 0xE3, 0x1D, 0xF6, 0xE2, 0x2E, 0x82, 0x66, 0xCA, 0x60, 0xC0, 0x29,
           0x23, 0xAB, 0x0D, 0x53, 0x4E, 0x6F, 0xD5, 0xDB, 0x37, 0x45, 0xDE, 0xFD, 0x8E, 0x2F, 0x03, 0xFF, 0x6A,
           0x72, 0x6D, 0x6C, 0x5B, 0x51, 0x8D, 0x1B, 0xAF, 0x92, 0xBB, 0xDD, 0xBC, 0x7F, 0x11, 0xD9, 0x5C, 0x41,
           0x1F, 0x10, 0x5A, 0xD8, 0x0A, 0xC1, 0x31, 0x88, 0xA5, 0xCD, 0x7B, 0xBD, 0x2D, 0x74, 0xD0, 0x12, 0xB8,
           0xE5, 0xB4, 0xB0, 0x89, 0x69, 0x97, 0x4A, 0x0C, 0x96, 0x77, 0x7E, 0x65, 0xB9, 0xF1, 0x09, 0xC5, 0x6E,
           0xC6, 0x84, 0x18, 0xF0, 0x7D, 0xEC, 0x3A, 0xDC, 0x4D, 0x20, 0x79, 0xEE, 0x5F, 0x3E, 0xD7, 0xCB, 0x39,
           0x48]
    return BOX[a]


# S盒函数

# T_加密算法函数
def t_func_e(x0, x1, x2, x3, rk):
    t = x1 ^ x2 ^ x3 ^ rk
    # 1个32位的数 -> 4个8位的数
    t1 = ((t & 0xFFFFFFFF) >> 24) & 0xFF
    t2 = ((t & 0xFFFFFF) >> 16) & 0xFF
    t3 = ((t & 0xFFFF) >> 8) & 0xFF
    t4 = t & 0xFF

    # tao函数
    s1, s2, s3, s4 = tao_func(t1, t2, t3, t4)

    s = (s1 << 24) + (s2 << 16) + (s3 << 8) + s4

    x4 = x0 ^ s ^ l_func_e(s)

    return x4


# T_加密算法盒函数

# F_密钥拓展函数
def f_func_pk(k, ck):
    k0 = ((k & 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF) >> 96) & 0xFFFFFFFF
    k1 = ((k & 0xFFFFFFFFFFFFFFFFFFFFFFFF) >> 64) & 0xFFFFFFFF
    k2 = ((k & 0xFFFFFFFFFFFFFFFF) >> 32) & 0xFFFFFFFF
    k3 = k & 0xFFFFFFFF

    t = k1 ^ k2 ^ k3 ^ ck

    t1 = ((t & 0xFFFFFFFF) >> 24) & 0xFF
    t2 = ((t & 0xFFFFFF) >> 16) & 0xFF
    t3 = ((t & 0xFFFF) >> 8) & 0xFF
    t4 = t & 0xFF

    s1, s2, s3, s4 = tao_func(t1, t2, t3, t4)
    s = (s1 << 24) + (s2 << 16) + (s3 << 8) + s4

    rk = s ^ k0 ^ l_func_pk(s)

    return rk


# F_密钥拓展函数

# F_加密算法盒函数
def f_func_e(x, rk):  # 输入128位，
    x0 = ((x & 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF) >> 96) & 0xFFFFFFFF
    x1 = ((x & 0xFFFFFFFFFFFFFFFFFFFFFFFF) >> 64) & 0xFFFFFFFF
    x2 = ((x & 0xFFFFFFFFFFFFFFFF) >> 32) & 0xFFFFFFFF
    x3 = x & 0xFFFFFFFF

    x4 = t_func_e(x0, x1, x2, x3, rk)

    return x4


# F_加密算法盒函数

# FF_密钥拓展函数
def ff_func_pk(mk, i):  # 输入128位

    ck = [0x00070e15, 0x1c232a31, 0x383f464d, 0x545b6269,
          0x70777e85, 0x8c939aa1, 0xa8afb6bd, 0xc4cbd2d9,
          0xe0e7eef5, 0xfc030a11, 0x181f262d, 0x343b4249,
          0x50575e65, 0x6c737a81, 0x888f969d, 0xa4abb2b9,
          0xc0c7ced5, 0xdce3eaf1, 0xf8ff060d, 0x141b2229,
          0x30373e45, 0x4c535a61, 0x686f767d, 0x848b9299,
          0xa0a7aeb5, 0xbcc3cad1, 0xd8dfe6ed, 0xf4fb0209,
          0x10171e25, 0x2c333a41, 0x484f565d, 0x646b7279]

    rk = f_func_pk(mk, ck[i])

    return rk


# F_密钥拓展函数

# 用SM4加密128位信息
def sm4_128_encode(x, mk):  # 都是128位
    fk0 = 0xA3B1BAC6
    fk1 = 0x56AA3350
    fk2 = 0x677D9197
    fk3 = 0xB27022DC
    fk = (fk0 << 96) + (fk1 << 64) + (fk2 << 32) + fk3
    mk = mk ^ fk
    for i in range(32):
        rk = ff_func_pk(mk, i)
        mk = ((mk & 0xFFFFFFFFFFFFFFFFFFFFFFFF) << 32) + rk  # 下一轮的密钥
        x4 = f_func_e(x, rk)
        x = ((x & 0xFFFFFFFFFFFFFFFFFFFFFFFF) << 32) + x4  # 下一轮的x
    # 结果需要逆序
    x32 = ((x & 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF) >> 96) & 0xFFFFFFFF
    x33 = ((x & 0xFFFFFFFFFFFFFFFFFFFFFFFF) >> 64) & 0xFFFFFFFF
    x34 = ((x & 0xFFFFFFFFFFFFFFFF) >> 32) & 0xFFFFFFFF
    x35 = x & 0xFFFFFFFF
    x = x32 + (x33 << 32) + (x34 << 64) + (x35 << 96)

    return x


# 用SM4加密128位信息

# 用SM4加密获得解密用的密钥
def sm4_128_rk(mk):
    fk0 = 0xA3B1BAC6
    fk1 = 0x56AA3350
    fk2 = 0x677D9197
    fk3 = 0xB27022DC
    fk = (fk0 << 96) + (fk1 << 64) + (fk2 << 32) + fk3
    mk = mk ^ fk
    rk = []
    for i in range(32):
        rk0 = ff_func_pk(mk, i)
        rk.append(rk0)
        mk = ((mk & 0xFFFFFFFFFFFFFFFFFFFFFFFF) << 32) + rk0  # 下一轮的密钥

    rk = rk[::-1]  # 倒序 (rk31,rk30,rk29,rk28......)

    return rk


# 用SM4加密获得解密用的密钥

# SM4解密128位信息
def sm4_128_decode(m, mk):
    rk = sm4_128_rk(mk)

    for i in range(4):
        m4 = f_func_e(m, rk[i])
        m = ((m & 0xFFFFFFFFFFFFFFFFFFFFFFFF) << 32) + m4  # 下一轮的m

    mk = (rk[0] << 96) + (rk[1] << 64) + (rk[2] << 32) + rk[3]

    for i in range(4, 32):
        rk0 = ff_func_pk(mk, 35 - i)
        mk = ((mk & 0xFFFFFFFFFFFFFFFFFFFFFFFF) << 32) + rk0  # 下一轮的密钥
        m4 = f_func_e(m, rk0)
        m = ((m & 0xFFFFFFFFFFFFFFFFFFFFFFFF) << 32) + m4  # 下一轮的m

    m3 = ((m & 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF) >> 96) & 0xFFFFFFFF
    m2 = ((m & 0xFFFFFFFFFFFFFFFFFFFFFFFF) >> 64) & 0xFFFFFFFF
    m1 = ((m & 0xFFFFFFFFFFFFFFFF) >> 32) & 0xFFFFFFFF
    m0 = m & 0xFFFFFFFF
    m = m3 + (m2 << 32) + (m1 << 64) + (m0 << 96)
    return m


# SM4解密128位信息

if __name__ == "__main__":
    iv = 0xa8638d2fb23cc49206edd7c84532eaab
    file_in_name = "2.bmp"
    file_out_name = '2_CBC.bmp'
    k = 0x7dfee2f716c4c4cd5217f0d57c75c2d7
    op = 1

    # 加解密数据输入
    s = ""
    head = b''

    with open(file_in_name, 'rb') as f:
        count = 0
        head_length = 0
        count_total = 0
        while True:
            ele = f.read(1)
            if ele == b'':
                break
            if head_length < 54:
                head = head + ele
                head_length += 1
            else:

                num = int.from_bytes(ele, byteorder='big')
                s = s + ("%02x" % num)
                count += 1
    print("图片接收完成")
    # 填充
    if op == 1:
        r = len(s) % 32
        content = "%02x" % ((32 - r) // 2)
        for i in range(16 - (r // 2)):
            s += content
        # print("填充后：")
        # print(s)

    # 分组
    gn = len(s) // 32
    gp = []
    for i in range(gn):
        v = int(s[i * 32:(i + 1) * 32], 16)
        gp.append(v)
    #########################################################################
    """
    只用改这部分即可
    CBC
    """
    # 获得结果

    # print("获得结果：")
    ans_gp = ""
    for i in gp:
        if op == 1:
            iv ^= i
            res = sm4_128_encode(iv, k)
            iv = res
        else:
            res = sm4_128_decode(i, k) ^ iv
            iv = i

        v = "%032x" % res
        ans_gp += v
    print("图片加密完成")
    # print('')
    #########################################################################
    # 解密判定
    if op == 0:
        r = ans_gp[-2:]
        gap = (int(r, 16)) * 2
        ans_gp = ans_gp[:-gap]

    # 输出结果
    with open(file_out_name, 'wb') as f_out:
        f_out.write(head)
        for i in range(0, len(ans_gp), 2):
            num = int(ans_gp[i:i + 2], 16)
            byte = num.to_bytes(1, byteorder='big')
            f_out.write(byte)
        print("over!")
