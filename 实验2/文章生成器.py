# -*- coding: utf-8 -*-
def file_deal(file_in, file_out):
    list = "qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM"
    with open(file_in, 'r') as f_in:
        with open(file_out, 'w') as f_out:
            while True:
                s = f_in.read(1)
                if s == "":
                    break
                else:
                    if s in list:
                        f_out.write(s.lower())


file_in = '#the_wealth_of_nations.txt'
file_out = '#the_wealth_of_nations_test.txt'
file_deal(file_in, file_out)
print("over!")
