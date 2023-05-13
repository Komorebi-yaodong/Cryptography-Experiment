import math


# 国密规定显著性水平alpha为0.01，样本序列的比特长度n为1000000。


# 1.频数检验（F检验）
def f_check(z: str):
    # 当alpha=0.01时，使用临界值B=6.635代替即可用V来验证，减少使用igamc函数
    B = 6.635
    a0 = 0
    a1 = 0
    length = len(z)
    for i in z:
        if i == '0':
            a0 += 1
        elif i == '1':
            a1 += 1
        else:
            print("请输入二进制序列")
            return None
    v = ((a0 - a1) * (a0 - a1)) / length
    if v <= B:
        print(f"{v}<={B}")
        return True
    else:
        print(f"{v}>{B}")
        return False


# 2.扑克检验
def poke_check(z: str):
    while True:
        in_m = input('请输入扑克大小（4或8）：').strip()
        if in_m == '8' or in_m == '4':
            m = int(in_m)
            break
        else:
            print('输入错误，', end='')
    B = {
        4: 30.578,
        8: 310.457
    }
    n = len(z)
    N = (n // m)
    z = z[:N * m]
    Z = {}
    for i in range(N):
        if z[i * m:(i + 1) * m] not in Z:
            Z[z[i * m:(i + 1) * m]] = 1
        else:
            Z[z[i * m:(i + 1) * m]] += 1
    tmp = 0
    for v in Z.values():
        tmp += v * v
    V = (2 ** m) * tmp / N - N
    if V <= B[m]:
        print(f"{V}<={B[m]}")
        return True
    else:
        print(f"{V}>{B[m]}")
        return False


# 3.游程检验
def R_check(z: str):
    alpha = 0.01
    Vnobs = 1
    n = len(z)
    for i in range(0, n - 1):
        if z[i] != z[i + 1]:
            Vnobs += 1
    a1 = 0
    for i in z:
        if i == '1':
            a1 += 1
    phi = a1 / n

    tmp1 = math.fabs(Vnobs - 2 * n * phi * (1 - phi))
    tmp2 = 2 * pow(2 * n, 0.5) * phi * (1 - phi)
    if phi == 0 or phi == 1:
        return False
    p_value = math.erfc(tmp1 / tmp2)
    if p_value >= alpha:
        print(f"{p_value}>={alpha}")
        return True
    else:
        print(f"{p_value}<{alpha}")
        return False


# 4.二元推导检测
def bd_f(z: str):
    Z = ''
    n = len(z)
    for i in range(0, n - 1):
        if z[i] == z[i + 1]:
            Z = Z + '0'
        else:
            Z = Z + '1'
    return Z


def bd_check(z: str):
    while True:
        in_k = input('请输入推导次数（3或7）：')
        if in_k == '3' or in_k == '7':
            k = int(in_k)
            break
        else:
            print('输入错误，', end='')
    for i in range(k):
        z = bd_f(z)
    res = f_check(z)
    return res


# 5.自相关检验
def a_check(z: str):
    alpha = 0.01
    while True:
        in_d = input('请输入距离大小（1，2，8，16）：')
        if in_d == '1' or in_d == '2' or in_d == '8' or in_d == '16':
            d = int(in_d)
            break
        else:
            print('输入错误，', end='')
    n = len(z)
    A = 0
    for i in range(0, n - d):
        if z[i] != z[i + d]:
            A += 1
    tmp1 = 2 * (A - ((n - d) / 2))
    tmp2 = pow(n - d, 0.5)
    v = tmp1 / tmp2
    p_value = math.erfc(math.fabs(v) / pow(2, 0.5))
    if p_value >= alpha:
        print(f"{p_value}>={alpha}")
        return True
    else:
        print(f"{p_value}<{alpha}")
        return False
