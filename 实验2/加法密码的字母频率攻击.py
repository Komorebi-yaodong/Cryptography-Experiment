# -*- coding: utf-8 -*-
from pycallgraph import Config
from pycallgraph import GlobbingFilter
from pycallgraph import PyCallGraph
from pycallgraph.output import GraphvizOutput


def frequency_attack(s):
    table = []
    for i in range(26):
        table.append(0)
    for c in s:
        num = ord(c) - ord('a')
        table[num] += 1
    max_c = 0
    for i in range(26):
        if table[i] > table[max_c]:
            max_c = i
    return max_c - 4


def main():
    s = input("").strip()

    k = frequency_attack(s)

    print(k)


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
    graphviz.output_file = '加法密码的字母频率攻击.png'
    with PyCallGraph(output=graphviz, config=config):
        main()
