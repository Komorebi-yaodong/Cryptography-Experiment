from hashlib import sha1


# def main():
#     n = 24
#     with open('Correct.txt', 'r') as fc_in:
#         with open('Wrong.txt', 'r') as fw_in:
#             with open('common.txt', 'w') as f_out:
#                 c_dir = {}
#                 while True:
#                     s = fc_in.readline()
#                     if s == '':
#                         break
#                     res1 = hex(int(sha1(s.encode('utf-8')).hexdigest(), 16))[2:].rjust(40, '0')[6:]
#                     print(s, res1)
#                     c_dir[res1] = s
#                 while True:
#                     s = fw_in.readline()
#                     if s == '':
#                         break
#                     res2 = hex(int(sha1(s.encode('utf-8')).hexdigest(), 16))[2:].rjust(40, '0')[:6]
#                     print(s, res2)
#                     if res2 in c_dir:
#                         f_out.write(c_dir[res2] + ':' + s + '\n')
#
#
# if __name__ == "__main__":
#     main()

from random import shuffle
