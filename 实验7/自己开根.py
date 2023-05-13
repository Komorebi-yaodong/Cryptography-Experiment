def my_root(x, n):  # 正整数范围内
    left = 1
    right = x
    mid = (left + right) // 2
    judge = (mid ** n) - x
    while judge != 0:
        if judge < mid:
            left = mid
        elif judge > mid:
            right = mid
        else:
            break
        mid = (left + right) // 2
        print(left, mid, right)
        judge = (mid ** n) - x
    return mid


if __name__ == "__main__":
    a = 13
    n = 100
    x = a ** n
    print(x)
    root_x = my_root(x, n)
    print(root_x)
