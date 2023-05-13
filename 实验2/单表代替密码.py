# -*- coding: utf-8 -*-
from pycallgraph import Config
from pycallgraph import GlobbingFilter
from pycallgraph import PyCallGraph
from pycallgraph.output import GraphvizOutput


def dictionary(t1, t2, mode):
    table = {}
    if mode == 1:
        for i in range(26):
            table[t1[i]] = t2[i]
    else:
        for i in range(26):
            table[t2[i]] = t1[i]
    return table


def single_table_cipher(t1, t2, s, mode):
    result = ""
    code = dictionary(t1, t2, mode)

    if mode == 1:
        for i in s:
            result += code[i]
    else:
        for i in s:
            result += code[i]
    return result


def main():
    t1 = input("").strip()
    t2 = input("").strip()
    s = input("").strip()
    mode = int(input("").strip())

    result = single_table_cipher(t1, t2, s, mode)

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
    graphviz.output_file = '单表代替密码.png'
    with PyCallGraph(output=graphviz, config=config):
        for i in range(3):
            main()
