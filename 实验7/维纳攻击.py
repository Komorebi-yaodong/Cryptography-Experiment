from gmpy2 import isqrt
import random
from pycallgraph import Config
from pycallgraph import GlobbingFilter
from pycallgraph import PyCallGraph
from pycallgraph.output import GraphvizOutput


def square_multiply(a, n, m):  # 平方乘算法
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


def solve_pq(a, b, c):
    par = isqrt(b * b - 4 * a * c)

    return (-b + par) // (2 * a), (-b - par) // (2 * a)


def gradualFra(cf):
    numerator = 0
    denominator = 1
    for x in cf[::-1]:
        numerator, denominator = denominator, x * denominator + numerator

    return numerator, denominator


def wiener(e, N):
    # 计算连分数
    cf = []
    x = e
    y = N
    while y:
        cf.append(x // y)
        x, y = y, x % y

    # 计算渐进分数
    gf = []
    for i in range(1, len(cf) + 1):
        gf.append(gradualFra(cf[:i]))
    d = 0
    p, q = 0, 0
    for d, k in gf:
        if k == 0:
            continue
        if (e * d - 1) % k != 0:
            continue
        phi = (e * d - 1) // k
        p, q = solve_pq(1, N - phi + 1, N)
        if p * q == N:
            break

    if d == 0:
        print("wrong")

    return p, q, d


def main():
    e = int(input().strip())
    N = int(input().strip())
    ans = wiener(e, N)

    print(ans[0])
    print(ans[1])
    print(ans[2])


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
    graphviz.output_file = '维纳攻击.png'
    with PyCallGraph(output=graphviz, config=config):
        main()
