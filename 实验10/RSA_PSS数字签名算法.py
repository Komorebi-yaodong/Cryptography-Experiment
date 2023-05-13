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


def rsa_code(m, salt, embits):
    bc = 'bc'
    emlen = embits // 8
    if embits % 8 != 0:
        emlen += 1
    h_len = s_len = 20  # 字节
    padding1 = '0000000000000000'
    padding2 = '00' * (emlen - s_len - h_len - 2) + '01'
    mhash = sha1(m.encode('utf-8')).hexdigest()
    # print('mhash', mhash)
    M = padding1 + mhash + salt
    # print('M1', M)
    H = sha1(bytearray().fromhex(M)).hexdigest()
    # print('H', H)
    DB = padding2 + salt
    # print('DB', DB)
    lengtth = len(DB) // 2
    DBmask = mgf(H, emlen - h_len - 1)
    # print('DBmask', DBmask)
    masked_DB = hex(int(DB, 16) ^ int(DBmask, 16))[2:].rjust((emlen - h_len - 1) * 2, '0')
    # print('maskedDB', masked_DB)
    EM = masked_DB + H + bc
    # print('EM', EM)

    return EM


def rsa_pss(m, n, embits, mode, link):
    emlen = embits // 8
    if embits % 8 != 0:
        emlen += 1
    h_len = s_len = 20  # 字节
    padding1 = '0000000000000000'
    padding2 = '00' * (emlen - s_len - h_len - 1) + '01'
    if mode == 'Sign':
        d = link[0]
        salt = link[1]
        M = int(rsa_code(m, salt, embits), 16)
        s = square_multiply(M, d, n)
        length = len(hex(n)[2:])
        if length & 1 == 1:
            length += 1
        k = length // 2
        s = hex(s)[2:].rjust(2 * k, '0')
        return s
    elif mode == 'Vrfy':
        e = link[0]
        s = link[1]
        EM = hex(square_multiply(s, e, n))[2:].rjust(emlen * 2, '0')
        mhsah = sha1(m.encode('utf-8')).hexdigest()
        masked_DB_len = emlen - h_len - 1
        masked_DB = EM[:masked_DB_len * 2]
        H = EM[masked_DB_len * 2:2 * (masked_DB_len + h_len)]
        DBmask = mgf(H, masked_DB_len)
        DB = hex(int(DBmask, 16) ^ int(masked_DB, 16))[2:].rjust(masked_DB_len * 2, '0')
        salt = DB[2 * (emlen - 2 * h_len - 1):]
        M = padding1 + mhsah + salt
        H_ = sha1(bytearray().fromhex(M)).hexdigest()
        if H == H_:
            return True
        else:
            return False
    else:
        print('mode wrong')
        return None


def main():
    m = input().strip()
    n = int(input().strip())
    emBits = int(input().strip())
    mode = input().strip()
    if mode == 'Sign':
        d = int(input().strip())
        salt = input().strip()
        ans = rsa_pss(m, n, emBits, mode, [d, salt])
        print(ans)
    elif mode == 'Vrfy':
        e = int(input().strip())
        s = int(input().strip(), 16)
        ans = rsa_pss(m, n, emBits, mode, [e, s])
        print(ans)
    else:
        print('mode wrong')
        return None


if __name__ == "__main__":
    main()