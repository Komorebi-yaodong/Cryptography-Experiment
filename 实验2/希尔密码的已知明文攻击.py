# -*- coding: utf-8 -*-
import random

from pycallgraph import Config
from pycallgraph import GlobbingFilter
from pycallgraph import PyCallGraph
from pycallgraph.output import GraphvizOutput


def expand_gcd(a, b):  # 欧几里得拓展算法
    if b == 0:
        return 1, 0, a
    else:
        x_tmp, y_tmp, r = expand_gcd(b, a % b)
        x = y_tmp
        y = x_tmp - int(a // b) * y_tmp

        if r < 0:
            r = -r
            x = -x
            y = -y
        if x < 0:
            x = abs(abs(b) - abs(x)) % abs(b)
            y = (r - x * a) // b
        return x, y, r


def minor_matrix(A, i, j, n):  # 余子式

    B = []
    # print("A:")
    # for k in A:
    #     print(k)
    count = -1
    for a in range(n):
        if a == i:
            continue
        else:
            B.append([])
            count += 1
            for b in range(n):
                if b == j:
                    continue
                else:
                    # print(b)
                    B[count].append(A[a][b])

    return B


def det(A, n):
    result = 0
    if n == 2:
        result = A[0][0] * A[1][1] - A[0][1] * A[1][0]
    else:
        for j in range(n):
            B = minor_matrix(A, 0, j, n)

            # print(j,A[0][j], det(B, n - 1) % 26, ((-1) ** (j + 1)) * det(B, n - 1) * A[0][j] % 26, B)
            result += ((-1) ** (j)) * det(B, n - 1) * A[0][j]

    return result % 26


def inverse_matrix(table, n):
    table_ = []
    e = expand_gcd(det(table, n), 26)[0]
    for i in range(n):
        table_.append([])
        for j in range(n):
            ele = (((-1) ** (i + j)) * e * det(minor_matrix(table, j, i, n), n - 1)) % 26
            table_[i].append(ele)
    return table_


def square_matrix_multiply(A, B):
    n = len(A[0])
    result = []
    for i in range(n):
        result.append([])
    for i in range(n):
        for j in range(n):
            element = 0
            for l in range(n):
                element += A[i][l] * B[l][j]
            result[i].append(element % 26)
    return result


def is_inverse(A, n):
    judge = det(A, n)

    if judge == 1:
        return True
    else:
        return False


def hill_plaintext_attack(m, c, n):
    m_table = []
    c_table = []

    # 将明文，密文按n分组
    count = 0
    i = -1
    for s in m:
        if count % n == 0:
            i += 1
            m_table.append([])
        ele = ord(s) - ord('a')
        m_table[i].append(ele)
        count += 1

    count = 0
    i = -1
    for s in c:
        if count % n == 0:
            i += 1
            c_table.append([])
        ele = ord(s) - ord('a')
        c_table[i].append(ele)
        count += 1

    while True:
        j = 0
        list = []
        while j < n:
            l = random.randint(0, len(m_table) - 1)
            # print(l)
            if l not in list:
                # print("pick:", l)
                list.append(l)
                j += 1
        A = []
        B = []
        for i in list:
            A.append(m_table[i])
            B.append(c_table[i])
        # print(is_inverse(A, n))
        if is_inverse(A, n):
            break

    A_ = inverse_matrix(A, n)
    k = square_matrix_multiply(A_, B)

    return k


def main():
    """
        1.求逆函数 √
        2.判断是否可逆函数 √
        3.矩阵组合生成函数
        4.矩阵乘法函数 √
        """
    n = int(input("").strip())
    m = input("").strip()
    c = input("").strip()
    ans = hill_plaintext_attack(m, c, n)

    for i in range(n):
        for j in range(n):
            print(ans[i][j] % 26, end=' ')
        print("")


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
    graphviz.output_file = '希尔密码的已知明文攻击.png'
    with PyCallGraph(output=graphviz, config=config):
        for i in range(3):
            main()
