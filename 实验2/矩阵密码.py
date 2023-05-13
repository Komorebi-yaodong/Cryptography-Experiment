# -*- coding: utf-8 -*-
from pycallgraph import Config
from pycallgraph import GlobbingFilter
from pycallgraph import PyCallGraph
from pycallgraph.output import GraphvizOutput


def matrix_cipher(s, k, n, mode):
    result = ""
    table = []
    for i in range(n):
        table.append([])

    if mode == 1:
        count = 0
        for m in s:
            if count == n:
                count = 0
            table[k[count]].append(m)
            # print(count,m)
            count += 1
        for i in table:
            for c in i:
                result += c
            # print(table[i])
    else:
        length = len(s) // n
        if len(s) % n != 0:
            length += 1
        r = length * n - len(s)

        if r == 0:
            disabled = []
        else:
            disabled = k[-r:]

        point = 0
        for i in range(n):
            num = 0
            for num in range(n):
                if k[num] == i:
                    break
            if num in disabled:
                table[num].append(s[point:point + length - 1])
                point += length - 1
            else:
                table[num].append(s[point:point + length])
                point += length

        count = 0
        i = 0
        for j in range(len(s)):
            if count == n:
                count = 0
                i += 1

            result += table[count][0][i]
            count += 1

    return result


def main():
    n = int(input("").strip())
    _k = input("").strip()
    s = input("").strip()
    mode = int(input("").strip())
    k = []
    for i in _k:
        k.append(int(i) - 1)
    # print(k)

    ans = matrix_cipher(s, k, n, mode)

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
    graphviz.output_file = '矩阵密码.png'
    with PyCallGraph(output=graphviz, config=config):
        main()
        main()
