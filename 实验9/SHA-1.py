from pycallgraph import Config
from pycallgraph import GlobbingFilter
from pycallgraph import PyCallGraph
from pycallgraph.output import GraphvizOutput

def sha1_packing(s):
    """
    位填充+附加长度
    :param s: 字节类型
    :return: 能被512整除
    """
    length = len(s)
    r = 64 - ((length + 8) % 64)
    packing = 1 * b'\x80' + (r - 1) * b'\x00' + (length * 8).to_bytes(8, 'big')
    res = s + packing
    return res


def sha1_512g(s):
    """
    分组：512bit（64字节）为一组
    :param s: 字节类型
    :return: 列表类型，每个元素64字节
    """
    length = len(s)
    res = []
    for i in range(0, length, 64):
        res.append(s[i:i + 64])
    return res


def sha1_32g(s):
    """
    512bit长的数据分为16个子组，每个组32bit（4字节）
    :param s: 字节类型，64字节
    :return: 列表类型，每个元素4字节
    """
    res = []
    for i in range(0, 64, 4):
        res.append(s[i:i + 4])
    return res


def sha1_xor(a, b):
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


def sha1_extend(m: list):
    """
    每个元素4字节
    :param m: 字节列表
    :return: 字节列表
    """
    w = []
    for i in range(80):
        if i <= 15:
            w.append(m[i])
        else:
            w1 = sha1_xor(w[i - 3], w[i - 8])
            w2 = sha1_xor(w[i - 14], w[i - 16])
            w_new = sha1_cls(sha1_xor(w1, w2), 1)
            w.append(w_new)
    return w


def sha1_round(w: list, A: bytes, B: bytes, C: bytes, D: bytes, E: bytes):
    """
    输入全为字节！
    输出也为字节！
    """
    length = len(A)
    a, b, c, d, e = A, B, C, D, E
    for j in range(80):
        tmp = ((int.from_bytes(sha1_cls(a, 5), byteorder='big') +
                int.from_bytes(sha1_f(b, c, d, j), byteorder='big') +
                int.from_bytes(e, byteorder='big') +
                int.from_bytes(w[j], byteorder='big') +
                int.from_bytes(sha1_k(j), byteorder='big')) % (1 << 32)).to_bytes(length, byteorder='big')
        e = d
        d = c
        c = sha1_cls(b, 30)
        b = a
        a = tmp

    A = ((int.from_bytes(A, byteorder='big') +
          int.from_bytes(a, byteorder='big')) % (1 << 32)).to_bytes(length, byteorder='big')
    B = ((int.from_bytes(B, byteorder='big') +
          int.from_bytes(b, byteorder='big')) % (1 << 32)).to_bytes(length, byteorder='big')
    C = ((int.from_bytes(C, byteorder='big') +
          int.from_bytes(c, byteorder='big')) % (1 << 32)).to_bytes(length, byteorder='big')
    D = ((int.from_bytes(D, byteorder='big') +
          int.from_bytes(d, byteorder='big')) % (1 << 32)).to_bytes(length, byteorder='big')
    E = ((int.from_bytes(E, byteorder='big') +
          int.from_bytes(e, byteorder='big')) % (1 << 32)).to_bytes(length, byteorder='big')

    return A, B, C, D, E


def sha1_cls(a: bytes, t: int):
    """
    将字节a循环左移t位
    输入也为字节！
    """
    length = len(a)
    tmp = bin(int.from_bytes(a, byteorder='big'))[2:].rjust(8 * length, '0')
    res = (int(tmp[t:] + tmp[:t], 2)).to_bytes(length, byteorder='big')
    return res


def sha1_f(b: bytes, c: bytes, d: bytes, j):
    """
    输入全为字节
    输出也为字节
    """
    length = len(b)
    b = int.from_bytes(b, byteorder='big')
    c = int.from_bytes(c, byteorder='big')
    d = int.from_bytes(d, byteorder='big')
    if 0 <= j < 20:
        f = (b & c) | ((~b) & (d))
    elif 20 <= j < 40:
        f = b ^ c ^ d
    elif 40 <= j < 60:
        f = (b & c) | (b & d) | (c & d)
    else:
        f = b ^ c ^ d
    f = f.to_bytes(length, byteorder='big')

    return f


def sha1_k(j: int):
    if 0 <= j < 20:
        return 0x5A827999.to_bytes(4, byteorder='big')
    elif 20 <= j < 40:
        return 0x6ED9EBA1.to_bytes(4, byteorder='big')
    elif 40 <= j < 60:
        return 0x8F1BBCDC.to_bytes(4, byteorder='big')
    else:
        return 0xCA62C1D6.to_bytes(4, byteorder='big')


def mysha1(s):
    """
    下列全部以字节类型进行处理
    448 / 8 = 56
    512 / 8 = 64
    :param s: 字节类型
    :return: 十六进制字符串类型
    """
    # 参数
    A = 0X67452301.to_bytes(4, byteorder='big')
    B = 0XEFCDAB89.to_bytes(4, byteorder='big')
    C = 0X98BADCFE.to_bytes(4, byteorder='big')
    D = 0X10325476.to_bytes(4, byteorder='big')
    E = 0XC3D2E1F0.to_bytes(4, byteorder='big')

    # 位填充+附加长度
    s = sha1_packing(s)

    # print('填充+附加长度后：', bin(int.from_bytes(s, byteorder='big'))[2:].rjust(len(s) * 8, '0'))
    # 分组：512bit（64字节）为一组
    Y = sha1_512g(s)

    # 子分组：512bit长的数据分为16个子组，每个组32bit（4字节）
    for l in Y:
        m = sha1_32g(l)
        w = sha1_extend(m)

        A, B, C, D, E = sha1_round(w, A, B, C, D, E)
    res = hex(int.from_bytes(A + B + C + D + E, byteorder='big'))[2:].rjust(40, '0')

    return res


def main():
    s = input().strip()
    ans = mysha1(s.encode('utf-8'))
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
    graphviz.output_file = 'SHA-1.png'
    with PyCallGraph(output=graphviz, config=config):
        for i in range(4):
            main()