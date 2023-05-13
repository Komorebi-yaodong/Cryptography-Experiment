import randomness_check
from random import randint

if __name__ == "__main__":
    # s = randint(1, 100000000000000000000)
    s = 20
    z = bin(s)[2:]
    # 频数检测
    print("频数检验".center(75, '='))
    print(randomness_check.f_check(z))

    # poke检测
    print("扑克检验".center(75, '='))
    print(randomness_check.poke_check(z))

    # 游程检测
    print("游程检测".center(75, '='))
    print(randomness_check.R_check(z))

    # 二元推导检测
    print("二元推导检测".center(75, '='))
    print(randomness_check.bd_check(z))

    # 自相关检验
    print("自相关检测".center(75, '='))
    print(randomness_check.a_check(z))
