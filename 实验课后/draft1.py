# for x in range(8):
#     res = 0
#     for i in range(7):
#         res = (res + (x ** i)) % 8
#     print(res % 8)
#     if res % 8 == 0:
#         print(x)
# print('over')

for x in range(8):
    res = x ** 7 + -1
    if res % 8 == 0:
        print(x)
