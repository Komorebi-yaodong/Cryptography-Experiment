# -*- coding: utf-8 -*-
from pycallgraph import Config
from pycallgraph import GlobbingFilter
from pycallgraph import PyCallGraph
from pycallgraph.output import GraphvizOutput


def vigenere_cipher(k, s, mode):
    result = ""
    k_table = []
    for element in k:
        num = ord(element) - ord('a')
        k_table.append(num)

    length = len(s)
    p = len(k)

    if mode == 1:
        for i in range(length):
            number = ord(s[i]) - ord('a')
            number = (number + k_table[i % p]) % 26 + ord('a')
            result += chr(number)
    else:
        for i in range(length):
            number = ord(s[i]) - ord('a')
            number = (number - k_table[i % p]) % 26 + ord('a')
            result += chr(number)

    return result


def main():
    k = input("").strip()
    s = input("").strip()
    mode = int(input("").strip())

    ans = vigenere_cipher(k, s, mode)
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
    graphviz.output_file = '维吉尼亚密码.png'
    with PyCallGraph(output=graphviz, config=config):
        for i in range(5):
            main()
