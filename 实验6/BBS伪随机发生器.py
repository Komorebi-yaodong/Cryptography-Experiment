# -*- coding: utf-8 -*-
from pycallgraph import Config
from pycallgraph import GlobbingFilter
from pycallgraph import PyCallGraph
from pycallgraph.output import GraphvizOutput


def bbs(p, q, s, length):
    n = p * q
    x = [(s ** 2) % n, ]
    b = 0
    for i in range(length):
        x_new = (x[-1] ** 2) % n
        b_new = x_new % 2
        x.append(x_new)
        b = b ^ (b_new << i)
    return b


def main():
    length = int(input().strip())
    p = int(input().strip())
    q = int(input().strip())
    s = int(input().strip())

    b = bbs(p, q, s, length)

    print(b)


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
    graphviz.output_file = 'BBS伪随机发生器.png'
    with PyCallGraph(output=graphviz, config=config):
        main()
