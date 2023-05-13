def expand_gcd(a, b):  # 欧几里得拓展算法

    '''
    从-1开始记数
    qi = ri-2 // ri-1
    '''
    # 前要判断
    if a == 0:
        if b > 0:
            return 0, 1, b
        else:
            return 0, -1, -b
    if b == 0:
        return 1, 0, a
    if a == 1 and b == 1:
        return 1, 0, 1
    # 准备工作
    t = 1  # 偏项，以便后续列表从i=-1开始，t+i表示第i项
    r = [a, b]
    x = [1, 0]
    y = [0, 1]
    q = [0, 0]

    i = -1

    q.append(r[t + i] // r[t + i + 1])  # q1

    i = 1
    while True:
        x_new = x[t + i - 2] - q[t + i] * x[t + i - 1]  # xi
        y_new = y[t + i - 2] - q[t + i] * y[t + i - 1]  # yi
        x.append(x_new)
        y.append(y_new)

        r_new = a * x[t + i] + b * y[t + i]  # ri
        if r_new == 0:
            break
        r.append(r_new)
        q_new = r[t + i - 1] // r[t + i]
        q.append(q_new)
        i = i + 1
    x_, y_, r_ = x[t + i - 1], y[t + i - 1], r[t + i - 1]

    if r_ < 0:
        x_ = -x_
        y_ = -y_
        r_ = -r_
    if x_ < 0:
        while x_ < 0:
            x_ = abs(b) // r_ + x_
        y_ = (r_ - a * x_) // b
    x_ = int(x_)
    y_ = int(y_)
    r_ = int(r_)
    return x_, y_, r_


def ecc_add(A, B, a, b, p):
    x, y = 0, 0
    if A[0] == B[0] and (A[1] + B[1]) % p == 0:
        return [x, y]
    elif A[0] == A[1] == 0:
        return B
    elif B[0] == B[1] == 0:
        return A
    else:
        if A != B:
            tmp = expand_gcd(B[0] - A[0], p)[0]
            delta = ((B[1] - A[1]) * tmp) % p
        else:
            tmp = expand_gcd(2 * A[1], p)[0]
            delta = ((3 * A[0] * A[0] + a) * tmp) % p
        x = (delta * delta - A[0] - B[0]) % p
        y = (delta * (A[0] - x) - A[1]) % p
        return [x, y]


def ecc_mul(A, k, a, b, p):
    x, y = 0, 0
    res = (x, y)
    reg = A
    while k > 0:
        if k & 1 == 1:
            res = ecc_add(res, reg, a, b, p)
        reg = ecc_add(reg, reg, a, b, p)
        k = k >> 1
    return res


g = [5, 9]
a = 1
b = 6
p = 11
n = 13

d = 5
k = 6
Q = [8, 3]
r = 2
e = 20220529
s = 11

w = expand_gcd(s, n)[0]

u1 = e * w % n
u2 = r * w % n

X = ecc_add(ecc_mul(g, u1, a, b, p), ecc_mul(Q, u2, a, b, p), a, b, p)
print(X)
