# -*- coding: utf-8 -*-
from pycallgraph import Config
from pycallgraph import GlobbingFilter
from pycallgraph import PyCallGraph
from pycallgraph.output import GraphvizOutput


def expand_gcd(a, b):  # 欧几里得拓展算法
    if b == 0:
        return 1, 0, a
    else:
        x_tmp, y_tmp, r = expand_gcd(b, a % b)
        x = y_tmp
        y = x_tmp - int(a // b) * y_tmp

        if r < 0:
            r = -r
            x = -x
            y = -y
        if x < 0:
            x = abs(abs(b) - abs(x)) % abs(b)
            y = (r - x * a) // b
        return x, y, r


def affine_cipher(s, k, b, mode):
    result = ""
    judge = expand_gcd(k, 26)[2]
    if judge == 1:
        if mode == 1:  # 加密模式
            for m in s:
                i = ord(m) - ord('a')
                c = (k * i + b) % 26 + ord('a')
                result += chr(c)

        else:  # 解密模式
            e = expand_gcd(k, 26)[0]
            for c in s:
                i = ord(c) - ord('a')
                m = ((i - b) * e) % 26 + ord('a')
                result += chr(m)
    else:
        result = "invalid key"

    return result


def main():
    s1 = input("")
    s2 = input("")
    s3 = input("")

    k, b = int(s1.strip().split()[0]) % 26, int(s1.strip().split()[1]) % 26
    s = s2.strip()
    mode = int(s3.strip())

    result = affine_cipher(s, k, b, mode)
    print(result)


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
    graphviz.output_file = '仿射密码.png'
    with PyCallGraph(output=graphviz, config=config):
        for i in range(7):
            main()
