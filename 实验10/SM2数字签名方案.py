from pycallgraph import Config
from pycallgraph import GlobbingFilter
from pycallgraph import PyCallGraph
from pycallgraph.output import GraphvizOutput

def expand_gcd(a, b):  # 欧几里得拓展算法

    '''
    从-1开始记数
    qi = ri-2 // ri-1
    '''
    # 前要判断
    if a == 0:
        if b > 0:
            return 0, 1, b
        else:
            return 0, -1, -b
    if b == 0:
        return 1, 0, a
    if a == 1 and b == 1:
        return 1, 0, 1
    # 准备工作
    t = 1  # 偏项，以便后续列表从i=-1开始，t+i表示第i项
    r = [a, b]
    x = [1, 0]
    y = [0, 1]
    q = [0, 0]

    i = -1

    q.append(r[t + i] // r[t + i + 1])  # q1

    i = 1
    while True:
        x_new = x[t + i - 2] - q[t + i] * x[t + i - 1]  # xi
        y_new = y[t + i - 2] - q[t + i] * y[t + i - 1]  # yi
        x.append(x_new)
        y.append(y_new)

        r_new = a * x[t + i] + b * y[t + i]  # ri
        if r_new == 0:
            break
        r.append(r_new)
        q_new = r[t + i - 1] // r[t + i]
        q.append(q_new)
        i = i + 1
    x_, y_, r_ = x[t + i - 1], y[t + i - 1], r[t + i - 1]

    if r_ < 0:
        x_ = -x_
        y_ = -y_
        r_ = -r_
    if x_ < 0:
        while x_ < 0:
            x_ = abs(b) // r_ + x_
        y_ = (r_ - a * x_) // b
    x_ = int(x_)
    y_ = int(y_)
    r_ = int(r_)
    return x_, y_, r_


def sm3_packing(s):
    length = len(s)
    r = 64 - ((length + 8) % 64)
    packing = 1 * b'\x80' + (r - 1) * b'\x00' + (length * 8).to_bytes(8, 'big')
    res = s + packing
    return res


def sm3_512g(m):
    """
    分组：512bit（64字节）为一组
    :param m: 字节类型
    :return: 列表类型，每个元素64字节
    """
    length = len(m)
    res = []
    for i in range(0, length, 64):
        res.append(m[i:i + 64])
    return res


def sm3_cls(a: bytes, t: int):
    """
    将字节a循环左移t位
    输入也为字节！
    """
    length = len(a)
    tmp = bin(int.from_bytes(a, byteorder='big'))[2:].rjust(8 * length, '0')
    res = (int(tmp[t:] + tmp[:t], 2)).to_bytes(length, byteorder='big')
    return res


def sm3_xor(a, b):
    """
    字节异或
    :param a: 字节
    :param b: 字节
    :return: 字节
    """
    length = len(a)
    a = int.from_bytes(a, byteorder='big')
    b = int.from_bytes(b, byteorder='big')
    res = (a ^ b).to_bytes(length, byteorder='big')
    return res


def sm3_P(x, judge):
    if judge == 0:
        return sm3_xor(sm3_xor(x, sm3_cls(x, 9)), sm3_cls(x, 17))
    else:
        return sm3_xor(sm3_xor(x, sm3_cls(x, 15)), sm3_cls(x, 23))


def sm3_extend(b: bytes):
    """
    w'[j] = w[j]^w[j+4]
    """
    w = []
    for i in range(0, 64, 4):
        w.append(b[i: i + 4])
    for j in range(16, 68):
        tmp = sm3_P(sm3_xor(sm3_xor(w[j - 16], w[j - 9]), sm3_cls(w[j - 3], 15)), 1)
        w_new = sm3_xor(sm3_xor(tmp, sm3_cls(w[j - 13], 7)), w[j - 6])
        w.append(w_new)

    return w


def sm3_T(j):
    if 0 <= j <= 15:
        return 0x79cc4519.to_bytes(4, byteorder='big')
    else:
        return 0x7a879d8a.to_bytes(4, byteorder='big')


def sm3_bool(x, y, z, j):
    length = len(x)
    if 0 <= j <= 15:
        ff = sm3_xor(sm3_xor(x, y), z)
        gg = sm3_xor(sm3_xor(x, y), z)
    else:
        ff = ((int.from_bytes(x, byteorder='big') & int.from_bytes(y, byteorder='big')) |
              (int.from_bytes(x, byteorder='big') & int.from_bytes(z, byteorder='big')) |
              (int.from_bytes(y, byteorder='big') & int.from_bytes(z, byteorder='big'))
              ).to_bytes(length, byteorder='big')
        gg = ((int.from_bytes(x, byteorder='big') & int.from_bytes(y, byteorder='big')) | (
                (~int.from_bytes(x, byteorder='big')) & int.from_bytes(z, byteorder='big'))
              ).to_bytes(length, byteorder='big')
    return ff, gg


def sm3_cf(v, w):
    A = v[0:4]
    B = v[4:8]
    C = v[8:12]
    D = v[12:16]
    E = v[16:20]
    F = v[20:24]
    G = v[24:28]
    H = v[28:32]
    for j in range(64):
        ss1 = sm3_cls(
            ((int.from_bytes(sm3_cls(A, 12), byteorder='big') +
              int.from_bytes(E, byteorder='big') +
              int.from_bytes(sm3_cls(sm3_T(j), j % 32), byteorder='big')) % (1 << 32)
             ).to_bytes(4, byteorder='big'), 7)
        ss2 = sm3_xor(ss1, sm3_cls(A, 12))
        tt1 = ((int.from_bytes(sm3_bool(A, B, C, j)[0], byteorder='big') +
                int.from_bytes(D, byteorder='big') +
                int.from_bytes(ss2, byteorder='big') +
                int.from_bytes(sm3_xor(w[j], w[j + 4]), byteorder='big')) % (1 << 32)
               ).to_bytes(4, byteorder='big')
        tt2 = ((int.from_bytes(sm3_bool(E, F, G, j)[1], byteorder='big') +
                int.from_bytes(H, byteorder='big') +
                int.from_bytes(ss1, byteorder='big') +
                int.from_bytes(w[j], byteorder='big')) % (1 << 32)
               ).to_bytes(4, byteorder='big')
        D = C
        C = sm3_cls(B, 9)
        B = A
        A = tt1
        H = G
        G = sm3_cls(F, 19)
        F = E
        E = sm3_P(tt2, 0)
    v_new = sm3_xor(A + B + C + D + E + F + G + H, v)
    return v_new


def sm3(m):
    # 参数
    iv = 0x7380166f4914b2b9172442d7da8a0600a96f30bc163138aae38dee4db0fb0e4e.to_bytes(32, byteorder='big')
    # 填充
    m_ = sm3_packing(m)
    # 迭代压缩
    V = [iv, ]

    B = sm3_512g(m_)
    for b in B:
        w = sm3_extend(b)
        v = sm3_cf(V[-1], w)
        V.append(v)
    return hex(int.from_bytes(V[-1], byteorder='big'))[2:].rjust(32 * 2, '0')


def ecc_add(A, B, a, b, p):
    x, y = 0, 0
    if A[0] == B[0] and A[1] + B[1] == 0:
        return [x, y]
    elif A[0] == A[1] == 0:
        return B
    elif B[0] == B[1] == 0:
        return A
    else:
        if A != B:
            tmp = expand_gcd(B[0] - A[0], p)[0]
            # print(tmp)
            delta = ((B[1] - A[1]) * tmp) % p
            # print(delta)
        else:
            tmp = expand_gcd(2 * A[1], p)[0]
            # print(tmp)
            delta = ((3 * A[0] * A[0] + a) * tmp) % p
            # print(delta)
        x = (delta * delta - A[0] - B[0]) % p
        y = (delta * (A[0] - x) - A[1]) % p
        return [x, y]


def ecc_mul(A, k, a, b, p):
    x, y = 0, 0
    res = (x, y)
    reg = A
    while k > 0:
        if k & 1 == 1:
            res = ecc_add(res, reg, a, b, p)
        reg = ecc_add(reg, reg, a, b, p)
        k = k >> 1
    return res


def change(x: int):
    x_ = hex(x)[2:]
    if len(x_) & 1 == 1:
        x_ = '0' + x_
    return bytearray().fromhex(x_)


def sm2_sv(m, p, a, b, G, n, IDA, PA, mode, link):
    ENTLA = (len(IDA) * 8).to_bytes(2, 'big')
    a_ = change(a)
    b_ = change(b)
    G_0 = change(G[0])
    G_1 = change(G[1])
    P0 = change(PA[0])
    P1 = change(PA[1])
    content = ENTLA + IDA.encode('utf-8') + a_ + b_ + G_0 + G_1 + P0 + P1
    # print('content', content)
    ZA = sm3(content)
    # print('ZA', ZA)
    if mode == 'Sign':
        d = link[0]
        k = link[1]
        M = bytearray().fromhex(ZA) + m.encode('utf-8')
        # print('M', M)
        e = int(sm3(M), 16)
        # print('e', e)
        G1 = ecc_mul(G, k, a, b, p)
        r = (e + G1[0]) % n
        s = (expand_gcd(1 + d, n)[0] * (k - r * d)) % n
        return r, s
    elif mode == 'Vrfy':
        r = link[0]
        s = link[1]
        if not ((0 < r < n) or (0 < s < n)):
            return False
        M = bytearray().fromhex(ZA) + m.encode('utf-8')
        e = int(sm3(M), 16)
        t = (r + s) % n
        if t == 0:
            return False
        J = ecc_add(ecc_mul(G, s, a, b, p), ecc_mul(PA, t, a, b, p), a, b, p)
        v = (e + J[0]) % n
        if v == r:
            return True
        else:
            return False
    else:
        print('mode wrong')
        return None


def main():
    p = int(input().strip())
    a = int(input().strip())
    b = int(input().strip())
    L = input().strip().split()
    G = [int(L[0]), int(L[1])]
    n = int(input().strip())
    IDA = input().strip()
    L = input().strip().split()
    PA = [int(L[0]), int(L[1])]
    m = input().strip()
    mode = input().strip()
    if mode == 'Sign':
        d = int(input().strip())
        k = int(input().strip())
        ans1, ans2 = sm2_sv(m, p, a, b, G, n, IDA, PA, mode, [d, k])
        print(ans1, ans2)
    elif mode == 'Vrfy':
        r = int(input().strip())
        s = int(input().strip())
        ans = sm2_sv(m, p, a, b, G, n, IDA, PA, mode, [r, s])
        print(ans)
    else:
        print('mode wrong')
        return None


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
    graphviz.output_file = 'SM2数字签名方案.png'
    with PyCallGraph(output=graphviz, config=config):
        main()
        main()
