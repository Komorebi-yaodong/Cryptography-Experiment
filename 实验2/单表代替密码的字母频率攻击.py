# -*- coding: utf-8 -*-


def tail_statistic(s, c):
    table = {}
    length = len(s)
    for i in range(length - 1):
        if s[i] == c:
            if s[i + 1] not in table:
                table[s[i + 1]] = 1
            else:
                table[s[i + 1]] += 1
    result = sorted(table, key=lambda x: table[x], reverse=True)
    return result


def tail_attack(s, k):
    """
    据统计，j,q,后跟随的字母数很少
    """
    table = []  # [['a',长度],['a',长度],......]
    for i in range(26):
        c = chr(i + ord('a'))
        tail = tail_statistic(s, c)
        length = len(tail)
        table.append([c, length])
    result = sorted(table, key=lambda x: x[1])
    # q:result[0][0] , j:result[1][0]
    if result[0][1] <= 20:  # q
        m = k[16]
        for i in range(26):
            if k[i] == result[0][0]:
                break
        k[16] = result[0][0]
        k[i] = m
    if result[1][1] <= 20:
        m = k[9]
        for i in range(26):
            if k[i] == result[1][0]:
                break
        k[9] = result[1][0]
        k[i] = m


def word_find_tail(s, word):  # 单词查找攻击 返回['','']
    table = {}
    length = len(s)
    for i in range(2, length - 2):
        if s[i:i + 2] == word:
            c = s[i - 1]
            if c not in table:
                table[c] = 1
            else:
                table[c] += 1
    result = sorted(table, key=lambda x: table[x], reverse=True)

    return result


def word_find_head(s, word):  # 单词查找攻击 返回['','']
    table = {}
    length = len(s)
    for i in range(2, length - 2):
        if s[i - 2:i] == word:
            c = s[i]
            if c not in table:
                table[c] = 1
            else:
                table[c] += 1
    result = sorted(table, key=lambda x: table[x], reverse=True)

    return result


def word_find_body(s, word):  # 单词查找攻击 返回['','']
    table = {}
    length = len(s)
    for i in range(2, length - 2):
        if s[i - 1] == word[0] and s[i + 1] == word[1]:
            c = s[i]
            if c not in table:
                table[c] = 1
            else:
                table[c] += 1
    result = sorted(table, key=lambda x: table[x], reverse=True)

    return result


def first_order_attack(s):
    """
    a,b,d,e,l,o,p,q,t,z
    a,b,d,e,l,n,o,p,r,t,y
    a,b,d,e,g,i,k,l,n,o,p,q,r,t,z
    a,b,d,e,l,m,n,o,p,q,r,t,y,z
    d,e,f,g,k,l,t,v,w,x,y,z
    大概率：a,b,d,e,l,n,o,p,t,z
    共同：d,e,l,t
    """
    order = [2, 19, 12, 9, 0, 15, 16, 7, 4, 22, 21, 10, 13, 5, 3, 18, 24, 8, 6, 1, 11, 20, 14, 23, 17, 25]
    table = []
    for i in range(26):
        table.append([chr(i + ord('a')), 0])
    for c in s:
        num = ord(c) - ord('a')
        table[num][1] += 1
    table = sorted(table, key=lambda x: x[1], reverse=True)
    # print("一阶词频统计：", table)
    result = []
    for i in order:
        result.append(table[i][0])
    # print("一阶词频统计：", result)
    return result


