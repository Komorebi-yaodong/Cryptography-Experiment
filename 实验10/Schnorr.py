from pycallgraph import Config
from pycallgraph import GlobbingFilter
from pycallgraph import PyCallGraph
from pycallgraph.output import GraphvizOutput

from hashlib import sha1


def square_multiply(a, n, m):
    t = a % m
    result = 1
    judge = 1
    while n > 0:
        if judge & n:
            result = (result * t) % m
        n = n >> 1
        t = (t * t) % m
    return result


def schnorr(m, p, q, a, mode, KEY, link):
    if mode == 'Sign':
        k = link[0]
        r = square_multiply(a, k, p)
        e = int(sha1((m + str(r)).encode('utf-8')).hexdigest(), 16)
        s = (k + KEY * e) % q
        return e, s
    elif mode == 'Vrfy':
        e = link[0]
        s = link[1]
        r = (square_multiply(a, s, p) * square_multiply(KEY, e, p)) % p
        hash = int(sha1((m + str(r)).encode('utf-8')).hexdigest(), 16)
        if hash == e:
            return True
        else:
            return False

    else:
        print('mode wrong!')
        return None


def main():
    p = int(input().strip())
    q = int(input().strip())
    a = int(input().strip())
    m = input().strip()

    mode = input().strip()

    if mode == 'Sign':
        x = int(input().strip())
        k = int(input().strip())
        ans1, ans2 = schnorr(m, p, q, a, mode, x, [k])
        print(ans1, ans2)
    elif mode == 'Vrfy':
        v = int(input().strip())
        link = input().strip().split()
        e = int(link[0])
        s = int(link[1])
        ans = schnorr(m, p, q, a, mode, v, [e, s])
        print(ans)
    else:
        print('mode wrong!')
        return None


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
    graphviz.output_file = 'Schnorr.png'
    with PyCallGraph(output=graphviz, config=config):
        main()
        main()
