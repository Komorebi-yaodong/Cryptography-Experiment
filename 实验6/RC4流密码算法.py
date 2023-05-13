# -*- coding: utf-8 -*-
from pycallgraph import Config
from pycallgraph import GlobbingFilter
from pycallgraph import PyCallGraph
from pycallgraph.output import GraphvizOutput


def s_table_get(k: str):
    S = [i for i in range(0, 256)]
    length = len(k)
    count = 0
    j = 0
    for i in range(256):
        t = int(k[count % length] + k[(count + 1) % length], 16)
        j = (j + S[i] + t) % 256
        S[i], S[j] = S[j], S[i]
        count += 2

    return S


def rc4(s, key):
    s_table = s_table_get(key)
    res = '0x'
    i = 0
    j = 0
    for count in range(0, len(s), 2):
        num = int(s[count] + s[count + 1], 16)
        i = (i + 1) % 256
        j = (j + s_table[i]) % 256
        s_table[i], s_table[j] = s_table[j], s_table[i]
        t = (s_table[i] + s_table[j]) % 256
        k = s_table[t]
        res += ("%02x" % (k ^ num))
    return res


def main():
    k = input().strip()[2:]
    m = input().strip()[2:]
    ans = rc4(m, k)
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
    graphviz.output_file = 'RC4流密码算法.png'
    with PyCallGraph(output=graphviz, config=config):
        main()
