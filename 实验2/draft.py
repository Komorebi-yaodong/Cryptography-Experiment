def encode_2_decode(k):  # k为字符串
    encode = {}
    for i in range(26):
        encode[chr(i + ord('a'))] = k[i]

    decode = {}
    for key in encode:
        decode[encode[key]] = key
    return decode


if __name__ == "__main__":
    """
    abcdefghijklynopqrstuvwxmz
    abmdefghijklcnopqrstuvwxyz
    apmdefghijklcnobqrstuvwxyz
    abcdefghijklmnopqrstuvwxyz
    abmdefghijklcnopqrstuvwxyz
    1.b p y
    2.c m 
    b:p 4/5
    y:m 4/5
    c:m 1/5
    """
    file_in = "#attack_single_table.txt"
    file_out = "#attack_single_table_answer.txt"
    k2 = "laksjdhfgpzoxicuvmqnwberyt"
    decode = encode_2_decode(k2)
    with open(file_in, 'r') as f:
        with open(file_out, 'w') as f_out:
            s = f.read()
            for i in s:
                f_out.write(decode[i])
