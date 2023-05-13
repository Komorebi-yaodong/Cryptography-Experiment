"""
弱密钥查找：
即CD两部分全部为0、1
故逆向思维：CD全部为0、1，PC1逆变换得到的即为结果
注意：校验位全为1和全为0两种模式
奇偶校验位为8，16，24，32，40，48，56，64位

半弱密钥查找：
原理：倘若两个密钥生成的子密钥是恰好对称的，
    那么由一个密钥加密的信息可以通过用另一个密钥再次加密来解密。

"""
"""
逆PC1表 生成代码
PC1 = [
        57, 49, 41, 33, 25, 17, 9, 1, 58, 50, 42, 34, 26, 18,
        10, 2, 59, 51, 43, 35, 27, 19, 11, 3, 60, 52, 44, 36,
        63, 55, 47, 39, 31, 23, 15, 7, 62, 54, 46, 38, 30, 22,
        14, 6, 61, 53, 45, 37, 29, 21, 13, 5, 28, 20, 12, 4
    ]

key = []
for i in range(64):
    if (i+1) % 8 == 0:
        key.append(-1)
    else:
        for j in range(56):
            if i+1 == PC1[j]:
                key.append(j+1)
print(key)
"""
from pycallgraph import Config
from pycallgraph import GlobbingFilter
from pycallgraph import PyCallGraph
from pycallgraph.output import GraphvizOutput


def PC_(num, mode):
    k = 0
    PC1_ = [8, 16, 24, 56, 52, 44, 36, -1,
            7, 15, 23, 55, 51, 43, 35, -1,
            6, 14, 22, 54, 50, 42, 34, -1,
            5, 13, 21, 53, 49, 41, 33, -1,
            4, 12, 20, 28, 48, 40, 32, -1,
            3, 11, 19, 27, 47, 39, 31, -1,
            2, 10, 18, 26, 46, 38, 30, -1,
            1, 9, 17, 25, 45, 37, 29, -1]
    judge = 0
    for i in range(64):
        if PC1_[i] != -1:
            distance = 56 - PC1_[i]
            flag = 1 & (num >> distance)
            k = k ^ (flag << (63 - i))
            judge += flag
        else:
            if mode == 1:
                flag = judge % 2
            else:
                flag = ((judge % 2) + 1) % 2
            k = k ^ (flag << (63 - i))
            judge = 0
    return k


def WEAK_KEY():  # 查找弱密钥
    test1 = 0xffffffffffffff
    test2 = 0xfffffff0000000
    test3 = 0x0000000fffffff
    test4 = 0x00000000000000

    weak_key = []
    weak_key_str = []

    test = [test1, test2, test3, test4]

    for i in test:
        k = PC_(i, 0)
        weak_key.append(k)
        k = PC_(i, 1)
        weak_key.append(k)

    weak_key.sort()

    for i in weak_key:
        k = str(hex(i))
        length = len(k)
        while length < 18:
            k = k[0:2] + "0" + k[2:]
            length += 1
        weak_key_str.append(k)

    return weak_key_str


def HALF_WEAK_KEY():  # 查找弱密钥
    test1 = 0x55555550000000
    test2 = 0xaaaaaaa0000000
    test3 = 0x00000005555555
    test4 = 0x0000000aaaaaaa
    test5 = 0xfffffffaaaaaaa
    test6 = 0xfffffff5555555
    test7 = 0xaaaaaaafffffff
    test8 = 0x5555555fffffff
    test9 = 0x5555555aaaaaaa
    testa = 0xaaaaaaa5555555
    testb = 0x55555555555555
    testc = 0xaaaaaaaaaaaaaa

    half_weak_key = []
    half_weak_key_str = []

    test = [
        (test1, test2), (test3, test4), (test5, test6),
        (test7, test8), (test9, testa), (testb, testc)
    ]

    for i in test:
        k1 = PC_(i[0], 0)
        k2 = PC_(i[1], 0)
        half_weak_key.append((k1, k2))
        k1 = PC_(i[0], 1)
        k2 = PC_(i[1], 1)
        half_weak_key.append((k1, k2))

    for i in half_weak_key:
        k1 = str(hex(i[0]))
        length = len(k1)
        while length < 18:
            k1 = k1[0:2] + "0" + k1[2:]
            length += 1
        k2 = str(hex(i[1]))
        length = len(k2)
        while length < 18:
            k2 = k2[0:2] + "0" + k2[2:]
            length += 1

        half_weak_key_str.append((k1, k2))

    return half_weak_key_str


def main():
    m = WEAK_KEY()
    n = HALF_WEAK_KEY()
    for i in m:
        print(i)
    for j in n:
        print(j[0], j[1])


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
    graphviz.output_file = '弱密钥与半弱密钥.png'
    with PyCallGraph(output=graphviz, config=config):
        for i in range(2):
            main()