def second_order_attack(s, k):
    """
    0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25
    a b c d e f g h i j k  l  m  n  o  p  q  r  s  t  u  v  w  x  y  z
    一阶：
    大概率：a,b,d,e,l,n,o,p,t,z
    共同：d,e,l,t

    二阶：th,he,in,er,an,re,ed,on,es,st
    可确定：a,b,d,e,l,n,o,p,t,z + h,i,r

    三阶：the,ing,and,her,ere,ent,tha,nth,was
    可确定：a,b,d,e,l,n,o,p,t,z + h,i,r + g
    """
    # 三阶统计
    table2 = {}
    for i in range(2, len(s)):
        double = s[i - 2:i + 1]
        if double not in table2:
            table2[double] = 0
        else:
            table2[double] += 1
    dic = sorted(table2, key=lambda x: table2[x], reverse=True)
    # print(dic)

    for c in dic[0:4]:  # and 的 a和n
        if k[3] == c[2]:
            m = k[0]
            for i in range(26):
                if k[i] == c[0]:
                    break
            k[0] = c[0]
            k[i] = m
            m = k[13]
            for i in range(26):
                if k[i] == c[1]:
                    break
            k[13] = c[1]
            k[i] = m
            break
    print("三阶词频统计完成".center(75, '-'))

    # 二阶统计
    table = {}
    for i in range(1, len(s)):
        double = s[i - 1:i + 1]
        if double not in table:
            table[double] = 0
        else:
            table[double] += 1
    dic = sorted(table, key=lambda x: table[x], reverse=True)
    for double in dic[0:4]:  # th_he_in_er
        if k[4] == double[1]:  # he 的 h
            m = k[7]
            for i in range(26):
                if k[i] == double[0]:
                    break
            k[7] = double[0]
            k[i] = m
        if k[4] == double[0]:  # er 的 r
            m = k[17]
            for i in range(26):
                if k[i] == double[1]:
                    break
            k[17] = double[1]
            k[i] = m
        if k[19] == double[0]:  # th 的 h
            m = k[7]
            for i in range(26):
                if k[i] == double[1]:
                    break
            k[7] = double[1]
            k[i] = m
        if k[13] == double[1]:  # in 的 i
            m = k[8]
            for i in range(26):
                if k[i] == double[0]:
                    break
            k[8] = double[0]
            k[i] = m

    print("二阶词频统计完成".center(75, '-'))

    # 跟随字母长度统计攻击 j,q,后跟随的字母数很少
    tail_attack(s, k)

    print("跟随字母长度统计完成".center(75, '-'))

    # 单词查找攻击
    # w+as
    word = k[0] + k[18]
    c_list = word_find_tail(s, word)
    # print(c_list)
    if c_list[0] != k[4]:
        m = k[22]

        for i in range(26):
            if k[i] == c_list[0]:
                break
        k[22] = c_list[0]
        k[i] = m
    else:
        m = k[22]

        for i in range(26):
            if k[i] == c_list[1]:
                break
        k[22] = c_list[1]
        k[i] = m
    # f + or
    word = k[14] + k[17]
    c_list = word_find_tail(s, word)
    m = k[5]
    for i in range(26):
        if k[i] == c_list[0]:
            break
    k[5] = c_list[0]
    k[i] = m

    # v + er
    word = k[4] + k[17]
    c_list = word_find_tail(s, word)
    for i in range(4):
        if c_list[i] != k[7] and c_list[i] != k[19] and c_list[i] != k[22]:
            m = k[21]

            for j in range(26):
                if k[j] == c_list[i]:
                    break
            k[21] = c_list[i]
            k[j] = m
            break
    # in+g (int干扰)
    word = k[8] + k[13]
    c_list = word_find_head(s, word)
    for i in range(2):
        if c_list[i] != k[19]:
            m = k[6]
            for j in range(26):
                if k[j] == c_list[i]:
                    break
            k[6] = c_list[i]
            k[j] = m
            break

    # b+u+t (bet干扰)
    word = k[1] + k[19]
    c_list = word_find_body(s, word)
    # print(c_list)
    for i in range(2):
        if c_list[i] != k[4] and c_list[i] != k[0]:
            m = k[20]
            for j in range(26):
                if k[j] == c_list[i]:
                    break
            k[20] = c_list[i]
            k[j] = m
            break

    print("单词查找统计完成".center(75, '-'))

    return k


def change(k, l, r):
    a = k[:]
    m = a[l]
    a[l] = a[r]
    a[r] = m
    return a


def single_table_attack(s):
    """
    0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25
    a b c d e f g h i j k  l  m  n  o  p  q  r  s  t  u  v  w  x  y  z
    abcdefghijklynopqrstuvwxmz
    abmdefghijklcnopqrstuvwxyz
    apmdefghijklcnobqrstuvwxyz
    abcdefghijklmnopqrstuvwxyz
    abmdefghijklcnopqrstuvwxyz
    b:p 1/5
    y:m 1/5
    c:m 3/5
    """
    result_1 = first_order_attack(s)
    print("一阶词频统计完成".center(75, '-'))
    result_2 = second_order_attack(s, result_1)
    result = []
    # 概率排序 a0 a1 a2 a3 a4 a5 a6 a7 a8
    a0 = result_2[:]  # 4*4*2
    a1 = change(result_2, 2, 12)  # 1:4*4*3
    a2 = change(result_2, 12, 24)  # 1:4*1*2
    a3 = change(result_2, 1, 15)  # 1:4*1*2
    a4 = change(a1, 12, 24)  # 2:1*4*2
    a5 = change(a1, 1, 15)  # 2:1*4*3
    a6 = change(a2, 2, 12)  # 2:1*4*3
    a7 = change(a2, 1, 15)  # 2:1*1*2
    a8 = change(a3, 12, 24)  # 2:1*1*2
    a9 = change(a8, 2, 12)  # 3:3*1*1

    print("概率统计完成".center(75, '-'))

    result.append(a1)
    result.append(a0)
    result.append(a6)
    result.append(a5)
    result.append(a2)
    result.append(a3)
    result.append(a4)
    result.append(a9)
    result.append(a7)
    result.append(a8)

    return result


def main():
    n = 1
    file_name = "#attack_single_table.txt"
    with open(file_name, 'r') as f:
        s = f.read()
    ans = single_table_attack(s)
    for line in ans:
        for e in line:
            print(e, end='')
        print()


if __name__ == "__main__":
    main()
