# -*- coding: utf-8 -*-
from pycallgraph import Config
from pycallgraph import GlobbingFilter
from pycallgraph import PyCallGraph
from pycallgraph.output import GraphvizOutput


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
            a = a & 0xff  # 这一步有何目的？
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
            a = a ^ (b << rec)
            if a == 0:
                rec = 0 - len(str(bin(b))[2:])
            else:
                rec = len(str(bin(a))[2:]) - len(str(bin(b))[2:])

        return ans, a


def is_primitive_polynomial(p, ploy):
    if p == 0:
        n = 0
    else:
        n = len(str(bin(p))[2:]) - 1

    # fx为不可约多项式
    for i in range(2, p):
        if GF2(p, i, '/', ploy)[1] == 0:
            # print(f"2.i:{i}")
            return False

    # fx可整除x^m+1(m=2^n-1)
    m = (1 << n) - 1
    T = (1 << m) + 1
    if GF2(T, p, '/', ploy)[1] != 0:
        # print(f"2.T:{T}")
        return False

    # fx不能整除x^q+1(q<m)
    for q in range(0, m):
        T = (1 << q) + 1
        if T != p:
            if GF2(T, p, '/', ploy)[1] == 0:
                # print(f"3.T:{T}")
                return False
        else:
            continue
    return True


def main():
    ploy = 0x11b
    start = int(1 << 8)
    end = int(1 << 9)
    P = []
    for p in range(start, end):
        if is_primitive_polynomial(p, ploy):
            P.append(p)
    length = len(P)
    for i in range(length):
        if i == length - 1:
            print(str(bin(P[i]))[2:])
        else:
            print(str(bin(P[i]))[2:], end=' ')


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
    graphviz.output_file = '本原多项式的判定和生成.png'
    with PyCallGraph(output=graphviz, config=config):
        main()
