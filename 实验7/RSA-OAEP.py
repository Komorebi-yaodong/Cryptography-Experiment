from hashlib import sha1
from pycallgraph import Config
from pycallgraph import GlobbingFilter
from pycallgraph import PyCallGraph
from pycallgraph.output import GraphvizOutput

def square_multiply(a, n, m):  # 平方乘算法
    t = a % m
    result = 1
    judge = 1
    while n > 0:
        if judge & n:
            result = (result * t) % m
        n = n >> 1
        t = (t * t) % m
    return result


def mgf(msgseed: str, masklen: int):
    res = bytearray(b'')
    h_len = 20
    if masklen > (2 ** 32) * h_len:
        return None
    else:
        length = masklen // h_len
        if masklen % h_len == 0:
            length -= 1
        if len(msgseed) & 1 == 1:
            msgseed = '0' + msgseed
        msgseed_bytes = bytearray.fromhex(msgseed)
        for i in range(2 * (length + 5)):
            tmp = msgseed_bytes + bytearray.fromhex('%08x' % i)
            res = res + bytearray.fromhex(sha1(tmp).hexdigest().rjust(h_len * 2, '0'))
        res = res[:masklen]
        return res.hex().rjust(2 * masklen, '0')


def rsaep(n, e, m):
    if not 0 <= m <= n - 1:
        return None
    else:
        c = square_multiply(m, e, n)
        return c


def rsa_oaep(op, k, e, N, text, L, Seed: str):
    if op == 1:
        # 长度检查
        h_len = 20
        m_len = len(text) // 2
        l_len = len(L)
        if l_len > (2 << 61) - 1:
            print("Err")
            return None
        # print('m_len:', m_len)
        if m_len > k - 2 * h_len - 2:
            print("Err")
            return None
        # EME-OAEP编码
        lhash = sha1(bytearray.fromhex(L)).hexdigest().rjust(2 * h_len, '0')
        ps_len = k - m_len - 2 * h_len - 2
        ps = ''.rjust(2 * ps_len, '0')
        db = lhash + ps + '01' + text
        # print('db:', db)

        db_mask = mgf(Seed, k - h_len - 1)
        # print('db_mask:', db_mask)
        if db_mask is None:
            print("Err")
            return None
        masked_db = hex(int(db, 16) ^ int(db_mask, 16))[2:].rjust((k - h_len - 1) * 2, '0')
        # print('masked_db:', masked_db)
        seed_mask = mgf(masked_db, h_len)
        # print('seed_mask', seed_mask)
        if seed_mask is None:
            print("Err")
            return None
        masked_seed = hex(int(Seed, 16) ^ int(seed_mask, 16))[2:].rjust(h_len * 2, '0')
        # print('masked_seed:', masked_seed)
        em = '00' + masked_seed + masked_db

        # RSA加密
        m = int(em, 16)
        if m == 0:
            print("Err")
            return None
        c = rsaep(N, e, m)
        if c is None:
            print('Err')
            return None
        res = hex(c)[2:].rjust(2 * k, '0')
        res = '0x' + res
        return res

    else:
        # 长度检查
        h_len = 20
        c_len = len(text)
        # print('c_len:', c_len)
        if c_len != k * 2 or k <= 2 * h_len + 2:
            print("Ree")
            return None
        # RSA解密
        c = int(text, 16)
        m = rsaep(N, e, c)
        if m is None:
            print("Ree")
            return None
        em = hex(m)[2:].rjust(2 * k, '0')
        # EME-OAEP编码
        lhash = sha1(bytearray.fromhex(L)).hexdigest().rjust(2 * h_len, '0')
        # print('lhash:', lhash)
        y = em[0] + em[1]
        # print('y:', y)
        masked_seed = em[2:2 + h_len * 2]
        # print('masked_seed:', masked_seed)
        masked_db = em[2 + h_len * 2:]
        # print('masked_db:', masked_db)
        seed_mask = mgf(masked_db, h_len)
        # print('seed_mask:', seed_mask)
        if seed_mask is None:
            print("Ree")
            return None
        seed = ("%040x" % (int(masked_seed, 16) ^ int(seed_mask, 16)))
        # print('seed:', seed)
        db_mask = mgf(seed, k - h_len - 1)
        # print('db_mask:', db_mask)
        if db_mask is None:
            print("Ree")
            return None
        db = hex(int(masked_db, 16) ^ int(db_mask, 16))[2:].rjust((k - h_len - 1) * 2, '0')
        # print('db:', db)
        lhash_ = db[0:2 * h_len]
        # print('lhash_:', lhash_)
        if y != '00' or lhash_ != lhash:
            print("Ree")
            return None
        remain = db[2 * h_len:]
        pace = 0
        for i in range(len(remain)):
            if remain[i] == '1':
                pace += 1
                break
            else:
                pace += 1
                if remain[i] != '0':
                    print("Ree")
                    return None
        if pace & 1 != 0:
            print("Ree")
            return None
        m = int(remain[pace:], 16)
        if m == 0:
            print("Ree")
            return None
        M = hex(m)
        # print(M)
        return M


def main():
    op = int(input().strip())
    k = int(input().strip())
    e = int(input().strip(), 16)
    N = int(input().strip(), 16)
    text = input().strip()[2:]
    L = input().strip()[2:]

    Seed = ''
    if op == 1:
        Seed = input().strip()[2:]

    ans = rsa_oaep(op, k, e, N, text, L, Seed)

    if ans is not None:
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
    graphviz.output_file = 'RSA-OAEP.png'
    with PyCallGraph(output=graphviz, config=config):
        for i in range(4):
            main()
