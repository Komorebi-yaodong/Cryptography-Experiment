# -*- coding: utf-8 -*-
from pycallgraph import Config
from pycallgraph import GlobbingFilter
from pycallgraph import PyCallGraph
from pycallgraph.output import GraphvizOutput


def vernam_cipher(s, k, mode):
    result = ""
    k_table = []
    for element in k:
        num = ord(element)
        k_table.append(num)

    length = len(s)
    p = len(k)

    for i in range(length):
        number = ord(s[i])
        number = number ^ k_table[i % p]
        result += chr(number)

    return result


def main():
    k = input("").strip()
    s = input("").strip()
    mode = int(input("").strip())

    ans = vernam_cipher(s, k, mode)

    print(ans)


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
    graphviz.output_file = '弗纳姆密码.png'
    with PyCallGraph(output=graphviz, config=config):
        for i in range(4):
            main()
