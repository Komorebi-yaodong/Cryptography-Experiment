# -*- coding: utf-8 -*-
from pycallgraph import Config
from pycallgraph import GlobbingFilter
from pycallgraph import PyCallGraph
from pycallgraph.output import GraphvizOutput


def extern_gcd2(a: int, b: int):  # 欧几里得拓展算法
    if b == 0:
        return 1, 0, a
    else:
        x_tmp, y_tmp, r = extern_gcd2(b, a % b)
        x = y_tmp
        y = x_tmp - int(a // b) * y_tmp

        if r < 0:
            r = -r
            x = -x
            y = -y

        return x, y, r


def chn_remainder_theorem(m: list, b: list, len):
    e = []
    M = 1
    result = 0
    for i in range(len):  # 求M
        M = M * m[i]
    for i in range(len):  # 求各项逆
        e_ = extern_gcd2(M // m[i], m[i])[0] % m[i]
        e.append(e_)
    for i in range(len):
        result = result + (M // m[i]) * e[i] * (b[i] % m[i])

    result = result % M

    if result < 0:
        result = M + result

    if result == 0:
        result = M

    return result


def main():
    s1 = input("")
    s2 = input("")
    m = []
    b = []
    count = 0
    for num in s1.split():
        m.append(int(num))
        count += 1
    for num in s2.split():
        b.append(int(num))

    result = chn_remainder_theorem(m, b, count)

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
    graphviz.output_file = '中国剩余定理.png'
    with PyCallGraph(output=graphviz, config=config):
        main()
