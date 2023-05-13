# -*- coding: utf-8 -*-
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


def gcd(a, b):  # 最大公因数
    c = a
    while c != 0:
        a = b
        b = c
        c = a % b
    return b


def is_prime(n):  # Miller-Rabin素性检验
    if n == 1:
        return False
    if n == 2:
        return True
    time = 5
    t = n - 1
    k = 0
    judge = 0
    while t & 1 == 0:
        k += 1
        t = t >> 1
    q = t

    for i in range(time):
        judge = 0
        a = random.randint(2, n-1)
        if square_multiply(a, q, n) == 1:
            judge = 1
        for j in range(k):
            if square_multiply(a, (2 ** j) * q, n) == n - 1:
                judge = 1
        # print(judge,a)
        if judge == 0:
            break

    if judge == 1:
        return True
    else:
        return False


def main():
    s = input("")
    x = int(s)
    if is_prime(x):
        print("YES")
    else:
        print("NO")


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
    graphviz.output_file = 'Miller_rabin素性检测算法.png'
    with PyCallGraph(output=graphviz, config=config):
        main()
