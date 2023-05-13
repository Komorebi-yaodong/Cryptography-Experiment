# -*- coding: utf-8 -*-
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


def minor_matrix(A, i, j, n):
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


def matrix_right(A, B):
    n = len(A)
    res = []
    for i in range(n):
        temp = 0
        for j in range(n):
            temp += (A[j] * B[j][i]) % 26
        res.append(temp)
    return res


def hill_cipher(s, table, mode):
    result = ""
    n = len(table[0])
    A = []
    table_ = []
    code_table = table
    if mode == 0:
        # 求table逆矩阵
        # print("det(table):", det(table, n))
        e = expand_gcd(det(table, n), 26)[0]
        # print("e:", e)
        for i in range(n):
            table_.append([])
            for j in range(n):
                ele = (((-1) ** (i + j)) * e * det(minor_matrix(table, j, i, n), n - 1)) % 26
                # print("ele:", ele)
                table_[i].append(ele)
        code_table = table_

        # for i in code_table:
        #     print(i[0] % 26, i[1] % 26, i[2] % 26)

    count = 0

    for ele in s:
        num = ord(ele) - ord('a')
        A.append(num)
        count += 1
        if count == n:
            tmp = matrix_right(A, code_table)
            for i in tmp:
                c = chr(i % 26 + ord('a'))
                result += c
            A = []
            count = 0
    return result


def main():
    n = int(input("").strip())
    table = []
    for i in range(n):
        line = input("").strip().split()
        for j in range(n):
            line[j] = int(line[j])
        table.append(line)
    s = input("").strip()
    mode = int(input("").strip())

    ans = hill_cipher(s, table, mode)
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
    graphviz.output_file = '希尔密码.png'
    with PyCallGraph(output=graphviz, config=config):
        for i in range(3):
            main()
