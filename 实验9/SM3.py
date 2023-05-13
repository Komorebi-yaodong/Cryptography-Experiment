from pycallgraph import Config
from pycallgraph import GlobbingFilter
from pycallgraph import PyCallGraph
from pycallgraph.output import GraphvizOutput


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


def main():
    m = input()
    ans = sm3(m.encode('utf-8'))
    print(ans)


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
    graphviz.output_file = 'SM3.png'
    with PyCallGraph(output=graphviz, config=config):
        for i in range(4):
            main()
