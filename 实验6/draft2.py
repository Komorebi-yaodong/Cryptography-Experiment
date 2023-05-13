# x = 2443250962
# y = x ^ ((x >> 11) & 0xffffffff)
# y = y ^ ((y << 7) & 0x9d2c5680)
# y = y ^ ((y << 15) & 0xefc60000)
# # z = y ^ (y >> 1)
# z = y ^ (y >> 18)
# print(z)

mt6 = 4042607538
mt5 = 2481403966
mt402 = 2428868268

lower_mask = 0x7fffffff
upper_mask = 0x80000000
print(bin(mt5))
print(bin(mt6))

# print("low %08x" % (mt6))
x = ((mt5 & upper_mask) + (mt6 & lower_mask)) & 0xffffffff
print("high %08x" % (mt5 & upper_mask))
print("low %08x" % (mt6 & lower_mask))
xA = x >> 1
if x % 2 != 0:
    xA = xA ^ 0x9908b0df
mt5 = mt402 ^ xA
print(mt5)
