# -*- coding: utf-8 -*-
'''
有限域：GF(2^8)
ploy = 0x11b
'''
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


def GF_square_multiply(a, n, ploy):
    judge = 1
    ans = 1

    while n > 0:
        if judge & n == 1:
            ans = GF2(ans, a, '*', ploy)[0]
        a = GF2(a, a, '*', ploy)[0]
        n = n >> 1
    return ans


def main():
    ploy = 0x11b
    s = input()
    a = int(s.split()[0], 16)
    n = int(s.split()[1])

    result = GF_square_multiply(a, n, ploy)

    print(str(hex(result))[2:])


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
    graphviz.output_file = '有限域快速模幂运算.png'
    with PyCallGraph(output=graphviz, config=config):
        main()
