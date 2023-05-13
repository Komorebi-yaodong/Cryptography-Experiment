# -*- coding: utf-8 -*-
# Eratosthenes Sieve 厄拉多塞筛选法
from pycallgraph import Config
from pycallgraph import GlobbingFilter
from pycallgraph import PyCallGraph
from pycallgraph.output import GraphvizOutput


def era_sieve(n: int):
    flag = [True] * (n + 1)

    m = int(pow(n, 0.5))
    for i in range(2, m + 1):
        if flag[i]:
            count = 2
            while True:
                j = count * i
                if j <= n:
                    flag[j] = False
                else:
                    break
                count += 1

    for i in range(2, n + 1):
        if flag[i]:
            print(i, end=' ')


def main():
    s = input("")
    n = int(s)
    era_sieve(n)


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
    graphviz.output_file = 'Eratosthenes_Sieve.png'
    with PyCallGraph(output=graphviz, config=config):
        main()
