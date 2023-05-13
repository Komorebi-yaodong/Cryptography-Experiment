from hashlib import sha256
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


def kdf(z: str, klen: int):  # 十六进制字符串输入，字符串输出
    ct = 1
    v = 256
    if len(z) & 1 != 0:
        z = '0' + z
    if klen % v != 0:
        end = (klen // v) + 1
    else:
        end = (klen // v) + 0
    Ha = []
    for i in range(end):
        ha = sha256(bytearray.fromhex(z + ("%08x" % ct))).hexdigest()
        Ha.append(ha)
        ct += 1
    if klen % v == 0:
        tail = Ha[-1]
    else:
        tail = Ha[-1][:(klen - v * (klen // v)) // 4]
        # print(len(tail))
    res = ''
    for i in range(len(Ha) - 1):
        res = res + Ha[i]
    res = res + tail
    return res


def e2s(num: int, length: int):
    if length % 8 == 0:
        l = length // 8
    else:
        l = (length // 8) + 1
    res = hex(num)[2:].rjust(l * 2, '0')

    return res


def sm2(text: str, a, b, p, G, Par, op, Key, k):
    text = text[2:]
    if op == 1:
        klen = len(text) * 4
        C1 = ecc_mul(G, k, a, b, p)
        # print("C1:", hex(C1[0]), hex(C1[0]))
        Q = ecc_mul(Key, k, a, b, p)
        s_C1 = '04' + e2s(C1[0], Par) + e2s(C1[1], Par)
        # print(hex(Q[0])[2:], len(hex(Q[0])[2:]))
        x2 = e2s(Q[0], Par)
        y2 = e2s(Q[1], Par)
        # print('x2:', x2, len(x2))
        # print('y2:', y2, len(y2))
        t = kdf(x2 + y2, klen)
        # print('t:', t, len(t))
        C2 = hex(int(text, 16) ^ int(t, 16))[2:].rjust(klen // 4, '0')
        # print('klen:', klen // 4)
        # print('x2|M|y2', x2 + text[2:] + y2)
        C3 = sha256(bytearray.fromhex(x2 + text + y2)).hexdigest()
        # print('C3:', C3)
        # print('s_C1:', s_C1, len(s_C1))
        # print('C2:', C2, len(C2))
        # print('C3:', C2, len(C3))
        res = s_C1 + C2 + C3
        return res
    else:
        # print('text:', text, len(text))
        C1 = text[:2 + Par // 2]
        C2 = text[2 + Par // 2:][:-64]
        # print('C1', C1, len(C1))
        # print('C2', C2, len(C2))
        klen = len(C2) * 4
        # print('c1:', C1[2:2 + Par // 4], C1[2 + Par // 4:])
        c1 = [int(C1[2:2 + Par // 4], 16), int(C1[2 + Par // 4:], 16)]
        Q = ecc_mul(c1, Key, a, b, p)
        x2 = e2s(Q[0], Par)
        y2 = e2s(Q[1], Par)
        t = kdf(x2 + y2, klen)
        # print('t', t)
        M = hex(int(C2, 16) ^ int(t, 16))[2:].rjust(klen // 4, '0')
        return M


def main():
    p = int(input().strip())
    a = int(input().strip())
    b = int(input().strip())
    L = input().strip().split()
    G = [int(L[0]), int(L[1])]
    Par = int(input().strip())
    op = int(input().strip())
    text = input().strip()
    if op == 1:
        L = input().strip().split()
        Key = [int(L[0]), int(L[1])]
        k = int(input().strip())
    else:
        Key = int(input().strip())
        k = 0
    ans = sm2(text, a, b, p, G, Par, op, Key, k)
    print("0x" + ans)


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
    graphviz.output_file = 'SM2-公钥加密.png'
    with PyCallGraph(output=graphviz, config=config):
        for i in range(4):
            main()
