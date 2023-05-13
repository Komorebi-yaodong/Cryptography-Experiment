# -*- coding: utf-8 -*-
'''
有限域：GF(2^8)上的运算
加减乘 带余除法
mod 11b(hex)
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
            a = a & 0xff
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
            ans = ans ^ (1 << rec)
            a = a ^ (b << rec)
            if a == 0:
                rec = 0 - len(str(bin(b))[2:])
            else:
                rec = len(str(bin(a))[2:]) - len(str(bin(b))[2:])

        return ans, a


def main():
    ploy = 0x11b
    string = input("")
    a = int(string.split()[0], 16)
    b = int(string.split()[2], 16)
    s = string.split()[1]

    # print(str(hex(a))[2:], s, str(hex(b))[2:])

    result = GF2(a, b, s, ploy)

    if s == '/':
        if result[0] < 16:
            print(f"0{str(hex(result[0]))[2:]}", end=' ')
        else:
            print(f"{str(hex(result[0]))[2:]}", end=' ')
        if result[1] < 16:
            print(f"0{str(hex(result[1]))[2:]}")
        else:
            print(f"{str(hex(result[1]))[2:]}")
    else:
        if result[0] < 16:
            print(f"0{str(hex(result[0]))[2:]}", end=' ')
        else:
            print(f"{str(hex(result[0]))[2:]}", end=' ')


if __name__ == "__main__":
    # ############################################################################
    # '''
    #     生成函数调用图
    # '''
    # config = Config()
    # config.trace_filter = GlobbingFilter(
    #     include=[
    #         '*'
    #     ]
    # )
    # config.trace_filter = GlobbingFilter(
    #     exclude=['pycallgraph.*']
    # )
    # ############################################################################
    #
    # graphviz = GraphvizOutput()
    # graphviz.output_file = '有限域四则运算.png'
    # with PyCallGraph(output=graphviz, config=config):
    #     main()
    main()
