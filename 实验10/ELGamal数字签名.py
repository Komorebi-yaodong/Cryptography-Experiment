from pycallgraph import Config
from pycallgraph import GlobbingFilter
from pycallgraph import PyCallGraph
from pycallgraph.output import GraphvizOutput

from hashlib import sha256


def square_multiply(a, n, m):
    t = a % m
    result = 1
    judge = 1
    while n > 0:
        if judge & n:
            result = (result * t) % m
        n = n >> 1
        t = (t * t) % m
    return result


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


def ElGamal(m: str, p, g, mode, KEY: int, link: list):
    if mode == 'Sign':
        k = link[0]
        M = int(sha256(m.encode('utf-8')).hexdigest(), 16)
        s1 = square_multiply(g, k, p)
        k_ = expand_gcd(k, p - 1)[0]
        s2 = (k_ * (M - KEY * s1)) % (p - 1)
        return s1, s2
    elif mode == 'Vrfy':
        s1 = link[0]
        s2 = link[1]
        M = int(sha256(m.encode('utf-8')).hexdigest(), 16)
        v1 = square_multiply(g, M, p)
        v2 = (square_multiply(KEY, s1, p) * square_multiply(s1, s2, p)) % p
        if v1 == v2:
            return True
        else:
            return False
    else:
        print('mode wrong')
        return None


def main():
    p = int(input().strip())
    g = int(input().strip())
    m = input()
    mode = input().strip()
    if mode == 'Sign':
        X = int(input().strip())  # 签名方的私钥
        K = int(input().strip())
        ans1,ans2 = ElGamal(m, p, g, mode, X, [K])
        print(ans1,ans2)
    elif mode == 'Vrfy':
        Y = int(input().strip())  # 签名方的公钥
        s = input().strip().split()
        s1 = int(s[0])
        s2 = int(s[1])
        ans = ElGamal(m, p, g, mode, Y, [s1, s2])
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
    graphviz.output_file = 'ELGamal数字签名.png'
    with PyCallGraph(output=graphviz, config=config):
        main()
        main()
