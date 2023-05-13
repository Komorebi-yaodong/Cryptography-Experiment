# -*- coding: utf-8 -*-

class Mersenne:
    def __init__(self):
        self.w = 32
        self.n = 624
        self.m = 397
        self.r = 31
        self.a = 0x9908b0df
        self.f = 0x6c078965
        self.u_d = (11, 0xffffffff)
        self.s_b = (7, 0x9d2c5680)
        self.t_c = (15, 0xefc60000)
        self.l = 18
        self.MT = [0] * self.n
        self.index = 0

    # def int32(self, x):
    #     return int(0xffffffff & x)

    def seedInit(self, seed):
        self.index = self.n
        self.MT[0] = seed
        for i in range(1, self.n):
            self.MT[i] = 0xffffffff & ((self.f * (self.MT[i - 1] ^ (self.MT[i - 1] >> (self.w - 2)))) + i)

    def twist(self):
        lower_mask = 0x7fffffff
        upper_mask = 0x80000000
        for i in range(self.n):
            x = 0xffffffff & ((self.MT[i] & upper_mask) + (self.MT[(i + 1) % self.n] & lower_mask))
            xA = x >> 1
            if x % 2 != 0:
                xA = xA ^ self.a
            self.MT[i] = self.MT[(i + self.m) % self.n] ^ xA
        self.index = 0

    def extract(self):
        if self.index >= self.n:
            self.twist()
        y = self.MT[self.index]
        y = y ^ ((y >> self.u_d[0]) & self.u_d[1])
        y = y ^ ((y << self.s_b[0]) & self.s_b[1])
        y = y ^ ((y << self.t_c[0]) & self.t_c[1])
        z = y ^ (y >> self.l)
        self.index += 1
        return 0xffffffff & z


def main():
    seed = int(input().strip())
    ram = Mersenne()
    ram.seedInit(seed)
    for i in range(20):
        print(ram.extract())


if __name__ == "__main__":
    main()
