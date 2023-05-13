# -*- coding: utf-8 -*-
from pycallgraph import Config
from pycallgraph import GlobbingFilter
from pycallgraph import PyCallGraph
from pycallgraph.output import GraphvizOutput


# 有限域上的四则运算
def GF2(a, b, sign, ploy):
    ans = 0

    if sign == '+' or sign == '-':  # 加减
        ans = a ^ b
        return ans, 0

    elif sign == '*':  # 乘
        while b > 0:
            if b & 1 == 1:
                ans = ans ^ a
            a = a << 1
            if 1 & (a >> 8) == 1:
                a = a ^ ploy
            a = a & 0xff
            b = b >> 1
        return ans, 0

    else:  # 除
        if a == 0:
            return 0, 0
        elif b == 0:
            print("error!")
            return None, None

        rec = len(str(bin(a))[2:]) - len(str(bin(b))[2:])
        while rec >= 0:
            ans = ans ^ (1 << rec)
            a = a ^ (b << rec)
            if a == 0:
                rec = 0 - len(str(bin(b))[2:])
            else:
                rec = len(str(bin(a))[2:]) - len(str(bin(b))[2:])

        return ans, a


# 有限域求逆元
def GF_expand_gcd(a, b, ploy):
    if b == 0:
        return 1, 0, a
    else:
        m, r = GF2(a, b, '/', ploy)
        x_tmp, y_tmp, gcd = GF_expand_gcd(b, r, ploy)
        x = y_tmp
        y = x_tmp ^ GF2(y_tmp, m, '*', ploy)[0]
        return x, y, gcd


def aes_get_sbox():
    ploy = 0x11b

    sbox_i = []
    for i in range(16):
        line = []
        for j in range(16):
            item = (i << 4) + j
            line.append(item)
        sbox_i.append(line[:])
    show_box(sbox_i)
    print()

    sbox1 = []
    for i in sbox_i:
        line = []
        for j in i:
            if j == 0x00:
                e = 0x00
            else:
                e = GF_expand_gcd(j, ploy, ploy)[0]
            line.append(e)
        sbox1.append(line[:])
    show_box(sbox1)
    print("")

    sbox = []
    for i in sbox1:
        line = []
        for j in i:
            b = []
            b_ = 0
            c = 0x63
            for k in range(8):
                b.append((j >> k) & 1)
            for k in range(8):
                tmp = b[k] ^ b[(k + 4) % 8] ^ b[(k + 5) % 8] ^ b[(k + 6) % 8] ^ b[(k + 7) % 8] ^ ((c >> k) & 1)
                b_ = b_ ^ (tmp << k)
            line.append(b_)
        sbox.append(line[:])
    show_box(sbox)
    print()

    sbox_ = []
    for i in range(16):
        line = []
        for j in range(16):
            num = (i << 4) + j
            for r in range(16):
                if num in sbox[r]:
                    for l in range(16):
                        if num == sbox[r][l]:
                            ele = (r << 4) + l
                            line.append(ele)
                            break
                        else:
                            continue
                    break
                else:
                    continue
        sbox_.append(line[:])
    show_box(sbox_)


def show_box(sbox):
    for i in sbox:
        for j in i:
            print("0x%02x" % j, end=' ')
        print("")


def main():
    aes_get_sbox()


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
    graphviz.output_file = 'AES算法的S盒生成.png'
    with PyCallGraph(output=graphviz, config=config):
        main()

