# -*- coding: utf-8 -*-
'''
利用有限域拓展欧几里得算法得到
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
            ans = ans ^ (1 << rec)
            a = a ^ (b << rec)
            if a == 0:
                rec = 0 - len(str(bin(b))[2:])
            else:
                rec = len(str(bin(a))[2:]) - len(str(bin(b))[2:])
            # print(f"a:{bin(a)},b:{bin(b)}")
            # print(f"rec:{rec}")

        return ans, a


def GF_expand_gcd(a, b, ploy):
    if b == 0:
        return 1, 0, a
    else:
        m, r = GF2(a, b, '/', ploy)
        x_tmp, y_tmp, gcd = GF_expand_gcd(b, r, ploy)
        x = y_tmp
        y = x_tmp ^ GF2(y_tmp, m, '*', ploy)[0]
        return x, y, gcd


def main():
    ploy = 0x11b
    s = input()
    a = int(s, 16)

    inverse = GF_expand_gcd(a, ploy, ploy)[0]

    if inverse < 16:
        print(f"0{str(hex(inverse))[2:]}")
    else:
        print(f"{str(hex(inverse))[2:]}")


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
    graphviz.output_file = '有限域求逆元.png'
    with PyCallGraph(output=graphviz, config=config):
        main()
