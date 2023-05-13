# -*- coding: utf-8 -*-
from pycallgraph import Config
from pycallgraph import GlobbingFilter
from pycallgraph import PyCallGraph
from pycallgraph.output import GraphvizOutput


def fence_crypto(s, k, mode):
    result = ""
    table = []
    length = len(s)
    if mode == 1:
        for i in range(k):
            table.append("")
        for i in range(length):
            table[i % k] += s[i]
        for ele in table:
            result += ele
    else:
        list = []
        n = length // k
        r = length % k
        # print(n,r)
        for i in range(k):
            if i <= r - 1:
                list.append(n + 1)
            else:
                list.append(n)
        # print(list)
        point = int(0)
        for i in list:
            # print(s[point: point + i])
            table.append(s[point: point + i])
            point += i
        for i in range(n):
            for j in table:
                result += j[i]
        if r != 0:
            for j in table:
                if len(j) > n:
                    result += j[n]

    return result


def main():
    k = int(input("").strip())
    s = input("").strip()
    mode = int(input("").strip())

    ans = fence_crypto(s, k, mode)
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
    graphviz.output_file = '栅栏密码.png'
    with PyCallGraph(output=graphviz, config=config):
        for i in range(4):
            main()
