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


p = 19
g = 13
x = 7
k = 11
m = 4

s1 = 2
s2 = 4
y = square_multiply(g, x, p)
v1 = square_multiply(g, m, p)
v2 = (square_multiply(y, s1, p) * square_multiply(s1, s2, p)) % p

s2_ = 15
t = (s2 * expand_gcd(s2_, p)[0]) % p
print(expand_gcd(s2_, p))
print(t)
di = expand_gcd((1 - t) * s1 % p, p)[0]
res = ((m - t * 17) * di) % p
print(res)
print(expand_gcd(5, 18)[0] * 1)
