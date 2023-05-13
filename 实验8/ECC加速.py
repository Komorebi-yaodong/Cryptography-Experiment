p = int(input().strip())
a = int(input().strip())
b = int(input().strip())


def exgcd(m, n):
    if n == 0:
        return 1, 0, m
    else:
        x, y, q = exgcd(n, m % n)
        x, y = y, (x - (m // b) * y)

    x = x % n // q
    if q < 0:
        q = -q
    y = (q - m * x) // n
    return x, y, q


def ecc_add(A, B):
    x, y = 0, 0
    if A[0] == B[0] and A[1] + B[1] == 0:
        return [x, y]
    elif A[0] == A[1] and A[1] == 0:
        return B
    elif B[0] == B[1] and B[1] == 0:
        return A
    else:
        if A != B:
            delta = ((B[1] - A[1]) * (exgcd(B[0] - A[0], p)[0])) % p
        else:
            delta = ((3 * A[0] * A[0] + a) * (exgcd(2 * A[1], p)[0])) % p
        x = (delta * delta - A[0] - B[0]) % p
        return [x, (delta * (A[0] - x) - A[1]) % p]


def ecc_mul(A, k):
    res = [0, 0]
    reg = A
    while k > 0:
        if k & 1 == 1:
            res = ecc_add(res, reg)
        reg = ecc_add(reg, reg)
        k = k >> 1
    return res


L = input().strip().split()
G = [int(L[0]), int(L[1])]
op = int(input().strip())
if op == 1:
    L = input().strip().split()
    P = [int(L[0]), int(L[1])]
    k = int(input().strip())
    L = input().strip().split()
    PB = [int(L[0]), int(L[1])]
    N = int(input().strip())

    k_PA = ecc_mul(PB, (N + 1) * k)
    k_G = ecc_mul(G, k)
    ans = ecc_add(P, k_PA)

    print(k_G[0], k_G[1])
    print(ans[0], ans[1])

else:
    L = input().strip().split()
    C1 = [int(L[0]), int(L[1])]
    L = input().strip().split()
    C2 = [int(L[0]), int(L[1])]
    nb = int(input().strip())
    N = int(input().strip())

    kP = ecc_mul(C1, (N + 1) * nb)
    kP[1] = -kP[1]
    ans = ecc_add(C2, kP)
    print(ans[0], ans[1])
